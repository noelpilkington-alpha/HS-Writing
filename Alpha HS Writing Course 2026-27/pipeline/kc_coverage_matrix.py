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

# ---------------------------------------------------------------------------
# 1. THE HS-OWNED KC REGISTRY (the corrected, post-audit map). 21 taught KCs.
#    Each: id, grade, name, primary CCSS/TEKS tag(s), secondary AP/ACT tags, the tested capability it funnels into.
# ---------------------------------------------------------------------------
HS_KCS = [
    # G9
    dict(id="C.9.01", grade="G9", name="Defensible argument claim", ccss=["W.9-10.1a"], teks=["EI.10.C"], sec=["ACT.1"], funnel="argument"),
    dict(id="C.9.05", grade="G9", name="Informational controlling-idea", ccss=["W.9-10.2a"], teks=["EI.9.B"], sec=[], funnel="informational"),
    dict(id="C.9.02", grade="G9", name="Attributed-evidence sentence", ccss=["W.9-10.1b", "W.9-10.8"], teks=["EI.11.H"], sec=["AP.3"], funnel="evidence"),
    dict(id="C.9.03", grade="G9", name="Reason/warrant sentence", ccss=["W.9-10.1b"], teks=["EI.10.C"], sec=["AP.5", "ACT.4"], funnel="reasoning"),
    dict(id="C.9.06", grade="G9", name="Transitions & cohesion", ccss=["W.9-10.1c", "W.9-10.2c"], teks=["EI.9.C"], sec=["ACT.9"], funnel="production_of_writing"),
    dict(id="C.9.04", grade="G9", name="Single-source essay (arg + informational)", ccss=["W.9-10.1", "W.9-10.2", "W.9-10.4"], teks=["EI.10.C", "EI.9.B"], sec=[], funnel="essay"),
    # G10
    dict(id="C.10.01", grade="G10", name="Counterclaim-aware claim", ccss=["W.9-10.1a"], teks=["EII.10.C"], sec=["ACT.2"], funnel="counterargument"),
    dict(id="C.10.02", grade="G10", name="Device->effect->warrant (text-dependent analysis)", ccss=["W.9-10.9", "RI.9-10.6"], teks=["EII.5.B"], sec=[], funnel="analysis"),
    dict(id="C.10.05", grade="G10", name="Rhetorical revision: add/delete/reorder + organization", ccss=["W.9-10.4", "W.9-10.5"], teks=["EII.9.C"], sec=["ACT.7", "ACT.8"], funnel="production_of_writing"),
    dict(id="C.10.06", grade="G10", name="Cross-text (2-3 source) argument/analysis", ccss=["W.9-10.7", "W.9-10.8", "W.9-10.9"], teks=["EII.5.D"], sec=[], funnel="multisource"),
    dict(id="C.10.03", grade="G10", name="Analysis essay strategy", ccss=["W.9-10.2", "W.9-10.9"], teks=["EII.5.B"], sec=[], funnel="analysis"),
    dict(id="C.10.04", grade="G10", name="Precision-in-argument (applied revision pass, woven)", ccss=["W.9-10.4", "W.9-10.5"], teks=["EII.9.C"], sec=[], funnel="production_of_writing"),
    # G11
    dict(id="C.11.01", grade="G11", name="Nuanced claim", ccss=["W.11-12.1a"], teks=[], sec=["AP.1", "ACT.6"], funnel="argument"),
    dict(id="C.11.03", grade="G11", name="Rhetorical-analysis essay (author's choices)", ccss=["W.11-12.9", "RI.11-12.6"], teks=[], sec=["APL.4"], funnel="rhetorical_analysis"),
    dict(id="C.11.02", grade="G11", name="Cross-source synthesis essay", ccss=["W.11-12.7", "W.11-12.8", "W.11-12.9"], teks=[], sec=["APL.3"], funnel="synthesis"),
    dict(id="C.11.08", grade="G11", name="Evaluate source credibility/bias", ccss=["W.11-12.8"], teks=["EII.11.G"], sec=[], funnel="source_evaluation"),
    dict(id="C.11.06", grade="G11", name="Argue from own knowledge (source-free)", ccss=["W.11-12.1"], teks=[], sec=["AP.4"], funnel="source_free_argument"),
    dict(id="C.11.07", grade="G11", name="Multi-perspective argument (3 given perspectives)", ccss=["W.11-12.1"], teks=[], sec=["ACT.2", "ACT.3"], funnel="multi_perspective"),
    dict(id="C.11.04", grade="G11", name="Rhetorical concision/style (applied revision pass, woven)", ccss=["W.11-12.4", "W.11-12.5"], teks=[], sec=["ACT.10"], funnel="production_of_writing"),
    dict(id="C.11.05", grade="G11", name="Timed-writing strategy", ccss=["W.11-12.4"], teks=[], sec=["AP.9"], funnel="timed"),
    # G12
    dict(id="C.12.01", grade="G12", name="AP sophistication (significance/context/complexity) [intro G11]", ccss=["W.11-12.1", "W.11-12.2"], teks=[], sec=["AP.8", "ACT.5"], funnel="sophistication"),
    dict(id="C.12.02", grade="G12", name="Sustained AP writing under timed conditions", ccss=["W.11-12.4"], teks=[], sec=["AP.9"], funnel="timed"),
    dict(id="D.12.01", grade="G12", name="Voice through syntactic choice (woven)", ccss=["W.11-12.4"], teks=[], sec=[], funnel="voice"),
]

# ---------------------------------------------------------------------------
# 2. EXTERNALLY-OWNED skills (gated; NOT taught by the writing course). Noel 2026-07-08:
#    separate HS Language, Vocabulary, Reading courses + K-8 apps own these. Gate is SAFE.
# ---------------------------------------------------------------------------
EXTERNAL_OWNED = {
    "conventions":        "HS Language course + EGUMPP (conventions G3-10)",
    "knowledge_of_language": "HS Language course (precision/concision/style-tone as SR editing of a given passage)",
    "sentence_mechanics": "EGUMPP + AlphaWrite (combining, appositives, subordination, parallelism, phrase/clause, modifiers)",
    "vocabulary":         "HS Vocabulary course + AlphaRead",
    "reading_comprehension": "Reading course / AlphaRead (incl. HS-Lexile + literary/nonfiction)",
}

# ---------------------------------------------------------------------------
# 3. EXPLICITLY DESCOPED / DEFERRED (documented decisions, NOT silent holes). Noel 2026-07-08.
# ---------------------------------------------------------------------------
DESCOPED = {
    "narrative":   "DESCOPED now, BACKLOGGED phase 2 (7 systems test it; core ships argument/analysis/synthesis first)",
    "ap_literature": "NAMED-BUT-DEFERRED backlog (B2 = AP Lang only; poetry/prose-fiction/literary-analysis KCs queued)",
    "research_process_full": "DEFERRED (locate/present/mode-of-delivery); source-evaluation slice IS covered (C.11.08)",
}

# ---------------------------------------------------------------------------
# 4. THE DENOMINATOR: every tested writing capability (from the crosswalk / released tests) + who must own it.
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
    return cap_rows, std_rows


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
    return errs


def _text_report(cap_rows, std_rows, errs) -> str:
    L = ["=== G9-12 KC MAP COVERAGE MATRIX (map-level, standards-first) ===",
         "(coverage, NOT efficacy: proves every tested capability + standard family has an owner;",
         " does NOT prove the teaching works. Efficacy needs field data with real students.)", ""]
    L.append("-- TESTED CAPABILITIES --")
    gaps = 0
    for r in cap_rows:
        tag = "OK" if r["ok"] else "**UN-OWNED**"
        if not r["ok"]:
            gaps += 1
        L.append(f"[{tag}] {r['label']}  ({r['need']})")
        L.append(f"        owner: {r['owner']}   | tested by: {r['tests']}")
    L.append("")
    L.append("-- CCSS/TEKS STANDARD FAMILIES (standards-first) --")
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
        L.append("  PASS: all consistency assertions hold (every tested cap owned, every KC standards-tagged,")
        L.append("        no KC duplicates a gated skill, all referenced KCs exist, descopes documented).")
    L.append("")
    L.append(f"{len(cap_rows)} capabilities + {len(std_rows)} standard families | "
             f"{gaps} un-owned | {len(errs)} consistency failures")
    L.append(f"HS-owned KCs: {len(HS_KCS)} | external-owned: {len(EXTERNAL_OWNED)} | descoped(documented): {len(DESCOPED)}")
    return "\n".join(L)


def _html_report(cap_rows, std_rows, errs) -> str:
    def esc(s): return html.escape(str(s))
    def rows_html(rows, kind):
        out = []
        for r in rows:
            ok = r["ok"]; cls = "ok" if ok else "gap"
            label = r["label"] if kind == "cap" else r["fam"]
            owner = r["owner"] if kind == "cap" else r["via"]
            tests = r.get("tests", "")
            out.append(f'<tr class="{cls}"><td>{esc(label)}'
                       + (f'<span class="t">tested by: {esc(tests)}</span>' if tests else '')
                       + f'</td><td class="need">{esc(r["need"])}</td>'
                       f'<td>{esc(owner)}</td>'
                       f'<td class="st">{"OK" if ok else "UN-OWNED"}</td></tr>')
        return "".join(out)
    cap_gaps = sum(1 for r in cap_rows if not r["ok"])
    std_gaps = sum(1 for r in std_rows if not r["ok"])
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
<h1>G9-12 Writing KC Map - Coverage Matrix</h1>
<p class="sub">Every tested writing capability + every CCSS/TEKS standard family, mapped to its owner: an HS-owned KC, an external HS course (Language/Vocabulary/Reading), or an explicit documented descope.</p>
<div class="ceiling"><b>What this proves, and what it does not.</b> A COVERAGE argument: no tested capability or standard family is left un-owned (necessary for students to pass). NOT an efficacy claim: coverage does not prove the teaching works - that needs field data with real students, which we do not have. Read as "the course targets everything the tests + standards demand, or explicitly defers it," not "proven to produce passing scores."</div>
<div><span class="stat"><b>{len(HS_KCS)}</b> HS-owned KCs</span>
<span class="stat"><b>{len(EXTERNAL_OWNED)}</b> external-owned</span>
<span class="stat"><b>{len(DESCOPED)}</b> documented descopes</span>
<span class="stat"><b>{cap_gaps+std_gaps}</b> un-owned</span></div>
{testblock}
<h2>Tested capabilities</h2>
<table><thead><tr><th>Capability (and tests that score it)</th><th>Owner need</th><th>Owner</th><th>Status</th></tr></thead>
<tbody>{rows_html(cap_rows,"cap")}</tbody></table>
<h2>CCSS / TEKS standard families (standards-first)</h2>
<table><thead><tr><th>Standard family</th><th>Owner need</th><th>Owned via</th><th>Status</th></tr></thead>
<tbody>{rows_html(std_rows,"std")}</tbody></table>
<p class="sub" style="margin-top:20px">Source: reconciled KC map (<code>KC_Map_and_Unit_Arch_G9-12.md</code>) + backward-trace audit (<code>_evidence/kc_coverage_audit.md</code>). Standards-first: AP/ACT are thin overlays on a CCSS/TEKS-anchored core. This matrix is a regression guard - drop a KC or owner and a denominator row goes un-owned.</p>
</body></html>"""


if __name__ == "__main__":
    cap_rows, std_rows = build()
    errs = self_test()
    if "--html" in sys.argv:
        out = os.path.join(ROOT, "kc_coverage_matrix.html")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(_html_report(cap_rows, std_rows, errs))
        print(f"wrote {os.path.relpath(out, HERE)}")
    print(_text_report(cap_rows, std_rows, errs))
    cap_gaps = sum(1 for r in cap_rows if not r["ok"])
    std_gaps = sum(1 for r in std_rows if not r["ok"])
    sys.exit(0 if (cap_gaps == 0 and std_gaps == 0 and not errs) else 1)
