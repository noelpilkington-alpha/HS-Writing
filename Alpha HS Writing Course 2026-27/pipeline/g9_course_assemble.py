"""
g9_course_assemble.py  -  OneRoster course assembly for the G9 slice (makes the pushed QTI a NAVIGABLE course).

The QTI push (g9_push_live.py) put the items/tests/stimuli on qti.alpha-1edtech.ai. That is reviewable
item-by-item, but to walk the course a reviewer needs the OneRoster layer on api.alpha-1edtech.ai:
  Course -> Components (the 4 G9 units) -> Resources (one per lesson, linking its assessment-test) ->
  ComponentResources (link resource to its unit at a sort position).
This is where expected_xp and lessonType live (the QTI assessment-tests endpoint silently dropped expected_xp
because it is a Content/OneRoster field, not a QTI field).

Gotchas honored (from the `timeback` skill create-course.md, empirically verified 2026-04-02):
- resources endpoint needs a TRAILING SLASH (else 422).
- lessonType in RESOURCE metadata triggers a 500; put lessonType in the COMPONENT-RESOURCE metadata instead.
- components: set BOTH parent + courseComponent (null for top-level units); status required; course ref required.
- course.org.sourcedId required (invalid = 404).
- PUT returns 201; 409 = exists = idempotent.

Usage:
  python pipeline/g9_course_assemble.py           # DRY: build the plan, no network
  python pipeline/g9_course_assemble.py --live     # LIVE: create course/components/resources/links
  python pipeline/g9_course_assemble.py --rename   # LIVE: PUT the new COURSE_TITLE onto the live course

Course title = COURSE_TITLE (student-facing). Changed to "AlphaWriting G9" 2026-07-23 (Noel). A plain
--live re-run will NOT rename an existing course (POST is 409-idempotent); use --rename (a PUT) for that.
Both --live and --rename need TIMEBACK_CLIENT_ID / TIMEBACK_CLIENT_SECRET (loaded from ../.env).
"""
from __future__ import annotations
import os, sys, glob, re, json, time

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
from xp_allocation import expected_xp
from g9_push_dryrun import _load

ONEROSTER = "https://api.alpha-1edtech.ai"
QTI_BASE = "https://qti.alpha-1edtech.ai/api"
ROSTER = f"{ONEROSTER}/ims/oneroster/rostering/v1p2"
RES = f"{ONEROSTER}/ims/oneroster/resources/v1p2/resources/"          # trailing slash REQUIRED
COMPRES = f"{ROSTER}/courses/component-resources"
COMPONENTS = f"{ROSTER}/courses/components"
COURSES = f"{ROSTER}/courses"
CHECKPOINT = os.path.join(ROOT, "G9_COURSE_CHECKPOINT.json")
ORG_ID = "a6d57e8d-080e-4c49-80b8-b122d447b70e"   # Alpha Denver (verified live 2026-07-12); fallback in main()
COURSE_ID = "hs-writing-g9-2026"
COURSE_TITLE = "AlphaWriting G9"   # student-facing course name (Noel 2026-07-23; was "Writing G9")
RETRY_ON = {429, 500, 502, 503, 504}
BACKOFF = [5, 15, 30]

# G9 unit structure (from the course map / lesson unit labels). Lesson number -> unit index.
UNITS = [
    ("g9-u1", "Unit 1: Claim and Controlling Idea", range(1, 7)),      # L01-L06
    ("g9-u2", "Unit 2: Evidence and Reasoning", range(7, 13)),          # L07-L12
    ("g9-u3", "Unit 3: Cohesion and Revision", range(13, 19)),          # L13-L18
    ("g9-u4", "Unit 4: Full Essay and Gate", range(19, 27)),            # L19-L26
]


def load_env():
    envp = os.path.join(ROOT, "..", ".env")
    if os.path.exists(envp):
        for line in open(envp, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def g9_lessons():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "Lesson_Bank_G9", "lesson_g9_l[0-9]*.py"))):
        m = _load(f)
        L = getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0]
        n = int(re.search(r"_l(\d+)_", f).group(1))
        if L:
            out.append((n, L))
    return out


def unit_of(n):
    for uid, title, rng in UNITS:
        if n in rng:
            return uid, title
    return "g9-u4", "Unit 4"


def lesson_type_for(L):
    # live API enum (verified 2026-07-12): powerpath-100 | map-adaptive | quiz | test-out | placement |
    # unit-test | alpha-read-article. Our SRSD instruction-through-production lessons map to 'quiz' (a graded
    # activity); the course GATE maps to 'unit-test'.
    return "unit-test" if "GATE" in (L.unit or "") else "quiz"


def build_plan():
    lessons = g9_lessons()
    total_xp = sum(expected_xp(L) for _n, L in lessons)
    plan = []  # (kind, id, url, body)
    # 1) course. metadata.metrics = the UI's Total XP / Total Lessons / Total Grades (verified against live
    # courses that display these). A "Class" (OneRoster class entity) is provisioned separately and our
    # credentials are write-denied on /classes (403 IAM deny) - it must be created by a roster-admin.
    # publishStatus 'published' + timebackVisible True are what make the course visible in the STUDENT runtime
    # (verified live 2026-07-13: 'testing' + no timebackVisible showed the tree in the builder but delivered no
    # lessons to the student view; student-accessible courses set both).
    course_metadata = {"publishStatus": "published", "timebackVisible": True,
                       "metrics": {"totalXp": total_xp, "totalLessons": len(lessons), "totalGrades": 1}}
    plan.append(("course", COURSE_ID, COURSES, {"course": {
        "sourcedId": COURSE_ID, "status": "active", "title": COURSE_TITLE,
        "courseCode": COURSE_ID, "grades": ["09"], "subjects": ["Writing"],
        "org": {"sourcedId": ORG_ID},
        "metadata": course_metadata}}))
    # 2) unit components (top-level: parent=null)
    for i, (uid, title, _rng) in enumerate(UNITS, 1):
        plan.append(("component", uid, COMPONENTS, {"courseComponent": {
            "sourcedId": uid, "status": "active", "title": title, "sortOrder": i,
            "course": {"sourcedId": COURSE_ID}, "parent": None, "courseComponent": None,
            "metadata": {}}}))
    # 3) per lesson: a LESSON/TOPIC component (parent=unit) + a resource (-> its assessment-test) +
    #    a component-resource link that attaches the resource TO THE TOPIC (not the unit).
    # CRITICAL (verified live 2026-07-13 against GAUNTLET-TEKSHI-G8 + create-course.md): the student UI walks
    # Course -> Unit component -> LESSON/TOPIC child component -> component-resource. A component-resource linked
    # directly to a UNIT renders NOTHING ("won't show in recommendations" - create-course.md). The first G9
    # assembly skipped the topic tier, so units showed as empty shells. This adds the middle tier.
    for n, L in lessons:
        uid, _ut = unit_of(n)
        tid = f"topic-{L.id}"
        rid = f"res-{L.id}"
        lt = lesson_type_for(L)
        # 3a) lesson/topic component under its unit (set BOTH parent + courseComponent per the doc)
        plan.append(("component", tid, COMPONENTS, {"courseComponent": {
            "sourcedId": tid, "status": "active", "title": (L.title or L.id)[:200], "sortOrder": n,
            "course": {"sourcedId": COURSE_ID},
            "parent": {"sourcedId": uid}, "courseComponent": {"sourcedId": uid},
            "metadata": {"isAssessment": True, "assessmentType": "quiz"}}}))
        # 3b) resource -> the lesson's assessment-test. The content target MUST live in metadata.url (verified
        # live 2026-07-13 against working lesson resources): a TOP-LEVEL `url` is silently DROPPED by the API,
        # leaving the resource with no target so the student player finds no lesson to deliver. metadata.type
        # "qti" + subType "qti-test" + xp mirror the working pattern. (Only `lessonType` in resource metadata
        # 500s - the 2026-07-12 "no resource metadata" note over-generalized that single bad field.)
        plan.append(("resource", rid, RES, {"resource": {
            "sourcedId": rid, "status": "active", "title": (L.title or L.id)[:200],
            "importance": "primary", "vendorResourceId": L.id, "vendorId": "alpha-incept",
            "applicationId": "incept",
            "metadata": {"type": "qti", "subType": "qti-test", "xp": expected_xp(L),
                         "url": f"{QTI_BASE}/assessment-tests/{L.id}"}}}))
        # 3c) component-resource link: attaches the resource to the TOPIC component
        plan.append(("component-resource", f"cr-{L.id}", COMPRES, {"componentResource": {
            "sourcedId": f"cr-{L.id}", "status": "active", "title": (L.title or L.id)[:200],
            "sortOrder": n, "resource": {"sourcedId": rid},
            "courseComponent": {"sourcedId": tid},
            "metadata": {"lessonType": lt, "expected_xp": expected_xp(L)}}}))
    return plan, lessons


def post(session, url, body, ctx):
    """Create via POST to the collection (this API's PUT is update-only -> 404 on new ids). 409 = idempotent.
    A 'already exists' 400/422 is also treated as success (re-runs are safe)."""
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


def rename_course(new_title=COURSE_TITLE):
    """Rename the ALREADY-LIVE course. build_plan()/POST is idempotent-on-409, so it will NOT update an
    existing course's title; a rename is a PUT to courses/{sourcedId} (update-only, per the gotchas). GETs the
    current record first, patches only `title`, and PUTs it back, so no other field is disturbed. Live only."""
    load_env()
    import requests
    from g9_push_live import get_token
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {get_token()}", "Content-Type": "application/json"})
    url = f"{COURSES}/{COURSE_ID}"
    r = session.get(url, timeout=30)
    if r.status_code != 200:
        print(f"  cannot GET {COURSE_ID} [{r.status_code}]: {(r.text or '')[:200]}")
        return 1
    course = r.json().get("course", r.json())
    old = course.get("title")
    if old == new_title:
        print(f"  already titled '{new_title}'. No change.")
        return 0
    course["title"] = new_title
    for attempt in range(4):
        pr = session.put(url, json={"course": course}, timeout=60)
        if pr.status_code in (200, 201):
            print(f"  RENAMED {COURSE_ID}: '{old}' -> '{new_title}'")
            return 0
        if pr.status_code in RETRY_ON and attempt < 3:
            time.sleep(BACKOFF[attempt]); continue
        print(f"  rename FAILED [{pr.status_code}]: {(pr.text or '')[:300]}")
        return 1
    return 1


def main(live=False, rename=False):
    if rename:
        return rename_course()
    plan, lessons = build_plan()
    print(f"G9 course-assembly plan: 1 course, {len(UNITS)} units, {len(lessons)} lessons "
          f"({len(plan)} objects). expected_xp on each resource + link.")
    if not live:
        print("DRY mode. Re-run with --live to create the course. No network call made.")
        return 0

    load_env()
    import requests
    global ORG_ID
    # token
    from g9_push_live import get_token
    tok = get_token()
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    # verify org id; fall back to a real Alpha org if the sample 404s
    ro = session.get(f"{ROSTER}/orgs?limit=50", timeout=30)
    if ro.status_code == 200:
        ids = [o.get("sourcedId") for o in ro.json().get("orgs", [])]
        if ORG_ID not in ids:
            real = next((o["sourcedId"] for o in ro.json()["orgs"] if "test-org" not in o.get("sourcedId", "")), ids[0])
            print(f"  org {ORG_ID} not found; using {real}")
            ORG_ID = real
            plan[0][3]["course"]["org"]["sourcedId"] = ORG_ID

    done = json.load(open(CHECKPOINT)) if os.path.exists(CHECKPOINT) else {"ok": [], "fail": []}
    okset = set(done["ok"]); done["fail"] = []
    for kind, oid, url, body in plan:
        if oid in okset:
            continue
        ok, status, detail = post(session, url, body, f"{kind} {oid}")
        if ok:
            okset.add(oid); done["ok"].append(oid)
        else:
            done["fail"].append({"id": oid, "kind": kind, "status": status, "detail": detail})
            print(f"  FAIL [{status}] {kind} {oid}: {detail}")
        json.dump({"ok": sorted(okset), "fail": done["fail"]}, open(CHECKPOINT, "w"), indent=1)
    print(f"\nG9 course assembly: {len(okset)} ok, {len(done['fail'])} failed.")
    if not done["fail"]:
        print(f"COURSE LIVE: {COURSE_ID}  (org {ORG_ID})")
    return 0 if not done["fail"] else 1


if __name__ == "__main__":
    # --rename : PUT the new COURSE_TITLE onto the already-live course (does not re-create anything).
    # --live   : create/assemble the full course (idempotent).
    sys.exit(main(live="--live" in sys.argv, rename="--rename" in sys.argv))
