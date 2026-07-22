"""
video_timing.py  -  derive PAUSE-POINT CUE TIMES for an interactive video's embedded questions.

WHY THIS EXISTS:
  Incept's interactive-video artifact (mode=interactive) gives us output_json with a `script` (segments,
  each with duration_seconds) + a flat `questions[]` list, but NO timestamps binding a question to a pause
  point. The Timeback player's pause->question->resume behavior needs a cue time per question. This module
  derives those cue times from the script, so the moment the delivery contract is known (PCI vs first-party
  player config) our side already produces the (question, cue_seconds) map it will consume.

DERIVATION (grounded in the proven probe, artifact 10892: 7 segments, roles start/model/try_it/recap, 3 Qs):
  A question should fire at a NATURAL CHECK MOMENT, i.e. at the END of a segment where the video has just
  prompted the learner (a `try_it` "your turn" beat, or the closing `recap`). So:
    1. Compute each segment's cumulative END time from duration_seconds.
    2. Identify CHECK-ROLE segments (role in CHECK_ROLES = try_it / recap / check / practice) as candidate
       pause points, in order.
    3. Assign questions to those candidate boundaries in order (q0 -> first check boundary, q1 -> second...).
    4. FALLBACK: if there are more questions than check-role boundaries (or no durations), distribute the
       remaining/all questions EVENLY across the total runtime (never at t=0 and never past the end).
  The cue is placed at the segment END (pause AFTER the beat plays), which is what "video pauses, question
  pops up, then resumes" describes.

Pure stdlib. Advisory/derivational: never raises (returns [] on an unusable artifact). No em dashes.
"""
from __future__ import annotations

# Segment roles that are a natural moment to pause and check (retrieval right after a prompt/summary).
CHECK_ROLES = ("try_it", "recap", "check", "practice", "your_turn")


def _script(video_json) -> list:
    """The output_json.script list (or a top-level script), else []. Never raises."""
    if not isinstance(video_json, dict):
        return []
    oj = video_json.get("output_json")
    if isinstance(oj, dict) and isinstance(oj.get("script"), list):
        return oj["script"]
    if isinstance(video_json.get("script"), list):
        return video_json["script"]
    return []


def _segment_ends(script: list) -> list:
    """Cumulative END time (seconds) for each segment, from duration_seconds. Missing/zero durations
    contribute 0 (so a script with no durations yields all-equal ends and triggers the even fallback)."""
    ends, cum = [], 0.0
    for s in script:
        try:
            d = float(s.get("duration_seconds") or 0)
        except (TypeError, ValueError):
            d = 0.0
        cum += max(0.0, d)
        ends.append(round(cum, 3))
    return ends


def _even_cues(n: int, total: float) -> list:
    """n cue times evenly spaced across (0, total), excluding 0 and total. If total<=0, returns []."""
    if n <= 0 or total <= 0:
        return []
    step = total / (n + 1)
    return [round(step * (i + 1), 3) for i in range(n)]


def cue_points(video_json, questions=None) -> list:
    """Return a list of {"question_index": i, "cue_seconds": t, "basis": "check-role"|"even"} pairing each
    embedded question to the pause time (segment END) where it should fire.

    Prefers check-role segment ends (try_it / recap / ...) in order; falls back to even distribution for any
    questions beyond the available check boundaries (or when the script carries no usable durations).
    Returns [] if there are no questions. NEVER raises."""
    try:
        script = _script(video_json)
        qs = questions if questions is not None else _questions(video_json)
        nq = len(qs) if qs else 0
        if nq == 0:
            return []
        ends = _segment_ends(script)
        total = ends[-1] if ends else 0.0
        # candidate check-role boundaries, in playback order
        check_ends = [ends[i] for i, s in enumerate(script)
                      if i < len(ends) and str((s or {}).get("role", "")).lower() in CHECK_ROLES]
        cues = []
        used = 0
        for i in range(nq):
            if used < len(check_ends):
                cues.append({"question_index": i, "cue_seconds": check_ends[used], "basis": "check-role"})
                used += 1
            else:
                cues.append({"question_index": i, "cue_seconds": None, "basis": "even"})
        # fill any "even" cues by spreading the leftover questions across the runtime (after the last
        # check boundary, up to total), so they do not collide with the assigned check-role cues.
        leftover = [c for c in cues if c["cue_seconds"] is None]
        if leftover:
            start = check_ends[-1] if check_ends else 0.0
            span = max(0.0, total - start)
            if span > 0:
                # spread the leftovers across the runtime AFTER the last check boundary (never clobber the
                # already-assigned check-role cues).
                extra = _even_cues(len(leftover), span)
                for c, e in zip(leftover, extra):
                    c["cue_seconds"] = round(start + e, 3)
            elif total > 0:
                # no runtime after the last check boundary (e.g. recap is the final segment): the leftover
                # questions fire at the video END. Keep the check-role cues intact.
                for c in leftover:
                    c["cue_seconds"] = total
            else:
                # no usable durations at all: index-order cues as a last resort. ONLY the leftovers.
                for c in leftover:
                    c["cue_seconds"] = float(c["question_index"] + 1)
        return cues
    except Exception:
        return []


def _questions(video_json) -> list:
    """Local copy of the embedded-questions extractor (kept import-light). Handles both shapes."""
    if not isinstance(video_json, dict):
        return []
    qs = video_json.get("questions")
    if isinstance(qs, list):
        return qs
    oj = video_json.get("output_json")
    if isinstance(oj, dict) and isinstance(oj.get("questions"), list):
        return oj["questions"]
    return []


def one_beat_cue(video_json, min_start: float = 0.0) -> dict:
    """Derive the SINGLE default cue time for a One-Beat Check (council rule 2026-07-22): the FIRST check-role
    (try_it / recap / ...) segment END at or after `min_start`, which is the video's first natural "your turn"
    beat. This NARROWS the general timing map (one cue, not one-per-check-role).

    `min_start` lets a caller require the cue to fall after the first on-screen positive instance of the target
    move (never test ahead of instruction). If no check-role boundary qualifies, fall back to the video
    midpoint (still after min_start when possible). Returns {"cue_seconds": t, "duration_seconds": total}.
    NEVER raises."""
    try:
        script = _script(video_json)
        ends = _segment_ends(script)
        total = ends[-1] if ends else 0.0
        check_ends = [ends[i] for i, s in enumerate(script)
                      if i < len(ends) and str((s or {}).get("role", "")).lower() in CHECK_ROLES]
        # first check-role boundary at/after min_start (and strictly before the end, so the video still resumes)
        cue = next((e for e in check_ends if e >= min_start and e < total), None)
        if cue is None:
            cue = next((e for e in check_ends if e < total), None)  # any check boundary before the end
        if cue is None and total > 0:
            mid = round(total / 2.0, 3)
            cue = mid if mid >= min_start else min(min_start, total)  # midpoint fallback
        return {"cue_seconds": cue, "duration_seconds": total}
    except Exception:
        return {"cue_seconds": None, "duration_seconds": 0.0}


def timing_map(video_json) -> dict:
    """Full derived timing map for one interactive video: the questions paired with their cue times.

    Returns {"total_seconds": t, "cues": [{question_index, cue_seconds, basis, stem}], "n_questions": n}.
    stem is copied through for readability/review. This is the artifact the delivery layer (PCI or the
    first-party player) will consume once its exact contract is known. NEVER raises."""
    try:
        qs = _questions(video_json)
        script = _script(video_json)
        ends = _segment_ends(script)
        cues = cue_points(video_json, qs)
        for c in cues:
            i = c["question_index"]
            q = qs[i] if 0 <= i < len(qs) else {}
            c["stem"] = (q.get("stem") or q.get("prompt") or q.get("text") or "") if isinstance(q, dict) else ""
        return {"total_seconds": ends[-1] if ends else 0.0, "n_questions": len(qs), "cues": cues}
    except Exception:
        return {"total_seconds": 0.0, "n_questions": 0, "cues": []}
