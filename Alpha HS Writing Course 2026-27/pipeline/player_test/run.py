"""
player_test/run.py  -  the student-agent course evaluator. Drives the live LearnWith player against each
lesson, runs the player checks (video loads, One-Beat pauses, answerable, content renders) + the grading check
(submit an exemplar response to the lesson's wired grader URL, assert a real score), collects Findings, writes
a JSON + markdown scorecard.

Read-only against the courses: it navigates + clicks WITHIN a lesson (student actions); it never mutates the
course tree, never touches the OneRoster/QTI push APIs. Checkpointed + resumable (per-lesson) and sample-capable
(--limit N) because a full 101-lesson browser run is long and the CLI has a per-call wall-clock ceiling.

Usage:
  python -m player_test.run G9                      # full G9
  python -m player_test.run G9 --limit 3            # first 3 G9 lessons (smoke)
  python -m player_test.run G9 --lessons l01,l07    # specific lessons
  python -m player_test.run G9 --no-browser         # expectations + grading only (no player)
  python -m player_test.run G9 --grading-only       # only the grading-outcome check
Outputs: C:/tmp/player_eval/<grade>_findings.json  +  <grade>_report.md  + screenshots/
"""
from __future__ import annotations
import os, sys, json, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.dirname(HERE)
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)

from player_test.expectations import grade_expectations
from player_test.driver import Driver
from player_test import checks as C
from player_test.grading_check import check_grading
from player_test.tree_check import check_lesson_tree
from player_test.report import markdown
import render_course_preview_grade as R

OUT = "C:/tmp/player_eval"


def _session():
    import course_assemble_v3_1 as A
    A.load_env()
    import requests
    from g9_push_live import get_token
    s = requests.Session()
    s.headers.update({"Authorization": f"Bearer {get_token()}"})
    return s


def run_lesson(driver, exp, shot_dir, session, do_browser=True, do_grading=True, do_tree=True) -> list:
    findings = []
    if do_tree:
        findings += check_lesson_tree(exp, session)   # OneRoster lesson-tree integrity (stale/extra CRs)
    if do_browser and driver.available:
        ok = driver.goto(exp["player_url"], timeout=90)
        driver.wait_ms(4000)   # let the SPA render the lesson
        if not ok:
            findings.append(C.Finding(exp["lesson_id"], exp["grade"], "player_loads", "fail",
                                      "player renders the lesson", "navigation failed / non-200"))
        else:
            findings += C.check_content_renders(driver, exp, shot_dir)
            findings += C.check_video_loads(driver, exp, shot_dir)
            findings += C.check_one_beat_pauses(driver, exp, shot_dir)
            findings += C.check_one_beat_answerable(driver, exp, shot_dir)
    elif do_browser:
        findings.append(C.Finding(exp["lesson_id"], exp["grade"], "player", "skipped",
                                  note="browser (browse daemon) unavailable"))
    if do_grading:
        findings += check_grading(exp, session)
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("grade", choices=["G9", "G10", "G11", "G12"])
    ap.add_argument("--limit", type=int, default=0, help="only the first N lessons")
    ap.add_argument("--lessons", default="", help="comma list of slugs, e.g. l01,l07")
    ap.add_argument("--no-browser", action="store_true")
    ap.add_argument("--grading-only", action="store_true")
    ap.add_argument("--tree-only", action="store_true", help="only the OneRoster lesson-tree integrity check")
    ap.add_argument("--base-url", default=R.DEFAULT_BASE)
    args = ap.parse_args()
    g = args.grade
    os.makedirs(OUT, exist_ok=True)
    shot_dir = os.path.join(OUT, "screenshots")
    os.makedirs(shot_dir, exist_ok=True)

    exps = grade_expectations(g, base_url=args.base_url)
    total = len(exps)
    if args.lessons:
        want = {s.strip().lower() for s in args.lessons.split(",")}
        exps = [e for e in exps if R.slug(g, e["n"]).split("/")[-1] in want]
    if args.limit:
        exps = exps[:args.limit]

    do_browser = not (args.no_browser or args.grading_only or args.tree_only)
    do_grading = not args.tree_only
    do_tree = not args.grading_only   # tree runs by default; --grading-only skips it, --tree-only keeps only it
    driver = Driver()
    session = _session()

    cp_path = os.path.join(OUT, f"{g}_findings.json")
    done = json.load(open(cp_path)) if os.path.exists(cp_path) else {}
    for e in exps:
        lid = e["lesson_id"]
        fs = run_lesson(driver, e, shot_dir, session, do_browser=do_browser, do_grading=do_grading, do_tree=do_tree)
        done[lid] = [f.dict() for f in fs]
        json.dump(done, open(cp_path, "w"), indent=1)   # checkpoint after each lesson
        sev = [f.severity for f in fs]
        print(f"  {g} {lid}: {sev.count('pass')}P {sev.count('warn')}W {sev.count('fail')}F "
              f"{sev.count('skipped')}S", flush=True)

    all_findings = [f for fs in done.values() for f in fs]
    meta = {"base_url": args.base_url, "lessons_run": len(exps), "lessons_total": total,
            "sample": bool(args.limit or args.lessons), "browser": driver.available and do_browser}
    md = markdown(g, all_findings, meta)
    open(os.path.join(OUT, f"{g}_report.md"), "w", encoding="utf-8").write(md)
    fails = sum(1 for f in all_findings if f["severity"] == "fail")
    print(f"\n{g}: {len(all_findings)} findings | {fails} fail. Report -> {OUT}/{g}_report.md")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
