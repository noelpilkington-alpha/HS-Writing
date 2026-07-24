# Hybrid Pipeline (best-item-wins) + 3-Way Bake-Off Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a G9 test form by picking the best gate-passing, highest-judged item per blueprint slot across ours + Incept-adapted pools (source-blind), then score ours/incept/hybrid through the same bake-off metric and report a 3-way verdict with hybrid source composition.

**Architecture:** One new module `pipeline/bakeoff_hybrid.py` that reuses everything already shipped: `bakeoff_g9._load_our_g9_items` / `_score_side` / `_fidelity` / `_judge_cached`, `incept_test_adapter.parse` + `classify_gate_failure`, `incept_test.load_cached_output_json`, `item_contract.qc_item`, `render_model_tests.BLUEPRINTS`. Merge both item pools (source-tagged in provenance), keep only fatal-gate passers, judge-rank per blueprint slot, select to the blueprint, then run the 3-way scorecard.

**Tech Stack:** Python 3 stdlib for the offline/default/tested path; the live judge path reuses `bakeoff_g9._judge_cached` (lazy `anthropic`). pytest. Offline fixture: `C:/tmp/incept_fulltest_11324.json`.

## Global Constraints

- Offline/default path + all tests: Python 3 stdlib only, network-free, deterministic.
- `anthropic` only on the live judge path (via `bakeoff_g9._judge_cached` -> `bakeoff_judge`), imported lazily there.
- No em dashes ( -  or -) in authored code/comments/docstrings (use `\u2014`/`\u2013` escapes when referencing).
- Never log or persist any API key.
- Judge stays SOURCE-BLIND: the source tag lives in `item.provenance["bakeoff_source"]`, NEVER in the judge prompt (`bakeoff_judge._judge_prompt` reads only stem/options/answer_key - do not change it).
- Verdict metric unchanged: `fidelity*25 + fatal_gate_pass*25 + judge_median_mean/100*50`; fixable + excluded reported separately.
- Gate eligibility uses the SAME cross_pipeline rule as the bake-off: ours scored `cross_pipeline=False`, Incept `cross_pipeline=True` (excludes our-internal acc_tags + cr/scr_binding).

---

## File Structure

- `pipeline/bakeoff_hybrid.py` - CREATE. Pool merge + tag, eligibility filter, per-slot judge-rank selector, hybrid assembly, 3-way scorecard + HTML, CLI.
- `pipeline/tests/test_bakeoff_hybrid.py` - CREATE. Offline-deterministic tests.

**Verified interfaces (reuse, do not modify):**
- `bakeoff_g9._load_our_g9_items() -> list[Item]` (full Items, blueprint-selected from Item_Bank_G9).
- `bakeoff_g9._score_side(items, cross_pipeline=False, live=False) -> dict` (keys: n_items, fatal_gate_pass_rate, fixable_failures, excluded_failures, judge_median_mean, judge_variance_mean, judge_mode, per_item).
- `bakeoff_g9._fidelity(items) -> float` (count-aware, 0-1, uses rmt.BLUEPRINTS["G9"]).
- `bakeoff_g9._judge_cached(item, live) -> {median, samples, variance}`.
- `incept_test_adapter.parse(output_json) -> (list[Item], list[str])`; `classify_gate_failure(gate_name, cross_pipeline=False) -> "fatal"|"fixable"|"excluded"`.
- `incept_test.load_cached_output_json(path="C:/tmp/incept_fulltest_11324.json") -> dict`.
- `item_contract.qc_item(item) -> {passed, gates:{name:{passed,detail}}, first_failure}`.
- `render_model_tests.BLUEPRINTS["G9"]` - list of section dicts: each has `family` ("CR"|"SCR"|"SR"), `count`, and `subskills` (SR/SCR) or `modes` (CR), plus `section`, `label`.
- `Item` fields: `.family`, `.subskill_or_mode`, `.provenance` (dict), `.id`.

**Blueprint slot -> item match rule (mirrors `_load_our_g9_items`):** an item matches a section iff `it.family == sec["family"]` AND `it.subskill_or_mode in (sec.get("subskills") or sec.get("modes") or [])`.

**Verified per-slot eligible counts (2026-07-23, offline gate filter):** ECR 2 (1 ours + 1 incept), SCR 3 (3 ours + 0 incept - our SCR items are `scr_writing`; Incept's lone SCR is `scr_analysis`, which does NOT match the `subskills=["scr_writing"]` slot), MC-evid 8 (4 ours + 4 incept - THE contest slot), MC-org 4 (ours only), MC-conv 5 (ours only), MC-sent 4 (ours only). So Incept can realistically win only MC-evid and possibly ECR; everywhere else is ours by availability. Every slot fills EXACTLY after filtering -> the hybrid is a full 21-item form, and `select_hybrid` FAILS LOUD if any slot is short (never pads).

---

## Task 1: Merged pool + eligibility filter

**Files:**
- Create: `pipeline/bakeoff_hybrid.py`
- Test: `pipeline/tests/test_bakeoff_hybrid.py`

**Interfaces:**
- Consumes: `bakeoff_g9._load_our_g9_items`, `incept_test.load_cached_output_json`, `incept_test_adapter.parse`, `item_contract.qc_item`, `incept_test_adapter.classify_gate_failure`.
- Produces:
  - `merged_pool() -> list[Item]` - ours (tagged `provenance["bakeoff_source"]="ours"`) + Incept-adapted (tagged `"incept"`).
  - `is_eligible(item) -> bool` - True iff no FATAL gate fails (cross_pipeline chosen by the item's source tag).

- [ ] **Step 1: Write the failing tests**

Create `pipeline/tests/test_bakeoff_hybrid.py`:

```python
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
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd "c:/Users/noelp/HS Writing/Alpha HS Writing Course 2026-27" && python -m pytest pipeline/tests/test_bakeoff_hybrid.py -v`
Expected: FAIL (`bakeoff_hybrid` not found). Use `py` if `python` missing.

- [ ] **Step 3: Implement merged_pool + is_eligible**

Create `pipeline/bakeoff_hybrid.py`:

```python
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
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest pipeline/tests/test_bakeoff_hybrid.py -v`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add pipeline/bakeoff_hybrid.py pipeline/tests/test_bakeoff_hybrid.py
git commit -m "feat(hybrid): merged source-tagged pool + fatal-gate eligibility filter"
```

---

## Task 2: Per-slot judge-rank selector + hybrid assembly

**Files:**
- Modify: `pipeline/bakeoff_hybrid.py`
- Test: `pipeline/tests/test_bakeoff_hybrid.py`

**Interfaces:**
- Consumes: `merged_pool`, `is_eligible` (Task 1); `bakeoff_g9._judge_cached`; `render_model_tests.BLUEPRINTS`.
- Produces:
  - `_matches(item, sec) -> bool` - blueprint-slot match (family + subskill/mode).
  - `select_hybrid(live=False) -> (list[Item], list[dict])` - the chosen items (blueprint order) + a per-slot source map `[{"section","picks":[{"id","source","judge"}...]}]`.

- [ ] **Step 1: Write the failing test**

Add to `pipeline/tests/test_bakeoff_hybrid.py`:

```python
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
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest pipeline/tests/test_bakeoff_hybrid.py::test_select_hybrid_fills_blueprint_and_reports_sources -v`
Expected: FAIL (`select_hybrid` not defined).

- [ ] **Step 3: Implement the selector**

Append to `pipeline/bakeoff_hybrid.py`:

```python
def _matches(item, sec) -> bool:
    if item.family != sec["family"]:
        return False
    keys = sec.get("subskills") or sec.get("modes") or []
    return item.subskill_or_mode in keys

def select_hybrid(live: bool = False):
    """For each blueprint slot: eligible items that match the slot, ranked by judge median (desc),
    source-blind; take the slot's count. Returns (picked_items_in_blueprint_order, per_slot_source_map)."""
    pool = [it for it in merged_pool() if is_eligible(it)]
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
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest pipeline/tests/test_bakeoff_hybrid.py -v`
Expected: PASS (5 passed).

- [ ] **Step 5: Commit**

```bash
git add pipeline/bakeoff_hybrid.py pipeline/tests/test_bakeoff_hybrid.py
git commit -m "feat(hybrid): per-slot judge-rank selector (source-blind, gate-floored) + source map"
```

---

## Task 3: 3-way scorecard + verdict + HTML

**Files:**
- Modify: `pipeline/bakeoff_hybrid.py`
- Test: `pipeline/tests/test_bakeoff_hybrid.py`

**Interfaces:**
- Consumes: `select_hybrid`, `merged_pool`; `bakeoff_g9._load_our_g9_items` / `_score_side` / `_fidelity`; `incept_test_adapter.parse` + `incept_test.load_cached_output_json`.
- Produces: `run_3way(live=False) -> dict` (keys `ours`, `incept`, `hybrid`, `verdict`, `hybrid_source_map`), writes `C:/tmp/bakeoff_3way_scorecard.json` + `C:/tmp/bakeoff_3way.html`. CLI `python pipeline/bakeoff_hybrid.py [--live]`.

- [ ] **Step 1: Write the failing test**

Add to `pipeline/tests/test_bakeoff_hybrid.py`:

```python
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
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest pipeline/tests/test_bakeoff_hybrid.py::test_run_3way_scores_all_three_and_hybrid_fidelity_full -v`
Expected: FAIL (`run_3way` not defined).

- [ ] **Step 3: Implement run_3way + HTML**

Append to `pipeline/bakeoff_hybrid.py`:

```python
def _rank(sc):
    return round(sc["fidelity"] * 25 + sc["fatal_gate_pass_rate"] * 25 + sc["judge_median_mean"] / 100 * 50, 2)

def run_3way(live: bool = False) -> dict:
    ours = bg._load_our_g9_items()
    incept, _w = parse(load_cached_output_json())
    hybrid_items, srcmap = select_hybrid(live=live)

    ours_sc = bg._score_side(ours, cross_pipeline=False, live=live); ours_sc["fidelity"] = bg._fidelity(ours)
    inc_sc = bg._score_side(incept, cross_pipeline=True, live=live); inc_sc["fidelity"] = bg._fidelity(incept)
    # hybrid: ours-side gate rule for our-authored picks and incept rule for incept picks is already baked into
    # eligibility; for scoring parity score the hybrid as a mixed form with cross_pipeline=False (its Incept
    # picks already passed the stricter-for-us gates during selection, so no acc_tags/binding exclusion needed).
    hyb_sc = bg._score_side(hybrid_items, cross_pipeline=False, live=live); hyb_sc["fidelity"] = bg._fidelity(hybrid_items)

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
    sc = run_3way(live=live)
    v = sc["verdict"]
    print(f"winner={v['winner']} ranks={v['ranks']}")
    print(f"incept won {v['incept_slot_wins']}/{v['total_slots']} hybrid slots")
    for side in ("ours", "incept", "hybrid"):
        s = sc[side]
        print(f"  {side}: fid={s['fidelity']} fatal={s['fatal_gate_pass_rate']} judge={s['judge_median_mean']} n={s['n_items']}")
    print("wrote C:/tmp/bakeoff_3way_scorecard.json + C:/tmp/bakeoff_3way.html")
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest pipeline/tests/test_bakeoff_hybrid.py -v`
Expected: PASS (6 passed).

- [ ] **Step 5: Run the offline 3-way + confirm composition**

Run: `python pipeline/bakeoff_hybrid.py`
Expected: prints winner + ranks + "incept won N/21 hybrid slots" + the three side lines; writes the JSON + HTML. Report the actual numbers (offline; the hybrid should show fidelity 1.0, fatal 1.0, and a judge score at least matching ours since it picks the highest-judged eligible item per slot).

- [ ] **Step 6: Commit**

```bash
git add pipeline/bakeoff_hybrid.py pipeline/tests/test_bakeoff_hybrid.py
git commit -m "feat(hybrid): 3-way scorecard (ours|incept|hybrid) + per-slot source map + HTML"
```

---

## Task 4: Verification sweep

**Files:** none (verification only)

- [ ] **Step 1: Hybrid tests pass**

Run: `python -m pytest pipeline/tests/test_bakeoff_hybrid.py -v`
Expected: 6 passed.

- [ ] **Step 2: Full suite (no regressions)**

Run: `python -m pytest pipeline/tests/ -q`
Expected: all pass (the module is additive).

- [ ] **Step 3: Offline determinism + anthropic-lazy**

Run:
```bash
python pipeline/bakeoff_hybrid.py >/dev/null && python -c "import json;d=json.load(open('C:/tmp/bakeoff_3way_scorecard.json'));print(d['verdict']['winner'],d['verdict']['ranks'])"
python pipeline/bakeoff_hybrid.py >/dev/null && python -c "import json;d=json.load(open('C:/tmp/bakeoff_3way_scorecard.json'));print(d['verdict']['winner'],d['verdict']['ranks'])"
python -c "import sys; sys.path.insert(0,'pipeline'); import bakeoff_hybrid; print('anthropic loaded:', 'anthropic' in sys.modules)"
```
Expected: identical verdict both runs; `anthropic loaded: False`.

- [ ] **Step 4: House-rule sweep**

Run: `grep -n " - \|-" pipeline/bakeoff_hybrid.py`
Expected: no matches.

- [ ] **Step 5: Commit (if any note added)**

```bash
git add -A && git commit -m "test(hybrid): verification sweep - 3-way offline deterministic, anthropic lazy"
```

---

## Self-Review

**Spec coverage:**
- Merged source-tagged pool + fatal-gate eligibility (Incept cross_pipeline=True, ours False) → Task 1. ✓
- Per-slot judge-rank, source-blind, gate-floored selection → Task 2. ✓
- 3-way scorecard on the same fidelity*25+fatal*25+judge*50 metric + per-slot source composition → Task 3. ✓
- Judge source-blind (tag in provenance, not prompt) → Task 1 (provenance tag) + reuses unmodified `_judge_prompt`. ✓
- Honest constraint (thin Incept pool, mostly ours, report slot wins) → Task 3 verdict `incept_slot_wins` + note. ✓
- Offline deterministic, anthropic lazy, no em dashes → Task 4. ✓

**Deferred (per spec non-goals):** deeper Incept pool; G10-12; production adoption; em-dash auto-repair; field test.

**Placeholder scan:** none.

**Type consistency:** `merged_pool()->list[Item]`, `is_eligible(item)->bool`, `_matches(item,sec)->bool`, `select_hybrid(live)->(list,list)`, `run_3way(live)->dict` consistent across tasks; reused bakeoff_g9 helpers match their verified signatures.
