"""
Source-free ARGUMENT stimulus for the G12 writing course (AP Lang mastery tier, TEST bucket).
Shape: AP English Language Q3 (a general, source-free prompt; the student argues from OWN knowledge,
with NO provided passage and NO fact table). family=prompt_only, mode=argument, form=ap, grade=12.
G12 dimension = SOPHISTICATION: an abstract epistemic tension (the worth of doubt against certainty)
that rewards a nuanced position and attention to the situation in which each becomes a virtue or a vice.
No em dashes in prose. Runs itself through the QC harness.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, qc_stimulus, qc_report

PROMPT = (
    "The philosopher Bertrand Russell observed that the trouble with the world is that the foolish are "
    "cocksure while the wise are full of doubt. Doubt, on this view, keeps a mind honest, open to "
    "correction, and unwilling to mistake its assumptions for facts. Others answer that doubt carried too "
    "far becomes paralysis, that action requires conviction, and that people who can commit to nothing "
    "accomplish nothing. A surgeon, a soldier, or a founder cannot pause forever to reconsider.\n\n"
    "Carefully consider the roles that doubt and certainty play in a life of thought and action. Then "
    "write an essay in which you develop a position on whether doubt is more valuable than certainty to a "
    "thinking person. Argue a position using specific evidence from your reading, studies, observation, "
    "or experience."
)

REC = StimulusRecord(
    id="ACC-W910-SFA-PROMPT-0005",
    grade="12", mode="argument", family="prompt_only", bucket="test",
    form="ap", topic_id="certainty_doubt",
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
