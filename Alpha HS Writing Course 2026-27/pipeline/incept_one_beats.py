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
# Video artifact 11400 (169s, 8 segments). The video scripts TWO "your turn" beats, so it gets TWO One-Beat
# checks (council cap = 2), one per scripted pause:
#   beat 1 @ 82s (after seg3 "test 'Homework is boring'"): the fact/opinion/claim definition + 3-question test
#     are fully shown by 67s, so this recognizes WHICH question the sentence fails. seg4 (82-115s) is the
#     video's own reveal -> reinforces, never tests-ahead.
#   beat 2 @ 131s (after seg5 "now build one yourself from the fact 'Students use phones during the school
#     day'"): the video is about to rebuild it in two moves (seg6, 131-152s). Rather than a graded free-text
#     write mid-video (a hard gate + validity problem the council ruled OUT), this is a recognition anchor on
#     the two-move schema: which added part turns the fact into an arguable claim. seg6 then reveals the build.
# Both are DIFFERENT IN KIND from the downstream 4-way discrimination + the downstream production writes.
_G9_L01 = {
    "duration_seconds": 169.0,
    "beats": [
        {
            "cue_seconds": 82.0,
            "item": {
                "title": "Quick check: the missing move",
                "note": "No penalty. Just your first call, then the video confirms it.",
                "stem": ('The video just asked you to test one sentence: "Homework is boring." It takes a side, '
                         'but which one of the three questions does it FAIL?'),
                "options": [
                    {"id": "A", "text": "Is there a reason? (there is no reason attached)",
                     "correct": True,
                     "why": ('Right. "Homework is boring" states a side but gives no reason, so it fails the '
                             'reason question. That is what keeps it a bare opinion instead of an arguable claim.')},
                    {"id": "B", "text": "Does it take a side? (it takes no side at all)",
                     "correct": False,
                     "why": ('It does take a side of sorts. The move it is missing is a reason, not a side. '
                             'Watch the reveal next.')},
                ],
            },
        },
        {
            "cue_seconds": 131.0,
            "item": {
                "title": "Quick check: build the claim",
                "note": "No penalty. Make your call, then watch the rebuild.",
                "stem": ('The video just asked you to rebuild this fact into an arguable claim: "Students use '
                         'phones during the school day." Which single addition turns that fact into a claim?'),
                "options": [
                    {"id": "A", "text": "Add a side to take AND a reason that backs it",
                     "correct": True,
                     "why": ('Right. A fact becomes an arguable claim only when you take a side someone could '
                             'reject and attach a reason. That is the two-move build the video shows next.')},
                    {"id": "B", "text": "Add another fact about how often phones are used",
                     "correct": False,
                     "why": ('More facts stay facts. A second checkable detail does not take a side or give a '
                             'reason, so it never turns into a claim.')},
                ],
            },
        },
    ],
}

# PROTOTYPE scope: only the greenlit G9 L01 entry is wired for the preview. Import this map explicitly in the
# preview render (do NOT populate the module-level ONE_BEATS until the shape is approved, so prod stays clean).
PROTOTYPE_ONE_BEATS = {
    "ACC-W910-L-G9-C901-0001": _G9_L01,
}

# module-level registry consumed by gated_reading when no explicit one_beat_map is passed. EMPTY in prod.
ONE_BEATS = {}
