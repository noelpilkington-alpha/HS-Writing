"""
Source-free ARGUMENT stimulus for the G11 writing course (TEST bucket).
Shape: AP English Language Q3 (a general, source-free prompt; the student argues from OWN knowledge,
with NO provided passage and NO fact table). family=prompt_only, mode=argument, form=ap.
Prompt = an attributed idea + background + the argue-a-position task. G11 academic register.
No em dashes in prose. Runs itself through the QC harness.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, qc_stimulus, qc_report

PROMPT = (
    "The statesman Edmund Burke described a society as a partnership not only among the living but "
    "between the living, the dead, and those yet to be born, and he argued that inherited customs carry "
    "a wisdom no single generation can match. Others insist that nearly every meaningful advance, from the "
    "repeal of unjust laws to the growth of scientific understanding, has demanded a deliberate break with "
    "practices that earlier generations accepted without question.\n\n"
    "Carefully consider the tension between honoring tradition and pursuing progress. Then write an essay "
    "in which you develop a position on whether genuine progress requires breaking with tradition. Argue "
    "a position using specific examples drawn from your reading, studies, observation, or experience."
)

REC = StimulusRecord(
    id="ACC-W910-SFA-PROMPT-0001",
    grade="11", mode="argument", family="prompt_only", bucket="test",
    form="ap", topic_id="tradition_progress",
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
