"""STAAR-rubric variant of the panel grader — for the rubric-vs-prompting experiment.

Reuses panel.py's machinery (preflight, _run_panel, _call_rubric_grader, _call_synthesis)
UNCHANGED. The ONLY difference is the rubric: STAAR's authentic 5-point scale
(Development/Organization 0-3 + Conventions 0-2) replacing Alpha's 20-point scale.

Same engine, same model, same judge architecture, same corpus → isolates the rubric variable.

Authentic STAAR rubric source: 2025 STAAR RLA Constructed-Response Scoring Guides (G3-G8),
in Grading Standards Documentation/. Same 5-point rubric for paragraph (G3-5) and essay (G6-8).
"""
from __future__ import annotations

from .models import QuestionScore
from .panel import (
    RubricDimension,
    _age_hint,
    _preflight,
    _run_panel,
    _default_panel_model,
    _build_audit,
)
from .per_cat import _normalize_response_preserving_paragraphs


# ═══════════════════════════════════════════════════════════════════════════════
# STAAR RUBRIC — Development/Organization of Ideas (0-3)
# Verbatim-grounded in the 2025 STAAR RLA scoring-guide descriptors.
# ═══════════════════════════════════════════════════════════════════════════════

_STAAR_DEVELOPMENT_PROMPT = """Score ORGANIZATION AND DEVELOPMENT OF IDEAS on the STAAR 0-3 scale.

This single trait covers central idea, organization, evidence, AND expression together — STAAR does
NOT score these as separate point-buckets. Judge the response holistically against the score-point
descriptors below and assign the ONE score point whose description best fits.

SCORE POINT 3 — Fully developed:
- Central idea is clear and fully developed; focus is consistent throughout; response is unified and
  easy to follow.
- Organization is effective: a purposeful structure with an effective introduction and conclusion;
  ideas logically connected.
- Evidence is specific, well chosen, and relevant; it is CLEARLY EXPLAINED and CONSISTENTLY supports
  and develops the central idea.
- Expression is clear and effective; word choice is specific and purposeful.

SCORE POINT 2 — Partially developed:
- Central idea is present but partially developed; may not be clearly identifiable; focus may not
  always be consistent.
- Organization is limited: an intro and conclusion are present, but structure may be inconsistent or
  not always support development; sentence-to-sentence connections may be lacking.
- Evidence is limited and may include some irrelevant information; it may be INSUFFICIENTLY EXPLAINED.
- Expression is basic; word choice may be general or imprecise.

SCORE POINT 1 — Minimally developed:
- Central idea is unclear or only minimally present.
- Little or no organizational structure; may read as a list.
- Minimal text-based evidence, or evidence is presented with little or no explanation.
- Expression is unclear; word choice is vague or imprecise.

SCORE POINT 0 — Insufficient:
- No clear central idea responsive to the prompt, OR off-topic, OR incoherent, OR a near-verbatim
  restatement of the prompt/passage with no original writing, OR no text evidence at all.

KEY CALIBRATION (from STAAR's own standard):
- The discriminator between 2 and 3 is whether evidence is CLEARLY EXPLAINED and reasoning runs
  THROUGHOUT (3) vs. evidence that is listed/summarized with explanation only in places (2).
- Causal/explanatory reasoning need NOT use the word "because" or formal transitions — plainspoken
  reasoning that tells why evidence matters or what happens as a result counts as explanation.
- Do NOT require sophistication beyond the grade level. A grade-appropriate fully-developed response
  earns 3 even if simple. Reward what the student demonstrates; do not score against an ideal ceiling.
- This is a 4-point scale (0-3). Most complete, on-prompt, passage-grounded responses with consistent
  explanation are a 3. Reserve 2 for genuinely uneven development, not for "good but not perfect."

Output evidence as short observations tying specific phrases to the descriptor; reasoning as 2-3
sentences naming which score point fits and why (esp. the 2-vs-3 call)."""


_STAAR_CONVENTIONS_PROMPT = """Score CONVENTIONS on the STAAR 0-2 scale.

This trait covers sentence construction, punctuation, capitalization, grammar, and spelling together.
Judge overall COMMAND, not error count. The controlling question is impact on clarity.

SCORE POINT 2 — Consistent command:
- The student demonstrates consistent command of grade-level-appropriate conventions.
- The response has FEW errors, and those errors DO NOT impact the clarity of the writing.
- A few minor, isolated slips (one spelling error, a missing comma) are fully acceptable at this level.

SCORE POINT 1 — Inconsistent command:
- Limited/inconsistent use of correct grade-level conventions.
- The response has SEVERAL errors (noticeable, often patterned), but the reader can still understand
  the writer's thoughts overall.

SCORE POINT 0 — Little to no command:
- MANY errors that affect clarity and the reader's understanding.
- Sentence boundaries, grammar, spelling, punctuation break down so often that meaning is impaired.

KEY CALIBRATION:
- Do NOT count errors against a rigid threshold. Ask: few (SP2), several (SP1), or many/disruptive (SP0)?
- A repeated single skill gap (e.g. the same the/there confusion) is ONE pattern, not N errors.
- The practical test: can a trained reader read this smoothly without rereading to decode it? If yes,
  and errors are few/isolated, score 2.
- Grade-level-appropriate: a G3 student's occasional phonetic misspelling is more acceptable than the
  same in G8, but the few/several/many framework is identical across grades.

Output evidence as categorized observations (spelling, punctuation, grammar, sentence construction,
clarity); reasoning as 1-2 sentences."""


# ═══════════════════════════════════════════════════════════════════════════════
# STAAR JUDGE / SYNTHESIS
# ═══════════════════════════════════════════════════════════════════════════════

_STAAR_SYNTHESIS = """Combine the panel's two STAAR-trait recommendations into a final STAAR score.

The STAAR extended-constructed-response score is the SUM of two traits:
  - Organization and Development of Ideas (0-3)
  - Conventions (0-2)
  Total = 0-5.

Apply these rules BEFORE finalizing:

1. CASCADE RULE (authentic STAAR): If Development = 0, Conventions is also 0. Apply automatically.
2. Verbatim-copy check: If the response copies substantial passage text with only trivial paraphrasing,
   Development cannot exceed 1 (the writing is not the student's own). Only apply with specific overlap.
3. Score-vs-evidence consistency: If a panel grader's reasoning contradicts its score, override to
   match the evidence it listed, and explain.
4. Do NOT inflate or deflate beyond what the descriptors warrant. STAAR is a coarse 5-point scale; a
   solid, complete, grade-appropriate response is a 3+2=5 and that is correct and expected — do not
   withhold the top point to seem rigorous. Equally, do not award 3 to a response that only lists
   evidence without explanation.

If no override is needed, accept the panel scores as-is.

Student-facing feedback should:
- Talk TO the student using "you"; name one specific thing they did well (a passage detail, a clear
  structure, clean mechanics).
- Name ONE concrete, actionable improvement drawn from the rubric evidence (if Development < 3, the
  usual lever is explaining WHY/HOW the evidence matters; give a short model sentence).
- Be 4-6 sentences, encouraging, age-appropriate. Never mention scores, points, or rubric names.

Return JSON: { "totalScore": <0-5>, "maxScore": 5,
  "categoryScores": [{"rubricId":"development","name":"Organization & Development","score":<0-3>,
   "maxPoints":3,"overridden":<bool>,"overrideReason":<string|null>},
  {"rubricId":"conventions","name":"Conventions","score":<0-2>,"maxPoints":2,
   "overridden":<bool>,"overrideReason":<string|null>}],
  "feedback":"<student-facing>", "reasoning":"<audit trail, not shown to student>" }"""


_STAAR_INTRO = """You are an experienced STAAR Reading Language Arts grader scoring a Grade {grade}
student's written response.

The student read a short text and wrote a response to a specific question about it. You will receive
the source text, the exact question, and the student's writing. Your job — with the rest of the panel —
is to score it on the authentic STAAR constructed-response rubric.

The STAAR rubric scores the response out of 5 total points across two traits:
- Organization and Development of Ideas (0-3): central idea, organization, evidence, explanation, expression.
- Conventions (0-2): sentence construction, punctuation, capitalization, grammar, spelling.

The student is {age_hint}. Score what the student demonstrates at grade level; do not penalize for the
absence of sophistication the rubric does not demand, and do not withhold full marks from a complete,
well-developed, grade-appropriate response."""


# ═══════════════════════════════════════════════════════════════════════════════
# PUBLIC API
# ═══════════════════════════════════════════════════════════════════════════════

def score_panel_staar(
    client,
    *,
    grade: int,
    passage: str,
    question: str,
    response: str,
    qnum: int = 11,
) -> QuestionScore:
    """Score a Q11 paragraph (G3-5) or essay (G6-8) on the STAAR 5-point rubric.

    Same panel engine as panel.py; only the rubric differs. Returns a QuestionScore
    with ideas_score = Development (0-3), conventions_score = Conventions (0-2),
    total_score = 0-5.
    """
    gate = _preflight(response)
    if gate == "empty":
        return QuestionScore.blank(qnum, 5, grade)
    if gate == "gibberish":
        return QuestionScore.gibberish(qnum, 5, grade)

    response = _normalize_response_preserving_paragraphs(response)
    model = _default_panel_model()
    intro = _STAAR_INTRO.format(grade=grade, age_hint=_age_hint(grade))

    dimensions = [
        RubricDimension(id="development", name="Organization & Development of Ideas",
                        max_points=3, prompt=_STAAR_DEVELOPMENT_PROMPT),
        RubricDimension(id="conventions", name="Conventions",
                        max_points=2, prompt=_STAAR_CONVENTIONS_PROMPT),
    ]

    synthesis, panel_results, elapsed = _run_panel(
        client, dimensions, intro, passage, question, response, grade, model, _STAAR_SYNTHESIS)

    dev = max(0, min(3, synthesis.category_scores.get("development", panel_results[0].score)))
    conv = max(0, min(2, synthesis.category_scores.get("conventions", panel_results[1].score)))
    # Cascade rule enforced deterministically as a backstop to the judge.
    if dev == 0:
        conv = 0
    total = dev + conv

    internal_notes, teacher_notes = _build_audit(panel_results, synthesis, elapsed, qnum, grade)
    internal_notes = "STAAR " + internal_notes + f" | dev={dev} conv={conv} total={total}/5"

    return QuestionScore(
        question=qnum, ideas_score=dev, ideas_max=3,
        organization_score=0, organization_max=0,
        conventions_score=conv, conventions_max=2,
        total_score=total, total_max=5,
        feedback=synthesis.feedback,
        internal_notes=internal_notes, teacher_notes=teacher_notes,
    )
