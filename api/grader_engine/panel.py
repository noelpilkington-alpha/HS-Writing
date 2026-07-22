"""Panel-of-experts grading engine.

Implements the panel → judge architecture from the AlphaTest reference spec:
1. Preflight gates (deterministic, zero LLM cost)
2. Rubric panel (parallel LLM calls, one per scoring dimension)
3. Judge/synthesis (single LLM call combining panel outputs)

Each panel grader sees ONLY its dimension's rubric — no cross-contamination.
The judge sees all panel evidence and can override with explanation.
Feedback is generated AFTER scores are finalized.

Supports all four AlphaTest writing question types:
- Q1-Q5 sentence-revision (G3-G5): Skill Application (0-1) + Conventions (0-1) = 2 pts
- Q6-Q10 sentence-writing (G3-G5): Answer Quality (0-2) + Conventions (0-1) = 3 pts
- Q11 paragraph (G3-G5): Ideas & Organization (0-15) + Conventions (0-5) = 20 pts
- Q11 essay (G6-G8): Structure (0-5) + Evidence (0-5) + Organization (0-4) + Sentences (0-3) + Editing (0-3) = 20 pts

Usage:
    from grader.engine.panel import score_panel
    result = score_panel(client, grade=3, passage=..., question=..., response=..., qnum=6)
"""

from __future__ import annotations

import logging
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

from .models import QuestionScore, sub_maxes
from .scorer import _api_call_with_retry, _parse_json

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class RubricDimension:
    id: str
    name: str
    max_points: int
    prompt: str
    model: str | None = None
    temperature: float | None = None


@dataclass
class PanelResult:
    id: str
    score: int
    evidence: list[str]
    reasoning: str


@dataclass
class SynthesisResult:
    total_score: int
    max_score: int
    category_scores: dict[str, int]
    overrides: dict[str, str]
    feedback: str
    reasoning: str


# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════

SYSTEM_RUBRIC = (
    "You are a single-dimension writing grader on a panel of experts. "
    "You evaluate ONE rubric category. Stay narrowly focused on that category. "
    "You will be shown the full task overview, the student's passage / prompt / submission, "
    "and your specific rubric. Return only the structured JSON requested."
)

SYSTEM_SYNTHESIS = (
    "You are the head judge of a writing-grading panel. Each panel member has scored "
    "one rubric category. Your job is to combine those recommendations into a final "
    "score and a single, kind, student-facing feedback message. You may override panel "
    "scores when warranted (e.g. evidence inconsistencies). "
    "Return only the structured JSON requested."
)


# ═══════════════════════════════════════════════════════════════════════════════
# PREFLIGHT GATES
# ═══════════════════════════════════════════════════════════════════════════════

def _preflight(response: str) -> str | None:
    """Deterministic preflight check. Returns gate reason or None if passes."""
    trimmed = (response or "").strip()
    if not trimmed:
        return "empty"

    cleaned = re.sub(r"<[^>]+>", " ", trimmed)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if not cleaned:
        return "empty"

    no_spaces = cleaned.replace(" ", "")
    if len(no_spaces) < 2:
        return "gibberish"

    unique_chars = set(no_spaces.lower())
    if len(unique_chars) <= 2 and len(no_spaces) > 4:
        return "gibberish"

    tokens = cleaned.split()
    if len(tokens) >= 3:
        unique_tokens = set(t.lower() for t in tokens)
        if len(unique_tokens) == 1:
            return "gibberish"
        if len(unique_tokens) <= 2 and all(len(t) <= 2 for t in tokens):
            return "gibberish"

    if len(no_spaces) >= 12:
        vowels = len(re.findall(r"[aeiouAEIOU]", no_spaces))
        if vowels / len(no_spaces) < 0.18:
            return "gibberish"

    return None


# ═══════════════════════════════════════════════════════════════════════════════
# MODEL / CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

def _default_panel_model() -> str:
    explicit = os.environ.get("ALPHA_PANEL_MODEL", "").strip()
    if explicit:
        return explicit
    provider = os.environ.get("ANTHROPIC_PROVIDER", "anthropic").strip().lower()
    if provider == "anthropic":
        return "claude-opus-4-8"
    return "us.anthropic.claude-opus-4-8"


def _model_supports_temperature(model: str) -> bool:
    # Opus 4.7 AND 4.8 reject non-default temperature/top_p/top_k (400). The panel
    # only sends temperature=1 (the default, accepted everywhere), so this gate is
    # belt-and-suspenders — but keep it correct for both model families.
    m = model or ""
    return "opus-4-7" not in m and "opus-4-8" not in m


def _age_hint(grade: int) -> str:
    if grade <= 4:
        return "approximately 8-10 years old"
    elif grade <= 6:
        return "approximately 10-12 years old"
    elif grade <= 8:
        return "approximately 12-14 years old"
    # high school (G9-12): STAAR English I/II + AP; students ~14-18. Added 2026-07-12 for the HS Writing courses.
    return "approximately 14-18 years old (high school)"


# ═══════════════════════════════════════════════════════════════════════════════
# RUBRIC PROMPTS — Q1-Q5 SENTENCE REVISION
# ═══════════════════════════════════════════════════════════════════════════════

_REVISION_INTRO = """You are an experienced writing grader assigned to score a Grade {grade} student's response to a short sentence-revision task.

For this task, the student was shown a short passage with numbered sentences and was asked to rewrite one specific sentence by applying a particular writing skill — combining sentences with a conjunction, adding an appositive, fixing a fragment, rewriting a sentence as a question, and so on. You will receive the source passage, the exact instruction the student was given, and the one-sentence revision the student wrote. Your job — together with the rest of the grading panel — is to evaluate the revision carefully and award a score that reflects how well the student applied the requested skill.

The revision is scored out of 2 total points across two dimensions:

- Skill Application (0-1): did the student correctly apply the requested writing skill?
- Writing Conventions (0-1): grammar, spelling, punctuation, capitalization.

The student is {age_hint}. Reward thoughtful, age-appropriate work."""

_SKILL_APPLICATION_PROMPT = """Score Skill Application on a 0-1 scale.

The student has been asked to rewrite a specific numbered sentence by applying a particular writing skill — for example, combining sentences with a conjunction, adding an appositive, fixing a fragment, rewriting a sentence as a question, or putting a sentence in clearer order. The point of this category is whether the student CORRECTLY APPLIED THE REQUESTED SKILL.

🔑 FIRST classify the skill the task asks for — STRUCTURAL vs QUALITY-LADEN — then apply the matching bar:

STRUCTURAL skills (the task names a specific transformation): combine sentences with a conjunction, add
an appositive, rewrite as a question, expand a fragment into a complete sentence, change sentence type.
For these, score the TRANSFORMATION ONLY:
- 1: the transformation is correctly performed (it IS a question / IS now complete / DOES contain an
  appositive / IS combined) and meaning is not materially reversed. Do NOT dock for awkward word choice,
  a slightly odd verb, or imperfect style — those are not skill failures here. (e.g. "His dedication
  provided a great impact" expands the fragment into a complete sentence → skill met, even if "provided"
  is an odd verb.)
- 0: the transformation is NOT performed (still a statement when a question was asked; no appositive
  present; still a fragment), or meaning is materially changed/reversed.

QUALITY-LADEN skills (the task asks to "revise to be clear and effective", "make it clearer/concise",
"improve" the sentence): here the GOAL is quality, so semantic appropriateness counts:
- 1: the revision genuinely makes the sentence clear, correct, and effective.
- 0: the revision fails to improve clarity, introduces a new error, or remains awkward/unclear.

If unsure which type, read the task verb: "rewrite as / combine / add / expand / change" = STRUCTURAL;
"revise / improve / make clear / make concise" = QUALITY-LADEN.

Output evidence as a list of short observations (e.g. "skill type: STRUCTURAL (rewrite-as-question)", "is a question: yes", "transformation correct"). Output reasoning as 1-2 sentences naming the skill type and the call."""

_REVISION_CONVENTIONS_PROMPT = """Score Writing Conventions on a 0-1 scale, focused on the single sentence the student wrote.

CLARITY IS THE GATE, not error count (aligned with the validated paragraph/essay conventions standard):
- 1: A reader can read the sentence smoothly and the meaning is never in doubt. A few errors — even
  several minor slips (spelling, a missing comma, a capitalization lapse) — do NOT cost the point as long
  as clarity holds. When clarity is intact, award 1; do not dock for error presence alone.
- 0: ONLY when the sentence fails as a sentence — it is a fragment/run-on, OR errors actually impede
  clarity (the reader must stop and reconstruct meaning, or words are merged/garbled like "becausethye"),
  OR the errors are so dense (roughly 3+ distinct errors in this one sentence) that the student shows no
  command of sentence-level conventions even if the meaning is technically recoverable.

Default to 1 for a readable sentence; reserve 0 for genuine failure of sentence-level control. This is a
single-sentence skill item, so the high-error ceiling (the 3+ clause) is the backstop — but a clean,
clear sentence with one or two slips is a 1, not a 0.

Output evidence as a list of categorized observations (e.g. "spelling: clean", "punctuation: missing question mark", "clarity: reader can understand smoothly"). Output reasoning as 1 sentence; state whether clarity was impeded."""


# ═══════════════════════════════════════════════════════════════════════════════
# RUBRIC PROMPTS — Q6-Q10 SENTENCE WRITING
# ═══════════════════════════════════════════════════════════════════════════════

_SENTENCE_WRITING_INTRO = """You are an experienced writing grader assigned to score a Grade {grade} student's response to a short open-ended writing task.

For this task, the student read a short passage and was then asked an open-ended question about its topic. The student was asked to respond with a single sentence that includes both a clear answer and a supporting reason, explanation, or example. You will receive the source passage, the exact question the student was asked, and the one-sentence response the student wrote. Your job — together with the rest of the grading panel — is to evaluate the response carefully and award a score that reflects how well the student answered.

The response is scored out of 3 total points across two dimensions:

- Answer Quality (0-2): clearly answers the question + provides a reason, explanation, or example.
- Writing Conventions (0-1): grammar, spelling, punctuation, capitalization.

The student is {age_hint}. Reward thoughtful, age-appropriate work."""

_ANSWER_QUALITY_PROMPT = """Score Answer Quality on a 0-2 scale.

The student has been asked an open-ended question that should be answered in ONE sentence. A strong answer (a) directly addresses the specific question asked, AND (b) provides a reason, explanation, or concrete example supporting the answer. Both halves matter.

Score bands:
- 2: Clearly answers the question AND offers a reason / explanation / example. The reason can be brief but must be present and connected to the answer.
- 1: Answers the question but offers no reason or only a vague restatement; OR provides a reason but the answer itself is unclear or only partially addresses the prompt; OR the answer is on-topic but tangential to the specific question asked.
- 0: Off-topic, factually contradicts the prompt's spirit (e.g. advocates the opposite of what was asked), unintelligible, or refuses.

WHAT COUNTS AS A "REASON": A reason must explain WHY, HOW, or WHAT HAPPENS AS A RESULT. It must add information beyond restating the event. Examples:
- "did the right thing" = vague restatement (score 1), NOT a reason
- "because it showed she respected nature" = reason (score 2)
- "she saw nature" = vague restatement of the premise (score 1)
- "the breeze and birds made her feel calm" = specific reason (score 2)

Be generous about age-appropriate phrasing — a Grade 3 student writing "I would feed them so they grow strong" satisfies both the answer and the reason.

🔑 ONE-SENTENCE RULE (the task asks for ONE sentence): if the student wrote MULTIPLE sentences, grade
ONLY THE FIRST sentence. The answer AND its reason/explanation/example must BOTH be present in that first
sentence to earn 2. If the first sentence only states the answer and the reason appears only in a later
sentence, the response earns at most 1 — the student did not meet the one-sentence requirement.
(Example: "My favorite thing is to read to them. I like this because animals don't judge you." → grade
sentence 1 only; it answers but gives no reason → 1, not 2.) A single sentence that contains both halves
(answer + reason, e.g. joined with "because") earns 2 normally.

Output evidence as a list of short observations (e.g. "answer: 'I'd ignore it and continue eating'", "reason given: 'hoping the owner would address it'", "wrote 1 sentence" or "wrote 2 sentences — graded first only"). Output reasoning as 1-2 sentences."""

_WRITING_CONVENTIONS_PROMPT = """Score Writing Conventions on a 0-1 scale, focused on the single sentence the student wrote.

CLARITY IS THE GATE, not error count (aligned with the validated paragraph/essay conventions standard):
- 1: A reader can read the sentence smoothly and the meaning is never in doubt. A few errors — even
  several minor slips (spelling, a missing comma, a capitalization lapse) — do NOT cost the point as long
  as clarity holds. When clarity is intact, award 1; do not dock for error presence alone.
- 0: ONLY when the sentence fails as a sentence — it is a fragment/run-on, OR errors actually impede
  clarity (the reader must stop and reconstruct meaning, or words are merged/garbled like "becausethye"),
  OR the errors are so dense (roughly 3+ distinct errors in this one sentence) that the student shows no
  command of sentence-level conventions even if the meaning is technically recoverable.

Default to 1 for a readable sentence; reserve 0 for genuine failure of sentence-level control. This is a
single-sentence skill item, so the high-error ceiling (the 3+ clause) is the backstop — but a clean,
clear sentence with one or two slips is a 1, not a 0.

Output evidence as a list of categorized observations (e.g. "spelling: one error 'becuase'", "punctuation: clean", "clarity: reader can understand smoothly"). Output reasoning as 1 sentence; state whether clarity was impeded."""


# ═══════════════════════════════════════════════════════════════════════════════
# RUBRIC PROMPTS — Q11 PARAGRAPH (G3-G5)
# Uses STAAR-calibrated prompts from per_cat.py
# ═══════════════════════════════════════════════════════════════════════════════

_PARAGRAPH_INTRO = """You are an experienced writing grader assigned to score a Grade {grade} student's response to a short writing task.

For this task, the student read a short text and then wrote a single well-organized paragraph in response to a specific question about that text. You will receive the source text, the exact question the student was asked, and the paragraph the student wrote. Your job — together with the rest of the grading panel — is to evaluate the paragraph carefully and award a score that reflects how well the student responded.

The paragraph is scored out of 20 total points across two dimensions:

- Ideas & Organization (0-15): central idea, passage-grounded reasoning, organization, depth.
- Writing Conventions (0-5): grammar, spelling, punctuation, sentence structure.

The student is {age_hint}. Reward thoughtful, age-appropriate work; do not penalize for sophistication beyond what the rubric demands."""

# Import the STAAR-calibrated prompts from per_cat
from .per_cat import G35_IDEAS as _G35_IDEAS_RAW, G35_CONVENTIONS as _G35_CONVENTIONS_RAW

# Adapt per-cat prompts to panel format (remove the {response}/{passage}/{prompt} placeholders
# since the panel framework inserts these via the standard sections structure)
def _adapt_percat_prompt(raw_prompt: str) -> str:
    """Strip the INPUT section from per-cat prompts (panel framework handles inputs)."""
    # Remove everything after "OUTPUT — valid JSON only:" and replace with panel output instruction
    output_idx = raw_prompt.find("OUTPUT — valid JSON only:")
    if output_idx == -1:
        output_idx = raw_prompt.find("OUTPUT —")
    if output_idx == -1:
        return raw_prompt

    rubric_section = raw_prompt[:output_idx].strip()
    # Remove the trailing input placeholders
    for marker in ["PROMPT (what the student was asked):", "STUDENT PARAGRAPH:", "PASSAGE:", "ESSAY:"]:
        idx = rubric_section.rfind(marker)
        if idx != -1:
            rubric_section = rubric_section[:idx].strip()

    return rubric_section + "\n\nOutput evidence and reasoning as structured JSON: { \"score\": <int>, \"evidence\": [<observations>], \"reasoning\": \"<2-3 sentences>\" }"


def _adapt_editing_prompt(raw_prompt: str) -> str:
    """Adapt the editing prompt to produce a single score while keeping sub-score logic."""
    output_idx = raw_prompt.find("OUTPUT — valid JSON only:")
    if output_idx == -1:
        output_idx = raw_prompt.find("OUTPUT —")
    if output_idx == -1:
        return raw_prompt

    rubric_section = raw_prompt[:output_idx].strip()
    for marker in ["PROMPT (what the student was asked):", "STUDENT PARAGRAPH:", "PASSAGE:", "ESSAY:"]:
        idx = rubric_section.rfind(marker)
        if idx != -1:
            rubric_section = rubric_section[:idx].strip()

    return rubric_section + (
        "\n\nYou MUST list specific errors found. Do NOT return an empty evidence list."
        "\n\nOutput as structured JSON: { \"score\": <int 0-3 = sum of sub-scores>, "
        "\"evidence\": [\"spelling: [list errors or 'clean']\", \"grammar: [list errors or 'clean']\", "
        "\"punctuation: [list errors or 'clean']\"], "
        "\"reasoning\": \"spelling X/1, grammar X/1, punctuation X/1 = total\" }"
    )


_PARAGRAPH_IDEAS_PROMPT = _adapt_percat_prompt(_G35_IDEAS_RAW)
_PARAGRAPH_CONVENTIONS_PROMPT = _adapt_percat_prompt(_G35_CONVENTIONS_RAW)


# ═══════════════════════════════════════════════════════════════════════════════
# RUBRIC PROMPTS — Q11 ESSAY (G6-G8)
# Uses STAAR-calibrated prompts from per_cat.py
# ═══════════════════════════════════════════════════════════════════════════════

_ESSAY_INTRO = """You are an experienced writing grader assigned to score a Grade {grade} student's response to an expository writing task.

For this task, the student read a short text and then wrote an expository essay (target: five paragraphs) in response to a specific question about that text. You will receive the source text, the exact question the student was asked, and the essay the student wrote. Your job — together with the rest of the grading panel — is to evaluate the essay carefully and award a score that reflects how well the student responded.

The essay is scored out of 20 total points across five dimensions:

- Structure (0-5): five-paragraph architecture; intro, body paragraphs, conclusion.
- Evidence & Explanation (0-5): passage-grounded details + causal reasoning that ties them to the thesis.
- Organization (0-4): idea flow, transitions, consistent thesis focus.
- Sentences (0-3): sentence variety, clarity, formal register.
- Editing (0-3): grammar, spelling, punctuation.

The student is {age_hint}. Reward thoughtful, age-appropriate work; do not penalize for sophistication beyond what the rubric demands."""

from .per_cat import G68_STRUCTURE as _G68_STRUCTURE_RAW
from .per_cat import G68_CONTENT as _G68_CONTENT_RAW
from .per_cat import G68_SENTENCES as _G68_SENTENCES_RAW
from .per_cat import G68_EDITING as _G68_EDITING_RAW

_ESSAY_STRUCTURE_PROMPT = _adapt_percat_prompt(_G68_STRUCTURE_RAW)
_ESSAY_CONTENT_PROMPT = _adapt_percat_prompt(_G68_CONTENT_RAW)
_ESSAY_SENTENCES_PROMPT = _adapt_percat_prompt(_G68_SENTENCES_RAW)
_ESSAY_EDITING_PROMPT = _adapt_editing_prompt(_G68_EDITING_RAW)


# ═══════════════════════════════════════════════════════════════════════════════
# JUDGE / SYNTHESIS PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════

_SYNTHESIS_SHORT = """Combine the panel's recommendations into a final score and a single student-facing feedback message.

Apply these gates BEFORE finalizing:

1. Verbatim-copy gate: If the student submission appears to copy substantial chunks of the passage with only trivial paraphrasing, override Ideas (or Evidence on essays) DOWN — cap at 6 if 50%+ verbatim, cap at 2 if 80%+ verbatim. Only apply this when you can cite specific extended overlap; do not penalize for legitimate paraphrasing.
2. Prompt-relevance corroboration: If a panel grader concluded the response addresses the prompt but you disagree (the response is topic-adjacent but never answers the specific question), override that score DOWN with a clear explanation.
3. Score-vs-evidence consistency: If a panel grader's reasoning contradicts its own score (e.g. enumerated 3 notable errors but reported full credit on conventions), override to match the evidence.
4. Conventions: Accept the conventions grader's score as-is. The grader applies the STAAR clarity standard directly — do NOT override conventions scores up or down unless the grader's reasoning clearly contradicts the evidence it listed.

If you do not override, accept the panel's recommendations as-is. Set overridden=true and fill overrideReason ONLY when you adjusted a score; otherwise set overridden=false and omit overrideReason.

Student-facing feedback should:
- Open with one specific, sincere positive observation tied to the submission.
- Name 1-2 concrete, actionable improvements drawn from the rubric evidence.
- Stay age-appropriate to the student's grade level — encouraging, never harsh.
- Avoid jargon ("Path A", "P_count", "NOTABLE") — translate into plain language.
- Be 4-7 sentences total.

reasoning is your audit trail (NOT shown to the student) — explain how you summed the categories, any overrides applied, and any gates that fired."""

_SYNTHESIS_PARAGRAPH = """Combine the panel's recommendations into a final score and a single student-facing feedback message.

Apply these gates BEFORE finalizing:

1. Verbatim-copy gate: If the student submission copies substantial chunks of the passage (>50% n-gram overlap), cap Ideas at 6. If >80%, cap at 2. Only apply when you can cite specific extended overlap.
2. Prompt-relevance corroboration: If the Ideas grader says prompt_addressed=true but the response only writes ABOUT the passage topic without answering the specific question, override Ideas DOWN (cap at 8/15).
3. Score-vs-evidence consistency: If a grader's P_count or error counts don't match their score, override to match the evidence. For example: Ideas grader claims P=3 but only listed 1 passage detail in evidence → reduce Ideas.
4. Conventions arithmetic: Verify that conventions_score matches the grade-band thresholds for the reported notable count. G3: 0-1 notables=5, 2-3=4, 4-5=3, 6+=2. G4: 0=5, 1-2=4, 3-4=3, 5+=2. G5: 0=5, 1=4, 2-3=3, 4+=2.

If no overrides needed, accept panel scores as-is.

Student-facing feedback PRIORITY RULES (follow in order):
1. If C_count=0 (no causal reasoning): the #1 improvement is ALWAYS "explain WHY or HOW your details matter." Do NOT suggest adding more details — the student needs depth, not breadth. Give a specific model showing how to extend one of their existing details with a reason/consequence.
2. If C_count>=1 but P_count<2: suggest adding more passage-specific details.
3. If both P and C are strong but conventions are weak: address the convention error.
4. If everything is strong: brief praise only.

Student-facing feedback should:
- Talk TO the student using "you"
- Name one specific passage detail the student used well
- Name ONE concrete improvement following the priority rules above
- If suggesting explanation, provide a SHORT model sentence showing what it would look like (e.g., "You could write: 'Police dogs help find lost people, which keeps communities safe.'")
- Be 4-6 sentences, encouraging and age-appropriate
- Never mention scores, points, rubric names, or "Path A/B/C"
- Never suggest "add more details" when the real issue is lack of explanation

Return JSON: { "totalScore": <0-20>, "maxScore": 20, "categoryScores": [...], "feedback": "<student-facing>", "reasoning": "<audit trail>" }"""

_SYNTHESIS_ESSAY = """Combine the panel's recommendations into a final score and a single student-facing feedback message.

Apply these gates BEFORE finalizing:

1. Structure-independence: A single-paragraph essay can legitimately score Structure 1/5 but Evidence 5/5 + Organization 4/4 + Sentences 3/3 + Editing 3/3. Never floor other categories because Structure is low.
2. Verbatim-copy gate: If substantial verbatim copying from the passage, cap Evidence at 2/5.
3. Score-vs-evidence consistency: If a grader's evidence contradicts its score, override to match evidence. Key checks:
   - Evidence P_count and C_count should match the P×C table score
   - Editing sub-scores should sum to editing_score
   - Structure paragraph_count should match the structure cap
4. Holistic sanity: If Editing ≤ 1/3 (significant convention problems) but total is 18+, re-examine — an essay with major editing issues is Proficient at best, not Advanced.

If no overrides needed, accept panel scores as-is.

Student-facing feedback should:
- Talk TO the student using "you"
- Name one strength (a good detail, a strong transition, clean mechanics)
- Name one concrete improvement
- Be 4-6 sentences, encouraging and age-appropriate
- Never mention scores, points, rubric names

Return JSON: { "totalScore": <0-20>, "maxScore": 20, "categoryScores": [...], "feedback": "<student-facing>", "reasoning": "<audit trail>" }"""


# ═══════════════════════════════════════════════════════════════════════════════
# CORE PANEL CALLS
# ═══════════════════════════════════════════════════════════════════════════════

def _call_rubric_grader(
    client,
    dimension: RubricDimension,
    *,
    intro: str,
    passage: str,
    question: str,
    response: str,
    grade: int,
    model: str,
) -> PanelResult:
    """Issue one panel grader call and return structured result."""
    sections = [
        "# Task overview",
        intro.strip(),
        "# Your scoring dimension",
        f"**{dimension.name}** — scored 0 to {dimension.max_points}.",
        dimension.prompt.strip(),
        "# Inputs",
        f"Grade level: {grade}",
    ]
    if passage.strip():
        sections.extend(["## Source passage", passage.strip()])
    if question.strip():
        sections.extend([
            "## Question prompt the student was asked",
            question.strip(),
        ])
    sections.extend([
        "## Student submission",
        response.strip(),
        "# Output",
        f'Return JSON matching: {{ "score": <integer 0-{dimension.max_points}>, '
        '"evidence": [<list of short string observations>], '
        '"reasoning": "<1-3 sentences explaining the score>" }}. '
        "You are recommending a score to a downstream judge. Do not write feedback for the student.",
    ])
    user_msg = "\n\n".join(sections)

    use_model = dimension.model or model
    # Budget must cover the ADAPTIVE THINKING block + the JSON output. Opus 4.8 thinks more verbosely
    # than 4.7; the old 512/1024 budgets truncated the JSON (stop_reason=max_tokens), the parse failed,
    # and the score silently defaulted to 0 — which the Ideas=0 gate then cascaded to a 0 total. Give
    # generous headroom so thinking can never starve the JSON.
    max_tokens = 3000 if dimension.max_points >= 5 else 2000
    kwargs = dict(
        model=use_model,
        max_tokens=max_tokens,
        system=SYSTEM_RUBRIC,
        messages=[{"role": "user", "content": user_msg}],
        thinking={"type": "adaptive"},
        temperature=1,
    )

    msg = _api_call_with_retry(client, **kwargs)
    text = next((b.text for b in msg.content if hasattr(b, 'text')), "") if msg.content else ""
    data = _parse_json(text) or {}

    return PanelResult(
        id=dimension.id,
        score=max(0, min(dimension.max_points, int(data.get("score", 0)))),
        evidence=data.get("evidence", []) if isinstance(data.get("evidence"), list) else [],
        reasoning=str(data.get("reasoning", "")),
    )


def _call_synthesis(
    client,
    *,
    intro: str,
    synthesis_prompt: str,
    dimensions: list[RubricDimension],
    panel_results: list[PanelResult],
    passage: str,
    question: str,
    response: str,
    grade: int,
    model: str,
) -> SynthesisResult:
    """Issue the judge/synthesis call after all panel graders complete."""
    sections = [
        "# Task overview",
        intro.strip(),
        "# Your role: judge / synthesis",
        synthesis_prompt.strip(),
        "# Inputs",
        f"Grade level: {grade}",
    ]
    if passage.strip():
        sections.extend(["## Source passage", passage.strip()])
    if question.strip():
        sections.extend([
            "## Question prompt the student was asked",
            question.strip(),
        ])
    sections.extend([
        "## Student submission",
        response.strip(),
        "# Panel recommendations",
    ])

    for dim in dimensions:
        result = next((r for r in panel_results if r.id == dim.id), None)
        sections.append(f"## {dim.name} (max {dim.max_points}, id={dim.id})")
        if result is None:
            sections.append("_No recommendation received — flag for review._")
        else:
            sections.append(f"Recommended score: **{result.score} / {dim.max_points}**")
            if result.evidence:
                sections.append("Evidence:\n" + "\n".join(f"- {e}" for e in result.evidence))
            sections.append(f"Reasoning: {result.reasoning}")

    total_max = sum(d.max_points for d in dimensions)
    sections.extend([
        "# Output",
        'Return JSON matching: { '
        f'"totalScore": <integer 0-{total_max}>, "maxScore": {total_max}, '
        '"categoryScores": [{"rubricId": "<id>", "name": "<name>", "score": <int>, '
        '"maxPoints": <int>, "overridden": <bool>, "overrideReason": "<string or null>"}], '
        '"feedback": "<student-facing>", '
        '"reasoning": "<audit trail NOT shown to student>" }',
    ])
    user_msg = "\n\n".join(sections)

    use_model = model
    kwargs = dict(
        model=use_model,
        max_tokens=4000,  # cover adaptive-thinking + scores + feedback + reasoning (4.8 thinks verbosely)
        system=SYSTEM_SYNTHESIS,
        messages=[{"role": "user", "content": user_msg}],
        thinking={"type": "adaptive"},
        temperature=1,
    )

    msg = _api_call_with_retry(client, **kwargs)
    text = next((b.text for b in msg.content if hasattr(b, 'text')), "") if msg.content else ""
    data = _parse_json(text) or {}

    cat_scores = {}
    overrides = {}
    for cs in data.get("categoryScores", []):
        rid = cs.get("rubricId", "")
        cat_scores[rid] = int(cs.get("score", 0))
        if cs.get("overridden"):
            overrides[rid] = cs.get("overrideReason", "")

    return SynthesisResult(
        total_score=int(data.get("totalScore", sum(cat_scores.values()) if cat_scores else 0)),
        max_score=total_max,
        category_scores=cat_scores,
        overrides=overrides,
        feedback=str(data.get("feedback", "")),
        reasoning=str(data.get("reasoning", "")),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# INTERNAL HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def _run_panel(client, dimensions, intro, passage, question, response, grade, model, synthesis_prompt):
    """Run the full panel → judge pipeline. Returns (SynthesisResult, list[PanelResult], elapsed)."""
    t0 = time.time()

    with ThreadPoolExecutor(max_workers=len(dimensions)) as ex:
        futures = {
            dim.id: ex.submit(
                _call_rubric_grader, client, dim,
                intro=intro, passage=passage, question=question,
                response=response, grade=grade, model=model,
            )
            for dim in dimensions
        }
        panel_results = []
        for dim in dimensions:
            try:
                panel_results.append(futures[dim.id].result(timeout=180))
            except Exception as e:
                logger.error(f"Panel grader '{dim.id}' failed: {e}")
                panel_results.append(PanelResult(id=dim.id, score=0, evidence=[f"ERROR: {e}"], reasoning="Grader call failed"))

    # Run synthesis with timeout to prevent hanging
    try:
        with ThreadPoolExecutor(max_workers=1) as synth_ex:
            synth_future = synth_ex.submit(
                _call_synthesis,
                client,
                intro=intro,
                synthesis_prompt=synthesis_prompt,
                dimensions=dimensions,
                panel_results=panel_results,
                passage=passage,
                question=question,
                response=response,
                grade=grade,
                model=model,
            )
            synthesis = synth_future.result(timeout=180)
    except Exception as e:
        logger.error(f"Panel synthesis failed: {e}")
        # Fallback: build a minimal synthesis from panel scores
        cat_scores = {r.id: r.score for r in panel_results}
        synthesis = SynthesisResult(
            total_score=sum(cat_scores.values()),
            max_score=sum(d.max_points for d in dimensions),
            category_scores=cat_scores,
            overrides={},
            feedback="",
            reasoning=f"Synthesis call failed: {e}",
        )

    elapsed = time.time() - t0
    return synthesis, panel_results, elapsed


def _build_audit(panel_results, synthesis, elapsed, qnum, grade):
    """Build internal_notes and teacher_notes from panel results."""
    override_notes = [f"OVERRIDE {rid}: {reason}" for rid, reason in synthesis.overrides.items()]

    scores_str = " ".join(f"{r.id}:{r.score}" for r in panel_results)
    internal_notes = f"panel G{grade} Q{qnum} in {elapsed:.1f}s | {scores_str}"
    if override_notes:
        internal_notes += " | " + " | ".join(override_notes)

    teacher_lines = []
    for r in panel_results:
        teacher_lines.append(f"[{r.id}] score={r.score}")
        teacher_lines.append(f"  Evidence: {r.evidence}")
        teacher_lines.append(f"  Reasoning: {r.reasoning}")
    teacher_lines.append(f"[Judge] {synthesis.reasoning}")

    return internal_notes, "\n".join(teacher_lines)


# ═══════════════════════════════════════════════════════════════════════════════
# PUBLIC API
# ═══════════════════════════════════════════════════════════════════════════════

def score_panel(
    client,
    *,
    grade: int,
    passage: str,
    question: str,
    response: str,
    qnum: int,
    max_score: int | None = None,
) -> QuestionScore:
    """Score any question type via the panel-of-experts architecture.

    Automatically selects the correct rubric configuration based on qnum and grade:
    - Q1-Q5 (G3-G5): sentence-revision (2 pts)
    - Q6-Q10 (G3-G5): sentence-writing (3 pts)
    - Q11 (G3-G5 paragraph / G6-G8 essay, 20 pts): delegated to the VALIDATED Joey 3-trait engine
      (score_panel_joey, scale=20). The legacy _score_paragraph/_score_essay handlers below remain for
      A/B reference but are no longer on the live path — the Joey engine is tighter at the low end.

    Returns a QuestionScore compatible with the rest of the grading pipeline.
    """
    # Determine max_score if not provided
    if max_score is None:
        if qnum <= 5:
            max_score = 2
        elif qnum <= 10:
            max_score = 3
        else:
            max_score = 20

    # Q11 (paragraph G3-5 / essay G6-8): route to the VALIDATED Joey 3-trait engine.
    # It was validated against Noel's blind grades (mean |Δ|≈0.74) and is tight at the low end
    # (+2.5% on weak responses) where the legacy 20-pt Alpha rubric inflated (+25%). It owns its own
    # preflight + Check-1 attempt floor, so delegate BEFORE the generic gate below. scale=20 fills the
    # legacy /20 Q11 slot (grades on native 0-3/0-3/0-4, then ×2). Lazy import avoids a circular import
    # (panel_joey reuses _run_panel/_build_audit/RubricDimension from this module).
    if qnum >= 11:
        from .panel_joey import score_panel_joey
        return score_panel_joey(client, grade=grade, passage=passage,
                                question=question, response=response,
                                qnum=qnum, scale=20 if max_score == 20 else 10)

    # Preflight gates
    gate = _preflight(response)
    if gate == "empty":
        return QuestionScore.blank(qnum, max_score, grade)
    if gate == "gibberish":
        return QuestionScore.gibberish(qnum, max_score, grade)

    model = _default_panel_model()

    # Route to the correct question-type handler
    if qnum <= 5:
        return _score_sentence_revision(client, grade=grade, passage=passage,
                                        question=question, response=response,
                                        qnum=qnum, max_score=max_score, model=model)
    else:  # qnum 6-10
        return _score_sentence_writing(client, grade=grade, passage=passage,
                                       question=question, response=response,
                                       qnum=qnum, max_score=max_score, model=model)


def score_panel_median(client, *, grade, passage, question, response, qnum,
                       max_score=None, runs=3):
    """Panel of Experts V2: run score_panel `runs` times IN PARALLEL and return the median result
    (by total_score). Stabilises the temp-1 panel — this is the validated median-of-3 protocol.

    Returns (median_QuestionScore, [all run scores]) so callers can record the spread.
    """
    def _one(_i):
        return score_panel(client, grade=grade, passage=passage, question=question,
                           response=response, qnum=qnum, max_score=max_score)

    with ThreadPoolExecutor(max_workers=runs) as ex:
        results = [r for r in ex.map(_one, range(runs)) if r is not None]
    if not results:
        # fall back to a single synchronous attempt
        return score_panel(client, grade=grade, passage=passage, question=question,
                           response=response, qnum=qnum, max_score=max_score), []
    ordered = sorted(results, key=lambda s: s.total_score)
    median = ordered[len(ordered) // 2]  # lower-median on even counts; runs is odd by default
    return median, results


# ───────────────────────────────────────────────────────────────────────────
# Q1-Q5 Sentence Revision
# ───────────────────────────────────────────────────────────────────────────

def _score_sentence_revision(client, *, grade, passage, question, response, qnum, max_score, model):
    intro = _REVISION_INTRO.format(grade=grade, age_hint=_age_hint(grade))
    dimensions = [
        RubricDimension(id="skill", name="Skill Application", max_points=1, prompt=_SKILL_APPLICATION_PROMPT),
        RubricDimension(id="conventions", name="Writing Conventions", max_points=1, prompt=_REVISION_CONVENTIONS_PROMPT),
    ]

    synthesis, panel_results, elapsed = _run_panel(
        client, dimensions, intro, passage, question, response, grade, model, _SYNTHESIS_SHORT)

    skill = max(0, min(1, synthesis.category_scores.get("skill", panel_results[0].score)))
    conv = max(0, min(1, synthesis.category_scores.get("conventions", panel_results[1].score)))
    total = skill + conv

    internal_notes, teacher_notes = _build_audit(panel_results, synthesis, elapsed, qnum, grade)

    return QuestionScore(
        question=qnum, ideas_score=skill, ideas_max=1,
        organization_score=0, organization_max=0,
        conventions_score=conv, conventions_max=1,
        total_score=total, total_max=max_score,
        feedback=synthesis.feedback,
        internal_notes=internal_notes, teacher_notes=teacher_notes,
    )


# ───────────────────────────────────────────────────────────────────────────
# Q6-Q10 Sentence Writing
# ───────────────────────────────────────────────────────────────────────────

def _score_sentence_writing(client, *, grade, passage, question, response, qnum, max_score, model):
    intro = _SENTENCE_WRITING_INTRO.format(grade=grade, age_hint=_age_hint(grade))
    dimensions = [
        RubricDimension(id="answer", name="Answer Quality", max_points=2, prompt=_ANSWER_QUALITY_PROMPT),
        RubricDimension(id="conventions", name="Writing Conventions", max_points=1, prompt=_WRITING_CONVENTIONS_PROMPT),
    ]

    synthesis, panel_results, elapsed = _run_panel(
        client, dimensions, intro, passage, question, response, grade, model, _SYNTHESIS_SHORT)

    answer = max(0, min(2, synthesis.category_scores.get("answer", panel_results[0].score)))
    conv = max(0, min(1, synthesis.category_scores.get("conventions", panel_results[1].score)))
    total = answer + conv

    internal_notes, teacher_notes = _build_audit(panel_results, synthesis, elapsed, qnum, grade)

    return QuestionScore(
        question=qnum, ideas_score=answer, ideas_max=2,
        organization_score=0, organization_max=0,
        conventions_score=conv, conventions_max=1,
        total_score=total, total_max=max_score,
        feedback=synthesis.feedback,
        internal_notes=internal_notes, teacher_notes=teacher_notes,
    )


# ───────────────────────────────────────────────────────────────────────────
# Q11 Paragraph (G3-G5)
# ───────────────────────────────────────────────────────────────────────────

def _score_paragraph(client, *, grade, passage, question, response, qnum, max_score, model):
    # Normalize HTML to preserve paragraphs
    from .per_cat import _normalize_response_preserving_paragraphs
    response = _normalize_response_preserving_paragraphs(response)

    intro = _PARAGRAPH_INTRO.format(grade=grade, age_hint=_age_hint(grade))
    dimensions = [
        RubricDimension(id="ideas", name="Ideas & Organization", max_points=15, prompt=_PARAGRAPH_IDEAS_PROMPT),
        RubricDimension(id="conventions", name="Writing Conventions", max_points=5, prompt=_PARAGRAPH_CONVENTIONS_PROMPT),
    ]

    synthesis, panel_results, elapsed = _run_panel(
        client, dimensions, intro, passage, question, response, grade, model, _SYNTHESIS_PARAGRAPH)

    ideas = max(0, min(15, synthesis.category_scores.get("ideas", panel_results[0].score)))
    conv = max(0, min(5, synthesis.category_scores.get("conventions", panel_results[1].score)))
    total = ideas + conv

    internal_notes, teacher_notes = _build_audit(panel_results, synthesis, elapsed, qnum, grade)

    return QuestionScore(
        question=qnum, ideas_score=ideas, ideas_max=15,
        organization_score=0, organization_max=0,
        conventions_score=conv, conventions_max=5,
        total_score=total, total_max=max_score,
        feedback=synthesis.feedback,
        internal_notes=internal_notes, teacher_notes=teacher_notes,
    )


# ───────────────────────────────────────────────────────────────────────────
# Q11 Essay (G6-G8)
# ───────────────────────────────────────────────────────────────────────────

def _score_essay(client, *, grade, passage, question, response, qnum, max_score, model):
    from .per_cat import _normalize_response_preserving_paragraphs
    response = _normalize_response_preserving_paragraphs(response)

    intro = _ESSAY_INTRO.format(grade=grade, age_hint=_age_hint(grade))
    dimensions = [
        RubricDimension(id="structure", name="Structure", max_points=5, prompt=_ESSAY_STRUCTURE_PROMPT),
        RubricDimension(id="content", name="Evidence & Organization", max_points=9, prompt=_ESSAY_CONTENT_PROMPT),
        RubricDimension(id="sentences", name="Sentences", max_points=3, prompt=_ESSAY_SENTENCES_PROMPT),
        RubricDimension(id="editing", name="Editing", max_points=3, prompt=_ESSAY_EDITING_PROMPT),
    ]

    synthesis, panel_results, elapsed = _run_panel(
        client, dimensions, intro, passage, question, response, grade, model, _SYNTHESIS_ESSAY)

    # Content grader returns combined Evidence (0-5) + Organization (0-4) = 0-9
    # The judge should split these in categoryScores, but fall back to panel result
    content_result = next((r for r in panel_results if r.id == "content"), None)
    content_score = content_result.score if content_result else 0

    structure = max(0, min(5, synthesis.category_scores.get("structure", panel_results[0].score)))
    evidence = synthesis.category_scores.get("evidence", None)
    organization = synthesis.category_scores.get("organization", None)

    # If judge split evidence + organization, use those. Otherwise derive from content.
    if evidence is not None and organization is not None:
        evidence = max(0, min(5, evidence))
        organization = max(0, min(4, organization))
    else:
        # Content grader returns combined score (0-9). Split: evidence=min(5, score), org=remainder
        evidence = max(0, min(5, content_score))
        organization = max(0, min(4, content_score - evidence))

    # Try to get content sub-scores from judge
    content_cat = synthesis.category_scores.get("content", None)
    if content_cat is not None and evidence is None:
        evidence = max(0, min(5, content_cat))
        organization = max(0, min(4, 0))

    sentences = max(0, min(3, synthesis.category_scores.get("sentences",
                   next((r.score for r in panel_results if r.id == "sentences"), 0))))
    editing = max(0, min(3, synthesis.category_scores.get("editing",
                 next((r.score for r in panel_results if r.id == "editing"), 0))))

    total = structure + evidence + organization + sentences + editing
    total = min(total, max_score)

    internal_notes, teacher_notes = _build_audit(panel_results, synthesis, elapsed, qnum, grade)
    internal_notes += f" | struct={structure} ev={evidence} org={organization} sent={sentences} edit={editing}"

    return QuestionScore(
        question=qnum, ideas_score=evidence, ideas_max=5,
        organization_score=organization, organization_max=4,
        conventions_score=editing, conventions_max=3,
        total_score=total, total_max=max_score,
        feedback=synthesis.feedback,
        internal_notes=internal_notes, teacher_notes=teacher_notes,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# BACKWARD COMPATIBILITY — keep the old function name working
# ═══════════════════════════════════════════════════════════════════════════════

def score_sentence_writing_panel(client, **kwargs) -> QuestionScore:
    """Backward-compatible alias for score_panel (Q6-Q10 only)."""
    return score_panel(client, **kwargs)
