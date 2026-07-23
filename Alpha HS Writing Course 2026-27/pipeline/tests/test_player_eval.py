"""
test_player_eval.py  -  the offline-testable pieces of the student-agent course evaluator (no browser, no net).

Covers: expectations built from the repo (cues/options/gates match one_beats + rendered checkpoints), the
report summarizer/markdown, and the content/video checks against a FAKE driver returning canned observations.
"""
from __future__ import annotations
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.dirname(HERE)
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)

from player_test.expectations import lesson_expectation, grade_expectations
from player_test import checks as C
from player_test.report import summarize, markdown
import render_course_preview_grade as R


def _g9_l01():
    for n, L, f in R.lessons_for("G9"):
        if L.id == "ACC-W910-L-G9-C901-0001":
            return n, L
    raise AssertionError("G9 L01 not found")


def test_expectation_l01_has_two_beats_four_options():
    n, L = _g9_l01()
    e = lesson_expectation("G9", n, L)
    assert e["has_video"] is True
    assert [b["cue_seconds"] for b in e["beats"]] == [82.0, 131.0]
    assert all(b["n_options"] == 4 for b in e["beats"]), "L01 beats are 4-option after the expansion"
    assert e["mastery_test_id"] == "ACC-W910-L-G9-C901-0001-MASTERY"
    assert e["mastery_frq_id"] == "ACC-W910-L-G9-C901-0001-MASTERY-FRQ"
    assert e["player_url"].startswith("https://content.platform.learnwith.ai/player?")


def test_expectation_gates_have_correct_text():
    n, L = _g9_l01()
    e = lesson_expectation("G9", n, L)
    assert len(e["gates"]) >= 2, "L01 has gated discrimination checkpoints"
    for gt in e["gates"]:
        assert gt["n_options"] >= 2
        assert gt["correct_text"], f"gate {gt['cp_id']} must carry a correct-option text"


def test_grade_expectations_counts():
    exps = grade_expectations("G9")
    assert len(exps) == 29
    assert sum(1 for e in exps if e["has_video"]) == 17
    assert sum(len(e["beats"]) for e in exps) == 36


class _FakeDriver:
    """Returns canned JS observations for the content/video checks (no browser)."""
    available = True
    def __init__(self, body="Take a Side Someone Could Argue With ... some lesson text", has_video=True, dur=169):
        self._body, self._has_video, self._dur = body, has_video, dur
    def body_text(self, limit=1200): return self._body[:limit]
    def js(self, expr, timeout=60):
        # video-state probe (check_one_beat_pauses / _js_video_state)
        if "has_video" in expr:
            return {"has_video": self._has_video, "paused": True, "t": 82, "dur": self._dur,
                    "src": "https://x/v.mp4", "interactions": 1, "body": self._body}
        # video-load poll (check_video_loads): {has, ready, dur, src}
        if "readyState" in expr or ("v.duration" in expr and "has:" in expr) or "has:true" in expr:
            return {"has": self._has_video, "ready": 4, "dur": self._dur, "src": "https://x/v.mp4"}
        return "ok"
    def wait_ms(self, ms): return None
    def screenshot(self, path): return True


def test_content_check_passes_when_title_present():
    n, L = _g9_l01()
    from player_test.expectations import lesson_expectation
    e = lesson_expectation("G9", n, L)
    d = _FakeDriver(body=L.title + " and the rest of the lesson body")
    fs = C.check_content_renders(d, e, "/tmp")
    assert any(f.severity == "pass" for f in fs)
    assert not any(f.severity == "fail" for f in fs)


def test_content_check_fails_on_leaked_markup():
    n, L = _g9_l01()
    e = lesson_expectation("G9", n, L)
    d = _FakeDriver(body=L.title + " <div class=x> raw markup leaked")
    fs = C.check_content_renders(d, e, "/tmp")
    assert any(f.severity == "fail" and f.check == "content_rawhtml" for f in fs)


def test_video_loads_check_matches_duration():
    n, L = _g9_l01()
    e = lesson_expectation("G9", n, L)
    d = _FakeDriver(dur=int(e["duration_seconds"]))
    fs = C.check_video_loads(d, e, "/tmp")
    assert fs[0].severity == "pass"


def test_report_summarize_and_markdown():
    findings = [
        C.Finding("L1", "G9", "video_loads", "pass").dict(),
        C.Finding("L1", "G9", "one_beat_pause_1", "fail", "pause", "no pause", "s.png").dict(),
        C.Finding("L2", "G9", "grading", "warn", "score", "0/5").dict(),
    ]
    s = summarize(findings)
    assert s["by_severity"]["pass"] == 1 and s["by_severity"]["fail"] == 1 and s["by_severity"]["warn"] == 1
    md = markdown("G9", findings, {"lessons_run": 2, "lessons_total": 29, "browser": True})
    assert "one_beat_pause_1" in md and "grading" in md
    assert "1 pass, 1 warn, 1 fail" in md
