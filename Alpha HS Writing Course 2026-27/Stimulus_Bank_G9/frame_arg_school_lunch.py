"""
frame_arg_school_lunch.py  -  ISSUE FRAME (lesson-bucket) for the free-school-meals debate.

Short, own-authored 2-sided framing bound to CLAIM-TIER (T2) lesson slots. family=issue_frame (floor/Lexile-
band exempt by design). Faithful paraphrase of the arguments in the full source ACC-W910-ARG-LESSON-SCHOOLLUNCH
(lesson_arg_school_lunch.py), which remains the provenance anchor + the evidence-lesson source. Own words, no
fabricated figures, no copyrighted text, no em dashes. Runs the QC harness on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, qc_stimulus, qc_report

FRAME = (
"A new question for a fresh claim: should schools give free meals to all students, no matter what their "
"families earn? Both sides have a case. Those who support free meals for everyone say that hunger in class "
"blocks learning for the students who need school most, and that making meals free for all removes the shame "
"some students feel when only a few get free food, so no one skips a meal they are owed. Those who are "
"against it say that families who can afford to pay should, so that limited school funds go to the students "
"who truly need the help rather than to everyone. Decide which case you find more convincing, and pick one "
"reason for it."
)

REC = StimulusRecord(
    id="ACC-W910-FRAME-SCHOOLLUNCH",
    grade="9", mode="argument", family="issue_frame", bucket="lesson",
    topic_id="free_school_meals",
    annotated=False,
    modeling_anchor="claim-task issue frame (short 2-sided framing for a T2 claim lesson)",
    acc_tags=["ACC.W.ARG.1", "CCSS.W.9-10.1a"],
    prompt=("Should schools give free meals to all students? Take a side and write one arguable claim with a "
            "reason."),
    passages=[Passage(title="The debate: free school meals",
                      angle="two-sided framing (for and against universal free meals)", text=FRAME)],
    fact_sources=[],
    provenance={"copyright": "own_authored", "rights": "own-words framing of an own-authored source",
                "authored": "2026-07-12",
                "note": ("Short claim-task framing; faithful paraphrase of the two sides in the full source "
                         "ACC-W910-ARG-LESSON-SCHOOLLUNCH (which holds the verified USDA/NCES figures + is "
                         "bound by the evidence lessons). Qualitative only; no figures reproduced here.")},
)

if __name__ == "__main__":
    qc = qc_stimulus(REC)
    import re
    print(f"  frame word count: {len(re.findall(r'[A-Za-z]+', FRAME))}")
    print(qc_report(REC))
    sys.exit(0 if qc["passed"] else 1)
