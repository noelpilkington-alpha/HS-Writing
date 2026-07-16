"""
g9_push_dryrun.py  -  QTI packaging + DRY-RUN push for the G9 thin-vertical-slice.

The existing push_targets.py + bank_loader are G10-only and expect a `LESSONS` module var; the decomposed
96-lesson build uses `LESSON` (singular) across G9-G12. Rather than retrofit the whole loader, this focused
script packages EXACTLY the G9 slice (26 lessons + their 14 bound stimuli) for a dry-run: it builds the QTI
wire shapes offline so the shapes, the stylized HTML, expected_xp, and the JSON-vs-XML routing are all
inspectable BEFORE any live push. NO network call is made (that needs creds + explicit go-ahead).

What it emits per object, following the `timeback` skill rules:
- STIMULUS -> POST /stimuli, one per distinct bound source, carrying the passage/prompt HTML (sanitized XHTML).
- LESSON SLOTS -> each slot becomes a QTI item:
    * teach_card / stimulus_display / annotated_before_after -> a `stimulus`-style HTML block (informational,
      not scored) carrying the STYLIZED inline-CSS XHTML from stylize.stylize_slot().
    * discrimination / predict_the_fix / self_score -> `choice` item (JSON POST safe), shuffle=True, with the
      stylized stem; these are formative/answer-revealed (not scored gates).
    * production_frq / diagnosis_frq -> `extended-text` item (JSON POST safe) routed to the external grader
      (ExternalApiScore + rubric_ref) for scored production.
- LESSON -> POST /assessment-tests: ordered item refs + expected_xp (est. completion minutes).
Every HTML fragment is run through stylize.verify_xhtml() so a malformed body fails the dry-run, not the push.

Run: python pipeline/g9_push_dryrun.py            -> prints a summary + writes ../G9_PUSH_DRYRUN.json
"""
from __future__ import annotations
import os, sys, glob, re, io, contextlib, importlib.util, json, html

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
import stylize
from xp_allocation import expected_xp

QTI_BASE = "https://qti.alpha-1edtech.ai/api"
JSON_SAFE = {"choice", "extended-text", "order", "text-entry"}

# slot kind -> how it delivers on the platform
KIND_QTI = {
    "teach_card": "stimulus", "stimulus_display": "stimulus", "annotated_before_after": "stimulus",
    "discrimination": "choice", "predict_the_fix": "choice", "self_score": "choice",
    "production_frq": "extended-text", "diagnosis_frq": "extended-text", "sr_practice": "choice",
}
_OPT = re.compile(r"\(([A-D])\)\s")
_CORRECT = re.compile(r"Correct:\s*([A-D])", re.I)


def _load(path):
    spec = importlib.util.spec_from_file_location("g9_" + re.sub(r"\W", "", path), path)
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        try:
            spec.loader.exec_module(m)
        except SystemExit:
            pass
        except Exception:
            return None
    return m


def _stim_index():
    idx = {}
    for g in ("G9", "G10", "G11", "G12"):
        for f in glob.glob(os.path.join(ROOT, f"Stimulus_Bank_{g}", "*.py")):
            if "__" in os.path.basename(f):
                continue
            m = _load(f)
            if not m:
                continue
            for v in vars(m).values():
                if type(v).__name__ == "StimulusRecord":
                    idx[v.id] = v
    return idx


STIM = _stim_index()


def _stim_html(rec) -> str:
    """Stylized XHTML for a bound source (passages + prompt + perspectives), Timeback-safe."""
    parts = []
    for p in getattr(rec, "passages", []) or []:
        t = getattr(p, "title", "")
        if t:
            parts.append(f'<h3 style="font-size:16px;margin:10px 0 4px">{html.escape(t)}</h3>')
        parts.append(f'<p style="font-size:16px;line-height:1.55;white-space:pre-wrap">'
                     f'{html.escape(getattr(p, "text", ""))}</p>')
    for i, pr in enumerate(getattr(rec, "perspectives", []) or [], 1):
        parts.append(f'<p style="font-size:16px;line-height:1.55"><b>Perspective {i}:</b> {html.escape(pr)}</p>')
    if getattr(rec, "prompt", "") and not parts:
        parts.append(f'<p style="font-size:16px;line-height:1.55;white-space:pre-wrap">'
                     f'{html.escape(rec.prompt)}</p>')
    return "".join(parts)


def _choice_options(slot):
    """Extract (identifier, text, correct) options + shuffle for a discrimination/predict/self_score item.
    These are formative + answer-revealed, so the 'correct' flag is informational (they are not scored gates),
    but we still emit it + shuffle=True so the QTI item is well-formed and position is not gameable."""
    body = re.sub(r"<[^>]+>", " ", slot.body or "")
    rev = re.search(r"\b(Correct:|Reveal:)", body, re.I)
    core = body[:rev.start()] if (rev and _OPT.search(body[:rev.start()])) else body
    fm = _OPT.search(core)
    if not fm:
        return None, None
    opts_region = core[fm.start():]
    pieces = re.split(r"(?=\([A-D]\)\s)", opts_region)
    opts = []
    cm = _CORRECT.search(slot.body or "") or _CORRECT.search(slot.feedback or "")
    correct = cm.group(1) if cm else None
    for pc in pieces:
        pc = pc.strip()
        m = re.match(r"\(([A-D])\)\s*(.+)", pc, re.S)
        if m:
            opts.append({"identifier": m.group(1), "content": m.group(2).strip(),
                         "correct": (m.group(1) == correct)})
    return opts, correct


def build_g9_plan():
    lessons = []
    # VERIFIED LIVE SET ONLY: the broad 'lesson_g9_l[0-9]*.py' also matches the superseded v1/v2/v3 files,
    # which share lesson IDs with the v3.1 versions (24 of 29 ids collide) and pull in 2 deprecated lessons
    # dropped in the re-architecture. Loading all of them made the pushed content non-deterministic (whichever
    # colliding file sorted last won). Use the SAME v3.1 pattern the deterministic pipeline certifies
    # (_GRADE_GLOB['G9']). Fixed 2026-07-16 (found while prepping the graded pilot).
    for f in sorted(glob.glob(os.path.join(ROOT, "Lesson_Bank_G9", "lesson_g9_l*_v3_1.py"))):
        if "_deprecated" in f:
            continue
        m = _load(f)
        if not m:
            continue
        L = getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0]
        if L:
            lessons.append((os.path.basename(f), L))

    calls = []
    errors = []
    xhtml_checked = 0

    # 1) stimuli (distinct bound sources), stylized HTML
    bound = sorted({s.ref for _f, L in lessons for s in L.slots if getattr(s, "ref", "")})
    for sid in bound:
        rec = STIM.get(sid)
        if not rec:
            errors.append(f"stimulus {sid} not found")
            continue
        h = _stim_html(rec)
        ok, msg = stylize.verify_xhtml(h)
        xhtml_checked += 1
        if not ok:
            errors.append(f"stimulus {sid}: {msg}")
        calls.append({"step": "stimulus", "method": "POST", "url": f"{QTI_BASE}/stimuli", "wire": "JSON",
                      "id": sid, "html_len": len(h)})

    # 2) lesson slots -> items ; 3) lesson -> assessment-test
    item_counts = {"stimulus": 0, "choice": 0, "extended-text": 0}
    for fname, L in lessons:
        item_refs = []
        current_source = None   # the most recent stimulus_display source in this lesson (for grader grounding)
        for i, s in enumerate(L.slots):
            qti = KIND_QTI.get(s.kind, "stimulus")
            item_id = f"{L.id}-S{i+1:02d}-{s.kind}"
            item_refs.append(item_id)
            if s.kind == "stimulus_display" and getattr(s, "ref", ""):
                current_source = s.ref
            styled = stylize.stylize_slot(s)
            ok, msg = stylize.verify_xhtml(styled)
            xhtml_checked += 1
            if not ok:
                errors.append(f"{item_id}: {msg}")
            call = {"step": "item", "method": "POST", "url": f"{QTI_BASE}/assessment-items",
                    "id": item_id, "qti_type": qti, "wire": "JSON" if qti in JSON_SAFE else "XML-in-JSON",
                    "html_len": len(styled)}
            if qti == "choice":
                opts, correct = _choice_options(s)
                call["shuffle"] = True
                call["n_options"] = len(opts) if opts else 0
                call["correct"] = correct
                call["scored"] = False   # formative / answer-revealed
            if qti == "extended-text":
                # A production_frq with a rubric = a SCORED write routed to the external grader; the grader
                # grounds against the source last displayed in this lesson (slots carry ref="" and rely on the
                # lesson's shown source). A diagnosis_frq has NO rubric = an ungraded self-check; it delivers as
                # plain extended-text with no ExternalApiScore (do not route unscorable items to the grader).
                rubric = getattr(s, "rubric_ref", "") or None
                if s.kind == "production_frq" and rubric:
                    call["scored"] = True
                    call["externalScore"] = {"operator": "ExternalApiScore", "rubric": rubric,
                                             "stimulusRef": getattr(s, "ref", "") or current_source}
                else:
                    call["scored"] = False   # diagnosis_frq self-check (ungraded)
                    call["note"] = "ungraded self-check (no rubric): plain extended-text, no grader route"
                if s.kind == "production_frq" and rubric and not (getattr(s, "ref", "") or current_source):
                    errors.append(f"{item_id}: scored production has no source to ground the grader against")
            item_counts[qti] = item_counts.get(qti, 0) + 1
            calls.append(call)
        # the lesson as an assessment-test with expected_xp
        calls.append({"step": "lesson", "method": "POST", "url": f"{QTI_BASE}/assessment-tests",
                      "id": L.id, "title": L.title, "expected_xp": expected_xp(L),
                      "item_count": len(item_refs), "wire": "JSON"})

    return {"lessons": len(lessons), "stimuli": len(bound), "item_counts": item_counts,
            "total_calls": len(calls), "xhtml_checked": xhtml_checked,
            "errors": errors, "total_expected_xp": sum(expected_xp(L) for _f, L in lessons),
            "calls": calls}


def main():
    plan = build_g9_plan()
    out = os.path.join(ROOT, "G9_PUSH_DRYRUN.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(plan, fh, indent=2)
    print("=== G9 DRY-RUN (no network; wire shapes only) ===")
    print(f"lessons: {plan['lessons']}  |  distinct stimuli: {plan['stimuli']}")
    print(f"items by QTI type: {plan['item_counts']}")
    print(f"total API calls: {plan['total_calls']}  |  XHTML fragments verified: {plan['xhtml_checked']}")
    print(f"total expected_xp (G9): {plan['total_expected_xp']} (~{round(plan['total_expected_xp']/60,1)} hrs)")
    print(f"XHTML/packaging errors: {len(plan['errors'])}")
    for e in plan["errors"][:20]:
        print("   !! " + e)
    print(f"\nfull manifest -> {out}")
    return 0 if not plan["errors"] else 1


if __name__ == "__main__":
    sys.exit(main())
