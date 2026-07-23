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
