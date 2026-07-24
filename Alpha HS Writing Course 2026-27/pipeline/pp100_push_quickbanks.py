"""
pp100_push_quickbanks.py  -  push the depth-N QUICK BANKS live for every auto-banked lesson (all grades).

Runs with the quick-bank overlay ON (PP100_QUICK_BANK_DEPTH must be set, e.g. 3). For each lesson whose
overlaid entry has >1 form, it pushes exactly that lesson's bank objects and re-points its PP100 CR at the
bank - the same scoped, idempotent, PUT-the-CR pattern the L01 pilot proved. Lessons that stay single-form
(the 41 safely refused) are left completely untouched. L01 (already live from the pilot) is skipped by default.

Per banked lesson:
  N grader-wired FRQ items (-MASTERY-FRQ-f{k}) + N single-item tests (-MASTERY-f{k})   [QTI API]
  N wrapping sub-resources (res-<lid>-pp100-f{k}) + 1 assessment-bank (res-<lid>-pp100-bank)  [OneRoster]
  re-point cr-<lid>-pp100 -> the bank (PUT/replace)

DRY by default (prints per-lesson object counts). --live pushes (needs creds + PP100_QUICK_BANK_DEPTH set).
Idempotent (409=ok); checkpointed so a re-run resumes. Only banked lessons are touched.
This is a live mutation across many lessons; run --live only on explicit go.
"""
from __future__ import annotations
import os, sys, json, time

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)

GRADER = "https://hs-writing-grading.onrender.com/score"
DEFAULT_BASE = "https://verceldeploy-five-tan.vercel.app"
GRADES = ("G9", "G10", "G11", "G12")
SKIP_LIDS = {"ACC-W910-L-G9-C901-0001"}   # already live via the pilot
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


def _banked_lids():
    """{lid: n_forms} for every lesson the overlay expanded to a bank (>1 form), across all grades, minus SKIP."""
    import mastery_forms as MF
    from mastery_targets_grade import _authored
    out = {}
    for g in GRADES:
        for lid, e in _authored(g).items():
            n = len(MF.forms_for(e))
            if n > 1 and lid not in SKIP_LIDS:
                out[lid] = (g, n)
    return out


def _plan_for_grade(grade):
    """All bank push steps for a grade: (kind, id, method, url, body), filtered to banked lessons."""
    import course_push_mastery_v3_1 as PM
    import course_assemble_v3_1 as CA
    banked = _banked_lids()
    mplan, _ = PM.build_plan(grade, GRADER)
    aplan, _, _ = CA.build_plan(grade, DEFAULT_BASE)
    lids = {lid for lid, (g, n) in banked.items() if g == grade}
    steps = []
    for kind in ("item", "test"):
        for k, oid, url, body in mplan:
            if k == kind and any(oid.startswith(lid) for lid in lids):
                steps.append((kind, oid, "POST", url, body))
    for k, oid, url, body in aplan:
        if k == "resource" and any(
                (oid.startswith(f"res-{lid}-pp100-f") or oid == f"res-{lid}-pp100-bank") for lid in lids):
            steps.append(("resource", oid, "POST", url, body))
    # sub-resources before banks (bank references subs)
    steps.sort(key=lambda s: (s[0] != "item", s[0] != "test", s[0] == "resource" and s[1].endswith("-bank")))
    for k, oid, url, body in aplan:
        if k == "component-resource" and any(oid == f"cr-{lid}-pp100" for lid in lids):
            steps.append(("component-resource", oid, "PUT", f"{url}/{oid}", body))
    return steps


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


def print_dry():
    if not os.environ.get("PP100_QUICK_BANK_DEPTH"):
        print("PP100_QUICK_BANK_DEPTH is not set - the overlay is OFF, so there are no quick banks to push.")
        print("Set it (e.g. PP100_QUICK_BANK_DEPTH=3) and re-run.")
        return
    banked = _banked_lids()
    total = 0
    print(f"\n=== quick-bank push - DRY. {len(banked)} banked lessons (depth={os.environ['PP100_QUICK_BANK_DEPTH']}), "
          f"L01 pilot skipped ===\n")
    for g in GRADES:
        steps = _plan_for_grade(g)
        total += len(steps)
        kinds = {}
        for kind, *_ in steps:
            kinds[kind] = kinds.get(kind, 0) + 1
        n_les = len({lid for lid, (gg, n) in banked.items() if gg == g})
        print(f"  {g}: {n_les} banked lessons -> {kinds}")
    print(f"\n  TOTAL objects to create/repoint: {total}. Only banked lessons touched; single-form lessons "
          f"untouched. Re-run with --live to push.")


def run_live():
    import requests
    load_env()
    if not os.environ.get("PP100_QUICK_BANK_DEPTH"):
        print("PP100_QUICK_BANK_DEPTH not set - overlay OFF, nothing to push. Set it and re-run."); return 2
    if not (os.environ.get("TIMEBACK_CLIENT_ID") and os.environ.get("TIMEBACK_CLIENT_SECRET")):
        print("LIVE needs TIMEBACK creds (../.env)."); return 2
    from g9_push_live import get_token
    session = requests.Session(); session.verify = False
    session.headers.update({"Authorization": f"Bearer {get_token()}", "Content-Type": "application/json"})
    cp = os.path.join(ROOT, "PP100_QUICKBANK_CHECKPOINT.json")
    done = json.load(open(cp)) if os.path.exists(cp) else {"ok": []}
    okset = set(done["ok"])
    ok_n = fail_n = 0
    for g in GRADES:
        steps = _plan_for_grade(g)
        print(f"=== {g}: pushing {len(steps)} objects ===")
        for kind, oid, method, url, body in steps:
            key = f"{method}:{oid}"
            if key in okset:
                continue
            r, err = _req(session, method, url, body)
            code = r.status_code if r is not None else err
            ok = r is not None and (r.status_code in (200, 201) or r.status_code == 409)
            if ok:
                ok_n += 1; okset.add(key)
                done["ok"] = sorted(okset); json.dump(done, open(cp, "w"), indent=1)
            else:
                fail_n += 1
                print(f"  FAIL {method} {kind} {oid}: {code}  {(r.text[:160] if r is not None else err)}")
        print(f"  {g} done ({ok_n} ok so far, {fail_n} failed)")
    print(f"\n  QUICK BANKS pushed: {ok_n} ok, {fail_n} failed."
          + ("  All banked lessons now round-robin on retry." if not fail_n else "  (see failures above; re-run resumes)"))
    return 1 if fail_n else 0


def main():
    args = sys.argv[1:]
    if "--live" in args:
        return run_live()
    print_dry(); return 0


if __name__ == "__main__":
    sys.exit(main())
