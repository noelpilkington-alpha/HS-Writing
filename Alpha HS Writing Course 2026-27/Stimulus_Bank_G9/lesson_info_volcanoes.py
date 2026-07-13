"""
Single-source EXPLANATORY LESSON stimulus for the G9 (English I) writing bank: how volcanoes form and
how scientists monitor them for warning signs. Explain, do not argue.

bucket="lesson", family="single", mode="explanatory", grade="9" (gates Lexile at the English I band
1010-1150L). Every figure traces to a fetched federal page (US Geological Survey). Runs itself through
the QC harness and reports. No em dashes in prose.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# Explanatory passage, G9 register (short sentences, fewer polysyllabic words). Every figure from a
# fetched federal page.
PASSAGE = (
"A volcano can seem like a mountain that suddenly turns violent. In truth, it is a window into the hot "
"interior of our planet. Deep below the surface, rock can grow so hot that it melts. When that molten "
"rock finds a path upward, a volcano is born. This passage explains how volcanoes form, how many exist, "
"and how scientists watch them for warning signs.\n\n"

"The story starts with melted rock. The U.S. Geological Survey explains that intense underground heat "
"melts some rock into a thick, flowing material called magma. This magma is lighter than the solid rock "
"around it. Because it is less dense, it slowly rises and collects in pools called magma chambers. These "
"chambers can sit for a long time before anything happens. Then, over time, some of the magma forces its "
"way up through cracks and vents toward the surface.\n\n"

"Scientists use two different names for this melted rock. The USGS notes that molten rock underground is "
"called magma, while molten rock that breaks through the surface is called lava. So the same material "
"has one name below the ground and another name above it. When magma finally reaches the open air, it "
"erupts as lava, ash, and gas. As the lava cools and hardens, it builds up in layers. Over many "
"eruptions, those layers can slowly grow into the tall cone shape that many volcanoes have.\n\n"

"Volcanoes are more common than most people think. The U.S. Geological Survey reports that there are "
"about 1,350 potentially active volcanoes around the world. Of those, about 500 have erupted in "
"recorded history. The United States alone has about 161 potentially active volcanoes. Most of them are "
"not spread out evenly. Instead, they sit along the west coast, in Alaska, and in Hawaii. These are "
"places where the edges of the planet's giant plates meet, and where magma can most easily reach the "
"surface.\n\n"

"Because eruptions can be dangerous, scientists watch volcanoes closely. The USGS explains that magma "
"rising toward the surface usually creates small earthquakes that instruments can detect. The moving "
"magma can also make the ground swell and can change the gases that leak from the volcano. To catch "
"these clues, scientists use seismometers to sense shaking. They use tilt meters and GPS to measure the "
"swelling of the ground. They also use sensors to track gases like sulfur dioxide and carbon dioxide.\n\n"

"These warning signs help, but they are not a perfect clock. The USGS cautions that unrest can last for "
"weeks, months, or even years without an eruption. It can also fade away with no eruption at all. That "
"uncertainty is why scientists watch the most dangerous volcanoes without pause. In a 2018 study, the "
"agency ranked 57 U.S. volcanoes as a high or very high threat to public safety. Those volcanoes get the "
"closest attention of all. By studying how volcanoes form and behave, scientists give nearby towns the "
"best possible chance to prepare before the ground begins to shake."
)

rec = StimulusRecord(
    id="ACC-W910-INFO-LESSON-VOLCANOES",
    grade="9", mode="explanatory", family="single", bucket="lesson",
    topic_id="volcanoes",
    annotated=False,
    modeling_anchor="STAAR English I informational ECR",
    acc_tags=["ACC.W.INFO.1", "ACC.W.INFO.2", "ACC.W.SRC.3", "CCSS.W.9-10.2"],
    prompt=("Write a well-organized informational composition that uses specific evidence from the article "
            "\"Windows into a Fiery Planet\" to explain how volcanoes form, how common they are, and how "
            "scientists monitor them for warning signs."),
    passages=[Passage(title="Windows into a Fiery Planet", text=PASSAGE)],
    fact_sources=[
        FactSource("Intense heat melts rock into magma that rises and collects", "", "US Geological Survey",
                   "https://www.usgs.gov/faqs/what-difference-between-magma-and-lava",
                   "a thick flowing substance called magma ... rises and collects in magma chambers"),
        FactSource("Magma is underground, lava is molten rock at the surface", "", "US Geological Survey",
                   "https://www.usgs.gov/faqs/what-difference-between-magma-and-lava",
                   "Scientists use the term magma for molten rock that is underground and lava for molten rock that breaks through the Earth's surface"),
        FactSource("Potentially active volcanoes worldwide", "1,350", "US Geological Survey",
                   "https://www.usgs.gov/faqs/how-many-active-volcanoes-are-there-earth",
                   "There are about 1,350 potentially active volcanoes worldwide"),
        FactSource("Volcanoes that have erupted in historical time", "500", "US Geological Survey",
                   "https://www.usgs.gov/faqs/how-many-active-volcanoes-are-there-earth",
                   "About 500 of those 1,350 volcanoes have erupted in historical time"),
        FactSource("Potentially active volcanoes in the United States", "161", "US Geological Survey",
                   "https://www.usgs.gov/faqs/how-can-we-tell-when-a-volcano-will-erupt",
                   "There are 161 potentially active volcanoes in the United States"),
        FactSource("U.S. volcanoes ranked high or very high threat (2018 assessment)", "57",
                   "US Geological Survey",
                   "https://www.usgs.gov/faqs/how-can-we-tell-when-a-volcano-will-erupt",
                   "57 volcanoes are a high threat or very high threat to public safety"),
        FactSource("Rising magma generates detectable earthquakes and deforms the ground", "",
                   "US Geological Survey",
                   "https://www.usgs.gov/faqs/how-can-we-tell-when-a-volcano-will-erupt",
                   "normally generates detectable earthquakes ... Subtle swelling of the ground surface"),
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
