"""
lesson_g9_l27_gate_argument_essay_v3_1.py  -  G9 KC C.9.04, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD, ceiling essay).
COURSE GATE (ARGUMENT). V3.1. NEW LESSON added 2026-07-14 per the Fable-5 course-design audit + Noel's decision:
the terminal gate must certify BOTH modes as separate cold full essays. L26 is the INFORMATIONAL gate; this is
its paired ARGUMENT gate.

Teaching point (KEPT): the course-terminal ARGUMENT task - independently plan, draft, and self-check a complete
single-source argument essay from scratch on a COLD (unseen) source, assembling every move the course taught (a
thesis that takes a side -> reasons backed by attributed evidence, each explained with a warrant ->
a conclusion that lands the upshot). Written at the essay, UNTIMED (Timeback has no timer; the rigor is the cold,
full, self-directed argument production). KC C.9.04.

COUNTERARGUMENT RE-ADDED 2026-07-21 (Noel overturned S2): counterargument is now TAUGHT in G9 as a full unit
(new KC C.9.07, G9 U4: recognize -> concede-then-answer -> answer-in-a-paragraph), so the argument gate again
REQUIRES and CHECKS it, at G9 introductory depth (name + answer ONE real objection while holding the side).
Standards basis: CCSS W.9-10.1a is a 9-10 BAND standard that includes distinguishing a claim from opposing
claims. The gate now certifies what G9 taught: side-taking thesis -> claim + attributed evidence + warrant per
reason -> a counterargument answered -> upshot. G10 U1 remains the deeper counterargument treatment. (Prior
2026-07-17 S2 removal is superseded; see docs/plans/2026-07-21-g9-counterargument-add.md.)

Rebuilt to the SCAFFOLD-FREE GATE template (spine re-architecture, SPINE_DELIBERATION_verdict.md), cloned from the
G10 L24 gate proof-of-concept. A gate certifies INDEPENDENT transfer, so it is the SRSD endpoint, not another
teaching lesson: NO annotated model, NO discrimination, NO predict-the-fix, NO diagnosis. Just five slots - a bare
moves-checklist recall cue (recall, not re-teach) -> the HELD-OUT source (boxed, stays on screen) -> an UNSCORED
plan affordance -> ONE cold argument essay (the certification write) -> a POST-HOC self-score. The whole course
taught these moves; the gate observes them cold. Uses ONLY the held-out WATERTRADEOFF source (the prior taught
SCHOOLLUNCH source is dropped, since the gate has nothing left to teach).

Preserved EXACTLY: id="ACC-W910-L-G9-C904-0029", lesson_type=7, mnemonic_status="proposal", kc="C.9.04", unit, and
the acc_tags. Own words, facts drawn faithfully from the bound source, no fabricated figures, no em dashes. Passes
all lesson_contract gates (incl. gate_gate_shape) + render-qc. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">The argument gate is the whole routine, run on your '
'own: <strong>PLAN</strong> a thesis that takes a side, then <strong>DRAFT</strong> from the plan, then '
'<strong>CHECK</strong>. No new move, just every move together, on a source you have not seen.</div></div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C904-0029", grade="9-10", lesson_type=7,
    lesson_class="gate",
    unit="G9 U5 - GATE: argument single-source essay (course terminal task, argue mode)",
    title="G9 Gate: Write a Complete Argument Essay",
    target=("The argument course gate: independently plan, draft, and self-check a complete single-source "
            "ARGUMENT essay (a thesis that takes a side), assembling every move the course taught. Paired with "
            "the informational gate. Written at the essay, untimed. Trait: Development/Organization/Purpose."),
    acc_tags=["ACC.W.PROD.1", "ACC.W.ARG.5", "ACC.W.INFO.2", "CCSS.W.9-10.1", "CCSS.W.9-10.4"],
    provenance={"copyright": "own_authored", "authored": "2026-07-14", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.9.04",
                "sot": "COURSE_DESIGN_AUDIT_2026-07-14.md (both-mode gate decision); paired with L26 informational gate",
                "taught_stimulus": "ACC-W910-ARG-LESSON-WATERTRADEOFF",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-WATERTRADEOFF",
                "one_idea": "The argument gate is the whole routine on your own: PLAN a side-taking thesis, DRAFT, then CHECK.",
                "one_reminder": "Gate self-check: thesis takes a side? claim+attributed evidence per paragraph? warrant explains why each fact proves the claim? one counterargument named and answered? upshot?",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": "SCAFFOLD-FREE GATE (cloned from G10 L24). ESSAY-TIER binds a full argument source; GATE = cold full production, UNTIMED.",
                "version_note": ("V3.1 rebuilt to the SCAFFOLD-FREE GATE template (spine re-architecture verdict, "
                                 "cloned from the G10 L24 gate proof-of-concept). A gate is the SRSD endpoint, not "
                                 "a teaching lesson, so the scaffold is removed: dropped the two extra teach cards, "
                                 "the annotated before/after, the discrimination, the predict-the-fix, the framed "
                                 "SUPPORTED plan-as-scored-write, and the diagnosis. Now five slots: a bare "
                                 "moves-checklist recall cue -> the held-out source (boxed) -> an UNSCORED plan "
                                 "affordance -> ONE cold argument essay (the certification write) -> a POST-HOC "
                                 "self-score. Uses ONLY the held-out WATERTRADEOFF source (the prior taught "
                                 "SCHOOLLUNCH source dropped). Preserved id, type 7, mnemonic_status=proposal, kc, "
                                 "unit, acc_tags. Untimed."),
                "council": ("T7/BUILD ARGUMENT GATE: minimal-scaffold terminal task in argue mode. Shell as a "
                            "final-review retrieval cue, then the full cold argument essay. Untimed: the rigor is the "
                            "cold self-directed production. BUILD=proposal; unit=essay."),
                "review_provenance": "rebuilt to the G10 L24 v3.1 scaffold-free gate pattern; all lesson_contract gates + render-qc clean."},
    fade_ledger_moves=["independent-full-argument-essay", "run-the-whole-routine"],
    # SCAFFOLD-FREE GATE (spine re-architecture, SPINE_DELIBERATION_verdict.md): a gate certifies INDEPENDENT
    # transfer, so it is the SRSD endpoint, not another teaching lesson. No annotated model, no discrimination,
    # no predict-the-fix, no diagnosis. Just: a bare moves-checklist cue (recall, not re-teach) -> the HELD-OUT
    # source (boxed, stays on screen) -> an UNSCORED plan affordance -> ONE cold argument essay (the certification)
    # -> a POST-HOC self-score. The whole course taught these moves; the gate observes them cold.
    slots=[
        # ===== TEACH: a BARE recall cue only (the argument moves the course already taught) - NO re-teaching =====
        Slot("TEACH", "teach_card", "Before you write: the moves you already know",
             body=(ONE_IDEA +
                   "This is the argument gate. You have practiced every one of these moves across the course; "
                   "here is the checklist to run from memory as you write. No new teaching, no worked example: "
                   "just you, the source, and the routine."
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>A thesis that takes a side</strong>: a thesis is a single "
                   "sentence your whole essay defends, and in an argument it takes a side someone could "
                   "dispute.</li>"
                   "<li style=\"margin:4px 0\"><strong>Reasons backed by evidence</strong>: each body paragraph "
                   "makes a claim and supports it with an attributed fact from the source.</li>"
                   "<li style=\"margin:4px 0\"><strong>A warrant for each reason</strong>: a warrant is a "
                   "sentence, placed after your evidence, that explains why that fact actually proves the claim, "
                   "instead of leaving the reader to connect it.</li>"
                   "<li style=\"margin:4px 0\"><strong>A counterargument, answered</strong>: name one real point "
                   "the other side would make, then answer it while holding your side (the move you built in the "
                   "counterargument unit).</li>"
                   "<li style=\"margin:4px 0\"><strong>Conclusion</strong>: land the upshot instead of repeating "
                   "the thesis.</li></ul>"
                   "There is no clock; take the time you need. Plan first, then draft.")),
        # ===== the HELD-OUT source (water tradeoff): boxed, stays on screen through the cold write =====
        Slot("TEACH", "stimulus_display", "Read the source: food vs power for water",
             ref="ACC-W910-ARG-LESSON-WATERTRADEOFF", bank="water_tradeoff",
             body=("Read this source about a region choosing between food and power when water runs short. This "
                   "is the gate: you will write one complete argument essay taking a side on which use should "
                   "get the limited water first. Read the whole thing, decide your side, and gather a claim plus "
                   "the objection you will answer. The text stays on screen while you work.")),
        # ===== UNSCORED plan affordance (not a certification write; a map for the cold essay) =====
        Slot("SUPPORTED", "production_frq", "Plan your essay (not graded)",
             ref="", bank="water_tradeoff", rubric_ref="rc.staar", scored=False, unit="essay",
             body=frq_prompt(
                 intro="Before you write, jot a quick plan. This plan is not graded; it is your map for the cold "
                       "essay. The task: when water runs short, which use, food or power, should get it first? "
                       "Take a side and use the source.",
                 setapart_block=setapart("Fill in this plan:",
                     "Thesis (the side you defend): ______. Reason 1: ______ (evidence: ______; warrant, why it "
                     "proves the claim: ______). Reason 2: ______ (evidence: ______; warrant: ______). "
                     "Counterargument (a real point the other side makes): ______; how you answer it while "
                     "holding your side: ______. Conclusion: the upshot is ______."),
                 closer="Then write the full essay from this plan.")),
        # ===== the GATE: ONE cold argument essay on the held-out source (the certification write) =====
        Slot("TRANSFER", "production_frq", "GATE: write the complete argument essay",
             ref="", bank="water_tradeoff", rubric_ref="rc.staar", scored=True, unit="essay",
             body=frq_prompt(
                 intro="The gate. On your own now, write the whole argument essay from your plan. The task: when "
                       "water runs short, which use, food or power, should get it first? Take a side and use the "
                       "source.",
                 closer="Write a complete argument essay: an introduction that states a thesis taking a clear "
                        "side, body paragraphs that each make a claim backed by attributed evidence and a warrant "
                        "explaining why that evidence proves the claim, a counterargument that names one real "
                        "point the other side would make and answers it while you hold your side, and a "
                        "conclusion that lands the upshot. This is the terminal task the whole course led to, and "
                        "you are ready to do it cold. Take the time you need; there is no time limit.")),
        # ===== POST-HOC self-score: judge your finished essay against the check (calibration) =====
        Slot("INDEPENDENT", "self_score", "Score your own essay, then predict the gate result",
             ref="", bank="water_tradeoff",
             body=("Predict, then see your grade. Reread your finished essay against the check: a clear side, "
                   "evidence for each reason, a warrant that explains why each fact proves the claim, and a "
                   "counterargument you named and answered. Did your essay earn the gate?"),
             choices=[
                 {"id": "pass", "text": "Yes: a clear side, attributed evidence and a warrant per reason, and a counterargument answered are all there.",
                  "correct": True,
                  "why": "If a side-taking claim, attributed evidence, a warrant explaining each fact, and one "
                         "counterargument named and answered are all present, the essay meets the gate. Compare "
                         "this prediction to the grade you get back: matching them is how you learn to judge your "
                         "own argument writing."},
                 {"id": "gap", "text": "Not yet: at least one of those is missing or weak.",
                  "correct": False,
                  "why": "Then fix it before you submit. Go back and add the missing piece (the side-taking "
                         "claim, the evidence, the warrant explaining why the evidence proves the claim, or the "
                         "counterargument answered), because any one of them missing keeps the essay below the gate."},
             ]),
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
