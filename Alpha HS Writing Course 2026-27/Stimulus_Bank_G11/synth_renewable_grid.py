"""
G11 SYNTHESIS SOURCE SET for the writing test bank (NEW multi-source shape, family="synthesis_set").
Debatable question: Can the United States power grid run mostly on renewable energy?
Four sources on one debatable question (SBAC 4-source / AP Lang synthesis model): three ~500-word
text sources plus one source that DESCRIBES a chart in words (visual/quantitative, exempt from the
480-word floor). Register is pinned to the G11 Lexile band (1120-1300L). Every numeric figure in the
prose traces to a real fetched federal page (US EIA, US DOE, NREL via DOE OSTI, US EPA), verified live
2026-07-09. Family=synthesis_set, mode=argument. Runs itself through the QC harness and reports.
No em dashes in prose.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# --- Source 1: US EIA -- the national generation mix and where it is heading -------------------
SOURCE_EIA = (
"For most of the last century, the United States produced its electricity by burning fossil fuels, and "
"that long-standing pattern is only now beginning to shift. According to the U.S. Energy Information "
"Administration, the nation's large power plants generated about 4,178 billion kilowatthours of "
"electricity in 2023. Most of that power still came from fossil fuels. Natural gas alone supplied about "
"43 percent of the nation's electricity, and coal supplied about 16 percent. Together the two fuels "
"accounted for close to 60 percent of the total. Nuclear reactors contributed nearly 19 percent. "
"Renewable sources, taken together, produced about 21 percent.\n\n"

"Within that renewable share, wind and solar have grown the fastest. The same agency reports that wind "
"supplied about 10 percent of the country's electricity in 2023, and solar supplied close to 4 percent. "
"Most of the remaining renewable power came from the nation's hydropower dams. Those dams have supplied "
"steady power for generations, but they can be built in only a limited number of places, so the newer "
"growth is coming from wind and solar instead. What stands out is how quickly these figures are "
"changing. Renewable generation passed nuclear generation for the first time in 2021, and it passed "
"coal generation for the first time in 2022. A source that was once a small part of the grid has "
"quietly grown into one of its largest contributors, and its rise shows no sign of slowing.\n\n"

"That growth is expected to continue in the near term. The Energy Information Administration projects "
"that solar generation will climb from 163 billion kilowatthours in 2023 to 286 billion kilowatthours "
"in 2025. That is an increase of about 75 percent in only two years. Wind generation is projected to "
"rise more gradually, from 430 billion kilowatthours to 476 billion kilowatthours over the same period. "
"New solar and wind farms are now joining the grid faster than any other kind of power plant. Much of "
"that new capacity is replacing older coal and gas stations as those plants retire from service.\n\n"

"These numbers explain why the debate over a renewable grid is no longer merely theoretical. The "
"country is already building a system in which wind and solar carry a growing portion of the load. The "
"genuine question is how far that shift can reasonably extend. Supplying one-fifth of the nation's "
"electricity from renewable sources is a real accomplishment. Supplying most of it, however, would "
"demand solving problems that grow steadily harder as the renewable share climbs toward the majority. "
"Those problems are not mainly about building more panels or turbines, which the country has shown it "
"can do quickly. They are about keeping supply and demand in balance at every hour once the easy share "
"of renewable power has already been added. To judge where the grid can go tomorrow, it helps to see "
"clearly where the grid stands today. The honest starting point is a system that still leans on fossil "
"fuels, yet tilts, year after year, toward the wind and the sun."
)

# --- Source 2: NREL (via DOE OSTI) -- feasibility of a mostly-renewable grid + what it requires -
SOURCE_NREL = (
"If wind and solar already supply a growing share of American electricity, a reasonable question "
"follows. Could they one day supply most of it? Researchers at the National Renewable Energy "
"Laboratory, a federal lab run for the U.S. Department of Energy, studied exactly this problem. Their "
"analysis of a fully clean power system found that there are several ways to reach a net-zero-carbon "
"grid by the year 2035 at a reasonable cost. In plain terms, the main barrier is not whether the goal "
"can be met. The barrier is what such a system would take to build and run.\n\n"

"The central problem is that wind and solar are variable. A wind farm makes power only when the wind "
"blows, and a solar array makes power only when the sun shines. Yet people use power in every hour of "
"every day, including calm nights when neither one is working. To keep supply and demand in balance at "
"those times, a grid that leans heavily on renewables must be able to store extra power made during "
"good hours and give it back later, when output falls short of what people need.\n\n"

"Storage is growing fast, though it is still small next to the size of the grid. The Energy Information "
"Administration reports that battery capacity at large power plants totaled around 16 gigawatts at the "
"end of 2023. Developers planned to add about 15 gigawatts in 2024 and another 9 gigawatts in 2025. "
"That growth is packed into a few states. California leads with about 7.3 gigawatts of battery "
"capacity, and Texas follows with about 3.2 gigawatts. Batteries like these can smooth the daily swings "
"of solar output. Storing power across a whole windless week, though, remains a much larger challenge "
"that today's batteries cannot yet meet.\n\n"

"Storage is only part of the job. A mostly renewable grid would also need thousands of miles of new "
"power lines to carry electricity from the sunny, windy places where it is cheapest to make toward the "
"far-off cities where it is used. It would need market rules rebuilt around changing supply rather than "
"steady fossil output. The lab's conclusion is cautiously hopeful, but it comes with a clear condition. "
"A mostly renewable grid can be built, but only if the nation is willing to spend, on a large scale, on "
"the storage and power lines that make renewable electricity steady. Without that spending, the same "
"weather that makes wind and solar clean would also make them shaky, and the promise of a renewable "
"grid would stall well short of its goal.\n\n"

"History offers some reassurance on this point. The country has rebuilt its grid before, stringing "
"power lines across the West in the last century and adding vast amounts of natural gas in this one. "
"The task ahead differs in scale, not in kind. What the laboratory stresses is that the choice is now "
"an economic and political one, not a purely scientific one. The tools exist; the open question is "
"whether the country will pay for them and build them fast enough."
)

# --- Source 3: US EPA -- the climate stakes and rising demand from electrification --------------
SOURCE_EPA = (
"Why does it matter whether the grid runs on renewable energy rather than fossil fuels? The clearest "
"answer involves pollution. Burning coal and natural gas to make electricity releases carbon dioxide, "
"the greenhouse gas most closely tied to a warming climate. The U.S. Environmental Protection Agency "
"reports that total American greenhouse gas emissions reached about 6,343 million metric tons of carbon "
"dioxide equivalent in 2022. Replacing fossil-fuel power with wind, solar, and other renewable sources "
"is one of the most direct ways to bring that yearly total down.\n\n"

"The power sector does not stand alone in this accounting. The Environmental Protection Agency reports "
"that transportation was the single largest source of greenhouse gas emissions in 2022. It was "
"responsible for about 28 percent of the national total. That fact is tied to the future of the grid in "
"a way that is easy to miss. As drivers slowly trade gasoline cars for electric ones, the pollution "
"once made by tailpipes shifts onto the power system instead. Whether that shift truly cuts emissions "
"depends on one thing: how the added electricity is made. A single electric car charged on a coal-heavy "
"grid can pollute nearly as much as the gasoline car it replaced. The same car charged on a clean grid "
"pollutes far less. The grid, not the car, sets the limit.\n\n"

"This link leads to a demanding conclusion. Electric cars, trucks, and home heating will raise the "
"total amount of electricity the country must generate. The increase may be large over the coming "
"decades. Suppose that added demand is met by burning still more natural gas. In that case, the climate "
"benefit of electric vehicles largely disappears. Suppose instead that it is met by renewable power. "
"Then the same shift toward electric machines delivers a real drop in emissions across the wider "
"economy.\n\n"

"For this reason, the agency treats the makeup of the grid as a decision that reaches well beyond the "
"power sector. A grid that runs mostly on renewables would lower the emissions produced in making "
"electricity today. It would also decide whether the broader move toward electric transportation and "
"heating actually reaches its goal. The environmental case for a renewable grid, in short, rests on two "
"things. It rests on the electricity Americans already use. It rests even more on the far larger amount "
"they are likely to demand as the economy keeps electrifying.\n\n"

"Seen this way, the fuel that powers the grid is not just one choice among many. It is the choice that "
"shapes how clean the rest of modern life can become. A dirty grid spreads its pollution into every "
"device plugged into it. A clean grid does the reverse, quietly cleaning each car, furnace, and factory "
"that draws on it. That is why the agency views the grid's fuel mix as a lever with unusually long "
"reach, one that can move emissions across the whole economy rather than the power sector alone."
)

# --- Source 4: US DOE -- DESCRIBED CHART (visual/quantitative), exempt from the 480-word floor --
SOURCE_DOE_CHART = (
"The bar chart below, drawn from data published by the U.S. Department of Energy, compares the 2024 "
"capacity factor of each major source of electricity. A capacity factor measures how much power a plant "
"actually produced over the year against the maximum it could have produced if it had run at full "
"output the entire time. A higher bar means a more consistently available source.\n\n"
"The tallest bar belongs to nuclear power, which ran at more than 92 percent of its maximum capacity in "
"2024. Natural gas follows at about 59.9 percent, and coal at about 42.36 percent. The two renewable "
"sources at the center of the debate sit noticeably lower on the chart. Wind registers a capacity "
"factor of about 34.3 percent, and solar about 23.4 percent.\n\n"
"The visual gap tells the essential story. The renewable bars are less than half the height of the "
"nuclear bar, not because their equipment is faulty, but because the wind and sun are intermittent. A "
"reader should draw the intended inference carefully. A low capacity factor does not mean a source is "
"unimportant. It means that far more renewable capacity must be built, and paired with storage, to "
"deliver the same steady supply that a single high-capacity-factor plant provides on its own."
)

REC = StimulusRecord(
    id="ACC-W910-SYNTH-SET-0001",
    grade="11", mode="argument", family="synthesis_set",
    bucket="test", form="4trait", annotated=False,
    modeling_anchor="SBAC G11 full-write / AP Lang synthesis",
    acc_tags=["ACC.W.SRC.1", "ACC.W.INFO.2", "CCSS.W.11-12.7", "CCSS.W.11-12.8"],
    topic_id="renewable_grid_synthesis",
    prompt=("These four sources address one debatable question: can the United States power grid run "
            "mostly on renewable energy? Drawing on at least three of the sources, write an essay that "
            "develops and defends your own position. Synthesize the sources to support your argument "
            "rather than summarizing them one by one, and cite each source you use."),
    passages=[
        Passage(title="Where the Grid Gets Its Power Today",
                angle="national generation data (US EIA)", text=SOURCE_EIA),
        Passage(title="Is a Mostly Renewable Grid Feasible?",
                angle="clean-grid feasibility modeling (NREL, via DOE)", text=SOURCE_NREL),
        Passage(title="Why the Grid's Fuel Mix Matters for the Climate",
                angle="environmental and emissions vantage (US EPA)", text=SOURCE_EPA),
        Passage(title="How Often Each Power Source Actually Runs",
                angle="visual quantitative (chart): capacity factors by source (US DOE)",
                text=SOURCE_DOE_CHART),
    ],
    fact_sources=[
        FactSource("Total US utility-scale electricity generation, 2023", "4,178 billion kilowatthours",
                   "US EIA", "https://www.eia.gov/tools/faqs/faq.php?id=427&t=3",
                   "4,178 billion kilowatthours"),
        FactSource("Fossil-fuel share of US electricity, 2023", "60 percent", "US EIA",
                   "https://www.eia.gov/tools/faqs/faq.php?id=427&t=3",
                   "About 60% of this electricity generation was from fossil fuels"),
        FactSource("Natural gas share of US electricity, 2023", "43 percent", "US EIA",
                   "https://www.eia.gov/tools/faqs/faq.php?id=427&t=3", "Natural gas 43.1%"),
        FactSource("Coal share of US electricity, 2023", "16 percent", "US EIA",
                   "https://www.eia.gov/tools/faqs/faq.php?id=427&t=3", "Coal 16.2%"),
        FactSource("Nuclear share of US electricity, 2023", "19 percent", "US EIA",
                   "https://www.eia.gov/tools/faqs/faq.php?id=427&t=3", "About 19% was from nuclear energy"),
        FactSource("Renewable share of US electricity, 2023", "21 percent", "US EIA",
                   "https://www.eia.gov/tools/faqs/faq.php?id=427&t=3", "about 21% was from renewable energy sources"),
        FactSource("Wind share of US electricity, 2023", "10 percent", "US EIA",
                   "https://www.eia.gov/tools/faqs/faq.php?id=427&t=3", "Wind 10.2%"),
        FactSource("Solar share of US electricity, 2023", "4 percent", "US EIA",
                   "https://www.eia.gov/tools/faqs/faq.php?id=427&t=3", "Solar (total) 3.9%"),
        FactSource("Solar generation projection, 2023 to 2025", "163 to 286 billion kilowatthours (75 percent)",
                   "US EIA", "https://www.eia.gov/todayinenergy/detail.php?id=61242",
                   "solar power generation will grow 75% from 163 billion kilowatthours (kWh) in 2023 to 286 billion kWh in 2025"),
        FactSource("Wind generation projection, 2023 to 2025", "430 to 476 billion kilowatthours",
                   "US EIA", "https://www.eia.gov/todayinenergy/detail.php?id=61242",
                   "wind power generation will grow 11% from 430 billion kWh in 2023 to 476 billion kWh in 2025"),
        FactSource("Renewables surpassed nuclear (2021) and coal (2022)", "2021 / 2022", "US EIA",
                   "https://www.eia.gov/todayinenergy/detail.php?id=61242",
                   "surpassed nuclear generation for the first time in 2021 and coal generation for the first time in 2022"),
        FactSource("100 percent clean grid feasible by 2035 (multiple cost-effective approaches)", "2035", "NREL",
                   "https://www.osti.gov/biblio/1885591",
                   "multiple approaches to cost-effectively achieve a net-zero carbon grid in 2035"),
        FactSource("US utility-scale battery capacity at end of 2023", "16 gigawatts", "US EIA",
                   "https://www.eia.gov/todayinenergy/detail.php?id=61202",
                   "utility-scale battery capacity totaled around 16 GW at the end of 2023"),
        FactSource("Planned battery additions, 2024 and 2025", "15 gigawatts / 9 gigawatts", "US EIA",
                   "https://www.eia.gov/todayinenergy/detail.php?id=61202",
                   "Developers plan to add another 15 GW in 2024 and around 9 GW in 2025"),
        FactSource("California installed battery capacity", "7.3 gigawatts", "US EIA",
                   "https://www.eia.gov/todayinenergy/detail.php?id=61202",
                   "California has the most installed battery storage capacity of any state, with 7.3 GW"),
        FactSource("Texas installed battery capacity", "3.2 gigawatts", "US EIA",
                   "https://www.eia.gov/todayinenergy/detail.php?id=61202", "followed by Texas with 3.2 GW"),
        FactSource("Total US greenhouse gas emissions, 2022", "6,343 million metric tons", "US EPA",
                   "https://www.epa.gov/ghgemissions/inventory-us-greenhouse-gas-emissions-and-sinks",
                   "U.S. greenhouse gas emissions totaled 6,343 million metric tons of carbon dioxide equivalents"),
        FactSource("Transportation share of US greenhouse gas emissions, 2022", "28 percent", "US EPA",
                   "https://www.epa.gov/greenvehicles/fast-facts-transportation-greenhouse-gas-emissions",
                   "transportation accounted for the largest portion (28%) of total U.S. GHG emissions in 2022"),
        FactSource("Nuclear capacity factor, 2024", "92 percent", "US DOE",
                   "https://www.energy.gov/ne/articles/what-generation-capacity",
                   "producing reliable and secure power more than 92% of the time"),
        FactSource("Natural gas capacity factor, 2024", "59.9 percent", "US DOE",
                   "https://www.energy.gov/ne/articles/what-generation-capacity", "natural gas (59.9%)"),
        FactSource("Coal capacity factor, 2024", "42.36 percent", "US DOE",
                   "https://www.energy.gov/ne/articles/what-generation-capacity", "coal (42.36%)"),
        FactSource("Wind capacity factor, 2024", "34.3 percent", "US DOE",
                   "https://www.energy.gov/ne/articles/what-generation-capacity", "wind (34.3%)"),
        FactSource("Solar capacity factor, 2024", "23.4 percent", "US DOE",
                   "https://www.energy.gov/ne/articles/what-generation-capacity", "solar (23.4%)"),
    ],
    provenance={"copyright": "own_authored",
                "rights": "public-domain-sourced (US federal)",
                "authored": "2026-07-09"},
)

qc = qc_stimulus(REC)
print(qc_report(REC))
import sys
sys.exit(0 if qc["passed"] else 1)
