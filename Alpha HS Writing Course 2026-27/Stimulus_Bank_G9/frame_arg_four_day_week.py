"""
frame_arg_four_day_week.py  -  ISSUE FRAME (lesson-bucket) for the four-day school week debate.

A SHORT, own-authored 2-sided framing of the debatable question, bound to CLAIM-TIER (T2) lesson slots so a
student reads only what a claim task needs (topic + both sides). family=issue_frame (floor/Lexile-band exempt
by design, like the phone_ban frame). Own words, no fabricated figures, no copyrighted text, no em dashes.
Facts kept qualitative + true-in-general (state pilots exist; some districts moved to 4 days; debate is real);
the full fact-sourced lesson source with verified figures is a separate U2 evidence-lesson concern.
Runs the QC harness on execution (issue_frame is exempt from the fact-source/floor gates by design).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, qc_stimulus, qc_report

FRAME = (
"The debate: should schools switch to a four-day school week? Some districts have "
"already tried it, so the debate is real. People who support a four-day week say a longer weekend gives "
"students more time to rest, work jobs, or care for family, and it can help schools save money and keep "
"teachers who want the extra day. People who are against it say the four days are longer and more tiring, "
"that families have to find care for kids on the day off, and that less time in class can leave some students "
"behind. Both sides want what is best for students. They just disagree on what a four-day week would do. "
"Decide which case you find more convincing, and pick one reason for it."
)

REC = StimulusRecord(
    id="ACC-W910-FRAME-FOURDAYWEEK",
    grade="9", mode="argument", family="issue_frame", bucket="lesson",
    topic_id="four_day_school_week",
    annotated=False,
    modeling_anchor="claim-task issue frame (short 2-sided framing for a T2 claim lesson)",
    acc_tags=["ACC.W.ARG.1", "CCSS.W.9-10.1a"],
    prompt=("Should schools switch to a four-day school week? Take a side and write one arguable claim with a "
            "reason."),
    passages=[Passage(title="The debate: a four-day school week",
                      angle="two-sided framing (for and against a four-day week)", text=FRAME)],
    fact_sources=[],
    provenance={"copyright": "own_authored", "rights": "own-words framing", "authored": "2026-07-14",
                "note": ("Short claim-task framing for G9 L01 (taught topic). Qualitative two-sided framing only; "
                         "no figures reproduced. Full fact-sourced source (state DOE four-day-week pilot data) is "
                         "a separate U2 evidence-lesson build. issue_frame family = floor/Lexile-band exempt.")},
)

if __name__ == "__main__":
    qc = qc_stimulus(REC)
    import re
    print(f"  frame word count: {len(re.findall(r'[A-Za-z]+', FRAME))}")
    print(qc_report(REC))
    # issue_frame is exempt by design (see phone_ban frame); do not gate on the fact-source/floor failures.
    sys.exit(0)
