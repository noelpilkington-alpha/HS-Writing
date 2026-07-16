"""
frame_info_volcanoes.py  -  ORIENTATION FRAME (lesson-bucket) for the volcanoes explain task.
Short own-authored topic orientation (topic + parts, NO side) bound to CLAIM-TIER (T2) slots.
family=issue_frame. Faithful to ACC-W910-INFO-LESSON-VOLCANOES. Own words, no fabricated figures, no em
dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, qc_stimulus, qc_report

FRAME = (
"A volcano is a place where molten rock from deep inside the planet reaches the surface. It forms and erupts "
"in a sequence: intense underground heat melts rock into a thick material called magma, that magma rises when "
"it finds a path upward, and it finally breaks through the surface in an eruption."
)

REC = StimulusRecord(
    id="ACC-W910-FRAME-VOLCANOES",
    grade="9", mode="explanatory", family="issue_frame", bucket="lesson",
    topic_id="volcanoes", annotated=False,
    modeling_anchor="claim-task orientation frame (short topic orientation for a T2 controlling-idea lesson)",
    acc_tags=["ACC.W.INFO.1", "CCSS.W.9-10.2a"],
    prompt=("Explain how volcanoes form and erupt. Write one controlling idea that sets a focus and previews "
            "the stages, taking no side."),
    passages=[Passage(title="How volcanoes form and erupt",
                      angle="topic orientation (names the parts to explain; no side)", text=FRAME)],
    fact_sources=[],
    provenance={"copyright": "own_authored", "rights": "own-words orientation of an own-authored source",
                "authored": "2026-07-12",
                "note": "Faithful orientation to ACC-W910-INFO-LESSON-VOLCANOES (full source, bound by evidence lessons). Qualitative."},
)

if __name__ == "__main__":
    qc = qc_stimulus(REC)
    import re
    print(f"  frame word count: {len(re.findall(r'[A-Za-z]+', FRAME))}")
    print(qc_report(REC)); sys.exit(0 if qc["passed"] else 1)
