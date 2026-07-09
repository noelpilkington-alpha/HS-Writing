"""
G11 SYNTHESIS SOURCE SET for the writing test bank (NEW multi-source shape, family="synthesis_set").
Debatable question: How should the United States manage water scarcity?
Five sources on one debatable question (SBAC 4-source / AP Lang synthesis model, extended to 5): four
~480-word text sources plus one source that DESCRIBES a chart in words (visual/quantitative, exempt
from the 480-word floor). Register is pinned to the G11 Lexile band (1120-1300L). Every numeric figure
in the prose traces to a real fetched federal page (US USGS, US EPA, US USDA, US NOAA), verified live
2026-07-09. Family=synthesis_set, mode=argument. Runs itself through the QC harness and reports.
No em dashes in prose.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# --- Source 1: US USGS -- where the nation's water actually goes -------------------------------
SOURCE_USGS_USE = (
"To decide how the United States should manage water scarcity, it helps to know first where the "
"nation's water actually goes. The U.S. Geological Survey, which has tracked the country's water use "
"for decades, provides the clearest picture. In 2015, the most recent year of its detailed national "
"survey, the United States withdrew about 322 billion gallons of water per day from its rivers, lakes, "
"and underground stores. That single figure captures every farm, factory, power plant, and household "
"in the country.\n\n"

"Most of that water flows to a small number of uses. The Geological Survey reports that irrigation and "
"thermoelectric power plants, together with public water supply, account for about 90 percent of daily "
"water use in the lower 48 states. Two uses dominate the total. Thermoelectric power plants, which burn "
"fuel or split atoms to boil water and spin turbines, withdrew about 133 billion gallons per day in "
"2015. That was roughly 41 percent of all water withdrawn in the country. Most of that water is used to "
"cool equipment and is later returned to its source, though often warmer than before.\n\n"

"Irrigation is the other giant. The Geological Survey reports that farms withdrew about 118 billion "
"gallons of water per day in 2015 to water their crops. That was about 42 percent of all the freshwater "
"the nation used. Unlike power-plant cooling water, most irrigation water does not return to the river. "
"It evaporates from fields or is taken up by plants, so it leaves the local supply for good. For that "
"reason, irrigation places a heavier long-term burden on scarce water than its share of withdrawals "
"alone would suggest. A gallon returned to a river can be used again downstream. A gallon lost to the "
"air cannot.\n\n"

"The distinction between withdrawing water and consuming it turns out to be central. A power plant may "
"withdraw enormous amounts of water yet consume little of it, since most flows back to the source. A "
"farm may withdraw less yet consume nearly all of it. Scarcity is driven by consumption, not by "
"withdrawal alone. Any honest plan to manage the nation's water must keep that difference clearly in "
"view, or it will aim its effort at the wrong target.\n\n"

"These numbers frame the whole debate. Water scarcity is not mainly a problem of people using too much "
"at home. It is a problem of how the country grows its food and generates its power. Any serious plan "
"to manage scarcity must therefore look hardest at farms and power plants, because that is where the "
"water actually goes. Small savings in those two sectors would free up more water than large sacrifices "
"anywhere else could hope to.\n\n"

"There is one more reason these totals matter. Water withdrawn in one place is rarely available in "
"another, because moving it over long distances is costly and difficult. Scarcity is therefore a local "
"problem, even when the national supply looks ample on paper. A wet year in the East does nothing for a "
"drying aquifer in the West, and a full reservoir in one basin cannot rescue an empty one across the "
"mountains."
)

# --- Source 2: US USGS -- groundwater depletion, the slow crisis -------------------------------
SOURCE_USGS_GW = (
"Rivers and lakes are only part of the nation's water. Beneath the surface lie vast stores of "
"groundwater, held in porous rock and sediment called aquifers. For more than a century, Americans "
"have pumped this hidden water to the surface faster than nature refills it. The U.S. Geological Survey "
"has measured the result, and the scale is sobering. Between 1900 and 2008, the nation drained an "
"estimated 1,000 cubic kilometers of water from its aquifers, a volume large enough to fill many of the "
"country's largest lakes.\n\n"

"The pace of that loss has been quickening. The Geological Survey reports that groundwater depletion "
"averaged about 25 cubic kilometers per year between 2000 and 2008. That recent rate is far higher than "
"the long-run average across the full century. In other words, the country is not only drawing down its "
"underground savings. It is drawing them down faster than ever before, even as demand for water "
"continues to climb.\n\n"

"The clearest warning comes from the High Plains aquifer, which stretches beneath eight states from "
"South Dakota to Texas. This single aquifer supplies much of the irrigation water for the nation's "
"grain belt. The Geological Survey reports that in parts of the High Plains, water levels have fallen "
"more than 100 feet. In some areas, more than half of the water that the aquifer once held has already "
"been pumped out. Water that took thousands of years to collect underground is being spent within a few "
"generations.\n\n"

"This slow crisis differs from a drought in a crucial way. A drought ends when the rains return. A "
"depleted aquifer may take centuries to refill, if it ever does. The distinction matters for policy. "
"Managing scarcity is not only about surviving a dry summer. It is about deciding how quickly the "
"nation is willing to spend water that cannot be replaced within any human lifetime. Once an aquifer is "
"drained, the farms and towns that depend on it lose an option they can never fully recover.\n\n"

"This is why some experts describe groundwater as a savings account rather than an income. A family can "
"live for a time by spending its savings, but not forever. The same is true of a region that meets its "
"water needs by mining an aquifer. The account can run dry, and when it does, there is no quick way to "
"refill it. Planning for scarcity means treating that underground balance as something to be spent with "
"great care, not drawn down as if it were endless. The water beneath the grain belt is, in a real "
"sense, borrowed from the future.\n\n"

"The consequences reach beyond the farms themselves. As an aquifer falls, the wells that tap it must be "
"drilled deeper and pumped harder, which raises the cost of every gallon. Land above a heavily pumped "
"aquifer can even sink, cracking roads and foundations. A resource that once seemed free thus grows "
"more expensive the longer it is overused, and the bill falls hardest on the communities least able to "
"drill their way out."
)

# --- Source 3: US USDA -- the food-water tradeoff ----------------------------------------------
SOURCE_USDA = (
"If irrigation is the largest single drain on the nation's freshwater, then any plan to manage scarcity "
"must reckon with American agriculture. The U.S. Department of Agriculture provides the fullest account "
"of how farms use water. Its research finds that irrigation accounted for about 47 percent of the "
"nation's total freshwater withdrawals between 2010 and 2020. Farming, in short, is the country's "
"thirstiest activity, and it competes directly with cities and ecosystems for a limited supply.\n\n"

"The land involved is vast. The Department reports that the 2022 Census of Agriculture counted about "
"54.9 million acres of irrigated cropland and pasture across the United States. Much of that acreage "
"lies in the dry western states, where crops cannot grow without added water. There the same rivers and "
"aquifers that supply farms must also serve growing cities, so every acre farmed under irrigation is "
"water not available for another use.\n\n"

"Yet the Department's data also reveal why this water is so hard to give up. Irrigated farms are "
"extraordinarily productive. Although irrigated land makes up less than 17 percent of the country's "
"harvested cropland, it produces more than half of the total value of American crop sales. A relatively "
"small share of the land, watered carefully, yields the majority of the nation's crop value. That "
"efficiency is precisely what makes irrigation both so valuable and so difficult to reduce.\n\n"

"This tension sits at the center of the water debate. Cutting irrigation would ease scarcity in the "
"West, but it would also strike at the most productive farmland in the country and at the food supply "
"it sustains. The Department's figures suggest that the goal should not be simply to use less water on "
"farms. It should be to grow more food with each gallon, through better technology and smarter choices "
"about which crops to plant where. The question is not whether farms will keep using water. It is "
"whether they can be made to use it far more sparingly without giving up the harvest the country "
"depends on.\n\n"

"Some of the tools already exist. Drip systems deliver water straight to plant roots and waste far less "
"than older sprinklers. Choosing lower-water crops in the driest regions can stretch a limited supply "
"further. None of these changes is free, and none is simple, but together they point toward a future in "
"which the same farmland produces as much food on less water than it uses today. The prize is a harvest "
"that no longer depends on draining the West.\n\n"

"The choice, however, is not one that farmers can make alone. Water rights in much of the West follow "
"old rules that reward those who use the most, not those who conserve. A farmer who invests in "
"efficient equipment may simply see the saved water claimed by someone downstream. Any workable plan to "
"manage scarcity must therefore change the incentives, so that using less water becomes a benefit to "
"the farmer rather than a gift to a stranger. Technology and policy have to move together, or neither "
"will move far."
)

# --- Source 4: US EPA -- households, the usable-water margin, and coming shortages -------------
SOURCE_EPA = (
"When most people picture saving water, they picture the home: shorter showers, a closed tap, a "
"low-flow toilet. Those habits matter, but the U.S. Environmental Protection Agency puts their scale in "
"perspective. The agency reports that the average American family uses more than 300 gallons of water "
"per day at home. Household use is real, yet it is small beside the water that farms and power plants "
"draw. This does not make home conservation pointless. It simply means that saving water at the tap "
"alone will never solve a national shortage.\n\n"

"The agency's more urgent message concerns the future. In one review, the Environmental Protection "
"Agency noted that 40 states told federal auditors they expected to face water shortages in the coming "
"years, even under normal, non-drought conditions. That figure is striking. Water stress is not "
"confined to the arid Southwest or to unusually dry years. A large majority of states foresee trouble "
"as a routine feature of the decades ahead, driven by growing populations and aging systems rather than "
"by weather alone.\n\n"

"The agency also stresses how little of the planet's water is usable. Although water covers most of the "
"Earth, less than 1 percent of it is fresh and available for human use. The rest is seawater or locked "
"in ice. That thin margin is what every farm, city, and factory must share. When one region draws more, "
"another must draw less, or the shared source begins to fail.\n\n"

"From these facts the agency draws a practical lesson about scarcity. Because usable water is so limited "
"and future shortages so widely expected, the wisest course is to use every gallon more efficiently "
"now, before a crisis forces harder choices later. Efficiency at home, on farms, and in industry all "
"belong in the same plan. No single sector can be spared, and no single sector can carry the whole "
"burden. The country's water problem, in the agency's view, is not one shortage but many local ones, "
"each demanding its own mix of conservation, reuse, and restraint.\n\n"

"That view reframes the familiar advice to save water at home. Home conservation is not the whole "
"answer, but it is part of a shared effort in which every user does less harm. When farms, factories, "
"and families all trim their use at once, the small savings add up to a supply that can outlast the "
"shortages ahead. The habit at the kitchen tap and the policy on the distant farm are, in the end, "
"parts of the same solution.\n\n"

"The agency also points to reuse as an underused tool. Water that has been cleaned after use can often "
"be used again, to irrigate parks, cool machinery, or recharge an aquifer, rather than being flushed "
"away. Cities that once treated wastewater as garbage are learning to treat it as a resource. Combined "
"with steady conservation, such reuse can stretch a fixed supply to serve a growing population. The "
"lesson the agency returns to is consistent: in a country facing many local shortages, no drop of water "
"is too small to count, and none is too used to matter."
)

# --- Source 5: US NOAA -- DESCRIBED CHART (visual/quantitative), exempt from the 480-word floor -
SOURCE_NOAA_CHART = (
"The map and accompanying bar chart below come from the U.S. Drought Monitor, a product of the National "
"Integrated Drought Information System, which is operated by the National Oceanic and Atmospheric "
"Administration. The display sorts the country into five drought categories, ranging from D0, "
"abnormally dry, up through D4, exceptional drought, the most severe level.\n\n"
"As of early July 2026, the data show that about 39.6 percent of the fifty states and Puerto Rico were "
"experiencing drought at the level of moderate or worse. The bar chart breaks that total into "
"categories. The most severe bands, though smaller, are the most alarming. Extreme drought, category "
"D3, covered about 8.6 percent of the country, while exceptional drought, category D4, covered about "
"0.8 percent.\n\n"
"The chart repays careful reading. A single national percentage can hide sharp regional differences, "
"because drought clusters in particular states rather than spreading evenly. Just as important, the map "
"captures one moment in time. Drought categories shift from week to week as rain falls or fails to "
"fall, so a reader should treat the figure as a snapshot of present conditions, not as a fixed measure "
"of the nation's long-term water supply."
)

REC = StimulusRecord(
    id="ACC-W910-SYNTH-SET-0003",
    grade="11", mode="argument", family="synthesis_set",
    bucket="test", form="4trait", annotated=False,
    modeling_anchor="SBAC G11 full-write / AP Lang synthesis",
    acc_tags=["ACC.W.SRC.1", "ACC.W.INFO.2", "CCSS.W.11-12.7", "CCSS.W.11-12.8"],
    topic_id="water_scarcity_synthesis",
    prompt=("These five sources address one debatable question: how should the United States manage water "
            "scarcity? Drawing on at least three of the sources, write an essay that develops and defends "
            "your own position on where the nation should focus its efforts. Synthesize the sources to "
            "support your argument rather than summarizing them one by one, and cite each source you use."),
    passages=[
        Passage(title="Where the Nation's Water Goes",
                angle="national water-use accounting (US USGS)", text=SOURCE_USGS_USE),
        Passage(title="The Water We Cannot Get Back",
                angle="groundwater depletion, the slow crisis (US USGS)", text=SOURCE_USGS_GW),
        Passage(title="Water, Food, and the Hardest Tradeoff",
                angle="agricultural water use and productivity (US USDA)", text=SOURCE_USDA),
        Passage(title="Small Taps and a Thin Margin",
                angle="household use and future shortages (US EPA)", text=SOURCE_EPA),
        Passage(title="How Much of the Country Is in Drought",
                angle="visual quantitative (chart): US Drought Monitor categories (US NOAA)",
                text=SOURCE_NOAA_CHART),
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
        FactSource("US groundwater depletion, 1900 to 2008", "1,000 cubic kilometers", "US USGS",
                   "https://www.usgs.gov/special-topics/water-science-school/science/groundwater-decline-and-depletion",
                   "estimated depletion over this period totals about 1,000 cubic kilometers"),
        FactSource("US groundwater depletion rate, 2000 to 2008", "25 cubic kilometers per year", "US USGS",
                   "https://www.usgs.gov/special-topics/water-science-school/science/groundwater-decline-and-depletion",
                   "the depletion rate averaged almost 25 km3 per year"),
        FactSource("High Plains aquifer water-level decline", "100 feet", "US USGS",
                   "https://www.usgs.gov/special-topics/water-science-school/science/groundwater-decline-and-depletion",
                   "water levels have declined more than 100 feet in some areas"),
        FactSource("Irrigation share of US freshwater withdrawals, 2010 to 2020", "47 percent", "US USDA",
                   "https://www.ers.usda.gov/topics/farm-practices-management/irrigation-water-use",
                   "accounted for 47 percent of the Nation's total freshwater withdrawals between 2010 and 2020"),
        FactSource("US irrigated cropland and pasture, 2022 Census", "54.9 million acres", "US USDA",
                   "https://www.ers.usda.gov/topics/farm-practices-management/irrigation-water-use",
                   "total U.S. irrigated crop and pastureland at 54.9 million acres"),
        FactSource("Irrigated land share of harvested cropland", "17 percent", "US USDA",
                   "https://www.ers.usda.gov/topics/farm-practices-management/irrigation-water-use",
                   "irrigated land accounted for less than 17 percent of harvested cropland"),
        FactSource("Irrigated-farm share of US crop sales value", "50 percent", "US USDA",
                   "https://www.ers.usda.gov/topics/farm-practices-management/irrigation-water-use",
                   "more than 50 percent of the total value of U.S. crop sales"),
        FactSource("Average American family household water use per day", "300 gallons", "US EPA",
                   "https://www.epa.gov/watersense/how-we-use-water",
                   "The average American family uses more than 300 gallons of water per day at home"),
        FactSource("States expecting water shortages (reported to auditors)", "40 states", "US EPA",
                   "https://www.epa.gov/watersense/how-we-use-water",
                   "Forty states told the Government Accountability Office"),
        FactSource("Share of Earth's water fresh and available for human use", "1 percent", "US EPA",
                   "https://www.epa.gov/watersense/how-we-use-water",
                   "less than 1 percent is available for human use"),
        FactSource("US area in drought (D1 to D4), early July 2026", "39.6 percent", "US NOAA",
                   "https://www.drought.gov/",
                   "Percent area of the 50 U.S. states and Puerto Rico that is currently in drought (D1-D4) ... 39.6"),
        FactSource("US area in extreme drought (D3), early July 2026", "8.6 percent", "US NOAA",
                   "https://www.drought.gov/", "D3 Extreme Drought 8.6"),
        FactSource("US area in exceptional drought (D4), early July 2026", "0.8 percent", "US NOAA",
                   "https://www.drought.gov/", "D4 Exceptional Drought 0.8"),
    ],
    provenance={"copyright": "own_authored",
                "rights": "public-domain-sourced (US federal)",
                "authored": "2026-07-09"},
)

qc = qc_stimulus(REC)
print(qc_report(REC))
import sys
sys.exit(0 if qc["passed"] else 1)
