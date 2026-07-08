"""
lesson_t7_essay_assembly.py  -  G10 model lesson, TYPE 7: ESSAY-ASSEMBLY / PLANNING (the composite).

Assembles a Timeback assessment-test (ordered item sequence) that instantiates the council-adjudicated
Type-7 shell (G10_Model_Lesson_Specs.md) against the REAL G10 banks. This is the type that IS the test:
the STAAR single-source full ECR essay, where the sub-skills taught in Types 1-6 must run at once. Binds
ONLY LESSON-pool stimuli (no test-pool item is reused as instruction):
  - stimulus  ACC-W910-ARG-OPP-LESSON-CONGESTION (congestion pricing, opposing pair) -> the source read
  - the INDEPENDENT full essay is AUTHORED inline (ref="") on the congestion sources    -> no CR item reuse
  - stimulus  ACC-W910-ARG-OPP-LESSON-DST (daylight saving, opposing pair)             -> partitioned transfer

SRSD shell (Teach/Model/Supported/Independent/Transfer). Model = the modality-corrected 4-mechanism async
sequence (clean annotated before/after -> predict-the-fix -> feedback on the student's OWN draft [the FRQ
grader] -> student-generated diagnosis). Mnemonic BUILD (proposal, NOT sourced): Brainstorm to the prompt,
Underline the SPO plan, Lay out paragraphs, Integrate the Types 2-4 moves, Double-check to the rubric.

Composing-process lens (Hayes & Flower): planning, translating (drafting), and reviewing compete for the
same working memory, so this lesson teaches planning and reviewing as DISTINCT phases and uses the SPO
(Single-Paragraph-Outline scaled to a multi-paragraph outline) to externalize the plan, freeing working
memory for sentence production. The planning scaffold is the LAST thing to fade. Two strategic-move gaps
are wired in: the funnel-opening intro (establish context, then thesis) and the reverse-funnel conclusion
(synthesize, then reach significance, not a summary). A style pass rides in the double-check step.

Bank-partitioned transfer (congestion pricing -> daylight saving). All slots map to native Timeback
interactions. Runs the QC harness on execution and prints PASS/FAIL. Dependency-free (stdlib + contract).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report

LESSON = Lesson(
    id="ACC-W910-L-T7-ESSAY-0001", grade="9-10", lesson_type=7,
    unit="G10 U4 - Source-based argument (essay-assembly / planning)",
    title="Build the Whole Essay: Plan First, Then Draft (BUILD)",
    target=("Assemble the sub-skills into a full source-based argument under test conditions: plan with an "
            "SPO (thesis plus ordered evidence) scaled to a multi-paragraph outline, draft from the plan, "
            "and manage the composing process. Open with a funnel that establishes context before the "
            "thesis and close with a conclusion that reaches significance, not a summary. Touches all four "
            "traits, Organization especially."),
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "ACC.W.ARG.5", "ACC.W.INFO.6", "CCSS.W.9-10.1", "OH-ELA.W.9-10.1"],
    provenance={"copyright": "own_authored", "authored": "2026-07-07", "mnemonic_status": "proposal"},
    fade_ledger_moves=["SPO", "because/but/so", "attributive-tag", "funnel-intro", "significance-close"],
    slots=[
        # ---------------- TEACH: background + discuss + the composing-process orientation ----------------
        Slot("TEACH", "teach_card", "Why a plan beats a plunge (BUILD, and the three phases)",
             body=("On the test you have one source set, one prompt, and a single sitting to produce a whole "
                   "essay. That is the hardest job in writing because three things fight for room in your "
                   "head at once: deciding WHAT to say (planning), turning it into sentences (drafting), and "
                   "checking whether it works (reviewing). Try to do all three in one pass and you stall. The "
                   "fix is to make them separate phases. First you plan on paper, then you draft from the "
                   "plan, then you review against the rubric. A written plan is not wasted time. It holds the "
                   "order for you so your working memory is free to build good sentences. "
                   "Our cue for the whole job is BUILD: Brainstorm to the prompt (what does it actually ask, "
                   "which side can you defend from the source), Underline (single out your plan by writing a "
                   "one-line thesis first, then list your body points in order with the evidence each will "
                   "use), Lay out paragraphs (turn each outline line into a paragraph), Integrate (bring in the moves you "
                   "already own: a defensible claim, integrated evidence with a because/but/so hinge, and a "
                   "fair answer to the other side), and Double-check to the rubric (a review pass for "
                   "development, order, and style). "
                   "Two moves win the top band and are easy to skip under pressure. Open with a funnel: give "
                   "the reader a sentence or two of context on the issue BEFORE you state your thesis, so the "
                   "claim lands in a setting instead of out of nowhere. Close with the reverse: pull your "
                   "reasons back together and then answer the question so what, why this position matters "
                   "beyond the page. A conclusion that only restates the introduction stays mid-band. "
                   "Goal for today: plan first, draft from the plan, and frame the essay with a context "
                   "opening and a significance close.")),
        Slot("TEACH", "stimulus_display", "Read both sides of the congestion-pricing source",
             ref="ACC-W910-ARG-OPP-LESSON-CONGESTION", bank="congestion_pricing",
             body=("Read the opposing pair on whether cities should charge tolls to drive downtown during "
                   "the busiest hours (congestion pricing). As you read, jot the single strongest fact on "
                   "each side (for example, the road-use and clean-air data on one side and the household-cost "
                   "and uneven-transit data on the other). You are gathering the raw material your plan will "
                   "order, not deciding your whole essay yet.")),

        # ---------------- MODEL: 4-mechanism async sequence (plunge vs planned) ----------------
        Slot("MODEL", "annotated_before_after", "Watch a plunged-in pile become a planned, ordered essay",
             bank="congestion_pricing",
             body=("BEFORE (plunges in, no plan): 'Traffic is bad. The FHWA says Americans drive more than 3 "
                   "trillion miles a year. Congestion pricing charges a toll. But a toll costs a low-wage "
                   "worker the same as a rich driver. Transportation is a huge household expense. Also transit "
                   "is uneven. So congestion pricing is complicated and there are good points on both sides.' "
                   "Notice what happened: the writer started typing before deciding anything, so the "
                   "sentences pile up (fact, counter-fact, fact) and build toward nothing. There is no "
                   "thesis, the order is random, and the ending just shrugs. "
                   "AFTER (SPO plan drives the order): the writer stopped and wrote a plan first. "
                   "[SPO plan] Thesis: cities should charge congestion tolls, because a crowded free road is "
                   "overused and the toll money can build the transit that gives people a real way out of the "
                   "car. Body 1: the road is a limited space (FHWA: more than 3 trillion miles a year, much "
                   "of it in dense areas with no room for new lanes), so pricing the busiest hour makes "
                   "sense. Body 2: the honest objection, a flat toll hits low-wage workers hardest and "
                   "transit is uneven (Census: most commuters still drive, many alone), and answer it, the "
                   "toll only works paired with low-income discounts and real transit built from the "
                   "proceeds. Body 3: significance, cleaner air for the people who live downtown (EPA: "
                   "transportation is the largest source of US greenhouse gas emissions). "
                   "[Drafted intro, funnel] 'Every weekday morning, the same downtown streets fill with cars "
                   "that crawl for blocks and burn fuel going nowhere [context]. Cities should charge a "
                   "congestion toll during the busiest hours, because a road that is both crowded and free "
                   "gets overused, and the money a toll raises can build the transit that lets people leave "
                   "the car at home [thesis].' "
                   "[Drafted conclusion, reverse funnel] 'The wasted hours and the dirty air are not distant "
                   "worries, they are measured on those streets right now [synthesis]. Pricing the crowded "
                   "hour matters because it turns a hidden cost we already pay, in lost time and fouled air, "
                   "into money a city can spend on a way out of the traffic [significance, the so-what].' "
                   "Annotation: the AFTER never wanders because the plan set the order first. The intro "
                   "situates the issue before the claim, each body paragraph is one planned point with its "
                   "evidence tied to the thesis, and the conclusion reaches significance instead of "
                   "restating the opening. That is the plan doing the work drafting cannot do under "
                   "pressure.")),
        Slot("MODEL", "predict_the_fix", "Predict what this essay is missing before the reveal",
             bank="congestion_pricing",
             body=("Diagnose this draft before we reveal the fix. A student writes: an opening sentence that "
                   "jumps straight to 'I think cities should charge congestion tolls,' three body paragraphs "
                   "of facts in no clear order, and a last paragraph that reads 'In conclusion, cities should "
                   "charge congestion tolls because they are better.' What is the single biggest problem? "
                   "(A) it has no plan, so the body has no order and the conclusion only restates the intro "
                   "instead of reaching significance  (B) the sentences are too short  (C) it uses too many "
                   "facts from the source  (D) it should not name the opposing side at all"),
             feedback=("The strongest answer is A. The trouble is not the sentences or the facts, it is the "
                       "missing plan. Because the writer never built an SPO, the body points sit in random "
                       "order and nothing builds. And the conclusion just repeats the opening claim, so it "
                       "stalls at mid-band. The fix is to plan the order first (thesis, then ordered body "
                       "points with evidence) and to close by answering so what: why the position matters "
                       "beyond restating it. A context opening and a significance close are the two framing "
                       "moves this draft skipped.")),

        # ---------------- SUPPORTED: discrimination (Grade-C, labeled) then a scaffolded plan ----------------
        Slot("SUPPORTED", "discrimination", "Planned-and-ordered vs plunged-in pile (minimal pair)",
             labeled_grade_c=True, bank="congestion_pricing",
             body=("Design-bet step (discriminate before you produce): you will see two openings for the same "
                   "congestion-pricing essay. Version 1 gives one sentence of context on the daily gridlock "
                   "downtown and then states a clear thesis (a funnel opening). Version 2 lists three facts "
                   "from the source and never states a position. Pick the version whose plan you can see "
                   "driving the order. The two differ on exactly one move: whether a thesis sets the "
                   "direction before the evidence arrives.")),
        Slot("SUPPORTED", "production_frq", "Complete the partial SPO plan (scaffold)",
             bank="congestion_pricing", rubric_ref="rc.4trait", scored=True,
             body=("Guided planning: here is a partial SPO for the congestion-pricing essay with the thesis "
                   "and the first body line filled in for you. Thesis (given): cities should charge a "
                   "congestion toll, because a crowded free road is overused and the toll money can build the "
                   "transit that gives people a way out of the car. Body 1 (given): the road is limited space "
                   "with no room for new lanes (FHWA road-use figures). Complete the plan: write Body 2 and "
                   "Body 3 as one line each, naming the point AND the specific source evidence each will use, "
                   "and order them so the essay builds. You are only planning here, not drafting sentences.")),
        Slot("SUPPORTED", "diagnosis_frq", "Diagnose your own plan and framing",
             bank="congestion_pricing", scored=True,
             body=("In two or three sentences, diagnose your own plan before you draft from it. Does your "
                   "opening establish context before the thesis, or does it jump straight to the claim? Do "
                   "your body points sit in an order that builds toward the thesis, or could they be shuffled "
                   "with no loss? Does your planned conclusion reach significance (why the position matters), "
                   "or would it only restate the introduction? Name one move you will change before drafting.")),

        # ---------------- INDEPENDENT: plan-then-draft, planning scaffold faded ----------------
        Slot("INDEPENDENT", "production_frq", "Build the full SPO plan from scratch (scaffold faded)",
             bank="congestion_pricing", rubric_ref="rc.4trait", scored=True,
             body=("Independent planning, no outline provided: for the congestion-pricing prompt, write your "
                   "own complete SPO. Give a one-line thesis that takes a defensible side, then list two or "
                   "three body points in order, each naming the specific source evidence it will use and how "
                   "that evidence ties to the thesis. Note in one phrase how you will open with context and "
                   "how your conclusion will reach significance. This plan is the map you will draft from "
                   "next.")),
        Slot("INDEPENDENT", "production_frq", "Draft the full essay from your plan (authored, on the congestion sources)",
             bank="congestion_pricing", rubric_ref="rc.staar", scored=True,
             body=("Independent performance, timed and from your own plan: write the full argumentative essay "
                   "on whether cities should charge tolls to drive downtown during the busiest hours. Use the "
                   "congestion-pricing sources you read at the start of the lesson. Draft from the SPO you "
                   "just built. Open with a funnel that establishes context before your thesis, develop each "
                   "body paragraph with integrated source evidence tied to the claim, directly answer at "
                   "least one objection from the side you argue against, and close with a conclusion that "
                   "reaches significance rather than restating your opening. Then run one quick double-check "
                   "pass for development, order, and style. Scored on all four traits, Organization "
                   "especially.")),

        # ---------------- TRANSFER: full timed essay, partitioned content bank ----------------
        Slot("TRANSFER", "production_frq", "Plan and draft a full timed essay on a NEW topic",
             ref="ACC-W910-ARG-OPP-LESSON-DST", bank="daylight_saving", rubric_ref="rc.ohio", scored=True,
             body=("Transfer: run the whole BUILD process on a source you have not practiced, a different "
                   "topic (whether the United States should abolish daylight saving time and keep one clock "
                   "year round). Read the opposing pair, then under timed conditions and with no outline "
                   "provided, plan your own SPO first and draft the full essay: a funnel opening that "
                   "establishes context, body paragraphs whose order your plan sets, integrated evidence from "
                   "both sources tied to your thesis, a fair answer to one objection, and a conclusion that "
                   "reaches significance. Scored on all four traits.")),
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
