"""
lesson_g9_l20_counterclaim_recognition_v3_1.py  -  G9 KC C.9.01, ARCHETYPE T2 (STAND, sentence). V3.1.

NEW G9 beat added to close a course<->test coverage gap: our STAAR English I anchor expects
counterargument at grades 8-EII, but the G9 course did not teach it anywhere. This lesson adds a LIGHT
RECOGNITION-ONLY treatment: the student learns to (1) spot the opposing view in a short argument and
(2) name it FAIRLY in one acknowledgment sentence. It deliberately STOPS THERE. Actually refuting the
other side (concede-and-hold, the "Although X, Y because Z" move) stays a G10 skill (KC C.10.01,
Lesson_Bank_G10/lesson_g10_l01_counterclaim_claim.py). Recognition-only is enforced in the copy: every
model, frame, and closer says "name it fairly, you do not have to prove it wrong today; that comes later."

Spine (v3.1, matching the G9 L01/L02 v3.1 archetype): one idea (teal ONE_IDEA callout + a real <ul> teach
list; counterclaim defined with a plain-words cue; the three acknowledgment frames shown) -> source (bound
four-day-week frame) -> coping-model think-aloud with literal BEFORE/AFTER (a writer notices the one-sided
claim never names the other side, then adds ONE fair acknowledgment sentence) + a REMEMBER 2-question check
tool -> TWO discriminations (Grade-C in code only, no leaked label; a fair acknowledgment vs. ignore /
strawman / restate-your-own-side; the acknowledgment frame words appear on BOTH a correct option and a
distractor so no surface-token confound; correct option is never the lone longest) -> predict-the-fix
(reveal in feedback) -> SUPPORTED framed write -> INDEPENDENT cold write (fresh topic) -> TRANSFER cold
write (a third topic). Topics partitioned like G9 L01: taught = four_day_week, independent = pay_for_grades,
transfer = free_transit.

ONE IDEA: a strong argument shows it knows the other side exists; name the opposing view fairly.
ONE REMINDER: the 2-question check (does it name THEIR point? is it stated fairly?). Passes every
lesson_contract gate. Own words, no fabricated figures, no em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A strong argument shows it knows the '
'<strong>other side</strong> exists. Naming an opposing view <strong>fairly</strong> (not knocking it down '
'yet) makes your own claim look considered.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 2 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit an acknowledgment sentence, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does it name the OTHER side\'s point (not your own)?</li>'
'<li style="margin:2px 0">Is it stated FAIRLY (a real point, not a silly version)?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If either answer is no, it is not a fair acknowledgment yet.</div></div>')

# coping-model think-aloud panel: a WRITTEN process (spot the one-sided claim -> find the other side's point
# -> add ONE fair acknowledgment sentence), then the endpoints. RECOGNITION-ONLY: the writer says out loud
# that they are NOT proving the other side wrong today.
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer thinking it through (the task: should schools switch to a four-day week?):</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>The claim so far:</strong> "Schools should switch to a four-day week, '
    'because a longer weekend gives students real time to rest." Check it: does it show I know the other side '
    'exists? No. It gives only my reason. A reader who worries about lost class time is never spoken to.</p>'
    '<p style="margin:0 0 8px"><strong>Find the other side:</strong> what is the strongest thing someone '
    'against this would say? Probably that fewer days could mean less time to learn. I will name that point, '
    'and name it fairly, not as a silly version nobody really holds.</p>'
    '<p style="margin:0"><strong>Add one acknowledgment sentence:</strong> "Some argue that cutting a school '
    'day leaves students with less time to learn, and that is a fair concern." I still hold my own claim. '
    'Notice what I did NOT do: I did not prove that worry wrong. Just naming it fairly is the job today; '
    'answering it is a later skill.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "Schools should switch to a four-day week, because a longer '
    'weekend gives students real time to rest." (never names the other side)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> Same claim, plus one sentence: "Some argue that cutting a '
    'school day leaves students with less time to learn, and that is a fair concern." (names the opposing '
    'view fairly)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C901-0020", grade="9-10", lesson_type=2,
    unit="G9 U1 - Claim/controlling-idea + evidence (recognize the opposing view)",
    title="Show You Know the Other Side Exists",
    target=("Recognize the opposing view in a short argument and name it fairly in one acknowledgment "
            "sentence, without knocking it down. Written at the sentence. Trait: Thesis/Purpose."),
    acc_tags=["ACC.W.ARG.2", "CCSS.W.9-10.1a"],
    provenance={"copyright": "own_authored", "authored": "2026-07-21",
                "mnemonic_status": "proposal", "kc": "C.9.01",
                "taught_stimulus": "ACC-W910-FRAME-FOURDAYWEEK",
                "independent_stimulus": "ACC-W910-FRAME-PAYGRADES",
                "transfer_stimulus": "ACC-W910-FRAME-FREETRANSIT",
                "one_idea": ("A strong argument shows it knows the other side exists. Naming an opposing view "
                             "fairly (not knocking it down yet) makes your own claim look considered."),
                "one_reminder": "2-question check: does it name THEIR point? is it stated fairly?",
                "scope_note": ("counterclaim RECOGNITION only; full acknowledge+refute deferred to "
                               "C.10.01/G10"),
                "coverage_rationale": ("added to close a course<->test coverage gap: the STAAR English I anchor "
                                       "expects counterargument at grades 8-EII, but the G9 course taught no "
                                       "counterclaim beat. This is the LIGHT recognition beat (recognize + "
                                       "fairly acknowledge an opposing view). Full acknowledge-and-refute "
                                       "(concede-then-hold, Although X Y because Z) stays G10 C.10.01."),
                "version_note": ("V3.1 built to the G9 L01/L02 v3.1 archetype: teal ONE_IDEA callout + a real "
                                 "<ul> teach list (counterclaim defined with a plain-words cue, the three "
                                 "acknowledgment frames shown), coping-model think-aloud with literal "
                                 "BEFORE/AFTER, a REMEMBER 2-question check tool, model precedes the "
                                 "discriminations (worked-example-before-quiz), two leak-free discriminations "
                                 "with the acknowledgment-frame words on both a correct option and a distractor "
                                 "(no surface-token confound) and the correct option never the lone longest, "
                                 "autonomy on the independent/transfer writes. Topics partitioned like G9 L01: "
                                 "taught = four-day week, independent = pay-for-grades, transfer = free transit.")},
    fade_ledger_moves=["spot-the-opposing-view", "fair-acknowledgment-sentence"],
    slots=[
        # ===== TEACH: ONE idea only (teal callout + a real list; counterclaim defined; the frames shown) =====
        Slot("TEACH", "teach_card", "The one idea: name the other side, and name it fairly",
             body=(ONE_IDEA +
                   "Every real argument has another side. A reader can tell when a writer has thought about "
                   "that other side and when they have just ignored it. Two moves do the work today:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Spot the opposing view.</strong> An opposing view, also "
                   "called a <strong>counterclaim</strong>, is a point that someone who disagrees with you would "
                   "make. Ask yourself: if a reader took the other side, what is the strongest thing they would "
                   "say?</li>"
                   "<li style=\"margin:4px 0\"><strong>Name it fairly.</strong> Put that point into one sentence, "
                   "stated as the real, reasonable worry it is, not a silly version no one actually holds. Three "
                   "sentence starters make this easy: <em>Some argue that ...</em>, <em>It is true that ...</em>, "
                   "and <em>Critics point out that ...</em></li></ul>"
                   "Here is the important limit for today: you only have to <strong>recognize</strong> the other "
                   "side and name it fairly. You do NOT have to prove it wrong. Answering the other side (showing "
                   "why your side still wins) is a real skill, but it is a later one you will build in a future "
                   "lesson. Today, just showing your argument knows the other side exists is the whole job.")),
        Slot("TEACH", "stimulus_display", "The debate: a four-day school week",
             ref="ACC-W910-FRAME-FOURDAYWEEK", bank="four_day_week",
             body=("Read the short framing of the debate. In a moment you will watch a writer add one fair "
                   "acknowledgment sentence to a one-sided claim, then do it yourself. You only need the topic "
                   "and the two sides, and this time, notice the strongest point on the side you do NOT take.")),

        # ===== MODEL (before the quiz): coping-model think-aloud, with the 2-question check tool folded in =====
        Slot("MODEL", "annotated_before_after", "Watch a writer add a fair acknowledgment",
             bank="four_day_week",
             body=("Here is the skill in action. Follow the writer's thinking below. " + COPING_HTML +
                   " Notice what turned the BEFORE into the AFTER: the writer found the strongest point on the "
                   "other side and named it fairly in one sentence, and then stopped there, without trying to "
                   "prove it wrong. " + REMEMBER +
                   "When you write your own, do the same: find the other side's strongest point, name it fairly, "
                   "and run the 2 questions before you submit.")),
        Slot("MODEL", "discrimination", "Which sentence fairly acknowledges the opposing view?",
             ref="", labeled_grade_c=True, bank="four_day_week",
             body=("Now that you have seen one built, spot the target. A writer is arguing FOR a four-day week. "
                   "Which added sentence fairly names the OTHER side's point, instead of ignoring it, mocking it, "
                   "or just repeating the writer's own side?"),
             choices=[
                 {"id": "A",
                  "text": ("A four-day week would give students a longer weekend to rest, and that extra day off "
                           "helps them come back to class ready to learn."),
                  "correct": False,
                  "why": ("This only adds another reason for the writer's own side. It never names the other "
                          "side's point, so it does not acknowledge the opposing view at all.")},
                 {"id": "B",
                  "text": ("Some people want to keep five days only because they are stuck in the past and are "
                           "just afraid of trying anything new."),
                  "correct": False,
                  "why": ("This names the other side, but as a silly, unfair version no one really holds (a "
                          "strawman). Acknowledging fairly means stating their real, reasonable point.")},
                 {"id": "C",
                  "text": ("Some argue that cutting a school day could leave students with less time to learn, "
                           "and that is a fair concern."),
                  "correct": True,
                  "why": ("Correct. It names the strongest point on the other side and treats it as reasonable. "
                          "That is exactly what fairly acknowledging the opposing view means.")},
                 {"id": "D",
                  "text": ("It is true that switching to a four-day week is the right choice for schools to make "
                           "for their students."),
                  "correct": False,
                  "why": ("This borrows an acknowledgment starter ('It is true that'), but the point it names is "
                          "the writer's OWN side. Acknowledging means naming the OTHER side's point.")},
             ]),
        Slot("MODEL", "discrimination", "Which sentence names the opposing view fairly?",
             ref="", labeled_grade_c=True, bank="four_day_week",
             body=("One more set. Each sentence below starts the same way and points at the other side. But only "
                   "one names a real opposing point and states it fairly. Which one is the fair acknowledgment?"),
             choices=[
                 {"id": "A",
                  "text": ("Critics point out that people who oppose a four-day week simply do not care whether "
                           "students ever get enough rest."),
                  "correct": False,
                  "why": ("This claims the other side does not care about students, an unfair version of their "
                          "real point. A strawman like this is not a fair acknowledgment.")},
                 {"id": "B",
                  "text": ("Critics point out that a shorter week can be hard on families who need child care on "
                           "the extra day off."),
                  "correct": True,
                  "why": ("Correct. It names a genuine, reasonable worry the other side raises and states it "
                          "fairly, without mocking it.")},
                 {"id": "C",
                  "text": ("Critics point out that a four-day week finally gives students the longer weekend they "
                           "have wanted for so long."),
                  "correct": False,
                  "why": ("This uses an acknowledgment starter but names a point for the writer's OWN side, so "
                          "it does not acknowledge the opposing view.")},
                 {"id": "D",
                  "text": ("Critics point out that there are always going to be two sides to just about every "
                           "single question that people argue over."),
                  "correct": False,
                  "why": ("This gestures at 'two sides' but never names the actual opposing point, so it "
                          "acknowledges nothing in particular.")},
             ]),
        Slot("MODEL", "predict_the_fix", "This claim ignores the other side. What fixes it?",
             bank="four_day_week",
             body=("Diagnose this draft before the reveal. The task asked the student to argue whether schools "
                   "should switch to a four-day week. The student wrote: 'Schools should switch to a four-day "
                   "week, because a longer weekend lets students rest.' It is a clear side, but it never shows "
                   "the writer knows the other side exists. Which single move would most improve it? "
                   "(A) name the strongest point on the other side and state it fairly in one added sentence  "
                   "(B) add one more reason for the writer's own side, such as saving the school money  "
                   "(C) rewrite the whole claim in longer and more formal language so it sounds more impressive  "
                   "(D) add more detail describing how the four-day and the five-day schedules each work"),
             feedback=("Correct: A. The draft takes a side but never names the other side, so a reader cannot "
                       "tell the writer has weighed it. The fix is the move you just saw: name the strongest "
                       "opposing point fairly in one sentence ('Some argue that fewer days could mean less time "
                       "to learn, and that is a fair concern'). Remember the limit: you name it fairly, you do "
                       "not have to prove it wrong today. A second same-side reason (B), fancier wording (C), or "
                       "more schedule detail (D) never show that the argument knows the other side exists.")),

        # ===== SUPPORTED: framed write (fill-in frame) on the taught topic =====
        Slot("SUPPORTED", "production_frq", "Finish the sentence: name the other side fairly",
             ref="", bank="four_day_week", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Imagine you are arguing FOR the four-day week. Use the frame so you can focus on the move.",
                 setapart_block=setapart(
                     "Copy this frame, then fill in the blank:",
                     "Some argue that ______ [the strongest point on the OTHER side, stated fairly]."),
                 closer="Name the other side's real point, and state it as a fair, reasonable worry (not a silly "
                        "version). You do not have to prove it wrong today; just show you know it exists. Then "
                        "check it: does it name THEIR point, and is it fair?")),

        # ===== INDEPENDENT: cold write on a DIFFERENT topic (pay-for-grades) =====
        Slot("INDEPENDENT", "stimulus_display", "The debate: paying students for grades",
             ref="ACC-W910-FRAME-PAYGRADES", bank="pay_for_grades",
             body=("A different debate now, so you name a fresh point instead of reusing the last one. Read the "
                   "short framing, then pick your side and notice the strongest point on the other side. You only "
                   "need the topic and the two sides.")),
        Slot("INDEPENDENT", "production_frq", "Acknowledge the other side on paying for grades",
             ref="", bank="pay_for_grades", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="On your own now, no frame. The task: should schools pay students for good grades?",
                 closer="Pick the side you actually hold. Then write ONE sentence that fairly names the strongest "
                        "point on the OTHER side, using a starter like 'Some argue that ...', 'It is true that "
                        "...', or 'Critics point out that ...'. You are not knocking it down, just showing your "
                        "argument knows it exists. Check it against the 2 questions before you submit.")),

        # ===== TRANSFER: same move, a THIRD topic (free transit), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "The debate: free public transit",
             ref="ACC-W910-FRAME-FREETRANSIT", bank="free_transit",
             body=("One more new debate. Read the short framing, then pick a side. Same move as before, a fresh "
                   "topic: find the strongest point on the side you did NOT take. You only need the topic and the "
                   "two sides.")),
        Slot("TRANSFER", "production_frq", "Acknowledge the other side on a NEW topic",
             ref="", bank="free_transit", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="New topic. The task: should cities make public transit free to ride?",
                 closer="Write ONE sentence that fairly acknowledges the strongest point on the side you did NOT "
                        "take. Same move as the four-day-week and pay-for-grades sentences, new topic. Name it "
                        "fairly; you do not have to prove it wrong. Check it against the 2 questions before you "
                        "submit.")),
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
