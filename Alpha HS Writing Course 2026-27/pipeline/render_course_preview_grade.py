"""
render_course_preview_grade.py  -  generalized (G10/G11/G12) Vercel review preview.

Mirrors render_course_preview.py (which is G9-hardcoded) for the other grades, driving everything off the
SAME engines the real push uses, so the preview matches what would ship to Timeback:
  - the grade's Lesson_Bank_G{N} v3.1 lessons (in course order)         -> the course tree + article links
  - gated_reading.build_lesson_html(L, base_url)                        -> each lesson's gated ARTICLE (lesson.html + items/*.xml)
  - mastery_targets_grade.mastery_prompt_html(L, authored_entry)        -> the exact PP100 mastery prompt HTML per lesson

Namespaced UNDER a per-grade subfolder ("g10/l01/lesson.html", "course-g10/index.html", ...) so it never touches
the live G9 files at the deploy root. Each article's base_url points at ITS OWN subfolder so the player resolves
tb-qti-config item hrefs against our host (relative hrefs 404 against the player origin).

RENDER-QC is a HARD GATE: build_lesson_html output is checked and the run aborts (exit 2) if any lesson has a
render defect, so the preview can never ship a broken article.

Run: python pipeline/render_course_preview_grade.py G10 [--deploy DIR] [--base-url URL]
"""
from __future__ import annotations
import os, sys, re, glob, html, json, argparse, urllib.parse

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
from g9_push_dryrun import _load, STIM
from gated_reading import build_lesson_html, render_qc
from mastery_targets_grade import _GRADE_GLOB, _authored, mastery_prompt_html, in_lesson_writes

DEFAULT_DEPLOY = "c:/Users/noelp/AppData/Local/Temp/vercel_deploy"
DEFAULT_BASE = "https://verceldeploy-five-tan.vercel.app"
LEARNWITH = "https://content.platform.learnwith.ai/player"


def lessons_for(grade):
    """[(n, L, file)] for a grade, in lesson-number order (v3.1 lessons only)."""
    subdir, pat = _GRADE_GLOB[grade]
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, subdir, pat))):
        if "_deprecated" in f:
            continue
        m = _load(f)
        L = getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0]
        if not L:
            continue
        n = int(re.search(r"_l(\d+)", os.path.basename(f)).group(1))
        out.append((n, L, f))
    out.sort(key=lambda t: t[0])
    return out


def slug(grade, n):
    return f"{grade.lower()}/l{n:02d}"


def article_player_url(grade, n, L, base_url):
    content = f"{base_url}/{slug(grade, n)}/lesson.html"
    q = urllib.parse.urlencode({"contentUrl": content, "contentId": L.id, "theme": "indigo", "ttsEnabled": "true"})
    return f"{LEARNWITH}?{q}"


_PAGE = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
<style>body{{margin:0;font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;background:#eef1f6;color:#1f2a44}}
.wrap{{max-width:860px;margin:0 auto;padding:24px 18px}}h1{{font-size:22px}}.crumb{{font-size:13px;color:#556}}
.card{{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:18px 20px;margin:14px 0}}
.tag{{display:inline-block;font-size:11px;font-weight:700;color:#0f766e;background:#ecfdf5;border-radius:4px;padding:2px 8px}}
a{{color:#1d4ed8}}</style></head><body><div class="wrap">{body}</div></body></html>"""


def render_mastery_page(grade, lesson_title, prompt_html, writes):
    """One review page per lesson: the held-out PP100 mastery prompt PLUS every scored in-lesson writing task
    (SUPPORTED / diagnosis / INDEPENDENT / TRANSFER), each rendered exactly as the student sees it."""
    parts = [f'<div class="crumb"><a href="index.html">&larr; Full {grade} course</a></div>',
             f'<h1>{html.escape(lesson_title)}</h1>']
    if prompt_html and prompt_html.strip():
        parts.append('<div class="tag">POWERPATH-100 held-out mastery &middot; graded by the external writing '
                     'grader (test-out &ge; 90)</div>')
        parts.append(f'<div class="card"><h2 style="margin:0 0 8px;font-size:15px;color:#0f766e">'
                     f'PP100 mastery task (held-out source)</h2>{prompt_html}</div>')
    if writes:
        parts.append(f'<div class="crumb" style="margin-top:18px">The {len(writes)} scored writing tasks inside '
                     'the lesson (in order), each shown exactly as the student sees it:</div>')
        for i, (label, wtitle, whtml) in enumerate(writes, 1):
            parts.append(f'<div class="card"><h2 style="margin:0 0 8px;font-size:15px;color:#b45309">'
                         f'{i}. {html.escape(wtitle)} <span style="font-weight:600;color:#94741f;font-size:12px">'
                         f'&middot; {html.escape(label)}</span></h2>{whtml}</div>')
    return _PAGE.format(title=f"Prompts: {html.escape(lesson_title)}", body="\n".join(parts))


def _unit_full(L):
    return re.sub(r"\s+", " ", getattr(L, "unit", "") or "Unit").strip()


def unit_key(L):
    """Group key = the real unit token (e.g. 'G9 U1'), NOT the full unit string. Lessons carry a
    per-lesson parenthetical sub-topic in .unit ('... (arguable claim)'); keying on the whole string
    made two lessons with the SAME sub-topic (L01 + L04, both 'arguable claim') collapse into one card
    out of sequence, and inflated the unit count. Key on 'G<grade> U<n>' so a unit's lessons stay together
    in course order; fall back to the full string if no U-token is present."""
    full = _unit_full(L)
    m = re.match(r"(G\d+\s+U\d+)", full)
    return m.group(1) if m else full


def unit_title(L):
    """Card heading: the unit's base label (the full unit string minus the trailing parenthetical
    sub-topic). Stable per unit; the first lesson in each unit supplies the heading."""
    full = _unit_full(L)
    return re.sub(r"\s*\([^)]*\)\s*$", "", full).strip() or full


def main():
    ap = argparse.ArgumentParser()
    # G9 uses the same static-article renderer as G10-12 (its nav lives in render_course_preview.py, but for
    # a fixes-current review we also want G9's gated ARTICLES rendered locally, not linked to the hosted -
    # pre-fix - player). _GRADE_GLOB + slug already handle G9 (g9/l01).
    ap.add_argument("grade", choices=["G9", "G10", "G11", "G12"])
    ap.add_argument("--deploy", default=DEFAULT_DEPLOY)
    ap.add_argument("--base-url", default=DEFAULT_BASE)
    args = ap.parse_args()
    grade = args.grade
    base_url = args.base_url.rstrip("/")

    lessons = lessons_for(grade)
    authored = _authored(grade)

    # PREVIEW-SCOPED video map: if a hosted-video manifest exists for this grade, pass it to
    # build_lesson_html so the preview embeds the intro video + compresses the opening teach (council rule).
    # This is preview-only: the production push passes no video_map, so it is unaffected. Manifest shape:
    # {lesson_id -> {"mp4":url, "vtt":url}} at C:/tmp/incept_videos/<grade>_videos.json.
    video_map = {}
    _vm_path = os.path.join("C:/tmp/incept_videos", f"{grade.lower()}_videos.json")
    if os.path.exists(_vm_path):
        try:
            video_map = json.load(open(_vm_path, encoding="utf-8"))
            print(f"video_map: {len(video_map)} {grade} lessons carry an intro video (preview embed + compress)")
        except Exception:
            video_map = {}

    # PREVIEW-SCOPED One-Beat map (rule 2026-07-22): every your-turn beat of a video gets one non-gating
    # in-video question, so a matching video renders as an INTERACTIVE tb-video. Preview-only: the production
    # push passes no one_beat_map, so it is unaffected.
    one_beat_map = {}
    try:
        from incept_one_beats import ALL_ONE_BEATS
        one_beat_map = {lid: b for lid, b in ALL_ONE_BEATS.items() if lid in video_map}
        if one_beat_map:
            _nbeats = sum(len(b.get("beats", [])) for b in one_beat_map.values())
            print(f"one_beat_map: {len(one_beat_map)} {grade} lesson(s), {_nbeats} in-video One-Beat checks")
    except Exception:
        one_beat_map = {}

    # 1) render each lesson's gated ARTICLE (lesson.html + items/*.xml) into its own subfolder
    qc_failures = []
    for n, L, _f in lessons:
        art_dir = os.path.join(args.deploy, slug(grade, n).replace("/", os.sep))
        items_dir = os.path.join(art_dir, "items")
        os.makedirs(items_dir, exist_ok=True)
        html_str, checkpoints = build_lesson_html(L, base_url=f"{base_url}/{slug(grade, n)}", video_map=video_map,
                                                   one_beat_map=one_beat_map)
        # pass the source lesson so render_qc also runs the OPTION-INTEGRITY choices[] cross-check (A6) - the
        # full Tier-A render gate, not the lighter artifact-only pass. Tier-A already proved all 100 pass it.
        problems = render_qc(html_str, checkpoints, lessons=L)
        if problems:
            qc_failures.append((L.id, problems))
            continue
        # clean stale item files for THIS lesson id, then write fresh
        for old in (glob.glob(os.path.join(items_dir, f"cp-{L.id}-*.xml")) +
                    glob.glob(os.path.join(items_dir, f"frq-{L.id}-*.xml")) +
                    glob.glob(os.path.join(items_dir, f"vq-{L.id}-*.xml"))):
            try:
                os.remove(old)
            except OSError:
                pass
        open(os.path.join(art_dir, "lesson.html"), "w", encoding="utf-8").write(html_str)
        for cp_id, xml in checkpoints:
            open(os.path.join(items_dir, f"{cp_id}.xml"), "w", encoding="utf-8").write(xml)

    if qc_failures:
        print(f"RENDER-QC FAILED for {grade} ({len(qc_failures)} lessons):", file=sys.stderr)
        for lid, probs in qc_failures:
            print(f"  {lid}:", file=sys.stderr)
            for p in probs:
                print("    - " + p, file=sys.stderr)
        return 2

    # 2) render the per-grade course index + mastery pages
    course_dir = os.path.join(args.deploy, f"course-{grade.lower()}")
    os.makedirs(course_dir, exist_ok=True)
    for f in glob.glob(os.path.join(course_dir, "*.html")):
        os.remove(f)

    # group by the real unit token (G9 U1, U2, ...), NOT the full parenthetical string, so a unit's
    # lessons stay together in course order and the unit count is correct. Heading = the unit's base label.
    rows_by_unit = {}
    heading = {}
    order = []
    for n, L, _f in lessons:
        k = unit_key(L)
        if k not in rows_by_unit:
            rows_by_unit[k] = []
            heading[k] = unit_title(L)
            order.append(k)
        rows_by_unit[k].append((n, L))

    body = [f'<h1>{grade} Writing Course &mdash; full preview (as it pushes to Timeback)</h1>',
            f'<div class="crumb">{len(lessons)} lessons across {len(order)} units. '
            'Each lesson = a gated-reading ARTICLE + its PP100 mastery task. Click a title to open the article '
            'in the live player; click Mastery to read the exact graded prompt.</div>']
    written_m = 0
    for u in order:
        body.append(f'<div class="card"><h2 style="margin:0 0 10px;font-size:17px">{html.escape(heading[u])}</h2>')
        for n, L in rows_by_unit[u]:
            art = article_player_url(grade, n, L, base_url)
            entry = authored.get(L.id, {})
            prompt_html = mastery_prompt_html(L, entry)
            writes = in_lesson_writes(L)
            if (prompt_html and prompt_html.strip()) or writes:
                open(os.path.join(course_dir, f"{L.id}-MASTERY.html"), "w", encoding="utf-8").write(
                    render_mastery_page(grade, L.title, prompt_html, writes))
                nlab = 1 if (prompt_html and prompt_html.strip()) else 0
                mlink = (f' &middot; <a href="{L.id}-MASTERY.html">all prompts '
                         f'({nlab + len(writes)})</a>')
                written_m += 1
            else:
                mlink = ' &middot; <span style="color:#999">(no prompts)</span>'
            body.append(f'<div style="padding:6px 0;border-top:1px solid #f1f5f9">'
                        f'<span class="crumb">L{n:02d}</span> '
                        f'<a href="{html.escape(art)}" target="_blank">{html.escape(L.title)}</a>{mlink}</div>')
        body.append('</div>')

    index_html = _PAGE.format(title=f"{grade} Writing Course - full preview", body="\n".join(body))
    open(os.path.join(course_dir, "index.html"), "w", encoding="utf-8").write(index_html)
    print(f"{grade} preview: {len(lessons)} articles -> {grade.lower()}/l*/, "
          f"index.html + {written_m} mastery pages -> {course_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
