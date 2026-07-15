"""
lesson_g11_l16_midgate_synthesis.py  -  G11 KC C.11.02, ARCHETYPE T8: CROSS-SOURCE-SYNTHESIS (WEAVE, essay). MID-GATE. SCAFFOLD-FREE.

G11 course L16 (Unit 3, MID-GATE): synthesis-competence full write, rebuilt to the SCAFFOLD-FREE GATE template
(spine re-architecture, SPINE_DELIBERATION_verdict.md). Teaching point (KEPT): independently PLAN, DRAFT, and
SELF-CHECK a full multi-source synthesis that weaves ONE argument from the set and weights each source by what
it can carry, assembling the synthesis and source-evaluation moves the unit taught. Written at the essay,
UNTIMED (Timeback has no timer; the rigor is the cold, self-directed full write). NOT the course gate; a
mid-course checkpoint. KC C.11.02. WEAVE = proposal, unit = essay.

SCAFFOLD-FREE rebuild: a gate certifies INDEPENDENT transfer, so it is the SRSD endpoint, not another teaching
lesson. No annotated model, no discrimination, no predict-the-fix, no diagnosis. Just: a bare moves-checklist
cue (recall, not re-teach) -> the HELD-OUT source (boxed, stays on screen) -> an UNSCORED plan affordance ->
ONE cold synthesis essay (the certification write) -> a POST-HOC self-score. The unit taught these moves; the
gate observes them cold. Only the held-out set (SET-0002, AI and the workforce) is used; the previously-taught
SET-0003 (water scarcity) is dropped.

Preserved EXACTLY from the prior L16: id="ACC-W1112-L-G11-C1102-0016", lesson_type=8, mnemonic_status="proposal",
kc="C.11.02", unit family, acc_tags, and the essay grain. lesson_class="gate" added.
Facts trace to the bound federal source set. Own words, no fabricated figures, no em dashes.
Passes all lesson_contract gates (gate-class rules) + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A synthesis is a <strong>PLAN, woven and weighted</strong>: '
'you name the ONE argument the whole set builds, organize by point so several sources meet on each, and lean on '
'each source where it is strong. You do not tour the sources one at a time and hope.</div></div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1102-0016", grade="9-10", lesson_type=8,
    lesson_class="gate",
    unit="G11 U3 - MID-GATE: synthesis-competence full write",
    title="Mid-Gate: Write a Full Synthesis on Your Own",
    target=("The mid-course gate: independently plan, draft, and self-check a full multi-source synthesis that "
            "weaves ONE argument from the set and weights each source, assembling the synthesis and source-"
            "evaluation moves the unit taught. Written at the essay, untimed. Trait: Development (synthesis) and "
            "Evidence (source evaluation)."),
    acc_tags=["ACC.W.SRC.1", "ACC.W.INQ.1", "CCSS.W.11-12.7", "CCSS.W.11-12.8"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.02", "sot": "icm course-G11.md L16 (MID-GATE)",
                "taught_stimulus": "ACC-W910-SYNTH-SET-0002",
                "transfer_stimulus": "ACC-W910-SYNTH-SET-0002",
                "playbook": "_phase2/playbook_T8_WEAVE.md",
                "template": ("SCAFFOLD-FREE GATE spine; SYNTHESIS-TIER binds full sets; MID-GATE = cold full "
                             "synthesis on a HELD-OUT set, UNTIMED (no Timeback timer). NOT the course gate."),
                "one_idea": "A synthesis is a plan, woven and weighted: one argument, organized by point, each source used where strong.",
                "one_reminder": "Synthesis self-check: one woven argument (not a source tour)? each source weighted where strong? conclusion names the limit?",
                "version_note": ("SCAFFOLD-FREE rebuild of L16 (spine re-architecture verdict): a gate certifies "
                                 "INDEPENDENT transfer, so the teaching scaffold is removed. Dropped the "
                                 "annotated before/after, the discrimination, the predict-the-fix, and the "
                                 "diagnosis_frq; kept only a bare moves-checklist cue -> the held-out source -> an "
                                 "UNSCORED plan affordance -> ONE cold synthesis essay -> a POST-HOC self-score. "
                                 "Uses ONLY the held-out set (SET-0002, AI and the workforce); the previously "
                                 "taught SET-0003 (water scarcity) is dropped. Preserved id, type 8, kc C.11.02, "
                                 "mnemonic_status=proposal, unit, acc_tags, and the essay grain; added "
                                 "lesson_class=gate."),
                "council": ("T8/WEAVE MID-GATE: SCAFFOLD-FREE synthesis-competence checkpoint. A bare recall cue "
                            "(ONE_IDEA + the moves list) -> the held-out source -> an unscored plan -> ONE cold "
                            "synthesis (the certification) -> a post-hoc self-score. Untimed: rigor is the cold, "
                            "self-directed full synthesis. WEAVE=proposal; unit=essay. Mid-course, not completion."),
                "review_provenance": "rebuilt to the G10 L24 scaffold-free gate pattern; gate-class gates + render-qc clean"},
    fade_ledger_moves=["independent-full-synthesis", "run-the-whole-synthesis-routine"],
    # SCAFFOLD-FREE GATE (spine re-architecture, SPINE_DELIBERATION_verdict.md): a gate certifies INDEPENDENT
    # transfer, so it is the SRSD endpoint, not another teaching lesson. No annotated model, no discrimination,
    # no predict-the-fix, no diagnosis. Just: a bare moves-checklist cue (recall, not re-teach) -> the HELD-OUT
    # source (boxed, stays on screen) -> an UNSCORED plan affordance -> ONE cold synthesis essay (the
    # certification) -> a POST-HOC self-score. The whole unit taught these moves; the gate observes them cold.
    slots=[
        # ===== TEACH: a BARE recall cue only (the moves the unit already taught) - NO re-teaching, NO model =====
        Slot("TEACH", "teach_card", "Before you write: the synthesis moves you already know",
             body=(ONE_IDEA +
                   "This is the mid-gate. You have practiced every one of these moves across the unit; here is the "
                   "checklist to run from memory as you write. No new teaching, no worked example: just you, the "
                   "sources, and the routine."
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Synthesis claim</strong>: one position the whole source set "
                   "jointly supports, not a summary of one source at a time.</li>"
                   "<li style=\"margin:4px 0\"><strong>Woven body</strong>: organize by point so several sources "
                   "meet on each, not a paragraph per source.</li>"
                   "<li style=\"margin:4px 0\"><strong>Weighted, evaluated sources</strong>: lean on each source "
                   "where it is strong and note what it cannot carry.</li>"
                   "<li style=\"margin:4px 0\"><strong>Conclusion</strong>: name what the set supports and where "
                   "it stops short.</li></ul>"
                   "There is no clock; take the time you need. Plan first, then weave.")),
        # ===== the HELD-OUT source (AI and the workforce): boxed, stays on screen through the cold write =====
        Slot("TEACH", "stimulus_display", "Read the source set: AI and the workforce",
             ref="ACC-W910-SYNTH-SET-0002", bank="ai_workforce_synthesis",
             body=("Read this source set on AI and the workforce. This is the mid-gate: you will write one "
                   "complete synthesis essay from it. Read the whole set, gather a synthesis claim the set builds, "
                   "and note what each source can carry. The texts stay on screen while you work.")),
        # ===== UNSCORED plan affordance (not a certification write; a map for the cold essay) =====
        Slot("SUPPORTED", "production_frq", "Plan your synthesis (not graded)",
             ref="", bank="ai_workforce_synthesis", rubric_ref="rc.ap", scored=False, unit="essay",
             body=frq_prompt(
                 intro="Before you write, jot a quick plan. This plan is not graded; it is your map for the cold "
                       "essay. Use every source in the set.",
                 setapart_block=setapart("Fill in this plan:",
                                         "Synthesis claim: ______ (the one position the whole set builds). Point 1: ______ (weaves several sources) + which source is strong for it. Point 2: ______ (weaves several) + source. The limit: where the set stops short: ______."),
                 closer="Then write the full synthesis from this plan.")),
        # ===== the GATE: ONE cold synthesis essay on the held-out set (the certification write) =====
        Slot("TRANSFER", "production_frq", "THE MID-GATE: write the complete synthesis",
             ref="", bank="ai_workforce_synthesis", rubric_ref="rc.ap", scored=True, unit="essay",
             body=frq_prompt(
                 intro="The gate. On your own now, write the whole synthesis from your plan. Use every source in "
                       "the set.",
                 closer="Write a complete synthesis essay: an introduction that states the one synthesis claim the "
                        "whole set builds, body paragraphs organized by point that weave several sources and weight "
                        "each by what it can carry, and a conclusion that names what the set supports and where it "
                        "stops short. This is the checkpoint the whole unit led to, and you are ready to do it "
                        "cold. Take the time you need; there is no time limit.")),
        # ===== POST-HOC self-score: judge your finished synthesis against the reread check (calibration) =====
        Slot("INDEPENDENT", "self_score", "Score your own synthesis, then predict the result",
             ref="", bank="ai_workforce_synthesis",
             body=("Predict, then see your grade. Reread your finished synthesis: is there one synthesis claim the "
                   "whole set builds, are the sources woven and weighted rather than toured, and does the "
                   "conclusion name the limit? Based on that, did your essay earn the gate?"),
             choices=[
                 {"id": "pass", "text": "Yes: synthesis claim, woven sources, weighted evidence.", "correct": True,
                  "why": "If a synthesis claim, woven sources, and weighted evidence are all present, the essay "
                         "meets the gate. Compare this prediction to the grade you get back: matching them is how "
                         "you learn to judge your own synthesis writing."},
                 {"id": "gap", "text": "Not yet: one is missing or weak.", "correct": False,
                  "why": "Then fix it before submitting. Go back and add the missing piece (the synthesis claim, "
                         "the weaving, or the weighting), because any one of the three missing keeps the essay "
                         "below the gate."},
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
