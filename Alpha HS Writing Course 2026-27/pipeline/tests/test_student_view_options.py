"""
test_student_view_options.py - the audit-lens (render_student_experience) must show the SAME options a
student sees in the pushed QTI item.

Bug this locks down: discrimination / predict_the_fix slots may carry their options ONLY in the structured
choices[] array (empty body prose). The student-view renderer parsed options out of the BODY, so for those
slots it emitted a prompt with ZERO options. The sim-student and readiness audits walk this renderer, so they
reported "blank / unanswerable multiple-choice steps" for exactly those slots - even though gated_reading
(the production push) renders the options correctly from choices[]. That divergence made a real render defect
IN THE AUDIT LENS look like a lesson defect, and (worse) got dismissed as a model hallucination.

Per the checker-corpus doctrine: the KNOWN-BAD fixture (options only in choices[]) is the load-bearing half.
We pair it with the two intact shapes (options in body; options in both) which must be UNCHANGED by the fix.

Run: pytest pipeline/tests/test_student_view_options.py
"""
from __future__ import annotations
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.dirname(HERE)
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)

from lesson_contract import Lesson, Slot            # noqa: E402
import lesson_review                                # noqa: E402


def _one_slot_lesson(slot: Slot) -> Lesson:
    return Lesson(id="X-SV", grade="9-10", lesson_type=2, unit="U", title="T", target="t", slots=[slot])


def _step1_block(view: str) -> str:
    """Return the STEP 1 block text (up to STEP 2 or end)."""
    m = re.search(r"(STEP 1 \(CHECK.*?)(?:\nSTEP 2 \(|\Z)", view, re.S)
    return m.group(1) if m else ""


def _count_option_lines(block: str) -> int:
    return len(re.findall(r"(?m)^\s*\([A-D]\)\s", block))


_CHOICES = [
    {"id": "A", "text": "Schools should reward good report cards.", "correct": False, "why": "vague side"},
    {"id": "B", "text": "Schools should pay twenty dollars per A.", "correct": False, "why": "no stakes"},
    {"id": "C", "text": "Pay twenty dollars per A, because it keeps at-risk students enrolled.",
     "correct": True, "why": "specific side and real stakes"},
]


# ---------------------------------------------------------------------------
# KNOWN-BAD (the bug): options live ONLY in choices[]; body has none.
# Before the fix this rendered a prompt with ZERO options.
# ---------------------------------------------------------------------------

def test_discrimination_options_only_in_choices_are_rendered():
    s = Slot(role="MODEL", kind="discrimination", title="Which claim has BOTH a side and its stakes?",
             body="Each option argues for paying for grades. Which one has both?", choices=_CHOICES)
    view = lesson_review.render_student_experience(_one_slot_lesson(s))
    block = _step1_block(view)
    assert _count_option_lines(block) == 3, f"all 3 choices[] options must render, got block:\n{block}"
    assert "Pay twenty dollars per A, because it keeps at-risk students" in block


def test_discrimination_choices_only_shows_reveal_as_post_answer_feedback():
    s = Slot(role="MODEL", kind="discrimination", title="Which claim has BOTH a side and its stakes?",
             body="Which one has both?", choices=_CHOICES)
    view = lesson_review.render_student_experience(_one_slot_lesson(s))
    block = _step1_block(view)
    # the correct choice's `why` becomes the after-answer reveal, NOT shown with the options
    assert "after the student answers" in block
    assert "specific side and real stakes" in block


def test_predict_the_fix_options_only_in_choices_are_rendered():
    s = Slot(role="MODEL", kind="predict_the_fix", title="Diagnose then pick the fix",
             body="Diagnose the weak draft, then pick the fix.", feedback="The fix adds the missing warrant.",
             choices=_CHOICES)
    view = lesson_review.render_student_experience(_one_slot_lesson(s))
    m = re.search(r"(STEP 1 \(CHECK - diagnose.*?)(?:\nSTEP 2 \(|\Z)", view, re.S)
    block = m.group(1) if m else ""
    assert _count_option_lines(block) == 3, f"predict_the_fix must render its 3 choices[], got:\n{block}"


# ---------------------------------------------------------------------------
# UNCHANGED: options in the body prose still render exactly as before (the fix must NOT touch these).
# ---------------------------------------------------------------------------

def test_discrimination_options_in_body_still_render():
    s = Slot(role="MODEL", kind="discrimination", title="Pick the arguable claim",
             body=("Which is arguable? (A) The sky is blue. (B) Schools should start later. "
                   "(C) Water is wet. Correct: B takes a debatable side."))
    view = lesson_review.render_student_experience(_one_slot_lesson(s))
    block = _step1_block(view)
    assert _count_option_lines(block) == 3, f"body-prose options must still stack, got:\n{block}"
    assert "after the student answers" in block  # the "Correct:" reveal is still split out


def test_discrimination_options_in_both_prefers_body_and_does_not_double():
    # options present in BOTH body and choices[] (the common case): body wins, no duplication.
    s = Slot(role="MODEL", kind="discrimination", title="Pick the arguable claim",
             body="Which is arguable? (A) Sky is blue. (B) Start school later. (C) Water is wet.",
             choices=_CHOICES)
    view = lesson_review.render_student_experience(_one_slot_lesson(s))
    block = _step1_block(view)
    assert _count_option_lines(block) == 3, f"must render exactly 3 (no doubling), got:\n{block}"
    assert "Start school later" in block and "at-risk students" not in block
