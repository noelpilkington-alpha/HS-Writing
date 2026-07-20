"""
lesson_g9_l19_spo_plan.py  -  G9 KC C.9.04, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD, ceiling essay).

G9 course L19 (Unit 4, intro). Plan an essay with a single-paragraph outline (SPO, B2): a one-line thesis plus
ordered body lines with named evidence, before drafting. Locked L01 template. ESSAY-TIER: binds the FULL
source. Taught: WATER-CYCLE (full) -> transfer: VOLCANOES (full, partitioned). rc.staar, unit="multi_paragraph"
(the plan scales to a multi-paragraph essay). BUILD=proposal. "SPO" is a gated tech term (defined in TEACH).
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
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> a vague plan that will not steer a draft</span>'
    '<p style="margin:8px 0 0;font-size:15px">Plan: Write about the water cycle. Say it is important. Add some '
    'facts. Write a good ending.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">This is a to-do list, not a plan. It names no '
    'thesis, no ordered points, and no specific evidence, so it cannot steer a draft.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> a single-paragraph outline that steers the draft</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">THESIS</span> The water cycle constantly recycles Earth\'s water. '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">POINT 1</span> Evaporation lifts water into the air (USGS). '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">POINT 2</span> Condensation and precipitation return it (USGS). '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">POINT 3</span> Collection stores it until the loop repeats (USGS).</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">A one-line thesis plus ordered points, each with '
    'named evidence. This plan can actually steer paragraph by paragraph.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C904-0019", grade="9-10", lesson_type=7,
    unit="G9 U4 - Build essay (single-paragraph-outline plan)",
    title="Plan Before You Draft: The Single-Paragraph Outline",
    target=("Plan an essay with a single-paragraph outline: a one-line thesis plus ordered body points, each "
            "with named evidence, so the plan can steer the draft. Written as a plan scaling to a "
            "multi-paragraph essay. Trait: Organization."),
    acc_tags=["ACC.W.PROD.1", "CCSS.W.9-10.4"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12",
                "mnemonic_status": "proposal", "kc": "C.9.04", "sot": "icm course-G9.md L19",
                "taught_stimulus": "ACC-W910-INFO-LESSON-WATER-CYCLE",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-VOLCANOES",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": "locked L01 template; ESSAY-TIER binds full sources.",
                "council": ("T7/BUILD planning rung: introduces B2 single-paragraph outline (SPO): one-line "
                            "thesis + ordered body points with named evidence. steers-vs-vague-plan "
                            "discrimination labeled Grade-C. SPO defined in TEACH. BUILD=proposal; "
                            "unit=multi_paragraph (the plan for a multi-paragraph essay).")},
    fade_ledger_moves=["single-paragraph-outline", "thesis-plus-ordered-points-with-evidence"],
    slots=[
        Slot("TEACH", "teach_card", "A plan that can actually steer a draft",
             body=("Before you draft an essay, make a plan that can steer it. The tool is the single-paragraph "
                   "outline. An SPO is a compact plan written in one block: a one-line thesis at the top, then "
                   "one line per body paragraph, each naming the point and the evidence that paragraph will "
                   "use. The difference between a real plan and a to-do list is specifics. 'Write about the "
                   "water cycle, add facts, end well' is a to-do list, it names no thesis, no order, and no "
                   "evidence, so it cannot steer anything. An SPO names the thesis, puts the points in order, "
                   "and attaches evidence to each, so when you draft you already know what each paragraph "
                   "argues and proves. The trap is skipping the plan or writing a vague one. Goal today: write "
                   "an SPO with a one-line thesis and ordered points that each name evidence.")),
        Slot("TEACH", "stimulus_display", "Read the source: the water cycle",
             ref="ACC-W910-INFO-LESSON-WATER-CYCLE", bank="water_cycle",
             body=("Read this source about the water cycle. Because your job is to PLAN an essay from it, read "
                   "the whole thing and note the main stages and the facts that go with each. You will turn "
                   "those into ordered points with named evidence. The text stays on screen while you work.")),
        Slot("TEACH", "discrimination", "Which one is a plan that can steer a draft?",
             ref="", labeled_grade_c=True, bank="water_cycle",
             body=("Sort these before you plan (spotting the target first, a Grade-C design bet we label as a "
                   "bet, not a proven ingredient). Which one is a real single-paragraph outline that could "
                   "steer a draft? "
                   "(A) Write about the water cycle. Say why it matters and why it is a big deal. Add some "
                   "facts from the reading. Explain the different parts. Use a few good examples. Finish with "
                   "a strong ending that ties it all together.  "
                   "(B) Thesis: the water cycle recycles Earth's water. Point 1: evaporation lifts water (USGS). "
                   "Point 2: condensation and precipitation return it (USGS). Point 3: collection stores it "
                   "until the loop repeats (USGS). "
                   "Correct: B. (A) is a to-do list, no thesis, no order, no specific evidence, so it steers "
                   "nothing. (B) names a one-line thesis, ordered points, and the evidence for each, so a "
                   "drafter knows exactly what each paragraph does. That is an SPO.")),
        Slot("MODEL", "annotated_before_after", "Watch a to-do list become a single-paragraph outline",
             bank="water_cycle",
             body=("Here is a vague to-do list being rebuilt into an SPO. Read the BEFORE, then the AFTER, and "
                   "notice the thesis, ordered points, and named evidence appear." + BEFORE_AFTER_HTML +
                   " The BEFORE cannot steer a draft. The AFTER names a thesis and ordered points that each "
                   "carry evidence. Turning the list into a thesis-plus-ordered-points plan is the move.")),
        Slot("MODEL", "predict_the_fix", "What does this plan most need?",
             bank="water_cycle",
             body=("Diagnose before the reveal. A student's plan reads: 'Thesis: the water cycle is really "
                   "important. Then write three paragraphs with facts.' Which single change would most improve "
                   "it as a plan? "
                   "(A) make the thesis a focusing idea (what the cycle does) and give each body point a "
                   "specific topic plus its evidence  "
                   "(B) add a fourth body paragraph so the essay is longer and covers even more parts of the "
                   "water cycle from the reading  "
                   "(C) make the thesis longer by adding more words about why the water cycle is really "
                   "important to people and to nature  "
                   "(D) move the thesis to the end so the plan lists all the facts and paragraphs first and "
                   "then builds up to the main idea"),
             feedback=("Correct: A. The thesis is vague ('really important') and the body is unplanned ('three "
                       "paragraphs with facts'), so the plan cannot steer. The fix names a focusing thesis (what "
                       "the cycle does) and gives each body point a specific topic plus the evidence it will "
                       "use. A fourth paragraph (B), a longer thesis (C), or reordering (D) do not add the "
                       "missing specifics.")),
        Slot("SUPPORTED", "production_frq", "Draft the thesis and first two points",
             ref="", bank="water_cycle", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=("Start an SPO for an essay explaining the water cycle. Write the one-line THESIS, then POINT "
                   "1 and POINT 2, each naming its topic and the evidence (from the source) that paragraph "
                   "will use. Goal: a focusing thesis plus two ordered points that each carry named evidence. "
                   "Do not write a to-do list. Scored on Organization.")),
        Slot("MODEL", "diagnosis_frq", "Check a plan against the SPO parts",
             ref="", bank="water_cycle", scored=True,
             body=("First watch the check run on a provided plan, then run it on a fresh plan of your own. "
                   "Provided plan: 'Thesis: water moves around. Body: some facts about rain and rivers.' Run "
                   "the check step by step. Step 1, THESIS a focusing idea? Barely ('water moves around'), "
                   "sharpen it. Step 2, points ORDERED and specific? No, 'some facts' names no ordered points, "
                   "so list them. Step 3, EVIDENCE named per point? No, attach a source to each. Now you: write "
                   "a fresh SPO thesis plus two points for the water-cycle essay, then run the same three "
                   "checks. For each No, use the fix: sharpen the thesis; list ordered points; name evidence "
                   "per point. Finish by naming which part your plan still needs most.")),
        Slot("INDEPENDENT", "production_frq", "Write a full single-paragraph outline",
             ref="", bank="water_cycle", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=("On your own now. Write a complete single-paragraph outline for an essay explaining the "
                   "water cycle: a one-line THESIS, then THREE ordered body POINTS, each naming its topic and "
                   "the evidence (from the source) it will use. Before you submit, check the plan: is the "
                   "thesis a focusing idea, are the points ordered and specific, does each point name evidence? "
                   "Fix any that fail before you submit. Scored on Organization.")),
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: volcanoes",
             ref="ACC-W910-INFO-LESSON-VOLCANOES", bank="volcanoes",
             body=("Read this new source about volcanoes. Because your job is to PLAN an essay from it, read "
                   "the whole thing and note the main stages and the facts that go with each. The text stays "
                   "on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Write a single-paragraph outline on a NEW topic",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=("New topic. Write a complete single-paragraph outline for an essay explaining how volcanoes "
                   "form and erupt: a one-line THESIS, then THREE ordered body POINTS, each with its topic and "
                   "named evidence from the source. Same planning move as the water-cycle SPO, new topic. Do "
                   "not write a to-do list. Scored on Organization.")),
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
