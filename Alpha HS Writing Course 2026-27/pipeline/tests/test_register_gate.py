"""Register/credibility gate corpus - verify the verifier (Tier A7).

Two invariants, same doctrine as test_checker_corpus:
  1. GOLDEN: a real, current lesson passes check_register with ZERO flags. The childish stimuli were
     already fixed and the leaked "Grade-C design bet" label was scrubbed from live choice text, so a
     live lesson must be clean. (Precision: no false flags.)
  2. KNOWN-BAD: a golden mutated to (a) OPEN a body with a childish/meta opener, and (b) carry
     "a Grade-C design bet" in a discrimination CHOICE text, must each be flagged. (Recall: the gate
     catches exactly the two classes Noel + the Fable eval flagged.)

Plus conservatism guards: a mid-body signpost is NOT flagged, and design vocabulary in a choice
RATIONALE ("why") / provenance is NOT flagged (those are authoring voice, not student-facing).
"""
from __future__ import annotations

import copy
import glob
import importlib.util
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.dirname(HERE)
ROOT = os.path.dirname(PIPE)
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)

from register_gate import check_register  # noqa: E402


def _load_module(path):
    spec = importlib.util.spec_from_file_location("rg_" + os.path.basename(path)[:-3], path)
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
    except SystemExit:
        pass
    return m


def golden_lesson():
    """A real, current, passing lesson from the live bank: G9 L07 integrate_not_drop_v3_1 has a
    teach_card (to mutate an opener into) and discrimination slots with structured choices=[] (to
    mutate a jargon leak into a choice text). Loading a real record keeps the golden ground-truth."""
    cands = sorted(glob.glob(os.path.join(ROOT, "Lesson_Bank_G9", "lesson_g9_l07_*_v3_1.py")))
    assert cands, "golden baseline lesson (G9 L07 v3.1) not found"
    m = _load_module(cands[0])
    L = getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0]
    assert L is not None, "no LESSON in golden baseline module"
    return copy.deepcopy(L)


# ---- (1) GOLDEN: a real live lesson passes clean --------------------------------------------

def test_golden_lesson_passes_clean():
    L = golden_lesson()
    ok, flags = check_register(L)
    assert ok, "golden (live) lesson wrongly flagged by register gate:\n" + "\n".join(flags)


# ---- (2) KNOWN-BADS: each defect is flagged --------------------------------------------------

def test_childish_opener_at_body_start_is_flagged():
    """A body that OPENS with a meta/childish opener ('The topic here is ...') must be flagged."""
    L = golden_lesson()
    tc = next(s for s in L.slots if s.kind == "teach_card")
    tc.body = "<p>The topic here is how volcanoes form.</p>" + tc.body
    ok, flags = check_register(L)
    assert ok is False, "childish opener at body start was not flagged"
    assert any("meta/childish opener" in f for f in flags), flags


def test_today_we_will_opener_is_flagged():
    """A second opener phrasing ('Today we will ...') at body start must also be flagged."""
    L = golden_lesson()
    tc = next(s for s in L.slots if s.kind == "teach_card")
    tc.body = "<p>Today we will learn how to write a claim.</p>" + tc.body
    ok, flags = check_register(L)
    assert ok is False and any("meta/childish opener" in f for f in flags), flags


def test_grade_c_design_bet_in_choice_text_is_flagged():
    """Auditor jargon ('a Grade-C design bet') leaked into a student-facing CHOICE text must flag
    (the exact Fable catch)."""
    L = golden_lesson()
    d = next(s for s in L.slots if s.kind == "discrimination" and getattr(s, "choices", None))
    d.choices[0]["text"] = "This option is a Grade-C design bet we label as a bet."
    ok, flags = check_register(L)
    assert ok is False, "leaked 'Grade-C design bet' in choice text was not flagged"
    assert any("auditor/design jargon" in f and "choice" in f for f in flags), flags


def test_distractor_jargon_in_body_is_flagged():
    """A body that names 'distractor' (QC vocabulary) in student-facing prose must flag."""
    L = golden_lesson()
    tc = next(s for s in L.slots if s.kind == "teach_card")
    tc.body = tc.body + "<p>Do not pick the distractor.</p>"
    ok, flags = check_register(L)
    assert ok is False and any("distractor" in f for f in flags), flags


# ---- (3) CONSERVATISM GUARDS: the documented over-flag modes must NOT fire -------------------

def test_this_lesson_is_about_signpost_is_not_flagged():
    """'This lesson is about ...' is a legitimate signpost the live corpus uses (G9 L04, G11 L24); it
    is intentionally NOT a banned opener and must never flag, at body start OR mid-body."""
    L = golden_lesson()
    tc = next(s for s in L.slots if s.kind == "teach_card")
    tc.body = "<p>This lesson is about how the quote sits in your sentence.</p>" + tc.body
    ok, flags = check_register(L)
    assert ok, "legitimate 'This lesson is about' signpost wrongly flagged:\n" + "\n".join(flags)


def test_childish_phrase_quoted_midbody_is_not_flagged():
    """A childish phrase QUOTED mid-body as a negative example (teaching what NOT to do) must not
    flag - it is not the body's opener. Guards the opener-window restriction against that false
    positive."""
    L = golden_lesson()
    tc = next(s for s in L.slots if s.kind == "teach_card")
    tc.body = ("<p>An arguable claim takes a side and gives a checkable reason.</p>"
               "<p>You already know the difference between a claim and a topic.</p>"
               "<p>A weak reader-facing hook restates the assignment.</p>"
               "<p>Never open a paragraph by writing 'Today we will explain the water cycle'; "
               "get straight to the claim instead.</p>")
    ok, flags = check_register(L)
    assert ok, "childish phrase quoted mid-body as an example wrongly flagged:\n" + "\n".join(flags)


def test_design_term_in_choice_rationale_is_not_flagged():
    """Design vocabulary in a choice RATIONALE ('why') is authoring/feedback voice, NOT student-facing
    text, and must NOT flag (only choice .text is scanned)."""
    L = golden_lesson()
    d = next(s for s in L.slots if s.kind == "discrimination" and getattr(s, "choices", None))
    d.choices[0]["why"] = "This is the distractor; it is a Grade-C design bet we confound on length."
    ok, flags = check_register(L)
    assert ok, "design term in choice rationale wrongly flagged:\n" + "\n".join(flags)


def test_dense_but_clean_teach_sentence_is_not_flagged():
    """A dense-but-coherent ~46-word AP teach sentence (natural top of the healthy corpus) must NOT
    trip the run-on readability flag (threshold is set above the clean corpus)."""
    L = golden_lesson()
    tc = next(s for s in L.slots if s.kind == "teach_card")
    tc.body = ("<p>A sophisticated argument puts them together and keeps them running from the first "
               "line to the last, so your thesis frames the narrow prompt as one instance of a larger "
               "question and every paragraph after it pulls that same thread through without ever "
               "letting go of the line.</p>")
    ok, flags = check_register(L)
    assert ok, "dense-but-clean teach sentence wrongly flagged as a run-on:\n" + "\n".join(flags)
