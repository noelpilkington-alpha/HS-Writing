"""
Opposing-pair argument stimulus for the G10 writing test bank.
TOPIC: Should the US increase federal spending on space exploration?
Family=opposing, mode=argument. Every figure traces to a fetched federal page (NASA economic-impact
study + NASA Spinoff program on the PRO side; US GAO oversight reports on the CON side). Each passage
concedes the other side's strongest point. Runs itself through the QC harness and reports.
Facts fetched live 2026-07-07.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)) + "/pipeline")
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# ---------------------------------------------------------------------------
# PRO passage (~560 words): increase spending. NASA economic-impact + Spinoff data.
# ---------------------------------------------------------------------------
PRO = (
"Ask most Americans how much of the federal budget goes to space, and the guess is usually far too "
"high. In truth, the space program is a small part of national spending. Supporters argue that this "
"small part returns far more than it costs. They point to hard numbers gathered by the space agency "
"itself. According to a NASA economic study, the agency created more than 64.3 billion in total "
"economic output during 2019, and that same activity supported more than 312,000 jobs across the "
"country. It also produced an estimated 7 billion in taxes. In other words, much of the money spent on "
"space did not simply vanish into the sky. It flowed back into paychecks, businesses, and public "
"revenue here at home.\n\n"

"Supporters also emphasize that the benefits reach ordinary life in ways people rarely notice. Since "
"1976, NASA has profiled more than 2,000 spinoffs, the commercial products that grew out of space "
"research. They range from medical devices to water filters to safety equipment. The lesson, "
"supporters say, is that solving the extreme problems of spaceflight forces engineers to invent tools "
"that later serve everyone. A dollar aimed at the Moon does not stay aimed at the Moon. It often lands "
"back in a hospital, a factory, or a kitchen.\n\n"

"The exploration programs themselves show this pattern. NASA reports that its Moon to Mars work alone "
"created more than 14 billion in economic output. That work also supported tens of thousands of jobs. "
"This single effort made up about 22 percent of the agency's entire economic impact. Supporters argue "
"that cutting back on exploration would not merely save money. It would also switch off an engine that "
"drives research, skilled jobs, and new industry.\n\n"

"To be fair, critics raise a genuine point, and honest supporters confront it. Large space projects "
"have run over budget, sometimes badly. Government auditors have documented billions of dollars in "
"cost overruns on major NASA programs. Those overruns are a real problem that demands a real remedy, "
"and supporters do not deny it. Their answer is that the remedy is better management, not retreat. A "
"program can waste money in places and still be worthwhile overall. In the same way, a valuable bridge "
"can still be constructed more carefully. Cutting the budget, they argue, punishes the mission for the "
"failures of its accounting.\n\n"

"There is also a case that reaches beyond dollars. A space program gives a country a frontier to work "
"toward. That sense of purpose is hard to measure but easy to feel. Students who watch a launch decide "
"to study engineering. Researchers who might have gone elsewhere stay to solve problems no one else is "
"attempting. Supporters admit that inspiration cannot be entered on a spreadsheet the way tax money "
"can. Even so, they insist it is real. A nation that stops reaching outward pays a quiet cost that "
"never appears on a budget page.\n\n"

"Weighed together, the argument for more federal spending on space rests on evidence, not hope alone. "
"The money supports hundreds of thousands of jobs. It returns economic output in the tens of billions. "
"It seeds thousands of everyday technologies. It points a generation toward hard, useful work. The "
"overruns are real, but so are the returns. For supporters, the sensible response is clear. A program "
"that costs too much in places yet gives back so much overall should be fixed, not shrunk. Repair the "
"waste and fund the future. Do not abandon one of the few investments that so plainly pays its own way."
)

# ---------------------------------------------------------------------------
# CON passage (~600 words): do not increase spending. US GAO cost-overrun watchdog data.
# ---------------------------------------------------------------------------
CON = (
"No one seriously claims that space research is worthless. The tools, the jobs, and the discoveries are "
"real. Even the sharpest critics of space spending admit as much. The question is not whether the space "
"program does any good. It is whether the country should pour more money into a program that keeps "
"proving it cannot control its own costs. On that narrower question, the record built by government "
"auditors is hard to ignore.\n\n"

"Look at the agency's main rocket, the Space Launch System. It is meant to carry astronauts back toward "
"the Moon. The Government Accountability Office reports that NASA asked for 11.2 billion to fund the "
"program through 2028. That request came on top of the 11.8 billion already spent to build the rocket's "
"first version. More telling is what NASA's own senior leaders told the auditors. At current cost "
"levels, they said, the program is unaffordable. When the people running a project describe it that "
"way, adding money without changing how it is managed looks less like investment and more like habit.\n\n"

"The problem is not one troubled rocket. It runs across the whole set of projects. The Government "
"Accountability Office found that NASA plans to invest more than 82 billion in its major projects. "
"These projects carry a long history of cost growth. In 2023, the auditors measured 7.6 billion in "
"cost overruns. The figure got better the next year. It fell to 4.4 billion in 2024, which shows that "
"progress is possible. But a smaller overrun is still an overrun. The Orion crew capsule alone made up "
"65 percent of the total baseline cost overrun, a share worth 2.9 billion. These are not rounding "
"errors. They are the size of whole public programs.\n\n"

"Critics of higher spending take care to grant the other side's best point. The economic returns that "
"supporters cite are genuine. Space work does support hundreds of thousands of jobs. It does create "
"tools that reach daily life. But a return on investment only means something if the investment is "
"under control. When a program keeps costing billions more than promised, no one can say for sure what "
"the true return is. No one can even say what the true cost will finally be. A benefit that rests on a "
"shaky price tag is a benefit built on sand.\n\n"

"There is also the matter of choice. Every dollar sent to an over-budget rocket is a dollar not spent "
"on needs that press harder on daily life. The auditors have set NASA new cost baselines. One totals "
"9.6 billion for three Artemis projects, and history hints those baselines will be tested. Before the "
"country agrees to spend more, it is fair to ask a simple question. Would the same money do more good "
"in classrooms, clinics, or research that helps people now, not decades from now?\n\n"

"None of this is a call to abandon space. It is a call to earn the next dollar before asking for it. "
"The sensible path is to hold NASA to firm cost baselines. Reward the programs that stay within them. "
"Prove that the overruns are shrinking for good, not just for a single year. Raising the budget today, "
"before that discipline is set, rewards the very behavior that caused the overruns in the first place. "
"The country can be proud of what space exploration has done and still insist that its money be spent "
"with care."
)

rec = StimulusRecord(
    id="ACC-W910-ARG-OPP-0006",
    grade="9-10", mode="argument", family="opposing",
    modeling_anchor="Ohio ELA II / MD MCAP (opposing-view pick-a-side argument)",
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "ACC.W.ARG.4", "CCSS.W.9-10.1",
              "OH-ELA.W.9-10.1", "MD-MCAP.W.ARG"],
    prompt=("Weighing both sources, write an argumentative essay that states and defends your position on "
            "whether the United States should increase federal spending on space exploration. Support your "
            "claim with specific evidence from both sources and address at least one objection from the "
            "side you argue against."),
    passages=[
        Passage(title="Why the Investment Pays Off", angle="pro-increase; NASA economic-impact + Spinoff data", text=PRO),
        Passage(title="A Bill the Country Keeps Underestimating", angle="anti-increase; US GAO cost-overrun oversight data", text=CON),
    ],
    fact_sources=[
        # ---- PRO side: NASA ----
        FactSource("NASA total economic output FY2019", "64.3 billion", "NASA",
                   "https://www.nasa.gov/news-release/nasa-report-details-how-agency-significantly-benefits-us-economy/",
                   "generated more than $64.3 billion in total economic output during fiscal year 2019"),
        FactSource("Jobs supported nationwide", "312,000 jobs", "NASA",
                   "https://www.nasa.gov/news-release/nasa-report-details-how-agency-significantly-benefits-us-economy/",
                   "supported more than 312,000 jobs nationwide"),
        FactSource("Federal/state/local taxes generated", "7 billion", "NASA",
                   "https://www.nasa.gov/news-release/nasa-report-details-how-agency-significantly-benefits-us-economy/",
                   "an estimated $7 billion in federal, state, and local taxes"),
        FactSource("Moon to Mars economic output", "14 billion", "NASA",
                   "https://www.nasa.gov/news-release/nasa-report-details-how-agency-significantly-benefits-us-economy/",
                   "generated more than $14 billion in total economic output"),
        FactSource("Moon to Mars jobs supported", "69,000 jobs", "NASA",
                   "https://www.nasa.gov/news-release/nasa-report-details-how-agency-significantly-benefits-us-economy/",
                   "supported more than 69,000 jobs nationwide"),
        FactSource("Moon to Mars share of NASA economic impact", "22 percent", "NASA",
                   "https://www.nasa.gov/news-release/nasa-report-details-how-agency-significantly-benefits-us-economy/",
                   "provided about 22 percent of NASA's economic impact"),
        FactSource("NASA spinoffs profiled since 1976", "2,000 spinoffs", "NASA Spinoff",
                   "https://spinoff.nasa.gov/",
                   "profiled more than 2,000 spinoffs since 1976"),
        # ---- CON side: US GAO ----
        FactSource("SLS funding requested through FY2028", "11.2 billion", "US GAO",
                   "https://www.gao.gov/products/gao-23-105609",
                   "NASA requested $11.2 billion ... to fund the program through fiscal year 2028"),
        FactSource("Already spent developing SLS initial capability", "11.8 billion", "US GAO",
                   "https://www.gao.gov/products/gao-23-105609",
                   "in addition to the $11.8 billion already spent developing the initial capability"),
        FactSource("NASA senior officials on SLS affordability", "", "US GAO",
                   "https://www.gao.gov/products/gao-23-105609",
                   "at current cost levels, the SLS program is unaffordable"),
        FactSource("NASA planned investment in major projects", "82 billion", "US GAO",
                   "https://www.gao.gov/products/gao-24-106767",
                   "NASA plans to invest over $82 billion in major projects"),
        FactSource("Portfolio cost overruns 2023", "7.6 billion", "US GAO",
                   "https://www.gao.gov/products/gao-24-106767",
                   "cost overruns decreased from $7.6 billion in 2023"),
        FactSource("Portfolio cost overruns 2024", "4.4 billion", "US GAO",
                   "https://www.gao.gov/products/gao-24-106767",
                   "to $4.4 billion in 2024"),
        FactSource("Orion share of baseline cost overrun", "65 percent / 2.9 billion", "US GAO",
                   "https://www.gao.gov/products/gao-24-106767",
                   "Orion accounted for 65 percent ($2.9 billion) of the portfolio's total cumulative baseline cost overrun"),
        FactSource("Development cost baselines for three Artemis projects", "9.6 billion", "US GAO",
                   "https://www.gao.gov/products/gao-24-106767",
                   "development cost baselines ... totaling $9.6 billion for three Artemis projects"),
    ],
    provenance={"copyright": "own_authored", "rights": "public-domain-sourced (NASA + US GAO, 17 USC 105)",
                "two_source_verified": True, "authored": "2026-07-07"},
)


# --- Two-bucket migration: decompose the opposing pair into stance-tagged TEST singles ---------
# One pro + one con member of proposition "prop_space_spending". The pair above (rec) is retained for backward
# compatibility; the singles are what the composer assembles opposing pairs from. Each single carries the
# FULL fact_sources list (the anti-fabrication gate only requires the figures IN its passage to be covered;
# extra rows are harmless and guarantee the >=3 citable-fact minimum).
SINGLES = [
    StimulusRecord(
        id="ACC-W910-ARG-SINGLE-SPACE-SPENDING-PRO",
        grade="9-10", mode="argument", family="single", bucket="test",
        modeling_anchor=rec.modeling_anchor,
        acc_tags=list(rec.acc_tags),
        prompt="Read this source arguing in favor of the proposal.",
        passages=[Passage(title=rec.passages[0].title, angle=rec.passages[0].angle, text=rec.passages[0].text)],
        fact_sources=list(rec.fact_sources),
        provenance=dict(rec.provenance),
        topic_id="space_spending", proposition_id="prop_space_spending", stance="pro",
        form="staar", task_demand=3),
    StimulusRecord(
        id="ACC-W910-ARG-SINGLE-SPACE-SPENDING-CON",
        grade="9-10", mode="argument", family="single", bucket="test",
        modeling_anchor=rec.modeling_anchor,
        acc_tags=list(rec.acc_tags),
        prompt="Read this source arguing against the proposal.",
        passages=[Passage(title=rec.passages[1].title, angle=rec.passages[1].angle, text=rec.passages[1].text)],
        fact_sources=list(rec.fact_sources),
        provenance=dict(rec.provenance),
        topic_id="space_spending", proposition_id="prop_space_spending", stance="con",
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
