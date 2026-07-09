"""
Source-free ARGUMENT stimulus for the G12 writing course (AP Lang mastery tier, TEST bucket).
Shape: AP English Language Q3 (a general, source-free prompt; the student argues from OWN knowledge,
with NO provided passage and NO fact table). family=prompt_only, mode=argument, form=ap, grade=12.
G12 dimension = SOPHISTICATION: an abstract tension in political and moral philosophy (whether real
freedom depends on obligation to others) that rewards precise definition and a qualified position.
No em dashes in prose. Runs itself through the QC harness.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, qc_stimulus, qc_report

PROMPT = (
    "It is common to imagine freedom as the absence of constraint, the condition of a person left alone "
    "to do as they please. Yet many thinkers have argued the opposite. They hold that a person is most "
    "free not when unbound but when bound well, by promises kept, by duties to family and community, by "
    "commitments that give a life direction and make its choices matter. On this account the person who "
    "owes nothing to anyone is not free but adrift.\n\n"
    "Carefully consider the relationship between freedom and the obligations a person owes to others. "
    "Then write an essay in which you develop a position on whether genuine freedom requires obligation "
    "to others. Argue a position using specific evidence from your reading, studies, observation, or "
    "experience."
)

REC = StimulusRecord(
    id="ACC-W910-SFA-PROMPT-0006",
    grade="12", mode="argument", family="prompt_only", bucket="test",
    form="ap", topic_id="freedom_obligation",
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
