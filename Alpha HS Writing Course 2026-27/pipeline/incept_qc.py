"""
incept_qc.py  -  an ADVISORY second-judge wrapper around the Incept /api/v1/qc endpoint.

WHAT THIS IS (and is NOT):
  * It is an INDEPENDENT second judge on our discrimination/production items. Incept QC scores an
    item you supply and returns axis scores + a pass verdict.
  * It is ADVISORY ONLY. Nothing in this module raises to fail a build or a gate. Our 30-gate
    contract stays the sole hard gate; QC output feeds a HUMAN-REVIEW shortlist that informs the
    NEXT content pass. This keeps the build offline-deterministic (Noel's decision).

DRY-BY-DEFAULT:
  qc_item(..., live=False) makes NO network call: it returns the would-send body from InceptClient.
  Only qc_item(..., live=True) POSTs + polls the QC endpoint to a terminal verdict.

SECRET / CONTENT HYGIENE (hard requirement):
  The receipt file (incept_qc_receipts.json) stores ONLY numeric scores, pass booleans, axis ids,
  and a single `flagged` boolean. It NEVER stores prompts, presigned URLs, student-facing content
  (stems/options/answers), rationales, or any explanation text. record() actively strips the verdict
  down to that allow-list so a leaky Incept response can never write a secret or content into the
  committed receipt.

Stdlib only (json + os), plus the sibling InceptClient for transport.
"""
from __future__ import annotations

import json
import os
import time

from incept_client import InceptClient

HERE = os.path.dirname(os.path.abspath(__file__))
RECEIPTS_PATH = os.path.join(HERE, "incept_qc_receipts.json")

# the advisory review bar: an item scoring below this (or failing) is surfaced for human review.
FLAG_THRESHOLD = 85

# QC terminal states we stop polling on.
_TERMINAL = {"complete", "completed", "done", "succeeded", "failed", "error"}


# ---- slot -> QC content ----------------------------------------------------
def slot_to_qc_content(slot) -> dict:
    """Map a lesson Slot to the Incept QC `content` shape.

    Discrimination (choices=[{id,text,correct,why}]) -> the probe-proven shape:
        {"stem": <title>, "options": [<option texts>],
         "answer_key": {"answer": <correct text>, "explanation": <correct why>}}
    A production_frq (a text artifact, no options) -> {"stem": <title>, "prompt": <body>}.
    """
    kind = getattr(slot, "kind", "")
    choices = getattr(slot, "choices", None) or []
    if kind in ("discrimination", "predict_the_fix", "self_score", "sr_practice") or choices:
        options = [str(c.get("text", "")) for c in choices]
        correct = next((c for c in choices if c.get("correct")), None)
        answer_key = {}
        if correct is not None:
            answer_key = {
                "answer": str(correct.get("text", "")),
                "explanation": str(correct.get("why", "")),
            }
        return {
            "stem": getattr(slot, "title", "") or "",
            "options": options,
            "answer_key": answer_key,
        }
    # production_frq / diagnosis_frq / teach text: a text artifact, mapped stem + prompt/body.
    return {
        "stem": getattr(slot, "title", "") or "",
        "prompt": getattr(slot, "body", "") or "",
    }


def _generation_type(slot) -> str:
    """The Incept generation_type to QC this slot as: discrimination-family -> 'question', else 'text'."""
    kind = getattr(slot, "kind", "")
    choices = getattr(slot, "choices", None) or []
    if kind in ("discrimination", "predict_the_fix", "self_score", "sr_practice") or choices:
        return "question"
    return "text"


# ---- lesson loading (for qc_item by id) ------------------------------------
def _find_lesson(lesson_id: str):
    """Locate a Lesson by its .id across the four grade lesson banks. Returns the Lesson or None.

    Only used when qc_item is called without an explicit `lesson=`. Import kept local so the module
    imports cleanly (and tests that pass `lesson=` never touch the bank on disk)."""
    import glob
    import importlib.util

    root = os.path.dirname(HERE)
    for grade in ("G9", "G10", "G11", "G12"):
        pat = os.path.join(root, f"Lesson_Bank_{grade}", f"lesson_{grade.lower()}_l[0-9]*.py")
        for f in sorted(glob.glob(pat)):
            if "_deprecated" in f:
                continue
            try:
                spec = importlib.util.spec_from_file_location("iqc_" + os.path.basename(f)[:-3], f)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
            except SystemExit:
                mod = None
            except Exception:
                continue
            for L in getattr(mod, "LESSONS", []) if mod else []:
                if getattr(L, "id", None) == lesson_id:
                    return L
    return None


# ---- the QC call ------------------------------------------------------------
def qc_item(lesson_id: str, slot_idx: int, live: bool = False,
            lesson=None, client: InceptClient | None = None,
            grade_levels=None, subject: str = "writing", prompt: str | None = None) -> dict:
    """QC one slot as an independent second judge. ADVISORY: never raises to fail a build.

    DRY (live=False): returns the would-send body from the client (no network).
    LIVE (live=True): POSTs to /api/v1/qc, polls /api/v1/qc/<id> to a terminal state, returns the verdict.

    Pass `lesson=` to QC an in-memory Lesson (tests, single-lesson runs); otherwise the lesson is
    located by id across the banks. Pass `client=` to inject a client (tests); else a default one.
    """
    if lesson is None:
        lesson = _find_lesson(lesson_id)
        if lesson is None:
            # advisory module: surface the problem as data, never raise.
            return {"status": "not_found", "lesson_id": lesson_id, "slot_idx": slot_idx}
    if client is None:
        client = InceptClient()

    slots = getattr(lesson, "slots", [])
    if slot_idx < 0 or slot_idx >= len(slots):
        return {"status": "bad_slot", "lesson_id": lesson_id, "slot_idx": slot_idx}
    slot = slots[slot_idx]

    content = slot_to_qc_content(slot)
    gen_type = _generation_type(slot)

    resp = client.qc(gen_type, content, prompt=prompt,
                     grade_levels=grade_levels, subject=subject, live=live)
    if not live:
        # dry stub straight from the client: {"status":"dry","would_send":...,"request_id":None}
        return resp

    # live: poll to a terminal state, then return the verdict payload.
    request_id = resp.get("request_id") or resp.get("id")
    verdict = resp
    for _ in range(40):
        status = str(verdict.get("status", "")).lower()
        if status in _TERMINAL or request_id is None:
            break
        time.sleep(2)
        verdict = client.poll(request_id, kind="qc", live=True)
    return verdict


# ---- redacted receipt (scores/axes/flag ONLY) ------------------------------
def _redact_verdict(verdict: dict) -> dict:
    """Strip a QC verdict down to the receipt allow-list: {judge_score, passed, axes:[{id,score,pass}],
    flagged}. NO prompts, NO URLs, NO content/answer text, NO rationale/explanation strings ever survive.

    `flagged` = the item is below the advisory bar: passed is False OR judge_score < FLAG_THRESHOLD.
    """
    v = verdict or {}
    score = v.get("judge_score", v.get("score"))
    try:
        score = float(score) if score is not None else None
    except (TypeError, ValueError):
        score = None
    passed = bool(v.get("passed", v.get("pass", False)))

    axes_out = []
    for ax in v.get("axes", []) or []:
        if not isinstance(ax, dict):
            continue
        ax_score = ax.get("score")
        try:
            ax_score = float(ax_score) if ax_score is not None else None
        except (TypeError, ValueError):
            ax_score = None
        axes_out.append({
            "id": str(ax.get("id", "")),          # an axis LABEL/id, never content
            "score": ax_score,                    # numeric only
            "pass": bool(ax.get("pass", ax.get("passed", False))),
        })

    flagged = (not passed) or (score is not None and score < FLAG_THRESHOLD)
    # numeric scores may be whole ints; keep them clean in the receipt.
    if score is not None and float(score).is_integer():
        score = int(score)
    for ax in axes_out:
        if ax["score"] is not None and float(ax["score"]).is_integer():
            ax["score"] = int(ax["score"])
    return {"judge_score": score, "passed": passed, "axes": axes_out, "flagged": bool(flagged)}


def record(lesson_id: str, slot_idx: int, verdict: dict, path: str | None = None) -> None:
    """Append a REDACTED receipt to the receipt JSON, keyed f"{lesson_id}:s{slot_idx}".

    Stores ONLY {judge_score, passed, axes:[{id,score,pass}], flagged}. Prompts, URLs, and all
    student-facing content/answer text are dropped by _redact_verdict before anything is written.
    """
    path = path or RECEIPTS_PATH
    data = {}
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, json.JSONDecodeError):
            data = {}
    key = f"{lesson_id}:s{slot_idx}"
    data[key] = _redact_verdict(verdict)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, sort_keys=True)


def low_scoring(threshold: int = FLAG_THRESHOLD, path: str | None = None) -> list:
    """Read the receipt file and return the human-review shortlist: items below the bar.

    An item is shortlisted when it is flagged OR its judge_score is below `threshold`. Each row is
    {"key": "<lesson>:s<idx>", "judge_score": <n>, "flagged": <bool>}, sorted lowest score first.
    Missing/empty receipt file -> empty list (advisory: never raises).
    """
    path = path or RECEIPTS_PATH
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return []
    rows = []
    for key, entry in (data or {}).items():
        if not isinstance(entry, dict):
            continue
        score = entry.get("judge_score")
        flagged = bool(entry.get("flagged"))
        below = (score is not None and score < threshold)
        if flagged or below:
            rows.append({"key": key, "judge_score": score, "flagged": flagged})
    rows.sort(key=lambda r: (r["judge_score"] is None, r["judge_score"] if r["judge_score"] is not None else 0))
    return rows
