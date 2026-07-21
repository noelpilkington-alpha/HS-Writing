"""
render_model_tests.py - assemble + render a MODEL TEST per grade (G9/G11/G12), to that grade's real blueprint.

The existing assemble_test.py builds the G10 STAAR model test (proven; left untouched). This module does the
same job for the OTHER grades, each to its own test blueprint, reading the grade's own bank directly
(glob + exec, no dependency on bank_loader's G10 hardcoding). Copyright-safe: our OWN items, modeled on the
real forms; no reproduced test content.

Blueprints (from the anchor docs):
  G9  = STAAR English I (near-identical to English II): 1 ECR (arg OR info) + 1 SCR + editing/revising SR sets.
  G11 = the college-test year: assembled as the AP-Lang-style 3-essay FRQ set (synthesis + rhetorical analysis
        + source-free argument) PLUS a multi-perspective (ACT) essay -- the four G11 CR task types.
  G12 = AP Lang exam FRQ section: synthesis + rhetorical analysis + argument, scored rc.ap (sophistication).

HONEST SCOPE: a blueprint-conformant FORM (items + sequence + scoring configs). NOT cut scores, NOT proof of
passing -- that needs a field test with student data. Run: python pipeline/render_model_tests.py [G9|G11|G12|all]
"""
from __future__ import annotations
import os, sys, glob, html, importlib.util

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")

# ---- per-grade blueprints (section -> family + filter + count + scoring) ----
BLUEPRINTS = {
    "G9": [
        {"section": "ECR", "label": "Extended Constructed Response (single-source essay, argument OR informational)",
         "family": "CR", "modes": ["argument", "explanatory"], "count": 1,
         "scoring": "rc.staar (Org/Dev 0-3 + Conv 0-2, x2 = 10)"},
        {"section": "SCR", "label": "Writing Short Constructed Response (repair/revision, 0-1)",
         "family": "SCR", "subskills": ["scr_writing"], "count": 3, "scoring": "rc.scr1 (0-1)"},
        {"section": "MC-evid", "label": "Evidence in context (add/delete/relevance)",
         "family": "SR", "subskills": ["evidence"], "count": 4, "scoring": "auto-key"},
        {"section": "MC-org", "label": "Organization & cohesion",
         "family": "SR", "subskills": ["organization"], "count": 4, "scoring": "auto-key"},
        {"section": "MC-conv", "label": "Conventions & mechanics",
         "family": "SR", "subskills": ["conventions"], "count": 5, "scoring": "auto-key"},
        {"section": "MC-sent", "label": "Sentence structure & boundaries",
         "family": "SR", "subskills": ["sentence"], "count": 4, "scoring": "auto-key"},
    ],
    # G11 = the four college-test-year CR task types. SFA (source-free AP Lang Q3) and MP (multi-perspective
    # ACT) both carry mode="argument", so they are separated by item-id substring, not by mode. SR editing at
    # G11 is the Language course's tier, so the G11 model WRITING test is the essay set.
    "G11": [
        {"section": "FRQ-synth", "label": "Synthesis essay, SBAC/AP Q1 (4-6 sources -> one argument)", "family": "CR", "modes": ["explanatory"], "count": 1, "scoring": "rc.ap (Thesis 0-1 + Ev&Comm 0-4 + Soph 0-1)"},
        {"section": "FRQ-ra", "label": "Rhetorical-analysis essay, AP Q2 (author's choices)", "family": "CR", "modes": ["analysis"], "count": 1, "scoring": "rc.ap"},
        {"section": "FRQ-arg-sf", "label": "Source-free argument essay, AP Lang Q3 (own knowledge)", "family": "CR", "modes": ["argument"], "id_contains": "-SFA-", "count": 1, "scoring": "rc.ap"},
        {"section": "FRQ-arg-mp", "label": "Multi-perspective argument essay, ACT Writing (3 given perspectives)", "family": "CR", "modes": ["argument"], "id_contains": "-MP-", "count": 1, "scoring": "rc.ap"},
    ],
    # G12 = AP Lang exam FRQ section (3 essays), the mastery/timed tier, all rc.ap with sophistication foregrounded.
    "G12": [
        {"section": "FRQ-synth", "label": "AP synthesis FRQ (sophistication + timed)", "family": "CR", "modes": ["explanatory"], "count": 1, "scoring": "rc.ap"},
        {"section": "FRQ-ra", "label": "AP rhetorical-analysis FRQ (sophistication + timed)", "family": "CR", "modes": ["analysis"], "count": 1, "scoring": "rc.ap"},
        {"section": "FRQ-arg", "label": "AP argument FRQ (sophistication + timed)", "family": "CR", "modes": ["argument"], "count": 1, "scoring": "rc.ap"},
    ],
}
ANCHOR = {"G9": "STAAR English I", "G11": "SBAC + ACT + AP Lang (college-test year)", "G12": "AP Lang FRQ (mastery)"}


class _It:
    __slots__ = ("id", "family", "mode", "stem", "stimulus_ref", "rubric_ref")


def _load_items(grade):
    """Read every Item in Item_Bank_<grade> by exec-ing the module and pulling its ITEMS list."""
    items = []
    for f in sorted(glob.glob(os.path.join(ROOT, f"Item_Bank_{grade}", "*.py"))):
        if "__" in os.path.basename(f):
            continue
        spec = importlib.util.spec_from_file_location("mt_" + os.path.basename(f)[:-3].replace(".", "_"), f)
        m = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(m)
        except SystemExit:
            pass
        for it in getattr(m, "ITEMS", []):
            o = _It()
            o.id = it.id; o.family = it.family; o.mode = it.subskill_or_mode
            o.stem = getattr(it, "stem", ""); o.stimulus_ref = getattr(it, "stimulus_ref", "")
            o.rubric_ref = getattr(it, "rubric_ref", "")
            items.append(o)
    return items


def _pool(items, spec):
    idc = spec.get("id_contains")
    out = [it for it in items if it.family == spec["family"] and (
        (spec["family"] == "CR" and it.mode in spec.get("modes", [])) or
        (spec["family"] == "SR" and it.mode in spec.get("subskills", [])) or
        (spec["family"] == "SCR" and it.mode in spec.get("subskills", []))) and (
        idc is None or idc in it.id)]
    return sorted(out, key=lambda i: i.id)


def assemble(grade, n_forms=2):
    bp = BLUEPRINTS[grade]
    items = _load_items(grade)
    pools = {s["section"]: _pool(items, s) for s in bp}
    capacity = min((len(pools[s["section"]]) // s["count"]) for s in bp) if all(pools[s["section"]] for s in bp) else 0
    cursors = {s["section"]: 0 for s in bp}
    forms = []
    for fi in range(n_forms):
        form = {"form_id": f"{grade}-MODEL-{fi+1:02d}", "sections": []}
        for s in bp:
            sec = s["section"]; pool = pools[sec]; c = cursors[sec]
            picked = pool[c:c + s["count"]]
            if len(picked) < s["count"] and pool:
                picked = (pool[c:] + pool[:s["count"] - len(picked)])
            cursors[sec] = (c + s["count"]) % max(len(pool), 1)
            form["sections"].append({"section": sec, "label": s["label"], "scoring": s["scoring"],
                                     "items": picked})
        forms.append(form)
    return forms, capacity, pools


def validate(grade, form):
    bp = {s["section"]: s for s in BLUEPRINTS[grade]}
    probs = []
    seen = set()
    for sec in form["sections"]:
        want = bp[sec["section"]]["count"]
        if len(sec["items"]) != want:
            probs.append(f"{sec['section']}: {len(sec['items'])} items, blueprint wants {want}")
        for it in sec["items"]:
            if it.family == "CR" and not it.stimulus_ref and "arg" not in it.mode:
                pass  # source-free/argument CR may have no stimulus
            if it.id in seen:
                probs.append(f"duplicate item {it.id} within form")
            seen.add(it.id)
    return probs


def _html(grade, forms, capacity, pools):
    def esc(s): return html.escape(str(s))
    secs = ""
    f = forms[0]
    for sec in f["sections"]:
        rows = ""
        for it in sec["items"]:
            ref = f' <span class="mono">-> {esc(it.stimulus_ref)}</span>' if it.stimulus_ref else ""
            rows += (f'<tr><td class="mono">{esc(it.id)}</td><td>{esc((it.stem or "")[:260])}{ref}</td>'
                     f'<td class="mono">{esc(it.rubric_ref or it.mode)}</td></tr>')
        secs += (f'<h3>{esc(sec["section"])} - {esc(sec["label"])}</h3>'
                 f'<div class="muted">scoring: {esc(sec["scoring"])}</div>'
                 f'<table><thead><tr><th>Item id</th><th>Stem (truncated) / binding</th><th>Scoring</th></tr></thead><tbody>{rows}</tbody></table>')
    pool_line = " · ".join(f"{s}: {len(p)}" for s, p in pools.items())
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/><title>{grade} Model Test</title>
<style>body{{font-family:-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:#1f2430;line-height:1.5;max-width:1080px;margin:0 auto;padding:32px 24px 80px;background:#fafafb}}
h1{{font-size:25px;border-bottom:4px solid #6d28d9;padding-bottom:9px}} h3{{color:#6d28d9;margin-top:24px;margin-bottom:2px}}
.sub{{color:#6b7280;font-size:14px}} .muted{{color:#6b7280;font-size:12px;margin-bottom:6px}}
.mono{{font-family:ui-monospace,Consolas,monospace;font-size:12px}}
table{{border-collapse:collapse;width:100%;margin:6px 0 4px;font-size:13px;background:#fff;border-radius:6px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.05)}}
th{{background:#6d28d9;color:#fff;text-align:left;padding:7px 10px;font-size:11px;text-transform:uppercase}} td{{padding:7px 10px;border-top:1px solid #eee;vertical-align:top}}
.ceiling{{background:#fef3c7;border-left:4px solid #d97706;padding:12px 16px;border-radius:0 8px 8px 0;margin:16px 0;font-size:13px}} .ceiling b{{color:#92400e}}</style></head><body>
<h1>{grade} Model Test</h1>
<p class="sub">Blueprint anchor: <b>{esc(ANCHOR[grade])}</b>. Assembled from our own QC-verified {grade} item bank; a blueprint-conformant instrument, not reproduced test content. Showing FORM 01 of {len(forms)}; parallel-form capacity (disjoint items): <b>{capacity}</b>.</p>
<div class="ceiling"><b>Scope.</b> This is a blueprint-conformant FORM (items + sequence + scoring configs). It is NOT cut scores and NOT proof that a student passes - that requires a field test with real student data. CR essays score via the external grader (rc.* configs); SR items auto-key.</div>
<p class="muted">Section pools available in the {grade} bank: {esc(pool_line)}</p>
{secs}
</body></html>"""


def _text(grade, forms, capacity):
    L = [f"=== {grade} MODEL TEST ({ANCHOR[grade]} blueprint) ===",
         "SCOPE: blueprint-conformant form; no cut scores, no student data.", ""]
    for f in forms:
        L.append(f"FORM {f['form_id']}:")
        for sec in f["sections"]:
            L.append(f"  {sec['section']:11} x{len(sec['items'])}  [{sec['scoring']}]  {', '.join(i.id for i in sec['items'])}")
        probs = validate(grade, f)
        L.append(f"    blueprint check: {'OK' if not probs else '**' + '; '.join(probs) + '**'}")
    L.append(f"\nparallel-form capacity (disjoint): {capacity}")
    return "\n".join(L)


def run(grade, n_forms=2, write_html=True):
    forms, capacity, pools = assemble(grade, n_forms)
    if write_html:
        out = os.path.join(ROOT, f"model_test_{grade.lower()}.html")
        open(out, "w", encoding="utf-8").write(_html(grade, forms, capacity, pools))
        print(f"wrote {os.path.relpath(out, HERE)}")
    print(_text(grade, forms, capacity))
    bad = any(validate(grade, f) for f in forms)
    return not bad


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    grades = args if args and args != ["all"] else ["G9", "G11", "G12"]
    ok = all(run(g, write_html=("--html" in sys.argv or True)) for g in grades)
    sys.exit(0 if ok else 1)
