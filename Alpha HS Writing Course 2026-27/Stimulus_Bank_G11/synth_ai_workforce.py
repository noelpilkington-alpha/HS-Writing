"""
G11 SYNTHESIS SOURCE SET for the writing test bank (NEW multi-source shape, family="synthesis_set").
Debatable question: How will artificial intelligence reshape the American workforce?
Four sources on one debatable question (SBAC 4-source / AP Lang synthesis model): three ~480-word
text sources plus one source that DESCRIBES a chart in words (visual/quantitative, exempt from the
480-word floor). Register is pinned to the G11 Lexile band (1120-1300L). Every numeric figure in the
prose traces to a real fetched federal page (US BLS, US NSF, US GAO, US Census Bureau), verified live
2026-07-09. Family=synthesis_set, mode=explanatory. Runs itself through the QC harness and reports.
No em dashes in prose.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# --- Source 1: US BLS -- the federal employment forecast ---------------------------------------
SOURCE_BLS = (
"How will artificial intelligence reshape the American workforce? A useful place to start is the "
"federal government's own forecast of where jobs are headed. The U.S. Bureau of Labor Statistics "
"projects that total employment across all occupations will grow about 3.1 percent between 2024 and "
"2034, adding roughly 5.2 million jobs to the economy. That is steady, unremarkable growth. Hidden "
"inside that broad average, however, are far sharper movements in the very occupations that build and "
"use artificial intelligence.\n\n"

"The clearest example is the job of data scientist. The Bureau projects that this occupation will grow "
"about 33.5 percent from 2024 to 2034, expanding from roughly 245,900 workers to about 328,300. That "
"rate is more than ten times the average for all jobs. A closely related field, computer and "
"information research scientists, is projected to grow about 19.7 percent over the same decade. These "
"are the workers who design the systems that many people fear will replace them, and demand for their "
"skills is rising quickly rather than falling.\n\n"

"This pattern points to an important idea about technology and work. New tools rarely erase jobs evenly "
"across the economy. Instead, they raise the value of some kinds of work while lowering the value of "
"others. Artificial intelligence appears to be following that familiar path. It is increasing demand "
"for people who can build, train, and manage intelligent systems, even as it threatens to automate "
"tasks that were once done by hand or by simpler software. The same tool can be a threat to one worker "
"and an opportunity to another, depending on what that worker does all day.\n\n"

"The size of an occupation matters as much as its growth rate. The occupations growing fastest in "
"percentage terms are often small to begin with, so a large percentage increase may add relatively few "
"jobs overall. A field that doubles from a small base still employs few people. Meanwhile, much larger "
"occupations may grow slowly yet still add many more positions in raw numbers. A modest percentage rise "
"in a giant field can outweigh a huge percentage rise in a tiny one. For that reason, the Bureau warns "
"against reading any single growth rate as the whole story.\n\n"

"Judging how artificial intelligence will change the workforce, then, requires looking past headline "
"numbers. It requires asking not only which jobs grow fastest, but which grow most in size, and which "
"quietly shrink as machines take over the routine parts of the work. The federal projections do not "
"predict a jobless future. They predict a reshaped one, in which the demand for human skill moves "
"toward the tasks that machines still cannot do well. The hard part is preparing workers to move with "
"it, since the jobs that grow and the jobs that fade are rarely held by the same people. That gap "
"between the winners and the losers of automation, more than the total number of jobs, is what will "
"decide whether the coming change feels like progress or like loss."
)

# --- Source 2: US NSF -- the size and growth of the STEM workforce -----------------------------
SOURCE_NSF = (
"If artificial intelligence rewards some skills over others, one question grows urgent. How many "
"American workers already hold jobs in the technical fields where those skills matter most? The "
"National Science Foundation offers a careful count. In its Science and Engineering Indicators report, "
"the Foundation estimates that the science, technology, engineering, and math workforce included about "
"36.8 million workers in 2021. That figure came to roughly 24 percent of all employed people in the "
"United States. Nearly one in four American workers, in other words, already held a STEM job.\n\n"

"That share has been climbing steadily. The Foundation reports that the share of workers in STEM "
"occupations rose from 22 percent in 2011 to 24 percent in 2021. A two-point gain may sound small. But "
"across the entire American workforce, it stands for millions of new technical jobs added in a single "
"decade. The trend runs in the same direction as the job forecasts for data scientists and computer "
"research scientists. The part of the economy that builds and uses advanced technology has been "
"growing, not shrinking.\n\n"

"The Foundation defines this workforce broadly. It counts not only workers who hold advanced degrees. "
"It also counts a large skilled technical workforce whose members use science and engineering knowledge "
"without a four-year degree. Electricians, technicians, and machinists all belong to it. This matters "
"for the debate over artificial intelligence. It shows that technical work is not limited to a small "
"group of programmers. It reaches deep into the middle of the job market, into work that pays well and "
"does not always require college.\n\n"

"These numbers reframe the usual fear about automation. Suppose artificial intelligence mainly raises "
"demand for technical skill. Then the country's economic future depends heavily on how many workers can "
"gain that skill. A large and growing STEM workforce is a real strength. Yet the same data raise a "
"harder question. If nearly a quarter of workers already hold STEM jobs, what happens to the other "
"three-quarters? Their work may be more exposed to automation and less likely to be lifted by it. The "
"Foundation's numbers describe an opportunity. They also mark a divide that policy will have to address "
"if the gains from new technology are to be shared widely, rather than flowing to those who already "
"hold the most technical jobs.\n\n"

"There is a second lesson buried in the count. A STEM job today is not a fixed thing. The tools that a "
"data analyst or a lab technician uses change every few years, and workers must keep learning to keep "
"pace. Artificial intelligence speeds up that churn. It can take over the routine parts of even a "
"technical job, pushing the worker toward tasks that call for judgment. So the size of the STEM "
"workforce is only half the picture. The other half is whether those workers can keep adapting as their "
"own tools are automated. A large workforce that cannot adapt is not the same as a resilient one."
)

# --- Source 3: US GAO -- the limits of what the data can tell us -------------------------------
SOURCE_GAO = (
"Forecasts of a workforce transformed by artificial intelligence share a quiet weakness. They rest on "
"data that may not be good enough to trust. That was the central finding of a study by the U.S. "
"Government Accountability Office, the investigative arm of Congress. The office examined how advanced "
"technologies were already changing American jobs. Its conclusion was humbling. The country does not "
"collect the kind of information that would let anyone say, with confidence, how many jobs automation "
"creates, destroys, or simply reshapes.\n\n"

"The office studied employment patterns from 2010 to 2016. This was a period when automation was "
"spreading through many industries. It found something that cuts against the common fear. As a group, "
"the occupations most exposed to automation did not suffer meaningfully higher job losses during those "
"years. Some workers were displaced. Others were moved into new roles. Some employers actually added "
"workers. The effect was mixed, not a simple wave of destruction. To see how uneven the change could "
"be, investigators visited firms that used the new tools. At one medical center, mobile robots "
"eliminated 17 positions, and the workers who held them were shifted to other jobs.\n\n"

"The larger point was about the missing data, not any single example. Federal statistics were not built "
"to trace the effect of one technology on one job. They can show that an occupation grew or shrank. They "
"cannot reliably show why. Automation and ordinary economic change often happen at the same time. When "
"they do, existing data cannot separate one cause from the other. The office concluded that better "
"information was needed. Only then could the nation plan wisely for the effects of advanced technology "
"on work.\n\n"

"This finding deserves weight in any debate about artificial intelligence. Confident predictions, in "
"either direction, often rest on thinner evidence than they appear to. Some claim that machines will "
"soon erase millions of jobs. Others claim that technology always creates more jobs than it destroys. "
"Both claims run ahead of what the data can actually support. The honest position, the office suggests, "
"is caution. Artificial intelligence may well transform the workforce. But the country still lacks the "
"measuring tools it would need to track that change as it happens. Building those tools, the office "
"argues, may matter as much as any single prediction about the future of work.\n\n"

"There is a practical reason this matters now. Policies meant to help displaced workers depend on "
"knowing who is being displaced, and where, and how fast. If the data arrive years late, the help "
"arrives late too. Better measurement is not a mere academic wish. It is the difference between "
"responding to a change while it can still be shaped and reacting to it only after the damage is done. "
"Uncertainty, in this case, is not a reason to do nothing. It is a reason to measure better, and to "
"measure sooner, so that the country is not left guessing about a change it can already feel taking hold."
)

# --- Source 4: US Census Bureau -- DESCRIBED CHART (visual/quantitative), exempt from word floor
SOURCE_CENSUS_CHART = (
"The chart below, built from U.S. Census Bureau data, shows how the number of workers in STEM "
"occupations has changed over recent decades, alongside their share of the entire workforce. It "
"combines two measures. Vertical bars represent the count of STEM workers in millions, while a line "
"plotted above them represents STEM employment as a percentage of all occupations.\n\n"
"According to the Census Bureau, about 10.8 million workers held STEM occupations in 2019. That came to "
"nearly 7 percent of all U.S. occupations under the Bureau's narrower definition. The line climbs "
"across the decades, and one series is especially striking. The share of STEM workers who are women "
"rose from 8 percent in 1970 to 27 percent in 2019, even as the overall STEM workforce continued to "
"expand.\n\n"
"Interpreted with care, the chart advances two conclusions at once. The rising bars show that technical "
"employment has grown in absolute size. The ascending line shows that it has also grown as a share of "
"total employment. A careful reader should nonetheless resist a frequent error. Because the Census "
"Bureau and the National Science Foundation define STEM differently, their totals diverge. The figures "
"on this chart should therefore be compared with one another, not combined with counts drawn from a "
"different definition."
)

REC = StimulusRecord(
    id="ACC-W910-SYNTH-SET-0002",
    grade="11", mode="explanatory", family="synthesis_set",
    bucket="test", form="4trait", annotated=False,
    modeling_anchor="SBAC G11 full-write / AP Lang synthesis",
    acc_tags=["ACC.W.SRC.1", "ACC.W.INFO.2", "CCSS.W.11-12.7", "CCSS.W.11-12.8"],
    topic_id="ai_workforce_synthesis",
    prompt=("These four sources address one debatable question: how will artificial intelligence reshape "
            "the American workforce? Drawing on at least three of the sources, write an essay that "
            "explains and defends your own analysis of how the workforce is likely to change. Synthesize "
            "the sources to build your explanation rather than summarizing them one by one, and cite each "
            "source you use."),
    passages=[
        Passage(title="What the Job Forecasts Show",
                angle="federal employment projections (US BLS)", text=SOURCE_BLS),
        Passage(title="How Big Is the Technical Workforce?",
                angle="size and growth of the STEM workforce (US NSF)", text=SOURCE_NSF),
        Passage(title="What the Data Cannot Yet Tell Us",
                angle="limits of available evidence, congressional watchdog (US GAO)", text=SOURCE_GAO),
        Passage(title="STEM Employment Over Time",
                angle="visual quantitative (chart): STEM workers and their share of jobs (US Census Bureau)",
                text=SOURCE_CENSUS_CHART),
    ],
    fact_sources=[
        FactSource("Total US employment growth, all occupations, 2024 to 2034", "3.1 percent / 5.2 million",
                   "US BLS", "https://data.bls.gov/projections/occupationProj",
                   "Total, all occupations ... 3.1 percent ... 5,211.8 thousand"),
        FactSource("Data scientist employment growth, 2024 to 2034", "33.5 percent", "US BLS",
                   "https://data.bls.gov/projections/occupationProj",
                   "Data scientists 33.5% (245.9 to 328.3 thousand)"),
        FactSource("Data scientist employment, base and projected (thousands)", "245,900 to 328,300",
                   "US BLS", "https://data.bls.gov/projections/occupationProj",
                   "Data scientists ... 245.9 ... 328.3"),
        FactSource("Computer and information research scientists growth, 2024 to 2034", "19.7 percent",
                   "US BLS", "https://data.bls.gov/projections/occupationProj",
                   "Computer and information research scientists 19.7%"),
        FactSource("STEM workforce size, 2021", "36.8 million", "US NSF",
                   "https://ncses.nsf.gov/pubs/nsb20245",
                   "the STEM workforce had 36.8 million workers"),
        FactSource("STEM share of all US workers, 2021", "24 percent", "US NSF",
                   "https://ncses.nsf.gov/pubs/nsb20245",
                   "which represented 24% of all U.S. workers in 2021"),
        FactSource("STEM occupation share rose, 2011 to 2021", "22 percent to 24 percent", "US NSF",
                   "https://ncses.nsf.gov/pubs/nsb20245",
                   "the percentage of workers in STEM occupations increased from 22% to 24%"),
        FactSource("Automation study period", "2010 to 2016", "US GAO",
                   "https://www.gao.gov/products/gao-19-257", "from 2010 to 2016"),
        FactSource("Positions eliminated by mobile robots at a medical center", "17 positions", "US GAO",
                   "https://www.gao.gov/products/gao-19-257",
                   "eliminated 17 positions and shifted workers to other positions"),
        FactSource("STEM workers, Census Bureau count, 2019", "10.8 million", "US Census Bureau",
                   "https://www.census.gov/library/stories/2021/01/women-making-gains-in-stem-occupations-but-still-underrepresented.html",
                   "there were nearly 10.8 million workers in STEM occupations"),
        FactSource("STEM share of all US occupations (Census definition)", "7 percent", "US Census Bureau",
                   "https://www.census.gov/library/stories/2021/01/women-making-gains-in-stem-occupations-but-still-underrepresented.html",
                   "STEM occupations account for nearly 7% of all U.S. occupations"),
        FactSource("Women's share of STEM workers, 1970 to 2019", "8 percent to 27 percent",
                   "US Census Bureau",
                   "https://www.census.gov/library/stories/2021/01/women-making-gains-in-stem-occupations-but-still-underrepresented.html",
                   "from 8% of STEM workers in 1970 to 27% in 2019"),
    ],
    provenance={"copyright": "own_authored",
                "rights": "public-domain-sourced (US federal)",
                "authored": "2026-07-09"},
)

qc = qc_stimulus(REC)
print(qc_report(REC))
import sys
sys.exit(0 if qc["passed"] else 1)
