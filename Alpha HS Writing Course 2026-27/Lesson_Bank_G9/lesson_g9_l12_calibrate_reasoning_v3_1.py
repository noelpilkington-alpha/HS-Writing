"""
lesson_g9_l13_calibrate_reasoning_v3_1.py  -  G9 KC C.9.03, ARCHETYPE T5: RUBRIC-REVISION (CHECK, sentence). V3.1.

V3.1 rebuild of lesson_g9_l13_calibrate_reasoning.py, applying the v3.1 lesson build spec (see icm/_config/
v3_1-lesson-build-spec.md), the pattern G9 L01 cleared. Teaching point + KC + id + bound stimuli are UNCHANGED:
this is the CHECK capstone of the reasoning unit, a CALIBRATION / predict-then-reveal lesson. The student judges
whether a PROVIDED draft's WARRANT truly explains WHY the evidence supports the claim (or only restates the
claim), predicts its score, sees the reveal, then revises the draft so the reasoning explains. KC C.9.03.
Taught on VOLCANOES (lightweight issue_frame, because the material is the inline provided draft, not a full
source); transfer on WATER-CYCLE (partitioned). The calibration engine (self_score = predict THEN reveal) is
preserved, since it is what makes this lesson a CHECK.

V3.1 changes vs the prior L13:
  1. TEACH is now ONE idea, hammered: a teal ONE-IDEA box + the minimum teaching as LISTS (restate-vs-explain
     contrast, the one-question test), not the two prose walls the old teach cards were (143 and 99 words with
     no block break, which tripped format_fidelity). "warrant" is still defined in plain words in a TEACH body
     (define-before-use), with the cue word "is a".
  2. CLEAN DISCRIMINATION: explicit choices=[{id,text,correct,why}]; the internal "Grade-C design bet, labeled
     as a bet" jargon is GONE from the student text (the live leaked_internal_label fail), kept only as
     labeled_grade_c=True in code. All three options attach because to the same claim, so "because" cannot
     co-vary with the key (DI faultless communication); the correct option is not the lone longest.
  3. MODEL BEFORE THE QUIZ (KH worked-example effect): the discrimination now follows the model.
  4. COPING-MODEL THINK-ALOUD (SRSD): the model shows a writer running the CHECK routine (read the warrant,
     predict weak, confirm, repair) then the clean BEFORE/AFTER endpoints, then the reusable check tool. No peer.
  5. STRUCTURED FRQ/DIAGNOSIS bodies (lesson_prompts.frq_prompt/setapart/checklist): the old diagnosis was a
     "Step 1, ... Step 2, ..." prose run that render-QC flagged as double-numbering; it is now a real checklist.
     No "Scored on ..." rubric-trait chrome in any student-facing prompt (the grader knows the trait from the id).
  6. AUTONOMY + SAY-THE-STANDARD (Yeager) on the independent revise.

ONE IDEA: a real warrant explains WHY; an empty warrant only restates the claim. ONE REMINDER: the warrant check.
Passes all 23 lesson_contract gates + gated_reading render-QC. Own words, no fabricated figures, no em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A <strong>warrant</strong> is a reasoning sentence '
'that says <strong>WHY</strong> your evidence supports your claim. An <strong>empty</strong> warrant only '
'restates the claim in new words, so it explains nothing and scores low.</div></div>')

# coping-model think-aloud panel: a WRITTEN check routine (read -> predict weak -> confirm -> repair).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer checking a warrant, step by step:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>Read it:</strong> "Volcanoes are dangerous because they are risky." Run '
    'the check: after because, is there a NEW reason, or the claim again? "Risky" means the same as "dangerous," '
    'so it just says the claim twice. Predict: weak.</p>'
    '<p style="margin:0 0 8px"><strong>Confirm:</strong> weak is right. That because-clause restates the claim '
    'and names no reason, so the warrant is empty. Now repair it.</p>'
    '<p style="margin:0"><strong>Repair:</strong> "Volcanoes are dangerous because an eruption can send ash, '
    'gas, and molten rock over nearby towns with little warning." Now after because there is a real reason, what '
    'an eruption actually does. That passes.</p>'
  '</div>'
'</div>')

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

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the warrant check</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you score or submit any warrant, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Is there a causal word (because, since, or as)?</li>'
'<li style="margin:2px 0">After it, is there a NEW reason, or just the claim again?</li>'
'<li style="margin:2px 0">Does the reason name what actually happens?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If it is the claim again, the warrant is empty and scores low.</div></div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C903-0013", grade="9-10", lesson_type=5,
    unit="G9 U2 - Reasoning (calibrate + revise reasoning on a provided draft)",
    title="Check the Reasoning: Does the Warrant Really Explain?",
    target=("Judge whether a provided draft's warrant truly explains WHY (or only restates the claim), predict "
            "its score, see the reveal, then revise the draft so the reasoning explains. Written at the "
            "sentence. Trait: Evidence/Development (reasoning)."),
    acc_tags=["ACC.W.ARG.2", "CCSS.W.9-10.1b", "CCSS.W.9-10.5"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.9.03", "sot": "icm course-G9.md L13",
                "taught_stimulus": "ACC-W910-FRAME-VOLCANOES",
                "transfer_stimulus": "ACC-W910-FRAME-WATER-CYCLE",
                "playbook": "_phase2/playbook_T5_CHECK.md",
                "template": "locked L01 template; REVISION-TIER binds a lightweight issue_frame (the material is the provided draft, inline).",
                "one_idea": "A real warrant explains WHY; an empty warrant only restates the claim.",
                "one_reminder": "warrant check: causal word? new reason (not the claim again)? names what happens?",
                "version_note": ("V3.1: rebuilt to the v3.1 spec (pattern from G9 L01 v3.1). Teaching point, KC "
                                 "C.9.03, id, lesson_type 5, mnemonic_status proposal, sentence units, and bound "
                                 "stimuli unchanged. Split the two prose-wall teach cards into a ONE-IDEA box + "
                                 "lists (fixed format_fidelity); removed the leaked 'Grade-C design bet, labeled "
                                 "as a bet' jargon from the discrimination (fixed leaked_internal_label) and gave "
                                 "it explicit choices with all options carrying because so the token cannot cue "
                                 "the key; moved discrimination AFTER the model (KH); added a coping-model "
                                 "think-aloud of the check routine (SRSD); structured the FRQ/diagnosis bodies "
                                 "with frq_prompt/setapart/checklist (fixed the 'Step 1/Step 2' double-numbering "
                                 "render-QC fail) and dropped 'Scored on ...' chrome; kept the self_score "
                                 "predict-then-reveal calibration engine but moved its reveal into per-choice "
                                 "feedback so the prompt is short; autonomy + say-the-standard on the independent "
                                 "revise (Yeager)."),
                "council": ("T5/CHECK capstone of the reasoning unit: calibration engine = predict-then-reveal "
                            "(self_score precedes graded reveal); revise a PROVIDED draft's warrant; "
                            "restates-vs-explains discrimination labeled Grade-C. CHECK=proposal; self-"
                            "assessment ES ~0.62, over-estimation bias ~0.206 (not SRSD live ES)."),
                "review_provenance": "v3.1 spec rebuild; 23 lesson_contract gates + gated_reading render-QC clean."},
    fade_ledger_moves=["calibrate-predict-then-reveal", "revise-empty-warrant-to-real-reason"],
    slots=[
        # ===== TEACH: ONE idea only (ONE-IDEA box + lists; warrant defined with the cue word "is a") =====
        Slot("TEACH", "teach_card", "A warrant must explain, not just repeat",
             body=(ONE_IDEA +
                   "You have written warrants; now you learn to CHECK them. The most common weak warrant does "
                   "not explain anything, it just restates the claim in new words. Two sentences can both use "
                   "because, but only one reasons:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Restates (empty)</strong>: 'Volcanoes are dangerous "
                   "because they are risky.' That says the same idea twice, so a reader learns no reason.</li>"
                   "<li style=\"margin:4px 0\"><strong>Explains (a real warrant)</strong>: 'Volcanoes are "
                   "dangerous because an eruption can bury nearby towns in ash and molten rock.' That names the "
                   "actual reason.</li></ul>"
                   "The test for any warrant is one question: after the word because, is there a NEW reason, or "
                   "just the claim again? If it is the claim again, the warrant is empty and scores low. Today "
                   "you will judge warrants, predict their scores, see the real score, then repair a weak one.")),
        Slot("TEACH", "stimulus_display", "The topic: volcanoes",
             ref="ACC-W910-FRAME-VOLCANOES", bank="volcanoes", tag="buy_in",
             body=("The drafts you will check are about volcanoes. Read this short orientation so the topic is "
                   "familiar. You are not writing about volcanoes from scratch here; you are checking and "
                   "repairing reasoning in drafts that are given to you.")),

        # ===== MODEL (before the quiz): coping-model check routine + clean before/after + the check tool. =====
        Slot("MODEL", "annotated_before_after", "Watch an empty warrant get checked and repaired",
             bank="volcanoes",
             body=("Here is the check in action. Follow the writer's thinking, then read the clean before and "
                   "after. " + COPING_HTML + BEFORE_AFTER_HTML +
                   " Notice the one move that turned the BEFORE into the AFTER: the writer stopped restating and "
                   "gave a real reason, what an eruption actually does. " + REMEMBER +
                   "When you judge or repair a warrant, run these questions before you commit.")),
        Slot("MODEL", "discrimination", "Which warrant explains, and which only restates?",
             ref="", labeled_grade_c=True, bank="volcanoes",
             body=("Now that you have seen one checked, spot the target. All four attach because to the same "
                   "claim. Which one is a real warrant, the sentence that EXPLAINS why volcanoes are dangerous, "
                   "not one that only RESTATES the claim? "
                   "(A) Volcanoes are dangerous because they are risky, unsafe, and genuinely hazardous places that can end up seriously hurting the people who happen to live somewhere close by.  "
                   "(B) Volcanoes are dangerous because an eruption can send ash, gas, and molten rock over nearby towns with little warning.  "
                   "(C) Volcanoes are dangerous because a government science agency has counted a large number of active volcanoes sitting close to where many people live.  "
                   "(D) Volcanoes are dangerous because most people find them frightening and feel nervous whenever they live somewhere near one. "
                   "Correct: B. It names what an eruption actually does, so it explains WHY. (A) uses because but "
                   "only restates the claim ('dangerous because risky'), so it explains nothing. (C) states a "
                   "fact with because but never says why that fact makes a volcano dangerous, so it stops at "
                   "claim-plus-fact. (D) names how people feel about volcanoes, not what a volcano actually does, so it explains nothing real."),
             choices=[
                 {"id": "A", "text": "Volcanoes are dangerous because they are risky, unsafe, and genuinely hazardous places that can end up seriously hurting the people who happen to live somewhere close by.",
                  "correct": False,
                  "why": "This has because, but it only restates the claim ('dangerous because risky, unsafe, hazardous'). Restating the claim in new words is not reasoning, so the warrant is empty and scores low."},
                 {"id": "B", "text": "Volcanoes are dangerous because an eruption can send ash, gas, and molten rock over nearby towns with little warning.",
                  "correct": True,
                  "why": "Correct. It names what an eruption actually does, so it explains WHY volcanoes are dangerous. That real reason is the warrant, not any single word like because."},
                 {"id": "C", "text": "Volcanoes are dangerous because a government science agency has counted a large number of active volcanoes sitting close to where many people live.",
                  "correct": False,
                  "why": "This drops in a fact with because but never says why that fact makes a volcano dangerous. It stops at claim-plus-fact, so the reasoning, the why, is still missing."},
                 {"id": "D", "text": "Volcanoes are dangerous because most people find them frightening and feel nervous whenever they live somewhere near one.",
                  "correct": False,
                  "why": "This gives a reason, but the reason is how people feel about volcanoes, not what a volcano actually does. A fear is not the physical cause of the danger, so the warrant explains nothing real."},
             ]),
        Slot("MODEL", "discrimination", "Find the warrant that truly explains", ref="",
             labeled_grade_c=True, bank="volcanoes",
             body=("A fresh claim to check: people near an active volcano should keep an emergency kit ready. "
                   "All four warrants use because. Which one EXPLAINS why the kit matters, instead of only "
                   "restating the claim or answering a different question? "
                   "(A) People near an active volcano should keep an emergency kit ready because an eruption can cut off power and clean water for days, so stored supplies let a family last until help arrives.  "
                   "(B) People near an active volcano should keep an emergency kit ready because being prepared is just what keeping a ready kit is all about.  "
                   "(C) People near an active volcano should keep an emergency kit ready because volcanoes have erupted many times all across the world throughout recorded human history, on nearly every inhabited continent.  "
                   "(D) People near an active volcano should keep an emergency kit ready because a good kit usually holds bottled water, canned food, a flashlight, and a small first aid pack. "
                   "Correct: A. It names what an eruption actually does, cutting off power and water, and links that "
                   "to why the kit matters. (B) loops the claim back on itself: prepared because a kit is for being "
                   "prepared says nothing new. (C) states a true fact about eruptions but answers a different "
                   "question, how often they happen, not why a family needs supplies. (D) describes what a kit holds, not why keeping one ready near a volcano matters."),
             choices=[
                 {"id": "A", "text": "People near an active volcano should keep an emergency kit ready because an eruption can cut off power and clean water for days, so stored supplies let a family last until help arrives.",
                  "correct": True,
                  "why": "Correct. It names what an eruption actually does, cutting off power and clean water, and links that to why the kit matters, so it gives a real reason instead of repeating the claim."},
                 {"id": "B", "text": "People near an active volcano should keep an emergency kit ready because being prepared is just what keeping a ready kit is all about.",
                  "correct": False,
                  "why": "This loops the claim back on itself: prepared because a kit is for being prepared says the same idea twice and names no real reason."},
                 {"id": "C", "text": "People near an active volcano should keep an emergency kit ready because volcanoes have erupted many times all across the world throughout recorded human history, on nearly every inhabited continent.",
                  "correct": False,
                  "why": "This states a true fact about eruptions but answers a different question, how often they happen, not why a family needs supplies, so the reason never connects to the claim."},
                 {"id": "D", "text": "People near an active volcano should keep an emergency kit ready because a good kit usually holds bottled water, canned food, a flashlight, and a small first aid pack.",
                  "correct": False,
                  "why": "This describes what is inside a kit, not why keeping one ready near a volcano matters. Listing the contents is not the reason, so the warrant never explains why the claim holds."},
             ]),
        Slot("MODEL", "predict_the_fix", "Predict: is this warrant strong or weak, and why?",
             bank="volcanoes",
             body=("Predict before the reveal. A draft reads: 'Volcanoes should be monitored because watching "
                   "them is a good idea.' Which single judgment is correct? "
                   "(A) weak, the because-clause restates the claim ('monitored because watching is good') and gives no real reason  "
                   "(B) strong, the because-clause clearly explains why monitoring matters and hands the reader a genuinely useful, concrete reason to accept it  "
                   "(C) weak, but only because it is a little too short; adding a few more descriptive words about monitoring would make the reasoning strong enough  "
                   "(D) strong, because it uses the signal word because, which by itself tells the reader that a real reason is now being provided"),
             feedback=("Correct: A. The warrant is weak because its because-clause just repeats the claim: "
                       "'monitored because watching them is good' is the same idea twice, with no real reason. "
                       "Length (C) is not the problem, and using the word because (D) does not make reasoning "
                       "real. A repair would give the reason: 'because early signs like small quakes and "
                       "swelling ground can warn a town before an eruption.' Predicting weak here trains your "
                       "eye for the empty-warrant trap.")),

        # ===== SUPPORTED: calibration self_score (predict THEN reveal), then repair the same draft. =====
        # self_score body is kept SHORT (the reveal lives in per-choice feedback), so the checkpoint prompt does
        # not render as a wall of text; explicit choices give the two scores reliable per-choice feedback.
        Slot("SUPPORTED", "self_score", "Score it yourself, then see the real score",
             ref="", bank="volcanoes",
             body=("Predict, then reveal. Here is a draft warrant: 'Volcanic ash is harmful because it is bad "
                   "for people.' On a 2-point scale, a 2 explains a real reason and a 1 only restates the claim. "
                   "Commit to a score, then check the reveal."),
             choices=[
                 {"id": "n1", "text": "1, it only restates the claim",
                  "correct": True,
                  "why": "Correct. 'Harmful because it is bad' just says harmful twice and names no real reason, so it scores 1. A 2 would explain what ash does, for example 'because breathing ash can damage the lungs and clog engines and water supplies.'"},
                 {"id": "n2", "text": "2, it explains a real reason",
                  "correct": False,
                  "why": "Look again. 'Bad for people' does not name what the ash actually does; it only restates 'harmful,' so no real reason is given. This is the pull to over-rate a warrant that sounds fine but explains nothing. It scores 1."},
             ]),
        Slot("SUPPORTED", "production_frq", "Repair the weak warrant",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="revision",
             body=frq_prompt(
                 intro="Revise this provided draft so the warrant explains a real reason, not a restatement.",
                 setapart_block=setapart("Weak draft to fix:", "Volcanic ash is harmful because it is bad for people.", "red"),
                 closer="Keep the claim, but replace the empty because-clause with a real reason (what ash "
                        "actually does). Write it in one sentence, then run the check: after because, is there a "
                        "new reason, or the claim again?")),
        # COUNCIL FIX (2026-07-24): Option A (later-in-arc). One graded rewrite; checks read-only beneath; name-act dropped.
        Slot("MODEL", "diagnosis_frq", "Write a warrant that explains",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="This provided draft has a causal word (because), but after it the draft only repeats the "
                       "claim: 'risky because dangerous' says the same idea twice and names nothing that actually "
                       "happens near a volcano, so the warrant is empty. Write a fresh warrant sentence that "
                       "explains a real reason instead.",
                 setapart_block=setapart("Empty warrant to replace:", "Living near a volcano is risky because it is dangerous.", "red"),
                 checklist_block=checklist(title="Make your warrant pass these (no need to type answers):", rows=[
                     "Is there a causal word (because, since, or as)?",
                     "After it, is there a new reason, or just the claim again?",
                     "Does the reason name what actually happens (such as lava flows, ashfall, or sudden eruptions)?",
                 ]),
                 closer="Write one fresh warrant sentence about living near a volcano. Run the check above before "
                        "you submit.")),

        # ===== INDEPENDENT: cold revise a provided draft + autonomy + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Revise a provided draft on your own",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="revision",
             body=frq_prompt(
                 intro="On your own now. Revise this provided draft so the warrant explains a real reason, not "
                       "a restatement.",
                 setapart_block=setapart("Provided draft to fix:", "Volcanoes are worth studying because studying them is important.", "red"),
                 closer="Judging and repairing weak reasoning is the check every strong writer runs on their "
                        "own work, and you are ready to do it cold. Write your revision in one sentence, then "
                        "run the check: after because, is there a new reason, or the claim again? Fix it before "
                        "you submit.")),

        # ===== TRANSFER: same check-and-repair move, a NEW topic (water cycle), partitioned from taught bank =====
        Slot("TRANSFER", "stimulus_display", "The topic: the water cycle",
             ref="ACC-W910-FRAME-WATER-CYCLE", bank="water_cycle",
             body=("The next draft to check is about the water cycle. Read this short orientation so the topic "
                   "is familiar. Again, you are checking and repairing a provided draft's reasoning, not writing "
                   "from scratch.")),
        Slot("TRANSFER", "production_frq", "Revise a provided draft on a NEW topic",
             ref="", bank="water_cycle", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="revision",
             body=frq_prompt(
                 intro="New topic. Revise this provided draft so the warrant explains a real reason (what the "
                       "cycle actually does), not a restatement.",
                 setapart_block=setapart("Provided draft to fix:", "The water cycle is important because it matters a lot.", "red"),
                 closer="Same check-and-repair move as the volcano drafts, a fresh topic. Write your revision in "
                        "one sentence, then run the check before you submit.")),
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
