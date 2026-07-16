"""
lesson_g11_l24_plan_fast.py  -  G11 KC C.11.05, ESSAY-ASSEMBLY (BUILD, ceiling essay). V3.1.

G11 course L24 (Unit 6, guided), rebuilt to the v3.1 build spec (hand-authored). Teaching point (KEPT):
under a tight window make a fast plan, a two or three line sketch of the position plus the ordered points,
that steers the draft, rather than skipping the plan or writing a full-page outline that eats the window.
A transferable exam STRATEGY; Timeback delivery is UNTIMED. This is a FULL-ESSAY (type 7) lesson and reaches
the essay ceiling.

Preserved EXACTLY from the prior L24: id="ACC-W1112-L-G11-C1106-0024", lesson_type=7,
mnemonic_status="proposal", kc="C.11.05", unit, the bound stimuli (AIWORKFORCE taught -> GRIDSPENDING
transfer), rubric_ref rc.ap, and every production_frq unit= value (SUPPORTED plan = multi_paragraph,
INDEPENDENT + TRANSFER = essay). The unit ladder climbs to the essay, the type-7 ceiling.

V3.1 changes vs the prior L24:
  1. FIXED the leaked internal label: the discrimination no longer says "a Grade-C design bet we label as a
     bet"; it is a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}].
  2. FIXED the wall-of-text teach card: the prose block is now a ONE_IDEA teal callout + a real <ul>/<ol>
     list of the parts and the order of work (format_fidelity).
  3. Deterministic FRQ + diagnosis prompts via frq_prompt/setapart/checklist (no "Step 1/2" prose, no
     "Scored on ..." chrome); coping-model before/after kept; the fast-plan check folded in at first use as a
     real <ol> REMEMBER box.
Own words, faithful to the bound federal-sourced passages, no fabricated figures, no em dashes.
Passes all 23 lesson_contract gates + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Under a tight window a <strong>fast plan</strong> is a '
'two or three line sketch that steers the whole draft. It is not a second essay, and it is not nothing: it is '
'just enough to keep the paragraphs on one line and leave time to write.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: is this plan fast enough?</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you draft from a plan, ask three questions:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Is there one line that names the position you will defend?</li>'
'<li style="margin:2px 0">Are there two or three ordered points, each in a few words?</li>'
'<li style="margin:2px 0">Is the whole plan a few lines, not written-out paragraphs?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you draft.</div></div>')

# coping-model before/after: a writer's FIRST TRY is a window-eating full-sentence outline; the writer runs the
# check, catches the over-plan, and rebuilds it into a three-line fast plan. Contains BOTH a literal BEFORE and
# AFTER (content_depth). Short sketch, not a whole essay - the point is the over-plan-to-fast-plan contrast.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> first try: a full-page outline that eats the window</span>'
    '<p style="margin:8px 0 0;font-size:15px"><i>The writer spends nearly half the window writing this out:</i> '
    '"Paragraph 1 topic sentence: The government should actively steer workers toward growing technology '
    'fields. Quote to use: the Bureau projects data scientist jobs will grow 33.5 percent from 2024 to 2034. '
    'Transition into paragraph 2: Building on this... " and keeps going, a complete sentence for every '
    'paragraph.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">Run the check. Position named? Yes, but buried in '
    'full sentences. A few lines? No, it is a written-out draft. This over-plans: it rewrites the essay as an '
    'outline and burns the time meant for drafting.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> final: a 3-line fast plan that steers the draft</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">FAST PLAN</span> Position: government should steer workers toward growing fields. '
      'P1: the growth gap (tech jobs like data science up 33.5 percent vs 3.1 percent overall). '
      'P2: markets are slow to retrain a mid-career worker. '
      'P3: concede the misjudged-plans worry, then answer it. Three lines, written in about two minutes.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Run the check again. Position named in one line? '
    'Yes. Two or three ordered points? Yes. A few lines, not paragraphs? Yes. Same thinking as the first try, '
    'but now the draft has a spine and the window is still open.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1106-0024", grade="9-10", lesson_type=7,
    unit="G11 U6 - Exam readiness (plan fast)",
    title="Make a Fast Plan: Position Plus Ordered Points",
    target=("Make a quick two or three line plan (the position plus ordered points) that steers the draft, "
            "rather than skipping the plan or writing a full-page outline that eats the window. A transferable "
            "exam strategy (Timeback delivery is untimed). Written at the essay. Trait: Organization and process."),
    acc_tags=["ACC.W.PROD.4", "CCSS.W.11-12.4", "CCSS.W.11-12.5"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.05", "sot": "icm course-G11.md L24",
                "taught_stimulus": "ACC-W910-ARG-LESSON-AIWORKFORCE",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-GRIDSPENDING",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": ("v3.1 spine; ESSAY-TIER binds full argument sources; teaches a transferable "
                             "fast-plan STRATEGY, Timeback delivery UNTIMED."),
                "one_idea": "Under a tight window a fast plan is a few-line sketch (position plus ordered points) that steers the draft.",
                "one_reminder": "Fast-plan check: one line names the position? two or three ordered points? a few lines, not paragraphs?",
                "version_note": ("V3.1 rebuild of L24. FIXED the leaked internal label (removed 'a Grade-C "
                                 "design bet we label as a bet' from the discrimination, moved to explicit "
                                 "choices=[]); broke the wall-of-text teach card into a ONE_IDEA callout + real "
                                 "<ul>/<ol> lists (format_fidelity); deterministic frq_prompt/setapart/checklist "
                                 "bodies (no 'Step 1/2' prose, no 'Scored on' chrome); coping-model before/after "
                                 "with the fast-plan check folded in at first use as an <ol> REMEMBER box. "
                                 "Preserved id, type 7, kc=C.11.05, mnemonic_status=proposal, bound stimuli, and "
                                 "every production_frq unit= value (SUPPORTED=multi_paragraph, "
                                 "INDEPENDENT/TRANSFER=essay); ladder climbs to essay."),
                "review_provenance": "built to the G9 L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["fast-plan", "position-plus-ordered-points"],
    slots=[
        # ===== TEACH: the one idea + what a fast plan is (list), then how to make it (list) =====
        Slot("TEACH", "teach_card", "The one idea: a fast plan is a few lines that steer",
             body=(ONE_IDEA +
                   "You already know how to build an argument essay. This lesson is about the planning STEP when "
                   "the clock is tight. A fast plan has just two things:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>The position</strong>: your thesis, which is a one-sentence "
                   "statement of the side you will defend, written on one line.</li>"
                   "<li style=\"margin:4px 0\"><strong>The ordered points</strong>: two or three reasons that "
                   "support the position, each named in a few words (not a full sentence), in the order you will "
                   "argue them.</li></ul>"
                   "That is enough to give the draft a spine and keep the paragraphs from drifting. Two errors "
                   "cost you here. Skipping the plan lets the essay wander. Over-planning, writing a full-page "
                   "outline in complete sentences, burns the minutes you need to draft and check.")),
        Slot("TEACH", "teach_card", "How to make one, and how fast",
             body=("Here is the order of work when the window is tight. Follow it and the plan takes about two "
                   "minutes:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Pick the side</strong>: decide the position and write it "
                   "on one line.</li>"
                   "<li style=\"margin:4px 0\"><strong>List the points</strong>: jot two or three reasons, each "
                   "in a few words, in the order you will argue them.</li>"
                   "<li style=\"margin:4px 0\"><strong>Tag the evidence</strong>: next to each point, note the "
                   "one fact you will use, in shorthand.</li>"
                   "<li style=\"margin:4px 0\"><strong>Stop</strong>: do not write full sentences yet. The plan "
                   "is done; the drafting time is what is left.</li></ol>"
                   "The fast plan sits between skipping and over-planning: quick to write, enough to steer. You "
                   "will practice building one here without a clock.")),
        Slot("TEACH", "stimulus_display", "Read the source: steering workers into growing fields",
             ref="ACC-W910-ARG-LESSON-AIWORKFORCE", bank="ai_regulation",
             body=("Read this source on whether the government should steer workers toward growing technology "
                   "fields. Picture a tight window: as you read, look for a position worth defending and the two "
                   "or three points you would jot in a fast plan. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + check tool, then the check items =====
        Slot("MODEL", "annotated_before_after", "Watch an over-plan become a fast plan",
             bank="ai_regulation",
             body=("Here is a writer who first over-plans, runs the check, catches it, and rebuilds a fast plan. "
                   "Read the BEFORE, then the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE writes a second essay as an outline and eats the window. The AFTER sketches the "
                   "position plus ordered points in a few lines. A fast plan is the move." + REMEMBER +
                   "When you build your own, jot the position and points, then run this check before you draft.")),
        Slot("MODEL", "discrimination", "Which one is a fast plan?",
             ref="", labeled_grade_c=True, bank="ai_regulation",
             body=("You have watched an over-plan become a fast plan. Now spot the target: which of these is a "
                   "FAST PLAN, the kind you can write in about two minutes and still have the window to draft? "
                   "(A) Three lines jotted in about two minutes: one line names the position to defend, then P1, "
                   "P2, and P3 name a reason each in a few words, with a shorthand fact beside each point.  "
                   "(B) A full page of complete sentences that writes out a topic sentence, a quotation, and a "
                   "closing transition for each and every planned paragraph in the essay before any drafting starts.  "
                   "(C) A blank page and a plan to skip planning, opening straight into paragraph one and adding "
                   "whatever new reason comes to mind next until the essay finally feels quite long enough to stop. "
                   "Correct: A. It names a position and an order in a few lines, enough to steer the draft while "
                   "the window stays open; B over-plans and rewrites the essay as an outline, and C skips "
                   "planning, so the draft wanders."),
             choices=[
                 {"id": "A", "text": "Three lines jotted in about two minutes: one line names the position to defend, then P1, P2, and P3 each name a reason, with a shorthand fact beside each point.",
                  "correct": True,
                  "why": "Correct. This names a position and an order in a few lines, enough to steer the draft while the window stays open to write."},
                 {"id": "B", "text": "A full page of complete sentences that writes out a topic sentence, a quotation, and a closing transition for every planned paragraph in the essay before any drafting begins.",
                  "correct": False,
                  "why": "This over-plans. It rewrites the essay as an outline in full sentences and burns the minutes meant for drafting and checking."},
                 {"id": "C", "text": "A blank page and a plan to skip planning, opening straight into paragraph one and adding whatever reason comes to mind next until the essay finally feels long enough to stop.",
                  "correct": False,
                  "why": "This skips planning. With no position and no order set first, the draft wanders and repeats instead of building one case."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this planning habit most need?",
             bank="ai_regulation",
             body=("Diagnose before the reveal. A student spends almost half a tight window writing a detailed, "
                   "full-sentence outline of the AI-workforce essay. Which single move would most improve the "
                   "result? "
                   "(A) shrink the plan to a few lines (the position plus ordered points) and start drafting sooner  "
                   "(B) keep the full-sentence outline as it is but add even more detail to every section before drafting  "
                   "(C) skip the planning step entirely the next time around and just start writing the essay right away  "
                   "(D) write the whole outline out as complete paragraphs so each section is fully drafted in advance"),
             feedback=("Correct: A. A half-window outline is over-planning; it steals drafting time. The fix "
                       "keeps a short plan (the position plus ordered points) and gets to drafting. More outline "
                       "detail (B) or full paragraphs (D) make it worse; skipping planning (C) overcorrects into "
                       "a wandering draft.")),

        # ===== SUPPORTED: write the fast plan (multi_paragraph) - the frame is the highest-value scaffold =====
        Slot("SUPPORTED", "production_frq", "Write a fast plan",
             ref="", bank="ai_regulation", rubric_ref="rc.ap", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="For the AI-workforce prompt, write a fast plan before you draft a word of the essay.",
                 setapart_block=setapart("Fill in this plan:",
                                         "Position: ______ (the side you will defend). Point 1: ______ + its fact. Point 2: ______ + its fact. Point 3: ______ + its fact."),
                 closer="Keep it to a few lines: one line for the position, then two or three ordered points, "
                        "each in a few words with the fact it will use in shorthand. Do not write full sentences "
                        "for each paragraph. This plan is what you will build the essay from.")),
        # DIAGNOSIS = self-revision: reread the fast plan you JUST wrote and run the three-question check on it,
        # fixing any line that fails (not a check on a provided weak plan, and not a fresh production). Same taught
        # source (load balance). Self-contained: the checklist is the scaffold and the grader scores the diagnosis.
        Slot("MODEL", "diagnosis_frq", "Check a fast plan before you draft",
             ref="", bank="ai_regulation", scored=True,
             body=frq_prompt(
                 intro="Reread the fast plan you just wrote. Run this checklist on YOUR plan and fix any line that fails.",
                 checklist_block=checklist(title="Check your own plan, row by row:", rows=[
                     ("Does one line name a position to defend?", "If it only names the topic, state a side someone could reject, such as whether the government should steer workers toward growing fields."),
                     ("Are there two or three ordered points?", "If they are missing, add two or three reasons, each in a few words, in the order you will argue them."),
                     ("Is it a few lines, not paragraphs?", "If it has grown into full sentences or written-out paragraphs, trim it back to a few lines: the position on one line and each point in a few words."),
                 ]),
                 closer="For every check your plan fails, fix that line now. Finish by naming the position your "
                        "plan will defend.")),

        # ===== INDEPENDENT: build the whole essay from the fast plan (essay ceiling) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Draft the essay from your fast plan",
             ref="", bank="ai_regulation", rubric_ref="rc.ap", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now. Make a two or three line fast plan for the AI-workforce prompt, then "
                       "build the whole essay from it.",
                 closer="Write a complete argument essay: an introduction that states the position, one body "
                        "paragraph per planned point (each with its evidence), and a conclusion. There is no "
                        "platform timer; the point is that a short plan steers the whole draft. Before you "
                        "submit, confirm the essay follows your planned points. Making a fast plan steer a full "
                        "draft is what every timed argument essay is built on, and you are ready to do it cold.")),
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
