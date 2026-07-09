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
    "Machines and software now perform work that once required human hands and human judgment, from "
    "assembling goods to drafting documents and diagnosing problems. As automation spreads into more "
    "fields, people disagree about what human work is still for and how much its value depends on being "
    "done by a person. Given the accelerating capabilities of machines, it is worth examining the value "
    "of human work in an automated age."
)

PERSPECTIVES = [
    ("Automation frees people from drudgery and dangerous labor. When machines take over repetitive or "
     "hazardous tasks, human beings are released to do more creative, meaningful, and safer work, and the "
     "value of human effort rises rather than falls."),
    ("Work is not only a way to produce goods; it is a source of dignity, purpose, and belonging. When "
     "machines displace workers faster than new roles appear, people lose more than income, so the value of "
     "human work cannot be measured by output alone."),
    ("What a machine can do and what a person should do are different questions. Even as automation grows, "
     "some work, such as caring for others, exercising judgment, and taking responsibility, gains value "
     "precisely because it is done by a human being who can be trusted and held accountable."),
]

PROMPT = (
    "Read and carefully consider the perspectives below. Each suggests a particular way of thinking about "
    "the value of human work as machines advance.\n\n"
    "Perspective One: " + PERSPECTIVES[0] + "\n\n"
    "Perspective Two: " + PERSPECTIVES[1] + "\n\n"
    "Perspective Three: " + PERSPECTIVES[2] + "\n\n"
    "Write a unified, coherent essay about the value of human work in an automated age. In your essay, be "
    "sure to evaluate the three perspectives given, develop and support your own perspective on the issue, "
    "and analyze the relationship between your perspective and at least one other perspective. You may "
    "agree with any of the perspectives, disagree with all of them, or stake out a position of your own. "
    "Support your reasoning with examples from your reading, studies, observation, or experience."
)

REC = StimulusRecord(
    id="ACC-W910-MP-PERSP-0001",
    grade="11", mode="argument", family="perspective_set", bucket="test",
    form="4trait", topic_id="automation_work",
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
