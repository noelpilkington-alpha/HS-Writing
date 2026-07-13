"""
lesson_t7_essay_assembly.py  -  G10 model lesson, TYPE 7: ESSAY-ASSEMBLY / PLANNING (the composite).

Recrafted to the 17-gate DI bar (T1 precedent). Assembles a Timeback assessment-test (ordered item
sequence) that instantiates the council-adjudicated Type-7 shell against the REAL G10 banks. This is the
type that IS the test: the single-source full essay, where the sub-skills taught in Types 1-6 must run at
once. Binds ONLY LESSON-pool stimuli (no test-pool item is reused as instruction):
  - stimulus  ACC-W910-ARG-OPP-LESSON-CONGESTION (congestion pricing, opposing pair) -> the source read
  - the INDEPENDENT full essay is AUTHORED inline (ref="") on the congestion sources    -> no test-item reuse
  - stimulus  ACC-W910-ARG-OPP-LESSON-DST (daylight saving, opposing pair)             -> partitioned transfer

SRSD shell (Teach/Model/Supported/Independent/Transfer). Model = the async 4-mechanism sequence (clean
annotated before/after -> predict-the-fix with a reveal -> feedback on the student's OWN draft [the FRQ
grader] -> a student-generated diagnosis MODELED on a provided flawed example first). Mnemonic BUILD
(proposal, NOT sourced): Brainstorm to the prompt, Underline your plan (write it out; NOT a mark on the
source), Lay out paragraphs, Integrate the moves you already own, Double-check to the rubric.

Composing-process lens (Hayes & Flower): planning, translating (drafting), and reviewing compete for the
same working memory, so this lesson teaches them as DISTINCT phases and uses the SPO (single-paragraph
outline, scaled to a multi-paragraph outline) to externalize the plan and free working memory for sentence
production. Per Kirschner & Hendrick, this is the highest-composite-load task, so the planning scaffold is
the LAST thing to fade. Two strategic-move gaps are wired in: the funnel opening (establish context, then
thesis) and the reverse-funnel conclusion (synthesize, then reach significance, not a summary).

Fixes vs the prior draft (now GATES): define-before-use (thesis, controlling idea, SPO, counterclaim,
synthesize all defined in plain words with a cue in a TEACH slot before first use); the BUILD U-step is
worded so it never reads as an instruction to mark the source (display-only stimuli); the diagnosis is
MODELED on a provided flawed intro and conclusion and hands the student the same checklist (no blank
"diagnose your own work"); every production prompt is self-contained (stateless items); discrimination is a
labeled Grade-C (A)-(D) minimal pair. Bank-partitioned transfer (congestion pricing -> daylight saving).
All slots map to native Timeback interactions. Runs the QC harness. Dependency-free (stdlib + contract).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report

LESSON = Lesson(
    id="ACC-W910-L-T7-ESSAY-0001", grade="9-10", lesson_type=7,
    unit="G10 U4 - Source-based argument (essay-assembly / planning)",
    title="Build the Whole Essay: Plan First, Then Draft (BUILD)",
    target=("Assemble the sub-skills into a full source-based argument under test conditions: plan with an "
            "SPO (a one-line position plus ordered evidence) scaled to a multi-paragraph outline, draft from "
            "the plan, and manage the composing process. Open with a funnel that establishes context before "
            "the position and close with a conclusion that reaches significance, not a summary. Touches all "
            "four traits, Organization especially."),
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "ACC.W.ARG.5", "ACC.W.INFO.6", "CCSS.W.9-10.1", "OH-ELA.W.9-10.1"],
    provenance={"copyright": "own_authored", "authored": "2026-07-08", "mnemonic_status": "proposal"},
    fade_ledger_moves=["SPO", "funnel-intro", "significance-close", "counterclaim-answer"],
    slots=[
        # ---------------- TEACH: define the terms, then why a plan beats a plunge, then BUILD ----------------
        Slot("TEACH", "teach_card", "The words this lesson uses, and why planning matters",
             body=("Before you build an essay, learn the words this lesson uses. A thesis is a single "
                   "sentence that states the position you will defend in the whole essay. A controlling idea "
                   "is a point that every paragraph has to support, so the thesis is the controlling idea of "
                   "the essay: if a paragraph does not support the thesis, it does not belong. A counterclaim "
                   "is a reason someone on the other side would give against your position, and a strong essay "
                   "names one and answers it fairly. An SPO, which stands for single-paragraph outline, is a "
                   "brief written plan: one line for the thesis, then one line for each body point in order, "
                   "with the source evidence each point will use; you scale it up to plan a multi-paragraph "
                   "essay. To synthesize means to pull your separate reasons back together into one connected "
                   "point instead of just listing them. "
                   "Now, why planning matters. On the test you get one source set, one prompt, and a single "
                   "sitting to produce a whole essay. That is the hardest job in writing because three jobs "
                   "fight for room in your head at once: deciding WHAT to say (planning), turning it into "
                   "sentences (drafting), and checking whether it works (reviewing). Try to do all three at "
                   "once and you stall. The fix is to make them separate phases: plan on paper first, then "
                   "draft from the plan, then review against the rubric. A written plan is not wasted time. It "
                   "holds the order for you so your working memory is free to build good sentences, and it is "
                   "the last thing you should give up under time pressure.")),
        Slot("TEACH", "teach_card", "The BUILD strategy, and the two framing moves",
             body=("Our cue for the whole job is BUILD. B, Brainstorm to the prompt: read what the prompt "
                   "actually asks and decide which side you can defend from the source. U, Underline your "
                   "plan: single out your plan by writing a one-line thesis first, then listing your body "
                   "points in order with the evidence each will use. (You write this plan on your own paper. "
                   "It is not a mark you make on the source.) L, Lay out paragraphs: turn each outline line "
                   "into one paragraph. I, Integrate the moves you already own: a defensible position, source "
                   "evidence tied back to that position, and a fair answer to a counterclaim. D, Double-check "
                   "to the rubric: a review pass for development, order, and style. "
                   "Two framing moves win the top band and are easy to skip under pressure. First, open with "
                   "a funnel: give the reader a sentence or two of context on the issue, and only then state "
                   "your thesis, so the claim lands in a setting instead of out of nowhere. Second, close with "
                   "a reverse funnel: synthesize, meaning pull your reasons back together into one point, then "
                   "reach significance by answering the question so what, why this position matters beyond the "
                   "page. A conclusion that only restates the introduction stays mid-band. Goal for today: "
                   "plan first, draft from the plan, and frame the essay with a context opening and a "
                   "significance close.")),
        Slot("TEACH", "stimulus_display", "Read both sides of the congestion-pricing source",
             ref="ACC-W910-ARG-OPP-LESSON-CONGESTION", bank="congestion_pricing",
             body=("Here is the opposing pair on whether cities should charge tolls to drive downtown during "
                   "the busiest hours, which is called congestion pricing. Read both sides, one at a time. As "
                   "you read, note the single strongest fact on each side, for example the road-use and "
                   "clean-air figures on the side that favors the toll, and the household-cost and uneven-"
                   "transit figures on the side against it. You are gathering the raw material your plan will "
                   "order, not deciding the whole essay yet. The sources stay on screen while you plan.")),

        # ---------------- MODEL: clean annotated before/after, then predict-the-fix ----------------
        Slot("MODEL", "annotated_before_after", "Watch a plunged-in pile become a planned, ordered essay",
             bank="congestion_pricing",
             body=("BEFORE (plunges in, no plan): 'Traffic is bad. The FHWA says Americans drive more than 3 "
                   "trillion miles a year. Congestion pricing charges a toll. But a toll costs a low-wage "
                   "worker the same as a rich driver. Transportation is a huge household expense. Also transit "
                   "is uneven. So congestion pricing is complicated and there are good points on both sides.' "
                   "Why it fails: the writer started typing before deciding anything, so the sentences pile up "
                   "(fact, counter-fact, fact) and build toward nothing. There is no thesis, the order is "
                   "random, and the ending just shrugs. "
                   "AFTER (an SPO plan sets the order first, then the writer drafts from it). "
                   "[SPO plan] Thesis: cities should charge a congestion toll, because a crowded free road is "
                   "overused and the toll money can build the transit that gives people a real way out of the "
                   "car. Body 1: the road is limited space (FHWA: more than 3 trillion miles a year, much of "
                   "it in dense areas with no room for new lanes), so pricing the busiest hour makes sense. "
                   "Body 2: the counterclaim, a flat toll hits low-wage workers hardest and transit is uneven "
                   "(Census: most commuters still drive, many alone), answered by pairing the toll with "
                   "low-income discounts and real transit built from the proceeds. Body 3: cleaner air for the "
                   "people who live downtown (EPA: transportation is the largest source of US greenhouse gas "
                   "emissions). "
                   "[Drafted intro, funnel] 'Every weekday morning the same downtown streets fill with cars "
                   "that crawl for blocks and burn fuel going nowhere [context]. Cities should charge a "
                   "congestion toll during the busiest hours, because a road that is both crowded and free "
                   "gets overused, and the money a toll raises can build the transit that lets people leave "
                   "the car at home [thesis].' "
                   "[Drafted conclusion, reverse funnel] 'The wasted hours and the dirty air are not distant "
                   "worries; they are measured on those streets right now [synthesis, the reasons pulled back "
                   "together]. Pricing the crowded hour matters because it turns a hidden cost we already pay, "
                   "in lost time and fouled air, into money a city can spend on a way out of the traffic "
                   "[significance, the so-what].' "
                   "Reading the labels: the AFTER never wanders because the plan set the order first; the "
                   "intro situates the issue before the claim [context], each body paragraph is one planned "
                   "point with its evidence tied to the thesis, and the conclusion pulls the reasons together "
                   "[synthesis] and then reaches significance instead of restating the opening. That is the "
                   "plan doing the work drafting cannot do under pressure.")),
        Slot("MODEL", "predict_the_fix", "Predict what this essay is missing before the reveal",
             bank="congestion_pricing",
             body=("Diagnose this draft before we reveal the fix. A student writes an opening sentence that "
                   "jumps straight to 'I think cities should charge congestion tolls,' three body paragraphs "
                   "of facts in no clear order, and a last paragraph that reads 'In conclusion, cities should "
                   "charge congestion tolls because they are better.' What is the single biggest problem? "
                   "(A) it has no plan, so the body has no order and the conclusion only restates the intro "
                   "instead of reaching significance  (B) the sentences are too short  (C) it uses too many "
                   "facts from the source  (D) it should not name the other side at all"),
             feedback=("Correct: A. The trouble is not the sentences or the facts, it is the missing plan. "
                       "Because the writer never built an SPO, the body points sit in random order and nothing "
                       "builds. And the conclusion just repeats the opening claim, so it stalls at mid-band. "
                       "The fix is to plan the order first (thesis, then ordered body points with evidence) "
                       "and to close by answering so what: why the position matters, not just restating it. A "
                       "context opening and a significance close are the two framing moves this draft skipped. "
                       "B and C are not the real problem, and D is wrong because answering a counterclaim "
                       "makes an argument stronger, not weaker.")),

        # ---------------- SUPPORTED: labeled Grade-C discrimination -> scaffolded plan -> modeled diagnosis --
        Slot("SUPPORTED", "discrimination", "Which opening shows a plan driving the essay? (minimal pair)",
             labeled_grade_c=True, bank="congestion_pricing",
             body=("Discriminate before you produce (a labeled Grade-C design bet). Here are four openings for "
                   "the same congestion-pricing essay. Which one is a funnel opening whose plan you can see "
                   "driving the essay, giving context and then a clear thesis? "
                   "(A) One sentence of context on the daily downtown gridlock, then a clear thesis that "
                   "cities should charge a congestion toll.  "
                   "(B) A list of three facts from the source, ending without stating any position.  "
                   "(C) 'This essay is about congestion pricing,' then straight into the first fact.  "
                   "(D) A personal story about being stuck in traffic once, never mentioning the sources or a "
                   "position. "
                   "Correct: A. Only A gives the reader context and then states the position the essay will "
                   "defend, so you can see the plan. B never takes a side, so nothing drives the order; C "
                   "announces the topic but skips both context and a thesis; D is off-source and takes no "
                   "position.")),
        Slot("SUPPORTED", "production_frq", "Complete the partial SPO plan (scaffold)",
             bank="congestion_pricing", rubric_ref="rc.4trait", scored=True, unit="sentence",
             body=("Guided planning. Here is a partial SPO for the congestion-pricing essay with the thesis "
                   "and the first body line filled in for you. Thesis (given): cities should charge a "
                   "congestion toll, because a crowded free road is overused and the toll money can build the "
                   "transit that gives people a way out of the car. Body 1 (given): the road is limited space "
                   "with no room for new lanes (FHWA road-use figures). Complete the plan: write Body 2 and "
                   "Body 3 as one line each, naming the point AND the specific source evidence each will use, "
                   "and order them so the essay builds toward the thesis. Product goal: two body lines, each "
                   "with a point plus named source evidence, in a build order. You are only planning here, "
                   "not drafting sentences. Scored on organization and support.")),
        Slot("SUPPORTED", "diagnosis_frq", "Diagnose a flawed intro and conclusion (modeled, then you)",
             bank="congestion_pricing", scored=True,
             body=("First watch the check run on a flawed opening and closing, then run the same checklist "
                   "yourself on that example. Flawed intro: 'I think cities should charge congestion tolls.' "
                   "Flawed conclusion: 'In conclusion, cities should charge congestion tolls because it is "
                   "better.' Now the checklist, step by step. Step 1, context: does the intro give the reader "
                   "any context before the thesis? No, it jumps straight to the claim, so the repair is to add "
                   "a sentence of context first. Step 2, thesis: is there a clear position? Yes, but it "
                   "arrives cold, with no setting. Step 3, significance: does the conclusion answer so what, "
                   "why the position matters, or does it only restate the opening? It only restates, so it "
                   "stalls at mid-band. Now you: in two or three sentences, name the two moves this intro and "
                   "conclusion are missing (context and significance), and write one repair sentence for each, "
                   "using the checklist above. Scored on the accuracy of your diagnosis and repairs.")),

        # ---------------- INDEPENDENT: plan from scratch, then the full authored essay ----------------
        Slot("INDEPENDENT", "production_frq", "Build the full SPO plan from scratch (scaffold faded)",
             bank="congestion_pricing", rubric_ref="rc.4trait", scored=True, unit="sentence",
             body=("Independent planning, no outline provided. For the congestion-pricing prompt, write your "
                   "own complete SPO. Give a one-line thesis that takes a defensible side, then list two or "
                   "three body points in order, each naming the specific source evidence it will use and how "
                   "that evidence ties to the thesis. In one phrase each, note how you will open with context "
                   "and how your conclusion will reach significance. Product goal: a thesis line plus ordered "
                   "body lines with named evidence, plus the two framing notes. This plan is the map you will "
                   "draft from next. Scored on organization and support.")),
        Slot("INDEPENDENT", "production_frq", "Draft ONE body paragraph from your plan (the paragraph rung)",
             bank="congestion_pricing", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=("Before you write the whole essay, turn ONE line of your plan into a full body paragraph. "
                   "Pick your strongest body point from the SPO and draft it: a topic sentence that states the "
                   "point, at least one piece of source evidence that names who reported it and is tied back to "
                   "your thesis so the reader sees why it matters, and a sentence explaining its importance. "
                   "This is the plan-to-paragraph step: you proved you can plan the whole essay, now prove you "
                   "can build one of its paragraphs before you build all of them. Product goal: one focused "
                   "body paragraph with a topic sentence, one piece of source evidence tied to the thesis, and "
                   "an explanation of why it matters. Scored on Evidence/Development.")),
        Slot("INDEPENDENT", "production_frq", "Draft the full essay (authored, on the congestion sources)",
             bank="congestion_pricing", rubric_ref="rc.staar", scored=True, unit="essay",
             body=("Independent performance, timed. Write the full argumentative essay on whether cities "
                   "should charge tolls to drive downtown during the busiest hours, using the congestion-"
                   "pricing sources. Begin by jotting a quick one-line thesis and an ordered list of body "
                   "points (an SPO), then write the essay from that plan. Open with a funnel that establishes "
                   "context before your thesis, develop each body paragraph with source evidence tied to the "
                   "thesis, answer at least one counterclaim from the side you argue against, and close with a "
                   "conclusion that synthesizes your reasons and reaches significance rather than restating "
                   "your opening. Finish with a quick double-check for development, order, and style. Product "
                   "goal: a context intro with a clear thesis, ordered evidence-based body paragraphs, one "
                   "answered counterclaim, and a significance conclusion. Scored on all four traits, "
                   "Organization especially.")),

        # ---------------- TRANSFER: full timed essay, partitioned content bank ----------------
        Slot("TRANSFER", "production_frq", "Plan and draft a full timed essay on a NEW topic",
             ref="ACC-W910-ARG-OPP-LESSON-DST", bank="daylight_saving", rubric_ref="rc.ohio", scored=True, unit="essay",
             body=("Transfer: run the whole BUILD process on a source you have not practiced, a different "
                   "topic (whether the United States should abolish daylight saving time and keep one clock "
                   "year round). Read the opposing pair, then under timed conditions and with no outline "
                   "provided, build your own SPO first and draft the full essay: a funnel opening that "
                   "establishes context, body paragraphs whose order your plan sets, source evidence from both "
                   "sides tied to your thesis, a fair answer to one counterclaim, and a conclusion that "
                   "synthesizes your reasons and reaches significance. Product goal: a planned, context-"
                   "framed, evidence-based essay with an answered counterclaim and a significance close. "
                   "Scored on all four traits.")),
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
