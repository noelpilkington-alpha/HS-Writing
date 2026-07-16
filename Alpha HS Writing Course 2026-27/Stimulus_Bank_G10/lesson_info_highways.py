"""
Single-source EXPLANATORY LESSON stimulus for the G10 writing bank: the Interstate Highway
System (history, scale, funding, function). Explain, do not argue.

bucket="lesson", family="single", mode="explanatory". Every figure traces to a fetched federal
page (US DOT / FHWA). Runs itself through the QC harness and reports. No em dashes in prose.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# Explanatory passage, G10 register, neutral tone. Every figure from a fetched federal page.
PASSAGE = (
"Most Americans have traveled on an interstate highway without ever thinking about it. The wide, "
"divided road with its blue and red shield is simply part of the landscape. Yet that road is part of one "
"of the largest building projects in the nation's history. It is called the Interstate Highway System. "
"This passage explains how the system began, how big it grew, how the country paid for it, and what it "
"does for daily life.\n\n"

"The story begins in the middle of the twentieth century. After World War II, more Americans owned cars "
"than ever before. The nation's roads, though, were a patchwork. Many were narrow, crowded, and slow. In "
"1956, Congress passed the Federal-Aid Highway Act. President Dwight Eisenhower signed it into law. The "
"act launched a plan for a connected network of modern, high-speed roads that would tie the whole country "
"together. Eisenhower had seen the value of such roads in Europe, and he pushed the idea as both a "
"convenience and a matter of national defense.\n\n"

"The scale of what followed was enormous. Over the decades that followed, crews built a network that now "
"runs about 46,876 miles. These roads reach nearly every large city in the country. They cross mountains, "
"span rivers, and cut through deserts. Building them meant moving vast amounts of earth, pouring millions "
"of tons of concrete, and raising thousands of bridges. The project took far longer than planners first "
"expected. It stretched across many decades rather than the twelve years first imagined.\n\n"

"A project this large raised an obvious question: who would pay for it? The answer was a partnership "
"between the federal government and the states. Under the 1956 law, the federal government agreed to "
"cover 90 percent of the cost of building the interstates. Each state paid the remaining share and took "
"charge of the work inside its own borders. The federal money came mostly from a tax on gasoline and "
"diesel fuel. That money flowed into a special account called the Highway Trust Fund. The idea was "
"simple. The people who used the roads, and who bought the fuel to drive on them, would help pay to build "
"and maintain them. The original plan was expected to cost about 25 billion dollars, but the final "
"figure ran far higher, near 114 billion dollars over the life of the program.\n\n"

"What does all this pavement actually do? Its main job is to move people and goods quickly and safely "
"over long distances. The interstates make up only a small fraction of the nation's total road mileage. "
"Even so, they carry a huge share of its traffic. The Federal Highway Administration reports that about "
"one quarter of all the miles driven in the country take place on the Interstate Highway System. That "
"means a small slice of the road network does a large slice of the work.\n\n"

"The system shapes the economy as much as it shapes travel. Trucks use the interstates to carry food, "
"fuel, and factory goods across state lines. A store shelf in one state may hold products that rode an "
"interstate from a farm or plant a thousand miles away. The roads also let people live in one town and "
"work in another. Whole suburbs grew up around interstate exits.\n\n"

"Taken together, the pieces tell a clear story. A law passed in 1956 set off decades of construction. A "
"funding partnership, paid largely through a fuel tax, spread the cost between the nation and the states. "
"The result is a network of about 46,876 miles that carries roughly a quarter of the country's driving. "
"The interstate is easy to overlook precisely because it works so well. Understanding how it was built, "
"and how it is paid for, shows just how much planning lies beneath an ordinary drive."
)

rec = StimulusRecord(
    id="ACC-W910-INFO-LESSON-HIGHWAYS",
    grade="9-10", mode="explanatory", family="single", bucket="lesson",
    topic_id="interstate_highways",
    annotated=False,
    modeling_anchor="STAAR English II / MCAS (single-source informational)",
    acc_tags=["ACC.W.INFO.1", "ACC.W.INFO.4", "CCSS.W.9-10.2"],
    prompt=("Write a well-organized informational composition that uses specific evidence from the article "
            "\"Building the Interstate Highway System\" to explain how the system began, how large it grew, "
            "how the country paid for it, and what it does for daily life."),
    passages=[Passage(title="Building the Interstate Highway System", text=PASSAGE)],
    fact_sources=[
        FactSource("Year the Federal-Aid Highway Act launched the interstate system", "1956",
                   "US DOT / Federal Highway Administration",
                   "https://highways.dot.gov/highway-history/interstate-system/50th-anniversary/interstate-frequently-asked-questions",
                   "Federal-Aid Highway Act of 1956 ... signed June 29, 1956"),
        FactSource("Total length of the Interstate Highway System", "46,876 miles",
                   "US DOT / Federal Highway Administration",
                   "https://highways.dot.gov/highway-history/interstate-system/50th-anniversary/interstate-frequently-asked-questions",
                   "currently, the Interstate System is 46,876 miles long"),
        FactSource("Federal government's share of interstate construction cost", "90 percent",
                   "US DOT / Federal Highway Administration",
                   "https://highways.dot.gov/highway-history/interstate-system/50th-anniversary/interstate-frequently-asked-questions",
                   "the Federal Government would pay 90 percent of the cost of construction"),
        FactSource("Original estimated cost of the interstate program", "25 billion dollars",
                   "US DOT / Federal Highway Administration",
                   "https://highways.dot.gov/highway-history/interstate-system/50th-anniversary/interstate-frequently-asked-questions",
                   "estimated to cost $25 billion over 12 years"),
        FactSource("Final cost of the interstate program over its life", "114 billion dollars",
                   "US DOT / Federal Highway Administration",
                   "https://highways.dot.gov/highway-history/interstate-system/50th-anniversary/interstate-frequently-asked-questions",
                   "final cost ... $114 billion"),
        FactSource("Share of all vehicle miles driven that occur on interstates", "one quarter / 25 percent",
                   "US DOT / Federal Highway Administration",
                   "https://www.fhwa.dot.gov/policyinformation/travel_monitoring/tvt.cfm",
                   "about one quarter of all vehicle miles driven in the country used the Interstate Highway System"),
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
