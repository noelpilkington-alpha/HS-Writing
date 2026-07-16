"""
INFORMATIONAL LESSON stimulus for the G11 writing bank: how the United States uses its water, and where the
largest demands fall. Explain, do not argue.

bucket="lesson", family="single", mode="explanatory", grade=11 (register 1120-1300L). LESSON bucket: the
SECOND informational source the G11 synthesis lesson (C.11.02, T8) binds (paired with the energy-mix source
so synthesis has >=2 sources to weave), and usable for source-reading (C.11.08). Distinct explanatory framing
from the G11 TEST synthesis set; contamination-partitioned.

Every figure traces to a fetched federal page (US USGS, US EPA). Facts reused from the verified federal source
rows already documented in the G11 test bank (no re-fetch, no fabrication). 9-gate QC footer. No em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

PASSAGE = (
"Water is the one resource a modern country cannot substitute or manufacture, yet most people never think "
"about how much of it their society uses or where it goes. Knowing the answer turns vague worry about "
"droughts and shortages into something a writer can actually reason about. This passage explains how much "
"water the United States uses, which activities consume the most, and why the pattern matters.\n\n"

"Begin with the total, because the shares beneath it are what reveal the country's priorities. The U.S. "
"Geological Survey estimates that in 2015 the nation used about 322 billion gallons of water per day. Almost "
"all of that use is concentrated in a few activities. The Survey reports that around 90 percent of daily "
"water use goes toward just three categories: crop irrigation, thermoelectric power plants, and public "
"water supply. In other words, the water that keeps a country running is not spread evenly across a "
"thousand small uses; it is dominated by a handful of very large ones.\n\n"

"The two largest are worth examining closely, because they surprise most people. Thermoelectric power, the "
"water used to cool coal, gas, and nuclear plants that make electricity, withdrew about 133 billion gallons "
"per day in 2015, which the Survey reports was roughly 41 percent of all water withdrawals in the country. "
"That figure links water directly to energy: making electricity is one of the thirstiest things the nation "
"does. Irrigation, the water used to grow crops, withdrew about 118 billion gallons per day, which the "
"Survey reports accounted for about 42 percent of the country's freshwater withdrawals. Notice that the "
"two percentages rest on different totals. The 41 percent counts against all water withdrawn, salt water "
"included. The 42 percent counts against freshwater only, a smaller pool. That is why a smaller volume can "
"show the larger share, and the two figures do not conflict. Together, cooling power plants and watering "
"fields dominate the national water budget.\n\n"

"A crucial distinction hides inside those numbers: withdrawal is not the same as consumption. Much of the "
"water a power plant withdraws for cooling is returned to the river or lake it came from, warmer but "
"available for use downstream. Much of the water used to irrigate a field, by contrast, is taken up by "
"plants or evaporates, and does not return to the same source. So although thermoelectric and irrigation "
"withdrawals are close in size, irrigation removes far more water permanently. This is why two uses that "
"look similar on a chart can place very different long-term demands on a region's water.\n\n"

"That difference matters most where the water does not come back. In many parts of the country, irrigation "
"draws on groundwater, the water stored in aquifers underground. When farms pump groundwater faster than "
"rain and snow can refill it, the aquifer level drops, a process the Survey calls groundwater depletion. "
"Unlike a river that refills each year, a depleted aquifer can take decades or longer to recover, if it "
"recovers at all. The largest water uses, then, are not only large; some of them draw down a store that is "
"slow to replace.\n\n"

"Taken together, the evidence sketches a clear pattern. The United States uses a great deal of water, most "
"of it for just three purposes, and the two biggest, cooling power plants and irrigating crops, place very "
"different demands on the resource depending on whether the water returns. Explaining the pattern settles "
"no policy question by itself. But it shows why arguments about water, energy, and food are so tightly "
"knotted together. In the national water budget, they draw from the same supply."
)

rec = StimulusRecord(
    id="ACC-W910-INFO-LESSON-WATERUSE",
    grade="11", mode="explanatory", family="single", bucket="lesson",
    topic_id="us_water_use",
    annotated=False,
    modeling_anchor="SBAC explanatory / AP Lang synthesis source (single-source informational)",
    acc_tags=["ACC.W.INFO.1", "ACC.W.INFO.2", "CCSS.W.11-12.2"],
    prompt=("Write a well-organized informational composition that uses specific evidence from the article to "
            "explain how the United States uses its water and why the largest uses matter."),
    passages=[Passage(title="How America Uses Its Water", text=PASSAGE)],
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
                        "single explanatory framing (national water budget), partitioned from the test set."},
)

if __name__ == "__main__":
    qc_stimulus(rec)
    import re
    wc = len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", PASSAGE))
    print(f"passage word count: {wc}")
    print(qc_report(rec))
    sys.exit(0 if rec.qc["passed"] else 1)
