"""
Source-free ARGUMENT stimulus for the G12 writing course (AP Lang mastery tier, TEST bucket).
Shape: AP English Language Q3 (a general, source-free prompt; the student argues from OWN knowledge,
with NO provided passage and NO fact table). family=prompt_only, mode=argument, form=ap, grade=12.
G12 dimension = SOPHISTICATION: the prompt reaches for a more abstract tension (the hidden costs of
optimizing for efficiency) and invites the student to weigh competing goods, not just pick a side.
No em dashes in prose. Runs itself through the QC harness.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, qc_stimulus, qc_report

PROMPT = (
    "The essayist Wendell Berry warned that a culture devoted to efficiency tends to measure only what it "
    "can count, and so it quietly discards the goods that resist measurement, such as craft, patience, "
    "loyalty, and the slow knowledge of a place. Yet the drive to do more with less has also lifted "
    "millions out of poverty, shortened famines, and freed people from labor that once consumed whole "
    "lives. Efficiency is neither simply a virtue nor simply a loss.\n\n"
    "Carefully consider what a society gains and what it may sacrifice when it organizes itself around "
    "efficiency. Then write an essay in which you develop a position on what, if anything, is lost when a "
    "society optimizes for efficiency. Argue a position using specific evidence from your reading, "
    "studies, observation, or experience."
)

REC = StimulusRecord(
    id="ACC-W910-SFA-PROMPT-0004",
    grade="12", mode="argument", family="prompt_only", bucket="test",
    form="ap", topic_id="progress_cost",
    modeling_anchor="AP Lang Q3 argument (G12 sophistication tier)",
    acc_tags=["ACC.W.ARG.1", "CCSS.W.11-12.1"],
    prompt=PROMPT,
    passages=[],
    fact_sources=[],
    annotated=False,
    provenance={"copyright": "own_authored", "rights": "original prompt", "authored": "2026-07-09"},
)

if __name__ == "__main__":
    qc = qc_stimulus(REC); print(qc_report(REC)); import sys; sys.exit(0 if qc["passed"] else 1)
