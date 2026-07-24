"""
native_prompts.py  -  authored Timeback NATIVE-grader rubric-block grading prompts for HS Writing.

The native AlphaTest grader (definition=https://alphatest.alpha.school/prod/ai-grading) reads a grading
prompt embedded in the item as `<qti-rubric-block use="ext:grading-prompt" view="scorer">`. Unlike our Render
grader (a panel of per-dimension LLM calls + a judge), the native grader is ONE model call, so each prompt
here folds the Render scorer's gates + per-dimension rubrics + synthesis into a single prompt, in the proven
shipped-G3 craft shape: header+scale -> PRE-SCORING GATES -> per-trait rubric bands -> feedback rules ->
strict single-JSON output with {{passage}} / {{question}} / {{response}} placeholders.

SOURCE OF TRUTH (translated verbatim in intent from the Render engine):
  - sentence: grader_engine/panel.py (_ANSWER_QUALITY_PROMPT 0-2, _WRITING_CONVENTIONS_PROMPT 0-1,
    _SKILL_APPLICATION_PROMPT 0-1, _REVISION_CONVENTIONS_PROMPT 0-1) + _SYNTHESIS_SHORT gates.
    Sentence scoring is RUBRIC-AGNOSTIC (rc.staar == rc.4trait); only frq_type (writing/revision) changes it.
  - paragraph: panel_joey.py (Ideas 0-3 + Org 0-3 + Conv 0-4 = 10) + the grade>=9 CONTENT GATE.
  - essay rc.staar: scored via the SBAC alias (panel_sbac.py Org/Purpose 0-4 + Evidence/Elab 0-4 + Conv 0-2
    = 10) then normalized to STAAR /5 for the item's declared scale.
  - essay rc.4trait: panel_ccss.py 4-criterion, argument (each 0-6, /24) | analysis (each 0-4, /16).

Each prompt is fidelity-checked against the live Render /score by native_vs_render_harness.py; the harness
comparison IS the calibration proof (behavioral equivalence), so intent-faithful translation + measured
agreement is the bar, not byte-identical prompt text (the native grader is a different architecture anyway).

PLACEHOLDERS: {{passage}} {{question}} {{response}} are filled by the native grader at submit time. When we
run a prompt through the harness we substitute the same three. Literal JSON braces are escaped {{ }} the way
the shipped G3 prompt does; PROMPTS here use the sentinel <<<JSONOPEN>>>/<<<JSONCLOSE>>> for the output-object
braces and .format-safe {{ }} for placeholders — see render_prompt().
"""
from __future__ import annotations

# ---- shared building blocks -------------------------------------------------

_GATES_COMMON = """═══════════════════════════════════════════════════════════════════════
PRE-SCORING GATES — check in order. Stop at the first that fires.
═══════════════════════════════════════════════════════════════════════

G1. BLANK / REFUSAL / GIBBERISH → total 0. Fires on: empty; "idk"/"no"/"skip";
    a single char or one char repeated; keyboard mash; fewer than 2 real English
    words; text with almost no vowels.
G2. OFF-TOPIC → the response never addresses the question or the passage topic
    at all (topic-adjacent but on the wrong question still counts as off-topic).
    Content/ideas dimension = 0; score conventions on its own.
G3. VERBATIM COPY → if the response copies the passage with only trivial changes,
    the ideas/answer dimension cannot exceed a bare-minimum score (cite the overlap).
"""

_FEEDBACK_COMMON = """═══════════════════════════════════════════════════════════════════════
FEEDBACK (student-facing) — write AFTER you finalize the score.
═══════════════════════════════════════════════════════════════════════
- Open with one specific, sincere positive tied to what the student actually wrote.
- Name 1-2 concrete, actionable next steps drawn from the rubric evidence.
- Age-appropriate for a high-school student; encouraging, never harsh.
- No jargon, no rubric labels, no scores, no internal logic in the feedback.
"""


# ---- SENTENCE — WRITING (/3): Answer Quality 0-2 + Conventions 0-1 ----------

SENTENCE_WRITING = {
    "id": "sentence_writing",
    "scale": 3,
    "frq_type": "writing",
    "prompt": """You are a careful high-school writing grader.

The student read a short passage and was asked an open-ended question about it. Their task is to respond in
ONE complete sentence that gives a clear answer WITH support (a reason, explanation, or concrete example).

Score the response out of 3: Answer Quality 0-2 + Writing Conventions 0-1.
Build a short evidence log first, then set the score. Output a single JSON object — no other text.

""" + _GATES_COMMON + """
═══════════════════════════════════════════════════════════════════════
ANSWER QUALITY (0-2)
═══════════════════════════════════════════════════════════════════════
A strong answer (a) directly addresses the specific question, AND (b) gives a reason/explanation/example
connected to the answer. Both halves matter.
- 2: clearly answers the question AND offers a genuine reason/explanation/example (may be brief but present
     and connected). Implicit reasoning via emotion/motivation/consequence counts.
- 1: answers but gives no reason or only a vague restatement; OR gives a reason but the answer is unclear or
     only partially on the question; OR on-topic but tangential to the specific question.
- 0: off-topic, contradicts the prompt's spirit, unintelligible, or a refusal.

WHAT COUNTS AS A REASON: it must explain WHY / HOW / WHAT-RESULTS, adding information beyond restating the
event. "did the right thing" = vague restatement (1). "because it showed she respected nature" = reason (2).
"because of plants" (cause named, relationship not explained) = underdeveloped (1). A reason that is a
synonym/definitional restatement of the claim is CIRCULAR → 1, not 2.

ONE-SENTENCE RULE: the task asks for ONE sentence. If the student wrote 2+ sentences, grade ONLY THE FIRST
sentence — the answer AND its reason must both be in that first sentence to earn 2; if the reason appears
only in a later sentence, cap Answer at 1. A student may negate the prompt's premise if they give a clear
reason (not off-topic).

═══════════════════════════════════════════════════════════════════════
WRITING CONVENTIONS (0-1) — clarity is the gate, not error count
═══════════════════════════════════════════════════════════════════════
- 1: a reader reads the sentence smoothly and meaning is never in doubt. A few minor slips (a missing comma,
     a spelling slip, a capitalization lapse) do NOT cost the point when clarity holds. Default to 1 for a
     readable sentence.
- 0: ONLY when the sentence fails as a sentence — a fragment/run-on, OR errors that impede clarity (the
     reader must stop and reconstruct meaning, words merged/garbled), OR ~3+ distinct errors in the one
     sentence showing no command of sentence conventions.

""" + _FEEDBACK_COMMON + """
═══════════════════════════════════════════════════════════════════════
OUTPUT — a single JSON object, no other text
═══════════════════════════════════════════════════════════════════════
<<<JSONOPEN>>>
  "answer_score": <0-2>,
  "answer_max": 2,
  "conventions_score": <0-1>,
  "conventions_max": 1,
  "total_score": <answer + conventions, 0-3>,
  "total_max": 3,
  "sentence_count": <integer>,
  "has_reason_or_example": <true|false>,
  "reason_is_circular": <true|false>,
  "gate_fired": "<G1 | G2 | G3 | none>",
  "feedback": "<warm student-facing feedback, 2-4 sentences, no scores>",
  "internal_notes": "<1-2 sentences on the key scoring decisions>"
<<<JSONCLOSE>>>

🔹 TEST CONTENT
Passage:
{{passage}}
Question:
{{question}}
Student response:
{{response}}
""",
}


# ---- SENTENCE — REVISION (/2): Skill Application 0-1 + Conventions 0-1 -------

SENTENCE_REVISION = {
    "id": "sentence_revision",
    "scale": 2,
    "frq_type": "revision",
    "prompt": """You are a careful high-school writing grader.

The student was shown a sentence and asked to REVISE it by applying a specific writing skill (combine with a
conjunction, add an appositive, fix a fragment, rewrite as a question, make it clearer/more concise, etc.).
You receive the instruction and the one-sentence revision.

Score out of 2: Skill Application 0-1 + Writing Conventions 0-1.
Build a short evidence log first, then set the score. Output a single JSON object — no other text.

""" + _GATES_COMMON + """
═══════════════════════════════════════════════════════════════════════
SKILL APPLICATION (0-1)
═══════════════════════════════════════════════════════════════════════
FIRST classify the requested skill, then apply the matching bar:

STRUCTURAL skills (a named transformation: combine with a conjunction, add an appositive, rewrite as a
question, expand a fragment into a complete sentence, change sentence type) — score the TRANSFORMATION ONLY:
- 1: the transformation is correctly performed (it IS a question / IS complete / DOES contain an appositive /
     IS combined) and meaning is not materially reversed. Do NOT dock for awkward word choice or imperfect
     style — those are not skill failures here.
- 0: the transformation is not performed (still a statement when a question was asked; no appositive; still a
     fragment), or meaning is materially changed/reversed.

QUALITY-LADEN skills (revise to be clear/effective, make it clearer/concise, improve it) — semantic quality
counts:
- 1: the revision genuinely makes the sentence clear, correct, and effective.
- 0: it fails to improve clarity, introduces a new error, or stays awkward/unclear.

Read the task verb: "rewrite as / combine / add / expand / change" = STRUCTURAL; "revise / improve / make
clear / make concise" = QUALITY-LADEN.

═══════════════════════════════════════════════════════════════════════
WRITING CONVENTIONS (0-1) — clarity is the gate, not error count
═══════════════════════════════════════════════════════════════════════
- 1: reader reads it smoothly, meaning never in doubt; minor slips do not cost the point. Default to 1.
- 0: only when it fails as a sentence (fragment/run-on), errors impede clarity, or ~3+ distinct errors.

""" + _FEEDBACK_COMMON + """
═══════════════════════════════════════════════════════════════════════
OUTPUT — a single JSON object, no other text
═══════════════════════════════════════════════════════════════════════
<<<JSONOPEN>>>
  "skill_score": <0-1>,
  "skill_max": 1,
  "conventions_score": <0-1>,
  "conventions_max": 1,
  "total_score": <skill + conventions, 0-2>,
  "total_max": 2,
  "skill_type": "<STRUCTURAL | QUALITY-LADEN>",
  "transformation_correct": <true|false>,
  "gate_fired": "<G1 | G2 | G3 | none>",
  "feedback": "<warm student-facing feedback, 2-4 sentences, no scores>",
  "internal_notes": "<1-2 sentences on the key scoring decisions>"
<<<JSONCLOSE>>>

🔹 TEST CONTENT
Instruction / sentence to revise:
{{question}}
Passage (if any):
{{passage}}
Student revision:
{{response}}
""",
}


def render_prompt(spec: dict, passage: str, question: str, response: str) -> str:
    """Fill a prompt spec's {{placeholders}} for a harness run. Restores the literal JSON braces.

    The stored prompt uses {{passage}}/{{question}}/{{response}} placeholders and <<<JSONOPEN>>>/<<<JSONCLOSE>>>
    sentinels for the output-object braces (so the text is safe to embed in XML and to str.replace here without
    a brittle .format). For the LIVE rubric-block we emit the SAME text but with the sentinels swapped for
    real { } (see native_rubric_block()).
    """
    txt = spec["prompt"]
    txt = txt.replace("<<<JSONOPEN>>>", "{").replace("<<<JSONCLOSE>>>", "}")
    txt = txt.replace("{{passage}}", passage or "(none)")
    txt = txt.replace("{{question}}", question or "(none)")
    txt = txt.replace("{{response}}", response or "")
    return txt


def rubric_block_text(spec: dict) -> str:
    """The text to embed in <qti-rubric-block> for the LIVE native grader: real JSON braces, placeholders LEFT
    as {{passage}}/{{question}}/{{response}} (the native grader substitutes them at submit time)."""
    return spec["prompt"].replace("<<<JSONOPEN>>>", "{").replace("<<<JSONCLOSE>>>", "}")


# route key -> spec. Sentence routes only (native path). Paragraph/essay specs live in native_prompts_long.py.
SENTENCE_SPECS = {
    ("sentence", "writing"): SENTENCE_WRITING,
    ("sentence", "revision"): SENTENCE_REVISION,
}
