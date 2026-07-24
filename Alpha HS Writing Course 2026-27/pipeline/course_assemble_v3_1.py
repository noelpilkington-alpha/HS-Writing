"""
course_assemble_v3_1.py  -  GRADE-GENERALIZED OneRoster assembly for the V3.1 gated-reading course structure.

Generalizes g9_assemble_v3_1.py to G9-G12. Each lesson = a LEAF topic component carrying TWO ordered sibling
component-resources:
  1. ARTICLE  (kind=text)   -> the hosted gated-reading lesson.html on the Vercel stable alias (the SAME URL the
                              LearnWith player renders today: teach + video + One-Beat + gated MCQ + write tasks).
  2. PP100    (powerpath-100) -> the lesson's production FRQ as a single-item QTI assessment-test, external-grader
                              scored to the >=90 test-out. (Grader wired AFTER push, when deployed.)

WHY A NEW FILE (not an edit of g9_assemble_v3_1.py): that G9-only file had two stale assumptions that would
misroute a live push -- (a) it pointed articles at a DEAD Vercel layout (l01v/ , v3_1/  -> 404); the live
lessons are grade-namespaced at <grade>/l{NN}/lesson.html (verified 200 for all 4 grades). (b) its hardcoded
UNITS predated the G9 counterargument unit (G9 is now 29 lessons / 5 units). This module instead REUSES the
canonical lesson selection + slug + unit grouping from render_course_preview_grade (the exact thing deployed
and tested), so the course tree can never drift from what is hosted.

Course ids (G9 REUSES its id so the push REPLACES the old per-item build; title stays "AlphaWriting G9"):
  G9  -> hs-writing-g9-2026     "AlphaWriting G9"
  G10 -> hs-writing-g10-2026    "AlphaWriting G10"
  G11 -> hs-writing-g11-2026    "AlphaWriting G11"
  G12 -> hs-writing-g12-2026    "AlphaWriting G12"

Gotchas honored (verified live; see g9_assemble_v3_1.py + gated-reading-runbook):
- resources endpoint needs a TRAILING SLASH.
- lessonType in RESOURCE metadata -> 500; put it on the COMPONENT-RESOURCE link.
- Article topic/leaf metadata must be {} (NOT quiz/assessment-flagged) or the student runtime filters it out.
- A leaf component carries the CRs; units carry topics; never mix.
- publishStatus 'published' + timebackVisible True make the course student-visible.
- POST to the collection (PUT is update-only, 404 on new ids); 409 = exists = idempotent.

Usage:
  python pipeline/course_assemble_v3_1.py G9                 # DRY: build + print the plan for one grade
  python pipeline/course_assemble_v3_1.py all                # DRY: all four grades
  python pipeline/course_assemble_v3_1.py G9 --live          # LIVE: create/replace the course (needs creds)
  python pipeline/course_assemble_v3_1.py all --live         # LIVE: all four
  python pipeline/course_assemble_v3_1.py G9 --base-url <alias>   # override the Vercel article host alias
"""
from __future__ import annotations
import os, sys, re, json, time, urllib.parse

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
from xp_allocation import expected_xp
import render_course_preview_grade as R   # canonical lesson selection + slug + unit grouping (what is deployed)
import mastery_forms as MF
from mastery_targets_grade import _authored   # per-grade MASTERY map (for PP100 form-bank depth)

ONEROSTER = "https://api.alpha-1edtech.ai"
QTI_BASE = "https://qti.alpha-1edtech.ai/api"
ROSTER = f"{ONEROSTER}/ims/oneroster/rostering/v1p2"
RES = f"{ONEROSTER}/ims/oneroster/resources/v1p2/resources/"          # trailing slash REQUIRED
COMPRES = f"{ROSTER}/courses/component-resources"
COMPONENTS = f"{ROSTER}/courses/components"
COURSES = f"{ROSTER}/courses"
ORG_ID = "a6d57e8d-080e-4c49-80b8-b122d447b70e"   # Alpha Denver (verified live 2026-07-12); fallback in _push
LEARNWITH = "https://content.platform.learnwith.ai/player"
DEFAULT_BASE = "https://verceldeploy-five-tan.vercel.app"
RETRY_ON = {429, 500, 502, 503, 504}
BACKOFF = [5, 15, 30]

GRADES = ("G9", "G10", "G11", "G12")
COURSE_ID = {g: f"hs-writing-{g.lower()}-2026" for g in GRADES}
COURSE_TITLE = {g: f"AlphaWriting {g}" for g in GRADES}
GRADE_NUM = {"G9": "09", "G10": "10", "G11": "11", "G12": "12"}


def load_env():
    envp = os.path.join(ROOT, "..", ".env")
    if os.path.exists(envp):
        for line in open(envp, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def mastery_test_id(L):
    """The single-item mastery assessment-test id the PP100 resource points at (distinct from the teaching test)."""
    return f"{L.id}-MASTERY"


def article_content_url(grade, n, base_url):
    """The hosted gated-reading lesson.html for (grade, lesson n): the grade-namespaced layout that is actually
    deployed (verified 200 all 4 grades). R.slug -> '<grade>/l{NN}'."""
    return f"{base_url}/{R.slug(grade, n)}/lesson.html"


def article_player_url(grade, n, L, base_url):
    q = urllib.parse.urlencode({"contentUrl": article_content_url(grade, n, base_url),
                                "contentId": L.id, "theme": "indigo", "ttsEnabled": "true"})
    return f"{LEARNWITH}?{q}"


def _units_in_order(lessons):
    """Contiguous units in COURSE ORDER, keyed by first appearance (NOT by token), so a lesson whose unit token
    reappears out of order (e.g. G11 L30 tagged 'G11 U2' after U6) does NOT fold back into an earlier unit and
    break course sequence. Returns [(synthetic_uid, title, [lesson_numbers...])] in order.
    A synthetic uid disambiguates a reused token: g<grade>-u<seq>."""
    units = []
    for n, L, _f in lessons:
        tok = R.unit_key(L)
        title = R.unit_title(L)
        if units and units[-1]["tok"] == tok:
            units[-1]["ns"].append(n)
        else:
            units.append({"tok": tok, "title": title, "ns": [n]})
    return units


def build_plan(grade, base_url):
    lessons = R.lessons_for(grade)              # canonical selection (newest version per lesson number), in order
    authored = _authored(grade)                 # per-lesson MASTERY entry -> PP100 form-bank depth
    cid = COURSE_ID[grade]
    total_xp = sum(expected_xp(L) for _n, L, _f in lessons)
    plan = []  # (kind, id, url, body)
    course_metadata = {"publishStatus": "published", "timebackVisible": True,
                       "metrics": {"totalXp": total_xp, "totalLessons": len(lessons), "totalGrades": 1}}
    plan.append(("course", cid, COURSES, {"course": {
        "sourcedId": cid, "status": "active", "title": COURSE_TITLE[grade],
        "courseCode": cid, "grades": [GRADE_NUM[grade]], "subjects": ["Writing"],
        "org": {"sourcedId": ORG_ID}, "metadata": course_metadata}}))

    units = _units_in_order(lessons)
    uid_of_n = {}
    for seq, u in enumerate(units, 1):
        uid = f"{grade.lower()}-u{seq}"
        for n in u["ns"]:
            uid_of_n[n] = uid
        plan.append(("component", uid, COMPONENTS, {"courseComponent": {
            "sourcedId": uid, "status": "active", "title": u["title"][:200], "sortOrder": seq,
            "course": {"sourcedId": cid}, "parent": None, "courseComponent": None, "metadata": {}}}))

    for n, L, _f in lessons:
        uid = uid_of_n[n]
        tid = f"topic-{L.id}"
        xp = expected_xp(L)
        art_url = article_player_url(grade, n, L, base_url)
        # LEAF topic (meta {} -> NOT quiz-flagged, so the article renders for students)
        plan.append(("component", tid, COMPONENTS, {"courseComponent": {
            "sourcedId": tid, "status": "active", "title": (L.title or L.id)[:200], "sortOrder": n,
            "course": {"sourcedId": cid},
            "parent": {"sourcedId": uid}, "courseComponent": {"sourcedId": uid}, "metadata": {}}}))
        # RESOURCE 1: gated-reading ARTICLE (kind=text -> LearnWith player wrapping the hosted lesson.html)
        art_rid = f"res-{L.id}-article"
        plan.append(("resource", art_rid, RES, {"resource": {
            "sourcedId": art_rid, "status": "active", "title": (L.title or L.id)[:200],
            "importance": "primary", "vendorResourceId": f"{L.id}-article", "vendorId": "alpha-incept",
            "applicationId": "incept",
            "metadata": {"type": "text", "activityType": "Article", "format": "html", "language": "en-US",
                         "xp": xp, "url": art_url}}}))
        plan.append(("component-resource", f"cr-{L.id}-article", COMPRES, {"componentResource": {
            "sourcedId": f"cr-{L.id}-article", "status": "active", "title": (L.title or L.id)[:200],
            "sortOrder": 1, "resource": {"sourcedId": art_rid},
            "courseComponent": {"sourcedId": tid}, "metadata": {"xp": xp}}}))
        # RESOURCE 2: PP100 MASTERY (powerpath-100). A lesson's PP100 is a form BANK: N equivalent single-item
        # tests the PowerPath engine round-robins across attempts (retry serves the next form). Depth N comes
        # from the lesson's MASTERY entry (mastery_forms.forms_for). PROD-SAFE: a bank of ONE points the PP100
        # resource straight at the single mastery test (byte-identical to today); a bank of >1 emits an
        # assessment-bank Resource listing the N form-test ids and points the CR at that bank.
        bank_size = len(MF.forms_for(authored.get(L.id, {})) or [{}])
        pp_title = f"{(L.title or L.id)[:180]} - Mastery"
        if bank_size <= 1:
            pp_rid = f"res-{L.id}-pp100"
            plan.append(("resource", pp_rid, RES, {"resource": {
                "sourcedId": pp_rid, "status": "active", "title": pp_title,
                "importance": "primary", "vendorResourceId": f"{L.id}-pp100", "vendorId": "alpha-incept",
                "applicationId": "incept",
                "metadata": {"type": "qti", "subType": "qti-test", "xp": xp,
                             "url": f"{QTI_BASE}/assessment-tests/{mastery_test_id(L)}"}}}))
            pp_link_target = pp_rid
        else:
            # each form-test is wrapped in its OWN Resource; the assessment-bank lists these SUB-RESOURCE ids
            # (verified live 2026-07-23: a type:assessment-bank validates metadata.resources as Resource
            # sourcedIds, NOT test ids). The engine round-robins over the bank's sub-resources per attempt.
            # Individual sub-resources are NOT linked as their own CRs (the documented "3 links per topic"
            # defect); only the bank is linked to the topic.
            sub_ids = []
            for k in range(1, bank_size + 1):
                sub_rid = MF.form_subresource_id(L.id, k)
                test_id = MF.form_test_id(L.id, k, bank_size=bank_size)
                sub_ids.append(sub_rid)
                plan.append(("resource", sub_rid, RES, {"resource": {
                    "sourcedId": sub_rid, "status": "active", "title": f"{pp_title} - form {k}",
                    "importance": "primary", "vendorResourceId": f"{L.id}-pp100-f{k}", "vendorId": "alpha-incept",
                    "applicationId": "incept",
                    "metadata": {"type": "qti", "subType": "qti-test", "xp": xp,
                                 "url": f"{QTI_BASE}/assessment-tests/{test_id}"}}}))
            bank_rid = MF.bank_resource_id(L.id)
            plan.append(("resource", bank_rid, RES, {"resource": {
                "sourcedId": bank_rid, "status": "active", "title": pp_title,
                "importance": "primary", "vendorResourceId": f"{L.id}-pp100-bank", "vendorId": "alpha-incept",
                "applicationId": "incept",
                "metadata": {"type": "assessment-bank", "xp": xp, "resources": sub_ids}}}))
            pp_link_target = bank_rid
        plan.append(("component-resource", f"cr-{L.id}-pp100", COMPRES, {"componentResource": {
            "sourcedId": f"cr-{L.id}-pp100", "status": "active", "title": pp_title,
            "sortOrder": 2, "resource": {"sourcedId": pp_link_target},
            "courseComponent": {"sourcedId": tid},
            "metadata": {"lessonType": "powerpath-100", "expected_xp": xp}}}))
    return plan, lessons, units


def post(session, url, body):
    import requests
    for attempt in range(4):
        try:
            r = session.post(url, json=body, timeout=60)
        except requests.RequestException as e:
            if attempt < 3:
                time.sleep(BACKOFF[attempt]); continue
            return False, 0, f"network error: {e}"
        if r.status_code in (200, 201):
            return True, r.status_code, "created"
        if r.status_code == 409 or "already exists" in (r.text or "").lower():
            return True, r.status_code, "exists (idempotent)"
        if r.status_code in RETRY_ON and attempt < 3:
            time.sleep(BACKOFF[attempt]); continue
        return False, r.status_code, (r.text or "")[:300]
    return False, 0, "exhausted retries"


def _checkpoint(grade):
    return os.path.join(ROOT, f"COURSE_ASSEMBLE_V3_1_{grade}_CHECKPOINT.json")


def push_grade(grade, base_url):
    """LIVE create/replace one grade's v3.1 course. Idempotent (409=ok) + checkpointed. Needs creds."""
    load_env()
    import requests
    global ORG_ID
    from g9_push_live import get_token
    plan, lessons, units = build_plan(grade, base_url)
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {get_token()}", "Content-Type": "application/json"})
    ro = session.get(f"{ROSTER}/orgs?limit=50", timeout=30)
    if ro.status_code == 200:
        ids = [o.get("sourcedId") for o in ro.json().get("orgs", [])]
        if ORG_ID not in ids:
            real = next((o["sourcedId"] for o in ro.json()["orgs"] if "test-org" not in o.get("sourcedId", "")), ids[0])
            print(f"  org {ORG_ID} not found; using {real}")
            ORG_ID = real
            plan[0][3]["course"]["org"]["sourcedId"] = ORG_ID
    cp = _checkpoint(grade)
    done = json.load(open(cp)) if os.path.exists(cp) else {"ok": [], "fail": []}
    okset = set(done["ok"]); done["fail"] = []
    for kind, oid, url, body in plan:
        if oid in okset:
            continue
        ok, status, detail = post(session, url, body)
        if ok:
            okset.add(oid); done["ok"].append(oid)
        else:
            done["fail"].append({"id": oid, "kind": kind, "status": status, "detail": detail})
            print(f"  FAIL [{status}] {kind} {oid}: {detail}")
        json.dump({"ok": sorted(okset), "fail": done["fail"]}, open(cp, "w"), indent=1)
    ok = not done["fail"]
    print(f"  {grade}: {len(okset)} ok, {len(done['fail'])} failed."
          + (f"  COURSE LIVE: {COURSE_ID[grade]}" if ok else ""))
    return ok


def print_dry(grade, base_url):
    plan, lessons, units = build_plan(grade, base_url)
    print(f"\n=== {grade}: {COURSE_TITLE[grade]} ({COURSE_ID[grade]}) ===")
    print(f"  {len(lessons)} lessons, {len(units)} units, 2 resources/lesson -> {len(plan)} objects. "
          f"article host = {base_url}")
    for seq, u in enumerate(units, 1):
        ns = u["ns"]
        print(f"  {grade.lower()}-u{seq}: L{ns[0]:02d}-L{ns[-1]:02d}  {u['title'][:56]}")
    # spot-check the first lesson's article URL resolves to the deployed layout
    n0, L0, _ = lessons[0]
    print(f"  sample article: {article_content_url(grade, n0, base_url)}")
    print(f"  sample pp100  : {QTI_BASE}/assessment-tests/{mastery_test_id(L0)}")
    return plan, lessons, units


def main():
    args = sys.argv[1:]
    if not args:
        print("usage: course_assemble_v3_1.py <G9|G10|G11|G12|all> [--live] [--base-url <alias>]")
        return 2
    target = args[0]
    live = "--live" in args
    base = args[args.index("--base-url") + 1] if "--base-url" in args else DEFAULT_BASE
    grades = list(GRADES) if target.lower() == "all" else [target.upper()]
    for g in grades:
        if g not in GRADES:
            print(f"unknown grade {g!r}"); return 2
    if not live:
        for g in grades:
            print_dry(g, base)
        print("\nDRY mode. No network call made. Re-run with --live (per grade or 'all') to create/replace.")
        return 0
    load_env()
    if not (os.environ.get("TIMEBACK_CLIENT_ID") and os.environ.get("TIMEBACK_CLIENT_SECRET")):
        print("LIVE push needs TIMEBACK_CLIENT_ID / TIMEBACK_CLIENT_SECRET (load ../.env)."); return 2
    allok = True
    for g in grades:
        allok = push_grade(g, base) and allok
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
