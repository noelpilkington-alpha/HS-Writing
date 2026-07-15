import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lesson_contract import Lesson, Slot, grain, qc_lesson


_TITLES = {
    "teach_card": "The one idea", "stimulus_display": "The debate on screen",
    "annotated_before_after": "Watch a weak claim become strong",
    "discrimination": "Which claim is stronger?", "predict_the_fix": "What is wrong here?",
    "production_frq": "Write your response", "diagnosis_frq": "Check and fix this draft",
    "self_score": "Score your own work",
}
# realistic-minimal bodies that clear _DEPTH_FLOOR; the diagnosis body carries a checklist scaffold so
# gate_model_before_required passes. These fixtures test contract LOGIC, not authored content quality.
_BODIES = {
    "teach_card": ("<p>An arguable claim is a sentence that takes a clear side and gives one checkable reason.</p>"
                   "<p>It is not a topic and not a feeling.</p>"
                   "<ul><li>State what you believe.</li><li>Give one reason a reader could test.</li>"
                   "<li>Write it so someone could disagree.</li></ul>"),
    "annotated_before_after": ("<p><b>BEFORE:</b> Buses matter to the city.</p>"
                               "<p><b>AFTER:</b> The city should make buses free because free rides cut car "
                               "traffic and help people who cannot afford a car get to work.</p>"
                               "<p>The AFTER takes a side and gives one checkable reason; the BEFORE just "
                               "names a topic.</p>"),
    "predict_the_fix": ("This draft says free buses are good because they are helpful. Predict the fix: it names "
                        "no checkable reason, so it cannot be argued with. Choose the option that adds a real "
                        "reason."),
    "discrimination": ("Which claim takes a side and gives one checkable reason a reader could test? Pick the "
                       "stronger of the two options below and say why the other one falls short."),
    "production_frq": ("Write one arguable claim on the source above: take a side and give one checkable reason. "
                       "State it in a single sentence a reader could argue with."),
    "diagnosis_frq": ("Reread what you just wrote. Run this checklist and fix any line that fails. "
                      "<ol><li>Did you take a clear side?</li><li>Is there one checkable reason?</li>"
                      "<li>Could a reader argue with it?</li></ol> Rewrite any sentence that does not pass."),
    "self_score": ("Score your own claim against the rubric: 1 point for a clear side, 1 point for a checkable "
                   "reason. Predict your score, then check it against the rubric shown."),
}


def _slot(role, kind, unit="", bank="", **kw):
    kw.setdefault("body", _BODIES.get(kind, ""))
    if kind == "predict_the_fix":
        kw.setdefault("feedback", "The fix adds a checkable reason so the claim can be argued with.")
    return Slot(role=role, kind=kind, title=_TITLES.get(kind, "Do this"), unit=unit, bank=bank,
                scored=(kind in ("production_frq", "diagnosis_frq")), **kw)


def _prov():
    return {"mnemonic_status": "proposal"}


def _practice_essay():
    # canonical post-rearchitecture essay: ONE full write + self-revision, NO in-article transfer.
    return Lesson(id="X-PRACTICE", grade="9-10", lesson_type=7, unit="U", title="T", target="t", provenance=_prov(),
        lesson_class="practice",
        slots=[
            _slot("TEACH", "teach_card"),
            _slot("MODEL", "stimulus_display", bank="a", ref="ACC-W910-FRAME-FOURDAYWEEK"),
            _slot("MODEL", "annotated_before_after", bank="a"),
            _slot("MODEL", "discrimination", bank="a", labeled_grade_c=True),
            _slot("MODEL", "predict_the_fix", bank="a"),
            _slot("SUPPORTED", "production_frq", unit="multi_paragraph", bank="a", rubric_ref="rc.staar"),
            _slot("INDEPENDENT", "production_frq", unit="essay", bank="a", rubric_ref="rc.staar"),
            _slot("INDEPENDENT", "diagnosis_frq", unit="essay", bank="a", rubric_ref="rc.staar"),
            _slot("INDEPENDENT", "self_score"),
        ])


def _practice_sentence():
    # sentence grain: dense discrimination, 3 short writes, near-variation transfer, NO diagnosis required.
    return Lesson(id="X-SENT", grade="9-10", lesson_type=2, unit="U", title="T", target="t", provenance=_prov(),
        lesson_class="practice",
        slots=[
            _slot("TEACH", "teach_card"),
            _slot("MODEL", "stimulus_display", bank="a", ref="ACC-W910-FRAME-FOURDAYWEEK"),
            _slot("MODEL", "annotated_before_after", bank="a"),
            _slot("MODEL", "discrimination", bank="a", labeled_grade_c=True),
            _slot("MODEL", "discrimination", bank="a", labeled_grade_c=True),
            _slot("MODEL", "predict_the_fix", bank="a"),
            _slot("SUPPORTED", "production_frq", unit="sentence", bank="a", rubric_ref="rc.staar"),
            _slot("INDEPENDENT", "production_frq", unit="sentence", bank="a", rubric_ref="rc.staar"),
            _slot("TRANSFER", "production_frq", unit="sentence", bank="a-var", rubric_ref="rc.staar"),
            _slot("INDEPENDENT", "self_score"),
        ])


def _gate():
    # scaffold-free: bare cue, UNSCORED plan affordance, held-out cold write, post-hoc self_score.
    plan = Slot(role="SUPPORTED", kind="production_frq", title="Plan your essay", unit="essay", bank="held",
                ref="ACC-W910-FRAME-FREETRANSIT", rubric_ref="rc.ap", scored=False,
                body=("<p>Before you write, jot a quick plan.</p>"
                      "<ul><li>Your main claim.</li><li>The moves you will use, in order.</li>"
                      "<li>The objection you will answer.</li></ul>"
                      "<p>This plan is not graded; it is your map for the cold write.</p>"))
    return Lesson(id="X-GATE", grade="9-10", lesson_type=8, unit="U", title="Gate", target="t", provenance=_prov(),
        lesson_class="gate",
        slots=[
            _slot("TEACH", "teach_card"),
            _slot("TEACH", "stimulus_display", bank="held", ref="ACC-W910-FRAME-FREETRANSIT"),
            plan,
            _slot("TRANSFER", "production_frq", unit="essay", bank="held", rubric_ref="rc.ap"),
            _slot("INDEPENDENT", "self_score"),
        ])


def test_grain_from_terminal_unit():
    assert grain(_practice_essay()) == "essay"
    assert grain(_practice_sentence()) == "sentence"


def test_practice_essay_passes_without_transfer():
    r = qc_lesson(_practice_essay())
    assert r["passed"], (r["first_failure"], {k: v for k, v in r["gates"].items() if not v["passed"]})


def test_practice_sentence_passes_without_diagnosis():
    r = qc_lesson(_practice_sentence())
    assert r["passed"], (r["first_failure"], {k: v for k, v in r["gates"].items() if not v["passed"]})


def test_gate_passes_when_scaffold_free():
    r = qc_lesson(_gate())
    assert r["passed"], (r["first_failure"], {k: v for k, v in r["gates"].items() if not v["passed"]})


def test_gate_rejects_smuggled_scaffold():
    g = _gate()
    g.slots.insert(1, _slot("MODEL", "annotated_before_after", bank="held"))
    r = qc_lesson(g)
    assert not r["passed"]
    # gate_gate_shape must flag the smuggled scaffold (it may not be the FIRST failure, since a smuggled
    # slot can also trip other gates; the point is gate_gate_shape catches it).
    assert not r["gates"]["gate_gate_shape"]["passed"], r["gates"]["gate_gate_shape"]
    assert "annotated_before_after" in r["gates"]["gate_gate_shape"]["detail"]
