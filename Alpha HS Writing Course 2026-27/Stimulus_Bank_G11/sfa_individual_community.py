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
    "People across every society prize their individual freedom: the right to speak, to move, and to choose "
    "how they live. Yet communities also depend on shared sacrifice, and there are moments when a personal "
    "liberty is asked to give way to the welfare of the group, whether during a public health emergency, an "
    "environmental crisis, or a threat to public safety. Thinkers throughout history have disagreed about "
    "where that line should fall.\n\n"
    "Carefully consider the relationship between individual freedom and the good of the community. Then write "
    "an essay in which you develop a position on the question of when, if ever, individual freedom should "
    "yield to the community good. Argue a position using specific examples drawn from your reading, studies, "
    "observation, or experience."
)

REC = StimulusRecord(
    id="ACC-W910-SFA-PROMPT-0002",
    grade="11", mode="argument", family="prompt_only", bucket="test",
    form="ap", topic_id="individual_community",
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
