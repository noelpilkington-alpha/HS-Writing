# tests/test_sse_journal.py
import os, sys
PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)

import json, tempfile, pytest
from sim_student_eval.journal import validate_entry, JournalStore


def test_validate_fills_defaults_and_requires_lesson():
    e = validate_entry({"lesson": "g9_l01", "seq": 1})
    assert e["skills_i_can_now_do"] == []
    assert e["felt_repeated"] is None
    assert e["confidence"] == {}
    with pytest.raises(ValueError):
        validate_entry({"seq": 1})


def test_validate_truncates_long_lists_and_strings():
    e = validate_entry({"lesson": "x", "seq": 2,
                        "open_questions": ["q"] * 50,
                        "where_i_struggled": ["z" * 999]})
    assert len(e["open_questions"]) == 12
    assert len(e["where_i_struggled"][0]) == 400


def test_store_append_and_readback():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "j.jsonl")
        s = JournalStore(p)
        assert s.entries() == []
        s.append({"lesson": "g9_l01", "seq": 1, "skills_i_can_now_do": ["state a claim"]})
        s.append({"lesson": "g9_l02", "seq": 2, "felt_repeated": {"echoes_lesson": "g9_l01", "what": "claim again"}})
        rows = s.entries()
        assert len(rows) == 2
        assert rows[1]["felt_repeated"]["echoes_lesson"] == "g9_l01"


def test_digest_is_compact_and_mentions_prior_skills():
    with tempfile.TemporaryDirectory() as d:
        s = JournalStore(os.path.join(d, "j.jsonl"))
        s.append({"lesson": "g9_l01", "seq": 1, "skills_i_can_now_do": ["state a claim"],
                  "confidence": {"claim": 0.8}})
        dig = s.digest()
        assert "state a claim" in dig
        assert "g9_l01" in dig
        assert len(dig) < 4000  # bounded
