"""
Source-free ARGUMENT stimulus for the G11 writing course (TEST bucket).
Shape: AP English Language Q3 (a general, source-free prompt; the student argues from OWN knowledge,
with NO provided passage and NO fact table). family=prompt_only, mode=argument, form=ap.
Prompt = an idea + background + the argue-a-position task. G11 academic register.
No em dashes in prose. Runs itself through the QC harness.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, qc_stimulus, qc_report

PROMPT = (
    "Ambition drives people to reach beyond what they already have, to build, to compete, and to leave a mark "
    "on the world, and societies often celebrate the ambitious as their inventors, founders, and reformers. "
    "Others argue that contentment, the capacity to find sufficiency and peace in one's present circumstances, "
    "is the rarer and more valuable achievement, and that restless striving can cost a person the very life it "
    "was meant to improve.\n\n"
    "Carefully consider the competing values of ambition and contentment. Then write an essay in which you "
    "develop a position on whether ambition is more valuable than contentment. Argue a position using specific "
    "examples drawn from your reading, studies, observation, or experience."
)

REC = StimulusRecord(
    id="ACC-W910-SFA-PROMPT-0003",
    grade="11", mode="argument", family="prompt_only", bucket="test",
    form="ap", topic_id="ambition_contentment",
    modeling_anchor="AP Lang Q3 argument",
    acc_tags=["ACC.W.ARG.1", "CCSS.W.11-12.1"],
    prompt=PROMPT,
    passages=[],
    fact_sources=[],
    annotated=False,
    provenance={"copyright": "own_authored", "rights": "original prompt", "authored": "2026-07-09"},
)

if __name__ == "__main__":
    qc = qc_stimulus(REC); print(qc_report(REC)); import sys; sys.exit(0 if qc["passed"] else 1)
