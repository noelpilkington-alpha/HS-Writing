import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import incept_pool as ip

CACHE = "C:/tmp/incept_pool"
SUBSKILLS = ["evidence", "organization", "conventions", "sentence", "scr_writing", "argument"]

def _write_fixture_banks():
    """Small deterministic fixture banks, one per subskill, in the shapes Incept can emit."""
    os.makedirs(CACHE, exist_ok=True)
    def mc(stem, key):
        return {"stem": stem, "interaction_type": "multiple_choice",
                "options": [key, "a distractor about weather", "an off-topic fact", "a vague opinion"],
                "answer": key, "explanations": {key: "correct", "a distractor about weather": "off topic",
                "an off-topic fact": "off topic", "a vague opinion": "vague"},
                "metadata": {"dok": "2", "difficulty": "medium", "standards": ["CCSS.W.9-10.1"]}}
    # SR subskills -> flat items[] shape
    for sk in ["evidence", "organization", "conventions", "sentence"]:
        items = [mc(f"{sk} question {i}: which choice is correct?", f"the correct {sk} choice {i}") for i in range(3)]
        json.dump({"items": items}, open(f"{CACHE}/{sk}.json", "w", encoding="utf-8"))
    # scr_writing -> text_entry items[]
    json.dump({"items": [{"stem": "Rewrite the sentence to fix the modifier.", "interaction_type": "text_entry",
               "answer": "A clear rewrite that fixes the modifier.", "metadata": {"difficulty": "medium"}}]},
              open(f"{CACHE}/scr_writing.json", "w", encoding="utf-8"))
    # argument -> a forms[].items[] shape (a test-style artifact) with one long constructed prompt
    json.dump({"forms": [{"items": [{"stem": "Write an argumentative essay on whether schools should adopt a "
               "four-day week, citing the passage. " + ("Develop your claim fully. " * 20),
               "interaction_type": "text_entry", "answer": "A full argument essay model.",
               "metadata": {"difficulty": "hard"}, "stimulus": {"article": "some passage text"}}]}]},
              open(f"{CACHE}/argument.json", "w", encoding="utf-8"))

def test_normalize_handles_four_shapes():
    single = {"stem": "s", "interaction_type": "multiple_choice", "options": ["a"], "answer": "a"}
    flat = {"items": [single, single]}
    formed = {"forms": [{"items": [single]}, {"items": [single, single]}]}
    qshape = {"questions": [single, single]}
    assert len(ip._normalize_items(single)) == 1     # single question IS the item
    assert len(ip._normalize_items(flat)) == 2       # items[]
    assert len(ip._normalize_items(formed)) == 3     # forms[].items[]
    assert len(ip._normalize_items(qshape)) == 2     # questions[] alt bank key

def test_load_deepened_pool_stamps_subskills():
    _write_fixture_banks()
    pool = ip.load_deepened_incept_pool(CACHE)
    got = {it.subskill_or_mode for it in pool}
    assert {"evidence", "organization", "conventions", "sentence", "scr_writing", "argument"} <= got
    # every item is tagged incept + has the right family per subskill
    for it in pool:
        assert it.provenance.get("bakeoff_source") == "incept"
    fam = {it.subskill_or_mode: it.family for it in pool}
    assert fam["evidence"] == "SR" and fam["conventions"] == "SR"
    assert fam["scr_writing"] == "SCR" and fam["argument"] == "CR"

def test_load_deepened_pool_missing_bank_raises():
    os.makedirs(CACHE, exist_ok=True)
    # remove one bank and confirm a clear error names it
    p = f"{CACHE}/organization.json"
    _write_fixture_banks()
    os.remove(p)
    try:
        ip.load_deepened_incept_pool(CACHE)
        assert False, "expected a missing-bank error"
    except Exception as e:
        assert "organization" in str(e)
    _write_fixture_banks()  # restore for other tests

def test_generate_pool_dry_returns_six_bodies():
    from incept_client import InceptClient
    subs = ip.generate_pool(live=False, client=InceptClient())   # dry: no network
    assert set(subs) == set(ip.SUBSKILLS)   # one submission per subskill

def test_merged_pool_deepened_uses_six_subskill_banks():
    _write_fixture_banks()
    import importlib, bakeoff_hybrid
    importlib.reload(bakeoff_hybrid)
    default_pool = bakeoff_hybrid.merged_pool()               # unchanged 8-item incept behavior
    deep_pool = bakeoff_hybrid.merged_pool(deepened=True)     # uses the 6 fixture banks
    inc_default = [it for it in default_pool if it.provenance.get("bakeoff_source") == "incept"]
    inc_deep = [it for it in deep_pool if it.provenance.get("bakeoff_source") == "incept"]
    # deepened incept pool spans multiple subskills (default is mostly 'evidence')
    assert len({it.subskill_or_mode for it in inc_deep}) >= 4
    assert len(inc_deep) > len(inc_default)
    # ours side identical in both
    assert sum(1 for it in default_pool if it.provenance.get("bakeoff_source") == "ours") == \
           sum(1 for it in deep_pool if it.provenance.get("bakeoff_source") == "ours")
