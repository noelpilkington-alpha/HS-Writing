"""
test_one_beat.py  -  the One-Beat Check: a single NON-GATING in-video question on a qualifying concept video.

RULE (Council of Writing Instruction, 2026-07-22): a qualifying concept lesson's intro video renders as an
INTERACTIVE tb-video with exactly ONE non-gating tb-interaction that pauses at a cue, shows a recognition
anchor, and resumes. It is DIFFERENT IN KIND from the downstream discrimination gate, authored NEW, and never
blocks progression. Prod push (no one_beat_map, empty module registry) is unaffected.

Covers: one_beat_xml (non-gating XML shape, no em dash), the interactive render (tb-video figure + cue +
catalog config + hosted vq item), the exempt path (video but no One-Beat -> plain video), the prod-safe empty
registry, and the video_timing.one_beat_cue single-cue derivation.

Run: pytest pipeline/tests/test_one_beat.py
"""
from __future__ import annotations
import os
import re
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.dirname(HERE)
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)

from gated_reading import build_lesson_html, one_beat_xml, _one_beat_list  # noqa: E402
import gated_reading as gr                                 # noqa: E402
import video_timing as vt                                  # noqa: E402


SAMPLE_ITEM = {
    "title": "Quick check: the missing move",
    "note": "No penalty. Just your first call, then the video confirms it.",
    "stem": 'The sentence "Homework is boring" takes a side, but which of the three questions does it FAIL?',
    "options": [
        {"id": "A", "text": "Is there a reason? (no reason is attached)", "correct": True,
         "why": "Right. It states a side but gives no reason, so it fails the reason question."},
        {"id": "B", "text": "Does it take a side? (it takes no side at all)", "correct": False,
         "why": "It does take a side of sorts. The move it is missing is a reason."},
    ],
}


# ---------------------------------------------------------------------------
# 1. one_beat_xml: well-formed QTI, NON-gating, per-choice feedback, no em dash.
# ---------------------------------------------------------------------------

def test_one_beat_xml_is_well_formed():
    xml = one_beat_xml("vq-TEST-1", SAMPLE_ITEM)
    ET.fromstring(xml)  # raises on malformed


def test_one_beat_xml_is_non_gating():
    xml = one_beat_xml("vq-TEST-1", SAMPLE_ITEM)
    # a checkpoint HARD-GATES via INTERACTION_VISIBILITY; the One-Beat must NOT.
    assert "INTERACTION_VISIBILITY" not in xml, "One-Beat must not carry the checkpoint gate machinery"
    # completionStatus must be 'completed' on BOTH branches so any answer lets the video resume.
    assert xml.count("<qti-value>completed</qti-value>") == 0  # set via set-outcome-value, not default
    assert xml.count('base-type="identifier">completed') == 2, "completed must be set on correct AND else branch"


def test_one_beat_xml_scores_and_routes_feedback():
    xml = one_beat_xml("vq-TEST-1", SAMPLE_ITEM)
    assert "<qti-correct-response><qti-value>opt_A</qti-value>" in xml, "correct option keyed"
    assert 'identifier="feedback_opt_B"' in xml, "the wrong option gets its own teaching feedback block"
    assert 'identifier="correct"' in xml, "a persistent correct feedback block is present"


def test_one_beat_xml_has_no_em_dash():
    xml = one_beat_xml("vq-TEST-1", SAMPLE_ITEM)
    assert "—" not in xml, "no em dash in student-facing in-video question"


def test_one_beat_xml_carries_note_and_stem():
    xml = one_beat_xml("vq-TEST-1", SAMPLE_ITEM)
    assert "No penalty" in xml, "the no-penalty transparency note renders"
    assert "which of the three questions does it FAIL" in xml, "the stem renders"


# ---------------------------------------------------------------------------
# Helper: a real G9 concept lesson with an opening one-idea teach_card.
# ---------------------------------------------------------------------------

def _find_g9_concept_lesson():
    import tier_a_regression as T
    for _f, L in T._lessons("G9"):
        slots = getattr(L, "slots", None) or []
        s0 = slots[0] if slots else None
        if s0 and getattr(s0, "kind", "") == "teach_card" and getattr(s0, "body", ""):
            return L
    return None


# ---------------------------------------------------------------------------
# 2. Interactive render: video + One-Beat -> tb-video figure with a cue + catalog config + hosted vq item.
# ---------------------------------------------------------------------------

def test_interactive_render_emits_tb_video_with_cue():
    L = _find_g9_concept_lesson()
    assert L is not None
    vm = {L.id: {"mp4": "https://cdn/v.mp4", "vtt": "https://cdn/v.vtt"}}
    obm = {L.id: {"cue_seconds": 82.0, "duration_seconds": 169.0, "item": SAMPLE_ITEM}}
    html, cps = build_lesson_html(L, base_url="https://x/g9/l01", video_map=vm, one_beat_map=obm)

    assert '<figure class="tb-video"' in html, "interactive video renders a tb-video figure"
    assert 'data-timestamp-seconds="82"' in html, "the cue time is on the tb-interaction"
    assert 'data-duration-seconds="169"' in html, "the figure carries the duration"
    vq_id = f"vq-{L.id}-1"
    assert f'data-catalog-idref="{vq_id}"' in html, "the interaction points at the vq item"
    assert f'<div class="tb-qti-config" id="{vq_id}">' in html, "the vq config joins the catalog"
    assert any(cid == vq_id for cid, _ in cps), "the vq item XML is returned for hosting"


def test_interactive_vq_item_is_non_gating_and_clean():
    L = _find_g9_concept_lesson()
    vm = {L.id: {"mp4": "https://cdn/v.mp4", "vtt": "https://cdn/v.vtt"}}
    obm = {L.id: {"cue_seconds": 82.0, "duration_seconds": 169.0, "item": SAMPLE_ITEM}}
    _, cps = build_lesson_html(L, base_url="https://x", video_map=vm, one_beat_map=obm)
    vqxml = next(xml for cid, xml in cps if cid.startswith("vq-"))
    ET.fromstring(vqxml)
    assert "INTERACTION_VISIBILITY" not in vqxml
    assert "—" not in vqxml


# ---------------------------------------------------------------------------
# 2b. Multi-beat: a video with TWO scripted "your turn" beats -> TWO tb-interactions + TWO vq items.
# ---------------------------------------------------------------------------

def _two_beat_item(letter):
    return {"title": f"Check {letter}", "note": "No penalty.",
            "stem": f"Beat {letter}: which move is missing?",
            "options": [{"id": "A", "text": "the reason", "correct": True, "why": "yes"},
                        {"id": "B", "text": "the side", "correct": False, "why": "no"}]}


def test_two_beats_emit_two_interactions_and_items():
    L = _find_g9_concept_lesson()
    vm = {L.id: {"mp4": "https://cdn/v.mp4", "vtt": "https://cdn/v.vtt"}}
    obm = {L.id: {"duration_seconds": 169.0, "beats": [
        {"cue_seconds": 82.0, "item": _two_beat_item("1")},
        {"cue_seconds": 131.0, "item": _two_beat_item("2")},
    ]}}
    html, cps = build_lesson_html(L, base_url="https://x", video_map=vm, one_beat_map=obm)
    assert 'data-timestamp-seconds="82"' in html and 'data-timestamp-seconds="131"' in html, "both cues render"
    assert f'data-catalog-idref="vq-{L.id}-1"' in html and f'data-catalog-idref="vq-{L.id}-2"' in html
    vq_ids = [cid for cid, _ in cps if cid.startswith("vq-")]
    assert vq_ids == [f"vq-{L.id}-1", f"vq-{L.id}-2"], f"two hosted vq items in order: {vq_ids}"
    # the meta caption below the video was removed course-wide (colleague review 2026-07-24): it was
    # non-student-facing lesson-mechanics commentary duplicating the "Watch: the one idea" heading. The
    # video card + its heading + the two interactions still render; only the caption line is gone.
    assert "pauses 2 times" not in html and "A short video of this lesson" not in html, "no meta caption"
    assert "Watch: the one idea" in html, "video card heading still present"


def test_one_beat_list_normalizes_both_shapes():
    single = {"cue_seconds": 82.0, "item": _two_beat_item("1")}
    multi = {"beats": [{"cue_seconds": 82.0, "item": _two_beat_item("1")},
                       {"cue_seconds": 131.0, "item": _two_beat_item("2")}]}
    assert len(_one_beat_list(single)) == 1
    assert len(_one_beat_list(multi)) == 2
    # rule 2026-07-22: cover EVERY your-turn beat, no cap. A 3-beat video keeps all 3.
    over = {"beats": [{"cue_seconds": t, "item": _two_beat_item(str(t))} for t in (10, 20, 30)]}
    assert len(_one_beat_list(over)) == 3, "no cap: every your-turn beat is covered"
    # junk / no item -> []
    assert _one_beat_list({"cue_seconds": 5.0}) == []
    assert _one_beat_list(None) == []


def test_registry_l01_has_two_beats():
    from incept_one_beats import ALL_ONE_BEATS
    l01 = ALL_ONE_BEATS["ACC-W910-L-G9-C901-0001"]
    beats = _one_beat_list(l01)
    assert len(beats) == 2, "L01 covers both scripted your-turn beats"
    assert [b["cue_seconds"] for b in beats] == [82.0, 131.0]
    # every authored stem/why must be em-dash free
    for b in beats:
        xml = one_beat_xml("vq-x", b["item"])
        assert "—" not in xml


def test_full_registry_all_items_pass_qc():
    """Every authored item in the committed registry passes the deterministic QC gate + renders non-gating."""
    import xml.etree.ElementTree as ET
    from incept_one_beats import ALL_ONE_BEATS
    import one_beat_extract as obe
    assert len(ALL_ONE_BEATS) == 45, f"expected 45 lessons, got {len(ALL_ONE_BEATS)}"
    total = 0
    for lid, entry in ALL_ONE_BEATS.items():
        for i, b in enumerate(_one_beat_list(entry)):
            total += 1
            assert obe.qc_one_beat(b["item"]) == [], f"{lid} beat {i}: QC failed"
            x = one_beat_xml(f"vq-{lid}-{i+1}", b["item"])
            ET.fromstring(x)
            assert "INTERACTION_VISIBILITY" not in x, f"{lid} beat {i}: gating xml"
    assert total == 96, f"expected 96 items, got {total}"


# ---------------------------------------------------------------------------
# 3. Exempt path: a video but NO One-Beat -> plain <video>, no tb-video figure, no vq item.
# ---------------------------------------------------------------------------

def test_video_without_one_beat_renders_plain():
    L = _find_g9_concept_lesson()
    vm = {L.id: {"mp4": "https://cdn/v.mp4", "vtt": "https://cdn/v.vtt"}}
    html, cps = build_lesson_html(L, base_url="https://x", video_map=vm, one_beat_map={})
    assert '<video controls="controls"' in html, "the plain intro video still renders"
    assert "tb-video" not in html, "an exempt lesson must NOT get the interactive figure"
    assert "data-timestamp-seconds" not in html, "no cue on an exempt lesson"
    assert not any(cid.startswith("vq-") for cid, _ in cps), "no vq item for an exempt lesson"


# ---------------------------------------------------------------------------
# 4. Prod-safe: no video_map at all -> no video, no interactive (byte-identical to today).
# ---------------------------------------------------------------------------

def test_prod_path_has_no_video_or_interaction():
    L = _find_g9_concept_lesson()
    html, cps = build_lesson_html(L, base_url="https://x")
    assert "<video" not in html, "prod path (no video_map) emits no video"
    assert "tb-video" not in html
    assert not any(cid.startswith("vq-") for cid, _ in cps)


def test_module_one_beats_ships_empty():
    from incept_one_beats import ONE_BEATS
    assert ONE_BEATS == {}, "the module registry ships EMPTY so prod is unaffected"
    assert gr._ONE_BEATS == {}


# ---------------------------------------------------------------------------
# 5. video_timing.one_beat_cue: the SINGLE default cue at the first check-role beat after min_start.
# ---------------------------------------------------------------------------

def _probe_like():
    # roles start/model/model/try_it/model/try_it/recap -> ends 12,28,43,61,83,101,116
    return {"output_json": {"script": [
        {"role": "start", "duration_seconds": 12},
        {"role": "model", "duration_seconds": 16},
        {"role": "model", "duration_seconds": 15},
        {"role": "try_it", "duration_seconds": 18},   # end 61
        {"role": "model", "duration_seconds": 22},
        {"role": "try_it", "duration_seconds": 18},   # end 101
        {"role": "recap", "duration_seconds": 15},    # end 116 == total
    ]}}


def test_one_beat_cue_first_check_role_after_min_start():
    vj = _probe_like()
    out = vt.one_beat_cue(vj, min_start=43.0)
    assert out["duration_seconds"] == 116.0
    assert out["cue_seconds"] == 61.0, "first try_it end at/after min_start"


def test_one_beat_cue_skips_boundary_before_min_start():
    vj = _probe_like()
    out = vt.one_beat_cue(vj, min_start=70.0)
    assert out["cue_seconds"] == 101.0, "the 61s beat is before min_start; take the next one (101)"


def test_one_beat_cue_never_at_video_end():
    # recap ends AT total (116); a cue there would leave no runtime to resume, so it must not be chosen.
    vj = _probe_like()
    out = vt.one_beat_cue(vj, min_start=110.0)
    assert out["cue_seconds"] != 116.0, "never cue at the video end"


def test_one_beat_cue_never_raises_on_garbage():
    for bad in (None, 42, "x", {"output_json": "nope"}):
        out = vt.one_beat_cue(bad)
        assert out["cue_seconds"] is None or isinstance(out["cue_seconds"], (int, float))


def test_one_beat_cues_returns_all_your_turn_beats_no_cap():
    vj = _probe_like()  # try_it ends at 61 and 101; recap end 116 == total (excluded)
    out = vt.one_beat_cues(vj, min_start=43.0)  # default: no cap
    assert out["cue_seconds"] == [61.0, 101.0], "every try_it beat, recap-at-end excluded"
    assert out["duration_seconds"] == 116.0


def test_one_beat_cues_respects_explicit_max():
    vj = _probe_like()
    assert vt.one_beat_cues(vj, max_cues=1, min_start=0.0)["cue_seconds"] == [61.0]


def test_one_beat_cues_never_raises_on_garbage():
    for bad in (None, 42, "x", {"output_json": "nope"}):
        assert isinstance(vt.one_beat_cues(bad)["cue_seconds"], list)
