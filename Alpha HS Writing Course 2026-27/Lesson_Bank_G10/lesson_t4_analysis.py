"""
lesson_t4_analysis.py  -  G10 model lesson, TYPE 4: TEXT-DEPENDENT ANALYSIS (highest-load).

Recrafted to the 17-gate DI bar, copying the moves the Type-1 source-reading lesson proved
(lesson_t1_source_reading.py): define every technical term before use, write out real
student-facing content (no blueprint stubs), model the high-load move before requiring it, and
name distinct objects distinctly. Type 4 is the highest-intrinsic-load type (KH element-count
ranking: analysis over evidence-integration over the rest), so it carries the MOST staging: the
worked example is kept longest, and the Supported stage gets ONE EXTRA rung (TWO discriminations,
the KH humanities under-support caveat) before any production.

CONTAMINATION-FREE: this lesson binds ONLY LESSON-pool stimuli, so a student never learns on the
same passage they are later tested on. The connective slots (both discriminations, the diagnosis,
and the independent prompt) are AUTHORED inline (ref=""), because the reusable practice-item
families and constructed-response items register their ids positionally in the test pool, and
binding one would reintroduce learn-on-what-you-test-on contamination. Inline authoring is the
contract-sanctioned alternative (ref="", and for choice items labeled_grade_c=True).

Binds:
  - stimulus  ACC-W910-ANALYSIS-LESSON-HOUR (Kate Chopin, "The Story of an Hour", 1894, public domain)
        -> the text analyzed (TEACH display + MODEL worked example + SUPPORTED completion + INDEPENDENT)
  - stimulus  ACC-W910-INFO-LESSON-WEATHER (NWS forecasting, US-federal-sourced explanatory single)
        -> the bank-partitioned TRANSFER text; students analyze HOW the informational author structures
           and sequences the piece (a valid analysis transfer into a new genre)

Mnemonic DEW (Device, Effect, Warrant), status = proposal (NOT a sourced or established mnemonic).
The scored top-band move is the W (Warrant, why-it-matters): analysis that reaches SIGNIFICANCE,
not analysis that stops at effect (the 4-to-5 lift). The classic failure this lesson discriminates
against is analysis versus summary versus paraphrase, then effect-stated versus significance-reached.

Model = the modality-corrected 4-mechanism async sequence (clean annotated before/after ->
predict-the-fix with a reveal -> feedback on the student's OWN draft via the grader -> a
student-generated diagnosis modeled first on a flawed example). No passive-read messy think-aloud,
and no claim to SRSD's live-enacted effect size. Bank-partitioned transfer (Chopin narrative ->
weather explanatory). When quoting Chopin the lesson uses short verbatim phrases; the analysis is
in the author's own words. All slots map to native Timeback interactions.

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
            "Effect it has on the reader, and reach the Warrant (why that effect matters to the author's "
            "purpose). The Warrant is the scored top-band move. Traits: Evidence/Development + Organization."),
    acc_tags=["ACC.W.INFO.6", "ACC.W.ANALYSIS.1", "CCSS.RI.9-10.6", "CCSS.W.9-10.2"],
    provenance={"copyright": "own_authored", "authored": "2026-07-08",
                "mnemonic_status": "proposal",
                "council": "DI faultless clean worked example + define-before-use + faultless minimal pairs; "
                           "KH highest-load staging (pre-trained elements, worked->completion->independent, one "
                           "extra support rung); SRSD DEW as an explicit named strategy + self-check; TSIS "
                           "metacommentary (naming what a move DOES); the significance beat elevated to the "
                           "scored top-band move. Async clean model; SRSD's live effect size NOT claimed."},
    fade_ledger_moves=["device-effect-warrant", "significance-reach", "attributive-tag"],
    slots=[
        # ---------------- TEACH: define the words (summary/paraphrase/analysis/device/warrant) ----------------
        Slot("TEACH", "teach_card", "The words first: summary, paraphrase, analysis, device, warrant",
             body=("Three jobs sound alike but are graded very differently, so keep them straight. A summary is "
                   "a short retelling of WHAT a text says, in the order it says it. Paraphrase means re-saying "
                   "the same content in different words, still just WHAT it says. Analysis is a different job: "
                   "analysis means explaining HOW an author builds meaning and WHY a choice works on the reader, "
                   "not only what happened. Here is the trap that costs the most points: on an analysis task, an "
                   "accurate retelling still sits in the low band, because it never answers the real question, "
                   "what is the author DOING, and why. Two more words you will use all lesson. A rhetorical "
                   "device is a deliberate choice a writer makes to shape how a reader feels or thinks, for "
                   "example an image, a repeated word, a shift in tone, or a moment of irony. A warrant means "
                   "your reasoning that ties the choice to its purpose: how you know the effect is real and why "
                   "it matters. Goal today: move past summary and paraphrase into analysis that names a device "
                   "and reaches its warrant.")),
        Slot("TEACH", "teach_card", "The DEW cue: each letter, with a right and a wrong example",
             body=("DEW is our cue for the analytical move, one job per letter. D = Device: name the specific "
                   "choice the author makes, one rhetorical device you can point to. Right: 'Chopin clusters "
                   "spring imagery at the window.' Wrong (too vague): 'Chopin uses good description,' which names "
                   "no specific choice. E = Effect: say what that choice does to the reader. Right: 'the images "
                   "tilt a scene of grief toward renewal.' Wrong (a label, not an effect): 'this is imagery,' "
                   "which spots a device but never says what it does. W = Warrant: reach the significance, why "
                   "that effect serves the author's purpose and how you know. Right: 'that early hint of renewal "
                   "is why her later whisper of freedom lands as discovery, not shock.' Wrong (stops at effect): "
                   "'it makes the scene feel hopeful,' which states an effect but never says why it matters. Hold "
                   "onto this: most writers stop at E and stall in the middle band. Reaching the W, the warrant, "
                   "is the move that lifts a response into the top band. That significance beat is the one thing "
                   "separating a solid response from an insightful one.")),
        Slot("TEACH", "stimulus_display", "Read the source: Kate Chopin, \"The Story of an Hour\" (1894)",
             ref="ACC-W910-ANALYSIS-LESSON-HOUR", bank="story_of_an_hour",
             body=("Read this excerpt from Kate Chopin's 1894 story. It opens with Mrs. Mallard learning that "
                   "her husband has died in a railroad accident, then follows her alone in her room. Read it once "
                   "for what happens. Then read it again and pick ONE choice Chopin makes that you could analyze: "
                   "an image she lingers on, a moment of irony, or a repeated word. You will analyze that one "
                   "move, not the whole story. Read and note especially what Mrs. Mallard sees through the open "
                   "window and the word she begins to whisper. You only need to keep your chosen move in mind.")),

        # ---------------- MODEL: highest-load, kept LONGEST (clean annotated before/after) ----------------
        Slot("MODEL", "annotated_before_after", "Watch summary become analysis that reaches significance",
             bank="story_of_an_hour",
             body=("BEFORE (this is summary, not analysis): In this part of the story Mrs. Mallard sits in a "
                   "chair by an open window after she hears that her husband has died. She looks outside and sees "
                   "trees, sky, and rain, and she hears birds and a song in the distance. Chopin uses a lot of "
                   "nature description here before Mrs. Mallard starts to feel free. Why this fails as analysis: "
                   "every sentence retells WHAT the passage shows, or slaps a label on it ('a lot of nature "
                   "description'). It never says what the choice DOES to the reader or why it matters. That is "
                   "summary plus device-spotting, and it caps at the middle band. "
                   "AFTER (real DEW analysis, annotated): Chopin fills the view through the open window with signs "
                   "of life, the tops of trees 'all aquiver with the new spring life,' the 'delicious breath of "
                   "rain,' and 'patches of blue sky' opening in the clouds [DEVICE: a cluster of spring and "
                   "renewal imagery, placed at the window in the exact moment of grief]. Because these images "
                   "press in right where a reader expects mourning, they tilt the scene toward life and "
                   "possibility instead of loss [EFFECT: the reader starts to feel renewal gathering around her "
                   "before she names it]. That matters because Chopin needs us to sense Mrs. Mallard's coming "
                   "freedom before she will admit it herself, so when the whispered 'free, free, free' arrives it "
                   "reads as something we have already half-felt, which is what makes the story's central irony, "
                   "that news of a death is what frees her, land as a discovery rather than a mere announcement "
                   "[WARRANT: why the effect serves Chopin's purpose, the significance]. "
                   "Notice the AFTER moves Device to Effect to Warrant and does not stop until it reaches why the "
                   "move matters. That last sentence, the significance, is what separates top-band analysis from "
                   "a competent effect statement.")),
        Slot("MODEL", "predict_the_fix", "Predict: is this analysis, and if not, what fixes it?",
             bank="story_of_an_hour",
             body=("Diagnose this draft before the reveal. A student wrote: 'Chopin repeats the word free near "
                   "the end. This is a powerful moment. It shows Mrs. Mallard is happy now.' The draft names a "
                   "real device but stays at summary and labeling. Which single move would most improve it? "
                   "(A) explain what the repetition of 'free' DOES to the reader and why it matters to Chopin's "
                   "purpose, reaching effect and warrant  "
                   "(B) quote one more sentence from the story  "
                   "(C) name two more devices Chopin uses  "
                   "(D) make the sentences longer and more formal"),
             feedback=("Correct: A. The draft names a device (the repeated 'free') and gives a vague label ('a "
                       "powerful moment'), but it never says what the repetition DOES to the reader or WHY that "
                       "matters. That is summary plus device-spotting, not analysis. The fix reaches Effect and "
                       "Warrant: whispering 'free' over and over, under her breath and almost against her will, "
                       "lets the reader watch a feeling surface that Mrs. Mallard has not yet dared to claim "
                       "(Effect), and that slow surfacing matters because it makes her freedom feel discovered "
                       "rather than declared, which is what gives the story's irony its force (Warrant). A second "
                       "quote (B), more device names (C), or longer sentences (D) never fix analysis that stalls "
                       "at effect. Reaching significance is the move from E to W, the lift into the top band.")),

        # ---------------- SUPPORTED: EXTRA rung (TWO discriminations) then guided completion ----------------
        Slot("SUPPORTED", "discrimination", "Discriminate: analysis vs summary vs paraphrase (three-way, minimal pair)",
             ref="", labeled_grade_c=True, bank="story_of_an_hour",
             body=("Discriminate before you produce (a Grade-C move we label as a design bet, not a proven "
                   "ingredient). Here are four responses to the same moment, the view through the open window. "
                   "Which one ANALYZES, that is, names the imagery as a device, states its effect on the reader, "
                   "and reaches the warrant? "
                   "(A) Mrs. Mallard looks out the window and sees trees, rain, and blue sky, and hears a song.  "
                   "(B) Through the open window she notices signs of the season: budding trees, the smell of "
                   "rain, and gaps of blue in the clouds.  "
                   "(C) Chopin loads the window with spring imagery so a scene of grief starts to feel like "
                   "renewal, which primes the reader to accept her coming sense of freedom as natural rather than "
                   "shocking.  "
                   "(D) This is a beautiful, moving passage that I really enjoyed reading. "
                   "Correct: C. (A) is SUMMARY, it retells what she sees. (B) is PARAPHRASE, the same content in "
                   "new words. (D) is a personal reaction, not analysis. Only (C) names the device, states its "
                   "effect on the reader, and reaches the warrant.")),
        Slot("SUPPORTED", "discrimination", "Discriminate: effect stated vs significance reached (the 4-to-5 lift)",
             ref="", labeled_grade_c=True, bank="story_of_an_hour",
             body=("Second discrimination, the top-band boundary pair (still a labeled Grade-C design bet). All "
                   "four responses talk about the same spring imagery, but only one reaches the warrant. Which "
                   "response reaches SIGNIFICANCE rather than stopping at effect? "
                   "(A) The spring imagery makes the scene feel hopeful instead of sad.  "
                   "(B) The spring imagery makes the scene feel hopeful, and that early hopefulness lets the "
                   "reader feel Mrs. Mallard's liberation before she admits it, which is what makes the "
                   "death-frees-her irony land as discovery.  "
                   "(C) Chopin describes trees, rain, and blue sky outside the window.  "
                   "(D) Chopin uses imagery in this passage. "
                   "Correct: B. (A) states a real EFFECT but stops there, the middle band. (C) is SUMMARY and (D) "
                   "is device-spotting with no effect at all. Only (B) reaches the WARRANT, why the effect serves "
                   "Chopin's purpose. This is the exact move that lifts a mid-band response into the top band.")),
        Slot("SUPPORTED", "production_frq", "Completion: the device is given, you supply Effect + Warrant",
             ref="", bank="story_of_an_hour", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("Guided completion: the device is named for you, so you can spend your effort on the hard "
                   "part. DEVICE: Chopin shows Mrs. Mallard 'striving to beat it back with her will,' then, when "
                   "she gives in, whispering 'free, free, free' over and over under her breath. In TWO sentences, "
                   "supply the rest of DEW. Sentence one: state the EFFECT this struggle-then-surrender has on the "
                   "reader. Sentence two: reach the WARRANT, why that effect matters to Chopin's purpose in "
                   "showing a woman discovering, against her own will, that she feels freed. Product goal: "
                   "sentence one names an effect on the reader (not a retelling), and sentence two says why it "
                   "matters to the author's purpose. Do not restate what the passage says; explain what it does "
                   "and why it matters.")),
        Slot("MODEL", "diagnosis_frq", "Diagnose with the DEW checklist: effect, or significance?",
             ref="", bank="story_of_an_hour", scored=True,
             body=("First watch the check run on a flawed draft, then run the same checklist on your own "
                   "response. Flawed draft: 'Chopin uses imagery of spring. This makes the passage feel hopeful.' "
                   "Run the DEW self-check, step by step. Step 1, D: did the writer name a specific device? "
                   "Partly, 'imagery of spring' is named but not pinned to a spot in the text, so the repair is "
                   "to point to the exact image. Step 2, E: did the writer state an effect on the reader? Yes, "
                   "'feel hopeful,' so E is met. Step 3, W: did the writer reach significance, why that effect "
                   "matters to the author's purpose? No, it stops at effect, so this draft stalls in the middle "
                   "band and needs a warrant. Now you: run the same three-item checklist on your current "
                   "response. In two or three sentences, name the exact sentence where you move from Device to "
                   "Effect to Warrant, or name the spot where your analysis stalled at effect and say what "
                   "warrant would finish it. Frame you may use: 'This choice matters to the author's purpose "
                   "because ____.'")),

        # ---------------- INDEPENDENT: full DEW analysis on the Chopin text (AUTHORED, not a bound CR item) --------
        Slot("INDEPENDENT", "production_frq", "Full DEW analysis of the Chopin excerpt (authored prompt)",
             ref="", bank="story_of_an_hour", rubric_ref="rc.ohio", scored=True, unit="paragraph",
             body=("Independent performance, self-contained. Choose ONE of Chopin's choices in the excerpt: the "
                   "open-window imagery, the irony of Mrs. Mallard's reaction to the news, the repetition of "
                   "'free,' or the shift in how her face and eyes are described (from 'a dull stare' to eyes that "
                   "'stayed keen and bright'). Write one analytical paragraph that runs the full DEW move. "
                   "Product goal, all three required: (1) DEVICE, name the specific choice and point to short "
                   "evidence from the text; (2) EFFECT, explain what that choice does to the reader; (3) WARRANT, "
                   "reach the significance, why that choice matters to how Chopin develops Mrs. Mallard's response "
                   "to the news. Then check your own paragraph against the three DEW items: if you stopped at "
                   "Effect, add a sentence beginning 'This matters to Chopin's purpose because ____.' until you "
                   "reach the Warrant. Do not summarize the plot. Scored on Evidence/Development and "
                   "Organization; the warrant, the significance beat, is the top-band move.")),

        # ---------------- TRANSFER: same DEW move, DIFFERENT author + genre, partitioned content bank ------------
        Slot("TRANSFER", "production_frq", "Analyze a DIFFERENT author's move (weather explanatory, partitioned)",
             ref="ACC-W910-INFO-LESSON-WEATHER", bank="weather_science", rubric_ref="rc.mcas", scored=True, unit="paragraph",
             body=("Transfer to a text you have not practiced on, in a different genre. The article 'How a "
                   "Weather Forecast Is Made' is not a story; it explains a process. Here the author's choices are "
                   "about STRUCTURE and SEQUENCE, not imagery. Analyze ONE such choice, for example the decision "
                   "to open by calling forecasts 'so ordinary that most people barely notice them' before "
                   "revealing the science behind them, or the choice to present the whole system as a single "
                   "chain that runs 'from a balloon drifting through the sky to an alert buzzing on a phone.' Run "
                   "the full DEW move: name the DEVICE (the structural or wording choice) with short evidence, "
                   "state its EFFECT on the reader, and reach the WARRANT, why that choice serves the author's "
                   "purpose of making a complex system feel clear and trustworthy. Product goal, all three "
                   "required: a named structural device with evidence, an effect on the reader, and a warrant "
                   "that reaches significance. Same analytical move as the story; new author, new genre. Scored "
                   "on Evidence/Development and Organization.")),
    ],
)

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
