"""
frame_arg_daylight_saving.py  -  ISSUE FRAME (lesson-bucket) for the daylight-saving debate (G10).
Short own-authored 2-sided framing bound to CLAIM-TIER G10 lessons. family=issue_frame. Faithful paraphrase of
ACC-W910-ARG-OPP-LESSON-DST. Own words, no fabricated figures, no em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, qc_stimulus, qc_report

FRAME = (
"The debate: should the United States stop switching the clocks twice a year and keep "
"one fixed time? Both sides have a case. Those who want to end the switch say the twice-a-year change disrupts "
"sleep and the body's clock, which can hurt health and focus for days afterward, so a single steady time would "
"be better. Those who are cautious say the real question is trickier: ending the switch is not the same as "
"choosing which fixed time to keep, and permanent evening daylight has trade-offs, such as darker winter "
"mornings for children heading to school. Decide which case you find more convincing, and pick one reason for "
"it."
)

REC = StimulusRecord(
    id="ACC-W910-FRAME-DST",
    grade="9-10", mode="argument", family="issue_frame", bucket="lesson",
    topic_id="daylight_saving", annotated=False,
    modeling_anchor="claim-task issue frame (short 2-sided framing for a G10 counterclaim/claim lesson)",
    acc_tags=["ACC.W.ARG.1", "CCSS.W.9-10.1a"],
    prompt=("Should the United States stop switching the clocks twice a year? Take a side and write one "
            "arguable claim, fairly noting the other side."),
    passages=[Passage(title="The debate: daylight saving time",
                      angle="two-sided framing (for and against ending the clock switch)", text=FRAME)],
    fact_sources=[],
    provenance={"copyright": "own_authored", "rights": "own-words framing of an own-authored source",
                "authored": "2026-07-12",
                "note": "Faithful paraphrase of the two sides in ACC-W910-ARG-OPP-LESSON-DST (full opposing pair holds the verified CDC/DOE/DOT points + is bound by the cross-text lessons). Qualitative only."},
)

if __name__ == "__main__":
    qc = qc_stimulus(REC)
    import re
    print(f"  frame word count: {len(re.findall(r'[A-Za-z]+', FRAME))}")
    print(qc_report(REC)); sys.exit(0 if qc["passed"] else 1)
