"""
incept_one_beats.py  -  authored One-Beat Check items for interactive intro videos (council rule 2026-07-22).

WHAT: one NON-GATING in-video recognition question per QUALIFYING concept video. It pauses the video at the
first natural "your turn" beat (after the target move has been shown on screen), asks a light recognition
anchor DIFFERENT IN KIND from the downstream discrimination gate, then resumes. Delivered as a tb-interaction
on the tb-video figure (see gated_reading.one_beat_xml + build_lesson_html).

SHIPS EMPTY by default: the module-level ONE_BEATS starts as {} for a single-lesson PROTOTYPE (only the entry
Noel greenlit), so the production push (which passes no one_beat_map) is unaffected and tier_a is unchanged.
The preview render loads its own map explicitly.

QC TEMPLATE (every item must satisfy, per the spec):
  - exactly ONE distinguishing feature varies between options; one interpretation only
  - the stem references NOTHING shown after the cue point (never test ahead of instruction)
  - the correct answer is resolvable from ON-SCREEN text/visual, not narration alone
  - no em dashes in any student-facing text
  - recognizably DISTINCT from the lesson's downstream discrimination items (no shared stem/option set)

cue_seconds / duration_seconds are derived from the hosted artifact's segment durations
(video_timing.one_beat_cue); recorded here so the render needs no re-probe.
"""

# ---- G9 L01 (ACC-W910-L-G9-C901-0001): "Take a Side Someone Could Argue With" -----------------------------
# Video artifact 11400 (169s, 8 segments). The fact/opinion/claim definition + the 3-question test are fully
# shown by 67s; the first "your turn" beat ENDS at 82s ("test 'Homework is boring' - which question does it
# fail?"). We pause THERE. The item is a recognition anchor on the 3-question test the video just taught, and
# the video's NEXT segment (82-115s) is its own reveal, so the pause reinforces rather than tests-ahead.
# Different in kind from the downstream 4-way discrimination (which asks to SORT four sentences).
_G9_L01 = {
    "cue_seconds": 82.0,
    "duration_seconds": 169.0,
    "item": {
        "title": "Quick check: the missing move",
        "note": "No penalty. Just your first call, then the video confirms it.",
        "stem": ('The video just asked you to test one sentence: "Homework is boring." It takes a side, '
                 'but which one of the three questions does it FAIL?'),
        "options": [
            {"id": "A", "text": "Is there a reason? (there is no reason attached)",
             "correct": True,
             "why": ('Right. "Homework is boring" states a side but gives no reason, so it fails the reason '
                     'question. That is what keeps it a bare opinion instead of an arguable claim.')},
            {"id": "B", "text": "Does it take a side? (it takes no side at all)",
             "correct": False,
             "why": ('It does take a side of sorts. The move it is missing is a reason, not a side. Watch the '
                     'reveal next.')},
        ],
    },
}

# PROTOTYPE scope: only the greenlit G9 L01 entry is wired for the preview. Import this map explicitly in the
# preview render (do NOT populate the module-level ONE_BEATS until the shape is approved, so prod stays clean).
PROTOTYPE_ONE_BEATS = {
    "ACC-W910-L-G9-C901-0001": _G9_L01,
}

# module-level registry consumed by gated_reading when no explicit one_beat_map is passed. EMPTY in prod.
ONE_BEATS = {}
