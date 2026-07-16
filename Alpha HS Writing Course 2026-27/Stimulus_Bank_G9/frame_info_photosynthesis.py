"""
frame_info_photosynthesis.py  -  ORIENTATION FRAME (lesson-bucket) for the photosynthesis explain task.
Short own-authored topic orientation (topic + parts to explain, NO side) bound to CLAIM-TIER (T2) slots.
family=issue_frame. Faithful to ACC-W910-INFO-LESSON-PHOTOSYNTHESIS. Own words, no fabricated figures, no em
dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, qc_stimulus, qc_report

FRAME = (
"Photosynthesis is the process a green plant uses to make its own food. It works by conversion: a plant takes "
"in three ingredients, sunlight, water, and carbon dioxide, and turns them into sugar, which feeds the plant, "
"and oxygen, which it releases into the air. This work happens mostly in the leaves."
)

REC = StimulusRecord(
    id="ACC-W910-FRAME-PHOTOSYNTHESIS",
    grade="9", mode="explanatory", family="issue_frame", bucket="lesson",
    topic_id="photosynthesis", annotated=False,
    modeling_anchor="claim-task orientation frame (short topic orientation for a T2 controlling-idea lesson)",
    acc_tags=["ACC.W.INFO.1", "CCSS.W.9-10.2a"],
    prompt=("Explain how photosynthesis turns light into food. Write one controlling idea that sets a focus "
            "and previews the inputs and outputs, taking no side."),
    passages=[Passage(title="How photosynthesis turns light into food",
                      angle="topic orientation (names the parts to explain; no side)", text=FRAME)],
    fact_sources=[],
    provenance={"copyright": "own_authored", "rights": "own-words orientation of an own-authored source",
                "authored": "2026-07-12",
                "note": "Faithful orientation to ACC-W910-INFO-LESSON-PHOTOSYNTHESIS (full source, bound by evidence lessons). Qualitative."},
)

if __name__ == "__main__":
    qc = qc_stimulus(REC)
    import re
    print(f"  frame word count: {len(re.findall(r'[A-Za-z]+', FRAME))}")
    print(qc_report(REC)); sys.exit(0 if qc["passed"] else 1)
