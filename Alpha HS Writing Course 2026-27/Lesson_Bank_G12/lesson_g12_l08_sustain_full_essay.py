"""
lesson_g12_l08_sustain_full_essay.py  -  G12 KC C.12.02, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD, ceiling essay). V3.1.

G12 course L08 (Unit 2, intro), rebuilt to the v3.1 build spec (hand-authored). Teaching point (KEPT): sustaining
a full AP essay = PACING the whole essay so quality holds from intro to conclusion, rather than front-loading a
brilliant open and letting the ending starve. It recycles a time BUDGET (T1) and a fast PLAN (T2) from G11, and
adds pacing the DRAFT (a rough share of the drafting minutes per body paragraph). Taught as a transferable exam
STRATEGY; Timeback delivery is UNTIMED (no platform timer). Binds the G12 argument LESSON source.

Preserved EXACTLY from the current L08: id="ACC-W910-L-G12-C1202-0008", lesson_type=7, mnemonic_status="proposal",
kc=C.12.02, the unit, the bound stimuli (WATERTRADEOFF taught -> WORKFORCEINVEST transfer), and the production
unit ladder (SUPPORTED plan = multi_paragraph, INDEPENDENT + TRANSFER = essay), which climbs to the type-7 essay.

V3.1 changes vs the current L08:
  1. FIXED the leaked internal label: the discrimination no longer says "a Grade-C design bet we label as a bet";
     it is a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}] (leaked_internal_label).
  2. FIXED the wall-of-text teach card: the prose block is now a ONE_IDEA callout + real <ul>/<ol> lists of the
     three pacing moves and the order of work (format_fidelity + the v3.1 "parallel items as a list" rule).
  3. Deterministic FRQ + diagnosis prompts via frq_prompt/setapart/checklist (no "Step 1/2" prose, no
     "Scored on ..." chrome); coping-model before/after kept; the pacing check folded in as a real <ol> REMEMBER
     box at the point of first use.
Own words, no fabricated figures (every figure traces to the bound USGS source), no em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist, outline_table

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Sustaining a full essay is <strong>pacing the whole '
'thing</strong>, not just starting strong. The last body paragraph and the conclusion have to get the same '
'finished work as the intro, so you spend the minutes on purpose instead of pouring them all into the opening.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: pace the whole essay</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you draft, and again halfway through, ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Did planning and checking get their own protected minutes?</li>'
'<li style="margin:2px 0">Does every body paragraph get a share of the drafting minutes, not just the first?</li>'
'<li style="margin:2px 0">Are minutes reserved so the last paragraph and the conclusion still get finished work?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, rebalance the minutes before you keep drafting.</div></div>')

# coping-model before/after: a front-loaded essay (strong open, one flat closing line) rebuilt into a paced one
# (same open, a finished close). Contains BOTH a literal BEFORE and AFTER (content_depth). The contrast is
# pacing, not ideas: same opening, different amount of drafting time left for the end.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> strong open, faded close</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">STRONG OPENING</span> "When a drying region cannot spare water for both farms and '
      'power plants, the two largest daily water withdrawals in the country, it must '
      'protect one over the other, and that choice deserves a defended rule rather than a reflex." '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">RUSHED CLOSE</span> "So farms matter more, and the region should pick them."</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The opening is fully developed, but the close got '
    'whatever minutes were left, so it shrinks to one flat line. A faded ending is a pacing failure, not a '
    'thinking failure.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> quality sustained to the last sentence</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">STRONG OPENING</span> "When a drying region cannot spare water for both farms and '
      'power plants, the two largest daily water withdrawals in the country, it must '
      'protect one over the other, and that choice deserves a defended rule rather than a reflex." '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">FINISHED CLOSE</span> "So in the driest years a region should protect irrigation '
      'first, yet reserve enough power for the electric pumps that lift the very groundwater those farms depend '
      'on, a rule that a reader who favors the grid would still have to take seriously."</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same opening, but the final sentence gets the same '
    'finished work as the first, because the drafting minutes were shared so the close was never starved. '
    'Quality that holds to the last sentence is the move.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G12-C1202-0008", grade="9-10", lesson_type=7,
    unit="G12 U2 - Sustain a full essay (pace end to end)",
    title="Sustain the Whole Essay, Do Not Front-Load It",
    target=("Carry a full essay end to end under a budget (recycling time-budget and fast-plan) so quality "
            "holds from intro to conclusion, rather than front-loading and fading. A transferable exam strategy "
            "(Timeback delivery is untimed). Written at the essay. Trait: Development, Organization, and "
            "process."),
    acc_tags=["ACC.W.PROD.4", "CCSS.W.11-12.4"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.12.02", "sot": "icm course-G12.md L08",
                "taught_stimulus": "ACC-W910-ARG-LESSON-WATERTRADEOFF",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-WORKFORCEINVEST",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": ("v3.1 spine; ESSAY-TIER binds full G12 argument sources; recycles T1/T2 pacing; "
                             "teaches the sustained-writing STRATEGY, Timeback delivery UNTIMED (no timer)."),
                "one_idea": "Sustaining a full essay is pacing the whole thing, not just starting strong.",
                "one_reminder": "Pace check: planning/checking protected? every body paragraph shares the minutes? end reserved?",
                "version_note": ("V3.1 rebuild of L08. FIXED the two failing gates on the prior version: removed "
                                 "the leaked internal label ('a Grade-C design bet we label as a bet') from the "
                                 "discrimination and moved it to explicit choices=[]; broke the wall-of-text teach "
                                 "card into a ONE_IDEA callout + real <ul>/<ol> lists (format_fidelity). "
                                 "Deterministic frq_prompt/setapart/checklist bodies (no 'Step 1/2' prose, no "
                                 "'Scored on' chrome); pacing check folded in as a REMEMBER <ol> at first use. "
                                 "Preserved id, type 7, kc C.12.02, mnemonic_status=proposal, the unit, bound "
                                 "stimuli, and every production_frq unit= value (SUPPORTED=multi_paragraph, "
                                 "INDEPENDENT/TRANSFER=essay); ladder climbs to the essay ceiling."),
                "council": ("T7/BUILD G12 sustain intro: T3 sustain-under-time (pace a full essay end to end) "
                            "recycling T1 budget + T2 fast-plan, delivery untimed. paced-vs-front-loaded "
                            "discrimination labeled_grade_c in code only. BUILD=proposal; unit=essay."),
                "review_provenance": "built to the G9 L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["sustain-full-essay", "pace-the-body-evenly"],
    slots=[
        # ===== TEACH: the one idea + the three pacing moves (as a list), then the order of work (as a list) =====
        Slot("TEACH", "teach_card", "The one idea: sustaining is pacing the whole essay",
             body=(ONE_IDEA +
                   "At mastery the challenge is not thinking of good ideas; it is carrying quality all the way to "
                   "the end. Sustaining recycles two moves you already own, budgeting the stages and fast-planning "
                   "the essay, and adds a third, pacing the draft:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Budget the stages</strong>: split the work into rough "
                   "minutes for read, plan, draft, and check, so no stage quietly eats the others. For a "
                   "40-minute window a workable split is read 5, plan 8, draft 22, check 5.</li>"
                   "<li style=\"margin:4px 0\"><strong>Fast-plan the whole essay</strong>: a few lines naming the "
                   "thesis, which is a one-sentence claim that states your position, plus the ordered points "
                   "that will defend it.</li>"
                   "<li style=\"margin:4px 0\"><strong>Pace the draft</strong>: give each body paragraph a rough "
                   "share of the drafting minutes, and move on when its share is up.</li></ul>"
                   "The failure mode is front-loading: a beautiful intro and first paragraph, then a collapse. "
                   "You will practice this without a clock so the habit is ready when a real exam has one.")),
        Slot("TEACH", "teach_card", "How to pace it, stage by stage",
             body=("Here is the order of work. Follow it and the minutes take care of themselves:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>BUDGET</strong>: name the minutes for read, plan, draft, "
                   "and check before you write a word.</li>"
                   "<li style=\"margin:4px 0\"><strong>PLAN</strong>: write the thesis and the ordered points, "
                   "each naming the evidence it will use.</li>"
                   "<li style=\"margin:4px 0\"><strong>SHARE THE DRAFTING MINUTES</strong>: divide the drafting "
                   "block across the body paragraphs and the conclusion, so the last one is not left on scraps.</li>"
                   "<li style=\"margin:4px 0\"><strong>DRAFT AND MOVE ON</strong>: when a paragraph's share is "
                   "spent, close it and start the next, even if you could keep polishing.</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: keep a few reserved minutes to reread and "
                   "confirm the ending got finished work.</li></ol>"
                   "You already own the budget and the plan; the new discipline is spending the drafting minutes "
                   "evenly so quality holds to the end. To watch the minutes here, keep a clock or a phone timer "
                   "in view and glance at it as you finish each paragraph; on a real exam the proctor's clock does "
                   "the same job.")),
        Slot("TEACH", "stimulus_display", "Read the source: water for food or power?",
             ref="ACC-W910-ARG-LESSON-WATERTRADEOFF", bank="automation_policy",
             body=("Read this source on protecting water for food or for power. Picture an exam window: budget "
                   "the stages, then plan the whole essay so you can pace the body evenly. The text stays on "
                   "screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + pacing check, then the discrimination =====
        Slot("MODEL", "annotated_before_after", "Watch a front-loaded essay get paced",
             bank="automation_policy",
             body=("Watch a writer catch a pacing problem. First try: they draft a striking opening and keep "
                   "polishing it, then run out of minutes and end on one flat line (the BEFORE). Second try: "
                   "they run the pacing check and see the close got starved, not that the idea was weak. Final: "
                   "they share the drafting minutes so the ending gets finished work (the AFTER). Read the "
                   "BEFORE, then the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE fades after a strong start; the AFTER paces the body so the last sentence is as "
                   "finished as the first. Sustaining the whole essay is the move." + REMEMBER +
                   "When you build your own, run this check before you draft and again halfway through.")),
        Slot("MODEL", "discrimination", "Which approach sustains the whole essay?",
             ref="", labeled_grade_c=True, bank="automation_policy",
             body=("You have watched a front-loaded essay get paced. Now sort these before you write: which "
                   "approach SUSTAINS the essay, and which one FRONT-LOADS it? "
                   "(A) Pour your strongest effort into a striking introduction and a fully developed first body "
                   "paragraph, polish them until they truly shine, and then race through the paragraphs and the "
                   "conclusion that remain with whatever minutes happen to be left over.  "
                   "(B) Give the introduction, each body paragraph, and the conclusion a rough share of the "
                   "drafting minutes at the start, then move on when a paragraph's share is spent, so the final "
                   "paragraph and the conclusion still get careful work.  "
                   "(C) Draft the paragraphs in whatever order they happen to occur to you, spend as long on "
                   "each one as it seems to need, and trust that the essay will come out balanced once every "
                   "idea you thought of has finally made it onto the page. "
                   "Correct: B. Approach B shares the minutes so the ending gets finished; A front-loads and "
                   "lets the close starve, and C never budgets, so the earliest paragraphs eat the time the "
                   "later ones need."),
             choices=[
                 {"id": "A", "text": "Pour your strongest effort into a striking introduction and a fully developed first body paragraph, polish them until they truly shine, and then race through the paragraphs and the conclusion that remain with whatever minutes happen to be left over.",
                  "correct": False,
                  "why": "This front-loads. The budget is spent early, so the last paragraph and conclusion get scraps, and quality fades exactly where a reader is deciding your score."},
                 {"id": "B", "text": "Give the introduction, each body paragraph, and the conclusion a rough share of the drafting minutes at the start, then move on when a paragraph's share is spent, so the final paragraph and the conclusion still get careful work.",
                  "correct": True,
                  "why": "Correct. Sharing the drafting minutes up front is pacing: every part gets finished work, so quality holds from the intro to the last sentence."},
                 {"id": "C", "text": "Draft the paragraphs in whatever order they happen to occur to you, spend as long on each one as it seems to need, and trust that the essay will come out balanced once every idea you thought of has finally made it onto the page.",
                  "correct": False,
                  "why": "No budget at all. Without a share per paragraph, the earliest paragraphs eat the minutes the later ones need, and the ending still gets rushed."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this essay's pacing most need?",
             bank="automation_policy",
             body=("Diagnose before the reveal. A student writes a superb first half, then a rushed, unfinished "
                   "second half every time. Which single move would most improve the result? "
                   "(A) give each body paragraph a rough share of the drafting minutes and move on when its "
                   "share is spent  "
                   "(B) polish the introduction even more so the strong opening becomes sharper and more "
                   "impressive still  "
                   "(C) add even more detail and a second example to the first body paragraph to make it the "
                   "strongest one  "
                   "(D) think up several more ideas and arguments before starting to draft the actual essay itself"),
             feedback=("Correct: A. The problem is pacing, not ideas; sharing the drafting minutes is what lets "
                       "the later paragraphs get finished. A more careful intro (B) or a bigger first paragraph "
                       "(C) worsen the front-loading; more ideas (D) do not help if the ending still gets rushed.")),

        # ===== SUPPORTED: plan + pacing frame (multi_paragraph) - the frame is the highest-value scaffold =====
        Slot("SUPPORTED", "production_frq", "Budget, fast-plan, and pace the essay",
             ref="", bank="automation_policy", rubric_ref="rc.ap", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="For a 40-minute window on the water trade-off, write your budget, your fast plan, and a "
                       "rough share of the drafting minutes per body paragraph before you draft. First set your "
                       "time budget: read ___ min, plan ___ min, draft ___ min, check ___ min. Then use the "
                       "outline grid below for your fast plan.",
                 setapart_block=outline_table(title="Copy this outline, then fill in each blank:", rows=[
                     ("THESIS", "______ (your position)"),
                     ("POINT 1", "______ + evidence"),
                     ("POINT 2", "______ + evidence"),
                     ("POINT 3", "______ + evidence"),
                 ]),
                 closer="Below the grid, set your drafting share: intro ___ min, each body paragraph ___ min, "
                        "conclusion ___ min. Write the whole frame out. The goal is a plan that paces the body so "
                        "the last paragraph and the conclusion still get finished minutes, not scraps.")),
        # ===== INDEPENDENT: sustain the whole essay from the plan (essay ceiling) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Sustain the full essay",
             ref="", bank="automation_policy", rubric_ref="rc.ap", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now, carry the whole essay from your plan and pacing.",
                 closer="Write a complete argument essay on the water trade-off so the last body paragraph and "
                        "the conclusion are as finished as the first. There is no platform timer, so keep a clock "
                        "or phone timer in view and run your own budget and pacing, then reread to confirm every "
                        "paragraph got finished work and the "
                        "conclusion is complete. This even pacing is what every strong exam essay is built on, "
                        "and you are ready to do it cold. Take the time you need.")),

        # DIAGNOSIS = self-revision: reread your OWN just-written draft and run the 3-question pacing check on it,
        # fixing any line that fails. Same taught source (load balance). Self-contained: the checklist is the
        # scaffold and the grader scores the diagnosis within the item.
        Slot("MODEL", "diagnosis_frq", "Run the pacing check on your own draft",
             ref="", bank="automation_policy", scored=True,
             body=frq_prompt(
                 intro="Reread the essay you just wrote and run this checklist on YOUR draft.",
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Did planning and checking get their own protected minutes?", "If planning up front or the final reread got squeezed out, reserve minutes for both on your next write, before the drafting block."),
                     ("Did every body paragraph get a share of the drafting minutes, not just the first?", "If the first paragraph took most of the block, split the drafting minutes more evenly across all the paragraphs on your next write."),
                     ("Do your last body paragraph and conclusion have the same finished work as your opening?", "If the ending is thin or shrinks to a flat line while the opening is fully developed, build it out now so it is as finished as the first paragraph."),
                 ]),
                 closer="The two pacing rows (protected minutes for planning and checking, and an even share of "
                        "the drafting minutes) cannot be repaired in a finished draft, so carry those adjustments "
                        "into your next write. The finished-work row is about this draft, so fix it now: if your "
                        "ending is starved, build the final body paragraph and conclusion out until they are as "
                        "finished as your opening. Finish by naming how many minutes the last body paragraph got.")),
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
