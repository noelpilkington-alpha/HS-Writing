"""
lesson_g9_l15_referential_cohesion_v3_1.py  -  G9 KC C.9.06, ARCHETYPE T6: EDITING-IN-CONTEXT (SPOT, ceiling
sentence). V3.1 rebuild of lesson_g9_l15_referential_cohesion.py to the v3.1 lesson build spec
(icm/_config/v3_1-lesson-build-spec.md), which cleared all 23 lesson_contract gates + the Fable-5 reviewer.

TEACHING POINT (KEEP): fix a vague back-reference. When a sentence starts with a naked "this," "that," or "it,"
anchor it by naming what it points to, so the sentences connect cleanly. KC C.9.06. Bound stimuli unchanged:
taught FRAME-MIGRATION -> transfer FRAME-VOLCANOES (bank-partitioned).

V3.1 changes from the current L15 (design pattern, not the teaching point):
  1. TEACH split to ONE idea in a callout + the vague/anchored contrast as a real LIST (was a 148-word wall of
     text that tripped format_fidelity).
  2. MODEL rebuilt as a coping-model think-aloud (draft -> run the check -> catch the vague "this" -> revise),
     still with a literal BEFORE and AFTER; the reusable 3-question check tool is folded in at point of first use.
  3. DISCRIMINATION uses explicit choices=[{id,text,correct,why}]; the "Grade-C design bet" jargon that leaked
     into the student prompt is gone (labeled_grade_c stays True in code only). Construct confound broken: a
     distractor also adds a noun after "this" ("This problem"), so the invariant is "names the real referent,"
     not "any noun follows this." Correct option is not the lone longest.
  4. FRQ + diagnosis bodies built with frq_prompt / setapart / checklist (no "Step 1/Step 2" prose -> kills the
     render double-numbering fail; no "Scored on ..." chrome).
  5. INDEPENDENT names the standard out loud (Yeager). TRANSFER stays a partitioned new topic (volcanoes).

id, lesson_type=6, and mnemonic_status="proposal" are the current L15's values, unchanged; every production_frq
unit="sentence" (T6 ceiling). Own words, no fabricated figures, no em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">When a sentence starts with a bare '
'<strong>this</strong>, <strong>that</strong>, or <strong>it</strong>, name what it points to. A reference the '
'reader has to guess about breaks the link between your sentences.</div></div>')

# reusable job-aid, folded in at point of first use (the decompose/model card), not cold in step 1 (KH load).
REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit any sentence that starts with this, that, or it, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Is there a back-reference (this, that, or it)?</li>'
'<li style="margin:2px 0">Does it point to one clear thing?</li>'
'<li style="margin:2px 0">If not, add a noun that names it.</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If it could point to two different things, it is not anchored yet.</div></div>')

# coping-model think-aloud: a WRITTEN editing process (draft -> run the check -> catch the vague this -> revise),
# then the endpoints. Contains a literal BEFORE and AFTER (content_depth). No named near-peer (Timeback rule).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer editing one sentence, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First draft:</strong> "Some birds fly thousands of miles, and the weather '
    'can turn harsh along the way. This makes migration dangerous." Run the check: does "this" point to one clear '
    'thing? No. It could mean the long distance, the harsh weather, or both. Anchor it.</p>'
    '<p style="margin:0 0 8px"><strong>Second draft:</strong> "This weather makes migration dangerous." Better, I '
    'added a noun. But is it the thing I meant? Not quite, the long distance matters too. Name both.</p>'
    '<p style="margin:0"><strong>Final:</strong> "This combination of distance and bad weather makes migration '
    'dangerous." Now the reference names the exact thing it points to. Anchored.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "...along the way. This makes migration dangerous." (this points '
    'to nothing clear)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "...along the way. This combination of distance and bad weather '
    'makes migration dangerous." (the reference names what it points to)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C906-0015", grade="9-10", lesson_type=6,
    unit="G9 U3 - Cohesion (referential cohesion)",
    title="Make Every This and It Point Clearly",
    target=("Fix a vague back-reference: when a sentence starts with a naked 'this,' 'that,' or 'it,' anchor it "
            "by naming what it points to, so sentences connect cleanly. Written at the sentence. Trait: "
            "Organization/Conventions."),
    acc_tags=["ACC.W.INFO.3", "CCSS.W.9-10.2c"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.9.06", "sot": "icm course-G9.md L15",
                "taught_stimulus": "ACC-W910-FRAME-MIGRATION",
                "transfer_stimulus": "ACC-W910-FRAME-VOLCANOES",
                "playbook": "_phase2/playbook_T6_SPOT.md",
                "template": "v3.1 lesson build spec; COHESION-TIER binds a lightweight issue_frame (material is a provided sentence, inline).",
                "one_idea": "A bare this/that/it must name what it points to.",
                "one_reminder": "3-question check: back-reference? one clear thing? if not, add a naming noun.",
                "version_note": ("V3.1 rebuild of L15 to the v3.1 build spec: TEACH split into one-idea callout + "
                                 "vague/anchored list (fixes the format_fidelity wall of text); MODEL rebuilt as a "
                                 "coping-model think-aloud with the 3-question check folded in at point of first "
                                 "use; discrimination moved to explicit choices with the 'Grade-C design bet' "
                                 "jargon removed and the noun-after-this confound broken (DI faultless "
                                 "communication); FRQ + diagnosis bodies use frq_prompt/setapart/checklist (kills "
                                 "the 'Step 1/2' render double-numbering and the 'Scored on' chrome); independent "
                                 "says the standard out loud (Yeager). Teaching point + bound stimuli unchanged."),
                "review_provenance": ("Rebuilt to icm/_config/v3_1-lesson-build-spec.md (the pattern that cleared "
                                      "all 23 lesson_contract gates + the Fable-5 reviewer on G9 L01 v3.1)."),
                "council": ("T6/SPOT cohesion: introduces oC2 referential-cohesion (anchored vs vague reference). "
                            "Pronoun/reference mechanic app-owned + gated; taught by the cohesion JOB. "
                            "anchored-vs-vague discrimination labeled Grade-C in code (not in student text). "
                            "SPOT=proposal; ceiling sentence.")},
    fade_ledger_moves=["referential-cohesion", "anchor-the-back-reference"],
    slots=[
        # ===== TEACH: ONE idea in a callout + the vague/anchored contrast as a real LIST (no wall of text) =====
        Slot("TEACH", "teach_card", "Make your this, that, and it point clearly",
             body=(ONE_IDEA +
                   "Words like 'this,' 'that,' and 'it' let you refer back to an earlier idea without repeating "
                   "it, which is handy, but they cause trouble when they point to nothing clear. Referential "
                   "cohesion means every back-reference clearly names, or obviously points to, the exact thing "
                   "it stands for. Two versions to keep apart:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>VAGUE</strong>: a bare 'this' (or 'that' or 'it') at the "
                   "start of a sentence when two or three things came before it, so the reader cannot tell which "
                   "one you mean ('This makes it dangerous').</li>"
                   "<li style=\"margin:4px 0\"><strong>ANCHORED</strong>: the same reference with a noun added "
                   "right after it that names the exact thing it stands for ('This long distance makes it "
                   "dangerous').</li></ul>"
                   "The fix is that simple: add a noun after the reference, whatever names the real thing, so "
                   "'this' becomes 'this delay,' 'this combination,' or 'this risk.' The pronoun rules "
                   "themselves come from your earlier courses; today's job is the editing move. Goal: find a "
                   "vague reference in a provided sentence and anchor it.")),
        Slot("TEACH", "stimulus_display", "The topic: animal migration",
             ref="ACC-W910-FRAME-MIGRATION", bank="animal_migration",
             body=("The sentences you will fix are about animal migration. Read this short orientation so the "
                   "topic is familiar. You are not writing about migration from scratch here; you are anchoring "
                   "a vague reference in a sentence that is given to you.")),

        # ===== MODEL (before the quiz): coping-model think-aloud with the check tool folded in =====
        Slot("MODEL", "annotated_before_after", "Watch a writer anchor a vague this",
             bank="animal_migration",
             body=("Here is the skill in action. Follow the writer's editing below. " + COPING_HTML +
                   " Notice the one move that turned the BEFORE into the AFTER: the writer added a noun after "
                   "'this' that named the exact thing it points to. " + REMEMBER +
                   "When you fix your own sentence, do the same: find the bare reference, then add the noun that "
                   "names what it stands for, and run the 3 questions before you submit.")),
        Slot("MODEL", "discrimination", "Which version anchors the reference?",
             ref="", labeled_grade_c=True, bank="animal_migration",
             body=("Now that you have seen one built, spot the target. Both versions follow this sentence: 'Some "
                   "birds fly thousands of miles, and storms can strike along the way.' Which one anchors the "
                   "reference so the reader knows exactly what it points to? "
                   "(A) This makes the whole crossing risky for nearly every bird that sets out on the long journey.  "
                   "(B) This problem makes the crossing risky for the birds.  "
                   "(C) This mix of long distance and sudden storms makes the crossing risky. "
                   "Correct: C. It names the exact thing the reference points to."),
             choices=[
                 {"id": "A", "text": "This makes the whole crossing risky for nearly every bird that sets out on the long journey.",
                  "correct": False,
                  "why": "The bare 'This' could mean the long distance, the storms, or both. The reader still has to guess, so the reference is vague, no matter how long the sentence is."},
                 {"id": "B", "text": "This problem makes the crossing risky for the birds.",
                  "correct": False,
                  "why": "'This problem' does add a noun, but 'problem' is generic and still does not say which thing you mean. Naming a real referent, not just any noun, is what anchors it."},
                 {"id": "C", "text": "This mix of long distance and sudden storms makes the crossing risky.",
                  "correct": True,
                  "why": "Correct. 'This mix of long distance and sudden storms' names the exact thing the reference points to. Naming the real referent is the anchor."},
             ]),
        # Second minimal pair (different confound): under-reference (bare pronoun) vs OVER-reference (restate the
        # whole prior sentence to dodge the pronoun) vs a concise naming phrase. Correct (C) is NOT the longest;
        # the over-repeat distractor (B) is, so no distractor_length_cue.
        Slot("MODEL", "discrimination", "Which version anchors this reference?",
             ref="", labeled_grade_c=True, bank="animal_migration",
             body=("Spot the target again, this time with a different wrong answer to rule out. Both versions "
                   "follow this sentence: 'Migrating herds swim across wide rivers, and hungry predators wait at "
                   "the crossings.' Which version anchors the reference so the reader knows exactly what it points "
                   "to? "
                   "(A) This is the most dangerous part of the whole journey.  "
                   "(B) Swimming across the wide rivers while hungry predators wait at the crossings is the most dangerous part of the whole journey.  "
                   "(C) This river crossing is the most dangerous part of the whole journey. "
                   "Correct: C. A short naming phrase points the reference at the exact thing it stands for."),
             choices=[
                 {"id": "A", "text": "This is the most dangerous part of the whole journey.",
                  "correct": False,
                  "why": "The bare 'This' could point to the rivers, the predators, or both, so the reader still has to guess what it means."},
                 {"id": "B", "text": "Swimming across the wide rivers while hungry predators wait at the crossings is the most dangerous part of the whole journey.",
                  "correct": False,
                  "why": "Restating the whole earlier sentence does connect the ideas, but it is wordy and skips the short anchoring move that a naming phrase gives you."},
                 {"id": "C", "text": "This river crossing is the most dangerous part of the whole journey.",
                  "correct": True,
                  "why": "Correct. 'This river crossing' names the exact thing the reference points to, so the link between the sentences stays clear."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this vague reference most need?",
             bank="animal_migration",
             body=("Diagnose this draft before the reveal. A sentence reads: 'Migrating birds face predators, "
                   "hunger, and exhaustion. It is why so few survive their first migration.' Which single edit "
                   "would most improve the reference? "
                   "(A) replace the bare 'It' with a phrase that names the referent, such as 'This combination of dangers'  "
                   "(B) delete the second sentence so the paragraph ends right after predators, hunger, and exhaustion  "
                   "(C) add another danger, such as harsh weather, to the first sentence's list  "
                   "(D) change the singular 'It' to the plural 'They' so the pronoun matches the three dangers that the first sentence already listed out"),
             feedback=("Correct: A. 'It' points vaguely at three dangers at once, so the reader cannot tell what "
                       "'it' means. Anchoring it, 'This combination of dangers is why so few survive,' names the "
                       "referent. Deleting the sentence (B) loses the idea; another danger (C) adds content, not "
                       "clarity; 'They' (D) is still vague and does not match a singular idea.")),

        # ===== SUPPORTED: framed edit (fill-in frame) on the taught topic (source read at TEACH step 2) =====
        Slot("SUPPORTED", "production_frq", "Anchor the vague reference",
             ref="", bank="animal_migration", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Anchor the reference so it points to one clear thing. Here is the sentence to fix: 'Birds "
                       "must find food, dodge storms, and cross open water. This is what makes migration so hard.'",
                 setapart_block=setapart("Copy this frame, then fill in the blank:",
                                         "This ______ [a noun that names what 'this' points to] is what makes migration so hard."),
                 closer="Add a noun after 'this' that names exactly what it points to (the three challenges), and "
                        "keep the meaning. Then run the 3-question check before you submit.")),
        # DIAGNOSIS = run the check on a PROVIDED weak draft, then rewrite it (not a fresh production, so it does
        # not repeat the Finish write). Stays on the taught topic = no new source to read (load balance).
        Slot("MODEL", "diagnosis_frq", "Check and fix a weak draft with the 3 questions",
             ref="", bank="animal_migration", scored=True,
             body=frq_prompt(
                 intro="Run the 3-question check on this weak draft, then rewrite it so the reference is anchored.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "Birds cross deserts, oceans, and mountains on one trip. This is why the route is so risky.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Is there a back-reference (this, that, or it)?", "Yes, 'This.'"),
                     ("Does it point to one clear thing?", "No. It could mean the deserts, the oceans, or the mountains, so anchor it."),
                     ("What noun would name it?", "Something like 'This long chain of obstacles.'"),
                 ]),
                 closer="Now rewrite the weak draft into one sentence whose reference names exactly what it points "
                        "to. Then name which question your rewrite fixed.")),

        # ===== INDEPENDENT: cold edit on the taught topic + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Fix a vague reference on your own",
             ref="", bank="animal_migration", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="On your own now, no frame. Anchor the reference in this sentence so 'that' names exactly "
                       "what it points to: 'Young birds learn the route, build up fat, and wait for the right "
                       "winds. That is how they prepare.'",
                 closer="Add a noun after 'that' that names what it points to. A clear reference is what keeps any "
                        "piece of writing easy to follow, and you are ready to do this without a frame. Run the "
                        "3-question check before you submit.")),

        # ===== TRANSFER: same move, a NEW topic (volcanoes), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "The topic: volcanoes",
             ref="ACC-W910-FRAME-VOLCANOES", bank="volcanoes",
             body=("The next sentence to fix is about volcanoes. Read this short orientation so the topic is "
                   "familiar. Again, you are anchoring a vague reference in a provided sentence, not writing "
                   "from scratch.")),
        Slot("TRANSFER", "production_frq", "Fix a vague reference on a NEW topic",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="New topic. Anchor the reference in this sentence so 'this' names exactly what it points "
                       "to: 'A volcano can release ash, gas, and lava all at once. This can force whole towns to "
                       "evacuate.'",
                 closer="Same anchoring move, new topic: add a noun after 'this' that names what it points to. "
                        "Run the 3-question check before you submit.")),
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
