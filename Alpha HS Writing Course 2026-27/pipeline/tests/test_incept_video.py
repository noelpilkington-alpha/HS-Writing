# pipeline/tests/test_incept_video.py
#
# Task 6 (Phase D): incept_video.py is the POST-LOCK video-stage MACHINERY. It builds + tests the
# stage only; it does NOT generate or bind any video here (video runs after the next full content
# build, by design). Every test runs live=False / no network. Fixtures use synthetic stems only:
# no S3 url or secret appears anywhere in this file.
import os
import sys

PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)

from incept_video import (video_targets, generate_video, reconcile_questions, VIDEO_TARGETS,
                          video_resource_plan)
from lesson_contract import Lesson, Slot


# ---- video component-resource plan (type=video, NOT QTI; lessonType on the link only) ----
def test_video_resource_plan_shape():
    plan = video_resource_plan("ACC-W910-L-G9-C901-0001",
                               "https://cdn.inceptstore.com/v/abc/video.mp4",
                               title="Take a Side", xp=50, topic_id="topic-xyz", sort_order=3)
    kinds = [row[0] for row in plan]
    assert kinds == ["resource", "component-resource"]
    res_body = plan[0][3]["resource"]
    cr_body = plan[1][3]["componentResource"]
    # resource: type=video + hosted url; NO lessonType in resource metadata (500-bug gotcha)
    assert res_body["metadata"]["type"] == "video"
    assert res_body["metadata"]["url"] == "https://cdn.inceptstore.com/v/abc/video.mp4"
    assert "lessonType" not in res_body["metadata"]
    # component-resource link: lessonType lives HERE, points at the leaf topic
    assert cr_body["metadata"]["lessonType"] == "video"
    assert cr_body["courseComponent"]["sourcedId"] == "topic-xyz"
    assert cr_body["resource"]["sourcedId"] == plan[0][1]  # link references the resource id


# ---- (a) curated seed list includes the required G9 L01 target --------------
def test_video_targets_g9_includes_l01():
    targets = video_targets("g9")
    assert isinstance(targets, list)
    assert ("C901-0001", 1) in targets


def test_seed_list_holds_the_required_entry():
    assert ("C901-0001", 1) in VIDEO_TARGETS


# ---- (b) dry generate_video echoes a video/voiceover would-send (no network) -
def test_generate_video_dry_is_video_voiceover():
    r = generate_video("C901-0001", live=False)
    assert r["status"] == "dry"
    assert r["request_id"] is None
    assert r["would_send"]["generation_type"] == "video"
    assert r["would_send"]["options"]["kind"] == "voiceover"
    assert r["would_send"]["options"]["mode"] == "content_only"


def test_generate_video_never_raises_on_unknown_lesson():
    # an unknown id must still return a dry body (stub prompt), never raise.
    r = generate_video("C999-9999", live=False)
    assert r["status"] == "dry"
    assert r["would_send"]["generation_type"] == "video"


# ---- (c) reconcile flags a duplicate + returns [] when the video has none ----
def _discrim_lesson():
    slot = Slot("SUPPORTED", "discrimination", "Which statement is an arguable claim?",
                labeled_grade_c=True)
    return Lesson(id="ACC-W910-L-G9-C901-0001", grade="9-10", lesson_type=2,
                  unit="G9 U1", title="Arguable claim", target="Pick the claim.", slots=[slot])


def test_reconcile_flags_a_duplicate_video_question():
    lesson = _discrim_lesson()
    video_json = {"questions": [{"stem": "Which statement is an arguable claim?"}]}
    flags = reconcile_questions(video_json, lesson)
    assert flags, "a video question duplicating a discrimination stem must be flagged"
    row = flags[0]
    assert "duplicates_slot" in row
    assert row["video_q_index"] == 0
    assert "video_stem" in row and "lesson_stem" in row


def test_reconcile_returns_empty_when_no_questions():
    lesson = _discrim_lesson()
    assert reconcile_questions({}, lesson) == []


def test_reconcile_never_raises_on_garbage():
    # defensive: junk input degrades to [] instead of raising.
    assert reconcile_questions(None, None) == []
