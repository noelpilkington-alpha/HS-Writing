"""
incept_client.py  -  shared transport for the Incept API (https://v2.incept.school).

DRY-BY-DEFAULT / --live contract (the whole point of this module):
  * Every method takes `live: bool` (default False).
  * DRY mode (live=False):
      - generate() / qc() make NO network call. They return the request they WOULD send:
        {"status": "dry", "would_send": <body dict>, "request_id": None}.
      - options() / poll() / artifact() are READS: they read a local cache dir and raise a
        clear error on cache miss (nothing is fetched in dry mode).
  * LIVE mode (live=True): the ONLY transport is `curl` via subprocess, with the flags
      curl -s --ssl-no-revoke --max-time 40 -X <METHOD> <base+path>
           -H "Authorization: Bearer <key>" [-H "Content-Type: application/json" -d <body>]
    `--ssl-no-revoke` is REQUIRED (verified 2026-07-20: without it, TLS fails with a Windows
    schannel cert-revocation error). Responses are parsed as JSON.

SECRET HYGIENE (hard requirement):
  The API key is read from the env var INCEPT_API_KEY, else parsed from
  `../Incept/Incept Production details.md` (the `ik_...` line after the `## API Key` heading).
  It is wrapped in a redacting holder so it NEVER appears in __repr__, str(vars(self)), any log,
  or any error message.

Stdlib only (subprocess + json). No `requests` dependency.
"""
from __future__ import annotations
import os
import json
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
_KEY_FILE = os.path.join(HERE, "..", "Incept", "Incept Production details.md")


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
    """Return the Incept API key from env or the production-details file, or None if absent.

    NEVER logs or echoes the key.
    """
    env = os.environ.get("INCEPT_API_KEY")
    if env and env.strip():
        return env.strip()
    try:
        with open(_KEY_FILE, "r", encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except OSError:
        return None
    for i, line in enumerate(lines):
        if line.strip().lower() == "## api key":
            # the key is the next non-empty line after the heading
            for nxt in lines[i + 1:]:
                if nxt.strip():
                    return nxt.strip()
            break
    return None


class InceptClient:
    """Shared transport for the Incept API. Dry-by-default; `live=True` spends quota."""

    BASE = "https://v2.incept.school"

    def __init__(self, cache_dir: str = "C:/tmp/incept_cache"):
        self.cache_dir = cache_dir
        # Wrap the key in a redacting holder so it never surfaces in repr/vars/logs.
        # Resolved eagerly (local file read, no network); may be None until a live call needs it.
        self._secret = _Secret(_resolve_key())

    def __repr__(self):
        # Deliberately excludes the key holder's value (holder repr is "<redacted>" anyway).
        return f"InceptClient(cache_dir={self.cache_dir!r})"

    # ------------------------------------------------------------------ secrets
    def _key(self) -> str:
        """Return the API key; raise (without echoing it) if it could not be found."""
        key = self._secret.reveal()
        if not key:
            raise RuntimeError(
                "INCEPT_API_KEY not found: set the env var or add it under '## API Key' "
                "in Incept/Incept Production details.md"
            )
        return key

    def _redact(self, text: str) -> str:
        """Strip the key from any string before it can reach a log or error message."""
        key = self._secret.reveal()
        if key and text:
            return text.replace(key, "<redacted>")
        return text or ""

    # ---------------------------------------------------------------- transport
    def _curl(self, method: str, path: str, body: dict | None = None, live: bool = False):
        """The only transport. In dry mode a POST returns the would-send stub (no network).

        In live mode, run `curl --ssl-no-revoke` and parse the JSON response. The key is
        never echoed in any error message.
        """
        if not live:
            if method == "POST":
                return {"status": "dry", "would_send": body, "request_id": None}
            # GET reads in dry mode must go through the local cache, not this transport.
            raise RuntimeError(f"dry-mode {method} {path} must be served from the cache")

        cmd = [
            "curl", "-s", "--ssl-no-revoke", "--max-time", "40",
            "-X", method, self.BASE + path,
            "-H", f"Authorization: Bearer {self._key()}",
        ]
        if body is not None:
            cmd += ["-H", "Content-Type: application/json", "-d", json.dumps(body)]

        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        except Exception as e:  # never include cmd (it carries the key) in the message
            raise RuntimeError(f"Incept transport failed for {method} {path}: {type(e).__name__}") from None
        if proc.returncode != 0:
            raise RuntimeError(
                f"Incept curl failed ({method} {path}) rc={proc.returncode}: {self._redact(proc.stderr)}"
            )
        try:
            return json.loads(proc.stdout)
        except json.JSONDecodeError:
            raise RuntimeError(
                f"Incept returned non-JSON ({method} {path}): {self._redact(proc.stdout)[:200]}"
            )

    # -------------------------------------------------------------------- cache
    def _cache_path(self, name: str) -> str:
        # server-generated ids flow into cache filenames; basename them so a '..'-bearing
        # id can never read/write outside cache_dir (path-traversal guard).
        return os.path.join(self.cache_dir, os.path.basename(name))

    def _write_cache(self, name: str, data) -> None:
        os.makedirs(self.cache_dir, exist_ok=True)
        with open(self._cache_path(name), "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)

    def _read_cache(self, name: str):
        path = self._cache_path(name)
        if not os.path.exists(path):
            raise RuntimeError(
                f"dry-mode cache miss: {path} not found. Run the corresponding read with "
                f"live=True first to populate the cache."
            )
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    def _get_cached(self, path: str, cache_name: str, live: bool):
        """GET a read endpoint: live fetches + writes through to cache; dry reads the cache."""
        if live:
            data = self._curl("GET", path, None, live=True)
            self._write_cache(cache_name, data)
            return data
        return self._read_cache(cache_name)

    # ------------------------------------------------------------------- public
    def options(self, live: bool = False):
        """GET /api/v1/options: capability discovery."""
        return self._get_cached("/api/v1/options", "options.json", live)

    def generate(self, prompt: str, generation_type: str, options: dict | None = None,
                 grade_levels=None, subject=None, state=None, live: bool = False):
        """POST /api/v1/generate. Dry mode returns the would-send body (no network)."""
        body: dict = {"prompt": prompt, "generation_type": generation_type}
        if options is not None:
            body["options"] = options
        if grade_levels is not None:
            body["grade_levels"] = grade_levels
        if subject is not None:
            body["subject"] = subject
        if state is not None:
            body["state"] = state
        return self._curl("POST", "/api/v1/generate", body, live)

    def poll(self, request_id, kind: str = "generate", live: bool = False):
        """GET /api/v1/<kind>/<request_id>: status polling (kind: 'generate' or 'qc')."""
        return self._get_cached(
            f"/api/v1/{kind}/{request_id}", f"poll_{kind}_{request_id}.json", live
        )

    def artifact(self, artifact_id, live: bool = False):
        """GET /api/v1/artifacts/<id>: full artifact detail."""
        return self._get_cached(
            f"/api/v1/artifacts/{artifact_id}", f"artifact_{artifact_id}.json", live
        )

    def qc(self, generation_type: str, content, prompt=None,
           grade_levels=None, subject=None, live: bool = False):
        """POST /api/v1/qc: judge an artifact you supply. Dry mode returns the would-send body."""
        body: dict = {"generation_type": generation_type, "content": content}
        if prompt is not None:
            body["prompt"] = prompt
        if grade_levels is not None:
            body["grade_levels"] = grade_levels
        if subject is not None:
            body["subject"] = subject
        return self._curl("POST", "/api/v1/qc", body, live)
