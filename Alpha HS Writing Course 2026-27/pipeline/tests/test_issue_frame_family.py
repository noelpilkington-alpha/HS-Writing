"""
Tests: issue_frame is a first-class, QC-recognized stimulus family.

Before this, issue_frame frames (the cheap two-sided claim-task framings used for PP100 sentence banks) were
NOT a recognized Family, so qc_stimulus reported spurious FAILs (unknown family, word-floor, fact-table,
citable-facts) even though the pipeline consumed them fine. This makes the gate meaningful for frames: an
issue_frame is a short own-words two-sided framing, exempt from the passage word-floor / fact-table /
citable-facts requirements (the student argues from the framing + own knowledge), and recognized by
source_config. It must still pass provenance, content (no bright-line / em dash), and register.
"""
import os
import sys

HERE = os.path.dirname(__file__)
PIPE = os.path.join(HERE, "..")
sys.path.insert(0, PIPE)

from stimulus_contract import StimulusRecord, Passage, qc_stimulus


def _frame(text="The debate: should X? Some say yes because A. Others say no because B. Both sides want good "
                "outcomes. Decide which case is stronger, and pick one reason."):
    return StimulusRecord(
        id="ACC-W910-FRAME-TESTONLY", grade="9", mode="argument", family="issue_frame", bucket="lesson",
        topic_id="test_topic", annotated=False,
        modeling_anchor="claim-task issue frame",
        acc_tags=["ACC.W.ARG.1", "CCSS.W.9-10.1a"],
        prompt="Should X? Take a side and write one arguable claim with a reason.",
        passages=[Passage(title="The debate: X", angle="two-sided framing (for and against)", text=text)],
        fact_sources=[],
        provenance={"copyright": "own_authored", "rights": "own-words framing", "authored": "2026-07-23",
                    "note": "issue_frame"},
    )


def test_issue_frame_passes_qc():
    qc = qc_stimulus(_frame())
    assert qc["passed"], {k:v for k,v in qc["gates"].items() if not v["passed"]}


def test_issue_frame_exempt_from_word_floor():
    """A ~40-word framing is fine (issue_frame is not held to the 480-word passage floor)."""
    short = ("The debate: should students get a say in choosing class texts? Some say yes, it builds interest. "
             "Others say teachers know the standards best. Pick a side and give one reason.")
    qc = qc_stimulus(_frame(short))
    struct = qc["gates"]["structure"]
    assert struct["passed"], struct["detail"]


def test_issue_frame_needs_no_fact_table():
    qc = qc_stimulus(_frame())
    facts = qc["gates"]["fact_sources"]
    citable = qc["gates"]["citable_facts"]
    assert facts["passed"] and citable["passed"]


def test_issue_frame_exemptions_do_not_touch_other_gates():
    """The exemptions are scoped to structure/fact/citable/config/lexile only. A malformed issue_frame (e.g.
    missing modeling_anchor) still fails the provenance gate, so the family is not a blanket pass."""
    r = _frame()
    r.modeling_anchor = ""            # break provenance
    qc = qc_stimulus(r)
    assert not qc["passed"]
    assert not qc["gates"]["provenance"]["passed"]


def test_wave1_frames_are_em_dash_free():
    """The em-dash ban is enforced at the render/push layer, not qc_stimulus; assert our authored frames carry
    no em/en dash so they are clean before they ever reach that layer."""
    import importlib.util
    path = os.path.join(PIPE, "..", "Stimulus_Bank_G9", "frames_pp100_bank_wave1.py")
    spec = importlib.util.spec_from_file_location("frames_pp100_bank_wave1", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for rec in mod.RECORDS:
        text = rec.passages[0].text + " " + rec.prompt
        assert "—" not in text and "–" not in text, f"{rec.id} contains an em/en dash"
