"""
lesson_g9_l24_full_informational_essay_v3_1.py  -  G9 KC C.9.04, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD). V3.1.

Rebuild of lesson_g9_l24_full_informational_essay.py to the v3.1 build spec (icm/_config/v3_1-lesson-build-spec.md).
Teaching point (KEPT): plan AND write a complete single-source INFORMATIONAL essay - a single-paragraph-outline
plan with a controlling idea (no side), an intro that frames the focus, ordered body paragraphs that explain each
part with attributed evidence, and a conclusion that lands the upshot. FULL-ESSAY, EXPLAIN mode. KC C.9.04.
Reaches the essay ceiling. ESSAY-TIER binds the full source. Taught: MIGRATION (full) -> transfer: WATER-CYCLE
(full, partitioned). rc.staar. BUILD=proposal. Untimed.

V3.1 changes vs the current L24 (design pattern, teaching point unchanged):
  1. TEACH is ONE hammered card: a ONE_IDEA callout + the build steps as a real ordered LIST (was two prose
     teach cards that tripped format_fidelity as walls of text). "controlling idea" + "single-paragraph outline"
     defined in-place with a definitional cue.
  2. Model BEFORE the quiz (KH): a coping-model think-aloud (draft -> test -> catch the drift-into-opinion ->
     revise), still with literal BEFORE + AFTER, then the reusable check tool (REMEMBER), then the discrimination.
  3. Discrimination uses explicit choices=[{id,text,correct,why}]; the confound is broken (both A and B are
     "planned with a controlling idea", so the invariant is holding the EXPLAIN mode with no side, not the token
     "planned"); the correct option is not the lone longest.
  4. FRQ + diagnosis bodies built with frq_prompt/setapart/checklist (no "Step N" prose, no "Scored on ..."
     chrome, no double-numbering).
  5. Grade-C is labeled in CODE (labeled_grade_c=True) but the "Grade-C design bet" language is out of the
     student-facing text (leaked_internal_label fix).
Own words, no fabricated figures, no em dashes. Passes all 23 lesson_contract gates + render-QC.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">An informational essay is a plan built out. It '
'<strong>EXPLAINS</strong> a topic and takes <strong>NO side</strong>.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: hold the explain mode</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit the essay, run this quick check:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does the controlling idea name a focus and take NO side?</li>'
'<li style="margin:2px 0">Does each body paragraph explain one part with attributed evidence?</li>'
'<li style="margin:2px 0">Do the parts build in order and link at the seams?</li>'
'<li style="margin:2px 0">Did I avoid slipping in opinions anywhere?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, you have drifted out of the explain mode. Fix it.</div></div>')

# coping-model think-aloud panel: a WRITTEN drafting process (attempt -> test -> revise), then the endpoints.
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer building the opening, testing each move:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Migration is an amazing thing that birds do, and '
    'everyone should care about it." Check it: does this take a side? Yes, it says migration is amazing and that '
    'people should care. The task is to explain, not argue. Start over with a focus.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "This essay is about bird migration." Better, no '
    'opinion now, but it names no focus and no parts. A controlling idea has to say what the explanation will '
    'cover.</p>'
    '<p style="margin:0"><strong>Final:</strong> "Bird migration is best understood as one connected journey, '
    'and this essay explains why birds migrate, how far they travel, and how scientists track them." A focus, no '
    'side, and it names the parts to explain.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "Migration is an amazing thing that birds do, and everyone '
    'should care." (drifts into opinion, names no focus)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "Bird migration is best understood as one connected journey; '
    'this essay explains why birds migrate, how far they travel, and how scientists track them." (a focus, no '
    'side, names the parts)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C904-0024", grade="9-10", lesson_type=7,
    unit="G9 U4 - Build essay (full informational essay)",
    title="Write a Full Informational Essay From Your Plan",
    target=("Plan and write a complete single-source informational essay: a single-paragraph-outline plan with a controlling-idea "
            "thesis, an intro that frames the focus, ordered body paragraphs that explain each part with "
            "attributed evidence, and a conclusion that lands the upshot, all with no side taken. Written at "
            "the essay. Trait: Development/Organization/Purpose."),
    acc_tags=["ACC.W.PROD.1", "ACC.W.INFO.2", "CCSS.W.9-10.2", "CCSS.W.9-10.4"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.9.04", "sot": "icm course-G9.md L24",
                "taught_stimulus": "ACC-W910-INFO-LESSON-MIGRATION",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-WATER-CYCLE",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": "locked L01 v3.1 template; ESSAY-TIER binds full sources; UNTIMED (no Timeback timer).",
                "one_idea": "An informational essay is a plan built out that explains and takes no side.",
                "one_reminder": "Hold the explain mode: focus with no side? evidence per part? parts build+link? no opinions?",
                "version_note": ("V3.1 rebuild of L24 to the v3.1 build spec: ONE hammered TEACH card (ONE_IDEA + "
                                 "build steps as a real ordered list, killing the two wall-of-text teach cards), "
                                 "coping-model think-aloud with BEFORE+AFTER + reusable check tool, discrimination "
                                 "moved after the model (KH) with explicit choices and the 'planned' confound "
                                 "broken, FRQ+diagnosis bodies via frq_prompt/setapart/checklist (no Step-N prose, "
                                 "no 'Scored on' chrome), Grade-C label out of the student text. Teaching point, "
                                 "id, lesson_type=7, mnemonic_status=proposal, and every production unit "
                                 "(multi_paragraph -> essay -> essay) PRESERVED."),
                "council": ("T7/BUILD full-informational-essay build (explain-mode partner to L23): plan a "
                            "controlling idea + ordered parts, build the essay, hold the explain mode "
                            "(no side). explains-vs-drifts-into-arguing discrimination labeled Grade-C. "
                            "BUILD=proposal; unit=essay. Untimed."),
                "review_provenance": "built to the L01 v3.1 pattern (23 gates + render-QC clean)"},
    fade_ledger_moves=["plan-then-draft-informational-essay", "hold-the-explain-mode"],
    slots=[
        # ===== TEACH: ONE hammered card - the one idea + the build steps as a real ordered list =====
        Slot("TEACH", "teach_card", "The one idea: an explanation is a plan built out, with no side",
             body=(ONE_IDEA +
                   "A strong informational essay is built the same way as an argument essay, from a plan, with "
                   "one difference: it informs and never takes a side. Build it in order:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:5px 0\"><strong>PLAN</strong>: write a single-paragraph outline. A "
                   "single-paragraph outline is a compact plan in one block: a controlling idea on top, then one "
                   "line per body paragraph naming its point and its evidence. A controlling idea means one "
                   "sentence that names the focus your explanation will take, with no side.</li>"
                   "<li style=\"margin:5px 0\"><strong>INTRO</strong>: frame the focus and state the controlling "
                   "idea.</li>"
                   "<li style=\"margin:5px 0\"><strong>BODY</strong>: one paragraph per part, explaining it with "
                   "attributed evidence, ordered so the parts build, linked at the seams.</li>"
                   "<li style=\"margin:5px 0\"><strong>CONCLUSION</strong>: land the upshot, what the reader "
                   "should take away.</li>"
                   "<li style=\"margin:5px 0\"><strong>CHECK</strong>: does every paragraph explain (not argue), "
                   "is each part backed by evidence, do the parts build and link, did I avoid taking a "
                   "side?</li></ol>"
                   "The trap unique to explain essays is drifting into arguing, slipping in opinions when the "
                   "task asked you to inform. Goal today: plan an informational essay and build it, holding the "
                   "explain mode throughout.")),
        Slot("TEACH", "stimulus_display", "Read the source: bird migration",
             ref="ACC-W910-INFO-LESSON-MIGRATION", bank="animal_migration",
             body=("Read this source about bird migration. Because your job is to write a full informational "
                   "essay from it, read the whole thing and gather a focusing controlling idea plus the parts "
                   "you will explain (why birds migrate, how far, how tracked) with facts and their sources. "
                   "The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model think-aloud + reusable check tool, THEN the discrimination.
        Slot("MODEL", "annotated_before_after", "Watch a drifting opening become a planned one",
             bank="animal_migration",
             body=("Here is the skill in action. Follow the writer build the opening, testing each move. " +
                   COPING_HTML +
                   " Notice the difference: the BEFORE takes a side and names no focus; the AFTER states a focus "
                   "and takes no side. Holding the explain mode with a plan is the move." + REMEMBER +
                   "When you build your own, plan the focus and parts first, then draft, and run the check "
                   "before you submit.")),
        Slot("MODEL", "discrimination", "Which essay holds the explain mode?",
             ref="", labeled_grade_c=True, bank="animal_migration",
             body=("Spot the target before you build. The task: EXPLAIN how and why birds migrate. Which "
                   "approach holds the explain mode? "
                   "(A) A planned essay: a focusing controlling idea, then ordered parts (why they migrate, how "
                   "far, how they are tracked), each part explained with an attributed fact, and no side taken.  "
                   "(B) A planned essay with a clear controlling idea and ordered parts, but one that argues "
                   "migration is amazing and insists that readers everywhere must act now to protect every "
                   "migrating bird species.  "
                   "(C) An essay that piles up true facts about how far the different birds fly, in no set order "
                   "at all, and never names a single controlling focus for the reader to follow. "
                   "Correct: A. It holds a focus, explains with attributed evidence, and takes no side."),
             choices=[
                 {"id": "A",
                  "text": "A planned essay: a focusing controlling idea, then ordered parts (why they migrate, how far, how they are tracked), each part explained with an attributed fact, and no side taken.",
                  "correct": True,
                  "why": "Correct. It holds the explain mode: a focus, parts explained with attributed evidence, and no side. A plan plus informing with no side is the move."},
                 {"id": "B",
                  "text": "A planned essay with a clear controlling idea and ordered parts, but one that argues migration is amazing and insists that readers everywhere must act now to protect every migrating bird species.",
                  "correct": False,
                  "why": "This one has a plan and a controlling idea, but it argues a side (amazing, must act). The task was to explain, so taking a side is the wrong mode, even with a plan behind it."},
                 {"id": "C",
                  "text": "An essay that piles up true facts about how far the different birds fly, in no set order at all, and never names a single controlling focus for the reader to follow.",
                  "correct": False,
                  "why": "These are true facts, but with no focus and no order the essay explains nothing clearly. A controlling idea and ordered parts are what hold an explanation together."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this informational essay most need?",
             bank="animal_migration",
             body=("Diagnose before the reveal. A student's explain essay on migration keeps adding lines like "
                   "'this is why migration is the most amazing thing in nature and we should all care.' Which "
                   "single change would most improve it for an EXPLAIN task? "
                   "(A) cut the opinions and hold the explain mode: a focusing controlling idea, and parts "
                   "explained with attributed evidence, no side  "
                   "(B) keep piling on more and more amazing facts about how far each of the different birds can "
                   "fly, so the essay carries as much information as it possibly can  "
                   "(C) make the opinions stronger and far more convincing, so the reader really feels how "
                   "amazing migration is and understands exactly why they should care about it  "
                   "(D) move the opinion up into the introduction and then repeat it again in the conclusion, so "
                   "the writer's own view has a clear and steady place in the essay"),
             feedback=("Correct: A. The task is to explain, but the essay keeps arguing a side (most amazing, "
                       "should care), which is the wrong mode. The fix is to cut the opinions and hold the "
                       "explain mode: a focusing controlling idea, parts explained with attributed evidence, no "
                       "side. More facts (B), stronger opinions (C), or relocating the opinion (D) do not fix "
                       "the mode.")),

        # ===== SUPPORTED: framed PLAN write (the single-paragraph outline) on the taught source =====
        Slot("SUPPORTED", "production_frq", "Plan the explanation: controlling idea and ordered parts",
             ref="", bank="animal_migration", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Plan your informational essay on bird migration before you write it. Use the outline "
                       "frame below so you build a real plan, not a first draft.",
                 setapart_block=setapart("Copy this frame, then fill in each line:",
                                         "CONTROLLING IDEA: ______ (a focus on migration, no side). PART 1: "
                                         "______ (topic + evidence from the source). PART 2: ______. PART 3: ______."),
                 closer="Write a one-line controlling idea that takes no side, then three ordered parts, each "
                        "naming its topic and the evidence from the source it will use. This plan is what you "
                        "will build the essay from. Do not argue a side.")),
        # ===== MODEL (diagnosis): self-revision - reread your OWN just-written draft and run the check on it =====
        Slot("MODEL", "diagnosis_frq", "Check your plan holds the explain mode",
             ref="", bank="animal_migration", scored=True,
             body=frq_prompt(
                 intro="Reread the essay you just wrote. Run this checklist on YOUR draft and fix any line that fails.",
                 checklist_block=checklist(title="Check your own draft, row by row:", rows=[
                     ("Does the controlling idea take NO side?",
                      "No. 'Incredible and worth protecting' argues a side. Reword it as a focus, like how and why birds migrate."),
                     ("Are the parts distinct and specific?",
                      "No. 'Amazing / long / important' are vague. Name real parts: why birds migrate, how far, how they are tracked."),
                     ("Does each part have evidence from the source?",
                      "No. Attach a fact and its source to each part."),
                 ]),
                 closer="For every row that fails on your draft, fix it in the essay before you move on. Finish by "
                        "confirming your controlling idea takes no side.")),

        # ===== INDEPENDENT: build the whole essay cold + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Write the full informational essay",
             ref="", bank="animal_migration", rubric_ref="rc.staar", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now, build the whole essay from your plan. Write a complete informational "
                       "essay explaining how and why birds migrate.",
                 checklist_block=checklist(title="Build it with these parts:", rows=[
                     "An INTRODUCTION that frames the controlling idea (no side).",
                     "THREE body paragraphs, each explaining one part with attributed evidence, ordered to build and linked.",
                     "A CONCLUSION that lands the upshot, what the reader now understands.",
                 ]),
                 closer="Before you submit, check: does every paragraph explain rather than argue, is each part "
                        "supported with evidence, do the parts build and link, did I avoid taking a side? "
                        "Assembling the plan into a full essay is the real move, and you are ready to do it "
                        "cold. Take the time you need.")),
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
