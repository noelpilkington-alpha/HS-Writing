"""
Single-source EXPLANATORY LESSON stimulus for the G9 (English I) writing bank: bird migration, the
paths birds follow (flyways), and how scientists track them. Explain, do not argue.

bucket="lesson", family="single", mode="explanatory", grade="9" (gates Lexile at the English I band
1010-1150L). Every figure traces to a fetched federal page (NPS / USGS). Runs itself through the QC
harness and reports. No em dashes in prose.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# Explanatory passage, G9 register (short sentences, fewer polysyllabic words). Every figure from a
# fetched federal page.
PASSAGE = (
"Twice a year, the sky fills with travelers. Millions of birds leave one home and fly toward another. "
"Some cross whole continents. Some cross entire oceans. This yearly journey is called migration. This "
"passage explains why birds migrate, how far some of them travel, what routes they follow, and how "
"scientists track their long trips.\n\n"

"Birds migrate mainly to find food and to raise their young. When winter arrives, cold weather can hide "
"or kill the insects, seeds, and plants that birds eat. So many birds fly toward warmer regions where "
"food is easier to find. When the season turns again, they return north to breed. The National Park "
"Service points to the far north as a rich summer nursery. At Cape Krusenstern in Alaska, the endless "
"summer sunlight and still tundra lakes make food incredibly abundant. About 150 species of birds use "
"that one area each year to breed.\n\n"

"The distances some birds cover are almost hard to believe. The National Park Service reports that the "
"Arctic tern makes the longest migration of any animal on Earth. This small seabird flies about 12,000 "
"miles in each direction. That adds up to a round trip of roughly 24,000 miles every year. Over ten "
"years, the Park Service notes, an Arctic tern travels about the same distance as a trip to the moon. "
"For a bird that weighs only a few ounces, that is a stunning feat of endurance.\n\n"

"Birds do not wander at random when they migrate. Instead, they tend to follow set routes. A migration "
"route that stretches between breeding grounds and winter grounds is called a flyway. The National Park "
"Service explains that two major flyways come together in northwest Alaska. These paths draw birds from "
"the Pacific and from across the Americas. The region even sits at the edge of a third flyway, which "
"sometimes carries in birds from Asia and Europe.\n\n"

"How do scientists learn where a single bird goes? One of the oldest methods is bird banding. A "
"scientist gently places a small numbered band around a bird's leg and then lets the bird go. If that "
"same bird is later found in another place, the number on its band reveals where it has traveled. Piece "
"by piece, these records map the routes that whole species use. The U.S. Geological Survey runs the "
"national Bird Banding Laboratory, which was established in 1920. The lab receives over 60,000 band "
"reports from hunters each year. Each report adds another clue about the hidden paths that birds "
"follow.\n\n"

"Migration ties distant places together. A bird that nests in Alaska may spend the winter thousands of "
"miles to the south. To survive the trip, it needs safe places to rest and enough food along the entire "
"route. A single broken link in that chain can put the whole journey at risk. That is why scientists "
"study migration so closely. Understanding where birds go, and when, is the first step toward protecting "
"the long journeys they have made for thousands of years."
)

rec = StimulusRecord(
    id="ACC-W910-INFO-LESSON-MIGRATION",
    grade="9", mode="explanatory", family="single", bucket="lesson",
    topic_id="animal_migration",
    annotated=False,
    modeling_anchor="STAAR English I informational ECR",
    acc_tags=["ACC.W.INFO.1", "ACC.W.INFO.2", "ACC.W.SRC.3", "CCSS.W.9-10.2"],
    prompt=("Write a well-organized informational composition that uses specific evidence from the article "
            "\"The Great Journeys of Birds\" to explain why birds migrate, how far some travel, the routes "
            "they follow, and how scientists track their journeys."),
    passages=[Passage(title="The Great Journeys of Birds", text=PASSAGE)],
    fact_sources=[
        FactSource("Bird species that use Cape Krusenstern each year to breed", "150", "National Park Service",
                   "https://www.nps.gov/cakr/learn/nature/birds.htm",
                   "150 species of birds ... the endless sunlight and still lakes on the tundra make food incredibly abundant"),
        FactSource("Arctic tern one-way migration distance", "12,000 miles", "National Park Service",
                   "https://www.nps.gov/cakr/learn/nature/birds.htm",
                   "flies between Antarctic and the Arctic - 12,000 miles each way"),
        FactSource("Arctic tern yearly round-trip migration (longest of any species)", "24,000 miles",
                   "National Park Service",
                   "https://www.nps.gov/cakr/learn/nature/birds.htm",
                   "24,000 mile yearly migration ... the longest of any species on earth"),
        FactSource("Major flyways that converge in northwest Alaska", "two", "National Park Service",
                   "https://www.nps.gov/cakr/learn/nature/birds.htm",
                   "Two major flyways ... drawing birds from the Pacific and the Americas ... a third flyway"),
        FactSource("Year the USGS Bird Banding Laboratory was established", "1920", "US Geological Survey",
                   "https://www.usgs.gov/labs/bird-banding-laboratory",
                   "The lab was established in 1920"),
        FactSource("Band encounter reports the program receives from hunters each year", "60,000",
                   "US Geological Survey",
                   "https://www.usgs.gov/labs/bird-banding-laboratory",
                   "receives over 60,000 band encounter reports from hunters each year"),
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
