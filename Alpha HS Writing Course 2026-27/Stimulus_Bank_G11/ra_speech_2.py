"""
Second G11 RHETORICAL-ANALYSIS stimulus for the test bank (AP Lang Q2 shape).

RHETORICAL ANALYSIS needs a REAL author's choices to analyze, so the passage is a VERBATIM
PUBLIC-DOMAIN text (an excerpt), NOT own-authored prose.

TEXT: William Jennings Bryan, "Cross of Gold" speech, delivered July 9, 1896, to the Democratic
National Convention in Chicago, arguing for the free coinage of silver against the gold standard.
Excerpt = the central movement (the redefinition of "a business man," the pioneer passage, the
Jackson allusion, and the defense of the party platform).

PUBLIC-DOMAIN JUSTIFICATION: the speech was delivered in 1896 and published soon after, far
earlier than 1929, so the text is unambiguously in the US public domain. No third-party
copyrighted expression is used; the excerpt is the speaker's own words, reproduced verbatim.

SOURCE FETCHED: Wikisource (a public-domain text repository), verbatim, on 2026-07-09.

Family=single, mode=analysis, grade=11. Runs itself through the QC harness and reports each gate.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# HEADNOTE (given to the student, AP Lang style): William Jennings Bryan delivered the "Cross
# of Gold" speech on July 9, 1896, to the Democratic National Convention in Chicago. Speaking to
# a divided audience of party delegates, he defended the free coinage of silver against the gold
# standard and sought to win the convention to the cause of the common working American.
# VERBATIM public-domain excerpt (real author's words, unaltered). The passage may keep the source's
# original em dashes; this module's own prose (docstring, comments, prompt) uses none.
PASSAGE = (
"We say to you that you have made the definition of a business man too limited in its application. The man who is "
"employed for wages is as much a business man as his employer; the attorney in a country town is as much a "
"business man as the corporation counsel in a great metropolis; the merchant at the cross-roads store is as much "
"a business man as the merchant of New York; the farmer who goes forth in the morning and toils all day—who "
"begins in the spring and toils all summer—and who by the application of brain and muscle to the natural "
"resources of the country creates wealth, is as much a business man as the man who goes upon the board of trade "
"and bets upon the price of grain; the miners who go down a thousand feet into the earth, or climb two thousand "
"feet upon the cliffs, and bring forth from their hiding places the precious metals to be poured into the "
"channels of trade are as much business men as the few financial magnates who, in a back room, corner the money "
"of the world. We come to speak of this broader class of business men. Ah, my friends, we say not one word "
"against those who live upon the Atlantic coast, but the hardy pioneers who have braved all the dangers of the "
"wilderness, who have made the desert to blossom as the rose—the pioneers away out there [pointing to the West], "
"who rear their children near to Nature's heart, where they can mingle their voices with the voices of the "
"birds—out there where they have erected schoolhouses for the education of their young, churches where they "
"praise their Creator, and cemeteries where rest the ashes of their dead—these people, we say, are as deserving "
"of the consideration of our party as any people in this country. It is for these that we speak. We do not come "
"as aggressors. Our war is not a war of conquest; we are fighting in the defence of our homes, our families, and "
"posterity. We have petitioned, and our petitions have been scorned; we have entreated, and our entreaties have "
"been disregarded; we have begged, and they have mocked when our calamity came. We beg no longer; we entreat no "
"more; we petition no more. We defy them! The gentleman from Wisconsin has said that he fears a Robespierre. My "
"friends, in this land of the free you need not fear that a tyrant will spring up from among the people. What we "
"need is an Andrew Jackson to stand, as Jackson stood, against the encroachments of organized wealth. They tell "
"us that this platform was made to catch votes. We reply to them that changing conditions make new issues; that "
"the principles upon which Democracy rests are as everlasting as the hills, but that they must be applied to new "
"conditions as they arise. Conditions have arisen, and we are here to meet those conditions. They tell us that "
"the income tax ought not to be brought in here; that it is a new idea. They criticise us for our criticism of "
"the Supreme Court of the United States. My friends, we have not criticised; we have simply called attention to "
"what you already know. If you want criticisms, read the dissenting opinions of the court. There you will find "
"criticisms. They say that we passed an unconstitutional law; we deny it. The income tax law was not "
"unconstitutional when it was passed; it was not unconstitutional when it went before the Supreme Court for the "
"first time; it did not become unconstitutional until one of the judges changed his mind, and we cannot be "
"expected to know when a judge will change his mind. The income tax is just. It simply intends to put the burdens "
"of government justly upon the backs of the people. I am in favor of an income tax. When I find a man who is not "
"willing to bear his share of the burdens of the government which protects him, I find a man who is unworthy to "
"enjoy the blessings of a government like ours."
)

SOURCE_URL = "https://en.wikisource.org/wiki/Cross_of_Gold_Speech"

REC = StimulusRecord(
    id="ACC-W910-RA-SINGLE-0002",
    grade="11", mode="analysis", family="single",
    modeling_anchor="AP Lang rhetorical analysis",
    acc_tags=["ACC.W.INFO.6", "ACC.W.SRC.3", "CCSS.W.11-12.9"],
    bucket="test", form="ap", annotated=False,
    topic_id="bryan_cross_of_gold_1896",
    prompt=("Read the following excerpt from William Jennings Bryan's \"Cross of Gold\" speech, delivered July "
            "9, 1896, to the Democratic National Convention in Chicago, where he defended the free coinage of "
            "silver before a divided audience of party delegates. Write an essay in which you analyze the "
            "rhetorical choices Bryan makes to persuade the convention to side with the common working "
            "American. Focus on the writer's choices (such as his appeals, repetition, parallelism, and "
            "definitions), not merely on his ideas, and support your analysis with specific evidence from the "
            "text."),
    passages=[Passage(
        title="From the \"Cross of Gold\" Speech (1896)",
        text=PASSAGE,
        angle="verbatim public-domain source text for rhetorical analysis")],
    # For a PD verbatim text these rows DOCUMENT THE SOURCE (author/work/year + fetched URL + PD status),
    # not authored facts. The contract skips figure-backing for public_domain but still requires the PD
    # source to be documented (a fact_sources row with the fetched http(s) URL).
    fact_sources=[
        FactSource("Speaker, work, and occasion of the source text",
                   "William Jennings Bryan, Cross of Gold speech, July 9, 1896",
                   "Wikisource (public-domain text repository)",
                   SOURCE_URL,
                   "We come to speak of this broader class of business men."),
        FactSource("Public-domain status of the text",
                   "delivered and published 1896; pre-1929 => US public domain",
                   "US public domain (pre-1929)",
                   SOURCE_URL,
                   "We say to you that you have made the definition of a business man too limited"),
        FactSource("Historical occasion (teacher context, not part of the student prompt)",
                   "Democratic National Convention, Chicago, 1896 (free-silver debate)",
                   "Wikisource (public-domain text repository)",
                   SOURCE_URL,
                   "We beg no longer; we entreat no more; we petition no more. We defy them!"),
    ],
    provenance={
        "copyright": "public_domain",
        "rights": "US public domain (pre-1929)",
        "source": ("William Jennings Bryan, \"Cross of Gold\" speech, delivered July 9, 1896, to the Democratic "
                   "National Convention, Chicago. Fetched verbatim from Wikisource (public-domain text repository): "
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
