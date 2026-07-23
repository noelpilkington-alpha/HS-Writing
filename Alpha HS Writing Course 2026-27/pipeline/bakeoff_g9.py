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

_CACHE_DIR = "C:/tmp/bakeoff_cache"

def _judge_cached(item, live):
    """Resumable judge: offline is free + deterministic (no cache needed); live results are cached to disk
    keyed by (item id + rubric version) so a killed/quota-limited run resumes without re-calling."""
    from bakeoff_judge import judge_item, RUBRIC_VERSION
    if not live:
        return judge_item(item, n=3, live=False)
    os.makedirs(_CACHE_DIR, exist_ok=True)
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in f"{item.id}_{RUBRIC_VERSION}")
    path = os.path.join(_CACHE_DIR, f"judge_{safe}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    result = judge_item(item, n=3, live=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(result, fh)
    return result

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

def _score_side(items, cross_pipeline=False, live=False):
    fatal_ok = 0
    fixable_failures = 0
    excluded_failures = 0
    per_item = []
    judges = []
    variances = []
    for it in items:
        r = qc_item(it)
        fatal = []
        fixable = []
        excluded = []
        if not r["passed"]:
            for gname, g in r["gates"].items():
                if not g["passed"]:
                    cls = classify_gate_failure(gname, cross_pipeline=cross_pipeline)
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
        j = _judge_cached(it, live)
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

def _fidelity(items):
    """Count-aware blueprint fidelity: how much of the required G9 section makeup the test actually supplies.

    For each blueprint family (with its required count), credit min(supplied_for_family, required_for_family);
    fidelity = sum(credits) / sum(required). Under-count (e.g. 8 items vs the required 21) shows up as a real
    fidelity drop rather than a presence-only pass."""
    required = {}
    for sec in rmt.BLUEPRINTS["G9"]:
        required[sec["family"]] = required.get(sec["family"], 0) + sec["count"]
    supplied = {}
    for it in items:
        supplied[it.family] = supplied.get(it.family, 0) + 1
    total_required = sum(required.values()) or 1
    credit = sum(min(supplied.get(fam, 0), req) for fam, req in required.items())
    return round(max(0.0, min(1.0, credit / total_required)), 3)

def run(live: bool = False) -> dict:
    ours = _load_our_g9_items()
    incept_items, warnings = parse(load_cached_output_json() if not live else _live_incept())
    ours_sc = _score_side(ours, cross_pipeline=False, live=live); ours_sc["fidelity"] = _fidelity(ours)
    inc_sc = _score_side(incept_items, cross_pipeline=True, live=live); inc_sc["fidelity"] = _fidelity(incept_items)
    inc_sc["adapter_warnings"] = warnings
    def rank(sc):
        return round(sc["fidelity"] * 25 + sc["fatal_gate_pass_rate"] * 25
                     + sc["judge_median_mean"] / 100 * 50, 2)
    ours_rank, inc_rank = rank(ours_sc), rank(inc_sc)
    winner = "ours" if ours_rank > inc_rank else "incept" if inc_rank > ours_rank else "tie"
    verdict = {"winner": winner, "ours_rank": ours_rank, "incept_rank": inc_rank,
               "primary_rank": "fidelity*25 + fatal_gate_pass*25 + judge_median_mean/100*50 "
                               "(fixable + excluded failures reported separately, not in rank)",
               "judge_note": "offline runs use a deterministic structural-heuristic proxy (variance 0); "
                             "live runs use the neutral own-Claude 3-sample median",
               "excluded_gates_note": "acc_tags + cr/scr_binding excluded from Incept fatal-gate "
                                       "(our-internal taxonomy/bank; not test-design defects)"}
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
                    f"<td>{s['fixable_failures']}</td><td>{s['excluded_failures']}</td>"
                    f"<td>{s['judge_median_mean']}</td><td>{esc(s['judge_mode'])}</td>"
                    f"<td>{s['judge_variance_mean']}</td><td>{s['n_items']}</td></tr>")
    doc = (f"<!DOCTYPE html><html><head><meta charset='UTF-8'><title>G9 Bake-Off</title></head><body>"
           f"<h1>G9 Test Bake-Off: winner = {esc(v['winner'])}</h1>"
           f"<p>ours rank {v['ours_rank']} vs incept rank {v['incept_rank']}</p>"
           f"<p>{esc(v['primary_rank'])}</p>"
           f"<p><em>{esc(v.get('excluded_gates_note', ''))}</em></p>"
           f"<p><em>{esc(v.get('judge_note', ''))}</em></p>"
           f"<table border=1 cellpadding=6><tr><th>side</th><th>fidelity</th><th>fatal gate pass</th>"
           f"<th>fixable failures</th><th>excluded failures</th><th>judge median mean</th>"
           f"<th>judge mode</th><th>judge variance mean</th><th>items</th></tr>{''.join(rows)}</table>"
           f"</body></html>")
    with open("C:/tmp/bakeoff_g9.html", "w", encoding="utf-8") as fh:
        fh.write(doc)

if __name__ == "__main__":
    live = "--live" in sys.argv
    sc = run(live=live)
    print(json.dumps(sc["verdict"], indent=1))
    print(f"ours: {sc['ours']['fidelity']} fid, {sc['ours']['fatal_gate_pass_rate']} fatal-pass, "
          f"{sc['ours']['judge_median_mean']} judge ({sc['ours']['judge_mode']}) | "
          f"incept: {sc['incept']['fidelity']} fid, {sc['incept']['fatal_gate_pass_rate']} fatal-pass, "
          f"{sc['incept']['judge_median_mean']} judge ({sc['incept']['judge_mode']})")
    print("wrote C:/tmp/bakeoff_g9_scorecard.json + C:/tmp/bakeoff_g9.html")
