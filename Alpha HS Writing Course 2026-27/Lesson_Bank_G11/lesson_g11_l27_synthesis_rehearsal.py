"""
lesson_g11_l27_synthesis_rehearsal.py  -  G11 KC C.11.05, CROSS-SOURCE-SYNTHESIS (WEAVE, essay). V3.1.

G11 L27 (Unit 6, build), rebuilt to the v3.1 build spec (hand-authored). Teaching point (KEPT): rehearse a
full synthesis end to end under a self-imposed budget - budget the stages, fast-plan the ONE argument the set
builds and which source carries each point, draft by point, and check it is woven and weighted, rather than
collapsing into a source-survey under pressure. Delivery UNTIMED (no platform timer); the budget is the
student's own discipline. KC C.11.05.

Preserved EXACTLY from the current L27: id="ACC-W1112-L-G11-C1106-0027", lesson_type=8,
mnemonic_status="proposal", kc=C.11.05, unit (G11 U6), and the bound stimuli (SYNTH-SET-0001 renewable grid
taught -> SYNTH-SET-0002 AI-workforce transfer). Every scored production unit= climbs to the essay (the type-8
ceiling): SUPPORTED plan = multi_paragraph, INDEPENDENT + TRANSFER = essay.

V3.1 changes vs the current L27:
  1. FIXED the leaked internal label: the discrimination no longer says "a Grade-C design bet we label as a
     bet"; it is a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}].
  2. FIXED the wall-of-text teach card: the prose block is now a ONE_IDEA teal callout + real <ul>/<ol> lists
     of the routine parts and the order of work (format_fidelity, "parallel items as a list" rule).
  3. Deterministic FRQ + diagnosis prompts via frq_prompt/setapart/checklist (no "Step 1/2" prose, no "Scored
     on ..." chrome); coping-model before/after kept; the woven-and-weighted check folded in at first use as a
     real <ol> REMEMBER box.
Own words, no fabricated figures (every number traces to SYNTH-SET-0001), no em dashes. Passes all 23
lesson_contract gates + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A synthesis under pressure is a <strong>ROUTINE you '
'run</strong>, not a race to summarize. Budget the stages, fast-plan the ONE argument the set builds, weave by '
'point, and check. You rehearse the whole routine so it holds when timed writing puts a clock on it.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: woven and weighted?</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, reread the whole synthesis and ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Is there ONE argument the whole set builds, not a summary of each source in turn?</li>'
'<li style="margin:2px 0">Is each source I use pulled in at the point it best carries, rather than given an equal paragraph?</li>'
'<li style="margin:2px 0">Did I protect budgeted minutes to plan and to check, not spend them all drafting?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you submit.</div></div>')

# coping-model before/after: a panic-survey (reads slow, summarizes each source, no argument, no check) rebuilt
# into a budgeted, fast-planned, WOVEN and WEIGHTED synthesis. Contains a literal BEFORE and AFTER
# (content_depth). Short structural sketch, not a full essay - the point is the survey-vs-routine contrast.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> reads slowly, then panics into a source-tour</span>'
    '<p style="margin:8px 0 0;font-size:15px">With a window to fill, the writer reads each source slowly, then '
    'drafts a paragraph that summarizes each one in turn: "Source 1 says renewables are about 21 percent of the '
    'grid. Source 2 says a clean grid is possible. Source 3 says pollution matters. Source 4 shows capacity '
    'factors." No argument is named, every source gets an equal paragraph, and the window closes with no minutes '
    'left to check.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">This is a survey, not a synthesis. The routine was '
    'never run: no budget, no fast plan, no weighting, no check.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> budgeted, fast-planned, woven and weighted</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">BUDGET</span> read and note (8), fast plan (5), draft by point (22), check (5). '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">ONE ARGUMENT</span> "The grid can move mostly to renewables, but only if the country '
      'funds storage and new power lines." '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">WEAVE BY POINT (weighted)</span> the EIA source carries "it is already climbing" '
      '(renewables reached about 21 percent and passed coal in 2022); NREL carries "feasible but conditional" '
      '(a net-zero grid by 2035 is possible only with large spending on storage and lines); the DOE capacity-'
      'factor chart carries "why it is hard" (wind runs at about 34 percent of capacity and solar about 23 '
      'percent, far below nuclear).</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same sources, but now one argument runs through '
    'them and each source is pulled in where it carries the most weight. The routine held.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1106-0027", grade="9-10", lesson_type=8,
    unit="G11 U6 - Synthesis rehearsal (whole routine under a budget)",
    title="Rehearse a Full Synthesis Under Your Own Budget",
    target=("Rehearse a full synthesis end to end under a self-imposed budget: budget the stages, fast-plan the "
            "one argument the set builds, weave by point and weight the sources, and check, rather than "
            "collapsing into a source survey under pressure. Delivery untimed. Written at the essay. Trait: "
            "Development (synthesis) and process."),
    acc_tags=["ACC.W.SRC.1", "ACC.W.PROD.4", "CCSS.W.11-12.7", "CCSS.W.11-12.4"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.05", "sot": "icm course-G11.md L27",
                "taught_stimulus": "ACC-W910-SYNTH-SET-0001",
                "transfer_stimulus": "ACC-W910-SYNTH-SET-0002",
                "playbook": "_phase2/playbook_T8_WEAVE.md",
                "one_idea": "A synthesis under pressure is a routine you run: budget, fast-plan the one argument, weave by point, check.",
                "one_reminder": "Woven-and-weighted check: one argument (not a survey)? each source at the point it carries? minutes reserved to plan and check?",
                "template": ("v3.1 spine; SYNTHESIS-TIER binds a cold synthesis set; rehearses the time-budget + "
                             "fast-plan strategies on a full synthesis, Timeback delivery UNTIMED."),
                "version_note": ("V3.1 rebuild of L27. FIXED the leaked internal label (removed 'a Grade-C "
                                 "design bet we label as a bet' from the discrimination, moved to explicit "
                                 "choices=[]); broke the wall-of-text teach card into a ONE_IDEA callout + real "
                                 "<ul>/<ol> lists (format_fidelity); deterministic frq_prompt/setapart/checklist "
                                 "bodies (no 'Step 1/2' prose, no 'Scored on' chrome); coping-model before/after "
                                 "kept; woven-and-weighted check folded in at first use as a real <ol> REMEMBER "
                                 "box. Preserved id, type 8, mnemonic_status=proposal, kc C.11.05, unit, bound "
                                 "stimuli, and every scored unit= (SUPPORTED=multi_paragraph, "
                                 "INDEPENDENT/TRANSFER=essay); ladder climbs to essay."),
                "review_provenance": "built to the G9 L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["synthesis-under-budget", "rehearse-the-whole-routine"],
    slots=[
        # ===== TEACH: the one idea + the routine parts (list), then the order of work (list) =====
        Slot("TEACH", "teach_card", "The one idea: a synthesis is a routine you run",
             body=(ONE_IDEA +
                   "To synthesize means to weave several sources into ONE argument the whole set builds toward, "
                   "instead of summarizing each source on its own. Under pressure the usual failure is the "
                   "opposite: a source-tour, one summary paragraph per source, with no argument and no time "
                   "left to check. The rehearsal today runs the whole routine, in this order:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>BUDGET the stages</strong>: split your window into read, "
                   "plan, draft, and check, and protect the plan and check minutes.</li>"
                   "<li style=\"margin:4px 0\"><strong>FAST-PLAN the one argument</strong>: name the single "
                   "argument the set builds, and note which source carries each point.</li>"
                   "<li style=\"margin:4px 0\"><strong>WEAVE by point (weighted)</strong>: draft organized by "
                   "point, pulling in each source where it carries the most weight, not one paragraph per "
                   "source.</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: reread to confirm it is woven and "
                   "weighted before you submit.</li></ul>"
                   "The trap is skipping straight to summaries. Run the routine instead.")),
        Slot("TEACH", "teach_card", "How to run it, stage by stage",
             body=("Here is the order of work for the window. Follow it and the synthesis assembles as one "
                   "argument instead of a tour:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>READ and note</strong>: read the set once and note what "
                   "each source can carry, then stop reading.</li>"
                   "<li style=\"margin:4px 0\"><strong>PLAN</strong>: in a few protected minutes, write the one "
                   "argument plus the ordered points, each tagged with the source that carries it.</li>"
                   "<li style=\"margin:4px 0\"><strong>DRAFT by point</strong>: write each planned point as a "
                   "paragraph, weaving in the sources it needs and citing each one.</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: reread against a short list, is there one "
                   "argument (not a survey), is each source at the point it carries, did you reserve minutes to "
                   "check?</li></ol>"
                   "Delivery here has no clock, so the budget is your own discipline. That is the point: you "
                   "rehearse the routine untimed so it is ready when timed writing has a timer.")),
        Slot("TEACH", "stimulus_display", "Read the source set: a renewable grid",
             ref="ACC-W910-SYNTH-SET-0001", bank="renewable_grid_synthesis",
             body=("Read this source set on whether the United States grid can run mostly on renewables. Picture "
                   "a timed-writing window: budget your reading, then look for the one argument the set builds and "
                   "which source carries each point, as a fast plan. The texts stay on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + check tool, then the discrimination =====
        Slot("MODEL", "annotated_before_after", "Watch a panic-survey become a budgeted synthesis",
             bank="renewable_grid_synthesis",
             body=("Here is the difference between panicking into a survey and running the routine. Read the "
                   "BEFORE, then the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE summarizes each source in turn with no argument and no time to check. The AFTER "
                   "budgets the stages, fast-plans one argument, and weaves the sources by point, weighting each "
                   "where it carries most. Run the routine, do not tour the sources." + REMEMBER +
                   "When you build your own, run the stages in this order, then use the check before you submit.")),
        Slot("MODEL", "discrimination", "Which rehearsal keeps the synthesis woven under pressure?",
             ref="", labeled_grade_c=True, bank="renewable_grid_synthesis",
             body=("You have watched a survey turn into a woven synthesis. Now spot the target: which writer "
                   "runs the whole routine, and which does not? "
                   "(A) The writer budgets the stages, fast-plans the one argument and which source carries each point, drafts by point, and reserves minutes to check it is woven and weighted.  "
                   "(B) The writer reads every source slowly, then drafts a separate summary paragraph of each one in turn until the window closes, naming no argument and leaving no minutes to check the result.  "
                   "(C) The writer skims fast, picks the two easiest sources to retell, and gives each its own paragraph, then adds one sentence at the very end that finally announces an argument.  "
                   "(D) The writer fast-plans one clear argument and drafts it well, but builds every point from the single source they liked best and never brings in the rest of the set. "
                   "Correct: A. It budgets, fast-plans one argument, and weaves the sources by point, so the "
                   "synthesis holds; B tours all four sources with no argument, C retells two sources and "
                   "bolts an argument on at the end instead of building it, and D has one argument but leans on a "
                   "single source, so nothing is actually woven across the set."),
             choices=[
                 {"id": "A", "text": "The writer budgets the stages, fast-plans the one argument and which source carries each point, drafts by point, and reserves minutes to check it is woven and weighted.",
                  "correct": True,
                  "why": "Correct. This runs the whole routine: budget, fast plan, weave by point, check. One argument carries the sources instead of a tour."},
                 {"id": "B", "text": "The writer reads every source slowly, then drafts a separate summary paragraph of each one in turn until the window closes, naming no argument and leaving no minutes to check the result.",
                  "correct": False,
                  "why": "This is the panic-survey. Every source gets an equal paragraph, no argument is named, and no minutes are kept to check. It is a tour, not a synthesis."},
                 {"id": "C", "text": "The writer skims fast, picks the two easiest sources to retell, and gives each its own paragraph, then adds one sentence at the very end that finally announces an argument.",
                  "correct": False,
                  "why": "Retelling two sources and bolting an argument on at the end is not a woven, weighted argument. The argument has to be planned first and run through the whole draft."},
                 {"id": "D", "text": "The writer fast-plans one clear argument and drafts it well, but builds every point from the single source they liked best and never brings in the rest of the set.",
                  "correct": False,
                  "why": "One argument is not enough on its own. Leaning on a single source leaves the other sources unused, so nothing is woven across the set and the sources are not weighted by what each can carry."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this rehearsal most need?",
             bank="renewable_grid_synthesis",
             body=("Diagnose before the reveal. A student says: 'With a synthesis under pressure I just start "
                   "summarizing the sources so I have something down.' Which single change would most improve "
                   "the result? "
                   "(A) budget a few minutes to fast-plan the one argument and which source carries each point before drafting  "
                   "(B) summarize each source a little faster so that every text in the whole set still gets its own paragraph before the window closes  "
                   "(C) go through the entire source set one more time so that every fact feels fresh in mind before any of the summarizing begins  "
                   "(D) write a much longer introduction that previews each source in turn so the reader knows what every text will go on to cover"),
             feedback=("Correct: A. Jumping straight to summaries is exactly what produces the source-tour. The "
                       "fix spends a few budgeted minutes fast-planning the one woven argument and tagging which "
                       "source carries each point, then drafts by point. Faster summaries (B), rereading (C), or "
                       "a longer intro (D) do not build the woven argument. There is no clock here, so there is "
                       "time to plan.")),

        # ===== SUPPORTED: budget + fast plan (multi_paragraph) - the frame is the highest-value scaffold =====
        Slot("SUPPORTED", "production_frq", "Budget the stages and fast-plan the synthesis",
             ref="", bank="renewable_grid_synthesis", rubric_ref="rc.4trait", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Imagine a 40-minute window on the renewable-grid set. Set your budget and fast plan "
                       "before you draft a word of the synthesis.",
                 setapart_block=setapart("Fill in this plan:",
                                         "Budget: read ___ min, plan ___ min, draft ___ min, check ___ min. "
                                         "One argument the set builds: ______. Point 1: ______ (source that carries it: ______). "
                                         "Point 2: ______ (source: ______). Point 3: ______ (source: ______)."),
                 closer="Write the stage budget, then the fast plan: the one argument the set builds, plus your "
                        "ordered points each tagged with the source that carries it. This budget and plan is "
                        "what you will build the full synthesis from.")),
        # ===== INDEPENDENT: build the whole synthesis from the plan (essay ceiling) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Rehearse the full synthesis",
             ref="", bank="renewable_grid_synthesis", rubric_ref="rc.4trait", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now, run the whole routine and build the synthesis from your budget and plan.",
                 closer="Write a complete synthesis on the renewable-grid set: weave ONE argument from the "
                        "sources, weight each source by what it can carry, and cite each one you use. Then run "
                        "the woven-and-weighted check and fix any part that fails. There is no platform timer; "
                        "run your own budget. Rehearsing the whole routine end to end is what every real timed "
                        "synthesis is built on, and you are ready to do it cold. Take the time you need.")),

        # DIAGNOSIS = self-revision: reread your OWN just-written synthesis and run the check on it. The two
        # substance lines (one argument, weighted sources) are fixed in the draft; the pacing/process line
        # cannot be fixed in a finished draft, so it reframes as a metacognitive adjustment for the NEXT write.
        # Same taught source (load balance). Self-contained: the checklist is the scaffold and the grader scores
        # the diagnosis within the item.
        Slot("MODEL", "diagnosis_frq", "Check your own synthesis: woven and weighted?",
             ref="", bank="renewable_grid_synthesis", scored=True,
             body=frq_prompt(
                 intro="Reread the synthesis you just wrote and run this check on YOUR draft.",
                 checklist_block=checklist(title="Check your own draft, line by line:", rows=[
                     ("Did planning and checking get protected minutes, or did the window go entirely to reading and drafting?", "If they got squeezed out, that is a process fix: on your NEXT synthesis, split the window into read, plan, draft, and check first, and protect the plan and check minutes."),
                     ("Does your draft build ONE argument the whole set supports, not a summary of each source in turn?", "If it walks through the sources one at a time, name one argument (such as whether the grid can go mostly renewable and on what condition) and rebuild the draft around it."),
                     ("Is each source pulled in at the point it best carries?", "If a source just sits in its own equal paragraph, tag each point with the source that best supports it and weave that source in where it carries the most weight."),
                 ]),
                 closer="Fix the two substance lines (one argument, and each source weighted to the point it "
                        "carries) in your draft now. The timing line cannot be fixed in a finished draft, so use "
                        "it to adjust how you budget your NEXT synthesis. Finish by naming the one argument your "
                        "synthesis builds.")),
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
