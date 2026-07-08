"""
lesson_t2_claim_building.py  -  G10 model lesson, TYPE 2: CLAIM-BUILDING.

Assembles a Timeback assessment-test (ordered item sequence) that instantiates the council-adjudicated
Type-2 shell (G10_Model_Lesson_Specs.md) against the REAL G10 banks. Target: a DEFENSIBLE thesis built
via they-say/I-say in three stances (agree / disagree / agree-with-a-difference), where the "I say" is a
because/but/so completion (TWR) and the claim must pass the "so what" stakes test (GAP #22). Binds ONLY
LESSON-pool stimuli (no test-pool item is reused as instruction):
  - stimulus  ACC-W910-ARG-OPP-LESSON-SCHOOLYEAR (longer school year, opposing pair) -> read + argued from
  - stimulus  ACC-W910-ARG-OPP-LESSON-CONGESTION (congestion pricing, opposing pair) -> partitioned transfer

SRSD shell (Teach/Model/Supported/Independent/Transfer). Model = the modality-corrected 4-mechanism async
sequence (clean annotated before/after -> predict-the-fix -> feedback on the student's OWN draft [the FRQ
grader] -> student-generated diagnosis). Mnemonic STAND (proposal, not sourced).

Discrimination is a TWO-part Grade-C move (labeled): a 3-way sort (arguable claim vs fact vs ungrounded
opinion) placed in TEACH per the constant shell, then a GAP-#22 minimal pair (claim-with-stakes vs
claim-without) in SUPPORTED. The EG unscored freewrite sits at the end of TEACH, AFTER the discrimination
(claim-building is an allowed placement; never entry to analysis/evidence types). Bank-partitioned transfer
(longer school year -> congestion pricing). All slots map to native Timeback interactions.

NOTE on the freewrite: it renders as an extended-text production_frq but is NOT scored (scored=False). The
grader_routing gate still requires a valid rc.* on every production_frq, so it carries rubric_ref="rc.4trait"
while the body states plainly that it is an ungraded warm-up.

Runs the QC harness on execution and prints PASS/FAIL. Dependency-free (stdlib + lesson_contract).
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
    provenance={"copyright": "own_authored", "authored": "2026-07-07", "mnemonic_status": "proposal"},
    fade_ledger_moves=["because/but/so", "they-say/I-say", "so-what/stakes"],
    slots=[
        # ---------------- TEACH: background + discuss + discrimination (Grade C) + test-demand + freewrite ----------------
        Slot("TEACH", "teach_card", "What a defensible claim is + the STAND cue + the so-what test",
             body=("A thesis is a claim you can defend. It is not a fact you can look up, and it is not an "
                   "opinion no one can weigh. Our cue for building one is STAND: Stance (which side you take), "
                   "Territory (the 'they say' you are answering), Assertion (a point a reasonable reader could "
                   "reject), Nuance (room to agree with a difference), Defensible (backed by reasons, not just "
                   "feeling). They-say/I-say gives you three stances to pick from: you can agree, you can "
                   "disagree, or you can agree with a difference (yes, but). Whichever you choose, a strong "
                   "claim also passes the 'so what' test: it says why the answer matters. On every state rubric, "
                   "the top band rewards a position that reaches significance, not one that just restates the "
                   "prompt. Goal for today: write a defensible claim that takes a stance and answers 'so what'.")),
        Slot("TEACH", "stimulus_display", "Read the sources on a longer school year",
             ref="ACC-W910-ARG-OPP-LESSON-SCHOOLYEAR", bank="longer_school_year",
             body=("Read both sources on whether the United States should adopt a longer school year. One side "
                   "argues that more days would narrow the summer-slide gap; the other argues that more seat "
                   "time is not the same as more learning. For each side, note the 'they say' (the position "
                   "that side takes) so you have real territory to answer.")),
        Slot("TEACH", "discrimination", "Sort it: fact vs arguable claim vs ungrounded opinion",
             labeled_grade_c=True, bank="longer_school_year",
             body=("Design-bet step (discriminate before you produce, a Grade-C move we label as a bet, not "
                   "proof): sort each statement as a FACT (checkable, no one argues it), an ARGUABLE CLAIM (a "
                   "stance a reasonable person could reject), or an UNGROUNDED OPINION (a preference with no "
                   "reason anyone could weigh). Only the arguable claim can anchor an essay. Sort these: "
                   "(1) 'A typical American public school runs about 180 days each year.' "
                   "(2) 'Because the long summer break lets some students slide backward while wealthier peers "
                   "keep learning, the United States should adopt a longer school year.' "
                   "(3) 'Summer break is just the best part of the whole year.'")),
        Slot("TEACH", "production_frq", "Ungraded warm-up: what do you actually think?",
             bank="longer_school_year", rubric_ref="rc.4trait", scored=False,
             body=("Ungraded warm-up (this one is not scored, so write freely): before you study any models, "
                   "freewrite for a few minutes on the real question. What do you actually think about whether "
                   "the United States should adopt a longer school year, and why? Get your honest take onto "
                   "the page. Next we will sharpen it into a defensible claim.")),

        # ---------------- MODEL: 4-mechanism async sequence ----------------
        Slot("MODEL", "annotated_before_after", "Watch a fact become a defensible claim",
             bank="longer_school_year",
             body=("BEFORE (a fact, not a claim): 'A typical American public school runs about 180 days a "
                   "year.' That statement is true, and the sources confirm it (NCES), but no one on the other "
                   "side disagrees with it, so there is nothing to argue. "
                   "AFTER (an arguable claim with stakes, annotated): 'The United States should adopt a longer "
                   "school year [Stance + Assertion the other side could reject], because a schedule that "
                   "sends students away for a long summer lets learning slide backward for the children who "
                   "can least afford tutoring or camps [because-hinge, the I say], which quietly widens the "
                   "gap between richer and poorer students every fall instead of closing it [so what: the "
                   "stakes].' "
                   "Notice the AFTER version does what the BEFORE cannot: it takes a Stance, makes an "
                   "Assertion a reasonable reader could reject, and answers 'so what'. That is the S, the A, "
                   "and the significance beat of STAND doing the work.")),
        Slot("MODEL", "predict_the_fix", "Predict: why can this not be your thesis?",
             bank="longer_school_year",
             body=("Diagnose this draft before we reveal the fix. If this sentence were offered as a thesis, "
                   "which is its single biggest problem? "
                   "Draft: 'The summer break lasts about two to three months in most American schools.' "
                   "(A) it states a fact no one disputes, so there is no arguable stance to defend  "
                   "(B) it is too short to be a thesis  (C) it does not name its source  "
                   "(D) it uses a number instead of words"),
             feedback=("The answer is A. 'The summer break lasts about two to three months' is a checkable "
                       "fact, and a fact is not a claim: nobody on the other side disagrees, so there is "
                       "nothing to argue. To turn it into a defensible thesis you add a Stance and an "
                       "Assertion the other side could reject ('the United States should adopt a longer "
                       "school year'), then answer 'so what' by naming the stakes (why the length of the "
                       "break matters). A fact can support a claim, but it cannot be the claim. Length, "
                       "citation, and numbers are not the issue here.")),

        # ---------------- SUPPORTED: discrimination (Grade-C, labeled, GAP #22) then guided production ----------------
        Slot("SUPPORTED", "discrimination", "Claim with stakes vs claim without (so-what minimal pair)",
             labeled_grade_c=True, bank="longer_school_year",
             body=("Design-bet step (labeled Grade-C): both options below are arguable claims that take the "
                   "same stance. They differ on exactly one move, the 'so what.' Pick the one that answers "
                   "why it matters. "
                   "(A) 'The United States should adopt a longer school year.' "
                   "(B) 'The United States should adopt a longer school year, because the long summer break "
                   "lets low-income students lose ground while wealthier peers keep learning, widening the "
                   "gap the schools then spend every fall trying to rebuild.' "
                   "B reaches the stakes; A stops at the position. Top-band rubrics reward the claim that says "
                   "why it matters.")),
        Slot("SUPPORTED", "production_frq", "Guided: write ONE defensible STAND claim",
             bank="longer_school_year", rubric_ref="rc.ohio", scored=True,
             body=("Guided practice: write ONE defensible claim on the longer-school-year question. Pick a "
                   "Stance (agree, disagree, or agree-with-a-difference), state an Assertion the other side "
                   "could reject, complete the 'I say' with a because/but/so hinge, and finish with a 'so "
                   "what' clause that names the stakes. Draw your reason from the sources. Scored on "
                   "Thesis/Purpose.")),
        Slot("MODEL", "diagnosis_frq", "Diagnose your own claim",
             bank="longer_school_year", scored=True,
             body=("In one or two sentences, diagnose your own work. Is your claim arguable (could a "
                   "reasonable reader on the other side reject it, or is it really a fact or a bare opinion)? "
                   "Does it answer 'so what' by naming the stakes? Name the STAND letters your claim delivers "
                   "and the one it still needs.")),

        # ---------------- INDEPENDENT: STAND claim with a stakes beat ----------------
        Slot("INDEPENDENT", "production_frq", "Write an independent STAND claim with stakes",
             bank="longer_school_year", rubric_ref="rc.ohio", scored=True,
             body=("Independent performance: on the longer-school-year question, write a defensible thesis "
                   "that takes a clear Stance, makes an Assertion the other side could reject, and answers 'so "
                   "what' with an explicit stakes beat (why the answer matters). Use a because/but/so hinge as "
                   "your 'I say.' Scored on Thesis/Purpose.")),

        # ---------------- TRANSFER: same move, partitioned content bank ----------------
        Slot("TRANSFER", "stimulus_display", "Read the sources on a NEW topic",
             ref="ACC-W910-ARG-OPP-LESSON-CONGESTION", bank="congestion_pricing",
             body=("Read this new pair of sources on whether cities should charge tolls to drive downtown "
                   "during the busiest hours (congestion pricing). For each side, note the 'they say' so you "
                   "have territory to answer.")),
        Slot("TRANSFER", "production_frq", "Build a STAND claim on the new topic",
             bank="congestion_pricing", rubric_ref="rc.ohio", scored=True,
             body=("Transfer to a topic you have not practiced: write a defensible claim on whether cities "
                   "should charge tolls to drive downtown during busy hours. Take a Stance, make an arguable "
                   "Assertion, add your 'I say' with a because/but/so hinge, and answer 'so what' by naming "
                   "the stakes. Scored on Thesis/Purpose.")),
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
