"""
lesson_g9_l26_gate_essay.py  -  G9 KC C.9.04, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD, ceiling essay). COURSE GATE.

G9 course L26 (Unit 4, GATE): the course-terminal task. Plan and write a complete single-source essay from
scratch, minimal scaffolding, on a stimulus reserved for the gate. UNTIMED (Timeback has no timer; the real
rigor is the cold, full, self-directed production, not a clock). The shell is a brief final-review retrieval
(TEACH = the checklist the student now owns; MODEL = one last discrimination + predict-the-fix), then the full
cold essay. Locked L01 template. ESSAY-TIER binds the FULL source. Bound: PHOTOSYNTHESIS (full) held for the
gate (moves were practiced across the course, but the full single-source essay on this prompt is the fresh
terminal task) -> transfer: HIGHWAYS (full, partitioned second cold essay, F8 cold-gate swap). rc.staar. BUILD=proposal.
No coping-model persona; no source markup; no prior-work ref; no em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report

BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> a body paragraph that fails the self-check</span>'
    '<p style="margin:8px 0 0;font-size:15px">Photosynthesis is how a plant makes food, and it is really '
    'important. About half of the oxygen on Earth comes from the ocean. The leaves have a green coloring in '
    'them. Plants matter a lot to living things.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The idea is vague, the ocean-oxygen fact is dropped '
    'in with no source and no link to making food, and no sentence explains how light actually becomes food.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> the same paragraph rebuilt to pass it</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">CONTROLLING IDEA</span> Inside its leaves, a plant turns sunlight into food through the '
      'reaction called photosynthesis. '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">EVIDENCE</span> The U.S. Department of Energy explains that the reaction uses only '
      'water, carbon dioxide, and sunlight, and the green chlorophyll in the leaves captures that sunlight. '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">EXPLANATION</span> That captured light energy is what lets the plant rearrange water '
      'and carbon dioxide into sugar, so the sunlight is not merely warming the leaf but powering the chemistry '
      'that builds the food a plant needs.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same topic, but now a controlling idea sets the '
    'focus, the evidence is attributed to its source, and an explanation shows how the light becomes food.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C904-0026", grade="9-10", lesson_type=7,
    unit="G9 U4 - GATE: single-source essay (course terminal task)",
    title="G9 Gate: Write a Complete Single-Source Essay",
    target=("The course gate: independently plan, draft, and self-check a complete single-source essay (argument "
            "or informational, as the prompt's verb sets), assembling every move the course taught. Written at "
            "the essay, untimed. Trait: Development/Organization/Purpose."),
    acc_tags=["ACC.W.PROD.1", "ACC.W.ARG.5", "ACC.W.INFO.2", "CCSS.W.9-10.1", "CCSS.W.9-10.2", "CCSS.W.9-10.4"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12",
                "mnemonic_status": "proposal", "kc": "C.9.04", "sot": "icm course-G9.md L26 (COURSE GATE)",
                "taught_stimulus": "ACC-W910-INFO-LESSON-PHOTOSYNTHESIS",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-HIGHWAYS",
                "f8_note": "2026-07-18 F8 cold-gate swap: 2nd cold write changed from VOLCANOES (used in 7 prior G9 lessons) to HIGHWAYS (Interstate system, 0 prior G9 use, verified 46,876-mi figure) so the gate tests genuinely cold transfer.",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": "locked L01 template; ESSAY-TIER binds full sources; GATE = cold full production, UNTIMED (no Timeback timer).",
                "council": ("T7/BUILD COURSE GATE: minimal-scaffold terminal task. Shell present as a final-"
                            "review retrieval (brief TEACH checklist + one MODEL discrimination/predict-the-fix "
                            "+ diagnosis), then the full cold essay. plan-and-check-vs-skip discrimination "
                            "labeled Grade-C. Untimed: the rigor is the cold, self-directed full production, "
                            "not a clock. BUILD=proposal; unit=essay.")},
    fade_ledger_moves=["independent-full-essay", "run-the-whole-routine"],
    slots=[
        Slot("TEACH", "teach_card", "The routine you now own",
             body=("This is the course gate: you will write a complete essay on your own, using everything the "
                   "course taught, in this routine. PLAN first with a single-paragraph outline, which is a "
                   "compact plan naming a one-line thesis plus ordered body points, each with evidence. DRAFT "
                   "from the plan: an introduction that frames the thesis, one body paragraph per point (each a "
                   "claim, attributed evidence, and a warrant; a warrant is a sentence that explains why the "
                   "evidence supports the claim), ordered so they build and linked at the seams, and a "
                   "conclusion that lands the upshot. Then CHECK: reread each paragraph against the list, does "
                   "it have a claim, attributed evidence, and a warrant, and do the paragraphs build and link? "
                   "There is no clock; take the time you need. Goal: run the whole routine once, on your own.")),
        Slot("TEACH", "teach_card", "Read the verb, pick the mode, then build",
             body=("One decision comes first: read the task verb. If it says argue or 'should ... ?', write an "
                   "argument, a thesis that takes a side, defended paragraph by paragraph. If it says explain or "
                   "describe, write an informational essay, a controlling idea that sets a focus and takes no "
                   "side, with the body walking through the parts. A controlling idea means one sentence naming "
                   "a focusing angle without taking a side. Get the mode right, then build the essay the same "
                   "way either way: plan, draft from the plan, self-check. The whole course led here.")),
        Slot("TEACH", "stimulus_display", "Read the source: photosynthesis",
             ref="ACC-W910-INFO-LESSON-PHOTOSYNTHESIS", bank="photosynthesis",
             body=("Read this source about photosynthesis. This is the gate: you will write a complete essay "
                   "explaining how photosynthesis turns light into food, using the source for evidence. Read "
                   "the whole thing, gather a focusing idea and the facts (with sources) you will use, and plan "
                   "before you draft. The text stays on screen while you work.")),
        Slot("TEACH", "discrimination", "Which approach earns the gate score?",
             ref="", labeled_grade_c=True, bank="photosynthesis",
             body=("One last sort before you write (spotting the target first, a Grade-C design bet we label as "
                   "a bet, not a proven ingredient). Which approach earns the score on the terminal essay? "
                   "(A) Read the prompt, plan a thesis and ordered points with evidence, draft from the plan "
                   "(intro, complete linked body paragraphs, upshot conclusion), then self-check and fix gaps.  "
                   "(B) Read the prompt and start drafting right away with no plan, writing whatever comes to "
                   "mind and adding sentences until it feels long enough, then submit without rereading for gaps. "
                   "Correct: A. The gate rewards the full routine, plan, build from the plan, self-check. (B) "
                   "skips the plan and the check, so the essay drifts and gaps go uncaught. Running the whole "
                   "routine is the move.")),
        Slot("MODEL", "annotated_before_after", "Watch the full routine replace skip-and-submit",
             bank="photosynthesis",
             body=("Here is skip-and-submit replaced by the full routine on the gate essay. Read the BEFORE, "
                   "then the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE skips the plan and the check. The AFTER plans, drafts from the plan, and "
                   "self-checks. Running the whole routine is what the gate measures.")),
        Slot("MODEL", "predict_the_fix", "What does this gate approach most need?",
             bank="photosynthesis",
             body=("Predict before the reveal. A student says: 'It is the final essay, so I will just write "
                   "fast and turn it in.' On the terminal task, which single change would most improve the "
                   "result? "
                   "(A) plan the thesis and ordered points first, then draft from the plan, then self-check "
                   "each paragraph before submitting  "
                   "(B) write a much longer introduction that restates the whole prompt and previews every "
                   "point before the body paragraphs begin  "
                   "(C) keep adding more body paragraphs onto the end until the finished essay finally looks "
                   "long enough, then hand it in  "
                   "(D) swap in bigger, more advanced vocabulary words all the way through so the finished "
                   "writing sounds more impressive"),
             feedback=("Correct: A. On the terminal essay, skipping the plan and the self-check is the main "
                       "cause of drifting paragraphs and uncaught gaps. The fix is the full routine: plan, "
                       "draft from the plan, self-check. A longer intro (B), extra paragraphs (C), or fancier "
                       "words (D) do not supply the plan and check the essay needs. There is no clock, so "
                       "there is time to do this.")),
        Slot("SUPPORTED", "production_frq", "Plan your gate essay",
             ref="", bank="photosynthesis", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=("Plan your gate essay. The task: explain how photosynthesis turns light into food. Write a "
                   "single-paragraph outline: a one-line controlling-idea THESIS (a focus, no side), then THREE "
                   "ordered PARTS to explain, each with its evidence from the source. This plan is what you "
                   "will build the full essay from in the next step. Scored on Organization.")),
        Slot("MODEL", "diagnosis_frq", "Self-check a plan before the full write",
             ref="", bank="photosynthesis", scored=True,
             body=("First watch the check run on a provided plan, then run it on your own. Provided plan: "
                   "'Thesis: photosynthesis is cool. Parts: sun, water, sugar.' Run the check step by step. "
                   "Step 1, thesis a focusing idea with no side? No, 'cool' is an opinion, so make it a focus "
                   "(how light becomes food). Step 2, parts ordered and specific? Loosely, so name them as real "
                   "steps (inputs, the conversion, outputs). Step 3, evidence per part? No, attach sources. Now "
                   "you: write a fresh thesis plus three parts for your gate essay, then run the same three "
                   "checks and fix any that fail. Finish by confirming your thesis sets a focus and takes no "
                   "side.")),
        Slot("INDEPENDENT", "production_frq", "GATE: write the complete essay",
             ref="", bank="photosynthesis", rubric_ref="rc.staar", scored=True, unit="essay",
             body=("The gate. Write a complete essay explaining how photosynthesis turns light into food, built "
                   "from your plan: an INTRODUCTION that frames the controlling idea, THREE body paragraphs "
                   "that each explain one part with attributed evidence (ordered to build and linked), and a "
                   "CONCLUSION that lands the upshot, with no side taken. Before you submit, run your self-"
                   "check: does every paragraph explain with a claim and attributed evidence and a warrant, do "
                   "the paragraphs build and link, does the conclusion add an upshot, and did I take no side? "
                   "Fix any gaps before you submit. There is no time limit; take the time you need. Scored on "
                   "Development/Organization/Purpose.")),
        Slot("TRANSFER", "stimulus_display", "A second gate source: the Interstate Highway System",
             ref="ACC-W910-INFO-LESSON-HIGHWAYS", bank="highways",
             body=("Read this second source about how the Interstate Highway System was built for another "
                   "complete essay. This is a topic the course has not used before, so it is a genuinely cold "
                   "gate: read the whole thing, gather a focusing idea and evidence (with sources), and plan "
                   "before you draft. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "GATE: write a complete essay on a NEW source",
             ref="", bank="highways", rubric_ref="rc.staar", scored=True, unit="essay",
             body=("Write a second complete essay explaining how the Interstate Highway System was built and why "
                   "it mattered, built from a plan: an intro that frames the controlling idea, three body "
                   "paragraphs explaining the parts with attributed evidence (ordered and linked), and a "
                   "conclusion that lands the upshot, no side taken. Run the same self-check before submitting. "
                   "Same full routine as the photosynthesis essay, a new source. No time limit; take the time "
                   "you need. Scored on Development/Organization/Purpose.")),
    ],
)

LESSONS = [LESSON]

if __name__ == "__main__":
    ok = True
    for L in LESSONS:
        qc_lesson(L); print(qc_report(L)); print(); ok = ok and L.qc["passed"]
    passed = sum(1 for L in LESSONS if L.qc["passed"])
    print(f"{passed}/{len(LESSONS)} PASS")
    sys.exit(0 if ok else 1)
