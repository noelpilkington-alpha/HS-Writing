"""
lesson_g11_l14_synthesis_with_evaluation.py  -  G11 KC C.11.02, ARCHETYPE type-8 cross-source synthesis (essay). V3.1.

G11 course L14 (Unit 3, build), REBUILT to the v3.1 build spec (hand-authored). Teaching point (KEPT): write a
full multi-source synthesis that WEAVES one argument from the set AND WEIGHTS each source by what it is good for
and where it falls short, rather than leaning on every source equally. Written at the essay ceiling. Trait:
Development (synthesis) and Evidence (source evaluation).

Preserved EXACTLY from the prior L14: id="ACC-W1112-L-G11-C1102-0014", lesson_type=8, kc="C.11.02",
mnemonic_status="proposal", unit, and the bound stimuli (SYNTH-LESSON-0001 taught -> SYNTH-SET-0003 transfer).
The scored production ladder climbs multi_paragraph -> essay -> essay (type-8 ceiling = essay).

V3.1 changes vs the prior L14 (the two failing gates + the spine polish):
  1. FIXED the leaked internal label: the discrimination no longer says "a Grade-C design bet we label as a
     bet"; it is a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}].
  2. FIXED the wall-of-text teach card: the prose block is now a ONE_IDEA callout + real <ul>/<ol> lists.
  3. Deterministic FRQ + diagnosis via frq_prompt/setapart/checklist (no "Step 1/2" prose, no "Scored on"
     chrome); coping-model before/after kept; check tool folded in at first use as a real <ol> REMEMBER box.
All facts trace to the bound USGS/EPA/EIA source set; no fabricated figures. Own words, no em dashes, no named
HTML entities. Passes all 23 lesson_contract gates + render-qc. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A ceiling synthesis does <strong>two jobs at once</strong>: '
'it <strong>weaves</strong> one argument from the whole set, AND it <strong>weights</strong> each source by what it '
'can and cannot carry. Weaving alone is not enough; leaning on every source equally is the weak move.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: reread the synthesis</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, reread the whole essay and ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Is there ONE argument woven from the whole set, not a source-by-source summary?</li>'
'<li style="margin:2px 0">Is each source used only where it is strong evidence?</li>'
'<li style="margin:2px 0">Does the essay say where the set stops short, what no single source can settle?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you submit.</div></div>')

# coping-model before/after: a synthesis that weighted every source equally, rebuilt to weave AND weight. Contains
# BOTH a literal BEFORE and AFTER (content_depth). Figures trace to the bound set: Source 1 = national totals + the
# usable-water limit, Source 2 = power-plant cooling (41 percent), Source 3 = irrigation (42 percent). No em dashes.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> weaves, but weights every source the same</span>'
    '<p style="margin:8px 0 0;font-size:15px">All three sources say water is under strain, so the country should '
    'cut its water use everywhere by the same amount.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The draft leans on every source as if each were equally '
    'strong for one sweeping claim. The overview source is strong on national totals but weak on any single sector.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> weaves AND weights each source</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">SYNTHESIS + WEIGHTING</span> Because the overview source is strong evidence for the scale of '
      'the national limit (about 322 billion gallons drawn each day from a supply only 1 percent of which is usable), '
      'while the two sector sources show where the largest draws sit (power-plant cooling at about 41 percent and '
      'irrigation at about 42 percent), the set supports cutting the two heaviest uses first, though no single source '
      'settles which of those two giants a region should cut before the other.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">The argument is woven from the set AND says what each '
    'source can and cannot carry. Weave-and-weight is the college move.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1102-0014", grade="9-10", lesson_type=8,
    unit="G11 U3 - Synthesis with source evaluation",
    title="Weave the Argument, Weight the Sources",
    target=("Write a full multi-source synthesis that weaves ONE argument from the set AND weights each source "
            "by what it is good for and where it falls short, rather than leaning on every source equally. "
            "Written at the essay. Trait: Development (synthesis) and Evidence (source evaluation)."),
    acc_tags=["ACC.W.SRC.1", "ACC.W.INQ.1", "CCSS.W.11-12.7", "CCSS.W.11-12.8"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.02", "sot": "icm course-G11.md L14",
                "taught_stimulus": "ACC-W1112-SYNTH-LESSON-0001",
                "transfer_stimulus": "ACC-W910-SYNTH-SET-0003",
                "playbook": "_phase2/playbook_T8_WEAVE.md",
                "template": "v3.1 spine; SYNTHESIS-TIER binds full 3+ source sets; folds in source evaluation; UNTIMED.",
                "one_idea": "A ceiling synthesis weaves ONE argument from the set AND weights each source by what it can carry.",
                "one_reminder": "Reread check: one woven argument (not a summary)? each source used only where strong? says where the set stops short?",
                "version_note": ("V3.1 rebuild of L14. FIXED the leaked internal label (removed 'a Grade-C design "
                                 "bet we label as a bet' from the discrimination; moved options to choices=[]); "
                                 "broke the wall-of-text teach card into a ONE_IDEA callout + real <ul>/<ol> lists; "
                                 "deterministic frq_prompt/setapart/checklist bodies; coping-model before/after kept; "
                                 "check tool folded in at first use as an <ol> REMEMBER box. Preserved id, type 8, "
                                 "kc=C.11.02, mnemonic_status=proposal, unit, bound stimuli, and the unit ladder "
                                 "(SUPPORTED=multi_paragraph, INDEPENDENT/TRANSFER=essay)."),
                "review_provenance": "built to the G9 L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["synthesis-with-source-evaluation", "weight-each-source"],
    slots=[
        # ===== TEACH: the one idea + what weave/weight mean (as a list), then the order of work (as a list) =====
        Slot("TEACH", "teach_card", "The one idea: weave the argument, weight the sources",
             body=(ONE_IDEA +
                   "You have already practiced weaving. This lesson adds the second job. Two moves work together:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Weave</strong>: to synthesize means to combine several "
                   "sources into the one argument the whole set builds, instead of summarizing each source in "
                   "turn.</li>"
                   "<li style=\"margin:4px 0\"><strong>Weight</strong>: to weight a source means to say what it is "
                   "good evidence for and where it falls short, then lean on it only where it is strong. A national "
                   "dataset is strong for country-wide totals and weak for any one region; a single case is the "
                   "reverse.</li></ul>"
                   "The weak move weaves the argument but treats every source as equally authoritative on every "
                   "point. The strong move builds ONE argument and marks what each source can and cannot carry.")),
        Slot("TEACH", "teach_card", "How to build it, in order",
             body=("Here is the order of work. Follow it and the synthesis assembles itself from moves you already "
                   "own:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>READ</strong> the set for the one argument it builds and "
                   "for what each source is strong or weak evidence for.</li>"
                   "<li style=\"margin:4px 0\"><strong>WEIGH</strong>: next to each source, note what it is good "
                   "evidence for and where it falls short.</li>"
                   "<li style=\"margin:4px 0\"><strong>WEAVE</strong>: state the one argument, then organize by "
                   "point and assign each point to the source strongest for it.</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: reread against a short list, is it one "
                   "woven argument, is each source used only where it is strong, does it say where the set stops "
                   "short?</li></ol>"
                   "You are assembling moves you already own, in this order, into one essay.")),
        Slot("TEACH", "stimulus_display", "Read the source set: competing water uses (3 sources)",
             ref="ACC-W1112-SYNTH-LESSON-0001", bank="water_competing_uses",
             body=("Read this three-source set again. Because your job is synthesis with source evaluation, read "
                   "for both the one argument the set builds and for what each source is strong or weak evidence "
                   "for. The texts stay on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + check tool, then the check items =====
        Slot("MODEL", "annotated_before_after", "Watch an equal-weight synthesis get weighted",
             bank="water_competing_uses",
             body=("Here is the difference between weaving alone and weaving-and-weighting. Read the BEFORE, then "
                   "the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE leans on all three sources equally for one sweeping claim. The AFTER builds one "
                   "argument and weights each source by what it can carry. Weave-and-weight is the move." + REMEMBER +
                   "When you build your own, put the work in this order, then run the check before you submit.")),
        Slot("MODEL", "discrimination", "Which synthesis also weights the sources?",
             ref="", labeled_grade_c=True, bank="water_competing_uses",
             body=("You have watched an equal-weight synthesis get weighted. Now spot the target: which of these "
                   "weaves AND weights the sources, and which three do not? "
                   "(A) Because the overview source, the power-plant source, and the irrigation source all describe "
                   "water under strain, each one backs the argument every bit as strongly, so the set proves that "
                   "every single region of the country must cut its water use by the very same amount.  "
                   "(B) Because the overview source shows the scale of the national limit while the two sector "
                   "sources show where the largest draws sit, the set supports cutting the heaviest uses first, "
                   "though no source alone settles which giant a region should cut.  "
                   "(C) The essay reports what the overview source says, then what the power-plant source says, "
                   "then what the irrigation source says, one after another, and never joins them into a single "
                   "argument.  "
                   "(D) The essay rates each source in turn, calling the overview source strong on national totals "
                   "but weak on any one sector and the two sector sources strong on their own draws, then stops "
                   "without ever stating an argument the set builds. "
                   "Correct: B. It builds one argument and marks what each source can and cannot carry. A leans on "
                   "every source equally for one sweeping claim, C just summarizes source by source, and D weighs "
                   "the sources but never weaves them into a single argument."),
             choices=[
                 {"id": "A", "text": "Because the overview source, the power-plant source, and the irrigation source all describe water under strain, each one backs the argument every bit as strongly, so the set proves that every single region of the country must cut its water use by the very same amount.",
                  "correct": False,
                  "why": "This weaves but weights every source the same. It treats each source as equally strong for one sweeping claim, so a source good only on national totals is stretched to cover every region."},
                 {"id": "B", "text": "Because the overview source shows the scale of the national limit while the two sector sources show where the largest draws sit, the set supports cutting the heaviest uses first, though no source alone settles which giant a region should cut.",
                  "correct": True,
                  "why": "Correct. This builds one argument from the set AND weights each source, using the overview source for the national limit and the sector sources for where the draws are, while naming what none can settle."},
                 {"id": "C", "text": "The essay reports what the overview source says, then what the power-plant source says, then what the irrigation source says, one after another, and never joins them into a single argument.",
                  "correct": False,
                  "why": "This is a source-by-source summary, not a synthesis. There is no single woven argument, so there is nothing to weight the sources against."},
                 {"id": "D", "text": "The essay rates each source in turn, calling the overview source strong on national totals but weak on any one sector and the two sector sources strong on their own draws, then stops without ever stating an argument the set builds.",
                  "correct": False,
                  "why": "This does the weighting job but skips the weaving job. Judging each source's strengths is not enough on its own; without one argument the set builds, there is no synthesis to attach the weighting to."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this synthesis most need?",
             bank="water_competing_uses",
             body=("Diagnose before the reveal. A draft weaves a real argument from the set but leans on the "
                   "power-plant source to prove which region should cut most, a claim that source cannot carry. "
                   "Which single move would most improve it? "
                   "(A) weight the sources, use the power-plant source for the size of the cooling draw and the "
                   "overview source for the national limit  "
                   "(B) add a fourth source to the set so the disputed regional claim has still more evidence "
                   "standing behind it and reads as stronger to the grader  "
                   "(C) drop the power-plant source from the essay entirely and lean only on the overview source "
                   "for every single point the argument tries to make  "
                   "(D) make the whole argument shorter and tighter so the finished essay stays concise and moves "
                   "faster for the reader who is scoring it"),
             feedback=("Correct: A. The synthesis is sound but over-trusts one source beyond what it can carry. "
                       "The fix weights the sources: use each where it is strong (the power-plant source for the "
                       "cooling draw, the overview source for the national limit) and name that no single source "
                       "settles the regional question. Adding a source (B), dropping one (C), or shortening (D) "
                       "leave the mismatched weighting in place.")),

        # ===== SUPPORTED: plan a weave-and-weight synthesis (multi_paragraph) - the frame is the scaffold =====
        Slot("SUPPORTED", "production_frq", "Plan a weave-and-weight synthesis",
             ref="", bank="water_competing_uses", rubric_ref="rc.4trait", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Plan your synthesis of the water set before you write the essay.",
                 setapart_block=setapart("Fill in this plan:",
                                         "Argument the whole set builds: ______. Overview source (national totals): strong for ______, weak for ______. Power-plant source (cooling): strong for ______, weak for ______. Irrigation source (crops): strong for ______, weak for ______. Where the set stops short: ______."),
                 closer="Name the ONE argument the set builds, then next to each source note what it is strong "
                        "evidence for and where it falls short, so you know which source carries which point. "
                        "This plan is what you will build the essay from.")),
        # ===== INDEPENDENT: build the whole synthesis essay (essay ceiling) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write the synthesis essay",
             ref="", bank="water_competing_uses", rubric_ref="rc.4trait", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now, build the whole essay from your plan.",
                 closer="Write a full synthesis essay on the water set: an introduction that states the one "
                        "argument the set builds, body paragraphs organized by point that draw on the sources and "
                        "weight each by what it can carry, and a conclusion that names what the set supports and "
                        "where it stops short. Then run the reread check and fix any part that fails. Weaving and "
                        "weighting is what every real college synthesis is built on, and you are ready to do it "
                        "cold. Take the time you need.")),

        # COUNCIL FIX (2026-07-24): Option A (later-in-arc), check-only: this is a self-check on the student's OWN
        # just-written essay (a calibration/self-revision scaffold that runs AFTER the INDEPENDENT write), not a
        # separate graded rewrite, so there is no fresh draft to grade. The checklist is made READ-ONLY (plain-
        # string rows; the (question, answer) tuple form dropped and each row's conditional guidance folded into
        # one plain instruction). The slot stays a self-check. scored left as-is; no rewrite invented. Same
        # taught source (load balance).
        Slot("MODEL", "diagnosis_frq", "Check your synthesis: woven and weighted?",
             ref="", bank="water_competing_uses", scored=True,
             body=frq_prompt(
                 intro="Reread the essay you just wrote. Run this checklist on YOUR draft and fix any line that fails.",
                 checklist_block=checklist(title="Check your own draft against these (no need to type answers):", rows=[
                     "Is there ONE argument woven from the whole set? If it just says every source agrees rather than building a single argument, state the ONE argument the whole set builds and organize by point.",
                     "Is each source used only where it is strong? If it leans on all three sources equally, assign each point to the source strongest for it, the overview source for the national limit and the sector sources for where the biggest draws are.",
                     "Does it say where the set stops short? If no line names what the set cannot settle, add one, such as which of the two giant uses a region should cut first.",
                 ]),
                 closer="For every row that fails on your draft, fix it in the essay before you move on. Finish by "
                        "naming one source and the exact point it carries.")),
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
