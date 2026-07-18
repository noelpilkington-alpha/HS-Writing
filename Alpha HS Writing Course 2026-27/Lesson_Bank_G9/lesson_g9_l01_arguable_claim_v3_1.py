"""
lesson_g9_l01_arguable_claim_v3_1.py  -  G9 KC C.9.01, ARCHETYPE T2 (STAND, sentence). V3.1.

V3.1 (Noel 2026-07-14): applies the adjudicated Council + Fable reviewer findings on v3. Changes:
  1. SPLIT STEP 1 (KH, load): teach only fact/opinion/claim + the SIDE+REASON idea + the thesis tooltip; the
     3-question self-check is NO LONGER cold in step 1 - it is introduced at the decompose card, right before
     the student first diagnoses/writes (point of first use). Verb habit trimmed to one sentence.
  2. MODEL BEFORE THE QUIZ (KH): the worked example + decompose now PRECEDE the discrimination check (student
     sees the schema-building model before being quizzed). Discrimination moved into MODEL role.
  3. COPING-MODEL THINK-ALOUD (SRSD, ES 1.14 for struggling writers): the model is rewritten as a written
     drafting process (attempt -> test -> catch the bare fact -> revise to add side + reason), not just a clean
     finished panel. Still contains BOTH BEFORE and AFTER (content_depth). No named near-peer (Timeback rule).
  4. FIX THE 'BECAUSE' CONFOUND (DI, faultless communication): in v3 the correct option was the ONLY one with
     the word 'because', so a novice could match the token not the structure. Now a DISTRACTOR contains
     'because' (on a fact) and the CORRECT claim uses NO 'because' - so SIDE+REASON is the only invariant.
  5. AUTONOMY + SAY-THE-STANDARD (Yeager): the independent write lets the student pick the side they actually
     hold and names the standard out loud ('this is what every real argument is built on; you are ready').
  eg (voice/formula) recorded as a risk to monitor across the unit (dissent seat, not an evidence ruling).

ONE IDEA: an arguable claim takes a SIDE and gives a REASON. ONE REMINDER: the 3-question test.
Passes all 23 lesson_contract gates. Own words, no fabricated figures, no em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">An arguable claim takes a '
'<strong>SIDE</strong> and gives a <strong>REASON</strong>. A fact or a bare opinion is not a claim.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit any claim, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does it take a side?</li>'
'<li style="margin:2px 0">Could someone disagree?</li>'
'<li style="margin:2px 0">Is there a reason?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, it is not an arguable claim yet.</div></div>')

# coping-model think-aloud panel: a WRITTEN drafting process (attempt -> test -> revise), then the endpoints.
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer thinking it through, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Some districts have tried a four-day week." '
    'Check it: does it take a side? No, that is just a fact. Nobody would argue with it. Start over.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "Schools should switch to a four-day week." '
    'Better, that takes a side someone could reject. Could someone disagree? Yes. Is there a reason? Not yet. '
    'Add one.</p>'
    '<p style="margin:0"><strong>Final:</strong> "Schools should switch to a four-day week, because a longer '
    'weekend gives students real time to rest." Side, and a reason. That passes.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "Some districts have tried a four-day week." (just a fact)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "Schools should switch to a four-day week, because a longer '
    'weekend gives students real time to rest." (an arguable claim)</span></div>'
'</div>')

DECOMPOSE_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#f0fdf4;padding:10px 14px;border-bottom:1px solid #bbf7d0;font-size:15px">'
    'The finished claim: <em>"Schools should switch to a four-day week, because a longer weekend gives students '
    'real time to rest."</em></div>'
  '<div style="padding:12px 14px">'
    '<div style="margin:0 0 10px">'
      '<span style="display:inline-block;background:#dbeafe;color:#1e3a8a;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">MOVE 1 - SIDE</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px"><strong>"Schools should switch to a four-day '
      'week"</strong> The writer picks a position someone could reject, not a neutral fact.</div></div>'
    '<div>'
      '<span style="display:inline-block;background:#fef9c3;color:#854d0e;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">MOVE 2 - REASON</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px">"...<strong>a longer weekend gives students real '
      'time to rest</strong>." A reason gives the side support (here joined with the word "because," though a '
      'claim does not always need that exact word).</div></div>'
    '<div style="margin-top:10px;color:#0f766e;font-size:13px">A side plus a reason. That is the whole '
    'construction. Every claim you write is built the same way.</div>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C901-0001", grade="9-10", lesson_type=2,
    unit="G9 U1 - Claim/controlling-idea + evidence (arguable claim)",
    title="Take a Side Someone Could Argue With",
    target=("Write one arguable claim: read what the task asks, take a clear side, and give a reason. A claim "
            "is arguable when someone could disagree with it and you can back it up. Written at the sentence. "
            "Trait: Thesis/Purpose."),
    acc_tags=["ACC.W.ARG.1", "CCSS.W.9-10.1a"],
    provenance={"copyright": "own_authored", "authored": "2026-07-14", "revised": "2026-07-15",
                "mnemonic_status": "proposal",
                "kc": "C.9.01", "sot": "icm course-G9.md L01; KC_Map_and_Unit_Arch_G9-12.md (G9 U1)",
                "taught_stimulus": "ACC-W910-FRAME-FOURDAYWEEK",
                "transfer_stimulus": "ACC-W910-FRAME-PAYGRADES",
                "one_idea": "An arguable claim takes a SIDE and gives a REASON.",
                "one_reminder": "3-question test: side? disagree? reason?",
                "version_note": ("V3.1: applied adjudicated Council+Fable findings on v3 - split Step 1 (KH load), "
                                 "model+decompose now precede the quiz (KH), coping-model think-aloud (SRSD ES "
                                 "1.14), fixed the 'because' confound in the discrimination (DI faultless "
                                 "communication), autonomy + say-the-standard on the independent write (Yeager). "
                                 "eg voice/formula concern = risk to monitor across the unit."),
                "review_provenance": ("Fable-5 reviewer (pipeline/lesson_review.py) + Council review mode "
                                      "(twr/srsd/di/kh/yeager/eg), adjudicated by evidence grade 2026-07-14.")},
    fade_ledger_moves=["decode-the-task-verb", "arguable-claim-vs-fact-vs-opinion", "side-plus-reason"],
    slots=[
        # ===== TEACH: ONE idea only (split; no cold 3-question test, verb trimmed to one line) =====
        Slot("TEACH", "teach_card", "The one idea: take a SIDE, give a REASON",
             body=(ONE_IDEA +
                   "Three kinds of sentence look alike but do different jobs, so keep them apart:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>FACT</strong>: something you can check and nobody argues "
                   "about ('Some districts have tried a four-day week').</li>"
                   "<li style=\"margin:4px 0\"><strong>OPINION</strong>: a bare preference with nothing behind it "
                   "('A four-day week sounds great').</li>"
                   "<li style=\"margin:4px 0\"><strong>Arguable claim</strong>: a sentence that takes a side "
                   "someone could disagree with AND backs it with a reason ('Schools should switch to a four-day "
                   "week, because a longer weekend gives students real time to rest').</li></ul>"
                   "That last one is the sentence an argument is built on. (Scoring sometimes calls this a "
                   "<dfn class=\"tb-glossary-term\" data-catalog-idref=\"def-thesis\" "
                   "title=\"Thesis means the arguable claim your whole response defends. You do not need this "
                   "word to finish today's task.\">thesis</dfn>, but you do not need that word for "
                   "today's task.) One habit first: when a task says 'argue' or 'should schools ... ?', it wants "
                   "a side; 'explain' wants no side. Today's task asks you to argue.")),
        Slot("TEACH", "stimulus_display", "The debate: a four-day school week",
             ref="ACC-W910-FRAME-FOURDAYWEEK", bank="four_day_week",
             body=("Read the short framing of the debate. In a moment you will watch a claim get built, then "
                   "build your own. You only need the topic and the two sides.")),

        # ===== MODEL (before the quiz): ONE coping-model think-aloud card, with the check tool folded in.
        # Council 2026-07-14 (SRSD+KH+Yeager, A-grade evidence): keep the coping-model think-aloud (mandated
        # Model It, worked-example effect); the standalone MOVE 1/MOVE 2 decompose was the redundancy effect
        # (re-presenting the SIDE+REASON structure the student just processed) -> removed. Only non-redundant
        # asset kept from it = the 3-question check tool (the reusable job-aid / autonomy handoff). =====
        Slot("MODEL", "annotated_before_after", "Watch a writer build an arguable claim",
             bank="four_day_week",
             body=("Here is the skill in action. Follow the writer's thinking below. " + COPING_HTML +
                   " Notice the two moves that turned the BEFORE into the AFTER: the writer took a "
                   "<strong>side</strong> someone could reject, then added a <strong>reason</strong>. " + REMEMBER +
                   "When you write your own, build it the same way: pick the side first, then add a reason, and "
                   "run the 3 questions before you submit.")),
        Slot("MODEL", "discrimination", "Which one is the arguable claim?",
             ref="", labeled_grade_c=True, bank="four_day_week",
             body=("Now that you have seen one built, spot the target. Which sentence is an arguable claim, not a "
                   "fact and not a bare opinion? "
                   "(A) Some districts switched to a four-day week because an old budget shortfall forced their hand during a difficult year.  "
                   "(B) Honestly, a four-day school week just sounds like a really nice idea to me and my friends.  "
                   "(C) Districts should keep the five-day week, because students lose ground when a full teaching day is cut. "
                   "Correct: C. It takes a side someone could disagree with AND gives a reason."),
             choices=[
                 {"id": "A", "text": "Some districts switched to a four-day week because an old budget shortfall forced their hand during a difficult year.",
                  "correct": False,
                  "why": "This has the word 'because,' but it only explains a past fact nobody argues with. A because-clause on a fact is still not a claim."},
                 {"id": "B", "text": "Honestly, a four-day school week just sounds like a really nice idea to me and my friends.",
                  "correct": False,
                  "why": "This is a bare opinion, a preference with no reason attached. An opinion is not yet a claim."},
                 {"id": "C", "text": "Districts should keep the five-day week, because students lose ground when a full teaching day is cut.",
                  "correct": True,
                  "why": "Correct. It takes a side someone could disagree with (keep five days) AND gives a reason (lost teaching time). The side plus the reason is what makes a claim, not any single word."},
             ]),
        Slot("MODEL", "discrimination", "Which sentence takes a side AND gives a reason?",
             ref="", labeled_grade_c=True, bank="four_day_week",
             body=("One more set, this time watch for a side with nothing behind it. Which sentence is an "
                   "arguable claim: one that takes a side and backs it with a reason? "
                   "(A) In many four-day plans, the school day simply runs longer and one weekday is dropped from the calendar.  "
                   "(B) Schools should keep the five-day week.  "
                   "(C) A four-day week would help students, since a lighter week keeps them more focused in class. "
                   "Correct: C. It takes a side someone could reject and gives a reason for it, while a side with no reason is not finished."),
             choices=[
                 {"id": "A", "text": "In many four-day plans, the school day simply runs longer and one weekday is dropped from the calendar.",
                  "correct": False,
                  "why": "This just reports how the schedule works, a fact no one would argue with, so it takes no side and is not a claim."},
                 {"id": "B", "text": "Schools should keep the five-day week.",
                  "correct": False,
                  "why": "This takes a clear side someone could reject, but it gives no reason to back that side, so it is not a finished claim yet."},
                 {"id": "C", "text": "A four-day week would help students, since a lighter week keeps them more focused in class.",
                  "correct": True,
                  "why": "Correct. It takes a side someone could disagree with and gives a reason for that side, and a side plus a reason is what makes a claim."},
             ]),
        Slot("MODEL", "predict_the_fix", "Is this an arguable claim, and if not, what fixes it?",
             bank="four_day_week",
             body=("Diagnose this draft before the reveal. The task asked the student to argue whether schools "
                   "should switch to a four-day week. The student wrote: 'School schedules have changed in a lot "
                   "of places over the years.' Which single move would most improve it? "
                   "(A) take a side on the four-day week and add a reason  "
                   "(B) add one more fact about how schedules have changed  "
                   "(C) make the sentence longer and use more formal words  "
                   "(D) describe how a normal school day is scheduled"),
             feedback=("Correct: A. The draft states a fact nobody disputes and never answers the question, "
                       "whether to switch to four days, so it is not an arguable claim. The fix is the two moves "
                       "you just saw: take a side, then add a reason ('Schools should switch to a four-day week, "
                       "because a longer weekend gives students time to rest'). Another fact (B), a longer "
                       "sentence (C), or describing the schedule (D) never turn a fact into a claim.")),

        # ===== SUPPORTED: framed write (fill-in frame) on the taught topic (source already read at STEP 2) =====
        Slot("SUPPORTED", "production_frq", "Finish the claim: fill in the side and the reason",
             ref="", bank="four_day_week", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on the two moves.",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "Schools should ______ [your side on the four-day week], because ______ [your reason]."),
                 closer="Take a clear side and give a reason a reader could weigh. Then check it against the 3 "
                        "questions.")),
        # DIAGNOSIS = a CHECK-and-FIX exercise on a PROVIDED draft (not a fresh production, so it does not repeat
        # the Finish write). Stays on the taught topic = no new source to read (load balance). Noel 2026-07-14:
        # the three PRODUCED claims (Finish / Independent / Transfer) now sit on THREE DIFFERENT topics so a
        # student cannot reuse one sentence; this self-check is the fourth beat but produces no new claim.
        Slot("MODEL", "diagnosis_frq", "Check and fix a weak draft with the 3 questions",
             ref="", bank="four_day_week", scored=True,
             body=frq_prompt(
                 intro="Run the 3-question test on this weak draft, then rewrite it into a real claim.",
                 setapart_block=setapart("Weak draft to fix:", "A lot of districts have four-day weeks now.", "red"),
                 checklist_block=checklist(title="Run the test:", rows=[
                     ("Does it take a side on the switch?", "No, it just reports a fact. Pick a side."),
                     ("Could someone disagree?", "No, nobody argues with it. Word it so they could."),
                     ("Is there a reason?", "No. Add one with 'because'."),
                 ]),
                 closer="Now rewrite the weak draft into one arguable claim that passes all three. "
                        "Then name which question your rewrite fixed.")),

        # ===== INDEPENDENT: cold write on a DIFFERENT topic (pay-for-grades) + autonomy + say-the-standard =====
        Slot("INDEPENDENT", "stimulus_display", "The debate: paying students for grades",
             ref="ACC-W910-FRAME-PAYGRADES", bank="pay_for_grades",
             body=("A different debate now, so you build a fresh claim instead of reusing the last one. Read the "
                   "short framing, then take a side. You only need the topic and the two sides.")),
        Slot("INDEPENDENT", "production_frq", "Write one arguable claim on paying for grades",
             ref="", bank="pay_for_grades", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="On your own now, no frame. The task: should schools pay students for good grades?",
                 closer="Pick the side you actually believe, then add a reason. This side-plus-reason move is "
                        "what every real argument is built on, and you are ready to do it cold. Check your "
                        "sentence against the 3 questions before you submit.")),

        # ===== TRANSFER: same move, a THIRD topic (free transit), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "The debate: free public transit",
             ref="ACC-W910-FRAME-FREETRANSIT", bank="free_transit",
             body=("One more new debate. Read the short framing, then take a side. Same move, a fresh topic, so "
                   "again you write a new claim. You only need the topic and the two sides.")),
        Slot("TRANSFER", "production_frq", "Write an arguable claim on a NEW topic",
             ref="", bank="free_transit", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="New topic. The task: should cities make public transit free to ride?",
                 closer="Write ONE arguable claim: pick a side, then add a reason. Check it against the 3 "
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
