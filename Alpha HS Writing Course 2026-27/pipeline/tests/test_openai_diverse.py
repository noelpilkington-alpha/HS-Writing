# pipeline/tests/test_openai_diverse.py
import os, sys, json
PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path: sys.path.insert(0, PIPE)
from openai_diverse import OpenAIDiverse


def test_judge_dry_returns_chat_body_with_prompt():
    c = OpenAIDiverse()
    prompt = "Assess whether the correct answer is defensible."
    r = c.second_opinion(
        "judge",
        {"stem": "x", "options": ["a", "b", "c", "d"]},
        prompt,
        live=False,
    )
    assert r["status"] == "dry"
    assert r["request_id"] is None
    body = r["would_send"]
    assert "model" in body
    assert "messages" in body and isinstance(body["messages"], list)
    # the prompt text appears somewhere in the messages
    joined = json.dumps(body["messages"])
    assert prompt in joined


def test_author_dry_returns_chat_body():
    c = OpenAIDiverse()
    r = c.second_opinion(
        "author",
        "Schools should extend lunch.",
        "Write a stronger version.",
        live=False,
    )
    assert r["status"] == "dry"
    assert r["request_id"] is None
    body = r["would_send"]
    assert "model" in body
    assert "messages" in body and isinstance(body["messages"], list)


def test_key_never_appears_in_repr():
    c = OpenAIDiverse()
    assert "sk-" not in repr(c) and "sk-" not in str(vars(c))
