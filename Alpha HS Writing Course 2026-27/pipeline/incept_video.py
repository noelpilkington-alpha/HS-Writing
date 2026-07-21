"""
incept_video.py  -  the POST-LOCK video-stage MACHINERY (Incept "video" voiceover -> local assets).

WHAT THIS IS (and is NOT):
  * Incept can generate a short instructional voiceover video (generation_type="video",
    options={"kind":"voiceover","mode":"content_only"}). The proven probe (artifact 10885) is the
    shape this module targets: an output_json.script list of narration segments + an output_file_url
    (mp4) + a files[] list of scene PNGs + a captions track.
  * This module BUILDS + TESTS that machinery ONLY. It does NOT generate or bind any video. Per the
    plan (Noel), video runs AFTER the next full content build (video is post-content-lock by design):
    the live path here is exercised only in Task 7. See docs/superpowers/specs/video-stage-README.md
    for the run order.

DRY-BY-DEFAULT:
  generate_video(lesson_id, live=False) makes NO network call: it returns the would-send body from
  InceptClient.generate. fetch_video(...) in dry mode reads the client cache / returns cached local
  paths and never touches the network. Only live=True spends quota (Task 7).

SECRET HYGIENE (hard requirement):
  The S3 urls in output_file_url and files[].url are LIVE PRESIGNED SECRETS. They are downloaded to a
  LOCAL dir only (live mode, Task 7) and NEVER written into any committed file, receipt, or note.
  bind_note() records HOW a video would bind + a delivery caveat; it stores no url.

ADVISORY / NON-RAISING:
  reconcile_questions + generate_video degrade gracefully. Nothing here raises to fail a build.

Stdlib only (os, json, re, glob) + the sibling InceptClient for transport.
"""
from __future__ import annotations

import glob
import importlib.util
import json
import os
import re

from incept_client import InceptClient

HERE = os.path.dirname(os.path.abspath(__file__))

# the proven probe options shape (artifact 10885): a content-only voiceover video.
_VIDEO_OPTIONS = {"kind": "voiceover", "mode": "content_only"}

# DELIVERY (resolved 2026-07-21 by the Incept team's instruction): the generated video is uploaded to
# the Incept video bucket (upload.inceptstore.com -> a permanent public_url) and referenced as its OWN
# OneRoster component-resource (type=video, metadata.url=public_url) on the lesson's leaf topic. It is
# NOT embedded in lesson.html and NOT wrapped in QTI. This sidesteps the player <video> sanitizer and
# CORS questions entirely: the video is a separate activity, not inline content.
DELIVERY_CAVEAT = (
    "Delivery: the video is hosted on the Incept bucket (upload.inceptstore.com) and referenced as its "
    "own OneRoster component-resource (type=video, metadata.url=public_url) on the lesson's leaf topic. "
    "Not embedded in lesson.html, not QTI."
)

# VIDEO_TARGETS: a CURATED seed list of (short_lesson_id, slot_idx) tuples = the LS-flagged
# foundational lessons that should get a video FIRST. This is a curated seed, NOT every lesson.
# C901-0001 (G9 L01: fact -> arguable claim) is the required first target.
VIDEO_TARGETS: list[tuple[str, int]] = [
    ("C901-0001", 1),    # G9 L01: take a side, give a reason (the foundational claim lesson)
    ("C1001-0001", 1),   # G10 L01: source-reading foundation
    ("C1101-0001", 1),   # G11 L01: rhetorical/analysis foundation
]

# short-id course-code prefix -> grade slug. A short id looks like "C901-0001" / "C1001-0001" /
# "C1101-0001" / "C1201-0006"; the leading digits after "C" carry the grade (9xx=g9, 10xx=g10, ...).
_GRADE_PREFIX = {"g9": "C9", "g10": "C10", "g11": "C11", "g12": "C12"}


def _short_id_grade(short_id: str) -> str:
    """Infer the grade slug ('g9'..'g12') from a lesson id. '' if unknown.

    Handles BOTH the full id (e.g. 'ACC-W910-L-G9-C901-0001', 'ACC-W1112-L-G11-C1102-0014') where the
    grade is explicit as '-G<n>-', AND the bare short id ('C901-0001' -> the C-code prefix encodes it:
    C9=g9, C10=g10, C11=g11, C12=g12)."""
    sid = short_id or ""
    # 1) full id carries the grade explicitly as -G<n>-
    m = re.search(r"-G(9|10|11|12)-", sid)
    if m:
        return "g" + m.group(1)
    # 2) bare short id: the C-code prefix (C9.. / C10.. / C11.. / C12..)
    m = re.match(r"C(12|11|10|9)\d*-", sid)
    if m:
        return "g" + m.group(1)
    return ""


def video_targets(grade: str) -> list[tuple[str, int]]:
    """Return the curated VIDEO_TARGETS subset for `grade` (e.g. 'g9').

    Matches by the short-id course-code prefix (g9 ids start 'C9', g10 'C10', g11 'C11', g12 'C12').
    For 'g9' this MUST include ('C901-0001', 1)."""
    g = (grade or "").strip().lower()
    return [t for t in VIDEO_TARGETS if _short_id_grade(t[0]) == g]


# ---- lesson loading (mirror incept_qc._find_lesson) ------------------------
def _find_lesson(lesson_id: str):
    """Locate a Lesson by id across the four grade banks; return the Lesson or None.

    Mirrors incept_qc._find_lesson: globs Lesson_Bank_{G9..G12}/lesson_*.py, imports each, and returns
    the first Lesson whose .id matches. Accepts either the full id (ACC-W910-L-G9-C901-0001) or the
    short canonical id (C901-0001) -- the short id matches as a suffix of the full id. Import kept local
    so this module imports cleanly and never raises on a bad bank file."""
    root = os.path.dirname(HERE)
    for grade in ("G9", "G10", "G11", "G12"):
        pat = os.path.join(root, f"Lesson_Bank_{grade}", f"lesson_{grade.lower()}_l[0-9]*.py")
        for f in sorted(glob.glob(pat)):
            if "_deprecated" in f:
                continue
            try:
                spec = importlib.util.spec_from_file_location("ivid_" + os.path.basename(f)[:-3], f)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
            except SystemExit:
                mod = None
            except Exception:
                continue
            if not mod:
                continue
            candidates = list(getattr(mod, "LESSONS", []) or [])
            single = getattr(mod, "LESSON", None)
            if single is not None:
                candidates.append(single)
            for L in candidates:
                lid = getattr(L, "id", None)
                if lid == lesson_id or (lid and lid.endswith(lesson_id)):
                    return L
    return None


def _teach_text(lesson) -> str:
    """Concatenate the teach/model card text of a lesson into a plain-text prompt basis.

    Pulls the body of TEACH/MODEL teach_card + annotated_before_after slots, strips HTML tags, and
    joins them. Returns '' if the lesson is None or carries no teach text."""
    if lesson is None:
        return ""
    parts = []
    for s in getattr(lesson, "slots", []) or []:
        role = getattr(s, "role", "")
        kind = getattr(s, "kind", "")
        if role in ("TEACH", "MODEL") and kind in ("teach_card", "annotated_before_after"):
            body = getattr(s, "body", "") or ""
            if body:
                parts.append(body)
    text = " ".join(parts)
    text = re.sub(r"<[^>]+>", " ", text)      # strip HTML tags
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ---- generate (dry-by-default) ---------------------------------------------
def generate_video(lesson_id: str, live: bool = False, client: InceptClient | None = None,
                   grade_levels=None, subject: str = "writing") -> dict:
    """POST a "video" (voiceover, content_only) generate whose prompt derives from the LOCKED lesson's
    teach text.

    DRY (live=False): returns the client would-send stub {"status":"dry","would_send":<body>,
    "request_id":None} -- no network. LIVE (live=True): the client POSTs it (Task 7 only).

    If the lesson cannot be found, this STILL returns a dry body using the lesson_id as a stub prompt;
    it never raises."""
    lesson = _find_lesson(lesson_id)
    teach = _teach_text(lesson)
    # No-em-dash rule (same hard rule as diagrams): the narration + captions are student-facing, and
    # Incept output carries em dashes by default. Append it to every prompt.
    _NO_DASH = (" Use NO em dashes or en dashes anywhere in the narration or captions; use commas, "
                "colons, or parentheses instead.")
    if teach:
        title = getattr(lesson, "title", "") or lesson_id
        prompt = (f"A short instructional voiceover video for the lesson '{title}'. Teach the SAME "
                  f"content the lesson teaches, using this teach text as the source of truth:\n{teach}"
                  + _NO_DASH)
        if grade_levels is None:
            grade = _short_id_grade(getattr(lesson, "id", "") or lesson_id) or _short_id_grade(lesson_id)
            grade_levels = [grade] if grade else None
    else:
        # lesson not found (or no teach text): a safe stub prompt keyed on the id. Never raise.
        prompt = f"A short instructional voiceover video for lesson {lesson_id}." + _NO_DASH
        if grade_levels is None:
            grade = _short_id_grade(lesson_id)
            grade_levels = [grade] if grade else None

    if client is None:
        client = InceptClient()
    return client.generate(prompt, "video", options=dict(_VIDEO_OPTIONS),
                           grade_levels=grade_levels, subject=subject, live=live)


# ---- fetch (download to a local hosted dir) --------------------------------
def _script_segments(video_json: dict) -> list:
    """Return the output_json.script list of segments (or [] if absent). Handles the probe shape."""
    if not isinstance(video_json, dict):
        return []
    oj = video_json.get("output_json")
    if isinstance(oj, dict) and isinstance(oj.get("script"), list):
        return oj["script"]
    if isinstance(video_json.get("script"), list):
        return video_json["script"]
    return []


def _fmt_ts(seconds: float) -> str:
    """Format seconds as a WebVTT timestamp (HH:MM:SS.mmm)."""
    seconds = max(0.0, float(seconds))
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def _script_to_vtt(segments: list) -> str:
    """Build a WebVTT captions string from script segments' narration + duration_seconds.

    Uses each segment's duration_seconds to lay cues end-to-end. This is derived from the artifact's
    own script text (no url, no secret). Returns 'WEBVTT\\n' with no cues if there is no narration."""
    lines = ["WEBVTT", ""]
    t = 0.0
    for seg in segments or []:
        if not isinstance(seg, dict):
            continue
        narration = str(seg.get("narration", "") or "").strip()
        try:
            dur = float(seg.get("duration_seconds", 0) or 0)
        except (TypeError, ValueError):
            dur = 0.0
        if not narration:
            t += dur
            continue
        start, end = t, t + (dur if dur > 0 else 4.0)
        lines.append(f"{_fmt_ts(start)} --> {_fmt_ts(end)}")
        lines.append(narration)
        lines.append("")
        t = end
    return "\n".join(lines).rstrip() + "\n"


def _write_bytes(dest_dir: str, name: str, data) -> str:
    """Write bytes/text to dest_dir/name; return the LOCAL relative path (basename)."""
    os.makedirs(dest_dir, exist_ok=True)
    safe = os.path.basename(name)
    path = os.path.join(dest_dir, safe)
    if isinstance(data, (bytes, bytearray)):
        with open(path, "wb") as fh:
            fh.write(data)
    else:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(data)
    return safe


def fetch_video(artifact_id, dest: str, live: bool = False,
                client: InceptClient | None = None) -> dict:
    """Pull a video artifact's assets into `dest`; return LOCAL relative paths.

    Returns {"mp4": <rel path or None>, "captions": <rel path or None>, "scenes": [<rel paths>]}.

    LIVE (live=True): read the artifact JSON (client.artifact), download the mp4 from output_file_url +
    each scene PNG from files[].url into `dest`, and write captions.vtt from output_json.script
    narration. This path is exercised live only in Task 7. (No presigned url is ever persisted here;
    only the downloaded bytes land on local disk.)
    DRY (live=False): if the local files are already present in dest, return their relative paths
    without any network; otherwise read the artifact from the client cache (raises a clear cache-miss
    inside the client if absent). Never writes a secret."""
    if client is None:
        client = InceptClient()

    base = f"artifact_{artifact_id}"
    out = {"mp4": None, "captions": None, "scenes": []}

    # Dry short-circuit: if the local assets are already on disk, just return them (no cache read).
    if not live:
        mp4 = os.path.join(dest, base + ".mp4")
        vtt = os.path.join(dest, base + ".vtt")
        if os.path.exists(mp4):
            out["mp4"] = os.path.basename(mp4)
        if os.path.exists(vtt):
            out["captions"] = os.path.basename(vtt)
        for png in sorted(glob.glob(os.path.join(dest, base + "_*.png"))):
            out["scenes"].append(os.path.basename(png))
        if out["mp4"] or out["captions"] or out["scenes"]:
            return out

    # Read the artifact JSON (live: fetch + write-through cache; dry: read cache, raises on miss).
    art = client.artifact(artifact_id, live=live)
    if not isinstance(art, dict):
        return out

    # captions.vtt is built from the script narration (text we already hold) -- no url involved.
    segments = _script_segments(art)
    if segments:
        out["captions"] = _write_bytes(dest, base + ".vtt", _script_to_vtt(segments))

    # In live mode a downloader would GET output_file_url + each files[].url and write the BYTES.
    # Only actual downloaded bytes are written locally; the presigned urls are never persisted.
    if live:
        mp4_url = art.get("output_file_url")
        if isinstance(mp4_url, str) and mp4_url.startswith("http"):
            data = _download(mp4_url, client)
            if data is not None:
                out["mp4"] = _write_bytes(dest, base + ".mp4", data)
        for f in art.get("files", []) or []:
            if not isinstance(f, dict):
                continue
            fname = str(f.get("filename", "") or "")
            furl = f.get("url")
            if fname.lower().endswith(".png") and isinstance(furl, str) and furl.startswith("http"):
                data = _download(furl, client)
                if data is not None:
                    out["scenes"].append(_write_bytes(dest, base + "_" + os.path.basename(fname), data))
    return out


def _download(url: str, client: InceptClient):
    """Download raw bytes from a presigned url (live only). Returns bytes or None on failure.

    Uses curl via subprocess (stdlib) so no extra dependency is added. The url is a live presigned
    SECRET: it is passed to curl at call time only, never logged or persisted. Exercised live in Task 7."""
    import subprocess
    try:
        proc = subprocess.run(
            ["curl", "-s", "--ssl-no-revoke", "--max-time", "120", "-L", url],
            capture_output=True, timeout=180,
        )
    except Exception:
        return None
    if proc.returncode != 0 or not proc.stdout:
        return None
    return proc.stdout


# ---- reconcile embedded video questions against the lesson's discriminations ----
def _norm(text: str) -> str:
    """Normalize a stem for comparison: strip tags, lowercase, drop non-alphanumerics, collapse space."""
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = re.sub(r"[^a-z0-9 ]+", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def _video_questions(video_json) -> list:
    """Extract the embedded questions list from a video artifact, or [] if none.

    Handles BOTH shapes: top-level video_json['questions'] AND video_json['output_json']['questions'].
    NOTE: a content_only voiceover (the proven probe) carries NO 'questions' key -> returns []."""
    if not isinstance(video_json, dict):
        return []
    qs = video_json.get("questions")
    if isinstance(qs, list):
        return qs
    oj = video_json.get("output_json")
    if isinstance(oj, dict) and isinstance(oj.get("questions"), list):
        return oj["questions"]
    return []


def _q_stem(q) -> str:
    """Pull a comparable stem from a video question dict (stem / narration / prompt / text)."""
    if not isinstance(q, dict):
        return ""
    for k in ("stem", "narration", "prompt", "text", "question"):
        v = q.get(k)
        if isinstance(v, str) and v.strip():
            return v
    return ""


# Jaccard token-overlap at or above this fraction counts a video question as a duplicate of an
# existing discrimination stem. 0.6 = 60% shared tokens: tight enough not to flag every question,
# loose enough to catch near-restatements. The one tuning knob for reconcile_questions.
_DUP_OVERLAP_THRESHOLD = 0.6


def _token_overlap(a: str, b: str) -> float:
    """Jaccard token overlap of two normalized stems (0..1). '' vs anything -> 0."""
    sa, sb = set(a.split()), set(b.split())
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def reconcile_questions(video_json, lesson) -> list:
    """Flag embedded video questions that DUPLICATE one of the lesson's existing discrimination stems.

    This guards against the video's embedded checks duplicating our gated discriminations (the probe's
    Q1 approximately equalled our L01 slot-4). For each embedded question, its stem is compared against
    every discrimination slot's title/stem; a match (normalized-substring OR high token overlap >= 0.6)
    is FLAGGED.

    Returns a list of {"video_q_index", "duplicates_slot", "video_stem", "lesson_stem"}. A video with
    no questions returns []. NEVER raises (advisory machinery)."""
    try:
        questions = _video_questions(video_json)
        if not questions:
            return []
        # collect (slot_index, stem) for every discrimination-family slot in the lesson.
        disc = []
        for i, s in enumerate(getattr(lesson, "slots", []) or []):
            if getattr(s, "kind", "") in ("discrimination", "predict_the_fix", "self_score"):
                stem = getattr(s, "title", "") or getattr(s, "body", "") or ""
                disc.append((i, stem))
        flags = []
        for qi, q in enumerate(questions):
            vstem = _q_stem(q)
            nv = _norm(vstem)
            if not nv:
                continue
            for si, lstem in disc:
                nl = _norm(lstem)
                if not nl:
                    continue
                is_dup = (nv in nl or nl in nv or _token_overlap(nv, nl) >= _DUP_OVERLAP_THRESHOLD)
                if is_dup:
                    flags.append({
                        "video_q_index": qi,
                        "duplicates_slot": si,
                        "video_stem": vstem,
                        "lesson_stem": lstem,
                    })
                    break   # one flag per video question
        return flags
    except Exception:
        # advisory: degrade to no-flags rather than break a build.
        return []


# ---- bind note (a record of HOW a video binds) ----
def bind_note(lesson_id: str, artifact_id) -> dict:
    """Return a small note recording HOW a video binds + the delivery caveat.

    Delivery (resolved): the video is a SEPARATE OneRoster component-resource (type=video) on the
    lesson's leaf topic, pointing at its hosted public_url. NOTE ONLY: no binding happens here."""
    return {
        "lesson_id": lesson_id,
        "artifact_id": artifact_id,
        "bind_as": "component_resource",
        "resource_type": "video",
        "delivery_caveat": DELIVERY_CAVEAT,
        "note_only": True,
    }


# ---- OneRoster resource plan (video component-resource, NOT QTI) ----
# Endpoints match g9_assemble_v3_1 (the working G9 push path).
_ONEROSTER = "https://api.alpha-1edtech.ai"
_RES_URL = f"{_ONEROSTER}/ims/oneroster/resources/v1p2/resources/"          # trailing slash REQUIRED
_COMPRES_URL = f"{_ONEROSTER}/ims/oneroster/rostering/v1p2/courses/component-resources"


def video_resource_plan(lesson_id: str, public_url: str, title: str = "", xp: int = 0,
                        topic_id: str = "", sort_order: int = 3) -> list:
    """Build the OneRoster (resource, component-resource) plan for a hosted lesson video.

    Mirrors the ARTICLE block in g9_assemble_v3_1 exactly, EXCEPT type=video + the inceptstore public_url.
    Returns a list of ("resource"|"component-resource", sourcedId, endpoint_url, body) tuples (the same
    plan shape g9_assemble_v3_1.post() consumes), so the caller can dry-print or POST them.

    GOTCHAS (both verified live 2026-07-21):
    - `lessonType` in RESOURCE metadata returns HTTP 500 (server bug), so it is omitted there.
    - `lessonType` on the LINK is an ENUM that has NO video value (server accepts only powerpath-100 /
      map-adaptive / quiz / test-out / placement / unit-test / alpha-read-article). A video is none of
      these, so lessonType is OMITTED from the link too. The `type: "video"` on the resource metadata is
      what marks it a video; the link carries just {xp} (exactly like the working Article CR).

    topic_id = the leaf topic (courseComponent) the video attaches to; sort_order defaults to 3 so the
    video sits AFTER the article (1) and mastery (2) on a lesson's topic (adjust per placement)."""
    title = (title or lesson_id)[:200]
    vid_rid = f"res-{lesson_id}-video"
    cr_id = f"cr-{lesson_id}-video"
    plan = [
        ("resource", vid_rid, _RES_URL, {"resource": {
            "sourcedId": vid_rid, "status": "active", "title": title,
            "importance": "primary", "vendorResourceId": f"{lesson_id}-video", "vendorId": "alpha-incept",
            "applicationId": "incept",
            # type=video marks the resource; NO lessonType (500 bug); url = the hosted public_url.
            "metadata": {"type": "video", "activityType": "Video", "format": "mp4", "language": "en-US",
                         "xp": xp, "url": public_url}}}),
        ("component-resource", cr_id, _COMPRES_URL, {"componentResource": {
            "sourcedId": cr_id, "status": "active", "title": title,
            "sortOrder": sort_order, "resource": {"sourcedId": vid_rid},
            "courseComponent": {"sourcedId": topic_id},
            # no lessonType: it is an enum with no video value; match the working Article CR ({xp} only).
            "metadata": {"xp": xp}}}),
    ]
    return plan


if __name__ == "__main__":
    print("VIDEO_TARGETS:", VIDEO_TARGETS)
    print("g9 targets:", video_targets("g9"))
    print(json.dumps(generate_video("C901-0001", live=False), indent=2)[:600])
