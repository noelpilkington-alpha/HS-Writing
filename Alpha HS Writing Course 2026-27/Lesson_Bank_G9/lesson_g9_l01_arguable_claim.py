"""
lesson_g9_l01_arguable_claim.py  -  G9 KC C.9.01, ARCHETYPE T2: CLAIM-BUILDING (STAND, ceiling = sentence).

FIRST lesson of the G9 course. Authored from icm/stages/06-authoring/output/brief_G9_L01.md, to the T2/STAND
playbook + 19-gate contract. REVISED 2026-07-12 (Noel review): cut instructional redundancy, student-friendly
register, before/after rendered as Timeback-safe inline-styled HTML panels, discrimination triaged to the ONE
signature-error sort. So-what/stakes REMOVED from L01 (that is cS1, mapped to L03 in course-G9.md); L01 holds to
its actual scope, P1 arguable-claim + Dd1 decode-the-verb.
  - KC: C.9.01 (gateway) | unit: G9 U1 | funnel: argument | archetype: T2 (STAND) | ceiling: sentence
  - moves INTRODUCED: P1 arguable-claim (claim vs fact vs opinion), Dd1 decode-the-task-verb
  - acc: [ACC.W.ARG.1] ccss: [W.9-10.1a] | rc.staar
  - taught: ACC-W910-ARG-LESSON-PHONEBAN (phone_ban) -> transfer: ACC-W910-ARG-LESSON-SCHOOLLUNCH (school_lunch)

Timeback-safe: annotated before/after ships as a QTI stimulus authored with INLINE CSS only (no <style>, no JS,
no <table> in <p>), so it renders identically in review and in Platform3. STAND labeled proposal; app-owned
mechanics gated; no near-peer coping model; no source markup; no prior-work reference; no em dashes.
Runs the QC harness on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report

# Timeback-safe inline-styled before/after (all CSS inline; renders in QTI stimulus display + review browser).
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> just a fact, not a claim</span>'
    '<p style="margin:8px 0 0;font-size:15px">"Students use phones during the school day."</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">There is nothing to argue here. It is true, nobody '
    'disputes it, and no reason is attached. Restating a fact is not taking a side.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> an arguable claim, built in two moves</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">SIDE</span> Schools should ban phones for the whole day, '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">REASON</span> because constant alerts pull attention away from learning.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same topic (phones in school), but now it takes a '
    'SIDE and gives a REASON, so someone could disagree with it. That is what makes it an arguable claim.</p>'
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
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-12",
                "mnemonic_status": "proposal",
                "kc": "C.9.01", "sot": "icm course-G9.md L01; KC_Map_and_Unit_Arch_G9-12.md (G9 U1)",
                "brief": "icm/stages/06-authoring/output/brief_G9_L01.md",
                "taught_stimulus": "ACC-W910-ARG-LESSON-PHONEBAN",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-SCHOOLLUNCH",
                "playbook": "_phase2/playbook_T2_STAND.md",
                "revision_note": ("Noel review 2026-07-12: cut redundant 2nd STAND teach card (now Dd1 decode-"
                                  "the-verb, distinct); removed so-what/stakes (cS1, belongs to L03) to hold "
                                  "L01 scope; triaged 2 discriminations -> 1 signature-error sort; student-"
                                  "friendly register; before/after as Timeback-safe inline-HTML panels."),
                "council": ("T2/STAND intro: define arguable-claim vs fact vs opinion (one card, examples do "
                            "double duty); decode-the-verb; annotated fact-to-claim before/after as visual "
                            "panels (no near-peer coping model); predict-the-fix with reveal; claim-vs-fact-vs-"
                            "opinion discrimination labeled Grade-C; frame-provided claim then STAND self-check. "
                            "Sentence ceiling flat. SRSD live ES not claimed for async.")},
    fade_ledger_moves=["decode-the-task-verb", "arguable-claim-vs-fact-vs-opinion", "side-plus-reason"],
    slots=[
        # ================= TEACH: one card on the arguable claim + one on reading the verb =================
        Slot("TEACH", "teach_card", "What makes a claim arguable",
             body=("Three kinds of sentences look alike but do very different jobs, so keep them apart. A FACT "
                   "is something you can check and nobody argues about: 'Most US schools limit phone use during "
                   "the day.' An OPINION is a personal preference with nothing behind it: 'Phones are annoying.' "
                   "An arguable claim is different, and it is what an argument is built on. An arguable claim "
                   "means a sentence that takes a side someone could disagree with AND that you can back up with "
                   "a reason: 'Schools should ban phones all day, because alerts pull focus from learning.' Quick "
                   "test for any claim you write, three questions: Does it take a side? Could someone disagree "
                   "with it? Is there a reason? If you answer no to any of them, it is not an arguable claim "
                   "yet. Watch the trap: writers often restate a fact or drop a bare opinion and think they have "
                   "made a claim. They have not. One word you will see on the scoring: a thesis is a name "
                   "for this arguable claim, the sentence that states the side your whole response defends. "
                   "Today you will write one arguable claim that passes all three questions.")),
        Slot("TEACH", "teach_card", "Read the task first: argue or explain?",
             body=("Before you write, read what the task asks you to do. The verb tells you the job. 'Argue,' "
                   "'take a position,' or 'should schools ... ?' means take a side and defend it. 'Explain' or "
                   "'describe' means lay out how something works, with no side. Getting this wrong is the "
                   "fastest way to answer the wrong question. If a prompt says 'argue whether schools should ban "
                   "phones' and you write a neutral description of the rules, you have not answered it, no "
                   "matter how clear your writing is. So step one is always: what does the verb ask for? Today "
                   "the tasks ask you to argue, so your job is to take a side and give a reason.")),
        Slot("TEACH", "stimulus_display", "The debate: phones in school",
             ref="ACC-W910-FRAME-PHONEBAN", bank="phone_ban",
             body=("Read the short framing of the debate, then take a side. You only need the topic and the two "
                   "sides to write your claim.")),
        Slot("TEACH", "discrimination", "Which one is an arguable claim?",
             ref="", labeled_grade_c=True, bank="phone_ban",
             body=("Sort these before you write your own (we practice spotting the target before producing it, "
                   "a Grade-C design bet we label as a bet, not a proven ingredient). Which sentence is an "
                   "arguable claim, not a fact and not a bare opinion? "
                   "(A) Most US public schools already have written rules that limit phone use during the regular school day.  "
                   "(B) Phones are really annoying in class, and they are one of the most irritating parts of the whole school day.  "
                   "(C) Schools should ban phones for the whole day, because constant alerts pull attention away "
                   "from learning. "
                   "Correct: C. (A) is a FACT you can check and nobody disputes. (B) is a bare OPINION with no "
                   "reason. Only (C) takes a side someone could disagree with and gives a reason, so it passes "
                   "all three questions.")),

        # ================= MODEL: visual before/after panels -> predict-the-fix =================
        Slot("MODEL", "annotated_before_after", "Watch a fact turn into an arguable claim",
             bank="phone_ban",
             body=("Here is a fact being rebuilt into an arguable claim. Read the BEFORE, then the AFTER, and "
                   "notice the two moves that were added: a SIDE and a REASON. " + BEFORE_AFTER_HTML +
                   " The BEFORE only restates something true. The AFTER takes a side someone could reject and "
                   "attaches a reason. Adding the side and the reason is the whole move.")),
        Slot("MODEL", "predict_the_fix", "Is this an arguable claim, and if not, what fixes it?",
             bank="phone_ban",
             body=("Diagnose this draft before the reveal. The task asked the student to argue whether schools "
                   "should ban phones for the full day. The student wrote: 'Phone rules in schools have changed "
                   "a lot over the years.' Which single move would most improve it? "
                   "(A) take a side on the full-day ban and add a reason  "
                   "(B) add one more fact about how the phone rules changed  "
                   "(C) make the sentence longer and use more formal words  "
                   "(D) describe how phones work during the school day"),
             feedback=("Correct: A. The draft states a fact that nobody disputes, and it never answers the "
                       "question, whether to ban phones all day. So it is not an arguable claim. The fix is to "
                       "take a side and add a reason: 'Schools should ban phones all day, because alerts pull "
                       "focus from learning.' Another fact (B), a longer sentence (C), or explaining how phones "
                       "work (D) never turn a fact into a claim.")),

        # ================= SUPPORTED: framed claim -> STAND self-check =================
        Slot("SUPPORTED", "production_frq", "Finish the claim: add your side and a reason",
             ref="", bank="phone_ban", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("Finish this claim about the phone source. The frame gives you the shape so you can focus on "
                   "the side and the reason: 'Schools should ______ [your side on the full-day ban], because "
                   "______ [a reason from the source].' Goal: take a clear side and give a reason a reader "
                   "could weigh. Do not restate a fact. Write one sentence. Scored on Thesis/Purpose.")),
        Slot("MODEL", "diagnosis_frq", "Check your claim with the three questions",
             ref="", bank="phone_ban", scored=True,
             body=("First watch the check run on a weak draft, then run it on a fresh claim of your own. Weak "
                   "draft: 'Lots of schools have phone rules now.' Run the three-question checklist step by "
                   "step. Step 1, side: does it take a side on the full-day ban? No, it just reports a fact, so "
                   "the fix is to pick a side. Step 2, could someone disagree? No, nobody argues with it yet. "
                   "Step 3, reason: is there a because-reason? No, add one. Now you: write one fresh claim on "
                   "the phone task, then run the same three questions on it. For each No, use the fix: pick a "
                   "side, word it so someone could disagree, add 'because ____.' Finish by naming which "
                   "question your sentence still needs most.")),

        # ================= INDEPENDENT: one arguable claim, self-checked =================
        Slot("INDEPENDENT", "production_frq", "Write one arguable claim on the phone source",
             ref="", bank="phone_ban", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("On your own now. The task: argue whether schools should ban phones for the whole day. Write "
                   "ONE arguable claim sentence. Goal: take a clear side, word it so someone could disagree, and "
                   "add a reason from the source. Before you submit, run the three questions on your claim: is "
                   "there a side, could someone disagree, is there a reason? If any answer is no, fix it before "
                   "you submit. Do not restate a fact or drop a bare opinion. Scored on Thesis/Purpose.")),

        # ================= TRANSFER: same move, new topic, partitioned bank =================
        Slot("TRANSFER", "stimulus_display", "The debate: free school meals",
             ref="ACC-W910-FRAME-SCHOOLLUNCH", bank="school_lunch",
             body=("Read the short framing of this new debate, then take a side. Same as before, you only need "
                   "the topic and the two sides to write your claim.")),
        Slot("TRANSFER", "production_frq", "Write an arguable claim on a NEW topic",
             ref="", bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("New topic. The task: argue whether schools should give free meals to all students. Write "
                   "ONE arguable claim sentence. Goal: take a clear side, word it so someone could disagree, and "
                   "add a reason from this source. Same move as the phone claim, new topic. Do not restate a "
                   "fact or drop a bare opinion. Scored on Thesis/Purpose.")),
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
