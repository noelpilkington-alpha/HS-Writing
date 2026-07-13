"""
Single-source EXPLANATORY TEST stimulus for the G9 (English I) writing test bank: honeybees, how a hive
works, and the role their pollination plays in the food supply. Explain, do not argue.

Framed as HONEYBEE BIOLOGY + HIVES (topic_id="honeybees"), deliberately distinct from the G10
"pollinators" stimulus (which covers pollinators in general). bucket="test", form="mcas",
family="single", mode="explanatory", grade="9" (gates Lexile at the English I band 1010-1150L). Every
figure traces to a fetched federal page (USDA Agricultural Research Service, NOAA-independent: US NPS,
US EPA), fetched live 2026-07-08. Not annotated (test bucket). Runs itself through the QC harness and
reports. No em dashes in prose.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# Explanatory passage, G9 register (short sentences, fewer polysyllabic words). Every figure from a
# fetched federal page.
PASSAGE = (
"A single honeybee seems almost too small to matter. It weighs less than a paper clip and lives only a "
"few weeks. Yet honeybees, working together, help grow a huge share of the food we eat. This passage "
"explains how a honeybee hive works, how bees pollinate crops as they feed, and why the health of the "
"honeybee matters to farmers and families alike.\n\n"

"A honeybee never lives alone. Instead, it lives in a large group called a colony, or hive. A single "
"hive can hold tens of thousands of bees. The bees are not all the same, though. Most of them are worker "
"bees, and the U.S. Environmental Protection Agency notes that these workers do nearly all the labor of "
"the colony. One queen lays the eggs. The workers gather food, build the comb, and guard the entrance. "
"Each day, thousands of workers fly out to search for flowers. This teamwork is what keeps the hive "
"alive.\n\n"

"That search for food is where pollination happens. Honeybees visit flowers to drink a sweet liquid "
"called nectar. The U.S. National Park Service explains that as bees drink nectar or land on a flower, "
"pollen sticks to their bodies. When a bee flies to the next flower, some of that pollen rubs off. The "
"Park Service explains that this simple movement fertilizes the plant. It helps the plant make the "
"seeds, fruits, and new plants that follow. The bee is only looking for a meal. Without knowing it, the "
"bee is also helping the plant reproduce.\n\n"

"The scale of this quiet work is enormous. The U.S. Department of Agriculture reports that pollination "
"by managed honeybee colonies adds at least 18 billion dollars to the value of American agriculture each "
"year. The same agency offers an even more striking fact. It reports that about one mouthful in three of "
"our diet benefits from honeybee pollination, either directly or indirectly. Some crops depend on the "
"honeybee almost completely. The agency notes that almonds, for example, rely on honeybees for nearly "
"all of their pollination.\n\n"

"Because so much food depends on them, a drop in honeybee numbers is a serious concern. The USDA reports "
"that the number of managed honeybee colonies in the United States has fallen sharply. It dropped from "
"about 5 million colonies in the 1940s to roughly 2.66 million today. Beekeepers have also faced sudden "
"and mysterious losses. The agency reports that in October 2006, some beekeepers began losing 30 to 90 "
"percent of their hives. Scientists named this troubling pattern Colony Collapse Disorder.\n\n"

"Researchers are still working to understand what harms honeybees. The USDA reports that no single cause "
"of Colony Collapse Disorder has been proven. Instead, several stresses seem to combine. These include "
"disease, poor nutrition, and the loss of the wild flowers that bees feed on. Scientists study each of "
"these stresses in turn. Knowing these facts does not by itself save a single hive. But it does make one "
"point clear. The honeybee is not just an insect at a picnic. It is a quiet partner in growing the food "
"that reaches our tables."
)

REC = StimulusRecord(
    id="ACC-W910-INFO-SINGLE-0009",
    grade="9", mode="explanatory", family="single", bucket="test", form="mcas",
    topic_id="honeybees",
    annotated=False,
    modeling_anchor="STAAR English I / MCAS informational",
    acc_tags=["ACC.W.INFO.1", "ACC.W.INFO.2", "ACC.W.SRC.3", "CCSS.W.9-10.2"],
    prompt=("Write a well-organized informational composition that uses specific evidence from the article "
            "\"The Work of the Honeybee\" to explain how a honeybee hive works, how bees pollinate crops, "
            "and why the health of honeybees matters to the food supply."),
    passages=[Passage(title="The Work of the Honeybee", text=PASSAGE)],
    fact_sources=[
        FactSource("Worker bees do the majority of the labor in a honeybee colony", "", "US EPA",
                   "https://www.epa.gov/pollinator-protection/colony-collapse-disorder",
                   "Colony Collapse Disorder is the phenomenon that occurs when the majority of worker bees in a colony disappear"),
        FactSource("Pollen sticks to bees as they drink nectar or land on a flower", "", "US NPS",
                   "https://www.nps.gov/subjects/pollinators/what-is-a-pollinator.htm",
                   "As they drink nectar or land on flowers, pollen sticks to their bodies and gets carried to the next flower they visit."),
        FactSource("Pollen movement fertilizes the plant and helps it make seeds, fruits, and new plants",
                   "", "US NPS",
                   "https://www.nps.gov/subjects/pollinators/what-is-a-pollinator.htm",
                   "This movement fertilizes a plant, helping make seeds, fruits, and new plants."),
        FactSource("Managed honeybee colonies add at least $18 billion to US agriculture annually",
                   "18 billion", "US Department of Agriculture",
                   "https://www.ars.usda.gov/oc/br/ccd/index/",
                   "Pollination by managed honey bee colonies adds at least $18 billion to the value of U.S. agriculture annually"),
        FactSource("About one mouthful in three of the diet benefits from honeybee pollination", "1 in 3",
                   "US Department of Agriculture",
                   "https://www.ars.usda.gov/oc/br/ccd/index/",
                   "About one mouthful in three in our diet directly or indirectly benefits from honey bee pollination."),
        FactSource("Almonds are almost completely dependent on honeybees for pollination", "",
                   "US Department of Agriculture",
                   "https://www.ars.usda.gov/oc/br/ccd/index/",
                   "Almonds, for example, are almost completely dependent on honey bees for pollination."),
        FactSource("US managed colonies fell from 5 million in the 1940s to about 2.66 million",
                   "5 million / 2.66 million", "US Department of Agriculture",
                   "https://www.ars.usda.gov/oc/br/ccd/index/",
                   "decreased from 5 million in the 1940s to about 2.66 million today"),
        FactSource("In October 2006 some beekeepers began losing 30 to 90 percent of their hives",
                   "30 to 90 percent", "US Department of Agriculture",
                   "https://www.ars.usda.gov/oc/br/ccd/index/",
                   "In October 2006, some beekeepers began reporting losses of 30-90 percent of their hives."),
        FactSource("No single cause of Colony Collapse Disorder has been proven", "",
                   "US Department of Agriculture",
                   "https://www.ars.usda.gov/oc/br/ccd/index/",
                   "No scientific cause for CCD has been proven ... no one factor is the cause of CCD."),
    ],
    provenance={"copyright": "own_authored", "rights": "public-domain-sourced (US federal)",
                "authored": "2026-07-08"},
)

if __name__ == "__main__":
    qc = qc_stimulus(REC)
    import re
    wc = len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", PASSAGE))
    print(f"passage word count: {wc}")
    print(qc_report(REC))
    import sys
    sys.exit(0 if qc["passed"] else 1)
