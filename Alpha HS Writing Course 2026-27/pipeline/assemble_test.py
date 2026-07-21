"""
assemble_test.py  -  Assemble a G10 model test form from the bank, to the STAAR English II blueprint,
and prove the equivalent-form pool (parallel retake forms with disjoint items, same blueprint).

WHY THIS EXISTS: the coverage matrix proves every tested skill is taught + measured. A model TEST turns
that into the concrete instrument a student sits: real bank items selected + sequenced to a real form's
shape. It is the yardstick the course is measured against.

BLUEPRINT (from AnchorSets/G10_anchor_forms.md, STAAR English II, our top G10 anchor):
  - 1 Extended Constructed Response (ECR): the source-based essay, scored Org/Dev 0-3 + Conventions 0-2,
    x2 scorers = 10 pts. Mode fixed by the prompt (argument or informational), anchored to a reading selection.
  - 2 Short Constructed Responses (SCR): one writing-domain SCR (0-1) = our SCR modifier-repair item.
    (STAAR's second SCR is reading-domain; our writing bank models the writing SCR.)
  - SR editing/revising set: two revising passages + two editing passages worth of items, spanning the
    tested SR sub-skills (conventions, sentence boundaries, organization, evidence-in-context, language/style).
    We model this as a fixed count per sub-skill drawn from the SR bank.

HONEST SCOPE: this assembles a blueprint-conformant FORM (items + sequence + scoring configs). It does NOT
set cut scores (the score that = passing) and carries no student-response data. Cut scores + pass rates
require a field test. This is the instrument, not proof of passing.

Reads live from the bank (bank_loader) so a form can never cite an item that does not exist.
Dependency-free (stdlib). Run: python pipeline/assemble_test.py [--html] [--forms N]
"""
from __future__ import annotations
import os, sys, html

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
from bank_loader import load_bank

# STAAR English II blueprint, writing-relevant core (counts our bank can source).
# section -> (label, family, subskill_or_mode filter, count, scoring)
BLUEPRINT = [
    {"section": "ECR", "label": "Extended Constructed Response (source-based essay)",
     "family": "CR", "modes": ["argument", "explanatory"], "count": 1, "scoring": "rc.staar (Org/Dev 0-3 + Conv 0-2, x2 = 10)"},
    # G10 scr items migrated to SCR family; analysis/research types deferred
    {"section": "SCR", "label": "Writing Short Constructed Response (modifier-repair, meaning-preserved)",
     "family": "SCR", "subskills": ["scr_writing"], "count": 1, "scoring": "0-1 generic (grader)"},
    {"section": "EDIT-conv", "label": "Editing set: conventions & mechanics",
     "family": "SR", "subskills": ["conventions"], "count": 6, "scoring": "auto-key (match_correct)"},
    {"section": "EDIT-sent", "label": "Editing set: sentence structure & boundaries",
     "family": "SR", "subskills": ["sentence"], "count": 5, "scoring": "auto-key"},
    {"section": "REV-org", "label": "Revising set: organization & cohesion",
     "family": "SR", "subskills": ["organization"], "count": 5, "scoring": "auto-key"},
    {"section": "REV-evid", "label": "Revising set: evidence in context (add/delete/relevance)",
     "family": "SR", "subskills": ["evidence"], "count": 5, "scoring": "auto-key"},
    {"section": "REV-lang", "label": "Revising set: knowledge of language / style",
     "family": "SR", "subskills": ["language"], "count": 4, "scoring": "auto-key"},
]


def _pool(ir, spec):
    """All bank items eligible for a blueprint section (a stable, sorted candidate pool)."""
    out = []
    for it in ir.items:
        if it.family != spec["family"]:
            continue
        key = it.subskill_or_mode
        if spec["family"] == "CR" and key in spec.get("modes", []):
            out.append(it)
        elif spec["family"] == "SR" and key in spec.get("subskills", []):
            out.append(it)
        elif spec["family"] == "SCR" and key in spec.get("subskills", []):
            out.append(it)
    return sorted(out, key=lambda i: i.id)


def assemble_forms(ir, n_forms: int):
    """Build n parallel forms. Each form takes the NEXT `count` items from each section's pool, so forms
    are disjoint (no item reused across forms) as long as the pool is deep enough. Returns (forms, capacity)."""
    pools = {spec["section"]: _pool(ir, spec) for spec in BLUEPRINT}
    # capacity: how many disjoint full forms the bank can build = min over sections of floor(pool/count)
    capacity = min(len(pools[s["section"]]) // s["count"] for s in BLUEPRINT)
    cursors = {s["section"]: 0 for s in BLUEPRINT}
    forms = []
    for fi in range(n_forms):
        form = {"form_id": f"G10-STAAR-MODEL-{fi+1:02d}", "sections": []}
        for spec in BLUEPRINT:
            sec = spec["section"]
            pool = pools[sec]
            c = cursors[sec]
            picked = pool[c:c + spec["count"]]
            # wrap if we run past the pool (only happens when n_forms > capacity; flagged in output)
            if len(picked) < spec["count"]:
                picked = (pool[c:] + pool[:spec["count"] - len(picked)])
            cursors[sec] = (c + spec["count"]) % max(len(pool), 1)
            form["sections"].append({
                "section": sec, "label": spec["label"], "scoring": spec["scoring"],
                "items": [{"id": it.id, "mode": it.subskill_or_mode,
                           "stimulus": getattr(it, "stimulus_ref", "") or None} for it in picked],
            })
        forms.append(form)
    return forms, capacity


def validate(form) -> list[str]:
    """Mechanical blueprint check: right count per section, ECR binds a stimulus, no dup items within a form."""
    problems, seen = [], set()
    by_section = {s["section"]: s for s in BLUEPRINT}
    for sec in form["sections"]:
        spec = by_section[sec["section"]]
        if len(sec["items"]) != spec["count"]:
            problems.append(f"{sec['section']}: {len(sec['items'])} items, blueprint wants {spec['count']}")
        for it in sec["items"]:
            if it["id"] in seen:
                problems.append(f"duplicate item within form: {it['id']}")
            seen.add(it["id"])
            if sec["section"] == "ECR" and not it["stimulus"]:
                problems.append(f"ECR item {it['id']} binds no stimulus (a source-based essay needs a source)")
    return problems


def disjoint_check(forms) -> dict:
    """Confirm parallel forms share no items (true equivalent forms for retakes)."""
    sets = [set(it["id"] for sec in f["sections"] for it in sec["items"]) for f in forms]
    overlaps = []
    for i in range(len(sets)):
        for j in range(i + 1, len(sets)):
            shared = sets[i] & sets[j]
            if shared:
                overlaps.append((forms[i]["form_id"], forms[j]["form_id"], sorted(shared)))
    return {"all_disjoint": not overlaps, "overlaps": overlaps}


def _text(forms, capacity, n_forms):
    L = ["=== G10 MODEL TEST (STAAR English II blueprint) ===",
         f"assembled from the live bank; {len(forms)} parallel form(s) shown; pool supports ~{capacity} disjoint forms",
         "SCOPE: a blueprint-conformant instrument. No cut scores, no student data. Passing requires a field test.",
         ""]
    total_pts_note = "Form scoring: 1 ECR (rc.staar, 10 pts) + 1 writing SCR (0-1) + 25 auto-keyed SR editing/revising items."
    for f in forms:
        L.append(f"--- {f['form_id']} ---   ({total_pts_note})")
        probs = validate(f)
        L.append(f"    blueprint check: {'OK' if not probs else '**' + '; '.join(probs) + '**'}")
        for sec in f["sections"]:
            ids = ", ".join(it["id"].replace("ACC-W910-", "") for it in sec["items"])
            src = ""
            if sec["section"] == "ECR":
                src = f"  [source: {sec['items'][0]['stimulus'].replace('ACC-W910-','') if sec['items'][0]['stimulus'] else 'NONE'}]"
            L.append(f"    {sec['label']}: {ids}{src}")
        L.append("")
    dj = disjoint_check(forms)
    L.append(f"equivalent-form pool: {'DISJOINT (no item shared across forms -> valid retake forms)' if dj['all_disjoint'] else 'OVERLAP: ' + str(dj['overlaps'])}")
    return "\n".join(L)


def _html(forms, capacity):
    def esc(s): return html.escape(str(s))
    dj = disjoint_check(forms)
    secs_html = []
    for f in forms:
        probs = validate(f)
        rows = []
        for sec in f["sections"]:
            items = "".join(
                f'<li><code>{esc(it["id"])}</code>'
                + (f' <span class="src">source: {esc(it["stimulus"])}</span>' if it.get("stimulus") else "")
                + "</li>" for it in sec["items"])
            rows.append(f'<div class="sec"><div class="sl">{esc(sec["label"])} '
                        f'<span class="sc">{esc(sec["scoring"])}</span></div><ul>{items}</ul></div>')
        secs_html.append(
            f'<div class="form"><h3>{esc(f["form_id"])} '
            f'<span class="bp {"ok" if not probs else "bad"}">{"blueprint OK" if not probs else "; ".join(probs)}</span></h3>'
            + "".join(rows) + "</div>")
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0"><title>G10 Model Test (STAAR English II blueprint)</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:#1e293b;line-height:1.5;max-width:1000px;margin:0 auto;padding:30px 22px 80px}}
h1{{font-size:1.55rem;margin:0 0 4px}}.sub{{color:#64748b;font-size:.95rem}}
.scope{{background:#fef3c7;border-left:4px solid #d97706;padding:13px 17px;border-radius:0 8px 8px 0;margin:16px 0;font-size:.9rem}}.scope b{{color:#92400e}}
.bpnote{{background:#f0f9ff;border:1px solid #bae6fd;border-radius:8px;padding:12px 16px;font-size:.87rem;margin:14px 0}}
.forms{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}@media(max-width:800px){{.forms{{grid-template-columns:1fr}}}}
.form{{border:1px solid #e2e8f0;border-radius:12px;padding:16px 18px}}
.form h3{{margin:0 0 10px;font-size:1.05rem}}
.bp{{font-size:.68rem;font-weight:700;padding:2px 9px;border-radius:20px;vertical-align:middle}}
.bp.ok{{background:#dcfce7;color:#166534}}.bp.bad{{background:#fee2e2;color:#991b1b}}
.sec{{margin:9px 0}}.sl{{font-size:.83rem;font-weight:700}}.sc{{font-weight:400;color:#64748b;font-size:.72rem;font-family:ui-monospace,Menlo,monospace}}
ul{{margin:4px 0 0;padding-left:20px}}li{{font-size:.8rem;margin:2px 0}}
code{{background:#eef2ff;color:#4338ca;border-radius:4px;padding:1px 5px;font-size:.76rem}}
.src{{color:#0369a1;font-size:.72rem}}
.pool{{margin-top:20px;padding:12px 16px;border-radius:8px;background:#f6fefb;border:1px solid #86efac;font-size:.88rem}}
.pool.bad{{background:#fef2f2;border-color:#fca5a5}}
</style></head><body>
<h1>Grade 10 Model Test</h1><p class="sub">Assembled from the item bank to the STAAR English II blueprint (our top G10 anchor).</p>
<div class="scope"><b>What this is, and is not.</b> This is a blueprint-conformant test FORM: real bank items
selected and sequenced to the shape of a real G10 EOC. It is the instrument the course is measured against.
It does NOT include cut scores (the score that equals passing) and carries no student-response data. Pass
rates and cut scores require a field test with real students. This shows the test, not proof of passing.</div>
<div class="bpnote"><b>STAAR English II blueprint (writing core):</b> 1 Extended Constructed Response
(source-based essay, scored Organization/Development 0-3 + Conventions 0-2, x2 scorers = 10) + 1 writing
Short Constructed Response (modifier-repair, 0-1) + a 25-item editing/revising set spanning conventions,
sentence boundaries, organization, evidence-in-context, and language/style. Source: AnchorSets/G10_anchor_forms.md.</div>
<div class="pool {'' if dj['all_disjoint'] else 'bad'}"><b>Equivalent-form pool:</b> the bank supports about
<b>{capacity}</b> fully disjoint parallel forms (same blueprint, no shared items) for retakes.
{'The forms shown below share no items, so they are valid equivalent retake forms.' if dj['all_disjoint'] else 'WARNING: forms overlap: ' + esc(dj['overlaps'])}</div>
<div class="forms">{"".join(secs_html)}</div>
<p class="sub" style="margin-top:20px">Forms are read live from the bank (bank_loader), so a form can never
cite an item that does not exist. The equivalent-form pool is what a Timeback <code>test_bank</code> draws
from to give each retake an unseen form.</p></body></html>"""


if __name__ == "__main__":
    n = 2
    if "--forms" in sys.argv:
        n = int(sys.argv[sys.argv.index("--forms") + 1])
    ir = load_bank(run_qc=False)
    forms, capacity = assemble_forms(ir, n)
    if "--html" in sys.argv:
        out = os.path.join(ROOT, "model_test_g10.html")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(_html(forms, capacity))
        print(f"wrote {os.path.relpath(out, HERE)}")
    print(_text(forms, capacity, n))
    # exit non-zero if any form fails the blueprint or forms overlap
    bad = any(validate(f) for f in forms) or not disjoint_check(forms)["all_disjoint"]
    sys.exit(1 if bad else 0)
