"""Tier B judge harness - verify the verifier's promotion machinery (B1/B5/B6/B7).

No API: deterministic fake judges + tmp ledger/kill-switch paths. Proves the machinery that decides
WHETHER an LLM judge may block is itself sound - a judge cannot block until it has probed clean N
times, a kill-switch demotes it instantly, and the three-way verdict routes uncertainty to triage
rather than a silent hard-fail.
"""
from __future__ import annotations

import os
import sys

PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)

import tier_b_judge as TB  # noqa: E402
from tier_b_judge import (PASS, FAIL, LOW_CONFIDENCE, three_way_verdict, adversarial_rubric,
                          make_adversarial_verifier, probe, record_probe, can_block, authority_for,
                          PROMOTE_AFTER_N_GREEN)  # noqa: E402
from judge_calibration import CALIBRATION_CASES  # noqa: E402


# ---- fakes -----------------------------------------------------------------------------------

def _perfect(excerpt, rubric):
    for c in CALIBRATION_CASES:
        if excerpt == c.before:
            return True
        if excerpt == c.after:
            return False
    return False


def _blind(excerpt, rubric):
    return False


# ---- B1: adversarial framing -----------------------------------------------------------------

def test_adversarial_rubric_is_fail_closed():
    r = adversarial_rubric("Is any distractor also correct?")
    assert "REFUTE" in r and "cannot" in r.lower()
    assert "when genuinely uncertain, flag it" in r.lower()


def test_adversarial_wrapper_preserves_contract_and_passes_framed_rubric():
    seen = {}

    def raw(excerpt, rubric):
        seen["rubric"] = rubric
        return True
    v = make_adversarial_verifier(raw)
    out = v("some excerpt", "base rule")
    assert out is True
    assert "REFUTE" in seen["rubric"], "wrapper did not apply the adversarial frame"


# ---- B5: three-way verdict -------------------------------------------------------------------

def test_three_way_unanimous_flag_is_fail():
    assert three_way_verdict([True, True, True]) == FAIL


def test_three_way_unanimous_clean_is_pass():
    assert three_way_verdict([False, False, False]) == PASS


def test_three_way_split_is_low_confidence():
    assert three_way_verdict([True, False, True]) == LOW_CONFIDENCE


def test_single_flag_is_low_confidence_not_fail():
    """A lone verifier asserting a defect is a triage trigger, not an automatic block."""
    assert three_way_verdict([True]) == LOW_CONFIDENCE
    assert three_way_verdict([False]) == PASS


# ---- B6: probe-before-block ------------------------------------------------------------------

def test_probe_perfect_judge_clears():
    res = probe(_perfect)
    assert res["clears"] is True and res["recall"] == 1.0 and res["precision"] == 1.0


def test_probe_blind_judge_does_not_clear():
    res = probe(_blind)
    assert res["clears"] is False and res["recall"] == 0.0


# ---- B7: promotion ledger + kill-switch ------------------------------------------------------

def test_judge_cannot_block_until_n_consecutive_green(tmp_path):
    ledger = str(tmp_path / "ledger.json")
    ks = str(tmp_path / "killswitch")
    name = "j"
    assert not can_block(name, ledger, ks), "un-probed judge must not be able to block"
    for i in range(PROMOTE_AFTER_N_GREEN - 1):
        record_probe(name, probe(_perfect), ledger_path=ledger, stamp=f"t{i}")
        assert not can_block(name, ledger, ks), f"blocked too early at streak {i+1}"
    record_probe(name, probe(_perfect), ledger_path=ledger, stamp="tN")
    assert can_block(name, ledger, ks), "judge should be promoted after N consecutive green probes"


def test_one_bad_probe_resets_the_streak(tmp_path):
    ledger = str(tmp_path / "ledger.json")
    ks = str(tmp_path / "killswitch")
    name = "j"
    for i in range(PROMOTE_AFTER_N_GREEN):
        record_probe(name, probe(_perfect), ledger_path=ledger, stamp=f"g{i}")
    assert can_block(name, ledger, ks)
    record_probe(name, probe(_blind), ledger_path=ledger, stamp="bad")   # a drift/regression run
    assert not can_block(name, ledger, ks), "one non-clearing probe must reset the green streak to 0"


def test_killswitch_demotes_a_promoted_judge_instantly(tmp_path):
    ledger = str(tmp_path / "ledger.json")
    ks = str(tmp_path / "killswitch")
    name = "j"
    for i in range(PROMOTE_AFTER_N_GREEN):
        record_probe(name, probe(_perfect), ledger_path=ledger, stamp=f"g{i}")
    assert can_block(name, ledger, ks)
    with open(ks, "w", encoding="utf-8") as fh:
        fh.write(name + "\n")
    assert not can_block(name, ledger, ks), "kill-switch must demote a promoted judge without a code change"


# ---- authority_for: raw verdict -> enforced action -------------------------------------------

def test_unpromoted_fail_is_downgraded_to_triage(tmp_path):
    ledger = str(tmp_path / "ledger.json")
    ks = str(tmp_path / "killswitch")
    # no probes recorded -> not promoted
    assert authority_for("j", FAIL, ledger, ks) == "triage", "un-promoted FAIL must not hard-block"
    assert authority_for("j", LOW_CONFIDENCE, ledger, ks) == "triage"
    assert authority_for("j", PASS, ledger, ks) == "pass"


def test_promoted_fail_blocks_but_low_confidence_still_triages(tmp_path):
    ledger = str(tmp_path / "ledger.json")
    ks = str(tmp_path / "killswitch")
    name = "j"
    for i in range(PROMOTE_AFTER_N_GREEN):
        record_probe(name, probe(_perfect), ledger_path=ledger, stamp=f"g{i}")
    assert authority_for(name, FAIL, ledger, ks) == "block", "promoted FAIL should block"
    assert authority_for(name, LOW_CONFIDENCE, ledger, ks) == "triage", "LOW_CONFIDENCE always triages"
    assert authority_for(name, PASS, ledger, ks) == "pass"
