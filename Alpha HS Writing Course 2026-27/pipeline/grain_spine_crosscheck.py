"""
grain_spine_crosscheck.py - validate each lesson's slot shape against its (class, grain) template.

The AUTHORING TEST for the spine re-architecture (SPINE_DELIBERATION_verdict.md): mirrors the contract's
grain/class rules so the punch-list tool is never weaker than QC. Self-tested, HTML-viewable, exit-coded.
Runs OVER the live lesson banks (per Lesson_Bank_G*/), same discipline as scaffold_crosscheck.py.

  python pipeline/grain_spine_crosscheck.py [--grade G10] [--html out.html] [--exempt-types 4,5]
"""
from __future__ import annotations
import sys, os, glob, re, argparse

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
from lesson_contract import grain, GRAIN_TEMPLATES, UNIT_RANK
from g9_push_dryrun import _load
from mastery_targets_grade import _GRADE_GLOB  # the authoritative LIVE lesson set (what the pipeline loads)


def check_lesson(L) -> list:
    """Return a list of grain-conformance problems (empty = conforms). Mirrors gate_gate_shape +
    the practice grain templates."""
    probs = []
    cls = getattr(L, "lesson_class", "practice")
    kinds = [s.kind for s in L.slots]
    writes = [s for s in L.slots if s.kind == "production_frq"]
    scored_writes = [s for s in writes if getattr(s, "scored", False)]
    if cls == "gate":
        spec = GRAIN_TEMPLATES["gate"]
        bad = spec["banned_kinds"] & set(kinds)
        if bad:
            probs.append(f"gate has banned scaffold {sorted(bad)}")
        if len(scored_writes) > spec["max_scored_writes"]:
            probs.append(f"gate has {len(scored_writes)} scored writes > {spec['max_scored_writes']}")
        if not any(s.role == "TRANSFER" for s in scored_writes):
            probs.append("gate has no TRANSFER (cold, held-out) scored write")
        return probs
    g = grain(L)
    spec = GRAIN_TEMPLATES.get((cls, g))
    if not spec:
        return probs  # grains without a template are unconstrained here
    dcount = sum(1 for k in kinds if k == "discrimination")
    if "discrimination_min" in spec and dcount < spec["discrimination_min"]:
        probs.append(f"{g}: {dcount} discrimination slots < min {spec['discrimination_min']}")
    if "discrimination_max" in spec and dcount > spec["discrimination_max"]:
        probs.append(f"{g}: {dcount} discrimination slots > max {spec['discrimination_max']}")
    # production_writes counts the COMPOSITIONS (INDEPENDENT + TRANSFER production_frq). The SUPPORTED
    # outline/frame is a planning affordance and the diagnosis is self-revision, so neither counts as a "write".
    comp_writes = [s for s in writes if s.role in ("INDEPENDENT", "TRANSFER")]
    lo, hi = spec.get("production_writes", (0, 99))
    if not (lo <= len(comp_writes) <= hi):
        probs.append(f"{g}: {len(comp_writes)} composition writes (INDEPENDENT/TRANSFER) outside [{lo},{hi}]")
    if spec.get("no_transfer_write") and any(s.role == "TRANSFER" for s in writes):
        probs.append(f"{g}: has an in-article TRANSFER write (verdict: route transfer to gate/PP100)")
    # paragraph grain and above: EITHER an own-draft diagnosis OR one coached (feedback-bearing) TRANSFER write
    if spec.get("revision_or_coached_transfer") and UNIT_RANK.get(g, 0) >= UNIT_RANK["paragraph"]:
        has_diag = any(s.kind == "diagnosis_frq" for s in L.slots)
        has_coached_transfer = any(s.role == "TRANSFER" and s.kind == "production_frq" and s.feedback.strip()
                                   for s in L.slots)
        # essay grain forbids the in-article transfer, so only the diagnosis branch is available there.
        if spec.get("no_transfer_write"):
            if not has_diag:
                probs.append(f"{g}: missing an own-draft diagnosis_frq (self-revision)")
        elif not (has_diag or has_coached_transfer):
            probs.append(f"{g}: needs EITHER an own-draft diagnosis_frq OR one coached TRANSFER write")
    return probs


def _iter(grade=None):
    """Iterate the LIVE lessons only (per _GRADE_GLOB, what the pipeline actually loads), NOT stale prototypes."""
    grades = [grade] if grade else ["G9", "G10", "G11", "G12"]
    for gd in grades:
        subdir, pat = _GRADE_GLOB[gd]
        for f in sorted(glob.glob(os.path.join(ROOT, subdir, pat))):
            if "_deprecated" in f:
                continue
            try:
                m = _load(f)
                L = getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0]
            except Exception:
                L = None
            if L:
                yield f, L


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grade")
    ap.add_argument("--html")
    ap.add_argument("--exempt-types", default="", help="comma list of lesson_type ints to report-only (not fail)")
    a = ap.parse_args()
    exempt = {int(x) for x in a.exempt_types.split(",") if x.strip().isdigit()}
    bad = 0
    rows = []
    for f, L in _iter(a.grade):
        probs = check_lesson(L)
        cls = getattr(L, "lesson_class", "practice")
        exempted = getattr(L, "lesson_type", 0) in exempt
        rows.append((L.id, cls, grain(L), probs, exempted))
        if probs:
            tag = "REPORT-ONLY" if exempted else "FAIL"
            print(f"{tag} {L.id} [{cls}/{grain(L)}]: {probs}")
            if not exempted:
                bad += 1
    print(f"\ngrain-spine crosscheck: {sum(1 for r in rows if not r[3])}/{len(rows)} conform"
          f"{f' ({bad} hard failures)' if bad else ''}")
    if a.html:
        body = "".join(f"<li>{i} [{c}/{g}] {'OK' if not p else ('(exempt) ' if ex else '')+str(p)}</li>"
                       for i, c, g, p, ex in rows)
        open(a.html, "w", encoding="utf-8").write(f"<h1>Grain-spine crosscheck</h1><ul>{body}</ul>")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
