"""
lesson_g9_l24_full_informational_essay.py  -  G9 KC C.9.04, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD, ceiling essay).

G9 course L24 (Unit 4, build). Plan and write a full single-source INFORMATIONAL essay: SPO plan (controlling-
idea thesis) -> intro that frames the focus -> ordered body paragraphs that explain each part with attributed
evidence -> conclusion that lands the upshot (no side taken). The explain-mode partner to L23. Reaches the
essay ceiling. Locked L01 template. ESSAY-TIER binds the FULL source. Taught: MIGRATION (full) -> transfer:
WATER-CYCLE (full, partitioned). rc.staar. BUILD=proposal. UNTIMED. No coping-model persona; no source markup;
no prior-work ref; no em dashes. Runs QC on execution.
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
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> a vague opening that drifts into opinion</span>'
    '<p style="margin:8px 0 0;font-size:15px">Migration is an amazing thing that birds do, and everyone '
    'should care about it. Birds fly to a lot of different places every year. The Arctic tern flies 12,000 '
    'miles. There is so much to say about how incredible birds are.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The task was to explain, but this opens with an '
    'opinion (amazing, everyone should care), drops a fact with no source and no focus, and follows no '
    'order.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> a focus stated, then explained, no side</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">CONTROLLING IDEA</span> Bird migration is best understood as one connected journey '
      'that links faraway places, and this essay explains why birds migrate, how far they travel, and how '
      'scientists follow them. '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">EVIDENCE</span> Birds head toward warmer regions mainly to find the food that winter '
      'hides, and some cover astonishing distances: the National Park Service reports that the Arctic tern '
      'flies about 12,000 miles each way, a round trip of roughly 24,000 miles a year.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">The controlling idea names a focus and takes no '
    'side, and the evidence beat explains one part with a fact tied to its source. A focus plus attributed '
    'explanation is the move.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C904-0024", grade="9-10", lesson_type=7,
    unit="G9 U4 - Build essay (full informational essay)",
    title="Write a Full Informational Essay From Your Plan",
    target=("Plan and write a complete single-source informational essay: an SPO plan with a controlling-idea "
            "thesis, an intro that frames the focus, ordered body paragraphs that explain each part with "
            "attributed evidence, and a conclusion that lands the upshot, all with no side taken. Written at "
            "the essay. Trait: Development/Organization/Purpose."),
    acc_tags=["ACC.W.PROD.1", "ACC.W.INFO.2", "CCSS.W.9-10.2", "CCSS.W.9-10.4"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12",
                "mnemonic_status": "proposal", "kc": "C.9.04", "sot": "icm course-G9.md L24",
                "taught_stimulus": "ACC-W910-INFO-LESSON-MIGRATION",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-WATER-CYCLE",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": "locked L01 template; ESSAY-TIER binds full sources; UNTIMED (no Timeback timer).",
                "council": ("T7/BUILD full-informational-essay build (explain-mode partner to L23): plan a "
                            "controlling-idea thesis + ordered parts, build the essay, hold the explain mode "
                            "(no side). explains-vs-drifts-into-arguing discrimination labeled Grade-C. "
                            "BUILD=proposal; unit=essay. Untimed.")},
    fade_ledger_moves=["plan-then-draft-informational-essay", "hold-the-explain-mode"],
    slots=[
        Slot("TEACH", "teach_card", "An explanation is a plan built out, with no side",
             body=("A strong informational essay is built the same way as an argument essay, from a plan, with "
                   "one key difference: it explains and takes no side. First you plan: a controlling-idea "
                   "thesis (a focusing angle on the topic, no side) plus ordered parts to explain, each with "
                   "evidence. A controlling idea means one sentence that names the focus your explanation will "
                   "take. Then you draft: an intro that frames the focus, one body paragraph per part (explain "
                   "it, with attributed evidence), the parts ordered so they build and linked at the seams, and "
                   "a conclusion that lands the upshot (what the reader should take away). The trap unique to "
                   "explain essays is drifting into arguing, slipping in opinions when the task asked you to "
                   "inform. Goal today: plan an informational essay and build it, holding the explain mode "
                   "throughout.")),
        Slot("TEACH", "teach_card", "How to build it, part by part",
             body=("The order of work matches the argument essay, with the explain mode held throughout. One, "
                   "PLAN with a single-paragraph outline. A single-paragraph outline is a compact plan written "
                   "in one block: the thesis on top, then one line per body paragraph naming its point and "
                   "evidence. Here that is a controlling-idea thesis plus three ordered parts, each with evidence. Two, INTRO: "
                   "frame the focus and state the controlling idea, no side. Three, BODY: one paragraph per "
                   "part, explaining it with attributed evidence, ordered to build and linked. Four, "
                   "CONCLUSION: land the upshot, what the reader now understands. Five, CHECK: does every "
                   "paragraph explain (not argue), is each part supported with evidence, do the parts build "
                   "and link, and did I avoid taking a side anywhere? You are assembling the same moves as the "
                   "argument essay, kept in explain mode.")),
        Slot("TEACH", "stimulus_display", "Read the source: animal migration",
             ref="ACC-W910-INFO-LESSON-MIGRATION", bank="animal_migration",
             body=("Read this source about animal migration. Because your job is to write a full informational "
                   "essay from it, read the whole thing and gather a focusing controlling idea plus the parts "
                   "you will explain (why birds migrate, how far, how tracked) with facts and their sources. "
                   "The text stays on screen while you work.")),
        Slot("TEACH", "discrimination", "Which essay holds the explain mode?",
             ref="", labeled_grade_c=True, bank="animal_migration",
             body=("Sort before you build (spotting the target first, a Grade-C design bet we label as a bet, "
                   "not a proven ingredient). The task: EXPLAIN how and why animals migrate. Which approach "
                   "holds the explain mode? "
                   "(A) A planned essay: a focusing controlling idea, then ordered parts (why, how far, how "
                   "tracked), each explained with attributed evidence, no side taken.  "
                   "(B) An essay that says migration is amazing and that people must protect migrating birds, "
                   "jumping between scattered facts with no planned order and taking a side. "
                   "Correct: A. The task is to explain, so (A) holds a focusing idea and informs with no side. "
                   "(B) argues a side (amazing, must protect), which is the wrong mode, and it has no planned "
                   "order. Holding the explain mode with a plan is the move.")),
        Slot("MODEL", "annotated_before_after", "Watch a drifting explanation become a planned one",
             bank="animal_migration",
             body=("Here is an explain essay that drifts into arguing being rebuilt as a planned explanation "
                   "that holds its mode. Read the BEFORE, then the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE slips into opinions and has no order. The AFTER plans a focus and ordered "
                   "parts, and explains with no side. Planning plus holding the explain mode is the move.")),
        Slot("MODEL", "predict_the_fix", "What does this informational essay most need?",
             bank="animal_migration",
             body=("Diagnose before the reveal. A student's explain essay on migration keeps adding lines like "
                   "'this is why migration is the most amazing thing in nature and we should all care.' Which "
                   "single change would most improve it for an EXPLAIN task? "
                   "(A) cut the opinions and keep the essay in explain mode, a focusing idea and parts "
                   "explained with evidence, no side  "
                   "(B) keep piling on more amazing facts about how far the different birds fly, so the essay holds as much information as it can  "
                   "(C) make the opinions stronger and more convincing, so readers feel how amazing migration is and why they should care  "
                   "(D) move the opinion up into the introduction and repeat it in the conclusion, so the writer's view has a clear spot"),
             feedback=("Correct: A. The task is to explain, but the essay keeps arguing a side (most amazing, "
                       "should care), which is the wrong mode. The fix is to cut the opinions and hold the "
                       "explain mode: a focusing controlling idea, parts explained with attributed evidence, no "
                       "side. More facts (B), stronger opinions (C), or relocating the opinion (D) do not fix "
                       "the mode.")),
        Slot("SUPPORTED", "production_frq", "Plan the explanation: controlling idea and ordered parts",
             ref="", bank="animal_migration", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=("Plan your informational essay on animal migration. Write a single-paragraph outline: a "
                   "one-line CONTROLLING IDEA (a focus, no side), then THREE ordered PARTS to explain, each "
                   "naming its topic and the evidence (from the source) it will use. This plan is what you will "
                   "build the essay from. Do not argue a side. Scored on Organization.")),
        Slot("MODEL", "diagnosis_frq", "Check your plan holds the explain mode",
             ref="", bank="animal_migration", scored=True,
             body=("First watch the check run on a provided plan, then run it on your own. Provided plan: "
                   "'Thesis: migration is incredible and worth protecting. Parts: it is amazing, it is long, "
                   "it is important.' Run the check step by step. Step 1, is the thesis a focusing idea with NO "
                   "side? No, 'incredible and worth protecting' argues, so make it a focus (how and why birds "
                   "migrate). Step 2, are the parts distinct and specific? No, 'amazing / long / important' are "
                   "vague, so name real parts (why, how far, how tracked). Step 3, evidence per part? No, "
                   "attach sources. Now you: write a fresh controlling idea plus three parts for the migration "
                   "essay, then run the same checks and fix any that fail. Finish by confirming your thesis "
                   "takes no side.")),
        Slot("INDEPENDENT", "production_frq", "Write the full informational essay",
             ref="", bank="animal_migration", rubric_ref="rc.staar", scored=True, unit="essay",
             body=("On your own now, write the whole essay from your plan. Write a complete informational essay "
                   "explaining how and why animals migrate: an INTRODUCTION that frames the controlling idea, "
                   "THREE body paragraphs that each explain one part with attributed evidence (ordered to build "
                   "and linked), and a CONCLUSION that lands the upshot, all with no side taken. Before you "
                   "submit, check: does every paragraph explain rather than argue, is each part supported with "
                   "evidence, do the parts build and link, did I avoid taking a side? Fix any that fail before "
                   "you submit. Take the time you need. Scored on Development/Organization/Purpose.")),
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: the water cycle",
             ref="ACC-W910-INFO-LESSON-WATER-CYCLE", bank="water_cycle",
             body=("Read this new source about the water cycle. Because your job is to write a full "
                   "informational essay from it, read the whole thing and gather a focusing controlling idea "
                   "plus the parts you will explain, with facts and their sources. The text stays on screen "
                   "while you work.")),
        Slot("TRANSFER", "production_frq", "Write a full informational essay on a NEW topic",
             ref="", bank="water_cycle", rubric_ref="rc.staar", scored=True, unit="essay",
             body=("New topic. Plan and write a complete informational essay explaining how the water cycle "
                   "works: an intro that frames the controlling idea, three body paragraphs that explain the "
                   "stages with attributed evidence (ordered and linked), and a conclusion that lands the "
                   "upshot, no side taken. Same plan-then-build-in-explain-mode move as the migration essay, "
                   "new topic. Take the time you need. Scored on Development/Organization/Purpose.")),
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
