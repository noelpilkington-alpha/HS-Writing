"""
lesson_g9_l15_referential_cohesion.py  -  G9 KC C.9.06, ARCHETYPE T6: EDITING-IN-CONTEXT (SPOT, ceiling sentence).

G9 course L15 (Unit 3 Cohesion, guided). Referential cohesion (oC2): fix a vague back-reference (a naked
"this/which") so it clearly points to what it means. Locked L01 template. COHESION-TIER: the material is a
PROVIDED paragraph (inline); binds a lightweight issue_frame for topic context. Taught: FRAME-MIGRATION ->
transfer: FRAME-VOLCANOES (bank-partitioned). rc.staar, unit="sentence" (T6 ceiling = sentence; the edit is a
sentence-level fix inside a paragraph). SPOT=proposal. The pronoun/reference mechanic is app-owned + gated;
taught by the cohesion JOB (does the reference point clearly?). No coping-model persona; no source markup; no
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
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> a naked "this" points to nothing clear</span>'
    '<p style="margin:8px 0 0;font-size:15px">Some birds fly thousands of miles, and the weather can turn '
    'harsh along the way. This makes migration dangerous.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">"This" could mean the long distance, the harsh '
    'weather, or both. The reader has to guess what it points to, so the sentences do not connect cleanly.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> the reference names what it points to</span>'
    '<p style="margin:8px 0 0;font-size:15px">Some birds fly thousands of miles, and the weather can turn '
    'harsh along the way. '
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">ANCHORED</span> This combination of distance and bad weather makes migration '
      'dangerous.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Adding a noun after "this" (this combination of '
    'distance and bad weather) anchors the reference, so the reader knows exactly what it points to.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C906-0015", grade="9-10", lesson_type=6,
    unit="G9 U3 - Cohesion (referential cohesion)",
    title="Make Every This and It Point Clearly",
    target=("Fix a vague back-reference: when a sentence starts with a naked 'this,' 'that,' or 'it,' anchor it "
            "by naming what it points to, so sentences connect cleanly. Written at the sentence. Trait: "
            "Organization/Conventions."),
    acc_tags=["ACC.W.INFO.3", "CCSS.W.9-10.2c"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12",
                "mnemonic_status": "proposal", "kc": "C.9.06", "sot": "icm course-G9.md L15",
                "taught_stimulus": "ACC-W910-FRAME-MIGRATION",
                "transfer_stimulus": "ACC-W910-FRAME-VOLCANOES",
                "playbook": "_phase2/playbook_T6_SPOT.md",
                "template": "locked L01 template; COHESION-TIER binds a lightweight issue_frame (material is a provided paragraph, inline).",
                "council": ("T6/SPOT cohesion: introduces oC2 referential-cohesion (anchored vs vague "
                            "reference). Pronoun/reference mechanic app-owned + gated; taught by the cohesion "
                            "JOB. anchored-vs-vague discrimination labeled Grade-C. SPOT=proposal; ceiling "
                            "sentence.")},
    fade_ledger_moves=["referential-cohesion", "anchor-the-back-reference"],
    slots=[
        Slot("TEACH", "teach_card", "Make your this, that, and it point clearly",
             body=("Words like 'this,' 'that,' 'it,' and 'which' are handy because they let you refer back to "
                   "an earlier idea without repeating it. But they cause trouble when they point to nothing "
                   "clear. Referential cohesion means every back-reference clearly names, or obviously points "
                   "to, the exact thing it stands for. A vague reference is a naked 'this' at the start of a "
                   "sentence when two or three things came before it, so the reader cannot tell which one you "
                   "mean. The fix is simple: add a noun right after it. 'This' becomes 'this delay,' 'this "
                   "combination,' 'this risk', whatever names the real referent. Compare: 'This makes it "
                   "dangerous' (vague) versus 'This long distance makes it dangerous' (anchored). This is an "
                   "editing move that keeps sentences connected; the pronoun rules themselves come from your "
                   "earlier courses. Goal today: find a vague reference in a provided paragraph and anchor it.")),
        Slot("TEACH", "stimulus_display", "The topic: animal migration",
             ref="ACC-W910-FRAME-MIGRATION", bank="animal_migration",
             body=("The sentences you will fix are about animal migration. Read this short orientation so the "
                   "topic is familiar. You are not writing about migration from scratch here; you are anchoring "
                   "a vague reference in a sentence that is given to you.")),
        Slot("TEACH", "discrimination", "Which reference is anchored, and which is vague?",
             ref="", labeled_grade_c=True, bank="animal_migration",
             body=("Sort these before you edit (spotting the target first, a Grade-C design bet we label as a "
                   "bet, not a proven ingredient). Both follow this sentence: 'Some birds fly thousands of "
                   "miles, and storms can strike along the way.' Which version anchors the reference clearly? "
                   "(A) This makes the whole trip risky for nearly every bird that tries it.  "
                   "(B) This mix of long distance and sudden storms makes migration risky. "
                   "Correct: B. In (A), 'this' could mean the distance, the storms, or both, so the reader "
                   "guesses. In (B), 'this mix of long distance and sudden storms' names exactly what the "
                   "reference points to. Naming the referent is the anchor.")),
        Slot("MODEL", "annotated_before_after", "Watch a vague this get anchored",
             bank="animal_migration",
             body=("Here is a vague reference being anchored. Read the BEFORE, then the AFTER, and notice the "
                   "noun added after 'this' to name what it points to." + BEFORE_AFTER_HTML +
                   " The BEFORE leaves 'this' floating between two possible referents. The AFTER names the "
                   "referent (this combination of distance and bad weather). Adding the naming noun is the "
                   "edit.")),
        Slot("MODEL", "predict_the_fix", "What does this vague reference most need?",
             bank="animal_migration",
             body=("Diagnose before the reveal. A sentence reads: 'Migrating birds face predators, hunger, and "
                   "exhaustion. It is why so few survive their first migration.' Which single edit would most "
                   "improve the reference? "
                   "(A) replace the naked 'It' with a phrase that names the referent, such as 'This "
                   "combination of dangers'  "
                   "(B) delete the second sentence completely so the paragraph ends right after predators, hunger, and exhaustion  "
                   "(C) add another danger, such as harsh weather, to the first sentence's list of things birds face  "
                   "(D) change the singular 'It' to the plural 'They' so the pronoun matches the three dangers listed"),
             feedback=("Correct: A. 'It' points vaguely at three dangers at once, so the reader cannot tell "
                       "what 'it' means. Anchoring it, 'This combination of dangers is why so few survive,' "
                       "names the referent. Deleting the sentence (B) loses the idea; another example (C) adds "
                       "content, not clarity; 'They' (D) is still vague and does not match a singular idea.")),
        Slot("SUPPORTED", "production_frq", "Anchor the vague reference",
             ref="", bank="animal_migration", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("Revise this provided sentence so the reference is anchored: 'Birds must find food, dodge "
                   "storms, and cross open water. This is what makes migration so hard.' Rewrite the second "
                   "sentence so 'this' names exactly what it points to (add a noun after it). Keep the meaning; "
                   "change only what is needed to anchor the reference. Write one sentence. Scored on "
                   "Organization/Conventions.")),
        Slot("MODEL", "diagnosis_frq", "Check a fresh sentence for a vague reference",
             ref="", bank="animal_migration", scored=True,
             body=("First watch the check run on a provided draft, then run it on a fresh sentence of your own. "
                   "Provided draft: 'Some birds migrate at night and some by day. This helps scientists study "
                   "them.' Run the check step by step. Step 1, is there a back-reference (this/that/it)? Yes, "
                   "'this.' Step 2, does it point to one clear thing? No, it could mean night-flying, day-"
                   "flying, or the variety itself, so anchor it (for example 'This variety in timing'). Now "
                   "you: write one fresh sentence about migration that uses 'this' or 'it' to refer back, then "
                   "check it, does the reference point to one clear thing? Anchor it if not. Finish by naming "
                   "what your reference points to.")),
        Slot("INDEPENDENT", "production_frq", "Fix a vague reference on your own",
             ref="", bank="animal_migration", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("On your own now. Revise this provided sentence so the reference is anchored: 'Young birds "
                   "learn the route, build up fat, and wait for the right winds. That is how they prepare.' "
                   "Rewrite the second sentence so 'that' names exactly what it points to. Before you submit, "
                   "check: does the reference point to one clear thing? If it is still vague, anchor it before "
                   "you submit. Scored on Organization/Conventions.")),
        Slot("TRANSFER", "stimulus_display", "The topic: volcanoes",
             ref="ACC-W910-FRAME-VOLCANOES", bank="volcanoes",
             body=("The next sentence to fix is about volcanoes. Read this short orientation so the topic is "
                   "familiar. Again, you are anchoring a vague reference in a provided sentence, not writing "
                   "from scratch.")),
        Slot("TRANSFER", "production_frq", "Fix a vague reference on a NEW topic",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("New topic. Revise this provided sentence so the reference is anchored: 'A volcano can "
                   "release ash, gas, and lava all at once. This can force whole towns to evacuate.' Rewrite "
                   "the second sentence so 'this' names exactly what it points to. Same anchoring move as the "
                   "migration sentences, new topic. Scored on Organization/Conventions.")),
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
