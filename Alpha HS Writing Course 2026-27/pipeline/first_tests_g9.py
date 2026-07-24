"""
first_tests_g9.py  -  assemble the first shippable G9 hybrid test forms.

Clean the deepened hybrid pool (Incept items through incept_cleanup; ours pass through), then apply the
STRICT shippable-eligibility filter (full item_contract.qc_item, all real fatal gates, NO cross_pipeline
exclusion) so only fully-gate-clean items are selection candidates, select disjoint forms over that pool,
re-assert every selected item passes full qc_item, and write review artifacts + a cleanup ledger + the
strict gate-drop list. This is a STRICTER bar than the bake-off's is_eligible (which excludes our-internal
acc_tags + cr/scr_binding for a fair source-blind comparison); a real student-facing form must clear the
full contract. No grader-wiring, no push - delivery is a separate step on approval.
"""
from __future__ import annotations
import os, sys, json, html
sys.path.insert(0, os.path.dirname(__file__))
from item_contract import qc_item
from incept_cleanup import clean_item
import bakeoff_hybrid as bh

OUT_DIR = "C:/tmp/first_tests_g9"

def _cleaned_pool(live: bool):
    """merged deepened pool -> clean each item -> STRICT full-gate filter -> (ship_eligible_pool, ledger, gate_dropped).

    SHIPPABLE bar (differs from the bake-off's is_eligible): an item is ship-eligible iff it passes the FULL
    item_contract.qc_item (all real fatal gates, NO cross_pipeline exclusion). The bake-off deliberately excludes
    our-internal acc_tags + cr/scr_binding for a fair source-blind COMPARISON; that is the wrong bar for a real
    student-facing test, so we do NOT use it here. Only fully-gate-clean items become selection candidates.
    Items dropped by the strict gate are recorded in gate_dropped so the drop is visible, not silent.
    Ledger: per Incept item kept/dropped by the cleanup pass."""
    raw = bh.merged_pool(deepened=True)
    cleaned, ledger = [], []
    for it in raw:
        out, actions = clean_item(it)
        if (it.provenance or {}).get("bakeoff_source") == "incept":
            ledger.append({"id": it.id, "kept": out is not None, "actions": actions})
        if out is not None:
            cleaned.append(out)
    ship, gate_dropped = [], []
    for it in cleaned:
        r = qc_item(it)
        if r["passed"]:
            ship.append(it)
        else:
            gate_dropped.append({"id": it.id, "source": (it.provenance or {}).get("bakeoff_source"),
                                 "first_failure": r["first_failure"],
                                 "detail": r["gates"][r["first_failure"]]["detail"] if r["first_failure"] else ""})
    return ship, ledger, gate_dropped

def _select_disjoint(cleaned, n_forms, live):
    """n disjoint forms via repeated select_hybrid over the cleaned pool, removing picked ids each round."""
    forms = []
    remaining = list(cleaned)
    for _ in range(n_forms):
        picked, srcmap = bh.select_hybrid(live=live, pool=remaining)
        forms.append({"items": picked, "source_map": srcmap})
        used = {it.id for it in picked}
        remaining = [it for it in remaining if it.id not in used]
    return forms

def build(n_forms: int = 2, live: bool = False) -> dict:
    cleaned, ledger, gate_dropped = _cleaned_pool(live)
    forms = _select_disjoint(cleaned, n_forms, live)
    # STRICT shippable re-check: every selected item must pass the FULL qc_item (all real fatal gates, no
    # cross_pipeline exclusion). The pool was already filtered to full-gate-clean items in _cleaned_pool, so
    # this is a fail-loud guarantee that nothing gate-failing reaches a real form.
    for f in forms:
        for it in f["items"]:
            r = qc_item(it)
            assert r["passed"], (f"gate-failing item {it.id} on shippable form "
                                 f"(first_failure={r['first_failure']})")
    res = {"forms": forms, "cleanup_ledger": ledger, "gate_dropped": gate_dropped,
           "kept_incept": sum(1 for e in ledger if e["kept"]),
           "dropped_incept": sum(1 for e in ledger if not e["kept"])}
    os.makedirs(OUT_DIR, exist_ok=True)
    _write_json(res)
    _write_html(res)
    return res

def _write_json(res):
    def item_d(it):
        return {"id": it.id, "family": it.family, "subskill": it.subskill_or_mode,
                "source": (it.provenance or {}).get("bakeoff_source"), "stem": it.stem,
                "options": [{"id": o.id, "text": o.text, "correct": o.correct} for o in it.options],
                "answer_key": it.answer_key, "provenance": it.provenance}
    out = {"forms": [{"items": [item_d(i) for i in f["items"]], "source_map": f["source_map"]} for f in res["forms"]],
           "cleanup_ledger": res["cleanup_ledger"], "gate_dropped": res["gate_dropped"],
           "kept_incept": res["kept_incept"], "dropped_incept": res["dropped_incept"]}
    with open(os.path.join(OUT_DIR, "forms.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)

def _write_html(res):
    def esc(s): return html.escape(str(s))
    parts = [f"<h1>First G9 Hybrid Tests</h1><p>{len(res['forms'])} disjoint forms. "
             f"Incept items kept {res['kept_incept']}, dropped {res['dropped_incept']} (see ledger).</p>"]
    for fi, f in enumerate(res["forms"], 1):
        parts.append(f"<h2>Form {fi}</h2><ol>")
        for it in f["items"]:
            src = (it.provenance or {}).get("bakeoff_source")
            parts.append(f"<li><b>[{esc(src)}/{esc(it.subskill_or_mode)}]</b> {esc(it.stem)}</li>")
        parts.append("</ol>")
    parts.append("<h2>Cleanup ledger (Incept items)</h2><table border=1 cellpadding=5>"
                 "<tr><th>id</th><th>kept</th><th>actions</th></tr>")
    for e in res["cleanup_ledger"]:
        parts.append(f"<tr><td>{esc(e['id'])}</td><td>{'kept' if e['kept'] else 'DROPPED'}</td>"
                     f"<td>{esc('; '.join(e['actions']))}</td></tr>")
    parts.append("</table>")
    gd = res.get("gate_dropped") or []
    parts.append(f"<h2>Strict gate drops ({len(gd)} items dropped by full qc_item before selection)</h2>"
                 "<p>Ship-eligibility requires passing the FULL item contract (real fatal gates, no bake-off "
                 "exclusion). Items failing here never reach a form.</p>"
                 "<table border=1 cellpadding=5><tr><th>id</th><th>source</th><th>first failure</th><th>detail</th></tr>")
    for e in gd:
        parts.append(f"<tr><td>{esc(e['id'])}</td><td>{esc(e['source'])}</td>"
                     f"<td>{esc(e['first_failure'])}</td><td>{esc(e['detail'])}</td></tr>")
    parts.append("</table>")
    with open(os.path.join(OUT_DIR, "first_tests_g9.html"), "w", encoding="utf-8") as fh:
        fh.write("<!DOCTYPE html><html><head><meta charset=UTF-8><title>First G9 Hybrid Tests</title></head>"
                 "<body style='font-family:sans-serif;max-width:900px;margin:0 auto;padding:24px'>"
                 + "".join(parts) + "</body></html>")

if __name__ == "__main__":
    live = "--live" in sys.argv
    # Pool constraint (2026-07-24): 3 SCR items total, 3 required per form -> max 1 form.
    # Building 2+ forms will fail-loud at SCR slot. Extend when the pool deepens.
    res = build(n_forms=1, live=live)
    print(f"built {len(res['forms'])} forms; incept cleanup kept {res['kept_incept']} dropped {res['dropped_incept']}; "
          f"strict-gate dropped {len(res['gate_dropped'])} before selection")
    from collections import Counter
    comp = Counter((it.provenance or {}).get("bakeoff_source") for f in res["forms"] for it in f["items"])
    print("form source composition:", dict(comp))
    print("wrote", OUT_DIR + "/forms.json + first_tests_g9.html")
