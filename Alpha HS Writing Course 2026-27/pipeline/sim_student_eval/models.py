# pipeline/sim_student_eval/models.py
"""Thin model clients used AS STUDENTS. Both Fable-5 (Anthropic) and GPT (OpenAI) implement
the same .ask(system, user) -> {response, journal_update} contract via forced structured output,
so journal updates are always machine-valid (never free-text JSON parsing)."""
import os

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..", "..")  # -> Alpha HS Writing Course 2026-27/


def _read_env_val(names):
    for base in (os.path.join(ROOT, ".env"), os.path.join(ROOT, "..", ".env")):
        if os.path.exists(base):
            with open(base, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    for n in names:
                        if line.startswith(n) and "=" in line:
                            return line.split("=", 1)[1].strip().strip('"').strip("'")
    for n in names:
        if os.environ.get(n):
            return os.environ[n]
    return ""


def load_keys() -> dict:
    return {"anthropic": _read_env_val(["ANTHROPIC_API_KEY"]),
            "openai": _read_env_val(["OPEN_AI_API_KEY", "OPENAI_API_KEY"])}


_JOURNAL_SCHEMA = {
    "type": "object",
    "properties": {
        "skills_i_can_now_do": {"type": "array", "items": {"type": "string"}},
        "terms_learned": {"type": "array", "items": {"type": "string"}},
        "where_i_struggled": {"type": "array", "items": {"type": "string"}},
        "felt_repeated": {
            "type": "object",
            "properties": {"echoes_lesson": {"type": "string"}, "what": {"type": "string"}},
        },
        "open_questions": {"type": "array", "items": {"type": "string"}},
        "confidence": {"type": "object", "additionalProperties": {"type": "number"}},
    },
    "required": ["skills_i_can_now_do", "where_i_struggled", "open_questions", "confidence"],
}

STUDENT_TOOL = {
    "name": "report_student_turn",
    "description": "Report what you did on this lesson and update your running memory.",
    "input_schema": {
        "type": "object",
        "properties": {
            "response": {"type": "string",
                         "description": "In character: your answers to the checks, your attempt at "
                                        "the writing tasks, and your honest reactions."},
            "journal_update": _JOURNAL_SCHEMA,
        },
        "required": ["response", "journal_update"],
    },
}

# EXTRACT_TOOL: the journal schema FLATTENED to top-level tool parameters (no nested object). The
# live pilot showed Fable stochastically empties a NESTED tool-object; a flat tool (each field a
# top-level parameter, exactly like the test-taker's reliable report_item_attempt) does not have that
# failure mode. Phase 2 of walk_lesson uses this to extract the structured journal FROM the student's
# already-written narration, so the structured signal no longer depends on the model self-structuring
# while it narrates.
EXTRACT_TOOL = {
    "name": "record_learning_state",
    "description": ("Read the student's narration of the lesson they just did and record their "
                    "learning state in structured form. Extract only what the narration supports; "
                    "do not invent skills or struggles the student did not express."),
    "input_schema": {
        "type": "object",
        "properties": dict(_JOURNAL_SCHEMA["properties"]),
        "required": ["skills_i_can_now_do", "where_i_struggled", "open_questions", "confidence"],
    },
}

# Fable-5 intermittently serializes a NESTED tool-object as a string of pseudo-XML
# <parameter name="KEY">JSON_VALUE</parameter> blocks instead of a real object. When that happens,
# journal_update arrives as a str and dict(...) on it throws. _coerce_dict recovers the object so a
# malformed nested field never crashes the walk or loses the turn. (The top-level `response` string
# is unaffected by this quirk; we only need to repair the nested journal_update.)
import json as _json
import re as _re

_PARAM_RE = _re.compile(r'<parameter\s+name="([^"]+)">(.*?)</parameter>', _re.DOTALL)


def _coerce_dict(val):
    """Return val as a dict. Already-dict -> unchanged. String -> try JSON, then the
    <parameter name=..> pseudo-XML form; each extracted value is JSON-parsed when possible.
    Anything unrecoverable -> {} (never raises)."""
    if isinstance(val, dict):
        return val
    if not isinstance(val, str):
        return {}
    s = val.strip()
    try:
        parsed = _json.loads(s)
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        pass
    out = {}
    for k, raw in _PARAM_RE.findall(s):
        raw = raw.strip()
        try:
            out[k] = _json.loads(raw)
        except Exception:
            out[k] = raw
    return out


def _normalize_turn(inp: dict) -> dict:
    """Normalize a report_student_turn tool input: guarantee response is a str and
    journal_update is a dict, repairing the Fable pseudo-XML string form when present."""
    resp = inp.get("response", "")
    if not isinstance(resp, str):
        resp = str(resp)
    return {"response": resp, "journal_update": _coerce_dict(inp.get("journal_update"))}


def _journal_is_thin(turn: dict) -> bool:
    """A turn is 'thin' when the model wrote a real response but left the STRUCTURED journal
    essentially empty (no skills AND no confidence). Fable does this stochastically - the same
    lesson returns rich on one call and empty on the next - so a retry usually recovers it. The
    structured fields feed the redundancy pre-pass + readiness signal, so thin turns are low-value."""
    ju = turn.get("journal_update") or {}
    return not ju.get("skills_i_can_now_do") and not ju.get("confidence")


def ask_with_retry(raw_ask, system: str, user: str, tries: int = 3) -> dict:
    """Call raw_ask (which returns an already-normalized turn dict) up to `tries` times, keeping
    the FIRST non-thin result. If every attempt is thin, return the richest one seen (most skills)
    so we never lose the response. Vary nothing but the attempt (the model is stochastic)."""
    best = None
    for _ in range(max(1, tries)):
        turn = raw_ask(system, user)
        if turn.get("error"):          # a real API/no-tool error: return immediately, orchestrator logs it
            return turn
        if not _journal_is_thin(turn):
            return turn
        if best is None or len((turn.get("journal_update") or {}).get("skills_i_can_now_do", [])) \
                > len((best.get("journal_update") or {}).get("skills_i_can_now_do", [])):
            best = turn
    return best if best is not None else {"response": "", "journal_update": {}, "error": "no result"}


class FableClient:
    def __init__(self, api_key: str, model: str = "claude-fable-5"):
        import anthropic
        self._c = anthropic.Anthropic(api_key=api_key)
        self._model = model

    @property
    def name(self) -> str:
        return "fable"

    def _ask_once(self, system: str, user: str) -> dict:
        r = self._c.messages.create(
            model=self._model, max_tokens=3000, system=system,
            tools=[STUDENT_TOOL], tool_choice={"type": "tool", "name": "report_student_turn"},
            messages=[{"role": "user", "content": user}])
        for b in r.content:
            if getattr(b, "type", "") == "tool_use" and getattr(b, "name", "") == "report_student_turn":
                return _normalize_turn(dict(b.input))
        return {"response": "", "journal_update": {}, "error": "no tool call"}

    def ask(self, system: str, user: str) -> dict:
        # retry stochastically-thin journals (Fable skips the nested object ~intermittently)
        return ask_with_retry(self._ask_once, system, user)

    def ask_tool(self, system: str, user: str, tool: dict) -> dict:
        r = self._c.messages.create(
            model=self._model, max_tokens=1500, system=system,
            tools=[tool], tool_choice={"type": "tool", "name": tool["name"]},
            messages=[{"role": "user", "content": user}])
        for b in r.content:
            if getattr(b, "type", "") == "tool_use":
                return dict(b.input)
        return {}

    def narrate(self, system: str, user: str) -> str:
        """Plain-text call (no tool): the student does the lesson and reacts in free text. No nested
        object to skip, so the response is reliably full - the structured journal is extracted from it
        in a second step (ask_tool + EXTRACT_TOOL)."""
        r = self._c.messages.create(
            model=self._model, max_tokens=3000, system=system,
            messages=[{"role": "user", "content": user}])
        parts = [getattr(b, "text", "") for b in r.content if getattr(b, "type", "") == "text"]
        return "\n".join(p for p in parts if p).strip()


class GptClient:
    def __init__(self, api_key: str, model: str = "gpt-5.5"):
        import openai
        self._c = openai.OpenAI(api_key=api_key)
        self._model = model

    @property
    def name(self) -> str:
        return "gpt"

    def _ask_once(self, system: str, user: str) -> dict:
        import json as _json
        tool = {"type": "function", "function": {
            "name": STUDENT_TOOL["name"], "description": STUDENT_TOOL["description"],
            "parameters": STUDENT_TOOL["input_schema"]}}
        r = self._c.chat.completions.create(
            model=self._model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            tools=[tool], tool_choice={"type": "function", "function": {"name": STUDENT_TOOL["name"]}},
            max_completion_tokens=3000)
        msg = r.choices[0].message
        if msg.tool_calls:
            return _normalize_turn(dict(_json.loads(msg.tool_calls[0].function.arguments)))
        return {"response": msg.content or "", "journal_update": {}, "error": "no tool call"}

    def ask(self, system: str, user: str) -> dict:
        return ask_with_retry(self._ask_once, system, user)

    def ask_tool(self, system: str, user: str, tool: dict) -> dict:
        import json as _json
        ot = {"type": "function", "function": {"name": tool["name"],
              "description": tool["description"], "parameters": tool["input_schema"]}}
        r = self._c.chat.completions.create(
            model=self._model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            tools=[ot], tool_choice={"type": "function", "function": {"name": tool["name"]}},
            max_completion_tokens=1500)
        msg = r.choices[0].message
        if msg.tool_calls:
            return dict(_json.loads(msg.tool_calls[0].function.arguments))
        return {}

    def narrate(self, system: str, user: str) -> str:
        r = self._c.chat.completions.create(
            model=self._model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            max_completion_tokens=3000)
        return (r.choices[0].message.content or "").strip()
