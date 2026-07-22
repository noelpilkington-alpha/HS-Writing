"""
incept_one_beats.py  -  authored One-Beat Check items for interactive intro videos.

WHAT: one NON-GATING in-video recognition question per YOUR-TURN beat of a concept video. It pauses the video
at each scripted "your turn" beat, asks a light recognition anchor DIFFERENT IN KIND from the downstream
discrimination gate, then resumes. Delivered as a tb-interaction on the tb-video figure (see
gated_reading.one_beat_xml + build_lesson_html).

RULE (2026-07-22, Noel): cover EVERY your-turn beat, no exceptions (overrides the earlier council cap of 2).
The only skips are mechanical: a beat at the very end of a video (no runtime to resume), and recap segments
(summaries, not your-turn beats).

DATA: the authored items live in the committed, reviewable data file `data/one_beats.json`, shape
  {lesson_id -> {"duration_seconds": float, "beats": [{"cue_seconds": float, "item": {...}}, ...]}}.
Each item was authored from the video's own beat prompt + reveal (see one_beat_extract.beats) and passed the
deterministic QC gate (one_beat_extract.qc_one_beat): exactly one correct option, non-empty fields, no em
dashes, no leaked choice markers, grounded in the beat.

SHIPS EMPTY: the module-level ONE_BEATS starts as {} so the PRODUCTION push (which passes no one_beat_map) is
unaffected and tier_a is unchanged. The preview render loads ALL_ONE_BEATS explicitly.
"""
from __future__ import annotations
import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_DATA = os.path.join(_HERE, "data", "one_beats.json")


def _load() -> dict:
    """Load the committed authored-items registry. Returns {} if the file is missing (never raises)."""
    try:
        with open(_DATA, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


# the FULL authored registry (45 lessons, 96 beats), loaded by the preview render explicitly.
ALL_ONE_BEATS = _load()

# module-level registry consumed by gated_reading when no explicit one_beat_map is passed. EMPTY in prod.
ONE_BEATS = {}
