"""
lesson_g12_l07_calibrate_sophistication.py  -  G12 KC C.12.01, ARCHETYPE T8 (cross-source-synthesis, WEAVE,
essay ceiling) with a K2 own-work CALIBRATION overlay on AP Sophistication (Row C). V3.1.

G12 course L07 (Unit 1, calibration). Teaching point (KEPT): predict whether your OWN essay earns the
sophistication point (Row C) with a reason tied to the CRITERION, submit it, then name the GAP between your
prediction and the grader, rather than guessing from feel. Written at the essay. Stateless-safe (fresh writing
routed to the grader; no reference to prior submissions).

Preserved EXACTLY from the prior L07: id="ACC-W910-L-G12-C1201-0007", lesson_type=8, mnemonic_status="proposal",
kc="C.12.01", the unit, the bound stimuli (WORKFORCEINVEST taught, bank=public_health -> WATERTRADEOFF transfer,
bank=automation_policy), and the essay-tier unit on every scored production.

V3.1 rebuild (the prose-wall PRE-v3.1 version -> the v3.1 spine):
  1. TEACH is now a ONE_IDEA teal callout + real <ul>/<ol> lists (no >45-word prose block); "thesis" is defined
     in plain words before use (define_before_use / format_fidelity).
  2. The leaked internal label ("a Grade-C design bet we label as a bet") is GONE from the discrimination; it is
     a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}] and the reveal in a
     "Correct: A ..." tail, not inside an option (leaked_internal_label / leaked_answer_cue).
  3. Coping-model BEFORE/AFTER kept (feel-guess -> criterion prediction, gap named), plus a REMEMBER dashed box
     with a real 3-question <ol> check tool folded in at first use.
  4. Deterministic FRQ + diagnosis bodies via frq_prompt/setapart/checklist (no "Step 1/Step 2" prose, no
     "Scored on ..." chrome). Own words, faithful to the bound federal sources, no fabricated figures, no em dashes.
Passes all 23 lesson_contract gates + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">You can predict your own <strong>Row C</strong> result '
'before the grader does, but only if you predict against the actual <strong>criterion</strong>, not against a '
'feeling. "It sounded smart" is not the test; "the tension was held across the whole essay" is.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: calibrate the prediction</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before and after the grader returns, ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Did I predict yes or no against the Row C criterion (situated question plus tension held throughout), not a feeling?</li>'
'<li style="margin:2px 0">Did I point to the exact place in my essay that meets or misses it?</li>'
'<li style="margin:2px 0">After the reveal, can I name the specific gap between my prediction and the grader?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, your read was a feel-guess, not a calibration.</div></div>')

# coping-model before/after: a feel-guess rebuilt into a prediction tied to the Row C criterion, with the gap
# named after the reveal. Contains BOTH a literal BEFORE and AFTER (content_depth). No named person.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> a feel-guess about sophistication</span>'
    '<p style="margin:8px 0 0;font-size:15px"><i>First try:</i> I think I earned the sophistication point '
    'because my essay sounded smart and used some big ideas.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">"Sounded smart" is not the Row C criterion. The '
    'grader looks for a situated question and a real tension held across the whole essay, not a tone.</p>'
  '</div>'
  '<div style="background:#fffbeb;padding:12px 14px;border-bottom:1px solid #fde68a">'
    '<span style="display:inline-block;background:#d97706;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">SECOND TRY</span>'
    '<span style="color:#92400e;font-size:13px;font-weight:600"> runs the check against the criterion</span>'
    '<p style="margin:8px 0 0;font-size:15px">Did I situate the question in the broader tension? Yes. Did I '
    'hold that tension across every body paragraph? Body two dropped it and just called the other side wrong.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> predicts on the criterion, then names the gap</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">PREDICT + REASON</span> I predict no Row C: I situated the question but flattened the '
      'tension in body two. '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">GAP</span> The grader agreed, no Row C; the gap is that one flattened paragraph sank the '
      'sophistication for the whole essay.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same essay, but now the read is tied to the Row C '
    'criterion and points to the exact paragraph that missed it. That is calibration on sophistication.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G12-C1201-0007", grade="9-10", lesson_type=8,
    unit="G12 U1 - Calibrate your own sophistication (predict, grader-reveal, name the gap)",
    title="Predict Whether You Earned Sophistication, Then Name the Gap",
    target=("Predict whether your own essay earns the sophistication point (Row C) with a reason tied to the "
            "criterion, submit it, then name the gap between your prediction and the grader, rather than "
            "guessing from feel. Written at the essay. Trait: self-assessment against Sophistication (Row C)."),
    acc_tags=["ACC.W.PROD.3", "CCSS.W.11-12.5"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.12.01", "sot": "icm course-G12.md L07",
                "taught_stimulus": "ACC-W910-ARG-LESSON-WORKFORCEINVEST",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-WATERTRADEOFF",
                "playbook": "_phase2/playbook_T5_CHECK.md",
                "template": ("v3.1 spine; binds G12 argument LESSON sources; K2 own-work calibration on Row C is "
                             "stateless-safe; lesson_type=8 because the calibration operates on a full essay "
                             "(essay ceiling)."),
                "one_idea": "You can predict your own Row C before the grader, if you predict against the criterion, not a feeling.",
                "one_reminder": "Calibrate check: predicted against the Row C criterion (not feel)? pointed to the exact place? can name the gap?",
                "version_note": ("V3.1 rebuild of L07 (PRE-v3.1 prose walls -> the spine). Removed the leaked "
                                 "internal label ('a Grade-C design bet we label as a bet') from the "
                                 "discrimination and moved options to explicit choices=[]; broke the wall-of-text "
                                 "teach cards into a ONE_IDEA callout + real <ul>/<ol> lists (format_fidelity); "
                                 "defined 'thesis' before use; folded a REMEMBER 3-question check tool in at "
                                 "first use; deterministic frq_prompt/setapart/checklist bodies (no 'Step 1/2' "
                                 "prose). Preserved id, type 8, mnemonic_status=proposal, kc C.12.01, bound "
                                 "stimuli, and the essay unit on every scored production."),
                "council": ("T8/WEAVE G12 own-work calibration (K2, map role = check): predict-own-Row-C -> "
                            "grader-reveal -> name-gap on a sophisticated essay. self_score calibration enforced "
                            "by the judge-then-reveal gate. unit=essay. Stateless-safe.")},
    fade_ledger_moves=["predict-own-sophistication", "name-the-gap-on-row-c"],
    slots=[
        # ===== TEACH: the one idea + what the Row C criterion is (as a list), then the routine (as a list) =====
        Slot("TEACH", "teach_card", "The one idea: predict against the criterion, not the feeling",
             body=(ONE_IDEA +
                   "A mastery writer can call the sophistication point before the grader does. Row C rewards a "
                   "consistently sophisticated argument, and it has parts you can check:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Situate the question</strong>: the thesis question sits "
                   "inside a broader frame or tension, not on its own. A thesis is a one-sentence claim that "
                   "states your position, and your whole essay defends it.</li>"
                   "<li style=\"margin:4px 0\"><strong>Hold the tension</strong>: a real tension is carried, not "
                   "flattened, across every body paragraph. One paragraph that dismisses the other side as 'just "
                   "wrong' breaks it.</li>"
                   "<li style=\"margin:4px 0\"><strong>Carry it throughout</strong>: Row C is holistic, so a "
                   "strong opening plus one flat paragraph is inconsistent and falls short.</li></ul>"
                   "The weak move is guessing from feel ('it sounded smart', 'I worked hard'). Predict against "
                   "the criterion instead.")),
        Slot("TEACH", "teach_card", "The routine: predict, submit, name the gap",
             body=("Run this routine on your own essay. Follow it in order and the calibration teaches you where "
                   "your read is off:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>PREDICT</strong>: Row C yes or no, with the reason from "
                   "your text ('no, because body two flattened the tension').</li>"
                   "<li style=\"margin:4px 0\"><strong>SUBMIT</strong>: send the essay to the grader, which "
                   "scores the sophistication.</li>"
                   "<li style=\"margin:4px 0\"><strong>READ THE REVEAL</strong>: see the grader's Row C result.</li>"
                   "<li style=\"margin:4px 0\"><strong>NAME THE GAP</strong>: if your prediction and the grader "
                   "differ, say what you misjudged ('I thought one clever line earned it; Row C needs the "
                   "sophistication carried throughout').</li></ol>"
                   "Committing to a criterion-based prediction before the reveal is what surfaces the blind spot; "
                   "a feel-guess hides it.")),
        Slot("TEACH", "stimulus_display", "Read the source: prepare workers or protect them?",
             ref="ACC-W910-ARG-LESSON-WORKFORCEINVEST", bank="public_health",
             body=("Read this source on whether a society should invest first in preparing more people for "
                   "fast-growing technical fields or first in protecting the workers the change leaves behind. "
                   "Because you will write a sophisticated argument on it and then predict your own Row C result, "
                   "read for the larger question and the real tension between the future workforce and the "
                   "present one. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + the check tool, then discrimination =====
        Slot("MODEL", "annotated_before_after", "Watch a feel-guess become a criterion-based prediction",
             bank="public_health",
             body=("Here is a feel-guess rebuilt into a prediction tied to the Row C criterion, with the gap "
                   "named after the reveal. Read the BEFORE, then the SECOND TRY, then the AFTER." +
                   BEFORE_AFTER_HTML +
                   " The BEFORE guesses from feel. The AFTER predicts against the criterion and names the exact "
                   "gap. Predicting on the criterion is the move." + REMEMBER +
                   "When you predict your own Row C, run this check first, then name the gap after the grader returns.")),
        Slot("MODEL", "discrimination", "Which self-prediction can be compared against the grader?",
             ref="", labeled_grade_c=True, bank="public_health",
             body=("You have watched a feel-guess become a criterion-based prediction. Now spot the target: "
                   "which self-prediction is tied to the Row C criterion, so it can actually be checked against "
                   "the grader? "
                   "(A) I predict no Row C: I situated the question in the broader tension but flattened it in "
                   "one body paragraph, and Row C needs it held throughout.  "
                   "(B) I think I earned Row C because the essay sounded genuinely smart, used ambitious "
                   "vocabulary, and honestly felt deep and impressive to me the whole time I was writing it.  "
                   "(C) I predict Row C because I worked hard on this piece, spent a long time revising every "
                   "paragraph, and it came out longer and more polished than my usual drafts. "
                   "Correct: A. It predicts against the actual criterion (situate the question, hold the tension "
                   "throughout) and points to the exact place it misses. B rests on tone and word choice; C "
                   "rests on effort and length. Neither B nor C is the Row C criterion, so neither can be "
                   "compared against the grader."),
             choices=[
                 {"id": "A", "text": "I predict no Row C: I situated the question in the broader tension but flattened it in one body paragraph, and Row C needs it held throughout.",
                  "correct": True,
                  "why": "Correct. This predicts against the actual Row C criterion (situate the question, hold the tension throughout) and points to the exact paragraph that misses it, so it can be checked against the grader."},
                 {"id": "B", "text": "I think I earned Row C because the essay sounded genuinely smart, used ambitious vocabulary, and honestly felt deep and impressive to me the whole time I was writing it.",
                  "correct": False,
                  "why": "This rests on tone and word choice, not the criterion. 'Sounded smart' is a feeling, so there is nothing specific to compare against the grader."},
                 {"id": "C", "text": "I predict Row C because I worked hard on this piece, spent a long time revising every paragraph, and it came out longer and more polished than my usual drafts.",
                  "correct": False,
                  "why": "Effort, time, and length are not the Row C criterion. A holistic point is not earned by how hard the draft was, so this cannot be checked against the grader."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this self-prediction most need?",
             bank="public_health",
             body=("Diagnose before the reveal. A student wrote: 'I probably got the sophistication point "
                   "because I worked hard and it felt deep.' Which single move would most improve the "
                   "prediction? "
                   "(A) predict yes or no against the Row C criterion (situated question plus tension held "
                   "throughout) and cite the reason from the essay  "
                   "(B) predict yes with even more confidence, since the essay already felt quite deep and used "
                   "plenty of big, smart-sounding ideas all the way through to the end  "
                   "(C) describe how many hours went into the draft and how much effort the whole thing took, "
                   "and let that stand in for the actual prediction of the result  "
                   "(D) skip predicting anything at all and simply wait for the grader to reveal the Row C "
                   "result and explain the reasoning for you"),
             feedback=("Correct: A. Effort and 'felt deep' (B, C) are not the Row C criterion, and skipping the "
                       "prediction (D) throws away the calibration. The fix predicts against the actual "
                       "criterion and cites the specific place the essay meets or misses it.")),

        # ===== SUPPORTED: calibration warmup (self_score, predict THEN reveal) + the framed production write =====
        Slot("SUPPORTED", "self_score", "Predict a sample essay's Row C, then see the grader",
             ref="", bank="public_health",
             body=("Predict, then reveal. Sample essay on the workforce prompt: it situates the choice in the "
                   "broader question and holds the tension in body one, but body two dismisses the other side as "
                   "'just wrong' and the conclusion only restates the position. Does it earn Row C?"),
             choices=[
                 {"id": "A", "text": "No: the sophistication is not carried throughout, so it falls short.",
                  "correct": True,
                  "why": "Correct. Row C is holistic: a strong opening plus one flattened paragraph and a flat conclusion is inconsistent, so it does not earn the point."},
                 {"id": "B", "text": "Yes: the situated question and the strong first body paragraph are enough.",
                  "correct": False,
                  "why": "A good start does not earn a holistic point. Row C needs the tension held across every body paragraph, and body two flattened it."},
             ]),
        Slot("SUPPORTED", "production_frq", "Write your essay, then predict its Row C",
             ref="", bank="public_health", rubric_ref="rc.ap", scored=True, unit="essay",
             body=frq_prompt(
                 intro="Write a sophisticated argument on the workforce prompt: situate the question in the "
                       "broader tension, and hold that tension throughout. Then predict your Row C result.",
                 setapart_block=setapart("Predict in one line:",
                                         "Row C yes or no, because ______ (name the exact place in your essay that meets or misses the criterion)."),
                 closer="The grader will score the sophistication; your one-line prediction is what you will "
                        "compare against it. Write the full essay, then the prediction.")),

        # ===== INDEPENDENT: calibrate cold, no frame + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Calibrate on your own",
             ref="", bank="public_health", rubric_ref="rc.ap", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now, with no frame.",
                 closer="Write a fresh sophisticated argument on the workforce prompt, predict your Row C result "
                        "against the criterion with a reason, and after the grader returns its score, name the "
                        "gap. Predicting against the Row C criterion and then naming the gap is what every "
                        "calibrated writer is built on, and you are ready to do it cold. Take the time you need.")),

        # ===== DIAGNOSIS = run the same 3-question check on your OWN just-written draft (scaffolded self-revision) =====
        Slot("MODEL", "diagnosis_frq", "Name the gap between your prediction and the grader",
             ref="", bank="public_health", scored=True,
             body=frq_prompt(
                 intro="Here is what naming a gap looks like:",
                 checklist_block=checklist(title="Example (naming a gap):", rows=[
                     ("Where did the essay meet the criterion?", "It situated the question in the broader tension."),
                     ("Where did it miss?", "One body paragraph flattened the tension, so the sophistication was not consistent."),
                     ("What was the blind spot?", "Counting the strong opening as enough for a holistic point."),
                 ]),
                 closer="Now do the same on YOUR draft: reread the essay you just wrote, run these three questions "
                        "on it, revise the weakest line, and finish by naming your single biggest gap and the one "
                        "change you made to close it.")),
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
