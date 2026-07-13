"""
Opposing-pair ARGUMENT stimulus for the G9 (English I band) writing TEST bank.
Topic: Should schools switch to a year-round calendar?  family=opposing, mode=argument, bucket=test.
TWO original G9-register passages (~500-620 words each, targeted 1010-1150L), one pro and one con, each
conceding the other side. >=2 distinct source orgs for credibility contrast:
  PRO side  (spacing / summer gap / room to grow):  US Dept. of Education / NCES.
  CON side  (cost / family strain / no more days):  US Census Bureau  (+ NCES calendar context).
Every numeric figure in prose traces to a federal page fetched live 2026-07-08. No em/en dashes in prose.
Runs itself through the QC harness and exits on the verdict.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# ---------------------------------------------------------------------------
# PASSAGE A  -  pro-year-round (NCES calendar data + 180-day standard)
# ---------------------------------------------------------------------------
PASSAGE_A = (
"For most American students, the school year follows an old pattern. They study for about nine months, "
"then take a long summer off. This calendar is older than the students who follow it. It was built for "
"a time when many children helped on farms in summer. Few students farm today. Supporters of "
"year-round school say the summer break has outlived its purpose. They want a calendar that fits "
"modern life.\n\n"

"A year-round calendar does not add more school. It keeps the same number of days. Most states already "
"set that number. The National Center for Education Statistics reports that in 2018, 28 states required "
"180 instructional days. A year-round school still meets that mark. It simply spreads the days out. "
"Instead of one long summer, students take several short breaks. A common plan is 45 days of school, "
"then a shorter break, repeated through the year.\n\n"

"The main reason for this switch is memory. Over a long summer, students forget some of what they "
"learned. Teachers then spend weeks each fall reviewing old material. Supporters call this the summer "
"slide. Shorter breaks give the brain less time to forget. When students return after two or three "
"weeks, the lessons are still fresh. Less review means more time for new learning.\n\n"

"Shorter breaks may help in other ways too. A long stretch of school can wear students down. Frequent "
"breaks give tired minds a chance to rest and reset. Students can return with fresh energy. Teachers "
"get the same benefit. A calendar with regular pauses may keep both groups steadier across the year. "
"Fewer weeks of burnout, supporters say, can mean fewer weeks of lost effort.\n\n"

"There may be a fairness benefit as well. Wealthy families often fill the long summer with camps, trips, "
"and lessons. Poorer families may not afford any of that. So the gap between students can grow wider "
"over one long break. Supporters argue that shorter breaks shrink that gap. When students are away for "
"only a few weeks at a time, the summer slide affects everyone less.\n\n"

"Right now, very few schools use this plan. The same federal agency reports that only 4.1 percent of "
"public schools had all students on a year-round calendar in the 2011 to 2012 school year. That was "
"about 3,700 schools out of roughly 90,000. A few years earlier, in the 2007 to 2008 school year, the "
"share was 4.4 percent. So the idea is rare, but it has been tried. Supporters see room to grow. They "
"argue that most schools stick with the old calendar out of habit, not proof that it works best.\n\n"

"Supporters know a new calendar brings real trouble. Summer camps, family trips, and student jobs are "
"all built around the long break. Working parents plan childcare around it too. These are honest "
"concerns, and supporters do not dismiss them. But they argue that schedules can adjust over time. The "
"deeper goal is learning. If a calendar helps students remember more and burn out less, supporters say, "
"it deserves a fair look. The summer break made sense for a farming country. Today, they argue, schools "
"should build a calendar around how students actually learn."
)

# ---------------------------------------------------------------------------
# PASSAGE B  -  against a year-round switch (US Census family-strain + NCES day-count context)
# ---------------------------------------------------------------------------
PASSAGE_B = (
"The idea behind year-round school sounds smart. Spread the days out, and students forget less. But a "
"calendar does not live on a chart. It lives in the daily lives of families, workers, and whole towns. "
"Critics warn that a year-round switch can cause more harm than good. The costs are real, and they land "
"hardest on the families with the least.\n\n"

"Start with a plain fact. Year-round school does not add a single day of learning. It keeps the same "
"total. The National Center for Education Statistics reports that in 2018, 28 states required 180 "
"instructional days. A year-round plan meets that same number. It only moves the days around. So the "
"promise of more learning time is misleading. Students are not in class any longer than before.\n\n"

"The heavier problem is money and childcare, which a schedule change quietly multiplies. A long summer "
"is relatively easy to plan around, because parents can arrange a single camp or one steady sitter. A "
"year-round calendar instead breaks the year into many short gaps, and each separate gap demands its "
"own childcare arrangement. For families already stretched thin financially, that repeated expense "
"becomes a serious burden. The U.S. Census Bureau reports that the official poverty rate was 11.5 "
"percent in 2022. Using a fuller measure that accounts for costs and benefits, child poverty reached "
"12.4 percent in 2022, a sharp increase from just 5.2 percent the previous year. Scattered breaks can "
"force these vulnerable families to arrange and pay for supervision again and again.\n\n"

"Older students feel the pressure too, often in ways adults overlook. Many teenagers work over the "
"summer to help at home or to save for the future, and a long break lets them hold a steady job. "
"Dividing the year into short pieces makes that far harder. An employer wants workers who can stay "
"through the whole season, so a student who leaves every few weeks is hard to hire. In that quiet way, "
"a year-round calendar can cost teenagers income they truly depend on.\n\n"

"Schools themselves absorb additional costs under a year-round model. Operating a large building "
"through the hottest summer months is genuinely expensive, and cooling crowded classrooms in July "
"drives energy bills sharply upward. Buses, staff, and cafeteria meals must all run across more of the "
"calendar. For a district already managing a tight budget, these accumulated expenses are hardly "
"trivial. That same money, critics point out, might accomplish far more if spent on books, teachers, "
"or smaller classes.\n\n"

"Critics of year-round school are not against helping students remember. They agree the summer slide is "
"real and worth study. Their point is narrower. A change this large, which touches every family's "
"summer and every school's budget, should not be forced from the top. It should be weighed slowly, "
"district by district. Some communities may find the trade worth it. But many will not. Before a "
"district scraps the summer break, critics argue, it should ask a fair question. Does moving the days "
"around truly help students, or does it just shuffle the same year and hand families a new bill?"
)

FACTS = [
    # ---- shared / framing (NCES) ----
    FactSource("States requiring 180 instructional days, 2018", "28 states; 180 days",
               "US Dept. of Education / NCES",
               "https://nces.ed.gov/programs/statereform/tab5_14.asp",
               "Number of instructional days and hours in the school year, by state: 2018 ... 180"),
    # ---- PRO side (NCES calendar adoption) ----
    FactSource("Public schools with all students on year-round calendar, 2011-12", "4.1 percent",
               "US Dept. of Education / NCES",
               "https://nces.ed.gov/programs/digest/d13/tables/dt13_234.12.asp",
               "Percent of schools with a year-round calendar cycle ... 4.1"),
    FactSource("Year-round schools and total public schools, 2011-12", "3,700 of 90,000",
               "US Dept. of Education / NCES",
               "https://nces.ed.gov/programs/digest/d13/tables/dt13_234.12.asp",
               "Number of schools with year-round calendar cycle 3,700 ... Total number of public schools 90,000"),
    FactSource("Public schools with all students on year-round calendar, 2007-08", "4.4 percent",
               "US Dept. of Education / NCES",
               "https://nces.ed.gov/surveys/sass/tables/sass0708_1023181_s1n.asp",
               "all public schools totaled 90,760 ... 4.4 percent had all students attending a year-round calendar"),
    # ---- CON side (US Census Bureau) ----
    FactSource("US official poverty rate, 2022", "11.5 percent", "US Census Bureau",
               "https://www.census.gov/library/publications/2023/demo/p60-280.html",
               "The official poverty rate in 2022 was 11.5 percent"),
    FactSource("Child poverty rate (Supplemental Poverty Measure), 2022", "12.4 percent", "US Census Bureau",
               "https://www.census.gov/library/publications/2023/demo/p60-280.html",
               "SPM child poverty rate more than doubled, from 5.2 percent in 2021 to 12.4 percent in 2022"),
    FactSource("Child poverty rate (SPM), 2021", "5.2 percent", "US Census Bureau",
               "https://www.census.gov/library/publications/2023/demo/p60-280.html",
               "from 5.2 percent in 2021 to 12.4 percent in 2022"),
]

REC = StimulusRecord(
    id="ACC-W910-ARG-OPP-0008",
    grade="9", mode="argument", family="opposing", bucket="test",
    form="ohio", annotated=False,
    topic_id="year_round_school",
    modeling_anchor="Ohio ELA II / MD MCAP (opposing-view pick-a-side)",
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "CCSS.W.9-10.1"],
    prompt=("Weighing both sources, write an argumentative essay stating your position on whether schools "
            "should switch to a year-round calendar. Support your claim with specific evidence from both "
            "sources, and respond to at least one objection from the side you do not take."),
    passages=[
        Passage(title="The Case for a Year-Round Calendar",
                angle="pro-year-round; US Dept. of Education / NCES calendar-adoption and instructional-day data",
                text=PASSAGE_A),
        Passage(title="Why Year-Round School Costs Families More",
                angle="against a year-round switch; US Census Bureau family-strain data plus NCES day-count context",
                text=PASSAGE_B),
    ],
    fact_sources=FACTS,
    provenance={"copyright": "own_authored",
                "rights": "public-domain-sourced (US federal)",
                "authored": "2026-07-08"},
)

if __name__ == "__main__":
    import re
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
    import readability_gate as rg
    for p in REC.passages:
        wc = len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", p.text))
        lex = rg.analyze_text(p.text)["lexile_estimate"]
        print(f"passage '{p.title[:44]}': {wc} words, ~{lex}L")
    qc = qc_stimulus(REC); print(qc_report(REC)); import sys; sys.exit(0 if qc["passed"] else 1)
