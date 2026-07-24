"""
course_push_mastery_v3_1.py  -  GRADE-GENERALIZED PP100 mastery push for the v3.1 gated-reading course.

Generalizes g9_push_mastery_v3_1.py to G9-G12. For each lesson it builds + pushes:
  1. a grader-wired extended-text FRQ item   id = <lesson>-MASTERY-FRQ   (ExternalApiScore + rc.* rubricBlock)
  2. a single-item assessment-test           id = <lesson>-MASTERY       (points at the FRQ item)
course_assemble_v3_1 points each lesson's PP100 resource at {QTI_BASE}/assessment-tests/<lesson>-MASTERY, so
the ids MUST match (both derive them the same way). This is STAGE 1; the course tree (assemble) is STAGE 2.

WHY A NEW FILE (not an edit of g9_push_mastery_v3_1.py): the G9 file carried a hardcoded HELDOUT source map and
a G9-only lesson glob. The held-out source now lives in each grade's mastery_prompts_g{N} bank (verified: all 4
banks carry a `source` field), and mastery_targets_grade.mastery_targets(grade) ALREADY returns the fully
rendered prompt (held-out source block + authored task) per grade. This module reuses that single generic path
so the pushed mastery prompt is byte-identical to the reviewed preview (render_course_preview_grade renders the
same mastery_prompt_html), and can never drift by grade.

The mastery FRQ prompt is the reviewed PP100 prompt (held-out source + cold task); the FRQ item carries the
grader wiring (customOperator ExternalApiScore + rubricBlock) via g9_wire_grader.wire_payload, so the item is
grader-ready the moment the grader base URL is live. The grader itself is wired/flipped separately.

Usage:
  python pipeline/course_push_mastery_v3_1.py G9  <grader-base-url>          # DRY: plan for one grade
  python pipeline/course_push_mastery_v3_1.py all <grader-base-url>          # DRY: all four grades
  python pipeline/course_push_mastery_v3_1.py G9  <grader-base-url> --live    # LIVE: push (needs creds)
  python pipeline/course_push_mastery_v3_1.py all <grader-base-url> --live    # LIVE: all four
"""
from __future__ import annotations
import os, sys, json, time

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
from g9_push_live import get_token, QTI_BASE
from g9_wire_grader import wire_payload, normalize_grader_url, item_to_xml_payload
from mastery_targets_grade import mastery_targets, mastery_prompt_html, _authored, _indep_slot
import mastery_forms as MF
import pp100_forms as PF
from g9_push_dryrun import STIM

ITEMS_URL = f"{QTI_BASE}/assessment-items"
TESTS_URL = f"{QTI_BASE}/assessment-tests"
GRADES = ("G9", "G10", "G11", "G12")
RETRY_ON = {429, 500, 502, 503, 504}
BACKOFF = [5, 15, 30]


def load_env():
    envp = os.path.join(ROOT, "..", ".env")
    if os.path.exists(envp):
        for line in open(envp, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _checkpoint(grade):
    return os.path.join(ROOT, f"MASTERY_V3_1_{grade}_CHECKPOINT.json")


def _taught_sources(L):
    """The set of stimulus ids the ARTICLE teaches (every stimulus_display ref). A held-out mastery form must
    not reuse any of these (seen-in-lesson leakage). Used as the QC gate's taught_source."""
    return {getattr(s, "ref", "") for s in L.slots
            if s.kind == "stimulus_display" and getattr(s, "ref", "")}


def _single_item_test(test_id, frq_id, title):
    return {"identifier": test_id, "title": f"{title[:110]} - Mastery",
            "qti-test-part": [{"identifier": "test_part", "navigationMode": "linear",
                               "submissionMode": "individual", "sequence": 1,
                               "qti-assessment-section": [{
                                   "identifier": "mastery_section", "title": "Mastery", "visible": True,
                                   "sequence": 1,
                                   "qti-assessment-item-ref": [
                                       {"identifier": frq_id, "href": f"{frq_id}.xml", "sequence": 1}]}]}],
            "outcomeDeclarations": [{"identifier": "SCORE", "cardinality": "single", "baseType": "float"}]}


def build_plan(grade, grader_url, gate=True):
    """(kind, id, url, body) plan for one grade. Per lesson, expand its PP100 form BANK (mastery_forms.forms_for)
    into N grader-wired FRQ items + N single-item mastery tests (one per equivalent form). A bank of ONE reuses
    the legacy ids (`<lesson>-MASTERY-FRQ`/`<lesson>-MASTERY`), so single-form lessons are byte-identical to
    today. A bank of >1 uses the `-f{k}` suffixed ids and the assembler wraps them in an assessment-bank.

    Skips a lesson only if it has no INDEPENDENT production slot (no composition outcome to master). When
    gate=True, a bank that fails the equivalence QC gate is skipped (with its problems recorded); this keeps a
    malformed multi-form bank from ever reaching the API. A single-form bank always passes (it is the taught
    form itself), so gating never blocks the prod-safe path."""
    plan = []
    skipped = []
    gate_fail = []
    authored = _authored(grade)
    # mastery_targets already resolves the lesson list + indep slot per grade; reuse it for the slot + L object.
    for lid, slot, _prompt_html, L in mastery_targets(grade):
        if slot is None:
            skipped.append(lid)
            continue
        entry = authored.get(lid, {})
        forms = MF.forms_for(entry) or [{}]   # a lesson with no authored entry still masters its indep slot
        bank_size = len(forms)
        if gate and bank_size > 1:
            ok, problems = PF.qc_form_bank(lid, forms, taught_source=_taught_sources(L), stim=STIM)
            if not ok:
                gate_fail.append((lid, problems))
                continue
        for k, form in enumerate(forms, 1):
            frq_id = MF.form_frq_id(lid, k, bank_size=bank_size)
            test_id = MF.form_test_id(lid, k, bank_size=bank_size)
            # render THIS form's prompt (held-out source block + authored task) exactly as the preview does
            prompt_html = mastery_prompt_html(L, form if form else entry)
            item = wire_payload(frq_id, slot, grader_url, source_html=None)
            item["interaction"]["questionStructure"]["prompt"] = prompt_html
            # Serialize to XML so the customOperator lands in the executable rawXml (a JSON push silently
            # strips it -> no grader fires; CRITICAL RULE 1 + 2026-07-24 allowlist finding).
            plan.append(("item", frq_id, ITEMS_URL, item_to_xml_payload(item)))
            plan.append(("test", test_id, TESTS_URL,
                         _single_item_test(test_id, frq_id, getattr(slot, "title", "") or lid)))
    if gate_fail:
        for lid, problems in gate_fail:
            print(f"  QC-GATE SKIP {lid}: {problems[0]}" + (f" (+{len(problems)-1} more)" if len(problems) > 1 else ""))
    return plan, skipped


def post(session, url, body, upsert=False):
    """POST (create) with retry. 409/already-exists = idempotent success. When upsert=True, a 409 (or an
    'already exists') triggers a PUT to url/{identifier} to UPDATE the existing object (full replace) - used to
    RE-WIRE live items whose grader config changed (e.g. rc.ap -> rc.4trait). The body already carries the
    complete item (wire_payload builds it), so a full-replace PUT is safe."""
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
            if not upsert:
                return True, r.status_code, "exists (idempotent)"
            # UPDATE the existing object via PUT (full replace) to apply the new wiring
            put_url = f"{url.rstrip('/')}/{body['identifier']}"
            for a2 in range(4):
                try:
                    pr = session.put(put_url, json=body, timeout=60)
                except requests.RequestException as e:
                    if a2 < 3:
                        time.sleep(BACKOFF[a2]); continue
                    return False, 0, f"PUT network error: {e}"
                if pr.status_code in (200, 201):
                    return True, pr.status_code, "updated (re-wired)"
                if pr.status_code in RETRY_ON and a2 < 3:
                    time.sleep(BACKOFF[a2]); continue
                return False, pr.status_code, "PUT: " + (pr.text or "")[:280]
        if r.status_code in RETRY_ON and attempt < 3:
            time.sleep(BACKOFF[attempt]); continue
        return False, r.status_code, (r.text or "")[:300]
    return False, 0, "exhausted retries"


def push_grade(grade, grader_url, rewire=False):
    """Push (or, with rewire=True, RE-WIRE) a grade's mastery FRQs + tests. rewire=True upserts ITEMS via PUT on
    409 (to apply changed grader config on already-live items) and IGNORES the item checkpoint so every item is
    re-PUT; tests are unchanged so they stay POST-409-idempotent."""
    load_env()
    import requests
    plan, skipped = build_plan(grade, grader_url)
    n_tests = sum(1 for k, *_ in plan if k == "test")
    mode = "RE-WIRE (PUT existing items)" if rewire else "push"
    print(f"  {grade} [{mode}]: {n_tests} lessons -> {n_tests} FRQ items + {n_tests} tests ({len(plan)} objects)."
          + (f" skipped (no INDEPENDENT slot): {skipped}" if skipped else ""))
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {get_token()}", "Content-Type": "application/json"})
    cp = _checkpoint(grade)
    done = json.load(open(cp)) if os.path.exists(cp) else {"ok": [], "fail": []}
    okset = set(done["ok"]); done["fail"] = []
    # push ALL items first, then tests (a test that refs a not-yet-created item 400s)
    for kind in ("item", "test"):
        for k, oid, url, body in plan:
            if k != kind:
                continue
            # on a re-wire, do NOT skip already-"ok" ITEMS (they must be re-PUT); tests still honor the checkpoint
            if oid in okset and not (rewire and k == "item"):
                continue
            ok, status, detail = post(session, url, body, upsert=(rewire and k == "item"))
            if ok:
                okset.add(oid)
                if oid not in done["ok"]:
                    done["ok"].append(oid)
                if rewire and k == "item":
                    print(f"    {k} {oid}: {detail}")
            else:
                done["fail"].append({"id": oid, "kind": k, "status": status, "detail": detail})
                print(f"    FAIL [{status}] {k} {oid}: {detail}")
            json.dump({"ok": sorted(okset), "fail": done["fail"]}, open(cp, "w"), indent=1)
    ok = not done["fail"]
    print(f"  {grade} mastery: {len(okset)} ok, {len(done['fail'])} failed."
          + ("" if ok else "  (see checkpoint)"))
    return ok


def print_dry(grade, grader_url):
    plan, skipped = build_plan(grade, grader_url)
    n_tests = sum(1 for k, *_ in plan if k == "test")
    print(f"\n=== {grade}: {n_tests} lessons -> {n_tests} FRQ items + {n_tests} single-item tests "
          f"({len(plan)} objects) ===")
    if skipped:
        print(f"  skipped (no INDEPENDENT production slot): {skipped}")
    # show a couple of ids so the id-match with the assembler is visible
    tests = [oid for k, oid, *_ in plan if k == "test"]
    print(f"  first mastery test id: {tests[0] if tests else '(none)'}")
    print(f"  last  mastery test id: {tests[-1] if tests else '(none)'}")


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print("usage: course_push_mastery_v3_1.py <G9|G10|G11|G12|all> <grader-base-url> [--live] [--rewire]")
        return 2
    target, grader_base = args[0], args[1]
    live = "--live" in args
    rewire = "--rewire" in args   # PUT-update EXISTING live items to apply changed grader wiring
    grader_url = normalize_grader_url(grader_base)
    grades = list(GRADES) if target.lower() == "all" else [target.upper()]
    for g in grades:
        if g not in GRADES:
            print(f"unknown grade {g!r}"); return 2
    print(f"v3.1 MASTERY {'RE-WIRE' if rewire else 'push'}  grader = {grader_url}")
    if not live:
        for g in grades:
            print_dry(g, grader_url)
        print(f"\nDRY mode. No network call made. Re-run with --live{' --rewire' if rewire else ''} to "
              f"{'re-wire existing items (PUT)' if rewire else 'push'}.")
        return 0
    load_env()
    if not (os.environ.get("TIMEBACK_CLIENT_ID") and os.environ.get("TIMEBACK_CLIENT_SECRET")):
        print("LIVE push needs TIMEBACK_CLIENT_ID / TIMEBACK_CLIENT_SECRET (load ../.env)."); return 2
    allok = True
    for g in grades:
        allok = push_grade(g, grader_url, rewire=rewire) and allok
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
