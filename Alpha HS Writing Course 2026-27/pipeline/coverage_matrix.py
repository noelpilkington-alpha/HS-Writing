"""
coverage_matrix.py  -  Alignment coverage matrix: every G10-TESTED writing skill -> is it TAUGHT (a lesson
type) and MEASURED (an item family)?

WHAT THIS PROVES (and what it does NOT): this is a COVERAGE argument, not an efficacy claim. It checks,
mechanically, that no skill the real G10 tests score is left un-taught or un-measured by our content. That
is NECESSARY for students to pass (you cannot pass on a skill you were never taught or tested on) but NOT
SUFFICIENT (coverage does not prove the teaching works; that needs a field test with real students, which
we do not have). The output states this ceiling explicitly.

Source of "what G10 tests score": the reconciled test-design crosswalk (skills_by_grade_crosswalk.html /
TestDesign_Reference.md), reverse-engineered from real released forms (STAAR Eng II, Ohio ELA II, MCAS,
SC-TDA, etc.). Each tested skill is keyed by its ACC standard family.

Method: load the bank (lessons + items) via bank_loader; for each tested skill, find lesson types whose
acc_tags intersect the skill's ACC codes (TAUGHT) and item files whose ACC tags intersect (MEASURED).
Report a per-skill row + flag any gap (tested but not taught, or tested but not measured).

Dependency-free (stdlib + bank_loader). Run: python pipeline/coverage_matrix.py [--html]
"""
from __future__ import annotations
import os, sys, re, glob, html

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
from bank_loader import load_bank
from lesson_contract import LESSON_TYPES

# ---------------------------------------------------------------------------
# The G10-TESTED skills, from the crosswalk (only rows marked TESTED at G10).
# Each: label, the ACC code prefixes it covers, family (CR essay / SR editing), and the real forms that test it.
# ---------------------------------------------------------------------------
TESTED_SKILLS = [
    {"id": "arg", "label": "Argument from sources", "family": "CR",
     "acc": ["ACC.W.ARG.1", "ACC.W.ARG.2", "ACC.W.ARG.3", "ACC.W.ARG.5"],
     "forms": "STAAR Eng II, OH ELA II, MD, MA, SC-TDA"},
    {"id": "info", "label": "Informative / explanatory from sources", "family": "CR",
     "acc": ["ACC.W.INFO.1", "ACC.W.INFO.2", "ACC.W.INFO.3", "ACC.W.INFO.4", "ACC.W.INFO.5"],
     "forms": "English II EOCs (OH, MO), MD informative PCR, ND"},
    {"id": "analysis", "label": "Text-dependent / rhetorical analysis", "family": "CR",
     "acc": ["ACC.W.INFO.6", "ACC.W.SRC.3"],
     "forms": "SC-TDA, PA Keystone, MA, GA Am Lit, NY Regents"},
    {"id": "src", "label": "Reading sources for a writing task (fair use of evidence)", "family": "CR",
     "acc": ["ACC.W.SRC.1", "ACC.W.SRC.2"],
     "forms": "all source-based EOCs"},
    {"id": "synthesis", "label": "Cross-source synthesis (2+ sources)", "family": "CR",
     "acc": ["ACC.W.SRC.1", "ACC.W.SRC.2", "ACC.W.INFO.2"],
     "forms": "MCAS complementary, OH opposing; feeds G11 AP synthesis"},
    {"id": "conv", "label": "Conventions & mechanics (in context)", "family": "SR",
     "acc": ["ACC.W.CONV.1", "ACC.W.CONV.2"],
     "forms": "EOC editing sets, ACT English, SAT, STAAR revising"},
    {"id": "sentence", "label": "Sentence structure & boundaries", "family": "SR",
     "acc": ["ACC.W.CONV.1"],
     "forms": "state EOC/editing, ACT English, SAT"},
    {"id": "org", "label": "Organization & cohesion", "family": "SR",
     "acc": ["ACC.W.ARG.3", "ACC.W.INFO.3"],
     "forms": "TX English I, WY, ACT/SAT expression of ideas"},
    {"id": "evidence_sr", "label": "Evidence in context (add/delete/relevance)", "family": "SR",
     "acc": ["ACC.W.SRC.1", "ACC.W.ARG.2"],
     "forms": "SAT information & ideas, STAAR revising"},
    {"id": "language", "label": "Knowledge of language / style", "family": "SR",
     "acc": ["ACC.W.CONV.3", "ACC.W.ARG.4"],
     "forms": "ACT language use, SAT craft & structure"},
    {"id": "revision", "label": "Scoring & revision to the rubric", "family": "CR",
     "acc": ["ACC.W.PROC.2", "ACC.W.REV.1", "ACC.W.CAL.1"], "rubric_dimension": True,
     "forms": "scored as a rubric dimension inside every EOC essay (not a discrete item)"},
]

# lesson type -> the item-file subskill/mode families that measure the same standard (for the MEASURED column)
ITEM_DIR = os.path.join(ROOT, "Item_Bank_G10")


def _acc_prefixes(tags: list[str]) -> set[str]:
    """Normalize an object's acc_tags to comparable ACC.W.<FAM>.<n> prefixes (drop CCSS/state codes)."""
    out = set()
    for t in tags or []:
        m = re.match(r"(ACC\.W\.[A-Z]+\.\d+)", t)
        if m:
            out.add(m.group(1))
    return out


def _skill_matches(skill_acc: list[str], obj_prefixes: set[str]) -> bool:
    # a skill is served if ANY of its ACC codes appears in the object's tags
    return any(code in obj_prefixes for code in skill_acc)


def build():
    ir = load_bank(run_qc=False)

    # lesson index: type_num -> (name, acc_prefixes)
    lesson_by_type = {}
    for L in ir.lessons:
        lesson_by_type.setdefault(L.lesson_type, (LESSON_TYPES.get(L.lesson_type, ("?",))[0], set()))
        lesson_by_type[L.lesson_type][1].update(_acc_prefixes(L.acc_tags))

    # item index: scan item files for their ACC tags (items expose acc_tags; group by file family)
    item_families = {}  # family label -> set of acc prefixes
    for f in sorted(glob.glob(os.path.join(ITEM_DIR, "*.py"))):
        fam = os.path.basename(f)[:-3]
        src = open(f, encoding="utf-8").read()
        prefixes = set(re.findall(r"ACC\.W\.[A-Z]+\.\d+", src))
        item_families[fam] = prefixes

    rows = []
    for sk in TESTED_SKILLS:
        taught = [f"T{n} {nm}" for n, (nm, pfx) in sorted(lesson_by_type.items())
                  if _skill_matches(sk["acc"], pfx)]
        measured = [fam for fam, pfx in item_families.items() if _skill_matches(sk["acc"], pfx)]
        # Skills scored AS A RUBRIC DIMENSION INSIDE THE ESSAY (not a discrete SR item) are measured by the
        # rc.* rubric engine applied to every CR essay, per TestDesign_Reference (state EOCs score conventions
        # /revision "as a rubric dimension inside the essay"). Real tests have NO standalone item for these, so
        # absence of an SR item file is correct, not a gap.
        rubric_measured = sk.get("rubric_dimension", False)
        if rubric_measured and not measured:
            measured = ["rc.* rubric engine (scored inside every CR essay, not a discrete item)"]
        gap = []
        if not taught:
            gap.append("NOT TAUGHT")
        if not measured:
            gap.append("NOT MEASURED")
        rows.append({**sk, "taught": taught, "measured": measured, "gap": gap})
    return rows


def _text_report(rows) -> str:
    lines = ["=== G10 ALIGNMENT COVERAGE MATRIX ===",
             "(coverage, NOT efficacy: proves no tested skill is un-taught/un-measured; does NOT prove the",
             " teaching works. Efficacy requires a field test with real students, which we do not have.)", ""]
    gaps = 0
    for r in rows:
        status = "OK" if not r["gap"] else ("**" + " + ".join(r["gap"]) + "**")
        if r["gap"]:
            gaps += 1
        lines.append(f"[{status}] {r['label']} ({r['family']}) - {', '.join(r['acc'])}")
        lines.append(f"     taught by:   {', '.join(r['taught']) or 'NOTHING'}")
        lines.append(f"     measured by: {', '.join(r['measured']) or 'NOTHING'}")
    lines.append("")
    lines.append(f"{len(rows)} tested skills | {len(rows)-gaps} fully covered | {gaps} with a coverage gap")
    return "\n".join(lines)


def _html_report(rows) -> str:
    def esc(s): return html.escape(str(s))
    trs = []
    for r in rows:
        cls = "gap" if r["gap"] else "ok"
        status = "OK" if not r["gap"] else " + ".join(r["gap"])
        trs.append(
            f'<tr class="{cls}"><td>{esc(r["label"])}<span class="forms">tested by: {esc(r["forms"])}</span></td>'
            f'<td class="fam {r["family"].lower()}">{esc(r["family"])}</td>'
            f'<td class="acc">{"".join(f"<span>{esc(a)}</span>" for a in r["acc"])}</td>'
            f'<td>{"<br>".join(esc(t) for t in r["taught"]) or "<b>NOTHING</b>"}</td>'
            f'<td>{"<br>".join(esc(m) for m in r["measured"]) or "<b>NOTHING</b>"}</td>'
            f'<td class="st">{esc(status)}</td></tr>')
    gaps = sum(1 for r in rows if r["gap"])
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0"><title>G10 Alignment Coverage Matrix</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:#1e293b;line-height:1.5;max-width:1120px;margin:0 auto;padding:30px 22px 80px;background:#fff}}
h1{{font-size:1.6rem;margin:0 0 4px}}.sub{{color:#64748b;font-size:.95rem}}
.ceiling{{background:#fef3c7;border-left:4px solid #d97706;padding:13px 17px;border-radius:0 8px 8px 0;margin:18px 0;font-size:.9rem}}
.ceiling b{{color:#92400e}}
.stat{{display:inline-block;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:8px 16px;margin:6px 8px 6px 0;font-size:.85rem}}
.stat b{{font-size:1.2rem;color:#2563eb}}
table{{width:100%;border-collapse:collapse;margin:16px 0;font-size:.82rem}}
th,td{{text-align:left;padding:9px 11px;border:1px solid #e2e8f0;vertical-align:top}}
th{{background:#f8fafc;font-size:.7rem;text-transform:uppercase;letter-spacing:.03em;color:#64748b}}
tr.ok{{background:#f6fefb}} tr.gap{{background:#fef2f2}}
tr.gap .st{{color:#991b1b;font-weight:800}} tr.ok .st{{color:#166534;font-weight:800}}
.fam{{font-weight:700;text-align:center}}.fam.cr{{color:#7c3aed}}.fam.sr{{color:#0d9488}}
.acc{{font-family:ui-monospace,Menlo,monospace;font-size:.7rem}}.acc span{{display:block;background:#eef2ff;color:#4338ca;border-radius:4px;padding:1px 5px;margin-bottom:2px}}
.forms{{display:block;color:#64748b;font-size:.72rem;margin-top:4px;font-style:italic}}
</style></head><body>
<h1>Grade 10 Writing: Alignment Coverage Matrix</h1>
<p class="sub">Every skill the real G10 writing tests SCORE, mapped to the lesson type that TEACHES it and the item family that MEASURES it.</p>
<div class="ceiling"><b>What this proves, and what it does not.</b> This is a COVERAGE argument: it shows no
tested skill is left un-taught or un-measured, which is NECESSARY for students to pass (you cannot pass on a
skill you were never taught or tested on). It is NOT an efficacy claim: coverage does not prove the teaching
works. That requires a field test with real student data, which we do not yet have. Read this as "the course
targets everything the test scores," not "the course is proven to produce passing scores."</div>
<div><span class="stat"><b>{len(rows)}</b> tested skills</span>
<span class="stat"><b>{len(rows)-gaps}</b> fully covered</span>
<span class="stat"><b>{gaps}</b> coverage gaps</span></div>
<table><thead><tr><th>Tested skill (and the real forms that score it)</th><th>Family</th><th>ACC standards</th><th>Taught by (lesson type)</th><th>Measured by (item family)</th><th>Status</th></tr></thead>
<tbody>{"".join(trs)}</tbody></table>
<p class="sub" style="margin-top:20px">Source of tested skills: the reconciled test-design crosswalk (skills_by_grade_crosswalk.html / TestDesign_Reference.md), reverse-engineered from real released G10 forms. Taught/measured columns are read live from the lesson and item banks (acc_tags), so this matrix cannot drift from what was actually built.</p>
</body></html>"""


if __name__ == "__main__":
    rows = build()
    if "--html" in sys.argv:
        out = os.path.join(ROOT, "coverage_matrix.html")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(_html_report(rows))
        print(f"wrote {os.path.relpath(out, HERE)}")
    print(_text_report(rows))
    gaps = sum(1 for r in rows if r["gap"])
    sys.exit(0 if gaps == 0 else 1)
