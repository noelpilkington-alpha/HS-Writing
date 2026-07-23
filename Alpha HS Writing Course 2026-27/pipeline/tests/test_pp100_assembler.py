"""
Tests for the assembler's PP100 assessment-bank support (Phase A4).

course_assemble_v3_1.build_plan(grade, base_url) must:
  - for a SINGLE-form lesson (today), emit the PP100 resource pointing at the single mastery test
    (`type: qti`, url .../assessment-tests/<lesson>-MASTERY) and the CR linking it, byte-identical to today
    (prod-safe: bank of 1 == today);
  - for a MULTI-form lesson, emit ONE assessment-bank Resource (`type: assessment-bank`,
    metadata.resources = [the N form-test ids]) plus the PP100 CR pointing at the BANK resource (not a single
    test), and NOT link the individual form-tests directly (the documented "3 links per topic" defect).

Single-form assertions run against real G9 (all single-form today). Multi-form runs with an injected 2-form
entry, patching the assembler's authored-map binding.
"""
import os
import sys

HERE = os.path.dirname(__file__)
PIPE = os.path.join(HERE, "..")
sys.path.insert(0, PIPE)

import course_assemble_v3_1 as CA
import mastery_forms as MF


def _resources(plan):
    return {oid: body for k, oid, url, body in plan if k == "resource"}


def _crs(plan):
    return {oid: body for k, oid, url, body in plan if k == "component-resource"}


def test_single_form_pp100_points_at_single_test():
    plan, lessons, units = CA.build_plan("G9", "https://base.example")
    res = _resources(plan)
    lid = "ACC-W910-L-G9-C901-0001"
    pp = res.get(f"res-{lid}-pp100")
    assert pp is not None, "single-form PP100 resource missing"
    md = pp["resource"]["metadata"]
    assert md["type"] == "qti"
    assert md["url"].endswith(f"/assessment-tests/{lid}-MASTERY")
    # NO assessment-bank resource for a single-form lesson
    assert f"{MF.bank_resource_id(lid)}" not in res


def test_single_form_cr_points_at_pp100_resource():
    plan, *_ = CA.build_plan("G9", "https://base.example")
    crs = _crs(plan)
    lid = "ACC-W910-L-G9-C901-0001"
    cr = crs.get(f"cr-{lid}-pp100")
    assert cr is not None
    assert cr["componentResource"]["resource"]["sourcedId"] == f"res-{lid}-pp100"
    assert cr["componentResource"]["metadata"]["lessonType"] == "powerpath-100"


def test_multiform_emits_assessment_bank(monkeypatch):
    """Inject a 2-form bank for L01; assert the assembler emits an assessment-bank resource listing both
    form-test ids and points the PP100 CR at that bank."""
    lid = "ACC-W910-L-G9-C901-0001"
    injected = {
        "unit": "sentence", "rubric_ref": "rc.staar", "frq_type": "writing",
        "forms": [
            {"source": "ACC-W910-FRAME-SOCIALMEDIAAGE", "prompt_html": "<p>A</p>"},
            {"source": "ACC-W910-FRAME-PHONEBAN", "prompt_html": "<p>B</p>"},
        ],
    }
    real = CA._authored

    def fake(grade):
        d = dict(real(grade))
        if grade == "G9":
            d[lid] = injected
        return d

    monkeypatch.setattr(CA, "_authored", fake)

    plan, *_ = CA.build_plan("G9", "https://base.example")
    res = _resources(plan)
    crs = _crs(plan)
    bank_id = MF.bank_resource_id(lid)
    # bank resource exists, correct type, lists BOTH form-test ids
    bank = res.get(bank_id)
    assert bank is not None, "assessment-bank resource missing for multi-form lesson"
    md = bank["resource"]["metadata"]
    assert md["type"] == "assessment-bank"
    assert md["resources"] == [f"{lid}-MASTERY-f1", f"{lid}-MASTERY-f2"]
    # the PP100 CR now points at the BANK, not a single test resource
    cr = crs[f"cr-{lid}-pp100"]
    assert cr["componentResource"]["resource"]["sourcedId"] == bank_id
    # individual form-tests are NOT linked as their own CRs (only the bank is linked)
    assert f"cr-{lid}-MASTERY-f1" not in crs
    assert f"cr-{lid}-MASTERY-f2" not in crs


def test_other_lessons_unaffected_by_one_multiform(monkeypatch):
    """Injecting a multi-form bank on ONE lesson must not change any other lesson's single-form PP100."""
    lid = "ACC-W910-L-G9-C901-0001"
    injected = {"unit": "sentence", "rubric_ref": "rc.staar", "frq_type": "writing",
                "forms": [{"source": "ACC-W910-FRAME-SOCIALMEDIAAGE", "prompt_html": "<p>A</p>"},
                          {"source": "ACC-W910-FRAME-PHONEBAN", "prompt_html": "<p>B</p>"}]}
    real = CA._authored
    monkeypatch.setattr(CA, "_authored", lambda g: ({**real(g), lid: injected} if g == "G9" else real(g)))
    plan, *_ = CA.build_plan("G9", "https://base.example")
    res = _resources(plan)
    other = "ACC-W910-L-G9-C901-0003"
    pp = res[f"res-{other}-pp100"]
    assert pp["resource"]["metadata"]["type"] == "qti"
    assert pp["resource"]["metadata"]["url"].endswith(f"/assessment-tests/{other}-MASTERY")
