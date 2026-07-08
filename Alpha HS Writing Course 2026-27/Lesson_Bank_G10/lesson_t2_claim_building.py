"""
lesson_t2_claim_building.py  -  G10 model lesson, TYPE 2: CLAIM-BUILDING (moderate-load core component).

FULLY CRAFTED to the 17-gate DI bar via the Council of Writing Instruction (TSIS they-say/I-say + the three
stances; SRSD STAND as an explicit modeled strategy with a self-check; DI/Engelmann define-before-use +
faultless minimal pairs for arguable-claim vs fact vs opinion; Kirschner & Hendrick worked->completion->
independent fade for a moderate-load move), with a judge adjudication. Copies the T1 (source-reading) moves.

Solves the same four defects T1 had, now enforced as gates:
  1. DEFINE every technical term before use (define_before_use). TEACH card 1 defines, in plain words with a
     definitional cue: thesis, controlling idea, arguable claim, they-say, I-say, the three stances, the
     because/but/so hinge, and the 'so what' test. TEACH card 2 defines STAND letter by letter with a right
     AND a wrong example per letter (DI faultless communication at the strategy level).
  2. NO blueprint stubs (content_depth). Every teach card, the annotated before/after (a FACT-not-a-claim
     BEFORE -> an arguable stanced claim WITH a 'so what' stakes beat AFTER, STAND-annotated), the
     predict-the-fix (4 options + reveal in the feedback field), both discrimination items ((A)-(D) options +
     'Correct: X.' inline), the guided/independent/transfer prompts (frames + explicit product goals), and the
     scaffolded diagnosis are written out as real student-facing content.
  3. MODEL before you require a high-load move (model_before_required). The diagnosis is MODELED on a flawed
     claim first (a step-by-step 4-point check with repair frames), THEN the student runs the same checklist
     on a fresh claim of their own. No blank 'diagnose your own work.'
  4. NO ambiguous referents (no_ambiguous_reference). Distinct objects named distinctly; every 'this claim /
     this draft' shows its text inline (a quote, a BEFORE/AFTER, or an (A)-(D) option list).

Type-2 target: build a DEFENSIBLE thesis via they-say/I-say in three stances (agree / disagree /
agree-with-a-difference), where the 'I say' is a because/but/so completion (TWR) and the claim must pass the
'so what' stakes test (GAP #22). Discrimination is a TWO-part Grade-C move (labeled): a fact-vs-arguable-claim
-vs-ungrounded-opinion identify item in TEACH, then a GAP-#22 so-what minimal pair in SUPPORTED. The EG
unscored freewrite renders as a production_frq but is NOT scored (scored=False); grader_routing still requires
a valid rc.* on every production_frq, so it carries rubric_ref='rc.4trait' while the body states plainly that
it is an ungraded warm-up. It is placed AFTER a discrimination (allowed for claim-building) and is
self-contained (no prior-work reference).

Binds ONLY lesson-pool stimuli (contamination-free): longer_school_year (taught) -> congestion_pricing
(bank-partitioned transfer). Mnemonic STAND (proposal, not sourced). Async clean labeled model (SRSD's live
effect size is NOT claimed for the async modality). All slots map to native Timeback interactions. Runs the
QC harness on execution and prints PASS/FAIL. Dependency-free (stdlib + lesson_contract).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report

LESSON = Lesson(
    id="ACC-W910-L-T2-CLAIM-0001", grade="9-10", lesson_type=2,
    unit="G10 U1 - Source-based argument (claim-building)",
    title="Take a STAND: Build a Defensible Claim That Answers So What (STAND)",
    target=("Build a defensible thesis using they-say/I-say in three stances (agree, disagree, "
            "agree-with-a-difference): take a clear stance, make an arguable assertion the other side could "
            "reject, complete the 'I say' with a because/but/so hinge, and answer 'so what' by naming the "
            "stakes. Trait: Thesis/Purpose."),
    acc_tags=["ACC.W.ARG.1", "ACC.W.INFO.6", "CCSS.W.9-10.1", "CCSS.W.9-10.1b"],
    provenance={"copyright": "own_authored", "authored": "2026-07-08", "mnemonic_status": "proposal",
                "council": "Judge-adjudicated: SRSD STAND shell + self-check; TSIS they-say/I-say def + three "
                           "stances; DI define-before-use + faultless arguable/fact/opinion minimal pairs; KH "
                           "worked->completion->independent fade (moderate load). Async clean model (SRSD live "
                           "ES NOT claimed for the async modality)."},
    fade_ledger_moves=["because/but/so", "they-say/I-say", "so-what/stakes"],
    slots=[
        # ========== TEACH: define terms + STAND before use; read source; discriminate; freewrite ==========
        Slot("TEACH", "teach_card", "What a defensible claim is (thesis, they-say/I-say, the three stances)",
             body=("A thesis is a claim you can defend, also called the controlling idea, which means the one "
                   "point that everything else in your essay works to support. A thesis is not a fact you can "
                   "look up, and it is not an opinion no one can weigh. An arguable claim is a statement a "
                   "reasonable person on the other side could disagree with, and only an arguable claim can "
                   "anchor an argument. To build one, you first listen to the other side. The they-say means "
                   "the other side's position, that is, what someone who disagrees with you would actually say. "
                   "Your I-say means your own answer to that they-say. They-say/I-say gives you three stances "
                   "to choose from: you can agree, you can disagree, or you can agree with a difference (a "
                   "'yes, but' that accepts part of the other side and then adds your own point). You complete "
                   "the I-say with a because/but/so hinge, which means you attach your reason using the word "
                   "because, but, or so. Whichever stance you pick, a strong claim also passes the 'so what' "
                   "test, meaning it says why the answer matters, not just what you believe. Goal for today: "
                   "write a defensible claim that takes a stance and answers 'so what'.")),
        Slot("TEACH", "teach_card", "The STAND strategy: each letter, with a right and a wrong example",
             body=("STAND is our cue for building a defensible claim from a they-say/I-say. Each letter has one "
                   "job. "
                   "S = Stance: pick a clear side. Right: 'The US should adopt a longer school year.' Wrong (no "
                   "side): 'There are many views about the length of the school year.' "
                   "T = Territory: name the they-say you are answering, so your claim is a real reply and not a "
                   "random opinion. Right: answering the side that says more seat time is not the same as more "
                   "learning. Wrong: ignoring the other side and arguing into thin air. "
                   "A = Assertion: make a point the other side could reject. Right: 'a longer year would narrow "
                   "the gap between richer and poorer students.' Wrong (a fact no one argues): 'a school year "
                   "is about 180 days long.' "
                   "N = Nuance: leave room to agree with a difference when the other side has a fair point. "
                   "Right: 'Yes, more seat time alone is not more learning, but a longer year paired with "
                   "better teaching would help the students who slide back most.' Wrong: pretending the other "
                   "side has no point at all. "
                   "D = Defensible: back the claim with a reason and a stake, not just a feeling. Right: "
                   "'...because the summer slide widens the gap, which matters because schools then spend every "
                   "fall rebuilding it.' Wrong (bare feeling): 'because summer is boring anyway.' "
                   "Your goal: a claim that picks an S, states an A the other side could reject, and delivers a "
                   "D that answers 'so what'.")),
        Slot("TEACH", "stimulus_display", "Read the sources on a longer school year",
             ref="ACC-W910-ARG-OPP-LESSON-SCHOOLYEAR", bank="longer_school_year",
             body=("Read both sources on whether the United States should adopt a longer school year. One side "
                   "argues that more days would narrow the summer-slide gap; the other argues that more seat "
                   "time is not the same as more learning. Read and note, for each side, the they-say (the "
                   "position that side takes) so you have real territory to answer. Both sources stay on screen "
                   "while you work.")),
        Slot("TEACH", "discrimination", "Sort it: which one is the arguable claim? (fact vs claim vs opinion)",
             ref="", labeled_grade_c=True, bank="longer_school_year",
             body=("Design-bet step (discriminate before you produce, a Grade-C move we label as a bet, not "
                   "proof): only an arguable claim can anchor an essay. Which one below is the arguable claim? "
                   "(A) 'A typical American public school runs about 180 days each year.'  "
                   "(B) 'The United States should adopt a longer school year, because the long summer break "
                   "lets some students slide backward while wealthier peers keep learning.'  "
                   "(C) 'Summer break is just the best part of the whole year.'  "
                   "(D) 'Teachers are salaried professionals.'  "
                   "Correct: B. A and D are FACTS (checkable, no one on the other side argues them). C is an "
                   "UNGROUNDED OPINION (a preference with no reason anyone could weigh). Only B is an ARGUABLE "
                   "CLAIM: a reasonable person on the other side could reject it, so it can anchor an argument.")),
        Slot("TEACH", "production_frq", "Ungraded warm-up: what do you actually think?",
             ref="", bank="longer_school_year", rubric_ref="rc.4trait", scored=False,
             body=("Ungraded warm-up (this one is NOT scored, so write freely): before you study any models, "
                   "freewrite a short paragraph on the real question. What do you actually think about whether "
                   "the United States should adopt a longer school year, and why? Get your honest take onto the "
                   "page in your own words. There is no wrong answer here; next we will sharpen a take like "
                   "this into a defensible claim.")),

        # ========== MODEL: clean annotated before/after -> predict-the-fix (async mechanisms 1-2) ==========
        Slot("MODEL", "annotated_before_after", "Watch a fact become a defensible claim",
             bank="longer_school_year",
             body=("BEFORE (a fact, not a claim): 'A typical American public school runs about 180 days a "
                   "year.' Check it against STAND: it takes no Stance (it picks no side), it makes no Assertion "
                   "the other side could reject (no one argues that 180 is 180), and it answers no 'so what' "
                   "(it never says why the number matters). A fact can support a claim, but it cannot BE the "
                   "claim, because there is nothing there to argue. "
                   "AFTER (an arguable claim with stakes, annotated): 'The United States should adopt a longer "
                   "school year [Stance: picks a side and an Assertion the other side could reject], because a "
                   "calendar that sends students away for a long summer lets learning slide backward for the "
                   "children who can least afford tutoring or camps [because-hinge: the I-say reason], which "
                   "quietly widens the gap between richer and poorer students every fall instead of closing it "
                   "[so what: the stakes].' "
                   "Read the labels: the part that picks a side and states a rejectable point is the Stance and "
                   "Assertion (S and A); the clause beginning with 'because' is the I-say reason, the "
                   "because/but/so hinge; the clause beginning with 'which quietly widens' is the 'so what,' "
                   "the stakes. The AFTER can be argued and the BEFORE cannot: that is the whole difference "
                   "between a fact and a defensible claim.")),
        Slot("MODEL", "predict_the_fix", "Predict: why can this not be your thesis?",
             bank="longer_school_year",
             body=("Diagnose this draft before we reveal the fix. If this sentence were offered as a thesis, "
                   "what is its single biggest problem? "
                   "Draft: 'The summer break lasts about two to three months in most American schools.' "
                   "(A) it states a fact no one disputes, so there is no arguable stance to defend  "
                   "(B) it is too short to be a thesis  "
                   "(C) it does not name its source  "
                   "(D) it uses a number instead of spelling the words out"),
             feedback=("Correct: A. 'The summer break lasts about two to three months' is a checkable fact, and "
                       "a fact is not a claim: no one on the other side disagrees with it, so there is nothing "
                       "to argue. To turn it into a defensible thesis you add a Stance and an Assertion the "
                       "other side could reject ('the United States should adopt a longer school year'), attach "
                       "a because/but/so reason (the I-say), then answer 'so what' by naming the stakes (why "
                       "the length of the break matters). B, C, and D are traps: length, citation, and how you "
                       "write a number are not what makes a sentence arguable.")),

        # ========== SUPPORTED: GAP-#22 so-what minimal pair (Grade-C) -> guided completion production ==========
        Slot("SUPPORTED", "discrimination", "Claim with stakes vs claim without (the so-what minimal pair)",
             ref="", labeled_grade_c=True, bank="longer_school_year",
             body=("Design-bet step (labeled Grade-C): A and B are both arguable claims taking the same stance; "
                   "they differ on exactly ONE move, the 'so what.' Which one answers why it matters (the "
                   "stakes)? "
                   "(A) 'The United States should adopt a longer school year.'  "
                   "(B) 'The United States should adopt a longer school year, because the long summer break "
                   "lets low-income students lose ground while wealthier peers keep learning, widening the gap "
                   "the schools then spend every fall trying to rebuild.'  "
                   "(C) 'A school year is about 180 days long.'  "
                   "(D) 'I just think school should be longer, honestly.'  "
                   "Correct: B. A takes a Stance but stops there; it never says why the length matters. B "
                   "reaches the stakes, so it answers 'so what.' C is only a fact and D is only a bare opinion, "
                   "so neither is even a full arguable claim. Top-band rubrics reward the claim that reaches "
                   "significance, not the one that just restates the prompt.")),
        Slot("SUPPORTED", "production_frq", "Guided: write ONE defensible STAND claim (frame provided)",
             ref="", bank="longer_school_year", rubric_ref="rc.ohio", scored=True, unit="sentence",
             body=("Guided practice with a frame provided. Write ONE defensible claim on the longer-school-year "
                   "question. Fill in this frame, or write your own sentence that does the same jobs: 'The US "
                   "should ____ [Stance + an Assertion the other side could reject], because ____ [your I-say "
                   "reason, a because/but/so hinge drawn from the sources], which matters because ____ [so "
                   "what: the stakes].' Product goal, all four required: (1) pick a clear Stance (agree, "
                   "disagree, or agree-with-a-difference); (2) make an Assertion a reasonable reader could "
                   "reject; (3) attach a because/but/so reason taken from the sources; (4) name the stakes. "
                   "Scored on Thesis/Purpose.")),
        Slot("MODEL", "diagnosis_frq", "Diagnose a claim with the STAND self-check (modeled, then you)",
             ref="", bank="longer_school_year", scored=True,
             body=("First watch the 4-point check run on a flawed claim, then run the same checklist on a fresh "
                   "claim of your own. "
                   "Flawed claim: 'A longer school year would be good.' Run the check step by step. "
                   "Step 1, Stance: does it pick a clear side? Barely (good for whom?); sharpen it with the "
                   "frame 'The US should ____.'. "
                   "Step 2, Assertion: could a reasonable person on the other side reject it? Not really, "
                   "because 'good' is too vague to argue; make the point sharp enough to reject. "
                   "Step 3, I-say/because: is there a because/but/so reason? No; add one with the frame "
                   "'because ____.'. "
                   "Step 4, So what: does it name the stakes (why it matters)? No; add one with the frame "
                   "'which matters because ____.'. "
                   "Now you: write one fresh claim on the longer-school-year question in the box, then run the "
                   "same 4-point checklist on it. For each point you mark No, use the matching frame to repair "
                   "it. Finish by naming the STAND letters your claim delivers and the one it still needs.")),

        # ========== INDEPENDENT: full STAND claim + self-check on the current response ==========
        Slot("INDEPENDENT", "production_frq", "Write an independent STAND claim with stakes (no frame)",
             ref="", bank="longer_school_year", rubric_ref="rc.ohio", scored=True, unit="sentence",
             body=("Independent performance, no frame provided: on the longer-school-year question, write a "
                   "defensible thesis. Product goal, all four required: (1) take a clear Stance; (2) make an "
                   "Assertion the other side could reject; (3) attach your I-say reason with a because/but/so "
                   "hinge, drawn from the sources; (4) answer 'so what' with an explicit stakes beat that says "
                   "why the answer matters. Then run the STAND self-check on your claim: S, did I pick a side? "
                   "A, could a reasonable reader reject it? because, did I give a reason? so-what, did I name "
                   "why it matters? If you mark any No, revise before you submit. Scored on Thesis/Purpose.")),

        # ========== TRANSFER: same STAND move, bank-partitioned content ==========
        Slot("TRANSFER", "stimulus_display", "Read the sources on a NEW topic",
             ref="ACC-W910-ARG-OPP-LESSON-CONGESTION", bank="congestion_pricing",
             body=("Read this new pair of sources on whether cities should charge tolls to drive downtown "
                   "during the busiest hours (congestion pricing). Read and note, for each side, the they-say "
                   "(the position that side takes) so you have territory to answer. Both sources stay on "
                   "screen while you work.")),
        Slot("TRANSFER", "production_frq", "Build a STAND claim on the new topic (bank-partitioned)",
             ref="", bank="congestion_pricing", rubric_ref="rc.ohio", scored=True, unit="sentence",
             body=("Transfer to a topic you have not practiced: on the congestion-pricing question (should "
                   "cities charge tolls to drive downtown during the busiest hours?), write a defensible claim "
                   "using the same STAND moves. Product goal, all four required: take a clear Stance; make an "
                   "Assertion the other side could reject; attach your I-say reason with a because/but/so "
                   "hinge, drawn from the two sources; and answer 'so what' by naming the stakes. Scored on "
                   "Thesis/Purpose.")),
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
