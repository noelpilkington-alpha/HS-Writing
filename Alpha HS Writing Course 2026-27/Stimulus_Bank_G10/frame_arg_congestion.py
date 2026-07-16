"""
frame_arg_congestion.py  -  ISSUE FRAME (lesson-bucket) for the congestion-pricing debate (G10).
Short own-authored 2-sided framing bound to CLAIM-TIER (counterclaim) G10 lessons. family=issue_frame.
Faithful paraphrase of the two sides in ACC-W910-ARG-OPP-LESSON-CONGESTION (the full opposing pair remains the
provenance anchor + the source the cross-text lessons bind). Own words, no fabricated figures, no em dashes.
Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, qc_stimulus, qc_report

FRAME = (
"The debate: should cities charge drivers a toll to enter the busiest downtown "
"streets at peak hours (congestion pricing)? Both sides have a case. Supporters say charging for peak road "
"use thins the worst traffic, cuts the pollution idling cars create, and raises money that can fund buses and "
"trains for everyone. Opponents say the toll asks the wrong people to pay, since lower-income workers who "
"must drive at fixed hours cannot simply shift their trips, so the charge can hit hardest those who can least "
"afford it. Decide which case you find more convincing, and pick one reason for it."
)

REC = StimulusRecord(
    id="ACC-W910-FRAME-CONGESTION",
    grade="9-10", mode="argument", family="issue_frame", bucket="lesson",
    topic_id="congestion_pricing", annotated=False,
    modeling_anchor="claim-task issue frame (short 2-sided framing for a G10 counterclaim/claim lesson)",
    acc_tags=["ACC.W.ARG.1", "CCSS.W.9-10.1a"],
    prompt=("Should cities charge a toll to drive into the busiest downtown at peak hours? Take a side and "
            "write one arguable claim, fairly noting the other side."),
    passages=[Passage(title="The debate: congestion pricing",
                      angle="two-sided framing (for and against downtown tolls)", text=FRAME)],
    fact_sources=[],
    provenance={"copyright": "own_authored", "rights": "own-words framing of an own-authored source",
                "authored": "2026-07-12",
                "note": "Faithful paraphrase of the two sides in ACC-W910-ARG-OPP-LESSON-CONGESTION (full opposing pair holds the verified DOT/EPA/BLS figures + is bound by the cross-text lessons). Qualitative only."},
)

if __name__ == "__main__":
    qc = qc_stimulus(REC)
    import re
    print(f"  frame word count: {len(re.findall(r'[A-Za-z]+', FRAME))}")
    print(qc_report(REC)); sys.exit(0 if qc["passed"] else 1)
