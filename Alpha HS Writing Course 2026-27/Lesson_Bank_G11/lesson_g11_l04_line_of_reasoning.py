"""
lesson_g11_l04_line_of_reasoning.py  -  G11 KC C.11.01, ARCHETYPE T3 (PROVE, paragraph). V3.1.

G11 course L04 (Unit 1, intro), rebuilt to the v3.1 build spec. Teaching point (kept): a strong argument is a
LINE OF REASONING, a chain where each reason leads to the next toward the claim, not a pile of unconnected
points. KC C.11.01. lesson_type=3, mnemonic_status=established-caveat. EVIDENCE-TIER binds the full sources:
infrastructure_spending (grid investment, taught) -> ai_workforce_policy (transfer, partitioned). rc.ap register.
V3.1 spine: ONE_IDEA teal callout + list teach, coping-model think-aloud with literal BEFORE/AFTER, REMEMBER
3-question check, explicit-choices discrimination, deterministic FRQ prompts. No coping-model persona (stateless),
no source markup, no prior-work ref, no em dashes. 23 gates.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A line of reasoning is a chain of reasons where each '
'one leads to the next until the claim follows. A pile of separate true points sitting side by side is not the '
'same thing, and it is weaker, because the reader has to build the argument for you.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: line, or list?</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, run your reasons through three questions:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0"><strong>Connected?</strong> Does each reason lead into the next with a link word like '
'so, therefore, or which means?</li>'
'<li style="margin:2px 0"><strong>One direction?</strong> Does the chain build one way, each step using the one '
'before it?</li>'
'<li style="margin:2px 0"><strong>Arrives?</strong> Does the last step actually reach the claim?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">Answer no to any of these and you have a list, not a line.</div></div>')

COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer turning a pile of reasons into a line, one pass at a time:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Fund the grid first. Wind and solar are cheap now. '
    'Storage already exists. Renewables are about a fifth of our power and rising." Four true points, all about '
    'the same topic.</p>'
    '<p style="margin:0 0 8px"><strong>Run the check:</strong> Does each reason lead into the next? No. They just '
    'sit next to each other. A reader still has to figure out how "wind is cheap" gets me to "fund the grid." So '
    'the points are true but they do not build.</p>'
    '<p style="margin:0"><strong>Final:</strong> "Wind and solar are now cheap and fast to add, so the limit is '
    'no longer making power but moving it, and therefore the next dollar should go to the grid that carries it." '
    'Now each step uses the one before, and the last step reaches the claim.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> Four reasons listed side by side: true, but unconnected, so the '
    'reader must assemble the argument.</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> The same reasons chained with "so" and "therefore" so each step '
    'leads to the next and the last one lands on the claim.</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1101-0004", grade="9-10", lesson_type=3,
    unit="G11 U1 - Nuance (line of reasoning)",
    title="Build a Line of Reasoning, Not a List",
    target=("Chain reasons so each builds on the one before toward the claim (a line of reasoning), rather "
            "than stacking unconnected points. Written at the paragraph. Trait: Evidence and Commentary "
            "(line of reasoning)."),
    acc_tags=["ACC.W.ARG.2", "CCSS.W.11-12.1"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "established-caveat", "kc": "C.11.01", "sot": "icm course-G11.md L04",
                "taught_stimulus": "ACC-W910-ARG-LESSON-GRIDSPENDING",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-AIWORKFORCE",
                "playbook": "_phase2/playbook_T3_PROVE.md",
                "template": "locked L01 template; EVIDENCE-TIER binds full sources. G11 register.",
                "one_idea": "A line of reasoning is a chain where each reason leads to the next toward the claim.",
                "one_reminder": "Check: connected? one direction? does the last step reach the claim?",
                "version_note": ("V3.1 rebuild of a pre-v3.1 prose-wall lesson. Adopts the G9 L12 v3.1 T3 pattern: "
                                 "ONE_IDEA teal callout + list teach, coping-model think-aloud (First try -> check "
                                 "-> Final) with literal BEFORE/AFTER, REMEMBER 3-question check, explicit-choices "
                                 "discrimination (no leaked Grade-C label), deterministic FRQ prompts. Kept id, KC, "
                                 "unit, teaching point, bound stimuli. Paragraph-level with a sentence warm-up."),
                "council": ("T3 G11 line-of-reasoning intro: introduces the line of reasoning (reasons build on "
                            "each other toward the claim). line-vs-list discrimination is a labeled design bet in "
                            "code (labeled_grade_c=True), never surfaced to the student. PROVE=established-caveat.")},
    fade_ledger_moves=["line-of-reasoning", "each-reason-advances-the-argument"],
    slots=[
        Slot("TEACH", "teach_card", "The one idea: a line, not a list",
             body=(ONE_IDEA +
                   "You have gathered reasons before. At this level, how you ORDER them is the move. Compare the "
                   "two shapes an argument can take:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>A list</strong>: several true points set side by side. Each "
                   "may be correct, but none leads to the next, so the reader has to connect them.</li>"
                   "<li style=\"margin:4px 0\"><strong>A line of reasoning</strong>: reasons chained so step one "
                   "sets up step two (\"so ...\"), which sets up step three (\"therefore ...\"), until the claim "
                   "follows on its own.</li></ul>"
                   "The link words (so, therefore, which means, as a result) are what show the chain. Goal today: "
                   "chain your reasons so each one advances the argument toward the claim.")),
        Slot("TEACH", "stimulus_display", "The source: build capacity or fix the grid first",
             ref="ACC-W910-ARG-LESSON-GRIDSPENDING", bank="infrastructure_spending",
             body=("Read this source on energy-spending priorities. Because your job is to build a LINE of "
                   "reasoning, read the whole thing and gather reasons that can be ordered so each leads to the "
                   "next. The text stays on screen while you work.")),
        Slot("MODEL", "annotated_before_after", "Watch a pile of reasons become a line",
             bank="infrastructure_spending",
             body=("Here is the move in action. Follow the writer turn a list into a line, one pass at a time. " +
                   COPING_HTML +
                   " Notice the difference: the first try lists true reasons that never connect; the final version "
                   "chains them so each step leads to the next and the last reaches the claim." + REMEMBER +
                   "When you build your own, order the reasons into a chain, then run the check.")),
        Slot("MODEL", "discrimination", "Which one is a line of reasoning, not a list?",
             ref="", labeled_grade_c=True, bank="infrastructure_spending",
             body=("Spot the target before you build it. Which option is a line of reasoning, where each step "
                   "leads to the next toward the claim (fund the grid first)? "
                   "(A) The grid should come first. Wind power is cheap now. Battery storage already exists in many places. Big cities use huge amounts of power, so demand keeps rising.  "
                   "(B) New wind and solar are cheap to add, so the real limit is now moving that power, and therefore energy money should go first to the grid, not new generation.  "
                   "(C) The grid should come first. Solar is popular with voters. Coal use is falling steadily. Nuclear plants still run. New capacity is being built across many states.  "
                   "(D) Wind and solar are cheap to add, so the country can build more of them, and therefore new clean power keeps getting easier to install. "
                   "Correct: B."),
             choices=[
                 {"id": "A", "text": "The grid should come first. Wind power is cheap now. Battery storage already exists in many places. Big cities use huge amounts of power, so demand keeps rising.",
                  "correct": False,
                  "why": "These are true points about the same topic, and one even uses 'so,' but they sit side by side and none leads into the next. It is a list, not a chain, so the reader has to build the argument."},
                 {"id": "B", "text": "New wind and solar are cheap to add, so the real limit is now moving that power, and therefore energy money should go first to the grid, not new generation.",
                  "correct": True,
                  "why": "Correct. Each step uses the one before: cheap-to-add ('so') means the limit shifts to delivery, ('therefore') which is why the money should go to the grid. The chain builds in one direction and the last step reaches the claim."},
                 {"id": "C", "text": "The grid should come first. Solar is popular with voters. Coal use is falling steadily. Nuclear plants still run. New capacity is being built across many states.",
                  "correct": False,
                  "why": "Five separate facts stacked behind the claim. They point in different directions and none leads to the next, so it is a pile of reasons, not a line."},
                 {"id": "D", "text": "Wind and solar are cheap to add, so the country can build more of them, and therefore new clean power keeps getting easier to install.",
                  "correct": False,
                  "why": "This one does chain with 'so' and 'therefore,' but it heads the wrong way: it ends on building more generation, so it never arrives at the claim that the money should go to the grid. A line has to land on the claim, not drift off it."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this reason-pile most need?",
             bank="infrastructure_spending",
             body=("Diagnose before the reveal. A draft reads: 'Fund the grid. Solar is growing. Batteries are "
                   "improving. Power demand is rising. So the grid matters.' Which single move would most improve "
                   "it? "
                   "(A) chain the reasons so each one leads to the next and the last reaches the claim  "
                   "(B) add a fifth separate reason so even more true points stack up behind the claim at the end  "
                   "(C) rewrite each reason as a longer, more formal sentence so the whole paragraph sounds polished  "
                   "(D) move the claim to the front so the reader meets the main point before reading any reasons"),
             feedback=("Correct: A. The reasons are true but unconnected, so the draft is a list. The fix chains "
                       "them: growing solar and better batteries mean generation is no longer the limit, so rising "
                       "demand will strain delivery, therefore fund the grid. A fifth reason (B), longer sentences "
                       "(C), or reordering (D) do not connect the reasons into a line.")),
        Slot("SUPPORTED", "production_frq", "Warm up: chain just two reasons",
             ref="", bank="infrastructure_spending", rubric_ref="rc.ap", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Warm up the move with a single link. Here is a claim and two loose reasons about the grid:",
                 setapart_block=setapart("Claim + two loose reasons:",
                                         "Claim: energy money should go first to the grid. Reason 1: wind and solar are cheap and fast to add. Reason 2: variable power still has to travel from where it is made to where it is used."),
                 closer="Write ONE sentence that chains the two reasons with a link word (so, therefore, which "
                        "means) so the first leads into the second and the second points at the claim. Then check "
                        "the link actually connects them.")),
        Slot("MODEL", "diagnosis_frq", "Check a draft: line, or list?",
             ref="", bank="infrastructure_spending", scored=True,
             body=frq_prompt(
                 intro="Run the line-or-list check on this weak draft, then rebuild it as a chain.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "Fund the grid first. Wind is cheap. Storage helps. Renewables are rising.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Connected: does each reason lead into the next?", "No. Four points sit side by side with no link words. Chain them."),
                     ("One direction: does the chain build one way?", "No. They are parallel, not building. Make each step use the one before."),
                     ("Arrives: does the last step reach the claim?", "No. It jumps to 'fund the grid' without getting there. End the chain on the claim."),
                 ]),
                 closer="Now rewrite it as a two- or three-step line of reasoning for the grid claim, each step "
                        "leading to the next. Then name the link word you used to connect the steps.")),
        Slot("INDEPENDENT", "production_frq", "Build a line of reasoning on your own",
             ref="", bank="infrastructure_spending", rubric_ref="rc.ap", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="On your own now. For a claim about energy-spending priorities, build a short paragraph "
                       "that is a LINE of reasoning, not a list.",
                 closer="Write two or three reasons chained so each builds on the last and the chain arrives at "
                        "the claim. This is what every real argument at this level is built on, and you are ready "
                        "to do it cold. Run the line-or-list check before you submit, and do not write a list.")),
        Slot("TRANSFER", "stimulus_display", "A NEW source: government and the AI workforce",
             ref="ACC-W910-ARG-LESSON-AIWORKFORCE", bank="ai_workforce_policy",
             body=("A new source on whether the government should steer workers toward growing technology fields. "
                   "Read the whole thing and gather reasons that can be ordered so each leads to the next. Same "
                   "build-a-line move, new topic. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Build a line of reasoning on a NEW topic",
             ref="", bank="ai_workforce_policy", rubric_ref="rc.ap", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="New topic. For a claim about the government's role in the AI workforce, build a short "
                       "paragraph that is a line of reasoning.",
                 closer="Chain two or three reasons so each builds on the last toward the claim. Same move as the "
                        "energy paragraph, new material. Run the line-or-list check before you submit, and do not "
                        "write a list.")),
    ],
)

LESSONS = [LESSON]

if __name__ == "__main__":
    ok = True
    for L in LESSONS:
        qc_lesson(L); print(qc_report(L)); print(); ok = ok and L.qc["passed"]
    print(f"{sum(1 for L in LESSONS if L.qc['passed'])}/{len(LESSONS)} PASS")
    sys.exit(0 if ok else 1)
