# pipeline/sim_student_eval/student_agent.py
"""Walk ONE lesson as ONE student, in TWO phases:
  1. NARRATE - the student sees persona + running-memory digest + the dev-free lesson view, does
     every check/write, and reacts in free text. Plain text, no tool -> reliably full (the live
     pilot showed a single narrate+self-structure call stochastically empties the structured half).
  2. EXTRACT - a dedicated flat-tool call reads that narration + digest and records the structured
     learning state (skills / struggles / open questions / confidence / felt_repeated). A flat tool
     does not have the nested-object thinness failure mode.
Composition-probe lessons add the 'use only what you've learned; name what you're missing' ask.
Falls back to a single client.ask() when a client has no narrate/ask_tool (keeps mocks + tests simple)."""
from sim_student_eval.render_course import short_id, student_view
try:
    from sim_student_eval.models import EXTRACT_TOOL
except Exception:  # pragma: no cover - models import is always available in the real harness
    EXTRACT_TOOL = None

COMPOSITION_LESSONS = {"g9_l18", "g9_l23", "g9_l24", "g9_l26", "g9_l27"}


def _is_composition(sid: str) -> bool:
    return any(sid.startswith(p) for p in COMPOSITION_LESSONS)


def build_narrate_prompt(sid: str, view: str, digest: str, is_composition: bool) -> str:
    extra = ""
    if is_composition:
        extra = (
            "\n\nTHIS LESSON ASKS YOU TO WRITE A FULL PIECE. Use ONLY the skills you have "
            "actually learned in earlier lessons (see YOUR MEMORY above). Attempt it fully. "
            "If you find you are missing a skill you were never taught, write your best attempt "
            "anyway and then say clearly which skill you are missing and that you do not remember "
            "a lesson that taught it.")
    return (
        "YOUR MEMORY FROM EARLIER LESSONS:\n" + digest +
        "\n\n===== TODAY'S LESSON (read it and do every step) =====\n" + view + extra +
        "\n\n=====\nNow, in character as a 9th grader working alone, actually answer every check "
        "and attempt every writing task. Think out loud: what clicked, what confused you, what felt "
        "like a repeat of an earlier lesson (name which one), and how sure you feel about each skill. "
        "Write it all as your honest first-person reaction.")


# kept for back-compat with any caller/test that used the old single-call name
build_user_prompt = build_narrate_prompt


def _extract_prompt(sid: str, digest: str, narration: str) -> str:
    return (
        "Below is a 9th-grade student's own narration of the writing lesson they just finished, plus "
        "the running memory of what they knew before it. Record their learning state in structured "
        "form, extracting ONLY what the narration actually supports (do not invent skills or struggles).\n\n"
        "For felt_repeated: set echoes_lesson to an earlier lesson's name (like 'g9_l03...') ONLY if the "
        "student said this lesson repeated an earlier one; otherwise leave it empty. For confidence: a "
        "0.0-1.0 number per skill the student showed a confidence signal about.\n\n"
        "PRIOR MEMORY (earlier-lesson names appear here):\n" + digest +
        "\n\n===== THE STUDENT'S NARRATION OF LESSON " + sid + " =====\n" + narration)


def walk_lesson(client, persona: dict, L, digest: str) -> dict:
    sid = short_id(L)
    view = student_view(L)
    system = persona["system_preamble"]
    narrate_user = build_narrate_prompt(sid, view, digest, _is_composition(sid))

    # Two-phase path (real clients): narrate in free text, then extract the structured journal from it.
    if EXTRACT_TOOL is not None and hasattr(client, "narrate") and hasattr(client, "ask_tool"):
        response = client.narrate(system, narrate_user)
        upd = {}
        err = ""
        if response:
            try:
                raw = client.ask_tool(system, _extract_prompt(sid, digest, response), EXTRACT_TOOL)
                upd = dict(raw) if isinstance(raw, dict) else {}
            except Exception as e:  # extraction must never lose the (already captured) narration
                err = f"extract failed: {e!r}"
        else:
            err = "empty narration"
    else:
        # Fallback single-call path (mocks / any client without narrate+ask_tool).
        out = client.ask(system, narrate_user)
        response = out.get("response", "")
        ju = out.get("journal_update")
        upd = dict(ju) if isinstance(ju, dict) else {}
        err = out.get("error", "")
        if ju is not None and not isinstance(ju, dict):
            err = (err + "; " if err else "") + f"journal_update was {type(ju).__name__}, not dict"

    upd["lesson"] = sid
    # seq is assigned by the orchestrator (it knows position); default 0 here, overwritten in run_eval
    upd.setdefault("seq", 0)
    return {"lesson": sid, "response": response, "journal_update": upd, "raw_error": err}
