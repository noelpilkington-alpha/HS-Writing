# tests/test_sse_test_taker.py
import os, sys
PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)
from sim_student_eval.test_taker import load_g9_test_items, present_item


def test_loads_items_with_separated_answer_key():
    items = load_g9_test_items()
    assert len(items) > 10  # G9 bank has many SR + CR items
    mcq = [i for i in items if i["kind"] == "choice"]
    assert mcq, "expected some choice items"
    m = mcq[0]
    # answer key is stored for the harness, but options carry NO correctness signal
    assert "answer_key" in m and m["answer_key"]
    for opt in m["options"]:
        assert set(opt.keys()) == {"id", "text"}, "option leaked correct/rationale to student"


def test_present_item_hides_the_key():
    items = load_g9_test_items()
    mcq = next(i for i in items if i["kind"] == "choice")
    shown = present_item(mcq)
    assert mcq["stem"][:20] in shown
    # the correct-answer rationale text must never appear in what the student sees
    assert "rationale" not in shown.lower()


def test_extended_text_items_present_stem_only():
    items = load_g9_test_items()
    et = [i for i in items if i["kind"] == "extended-text"]
    assert et, "expected CR extended-text items"
    shown = present_item(et[0])
    assert et[0]["stem"][:20] in shown
