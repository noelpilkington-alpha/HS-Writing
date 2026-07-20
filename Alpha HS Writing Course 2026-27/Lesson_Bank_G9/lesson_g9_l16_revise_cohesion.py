"""
lesson_g9_l16_revise_cohesion.py  -  G9 KC C.9.06, ARCHETYPE T5: RUBRIC-REVISION (CHECK, ceiling paragraph).

G9 course L16 (Unit 3 Cohesion, guided CHECK). Revise a PROVIDED choppy paragraph for cohesion, combining both
cohesion moves: transition-by-function (oC1) + referential cohesion (oC2). Locked L01 template. REVISION-TIER:
the material is the PROVIDED paragraph (inline); binds a lightweight issue_frame for topic context. Taught:
FRAME-SCHOOLLUNCH -> transfer: FRAME-COMMUNITYSERVICE (bank-partitioned). rc.staar, unit="paragraph".
CHECK=proposal; calibration self_score precedes graded reveal. No coping-model persona; no source markup; no
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
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> choppy: filler links and a vague reference</span>'
    '<p style="margin:8px 0 0;font-size:15px">Free meals help students focus. Also, they remove a daily worry '
    'for families. Also, hungry students struggle in class. This is why many schools support the idea.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The links are all "also," so the relationships are '
    'hidden, and the final "this" points to no one clear idea. The paragraph reads as a list, not a connected '
    'point.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> functional transitions + an anchored reference</span>'
    '<p style="margin:8px 0 0;font-size:15px">Free meals help students focus. '
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">ADD</span> In addition, they remove a daily worry for families. '
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">CAUSE</span> Because hungry students struggle in class, the payoff is real. '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">ANCHORED</span> This combination of benefits is why many schools support the idea.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Now each transition names its relationship (add, '
    'cause), and "this combination of benefits" anchors the final reference. The paragraph connects.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C906-0016", grade="9-10", lesson_type=5,
    unit="G9 U3 - Cohesion (revise a paragraph for cohesion)",
    title="Revise a Choppy Paragraph Into a Connected One",
    target=("Revise a provided paragraph for cohesion: replace filler transitions with ones that name the real "
            "relationship, and anchor any vague reference. Written at the paragraph. Trait: Organization."),
    acc_tags=["ACC.W.ARG.3", "ACC.W.INFO.3", "CCSS.W.9-10.1c", "CCSS.W.9-10.2c"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12",
                "mnemonic_status": "proposal", "kc": "C.9.06", "sot": "icm course-G9.md L16",
                "taught_stimulus": "ACC-W910-FRAME-SCHOOLLUNCH",
                "transfer_stimulus": "ACC-W910-FRAME-COMMUNITYSERVICE",
                "playbook": "_phase2/playbook_T5_CHECK.md",
                "template": "locked L01 template; REVISION-TIER binds a lightweight issue_frame (material is the provided paragraph, inline).",
                "council": ("T5/CHECK cohesion capstone: revise a provided paragraph, combining oC1 transition-"
                            "by-function + oC2 referential cohesion. Calibration self_score precedes reveal. "
                            "cohered-vs-choppy discrimination labeled Grade-C. CHECK=proposal.")},
    fade_ledger_moves=["revise-for-cohesion", "combine-transition-and-reference-fixes"],
    slots=[
        Slot("TEACH", "teach_card", "Two cohesion fixes, one revision",
             body=("You have learned the two moves that connect a paragraph: transition by function (pick the "
                   "connector that names the real relationship, not filler like 'also' or 'then') and "
                   "referential cohesion (anchor a vague 'this' or 'it' by naming what it points to). Today you "
                   "put both to work at once, revising a whole paragraph. A choppy paragraph usually has both "
                   "problems together: every sentence linked with 'also,' and a floating 'this' at the end. "
                   "Revising for cohesion means walking through the paragraph and, at each link, naming the "
                   "real relationship and choosing the signpost that fits, then anchoring any vague reference. "
                   "You are not adding new ideas; you are connecting the ones already there. The trap is "
                   "leaving a paragraph as a list of sentences that never signal how they relate. Goal today: "
                   "revise a provided paragraph so it reads as one connected point.")),
        Slot("TEACH", "teach_card", "How the check works: read, name, fix, confirm",
             body=("Run this routine on the paragraph. First, READ it and mark where it feels choppy. Second, "
                   "at each transition, NAME the real relationship (add, contrast, cause, sequence, conclude) "
                   "and pick a signpost that fits. Third, FIND any vague 'this/it/that' and anchor it with a "
                   "noun. Fourth, CONFIRM by rereading: does each link now name a relationship, and does every "
                   "reference point to one clear thing? Because writers tend to think their own paragraph "
                   "already flows, predicting a score before you see the reveal trains you to catch the choppy "
                   "spots you would otherwise skip past.")),
        Slot("TEACH", "stimulus_display", "The topic: free school meals",
             ref="ACC-W910-FRAME-SCHOOLLUNCH", bank="school_lunch",
             body=("The paragraph you will revise is about free school meals. Read this short orientation so "
                   "the topic is familiar. You are not writing about meals from scratch here; you are "
                   "connecting a paragraph that is given to you.")),
        Slot("TEACH", "discrimination", "Which paragraph is cohered, and which is choppy?",
             ref="", labeled_grade_c=True, bank="school_lunch",
             body=("Sort these before you revise (spotting the target first, a Grade-C design bet we label as a "
                   "bet, not a proven ingredient). Both make the same points. Which one is COHERED (functional "
                   "transitions, anchored reference)? "
                   "(A) Free meals cut hunger for students. Also, they save families money every week. Also, they help students focus in class. This is something schools care about.  "
                   "(B) Free meals cut hunger. In addition, they save families money. As a result, students "
                   "focus better in class. This mix of benefits is why schools support them. "
                   "Correct: B. (A) links everything with 'also' and ends on a vague 'this.' (B) names the "
                   "relationships (in addition, as a result) and anchors the reference ('this mix of "
                   "benefits'), so it connects. Cohered means the connections are visible.")),
        Slot("MODEL", "annotated_before_after", "Watch a choppy paragraph get connected",
             bank="school_lunch",
             body=("Here is a choppy paragraph being revised for cohesion, fixing both the transitions and the "
                   "vague reference. Read the BEFORE, then the AFTER, and notice the filler 'also's become "
                   "functional signposts and the final 'this' gets anchored." + BEFORE_AFTER_HTML +
                   " The BEFORE reads as a list. The AFTER names each relationship and anchors the reference. "
                   "Doing both fixes together is the revision.")),
        Slot("MODEL", "predict_the_fix", "What does this choppy paragraph most need?",
             bank="school_lunch",
             body=("Diagnose before the reveal. A paragraph reads: 'Free meals reduce stress at home. Also, "
                   "kids eat better. Also, some families still feel judged asking for help. This is a concern.' "
                   "Which single set of changes would most improve its cohesion? "
                   "(A) replace the filler 'also's with signposts that fit (add, then contrast for the "
                   "judged-feeling idea) and anchor the final 'this'  "
                   "(B) add another benefit of free meals, such as better attendance, so the paragraph "
                   "makes a fuller and more convincing case for the program  "
                   "(C) make every sentence longer and more detailed, since a choppy paragraph is really "
                   "just one built from sentences that feel too short and abrupt  "
                   "(D) move the last sentence to the front so the paragraph opens with its main point "
                   "and the ideas that follow seem better organized behind it"),
             feedback=("Correct: A. The paragraph hides its relationships behind 'also' (one of the ideas is "
                       "actually a contrast, not an addition) and ends on a floating 'this.' The cohesion fix "
                       "is to name each relationship (in addition ... however ...) and anchor the reference "
                       "('this worry about stigma'). Another benefit (B), longer sentences (C), or reordering "
                       "(D) do not connect the existing ideas.")),
        Slot("SUPPORTED", "self_score", "Score a revision, then see the real score",
             ref="", bank="school_lunch",
             body=("Predict, then reveal. A student revised the choppy paragraph to: 'Free meals cut hunger. "
                   "Also, they save money. Also, kids focus. This helps everyone.' On a 2-point cohesion scale "
                   "(2 = transitions name relationships AND references are anchored, 1 = still choppy), what "
                   "score would you give? Commit, then read the reveal. Reveal: this scores 1. The student "
                   "changed the ideas' wording but kept the filler 'also's and the vague 'this,' so the "
                   "cohesion problems remain. A 2 would name the relationships and anchor the reference. If you "
                   "predicted 2, notice how easy it is to think a paragraph flows when it does not.")),
        Slot("SUPPORTED", "production_frq", "Revise the provided paragraph for cohesion",
             ref="", bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=("Revise this provided paragraph for cohesion: 'Free meals help students focus. Also, they "
                   "remove a worry for families. Also, hungry students struggle in class. This is why schools "
                   "support the idea.' Rewrite it so each transition names the real relationship and the final "
                   "reference is anchored. Keep the ideas; change only the transitions, the reference, and "
                   "small wording needed to fit them. Scored on Organization.")),
        Slot("MODEL", "diagnosis_frq", "Check a fresh paragraph for cohesion",
             ref="", bank="school_lunch", scored=True,
             body=("First watch the check run on a provided draft, then run it on a fresh paragraph of your "
                   "own. Provided draft: 'Free meals feed more kids. Also, they cost the district money. This "
                   "is debated.' Run the check step by step. Step 1, transitions: does each name a real "
                   "relationship? No, the second idea is a contrast (feeds kids BUT costs money), so 'also' is "
                   "wrong. Step 2, references: does 'this' point to one clear thing? No, anchor it ('this "
                   "tradeoff'). Now you: write a fresh two-or-three-sentence paragraph on free meals, then run "
                   "the same check, functional transitions and an anchored reference? Fix any that fail. "
                   "Finish by naming each relationship your transitions signal.")),
        Slot("INDEPENDENT", "production_frq", "Revise a provided paragraph on your own",
             ref="", bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=("On your own now. Revise this provided paragraph for cohesion: 'Free meals reach every "
                   "student. Also, no child is singled out. Also, some taxpayers question the cost. This shapes "
                   "the debate.' Rewrite it so each transition names the real relationship (watch for the "
                   "contrast) and the final reference is anchored. Before you submit, check the paragraph: does "
                   "each transition name a relationship, does every reference point clearly? Fix any that fail "
                   "before you submit. Scored on Organization.")),
        Slot("TRANSFER", "stimulus_display", "The topic: required community service",
             ref="ACC-W910-FRAME-COMMUNITYSERVICE", bank="community_service",
             body=("The next paragraph to revise is about required community service. Read this short "
                   "orientation so the topic is familiar. Again, you are connecting a provided paragraph, not "
                   "writing from scratch.")),
        Slot("TRANSFER", "production_frq", "Revise a provided paragraph on a NEW topic",
             ref="", bank="community_service", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=("New topic. Revise this provided paragraph for cohesion: 'Required service teaches "
                   "responsibility. Also, it connects students to their town. Also, some students already "
                   "volunteer and resent a rule. This is the tension.' Rewrite it so each transition names the "
                   "real relationship (watch for the contrast) and the final reference is anchored. Same "
                   "revision move as the meals paragraph, new topic. Scored on Organization.")),
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
