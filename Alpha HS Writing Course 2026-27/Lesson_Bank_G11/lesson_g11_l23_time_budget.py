"""
lesson_g11_l23_time_budget.py  -  G11 KC C.11.05, ESSAY-ASSEMBLY (BUILD, ceiling essay). V3.1.

G11 course L23 (Unit 6, exam-readiness intro), rebuilt to the v3.1 build spec (hand-authored). Teaching point
(KEPT): plan a TIME BUDGET that allots minutes to reading, planning, drafting, and checking so a full essay
fits an exam window, rather than drafting until time runs out. Taught as a transferable AP-exam STRATEGY the
student applies to their own writing; the Timeback delivery itself is UNTIMED (no platform timer), per the
standing course decision. KC C.11.05. FULL-ESSAY lesson (type 7): reaches the essay ceiling.

Preserved EXACTLY from the current L23: id="ACC-W1112-L-G11-C1106-0023", lesson_type=7,
mnemonic_status="proposal", kc="C.11.05", unit, the bound stimuli (GRIDSPENDING taught -> AIWORKFORCE transfer),
and every production_frq unit= value (SUPPORTED plan = multi_paragraph, INDEPENDENT + TRANSFER = essay). The
unit ladder climbs to the essay, the type-7 ceiling.

V3.1 changes vs the prior version:
  1. Removed the leaked internal label ("a Grade-C design bet we label as a bet") from the discrimination and
     moved the sort to explicit choices=[{id,text,correct,why}] (leaked_internal_label).
  2. Broke the wall-of-text teach card into a ONE_IDEA teal callout + real <ul>/<ol> lists of the stages and
     the order of work (format_fidelity + the v3.1 "parallel items as a list" rule).
  3. Deterministic FRQ + diagnosis prompts via frq_prompt/setapart/checklist (no "Step 1/2" prose, no
     "Scored on ..." chrome); coping-model before/after kept; the budget check folded in at first use as a real
     <ol> REMEMBER box.
Own words, no fabricated figures (all facts trace to the bound EIA / BLS / NSF / GAO stimuli), no em dashes.
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
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">On a timed exam, the writers who finish well do not '
'write faster; they <strong>budget the minutes</strong>. A time budget gives each stage, reading, planning, '
'drafting, and checking, its own protected minutes decided before you write a word.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: test the budget</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you draft, look at the four numbers and ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does reading get real minutes, enough to understand the prompt and gather evidence?</li>'
'<li style="margin:2px 0">Are planning and checking protected, not crowded out by drafting?</li>'
'<li style="margin:2px 0">Does drafting fit the minutes that remain after read, plan, and check are set?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, move minutes before you start.</div></div>')

# coping-model before/after: a draft-until-time-runs-out approach rebuilt into a budgeted window. Contains BOTH
# a literal BEFORE and AFTER (content_depth). Short structural sketch, not a full essay - the point is the
# no-budget vs budgeted-window contrast. Figures are the strategy's own minute split, not source facts.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> no budget: draft until time runs out</span>'
    '<p style="margin:8px 0 0;font-size:15px">For a 40-minute essay the writer starts drafting at once, writes a '
    'huge opening paragraph, and is still on the second body point when time is called. No conclusion, no '
    'reread.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">With no plan for the minutes, reading was rushed and '
    'planning and checking got zero protected time, so the essay is lopsided and unfinished.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> minutes allotted, then defended</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">40-MIN BUDGET</span> read 7, plan 6, draft 23, check 4. The writer reads and notes the '
      'source in the first 7, sets a thesis and ordered points in the next 6, drafts the whole essay in 23, and '
      'stops at minute 36 to reread and fix, finishing complete and reviewed.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same window, but each stage was given minutes up '
    'front and then held to them, so planning and checking survived instead of being crowded out.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1106-0023", grade="9-10", lesson_type=7,
    unit="G11 U6 - Exam readiness (budget the minutes)",
    title="Budget Your Minutes Across Read, Plan, Draft, Check",
    target=("Plan a time budget that allots minutes to reading, planning, drafting, and checking so a full "
            "essay fits an exam window, rather than drafting until time runs out. A transferable exam strategy "
            "(Timeback delivery is untimed). Written at the essay. Trait: Purpose and process."),
    acc_tags=["ACC.W.PROD.4", "CCSS.W.11-12.4"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.05", "sot": "icm course-G11.md L23",
                "taught_stimulus": "ACC-W910-ARG-LESSON-GRIDSPENDING",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-AIWORKFORCE",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": ("v3.1 spine; ESSAY-TIER binds full argument sources; teaches a transferable exam "
                             "time-budget STRATEGY, Timeback delivery UNTIMED (no platform timer)."),
                "one_idea": "On a timed exam you budget the minutes: each stage gets its own protected minutes.",
                "one_reminder": "Budget check: reading gets real minutes? planning and checking protected? drafting fits the rest?",
                "version_note": ("V3.1 rebuild of L23. Removed the leaked internal label from the discrimination "
                                 "and moved the sort to explicit choices=[]; broke the wall-of-text teach card "
                                 "into a ONE_IDEA callout + real <ul>/<ol> lists (format_fidelity). Deterministic "
                                 "frq_prompt/setapart/checklist bodies (no 'Step 1/2' prose, no 'Scored on' "
                                 "chrome); budget check folded in at first use. Preserved id, type 7, "
                                 "mnemonic_status=proposal, kc=C.11.05, unit, bound stimuli, and every "
                                 "production_frq unit= value (SUPPORTED=multi_paragraph, INDEPENDENT/TRANSFER="
                                 "essay); ladder climbs to essay."),
                "council": ("T7/BUILD G11 exam-readiness intro: time-budget as a transferable exam strategy "
                            "(allot read/plan/draft/check minutes), delivery untimed. budgeted-vs-draft-until-out "
                            "discrimination. BUILD=proposal; unit=essay.")},
    fade_ledger_moves=["time-budget", "protect-plan-and-check-minutes"],
    slots=[
        # ===== TEACH: the one idea + the four stages (as a list), then the order of work (as a list) =====
        Slot("TEACH", "teach_card", "The one idea: budget the minutes, do not just write faster",
             body=(ONE_IDEA +
                   "A time budget is a short plan for where the minutes go. It hands each stage of the essay its "
                   "own protected block:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>READ</strong>: give the source real minutes so you "
                   "understand the prompt and gather the evidence you will use.</li>"
                   "<li style=\"margin:4px 0\"><strong>PLAN</strong>: protect minutes to set your thesis and "
                   "order your points before you draft.</li>"
                   "<li style=\"margin:4px 0\"><strong>DRAFT</strong>: write the essay in the block of minutes "
                   "that remain, not in whatever is left over.</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: reserve minutes at the end to reread and "
                   "fix gaps before you submit.</li></ul>"
                   "The failure mode is drafting until time runs out, which leaves reading rushed and planning "
                   "and checking crowded out. Budget the minutes first, then write.")),
        Slot("TEACH", "teach_card", "How to build the budget, stage by stage",
             body=("Here is the order of work for a 40-minute window. A common split is read 7, plan 6, draft "
                   "23, check 4:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>WRITE THE BUDGET</strong>: before anything else, note the "
                   "minutes for read, plan, draft, and check.</li>"
                   "<li style=\"margin:4px 0\"><strong>READ</strong>: use the reading minutes to understand the "
                   "prompt and collect facts you can cite.</li>"
                   "<li style=\"margin:4px 0\"><strong>PLAN</strong>: in the planning minutes, set the thesis and "
                   "the order of points. A thesis is a one-sentence claim that takes a side, and the whole essay "
                   "defends it.</li>"
                   "<li style=\"margin:4px 0\"><strong>DRAFT</strong>: write the intro, body, and conclusion "
                   "inside the drafting minutes, and move on when they are up.</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: spend the last minutes rereading and "
                   "fixing the biggest gaps.</li></ol>"
                   "The minutes are yours to set, but planning and checking must get protected time, not the "
                   "leftovers.")),
        Slot("TEACH", "stimulus_display", "Read the source: build the power, or build the grid?",
             ref="ACC-W910-ARG-LESSON-GRIDSPENDING", bank="infrastructure_spending",
             body=("Read this source on grid and generation spending. Picture a 40-minute exam window: as you "
                   "read, notice how much time understanding the prompt and gathering evidence would take, so "
                   "you can budget the stages. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + the budget check, then the sort =====
        Slot("MODEL", "annotated_before_after", "Watch draft-until-out become a budgeted window",
             bank="infrastructure_spending",
             body=("Here is a draft-until-time-runs-out approach rebuilt as a budgeted window. Read the BEFORE, "
                   "then the AFTER, and notice which stages got protected minutes." + BEFORE_AFTER_HTML +
                   " The BEFORE drafts with no budget, so it runs out unfinished. The AFTER names the moves in "
                   "order: allot the minutes, hold each stage to them, and defend planning and checking. Budget "
                   "the minutes is the move." + REMEMBER +
                   "When you set your own budget, run this check on the four numbers before you draft.")),
        Slot("MODEL", "discrimination", "Which approach budgets the exam window?",
             ref="", labeled_grade_c=True, bank="infrastructure_spending",
             body=("You have watched a no-budget draft become a budgeted window. Now sort these three approaches: "
                   "which one BUDGETS the minutes, and which two do not? "
                   "(A) Allot minutes up front, read 7, plan 6, draft 23, check 4, and move to the next stage the "
                   "moment its minutes run out.  "
                   "(B) Open the exam, start drafting the essay right away, and keep writing without stopping "
                   "until the proctor finally calls time at the end.  "
                   "(C) Spend nearly the whole window drafting a long body and leave just a single minute at the "
                   "very end for reading and planning together. "
                   "Correct: A. Only A gives each stage its own protected minutes; B protects nothing and C "
                   "starves reading, planning, and checking to feed the draft."),
             choices=[
                 {"id": "A", "text": "Allot minutes up front, read 7, plan 6, draft 23, check 4, and move to the next stage the moment its minutes run out.",
                  "correct": True,
                  "why": "Correct. Every stage gets its own protected minutes decided before writing, so planning and checking survive and the essay finishes complete."},
                 {"id": "B", "text": "Open the exam, start drafting the essay right away, and keep writing without stopping until the proctor finally calls time at the end.",
                  "correct": False,
                  "why": "This is drafting until time runs out. No stage is protected, so reading is rushed and there is no reserved planning or checking time."},
                 {"id": "C", "text": "Spend nearly the whole window drafting a long body and leave just a single minute at the very end for reading and planning together.",
                  "correct": False,
                  "why": "One shared minute for reading and planning starves the stages that make an essay coherent. Drafting is not the only thing that needs protected minutes."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this exam approach most need?",
             bank="infrastructure_spending",
             body=("Diagnose before the reveal. A student says: 'On the exam I just write as much as I can until "
                   "they call time.' Which single move would most improve the result? "
                   "(A) set a minute budget for reading, planning, drafting, and checking before writing one word  "
                   "(B) write faster and pack in as many words as possible before the exam window finally closes  "
                   "(C) skip writing the conclusion entirely so there are more minutes free to draft a longer body  "
                   "(D) make the opening paragraph much longer so the essay looks developed right from the start"),
             feedback=("Correct: A. Writing as much as possible with no budget is exactly what leaves essays "
                       "unplanned and unchecked. The fix allots protected minutes to each stage. Writing faster "
                       "(B), dropping the conclusion (C), or padding the opening (D) still leave planning and "
                       "checking with no protected time.")),

        # ===== SUPPORTED: set the budget + plan (multi_paragraph) - the frame is the highest-value scaffold =====
        Slot("SUPPORTED", "production_frq", "Set your budget, then plan the essay",
             ref="", bank="infrastructure_spending", rubric_ref="rc.ap", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Set a time budget for a 40-minute window on the grid-spending prompt, then use the "
                       "planning minutes to outline the essay.",
                 setapart_block=setapart("Fill in this budget and plan:",
                                         "Budget: read __, plan __, draft __, check __. Thesis: ______ (your side). "
                                         "Point 1: ______ + its evidence. Point 2: ______ + its evidence. "
                                         "Point 3: ______ + its evidence."),
                 closer="Write the four budget numbers so planning and checking each get protected minutes, then "
                        "write a one-line thesis that takes a side and three ordered points, each naming the "
                        "source fact it will use. This budget and plan are what you will build the essay from.")),
        # ===== INDEPENDENT: build the whole essay on the budget (essay ceiling) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write a full essay on your budget",
             ref="", bank="infrastructure_spending", rubric_ref="rc.ap", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now, build the whole essay on your budget.",
                 closer="Using a minute budget for a 40-minute window, write a complete argument essay on the "
                        "grid-spending prompt: plan in the planning minutes, draft in the drafting minutes, and "
                        "reserve the check minutes to fix gaps before submitting. There is no platform timer; "
                        "treat the budget as your own discipline. Confirm every stage got its minutes and the "
                        "essay is complete and checked. Budgeting the minutes is what every timed exam essay is "
                        "built on, and you are ready to do it cold.")),

        # DIAGNOSIS = metacognitive pacing check: reread your OWN draft and run the three-question budget check on
        # how you spent your minutes. Pacing cannot be bought back on a finished draft, so failing rows route to a
        # process fix on the NEXT write; only a substance gap the pacing left behind (a missing conclusion, an
        # unchecked error) is fixed in the draft now. Same taught bank (load balance). Self-contained: the checklist
        # is the scaffold and the grader scores the diagnosis within the item.
        Slot("MODEL", "diagnosis_frq", "Check your own budget and essay",
             ref="", bank="infrastructure_spending", scored=True,
             body=frq_prompt(
                 intro="Reread the essay you just wrote and look at how you spent your minutes. Run this pacing check on YOUR draft, one row at a time.",
                 checklist_block=checklist(title="Check your own draft, row by row:", rows=[
                     ("Does reading get real minutes?", "If reading got almost none, the prompt and evidence get skipped. Carve out minutes to read."),
                     ("Are planning and checking protected?", "If planning or checking got only leftovers, give each its own protected minutes."),
                     ("Does drafting fit what remains?", "If drafting swallowed the window, the other stages starve. Shrink drafting so read, plan, and check fit."),
                 ]),
                 closer="The rows above are all about how you spent your minutes, and you cannot buy those minutes "
                        "back by editing a finished draft. For each row that fails, note it and adjust your process "
                        "on your NEXT write, deciding those protected minutes before you start. If the rushed pacing "
                        "left a substance gap you can still repair, such as a missing conclusion or an unchecked "
                        "error, fix that gap in your draft now. Finish by naming how many minutes you will protect "
                        "for planning next time.")),

        # TRANSFER routed out to the gate/PP100 (essay-grain verdict): the lesson ends at the INDEPENDENT write
        # plus its own-draft self-revision. The PP100 mastery task is a separate resource and is unaffected.
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
