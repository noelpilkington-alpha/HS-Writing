"""
ANALYSIS-mode TEST stimulus for the G9 writing test bank (English I band, test bucket).

TEXT: Guy de Maupassant, "The Necklace" (French title "La Parure"), first published in the newspaper
Le Gaulois, February 17, 1884. This English translation is the one carried in the Project Gutenberg
edition below (titled "The Diamond Necklace" there). Verbatim public-domain excerpt = the story's setup
movement, from Mathilde's "no gowns, no jewels, nothing" longing, through the ball invitation and the
gown negotiation, to the moment she discovers the superb diamond necklace and "fled with her treasure."
~837 words, measured at 1049L (inside the G9 English I ship gate, 1010-1150L).

WHY THIS TEXT: literary analysis needs a real author's craft to analyze. This excerpt is rich for it: the
opening irony of a woman who "had no gowns, no jewels, nothing" and yet "loved nothing but that"; the
free-indirect longing that characterizes Mathilde through her cravings; the small comic-pathetic detail of
the husband quietly surrendering the gun money he had saved; and a clear narrative turn when the diamond
necklace, the very object that will destroy the couple, is seized in "ecstasy." Students analyze CHOICES
(irony, characterization, imagery, the turn) rather than plot, because the excerpt stops before the loss.

WHY G9 (not G10): this translation's dialogue-heavy setup lands at 1049L, comfortably inside the G9 band
(1010-1150L) and below the G10 analysis texts; the very dense descriptive opening paragraphs (silent
antechambers, bronze candelabra) measure far harder and were deliberately left out so the excerpt sits in
band on both length and complexity.

NO CONTAMINATION WITH G10 OR THE G9 LESSON POOL: the G10 analysis pool uses Kate Chopin ("The Story of an
Hour", "A Pair of Silk Stockings"), Patrick Henry, Reagan's Challenger address, and Frederick Douglass;
the G9 LESSON analysis uses O. Henry, "The Gift of the Magi." This is a DIFFERENT author and work (Guy de
Maupassant, "The Necklace"), so there is no text overlap across grade, bucket, or lesson-to-test.

PUBLIC-DOMAIN JUSTIFICATION: Maupassant (1850-1893) and the 1884 first publication are both far earlier
than 1929, so the underlying work is unambiguously in the US public domain. The English translation in
this Gutenberg volume is itself old enough to be public domain in the US; Project Gutenberg lists the
edition as free for use "in the United States and most other parts of the world." No third-party
copyrighted expression is used; the excerpt reproduces the translation's words unaltered.

SOURCE FETCHED: Project Gutenberg (public-domain text repository), eBook #3090, "Complete Original Short
Stories of Guy De Maupassant," plain-text edition, https://www.gutenberg.org/cache/epub/3090/pg3090.txt
(fetched 2026-07-09, verbatim). The Gutenberg boilerplate header and footer were stripped; only the
underlying text is used. Curly quotation marks were normalized to straight ASCII quotes (matching the
other analysis stimuli), and wrapped source lines were rejoined into running paragraphs; no wording was
changed.

Family=single, mode=analysis, bucket=test. Runs itself through the QC harness and reports every gate.
NOTE: the one em dash below ("occasions-something") is IN THE VERBATIM PUBLIC-DOMAIN SOURCE and is
preserved unaltered; the house no-em-dash rule applies to OWN-AUTHORED prose, not to a quoted text.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# VERBATIM public-domain excerpt (Guy de Maupassant, "The Necklace", 1884; this Gutenberg translation).
# Real author's/translator's words, unaltered. Paragraph breaks preserved; only wrapped lines were rejoined
# and curly quotes normalized to straight ASCII. The single em dash is preserved from the source.
PASSAGE = """She had no gowns, no jewels, nothing. And she loved nothing but that. She felt made for that. She would have liked so much to please, to be envied, to be charming, to be sought after.

She had a friend, a former schoolmate at the convent, who was rich, and whom she did not like to go to see any more because she felt so sad when she came home.

But one evening her husband reached home with a triumphant air and holding a large envelope in his hand.

"There," said he, "there is something for you."

She tore the paper quickly and drew out a printed card which bore these words:

The Minister of Public Instruction and Madame Georges Ramponneau request the honor of M. and Madame Loisel's company at the palace of the Ministry on Monday evening, January 18th.

Instead of being delighted, as her husband had hoped, she threw the invitation on the table crossly, muttering:

"What do you wish me to do with that?"

"Why, my dear, I thought you would be glad. You never go out, and this is such a fine opportunity. I had great trouble to get it. Every one wants to go; it is very select, and they are not giving many invitations to clerks. The whole official world will be there."

She looked at him with an irritated glance and said impatiently:

"And what do you wish me to put on my back?"

He had not thought of that. He stammered:

"Why, the gown you go to the theatre in. It looks very well to me."

He stopped, distracted, seeing that his wife was weeping. Two great tears ran slowly from the corners of her eyes toward the corners of her mouth.

"What's the matter? What's the matter?" he answered.

By a violent effort she conquered her grief and replied in a calm voice, while she wiped her wet cheeks:

"Nothing. Only I have no gown, and, therefore, I can't go to this ball. Give your card to some colleague whose wife is better equipped than I am."

He was in despair. He resumed:

"Come, let us see, Mathilde. How much would it cost, a suitable gown, which you could use on other occasions—something very simple?"

She reflected several seconds, making her calculations and wondering also what sum she could ask without drawing on herself an immediate refusal and a frightened exclamation from the economical clerk.

Finally she replied hesitating:

"I don't know exactly, but I think I could manage it with four hundred francs."

He grew a little pale, because he was laying aside just that amount to buy a gun and treat himself to a little shooting next summer on the plain of Nanterre, with several friends who went to shoot larks there of a Sunday.

But he said:

"Very well. I will give you four hundred francs. And try to have a pretty gown."

The day of the ball drew near and Madame Loisel seemed sad, uneasy, anxious. Her frock was ready, however. Her husband said to her one evening:

"What is the matter? Come, you have seemed very queer these last three days."

And she answered:

"It annoys me not to have a single piece of jewelry, not a single ornament, nothing to put on. I shall look poverty-stricken. I would almost rather not go at all."

"You might wear natural flowers," said her husband. "They're very stylish at this time of year. For ten francs you can get two or three magnificent roses."

She was not convinced.

"No; there's nothing more humiliating than to look poor among other women who are rich."

"How stupid you are!" her husband cried. "Go look up your friend, Madame Forestier, and ask her to lend you some jewels. You're intimate enough with her to do that."

She uttered a cry of joy:

"True! I never thought of it."

The next day she went to her friend and told her of her distress.

Madame Forestier went to a wardrobe with a mirror, took out a large jewel box, brought it back, opened it and said to Madame Loisel:

"Choose, my dear."

She saw first some bracelets, then a pearl necklace, then a Venetian gold cross set with precious stones, of admirable workmanship. She tried on the ornaments before the mirror, hesitated and could not make up her mind to part with them, to give them back. She kept asking:

"Haven't you any more?"

"Why, yes. Look further; I don't know what you like."

Suddenly she discovered, in a black satin box, a superb diamond necklace, and her heart throbbed with an immoderate desire. Her hands trembled as she took it. She fastened it round her throat, outside her high-necked waist, and was lost in ecstasy at her reflection in the mirror.

Then she asked, hesitating, filled with anxious doubt:

"Will you lend me this, only this?"

"Why, yes, certainly."

She threw her arms round her friend's neck, kissed her passionately, then fled with her treasure."""

SOURCE_URL = "https://www.gutenberg.org/cache/epub/3090/pg3090.txt"

REC = StimulusRecord(
    id="ACC-W910-ANALYSIS-SINGLE-0005",
    grade="9", mode="analysis", family="single", bucket="test", form="mcas", annotated=False,
    topic_id="the_necklace_maupassant",
    modeling_anchor="MCAS / SC-TDA analysis",
    acc_tags=["ACC.W.INFO.6", "ACC.W.ANALYSIS.1", "CCSS.RL.9-10.4", "CCSS.RL.9-10.3", "CCSS.W.9-10.9"],
    prompt=("Analyze how Guy de Maupassant uses literary choices (such as characterization, imagery, "
            "and irony) to develop Madame Loisel and the tone of this excerpt from the setup of his "
            "1884 short story \"The Necklace.\" Use specific evidence from the text to support your "
            "analysis."),
    passages=[Passage(
        title="From \"The Necklace\" (1884)",
        text=PASSAGE,
        angle="verbatim public-domain source text for literary (prose-fiction) analysis")],
    # For a PD verbatim text these rows DOCUMENT THE SOURCE (author/work/year + fetched URL + PD status),
    # not authored facts. The contract skips figure-backing for public_domain but still requires >=1 source
    # row and >=1 fetched http(s) URL (provenance + citable_facts gates).
    fact_sources=[
        FactSource("Author and work of the source text",
                   "Guy de Maupassant, \"The Necklace\" (\"La Parure\"), first published 1884",
                   "Project Gutenberg (public-domain text repository), eBook #3090",
                   SOURCE_URL,
                   "She had no gowns, no jewels, nothing. And she loved nothing but that."),
        FactSource("Public-domain status of the text",
                   "author lived 1850-1893; story first published 1884; both pre-1929 => US public domain",
                   "US public domain (17 USC; pre-1929 publication + translation); Gutenberg: free \"in the United States\"",
                   SOURCE_URL,
                   "But one evening her husband reached home with a triumphant air"),
        FactSource("Craft focus of the excerpt (teacher/context, not the student prompt)",
                   "setup establishes characterization, imagery, and irony; ends on the turn (the diamond necklace)",
                   "Project Gutenberg, eBook #3090 (Guy de Maupassant)",
                   SOURCE_URL,
                   "Suddenly she discovered, in a black satin box, a superb diamond necklace"),
    ],
    provenance={
        "copyright": "public_domain",
        "rights": "US public domain (pre-1929 publication and translation)",
        "source": ("Guy de Maupassant, \"The Necklace\" (\"La Parure\"), first published in Le Gaulois, "
                   "February 17, 1884; author lived 1850-1893. Verbatim excerpt (the setup movement, from "
                   "\"no gowns, no jewels\" through discovering the diamond necklace) fetched from Project "
                   "Gutenberg eBook #3090, \"Complete Original Short Stories of Guy De Maupassant\": "
                   + SOURCE_URL),
        "verbatim": True,
        "fetched": "2026-07-09",
    },
)

if __name__ == "__main__":
    import re
    wc = len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", PASSAGE))
    print(f"passage word count: {wc}")
    qc = qc_stimulus(REC); print(qc_report(REC)); import sys; sys.exit(0 if qc["passed"] else 1)
