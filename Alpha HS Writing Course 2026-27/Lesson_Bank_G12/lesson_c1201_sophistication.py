"""
lesson_c1201_sophistication.py  -  G12 KC C.12.01, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD) + mandatory T5
calibration loop, applied to SOPHISTICATION (AP Lang Row C).

CURRENT SoT ANCHOR:
  - KC:    C.12.01  "AP sophistication (significance / context / complexity)"  (OVERLAY: the AP Lang Row C
           rubric point on the CCSS W.1/W.2 argument+explanatory standards)
  - unit:  G12 U1  Sophistication mastery
  - funnel: sophistication   archetype: T7 (BUILD) + mandatory T5 calibration loop (per 2026-07-09 council)
           production ceiling: essay
  - acc:   [ACC.W.ARG.2]   ccss: [W.11-12.1, W.11-12.2]
  - taught stimulus:   ACC-W910-ARG-LESSON-WATERTRADEOFF   (G12 lesson bucket; a hard trade-off that rewards nuance)
  - transfer stimulus: ACC-W910-ARG-LESSON-WORKFORCEINVEST (bank-partitioned)
  - rc.* rubric:       rc.ap

AUTHORED to the finalized playbook + the 19-gate contract + the council ruling:
  * 2026-07-09 council: sophistication is DEVELOPED through PRODUCTION (T7 BUILD), with a mandatory calibration
    loop (T5): the trait is scored in the student's OWN produced argument, so production is the vehicle; the
    calibration loop trains the student to recognize sophistication (predict-then-reveal), it does not replace
    producing it. Sophistication = the three teachable moves: situate the argument in a broader context,
    explain complexity/significance, hold the tension with nuance.
  * MODEL is the async annotated before/after worked example (NO near-peer/human coping model; labeled
    author-voice annotations) + predict-the-fix; a self_score calibration step precedes a graded reveal;
    diagnosis modeled-then-scaffolded. SRSD live ES NOT claimed. Evidence cited is calibration-specific.
  * TWR moves CUED as already-faded prerequisites (nuanced claim, evidence, warrant), NOT re-taught. Mechanics
    APP-OWNED, assumed gated + applied.
  * Stateless / display-only; no prior-work ref; no off-platform; no loops. Seam-routing UNBUILT/pending-eng.

Runs the QC harness on execution and prints PASS/FAIL. Dependency-free (stdlib + lesson_contract).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report

LESSON = Lesson(
    id="ACC-W910-L-G12-C1201-0001", grade="9-10", lesson_type=7,
    unit="G12 U1 - Sophistication mastery (situate, complicate, nuance)",
    title="Earn the Sophistication Point: Situate, Complicate, Nuance (BUILD)",
    target=("Develop sophistication in an argument essay by making three moves: situate the argument in a "
            "broader context, explain its complexity and significance, and hold the tension with nuance rather "
            "than flattening it. Produced in a full essay, with a calibration loop that trains recognition of "
            "the move. Climbs to the essay. Trait: Sophistication (AP Row C)."),
    acc_tags=["ACC.W.ARG.2", "CCSS.W.11-12.1", "CCSS.W.11-12.2"],
    provenance={"copyright": "own_authored", "authored": "2026-07-10", "mnemonic_status": "proposal",
                "kc": "C.12.01", "sot": "KC_Map_and_Unit_Arch_G9-12.md (G12 U1 Sophistication; OVERLAY)",
                "taught_stimulus": "ACC-W910-ARG-LESSON-WATERTRADEOFF",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-WORKFORCEINVEST",
                "playbook": "_phase2/playbook_T7_BUILD.md (+ T5 calibration loop)",
                "council": ("2026-07-09 council: sophistication = T7 BUILD (developed via production) + mandatory "
                            "T5 calibration loop; NOT T5-as-primary (the trait is scored in the PRODUCED "
                            "argument). Annotated before/after (labeled author-voice annotations, NO near-peer/"
                            "human coping model), predict-the-fix, self_score-before-reveal, diagnosis modeled-"
                            "then-scaffolded; calibration-specific evidence only; TWR moves cued not re-taught; "
                            "app-owned mechanics assumed not re-taught; SRSD live ES NOT claimed.")},
    fade_ledger_moves=["situate-in-context", "explain-complexity", "hold-the-tension"],
    slots=[
        # ================= TEACH: define sophistication + its three teachable moves =================
        Slot("TEACH", "teach_card", "What sophistication is (not big words, but deeper thinking)",
             body=("At the top of the AP argument rubric sits a point for sophistication. Sophistication does "
                   "NOT mean fancy vocabulary or long sentences; a common trap is dressing a simple argument in "
                   "big words and expecting the point. Sophistication means a demonstrated depth of thought: an "
                   "argument that situates its question in a broader context, explains why the question is "
                   "complex and why it matters, and holds the tension between competing considerations instead "
                   "of pretending one side is obviously right. Your claim, also called the thesis, means the "
                   "one position your essay defends; sophistication is a QUALITY of how you defend it, not a "
                   "separate paragraph you bolt on. The trap that loses the point is oversimplifying, treating "
                   "a genuinely hard trade-off as if the answer were easy, or reducing the other side to a "
                   "strawman. Goal today: produce an argument that earns the sophistication point by situating, "
                   "complicating, and holding the tension of a hard question.")),
        Slot("TEACH", "teach_card", "The three sophistication moves, and how to make them",
             body=("Sophistication comes down to three teachable moves; you already own the claim and evidence "
                   "moves, so cue those and add these. SITUATE: place the specific question inside a larger "
                   "one. Right: framing a local water fight as an instance of how societies ration a resource "
                   "no one can make more of. Wrong: treating it as an isolated squabble. COMPLICATE: name why "
                   "the question is genuinely hard, what makes each side's concern legitimate, so the reader "
                   "sees real stakes on both sides. Right: showing that protecting farms and protecting power "
                   "each has a fair claim. Wrong: a strawman of the losing side. HOLD THE TENSION: defend your "
                   "position while keeping the opposing consideration in view, often with a 'even though ... "
                   "still ...' or 'the harder truth is ...' turn, rather than declaring the other side simply "
                   "wrong. These are moves you PRODUCE in the essay, not phrases you sprinkle. Reward the "
                   "thinking, not the vocabulary. (App-ownership note: the sentence mechanics behind these "
                   "moves are owned upstream by AlphaWrite, G3-8, and EGUMPP, G3-10; assumed as retrieval-gated "
                   "prerequisites and applied, not re-taught here.)")),
        Slot("TEACH", "stimulus_display", "Read the prompt source: when food and power compete for the same water",
             ref="ACC-W910-ARG-LESSON-WATERTRADEOFF", bank="water_tradeoff",
             body=("Read the source on a hard trade-off: when water is scarce, should a region protect it for "
                   "growing food or for generating power? Notice the source is built to resist an easy answer, "
                   "each use has a fair claim, and they depend on each other. Read and note where the real "
                   "complexity lives, because a sophisticated argument here will situate, complicate, and hold "
                   "that tension rather than pick a side and dismiss the other. The source stays on screen "
                   "while you work.")),

        # ================= MODEL: annotated before/after -> predict-the-fix =================
        Slot("MODEL", "annotated_before_after", "Watch a flat argument gain sophistication",
             bank="water_tradeoff",
             body=("BEFORE (a competent but flat argument): 'When water is scarce, the region should protect it "
                   "for growing food. Food is a basic need, and people cannot live without it. Power is less "
                   "important than eating, so farms should come first.' Check it: it takes a clear side and "
                   "gives a reason, so it would score on the lower rows, but it earns no sophistication point. "
                   "It never situates the question in anything larger, never grants that the power side has a "
                   "real claim, and flattens the tension ('power is less important') into a strawman. "
                   "AFTER (the same position, now sophisticated, annotated): 'When water runs short, a region "
                   "is really being asked how it rations a resource it cannot manufacture, and that larger "
                   "question is why the food-or-power choice resists an easy answer [SITUATE: the specific "
                   "fight placed inside a larger one]. Protecting farms first is defensible, because a lost "
                   "growing season can end farms that took generations to build; yet the case for power is not "
                   "weaker but entangled, since the pumps that irrigate those very farms run on the "
                   "electricity that cooling water makes possible [COMPLICATE: both claims shown legitimate and "
                   "interdependent]. The honest position, then, is not to crown one use but to protect food "
                   "first while treating the power it depends on as part of the food system, even though that "
                   "means neither side gets all it wants [HOLD THE TENSION: defends a side without flattening "
                   "the other].' "
                   "Read the labels: same side as the BEFORE, but it situates the question, shows why both "
                   "claims are real and linked, and holds the tension instead of dismissing the loser. That "
                   "depth of thinking, not any fancy word, is the sophistication point.")),
        Slot("MODEL", "predict_the_fix", "Predict: why does this argument miss the sophistication point?",
             bank="water_tradeoff",
             body=("Diagnose this draft before the reveal. A student wrote: 'The region should protect water "
                   "for power, because electricity runs everything in modern life. Farming matters less because "
                   "we can import food from other places.' What single move would most help it earn "
                   "sophistication? "
                   "(A) grant that the food side has a real, not weaker, claim and hold the tension (show why "
                   "the choice is genuinely hard), instead of dismissing farming  "
                   "(B) use more advanced vocabulary  "
                   "(C) add another reason power matters  "
                   "(D) make the conclusion more confident"),
             feedback=("Correct: A. The draft picks a side and then flattens the other ('farming matters less,' "
                       "'we can import food'), which is the strawman that costs the sophistication point. The "
                       "fix does not switch sides; it grants that food security is a real claim, situates the "
                       "choice in the larger problem of rationing scarce water, and holds the tension (defends "
                       "power while acknowledging what protecting it costs food). Advanced vocabulary (B), "
                       "another same-side reason (C), or a more confident tone (D) add no depth. Sophistication "
                       "is thinking, not diction.")),

        # ================= SUPPORTED: self_score calibration -> discrimination -> guided completion =========
        Slot("SUPPORTED", "self_score", "Predict the sophistication score, then reveal the gap",
             bank="water_tradeoff",
             body=("Calibration step: judge a provided draft, commit to a score, THEN see the gap. Calibration "
                   "matters here because sophistication is the trait writers most often think they have earned "
                   "when they have not; recognizing it in others trains you to produce it. Provided draft: "
                   "'This is a hard issue with good points on both sides. Water is important for food and for "
                   "power. In the end, the region should protect food, because eating is essential. Both sides "
                   "have merit, but food wins.' On a simple 2-point sophistication scale, 0 = no sophistication "
                   "(states 'both sides' but does not situate, complicate, or hold tension), 1 = earns the "
                   "point, predict the score and hold your number in mind. Reveal: this draft scores 0. Saying "
                   "'both sides have merit' is not the same as SHOWING why: it never situates the question in "
                   "anything larger, never explains what makes each claim legitimate, and resolves the tension "
                   "by fiat ('food wins') rather than holding it. If you predicted a 1, that gap is the point: "
                   "gesturing at complexity ('hard issue,' 'both sides') is the most common counterfeit of "
                   "sophistication. Recalibrate toward the three moves, situate, complicate, hold.")),
        Slot("SUPPORTED", "discrimination", "Sophisticated vs merely balanced (labeled Grade-C)",
             ref="", labeled_grade_c=True, bank="water_tradeoff",
             body=("Discriminate before you produce (a Grade-C design bet we label as a bet, not proof). Both "
                   "responses take the same side; they differ on ONE thing, whether they earn sophistication. "
                   "Which one is SOPHISTICATED? "
                   "(A) 'The region should protect food. There are points on both sides, but food is more "
                   "important than power, so it should come first.'  "
                   "(B) 'Because a region facing scarce water is really deciding how to ration something it "
                   "cannot make more of, the food-or-power choice cannot be settled by ranking needs; the "
                   "sharper truth is that the farms worth protecting run on the very power that competes with "
                   "them, so protecting food means protecting the electricity it depends on, even though that "
                   "leaves neither use fully satisfied.'  "
                   "(C) 'Water is used for many things in the United States.'  "
                   "(D) 'I think both food and power are really important to people.'  "
                   "Correct: B. A takes a side but only asserts a ranking (no situating, no held tension). C is "
                   "a fact; D is a vague both-sides gesture. Only B situates the question, shows the "
                   "interdependence (complexity), and holds the tension while defending a side. That is the "
                   "sophistication move.")),
        Slot("SUPPORTED", "production_frq", "Completion: the claim is given, you supply the sophistication moves",
             ref="", bank="water_tradeoff", rubric_ref="rc.4trait", scored=True, unit="paragraph",
             body=("Guided completion: the position is given, so spend your effort on the sophistication moves. "
                   "POSITION: in a water-scarce region, protect food first. Write a short paragraph defending "
                   "this position that earns the sophistication point. Product goal, all three moves required: "
                   "(1) SITUATE, place the food-or-power choice inside the larger problem of rationing a "
                   "resource that cannot be made; (2) COMPLICATE, show why the power side has a real, "
                   "interdependent claim (the farms need electricity), not a weaker one; (3) HOLD THE TENSION, "
                   "defend protecting food while acknowledging what that costs the power side, using an 'even "
                   "though ... still ...' turn. Do not flatten the other side. Scored on Sophistication.")),
        Slot("MODEL", "diagnosis_frq", "Diagnose with the sophistication checklist (modeled, then you)",
             ref="", bank="water_tradeoff", scored=True,
             body=("First watch the check run on a flat draft, then run the same checklist on a fresh paragraph "
                   "of your own. Flat draft: 'Protect food first. Food is more important than power. Both "
                   "matter, but food wins.' Run the sophistication check step by step. Step 1, Situate: is the "
                   "question placed in a larger one? No; add the rationing-scarce-resource frame. Step 2, "
                   "Complicate: is the other side shown as a real, legitimate claim (here, interdependent)? No; "
                   "add that the farms depend on the power. Step 3, Hold tension: does it defend a side while "
                   "keeping the other in view, or flatten it? Flattens ('food wins'); add an 'even though ... "
                   "still ...' turn. Now you: write one fresh sophisticated paragraph on the water trade-off, "
                   "then run the same three-item checklist on it. Before you submit, apply this one-pass check: "
                   "if you named 'both sides' without SHOWING why each is legitimate, add the complication; if "
                   "you resolved the tension by fiat, replace it with a held tension. Finish by naming which "
                   "sophistication move your paragraph still needs.")),

        # ================= INDEPENDENT: full sophisticated essay, self-contained =================
        Slot("INDEPENDENT", "production_frq", "Write a full sophisticated argument essay (self-contained)",
             ref="", bank="water_tradeoff", rubric_ref="rc.4trait", scored=True, unit="essay",
             body=("Independent performance, self-contained (write a fresh essay; do not refer to an earlier "
                   "item). On the water trade-off, write a full argument essay that takes a clear position AND "
                   "earns the sophistication point. Product goal: (1) a nuanced claim; (2) body paragraphs with "
                   "evidence and reasoning; and, threaded through, the three sophistication moves, SITUATE the "
                   "question in the larger problem of rationing scarce water, COMPLICATE by showing both claims "
                   "as legitimate and interdependent, and HOLD THE TENSION rather than flattening the losing "
                   "side. Before you submit, check: did I situate, complicate, and hold the tension, or did I "
                   "just assert 'both sides matter'? Sophistication is shown, not stated. Scored on the full "
                   "rubric with Sophistication as the top-band move.")),

        # ================= TRANSFER: same sophistication move, bank-partitioned trade-off =================
        Slot("TRANSFER", "stimulus_display", "Read a NEW hard trade-off: prepare the next workers, or protect the present ones?",
             ref="ACC-W910-ARG-LESSON-WORKFORCEINVEST", bank="workforce_invest",
             body=("Read this new source on another hard trade-off: as technical fields grow fast, should a "
                   "society invest first in preparing more people for those fields, or first in protecting the "
                   "workers the change leaves behind? Like the water source, it resists an easy answer, both "
                   "claims are real and in tension. Read and note where the genuine complexity lives. The "
                   "source stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Write a sophisticated essay on the new trade-off (bank-partitioned)",
             ref="", bank="workforce_invest", rubric_ref="rc.4trait", scored=True, unit="essay",
             body=("Transfer to a trade-off you have not practiced. On the workforce-investment question, write "
                   "a full argument essay that takes a position and earns the sophistication point. Product "
                   "goal: a nuanced claim, evidence and reasoning, and the three sophistication moves, SITUATE "
                   "the choice in a larger question (how a society balances its future against its present), "
                   "COMPLICATE by showing both claims as legitimate, and HOLD THE TENSION rather than "
                   "flattening the other side. Same sophistication move as the water trade-off; new question. "
                   "Scored with Sophistication as the top-band move.")),
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
