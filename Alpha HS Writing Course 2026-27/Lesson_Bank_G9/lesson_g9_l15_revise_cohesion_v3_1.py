"""
lesson_g9_l16_revise_cohesion_v3_1.py  -  G9 KC C.9.06, ARCHETYPE T5: RUBRIC-REVISION (CHECK, paragraph). V3.1.

G9 L16, rebuilt to the v3.1 build spec (icm/_config/v3_1-lesson-build-spec.md), from lesson_g9_l16_revise_cohesion.py.
Teaching point (KEPT): revise a PROVIDED choppy paragraph for cohesion - replace filler transitions ('also') with
ones that name the real relationship, and anchor any vague reference. KC C.9.06. This is a REVISION lesson on a
PROVIDED draft, so it is stateless-safe (no look-back at the student's own prior work). Bound stimuli KEPT:
FRAME-SCHOOLLUNCH (taught) -> FRAME-COMMUNITYSERVICE (transfer, bank-partitioned). rc.staar, unit="paragraph".

V3.1 changes over the current L16 (both prior failures fixed):
  1. TEACH is now ONE idea, hammered: a teal ONE_IDEA callout + the two cohesion moves as a real <ul> list (the
     old two prose teach cards were walls of text -> format_fidelity failed). The read-name-fix-confirm routine
     moved to the REMEMBER check tool at the model card (point of first use), not cold up front (KH load).
  2. NO leaked internal labels: the old discrimination prose said "a Grade-C design bet we label as a bet"
     (leaked_internal_label failed). Removed; the discrimination now uses explicit choices=[{id,text,correct,why}]
     with the correct option NOT the lone-longest (homogeneous option length; Haladyna).
  3. FRQ + diagnosis bodies are built with frq_prompt / setapart / checklist (no "Step 1/2" prose, no "Scored on"
     chrome). The provided draft to revise sits in a setapart(...) block each time.
  4. Coping-model before/after kept (literal BEFORE + AFTER inline). Own words, no fabricated figures, no em dashes.
Passes all 23 lesson_contract gates + gated_reading render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A connected paragraph makes two moves: at each link it '
'<strong>names the real relationship</strong> (not filler like "also"), and it '
'<strong>anchors any vague reference</strong> ("this", "it") to a clear noun.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: read, name, fix, confirm</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Run this routine on any paragraph before you submit it:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0"><strong>Read</strong> it and note where it feels choppy.</li>'
'<li style="margin:2px 0"><strong>Name</strong> the real relationship at each link (add, contrast, cause, sequence, conclude) and pick a signpost that fits.</li>'
'<li style="margin:2px 0"><strong>Fix</strong> any vague "this", "it", or "that" by anchoring it to a noun.</li>'
'<li style="margin:2px 0"><strong>Confirm</strong> by rereading: does each link name a relationship, and does every reference point to one clear thing?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">Writers tend to think their own paragraph already flows, so run the check even when it feels fine.</div></div>')

# coping-model before/after panel: a choppy paragraph revised, with functional transitions + an anchored reference.
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
      'font-weight:700">CAUSE</span> After all, hungry students struggle in class. '
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
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-14",
                "mnemonic_status": "proposal", "kc": "C.9.06",
                "sot": "icm course-G9.md L16; KC_Map_and_Unit_Arch_G9-12.md (G9 U3)",
                "taught_stimulus": "ACC-W910-FRAME-SCHOOLLUNCH",
                "transfer_stimulus": "ACC-W910-FRAME-COMMUNITYSERVICE",
                "one_idea": "A connected paragraph names the real relationship at each link and anchors vague references.",
                "one_reminder": "Read, name (the relationship), fix (the vague reference), confirm.",
                "version_note": ("V3.1 rebuild of lesson_g9_l16_revise_cohesion.py to the v3.1 build spec. Fixed the "
                                 "two prior failures: (a) TEACH is now one hammered idea (ONE_IDEA callout + the two "
                                 "moves as a <ul>), the read-name-fix-confirm routine moved to the REMEMBER check "
                                 "tool at point of first use (was two wall-of-text teach cards -> format_fidelity); "
                                 "(b) discrimination uses explicit choices with no leaked internal labels (was "
                                 "'a Grade-C design bet we label as a bet' -> leaked_internal_label). FRQ + "
                                 "diagnosis built with frq_prompt/setapart/checklist (no Step-N prose, no 'Scored "
                                 "on' chrome). REVISION-TIER: material is the PROVIDED paragraph, inline; binds a "
                                 "lightweight issue_frame for topic context. Kept bound stimuli + unit='paragraph'."),
                "review_provenance": "built to the G9 L01 v3.1 pattern (icm/_config/v3_1-lesson-build-spec.md)."},
    fade_ledger_moves=["revise-for-cohesion", "combine-transition-and-reference-fixes"],
    slots=[
        # ===== TEACH: ONE idea, hammered (callout + the two moves as a list; routine moved to the model card) =====
        Slot("TEACH", "teach_card", "The one idea: name the relationship, anchor the reference",
             body=(ONE_IDEA +
                   "You have practiced each cohesion move on its own. Revising a paragraph puts both to work at "
                   "once. A choppy paragraph usually has both problems together, so watch for both:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Filler links</strong>: every sentence joined with \"also\" "
                   "or \"then,\" so the reader cannot tell whether an idea is an addition, a cause, or a "
                   "contrast.</li>"
                   "<li style=\"margin:4px 0\"><strong>A floating reference</strong>: a vague \"this\" or \"it\" "
                   "at the end that points to no single, clear idea.</li></ul>"
                   "You are not adding new ideas; you are connecting the ones already there. Leave a paragraph as "
                   "a list of sentences that never signal how they relate, and it never reads as one point.")),
        # tag="buy_in": this is a get-familiar topic-orientation read (the paragraph you revise is about this
        # topic), not a counted teach segment, so it does not tighten the checking_revision cadence ceiling.
        Slot("TEACH", "stimulus_display", "The topic: free school meals",
             ref="ACC-W910-FRAME-SCHOOLLUNCH", bank="school_lunch", tag="buy_in",
             body=("The paragraph you will revise is about free school meals. Read this short orientation so the "
                   "topic is familiar. You are not writing about meals from scratch here; you are connecting a "
                   "paragraph that is given to you.")),

        # ===== MODEL (before the quiz): before/after worked example + the check tool at point of first use =====
        Slot("MODEL", "annotated_before_after", "Watch a choppy paragraph get connected",
             bank="school_lunch",
             body=("Here is the skill in action. Read the BEFORE, then the AFTER, and notice the filler \"also\"s "
                   "become functional signposts and the final \"this\" gets anchored." + BEFORE_AFTER_HTML +
                   " The BEFORE reads as a list; the AFTER names each relationship and anchors the reference. "
                   "Doing both fixes together is the revision. " + REMEMBER +
                   "When you revise a paragraph, walk it with this routine, then reread once more.")),
        Slot("MODEL", "discrimination", "Which paragraph is the cohered one?",
             ref="", labeled_grade_c=True, bank="school_lunch",
             body=("Spot the target before you revise. All three make the same points, but only one is cohered, "
                   "with transitions that name each relationship and a reference that is anchored. Which one is "
                   "it? "
                   "(A) Free meals cut hunger for students. Also, they save families real money every single "
                   "week. Also, they help students focus far better all through the whole school day. This is "
                   "truly something that schools everywhere care very deeply about.  "
                   "(B) Free meals cut hunger. In addition, they save families money. As a result, students "
                   "focus better in class. This mix of benefits is why schools support them.  "
                   "(C) Free meals cut hunger. Also, they save money. Also, students focus. This matters to "
                   "schools.  "
                   "(D) Free meals cut hunger. In addition, they save families money. As a result, students "
                   "focus better in class. This is why schools support them. "
                   "Correct: B."),
             choices=[
                 {"id": "A", "text": "Free meals cut hunger for students. Also, they save families real money every single week. Also, they help students focus far better all through the whole school day. This is truly something that schools everywhere care very deeply about.",
                  "correct": False,
                  "why": "Every link is 'also,' so the relationships stay hidden, and the closing 'this' floats with no anchor. Padding the sentences with extra words does not connect them."},
                 {"id": "B", "text": "Free meals cut hunger. In addition, they save families money. As a result, students focus better in class. This mix of benefits is why schools support them.",
                  "correct": True,
                  "why": "Correct. Each transition names its relationship ('in addition' for an addition, 'as a result' for a cause), and 'this mix of benefits' anchors the final reference, so the paragraph connects."},
                 {"id": "C", "text": "Free meals cut hunger. Also, they save money. Also, students focus. This matters to schools.",
                  "correct": False,
                  "why": "Short does not mean cohered. The links are still filler 'also's and the final 'this' points to no one clear idea, so the ideas never signal how they relate."},
                 {"id": "D", "text": "Free meals cut hunger. In addition, they save families money. As a result, students focus better in class. This is why schools support them.",
                  "correct": False,
                  "why": "This one fixes only half the job. The transitions now name their relationships, but the closing 'This' still floats with no anchor, so one of the two cohesion moves is left undone."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this choppy paragraph most need?",
             bank="school_lunch",
             body=("Diagnose before the reveal. A paragraph reads: 'Free meals reduce stress at home. Also, kids "
                   "eat better. Also, some families still feel judged asking for help. This is a concern.' Which "
                   "single set of changes would most improve its cohesion? "
                   "(A) replace the filler 'also's with signposts that fit (add, then contrast for the "
                   "judged-feeling idea) and anchor the final 'this'  "
                   "(B) add another benefit of free meals, such as better attendance, so the paragraph makes a "
                   "fuller and more convincing case for the program  "
                   "(C) make every sentence longer and more detailed, since a choppy paragraph is really just "
                   "one built from sentences that feel too short and abrupt  "
                   "(D) move the last sentence to the front so the paragraph opens with its main point and the "
                   "ideas that follow seem better organized behind it"),
             feedback=("Correct: A. The paragraph hides its relationships behind 'also' (one of the ideas is "
                       "actually a contrast, not an addition) and ends on a floating 'this.' The cohesion fix is "
                       "to name each relationship (in addition ... however ...) and anchor the reference ('this "
                       "worry about stigma'). Another benefit (B), longer sentences (C), or reordering (D) do not "
                       "connect the existing ideas.")),

        # ===== SUPPORTED: scaffolded revision of a PROVIDED paragraph (draft in a set-apart block + a checklist) =====
        Slot("SUPPORTED", "production_frq", "Revise the provided paragraph for cohesion",
             ref="", bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="revision",
             body=frq_prompt(
                 intro="Revise the paragraph below so it reads as one connected point. Keep the ideas; change "
                       "only the transitions, the reference, and small wording needed to fit them.",
                 setapart_block=setapart("Paragraph to revise:",
                                         "Free meals reduce stress for parents. Also, students eat healthier lunches. Also, no child is singled out for needing help. This is the case supporters make."),
                 checklist_block=checklist(title="Use both moves:", rows=[
                     "At each link, name the real relationship and pick a signpost that fits (add, cause, contrast, conclude).",
                     "Anchor the final 'this' to a noun so it points to one clear idea.",
                 ]),
                 closer="Then reread: does each transition name a relationship, and does every reference point "
                        "clearly?")),
        # DIAGNOSIS: watch the check run on a provided draft, then run it on a fresh paragraph (stateless-safe;
        # the material is provided, so no look-back at the student's own prior submission).
        Slot("MODEL", "diagnosis_frq", "Check and fix a weak paragraph for cohesion",
             ref="", bank="school_lunch", scored=True,
             body=frq_prompt(
                 intro="Run the check on this weak paragraph, then rewrite it so it connects.",
                 setapart_block=setapart("Weak paragraph to fix:",
                                         "Free meals feed more kids. Also, they cost the district money. This is debated.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Does each transition name a real relationship?", "No. The second idea is a contrast (feeds kids but costs money), so 'also' hides it. Name it with 'however' or 'but'."),
                     ("Does every reference point to one clear thing?", "No. The final 'this' floats. Anchor it, such as 'this tradeoff'."),
                 ]),
                 closer="Now rewrite it as one connected paragraph: each transition naming the real relationship "
                        "(watch the contrast) and the final reference anchored. Then name which relationship each "
                        "transition signals.")),

        # ===== INDEPENDENT: revise a PROVIDED paragraph with no checklist scaffold (still on the taught topic) =====
        Slot("INDEPENDENT", "production_frq", "Revise a provided paragraph on your own",
             ref="", bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="revision",
             body=frq_prompt(
                 intro="On your own now, no checklist. Revise the paragraph below for cohesion, and watch for one "
                       "link that is really a contrast.",
                 setapart_block=setapart("Paragraph to revise:",
                                         "Free meals reach every student. Also, no child is singled out. Also, some taxpayers question the cost. This shapes the debate."),
                 closer="Rewrite it so each transition names the real relationship and the final reference is "
                        "anchored. Connecting a paragraph is the real move, and you are ready to do it cold. Before "
                        "you submit, check: does each transition name a relationship, does every reference point "
                        "clearly?")),

        # ===== TRANSFER: same revision move, a NEW topic (community service), bank-partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "The topic: required community service",
             ref="ACC-W910-FRAME-COMMUNITYSERVICE", bank="community_service",
             body=("The next paragraph to revise is about required community service. Read this short "
                   "orientation so the topic is familiar. Again, you are connecting a provided paragraph, not "
                   "writing from scratch.")),
        Slot("TRANSFER", "production_frq", "Revise a provided paragraph on a NEW topic",
             ref="", bank="community_service", rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="revision",
             body=frq_prompt(
                 intro="New topic. Revise the paragraph below for cohesion, the same move as the meals "
                       "paragraphs.",
                 setapart_block=setapart("Paragraph to revise:",
                                         "Required service teaches responsibility. Also, it connects students to their town. Also, some students already volunteer and resent a rule. This is the tension."),
                 closer="Rewrite it so each transition names the real relationship (watch for the contrast) and "
                        "the final reference is anchored. Run the read, name, fix, confirm check before you "
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
