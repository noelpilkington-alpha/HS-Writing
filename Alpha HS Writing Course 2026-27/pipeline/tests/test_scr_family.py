import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from item_contract import Item, qc_item

def _scr_writing(**kw):
    base = dict(id="ACC-W910-SCR-WRIT-0001", family="SCR", grade="9-10",
                subskill_or_mode="scr_writing", qti_type="text-entry",
                stem="Rewrite the sentence to fix the dangling modifier.",
                acc_tags=["ACC.W.CONV.1", "CCSS.L.9-10.1"],
                answer_key=["Running to catch the bus, I felt my backpack fall open."],
                rubric_ref="rc.scr1", provenance={"copyright": "own_authored"})
    base.update(kw); return Item(**base)

def test_valid_scr_writing_passes():
    it = _scr_writing()
    r = qc_item(it)
    assert r["passed"], r["gates"]

def test_scr_writing_must_not_bind_stimulus():
    it = _scr_writing(stimulus_ref="ACC-W910-ARG-OPP-0007")
    r = qc_item(it)
    assert not r["passed"]
    assert r["first_failure"] == "scr_binding"

def test_scr_analysis_must_bind_stimulus():
    it = _scr_writing(id="ACC-W910-SCR-ANAL-0001", subskill_or_mode="scr_analysis",
                      rubric_ref="rc.scr3", stimulus_ref="")
    r = qc_item(it)
    assert not r["passed"]
    assert r["first_failure"] == "scr_binding"

def test_scr_wrong_rubric_fails():
    it = _scr_writing(rubric_ref="rc.staar")
    r = qc_item(it)
    assert not r["passed"]
    assert r["first_failure"] == "scr_rubric"

def test_scr_requires_model_answer():
    it = _scr_writing(answer_key=[])
    r = qc_item(it)
    assert not r["passed"]
    assert r["first_failure"] == "scr_schema"

def test_scr_em_dash_rejected():
    it = _scr_writing(stem="Rewrite the sentence — fix the modifier.")
    r = qc_item(it)
    assert not r["passed"]
