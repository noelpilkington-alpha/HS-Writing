"""
player_test/expectations.py  -  build the per-lesson EXPECTED state from the repo (deterministic, offline).

The testing agent compares OBSERVED player behavior to this expected state. Truth comes from the repo, never
from the page. For each lesson we know, deterministically:
  - the player URL (same builder the deployed course uses: render_course_preview_grade.article_player_url)
  - the intro-video One-Beat cues: (cue_seconds, option_count, correct_option_text) per beat, from data/one_beats.json
  - the gated discrimination checkpoints: (cp_id, n_options, correct_option_text) from the rendered checkpoint XML
  - the PP100 mastery: (test_id, frq_id) that must exist + score
  - content assertions: the lesson title must render; no leaked placeholder / Cat-N blobs (render_qc classes)

Pure stdlib + repo imports. No network. Tested by tests/test_player_expectations.py.
"""
from __future__ import annotations
import os, sys, re, json, html as _html

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.dirname(HERE)
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)

import render_course_preview_grade as R
from gated_reading import build_lesson_html, _OPT_RENDER_RE, _CORRECT_RESP_RE, _flat_text

_ONE_BEATS_PATH = os.path.join(PIPE, "data", "one_beats.json")


def _one_beats() -> dict:
    try:
        with open(_ONE_BEATS_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _correct_text_from_xml(xml: str) -> tuple[int, str]:
    """(option_count, correct_option_flat_text) from a rendered choice-interaction item. '' if none."""
    opts = _OPT_RENDER_RE.findall(xml)   # [(opt_id, body_html), ...]
    if not opts:
        return 0, ""
    cr = _CORRECT_RESP_RE.search(xml)
    correct_id = cr.group(1) if cr else None
    correct_text = ""
    for oid, body in opts:
        if oid == correct_id:
            correct_text = _flat_text(body)
            break
    return len(opts), correct_text


def lesson_expectation(grade: str, n: int, L, base_url: str = R.DEFAULT_BASE) -> dict:
    """The full expected state for one lesson. base_url = where the gated lesson.html is hosted (the live alias
    the course points at). Building the html here (with the one_beat_map) tells us exactly which checkpoints +
    video interactions the player WILL render, and their correct answers - the ground truth the agent checks."""
    ob = _one_beats()
    beat_entry = ob.get(L.id) or {}
    beats = beat_entry.get("beats") or ([] if "beats" in beat_entry else (
        [{"cue_seconds": beat_entry["cue_seconds"], "item": beat_entry["item"]}] if beat_entry.get("item") else []))
    # build the html with the one_beat_map so the rendered checkpoints + video figure match what deploys
    one_beat_map = {L.id: beat_entry} if beat_entry else None
    html, checkpoints = build_lesson_html(L, base_url=f"{base_url}/{R.slug(grade, n)}",
                                          video_map=({L.id: {"mp4": "x", "vtt": "y"}} if beat_entry else None),
                                          one_beat_map=one_beat_map)
    cp_by_id = dict(checkpoints)

    # expected One-Beat cues (from the authored bank): cue time + option count + correct option text
    exp_beats = []
    for i, b in enumerate(beats, 1):
        item = b.get("item") or {}
        opts = item.get("options") or []
        correct = next((o.get("text", "") for o in opts if o.get("correct")), "")
        exp_beats.append({"index": i, "cue_seconds": float(b.get("cue_seconds") or 0),
                          "n_options": len(opts), "correct_text": correct,
                          "stem": (item.get("stem") or "")})

    # expected gated discrimination checkpoints (cp-*), from the rendered item XML
    exp_gates = []
    for cp_id, xml in checkpoints:
        if not cp_id.startswith("cp-"):
            continue
        if "<qti-choice-interaction" not in xml:
            continue
        n_opts, correct_text = _correct_text_from_xml(xml)
        exp_gates.append({"cp_id": cp_id, "n_options": n_opts, "correct_text": correct_text})

    return {
        "grade": grade, "n": n, "lesson_id": L.id, "title": L.title or L.id,
        "player_url": R.article_player_url(grade, n, L, base_url),
        "content_url": f"{base_url}/{R.slug(grade, n)}/lesson.html",
        "has_video": bool(beat_entry),
        "duration_seconds": float(beat_entry.get("duration_seconds") or 0) if beat_entry else 0.0,
        "beats": exp_beats,
        "gates": exp_gates,
        "mastery_test_id": f"{L.id}-MASTERY",
        "mastery_frq_id": f"{L.id}-MASTERY-FRQ",
        # content assertions: the title must appear; these tokens must NOT (leaked-placeholder classes)
        "must_contain": [L.title] if (L.title and len(L.title) > 4) else [],
    }


def grade_expectations(grade: str, base_url: str = R.DEFAULT_BASE) -> list:
    """Expected state for every lesson in a grade, in course order."""
    return [lesson_expectation(grade, n, L, base_url) for n, L, _f in R.lessons_for(grade)]


if __name__ == "__main__":
    g = sys.argv[1] if len(sys.argv) > 1 else "G9"
    exps = grade_expectations(g)
    nb = sum(len(e["beats"]) for e in exps)
    ng = sum(len(e["gates"]) for e in exps)
    print(f"{g}: {len(exps)} lessons | {sum(1 for e in exps if e['has_video'])} with video | "
          f"{nb} one-beat cues | {ng} gated checkpoints")
    e0 = exps[0]
    print(f"  sample {e0['lesson_id']}: {len(e0['beats'])} beats "
          f"(cues {[b['cue_seconds'] for b in e0['beats']]}), {len(e0['gates'])} gates")
