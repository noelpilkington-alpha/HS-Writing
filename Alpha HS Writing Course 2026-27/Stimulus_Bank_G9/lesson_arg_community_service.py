"""
Single-source ARGUMENT stimulus for the G9 (English I band) writing course (LESSON bucket).
Topic: Should community service be a graduation requirement?
grade=9, mode=argument, family=single, bucket=lesson. One original G9-register passage (~520-620 words,
targeted 1010-1150L) presenting the issue with evidence on both sides so the student can argue a position.
Figures trace to US federal public-domain sources (US Dept. of Education / NCES). No em dashes / en dashes
in prose. Runs itself through the QC harness and exits on the verdict.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

PASSAGE = (
"Across the country, many students already give their time to help others. They tutor younger children. "
"They clean up parks. They serve meals at shelters. This kind of unpaid work is called community service. "
"The National Center for Education Statistics ran a federal survey on it. The survey found that 64 percent "
"of all public schools had students doing community service. Among high schools, that share rose to 83 "
"percent. So service is already a common part of school life. The harder question is different. Should a "
"student be required to do it in order to graduate?\n\n"
"Service is common, but a formal program is not. The same survey looked at service-learning. That is a "
"program that ties the volunteer work to classroom lessons. Only 32 percent of public schools ran such a "
"program. Among high schools, the figure reached 46 percent. So most schools encourage service. Far fewer "
"build it into the official course of study. A graduation rule would change that. It would turn service "
"from a choice into a must.\n\n"
"Supporters of a requirement say the change would help students and towns alike. Their first point is "
"about character. Picture a student who spends an afternoon at a food bank. That student learns "
"responsibility. That student sees the needs of neighbors up close. A textbook cannot teach those lessons "
"as well. A rule, supporters say, makes sure every graduate has at least tried to give back.\n\n"
"Supporters offer a second point about fairness. Right now, the students most likely to volunteer already "
"get a push at home. A student without that push may never start. A requirement would open the door for "
"everyone. Then the habit of service would not depend on a family's background. That shared duty, "
"supporters believe, makes a school stronger and more united.\n\n"
"Critics see the matter in another way. Their main point is simple. Forced service is not really service "
"at all. To volunteer means to choose to help freely. A school can demand the hours and threaten to hold "
"back a diploma. But then the act loses its meaning. A student who resents the hours may do the least "
"possible and learn nothing.\n\n"
"Critics raise a practical worry too. Students already juggle hard classes, jobs, and family duties. Think "
"of a teenager who works after school to help pay the bills. That student may have little time left for "
"required volunteering. For that student, the rule could feel less like a gift. It could feel like one "
"more burden on a full schedule.\n\n"
"Both sides value service. Both want young people to care about their communities. They disagree about one "
"thing: should a school force it? Should a school make community service a firm rule for graduation, so "
"every student takes part and no one is left out? Or should it keep service a choice, so the decision to "
"help stays real and students control their own time? That is the question you must now decide."
)

FACTS = [
    FactSource("Public schools with students participating in community service", "64 percent",
               "US Dept. of Education / National Center for Education Statistics (FRSS 1999)",
               "https://nces.ed.gov/surveys/frss/publications/1999043/index.asp?sectionid=4",
               verbatim="64 percent of all public schools"),
    FactSource("High schools with students participating in community service", "83 percent",
               "US Dept. of Education / National Center for Education Statistics (FRSS 1999)",
               "https://nces.ed.gov/surveys/frss/publications/1999043/index.asp?sectionid=4",
               verbatim="high schools ... 83 percent"),
    FactSource("Public schools organizing service-learning", "32 percent",
               "US Dept. of Education / National Center for Education Statistics (FRSS 1999)",
               "https://nces.ed.gov/surveys/frss/publications/1999043/index.asp?sectionid=5",
               verbatim="percentage of public schools nationwide with service-learning was 32 percent"),
    FactSource("High schools with students participating in service-learning", "46 percent",
               "US Dept. of Education / National Center for Education Statistics (FRSS 1999)",
               "https://nces.ed.gov/surveys/frss/publications/1999043/index.asp?sectionid=5",
               verbatim="46 percent of all high schools had students participating in service-learning"),
]

REC = StimulusRecord(
    id="ACC-W910-ARG-LESSON-COMMUNITYSERVICE",
    grade="9", mode="argument", family="single", bucket="lesson",
    topic_id="community_service_requirement",
    modeling_anchor="STAAR English I argumentative ECR",
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "ACC.W.SRC.3", "CCSS.W.9-10.1"],
    prompt=("Read the source about community service in schools. Then write an argumentative essay stating "
            "your position on whether community service should be a graduation requirement. Support your "
            "claim with evidence from the source, and respond to at least one objection from the side you "
            "do not take."),
    passages=[
        Passage(title="Required to Give Back? Community Service and the Diploma",
                angle="issue-presenting single source; NCES community-service and service-learning data", text=PASSAGE),
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
