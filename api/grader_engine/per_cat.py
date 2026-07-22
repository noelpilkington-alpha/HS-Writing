"""Per-category Opus 4.7 grading engine — v2a ship.

Standards-alignment: mean |Δ| = 0.69 vs ground-truth on n=35 audit (best of all
engines tested; beats AW's 1.11 and current 4-run Sonnet's 2.29).

Architecture:
  G3-G5 paragraph (20 pts):
    2 parallel Opus 4.7 calls (Ideas 0-15, Conventions 0-5)
    + deterministic verbatim-copying post-processor on Ideas
  G6-G8 essay (20 pts):
    4 parallel Opus 4.7 calls (Structure 0-5, Content [Ev 0-5 + Org 0-4],
                                Sentences 0-3, Editing 0-3)

See Case Studies/Grader_Spec_For_AlphaTest.md for the full spec, including
prompt texts and validation methodology.
"""

from __future__ import annotations

import logging
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from .models import QuestionScore
from .scorer import _api_call_with_retry, _parse_json, extract_text

_BLANK_PLACEHOLDERS = frozenset([
    "(no response provided)",
    "(no response)",
    "(no answer provided)",
    "(no answer)",
])


def _is_blank_response(text: str) -> bool:
    """Detect if a student response is blank or a placeholder string."""
    if not text or not text.strip():
        return True
    return text.strip().lower() in _BLANK_PLACEHOLDERS

logger = logging.getLogger(__name__)

def _default_opus_model() -> str:
    """Pick the right Opus 4.7 model ID for the configured provider.

    AWS Bedrock uses a prefixed ID (`us.anthropic.claude-opus-4-7`); the direct
    Anthropic API uses the unprefixed form (`claude-opus-4-7`). Sending the
    Bedrock ID to the direct API (or vice versa) returns a 404 and crashes the
    grading job. Detect provider from the env and pick accordingly.
    Override via `ALPHA_PER_CAT_MODEL` if you need a specific ID.
    """
    provider = os.environ.get("ANTHROPIC_PROVIDER", "bedrock").strip().lower()
    if provider == "anthropic":
        return "claude-opus-4-7"
    return "us.anthropic.claude-opus-4-7"


OPUS_MODEL = os.environ.get("ALPHA_PER_CAT_MODEL") or _default_opus_model()

# Median-of-N voting is available but defaults OFF (N=1) because the original
# ±3 "variance" we observed was actually an input-normalization bug (HTML-strip
# destroying paragraph breaks), not LLM noise. Once the engine normalizes
# responses correctly (see _normalize_response_preserving_paragraphs), a single
# call per category produces standards-aligned scores.
# Set ALPHA_PER_CAT_G68_N=3 to enable median-of-3 if you want belt-and-braces.
G68_CATEGORY_N = int(os.environ.get("ALPHA_PER_CAT_G68_N", "1"))
G35_CATEGORY_N = int(os.environ.get("ALPHA_PER_CAT_G35_N", "1"))

# Opus 4.7 rejects the temperature parameter.
def _model_supports_temperature(model: str) -> bool:
    return "opus-4-7" not in (model or "")


# ─────────────────────────────────────────────────────────────────────────────
# PROMPTS — canonical per-category grading prompts.
# Sync with Case Studies/Grader_Spec_For_AlphaTest.md §3.
# ─────────────────────────────────────────────────────────────────────────────

G35_IDEAS = """You are grading ONE category of a Grade {grade} paragraph response: IDEAS & ORGANIZATION (0-15).

The paragraph scores 0-15 for content/structure/flow combined. Apply the three-paths rule below.

🔒 STEP 0 — PROMPT-RELEVANCE GATE (apply BEFORE three-paths rule):
Read the PROMPT carefully. Does the student's response actually answer the specific
question the prompt asks? (Not: does it relate to the passage topic. But: does it
answer the specific WHY/HOW/WHAT the prompt names?)

  ❌ Example of prompt-miss: prompt asks "why Jason chose to place sculptures under
     the sea"; student describes the statues (where, how many, how to see them) but
     never explains the coral-reef protection reason. This is a prompt-miss.
     → Cap Ideas at 8/15 regardless of passage grounding.
  ✅ Example of prompt-addressed: prompt asks "why soil is important"; student says
     "plants need soil and humans need plants." Addresses the prompt's question
     (why = plants + humans depend on it). Proceed to three-paths rule.

If the response writes ABOUT the passage topic without ANSWERING the prompt's
specific question, Ideas ≤ 8/15. Otherwise proceed.

🔒 STEP 1 — PASSAGE-GROUNDING TEST (apply after prompt-relevance gate):
Count ONLY passage-SPECIFIC details — facts a student could not have written from
general knowledge alone. Generic claims that sound passage-adjacent but lack
specifics do NOT count.

  ❌ DOES NOT COUNT as passage-grounded (generic, general-knowledge):
     "high-speed trains save time and money" (could be written without reading)
     "trains are better for the environment than cars" (general knowledge)
     "learning to cook is useful when you're home alone" (general claim)
     "fair rules make sports more fun" (general opinion)
  ✅ COUNTS as passage-grounded (passage-specific):
     "Brightline express, which opened in 2018" (specific named fact)
     "the Sussex researchers found 17 facial expressions" (specific detail)
     "Alfred makes the stories fun" (specific passage claim)
     "carbon fibre and electric motors" (passage-specific materials)
  If 0 passage-specific details → Ideas capped at 9/15 (the 9-tier for
  generic/formulaic responses).

🔓 BACKGROUND KNOWLEDGE IS LEGITIMATE SUPPORT (do not penalize):
Evidence must ANCHOR to the passage (P_count above is the anchor), but the REASONING
that explains that evidence may draw on the student's OWN knowledge. When a student
anchors a claim to the passage and then uses background/outside knowledge to EXPLAIN
or SUPPORT it, that explanation COUNTS as Path A/C development — do NOT discount it as
"not passage-grounded" or treat it as tangential.
  ✅ COUNTS as support: passage says "students catch up with friends, play games, and
     sometimes meet new classmates" on the train; student writes "for example, this is
     where lifelong friendships are formed" drawing on their own knowledge of the story.
     The claim is passage-anchored; the elaboration is the student's. Credit it as
     genuine reasoning — this is exactly the synthesis we want.
ONLY treat outside information as a problem when it is SUPERFLUOUS (irrelevant to the
claim being made) OR when there is NO passage anchor at all (pure prior knowledge with
zero passage grounding — the STEP 1 cap still applies in that case).

🔒 THREE PATHS TO SCORE 13+ (STAAR SP3 equivalent):
  PATH A — CAUSAL: every detail followed by explanation. But "because" is NOT required. Path A counts plainspoken reasoning:
    CONCRETE EXAMPLES that COUNT:
      "in the process they carelessly remove milkweed plants" (consequence chain, implicit)
      "These actions help scientists understand where the monarchs are"
      "gardens release oxygen which is especially beneficial"
      "children can study into the evening and businesses can be open later"
      "This teaches children that it's okay for things to go wrong"
    DOES NOT count: bare restatement, formulaic "this shows" with no new info.

  PATH B — ORGANIZATIONAL: intro with central idea + 3+ details with transitions (First/Second/Lastly, One way/Another way/Also) + conclusion that synthesizes. Even without causal language, PATH B alone earns 13 minimum.

  PATH C — EVIDENCE VARIETY: mix of quotes/paraphrase + 2+ interpretive moves ("This means", "This shows") tying to central claim.

Any ONE path fully demonstrated → 13 minimum.
TWO paths → 14.
All THREE + voice → 15.

🔓 SINGLE-PATH RESPONSES CAN REACH THE TOP (do not require 2+ paths for 15):
The number of paths a response CAN demonstrate is limited by what the PROMPT affords.
A one-dimensional prompt (e.g. a "what" question, or a what+how that has a single
correct synthesis) may not give the student room for multiple analytical angles. When
the prompt is one-dimensional, a SINGLE fully-developed path that includes a genuine
synthesizing sentence reaches 14-15 — do NOT cap it at 13 merely because a second path
is absent. "Beyond-passage insight" is also not required when the passage/question
concerns a specialized topic where the synthesis itself IS the insight.
  ✅ Example: a "what are three X and how are they done" prompt where the student lists
     three details and adds one sentence synthesizing what they have in common (e.g. "all
     three require a strong body and proper form") — that synthesis is full analysis for a
     one-dimensional prompt. Score 14-15, not 13.
This relaxation applies ONLY to responses that are genuinely DEVELOPED (per the
"FULLY DEMONSTRATED" test below). A response that merely GESTURES at a path is still
capped at 11 — this does not lower that bar.

"FULLY DEMONSTRATED" means the path's technique is DEVELOPED, not just gestured at:
  - Path A: at least one detail must be explained across 2+ clauses showing depth. Three single-clause "because X" links with no elaboration, no central idea, and no conclusion = Path A GESTURED AT (cap at floor 11), not fully demonstrated.
  - Path B: must have an actual intro sentence with central idea + actual conclusion. Listing details with transitions but no intro/conclusion = not fully demonstrated.
  - Path C: interpretive moves must add genuine insight, not just "this shows that..."

Score bands:
  15 = exceptional — 2+ paths with voice, OR one fully-developed path with genuine
       synthesis on a one-dimensional prompt that affords only one path
  13-14 = fully developed via any path(s)
  11-12 = partial development (some explanation, inconsistent)
  9-10 = passage details LISTED without explanation
  7-8 = central idea + thin passage grounding
  3-6 = short, opinion-only, or topic-adjacent
  0-2 = off-topic / no central idea / verbatim copy

🔒 9-VS-11 FLOOR OVERRIDES MIN-DEV CAP:
If the response has 2+ PASSAGE-SPECIFIC details (per the passage-grounding test
above), Ideas = 11 MINIMUM, even if the paragraph is brief (3-5 sentences).
The MIN-DEV cap (cap at 10 for short paragraphs) only applies to:
  - Responses with FEWER than 3 sentences, OR
  - Responses with <2 passage-specific details
A 3-sentence paragraph with 2+ passage-specific details earns 11+ per this floor,
not 10.

All three paths are equally valid routes to 13+. Causal reasoning is NOT required — organizational sophistication (Path B) alone earns top marks. But single-clause "because/so" connectors alone do NOT satisfy Path A — at least one detail must be developed across 2+ clauses.

OUTPUT — valid JSON only:
{{
  "prompt_addressed": <true/false — did the response answer the prompt's specific question?>,
  "ideas_score": <0-15>,
  "P_count": <int — PASSAGE-SPECIFIC details only>,
  "C_count": <int>,
  "paths_detected": {{"A": <bool>, "B": <bool>, "C": <bool>}},
  "passage_details_used": [<3-5 details; must be passage-specific>],
  "causal_sentences": [<verbatim>],
  "reasoning": "<2-3 sentences; if ideas<11 despite P≥2, explain which gate triggered>"
}}

PROMPT (what the student was asked):
{prompt}

PASSAGE (article the student read):
{passage}

STUDENT PARAGRAPH:
{response}
"""


G35_CONVENTIONS = """You are grading ONE category of a Grade {grade} paragraph: CONVENTIONS (0-5).

Apply the STAAR clarity standard. Score based on overall command of grade-level conventions and impact on clarity:

- 5: Few errors (isolated slips). Reader can read smoothly without rereading. Student demonstrates consistent command of spelling, grammar, punctuation, and sentence construction.
- 4: A few noticeable errors but no strong pattern — one area may be slightly weak. Clarity still fully maintained.
- 3: Several errors OR one clear pattern (e.g., repeated spelling issues, recurring punctuation problems). Reader can still understand but notices the errors.
- 2: Many errors across multiple categories. Reader must work to understand in places.
- 1: Pervasive errors that impede comprehension in several sentences.
- 0: Writing is largely unintelligible.

KEY GUIDANCE:
- A few minor errors do NOT cost points if clarity is maintained.
- Focus on whether errors are FEW (isolated), SEVERAL (patterned), or MANY (pervasive).
- Do NOT count errors one-by-one against rigid thresholds. Judge overall command.
- The practical test: can a trained reader read this paragraph smoothly? If yes, score 5.
- The same standard applies across G3-G5. "Grade-level-appropriate" means a G3 student writing "becuase" once is not the same as a G5 student doing so — but the clarity test remains the same.

OUTPUT — valid JSON only:
{{
  "errors_noted": [<list of specific errors found>],
  "error_pattern": "few/several/many",
  "clarity_impact": "none/minor/significant",
  "conventions_score": <0-5>,
  "reasoning": "<1-2 sentences explaining the holistic judgment>"
}}

STUDENT PARAGRAPH:
{response}
"""


G68_STRUCTURE = """You are grading ONE category of a Grade {grade} expository essay: STRUCTURE (0-5).

Structure scores whether the response meets the five-paragraph architecture.

SCORING — START from the paragraph-count cap, then subtract only for listed defects:
  5+ paragraphs → START at 5/5
  4 paragraphs → START at 4/5
  3 paragraphs → START at 3/5
  2 paragraphs → START at 2/5
  1 paragraph  → START at 1/5

Within the cap, descend 1 point per structural defect ONLY for these specific issues:
  - Missing introduction (no thesis or topic statement)
  - Missing conclusion (essay just stops after last body paragraph)
  - Single-sentence body paragraph (a body paragraph with only one sentence)
Do NOT subtract for any other reason. Body-paragraph quality, topic drift, or weak transitions are Organization issues, NOT Structure.

Paragraph-count is NON-NEGOTIABLE and is the PRIMARY determinant of the score. If you count 5+ paragraphs with an intro and conclusion, the score is 5 unless a body paragraph is a single sentence.

OUTPUT — valid JSON only:
{{
  "structure_score": <integer 0-5>,
  "paragraph_count": <integer>,
  "defects": [<specific defects>],
  "reasoning": "<1-2 sentences>"
}}

ESSAY:
{response}
"""


G68_CONTENT = """You are grading TWO categories of a Grade {grade} expository essay:
  EVIDENCE & EXPLANATION (0-5) and ORGANIZATION (0-4).

═══ EVIDENCE & EXPLANATION (0-5) ═══
STEP 1 — Count P = passage-grounded details (paraphrase of specific passage claims; proper nouns; dates; places).
STEP 2 — Count C = genuine causal sentences.

🔒 WORKMANLIKE REASONING COUNTS — most common scoring failure:
Causal sentences do NOT need the word "because". Plainspoken reasoning that tells the reader WHAT HAPPENS AS A RESULT, WHY something matters, or HOW something works IS causal. COUNT these.

COUNTS as causal:
  - "in the process they carelessly remove milkweed plants" (consequence chain)
  - "The bridge became a gathering place, bringing neighborhoods together"
  - "This has brought increased profits to many businesses fueling the economy"
  - "These actions help scientists understand where the monarchs are and how to provide protection"
  - "gardens release oxygen which is especially beneficial in cities"
  - "children can study into the evening and businesses can be open later"
  - "This teaches children that it's okay for things to go wrong" (Path C interpretive)
  - "This shows that animated movies can teach children to work with others"
  - "After seeing their favorite animated characters do the right thing, that makes the children want to do it too"
  - "Animated movies can not replace real-world life lessons, but they can help children think"
  - "teaches it ok to make mistakes and try again"

DOES NOT count:
  - Bare restatement: "This shows butterflies are important" (tautology)
  - Formulaic with no new info: "This proves the bike lanes helped"
  - Simple fact without explanation

"this shows / this teaches": COUNTS when extending evidence to a NEW claim about WHY/HOW it matters; DOES NOT count when restating evidence with "this shows" prefix.

🔒 STRUCTURE-INDEPENDENCE RULE:
Count causal sentences THE SAME WAY whether the essay is 1 paragraph or 5 paragraphs.
If you found 3 causal sentences in a single-block essay, C=3 — do NOT reduce C because
"it's all one paragraph" or "the essay lacks structure." Structure is scored separately
in its own category. The Content score must reflect the content only.

RECOGNITION RULE: Before finalizing C, re-read every sentence. If it explains why/how/what-happens-as-a-result, count it, even if informal. DEFAULT HIGH when close — 3+ passage details + multiple "this shows / this helps / this means" moves should reach C≥2.

STEP 3 — P×C table:
          | C≥2 | C=1 | C=0 |
  P≥3     |  5  |  4  |  3  |
  P=2     |  4  |  3  |  2  |
  P=1     |  2  |  1  |  1  |
  P=0     |  0  |  0  |  0  |

═══ ORGANIZATION (0-4) ═══ (idea flow, NOT paragraph breaks)
  4 = Smooth varied transitions; ideas build on each other; consistent thesis focus. "Ideas build" means each paragraph advances the argument into new territory — parallel impacts that together build a complete picture count. It does NOT require each paragraph to causally cause the next.
  3 = Functional transitions, may be formulaic; essay flows.
  2 = Some transitions but arbitrary ordering OR drift from thesis.
  1 = Few/no transitions.
  0 = No flow.

OUTPUT — valid JSON only:
{{
  "evidence_score": <0-5>,
  "P_count": <int>,
  "C_count": <int>,
  "passage_details_used": [<3-5 details>],
  "causal_sentences": [<verbatim student sentences>],
  "organization_score": <0-4>,
  "transitions_used": [<actual words/phrases>],
  "thesis_focus": "<brief>",
  "reasoning": "<2-3 sentences>"
}}

PASSAGE:
{passage}

ESSAY:
{response}
"""


G68_SENTENCES = """You are grading ONE category of a Grade {grade} expository essay: SENTENCES (0-3).

Three 0/1 sub-dimensions: Variety, Clarity, Formal register. Sum for total.

Variety (0/1): 1 = mix of lengths/structures/openers; 0 = monotonous.
Clarity (0/1): 1 = clear on first reading; 0 = multiple sentences require re-reading due to awkward phrasing.
Register (0/1): 1 = age-appropriate academic; contractions OK; 1-2 idioms OK.
              0 = PERVASIVE (3+ distinct) slang, text-speak, or casual phrasing.

🔒 "PERVASIVE" THRESHOLD: register = 0 ONLY if you can cite 3+ distinct instances of slang/text-speak/conversational address. Two isolated idioms = NOT pervasive → register = 1.

🔒 CROSS-CATEGORY LOCK — DO NOT dock Sentences for grammar errors:
  "us citizens" (pronoun case) → Editing, not register
  "they helps" (S-V) → Editing, not clarity
  comma splice → Editing, not clarity
  missing word → Editing, not clarity
  Clarity = 0 ONLY for awkward syntax (not errors) requiring re-reading.

Typos and convention errors do NOT affect Sentences — those live in Editing.

OUTPUT — valid JSON only:
{{
  "variety_sub": <0-1>,
  "clarity_sub": <0-1>,
  "register_sub": <0-1>,
  "sentences_score": <sum 0-3>,
  "reasoning": "<1-2 sentences>"
}}

ESSAY:
{response}
"""


G68_EDITING = """You are grading ONE category of a Grade {grade} expository essay: EDITING (0-3).

Apply the STAAR clarity standard. Score based on overall command of conventions and impact on clarity:

- 3: Few errors (isolated slips). Reader can read smoothly without rereading. Student demonstrates consistent command of spelling, grammar, punctuation, and sentence construction.
- 2: Several errors OR one noticeable pattern (e.g., repeated spelling issues, recurring comma problems), but the reader can still understand the writer's thoughts throughout.
- 1: Many errors across multiple categories. Reader must work to understand in places. Student demonstrates inconsistent command of conventions.
- 0: Pervasive errors that impede comprehension. Reader cannot follow the writer's meaning.

KEY GUIDANCE:
- A few minor errors do NOT cost points if clarity is maintained.
- Focus on whether errors are FEW (isolated), SEVERAL (patterned), or MANY (pervasive).
- Do NOT count errors one-by-one against rigid thresholds. Judge overall command.
- The practical test: can a trained reader read this essay smoothly? If yes, score 3.

OUTPUT — valid JSON only:
{{
  "errors_noted": [<list of specific errors found, categorized by type>],
  "error_pattern": "few/several/many",
  "clarity_impact": "none/minor/significant",
  "editing_score": <0-3>,
  "reasoning": "<1-2 sentences explaining the holistic judgment>"
}}

ESSAY:
{response}
"""


# ─────────────────────────────────────────────────────────────────────────────
# VERBATIM POST-PROCESSOR — deterministic n-gram-based copy detection.
# Applied to G3-G5 Ideas after LLM scoring.
# ─────────────────────────────────────────────────────────────────────────────

def _normalize_text(text: str) -> str:
    """Lowercase, strip HTML, collapse whitespace, remove most punctuation.

    Used only for the verbatim post-processor (n-gram overlap on bag-of-words).
    Does NOT preserve paragraph structure.
    """
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = re.sub(r"[^\w\s']", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def _normalize_response_preserving_paragraphs(text: str) -> str:
    """Normalize student-response text for grading while preserving paragraph breaks.

    The Structure category's paragraph-count cap depends on detectable paragraph
    boundaries. Many student inputs arrive as HTML (`<p>...</p>`) or already have
    `\\n\\n` separators. This helper:
      - Converts block HTML tags (`<p>`, `<br>`, `<div>`, `<li>`) to newlines
      - Strips remaining inline HTML (`<strong>`, `<u>`, etc.)
      - Collapses runs of whitespace within a line but preserves blank lines
        between paragraphs
    Leaves plaintext responses with `\\n\\n` separators unchanged.
    """
    if not text:
        return ""
    # Convert block-level HTML to newlines
    t = re.sub(r"<\s*(p|br|div|li)\s*/?>", "\n", text, flags=re.IGNORECASE)
    t = re.sub(r"<\s*/\s*(p|div|li)\s*>", "\n", t, flags=re.IGNORECASE)
    # Strip remaining HTML tags
    t = re.sub(r"<[^>]+>", "", t)
    # Decode HTML entities conservatively
    t = t.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&#39;", "'").replace("&quot;", '"')
    # Collapse within-line whitespace runs (but preserve newlines)
    t = "\n".join(re.sub(r"[ \t]+", " ", line).strip() for line in t.splitlines())
    # Collapse 3+ consecutive newlines to 2 (standard paragraph separator)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def _tokens(text: str) -> list[str]:
    return _normalize_text(text).split()


def _ngrams(tokens: list[str], n: int = 5) -> list[tuple]:
    if len(tokens) < n:
        return []
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]


def verbatim_fraction(response: str, passage: str, n: int = 5) -> tuple[float, int, int]:
    """Return (n-gram overlap fraction, original-word count, total-word count).

    Original words = tokens in response not present in passage vocabulary.
    Fraction = (response n-grams found in passage) / (total response n-grams).
    """
    r_tok = _tokens(response)
    p_tok = _tokens(passage)
    if not r_tok:
        return 0.0, 0, 0
    if not p_tok:
        return 0.0, len(r_tok), len(r_tok)

    r_ngrams = _ngrams(r_tok, n)
    p_ngram_set = set(_ngrams(p_tok, n))
    if r_ngrams:
        matches = sum(1 for g in r_ngrams if g in p_ngram_set)
        frac = matches / len(r_ngrams)
    else:
        p_vocab = set(p_tok)
        frac = sum(1 for t in r_tok if t in p_vocab) / len(r_tok)

    p_vocab = set(p_tok)
    original_words = sum(1 for t in r_tok if t not in p_vocab)
    return frac, original_words, len(r_tok)


def apply_verbatim_cap(
    ideas_score: int, response: str, passage: str
) -> tuple[int, Optional[str]]:
    """Cap Ideas score per verbatim-copying rubric thresholds.

    Returns (new_ideas_score, cap_reason_or_None).

    Rules:
      Cap at 2: ≥80% verbatim OR (≥60% verbatim + <10% original + ≥40 words)
      Cap at 6: ≥50% verbatim OR (≥30% verbatim + <20% original + ≥40 words)
      Otherwise: no cap
    """
    frac, original_words, total_words = verbatim_fraction(response, passage)
    orig_ratio = (original_words / total_words) if total_words > 0 else 1.0

    if frac >= 0.80:
        return min(ideas_score, 2), f"{frac:.0%} verbatim → cap at 2"
    if frac >= 0.60 and orig_ratio < 0.10 and total_words >= 40:
        return min(ideas_score, 2), f"{frac:.0%} verbatim + {orig_ratio:.0%} original → cap at 2"
    if frac >= 0.50:
        return min(ideas_score, 6), f"{frac:.0%} verbatim → cap at 6"
    if frac >= 0.30 and orig_ratio < 0.20 and total_words >= 40:
        return min(ideas_score, 6), f"{frac:.0%} verbatim + {orig_ratio:.0%} original (light paraphrase) → cap at 6"
    return ideas_score, None


# ─────────────────────────────────────────────────────────────────────────────
# CATEGORY CALL — single Opus 4.7 API call for one category prompt.
# ─────────────────────────────────────────────────────────────────────────────

_SYSTEM = "You are a writing grader. Output ONLY valid JSON."


def _call_category(
    client,
    prompt_template: str,
    *,
    grade: int,
    passage: str = "",
    response: str = "",
    prompt: str = "",
    max_tokens: int = 3000,
    model: str = OPUS_MODEL,
) -> dict:
    """Issue one Opus 4.7 call for a category prompt; return parsed JSON."""
    filled = prompt_template.format(
        grade=grade,
        passage=passage or "",
        response=response or "",
        prompt=prompt or "",
    )
    kwargs = dict(
        model=model,
        max_tokens=max_tokens,
        system=_SYSTEM,
        messages=[{"role": "user", "content": filled}],
    )
    if _model_supports_temperature(model):
        kwargs["temperature"] = 0.0
    msg = _api_call_with_retry(client, **kwargs)
    text = extract_text(msg)
    return _parse_json(text) or {}


def _median_call_category(
    client,
    prompt_template: str,
    score_field: str,
    *,
    grade: int,
    passage: str = "",
    response: str = "",
    prompt: str = "",
    max_tokens: int = 3000,
    n_runs: int = 3,
) -> dict:
    """Run a category prompt N times in parallel; return the run whose score
    equals the median of the N scores.

    Rationale: Opus 4.7 at default temperature has ~±3 per-essay variance on
    G6-G8 causal-sentence recognition. Taking median-of-3 collapses that
    variance to ~±1 in practice while keeping total wall-clock low
    (3 parallel calls ≈ 1 call's latency).

    If n_runs == 1, falls through to _call_category (no median voting).
    """
    if n_runs <= 1:
        return _call_category(
            client, prompt_template,
            grade=grade, passage=passage, response=response, prompt=prompt,
            max_tokens=max_tokens,
        )

    with ThreadPoolExecutor(max_workers=n_runs) as ex:
        futures = [
            ex.submit(
                _call_category, client, prompt_template,
                grade=grade, passage=passage, response=response, prompt=prompt,
                max_tokens=max_tokens,
            )
            for _ in range(n_runs)
        ]
        runs = [f.result() for f in futures]

    # Extract scores per run
    scored_runs = []
    for r in runs:
        try:
            s = int(r.get(score_field, 0) or 0)
        except (TypeError, ValueError):
            s = 0
        scored_runs.append((s, r))
    scored_runs.sort(key=lambda x: x[0])
    # Median: middle element (rounds toward lower of two middles for even N)
    median_score = scored_runs[len(scored_runs) // 2][0]
    # Return the first run whose score equals the median (preserves full JSON)
    for s, r in scored_runs:
        if s == median_score:
            # Attach run-level metadata for debugging
            r.setdefault("_median_vote", {
                "n_runs": n_runs,
                "all_scores": [s_ for s_, _ in scored_runs],
                "median": median_score,
            })
            return r
    return runs[0]


# ─────────────────────────────────────────────────────────────────────────────
# STUDENT-FACING FEEDBACK COMPOSER
# ─────────────────────────────────────────────────────────────────────────────

_FEEDBACK_SYSTEM = (
    "You are the student-feedback writer for a writing grader. Given a fact "
    "skeleton summarizing what the grader observed, you paraphrase it into "
    "warm, specific, student-facing feedback. Rules: (1) Talk TO the student "
    "using 'you'. (2) Do NOT mention scores, points, or fractions — the total "
    "is shown separately. (3) Name ONE concrete detail the student used. "
    "(4) Keep it to 4-6 short sentences. (5) Never invent observations not in "
    "the skeleton. (6) No rubric jargon (no 'Path A', 'P×C', 'SP3'). Output "
    "ONLY valid JSON: {\"feedback\": \"<your feedback text>\"}."
)


def _compose_feedback_llm(client, skeleton: str, max_retries: int = 2) -> str:
    """Issue one short Claude call to paraphrase a fact skeleton into feedback.

    Returns the feedback string, or a mechanical fallback on parse/call failure.
    """
    for attempt in range(max_retries):
        try:
            kwargs = dict(
                model=OPUS_MODEL,
                max_tokens=800,
                system=_FEEDBACK_SYSTEM,
                messages=[{"role": "user", "content": skeleton}],
            )
            if _model_supports_temperature(OPUS_MODEL):
                kwargs["temperature"] = 0.3
            msg = _api_call_with_retry(client, **kwargs)
            text = extract_text(msg)
            data = _parse_json(text) or {}
            fb = data.get("feedback") or ""
            if isinstance(fb, str) and len(fb.strip()) >= 20:
                return fb.strip()
        except Exception as e:
            logger.warning(f"feedback composer attempt {attempt+1} failed: {e}")
    # Mechanical fallback so callers never get an empty-string
    return _mechanical_feedback_fallback(skeleton)


def _mechanical_feedback_fallback(skeleton: str) -> str:
    """Minimal feedback when the LLM call fails. Rare but keeps UX alive."""
    return (
        "Nice work on this one! Keep reading the passage carefully and "
        "connecting your ideas back to specific details from the text. "
        "Small proofreading passes make a big difference too."
    )


def _build_g35_skeleton(grade, ideas, conv, ideas_data, conv_data, cap_reason):
    lines = [
        f"Grade level: {grade} paragraph",
        f"Ideas score tier: {'exceptional' if ideas >= 14 else 'strong' if ideas >= 11 else 'developing' if ideas >= 7 else 'limited'}",
        f"Conventions tier: {'clean' if conv >= 4 else 'some-errors' if conv >= 2 else 'many-errors'}",
    ]
    paths = ideas_data.get("paths_detected") or {}
    active = [k for k, v in paths.items() if v] if isinstance(paths, dict) else []
    if active:
        lines.append(f"Development strategies detected: {', '.join(active)}")
    details = ideas_data.get("passage_details_used") or []
    if details:
        lines.append(f"Passage details the student used: {details[:3]}")
    causal = ideas_data.get("causal_sentences") or []
    if causal:
        lines.append(f"Causal/explanatory sentences the student wrote: {causal[:2]}")
    if ideas_data.get("prompt_addressed") is False:
        lines.append("Issue: response does not fully answer the specific question the prompt asked")
    if cap_reason:
        lines.append(f"Issue: response contains substantial verbatim copying — {cap_reason}")
    # Convention flags
    for cat in ("spelling_notable", "grammar_notable", "punctuation_notable"):
        items = conv_data.get(cat) or []
        if items:
            lines.append(f"{cat.replace('_',' ')}: {items[:3]}")
    return "\n".join(lines)


def _build_g68_skeleton(grade, struct_data, content_data, sent_data, edit_data,
                        structure, evidence, organization, sentences, editing):
    lines = [
        f"Grade level: {grade} essay",
        f"Structure: {structure}/5 (paragraphs: {struct_data.get('paragraph_count','?')})",
        f"Evidence: {evidence}/5",
        f"Organization: {organization}/4",
        f"Sentences: {sentences}/3",
        f"Editing: {editing}/3",
    ]
    defects = struct_data.get("defects") or []
    if defects:
        lines.append(f"Structural defects: {defects[:3]}")
    details = content_data.get("passage_details_used") or []
    if details:
        lines.append(f"Passage details the student used: {details[:4]}")
    causal = content_data.get("causal_sentences") or []
    if causal:
        lines.append(f"Causal/explanatory sentences: {causal[:2]}")
    transitions = content_data.get("transitions_used") or []
    if transitions:
        lines.append(f"Transitions used: {transitions[:5]}")
    thesis = content_data.get("thesis_focus")
    if thesis:
        lines.append(f"Thesis focus: {thesis}")
    for cat in ("spelling_notable", "grammar_notable", "punctuation_notable"):
        items = edit_data.get(cat) or []
        if items:
            lines.append(f"{cat.replace('_',' ')}: {items[:3]}")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC ENTRY POINTS
# ─────────────────────────────────────────────────────────────────────────────

def score_g35_paragraph(
    client,
    *,
    grade: int,
    passage: str,
    response: str,
    prompt: str = "",
    qnum: int = 11,
    max_score: int = 20,
    compose_feedback: bool = True,
) -> QuestionScore:
    """Grade a G3-G5 paragraph with the per-cat v2a engine.

    Args:
        compose_feedback: If True (default), issues an extra short Claude call
          to paraphrase the category observations into student-facing feedback.
          Set False when wrapping this in a consensus layer that will run the
          scorer N times — only the winning run needs feedback composed.

    Returns a QuestionScore with ideas_score, conventions_score, total_score,
    and internal_notes capturing the verbatim cap if one fired.
    """
    if _is_blank_response(response):
        return QuestionScore.blank(qnum, max_score, grade)

    response = _normalize_response_preserving_paragraphs(response)

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=2) as ex:
        f_ideas = ex.submit(
            _call_category,
            client, G35_IDEAS,
            grade=grade, passage=passage, response=response, prompt=prompt,
        )
        f_conv = ex.submit(
            _call_category,
            client, G35_CONVENTIONS,
            grade=grade, response=response,
        )
        ideas_data = f_ideas.result()
        conv_data = f_conv.result()

    raw_ideas = int(ideas_data.get("ideas_score", 0) or 0)
    raw_ideas = max(0, min(15, raw_ideas))
    conv = int(conv_data.get("conventions_score", 0) or 0)
    conv = max(0, min(5, conv))

    capped_ideas, cap_reason = apply_verbatim_cap(raw_ideas, response, passage)
    total = capped_ideas + conv

    notes_parts = [f"per_cat_v2a G{grade} paragraph in {time.time()-t0:.1f}s"]
    if cap_reason:
        notes_parts.append(f"verbatim_cap: {cap_reason} (raw Ideas {raw_ideas} → {capped_ideas})")
    notes_parts.append(
        f"P={ideas_data.get('P_count','?')} C={ideas_data.get('C_count','?')} "
        f"paths={ideas_data.get('paths_detected','?')} "
        f"prompt_addressed={ideas_data.get('prompt_addressed','?')}"
    )
    notes_parts.append(f"notables={conv_data.get('total_notables','?')}")
    internal_notes = " | ".join(notes_parts)

    skeleton = _build_g35_skeleton(grade, capped_ideas, conv, ideas_data, conv_data, cap_reason)
    feedback = _compose_feedback_llm(client, skeleton) if compose_feedback else ""

    # Stash the skeleton in teacher_notes so a consensus wrapper can
    # re-compose feedback on the winning run without recomputing.
    teacher_notes = (
        f"Ideas reasoning: {ideas_data.get('reasoning','')}\n"
        f"Conventions reasoning: {conv_data.get('reasoning','')}\n"
        f"[skeleton]{skeleton}[/skeleton]"
    )

    return QuestionScore(
        question=qnum,
        ideas_score=capped_ideas, ideas_max=15,
        organization_score=0, organization_max=0,
        conventions_score=conv, conventions_max=5,
        total_score=total, total_max=max_score,
        feedback=feedback,
        internal_notes=internal_notes,
        teacher_notes=teacher_notes,
    )


def score_g68_essay(
    client,
    *,
    grade: int,
    passage: str,
    response: str,
    prompt: str = "",
    qnum: int = 11,
    max_score: int = 20,
    compose_feedback: bool = True,
) -> QuestionScore:
    """Grade a G6-G8 expository essay with the per-cat v2a engine.

    Each category is scored via median-of-N (default N=3) to control
    per-essay LLM variance. Total wall-clock is ~max(category latency) since
    all N runs × 4 categories fire in parallel.

    Returns a QuestionScore with ideas_score = structure+evidence,
    organization_score = organization+sentences, conventions_score = editing,
    matching the existing Alpha sub-score convention.
    """
    if _is_blank_response(response):
        return QuestionScore.blank(qnum, max_score, grade)

    response = _normalize_response_preserving_paragraphs(response)

    n = G68_CATEGORY_N
    t0 = time.time()
    # Fire all category × run combinations in parallel.
    # Content is voted on evidence_score since that's the category most
    # affected by causal-count variance; organization_score rides with it.
    with ThreadPoolExecutor(max_workers=max(4, 4 * n)) as ex:
        f_struct = ex.submit(
            _median_call_category, client, G68_STRUCTURE, "structure_score",
            grade=grade, response=response, n_runs=n,
        )
        f_content = ex.submit(
            _median_call_category, client, G68_CONTENT, "evidence_score",
            grade=grade, passage=passage, response=response, n_runs=n,
        )
        f_sent = ex.submit(
            _median_call_category, client, G68_SENTENCES, "sentences_score",
            grade=grade, response=response, n_runs=n,
        )
        f_edit = ex.submit(
            _median_call_category, client, G68_EDITING, "editing_score",
            grade=grade, response=response, n_runs=n,
        )
        struct_data = f_struct.result()
        content_data = f_content.result()
        sent_data = f_sent.result()
        edit_data = f_edit.result()

    structure = max(0, min(5, int(struct_data.get("structure_score", 0) or 0)))
    evidence = max(0, min(5, int(content_data.get("evidence_score", 0) or 0)))
    organization = max(0, min(4, int(content_data.get("organization_score", 0) or 0)))
    sentences = max(0, min(3, int(sent_data.get("sentences_score", 0) or 0)))
    editing = max(0, min(3, int(edit_data.get("editing_score", 0) or 0)))
    total = structure + evidence + organization + sentences + editing

    # Alpha sub-score convention: Ideas=Structure+Evidence (10), Org=Org+Sent (7), Conv=Editing (3).
    ideas_sub = structure + evidence
    org_sub = organization + sentences

    # Summarize median-vote spreads for debugging
    def _vote_summary(d):
        v = d.get("_median_vote")
        return f'{v["all_scores"]}' if v else "single"

    internal_notes = (
        f"per_cat_v2a G{grade} essay (median-of-{n}) in {time.time()-t0:.1f}s | "
        f"S={structure}{_vote_summary(struct_data)} E={evidence}{_vote_summary(content_data)} "
        f"O={organization} Sent={sentences}{_vote_summary(sent_data)} Ed={editing}{_vote_summary(edit_data)} | "
        f"P={content_data.get('P_count','?')} C={content_data.get('C_count','?')} | "
        f"paragraph_count={struct_data.get('paragraph_count','?')}"
    )
    teacher_notes = "\n".join([
        f"Structure: {struct_data.get('reasoning','')}",
        f"Content: {content_data.get('reasoning','')}",
        f"Sentences: {sent_data.get('reasoning','')}",
        f"Editing: {edit_data.get('reasoning','')}",
    ])

    skeleton = _build_g68_skeleton(
        grade, struct_data, content_data, sent_data, edit_data,
        structure, evidence, organization, sentences, editing,
    )
    feedback = _compose_feedback_llm(client, skeleton) if compose_feedback else ""

    # Stash skeleton in teacher_notes for consensus re-composition.
    teacher_notes = teacher_notes + f"\n[skeleton]{skeleton}[/skeleton]"

    return QuestionScore(
        question=qnum,
        ideas_score=ideas_sub, ideas_max=10,
        organization_score=org_sub, organization_max=7,
        conventions_score=editing, conventions_max=3,
        total_score=total, total_max=max_score,
        feedback=feedback,
        internal_notes=internal_notes,
        teacher_notes=teacher_notes,
    )


def score_q11_per_cat(
    client,
    *,
    grade: int,
    passage: str,
    response: str,
    prompt: str = "",
    qnum: int = 11,
    max_score: int = 20,
    compose_feedback: bool = True,
) -> QuestionScore:
    """Top-level per-cat entry point. Routes to G3-G5 or G6-G8 engine by grade.

    compose_feedback=False when being called from a consensus wrapper that will
    run this N times and only compose feedback for the winning run.
    """
    assert qnum == 11, "per-cat engine currently supports Q11 only"
    if grade < 6:
        return score_g35_paragraph(
            client, grade=grade, passage=passage, response=response,
            prompt=prompt, qnum=qnum, max_score=max_score,
            compose_feedback=compose_feedback,
        )
    return score_g68_essay(
        client, grade=grade, passage=passage, response=response,
        prompt=prompt, qnum=qnum, max_score=max_score,
        compose_feedback=compose_feedback,
    )


def compose_feedback_from_score(client, score: QuestionScore) -> str:
    """Compose student-facing feedback for an already-scored per_cat result.

    Extracts the skeleton stashed in teacher_notes during scoring and issues
    one short Claude paraphrase call. Used by the consensus wrapper to avoid
    composing feedback on every run — only on the winning run.

    Falls through to the mechanical fallback if no skeleton is found.
    """
    import re as _re
    tn = score.teacher_notes or ""
    m = _re.search(r"\[skeleton\](.*?)\[/skeleton\]", tn, _re.DOTALL)
    if not m:
        return _mechanical_feedback_fallback("")
    return _compose_feedback_llm(client, m.group(1).strip())
