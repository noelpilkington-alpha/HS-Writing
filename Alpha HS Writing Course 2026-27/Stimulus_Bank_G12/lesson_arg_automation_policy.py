"""
ARGUMENT LESSON stimulus for the G12 writing bank: should the country prioritize water for growing food, or
for generating power, when the two largest uses compete in a drying region?

bucket="lesson", family="single", mode="argument", grade=12 (register 1185-1385L, the densest band).
LESSON bucket: serves the G12 sophistication lesson (C.12.01, T7). A hard trade-off prompt that rewards
sophistication (situating the choice in a broader context, holding the tension). Distinct from any test-bucket
stimulus. Every figure traces to a fetched federal page (US USGS). Facts reuse verified USGS rows from the G11
test bank (no re-fetch, no fabrication). 9-gate QC footer. No em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

PASSAGE = (
"In a region where the water is running short, two of the largest demands on that water can end up in direct "
"competition, and a society is forced to choose which it will protect. The two claimants are not villains "
"or luxuries. They are the systems that feed people and the systems that keep the lights on. Deciding "
"between them, when there is not enough water for both to grow, is among the harder trade-offs a community "
"can face, and it does not yield to a slogan. This passage lays out the competing claims so that a writer "
"can take a position sophisticated enough to survive the objections it will meet.\n\n"

"The scale of the two uses is documented by the U.S. Geological Survey. In 2015 the country withdrew about "
"322 billion gallons of water per day, and roughly 90 percent of that daily use went to just three purposes: "
"irrigation for crops, thermoelectric power for electricity, and public water supply for homes and "
"businesses. Two of those three dominate the argument here, and they are best compared in the same units, "
"billions of gallons withdrawn per day. Thermoelectric power, the water used to cool the plants that make "
"electricity, withdrew about 133 billion gallons per day. Irrigation, the water used to grow crops, withdrew "
"about 118 billion gallons per day. Measured that one way, the two are close in size and are the largest "
"daily water withdrawals in the country. The Survey also reports each use as a percentage, but of a "
"different base, so the two percentages cannot be lined up against each other: thermoelectric power was "
"about 41 percent of all water withdrawn, while irrigation was about 42 percent of freshwater withdrawn, a "
"smaller pool that leaves out the saltwater used to cool power plants. When you weigh the two uses against "
"each other, use the gallons-per-day figures, not the two percentages. Cooling the power supply and watering "
"the food supply are, by these figures, the two thirstiest things the nation does.\n\n"

"A case can be made for protecting agriculture first. Food is the more basic need, the argument runs, and a "
"region that cannot feed itself becomes dependent and fragile. Farmland taken out of production in a dry "
"year may not come back, because growers who lose a season lose the capital and the workforce that make the "
"next season possible. Protect the water for crops, this side concludes, and you protect the community's "
"ability to feed itself and to hold onto the farms that took generations to build.\n\n"

"The case for protecting power first is just as serious, and it turns on a hidden dependency. Modern "
"irrigation is not a matter of rain and ditches; it runs on electric pumps that lift groundwater and move "
"it across fields. Cut the power supply to protect farms, and you may cut the very electricity the farms "
"need to irrigate, along with the electricity that runs hospitals, water-treatment plants, and homes in a "
"heat wave. Protect the power first, this side concludes, because in a modern economy almost everything, "
"including the food system, depends on a grid that stays up.\n\n"

"Notice that the strongest form of each position has already absorbed the other's best point. The "
"agriculture-first case must concede that farms themselves run on electricity; the power-first case must "
"concede that electricity with no food to buy is cold comfort. That mutual dependence is the real subject. "
"A sophisticated argument on this question will not simply pick a side and defend it against a strawman. It "
"will situate the choice in that dependence, acknowledge what protecting either use costs the other, and "
"defend a position, perhaps a rule for how to ration in the worst years, that a thoughtful reader on the "
"opposite side would still have to take seriously."
)

rec = StimulusRecord(
    id="ACC-W910-ARG-LESSON-WATERTRADEOFF",
    grade="12", mode="argument", family="single", bucket="lesson",
    topic_id="water_food_energy_tradeoff",
    annotated=False,
    modeling_anchor="AP Lang argument (single-source argument; sophistication-tier trade-off)",
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "CCSS.W.11-12.1"],
    prompt=("When water is scarce, should a region protect water for growing food or for generating power? "
            "Write an argument that takes a clear, defensible position and shows the complexity of the "
            "trade-off, acknowledging what protecting either use costs the other."),
    passages=[Passage(title="When Food and Power Compete for the Same Water", text=PASSAGE)],
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
    ],
    provenance={"copyright": "own_authored", "rights": "public-domain-sourced (US federal)",
                "authored": "2026-07-10",
                "note": "facts reuse verified USGS rows from the G11 test synth_water_scarcity bank; distinct "
                        "single-argument framing (food-vs-power water trade-off) at the G12 sophistication tier."},
)

if __name__ == "__main__":
    qc_stimulus(rec)
    import re
    wc = len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", PASSAGE))
    print(f"passage word count: {wc}")
    print(qc_report(rec))
    sys.exit(0 if rec.qc["passed"] else 1)
