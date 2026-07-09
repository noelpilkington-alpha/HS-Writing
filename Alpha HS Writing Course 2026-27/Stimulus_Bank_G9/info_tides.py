"""
Single-source EXPLANATORY TEST stimulus for the G9 (English I) writing test bank: how ocean tides work,
how often they occur, and why their timing shifts a little each day. Explain, do not argue.

bucket="test", form="mcas", family="single", mode="explanatory", grade="9" (gates Lexile at the English I
band 1010-1150L). Every figure traces to a fetched federal page (NOAA National Ocean Service), fetched
live 2026-07-08. Not annotated (test bucket). Runs itself through the QC harness and reports.
No em dashes in prose.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# Explanatory passage, G9 register (short sentences, fewer polysyllabic words). Every figure from a
# fetched federal page (NOAA National Ocean Service).
PASSAGE = (
"Anyone who has spent a day at the beach has watched the tide change. In the morning the water may reach "
"far up the sand. By afternoon it has pulled back and left a wide, wet shore behind it. This slow rise "
"and fall of the sea is called the tide, and it follows a steady schedule, day after day. This passage "
"explains what generates the tides, how often they occur, and why their timing shifts a little later "
"each day.\n\n"

"Tides begin far out in the open ocean. The National Oceanic and Atmospheric Administration explains "
"that tides are very long waves. These waves move through the ocean in response to the gravitational "
"pull of the moon and the sun. The moon has the stronger effect because it orbits much closer to Earth. "
"Its gravity tugs on the ocean and lifts a bulge of water toward it. A second bulge forms at the same "
"time on the opposite side of the planet. As the Earth rotates, its coastlines pass through these two "
"bulges. When a coast rotates into a bulge, the water climbs and the tide comes in.\n\n"

"Scientists use precise names for each part of this cycle. NOAA notes that high tide is the crest, or "
"highest point, of the passing wave. Low tide is the trough, or lowest point. The difference in height "
"between them is called the tidal range. The moving water carries names too. The incoming tide is called "
"a flood current. The outgoing tide is called an ebb current. The brief calm between them is known as "
"slack water.\n\n"

"How often do these tides occur? NOAA reports that most coastal areas have two high tides and two low "
"tides each day. When the two high tides reach about the same height, the pattern is called a "
"semidiurnal tide. When they differ noticeably in height, it is called a mixed semidiurnal tide. A few "
"locations have only one high tide and one low tide each day, a pattern known as a diurnal tide. The "
"pattern depends on the coastline. NOAA notes that the East Coast of the United States tends to have "
"semidiurnal tides. The West Coast tends to have mixed semidiurnal tides.\n\n"

"The most puzzling feature of the tides is their timing. High tides do not arrive at the same clock time "
"each day. Instead, they slide steadily later, and the reason is once again the moon. NOAA explains that "
"a lunar day lasts 24 hours and 50 minutes rather than the familiar 24 hours. The moon revolves around "
"the Earth in the same direction that the Earth rotates on its axis. So the planet needs an extra 50 "
"minutes to catch up to the moon each day. Because the tides follow the moon, they arrive about 50 "
"minutes later than they did the day before. Successive high tides come about 12 hours and 25 minutes "
"apart.\n\n"

"Knowing the schedule of the tides matters to a great many people. Sailors, commercial fishers, and "
"surfers all plan their days around it. The federal government publishes detailed tide tables so that "
"ships can enter and leave crowded harbors safely. Understanding the tides does not change the steady "
"pull of the moon overhead. It does, however, explain a dependable rhythm that has shaped coastlines and "
"coastal life for as long as people have lived beside the sea."
)

REC = StimulusRecord(
    id="ACC-W910-INFO-SINGLE-0006",
    grade="9", mode="explanatory", family="single", bucket="test", form="mcas",
    topic_id="ocean_tides",
    annotated=False,
    modeling_anchor="STAAR English I / MCAS informational",
    acc_tags=["ACC.W.INFO.1", "ACC.W.INFO.2", "ACC.W.SRC.3", "CCSS.W.9-10.2"],
    prompt=("Write a well-organized informational composition that uses specific evidence from the article "
            "\"The Rhythm of the Tides\" to explain what causes ocean tides, how often they occur, and why "
            "their timing shifts a little each day."),
    passages=[Passage(title="The Rhythm of the Tides", text=PASSAGE)],
    fact_sources=[
        FactSource("Tides are very long waves that respond to the moon and sun", "", "NOAA",
                   "https://oceanservice.noaa.gov/education/tutorial_tides/tides01_intro.html",
                   "tides are very long-period waves that move through the oceans in response to the forces exerted by the moon and sun"),
        FactSource("The moon and sun cause tides through their gravitational pull", "", "NOAA",
                   "https://oceanservice.noaa.gov/facts/moon-tide.html",
                   "While the moon and sun cause tides on our planet, the gravitational pull of these celestial bodies"),
        FactSource("High tide is the wave crest, low tide is the trough, difference is the tidal range", "",
                   "NOAA",
                   "https://oceanservice.noaa.gov/education/tutorial_tides/tides01_intro.html",
                   "high tide ... the crest of the wave ... low tide corresponds to the lowest part of the wave, or its trough ... the tidal range"),
        FactSource("Incoming tide is a flood current, outgoing is an ebb current, calm is slack water", "",
                   "NOAA",
                   "https://oceanservice.noaa.gov/education/tutorial_tides/tides01_intro.html",
                   "The incoming tide ... is called a flood current; the outgoing tide is called an ebb current ... slack water"),
        FactSource("Most areas have two high tides and two low tides each day", "2 high / 2 low", "NOAA",
                   "https://oceanservice.noaa.gov/education/tutorial_tides/tides07_cycles.html",
                   "most areas have two high tides and two low tides each day"),
        FactSource("Semidiurnal, mixed semidiurnal, and diurnal tide patterns by coast", "", "NOAA",
                   "https://oceanservice.noaa.gov/education/tutorial_tides/tides07_cycles.html",
                   "semidiurnal tide ... mixed semidiurnal tide ... diurnal tide ... West Coast tends to have mixed semidiurnal tides, whereas a semidiurnal pattern is more typical of the East Coast"),
        FactSource("A lunar day lasts 24 hours and 50 minutes, so tides arrive about 50 minutes later",
                   "24 hours 50 minutes", "NOAA",
                   "https://oceanservice.noaa.gov/education/tutorial_tides/tides05_lunarday.html",
                   "a lunar day is 24 hours and 50 minutes ... it takes the Earth an extra 50 minutes to catch up to the moon"),
        FactSource("High tides occur about 12 hours and 25 minutes apart", "12 hours 25 minutes", "NOAA",
                   "https://oceanservice.noaa.gov/education/tutorial_tides/tides05_lunarday.html",
                   "High tides occur 12 hours and 25 minutes apart"),
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
