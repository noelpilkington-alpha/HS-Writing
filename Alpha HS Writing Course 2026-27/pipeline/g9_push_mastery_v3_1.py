"""
g9_push_mastery_v3_1.py  -  push the per-lesson PP100 MASTERY assessment-tests for the v3.1 course structure.

Per icm/_config/course-structure.md, each v3.1 lesson's PP100 resource points at a single-item assessment-test
= the lesson's INDEPENDENT (production) FRQ, external-grader scored to the >=90 test-out. This builds + pushes,
per lesson:
  1. a grader-wired extended-text FRQ item   id = <lesson>-MASTERY-FRQ   (ExternalApiScore + rc.* rubricBlock)
  2. a single-item assessment-test           id = <lesson>-MASTERY       (points to the FRQ item)
The assemble step (g9_assemble_v3_1.py) already points each PP100 resource.metadata.url at
{QTI_BASE}/assessment-tests/<lesson>-MASTERY, so the ids MUST match (they are derived the same way here).

The INDEPENDENT FRQ is the "write the claim cold" task = the lesson's actual composition outcome (the doc's
Layer-3 mastery instrument). Its framing source is INLINED (a gated student cannot scroll back; grader + side
stimulus cannot coexist), same decision as the live G9 FRQs.

Usage:
  python pipeline/g9_push_mastery_v3_1.py https://hs-writing-grading.onrender.com            # DRY: plan only
  python pipeline/g9_push_mastery_v3_1.py https://hs-writing-grading.onrender.com --live      # LIVE: push
"""
from __future__ import annotations
import os, sys, glob, re, json, time

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
from g9_push_dryrun import _load, STIM, _stim_html
from g9_push_live import frq_payload, test_payload, get_token, QTI_BASE
from g9_wire_grader import wire_payload   # grader-attached FRQ payload (ExternalApiScore + rubricBlock)
# render the mastery prompt with the SAME gated-reading typography engine the in-article writes use, so the
# PP100 mastery task is formatted identically (bold key terms, per-line instructions, set-apart frame/source),
# not the flatter stylize path. _render_task passes frq_prompt-authored HTML through cleanly; _html_blocks +
# _render_body preserve the source structure.
from gated_reading import _render_task, _render_body, _html_blocks, _plain, esc, _xml_safe_entities, _render_source_block
from mastery_prompts_g9 import MASTERY as _AUTHORED_MASTERY  # per-lesson task-specific mastery prompts


def _mastery_for(L):
    """The effective mastery dict for a lesson: an inline L.mastery on the lesson file wins; else the authored
    per-lesson entry in mastery_prompts_g9.MASTERY; else {} (falls back to the generic held-out instruction)."""
    inline = getattr(L, "mastery", None)
    if inline and inline.get("prompt_html"):
        return inline
    return _AUTHORED_MASTERY.get(L.id, inline or {})


def _mastery_instruction(L, slot):
    """A COLD, topic-agnostic mastery instruction derived from the lesson's own skill (target + slot title),
    NOT the in-lesson slot body (which names the article's topic). The student applies the taught skill to the
    held-out source below. One instruction per line so _render_task formats it cleanly."""
    unit = getattr(slot, "unit", "") or "sentence"
    skill = (L.target or slot.title or "").strip()
    # trim the trailing rubric-trait sentence from the target if present
    skill = re.sub(r"\s*(Written at the.*|Trait:.*|Sentence then.*|Interleaves.*)$", "", skill).strip().rstrip(".")
    what = {"sentence": "Write ONE sentence", "paragraph": "Write ONE paragraph",
            "multi_paragraph": "Plan and write a short multi-paragraph response",
            "essay": "Plan and write a complete essay"}.get(unit, "Write your response")
    return (f"This is your mastery task. Read the NEW source above, which you have not seen in this lesson. "
            f"Then apply the skill you practiced: {skill}. {what} in response to this source. "
            f"Use the check tool from the lesson on your own work before you submit.")


def _mastery_prompt(L, slot, src_html):
    """Build the mastery FRQ prompt HTML with the gated-reading engine: an inlined HELD-OUT Source block
    (structured, title + paragraphs) + a COLD skill instruction (not the in-lesson topic). Matches the
    in-article write formatting (bold terms, per-line instructions) via _render_task."""
    parts = []
    if src_html:
        blocks = _html_blocks(src_html) or [_plain(src_html)]
        body = ""
        for k, b in enumerate(blocks):
            if k == 0 and len(blocks) > 1:
                body += f'<div style="font-weight:700;margin:0 0 4px;">{esc(b)}</div>'
            else:
                body += _render_source_block(b)
        parts.append('<div class="tb-source" style="border-left:4px solid #0d9488;background:#f8fafc;'
                     'border-radius:8px;padding:10px 14px;margin:0 0 12px;">'
                     '<div style="font-size:12px;font-weight:700;letter-spacing:.04em;color:#0f766e;'
                     'text-transform:uppercase;margin-bottom:4px;">New source</div>'
                     f'<div style="color:#1f2a44;line-height:1.6;">{body}</div></div>')
    # prefer the lesson's AUTHORED task-specific mastery prompt (inline or from mastery_prompts_g9); else the
    # generic cold instruction.
    authored = _mastery_for(L).get("prompt_html")
    if authored:
        parts.append(_render_body(authored))
    else:
        parts.append(_render_task(_mastery_instruction(L, slot)))
    return _xml_safe_entities("".join(parts))

ITEMS_URL = f"{QTI_BASE}/assessment-items"
TESTS_URL = f"{QTI_BASE}/assessment-tests"
CHECKPOINT = os.path.join(ROOT, "G9_MASTERY_V3_1_CHECKPOINT.json")
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


def _grader_score_url(base):
    # Single source of truth for the endpoint path: the live grader serves POST {BASE}/score (root, no
    # prefix), verified 2026-07-16 against api/external_score.py. Delegate to g9_wire_grader so the mastery
    # push and the in-lesson wiring can never disagree on the path (they did: this helper defaulted to the
    # older /timeback/score).
    from g9_wire_grader import normalize_grader_url
    return normalize_grader_url(base)


# HELD-OUT mastery source per lesson: a mode-appropriate stimulus the lesson's ARTICLE does NOT use, so the
# PP100 mastery is a FRESH cold task, not a re-submit of the in-lesson INDEPENDENT write (the readiness-audit
# blocker). Argument/claim lessons get a short argument FRAME; explain lessons an explain FRAME; evidence/essay
# lessons a fuller -LESSON- source (they need real text to quote/analyze). All verified to exist + be readable.
HELDOUT = {
    "ACC-W910-L-G9-C901-0001": "ACC-W910-FRAME-SOCIALMEDIAAGE",   # claim (arg): held-out arg frame
    "ACC-W910-L-G9-C901-0003": "ACC-W910-FRAME-SOCIALMEDIAAGE",   # sharpen claim (arg)
    "ACC-W910-L-G9-C905-0004": "ACC-W910-INFO-LESSON-RECYCLING",  # controlling idea (explain); L05 merged in
    "ACC-W910-L-G9-C901-0006": "ACC-W910-FRAME-SCHOOLYEAR",       # argue-or-explain interleave -> cold arg+explain-verb source
    "ACC-W910-L-G9-C902-0007": "ACC-W910-ARG-LESSON-AIWORKFORCE", # quote/paraphrase/summarize (needs real source)
    "ACC-W910-L-G9-C902-0008": "ACC-W910-ARG-LESSON-GRIDSPENDING",# select relevant evidence (needs real source)
    "ACC-W910-L-G9-C902-0009": "ACC-W910-ARG-LESSON-AIWORKFORCE", # integrate a quote (needs real source)
    "ACC-W910-L-G9-C903-0010": "ACC-W910-ARG-LESSON-GRIDSPENDING",# because/but/so hinge
    "ACC-W910-L-G9-C903-0011": "ACC-W910-ARG-LESSON-AIWORKFORCE", # warrant
    "ACC-W910-L-G9-C903-0012": "ACC-W910-INFO-LESSON-RECYCLING",  # PEW paragraph
    "ACC-W910-L-G9-C903-0013": "ACC-W910-INFO-LESSON-ENERGYMIX",  # calibrate reasoning
    "ACC-W910-L-G9-C906-0014": "ACC-W910-INFO-LESSON-HIGHWAYS",   # transitions (paragraph)
    "ACC-W910-L-G9-C906-0015": "ACC-W910-INFO-LESSON-RECYCLING",  # referential cohesion
    "ACC-W910-L-G9-C906-0016": "ACC-W910-ARG-LESSON-GRIDSPENDING",# revise cohesion (paragraph)
    "ACC-W910-L-G9-C906-0017": "ACC-W910-ARG-LESSON-AIWORKFORCE", # build paragraph
    "ACC-W910-L-G9-C906-0018": "ACC-W910-ARG-LESSON-GRIDSPENDING",# fresh paragraph + self-check
    # C904-0019 (standalone MPO) RETIRED 2026-07-18 (F3): teaching folded into C904-0023/0024; mastery dropped.
    "ACC-W910-L-G9-C904-0020": "ACC-W910-INFO-LESSON-RECYCLING",  # multi-para order
    "ACC-W910-L-G9-C904-0021": "ACC-W910-INFO-LESSON-ENERGYMIX",  # intro/conclusion
    "ACC-W910-L-G9-C901-0022": "ACC-W910-FRAME-SCHOOLYEAR",       # essay-mode interleave
    "ACC-W910-L-G9-C904-0023": "ACC-W910-ARG-LESSON-AIWORKFORCE", # full argument essay
    "ACC-W910-L-G9-C904-0024": "ACC-W910-INFO-LESSON-HIGHWAYS",   # full informational essay
    "ACC-W910-L-G9-C904-0025": "ACC-W910-ARG-LESSON-GRIDSPENDING",# essay revision (provided draft)
    "ACC-W910-L-G9-C904-0026": "ACC-W910-INFO-LESSON-ENERGYMIX",  # GATE (cold single-source essay)
}


def mastery_targets():
    """For each v3.1 lesson: (lesson_id, mastery_slot, held_out_source_html). The mastery slot is the lesson's
    INDEPENDENT production (the cold-write task = the composition outcome), but the SOURCE is a HELD-OUT stimulus
    the article never used, so the student cannot re-submit an in-lesson answer (readiness fix). We keep the
    slot's rubric_ref/unit (the graded shape) and swap only the source + the topic-specific wording."""
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "Lesson_Bank_G9", "lesson_g9_l*_v3_1.py"))):
        if "_deprecated" in f:
            continue
        m = _load(f)
        L = getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0]
        if not L:
            continue
        indep = None
        for s in L.slots:
            if s.kind == "production_frq" and s.role == "INDEPENDENT":
                indep = s
        if indep is None:
            prods = [s for s in L.slots if s.kind == "production_frq" and getattr(s, "scored", False)]
            indep = prods[-1] if prods else None
        if indep is None:
            print(f"  WARNING: {L.id} has no production FRQ -> no mastery test")
            continue
        # prefer the AUTHORED mastery source (inline or mastery_prompts_g9); else the HELDOUT-map source.
        held = _mastery_for(L).get("source") or HELDOUT.get(L.id)
        rec = STIM.get(held) if held else None
        if held and not rec:
            print(f"  WARNING: {L.id} held-out source {held} not found -> mastery has no source")
        src_html = _stim_html(rec) if rec else None
        out.append((L.id, indep, src_html, L))
    return out


def build_plan(grader_url):
    """(kind, id, url, body) plan: per lesson a grader-wired FRQ item + a single-item mastery test."""
    plan = []
    for lid, slot, src_html, L in mastery_targets():
        frq_id = f"{lid}-MASTERY-FRQ"
        test_id = f"{lid}-MASTERY"
        item = wire_payload(frq_id, slot, grader_url, source_html=src_html)
        # override wire_payload's stylize-built prompt with the gated-reading-rendered prompt: a HELD-OUT source
        # (not used in the article) + a COLD skill instruction, so mastery is a fresh independent task, not a
        # re-submit of the in-lesson write. Formatted the SAME as the in-article writes.
        item["interaction"]["questionStructure"]["prompt"] = _mastery_prompt(L, slot, src_html)
        plan.append(("item", frq_id, ITEMS_URL, item))
        # single-item assessment-test; reuse test_payload shape but with our own id/title (L is not needed - build inline)
        test = {"identifier": test_id, "title": f"{(slot.title or lid)[:110]} - Mastery",
                "qti-test-part": [{"identifier": "test_part", "navigationMode": "linear",
                                   "submissionMode": "individual", "sequence": 1,
                                   "qti-assessment-section": [{
                                       "identifier": "mastery_section", "title": "Mastery", "visible": True,
                                       "sequence": 1,
                                       "qti-assessment-item-ref": [
                                           {"identifier": frq_id, "href": f"{frq_id}.xml", "sequence": 1}]}]}],
                "outcomeDeclarations": [{"identifier": "SCORE", "cardinality": "single", "baseType": "float"}]}
        plan.append(("test", test_id, TESTS_URL, test))
    return plan


def post(session, url, body, is_test):
    """POST (create) with retry + 409-as-success. Tests + items use POST to the collection."""
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


def main(grader_base, live=False):
    grader_url = _grader_score_url(grader_base)
    plan = build_plan(grader_url)
    n_tests = sum(1 for k, *_ in plan if k == "test")
    print(f"G9 v3.1 MASTERY push: {n_tests} lessons -> {n_tests} FRQ items + {n_tests} single-item tests "
          f"({len(plan)} objects). grader = {grader_url}")
    for kind, oid, _url, _body in plan:
        if kind == "test":
            print(f"  test {oid}")
    if not live:
        print("DRY mode. Re-run with --live to push. No network call made.")
        return 0
    load_env()
    import requests
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {get_token()}", "Content-Type": "application/json"})
    done = json.load(open(CHECKPOINT)) if os.path.exists(CHECKPOINT) else {"ok": [], "fail": []}
    okset = set(done["ok"]); done["fail"] = []
    # push all ITEMS first, then tests (a test that refs a not-yet-created item 400s)
    for kind in ("item", "test"):
        for k, oid, url, body in plan:
            if k != kind or oid in okset:
                continue
            ok, status, detail = post(session, url, body, k == "test")
            if ok:
                okset.add(oid); done["ok"].append(oid)
            else:
                done["fail"].append({"id": oid, "kind": k, "status": status, "detail": detail})
                print(f"  FAIL [{status}] {k} {oid}: {detail}")
            json.dump({"ok": sorted(okset), "fail": done["fail"]}, open(CHECKPOINT, "w"), indent=1)
    print(f"\nG9 v3.1 mastery: {len(okset)} ok, {len(done['fail'])} failed.")
    return 0 if not done["fail"] else 1


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        raise SystemExit("Usage: python g9_push_mastery_v3_1.py <grader-base-url> [--live]")
    sys.exit(main(args[0], live="--live" in sys.argv))
