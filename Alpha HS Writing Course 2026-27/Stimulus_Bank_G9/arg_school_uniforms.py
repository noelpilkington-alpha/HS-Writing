"""
Opposing-pair ARGUMENT stimulus for the G9 (English I band) writing TEST bank.
Topic: Should schools require students to wear uniforms?  family=opposing, mode=argument, bucket=test.
TWO original G9-register passages (~500-620 words each, targeted 1010-1150L), one pro and one con, each
conceding the other side. >=2 distinct source orgs for credibility contrast:
  PRO side  (focus / fairness / bullying):  US Dept. of Education / NCES.
  CON side  (cost / freedom / weak case):   US Census Bureau  (+ NCES dress-code context).
Every numeric figure in prose traces to a federal page fetched live 2026-07-08. No em/en dashes in prose.
Runs itself through the QC harness and exits on the verdict.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# ---------------------------------------------------------------------------
# PASSAGE A  -  pro-uniforms (NCES uniform-adoption + bullying data)
# ---------------------------------------------------------------------------
PASSAGE_A = (
"Walk into many American schools today, and you will see students dressed alike. More and more "
"districts now ask students to wear a school uniform. The trend has grown for over twenty years. The "
"National Center for Education Statistics reports that 18.8 percent of public schools required "
"uniforms in the 2019 to 2020 school year. Back in the 1999 to 2000 school year, only 11.8 percent "
"did. That is a large jump in a short time. Supporters say this growth points to a simple idea.\n\n"

"The strongest reason for uniforms is focus. When everyone wears the same clothes, students think less "
"about fashion. They do not compare brands or judge each other by price. A student in a plain shirt "
"looks like everyone else. Supporters believe this frees the mind for learning. The school day becomes "
"about ideas, not outfits. Even small distractions add up over a long day.\n\n"

"Uniforms may also help with a serious problem: bullying. The same federal agency reports that about "
"19 percent of students ages 12 to 18 said they were bullied at school in the 2021 to 2022 school "
"year. That share was down from 28 percent about ten years earlier. Still, nearly one in five students "
"faces bullying. Supporters argue that clothing is often a trigger. A student in old or cheap clothes "
"can become a target. Uniforms hide these differences. When everyone dresses the same, one common "
"reason for cruelty fades.\n\n"

"There is a fairness point here as well. Not every family can afford trendy clothes. A closet full of "
"name brands is out of reach for many students. Uniforms level the field. A wealthy student and a poor "
"student walk in looking the same. No one can tell at a glance who has money and who does not. "
"Supporters say this quiet fairness is worth protecting.\n\n"

"Uniforms can also make a school calmer. Staff can spot a stranger more easily when students share one "
"look. Mornings grow simpler too, because students do not waste time choosing an outfit. Families argue "
"less about clothes before school. A child gets dressed and heads out the door. These small gains add "
"up across a long year. Over many mornings, saved minutes and calmer starts can shape the whole day. A "
"steady routine helps a student arrive ready to think.\n\n"

"Supporters point to school spirit too. A shared look can build a sense of belonging. Students feel "
"like part of one group with a shared purpose. When a class dresses alike, it can feel more like a "
"team than a crowd. That sense of unity, supporters argue, is easy to lose and hard to build.\n\n"

"Supporters do not claim uniforms fix every problem. They know a shirt cannot teach a lesson or stop "
"every unkind word. They agree that students give up some freedom in how they dress. But they argue "
"the trade is fair. A calmer, more equal school helps students learn. If a simple change can ease "
"money pressure, cut a trigger for bullying, and sharpen focus, then supporters believe it is worth "
"making. The goal is not to erase who students are. The goal is to build a place where every student "
"feels equal and ready to work."
)

# ---------------------------------------------------------------------------
# PASSAGE B  -  against a uniform mandate (US Census cost + NCES dress-code context)
# ---------------------------------------------------------------------------
PASSAGE_B = (
"No one wants students to feel judged by their clothes. That worry is real, and uniforms try to answer "
"it. Yet many families and students push back against uniform rules. They argue that the costs and the "
"loss of freedom are too high. A closer look shows the idea is not as simple as it sounds.\n\n"

"Start with money. Uniforms are not free. A family must buy several sets so a child has clean clothes "
"each day. For homes that are already stretched, this is a real burden. The U.S. Census Bureau reports "
"that the official poverty rate was 11.5 percent in 2022. Using a fuller measure that counts costs and "
"aid, child poverty reached 12.4 percent in 2022. That was a sharp rise from just 5.2 percent the year "
"before. Millions of children live in homes where every dollar matters. Asking these families to buy "
"special clothes can add stress they do not need.\n\n"

"Critics also question how well uniforms even work. A school does not have to pick uniforms to set "
"rules about dress. The National Center for Education Statistics reports that 43.7 percent of public "
"schools enforced a strict dress code in the 2019 to 2020 school year. A dress code can ban rude or "
"unsafe clothing without forcing one outfit on everyone. In fact, uniform rules have started to fade. "
"The share of schools requiring uniforms fell from 21.5 percent in the 2015 to 2016 school year to "
"18.8 percent by 2019 to 2020. If uniforms were a clear win, that number would likely be climbing.\n\n"

"Then there is the matter of self-expression. Clothing is one way young people show who they are. A "
"student may reveal culture, mood, or personality through what they wear. Critics argue that a school "
"should teach students to think for themselves. Forcing everyone into the same shirt sends the "
"opposite message. It treats a school like a factory, not a place that values each mind.\n\n"

"There is also a question of respect. When a school hands down a uniform rule, students often have "
"little say. Many feel the rule is about control, not learning. A student who resents a rule may fight "
"it rather than focus. Critics say trust often works better than force. A clear dress code, shaped with "
"student input, can keep order without heavy control.\n\n"

"Critics also doubt the fairness claim. Uniforms may hide brand-name shirts, but they cannot hide "
"everything. Students still notice shoes, backpacks, and phones. A uniform can even create new costs, "
"since a family must buy it on top of regular clothes. So the promise of a level field may be thinner "
"than it looks. The deeper causes of status and cruelty do not vanish when a shirt changes.\n\n"

"Critics of uniforms are not saying clothes never cause problems. They agree that bullying and status "
"battles are real. Their point is narrower. A rule that costs families money, limits free expression, "
"and stirs resentment should not be forced on every school. The choice belongs to each community, "
"weighed with care. Schools can protect fairness and safety in gentler ways. Before a district orders "
"one shirt for all, critics argue, it should ask a fair question. Does this rule truly help students, "
"or does it only make them look the same?"
)

FACTS = [
    # ---- PRO side (NCES) ----
    FactSource("Public schools requiring uniforms, 2019-20", "18.8 percent",
               "US Dept. of Education / NCES",
               "https://nces.ed.gov/fastfacts/display.asp?id=50",
               "18.8 percent of public schools required that students wear uniforms"),
    FactSource("Public schools requiring uniforms, 1999-2000", "11.8 percent",
               "US Dept. of Education / NCES",
               "https://nces.ed.gov/programs/digest/d21/tables/dt21_233.50.asp",
               "Required students to wear uniforms ... 1999-2000 ... 11.8"),
    FactSource("Students ages 12-18 bullied at school, 2021-22", "19 percent",
               "US Dept. of Education / NCES",
               "https://nces.ed.gov/fastfacts/display.asp?id=719",
               "about 19 percent of students ages 12-18 ... reported being bullied ... during school"),
    FactSource("Students ages 12-18 bullied at school, 2010-11", "28 percent",
               "US Dept. of Education / NCES",
               "https://nces.ed.gov/fastfacts/display.asp?id=719",
               "a decline from 2010-11, when 28 percent reported being bullied"),
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
    # ---- CON side context (NCES) ----
    FactSource("Public schools enforcing a strict dress code, 2019-20", "43.7 percent",
               "US Dept. of Education / NCES",
               "https://nces.ed.gov/programs/digest/d21/tables/dt21_233.50.asp",
               "Enforced a strict dress code ... 2019-20 ... 43.7"),
    FactSource("Public schools requiring uniforms, 2015-16", "21.5 percent",
               "US Dept. of Education / NCES",
               "https://nces.ed.gov/programs/digest/d21/tables/dt21_233.50.asp",
               "Required students to wear uniforms ... 2015-16 ... 21.5"),
]

REC = StimulusRecord(
    id="ACC-W910-ARG-OPP-0007",
    grade="9", mode="argument", family="opposing", bucket="test",
    form="ohio", annotated=False,
    topic_id="school_uniforms",
    modeling_anchor="Ohio ELA II / MD MCAP (opposing-view pick-a-side)",
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "CCSS.W.9-10.1"],
    prompt=("Weighing both sources, write an argumentative essay stating your position on whether schools "
            "should require students to wear uniforms. Support your claim with specific evidence from both "
            "sources, and respond to at least one objection from the side you do not take."),
    passages=[
        Passage(title="The Case for School Uniforms",
                angle="pro-uniforms; US Dept. of Education / NCES uniform-adoption and bullying data",
                text=PASSAGE_A),
        Passage(title="Why a Uniform Rule Costs More Than It Seems",
                angle="against a uniform mandate; US Census Bureau cost data plus NCES dress-code context",
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
