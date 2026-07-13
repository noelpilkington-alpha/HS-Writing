"""
Single-source EXPLANATORY LESSON stimulus for the G9 (English I) writing bank: how plants convert
sunlight into food and energy (photosynthesis), and why the reaction matters. Explain, do not argue.

bucket="lesson", family="single", mode="explanatory", grade="9" (gates Lexile at the English I band
1010-1150L). Every figure traces to a fetched federal page (NASA / NOAA / US DOE). Runs itself through
the QC harness and reports. No em dashes in prose.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# Explanatory passage, G9 register (short sentences, fewer polysyllabic words). Every figure from a
# fetched federal page.
PASSAGE = (
"Every green plant runs a kind of quiet factory. It takes in light and gives back the air we breathe. "
"This process has a name. It is called photosynthesis. It is one of the most important reactions on "
"Earth. This passage explains how a plant turns sunlight into food, and why that work matters for every "
"living thing.\n\n"

"Photosynthesis needs three simple ingredients. A plant must have sunlight, water, and a gas called "
"carbon dioxide. The U.S. Department of Energy explains that the reaction uses only water, carbon "
"dioxide, and sunlight to make fuel. The plant pulls water up through its roots. It takes in carbon "
"dioxide through tiny holes in its leaves. Sunlight then provides the energy that drives the whole "
"reaction forward. None of these ingredients is rare. Water falls as rain, carbon dioxide floats in the "
"air, and sunlight arrives every day. That is part of why plants can grow almost everywhere on land.\n\n"

"The real work happens inside the leaves. Leaves are full of a green coloring called chlorophyll. "
"Chlorophyll is what makes most plants look green. It also acts like a tiny solar panel. It captures "
"the energy in sunlight and puts that energy to work. Using this power, the plant rearranges water and "
"carbon dioxide into sugar. The sugar is the plant's food. Some of it fuels new growth right away. Some "
"of it is stored for later. Over time it builds the roots, the stems, and the leaves that we see.\n\n"

"The reaction also makes something we cannot live without. As a plant builds sugar, it releases oxygen "
"into the air. That oxygen is the gas that people and animals breathe. Plants on land are not the only "
"source, though. Tiny drifting ocean plants, called phytoplankton, photosynthesize as well. NOAA reports "
"that about half of the oxygen on Earth comes from the ocean. One kind of ocean bacteria, called "
"Prochlorococcus, produces up to 20 percent of the oxygen in the whole living world.\n\n"

"Photosynthesis does one more vital job. It helps balance the gases in the air. As plants grow, they "
"pull carbon dioxide out of the atmosphere. NOAA reports that the oceans and land plants trade more than "
"200 billion metric tons of carbon with the air each year. The U.S. Department of Energy adds that "
"forests, grasslands, and farms have soaked up about 25 percent of the carbon that human activity "
"releases. NASA scientists track that gas closely. The air now holds about 430 parts of carbon dioxide "
"for every million parts of air.\n\n"

"The chain does not stop with a single plant. Animals cannot make their own food from light. Instead, "
"they eat plants for the sugar stored inside them. Other animals then eat those plant eaters. In this "
"way, almost every food chain traces back to photosynthesis. The energy in a meal usually began as "
"sunlight caught by a leaf. The same reaction fills the sky with oxygen and pulls carbon dioxide back "
"down. A single leaf may look still and plain. Inside, it is running one of the busiest reactions on "
"the planet."
)

rec = StimulusRecord(
    id="ACC-W910-INFO-LESSON-PHOTOSYNTHESIS",
    grade="9", mode="explanatory", family="single", bucket="lesson",
    topic_id="photosynthesis",
    annotated=False,
    modeling_anchor="STAAR English I informational ECR",
    acc_tags=["ACC.W.INFO.1", "ACC.W.INFO.2", "ACC.W.SRC.3", "CCSS.W.9-10.2"],
    prompt=("Write a well-organized informational composition that uses specific evidence from the article "
            "\"How a Leaf Makes Food from Light\" to explain how photosynthesis works, what it produces, and "
            "why the reaction matters for living things."),
    passages=[Passage(title="How a Leaf Makes Food from Light", text=PASSAGE)],
    fact_sources=[
        FactSource("Photosynthesis uses only water, carbon dioxide, and sunlight", "", "US DOE",
                   "https://www.energy.gov/science/doe-explainssolar-fuels",
                   "natural photosynthesis in plants by using only water, carbon dioxide, and sunlight to generate fuel"),
        FactSource("Share of Earth's oxygen that comes from the ocean", "about half / 50 percent", "NOAA",
                   "https://oceanservice.noaa.gov/facts/ocean-oxygen.html",
                   "about half of Earth's oxygen comes from the ocean"),
        FactSource("Oxygen produced by the ocean bacteria Prochlorococcus", "20 percent", "NOAA",
                   "https://oceanservice.noaa.gov/facts/ocean-oxygen.html",
                   "Prochlorococcus ... produces up to 20% of the oxygen in our entire biosphere"),
        FactSource("Carbon traded between oceans/land plants and the air each year", "200 billion metric tons",
                   "NOAA",
                   "https://www.gml.noaa.gov/outreach/faq.html",
                   "The oceans and land vegetation release and absorb over 200 billion metric tons of carbon into and out of the atmosphere each year"),
        FactSource("Share of human carbon emissions absorbed by forests, grasslands, and farms", "25 percent",
                   "US DOE",
                   "https://www.energy.gov/science/doe-explainsthe-carbon-cycle",
                   "about 25 percent of human-source carbon emissions have been captured by forests, grassland, and farms"),
        FactSource("Current atmospheric carbon dioxide level", "430 parts per million", "NASA",
                   "https://science.nasa.gov/kids/earth/",
                   "430 parts of Carbon Dioxide for every million parts of air"),
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
