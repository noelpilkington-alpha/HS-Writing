"""
Single-source EXPLANATORY LESSON stimulus for the G10 writing bank: how recycling and materials
recovery work (the recovery process, recovery rates, contamination). Explain, do not argue.

bucket="lesson", family="single", mode="explanatory". Every figure traces to a fetched federal
page (US EPA). Runs itself through the QC harness and reports. No em dashes in prose.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# Explanatory passage, G10 register, neutral tone. Every figure from a fetched federal page.
PASSAGE = (
"When a bottle drops into a blue bin, it looks like the end of a story. In truth, it is the beginning of "
"one. That bottle now enters a long chain of trucks, machines, and factories that can turn old material "
"into new products. That chain is called materials recovery. This passage explains how recycling works, "
"how much of the nation's waste is actually recovered, and why one common mistake can undo the whole "
"effort.\n\n"

"Start with the scale of the problem. The U.S. Environmental Protection Agency, or EPA, tracks the trash "
"the country makes. In 2018, Americans generated about 292.4 million tons of what the agency calls "
"municipal solid waste. That works out to roughly 4.9 pounds per person each day. Not all of that waste "
"is thrown away, though. In the same year, more than 69 million tons were recycled. Another 25 million "
"tons were composted. Together, recycling and composting handled almost 94 million tons of material. That "
"is a recycling and composting rate of about 32 percent.\n\n"

"How does the recovery actually happen? The journey usually starts at the curb. Trucks carry the mixed "
"contents of recycling bins to a building called a materials recovery facility. Inside, the material "
"moves along conveyor belts. Workers and machines then sort it into clean streams: paper here, aluminum "
"there, glass and plastic in their own bins. Magnets pull out steel cans. Screens and spinning disks "
"separate flat paper from round containers. Once the material is sorted and pressed into bales, it is "
"sold to factories. There it becomes the raw stock for new goods.\n\n"

"Recovery matters because making a product from recycled material often takes far less energy than making "
"it from scratch. Aluminum is the clearest example. The EPA reports that recycling just one ton of "
"aluminum cans saves more than 152 million Btu of energy. That is about the same as 1,024 gallons of "
"gasoline. Paper shows a similar gain. The agency notes that recycling one ton of office paper can save "
"the energy equal to 322 gallons of gasoline. Those savings add up across millions of tons, and they cut "
"both pollution and cost.\n\n"

"Recycling also supports the economy. In a study of 2012 data, the EPA found that recycling and reuse "
"activities accounted for about 681,000 jobs in a single year. The same activities produced tens of "
"billions of dollars in wages. So the material in a blue bin is not only waste to be managed. It is also "
"a resource that people are paid to recover.\n\n"

"There is a catch, though, and it is a serious one. The sorting system only works when the right things "
"go in the bin. When people toss in items that do not belong, they cause a problem the industry calls "
"contamination. A greasy pizza box, a tangle of plastic bags, or a jar still full of food can foul a "
"whole load. The bags wrap around the spinning machines and jam them. The food soaks into paper and ruins "
"it. If a batch is too dirty, a recycling plant may have to send the entire load to a landfill instead. "
"In that case, the effort of every careful household is wasted along with it.\n\n"

"That is why experts stress a simple rule. It is better to leave a doubtful item out of the bin than to "
"toss it in and hope. Clean, correctly sorted material keeps the recovery chain running. Dirty material "
"breaks it. The numbers from the EPA show that the nation already recovers a large share of its waste. "
"They also show how much still ends up buried. Understanding how the system works, and how easily it can "
"be fouled, is the first step toward making it work better."
)

rec = StimulusRecord(
    id="ACC-W910-INFO-LESSON-RECYCLING",
    grade="9-10", mode="explanatory", family="single", bucket="lesson",
    topic_id="recycling_recovery",
    annotated=False,
    modeling_anchor="STAAR English II / MCAS (single-source informational)",
    acc_tags=["ACC.W.INFO.1", "ACC.W.INFO.4", "CCSS.W.9-10.2"],
    prompt=("Write a well-organized informational composition that uses specific evidence from the article "
            "\"What Happens to What You Recycle\" to explain how materials recovery works, how much of the "
            "nation's waste is recovered, and why contamination threatens the process."),
    passages=[Passage(title="What Happens to What You Recycle", text=PASSAGE)],
    fact_sources=[
        FactSource("Municipal solid waste generated in 2018", "292.4 million tons", "US EPA",
                   "https://www.epa.gov/facts-and-figures-about-materials-waste-and-recycling/national-overview-facts-and-figures-materials",
                   "In 2018, about 292.4 million tons of MSW were generated"),
        FactSource("Waste generated per person per day in 2018", "4.9 pounds", "US EPA",
                   "https://www.epa.gov/facts-and-figures-about-materials-waste-and-recycling/national-overview-facts-and-figures-materials",
                   "approximately 4.9 pounds per person per day"),
        FactSource("Amount recycled in 2018", "69 million tons", "US EPA",
                   "https://www.epa.gov/facts-and-figures-about-materials-waste-and-recycling/national-overview-facts-and-figures-materials",
                   "Of the MSW generated, approximately ... more than 69 million tons were recycled"),
        FactSource("Amount composted in 2018", "25 million tons", "US EPA",
                   "https://www.epa.gov/facts-and-figures-about-materials-waste-and-recycling/national-overview-facts-and-figures-materials",
                   "25 million tons were composted"),
        FactSource("Recycling + composting combined tonnage and rate in 2018", "94 million tons / 32 percent",
                   "US EPA",
                   "https://www.epa.gov/facts-and-figures-about-materials-waste-and-recycling/national-overview-facts-and-figures-materials",
                   "almost 94 million tons ... a 32.1 percent recycling and composting rate"),
        FactSource("Energy saved by recycling one ton of aluminum cans", "152 million Btu / 1,024 gallons",
                   "US EPA",
                   "https://www.epa.gov/recycle/frequent-questions-recycling",
                   "Recycling just one ton of aluminum cans conserves more than 152 million Btu, the equivalent of 1,024 gallons of gasoline"),
        FactSource("Energy saved by recycling one ton of office paper", "322 gallons", "US EPA",
                   "https://www.epa.gov/recycle/frequent-questions-recycling",
                   "Recycling one ton of office paper can save the energy equivalent of consuming 322 gallons of gasoline"),
        FactSource("Jobs supported by recycling and reuse (2012 REI data)", "681,000", "US EPA",
                   "https://www.epa.gov/smm/recycling-economic-information-rei-report",
                   "recycling and reuse activities in the United States accounted for 681,000 jobs"),
        FactSource("Contamination can send a recyclable load to landfill", "", "US EPA",
                   "https://www.epa.gov/recycle/frequent-questions-recycling",
                   "items in the recycling bin that can ... t be recycled can contaminate the recycling stream"),
    ],
    provenance={"copyright": "own_authored", "rights": "public-domain-sourced (US federal)",
                "authored": "2026-07-08"},
)

if __name__ == "__main__":
    qc_stimulus(rec)
    import re
    wc = len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", PASSAGE))
    print(f"passage word count: {wc}")
    print(qc_report(rec))
    sys.exit(0 if rec.qc["passed"] else 1)
