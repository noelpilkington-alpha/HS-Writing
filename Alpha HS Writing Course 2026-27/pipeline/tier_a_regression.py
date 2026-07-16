"""
tier_a_regression.py  -  the ONE deterministic Tier-A gate runner (all offline gates, per lesson).

WHY: the hardening this session added four new offline gates (render-fidelity in render_qc, register,
mastery-genre/DOK, structural-item) that lived in separate modules and were never composed into a
single course-wide pass. A defect only stays caught if EVERY run checks EVERY gate. This runner is
that single pass: for every live lesson in a grade it runs

  1. the 25 deterministic CONTRACT gates            (lesson_contract.qc_lesson)
  2. RENDER-FIDELITY on the actually-rendered html   (gated_reading.render_qc, WITH the source lesson
     so the option-integrity choices[] cross-check is active - the two live callers omit it)
  3. REGISTER / credibility                          (register_gate.check_register)
  4. MASTERY GENRE-MATCH + Webb DOK                   (mastery_genre_gate.check_mastery_alignment)

and for every STIMULUS a lesson binds, the 10 stimulus-contract gates (including the new passage
register gate). It emits a per-lesson RECEIPT (every gate + pass/fail + one-line detail) and a course
tally. Exit 0 iff every lesson and every bound stimulus is clean.

This is deterministic and offline (no LLM, no network) - it is the Tier-A floor the LLM judges (Tier
B) sit on top of. Run it before any push, and as the Tier-A checkpoint.

Run:
  python pipeline/tier_a_regression.py                # all grades, summary
  python pipeline/tier_a_regression.py G9             # one grade
  python pipeline/tier_a_regression.py G9 --receipts  # one grade, full per-lesson receipts
  python pipeline/tier_a_regression.py --json out.json
"""
from __future__ import annotations
import os, sys, glob, json, argparse

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)

from g9_push_dryrun import _load, STIM                                   # noqa: E402
import lesson_contract as LC                                             # noqa: E402
import stimulus_contract as SC                                           # noqa: E402
from gated_reading import build_lesson_html, render_qc                   # noqa: E402
from register_gate import check_register                                 # noqa: E402
from mastery_genre_gate import check_mastery_alignment                   # noqa: E402
from mastery_targets_grade import _GRADE_GLOB                            # noqa: E402

BASE = "https://example.invalid/preview"   # render needs a base_url; content is what we QC, not the URL

# DECLARED EXCEPTION (expected_exceptions doctrine, applied to the stimulus contract):
# family="issue_frame" stimuli are SHORT orientation cards (~50-130 words, no fact table, qualitative)
# bound to claim-tier lessons - deliberately NOT full source passages. Per commit f9944e0, a frame
# "fails standalone stimulus QC on word-count/Lexile/facts by design; issue_frames are floor/Lexile-
# exempt." The push pipeline ships them regardless. So for an issue_frame the source-PASSAGE gates
# (word floor, fact table, citable facts, source_config family whitelist, Lexile band) are N/A by
# design; the gates that DO apply - provenance, content-appropriateness, bucket_profile, and REGISTER
# (the childish-opener check, the exact defect Noel flagged on a frame) - stay enforced.
# REVERSE_IF: issue_frame is added to the stimulus_contract Family type with its own passage-size band
# and fact rules, at which point these should be checked against that band instead of exempted.
_ISSUE_FRAME_NA_GATES = {"structure", "fact_sources", "citable_facts", "source_config", "lexile"}


def _lessons(grade):
    subdir, pat = _GRADE_GLOB[grade]
    for f in sorted(glob.glob(os.path.join(ROOT, subdir, pat))):
        if "_deprecated" in f:
            continue
        m = _load(f)
        L = (getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0]) if m else None
        if L:
            yield f, L


def _bound_stimulus_ids(L):
    """Stimulus ids this lesson references from a slot (so we QC exactly the sources it ships)."""
    ids = []
    for s in getattr(L, "slots", []) or []:
        ref = getattr(s, "ref", "") or ""
        if ref and ref in STIM and ref not in ids:
            ids.append(ref)
    return ids


def audit_lesson(L, grade) -> dict:
    """Run every deterministic gate on one lesson + its bound stimuli. Returns a receipt dict."""
    receipt = {"lesson_id": getattr(L, "id", "?"), "title": getattr(L, "title", ""),
               "gates": {}, "blockers": []}

    # 1. contract gates (25)
    qc = LC.qc_lesson(L)
    for name, g in qc["gates"].items():
        receipt["gates"][f"contract:{name}"] = {"passed": g["passed"], "detail": g["detail"]}
        if not g["passed"]:
            receipt["blockers"].append(f"contract:{name}: {g['detail']}")

    # 2. render-fidelity on the rendered artifact (WITH source lesson -> option-integrity cross-check on)
    try:
        html_str, checkpoints = build_lesson_html(L, base_url=BASE)
        rprobs = render_qc(html_str, checkpoints, lessons=L)
    except Exception as e:
        rprobs = [f"render/render_qc crashed: {e!r}"]
    receipt["gates"]["render:fidelity"] = {"passed": not rprobs,
                                           "detail": "clean" if not rprobs else "; ".join(rprobs)}
    for p in rprobs:
        receipt["blockers"].append(f"render:{p}")

    # 3. register / credibility (lesson slots)
    rok, rflags = check_register(L)
    receipt["gates"]["register"] = {"passed": rok, "detail": "clean" if rok else "; ".join(rflags)}
    for fl in rflags:
        receipt["blockers"].append(f"register:{fl}")

    # 4. mastery genre-match + Webb DOK
    mok, mprobs = check_mastery_alignment(L, grade)
    receipt["gates"]["mastery_genre"] = {"passed": mok, "detail": "clean" if mok else "; ".join(mprobs)}
    for p in mprobs:
        receipt["blockers"].append(f"mastery_genre:{p}")

    # 5. stimulus-contract gates for every bound source
    for sid in _bound_stimulus_ids(L):
        s = STIM.get(sid)
        if s is None:
            continue
        is_frame = (getattr(s, "family", "") == "issue_frame")
        sqc = SC.qc_stimulus(s)
        for name, g in sqc["gates"].items():
            key = f"stimulus[{sid}]:{name}"
            na = is_frame and name in _ISSUE_FRAME_NA_GATES
            if na:
                # by-design N/A for an issue_frame: record it, but do NOT count it as a blocker
                receipt["gates"][key] = {"passed": True, "detail": "n/a (issue_frame: " + g["detail"][:60] + ")"}
                continue
            receipt["gates"][key] = {"passed": g["passed"], "detail": g["detail"]}
            # equivalent_form UNCERTIFIED is a deliberate pass (no student writing yet) - already returns
            # True, so it never lands here as a blocker.
            if not g["passed"]:
                receipt["blockers"].append(f"{key}: {g['detail']}")

    receipt["passed"] = not receipt["blockers"]
    return receipt


def run_grade(grade) -> list:
    return [audit_lesson(L, grade) for _f, L in _lessons(grade)]


def run_all() -> dict:
    return {g: run_grade(g) for g in ("G9", "G10", "G11", "G12")}


def _print_receipt(r, full=False):
    mark = "PASS" if r["passed"] else "FAIL"
    print(f"  [{mark}] {r['lesson_id']:26} {len(r['blockers'])} blocker(s)")
    if full:
        for name, g in r["gates"].items():
            gm = "ok  " if g["passed"] else "FAIL"
            print(f"        {gm} {name}: {g['detail'][:90]}")
    elif r["blockers"]:
        for b in r["blockers"]:
            print(f"        !! {b[:120]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("grade", nargs="?", default="all", help="G9|G10|G11|G12|all")
    ap.add_argument("--receipts", action="store_true", help="print the full per-gate receipt for every lesson")
    ap.add_argument("--json", default="", help="write the full receipts to this JSON path")
    args = ap.parse_args()
    grades = ["G9", "G10", "G11", "G12"] if args.grade.lower() == "all" else [args.grade.upper()]

    print("=== TIER-A DETERMINISTIC REGRESSION (contract + render + register + mastery-genre + stimuli) ===")
    all_results, total_fail = {}, 0
    for g in grades:
        results = run_grade(g)
        all_results[g] = results
        nfail = sum(1 for r in results if not r["passed"])
        total_fail += nfail
        print(f"\n{g}: {len(results)} lessons  |  {len(results) - nfail} PASS  |  {nfail} FAIL")
        for r in results:
            if args.receipts or not r["passed"]:
                _print_receipt(r, full=args.receipts)
    n = sum(len(v) for v in all_results.values())
    print(f"\n=== TIER-A: {n - total_fail}/{n} lessons clean across {', '.join(grades)} "
          f"({total_fail} with blockers) ===")
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(all_results, fh, indent=1, ensure_ascii=False)
        print(f"(receipts written to {args.json})")
    return 0 if total_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
