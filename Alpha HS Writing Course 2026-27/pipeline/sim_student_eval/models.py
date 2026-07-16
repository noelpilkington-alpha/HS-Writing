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
            for line in open(base, encoding="utf-8"):
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


class FableClient:
    def __init__(self, api_key: str, model: str = "claude-fable-5"):
        import anthropic
        self._c = anthropic.Anthropic(api_key=api_key)
        self._model = model

    @property
    def name(self) -> str:
        return "fable"

    def ask(self, system: str, user: str) -> dict:
        r = self._c.messages.create(
            model=self._model, max_tokens=3000, system=system,
            tools=[STUDENT_TOOL], tool_choice={"type": "tool", "name": "report_student_turn"},
            messages=[{"role": "user", "content": user}])
        for b in r.content:
            if getattr(b, "type", "") == "tool_use" and getattr(b, "name", "") == "report_student_turn":
                return dict(b.input)
        return {"response": "", "journal_update": {}, "error": "no tool call"}


class GptClient:
    def __init__(self, api_key: str, model: str = "gpt-5.5"):
        import openai
        self._c = openai.OpenAI(api_key=api_key)
        self._model = model

    @property
    def name(self) -> str:
        return "gpt"

    def ask(self, system: str, user: str) -> dict:
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
            return dict(_json.loads(msg.tool_calls[0].function.arguments))
        return {"response": msg.content or "", "journal_update": {}, "error": "no tool call"}
