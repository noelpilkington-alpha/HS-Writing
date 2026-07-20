"""
openai_diverse.py  -  thin OpenAI (GPT) cross-model diversity check.

WHAT THIS IS (and is NOT):
  * ADVISORY / DIVERSITY-CHECK ONLY. This module gives an independent OpenAI
    author-or-judge second opinion on an item/claim, to diversify against
    Claude/Fable/Incept. It NEVER blocks a build and nothing here raises to fail one.
  * OpenAI's IMAGE role is RETIRED in favor of Incept drawio (per the strategy doc):
    Incept drawio owns editable diagrams now. This module is the diversity-check role
    ONLY (author = an alternative version; judge = an assessment of an item/claim).

DRY-BY-DEFAULT / --live contract (mirrors incept_client.py):
  * second_opinion() takes `live: bool` (default False).
  * DRY mode (live=False): makes NO network call. Returns the request it WOULD send:
      {"status": "dry", "would_send": <chat body>, "request_id": None}.
  * LIVE mode (live=True): the ONLY transport is `curl` via subprocess, with the flags
      curl -s --ssl-no-revoke --max-time 40 -X POST
           https://api.openai.com/v1/chat/completions
           -H "Authorization: Bearer <key>" -H "Content-Type: application/json" -d <body>
    Responses are parsed as JSON. The key is never echoed in any error message.

SECRET HYGIENE (hard requirement, mirrors incept_client.py):
  The API key is read LAZILY from the env var OPEN_AI_API_KEY, else parsed from the
  `../../.env` file (a line `OPEN_AI_API_KEY=...`, quotes/whitespace stripped). It is
  wrapped in a redacting holder so it NEVER appears in __repr__, str(vars(self)), any
  log, or any error message. Importing this module with NO key present must NOT raise.

Stdlib only (subprocess + json + os). No `openai` SDK, no `requests` dependency.
"""
from __future__ import annotations
import os
import json
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
# module lives in Alpha HS Writing Course 2026-27/pipeline/ ; the .env is in HS Writing/
_ENV_FILE = os.path.normpath(os.path.join(HERE, "..", "..", ".env"))
_ENV_VAR = "OPEN_AI_API_KEY"


class _Secret:
    """Holds a secret value; its repr/str NEVER reveal the value.

    Because the value lives in a slot (not in a mapping), formatting the owning
    object's __dict__ (i.e. `str(vars(client))`) only ever calls this repr.
    """
    __slots__ = ("_v",)

    def __init__(self, value):
        self._v = value

    def reveal(self):
        return self._v

    def __repr__(self):
        return "<redacted>"

    __str__ = __repr__


def _resolve_key() -> str | None:
    """Return the OpenAI API key from env or the ../../.env file, or None if absent.

    NEVER logs or echoes the key. Import-safe: a missing env var and a missing/unreadable
    .env both simply return None (no exception).
    """
    env = os.environ.get(_ENV_VAR)
    if env and env.strip():
        return _strip_val(env)
    try:
        with open(_ENV_FILE, "r", encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except OSError:
        return None
    for line in lines:
        s = line.strip()
        if s.startswith(_ENV_VAR + "="):
            val = _strip_val(s.split("=", 1)[1])
            if val:
                return val
    return None


def _strip_val(raw: str) -> str:
    """Strip whitespace and a single pair of surrounding quotes from a value."""
    v = raw.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
        v = v[1:-1].strip()
    return v


class OpenAIDiverse:
    """Thin OpenAI second-opinion client. Dry-by-default; `live=True` spends quota.

    Advisory only: an author-or-judge diversity check, never a build gate.
    """

    BASE = "https://api.openai.com"
    ENDPOINT = "/v1/chat/completions"
    MODEL = "gpt-4o"

    def __init__(self, model: str | None = None):
        self.model = model or self.MODEL
        # Wrap the key in a redacting holder so it never surfaces in repr/vars/logs.
        # Read lazily from env/file; may be None until a live call needs it (import-safe).
        self._secret = _Secret(_resolve_key())

    def __repr__(self):
        # Deliberately excludes the key holder's value (holder repr is "<redacted>" anyway).
        return f"OpenAIDiverse(model={self.model!r})"

    # ------------------------------------------------------------------ secrets
    def _key(self) -> str:
        """Return the API key; raise (without echoing it) if it could not be found."""
        key = self._secret.reveal()
        if not key:
            raise RuntimeError(
                "OPEN_AI_API_KEY not found: set the env var or add a line "
                "'OPEN_AI_API_KEY=...' in the .env at the repo root."
            )
        return key

    def _redact(self, text: str) -> str:
        """Strip the key from any string before it can reach a log or error message."""
        key = self._secret.reveal()
        if key and text:
            return text.replace(key, "<redacted>")
        return text or ""

    # -------------------------------------------------------------- request body
    def _system_for(self, kind: str) -> str:
        """The system message that frames the second-opinion role."""
        if kind == "author":
            return (
                "You are an independent second author providing a cross-model "
                "diversity check. Given a piece of writing, produce a stronger "
                "alternative version. Advisory only."
            )
        if kind == "judge":
            return (
                "You are an independent second judge providing a cross-model "
                "diversity check. Assess the supplied item or claim on its merits. "
                "Advisory only."
            )
        raise ValueError("kind must be 'author' or 'judge'")

    def _build_body(self, kind: str, content, prompt: str) -> dict:
        """Build an OpenAI Chat Completions request body.

        `content` may be a dict (e.g. an item) or a string; it is serialized into the
        user message alongside the caller's prompt.
        """
        if isinstance(content, str):
            content_text = content
        else:
            content_text = json.dumps(content, ensure_ascii=False, indent=2)
        user = f"{prompt}\n\n{content_text}"
        return {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self._system_for(kind)},
                {"role": "user", "content": user},
            ],
        }

    # ------------------------------------------------------------------- public
    def second_opinion(self, kind: str, content, prompt: str, live: bool = False) -> dict:
        """An independent OpenAI author-or-judge second opinion (diversity check).

        `kind` is "author" (give an alternative version) or "judge" (assess the item/claim).
        DRY mode (default) returns {"status":"dry","would_send":<chat body>,"request_id":None}
        with NO network call. LIVE mode POSTs to the Chat Completions endpoint and returns
        the parsed JSON. Advisory only; never raises to fail a build in dry mode.
        """
        body = self._build_body(kind, content, prompt)
        if not live:
            return {"status": "dry", "would_send": body, "request_id": None}
        return self._post(body)

    # ---------------------------------------------------------------- transport
    def _post(self, body: dict) -> dict:
        """LIVE transport: `curl --ssl-no-revoke` POST, parsed as JSON. Key never echoed."""
        cmd = [
            "curl", "-s", "--ssl-no-revoke", "--max-time", "40",
            "-X", "POST", self.BASE + self.ENDPOINT,
            "-H", f"Authorization: Bearer {self._key()}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(body),
        ]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        except Exception as e:  # never include cmd (it carries the key) in the message
            raise RuntimeError(
                f"OpenAI transport failed for POST {self.ENDPOINT}: {type(e).__name__}"
            ) from None
        if proc.returncode != 0:
            raise RuntimeError(
                f"OpenAI curl failed (POST {self.ENDPOINT}) rc={proc.returncode}: "
                f"{self._redact(proc.stderr)}"
            )
        try:
            return json.loads(proc.stdout)
        except json.JSONDecodeError:
            raise RuntimeError(
                f"OpenAI returned non-JSON (POST {self.ENDPOINT}): "
                f"{self._redact(proc.stdout)[:200]}"
            )
