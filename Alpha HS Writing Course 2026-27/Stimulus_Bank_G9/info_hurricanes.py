"""
Single-source EXPLANATORY TEST stimulus for the G9 (English I) writing test bank: how hurricanes form,
how they are classified, and how forecasters track them. Explain, do not argue.

bucket="test", form="mcas", family="single", mode="explanatory", grade="9" (gates Lexile at the English I
band 1010-1150L). Every figure traces to a fetched federal page (NOAA National Ocean Service, NOAA
National Hurricane Center, NOAA National Weather Service), fetched live 2026-07-08. Not annotated
(test bucket). Runs itself through the QC harness and reports. No em dashes in prose.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# Explanatory passage, G9 register (short sentences, fewer polysyllabic words). Every figure from a
# fetched federal page (NOAA).
PASSAGE = (
"A hurricane is one of the largest and most powerful storms on Earth. It can stretch for hundreds of "
"miles and last for many days. When one reaches land, it can flood cities and flatten homes. Yet every "
"hurricane begins in a quiet way, over warm ocean water. This passage explains how hurricanes form, how "
"forecasters rank their strength, and how they are tracked from space.\n\n"

"The story of a hurricane starts with heat. The National Oceanic and Atmospheric Administration explains "
"that these storms need warm ocean water to grow. The water must be at least 26.5 degrees Celsius. That "
"warmth also has to reach down to a depth of about 50 meters. Warm water feeds a hurricane in a simple "
"way. It heats the air just above the sea and makes that air rise. As the warm, moist air climbs, it "
"cools and forms clouds. Soon those clouds grow into towering thunderstorms. NOAA explains that these "
"thunderstorms turn ocean heat into the fuel that powers the storm.\n\n"

"Most hurricanes begin as a weak disturbance called a tropical wave. NOAA describes a tropical wave as a "
"low pressure area that drifts through the moist tropics. If the conditions are right, the storm spins "
"faster and grows stronger. Forecasters give it a new name at each stage. The National Weather Service "
"explains that a storm with winds up to 38 miles per hour is a tropical depression. When its winds reach "
"39 to 73 miles per hour, it becomes a tropical storm and earns a name. Once its winds hit 74 miles per "
"hour or more, it is officially a hurricane.\n\n"

"Not all hurricanes are equal, so forecasters rank them by strength. The National Hurricane Center uses "
"the Saffir-Simpson scale. NOAA explains that this scale gives a storm a rating from 1 to 5, based only "
"on its top wind speed. A Category 1 hurricane has winds of 74 to 95 miles per hour. A Category 5 "
"hurricane, the strongest of all, has winds of 157 miles per hour or higher. NOAA notes that Category 3, "
"4, and 5 storms are called major hurricanes because their winds can cause devastating damage.\n\n"

"Hurricanes do not strike at random times. NOAA reports that the Atlantic hurricane season runs from "
"June 1 to November 30 each year. There is a reason for those dates. The ocean needs the summer sun to "
"warm up first. In a typical season, forecasters expect about 14 named storms and 7 hurricanes to form. "
"Of those, about 3 grow into major hurricanes. The peak of the season falls around the middle of "
"September, when the ocean is warmest.\n\n"

"Once a storm forms, the work of tracking it begins. Forecasters at the National Hurricane Center watch "
"each storm using satellites high above the Earth. These satellites take pictures of the storm from "
"space. Forecasters also fly special planes straight into the storm. The planes measure its winds and "
"pressure from the inside. All of this data helps forecasters predict where the storm will go and how "
"strong it will be. That warning gives families time to prepare or to leave. Scientists cannot stop a "
"hurricane. But by understanding how these storms form and grow, they can help keep people out of harm's "
"way."
)

REC = StimulusRecord(
    id="ACC-W910-INFO-SINGLE-0008",
    grade="9", mode="explanatory", family="single", bucket="test", form="mcas",
    topic_id="hurricanes",
    annotated=False,
    modeling_anchor="STAAR English I / MCAS informational",
    acc_tags=["ACC.W.INFO.1", "ACC.W.INFO.2", "ACC.W.SRC.3", "CCSS.W.9-10.2"],
    prompt=("Write a well-organized informational composition that uses specific evidence from the article "
            "\"How a Hurricane Is Born\" to explain how hurricanes form, how forecasters rank their "
            "strength, and how they are tracked."),
    passages=[Passage(title="How a Hurricane Is Born", text=PASSAGE)],
    fact_sources=[
        FactSource("Hurricanes need warm water at least 26.5 C over about 50 meters depth",
                   "26.5 degrees Celsius / 50 meters", "NOAA",
                   "https://oceanservice.noaa.gov/facts/how-hurricanes-form.html",
                   "Water at least 26.5 degrees Celsius over a depth of 50 meters powers the storm."),
        FactSource("Thunderstorms turn ocean heat into hurricane fuel", "", "NOAA",
                   "https://oceanservice.noaa.gov/facts/how-hurricanes-form.html",
                   "Thunderstorms turn ocean heat into hurricane fuel."),
        FactSource("Hurricanes often begin as a tropical wave, a low pressure area in the tropics", "",
                   "NOAA",
                   "https://oceanservice.noaa.gov/facts/how-hurricanes-form.html",
                   "a tropical wave ... a low pressure area that moves through the moisture-rich tropics"),
        FactSource("Tropical depression has maximum sustained winds of 38 mph or less", "38 mph",
                   "NOAA National Weather Service",
                   "https://www.weather.gov/mob/tropical_definitions",
                   "A tropical cyclone that has maximum sustained surface winds ... of 38 mph (33 knots) or less."),
        FactSource("Tropical storm has winds of 39 to 73 mph", "39-73 mph",
                   "NOAA National Weather Service",
                   "https://www.weather.gov/mob/tropical_definitions",
                   "maximum sustained surface winds ranging from 39-73 mph (34 to 63 knots)."),
        FactSource("Hurricane has winds of 74 mph or greater", "74 mph",
                   "NOAA National Weather Service",
                   "https://www.weather.gov/mob/tropical_definitions",
                   "A hurricane is a tropical cyclone that has maximum sustained surface winds of 74 mph or greater"),
        FactSource("Saffir-Simpson scale rates 1 to 5 on maximum sustained wind speed", "1 to 5", "NOAA",
                   "https://www.nhc.noaa.gov/aboutsshws.php",
                   "a 1 to 5 rating based only on a hurricane's maximum sustained wind speed"),
        FactSource("Category 1 winds 74 to 95 mph; Category 5 winds 157 mph or higher",
                   "74-95 mph / 157 mph", "NOAA",
                   "https://www.nhc.noaa.gov/aboutsshws.php",
                   "Category 1: 74-95 mph ... Category 5: 157 mph or higher"),
        FactSource("Categories 3, 4, and 5 are called major hurricanes", "", "NOAA",
                   "https://www.nhc.noaa.gov/aboutsshws.php",
                   "Categories 3, 4 and 5 are considered major hurricanes"),
        FactSource("Atlantic hurricane season runs June 1 to November 30", "June 1 / November 30",
                   "NOAA National Hurricane Center",
                   "https://www.nhc.noaa.gov/climo/",
                   "The Atlantic hurricane season runs from June 1 to November 30."),
        FactSource("Average season: about 14 named storms, 7 hurricanes, 3 major hurricanes",
                   "14 / 7 / 3", "NOAA National Hurricane Center",
                   "https://www.nhc.noaa.gov/climo/",
                   "14 named storms, 7 hurricanes, and 3 major hurricanes"),
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
