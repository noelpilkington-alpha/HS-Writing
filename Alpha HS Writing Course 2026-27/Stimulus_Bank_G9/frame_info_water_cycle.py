"""
frame_info_water_cycle.py  -  ORIENTATION FRAME (lesson-bucket) for the water-cycle explain task.
Short own-authored topic orientation (names the topic + the parts to explain, NO side) bound to CLAIM-TIER
(T2 controlling-idea) lesson slots. family=issue_frame. Faithful to ACC-W910-INFO-LESSON-WATER-CYCLE (the full
source + provenance anchor). Own words, no fabricated figures, no em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, qc_stimulus, qc_report

FRAME = (
"The water cycle is the endless loop that moves the planet's water between the surface and the sky. It runs "
"through connected stages: water evaporates into the air, condenses into clouds, falls back down as "
"precipitation, and collects in rivers, lakes, and oceans before the loop begins again."
)

REC = StimulusRecord(
    id="ACC-W910-FRAME-WATER-CYCLE",
    grade="9", mode="explanatory", family="issue_frame", bucket="lesson",
    topic_id="water_cycle", annotated=False,
    modeling_anchor="claim-task orientation frame (short topic orientation for a T2 controlling-idea lesson)",
    acc_tags=["ACC.W.INFO.1", "CCSS.W.9-10.2a"],
    prompt=("Explain how the water cycle works. Write one controlling idea that sets a focus and previews the "
            "stages, taking no side."),
    passages=[Passage(title="How the water cycle works",
                      angle="topic orientation (names the parts to explain; no side)", text=FRAME)],
    fact_sources=[],
    provenance={"copyright": "own_authored", "rights": "own-words orientation of an own-authored source",
                "authored": "2026-07-12",
                "note": ("Faithful orientation to ACC-W910-INFO-LESSON-WATER-CYCLE (full source + USGS figures, "
                         "bound by the evidence lessons). Qualitative; no figures reproduced.")},
)

if __name__ == "__main__":
    qc = qc_stimulus(REC)
    import re
    print(f"  frame word count: {len(re.findall(r'[A-Za-z]+', FRAME))}")
    print(qc_report(REC)); sys.exit(0 if qc["passed"] else 1)
