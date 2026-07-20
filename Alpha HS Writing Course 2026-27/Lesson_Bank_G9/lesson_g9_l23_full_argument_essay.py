"""
lesson_g9_l23_full_argument_essay.py  -  G9 KC C.9.04, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD, ceiling essay).

G9 course L23 (Unit 4, build). Plan and write a full single-source ARGUMENT essay: SPO plan -> intro that
frames the thesis -> ordered body paragraphs (claim+evidence+warrant, cohered, linked) -> conclusion that
lands the upshot. Recycles the entire G9 stack; reaches the essay ceiling (unit="essay"). Locked L01 template.
ESSAY-TIER binds the FULL source. Taught: COMMUNITYSERVICE (full) -> transfer: PHONEBAN (full, partitioned).
rc.staar. BUILD=proposal. UNTIMED (Timeback has no timer). No coping-model persona; no source markup; no
prior-work ref; no em dashes. Runs QC on execution.
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
    target=("Plan and write a complete single-source argument essay: SPO plan, an intro that frames the "
            "thesis, ordered body paragraphs (claim + evidence + warrant, linked), and a conclusion that lands "
            "the upshot. Written at the essay. Trait: Development/Organization/Purpose."),
    acc_tags=["ACC.W.PROD.1", "ACC.W.ARG.5", "CCSS.W.9-10.1", "CCSS.W.9-10.4"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12",
                "mnemonic_status": "proposal", "kc": "C.9.04", "sot": "icm course-G9.md L23",
                "taught_stimulus": "ACC-W910-ARG-LESSON-COMMUNITYSERVICE",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-PHONEBAN",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": "locked L01 template; ESSAY-TIER binds full sources; UNTIMED (no Timeback timer).",
                "council": ("T7/BUILD full-argument-essay build: plan-first-then-draft, assembling the entire "
                            "G9 stack into one essay. planned-vs-unplanned discrimination labeled Grade-C. "
                            "BUILD=proposal; unit=essay (T7 ceiling). Untimed.")},
    fade_ledger_moves=["plan-then-draft-full-essay", "assemble-the-g9-stack"],
    slots=[
        Slot("TEACH", "teach_card", "An essay is the plan, built out",
             body=("This is where the pieces come together. A strong argument essay is not written by starting "
                   "at the top and hoping; it is a PLAN, built out. First you make a single-paragraph outline: "
                   "a one-line thesis that takes a side, plus ordered body points that each name evidence. Then "
                   "you draft from it: an introduction that frames the thesis, one body paragraph per planned "
                   "point (each a claim, attributed evidence, and a warrant, connected). A warrant is a "
                   "sentence that explains why the evidence supports the claim. The paragraphs are ordered "
                   "so they build and linked at the seams, and a conclusion lands the upshot instead of "
                   "repeating the thesis. Every move you have practiced has a place here. The trap is drafting "
                   "with no plan, which makes essays drift and repeat. Goal today: plan an argument essay, then "
                   "build the whole thing from the plan.")),
        Slot("TEACH", "teach_card", "How to build it, part by part",
             body=("Here is the order of work. One, PLAN: write the thesis and three ordered points with "
                   "evidence. Two, INTRO: orient the reader and state the thesis. Three, BODY: write each "
                   "planned point as a full paragraph (claim, attributed evidence, warrant), and open each "
                   "after the first with a transition linking it to the one before. Four, CONCLUSION: land the "
                   "upshot. Five, CHECK: reread against a short list, does every paragraph defend the thesis, "
                   "is each a complete claim-evidence-warrant, do the paragraphs build and link, does the "
                   "conclusion add an upshot? You are assembling moves you already own, in this order, into one "
                   "essay.")),
        Slot("TEACH", "stimulus_display", "Read the source: required community service",
             ref="ACC-W910-ARG-LESSON-COMMUNITYSERVICE", bank="community_service",
             body=("Read this source about required community service. Because your job is to write a full "
                   "argument essay from it, read the whole thing and gather a thesis-worthy position plus "
                   "several facts (with sources) you can use as evidence across body paragraphs. The text "
                   "stays on screen while you work.")),
        Slot("TEACH", "discrimination", "Which draft was built from a plan?",
             ref="", labeled_grade_c=True, bank="community_service",
             body=("Sort before you build (spotting the target first, a Grade-C design bet we label as a bet, "
                   "not a proven ingredient). Which essay approach was PLANNED, and which was not? "
                   "(A) The writer picks a thesis, lists three ordered points each with evidence, then drafts "
                   "an intro, one paragraph per point, and a conclusion that lands the upshot.  "
                   "(B) The writer opens a blank page and types whatever thoughts about community service come to mind, adding each new idea as it arrives and stopping once the essay feels long enough. "
                   "Correct: A is planned; B is not. (A) fixes a thesis and an order first, so every paragraph "
                   "defends the thesis in a building sequence. (B) drifts with no thesis or order and tends to "
                   "repeat. Planning first is the move.")),
        Slot("MODEL", "annotated_before_after", "Watch unplanned drafting become plan-then-build",
             bank="community_service",
             body=("Here is the difference between drafting cold and building from a plan. Read the BEFORE, "
                   "then the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE writes with no plan and wanders. The AFTER plans a thesis and ordered points, "
                   "then builds each part from the plan. Plan first, then build, is the move.")),
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
        Slot("SUPPORTED", "production_frq", "Plan the essay: thesis and ordered points",
             ref="", bank="community_service", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=("Plan your argument essay on required community service. Write a single-paragraph outline: a "
                   "one-line THESIS that takes a side, then THREE ordered body POINTS, each naming its claim "
                   "and the evidence (from the source) it will use. This plan is what you will build the essay "
                   "from. Scored on Organization.")),
        Slot("MODEL", "diagnosis_frq", "Check your plan before you draft the whole essay",
             ref="", bank="community_service", scored=True,
             body=("First watch the check run on a provided plan, then run it on your own. Provided plan: "
                   "'Thesis: service is good. Points: it helps, it is nice, people like it.' Run the check "
                   "step by step. Step 1, thesis takes a clear side? Barely ('is good'), sharpen it. Step 2, "
                   "points ordered and distinct? No, 'helps / is nice / people like it' overlap, so make them "
                   "distinct and ordered. Step 3, evidence named per point? No, attach a source fact to each. "
                   "Now you: write a fresh thesis plus three ordered points for your service essay, then run "
                   "the same three checks and fix any that fail. Finish by naming which part your plan still "
                   "needs most.")),
        Slot("INDEPENDENT", "production_frq", "Write the full argument essay",
             ref="", bank="community_service", rubric_ref="rc.staar", scored=True, unit="essay",
             body=("On your own now, write the whole essay from your plan. Write a complete argument essay on "
                   "required community service: an INTRODUCTION that frames the thesis, THREE body paragraphs "
                   "(each a claim, attributed evidence, and a warrant, ordered to build and linked), and a "
                   "CONCLUSION that lands the upshot. Before you submit, check the essay: does every paragraph "
                   "defend the thesis, is each body paragraph a complete claim-evidence-warrant, do the "
                   "paragraphs build and link, does the conclusion add an upshot? Fix any that fail before you "
                   "submit. Take the time you need. Scored on Development/Organization/Purpose.")),
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: phones in school",
             ref="ACC-W910-ARG-LESSON-PHONEBAN", bank="phone_ban",
             body=("Read this new source about phones in school. Because your job is to write a full argument "
                   "essay from it, read the whole thing and gather a position plus several facts (with "
                   "sources) for evidence. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Write a full argument essay on a NEW topic",
             ref="", bank="phone_ban", rubric_ref="rc.staar", scored=True, unit="essay",
             body=("New topic. Plan and write a complete argument essay on whether schools should ban phones "
                   "for the full day: an intro that frames the thesis, three body paragraphs (claim + evidence "
                   "+ warrant, ordered and linked), and a conclusion that lands the upshot. Same plan-then-"
                   "build move as the service essay, new topic. Take the time you need. Scored on "
                   "Development/Organization/Purpose.")),
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
