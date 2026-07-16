"""
frame_arg_community_service.py  -  ISSUE FRAME (lesson-bucket) for the required-community-service debate.
Short own-authored 2-sided framing bound to CLAIM-TIER (T2) lesson slots. family=issue_frame. Faithful
paraphrase of the two sides in ACC-W910-ARG-LESSON-COMMUNITYSERVICE (the full source + provenance anchor).
Own words, no fabricated figures, no em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, qc_stimulus, qc_report

FRAME = (
"The debate: should schools require students to do community service in order to "
"graduate? Both sides have a case. Those who support a requirement say it builds character and responsibility "
"that a textbook cannot teach, and that requiring it is fairer, since students who would never volunteer on "
"their own get the same chance to help their community as students who are already pushed to volunteer at "
"home. Those who are against a requirement say that forcing service turns a generous act into just another "
"box to check, which can drain the meaning out of it, and that students are already busy and should choose "
"service freely. Decide which case you find more convincing, and pick one reason for it."
)

REC = StimulusRecord(
    id="ACC-W910-FRAME-COMMUNITYSERVICE",
    grade="9", mode="argument", family="issue_frame", bucket="lesson",
    topic_id="community_service_requirement", annotated=False,
    modeling_anchor="claim-task issue frame (short 2-sided framing for a T2 claim lesson)",
    acc_tags=["ACC.W.ARG.1", "CCSS.W.9-10.1a"],
    prompt=("Should schools require community service for graduation? Take a side and write one arguable claim "
            "with a reason."),
    passages=[Passage(title="The debate: required community service",
                      angle="two-sided framing (for and against a graduation requirement)", text=FRAME)],
    fact_sources=[],
    provenance={"copyright": "own_authored", "rights": "own-words framing of an own-authored source",
                "authored": "2026-07-12",
                "note": ("Faithful paraphrase of the two sides in ACC-W910-ARG-LESSON-COMMUNITYSERVICE (which "
                         "holds the verified NCES figures + is bound by the evidence lessons). Qualitative only.")},
)

if __name__ == "__main__":
    qc = qc_stimulus(REC)
    import re
    print(f"  frame word count: {len(re.findall(r'[A-Za-z]+', FRAME))}")
    print(qc_report(REC)); sys.exit(0 if qc["passed"] else 1)
