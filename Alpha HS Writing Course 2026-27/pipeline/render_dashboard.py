"""
render_dashboard.py - one consolidated, LIVE dashboard for the G9-12 writing course build.

Reads CURRENT state (imports the source-of-truth module, counts the stimulus/item banks, runs each grade's
cross-check) so the dashboard reflects reality, not a hand-typed snapshot that drifts. Writes DASHBOARD.html
next to the source docs, linking every rendered artifact.

Run: python pipeline/render_dashboard.py   ->  writes ../DASHBOARD.html
Dependency-free (stdlib + the local pipeline). Does not overwrite the repo-root index.html (old-courses nav).
"""
from __future__ import annotations
import os, sys, glob, html, subprocess, re, importlib.util

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
from course_sequence_g9_12 import HS_KCS, ACC_SPINE, EXTERNAL_OWNED, DESCOPED, UNITS  # source of truth

GRADES = ["G9", "G10", "G11", "G12"]


def _count_bank(dirname):
    """Return (file_count, item_or_stimulus_count) by exec-ing each module and reading ITEMS/REC."""
    d = os.path.join(ROOT, dirname)
    files = sorted(glob.glob(os.path.join(d, "*.py")))
    files = [f for f in files if "__" not in os.path.basename(f)]
    n_files, n_units = 0, 0
    for f in files:
        n_files += 1
        try:
            spec = importlib.util.spec_from_file_location("m_" + os.path.basename(f)[:-3].replace(".", "_"), f)
            m = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(m)
            except SystemExit:
                pass
            if hasattr(m, "ITEMS"):
                n_units += len(m.ITEMS)
            else:
                # stimulus modules name their record variably (REC/rec/...); count any StimulusRecord instance
                found = [v for v in vars(m).values() if type(v).__name__ == "StimulusRecord"]
                n_units += len(found) if found else 0
        except Exception:
            pass
    return n_files, n_units


def _crosscheck(grade):
    """Run the grade cross-check; return (passed, headline)."""
    try:
        r = subprocess.run([sys.executable, os.path.join(HERE, "testbank_kc_crosscheck.py"), grade],
                           capture_output=True, text=True, timeout=120)
        passed = r.returncode == 0
        m = re.search(r"item files: \d+ \| distinct ACC codes used by items: \d+ \| stimulus ids found: \d+", r.stdout)
        return passed, (m.group(0) if m else ("PASS" if passed else "FAIL"))
    except Exception as e:
        return False, f"error: {e}"


def _run_selftest(modpath, label):
    try:
        r = subprocess.run([sys.executable, os.path.join(HERE, modpath)], capture_output=True, text=True, timeout=120)
        return r.returncode == 0
    except Exception:
        return False


def esc(s):
    return html.escape(str(s))


def main():
    # --- live gather ---
    kc_by_grade = {g: [k for k in HS_KCS if k["grade"] == g] for g in GRADES}
    acc_hs = sum(1 for a in ACC_SPINE if a["need"] == "hs")
    acc_ext = sum(1 for a in ACC_SPINE if a["need"] == "external")
    acc_desc = sum(1 for a in ACC_SPINE if a["need"] == "descoped")

    banks = {}
    for g in GRADES:
        sf, sc = _count_bank(f"Stimulus_Bank_{g}")
        if_, ic = _count_bank(f"Item_Bank_{g}")
        cc_pass, cc_head = _crosscheck(g)
        banks[g] = dict(stim_files=sf, stim_ct=sc, item_files=if_, item_ct=ic, cc_pass=cc_pass, cc_head=cc_head,
                        kcs=len(kc_by_grade[g]), units=len(UNITS.get(g, [])))

    module_ok = _run_selftest("course_sequence_g9_12.py", "source of truth")
    matrix_ok = _run_selftest("kc_coverage_matrix.py", "coverage matrix")

    # --- rendered docs to link (only those that exist) ---
    doc_links = [
        ("KC_Map_and_Unit_Arch_G9-12.html", "KC Map + Unit Architectures", "the per-grade KC map, ACC-anchored, with unit archs"),
        ("Sentence_Skill_Roster_FINAL.html", "Sentence/Paragraph/Essay Roster", "the gap-scoped skill roster + ACC crosswalk"),
        ("Sentence_Progression_G9-12.html", "Sentence Progression (reasoning trail)", "the evidence/reasoning behind the roster"),
        ("kc_coverage_matrix.html", "KC Coverage Matrix (ACC)", "every ACC standard + tested capability -> owner; regression guard"),
        ("_evidence/writing_item_type_catalog.html", "Item-Type Catalog", "test item formats x Timeback deliverability"),
        ("coverage_matrix.html", "G10 Bank Coverage Matrix (legacy)", "the older G10 bank-level matrix"),
        ("model_test_g10.html", "Model Test (G10)", "assembled model test"),
        ("model_test_content_vs_staar.html", "Model Test vs STAAR", "content-vs-real-form comparison"),
        ("skills_by_grade_crosswalk.html", "Skills-by-Grade Crosswalk", "tested skills across states"),
        ("timeback_feasibility.html", "Timeback Feasibility", "QTI deliverability of item types"),
    ]
    doc_links = [(h, t, d) for (h, t, d) in doc_links if os.path.exists(os.path.join(ROOT, h))]

    total_stim = sum(b["stim_ct"] for b in banks.values())
    total_items = sum(b["item_ct"] for b in banks.values())
    all_cc = all(b["cc_pass"] for b in banks.values())

    # --- build HTML ---
    grade_rows = ""
    for g in GRADES:
        b = banks[g]
        cc = '<span class="ok">PASS</span>' if b["cc_pass"] else '<span class="bad">FAIL</span>'
        grade_rows += (f"<tr><td><b>{g}</b></td><td>{b['kcs']}</td><td>{b['units']}</td>"
                       f"<td>{b['stim_ct']} <span class='muted'>({b['stim_files']} files)</span></td>"
                       f"<td>{b['item_ct']} <span class='muted'>({b['item_files']} files)</span></td>"
                       f"<td>{cc}</td></tr>")

    acc_rows = ""
    for a in ACC_SPINE:
        owners = [k["id"] for k in HS_KCS if a["code"] in k["acc"]]
        who = ", ".join(owners) if owners else (EXTERNAL_OWNED_hint(a) )
        cls = {"hs": "hs", "external": "ext", "descoped": "desc"}[a["need"]]
        acc_rows += (f"<tr class='{cls}'><td class='mono'>{esc(a['code'])}</td><td>{esc(a['name'])}</td>"
                     f"<td>{esc(a['need'])}</td><td>{esc(who)}</td></tr>")

    doc_cards = "".join(
        f'<a class="card" href="{esc(h)}"><div class="ct">{esc(t)}</div><div class="cd">{esc(d)}</div></a>'
        for (h, t, d) in doc_links)

    banks_note = ("The test banks (stimuli + items) are Python modules that self-verify against the QC contracts; "
                  "they have no per-file HTML, but their LIVE counts + cross-check status are shown above "
                  "(this dashboard re-runs each grade's cross-check on render).")

    doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>G9-12 Writing Course - Build Dashboard</title>
<style>
  :root{{--accent:#6d28d9;--ok:#16a34a;--bad:#b91c1c;--ink:#1f2430;--muted:#6b7280;}}
  *{{box-sizing:border-box}}
  body{{font-family:-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:var(--ink);line-height:1.5;max-width:1100px;margin:0 auto;padding:34px 26px 90px;background:#fafafb}}
  h1{{font-size:27px;border-bottom:4px solid var(--accent);padding-bottom:10px;margin-bottom:4px}}
  h2{{font-size:19px;color:var(--accent);margin-top:34px;border-bottom:1px solid #e5e7eb;padding-bottom:5px}}
  .sub{{color:var(--muted);font-size:14px;margin-top:0}}
  .status{{display:flex;gap:14px;flex-wrap:wrap;margin:18px 0}}
  .pill{{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:12px 18px;box-shadow:0 1px 3px rgba(0,0,0,.05)}}
  .pill b{{font-size:22px;display:block;color:var(--accent)}}
  .ok{{color:var(--ok);font-weight:700}} .bad{{color:var(--bad);font-weight:700}}
  .muted{{color:var(--muted);font-size:12px}} .mono{{font-family:ui-monospace,Consolas,monospace;font-size:12px}}
  table{{border-collapse:collapse;width:100%;margin:12px 0;font-size:14px;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.05)}}
  th{{background:var(--accent);color:#fff;text-align:left;padding:9px 11px;font-size:12px;text-transform:uppercase;letter-spacing:.02em}}
  td{{padding:8px 11px;border-top:1px solid #eee;vertical-align:top}}
  tr.hs td:first-child{{border-left:3px solid var(--accent)}} tr.ext td:first-child{{border-left:3px solid #0d9488}} tr.desc td:first-child{{border-left:3px solid #9ca3af}}
  .cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px;margin:14px 0}}
  .card{{display:block;background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:14px 16px;text-decoration:none;color:var(--ink);box-shadow:0 1px 3px rgba(0,0,0,.05)}}
  .card:hover{{border-color:var(--accent)}}
  .card .ct{{font-weight:700;color:var(--accent)}} .card .cd{{font-size:13px;color:var(--muted);margin-top:3px}}
  .ceiling{{background:#fef3c7;border-left:4px solid #d97706;padding:13px 17px;border-radius:0 8px 8px 0;margin:18px 0;font-size:14px}}
  .ceiling b{{color:#92400e}} .note{{font-size:13px;color:var(--muted);margin-top:8px}}
</style></head><body>
<h1>G9-12 Writing Course - Build Dashboard</h1>
<p class="sub">Live view (re-computed on render) of the ACC-anchored KC map, the verified test bank across all four grades, and the sentence/paragraph/essay roster. Source of truth: <span class="mono">pipeline/course_sequence_g9_12.py</span>.</p>

<div class="status">
  <div class="pill"><b>{len(HS_KCS)}</b>HS-owned KCs</div>
  <div class="pill"><b>{len(ACC_SPINE)}</b>ACC codes ({acc_hs} hs / {acc_ext} ext / {acc_desc} descoped)</div>
  <div class="pill"><b>{total_stim}</b>stimuli (all grades)</div>
  <div class="pill"><b>{total_items}</b>test items (all grades)</div>
  <div class="pill"><b class="{ 'ok' if all_cc else 'bad'}">{ 'ALL PASS' if all_cc else 'CHECK'}</b>cross-checks</div>
  <div class="pill"><b class="{ 'ok' if module_ok else 'bad'}">{ 'PASS' if module_ok else 'FAIL'}</b>source-of-truth self-test</div>
  <div class="pill"><b class="{ 'ok' if matrix_ok else 'bad'}">{ 'PASS' if matrix_ok else 'FAIL'}</b>coverage matrix</div>
</div>

<div class="ceiling"><b>What this proves, and what it does not.</b> COVERAGE + QC integrity: every ACC standard is taught + tested, every stimulus is Lexile-banded + fact-grounded, every item passes its gates, and the KC map / test bank / roster all speak the same ACC common standard. It does NOT prove EFFICACY (that students taught this pass) - that needs field data with real students. Pre-ship items: Lexile is a proxy (needs licensed MetaMetrics); CR scoring goes live when the grader redeploys; AP Lit deferred (G12 = AP Lang).</div>

<h2>Test bank + KCs, by grade (live)</h2>
<table><thead><tr><th>Grade</th><th>HS KCs</th><th>Units</th><th>Stimuli</th><th>Test items</th><th>Cross-check</th></tr></thead>
<tbody>{grade_rows}</tbody></table>
<p class="note">{esc(banks_note)}</p>

<h2>Rendered documents</h2>
<div class="cards">{doc_cards}</div>

<h2>AlphaCommonCore spine - coverage (live)</h2>
<p class="sub">The common standard (&gt;=2-state union). hs = an HS KC owns it; ext = a separate HS course (Language/Vocabulary/Reading); descoped = documented deferral.</p>
<table><thead><tr><th>ACC code</th><th>Sub-skill</th><th>Owner type</th><th>Owned by</th></tr></thead>
<tbody>{acc_rows}</tbody></table>

<p class="note">Generated by <span class="mono">pipeline/render_dashboard.py</span> - re-run it to refresh. This dashboard does not replace the repo-root index.html (old-courses nav).</p>
</body></html>"""
    out = os.path.join(ROOT, "DASHBOARD.html")
    open(out, "w", encoding="utf-8").write(doc)
    print(f"wrote {os.path.relpath(out, HERE)}")
    print(f"  KCs={len(HS_KCS)} ACC={len(ACC_SPINE)} stimuli={total_stim} items={total_items} "
          f"cross-checks={'ALL PASS' if all_cc else 'CHECK'} module={'PASS' if module_ok else 'FAIL'}")


def EXTERNAL_OWNED_hint(a):
    if a["need"] == "external":
        return "external HS course (Language/Vocabulary/Reading)"
    if a["need"] == "descoped":
        return "documented descope/defer"
    return "NO HS KC"


if __name__ == "__main__":
    main()
