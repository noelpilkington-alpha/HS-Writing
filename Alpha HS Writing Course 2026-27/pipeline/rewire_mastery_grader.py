"""
rewire_mastery_grader.py  -  PUT-update the LIVE per-lesson MASTERY-FRQ items with the current grader wiring.

course_push_mastery_v3_1.py POSTs (create); it treats an already-live item as a 409 no-op ("exists
idempotent"), so it CANNOT change an item that is already live. The 47 G11/G12 mastery FRQs are live but
were wired with the deprecated rc.ap rubric (GRADER_WIRING_FINDINGS Defect 2). This module PUTs the SAME
payload course_push_mastery_v3_1.build_plan builds (so content stays byte-identical, incl. the PP100 prompt
override) but as a FULL-REPLACE PUT, so the new rc.4trait rubricBlock + baked ?mode= URL land on the live item.

PUT is a full replace on this API (timeback RULE 3) - the payload build here is IDENTICAL to build_plan's,
so nothing but the grader wiring changes.

Usage:
  python pipeline/rewire_mastery_grader.py G11 https://hs-writing-grading.onrender.com            # DRY
  python pipeline/rewire_mastery_grader.py G11 https://hs-writing-grading.onrender.com --live      # PUT
  python pipeline/rewire_mastery_grader.py G11,G12 <url> --live                                    # multi
"""
from __future__ import annotations
import os, sys, time

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)

from course_push_mastery_v3_1 import build_plan, load_env
from g9_push_live import get_token, QTI_BASE
from g9_wire_grader import normalize_grader_url

RETRY_ON = {429, 500, 502, 503, 504}
BACKOFF = [5, 15, 30]


def _put(session, url, body):
    import requests
    for attempt in range(4):
        try:
            r = session.put(url, json=body, timeout=90)
        except requests.RequestException as e:
            if attempt < 3:
                time.sleep(BACKOFF[attempt]); continue
            return False, 0, f"network error: {e}"
        if r.status_code in (200, 201):
            return True, r.status_code, "rewired"
        if r.status_code in RETRY_ON and attempt < 3:
            time.sleep(BACKOFF[attempt]); continue
        return False, r.status_code, (r.text or "")[:300]
    return False, 0, "exhausted retries"


def rewire_grade(grade, grader_url, live):
    """PUT every MASTERY-FRQ item for a grade with the current build_plan payload (rc.4trait + baked mode)."""
    plan, skipped = build_plan(grade, grader_url)
    frqs = [(oid, body) for kind, oid, url, body in plan if kind == "item"]
    print(f"  {grade}: {len(frqs)} mastery FRQ items to PUT-rewire"
          + (f"  (skipped no-INDEPENDENT: {skipped})" if skipped else ""))
    if not live:
        # DRY: show the baked grader URL + rubricBlock kind for each, so the plan is auditable pre-PUT.
        for oid, body in frqs:
            defn = body["responseProcessing"]["customOperator"]["definition"]
            blk = body["rubricBlock"]["content"]
            which = ("rc.4trait" if "content_analysis" in blk else
                     "sentence-grain" if ("Skill Application" in blk or "Answer Quality" in blk) else
                     "paragraph-grain" if "Ideas &amp; Content" in blk else
                     "rc.staar" if "STAAR" in blk else "??")
            tail = "/score" + defn.split("/score")[-1] if "/score" in defn else defn
            print(f"    {oid:44s} {tail:44s} block={which}")
        return True, len(frqs), 0
    load_env()
    import requests
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {get_token()}", "Content-Type": "application/json"})
    ok = fail = 0
    for oid, body in frqs:
        good, status, detail = _put(session, f"{QTI_BASE}/assessment-items/{oid}", body)
        if good:
            ok += 1
        else:
            fail += 1
            print(f"    FAIL [{status}] {oid}: {detail}")
    print(f"  {grade}: rewired {ok}, failed {fail}.")
    return fail == 0, ok, fail


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print("usage: rewire_mastery_grader.py <G11|G12|G11,G12> <grader-base-url> [--live]")
        return 2
    grades = [g.strip().upper() for g in args[0].split(",")]
    grader_url = normalize_grader_url(args[1])
    live = "--live" in args
    print(f"MASTERY grader re-wire (PUT)  grader = {grader_url}  {'LIVE' if live else 'DRY'}")
    allok = True; total_ok = total_fail = 0
    for g in grades:
        good, ok, fail = rewire_grade(g, grader_url, live)
        allok = good and allok; total_ok += ok; total_fail += fail
    if live:
        print(f"\nTOTAL: rewired {total_ok}, failed {total_fail}.")
    else:
        print("\nDRY mode. No network call made. Re-run with --live to PUT.")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
