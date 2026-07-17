"""
lesson_review.py  -  standing REVIEWER PASSES for a lesson, run AFTER the deterministic lesson_contract gates.

Two judgment passes the hard gates cannot do (Noel 2026-07-14):
  1. Fable-5 reviewer  -> operational-necessity + engagement + clarity, from the async-student POV.
  2. Council (separate: council-of-writing-instruction skill, review mode) -> grounded-pedagogy critique.

This module owns pass 1 (+ the shared student-experience renderer both use). It renders a lesson to the ORDERED
STUDENT-FACING experience (what a student actually reads/does, step by step: teach prose with callouts flattened
to text, diagrams as their labels, MCQ prompts+options, writing prompts with the source treatment), NOT the
Python source, then asks Fable-5 to judge it against the three quality gates and return STRUCTURED findings.

The reviewer is ADVISORY (returns findings + a verdict), not a hard gate: judgment calls go to a human. Run:
  python pipeline/lesson_review.py Lesson_Bank_G9/lesson_g9_l01_arguable_claim_v3.py
Requires ANTHROPIC_API_KEY in ../.env (HS Writing/.env). Never echoes the key.
"""
from __future__ import annotations
import os, sys, re, json

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
from g9_push_dryrun import _load, _stim_html, STIM
# reuse the generator's exact flatteners so the reviewer sees what the player renders
from gated_reading import _plain, _html_blocks, _sentences_to_paras, _source_reminder
try:
    from l01_diagrams import DIAGRAMS as _DIAGRAMS
except Exception:
    _DIAGRAMS = {}

MODEL = "claude-fable-5"


def _load_env_key() -> str:
    """Read ANTHROPIC_API_KEY from HS Writing/.env without printing it."""
    for base in (os.path.join(ROOT, ".env"), os.path.join(ROOT, "..", ".env")):
        if os.path.exists(base):
            for line in open(base, encoding="utf-8"):
                line = line.strip()
                if line.startswith("ANTHROPIC_API_KEY") and "=" in line:
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return os.environ.get("ANTHROPIC_API_KEY", "")


def _clean(t: str) -> str:
    """Tidy the flattened text so the reviewer does not mistake tag-stripping artifacts for real defects:
    remove the space that tag-stripping leaves BEFORE punctuation ('REASON .' -> 'REASON.')."""
    return re.sub(r"[ \t]+([.,;:!?])", r"\1", t)


def _structured(body_html: str) -> str:
    """Flatten authored body to text but PRESERVE visual structure the student sees: list items become bullet
    lines, paragraphs/divs/breaks become line breaks. So the reviewer judges the real layout, not a run-on blob
    (else it false-flags well-formatted lists/steps as 'walls of text')."""
    h = body_html or ""
    h = re.sub(r"<li\b[^>]*>", "\n  - ", h, flags=re.I)
    # a <span> label (e.g. 'MOVE 1 - SIDE') is usually a heading for the block that follows -> break after it
    h = re.sub(r"</span>\s*(?=<div)", "</span>\n", h, flags=re.I)
    h = re.sub(r"</(p|div|li|h[1-6]|ol|ul|tr|span)>", "\n", h, flags=re.I)
    h = re.sub(r"<br\s*/?>", "\n", h, flags=re.I)
    # an opening block tag right after text (no close between) also implies a visual break
    h = re.sub(r"(?<=[.!?:\"'])\s*(?=<(div|p|ol|ul|table)\b)", "\n", h, flags=re.I)
    h = re.sub(r"<[^>]+>", "", h)
    h = re.sub(r"&#x27;", "'", h); h = re.sub(r"&amp;", "&", h)
    lines = [ln.rstrip() for ln in h.split("\n")]
    out, blank = [], False
    for ln in lines:
        if ln.strip():
            out.append(_clean(re.sub(r"[ \t]{2,}", " ", ln))); blank = False
        elif not blank:
            out.append(""); blank = True
    return "\n".join(out).strip()


def _stack_options(text: str) -> str:
    """Put each (A)/(B)/(C)/(D) choice on its own line - the player renders them as stacked radio options, so a
    run-on single line is a review-renderer artifact, not what the student sees."""
    return re.sub(r"\s*(\([A-D]\)\s)", r"\n  \1", text).strip()


def _options_from_choices(choices) -> tuple[str, str]:
    """Render structured choices[] as stacked (A)/(B) option lines + the correct-choice reveal.

    Production (gated_reading.build_lesson_html) renders the checkpoint's options from the slot's
    choices[] array, NOT from inline body prose. Some discrimination / predict_the_fix slots carry their
    options ONLY in choices[] with an empty body; parsing the body for those yields ZERO options, so the
    student-view renderer showed a prompt with no answers. That divergence made the sim-student / readiness
    audits (which walk this renderer) report 'blank / unanswerable multiple-choice steps' for exactly those
    slots, even though the pushed QTI item renders the options correctly. Falling back to choices[] here
    aligns the audited view with the student's real experience. Returns (stacked_option_lines, reveal_text)."""
    opts = choices or []
    opt_lines = "\n".join(
        f"  ({o.get('id') or chr(65 + j)}) {_plain(o.get('text', ''))}" for j, o in enumerate(opts)
    )
    correct = next((o for o in opts if o.get("correct")), None)
    reveal = _plain(correct.get("why", "")) if correct else ""
    return opt_lines, reveal


def render_student_experience(L) -> str:
    """The ordered student-facing walkthrough: each slot as the student encounters it. Teach/model bodies are
    flattened to plain text (callout/panel text preserved as prose), diagrams named by role, MCQ options listed,
    writing prompts shown with the once-per-topic source treatment the generator uses. NOTE: the correct-answer
    reveal on a check is shown as post-answer feedback (not with the options), matching what a student sees."""
    lines = []
    inlined = set()
    cur_source = ""
    for i, s in enumerate(L.slots, 1):
        kind = s.kind
        if kind in ("teach_card", "annotated_before_after"):
            body = _structured(s.body)
            # derive the visual note from THIS slot's ACTUAL content (never hardcode a lesson's labels; that
            # stamped L01's 'MOVE 1 = SIDE' onto every lesson and caused false 'panel contradicts content'
            # audit blockers). The panel/list text is already rendered into `body`; the note only names the
            # visual FORM that is present, using the slot's own move labels.
            raw = s.body or ""
            notes = []
            moves = re.findall(r"MOVE\s*\d+\s*[-:–]?\s*([A-Za-z][A-Za-z /]{1,24})", raw)
            if moves:
                notes.append("a labeled DECOMPOSE panel (" + ", ".join(f"MOVE {j+1}={m.strip().upper()}" for j, m in enumerate(moves[:3])) + ")")
            if re.search(r"\bBEFORE\b", raw) and re.search(r"\bAFTER\b", raw):
                notes.append("a BEFORE/AFTER worked example")
            if _DIAGRAMS.get((L.id, i)):
                notes.append("a labeled diagram")
            note = f" [shows {', '.join(notes)}]" if notes else ""
            lines.append(f"STEP {i} (TEACH: {s.title}){note}\n{body}")
        elif kind == "stimulus_display":
            rec = STIM.get(getattr(s, "ref", "")) if getattr(s, "ref", "") else None
            src = _structured(_stim_html(rec)) if rec else _structured(s.body)
            cur_source = _plain(_stim_html(rec)) if rec else _plain(s.body)
            lines.append(f"STEP {i} (SOURCE: {s.title})\n{src}")
        elif kind == "discrimination":
            # the student sees ONLY the prompt+options (the player renders each option as a STACKED radio choice);
            # "Correct: X ..." is post-answer feedback, NOT shown with the options. Split + stack so the reviewer
            # judges the real student view (else it flags a 'spoiled quiz' or 'run-on options').
            body = _plain(s.body)
            m = re.search(r"\b(Correct:|Reveal:)", body)
            options = _stack_options(body[:m.start()].strip() if m else body)
            reveal = body[m.start():].strip() if m else ""
            # options in the body prose? use them. If not (options live ONLY in choices[]), render choices[]
            # so the student view matches the pushed QTI item instead of showing a prompt with no answers.
            if not re.search(r"\([A-D]\)", options) and getattr(s, "choices", None):
                opt_lines, why = _options_from_choices(s.choices)
                if opt_lines:
                    options = opt_lines
                    if not reveal and why:
                        reveal = f"Correct: {why}"
            lines.append(f"STEP {i} (CHECK - multiple choice: {s.title})\n{options}"
                         + (f"\n[after the student answers, they see: {reveal}]" if reveal else ""))
        elif kind == "predict_the_fix":
            body = _plain(s.body)
            m = re.search(r"\b(Correct:|Reveal:)", body)
            options = _stack_options(body[:m.start()].strip() if m else body)
            # same choices[]-only fallback as discrimination (see _options_from_choices)
            if not re.search(r"\([A-D]\)", options) and getattr(s, "choices", None):
                opt_lines, _ = _options_from_choices(s.choices)
                if opt_lines:
                    options = opt_lines
            lines.append(f"STEP {i} (CHECK - diagnose then reveal: {s.title})\n{options}"
                         f"\n[after the student answers, they see: {_plain(s.feedback)}]")
        elif kind == "self_score":
            # a predict-the-score checkpoint: prompt (the draft + rubric) + the student's score OPTIONS, then a
            # post-answer reveal per choice. MUST be rendered, else the auditor sees a gap where this step is and
            # false-flags 'STEP N missing / content cut off' (this slot kind was previously dropped).
            prompt = _plain(s.body)
            opts = getattr(s, "choices", None) or []
            opt_lines = "\n".join(f"  ({chr(65+j)}) {_plain(o.get('text',''))}" for j, o in enumerate(opts))
            correct = next((o for o in opts if o.get("correct")), None)
            reveal = _plain(correct.get("why", "")) if correct else _plain(s.feedback)
            lines.append(f"STEP {i} (CHECK - score it yourself then reveal: {s.title})\n{prompt}\n{opt_lines}"
                         + (f"\n[after the student answers, they see: {reveal}]" if reveal else ""))
        elif kind in ("production_frq", "diagnosis_frq"):
            task = _plain(s.body)
            if cur_source and cur_source not in inlined:
                srcline = f"[SOURCE shown in full here]\n{cur_source}\n"
                inlined.add(cur_source)
            elif cur_source:
                srcline = f"[one-line reminder only: Same topic: {_source_reminder(cur_source)}]\n"
            else:
                srcline = ""
            lines.append(f"STEP {i} (WRITE - free text: {s.title})\n{srcline}{task}")
    return _clean("\n\n".join(lines))


REVIEW_SCHEMA_INSTRUCTION = """Call the report_review tool. For each of the three sections give a verdict
('pass' or 'revise') and an `items` list of the specific problems you found (empty if pass), plus a one-sentence
`note`:
- operational_necessity.items = exact phrases/terms that teach something NOT needed to complete this lesson's tasks (should be cut or moved to a tooltip).
- formatting.items = specific run-together text, missing breaks, or confusing layout.
- engagement.items = specific boredom/repetition/confusion risks for a real 9th grader working alone.
Then `overall` = one blunt sentence: would a real unaided 9th grader learn the skill and stay engaged?
Keep each item under 30 words and paraphrase lesson wording rather than quoting it."""


def fable_review(experience: str, lesson_title: str, required_actions: str) -> dict:
    import anthropic
    key = _load_env_key()
    if not key:
        return {"error": "no ANTHROPIC_API_KEY found in .env"}
    client = anthropic.Anthropic(api_key=key)
    prompt = f"""You are a demanding instructional-content reviewer judging a self-paced online writing lesson for a 9th grader who works ALONE (no teacher, no help). You care about three things ONLY:

1. OPERATIONAL NECESSITY: does the instructional text teach ONLY what the student must know to DO this lesson's tasks? Flag any sentence/term that is nice-to-know but not needed to complete the tasks (it should be cut or moved to an optional tooltip). Be strict.
2. FORMATTING: is everything cleanly readable - proper breaks between ideas, sources and prompts not run together, no wall-of-text, no confusing layout?
3. ENGAGEMENT: would a real, easily-bored 9th grader working alone stay engaged, or skim/quit? Flag repetition, padding, or anything that reads like busywork.

LESSON TITLE: {lesson_title}
WHAT THE STUDENT MUST ACTUALLY DO (the tasks): {required_actions}

=========== THE STUDENT EXPERIENCE, STEP BY STEP ===========
{experience}
============================================================

{REVIEW_SCHEMA_INSTRUCTION}"""
    # Force STRUCTURED OUTPUT via a tool schema: the model must call report_review with typed fields, so we
    # never parse free-text JSON (which intermittently broke on inner quotes). tool_choice forces the call.
    sect = {"type": "object", "properties": {
                "verdict": {"type": "string", "enum": ["pass", "revise"]},
                "items": {"type": "array", "items": {"type": "string"}},
                "note": {"type": "string"}},
            "required": ["verdict", "items", "note"]}
    tool = {"name": "report_review", "description": "Report the lesson review findings.",
            "input_schema": {"type": "object", "properties": {
                "operational_necessity": sect, "formatting": sect, "engagement": sect,
                "overall": {"type": "string"}},
                "required": ["operational_necessity", "formatting", "engagement", "overall"]}}
    r = client.messages.create(model=MODEL, max_tokens=2000, tools=[tool],
                               tool_choice={"type": "tool", "name": "report_review"},
                               messages=[{"role": "user", "content": prompt}])
    for b in r.content:
        if getattr(b, "type", "") == "tool_use" and getattr(b, "name", "") == "report_review":
            return b.input
    return {"error": "model did not call report_review", "raw": str(r.content)[:400]}


def _required_actions(L) -> str:
    """Describe what the student must DO, derived from THIS lesson's own slots (title as the skill label), not
    a hardcoded 'arguable claim' (that L01-boilerplate falsely flagged every other lesson as objectives-
    mismatched). The write's product is named by the slot title; the check/diagnose actions are generic."""
    acts = []
    for s in L.slots:
        if s.kind == "discrimination":
            acts.append(f"identify the target in a multiple-choice check ({(s.title or '').rstrip('?')})")
        elif s.kind == "predict_the_fix":
            acts.append("diagnose a weak draft and pick the fix")
        elif s.kind == "diagnosis_frq":
            acts.append("run the self-check on a draft, then revise")
        elif s.kind == "production_frq":
            unit = getattr(s, "unit", "") or "sentence"
            acts.append(f"write ({unit}): {(s.title or '').strip()}")
    return "; ".join(dict.fromkeys(acts)) or "complete the lesson tasks"


def review_lesson_file(path: str) -> dict:
    m = _load(path if os.path.isabs(path) else os.path.join(ROOT, path))
    L = getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0]
    exp = render_student_experience(L)
    findings = fable_review(exp, L.title, _required_actions(L))
    return {"lesson_id": L.id, "title": L.title, "findings": findings, "experience_chars": len(exp)}


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "Lesson_Bank_G9/lesson_g9_l01_arguable_claim_v3.py"
    out = review_lesson_file(path)
    print(json.dumps(out, indent=2, ensure_ascii=False))
