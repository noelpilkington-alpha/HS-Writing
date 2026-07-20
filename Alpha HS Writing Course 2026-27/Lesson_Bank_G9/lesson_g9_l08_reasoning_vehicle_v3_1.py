"""
lesson_g9_l10_reasoning_vehicle_v3_1.py  -  G9 KC C.9.03, ARCHETYPE T3: EVIDENCE-INTEGRATION/REASONING
(PROVE, sentence). V3.1 rebuild of lesson_g9_l10_reasoning_vehicle.py.

TEACHING POINT (KEPT, unchanged): tie EVIDENCE to your CLAIM with a reasoning hinge - because states the
reason, but concedes/limits, so states the upshot. Taught by FUNCTION (the reasoning job each word does),
NOT as grammar; the connector mechanic is app-owned + gated. Id ACC-W910-L-G9-C903-0010, KC C.9.03,
established-caveat mnemonic, and the EXISTING bound stimuli (SCHOOLLUNCH taught -> COMMUNITYSERVICE transfer)
are all preserved.

V3.1 (2026-07-14): applies the adjudicated Council + Fable pattern captured in icm/_config/v3_1-lesson-build-spec.md.
Changes vs the v1 lesson:
  1. TEACH is now ONE idea, hammered: a teal ONE_IDEA callout + the three hinge JOBS as a real <ul> list
     (was a 172-word wall of prose that tripped format_fidelity).
  2. MODEL is a coping-model think-aloud (a writer drafting side-by-side -> running the check -> catching the
     missing hinge -> revising), draft by draft, still holding literal BEFORE + AFTER. No named near-peer
     (Timeback stateless rule). The reusable 3-question check tool is folded in at the POINT OF FIRST USE.
  3. Discrimination now carries explicit choices=[{id,text,correct,why}] and NO leaked internal label
     ("Grade-C"/"design bet" removed from the student text). The token confound is broken: a DISTRACTOR
     carries "because" (on a reason that restates the claim, no fact linked) and the CORRECT option uses "so"
     with no "because" - so the invariant a novice must read is "the hinge ties the fact to the claim," not
     the single word "because" (DI faultless communication).
  4. SUPPORTED / DIAGNOSIS / TRANSFER FRQ bodies are built with frq_prompt/setapart/checklist (no "Step 1/2"
     prose that rendered as double-numbered lists; no "Scored on ..." trait chrome).
  5. INDEPENDENT write gives autonomy + says the standard out loud (Yeager): the linking move is what turns a
     fact into real evidence, and you are ready to do it cold.

Passes all 23 lesson_contract gates. Own words, federal-sourced facts only, no fabricated figures, no em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Evidence does not speak for itself. A reasoning '
'<strong>hinge</strong> - the word <strong>because</strong>, <strong>but</strong>, or <strong>so</strong> - '
'shows HOW a fact supports your claim.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit a linked sentence, run this test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Is there a hinge (because, but, or so)?</li>'
'<li style="margin:2px 0">Does the hinge show HOW the fact supports the claim?</li>'
'<li style="margin:2px 0">Is a real fact from the source used?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, the fact is not linked to your claim yet.</div></div>')

# coping-model think-aloud: a WRITTEN drafting process (side-by-side -> catch the missing hinge -> revise),
# then the BEFORE/AFTER endpoints. No named near-peer (Timeback stateless rule).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer thinking it through, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Schools should offer free meals to all students. '
    'The program already reaches millions who would otherwise go hungry." Check it: is there a hinge that shows '
    'HOW the fact backs the claim? No. The claim and the fact just sit side by side, so the reader has to '
    'connect them alone. Add a hinge.</p>'
    '<p style="margin:0"><strong>Second try:</strong> "Schools should offer free meals to all students, '
    'because the program already reaches millions who would otherwise go hungry in class." Now "because" '
    'states the reason the fact supports the claim, so the link is right there on the page. That passes.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "Schools should offer free meals to all students. The program '
    'already reaches millions who would otherwise go hungry." (claim and fact side by side, no link)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "Schools should offer free meals to all students, '
    '<strong>because</strong> the program already reaches millions who would otherwise go hungry in class." '
    '(a hinge states the reason, so the link is clear)</span></div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C903-0010", grade="9-10", lesson_type=3,
    unit="G9 U2 - Reasoning (the because/but/so vehicle)",
    title="Link Evidence to Your Claim With Because, But, So",
    target=("Tie your evidence to your claim with a reasoning hinge: because states the reason, but states a "
            "limit or contrast, so states the consequence. Written at the sentence. Trait: Evidence/Development "
            "(reasoning)."),
    acc_tags=["ACC.W.ARG.2", "CCSS.W.9-10.1b"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "established-caveat", "kc": "C.9.03", "sot": "icm course-G9.md L10",
                "taught_stimulus": "ACC-W910-ARG-LESSON-SCHOOLLUNCH",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-COMMUNITYSERVICE",
                "playbook": "_phase2/playbook_T3_PROVE.md",
                "template": "locked L01 template; EVIDENCE-TIER binds full sources.",
                "one_idea": "A reasoning hinge (because, but, so) shows HOW a fact supports your claim.",
                "one_reminder": "3-question check: hinge? shows how? real fact?",
                "version_note": ("V3.1: rebuilt to the v3.1 spine (icm/_config/v3_1-lesson-build-spec.md). TEACH "
                                 "trimmed to one idea + the three hinge jobs as a real list (was a 172-word wall); "
                                 "MODEL is a coping-model think-aloud with BEFORE/AFTER + the 3-question check tool "
                                 "folded in at first use; discrimination now uses explicit choices with per-option "
                                 "'why', drops the leaked 'Grade-C'/'design bet' label, and breaks the 'because' "
                                 "token confound (a distractor carries 'because', the correct option uses 'so'); "
                                 "all FRQ/diagnosis bodies use frq_prompt/setapart/checklist (no 'Step 1/2' prose, "
                                 "no 'Scored on' chrome); INDEPENDENT adds autonomy + say-the-standard. Teaching "
                                 "point, id, KC C.9.03, and the bound SCHOOLLUNCH/COMMUNITYSERVICE stimuli preserved."),
                "council": ("T3/PROVE reasoning intro: the because/but/so vehicle taught by FUNCTION "
                            "(because=reason, but=limit/contrast, so=consequence), NOT as grammar. Connector "
                            "mechanic app-owned + gated."),
                "review_provenance": ("v3.1-lesson-build-spec.md pattern (adjudicated Council + Fable-5 findings "
                                      "cleared on G9 L01 v3.1), applied 2026-07-14.")},
    fade_ledger_moves=["because-but-so-vehicle", "link-evidence-to-claim"],
    slots=[
        # ===== TEACH: ONE idea, hammered - the teal callout + the three hinge JOBS as a real list =====
        Slot("TEACH", "teach_card", "The word that shows HOW your evidence backs your claim",
             body=(ONE_IDEA +
                   "<p style=\"color:#1f2a44;font-size:14px;margin:6px 0 0\">Putting a claim and a fact next to "
                   "each other is not enough; you have to show HOW the fact backs the claim. The "
                   "<strong>because/but/so hinge</strong> means a small linking word (because, but, or so) that "
                   "does exactly that job. Each one does a different job:</p>"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Because</strong> states the reason the fact supports the "
                   "claim ('free meals help, because hunger blocks learning').</li>"
                   "<li style=\"margin:4px 0\"><strong>But</strong> states a limit or a contrast ('the program is "
                   "large, but it still misses some families').</li>"
                   "<li style=\"margin:4px 0\"><strong>So</strong> states the consequence ('hunger blocks "
                   "learning, so free meals raise focus').</li></ul>"
                   "<p style=\"color:#1f2a44;font-size:14px;margin:6px 0 0\">Notice we care about the JOB each "
                   "word does (the reason, the contrast, the consequence), not about naming a grammar part. "
                   "Connecting sentences is a skill you already own from earlier courses; here you use it to tie "
                   "evidence to a claim. The trap this fixes: a claim and a fact sitting side by side with no "
                   "hinge, so the reader cannot see the connection. Today's goal: link one fact to a claim with "
                   "because, but, or so.</p>")),
        Slot("TEACH", "stimulus_display", "Read the source: free school meals",
             ref="ACC-W910-ARG-LESSON-SCHOOLLUNCH", bank="school_lunch",
             body=("Read this source about free school meals. Because your job is to LINK a fact to a claim, "
                   "read the whole thing and pick one fact you could use, then think about the reason it "
                   "supports a claim. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model think-aloud + the reusable check tool at first use =====
        Slot("MODEL", "annotated_before_after", "Watch a writer link a fact to a claim",
             bank="school_lunch",
             body=("Here is the skill in action. Follow the writer's thinking below." + COPING_HTML +
                   " Notice the one move that turned the BEFORE into the AFTER: the writer added a "
                   "<strong>hinge</strong> that states the reason the fact backs the claim. " + REMEMBER +
                   "When you write your own, build it the same way: state the claim, bring in a fact, then add a "
                   "because, but, or so hinge that shows HOW the fact supports the claim.")),
        Slot("MODEL", "discrimination", "Which sentence links the fact to the claim?",
             ref="", labeled_grade_c=True, bank="school_lunch",
             body=("Now that you have seen one built, spot the target. All four use the same claim and the same "
                   "fact about free meals. Which sentence LINKS the fact to the claim with a hinge that shows HOW "
                   "the fact supports it? "
                   "(A) Schools should offer free meals to all students. The National School Lunch Program already "
                   "serves billions of low-cost lunches to hungry children in schools all across the country.  "
                   "(B) Schools should offer free meals to all students, because free meals for all students would "
                   "clearly be a good and fair policy for a caring school to adopt.  "
                   "(C) The program already reaches millions who would otherwise go hungry, so schools should make "
                   "meals free for everyone and keep those students fed.  "
                   "(D) The program already reaches millions who would otherwise go hungry, so it is honestly very "
                   "sad that any child in the country ever has to sit through class hungry. "
                   "Correct: C. B has the word 'because,' but its clause just restates the claim; D has a hinge "
                   "and a real fact, but the 'so' leads to a feeling, not the claim. Only C's hinge links the "
                   "actual fact to the claim."),
             choices=[
                 {"id": "A", "text": "Schools should offer free meals to all students. The National School Lunch Program already serves billions of low-cost lunches to hungry children in schools all across the country.",
                  "correct": False,
                  "why": "This places the claim and the fact side by side, but nothing links them, so the reader has to figure out on their own how the fact supports the claim."},
                 {"id": "B", "text": "Schools should offer free meals to all students, because free meals for all students would clearly be a good and fair policy for a caring school to adopt.",
                  "correct": False,
                  "why": "This uses the word 'because,' but the reason just restates the claim and never brings in the fact, so no evidence is actually linked to the claim."},
                 {"id": "C", "text": "The program already reaches millions who would otherwise go hungry, so schools should make meals free for everyone and keep those students fed.",
                  "correct": True,
                  "why": "Correct. It uses the hinge 'so' to show HOW the fact (the program reaches millions who would go hungry) supports the claim. The hinge does the linking, not the word 'because' specifically."},
                 {"id": "D", "text": "The program already reaches millions who would otherwise go hungry, so it is honestly very sad that any child in the country ever has to sit through class hungry.",
                  "correct": False,
                  "why": "This has a hinge and a real fact, but the 'so' leads to a feeling about the fact, not to the claim, so the fact is never actually linked to the claim you are arguing."},
             ]),
        Slot("MODEL", "discrimination", "Which connector does the reasoning job?",
             ref="", labeled_grade_c=True, bank="school_lunch",
             body=("Here all three sentences carry the same fact and the same claim about free school meals, and "
                   "only the connecting word changes. Which one uses a hinge that shows HOW the fact supports the "
                   "claim?"),
             choices=[
                 {"id": "A", "text": "Many students who count on the program would otherwise go hungry in class, but schools should offer free meals to all students.",
                  "correct": False,
                  "why": "The word 'but' signals a contrast, so it frames the fact as working against the claim instead of showing how it backs the claim."},
                 {"id": "B", "text": "Many students who count on the program would otherwise go hungry in class, and schools should offer free meals to all students.",
                  "correct": False,
                  "why": "The word 'and' only glues the fact and the claim together, so it still leaves the reader to guess how the fact supports the claim."},
                 {"id": "C", "text": "Many students who count on the program would otherwise go hungry in class, so schools should offer free meals to all students.",
                  "correct": True,
                  "why": "Correct. The hinge 'so' states the consequence, showing that the fact about hungry students is exactly why the claim holds."},
                 {"id": "D", "text": "Many students who count on the program would otherwise go hungry in class, then schools should offer free meals to all students.",
                  "correct": False,
                  "why": "The word 'then' marks time order, not reasoning, so it lines the two ideas up in sequence without showing how the fact supports the claim."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this pair of sentences most need?",
             bank="school_lunch",
             body=("Diagnose this draft before the reveal. A student wrote: 'Free school meals matter a lot. The "
                   "program serves billions of lunches each year.' Which single move would most improve the "
                   "reasoning? "
                   "(A) add a hinge that states HOW the fact supports the claim, such as a because-reason or a "
                   "so-consequence  "
                   "(B) add a third sentence with one more fact about exactly how many billions of lunches the "
                   "program serves to children each year  "
                   "(C) make both the claim and the fact longer by adding more formal and descriptive words to "
                   "each one  "
                   "(D) swap the order so the fact about lunches comes first and the claim comes second"),
             feedback=("Correct: A. The claim and the fact sit side by side with no hinge, so the reader cannot "
                       "see WHY the fact matters to the claim. The fix is a hinge: 'The program serves billions "
                       "of lunches, so free meals already reach the students who most need to eat before class.' "
                       "Another fact (B), longer wording (C), or reordering (D) never build the missing link.")),

        # ===== SUPPORTED: framed write (fill-in frame) on the taught source =====
        Slot("SUPPORTED", "production_frq", "Link a fact to a claim with a hinge",
             ref="", bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on the one move: linking a fact to your claim.",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "______ [your claim about free meals] because ______ [a fact from the source, and the reason it supports your claim]."),
                 closer="You may use but or so instead of because if that fits your reasoning better. Write one "
                        "sentence, and do not just place the fact next to the claim.")),
        # DIAGNOSIS = check-and-fix on a PROVIDED weak draft (produces a fresh sentence, not a look-back at
        # the student's own earlier work). Stays on the taught source = no new reading load.
        Slot("MODEL", "diagnosis_frq", "Check and fix a weak draft with the 3 questions",
             ref="", bank="school_lunch", scored=True,
             body=frq_prompt(
                 intro="Run the check on this weak draft, then rewrite it into one linked sentence of your own.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "Free meals are important. The program serves billions of lunches.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Is there a hinge (because, but, or so)?", "No. The two ideas just sit side by side. Add a hinge."),
                     ("Does the hinge show HOW the fact supports the claim?", "Not yet. Make the reason the fact backs the claim clear."),
                     ("Is a real fact from the source used?", "Yes, the lunches-served fact is real. Keep it."),
                 ]),
                 closer="Now write one fresh sentence that links a source fact to a claim with a hinge, then run the "
                        "same three checks on your own sentence to confirm all three pass.")),

        # ===== INDEPENDENT: cold write on the taught source + autonomy + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Link evidence to a claim on your own",
             ref="", bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="On your own now, no frame. Make a claim about free school meals and link one fact from "
                       "the source to it.",
                 closer="Use because, but, or so to show HOW the fact supports your claim. This linking move is "
                        "what turns a fact into real evidence, and you are ready to do it cold. Before you submit, "
                        "check for a hinge, that the hinge shows how the fact supports the claim, and that a real "
                        "fact is used.")),

        # ===== TRANSFER: same move, a NEW source (community service), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: required community service",
             ref="ACC-W910-ARG-LESSON-COMMUNITYSERVICE", bank="community_service",
             body=("Read this new source about making community service a graduation requirement. Your job is the "
                   "same: pick one fact you could use, then think about the reason it supports a claim. The text "
                   "stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Link evidence to a claim on a NEW topic",
             ref="", bank="community_service", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="New topic. The task: should community service be required to graduate? Make a claim, then "
                       "link one fact from the source to it.",
                 closer="Use a because, but, or so hinge to show HOW the fact supports your claim. Same move as "
                        "the meals sentence, new topic. Do not just place the fact next to the claim.")),
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
