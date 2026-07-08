"""
lesson_t4_analysis.py  -  G10 model lesson, TYPE 4: TEXT-DEPENDENT ANALYSIS (highest-load).

Assembles a Timeback assessment-test (ordered item sequence) that instantiates the council-adjudicated
Type-4 shell (G10_Model_Lesson_Specs.md) against the REAL G10 banks. Type 4 is the highest-intrinsic-load
type (KH ranking: analysis > evidence-integration > ...), so it carries the MOST staging: the worked example
is kept longest, and the Supported stage gets ONE EXTRA rung (the KH humanities under-support caveat).

CONTAMINATION-FREE REBUILD: this lesson binds ONLY LESSON-pool stimuli, so a student never learns on the
same passage they are later tested on. The old build bound a TEST-pool analysis single and a TEST
constructed-response item; those bindings are removed.
Binds:
  - stimulus  ACC-W910-ANALYSIS-LESSON-HOUR (Kate Chopin, "The Story of an Hour", 1894, public domain)
        -> the text analyzed (TEACH display + MODEL worked example + SUPPORTED completion + INDEPENDENT)
  - stimulus  ACC-W910-INFO-LESSON-WEATHER (NWS forecasting, US-federal-sourced explanatory single)
        -> the bank-partitioned TRANSFER text; students analyze HOW the informational author structures and
           sequences the piece (a valid analysis transfer into a new genre)

The INDEPENDENT analysis is an AUTHORED production_frq (ref="") on the Chopin text, NOT a bound CR item: the
CR items live in the TEST bank, and binding one would reintroduce the learn-on-what-you-test-on contamination.
The two SUPPORTED discriminations are authored inline (ref="") for the same reason (the SR families register
ids positionally, and those items are test-bank items). Inline discrimination is the contract-sanctioned
alternative (ref="", labeled_grade_c=True).

Mnemonic DEW (Device, Effect, Warrant), status = proposal (NOT a sourced/established mnemonic). The scored
top-band move is the W (Warrant / why-it-matters): analysis that reaches SIGNIFICANCE, not analysis that stops
at effect (gap #22, the 4->5 lift). The classic failure this lesson discriminates against is analysis-vs-
summary-vs-paraphrase.

Model = the modality-corrected 4-mechanism async sequence (clean annotated before/after -> predict-the-fix ->
feedback on the student's OWN draft [the FRQ grader] -> student-generated diagnosis). No passive-read messy
think-aloud, and no claim to SRSD's live-enacted effect size. Bank-partitioned transfer (Chopin narrative ->
weather explanatory). All slots map to native Timeback interactions.

Runs the QC harness on execution and prints PASS/FAIL. Dependency-free (stdlib + lesson_contract).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report

LESSON = Lesson(
    id="ACC-W910-L-T4-ANALYSIS-0001", grade="9-10", lesson_type=4,
    unit="G10 U3 - Text-dependent analysis (analyze the author's move)",
    title="Analyze the Move, Reach the Significance (DEW)",
    target=("Analyze HOW an author builds meaning, not WHAT the text says: name the Device, state the "
            "Effect it has on the audience, and reach the Warrant (why that effect matters to the author's "
            "purpose). The Warrant is the scored top-band move. Traits: Evidence/Development + Organization."),
    acc_tags=["ACC.W.INFO.6", "ACC.W.ANALYSIS.1", "CCSS.RI.9-10.6", "CCSS.W.9-10.2"],
    provenance={"copyright": "own_authored", "authored": "2026-07-08",
                "mnemonic_status": "proposal",
                "council": "DI faultless-clean worked example (highest rigor) + KH extra-rung under-support "
                           "caveat; TSIS metacommentary as content; W&H boundary-pair discrimination; "
                           "gap #22 significance elevated to the scored move"},
    fade_ledger_moves=["device-effect-warrant", "because/but/so", "attributive-tag"],
    slots=[
        # ---------------- TEACH: the DEW cue + analysis-is-not-summary + the significance principle ----------------
        Slot("TEACH", "teach_card", "Analysis is not summary: the DEW cue and the significance principle",
             body=("Summary retells WHAT a text says. Paraphrase re-says it in other words. Analysis is a "
                   "different job: it explains HOW an author builds meaning and WHY that choice works on the "
                   "reader. On an analysis rubric, retelling the text sits in the low band no matter how "
                   "accurate it is, because it never answers the real question: what is the author DOING? Our "
                   "cue for the analytical move is DEW. Device: name the specific choice the author makes (an "
                   "image, a repeated word, a shift in tone, a piece of irony). Effect: say what that choice "
                   "does to the reader. Warrant: reach the significance, why that effect matters to the "
                   "author's purpose and how you know. Here is the part to hold onto: most students stop at the "
                   "Effect and stall in the middle band. The move that lifts analysis into the top band is the "
                   "W, the Warrant. Reaching why it matters is the difference between a solid response and an "
                   "insightful one. Goal for today: write analysis that reaches significance, not analysis "
                   "that stops at what the author did.")),
        Slot("TEACH", "stimulus_display", "Read the source: Kate Chopin, \"The Story of an Hour\" (1894)",
             ref="ACC-W910-ANALYSIS-LESSON-HOUR", bank="story_of_an_hour",
             body=("Read this excerpt from Kate Chopin's 1894 story. It opens with Mrs. Mallard learning that "
                   "her husband has died in a railroad accident, then follows her alone in her room. As you "
                   "read, mark ONE choice the author makes (an image she lingers on, a moment of irony, a "
                   "repeated word). You will analyze that one move, not the whole story. Notice especially what "
                   "Mrs. Mallard sees through the open window and the word she begins to whisper.")),

        # ---------------- MODEL: highest-load, kept LONGEST (4-mechanism async sequence) ----------------
        Slot("MODEL", "annotated_before_after", "Watch summary become analysis that reaches significance",
             bank="story_of_an_hour",
             body=("BEFORE (this is summary, not analysis): In this part of the story Mrs. Mallard sits in a "
                   "chair by an open window after she hears that her husband has died. She looks outside and "
                   "sees trees, blue sky, and rain, and she hears birds and a song in the distance. Chopin uses "
                   "a lot of nature description to set the scene before Mrs. Mallard starts saying she is free. "
                   "Why the BEFORE version fails: every sentence retells WHAT the text shows or slaps a label on "
                   "it ('a lot of nature description to set the scene'). It never explains what the choice DOES "
                   "or why it matters. That is summary plus device-spotting, and it caps at the middle band. "
                   "AFTER (real DEW analysis, annotated): Chopin crowds the view through the open window with "
                   "signs of life: the tops of trees 'all aquiver with the new spring life,' the 'delicious "
                   "breath of rain,' and 'patches of blue sky' breaking through the clouds [DEVICE: a cluster of "
                   "spring and renewal imagery, placed at the window at the very moment of grief]. Because those "
                   "images press in exactly where the reader expects mourning, they tilt the scene toward life "
                   "and possibility rather than loss [EFFECT: the reader begins to feel renewal gathering around "
                   "her before she names it]. That matters because Chopin needs the reader to sense Mrs. "
                   "Mallard's coming liberation before she will admit it herself, so the open window lets the "
                   "whispered 'free, free, free' arrive as something the reader has already half-felt, which is "
                   "what makes the story's central irony, that a death is what frees her, land as a discovery "
                   "instead of a mere announcement [WARRANT: why the effect serves Chopin's purpose, the "
                   "significance]. "
                   "Notice the AFTER version moves Device to Effect to Warrant and does not stop until it "
                   "reaches why the move matters. The last sentence is the significance, and it is what separates "
                   "top-band analysis from a competent effect statement.")),
        Slot("MODEL", "predict_the_fix", "Predict: is this analysis, and if not, what fixes it?",
             bank="story_of_an_hour",
             body=("Diagnose this draft before we reveal the fix. Draft: 'Chopin repeats the word free near the "
                   "end. This is a powerful moment. It shows Mrs. Mallard is happy now.' Which single move would "
                   "most improve it? "
                   "(A) explain what the repetition of 'free' DOES to the reader and why it matters to Chopin's "
                   "purpose (reach effect and warrant)  "
                   "(B) quote one more sentence from the story  "
                   "(C) name two more literary devices Chopin uses  "
                   "(D) make the sentences longer and more formal")),
        # feedback carried on the predict_the_fix slot (feedback-block reveal); required by model_sequence gate.
        # (kept short of the ~1000-char limit)

        # ---------------- SUPPORTED: EXTRA rung (KH under-support): TWO discriminations, then completion ----------------
        Slot("SUPPORTED", "discrimination", "Discriminate: analysis vs summary vs paraphrase (three-way)",
             ref="", labeled_grade_c=True, bank="story_of_an_hour",
             body=("Design-bet step (discriminate before you produce; this is a Grade-C move we label as a bet, "
                   "not a proven ingredient). You will see three responses to the same moment in the Chopin "
                   "excerpt, the view through the open window. One SUMMARIZES (retells what she sees), one "
                   "PARAPHRASES (re-says it in other words), and one ANALYZES (names the imagery as a device, "
                   "states its effect on the reader, and reaches the warrant). Pick the analysis. The three "
                   "differ on exactly one thing: whether the response explains HOW and WHY the choice works, or "
                   "only re-reports the content.")),
        Slot("SUPPORTED", "discrimination", "Discriminate: effect stated vs significance reached (the 4->5 lift)",
             ref="", labeled_grade_c=True, bank="story_of_an_hour",
             body=("Second discrimination (the top-band boundary pair). Both responses are real analysis and "
                   "both correctly state an EFFECT of the spring imagery. They differ on one move only: one "
                   "stops at the effect ('the imagery makes the scene feel hopeful, not sad'), the other reaches "
                   "the WARRANT ('and that hopefulness lets the reader feel her liberation before she admits it, "
                   "which is what makes the death-frees-her irony land as discovery'). Pick the version that "
                   "reaches significance. This is the exact move that lifts a mid-band response into the top "
                   "band.")),
        Slot("SUPPORTED", "production_frq", "Completion: the device is given, you supply Effect + Warrant",
             bank="story_of_an_hour", rubric_ref="rc.staar", scored=True,
             body=("Guided completion (the device is named for you, so you can spend all your effort on the "
                   "hard part). DEVICE: Chopin describes Mrs. Mallard as 'striving to beat it back with her "
                   "will' and then, when she gives in, whispering 'free, free, free' over and over under her "
                   "breath. In TWO sentences, supply the rest of DEW: sentence one states the EFFECT this "
                   "struggle-then-surrender has on the reader, sentence two reaches the WARRANT (why that effect "
                   "matters to Chopin's purpose in showing a woman discovering, against her own will, that she "
                   "feels freed). Do not restate what the passage says; explain what it does and why it "
                   "matters.")),
        Slot("MODEL", "diagnosis_frq", "Diagnose your own analysis: effect, or significance?",
             bank="story_of_an_hour", scored=True,
             body=("Diagnose your own work. In one or two sentences: did your response stop at the EFFECT (what "
                   "the device does), or did you reach the WARRANT (why it matters to the author's purpose)? "
                   "Point to the exact sentence where you move from Device to Effect to Warrant, or name the "
                   "spot where your analysis stalled at effect and did not reach significance.")),

        # ---------------- INDEPENDENT: full DEW analysis on the Chopin text (AUTHORED, not a bound CR item) --------
        Slot("INDEPENDENT", "production_frq", "Full DEW analysis of the Chopin excerpt (authored prompt)",
             ref="", bank="story_of_an_hour", rubric_ref="rc.ohio", scored=True,
             body=("Independent performance. Choose one of Chopin's literary choices in the excerpt (the "
                   "open-window imagery, the irony of Mrs. Mallard's reaction, the repetition of 'free,' or the "
                   "shift in how her face and body are described). Write a paragraph that runs the full DEW "
                   "move: name the DEVICE with specific evidence from the text, explain the EFFECT it has on the "
                   "reader, and reach the WARRANT (why that choice matters to how Chopin develops Mrs. Mallard's "
                   "response to the news). Scored on Evidence/Development and Organization; the significance "
                   "beat is the top-band move.")),

        # ---------------- TRANSFER: same DEW move, DIFFERENT author + genre, partitioned content bank ------------
        Slot("TRANSFER", "production_frq", "Analyze a DIFFERENT author's move (weather explanatory, partitioned)",
             ref="ACC-W910-INFO-LESSON-WEATHER", bank="weather_science", rubric_ref="rc.mcas", scored=True,
             body=("Transfer to a text you have not practiced on, in a different genre. The article 'How a "
                   "Weather Forecast Is Made' is not a story; it explains a process. Here the author's choices "
                   "are about STRUCTURE and SEQUENCE, not imagery. Analyze ONE such choice, for example the "
                   "decision to open with how 'ordinary' forecasts seem before revealing the science behind "
                   "them, or the choice to present the whole system as a single chain that runs from a balloon "
                   "drifting through the sky to an alert buzzing on a phone. Run the full DEW move: name the "
                   "DEVICE (the structural or wording choice) with evidence, state its EFFECT on the reader, and "
                   "reach the WARRANT (why that choice serves the author's purpose of making a complex system "
                   "clear). Same analytical move as the story; new author, new genre. Scored on "
                   "Evidence/Development and Organization.")),
    ],
)

# The predict-the-fix reveal (feedback-block). Set after construction to keep the slot list readable.
for _s in LESSON.slots:
    if _s.kind == "predict_the_fix":
        _s.feedback = (
            "The strongest fix is A. The draft names a device (the repetition of 'free') and gives a vague "
            "label ('a powerful moment'), but it never explains what the repetition DOES to the reader or WHY "
            "that matters. That is summary plus device-spotting, not analysis. The fix is to reach the Effect "
            "and the Warrant: whispering 'free' over and over, under her breath and almost against her will, "
            "lets the reader watch a feeling surface that Mrs. Mallard has not yet dared to claim (Effect), and "
            "that slow surfacing matters because it makes her liberation feel discovered rather than declared, "
            "which is what gives the story's irony its force (Warrant). A second quote (B), more device names "
            "(C), or longer sentences (D) do not fix analysis that stalls at effect. Reaching significance is "
            "the E-to-W move, the lift into the top band.")

LESSONS = [LESSON]

if __name__ == "__main__":
    ok = True
    for L in LESSONS:
        qc_lesson(L)
        print(qc_report(L)); print()
        ok = ok and L.qc["passed"]
    passed = sum(1 for L in LESSONS if L.qc["passed"])
    print(f"{passed}/{len(LESSONS)} PASS")
    sys.exit(0 if ok else 1)
