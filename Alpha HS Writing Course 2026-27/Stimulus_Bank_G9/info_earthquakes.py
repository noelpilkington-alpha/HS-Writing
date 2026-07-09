"""
Single-source EXPLANATORY TEST stimulus for the G9 (English I) writing test bank: how earthquakes happen
and how scientists measure them. Explain, do not argue.

bucket="test", form="mcas", family="single", mode="explanatory", grade="9" (gates Lexile at the English I
band 1010-1150L). Every figure traces to a fetched federal page (US Geological Survey), fetched live
2026-07-08. Not annotated (test bucket). Runs itself through the QC harness and reports.
No em dashes in prose.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# Explanatory passage, G9 register (short sentences, fewer polysyllabic words). Every figure from a
# fetched federal page (US Geological Survey).
PASSAGE = (
"The ground beneath our feet feels perfectly solid and still. Most of the time, that is true. But every "
"so often the earth lurches, buildings sway, and the surface itself seems to roll like water. That "
"sudden shaking is an earthquake. This passage explains what actually causes an earthquake and how "
"scientists measure the size of one after it strikes.\n\n"

"To understand earthquakes, start with the outer shell of the planet. The U.S. Geological Survey "
"explains that the surface of the Earth is broken into large pieces called tectonic plates. These plates "
"are huge. They carry the continents and the ocean floor on their backs. The plates drift very slowly "
"over time. They do not slide smoothly past one another, though. Instead, the plates get stuck at their "
"edges because of friction. Stress then builds along the stuck edge, sometimes for hundreds of "
"years.\n\n"

"An earthquake is what happens when that stress finally wins. The USGS explains that an earthquake is "
"caused by a sudden slip on a fault. A fault is a crack where two blocks of rock meet. When the stress "
"on the edge overcomes the friction, the rock slips all at once. That slip releases energy in waves. "
"These waves travel outward through the crust of the Earth. They are the reason the ground shakes. The "
"shaking can last only a few seconds, yet it can topple walls and crack roads in that short time.\n\n"

"California offers a famous example of this process. The USGS reports that two plates meet there, the "
"Pacific Plate and the North American Plate. The boundary between them is the San Andreas Fault. That "
"fault is more than 650 miles long and reaches at least 10 miles deep. The Pacific Plate grinds past the "
"North American Plate at a rate of about two inches per year. Where the plates lock in place, strain can "
"build for centuries before it breaks loose in a great earthquake.\n\n"

"After an earthquake, scientists want to measure how large it was. The USGS explains that they use a "
"number called the magnitude. For most earthquakes, the best measure is the moment magnitude scale. It "
"has largely replaced the older Richter scale, which Charles Richter introduced in 1935. The magnitude "
"comes from records made by instruments called seismographs. Each step up the scale means a big jump in "
"power. The USGS notes that each whole number is a tenfold increase in the wave height on the record. It "
"also represents about 32 times more energy released by the quake.\n\n"

"Magnitude is not the only measure that matters. The USGS explains that scientists also track intensity, "
"which is the strength of shaking felt at a given place. Two towns can feel the same quake very "
"differently. A town near the fault may feel violent shaking. A town far away may feel only a gentle "
"sway. That is why intensity depends heavily on the distance from the fault. It is recorded on the "
"Modified Mercalli scale using Roman numerals. All of this monitoring is constant. The National "
"Earthquake Information Center locates and publishes about 30,000 earthquakes every year. By measuring "
"each one, scientists help engineers design safer buildings and help communities prepare for the shaking "
"that will surely come again."
)

REC = StimulusRecord(
    id="ACC-W910-INFO-SINGLE-0007",
    grade="9", mode="explanatory", family="single", bucket="test", form="mcas",
    topic_id="earthquakes",
    annotated=False,
    modeling_anchor="STAAR English I / MCAS informational",
    acc_tags=["ACC.W.INFO.1", "ACC.W.INFO.2", "ACC.W.SRC.3", "CCSS.W.9-10.2"],
    prompt=("Write a well-organized informational composition that uses specific evidence from the article "
            "\"When the Ground Slips\" to explain what causes earthquakes and how scientists measure their "
            "size after they strike."),
    passages=[Passage(title="When the Ground Slips", text=PASSAGE)],
    fact_sources=[
        FactSource("Earth's surface is broken into tectonic plates that get stuck at their edges", "",
                   "US Geological Survey",
                   "https://www.usgs.gov/faqs/what-earthquake-and-what-causes-them-happen",
                   "The tectonic plates ... get stuck at their edges due to friction."),
        FactSource("An earthquake is caused by a sudden slip on a fault, releasing energy in waves", "",
                   "US Geological Survey",
                   "https://www.usgs.gov/faqs/what-earthquake-and-what-causes-them-happen",
                   "An earthquake is caused by a sudden slip on a fault ... releases energy in waves that travel through the earth's crust and cause the shaking that we feel"),
        FactSource("Stress builds until it overcomes friction, then the rock slips", "",
                   "US Geological Survey",
                   "https://www.usgs.gov/faqs/what-earthquake-and-what-causes-them-happen",
                   "When the stress on the edge overcomes the friction, there is an earthquake"),
        FactSource("San Andreas Fault length and depth", "650 miles / 10 miles", "US Geological Survey",
                   "https://www.usgs.gov/faqs/what-earthquake-and-what-causes-them-happen",
                   "more than 650 miles long and extends to depths of at least 10 miles"),
        FactSource("Pacific Plate moves past the North American Plate about two inches per year",
                   "2 inches per year", "US Geological Survey",
                   "https://www.usgs.gov/faqs/what-earthquake-and-what-causes-them-happen",
                   "the Pacific Plate is moving to the northwest ... at a rate of about two inches per year"),
        FactSource("Richter scale introduced by Charles Richter in 1935; moment magnitude now preferred",
                   "1935", "US Geological Survey",
                   "https://www.usgs.gov/programs/earthquake-hazards/earthquake-magnitude-energy-release-and-shaking-intensity",
                   "The Richter Scale (ML) ... was the first magnitude scale ... introduced in 1935 ... moment magnitude (MW) is a more accurate measure of the earthquake size"),
        FactSource("Each whole magnitude step is a tenfold rise in amplitude and about 32 times the energy",
                   "10 / 32 times", "US Geological Survey",
                   "https://www.usgs.gov/programs/earthquake-hazards/earthquake-magnitude-energy-release-and-shaking-intensity",
                   "a tenfold increase in measured amplitude ... 32 times more energy release"),
        FactSource("Intensity is measured on the Modified Mercalli scale and depends on distance", "",
                   "US Geological Survey",
                   "https://www.usgs.gov/programs/earthquake-hazards/earthquake-magnitude-energy-release-and-shaking-intensity",
                   "Intensity is the measure of shaking at each location ... Modified Mercalli Intensity Scale ... expressed in Roman numerals"),
        FactSource("NEIC locates and publishes about 30,000 earthquakes each year", "30,000",
                   "US Geological Survey",
                   "https://www.usgs.gov/programs/earthquake-hazards/national-earthquake-information-center-neic",
                   "the NEIC staff locates and publishes approximately 30,000 earthquakes on a yearly basis"),
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
