"""
lesson_g9_l03_sharpen_stakes_v3_1.py  -  G9 KC C.9.01, ARCHETYPE T2 (STAND, sentence). V3.1.

G9 L03, rebuilt to the v3.1 build spec (icm/_config/v3_1-lesson-build-spec.md). Teaching point PRESERVED
(distinct from L01/L02): take a VAGUE claim, SHARPEN it into a specific position, then reach the SO-WHAT /
STAKES (say why it matters). Lesson id preserved (ACC-W910-L-G9-C901-0003).

Spine (v3.1): one idea + list-formatted teach (recap arguable-claim; teach the two new moves) -> source ->
coping-model think-aloud (draft -> test -> catch the vague/no-stakes -> revise) -> decompose into named moves
+ check tool at point of first use -> discrimination AFTER the model (no leaked labels; distractors
homogeneous in length; the 'because'/'matters' tokens do NOT co-vary with the correct answer) -> predict the
fix (reveal in feedback) -> framed write -> scaffolded diagnosis -> independent (autonomy + say the standard)
-> transfer (partitioned bank).

TOPIC CHANGE per the approved slate: taught topic = pay-for-grades (ACC-W910-FRAME-PAYGRADES, bank
'pay_for_grades'); transfer topic = free-public-transit (ACC-W910-FRAME-FREETRANSIT, bank 'free_transit').
Community-service/phone-ban topics DROPPED. All authored HTML inline-styled with real lists. 23 gates.
Own words, no fabricated figures, no em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A strong claim is <strong>SPECIFIC</strong> and '
'reaches the <strong>SO-WHAT</strong> (it says why it matters). A vague claim that stops at the position stays '
'in the middle of the scoring.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit any claim, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Is the side specific (names an amount or kind)?</li>'
'<li style="margin:2px 0">Is there a reason?</li>'
'<li style="margin:2px 0">Does it say why it matters (the so-what)?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, it is not there yet.</div></div>')

# coping-model think-aloud panel: a WRITTEN drafting process (attempt -> test -> revise), then the endpoints.
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer thinking it through, draft by draft (the task: should schools pay students for good grades?):</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Paying students for grades is a good thing." '
    'Check it: is it specific? No, it names no amount and no kind, so a reader cannot tell what I am really '
    'arguing. Does it say why it matters? No. Start over.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "Schools should pay students for good grades." '
    'Better, it takes a clearer side. But is it specific? Not yet, it still names no amount. And it stops '
    'there, it never says why it matters. Add the stakes.</p>'
    '<p style="margin:0"><strong>Final:</strong> "Schools should pay fifty dollars for every A, because a '
    'reward pulls back in students who quit trying, which matters because those students most often drop out." '
    'A specific side, a reason, and a so-what.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "Paying students for grades is a good thing." (vague, and no stakes)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "Schools should pay fifty dollars for every A, because a '
    'reward pulls back in students who quit trying, which matters because those students most often drop out." '
    '(specific, and it reaches the stakes)</span></div>'
'</div>')

DECOMPOSE_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#f0fdf4;padding:10px 14px;border-bottom:1px solid #bbf7d0;font-size:15px">'
    'The finished claim: <em>"Schools should pay fifty dollars for every A, because a reward pulls back in '
    'students who quit trying, which matters because those students most often drop out."</em></div>'
  '<div style="padding:12px 14px">'
    '<div style="margin:0 0 10px">'
      '<span style="display:inline-block;background:#dbeafe;color:#1e3a8a;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">MOVE 1 - SPECIFIC SIDE</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px"><strong>"pay fifty dollars for every A"</strong> '
      'names an exact amount, not just "good grades" in general.</div></div>'
    '<div style="margin:0 0 10px">'
      '<span style="display:inline-block;background:#fef9c3;color:#854d0e;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">MOVE 2 - REASON</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px">"...<strong>a reward pulls back in students '
      'who quit trying</strong>" gives the side support.</div></div>'
    '<div>'
      '<span style="display:inline-block;background:#ede9fe;color:#5b21b6;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">MOVE 3 - SO WHAT</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px">"...<strong>which matters because those '
      'students most often drop out</strong>" says why the side is worth caring about.</div></div>'
    '<div style="margin-top:10px;color:#0f766e;font-size:13px">A specific side, a reason, and a so-what. That '
    'is the strong-claim build.</div>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C901-0003", grade="9-10", lesson_type=2,
    unit="G9 U1 - Claim/controlling-idea + evidence (sharpen + stakes)",
    title="Make the Claim Sharp and Say Why It Matters",
    target=("Take a vague claim, sharpen it into a specific position, and reach the so-what: say why it "
            "matters. Written at the sentence. Trait: Thesis/Purpose."),
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.5", "CCSS.W.9-10.1a"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.9.01",
                "sot": "icm course-G9.md L03; KC_Map_and_Unit_Arch_G9-12.md (G9 U1)",
                "taught_stimulus": "ACC-W910-FRAME-PAYGRADES",
                "transfer_stimulus": "ACC-W910-FRAME-FREETRANSIT",
                "one_idea": "A strong claim is SPECIFIC and reaches the SO-WHAT (why it matters).",
                "one_reminder": "3-question test: specific? reason? why it matters?",
                "version_note": ("V3.1 rebuild per icm/_config/v3_1-lesson-build-spec.md, preserving the L03 "
                                 "teaching point (sharpen a vague claim into a specific position + reach the "
                                 "so-what/stakes) and the lesson id. Applied the L01/L02 v3.1 pattern: "
                                 "list-formatted teach + arguable-claim recap + thesis tooltip, coping-model "
                                 "think-aloud (SRSD ES-flexible), model + decompose + check-tool-at-point-of-use "
                                 "PRECEDE the discrimination (KH worked-example-before-quiz), leak-free "
                                 "discrimination with the 'because'/'matters' token confound broken (DI faultless "
                                 "communication), autonomy + say-the-standard on the independent write (Yeager). "
                                 "TOPIC CHANGE to the approved slate: taught = pay-for-grades, transfer = "
                                 "free-public-transit (community-service/phone-ban dropped)."),
                "review_provenance": "built to the L01/L02 v3.1 pattern (Fable+Council adjudicated 2026-07-14)"},
    # PP100 mastery prompt is authored per-lesson in pipeline/mastery_prompts_g9.py (single source of truth).
    fade_ledger_moves=["sharpen-vague-to-specific", "so-what-stakes", "specific-side-plus-reason"],
    slots=[
        # ===== TEACH: recap the arguable claim, then teach the two NEW moves (specific + so-what) =====
        Slot("TEACH", "teach_card", "The one idea: make it specific, then say why it matters",
             body=(ONE_IDEA +
                   "You already know an arguable claim is a sentence that takes a side someone could disagree "
                   "with and backs it with a reason. Now make that claim STRONG. Two moves do it:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Be specific.</strong> A vague claim names no amount, no "
                   "who, no what, so a reader cannot tell exactly what you are arguing ('paying students is good' "
                   "is vague). A specific claim names the exact position ('schools should pay fifty dollars for "
                   "every A').</li>"
                   "<li style=\"margin:4px 0\"><strong>Reach the so-what.</strong> After your claim, say why it "
                   "matters. Ask yourself: if a reader agreed with me, why would that be worth caring "
                   "about?</li></ul>"
                   "A claim that names why it matters reaches the top of the scoring; a claim that stops at the "
                   "position stays in the middle. (Scoring sometimes calls your governing claim a "
                   "<dfn class=\"tb-glossary-term\" data-catalog-idref=\"def-thesis\" "
                   "title=\"Thesis means the arguable claim your whole response defends. You do not need this "
                   "word to finish today's task.\">thesis</dfn>, but you do not need that word for today's task.) "
                   "Today you will sharpen a vague claim and add its stakes.")),
        Slot("TEACH", "stimulus_display", "The debate: paying students for grades",
             ref="ACC-W910-FRAME-PAYGRADES", bank="pay_for_grades",
             body=("Read the short framing of the debate. In a moment you will watch a vague claim get sharpened "
                   "and reach its stakes, then build your own. You only need the topic and the two sides. This "
                   "time, make your side specific and say why it matters.")),

        # ===== MODEL first (before the quiz): coping-model think-aloud -> decompose + the check tool =====
        Slot("MODEL", "annotated_before_after", "Watch a vague claim get sharp and reach its stakes",
             bank="pay_for_grades",
             body=("Here is the skill in action. Follow the writer's thinking below. " + COPING_HTML +
                   " Notice what turned the BEFORE into the AFTER: the writer made the side specific (a real "
                   "amount), added a reason, and then said why it matters.")),
        Slot("MODEL", "teach_card", "Decompose it, and get your check tool",
             body=("Now take the finished claim apart to see how it is built, then keep the tool you will use to "
                   "check your own." + DECOMPOSE_HTML + REMEMBER +
                   "When you write your own, build it the same way: pick a specific side, add a reason, then say "
                   "why it matters, and run the 3 questions before you submit.")),
        Slot("MODEL", "discrimination", "Which claim is specific AND says why it matters?",
             ref="", labeled_grade_c=True, bank="pay_for_grades",
             body=("Now that you have seen one built, spot the target. Which sentence is a specific claim that "
                   "also says why it matters, not a vague one? "
                   "(A) Paying students for their grades is honestly a really good and worthwhile idea, because it clearly matters a great deal to a whole lot of students and their families all across the country today.  "
                   "(B) Schools ought to go ahead and start paying at least some of their students a bit of money at some point whenever those students manage to earn themselves some good grades in their classes.  "
                   "(C) Schools should pay fifty dollars for every A, because a reward pulls back in students who quit trying, which matters because those students most often drop out. "
                   "Correct: C. Watch the trap: (A) sounds positive and even uses 'because' and 'matters,' but it "
                   "is vague and circular, it names no specific side and gives no real reason. (B) takes a side "
                   "but stays vague (how much? for which grades?) and never says why it matters. Only (C) names a "
                   "specific amount, gives a reason, and reaches the so-what. It is the specific side plus the "
                   "reason plus the why-it-matters that makes the claim strong, not any single word.")),
        Slot("MODEL", "discrimination", "Which claim has BOTH a specific side and its stakes?",
             ref="", labeled_grade_c=True, bank="pay_for_grades",
             body=("Each option below argues for paying for grades. A strong claim needs a specific side and a "
                   "why-it-matters. Which one has both, instead of missing one of them?"),
             choices=[
                 {"id": "A",
                  "text": ("Schools should reward good report cards, because a payoff gives real motivation, "
                           "which matters because students who stay motivated are far less likely to give up "
                           "on school."),
                  "correct": False,
                  "why": ("It reaches a real why-it-matters, but it never names a specific amount or kind, so "
                          "the side stays vague.")},
                 {"id": "B",
                  "text": ("Schools should pay twenty dollars for each report-card A, because a clear, "
                           "guaranteed cash reward gives students a concrete, day-to-day reason to keep "
                           "studying hard for every single test they take."),
                  "correct": False,
                  "why": ("It names an exact amount and gives a reason, but it stops at the position and never "
                          "says why it matters.")},
                 {"id": "C",
                  "text": ("Schools should pay twenty dollars for each report-card A, because the reward keeps "
                           "struggling students in class, which matters because they are the ones who "
                           "graduate."),
                  "correct": True,
                  "why": ("It names an exact amount, gives a reason, and then says why it matters, so it is "
                          "specific and reaches the stakes.")},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this vague claim most need, and what fixes it?",
             bank="pay_for_grades",
             body=("Diagnose this draft before the reveal. The task asked the student to argue whether schools "
                   "should pay students for good grades. The student wrote: 'Paying students for good grades is "
                   "something a lot of schools have talked about.' Which single move would most improve it? "
                   "(A) sharpen it to a specific side and add a reason plus a so-what  "
                   "(B) add one more detail about which schools have discussed paying students  "
                   "(C) make the whole sentence quite a bit longer and much more formal  "
                   "(D) describe in detail how a report card and letter grades usually work"),
             feedback=("Correct: A. The draft only reports that the idea has been discussed, it names no side, no "
                       "reason, and no stakes, so it stays vague. The fix is the move you just saw: sharpen to a "
                       "specific side ('pay fifty dollars for every A'), add a reason, then say why it matters. "
                       "One more detail about which schools (B), a longer or more formal sentence (C), or a "
                       "description of report cards (D) never turn a vague sentence into a specific claim that "
                       "reaches its stakes.")),

        # ===== SUPPORTED: framed write (fill-in frame) =====
        Slot("SUPPORTED", "production_frq", "Finish the claim: make it specific, add a reason and the stakes",
             ref="", bank="pay_for_grades", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on the moves.",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "Schools should ______ [a SPECIFIC side on paying for grades, name an "
                                         "amount or kind], because ______ [a reason], which matters because "
                                         "______ [the stakes]."),
                 closer="Make the side specific, give a reason a reader could weigh, and say why it matters. "
                        "Then check it against the 3 questions (specific? reason? why it matters?).")),
        Slot("MODEL", "diagnosis_frq", "Check a claim with the 3 questions, then your own",
             ref="", bank="pay_for_grades", scored=True,
             body=frq_prompt(
                 intro="Run the 3-question test on this weak draft, then write a sharp claim of your own.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "A lot of schools are paying students for grades now.", "red"),
                 checklist_block=checklist(title="Run the test:", rows=[
                     ("Is the side specific (names an amount or kind)?",
                      "No, it just reports a trend. Pick a specific position, like a set amount for an A."),
                     ("Is there a reason?", "No. Add one with 'because'."),
                     ("Does it say why it matters (the so-what)?",
                      "No. Add a 'which matters because' beat."),
                 ]),
                 closer="Now write one fresh, specific claim on the pay-for-grades question that passes all "
                        "three. Then run the three checks on your own claim to confirm each one passes.")),

        # ===== INDEPENDENT: autonomy (own side) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write one sharp claim with stakes on paying for grades",
             ref="", bank="pay_for_grades", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="On your own now, no frame. The task: should schools pay students for good grades?",
                 closer="Pick the side you actually hold, then write ONE claim that is specific (name an amount "
                        "or kind), gives a reason, and reaches its stakes (why it matters). Reaching the so-what "
                        "is what lifts a claim to the top, and you are ready to do it cold. Check it against the "
                        "3 questions before you submit.")),

        # ===== TRANSFER: same move, new topic, partitioned bank =====
        Slot("TRANSFER", "stimulus_display", "The debate: free public transit",
             ref="ACC-W910-FRAME-FREETRANSIT", bank="free_transit",
             body=("A new debate. Read the short framing, then take a side. Same move as before, new topic: make "
                   "your side specific and say why it matters. You only need the topic and the two sides.")),
        Slot("TRANSFER", "production_frq", "Write a sharp claim with stakes on a NEW topic",
             ref="", bank="free_transit", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="New topic. The task: should cities make public transit free to ride?",
                 closer="Write ONE arguable claim that is specific (a specific side), gives a reason, and reaches "
                        "its stakes (why it matters). Same move as the pay-for-grades claim, new topic. Check it "
                        "against the 3 questions before you submit.")),
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
