"""
lesson_g9_l21_counterargument_paragraph_v3_1.py  -  G9 KC C.9.07, ARCHETYPE T3 (PROVE, paragraph tier). V3.1.

G9 U4 CLOSER (the new Counterargument unit, third and final rung). This is the PARAGRAPH step that
ASSEMBLES the two earlier rungs: L19 (RECOGNIZE the other side) and L20 (CONCEDE + ANSWER at the
sentence). Here the student folds the concede-then-answer move into ONE short structured paragraph:
state your position, fairly name the opposing point, then ANSWER it with a REASON (not just a repeat of
the claim), while keeping your position. INTRODUCTORY G9 depth: a short paragraph answered with a REASON.
It deliberately sits BELOW the G10 spiral: G10 L03 ("Answer the Counterclaim in a Full Paragraph") answers
with EVIDENCE + reasoning and WEIGHS the objection; this lesson answers with a reason only. Taught:
FRAME-SCHOOLLUNCH (bank school_lunch) -> transfer: FRAME-SOCIALMEDIAAGE (bank social_media_age),
partitioned. Topics differ from the G10 counterargument set (daylight_saving/school_year/congestion) and
from the two sibling G9 rungs (community_service/pay_for_grades), so no collision. rc.staar,
unit="paragraph". PROVE=established-caveat. No named persona, no source markup, no prior-work ref, no em dashes.

V3.1 spine: ONE_IDEA teal callout + minimal LIST teach (define counterargument in plain words + a dfn) ->
bound issue frame -> coping-model think-aloud (draft that only NAMES the objection -> run the check ->
catch that it never answered -> revise to answer with a reason) with literal BEFORE/AFTER -> named
POSITION/OTHER SIDE/ANSWER moves + REMEMBER 3-question check tool -> discrimination (choices=, 4 options,
homogeneous length, reveal in tail + per-choice why) -> predict-the-fix (reveal in feedback) -> SUPPORTED
framed paragraph -> DIAGNOSIS check-and-fix on a provided weak draft -> INDEPENDENT cold paragraph ->
TRANSFER on the partitioned social-media-age frame.

ONE IDEA: a counterargument paragraph does not just NAME the other side, it ANSWERS it with a reason while
you keep your position. ONE REMINDER: the 3-question check (position clear? opposing point named fairly?
answered with a reason, not a repeat?).
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
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A counterargument paragraph does not just '
'<strong>name</strong> the other side, it <strong>answers</strong> it with a reason while you keep your '
'position, like this: <strong>"Some say free meals waste school money, but sorting students by who can pay '
'is exactly what makes some go hungry."</strong> Name the objection and stop, and it still stands.</div></div>')

# the reusable 3-question CHECK TOOL, attached at the model (point of first use), as a real <ol>.
REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit any counterargument paragraph, run this quick check:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Did I state my position clearly?</li>'
'<li style="margin:2px 0">Did I name the opposing point fairly (the real point, not a weak or unfair version)?</li>'
'<li style="margin:2px 0">Did I answer it with a reason, not just repeat my claim?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If the objection is only named and never answered, the paragraph is not finished yet.</div></div>')

# coping-model think-aloud: a WRITTEN drafting process (draft a paragraph that only NAMES the objection ->
# run the check -> catch that it never answered -> revise to answer with a reason), then the literal BEFORE
# and AFTER endpoints (content_depth needs BOTH inline). Taught topic = free school meals. No named peer.
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer building the counterargument paragraph, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Schools should give free meals to every student. '
    'Some fairly say the limited school money should go to the students who need it most, not to families who '
    'can pay. Free meals would still help students focus and learn." Run the check: position clear? Yes. '
    'Opposing point named fairly? Yes, the money worry. Answered? No, it names the worry and then just repeats '
    'that free meals help, so the worry is still standing. Not finished.</p>'
    '<p style="margin:0"><strong>Second try, answers it:</strong> "It is fair to say the limited money should '
    'reach the neediest students first. But when only some students get free lunch, the ones who qualify feel '
    'singled out and skip it, so a program that feeds everyone is the one that actually reaches those students '
    'too." Now the objection is answered with a reason. That passes.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> names the money objection, then repeats the claim, so the objection is never answered.</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> '
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;font-weight:700">POSITION</span> '
      'Schools should give free meals to every student. '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;font-weight:700">OTHER SIDE</span> '
      'It is fair to say the limited money should reach the neediest students first. '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;font-weight:700">ANSWER</span> '
      'But sorting students by who can pay is what makes some skip the meal, so feeding everyone reaches the '
      'hungry students too. (position, the other side named, and a real answer)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C904-0032", grade="9-10", lesson_type=3,
    unit="G9 U4 - Counterargument (answer it in a short paragraph)",
    title="Answer the Other Side in a Short Paragraph",
    target=("Build a short counterargument paragraph: state your position, fairly name the opposing point, "
            "then answer it with a reason while keeping your claim. Written at the paragraph. Trait: "
            "Development."),
    acc_tags=["ACC.W.ARG.2", "CCSS.W.9-10.1a"],
    provenance={"copyright": "own_authored", "authored": "2026-07-21",
                "mnemonic_status": "established-caveat", "kc": "C.9.07",
                "sot": "KC_Map_and_Unit_Arch_G9-12.md (G9 U4 - Counterargument)",
                "taught_stimulus": "ACC-W910-FRAME-SCHOOLLUNCH",
                "transfer_stimulus": "ACC-W910-FRAME-SOCIALMEDIAAGE",
                "template": "locked v3.1 spine (lesson_g10_l03_counterclaim_paragraph); reason-tier G9 adaptation.",
                "one_idea": "A counterargument paragraph does not just name the other side, it answers it with a reason while you keep your position.",
                "one_reminder": "3-question check: position clear? opposing point named fairly? answered with a reason, not a repeat?",
                "mnemonic_status_note": ("Requested spec said mnemonic_status='proposal'; gate_mnemonic_status hard-couples "
                                         "lesson_type=3 (PROVE/evidence-integration) to 'established-caveat' (as all 8 live G9 "
                                         "type-3 lessons L05-L13 declare). Used 'established-caveat' to pass qc_lesson, per the "
                                         "gate-critical constraint. The paragraph-tier build fits type 3 (paragraph ceiling)."),
                "version_note": ("V3.1 build to the locked spine: ONE_IDEA teal callout + minimal list teach "
                                 "(counterargument defined in plain words with a dfn), coping-model think-aloud "
                                 "(draft that only NAMES the objection -> run the check -> catch it -> revise to "
                                 "answer with a reason) with literal BEFORE/AFTER, named POSITION/OTHER SIDE/ANSWER "
                                 "moves + REMEMBER 3-question check tool, one leak-free discrimination via explicit "
                                 "choices= (4 options, homogeneous length, per-choice why, reveal in tail), "
                                 "predict-the-fix reveal in feedback, framed SUPPORTED paragraph, check-and-fix "
                                 "DIAGNOSIS on a provided weak draft, cold INDEPENDENT paragraph, and a partitioned "
                                 "social-media-age TRANSFER paragraph."),
                "council": ("G9 PARAGRAPH rung of the counterargument ladder (unit closer), assembling L19 RECOGNIZE "
                            "+ L20 CONCEDE-AND-ANSWER into one short paragraph. It answers the objection with a REASON "
                            "only; EVIDENCE-based rebuttal and WEIGHING are deliberately reserved for the deeper G10 "
                            "spiral (lesson_g10_l03_counterclaim_paragraph answers with evidence + reasoning and "
                            "weighs). Keeping G9 at a reason-answered SHORT paragraph holds the cognitive load "
                            "appropriate for the introductory rung. PROVE=established-caveat; paragraph ceiling.")},
    fade_ledger_moves=["counterargument-paragraph", "answer-with-a-reason-not-just-name"],
    slots=[
        # ===== TEACH: ONE idea + the three parts as a LIST; define counterargument in plain words (dfn) =====
        Slot("TEACH", "teach_card", "Naming the other side is not answering it",
             body=(ONE_IDEA +
                   "You already know how to name the other side and how to answer it in a sentence. Today you "
                   "fold both into one short paragraph. A "
                   "<dfn class=\"tb-glossary-term\" data-catalog-idref=\"def-counterargument\" "
                   "title=\"A counterargument is the point that someone who disagrees with your position would "
                   "make.\">counterargument</dfn> is the point that someone who disagrees with your position "
                   "would make. A short counterargument paragraph has three parts:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>POSITION</strong>: the side you are arguing, stated "
                   "clearly.</li>"
                   "<li style=\"margin:4px 0\"><strong>THE OTHER SIDE</strong>: fairly name the opposing point, "
                   "the real objection someone who disagrees would raise, not a weak version of it.</li>"
                   "<li style=\"margin:4px 0\"><strong>ANSWER</strong>: respond to that objection with a reason "
                   "that shows why your position still holds.</li></ul>"
                   "The common failure is naming the objection and then ignoring it: <em>Some say it wastes "
                   "money. But free meals help students learn.</em> That mentions the other side and then just "
                   "repeats your own point, so the money worry is still standing. Answering means giving a reason "
                   "that meets the objection head on. You are not learning a new move today, you are building the "
                   "moves you know into one short paragraph.")),
        Slot("TEACH", "stimulus_display", "The debate: free meals for all students",
             ref="ACC-W910-FRAME-SCHOOLLUNCH", bank="school_lunch",
             body=("Read the short framing of the debate. Picture a writer whose position is that schools should "
                   "give free meals to every student. In a moment you will watch that writer answer the other "
                   "side in a paragraph, then you will do it. Read and note the strongest objection to the "
                   "position and one reason you could use to answer it. You only need the topic and the two sides.")),

        # ===== MODEL (before the quiz): coping-model think-aloud + the reusable 3-question check tool =====
        Slot("MODEL", "annotated_before_after", "Watch a writer answer the other side",
             bank="school_lunch",
             body=("Here is the build in action. A writer drafts a paragraph that only names the objection, runs "
                   "the check, catches that it never answered, and revises. Follow the thinking below. " + COPING_HTML +
                   " The BEFORE names the money worry and drops it. The AFTER names that worry and answers it with "
                   "a reason, so the objection no longer stands. " + REMEMBER +
                   "When you build your own, use this same check before you submit.")),
        Slot("MODEL", "discrimination", "Which paragraph answers the other side?",
             ref="", labeled_grade_c=True, bank="school_lunch",
             body=("Now that you have seen one built, spot the target. All four state the same position and name "
                   "the same objection (that limited money should go to the neediest students). Which one "
                   "actually ANSWERS that objection with a reason? "
                   "(A) Schools should give free meals to every student. It is fair to say limited school money "
                   "should reach the students who need it most, not families who can pay. School lunches have "
                   "also gotten a great deal healthier in recent years, with more fresh fruit and more vegetables "
                   "served on every single tray.  "
                   "(B) Schools should give free meals to every student. It is fair to say limited school money "
                   "should reach the students who need it most, not families who can pay. But when only some "
                   "students qualify, they feel singled out and skip the meal, so feeding everyone is what reaches "
                   "the hungry students.  "
                   "(C) Schools should give free meals to every student. It is fair to say limited school money "
                   "should reach the students who need it most, not families who can pay. Still, free meals for "
                   "all students is simply the right thing to do, so schools really ought to just go ahead and "
                   "provide them for everyone.  "
                   "(D) Schools should give free meals to every student. It is fair to say limited school money "
                   "should reach the students who need it most, not families who can pay. Honestly both sides here "
                   "make some genuinely strong points, so in the end it is really hard to say what any school "
                   "should decide to do. "
                   "Correct: B answers the objection with a reason. A changes the subject, C just repeats the "
                   "claim as the answer, and D concedes and then gives up its position."),
             choices=[
                 {"id": "A",
                  "text": "Schools should give free meals to every student. It is fair to say limited school money should reach the students who need it most, not families who can pay. School lunches have also gotten a great deal healthier in recent years, with more fresh fruit and more vegetables served on every single tray.",
                  "correct": False,
                  "why": "It names the money objection and then changes the subject to how healthy lunches are. That is a new topic, not an answer to the worry it just raised."},
                 {"id": "B",
                  "text": "Schools should give free meals to every student. It is fair to say limited school money should reach the students who need it most, not families who can pay. But when only some students qualify, they feel singled out and skip the meal, so feeding everyone is what reaches the hungry students.",
                  "correct": True,
                  "why": "Correct. It states the position, names the money objection fairly, and then answers it with a reason: sorting students by who can pay is what makes the neediest skip the meal, so feeding everyone reaches them. Answering, not just naming, is the move."},
                 {"id": "C",
                  "text": "Schools should give free meals to every student. It is fair to say limited school money should reach the students who need it most, not families who can pay. Still, free meals for all students is simply the right thing to do, so schools really ought to just go ahead and provide them for everyone.",
                  "correct": False,
                  "why": "It names the objection and then just repeats the claim ('free meals for all is the right thing to do'). Restating your position is not the same as giving a reason that answers the money worry."},
                 {"id": "D",
                  "text": "Schools should give free meals to every student. It is fair to say limited school money should reach the students who need it most, not families who can pay. Honestly both sides here make some genuinely strong points, so in the end it is really hard to say what any school should decide to do.",
                  "correct": False,
                  "why": "It names the objection and then collapses into 'hard to say,' giving up the position instead of answering. A shrug is not an answer."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this counterargument paragraph most need?",
             bank="school_lunch",
             body=("Diagnose before the reveal. A paragraph reads: 'Schools should give free meals to every "
                   "student. People worry it costs too much money. Anyway, free meals are a good idea and would "
                   "help kids learn.' Which single move would most improve it as a counterargument paragraph? "
                   "(A) answer the money worry with a reason, such as that feeding everyone is what reaches the students who skip meals  "
                   "(B) add a whole second objection from the other side, such as food being wasted, on top of the money worry already there  "
                   "(C) state the position much more forcefully, with stronger and more confident wording that just repeats the claim again  "
                   "(D) move the objection down to the very end so it comes after the claim, changing only the order of these sentences here"),
             feedback=("Correct: A. The paragraph names the money worry and then just repeats that free meals are "
                       "good, so the objection is never answered. The fix answers it with a reason: when only some "
                       "students qualify they feel singled out and skip the meal, so feeding everyone is what "
                       "reaches the hungry students. A second objection (B), more forceful wording (C), or "
                       "reordering (D) do not answer the money worry.")),

        # ===== SUPPORTED: framed write, build the two answering parts onto a given position =====
        Slot("SUPPORTED", "production_frq", "Name the other side, then answer it", ref="", bank="school_lunch",
             rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="Warm up the build. Start from the given position, then add the two parts that answer the other side.",
                 setapart_block=setapart("Copy this frame, then fill in the two blanks:",
                                         "Schools should give free meals to every student. It is fair to say "
                                         "______ [the opposing point, named fairly]. But ______ [your answer: a "
                                         "reason that meets the objection, not a repeat of the claim]."),
                 closer="Write those two parts so the answer truly meets the objection, not just restates your "
                        "position. You are building the name-then-answer onto the given position, in a short paragraph.")),
        # COUNCIL FIX (2026-07-24): Option A (later-in-arc), watch-then-do: demo preserved, produce is the graded
        # act. The old diagnosis_frq bundled a watched 3-question check-run demo + a fresh paragraph + a run-the-
        # same-three-questions-and-name-how-your-answer-meets-the-objection tail in one box (unscoreable, wired to
        # no grader). The coping-model demo is PRESERVED as read-only narration (the 3-question check shown running
        # on the weak draft, in plain declarative form so it is not a hidden self-answer prompt). The student's ONLY
        # graded act is now the fresh build; the three questions sit read-only beneath as plain-string reminders;
        # the run-and-name tail is deleted. Stays on the taught topic (no new source to read).
        Slot("MODEL", "diagnosis_frq", "Check a counterargument: named, or answered?", ref="", bank="school_lunch",
             rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="First, watch the 3-question check run on the weak draft below. The POSITION is clear "
                       "('free meals for all are good' states the side) and the OPPOSING POINT is named fairly "
                       "(the money should go to the neediest students), but the draft never ANSWERS that worry: "
                       "'still a good idea' just repeats the claim, so the objection is left standing. Now write a "
                       "fresh paragraph of your own that answers the other side instead of just naming it.",
                 setapart_block=setapart("Weak draft the check was run on:",
                                         "Free meals for all are good. Some say the money should go to the "
                                         "neediest students. But free meals are still a good idea.", "red"),
                 checklist_block=checklist(title="Check your paragraph against these (no need to type answers):", rows=[
                     "Is your position stated clearly?",
                     "Is the opposing point named fairly (the real point, not a weak version)?",
                     "Do you answer it with a reason, not just repeat your claim?",
                 ]),
                 closer="Write ONE fresh short counterargument paragraph on whether schools should give free meals "
                        "to every student, with all three parts: state your position, name the opposing point "
                        "fairly, then answer it with a reason while keeping your position. Run the check above "
                        "before you submit.")),

        # ===== INDEPENDENT: cold short-paragraph build on the taught topic + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Write a short counterargument paragraph", ref="", bank="school_lunch",
             rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now, build the whole short paragraph.",
                 closer="Write ONE short counterargument paragraph on whether schools should give free meals to "
                        "every student, with all three parts: state your POSITION, fairly name the OPPOSING POINT, "
                        "then ANSWER it with a reason while keeping your position. Before you submit, run the "
                        "3-question check and fix any part that fails. Answering the other side is what every real "
                        "argument rests on, and you are ready to do it cold.")),

        # ===== TRANSFER: same move, a NEW topic (verify social media age), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "The debate: checking ages on social media",
             ref="ACC-W910-FRAME-SOCIALMEDIAAGE", bank="social_media_age",
             body=("A different debate now, so you build a fresh paragraph instead of reusing the last one. Read "
                   "the short framing, then take a side on whether social media apps should have to check how old "
                   "their users are. Read and note the strongest objection to your side and a reason you could use "
                   "to answer it. You only need the topic and the two sides.")),
        Slot("TRANSFER", "production_frq", "Write a short counterargument paragraph on a NEW topic", ref="",
             bank="social_media_age", rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="New topic, same build. The task: argue a position on whether social media apps should have to check users' ages.",
                 closer="Write ONE short counterargument paragraph with all three parts: state your POSITION, "
                        "fairly name the OPPOSING POINT (for example the risk to everyone's private information), "
                        "then ANSWER it with a reason while keeping your position. Same name-then-answer build as "
                        "the free-meals paragraph, fresh topic. Do not stop at naming the objection. Run the "
                        "3-question check before you submit.")),
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
