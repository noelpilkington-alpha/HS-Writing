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
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

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
    # rc.4trait = NY Regents 4-criterion analytic (G11/G12 CCSS), scored by panel_ccss. The per-criterion
    # ceiling varies by mode (argument 0-6 x4 = 24 | analysis 0-4 x4 = 16); the student-visible block names
    # the four criteria without pinning a scale (the grader returns the mode-correct max in maxScore).
    "rc.4trait": '<div data-part="content_analysis">Content &amp; Analysis</div>'
                 '<div data-part="command_of_evidence">Command of Evidence</div>'
                 '<div data-part="coherence_org_style">Coherence, Organization &amp; Style</div>'
                 '<div data-part="control_of_conventions">Control of Conventions</div>',
    # rc.ap retained for any legacy caller; the deployed grader 503s it (superseded by rc.4trait for G11/G12).
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


def _grader_url_for(base_url: str, unit: str, frq_type: str, mode: str = "") -> str:
    """Bake the DECLARED (grain, frq_type[, mode]) into the grader definition URL (regeneration contract).

    The grader routes off these query params; rubric_ref stays stable in the item. Essay/multi_paragraph
    carry no grain (back-compat: the grader defaults absent-grain -> essay). Sentence/paragraph carry both.
    `mode` (rc.4trait TASK PROFILE: argument|analysis) is baked ONLY when the slot declares it — an empty mode
    lets the grader apply its rc.4trait default (argument), so only analysis essays carry ?mode=analysis. mode
    is orthogonal to grain, so it can ride ALONGSIDE grain (short-grain rc.4trait) OR alone (essay-grain).

    IDEMPOTENT: any pre-existing grain/frq_type/mode on `base_url` is stripped before the computed params are
    re-added, so passing an already-parameterized URL (e.g. a re-wire of a live item's current definition)
    yields the same result instead of doubling params (the 2026-07-24 L01 doubled-param bug). Query keys we do
    NOT manage are preserved.
    """
    parts = urlsplit(base_url)
    # drop only the keys this wirer owns; keep any other query the caller set
    kept = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
            if k not in ("grain", "frq_type", "mode")]
    if unit in ("sentence", "paragraph"):
        kept.append(("grain", unit))
        kept.append(("frq_type", frq_type or "writing"))
    if mode:
        kept.append(("mode", mode))
    # urlencode with safe='' keeps values readable; order is deterministic (kept-first, then grain/frq_type/mode)
    new_query = urlencode(kept)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, new_query, parts.fragment))


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


# NATIVE grader (AlphaTest AI grader): the SAME customOperator class, but Timeback's OWN hosted definition
# URL (inherently allowlist-approved) + a full authored grading prompt carried in a
# <qti-rubric-block use="ext:grading-prompt" view="scorer">. Split decision (2026-07-24): SENTENCE grain ->
# native (removes the allowlist/AWS dependency for the largest slice); paragraph+ -> Render (purpose-built
# panels; pending the Render host resolution).
NATIVE_GRADER_URL = "https://alphatest.alpha.school/prod/ai-grading"


def _native_prompt_for(unit, frq_type):
    """The authored native rubric-block grading prompt for a sentence route (or None if not sentence).
    Sentence scoring is rubric-agnostic (rc.staar==rc.4trait), so only (grain, frq_type) selects the prompt."""
    if unit != "sentence":
        return None
    try:
        sys.path.insert(0, os.path.join(HERE, "native_grader"))
        import native_prompts as _NP
        spec = _NP.SENTENCE_SPECS.get(("sentence", frq_type or "writing"))
        return _NP.rubric_block_text(spec) if spec else None
    except Exception:
        return None


def wire_payload(item_id, slot, grader_url, source_html=None, native=None):
    """Rebuild the known-good FRQ payload FROM SOURCE and attach the external grader config.

    We do NOT round-trip the live item: a GET returns the interaction only inside `rawXml` (no top-level
    `interaction` JSON field), so PUTting the parsed JSON drops the interaction and the API rejects the item
    as malformed ("missing its interaction"). Extended-text is JSON-safe (timeback RULE 1), so rebuilding the
    exact payload the original push used - then swapping match_correct for the ExternalApiScore operator and
    adding the 5 grader outcome declarations + rubricBlock - is faithful and idempotent. source_html re-inlines
    the framing Source card so the grader wire does not drop it.

    ROUTING (2026-07-24 split): sentence grain wires to the NATIVE grader (Timeback's hosted AI grader +
    an embedded ext:grading-prompt), everything else wires to the Render grader with the baked routing URL.
    `native` overrides the auto-decision (True/False); default None = auto (sentence -> native).
    """
    p = frq_payload(item_id, slot, source_html=source_html)   # identical to what was pushed live (prompt + source)
    rubric = getattr(slot, "rubric_ref", "") or "rc.staar"
    unit = getattr(slot, "unit", "") or ""
    frq_type = getattr(slot, "frq_type", "") or ""
    mode = getattr(slot, "mode", "") or ""   # rc.4trait TASK PROFILE (analysis essays only; else grader defaults argument)
    use_native = native if native is not None else (unit == "sentence")
    native_prompt = _native_prompt_for(unit, frq_type) if use_native else None

    if use_native and native_prompt:
        # NATIVE: Timeback's own hosted grader URL (no query routing - the rubric-block prompt carries the rubric)
        p["responseProcessing"] = {"templateType": "custom",
                                   "customOperator": {"class": "com.alpha-1edtech.ExternalApiScore",
                                                      "definition": NATIVE_GRADER_URL}}
        # the ext:grading-prompt rubric-block IS the grading spec the native grader reads.
        scale = 2 if (frq_type or "writing") == "revision" else 3
        p["nativeGradingPrompt"] = native_prompt
        p["scoreMax"] = scale
        p["rubricBlock"] = {"view": "scorer", "content": _GRAIN_RUBRIC_BLOCKS.get((unit, frq_type or "writing"), "")}
    else:
        # RENDER: bake the declared (grain, frq_type[, mode]) into the grader URL so /score routes off them.
        definition = _grader_url_for(grader_url, unit, frq_type, mode)
        p["responseProcessing"] = {"templateType": "custom",
                                   "customOperator": {"class": "com.alpha-1edtech.ExternalApiScore",
                                                      "definition": definition}}
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


_QTI_NS = "http://www.imsglobal.org/xsd/imsqtiasi_v3p0"
_XSI = "http://www.w3.org/2001/XMLSchema-instance"
_SCHEMA_LOC = (f"{_QTI_NS} https://purl.imsglobal.org/spec/qti/v3p0/schema/xsd/imsqti_asiv3p0_v1p0.xsd")

_BASETYPE = {"SCORE": "float", "FEEDBACK": "identifier", "API_RESPONSE": "string",
             "GRADING_RESPONSE": "string", "FEEDBACK_VISIBILITY": "boolean", "RESPONSE": "string"}


def _xattr(s: str) -> str:
    """Escape a value for an XML attribute (the grader URL: & -> &amp; etc.)."""
    return (str(s).replace("&", "&amp;").replace('"', "&quot;")
            .replace("<", "&lt;").replace(">", "&gt;"))


def item_to_xml_payload(item: dict) -> dict:
    """Serialize a wire_payload() item dict into the {format:xml,xml,metadata} POST/PUT body.

    WHY XML (CRITICAL RULE 1 + 2026-07-24 allowlist finding): the JSON->XML converter SILENTLY DROPS the
    customOperator - even for an allowlisted host - so a JSON-pushed FRQ ends up with an empty
    `<qti-response-processing template=".../custom.xml"/>` and NO grader in the executable rawXml (verified on
    the live L01 FRQ). The runtime executes rawXml, so the grader never fires. We must write the operator
    LITERALLY as `<qti-custom-operator class="com.alpha-1edtech.ExternalApiScore" definition="<url>"/>` inside
    `<qti-response-processing>` and POST/PUT as {"format":"xml","xml":...}. The prompt HTML is already
    sanitized XHTML (frq_payload -> _san_verify), so it is embedded verbatim inside <qti-prompt>.

    Modeled byte-for-byte on the live rawXml shape (extended-text FRQ + 5 grader outcome declarations).
    """
    iid = item["identifier"]
    title = _xattr(item.get("title", iid))
    prompt = item["interaction"]["questionStructure"]["prompt"]      # already XHTML-sanitized
    score_max = item.get("scoreMax")                                 # set for NATIVE items -> normal-maximum
    outcomes = ""
    for od in item.get("outcomeDeclarations", []):
        ident = od["identifier"]
        bt = od.get("baseType", _BASETYPE.get(ident, "string"))
        extra = ""
        if ident == "SCORE" and score_max is not None:
            # native items express the scale on the SCORE declaration (shipped-STC shape: normal-maximum/minimum)
            extra = f' normal-maximum="{score_max}" normal-minimum="0"'
        outcomes += (f'<qti-outcome-declaration identifier="{ident}" '
                     f'base-type="{bt}" cardinality="single"{extra}/>')
    definition = item["responseProcessing"]["customOperator"]["definition"]
    rp = (f'<qti-response-processing>'
          f'<qti-custom-operator class="com.alpha-1edtech.ExternalApiScore" definition="{_xattr(definition)}"/>'
          f'</qti-response-processing>')
    # NATIVE grading prompt: embed as <qti-rubric-block use="ext:grading-prompt" view="scorer"> at the TOP of
    # the item body (shipped-STC shape). The prompt text goes in <qti-content-body><pre> with XML entities
    # escaped (& < >), newlines preserved as literal &#10; so the native grader receives it verbatim.
    grading_block = ""
    native_prompt = item.get("nativeGradingPrompt")
    if native_prompt:
        esc = (native_prompt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
               .replace("\r\n", "\n").replace("\n", "&#10;"))
        grading_block = (f'<qti-rubric-block use="ext:grading-prompt" view="scorer">'
                         f'<qti-content-body><pre>{esc}</pre></qti-content-body></qti-rubric-block>')
    xml = (f'<?xml version="1.0" encoding="UTF-8"?>'
           f'<qti-assessment-item xmlns="{_QTI_NS}" xmlns:xsi="{_XSI}" xsi:schemaLocation="{_SCHEMA_LOC}" '
           f'identifier="{iid}" title="{title}" adaptive="false" time-dependent="false">'
           f'<qti-response-declaration identifier="RESPONSE" cardinality="single" base-type="string">'
           f'<qti-correct-response/></qti-response-declaration>'
           f'{outcomes}'
           f'<qti-item-body>{grading_block}'
           f'<qti-extended-text-interaction response-identifier="RESPONSE">'
           f'<qti-prompt>{prompt}</qti-prompt>'
           f'</qti-extended-text-interaction></qti-item-body>'
           f'{rp}'
           f'</qti-assessment-item>')
    # validate locally before it ever hits the wire (RULE 2: always ET.fromstring first)
    import xml.etree.ElementTree as ET
    ET.fromstring(xml)
    body = {"format": "xml", "xml": xml}
    md = dict(item.get("metadata") or {})
    rb = item.get("rubricBlock")
    if rb:
        # rubricBlock rides in metadata (the JSON field is dropped from rawXml; the grader routes off the URL
        # params + rubric anyway, but we keep the scorer-view block for the platform's grader UI).
        md["rubricBlock"] = rb
    if md:
        body["metadata"] = md
    return body


def put_item(session, item_id, slot, grader_url, live, source_html=None):
    """Rebuild the FRQ from source with the grader config and PUT it back (full replace) as XML.

    XML-format PUT (2026-07-24): a JSON PUT drops the customOperator from rawXml (CRITICAL RULE 1), so the
    grader never fires. We serialize to {format:xml} so the operator lands in the executable XML.
    """
    item = wire_payload(item_id, slot, grader_url, source_html=source_html)
    body = item_to_xml_payload(item)
    if not live:
        return True, 0, "DRY: would PUT XML payload with literal custom-operator"
    for attempt in range(4):
        pr = session.put(f"{QTI_BASE}/assessment-items/{item_id}", json=body, timeout=60)
        if pr.status_code in (200, 201):
            return True, pr.status_code, "wired (xml)"
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

    IDEMPOTENT on an already-parameterized URL: any query string (e.g. '?grain=sentence&frq_type=writing' a
    caller mistakenly passed in) is stripped here so we never append '/score' AFTER the query
    (the 2026-07-24 '...frq_type=writing/score' bug). _grader_url_for re-adds the routing params.
    """
    parts = urlsplit(url)
    path = parts.path.rstrip("/")
    if not path.endswith("/score"):     # covers both '/score' and legacy '/timeback/score'
        path = path + "/score"
    return urlunsplit((parts.scheme, parts.netloc, path, "", ""))


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
