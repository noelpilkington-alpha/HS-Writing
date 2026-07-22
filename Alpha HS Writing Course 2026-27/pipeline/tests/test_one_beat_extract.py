"""
test_one_beat_extract.py  -  the your-turn beat EXTRACTOR + the authored-item QC gate.

RULE (2026-07-22): cover every your-turn beat, no exceptions. The extractor returns one beat per try_it/your_turn
segment (excluding a beat at the video end, which has no runtime to resume); the QC gate enforces the spec
template on each authored item. No network: uses a synthetic artifact modeled on the real probe shape.

Run: pytest pipeline/tests/test_one_beat_extract.py
"""
from __future__ import annotations
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.dirname(HERE)
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)

import one_beat_extract as obe  # noqa: E402


def _artifact():
    # roles start/model/try_it/model/try_it/recap -> ends 10,25,45,60,80,95 (recap end == total, excluded)
    return {"output_json": {"script": [
        {"role": "start", "duration_seconds": 10, "narration": "Intro."},
        {"role": "model", "duration_seconds": 15, "narration": "A claim takes a side and a reason."},
        {"role": "try_it", "duration_seconds": 20, "narration": "Your turn. Test 'Recess is fun'.",
         "student_facing_prompt": "Which question does 'Recess is fun' fail?"},
        {"role": "model", "duration_seconds": 15, "narration": "Reveal. It gives no reason, so it fails reason."},
        {"role": "try_it", "duration_seconds": 20, "narration": "Now build one from 'Kids have recess'.",
         "student_facing_prompt": "Which addition makes it a claim?"},
        {"role": "recap", "duration_seconds": 15, "narration": "So: side plus reason."},
    ]}}


def test_beats_extracts_every_your_turn_excluding_end():
    bs = obe.beats(_artifact())
    assert [b["index"] for b in bs] == [2, 4], "both try_it beats"
    assert [b["cue_seconds"] for b in bs] == [45.0, 80.0]
    assert all(b["role"] == "try_it" for b in bs)


def test_beats_carries_prompt_and_reveal():
    bs = obe.beats(_artifact())
    assert bs[0]["prompt"] == "Which question does 'Recess is fun' fail?"
    assert "fails reason" in bs[0]["reveal"], "the following model segment is the reveal"
    assert bs[1]["prompt"] == "Which addition makes it a claim?"


def test_beats_excludes_your_turn_at_video_end():
    # a try_it that IS the final segment has no runtime to resume -> excluded.
    art = {"output_json": {"script": [
        {"role": "model", "duration_seconds": 30, "narration": "teach"},
        {"role": "try_it", "duration_seconds": 20, "narration": "your turn"},  # end 50 == total
    ]}}
    assert obe.beats(art) == []


def test_beats_never_raises_on_garbage():
    for bad in (None, 42, "x", {"output_json": "nope"}, {}):
        assert obe.beats(bad) == []


# ---- QC gate ----------------------------------------------------------------

_GOOD = {
    "title": "Quick check", "note": "No penalty.",
    "stem": "Which question does the sentence about recess fail?",
    "options": [
        {"id": "A", "text": "the reason question", "correct": True, "why": "yes, no reason attached"},
        {"id": "B", "text": "the side question", "correct": False, "why": "it does take a side"},
    ],
}


def test_qc_passes_clean_item():
    assert obe.qc_one_beat(_GOOD) == []


def test_qc_flags_no_correct():
    bad = {"stem": "s", "options": [{"id": "A", "text": "x", "correct": False, "why": "w"},
                                    {"id": "B", "text": "y", "correct": False, "why": "w"}]}
    probs = obe.qc_one_beat(bad)
    assert any("exactly one option must be correct" in p for p in probs)


def test_qc_flags_two_correct():
    bad = {"stem": "s", "options": [{"id": "A", "text": "x", "correct": True, "why": "w"},
                                    {"id": "B", "text": "y", "correct": True, "why": "w"}]}
    assert any("exactly one option must be correct" in p for p in obe.qc_one_beat(bad))


def test_qc_flags_empty_why_and_text():
    bad = {"stem": "s", "options": [{"id": "A", "text": "x", "correct": True, "why": ""},
                                    {"id": "B", "text": "", "correct": False, "why": "w"}]}
    probs = obe.qc_one_beat(bad)
    assert any("empty 'why'" in p for p in probs) and any("empty text" in p for p in probs)


def test_qc_flags_em_dash():
    bad = dict(_GOOD, stem="A claim needs a side and a reason - both of them.".replace(" - ", " — "))
    assert any("em dash in stem" in p for p in obe.qc_one_beat(bad))


def test_qc_flags_em_dash_in_option():
    opt = [{"id": "A", "text": "the reason — the missing move", "correct": True, "why": "w"},
           {"id": "B", "text": "the side", "correct": False, "why": "w"}]
    bad = dict(_GOOD, options=opt)
    assert any("em dash in option A text" in p for p in obe.qc_one_beat(bad))


def test_qc_grounding_check_with_beat():
    beat = {"prompt": "Which addition turns the fact about phones into a claim?",
            "narration": "Now build one from the phones fact."}
    # a stem about something totally unrelated shares no content word -> flagged
    off = dict(_GOOD, stem="What color is the sky today?")
    assert any("grounding" in p for p in obe.qc_one_beat(off, beat))
    # an on-topic stem passes
    on = dict(_GOOD, stem="Which addition turns the phones fact into a claim?")
    assert not any("grounding" in p for p in obe.qc_one_beat(on, beat))
