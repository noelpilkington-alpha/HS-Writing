"""
Opposing-pair ARGUMENT stimulus for the G9 (English I band) writing TEST bank.
Topic: Should the voting age be lowered to 16?  family=opposing, mode=argument, bucket=test.
TWO original G9-register passages (~500-620 words each, targeted 1010-1150L), one pro and one con, each
conceding the other side. >=2 distinct source orgs for credibility contrast:
  PRO side  (history of change / civic habit):   US National Archives (26th Amendment record).
  CON side  (turnout gap / readiness):            US Census Bureau (voting-by-age data).
Every numeric figure in prose traces to a federal page fetched live 2026-07-08. No em/en dashes in prose.
Runs itself through the QC harness and exits on the verdict.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# ---------------------------------------------------------------------------
# PASSAGE A  -  pro-lowering (US National Archives: the 26th Amendment precedent)
# ---------------------------------------------------------------------------
PASSAGE_A = (
"The voting age in the United States has not always been 18. For most of the country's history, it was "
"21. That changed only about fifty years ago. The National Archives records that the 26th Amendment was "
"ratified on July 1, 1971. Congress had passed it just months earlier, on March 23, 1971. The amendment "
"says the right to vote shall not be denied to citizens who are 18 or older on account of age. "
"Supporters of a lower age point to this history. If the country could lower the age once, they argue, "
"it can do so again.\n\n"

"The change in 1971 had a clear reason behind it. Young men could be drafted to fight at 18, yet they "
"could not vote. Many people felt that gap was unfair. The slogan of the day was simple: old enough to "
"fight, old enough to vote. Supporters of a 16 age say a similar unfairness exists now. A 16-year-old "
"can work a real job and pay taxes on what they earn. Yet they have no voice in how that tax money is "
"spent. To supporters, that gap looks just as unfair as the old one.\n\n"

"There is also a case built on habit. Studies of voting show that people who vote early tend to keep "
"voting for life. Voting, in other words, is a habit that forms young. A 16-year-old usually lives at "
"home and attends school. That setting is steady and supportive. Supporters argue it is the ideal time "
"to cast a first ballot. A student could learn about the issues in class, then vote with family nearby. "
"A first vote at 18 often comes during a move to college or a job, a far less settled moment.\n\n"

"Supporters add that teenagers have a real stake in public choices. Decisions about schools, climate, "
"and the future will shape their lives the longest. Yet they have no say in those decisions. A young "
"person who marches or speaks out still cannot vote on the very issues they care about most. Giving "
"them a ballot, supporters argue, would tie their strong feelings to real civic power. It would also "
"send a message that their voices count in the country they will one day lead.\n\n"

"Some other places have already tried this step. A few nations and even a handful of local towns now "
"let 16-year-olds vote in certain elections. Supporters point to these examples as proof that the idea "
"can work in practice. Where young people have been given the vote, they note, the sky did not fall. "
"Instead, some studies found that these young voters turned out at healthy rates.\n\n"

"Supporters do not claim every 16-year-old is ready. They agree that some teenagers know little about "
"politics and may not vote with care. But they point out that the same is true of many adults. We do "
"not test grown voters for knowledge, and we should not test teenagers either. The country once judged "
"18-year-olds too young, then decided otherwise, and the republic held firm. Supporters believe the "
"nation could take that step again. Lowering the age to 16, in their view, would welcome young people "
"into public life at the very moment they are learning what it means to be a citizen."
)

# ---------------------------------------------------------------------------
# PASSAGE B  -  against lowering (US Census Bureau: the young-voter turnout gap)
# ---------------------------------------------------------------------------
PASSAGE_B = (
"Young people clearly care about the future, and that energy deserves respect. But caring about an "
"issue is not the same as being ready to vote on it. Critics of lowering the voting age to 16 argue "
"that the country should be careful. The evidence we already have, they say, points the other way.\n\n"

"Look first at how younger citizens vote now. The U.S. Census Bureau reports that in the 2020 election, "
"about 57 percent of citizens ages 18 to 34 voted. Among citizens 65 and older, turnout reached about "
"74 percent. The national rate across all adults was about 67 percent. So the youngest group of voters "
"already turns out at the lowest rate. Critics argue this is a warning sign. If many young adults skip "
"elections, adding even younger voters may not strengthen democracy. It may simply add more names that "
"never appear at the polls.\n\n"

"Critics raise a deeper point about readiness. At 16, most teenagers still live under their parents' "
"roof and follow their parents' rules. The law already treats this age as not fully grown. A "
"16-year-old cannot sign a contract, serve on a jury, or, in most places, drive without limits. Voting "
"is a serious duty that shapes the whole country. Critics ask why we would hand that duty to people the "
"law does not yet treat as adults in other ways.\n\n"

"There is also a worry about influence. A 16-year-old usually lives with parents and depends on them "
"for almost everything. Critics fear that a teenager might simply copy a parent's vote, or feel "
"pressure to vote a certain way at home. An 18-year-old is more likely to live on their own and think "
"for themselves. A vote, critics argue, should reflect the voter's own mind, not an echo of the "
"household. A ballot cast under pressure, they warn, weakens the very idea of a free and secret vote.\n\n"

"Finally, critics point to knowledge. Voting well takes some grasp of history, government, and current "
"events. Many 16-year-olds are still learning these subjects in school. They may not yet have the "
"background to weigh hard choices. Waiting until 18 gives students more time to finish that learning "
"and to see more of the adult world. Those extra two years, critics argue, let a young person test "
"ideas and form views that are truly their own.\n\n"

"Critics of a lower voting age are not against young people or their voice. They agree that teenagers "
"should learn about government and speak out on issues. Their point is narrower. The age of 18 is a "
"reasonable line, drawn where the law treats a person as an adult. Given that young adults already vote "
"least often, critics argue, the wiser path is to help them use the vote they have, not to push the "
"age lower still. Before the country changes a rule this basic, it should ask a fair question. Would "
"lowering the age truly strengthen our democracy, or would it only widen the gap we already see?"
)

FACTS = [
    # ---- PRO side (US National Archives) ----
    FactSource("26th Amendment ratified", "July 1, 1971", "US National Archives",
               "https://www.archives.gov/milestone-documents/26th-amendment",
               "Ratified July 1, 1971"),
    FactSource("26th Amendment passed by Congress", "March 23, 1971", "US National Archives",
               "https://www.archives.gov/milestone-documents/26th-amendment",
               "passed by Congress March 23, 1971"),
    FactSource("26th Amendment set the national voting age at 18", "18", "US National Archives",
               "https://www.archives.gov/milestone-documents/26th-amendment",
               "shall not be denied or abridged by the United States or by any State on account of age"),
    # ---- CON side (US Census Bureau) ----
    FactSource("Turnout of citizens ages 18-34, 2020 election", "57 percent", "US Census Bureau",
               "https://www.census.gov/library/stories/2021/04/record-high-turnout-in-2020-general-election.html",
               "57% voted in 2020, up from 49% in 2016"),
    FactSource("Turnout of citizens 65 and older, 2020 election", "74 percent", "US Census Bureau",
               "https://www.census.gov/library/stories/2021/04/record-high-turnout-in-2020-general-election.html",
               "74% voted in 2020, compared to 71% in 2016"),
    FactSource("National voter turnout, 2020 election", "67 percent", "US Census Bureau",
               "https://www.census.gov/library/stories/2021/04/record-high-turnout-in-2020-general-election.html",
               "national turnout at 67% of citizens 18 and older"),
]

REC = StimulusRecord(
    id="ACC-W910-ARG-OPP-0009",
    grade="9", mode="argument", family="opposing", bucket="test",
    form="ohio", annotated=False,
    topic_id="voting_age_16",
    modeling_anchor="Ohio ELA II / MD MCAP (opposing-view pick-a-side)",
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "CCSS.W.9-10.1"],
    prompt=("Weighing both sources, write an argumentative essay stating your position on whether the "
            "voting age should be lowered to 16. Support your claim with specific evidence from both "
            "sources, and respond to at least one objection from the side you do not take."),
    passages=[
        Passage(title="The Case for Lowering the Voting Age to 16",
                angle="pro-lowering; US National Archives record of the 26th Amendment as precedent",
                text=PASSAGE_A),
        Passage(title="Why 18 Should Stay the Voting Age",
                angle="against lowering the age; US Census Bureau voting-by-age turnout data",
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
