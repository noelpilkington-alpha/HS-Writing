"""
pp100_roundrobin_probe.py  -  LIVE behavioral probe: does the PowerPath engine round-robin over an
assessment-bank's sub-tests across attempts? The design spec confirms this from the OpenAPI text; this
observes it end-to-end on the real runtime before we author ~1,770 forms on that assumption.

ISOLATED + SELF-CLEANING. All objects use a TEST-PP100RR- / test-pp100rr- prefix and are torn down at the end
(and on --cleanup). NOTHING touches the live AlphaWriting courses. Disposable graph:
  - 2 FRQ items + 2 single-item tests (form A, form B) with DISTINCT prompts (so the served form is observable)
  - 1 assessment-bank Resource listing [testA, testB]
  - 1 throwaway course + component (topic) + a component-resource linking the bank (this CR = the 'lesson')
  - 1 throwaway class + student + enrollment (PowerPath requires an active enrollment)
Then: createNewAttempt #1 -> getNextQuestion (observe prompt) -> complete; createNewAttempt #2 -> getNextQuestion
(observe prompt). ROUND-ROBIN CONFIRMED iff attempt 1 serves form A and attempt 2 serves form B.

DRY BY DEFAULT: prints the exact object graph + calls, no network. --live runs it (needs creds in ../.env).
--cleanup deletes any leftover TEST-PP100RR- objects. This is a live-mutation tool; run --live only on explicit go.
"""
from __future__ import annotations
import os, sys, json, time

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)

ONEROSTER = "https://api.alpha-1edtech.ai"
QTI_BASE = "https://qti.alpha-1edtech.ai/api"
ROSTER = f"{ONEROSTER}/ims/oneroster/rostering/v1p2"
RES = f"{ONEROSTER}/ims/oneroster/resources/v1p2/resources/"
COMPRES = f"{ROSTER}/courses/component-resources"
COMPONENTS = f"{ROSTER}/courses/components"
COURSES = f"{ROSTER}/courses"
PP = f"{ONEROSTER}/powerpath"
ORG_ID = "a6d57e8d-080e-4c49-80b8-b122d447b70e"   # Alpha Denver (same as assembler)
RETRY_ON = {429, 500, 502, 503, 504}
BACKOFF = [5, 15, 30]

## run-scoped suffix: soft-deleted objects keep their sourcedId (status tobedeleted) and block id reuse, so
## each probe run uses a fresh tag. Pass --tag <t> (e.g. --tag r2); defaults to "r1".
def _apply_tag(tag):
    global PFX, IDS
    PFX = f"TEST-PP100RR{tag.upper()}"
    IDS = _make_ids(PFX)


def _make_ids(pfx):
    lo = pfx.lower()
    return {
        "itemA": f"{pfx}-ITEM-A", "itemB": f"{pfx}-ITEM-B",
        "testA": f"{pfx}-TEST-A", "testB": f"{pfx}-TEST-B",
        "subA":  f"res-{lo}-fa", "subB": f"res-{lo}-fb",
        "bank":  f"res-{lo}-bank",
        "course": f"{lo}-course", "unit": f"{lo}-unit", "topic": f"{lo}-topic",
        "cr":    f"cr-{lo}-pp100",
        "class": f"{lo}-class", "student": f"{lo}-student",
        "enroll": f"{lo}-enroll", "term": f"{lo}-term",
    }


PFX = "TEST-PP100RR"
IDS = {
    "itemA": f"{PFX}-ITEM-A", "itemB": f"{PFX}-ITEM-B",
    "testA": f"{PFX}-TEST-A", "testB": f"{PFX}-TEST-B",
    # each form-test is wrapped in its own OneRoster Resource; the bank lists these SUB-RESOURCE ids
    # (verified: a type:assessment-bank bank validates metadata.resources as Resource sourcedIds, NOT test ids).
    "subA":  f"res-{PFX.lower()}-fa", "subB": f"res-{PFX.lower()}-fb",
    "bank":  f"res-{PFX.lower()}-bank",
    "course": f"{PFX.lower()}-course", "unit": f"{PFX.lower()}-unit", "topic": f"{PFX.lower()}-topic",
    "cr":    f"cr-{PFX.lower()}-pp100",
    "class": f"{PFX.lower()}-class", "student": f"{PFX.lower()}-student",
    "enroll": f"{PFX.lower()}-enroll", "term": f"{PFX.lower()}-term",
}


def load_env():
    envp = os.path.join(ROOT, "..", ".env")
    if os.path.exists(envp):
        for line in open(envp, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _frq_item(iid, prompt_text):
    """A minimal extended-text FRQ whose prompt is DISTINCT per form (the observable)."""
    return {"identifier": iid, "title": f"{iid}", "type": "extended-text",
            "interaction": {"type": "extended-text", "questionStructure": {
                "prompt": f"<p>{prompt_text}</p>"}},
            "responseDeclarations": [{"identifier": "RESPONSE", "cardinality": "single", "baseType": "string"}],
            "outcomeDeclarations": [{"identifier": "SCORE", "cardinality": "single", "baseType": "float"}]}


def _single_test(tid, iid):
    return {"identifier": tid, "title": tid,
            "qti-test-part": [{"identifier": "tp", "navigationMode": "linear", "submissionMode": "individual",
                               "sequence": 1, "qti-assessment-section": [{
                                   "identifier": "sec", "title": "S", "visible": True, "sequence": 1,
                                   "qti-assessment-item-ref": [{"identifier": iid, "href": f"{iid}.xml",
                                                                "sequence": 1}]}]}],
            "outcomeDeclarations": [{"identifier": "SCORE", "cardinality": "single", "baseType": "float"}]}


def build_graph():
    """The dependency-ordered create plan: (kind, id, method, url, body)."""
    plan = []
    plan.append(("item", IDS["itemA"], f"{QTI_BASE}/assessment-items", _frq_item(IDS["itemA"], "FORM A PROBE PROMPT: write one sentence about topic A.")))
    plan.append(("item", IDS["itemB"], f"{QTI_BASE}/assessment-items", _frq_item(IDS["itemB"], "FORM B PROBE PROMPT: write one sentence about topic B.")))
    plan.append(("test", IDS["testA"], f"{QTI_BASE}/assessment-tests", _single_test(IDS["testA"], IDS["itemA"])))
    plan.append(("test", IDS["testB"], f"{QTI_BASE}/assessment-tests", _single_test(IDS["testB"], IDS["itemB"])))
    # a Resource wrapping each single-item test (the bank references these, not the test ids directly)
    for sub, test, tag in ((IDS["subA"], IDS["testA"], "fa"), (IDS["subB"], IDS["testB"], "fb")):
        plan.append(("resource", sub, RES, {"resource": {
            "sourcedId": sub, "status": "active", "title": f"PP100 RR probe form {tag}",
            "importance": "primary", "vendorResourceId": f"{PFX.lower()}-{tag}", "vendorId": "alpha-incept",
            "applicationId": "incept",
            "metadata": {"type": "qti", "subType": "qti-test", "url": f"{QTI_BASE}/assessment-tests/{test}"}}}))
    plan.append(("resource", IDS["bank"], RES, {"resource": {
        "sourcedId": IDS["bank"], "status": "active", "title": "PP100 RR probe bank",
        "importance": "primary", "vendorResourceId": f"{PFX.lower()}-bank", "vendorId": "alpha-incept",
        "applicationId": "incept",
        "metadata": {"type": "assessment-bank", "resources": [IDS["subA"], IDS["subB"]]}}}))
    plan.append(("course", IDS["course"], COURSES, {"course": {
        "sourcedId": IDS["course"], "status": "active", "title": "PP100 RR Probe Course",
        "courseCode": IDS["course"], "grades": ["09"], "subjects": ["Writing"],
        "org": {"sourcedId": ORG_ID}, "metadata": {"publishStatus": "published", "timebackVisible": False}}}))
    plan.append(("component", IDS["unit"], COMPONENTS, {"courseComponent": {
        "sourcedId": IDS["unit"], "status": "active", "title": "Probe Unit", "sortOrder": 1,
        "course": {"sourcedId": IDS["course"]}, "parent": None, "courseComponent": None, "metadata": {}}}))
    plan.append(("component", IDS["topic"], COMPONENTS, {"courseComponent": {
        "sourcedId": IDS["topic"], "status": "active", "title": "Probe Topic", "sortOrder": 1,
        "course": {"sourcedId": IDS["course"]}, "parent": {"sourcedId": IDS["unit"]},
        "courseComponent": {"sourcedId": IDS["unit"]}, "metadata": {}}}))
    plan.append(("component-resource", IDS["cr"], COMPRES, {"componentResource": {
        "sourcedId": IDS["cr"], "status": "active", "title": "Probe PP100 (bank)", "sortOrder": 1,
        "resource": {"sourcedId": IDS["bank"]}, "courseComponent": {"sourcedId": IDS["topic"]},
        "metadata": {"lessonType": "powerpath-100"}}}))
    # roster: student + class + enrollment (PowerPath requires an active enrollment for the subject).
    # OneRoster creates these via PUT /{collection}/{sourcedId} (upsert), NOT POST to the collection; the
    # create loop routes any kind in _PUT_KINDS as PUT to url/{id}. The URL here is the collection base.
    plan.append(("student", IDS["student"], f"{ROSTER}/users", {"user": {
        "sourcedId": IDS["student"], "status": "active", "enabledUser": True,
        "givenName": "Probe", "familyName": "Student", "roles": [
            {"roleType": "primary", "role": "student", "org": {"sourcedId": ORG_ID}}]}}))
    plan.append(("class", IDS["class"], f"{ROSTER}/classes", {"class": {
        "sourcedId": IDS["class"], "status": "active", "title": "Probe Class", "classCode": IDS["class"],
        "classType": "scheduled", "course": {"sourcedId": IDS["course"]}, "org": {"sourcedId": ORG_ID},
        "terms": []}}))
    plan.append(("enrollment", IDS["enroll"], f"{ROSTER}/enrollments", {"enrollment": {
        "sourcedId": IDS["enroll"], "status": "active", "role": "student", "primary": True,
        "user": {"sourcedId": IDS["student"]}, "class": {"sourcedId": IDS["class"]},
        "school": {"sourcedId": ORG_ID}}}))
    return plan


# roster kinds are created via PUT /{collection}/{sourcedId}; everything else via POST to the collection URL
_PUT_KINDS = {"student", "class", "enrollment"}


def print_dry():
    plan = build_graph()
    print(f"\n=== PP100 round-robin probe - DRY (no network). {len(plan)} disposable objects ===\n")
    for kind, oid, url, body in plan:
        print(f"  CREATE {kind:17} {oid}")
    print("\nThen the OBSERVATION sequence (student runtime):")
    print(f"  1. POST {PP}/createNewAttempt  {{student, lesson={IDS['cr']}}}   -> attempt 1")
    print(f"  2. GET  {PP}/getNextQuestion?student=&lesson={IDS['cr']}          -> observe PROMPT (expect FORM A)")
    print(f"  3. complete attempt 1 (submit a response so createNewAttempt can advance)")
    print(f"  4. POST {PP}/createNewAttempt                                     -> attempt 2")
    print(f"  5. GET  {PP}/getNextQuestion                                      -> observe PROMPT (expect FORM B)")
    print(f"  6. GET  {PP}/getAttempts?student=&lesson={IDS['cr']}              -> both attempts, distinct sub-tests")
    print("\nROUND-ROBIN CONFIRMED iff attempt 1 serves FORM A and attempt 2 serves FORM B.")
    print("Teardown deletes every TEST-PP100RR- object. Re-run with --live to execute, --cleanup to purge leftovers.")


def _req(session, method, url, body=None):
    import requests
    for attempt in range(4):
        try:
            r = session.request(method, url, json=body, timeout=60)
        except requests.RequestException as e:
            if attempt < 3:
                time.sleep(BACKOFF[attempt]); continue
            return None, f"net: {e}"
        if r.status_code in RETRY_ON and attempt < 3:
            time.sleep(BACKOFF[attempt]); continue
        return r, None
    return None, "exhausted"


def _token():
    import requests
    r = requests.post(os.environ["TIMEBACK_IDP_URL"],
                      data={"grant_type": "client_credentials",
                            "client_id": os.environ["TIMEBACK_CLIENT_ID"],
                            "client_secret": os.environ["TIMEBACK_CLIENT_SECRET"]},
                      headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=30, verify=False)
    r.raise_for_status()
    return r.json()["access_token"]


def cleanup(session):
    """Delete every probe object in reverse dependency order (idempotent; 404 = already gone)."""
    # (kind, base_url, id) in reverse dependency order; bank before its sub-resources before tests before items
    steps = [
        ("enrollment", f"{ROSTER}/enrollments", IDS["enroll"]),
        ("class", f"{ROSTER}/classes", IDS["class"]),
        ("student", f"{ROSTER}/students", IDS["student"]),
        ("component-resource", COMPRES, IDS["cr"]),
        ("component", COMPONENTS, IDS["topic"]),
        ("component", COMPONENTS, IDS["unit"]),
        ("course", COURSES, IDS["course"]),
        ("resource", RES.rstrip("/"), IDS["bank"]),
        ("resource", RES.rstrip("/"), IDS["subA"]),
        ("resource", RES.rstrip("/"), IDS["subB"]),
        ("test", f"{QTI_BASE}/assessment-tests", IDS["testA"]),
        ("test", f"{QTI_BASE}/assessment-tests", IDS["testB"]),
        ("item", f"{QTI_BASE}/assessment-items", IDS["itemA"]),
        ("item", f"{QTI_BASE}/assessment-items", IDS["itemB"]),
    ]
    for kind, base, oid in steps:
        r, err = _req(session, "DELETE", f"{base}/{oid}")
        code = r.status_code if r is not None else err
        print(f"  cleanup {kind:17} {oid}: {code}")


def run_live():
    import requests
    load_env()
    if not (os.environ.get("TIMEBACK_CLIENT_ID") and os.environ.get("TIMEBACK_CLIENT_SECRET")):
        print("LIVE needs TIMEBACK_CLIENT_ID / TIMEBACK_CLIENT_SECRET (../.env)."); return 2
    session = requests.Session()
    session.verify = False
    session.headers.update({"Authorization": f"Bearer {_token()}", "Content-Type": "application/json"})
    plan = build_graph()
    created = []
    print("=== creating probe graph ===")
    for kind, oid, url, body in plan:
        if kind in _PUT_KINDS:
            method, target = "PUT", f"{url}/{oid}"
        else:
            method, target = "POST", url
        r, err = _req(session, method, target, body)
        code = r.status_code if r is not None else err
        ok = r is not None and (r.status_code in (200, 201) or r.status_code == 409)
        print(f"  {method:4} {kind:17} {oid}: {code}" + ("" if ok else f"  !! {(r.text[:200] if r is not None else err)}"))
        if not ok:
            print("  ABORT: create failed; cleaning up.")
            cleanup(session); return 1
        created.append(oid)
    # observation
    sid, lesson = IDS["student"], IDS["cr"]
    print("\n=== observation ===")
    def next_prompt(label):
        r, _ = _req(session, "GET", f"{PP}/getNextQuestion?student={sid}&lesson={lesson}")
        txt = (r.text if r is not None else "")[:400]
        form = "A" if "FORM A" in txt else ("B" if "FORM B" in txt else "?")
        print(f"  {label}: served FORM {form}  (status {r.status_code if r else '?'})")
        return form
    r1, _ = _req(session, "POST", f"{PP}/createNewAttempt", {"student": sid, "lesson": lesson})
    print(f"  createNewAttempt #1: {r1.status_code if r1 else '?'}")
    f1 = next_prompt("attempt 1")
    # finalize attempt 1 so a new attempt can be created
    _req(session, "POST", f"{PP}/finalStudentAssessmentResponse", {"student": sid, "lesson": lesson})
    r2, _ = _req(session, "POST", f"{PP}/createNewAttempt", {"student": sid, "lesson": lesson})
    print(f"  createNewAttempt #2: {r2.status_code if r2 else '?'}")
    f2 = next_prompt("attempt 2")
    ra, _ = _req(session, "GET", f"{PP}/getAttempts?student={sid}&lesson={lesson}")
    print(f"  getAttempts: {ra.status_code if ra else '?'} {(ra.text[:300] if ra else '')}")
    verdict = "ROUND-ROBIN CONFIRMED" if (f1 == "A" and f2 == "B") else \
              f"NOT CONFIRMED (attempt1={f1}, attempt2={f2}) - inspect getAttempts above"
    print(f"\n  VERDICT: {verdict}")
    print("\n=== teardown ===")
    cleanup(session)
    return 0 if (f1 == "A" and f2 == "B") else 1


def main():
    args = sys.argv[1:]
    # optional run-scoped tag so a re-run avoids soft-deleted id ghosts: --tag r2
    if "--tag" in args:
        i = args.index("--tag")
        if i + 1 < len(args):
            _apply_tag(args[i + 1])
    if "--cleanup" in args:
        import requests
        load_env()
        s = requests.Session(); s.verify = False
        s.headers.update({"Authorization": f"Bearer {_token()}", "Content-Type": "application/json"})
        print("=== cleanup only ==="); cleanup(s); return 0
    if "--live" in args:
        return run_live()
    print_dry()
    return 0


if __name__ == "__main__":
    sys.exit(main())
