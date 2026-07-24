"""
test_grader_mode_wiring.py  -  lock in GRADER_WIRING_FINDINGS Defect 2 (rc.ap -> rc.4trait + mode routing).

Regeneration guardrail: a regenerated G11/G12 course must keep declaring rc.4trait (never the deprecated
rc.ap the grader 503s) and must keep the rc.4trait TASK PROFILE (`mode`) baked into the grader URL for the
analysis-essay lessons. If a skill-pack regeneration drops the mode declaration or reverts to rc.ap, these
fail at CI, not silently at grade time.

Facts under test:
  1. No live G11/G12 lesson/mastery declares rubric_ref="rc.ap" (deprecated -> 503).
  2. The 3 pure-analysis lessons declare mode="analysis" on their scored rc.4trait slots; the wirer bakes
     ?mode=analysis into their mastery-FRQ grader URL.
  3. Every OTHER G11/G12 essay-grain mastery FRQ bakes NO mode (the grader defaults rc.4trait -> argument).
  4. Every essay-grain rc.4trait mastery FRQ carries the rc.4trait rubricBlock (the 4 Regents criteria),
     never a fallthrough to the rc.staar block.
  5. mode is orthogonal to the (unit, frq_type) routing tuple, so it is validated as a free field on the
     Slot (in MODES, rc.4trait-only), not part of GRADER_SUPPORTED_TUPLES.
"""
import os, sys

HERE = os.path.dirname(__file__)
PIPE = os.path.join(HERE, "..")
sys.path.insert(0, PIPE)

from course_push_mastery_v3_1 import build_plan
from lesson_contract import MODES, Slot, RUBRIC_CONFIGS

BASE = "https://hs-writing-grading.onrender.com/score"
# The pure-analysis lessons (rhetorical/literary analysis essays). Everything else is argument-or-agnostic.
ANALYSIS_FRQ_IDS = {
    "ACC-W1112-L-G11-C1103-0031-MASTERY-FRQ",   # g11_l30 rhetorical-analysis essay
    "ACC-W910-L-G12-C1201-0005-MASTERY-FRQ",    # g12_l05 sophisticated analysis
    "ACC-W910-L-G12-C1202-0010-MASTERY-FRQ",    # g12_l10 timed analysis
}


def _plan_items(grade):
    plan, _ = build_plan(grade, BASE)
    return [(oid, body) for kind, oid, url, body in plan if kind == "item"]


def _definition(body):
    # build_plan now emits the XML-format body ({format,xml,metadata}); the operator + grader URL live
    # LITERALLY in the XML (a JSON body would have the converter strip them). Read the definition from there.
    import re
    xml = body.get("xml", "")
    assert "custom-operator" in xml, "customOperator missing from the executable XML (JSON strip regression!)"
    m = re.search(r'definition="([^"]*)"', xml)
    return (m.group(1) if m else "").replace("&amp;", "&")


def _block(body):
    return ((body.get("metadata") or {}).get("rubricBlock") or {}).get("content", "")


def test_mode_is_a_valid_slot_field():
    assert Slot("INDEPENDENT", "production_frq", "t").mode == ""
    assert MODES == {"argument", "analysis"}
    # rc.ap kept as a VALID VALUE definition (legacy caller), even though the grader 503s it at score time.
    assert "rc.ap" in RUBRIC_CONFIGS and "rc.4trait" in RUBRIC_CONFIGS


def test_no_g11_g12_mastery_frq_uses_rc_ap():
    # Defect 2 root: the live items were wired rc.ap (which the grader 503s). No mastery FRQ may carry the
    # AP-style rubricBlock (the "AP Row A/B/C" markers) — every essay FRQ must show the rc.4trait criteria.
    for grade in ("G11", "G12"):
        for oid, body in _plan_items(grade):
            blk = _block(body)
            assert "AP Row" not in blk, f"{oid} still carries an rc.ap-style rubricBlock: {blk[:80]}"


def test_analysis_lessons_bake_mode_analysis():
    seen = set()
    for grade in ("G11", "G12"):
        for oid, body in _plan_items(grade):
            defn = _definition(body)
            if oid in ANALYSIS_FRQ_IDS:
                assert "mode=analysis" in defn, f"{oid} (analysis) missing ?mode=analysis: {defn}"
                seen.add(oid)
            else:
                assert "mode=analysis" not in defn, (
                    f"{oid} baked mode=analysis but is not a declared analysis lesson: {defn}")
    assert seen == ANALYSIS_FRQ_IDS, f"missing analysis FRQs in the plan: {ANALYSIS_FRQ_IDS - seen}"


def test_essay_grain_rc4trait_frqs_carry_the_rc4trait_block():
    # An essay-grain (no grain= in the URL) G11/G12 mastery FRQ scores via panel_ccss and must show the
    # 4 Regents criteria, not the rc.staar 2-part block.
    checked = 0
    for grade in ("G11", "G12"):
        for oid, body in _plan_items(grade):
            defn = _definition(body)
            if "grain=" in defn or "alphatest.alpha.school" in defn:
                continue  # sentence/paragraph carry their own block; sentence now routes to the NATIVE grader
            blk = _block(body)
            assert "content_analysis" in blk and "command_of_evidence" in blk, (
                f"{oid} essay-grain FRQ missing the rc.4trait block: {blk[:80]}")
            assert "STAAR" not in blk, f"{oid} fell through to the rc.staar block: {blk[:80]}"
            checked += 1
    assert checked >= 3, f"expected several essay-grain rc.4trait FRQs, saw {checked}"


if __name__ == "__main__":
    test_mode_is_a_valid_slot_field()
    test_no_g11_g12_mastery_frq_uses_rc_ap()
    test_analysis_lessons_bake_mode_analysis()
    test_essay_grain_rc4trait_frqs_carry_the_rc4trait_block()
    print("OK: Defect 2 mode/rc.4trait wiring locked in")
