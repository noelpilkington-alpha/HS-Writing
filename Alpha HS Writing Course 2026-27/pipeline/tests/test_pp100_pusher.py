"""
Tests for the PP100 pusher's N-form plan (Phase A3).

course_push_mastery_v3_1.build_plan(grade, grader_url) must:
  - for a single-form lesson (today's shape), emit EXACTLY one FRQ item id `<lesson>-MASTERY-FRQ` + one test id
    `<lesson>-MASTERY` (byte-for-byte prod-safe; nothing regresses);
  - for a multi-form lesson, emit N FRQ items `<lesson>-MASTERY-FRQ-f{k}` + N tests `<lesson>-MASTERY-f{k}`,
    one per validated equivalent form, each test referencing its own FRQ item.

We drive it against a REAL grade (G9) whose mastery banks are currently single-form, so the prod-safe id shape
is asserted directly. Multi-form id derivation is asserted via mastery_forms (unit-level), since authoring
multi-form banks is Phase B.
"""
import os
import sys

HERE = os.path.dirname(__file__)
PIPE = os.path.join(HERE, "..")
sys.path.insert(0, PIPE)

import course_push_mastery_v3_1 as PM
import mastery_forms as MF


def test_single_form_lesson_keeps_legacy_ids():
    """A still-single-form lesson (C901-0003) must yield the CURRENT live ids and nothing else.
    (C901-0001 is now a real 30-form bank, so it is no longer the single-form fixture.)"""
    plan, skipped = PM.build_plan("G9", "https://grader.example/score")
    items = [oid for k, oid, *_ in plan if k == "item"]
    tests = [oid for k, oid, *_ in plan if k == "test"]
    # a known single-form lesson's ids are the legacy (unsuffixed) ones
    assert "ACC-W910-L-G9-C901-0003-MASTERY-FRQ" in items
    assert "ACC-W910-L-G9-C901-0003-MASTERY" in tests
    # and NOT the suffixed form ids (bank of 1 uses legacy ids)
    assert "ACC-W910-L-G9-C901-0003-MASTERY-FRQ-f1" not in items
    # every test has a matching FRQ item
    for t in tests:
        assert t.replace("-MASTERY", "-MASTERY-FRQ") in items or (t + "-FRQ") in items


def test_plan_pairs_each_test_with_its_frq():
    """Structural invariant: #tests == #items, and each test references an existing item id."""
    plan, _ = PM.build_plan("G9", "https://grader.example/score")
    items = {oid for k, oid, *_ in plan if k == "item"}
    tests = [(oid, body) for k, oid, url, body in plan if k == "test"]
    assert len(items) == len(tests)
    for tid, body in tests:
        ref = body["qti-test-part"][0]["qti-assessment-section"][0]["qti-assessment-item-ref"][0]["identifier"]
        assert ref in items, f"test {tid} references unknown item {ref}"


def test_multiform_ids_derive_from_mastery_forms():
    """When a lesson DOES carry N>1 forms, the pusher must use the suffixed ids (asserted at the id-derivation
    layer, which the pusher calls)."""
    lid = "ACC-W910-L-G9-C901-0001"
    assert MF.form_frq_id(lid, 1, bank_size=3) == f"{lid}-MASTERY-FRQ-f1"
    assert MF.form_test_id(lid, 3, bank_size=3) == f"{lid}-MASTERY-f3"


def test_pusher_expands_a_multiform_entry(monkeypatch):
    """Force the multi-form path: inject a 2-form bank for L01 into the authored map and assert the pusher
    emits 2 suffixed FRQ items + 2 suffixed tests for that lesson, each test paired with its own FRQ, while
    every OTHER (single-form) lesson keeps its legacy ids untouched."""
    lid = "ACC-W910-L-G9-C901-0001"
    # a valid 2-form entry (grain/rubric constant; two distinct held-out sources)
    injected = {
        "unit": "sentence", "rubric_ref": "rc.staar", "frq_type": "writing",
        "forms": [
            {"source": "ACC-W910-FRAME-SOCIALMEDIAAGE", "prompt_html": "<p>Claim on social media age checks.</p>"},
            {"source": "ACC-W910-FRAME-PHONEBAN", "prompt_html": "<p>Claim on a school phone ban (held-out B).</p>"},
        ],
    }
    # the pusher binds _authored into its own namespace at import, so patch it THERE (the name it calls)
    real_authored = PM._authored

    def fake_authored(grade):
        d = dict(real_authored(grade))
        if grade == "G9":
            d[lid] = injected
        return d

    monkeypatch.setattr(PM, "_authored", fake_authored)

    plan, _ = PM.build_plan("G9", "https://grader.example/score")
    items = [oid for k, oid, *_ in plan if k == "item"]
    tests = [oid for k, oid, *_ in plan if k == "test"]
    # the injected lesson now has 2 suffixed forms, not the legacy id
    assert f"{lid}-MASTERY-FRQ-f1" in items
    assert f"{lid}-MASTERY-FRQ-f2" in items
    assert f"{lid}-MASTERY-f1" in tests
    assert f"{lid}-MASTERY-f2" in tests
    assert f"{lid}-MASTERY-FRQ" not in items, "multi-form lesson must NOT emit the legacy unsuffixed id"
    # a different, still-single-form lesson keeps its legacy id
    assert "ACC-W910-L-G9-C901-0003-MASTERY-FRQ" in items
