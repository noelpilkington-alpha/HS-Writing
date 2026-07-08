"""
Opposing-pair argument stimulus for the G10 writing test bank, authored through the proven engine.
Topic: Should the federal minimum wage be raised to $15/hour?
Family=opposing, mode=argument. Every figure traces to a fetched FEDERAL page:
  - US CBO, "The Budgetary Effects of the Raise the Wage Act of 2021" (publication 56975), fetched
    2026-07-07 via the Internet Archive snapshot of cbo.gov (live cbo.gov is CAPTCHA-gated; the archived
    federal page is public domain, 17 USC 105).
  - US Bureau of Labor Statistics, "Characteristics of minimum wage workers, 2022" (Report 1104).
  - US Department of Labor, Wage and Hour Division, "Minimum Wage."
Runs itself through the QC harness (all 6 gates) and reports. No em dashes in passage prose.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# ---------------------------------------------------------------------------
# Source A: RAISE IT. Angle = pro-raise; CBO earnings/poverty + DOL frozen-floor data.
# Concedes the other side's strongest point (CBO's 1.4 million job-loss estimate).
# ---------------------------------------------------------------------------
PASSAGE_A = (
"The federal minimum wage sets the lowest hourly pay an employer can legally give most workers. "
"According to the U.S. Department of Labor, that floor has stood at 7.25 dollars per hour since "
"July 24, 2009. Prices have climbed in the years since, but the wage itself has not moved. "
"Supporters argue that a floor frozen for more than a decade no longer does its job, and that "
"Congress should raise it to 15 dollars per hour.\n\n"

"The strongest case for raising the wage is the sheer number of people it would help. The "
"Congressional Budget Office studied a 2021 bill that would have lifted the federal minimum to 15 "
"dollars an hour by 2025. In an average week that year, the office estimated, 17 million workers who "
"would otherwise earn less than 15 dollars would be directly affected. Millions more who earn a "
"little above that line would likely see raises too, as employers adjust their pay ladders. These "
"are not abstract figures. They are cashiers, home health aides, cooks, and warehouse workers whose "
"paychecks would grow.\n\n"

"Those raises add up to real money in real households. The Congressional Budget Office estimated "
"that the higher wage would deliver 509 billion dollars in additional pay to people who kept their "
"jobs under the bill. For a worker earning near the current floor, an extra few dollars an hour can "
"mean the difference between covering the rent and falling behind. Supporters say that money would "
"not vanish. Low-wage workers tend to spend what they earn quickly, on groceries, gas, and other "
"local needs, which sends that spending back into their own communities.\n\n"

"The wage floor also reaches the people who need it most. The same Congressional Budget Office "
"report estimated that raising the minimum to 15 dollars would lift 0.9 million people out of "
"poverty. A person who works full time should not have to live below the poverty line, supporters "
"argue, yet at 7.25 dollars an hour a full year of full-time work still leaves many families short. "
"Raising the floor is a direct way to reward work and to shrink the number of households who work "
"hard and still cannot afford the basics.\n\n"

"Honesty requires facing the strongest objection head on. The Congressional Budget Office also "
"estimated that the same increase would reduce employment by about 1.4 million workers. Supporters "
"do not dismiss that cost. But they point out that the office calls this an average estimate, which "
"means the true effect could be smaller, and that it must be weighed against the 17 million workers "
"who would earn more and the nearly one million who would climb out of poverty. A policy that helps "
"tens of millions while risking harm to a much smaller group is still worth adopting, they argue, "
"especially if it is phased in gradually so businesses can adjust.\n\n"

"That gradual approach matters. The 2021 bill did not jump the wage overnight. It raised the floor "
"in yearly steps, reaching 15 dollars only in 2025. Step increases give employers time to plan, to "
"raise prices slowly, and to find savings before the full raise arrives. Supporters say this is how "
"a responsible increase should work: predictable, announced years ahead, and tied afterward to the "
"growth of typical wages so the floor never again sits frozen for a decade.\n\n"

"In the end, supporters return to a simple standard. A minimum wage is meant to guarantee that a "
"hard day of work pays enough to live on. By that measure, a floor stuck at 7.25 dollars for well "
"over ten years has failed, while millions of workers wait. Raising it to 15 dollars, they argue, "
"would restore the wage's basic purpose and reward the people who keep stores open, meals served, "
"and patients cared for."
)

# ---------------------------------------------------------------------------
# Source B: RAISE IT CAREFULLY, OR NOT AT ALL. Angle = caution; CBO job-loss/deficit + BLS worker profile.
# Concedes the other side's strongest point (real wage gains + people lifted from poverty).
# ---------------------------------------------------------------------------
PASSAGE_B = (
"Almost everyone agrees that a raise would help the workers who receive it. The Congressional Budget "
"Office estimated that lifting the federal minimum wage to 15 dollars an hour would deliver hundreds "
"of billions of dollars in higher pay and would lift roughly 0.9 million people out of poverty. "
"Those gains are real, and no honest argument ignores them. Yet the same federal research shows why "
"raising the floor so high, so fast, carries serious risks, and why many economists urge caution.\n\n"

"Start with jobs. The Congressional Budget Office estimated that raising the federal minimum to 15 "
"dollars an hour would cut employment by about 1.4 million workers, its average estimate. When labor "
"costs more, some bosses hire fewer people, cut hours, or turn to machines. The workers most likely "
"to lose those first jobs are often the least skilled. That means the very people a higher wage is "
"meant to help can be the ones shut out of work.\n\n"

"The costs do not stop at the workplace. The same report found that the increase would add 54 "
"billion dollars to the federal budget deficit from 2021 to 2031. It also warned that higher wages "
"would push up prices for goods and services, from restaurant meals to health care. Those higher "
"prices fall on everyone. That includes the low-income families a wage increase is meant to protect. "
"A raise that comes with higher grocery and rent bills can take back with one hand what it gives "
"with the other.\n\n"

"Federal data also raise a question about how many workers a 15 dollar floor would truly reach "
"through the current minimum. The U.S. Bureau of Labor Statistics reports that only about 1.0 "
"million workers earned at or below the federal minimum wage of 7.25 dollars in 2022. That is just "
"1.3 percent of all hourly paid workers, far below the 13.4 percent recorded in 1979. Many states "
"and cities have already set their own minimums well above the federal floor. That is one reason so "
"few workers still earn 7.25 dollars. A single national figure of 15 dollars ignores how differently "
"a dollar stretches in a small town compared with a big city.\n\n"

"Who earns the minimum also matters. The Bureau of Labor Statistics reports that workers under age "
"25 make up about 45 percent of those paid the federal minimum or less, though they are only about "
"one-fifth of hourly workers. Among teens paid by the hour, about 3 percent earn the minimum or "
"less, compared with just under 1 percent of workers age 25 and older. Many minimum wage jobs are "
"first jobs, part-time jobs, or stepping stones. They are not the sole support of a family. Cautious "
"observers argue that a steep national raise aimed at that group could wipe out the very first jobs "
"where young workers gain their skills.\n\n"

"None of this means the wage should stay frozen forever. It means the size and speed of any raise "
"deserve care. A raise phased in more slowly, or set to fit local living costs, might capture much "
"of the benefit while avoiding the sharpest job losses. Some argue the choice belongs closer to "
"home, with the states and cities that know their own economies, rather than in one figure applied "
"from Maine to Mississippi.\n\n"

"The honest conclusion is that this is a trade-off, not a free gift. Higher pay for millions of "
"workers is a real good. So is the paycheck of the worker who keeps a job, the budget of the family "
"facing higher prices, and the chance for a teen looking for a first job. Weighing those interests, "
"the cautious case is not that the minimum wage should never rise. It is that raising it to 15 "
"dollars nationwide, all at once, may cost more than its supporters admit."
)

CBO_URL = "http://web.archive.org/web/20211215061809/https://www.cbo.gov/publication/56975"
BLS_URL = "https://www.bls.gov/opub/reports/minimum-wage/2022/home.htm"
DOL_URL = "https://www.dol.gov/agencies/whd/minimum-wage"

rec = StimulusRecord(
    id="ACC-W910-ARG-OPP-0002",
    grade="9-10", mode="argument", family="opposing",
    modeling_anchor="Ohio ELA II / MD MCAP (opposing-view pick-a-side argument)",
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "ACC.W.ARG.5", "CCSS.W.9-10.1", "OH.ELA.W.9-10.1"],
    prompt=("Weighing both sources, write an argumentative essay stating your position on whether the "
            "federal minimum wage should be raised to 15 dollars per hour. Support your claim with "
            "specific evidence from BOTH sources, and address at least one objection from the side you "
            "do not take."),
    passages=[
        Passage(title="Raise the Floor: The Case for a 15 Dollar Minimum Wage",
                angle="pro-raise; CBO earnings/poverty gains + DOL frozen-floor data", text=PASSAGE_A),
        Passage(title="Raise It Carefully, or Not at All",
                angle="caution/against; CBO job-loss and deficit costs + BLS worker-profile data", text=PASSAGE_B),
    ],
    fact_sources=[
        FactSource("Federal minimum wage has been $7.25/hr since 2009", "$7.25 / July 24, 2009", "US DOL",
                   DOL_URL,
                   "The federal minimum wage is $7.25 per hour effective July 24, 2009."),
        FactSource("Workers directly affected by a $15 minimum in 2025", "17 million", "US CBO",
                   CBO_URL,
                   "17 million workers whose wages would otherwise be below $15 per hour would be directly affected"),
        FactSource("Higher pay delivered to workers who kept jobs", "509 billion", "US CBO",
                   CBO_URL,
                   "higher pay ($509 billion) for people who were employed at higher hourly wages under the bill"),
        FactSource("People lifted out of poverty", "0.9 million", "US CBO",
                   CBO_URL,
                   "The number of people in poverty would be reduced by 0.9 million."),
        FactSource("Reduction in employment (CBO average estimate)", "1.4 million / 0.9 percent", "US CBO",
                   CBO_URL,
                   "Employment would be reduced by 1.4 million workers, or 0.9 percent, according to CBO's average estimate"),
        FactSource("Increase in the cumulative federal budget deficit", "54 billion", "US CBO",
                   CBO_URL,
                   "the cumulative budget deficit over the 2021-2031 period would increase by $54 billion"),
        FactSource("Workers at or below the federal minimum wage, 2022", "1.0 million / 1.3 percent", "US BLS",
                   BLS_URL,
                   "these 1.0 million workers with wages at or below the federal minimum made up 1.3 percent of all hourly paid workers"),
        FactSource("Share earning federal minimum or less vs 1979", "13.4 percent", "US BLS",
                   BLS_URL,
                   "well below the percentage of 13.4 recorded in 1979"),
        FactSource("Under-25 share of those paid federal minimum or less", "45 percent", "US BLS",
                   BLS_URL,
                   "workers under age 25 ... made up about 45 percent of those paid the federal minimum wage or less"),
        FactSource("Teens vs workers 25+ earning minimum or less", "3 percent / 1 percent", "US BLS",
                   BLS_URL,
                   "about 3 percent earned the minimum wage or less, compared with just under 1 percent of workers age 25 and older"),
    ],
    provenance={"copyright": "own_authored",
                "rights": "public-domain-sourced (US CBO + US BLS + US DOL; federal, 17 USC 105)",
                "two_source_verified": True,
                "cbo_fetched_via": "Internet Archive snapshot 20211215061809 of cbo.gov/publication/56975 "
                                   "(live cbo.gov CAPTCHA-gated); figures verbatim from the archived federal page",
                "authored": "2026-07-07"},
)


# --- Two-bucket migration: decompose the opposing pair into stance-tagged TEST singles ---------
# One pro + one con member of proposition "prop_minimum_wage". The pair above (rec) is retained for backward
# compatibility; the singles are what the composer assembles opposing pairs from. Each single carries the
# FULL fact_sources list (the anti-fabrication gate only requires the figures IN its passage to be covered;
# extra rows are harmless and guarantee the >=3 citable-fact minimum).
SINGLES = [
    StimulusRecord(
        id="ACC-W910-ARG-SINGLE-MINIMUM-WAGE-PRO",
        grade="9-10", mode="argument", family="single", bucket="test",
        modeling_anchor=rec.modeling_anchor,
        acc_tags=list(rec.acc_tags),
        prompt="Read this source arguing in favor of the proposal.",
        passages=[Passage(title=rec.passages[0].title, angle=rec.passages[0].angle, text=rec.passages[0].text)],
        fact_sources=list(rec.fact_sources),
        provenance=dict(rec.provenance),
        topic_id="minimum_wage", proposition_id="prop_minimum_wage", stance="pro",
        form="staar", task_demand=3),
    StimulusRecord(
        id="ACC-W910-ARG-SINGLE-MINIMUM-WAGE-CON",
        grade="9-10", mode="argument", family="single", bucket="test",
        modeling_anchor=rec.modeling_anchor,
        acc_tags=list(rec.acc_tags),
        prompt="Read this source arguing against the proposal.",
        passages=[Passage(title=rec.passages[1].title, angle=rec.passages[1].angle, text=rec.passages[1].text)],
        fact_sources=list(rec.fact_sources),
        provenance=dict(rec.provenance),
        topic_id="minimum_wage", proposition_id="prop_minimum_wage", stance="con",
        form="staar", task_demand=3),
]

if __name__ == "__main__":
    import re
    import readability_gate as rg
    qc_stimulus(rec)
    print(qc_report(rec))
    for p in rec.passages:
        wc = len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", p.text))
        lex = rg.analyze_text(p.text)["lexile_estimate"]
        print(f"  passage '{p.title[:40]}': {wc} words, ~{lex}L")
    print("-> PASS" if rec.qc["passed"] else "-> FAIL")
    # decomposed stance singles
    assert len(SINGLES) == 2 and {x.stance for x in SINGLES} == {"pro", "con"}
    for _x in SINGLES:
        assert _x.family == "single" and _x.bucket == "test" and _x.proposition_id and _x.topic_id and _x.form
        qc_stimulus(_x)
        assert _x.qc["passed"], f"single {_x.id} must pass QC: {_x.qc.get('first_failure')}"
    print("SINGLES decomposition OK")
    sys.exit(0 if rec.qc["passed"] else 1)
