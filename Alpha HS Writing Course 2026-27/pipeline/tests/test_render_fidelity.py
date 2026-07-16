"""
test_render_fidelity.py  -  verify the RENDER-FIDELITY checks in gated_reading.render_qc (Tier A6).

These checks parse the RENDERED output back and assert integrity, catching the "mangled options / chopped
reveal behind a green PASS badge" class the Fable eval flagged (FABLE5_PIPELINE_EVAL section 2a) and the
"Cat-N label" / leaked-figure-blob class (Test Builder BrainLift). Per the checker-corpus doctrine
(tests/fixtures.py): a corpus of only-passing content validates nothing; the known-BAD fixtures are the
load-bearing half. So this file pairs ONE golden (a real clean lesson renders with no NEW problems) with
one KNOWN-BAD per check (assert each defect IS flagged, and that the defect string names the right class).

Run: pytest pipeline/tests/test_render_fidelity.py
"""
from __future__ import annotations
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.dirname(HERE)
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)

from lesson_contract import Lesson, Slot          # noqa: E402
from gated_reading import build_lesson_html, render_qc, checkpoint_xml, _content_card, _node, NODE_COLORS  # noqa: E402
from fixtures import golden_lesson                # noqa: E402


# ---------------------------------------------------------------------------
# GOLDEN: a real clean lesson renders with NO render-fidelity problems.
# ---------------------------------------------------------------------------

def test_golden_lesson_renders_clean():
    """A real passing lesson from the bank must render with zero render_qc problems, including the NEW checks
    AND the choices[] cross-check (pass the source lesson so option-count integrity is asserted too)."""
    L = golden_lesson()
    html, checkpoints = build_lesson_html(L, base_url="https://x")
    problems = render_qc(html, checkpoints, lessons=L)
    assert problems == [], f"golden lesson should render clean, got: {problems}"


def test_golden_lesson_clean_without_source_arg():
    """Backward-compatible call shape (html, checkpoints) - the two live callers use this. Still clean."""
    L = golden_lesson()
    html, checkpoints = build_lesson_html(L, base_url="https://x")
    assert render_qc(html, checkpoints) == []


# ---------------------------------------------------------------------------
# Helpers to build minimal rendered artifacts for the KNOWN-BAD checks.
# ---------------------------------------------------------------------------

def _minimal_lesson_html(body_inner: str) -> str:
    """Wrap a body fragment in the same <body>/tb-article-container shell build_lesson_html emits, so render_qc's
    body parse + narration scan see it exactly as they would a real lesson."""
    return ('<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8"><title>x</title></head>\n'
            '<body>\n  <div class="tb-article-container">' + body_inner +
            '</div>\n  <div class="tb-catalog" hidden></div>\n</body></html>')


def _narration_node(inner_html: str) -> str:
    """A content node whose tb-narration div carries `inner_html` verbatim (as a stimulus/diagram would)."""
    card = _content_card("A stimulus", [inner_html], "narr-1", NODE_COLORS[0])
    return _node(NODE_COLORS[0], card, first=True, last=True)


# ---------------------------------------------------------------------------
# KNOWN-BAD 1a: a chopped option (leaked "(A)/(B)" choice marker inside an option's text).
# This is the eval's slot-6 defect: reveal prose split mid-list into a fake option item.
# ---------------------------------------------------------------------------

def test_chopped_option_leaked_marker_is_flagged():
    # a discrimination whose body has options + a reveal but NO explicit choices[], forcing the prose-parse path
    # that produced the eval's mangled render. The reveal's inline "(B)"/"(C)" chop into the last option's text.
    s = Slot(role="MODEL", kind="discrimination", title="Which move improves it?",
             body=("Which move most improves it? "
                   "(A) take a side and add a reason. "
                   "(B) add another fact. Another fact "
                   "(B), a longer sentence (C), or explaining how phones work never turns a fact into a claim."))
    xml = checkpoint_xml("cp-chop-marker", s)
    html = _minimal_lesson_html("")
    problems = render_qc(html, [("cp-chop-marker", xml)])
    assert any("leaked choice marker" in p or "fake option" in p for p in problems), \
        f"chopped option with a leaked (B)/(C) marker must be flagged, got: {problems}"


# ---------------------------------------------------------------------------
# KNOWN-BAD 1b: a chopped option that ends mid-clause on a dangling connective.
# This is the eval's slot-4 defect: "...is a bare OPINION with no reason. Only" rendered as an option.
# ---------------------------------------------------------------------------

def test_chopped_option_dangling_tail_is_flagged():
    # hand-build the exact mangled XML the eval described: an option whose text is a full sentence + a dangling
    # "Only" (the residue of chopping "...Only (C) takes a side" at the (C) marker).
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<qti-assessment-item identifier="cp-dangle">'
        '<qti-response-declaration identifier="RESPONSE"><qti-correct-response>'
        '<qti-value>opt_A</qti-value></qti-correct-response></qti-response-declaration>'
        '<qti-item-body><qti-choice-interaction response-identifier="RESPONSE">'
        '<qti-prompt>Which sentence is the arguable claim?</qti-prompt>'
        '<qti-simple-choice identifier="opt_A"><div>Schools should switch to a four-day week.</div></qti-simple-choice>'
        '<qti-simple-choice identifier="opt_B"><div>It is a bare OPINION with no reason. Only</div></qti-simple-choice>'
        '</qti-choice-interaction></qti-item-body></qti-assessment-item>')
    problems = render_qc(_minimal_lesson_html(""), [("cp-dangle", xml)])
    assert any("dangling connective" in p or "chopped mid-sentence" in p for p in problems), \
        f"option ending mid-clause on a dangling connective must be flagged, got: {problems}"


# ---------------------------------------------------------------------------
# KNOWN-BAD 1c: an EMPTY rendered option (prose chopped to nothing).
# ---------------------------------------------------------------------------

def test_empty_option_is_flagged():
    xml = (
        '<qti-assessment-item identifier="cp-empty"><qti-item-body>'
        '<qti-choice-interaction response-identifier="RESPONSE">'
        '<qti-prompt>Pick one.</qti-prompt>'
        '<qti-simple-choice identifier="opt_A"><div>A real option.</div></qti-simple-choice>'
        '<qti-simple-choice identifier="opt_B"><div></div></qti-simple-choice>'
        '</qti-choice-interaction></qti-item-body></qti-assessment-item>')
    problems = render_qc(_minimal_lesson_html(""), [("cp-empty", xml)])
    assert any("EMPTY" in p for p in problems), f"an empty rendered option must be flagged, got: {problems}"


# ---------------------------------------------------------------------------
# KNOWN-BAD 1d: rendered option count != authored slot's choices[] count (when the source lesson is passed).
# ---------------------------------------------------------------------------

def test_option_count_mismatch_is_flagged():
    # a slot declaring 3 explicit choices, but we inject XML that rendered only 2 -> the cross-check must fire.
    s = Slot(role="MODEL", kind="discrimination", title="x", labeled_grade_c=True, bank="a",
             body="Pick one. (A) one (B) two (C) three",
             choices=[{"id": "A", "text": "one", "correct": True, "why": "yes"},
                      {"id": "B", "text": "two", "correct": False, "why": "no"},
                      {"id": "C", "text": "three", "correct": False, "why": "no"}])
    L = Lesson(id="X-CNT", grade="9-10", lesson_type=2, unit="U", title="T", target="t", slots=[s])
    bad_xml = (
        '<qti-assessment-item identifier="cp-X-CNT-s1"><qti-item-body>'
        '<qti-choice-interaction response-identifier="RESPONSE"><qti-prompt>Pick one.</qti-prompt>'
        '<qti-simple-choice identifier="opt_A"><div>one</div></qti-simple-choice>'
        '<qti-simple-choice identifier="opt_B"><div>two</div></qti-simple-choice>'
        '</qti-choice-interaction></qti-item-body></qti-assessment-item>')
    problems = render_qc(_minimal_lesson_html(""), [("cp-X-CNT-s1", bad_xml)], lessons=L)
    assert any("declares 3 choices" in p and "rendered 2" in p for p in problems), \
        f"option-count mismatch vs authored choices[] must be flagged, got: {problems}"


# ---------------------------------------------------------------------------
# KNOWN-BAD 2: a leaked figure-descriptor placeholder ("[Bar graph - ...]") in student-visible content.
# ---------------------------------------------------------------------------

def test_leaked_bar_graph_placeholder_in_narration_is_flagged():
    inner = "The data shows a clear upward trend. [Bar graph - CO2 emissions rising from 1990 to 2020.]"
    problems = render_qc(_minimal_lesson_html(_narration_node(inner)), [])
    assert any("figure-descriptor placeholder" in p for p in problems), \
        f"a leaked [Bar graph - ...] blob in narration must be flagged, got: {problems}"


def test_leaked_image_placeholder_in_item_prompt_is_flagged():
    s = Slot(role="INDEPENDENT", kind="production_frq", title="Write", unit="sentence", rubric_ref="rc.staar",
             scored=True, body="Study the visual. [Image: a technician adjusting a solar panel] Then write your claim.")
    xml = __import__("gated_reading").frq_xml("frq-img", s)
    problems = render_qc(_minimal_lesson_html(""), [("frq-img", xml)])
    assert any("figure-descriptor placeholder" in p for p in problems), \
        f"a leaked [Image: ...] blob in an FRQ prompt must be flagged, got: {problems}"


def test_authored_fillin_frame_is_not_flagged_as_placeholder():
    # a real authored fill-in frame like "[your side on the four-day week]" must NOT trip the placeholder check
    # (precision guard: the check anchors on a figure/visual keyword, not any bracketed text).
    inner = "Copy this frame: Schools should ______ [your side on the four-day week], because ______ [your reason]."
    problems = render_qc(_minimal_lesson_html(_narration_node(inner)), [])
    assert not any("figure-descriptor placeholder" in p for p in problems), \
        f"an authored fill-in frame must NOT be flagged as a placeholder, got: {problems}"


# ---------------------------------------------------------------------------
# KNOWN-BAD 3: generic Cat-N axis/category labels where real data labels are expected.
# ---------------------------------------------------------------------------

def test_cat_n_labels_in_stimulus_are_flagged():
    inner = ("The chart compares three groups. The x-axis is labeled Category 1, Category 2, and Category 3, "
             "with bars rising left to right.")
    problems = render_qc(_minimal_lesson_html(_narration_node(inner)), [])
    assert any("Cat-N labels" in p for p in problems), \
        f"generic 'Category 1/2/3' placeholder labels must be flagged, got: {problems}"


def test_lone_category_reference_is_not_flagged():
    # a single "Category 3" (e.g. a hurricane) is legitimate; only a SEQUENCE of generic siblings is the defect.
    inner = "A Category 3 hurricane made landfall, and the essay argues cities were underprepared for it."
    problems = render_qc(_minimal_lesson_html(_narration_node(inner)), [])
    assert not any("Cat-N labels" in p for p in problems), \
        f"a lone 'Category 3' reference must NOT be flagged, got: {problems}"


# ---------------------------------------------------------------------------
# Regression: the EXISTING checks still work (well-formed body, wall of text, etc. are untouched).
# ---------------------------------------------------------------------------

def test_existing_wall_of_text_check_still_fires():
    s = Slot(role="INDEPENDENT", kind="production_frq", title="Write", unit="sentence", rubric_ref="rc.staar",
             scored=True,
             body=(" ".join(["word"] * 60) + " and finally write your claim now"))
    xml = __import__("gated_reading").frq_xml("frq-wall", s)
    # force the no-block-break shape: strip the <p> wrappers _render_task produced, leaving a bare run
    import re
    xml2 = re.sub(r"</?p[^>]*>", "", xml)
    problems = render_qc(_minimal_lesson_html(""), [("frq-wall", xml2)])
    assert any("wall of text" in p for p in problems), \
        f"the pre-existing wall-of-text check must still fire, got: {problems}"
