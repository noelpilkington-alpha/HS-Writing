"""
G11 SYNTHESIS SOURCE SET for the writing course (LESSON bucket, annotatable). family="synthesis_set".
Debatable question: when water grows scarce, should the United States protect the water that cools its power
plants or the water that grows its crops? THREE ~500-word text sources on one debatable question (SBAC/AP Lang
synthesis model, minimum set). This is the TEACHING version used by the G11 course-map synthesis unit (U3:
L12 intro, L13 guided) so the cold TEST synthesis sets (synth_renewable_grid, synth_ai_workforce,
synth_water_scarcity) are NOT burned as worked examples before the gate. The QUESTION here (competing uses:
energy vs. agriculture) is DISTINCT from the cold water set's question (how to MANAGE scarcity).

Every numeric figure traces to a verified US USGS row already documented + QC-passed in the G11 bank
(lesson_info_water_infrastructure); NO re-fetch, NO fabrication, NO derived figures (per the source-cache
decision). Register pinned to the G11 band (1120-1300L). Family=synthesis_set, mode=argument. No em dashes.
Runs itself through the QC harness and reports.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# --- Source 1: US USGS -- the overall picture: where the nation's water actually goes ------------
SOURCE_OVERVIEW = (
"Water is the one resource a modern country cannot do without and cannot easily replace, and the United "
"States uses a staggering amount of it. According to the U.S. Geological Survey, the nation withdrew about "
"322 billion gallons of water each day in 2015, drawn from rivers, lakes, reservoirs, and underground "
"aquifers. That figure is difficult to picture until it is broken down, because the water does not spread "
"evenly across the many things a country does. A small number of uses dominate the total, and understanding "
"which ones is the first step toward any honest argument about how a drier future should be handled.\n\n"

"The Geological Survey reports that around 90 percent of daily water use in the lower forty-eight states "
"goes toward just three purposes: cooling the power plants that make electricity, irrigating the farms that "
"grow food, and supplying homes and businesses through public water systems. Everything else a nation does "
"with water, from manufacturing to mining to raising livestock, fits into the slim remainder. When people "
"picture water use, they often think first of showers, lawns, and kitchen taps. Those household uses matter, "
"but they are not where the great rivers of national water actually flow. The largest demands come from the "
"systems that keep the lights on and the systems that keep the country fed.\n\n"

"This concentration is what makes the coming decades so difficult, and a second fact makes it harder still. "
"The U.S. Environmental Protection Agency reports that only about 1 percent of the water on Earth is fresh "
"and readily available for human use; the rest is salt water or locked in ice. The nation's enormous daily "
"withdrawal, in other words, is drawn from a supply that is far smaller and far more fragile than the blue "
"expanse of the planet suggests. If water were spread thinly across thousands of small uses, a shortage "
"could be met by trimming a little from each. Instead, the water is gathered into a few enormous channels, "
"and two of those channels are far larger than the rest. Cutting national water use in a serious drought "
"therefore means confronting the giants, not the household faucet. It means asking hard questions about the "
"water that cools power plants and the water that irrigates crops, because those two uses together account "
"for most of the freshwater the country draws from that thin one percent each day.\n\n"

"That is the uncomfortable heart of the matter. In an average year, when rain is plentiful and rivers run "
"high, the country need not choose between its great water uses; there is enough for all of them. In a dry "
"year, when reservoirs fall and aquifers drop, the choices grow sharp. Water promised to a power plant "
"cannot also be promised to a farm downstream. A region cannot cool its electricity and irrigate its fields "
"with the same gallon. The debate that follows is not about whether Americans use too much water in some "
"abstract sense. It is about which of two essential uses a community should protect first when there is no "
"longer enough to satisfy both. To answer that, a writer has to look closely at what each of those two "
"giant uses actually does for the country, and what would happen if its share of the water were cut."
)

# --- Source 2: US USGS -- the case for protecting the water that makes electricity ---------------
SOURCE_ENERGY = (
"Consider first the water that cools the nation's power plants. Most Americans never think of electricity "
"as a thirsty product, yet making it consumes more water than almost anything else the country does. The "
"U.S. Geological Survey reports that thermoelectric power plants, the large stations that boil water into "
"steam to spin their turbines, withdrew about 133 billion gallons of water each day in 2015. That single "
"use accounted for roughly 41 percent of all the water the nation withdrew, more than any other category. "
"Behind every lit room and charged phone stands a hidden current of water, drawn from a nearby river or "
"lake to carry away the enormous heat that generating power produces.\n\n"

"Those who would protect this water first begin from how much depends on it, and from how that power is made. "
"The U.S. Energy Information Administration reports that fossil fuels still supplied about 60 percent of the "
"nation's electricity in 2023, and those coal and gas plants are precisely the thermoelectric stations that "
"must draw water to carry off their heat. For most of the grid, water and power are not two separate "
"resources but one linked system: cut the cooling water and the largest share of the nation's electricity is "
"what falters. Electricity is not one need "
"among many; it is the need that underpins the others. Hospitals, water-treatment plants, food refrigeration, "
"heating and cooling, communications, and modern industry all fail when the power fails. A community that "
"loses its electricity for more than a short time faces a genuine emergency, one that endangers lives rather "
"than merely inconveniencing them. From this vantage, the water that keeps power plants running is not a "
"luxury to be trimmed in a dry season. It is the thread that holds the rest of modern life together, and "
"cutting it to save water elsewhere could cause far more harm than the drought itself.\n\n"

"There is also a matter of timing that this side stresses. A farm can, in a hard year, plant fewer acres or "
"switch to a crop that needs less water, and the loss, though painful, is bounded and temporary. A power "
"plant starved of cooling water has no such option in the moment. It must reduce its output or shut down, "
"and when it does, the electricity it would have made does not simply wait. It disappears from the grid at "
"the very hours when people, straining their air conditioners against the same heat that caused the drought, "
"need it most. The argument, then, is one of sequence and consequence: protect the cooling water first, "
"because its failure arrives fastest and strikes hardest.\n\n"

"This position does not claim that farms do not matter. It claims that among the great uses of water, the "
"one attached to electricity has the shortest fuse and the widest blast radius. Take water from irrigation "
"and a harvest shrinks; take water from power generation and the machinery of an entire region can stall "
"within days. Because that 41 percent share of the nation's withdrawals stands behind nearly every other "
"essential service, this side argues, it deserves the first and firmest claim on a shrinking supply. When "
"the reservoirs fall, in their view, the country should keep the turbines cool before it keeps the fields "
"green, and accept the smaller harvest as the lesser of two hard losses."
)

# --- Source 3: US USGS -- the case for protecting the water that grows food ----------------------
SOURCE_FARM = (
"Set beside the power plants stands the other giant, and its defenders argue that it, not electricity, "
"deserves the first claim on scarce water. The U.S. Geological Survey reports that irrigation withdrew "
"about 118 billion gallons of water each day in 2015, an amount that accounted for roughly 42 percent of "
"the nation's freshwater withdrawals. That share is measured against freshwater alone, while the power-"
"plant share above is measured against all withdrawals including salt water, so the two percentages rest "
"on different totals and cannot be lined up directly; compared by daily volume, though, the 118 billion "
"gallons for crops is nearly the equal of the water used to cool the country's power plants. On the "
"scale of national water use, in other words, food and electricity are close rivals, and choosing between "
"them is choosing between two of the largest things the country does with the water it has.\n\n"

"Those who would protect irrigation first make an argument about depth rather than speed. A power shortage, "
"they concede, arrives quickly and frightens everyone, but it can also be managed and recovered from within "
"a season. A food system starved of water fails more slowly and heals far more slowly still. Orchards and "
"vineyards represent decades of investment; a tree killed by a single dry summer cannot be replaced the "
"following spring. Farmland left unwatered for years loses not only its crop but the farmers, workers, and "
"rural towns that depend on it. To this side, the harm from cutting irrigation is not smaller than a power "
"outage but larger, because it reaches further into the future and cannot be switched back on.\n\n"

"There is also the question of what a country most fundamentally owes its people. A nation can, at real "
"cost, import electricity from a neighbor or build new kinds of power plants that use less water. Food is "
"harder to outsource without surrendering a basic form of security, and a country that cannot feed itself "
"has traded away something it may not get back. From this angle, the 42 percent of freshwater that irrigation "
"draws is not a discretionary use to be sacrificed when reservoirs fall. It is the foundation of a food "
"supply that no import can fully guarantee, and protecting it is a matter of national resilience rather "
"than mere agricultural convenience.\n\n"

"Notice that this side and the last one accept the very same facts. Both agree that cooling water and "
"irrigation water are the two largest demands the nation places on its supply, each claiming roughly four "
"gallons in ten of what the country withdraws. Both agree that a serious drought will force a choice between "
"them. The disagreement is only about which loss a community should be willing to bear. One side would keep "
"the power plants cool and accept a thinner harvest; the other would keep the fields watered and accept a "
"strained grid. A strong synthesis will not pretend the tension away. It will weigh the speed of one harm "
"against the depth of the other, and defend a position on which giant a drying country should feed first."
)

REC = StimulusRecord(
    id="ACC-W1112-SYNTH-LESSON-0001",
    grade="11", mode="argument", family="synthesis_set", bucket="lesson",
    annotated=True,
    modeling_anchor="SBAC G11 full-write / AP Lang synthesis (teaching version)",
    acc_tags=["ACC.W.SRC.1", "ACC.W.INFO.2", "CCSS.W.11-12.7", "CCSS.W.11-12.8"],
    topic_id="water_competing_uses",
    prompt=("These three sources address one debatable question: when water grows scarce, should the United "
            "States protect the water that cools its power plants or the water that grows its crops? Drawing "
            "on at least two of the sources, write an essay that develops and defends your own position. "
            "Synthesize the sources to support your argument rather than summarizing them one by one, and "
            "cite each source you use."),
    passages=[
        Passage(title="Where the Nation's Water Goes",
                angle="national water-use framing (US USGS)", text=SOURCE_OVERVIEW),
        Passage(title="The Water That Keeps the Lights On",
                angle="energy-first vantage: thermoelectric cooling (US USGS)", text=SOURCE_ENERGY),
        Passage(title="The Water That Grows the Food",
                angle="agriculture-first vantage: irrigation (US USGS)", text=SOURCE_FARM),
    ],
    fact_sources=[
        FactSource("Total US water withdrawals per day, 2015", "322 billion gallons", "US USGS",
                   "https://www.usgs.gov/mission-areas/water-resources/science/water-use-united-states",
                   "Water use in the United States in 2015 was estimated to be about 322 billion gallons per day"),
        FactSource("Share of daily water use from top three categories (lower 48)", "90 percent", "US USGS",
                   "https://www.usgs.gov/mission-areas/water-resources/science/water-use-united-states",
                   "Around 90% of daily water use ... goes toward crop irrigation, thermoelectric power plants ... and public supply"),
        FactSource("Thermoelectric water withdrawals per day, 2015", "133 billion gallons", "US USGS",
                   "https://www.usgs.gov/mission-areas/water-resources/science/thermoelectric-power-water-use",
                   "Total withdrawals for thermoelectric power for 2015 were 133,000 Mgal/d"),
        FactSource("Thermoelectric share of total US water withdrawals, 2015", "41 percent", "US USGS",
                   "https://www.usgs.gov/mission-areas/water-resources/science/thermoelectric-power-water-use",
                   "accounted for 41 percent of total water withdrawals"),
        FactSource("Irrigation water withdrawals per day, 2015", "118 billion gallons", "US USGS",
                   "https://www.usgs.gov/mission-areas/water-resources/science/irrigation-water-use",
                   "total irrigation withdrawals were 118,000 Mgal/d"),
        FactSource("Irrigation share of US freshwater withdrawals, 2015", "42 percent", "US USGS",
                   "https://www.usgs.gov/mission-areas/water-resources/science/irrigation-water-use",
                   "which accounted for 42 percent of total freshwater withdrawals"),
        FactSource("Share of Earth's water fresh and available for human use", "1 percent", "US EPA",
                   "https://www.epa.gov/watersense/how-we-use-water",
                   "only about 1 percent is available for human use"),
        FactSource("Fossil-fuel share of US electricity, 2023", "60 percent", "US EIA",
                   "https://www.eia.gov/tools/faqs/faq.php?id=427&t=3",
                   "About 60% of this electricity generation was from fossil fuels"),
    ],
    provenance={"copyright": "own_authored", "rights": "public-domain-sourced (US federal)",
                "authored": "2026-07-10",
                "note": "LESSON-bucket teaching version for G11 U3; facts reuse verified USGS rows already "
                        "QC-passed in lesson_info_water_infrastructure. Question (competing uses: energy vs "
                        "agriculture) is distinct from the cold synth_water_scarcity set (how to manage "
                        "scarcity), so the synthesis gate is not pre-exposed."},
)

if __name__ == "__main__":
    qc = qc_stimulus(REC)
    import re
    for p in REC.passages:
        wc = len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", p.text))
        print(f"  {p.title}: {wc} words")
    print(qc_report(REC))
    sys.exit(0 if qc["passed"] else 1)
