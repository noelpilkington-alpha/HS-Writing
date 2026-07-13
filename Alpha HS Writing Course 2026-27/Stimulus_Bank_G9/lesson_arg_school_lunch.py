"""
Single-source ARGUMENT stimulus for the G9 (English I band) writing course (LESSON bucket).
Topic: Should schools offer free meals to all students?
grade=9, mode=argument, family=single, bucket=lesson. One original G9-register passage (~520-620 words,
targeted 1010-1150L) that presents the issue with evidence on both sides so the student can argue a position.
Figures trace to US federal public-domain sources (US Dept. of Agriculture / ERS, US Dept. of Education /
NCES). No em dashes / en dashes in prose. Runs itself through the QC harness and exits on the verdict.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

PASSAGE = (
"Every school day, millions of American students line up for lunch. For many of them, that meal is free "
"or sold at a low price. The National School Lunch Program is a federal program that helps pay for these "
"meals. According to the U.S. Department of Agriculture, the program served more than 4.8 billion lunches "
"in a recent year, at a total cost of about 17.7 billion dollars. It runs in nearly 100,000 public and "
"private schools across the country. That makes it one of the largest food programs the nation operates.\n\n"
"Right now, not every student eats for free. A family must earn below a set income to qualify. The "
"National Center for Education Statistics reports that students can get free or reduced-price meals when "
"their family income falls under 185 percent of the federal poverty line. Students above that line pay "
"full price. This system tries to aim the most help at the families who need it most.\n\n"
"Some people argue the country should go further and offer free meals to every student, no matter what "
"their families earn. They make several points. First, hunger hurts learning. A student who skips lunch "
"may struggle to focus in an afternoon class. Second, the current system can embarrass students. When "
"only some children get free food, their classmates may notice. To avoid that shame, some students skip "
"meals they are owed. A universal program would erase that line completely. Every student would eat the "
"same way, so no child would be marked as poor.\n\n"
"Supporters also point to who fills our neediest schools. The National Center for Education Statistics "
"reports that about 10.5 million students attended high-poverty public schools in one recent year. In "
"those buildings, nearly every child already qualifies for a free meal. Feeding everyone, supporters "
"say, would cut paperwork and make sure no hungry student slips through the cracks.\n\n"
"Others are not convinced. They agree that no child should go hungry, but they question the cost. Feeding "
"every student, including children from wealthy homes, would raise the price of a program that is already "
"expensive. Critics ask whether that money could do more good if it were aimed only at the families who "
"truly need it. A wealthy family, they argue, can easily pay for lunch, so why should taxpayers cover it?\n\n"
"Critics raise a second worry about waste. When food is free, some students take a full tray and then "
"throw much of it away. If meals are free for everyone, that waste could grow. A school should think "
"carefully, critics say, before handing out food that ends up in the trash.\n\n"
"Both sides agree on the basic goal. A hungry student cannot learn well, and school should not be a place "
"where children go without food. The disagreement is about the best path. Should the country feed every "
"student and treat lunch like a free part of school, the way it treats textbooks and buses? Or should it "
"keep aiming its limited dollars at the families who need help the most? That is the question you must "
"now decide."
)

FACTS = [
    FactSource("Lunches served by the National School Lunch Program in a recent year", "4.8 billion",
               "US Dept. of Agriculture (Economic Research Service)",
               "https://www.ers.usda.gov/topics/food-nutrition-assistance/child-nutrition-programs/national-school-lunch-program",
               verbatim="more than 4.8 billion lunches"),
    FactSource("Total cost of the National School Lunch Program in a recent year", "17.7 billion",
               "US Dept. of Agriculture (Economic Research Service)",
               "https://www.ers.usda.gov/topics/food-nutrition-assistance/child-nutrition-programs/national-school-lunch-program",
               verbatim="total cost of $17.7 billion"),
    FactSource("Schools and institutions the program operates in", "100,000",
               "US Dept. of Agriculture (Economic Research Service)",
               "https://www.ers.usda.gov/topics/food-nutrition-assistance/child-nutrition-programs/national-school-lunch-program",
               verbatim="operates in nearly 100,000 public and nonprofit private schools"),
    FactSource("Income cutoff for free or reduced-price meals", "185 percent",
               "US Dept. of Education / National Center for Education Statistics",
               "https://nces.ed.gov/fastfacts/display.asp?id=898",
               verbatim="under 185 percent of the poverty threshold"),
    FactSource("Students in high-poverty public schools in a recent year", "10.5 million",
               "US Dept. of Education / National Center for Education Statistics",
               "https://nces.ed.gov/fastfacts/display.asp?id=898",
               verbatim="about 10.5 million students attended high-poverty schools"),
]

REC = StimulusRecord(
    id="ACC-W910-ARG-LESSON-SCHOOLLUNCH",
    grade="9", mode="argument", family="single", bucket="lesson",
    topic_id="free_school_meals",
    modeling_anchor="STAAR English I argumentative ECR",
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "ACC.W.SRC.3", "CCSS.W.9-10.1"],
    prompt=("Read the source about free school meals. Then write an argumentative essay stating your "
            "position on whether schools should offer free meals to all students. Support your claim with "
            "evidence from the source, and respond to at least one objection from the side you do not take."),
    passages=[
        Passage(title="Free Lunch for Everyone? A School Meals Debate",
                angle="issue-presenting single source; USDA/ERS program data and NCES poverty data", text=PASSAGE),
    ],
    fact_sources=FACTS,
    provenance={"copyright": "own_authored", "rights": "public-domain-sourced (US federal)",
                "authored": "2026-07-08"},
)

if __name__ == "__main__":
    import re
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
    import readability_gate as rg
    for p in REC.passages:
        wc = len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", p.text))
        lex = rg.analyze_text(p.text)["lexile_estimate"]
        print(f"passage '{p.title[:40]}': {wc} words, ~{lex}L")
    qc = qc_stimulus(REC); print(qc_report(REC)); import sys; sys.exit(0 if qc["passed"] else 1)
