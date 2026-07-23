"""
bakeoff_hybrid.py  -  build a G9 test from the best gate-passing, highest-judged item per blueprint slot
across BOTH pipelines (ours + Incept-adapted), source-blind, then score ours/incept/hybrid on the same
bake-off metric. Reuses the shipped adapter, gates, judge, and scorer; adds no new judge or gate.

Honest scope: ranks TEST-ARTIFACT quality, not student outcomes. The Incept pool is 8 items from one cached
test (mostly 'evidence'), so the hybrid is mostly ours + Incept wins only the few slots it has eligible
items for; the 3-way scorecard reports per-slot source composition.

RESULT DEPENDS ON THE JUDGE MODE (read before quoting a headline):
- OFFLINE (default `python bakeoff_hybrid.py`): the deterministic heuristic proxy penalizes Incept's
  em-dashes, so Incept wins 0/21 slots, the hybrid TIES ours (96.45), and winner=ours.
- LIVE (`--live`, neutral Claude judge): Incept's items judge higher, so it wins ~4 slots (ECR + MC-evidence)
  and the HYBRID WINS (e.g. 81.05 > ours 79.4 > incept 65.57). The "hybrid wins" headline is a LIVE result;
  the offline default does NOT reproduce it (by design - offline is a reproducible proxy, not the real judge).
"""
from __future__ import annotations
import os, sys, json, html, copy
sys.path.insert(0, os.path.dirname(__file__))
from item_contract import qc_item
from incept_test_adapter import parse, classify_gate_failure
from incept_test import load_cached_output_json
import bakeoff_g9 as bg
import render_model_tests as rmt
import incept_pool

def merged_pool(deepened=False):
    """Ours (source=ours) + Incept (source=incept), each tagged in provenance (NOT in judge input).
    deepened=True pulls the 6-subskill deepened Incept pool; default pulls the single cached test (8 items)."""
    pool = []
    for it in bg._load_our_g9_items():
        it = copy.copy(it); it.provenance = dict(it.provenance or {}); it.provenance["bakeoff_source"] = "ours"
        pool.append(it)
    if deepened:
        inc = incept_pool.load_deepened_incept_pool()
        for it in inc:
            it = copy.copy(it); it.provenance = dict(it.provenance or {}); it.provenance["bakeoff_source"] = "incept"
            pool.append(it)
    else:
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

def _matches(item, sec) -> bool:
    if item.family != sec["family"]:
        return False
    keys = sec.get("subskills") or sec.get("modes") or []
    return item.subskill_or_mode in keys

def select_hybrid(live: bool = False, deepened: bool = False):
    """For each blueprint slot: eligible items that match the slot, ranked by judge median (desc),
    source-blind; take the slot's count. Returns (picked_items_in_blueprint_order, per_slot_source_map)."""
    pool = [it for it in merged_pool(deepened=deepened) if is_eligible(it)]
    # judge each eligible item ONCE (cache dedupes live calls); attach the score
    scored = {}
    for it in pool:
        scored[id(it)] = bg._judge_cached(it, live)["median"]
    picked, srcmap, used = [], [], set()
    for sec in rmt.BLUEPRINTS["G9"]:
        cands = [it for it in pool if _matches(it, sec) and id(it) not in used]
        # rank by judge desc, then id for determinism
        cands.sort(key=lambda it: (-scored[id(it)], it.id))
        take = cands[:sec["count"]]
        if len(take) < sec["count"]:
            # FAIL LOUD: never assemble a short/invalid form by padding. If a slot cannot be filled from
            # eligible items, that is a real finding (pool too thin after gate-filtering), not something to
            # paper over. Verified 2026-07-23: every G9 slot fills exactly (SCR 3/3, org 4/4, conv 5/5,
            # sent 4/4; MC-evid 8 eligible for 4; ECR 2 for 1) - so this raises only if the pool shrinks.
            raise ValueError(f"hybrid slot '{sec['section']}' short: {len(take)}/{sec['count']} eligible items")
        for it in take:
            used.add(id(it))
        picked += take
        srcmap.append({"section": sec["section"], "count": sec["count"],
                       "picks": [{"id": it.id, "source": it.provenance.get("bakeoff_source"),
                                  "judge": scored[id(it)]} for it in take]})
    return picked, srcmap

def _score_side_mixed(items, live=False):
    """Per-item source-aware scorer: Incept-origin items use cross_pipeline=True (excludes our-internal
    acc_tags + cr/scr_binding), ours use cross_pipeline=False. Reuses the shared gate classification + judge."""
    fatal_ok = 0
    fixable_failures = 0
    excluded_failures = 0
    per_item = []
    judges = []
    variances = []
    for it in items:
        r = qc_item(it)
        xp = (it.provenance.get("bakeoff_source") == "incept")
        fatal = []
        fixable = []
        excluded = []
        if not r["passed"]:
            for gname, g in r["gates"].items():
                if not g["passed"]:
                    cls = classify_gate_failure(gname, cross_pipeline=xp)
                    if cls == "fatal":
                        fatal.append(gname)
                    elif cls == "fixable":
                        fixable.append(gname)
                    else:  # "excluded"
                        excluded.append(gname)
        if not fatal:
            fatal_ok += 1
        fixable_failures += len(fixable)
        excluded_failures += len(excluded)
        j = bg._judge_cached(it, live)
        judges.append(j["median"])
        variances.append(j["variance"])
        per_item.append({"id": it.id, "family": it.family, "fatal": fatal, "fixable": fixable,
                         "excluded": excluded, "judge_median": j["median"], "judge_variance": j["variance"]})
    n = len(items) or 1
    return {"n_items": len(items), "fatal_gate_pass_rate": round(fatal_ok / n, 3),
            "fixable_failures": fixable_failures, "excluded_failures": excluded_failures,
            "judge_median_mean": round(sum(judges) / n, 1),
            "judge_variance_mean": round(sum(variances) / n, 3),
            "judge_mode": "live_llm_median" if live else "offline_heuristic_proxy",
            "per_item": per_item}

def _rank(sc):
    return round(sc["fidelity"] * 25 + sc["fatal_gate_pass_rate"] * 25 + sc["judge_median_mean"] / 100 * 50, 2)

def run_3way(live: bool = False, deepened: bool = False) -> dict:
    ours = bg._load_our_g9_items()
    if deepened:
        incept = incept_pool.load_deepened_incept_pool()
    else:
        incept, _w = parse(load_cached_output_json())
    hybrid_items, srcmap = select_hybrid(live=live, deepened=deepened)

    ours_sc = bg._score_side(ours, cross_pipeline=False, live=live); ours_sc["fidelity"] = bg._fidelity(ours)
    inc_sc = bg._score_side(incept, cross_pipeline=True, live=live); inc_sc["fidelity"] = bg._fidelity(incept)
    # hybrid: score each item under its own source rule (Incept-origin uses cross_pipeline=True to exclude
    # our-internal acc_tags + cr/scr_binding; ours uses cross_pipeline=False). This matches the per-item
    # eligibility rule and prevents false-fatal failures on Incept picks that were selected as eligible.
    hyb_sc = _score_side_mixed(hybrid_items, live=live); hyb_sc["fidelity"] = bg._fidelity(hybrid_items)

    ranks = {"ours": _rank(ours_sc), "incept": _rank(inc_sc), "hybrid": _rank(hyb_sc)}
    winner = max(ranks, key=ranks.get)
    incept_slot_wins = sum(1 for sec in srcmap for p in sec["picks"] if p["source"] == "incept")
    total_slots = sum(len(sec["picks"]) for sec in srcmap)
    verdict = {"winner": winner, "ranks": ranks,
               "primary_rank": "fidelity*25 + fatal_gate_pass*25 + judge_median_mean/100*50 "
                               "(fixable + excluded reported separately, not in rank)",
               "incept_slot_wins": incept_slot_wins, "total_slots": total_slots,
               "note": "hybrid = best gate-passing, highest-judged item per slot, source-blind; Incept pool is "
                       "8 items (mostly evidence) so most slots are ours by availability, not preference"}
    sc = {"ours": ours_sc, "incept": inc_sc, "hybrid": hyb_sc, "verdict": verdict, "hybrid_source_map": srcmap}
    with open("C:/tmp/bakeoff_3way_scorecard.json", "w", encoding="utf-8") as fh:
        json.dump(sc, fh, indent=1)
    _write_html(sc)
    return sc

def _write_html(sc):
    def esc(s): return html.escape(str(s))
    v = sc["verdict"]
    rows = []
    for side in ("ours", "incept", "hybrid"):
        s = sc[side]
        rows.append(f"<tr><td>{side}</td><td>{v['ranks'][side]}</td><td>{s['fidelity']}</td>"
                    f"<td>{s['fatal_gate_pass_rate']}</td><td>{s['judge_median_mean']}</td>"
                    f"<td>{s.get('judge_variance_mean')}</td><td>{s['n_items']}</td></tr>")
    slot_rows = "".join(
        f"<tr><td>{esc(sec['section'])}</td><td>"
        + ", ".join(f"{esc(p['source'])}:{esc(p['id'])} ({esc(p['judge'])})" for p in sec["picks"])
        + "</td></tr>" for sec in sc["hybrid_source_map"])
    doc = (f"<!DOCTYPE html><html><head><meta charset='UTF-8'><title>G9 3-Way Bake-Off</title></head><body>"
           f"<h1>G9 3-Way Bake-Off: winner = {esc(v['winner'])}</h1>"
           f"<p>{esc(v['primary_rank'])}</p>"
           f"<p>Incept won {esc(v['incept_slot_wins'])} of {esc(v['total_slots'])} hybrid slots. {esc(v['note'])}</p>"
           f"<table border=1 cellpadding=6><tr><th>side</th><th>rank</th><th>fidelity</th><th>fatal pass</th>"
           f"<th>judge</th><th>judge var</th><th>items</th></tr>{''.join(rows)}</table>"
           f"<h2>Hybrid per-slot source map</h2>"
           f"<table border=1 cellpadding=6><tr><th>slot</th><th>picks (source:id (judge))</th></tr>{slot_rows}</table>"
           f"</body></html>")
    with open("C:/tmp/bakeoff_3way.html", "w", encoding="utf-8") as fh:
        fh.write(doc)

if __name__ == "__main__":
    live = "--live" in sys.argv
    deep = "--deepened" in sys.argv
    sc = run_3way(live=live, deepened=deep)
    v = sc["verdict"]
    print(f"winner={v['winner']} ranks={v['ranks']}")
    print(f"incept won {v['incept_slot_wins']}/{v['total_slots']} hybrid slots")
    for side in ("ours", "incept", "hybrid"):
        s = sc[side]
        print(f"  {side}: fid={s['fidelity']} fatal={s['fatal_gate_pass_rate']} judge={s['judge_median_mean']} n={s['n_items']}")
    print("wrote C:/tmp/bakeoff_3way_scorecard.json + C:/tmp/bakeoff_3way.html")
