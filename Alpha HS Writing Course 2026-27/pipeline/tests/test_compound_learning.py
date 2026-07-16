"""Compound-learning metric - prove it is a RECEIPT, not a self-report (Tier C1/C2).

The whole value of the metric is that it cannot be gamed: a defect record claiming automated coverage
whose anchor (fixture / gate / calibration case) does NOT actually exist must be counted as UNCOVERED.
These tests verify that against the LIVE corpus, and pin the goal state (0 human-only defects) so a
future regression that drops a fixture makes the metric go RED, not silently stay green.
"""
from __future__ import annotations

import os
import sys

PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)

import compound_learning as CL  # noqa: E402
from compound_learning import (DefectRecord, verify_coverage, metric, next_actions,
                               DET_GATE, JUDGE_CASE, UNCOVERED)  # noqa: E402


# ---- the goal state: every seeded defect has VERIFIED coverage -------------------------------

def test_metric_reports_zero_human_only_defects():
    m = metric()
    assert m["caught_by_human_not_by_gate"] == 0, (
        f"uncovered defects: {m['uncovered_ids']} - each needs a fixture or calibration case")
    assert m["coverage_rate"] == 1.0
    assert not next_actions(), f"next_actions should be empty at the goal state: {next_actions()}"


def test_every_ledger_record_verifies_against_the_live_corpus():
    """Each record's claimed anchor must actually exist in fixtures.py / judge_calibration right now."""
    for r in CL.DEFECT_LEDGER:
        assert verify_coverage(r), (
            f"{r.id} claims {r.coverage_kind} but its anchor does not exist in the live corpus "
            f"(gate={r.fixture_gate!r} scope={r.fixture_scope!r} class={r.calibration_class!r})")


# ---- the metric cannot be gamed: a phantom anchor counts as UNCOVERED -------------------------

def test_det_gate_claim_with_missing_fixture_is_uncovered():
    """A record claiming a deterministic gate whose known-bad fixture does NOT exist must NOT verify."""
    fake = DefectRecord("fake_det", "claims a gate with no fixture", caught_by="human",
                        date="2026-07-16", coverage_kind=DET_GATE,
                        fixture_gate="a_gate_that_does_not_exist", fixture_scope="lesson")
    assert verify_coverage(fake) is False


def test_judge_claim_with_missing_calibration_class_is_uncovered():
    fake = DefectRecord("fake_judge", "claims a calibration class that isn't in the corpus",
                        caught_by="human", date="2026-07-16", coverage_kind=JUDGE_CASE,
                        calibration_class="no_such_defect_class")
    assert verify_coverage(fake) is False


def test_uncovered_record_raises_the_number_and_lists_an_action():
    """C1 ratchet: appending a genuinely uncovered defect must (a) raise caught_by_human_not_by_gate
    and (b) surface a concrete next action - the mechanism that turns a review catch into a to-do."""
    before = metric()["caught_by_human_not_by_gate"]
    orig = list(CL.DEFECT_LEDGER)
    try:
        CL.DEFECT_LEDGER.append(DefectRecord(
            "brand_new_uncovered", "a defect a human just caught with no coverage yet",
            caught_by="human", date="2026-07-16", coverage_kind=UNCOVERED, recurrences=2))
        m = metric()
        assert m["caught_by_human_not_by_gate"] == before + 1
        acts = next_actions()
        assert any(a["id"] == "brand_new_uncovered" for a in acts), acts
        # richest signal (recurrences>=2) is ordered first
        assert acts[0]["recurrences"] >= 2
    finally:
        CL.DEFECT_LEDGER[:] = orig   # never leak test state into the module ledger


# ---- this session's specific defects are all represented -------------------------------------

def test_this_sessions_defects_are_in_the_ledger():
    ids = {r.id for r in CL.DEFECT_LEDGER}
    for required in ("also_correct_distractor", "planner_grain_mismatch", "phantom_draft_diagnosis",
                     "childish_stimulus_opener", "mastery_genre_mismatch"):
        assert required in ids, f"session defect not tracked in the compound-learning ledger: {required}"
