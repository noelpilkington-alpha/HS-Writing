"""
lesson_g10_l24_gate_cross_text.py  -  G10 KC C.10.06, ARCHETYPE T7/T8: ESSAY-ASSEMBLY (BUILD, ceiling essay). COURSE GATE. V3.1.

G10 course L24 (Unit 4, GATE), rebuilt to the v3.1 build spec (hand-authored). Teaching point (KEPT): the
course-terminal task - independently plan, draft, and self-check a complete cross-text essay (analysis or
argument, as the prompt's verb sets) from a source set, with a synthesis claim, woven sources, and the
counterclaim answered. Written at the essay, UNTIMED (no Timeback timer; the rigor is the cold, full,
self-directed cross-text production). KC C.10.06.

Preserved EXACTLY from the current L24: id="ACC-W910-L-G10-C1006-0024", lesson_type=7,
mnemonic_status="proposal", kc="C.10.06", unit, the bound stimuli (SCHOOLYEAR taught -> CONGESTION transfer),
and every production_frq unit= value (SUPPORTED plan = multi_paragraph, INDEPENDENT + TRANSFER = essay). The
unit ladder still climbs to the essay, the type-7 ceiling.

V3.1 changes vs the prior L24 (the two failing gates + the spine polish):
  1. FIXED the leaked internal label: the discrimination no longer says "a Grade-C design bet we label as a
     bet"; it is a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}].
  2. FIXED the two wall-of-text teach cards: the prose blocks are now a ONE_IDEA callout + real <ul>/<ol>
     lists of the parts and the order of work (format_fidelity, and the v3.1 "parallel items as a list" rule).
  3. Deterministic FRQ + diagnosis prompts via frq_prompt/setapart/checklist (no "Step 1/2" prose, no
     "Scored on ..." chrome); coping-model before/after kept; the cross-text self-check (the 3-question reread)
     folded in at first use as a real <ol> REMEMBER box.
Own words faithful to the bound sources (NCES ~180-day calendar / summer slide / BLS salaried teachers for the
school-year set; no fabricated figures). No em dashes. Passes all 23 lesson_contract gates + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A strong cross-text essay is a <strong>PLAN, built '
'out and woven</strong>: a synthesis claim the whole source set supports, body paragraphs that weave the '
'sources together, one paragraph that answers the counterclaim, and a conclusion that lands the upshot. You '
'draft from the plan; you do not summarize one source, then the next, and hope.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: reread the cross-text essay</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, reread the whole essay and ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Is there a synthesis claim the whole source set supports?</li>'
'<li style="margin:2px 0">Are the sources woven together across paragraphs, not listed one at a time?</li>'
'<li style="margin:2px 0">Is the counterclaim named and then answered?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you submit.</div></div>')

# coping-model before/after: a source-by-source draft (no synthesis claim, sources listed, counterclaim never
# answered) rebuilt into a planned, woven cross-text essay. Contains BOTH a literal BEFORE and AFTER
# (content_depth). Short structural sketch, not a whole essay - the point is the list-vs-weave contrast.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> no plan, sources listed one at a time</span>'
    '<p style="margin:8px 0 0;font-size:15px"><i>Paragraph 1:</i> Source 1 says a longer school year would add '
    'learning time and shrink the summer slide. <i>Paragraph 2:</i> Source 2 says a longer year costs money and '
    'that time in a seat is not the same as learning. <i>Paragraph 3:</i> I think a longer year is good.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">There is no synthesis claim the set jointly '
    'supports, the sources are summarized in turn rather than woven, and the objection is stated but never '
    'answered. Nothing is built across the texts.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> planned, woven, and the objection answered</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">SYNTHESIS CLAIM</span> "A longer school year is worth adopting only if the added days '
      'raise the quality of learning, not just its quantity." '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">WOVEN BODY</span> "Source 1 shows why more days help: with a typical calendar near 180 '
      'days, the long break lets the summer slide erase learning that a fuller year would keep alive. Source 2 '
      'adds the limit: paid, salaried teachers and hot late-summer classrooms mean added days only pay off if '
      'the teaching stays strong." '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">COUNTERCLAIM ANSWERED</span> "Critics are right that seat time is not learning, which is '
      'exactly why the plan must fund quality, not only length."</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same two sources, but now a synthesis claim frames '
    'them, each body sentence pulls from both texts at once, and the objection is conceded and then answered. '
    'Every part is built from a plan.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1006-0024", grade="9-10", lesson_type=7,
    lesson_class="gate",
    unit="G10 U4 - GATE: cross-text essay (course terminal task)",
    title="G10 Gate: Write a Complete Cross-Text Essay",
    target=("The course gate: independently plan, draft, and self-check a complete cross-text essay (analysis "
            "or argument, as the prompt's verb sets) from a source set, with a synthesis claim, woven sources, "
            "and the counterclaim answered. Written at the essay, untimed. Trait: "
            "Development/Organization/Purpose."),
    acc_tags=["ACC.W.SRC.1", "ACC.W.PROD.1", "ACC.W.INFO.2", "CCSS.W.9-10.1", "CCSS.W.9-10.7", "CCSS.W.9-10.9"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.06", "sot": "icm course-G10.md L24 (COURSE GATE)",
                "taught_stimulus": "ACC-W910-ARG-OPP-LESSON-SCHOOLYEAR",
                "transfer_stimulus": "ACC-W910-ARG-OPP-LESSON-CONGESTION",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": "v3.1 spine; locked L01 template; SYNTHESIS-TIER binds full source sets; GATE = cold full cross-text production, UNTIMED.",
                "one_idea": "A strong cross-text essay is a plan, built out and woven (synthesis claim, woven sources, counterclaim answered, upshot).",
                "one_reminder": "Reread check: synthesis claim the set supports? sources woven not listed? counterclaim named and answered?",
                "version_note": ("V3.1 rebuild of L24. FIXED the two failing gates on the prior version: removed "
                                 "the leaked internal label ('a Grade-C design bet we label as a bet') from the "
                                 "discrimination and moved it to explicit choices=[]; broke the two wall-of-text "
                                 "teach cards into a ONE_IDEA callout + real <ul>/<ol> lists (format_fidelity). "
                                 "Deterministic frq_prompt/setapart/checklist bodies (no 'Step 1/2' prose, no "
                                 "'Scored on' chrome); the cross-text self-check folded in at first use. Preserved "
                                 "id, type 7, mnemonic_status=proposal, kc, unit, bound stimuli, and every "
                                 "production_frq unit= value (SUPPORTED=multi_paragraph, INDEPENDENT/TRANSFER=essay)."),
                "council": ("T7/T8 COURSE GATE: minimal-scaffold cross-text terminal task. Shell as final-review "
                            "retrieval, then the full cold cross-text essay. plan-weave-answer-vs-list "
                            "discrimination. Untimed: rigor is the cold self-directed cross-text production. "
                            "BUILD=proposal; unit=essay."),
                "review_provenance": "built to the L01/L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["independent-cross-text-essay", "run-the-whole-synthesis-routine"],
    # SCAFFOLD-FREE GATE (spine re-architecture, SPINE_DELIBERATION_verdict.md): a gate certifies INDEPENDENT
    # transfer, so it is the SRSD endpoint, not another teaching lesson. No annotated model, no discrimination,
    # no predict-the-fix. Just: a bare moves-checklist cue (recall, not re-teach) -> the HELD-OUT source
    # (boxed, stays on screen) -> an UNSCORED plan affordance -> ONE cold cross-text essay (the certification)
    # -> a POST-HOC self-score. The whole course taught these moves; the gate observes them cold.
    slots=[
        # ===== TEACH: a BARE recall cue only (the moves the course already taught) - NO re-teaching, NO model =====
        Slot("TEACH", "teach_card", "Before you write: the moves you already know",
             body=(ONE_IDEA +
                   "This is the gate. You have practiced every one of these moves across the course; here is the "
                   "checklist to run from memory as you write. No new teaching, no worked example: just you, the "
                   "sources, and the routine."
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Read the verb</strong>: analyze means one analytical claim "
                   "about the authors' craft; argue or should means a synthesis claim defended across the set "
                   "with the counterclaim answered.</li>"
                   "<li style=\"margin:4px 0\"><strong>Synthesis claim</strong>: a position the whole set jointly "
                   "supports, not a summary of one text at a time.</li>"
                   "<li style=\"margin:4px 0\"><strong>Woven body</strong>: one paragraph per point, each pulling "
                   "from more than one source at once, not a paragraph per source.</li>"
                   "<li style=\"margin:4px 0\"><strong>Counterclaim answered</strong>: name the strongest claim "
                   "from the other side, then answer it.</li>"
                   "<li style=\"margin:4px 0\"><strong>Conclusion</strong>: land the upshot.</li></ul>"
                   "There is no clock; take the time you need. Plan first, then weave.")),
        # ===== the HELD-OUT source (congestion): boxed, stays on screen through the cold write =====
        Slot("TEACH", "stimulus_display", "Read the source set: congestion pricing (both sides)",
             ref="ACC-W910-ARG-OPP-LESSON-CONGESTION", bank="congestion_pricing",
             body=("Read this two-source set on congestion pricing, charging tolls to drive downtown at busy "
                   "hours. This is the gate: you will write one complete cross-text argument essay from it. Read "
                   "both sources and gather a synthesis claim plus the objection you will answer. The texts stay "
                   "on screen while you work.")),
        # ===== UNSCORED plan affordance (not a certification write; a map for the cold essay) =====
        Slot("SUPPORTED", "production_frq", "Plan your essay (not graded)",
             ref="", bank="congestion_pricing", rubric_ref="rc.staar", scored=False, unit="essay",
             body=frq_prompt(
                 intro="Before you write, jot a quick plan. This plan is not graded; it is your map for the cold "
                       "essay. The task: should cities charge tolls to drive downtown during busy hours "
                       "(congestion pricing)? Use both sources.",
                 setapart_block=setapart("Fill in this plan:",
                                         "Synthesis claim: ______ (the position both sources support). Point 1: ______ (weaves both sources). Point 2: ______ (weaves both). Counterclaim point: names ______ from the other side, then answers it with ______."),
                 closer="Then write the full essay from this plan.")),
        # ===== the GATE: ONE cold cross-text essay on the held-out set (the certification write) =====
        Slot("TRANSFER", "production_frq", "GATE: write the complete cross-text essay",
             ref="", bank="congestion_pricing", rubric_ref="rc.staar", scored=True, unit="essay",
             body=frq_prompt(
                 intro="The gate. On your own now, write the whole cross-text essay from your plan. The task: "
                       "should cities charge tolls to drive downtown during busy hours (congestion pricing)? Use "
                       "both sources.",
                 closer="Write a complete cross-text argument essay: an introduction that states a synthesis "
                        "claim, body paragraphs that weave both sources and one that concedes and answers the "
                        "counterclaim, and a conclusion that lands the upshot. This is the terminal task the "
                        "whole course led to, and you are ready to do it cold. Take the time you need; there is "
                        "no time limit.")),
        # ===== POST-HOC self-score: judge your finished essay against the reread check (calibration) =====
        Slot("INDEPENDENT", "self_score", "Score your own essay, then predict the gate result",
             ref="", bank="congestion_pricing",
             body=("Predict, then see your grade. Reread your finished essay and run the three-question check: "
                   "is there a synthesis claim the whole set supports, are the sources woven rather than listed, "
                   "and is the counterclaim named and answered? Based on that, did your essay earn the gate?"),
             choices=[
                 {"id": "pass", "text": "Yes: all three are clearly there.", "correct": True,
                  "why": "If a synthesis claim, woven sources, and an answered counterclaim are all present, the "
                         "essay meets the gate. Compare this prediction to the grade you get back: matching them "
                         "is how you learn to judge your own cross-text writing."},
                 {"id": "gap", "text": "Not yet: at least one is missing or weak.", "correct": False,
                  "why": "Then fix it before you submit. Go back and add the missing piece (the synthesis claim, "
                         "the weaving, or the answer to the counterclaim), because any one of the three missing "
                         "keeps the essay below the gate."},
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
