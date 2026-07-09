"""
Single-source EXPLANATORY LESSON stimulus for the G9 (English I) writing bank: the water cycle and
watersheds (how water moves, where it is stored, how land drains to a common outlet). Explain, do not argue.

bucket="lesson", family="single", mode="explanatory", grade="9" (gates Lexile at the English I band
1010-1150L). Every figure traces to a fetched federal page (USGS / NOAA / US EPA). Runs itself through
the QC harness and reports. No em dashes in prose.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# Explanatory passage, G9 register (short sentences, fewer polysyllabic words). Every figure from a
# fetched federal page.
PASSAGE = (
"The water in a glass may look brand new, but it is not. The same water has been circling the planet for "
"billions of years. It rises into the sky, falls as precipitation, flows to the sea, and then rises once "
"more. Scientists call this endless loop the water cycle. This passage explains how the cycle works, "
"where the planet stores its water, and how the shape of the land guides that water back toward the "
"sea.\n\n"

"Two natural forces keep the entire cycle moving. The U.S. Geological Survey explains that energy from "
"the sun and the force of gravity drive the continual movement of water. The sun heats the water in "
"oceans, lakes, and soil. Some of that liquid then turns into an invisible gas called water vapor, in a "
"process known as evaporation. Living plants add vapor as well. They release it through their leaves in "
"a process called transpiration. The rising vapor then drifts upward into the cooler air.\n\n"

"High above the surface, the water transforms yet again. As the vapor cools, it condenses back into "
"countless tiny droplets of liquid. This process is called condensation, and it gathers into the clouds "
"we see overhead. When enough moisture collects inside a cloud, gravity pulls the water back toward the "
"ground as precipitation. That water may fall as rain, snow, sleet, or hail. In this steady exchange, "
"the water that once left the surface always returns to it.\n\n"

"Most of the planet's water, however, is not fresh and drinkable. The U.S. Geological Survey reports "
"that the oceans hold about 96.5 percent of all the water on Earth. That enormous supply is far too "
"salty to drink. Of the small share that is fresh, more than 68 percent is frozen and locked away inside "
"ice and glaciers. Roughly 30 percent more is hidden underground. Only a very thin slice remains in the "
"rivers and lakes that people depend on most. In fact, rivers hold only about one ten-thousandth of one "
"percent of the world's water.\n\n"

"Once precipitation reaches the ground, the surrounding landscape decides where it will travel. An area "
"of land that drains toward a single common outlet is called a watershed. The USGS describes a watershed "
"as an area that drains all its streams and rainfall to one shared point, such as the mouth of a bay or "
"a spot along a river. High ridges act like natural walls. They send falling rain down one side or the "
"other. Small watersheds gradually join together to form far larger ones. In the end, nearly all of this "
"water flows downhill to the sea, where the cycle can begin again.\n\n"

"Understanding the water cycle helps explain much of the natural world around us. It shows why heavy "
"rain often follows a long dry spell. It shows why rivers keep flowing steadily even when no rain has "
"fallen for many days. It also reminds us that the water we drink is borrowed, not manufactured. The "
"same drops that fall on a distant mountain today may fill a faraway ocean next year, then rise once "
"more into a passing cloud."
)

rec = StimulusRecord(
    id="ACC-W910-INFO-LESSON-WATER-CYCLE",
    grade="9", mode="explanatory", family="single", bucket="lesson",
    topic_id="water_cycle",
    annotated=False,
    modeling_anchor="STAAR English I informational ECR",
    acc_tags=["ACC.W.INFO.1", "ACC.W.INFO.2", "ACC.W.SRC.3", "CCSS.W.9-10.2"],
    prompt=("Write a well-organized informational composition that uses specific evidence from the article "
            "\"The Endless Journey of Water\" to explain how the water cycle works, where Earth's water is "
            "stored, and how a watershed guides water back to the sea."),
    passages=[Passage(title="The Endless Journey of Water", text=PASSAGE)],
    fact_sources=[
        FactSource("The sun's energy and gravity drive the water cycle", "", "US Geological Survey",
                   "https://www.usgs.gov/special-topics/water-science-school/science/water-cycle",
                   "Energy from the sun and the force of gravity drive the continual movement of water between pools"),
        FactSource("Share of Earth's water held by the oceans", "96.5 percent", "US Geological Survey",
                   "https://www.usgs.gov/special-topics/water-science-school/science/how-much-water-there-earth",
                   "about 96.5 percent of all Earth's water"),
        FactSource("Share of fresh water locked in ice and glaciers", "68 percent", "US Geological Survey",
                   "https://www.usgs.gov/special-topics/water-science-school/science/how-much-water-there-earth",
                   "over 68 percent is locked up in ice and glaciers"),
        FactSource("Share of fresh water stored underground", "30 percent", "US Geological Survey",
                   "https://www.usgs.gov/special-topics/water-science-school/science/how-much-water-there-earth",
                   "Another 30 percent of freshwater is in the ground"),
        FactSource("Share of the world's water held in rivers", "one ten-thousandth of one percent",
                   "US Geological Survey",
                   "https://www.usgs.gov/special-topics/water-science-school/science/how-much-water-there-earth",
                   "about 1/10,000th of one percent of total water"),
        FactSource("Definition of a watershed (drains to a common outlet)", "", "US Geological Survey",
                   "https://www.usgs.gov/special-topics/water-science-school/science/watersheds-and-drainage-basins",
                   "an area of land that drains all the streams and rainfall to a common outlet"),
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
