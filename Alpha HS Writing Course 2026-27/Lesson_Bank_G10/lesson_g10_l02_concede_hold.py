"""
lesson_g10_l02_concede_hold.py  -  G10 KC C.10.01, ARCHETYPE T2: CLAIM-BUILDING (STAND, sentence). V3.1.

G10 course L02 (Unit 1, guided). The signature error of the counterclaim move: concede-and-HOLD vs
concede-and-COLLAPSE (giving away your own position while conceding). Recycles the DST issue frame.
CLAIM-TIER binds issue_frame. Taught: FRAME-DST -> transfer: FRAME-SCHOOLYEAR (bank-partitioned). rc.staar,
unit="sentence". STAND=proposal. No named persona (Timeback stateless rule); no source markup; no prior-work
ref; no em dashes.

V3.1 spine: ONE_IDEA teal callout + minimal LIST teach -> bound source -> coping-model think-aloud
(draft -> check -> catch collapse -> hold) with literal BEFORE/AFTER -> named CONCEDE/HOLD moves + REMEMBER
3-question check tool -> discrimination (choices=, homogeneous length, confound broken, reveal in tail) ->
predict-the-fix (reveal in feedback) -> SUPPORTED framed write -> DIAGNOSIS check-and-fix on a provided
weak draft -> INDEPENDENT cold write + say-the-standard -> TRANSFER on the partitioned school-year frame.

ONE IDEA: conceding is a strength ONLY if you still HOLD your position. ONE REMINDER: the 3-question test.
Passes all 23 lesson_contract gates. Own words, no fabricated figures, no em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Conceding a point is a strength, but only if you '
'still <strong>HOLD</strong> your position. Concede to set up a stronger stand, never to surrender it.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit any concede-and-hold claim, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Did you name a real objection (concede)?</li>'
'<li style="margin:2px 0">After conceding, do you still hold a clear side?</li>'
'<li style="margin:2px 0">Is there a reason for the side you hold?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If the middle answer is no, the claim has collapsed. Hold a side.</div></div>')

# coping-model think-aloud panel: a WRITTEN drafting process (concede -> catch the collapse -> hold), then endpoints.
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer thinking it through, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Both sides of the clock debate make good points." '
    'Check it: does it hold a side? No, it names no position at all. Pick one and be fair to the other.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "Although the switch disrupts sleep, both sides have '
    'fair points, so it is hard to say what we should do." Better, it concedes now. But does it still hold a '
    'position? No, "hard to say" gives it away. That is a collapse. Hold a side after conceding.</p>'
    '<p style="margin:0"><strong>Final:</strong> "Although picking one fixed time has real trade-offs, the '
    'country should still end the twice-a-year switch, because a steady clock spares people the health costs of '
    'losing sleep every spring." It concedes, holds a side, and gives a reason. That passes.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "Although the switch disrupts sleep, both sides have fair '
    'points, so it is hard to say what we should do." (concedes, then collapses)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "Although picking one fixed time has real trade-offs, the '
    'country should still end the switch, because a steady clock spares people lost sleep every spring." '
    '(concedes, then holds)</span></div>'
'</div>')

DECOMPOSE_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#f0fdf4;padding:10px 14px;border-bottom:1px solid #bbf7d0;font-size:15px">'
    'The finished claim: <em>"Although picking one fixed time has real trade-offs, the country should still end '
    'the switch, because a steady clock spares people lost sleep every spring."</em></div>'
  '<div style="padding:12px 14px">'
    '<div style="margin:0 0 10px">'
      '<span style="display:inline-block;background:#fef9c3;color:#854d0e;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">MOVE 1 - CONCEDE</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px"><strong>"Although picking one fixed time has '
      'real trade-offs"</strong> The writer names a real objection the other side would raise, fairly.</div></div>'
    '<div>'
      '<span style="display:inline-block;background:#dbeafe;color:#1e3a8a;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">MOVE 2 - HOLD</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px">"...<strong>the country should still end the '
      'switch, because a steady clock spares people lost sleep</strong>." The writer keeps a clear side and '
      'gives a reason, instead of drifting into "it is hard to say."</div></div>'
    '<div style="margin-top:10px;color:#0f766e;font-size:13px">Concede, then hold with a reason. The concession '
    'sets up the stand; it never replaces it.</div>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1001-0002", grade="9-10", lesson_type=2,
    unit="G10 U1 - Counterargument (concede and hold, not collapse)",
    title="Concede Without Giving Up Your Position",
    target=("Concede a real objection AND still hold your position (concede-and-hold), rather than conceding so "
            "far that you abandon your own claim (concede-and-collapse). Written at the sentence. Trait: "
            "Thesis/Purpose."),
    acc_tags=["ACC.W.ARG.2", "CCSS.W.9-10.1a"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.01", "sot": "icm course-G10.md L02",
                "taught_stimulus": "ACC-W910-FRAME-DST",
                "transfer_stimulus": "ACC-W910-FRAME-SCHOOLYEAR",
                "playbook": "_phase2/playbook_T2_STAND.md",
                "template": "locked v3.1 L01 template (lesson_g9_l01_arguable_claim_v3_1); CLAIM-TIER binds issue_frame.",
                "one_idea": "Conceding is a strength only if you still HOLD your position.",
                "one_reminder": "3-question test: conceded a real objection? still hold a side? reason for it?",
                "version_note": ("V3.1: rebuilt to the locked v3.1 spine - ONE_IDEA teal callout + minimal list "
                                 "teach, coping-model think-aloud (concede -> catch collapse -> hold) with "
                                 "literal BEFORE/AFTER, named CONCEDE/HOLD moves + REMEMBER check tool, "
                                 "discrimination via explicit choices= (homogeneous length, since/because "
                                 "confound broken, reveal in tail), predict-the-fix reveal in feedback, framed "
                                 "SUPPORTED write, check-and-fix DIAGNOSIS, autonomy + say-the-standard on the "
                                 "cold INDEPENDENT write. Replaces the PRE-v3.1 prose walls + leaked Grade-C "
                                 "label."),
                "council": ("T2/STAND counterargument guided rung: the signature error is concede-and-collapse "
                            "(giving away the position while conceding). hold-vs-collapse discrimination is the "
                            "Grade-C discriminate-before-produce bet (labeled in code, never in student text). "
                            "STAND=proposal; sentence ceiling.")},
    fade_ledger_moves=["concede-and-hold", "avoid-concede-and-collapse"],
    slots=[
        # ===== TEACH: ONE idea only, minimal list; counterclaim + thesis defined here (define_before_use) =====
        Slot("TEACH", "teach_card", "The one idea: concede, then HOLD",
             body=(ONE_IDEA +
                   "A counterclaim is a point that someone who disagrees with you would make. When you concede "
                   "one, it can go two ways, and they are easy to mix up:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Concede-and-HOLD</strong>: you name the other side's real "
                   "point, then keep your claim with a reason ('Although X, Y because Z').</li>"
                   "<li style=\"margin:4px 0\"><strong>Concede-and-COLLAPSE</strong> (the trap): you name the "
                   "other side's point and then drift into 'both sides are right, it is hard to say', giving "
                   "your own position away.</li></ul>"
                   "A reader should finish your sentence knowing exactly where you stand. (Scoring calls the "
                   "arguable claim your response defends a "
                   "<dfn class=\"tb-glossary-term\" data-catalog-idref=\"def-thesis\" "
                   "title=\"Thesis means the one arguable claim your whole response defends. You do not need "
                   "this word to finish today's task.\">thesis</dfn>, and a collapsing claim leaves no thesis "
                   "at all, but you do not need that word for today's task.) Goal today: concede a real point "
                   "and still hold your position.")),
        Slot("TEACH", "stimulus_display", "The debate: daylight saving time",
             ref="ACC-W910-FRAME-DST", bank="daylight_saving",
             body=("Read the short framing of the debate. In a moment you will watch a claim get built, then "
                   "build your own. Notice the strongest point on the other side, you will concede it without "
                   "giving up your own position. You only need the topic and the two sides.")),

        # ===== MODEL (before the quiz): coping-model think-aloud, named moves, then the check tool folded in =====
        Slot("MODEL", "annotated_before_after", "Watch a writer concede without collapsing",
             bank="daylight_saving",
             body=("Here is the skill in action. Follow the writer's thinking below. " + COPING_HTML +
                   " The two moves that turned the BEFORE into the AFTER: " + DECOMPOSE_HTML +
                   " When you write your own, build it the same way: concede first, then hold a side with a "
                   "reason, and run the 3 questions before you submit. " + REMEMBER)),
        Slot("MODEL", "discrimination", "Which one concedes AND holds?",
             ref="", labeled_grade_c=True, bank="daylight_saving",
             body=("Now that you have seen one built, spot the target. All three concede a trade-off about the "
                   "clock switch. Which one still HOLDS a clear position (concede-and-hold), instead of "
                   "collapsing into 'it is hard to say'? "
                   "(A) Although fixed time has trade-offs, both sides make fair points, and because each side "
                   "has real evidence it is honestly hard to say what the whole country should end up deciding.  "
                   "(B) Although fixed time has trade-offs, the country should still end the twice-a-year "
                   "switch, since a steady clock spares people lost sleep every spring.  "
                   "(C) Although fixed time has trade-offs, the issue stays complicated, since reasonable people "
                   "are going to keep on disagreeing about it for a long time. "
                   "Correct: B holds. (B) concedes the trade-off but keeps its position with a reason. (A) and "
                   "(C) concede and then abandon their position, leaving no thesis. Concede-and-hold is the move."),
             choices=[
                 {"id": "A",
                  "text": "Although fixed time has trade-offs, both sides make fair points, and because each side has real evidence it is honestly hard to say what the whole country should end up deciding.",
                  "correct": False,
                  "why": "This has the word 'because,' but it concedes and then collapses into 'hard to say,' leaving no position. A because-clause does not hold a side."},
                 {"id": "B",
                  "text": "Although fixed time has trade-offs, the country should still end the twice-a-year switch, since a steady clock spares people lost sleep every spring.",
                  "correct": True,
                  "why": "Correct. It concedes the trade-off, then still holds a clear side ('should still end the switch') and backs it with a reason. Concede-and-hold."},
                 {"id": "C",
                  "text": "Although fixed time has trade-offs, the issue stays complicated, since reasonable people are going to keep on disagreeing about it for a long time.",
                  "correct": False,
                  "why": "This concedes, then collapses into 'the issue stays complicated' and never takes a side. Conceding is not supposed to end in a shrug."},
             ]),
        Slot("MODEL", "discrimination", "Which one concedes a REAL point from the other side?",
             ref="", labeled_grade_c=True, bank="daylight_saving",
             body=("A different trap this time. All three sentences below hold the same clear side, end the "
                   "clock switch, so holding is not the issue here. The catch is the concession itself: only one "
                   "names a point the other side would truly raise. Which one really concedes and holds? "
                   "(A) Although later evening light is genuinely popular with many families, the country should "
                   "still end the switch, since steady sleep matters more.  "
                   "(B) Although the twice-a-year change costs people real sleep, the country should end the "
                   "switch, because that same lost sleep is exactly what makes the change so harmful to families.  "
                   "(C) Although nearly everyone checks a clock many times a day, the country should end the "
                   "switch, because one fixed time keeps ordinary routines simpler. "
                   "Correct: A concedes. (A) names a real benefit the other side points to, popular evening "
                   "light, then still holds its side. (B) only dresses up its own reason as a concession, and "
                   "(C) concedes a neutral fact nobody disputes, so neither truly faces the other side."),
             choices=[
                 {"id": "A",
                  "text": "Although later evening light is genuinely popular with many families, the country should still end the switch, since steady sleep matters more.",
                  "correct": True,
                  "why": "Correct. It concedes a real benefit the other side points to, popular evening light, then still holds its side with a reason."},
                 {"id": "B",
                  "text": "Although the twice-a-year change costs people real sleep, the country should end the switch, because that same lost sleep is exactly what makes the change so harmful to families.",
                  "correct": False,
                  "why": "This uses 'although,' but the point it concedes is really its own reason for ending the switch, so it never faces the other side."},
                 {"id": "C",
                  "text": "Although nearly everyone checks a clock many times a day, the country should end the switch, because one fixed time keeps ordinary routines simpler.",
                  "correct": False,
                  "why": "The 'although' clause states a neutral fact nobody is arguing about, so nothing the other side holds is actually conceded."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this collapsing claim most need?",
             bank="daylight_saving",
             body=("Diagnose this draft before the reveal. A student wrote: 'Although the clock switch hurts "
                   "sleep, there are good arguments on both sides, so it is complicated.' Which single move "
                   "would most improve the claim? "
                   "(A) after conceding, hold a clear position and back it with a reason  "
                   "(B) concede a second objection as well, naming another fair point the other side could raise here  "
                   "(C) spell out the other side's objection in much fuller and more thorough detail before moving on  "
                   "(D) drop the concession completely and just assert one position without noting any objection at all"),
             feedback=("Correct: A. The claim concedes and then collapses into 'it is complicated,' leaving no "
                       "position. The fix is to hold after conceding: 'Although the switch hurts sleep, the "
                       "country should end it because a steady clock spares that harm.' A second concession (B) "
                       "or a longer one (C) makes the collapse worse; removing the concession (D) throws away "
                       "the counterclaim-aware move entirely.")),

        # ===== SUPPORTED: framed write (fill-in frame) on the taught topic (source already read at STEP 2) =====
        Slot("SUPPORTED", "production_frq", "Write a concede-and-hold claim",
             ref="", bank="daylight_saving", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on the two moves: concede, then hold.",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "Although ______ [a real objection], ______ [your position, held] because ______ [a reason]."),
                 closer="Concede a real point AND keep a clear position with a reason. Do not drift into 'both "
                        "sides are right.' Then check it against the 3 questions.")),
        # DIAGNOSIS = a CHECK-and-FIX exercise on a PROVIDED draft (not a fresh production, so it does not repeat
        # the framed write). Stays on the taught topic = no new source to read (load balance).
        Slot("MODEL", "diagnosis_frq", "Check and fix a weak draft with the 3 questions",
             ref="", bank="daylight_saving", scored=True,
             body=frq_prompt(
                 intro="Run the 3-question test on this weak draft, then rewrite it into a real concede-and-hold claim.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "Although some people like evening light, it is hard to know the best answer.", "red"),
                 checklist_block=checklist(title="Run the test:", rows=[
                     ("Did it name a real objection (concede)?", "Yes, evening light is a real point."),
                     ("After conceding, does it hold a clear side?", "No, 'hard to know' collapses. State a side."),
                     ("Is there a reason for that side?", "No. Add one with 'because'."),
                 ]),
                 closer="Now rewrite the weak draft into one concede-and-hold claim that passes all three. Then "
                        "name your held position in a few words.")),

        # ===== INDEPENDENT: cold write on the taught topic (only 2 bound frames), no frame, say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write a concede-and-hold claim on your own",
             ref="", bank="daylight_saving", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="On your own now, no frame. The task: should the United States stop switching the clocks twice a year?",
                 closer="Concede a real objection, then hold a clear side with a reason. This concede-and-hold "
                        "move is what every real counterargument is built on, and you are ready to do it cold. "
                        "Do not collapse into 'both sides are right.' Check your sentence against the 3 "
                        "questions before you submit.")),

        # ===== TRANSFER: same move, a NEW topic (school year), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "The debate: a longer school year",
             ref="ACC-W910-FRAME-SCHOOLYEAR", bank="school_year",
             body=("A different debate now, so you build a fresh claim instead of reusing the last one. Read the "
                   "short framing, then take a side. Notice the strongest objection to concede without giving up "
                   "your position. You only need the topic and the two sides.")),
        Slot("TRANSFER", "production_frq", "Write a concede-and-hold claim on a NEW topic",
             ref="", bank="school_year", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="New topic. The task: should the United States lengthen the school year with more instructional days?",
                 closer="Write ONE concede-and-hold claim: concede a real objection, then hold a clear position "
                        "with a reason. Same move as the clock claim, new topic. Do not collapse into 'both "
                        "sides are right.' Check it against the 3 questions before you submit.")),
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
