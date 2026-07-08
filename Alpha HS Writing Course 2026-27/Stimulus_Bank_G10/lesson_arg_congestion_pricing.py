"""
Opposing-pair ARGUMENT stimulus for the G10 writing course (LESSON bucket).
Topic: Should cities charge tolls to drive downtown (congestion pricing)?
Family=opposing, mode=argument, bucket=lesson. Two original 500-900 word G10-register passages, each
conceding the other side. Figures trace to US federal public-domain sources (US DOT / FHWA, US BLS, US EPA,
US Census Bureau). Decomposes into two stance-tagged lesson singles under proposition prop_congestion_pricing.
No em dashes in prose. Runs itself through the QC harness.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

PASSAGE_A = (
"Every weekday morning, the same predictable pattern unfolds in large American downtowns: thousands of "
"cars pour toward the same few streets at the same hour, the roads fill, traffic slows to a crawl, and the "
"city loses time it can never recover. Supporters of congestion pricing argue there is a fair way to fix "
"this, which is to charge a toll to drive into the busiest part of the city during the busiest hours. The "
"underlying idea is straightforward. When a valuable road is both crowded and free, people inevitably "
"overuse it, but when drivers pay a modest price at peak times, some will choose a different hour, a "
"different route, or a bus or train instead. The road clears, and the people who genuinely need to drive "
"can finally move.\n\n"
"The scale of the problem is large. The Federal Highway Administration reports that Americans drive more "
"than 3 trillion miles on the nation's roads each year. A big share of those miles happen in dense urban "
"areas where there is no room to build new lanes. You cannot widen a downtown street without tearing down "
"the city around it. Congestion pricing treats the road like the limited space it really is.\n\n"
"The money matters too. A toll on peak driving raises funds, and cities can spend that money on the buses "
"and trains that give people a way to leave the car at home. That is the part supporters care about most. "
"Public transit serves people who cannot afford a car or cannot drive. When transit runs often and on time, "
"a toll is not a punishment. It is a trade. Drivers who choose to pay get a faster trip, and everyone who "
"rides transit gets a better system paid for by that toll.\n\n"
"There is a clean-air benefit as well. The Environmental Protection Agency reports that transportation is "
"the largest source of the greenhouse gas emissions the United States produces. Cars stuck in stop-and-go "
"traffic burn fuel and give nothing back. Fewer cars crawling downtown means less wasted fuel and cleaner "
"air for the people who live and work there.\n\n"
"Supporters also point to a lesson from cities that already tried it. When a downtown starts charging for "
"peak driving, the first thing that changes is the hour people travel. Some trips that did not have to "
"happen at eight in the morning move to nine or ten, when the road has room. A delivery that once idled in "
"gridlock now rolls through. This is the quiet power of a price. It does not order anyone to stay home. It "
"simply asks people to notice the true cost of the most crowded hour, and it lets them decide.\n\n"
"Supporters do not claim the toll is painless. A driver who must come downtown at rush hour will pay, and "
"that is a real cost. They also agree that the plan is only fair if the city protects people who earn the "
"least, through discounts or credits for low-income drivers. But they argue the current system already "
"charges everyone, just in a hidden way. It charges them in lost hours, in wasted fuel, and in dirty air. "
"A toll at least turns that hidden cost into money the city can use to build something better. To "
"supporters, that is the honest choice: pay for the road we share, and use what we collect to give people "
"a real way out of the car."
)

PASSAGE_B = (
"Congestion pricing sounds tidy on paper. Charge drivers to enter the crowded downtown, and the traffic "
"clears. But critics warn that the plan asks the wrong people to pay, and that it can fail the very city "
"it is meant to help. Their first worry is fairness. A toll is a flat charge. It costs a wealthy driver "
"the same few dollars it costs a worker earning far less, so the same toll takes a much bigger bite out of "
"the smaller paycheck. The people most likely to feel the sting are the ones who cannot shift their hours: "
"nurses, cleaners, and delivery workers who must be downtown at a set time.\n\n"
"The cost of driving is already heavy. The Bureau of Labor Statistics reports that transportation is one "
"of the largest expenses for the average American household, second only to housing. For a family that is "
"already stretched, a new daily toll is one more bill they did not choose. Critics say a city should think "
"hard before adding to that load.\n\n"
"There is also the question of whether the plan even works for everyone. Congestion pricing only feels fair "
"if there is a good bus or train to switch to. But transit is uneven. The Census Bureau reports that the "
"large majority of American commuters still drive to work, many of them alone, because transit near their "
"home does not go where they need to go. Telling those drivers to take a train they do not have is not a "
"real choice. It is a toll with no way around it.\n\n"
"Critics also point to the businesses downtown. If a toll makes people think twice about coming into the "
"city center, some shoppers and diners may simply go somewhere else. A store owner who depends on foot "
"traffic could lose customers to a mall outside the toll zone, where parking is free and no charge waits "
"at the door.\n\n"
"Critics raise a timing problem too. Building good transit takes years, but a toll can start the moment a "
"city flips the switch. That gap is the danger. If the charge comes first and the buses come later, drivers "
"are stuck paying for a choice they do not yet have. Supporters promise the toll money will fund transit, "
"but critics note that promise depends on how a city actually spends what it collects, and budgets can "
"drift toward other needs once the money is flowing.\n\n"
"None of this means traffic is fine. Critics agree that crowded downtowns are a real problem and that clean "
"air is worth protecting. But they argue there are fairer tools to try first. A city can improve its buses "
"and trains before it charges the toll, so the alternative is ready when drivers need it. It can offer "
"discounts to low-income drivers, or charge less at the edges of rush hour. What it should not do, critics "
"say, is rush to charge working people for a road their taxes already paid to build, and hope the buses "
"catch up later."
)

FACTS = [
    FactSource("US annual vehicle miles traveled", "3 trillion", "US DOT / Federal Highway Administration",
               "https://www.fhwa.dot.gov/policyinformation/travel_monitoring/tvt.cfm"),
    FactSource("Transportation is the largest source of US greenhouse gas emissions", "largest source",
               "US EPA", "https://www.epa.gov/ghgemissions/sources-greenhouse-gas-emissions"),
    FactSource("Transportation is a top household expense (second to housing)", "second-largest",
               "US Bureau of Labor Statistics", "https://www.bls.gov/cex/"),
    FactSource("Most US commuters drive to work, many alone", "majority drive alone",
               "US Census Bureau (American Community Survey)", "https://www.census.gov/topics/employment/commuting.html"),
]

rec = StimulusRecord(
    id="ACC-W910-ARG-OPP-LESSON-CONGESTION",
    grade="9-10", mode="argument", family="opposing", bucket="lesson",
    topic_id="congestion_pricing",
    modeling_anchor="Ohio ELA II / MD MCAP (opposing-view pick-a-side)",
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "CCSS.W.9-10.1"],
    prompt=("Weighing both sources, write an argumentative essay stating your position on whether cities "
            "should charge tolls to drive downtown during busy hours (congestion pricing). Support your claim "
            "with evidence from both sources, and respond to at least one objection from the side you do not take."),
    passages=[
        Passage(title="Charge for the Crowded Road: The Case for Congestion Pricing",
                angle="pro; DOT/EPA road-use and emissions data", text=PASSAGE_A),
        Passage(title="A Toll on the People Who Can Least Afford It",
                angle="con; BLS/Census household-cost and commuting data", text=PASSAGE_B),
    ],
    fact_sources=FACTS,
    provenance={"copyright": "own_authored", "rights": "public-domain-sourced (US DOT/EPA/BLS/Census)",
                "authored": "2026-07-08"},
)

SINGLES = [
    StimulusRecord(
        id="ACC-W910-ARG-SINGLE-CONGESTION-PRO", grade="9-10", mode="argument", family="single", bucket="lesson",
        modeling_anchor=rec.modeling_anchor, acc_tags=list(rec.acc_tags),
        prompt="Read this source arguing in favor of congestion pricing.",
        passages=[Passage(title=rec.passages[0].title, angle=rec.passages[0].angle, text=PASSAGE_A)],
        fact_sources=list(rec.fact_sources), provenance=dict(rec.provenance),
        topic_id="congestion_pricing", proposition_id="prop_congestion_pricing", stance="pro",
        form="staar", task_demand=3),
    StimulusRecord(
        id="ACC-W910-ARG-SINGLE-CONGESTION-CON", grade="9-10", mode="argument", family="single", bucket="lesson",
        modeling_anchor=rec.modeling_anchor, acc_tags=list(rec.acc_tags),
        prompt="Read this source arguing against congestion pricing.",
        passages=[Passage(title=rec.passages[1].title, angle=rec.passages[1].angle, text=PASSAGE_B)],
        fact_sources=list(rec.fact_sources), provenance=dict(rec.provenance),
        topic_id="congestion_pricing", proposition_id="prop_congestion_pricing", stance="con",
        form="staar", task_demand=3),
]

if __name__ == "__main__":
    import re
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
    import readability_gate as rg
    qc_stimulus(rec)
    for p in rec.passages:
        wc = len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", p.text))
        lex = rg.analyze_text(p.text)["lexile_estimate"]
        print(f"passage '{p.title[:40]}': {wc} words, ~{lex}L")
    print(qc_report(rec))
    assert len(SINGLES) == 2 and {x.stance for x in SINGLES} == {"pro", "con"}
    for x in SINGLES:
        qc_stimulus(x)
        assert x.qc["passed"], f"single {x.id} failed: {x.qc.get('first_failure')}"
    print("SINGLES decomposition OK")
    sys.exit(0 if rec.qc["passed"] else 1)
