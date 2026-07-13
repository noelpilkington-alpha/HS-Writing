"""
First G11 RHETORICAL-ANALYSIS stimulus for the test bank (AP Lang Q2 shape).

RHETORICAL ANALYSIS needs a REAL author's choices to analyze, so the passage is a VERBATIM
PUBLIC-DOMAIN text (an excerpt), NOT own-authored prose.

TEXT: Franklin D. Roosevelt, First Inaugural Address, delivered March 4, 1933, from the east
front of the United States Capitol at the depth of the Great Depression. Excerpt = the opening
movement ("This is a day of national consecration ... put people to work.").

PUBLIC-DOMAIN JUSTIFICATION: the address was delivered by the President of the United States in
his official capacity, so it is a work of the United States Government. Under 17 USC 105, works
prepared by a federal officer as part of official duties carry no copyright and are in the US
public domain. No third-party copyrighted expression is used; the excerpt is the speaker's own
words, reproduced verbatim.

SOURCE FETCHED: Wikisource (a public-domain text repository), verbatim, on 2026-07-09.

Family=single, mode=analysis, grade=11. Runs itself through the QC harness and reports each gate.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# HEADNOTE (given to the student, AP Lang style): Franklin D. Roosevelt delivered his First
# Inaugural Address on March 4, 1933, as he took office during the worst year of the Great
# Depression. Speaking to a fearful national audience of citizens (and to Congress), he sought
# to restore public confidence and to justify vigorous federal action.
# VERBATIM public-domain excerpt (real author's words, unaltered). The passage may keep the source's
# original em dashes; this module's own prose (docstring, comments, prompt) uses none.
PASSAGE = (
"This is a day of national consecration, and I am certain that my fellow Americans expect that on my induction "
"into the Presidency I will address them with a candor and a decision which the present situation of our people "
"impels. This is preeminently the time to speak the truth, the whole truth, frankly and boldly. Nor need we "
"shrink from honestly facing conditions in our country today. This great Nation will endure as it has endured, "
"will revive and will prosper. So, first of all, let me assert my firm belief that the only thing we have to fear "
"is fear itself—nameless, unreasoning, unjustified terror which paralyzes needed efforts to convert retreat into "
"advance. In every dark hour of our national life a leadership of frankness and vigor has met with that "
"understanding and support of the people themselves which is essential to victory. I am convinced that you will "
"again give that support to leadership in these critical days. In such a spirit on my part and on yours we face "
"our common difficulties. They concern, thank God, only material things. Values have shrunken to fantastic "
"levels; taxes have risen; our ability to pay has fallen; government of all kinds is faced by serious curtailment "
"of income; the means of exchange are frozen in the currents of trade; the withered leaves of industrial "
"enterprise lie on every side; farmers find no markets for their produce; the savings of many years in thousands "
"of families are gone. More important, a host of unemployed citizens face the grim problem of existence, and an "
"equally great number toil with little return. Only a foolish optimist can deny the dark realities of the moment. "
"Yet our distress comes from no failure of substance. We are stricken by no plague of locusts. Compared with the "
"perils which our forefathers conquered because they believed and were not afraid we have still much to be "
"thankful for. Nature still offers her bounty and human efforts have multiplied it. Plenty is at our doorstep, "
"but a generous use of it languishes in the very sight of the supply. Primarily this is because rulers of the "
"exchange of mankind's goods have failed through their own stubbornness and their own incompetence, have admitted "
"their failure, and have abdicated. Practices of the unscrupulous money changers stand indicted in the court of "
"public opinion, rejected by the hearts and minds of men. True they have tried, but their efforts have been cast "
"in the pattern of an outworn tradition. Faced by failure of credit they have proposed only the lending of more "
"money. Stripped of the lure of profit by which to induce our people to follow their false leadership, they have "
"resorted to exhortations, pleading tearfully for restored confidence. They know only the rules of a generation "
"of self-seekers. They have no vision, and when there is no vision the people perish. The money changers have "
"fled from their high seats in the temple of our civilization. We may now restore that temple to the ancient "
"truths. The measure of the restoration lies in the extent to which we apply social values more noble than mere "
"monetary profit. Happiness lies not in the mere possession of money; it lies in the joy of achievement, in the "
"thrill of creative effort. The joy and moral stimulation of work no longer must be forgotten in the mad chase of "
"evanescent profits. These dark days will be worth all they cost us if they teach us that our true destiny is not "
"to be ministered unto but to minister to ourselves and to our fellow men. Recognition of the falsity of material "
"wealth as the standard of success goes hand in hand with the abandonment of the false belief that public office "
"and high political position are to be valued only by the standards of pride of place and personal profit; and "
"there must be an end to a conduct in banking and in business which too often has given to a sacred trust the "
"likeness of callous and selfish wrongdoing. Small wonder that confidence languishes, for it thrives only on "
"honesty, on honor, on the sacredness of obligations, on faithful protection, on unselfish performance; without "
"them it cannot live. Restoration calls, however, not for changes in ethics alone. This Nation asks for action, "
"and action now. Our greatest primary task is to put people to work."
)

SOURCE_URL = "https://en.wikisource.org/wiki/Franklin_D._Roosevelt%27s_First_Inaugural_Address"

REC = StimulusRecord(
    id="ACC-W910-RA-SINGLE-0001",
    grade="11", mode="analysis", family="single",
    modeling_anchor="AP Lang rhetorical analysis",
    acc_tags=["ACC.W.INFO.6", "ACC.W.SRC.3", "CCSS.W.11-12.9"],
    bucket="test", form="ap", annotated=False,
    topic_id="fdr_first_inaugural_1933",
    prompt=("Read the following excerpt from Franklin D. Roosevelt's First Inaugural Address, delivered March "
            "4, 1933, at the depth of the Great Depression to an anxious national audience. Write an essay in "
            "which you analyze the rhetorical choices Roosevelt makes to restore his listeners' confidence "
            "and to prepare them to accept vigorous action. Focus on the writer's choices (such as his "
            "appeals, figurative language, repetition, and structure), not merely on his ideas, and support "
            "your analysis with specific evidence from the text."),
    passages=[Passage(
        title="From the First Inaugural Address (1933)",
        text=PASSAGE,
        angle="verbatim public-domain source text for rhetorical analysis")],
    # For a PD verbatim text these rows DOCUMENT THE SOURCE (author/work/year + fetched URL + PD status),
    # not authored facts. The contract skips figure-backing for public_domain but still requires the PD
    # source to be documented (a fact_sources row with the fetched http(s) URL).
    fact_sources=[
        FactSource("Speaker, work, and occasion of the source text",
                   "Franklin D. Roosevelt, First Inaugural Address, March 4, 1933",
                   "Wikisource (public-domain text repository)",
                   SOURCE_URL,
                   "the only thing we have to fear is fear itself"),
        FactSource("Public-domain status of the text",
                   "work of the US Government (17 USC 105); no copyright",
                   "US public domain (federal work)",
                   SOURCE_URL,
                   "This is a day of national consecration"),
        FactSource("Historical occasion (teacher context, not part of the student prompt)",
                   "delivered at the depth of the Great Depression, US Capitol",
                   "Wikisource (public-domain text repository)",
                   SOURCE_URL,
                   "Our greatest primary task is to put people to work."),
    ],
    provenance={
        "copyright": "public_domain",
        "rights": "US public domain (work of the US Government, 17 USC 105)",
        "source": ("Franklin D. Roosevelt, First Inaugural Address, delivered March 4, 1933, at the United States "
                   "Capitol. Fetched verbatim from Wikisource (public-domain text repository): "
                   + SOURCE_URL),
        "verbatim": True,
        "fetched": "2026-07-09",
    },
)

if __name__ == "__main__":
    qc = qc_stimulus(REC)
    print(qc_report(REC))
    import sys
    sys.exit(0 if qc["passed"] else 1)
