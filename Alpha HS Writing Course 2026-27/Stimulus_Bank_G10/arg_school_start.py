"""
Opposing-pair argument stimulus: Should public high schools start the school day later
(no earlier than 8:30 a.m.)? Family=opposing, mode=argument. G10 register.

Every figure is drawn from a federal page fetched live 2026-07-07 via the pipeline's
resolve_source.fetch_with_fallback:
  PRO side (later start / health):  US CDC (adolescent sleep need) + US CDC & US Dept. of
                                    Education (2015 MMWR school-start-time report).
  CON side (costs / logistics):     US BLS (employment characteristics of families, 2025)
                                    + US NCES / US Dept. of Education (student-transportation cost).
>=2 distinct source orgs; both passages concede the other side. No em dashes in prose.

Runs itself through the QC harness and reports.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# ---------------------------------------------------------------------------
# PASSAGE A  -  pro-later-start (CDC adolescent-sleep + CDC/DoEd start-time data)
# ---------------------------------------------------------------------------
PASSAGE_A = (
"Ask a tired teenager why the first period of the day feels like a fog, and the honest answer is "
"often the simplest one: not enough sleep. The science behind that complaint is clear. The Centers "
"for Disease Control and Prevention reports that teenagers between the ages of 13 and 17 need 8 to 10 "
"hours of sleep each night for healthy growth, steady focus, and stable mood. Yet most American "
"teenagers fall well short of that target. According to federal survey data reported by the CDC, "
"about two out of three high school students fail to get enough sleep on a school night. Supporters "
"of a later start time argue that the school clock itself is a large part of the problem, and that "
"moving the first bell would help fix it.\n\n"

"The numbers on when school begins are striking. Drawing on a national survey of nearly 40,000 public "
"schools, researchers at the CDC and the U.S. Department of Education found that the average school "
"start time was 8:03 a.m. Fewer than one in five middle and high schools began the day at 8:30 a.m. or "
"later. In 42 states, most public schools started before 8:30. For a student who must catch a bus "
"before sunrise, an early bell can mean waking at an hour when the teenage body is still biologically "
"primed for sleep.\n\n"

"That biological point sits at the heart of the argument. During the teen years, the body's internal "
"clock shifts later, which makes it hard for many adolescents to fall asleep early even when they "
"honestly try. A first bell at 7:30 or 8:00 a.m. therefore collides with a natural rhythm that no "
"amount of willpower can simply override. This is why, in 2014, the American Academy of Pediatrics "
"urged middle and high schools to set start times no earlier than 8:30 a.m. The aim was not to hand "
"students a lazy morning. It was to line the school day up with the sleep that health experts say "
"adolescents genuinely require.\n\n"

"The benefits, supporters say, reach well beyond simply feeling rested. Insufficient sleep among "
"teenagers has been tied to weaker academic performance and to a range of health risks, from injuries "
"to mood problems. A student who arrives at school exhausted is not in a strong position to read a "
"difficult text, solve a hard problem, or drive safely home in the afternoon. If the school day is "
"meant to help young people learn, then the hours of that day ought to fit the biology of the people "
"sitting in the seats.\n\n"

"Supporters of a later start do not pretend the change is free or easy. Shifting the first bell "
"ripples out to bus routes, after-school jobs, sports practice, and the schedules of working parents, "
"and those are real costs that districts must weigh with care. But they argue that the health of "
"students belongs at the center of the decision, not at its edges. A school system exists to help "
"young people learn, and a growing body of federal evidence suggests that a well-rested student is a "
"student better able to learn. If the average school in the country still begins before the hour that "
"pediatricians recommend, then the current schedule, supporters contend, was built around buses and "
"long habit rather than around the students it is supposed to serve. Starting the day a little later, "
"in this view, is one of the rare reforms that could lift both health and learning at the same time."
)

# ---------------------------------------------------------------------------
# PASSAGE B  -  against a mandate (BLS working-family + NCES/DoEd transport-cost data)
# ---------------------------------------------------------------------------
PASSAGE_B = (
"No one seriously disputes that teenagers need more sleep than they usually get. The health research "
"is real, and a later start time can genuinely help students who struggle to wake before sunrise. Yet "
"the school day does not exist on its own. It is tied to bus fleets, sports schedules, part-time jobs, "
"and, above all, to the working families who plan their lives around it. Critics of a forced later "
"start warn that a change that looks simple on paper can create serious problems in practice.\n\n"

"Start with transportation. Most districts cannot afford a separate bus for every school, so they run "
"one set of buses on a tiered schedule, carrying high school students on an early loop, then middle "
"schoolers, then the youngest children. Pushing the high school bell to 8:30 a.m. forces that entire "
"chain to shift, and often the cheapest fix is to make elementary students start earlier or wait "
"longer in the morning dark. Busing is already a heavy expense. The U.S. National Center for "
"Education Statistics reports that public schools spent about 1,152 dollars per student transported "
"in the 2018 to 2019 school year, and that roughly 51.4 percent of all students, about 24 million "
"children, ride to school at public expense. Buying more buses or hiring more drivers to protect a "
"tiered system can strain budgets that are already stretched thin.\n\n"

"Then there are the working families. A later release time can leave the after-school hours "
"unsupervised for younger children or push a teenager's job and practice deep into the evening. This "
"matters because most children live in homes where the adults work. The U.S. Bureau of Labor "
"Statistics reports that in 2025, both parents were employed in 66.3 percent of married-couple "
"families with children, and that 73.9 percent of mothers with children under 18 were in the labor "
"force. For these households, the morning bell is a fixed point around which jobs, childcare, and "
"commutes are all arranged. Move it, and the whole day has to be rebuilt.\n\n"

"Sports and activities add one more layer of difficulty. When the last bell rings later, practices, "
"games, rehearsals, and club meetings slide into the evening as well. Athletes end up finishing "
"outdoor practice in fading light, and students who work to help their families may lose the shifts "
"they count on. In districts that share fields, coaches, or buses across several schools, a single "
"change to the high school clock can throw the whole regional schedule out of order.\n\n"

"Critics of a mandated later start are not claiming that student sleep does not matter. They agree "
"that teenagers are chronically short on rest and that the health evidence deserves real respect. "
"Their point is narrower. A decision that touches bus budgets, working parents, and every family's "
"morning routine should be made carefully, district by district, rather than imposed as one rule for "
"the entire country. School start times are set locally for good reason, because the trade-offs look "
"different in a rural county with long bus rides than in a compact city where students walk. A later "
"bell may well prove worth its costs in some communities. But pretending those costs do not exist, "
"critics argue, is exactly how a well-meaning reform ends up harming the families it was meant to help."
)

rec = StimulusRecord(
    id="ACC-W910-ARG-OPP-0004",
    grade="9-10", mode="argument", family="opposing",
    modeling_anchor="Ohio ELA II / MD MCAP (opposing-view pick-a-side argument)",
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "ACC.W.ARG.5",
              "CCSS.W.9-10.1", "CCSS.W.9-10.1b", "TX-TEKS.EII.7.C"],
    prompt=("Weighing both sources, write an argumentative essay stating your position on whether public "
            "high schools should start the school day later, no earlier than 8:30 a.m. Support your claim "
            "with specific evidence from both sources and address at least one objection from the side you "
            "do not take."),
    passages=[
        Passage(title="The Case for a Later First Bell",
                angle="pro-later-start; US CDC adolescent-sleep need + US CDC/US Dept. of Education start-time data",
                text=PASSAGE_A),
        Passage(title="Why a Later Bell Is Harder Than It Sounds",
                angle="against a mandated later start; US BLS working-family data + US NCES/US Dept. of Education transportation-cost data",
                text=PASSAGE_B),
    ],
    fact_sources=[
        # ---- PRO side (health) ----
        FactSource("Teens 13-17 need 8-10 hours of sleep nightly", "8-10 hours", "US CDC",
                   "https://www.cdc.gov/sleep/about/index.html",
                   "Teen 13-17 years 8-10 hours"),
        FactSource("About two out of three high school students fail to get enough sleep", "2 out of 3", "US CDC",
                   "https://archive.cdc.gov/www_cdc_gov/media/releases/2015/p0806-school-sleep.html",
                   "The proportion of high school students who fail to get sufficient sleep (2 out of 3)"),
        FactSource("Average US school start time (2011-12 SASS)", "8:03 a.m.", "US CDC / US Dept. of Education",
                   "https://archive.cdc.gov/www_cdc_gov/media/releases/2015/p0806-school-sleep.html",
                   "The average start time was 8:03 AM."),
        FactSource("Fewer than 1 in 5 schools started at 8:30 or later; 42 states before 8:30",
                   "fewer than 1 in 5; 42 states", "US CDC / US Dept. of Education",
                   "https://archive.cdc.gov/www_cdc_gov/media/releases/2015/p0806-school-sleep.html",
                   "Fewer than 1 in 5 middle and high schools ... 42 states reported that 75-100 percent ... started before 8:30 AM."),
        FactSource("AAP (2014) urged start times no earlier than 8:30 a.m.", "8:30 a.m.", "US CDC",
                   "https://archive.cdc.gov/www_cdc_gov/media/releases/2015/p0806-school-sleep.html",
                   "the American Academy of Pediatrics issued a policy statement urging ... no earlier than 8:30 AM"),
        FactSource("Nearly 40,000 public schools reviewed", "40,000 schools", "US CDC / US Dept. of Education",
                   "https://archive.cdc.gov/www_cdc_gov/media/releases/2015/p0806-school-sleep.html",
                   "data from the 2011-2012 Schools and Staffing Survey of nearly 40,000 public middle, high, and combined schools"),
        # ---- CON side (cost / logistics) ----
        FactSource("Both parents employed in 66.3% of married-couple families with children (2025)",
                   "66.3 percent", "US BLS",
                   "https://www.bls.gov/news.release/famee.nr0.htm",
                   "in 66.3 percent of these families both parents were employed"),
        FactSource("Labor force participation of mothers with children under 18 (2025)", "73.9 percent", "US BLS",
                   "https://www.bls.gov/news.release/famee.nr0.htm",
                   "for all mothers with children under age 18 was 73.9 percent"),
        FactSource("Per-student transportation cost 2018-19", "1,152 dollars", "US NCES",
                   "https://nces.ed.gov/fastfacts/display.asp?id=67",
                   "$1,152 per student transported in 2018-19 (in unadjusted dollars)"),
        FactSource("Share/number of students transported at public expense 2018-19",
                   "51.4 percent; 24,245,000 (about 24 million)", "US NCES",
                   "https://nces.ed.gov/fastfacts/display.asp?id=67",
                   "2018-19  24,245,000 ... 51.4 (percent of total)"),
    ],
    provenance={"copyright": "own_authored",
                "rights": "public-domain-sourced (US CDC + US Dept. of Education + US BLS + US NCES)",
                "two_source_verified": True, "authored": "2026-07-07"},
)


# --- Two-bucket migration: decompose the opposing pair into stance-tagged TEST singles ---------
# One pro + one con member of proposition "prop_school_start". The pair above (rec) is retained for backward
# compatibility; the singles are what the composer assembles opposing pairs from. Each single carries the
# FULL fact_sources list (the anti-fabrication gate only requires the figures IN its passage to be covered;
# extra rows are harmless and guarantee the >=3 citable-fact minimum).
SINGLES = [
    StimulusRecord(
        id="ACC-W910-ARG-SINGLE-SCHOOL-START-PRO",
        grade="9-10", mode="argument", family="single", bucket="test",
        modeling_anchor=rec.modeling_anchor,
        acc_tags=list(rec.acc_tags),
        prompt="Read this source arguing in favor of the proposal.",
        passages=[Passage(title=rec.passages[0].title, angle=rec.passages[0].angle, text=rec.passages[0].text)],
        fact_sources=list(rec.fact_sources),
        provenance=dict(rec.provenance),
        topic_id="school_start", proposition_id="prop_school_start", stance="pro",
        form="staar", task_demand=3),
    StimulusRecord(
        id="ACC-W910-ARG-SINGLE-SCHOOL-START-CON",
        grade="9-10", mode="argument", family="single", bucket="test",
        modeling_anchor=rec.modeling_anchor,
        acc_tags=list(rec.acc_tags),
        prompt="Read this source arguing against the proposal.",
        passages=[Passage(title=rec.passages[1].title, angle=rec.passages[1].angle, text=rec.passages[1].text)],
        fact_sources=list(rec.fact_sources),
        provenance=dict(rec.provenance),
        topic_id="school_start", proposition_id="prop_school_start", stance="con",
        form="staar", task_demand=3),
]

if __name__ == "__main__":
    import re
    qc_stimulus(rec)
    for p in rec.passages:
        wc = len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", p.text))
        print(f"passage '{p.title}': {wc} words")
    print(qc_report(rec))
    # decomposed stance singles
    assert len(SINGLES) == 2 and {x.stance for x in SINGLES} == {"pro", "con"}
    for _x in SINGLES:
        assert _x.family == "single" and _x.bucket == "test" and _x.proposition_id and _x.topic_id and _x.form
        qc_stimulus(_x)
        assert _x.qc["passed"], f"single {_x.id} must pass QC: {_x.qc.get('first_failure')}"
    print("SINGLES decomposition OK")
    sys.exit(0 if rec.qc["passed"] else 1)
