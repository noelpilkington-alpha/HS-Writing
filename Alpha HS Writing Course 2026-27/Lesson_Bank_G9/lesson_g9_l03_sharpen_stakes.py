"""
lesson_g9_l03_sharpen_stakes.py  -  G9 KC C.9.01, ARCHETYPE T2: CLAIM-BUILDING (STAND, ceiling = sentence).

G9 course L03. Independent rung: sharpen a vague claim + reach the so-what stakes (cS1 introduced here).
REVISED 2026-07-12 to the locked L01 template. Taught frame = FRAME-COMMUNITYSERVICE; transfer frame =
FRAME-PHONEBAN (bank-partitioned). rc.staar, unit="sentence". STAND labeled proposal; mechanics gated; no
coping-model persona; no source markup; no prior-work reference; no em dashes. Runs QC on execution.
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
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> vague, and no stakes</span>'
    '<p style="margin:8px 0 0;font-size:15px">"Community service is a good thing for students."</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">It names no specific position (how much? required '
    'or not?), gives no reason, and never says why it matters. A reader cannot tell what is being argued.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> specific, and it reaches the stakes</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">SHARP SIDE</span> Schools should require forty hours of community service to graduate, '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">REASON</span> because guided service builds civic habits, '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">SO WHAT</span> which matters because those habits shape whether teens stay engaged '
      'citizens as adults.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">It names a specific amount, gives a reason, and '
    'says why it matters. The stakes are the lift.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C901-0003", grade="9-10", lesson_type=2,
    unit="G9 U1 - Claim/controlling-idea + evidence (sharpen + stakes)",
    title="Make the Claim Sharp and Say Why It Matters",
    target=("Take a vague claim, sharpen it into a specific position, and reach the so-what: say why it "
            "matters. Written at the sentence. Trait: Thesis/Purpose."),
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.5", "CCSS.W.9-10.1a"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-12",
                "mnemonic_status": "proposal", "kc": "C.9.01", "sot": "icm course-G9.md L03",
                "taught_stimulus": "ACC-W910-FRAME-COMMUNITYSERVICE",
                "transfer_stimulus": "ACC-W910-FRAME-PHONEBAN",
                "playbook": "_phase2/playbook_T2_STAND.md",
                "revision_note": "Locked L01 template: student register, one teach concept, visual before/after, one discrimination, bound issue_frame.",
                "council": "T2/STAND independent rung: introduces cS1 so-what/stakes (stakes-reached vs stakes-absent)."},
    fade_ledger_moves=["sharpen-vague-to-specific", "so-what-stakes"],
    slots=[
        Slot("TEACH", "teach_card", "Make it specific, then say why it matters",
             body=("You can already take a side and give a reason. Two moves turn an okay claim into a strong "
                   "one. First, be specific. A vague claim names no amount, no who, no what, so a reader cannot "
                   "tell exactly what you are arguing: 'community service is good' is vague; 'schools should "
                   "require forty hours of community service to graduate' is specific. Second, reach the "
                   "so-what: after your claim, say why it matters. Ask yourself, if a reader agreed with me, why "
                   "would that be worth caring about? A claim that names why it matters reaches the top of the "
                   "scoring; a claim that stops at the position stays in the middle. The scoring calls your "
                   "governing claim the thesis, which is a name for the arguable claim your response defends. "
                   "Today you will sharpen a vague claim and add its stakes.")),
        Slot("TEACH", "stimulus_display", "The debate: required community service",
             ref="ACC-W910-FRAME-COMMUNITYSERVICE", bank="community_service",
             body=("Read the short framing of the debate, then take a side. You only need the topic and the two "
                   "sides to write your claim. This time, make your side specific and say why it matters.")),
        Slot("TEACH", "discrimination", "Which claim is specific AND reaches the stakes?",
             ref="", labeled_grade_c=True, bank="community_service",
             body=("Sort these before you write (spotting the target before producing it, a Grade-C design bet "
                   "we label as a bet, not a proven ingredient). Which sentence is a specific claim that also "
                   "says why it matters? "
                   "(A) Community service is a genuinely important and worthwhile thing for young people, and most everyone would agree it is good and valuable and something students really ought to care much more about.  "
                   "(B) Schools really should make all of their students go out and do at least some kind of community service at some point before they are finally allowed to finish up and graduate from high school.  "
                   "(C) Schools should require forty hours of community service to graduate, because guided "
                   "service builds civic habits, which matters because teens who serve tend to stay engaged "
                   "citizens as adults. "
                   "Correct: C. (A) is vague with no reason. (B) takes a side but is still vague (how much? "
                   "what kind?) and names no stakes. Only (C) is specific, gives a reason, and reaches the "
                   "so-what.")),
        Slot("MODEL", "annotated_before_after", "Watch a vague claim get sharp and reach its stakes",
             bank="community_service",
             body=("Here is a vague claim being rebuilt. Read the BEFORE, then the AFTER, and notice the three "
                   "things that were added: a specific side, a reason, and a so-what." + BEFORE_AFTER_HTML +
                   " The BEFORE could mean anything. The AFTER names a specific amount, gives a reason, and "
                   "says why it matters. Sharpening and adding the stakes is the move.")),
        Slot("MODEL", "predict_the_fix", "What does this vague claim most need?",
             bank="community_service",
             body=("Diagnose this draft before the reveal. The student wrote: 'Doing community service is good "
                   "for young people.' Which single move would most improve it as a claim? "
                   "(A) make it specific and add why it matters, a reason and the stakes  "
                   "(B) add the fact that many students already volunteer at places in town  "
                   "(C) list the kinds of service students could do, like tutoring and cleanups  "
                   "(D) make it sound more formal by swapping in bigger, more academic words"),
             feedback=("Correct: A. The draft is vague, takes no specific side, gives no reason, and names no "
                       "stakes, so it sits at the bottom. The fix is to sharpen and add the so-what: a specific "
                       "side ('require forty hours ...'), a reason, and a which-matters beat. A fact about "
                       "volunteering (B), a list of service types (C), or a formal tone (D) never turn a vague "
                       "sentence into a specific claim that reaches its stakes.")),
        Slot("SUPPORTED", "production_frq", "Sharpen the claim, add a reason and the stakes",
             ref="", bank="community_service", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("Finish this claim, making it specific: 'Schools should ______ [a SPECIFIC side, name an "
                   "amount or kind], because ______ [a reason], which matters because ______ [the stakes].' "
                   "Goal: a specific side, a reason, and a so-what. Do not leave it vague ('service is good'). "
                   "Write one sentence. Scored on Thesis/Purpose.")),
        Slot("MODEL", "diagnosis_frq", "Check your claim: specific, and does it reach the stakes?",
             ref="", bank="community_service", scored=True,
             body=("First watch the check run on a weak draft, then run it on a fresh claim of your own. Weak "
                   "draft: 'Community service helps students grow.' Run the check step by step. Step 1, "
                   "specific: is the side specific (amount, kind)? No, 'helps students grow' is vague, so name "
                   "a specific position. Step 2, reason: is there a because-reason? No, add one. Step 3, "
                   "so-what: does it say why it matters? No, add a which-matters beat. Now you: write one "
                   "fresh, specific claim on the community-service question, then run the same three checks. "
                   "For each No, use the fix: name a specific amount or kind; add 'because ____'; add 'which "
                   "matters because ____.' Finish by naming which check your claim still needs most.")),
        Slot("INDEPENDENT", "production_frq", "Write one sharp claim with stakes on community service",
             ref="", bank="community_service", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("On your own now. The task: argue whether schools should require community service for "
                   "graduation. Write ONE arguable claim that is SPECIFIC and reaches its stakes. Goal: a "
                   "specific side (name an amount or kind), worded so someone could disagree, a reason, and a "
                   "so-what saying why it matters. Before you submit, check your claim: is it specific, could "
                   "someone disagree, is there a reason, does it say why it matters? If any answer is no, fix "
                   "it before you submit. Scored on Thesis/Purpose.")),
        Slot("TRANSFER", "stimulus_display", "The debate: phones in school",
             ref="ACC-W910-FRAME-PHONEBAN", bank="phone_ban",
             body=("Read the short framing of this new debate, then take a side. You only need the topic and "
                   "the two sides. Make your side specific and say why it matters.")),
        Slot("TRANSFER", "production_frq", "Write a sharp claim with stakes on a NEW topic",
             ref="", bank="phone_ban", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("New topic. The task: argue whether schools should ban phones for the whole day. Write ONE "
                   "arguable claim that is specific and reaches its stakes. Goal: a specific side, a reason, "
                   "and a so-what saying why it matters. Same move as the service claim, new topic. Do not "
                   "leave it vague. Scored on Thesis/Purpose.")),
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
