"""
Multi-perspective ARGUMENT stimulus for the G11 writing course (TEST bucket).
Shape: ACT Writing (an issue + EXACTLY 3 given perspectives, NO source passage). The scored move is to
evaluate the perspectives, develop the student's own, and analyze the relationship between the student's
position and at least one given perspective. family=perspective_set, mode=argument, form=4trait.
G11 academic register. No em dashes in prose. Runs itself through the QC harness.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, qc_stimulus, qc_report

ISSUE = (
    "Cameras, sensors, and data networks now record much of daily life, and officials argue that this "
    "information helps prevent crime, respond to emergencies, and keep the public safe. Others worry that "
    "constant monitoring erodes the private space in which people think, speak, and live freely. As our "
    "communities grow more connected, it is worth examining how a society should weigh personal privacy "
    "against public safety."
)

PERSPECTIVES = [
    ("Safety must come first. When surveillance tools help authorities stop violence, find missing people, "
     "and hold wrongdoers accountable, the protection of the public justifies a reasonable loss of privacy, "
     "and those who obey the law have little to fear."),
    ("Privacy is the foundation of a free society. Once people believe they are always being watched, they "
     "censor their own speech and behavior, so unchecked monitoring threatens the very liberties that public "
     "safety is meant to protect."),
    ("The real question is not privacy or safety but oversight. Surveillance is neither good nor evil in "
     "itself; its effect depends on who controls the data, what limits the law imposes, and whether citizens "
     "can hold that power accountable."),
]

PROMPT = (
    "Read and carefully consider the perspectives below. Each suggests a particular way of thinking about "
    "privacy and public safety in a connected world.\n\n"
    "Perspective One: " + PERSPECTIVES[0] + "\n\n"
    "Perspective Two: " + PERSPECTIVES[1] + "\n\n"
    "Perspective Three: " + PERSPECTIVES[2] + "\n\n"
    "Write a unified, coherent essay about the balance between privacy and public safety in a connected "
    "world. In your essay, be sure to evaluate the three perspectives given, develop and support your own "
    "perspective on the issue, and analyze the relationship between your perspective and at least one other "
    "perspective. You may agree with any of the perspectives, disagree with all of them, or stake out a "
    "position of your own. Support your reasoning with examples from your reading, studies, observation, or "
    "experience."
)

REC = StimulusRecord(
    id="ACC-W910-MP-PERSP-0002",
    grade="11", mode="argument", family="perspective_set", bucket="test",
    form="4trait", topic_id="privacy_safety",
    modeling_anchor="ACT Writing 3-perspective",
    acc_tags=["ACC.W.ARG.2", "CCSS.W.11-12.1"],
    prompt=PROMPT,
    passages=[],
    perspectives=list(PERSPECTIVES),
    fact_sources=[],
    annotated=False,
    provenance={"copyright": "own_authored", "rights": "original prompt", "authored": "2026-07-09"},
)

if __name__ == "__main__":
    qc = qc_stimulus(REC); print(qc_report(REC)); import sys; sys.exit(0 if qc["passed"] else 1)
