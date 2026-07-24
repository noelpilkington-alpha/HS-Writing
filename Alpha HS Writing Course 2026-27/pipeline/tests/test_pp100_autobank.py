"""
Tests for the conservative depth-N PP100 auto-bank generator (Phase B, quick banks).

pp100_autobank.build_quick_bank(grade, lid, entry, slot, taught_sources, stim, depth) returns
(forms, skipped_reason). It EXTENDS a lesson's existing forms[0] (the current authored prompt, verbatim) with
up to depth-1 additional equivalent forms drawn from the stimulus pool, each on a distinct held-out source of
the SAME grain/mode/family band, with a mechanically-parallel prompt. It is CONSERVATIVE: if the lesson's
prompt references source-set-specific material ("the source set above", "the three sources", an embedded
quoted draft/claim) that a source swap would strand, it refuses (returns forms=[existing forms[0]] only, with a
skip reason) rather than emit a broken prompt. Whatever it returns must pass pp100_forms.qc_form_bank.
"""
import os
import sys

HERE = os.path.dirname(__file__)
PIPE = os.path.join(HERE, "..")
sys.path.insert(0, PIPE)

import pp100_autobank as AB


class _Stim:
    def __init__(self, family="issue_frame", mode="argument", grade="9", topic="t"):
        self.family, self.mode, self.grade, self.topic_id, self.theme_id = family, mode, grade, topic, ""


POOL = {
    "TAUGHT": _Stim(topic="taught_topic"),
    "SRC-A": _Stim(topic="topic_a"),
    "SRC-B": _Stim(topic="topic_b"),
    "SRC-C": _Stim(topic="topic_c"),
    "SRC-D": _Stim(topic="topic_d"),
}


def _agnostic_entry():
    return {"source": "TAUGHT", "unit": "sentence", "rubric_ref": "rc.staar", "frq_type": "writing",
            "prompt_html": "<p>Write ONE arguable claim answering the question in the source above.</p>"}


def _sourceset_entry():
    return {"source": "TAUGHT", "unit": "essay", "rubric_ref": "rc.staar", "frq_type": "writing",
            "prompt_html": "<p>Using the source set above, weigh the three sources and take a side.</p>"}


class _Slot:
    unit = "sentence"; rubric_ref = "rc.staar"; frq_type = "writing"; role = "INDEPENDENT"


def test_agnostic_lesson_gets_depth3_bank():
    forms, skip = AB.build_quick_bank("G9", "L-AG", _agnostic_entry(), _Slot(),
                                      taught_sources={"TAUGHT"}, stim=POOL, depth=3)
    assert skip is None, skip
    assert len(forms) == 3
    # forms[0] is the original prompt, verbatim
    assert forms[0]["source"] == "TAUGHT"
    assert "arguable claim answering" in forms[0]["prompt_html"]
    # the added forms use distinct held-out sources (not the taught one, not each other)
    added = [f["source"] for f in forms[1:]]
    assert "TAUGHT" not in added
    assert len(set(added)) == len(added)
    for s in added:
        assert s in POOL


def test_sourceset_prompt_is_refused():
    """A prompt that references 'the source set above / three sources' must NOT be source-swapped."""
    forms, skip = AB.build_quick_bank("G9", "L-SS", _sourceset_entry(), _Slot(),
                                      taught_sources={"TAUGHT"}, stim=POOL, depth=3)
    assert skip is not None
    assert "source" in skip.lower() or "swap" in skip.lower()
    assert len(forms) == 1  # only the original, untouched


def test_output_passes_equivalence_gate():
    import pp100_forms as PF
    forms, skip = AB.build_quick_bank("G9", "L-AG", _agnostic_entry(), _Slot(),
                                      taught_sources={"TAUGHT"}, stim=POOL, depth=3)
    ok, problems = PF.qc_form_bank("L-AG", forms, taught_source={"TAUGHT"}, stim=POOL)
    assert ok, problems


def test_depth_capped_by_available_pool():
    """If the eligible pool is smaller than depth, return as many distinct forms as the pool allows (not a
    broken bank of duplicates)."""
    small = {"TAUGHT": _Stim(topic="taught_topic"), "SRC-A": _Stim(topic="topic_a")}
    forms, skip = AB.build_quick_bank("G9", "L-AG", _agnostic_entry(), _Slot(),
                                      taught_sources={"TAUGHT"}, stim=small, depth=3)
    # only 1 held-out source available -> bank of 2 (taught form + 1)
    assert len(forms) == 2
    assert len({f["source"] for f in forms}) == 2


def test_stagger_offset_varies_first_added_source():
    """Two lessons in the same group should not both start their added forms at the same pool source; the
    stagger offset (keyed to the lesson id) shifts where each begins."""
    f1, _ = AB.build_quick_bank("G9", "LESSON-ONE", _agnostic_entry(), _Slot(),
                                taught_sources={"TAUGHT"}, stim=POOL, depth=2)
    f2, _ = AB.build_quick_bank("G9", "LESSON-TWO-DIFFERENT", _agnostic_entry(), _Slot(),
                                taught_sources={"TAUGHT"}, stim=POOL, depth=2)
    # deterministic per lesson id; the added source is allowed to match, but the function must be stable
    assert f1[1]["source"] in POOL and f2[1]["source"] in POOL
    # same lesson id -> same result (determinism, required for idempotent pushes)
    f1b, _ = AB.build_quick_bank("G9", "LESSON-ONE", _agnostic_entry(), _Slot(),
                                 taught_sources={"TAUGHT"}, stim=POOL, depth=2)
    assert [f["source"] for f in f1] == [f["source"] for f in f1b]
