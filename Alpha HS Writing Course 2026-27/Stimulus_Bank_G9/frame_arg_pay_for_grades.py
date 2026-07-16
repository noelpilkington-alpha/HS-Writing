"""
frame_arg_pay_for_grades.py  -  ISSUE FRAME (lesson-bucket) for the "pay students for good grades" debate.

A SHORT, own-authored 2-sided framing of the debatable question, bound to CLAIM-TIER (T2) lesson slots (used
as the TRANSFER topic in G9 L01, partitioned from the taught four-day-week topic). family=issue_frame
(floor/Lexile-band exempt by design). Own words, no fabricated figures, no copyrighted text, no em dashes.
Runs the QC harness on execution (issue_frame is exempt from the fact-source/floor gates by design).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, qc_stimulus, qc_report

FRAME = (
"The debate: should schools pay students for getting good grades? Some schools have "
"tried cash rewards, so the debate is real. People who support paying students say a reward can push students "
"who have given up to start trying, and that adults get paid for good work, so students could too. People who "
"are against it say students should learn for their own reasons, not for money, and that the effect often "
"fades once the payments stop. They also worry it is unfair to students who work hard but still struggle to "
"earn top grades. Both sides want students to care about school. They disagree on whether money helps or "
"hurts. Decide which case you find more convincing, and pick one reason for it."
)

REC = StimulusRecord(
    id="ACC-W910-FRAME-PAYGRADES",
    grade="9", mode="argument", family="issue_frame", bucket="lesson",
    topic_id="pay_students_for_grades",
    annotated=False,
    modeling_anchor="claim-task issue frame (short 2-sided framing for a T2 claim lesson)",
    acc_tags=["ACC.W.ARG.1", "CCSS.W.9-10.1a"],
    prompt=("Should schools pay students for getting good grades? Take a side and write one arguable claim with "
            "a reason."),
    passages=[Passage(title="The debate: paying students for grades",
                      angle="two-sided framing (for and against cash rewards for grades)", text=FRAME)],
    fact_sources=[],
    provenance={"copyright": "own_authored", "rights": "own-words framing", "authored": "2026-07-14",
                "note": ("Short claim-task framing for G9 L01 (TRANSFER topic, partitioned from taught four-day-"
                         "week). Qualitative two-sided framing only; no figures reproduced. issue_frame family = "
                         "floor/Lexile-band exempt.")},
)

if __name__ == "__main__":
    qc = qc_stimulus(REC)
    import re
    print(f"  frame word count: {len(re.findall(r'[A-Za-z]+', FRAME))}")
    print(qc_report(REC))
    sys.exit(0)
