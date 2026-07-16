"""Judge-calibration harness - verify the verifier's verifier (Tier B).

The judge_calibration corpus is the ANSWER KEY an LLM judge is scored against. This test proves the
SCORING HARNESS itself is sound, using deterministic fake judges (no API): a perfect judge scores
composite 1.0, a blind judge (flags nothing) scores recall 0, and an over-flagger (flags everything)
scores precision 0. If the harness could not tell these apart, it could not certify a real judge.

Also asserts the corpus invariants: every case is fully labeled and traces to a real lesson + fix
commit (so a label is never a paraphrase nobody can check).
"""
from __future__ import annotations

import os
import sys

PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)

from judge_calibration import CALIBRATION_CASES, CalibrationCase, score_judge  # noqa: E402


# ---- fake judges (deterministic) -------------------------------------------------------------

def _perfect_judge(excerpt, rubric):
    """Flags exactly the `before` excerpts, passes the `after` ones - by matching each case's text."""
    for c in CALIBRATION_CASES:
        if excerpt == c.before:
            return True
        if excerpt == c.after:
            return False
    return False


def _blind_judge(excerpt, rubric):
    return False            # never flags anything (misses every real defect)


def _overflag_judge(excerpt, rubric):
    return True             # flags everything (re-litigates every fixed lesson)


# ---- (1) the harness distinguishes the three judge behaviors ---------------------------------

def test_perfect_judge_scores_composite_one():
    res = score_judge(_perfect_judge)
    assert res["recall"] == 1.0, res
    assert res["precision"] == 1.0, res
    assert res["composite"] == 1.0, res
    assert all(cd["flagged_before"] and cd["passed_after"] for cd in res["cases"]), res["cases"]


def test_blind_judge_has_zero_recall():
    """A judge that flags nothing must score recall 0 (it misses every real defect) - the harness must
    catch blindness, or it could certify a judge that passes everything."""
    res = score_judge(_blind_judge)
    assert res["recall"] == 0.0, res
    assert res["precision"] == 1.0, res       # it never over-flags, but that is worthless here
    assert res["composite"] == 0.0, res


def test_overflagging_judge_has_zero_precision():
    """A judge that flags everything must score precision 0 (it re-litigates every fixed lesson) - the
    harness must catch the documented over-flag failure mode."""
    res = score_judge(_overflag_judge)
    assert res["precision"] == 0.0, res
    assert res["recall"] == 1.0, res          # it 'catches' everything, but that is worthless here
    assert res["composite"] == 0.0, res


def test_composite_penalizes_a_single_miss():
    """A judge that misses exactly one before (blind on one defect class) drops below 1.0 - the key
    is not all-or-nothing padding."""
    miss = CALIBRATION_CASES[0]

    def _one_miss_judge(excerpt, rubric):
        if excerpt == miss.before:
            return False                       # miss this one real defect
        return _perfect_judge(excerpt, rubric)

    res = score_judge(_one_miss_judge)
    assert res["recall"] < 1.0, res
    assert res["composite"] < 1.0, res


# ---- (2) corpus invariants -------------------------------------------------------------------

def test_every_case_is_fully_labeled_and_traceable():
    assert CALIBRATION_CASES, "calibration corpus is empty"
    for c in CALIBRATION_CASES:
        assert isinstance(c, CalibrationCase)
        assert c.before and c.after and c.before != c.after, f"{c.id}: before/after missing or identical"
        assert c.rubric.strip(), f"{c.id}: no rubric"
        assert c.lesson_id.startswith("ACC-"), f"{c.id}: lesson_id not a real ACC id"
        assert len(c.fix_commit) >= 7, f"{c.id}: fix_commit not a real short hash"
        assert c.why_before_fails.strip() and c.why_after_passes.strip(), f"{c.id}: missing rationale"


def test_defect_classes_cover_this_sessions_semantic_defects():
    """The three semantic defects this session found+fixed must each be represented (so a regression
    of any one is measurable against a live judge)."""
    classes = {c.defect_class for c in CALIBRATION_CASES}
    for required in ("also_correct_distractor", "planner_grain_mismatch", "phantom_draft_diagnosis"):
        assert required in classes, f"missing calibration case for semantic defect: {required}"
