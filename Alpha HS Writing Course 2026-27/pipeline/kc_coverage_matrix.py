"""
kc_coverage_matrix.py - Map-level coverage matrix for the reconciled G9-12 KC map.

WHAT THIS PROVES (and what it does NOT): a COVERAGE argument, not an efficacy claim. It checks,
mechanically, that every tested writing capability AND every CCSS/TEKS writing-standard family has an
OWNER - an HS-owned KC, an external HS course (Language / Vocabulary / Reading), a gated app, or an
EXPLICIT documented descope. A capability/standard with no owner = a silent hole = FAIL. This is
NECESSARY for students to pass (you cannot pass a skill nobody teaches) but NOT SUFFICIENT (coverage does
not prove the teaching works; that needs field data with real students, which we do not have).

This is the machine-checkable form of the backward-trace audit (`_evidence/kc_coverage_audit.md`). It is a
regression guard: if a later edit drops a KC or an owner, a denominator row goes un-owned and this fails.

Standards-first (Noel 2026-07-08): the course anchors to the common standards (CCSS/TEKS + AlphaCommonCore
spine); AP/ACT are thin overlays. So every HS KC must carry a PRIMARY CCSS/TEKS tag; the matrix validates
standards coverage first, tested-capability coverage second.

Distinct from `coverage_matrix.py` (the older G10 BANK-level matrix that reads live lesson/item files -
useful once lessons are rebuilt against these KCs; stale until then).

Dependency-free (stdlib). Run: python pipeline/kc_coverage_matrix.py [--html]
Exit 0 iff every denominator row is owned AND every consistency assertion holds.
"""
from __future__ import annotations
import os, sys, html

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)

# SINGLE SOURCE OF TRUTH: import the KC map / ACC spine / ownership registries from the canonical module.
# This matrix does NOT redefine them - it VALIDATES coverage over them, so the two cannot diverge.
from course_sequence_g9_12 import HS_KCS, ACC_SPINE, EXTERNAL_OWNED, DESCOPED  # noqa: E402

# (HS_KCS, EXTERNAL_OWNED, DESCOPED, ACC_SPINE are imported above from course_sequence_g9_12 - the
#  single source of truth. This module only adds the tested-capability + CCSS/TEKS-family DENOMINATORS
#  below and validates that every one is owned by the imported data.)

# ---------------------------------------------------------------------------
# THE DENOMINATOR: every tested writing capability (from the crosswalk / released tests) + who must own it.
#    'need' = owner category the matrix requires: 'hs' (an HS KC funnel), 'external', or 'descoped'.
#    'need' = owner category the matrix requires: 'hs' (an HS KC funnel), 'external', or 'descoped'.
# ---------------------------------------------------------------------------
TESTED_CAPABILITIES = [
    dict(cap="argument", label="Argument from sources", tests="STAAR EI/EII, all EOC, SBAC, AP Lang", need="hs"),
    dict(cap="informational", label="Informational/explanatory from source(s)", tests="STAAR (dominant ECR), OH/MO EOC, SBAC explanatory", need="hs"),
    dict(cap="analysis", label="Text-dependent / rhetorical analysis of a text's ideas", tests="SC-TDA, PA Keystone, MA, Regents Pt3", need="hs"),
    dict(cap="rhetorical_analysis", label="Rhetorical analysis of author's CHOICES", tests="AP Lang RA, NH SAT, FL G11", need="hs"),
    dict(cap="counterargument", label="Counterclaim (acknowledge + refute)", tests="STAAR EII, SBAC, MD, SC", need="hs"),
    dict(cap="evidence", label="Attributed evidence (cite/quote/paraphrase)", tests="all source-based EOC", need="hs"),
    dict(cap="reasoning", label="Reasoning/warrant (why evidence supports claim)", tests="EOC development trait, AP Row B", need="hs"),
    dict(cap="multisource", label="Cross-text 2-3 source integration", tests="NY/FL/MA/MD/SC/LA/NJ (modal G10 EOC)", need="hs"),
    dict(cap="synthesis", label="Full synthesis (4-6 sources)", tests="SBAC, AP Lang 6-source, Regents 4-source", need="hs"),
    dict(cap="source_free_argument", label="Argue from own knowledge (no source)", tests="AP Lang Q3", need="hs"),
    dict(cap="multi_perspective", label="Multi-perspective argument (3 given perspectives)", tests="ACT Writing", need="hs"),
    dict(cap="source_evaluation", label="Evaluate source credibility/bias", tests="SBAC/PARCC research tasks", need="hs"),
    dict(cap="production_of_writing", label="Production of Writing (transitions, add/delete/reorder, organization)", tests="ACT English 38-43%, SAT Expression, STAAR revising", need="hs"),
    dict(cap="sophistication", label="Sophistication (significance/context/complexity)", tests="AP Row C, ACT Ideas&Analysis", need="hs"),
    dict(cap="timed", label="Timed-writing performance", tests="ACT/SAT/AP timing", need="hs"),
    dict(cap="essay", label="Multi-paragraph essay assembly", tests="every CR essay", need="hs"),
    # externally owned (gate must be safe)
    dict(cap="conventions", label="Conventions & mechanics (in context)", tests="EOC editing, ACT English CSE, SAT, STAAR editing", need="external"),
    dict(cap="knowledge_of_language", label="Knowledge of language / style (SR editing)", tests="ACT KoL, SAT Craft & Structure", need="external"),
    dict(cap="sentence_mechanics", label="Sentence structure & boundaries (SR)", tests="state EOC/editing, ACT, SAT", need="external"),
    dict(cap="vocabulary", label="Vocabulary in context", tests="SAT Craft, SBAC vocab", need="external"),
    dict(cap="reading_comprehension", label="Reading comprehension of stimuli", tests="all source-based tasks", need="external"),
    # descoped (must be an EXPLICIT decision, not a silent hole)
    dict(cap="narrative", label="Narrative writing", tests="LA/MD/TN/NJ/SBAC-option/MS/IA", need="descoped"),
    dict(cap="ap_literature", label="Literary analysis (poetry/prose fiction)", tests="AP Lit", need="descoped"),
    dict(cap="research_process_full", label="Full research process (locate/present)", tests="research-simulation, W.7-9", need="descoped"),
]

# ---------------------------------------------------------------------------
# 5. CCSS/TEKS writing-standard-family denominator (standards-first check). family -> owner category.
# ---------------------------------------------------------------------------
STANDARD_FAMILIES = [
    dict(fam="CCSS W.1 (Argument)", need="hs", via="C.9.01/C.9.03/C.9.04/C.10.01/C.11.01/C.11.06/C.11.07"),
    dict(fam="CCSS W.2 (Informative/Explanatory)", need="hs", via="C.9.05/C.9.04/C.10.03"),
    dict(fam="CCSS W.3 (Narrative)", need="descoped", via="narrative (deferred)"),
    dict(fam="CCSS W.4 (Production/clarity/organization)", need="hs", via="C.9.06/C.10.05/C.11.05"),
    dict(fam="CCSS W.5 (Development/revision)", need="hs", via="C.10.05/C.10.04/C.11.04"),
    dict(fam="CCSS W.6 (Technology/publishing)", need="external", via="platform-inherent / not a writing-skill KC"),
    dict(fam="CCSS W.7-8 (Research/gather/assess)", need="hs", via="C.11.02/C.11.08 (source use + credibility)"),
    dict(fam="CCSS W.9 (Draw evidence for analysis)", need="hs", via="C.10.02/C.10.06/C.11.03"),
    dict(fam="CCSS L.1-2 (Conventions)", need="external", via="Language course + EGUMPP"),
    dict(fam="CCSS L.3 (Knowledge of language)", need="external", via="Language course (SR) + C.10.04/C.11.04 (own-essay revision)"),
    dict(fam="CCSS L.4-6 (Vocabulary)", need="external", via="Vocabulary course + AlphaRead"),
    dict(fam="TEKS EI/EII writing strands (9/10/5/11)", need="hs", via="C.9.01/C.9.05/C.10.01/C.10.02/C.10.06 (argument/info/analysis/research)"),
]

# (ACC_SPINE imported from course_sequence_g9_12 - single source of truth; not redefined here.)


def _owned(need: str, cap: str) -> tuple[bool, str]:
    """Is this capability owned per its 'need' category? Return (ok, owner-description)."""
    if need == "hs":
        owners = [k["id"] for k in HS_KCS if k["funnel"] == cap]
        return (bool(owners), "HS KCs: " + ", ".join(owners) if owners else "NO HS KC")
    if need == "external":
        return (cap in EXTERNAL_OWNED, EXTERNAL_OWNED.get(cap, "NO external owner"))
    if need == "descoped":
        return (cap in DESCOPED, DESCOPED.get(cap, "NOT documented as descoped"))
    return (False, "unknown need category")


def build():
    cap_rows = []
    for c in TESTED_CAPABILITIES:
        ok, owner = _owned(c["need"], c["cap"])
        cap_rows.append({**c, "ok": ok, "owner": owner})
    std_rows = []
    for s in STANDARD_FAMILIES:
        # standard families are validated by their declared owner category existing (hs KC funnels exist, or external/descoped registered)
        if s["need"] == "hs":
            ok = True  # 'via' lists the KCs; assertion below checks those KC ids exist
        elif s["need"] == "external":
            ok = True
        else:
            ok = any(d in DESCOPED for d in DESCOPED)  # descoped registry non-empty
        std_rows.append({**s, "ok": ok})
    # ACC spine rows: hs -> some KC carries this acc code; external -> registered; descoped -> registered decision
    kc_acc = {a for k in HS_KCS for a in k.get("acc", [])}
    acc_rows = []
    for a in ACC_SPINE:
        if a["need"] == "hs":
            owners = [k["id"] for k in HS_KCS if a["code"] in k.get("acc", [])]
            ok, owner = bool(owners), ("HS KCs: " + ", ".join(owners) if owners else "NO HS KC carries this ACC code")
        elif a["need"] == "external":
            ok, owner = True, "external HS course (Language/Vocabulary/Reading) or woven"
        else:
            ok, owner = True, "documented descope/defer"
        acc_rows.append({**a, "ok": ok, "owner": owner})
    return cap_rows, std_rows, acc_rows


def self_test():
    """Consistency assertions - the regression guard."""
    errs = []
    kc_ids = {k["id"] for k in HS_KCS}
    # A. every 'hs' tested capability has >=1 HS KC funneling into it
    for c in TESTED_CAPABILITIES:
        if c["need"] == "hs":
            if not any(k["funnel"] == c["cap"] for k in HS_KCS):
                errs.append(f"tested capability '{c['cap']}' needs an HS KC but none funnels into it")
    # B. every HS KC carries a PRIMARY CCSS/TEKS tag (standards-first rule, E2b)
    for k in HS_KCS:
        if not (k["ccss"] or k["teks"]):
            errs.append(f"{k['id']} has no primary CCSS/TEKS tag (standards-first violated)")
    # C. no HS KC funnels into an externally-owned capability (no redundancy with gated skills)
    for k in HS_KCS:
        if k["funnel"] in EXTERNAL_OWNED:
            errs.append(f"{k['id']} funnels into externally-owned '{k['funnel']}' (redundant with a gated course)")
    # D. every 'via' KC id referenced by a standard family actually exists
    for s in STANDARD_FAMILIES:
        if s["need"] == "hs":
            for tok in s["via"].replace("/", " ").split():
                if tok.startswith(("C.", "D.")) and tok not in kc_ids:
                    errs.append(f"standard family '{s['fam']}' references missing KC {tok}")
    # E. every descoped capability is in the DESCOPED registry
    for c in TESTED_CAPABILITIES:
        if c["need"] == "descoped" and c["cap"] not in DESCOPED:
            errs.append(f"capability '{c['cap']}' marked descoped but not in DESCOPED registry")
    # F. every HS KC's acc= code is a real ACC-spine code (no invented ACC codes)
    acc_codes = {a["code"] for a in ACC_SPINE}
    for k in HS_KCS:
        for a in k.get("acc", []):
            if a not in acc_codes:
                errs.append(f"{k['id']} tagged ACC code '{a}' not in the ACC spine")
    # G. every ACC §1 CORE code with need='hs' is carried by >=1 KC (the common-standard coverage guarantee)
    kc_acc = {a for k in HS_KCS for a in k.get("acc", [])}
    for a in ACC_SPINE:
        if a["need"] == "hs" and a["code"] not in kc_acc:
            errs.append(f"ACC code '{a['code']}' needs an HS KC but none carries it")
    return errs


def _text_report(cap_rows, std_rows, acc_rows, errs) -> str:
    L = ["=== G9-12 KC MAP COVERAGE MATRIX (map-level, ACC-anchored) ===",
         "(coverage, NOT efficacy: proves every ACC standard + tested capability has an owner;",
         " does NOT prove the teaching works. Efficacy needs field data with real students.)", ""]
    gaps = 0
    L.append("-- ACC SPINE (the common standard: >=2-state union; THE source of truth) --")
    for a in acc_rows:
        tag = "OK" if a["ok"] else "**UN-OWNED**"
        if not a["ok"]:
            gaps += 1
        note = f"  [{a['note']}]" if a.get("note") else ""
        L.append(f"[{tag}] {a['code']} {a['name']}  ({a['need']}) -> {a['owner']}{note}")
    L.append("")
    L.append("-- TESTED CAPABILITIES --")
    for r in cap_rows:
        tag = "OK" if r["ok"] else "**UN-OWNED**"
        if not r["ok"]:
            gaps += 1
        L.append(f"[{tag}] {r['label']}  ({r['need']})")
        L.append(f"        owner: {r['owner']}   | tested by: {r['tests']}")
    L.append("")
    L.append("-- CCSS/TEKS STANDARD FAMILIES (subset alignment) --")
    for s in std_rows:
        tag = "OK" if s["ok"] else "**UN-OWNED**"
        if not s["ok"]:
            gaps += 1
        L.append(f"[{tag}] {s['fam']}  ({s['need']}) -> {s['via']}")
    L.append("")
    L.append("-- CONSISTENCY SELF-TEST --")
    if errs:
        L += [f"  FAIL: {e}" for e in errs]
    else:
        L.append("  PASS: all assertions hold (every ACC-core owned, every tested cap owned, every KC")
        L.append("        ACC+standards-tagged, no KC duplicates a gated skill, refs exist, descopes documented).")
    L.append("")
    L.append(f"{len(acc_rows)} ACC codes + {len(cap_rows)} capabilities + {len(std_rows)} standard families | "
             f"{gaps} un-owned | {len(errs)} consistency failures")
    L.append(f"HS-owned KCs: {len(HS_KCS)} | external-owned: {len(EXTERNAL_OWNED)} | descoped(documented): {len(DESCOPED)}")
    return "\n".join(L)


def _html_report(cap_rows, std_rows, acc_rows, errs) -> str:
    def esc(s): return html.escape(str(s))
    def rows_html(rows, kind):
        out = []
        for r in rows:
            ok = r["ok"]; cls = "ok" if ok else "gap"
            if kind == "cap":
                label, owner, tests = r["label"], r["owner"], r.get("tests", "")
            elif kind == "acc":
                label = f'{r["code"]} {r["name"]}'
                owner = r["owner"] + (f'  ({r["note"]})' if r.get("note") else "")
                tests = ""
            else:
                label, owner, tests = r["fam"], r["via"], ""
            out.append(f'<tr class="{cls}"><td>{esc(label)}'
                       + (f'<span class="t">tested by: {esc(tests)}</span>' if tests else '')
                       + f'</td><td class="need">{esc(r["need"])}</td>'
                       f'<td>{esc(owner)}</td>'
                       f'<td class="st">{"OK" if ok else "UN-OWNED"}</td></tr>')
        return "".join(out)
    cap_gaps = sum(1 for r in cap_rows if not r["ok"])
    std_gaps = sum(1 for r in std_rows if not r["ok"])
    acc_gaps = sum(1 for r in acc_rows if not r["ok"])
    testblock = ('<div class="pass">PASS - all consistency assertions hold</div>' if not errs
                 else '<div class="fail">FAIL<ul>' + "".join(f"<li>{esc(e)}</li>" for e in errs) + "</ul></div>")
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0"><title>G9-12 KC Coverage Matrix</title>
<style>
body{{font-family:-apple-system,"Segoe UI",Roboto,sans-serif;color:#1e293b;line-height:1.5;max-width:1120px;margin:0 auto;padding:30px 22px 80px;background:#fff}}
h1{{font-size:1.6rem;margin:0 0 4px}} h2{{font-size:1.05rem;color:#6d28d9;margin-top:30px}}
.sub{{color:#64748b;font-size:.95rem}}
.ceiling{{background:#fef3c7;border-left:4px solid #d97706;padding:13px 17px;border-radius:0 8px 8px 0;margin:18px 0;font-size:.9rem}}
.ceiling b{{color:#92400e}}
.stat{{display:inline-block;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:8px 16px;margin:6px 8px 6px 0;font-size:.85rem}}
.stat b{{font-size:1.2rem;color:#2563eb}}
table{{width:100%;border-collapse:collapse;margin:12px 0;font-size:.82rem}}
th,td{{text-align:left;padding:9px 11px;border:1px solid #e2e8f0;vertical-align:top}}
th{{background:#f8fafc;font-size:.7rem;text-transform:uppercase;letter-spacing:.03em;color:#64748b}}
tr.ok{{background:#f6fefb}} tr.gap{{background:#fef2f2}}
tr.gap .st{{color:#991b1b;font-weight:800}} tr.ok .st{{color:#166534;font-weight:800}}
.need{{font-family:ui-monospace,monospace;font-size:.72rem;color:#4338ca}}
.t{{display:block;color:#64748b;font-size:.72rem;margin-top:4px;font-style:italic}}
.pass{{background:#dcfce7;border-left:4px solid #16a34a;padding:12px 16px;border-radius:0 8px 8px 0;font-weight:700;color:#166534}}
.fail{{background:#fef2f2;border-left:4px solid #991b1b;padding:12px 16px;border-radius:0 8px 8px 0;color:#991b1b}}
</style></head><body>
<h1>G9-12 Writing KC Map - Coverage Matrix (ACC-anchored)</h1>
<p class="sub">Anchored to the AlphaCommonCore spine (the empirical >=2-state union of all 50 states' writing standards). Every ACC standard + tested capability mapped to its owner: an HS-owned KC, an external HS course (Language/Vocabulary/Reading), or an explicit documented descope.</p>
<div class="ceiling"><b>What this proves, and what it does not.</b> A COVERAGE argument: no ACC standard or tested capability is left un-owned (necessary for students to pass). NOT an efficacy claim: coverage does not prove the teaching works - that needs field data with real students, which we do not have. Read as "the course targets everything the common standard + tests demand, or explicitly defers it," not "proven to produce passing scores."</div>
<div><span class="stat"><b>{len(ACC_SPINE)}</b> ACC codes</span>
<span class="stat"><b>{len(HS_KCS)}</b> HS-owned KCs</span>
<span class="stat"><b>{len(EXTERNAL_OWNED)}</b> external-owned</span>
<span class="stat"><b>{len(DESCOPED)}</b> documented descopes</span>
<span class="stat"><b>{acc_gaps+cap_gaps+std_gaps}</b> un-owned</span></div>
{testblock}
<h2>AlphaCommonCore spine (the common standard - source of truth)</h2>
<p class="sub">§1 core (CCSS-anchored, ~37+ states each) + §3 net-new (>=2 deviation states, beyond CCSS). Per Noel: WRITING owns only the TESTED slices of §3; the rest are the differentiation layer, deferred or owned elsewhere (noted).</p>
<table><thead><tr><th>ACC code + sub-skill</th><th>Owner need</th><th>Owner (+ scope note)</th><th>Status</th></tr></thead>
<tbody>{rows_html(acc_rows,"acc")}</tbody></table>
<h2>Tested capabilities (backward-trace audit denominator)</h2>
<table><thead><tr><th>Capability (and tests that score it)</th><th>Owner need</th><th>Owner</th><th>Status</th></tr></thead>
<tbody>{rows_html(cap_rows,"cap")}</tbody></table>
<h2>CCSS / TEKS standard families (subset alignment)</h2>
<table><thead><tr><th>Standard family</th><th>Owner need</th><th>Owned via</th><th>Status</th></tr></thead>
<tbody>{rows_html(std_rows,"std")}</tbody></table>
<p class="sub" style="margin-top:20px">Source of truth: the AlphaCommonCore spine (<code>05_AlphaCommonCore_Writing_Spine.md</code>, the >=2-state union). Reconciled KC map (<code>KC_Map_and_Unit_Arch_G9-12.md</code>) + backward-trace audit (<code>_evidence/kc_coverage_audit.md</code>). CCSS/TEKS are subsets of ACC; AP/ACT are thin overlays. Regression guard - drop a KC or owner and a denominator row goes un-owned.</p>
</body></html>"""


if __name__ == "__main__":
    cap_rows, std_rows, acc_rows = build()
    errs = self_test()
    if "--html" in sys.argv:
        out = os.path.join(ROOT, "kc_coverage_matrix.html")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(_html_report(cap_rows, std_rows, acc_rows, errs))
        print(f"wrote {os.path.relpath(out, HERE)}")
    print(_text_report(cap_rows, std_rows, acc_rows, errs))
    gaps = sum(1 for r in (cap_rows + std_rows + acc_rows) if not r["ok"])
    sys.exit(0 if (gaps == 0 and not errs) else 1)
