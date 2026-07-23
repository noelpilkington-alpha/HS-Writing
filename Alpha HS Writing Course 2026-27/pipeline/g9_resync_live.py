"""
g9_resync_live.py  -  UPSERT re-sync of the full G9 course tree to the current v3.1 source.

WHY: the live G9 tree is a STALE PARTIAL push predating the current v3.1 structure. Audit (2026-07-23): of
298 current-source slot-items, only 103 are live and 195 are 404; the 103 live are partly stale content; the
old G9_PUSH_CHECKPOINT marks 126 current ids "done" (so a plain g9_push_live re-run would SKIP them) and holds
186 orphan ids from the old structure. So neither a resume nor a POST-only re-run fixes it.

WHAT: rebuild EVERY payload from source exactly as g9_push_live.main() does (same sanitize + XML-validate +
builders, so content is byte-identical to what the pipeline certifies), then UPSERT each: POST to create; on
409 (already exists) PUT the same payload as a full replace so stale live content is refreshed. Ignores the
stale checkpoint entirely (fresh run), writes its own resync checkpoint. Dependency order: stimuli -> items ->
tests. FRQs push as BASIC extended-text (no grader) here, exactly like the original push; g9_wire_grader.py
adds the ExternalApiScore wiring in a SECOND pass (its own PUT) once these items exist.

NOTE (timeback RULE): PUT is a full replace + a round-tripped GET drops the interaction, so we PUT the
FRESHLY-BUILT payload (never a GET round-trip) - identical to how g9_wire_grader rebuilds-from-source.

Usage:
  python pipeline/g9_resync_live.py            # DRY (default): build + validate, show create/update counts
  python pipeline/g9_resync_live.py --live      # LIVE: upsert (POST, PUT-on-409) all G9 items + tests
"""
from __future__ import annotations
import os, sys, json, time, glob

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)

from g9_push_dryrun import _load, STIM
from g9_push_live import (get_token, load_env, QTI_BASE, RETRY_ON, BACKOFF, KIND_QTI,
                          stimulus_payload, display_payload, frq_payload, choice_payload,
                          stimulus_item_payload, test_payload)

CHECKPOINT = os.path.join(ROOT, "G9_RESYNC_CHECKPOINT.json")
DISPLAY_KINDS = {"teach_card", "stimulus_display", "annotated_before_after"}


def build_plan():
    """Identical plan to g9_push_live.main(): (kind, id, endpoint_key, body) for every current-source object."""
    lessons = []
    for f in sorted(glob.glob(os.path.join(ROOT, "Lesson_Bank_G9", "lesson_g9_l*_v3_1.py"))):
        if "_deprecated" in f:
            continue
        m = _load(f)
        L = getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0]
        if L:
            lessons.append(L)
    bound = sorted({s.ref for L in lessons for s in L.slots if getattr(s, "ref", "")})
    plan = []
    for sid in bound:
        plan.append(("stimulus", sid, "stimulus", stimulus_payload(sid, STIM[sid])))
    for L in lessons:
        item_ids = []
        cur_src = None
        for i, s in enumerate(L.slots):
            iid = f"{L.id}-S{i+1:02d}-{s.kind}"
            item_ids.append(iid)
            if s.kind == "stimulus_display" and getattr(s, "ref", ""):
                cur_src = s.ref
            if s.kind in DISPLAY_KINDS:
                ref = s.ref if (s.kind == "stimulus_display" and getattr(s, "ref", "")) else cur_src
                plan.append(("item", iid, "item", display_payload(iid, s, stimulus_ref=ref)))
            elif s.kind in ("production_frq", "diagnosis_frq"):
                plan.append(("item", iid, "item", frq_payload(iid, s, stimulus_ref=cur_src)))
            elif KIND_QTI.get(s.kind) == "choice":
                plan.append(("item", iid, "item", choice_payload(iid, s)))
            else:
                plan.append(("item", iid, "item", stimulus_item_payload(iid, s)))
        plan.append(("test", L.id, "test", test_payload(L, item_ids)))
    return plan, len(bound), len(lessons)


_EP = {"stimulus": "stimuli", "item": "assessment-items", "test": "assessment-tests"}


def upsert(session, kind, oid, body):
    """POST to create; on 409 (exists) PUT the same payload (full replace) so stale content is refreshed."""
    import requests
    coll = _EP[kind]
    for attempt in range(4):
        try:
            r = session.post(f"{QTI_BASE}/{coll}", json=body, timeout=90)
        except requests.RequestException as e:
            if attempt < 3:
                time.sleep(BACKOFF[attempt]); continue
            return False, 0, f"network error: {e}"
        if r.status_code in (200, 201):
            return True, r.status_code, "created"
        if r.status_code == 409 or "already exists" in (r.text or "").lower():
            # exists -> PUT the freshly-built payload as a full replace (refresh stale content)
            for a2 in range(4):
                try:
                    pr = session.put(f"{QTI_BASE}/{coll}/{oid}", json=body, timeout=90)
                except requests.RequestException as e:
                    if a2 < 3:
                        time.sleep(BACKOFF[a2]); continue
                    return False, 0, f"network error (put): {e}"
                if pr.status_code in (200, 201):
                    return True, pr.status_code, "updated (put)"
                if pr.status_code in RETRY_ON and a2 < 3:
                    time.sleep(BACKOFF[a2]); continue
                return False, pr.status_code, "PUT: " + (pr.text or "")[:250]
        if r.status_code in RETRY_ON and attempt < 3:
            time.sleep(BACKOFF[attempt]); continue
        return False, r.status_code, (r.text or "")[:250]
    return False, 0, "exhausted retries"


def main(live=False):
    plan, n_stim, n_less = build_plan()
    n_items = sum(1 for k, *_ in plan if k == "item")
    print(f"G9 resync plan: {len(plan)} objects ({n_stim} stimuli, {n_items} items, {n_less} tests). "
          f"Built + sanitized + XML-validated from current v3.1 source.")
    if not live:
        print("DRY mode (default). Re-run with --live to UPSERT (POST create / PUT-on-409 refresh).")
        return 0
    load_env()
    if not (os.environ.get("TIMEBACK_CLIENT_ID") and os.environ.get("TIMEBACK_CLIENT_SECRET")):
        print("LIVE needs TIMEBACK_CLIENT_ID / TIMEBACK_CLIENT_SECRET (load ../.env)."); return 2
    import requests
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {get_token()}", "Content-Type": "application/json"})
    done = json.load(open(CHECKPOINT)) if os.path.exists(CHECKPOINT) else {"ok": [], "fail": []}
    okset = set(done["ok"]); done["fail"] = []
    created = updated = fail = 0
    # dependency order: stimuli -> items -> tests
    for want in ("stimulus", "item", "test"):
        for kind, oid, ep, body in plan:
            if kind != want or oid in okset:
                continue
            good, status, detail = upsert(session, kind, oid, body)
            if good:
                okset.add(oid); done["ok"].append(oid)
                if "updated" in detail:
                    updated += 1
                else:
                    created += 1
            else:
                fail += 1; done["fail"].append({"id": oid, "kind": kind, "status": status, "detail": detail})
                print(f"  FAIL [{status}] {kind} {oid}: {detail}")
            json.dump({"ok": sorted(okset), "fail": done["fail"]}, open(CHECKPOINT, "w"), indent=1)
    print(f"\nG9 resync: created {created}, updated {updated}, failed {fail}.")
    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main(live="--live" in sys.argv))
