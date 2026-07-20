"""
lesson_g9_l23_full_argument_essay_v3_1.py  -  G9 KC C.9.04, ESSAY-ASSEMBLY (BUILD, ceiling essay). V3.1.

G9 L23, rebuilt to the v3.1 build spec (hand-authored). Teaching point (KEPT): plan AND write a complete
single-source ARGUMENT essay - a single-paragraph outline (thesis + ordered body points), an intro that frames
the thesis, body paragraphs (claim + evidence + warrant, linked), and a conclusion that lands the upshot.
KC C.9.04. This is a FULL-ESSAY lesson; it recycles the whole G9 stack and reaches the essay ceiling.

Preserved EXACTLY from the current L23: id="ACC-W910-L-G9-C904-0023", lesson_type=7, mnemonic_status="proposal",
the bound stimuli (COMMUNITYSERVICE taught -> PHONEBAN transfer), and every production_frq unit= value
(SUPPORTED plan = multi_paragraph, INDEPENDENT + TRANSFER = essay). The unit ladder still climbs to the essay,
which is the type-7 ceiling.

V3.1 changes vs the current L23 (both were the only two failing gates + the spine polish):
  1. FIXED the leaked internal label: the discrimination no longer says "a Grade-C design bet we label as a
     bet"; it is a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}] (leaked_internal_label).
  2. FIXED the two wall-of-text teach cards: the two prose blocks are now a ONE_IDEA callout + real <ul>/<ol>
     lists of the parts and the order of work (format_fidelity, and the v3.1 "parallel items as a list" rule).
  3. Deterministic FRQ + diagnosis prompts via frq_prompt/setapart/checklist (no "Step 1/2" prose, no
     "Scored on ..." chrome); coping-model before/after kept; check tool (the 4-point reread) folded in at the
     point of first use as a real <ol> REMEMBER box.
Own words, no fabricated figures, no em dashes. Passes all 23 lesson_contract gates + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist, outline_table

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A strong argument essay is a <strong>PLAN, built '
'out</strong>: a thesis, body paragraphs that each prove a point, and a conclusion that lands the upshot. You '
'draft from the plan; you do not start at the top and hope.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: reread the essay</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, reread the whole essay and ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does every paragraph defend the thesis?</li>'
'<li style="margin:2px 0">Is each body paragraph a complete claim, evidence, and warrant?</li>'
'<li style="margin:2px 0">Do the paragraphs build and link at the seams?</li>'
'<li style="margin:2px 0">Does the conclusion add an upshot instead of repeating the thesis?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you submit.</div></div>')

# coping-model before/after: an unplanned draft (no side, dropped fact, repeated ending) rebuilt into planned,
# built sentences. Contains BOTH a literal BEFORE and AFTER (content_depth). Short structural sketch, not a
# whole essay - the point is the plan-then-build contrast, not a full draft.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> no side, a dropped fact, a repeated ending</span>'
    '<p style="margin:8px 0 0;font-size:15px"><i>Thesis:</i> Community service is a thing a lot of schools have, '
    'and it can be good or bad for students. <i>Body:</i> 83 percent. Service is nice and it teaches students '
    'stuff they need. <i>Conclusion:</i> So community service is a thing a lot of schools have, and it can be '
    'good or bad.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The thesis picks no side, the body drops a number '
    'with no source and no point, and the conclusion just repeats the thesis. Nothing is built.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> rebuilt as real sentences that take a side and build</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">THESIS</span> "Schools should make community service a graduation requirement, because '
      'a rule turns giving back from a lucky habit into something every student gets to do." '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">CLAIM + EVIDENCE + WARRANT (body)</span> "Service is already part of school life. The '
      'National Center for Education Statistics found that 83 percent of high schools had students doing '
      'community service, so a requirement would mostly formalize a habit students already share rather than '
      'force a brand new task." '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">CONCLUSION (upshot)</span> "If service is already this common, a rule would mainly '
      'reach the students who never get the push to start, so every graduate would leave having given back at '
      'least once."</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same topic, but now the thesis takes a side, the '
    'body is a claim with an attributed fact and a warrant tying them together, and the conclusion adds an '
    'upshot instead of repeating. Every part is built from the plan.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C904-0023", grade="9-10", lesson_type=7,
    unit="G9 U4 - Build essay (full argument essay)",
    title="Write a Full Argument Essay From Your Plan",
    target=("Plan and write a complete single-source argument essay: a multiple-paragraph outline, an intro "
            "that frames the thesis, ordered body paragraphs (claim + evidence + warrant, linked), and a "
            "conclusion that lands the upshot. Written at the essay. Trait: Development/Organization/Purpose."),
    acc_tags=["ACC.W.PROD.1", "ACC.W.ARG.5", "CCSS.W.9-10.1", "CCSS.W.9-10.4"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.9.04", "sot": "icm course-G9.md L23",
                "taught_stimulus": "ACC-W910-ARG-LESSON-COMMUNITYSERVICE",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-PHONEBAN",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": "v3.1 spine; ESSAY-TIER binds full sources; UNTIMED (no Timeback timer).",
                "one_idea": "A strong argument essay is a plan, built out (thesis, body, conclusion).",
                "one_reminder": "Reread check: every paragraph defends the thesis? each is claim+evidence+warrant? build+link? upshot?",
                "version_note": ("V3.1 rebuild of L23. FIXED the two failing gates on the prior version: removed "
                                 "the leaked internal label ('a Grade-C design bet we label as a bet') from the "
                                 "discrimination and moved it to explicit choices=[]; broke the two wall-of-text "
                                 "teach cards into a ONE_IDEA callout + real <ul>/<ol> lists (format_fidelity). "
                                 "Deterministic frq_prompt/setapart/checklist bodies (no 'Step 1/2' prose, no "
                                 "'Scored on' chrome); check tool folded in at first use. Preserved id, type 7, "
                                 "mnemonic_status=proposal, bound stimuli, and every production_frq unit= value "
                                 "(SUPPORTED=multi_paragraph, INDEPENDENT/TRANSFER=essay); ladder climbs to essay."),
                "review_provenance": "built to the L01/L12 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["plan-then-draft-full-essay", "assemble-the-g9-stack"],
    slots=[
        # ===== TEACH: the one idea + the parts (as a list), then the order of work (as a list) =====
        Slot("TEACH", "teach_card", "The one idea: an essay is a plan, built out",
             body=(ONE_IDEA +
                   "You have practiced every one of these moves on its own. A full essay puts them together, in "
                   "order:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Plan first, at two levels</strong>: a single-paragraph "
                   "outline is a plan for ONE paragraph, which you already know. An essay is bigger, so it needs "
                   "a bigger plan, the multiple-paragraph outline: one governing thesis on top, then ordered body "
                   "paragraphs under it (each pairing a point with the evidence it will use), framed by an "
                   "introduction and a conclusion. Write the thesis, then lay out the body paragraphs in order "
                   "before you draft.</li>"
                   "<li style=\"margin:4px 0\"><strong>Thesis</strong>: a thesis is a one-sentence claim that "
                   "takes a side, and your whole essay defends it.</li>"
                   "<li style=\"margin:4px 0\"><strong>Body</strong>: one paragraph per planned point, each a "
                   "claim, an attributed fact, and a warrant. A warrant is a sentence that explains why that "
                   "evidence supports the claim.</li>"
                   "<li style=\"margin:4px 0\"><strong>Conclusion</strong>: land the upshot instead of repeating "
                   "the thesis.</li></ul>"
                   "The trap is drafting with no plan, which makes essays drift and repeat. Plan first, then "
                   "build.")),
        Slot("TEACH", "teach_card", "How to build it, part by part",
             body=("Here is the order of work. Follow it and the essay assembles itself from moves you already "
                   "own:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>PLAN</strong>: write the thesis and three ordered points, "
                   "each with the evidence it will use.</li>"
                   "<li style=\"margin:4px 0\"><strong>INTRO</strong>: orient the reader and state the thesis.</li>"
                   "<li style=\"margin:4px 0\"><strong>BODY</strong>: write each planned point as a full "
                   "paragraph (claim, attributed evidence, warrant), and open each paragraph after the first "
                   "with a transition linking it to the one before.</li>"
                   "<li style=\"margin:4px 0\"><strong>CONCLUSION</strong>: land the upshot.</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: reread against a short list, does every "
                   "paragraph defend the thesis, is each a complete claim, evidence, and warrant, do the "
                   "paragraphs build and link, does the conclusion add an upshot?</li></ol>"
                   "You are assembling moves you already own, in this order, into one essay.")),
        Slot("TEACH", "stimulus_display", "Read the source: required community service",
             ref="ACC-W910-ARG-LESSON-COMMUNITYSERVICE", bank="community_service",
             body=("Read this source about required community service. Because your job is to write a full "
                   "argument essay from it, read the whole thing and gather a position worth defending plus "
                   "several facts (with their sources) you can use as evidence across body paragraphs. The text "
                   "stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + check tool, then the check items =====
        Slot("MODEL", "annotated_before_after", "Watch a plan turn a wandering draft into a built essay",
             bank="community_service",
             body=("Here is the difference between drafting cold and building from a plan. Read the BEFORE, then "
                   "the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE writes with no plan and wanders: the thesis picks no side, the body drops a "
                   "number, the conclusion repeats. The AFTER plans a thesis and ordered points, then builds "
                   "each part from the plan. Plan first, then build, is the move." + REMEMBER +
                   "When you build your own, put the parts in this order, then run the check before you submit.")),
        Slot("MODEL", "discrimination", "Which draft was built from a plan?",
             ref="", labeled_grade_c=True, bank="community_service",
             body=("You have watched a plan turn a wandering draft into a built essay. Now spot the target: "
                   "which writer built the essay from a plan, and which did not? "
                   "(A) The writer first makes a short outline, a thesis plus three ordered points that each name their evidence, then drafts the intro, one paragraph per point, and a conclusion.  "
                   "(B) The writer opens a blank page and types whatever thoughts about community service come to mind, adding each new idea as it arrives and stopping only once the essay finally feels long enough to be done.  "
                   "(C) The writer starts with a big, impressive-sounding introduction and keeps adding paragraphs until the page looks full, planning nothing in advance.  "
                   "(D) The writer jots a list of every fact they know about community service, then writes one paragraph per fact in the order the facts were listed, never deciding a thesis. "
                   "Correct: A. It fixes a thesis and an order first, so every paragraph defends the thesis in a "
                   "building sequence; B and C pile on text with no thesis and no order, and D lists facts with no thesis, so all three drift and repeat."),
             choices=[
                 {"id": "A", "text": "The writer first makes a short outline, a thesis plus three ordered points that each name their evidence, then drafts the intro, one paragraph per point, and a conclusion.",
                  "correct": True,
                  "why": "Correct. This writer plans first, a thesis and an order, so every paragraph defends the thesis in a building sequence."},
                 {"id": "B", "text": "The writer opens a blank page and types whatever thoughts about community service come to mind, adding each new idea as it arrives and stopping only once the essay finally feels long enough to be done.",
                  "correct": False,
                  "why": "This is drafting with no plan. Ideas arrive in random order, so the essay drifts and repeats instead of building one case."},
                 {"id": "C", "text": "The writer starts with a big, impressive-sounding introduction and keeps adding paragraphs until the page looks full, planning nothing in advance.",
                  "correct": False,
                  "why": "A big introduction and more paragraphs are not a plan. With no thesis and no order set first, the essay still drifts and repeats."},
                 {"id": "D", "text": "The writer jots a list of every fact they know about community service, then writes one paragraph per fact in the order the facts were listed, never deciding a thesis.",
                  "correct": False,
                  "why": "A fact list is not a plan for an argument. Without a thesis, the paragraphs have nothing to defend, so the essay reports facts in list order instead of building one case."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this essay approach most need?",
             bank="community_service",
             body=("Diagnose before the reveal. A student says: 'I will just start writing about community "
                   "service and see where it goes; I write better without planning.' For a full argument "
                   "essay, which single change would most improve the result? "
                   "(A) make a single-paragraph outline first, a thesis plus ordered points with evidence, then "
                   "draft from it  "
                   "(B) write a much longer introduction that carefully explains the whole community service "
                   "topic up front  "
                   "(C) add several more body paragraphs at the very end so the finished essay turns out "
                   "noticeably longer  "
                   "(D) swap in bigger, more impressive vocabulary words throughout so the writing sounds "
                   "smarter and advanced"),
             feedback=("Correct: A. Drafting an argument essay with no plan is the most common cause of "
                       "essays that drift, repeat, and never clearly defend one thesis. The fix is to plan "
                       "first: a thesis and ordered points with evidence, then build each part from the plan. "
                       "A longer intro (B), extra paragraphs (C), or bigger words (D) do not give the essay "
                       "the thesis-and-order it needs.")),

        # ===== SUPPORTED: plan the essay (multi_paragraph) - the frame is the highest-value scaffold =====
        Slot("SUPPORTED", "production_frq", "Plan the essay: thesis and ordered points",
             ref="", bank="community_service", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Use the outline grid below so you can see the shape of the plan. Copy it into the box and "
                       "fill each blank to plan your argument essay on required community service before you write "
                       "a word of it.",
                 setapart_block=outline_table(title="Copy this outline, then fill in each blank:", rows=[
                     ("THESIS", "______ (your side)"),
                     ("POINT 1", ["claim: ______", "evidence: ______"]),
                     ("POINT 2", ["claim: ______", "evidence: ______"]),
                     ("POINT 3", ["claim: ______", "evidence: ______"]),
                 ]),
                 closer="Write a single-paragraph outline: a one-line thesis that takes a side, then three "
                        "ordered body points, each naming its claim and the source fact it will use. This plan "
                        "is what you will build the essay from.")),
        # ===== INDEPENDENT: build the whole essay from the plan (essay ceiling) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write the full argument essay",
             ref="", bank="community_service", rubric_ref="rc.staar", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now, build the whole essay from your plan.",
                 closer="Write a complete argument essay on required community service: an introduction that "
                        "frames the thesis, three body paragraphs (each a claim, attributed evidence, and a "
                        "warrant, ordered to build and linked), and a conclusion that lands the upshot. Then run "
                        "the reread check and fix any part that fails. Assembling the moves you own into one "
                        "essay is the real skill, and you are ready to do it. Take the time you need.")),

        # DIAGNOSIS = self-revision: reread your OWN just-written draft and run the same checklist on it, fixing
        # any line that fails. Same taught source (load balance). Scaffolded by the checklist itself.
        Slot("MODEL", "diagnosis_frq", "Check your draft defends the thesis",
             ref="", bank="community_service", scored=True,
             body=frq_prompt(
                 intro="Reread the essay you just wrote. Run this checklist on YOUR draft and fix any line that fails.",
                 checklist_block=checklist(title="Check your own draft, row by row:", rows=[
                     ("Does your thesis take a clear side?", "If it only rates the topic (like 'X is good'), sharpen it into a position someone could reject."),
                     ("Are your body points distinct and ordered?", "If they overlap or restate each other, make them distinct and put them in a building order."),
                     ("Is a source fact named for each point?", "If a point has no evidence behind it, attach one piece of evidence to it."),
                 ]),
                 closer="For every row that fails on your draft, fix it in the essay before you submit. Finish by "
                        "naming which part your essay still needs most.")),
        # Per the essay-grain verdict, in-article TRANSFER is routed to the gate/PP100 (a separate resource), so
        # the lesson ends at the INDEPENDENT write + its self-revision. The prior TRANSFER stimulus + write are
        # removed here; the PP100 mastery task remains a separate, held-out resource.
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
