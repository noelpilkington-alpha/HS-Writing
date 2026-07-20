import os, sys
PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path: sys.path.insert(0, PIPE)
from lesson_contract import Slot, Lesson, gate_structural_item

def _disc(nopts):
    ch = [{"id": chr(65+i), "text": f"option {i} with enough words to be real here", "correct": i==nopts-1,
           "why": "because reasons"} for i in range(nopts)]
    s = Slot("MODEL", "discrimination", "q", body="Pick one.", choices=ch)
    return Lesson(id="X", grade="9-10", lesson_type=2, unit="U", title="T", target="t", slots=[s])

def test_three_option_discrimination_fails():
    ok, msg = gate_structural_item(_disc(3))
    assert not ok and ("4" in msg or "four" in msg.lower())

def test_four_option_discrimination_passes():
    ok, _ = gate_structural_item(_disc(4))
    assert ok

def test_self_score_two_option_still_passes():
    ch = [{"id":"pass","text":"yes all present and correct here","correct":True,"why":"y"},
          {"id":"gap","text":"no at least one missing or weak","correct":False,"why":"n"}]
    s = Slot("INDEPENDENT","self_score","score",body="predict",choices=ch)
    L = Lesson(id="X",grade="9-10",lesson_type=7,unit="U",title="T",target="t",slots=[s])
    ok, _ = gate_structural_item(L)
    assert ok
