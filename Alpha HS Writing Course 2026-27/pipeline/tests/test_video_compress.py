"""
test_video_compress.py  -  the Council-ruled teach_card COMPRESSION when a concept lesson has an intro video.

RULE (Council of Writing Instruction, 2026-07-21): when a concept lesson's id is registered in
incept_videos.INCEPT_VIDEOS (an intro video is bound to it), the OPENING teach_card's written recap is
COMPRESSED to just its leading "one idea" callout (the video now teaches the expanded explanation). The
callout is non-negotiable: it SHOWS the built target sentence (the <strong> example), so the compressed
recap still demonstrates the concept instead of merely asserting it. With NO video (empty registry), the
teach_card renders FULL, byte-identical to today.

Run: pytest pipeline/tests/test_video_compress.py
"""
from __future__ import annotations
import os
import re
import sys
import html as _h

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.dirname(HERE)
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)

from gated_reading import _compress_teach_body, build_lesson_html  # noqa: E402
import gated_reading as gr                                          # noqa: E402


# ---------------------------------------------------------------------------
# A synthetic teach_card body in the exact shape: a leading #0d9488 "one idea"
# callout (2 inner divs, a <strong> target example) then an expansion <ul>.
# ---------------------------------------------------------------------------
SAMPLE_CALLOUT = (
    '<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0">'
    '<div style="font-size:11px;font-weight:700;color:#0f766e;text-transform:uppercase">The one idea</div>'
    '<div style="color:#0f2f28;font-size:15px">An arguable claim takes a <strong>SIDE</strong> and gives a '
    '<strong>REASON</strong>. A fact or a bare opinion is not a claim.</div></div>')

SAMPLE_EXPANSION = (
    'Three kinds of sentence look alike but do different jobs, so keep them apart:'
    '<ul style="margin:6px 0"><li><strong>FACT</strong>: something you can check.</li>'
    '<li><strong>OPINION</strong>: a bare preference.</li></ul>'
    'That last one is the sentence an argument is built on.')

SAMPLE_BODY = SAMPLE_CALLOUT + SAMPLE_EXPANSION


# ---------------------------------------------------------------------------
# 1. _compress_teach_body: keep ONLY the callout, keep the <strong> target,
#    drop the expansion. Balanced depth-match across the callout's inner divs.
# ---------------------------------------------------------------------------

def test_compress_keeps_callout_drops_expansion():
    out = _compress_teach_body(SAMPLE_BODY)
    assert out == SAMPLE_CALLOUT, "compression must return exactly the balanced callout div"
    assert "<strong>SIDE</strong>" in out and "<strong>REASON</strong>" in out, \
        "the built target sentence (the <strong> example) must survive - the whole point"
    assert "Three kinds of sentence" not in out, "the expansion prose must be dropped"
    assert "<ul" not in out, "the expansion list must be dropped"


def test_compress_stops_at_callout_close_not_a_later_div():
    # a trailing panel <div> after the callout must NOT be swallowed by the depth-match.
    body = SAMPLE_CALLOUT + '<div class="panel">a later panel</div>'
    assert _compress_teach_body(body) == SAMPLE_CALLOUT


# ---------------------------------------------------------------------------
# 2. Defensive: no callout -> unchanged (never lose content on an unexpected shape).
# ---------------------------------------------------------------------------

def test_compress_no_callout_returns_unchanged():
    body = "<p>Just some prose with no callout.</p><ul><li>a</li></ul>"
    assert _compress_teach_body(body) == body


def test_compress_marker_without_label_returns_unchanged():
    # the #0d9488 border exists (e.g. an FRQ-style source), but no "The one idea" label -> not our callout.
    body = ('<div style="border-left:4px solid #0d9488">A source block with no one-idea label.</div>'
            '<p>rest</p>')
    assert _compress_teach_body(body) == body


def test_compress_label_without_marker_returns_unchanged():
    body = '<div style="border-left:4px solid #333">The one idea, but not the signature border.</div><p>x</p>'
    assert _compress_teach_body(body) == body


# ---------------------------------------------------------------------------
# Helpers for the render tests: find a REAL G9 concept lesson whose opening
# slot is a one-idea teach_card with an expansion to drop.
# ---------------------------------------------------------------------------

def _plain(s: str) -> str:
    t = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", _h.unescape(t)).strip()


def _lead_phrase(expansion_html: str) -> str:
    """A distinctive plain-text phrase from the START of the expansion (stays within the first sentence and
    trims to a word boundary), used to detect the expansion in rendered output."""
    p = _plain(expansion_html).split(".")[0]
    return p[:40].rsplit(" ", 1)[0]


def _find_g9_callout_lesson():
    import tier_a_regression as T
    for _f, L in T._lessons("G9"):
        slots = getattr(L, "slots", None) or []
        s0 = slots[0] if slots else None
        if not (s0 and getattr(s0, "kind", "") == "teach_card" and getattr(s0, "body", "")):
            continue
        b = s0.body
        if "border-left:4px solid #0d9488" in b and "The one idea" in b:
            if _compress_teach_body(b) != b:   # must have an expansion to drop
                return L
    return None


# ---------------------------------------------------------------------------
# 3. Empty registry (ships empty) => teach_card renders FULL (compression NOT triggered).
# ---------------------------------------------------------------------------

def test_empty_registry_ships_empty():
    from incept_videos import INCEPT_VIDEOS
    assert INCEPT_VIDEOS == {}, "the registry ships EMPTY (populated later by the wiring step)"
    assert gr._INCEPT_VIDEOS == {}


def test_empty_registry_renders_full_teach_body():
    L = _find_g9_callout_lesson()
    assert L is not None, "expected a real G9 one-idea teach_card lesson"
    body0 = L.slots[0].body
    callout = _compress_teach_body(body0)
    expansion = body0[len(callout):]
    marker = _lead_phrase(expansion)
    assert marker, "the chosen lesson must have a non-empty expansion"
    html, _ = build_lesson_html(L, base_url="https://x")
    assert marker in _plain(html), "with an empty registry the FULL expansion must render (not compressed)"


# ---------------------------------------------------------------------------
# 4. Registry HIT => the opening teach_card is compressed: <strong> target survives, expansion gone.
# ---------------------------------------------------------------------------

def test_registry_hit_compresses_opening_teach_card(monkeypatch):
    L = _find_g9_callout_lesson()
    assert L is not None
    body0 = L.slots[0].body
    callout = _compress_teach_body(body0)
    m = re.search(r"<strong>(.*?)</strong>", callout)
    assert m, "the callout must contain a <strong> target example"
    strong_tag = m.group(0)
    expansion = body0[len(callout):]
    marker = _lead_phrase(expansion)

    monkeypatch.setitem(gr._INCEPT_VIDEOS, L.id, {"mp4": "https://cdn/x.mp4", "vtt": "https://cdn/x.vtt"})
    html, _ = build_lesson_html(L, base_url="https://x")

    assert strong_tag in html, "the built target sentence (<strong> example) must survive compression"
    assert marker not in _plain(html), "the expansion the video now teaches must be dropped"
