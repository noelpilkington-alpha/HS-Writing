"""Test-readiness pass. The student takes the G9 test bank items carrying only its journal.
For MCQ we log a deterministic answer-vs-key match (allowed - not a writing score). For
extended-text (CR) we log attemptability + the student's self-reported missing skill only."""
import os, sys, glob, importlib.util, json

HERE = os.path.dirname(__file__)
PIPE = os.path.join(HERE, "..")
ROOT = os.path.join(PIPE, "..")
sys.path.insert(0, PIPE)

_SKIP_PREFIXES = ("pp100_",)  # mastery instruments: out of scope for lived test-readiness


def _load_module(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def load_g9_test_items() -> list:
    items = []
    for f in sorted(glob.glob(os.path.join(ROOT, "Item_Bank_G9", "*.py"))):
        if os.path.basename(f).startswith(_SKIP_PREFIXES):
            continue
        try:
            m = _load_module(f)
        except Exception:
            continue
        for it in getattr(m, "ITEMS", []):
            items.append({
                "id": it.id,
                "kind": it.qti_type,
                "stem": it.stem,
                "mode": it.subskill_or_mode,
                "options": [{"id": o.id, "text": o.text} for o in it.options],
                "answer_key": list(it.answer_key),  # harness-only, never shown
            })
    return items


def present_item(item: dict) -> str:
    lines = [item["stem"]]
    if item["options"]:
        for i, o in enumerate(item["options"]):
            lines.append(f"  ({chr(65 + i)}) {o['text']}")
    return "\n".join(lines)


_TEST_TOOL = {
    "name": "report_item_attempt",
    "description": "Report your attempt at one test question.",
    "input_schema": {"type": "object", "properties": {
        "answer_letter": {"type": "string", "description": "For multiple choice: the single letter you pick (A/B/C/D). Empty for written items."},
        "written_answer": {"type": "string", "description": "For written items: your attempt."},
        "can_attempt": {"type": "boolean", "description": "Can you attempt this at all with what the course taught you?"},
        "missing_skill": {"type": "string", "description": "If you cannot, name the skill you were never taught. Else empty."}},
        "required": ["can_attempt", "missing_skill"]}}


def _letter_to_option_id(item, letter):
    if not letter:
        return ""
    idx = ord(letter.strip().upper()[:1]) - ord("A")
    if 0 <= idx < len(item["options"]):
        return item["options"][idx]["id"]
    return ""


def take_test(client, persona: dict, items: list, digest: str) -> dict:
    attempts = []
    correct = 0
    total_mcq = 0
    for item in items:
        user = ("YOUR MEMORY FROM THE COURSE:\n" + digest +
                "\n\n===== TEST QUESTION =====\n" + present_item(item) +
                "\n\nAttempt this question in character. If it is multiple choice, pick one letter. "
                "If you cannot do it with what the course taught you, set can_attempt false and name "
                "the missing skill.")
        out = _ask_tool(client, persona["system_preamble"], user)
        rec = {"id": item["id"], "kind": item["kind"], "mode": item["mode"],
               "student_answer": out.get("answer_letter") or out.get("written_answer", ""),
               "can_attempt": bool(out.get("can_attempt", False)),
               "missing_skill": out.get("missing_skill", "")}
        if item["kind"] == "choice" and item["answer_key"]:
            total_mcq += 1
            picked = _letter_to_option_id(item, out.get("answer_letter", ""))
            rec["mcq_correct"] = picked in item["answer_key"]
            if rec["mcq_correct"]:
                correct += 1
        attempts.append(rec)
    return {"attempts": attempts, "mcq_scored": {"correct": correct, "total": total_mcq}}


def _ask_tool(client, system, user):
    """Use the client's underlying model with the item-attempt tool. Falls back to .ask
    if the client does not expose a raw tool path (keeps the protocol simple)."""
    fn = getattr(client, "ask_tool", None)
    if callable(fn):
        return fn(system, user, _TEST_TOOL)
    # default: reuse .ask (student turn) and read answer text; can_attempt inferred True
    out = client.ask(system, user)
    return {"written_answer": out.get("response", ""), "can_attempt": True, "missing_skill": ""}
