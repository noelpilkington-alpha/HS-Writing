"""
incept_test.py  -  generate + fetch a full Incept `test` artifact for the G9 bake-off.

Thin wrapper over InceptClient. LIVE calls go through the client (which handles auth, curl --ssl-no-revoke,
poll/fetch, and key redaction). DRY/offline reads a cached artifact so the bake-off is re-runnable without
the API. Never logs the key.
"""
from __future__ import annotations
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from incept_client import InceptClient  # noqa: E402

_TEST_OPTIONS = {"purpose": "mastery", "grain": "grade_level", "structure": "single"}
_PROMPT = ("A complete grade 9 argumentative writing test built around a reading passage: a source passage, "
           "several multiple-choice items on claims and evidence tied to the passage, at least one short "
           "constructed-response item, and one extended constructed-response argument essay with a rubric.")

def generate_g9_test(live: bool = False, client: InceptClient | None = None) -> dict:
    client = client or InceptClient()
    return client.generate(_PROMPT, "test", options=dict(_TEST_OPTIONS),
                           grade_levels=["g9"], subject="writing", live=live)

def fetch_g9_test(artifact_id, live: bool = False, client: InceptClient | None = None) -> dict:
    client = client or InceptClient()
    art = client.artifact(artifact_id, live=live)
    return (art or {}).get("output_json", {})

def load_cached_output_json(path: str = "C:/tmp/incept_fulltest_11324.json") -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh).get("output_json", {})
