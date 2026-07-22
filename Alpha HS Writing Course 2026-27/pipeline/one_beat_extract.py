"""
one_beat_extract.py  -  deterministic extraction of a video's YOUR-TURN beats + a QC gate for authored items.

RULE (updated 2026-07-22, Noel): "cover every your-turn beat, no exceptions." Every segment where the video
explicitly tells the student to pause and act (role try_it / your_turn) gets ONE non-gating in-video question,
UNLESS the beat sits at the very end of the video (no runtime left to resume). This OVERRIDES the earlier
council cap of two per video: a scripted your-turn beat that dangles with no question is the passivity failure
interactivity is meant to fix.

This module does NOT call the model. It provides:
  - beats(artifact_json): the ordered list of your-turn beats to author, each with its cue time, the beat's own
    narration/prompt, and the REVEAL segment that follows it (the video's own answer, so an authored item is
    grounded and never tests ahead of what the video states).
  - qc_one_beat(item, beat): a deterministic gate enforcing the spec's QC template on an authored item.

Pure stdlib. Never raises on a malformed artifact (returns []).
"""
from __future__ import annotations
import video_timing as vt

# segments that explicitly tell the student to pause and act. `recap` is a summary, NOT a your-turn beat, so it
# is deliberately excluded (no question on a recap unless a future rule adds retrieval checks there).
YOUR_TURN_ROLES = ("try_it", "your_turn")


def _seg_text(seg) -> str:
    if not isinstance(seg, dict):
        return ""
    return str(seg.get("narration") or seg.get("text") or seg.get("voiceover") or "").strip()


def _seg_prompt(seg) -> str:
    """The student-facing prompt the video shows at this beat, else the narration."""
    if not isinstance(seg, dict):
        return ""
    return str(seg.get("student_facing_prompt") or "").strip() or _seg_text(seg)


def beats(artifact_json) -> list:
    """Return the ordered your-turn beats to author for one video. Each beat is:
        {"index": segment_index, "cue_seconds": end_time, "role": role,
         "prompt": beat's student-facing prompt/narration,
         "narration": beat's full narration,
         "reveal": the FOLLOWING segment's narration (the video's own answer), or ""}
    A beat whose end == the video total (final segment, no runtime to resume) is EXCLUDED. Never raises."""
    try:
        script = vt._script(artifact_json)
        ends = vt._segment_ends(script)
        total = ends[-1] if ends else 0.0
        out = []
        for i, s in enumerate(script):
            role = str((s or {}).get("role", "")).lower()
            if role not in YOUR_TURN_ROLES:
                continue
            end = ends[i] if i < len(ends) else 0.0
            if not (0 < end < total):   # must have runtime AFTER it to resume
                continue
            reveal = _seg_text(script[i + 1]) if i + 1 < len(script) else ""
            out.append({"index": i, "cue_seconds": end, "role": role,
                        "prompt": _seg_prompt(s), "narration": _seg_text(s), "reveal": reveal})
        return out
    except Exception:
        return []


# ---- QC gate on an authored One-Beat item (the spec's QC template, deterministic) --------------------------

def qc_one_beat(item: dict, beat: dict | None = None) -> list:
    """Return a list of QC problem strings for one authored item (empty = clean). Enforces the spec template:
      - exactly one option flagged correct; >= 2 options
      - every option has a non-empty text + a non-empty 'why'
      - a non-empty stem
      - NO em dash anywhere in student-facing text (project hard rule)
    If `beat` is given, also warn when the stem shares no lexical anchor with the beat prompt (a loose sign the
    item may not be grounded in what the video actually asked). Never raises."""
    problems = []
    if not isinstance(item, dict):
        return ["item is not a dict"]
    stem = (item.get("stem") or "").strip()
    opts = item.get("options") or []
    note = (item.get("note") or "")
    title = (item.get("title") or "")
    if not stem:
        problems.append("empty stem")
    if not isinstance(opts, list) or len(opts) < 2:
        problems.append(f"needs >= 2 options (has {len(opts) if isinstance(opts, list) else 0})")
        opts = opts if isinstance(opts, list) else []
    n_correct = sum(1 for o in opts if isinstance(o, dict) and o.get("correct"))
    if n_correct != 1:
        problems.append(f"exactly one option must be correct (has {n_correct})")
    ids = [o.get("id") for o in opts if isinstance(o, dict)]
    if len(set(ids)) != len(ids):
        problems.append(f"duplicate option ids: {ids}")
    for o in opts:
        if not isinstance(o, dict):
            problems.append("option is not a dict"); continue
        if not (o.get("text") or "").strip():
            problems.append(f"option {o.get('id')} has empty text")
        if not (o.get("why") or "").strip():
            problems.append(f"option {o.get('id')} has empty 'why' feedback")
    # em-dash ban across ALL student-facing fields
    for field, val in (("stem", stem), ("note", note), ("title", title)):
        if "—" in (val or ""):
            problems.append(f"em dash in {field}")
    for o in opts:
        if isinstance(o, dict):
            for field in ("text", "why"):
                if "—" in (o.get(field) or ""):
                    problems.append(f"em dash in option {o.get('id')} {field}")
    # grounding heuristic (advisory): the stem should echo a content word from the beat prompt.
    if beat and stem:
        import re
        STOP = {"the", "a", "an", "to", "of", "and", "or", "is", "it", "in", "on", "your", "you", "this",
                "that", "which", "what", "here", "now", "run", "them", "then", "with", "for", "one", "pause",
                "turn", "decide", "test", "sentence", "not", "do", "does", "into", "add", "start"}
        def words(t):
            return {w for w in re.findall(r"[a-z]{4,}", (t or "").lower()) if w not in STOP}
        if beat.get("prompt") and not (words(stem) & words(beat["prompt"] + " " + beat.get("narration", ""))):
            problems.append("stem shares no content word with the beat prompt (grounding check)")
    return problems
