"""
g9_wire_grader.py  -  wire the LIVE grader URL into the already-pushed G9 production FRQs (no re-push).

The G9 FRQs are live as basic extended-text (they accept responses but do not auto-score). Once the grader is
deployed and you have its /score URL, this attaches the Timeback ExternalApiScore customOperator + rubricBlock
to each SCORED production FRQ via PUT (rebuild-from-source -> add grader config -> PUT full item back). Content
is NOT re-pushed; only the scoring wiring is added.

PUT is a FULL REPLACE on this API - so we rebuild the exact known-good FRQ payload the original push used and
PUT it back with the grader config added, or the item's content is silently cleared (timeback RULE 3).

GRADER CONTRACT (verified 2026-07-16 against the writing-grader service, api/external_score.py):
  - endpoint: POST {BASE}/score  (router mounted at root, NO prefix - NOT the older /timeback/score)
  - request: RUBRIC-BASED {response, rubric, grade, prompt, passage} (defensive superset), routed by the
    `rubric` field server-side - NOT the older {identifier}-parsing design.
  - REGENERATION CONTRACT (2026-07-21): each scored FRQ declares (unit, frq_type, rubric_ref). The wirer bakes
    the DECLARED grain+frq_type into the grader URL (?grain=&frq_type=) so /score routes off them; rubric_ref
    stays in the rubricBlock. sentence -> panel sentence scorers (Skill/Answer + Conv); essay/multi_paragraph
    -> the essay engines (rc.sbac scores rc.staar items via the route-only alias). paragraph is reserved
    (grader 501 until G9-12 calibrated). rc.ap deprecated -> 503 (G11/G12 now use rc.4trait).
The grader URL is carried in the item's customOperator.definition; the rubric is carried in the rubricBlock.

Usage:
  python pipeline/g9_wire_grader.py https://writing-grader.onrender.com            # DRY (default): plan
  python pipeline/g9_wire_grader.py https://writing-grader.onrender.com --live      # LIVE: PUT updates
"""
from __future__ import annotations
import os, sys, glob, re, json, time

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
from g9_push_dryrun import _load
from g9_push_live import get_token, load_env, QTI_BASE, frq_payload  # reuse auth + the known-good FRQ builder
import requests

RETRY_ON = {429, 500, 502, 503, 504}
BACKOFF = [5, 15, 30]

# rubric_ref -> the scorer rubricBlock data-part divs the platform requires to display/route grading.
# ESSAY-grain blocks (the standard family the essay engines score against).
_RUBRIC_BLOCKS = {
    "rc.staar": '<div data-part="development">STAAR Organization &amp; Development of Ideas (0-3)</div>'
                '<div data-part="conventions">STAAR Conventions (0-2)</div>',
    "rc.ap": '<div data-part="thesis">AP Row A Thesis (0-1)</div>'
             '<div data-part="evidence">AP Row B Evidence &amp; Commentary (0-4)</div>'
             '<div data-part="sophistication">AP Row C Sophistication (0-1)</div>',
}

# SHORT-GRAIN blocks (regeneration contract): a sentence task is scored by the sentence panel scorers
# (Skill/Answer + Conventions), NOT the essay rubric — so the student-visible block must match. Keyed by
# (grain, frq_type). Paragraph is reserved (grader returns 501 until G9-12 calibrated) — no block emitted yet.
_GRAIN_RUBRIC_BLOCKS = {
    ("sentence", "revision"): '<div data-part="skill">Skill Application (0-1)</div>'
                              '<div data-part="conventions">Conventions (0-1)</div>',
    ("sentence", "writing"):  '<div data-part="answer">Answer Quality (0-2)</div>'
                              '<div data-part="conventions">Conventions (0-1)</div>',
    # paragraph -> panel_joey 3-trait /10 (G9-12 analytical-paragraph band)
    ("paragraph", "revision"): '<div data-part="ideas">Ideas &amp; Content (0-3)</div>'
                               '<div data-part="organization">Organization &amp; Structure (0-3)</div>'
                               '<div data-part="conventions">Conventions (0-4)</div>',
    ("paragraph", "writing"):  '<div data-part="ideas">Ideas &amp; Content (0-3)</div>'
                               '<div data-part="organization">Organization &amp; Structure (0-3)</div>'
                               '<div data-part="conventions">Conventions (0-4)</div>',
}


def _grader_url_for(base_url: str, unit: str, frq_type: str) -> str:
    """Bake the DECLARED (grain, frq_type) into the grader definition URL (regeneration contract).

    The grader routes off these query params; rubric_ref stays stable in the item. Essay/multi_paragraph
    carry no grain (back-compat: the grader defaults absent-grain -> essay). Sentence/paragraph carry both.
    """
    if unit in ("sentence", "paragraph"):
        sep = "&" if "?" in base_url else "?"
        return f"{base_url}{sep}grain={unit}&frq_type={frq_type or 'writing'}"
    return base_url


def g9_production_frq_items():
    """(item_id, slot, source_html) for every SCORED production_frq in the LIVE G9 course.

    SOURCE OF TRUTH: the VERIFIED v3.1 course (_GRADE_GLOB['G9'] = 'lesson_g9_l*_v3_1.py'), the same 27
    lessons the deterministic floor + fact-verification pass certified. This deliberately does NOT use the
    broad 'lesson_g9_l[0-9]*.py' glob: that also matches the superseded v1/v2/v3 files, which share lesson
    IDs with the v3.1 versions (24 of 29 ids collide) and pull in 2 deprecated lessons (C901-0002,
    C905-0005) that were dropped in the re-architecture. Wiring the grader onto stale/dead item IDs (or a
    version whose slot count differs, shifting every -S{i} suffix) would attach scoring to the wrong items.
    Fixed 2026-07-16 (found while prepping the graded pilot).

    source_html is the nearest-preceding stimulus_display's source, INLINED into the prompt (a scored FRQ
    keeps the grader, and grader + a linked side-panel stimulus cannot coexist on this API - so the source is
    inlined). The grader wire must re-inline it, or the JSON-PUT rebuild would drop the Source card."""
    from g9_push_dryrun import STIM, _stim_html
    from mastery_targets_grade import _GRADE_GLOB
    subdir, pat = _GRADE_GLOB["G9"]
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, subdir, pat))):
        if "_deprecated" in f:
            continue
        m = _load(f)
        L = getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0]
        if not L:
            continue
        cur_src = None
        for i, s in enumerate(L.slots):
            if s.kind == "stimulus_display" and getattr(s, "ref", ""):
                cur_src = s.ref
            if s.kind == "production_frq" and getattr(s, "scored", False) and getattr(s, "rubric_ref", ""):
                rec = STIM.get(cur_src) if cur_src else None
                src_html = _stim_html(rec) if rec else None
                out.append((f"{L.id}-S{i+1:02d}-{s.kind}", s, src_html))
    return out


def wire_payload(item_id, slot, grader_url, source_html=None):
    """Rebuild the known-good FRQ payload FROM SOURCE and attach the external grader config.

    We do NOT round-trip the live item: a GET returns the interaction only inside `rawXml` (no top-level
    `interaction` JSON field), so PUTting the parsed JSON drops the interaction and the API rejects the item
    as malformed ("missing its interaction"). Extended-text is JSON-safe (timeback RULE 1), so rebuilding the
    exact payload the original push used - then swapping match_correct for the ExternalApiScore operator and
    adding the 5 grader outcome declarations + rubricBlock - is faithful and idempotent. source_html re-inlines
    the framing Source card so the grader wire does not drop it.
    """
    p = frq_payload(item_id, slot, source_html=source_html)   # identical to what was pushed live (prompt + source)
    rubric = getattr(slot, "rubric_ref", "") or "rc.staar"
    unit = getattr(slot, "unit", "") or ""
    frq_type = getattr(slot, "frq_type", "") or ""
    # REGENERATION CONTRACT: bake the declared (grain, frq_type) into the grader URL so /score routes off them.
    definition = _grader_url_for(grader_url, unit, frq_type)
    p["responseProcessing"] = {"templateType": "custom",
                               "customOperator": {"class": "com.alpha-1edtech.ExternalApiScore",
                                                  "definition": definition}}
    # rubricBlock must MATCH the scorer the grain routes to: sentence -> short-grain block; else essay block.
    grain_block = _GRAIN_RUBRIC_BLOCKS.get((unit, frq_type or "writing"))
    block = grain_block if grain_block else _RUBRIC_BLOCKS.get(rubric, _RUBRIC_BLOCKS["rc.staar"])
    p["rubricBlock"] = {"view": "scorer", "content": block}
    p["outcomeDeclarations"] = [
        {"identifier": "SCORE", "cardinality": "single", "baseType": "float"},
        {"identifier": "FEEDBACK", "cardinality": "single", "baseType": "identifier"},
        {"identifier": "API_RESPONSE", "cardinality": "single", "baseType": "string"},
        {"identifier": "GRADING_RESPONSE", "cardinality": "single", "baseType": "string"},
        {"identifier": "FEEDBACK_VISIBILITY", "cardinality": "single", "baseType": "boolean"}]
    return p


def put_item(session, item_id, slot, grader_url, live, source_html=None):
    """Rebuild the FRQ from source with the grader config and PUT it back (full replace)."""
    item = wire_payload(item_id, slot, grader_url, source_html=source_html)
    if not live:
        return True, 0, "DRY: would PUT rebuilt payload with grader config"
    for attempt in range(4):
        pr = session.put(f"{QTI_BASE}/assessment-items/{item_id}", json=item, timeout=60)
        if pr.status_code in (200, 201):
            return True, pr.status_code, "wired"
        if pr.status_code in RETRY_ON and attempt < 3:
            time.sleep(BACKOFF[attempt]); continue
        return False, pr.status_code, (pr.text or "")[:200]
    return False, 0, "exhausted retries"


def normalize_grader_url(url: str) -> str:
    """Accept a Render base url or a full endpoint; return the ExternalApiScore endpoint url.

    LIVE GRADER CONTRACT (verified 2026-07-16 against api/external_score.py): the writing-grader service
    mounts the ExternalApiScore router at ROOT with NO prefix, so the endpoint is `/score` (POST). The
    request is RUBRIC-BASED - {response, rubric, grade, prompt, passage} (a defensive superset; see
    external_score.ScoreRequest) - NOT the older {identifier}-routing '/timeback/score' design a prior
    version used. So a bare host gets '/score' appended; an explicit '/score' (or a legacy
    '/timeback/score', left as-given for back-compat) is preserved.
    """
    url = url.rstrip("/")
    if url.endswith("/score"):          # covers both '/score' and legacy '/timeback/score'
        return url
    return url + "/score"


def main(grader_url, live=False):
    if not (grader_url.startswith("http://") or grader_url.startswith("https://")):
        raise SystemExit("grader URL must start with http:// or https://")
    grader_url = normalize_grader_url(grader_url)
    items = g9_production_frq_items()
    print(f"G9 production FRQs to wire to grader: {len(items)} (rubric rc.staar). URL: {grader_url}")
    if not live:
        print("DRY mode. Re-run with --live to PUT. No network call made.")
        return 0
    load_env()
    tok = get_token()
    s = requests.Session(); s.headers.update({"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    ok = fail = 0
    for item_id, slot, source_html in items:
        good, status, detail = put_item(s, item_id, slot, grader_url, live=True, source_html=source_html)
        if good:
            ok += 1
        else:
            fail += 1; print(f"  FAIL [{status}] {item_id}: {detail}")
    print(f"\nwired {ok} FRQs, {fail} failed.")
    return 0 if not fail else 1


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--live"]
    url = args[0] if args else "https://GRADER-URL-HERE/score"
    sys.exit(main(url, live="--live" in sys.argv))
