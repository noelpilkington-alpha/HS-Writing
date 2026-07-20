"""
lesson_g9_l20_multi_para_coherence.py  -  G9 KC C.9.04, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD, ceiling essay).

G9 course L20 (Unit 4, guided). Multi-paragraph coherence + order (B3): order the body paragraphs so each
builds on the last, with transitions BETWEEN paragraphs. Locked L01 template. ESSAY-TIER binds full sources.
Taught: VOLCANOES (full) -> transfer: SCHOOLLUNCH (full, partitioned). rc.staar, unit="multi_paragraph".
BUILD=proposal. No coping-model persona; no source markup; no prior-work ref; no em dashes. Runs QC on execution.
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
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> paragraphs in a random order, no links between them</span>'
    '<p style="margin:8px 0 0;font-size:15px">P1: Volcanoes can erupt violently. P2: Deep underground, heat '
    'melts rock into magma. P3: Scientists watch for warning signs. P2 belongs before P1, and nothing connects '
    'the paragraphs.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The cause (magma forms) comes after the effect '
    '(eruption), and each paragraph starts cold. The essay jumps around instead of building.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> ordered so each paragraph builds, linked between them</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">CAUSE FIRST</span> P1: Deep underground, heat melts rock into magma. '
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">THEN EFFECT</span> P2: When that magma rises, a volcano can erupt violently. '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">LINK</span> P3: Because eruptions are dangerous, scientists watch for warning signs.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Cause before effect, and each paragraph opens by '
    'linking to the one before ("when that magma," "because eruptions"). Now the essay builds.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C904-0020", grade="9-10", lesson_type=7,
    unit="G9 U4 - Build essay (multi-paragraph coherence and order)",
    title="Order the Paragraphs So the Essay Builds",
    target=("Order the body paragraphs so each builds on the one before (for example cause before effect), and "
            "open each with a transition that links it to the last. Written across a multi-paragraph essay. "
            "Trait: Organization."),
    acc_tags=["ACC.W.PROD.1", "CCSS.W.9-10.4"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12",
                "mnemonic_status": "proposal", "kc": "C.9.04", "sot": "icm course-G9.md L20",
                "taught_stimulus": "ACC-W910-INFO-LESSON-VOLCANOES",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-SCHOOLLUNCH",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": "locked L01 template; ESSAY-TIER binds full sources.",
                "council": ("T7/BUILD structure rung: introduces B3 multi-paragraph coherence (order so each "
                            "paragraph builds; transitions BETWEEN paragraphs). builds-vs-jumps discrimination "
                            "labeled Grade-C. BUILD=proposal; unit=multi_paragraph.")},
    fade_ledger_moves=["order-paragraphs-to-build", "transitions-between-paragraphs"],
    slots=[
        Slot("TEACH", "teach_card", "Paragraphs need an order and links, like sentences do",
             body=("A paragraph connects its sentences; an essay must connect its paragraphs the same way. Two "
                   "things make a multi-paragraph essay cohere. First, ORDER: put the paragraphs in a sequence "
                   "where each builds on the one before, cause before effect, background before argument, "
                   "problem before solution. Second, LINKS: open each body paragraph with a transition that "
                   "ties it to the paragraph before, so the reader feels the essay moving, not restarting. A "
                   "weak essay has good paragraphs in a random order, each starting cold, so the essay jumps "
                   "around. A strong one orders them to build and links them at the seams. The trap is treating "
                   "paragraphs as separate boxes. Goal today: put paragraphs in a building order and link them "
                   "with transitions between paragraphs.")),
        Slot("TEACH", "stimulus_display", "Read the source: volcanoes",
             ref="ACC-W910-INFO-LESSON-VOLCANOES", bank="volcanoes",
             body=("Read this source about volcanoes. Because your job is to ORDER paragraphs, read the whole "
                   "thing and notice the natural sequence, what causes what, what comes first. You will use "
                   "that to order body paragraphs. The text stays on screen while you work.")),
        Slot("TEACH", "discrimination", "Which order lets the essay build?",
             ref="", labeled_grade_c=True, bank="volcanoes",
             body=("Sort these before you order (spotting the target first, a Grade-C design bet we label as a "
                   "bet, not a proven ingredient). Which paragraph order lets the essay BUILD? "
                   "(A) P1: Volcanoes can erupt violently and bury a town in ash. P2: Heat deep underground melts solid rock into magma. P3: Scientists watch active volcanoes for warning signs.  "
                   "(B) P1: Heat underground melts rock into magma. P2: When that magma rises, a volcano can "
                   "erupt. P3: Because eruptions are dangerous, scientists watch for warning signs. "
                   "Correct: B. (A) puts the effect (eruption) before its cause (magma forms), so it jumps "
                   "backward. (B) goes cause, then effect, then response, each paragraph building on the last, "
                   "and links them ('when that magma,' 'because eruptions'). Ordering to build is the move.")),
        Slot("MODEL", "annotated_before_after", "Watch scrambled paragraphs get ordered and linked",
             bank="volcanoes",
             body=("Here are paragraphs in a jumbled order being resequenced to build, with links added between "
                   "them. Read the BEFORE, then the AFTER, and notice cause moves before effect and each "
                   "paragraph opens with a link." + BEFORE_AFTER_HTML +
                   " The BEFORE puts effect before cause and starts each paragraph cold. The AFTER orders "
                   "cause-effect-response and links the seams. Ordering plus linking is the move.")),
        Slot("MODEL", "predict_the_fix", "What does this multi-paragraph draft most need?",
             bank="volcanoes",
             body=("Diagnose before the reveal. An essay has three body paragraphs: P1 says eruptions destroy "
                   "towns; P2 explains how magma forms deep underground; P3 says people build near volcanoes "
                   "for fertile soil. Which single change would most improve the structure? "
                   "(A) reorder so the cause (magma forms) comes before the effect (eruptions destroy towns), "
                   "and add transitions linking the paragraphs  "
                   "(B) add a fourth body paragraph that covers one more fact about volcanoes, since a longer essay with more paragraphs feels more complete  "
                   "(C) make each body paragraph longer by adding several more sentences and specific details, so every point is explained more fully  "
                   "(D) delete the paragraph about fertile soil, because it explains why people live near volcanoes instead of how the eruptions happen"),
             feedback=("Correct: A. The paragraphs are in an order that puts an effect before its cause and "
                       "starts each one cold, so the essay jumps. The fix is to reorder (cause before effect) "
                       "and link the paragraphs with transitions. A fourth paragraph (B) or longer paragraphs "
                       "(C) do not fix the order; deleting content (D) removes a relevant point rather than "
                       "sequencing it.")),
        Slot("SUPPORTED", "production_frq", "Order three points and link the first two",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=("You are given three body points about volcanoes, out of order: (a) scientists monitor for "
                   "warning signs; (b) heat underground melts rock into magma; (c) rising magma can erupt "
                   "violently. Write the correct building ORDER as three labeled lines, then write the opening "
                   "transition sentence for the second and third paragraphs so each links to the one before. "
                   "Goal: a building order plus links between paragraphs. Scored on Organization.")),
        Slot("MODEL", "diagnosis_frq", "Check a fresh plan for order and links",
             ref="", bank="volcanoes", scored=True,
             body=("First watch the check run on a provided plan, then run it on a fresh one of your own. "
                   "Provided plan order: P1 eruptions are dangerous; P2 magma forms; P3 monitoring helps. Run "
                   "the check step by step. Step 1, does each paragraph build on the one before? No, P1 (effect) "
                   "comes before P2 (cause), so reorder to magma, eruption, monitoring. Step 2, are there links "
                   "between paragraphs? No, add opening transitions. Now you: write a fresh three-point order "
                   "for a volcano essay, then run the same two checks, building order? links between? Fix any "
                   "that fail. Finish by naming the relationship your order follows (cause to effect).")),
        Slot("INDEPENDENT", "production_frq", "Order and link a full set of body paragraphs",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=("On your own now. For an essay explaining how volcanoes form and erupt, write the body as "
                   "THREE ordered paragraph plans (one to two sentences each) in a building order, and open the "
                   "second and third with a transition that links to the paragraph before. Before you submit, "
                   "check: does each paragraph build on the last, and does each after the first open with a "
                   "link? Fix any that fail before you submit. Scored on Organization.")),
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: free school meals",
             ref="ACC-W910-ARG-LESSON-SCHOOLLUNCH", bank="school_lunch",
             body=("Read this new source about free school meals. Because your job is to ORDER paragraphs, read "
                   "the whole thing and think about a building order for an argument (for example, problem, "
                   "then benefit, then a response to the cost concern). The text stays on screen while you "
                   "work.")),
        Slot("TRANSFER", "production_frq", "Order and link body paragraphs on a NEW topic",
             ref="", bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=("New topic. For an argument about free school meals, write the body as THREE ordered "
                   "paragraph plans in a building order (for example: the problem of classroom hunger, then the "
                   "benefit of universal meals, then a response to the cost concern), and link the second and "
                   "third to the paragraph before. Same ordering-and-linking move as the volcano essay, new "
                   "topic. Scored on Organization.")),
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
