"""
lesson_g9_l20_spo_plan_v3_1.py  -  G9 KC C.9.04, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD). V3.1 + MPO CORRECTION.

G9 course L19/L20 (Unit 4, intro): plan a full ESSAY. KC C.9.04. ESSAY-TIER: binds the FULL source.
Taught: WATER-CYCLE (full) -> transfer: VOLCANOES (full, partitioned). unit="multi_paragraph".

MPO CORRECTION (2026-07-15, Noel flag + TWR 2.0 primary-text verification, SPINE_TWR_essay_planning_VERIFIED.md):
the prior version taught students to plan a full essay with a SINGLE-PARAGRAPH OUTLINE (SPO). That is a TWR
category error: the SPO (TWR 2.0 Ch. 5) is the planner for ONE paragraph; TWR plans a multi-paragraph essay with
the MULTIPLE-PARAGRAPH OUTLINE (MPO, TWR 2.0 Ch. 9, Appendix Q). This lesson is rebuilt around the MPO. Verified
from the licensed TWR 2.0 PDF (Ch. 9 "Moving On to Compositions: The Transition Outline and the Multiple-Paragraph
Outline"): an essay = a series of paragraphs united by a thesis; the MPO holds a THESIS STATEMENT at top, an
INTRODUCTION row, ordered BODY paragraphs each as a Main Idea + Details block (details in note form), and a
CONCLUSION. The SPO is the PREREQUISITE building block (students already write details in note form and craft
topic/concluding sentences); the two NEW skills at essay level are generating a thesis for the whole essay and a
concluding statement that rephrases it. Own words only (copyright posture: no verbatim TWR); TWR labels
Thesis/Introduction/Main Idea/Details/Conclusion used as the student-facing structure; Appendix/Exhibit cites are
internal only. Grain, diagnosis-as-provided-weak-plan (Council-verified sound at paragraph grain), id, kc,
bound sources preserved. Passes 23 lesson_contract gates + render-QC. No fabricated figures, no em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist, outline_table

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">An essay is planned at <strong>two levels</strong>: '
'one <strong>thesis</strong> that governs the whole essay, then a <strong>multiple-paragraph outline</strong> '
'under it: an introduction, ordered body paragraphs that each pair a main idea with its details, and a '
'conclusion. A single-paragraph plan cannot hold an essay.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the essay outline</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit an essay outline, check it has all four:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0"><strong>Thesis</strong>: one line that governs the whole essay.</li>'
'<li style="margin:2px 0"><strong>Introduction</strong>: a line planning how you open and land the thesis.</li>'
'<li style="margin:2px 0"><strong>Body paragraphs</strong>: one row each, in order, pairing a main idea with its details.</li>'
'<li style="margin:2px 0"><strong>Conclusion</strong>: a line that restates the thesis in new words.</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">A single main idea with details is one paragraph, not an essay. The essay outline holds all of them.</div></div>')

# coping-model panel: a single-paragraph plan (the OLD mistake) REBUILT into a multiple-paragraph outline.
# Contains literal BEFORE + AFTER (content_depth). Shows the two-level structure the MPO adds.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> a single-paragraph plan, too flat to hold an essay</span>'
    '<p style="margin:8px 0 0;font-size:15px">Thesis: the water cycle recycles Earth\'s water. Point 1: '
    'evaporation lifts water (USGS). Point 2: precipitation returns it (USGS). Point 3: collection stores it (USGS).</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">This is a single-paragraph outline: a thesis and a '
    'flat list of points. It plans one paragraph. An essay needs an introduction, a conclusion, and each point '
    'grown into its own paragraph with details.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> a multiple-paragraph outline that holds the whole essay</span>'
    # the MPO shown as a real 2-D outline GRID (label column + content; body rows pair main idea with details),
    # so the two-level structure is visible, not a run-on line. <table> is a top-level block here (never inside a
    # <p>) and uses inline styles only -> Timeback-safe (verified 2026-07-16).
    '<table style="border-collapse:collapse;width:100%;margin:8px 0 0;font-size:14px">'
      '<tr><td style="border:1px solid #bbf7d0;padding:5px 8px;background:#dbeafe;color:#1e3a8a;font-weight:700;'
      'white-space:nowrap;vertical-align:top">THESIS</td>'
      '<td style="border:1px solid #bbf7d0;padding:5px 8px;vertical-align:top" colspan="2">The water cycle '
      'constantly recycles Earth\'s water through connected stages.</td></tr>'
      '<tr><td style="border:1px solid #bbf7d0;padding:5px 8px;background:#e0e7ff;color:#3730a3;font-weight:700;'
      'white-space:nowrap;vertical-align:top">INTRO</td>'
      '<td style="border:1px solid #bbf7d0;padding:5px 8px;vertical-align:top" colspan="2">Open on water always '
      'moving, land the thesis.</td></tr>'
      '<tr><td style="border:1px solid #bbf7d0;padding:5px 8px;background:#fef9c3;color:#854d0e;font-weight:700;'
      'white-space:nowrap;vertical-align:top">BODY 1</td>'
      '<td style="border:1px solid #bbf7d0;padding:5px 8px;vertical-align:top">Main idea: evaporation lifts water '
      'into the air.</td><td style="border:1px solid #bbf7d0;padding:5px 8px;vertical-align:top">Details: sun '
      'heats surface water, vapor rises (USGS).</td></tr>'
      '<tr><td style="border:1px solid #bbf7d0;padding:5px 8px;background:#fef9c3;color:#854d0e;font-weight:700;'
      'white-space:nowrap;vertical-align:top">BODY 2</td>'
      '<td style="border:1px solid #bbf7d0;padding:5px 8px;vertical-align:top">Main idea: it cools and falls '
      'back.</td><td style="border:1px solid #bbf7d0;padding:5px 8px;vertical-align:top">Details: vapor condenses '
      'into clouds, returns as precipitation (USGS).</td></tr>'
      '<tr><td style="border:1px solid #bbf7d0;padding:5px 8px;background:#fef9c3;color:#854d0e;font-weight:700;'
      'white-space:nowrap;vertical-align:top">BODY 3</td>'
      '<td style="border:1px solid #bbf7d0;padding:5px 8px;vertical-align:top">Main idea: it collects and the loop '
      'repeats.</td><td style="border:1px solid #bbf7d0;padding:5px 8px;vertical-align:top">Details: gathers in '
      'rivers, lakes, oceans (USGS).</td></tr>'
      '<tr><td style="border:1px solid #bbf7d0;padding:5px 8px;background:#dcfce7;color:#166534;font-weight:700;'
      'white-space:nowrap;vertical-align:top">CONC</td>'
      '<td style="border:1px solid #bbf7d0;padding:5px 8px;vertical-align:top" colspan="2">Restate: the same water '
      'cycles endlessly.</td></tr>'
    '</table>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Now the thesis governs the whole plan, an intro and '
    'conclusion frame it, and each body row pairs a main idea with its own details, so every paragraph knows '
    'what it argues and proves.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C904-0019", grade="9-10", lesson_type=7,
    unit="G9 U4 - Build essay (multiple-paragraph-outline plan)",
    title="Plan Before You Draft: The Multiple-Paragraph Outline",
    target=("Plan a full essay with a multiple-paragraph outline: a thesis that governs the essay, an "
            "introduction, ordered body paragraphs that each pair a main idea with its details, and a "
            "conclusion. Builds on the single-paragraph outline. Written as a plan for a multi-paragraph "
            "essay. Trait: Organization."),
    acc_tags=["ACC.W.PROD.1", "CCSS.W.9-10.4"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.9.04", "sot": "icm course-G9.md L19",
                "taught_stimulus": "ACC-W910-INFO-LESSON-WATER-CYCLE",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-VOLCANOES",
                "one_idea": "Plan the essay with a multiple-paragraph outline: thesis governs; intro, ordered body paragraphs (main idea + details), conclusion.",
                "one_reminder": "Check the essay outline: governing thesis? intro? each body a main idea + details, in order? conclusion that restates?",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": "L01/L12 v3.1 pattern; ESSAY-TIER binds full sources.",
                "twr_source": ("TWR 2.0 Ch. 9 (Moving On to Compositions: the Transition Outline and the "
                               "Multiple-Paragraph Outline); MPO = Appendix Q / Exhibit 9.2. Verified from the "
                               "licensed PDF: essay = paragraphs united by a thesis; MPO holds THESIS -> "
                               "INTRODUCTION -> body paragraphs (Main Idea + Details, details in note form) -> "
                               "CONCLUSION. SPO (Ch. 5) is the single-paragraph prerequisite; new essay-level "
                               "skills = generate a whole-essay thesis + a concluding statement that rephrases it. "
                               "See SPINE_TWR_essay_planning_VERIFIED.md."),
                "council": ("T7/BUILD planning rung: introduces the MULTIPLE-PARAGRAPH OUTLINE (MPO) as the essay "
                            "planner, built on the SPO. two-level (thesis -> body main-idea+details) vs single-"
                            "paragraph-flat discrimination labeled Grade-C. MPO/thesis defined in TEACH. "
                            "BUILD=proposal; unit=multi_paragraph."),
                "version_note": ("2026-07-15 MPO CORRECTION: replaced the SPO-for-an-essay teaching (a TWR category "
                                 "error Noel flagged) with the TWR Multiple-Paragraph Outline, verified against the "
                                 "TWR 2.0 primary text. The SPO is now framed as the prerequisite building block; "
                                 "the MPO adds a governing thesis, an introduction, body paragraphs as main "
                                 "idea + details, and a conclusion. Kept grain=multi_paragraph, id, kc, bound "
                                 "sources, and the provided-weak-plan diagnosis (Council-verified sound). Prior "
                                 "V3.1 structural fixes (ONE_IDEA + <ul>, model-before-quiz, explicit choices, "
                                 "deterministic frq bodies) preserved."),
                "review_provenance": "built to the L01/L12 v3.1 pattern; MPO verified from TWR 2.0 PDF Ch.9"},
    fade_ledger_moves=["multiple-paragraph-outline", "thesis-governs-intro-body-mainidea-details-conclusion"],
    slots=[
        # ===== TEACH: the two-level idea + the parts of an MPO (defines 'thesis' and 'MPO', builds on SPO) =====
        Slot("TEACH", "teach_card", "The one idea: plan the essay with a multiple-paragraph outline",
             body=(ONE_IDEA +
                   "You already know the single-paragraph outline, which is a plan for ONE paragraph: a topic "
                   "sentence with its supporting details. An essay is bigger, so it needs a bigger plan, the "
                   "multiple-paragraph outline, or MPO. It has four parts:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Thesis</strong>: a thesis is a single sentence that states "
                   "the main idea the whole essay defends. It governs every paragraph, so write it first.</li>"
                   "<li style=\"margin:4px 0\"><strong>Introduction</strong>: a line planning how you open the "
                   "topic and land the thesis.</li>"
                   "<li style=\"margin:4px 0\"><strong>Body paragraphs</strong>: one row per paragraph, in order. "
                   "Each row pairs a <strong>main idea</strong> (what that paragraph argues) with its "
                   "<strong>details</strong> (the facts and source that prove it, in note form). This is where "
                   "your single-paragraph-outline skill lives: each body row is one paragraph's plan.</li>"
                   "<li style=\"margin:4px 0\"><strong>Conclusion</strong>: a line that restates the thesis in "
                   "new words.</li></ul>"
                   "Write those together and you have an MPO: a plan for the whole essay you can see at a glance. "
                   "The trap is planning an essay with a single-paragraph outline, a thesis and a flat list of "
                   "points, which plans only one paragraph and leaves the intro, the conclusion, and each "
                   "paragraph's details unplanned. Goal today: write an MPO with a governing thesis, an intro, "
                   "ordered body rows that pair a main idea with details, and a conclusion.")),
        Slot("TEACH", "stimulus_display", "Read the source: the water cycle",
             ref="ACC-W910-INFO-LESSON-WATER-CYCLE", bank="water_cycle",
             body=("Read this source about the water cycle. Because your job is to PLAN an essay from it, read "
                   "the whole thing and note the main stages and the facts that go with each. You will turn "
                   "those into body rows, each a main idea with its details. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + the reusable check tool =====
        Slot("MODEL", "annotated_before_after", "Watch a single-paragraph plan grow into a multiple-paragraph outline",
             bank="water_cycle",
             body=("Here is the skill in action. Read the BEFORE (a single-paragraph plan), then the AFTER, and "
                   "notice the thesis now governs an intro, ordered body rows with main idea plus details, and a "
                   "conclusion." + BEFORE_AFTER_HTML +
                   " The BEFORE plans one paragraph; the AFTER plans the whole essay. Growing the flat list into "
                   "a thesis that governs an intro, body rows (main idea + details), and a conclusion is the "
                   "move." + REMEMBER +
                   "When you build your own, write the thesis first, then the intro, then the ordered body rows "
                   "with details, then the conclusion, and run the check.")),
        Slot("MODEL", "discrimination", "Which one is an essay outline, not a single-paragraph plan?",
             ref="", labeled_grade_c=True, bank="water_cycle",
             body=("Now that you have seen one built, spot the target. Which one is a multiple-paragraph outline "
                   "that plans a whole essay? "
                   "(A) Write about the water cycle for the whole essay. Say why it matters and why it is such a "
                   "big deal. Add plenty of facts from the reading, explain each of the parts in turn, and finish "
                   "with a strong, memorable ending that ties the whole thing together for the reader.  "
                   "(B) Thesis: the water cycle recycles Earth's water. Point 1: evaporation lifts water (USGS). "
                   "Point 2: precipitation returns it (USGS). Point 3: collection stores it until the loop "
                   "repeats all over again (USGS), and so on until the essay is long enough.  "
                   "(C) Thesis governs; intro line; Body 1 main idea + details (USGS); Body 2 main idea + details "
                   "(USGS); Body 3 main idea + details (USGS); conclusion restates the thesis. "
                   "Correct: C. (A) is a to-do list, no thesis or structure. (B) is a single-paragraph outline, a "
                   "thesis and a flat list, so it plans one paragraph with no intro, conclusion, or per-paragraph "
                   "details. (C) is a multiple-paragraph outline: a governing thesis, an intro, ordered body rows "
                   "each pairing a main idea with details, and a conclusion, so it plans the whole essay."),
             choices=[
                 {"id": "A", "text": "Write about the water cycle for the whole essay. Say why it matters and why it is such a big deal for the planet. Add plenty of facts from the reading. Explain each of the different parts in turn. Then finish the essay off with a strong, memorable ending that ties everything together.",
                  "correct": False,
                  "why": "A to-do list, not a plan. No thesis, no ordered paragraphs, no specific details, so it steers nothing however long it runs."},
                 {"id": "B", "text": "Thesis: the water cycle recycles Earth's water. Point 1: evaporation (USGS). Point 2: precipitation (USGS). Point 3: collection (USGS).",
                  "correct": False,
                  "why": "This is a single-paragraph outline, a thesis plus a flat list of points. It plans one paragraph. An essay outline also needs an introduction, a conclusion, and each point grown into a body row with its own main idea and details."},
                 {"id": "C", "text": "Thesis governs the essay, then an intro line, three ordered body rows each pairing a main idea with its details (USGS), and a conclusion that restates the thesis.",
                  "correct": True,
                  "why": "Correct. A governing thesis, an introduction, ordered body rows that each pair a main idea with details, and a conclusion. That is a multiple-paragraph outline: it plans the whole essay."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this essay outline most need?",
             bank="water_cycle",
             body=("Diagnose before the reveal. A student's essay outline reads: 'Thesis: the water cycle is "
                   "important. Body 1: evaporation. Body 2: condensation. Body 3: collection.' Which single "
                   "change would most improve it as an essay plan? "
                   "(A) sharpen the thesis to what the cycle does, add an intro and conclusion line, and give "
                   "each body row its details, not just a one-word main idea  "
                   "(B) add a fourth and then a fifth body paragraph to the plan so that the finished essay ends "
                   "up longer and manages to cover several more stages from the reading  "
                   "(C) make the thesis a good deal longer by piling on more words about why the water cycle "
                   "matters so much to people, to farms, and to nature across the whole planet  "
                   "(D) move the thesis all the way to the very end so the outline lists every body paragraph "
                   "first and only then, at the bottom, finally arrives at the main idea"),
             feedback=("Correct: A. The thesis is vague ('important'), there is no intro or conclusion row, and "
                       "each body is a bare one-word main idea with no details, so the plan cannot steer a draft. "
                       "The fix sharpens the thesis, frames it with an intro and conclusion, and gives each body "
                       "row its details. More paragraphs (B), a longer thesis (C), or reordering (D) do not add "
                       "the missing structure or specifics.")),

        # ===== SUPPORTED: framed write (fill-in frame) on the taught source =====
        Slot("SUPPORTED", "production_frq", "Draft the thesis, intro, and first body row",
             ref="", bank="water_cycle", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Use the outline grid below so you can see the shape of the plan. Copy it into the box and "
                       "fill each blank to start a multiple-paragraph outline for an essay explaining the water cycle.",
                 setapart_block=outline_table(title="Copy this outline, then fill in each blank:", rows=[
                     ("THESIS", "______ (what the water cycle does across the whole essay)"),
                     ("INTRODUCTION", "______ (how you open and land the thesis)"),
                     ("BODY 1", ["main idea: ______ (first stage)", "details: ______ (______ source)"]),
                 ]),
                 closer="Write a governing thesis, an intro line, and one body row that pairs a main idea with "
                        "its details and source. Do not write a single-paragraph plan. Then check it: does the "
                        "thesis govern, is there an intro, does the body row pair a main idea with details?")),
        # DIAGNOSIS: watch the check run on a PROVIDED weak plan (checklist), then write + check your own.
        Slot("MODEL", "diagnosis_frq", "Check a plan against the essay-outline parts",
             ref="", bank="water_cycle", scored=True,
             body=frq_prompt(
                 intro="Run the essay-outline check on this weak plan, then write and check a plan of your own.",
                 setapart_block=setapart("Weak plan to check:",
                                         "Thesis: water moves around. Body: some facts about rain and rivers.", "red"),
                 checklist_block=checklist(title="Check the essay outline:", rows=[
                     ("Thesis: a governing idea?", "Barely, 'water moves around' is vague. Sharpen it to what the cycle does across the whole essay."),
                     ("Intro and conclusion planned?", "No. Neither is here. Add a line for how you open and how you restate the thesis."),
                     ("Body rows: main idea + details, in order?", "No. 'Some facts' is one flat blob, not ordered body rows that each pair a main idea with its details and source."),
                 ]),
                 closer="Now write a fresh multiple-paragraph outline (thesis, intro, two ordered body rows with "
                        "details, conclusion) for the water-cycle essay, then run the same checks on your plan.")),

        # ===== INDEPENDENT: full MPO on the taught topic + autonomy + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write a full multiple-paragraph outline",
             ref="", bank="water_cycle", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="On your own now, no frame. Plan the whole essay explaining the water cycle.",
                 closer="Write a complete multiple-paragraph outline: a THESIS that governs the essay, an "
                        "INTRODUCTION line, THREE ordered BODY rows that each pair a main idea with its details "
                        "and source, and a CONCLUSION that restates the thesis. Planning the whole essay before "
                        "you draft is the move every strong writer makes, and you are ready to do it cold. Check "
                        "the plan (governing thesis, intro, ordered body rows with details, conclusion) before "
                        "you submit.")),

        # ===== TRANSFER: same move, a NEW topic (volcanoes), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: volcanoes",
             ref="ACC-W910-INFO-LESSON-VOLCANOES", bank="volcanoes",
             body=("Read this new source about volcanoes. Because your job is to PLAN an essay from it, read "
                   "the whole thing and note the main stages and the facts that go with each. The text stays "
                   "on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Write a multiple-paragraph outline on a NEW topic",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="New topic. Plan an essay explaining how volcanoes form and erupt.",
                 closer="Write a complete multiple-paragraph outline: a THESIS, an INTRODUCTION line, THREE "
                        "ordered BODY rows that each pair a main idea with its details and source, and a "
                        "CONCLUSION. Same planning move as the water-cycle outline, new topic. Do not write a "
                        "single-paragraph plan. Run the check before you submit.")),
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
