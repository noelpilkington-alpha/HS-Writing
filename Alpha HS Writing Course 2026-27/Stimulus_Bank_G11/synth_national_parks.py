"""
G11 SYNTHESIS SOURCE SET for the writing test bank (family="synthesis_set"), authored 2026-07-18 to give
the G11 mid-gate (C1102-0016) a GENUINELY COLD topic. The prior mid-gate reused the AI-workforce set that
appears across the G11 unit; national parks appears NOWHERE in G11, so the gate finally tests cold transfer.

Debatable question: How should the country balance PUBLIC USE of the national parks against PRESERVING them
for future generations? Four sources on that one question (SBAC 4-source / AP Lang synthesis model): three
~500-540-word text sources plus one source that DESCRIBES a chart in words (visual/quantitative, exempt from
the 480-word floor). Register pinned to the G11 band.

EVERY numeric figure traces to a real fetched federal page (US NPS + US DOI), reused VERBATIM from the
already-verified fact table in Stimulus_Bank_G10/info_national_parks.py (facts fetched live 2026-07-07). No
NEW figures are introduced, so nothing here needs fresh fetch-verification. Family=synthesis_set,
mode=explanatory. No em dashes. Runs itself through the QC harness and reports.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# --- Source 1: US NPS -- what the system is and the tension written into its founding law ----------
SOURCE_NPS_MISSION = (
"How should the country balance letting the public enjoy the national parks against protecting those parks "
"for the future? The tension is not new. It was written into the law that created the system. According to "
"the National Park Service, the system today includes 433 units that cover more than 85 million acres, "
"reaching into all 50 states, the District of Columbia, and several territories. Only 63 of those units "
"carry the formal title of national park; the rest hold at least 19 other kinds of names, from monuments "
"and historic sites to seashores and scenic trails. The system is vast, and no single famous park stands "
"for the whole of it.\n\n"

"Congress created the National Park Service in 1916 and placed it inside the Department of the Interior. "
"The law gave the agency one job with two halves. The Service was to protect the scenery, the wildlife, and "
"the historic sites in the parks, and at the same time to let the public enjoy them. It had to do both in a "
"way that would leave the parks, in the words of the law, unimpaired for the enjoyment of future "
"generations. That single sentence holds the whole debate. The parks are meant to be used today. They are "
"also meant to be guarded so carefully that they outlast everyone now living.\n\n"

"For most of a century that double mission caused little open conflict. The parks were large, the crowds "
"were smaller, and use and protection could sit side by side. A staff of about 20,000 workers kept the "
"sites open, helped each year by volunteers and partner groups. Rangers guided visitors, maintained trails, "
"and watched over wildlife, treating access and preservation as two parts of the same task rather than as "
"rivals for the same limited time and money. When a trail wore thin, there were fewer feet to wear it, and "
"the budget could usually cover the fix before the damage spread. Enjoyment and protection, in those "
"quieter decades, rarely forced anyone to choose between them.\n\n"

"The reason the balance matters more now is that one half of the mission has grown much heavier than the "
"other. Use has surged while the means to protect the parks have not kept pace. When a law asks an agency "
"to do two things at once, the real question is what happens when those two things start to pull in "
"opposite directions. That is the situation the parks face today, and it is why a founding sentence written "
"in 1916 has become a live argument about how the parks should be run.\n\n"

"Reading the mission honestly means admitting that neither half can simply win. A park closed to people "
"would protect its scenery but betray the promise that the public may enjoy it. A park loved to the point "
"of damage would honor access while breaking the promise to future generations. The Service was handed both "
"promises at once, and the sources that follow show how hard they have become to keep together as the parks "
"have grown more popular than their founders could have imagined."
)

# --- Source 2: US DOI -- the economic case that use is the parks' greatest public value ------------
SOURCE_DOI_ECONOMY = (
"One powerful answer to the balance question is that public use is not a threat to the parks but the very "
"reason they are worth protecting. The strongest evidence for that view is economic, and it comes from the "
"federal government's own accounting. Each year the National Park Service studies how visitor money flows "
"into the towns around the parks, and the Department of the Interior reports the result. In 2023, park "
"visitors spent 26.4 billion dollars in nearby communities, paying for lodging, meals, fuel, and other "
"needs as they traveled.\n\n"

"That spending does not stay local. The Department of the Interior reported that visitor spending in 2023 "
"produced a record high 55.6 billion dollars in benefit to the national economy. The same activity "
"supported about 415,400 jobs across the country and created 19.4 billion dollars in labor income. These "
"are not abstract figures. In many rural areas, a nearby park is one of the largest engines of the local "
"economy, and the shops, hotels, and guides in gateway towns depend on the steady stream of travelers who "
"come to see it.\n\n"

"Seen this way, access is not the enemy of preservation but its ally. The parks earn broad public support, "
"and the federal dollars that maintain them, in large part because so many people visit and value them. A "
"park that no one is allowed to enjoy would lose the constituency that fights for its budget. The 55.6 "
"billion dollars in economic benefit is, in effect, a yearly vote of confidence cast by the millions of "
"people who use the system and want it kept whole. A lawmaker asked to fund park repairs can point to the "
"415,400 jobs and the spending in gateway towns as proof that the money comes back. Take the visitors away, "
"and that argument loses much of its force, along with the political will that keeps the parks funded at "
"all.\n\n"

"There is a warning folded into the same numbers. If use is what gives the parks their political and "
"economic weight, then policies that sharply limit visitors carry a hidden cost. Cutting access to protect "
"a fragile trail may also cut the spending that supports the town beside it and the jobs that town depends "
"on. The economic data do not settle the debate, but they raise the stakes on the preservation side of it. "
"Every limit placed on use is also a limit placed on the benefit the parks return to the public.\n\n"

"The economic view therefore reframes the founding tension rather than resolving it. It insists that "
"enjoyment is not a favor granted to tourists but a core part of what the parks are for, and that the "
"public value measured in those billions of dollars is exactly what preservation is meant to protect. The "
"harder that case is pressed, though, the sharper the reply from the other side becomes, because the same "
"popularity that produces the benefit is also what wears the parks down."
)

# --- Source 3: US NPS -- the preservation case that popularity is doing real damage ----------------
SOURCE_NPS_STRAIN = (
"The case for putting preservation first begins with a simple fact: the parks are being worn down by the "
"very popularity that proves their worth. The National Park Service reported 323 million recreation visits "
"in 2025. That total was actually a small drop, falling by 8.85 million visits, or 2.7 percent, from the "
"record set in 2024. Even with that dip, the larger pattern is unmistakable. The system now absorbs "
"hundreds of millions of visits year after year, a level of use its roads, trails, and buildings were never "
"designed to carry.\n\n"

"Years of heavy use and tight budgets have left a mark that can be measured in dollars. Roads, buildings, "
"and water systems break down faster than the agency can repair them. The National Park Service estimates "
"that by the end of the 2025 budget year, the cost of this delayed repair work had grown to about 24 "
"billion dollars. That backlog is the physical record of the imbalance: use has climbed into the hundreds "
"of millions while the money and staff needed to absorb it have not kept pace, so the wear simply "
"accumulates.\n\n"

"Crowding makes the strain worse in a way raw budgets do not capture. Visitors do not spread themselves "
"evenly. They gather at the most famous sites and during the summer months, so a handful of places bear the "
"weight of the whole system at its busiest times. Parking lots overflow, popular trails erode under "
"thousands of feet a day, and the staff of about 20,000 who run the entire system are stretched thinnest "
"exactly when the crowds are largest. The damage is concentrated where the love is greatest.\n\n"

"This is why the preservation side reads the founding law as a warning rather than a balance. The promise "
"to keep the parks unimpaired for future generations is not automatically satisfied by keeping them open. A "
"trail loved into a gully, or a historic building left to decay behind a 24 billion dollar repair backlog, "
"has been enjoyed today at the direct expense of the people not yet born who were also promised it. On this "
"view, some limits on use are not hostility to the public but the only honest way to keep the second half "
"of the mission.\n\n"

"The preservation argument does not deny the economic value of the parks. It insists instead that value is "
"borrowed, not free, if the crowds that create it are quietly destroying the thing they came to see. Left "
"unmanaged, popularity becomes a form of consumption. The parks can be spent like any other resource, and "
"the repair backlog is the bill coming due. Protecting the parks for the future, on this account, sometimes "
"means protecting them from the present. That can mean limiting how many cars enter on a peak day, "
"requiring reservations at the most crowded sites, or steering visitors toward the many units that carry "
"names other than national park. Each of those steps trims use now so that something is left to enjoy "
"later, which is exactly the trade the founding law demands."
)

# --- Source 4: US NPS -- DESCRIBED CHART (visual/quantitative), exempt from the word floor ----------
SOURCE_NPS_CHART = (
"This U.S. National Park Service data tracks recreation visits to the system and the size of the workforce "
"that manages them, two measures that together show how the balance between use and capacity has shifted.\n\n"
"According to the National Park Service, the system recorded 323 million recreation visits in 2025, a "
"decrease of 8.85 million visits, or 2.7 percent, from the record year of 2024. Against that flow of "
"hundreds of millions of visitors stands a permanent workforce of about 20,000 employees who keep the sites "
"open across all seasons.\n\n"
"Read side by side, the two figures sketch the core problem. Visits are counted in the hundreds of "
"millions; the staff who protect the parks and serve those visitors are counted in the tens of thousands. "
"A careful reader should treat the single-year 2.7 percent dip with caution: one year's decline against a "
"record does not reverse the long climb in use, and it does nothing to shrink the 24 billion dollar repair "
"backlog that the earlier years of record crowds helped build."
)

REC = StimulusRecord(
    id="ACC-W910-SYNTH-SET-0004",
    grade="11", mode="explanatory", family="synthesis_set",
    bucket="test", form="4trait", annotated=False,
    modeling_anchor="SBAC G11 full-write / AP Lang synthesis",
    acc_tags=["ACC.W.SRC.1", "ACC.W.INFO.2", "CCSS.W.11-12.7", "CCSS.W.11-12.8"],
    topic_id="national_parks_synthesis",
    prompt=("These four sources address one debatable question: how should the country balance letting the "
            "public use and enjoy the national parks against preserving them for future generations? Drawing "
            "on at least three of the sources, write an essay that develops and defends your own position on "
            "how that balance should be struck. Synthesize the sources to build your argument rather than "
            "summarizing them one by one, and cite each source you use."),
    passages=[
        Passage(title="A Mission With Two Halves",
                angle="the founding law's use-vs-preservation tension (US NPS)", text=SOURCE_NPS_MISSION),
        Passage(title="What the Parks Return",
                angle="the economic case that public use is the parks' core value (US DOI)", text=SOURCE_DOI_ECONOMY),
        Passage(title="The Cost of Being Loved",
                angle="the preservation case that popularity is doing measurable damage (US NPS)", text=SOURCE_NPS_STRAIN),
        Passage(title="Visits Against Capacity",
                angle="visual quantitative (chart): recreation visits vs. workforce size (US NPS)",
                text=SOURCE_NPS_CHART),
    ],
    fact_sources=[
        FactSource("Units in the National Park System", "433 units", "US NPS",
                   "https://www.nps.gov/aboutus/national-park-system.htm",
                   "433 units (often referred to as parks) ... covering more than 85 million acres"),
        FactSource("Total acreage of the system", "85 million acres", "US NPS",
                   "https://www.nps.gov/aboutus/national-park-system.htm",
                   "covering more than 85 million acres"),
        FactSource("Units titled 'national park'", "63", "US NPS",
                   "https://www.nps.gov/aboutus/national-park-system.htm",
                   "National Parks (63)"),
        FactSource("Number of naming designations", "19", "US NPS",
                   "https://www.nps.gov/aboutus/national-park-system.htm",
                   "at least 19 naming designations"),
        FactSource("Year NPS was created (Organic Act)", "1916", "US NPS",
                   "https://www.nps.gov/aboutus/history.htm",
                   "the Organic Act, signed August 25, 1916, created the National Park Service"),
        FactSource("NPS workforce size", "20,000 employees", "US NPS",
                   "https://www.nps.gov/aboutus/index.htm",
                   "Approximately 20,000 strong, the ... men and women of the National Park Service"),
        FactSource("Visitor spending in gateway communities 2023", "26.4 billion", "US DOI",
                   "https://www.doi.gov/pressreleases/national-parks-contributed-record-high-556-billion-us-economy-supported-415000-jobs",
                   "$26.4 billion in communities near national parks"),
        FactSource("Benefit to national economy 2023", "55.6 billion", "US DOI",
                   "https://www.doi.gov/pressreleases/national-parks-contributed-record-high-556-billion-us-economy-supported-415000-jobs",
                   "record high $55.6 billion benefit to the nation's economy"),
        FactSource("Jobs supported by visitor spending 2023", "415,400 jobs", "US DOI",
                   "https://www.doi.gov/pressreleases/national-parks-contributed-record-high-556-billion-us-economy-supported-415000-jobs",
                   "supported 415,400 jobs"),
        FactSource("Labor income from visitor spending 2023", "19.4 billion", "US DOI",
                   "https://www.doi.gov/pressreleases/national-parks-contributed-record-high-556-billion-us-economy-supported-415000-jobs",
                   "$19.4 billion in labor income"),
        FactSource("2025 recreation visits", "323 million", "US NPS",
                   "https://www.nps.gov/subjects/socialscience/annual-visitation-highlights.htm",
                   "The National Park Service reported 323 million recreation visits in calendar year 2025."),
        FactSource("Decline from 2024 record", "8.85 million / 2.7 percent", "US NPS",
                   "https://www.nps.gov/subjects/socialscience/annual-visitation-highlights.htm",
                   "a decrease of 8.85 million recreation visits, or 2.7%, from the record year in 2024"),
        FactSource("Deferred maintenance / repair backlog FY2025", "24 billion", "US NPS",
                   "https://www.nps.gov/subjects/infrastructure/deferred-maintenance.htm",
                   "an estimated $24 billion in repair need existed on roads, buildings, utility systems"),
    ],
    provenance={"copyright": "own_authored",
                "rights": "public-domain-sourced (US NPS + US DOI)",
                "authored": "2026-07-18",
                "note": ("Figures reused verbatim from the already-verified table in "
                         "Stimulus_Bank_G10/info_national_parks.py (fetched 2026-07-07); no new figures "
                         "introduced. Authored to give the G11 mid-gate a cold topic (F8).")},
)

if __name__ == "__main__":
    qc_stimulus(REC)
    import re
    for p in REC.passages:
        wc = len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", p.text))
        print(f"  passage '{p.title}': {wc} words")
    print(qc_report(REC))
    sys.exit(0 if REC.qc["passed"] else 1)
