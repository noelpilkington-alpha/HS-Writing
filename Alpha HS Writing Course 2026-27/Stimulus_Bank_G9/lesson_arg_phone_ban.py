"""
Single-source ARGUMENT stimulus for the G9 (English I band) writing course (LESSON bucket).
Topic: Should phones be banned during the school day?
grade=9, mode=argument, family=single, bucket=lesson. One original G9-register passage (~520-620 words,
targeted 1010-1150L) presenting the issue with evidence on both sides so the student can argue a position.
Figures trace to US federal public-domain sources (US Dept. of Education / NCES). No em dashes / en dashes
in prose. Runs itself through the QC harness and exits on the verdict.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

PASSAGE = (
"Walk into an American high school today, and you will notice phones almost everywhere you look. Students "
"check them between classes, at lunch, and sometimes in the middle of an important lesson. School leaders "
"have argued about these powerful devices for years, and many districts have finally decided to act. The "
"National Center for Education Statistics reports that in the 2019 to 2020 school year, about 76.9 percent "
"of public schools prohibited students from using cell phones for non-academic reasons during the school "
"day. That figure represents more than three out of every four schools nationwide. Now some people want to "
"go further and ban phones from the entire school day.\n\n"
"The rules governing phones have not always been this strict, and they certainly have not stayed the same "
"over time. That same federal source shows that back in the 2009 to 2010 school year, roughly 90.9 percent "
"of schools enforced such a rule. Only a few years later, in the 2015 to 2016 school year, that share had "
"tumbled to just 65.8 percent before it eventually climbed upward again. This constant back-and-forth "
"reveals that schools are still searching for the right approach, which means the debate remains far from "
"settled.\n\n"
"Those who want a full ban make a clear case. Their main point is focus. A phone that buzzes with a new "
"message pulls a student's mind away from the lesson. Even a phone sitting face down on a desk can tempt "
"a student to check it. When phones go away, supporters say, students pay more attention and talk to each "
"other more. A ban can also cut down on cheating, since a hidden phone can hold answers or take pictures "
"of a test.\n\n"
"Supporters point to a second benefit as well. Phones can be tools for cruelty. A student can use one to "
"take an embarrassing photo or to spread a mean message in seconds. If phones are locked away during the "
"day, that kind of bullying gets harder. School, they argue, should be a break from the screen, not "
"another place ruled by it.\n\n"
"Others push back. Their first worry is safety. In an emergency, a parent may want to reach a child right "
"away, and a student may need to call for help. A full ban, critics say, could cut off that lifeline at "
"the worst moment. Many families feel safer knowing their child carries a phone.\n\n"
"Critics raise a second point about learning to choose. A phone is a tool students will use for the rest "
"of their lives. If schools simply lock phones away, critics argue, students never learn to manage the "
"device on their own. It might be wiser to teach smart habits than to ban the phone outright. A student "
"who learns to silence a phone and set it aside gains a skill that lasts.\n\n"
"Both sides want the same thing in the end. They want a school where students can focus, stay safe, and "
"treat one another well. They simply disagree about how to get there. Should a school ban phones for the "
"whole day to protect attention and cut down on harm? Or should it allow phones with limits and teach "
"students to use them wisely? That is the question you must now decide."
)

FACTS = [
    FactSource("Public schools prohibiting non-academic cell phone use, 2019-20", "76.9 percent",
               "US Dept. of Education / National Center for Education Statistics (Digest tbl 233.50)",
               "https://nces.ed.gov/programs/digest/d21/tables/dt21_233.50.asp",
               verbatim="Prohibited non-academic use of cell phones or smartphones during school hours ... 76.9"),
    FactSource("Public schools prohibiting cell phone use, 2009-10", "90.9 percent",
               "US Dept. of Education / National Center for Education Statistics (Digest tbl 233.50)",
               "https://nces.ed.gov/programs/digest/d21/tables/dt21_233.50.asp",
               verbatim="2009-10 ... 90.9"),
    FactSource("Public schools prohibiting cell phone use, 2015-16", "65.8 percent",
               "US Dept. of Education / National Center for Education Statistics (Digest tbl 233.50)",
               "https://nces.ed.gov/programs/digest/d21/tables/dt21_233.50.asp",
               verbatim="2015-16 ... 65.8"),
]

REC = StimulusRecord(
    id="ACC-W910-ARG-LESSON-PHONEBAN",
    grade="9", mode="argument", family="single", bucket="lesson",
    topic_id="phone_ban_school_day",
    modeling_anchor="STAAR English I argumentative ECR",
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "ACC.W.SRC.3", "CCSS.W.9-10.1"],
    prompt=("Read the source about phones in school. Then write an argumentative essay stating your "
            "position on whether phones should be banned during the school day. Support your claim with "
            "evidence from the source, and respond to at least one objection from the side you do not take."),
    passages=[
        Passage(title="Phones in School: Ban Them or Teach With Them?",
                angle="issue-presenting single source; NCES public-school phone-policy data", text=PASSAGE),
    ],
    fact_sources=FACTS,
    provenance={"copyright": "own_authored", "rights": "public-domain-sourced (US federal)",
                "authored": "2026-07-08"},
)

if __name__ == "__main__":
    import re
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
    import readability_gate as rg
    for p in REC.passages:
        wc = len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", p.text))
        lex = rg.analyze_text(p.text)["lexile_estimate"]
        print(f"passage '{p.title[:40]}': {wc} words, ~{lex}L")
    qc = qc_stimulus(REC); print(qc_report(REC)); import sys; sys.exit(0 if qc["passed"] else 1)
