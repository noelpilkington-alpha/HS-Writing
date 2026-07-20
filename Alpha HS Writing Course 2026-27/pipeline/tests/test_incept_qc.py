# pipeline/tests/test_incept_qc.py
#
# Task 2 (Phase A): incept_qc.py is an ADVISORY second-judge wrapper. These tests prove:
#   (a) slot_to_qc_content maps a built discrimination Slot -> {stem, options[4], answer_key}
#   (b) record()/low_scoring() round-trip a synthetic verdict WITHOUT network, and the written
#       receipt contains ONLY score/axes/flag keys (NO content/url/secret leaks)
#   (c) qc_item(live=False) returns a dry would-send (no network call)
import json
import os
import sys

PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)

from incept_client import InceptClient
from incept_qc import slot_to_qc_content, qc_item, record, low_scoring
from lesson_contract import Slot, Lesson

TEST_CACHE = "C:/tmp/incept_cache_test"


def _discrim_slot():
    return Slot(
        "SUPPORTED", "discrimination", "Which one is the arguable claim?",
        choices=[
            {"id": "A", "text": "The sky is blue on a clear day.", "correct": False,
             "why": "A verifiable fact, so there is nothing to argue."},
            {"id": "B", "text": "Schools should ban phones during class.", "correct": True,
             "why": "It takes a disputable side a reader could push back on."},
            {"id": "C", "text": "Phones exist in most classrooms.", "correct": False,
             "why": "A fact, not a position."},
            {"id": "D", "text": "I personally enjoy using my phone.", "correct": False,
             "why": "A private preference, not an arguable claim."},
        ],
        labeled_grade_c=True, bank="phones",
    )


def _wrap_lesson(slot):
    return Lesson(
        id="ACC-W910-L-G9-C901-0001", grade="9-10", lesson_type=2,
        unit="G9 U1 claim-building", title="Arguable claims", target="Pick the arguable claim.",
        slots=[slot],
    )


# ---- (a) slot mapping ------------------------------------------------------
def test_slot_to_qc_content_maps_discrimination():
    content = slot_to_qc_content(_discrim_slot())
    assert content["stem"] == "Which one is the arguable claim?"
    assert len(content["options"]) == 4
    assert content["answer_key"]["answer"] == "Schools should ban phones during class."
    assert "explanation" in content["answer_key"]


def test_slot_to_qc_content_maps_production_frq_as_text():
    slot = Slot("INDEPENDENT", "production_frq", "Write an arguable claim",
                body="Write one sentence that takes a disputable side on phones in class.",
                rubric_ref="rc.staar", scored=True, unit="sentence")
    content = slot_to_qc_content(slot)
    assert content["stem"] == "Write an arguable claim"
    assert "prompt" in content and content["prompt"].startswith("Write one sentence")


# ---- (b) record + low_scoring round-trip (NO network, content/secret free) --
def test_record_and_low_scoring_roundtrip_no_network(tmp_path):
    p = str(tmp_path / "receipts.json")
    verdict = {
        "judge_score": 72,
        "passed": False,
        "axes": [
            {"id": "clarity", "score": 80, "pass": True, "detail": "leaky rationale text"},
            {"id": "rigor", "score": 64, "pass": False, "explanation": "leaky text"},
        ],
        # every one of these MUST be dropped from the receipt:
        "presigned_url": "https://incept-assets.s3.amazonaws.com/secretpath?sig=abc",
        "prompt": "secret judge prompt",
        "content": {"stem": "secret stem", "options": ["a", "b"], "answer_key": {"answer": "a"}},
    }
    record("ACC-W910-L-G9-C901-0001", 3, verdict, path=p)

    data = json.loads(open(p, encoding="utf-8").read())
    key = "ACC-W910-L-G9-C901-0001:s3"
    assert key in data
    entry = data[key]
    # the receipt entry holds ONLY scores/axes/flag
    assert set(entry.keys()) == {"judge_score", "passed", "axes", "flagged"}
    assert entry["judge_score"] == 72
    assert entry["passed"] is False
    assert entry["flagged"] is True
    for ax in entry["axes"]:
        assert set(ax.keys()) == {"id", "score", "pass"}

    # NO content/secret keys anywhere in the written receipt json
    def all_keys(o):
        if isinstance(o, dict):
            for k, v in o.items():
                yield k
                yield from all_keys(v)
        elif isinstance(o, list):
            for v in o:
                yield from all_keys(v)
    banned = {"stem", "options", "answer", "url", "prompt", "presigned_url", "content",
              "why", "detail", "explanation", "answer_key"}
    assert not (banned & set(all_keys(data)))
    # strongest check: no url/secret/content text survived into the raw file
    raw = open(p, encoding="utf-8").read()
    assert "http" not in raw
    assert "secret" not in raw

    # low_scoring surfaces the flagged item (lesson:slot + score)
    short = low_scoring(85, path=p)
    assert any("C901-0001:s3" in str(row) for row in short)


def test_low_scoring_omits_passing_high_scores(tmp_path):
    p = str(tmp_path / "receipts.json")
    record("L-A", 0, {"judge_score": 95, "passed": True, "axes": []}, path=p)
    record("L-B", 1, {"judge_score": 60, "passed": False, "axes": []}, path=p)
    short = low_scoring(85, path=p)
    keys = [row["key"] for row in short]
    assert "L-B:s1" in keys
    assert "L-A:s0" not in keys


# ---- (c) qc_item dry = would-send, no network ------------------------------
def test_qc_item_dry_returns_would_send():
    slot = _discrim_slot()
    L = _wrap_lesson(slot)
    r = qc_item(L.id, 0, live=False, lesson=L,
                client=InceptClient(cache_dir=TEST_CACHE))
    assert r["status"] == "dry"
    assert r["request_id"] is None
    assert r["would_send"]["generation_type"] == "question"
    assert r["would_send"]["content"]["stem"] == "Which one is the arguable claim?"
    assert len(r["would_send"]["content"]["options"]) == 4
