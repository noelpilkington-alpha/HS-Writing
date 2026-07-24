import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bakeoff_hybrid import merged_pool, is_eligible
from item_contract import Item, Option

def test_merged_pool_tags_sources():
    pool = merged_pool()
    srcs = {it.provenance.get("bakeoff_source") for it in pool}
    assert srcs == {"ours", "incept"}
    assert sum(1 for it in pool if it.provenance.get("bakeoff_source") == "ours") == 21
    assert sum(1 for it in pool if it.provenance.get("bakeoff_source") == "incept") == 8

def test_is_eligible_drops_length_leak():
    # a length-leak MC item (correct option >1.25x longest distractor) must be INELIGIBLE
    leak = Item(id="LEAK", family="SR", grade="9-10", stem="Which is the best evidence?",
                qti_type="choice", subskill_or_mode="evidence", acc_tags=["ACC.W.SRC.1", "CCSS.W.9-10.1"],
                options=[Option("A","A study of 62 districts over four years found a measurable multi-point rise in "
                                    "attendance and test scores after the change was adopted district wide.",True,""),
                         Option("B","It was warm.",False,"off topic"),
                         Option("C","Buses run late.",False,"off topic"),
                         Option("D","People liked it.",False,"vague")],
                answer_key=["A"], provenance={"bakeoff_source": "incept"})
    assert is_eligible(leak) is False

def test_is_eligible_passes_clean_item():
    clean = Item(id="CLEAN", family="SR", grade="9-10", stem="Which statement is an arguable claim?",
                 qti_type="choice", subskill_or_mode="evidence", acc_tags=["ACC.W.SRC.1", "CCSS.W.9-10.1"],
                 options=[Option("A","Cities should build bike lanes, because safer routes get more people cycling.",True,""),
                          Option("B","Many cities added bike lanes over the past ten years now.",False,"a fact"),
                          Option("C","Bike lanes are honestly one of the best things ever, truly.",False,"opinion"),
                          Option("D","Some cities added bike lanes because they received federal grants.",False,"fact w/ because")],
                 answer_key=["A"], provenance={"bakeoff_source": "ours"})
    assert is_eligible(clean) is True

def test_select_hybrid_fills_blueprint_and_reports_sources():
    from bakeoff_hybrid import select_hybrid
    import render_model_tests as rmt
    items, srcmap = select_hybrid(live=False)
    # total picked == sum of blueprint counts (21 for G9)
    assert len(items) == sum(s["count"] for s in rmt.BLUEPRINTS["G9"])
    # every picked item is eligible (no fatal gate)
    from bakeoff_hybrid import is_eligible
    assert all(is_eligible(it) for it in items)
    # source map covers every section and records which source won each pick
    assert len(srcmap) == len(rmt.BLUEPRINTS["G9"])
    picks = [p for sec in srcmap for p in sec["picks"]]
    assert all(p["source"] in ("ours", "incept") for p in picks)

def test_select_hybrid_prefers_higher_judge_within_slot():
    # within a slot, a higher-judged eligible item outranks a lower one, source-blind.
    # offline heuristic judge: an item with rationalized distractors + balanced lengths scores higher than
    # a bare one. Confirm the evidence slot's first pick has a real (>=60) judge score.
    from bakeoff_hybrid import select_hybrid
    items, srcmap = select_hybrid(live=False)
    ev = next(sec for sec in srcmap if "evid" in sec["section"].lower())
    assert ev["picks"][0]["judge"] >= 60

def test_run_3way_scores_all_three_and_hybrid_fidelity_full():
    from bakeoff_hybrid import run_3way
    sc = run_3way(live=False)
    assert set(sc) >= {"ours", "incept", "hybrid", "verdict", "hybrid_source_map"}
    for side in ("ours", "incept", "hybrid"):
        assert "fidelity" in sc[side] and "fatal_gate_pass_rate" in sc[side] and "judge_median_mean" in sc[side]
    # hybrid is assembled to the full blueprint -> fidelity 1.0 and no fatal-gate failures
    assert sc["hybrid"]["fidelity"] == 1.0
    assert sc["hybrid"]["fatal_gate_pass_rate"] == 1.0
    # ranks present for all three; winner is one of them
    assert sc["verdict"]["winner"] in ("ours", "incept", "hybrid", "tie")
    assert "25" in sc["verdict"]["primary_rank"] and "50" in sc["verdict"]["primary_rank"]
    # source composition reported: how many slots incept won
    assert "incept_slot_wins" in sc["verdict"]

def test_hybrid_scored_source_aware_no_false_fatal():
    # every item selected for the hybrid was eligible under its own source rule (Incept items excluded
    # our-internal acc_tags + cr/scr_binding); when scored source-aware, none should be fatal
    from bakeoff_hybrid import run_3way
    sc = run_3way(live=False)
    assert sc["hybrid"]["fatal_gate_pass_rate"] == 1.0
