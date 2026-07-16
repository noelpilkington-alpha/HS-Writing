"""
frame_arg_ai_regulation.py  -  ISSUE FRAME (lesson-bucket) for the AI-workforce-policy debate (G11).
Short own-authored 2-sided framing bound to CLAIM/NUANCE-TIER G11 lessons. family=issue_frame. Faithful
paraphrase of ACC-W910-ARG-LESSON-AIWORKFORCE. Own words, no fabricated figures, no em dashes. Runs QC.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, qc_stimulus, qc_report

FRAME = (
"The debate: as artificial intelligence reshapes work, should the government actively "
"steer workers toward the fastest-growing fields, or leave that sorting to the market? Both sides accept that "
"the technology fields are growing quickly. Those who favor active steering argue that leaving workers to find "
"their own way wastes talent and time, so public money should fund training pipelines and target help at "
"workers whose industries are shrinking. Those who favor a light touch argue that official projections are "
"only estimates, that today's hot field may fade in ten years, and that workers and employers, who feel the "
"shifts first, respond better than central plans. A strong claim here will be nuanced, not one-sided. Decide "
"where you land and pick your strongest reason."
)

REC = StimulusRecord(
    id="ACC-W910-FRAME-AIWORKFORCE",
    grade="11", mode="argument", family="issue_frame", bucket="lesson",
    topic_id="ai_workforce_policy", annotated=False,
    modeling_anchor="claim-task issue frame (short 2-sided framing for a G11 nuance/claim lesson)",
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "CCSS.W.11-12.1"],
    prompt=("Should the government steer workers toward growing fields, or leave it to the market? Write one "
            "nuanced, arguable claim."),
    passages=[Passage(title="The debate: government and the AI workforce",
                      angle="two-sided framing (active steering vs light touch)", text=FRAME)],
    fact_sources=[],
    provenance={"copyright": "own_authored", "rights": "own-words framing of an own-authored source",
                "authored": "2026-07-12",
                "note": "Faithful paraphrase of ACC-W910-ARG-LESSON-AIWORKFORCE (holds verified BLS/NSF/GAO figures + bound by the reasoning/analysis lessons). Qualitative only."},
)

if __name__ == "__main__":
    qc = qc_stimulus(REC)
    import re
    print(f"  frame word count: {len(re.findall(r'[A-Za-z]+', FRAME))}")
    print(qc_report(REC)); sys.exit(0 if qc["passed"] else 1)
