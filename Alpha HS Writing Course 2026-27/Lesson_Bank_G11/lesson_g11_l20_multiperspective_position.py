"""
lesson_g11_l20_multiperspective_position.py  -  G11 KC C.11.07, ARCHETYPE T2 (STAND, sentence). V3.1.

G11 course L20 (Unit 5, intro). E2 multi-perspective position: on an issue with three given perspectives,
WEIGH them against each other and STAKE your OWN position in relation to them, rather than summarizing the
three in turn. Written at the sentence. STAND=proposal. Taught set: MP-LESSON-0001 (public streets) ->
transfer set: MP-PERSP-0001 (automation and work). Source-free perspective sets (student argues from own
knowledge); no source markup; no prior-work ref; no named person (Timeback stateless rule); no em dashes.

V3.1 spine (matches the locked G9 L01 v3.1 template of the same T2/STAND archetype):
  1. TEACH one idea, hammered (ONE_IDEA teal callout + a real <ul> of the two answers), thesis in a tooltip.
  2. SOURCE = the bound streets perspective set.
  3. MODEL = a coping-model think-aloud (First try -> check -> catch -> Final) with a literal BEFORE and AFTER.
  4. Decompose the two moves (WEIGH, STAKE) + fold in the reusable 3-question check as a REMEMBER dashed box.
  5-6. Discrimination + predict-the-fix (reveal in the tail / feedback, never in the option text).
  7. SUPPORTED = a fill-in FRAME. 8. DIAGNOSIS = a check on a PROVIDED weak draft, then rewrite.
  9. INDEPENDENT = no frame, autonomy + say-the-standard. 10. TRANSFER = same move, the automation set.

ONE IDEA: weigh the given perspectives against each other, then stake your OWN position in relation to them.
ONE REMINDER: the 3-question weigh-and-stake check. Passes all 23 lesson_contract gates. Own words, no
fabricated figures, no em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">When a prompt hands you several set perspectives, '
'<strong>WEIGH</strong> them against each other and <strong>STAKE</strong> your own position in relation to '
'them. Reporting the three views one by one is not a position.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit any position, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does it WEIGH the views against each other (name where one holds, or where one depends on another)?</li>'
'<li style="margin:2px 0">Does it STAKE a position of your own, not just report theirs?</li>'
'<li style="margin:2px 0">Could a reader tell what YOU hold, not only what the three perspectives say?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, it is not a staked position yet.</div></div>')

# coping-model think-aloud: a WRITTEN drafting process (attempt -> check -> catch -> revise), then the endpoints.
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer thinking it through, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Perspective One wants traffic, Two wants a public '
    'room, and Three wants residents to decide." Check it: does it weigh the views or stake a position? No, it '
    'just lists the three and stops. Start over.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "Residents should decide what their street is for." '
    'Better, that takes a side someone could reject. But does it weigh the given views, showing how they relate? '
    'Not yet, and it drops Two entirely. Bring the views in.</p>'
    '<p style="margin:0"><strong>Final:</strong> "Perspective Three is right that street users should decide, '
    'but that only works once the city first protects Two\'s public-room use, so residents should choose within '
    'a rule that keeps some space for people, not cars alone." It weighs Two against Three, then stakes a '
    'position. That passes.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "Perspective One wants traffic, Two wants a public room, and '
    'Three wants residents to decide." (reports the three, takes no position)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "Perspective Three is right that street users should decide, '
    'but that only works once the city protects Two\'s public-room use, so residents should choose within a rule '
    'that keeps space for people, not cars alone." (weighs, then stakes)</span></div>'
'</div>')

DECOMPOSE_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#f0fdf4;padding:10px 14px;border-bottom:1px solid #bbf7d0;font-size:15px">'
    'The two moves that turned the BEFORE into the AFTER:</div>'
  '<div style="padding:12px 14px">'
    '<div style="margin:0 0 10px">'
      '<span style="display:inline-block;background:#dbeafe;color:#1e3a8a;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">MOVE 1 - WEIGH</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px"><strong>"but that only works once the city '
      'protects Two\'s public-room use"</strong> The writer measures Two against Three, showing where one view '
      'depends on another instead of listing them side by side.</div></div>'
    '<div>'
      '<span style="display:inline-block;background:#fef9c3;color:#854d0e;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">MOVE 2 - STAKE</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px">"...so <strong>residents should choose within a '
      'rule that keeps space for people</strong>." The writer commits to a position of their own, in relation to '
      'the given views.</div></div>'
    '<div style="margin-top:10px;color:#0f766e;font-size:13px">Weigh, then stake. That is the whole move. Every '
    'multi-perspective position you write is built the same way.</div>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1105-0020", grade="9-10", lesson_type=2,
    unit="G11 U5 - Multi-perspective position (weigh the given views, stake your own)",
    title="Weigh the Perspectives, Then Stake Your Own",
    target=("On an issue with several given perspectives, weigh them against each other and stake your own "
            "position in relation to them, rather than summarizing the perspectives one by one. Written at the "
            "sentence. Trait: Thesis (position in a conversation)."),
    acc_tags=["ACC.W.ARG.2", "CCSS.W.11-12.1"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.07", "sot": "icm course-G11.md L20",
                "taught_stimulus": "ACC-W1112-MP-LESSON-0001",
                "transfer_stimulus": "ACC-W910-MP-PERSP-0001",
                "playbook": "_phase2/playbook_T2_STAND.md",
                "one_idea": "Weigh the given perspectives against each other, then stake your own position in relation to them.",
                "one_reminder": "3-question weigh-and-stake check: weigh? stake? can a reader tell what YOU hold?",
                "template": "locked L01 template; PERSPECTIVE-SET tier binds the 3-perspective prompt (no passage).",
                "version_note": ("V3.1: rebuilt from the prose-wall pre-v3.1 to the locked G9 L01 v3.1 spine - "
                                 "ONE_IDEA callout + <ul> teach, coping-model think-aloud with literal "
                                 "BEFORE/AFTER, WEIGH/STAKE decompose + REMEMBER 3-question check, explicit "
                                 "discrimination choices with homogeneous length and no token confound, "
                                 "predict-the-fix reveal in feedback, fill-in frame -> diagnosis on a provided "
                                 "draft -> cold independent + say-the-standard -> transfer to the automation "
                                 "set. Removed the leaked 'Grade-C'/'design bet' student-facing labels."),
                "council": ("T2/STAND G11 multi-perspective intro: introduces E2 (weigh given perspectives, "
                            "stake own position in relation). weigh-and-stake vs summarize-the-three "
                            "discrimination labeled Grade-C in code only (labeled_grade_c=True). STAND=proposal.")},
    fade_ledger_moves=["multi-perspective-position", "weigh-then-stake"],
    slots=[
        # ===== TEACH: ONE idea only (the two answers as a real list; thesis in a tooltip) =====
        Slot("TEACH", "teach_card", "The one idea: weigh the views, then stake your own position",
             body=(ONE_IDEA +
                   "Some prompts hand you an issue and several set perspectives and ask you to respond. Two "
                   "answers look alike but do opposite jobs, so keep them apart:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>The weak answer SUMMARIZES</strong>: it reports the "
                   "perspectives in turn and says they all have a point, then commits to nothing.</li>"
                   "<li style=\"margin:4px 0\"><strong>The strong answer WEIGHS, then STAKES</strong>: it "
                   "measures the views against each other (which holds up, where one depends on another, where "
                   "one goes too far) and then commits to the writer's own position in relation to them.</li></ul>"
                   "Your position may agree with one view, combine two, or reject all three, but it must be "
                   "YOURS and must engage the given views, not float free of them. (Scoring calls this position "
                   "your <dfn class=\"tb-glossary-term\" data-catalog-idref=\"def-thesis\" "
                   "title=\"Thesis means the one-sentence position your whole response defends. You do not need "
                   "this word to finish today's task.\">thesis</dfn>, but you do not need that word for today's "
                   "task.) Today's task asks you to weigh the given perspectives and state your own position in "
                   "one sentence.")),
        Slot("TEACH", "stimulus_display", "Read the issue and three perspectives: public streets",
             ref="ACC-W1112-MP-LESSON-0001", bank="mp_public_space",
             body=("Read this issue on who a public street should serve, with three given perspectives (traffic "
                   "first; the street as a public room; the users should decide). There is no passage; you argue "
                   "from your own knowledge. As you read, note where the perspectives conflict and where one "
                   "depends on another. The prompt stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model think-aloud + WEIGH/STAKE decompose + the check tool =====
        Slot("MODEL", "annotated_before_after", "Watch a summary become a staked position",
             bank="mp_public_space",
             body=("Here is the skill in action. Follow the writer's thinking below, from a bare list of the "
                   "three views to a weighed, staked position. " + COPING_HTML +
                   " Two moves turned the BEFORE into the AFTER: the writer WEIGHED the views against each other, "
                   "then STAKED a position of their own. " + DECOMPOSE_HTML + REMEMBER +
                   "When you write your own, build it the same way: weigh the views first, then commit to your "
                   "position, and run the 3 questions before you submit.")),
        Slot("MODEL", "discrimination", "Which response weighs the views and stakes a position?",
             ref="", labeled_grade_c=True, bank="mp_public_space",
             body=("Now that you have seen one built, spot the target. Which response WEIGHS the perspectives and "
                   "STAKES a position, rather than just summarizing the three? "
                   "(A) Perspective One favors moving traffic, Perspective Two favors public gathering, and "
                   "Perspective Three favors letting locals decide, and honestly each of these three views "
                   "raises a fair and reasonable point about our streets.  "
                   "(B) Perspective One is right that a street must keep traffic moving, but it misses Two, whose "
                   "point is that a street with no room for people stops being public, so the city should keep "
                   "some streets for cars and some for people.  "
                   "(C) Streets clearly matter a great deal to everyone who lives in a busy city, so local "
                   "leaders really ought to think hard and choose quite carefully before they change any shared "
                   "street.  "
                   "(D) Perspective One is simply correct that a street's first job is to move traffic, so the "
                   "city should design every street around keeping cars flowing. "
                   "Correct: B. It measures One against Two and lands the writer's own position. (A) reports "
                   "the three and commits to nothing. (C) sounds decisive but never engages the given views. (D) "
                   "adopts one view whole without weighing it against the others."),
             choices=[
                 {"id": "A", "text": "Perspective One favors moving traffic, Perspective Two favors public gathering, and Perspective Three favors letting locals decide, and honestly each of these three views raises a fair and reasonable point about our streets.",
                  "correct": False,
                  "why": "This reports the three perspectives in turn and says they all have a point. Naming each view is not weighing them, and 'each raises a fair point' commits to no position of your own."},
                 {"id": "B", "text": "Perspective One is right that a street must keep traffic moving, but it misses Two, whose point is that a street with no room for people stops being public, so the city should keep some streets for cars and some for people.",
                  "correct": True,
                  "why": "Correct. It weighs One against Two (One is right about traffic, but misses Two's point about public space) and then stakes the writer's own position in relation to them. Weigh, then stake, is the move."},
                 {"id": "C", "text": "Streets clearly matter a great deal to everyone who lives in a busy city, so local leaders really ought to think hard and choose quite carefully before they change any shared street.",
                  "correct": False,
                  "why": "This sounds decisive and uses 'should,' but it never touches the three given views or measures them against each other. Calling for careful thought is not a position on the issue."},
                 {"id": "D", "text": "Perspective One is simply correct that a street's first job is to move traffic, so the city should design every street around keeping cars flowing.",
                  "correct": False,
                  "why": "This commits to a position and names Perspective One, but it adopts that one view whole without measuring it against Two or Three, so it stakes without weighing."},
             ]),
        Slot("MODEL", "discrimination", "Weigh and stake, or only name the tension?",
             ref="", labeled_grade_c=True, bank="mp_public_space",
             body=("Here is a second set on the same streets issue. Which response WEIGHS the perspectives "
                   "against each other AND stakes a position of the writer's own, rather than stopping at the "
                   "tension between them or just asserting one view? "
                   "(A) Perspective One's push for faster traffic runs straight into Perspective Two's call for "
                   "gathering space, and Perspective Three's demand that residents themselves make the choice "
                   "only sharpens the clash, so the three given views clearly pull hard against one another "
                   "here.  "
                   "(B) Perspective Two is right that a street should be a place people gather, but that fails "
                   "wherever cars have nowhere else to go, so the city should add gathering space only on "
                   "streets that already have a parallel route.  "
                   "(C) Residents by themselves should simply decide what their own street becomes, and that is "
                   "the fairest way to settle it.  "
                   "(D) Perspective One cares about traffic, Perspective Two cares about gathering space, and "
                   "Perspective Three cares about local choice, so the issue of what a street is for turns out to "
                   "be a genuinely complicated one. "
                   "Correct: B. It measures Two against the traffic view and lands the writer's own rule. (A) "
                   "shows the clash but stops at naming the tension. (C) picks a side without weighing the views "
                   "against each other. (D) just reports the three and calls the issue complicated."),
             choices=[
                 {"id": "A", "text": "Perspective One's push for faster traffic runs straight into Perspective Two's call for gathering space, and Perspective Three's demand that residents themselves make the choice only sharpens the clash, so the three given views clearly pull hard against one another here.",
                  "correct": False,
                  "why": "This weighs the views by showing how they clash, but it stops at naming the tension and never commits to a position of your own."},
                 {"id": "B", "text": "Perspective Two is right that a street should be a place people gather, but that fails wherever cars have nowhere else to go, so the city should add gathering space only on streets that already have a parallel route.",
                  "correct": True,
                  "why": "Correct. It measures Two against the traffic view and then commits to the writer's own rule, so it both weighs and stakes."},
                 {"id": "C", "text": "Residents by themselves should simply decide what their own street becomes, and that is the fairest way to settle it.",
                  "correct": False,
                  "why": "This commits to a side, but it just asserts one view without measuring it against the others, so it stakes without weighing."},
                 {"id": "D", "text": "Perspective One cares about traffic, Perspective Two cares about gathering space, and Perspective Three cares about local choice, so the issue of what a street is for turns out to be a genuinely complicated one.",
                  "correct": False,
                  "why": "This reports what each perspective cares about and concludes the issue is complicated. It neither measures the views against each other nor commits to a position, so it does neither move."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this multi-perspective response most need?",
             bank="mp_public_space",
             body=("Diagnose this draft before the reveal. A student wrote: 'All three perspectives are "
                   "interesting and each has real strengths and weaknesses, so the issue is complicated.' Which "
                   "single move would most improve it? "
                   "(A) weigh the perspectives against each other and stake the writer's own position in "
                   "relation to them  "
                   "(B) state even more strongly that all three perspectives are interesting and each one has "
                   "some genuine merit  "
                   "(C) summarize each of the three perspectives one more time, this time in fuller and more "
                   "careful detail  "
                   "(D) add a sentence explaining that this issue is very important and deserves careful thought "
                   "from all of us"),
             feedback=("Correct: A. 'Each has strengths and weaknesses, so it is complicated' is exactly the "
                       "non-committal summary the task penalizes. The fix is the two moves you just saw: weigh "
                       "the views against each other, then commit to your own position. Praising them (B), "
                       "re-summarizing (C), or calling the issue important (D) all still take no position.")),

        # ===== SUPPORTED: framed write (fill-in frame) on the taught topic (source already read at slot 2) =====
        Slot("SUPPORTED", "production_frq", "Finish the position: fill in the frame",
             ref="", bank="mp_public_space", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on the two moves: weigh, then stake.",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "Perspective ___ is right that ___, but ___, so I hold that ___."),
                 closer="Measure the views against each other AND land your own position in relation to them. Do "
                        "not just summarize the three. Write one sentence, then check it against the 3 questions.")),
        # DIAGNOSIS = a CHECK-and-FIX exercise on a PROVIDED draft (self-contained; no look-back at prior work).
        Slot("MODEL", "diagnosis_frq", "Check and fix a weak draft with the 3 questions",
             ref="", bank="mp_public_space", scored=True,
             body=frq_prompt(
                 intro="Run the 3-question check on this provided weak draft, then rewrite it into a real "
                       "position.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "Each perspective on streets has a good point, and the answer is "
                                         "somewhere in the middle.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Does it WEIGH the views against each other?", "your call: yes / no"),
                     ("Does it STAKE a position of your own?", "your call: yes / no"),
                     ("Could a reader tell what YOU hold?", "your call: yes / no"),
                 ]),
                 closer="Now rewrite the weak draft into one weighed, staked position on the streets issue that "
                        "passes all three. Then name which question your rewrite fixed.")),

        # ===== INDEPENDENT: cold write on the same issue, no frame + autonomy + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Weigh and stake on your own",
             ref="", bank="mp_public_space", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now, no frame. Write ONE position on the streets issue that weighs the given "
                       "perspectives against each other and stakes your own position in relation to them.",
                 closer="Take the position you actually hold, then show how it measures against the given views. "
                        "This weigh-then-stake move is what every real multi-perspective response is built on, "
                        "and you are ready to do it cold. Check your sentence against the 3 questions before you "
                        "submit.")),

        # ===== TRANSFER: same move, a NEW perspective set (automation + work), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW perspective set: automation and work",
             ref="ACC-W910-MP-PERSP-0001", bank="mp_automation_work",
             body=("Read this new issue on the value of human work as machines advance, with three given "
                   "perspectives. There is no passage; you argue from your own knowledge. Note where the "
                   "perspectives conflict and where one depends on another. The prompt stays on screen while you "
                   "work.")),
        Slot("TRANSFER", "production_frq", "Weigh and stake on a NEW set",
             ref="", bank="mp_automation_work", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="New set. Write ONE position on the automation-and-work issue that weighs the given "
                       "perspectives and stakes your own in relation to them.",
                 closer="Same weigh-then-stake move as the streets issue, new topic. Do not just summarize the "
                        "three. Check it against the 3 questions before you submit.")),
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
