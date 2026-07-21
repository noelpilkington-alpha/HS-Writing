"""
lesson_g9_l19_recognize_counterargument_v3_1.py  -  G9 KC C.9.07, ARCHETYPE T2 (STAND, sentence). V3.1.

G9 U4 OPENER (the new Counterargument unit). RECOGNITION rung only: given a claim, identify the strongest
REAL counterargument (a point someone who disagrees would make), and tell a genuine objection apart from a
neutral fact, a restatement of your own claim, and a strawman. This lesson NAMES the other side; it does NOT
build a concede-and-hold sentence (that is the next lesson) and it does NOT teach the concede-and-collapse
failure mode (reserved for the deeper G10 spiral). Taught: FRAME-COMMUNITYSERVICE (bank community_service) ->
transfer: FRAME-PAYGRADES (bank pay_for_grades), partitioned. Topics deliberately DIFFER from the G10
counterargument set (daylight_saving/school_year/congestion), so no collision. rc.staar, unit="sentence".
STAND=proposal. No named persona, no source markup, no prior-work ref, no em dashes.

V3.1 spine: ONE_IDEA teal callout + minimal LIST teach (define counterargument/counterclaim + thesis tooltip)
-> bound issue frame -> coping-model think-aloud (try a fact -> try a restatement -> catch them -> name the
real point) with literal BEFORE/AFTER -> named OPPOSES/FAIR moves + REMEMBER 3-question check tool ->
discrimination x2 (choices=, homogeneous length, reveal in tail + per-choice why) -> predict-the-fix (reveal
in feedback) -> SUPPORTED framed naming write -> DIAGNOSIS check-and-fix on a provided strawman -> INDEPENDENT
cold naming write -> TRANSFER on the partitioned pay-for-grades frame.

ONE IDEA: a counterargument is the point someone who DISAGREES with your claim would make; naming it fairly is
the first step. ONE REMINDER: the 3-question test (opposes? real, not a strawman? strongest version?).
Passes all lesson_contract gates. Own words, no fabricated figures, no em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A counterargument is the point that someone who '
'<strong>disagrees</strong> with your claim would make, such as, "Forcing students to serve drains the meaning '
'out of a generous act." Naming that point fairly is the first step of a strong argument.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you call something a counterargument, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does it actually oppose my claim (not just repeat a fact both sides accept)?</li>'
'<li style="margin:2px 0">Would someone on the other side really say it (not a weak version I made up)?</li>'
'<li style="margin:2px 0">Is it the strongest form of their point?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, it is not the real other side yet.</div></div>')

# coping-model think-aloud panel: a WRITTEN process (try a fact -> try a restatement -> catch both -> name the
# real point), then the endpoints. The writer's own claim here: schools should require community service.
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer thinking it through (the writer\'s own claim: schools should require community service):</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Many students already volunteer on their own." '
    'Check it: does this oppose my claim? No, it is a fact both sides would accept. A fact is not a counterargument.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "Community service teaches responsibility, so schools '
    'should require it." Better wording, but is this the OTHER side? No, that is my own point again. I need the '
    'point of someone who disagrees.</p>'
    '<p style="margin:0"><strong>Final:</strong> "Someone who disagrees would say that forcing students to serve '
    'turns a generous act into just another box to check, which drains its meaning." It opposes my claim, the '
    'other side would really say it, and it is their strongest point. That is a real counterargument.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "Many students already volunteer on their own." '
    '(a neutral fact, not the other side)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "Forcing students to serve turns a generous act into just '
    'another box to check, which drains its meaning." (a real point the other side would make)</span></div>'
'</div>')

DECOMPOSE_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#f0fdf4;padding:10px 14px;border-bottom:1px solid #bbf7d0;font-size:15px">'
    'The finished counterargument: <em>"Forcing students to serve turns a generous act into just another box to '
    'check, which drains its meaning."</em></div>'
  '<div style="padding:12px 14px">'
    '<div style="margin:0 0 10px">'
      '<span style="display:inline-block;background:#fef9c3;color:#854d0e;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">MOVE 1 - OPPOSES THE CLAIM</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px"><strong>"Forcing students to serve turns a '
      'generous act into just another box to check"</strong> gives a reason AGAINST requiring service, not a '
      'neutral fact and not the writer\'s own point.</div></div>'
    '<div>'
      '<span style="display:inline-block;background:#dbeafe;color:#1e3a8a;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">MOVE 2 - FAIR AND STRONGEST</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px">"...<strong>which drains its meaning</strong>" '
      'states the objection in the real, strongest form the other side would actually use, not a weak '
      'caricature.</div></div>'
    '<div style="margin-top:10px;color:#0f766e;font-size:13px">Oppose the claim, and state it fairly and at full '
    'strength. That is what makes it the real other side.</div>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C904-0030", grade="9-10", lesson_type=2,
    unit="G9 U4 - Counterargument (recognize the other side)",
    title="Name the Other Side",
    target=("Given a claim, identify the strongest real counterargument (a point someone who disagrees would "
            "make), and tell a genuine objection apart from a neutral fact, a restatement, or a strawman. "
            "Written at the sentence. Trait: Thesis/Purpose."),
    acc_tags=["ACC.W.ARG.2", "CCSS.W.9-10.1a"],
    provenance={"copyright": "own_authored", "authored": "2026-07-21",
                "mnemonic_status": "proposal", "kc": "C.9.07",
                "sot": "KC_Map_and_Unit_Arch_G9-12.md (G9 U4 - Counterargument)",
                "taught_stimulus": "ACC-W910-FRAME-COMMUNITYSERVICE",
                "transfer_stimulus": "ACC-W910-FRAME-PAYGRADES",
                "template": "locked v3.1 spine (lesson_g10_l02_concede_hold); recognition-level adaptation.",
                "one_idea": "A counterargument is the point someone who disagrees with your claim would make; name it fairly first.",
                "one_reminder": "3-question test: does it oppose the claim? would the other side really say it? is it their strongest version?",
                "version_note": ("V3.1 build to the locked spine: ONE_IDEA teal callout + minimal list teach "
                                 "(counterargument/counterclaim defined + thesis tooltip), coping-model think-aloud "
                                 "(try a fact -> try a restatement -> catch both -> name the real point) with "
                                 "literal BEFORE/AFTER, named OPPOSES/FAIR moves + REMEMBER 3-question check tool, "
                                 "two leak-free discriminations via explicit choices= (homogeneous length, per-choice "
                                 "why, reveal in tail), predict-the-fix reveal in feedback, framed SUPPORTED naming "
                                 "write, check-and-fix DIAGNOSIS on a provided strawman, cold INDEPENDENT naming "
                                 "write, and a partitioned pay-for-grades TRANSFER."),
                "council": ("G9 RECOGNITION rung of the counterargument ladder: this lesson only NAMES the other "
                            "side and sorts a real objection from a neutral fact, a restatement, and a strawman. "
                            "Concede-and-hold sentence construction is the NEXT G9 lesson; the deeper "
                            "concede-and-collapse failure mode and evidence-rebuttal are deliberately reserved for "
                            "the G10 spiral (lesson_g10_l02_concede_hold). Recognition + naming only keeps the "
                            "cognitive load at the sentence, appropriate for the unit opener. STAND=proposal; "
                            "sentence ceiling.")},
    fade_ledger_moves=["recognize-counterargument", "sort-objection-from-fact-restatement-strawman"],
    slots=[
        # ===== TEACH: ONE idea only, minimal list; counterargument/counterclaim + thesis defined here =====
        Slot("TEACH", "teach_card", "The one idea: name the point of someone who disagrees",
             body=(ONE_IDEA +
                   "A counterclaim, also called a counterargument, is a point that someone who disagrees with your "
                   "claim would make. It is not the same as three things people mix up with it:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>A neutral fact</strong> that both sides accept "
                   "('many students already volunteer') does not oppose your claim, so it is not a "
                   "counterargument.</li>"
                   "<li style=\"margin:4px 0\"><strong>A restatement of your own claim</strong> ('service is "
                   "good, so require it') is your side again, not the other side.</li>"
                   "<li style=\"margin:4px 0\"><strong>A strawman</strong> is a weak, unfair version of the other "
                   "side ('they just do not care about anyone') that is easy to knock down but nobody really "
                   "holds.</li></ul>"
                   "A real counterargument opposes your claim, states the other side fairly, and gives their "
                   "strongest point. (Scoring calls the arguable claim your response defends a "
                   "<dfn class=\"tb-glossary-term\" data-catalog-idref=\"def-thesis\" "
                   "title=\"Thesis means the one arguable claim your whole response defends. You do not need "
                   "this word to finish today's task.\">thesis</dfn>, but you do not need that word for today's "
                   "task.) Goal today: given a claim, name the strongest real point on the other side.")),
        Slot("TEACH", "stimulus_display", "The debate: required community service",
             ref="ACC-W910-FRAME-COMMUNITYSERVICE", bank="community_service",
             body=("Read the short framing of the debate. Picture a writer whose claim is that schools should "
                   "require community service to graduate. In a moment you will watch that writer name the other "
                   "side, then you will do it. Notice the strongest point AGAINST the requirement. You only need "
                   "the topic and the two sides.")),

        # ===== MODEL (before the quiz): coping-model think-aloud, named moves, then the check tool folded in ====
        Slot("MODEL", "annotated_before_after", "Watch a writer name the other side",
             bank="community_service",
             body=("Here is the skill in action. Follow the writer's thinking below. " + COPING_HTML +
                   " The two things that turned the BEFORE into the AFTER: " + DECOMPOSE_HTML +
                   " When you name the other side, do it the same way: find a point that opposes the claim, then "
                   "state it fairly and at full strength, and run the 3 questions before you call it done. " +
                   REMEMBER)),
        Slot("MODEL", "discrimination", "Which one is a real counterargument?",
             ref="", labeled_grade_c=True, bank="community_service",
             body=("Now that you have seen one built, spot the target. The writer's claim is that schools should "
                   "require community service to graduate. Which option below is a real counterargument (a point "
                   "the other side would make), not a fact, a restatement, or a strawman? "
                   "(A) Forcing students to serve can turn a genuine act of giving into one more box to check, which drains its real meaning.  "
                   "(B) A large share of high school students all across the country already take part in some kind of volunteer work each year.  "
                   "(C) Schools really should require community service, because helping out in the community is a good thing for every student.  "
                   "(D) The people who are against the rule simply do not care about anyone else and would rather just stay home doing nothing. "
                   "Correct: A opposes the claim with the other side's real point. (B) is a neutral fact both "
                   "sides accept, so it opposes nothing. (C) restates the writer's own claim, so it is not the "
                   "other side at all. (D) is a strawman, a weak and unfair version of the other side that nobody "
                   "really holds. Only (A) names the real objection."),
             choices=[
                 {"id": "A",
                  "text": "Forcing students to serve can turn a genuine act of giving into one more box to check, which drains its real meaning.",
                  "correct": True,
                  "why": "Correct. It opposes the claim and states the other side's strongest, fairest point: a requirement can drain the meaning out of service."},
                 {"id": "B",
                  "text": "A large share of high school students all across the country already take part in some kind of volunteer work each year.",
                  "correct": False,
                  "why": "This is a neutral fact both sides would accept. It does not oppose the claim, so it is not a counterargument."},
                 {"id": "C",
                  "text": "Schools really should require community service, because helping out in the community is a good thing for every student.",
                  "correct": False,
                  "why": "This restates the writer's own claim. It is your side again, not the point of someone who disagrees."},
                 {"id": "D",
                  "text": "The people who are against the rule simply do not care about anyone else and would rather just stay home doing nothing.",
                  "correct": False,
                  "why": "This is a strawman: a weak, unfair version of the other side that nobody really holds. It attacks the people, not their real point."},
             ]),
        Slot("MODEL", "discrimination", "Which one states the other side FAIRLY?",
             ref="", labeled_grade_c=True, bank="community_service",
             body=("A different trap this time. Each option below is offered as the view of someone who opposes "
                   "the requirement. Which one names their strongest, fairest point, instead of a weak caricature "
                   "or a point they would not actually hold? "
                   "(A) Requiring service can turn a genuine act of giving into just one more box to check, which drains the meaning from it.  "
                   "(B) People who are against the rule are simply lazy and do not really want to help anyone at all except for themselves.  "
                   "(C) The other side believes that community service should be banned from every school in the country, once and for all.  "
                   "(D) Some students already choose to volunteer on their own time, completely outside of anything that school requires now. "
                   "Correct: A is the fair, strong version. (A) names the real objection the other side holds. "
                   "(B) is a strawman that attacks the people, not their point. (C) is an extreme claim the other "
                   "side does not actually make (they oppose a requirement, not service itself). (D) is a neutral "
                   "fact that does not oppose the claim. Only (A) states the other side fairly."),
             choices=[
                 {"id": "A",
                  "text": "Requiring service can turn a genuine act of giving into just one more box to check, which drains the meaning from it.",
                  "correct": True,
                  "why": "Correct. It states the other side's real objection fairly and at full strength: a requirement can drain the meaning out of service."},
                 {"id": "B",
                  "text": "People who are against the rule are simply lazy and do not really want to help anyone at all except for themselves.",
                  "correct": False,
                  "why": "This is a strawman. It attacks the people as lazy instead of stating their real point, so it is not a fair version of the other side."},
                 {"id": "C",
                  "text": "The other side believes that community service should be banned from every school in the country, once and for all.",
                  "correct": False,
                  "why": "This is an extreme point the other side does not hold. They oppose a requirement, not service itself, so it misstates their view."},
                 {"id": "D",
                  "text": "Some students already choose to volunteer on their own time, completely outside of anything that school requires now.",
                  "correct": False,
                  "why": "This is a neutral fact that does not oppose the claim, so it is not the other side's objection at all."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this weak counterargument most need?",
             bank="community_service",
             body=("Diagnose this draft before the reveal. A student was asked to name the other side of the "
                   "community-service claim and wrote: 'The other side just thinks community service is a total "
                   "waste of time and does not matter to anyone.' Which single move would most improve it? "
                   "(A) state the other side's point in its real, strongest form, the fair reason someone who disagrees would truly give  "
                   "(B) add one more objection so the other side ends up with two weak points here instead of only the single one  "
                   "(C) make the whole sentence quite a bit longer and a good deal more formal without changing what it actually says  "
                   "(D) drop the other side's point completely and simply repeat your own claim once again, only stated much more strongly"),
             feedback=("Correct: A. The draft is a strawman, a weak and unfair version of the other side that "
                       "nobody really holds. The fix is to name their real, strongest point, for example: "
                       "'Requiring service can turn a generous act into just another box to check, which drains "
                       "its meaning.' Adding a second weak point (B) or padding the sentence (C) keeps it unfair; "
                       "repeating your own claim (D) drops the other side entirely.")),

        # ===== SUPPORTED: framed NAMING write on the taught topic (source already read at STEP 2) =====
        Slot("SUPPORTED", "production_frq", "Name the other side (with a frame)",
             ref="", bank="community_service", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Here is a claim: schools should require community service to graduate. You are not "
                       "arguing your own side yet. Just name the other side, using the frame below.",
                 setapart_block=setapart("Copy this frame, then fill in the blank:",
                                         "Someone who disagrees would say that ______ [the other side's strongest point, stated fairly]."),
                 closer="Name a point that opposes the claim, stated fairly. Do not restate the claim, and do not "
                        "give a neutral fact both sides accept. Then run the 3 questions on it.")),
        # DIAGNOSIS = a CHECK-and-FIX on a PROVIDED weak draft (a strawman), so it is not a fresh production and
        # does not repeat the framed write. Stays on the taught topic = no new source to read (load balance).
        Slot("MODEL", "diagnosis_frq", "Check and fix a weak counterargument with the 3 questions",
             ref="", bank="community_service", scored=True,
             body=frq_prompt(
                 intro="Run the 3-question test on this weak draft, then rewrite it into a fair counterargument.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "The other side just does not care about helping people.", "red"),
                 checklist_block=checklist(title="Run the test:", rows=[
                     ("Does it actually oppose the claim?",
                      "Not really. It attacks the people, not any reason for or against requiring service."),
                     ("Would the other side really say it?",
                      "No. It is a weak caricature (a strawman), not a point they truly hold."),
                     ("Is it their strongest version?",
                      "No. Their strongest point is that forcing service can drain the meaning out of it. Name that instead."),
                 ]),
                 closer="Now rewrite the weak draft into one fair counterargument that passes all three. Then "
                        "name, in a few words, whose point it is.")),

        # ===== INDEPENDENT: cold naming write on the taught topic (no frame) =====
        Slot("INDEPENDENT", "production_frq", "Name the other side on your own",
             ref="", bank="community_service", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="On your own now, no frame. The claim is: schools should require community service to "
                       "graduate.",
                 closer="Write ONE sentence that names the single strongest counterargument, the best point "
                        "someone who disagrees would make, stated fairly. Naming the other side fairly is the "
                        "first move every real counterargument is built on, and you are ready to do it cold. Do "
                        "not restate the claim or give a neutral fact. Check it against the 3 questions before you "
                        "submit.")),

        # ===== TRANSFER: same move, a NEW topic (pay for grades), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "The debate: paying students for grades",
             ref="ACC-W910-FRAME-PAYGRADES", bank="pay_for_grades",
             body=("A different debate now, so you name the other side of a fresh claim. Read the short framing, "
                   "then picture a writer whose claim is that schools should pay students for good grades. Notice "
                   "the strongest point AGAINST paying. You only need the topic and the two sides.")),
        Slot("TRANSFER", "production_frq", "Name the other side on a NEW topic",
             ref="", bank="pay_for_grades", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="New topic. The claim is: schools should pay students for good grades.",
                 closer="Write ONE sentence that names the strongest counterargument, the best point someone who "
                        "disagrees would make, stated fairly. Same move as the community-service claim, new "
                        "topic. Do not restate the claim or give a neutral fact. Check it against the 3 questions "
                        "before you submit.")),
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
