# tests/test_sse_render_course.py
import os, sys
PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)
from sim_student_eval.render_course import load_g9_lessons, student_view, short_id


def test_loads_27_lessons_in_order():
    ls = load_g9_lessons()
    assert len(ls) == 27
    # first is l01 arguable claim, last is l27 gate argument essay (filename order)
    assert short_id(ls[0]).startswith("g9_l01")
    assert short_id(ls[-1]).startswith("g9_l27")


def test_short_id_has_no_internal_id():
    ls = load_g9_lessons()
    sid = short_id(ls[8])  # l09 warrant
    assert "ACC-" not in sid and "_v3_1" not in sid and "lesson_" not in sid
    assert sid.startswith("g9_l09")


def test_student_view_is_dev_free_and_nonempty():
    ls = load_g9_lessons()
    view = student_view(ls[8])
    assert len(view) > 500
    assert "STEP 1" in view
    # NONE of these development internals may leak to a student:
    for banned in ("lesson_type", "acc_tags", "Slot(", "Lesson(", "qc_lesson",
                   "mnemonic_status", "lesson_class", "ACC-W910", "design bet", "Grade-C"):
        assert banned not in view, f"dev internal leaked into student view: {banned}"
