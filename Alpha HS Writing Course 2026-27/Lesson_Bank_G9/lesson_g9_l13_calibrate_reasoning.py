"""
lesson_g9_l13_calibrate_reasoning.py  -  G9 KC C.9.03, ARCHETYPE T5: RUBRIC-REVISION (CHECK, ceiling paragraph).

G9 course L13. CHECK capstone of the reasoning work (U2): calibrate reasoning on a PROVIDED draft - predict
whether a draft's warrant really explains WHY, see the reveal, then revise the provided draft. Recycles W1/W2
+ P1. Locked L01 template. REVISION-TIER: the material is the PROVIDED DRAFT (inline in the stem), so it binds
a lightweight issue_frame for topical context, NOT a full source. Taught: FRAME-VOLCANOES -> transfer:
FRAME-WATER-CYCLE (bank-partitioned). rc.staar, unit="sentence". CHECK=proposal. Calibration engine =
predict-then-reveal (self_score precedes the graded reveal). No coping-model persona; no source markup; no
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
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> a warrant that only restates</span>'
    '<p style="margin:8px 0 0;font-size:15px">Volcanoes are dangerous because they are risky to people who '
    'live near them.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The because-clause just repeats the claim '
    '("dangerous because risky"). It names no real reason, so the reasoning is empty. A restating warrant '
    'scores in the low band.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> a warrant that explains the real reason</span>'
    '<p style="margin:8px 0 0;font-size:15px">Volcanoes are dangerous '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">REAL REASON</span> because an eruption can send ash, gas, and molten rock over nearby '
      'towns with little warning, giving residents little time to escape.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Now the because-clause gives a real reason (what '
    'an eruption actually does), not a restatement. That is a warrant that earns its score.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C903-0013", grade="9-10", lesson_type=5,
    unit="G9 U2 - Reasoning (calibrate + revise reasoning on a provided draft)",
    title="Check the Reasoning: Does the Warrant Really Explain?",
    target=("Judge whether a provided draft's warrant truly explains WHY (or only restates the claim), predict "
            "its score, see the reveal, then revise the draft so the reasoning explains. Written at the "
            "sentence. Trait: Evidence/Development (reasoning)."),
    acc_tags=["ACC.W.ARG.2", "CCSS.W.9-10.1b", "CCSS.W.9-10.5"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12",
                "mnemonic_status": "proposal", "kc": "C.9.03", "sot": "icm course-G9.md L13",
                "taught_stimulus": "ACC-W910-FRAME-VOLCANOES",
                "transfer_stimulus": "ACC-W910-FRAME-WATER-CYCLE",
                "playbook": "_phase2/playbook_T5_CHECK.md",
                "template": "locked L01 template; REVISION-TIER binds a lightweight issue_frame (the material is the provided draft, inline).",
                "council": ("T5/CHECK capstone of the reasoning unit: calibration engine = predict-then-reveal "
                            "(self_score precedes graded reveal); revise a PROVIDED draft's warrant; "
                            "restates-vs-explains discrimination labeled Grade-C. CHECK=proposal; self-"
                            "assessment ES ~0.62, over-estimation bias ~0.206 (not SRSD live ES).")},
    fade_ledger_moves=["calibrate-predict-then-reveal", "revise-empty-warrant-to-real-reason"],
    slots=[
        Slot("TEACH", "teach_card", "A warrant must explain, not just repeat",
             body=("You have written warrants; now learn to CHECK them. The most common weak warrant does not "
                   "explain anything, it just restates the claim in new words. 'Volcanoes are dangerous because "
                   "they are risky' says the same thing twice, so a reader learns no reason. A real warrant "
                   "gives the actual reason: 'dangerous because an eruption can bury nearby towns in ash and "
                   "molten rock.' The test for any warrant is one question: after the word because, is there a "
                   "NEW reason, or just the claim again? If it is the claim again, the warrant is empty and "
                   "scores low. Today you will judge warrants, predict their scores, see the real score, and "
                   "then repair a weak one. Predicting first and then checking against the reveal is how you "
                   "train your eye, because writers usually rate their own reasoning higher than a scorer "
                   "would.")),
        Slot("TEACH", "teach_card", "How the check works: predict, reveal, repair",
             body=("Here is the routine you will run. First, CHECK the warrant against one criterion: does the "
                   "because-clause give a real reason, or restate the claim? Second, PREDICT the score, is this "
                   "a strong warrant or a weak one? Third, see the REVEAL, the real score and why. Fourth, "
                   "REPAIR, rewrite a weak warrant so it explains. Predicting before you see the answer matters: "
                   "it forces you to commit, so the reveal actually teaches you where your eye was off. Scorers "
                   "and students often disagree because students read their own reasoning generously, so "
                   "practicing the prediction closes that gap.")),
        Slot("TEACH", "stimulus_display", "The topic: volcanoes",
             ref="ACC-W910-FRAME-VOLCANOES", bank="volcanoes",
             body=("The drafts you will check are about volcanoes. Read this short orientation so the topic is "
                   "familiar. You are not writing about volcanoes from scratch here; you are checking and "
                   "repairing reasoning in drafts that are given to you.")),
        Slot("TEACH", "discrimination", "Which warrant explains, and which only restates?",
             ref="", labeled_grade_c=True, bank="volcanoes",
             body=("Sort these before you check on your own (spotting the target first, a Grade-C design bet we "
                   "label as a bet, not a proven ingredient). Both answer the same claim. Which warrant EXPLAINS "
                   "the reason, and which only RESTATES the claim? "
                   "(A) Volcanoes are dangerous because they are risky, unsafe, and hazardous places that "
                   "can end up hurting the people living nearby.  "
                   "(B) Volcanoes are dangerous because an eruption can send ash, gas, and molten rock over "
                   "nearby towns with little warning. "
                   "Correct: B explains; A restates. (A) says 'dangerous because risky,' which repeats the "
                   "claim and gives no new reason. (B) names what an eruption actually does, so it is a real "
                   "warrant. The empty warrant (A) is the low-band trap this lesson trains you to catch.")),
        Slot("MODEL", "annotated_before_after", "Watch an empty warrant get repaired",
             bank="volcanoes",
             body=("Here is a restating warrant being repaired into one that explains. Read the BEFORE, then "
                   "the AFTER, and notice the empty because-clause replaced with a real reason."
                   + BEFORE_AFTER_HTML +
                   " The BEFORE repeats the claim. The AFTER gives the actual reason an eruption is dangerous. "
                   "Replacing the restatement with a real reason is the repair.")),
        Slot("MODEL", "predict_the_fix", "Predict: is this warrant strong or weak, and why?",
             bank="volcanoes",
             body=("Predict before the reveal. A draft reads: 'Volcanoes should be monitored because watching "
                   "them is a good idea.' Which single judgment is correct? "
                   "(A) weak, the because-clause restates the claim ('monitored because watching is good') and "
                   "gives no real reason  "
                   "(B) strong, the because-clause clearly explains why monitoring matters and gives the reader a real, useful reason  "
                   "(C) weak, but only because it is too short; adding a few more words about monitoring would make the reasoning strong  "
                   "(D) strong, because it uses the word because, which signals to the reader that a genuine reason is being given"),
             feedback=("Correct: A. The warrant is weak because its because-clause just repeats the claim: "
                       "'monitored because watching them is good' is the same idea twice, with no real reason. "
                       "Length (C) is not the problem, and using the word because (D) does not make reasoning "
                       "real. A repair would give the reason: 'because early signs like small quakes and "
                       "swelling ground can warn a town before an eruption.' Predicting weak here trains your "
                       "eye for the empty-warrant trap.")),
        Slot("SUPPORTED", "self_score", "Score it yourself, then see the real score",
             ref="", bank="volcanoes",
             body=("Predict, then reveal. Here is a draft warrant: 'Volcanic ash is harmful because it is bad "
                   "for people.' On a simple 2-point scale (2 = explains a real reason, 1 = only restates), "
                   "what score would you give it? Commit to your prediction, then read the reveal. Reveal: this "
                   "scores 1. 'Harmful because it is bad' restates the claim, it names no real reason. A 2 "
                   "would explain the reason, for example 'because breathing ash can damage the lungs and "
                   "clog engines and water supplies.' If you predicted 2, notice the pull to over-rate a "
                   "warrant that sounds fine but explains nothing.")),
        Slot("SUPPORTED", "production_frq", "Repair the weak warrant",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("Revise this provided draft so the warrant explains: 'Volcanic ash is harmful because it is "
                   "bad for people.' Rewrite it in one sentence so the because-clause gives a REAL reason (what "
                   "ash actually does), not a restatement. Goal: keep the claim, replace the empty reason with "
                   "a real one. Scored on Evidence/Development.")),
        Slot("MODEL", "diagnosis_frq", "Run the check on a fresh warrant",
             ref="", bank="volcanoes", scored=True,
             body=("First watch the check run on a provided draft, then run it on a fresh warrant of your own. "
                   "Provided draft: 'Living near a volcano is risky because it is dangerous.' Run the check "
                   "step by step. Step 1, Criterion: does the because-clause give a real reason? No, 'risky "
                   "because dangerous' restates. Step 2, so the score is low; the repair is to name the real "
                   "reason (lava flows, ashfall, sudden eruptions). Now you: write one fresh warrant sentence "
                   "about volcanoes, then run the same check on it, does your because-clause explain or "
                   "restate? Use the fix if needed: replace any restatement with a real reason. Finish by "
                   "naming whether your warrant explains or still restates.")),
        Slot("INDEPENDENT", "production_frq", "Revise a provided draft on your own",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("On your own now. Here is a provided draft: 'Volcanoes are worth studying because studying "
                   "them is important.' Revise it in one sentence so the warrant explains a REAL reason, not a "
                   "restatement. Before you submit, run the check on your revision: after because, is there a "
                   "new reason, or the claim again? If it restates, fix it before you submit. Scored on "
                   "Evidence/Development.")),
        Slot("TRANSFER", "stimulus_display", "The topic: the water cycle",
             ref="ACC-W910-FRAME-WATER-CYCLE", bank="water_cycle",
             body=("The next draft to check is about the water cycle. Read this short orientation so the topic "
                   "is familiar. Again, you are checking and repairing a provided draft's reasoning, not "
                   "writing from scratch.")),
        Slot("TRANSFER", "production_frq", "Revise a provided draft on a NEW topic",
             ref="", bank="water_cycle", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("New topic. Here is a provided draft: 'The water cycle is important because it matters a "
                   "lot.' Revise it in one sentence so the warrant explains a REAL reason (what the cycle "
                   "actually does), not a restatement. Same check-and-repair move as the volcano drafts, new "
                   "topic. Scored on Evidence/Development.")),
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
