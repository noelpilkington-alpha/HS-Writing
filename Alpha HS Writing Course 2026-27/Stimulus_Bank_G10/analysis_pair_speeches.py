"""
CROSS-TEXT ANALYSIS-mode stimulus for the G10 lesson bank: a PAIR of verbatim public-domain speeches.

WHY THIS EXISTS: the held-out mastery for ACC-W910-L-G10-C1006-0021 ("Write a Cross-Text Analysis
Essay") needs a genuine analysis-mode SOURCE PAIR - two analyzable texts a student can make ONE
analytical claim about, woven across both. The bank had only single-passage analysis sources; a
cross-text analysis task on a single text (or on an argument op-ed pair, the pre-2026-07-16 source) is
a genre mismatch (COURSE_MASTERY17_TRIAGE C1006-0021; caught by mastery_genre_gate + Tier-B Fable).
This record is that missing pair.

CRITICAL (same as the single analysis sources): rhetorical analysis requires REAL authors' choices, so
BOTH passages are VERBATIM PUBLIC-DOMAIN excerpts, not own-authored prose. The two texts are chosen to
share an analyzable craft move - both build a cascade of rhetorical QUESTIONS and PARALLEL clauses to
move an audience from reflection to a demanded response - so a single cross-text claim about that craft
is well-supported from both.

TEXT 1: Patrick Henry, "Speech to the Virginia Convention" (1775), closing movement. Verbatim from the
excerpt already in the bank as ACC-W910-ANALYSIS-SINGLE-0001 (626 words, ~1096L, G10 PASS).
TEXT 2: Frederick Douglass, "What to the Slave Is the Fourth of July?" (1852), the "Fellow-citizens,
pardon me" turn. Verbatim from ACC-W910-ANALYSIS-SINGLE-0004 (611 words, ~1165L, G10 PASS).

Both excerpts are byte-identical to the verified single-source records (same fetched URLs, same PD
justification); only typography was normalized in those originals. NEITHER is taught in C1006-0021 (that
lesson teaches on HOUR + HIGHWAYS), so both are genuinely held-out.

Family=complementary (a 2-passage set), mode=analysis, copyright=public_domain. Runs its own QC.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# ---- TEXT 1: Patrick Henry (1775) - verbatim, identical to ACC-W910-ANALYSIS-SINGLE-0001 ----
HENRY = (
"Shall we try argument? Sir, we have been trying that for the last ten years. Have we anything new to "
"offer upon the subject? Nothing. We have held the subject up in every light of which it is capable; but "
"it has been all in vain. Shall we resort to entreaty and humble supplication? What terms shall we find "
"which have not been already exhausted? Let us not, I beseech you, sir, deceive ourselves. Sir, we have "
"done everything that could be done to avert the storm which is now coming on. We have petitioned; we "
"have remonstrated; we have supplicated; we have prostrated ourselves before the throne, and have implored "
"its interposition to arrest the tyrannical hands of the ministry and Parliament. Our petitions have been "
"slighted; our remonstrances have produced additional violence and insult; our supplications have been "
"disregarded; and we have been spurned, with contempt, from the foot of the throne! In vain, after these "
"things, may we indulge the fond hope of peace and reconciliation. There is no longer any room for hope. "
"If we wish to be free-- if we mean to preserve inviolate those inestimable privileges for which we have "
"been so long contending--if we mean not basely to abandon the noble struggle in which we have been so "
"long engaged, and which we have pledged ourselves never to abandon until the glorious object of our "
"contest shall be obtained--we must fight! I repeat it, sir, we must fight! An appeal to arms and to the "
"God of hosts is all that is left us! They tell us, sir, that we are weak; unable to cope with so "
"formidable an adversary. But when shall we be stronger? Will it be the next week, or the next year? Will "
"it be when we are totally disarmed, and when a British guard shall be stationed in every house? Shall we "
"gather strength by irresolution and inaction? Shall we acquire the means of effectual resistance by lying "
"supinely on our backs and hugging the delusive phantom of hope, until our enemies shall have bound us "
"hand and foot? Sir, we are not weak if we make a proper use of those means which the God of nature hath "
"placed in our power. The millions of people, armed in the holy cause of liberty, and in such a country as "
"that which we possess, are invincible by any force which our enemy can send against us. Besides, sir, we "
"shall not fight our battles alone. There is a just God who presides over the destinies of nations, and "
"who will raise up friends to fight our battles for us. The battle, sir, is not to the strong alone; it is "
"to the vigilant, the active, the brave. Besides, sir, we have no election. If we were base enough to "
"desire it, it is now too late to retire from the contest. There is no retreat but in submission and "
"slavery! Our chains are forged! Their clanking may be heard on the plains of Boston! The war is "
"inevitable--and let it come! I repeat it, sir, let it come. It is in vain, sir, to extenuate the matter. "
"Gentlemen may cry, Peace, Peace-- but there is no peace. The war is actually begun! The next gale that "
"sweeps from the north will bring to our ears the clash of resounding arms! Our brethren are already in "
"the field! Why stand we here idle? What is it that gentlemen wish? What would they have? Is life so dear, "
"or peace so sweet, as to be purchased at the price of chains and slavery? Forbid it, Almighty God! I know "
"not what course others may take; but as for me, give me liberty or give me death!"
)

# ---- TEXT 2: Frederick Douglass (1852) - verbatim, identical to ACC-W910-ANALYSIS-SINGLE-0004 ----
DOUGLASS = (
    "Fellow-citizens, pardon me, allow me to ask, why am I called upon to speak here to-day? What have I, or "
    "those I represent, to do with your national independence? Are the great principles of political freedom and "
    "of natural justice, embodied in that Declaration of Independence, extended to us? and am I, therefore, "
    "called upon to bring our humble offering to the national altar, and to confess the benefits and express "
    "devout gratitude for the blessings resulting from your independence to us? Would to God, both for your sakes "
    "and ours, that an affirmative answer could be truthfully returned to these questions! Then would my task be "
    "light, and my burden easy and delightful. For who is there so cold, that a nation's sympathy could not warm "
    "him? Who so obdurate and dead to the claims of gratitude, that would not thankfully acknowledge such "
    "priceless benefits? Who so stolid and selfish, that would not give his voice to swell the hallelujahs of a "
    "nation's jubilee, when the chains of servitude had been torn from his limbs? I am not that man. In a case "
    "like that, the dumb might eloquently speak, and the \"lame man leap as an hart.\" But, such is not the state "
    "of the case. I say it with a sad sense of the disparity between us. I am not included within the pale of "
    "this glorious anniversary! Your high independence only reveals the immeasurable distance between us. The "
    "blessings in which you, this day, rejoice, are not enjoyed in common.-- The rich inheritance of justice, "
    "liberty, prosperity and independence, bequeathed by your fathers, is shared by you, not by me. The sunlight "
    "that brought life and healing to you, has brought stripes and death to me. This Fourth July is yours, not "
    "mine. You may rejoice, I must mourn. To drag a man in fetters into the grand illuminated temple of liberty, "
    "and call upon him to join you in joyous anthems, were inhuman mockery and sacrilegious irony. Do you mean, "
    "citizens, to mock me, by asking me to speak to-day? If so, there is a parallel to your conduct. And let me "
    "warn you that it is dangerous to copy the example of a nation whose crimes, towering up to heaven, were "
    "thrown down by the breath of the Almighty, burying that nation in irrecoverable ruin! I can to-day take up "
    "the plaintive lament of a peeled and woe-smitten people! \"By the rivers of Babylon, there we sat down. Yea! "
    "we wept when we remembered Zion. We hanged our harps upon the willows in the midst thereof. For there, they "
    "that carried us away captive, required of us a song; and they who wasted us required of us mirth, saying, "
    "Sing us one of the songs of Zion. How can we sing the Lord's song in a strange land? If I forget thee, O "
    "Jerusalem, let my right hand forget her cunning. If I do not remember thee, let my tongue cleave to the roof "
    "of my mouth.\" Fellow-citizens; above your national, tumultuous joy, I hear the mournful wail of millions! "
    "whose chains, heavy and grievous yesterday, are, to-day, rendered more intolerable by the jubilee shouts "
    "that reach them. If I do forget, if I do not faithfully remember those bleeding children of sorrow this day, "
    "\"may my right hand forget her cunning, and may my tongue cleave to the roof of my mouth!\" To forget them, to "
    "pass lightly over their wrongs, and to chime in with the popular theme, would be treason most scandalous and "
    "shocking, and would make me a reproach before God and the world. My subject, then, fellow-citizens, is "
    "American Slavery."
)

HENRY_URL = "https://avalon.law.yale.edu/18th_century/patrick.asp"
DOUGLASS_URL = "https://en.wikisource.org/wiki/What_to_the_Slave_Is_the_Fourth_of_July%3F"
DOUGLASS_SCAN_URL = "https://archive.org/stream/Douglass_July_Oration/ocm30553533_V_0_djvu.txt"

rec = StimulusRecord(
    id="ACC-W910-ANALYSIS-PAIR-0001",
    grade="9-10", mode="analysis", family="complementary",
    modeling_anchor="cross-text rhetorical analysis (AP Lang analysis across two texts / NY Regents-style text-analysis)",
    acc_tags=["ACC.W.INFO.6", "ACC.W.ANALYSIS.1", "CCSS.RI.9-10.6", "CCSS.W.9-10.2", "CCSS.RI.9-10.9"],
    prompt=("Both speakers use a cascade of rhetorical questions and parallel clauses to move an audience. "
            "Analyze how each author uses that craft to move his audience, and make ONE analytical claim "
            "that holds across BOTH texts. Support it with device-effect-warrant evidence woven from both "
            "the Henry and the Douglass excerpt, not one text and then the other."),
    passages=[
        Passage(title="From the Speech to the Virginia Convention (1775)", text=HENRY,
                angle="verbatim public-domain text 1 for cross-text rhetorical analysis (Patrick Henry)"),
        Passage(title="From \"What to the Slave Is the Fourth of July?\" (1852)", text=DOUGLASS,
                angle="verbatim public-domain text 2 for cross-text rhetorical analysis (Frederick Douglass)"),
    ],
    # PD verbatim texts: these rows DOCUMENT each source (author/work/year + fetched URL + PD status),
    # not authored facts. copyright=public_domain, so the contract skips figure-backing but requires a
    # documented source + a fetched http(s) URL.
    fact_sources=[
        FactSource("Speaker and work of text 1",
                   "Patrick Henry, Speech to the Virginia Convention, 1775",
                   "The Avalon Project, Yale Law School (public-domain documents repository)",
                   HENRY_URL, "give me liberty or give me death!"),
        FactSource("Public-domain status of text 1",
                   "delivered 1775; first published 1817 (Wirt); both pre-1929 => US public domain",
                   "US public domain (17 USC; pre-1929 publication)",
                   HENRY_URL, "The war is actually begun!"),
        FactSource("Speaker and work of text 2",
                   "Frederick Douglass, What to the Slave Is the Fourth of July?, 1852",
                   "Wikisource (transcription of the 1852 Corinthian Hall pamphlet)",
                   DOUGLASS_URL, "This Fourth July is yours, not mine. You may rejoice, I must mourn."),
        FactSource("Public-domain status of text 2 (reconciled vs the 1852 pamphlet scan)",
                   "delivered and first published 1852 (pamphlet); pre-1929 => US public domain",
                   "Internet Archive, 1852 pamphlet scan (ocm30553533)",
                   DOUGLASS_SCAN_URL, "My subject, then, fellow-citizens, is American Slavery."),
    ],
    provenance={
        "copyright": "public_domain",
        "rights": "US public domain (pre-1929)",
        "source": ("A cross-text analysis PAIR of two verbatim public-domain speeches. Text 1: Patrick "
                   "Henry, \"Speech to the Virginia Convention\" (1775), fetched from The Avalon Project, "
                   "Yale Law School: " + HENRY_URL + " . Text 2: Frederick Douglass, \"What to the Slave "
                   "Is the Fourth of July?\" (1852), fetched from Wikisource: " + DOUGLASS_URL + " and "
                   "reconciled against the 1852 pamphlet scan at the Internet Archive: " + DOUGLASS_SCAN_URL +
                   " . Both excerpts are identical to the single-source bank records "
                   "ACC-W910-ANALYSIS-SINGLE-0001 and -0004."),
        "verbatim": True,
        "fetched": "2026-07-07",
    },
)

if __name__ == "__main__":
    qc_stimulus(rec)
    import re
    for p in rec.passages:
        print(f"  {p.title}: {len(re.findall(r'[A-Za-z]+(?:.[A-Za-z]+)?', p.text))} words")
    print(qc_report(rec))
    sys.exit(0 if rec.qc["passed"] else 1)
