# tests/test_sse_smoke.py
import os, sys
PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)
import tempfile
from sim_student_eval.render_course import load_g9_lessons, short_id
from sim_student_eval.student_agent import walk_lesson
from sim_student_eval.journal import JournalStore


class FakeClient:
    name = "fake"
    def __init__(self):
        self.seen = []
    def ask(self, system, user):
        self.seen.append(user)
        return {"response": "I picked B. My claim: schools should X because Y.",
                "journal_update": {"skills_i_can_now_do": ["state a claim"],
                                   "where_i_struggled": [], "open_questions": [],
                                   "confidence": {"claim": 0.7},
                                   "felt_repeated": {"echoes_lesson": "g9_l01", "what": "claim again"}}}
    def ask_tool(self, system, user, tool):
        return {"answer_letter": "B", "can_attempt": True, "missing_skill": ""}


def test_walk_three_lessons_builds_journal_and_bounds_context():
    lessons = load_g9_lessons()[:3]
    fc = FakeClient()
    with tempfile.TemporaryDirectory() as d:
        js = JournalStore(os.path.join(d, "j.jsonl"))
        for seq, L in enumerate(lessons, 1):
            res = walk_lesson(fc, {"system_preamble": "you are a student"}, L, js.digest())
            res["journal_update"]["seq"] = seq
            js.append(res["journal_update"])
        rows = js.entries()
        assert len(rows) == 3
        assert rows[0]["lesson"].startswith("g9_l01")
        # the SECOND lesson's prompt must contain the digest from lesson 1 (memory carried)
        assert "state a claim" in fc.seen[1]
        # but must NOT contain lesson 1's raw response text (no transcript contamination)
        assert "I picked B" not in fc.seen[1]


def test_dev_internals_never_reach_the_client():
    lessons = load_g9_lessons()[:2]
    fc = FakeClient()
    with tempfile.TemporaryDirectory() as d:
        js = JournalStore(os.path.join(d, "j.jsonl"))
        walk_lesson(fc, {"system_preamble": "s"}, lessons[0], js.digest())
    joined = "\n".join(fc.seen)
    for banned in ("ACC-W910", "lesson_type", "Slot(", "Grade-C", "mnemonic_status"):
        assert banned not in joined
