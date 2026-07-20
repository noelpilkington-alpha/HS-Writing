# pipeline/tests/test_incept_question_seeds.py
#
# Task 4 (Phase C): incept_question_seeds.py is a SEED-ONLY distractor assist. These tests prove:
#   (a) seed_distractors(live=False) returns a dry would-send for a `question` bank request
#       whose interaction_type=="multiple_choice" and structure=="bank", with the skill prompt
#       text embedded somewhere in the would-send prompt (NO network call).
#   (b) parse_distractors turns a synthetic Incept `question` response into a flat list of
#       wrong-answer strings (correct excluded, order preserved).
#   (c) parse_distractors dedups exact repeats within one response.
#   (d) parse_distractors returns [] on an unrecognized shape (never raises).
import os
import sys

PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)

from incept_question_seeds import (
    seed_distractors,
    parse_distractors,
    SEEDS_ARE_NOT_ITEMS,
)


# ---- (a) dry would-send for a question bank request ------------------------
def test_seed_distractors_dry_returns_question_bank_would_send():
    r = seed_distractors(
        "teach: identify a bare opinion vs a defensible claim",
        ["It is raining.",
         "Schools should extend lunch because students focus better after eating."],
        n=3, live=False,
    )
    assert r["status"] == "dry"
    assert r["request_id"] is None
    body = r["would_send"]
    assert body["generation_type"] == "question"
    assert body["options"]["interaction_type"] == "multiple_choice"
    assert body["options"]["structure"] == "bank"
    # the skill/concept being taught must appear in the would-send prompt
    assert "identify a bare opinion vs a defensible claim" in body["prompt"]


# ---- (b) parse a question response into wrong-answer distractors ------------
def test_parse_distractors_excludes_correct_and_preserves_order():
    response = {
        "questions": [
            {
                "options": [
                    {"text": "correct answer", "correct": True},
                    {"text": "distractor one", "correct": False},
                    {"text": "distractor two", "correct": False},
                ]
            }
        ]
    }
    assert parse_distractors(response) == ["distractor one", "distractor two"]


# ---- (c) dedup exact repeats within one response ---------------------------
def test_parse_distractors_dedups_exact_repeats():
    assert parse_distractors({"distractors": ["a", "b", "a"]}) == ["a", "b"]


# ---- (d) unrecognized shape -> [] (never raises) ---------------------------
def test_parse_distractors_unrecognized_shape_returns_empty():
    assert parse_distractors({}) == []


# ---- guard: seeds are raw material, not items ------------------------------
def test_seeds_are_not_items_guard_present():
    assert "RAW MATERIAL" in SEEDS_ARE_NOT_ITEMS
    assert "gate_structural_item" in SEEDS_ARE_NOT_ITEMS
