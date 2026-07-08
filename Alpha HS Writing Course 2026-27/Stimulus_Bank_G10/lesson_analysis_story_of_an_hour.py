"""
ANALYSIS-mode LESSON stimulus for the G10 writing course (lesson bucket).

TEXT: Kate Chopin, "The Story of an Hour" (1894). Verbatim public-domain excerpt (the opening through the
turn "Free! Body and soul free!"), ~764 words, measured at 1123L (in the G10 1050-1185L band).

WHY THIS TEXT: rhetorical/literary analysis needs a real author's craft to analyze. This excerpt is rich for
analyzing how Chopin builds meaning (irony, the open-window imagery as the emotional turn, free indirect
style). Chosen after founding-era oratory (Lincoln 2nd Inaugural 1324L, Washington Farewell 1350L) measured
too hard, and short speeches (Gettysburg, Sojourner Truth) fell below the 480-word structure floor: this
narrative prose lands in band on BOTH dimensions, the way the existing four analysis stimuli were sized.

NOTE ON THE EXISTING CHOPIN STIMULUS: the test bank already has a Chopin text (analysis_prose = "A Pair of
Silk Stockings", topic chopin_prose, TEST pool). This is a DIFFERENT work (topic story_of_an_hour, LESSON
pool), so there is no lesson-to-test contamination; the topics are disjoint in topic_seed_g10.py.

PUBLIC-DOMAIN JUSTIFICATION: published 1894, far earlier than 1929 => unambiguously US public domain.

SOURCE FETCHED: Wikisource (public-domain text repository),
https://en.wikisource.org/wiki/The_Story_of_an_Hour (fetched 2026-07-08, verbatim).

Family=single, mode=analysis, bucket=lesson. Runs itself through the QC harness and reports every gate.
NOTE: the em dashes below are IN THE VERBATIM PUBLIC-DOMAIN SOURCE and are preserved unaltered; the house
no-em-dash rule applies to OWN-AUTHORED prose, not to a quoted historical text.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# VERBATIM public-domain excerpt (Kate Chopin, "The Story of an Hour", 1894). Real author's words, unaltered.
PASSAGE = (
"Knowing that Mrs. Mallard was afflicted with a heart trouble, great care was taken to break to her as "
"gently as possible the news of her husband's death.\n\n"
"It was her sister Josephine who told her, in broken sentences; veiled hints that revealed in half "
"concealing. Her husband's friend Richards was there, too, near her. It was he who had been in the newspaper "
"office when intelligence of the railroad disaster was received, with Brently Mallard's name leading the "
"list of \"killed.\" He had only taken the time to assure himself of its truth by a second telegram, and had "
"hastened to forestall any less careful, less tender friend in bearing the sad message.\n\n"
"She did not hear the story as many women have heard the same, with a paralyzed inability to accept its "
"significance. She wept at once, with sudden, wild abandonment, in her sister's arms. When the storm of "
"grief had spent itself she went away to her room alone. She would have no one follow her.\n\n"
"There stood, facing the open window, a comfortable, roomy armchair. Into this she sank, pressed down by a "
"physical exhaustion that haunted her body and seemed to reach into her soul.\n\n"
"She could see in the open square before her house the tops of trees that were all aquiver with the new "
"spring life. The delicious breath of rain was in the air. In the street below a peddler was crying his "
"wares. The notes of a distant song which some one was singing reached her faintly, and countless sparrows "
"were twittering in the eaves. There were patches of blue sky showing here and there through the clouds "
"that had met and piled one above the other in the west facing her window.\n\n"
"She sat with her head thrown back upon the cushion of the chair, quite motionless, except when a sob came "
"up into her throat and shook her, as a child who has cried itself to sleep continues to sob in its dreams.\n\n"
"She was young, with a fair, calm face, whose lines bespoke repression and even a certain strength. But now "
"there was a dull stare in her eyes, whose gaze was fixed away off yonder on one of those patches of blue "
"sky. It was not a glance of reflection, but rather indicated a suspension of intelligent thought.\n\n"
"There was something coming to her and she was waiting for it, fearfully. What was it? She did not know; it "
"was too subtle and elusive to name. But she felt it, creeping out of the sky, reaching toward her through "
"the sounds, the scents, the color that filled the air.\n\n"
"Now her bosom rose and fell tumultuously. She was beginning to recognize this thing that was approaching to "
"possess her, and she was striving to beat it back with her will—as powerless as her two white slender "
"hands would have been. When she abandoned herself a little whispered word escaped her slightly parted lips. "
"She said it over and over under her breath: \"free, free, free!\" The vacant stare and the look of terror "
"that had followed it went from her eyes. They stayed keen and bright. Her pulses beat fast, and the coursing "
"blood warmed and relaxed every inch of her body.\n\n"
"She did not stop to ask if it were or were not a monstrous joy that held her. A clear and exalted "
"perception enabled her to dismiss the suggestion as trivial.\n\n"
"She knew that she would weep again when she saw the kind, tender hands folded in death; the face that had "
"never looked save with love upon her, fixed and gray and dead. But she saw beyond that bitter moment a long "
"procession of years to come that would belong to her absolutely. And she opened and spread her arms out to "
"them in welcome.\n\n"
"There would be no one to live for her during those coming years; she would live for herself. There would be "
"no powerful will bending hers in that blind persistence with which men and women believe they have a right "
"to impose a private will upon a fellow-creature. A kind intention or a cruel intention made the act seem no "
"less a crime as she looked upon it in that brief moment of illumination.\n\n"
"And yet she had loved him—sometimes. Often she had not. What did it matter! What could love, the "
"unsolved mystery, count for in face of this possession of self-assertion which she suddenly recognized as "
"the strongest impulse of her being!\n\n"
"\"Free! Body and soul free!\""
)

SOURCE_URL = "https://en.wikisource.org/wiki/The_Story_of_an_Hour"

rec = StimulusRecord(
    id="ACC-W910-ANALYSIS-LESSON-HOUR",
    grade="9-10", mode="analysis", family="single", bucket="lesson",
    topic_id="story_of_an_hour",
    modeling_anchor="AP Lang / AP Lit prose analysis / NY Regents Part 3",
    acc_tags=["ACC.W.INFO.6", "ACC.W.SRC.3", "CCSS.RL.9-10.4", "CCSS.W.9-10.9"],
    prompt=("Analyze how Kate Chopin uses literary choices (such as imagery, irony, and point of view) to "
            "develop Mrs. Mallard's response to the news in this excerpt from her 1894 story \"The Story of "
            "an Hour.\" Use specific evidence from the text to support your analysis."),
    passages=[Passage(
        title="From \"The Story of an Hour\" (1894)",
        text=PASSAGE,
        angle="verbatim public-domain source text for literary analysis")],
    fact_sources=[
        FactSource("Author and work of the source text",
                   "Kate Chopin, \"The Story of an Hour\", 1894",
                   "Wikisource (public-domain text repository)",
                   SOURCE_URL,
                   "Free! Body and soul free!"),
        FactSource("Public-domain status of the text",
                   "published 1894 (pre-1929) => US public domain",
                   "US public domain (pre-1929 publication)",
                   SOURCE_URL,
                   "Knowing that Mrs. Mallard was afflicted with a heart trouble"),
        FactSource("Work context (teacher context, not the student prompt)",
                   "short story first published 1894 (as \"The Dream of an Hour\")",
                   "Wikisource",
                   SOURCE_URL,
                   "There stood, facing the open window, a comfortable, roomy armchair."),
    ],
    provenance={
        "copyright": "public_domain",
        "rights": "US public domain (pre-1929)",
        "source": ("Kate Chopin, \"The Story of an Hour\", first published 1894. Verbatim excerpt (opening "
                   "through \"Free! Body and soul free!\") fetched from Wikisource: " + SOURCE_URL),
        "verbatim": True,
        "fetched": "2026-07-08",
    },
)

if __name__ == "__main__":
    qc_stimulus(rec)
    import re
    wc = len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", PASSAGE))
    print(f"passage word count: {wc}")
    print(qc_report(rec))
    sys.exit(0 if rec.qc["passed"] else 1)
