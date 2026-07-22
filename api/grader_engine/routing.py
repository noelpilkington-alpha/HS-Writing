"""Grading routing table — the GRADER-OWNED source of truth for what (grain, construct) combos are gradeable.

Futureproofing for skill-pack regeneration (design: Grading_Regeneration_Contract_DESIGN.md).
A skill pack regenerates a lesson with NEW content but the SAME structure. Grading must therefore route off
DECLARED fields only — never off content inferred from the prompt wording (which changes every regeneration):

    (unit, frq_type)  ->  a validated scorer.

  - unit      = the GRAIN / scale:   sentence | paragraph | multi_paragraph | essay   (course UNIT_LADDER)
  - frq_type  = the CONSTRUCT:        revision (transform a provided draft) | writing (produce from a task)
  - rubric_ref (rc.*) selects the STANDARD family WITHIN the essay/paragraph scorers; sentence scorers are
    standard-agnostic (skill+conventions), so rubric_ref is not needed to pick the sentence scorer.

HYBRID grading (decision 2026-07-21): the grader always receives THIS lesson's regenerated stimulus+prompt+
response and scores the ACTUAL question, but against a VALIDATED NAMED scorer selected here — NOT a rubric the
skill pack hand-authors. Keeps the anchor-validation; resilient to content regeneration.

This module is the SINGLE SOURCE OF TRUTH. The course contract mirrors SUPPORTED as a thin capability set and
a drift test asserts they match (it does not copy the grader's scoring rules — only which tuples are accepted).
"""
from __future__ import annotations

# grain -> allowed frq_type constructs (course declares one of these per scored production_frq)
UNIT_LADDER = ["sentence", "paragraph", "multi_paragraph", "essay"]
FRQ_TYPES = ["revision", "writing"]

# (unit, frq_type) -> scorer key. The /score route maps each scorer key to an engine call.
#   "sentence_revision" -> panel sentence-revision (Skill 0-1 + Conv 0-1 = 2)   [VALIDATED, reused from G3-8]
#   "sentence_writing"  -> panel sentence-writing  (Answer 0-2 + Conv 0-1 = 3)  [VALIDATED, reused from G3-8]
#   "paragraph"         -> paragraph engine        [Phase 2 — reserved, needs G9-12 calibration]
#   "essay"             -> essay engines (rc.sbac / rc.4trait / rc.staar)        [VALIDATED + LIVE]
ROUTING = {
    ("sentence", "revision"): "sentence_revision",
    ("sentence", "writing"): "sentence_writing",
    ("paragraph", "revision"): "paragraph",
    ("paragraph", "writing"): "paragraph",
    ("multi_paragraph", "writing"): "essay",
    ("multi_paragraph", "revision"): "essay",
    ("essay", "writing"): "essay",
    ("essay", "revision"): "essay",
}

# The capability set the course contract validates declared tuples against (thin — tuples only, no rules).
SUPPORTED = set(ROUTING)

# Scorer keys IMPLEMENTED + validated on the live /score path.
#   paragraph = panel_joey 3-trait (Ideas+Org+Conv=10) with the G9-12 calibration band, for single
#   analytical/argumentative paragraphs. Bounded validation (2026-07-21): discriminates strong/weak, no
#   inflation of weak; NO grade+construct-matched paragraph ground truth exists (all HS anchors are
#   sub-paragraph or full-essay — see Grading_Regeneration_Contract_DESIGN.md), so it is validated by
#   construct-fit + spot-check + the already-validated panel_joey mechanics, NOT by paragraph anchor papers.
IMPLEMENTED = {"sentence_revision", "sentence_writing", "paragraph", "essay"}


def resolve(unit: str, frq_type: str) -> str | None:
    """Return the scorer key for a declared (unit, frq_type), or None if the combo is not supported."""
    return ROUTING.get((unit or "", frq_type or ""))


def is_implemented(scorer_key: str) -> bool:
    return scorer_key in IMPLEMENTED


def default_frq_type(unit: str) -> str:
    """Essay/multi_paragraph default to 'writing' (they are always produce-from-task); sentence/paragraph must
    declare it explicitly (the construct is load-bearing there)."""
    return "writing"


def capability_manifest() -> dict:
    """The thin capability set the course mirrors + the drift test compares against."""
    return {
        "unit_ladder": list(UNIT_LADDER),
        "frq_types": list(FRQ_TYPES),
        "supported": sorted(f"{u}:{t}" for (u, t) in SUPPORTED),
        "implemented_scorers": sorted(IMPLEMENTED),
    }
