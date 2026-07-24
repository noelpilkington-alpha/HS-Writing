"""
Tests for the PP100 form-bank QC gate + builder (Phase A2).

pp100_forms.qc_form_bank(lesson_id, forms, taught_source, stim) enforces the equivalence contract from the
design spec: every form in a lesson's bank must hold constant the grain (unit), rubric_ref, frq_type, and mode,
and each form's held-out source must (a) exist in the stimulus bank, (b) be distinct from every other form's
source in this lesson, and (c) not equal the article's taught source. No em dash anywhere in a form's prompt.

Pure functions; a tiny fake stimulus map stands in for STIM so the test is deterministic.
"""
import os
import sys

HERE = os.path.dirname(__file__)
PIPE = os.path.join(HERE, "..")
sys.path.insert(0, PIPE)

import pp100_forms as PF


class _Stim:
    def __init__(self, family="single", mode="argument", grade="9"):
        self.family, self.mode, self.grade = family, mode, grade


# a fake bank of vetted sources
FAKE_STIM = {
    "SRC-A": _Stim(),
    "SRC-B": _Stim(),
    "SRC-C": _Stim(),
    "TAUGHT": _Stim(),
}


def _f(source, prompt="<p>Write one claim.</p>", unit="sentence", rubric="rc.staar", frq="writing", mode="argument"):
    return {"source": source, "prompt_html": prompt, "unit": unit, "rubric_ref": rubric,
            "frq_type": frq, "mode": mode}


def test_equivalent_bank_passes():
    forms = [_f("SRC-A"), _f("SRC-B"), _f("SRC-C")]
    ok, problems = PF.qc_form_bank("L1", forms, taught_source="TAUGHT", stim=FAKE_STIM)
    assert ok, problems


def test_grain_mismatch_fails():
    forms = [_f("SRC-A", unit="sentence"), _f("SRC-B", unit="paragraph")]
    ok, problems = PF.qc_form_bank("L1", forms, taught_source="TAUGHT", stim=FAKE_STIM)
    assert not ok
    assert any("grain" in p or "unit" in p for p in problems)


def test_rubric_mismatch_fails():
    forms = [_f("SRC-A", rubric="rc.staar"), _f("SRC-B", rubric="rc.4trait")]
    ok, problems = PF.qc_form_bank("L1", forms, taught_source="TAUGHT", stim=FAKE_STIM)
    assert not ok
    assert any("rubric" in p for p in problems)


def test_duplicate_source_within_lesson_fails():
    forms = [_f("SRC-A"), _f("SRC-A")]
    ok, problems = PF.qc_form_bank("L1", forms, taught_source="TAUGHT", stim=FAKE_STIM)
    assert not ok
    assert any("distinct" in p or "duplicate" in p for p in problems)


def test_taught_source_reuse_fails():
    """A form may not use the source the article already taught (seen-in-lesson leakage)."""
    forms = [_f("SRC-A"), _f("TAUGHT")]
    ok, problems = PF.qc_form_bank("L1", forms, taught_source="TAUGHT", stim=FAKE_STIM)
    assert not ok
    assert any("taught" in p or "article" in p for p in problems)


def test_missing_source_in_bank_fails():
    forms = [_f("SRC-A"), _f("SRC-NONEXISTENT")]
    ok, problems = PF.qc_form_bank("L1", forms, taught_source="TAUGHT", stim=FAKE_STIM)
    assert not ok
    assert any("exist" in p or "not in" in p.lower() for p in problems)


def test_em_dash_in_prompt_fails():
    forms = [_f("SRC-A", prompt="<p>Write one claim — take a side.</p>")]
    ok, problems = PF.qc_form_bank("L1", forms, taught_source="TAUGHT", stim=FAKE_STIM)
    assert not ok
    assert any("em dash" in p or "em-dash" in p for p in problems)


def test_source_free_forms_skip_source_checks():
    """A source-free lesson (source=None on every form) is exempt from the source-existence/distinctness checks
    but still gated on grain/rubric/em-dash. Distinctness for source-free forms is on prompt text instead."""
    forms = [_f(None, prompt="<p>Take a position with your own example A.</p>"),
             _f(None, prompt="<p>Take a position with your own example B.</p>")]
    ok, problems = PF.qc_form_bank("L1", forms, taught_source=None, stim=FAKE_STIM)
    assert ok, problems


def test_source_free_identical_prompts_fail():
    forms = [_f(None, prompt="<p>Same prompt.</p>"), _f(None, prompt="<p>Same prompt.</p>")]
    ok, problems = PF.qc_form_bank("L1", forms, taught_source=None, stim=FAKE_STIM)
    assert not ok
    assert any("distinct" in p or "identical" in p for p in problems)


def test_empty_bank_fails():
    ok, problems = PF.qc_form_bank("L1", [], taught_source="TAUGHT", stim=FAKE_STIM)
    assert not ok
