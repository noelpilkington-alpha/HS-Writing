"""
lesson_g9_l20_concede_answer_v3_1.py  -  G9 KC C.9.07, ARCHETYPE T2 (STAND, sentence). V3.1.

G9 U4, SECOND rung of the new Counterargument unit. CONCEDE-THEN-ANSWER at the sentence: acknowledge a real
opposing point, then respond to it while HOLDING your own claim, in the shape "Although X, Y because Z". This
is the INTRODUCTORY G9 depth: teach the positive concede+answer MOVE cleanly. It does NOT teach the
concede-and-COLLAPSE failure mode in depth (a light one-line "keep your side, do not drift to both-sides-are-
right" reminder only); the collapse-trap + strawman-rebuttal + evidence-rebuttal nuance is reserved for the
deeper G10 spiral (lesson_g10_l02_concede_hold). This lesson follows the RECOGNIZE rung
(lesson_g9_l19_recognize_counterargument_v3_1, which only NAMES the other side); yours is the next step:
concede a named objection AND answer it. Taught: FRAME-FREETRANSIT (bank free_transit) -> transfer:
FRAME-FOURDAYWEEK (bank four_day_week), partitioned. Topics deliberately DIFFER from the G10 counterargument
set (daylight_saving/school_year/congestion) AND from the sibling recognize lesson (community_service/
pay_for_grades), so no collision. rc.staar, unit="sentence". STAND=proposal. No named persona, no source
markup, no prior-work ref, no em dashes.

V3.1 spine: ONE_IDEA teal callout + minimal LIST teach (define counterargument/counterclaim + thesis tooltip)
-> bound issue frame -> coping-model think-aloud (skip the concession -> concede but never answer -> concede +
answer + hold) with literal BEFORE/AFTER -> named CONCEDE/ANSWER moves + REMEMBER 3-question check tool ->
discrimination x2 (choices=, homogeneous length, reveal in tail + per-choice why) -> predict-the-fix (reveal
in feedback) -> SUPPORTED framed "Although __, __ because __" write -> DIAGNOSIS check-and-fix on a provided
concede-no-answer draft -> INDEPENDENT cold concede+answer write -> TRANSFER on the partitioned four-day-week
frame.

ONE IDEA: concede a real objection, then ANSWER it and keep your side (Although X, Y because Z).
ONE REMINDER: the 3-question test (conceded a real objection, not a fact? answered it with a reason? still
hold a clear position?). Passes all lesson_contract gates. Own words, no fabricated figures, no em dashes.
Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Concede a real objection, then <strong>answer</strong> '
'it and keep your side. The shape is Although X, Y because Z, as in: <strong>Although free transit costs '
'taxpayers money, cities should still make the buses free because it gets people who cannot afford a car to '
'work.</strong></div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit any concede-and-answer sentence, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Did I concede a real objection (not a fact everyone already accepts)?</li>'
'<li style="margin:2px 0">Did I answer it with a reason (not just repeat my side)?</li>'
'<li style="margin:2px 0">Do I still hold a clear position?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, the sentence is not there yet.</div></div>')

# coping-model think-aloud panel: a WRITTEN process (skip the concession -> concede but never answer -> concede
# + answer + hold), then the endpoints. The writer's own claim here: cities should make public transit free.
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer thinking it through, draft by draft (the writer\'s own claim: cities should make public transit free):</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Cities should make the buses free, because free rides '
    'get people to work." Check it: did I concede a point the other side would raise? No, I skipped their '
    'strongest objection, the cost. Concede a real objection first.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "Although free transit costs taxpayers money, cities '
    'should make the buses free." Better, now it concedes. But did I answer that objection? No, I named the cost '
    'and then just repeated my side without a reason that answers it. Add the answer.</p>'
    '<p style="margin:0"><strong>Final:</strong> "Although free transit costs taxpayers money, cities should make '
    'the buses free, because getting people who cannot afford a car to work is worth that shared cost." It '
    'concedes a real point, answers it with a reason, and still holds the claim. That passes.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "Although free transit costs taxpayers money, cities should make '
    'the buses free." (concedes, but gives no reason that answers it)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "Although free transit costs taxpayers money, cities should make '
    'the buses free, because getting people who cannot afford a car to work is worth that shared cost." '
    '(concedes, answers, holds)</span></div>'
'</div>')

DECOMPOSE_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#f0fdf4;padding:10px 14px;border-bottom:1px solid #bbf7d0;font-size:15px">'
    'The finished sentence: <em>"Although free transit costs taxpayers money, cities should make the buses free, '
    'because getting people who cannot afford a car to work is worth that shared cost."</em></div>'
  '<div style="padding:12px 14px">'
    '<div style="margin:0 0 10px">'
      '<span style="display:inline-block;background:#fef9c3;color:#854d0e;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">MOVE 1 - CONCEDE</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px"><strong>"Although free transit costs taxpayers '
      'money"</strong> names a real objection the other side would raise, fairly, instead of pretending it '
      'away.</div></div>'
    '<div>'
      '<span style="display:inline-block;background:#dbeafe;color:#1e3a8a;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">MOVE 2 - ANSWER AND HOLD</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px">"...<strong>cities should make the buses free, '
      'because getting people who cannot afford a car to work is worth that shared cost</strong>" keeps a clear '
      'side AND gives a reason that answers the cost objection, instead of dropping the side.</div></div>'
    '<div style="margin-top:10px;color:#0f766e;font-size:13px">Concede a real point, then answer it with a reason '
    'and hold your side. The concession sets up the answer; it never replaces your position.</div>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C904-0031", grade="9-10", lesson_type=2,
    unit="G9 U4 - Counterargument (concede, then answer)",
    title="Concede a Point, Then Answer It",
    target=("Concede a real opposing point AND answer it while holding your own claim, in the shape Although X, "
            "Y because Z. Written at the sentence. Trait: Thesis/Purpose."),
    acc_tags=["ACC.W.ARG.2", "CCSS.W.9-10.1a"],
    provenance={"copyright": "own_authored", "authored": "2026-07-21",
                "mnemonic_status": "proposal", "kc": "C.9.07",
                "sot": "KC_Map_and_Unit_Arch_G9-12.md (G9 U4 - Counterargument)",
                "taught_stimulus": "ACC-W910-FRAME-FREETRANSIT",
                "transfer_stimulus": "ACC-W910-FRAME-FOURDAYWEEK",
                "template": "locked v3.1 spine (lesson_g10_l02_concede_hold); G9 concede+answer adaptation (shallower).",
                "one_idea": "Concede a real objection, then ANSWER it and keep your side (Although X, Y because Z).",
                "one_reminder": "3-question test: conceded a real objection (not a fact)? answered it with a reason? still hold a clear position?",
                "version_note": ("V3.1 build to the locked spine: ONE_IDEA teal callout with a built example + "
                                 "minimal list teach (counterargument/counterclaim defined + thesis tooltip), "
                                 "coping-model think-aloud (skip the concession -> concede but never answer -> "
                                 "concede + answer + hold) with literal BEFORE/AFTER, named CONCEDE/ANSWER moves + "
                                 "REMEMBER 3-question check tool, two leak-free discriminations via explicit "
                                 "choices= (homogeneous length, per-choice why, reveal in tail), predict-the-fix "
                                 "reveal in feedback, framed SUPPORTED 'Although __, __ because __' write, "
                                 "check-and-fix DIAGNOSIS on a provided concede-no-answer draft, cold INDEPENDENT "
                                 "concede+answer write, and a partitioned four-day-week TRANSFER."),
                "council": ("G9 CONCEDE-THEN-ANSWER rung of the counterargument ladder: this is the second rung, "
                            "one step past the RECOGNIZE lesson (lesson_g9_l19_recognize_counterargument_v3_1, "
                            "which only NAMES the other side). It teaches the positive move cleanly: concede a "
                            "real objection + answer it with a reason + hold the claim (Although X, Y because Z). "
                            "The concede-and-COLLAPSE failure mode gets only a one-line 'keep your side' reminder "
                            "here; the deeper collapse-vs-hold discrimination, strawman rebuttal, and "
                            "evidence-rebuttal are deliberately reserved for the G10 spiral "
                            "(lesson_g10_l02_concede_hold). Keeping the load at the sentence, appropriate for an "
                            "introductory rung. STAND=proposal; sentence ceiling.")},
    fade_ledger_moves=["concede-then-answer", "hold-claim-while-conceding"],
    slots=[
        # ===== TEACH: ONE idea only, minimal list; counterargument/counterclaim + thesis defined here =====
        Slot("TEACH", "teach_card", "The one idea: concede a real point, then answer it",
             body=(ONE_IDEA +
                   "A counterargument, also called a counterclaim, is a point that someone who disagrees with your "
                   "claim would make. In the last lesson you learned to NAME that point. Now you take the next "
                   "step: concede it, then answer it while keeping your side. Three moves do it:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Concede a real objection.</strong> Name a point the other "
                   "side would truly raise ('free transit costs taxpayers money'), not a fact everyone already "
                   "accepts.</li>"
                   "<li style=\"margin:4px 0\"><strong>Answer it with a reason.</strong> Give a reason that meets "
                   "that objection, not just a repeat of your side.</li>"
                   "<li style=\"margin:4px 0\"><strong>Hold your position.</strong> Keep a clear side. Do not "
                   "drift into 'both sides are right'; conceding sets up your answer, it does not replace "
                   "it.</li></ul>"
                   "Put together, that is the shape Although X, Y because Z. (Scoring calls the arguable claim "
                   "your response defends a "
                   "<dfn class=\"tb-glossary-term\" data-catalog-idref=\"def-thesis\" "
                   "title=\"Thesis means the one arguable claim your whole response defends. You do not need "
                   "this word to finish today's task.\">thesis</dfn>, but you do not need that word for today's "
                   "task.) Goal today: concede a real objection and answer it while holding your position.")),
        Slot("TEACH", "stimulus_display", "The debate: free public transit",
             ref="ACC-W910-FRAME-FREETRANSIT", bank="free_transit",
             body=("Read the short framing of the debate. Picture a writer whose claim is that cities should make "
                   "public transit free to ride. In a moment you will watch that writer concede the other side's "
                   "strongest point and answer it, then you will do it. Notice the strongest objection to free "
                   "fares, you will concede it without giving up your own position. You only need the topic and "
                   "the two sides.")),

        # ===== MODEL (before the quiz): coping-model think-aloud, named moves, then the check tool folded in ====
        Slot("MODEL", "annotated_before_after", "Watch a writer concede a point, then answer it",
             bank="free_transit",
             body=("Here is the skill in action. Follow the writer's thinking below. " + COPING_HTML +
                   " The two moves that turned the BEFORE into the AFTER: " + DECOMPOSE_HTML +
                   " When you write your own, build it the same way: concede a real objection first, then answer "
                   "it with a reason and hold your side, and run the 3 questions before you submit. " + REMEMBER)),
        Slot("MODEL", "discrimination", "Which one concedes a point AND answers it while holding the claim?",
             ref="", labeled_grade_c=True, bank="free_transit",
             body=("Now that you have seen one built, spot the target. The writer's claim is that cities should "
                   "make public transit free. Which sentence concedes a real objection AND answers it while still "
                   "holding the claim, instead of leaving out the answer, the concession, or the side? "
                   "(A) Although free transit really would cost taxpayers a lot of money, that cost is a fair "
                   "thing to bring up whenever anyone sits down and thinks hard about the whole idea for a while.  "
                   "(B) Although free transit costs taxpayers money, cities should make the buses free, because "
                   "getting people who cannot afford a car to work is worth that shared cost.  "
                   "(C) Cities really should make the buses completely free to ride, because free rides help the "
                   "people who cannot afford a car get to their jobs and to their classes each and every day.  "
                   "(D) Cities should make the buses free to ride, and that is exactly why free public transit is "
                   "the right choice for every single city in the country to go ahead and pick right now. "
                   "Correct: B concedes and answers. (B) concedes the cost objection, then answers it with a "
                   "reason and holds the claim. (A) concedes the cost but never answers it or takes a side. (C) "
                   "gives a reason and holds a side but concedes nothing from the other side. (D) just restates "
                   "the same claim twice and never concedes or answers. Concede, then answer and hold."),
             choices=[
                 {"id": "A",
                  "text": "Although free transit really would cost taxpayers a lot of money, that cost is a fair thing to bring up whenever anyone sits down and thinks hard about the whole idea for a while.",
                  "correct": False,
                  "why": "It concedes the cost, but it never answers that objection or takes a side. Conceding is only the first move; you still owe an answer and a held position."},
                 {"id": "B",
                  "text": "Although free transit costs taxpayers money, cities should make the buses free, because getting people who cannot afford a car to work is worth that shared cost.",
                  "correct": True,
                  "why": "Correct. It concedes a real objection (the cost), answers it with a reason, and still holds a clear side. That is concede-then-answer."},
                 {"id": "C",
                  "text": "Cities really should make the buses completely free to ride, because free rides help the people who cannot afford a car get to their jobs and to their classes each and every day.",
                  "correct": False,
                  "why": "It holds a side and gives a reason, but it concedes nothing the other side would raise, so it never faces the objection at all."},
                 {"id": "D",
                  "text": "Cities should make the buses free to ride, and that is exactly why free public transit is the right choice for every single city in the country to go ahead and pick right now.",
                  "correct": False,
                  "why": "It just restates the same claim twice. There is no concession and no reason that answers the other side, so it is not a concede-and-answer sentence."},
             ]),
        Slot("MODEL", "discrimination", "Which one concedes a REAL objection, not just a fact?",
             ref="", labeled_grade_c=True, bank="free_transit",
             body=("A different trap this time. Each sentence below holds the same clear side, make the buses "
                   "free, so holding is not the issue here. The catch is the concession: only one concedes a "
                   "point the other side would truly raise. Which one concedes a real objection AND answers it? "
                   "(A) Although free transit means taxpayers have to cover the whole cost, cities should make the "
                   "buses free, because getting low-income riders to their jobs is worth that shared cost.  "
                   "(B) Although buses and trains already run all across the city every single day of the week, "
                   "cities should make the buses free, because free rides help low-income riders get to work.  "
                   "(C) Although free buses would clearly help the low-income riders the very most of anyone, "
                   "cities should make the buses free, because helping those riders is exactly why free transit "
                   "is worth it.  "
                   "(D) Although free public transit is honestly just a good idea for a city to have, cities "
                   "should make the buses free, because free rides really are the right choice for the whole city. "
                   "Correct: A concedes a real objection. (A) concedes the cost, a point the other side truly "
                   "raises, then answers it. (B) concedes a neutral fact both sides accept, so it faces no "
                   "objection. (C) dresses up the writer's own reason as a concession. (D) just restates the "
                   "writer's own side in the although clause. Only (A) concedes the real other side and answers "
                   "it."),
             choices=[
                 {"id": "A",
                  "text": "Although free transit means taxpayers have to cover the whole cost, cities should make the buses free, because getting low-income riders to their jobs is worth that shared cost.",
                  "correct": True,
                  "why": "Correct. It concedes the cost, a real point the other side raises, then answers it with a reason and holds the side."},
                 {"id": "B",
                  "text": "Although buses and trains already run all across the city every single day of the week, cities should make the buses free, because free rides help low-income riders get to work.",
                  "correct": False,
                  "why": "The although clause states a neutral fact both sides accept. It concedes nothing the other side would argue, so there is no real objection here."},
                 {"id": "C",
                  "text": "Although free buses would clearly help the low-income riders the very most of anyone, cities should make the buses free, because helping those riders is exactly why free transit is worth it.",
                  "correct": False,
                  "why": "The although clause is really the writer's own reason for free transit, dressed up as a concession. It never faces the other side."},
                 {"id": "D",
                  "text": "Although free public transit is honestly just a good idea for a city to have, cities should make the buses free, because free rides really are the right choice for the whole city.",
                  "correct": False,
                  "why": "The although clause simply restates the writer's own side. A concession has to name the OTHER side's point, not repeat your own."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this concede-only sentence most need?",
             bank="free_transit",
             body=("Diagnose this draft before the reveal. A student wrote: 'Although free transit costs taxpayers "
                   "money, cities should make the buses free.' It concedes the cost and holds a side. Which single "
                   "move would most improve it? "
                   "(A) after conceding, answer the cost objection with a reason, and keep the claim  "
                   "(B) concede a second objection as well, naming another point the other side could raise here  "
                   "(C) make the whole sentence quite a bit longer and a good deal more formal without changing the idea  "
                   "(D) drop the concession completely and just assert the claim without noting any objection at all"),
             feedback=("Correct: A. The sentence concedes the cost and holds a side, but it never answers that "
                       "objection, so the other side's point is left standing. The fix is to add a reason that "
                       "answers it: 'Although free transit costs taxpayers money, cities should make the buses "
                       "free, because getting people who cannot afford a car to work is worth that shared cost.' A "
                       "second concession (B) or a longer, more formal sentence (C) still leaves the objection "
                       "unanswered; dropping the concession (D) throws away the concede-and-answer move "
                       "entirely.")),

        # ===== SUPPORTED: framed concede-and-answer write on the taught topic (source read at STEP 2) =====
        Slot("SUPPORTED", "production_frq", "Write a concede-and-answer sentence (with a frame)",
             ref="", bank="free_transit", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="The claim is: cities should make public transit free to ride. Use the frame below so you "
                       "can focus on the two moves: concede, then answer.",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "Although ______ [a real objection], ______ [your position, held] because ______ [a reason that answers it]."),
                 closer="Concede a real objection AND answer it with a reason while keeping a clear side. Do not "
                        "drift into 'both sides are right.' Then check it against the 3 questions.")),
        # DIAGNOSIS = a CHECK-and-FIX on a PROVIDED weak draft (concede-no-answer), so it is not a fresh production
        # and does not repeat the framed write. Stays on the taught topic = no new source to read (load balance).
        Slot("MODEL", "diagnosis_frq", "Check and fix a weak draft with the 3 questions",
             ref="", bank="free_transit", scored=True,
             body=frq_prompt(
                 intro="Run the 3-question test on this weak draft, then rewrite it into a real concede-and-answer sentence.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "Although free transit costs money, cities should just make the buses free anyway.", "red"),
                 checklist_block=checklist(title="Run the test:", rows=[
                     ("Did it concede a real objection (not a fact)?", "Yes, the cost is a real point the other side raises."),
                     ("Did it answer that objection with a reason?",
                      "No. It says 'anyway' but gives no reason, so the cost objection is left standing. Add a "
                      "reason that answers it, such as free rides getting low-income workers to their jobs."),
                     ("Does it still hold a clear position?", "Yes, it keeps the side that the buses should be free."),
                 ]),
                 closer="Now rewrite the weak draft into one concede-and-answer sentence that passes all three. "
                        "Then name, in a few words, the reason you used to answer the objection.")),

        # ===== INDEPENDENT: cold concede-and-answer write on the taught topic (no frame) =====
        Slot("INDEPENDENT", "production_frq", "Write a concede-and-answer sentence on your own",
             ref="", bank="free_transit", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="On your own now, no frame. The task: should cities make public transit free to ride? Take "
                       "a side.",
                 closer="Write ONE sentence that concedes a real objection, then answers it with a reason while "
                        "holding your side (Although X, Y because Z). Concede-and-answer is the move every real "
                        "counterargument is built on, and you are ready to do it cold. Do not drift into 'both "
                        "sides are right.' Check your sentence against the 3 questions before you submit.")),

        # ===== TRANSFER: same move, a NEW topic (four-day week), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "The debate: a four-day school week",
             ref="ACC-W910-FRAME-FOURDAYWEEK", bank="four_day_week",
             body=("A different debate now, so you build a fresh sentence instead of reusing the last one. Read "
                   "the short framing, then take a side. Notice the strongest objection to concede without giving "
                   "up your position, and get ready to answer it. You only need the topic and the two sides.")),
        Slot("TRANSFER", "production_frq", "Write a concede-and-answer sentence on a NEW topic",
             ref="", bank="four_day_week", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="New topic. The task: should schools switch to a four-day school week? Take a side.",
                 closer="Write ONE concede-and-answer sentence: concede a real objection, then answer it with a "
                        "reason while holding your side (Although X, Y because Z). Same move as the free-transit "
                        "sentence, new topic. Do not drift into 'both sides are right.' Check it against the 3 "
                        "questions before you submit.")),
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
