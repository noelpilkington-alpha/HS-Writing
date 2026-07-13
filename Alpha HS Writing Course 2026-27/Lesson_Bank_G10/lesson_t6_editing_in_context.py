"""
lesson_t6_editing_in_context.py  -  G10 model lesson, TYPE 6: EDITING-IN-CONTEXT (SR / spacing vehicle).

FULLY CRAFTED to the 17-gate DI bar (copies the T1 precedent moves). Assembles a Timeback assessment-test
(ordered item sequence) that instantiates the council-adjudicated Type-6 shell against the REAL G10 banks.
This is the LOWEST-load type and the spaced-retrieval vehicle: the sentence moves taught in Types 1-5
(sentence boundaries, because/but/so, appositives, sentence-combining, precise word choice) recur here as
in-context editing, from the SAME passage. Fix mechanics/conventions AND style, select-then-produce, meaning
preserved.

Four DI fixes now enforced as gates, applied to Type-6 content:
  1. DEFINE-BEFORE-USE: a second TEACH card defines every convention term the lesson uses (complete sentence,
     fragment, run-on, comma splice, modifier, appositive) in plain words + a definitional cue, BEFORE any
     item asks the student to name or repair that error. Naming the error type IS the Pinpoint step of SPOT.
  2. CONTENT DEPTH (no blueprint stubs): the annotated worked example is written out with a literal BEFORE and
     a literal AFTER inline; every choice item embeds (A)-(D) plus "Correct: X." with the reasoning; the SCR
     production prompts carry explicit product goals. No gestures at content.
  3. MODEL BEFORE REQUIRED: the diagnosis is MODELED on a flawed edit first (the SPOT check run step by step),
     then handed to the student as a numbered checklist on a self-contained sentence. No blank "diagnose it."
  4. NO AMBIGUOUS REFERENT / STATELESS: every item quotes its own sentence inline; nothing points at "the
     items above" or the student's earlier submission. Each production slot stands alone (QTI is stateless).

CONTAMINATION-FREE: binds ONLY LESSON-pool stimuli for passage context (a student never edits inside a
passage they are later tested on). Every selected-response practice and every discrimination is AUTHORED
INLINE (ref=""), because the real selected-response items are test-bank items and binding them would
reintroduce item-level reuse (learn on what you test on). INDEPENDENT + TRANSFER are authored SCR productions
(ref="", rc.staar).

Binds (LESSON-pool stimuli only, ids verified present):
  - stimulus  ACC-W910-INFO-LESSON-HIGHWAYS (Interstate Highway System, US-federal-sourced explanatory single)
        -> the same-passage editing context (TEACH display; every taught edit rides on this one passage)
  - stimulus  ACC-W910-INFO-LESSON-WEATHER (NWS forecasting explanatory single)
        -> the bank-partitioned TRANSFER passage

Mnemonic SPOT (proposal, NOT sourced): Scan, Pinpoint (error type), Options, Test (the fix corrects the
error AND preserves the meaning). Two tiers: a mechanics tier ("is it correct?") and, above it, a STYLE tier
(gap #43: "is it precise / varied / register-appropriate?"). SCR modifier-repair short production (gap #21).

Honesty flag: this type's evidence base is sentence-combining (about 0.50) plus grammar-in-context (TWR),
NOT the SRSD strategy effect. It is the LEAST SRSD-suited type; no SRSD effect size is claimed for it. Hard
constraint (TWR + W&H): NO isolated grammar (isolated-grammar effect is slightly negative); every item rides
on the same passage and mirrors a taught sentence move. Select THEN produce.

Model = the modality-corrected sequence: clean annotated before/after (a fix that CHANGES meaning vs a fix
that corrects the error AND preserves meaning, the SPOT "Test" step) -> predict-the-fix (student picks the
meaning-preserving edit before the reveal) -> student-generated diagnosis. Bank-partitioned transfer
(highways -> weather). All slots map to native Timeback interactions.

Runs the QC harness on execution and prints PASS/FAIL. Dependency-free (stdlib + lesson_contract).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report

LESSON = Lesson(
    id="ACC-W910-L-T6-EDITING-0001", grade="9-10", lesson_type=6,
    unit="G10 U6 - Editing in context (conventions + style; spaced-retrieval vehicle)",
    title="Fix It Without Breaking It: Editing in Context (SPOT)",
    target=("Fix mechanics/conventions AND style IN CONTEXT: select the edit that corrects the error and "
            "preserves the writer's meaning, then produce the repair yourself. Items come from the SAME "
            "passage and mirror the taught sentence moves. Trait: Conventions/Language."),
    acc_tags=["ACC.W.CONV.1", "ACC.W.CONV.2", "ACC.W.CONV.3", "CCSS.L.9-10.1", "CCSS.L.9-10.3"],
    provenance={"copyright": "own_authored", "authored": "2026-07-08", "mnemonic_status": "proposal"},
    fade_ledger_moves=["sentence-boundary", "because/but/so", "appositive", "sentence-combining",
                       "word-choice-precision"],
    slots=[
        # ---------------- TEACH: SPOT (mechanics tier THEN style tier) + honesty flag + no-isolated-grammar --
        Slot("TEACH", "teach_card", "SPOT: the two-tier editing routine + why it rides on real writing",
             body=("Editing is not hunting for red marks at random. It is a routine you can run on any "
                   "sentence, so we give it a cue. SPOT stands for four steps: Scan the sentence, Pinpoint the "
                   "error type, weigh your Options, and Test the fix. The Test step is the one that matters "
                   "most: a fix has to do TWO things at once. It has to correct the error AND keep the meaning "
                   "the writer intended. A change that fixes the grammar but quietly says something different "
                   "is not a fix, it is a new error. "
                   "SPOT works on two tiers. First the mechanics tier, which asks: is it correct? (a complete "
                   "sentence, not a fragment or a run-on; the modifier next to the right word; the punctuation "
                   "doing its job). Then, once it is correct, the style tier, which asks: is it precise, is it "
                   "varied, is it right for a formal report? A sentence can be perfectly correct and still be "
                   "vague or clunky, and the style tier is where you sharpen it. Fix the mechanics first, then "
                   "raise the style. "
                   "Honesty about the evidence here: this lesson is NOT built on the SRSD strategy-writing "
                   "result, and it does not borrow that strength. Its support comes from sentence-combining "
                   "work (about a 0.50 effect) and from teaching grammar inside real writing rather than on "
                   "worksheets. That is also the hard rule for this whole lesson: no isolated grammar drills. "
                   "Grammar taught apart from writing actually tests slightly negative, so every item you edit "
                   "today lives inside one real passage and mirrors a sentence move you have already met.")),
        Slot("TEACH", "teach_card", "The words editors use (learn these before you Pinpoint)",
             body=("Before you can Pinpoint an error, you have to be able to name it, so learn these terms "
                   "first. A COMPLETE SENTENCE is a group of words with a subject and a verb that can stand on "
                   "its own (example: 'Congress passed the act.'). A FRAGMENT is a piece of a sentence that has "
                   "been cut off from the words it needs, so it cannot stand on its own (example: 'Because the "
                   "fuel tax paid for it.'). A RUN-ON is when two complete sentences are jammed together with "
                   "no punctuation between them (example: 'The system runs 48,890 miles it reaches every large "
                   "city.'). A COMMA SPLICE is when two complete sentences are joined with only a comma, which "
                   "is too weak to hold them (example: 'The states paid part, the federal government paid the "
                   "rest.'). A MODIFIER is a word or phrase that describes something else in the sentence; a "
                   "misplaced modifier sits next to the wrong word, so it seems to describe the wrong thing "
                   "(example: 'Stretching across rivers, the engineers worked' sounds like the engineers "
                   "stretch across rivers). An APPOSITIVE is a noun phrase that renames the noun right before "
                   "it, set off with commas (example: 'the Highway Trust Fund, a special account, paid the "
                   "bills'). The cue for the Pinpoint step: say the error's name out loud, because you repair a "
                   "run-on differently than a comma splice or a misplaced modifier.")),
        Slot("TEACH", "stimulus_display", "Read the passage you will edit (interstate highways)",
             ref="ACC-W910-INFO-LESSON-HIGHWAYS", bank="interstate_highways",
             body=("Read the interstate-highway passage once. This is the single passage every taught edit "
                   "today comes from. It explains how the system began in 1956, how large it grew (about "
                   "48,890 miles), how a fuel tax and a federal-state partnership paid for it, and what it does "
                   "for daily life. As you read, note the kinds of sentences it uses (cause-and-effect hinges, "
                   "added detail, combined clauses); those are the moves you will Scan for. The passage stays "
                   "on screen while you work.")),
        Slot("TEACH", "discrimination", "Pinpoint the error type (the P in SPOT)",
             ref="", labeled_grade_c=True, bank="interstate_highways",
             body=("Warm up the Pinpoint step (a labeled Grade-C discriminate-before-produce move: naming the "
                   "error before you fix it). Read this draft sentence built from the passage: 'The interstate "
                   "system began in 1956 it grew to about 48,890 miles.' What kind of error is it? "
                   "(A) a fragment, because it cannot stand on its own  "
                   "(B) a run-on, because two complete sentences are jammed together with no boundary  "
                   "(C) a misplaced modifier, because a describing phrase sits next to the wrong word  "
                   "(D) no error, the sentence is already correct. "
                   "Correct: B. Both 'The interstate system began in 1956' and 'it grew to about 48,890 miles' "
                   "are complete sentences, and nothing separates them, so it is a run-on. Naming the type is "
                   "the Pinpoint step, and it decides the fix: a run-on needs a real boundary, not just a "
                   "comma.")),

        # ---------------- MODEL: annotated BEFORE/AFTER (the SPOT Test step) -> predict-the-fix ------------
        Slot("MODEL", "annotated_before_after", "The Test step: a fix that breaks meaning vs a fix that keeps it",
             bank="interstate_highways",
             body=("Watch the SPOT Test step decide between two edits of one flawed sentence about the passage. "
                   "BEFORE (flawed, a comma splice: two complete sentences joined by only a comma): 'Because "
                   "the federal government paid 90 percent of the cost, the states could afford the work, this "
                   "let construction spread across the whole country.' "
                   "A FIX THAT CHANGES THE MEANING (reject this one): 'Because the federal government paid 90 "
                   "percent of the cost, the states could afford the work. This let construction spread across "
                   "the whole country.' The period is correct grammar, but it quietly severs the writer's "
                   "chain: 'the states could afford the work' is no longer presented as the thing that let "
                   "construction spread, just a stray fact set beside it [annotate: correct grammar, WRONG "
                   "meaning, the because-chain is cut]. "
                   "AFTER (the fix that corrects the error AND preserves the meaning): 'Because the federal "
                   "government paid 90 percent of the cost, the states could afford the work, which let "
                   "construction spread across the whole country.' Replacing the splice with 'which' repairs "
                   "the boundary AND keeps the single cause-and-effect chain the writer built [annotate: "
                   "correct grammar AND meaning preserved]. "
                   "That contrast IS the Test step: both edits are grammatical, only the AFTER version passes, "
                   "because only it keeps the meaning.")),
        Slot("MODEL", "predict_the_fix", "Predict which edit preserves the meaning",
             bank="interstate_highways",
             body=("Run SPOT yourself before the reveal. A draft sentence reads: 'The interstates are a small "
                   "fraction of the nation's roads, they carry about a quarter of its traffic.' (a comma splice "
                   "again). Which single edit corrects the boundary AND preserves the writer's contrast between "
                   "how LITTLE of the network the interstates are and how MUCH of the traffic they carry? "
                   "(A) 'The interstates are a small fraction of the nation's roads, but they carry about a "
                   "quarter of its traffic.'  "
                   "(B) 'The interstates are a small fraction of the nation's roads because they carry about a "
                   "quarter of its traffic.'  "
                   "(C) 'The interstates are a small fraction of the nation's roads they carry about a quarter "
                   "of its traffic.'  "
                   "(D) 'The interstates are a small fraction of the nation's roads; they carry about a "
                   "quarter, of its traffic.'"),
             feedback=("Correct: A. The two clauses contrast (a small share of the roads, yet a large share of "
                       "the traffic), so the coordinating conjunction 'but' both repairs the comma splice and "
                       "keeps that contrast, which is exactly the meaning-preservation half of the Test step. "
                       "B is grammatical but changes the meaning: 'because' invents a cause the writer never "
                       "claimed. C leaves a run-on (no boundary at all). D adds a stray comma inside the second "
                       "clause and scrambles the sense. Correct AND meaning-preserving is the bar, not correct "
                       "alone.")),

        # ---------------- SUPPORTED: discrimination FIRST (Grade-C, labeled, INLINE), then in-context selects ----
        Slot("SUPPORTED", "discrimination", "Meaning preserved vs meaning changed (modifier minimal set)",
             ref="", labeled_grade_c=True, bank="interstate_highways",
             body=("Discriminate before you produce (a labeled Grade-C design bet: recognition before "
                   "production, not a proven result, A/B-flagged). Here is a flawed sentence with a misplaced "
                   "modifier: 'Stretching across mountains and rivers, engineers built the interstates to "
                   "connect distant cities.' The opening phrase 'stretching across mountains and rivers' should "
                   "describe the roads, not the engineers. All four rewrites are grammatical. Pick the ONE that "
                   "repairs the modifier AND preserves the intended meaning (the roads stretch across the "
                   "terrain; the point is that they connect distant cities): "
                   "(A) 'Stretching across mountains and rivers, the interstates that engineers built connect "
                   "distant cities.'  "
                   "(B) 'Stretching across mountains and rivers, engineers connected distant cities as they "
                   "built the interstates.'  "
                   "(C) 'Engineers, stretching across mountains and rivers, built the interstates to connect "
                   "distant cities.'  "
                   "(D) 'The interstates stretch across mountains and rivers, engineers built them to connect "
                   "distant cities.' "
                   "Correct: A. Only A puts the roads right after the opening phrase (so the roads, not the "
                   "engineers, do the stretching) and keeps the main point that the roads connect cities. B "
                   "fixes the grammar but shifts the meaning: now the engineers do the connecting, not the "
                   "roads. C still attaches the phrase to 'Engineers,' so the modifier is still misplaced. D "
                   "repairs the modifier but trades in a comma splice, swapping one error for another.")),
        Slot("SUPPORTED", "sr_practice", "In-context select: conventions (NO CHANGE is an option)",
             ref="", bank="interstate_highways",
             body=("Now select in context (the mechanics tier of SPOT). In the passage sentence 'The federal "
                   "money came mostly from a tax on gasoline and diesel fuel,' choose the best edit for the "
                   "phrase 'gasoline and diesel fuel': "
                   "(A) NO CHANGE  "
                   "(B) gasoline, and diesel fuel  "
                   "(C) gasoline and diesel, fuel  "
                   "(D) gasoline; and diesel fuel  "
                   "Correct: A. The phrase is a simple two-item list joined by 'and,' so no comma or semicolon "
                   "belongs inside it. B splits the two items with a needless comma, C drops a comma into the "
                   "middle of one item ('diesel fuel'), and D uses a semicolon where nothing is being "
                   "separated. NO CHANGE can be the right answer: do not fix what is not broken.")),
        Slot("SUPPORTED", "sr_practice", "In-context select: sentence boundary (fragment / run-on)",
             ref="", bank="interstate_highways",
             body=("Pinpoint the boundary first (sentence boundaries are the error most likely to sink a "
                   "conventions score). Select the edit that turns this run-on into one complete, correctly "
                   "bounded sentence WITHOUT changing the writer's meaning: 'The system runs about 48,890 miles "
                   "it reaches nearly every large city in the country.' "
                   "(A) miles, it reaches  "
                   "(B) miles and reaches  "
                   "(C) miles, reaching  "
                   "(D) miles it, reaches  "
                   "Correct: B. 'and reaches' joins the two facts into one clean sentence and keeps both as "
                   "equal points (the length AND the reach). A only swaps the run-on for a comma splice (a "
                   "comma is too weak to join two complete sentences). D leaves the run-on and adds a stray "
                   "comma. C ('miles, reaching') is grammatical but demotes the second fact into an "
                   "afterthought, so B preserves the meaning best.")),
        Slot("SUPPORTED", "sr_practice", "In-context select: the STYLE tier (precise / register-appropriate)",
             ref="", bank="interstate_highways",
             body=("This item is the STYLE tier, one step above mechanics (a design bet that style earns its "
                   "own tier, gap #43). The sentence 'The project was really big and cost a lot of money' is "
                   "already grammatically correct; your job is to choose the most precise, formal rewrite for "
                   "an informational report: "
                   "(A) The project was really big and cost a ton.  "
                   "(B) The project was enormous in scale and cost about 114 billion dollars.  "
                   "(C) The project was pretty huge and super expensive.  "
                   "(D) The project was big money.  "
                   "Correct: B. B replaces the vague words ('really big,' 'a lot of money') with a precise "
                   "scale and the actual figure from the passage, in formal register. A and C stay casual and "
                   "vague ('a ton,' 'super expensive'), and D is an informal idiom that drops the meaning "
                   "almost entirely. Style still passes the Test step: the better wording sharpens the meaning, "
                   "it does not drift from it.")),
        Slot("MODEL", "diagnosis_frq", "Diagnose an edit with the SPOT checklist (modeled, then you)",
             bank="interstate_highways", scored=True,
             body=("First watch the check run on a flawed edit, then run the same check yourself. A writer "
                   "tried to fix this run-on from a highway draft: 'Trucks carry goods across state lines they "
                   "use the interstates to do it.' The attempted fix was: 'Trucks carry goods across state "
                   "lines, they use the interstates to do it.' Run the SPOT check step by step. Step 1, Scan "
                   "and Pinpoint: what is the error type? A run-on, two complete sentences with no real "
                   "boundary. Step 2, does the fix correct the error? No: a comma alone cannot join two "
                   "complete sentences, so the fix only turned a run-on into a comma splice, and the error is "
                   "not repaired. Step 3, does it preserve the meaning? The meaning survives, but the error "
                   "does not, and a fix has to pass BOTH halves of the Test step. Now you: write ONE better fix "
                   "for that same sentence, then run this checklist on your fix and answer all three in two or "
                   "three sentences. Checklist: (1) Which error type did I Pinpoint? (2) Does my fix correct "
                   "the error with a real boundary, not just a comma? (3) Does my fix keep the writer's meaning, "
                   "or did it quietly change who does what? Scored on Conventions.")),

        # ---------------- INDEPENDENT: STAAR SCR short production (revise, keep the meaning) ----------------
        Slot("INDEPENDENT", "production_frq", "Short revision: fix the modifier, keep the meaning (highways)",
             ref="", bank="interstate_highways", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("Independent performance (a STAAR short-constructed-response: a short, focused revision, not "
                   "a full essay). Here is a flawed sentence about the highway passage: 'Signed into law in "
                   "1956, the country began building a connected network of high-speed roads.' The opening "
                   "phrase 'Signed into law in 1956' is a misplaced modifier: it should describe the ACT that "
                   "was signed, not 'the country' (the country was not signed into law). Rewrite the sentence "
                   "so the opening phrase attaches to the right word AND the writer's meaning is preserved. Run "
                   "SPOT: Scan, Pinpoint the error type, weigh your Options, and Test that your fix corrects "
                   "the error and keeps the meaning. Product goal: (1) the opening phrase clearly describes the "
                   "1956 act, (2) the sentence is complete and correctly bounded, (3) the original meaning (a "
                   "1956 law started the roadbuilding) is unchanged, and (4) you change only what you must. "
                   "Scored on Conventions.")),

        # ---------------- TRANSFER: same move, bank-partitioned NEW passage (weather) -----------------
        Slot("TRANSFER", "production_frq", "Short revision on a NEW passage: fix the modifier, keep the meaning (weather)",
             ref="ACC-W910-INFO-LESSON-WEATHER", bank="weather_science", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("Transfer to a passage you have not edited (how the National Weather Service makes a "
                   "forecast, a different topic). A flawed draft sentence reads: 'Rising above 35 kilometers, "
                   "forecasters use weather balloons to measure the upper air.' The opening phrase 'Rising "
                   "above 35 kilometers' is a misplaced modifier: it should describe the BALLOON that rises, "
                   "not the forecasters. Rewrite the sentence so the opening phrase attaches to the right word "
                   "AND the writer's meaning is preserved. Run SPOT: Scan, Pinpoint the modifier, weigh your "
                   "Options, and Test that the fix keeps the meaning. Product goal: (1) the opening phrase "
                   "clearly describes the balloon, (2) the sentence stays complete and correctly bounded, (3) "
                   "the meaning (balloons rise high to measure the upper air) is unchanged, and (4) you change "
                   "only what you must. Scored on Conventions.")),
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
