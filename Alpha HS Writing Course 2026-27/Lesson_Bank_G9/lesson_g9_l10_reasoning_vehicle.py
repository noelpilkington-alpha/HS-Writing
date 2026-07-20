"""
lesson_g9_l10_reasoning_vehicle.py  -  G9 KC C.9.03, ARCHETYPE T3: EVIDENCE-INTEGRATION/REASONING (PROVE, paragraph).

G9 course L10. Intro to reasoning: the because/but/so vehicle (W2) - attach a reason (because), a
limit/contrast (but), or a consequence (so) to tie evidence to the claim. Locked L01 template; EVIDENCE-TIER
binds full sources. Taught: SCHOOLLUNCH (full) -> transfer: COMMUNITYSERVICE (full, partitioned). rc.staar,
unit="sentence". because/but/so is taught by FUNCTION (the reasoning job), not as grammar; the connector
mechanic is app-owned + gated. PROVE=established-caveat; no coping-model persona; no source markup; no
prior-work ref; no em dashes. Runs QC on execution.
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
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> claim and evidence sit side by side, no link</span>'
    '<p style="margin:8px 0 0;font-size:15px">Schools should offer free meals. The U.S. Department of '
    'Agriculture reports the program serves billions of lunches.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The claim and the fact are both there, but nothing '
    'says HOW the fact supports the claim. The reader has to connect them alone.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> a because-hinge ties the fact to the claim</span>'
    '<p style="margin:8px 0 0;font-size:15px">Schools should offer free meals to all students, '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">BECAUSE = REASON</span> because, as the U.S. Department of Agriculture reports, the '
      'program already reaches millions who would otherwise go hungry in class.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">The word "because" does the work: it states the '
    'reason the fact supports the claim, so the reader sees the link. That is the reasoning vehicle.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C903-0010", grade="9-10", lesson_type=3,
    unit="G9 U2 - Reasoning (the because/but/so vehicle)",
    title="Link Evidence to Your Claim With Because, But, So",
    target=("Tie your evidence to your claim with a reasoning hinge: because states the reason, but states a "
            "limit or contrast, so states the consequence. Written at the sentence. Trait: Evidence/Development "
            "(reasoning)."),
    acc_tags=["ACC.W.ARG.2", "CCSS.W.9-10.1b"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12",
                "mnemonic_status": "established-caveat", "kc": "C.9.03", "sot": "icm course-G9.md L10",
                "taught_stimulus": "ACC-W910-ARG-LESSON-SCHOOLLUNCH",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-COMMUNITYSERVICE",
                "playbook": "_phase2/playbook_T3_PROVE.md",
                "template": "locked L01 template; EVIDENCE-TIER binds full sources.",
                "council": ("T3/PROVE reasoning intro: introduces W2 the because/but/so vehicle, taught by "
                            "FUNCTION (because=reason, but=limit/contrast, so=consequence), NOT as grammar. "
                            "Connector mechanic app-owned + gated. Linked-vs-unlinked discrimination labeled "
                            "Grade-C; before/after (no coping-model persona); predict-the-fix with reveal.")},
    fade_ledger_moves=["because-but-so-vehicle", "link-evidence-to-claim"],
    slots=[
        Slot("TEACH", "teach_card", "The word that links a fact to your claim",
             body=("Putting a claim and a fact next to each other is not enough; you have to show HOW the fact "
                   "supports the claim. The because/but/so hinge means a small linking word that connects a "
                   "fact to a claim, and each one does a different job. Because states the reason the fact "
                   "supports the claim "
                   "('free meals help, because hunger blocks learning'). But states a limit or a contrast "
                   "('the program is large, but it still misses some families'). So states the consequence "
                   "('hunger blocks learning, so free meals raise focus'). Notice we care about the JOB each "
                   "word does, the reason, the contrast, the consequence, not about naming a grammar part. The "
                   "connecting itself is a sentence skill you already own from earlier courses; here we use it "
                   "to link evidence to a claim. The trap this fixes: a claim and a fact sitting side by side "
                   "with no hinge, so the reader cannot see the connection. Goal today: link one fact to a "
                   "claim with because, but, or so.")),
        Slot("TEACH", "stimulus_display", "Read the source: free school meals",
             ref="ACC-W910-ARG-LESSON-SCHOOLLUNCH", bank="school_lunch",
             body=("Read this source about free school meals. Because your job is to LINK a fact to a claim, "
                   "read the whole thing and pick one fact you could use, then think about the reason it "
                   "supports a claim. The text stays on screen while you work.")),
        Slot("TEACH", "discrimination", "Which sentence links the fact to the claim?",
             ref="", labeled_grade_c=True, bank="school_lunch",
             body=("Sort these before you write (spotting the target before producing it, a Grade-C design bet "
                   "we label as a bet, not a proven ingredient). Both include the same claim and fact. Which "
                   "one LINKS them with a reasoning hinge? "
                   "(A) Schools should offer free meals to all students. The U.S. Department of Agriculture "
                   "reports that the program serves billions of lunches to hungry children across the country "
                   "each year.  "
                   "(B) Schools should offer free meals to all students, because the U.S. Department of "
                   "Agriculture reports the program already reaches millions who would otherwise go hungry in "
                   "class. "
                   "Correct: B. (A) puts the claim and the fact side by side but nothing links them, so the "
                   "reader must connect them alone. (B) uses because to state the reason the fact supports the "
                   "claim, so the link is clear. That is the reasoning vehicle.")),
        Slot("MODEL", "annotated_before_after", "Watch a because-hinge link the fact to the claim",
             bank="school_lunch",
             body=("Here is a claim and a fact getting linked with a because-hinge. Read the BEFORE, then the "
                   "AFTER, and notice the one word that does the linking job." + BEFORE_AFTER_HTML +
                   " The BEFORE leaves the claim and fact unconnected. The AFTER uses because to state why the "
                   "fact supports the claim. Adding the hinge is the move.")),
        Slot("MODEL", "predict_the_fix", "What does this pair of sentences most need?",
             bank="school_lunch",
             body=("Diagnose this draft before the reveal. A student wrote: 'Schools should require community "
                   "service. Many students already volunteer.' Which single move would most improve the "
                   "reasoning? "
                   "(A) add a hinge that states HOW the fact supports the claim, such as a because-reason or a "
                   "so-consequence  "
                   "(B) add a third sentence with one more fact about how many students already volunteer in "
                   "their communities  "
                   "(C) make both sentences longer by adding more descriptive words to the claim and to the "
                   "fact about volunteering  "
                   "(D) move the fact before the claim so the volunteering detail comes first and the claim "
                   "comes second"),
             feedback=("Correct: A. The claim and the fact sit side by side with no link, so the reader cannot "
                       "see why the fact matters to the claim. The fix is a hinge: 'Schools should require "
                       "service, because guided volunteering builds habits students keep,' or 'many already "
                       "volunteer, so a requirement mostly formalizes what is happening.' Another fact (B), "
                       "longer sentences (C), or reordering (D) do not create the missing link.")),
        Slot("SUPPORTED", "production_frq", "Link a fact to a claim with a hinge",
             ref="", bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("Use this frame with a fact from the source: '______ [your claim about free meals], because "
                   "______ [the reason, using a fact from the reading].' Goal: state a claim, then use because "
                   "to state the reason a fact from the source supports it. (You may use but or so instead if "
                   "it fits the reasoning better.) Do not just place the fact next to the claim. Write one "
                   "sentence. Scored on Evidence/Development.")),
        Slot("MODEL", "diagnosis_frq", "Check your sentence: is the fact linked to the claim?",
             ref="", bank="school_lunch", scored=True,
             body=("First watch the check run on a weak draft, then run it on a fresh sentence of your own. "
                   "Weak draft: 'Free meals are important. The program serves billions of lunches.' Run the "
                   "check step by step. Step 1, is there a hinge (because, but, or so)? No, the two ideas just "
                   "sit side by side, so add one. Step 2, does the hinge state HOW the fact supports the "
                   "claim? Not yet, make the because-reason clear. Step 3, is a real fact from the source "
                   "used? Yes. Now you: write one fresh sentence that links a source fact to a claim with a "
                   "hinge, then run the same checks. For each No, use the fix: add because/but/so; make the "
                   "reason clear. Finish by naming which check your sentence still needs most.")),
        Slot("INDEPENDENT", "production_frq", "Link evidence to a claim on your own",
             ref="", bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("On your own now. Write one sentence that makes a claim about free meals and links a fact "
                   "from the source to it with a reasoning hinge. Goal: use because, but, or so to state how "
                   "the fact supports the claim. Before you submit, check your sentence: is there a hinge, does "
                   "it show how the fact supports the claim, is a real fact used? If any answer is no, fix it "
                   "before you submit. Do not just place the fact next to the claim. Scored on "
                   "Evidence/Development.")),
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: required community service",
             ref="ACC-W910-ARG-LESSON-COMMUNITYSERVICE", bank="community_service",
             body=("Read this new source about required community service. Because your job is to LINK a fact "
                   "to a claim, read the whole thing and pick one fact you could use, then think about the "
                   "reason it supports a claim. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Link evidence to a claim on a NEW topic",
             ref="", bank="community_service", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("New topic. Write one sentence that makes a claim about required community service and links "
                   "a fact from the source to it with a because, but, or so hinge. Goal: show how the fact "
                   "supports the claim. Same move as the meals sentence, new topic. Do not just place the fact "
                   "next to the claim. Scored on Evidence/Development.")),
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
