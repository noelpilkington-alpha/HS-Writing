"""
frame_info_migration.py  -  ORIENTATION FRAME (lesson-bucket) for the animal-migration explain task.
Short own-authored topic orientation (topic + parts, NO side) bound to CLAIM-TIER (T2) slots.
family=issue_frame. Faithful to ACC-W910-INFO-LESSON-MIGRATION. Own words, no fabricated figures, no em
dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, qc_stimulus, qc_report

FRAME = (
"Migration is the long yearly journey some animals make between one home and another. Explaining it means "
"covering a few connected parts: why animals migrate, mainly to find food and to raise their young when the "
"seasons change; how far they travel, sometimes across whole continents or oceans; and how scientists track "
"their routes."
)

REC = StimulusRecord(
    id="ACC-W910-FRAME-MIGRATION",
    grade="9", mode="explanatory", family="issue_frame", bucket="lesson",
    topic_id="animal_migration", annotated=False,
    modeling_anchor="claim-task orientation frame (short topic orientation for a T2 controlling-idea lesson)",
    acc_tags=["ACC.W.INFO.1", "CCSS.W.9-10.2a"],
    prompt=("Explain how and why animals migrate. Write one controlling idea that sets a focus and previews "
            "the parts, taking no side."),
    passages=[Passage(title="How and why animals migrate",
                      angle="topic orientation (names the parts to explain; no side)", text=FRAME)],
    fact_sources=[],
    provenance={"copyright": "own_authored", "rights": "own-words orientation of an own-authored source",
                "authored": "2026-07-12",
                "note": "Faithful orientation to ACC-W910-INFO-LESSON-MIGRATION (full source, bound by evidence lessons). Qualitative."},
)

if __name__ == "__main__":
    qc = qc_stimulus(REC)
    import re
    print(f"  frame word count: {len(re.findall(r'[A-Za-z]+', FRAME))}")
    print(qc_report(REC)); sys.exit(0 if qc["passed"] else 1)
