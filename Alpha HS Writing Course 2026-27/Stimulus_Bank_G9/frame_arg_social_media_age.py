"""
frame_arg_social_media_age.py  -  ISSUE FRAME (lesson-bucket) for the "verify social media users' ages" debate.

Short own-authored 2-sided framing bound to CLAIM-TIER (T2) lesson slots. family=issue_frame (floor/Lexile-band
exempt by design, like the phone_ban/four_day_week frames). Own words, no fabricated figures, no copyrighted
text, no em dashes. Qualitative two-sided framing only; a full fact-sourced source (FTC / Surgeon General public
advisories) is a separate U2 evidence-lesson build. Runs the QC harness on execution (issue_frame exempt).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, qc_stimulus, qc_report

FRAME = (
"The debate: should social media apps be required to check how old their users are? "
"Lawmakers in several places have proposed rules like this, so the debate is real. People who support age "
"checks say young kids can end up on apps built for adults. There they may see harmful posts or get messages "
"from strangers, and a real age check would help keep them out. People who are against it say the checks often "
"mean handing over an ID or a face scan. That puts everyone's private information at risk, and determined kids "
"can often get around the checks anyway. Both sides want to keep young users safe. They disagree on whether "
"age checks would do more good than harm. Decide which case you find more convincing, and pick one reason."
)

REC = StimulusRecord(
    id="ACC-W910-FRAME-SOCIALMEDIAAGE",
    grade="9", mode="argument", family="issue_frame", bucket="lesson",
    topic_id="verify_social_media_age",
    annotated=False,
    modeling_anchor="claim-task issue frame (short 2-sided framing for a T2 claim lesson)",
    acc_tags=["ACC.W.ARG.1", "CCSS.W.9-10.1a"],
    prompt=("Should social media apps be required to verify their users' ages? Take a side and write one arguable "
            "claim with a reason."),
    passages=[Passage(title="The debate: checking ages on social media",
                      angle="two-sided framing (for and against required age checks)", text=FRAME)],
    fact_sources=[],
    provenance={"copyright": "own_authored", "rights": "own-words framing", "authored": "2026-07-14",
                "note": ("Short claim-task framing (topic slate). Qualitative two-sided framing only; no figures. "
                         "Full fact-sourced source (FTC / Surgeon General public advisories) is a separate U2 "
                         "evidence-lesson build. issue_frame family = floor/Lexile-band exempt.")},
)

if __name__ == "__main__":
    qc = qc_stimulus(REC)
    import re
    print(f"  frame word count: {len(re.findall(r'[A-Za-z]+', FRAME))}")
    print(qc_report(REC))
    sys.exit(0)
