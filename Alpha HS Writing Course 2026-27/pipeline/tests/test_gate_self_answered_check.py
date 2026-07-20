# pipeline/tests/test_gate_self_answered_check.py
import os, sys
PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path: sys.path.insert(0, PIPE)
from lesson_contract import Slot, Lesson, gate_self_answered_check

def _L(body): return Lesson(id="X",grade="9-10",lesson_type=2,unit="U",title="T",target="t",
                            slots=[Slot("MODEL","diagnosis_frq","check",body=body)])

def test_pure_giveaway_fails():
    # prompt answers its own checks AND gives the student no independent turn
    body=("Run the 3-question test on this draft. Does it take a side? No, it just reports a fact. "
          "Is there a reason? No. Now you have the fixed version.")
    ok, msg = gate_self_answered_check(_L(body))
    assert not ok

def test_coping_model_then_own_turn_passes():
    # the modeled check runs on a PROVIDED weak draft, THEN the student does their own -> sanctioned
    body=("Run the check on this provided weak draft. Does it take a side? No, add one. "
          "Now write a fresh claim of your own and run the same three checks on it.")
    ok, _ = gate_self_answered_check(_L(body))
    assert ok

def test_clean_diagnosis_no_selfanswers_passes():
    body=("Run the 3-question test on your draft, then rewrite it so it passes all three.")
    ok, _ = gate_self_answered_check(_L(body))
    assert ok

def test_giveaway_with_bare_rewrite_tail_but_no_provided_specimen_fails():
    """The hole a bare own-turn tail used to leave open is now CLOSED (reviewer's tightening, Task 4).
    A prompt that pre-answers its own checks and appends 'now rewrite it' but names NO provided specimen
    is a giveaway wearing a fig leaf, not a coping model -> it must FAIL. The sanctioned exemption now
    requires BOTH an own-turn signal AND a named provided draft (see test below)."""
    body=("Does it take a side? No, it just reports a fact. Is there a reason? No. Now rewrite it.")
    ok, _ = gate_self_answered_check(_L(body))
    assert not ok

def test_sanctioned_coping_model_with_provided_weak_draft_passes():
    """The real bank pattern: pre-answered checks that diagnose a NAMED provided weak draft, then an
    independent student turn. This is the coping model and must PASS."""
    body=("Run the check on this weak draft. Does it take a side? No, add one. "
          "Now rewrite the weak draft, then name which question your rewrite fixed.")
    ok, _ = gate_self_answered_check(_L(body))
    assert ok
