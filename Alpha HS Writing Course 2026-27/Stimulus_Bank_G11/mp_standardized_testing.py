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
    "Schools and colleges have long relied on standardized tests to measure what students know and to "
    "compare applicants on a common scale. Supporters see these exams as an objective yardstick, while "
    "critics argue that they narrow what gets taught and reward the advantages some students already hold. "
    "As institutions reconsider how they evaluate learning, it is worth examining the role standardized "
    "testing should play in education."
)

PERSPECTIVES = [
    ("Standardized tests provide a fair, common measure. Because every student answers the same questions "
     "under the same conditions, the results let schools identify who needs help and let colleges compare "
     "applicants from very different backgrounds on a single scale."),
    ("Tests distort the purpose of education. When scores carry high stakes, teaching narrows to what the "
     "exam rewards, curiosity gives way to drilling, and rich learning that cannot be captured in a bubble "
     "sheet is pushed aside."),
    ("A single test cannot capture a whole student. Standardized exams measure certain skills at one moment, "
     "so their scores are most useful as one piece of evidence among many, alongside coursework, projects, "
     "and teacher judgment, rather than as the final word."),
]

PROMPT = (
    "Read and carefully consider the perspectives below. Each suggests a particular way of thinking about "
    "the role of standardized testing in education.\n\n"
    "Perspective One: " + PERSPECTIVES[0] + "\n\n"
    "Perspective Two: " + PERSPECTIVES[1] + "\n\n"
    "Perspective Three: " + PERSPECTIVES[2] + "\n\n"
    "Write a unified, coherent essay about the role of standardized testing in education. In your essay, be "
    "sure to evaluate the three perspectives given, develop and support your own perspective on the issue, "
    "and analyze the relationship between your perspective and at least one other perspective. You may agree "
    "with any of the perspectives, disagree with all of them, or stake out a position of your own. Support "
    "your reasoning with examples from your reading, studies, observation, or experience."
)

REC = StimulusRecord(
    id="ACC-W910-MP-PERSP-0003",
    grade="11", mode="argument", family="perspective_set", bucket="test",
    form="4trait", topic_id="standardized_testing",
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
