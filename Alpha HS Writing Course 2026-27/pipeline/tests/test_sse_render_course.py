# tests/test_sse_render_course.py
import os, sys
PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)
from sim_student_eval.render_course import load_g9_lessons, student_view, short_id


def test_loads_29_lessons_in_order():
    # G9 was 26; the 2026-07-21 counterargument add (overturning S2) inserted a new U4 Counterargument unit
    # (3 lessons: l19 recognize / l20 concede-answer / l21 paragraph, KC C.9.07) and renumbered the essay+gate
    # block l19,l21-l27 -> l22-l29 (now G9 U5). Net G9 = 29 lessons. See docs/plans/2026-07-21-g9-counterargument-add.md.
    ls = load_g9_lessons()
    assert len(ls) == 29
    # first is l01 arguable claim, last is l29 gate argument essay (filename order)
    assert short_id(ls[0]).startswith("g9_l01")
    assert short_id(ls[-1]).startswith("g9_l29")


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


def test_all_grades_load_in_lesson_order():
    from sim_student_eval.render_course import load_lessons, GRADES
    import re
    counts = {}
    for g in GRADES:
        ls = load_lessons(g)
        assert ls, f"{g} loaded no lessons"
        sids = [short_id(L) for L in ls]
        for s in sids:                                   # dev-free short ids for every grade
            assert "ACC-" not in s and "_v3_1" not in s and not s.startswith("lesson_")
        nums = [int(re.search(r"_l(\d+)", s).group(1)) for s in sids]
        assert nums == sorted(nums), f"{g} out of lesson order: {nums}"
        counts[g] = len(ls)
    # G9 = 29 after the 2026-07-21 counterargument add (+3 new U4 lessons; overturns S2). G10 25, G11 31, G12 16.
    assert counts == {"g9": 29, "g10": 25, "g11": 31, "g12": 16}, counts


def test_composition_probes_are_structural_and_cover_original_g9_set():
    from sim_student_eval.render_course import load_lessons
    from sim_student_eval.student_agent import is_composition_lesson
    g9 = load_lessons("g9")
    probes = {short_id(L).rsplit("_", 0)[0] for L in g9 if is_composition_lesson(L)}
    # structural detection (type 7/8 or gate) must be a SUPERSET of the known composition lessons.
    # File numbers shifted with the 2026-07-21 counterargument add (essay+gate block renumbered to l22-l29):
    # the paragraph builders (l17/l18) + the essay/gate block (l22-l26, l28 informational gate, l29 argument gate).
    for want in ("g9_l18", "g9_l24", "g9_l26", "g9_l28", "g9_l29"):
        assert any(p.startswith(want) for p in probes), f"{want} not detected as a composition probe"
    # every grade produces a non-empty probe set
    for g in ("g10", "g11", "g12"):
        assert any(is_composition_lesson(L) for L in load_lessons(g)), f"{g} has no composition probes"
