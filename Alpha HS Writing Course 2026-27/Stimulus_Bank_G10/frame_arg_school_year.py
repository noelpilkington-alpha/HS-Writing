"""
frame_arg_school_year.py  -  ISSUE FRAME (lesson-bucket) for the longer-school-year debate (G10).
Short own-authored 2-sided framing bound to CLAIM-TIER G10 lessons. family=issue_frame. Faithful paraphrase of
ACC-W910-ARG-OPP-LESSON-SCHOOLYEAR. Own words, no fabricated figures, no em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, qc_stimulus, qc_report

FRAME = (
"The debate: should the United States lengthen the school year with more instructional "
"days? Both sides have a case. Supporters say the traditional calendar was built around farming, not learning, "
"and that long summers cause a learning slide that hits students from lower-income families hardest, so more "
"days would help close that gap. Opponents say more days is a costly fix that lands hardest on school budgets "
"and families, and that how well time is used matters more than how much of it there is, so quality should come "
"before quantity. Decide which case you find more convincing, and pick one reason for it."
)

REC = StimulusRecord(
    id="ACC-W910-FRAME-SCHOOLYEAR",
    grade="9-10", mode="argument", family="issue_frame", bucket="lesson",
    topic_id="school_year", annotated=False,
    modeling_anchor="claim-task issue frame (short 2-sided framing for a G10 counterclaim/claim lesson)",
    acc_tags=["ACC.W.ARG.1", "CCSS.W.9-10.1a"],
    prompt=("Should the United States lengthen the school year? Take a side and write one arguable claim, "
            "fairly noting the other side."),
    passages=[Passage(title="The debate: a longer school year",
                      angle="two-sided framing (for and against more school days)", text=FRAME)],
    fact_sources=[],
    provenance={"copyright": "own_authored", "rights": "own-words framing of an own-authored source",
                "authored": "2026-07-12",
                "note": "Faithful paraphrase of the two sides in ACC-W910-ARG-OPP-LESSON-SCHOOLYEAR (full opposing pair holds the verified NCES/BLS points + is bound by the cross-text lessons). Qualitative only."},
)

if __name__ == "__main__":
    qc = qc_stimulus(REC)
    import re
    print(f"  frame word count: {len(re.findall(r'[A-Za-z]+', FRAME))}")
    print(qc_report(REC)); sys.exit(0 if qc["passed"] else 1)
