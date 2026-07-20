# pipeline/tests/test_gate_frame_comma.py
import os, sys
PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path: sys.path.insert(0, PIPE)
from lesson_contract import Slot, Lesson, gate_frame_comma

def _L(*slots): return Lesson(id="X", grade="9-10", lesson_type=2, unit="U", title="T", target="t", slots=list(slots))

def test_bad_comma_before_because_in_frame():
    # a fill-in frame with the offending comma
    s = Slot("SUPPORTED", "production_frq", "w",
             body='<div>Copy this frame: Schools should ______ [your side], because ______ [your reason].</div>')
    ok, msg = gate_frame_comma(_L(s))
    assert not ok and "because" in msg.lower()

def test_good_frame_no_comma():
    s = Slot("SUPPORTED", "production_frq", "w",
             body='<div>Copy this frame: Schools should ______ [your side] because ______ [your reason].</div>')
    ok, _ = gate_frame_comma(_L(s))
    assert ok

def test_ordinary_prose_comma_before_because_is_fine():
    # NOT a fill-in frame (no blanks) -> a normal sentence with ", because" must NOT be flagged
    s = Slot("TEACH", "teach_card", "t",
             body='<div>A claim is arguable, because someone could disagree with it.</div>')
    ok, _ = gate_frame_comma(_L(s))
    assert ok
