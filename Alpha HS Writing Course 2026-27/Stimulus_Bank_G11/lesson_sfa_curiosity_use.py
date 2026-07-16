"""
Source-free ARGUMENT stimulus for the G11 writing course (LESSON bucket, annotatable).
Shape: AP English Language Q3 (a general, source-free prompt; the student argues from OWN knowledge, with
NO provided passage and NO fact table). This is the TEACHING version used by the G11 course-map source-free
unit (U4: L17 intro, L18 guided) so the cold TEST source-free prompts (sfa_ambition_contentment,
sfa_individual_community, sfa_tradition_progress) are NOT burned as worked examples before the gate. Topic
(curiosity vs. usefulness) is DISTINCT from every cold test topic. family=prompt_only, mode=argument.
Source-free family: no external fact table required. G11 academic register. No em dashes. Self-QC on run.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, qc_stimulus, qc_report

PROMPT = (
    "The educator Abraham Flexner argued that much of the knowledge that later proved most useful began as "
    "pure curiosity, pursued by people who had no practical end in view and no way to foresee where their "
    "questions would lead. Others counter that a society facing urgent problems cannot afford open-ended "
    "inquiry, and that learning and research should be directed toward needs a community can actually name.\n\n"
    "Carefully consider the tension between knowledge pursued for its own sake and knowledge pursued for a "
    "practical purpose. Then write an essay in which you develop a position on whether a society should "
    "support inquiry that has no foreseeable use. Argue a position using specific examples drawn from your "
    "reading, studies, observation, or experience."
)

REC = StimulusRecord(
    id="ACC-W1112-SFA-LESSON-0001",
    grade="11", mode="argument", family="prompt_only", bucket="lesson",
    topic_id="curiosity_usefulness",
    modeling_anchor="AP Lang Q3 argument (teaching version)",
    acc_tags=["ACC.W.ARG.1", "CCSS.W.11-12.1"],
    prompt=PROMPT,
    passages=[],
    fact_sources=[],
    annotated=True,
    provenance={"copyright": "own_authored", "rights": "original prompt", "authored": "2026-07-10",
                "note": "LESSON-bucket teaching version for G11 U4; topic distinct from all cold test "
                        "source-free prompts so the source-free gate is not pre-exposed."},
)

if __name__ == "__main__":
    qc = qc_stimulus(REC); print(qc_report(REC)); import sys; sys.exit(0 if qc["passed"] else 1)
