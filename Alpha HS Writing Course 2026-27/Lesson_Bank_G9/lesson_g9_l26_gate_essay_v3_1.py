"""
lesson_g9_l26_gate_essay_v3_1.py  -  G9 KC C.9.04, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD, ceiling essay). COURSE GATE.

G9 course L26 (Unit 4, GATE): the course-terminal task. Teaching point (KEPT): independently PLAN, DRAFT, and
SELF-CHECK a complete single-source INFORMATIONAL essay (a controlling idea, no side) from scratch on a COLD
(unseen) stimulus, assembling every move the course taught. KC C.9.04. This is the terminal gate; the rigor is
the cold source + independence, NOT a clock (UNTIMED - Timeback has no timer). rc.staar. BUILD=proposal.

SCAFFOLD-FREE GATE rebuild (spine re-architecture, SPINE_DELIBERATION_verdict.md):
  A gate certifies INDEPENDENT transfer, so it is the SRSD endpoint, not another teaching lesson. The prior L26
  carried a full teaching arc (annotated before/after model, discrimination, predict-the-fix, diagnosis, and a
  taught+transfer source pair). Those are REMOVED. The gate now has five slots: a bare moves-checklist cue
  (recall, not re-teach) -> the HELD-OUT volcanoes source (boxed, stays on screen) -> an UNSCORED plan affordance
  -> ONE cold informational essay (the certification write) -> a POST-HOC self-score. Only the held-out volcanoes
  source is used; the previously taught photosynthesis source is dropped. lesson_class="gate".

Preserved EXACTLY: id="ACC-W910-L-G9-C904-0026", lesson_type=7, mnemonic_status="proposal", kc="C.9.04",
acc_tags, unit. The scored cold write is unit="essay" (the T7 ceiling); the plan is scored=False. Own words
faithful to the volcanoes source. No em dashes. Passes the lesson_contract gates + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">The gate is the whole routine, run on your own: '
'<strong>PLAN</strong>, then <strong>DRAFT</strong> from the plan, then <strong>CHECK</strong>. No new move, '
'just every move together, on a source you have not seen.</div></div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C904-0026", grade="9-10", lesson_type=7,
    lesson_class="gate",
    unit="G9 U4 - GATE: informational single-source essay (course terminal task, explain mode)",
    title="G9 Gate: Write a Complete Informational Essay",
    target=("The informational course gate: independently plan, draft, and self-check a complete single-source "
            "INFORMATIONAL essay (a controlling idea, no side), assembling every move the course taught. Paired "
            "with the argument gate. Written at the essay, untimed. Trait: Development/Organization/Purpose."),
    acc_tags=["ACC.W.PROD.1", "ACC.W.ARG.5", "ACC.W.INFO.2", "CCSS.W.9-10.1", "CCSS.W.9-10.2", "CCSS.W.9-10.4"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.9.04", "sot": "icm course-G9.md L26 (COURSE GATE)",
                "taught_stimulus": "ACC-W910-INFO-LESSON-VOLCANOES",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-VOLCANOES",
                "one_idea": "The gate is the whole routine on your own: PLAN, DRAFT from the plan, then CHECK.",
                "one_reminder": "Gate self-check: controlling idea (no side)? body paragraphs with evidence? transitions? conclusion with an upshot?",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": "SCAFFOLD-FREE GATE; ESSAY-TIER binds full sources; GATE = cold full production, UNTIMED (no Timeback timer).",
                "version_note": ("SCAFFOLD-FREE GATE rebuild (SPINE_DELIBERATION_verdict.md). A gate certifies "
                                 "independent transfer, so the full teaching arc is REMOVED: the prior L26's "
                                 "annotated before/after model, discrimination, predict-the-fix, diagnosis, and the "
                                 "taught photosynthesis source are all gone. Five slots remain: a bare "
                                 "moves-checklist cue (recall, not re-teach), the HELD-OUT volcanoes source (boxed, "
                                 "on screen), an UNSCORED plan affordance (scored=False), ONE cold informational "
                                 "essay (scored TRANSFER, unit=essay), and a POST-HOC self-score. Preserved id, "
                                 "type 7, mnemonic_status=proposal, kc, acc_tags, unit. Untimed - no timer."),
                "council": ("T7/BUILD COURSE GATE: scaffold-free terminal task. A bare recall cue (the moves the "
                            "course already taught) -> the held-out source -> an unscored plan -> the full cold "
                            "informational essay -> a post-hoc self-score. Untimed: the rigor is the cold, "
                            "self-directed full production, not a clock. BUILD=proposal; unit=essay."),
                "review_provenance": "rebuilt to the G10 L24 scaffold-free gate pattern; gate-shape + render-qc clean"},
    fade_ledger_moves=["independent-full-essay", "run-the-whole-routine"],
    # SCAFFOLD-FREE GATE (spine re-architecture, SPINE_DELIBERATION_verdict.md): a gate certifies INDEPENDENT
    # transfer, so it is the SRSD endpoint, not another teaching lesson. No annotated model, no discrimination,
    # no predict-the-fix, no diagnosis. Just: a bare moves-checklist cue (recall, not re-teach) -> the HELD-OUT
    # volcanoes source (boxed, stays on screen) -> an UNSCORED plan affordance -> ONE cold informational essay
    # (the certification) -> a POST-HOC self-score. The whole course taught these moves; the gate observes them cold.
    slots=[
        # ===== TEACH: a BARE recall cue only (the moves the course already taught) - NO re-teaching, NO model =====
        Slot("TEACH", "teach_card", "Before you write: the moves you already know",
             body=(ONE_IDEA +
                   "This is the gate. You have practiced every one of these moves across the course; here is the "
                   "checklist to run from memory as you write. No new teaching, no worked example: just you, the "
                   "source, and the routine."
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Controlling idea</strong>: a controlling idea is a single "
                   "sentence that sets the focus your whole essay explains and takes no side. (For an argument "
                   "you would write a thesis, which is a single sentence that takes a side; this gate is explain "
                   "mode, so you write a controlling idea.)</li>"
                   "<li style=\"margin:4px 0\"><strong>Organized body paragraphs</strong>: one paragraph per "
                   "point, each with a clear point and a real source fact as its evidence, then a sentence that "
                   "explains how the fact supports the point.</li>"
                   "<li style=\"margin:4px 0\"><strong>Transitions</strong>: link the paragraphs at the seams so "
                   "they build in order.</li>"
                   "<li style=\"margin:4px 0\"><strong>Conclusion</strong>: land the upshot instead of "
                   "repeating.</li></ul>"
                   "There is no clock; take the time you need. Plan first, then draft.")),
        # ===== the HELD-OUT source (volcanoes): boxed, stays on screen through the cold write =====
        Slot("TEACH", "stimulus_display", "Read the source: volcanoes",
             ref="ACC-W910-INFO-LESSON-VOLCANOES", bank="volcanoes",
             body=("Read this source about volcanoes. This is the gate: you will write one complete "
                   "informational essay explaining how volcanoes form and erupt, using the source for your "
                   "evidence. Read the whole thing and gather a controlling idea plus a short plan (the parts "
                   "you will explain, each with a source fact). The text stays on screen while you work.")),
        # ===== UNSCORED plan affordance (not a certification write; a map for the cold essay) =====
        Slot("SUPPORTED", "production_frq", "Plan your essay (not graded)",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=False, unit="essay",
             body=frq_prompt(
                 intro="Before you write, jot a quick plan. This plan is not graded; it is your map for the cold "
                       "essay. The task: explain how volcanoes form and erupt, using the source.",
                 setapart_block=setapart("Fill in this plan:",
                     "Controlling idea (a focus, no side): ______. Body point 1: ______ (source fact: ______). "
                     "Body point 2: ______ (source fact: ______). Body point 3: ______ (source fact: ______). "
                     "Conclusion (the upshot): ______."),
                 closer="Then write the full essay from this plan.")),
        # ===== the GATE: ONE cold informational essay on the held-out source (the certification write) =====
        Slot("TRANSFER", "production_frq", "GATE: write the complete informational essay",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="essay",
             body=frq_prompt(
                 intro="The gate. On your own now, write the whole informational essay from your plan. The task: "
                       "explain how volcanoes form and erupt, using the source.",
                 closer="Write a complete informational essay: an introduction that states your controlling idea "
                        "(a focus, no side), body paragraphs that each explain one part with a source fact and an "
                        "explanation and are linked so they build, and a conclusion that lands the upshot. This "
                        "is the terminal task the whole course led to, and you are ready to do it cold. Take the "
                        "time you need; there is no time limit.")),
        # ===== POST-HOC self-score: judge your finished essay against the reread check (calibration) =====
        Slot("INDEPENDENT", "self_score", "Score your own essay, then predict the gate result",
             ref="", bank="volcanoes",
             body=("Predict, then see your grade. Reread your essay and run the check: a controlling idea (no "
                   "side), organized body paragraphs with evidence, transitions, and a conclusion with an "
                   "upshot. Did your essay earn the gate?"),
             choices=[
                 {"id": "pass", "text": "Yes: all parts are clearly there.", "correct": True,
                  "why": "If a controlling idea, organized body paragraphs with evidence, transitions, and a "
                         "conclusion with an upshot are all present, the essay meets the gate. Compare this "
                         "prediction to the grade you get back: matching them is how you learn to judge your own "
                         "writing."},
                 {"id": "gap", "text": "Not yet: at least one part is missing or weak.", "correct": False,
                  "why": "Then fix it before you submit. Add the missing piece (the controlling idea, a body "
                         "point's evidence, a transition, or the conclusion's upshot), because any one part "
                         "missing keeps the essay below the gate."},
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
