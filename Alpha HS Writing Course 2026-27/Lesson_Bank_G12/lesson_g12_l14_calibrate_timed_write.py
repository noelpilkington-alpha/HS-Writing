"""
lesson_g12_l14_calibrate_timed_write.py  -  G12 KC C.12.02, ARCHETYPE T8: CROSS-SOURCE-SYNTHESIS (WEAVE, essay)
with a K2 CHECK/calibration overlay. V3.1.

G12 course L14 (Unit 2, check), rebuilt to the v3.1 build spec (hand-authored). Teaching point (KEPT): calibrate
a full-write. Predict your OWN essay's rubric scores across the AP rows (Evidence, Sophistication) with reasons
drawn from the WHOLE essay, submit, the grader reveals the scores, then name the GAP, especially the pacing
failure mode where a strong first half is predicted high but a rushed, fading second half scores lower.
KC C.12.02. Delivery UNTIMED (Timeback has no timer); framed as writing under your own budget/pacing.

Preserved EXACTLY from the prior L14: id="ACC-W910-L-G12-C1202-0014", lesson_type=8, mnemonic_status="proposal",
unit, the bound stimuli (WATERTRADEOFF taught -> WORKFORCEINVEST transfer), rc.ap grader routing, and every
production_frq unit= value (essay). The K2 predict->reveal (self_score before a graded reveal) is preserved.

V3.1 changes vs the prior L14 (the two failing gates + the spine polish):
  1. FIXED the leaked internal label: the discrimination no longer says "a Grade-C design bet we label as a
     bet"; it is a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}]
     (leaked_internal_label). labeled_grade_c=True stays in CODE only.
  2. FIXED the wall-of-text teach cards: the two prose blocks are now a ONE_IDEA callout + real <ul>/<ol> lists
     of the routine and the pacing failure mode (format_fidelity, "parallel items as a list" rule).
  3. Deterministic FRQ + diagnosis prompts via frq_prompt/setapart/checklist (no "Step 1/2" prose); the
     coping-model before/after is kept with a literal BEFORE + AFTER; the check tool (predict-from-the-whole
     3-question checklist) is folded in at first use as a real <ol> REMEMBER box.
Own words, no fabricated figures, no em dashes, no named HTML entities. Passes all 23 gates + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A mastery writer can <strong>predict a full-write&#39;s '
'scores before the grader returns them</strong>, but only by reading the <strong>whole essay</strong>, not the '
'strong opening. Calibration means predicting each rubric row with a reason, then naming the gap to the grader, '
'usually a pacing gap where the second half faded.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: predict from the whole essay</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit a prediction, ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Did I predict each row from the WHOLE essay, not just the opening?</li>'
'<li style="margin:2px 0">Did I give a reason for each row, tied to a specific part of the essay?</li>'
'<li style="margin:2px 0">After the reveal, can I name the gap and check whether pacing caused it?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If you cannot answer yes to all three, your prediction '
'is reading the opening, not the essay.</div></div>')

# coping-model before/after: an opening-only prediction rebuilt into a whole-essay prediction that names the
# pacing gap. Contains BOTH a literal BEFORE and AFTER (content_depth). No named person (stateless rule).
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> predicts from the strong opening only</span>'
    '<p style="margin:8px 0 0;font-size:15px">I predict a top score, because my introduction and first body '
    'paragraph were excellent.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The grader scores the whole essay, not the opening. '
    'Predicting from the strong start ignores the rushed third paragraph and cut ending that pacing usually '
    'costs.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> predicts across the whole essay, names the gap</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">PREDICT + REASON</span> I predict Evidence 2, Sophistication no: the opening held the '
      'tension, but body three ran thin and the ending was cut short. '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">NAME THE GAP</span> If the grader agrees, the gap is that pacing let the last '
      'paragraph fade, which is what cost the Sophistication row.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same essay, but now the prediction reads the whole '
    'piece and names the pacing gap instead of coasting on the strong start. That is calibration on a '
    'full-write.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G12-C1202-0014", grade="9-10", lesson_type=8,
    unit="G12 U2 - Calibrate a full-write (predict, grader-reveal, name the pacing gap)",
    title="Predict Your Full-Write Scores, Then Name the Pacing Gap",
    target=("Predict your own full-write's rubric scores across the rows (Evidence, Sophistication) with reasons "
            "drawn from the WHOLE essay, submit, then name the gap between your prediction and the grader, "
            "especially where pacing let the essay fade, rather than predicting from the strong opening. Written "
            "at the essay. Trait: self-assessment across the AP rows."),
    acc_tags=["ACC.W.PROD.3", "CCSS.W.11-12.5"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.12.02", "sot": "icm course-G12.md L14",
                "taught_stimulus": "ACC-W910-ARG-LESSON-WATERTRADEOFF",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-WORKFORCEINVEST",
                "playbook": "_phase2/playbook_T5_CHECK.md",
                "template": ("v3.1 spine; binds G12 argument LESSON source; K2 own-work calibration on a "
                             "budgeted full-write is stateless-safe; lesson_type=8 because calibration operates "
                             "on a full essay (T5 caps at paragraph); UNTIMED (no Timeback timer)."),
                "one_idea": "Predict a full-write's scores from the WHOLE essay, then name the gap (usually a pacing gap).",
                "one_reminder": "Predict-from-the-whole check: whole essay not opening? a reason per row? name the gap + check pacing?",
                "version_note": ("V3.1 rebuild of L14. FIXED the two failing gates: removed the leaked internal "
                                 "label ('a Grade-C design bet we label as a bet') from the discrimination and "
                                 "moved it to explicit choices=[]; broke the wall-of-text teach cards into a "
                                 "ONE_IDEA callout + real <ul>/<ol> lists (format_fidelity). Deterministic "
                                 "frq_prompt/setapart/checklist bodies (no 'Step 1/2' prose); coping-model "
                                 "before/after kept; check tool folded in at first use. Preserved id, type 8, "
                                 "mnemonic_status=proposal, unit, bound stimuli, rc.ap routing, and every "
                                 "production_frq unit=essay value (calibration ceiling = essay)."),
                "council": ("T8/WEAVE G12 own-work calibration (K2, map role = check): predict-own-scores -> "
                            "grader-reveal -> name-pacing-gap on a budgeted full-write. self_score calibration "
                            "enforced by judge-then-reveal gate. whole-essay-vs-opening discrimination labeled "
                            "Grade-C in code. unit=essay. Stateless-safe.")},
    fade_ledger_moves=["predict-full-write-scores", "name-the-pacing-gap"],
    slots=[
        # ===== TEACH: the one idea + the routine (as a list), then the pacing failure mode (as a list) =====
        Slot("TEACH", "teach_card", "The one idea: predict from the whole essay",
             body=(ONE_IDEA +
                   "You already know how to write a full argument essay. The new move is judging your own "
                   "finished essay before the grader does. Run this routine:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>PREDICT</strong>: for each rubric row (Evidence 1 to 4, "
                   "Sophistication yes or no), write your predicted score.</li>"
                   "<li style=\"margin:4px 0\"><strong>REASON</strong>: tie each prediction to a specific part "
                   "of the essay, drawn from the whole piece, not just the opening.</li>"
                   "<li style=\"margin:4px 0\"><strong>SUBMIT</strong>: send the essay to the grader and read "
                   "the scores it returns.</li>"
                   "<li style=\"margin:4px 0\"><strong>NAME THE GAP</strong>: for any row where you and the "
                   "grader differ, say what you missed, and check whether pacing caused it.</li></ul>"
                   "The trap is predicting from the strong start. A great intro feels like a top score, but the "
                   "grader also reads the paragraphs you wrote when you were running low on time.")),
        Slot("TEACH", "teach_card", "The pacing failure mode: a strong start, a fading finish",
             body=("Most miscalibration on a full-write comes from one place. You feel best about the parts you "
                   "wrote first, when you were fresh, so you predict high. But budget pressure shows up late, "
                   "and the grader reads all of it. Watch for these:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>The thin late paragraph</strong>: body three drops its "
                   "evidence or its reasoning because time was short.</li>"
                   "<li style=\"margin:4px 0\"><strong>The cut ending</strong>: the conclusion is one rushed "
                   "line, or missing, so nothing lands.</li>"
                   "<li style=\"margin:4px 0\"><strong>The dropped tension</strong>: the essay stops holding "
                   "both sides of the trade-off near the end, which is what the Sophistication row rewards.</li></ol>"
                   "So predict across the essay: name where it stayed strong AND where pacing let it fade. "
                   "Committing to a whole-essay prediction is what surfaces the fade the opening hides.")),
        Slot("TEACH", "stimulus_display", "Read the source: water for food or power?",
             ref="ACC-W910-ARG-LESSON-WATERTRADEOFF", bank="automation_policy",
             body=("Read this source on protecting scarce water for growing food or for generating power. You "
                   "will write a full argument essay from it under your own budget, then predict its scores "
                   "across the rows before the grader returns them. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + check tool, then discrimination + predict =====
        Slot("MODEL", "annotated_before_after", "Watch an opening-only prediction become a whole-essay one",
             bank="automation_policy",
             body=("Here is the difference between coasting on the strong start and predicting across the whole "
                   "essay. Read the BEFORE, then the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE predicts from the strong opening. The AFTER predicts across the essay and names "
                   "the pacing gap. Predicting across the essay is the move." + REMEMBER +
                   "When you predict your own scores, run this check before you submit.")),
        Slot("MODEL", "discrimination", "Which self-prediction can be compared to the grader?",
             ref="", labeled_grade_c=True, bank="automation_policy",
             body=("You have watched an opening-only prediction rebuilt into a whole-essay one. Now spot the "
                   "target: which prediction covers the WHOLE essay, and which reads only the OPENING? "
                   "(A) I predict a top score on every row, because my introduction was sharp and my first body "
                   "paragraph laid out strong, clearly organized evidence that read cleanly and made a confident "
                   "early impression.  "
                   "(B) I predict Evidence 2 and no Sophistication, because the opening was strong but my third "
                   "body paragraph ran thin and my ending was cut short, so the case faded before it landed.  "
                   "(C) I predict a high overall score, because the essay opened with a polished, confident "
                   "first paragraph that set an impressive tone and showed the grader right away that I "
                   "understood the whole prompt. "
                   "Correct: B covers the whole essay, including the parts pacing tends to hurt, and names the "
                   "late fade. A and C predict from the strong start only and miss the fade."),
             choices=[
                 {"id": "A", "text": "I predict a top score on every row, because my introduction was sharp and my first body paragraph laid out strong, clearly organized evidence that read cleanly and made a confident early impression.",
                  "correct": False,
                  "why": "This reads the opening only. A sharp intro and first paragraph are not the whole essay; the prediction never looks at the late paragraphs or the ending, where pacing costs points."},
                 {"id": "B", "text": "I predict Evidence 2 and no Sophistication, because the opening was strong but my third body paragraph ran thin and my ending was cut short, so the case faded before it landed.",
                  "correct": True,
                  "why": "Correct. This predicts each row from the whole essay, names the specific parts that faded, and can be compared to the grader row by row."},
                 {"id": "C", "text": "I predict a high overall score, because the essay opened with a polished, confident first paragraph that set an impressive tone and showed the grader right away that I understood the whole prompt.",
                  "correct": False,
                  "why": "This still predicts from the strong start. A polished opening tells you nothing about the rushed third paragraph and the ending that pacing usually hurts."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this self-prediction most need?",
             bank="automation_policy",
             body=("Diagnose before the reveal. A student wrote: 'I nailed it, the beginning was so strong.' "
                   "Which single move would most improve the prediction? "
                   "(A) predict each row from the WHOLE essay, including the late paragraphs and the conclusion, "
                   "and give a reason for each  "
                   "(B) praise the strong introduction and first paragraph even more, since those are the parts "
                   "that made the best impression on the reader  "
                   "(C) predict a higher overall score, because the opening was polished and the essay started "
                   "off sounding confident, clear, and well organized  "
                   "(D) ignore the rushed ending and the thin conclusion, and judge the essay mainly on how well "
                   "its first half was written"),
             feedback=("Correct: A. A strong start is not the whole essay. The fix predicts each row from the "
                       "full piece, including the parts pacing tends to hurt. Praising the intro (B), a higher "
                       "guess (C), or ignoring the ending (D) all repeat the opening-only error.")),

        # ===== SUPPORTED: predict a sample full-write then reveal (K2), then write + predict with a frame =====
        Slot("SUPPORTED", "self_score", "Predict a sample full-write, then see the grader",
             ref="", bank="automation_policy",
             body=("Predict, then reveal. Sample essay: a strong situated intro and first paragraph, a shorter "
                   "second, a one-line third, and no conclusion (the budget ran out). Predict its Sophistication "
                   "row, then check the reveal."),
             choices=[
                 {"id": "no", "text": "Sophistication no, the tension faded at the end",
                  "correct": True,
                  "why": "Correct. The strong start cannot offset a thin third paragraph and a missing conclusion. The Sophistication row needs the trade-off held to the end, and the pacing fade breaks it. Predicting from the whole essay catches this; predicting from the opening does not."},
                 {"id": "yes", "text": "Sophistication yes, the opening was excellent",
                  "correct": False,
                  "why": "Look again. A strong opening is not the whole essay. The grader also reads the thin third paragraph and the missing conclusion, and the tension dropped at the end, so this row scores no. That is the opening-only pull."},
             ]),
        Slot("SUPPORTED", "production_frq", "Write a full essay, then predict its scores",
             ref="", bank="automation_policy", rubric_ref="rc.ap", scored=True, unit="essay",
             body=frq_prompt(
                 intro="Under your own budget, write a full argument essay on the water trade-off end to end, "
                       "then predict its scores using this frame.",
                 setapart_block=setapart("Fill in this prediction frame:",
                                         "Evidence __ because __ (name the part). Sophistication yes/no because __ (name where the tension held or faded)."),
                 closer="Write the complete essay first (introduction, body paragraphs, conclusion). Then fill "
                        "the frame with a reason for each row drawn from the WHOLE essay. The grader will score "
                        "the essay; your prediction is what you will compare against.")),

        # ===== INDEPENDENT: calibrate a full-write cold (no frame) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Calibrate a full-write on your own",
             ref="", bank="automation_policy", rubric_ref="rc.ap", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now, no frame. Under your own budget, write a fresh full essay on the water "
                       "trade-off.",
                 closer="Predict your scores across the rows with a reason for each drawn from the whole essay, "
                        "and after the grader returns them, name the gap and whether pacing caused it. Predicting "
                        "your own full-write from the whole piece is what every calibrated writer is built on, "
                        "and you are ready to do it cold. Take the budget you need.")),

        # ===== DIAGNOSIS = run the gap-naming check on the student's OWN just-written draft (self-revision) =====
        Slot("MODEL", "diagnosis_frq", "Name the gap, and whether pacing caused it",
             ref="", bank="automation_policy", scored=True,
             body=frq_prompt(
                 intro="Here is what naming a gap looks like. This example runs the check on one essay:",
                 checklist_block=checklist(title="Example: naming a gap", rows=[
                     ("Where did the essay meet the row?", "The intro and body one held the trade-off in tension, so the start earned the prediction."),
                     ("Where did it miss?", "Body three flattened into one side and the conclusion was cut, so the tension dropped at the end."),
                     ("Did PACING cause the miss?", "Yes. The late fade, not a thinking error, is what cost the row; the writer ran out of budget."),
                 ]),
                 closer="Now run this same check on YOUR draft. Reread the essay you just wrote, name each gap "
                        "between your predicted rows and the grader's rows, and fix any line that fails. Flag any "
                        "gap caused by pacing, then name your single biggest pacing gap. If your prediction "
                        "matched and pacing held, say so and name the row you were most at risk of missing.")),
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
