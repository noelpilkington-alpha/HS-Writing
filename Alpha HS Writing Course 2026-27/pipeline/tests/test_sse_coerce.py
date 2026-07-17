# tests/test_sse_coerce.py
# Regression: Fable-5 intermittently returns the NESTED journal_update object as a string of
# <parameter name="KEY">JSON</parameter> pseudo-XML instead of a real object. That crashed the
# G9 pilot (dict(<str>) -> ValueError) on 20/27 lessons AND discarded the student's response.
# These tests lock the recovery + the defense-in-depth in walk_lesson.
import os, sys
PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)
from sim_student_eval.models import _coerce_dict, _normalize_turn
from sim_student_eval.student_agent import walk_lesson

# the real failing shape captured from the live run (skills as a <parameter> block, etc.)
_XML_FORM = ('\n<parameter name="skills_i_can_now_do">["Tell apart a fact", "Write a claim"]</parameter>'
             '<parameter name="confidence">{"claim": 0.8}</parameter>'
             '<parameter name="felt_repeated">{"echoes_lesson": "g9_l01", "what": "repeat"}</parameter>')


def test_coerce_recovers_parameter_xml_form():
    d = _coerce_dict(_XML_FORM)
    assert d["skills_i_can_now_do"] == ["Tell apart a fact", "Write a claim"]
    assert d["confidence"] == {"claim": 0.8}          # inner JSON parsed, not left as a string
    assert d["felt_repeated"]["echoes_lesson"] == "g9_l01"


def test_coerce_handles_dict_json_and_garbage():
    assert _coerce_dict({"a": 1}) == {"a": 1}          # already a dict
    assert _coerce_dict('{"x": 1}') == {"x": 1}        # plain JSON string
    assert _coerce_dict("total nonsense") == {}         # unrecoverable -> {} (never raises)
    assert _coerce_dict(None) == {}


def test_normalize_turn_keeps_response_and_coerces_journal():
    nt = _normalize_turn({"response": "my answer", "journal_update": _XML_FORM})
    assert nt["response"] == "my answer"                # the response is NEVER lost
    assert isinstance(nt["journal_update"], dict)
    assert "skills_i_can_now_do" in nt["journal_update"]


class _StrJournalClient:
    """A client whose .ask returns journal_update as the raw string form (simulating an
    un-normalized path), to prove walk_lesson itself won't crash or drop the response."""
    def ask(self, system, user):
        return {"response": "I answered the checks.", "journal_update": _XML_FORM}


def test_walk_lesson_survives_string_journal_update():
    from sim_student_eval.render_course import load_g9_lessons
    L = load_g9_lessons()[1]  # a lesson that failed in the pilot (g9_l02)
    res = walk_lesson(_StrJournalClient(), {"system_preamble": "s"}, L, "(memory)")
    # the response survives even though journal_update arrived as a string
    assert res["response"] == "I answered the checks."
    # journal_update is always a dict with lesson + seq set
    assert isinstance(res["journal_update"], dict)
    assert res["journal_update"]["lesson"].startswith("g9_l02")
    assert "seq" in res["journal_update"]
