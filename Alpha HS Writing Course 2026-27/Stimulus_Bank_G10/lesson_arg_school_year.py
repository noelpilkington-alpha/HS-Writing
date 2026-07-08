"""
Opposing-pair ARGUMENT stimulus for the G10 writing course (LESSON bucket).
Topic: Should the United States adopt a longer school year?
Family=opposing, mode=argument, bucket=lesson. Two original G10-register passages (~550-650 words each,
~1080-1130L), each conceding the other side. Figures trace to US federal public-domain sources (US Dept.
of Education / NCES, US BLS). Decomposes into two stance-tagged lesson singles under prop_longer_school_year.
No em dashes in prose. Runs itself through the QC harness.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

PASSAGE_A = (
"For most of American history, the school calendar was built around farming. It was not built around "
"learning. Children were needed in the fields during the summer. So schools closed for the warmest months. "
"That long summer break survived. It lasted long after the farms that created it were gone. Supporters of "
"a longer school year say it is time to question this old schedule. It was designed for a country that no "
"longer exists. A longer year, they believe, would give students more time to learn. It would give them "
"more time to master hard material. It would also give a fairer start to the children who need school the "
"most.\n\n"
"The National Center for Education Statistics reports a clear number. A typical American public school runs "
"about 180 days each year. Many high-performing countries run longer calendars. Supporters point out a "
"simple result. More days in the building means more days of instruction. It means more practice and more "
"feedback. Think about a skill a student almost masters in June. It is easier to finish that skill in July. "
"It is much harder to rebuild it in September after months away.\n\n"
"That gap over the summer is the heart of the argument. Researchers have long described a summer slide. In "
"a summer slide, students forget part of what they learned. Supporters argue the slide hits some students "
"hardest. Students from low-income families may not have books, camps, or tutoring over the break. "
"Wealthier families often fill the summer with enrichment. That enrichment keeps learning alive. Other "
"children lose ground through no fault of their own. A longer school year would narrow that gap. It would "
"keep every student engaged, not just the ones whose families can pay.\n\n"
"There is a practical benefit for families too. School lets out for the summer. Then working parents must "
"suddenly find weeks of childcare. Childcare is expensive and hard to arrange. A longer school year would "
"shrink that scramble. It would give students a safe, structured place during more of the year.\n\n"
"Supporters also point to how uneven the current summer really is across the country. Some students spend "
"those months in enriching programs that keep their reading and math sharp. Others spend the same months "
"with almost nothing structured to do at all. By the first week of fall, those two groups return to the "
"same classroom at very different levels. Teachers then lose weeks reviewing old material before the new "
"year can truly begin. A longer, more balanced calendar would shrink those long gaps and make each fall "
"restart far less painful for everyone in the room.\n\n"
"Supporters do not pretend the change is free. More school days cost money, and teachers and students "
"would give up part of a break they genuinely value. But the country already pays for the summer slide "
"every single year. It simply pays quietly, in the lost learning that schools must rebuild each fall. "
"Supporters believe there is a wiser way to spend that same effort. The country could invest it in new "
"learning instead of in relearning what students forgot over a long break. If school is truly the place "
"where children learn the most, they ask, why do we send them away from it for a full quarter of the year?"
)

PASSAGE_B = (
"A longer school year sounds like a simple fix. Add more days. Get more learning. But critics argue the "
"promise is thinner than it looks. The costs, they say, land hardest on the people schools depend on most. "
"Their first point is straightforward. More time in a seat is not the same as more learning. Picture a "
"tired student in a hot classroom in late July. That student is not absorbing more than a rested student "
"in May. What matters is the quality of the time, not just the amount. Simply extending a calendar does "
"nothing to make the teaching inside it better.\n\n"
"Then there is the price. Running schools longer costs real money. The Bureau of Labor Statistics reports "
"that teachers are salaried professionals. Asking them to work more weeks means paying them more. There is "
"also the cost of running buildings, buses, and air conditioning deeper into the summer. Critics raise a "
"warning. A district with a tight budget might add days without adding pay. It might add days without "
"adding support. That is a fast way to burn out the teachers a school cannot afford to lose.\n\n"
"Critics also defend the summer itself. A long break is not simply wasted time. Students rest during it. "
"They work summer jobs. They care for younger siblings. They attend camps. They explore interests that a "
"packed calendar leaves no room for. Teachers use the break to recover from a hard year. They also use it "
"to prepare for the next one. Shortening that break could leave students and teachers more drained, not "
"more ready.\n\n"
"There is also a fairness point that cuts the other way. Older students often rely on summer jobs. They "
"save that money or use it to help their families. A longer school year could take those weeks away. It "
"could take that income from the very students who need it most.\n\n"
"Critics add that a longer calendar could crowd out learning that does not happen inside a classroom. Many "
"students grow the most during summer through jobs, travel, family responsibilities, and hobbies they "
"choose themselves. A teenager who runs a summer job learns about money, responsibility, and the working "
"world in ways no worksheet can teach. Critics worry that a longer school year treats all of that valuable "
"experience as if it were wasted time. In their view, a good education includes room to live and grow "
"outside the school building, not only more hours seated within it.\n\n"
"None of this means the summer slide is imaginary. Critics agree that some students lose ground over the "
"long break, and they agree the gap between richer and poorer students is a serious problem worth solving. "
"But they argue for a more careful answer than simply adding days. A country could aim its resources where "
"they are actually needed, through strong summer programs built for the students who benefit most. It does "
"not have to lengthen the year for everyone at enormous cost. Before adding weeks to the calendar, critics "
"say, a country should first make sure the many days it already has are being used well."
)

FACTS = [
    FactSource("Typical US public school year length", "about 180 days",
               "US Dept. of Education / National Center for Education Statistics",
               "https://nces.ed.gov/fastfacts/display.asp?id=52"),
    FactSource("Teachers are salaried professionals (longer year raises labor cost)", "salaried",
               "US Bureau of Labor Statistics (Occupational Outlook Handbook)",
               "https://www.bls.gov/ooh/education-training-and-library/high-school-teachers.htm"),
    FactSource("Summer learning loss (summer slide) affects students over the long break", "summer slide",
               "US Dept. of Education", "https://ies.ed.gov/ncee/"),
]

rec = StimulusRecord(
    id="ACC-W910-ARG-OPP-LESSON-SCHOOLYEAR",
    grade="9-10", mode="argument", family="opposing", bucket="lesson",
    topic_id="longer_school_year",
    modeling_anchor="Ohio ELA II / MD MCAP (opposing-view pick-a-side)",
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "CCSS.W.9-10.1"],
    prompt=("Weighing both sources, write an argumentative essay stating your position on whether the United "
            "States should adopt a longer school year. Support your claim with evidence from both sources, "
            "and respond to at least one objection from the side you do not take."),
    passages=[
        Passage(title="More Days, More Learning: The Case for a Longer School Year",
                angle="pro; NCES calendar data and the summer-slide equity argument", text=PASSAGE_A),
        Passage(title="Longer Is Not the Same as Better",
                angle="con; BLS labor-cost and quality-over-quantity argument", text=PASSAGE_B),
    ],
    fact_sources=FACTS,
    provenance={"copyright": "own_authored", "rights": "public-domain-sourced (US DoEd/NCES/BLS)",
                "authored": "2026-07-08"},
)

SINGLES = [
    StimulusRecord(
        id="ACC-W910-ARG-SINGLE-SCHOOLYEAR-PRO", grade="9-10", mode="argument", family="single", bucket="lesson",
        modeling_anchor=rec.modeling_anchor, acc_tags=list(rec.acc_tags),
        prompt="Read this source arguing in favor of a longer school year.",
        passages=[Passage(title=rec.passages[0].title, angle=rec.passages[0].angle, text=PASSAGE_A)],
        fact_sources=list(rec.fact_sources), provenance=dict(rec.provenance),
        topic_id="longer_school_year", proposition_id="prop_longer_school_year", stance="pro",
        form="staar", task_demand=3),
    StimulusRecord(
        id="ACC-W910-ARG-SINGLE-SCHOOLYEAR-CON", grade="9-10", mode="argument", family="single", bucket="lesson",
        modeling_anchor=rec.modeling_anchor, acc_tags=list(rec.acc_tags),
        prompt="Read this source arguing against a longer school year.",
        passages=[Passage(title=rec.passages[1].title, angle=rec.passages[1].angle, text=PASSAGE_B)],
        fact_sources=list(rec.fact_sources), provenance=dict(rec.provenance),
        topic_id="longer_school_year", proposition_id="prop_longer_school_year", stance="con",
        form="staar", task_demand=3),
]

if __name__ == "__main__":
    import re
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
    import readability_gate as rg
    qc_stimulus(rec)
    for p in rec.passages:
        wc = len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", p.text))
        lex = rg.analyze_text(p.text)["lexile_estimate"]
        print(f"passage '{p.title[:40]}': {wc} words, ~{lex}L")
    print(qc_report(rec))
    assert len(SINGLES) == 2 and {x.stance for x in SINGLES} == {"pro", "con"}
    for x in SINGLES:
        qc_stimulus(x)
        assert x.qc["passed"], f"single {x.id} failed: {x.qc.get('first_failure')}"
    print("SINGLES decomposition OK")
    sys.exit(0 if rec.qc["passed"] else 1)
