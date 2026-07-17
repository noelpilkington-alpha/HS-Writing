# pipeline/sim_student_eval/student_agent.py
"""Walk ONE lesson as ONE student. The student sees only: persona + running-memory digest +
the dev-free lesson view. It attempts every check/write in character and emits a journal update.
Composition-probe lessons add the 'use only what you've learned; name what you're missing' ask."""
from sim_student_eval.render_course import short_id, student_view

COMPOSITION_LESSONS = {"g9_l18", "g9_l23", "g9_l24", "g9_l26", "g9_l27"}


def _is_composition(sid: str) -> bool:
    return any(sid.startswith(p) for p in COMPOSITION_LESSONS)


def build_user_prompt(sid: str, view: str, digest: str, is_composition: bool) -> str:
    extra = ""
    if is_composition:
        extra = (
            "\n\nTHIS LESSON ASKS YOU TO WRITE A FULL PIECE. Use ONLY the skills you have "
            "actually learned in earlier lessons (see YOUR MEMORY above). Attempt it fully. "
            "If you find you are missing a skill you were never taught, write your best attempt "
            "anyway and then say clearly, in your response, which skill you are missing and that "
            "you do not remember a lesson that taught it.")
    return (
        "YOUR MEMORY FROM EARLIER LESSONS:\n" + digest +
        "\n\n===== TODAY'S LESSON (read it and do every step) =====\n" + view + extra +
        "\n\n=====\nNow: (1) actually answer the checks and attempt the writing tasks in your "
        "`response`, in character as a 9th grader. (2) In `journal_update`, honestly record what "
        "you can now do, terms you learned, where you struggled, whether anything felt like a "
        "repeat of an earlier lesson (set felt_repeated.echoes_lesson to that lesson's name like "
        "'g9_l03...' if so), any open questions, and your confidence per skill (0.0-1.0). "
        "Use the earlier-lesson NAMES exactly as they appear in YOUR MEMORY.")


def walk_lesson(client, persona: dict, L, digest: str) -> dict:
    sid = short_id(L)
    view = student_view(L)
    user = build_user_prompt(sid, view, digest, _is_composition(sid))
    out = client.ask(persona["system_preamble"], user)
    # journal_update should be a dict (clients normalize it), but stay defensive: a malformed
    # field must never crash the lesson or discard the student's response.
    ju = out.get("journal_update")
    upd = dict(ju) if isinstance(ju, dict) else {}
    upd["lesson"] = sid
    # seq is assigned by the orchestrator (it knows position); default 0 here, overwritten in run_eval
    upd.setdefault("seq", 0)
    err = out.get("error", "")
    if ju is not None and not isinstance(ju, dict):
        err = (err + "; " if err else "") + f"journal_update was {type(ju).__name__}, not dict"
    return {"lesson": sid, "response": out.get("response", ""),
            "journal_update": upd, "raw_error": err}
