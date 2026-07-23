import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from incept_test_adapter import parse, classify_gate_failure

FIXTURE = "C:/tmp/incept_fulltest_11324.json"

def _output_json():
    return json.load(open(FIXTURE, encoding="utf-8"))["output_json"]

def test_parse_returns_items_and_warnings():
    items, warnings = parse(_output_json())
    assert len(items) == 8               # the fixture has 8 items
    assert isinstance(warnings, list)

def test_mc_correct_id_resolved_by_text_match():
    items, _ = parse(_output_json())
    mc = [it for it in items if it.qti_type == "choice"]
    assert mc, "expected at least one MC item"
    for it in mc:
        correct = [o for o in it.options if o.correct]
        assert len(correct) == 1                       # exactly one keyed correct option
        assert it.answer_key == [correct[0].id]        # answer_key matches the correct Option id
        assert all(o.rationale.strip() for o in it.options if not o.correct), "distractors need non-empty rationales"

def test_text_entry_becomes_scr_or_cr_with_model_answer():
    items, _ = parse(_output_json())
    constructed = [it for it in items if it.qti_type in ("text-entry", "extended-text")]
    assert constructed, "expected SCR/ECR items"
    for it in constructed:
        assert it.answer_key and it.answer_key[0].strip()   # model answer carried
        assert it.family in ("SCR", "CR")

def test_no_item_silently_dropped():
    oj = _output_json()
    items, warnings = parse(oj)
    assert len(items) == len(oj["items"])   # one Item per source item, none dropped

def test_classify_gate_failure_split():
    assert classify_gate_failure("distractor_integrity") == "fatal"
    assert classify_gate_failure("scr_binding") == "fatal"
    assert classify_gate_failure("rubric_config") == "fatal"
    assert classify_gate_failure("schema") == "fatal"
    assert classify_gate_failure("no_em_dash") == "fixable"
    # cross-pipeline mode excludes our-internal taxonomy gates
    assert classify_gate_failure("acc_tags") == "fatal"
    assert classify_gate_failure("acc_tags", cross_pipeline=True) == "excluded"
    # binding gates are our-bank-specific: fatal for our items, excluded cross-pipeline
    assert classify_gate_failure("cr_binding") == "fatal"
    assert classify_gate_failure("cr_binding", cross_pipeline=True) == "excluded"
    assert classify_gate_failure("scr_binding") == "fatal"
    assert classify_gate_failure("scr_binding", cross_pipeline=True) == "excluded"

def test_load_cached_output_json_roundtrips_to_adapter():
    from incept_test import load_cached_output_json
    oj = load_cached_output_json("C:/tmp/incept_fulltest_11324.json")
    assert "items" in oj and len(oj["items"]) == 8
    items, warnings = parse(oj)          # cached -> adapter must work end to end offline
    assert len(items) == 8

def test_judge_offline_is_deterministic_and_medianed():
    from bakeoff_judge import judge_item
    from item_contract import Item, Option
    it = Item(id="X", family="SR", grade="9-10", stem="Which is an arguable claim?",
              qti_type="choice", subskill_or_mode="evidence", acc_tags=["CCSS.W.9-10.1"],
              options=[Option("A","Schools should start later, because teens need sleep.",True,""),
                       Option("B","School starts at 8am.",False,"a fact")],
              answer_key=["A"])
    r1 = judge_item(it, n=3, live=False)
    r2 = judge_item(it, n=3, live=False)
    assert r1["median"] == r2["median"]
    assert len(r1["samples"]) == 3 and 0 <= r1["median"] <= 100 and r1["variance"] >= 0

def test_judge_has_rubric_version_and_prompt_is_source_neutral():
    import bakeoff_judge as bj
    from item_contract import Item, Option
    assert isinstance(bj.RUBRIC_VERSION, str) and bj.RUBRIC_VERSION
    it = Item(id="X", family="SR", grade="9-10", stem="Pick the arguable claim.", qti_type="choice",
              subskill_or_mode="evidence", acc_tags=["CCSS.W.9-10.1"],
              options=[Option("A","Schools should start later, because teens need sleep.",True,""),
                       Option("B","School starts at 8am.",False,"a fact")], answer_key=["A"])
    p = bj._judge_prompt(it, "STAAR English I (G9 argument)")
    # prompt must NOT leak which pipeline authored the item (fairness): no provenance words
    low = p.lower()
    assert "incept" not in low and "own_authored" not in low and "our pipeline" not in low
    assert "arguable claim" in low   # it embeds the actual item content

def test_judge_live_fails_loud_without_provider(monkeypatch):
    import bakeoff_judge as bj
    from item_contract import Item, Option
    # no provider configured -> live must raise, never silently heuristic-fallback
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("ANTHROPIC_PROVIDER", "direct")   # direct needs a key; none set -> must raise
    it = Item(id="X", family="SR", grade="9-10", stem="s", qti_type="choice",
              subskill_or_mode="evidence", acc_tags=["CCSS.W.9-10.1"],
              options=[Option("A","x",True,""),Option("B","y",False,"z")], answer_key=["A"])
    import pytest
    with pytest.raises(Exception):
        bj.judge_item(it, n=1, live=True)

def test_parse_score_extracts_number():
    from bakeoff_judge import _parse_score
    assert _parse_score('{"score": 82}') == 82.0
    assert _parse_score("Score: 74 / 100") == 74.0
    assert _parse_score("no number here") == 0.0

def test_bakeoff_run_offline_produces_ranked_scorecard():
    from bakeoff_g9 import run
    sc = run(live=False)
    assert set(sc["ours"]) >= {"fidelity", "fatal_gate_pass_rate", "fixable_failures", "excluded_failures", "judge_median_mean", "n_items"}
    assert set(sc["incept"]) >= {"fidelity", "fatal_gate_pass_rate", "fixable_failures", "excluded_failures", "judge_median_mean", "n_items"}
    assert sc["verdict"]["winner"] in ("ours", "incept", "tie")
    assert "primary_rank" in sc["verdict"]           # documents the fidelity+fatal+judge formula
    # Incept side must surface its known structural costs (uncited inline stimulus -> binding fails)
    assert sc["incept"]["fatal_gate_pass_rate"] <= 1.0
    # acc_tags gate excluded from cross-pipeline fatal metric for Incept
    assert "excluded_failures" in sc["incept"]
    # With acc_tags excluded, Incept fatal-pass should now be > 0 (not all items fail fatal)
    assert sc["incept"]["fatal_gate_pass_rate"] > 0
    # count-aware fidelity: Incept's under-count drops its fidelity below ours (which is 1.0)
    assert sc["incept"]["fidelity"] < sc["ours"]["fidelity"]
    # offline runs disclose the judge proxy mode
    assert "judge_mode" in sc["ours"]
    assert sc["ours"]["judge_mode"] == "offline_heuristic_proxy"
