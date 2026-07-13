"""
Opposing-pair argument stimulus for the G10 writing test bank.
TOPIC: Should the US government require automakers to phase out new gas-powered cars (EV mandates)?
family=opposing, mode=argument. Two genuinely opposing sides, each conceding the other's strongest point.

Every figure traces to a FETCHED federal page (US EPA, US DOE, US Geological Survey), fetched live 2026-07-07.
Authored through the proven engine (imports stimulus_contract); runs itself through the QC harness on run.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# --- Source A: PRO-MANDATE (US EPA efficiency + emissions data) -------------------------------------
PASSAGE_A = (
"Cars and trucks are one of the largest sources of the pollution that is warming the planet. The U.S. "
"Environmental Protection Agency reports that a typical gas-powered passenger vehicle gives off about 4.6 "
"metric tons of carbon dioxide every year. Spread across a whole country of drivers, that adds up to an "
"huge load on the air we all share. Supporters of a phase-out say the government should make "
"carmakers stop selling new gas cars and switch fully to electric vehicles. Their case rests on a simple "
"idea. If the cleaner choice is already here, the country should not wait for drivers to find it alone.\n\n"

"Start with how much cleaner an electric vehicle is to drive. A gas engine wastes most of the fuel it burns. "
"The Environmental Protection Agency estimates that gasoline vehicles turn only about 16 to 25 percent of the "
"energy in their fuel into actual movement. The rest escapes as heat and noise. Electric vehicles are far "
"better. They use roughly 87 to 91 percent of the energy stored in their batteries to move the car forward. "
"That gap is not small. It means an electric vehicle does far more with each unit of energy, and it does so "
"without sending carbon dioxide out of a tailpipe. The average gas car, by contrast, releases about 400 grams "
"of carbon dioxide for every mile it travels.\n\n"

"Supporters admit that electric vehicles are not perfect. Building a battery takes energy and raw materials, "
"and that step does create pollution before the car is ever driven. This is the strongest point the other "
"side makes, and it is a fair one. But the Environmental Protection Agency has studied the full life of both "
"kinds of car, from the factory to the junkyard. Even after counting the pollution from building the battery, "
"an electric vehicle still gives off less greenhouse gas than a similar gas car over its whole "
"life. The early cost in pollution is real, yet the car pays it back and then keeps on saving.\n\n"

"Why require the change instead of leaving it to shoppers? Supporters point out that the market has moved "
"slowly, and the climate does not wait. Carmakers plan their factories years in advance. A clear national "
"rule gives them a firm deadline, so they can invest in electric models with confidence instead of hedging "
"their bets. A rule also spreads the effort fairly. No single company has to fear that it will go green while "
"its rivals keep selling cheap gas cars. When everyone must meet the same rule, the whole industry moves "
"as one.\n\n"

"There is also the matter of clean air in the places people actually live. Gas cars do more than warm the "
"planet. They release gases and fine particles along every road, and that pollution is worst in crowded "
"neighborhoods near busy highways. Because electric vehicles have no tailpipe, phasing out gas engines would "
"lift a health burden from the people who breathe the most traffic exhaust. That benefit lands close to "
"home, not only in far-off climate charts.\n\n"

"None of this means the switch is easy. It will take new charging stations, a stronger power grid, and a "
"steady supply of battery materials. Supporters do not deny those challenges. They argue that a firm "
"government deadline is the very thing that will pull the needed investment forward. The alternative, they "
"say, is to keep locking in gas cars that will burn fuel for the next fifteen years. Every new gas car sold "
"today is a promise of carbon tomorrow. To supporters of a phase-out, the cleaner technology is already here, "
"its advantage is measured and real, and the responsible move is to require the change rather than merely "
"hope for it."
)

# --- Source B: ANTI/CAUTIOUS (US DOE grid data + USGS mineral-supply data) --------------------------
PASSAGE_B = (
"No one seriously argues that electric vehicles are dirty to drive. They are quiet, they have no tailpipe, "
"and they use energy far more efficiently than a gas engine. On that point the two sides agree. The real "
"question is a different one. Should the federal government force carmakers to stop selling gas cars on a "
"fixed timeline, before the country is ready to support a fleet that runs entirely on electricity? A growing "
"number of experts say the honest answer is not yet.\n\n"

"Begin with the power grid. Every electric vehicle that replaces a gas car becomes a new mouth to feed on the "
"electric system. The U.S. Department of Energy reports that in 2022, only about 0.15 percent of the nation's "
"electricity went to transportation. If the entire 2022 fleet of cars and trucks were suddenly electric, that "
"share would jump to roughly 34 percent. In plain terms, powering the vehicles we already own would force the "
"grid to send about a third of all its output to the roads. That is not a small tune-up. It is a massive new "
"demand on a system that already strains during heat waves and cold snaps.\n\n"

"Building the wires and stations to carry that load is expensive, and the bill is local. The Department of "
"Energy points to California, where upgrading the local distribution grid for electric vehicles could cost as "
"much as 50 billion dollars by the year 2035. In New York, the projected cost of those upgrades ranges from "
"about 1.4 billion to 26.8 billion dollars, depending on how carefully charging is managed. Someone has to "
"pay for that work, and much of it will land on ordinary electricity customers through their monthly bills.\n\n"

"Then there is the question of where the batteries and motors come from. A modern electric vehicle depends on "
"minerals that the United States mostly does not produce. Many electric motors, for example, rely on rare "
"earth elements, and the U.S. Geological Survey reports that the country imported 80 percent of the rare earth "
"elements it used in 2024. A law that forces every new car to be electric would tie the nation's "
"transportation to supply chains that run through other countries. If those supplies were cut off or priced "
"out of reach, a mandate could leave buyers with no legal car to buy at all.\n\n"

"Cautious voices are careful to give the other side its due. Electric vehicles really are cleaner over their "
"lifetime, and the country should keep encouraging them. Their argument is not against electric cars. It is "
"against the word require. A mandate sets a hard deadline that the grid, the charging network, and the "
"mineral supply may not be able to meet. When a rule outruns reality, the people caught in the gap are "
"ordinary drivers, above all those who cannot easily afford a new car or install a charger at home.\n\n"

"There is also the matter of fairness across the country. A driver in a dense city with plenty of chargers is "
"in a very different position from a driver in a rural county with almost none. A single national deadline "
"treats those two situations as if they were the same. Critics argue that a smarter path is to let the "
"technology and the grid catch up, keep offering incentives to buyers, and raise the standards as the country "
"becomes able to meet them. That way progress is real rather than forced onto paper.\n\n"

"The goal, in this view, is not to protect gas engines forever. It is to make the switch actually stick. A "
"phase-out that arrives before the grid and the supply chain are ready, they warn, risks higher bills, "
"blackouts, and a public backlash that could slow the very change that everyone claims to want."
)

rec = StimulusRecord(
    id="ACC-W910-ARG-OPP-0001",
    grade="9-10", mode="argument", family="opposing",
    modeling_anchor="Ohio ELA II / MD MCAP (opposing-view pick-a-side)",
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "ACC.W.ARG.4", "CCSS.W.9-10.1", "OH-ELA.W.9-10.1"],
    prompt=("Weighing both sources, write an argumentative essay that states and defends your position on "
            "whether the US government should require automakers to phase out new gas-powered cars. Support "
            "your claim with specific evidence from both sources, and respond to at least one objection raised "
            "by the side you disagree with."),
    passages=[
        Passage(title="Why the Government Should Require the Switch to Electric",
                angle="pro-mandate; US EPA efficiency and emissions data",
                text=PASSAGE_A),
        Passage(title="Why a Gas-Car Mandate Is the Wrong Move Right Now",
                angle="anti-mandate / cautious; US DOE grid-load and USGS mineral-supply data",
                text=PASSAGE_B),
    ],
    fact_sources=[
        # ---- Source A: US EPA (pro-mandate) ----
        FactSource("Annual CO2 from a typical passenger vehicle", "4.6 metric tons", "US EPA",
                   "https://www.epa.gov/greenvehicles/greenhouse-gas-emissions-typical-passenger-vehicle",
                   "A typical passenger vehicle emits about 4.6 metric tons of CO2 per year."),
        FactSource("Average passenger vehicle CO2 per mile", "400 grams", "US EPA",
                   "https://www.epa.gov/greenvehicles/greenhouse-gas-emissions-typical-passenger-vehicle",
                   "The average passenger vehicle emits about 400 grams of CO2 per mile."),
        FactSource("Efficiency of gasoline vehicles (energy to movement)", "16-25 percent", "US EPA",
                   "https://www.epa.gov/greenvehicles/electric-vehicle-myths",
                   "Gasoline vehicles only convert about 16-25% of the energy from gasoline into movement."),
        FactSource("Efficiency of electric vehicles (energy to movement)", "87-91 percent", "US EPA",
                   "https://www.epa.gov/greenvehicles/electric-vehicle-myths",
                   "EVs use approximately 87%-91% of the energy from the battery ... to propel the vehicle."),
        FactSource("Lifetime GHG of EV vs gas car (incl. battery manufacturing)", "", "US EPA",
                   "https://www.epa.gov/greenvehicles/electric-vehicle-myths",
                   "total GHGs for the EV are still lower than those for the gasoline car."),
        # ---- Source B: US DOE (cautious / grid) ----
        FactSource("Share of US electricity serving transportation, 2022", "0.15 percent", "US DOE",
                   "https://www.energy.gov/sites/default/files/2024-10/Congressional%20Report%20EV%20Grid%20Impacts.pdf",
                   "In 2022, only 0.15% of the available electricity produced served transportation."),
        FactSource("Electricity share if 2022 fleet were fully electrified", "34 percent", "US DOE",
                   "https://www.energy.gov/sites/default/files/2024-10/Congressional%20Report%20EV%20Grid%20Impacts.pdf",
                   "If 100% of the 2022 fleet were electrified, this percentage would be expected to grow to 34%."),
        FactSource("California distribution-grid investment for EVs by 2035", "50 billion", "US DOE",
                   "https://www.energy.gov/sites/default/files/2024-10/Congressional%20Report%20EV%20Grid%20Impacts.pdf",
                   "required distribution grid investments may be up to $50 billion by 2035."),
        FactSource("New York EV distribution-upgrade cost range", "1.4-26.8 billion", "US DOE",
                   "https://www.energy.gov/sites/default/files/2024-10/Congressional%20Report%20EV%20Grid%20Impacts.pdf",
                   "projected distribution system upgrade costs ... range from $1.4 billion to $26.8 billion."),
        # ---- Source B: US Geological Survey (cautious / mineral supply) ----
        FactSource("US import reliance on rare earth elements, 2024", "80 percent", "US Geological Survey",
                   "https://www.usgs.gov/news/science-snippet/interior-department-releases-final-2025-list-critical-minerals",
                   "In 2024, the U.S. imported 80% of the rare earth elements it used."),
    ],
    provenance={"copyright": "own_authored",
                "rights": "public-domain-sourced (US EPA + US DOE + US Geological Survey)",
                "multi_source_verified": True, "authored": "2026-07-07"},
)


# --- Two-bucket migration: decompose the opposing pair into stance-tagged TEST singles ---------
# One pro + one con member of proposition "prop_ev_mandate". The pair above (rec) is retained for backward
# compatibility; the singles are what the composer assembles opposing pairs from. Each single carries the
# FULL fact_sources list (the anti-fabrication gate only requires the figures IN its passage to be covered;
# extra rows are harmless and guarantee the >=3 citable-fact minimum).
SINGLES = [
    StimulusRecord(
        id="ACC-W910-ARG-SINGLE-EV-MANDATE-PRO",
        grade="9-10", mode="argument", family="single", bucket="test",
        modeling_anchor=rec.modeling_anchor,
        acc_tags=list(rec.acc_tags),
        prompt="Read this source arguing in favor of the proposal.",
        passages=[Passage(title=rec.passages[0].title, angle=rec.passages[0].angle, text=rec.passages[0].text)],
        fact_sources=list(rec.fact_sources),
        provenance=dict(rec.provenance),
        topic_id="ev_mandate", proposition_id="prop_ev_mandate", stance="pro",
        form="staar", task_demand=3),
    StimulusRecord(
        id="ACC-W910-ARG-SINGLE-EV-MANDATE-CON",
        grade="9-10", mode="argument", family="single", bucket="test",
        modeling_anchor=rec.modeling_anchor,
        acc_tags=list(rec.acc_tags),
        prompt="Read this source arguing against the proposal.",
        passages=[Passage(title=rec.passages[1].title, angle=rec.passages[1].angle, text=rec.passages[1].text)],
        fact_sources=list(rec.fact_sources),
        provenance=dict(rec.provenance),
        topic_id="ev_mandate", proposition_id="prop_ev_mandate", stance="con",
        form="staar", task_demand=3),
]

if __name__ == "__main__":
    import re
    qc_stimulus(rec)
    for p in rec.passages:
        wc = len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", p.text))
        print(f"passage word count [{p.title[:40]}]: {wc}")
    print(qc_report(rec))
    print("-> PASS" if rec.qc["passed"] else "-> FAIL")
    # decomposed stance singles
    assert len(SINGLES) == 2 and {x.stance for x in SINGLES} == {"pro", "con"}
    for _x in SINGLES:
        assert _x.family == "single" and _x.bucket == "test" and _x.proposition_id and _x.topic_id and _x.form
        qc_stimulus(_x)
        assert _x.qc["passed"], f"single {_x.id} must pass QC: {_x.qc.get('first_failure')}"
    print("SINGLES decomposition OK")
    sys.exit(0 if rec.qc["passed"] else 1)
