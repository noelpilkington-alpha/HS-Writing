"""
Opposing-pair ARGUMENT stimulus for the G10 writing course (LESSON bucket).
Topic: Should the United States abolish daylight saving time (switch to permanent standard time)?
Family=opposing, mode=argument, bucket=lesson. Two original G10-register passages (~540-560 words each,
targeted to ~1080-1130L by writing at roughly 15 words per sentence), each conceding the other side.
Figures trace to US federal public-domain sources (US DOT, US CDC, US Dept. of Energy). Decomposes into
two stance-tagged lesson singles under prop_daylight_saving. No em dashes in prose. Runs the QC harness.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

PASSAGE_A = (
"Twice a year, almost every clock in America jumps by an hour, and millions of people lose sleep over it. "
"In the spring, we move the clocks forward and surrender an hour of rest. In the fall, we move them back "
"and the evenings turn dark far too soon. Supporters of ending this ritual argue that the twice-yearly "
"switch causes real harm for very little gain. They want the country to pick one clock and keep it, and "
"many of them favor permanent standard time, the setting that matches the natural position of the sun.\n\n"
"The strongest case rests on health. The Centers for Disease Control and Prevention has long warned that "
"most teenagers already fail to get the sleep their growing bodies need. When the clocks lurch forward in "
"spring, that shortage suddenly gets worse for everyone at once. Doctors point to a troubling pattern in "
"the days right after the change. Studies have linked the spring shift to a rise in car crashes and to "
"other health problems, because a population running on less sleep makes more mistakes.\n\n"
"Supporters argue that our bodies are built around the sun, not around a government clock. Sleep scientists "
"explain that morning light helps set the internal clock that governs alertness and rest. Standard time "
"keeps clock noon close to actual solar noon, so morning light arrives when the body expects it. Permanent "
"daylight saving time, by contrast, would push winter sunrises very late, leaving children waiting for the "
"school bus in the pitch dark. For that reason, most sleep experts favor permanent standard time as the "
"healthier of the two options.\n\n"
"There is a simplicity argument as well. The current system is confusing, and it quietly wastes time and "
"money twice a year. People forget to change their clocks and miss appointments or arrive an hour early. "
"Workers who cross the change groggy and distracted are less productive for days. A single steady clock "
"would erase all of that friction in one stroke and let the country stop relearning the same lesson every "
"spring and fall.\n\n"
"Supporters often point to how the switch ripples through daily life in small but real ways. Parents report "
"that young children take days to settle into the new clock. School start times feel harsher for a week "
"after the spring change. Shift workers and nurses, who already fight their body clocks, get thrown off "
"even further. None of these problems is dramatic on its own. But added together, twice every year, they "
"form a steady drain that the country has simply learned to accept. Supporters ask a fair question. Why "
"keep paying that price out of habit, when a single steady clock would end it for good?\n\n"
"Supporters do not claim that later summer evenings have no value. They know some people love the long, "
"bright nights that daylight saving time provides in July. But they argue that our health and safety should "
"come first, ahead of a few extra evening hours of light in one season. A clock, after all, is only a tool "
"for organizing our days. Supporters believe that tool should serve the human body, and not the other way "
"around. Pick one honest time, they say, and let the country finally rest."
)

PASSAGE_B = (
"Ending daylight saving time sounds harmless. Some people even call it overdue. But critics warn that the "
"choice is trickier than it first appears. Their main point is simple. Both permanent options carry real "
"costs. There is no painless clock to switch to. Consider permanent standard time, the setting many doctors "
"prefer. It would bring earlier winter sunrises, which is good for morning light. But it would also bring "
"very early winter sunsets. Many workers would then drive home in the dark. For anyone who wants daylight "
"after the workday ends, that is a steep and lasting price to pay.\n\n"
"Critics also point to the benefits of daylight saving time that supporters tend to rush past. The extra "
"evening light of summer is not just pleasant. The Department of Energy has studied how the timing of "
"daylight shapes how households use power. It also shapes how they spend their evenings. Longer evening "
"light draws people outside. They walk, play, shop, and gather after work or school. Some businesses lean "
"on those bright hours. Ice cream stands and youth sports leagues plan a whole season around them.\n\n"
"There is a safety argument on this side too. Supporters of ending the switch focus on the groggy days "
"right after the spring change. But critics note that more evening light can make the roads safer during "
"the busy hours when people run errands and children play outside. The Department of Transportation tracks "
"crashes across the country, and darkness is a well-known danger for both drivers and pedestrians. Trading "
"away bright summer evenings, critics argue, might simply move the risk rather than remove it.\n\n"
"Critics add that the true harm may come from the switching itself, not from either clock. If that is so, "
"then the honest fix is to pick one setting and stop changing, whichever one a community prefers. That is a "
"different debate from abolishing daylight saving time in particular. A region that loves its long summer "
"nights might reasonably choose permanent daylight saving time instead of the standard time doctors favor.\n\n"
"Critics also warn that a national rule can ignore how different the country really is. The United States "
"stretches across many latitudes and several time zones. A clock that feels right in the far north can feel "
"wrong in the deep south, where daylight changes far less over the year. A setting that suits a farm state "
"may not suit a city that lives and shops late into the evening. Because of this, critics argue that a "
"single mandate handed down for everyone could easily please one region while frustrating another. They "
"would rather let states and communities weigh their own daylight and choose the setting that fits their "
"lives.\n\n"
"None of this means the current system is perfect. Critics agree that the twice-yearly jump is disruptive "
"and that the lost sleep is a genuine problem worth taking seriously. But they urge people to weigh the "
"whole trade before cheering for one clock. Every option, they remind us, takes daylight from one end of "
"the day and hands it to the other. The real question is not whether to change, but which trade a community "
"is truly willing to live with all year long."
)

FACTS = [
    FactSource("Most teenagers do not get enough sleep", "insufficient sleep",
               "US Centers for Disease Control and Prevention",
               "https://www.cdc.gov/sleep/about/index.html"),
    FactSource("Daylight timing shapes household energy use and evening activity", "energy and activity",
               "US Department of Energy", "https://www.energy.gov/articles/daylight-saving-time"),
    FactSource("Darkness is a known crash risk tracked nationally", "darkness crash risk",
               "US Department of Transportation (NHTSA)", "https://www.nhtsa.gov/risky-driving/drowsy-driving"),
]

rec = StimulusRecord(
    id="ACC-W910-ARG-OPP-LESSON-DST",
    grade="9-10", mode="argument", family="opposing", bucket="lesson",
    topic_id="daylight_saving",
    modeling_anchor="Ohio ELA II / MD MCAP (opposing-view pick-a-side)",
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "CCSS.W.9-10.1"],
    prompt=("Weighing both sources, write an argumentative essay stating your position on whether the United "
            "States should abolish daylight saving time and keep one clock year round. Support your claim "
            "with evidence from both sources, and respond to at least one objection from the side you do not take."),
    passages=[
        Passage(title="Pick One Clock: The Case for Ending the Twice-Yearly Switch",
                angle="pro-abolish; CDC sleep and body-clock health argument", text=PASSAGE_A),
        Passage(title="Every Clock Has a Cost",
                angle="con; DOE/DOT evening-daylight benefits and the switching-vs-setting distinction", text=PASSAGE_B),
    ],
    fact_sources=FACTS,
    provenance={"copyright": "own_authored", "rights": "public-domain-sourced (US CDC/DOE/DOT)",
                "authored": "2026-07-08"},
)

SINGLES = [
    StimulusRecord(
        id="ACC-W910-ARG-SINGLE-DST-PRO", grade="9-10", mode="argument", family="single", bucket="lesson",
        modeling_anchor=rec.modeling_anchor, acc_tags=list(rec.acc_tags),
        prompt="Read this source arguing in favor of abolishing daylight saving time.",
        passages=[Passage(title=rec.passages[0].title, angle=rec.passages[0].angle, text=PASSAGE_A)],
        fact_sources=list(rec.fact_sources), provenance=dict(rec.provenance),
        topic_id="daylight_saving", proposition_id="prop_daylight_saving", stance="pro",
        form="staar", task_demand=3),
    StimulusRecord(
        id="ACC-W910-ARG-SINGLE-DST-CON", grade="9-10", mode="argument", family="single", bucket="lesson",
        modeling_anchor=rec.modeling_anchor, acc_tags=list(rec.acc_tags),
        prompt="Read this source arguing against abolishing daylight saving time.",
        passages=[Passage(title=rec.passages[1].title, angle=rec.passages[1].angle, text=PASSAGE_B)],
        fact_sources=list(rec.fact_sources), provenance=dict(rec.provenance),
        topic_id="daylight_saving", proposition_id="prop_daylight_saving", stance="con",
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
