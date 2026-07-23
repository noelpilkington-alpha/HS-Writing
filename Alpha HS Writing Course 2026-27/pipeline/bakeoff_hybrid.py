"""
bakeoff_hybrid.py  -  build a G9 test from the best gate-passing, highest-judged item per blueprint slot
across BOTH pipelines (ours + Incept-adapted), source-blind, then score ours/incept/hybrid on the same
bake-off metric. Reuses the shipped adapter, gates, judge, and scorer; adds no new judge or gate.

Honest scope: ranks TEST-ARTIFACT quality, not student outcomes. The Incept pool is 8 items from one cached
test (mostly 'evidence'), so the hybrid is mostly ours + Incept wins only the few slots it has eligible
items for; the 3-way scorecard reports per-slot source composition.
"""
from __future__ import annotations
import os, sys, json, html, copy
sys.path.insert(0, os.path.dirname(__file__))
from item_contract import qc_item
from incept_test_adapter import parse, classify_gate_failure
from incept_test import load_cached_output_json
import bakeoff_g9 as bg
import render_model_tests as rmt

def merged_pool():
    """Ours (source=ours) + Incept-adapted (source=incept), each tagged in provenance (NOT in judge input)."""
    pool = []
    for it in bg._load_our_g9_items():
        it = copy.copy(it); it.provenance = dict(it.provenance or {}); it.provenance["bakeoff_source"] = "ours"
        pool.append(it)
    inc, _warnings = parse(load_cached_output_json())
    for it in inc:
        it = copy.copy(it); it.provenance = dict(it.provenance or {}); it.provenance["bakeoff_source"] = "incept"
        pool.append(it)
    return pool

def is_eligible(item) -> bool:
    """Eligible iff NO fatal gate fails. Incept items use cross_pipeline=True (excludes our-internal
    acc_tags + cr/scr_binding, consistent with the bake-off); ours use cross_pipeline=False."""
    xp = (item.provenance.get("bakeoff_source") == "incept")
    r = qc_item(item)
    if r["passed"]:
        return True
    for gname, g in r["gates"].items():
        if not g["passed"] and classify_gate_failure(gname, cross_pipeline=xp) == "fatal":
            return False
    return True
