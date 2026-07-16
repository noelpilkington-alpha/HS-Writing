"""
g9_push_live.py  -  LIVE push of the G9 slice to the current Timeback surface (qti.alpha-1edtech.ai).

ADAPTER DECISION (2026-07-12): per-item TimebackCurrent, NOT the qti-package import. Rationale: the env
credentials target this surface (Cognito IDP + qti.alpha-1edtech.ai + api.alpha-1edtech.ai); the `timeback`
skill documents exactly this per-item contract; per-item is DEBUGGABLE (a failed item names itself, vs an
opaque package import); the qti-package import is the end-goal Platform3 (Andy's Vercel build) which the env
does not point at. Get it reviewable on the reachable surface first.

Builds real QTI payloads per the `timeback` skill (create-stimulus / create-mcq / create-frq / create-test),
runs sanitize_html_for_xhtml on every HTML field, validates XML locally, and POSTs in dependency order
(stimuli -> items -> assessment-tests). 409 = already-exists = success (idempotent). Retries [5,15,30]s on
429/5xx. Writes a checkpoint after every successful call so a mid-run failure is resumable.

FRQ SCORING NOTE: the external grader is NOT live yet (Stage 09). FRQs push as BASIC extended-text now - they
accept student responses + render for review; the ExternalApiScore route is added by a PUT update once the
grader deploys (no re-push of content). This gets the course reviewable ASAP, which is the priority.

Usage:
  python pipeline/g9_push_live.py            # DRY (default): builds + sanitizes + validates, no network
  python pipeline/g9_push_live.py --live     # LIVE: auth + real POSTs (requires .env creds)
"""
from __future__ import annotations
import os, sys, re, json, time, html as _html
import xml.etree.ElementTree as ET

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import stylize
from xp_allocation import expected_xp
from g9_push_dryrun import build_g9_plan, _load, _stim_html, _choice_options, STIM, KIND_QTI

QTI_BASE = "https://qti.alpha-1edtech.ai/api"
TOKEN_URL = "https://prod-beyond-timeback-api-2-idp.auth.us-east-1.amazoncognito.com/oauth2/token"
CHECKPOINT = os.path.join(ROOT, "G9_PUSH_CHECKPOINT.json")
RETRY_ON = {429, 500, 502, 503, 504}
BACKOFF = [5, 15, 30]

_VOID = re.compile(r'<(br|hr|col|embed|input|link|meta|param|source|track|wbr)(\s[^>]*)?\s*(?<!/)\s*>')


def sanitize_html_for_xhtml(html: str) -> str:
    """Verbatim from the timeback skill: self-close voids, escape bare < and &, fix boolean attrs."""
    html = _VOID.sub(r'<\1\2/>', html or "")
    html = re.sub(r'<img((?:\s+[^>]*?)?)(?<!/)>', r'<img\1/>', html)
    html = re.sub(r'<(?![a-zA-Z/!])', '&lt;', html)
    html = re.sub(r'&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)', '&amp;', html)
    for attr in ("allowfullscreen", "disabled", "checked", "selected", "readonly",
                 "required", "autofocus", "autoplay", "controls", "loop", "muted"):
        html = re.sub(rf'(<[^>]*\s){attr}(?=[\s/>])', rf'\1{attr}="{attr}"', html)
    return html


def _san_verify(html: str, ctx: str) -> str:
    """Sanitize + assert it parses as XML (Timeback parses content as XML). Raise on failure."""
    s = sanitize_html_for_xhtml(html)
    try:
        ET.fromstring(f"<root>{s}</root>")
    except ET.ParseError as e:
        raise ValueError(f"XHTML invalid after sanitize [{ctx}]: {e}")
    return s


# ---- build real payloads (per the timeback skill) ----------------------------------------------------------

def stimulus_payload(sid, rec):
    return {"identifier": sid, "title": (getattr(rec, "topic_id", "") or sid)[:120],
            "content": _san_verify(_stim_html(rec), f"stimulus {sid}")}


def _reveal_text(slot):
    """The answer-key / explanation text for a choice item: the slot feedback if present, else the
    Correct:/Reveal: tail of the body. Delivered as metadata.explanation (shown after answering) - NEVER in the
    prompt, which would spoil the answer."""
    fb = (slot.feedback or "").strip()
    if fb:
        return re.sub(r"<[^>]+>", " ", fb).strip()
    body = re.sub(r"<[^>]+>", " ", slot.body or "")
    rev = re.search(r"\b(Correct:|Reveal:)", body, re.I)
    return body[rev.start():].strip() if rev else ""


def choice_payload(item_id, slot):
    opts, correct = _choice_options(slot)
    # PROMPT = stem ONLY. The options are rendered by the platform from `choices`; the answer key goes to
    # metadata.explanation. Rendering options/reveal in the prompt duplicated the options + spoiled the answer.
    stem = _san_verify(stylize.stylize_slot(slot, stem_only=True), f"choice {item_id}")
    choices = [{"identifier": o["identifier"], "content": _san_verify(o["content"], f"{item_id} opt")} for o in (opts or [])]
    md = {}
    reveal = _reveal_text(slot)
    if reveal:
        md["explanation"] = reveal
    return {"identifier": item_id, "title": (slot.title or item_id)[:120], "type": "choice",
            "interaction": {"type": "choice", "responseIdentifier": "RESPONSE",
                            "shuffle": True, "maxChoices": 1,
                            "questionStructure": {"prompt": stem, "choices": choices}},
            "responseDeclarations": [{"identifier": "RESPONSE", "cardinality": "single",
                                      "baseType": "identifier",
                                      "correctResponse": {"value": [correct] if correct else []}}],
            "outcomeDeclarations": [
                {"identifier": "FEEDBACK", "cardinality": "single", "baseType": "identifier"},
                {"identifier": "FEEDBACK-INLINE", "cardinality": "single", "baseType": "identifier"}],
            "responseProcessing": {"templateType": "match_correct",
                                   "responseDeclarationIdentifier": "RESPONSE",
                                   "outcomeIdentifier": "FEEDBACK",
                                   "correctResponseIdentifier": "CORRECT",
                                   "incorrectResponseIdentifier": "INCORRECT",
                                   "inlineFeedback": {"outcomeIdentifier": "FEEDBACK-INLINE",
                                                      "variableIdentifier": "RESPONSE"}},
            "metadata": md}


# the fill-in-the-blank frame marker (author bodies use runs of underscores). When present, we reword the
# prompt so the student COPIES the frame into the box and completes it (plain extended-text has no inline
# blank fields; the essay grader needs the full sentence anyway). Decision 2026-07-13: copy-and-complete.
_BLANK = re.compile(r"_{3,}")


def _copy_and_complete(prompt_html: str) -> str:
    """If the prompt contains a blank frame (___), append a copy-and-complete instruction so the student knows
    to type the completed sentence into the box (the box is empty; the frame lives in the prompt text)."""
    if not _BLANK.search(prompt_html):
        return prompt_html
    note = ('<p style="margin:10px 0 0;padding:8px 12px;background:#ecfeff;color:#0e7490;border-radius:6px;'
            'font-size:16px;font-weight:600">Type the full sentence in the box below, filling in each blank '
            '(______) with your own words.</p>')
    return prompt_html + note


def _source_card(source_html: str) -> str:
    """A bordered 'Source' block to INLINE the framing source at the top of a scored FRQ prompt. Scored FRQs
    carry the external grader, and on this API an item cannot hold BOTH a grader AND a linked side-panel
    stimulus (each save-path wipes the other, verified 2026-07-13). So for scored writing tasks the source is
    inlined here; non-scored items use the native reading-pane stimulus-ref link instead."""
    return ('<div style="border:1px solid #e2e8f0;border-left:4px solid #0d9488;border-radius:8px;'
            'background:#f8fafc;padding:12px 14px;margin:8px 0;font-family:-apple-system,Segoe UI,Roboto,Arial,'
            'sans-serif"><div style="font-size:12px;font-weight:700;letter-spacing:.04em;color:#0f766e;'
            'text-transform:uppercase;margin-bottom:2px">Source</div>' + source_html + '</div>')


def frq_payload(item_id, slot, stimulus_ref=None, source_html=None):
    """Build the FRQ item. If source_html is given (scored FRQs), the framing source is INLINED into the prompt
    (grader + side-panel stimulus cannot coexist on this API - the grader wins on scored tasks). stimulus_ref is
    NOT set here (JSON `stimulus` field is dropped); non-scored items get a native reading-pane link via a
    follow-up XML-format PUT in g9_repush_items.link_stimulus."""
    task = _copy_and_complete(stylize.stylize_slot(slot))
    prompt = (_source_card(source_html) + task) if source_html else task
    prompt = _san_verify(prompt, f"frq {item_id}")
    md = {}
    if getattr(slot, "rubric_ref", ""):
        md["rubric"] = slot.rubric_ref   # rc.* config; external grader route added by PUT when Stage 09 is live
    return {"identifier": item_id, "title": (slot.title or item_id)[:120], "type": "extended-text",
            "interaction": {"type": "extended-text", "responseIdentifier": "RESPONSE",
                            "questionStructure": {"prompt": prompt}},
            "responseDeclarations": [{"identifier": "RESPONSE", "cardinality": "single", "baseType": "string"}],
            "outcomeDeclarations": [
                {"identifier": "SCORE", "cardinality": "single", "baseType": "float"},
                {"identifier": "FEEDBACK", "cardinality": "single", "baseType": "identifier"}],
            "responseProcessing": {"templateType": "match_correct"},
            "metadata": md}


def display_payload(item_id, slot, stimulus_ref=None):
    """ACKNOWLEDGE-TO-CONTINUE (decision 2026-07-13): a display-only slot (teach_card / stimulus_display /
    annotated_before_after) delivered as a choice item with a single 'Continue' option that IS the correct
    answer. The student reads the content in the prompt, picks Continue, and advances - no forced writing box
    on non-interactive content. A reading-pane source (if any) is attached in a follow-up XML PUT, not here."""
    body = _san_verify(stylize.stylize_slot(slot), f"display {item_id}")
    return {"identifier": item_id, "title": (slot.title or item_id)[:120], "type": "choice",
            "interaction": {"type": "choice", "responseIdentifier": "RESPONSE",
                            "shuffle": False, "maxChoices": 1,
                            "questionStructure": {"prompt": body,
                                                  "choices": [{"identifier": "CONTINUE",
                                                               "content": "Continue"}]}},
            "responseDeclarations": [{"identifier": "RESPONSE", "cardinality": "single",
                                      "baseType": "identifier",
                                      "correctResponse": {"value": ["CONTINUE"]}}],
            "outcomeDeclarations": [
                {"identifier": "SCORE", "cardinality": "single", "baseType": "float"},
                {"identifier": "FEEDBACK", "cardinality": "single", "baseType": "identifier"}],
            "responseProcessing": {"templateType": "match_correct"},
            "metadata": {"role": "instructional"}}


def stimulus_item_payload(item_id, slot):
    """A teach_card / worked-example / source-display slot delivered as an informational extended-text with a
    display-only prompt (student sees the content; no scored response expected)."""
    body = _san_verify(stylize.stylize_slot(slot), f"info {item_id}")
    return {"identifier": item_id, "title": (slot.title or item_id)[:120], "type": "extended-text",
            "interaction": {"type": "extended-text", "responseIdentifier": "RESPONSE",
                            "questionStructure": {"prompt": body}},
            "responseDeclarations": [{"identifier": "RESPONSE", "cardinality": "single", "baseType": "string"}],
            "outcomeDeclarations": [{"identifier": "SCORE", "cardinality": "single", "baseType": "float"}],
            "responseProcessing": {"templateType": "match_correct"},
            "metadata": {"role": "instructional"}}


def test_payload(L, item_ids):
    return {"identifier": L.id, "title": (L.title or L.id)[:120], "expected_xp": expected_xp(L),
            "qti-test-part": [{"identifier": "test_part", "navigationMode": "linear",
                               "submissionMode": "individual", "sequence": 1,
                               "qti-assessment-section": [{
                                   "identifier": "test_section", "title": "Lesson", "visible": True,
                                   "sequence": 1,   # this API build REQUIRES a section sequence (skill example omitted it)
                                   "qti-assessment-item-ref": [
                                       {"identifier": iid, "href": f"{iid}.xml", "sequence": n + 1}
                                       for n, iid in enumerate(item_ids)]}]}],
            "outcomeDeclarations": [{"identifier": "SCORE", "cardinality": "single", "baseType": "float"}]}


# ---- live plumbing -----------------------------------------------------------------------------------------

def get_token():
    import requests
    cid, secret = os.environ.get("TIMEBACK_CLIENT_ID"), os.environ.get("TIMEBACK_CLIENT_SECRET")
    if not (cid and secret):
        raise SystemExit("Missing TIMEBACK_CLIENT_ID / TIMEBACK_CLIENT_SECRET (load the .env).")
    r = requests.post(TOKEN_URL, data={"grant_type": "client_credentials", "client_id": cid,
                                       "client_secret": secret},
                      headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=30)
    r.raise_for_status()
    return r.json()["access_token"]


def post(session, url, body, ctx):
    """POST with retry + 409-as-success. Returns (ok, status, detail)."""
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
        if r.status_code == 409:
            return True, 409, "already exists (idempotent)"
        if r.status_code in RETRY_ON and attempt < 3:
            time.sleep(BACKOFF[attempt]); continue
        return False, r.status_code, (r.text or "")[:300]
    return False, 0, "exhausted retries"


def load_env():
    envp = os.path.join(ROOT, "..", ".env")   # HS Writing/.env
    if os.path.exists(envp):
        for line in open(envp, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def main(live=False):
    lessons = []
    import glob
    # VERIFIED LIVE SET ONLY (see g9_push_dryrun.build_g9_plan): the broad 'lesson_g9_l[0-9]*.py' also loads
    # superseded v1/v2/v3 files with colliding lesson IDs (24/29 collide) + 2 deprecated lessons, making the
    # pushed content non-deterministic. Use the v3.1 pattern the deterministic pipeline certifies. Fixed 2026-07-16.
    for f in sorted(glob.glob(os.path.join(ROOT, "Lesson_Bank_G9", "lesson_g9_l*_v3_1.py"))):
        if "_deprecated" in f:
            continue
        m = _load(f)
        L = getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0]
        if L:
            lessons.append(L)
    bound = sorted({s.ref for L in lessons for s in L.slots if getattr(s, "ref", "")})

    # build every payload (this also sanitizes + XML-validates; raises on any bad HTML BEFORE we touch network)
    plan = []
    for sid in bound:
        plan.append(("stimulus", sid, stimulus_payload(sid, STIM[sid])))
    # kinds delivered as ACKNOWLEDGE-TO-CONTINUE display items (no writing box). diagnosis_frq is NOT here:
    # it is a genuine (ungraded) writing task and keeps its response box via frq_payload.
    DISPLAY_KINDS = {"teach_card", "stimulus_display", "annotated_before_after"}
    for L in lessons:
        item_ids = []
        # nearest-preceding source: each writing/display slot links the most recent stimulus_display's ref in
        # this lesson, so the framing source renders in the reading pane beside the task.
        cur_src = None
        for i, s in enumerate(L.slots):
            iid = f"{L.id}-S{i+1:02d}-{s.kind}"
            item_ids.append(iid)
            if s.kind == "stimulus_display" and getattr(s, "ref", ""):
                cur_src = s.ref
            if s.kind in DISPLAY_KINDS:
                # a stimulus_display links ITS OWN source; teach/before-after link the current source if any
                ref = s.ref if (s.kind == "stimulus_display" and getattr(s, "ref", "")) else cur_src
                plan.append(("item", iid, display_payload(iid, s, stimulus_ref=ref)))
            elif s.kind in ("production_frq", "diagnosis_frq"):
                plan.append(("item", iid, frq_payload(iid, s, stimulus_ref=cur_src)))
            elif KIND_QTI.get(s.kind) == "choice":
                plan.append(("item", iid, choice_payload(iid, s)))
            else:
                plan.append(("item", iid, stimulus_item_payload(iid, s)))
        plan.append(("test", L.id, test_payload(L, item_ids)))

    print(f"G9 push plan built + sanitized + XML-validated: {len(plan)} objects "
          f"({len(bound)} stimuli, {len(lessons)} tests). All HTML XHTML-valid.")
    if not live:
        print("DRY mode (default). Re-run with --live to push. No network call made.")
        return 0

    load_env()
    import requests
    token = get_token()
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    ep = {"stimulus": f"{QTI_BASE}/stimuli", "item": f"{QTI_BASE}/assessment-items",
          "test": f"{QTI_BASE}/assessment-tests"}
    done = json.load(open(CHECKPOINT)) if os.path.exists(CHECKPOINT) else {"ok": [], "fail": []}
    okset = set(done["ok"])
    print(f"LIVE push starting. {len(okset)} already done (resume). Order: stimuli -> items -> tests.")
    for kind, oid, body in plan:
        if oid in okset:
            continue
        ok, status, detail = post(session, ep[kind], body, f"{kind} {oid}")
        if ok:
            okset.add(oid); done["ok"].append(oid)
        else:
            done["fail"].append({"id": oid, "kind": kind, "status": status, "detail": detail})
            print(f"  FAIL [{status}] {kind} {oid}: {detail}")
        json.dump({"ok": sorted(okset), "fail": done["fail"]}, open(CHECKPOINT, "w"), indent=1)
    print(f"\nLIVE push done: {len(okset)} ok, {len(done['fail'])} failed. Checkpoint -> {CHECKPOINT}")
    return 0 if not done["fail"] else 1


if __name__ == "__main__":
    sys.exit(main(live="--live" in sys.argv))
