"""
lesson_g12_l09_timed_argument.py  -  G12 KC C.12.02, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD, ceiling essay). V3.1.

G12 course L09 (Unit 2, build), rebuilt to the v3.1 build spec (hand-authored). Teaching point (KEPT): rehearse
a COMPLETE AP argument essay under a self-imposed budget, sustaining quality end to end (a situated thesis,
body paragraphs that hold the tension, a defended conclusion), rather than practicing only the opening moves.
Delivery UNTIMED (transferable pacing strategy, no platform timer). Binds the G12 argument LESSON source.

Preserved EXACTLY from the current L09: id="ACC-W910-L-G12-C1202-0009", lesson_type=7, mnemonic_status="proposal",
kc="C.12.02", unit, the bound stimuli (WORKFORCEINVEST taught -> WATERTRADEOFF transfer), and every production_frq
unit= value (SUPPORTED plan = multi_paragraph, INDEPENDENT + TRANSFER = essay). The ladder climbs to the essay,
the type-7 ceiling.

V3.1 spine: ONE_IDEA teal callout + real <ul>/<ol> lists (no wall of text); coping-model before/after with a
literal BEFORE and AFTER; a REMEMBER dashed box holding a 3-question reread checklist; explicit choices=[] on the
discrimination (no leaked "Grade-C" / "design bet" label); deterministic frq_prompt/setapart/checklist bodies (no
"Step 1/2" prose, no "Scored on ..." chrome). Facts trace to the bound source (US BLS / US NSF). Own words, no
fabricated figures, no em dashes. Passes all 23 lesson_contract gates + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Rehearse the <strong>whole argument, end to end</strong>, '
'under a budget you set: a situated thesis, body paragraphs that hold the tension, and a defended conclusion. '
'Redrafting the opening over and over polishes the start and never trains the ending.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: is the whole thing finished?</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, run the plan and the draft past these three:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does the plan cover every body paragraph, not just the first one?</li>'
'<li style="margin:2px 0">Is there a defended conclusion, not just a repeated thesis?</li>'
'<li style="margin:2px 0">Did the budget leave enough time so the ending got finished work too?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you submit.</div></div>')

# coping-model before/after: opening-only practice (a polished thesis, then nothing) rebuilt into a full-write
# rehearsal carried to a defended conclusion. Contains BOTH a literal BEFORE and AFTER (content_depth). A short
# structural sketch, not a whole essay - the point is the opening-only vs end-to-end contrast. Figures trace to
# the bound WORKFORCEINVEST source (US BLS 3.1 percent; US NSF STEM share 22 to 24 percent).
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> a polished opening, then nothing</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">THESIS</span> "Because employment in fields like data science is projected to grow far '
      'faster than the roughly 3.1 percent expected across all jobs, a society should invest first in preparing '
      'more people for that work, but only if it also cushions the workers the shift displaces."</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">A sharp opening thesis, and then the draft stops. No '
    'body carries the claim and no conclusion defends it, so this rehearsal never trains the ending an FRQ has to '
    'reach.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> the same argument, carried to the end</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">THESIS</span> "Because employment in fields like data science is projected to grow far '
      'faster than the roughly 3.1 percent expected across all jobs, a society should invest first in preparing '
      'more people for that work, but only if it also cushions the workers the shift displaces." '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">BODY</span> "Preparation widens the pipeline through stronger math and science teaching '
      'and more community-college and apprenticeship routes, yet the STEM share of workers rose only from 22 to '
      '24 percent over the past decade, which means most workers will never enter these fields and some need '
      'transition support now." '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">CONCLUSION</span> "A budget that funds preparation first but reserves a set share for '
      'transition support answers both the growing fields and the shrinking ones, so even a reader who favors '
      'the displaced would be forced to respect the priority."</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same thesis, now carried to the end: a body beat '
    'that holds the tension and a conclusion that defends a priority. A complete argument, run end to end, is '
    'the move.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G12-C1202-0009", grade="9-10", lesson_type=7,
    unit="G12 U2 - Sustain a full argument FRQ",
    title="Rehearse a Complete Argument, End to End",
    target=("Rehearse a full AP argument essay under a self-imposed budget, sustaining quality from a situated "
            "claim through a defended conclusion, rather than practicing only the opening moves. Delivery "
            "untimed. Written at the essay. Trait: Sophistication, Development, and process."),
    acc_tags=["ACC.W.ARG.1", "ACC.W.PROD.4", "CCSS.W.11-12.1", "CCSS.W.11-12.4"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.12.02", "sot": "icm course-G12.md L09",
                "taught_stimulus": "ACC-W910-ARG-LESSON-WORKFORCEINVEST",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-WATERTRADEOFF",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": "v3.1 spine; ESSAY-TIER binds full G12 argument sources; UNTIMED (no Timeback timer).",
                "one_idea": "Rehearse the whole argument end to end under a budget, not just the opening.",
                "one_reminder": "Finished-essay check: plan covers every body paragraph? defended conclusion? budget left time for the ending?",
                "version_note": ("V3.1 rebuild of L09. Replaced the two wall-of-text teach cards with a ONE_IDEA "
                                 "callout + real <ul>/<ol> lists (format_fidelity); removed the leaked internal "
                                 "label ('a Grade-C design bet we label as a bet') from the discrimination and "
                                 "moved the options to explicit choices=[]; fixed the duplicated phrase in the "
                                 "predict_the_fix option (D); deterministic frq_prompt/setapart/checklist bodies "
                                 "(no 'Step 1/2' prose, no 'Scored on' chrome); coping-model before/after kept; "
                                 "3-question reread check folded in as a REMEMBER box. Preserved id, type 7, "
                                 "kc=C.12.02, mnemonic_status=proposal, bound stimuli, and every production_frq "
                                 "unit= value (SUPPORTED=multi_paragraph, INDEPENDENT/TRANSFER=essay)."),
                "council": ("T7/BUILD G12 sustain build: full ARGUMENT FRQ rehearsal end to end under own budget, "
                            "delivery untimed. full-write-vs-opening-only discrimination labeled Grade-C in code "
                            "(labeled_grade_c=True), not in student text. BUILD=proposal; unit=essay."),
                "review_provenance": "built to the G9 L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["full-argument-rehearsal", "run-the-whole-argument-end-to-end"],
    slots=[
        # ===== TEACH: the one idea + the parts (as a list), then the order of work (as a list) =====
        Slot("TEACH", "teach_card", "The one idea: rehearse the whole argument, not just the start",
             body=(ONE_IDEA +
                   "You already own each of these moves. A full-write rehearsal puts them together, in one "
                   "paced sitting, and carries them to the end:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Situated thesis</strong>: a thesis is a one-sentence "
                   "claim that states the position your whole essay defends, placed inside the real tension the "
                   "source lays out.</li>"
                   "<li style=\"margin:4px 0\"><strong>Body that holds the tension</strong>: paragraphs that "
                   "grant the other side its strongest fact and still argue the priority.</li>"
                   "<li style=\"margin:4px 0\"><strong>Defended conclusion</strong>: an ending that defends the "
                   "priority, not one that just repeats the thesis.</li>"
                   "<li style=\"margin:4px 0\"><strong>A budget</strong>: time you set aside for planning and "
                   "checking, so the ending gets finished work too.</li></ul>"
                   "The trap is polishing the introduction over and over: it feels productive but never trains "
                   "you to carry quality through paragraph three and the conclusion, which is exactly where full "
                   "essays fall apart.")),
        Slot("TEACH", "teach_card", "How to run it, stage by stage",
             body=("Here is the order of work. Delivery here has no clock; the budget is your discipline. Follow "
                   "the stages and the whole essay gets rehearsed, not just its opening:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>BUDGET</strong>: decide up front how much of your sitting "
                   "goes to planning, to drafting each part, and to checking. A workable split gives the largest "
                   "share to drafting, with a smaller slice each for planning up front and checking at the end, so "
                   "every paragraph including the conclusion gets built.</li>"
                   "<li style=\"margin:4px 0\"><strong>PLAN</strong>: fast-plan the whole argument, the situated "
                   "thesis and the point each body paragraph will hold, before drafting a word.</li>"
                   "<li style=\"margin:4px 0\"><strong>DRAFT</strong>: write the situated thesis, then the "
                   "tension-holding body, pacing so no paragraph starves the next.</li>"
                   "<li style=\"margin:4px 0\"><strong>CONCLUSION</strong>: defend the priority the argument "
                   "earned.</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: reread the finished essay against a short "
                   "list, does the plan cover every body paragraph, is there a defended conclusion, did the "
                   "budget leave time for the ending?</li></ol>"
                   "You are assembling moves you already own, in this order, into one complete essay.")),
        Slot("TEACH", "stimulus_display", "Read the source: prepare workers or protect them?",
             ref="ACC-W910-ARG-LESSON-WORKFORCEINVEST", bank="public_health",
             body=("Read this source on preparing more people for growing technical fields or protecting the "
                   "workers the change leaves behind. Because your job is a full FRQ, read the whole thing and "
                   "gather a position worth defending plus the facts (with their sources) you can carry across "
                   "body paragraphs. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + check tool, then discrimination =====
        Slot("MODEL", "annotated_before_after", "Watch opening-only practice become a full-write rehearsal",
             bank="public_health",
             body=("Here is opening-only practice rebuilt into a full-write rehearsal. Read the BEFORE, then the "
                   "AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE polishes the start and stops. The AFTER runs the same argument end to end: a "
                   "body beat that holds the tension and a conclusion that defends a priority. Running the "
                   "complete argument is the move." + REMEMBER +
                   "When you rehearse your own, run the stages in order, then check the whole thing before you "
                   "submit.")),
        Slot("MODEL", "discrimination", "Which rehearsal builds full-essay endurance?",
             ref="", labeled_grade_c=True, bank="public_health",
             body=("You have watched opening-only practice become a full-write rehearsal. Now spot the target: "
                   "which sitting builds endurance for a complete essay, and which trains only the opening? "
                   "(A) Polish the introduction and first body paragraph over and over until every sentence "
                   "reads perfectly, then stop working once the opening finally feels strong enough to submit.  "
                   "(B) Budget the stages, fast-plan the whole case, and draft it from situated claim through "
                   "defended conclusion in one paced pass, then check the finished essay against a list.  "
                   "(C) Spend the sitting gathering more facts and sharper vocabulary to use later, then write "
                   "one strong opening paragraph and leave the rest of the argument for a different day. "
                   "Correct: B runs the complete argument end to end, so the conclusion gets finished work; A "
                   "and C both stop at the opening, so the ending is never rehearsed."),
             choices=[
                 {"id": "A", "text": "Polish the introduction and first body paragraph over and over until every sentence reads perfectly, then stop working once the opening finally feels strong enough to submit.",
                  "correct": False,
                  "why": "This is opening-only practice. It never reaches the body and conclusion, which is exactly where full essays fall apart."},
                 {"id": "B", "text": "Budget the stages, fast-plan the whole case, and draft it from situated claim through defended conclusion in one paced pass, then check the finished essay against a list.",
                  "correct": True,
                  "why": "Correct. This runs the complete argument end to end under a budget, so the conclusion gets finished work, not just the opening."},
                 {"id": "C", "text": "Spend the sitting gathering more facts and sharper vocabulary to use later, then write one strong opening paragraph and leave the rest of the argument for a different day.",
                  "correct": False,
                  "why": "Collecting material and writing one opening is still opening-only. The body and conclusion are never rehearsed, so endurance never builds."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this rehearsal habit most need?",
             bank="public_health",
             body=("Diagnose before the reveal. A student always produces a strong opening and never a finished "
                   "essay, because every practice sitting stops after the first paragraph. Which single change "
                   "would most improve exam performance? "
                   "(A) rehearse the complete argument end to end under a budget, so the conclusion gets "
                   "finished work too  "
                   "(B) keep polishing the introduction and opening paragraph until they read even more sharply "
                   "than they already do  "
                   "(C) memorize a longer list of advanced vocabulary words to work into the argument while "
                   "you are drafting it  "
                   "(D) read more sample introductions from high-scoring essays and copy the way those strong "
                   "openers are built"),
             feedback=("Correct: A. Endurance comes only from finishing whole essays; the fix rehearses the "
                       "complete argument under a budget so the conclusion gets real work. A sharper intro (B), "
                       "more vocabulary (C), or more sample intros (D) all keep the practice stuck at the "
                       "opening, which is the exact habit that has to change.")),

        # ===== SUPPORTED: budget + fast-plan the whole argument (multi_paragraph) - the frame is the scaffold =====
        Slot("SUPPORTED", "production_frq", "Budget and plan the full argument",
             ref="", bank="public_health", rubric_ref="rc.ap", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Before you draft, budget your sitting and fast-plan the WHOLE argument on the workforce "
                       "prompt, end to end.",
                 setapart_block=setapart("Fill in this plan:",
                                         "Budget: ______ to plan, ______ to draft each part, ______ to check. Situated thesis: ______. Body point 1 (and the tension it holds): ______. Body point 2: ______. Defended conclusion: ______."),
                 closer="Write your stage budget and a fast plan that names the situated thesis, the tension "
                        "each body paragraph will hold, and what the conclusion defends. This plan is what you "
                        "will build the whole essay from.")),
        # DIAGNOSIS = self-revision: reread your OWN just-written essay and run the 3-question check on it,
        # fixing any line that fails. Same taught source (load balance). Self-contained: the checklist is the
        # scaffold and the grader scores the diagnosis within the item.
        Slot("MODEL", "diagnosis_frq", "Check the plan reaches the conclusion",
             ref="", bank="public_health", scored=True,
             body=frq_prompt(
                 intro="Reread the essay you just wrote. Run this checklist on YOUR draft and fix any line that fails.",
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Does your essay build every body paragraph, not just the opening?", "If a later paragraph is thin or missing, name the point it should hold and the tension it grants, then build it out."),
                     ("Does your conclusion defend the priority, not just repeat the thesis?", "If it only restates the claim, revise it to defend why that priority holds even for a reader who leans the other way."),
                     ("Did the ending get finished work, or did it run out of time?", "If the conclusion came out rushed, adjust your stage budget on your next write so the ending gets real time, not the last thirty seconds."),
                 ]),
                 closer="For the body and conclusion rows, name what is off in one sentence and fix it in your "
                        "draft now. The pacing row is about your process, not this finished draft, so instead "
                        "note one change to your stage budget for your next write. Finish by naming what your "
                        "conclusion defends.")),

        # ===== INDEPENDENT: rehearse the whole essay from the plan (essay ceiling) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Rehearse the full argument",
             ref="", bank="public_health", rubric_ref="rc.ap", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now, rehearse the whole essay from your budget and plan.",
                 closer="Write a complete argument essay on the workforce prompt end to end: a situated claim, "
                        "body paragraphs that hold the tension, and a conclusion that defends a priority. There "
                        "is no platform timer; run your own budget and pacing, then run the reread check and fix "
                        "any part that fails. Carrying a complete argument to a finished conclusion is what every "
                        "real AP argument is built on, and you are ready to do it cold. Take the time you need.")),
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
