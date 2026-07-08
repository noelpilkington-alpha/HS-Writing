"""
lesson_t6_editing_in_context.py  -  G10 model lesson, TYPE 6: EDITING-IN-CONTEXT (SR / spacing vehicle).

Assembles a Timeback assessment-test (ordered item sequence) that instantiates the council-adjudicated
Type-6 shell (G10_Model_Lesson_Specs.md) against the REAL G10 banks. This is the LOWEST-load type and the
spaced-retrieval vehicle: the sentence moves taught in Types 1-5 (sentence boundaries, because/but/so,
appositives, sentence-combining, precise word choice) recur here as in-context editing, from the SAME
passage. Fix mechanics/conventions AND style, select-then-produce, meaning preserved.

CONTAMINATION-FREE REBUILD: this lesson binds ONLY a LESSON-pool stimulus for the passage context, so a
student never edits inside the same passage they are later tested on. The old build bound a TEST-pool
explanatory single and four TEST selected-response items (conventions, sentence-boundary, language/style,
and modifier-repair); every one of those bindings is removed. The selected-response practice selects and the
discrimination are AUTHORED INLINE (ref=""), because the real selected-response items are test-bank items and
binding them would reintroduce item-level reuse (learn on what you test on).

Binds (LESSON-pool stimuli only, ids verified present):
  - stimulus  ACC-W910-INFO-LESSON-HIGHWAYS (Interstate Highway System, US-federal-sourced explanatory single)
        -> the same-passage editing context (TEACH display; every edit rides on this one passage)
  - stimulus  ACC-W910-INFO-LESSON-WEATHER (NWS forecasting explanatory single)
        -> the bank-partitioned TRANSFER passage

Mnemonic SPOT (proposal, NOT sourced): Scan, Pinpoint (error type), Options, Test (the fix corrects the
error AND preserves the meaning). Two tiers: a mechanics tier ("is it correct?") and, above it, a STYLE tier
(gap #43: "is it precise / varied / register-appropriate?"). SCR modifier-repair sub-type (gap #21).

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
        # ---------------- TEACH: SPOT cue (mechanics tier THEN style tier) + honesty flag + the passage ----
        Slot("TEACH", "teach_card", "SPOT: the two-tier editing routine + why it rides on real writing",
             body=("Editing is not hunting for red marks at random. It is a routine you can run on any "
                   "sentence, so we give it a cue: SPOT. Scan the sentence, Pinpoint the error type, weigh "
                   "your Options, and Test the fix. The Test step is the one that matters most: a fix has to "
                   "do TWO things at once. It has to correct the error AND keep the meaning the writer "
                   "intended. A change that fixes the grammar but quietly says something different is not a "
                   "fix, it is a new error. "
                   "SPOT works on two tiers. First the mechanics tier: is it correct? (a complete sentence, "
                   "not a fragment or a run-on; the modifier attached to the right word; the punctuation "
                   "doing its job). Then, once it is correct, the style tier: is it precise, is it varied, is "
                   "it right for a formal report? A sentence can be perfectly correct and still be vague or "
                   "clunky, and the style tier is where you sharpen it. "
                   "Honesty about the evidence here: this lesson is NOT built on a strategy-writing result. "
                   "Its support comes from sentence-combining work (about a 0.50 effect) and from teaching "
                   "grammar inside real writing rather than on worksheets. That is also the hard rule for "
                   "this whole lesson: no isolated grammar drills. Isolated grammar taught apart from writing "
                   "actually tests slightly negative, so every item you edit today lives inside one real "
                   "passage and mirrors a sentence move you have already met.")),
        Slot("TEACH", "stimulus_display", "Read the passage you will edit (interstate highways)",
             ref="ACC-W910-INFO-LESSON-HIGHWAYS", bank="interstate_highways",
             body=("Read the interstate-highway passage once. This is the single passage every edit today "
                   "comes from. It explains how the Interstate Highway System began in 1956, how large it grew "
                   "(about 48,890 miles), how a fuel tax and a federal-state partnership paid for it, and what "
                   "it does for daily life. As you read, notice the kinds of sentences it uses (cause-and-"
                   "effect hinges, added detail, combined clauses); those are the moves you will scan for.")),

        # ---------------- MODEL: annotated before/after (the SPOT Test step) -> predict-the-fix -----------
        Slot("MODEL", "annotated_before_after", "The Test step: a fix that breaks meaning vs a fix that keeps it",
             bank="interstate_highways",
             body=("Watch the SPOT Test step decide between two edits of one flawed sentence from a draft "
                   "about the passage. "
                   "FLAWED: 'Because the federal government paid 90 percent of the cost, the states could "
                   "afford the work, this let construction spread across the whole country.' (a comma splice "
                   "joins two full clauses). "
                   "FIX THAT CHANGES THE MEANING (reject): 'Because the federal government paid 90 percent of "
                   "the cost, the states could afford the work. This let construction spread across the whole "
                   "country.' Splitting after 'work' is punctuated correctly, but it quietly drops the writer's "
                   "chain: the states being able to afford the work is no longer presented as what let "
                   "construction spread, just a separate fact [annotate: correct grammar, WRONG meaning, the "
                   "because-chain is severed]. "
                   "FIX THAT KEEPS THE MEANING (accept): 'Because the federal government paid 90 percent of the "
                   "cost, the states could afford the work, which let construction spread across the whole "
                   "country.' Replacing the splice with 'which' fixes the boundary AND preserves the single "
                   "cause-and-effect chain the writer built [annotate: correct grammar AND meaning preserved, "
                   "the because/so relationship survives]. "
                   "That contrast IS the Test step: both options are grammatical, only one passes because "
                   "only one keeps the meaning.")),
        Slot("MODEL", "predict_the_fix", "Predict which edit preserves the meaning",
             bank="interstate_highways",
             body=("Run SPOT yourself before the reveal. A draft sentence reads: 'The interstates are a small "
                   "fraction of the nation's roads, they carry about a quarter of its traffic.' (a comma splice "
                   "again). Which single edit corrects the boundary AND preserves the writer's contrast between "
                   "how LITTLE of the network the interstates are and how MUCH of the traffic they carry? "
                   "(A) 'The interstates are a small fraction of the nation's roads, but they carry about a "
                   "quarter of its traffic.' "
                   "(B) 'The interstates are a small fraction of the nation's roads because they carry about a "
                   "quarter of its traffic.' "
                   "(C) 'The interstates are a small fraction of the nation's roads they carry about a quarter "
                   "of its traffic.' "
                   "(D) 'The interstates are a small fraction of the nation's roads; they carry about a "
                   "quarter, of its traffic.'"),
             feedback=("A is the fix. The two clauses contrast (a small share of the roads, yet a large share "
                       "of the traffic), so the coordinating conjunction 'but' both repairs the splice and "
                       "keeps that contrast, which is exactly the meaning-preservation half of the Test step. "
                       "B is grammatical but changes the meaning: 'because' invents a cause the writer never "
                       "claimed. C leaves a run-on (no boundary at all). D adds a stray comma inside the second "
                       "clause and scrambles the sense. Correct AND meaning-preserving is the bar, not correct "
                       "alone.")),

        # ---------------- SUPPORTED: discrimination FIRST (Grade-C, labeled, INLINE), then in-context selects ------
        Slot("SUPPORTED", "discrimination", "Meaning preserved vs meaning changed (modifier minimal pair)",
             ref="", labeled_grade_c=True, bank="interstate_highways",
             body=("Design-bet step (discriminate before you produce; this recognition-before-production move "
                   "is a labeled Grade-C design bet, not a proven result, and is A/B-flagged). Here is a flawed "
                   "sentence with a misplaced modifier: 'Stretching across mountains and rivers, engineers "
                   "built the interstates to connect distant cities.' The opening phrase should describe the "
                   "roads, not the engineers. Two rewrites both read smoothly: "
                   "(A) 'Stretching across mountains and rivers, the interstates that engineers built connect "
                   "distant cities.' "
                   "(B) 'Stretching across mountains and rivers, engineers connected distant cities as they "
                   "built the interstates.' "
                   "Pick the rewrite that repairs the modifier AND preserves the intended meaning (the roads "
                   "stretch across the terrain, and the point is that they connect cities), not the one that "
                   "fixes the grammar while shifting who or what does what. The two options differ on exactly "
                   "that one dimension.")),
        Slot("SUPPORTED", "sr_practice", "In-context select: conventions (NO-CHANGE is an option)",
             ref="", bank="interstate_highways",
             body=("Now select in context. In the passage sentence 'The federal money came mostly from a tax "
                   "on gasoline and diesel fuel,' choose the best edit for the underlined phrase 'gasoline and "
                   "diesel fuel.' "
                   "(A) NO CHANGE  "
                   "(B) gasoline, and diesel fuel  "
                   "(C) gasoline and diesel, fuel  "
                   "(D) gasoline; and diesel fuel  "
                   "Remember that NO CHANGE can be the right answer: do not fix what is not broken. This is the "
                   "mechanics tier of SPOT.")),
        Slot("SUPPORTED", "sr_practice", "In-context select: sentence boundary (fragment / run-on)",
             ref="", bank="interstate_highways",
             body=("Select the edit that turns this run-on into one complete, correctly bounded sentence "
                   "without changing the writer's meaning: 'The system runs about 48,890 miles it reaches "
                   "nearly every large city in the country.' "
                   "(A) miles, it reaches  "
                   "(B) miles and reaches  "
                   "(C) miles, reaching  "
                   "(D) miles it, reaches  "
                   "Sentence boundaries are the move most likely to sink the conventions score, so Pinpoint the "
                   "boundary first. (Both B and C are grammatical; choose the one that keeps the two facts in "
                   "one clean sentence and preserves the meaning.)")),
        Slot("SUPPORTED", "sr_practice", "In-context select: the STYLE tier (precise / register-appropriate)",
             ref="", bank="interstate_highways",
             body=("This item is the style tier, above mechanics (gap #43). The sentence 'The project was "
                   "really big and cost a lot of money' is already grammatically correct; your job is to choose "
                   "the most precise, formal-register rewrite for a report. "
                   "(A) The project was really big and cost a ton.  "
                   "(B) The project was enormous in scale and ran to about 114 billion dollars.  "
                   "(C) The project was pretty huge and super expensive.  "
                   "(D) The project was big money.  "
                   "Test it the same way: the better wording has to sharpen the meaning, not drift away from "
                   "it.")),
        Slot("MODEL", "diagnosis_frq", "Diagnose your own edit",
             bank="interstate_highways", scored=True,
             body=("In one or two sentences, diagnose your own work on the items above: which edit did you "
                   "pick, what error type did you Pinpoint, and how do you know your fix preserved the "
                   "writer's meaning rather than quietly changing it? Name the tier you were on (mechanics or "
                   "style).")),

        # ---------------- INDEPENDENT: the STAAR SCR short production (revise, keep the meaning) -----------
        Slot("INDEPENDENT", "production_frq", "SCR: revise the flawed sentence, keep the meaning (highways)",
             ref="", bank="interstate_highways", rubric_ref="rc.staar", scored=True,
             body=("Independent performance (STAAR short-constructed-response). Here is a flawed sentence "
                   "about the highway passage: 'Signed into law in 1956, the country began building a "
                   "connected network of high-speed roads.' The opening phrase does not attach to the right "
                   "word (the country was not signed into law; the act was). Rewrite the sentence so the "
                   "modifier attaches logically AND the intended meaning is preserved. Change only what you "
                   "must. Scored on Conventions.")),

        # ---------------- TRANSFER: same move, bank-partitioned NEW passage (weather) -----------------
        Slot("TRANSFER", "production_frq", "SCR transfer on a NEW passage: revise, keep the meaning (weather)",
             ref="ACC-W910-INFO-LESSON-WEATHER", bank="weather_science", rubric_ref="rc.staar", scored=True,
             body=("Transfer to a passage you have not edited (how the National Weather Service makes a "
                   "forecast, a different topic). A flawed draft sentence reads: 'Rising above 35 kilometers, "
                   "forecasters use weather balloons to measure the upper air.' The introductory phrase does "
                   "not describe the forecasters who follow it; it is the balloon that rises. Rewrite the "
                   "sentence so the opening phrase attaches to the right word AND the writer's meaning is "
                   "preserved. Run SPOT: Scan, Pinpoint the modifier, weigh Options, Test that the fix keeps "
                   "the meaning. Scored on Conventions.")),
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
