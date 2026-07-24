"""
lesson_g12_l11_timed_synthesis.py  -  G12 KC C.12.02, ARCHETYPE T8: CROSS-SOURCE-SYNTHESIS (WEAVE, essay). V3.1.

G12 course L11 (Unit 2, build), rebuilt to the v3.1 build spec (hand-authored). Teaching point (KEPT): rehearse a
complete AP synthesis essay under a self-imposed budget, capping the reading and pacing the writing so a woven,
weighted, sophisticated synthesis is finished end to end, rather than reading out the clock and defaulting to a
source-by-source survey. Delivery UNTIMED (a transferable pacing strategy, not a platform timer). Written at the
essay. KC C.12.02.

Preserved EXACTLY from the prior L11: id="ACC-W910-L-G12-C1202-0011", lesson_type=8, mnemonic_status="proposal",
kc="C.12.02", unit, the bound stimuli (synth_ai_workforce SYNTH-SET-0002 taught -> synth_renewable_grid
SYNTH-SET-0001 transfer), and every production_frq unit= value (SUPPORTED plan = multi_paragraph, INDEPENDENT +
TRANSFER = essay). The unit ladder still climbs to the essay, which is the type-8 ceiling.

V3.1 changes vs the prior L11:
  1. FIXED the leaked internal label: the discrimination no longer says "a Grade-C design bet we label as a bet";
     it is a clean choose-the-target prompt with explicit choices=[{id,text,correct,why}] (leaked_internal_label).
  2. FIXED the wall-of-text teach card: the prose block is now a ONE_IDEA callout + real <ul>/<ol> lists of the
     parts of a synthesis and the order of work (format_fidelity, and the v3.1 "parallel items as a list" rule).
  3. Deterministic FRQ + diagnosis prompts via frq_prompt/setapart/checklist (no "Step 1/2" prose, no "Scored on"
     chrome); coping-model before/after kept with literal BEFORE and AFTER; the check tool (the 3-question pacing
     check) folded in at first use as a real <ol> REMEMBER box.
Own words, no fabricated figures (facts trace to the bound federal sources), no em dashes. Passes all 23
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
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A full synthesis is a <strong>PACED REHEARSAL</strong>: '
'cap the reading, plan the weave, and finish the whole essay. If you read every source to the bottom, you run out '
'of time to weave and the essay collapses into a survey.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: pace the synthesis</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you draft, look at your plan and ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Is the reading capped to a share of the window, not read to the bottom?</li>'
'<li style="margin:2px 0">Is there ONE woven argument with a source assigned to each point, not a plan to summarize each source in turn?</li>'
'<li style="margin:2px 0">Is drafting time reserved so the essay can reach a real conclusion?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix the plan before you draft.</div></div>')

# coping-model before/after: a read-out-the-clock approach (all four sources read to the bottom, no time left, a
# source-by-source survey) rebuilt into a capped-reading, weave-first plan. Contains BOTH a literal BEFORE and
# AFTER (content_depth). A structural sketch of the approach, not a full essay - the point is the pacing contrast.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> reads all four sources to the bottom, then runs out of time</span>'
    '<p style="margin:8px 0 0;font-size:15px"><i>Approach:</i> Read the BLS forecast, the NSF STEM count, the GAO '
    'evidence-limits source, and the Census chart, all the way through. <i>Plan:</i> none, there is no time left. '
    '<i>Draft:</i> "Source 1 says AI jobs grow fast. Source 2 says the STEM workforce is 24 percent of workers. '
    'Source 3 says the data are weak. Source 4 shows a chart." One paragraph per source, in the order they appear.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">Reading out the clock leaves no time to weave. The '
    'essay becomes a source tour with no single argument the set builds.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> caps the reading, plans the weave, finishes the synthesis</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">ARGUMENT</span> "AI is reshaping work, not erasing it, so the real problem is the gap '
      'between the workers it lifts and the workers it leaves behind." '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">WEAVE (source per point)</span> "The BLS forecast carries the point that demand is '
      'shifting toward technical work (data scientists up 33.5 percent), the NSF count carries the scale of who '
      'is already inside that work (24 percent of workers), and the GAO source qualifies both by warning the data '
      'cannot yet say who is displaced." '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">CONCLUSION</span> "Because the winners and losers of automation are rarely the same '
      'people, measuring the gap matters more than counting total jobs."</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same sources, but the reading was capped, one argument '
    'was planned, each source was assigned to a point, and the essay reaches a real conclusion. The synthesis is '
    'woven and finished.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G12-C1202-0011", grade="9-10", lesson_type=8,
    unit="G12 U2 - Sustain a full synthesis FRQ",
    title="Rehearse a Complete Synthesis, End to End",
    target=("Rehearse a complete synthesis essay under a self-imposed budget, capping reading and pacing the "
            "writing so a woven, weighted, nuanced synthesis is finished end to end, rather than reading "
            "out the clock and defaulting to a survey. Delivery untimed. Written at the essay. Trait: "
            "Development (synthesis), complexity, and process."),
    acc_tags=["ACC.W.SRC.1", "ACC.W.PROD.4", "CCSS.W.11-12.7", "CCSS.W.11-12.4"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.12.02", "sot": "icm course-G12.md L11",
                "taught_stimulus": "ACC-W910-SYNTH-SET-0002",
                "transfer_stimulus": "ACC-W910-SYNTH-SET-0001",
                "playbook": "_phase2/playbook_T8_WEAVE.md",
                "one_idea": "A full synthesis is a paced rehearsal: cap the reading, plan the weave, finish the whole essay.",
                "one_reminder": "Pace check: reading capped? one woven argument with a source per point? drafting time reserved for a conclusion?",
                "template": ("v3.1 spine; SYNTHESIS-TIER binds cold-to-G12 set; full SYNTHESIS FRQ rehearsal "
                             "under own budget; Timeback delivery UNTIMED."),
                "version_note": ("V3.1 rebuild of L11. FIXED the leaked internal label (removed 'a Grade-C design "
                                 "bet we label as a bet' from the discrimination, moved to explicit choices=[]); "
                                 "broke the wall-of-text teach card into a ONE_IDEA callout + real <ul>/<ol> lists "
                                 "(format_fidelity); deterministic frq_prompt/setapart/checklist bodies (no 'Step "
                                 "1/2' prose, no 'Scored on' chrome); coping-model before/after with literal "
                                 "BEFORE/AFTER kept; check tool folded in at first use as a REMEMBER <ol>. "
                                 "Preserved id, type 8, kc C.12.02, mnemonic_status=proposal, unit, bound stimuli, "
                                 "and every production_frq unit= value (SUPPORTED=multi_paragraph, "
                                 "INDEPENDENT/TRANSFER=essay); ladder climbs to essay."),
                "review_provenance": "built to the G9 L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["full-synthesis-rehearsal", "cap-reading-plan-the-weave"],
    slots=[
        # ===== TEACH: the one idea + the parts (as a list), then the order of work (as a list) =====
        Slot("TEACH", "teach_card", "The one idea: a synthesis is a paced rehearsal",
             body=(ONE_IDEA +
                   "You already know how to weave sources. A full synthesis writing task puts that under a budget. To "
                   "synthesize means to combine several sources into one argument the set builds, rather than "
                   "reporting each source on its own. A finished synthesis has these parts:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>One argument</strong>: a single position the whole set of "
                   "sources builds toward, not one claim per source.</li>"
                   "<li style=\"margin:4px 0\"><strong>A weave</strong>: a weave is when each point is carried by "
                   "the one source that supports it best, and the sources are woven together instead of listed in "
                   "turn.</li>"
                   "<li style=\"margin:4px 0\"><strong>Weighting</strong>: some sources count for more, so you "
                   "lean on the strongest and treat weaker or qualifying ones as limits.</li>"
                   "<li style=\"margin:4px 0\"><strong>A real conclusion</strong>: an ending that lands the "
                   "upshot of the whole argument, not a restatement.</li></ul>"
                   "The trap is reading every source to the bottom and having no time left to weave, so the essay "
                   "turns into a survey. Cap the reading, then build.")),
        Slot("TEACH", "teach_card", "How to pace it, part by part",
             body=("Here is the order of work under a budget. Follow it and the synthesis stays woven and "
                   "finishes on time:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>CAP THE READING</strong>: read only enough to find the one "
                   "argument the set builds and which source carries each point, then stop reading.</li>"
                   "<li style=\"margin:4px 0\"><strong>FAST-PLAN THE WEAVE</strong>: write the one argument and "
                   "assign a source to each point (not a plan to summarize each source in turn).</li>"
                   "<li style=\"margin:4px 0\"><strong>DRAFT</strong>: write the whole synthesis, woven and "
                   "weighted, citing each source as you use it.</li>"
                   "<li style=\"margin:4px 0\"><strong>LAND IT</strong>: reserve time to reach a real conclusion "
                   "that states the upshot.</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: confirm it is one woven argument and it is "
                   "finished, not a survey cut off in the middle.</li></ol>"
                   "Delivery here has no clock. The budget is your own discipline, and it transfers to any timed "
                   "synthesis later.")),
        Slot("TEACH", "stimulus_display", "Read the source set: AI and the workforce",
             ref="ACC-W910-SYNTH-SET-0002", bank="ai_workforce_synthesis",
             body=("Read this source set on how artificial intelligence will reshape the American workforce. "
                   "Picture a full writing task: cap the reading to find the one argument the set builds and which source "
                   "carries each point, then plan the whole synthesis. Do not read out the clock. The texts stay "
                   "on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + check tool, then the check items =====
        Slot("MODEL", "annotated_before_after", "Watch a read-out-the-clock approach become a paced synthesis",
             bank="ai_workforce_synthesis",
             body=("Here is the difference between reading out the clock and pacing the synthesis. Read the "
                   "BEFORE, then the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE reads all four sources to the bottom and has no time to weave, so it surveys each "
                   "source in turn. The AFTER caps the reading, plans one argument with a source per point, and "
                   "finishes with a conclusion. Cap the reading, plan the weave, finish, is the move." + REMEMBER +
                   "When you plan your own, run this check before you draft.")),
        Slot("MODEL", "discrimination", "Which rehearsal finishes a woven synthesis?",
             ref="", labeled_grade_c=True, bank="ai_workforce_synthesis",
             body=("You have watched a paced rehearsal beat a read-out-the-clock one. Now choose the target: "
                   "which approach finishes a woven synthesis, and which leaves no time to weave? "
                   "(A) The writer reads all four sources to the very bottom, jots the main point of each, then, "
                   "low on time, writes one paragraph summarizing each source in turn, in the order they appear.  "
                   "(B) The writer caps the reading once the one argument is clear, assigns each point to the "
                   "source that carries it best, then drafts the whole woven synthesis and reserves time to close.  "
                   "(C) The writer reads all four sources to the very bottom, decides the one that seemed most "
                   "interesting is surely right, and spends the little time left defending that single source alone.  "
                   "(D) The writer caps the reading quickly, then spends most of the remaining time building a long, "
                   "detailed plan, and starts drafting so late that the synthesis stops partway and never reaches a "
                   "conclusion.  "
                   "Correct: B finishes a woven synthesis; A and C read out the clock, and D over-plans, so all "
                   "three leave the set unwoven or the essay unfinished."),
             choices=[
                 {"id": "A", "text": "The writer reads all four sources to the very bottom, jots the main point of each, then, low on time, writes one paragraph summarizing each source in turn, in the order the sources happen to appear.",
                  "correct": False,
                  "why": "This reads out the clock. With no time left to weave, the essay becomes a survey, one paragraph per source, not one argument the set builds."},
                 {"id": "B", "text": "The writer caps the reading once the one argument is clear, assigns each point to the source that carries it best, then drafts the whole woven synthesis and reserves time to close.",
                  "correct": True,
                  "why": "Correct. Capping the reading leaves time to weave one argument, assign a source to each point, and reach a real conclusion. The synthesis finishes."},
                 {"id": "C", "text": "The writer reads all four sources to the very bottom, decides the one source that seemed most interesting is right, and spends the little time left defending that single source on its own.",
                  "correct": False,
                  "why": "This also reads out the clock, and leaning on one source is not a synthesis. The set is never woven into a single argument."},
                 {"id": "D", "text": "The writer caps the reading quickly, then spends most of the remaining time building a long, detailed plan, and starts drafting so late that the synthesis stops partway and never reaches a conclusion.",
                  "correct": False,
                  "why": "Capping the reading was right, but over-planning burns the drafting time. A synthesis that stops before its conclusion is unfinished, so the weave never lands its upshot."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this synthesis rehearsal most need?",
             bank="ai_workforce_synthesis",
             body=("Diagnose before the reveal. A student reads all four sources on AI and the workforce "
                   "thoroughly and then, out of time, writes a source-by-source summary. For a full synthesis "
                   "writing task, which single change would most improve the result? "
                   "(A) cap the reading and move to planning the weave once the one argument and the source for "
                   "each point are clear  "
                   "(B) read each of the four sources a second time so every figure and detail is fully "
                   "understood before any writing begins at all  "
                   "(C) summarize each of the four sources a little faster so that all four still fit inside the "
                   "small amount of time that remains  "
                   "(D) bring in a fifth outside source so the finished synthesis can cover even more points and "
                   "viewpoints than the four provided"),
             feedback=("Correct: A. Reading out the clock is what forces the survey, so the fix is to cap the "
                       "reading and get to planning one woven argument with a source per point. A second read "
                       "(B), faster summaries (C), or an extra source (D) all leave even less time to weave.")),

        # ===== SUPPORTED: plan the synthesis (multi_paragraph) - the frame is the highest-value scaffold =====
        Slot("SUPPORTED", "production_frq", "Budget the reading and plan the weave",
             ref="", bank="ai_workforce_synthesis", rubric_ref="rc.4trait", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Plan your synthesis on the AI-workforce set before you draft, so the reading is capped "
                       "and there is time to weave.",
                 setapart_block=setapart("Fill in this plan:",
                                         "Reading cap: ______ (a share of your window). One argument the set builds: ______. Point 1 + the source that carries it: ______. Point 2 + its source: ______. Point 3 + its source: ______."),
                 closer="Write your reading cap, the one argument the set builds, and three points, each assigned "
                        "to the single source that carries it best (not a plan to summarize each source). This "
                        "plan is what you will draft the synthesis from.")),
        # ===== INDEPENDENT: rehearse the whole synthesis from the plan (essay ceiling) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Rehearse the full synthesis",
             ref="", bank="ai_workforce_synthesis", rubric_ref="rc.4trait", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now. Using your budget and plan, rehearse the complete synthesis end to end.",
                 closer="Write a complete synthesis essay on the AI-workforce set: a situated, woven, weighted "
                        "argument that assigns each point to the source that carries it, citing each source you "
                        "use, and a real conclusion that lands the upshot. Run your own reading cap; there is no "
                        "platform timer. Then confirm it is one woven argument, not a survey, and that it is "
                        "finished. Pacing a whole synthesis end to end is what every real synthesis writing task is built "
                        "on, and you are ready to do it cold. Take the time you need.")),

        # COUNCIL FIX (2026-07-24): Option A (later-in-arc). Was a bundle: mark a 3-question pacing check (as
        # pre-answered (q,a) tuple rows) + revise the draft + name the argument, all in one graded box (the (q,a)
        # rows leaked answers and could not be scored). Now ONE graded act (revise your own synthesis essay); the
        # checks print READ-ONLY beneath as plain strings; the reading-cap process line moved into the intro (it is
        # a next-time note, not a fix to this draft); the "name the one argument" tail is dropped. unit/frq_type/
        # rubric_ref added to declare the essay grain. NOTE: structurally near-identical to L09/L10 (self-revision
        # on the own just-written essay); treated as Option A per the arc classification (rewrite_plus_name).
        Slot("MODEL", "diagnosis_frq", "Revise your synthesis: one woven argument, a real conclusion",
             ref="", bank="ai_workforce_synthesis", rubric_ref="rc.4trait", scored=True, unit="essay", frq_type="writing",
             body=frq_prompt(
                 intro="Reread the synthesis essay you just wrote on the AI-workforce set, then revise it. If your "
                       "reading ate most of the window and left little time to weave, note that for your next write, "
                       "and repair the draft you have now.",
                 checklist_block=checklist(title="Make your revision pass these (no need to type answers):", rows=[
                     "Is there ONE woven argument, with a source assigned to each point (not a source-by-source survey)?",
                     "Does the essay reach a real conclusion that lands the upshot, not stop mid-thought or restate the claim?",
                 ]),
                 closer="Revise the draft so it reads as one woven, weighted argument that assigns each point to the "
                        "source that carries it, and add a conclusion that states what the whole argument adds up "
                        "to. Check your revision against the two points above before you submit.")),
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
