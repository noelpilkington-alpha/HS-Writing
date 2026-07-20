"""
lesson_g9_l01_arguable_claim_v3.py  -  G9 KC C.9.01, ARCHETYPE T2 (STAND, sentence ceiling). V3.

V3 (Noel 2026-07-14), built on the Fable-5 async-student eval of v1 vs v2 + Noel's density/quality directives:
  - KEEP v2's spine: TEACH -> MODEL -> DECOMPOSE-the-model (the decompose beat scored as the single most useful
    step; students named "weld the reason on with because" as the move they reach for).
  - ADD BACK v1's FILL-IN FRAME as the first supported write ("Schools should ___, because ___") - struggling +
    average students called it the most useful single thing; v2 dropped it and weaker students felt dumped into
    solo writing. Framed write -> then independent (unframed) -> then transfer.
  - DEDUP: the taught topic appears in exactly the moves that need it; ONE independent write on the taught topic
    (v1 had 3 near-identical phone writes; students skimmed/copy-pasted). One taught + one transfer.
  - OPERATIONAL NECESSITY (Noel): only what the student must DO to write an arguable claim. "thesis" is NOT
    operationally required -> demoted to a <dfn> TOOLTIP (player renders tap-to-reveal), out of the reading flow.
  - LEAK FIX: no "Grade-C design bet" / internal jargon in student text (gate_leaked_internal_label); discrimination
    prompt reworded plainly. No "Try again" text inside options (gate_leaked_answer_cue).
  - NEW TOPIC (Noel): taught = four-day school week; transfer = pay-for-grades (partitioned banks). Phones dropped.
  - ONE IDEA: an arguable claim takes a SIDE and gives a REASON. ONE REMINDER: the 3-question test.

Passes all lesson_contract gates (incl. the 3 new ones). Own words, no fabricated figures, no em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">An arguable claim takes a '
'<strong>SIDE</strong> and gives a <strong>REASON</strong>. A fact or a bare opinion is not a claim.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Remember: SIDE + REASON</div>'
'<div style="color:#1f2a44;font-size:14px;margin-top:2px">Before you submit any claim, run the 3-question test: '
'<strong>1.</strong> Does it take a side?  <strong>2.</strong> Could someone disagree?  '
'<strong>3.</strong> Is there a reason?  If any answer is no, it is not an arguable claim yet.</div></div>')

# worked before/after (BOTH examples inline -> content_depth gate)
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> just a fact, not a claim</span>'
    '<p style="margin:8px 0 0;font-size:15px">"Some school districts have tried a four-day week."</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">Nothing to argue. It is true, nobody disputes it, '
    'and no reason is attached.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> an arguable claim, built in two moves</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">SIDE</span> Schools should switch to a four-day week, '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">REASON</span> because a longer weekend gives students real time to rest and catch up.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same topic, but now it takes a SIDE and gives a '
    'REASON, so someone could disagree with it. That is what makes it an arguable claim.</p>'
  '</div>'
'</div>')

# decompose the finished claim into its two moves (the beat students rated highest)
DECOMPOSE_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#f0fdf4;padding:10px 14px;border-bottom:1px solid #bbf7d0;font-size:15px">'
    'The finished claim: <em>"Schools should switch to a four-day week, because a longer weekend gives students '
    'real time to rest and catch up."</em></div>'
  '<div style="padding:12px 14px">'
    '<div style="margin:0 0 10px">'
      '<span style="display:inline-block;background:#dbeafe;color:#1e3a8a;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">MOVE 1 - SIDE</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px"><strong>"Schools should switch to a four-day '
      'week"</strong> The writer picks a position on the exact question asked. It is a "should" sentence someone '
      'could reject, not a neutral fact. That is what makes it arguable.</div></div>'
    '<div>'
      '<span style="display:inline-block;background:#fef9c3;color:#854d0e;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">MOVE 2 - REASON</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px">"...<strong>because a longer weekend gives '
      'students real time to rest and catch up</strong>." One because-reason gives the side support. Drop this '
      'clause and only the bare side is left, which a reader cannot yet weigh.</div></div>'
    '<div style="margin-top:10px;color:#0f766e;font-size:13px">Two moves, joined with '
    '<strong>because</strong>. That is the whole construction. Every claim you write is built the same way.</div>'
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
    provenance={"copyright": "own_authored", "authored": "2026-07-14", "revised": "2026-07-14",
                "mnemonic_status": "proposal",
                "kc": "C.9.01", "sot": "icm course-G9.md L01; KC_Map_and_Unit_Arch_G9-12.md (G9 U1)",
                "taught_stimulus": "ACC-W910-FRAME-FOURDAYWEEK",
                "transfer_stimulus": "ACC-W910-FRAME-PAYGRADES",
                "playbook": "_phase2/playbook_T2_STAND.md",
                "one_idea": "An arguable claim takes a SIDE and gives a REASON.",
                "one_reminder": "3-question test: side? disagree? reason?",
                "version_note": ("V3: v2 spine (teach->model->decompose) + v1 fill-in frame restored as first "
                                 "supported write; deduped to one taught + one transfer write; 'thesis' demoted "
                                 "to a tooltip (operational-necessity); leaked internal labels stripped from the "
                                 "discrimination prompt; new topic (four-day week taught / pay-for-grades "
                                 "transfer). Built from the Fable-5 v1-vs-v2 async-student eval."),
                "council": ("Teach fact/opinion/claim visually (S01 diagram) -> model fact->claim (before/after + "
                            "S05 diagram) -> decompose into SIDE + REASON moves -> one plain discrimination -> "
                            "framed supported write -> independent write -> transfer write on a partitioned "
                            "topic. Non-operational term 'thesis' behind a tooltip. Sentence ceiling flat.")},
    fade_ledger_moves=["decode-the-task-verb", "arguable-claim-vs-fact-vs-opinion", "side-plus-reason"],
    slots=[
        # ===== TEACH: one idea, taught visually (S01 diagram = slot 1) + one reminder =====
        Slot("TEACH", "teach_card", "The one idea: take a SIDE, give a REASON",
             body=(ONE_IDEA +
                   "Three kinds of sentence look alike but do different jobs, so keep them apart. A "
                   "<strong>FACT</strong> is something you can check and nobody argues about ('Some districts "
                   "have tried a four-day week'). An <strong>OPINION</strong> is a bare preference with nothing "
                   "behind it ('A four-day week sounds great'). An <strong>arguable claim</strong> means a "
                   "sentence that takes a side someone could disagree with AND backs it with a reason ('Schools "
                   "should switch to a four-day week, because a longer weekend gives students real time to "
                   "rest'). That is the sentence an argument is built on. (Scoring sometimes calls this a "
                   "<dfn class=\"tb-glossary-term\" data-catalog-idref=\"def-thesis\" "
                   "title=\"Thesis: another name for the arguable claim your whole response defends. You do not "
                   "need this word to finish today's task.\">thesis</dfn>, but you do not need that word for "
                   "today's task.) One quick habit first: read the task verb. 'Argue' or 'should schools ... ?' "
                   "means take a side; 'explain' means lay out how something works with no side. Today's task "
                   "asks you to argue, so your job is to take a side and give a reason." + REMEMBER)),
        Slot("TEACH", "stimulus_display", "The debate: a four-day school week",
             ref="ACC-W910-FRAME-FOURDAYWEEK", bank="four_day_week",
             body=("Read the short framing of the debate, then you will practice spotting a real claim before "
                   "you write one. You only need the topic and the two sides.")),
        Slot("TEACH", "discrimination", "Which one is the arguable claim?",
             ref="", labeled_grade_c=True, bank="four_day_week",
             body=("Spot the target before you build your own. Which sentence is an arguable claim, not a fact "
                   "and not a bare opinion? "
                   "(A) A good number of school districts across the country have already tested out a four-day school week in recent years, some for a while now.  "
                   "(B) Honestly, switching over to a four-day school week just sounds like a really nice and genuinely fun idea to me and my friends.  "
                   "(C) Schools should adopt a four-day week, because a longer weekend lets students rest and catch up. "
                   "Correct: C. (A) is a FACT you can check and nobody disputes. (B) is a bare OPINION with no "
                   "reason. Only (C) takes a side someone could disagree with and gives a reason.")),

        # ===== MODEL + DECOMPOSE: before/after (S05 diagram = slot 4), then break it down =====
        Slot("MODEL", "annotated_before_after", "Model: watch a fact become an arguable claim",
             bank="four_day_week",
             body=("Here is the skill in action. The writer starts from a plain fact and rebuilds it into an "
                   "arguable claim by adding just two things: a SIDE and a REASON. Read the before, then the "
                   "after, and watch what got added. " + BEFORE_AFTER_HTML +
                   " The before only restates something true. The after takes a side someone could reject and "
                   "attaches a reason. Adding the side and the reason is the whole move.")),
        Slot("MODEL", "teach_card", "Decompose it: how the writer built the claim",
             body=("Now take the finished claim apart to see how it was built, piece by piece. Every arguable "
                   "claim is joined from the same two moves." + DECOMPOSE_HTML +
                   "When you write your own in a moment, build it the same way: state the side first, then join "
                   "a reason with 'because.'")),
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
                       "you just decomposed: take a side, then join a reason ('Schools should switch to a "
                       "four-day week, because a longer weekend gives students time to rest'). Another fact (B), "
                       "a longer sentence (C), or describing the schedule (D) never turn a fact into a claim.")),

        # ===== SUPPORTED: the fill-in frame (v1's best-rated scaffold), restored =====
        Slot("SUPPORTED", "production_frq", "Finish the claim: fill in the side and the reason",
             ref="", bank="four_day_week", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("Use the frame so you can focus on the two moves. Fill in the blanks: 'Schools should ______ "
                   "[your side on the four-day week], because ______ [your reason].' Take a clear side and give "
                   "a reason a reader could weigh. Do not restate a fact. Write one sentence. Scored on "
                   "Thesis/Purpose.")),
        Slot("MODEL", "diagnosis_frq", "Check a claim with the 3 questions, then your own",
             ref="", bank="four_day_week", scored=True,
             body=("First watch the 3-question checklist run on a weak draft, then run it on a fresh claim of "
                   "your own. Weak draft: 'A lot of districts have four-day weeks now.' Step 1, side: does it "
                   "take a side on the switch? No, it reports a fact, so pick a side. Step 2, could someone "
                   "disagree? No, nobody argues with it. Step 3, reason: is there a because-reason? No, add one. "
                   "Now you: write one fresh claim on the four-day-week task, then run the same three questions "
                   "on it. For each No, use the fix: pick a side, word it so someone could disagree, add "
                   "'because ____.' Finish by naming which question your sentence still needs most.")),

        # ===== INDEPENDENT: one arguable claim, unframed, self-checked =====
        Slot("INDEPENDENT", "production_frq", "Write one arguable claim on the four-day week",
             ref="", bank="four_day_week", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("On your own, no frame this time. The task: argue whether schools should switch to a four-day "
                   "week. Write ONE arguable claim sentence, built from the two moves: a SIDE, then a REASON "
                   "joined with 'because.' Before you submit, run the 3-question test (side? could someone "
                   "disagree? reason?) and fix any No. Do not restate a fact or drop a bare opinion. Scored on "
                   "Thesis/Purpose.")),

        # ===== TRANSFER: same two moves, new topic, partitioned bank =====
        Slot("TRANSFER", "stimulus_display", "The debate: paying students for grades",
             ref="ACC-W910-FRAME-PAYGRADES", bank="pay_for_grades",
             body=("A new debate. Read the short framing, then take a side. Same two moves as before, new topic. "
                   "You only need the topic and the two sides.")),
        Slot("TRANSFER", "production_frq", "Write an arguable claim on a NEW topic",
             ref="", bank="pay_for_grades", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("New topic. The task: argue whether schools should pay students for good grades. Write ONE "
                   "arguable claim sentence using the same construction: SIDE, then REASON joined with "
                   "'because.' Run the 3-question test before you submit. Do not restate a fact or drop a bare "
                   "opinion. Scored on Thesis/Purpose.")),
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
