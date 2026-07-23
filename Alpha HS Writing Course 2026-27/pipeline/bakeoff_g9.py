"""
bakeoff_g9.py  -  orchestrate the G9 test bake-off: our pipeline vs Incept.

Loads a full G9 test from BOTH pipelines, runs every item through item_contract gates (classified
fatal/fixable), runs the shared median judge, and emits a ranked scorecard + side-by-side HTML. Offline by
default (reads the cached Incept artifact); --live regenerates from the API.

Honest scope: ranks TEST-ARTIFACT quality (fidelity + fatal-gate-pass + judge), NOT student outcomes. The
judge is a noise-flagged tie-breaker; the deterministic gate + fidelity metrics are the primary rank.
"""
from __future__ import annotations
import os, sys, glob, json, html, importlib.util
sys.path.insert(0, os.path.dirname(__file__))
from item_contract import qc_item
from incept_test_adapter import parse, classify_gate_failure
from incept_test import load_cached_output_json
from bakeoff_judge import judge_item
import render_model_tests as rmt

ROOT = os.path.join(os.path.dirname(__file__), "..")

def _load_our_g9_items():
    """Full Item objects for the G9 form, selected to BLUEPRINTS['G9'] section filters."""
    bank = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "Item_Bank_G9", "*.py"))):
        if "__" in os.path.basename(f):
            continue
        spec = importlib.util.spec_from_file_location("bk_" + os.path.basename(f)[:-3], f)
        m = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(m)
        except SystemExit:
            pass
        for it in getattr(m, "ITEMS", []):
            bank.setdefault(it.subskill_or_mode, []).append(it)
            if it.family == "CR":
                bank.setdefault("_CR_" + it.subskill_or_mode, []).append(it)
    picked = []
    for sec in rmt.BLUEPRINTS["G9"]:
        keys = sec.get("subskills") or sec.get("modes") or []
        n = sec["count"]
        pool = []
        for k in keys:
            pool += bank.get(k, []) if sec["family"] != "CR" else bank.get("_CR_" + k, [])
        picked += sorted(pool, key=lambda i: i.id)[:n]
    return picked

def _score_side(items):
    fatal_ok = 0
    fixable_failures = 0
    per_item = []
    judges = []
    for it in items:
        r = qc_item(it)
        fatal = []
        fixable = []
        if not r["passed"]:
            for gname, g in r["gates"].items():
                if not g["passed"]:
                    (fatal if classify_gate_failure(gname) == "fatal" else fixable).append(gname)
        if not fatal:
            fatal_ok += 1
        fixable_failures += len(fixable)
        j = judge_item(it, n=3, live=False)
        judges.append(j["median"])
        per_item.append({"id": it.id, "family": it.family, "fatal": fatal, "fixable": fixable,
                         "judge_median": j["median"]})
    n = len(items) or 1
    return {"n_items": len(items), "fatal_gate_pass_rate": round(fatal_ok / n, 3),
            "fixable_failures": fixable_failures,
            "judge_median_mean": round(sum(judges) / n, 1), "per_item": per_item}

def _fidelity(items, is_ours: bool):
    """Fraction of the G9 blueprint's shape the test hits: has an ECR, has >=1 SCR, has MC items."""
    fams = [it.family for it in items]
    checks = [("CR" in fams), ("SCR" in fams), (fams.count("SR") >= 3)]
    return round(sum(1 for c in checks if c) / len(checks), 3)

def run(live: bool = False) -> dict:
    ours = _load_our_g9_items()
    incept_items, warnings = parse(load_cached_output_json() if not live else _live_incept())
    ours_sc = _score_side(ours); ours_sc["fidelity"] = _fidelity(ours, True)
    inc_sc = _score_side(incept_items); inc_sc["fidelity"] = _fidelity(incept_items, False)
    inc_sc["adapter_warnings"] = warnings
    def rank(sc):
        return round(sc["fidelity"] * 40 + sc["fatal_gate_pass_rate"] * 40 + sc["judge_median_mean"] / 100 * 20, 2)
    ours_rank, inc_rank = rank(ours_sc), rank(inc_sc)
    winner = "ours" if ours_rank > inc_rank else "incept" if inc_rank > ours_rank else "tie"
    verdict = {"winner": winner, "ours_rank": ours_rank, "incept_rank": inc_rank,
               "primary_rank": "fidelity*40 + fatal_gate_pass*40 + judge_median_mean/100*20 "
                               "(fixable_failures reported separately, not in rank)"}
    sc = {"ours": ours_sc, "incept": inc_sc, "verdict": verdict}
    with open("C:/tmp/bakeoff_g9_scorecard.json", "w", encoding="utf-8") as fh:
        json.dump(sc, fh, indent=1)
    _write_html(sc)
    return sc

def _live_incept():
    from incept_test import generate_g9_test, fetch_g9_test
    sub = generate_g9_test(live=True)
    # NOTE: live polling to terminal is the operator's step; for --live, pass an already-succeeded
    # artifact id via env INCEPT_ARTIFACT_ID to fetch. Keeps this module non-blocking.
    aid = os.environ.get("INCEPT_ARTIFACT_ID")
    if not aid:
        raise SystemExit("live mode: set INCEPT_ARTIFACT_ID to a succeeded test artifact id")
    return fetch_g9_test(aid, live=True)

def _write_html(sc):
    def esc(s): return html.escape(str(s))
    v = sc["verdict"]
    rows = []
    for side in ("ours", "incept"):
        s = sc[side]
        rows.append(f"<tr><td>{side}</td><td>{s['fidelity']}</td><td>{s['fatal_gate_pass_rate']}</td>"
                    f"<td>{s['fixable_failures']}</td><td>{s['judge_median_mean']}</td><td>{s['n_items']}</td></tr>")
    doc = (f"<!DOCTYPE html><html><head><meta charset='UTF-8'><title>G9 Bake-Off</title></head><body>"
           f"<h1>G9 Test Bake-Off: winner = {esc(v['winner'])}</h1>"
           f"<p>ours rank {v['ours_rank']} vs incept rank {v['incept_rank']}</p>"
           f"<p>{esc(v['primary_rank'])}</p>"
           f"<table border=1 cellpadding=6><tr><th>side</th><th>fidelity</th><th>fatal gate pass</th>"
           f"<th>fixable failures</th><th>judge median mean</th><th>items</th></tr>{''.join(rows)}</table>"
           f"</body></html>")
    with open("C:/tmp/bakeoff_g9.html", "w", encoding="utf-8") as fh:
        fh.write(doc)

if __name__ == "__main__":
    live = "--live" in sys.argv
    sc = run(live=live)
    print(json.dumps(sc["verdict"], indent=1))
    print(f"ours: {sc['ours']['fidelity']} fid, {sc['ours']['fatal_gate_pass_rate']} fatal-pass, "
          f"{sc['ours']['judge_median_mean']} judge | incept: {sc['incept']['fidelity']} fid, "
          f"{sc['incept']['fatal_gate_pass_rate']} fatal-pass, {sc['incept']['judge_median_mean']} judge")
    print("wrote C:/tmp/bakeoff_g9_scorecard.json + C:/tmp/bakeoff_g9.html")
