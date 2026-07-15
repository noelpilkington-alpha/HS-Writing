"""
lesson_g11_l25_emphasis_order.py  -  G11 KC C.11.04, ARCHETYPE T6: EDITING-IN-CONTEXT (SPOT, ceiling sentence).
V3.1 rebuild of the pre-v3.1 L25 to the v3.1 lesson build spec (icm/_config/v3_1-lesson-build-spec.md), the
pattern that cleared all 23 lesson_contract gates + the Fable-5 reviewer.

TEACHING POINT (KEEP): emphasis order. Order the reasons in a paragraph so the STRONGEST reason lands LAST, in
the emphatic position, rather than trailing off on a weak one; edit the given reason string in place. KC C.11.04.
Bound stimuli unchanged: taught ENERGYMIX (bank energy_transition) -> transfer WATERUSE (bank
water_infrastructure), bank-partitioned.

V3.1 changes from the current L25 (design pattern, not the teaching point):
  1. TEACH split to ONE idea in a callout + the trails-off/strongest-last contrast as a real LIST (was a
     ~140-word prose wall that tripped format_fidelity).
  2. MODEL rebuilt as a coping-model think-aloud (draft -> run the check -> catch the weak ending -> revise),
     with a literal BEFORE and AFTER; the reusable 3-question check tool folded in at point of first use.
  3. DISCRIMINATION uses explicit choices=[{id,text,correct,why}]; the "Grade-C design bet" jargon that leaked
     into the student prompt is gone (labeled_grade_c stays True in code only). Signal-word confound broken: a
     distractor that ends WEAK still carries the strongest signal phrase ("most of all"), so the invariant is
     "ends on the strongest reason," not "has an emphasis cue word." Correct option is not the lone longest.
  4. FRQ + diagnosis bodies built with frq_prompt / setapart / checklist (no "Step 1/Step 2" prose -> kills the
     render double-numbering fail; no "Scored on ..." chrome).
  5. INDEPENDENT names the standard out loud (Yeager). TRANSFER stays a partitioned new source (water use).

id, lesson_type=6, kc="C.11.04", and mnemonic_status="proposal" are the current L25's values, unchanged; every
scored production_frq unit="sentence" (T6 ceiling). Own words, no fabricated figures, no em dashes. Runs QC.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A reader remembers what they read <strong>last</strong>. '
'So end a paragraph of reasons on your <strong>strongest</strong> one, not on a weak or minor point.</div></div>')

# reusable job-aid, folded in at point of first use (the decompose/model card), not cold in step 1 (KH load).
REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit any string of reasons, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Which reason is your strongest?</li>'
'<li style="margin:2px 0">Is that reason in the last slot?</li>'
'<li style="margin:2px 0">If not, move it there, and cut any weak filler reason.</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">The last slot is the emphatic position: the spot that lands hardest.</div></div>')

# coping-model think-aloud: a WRITTEN editing process (draft -> run the check -> catch the weak ending -> revise),
# then the endpoints. Contains a literal BEFORE and AFTER (content_depth). No named near-peer (Timeback rule).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer editing one reason string, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "We should expand clean power because it can create '
    'jobs, because a reliable grid prevents the enormous losses blackouts cause, and because it looks modern." '
    'Run the check: which reason is strongest? Preventing blackout losses. Is it last? No, "looks modern" is '
    'last. The weakest reason is sitting in the emphatic spot.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "...because it looks modern, because it creates jobs, '
    'and because a reliable grid prevents blackout losses." Better, the strongest reason is last now. But "looks '
    'modern" is weak filler and opens the string. Cut it.</p>'
    '<p style="margin:0"><strong>Final:</strong> "We should expand clean power because it creates jobs, and most '
    'of all because a reliable grid prevents the enormous losses that blackouts cause." Strongest reason lands '
    'last, weak filler gone.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "...and because it looks modern." (ends on the weakest reason)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "...and most of all because a reliable grid prevents the enormous '
    'losses that blackouts cause." (ends on the strongest reason)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1107-0025", grade="9-10", lesson_type=6,
    unit="G11 U6 - Emphasis order (strongest evidence last)",
    title="Put Your Strongest Reason in the Emphatic Spot",
    target=("Resequence the reasons or evidence in a paragraph so the strongest lands last (the emphatic "
            "position), rather than trailing off on the weakest, editing the given reason string in place. "
            "Written at the sentence. Trait: Organization (emphasis)."),
    acc_tags=["ACC.W.ARG.4", "CCSS.W.11-12.1", "CCSS.W.11-12.4"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.04", "sot": "icm course-G11.md L25",
                "taught_stimulus": "ACC-W910-INFO-LESSON-ENERGYMIX",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-WATERUSE",
                "playbook": "_phase2/playbook_T6_SPOT.md",
                "template": "v3.1 lesson build spec; binds full info source (paragraph material); editing-in-context.",
                "one_idea": "A reader remembers what they read last, so end on your strongest reason.",
                "one_reminder": "3-question check: which reason is strongest? is it last? if not, move it there and cut weak filler.",
                "version_note": ("V3.1 rebuild of L25 to the v3.1 build spec: TEACH split into one-idea callout + "
                                 "trails-off/strongest-last list (fixes the format_fidelity prose wall); MODEL "
                                 "rebuilt as a coping-model think-aloud with the 3-question check folded in at "
                                 "point of first use; discrimination moved to explicit choices with the 'Grade-C "
                                 "design bet' jargon removed and the emphasis-cue-word confound broken (a wrong "
                                 "option still ends weak while carrying 'most of all'); FRQ + diagnosis bodies use "
                                 "frq_prompt/setapart/checklist (kills 'Step 1/2' render double-numbering and the "
                                 "'Scored on' chrome); independent says the standard out loud (Yeager). Teaching "
                                 "point + bound stimuli unchanged."),
                "review_provenance": ("Rebuilt to icm/_config/v3_1-lesson-build-spec.md (the pattern that cleared "
                                      "all 23 lesson_contract gates + the Fable-5 reviewer on G9 L01 v3.1)."),
                "council": ("T6/SPOT G11 emphasis-order intro: O2 strongest-evidence-last (emphatic position), "
                            "edit a given reason string by resequencing. strongest-last-vs-trails-off "
                            "discrimination labeled Grade-C in code (not in student text). SPOT=proposal; "
                            "ceiling sentence.")},
    fade_ledger_moves=["emphasis-order", "strongest-evidence-last"],
    slots=[
        # ===== TEACH: ONE idea in a callout + the trails-off/strongest-last contrast as a real LIST =====
        Slot("TEACH", "teach_card", "The last position is the emphatic one",
             body=(ONE_IDEA +
                   "Order carries emphasis. When you list several reasons, the one you put last is the one the "
                   "reader carries away, so the last slot, called the emphatic position, means the spot that "
                   "lands hardest. That makes the editing move simple: end on your STRONGEST reason. Two orders "
                   "to keep apart:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>TRAILS OFF</strong>: the paragraph ends on a weak or minor "
                   "reason (say, 'and it looks modern'), so the writing fades right where the reader remembers it "
                   "most.</li>"
                   "<li style=\"margin:4px 0\"><strong>STRONGEST LAST</strong>: the paragraph ends on its "
                   "strongest reason (say, 'and most of all it prevents huge blackout losses'), so the point that "
                   "lands is the one that matters most.</li></ul>"
                   "The fix resequences: move the strongest reason to the final slot, and often cut the weakest "
                   "entirely. This is an editing move on writing that already exists, so you spot the ordering "
                   "problem and fix it in place. Goal today: reorder a reason string so the strongest lands last.")),
        Slot("TEACH", "stimulus_display", "Read the source: the U.S. electricity mix",
             ref="ACC-W910-INFO-LESSON-ENERGYMIX", bank="energy_transition",
             body=("Read this source on the U.S. electricity mix. The reason strings you edit draw their points "
                   "from it, so knowing which points are strong (backed by real figures, like the losses "
                   "blackouts cause) and which are weak lets you order them for emphasis. You are not writing "
                   "about energy from scratch here; you are reordering reasons that are given to you. The text "
                   "stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model think-aloud with the check tool folded in =====
        Slot("MODEL", "annotated_before_after", "Watch a trailing-off reason string get reordered",
             bank="energy_transition",
             body=("Here is the skill in action. Follow the writer's editing below. " + COPING_HTML +
                   " Notice the one move that turned the BEFORE into the AFTER: the writer moved the strongest "
                   "reason to the final slot and cut the weak filler. " + REMEMBER +
                   "When you fix your own reason string, do the same: find your strongest reason, move it last, "
                   "and run the 3 questions before you submit.")),
        Slot("MODEL", "discrimination", "Which ordering ends on the strongest reason?",
             ref="", labeled_grade_c=True, bank="energy_transition",
             body=("Now that you have seen one built, spot the target. Each string lists the same three reasons "
                   "in a different order. Which one ends on the STRONGEST reason (that a reliable grid prevents "
                   "the huge losses blackouts cause)? "
                   "(A) We should expand clean power because it creates jobs, and because a reliable grid "
                   "prevents huge blackout losses, and most of all because it looks modern and up to date.  "
                   "(B) We should expand clean power because it looks modern, and because it creates good jobs, "
                   "and finally because a reliable grid prevents the huge losses blackouts cause.  "
                   "(C) We should expand clean power because a reliable grid prevents huge blackout losses, and "
                   "because it looks modern, and because it can create good jobs for many people. "
                   "Correct: B. It ends on the strongest reason, the losses blackouts cause."),
             choices=[
                 {"id": "A", "text": "We should expand clean power because it creates jobs, and because a reliable grid prevents huge blackout losses, and most of all because it looks modern and up to date.",
                  "correct": False,
                  "why": "This one ends on 'it looks modern,' the weakest reason, so it trails off. The phrase 'most of all' cannot rescue a weak point: what matters is which reason is in the last slot, and here it is the wrong one."},
                 {"id": "B", "text": "We should expand clean power because it looks modern, and because it creates good jobs, and finally because a reliable grid prevents the huge losses blackouts cause.",
                  "correct": True,
                  "why": "Correct. It ends on the strongest reason, the huge losses a reliable grid prevents, so the point the reader carries away is the one that matters most. Strongest last is the move."},
                 {"id": "C", "text": "We should expand clean power because a reliable grid prevents huge blackout losses, and because it looks modern, and because it can create good jobs for many people.",
                  "correct": False,
                  "why": "This one buries the strongest reason (blackout losses) at the front and ends on a middling reason (jobs). The emphatic last slot goes to a weaker point, so it does not land."},
             ]),
        Slot("MODEL", "discrimination", "Which string ends on the strongest reason, not opens with it?",
             ref="", labeled_grade_c=True, bank="energy_transition",
             body=("Same skill, a new trap. Each string below lists the same three reasons in a different "
                   "order. The strongest reason is that cleaner air lowers the health costs pollution "
                   "causes. Which string puts that strongest reason in the emphatic last slot, not the first? "
                   "(A) We should expand clean power because cleaner air lowers the health costs that pollution "
                   "causes, because it can lower electricity bills, and because other countries are already doing it too.  "
                   "(B) We should expand clean power because other countries are doing it, because it can lower "
                   "electricity bills, and finally because cleaner air lowers the health costs that pollution causes.  "
                   "(C) We should expand clean power because cleaner air lowers the health costs pollution causes, "
                   "because other countries are doing it, and because it can lower electricity bills. "
                   "Correct: B. It ends on the strongest reason, cleaner air and lower health costs."),
             choices=[
                 {"id": "A", "text": "We should expand clean power because cleaner air lowers the health costs that pollution causes, because it can lower electricity bills, and because other countries are already doing it too.",
                  "correct": False,
                  "why": "This string leads with the strongest reason but ends on other countries doing it, so the weakest point is the one the reader carries away."},
                 {"id": "B", "text": "We should expand clean power because other countries are doing it, because it can lower electricity bills, and finally because cleaner air lowers the health costs that pollution causes.",
                  "correct": True,
                  "why": "Correct. It ends on the strongest reason, that cleaner air lowers the health costs pollution causes, so the emphatic last slot lands the point that matters most."},
                 {"id": "C", "text": "We should expand clean power because cleaner air lowers the health costs pollution causes, because other countries are doing it, and because it can lower electricity bills.",
                  "correct": False,
                  "why": "This string ends on lowering bills, a middling reason, and buries the strongest one up front, so the emphatic last slot is wasted."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this reason string's order most need?",
             bank="energy_transition",
             body=("Diagnose this draft before the reveal. A string lists three reasons and ends on 'and it is "
                   "also kind of a popular idea right now.' Which single move would most improve it? "
                   "(A) move the strongest reason to the final slot, and cut the weak closer about popularity  "
                   "(B) add a fourth reason so the string gives the reader even more support to consider  "
                   "(C) make every reason about the same length so the three of them look evenly balanced  "
                   "(D) start with the weakest reason instead and simply let the other two fall where they may"),
             feedback=("Correct: A. Ending on 'a popular idea right now' wastes the emphatic last slot on the "
                       "weakest point. The fix moves the strongest reason last and cuts the weak closer. A fourth "
                       "reason (B), equal lengths (C), or leading with the weakest (D) do not fix which reason "
                       "lands last.")),

        # ===== SUPPORTED: framed edit (fill-in frame) on the taught topic (source read at TEACH step 2) =====
        Slot("SUPPORTED", "production_frq", "Reorder to end on the strongest reason",
             ref="", bank="energy_transition", rubric_ref="rc.ap", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Reorder this reason string so the strongest reason lands last. Here is the string to fix: "
                       "'We should expand clean power because it can create jobs, because a reliable grid prevents "
                       "huge blackout losses, and because it looks modern.'",
                 setapart_block=setapart("Copy this frame, then fill the last slot:",
                                         "We should expand clean power because ______, and most of all because ______ [put your STRONGEST reason here]."),
                 closer="Put the strongest reason (the huge losses a reliable grid prevents) in the final slot, "
                        "and cut the weakest one ('it looks modern'). Write one sentence, then run the 3-question "
                        "check before you submit.")),
        # DIAGNOSIS = run the check on a PROVIDED weak draft, then rewrite it (not a fresh production, so it does
        # not repeat the Finish write). Stays on the taught topic = no new source to read (load balance).
        Slot("MODEL", "diagnosis_frq", "Check the order, then fix a weak draft",
             ref="", bank="energy_transition", scored=True,
             body=frq_prompt(
                 intro="Run the 3-question check on this weak draft, then rewrite it so the strongest reason lands last.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "Clean power matters because it prevents costly blackouts, because it makes jobs, and because it is modern.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Which reason is strongest?", "Preventing costly blackouts."),
                     ("Is that reason in the last slot?", "No. It opens the string, and 'it is modern' (the weakest) ends it, so resequence."),
                     ("What is the fix?", "Move the blackout reason last and cut 'it is modern.'"),
                 ]),
                 closer="Now rewrite the weak draft into one sentence that ends on the strongest reason. Then name "
                        "which reason you put last.")),

        # ===== INDEPENDENT: cold edit on the taught topic + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Order for emphasis on your own",
             ref="", bank="energy_transition", rubric_ref="rc.ap", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="On your own now, no frame. Write ONE reason string on the electricity-mix topic that ends "
                       "on its strongest reason (the emphatic last slot) and drops any weak filler reason.",
                 closer="Before you submit, check: is the strongest reason last, and is the weakest cut? Ending on "
                        "your strongest point is what every well-built argument paragraph is built on, and you are "
                        "ready to do this cold. Run the 3-question check before you submit.")),

        # ===== TRANSFER: same move, a NEW source (water use), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: U.S. water use",
             ref="ACC-W910-INFO-LESSON-WATERUSE", bank="water_infrastructure",
             body=("Read this new source on U.S. water use. Notice which reasons its figures make strong (say, "
                   "that a depleted aquifer can take decades to recover) and which are weaker, so you can order a "
                   "reason string for emphasis. Again, you are reordering reasons on a given topic, not writing "
                   "from scratch. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Order for emphasis on a NEW source",
             ref="", bank="water_infrastructure", rubric_ref="rc.ap", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="New source. Write ONE reason string on the water-use topic that ends on its strongest "
                       "reason (such as aquifers being slow to refill once they are drawn down) and cuts the "
                       "weakest.",
                 closer="Same strongest-last move as the electricity string, new source: put the strongest reason "
                        "in the final slot and drop weak filler. Run the 3-question check before you submit.")),
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
