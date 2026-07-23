# pipeline/tests/test_video_timing.py
# Cue-point derivation for interactive-video embedded questions. No network; synthetic fixtures modeled on
# the proven probe (artifact 10892): 7 segments (start/model/model/try_it/model/try_it/recap), 3 questions.
import os, sys
PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)
from video_timing import cue_points, timing_map, _segment_ends


def _probe_like():
    # durations mirror the real probe: 12,16,15,18,22,18,15 -> cum ends 12,28,43,61,83,101,116
    script = [
        {"segment": 1, "role": "start", "duration_seconds": 12},
        {"segment": 2, "role": "model", "duration_seconds": 16},
        {"segment": 3, "role": "model", "duration_seconds": 15},
        {"segment": 4, "role": "try_it", "duration_seconds": 18},
        {"segment": 5, "role": "model", "duration_seconds": 22},
        {"segment": 6, "role": "try_it", "duration_seconds": 18},
        {"segment": 7, "role": "recap", "duration_seconds": 15},
    ]
    questions = [{"stem": "Which sentence is an arguable claim?"},
                 {"stem": "What does this sentence lack?"},
                 {"stem": "Which part is the REASON?"}]
    return {"output_json": {"script": script, "questions": questions}}


def test_cues_land_on_check_role_segment_ends():
    vj = _probe_like()
    cues = cue_points(vj)
    assert len(cues) == 3
    # the 3 check-role segments are try_it(seg4 end=61), try_it(seg6 end=101), recap(seg7 end=116)
    times = [c["cue_seconds"] for c in cues]
    assert times == [61.0, 101.0, 116.0], times
    assert all(c["basis"] == "check-role" for c in cues)
    # cues are in playback order and never at t=0
    assert times == sorted(times) and times[0] > 0


def test_segment_ends_are_cumulative():
    script = _probe_like()["output_json"]["script"]
    assert _segment_ends(script) == [12.0, 28.0, 43.0, 61.0, 83.0, 101.0, 116.0]


def test_more_questions_than_check_roles_falls_back_to_even():
    # 2 check-role segments but 4 questions -> first 2 land on check ends, last 2 spread evenly after
    script = [
        {"role": "start", "duration_seconds": 10},
        {"role": "try_it", "duration_seconds": 10},   # end 20
        {"role": "model", "duration_seconds": 40},
        {"role": "recap", "duration_seconds": 10},     # end 100
    ]
    qs = [{"stem": "q0"}, {"stem": "q1"}, {"stem": "q2"}, {"stem": "q3"}]
    cues = cue_points({"output_json": {"script": script, "questions": qs}})
    assert len(cues) == 4
    # durations 10,10,40,10 -> cumulative ends 10,20,60,70. check-role cues PRESERVED at try_it end (20)
    # and recap end (70 == total).
    assert cues[0]["cue_seconds"] == 20.0 and cues[0]["basis"] == "check-role"
    assert cues[1]["cue_seconds"] == 70.0 and cues[1]["basis"] == "check-role"
    # recap is the final segment (end == total), so no runtime remains after it: the 2 leftover questions
    # fire at the video END (70), and the check-role cues are NOT clobbered.
    for c in cues[2:]:
        assert c["basis"] == "even"
        assert c["cue_seconds"] == 70.0


def test_no_durations_falls_back_to_even_over_total_zero():
    # script with no durations -> total 0 -> integer index-order cues (never crashes)
    script = [{"role": "model"}, {"role": "try_it"}]
    qs = [{"stem": "q0"}, {"stem": "q1"}]
    cues = cue_points({"output_json": {"script": script, "questions": qs}})
    assert len(cues) == 2
    assert all(c["cue_seconds"] is not None for c in cues)


def test_no_questions_returns_empty():
    assert cue_points({"output_json": {"script": [{"role": "model", "duration_seconds": 5}], "questions": []}}) == []
    assert cue_points({}) == []


def test_timing_map_carries_stems_and_total():
    tm = timing_map(_probe_like())
    assert tm["total_seconds"] == 116.0
    assert tm["n_questions"] == 3
    assert tm["cues"][0]["stem"] == "Which sentence is an arguable claim?"
    assert tm["cues"][0]["cue_seconds"] == 61.0


def test_never_raises_on_garbage():
    for bad in (None, 42, "x", {"output_json": "nope"}, {"output_json": {"script": "nope"}}):
        assert cue_points(bad) == []
        assert timing_map(bad)["cues"] == []
