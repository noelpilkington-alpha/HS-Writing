"""
lesson_g9_l02_take_position.py  -  G9 KC C.9.01, ARCHETYPE T2: CLAIM-BUILDING (STAND, ceiling = sentence).

G9 course L02. Guided practice of the arguable claim on a NEW topic; deepens P3 (prompt-responsive vs
topic-drift). REVISED 2026-07-12 to the locked L01 template: student register, one focused teach concept,
visual Timeback-safe before/after, ONE signature-error discrimination, and a bound issue_frame (not a 480-word
source) so the reading load matches a claim task. Taught frame = FRAME-SCHOOLLUNCH; transfer frame =
FRAME-COMMUNITYSERVICE (bank-partitioned). rc.staar, unit="sentence". STAND labeled proposal; mechanics gated;
no coping-model persona; no source markup; no prior-work reference; no em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report

BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> on the topic, but not the question</span>'
    '<p style="margin:8px 0 0;font-size:15px">"Eating well is important for students."</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The task asks whether meals should be FREE for '
    'ALL students. This is true, but it answers the general topic of eating, not the actual question.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> answers the exact question</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">SIDE</span> Schools should give free meals to every student, '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">REASON</span> because hunger in class blocks learning for the students who need '
      'school most.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">This takes a side on the real question, free for '
    'all, and gives a reason. It answers the prompt, not just the topic.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C901-0002", grade="9-10", lesson_type=2,
    unit="G9 U1 - Claim/controlling-idea + evidence (take a position)",
    title="Answer the Exact Question, Not the Topic",
    target=("Write one arguable claim that answers the specific question a task asks, not the general subject. "
            "Take a side and give a reason. Written at the sentence. Trait: Thesis/Purpose."),
    acc_tags=["ACC.W.ARG.1", "CCSS.W.9-10.1a"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-12",
                "mnemonic_status": "proposal", "kc": "C.9.01", "sot": "icm course-G9.md L02",
                "taught_stimulus": "ACC-W910-FRAME-SCHOOLLUNCH",
                "transfer_stimulus": "ACC-W910-FRAME-COMMUNITYSERVICE",
                "playbook": "_phase2/playbook_T2_STAND.md",
                "revision_note": "Locked L01 template: student register, one teach concept, visual before/after, one discrimination, bound issue_frame.",
                "council": "T2/STAND guided rung: recycles arguable-claim, deepens prompt-responsive (responsive vs topic-drift)."},
    fade_ledger_moves=["prompt-responsive-vs-topic-drift", "side-plus-reason"],
    slots=[
        Slot("TEACH", "teach_card", "Answer the question the task actually asks",
             body=("You already know an arguable claim: a sentence that takes a side someone could disagree "
                   "with and backs it with a reason. Today's focus is the most common way a claim goes wrong "
                   "even when it takes a side: it answers the TOPIC instead of the QUESTION. If a task asks "
                   "'should schools give free meals to ALL students,' and you write 'school lunch matters,' you "
                   "are on the topic of lunch but you never answered the actual question, whether meals should "
                   "be free for everyone. That is topic-drift, and it scores low no matter how true it sounds. "
                   "The word the scoring uses for your governing claim is thesis, which is a name for the "
                   "arguable claim your whole response defends. So before you write, pin down the exact "
                   "question, then make your claim land right on it. Also read the task verb: 'argue' or "
                   "'should ... ?' means take a side; 'explain' means lay out how something works with no side. "
                   "Today the task asks you to argue.")),
        Slot("TEACH", "stimulus_display", "The debate: free school meals",
             ref="ACC-W910-FRAME-SCHOOLLUNCH", bank="school_lunch",
             body=("Read the short framing of the debate, then take a side. The exact question is whether meals "
                   "should be free for ALL students. You only need the topic and the two sides to write your "
                   "claim.")),
        Slot("TEACH", "discrimination", "Which claim answers the question?",
             ref="", labeled_grade_c=True, bank="school_lunch",
             body=("Sort these before you write (we practice spotting the target before producing it, a Grade-C "
                   "design bet we label as a bet, not a proven ingredient). The question is whether schools "
                   "should give free meals to ALL students. Which sentence answers that exact question, not "
                   "just the topic? "
                   "(A) School meals are an important part of the school day, and a good lunch gives "
                   "students the energy they need for their afternoon classes.  "
                   "(B) Nutrition affects how well students can concentrate, and kids who eat a balanced "
                   "breakfast often stay more focused through the morning.  "
                   "(C) Schools should give free meals to every student, because hunger in class blocks "
                   "learning for the students who need school most. "
                   "Correct: C. (A) and (B) are true statements about school food, but neither answers whether "
                   "meals should be free for ALL. Only (C) takes a side on the actual question and gives a "
                   "reason.")),
        Slot("MODEL", "annotated_before_after", "Watch a topic sentence become a claim that answers the question",
             bank="school_lunch",
             body=("Here is a topic sentence being rebuilt into a claim that answers the exact question. Read "
                   "the BEFORE, then the AFTER, and notice it now lands on the real question and adds a reason. "
                   + BEFORE_AFTER_HTML +
                   " The BEFORE drifts to the general topic. The AFTER answers whether meals should be free for "
                   "ALL and gives a reason. Landing on the exact question is the move.")),
        Slot("MODEL", "predict_the_fix", "Does this answer the question, and if not, what fixes it?",
             bank="school_lunch",
             body=("Diagnose this draft before the reveal. The task asks whether schools should give free meals "
                   "to all students. The student wrote: 'Good nutrition helps kids do better in school.' Which "
                   "single move would most improve it? "
                   "(A) take a side on whether meals should be FREE for ALL, and add a reason  "
                   "(B) add a fact about which foods are the healthiest ones for students to eat  "
                   "(C) make the sentence longer by adding more describing words and detail  "
                   "(D) describe what a typical school lunch tray usually looks like at noon"),
             feedback=("Correct: A. The draft is true and on the topic of nutrition, but it never answers the "
                       "actual question, whether meals should be free for all. That is topic-drift. The fix is "
                       "to land on the exact question and add a reason: 'Schools should give free meals to "
                       "every student, because hunger in class blocks learning.' A fact about foods (B), a "
                       "longer sentence (C), or a description of lunch (D) all stay on the topic without "
                       "answering the question.")),
        Slot("SUPPORTED", "production_frq", "Finish the claim: answer the question, add a reason",
             ref="", bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("Finish this claim about the free-meals question: 'Schools should ______ [your side on "
                   "free-for-all], because ______ [a reason from the framing].' Goal: your side must answer the "
                   "exact question (free for ALL students), and your reason must fit the debate. Do not drift "
                   "to the general topic of nutrition. Write one sentence. Scored on Thesis/Purpose.")),
        Slot("MODEL", "diagnosis_frq", "Check your claim: does it answer the question?",
             ref="", bank="school_lunch", scored=True,
             body=("First watch the check run on a weak draft, then run it on a fresh claim of your own. Weak "
                   "draft: 'Healthy food helps students learn.' Run the check step by step. Step 1, question: "
                   "does it answer whether meals should be free for ALL? No, it is on the topic of healthy "
                   "food, so the fix is to land on the exact question. Step 2, side: is there a clear side on "
                   "free-for-all? No, add one. Step 3, reason: is there a because-reason? No, add one. Now you: "
                   "write one fresh claim on the free-meals question, then run the same three checks. For each "
                   "No, use the fix: answer the exact question, pick a side, add 'because ____.' Finish by "
                   "naming which check your claim still needs most.")),
        Slot("INDEPENDENT", "production_frq", "Write one claim that answers the free-meals question",
             ref="", bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("On your own now. The task: argue whether schools should give free meals to all students. "
                   "Write ONE arguable claim sentence. Goal: take a clear side on free-for-all, word it so "
                   "someone could disagree, and add a reason. Before you submit, check your claim: does it "
                   "answer the exact question, could someone disagree, is there a reason? If any answer is no, "
                   "fix it before you submit. Do not drift to the general topic. Scored on Thesis/Purpose.")),
        Slot("TRANSFER", "stimulus_display", "The debate: required community service",
             ref="ACC-W910-FRAME-COMMUNITYSERVICE", bank="community_service",
             body=("Read the short framing of this new debate, then take a side. The exact question is whether "
                   "schools should require community service to graduate. You only need the topic and the two "
                   "sides to write your claim.")),
        Slot("TRANSFER", "production_frq", "Write a claim that answers a NEW question",
             ref="", bank="community_service", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("New topic. The task: argue whether schools should require community service for "
                   "graduation. Write ONE arguable claim sentence that answers that exact question. Goal: a "
                   "clear side on the requirement, worded so someone could disagree, with a reason from the "
                   "framing. Same move as the meals claim, new topic. Do not drift to the general topic of "
                   "volunteering. Scored on Thesis/Purpose.")),
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
