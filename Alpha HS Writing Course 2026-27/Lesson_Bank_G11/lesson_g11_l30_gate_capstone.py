"""
lesson_g11_l30_gate_capstone.py  -  G11 KC C.11.02, ARCHETYPE T8: CROSS-SOURCE-SYNTHESIS (WEAVE, essay). COURSE GATE.

G11 course L30 (Unit 6, COURSE GATE): the course-terminal cumulative capstone, rebuilt to the SCAFFOLD-FREE GATE
template (spine re-architecture, SPINE_DELIBERATION_verdict.md). Teaching point (KEPT): on a cold prompt the
student FIRST names the FRQ task type from its tell, THEN writes the response that type rewards. A gate certifies
INDEPENDENT transfer, so it is the SRSD endpoint, not another teaching lesson: no annotated model, no
discrimination, no predict-the-fix, no diagnosis. Just a bare recall cue (the tells + core moves the whole course
already taught) -> the HELD-OUT source-free prompt (boxed, stays on screen) -> an UNSCORED plan affordance -> ONE
cold "name the type, then write" essay (the certification) -> a POST-HOC self-score. UNTIMED.

Preserved EXACTLY: id="ACC-W1112-L-G11-C1102-0030", lesson_type=8, mnemonic_status="proposal", kc="C.11.02",
unit (G11 U6 COURSE GATE), acc_tags, and the held-out transfer stimulus (SFA-PROMPT-0002) as the single bound
source. The SUPPORTED plan is unit=essay/scored=False (an affordance); the TRANSFER cold write is unit=essay/
scored=True (the one certification write).

Scaffold-free rewrite (vs the prior full-arc V3.1 version): removed the two extra teach cards, the
annotated_before_after coping model, the discrimination, the predict-the-fix, the diagnosis_frq, and the second
(synthesis) taught source. The gate now runs on ONLY the held-out source-free prompt: read it, name its type,
write the argument its moves reward. Own words, no em dashes. Passes all 24 lesson_contract gates + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">On the gate you write complete essays cold. The one '
'decision that governs each is the <strong>task type</strong>: name it first, because the wrong type means the '
'wrong moves however well you write.</div></div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1102-0030", grade="9-10", lesson_type=8,
    lesson_class="gate",
    unit="G11 U6 - COURSE GATE: cumulative capstone (name the task type, then write)",
    title="G11 Gate: Name the Task Type, Then Write the Right Essay",
    target=("The course gate: on a cold prompt, independently name the task type from its tell and write the "
            "essay its moves reward, planning and checking. Certified on a held-out source-free prompt (name it, "
            "then argue a position from own knowledge). Written at the essay, untimed. Trait: Development, "
            "Evidence, and Purpose."),
    acc_tags=["ACC.W.SRC.1", "ACC.W.ARG.1", "ACC.W.ARG.2", "ACC.W.PROD.1", "CCSS.W.11-12.1", "CCSS.W.11-12.7"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.02", "sot": "icm course-G11.md L30 (COURSE GATE)",
                "taught_stimulus": "ACC-W910-SYNTH-SET-0003",
                "transfer_stimulus": "ACC-W910-SFA-PROMPT-0002",
                "playbook": "_phase2/playbook_T8_WEAVE.md",
                "one_idea": "Name the task type first; the type dictates the moves. Read the tell, then run that type's moves.",
                "one_reminder": "Check: named the type + moves match? one clear position/argument, not a survey? planned before drafting?",
                "template": ("SCAFFOLD-FREE GATE spine (SPINE_DELIBERATION_verdict.md); GATE = cold full "
                             "production, UNTIMED (no Timeback timer). Held-out source = the source-free prompt "
                             "SFA-PROMPT-0002; the student names the type, then writes the argument."),
                "version_note": ("SCAFFOLD-FREE rewrite of the prior full-arc V3.1 L30. A gate certifies "
                                 "INDEPENDENT transfer, so it is the SRSD endpoint, not another teaching lesson: "
                                 "removed the two extra teach cards, the annotated_before_after coping model, the "
                                 "discrimination, the predict-the-fix, the diagnosis_frq, and the second (synthesis) "
                                 "taught source. Now: a bare recall cue (tells + core moves) -> the HELD-OUT "
                                 "source-free prompt (boxed) -> an UNSCORED plan (scored=False) -> ONE cold "
                                 "name-the-type-then-write essay (scored=True, TRANSFER) -> a POST-HOC self-score. "
                                 "Preserved id, type 8, mnemonic_status=proposal, kc, unit, acc_tags, and the "
                                 "held-out transfer stimulus (SFA-PROMPT-0002); SUPPORTED plan unit=essay/"
                                 "scored=False, TRANSFER cold write unit=essay/scored=True."),
                "council": ("T8/WEAVE COURSE GATE, scaffold-free (verdict): name-the-type-then-write, certified "
                            "cold on the held-out source-free prompt. Recall cue + held-out source + unscored plan "
                            "+ one cold scored write + post-hoc self-score. Untimed. WEAVE=proposal.")},
    fade_ledger_moves=["cumulative-capstone", "name-type-then-write"],
    # SCAFFOLD-FREE GATE (spine re-architecture, SPINE_DELIBERATION_verdict.md): a gate certifies INDEPENDENT
    # transfer, so it is the SRSD endpoint, not another teaching lesson. No annotated model, no discrimination,
    # no predict-the-fix, no diagnosis. Just: a bare recall cue (the tells + core moves the course already
    # taught) -> the HELD-OUT source (boxed, stays on screen) -> an UNSCORED plan affordance -> ONE cold
    # name-the-type-then-write essay (the certification) -> a POST-HOC self-score. The gate observes cold.
    slots=[
        # ===== TEACH: a BARE recall cue only (the tells + moves the course already taught) - NO re-teaching =====
        Slot("TEACH", "teach_card", "Before you write: name the type, then run its moves",
             body=(ONE_IDEA +
                   "This is the gate. You have practiced every one of these moves across the course; here is the "
                   "checklist to run from memory. No new teaching and no worked example: just you, the prompt, and "
                   "the routine. Read the prompt first for its <strong>tell</strong>, the signal that names the "
                   "task type:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>A labeled SET of sources on screen means SYNTHESIS</strong>. "
                   "To synthesize is when you combine several given sources into one argument, weaving them rather "
                   "than summarizing each in turn. Core moves: one argument the whole set supports, sources woven "
                   "and weighted.</li>"
                   "<li style=\"margin:4px 0\"><strong>One passage handed to you to analyze for HOW it works means "
                   "RHETORICAL ANALYSIS</strong>. A rhetorical device is a technique a writer uses to move a "
                   "reader, for example an appeal or a repeated phrase. Core moves: name the writer's choices and "
                   "explain the effect each has on the reader.</li>"
                   "<li style=\"margin:4px 0\"><strong>A general question with no sources to cite means "
                   "ARGUMENT</strong> (source-free). A thesis is a one-sentence claim you defend with your own "
                   "knowledge. Core moves: stake a defensible thesis and carry it with specific developed "
                   "examples.</li></ul>"
                   "The trap is forcing one favorite essay onto every prompt. Name the type first, then the right "
                   "moves follow. There is no clock; take the time you need. Plan first, then write.")),
        # ===== the HELD-OUT source (source-free prompt): boxed, stays on screen through the cold write =====
        Slot("TEACH", "stimulus_display", "Read the prompt: the individual or the community?",
             ref="ACC-W910-SFA-PROMPT-0002", bank="sfa_individual_community",
             body=("Read this prompt on the individual and the community. This is the gate: you will write one "
                   "complete essay from it. First name the task type from its tell. It opens with background "
                   "framing and then a question, but there are no titled sources to cite and no labeled "
                   "perspectives, so it is a source-free argument. Then gather your plan: a position and the "
                   "specific examples that will carry it. The text stays on screen while you work.")),
        # ===== UNSCORED plan affordance (not a certification write; a map for the cold essay) =====
        Slot("SUPPORTED", "production_frq", "Name the type and plan your essay (not graded)",
             ref="", bank="sfa_individual_community", rubric_ref="rc.ap", scored=False, unit="essay",
             body=frq_prompt(
                 intro="Before you write, jot a quick plan. This plan is not graded; it is your map for the cold "
                       "essay. First write which task type this is and the tell that names it, then plan the "
                       "essay that type rewards.",
                 setapart_block=setapart("Fill in this plan:",
                                         "Task type: ______ (and the tell that names it). Position: ______ (the stance you will defend). Point 1: ______ + the specific example that carries it. Point 2: ______ + its example. Strongest objection you will answer: ______."),
                 closer="Then write the full essay from this plan.")),
        # ===== the GATE: ONE cold name-the-type-then-write essay on the held-out prompt (certification write) ====
        Slot("TRANSFER", "production_frq", "GATE: name the type, then write the complete essay",
             ref="", bank="sfa_individual_community", rubric_ref="rc.ap", scored=True, unit="essay",
             body=frq_prompt(
                 intro="The gate. On your own now, write the whole essay from your plan. The task: when, if ever, "
                       "should individual freedom yield to the good of the community?",
                 closer="First name the task type in a phrase, then write the complete essay its moves reward. "
                        "Because this prompt gives no sources and no labeled perspectives, it is a source-free "
                        "argument: open with a defensible thesis, give body paragraphs each carried by one "
                        "specific developed example from your reading, studies, observation, or experience, and "
                        "close with a conclusion. This is the terminal task the whole course led to, and you are "
                        "ready to do it cold. Take the time you need; there is no time limit.")),
        # ===== POST-HOC self-score: judge your finished essay against the type-and-moves check (calibration) =====
        Slot("INDEPENDENT", "self_score", "Score your own essay, then predict the gate result",
             ref="", bank="sfa_individual_community",
             body=("Predict, then see your grade. Reread your finished essay: did you name the right task type, "
                   "and do your moves match it? Based on that, did your essay earn the gate?"),
             choices=[
                 {"id": "pass", "text": "Yes: I named the right type and wrote its core moves.", "correct": True,
                  "why": "If you named this as a source-free argument and defended one clear thesis with specific "
                         "developed examples, the essay meets the gate. Compare this prediction to the grade you "
                         "get back: matching them is how you learn to judge your own writing."},
                 {"id": "gap", "text": "Not yet: wrong type or a core move missing.", "correct": False,
                  "why": "Then fix it before you submit. Name the type correctly and add the missing move (a "
                         "defensible thesis, or an example that actually carries a point), because a type mismatch "
                         "or a missing core move keeps the essay below the gate."},
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
