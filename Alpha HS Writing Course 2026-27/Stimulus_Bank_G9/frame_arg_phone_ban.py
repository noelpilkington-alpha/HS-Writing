"""
frame_arg_phone_ban.py  -  ISSUE FRAME (lesson-bucket) for the phones-in-school debate.

A SHORT, own-authored 2-sided framing of the debatable question, bound to CLAIM-TIER (T2) lesson slots so a
student reads only what a claim task needs (topic + both sides), not the full 539-word source. family=
issue_frame (floor/Lexile-band exempt by design). Faithful paraphrase of the arguments in the full source
ACC-W910-ARG-LESSON-PHONEBAN (lesson_arg_phone_ban.py), which remains the provenance anchor + the source the
G9 U2 evidence lessons bind. Own words, no fabricated figures, no copyrighted text, no em dashes.
Runs the QC harness on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, qc_stimulus, qc_report

FRAME = (
"The debate: should schools ban phones for the whole school day? Both sides have a "
"case. Those who support a full-day ban say phones pull attention away from learning, since even a phone "
"sitting face-down on a desk tempts a student to check it, and a ban can cut down on cheating and help "
"students talk to each other more. Those who are against a full ban say students should learn to manage "
"phones responsibly rather than simply have them taken away, because they will use phones for the rest of "
"their lives, and that phones can be useful for schoolwork and reaching family. That is enough to take a "
"side. Decide which case you find more convincing, and pick one reason for it."
)

REC = StimulusRecord(
    id="ACC-W910-FRAME-PHONEBAN",
    grade="9", mode="argument", family="issue_frame", bucket="lesson",
    topic_id="phone_ban_school_day",
    annotated=False,
    modeling_anchor="claim-task issue frame (short 2-sided framing for a T2 claim lesson)",
    acc_tags=["ACC.W.ARG.1", "CCSS.W.9-10.1a"],
    prompt=("Should schools ban phones for the entire school day? Take a side and write one arguable claim "
            "with a reason."),
    passages=[Passage(title="The debate: phones in school",
                      angle="two-sided framing (for and against a full-day ban)", text=FRAME)],
    fact_sources=[],
    provenance={"copyright": "own_authored", "rights": "own-words framing of an own-authored source",
                "authored": "2026-07-12",
                "note": ("Short claim-task framing; faithful paraphrase of the two sides in the full source "
                         "ACC-W910-ARG-LESSON-PHONEBAN (which holds the verified federal figures + is bound by "
                         "the evidence lessons). Qualitative only; no figures reproduced here.")},
)

if __name__ == "__main__":
    qc = qc_stimulus(REC)
    import re
    print(f"  frame word count: {len(re.findall(r'[A-Za-z]+', FRAME))}")
    print(qc_report(REC))
    sys.exit(0 if qc["passed"] else 1)
