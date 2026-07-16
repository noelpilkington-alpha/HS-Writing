"""
frame_arg_infrastructure.py  -  ISSUE FRAME (lesson-bucket) for the energy-spending-priorities debate (G11).
Short own-authored 2-sided framing bound to CLAIM/NUANCE-TIER G11 lessons. family=issue_frame. Faithful
paraphrase of ACC-W910-ARG-LESSON-INFRASTRUCTURE. Own words, no fabricated figures, no em dashes. Runs QC.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, qc_stimulus, qc_report

FRAME = (
"The debate: with limited public money for energy, should the country spend first on "
"building new clean-power capacity (more wind and solar), or first on the grid itself (the wires, substations, "
"and storage that move and hold power)? Both sides want a cleaner, reliable system. The build-capacity camp "
"argues that more generation is what actually cuts emissions, and that new wind and solar can be added quickly. "
"The fix-the-grid camp argues that new power is useless if the grid cannot carry or store it, so the wires and "
"storage should come first or the new capacity is wasted. A strong claim will weigh the two, not just pick a "
"slogan. Decide where you land and pick your strongest reason."
)

REC = StimulusRecord(
    id="ACC-W910-FRAME-INFRASTRUCTURE",
    grade="11", mode="argument", family="issue_frame", bucket="lesson",
    topic_id="energy_spending_priority", annotated=False,
    modeling_anchor="claim-task issue frame (short 2-sided framing for a G11 nuance/claim lesson)",
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "CCSS.W.11-12.1"],
    prompt=("Should energy money go first to new clean-power capacity or first to the grid? Write one nuanced, "
            "arguable claim."),
    passages=[Passage(title="The debate: build capacity or fix the grid first",
                      angle="two-sided framing (capacity-first vs grid-first)", text=FRAME)],
    fact_sources=[],
    provenance={"copyright": "own_authored", "rights": "own-words framing of an own-authored source",
                "authored": "2026-07-12",
                "note": "Faithful paraphrase of ACC-W910-ARG-LESSON-INFRASTRUCTURE (holds verified EIA figures + bound by the reasoning lessons). Qualitative only."},
)

if __name__ == "__main__":
    qc = qc_stimulus(REC)
    import re
    print(f"  frame word count: {len(re.findall(r'[A-Za-z]+', FRAME))}")
    print(qc_report(REC)); sys.exit(0 if qc["passed"] else 1)
