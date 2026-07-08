"""
lesson_t5_rubric_revision.py  -  G10 model lesson, TYPE 5: RUBRIC-REVISION (the CALIBRATION ENGINE).

Assembles a Timeback assessment-test (ordered item sequence) that instantiates the council-adjudicated
Type-5 shell (G10_Model_Lesson_Specs.md) against the REAL G10 LESSON-POOL banks (contamination-free: no
test-pool stimulus, no CR/SR item is bound; students never learn on a passage they are later tested on).
This is the calibration engine: a JUDGE-THEN-REVEAL loop (predict a score, THEN reveal the gap) that
teaches students to revise for SUBSTANCE against the rubric, not to polish surface mechanics. Binds:
  - stimulus ACC-W910-INFO-LESSON-RECYCLING (materials recovery) -> the topic students calibrate + revise on
The TRANSFER topic is wetlands (bank "wetlands_restoration"), authored inline (ref="") so no id is reused.

SRSD shell (Teach/Model/Supported/Independent/Transfer). Model = the modality-corrected async sequence
(clean annotated before/after where a student over-rates own draft at a 3 and the reveal shows a 2 with the
gap named -> predict-the-fix boundary pair -> student-generated diagnosis). The calibration core is the
self_score -> production_frq/diagnosis_frq REVEAL pattern: every predict-your-score move is followed by a
graded reveal of the gap (never "hand rubric + grade yourself"). Feedback is GOAL/NOW/NEXT, never
person-praise, never a grade with nothing attached. The STAAR gating rule is taught as a principle
(score Organization/Development first; if 0, Conventions 0). Mnemonic CHECK (proposal).

Bank-partitioned transfer (recycling -> wetlands). Every production_frq is authored (ref=""); the lesson's
one real bank binding is the recycling lesson-pool stimulus in TEACH. All slots map to native Timeback
interactions. Runs the QC harness on execution and prints PASS/FAIL. Dependency-free (stdlib + lesson_contract).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report

LESSON = Lesson(
    id="ACC-W910-L-T5-RUBRIC-0001", grade="9-10", lesson_type=5,
    unit="G10 U3 - Rubric-based revision (the calibration engine)",
    title="Score It Before You're Scored: Revise for Substance (CHECK)",
    target=("Revise a paragraph for SUBSTANCE against the rubric, not surface mechanics: name the trait, "
            "predict your own score, reveal the gap to the anchor, and correct the one move that raises the "
            "score. Deeper engine = calibration. Trait: Organization/Development."),
    acc_tags=["ACC.W.REV.1", "ACC.W.CAL.1", "CCSS.W.9-10.5"],
    provenance={"copyright": "own_authored", "authored": "2026-07-07", "mnemonic_status": "proposal",
                "council": "W&H calibration engine (predict-then-reveal); DI boundary-pair discrimination; "
                           "SRSD shell + recovery model; gating rule as principle (conventions serve content)"},
    fade_ledger_moves=["predict-then-reveal calibration", "explain-the-evidence (2->3 move)", "gating-rule"],
    slots=[
        # ---------------- TEACH: CHECK cue + substance vs surface + gating rule + GOAL/NOW/NEXT ----------------
        Slot("TEACH", "teach_card", "Substantive revision vs surface editing + the CHECK cue",
             body=("Revising for substance means changing what your writing SAYS and how well it meets the "
                   "rubric, not just tidying commas and spelling. Surface editing fixes the sentence: a typo, a "
                   "run-on, a misused word. Substantive revision changes the score on the traits that carry the "
                   "most weight: does the paragraph state a clear controlling idea, does it develop that idea "
                   "with specific evidence, and does it EXPLAIN how the evidence supports the point. You can "
                   "proofread a thin paragraph until it is spotless and it will still sit in the middle band, "
                   "because clean commas do not add development. Our cue for the calibration move is CHECK: "
                   "Criteria (name the trait you are scoring), Hunt (find where the draft meets it and where it "
                   "misses), Explain the gap (say in words what a higher-scoring version does that this one does "
                   "not), Correct (make the substantive change), Keep-score (predict your score, THEN reveal the "
                   "real one and measure the gap). "
                   "The gating rule (STAAR) is a principle worth learning here: a scorer reads Organization and "
                   "Development FIRST, and if a response earns 0 there, Conventions is scored 0 as well. The idea "
                   "behind the rule is that conventions serve content: a flawlessly punctuated paragraph with no "
                   "real idea gives the punctuation nothing to carry. So do not polish commas on a thin essay, "
                   "fix the idea and the evidence first. "
                   "Every reveal in this lesson uses one feedback format, GOAL / NOW / NEXT: GOAL names the "
                   "target trait, NOW names exactly where the draft stands and what is missing, NEXT names the "
                   "single move that raises the score. No praise for the writer, and no bare number: a grade "
                   "with nothing attached does not tell you what to change.")),
        Slot("TEACH", "stimulus_display", "Read the source you will calibrate on",
             ref="ACC-W910-INFO-LESSON-RECYCLING", bank="recycling_recovery",
             body=("Read the source on recycling and materials recovery. You will score short paragraphs "
                   "written about this topic, so you need to know what the evidence actually says. Note two "
                   "specific figures a strong paragraph could use, and beside each one ask: could I say in a "
                   "sentence WHY that figure matters to a claim?")),

        # ---------------- MODEL: annotated over-rating reveal -> predict-the-fix boundary pair ----------------
        Slot("MODEL", "annotated_before_after", "A self-awarded 3 that the reveal shows is a 2",
             bank="recycling_recovery",
             body=("A student wrote this body paragraph on recycling and self-awarded it a 3 on Development. "
                   "BEFORE (student self-scores 3): 'Recycling is huge and important. According to the source, "
                   "Americans recycled more than 69 million tons of material in 2018. This shows recycling "
                   "matters. The country also makes about 292.4 million tons of waste, which is a lot.' The "
                   "student's reasoning for the 3: 'I stated a claim, I quoted the source, and I used two "
                   "facts.' "
                   "AFTER (revealed score 2, gap named): the anchor paper that actually earns a 3 does one thing "
                   "this draft never does, so it stays a 2. It names the 69 million ton figure and then only "
                   "labels it ('this shows recycling matters'); it never says HOW that tonnage matters, for "
                   "instance that recycling and composting together handled almost 94 million tons, about 32 "
                   "percent of the nation's waste, keeping that share out of landfills. The second fact (292.4 "
                   "million tons generated) is dropped with no tie to the claim at all. "
                   "GOAL: Development that explains evidence, not just names it. NOW: the draft names two figures "
                   "and explains neither, so it holds at a 2. NEXT: after the 69 million ton fact, add one "
                   "sentence saying why recovering that much material matters. Annotation on the sentence: the "
                   "anchor 3 explains after every figure and mine does not, that is the exact gap.")),
        Slot("MODEL", "predict_the_fix", "Predict which draft scores higher (2/3 boundary pair)",
             bank="recycling_recovery",
             body=("Two drafts sit on the 2/3 boundary and cite the SAME figure. Predict which one scores higher "
                   "on Development before the reveal. "
                   "Draft P: 'Recycling saves energy. The source says recycling one ton of aluminum cans saves "
                   "more than 152 million Btu. That is a lot of energy. Recycling is clearly worth it.' "
                   "Draft Q: 'Recycling saves energy. The source says recycling one ton of aluminum cans saves "
                   "more than 152 million Btu, which matters because that is about the same as 1,024 gallons of "
                   "gasoline, so every ton of cans recovered keeps a large amount of fuel from being burned to "
                   "make new metal from scratch.' "
                   "(A) Draft P scores higher  (B) Draft Q scores higher  (C) they score the same"),
             feedback=("Draft Q scores higher, and the single move that separates them is explanation. Both cite "
                       "the same 152 million Btu figure, so they are level on evidence PRESENCE. GOAL: "
                       "Development that ties evidence to a point. NOW: Draft P stops at 'that is a lot of "
                       "energy,' which only restates the number, so it holds at a 2. Draft Q takes the same "
                       "figure and explains what it means (152 million Btu equals about 1,024 gallons of "
                       "gasoline saved per ton), reaching the 3. NEXT: whenever you keep a figure, add the "
                       "because-clause that says what it proves. Length is not what earns the point, the "
                       "explanation is.")),

        # ---------------- SUPPORTED: boundary-pair discrimination -> calibration loop (predict THEN reveal) ----
        Slot("SUPPORTED", "discrimination", "Pick the 3 and name the one move (2 vs 3 boundary pair)",
             ref="", labeled_grade_c=True, bank="recycling_recovery",
             body=("Design-bet step (discriminate before you produce, a Grade-C move we are testing, not a proven "
                   "law): here are two paragraphs on recycling that differ on exactly ONE move. One earns a 2, "
                   "one earns a 3 on Development. Pick the 3 and name the single move that separates them. "
                   "Option A (2): 'Recycling helps the economy. Recycling and reuse supported about 681,000 jobs "
                   "in a single year. Recycling is good for the country.' "
                   "Option B (3): 'Recycling helps the economy. The source reports that recycling and reuse "
                   "activities supported about 681,000 jobs in a single year, which is why the material in a "
                   "blue bin is not just waste to be managed but a resource that pays people to recover it.' "
                   "The separating move: Option B EXPLAINS what the 681,000 jobs figure does (it shows recovery "
                   "is paid work, a resource and not just trash); Option A only labels it 'good.'")),
        Slot("SUPPORTED", "self_score", "Predict your Development score BEFORE you write (Stage B)",
             bank="recycling_recovery",
             body=("Stage B calibration: predict, THEN reveal. In the next step you will write one paragraph. "
                   "First, before you see any scoring, predict on the 3-point Development scale what your "
                   "paragraph will earn (1, 2, or 3), and write one sentence of trait evidence for it: 'I predict "
                   "a __ because my paragraph ___.' You judged the anchors above first, then predict your own, "
                   "on purpose: writers tend to over-rate their own drafts, so we always commit to a prediction "
                   "before the grader reveals the real score.")),
        Slot("SUPPORTED", "production_frq", "Write the paragraph you predicted, then see the gap",
             ref="", bank="recycling_recovery", rubric_ref="rc.staar", scored=True,
             body=("Now write the paragraph you just predicted. Using the recycling source, write one body "
                   "paragraph that states a controlling idea and develops it with at least one specific figure "
                   "PLUS a sentence explaining how that figure supports your idea (the move that separates a 2 "
                   "from a 3). The grader scores it on the STAAR scale, reading Organization and Development "
                   "first per the gating rule, and reveals the gap between your predicted score and your real "
                   "one.")),
        Slot("SUPPORTED", "diagnosis_frq", "Diagnose the gap between predicted and revealed (CHECK)",
             bank="recycling_recovery", scored=True,
             body=("Diagnose the gap in the CHECK format. In two or three sentences: GOAL (which trait were you "
                   "scoring), NOW (what score did you predict, what did the grader give, and what specifically "
                   "did the anchor-3 version do that yours did not), NEXT (the one substantive move you will add "
                   "on your next paragraph to close the gap). Comment on the evidence and the explanation, not "
                   "on yourself as a writer.")),

        # ---------------- INDEPENDENT: self-score BEFORE, then graded reveal on the real scale ----------------
        Slot("INDEPENDENT", "self_score", "Predict the score of the paragraph you are about to write",
             bank="recycling_recovery",
             body=("Independent calibration. In the next step you will write one full body paragraph on "
                   "recycling in which every figure you cite is followed by a sentence explaining how it "
                   "supports your controlling idea. First, predict the Development score that paragraph will "
                   "earn on the 3-point scale, and name the one move you will make to earn it. Predict first, "
                   "then write and reveal.")),
        Slot("INDEPENDENT", "production_frq", "Independent performance: write to a 3, then reveal",
             ref="", bank="recycling_recovery", rubric_ref="rc.staar", scored=True,
             body=("Independent performance: write one full body paragraph on recycling and materials recovery "
                   "so that every figure you cite is followed by a sentence explaining how it supports your "
                   "controlling idea. Scored on the STAAR scale (Organization and Development scored first, then "
                   "Conventions, per the gating rule). The grader reveals your real score against your "
                   "prediction so you can measure how well-calibrated you are.")),

        # ---------------- TRANSFER: same CHECK move, partitioned NEW topic + new scale ----------------
        Slot("TRANSFER", "production_frq", "Transfer the CHECK move to a NEW topic",
             ref="", bank="wetlands_restoration", rubric_ref="rc.mcas", scored=True,
             body=("Transfer to a NEW topic you have not calibrated on. Write one body paragraph about wetlands "
                   "that states a controlling idea and develops it: cite at least one specific figure (for "
                   "example that one stretch of the Mississippi River's wetlands once stored at least 60 days of "
                   "floodwater but only 12 days after most were drained, or that more than one-third of the "
                   "nation's threatened and endangered species live only in wetlands) and, for each figure, add "
                   "the sentence that explains why it supports your idea. Scored on the MCAS Idea Development "
                   "scale. Same CHECK move, new material: name the criteria, hunt for the gap, explain it, "
                   "correct it, keep score.")),
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
