# pipeline/tests/test_gate_check_cadence.py
import os, sys
PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path: sys.path.insert(0, PIPE)
from lesson_contract import Slot, Lesson, gate_check_cadence

def _mk(lt, kinds_tags, lesson_class="practice"):
    slots=[]
    for k,tag in kinds_tags:
        slots.append(Slot("TEACH" if k in ("teach_card","stimulus_display","annotated_before_after") else "MODEL",
                          k, "s", body="x"*120, tag=tag,
                          choices=[{"id":"A","text":"a","correct":True,"why":"y"}] if k=="discrimination" else []))
    return Lesson(id="X",grade="9-10",lesson_type=lt,unit="U",title="T",target="t",slots=slots,lesson_class=lesson_class)

def test_concept_four_teach_no_check_fails():
    L=_mk(2, [("teach_card",""),("teach_card",""),("teach_card",""),("teach_card","")])
    ok,msg=gate_check_cadence(L); assert not ok

def test_concept_three_then_check_passes():
    L=_mk(2, [("teach_card",""),("teach_card",""),("teach_card",""),("discrimination","")])
    ok,_=gate_check_cadence(L); assert ok

def test_memorizable_tool_tightens_to_two():
    # tool card, then 2 more teach with no check -> exceeds min(3,2)=2
    L=_mk(2, [("teach_card","memorizable_tool"),("teach_card",""),("teach_card","")])
    ok,_=gate_check_cadence(L); assert not ok

def test_worked_example_run_counts_as_one():
    # 3 consecutive annotated_before_after = ONE worked example, +1 teach, then check -> ok under N=3
    L=_mk(2, [("annotated_before_after",""),("annotated_before_after",""),("annotated_before_after",""),
              ("teach_card",""),("discrimination","")])
    ok,_=gate_check_cadence(L); assert ok

def test_buy_in_counts_zero():
    L=_mk(2, [("teach_card","buy_in"),("teach_card","buy_in"),("teach_card",""),("teach_card",""),("teach_card",""),("discrimination","")])
    ok,_=gate_check_cadence(L); assert ok  # only 3 counted before the check

def test_gate_class_exempt():
    L=_mk(7, [("teach_card",""),("teach_card",""),("teach_card",""),("teach_card","")], lesson_class="gate")
    ok,_=gate_check_cadence(L); assert ok

def test_worked_examples_separated_by_a_write_do_not_collapse():
    # REGRESSION (Task 6 review): two worked examples with a WRITE between them are DISTINCT, not one run.
    # A/B, production_frq, A/B, teach, teach on a concept lesson = 4 counted (WE1 + WE2 + teach + teach) -> FAIL.
    # (Bug was: prev_worked survived the write's continue, collapsing the two A/B into one -> false PASS.)
    L=_mk(2, [("annotated_before_after",""),("production_frq",""),("annotated_before_after",""),
              ("teach_card",""),("teach_card","")])
    ok,_=gate_check_cadence(L); assert not ok

def test_worked_examples_separated_by_a_buyin_do_not_collapse():
    # same escape via a buy_in card between two worked examples -> must still count them separately.
    L=_mk(2, [("annotated_before_after",""),("teach_card","buy_in"),("annotated_before_after",""),
              ("teach_card",""),("teach_card","")])
    ok,_=gate_check_cadence(L); assert not ok
