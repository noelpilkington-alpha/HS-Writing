"""
ANALYSIS-mode LESSON stimulus for the G9 writing course (English I band, lesson bucket).

TEXT: O. Henry (William Sydney Porter), "The Gift of the Magi" (1905). Verbatim public-domain excerpt
(the opening through the mock-heroic "queen of Sheba" / "King Solomon" paragraph), ~599 words, measured at
1082L (inside the G9 1010-1150L English I band).

WHY THIS TEXT: rhetorical/literary analysis needs a real author's craft to analyze. This opening is rich for
analyzing how O. Henry builds meaning and tone: the mock-heroic narrator who turns a poor young wife's small
savings into an epic problem, the deliberate repetition of "gray" that colors Della's world, the intrusive
narrator who addresses the reader directly, and the characterization of Della through what she treasures. It
sets up the story's central irony without resolving it, so students analyze CHOICES rather than plot.

WHY G9 (not G10): this excerpt lands at 1082L, comfortably inside the G9 English I ship gate (1010-1150L) and
lower than the G10 Chopin analysis text (1123L). O. Henry's narrative prose is more accessible than founding-era
oratory (which measured far too hard) yet clears the 480-word structure floor, so it lands in band on BOTH
dimensions.

NO CONTAMINATION WITH G10: the G10 analysis pool uses Chopin ("The Story of an Hour", "A Pair of Silk
Stockings"), Patrick Henry, Reagan's Challenger address, and Frederick Douglass. This is a DIFFERENT author and
work (O. Henry, "The Gift of the Magi"), so there is no lesson-to-test or grade-to-grade text overlap.

PUBLIC-DOMAIN JUSTIFICATION: first published 1905 (in "The New York Sunday World"), far earlier than 1929 =>
unambiguously US public domain.

SOURCE FETCHED: Project Gutenberg (public-domain text repository), eBook #7256,
https://www.gutenberg.org/cache/epub/7256/pg7256.txt (fetched 2026-07-09, verbatim).

Family=single, mode=analysis, bucket=lesson. Runs itself through the QC harness and reports every gate.
NOTE: the em dash below is IN THE VERBATIM PUBLIC-DOMAIN SOURCE and is preserved unaltered; the house
no-em-dash rule applies to OWN-AUTHORED prose, not to a quoted historical text. (The source's curly quotes were
normalized to straight ASCII quotes, matching the other analysis stimuli; no words were changed.)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# VERBATIM public-domain excerpt (O. Henry, "The Gift of the Magi", 1905). Real author's words, unaltered
# (curly quotes normalized to straight ASCII; the one em dash is preserved from the source).
PASSAGE = (
"One dollar and eighty-seven cents. That was all. And sixty cents of it was in pennies. Pennies saved one and "
"two at a time by bulldozing the grocer and the vegetable man and the butcher until one's cheeks burned with "
"the silent imputation of parsimony that such close dealing implied. Three times Della counted it. One dollar "
"and eighty-seven cents. And the next day would be Christmas.\n\n"
"There was clearly nothing to do but flop down on the shabby little couch and howl. So Della did it. Which "
"instigates the moral reflection that life is made up of sobs, sniffles, and smiles, with sniffles "
"predominating.\n\n"
"While the mistress of the home is gradually subsiding from the first stage to the second, take a look at the "
"home. A furnished flat at $8 per week. It did not exactly beggar description, but it certainly had that word "
"on the lookout for the mendicancy squad.\n\n"
"In the vestibule below was a letter-box into which no letter would go, and an electric button from which no "
"mortal finger could coax a ring. Also appertaining thereunto was a card bearing the name \"Mr. James "
"Dillingham Young.\"\n\n"
"The \"Dillingham\" had been flung to the breeze during a former period of prosperity when its possessor was "
"being paid $30 per week. Now, when the income was shrunk to $20, though, they were thinking seriously of "
"contracting to a modest and unassuming D. But whenever Mr. James Dillingham Young came home and reached his "
"flat above he was called \"Jim\" and greatly hugged by Mrs. James Dillingham Young, already introduced to you "
"as Della. Which is all very good.\n\n"
"Della finished her cry and attended to her cheeks with the powder rag. She stood by the window and looked out "
"dully at a gray cat walking a gray fence in a gray backyard. Tomorrow would be Christmas Day, and she had "
"only $1.87 with which to buy Jim a present. She had been saving every penny she could for months, with this "
"result. Twenty dollars a week doesn't go far. Expenses had been greater than she had calculated. They always "
"are. Only $1.87 to buy a present for Jim. Her Jim. Many a happy hour she had spent planning for something "
"nice for him. Something fine and rare and sterling—something just a little bit near to being worthy of the "
"honor of being owned by Jim.\n\n"
"There was a pier glass between the windows of the room. Perhaps you have seen a pier glass in an $8 flat. A "
"very thin and very agile person may, by observing his reflection in a rapid sequence of longitudinal strips, "
"obtain a fairly accurate conception of his looks. Della, being slender, had mastered the art.\n\n"
"Suddenly she whirled from the window and stood before the glass. Her eyes were shining brilliantly, but her "
"face had lost its color within twenty seconds. Rapidly she pulled down her hair and let it fall to its full "
"length.\n\n"
"Now, there were two possessions of the James Dillingham Youngs in which they both took a mighty pride. One "
"was Jim's gold watch that had been his father's and his grandfather's. The other was Della's hair. Had the "
"queen of Sheba lived in the flat across the airshaft, Della would have let her hair hang out the window some "
"day to dry just to depreciate Her Majesty's jewels and gifts. Had King Solomon been the janitor, with all "
"his treasures piled up in the basement, Jim would have pulled out his watch every time he passed, just to "
"see him pluck at his beard from envy."
)

SOURCE_URL = "https://www.gutenberg.org/cache/epub/7256/pg7256.txt"

rec = StimulusRecord(
    id="ACC-W910-ANALYSIS-LESSON-G9",
    grade="9", mode="analysis", family="single", bucket="lesson",
    topic_id="gift_of_the_magi",
    modeling_anchor="STAAR English I / SC-TDA analysis",
    acc_tags=["ACC.W.INFO.6", "ACC.W.SRC.3", "CCSS.W.9-10.9"],
    prompt=("Analyze how O. Henry uses literary choices (such as tone, imagery, and the narrator's voice) to "
            "develop Della and her situation in this opening from his 1905 short story \"The Gift of the "
            "Magi.\" Use specific evidence from the text to support your analysis."),
    passages=[Passage(
        title="From \"The Gift of the Magi\" (1905)",
        text=PASSAGE,
        angle="verbatim public-domain source text for literary analysis")],
    fact_sources=[
        FactSource("Author and work of the source text",
                   "O. Henry (William Sydney Porter), \"The Gift of the Magi\", 1905",
                   "Project Gutenberg (public-domain text repository), eBook #7256",
                   SOURCE_URL,
                   "One dollar and eighty-seven cents. That was all."),
        FactSource("Public-domain status of the text",
                   "first published 1905 (pre-1929) => US public domain",
                   "US public domain (pre-1929 publication)",
                   SOURCE_URL,
                   "And the next day would be Christmas."),
        FactSource("Work context (teacher context, not the student prompt)",
                   "short story first published 1905 in \"The New York Sunday World\"",
                   "Project Gutenberg",
                   SOURCE_URL,
                   "The other was Della's hair."),
    ],
    provenance={
        "copyright": "public_domain",
        "rights": "US public domain (pre-1929)",
        "source": ("O. Henry (William Sydney Porter), \"The Gift of the Magi\", first published 1905. Verbatim "
                   "excerpt (opening through the \"queen of Sheba\" / \"King Solomon\" paragraph) fetched from "
                   "Project Gutenberg eBook #7256: " + SOURCE_URL),
        "verbatim": True,
        "fetched": "2026-07-09",
    },
)

if __name__ == "__main__":
    qc = qc_stimulus(rec)
    import re
    wc = len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", PASSAGE))
    print(f"passage word count: {wc}")
    print(qc_report(rec))
    sys.exit(0 if qc["passed"] else 1)
