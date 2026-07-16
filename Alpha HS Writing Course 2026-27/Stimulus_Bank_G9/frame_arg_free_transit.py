"""
frame_arg_free_transit.py  -  ISSUE FRAME (lesson-bucket) for the "free public transit" debate.

Short own-authored 2-sided framing bound to CLAIM-TIER (T2) lesson slots. family=issue_frame (floor/Lexile-band
exempt by design, like the other issue frames). Own words, no fabricated figures, no copyrighted text, no em
dashes. Qualitative two-sided framing only; a full fact-sourced source (DOT / city transit public reports) is a
separate U2 evidence-lesson build. Runs the QC harness on execution (issue_frame exempt).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, qc_stimulus, qc_report

FRAME = (
"The debate: should cities make public buses and trains free to ride? Some cities "
"have already dropped fares, so the debate is real. People who support free transit say it helps people who "
"cannot afford a car get to work and school, cuts the traffic and pollution from cars, and speeds up trips "
"because no one waits to pay. People who are against it say someone still has to pay the cost, usually through "
"taxes, and they worry that without fare money the buses and trains will get crowded and harder to keep in "
"good repair. Both sides want a transit system that works for the city. They disagree on whether free rides "
"would make it better or worse. Decide which case you find more convincing, and pick one reason for it."
)

REC = StimulusRecord(
    id="ACC-W910-FRAME-FREETRANSIT",
    grade="9", mode="argument", family="issue_frame", bucket="lesson",
    topic_id="free_public_transit",
    annotated=False,
    modeling_anchor="claim-task issue frame (short 2-sided framing for a T2 claim lesson)",
    acc_tags=["ACC.W.ARG.1", "CCSS.W.9-10.1a"],
    prompt=("Should cities make public transit free to ride? Take a side and write one arguable claim with a "
            "reason."),
    passages=[Passage(title="The debate: free public transit",
                      angle="two-sided framing (for and against free fares)", text=FRAME)],
    fact_sources=[],
    provenance={"copyright": "own_authored", "rights": "own-words framing", "authored": "2026-07-14",
                "note": ("Short claim-task framing (topic slate). Qualitative two-sided framing only; no figures. "
                         "Full fact-sourced source (DOT / city transit public reports) is a separate U2 "
                         "evidence-lesson build. issue_frame family = floor/Lexile-band exempt.")},
)

if __name__ == "__main__":
    qc = qc_stimulus(REC)
    import re
    print(f"  frame word count: {len(re.findall(r'[A-Za-z]+', FRAME))}")
    print(qc_report(REC))
    sys.exit(0)
