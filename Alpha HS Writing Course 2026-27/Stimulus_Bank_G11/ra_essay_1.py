"""
Third G11 RHETORICAL-ANALYSIS stimulus for the test bank (AP Lang Q2 shape), a prose ESSAY.

RHETORICAL ANALYSIS needs a REAL author's choices to analyze, so the passage is a VERBATIM
PUBLIC-DOMAIN text (an excerpt), NOT own-authored prose.

TEXT: Ralph Waldo Emerson, "Self-Reliance," from Essays: First Series (1841). Excerpt = the
central movement on trusting oneself and refusing conformity ("Trust thyself ... if I live wholly
from within?").

PUBLIC-DOMAIN JUSTIFICATION: the essay was published in 1841, far earlier than 1929, so the text
is unambiguously in the US public domain. No third-party copyrighted expression is used; the
excerpt is the author's own words, reproduced verbatim.

SOURCE FETCHED: Wikisource (a public-domain text repository), verbatim, on 2026-07-09.

Family=single, mode=analysis, grade=11. Runs itself through the QC harness and reports each gate.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# HEADNOTE (given to the student, AP Lang style): Ralph Waldo Emerson published "Self-Reliance"
# in Essays: First Series (1841). Writing for a general reading audience of his day, the essayist
# argues that each person should trust an inner voice and resist the pressure to conform to
# society. The passage below comes from the middle of that argument.
# VERBATIM public-domain excerpt (real author's words, unaltered). The passage may keep the source's
# original em dashes; this module's own prose (docstring, comments, prompt) uses none.
PASSAGE = (
"Trust thyself: every heart vibrates to that iron string. Accept the place the divine providence has found for "
"you, the society of your contemporaries, the connection of events. Great men have always done so, and confided "
"themselves childlike to the genius of their age, betraying their perception that the absolutely trustworthy was "
"seated at their heart, working through their hands, predominating in all their being. And we are now men, and "
"must accept in the highest mind the same transcendent destiny; and not minors and invalids in a protected "
"corner, not cowards fleeing before a revolution, but guides, redeemers, and benefactors, obeying the Almighty "
"effort, and advancing on Chaos and the Dark. What pretty oracles nature yields us on this text, in the face and "
"behaviour of children, babes, and even brutes! That divided and rebel mind, that distrust of a sentiment because "
"our arithmetic has computed the strength and means opposed to our purpose, these have not. Their mind being "
"whole, their eye is as yet unconquered, and when we look in their faces, we are disconcerted. Infancy conforms "
"to nobody: all conform to it, so that one babe commonly makes four or five out of the adults who prattle and "
"play to it. So God has armed youth and puberty and manhood no less with its own piquancy and charm, and made it "
"enviable and gracious and its claims not to be put by, if it will stand by itself. Do not think the youth has no "
"force, because he cannot speak to you and me. Hark! in the next room his voice is sufficiently clear and "
"emphatic. It seems he knows how to speak to his contemporaries. Bashful or bold, then, he will know how to make "
"us seniors very unnecessary. The nonchalance of boys who are sure of a dinner, and would disdain as much as a "
"lord to do or say aught to conciliate one, is the healthy attitude of human nature. A boy is in the parlour what "
"the pit is in the playhouse; independent, irresponsible, looking out from his corner on such people and facts as "
"pass by, he tries and sentences them on their merits, in the swift, summary way of boys, as good, bad, "
"interesting, silly, eloquent, troublesome. He cumbers himself never about consequences, about interests: he "
"gives an independent, genuine verdict. You must court him: he does not court you. But the man is, as it were, "
"clapped into jail by his consciousness. As soon as he has once acted or spoken with eclat, he is a committed "
"person, watched by the sympathy or the hatred of hundreds, whose affections must now enter into his account. "
"There is no Lethe for this. Ah, that he could pass again into his neutrality! Who can thus avoid all pledges, "
"and having observed, observe again from the same unaffected, unbiased, unbribable, unaffrighted innocence, must "
"always be formidable. He would utter opinions on all passing affairs, which being seen to be not private, but "
"necessary, would sink like darts into the ear of men, and put them in fear. These are the voices which we hear "
"in solitude, but they grow faint and inaudible as we enter into the world. Society everywhere is in conspiracy "
"against the manhood of every one of its members. Society is a joint-stock company, in which the members agree, "
"for the better securing of his bread to each shareholder, to surrender the liberty and culture of the eater. The "
"virtue in most request is conformity. Self-reliance is its aversion. It loves not realities and creators, but "
"names and customs. Whoso would be a man must be a nonconformist. He who would gather immortal palms must not be "
"hindered by the name of goodness, but must explore if it be goodness. Nothing is at last sacred but the "
"integrity of your own mind. Absolve you to yourself, and you shall have the suffrage of the world. I remember an "
"answer which when quite young I was prompted to make to a valued adviser, who was wont to importune me with the "
"dear old doctrines of the church. On my saying, What have I to do with the sacredness of traditions, if I live "
"wholly from within?"
)

SOURCE_URL = "https://en.wikisource.org/wiki/Essays:_First_Series/Self-Reliance"

REC = StimulusRecord(
    id="ACC-W910-RA-SINGLE-0003",
    grade="11", mode="analysis", family="single",
    modeling_anchor="AP Lang rhetorical analysis",
    acc_tags=["ACC.W.INFO.6", "ACC.W.SRC.3", "CCSS.W.11-12.9"],
    bucket="test", form="ap", annotated=False,
    topic_id="emerson_self_reliance_1841",
    prompt=("Read the following excerpt from Ralph Waldo Emerson's essay \"Self-Reliance,\" published in "
            "Essays: First Series (1841) for a general reading audience. Write an essay in which you analyze "
            "the rhetorical choices Emerson makes to convince his readers to trust themselves and resist "
            "conformity. Focus on the writer's choices (such as his figurative language, analogy, aphorism, "
            "and shifts in tone), not merely on his ideas, and support your analysis with specific evidence "
            "from the text."),
    passages=[Passage(
        title="From \"Self-Reliance\" (1841)",
        text=PASSAGE,
        angle="verbatim public-domain source text for rhetorical analysis")],
    # For a PD verbatim text these rows DOCUMENT THE SOURCE (author/work/year + fetched URL + PD status),
    # not authored facts. The contract skips figure-backing for public_domain but still requires the PD
    # source to be documented (a fact_sources row with the fetched http(s) URL).
    fact_sources=[
        FactSource("Author and work of the source text",
                   "Ralph Waldo Emerson, Self-Reliance, Essays: First Series, 1841",
                   "Wikisource (public-domain text repository)",
                   SOURCE_URL,
                   "Trust thyself: every heart vibrates to that iron string."),
        FactSource("Public-domain status of the text",
                   "published 1841; pre-1929 => US public domain",
                   "US public domain (pre-1929)",
                   SOURCE_URL,
                   "Whoso would be a man must be a nonconformist."),
        FactSource("Central rhetorical figure (teacher context, not part of the student prompt)",
                   "the \"joint-stock company\" analogy for conformist society",
                   "Wikisource (public-domain text repository)",
                   SOURCE_URL,
                   "Society is a joint-stock company"),
    ],
    provenance={
        "copyright": "public_domain",
        "rights": "US public domain (pre-1929)",
        "source": ("Ralph Waldo Emerson, \"Self-Reliance,\" in Essays: First Series (1841). Fetched verbatim from "
                   "Wikisource (public-domain text repository): "
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
