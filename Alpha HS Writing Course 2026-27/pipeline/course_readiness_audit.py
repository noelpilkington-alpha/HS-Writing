"""
course_readiness_audit.py  -  Fable-5 STUDENT-READINESS audit of the full G9 v3.1 course.

Runs a STRICT auditor over each lesson's ACTUAL student experience (the gated-reading ARTICLE + its PP100
MASTERY task prompt), asking one question: is this ready to put in front of a real 9th grader working ALONE,
with no teacher? Returns a per-lesson verdict {ready|not_ready} + BLOCKERS (must-fix before students) and
WARNINGS (should-fix), via a forced structured tool call (reliable JSON). Aggregates into a course report.

Distinct from lesson_review.py's 3-dimension quality pass: this is a go/no-go readiness gate. It sees BOTH the
article experience AND the mastery prompt the student is graded on, and it looks for anything that would
confuse, mislead, or block a student: broken/missing content, a task a student cannot actually do from what was
taught, wrong/soft answer keys, mismatched examples, instructions that assume a teacher, factual/logical errors,
or a mastery task that does not match what the lesson taught.

Run:  python pipeline/course_readiness_audit.py            # audit all 25, write the report
      python pipeline/course_readiness_audit.py <lessonfile>   # audit one
Requires ANTHROPIC_API_KEY in HS Writing/.env. Never echoes the key.
"""
from __future__ import annotations
import os, sys, glob, re, json

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
from g9_push_dryrun import _load, STIM, _stim_html
from lesson_review import render_student_experience, _required_actions, _load_env_key
from mastery_targets_grade import mastery_targets as _grade_mastery_targets  # grade-aware (G9-G12)

GRADE = os.environ.get("READINESS_AUDIT_GRADE", "G9")

# cache the real rendered PP100 prompts (held-out source + task-specific prompt) keyed by lesson id, so the audit
# sees EXACTLY what the mastery pusher produces (not a re-derivation).
_MASTERY_CACHE = None
def _mastery_map():
    global _MASTERY_CACHE
    if _MASTERY_CACHE is None:
        _MASTERY_CACHE = {}
        for lid, slot, prompt_html, L in _grade_mastery_targets(GRADE):
            _MASTERY_CACHE[lid] = prompt_html
    return _MASTERY_CACHE

MODEL = "claude-fable-5"


def _mastery_experience_for(L):
    """The REAL mastery task prompt text (held-out source + cold instruction), exactly as the pusher builds it."""
    html = _mastery_map().get(L.id)
    if not html:
        return "(no mastery task found)"
    import html as _h
    # UNESCAPE entities so the auditor sees what the STUDENT sees (a rendered apostrophe), not the raw &#x27;
    # token (which the auditor wrongly flags as 'broken/unrendered content').
    return re.sub(r"\s+", " ", _h.unescape(re.sub(r"<[^>]+>", " ", html))).strip()


AUDIT_TOOL = {
    "name": "report_readiness",
    "description": "Report the student-readiness audit of one lesson.",
    "input_schema": {"type": "object", "properties": {
        "verdict": {"type": "string", "enum": ["ready", "not_ready"]},
        "blockers": {"type": "array", "items": {"type": "string"},
                     "description": "Must-fix-before-students issues: broken/missing content, a task the student cannot do from what was taught, a wrong/soft answer key, a mismatched example, teacher-dependent instructions, factual/logical errors, or a mastery task that does not match the lesson. Empty if none."},
        "warnings": {"type": "array", "items": {"type": "string"},
                     "description": "Should-fix issues that would not block a student but hurt quality. Empty if none."},
        "mastery_alignment": {"type": "string", "enum": ["aligned", "misaligned"],
                              "description": "Does the PP100 mastery task actually assess the skill this lesson taught?"},
        "summary": {"type": "string", "description": "One blunt sentence: is this ready for a solo 9th grader?"}},
        "required": ["verdict", "blockers", "warnings", "mastery_alignment", "summary"]}}


def audit_lesson(path):
    import anthropic
    m = _load(path)
    L = getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0]
    experience = render_student_experience(L)
    mastery = _mastery_experience_for(L)
    # Tier A3: inject the lesson's DECLARED design intent so the auditor judges against it and does not
    # re-litigate deliberate design (scaffold-free gates, one-write essays, dense minimal pairs, provided-
    # weak-draft diagnosis). This is the documented fix for the ~2:1 over-flag rate.
    try:
        from expected_exceptions import scope_note_for
        scope_note = scope_note_for(L)
    except Exception:
        scope_note = ""
    key = _load_env_key()
    if not key:
        return {"lesson_id": getattr(L, "id", "?"), "error": "no ANTHROPIC_API_KEY"}
    client = anthropic.Anthropic(api_key=key)
    prompt = f"""You are a STRICT curriculum readiness auditor. Your one job: decide if this lesson is 100% ready to put in front of a real 9th grader working ALONE, with NO teacher to clarify anything. Assume the student only knows what earlier lessons and THIS lesson teach. Be demanding: if anything would confuse, mislead, or block a solo student, it is not ready.

Audit BOTH parts:
1. THE LESSON (the gated-reading article the student works through: teaching, checkpoints, writing tasks).
2. THE PP100 MASTERY TASK (the graded write-the-response task the student must pass at the end).

Flag as a BLOCKER (must fix before students) anything like: content that is broken/cut off/missing; a task the student cannot actually do from what was taught; a multiple-choice answer key that is wrong, or where a distractor is also defensibly correct, or the "correct" answer is soft; an example that contradicts the instruction; instructions that assume a teacher or a feature that does not exist; a factual or logical error; or a mastery task that does not actually assess what the lesson taught. Flag softer issues as WARNINGS.

LESSON TITLE: {L.title}
WHAT THE STUDENT MUST DO: {_required_actions(L)}

{scope_note}
(The design-intent line above states DELIBERATE choices verified by a pedagogy council. Do NOT report these as
blockers; judge everything else strictly. A real defect worded around the intent still counts, e.g. a gate whose
held-out source is the wrong genre, or a mastery task that assesses a move the lesson never taught.)

=========== THE LESSON EXPERIENCE (step by step) ===========
{experience}

=========== THE PP100 MASTERY TASK (graded) ===========
{mastery}
============================================================

Call report_readiness. Be specific in every blocker/warning (name the step). Do not invent problems, but do not pass something a real student would trip on."""
    r = client.messages.create(model=MODEL, max_tokens=2000, tools=[AUDIT_TOOL],
                               tool_choice={"type": "tool", "name": "report_readiness"},
                               messages=[{"role": "user", "content": prompt}])
    for b in r.content:
        if getattr(b, "type", "") == "tool_use" and getattr(b, "name", "") == "report_readiness":
            out = dict(b.input); out["lesson_id"] = L.id; out["title"] = L.title
            # Tier A2: post-filter blockers through the written expected-exception registry. A blocker that
            # matches a deliberate, adjudicated design decision is moved to `expected_suppressed` (with the
            # rationale key) instead of counting - so the auditor stops re-litigating decided design. A
            # genuine defect worded around the exception still passes through as a real blocker.
            try:
                from expected_exceptions import is_expected
                real, suppressed = [], []
                for blk in out.get("blockers", []):
                    exp, key = is_expected(blk, L)
                    (suppressed if exp else real).append({"blocker": blk, "exception": key} if exp else blk)
                if suppressed:
                    out["blockers"] = real
                    out["expected_suppressed"] = suppressed
                    # if all blockers were expected-suppressed, the lesson is ready modulo warnings
                    if not real and out.get("verdict") == "not_ready":
                        out["verdict"] = "ready"
                        out["verdict_note"] = "all blockers matched written design exceptions (A2 suppression)"
            except Exception:
                pass
            return out
    return {"lesson_id": L.id, "title": L.title, "error": "no tool call"}


def main():
    if len(sys.argv) > 1 and sys.argv[1].endswith(".py"):
        print(json.dumps(audit_lesson(sys.argv[1]), indent=2, ensure_ascii=False))
        return 0
    from mastery_targets_grade import _GRADE_GLOB
    subdir, pat = _GRADE_GLOB[GRADE]
    files = sorted(glob.glob(os.path.join(ROOT, subdir, pat)))
    files = [f for f in files if "_deprecated" not in f]
    results = []
    outpath = os.path.join(ROOT, f"COURSE_READINESS_AUDIT_{GRADE}.json")
    for f in files:
        res = audit_lesson(f)
        results.append(res)
        v = res.get("verdict", "ERR"); nb = len(res.get("blockers", [])); nw = len(res.get("warnings", []))
        print(f"  {res.get('lesson_id','?'):26} {v:9} blockers={nb} warnings={nw} mastery={res.get('mastery_alignment','?')}", flush=True)
        # persist incrementally with UTF-8 so a crash (or a non-cp1252 char like the auditor's) never loses the run
        with open(outpath, "w", encoding="utf-8") as fh:
            json.dump(results, fh, indent=1, ensure_ascii=False)
    ready = sum(1 for r in results if r.get("verdict") == "ready")
    tot_block = sum(len(r.get("blockers", [])) for r in results)
    misaligned = [r["lesson_id"] for r in results if r.get("mastery_alignment") == "misaligned"]
    print(f"\n=== COURSE READINESS: {ready}/{len(results)} ready | {tot_block} total blockers | "
          f"{len(misaligned)} mastery-misaligned ===")
    if misaligned:
        print("  mastery-misaligned:", misaligned)
    return 0


if __name__ == "__main__":
    sys.exit(main())
