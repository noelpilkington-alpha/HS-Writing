"""Tier-A regression runner - smoke + invariants.

The runner composes every deterministic offline gate per lesson. These tests pin two things that
would otherwise silently rot:
  1. issue_frame stimuli are exempted from the source-PASSAGE gates (word floor / fact table / Lexile
     / source_config) - the documented by-design exemption; without it the runner over-flags ~9
     claim-tier lessons on frames that were never meant to be full passages.
  2. the runner reproduces EXACTLY the 4 genuine mastery-genre mismatches from the triage and nothing
     else (G9 fully clean) - i.e. the Tier-A floor surfaces the real defects with no noise.
"""
from __future__ import annotations

import os
import sys

PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)

from tier_a_regression import audit_lesson, run_all, _ISSUE_FRAME_NA_GATES  # noqa: E402
from g9_push_dryrun import STIM  # noqa: E402


EXPECTED_GENRE_MISMATCHES = {
    "ACC-W910-L-G10-C1006-0021",
    "ACC-W910-L-G10-C1003-0025",
    "ACC-W1112-L-G11-C1102-0030",
    "ACC-W910-L-G12-C1202-0012",
}


def test_g9_is_fully_clean():
    """G9 (the first course to ship) must be 27/27 clean on the full deterministic floor."""
    results = run_all()["G9"]
    fails = [r["lesson_id"] for r in results if not r["passed"]]
    assert not fails, f"G9 not clean on Tier-A floor: {fails}\n" + "\n".join(
        b for r in results for b in r["blockers"])


def test_only_the_four_triage_mismatches_remain():
    """Across the whole course the ONLY deterministic blockers are the 4 genuine mastery-genre
    mismatches - no over-flagging (the documented failure mode)."""
    failing = {r["lesson_id"] for _g, results in run_all().items() for r in results if not r["passed"]}
    assert failing == EXPECTED_GENRE_MISMATCHES, (
        f"missing={EXPECTED_GENRE_MISMATCHES - failing}  extra={failing - EXPECTED_GENRE_MISMATCHES}")


def test_issue_frame_passage_gates_are_exempted_not_failed():
    """A claim-tier lesson bound to an issue_frame must PASS: the frame's source-passage gates are
    recorded n/a, not counted as blockers. Guards the over-flag exemption directly."""
    # G9 L01 binds a FRAME source (issue_frame). Find any G9 lesson that binds an issue_frame.
    from tier_a_regression import _lessons, _bound_stimulus_ids
    hit = None
    for _f, L in _lessons("G9"):
        for sid in _bound_stimulus_ids(L):
            s = STIM.get(sid)
            if s is not None and getattr(s, "family", "") == "issue_frame":
                hit = (L, sid)
                break
        if hit:
            break
    assert hit, "no G9 lesson binds an issue_frame stimulus (fixture assumption broke)"
    L, sid = hit
    r = audit_lesson(L, "G9")
    # every N/A gate for that frame is recorded as passed n/a, and none is a blocker
    for name in _ISSUE_FRAME_NA_GATES:
        key = f"stimulus[{sid}]:{name}"
        if key in r["gates"]:
            assert r["gates"][key]["passed"], f"{key} should be n/a-passed for an issue_frame"
            assert "n/a (issue_frame" in r["gates"][key]["detail"], r["gates"][key]
    assert not any(sid in b and any(n in b for n in _ISSUE_FRAME_NA_GATES) for b in r["blockers"]), \
        f"issue_frame passage gate leaked into blockers: {r['blockers']}"


def test_receipt_shape():
    """Every receipt carries the fields a downstream consumer (checkpoint report) relies on."""
    from tier_a_regression import _lessons
    _f, L = next(iter(_lessons("G9")))
    r = audit_lesson(L, "G9")
    for k in ("lesson_id", "title", "gates", "blockers", "passed"):
        assert k in r, f"receipt missing {k}"
    assert isinstance(r["gates"], dict) and r["gates"], "receipt has no gate results"
