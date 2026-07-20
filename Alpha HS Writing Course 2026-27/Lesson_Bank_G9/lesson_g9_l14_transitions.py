"""
lesson_g9_l14_transitions.py  -  G9 KC C.9.06, ARCHETYPE T3 (cohesion), ceiling paragraph.

G9 course L14 (Unit 3 Cohesion, intro). Transition by FUNCTION (oC1): pick the connector that names the true
relationship (add / contrast / cause / sequence / conclude), not a filler "also/then". Locked L01 template.
COHESION-TIER: the material is a PROVIDED paragraph (inline); binds a lightweight issue_frame for topic
context. Taught: FRAME-PHOTOSYNTHESIS -> transfer: FRAME-MIGRATION (bank-partitioned). rc.staar,
unit="paragraph" (Unit 3 works at the paragraph). The transition WORDS are app-owned + gated; taught by the
FUNCTION (the relationship) they signal. No coping-model persona; no source markup; no prior-work ref; no em
dashes. Runs QC on execution.
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
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> filler transitions hide the real relationships</span>'
    '<p style="margin:8px 0 0;font-size:15px">Plants take in sunlight. Also, they take in water and carbon '
    'dioxide. Also, they make sugar. Also, some energy is lost as the plant uses the sugar.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">Every link is "also," so the reader cannot tell '
    'what actually connects the ideas. Some are steps in a sequence; one is a contrast. Filler transitions '
    'flatten all of that.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> each transition names the real relationship</span>'
    '<p style="margin:8px 0 0;font-size:15px">Plants take in sunlight. '
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">SEQUENCE</span> Next, they combine it with water and carbon dioxide. '
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">SEQUENCE</span> As a result, they produce sugar. '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">CONTRAST</span> However, some of that energy is later lost as the plant uses the '
      'sugar.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">"Next" and "as a result" mark the steps; '
    '"however" marks the contrast. Each transition now names the true relationship.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C906-0014", grade="9-10", lesson_type=3,
    unit="G9 U3 - Cohesion (transition by function)",
    title="Pick the Transition the Logic Needs",
    target=("Connect sentences with the transition that names the true relationship, add, contrast, cause, "
            "sequence, or conclude, instead of a filler like 'also' or 'then'. Written at the paragraph. "
            "Trait: Organization."),
    acc_tags=["ACC.W.ARG.3", "CCSS.W.9-10.1c"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12",
                "mnemonic_status": "established-caveat", "kc": "C.9.06", "sot": "icm course-G9.md L14",
                "taught_stimulus": "ACC-W910-FRAME-PHOTOSYNTHESIS",
                "transfer_stimulus": "ACC-W910-FRAME-MIGRATION",
                "playbook": "_phase2/playbook_T3_PROVE.md",
                "template": "locked L01 template; COHESION-TIER binds a lightweight issue_frame (material is a provided paragraph, inline).",
                "council": ("Cohesion intro: introduces oC1 transition-by-function (right-function vs filler "
                            "transition). Transition words app-owned + gated; taught by the RELATIONSHIP they "
                            "signal, not as a word list. right-vs-filler discrimination labeled Grade-C.")},
    fade_ledger_moves=["transition-by-function", "name-the-real-relationship"],
    slots=[
        Slot("TEACH", "teach_card", "Transitions are signposts for relationships",
             body=("A transition is a signpost that tells the reader how one idea relates to the next. The trap "
                   "is filler transitions, mostly 'also' and 'then', dropped in everywhere so they signal "
                   "nothing. Transition by function means picking the connector that names the TRUE "
                   "relationship between two ideas. There are a few common relationships, each with its own "
                   "signposts: adding a similar idea (also, in addition), contrast (however, but, on the other "
                   "hand), cause and effect (because, as a result, so), sequence or time (first, next, "
                   "finally), and concluding (in short, overall). The move is to name the real relationship, "
                   "then choose the signpost that matches it. The transition words themselves are a skill you "
                   "already own from earlier courses; here you learn to choose the one the logic actually "
                   "needs. Goal today: replace filler transitions with ones that name the real relationship.")),
        Slot("TEACH", "stimulus_display", "The topic: photosynthesis",
             ref="ACC-W910-FRAME-PHOTOSYNTHESIS", bank="photosynthesis",
             body=("The paragraph you will fix is about photosynthesis. Read this short orientation so the topic "
                   "is familiar. You are not writing about photosynthesis from scratch here; you are improving "
                   "the transitions in a paragraph that is given to you.")),
        Slot("TEACH", "discrimination", "Which transition names the real relationship?",
             ref="", labeled_grade_c=True, bank="photosynthesis",
             body=("Sort these before you revise (spotting the target first, a Grade-C design bet we label as a "
                   "bet, not a proven ingredient). The idea before: 'A plant makes sugar for energy.' The idea "
                   "after: 'some of that energy is lost as the plant uses it.' Which transition names the real "
                   "relationship between them? "
                   "(A) In addition, some of that energy is lost as the plant uses it.  "
                   "(B) However, some of that energy is lost as the plant uses it. "
                   "Correct: B. The second idea CONTRASTS with the first (the plant makes energy, but then "
                   "loses some), so 'however' names the real relationship. 'Also' (A) is filler here, it "
                   "signals adding a similar idea, which hides the contrast. Matching the signpost to the "
                   "relationship is the move.")),
        Slot("MODEL", "annotated_before_after", "Watch filler transitions become functional ones",
             bank="photosynthesis",
             body=("Here is a choppy paragraph whose filler transitions get replaced with ones that name the "
                   "real relationships. Read the BEFORE, then the AFTER, and notice each 'also' become a "
                   "signpost that fits." + BEFORE_AFTER_HTML +
                   " The BEFORE links everything with 'also.' The AFTER uses 'next' and 'as a result' for the "
                   "steps and 'however' for the contrast. Naming the relationship is the move.")),
        Slot("MODEL", "predict_the_fix", "What does this transition most need?",
             bank="photosynthesis",
             body=("Diagnose before the reveal. A paragraph reads: 'Plants need sunlight to make food. Then, "
                   "without enough light, a plant cannot make enough food and may die.' The word 'then' is "
                   "used. Which single change would most improve the transition? "
                   "(A) replace 'then' with a cause-and-effect signpost like 'as a result' or 'so,' because "
                   "the second idea is the consequence of the first  "
                   "(B) delete the second sentence completely, since the first sentence already states the "
                   "point and the extra idea is not really needed here  "
                   "(C) add another 'then' at the start of the first sentence too, so both sentences begin "
                   "the same way and the pair feels balanced to read  "
                   "(D) make both sentences shorter and simpler, since the transition reads badly mostly "
                   "because the two sentences run on for too long"),
             feedback=("Correct: A. The second idea is the RESULT of the first (no light, so no food), but "
                       "'then' signals mere time sequence, not cause. A cause signpost, 'as a result' or 'so,' "
                       "names the true relationship. Deleting the sentence (B) loses the idea; another 'then' "
                       "(C) adds filler; shorter sentences (D) do not fix the wrong signpost.")),
        Slot("SUPPORTED", "production_frq", "Fix the transitions in a provided paragraph",
             ref="", bank="photosynthesis", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=("Revise this provided paragraph by fixing its transitions: 'Plants take in sunlight. Also, "
                   "they take in water and carbon dioxide. Also, they make sugar. Also, some energy is lost as "
                   "the plant uses the sugar.' Rewrite it so each transition names the real relationship "
                   "(sequence for the steps, contrast for the loss). Keep the ideas; change only the "
                   "transitions and small wording needed to fit them. Scored on Organization.")),
        Slot("MODEL", "diagnosis_frq", "Check the transitions in a fresh paragraph",
             ref="", bank="photosynthesis", scored=True,
             body=("First watch the check run on a provided draft, then run it on a fresh paragraph of your "
                   "own. Provided draft: 'Sunlight reaches the leaf. Also, the leaf absorbs it. Also, this can "
                   "be blocked by shade.' Run the check step by step. Step 1, name the real relationship at "
                   "each link: sunlight-then-absorb is a sequence, but absorb-versus-blocked-by-shade is a "
                   "contrast. Step 2, does the transition match? No, both are 'also,' so replace them (next / "
                   "however). Now you: write a fresh two-or-three-sentence paragraph on photosynthesis, then "
                   "check each transition, does it name the real relationship? Use the fix if any is filler. "
                   "Finish by naming which relationship each transition signals.")),
        Slot("INDEPENDENT", "production_frq", "Revise a provided paragraph on your own",
             ref="", bank="photosynthesis", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=("On your own now. Revise this provided paragraph so every transition names the real "
                   "relationship: 'Leaves capture light. Also, they use it to split water. Also, this releases "
                   "oxygen. Also, too little light slows the whole process.' Rewrite it with functional "
                   "transitions (sequence for the steps, contrast for the last idea). Before you submit, check "
                   "each transition: does it name the real relationship, or is it filler? Fix any filler before "
                   "you submit. Scored on Organization.")),
        Slot("TRANSFER", "stimulus_display", "The topic: animal migration",
             ref="ACC-W910-FRAME-MIGRATION", bank="animal_migration",
             body=("The next paragraph to fix is about animal migration. Read this short orientation so the "
                   "topic is familiar. Again, you are improving the transitions in a provided paragraph, not "
                   "writing from scratch.")),
        Slot("TRANSFER", "production_frq", "Revise a provided paragraph on a NEW topic",
             ref="", bank="animal_migration", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=("New topic. Revise this provided paragraph so every transition names the real relationship: "
                   "'Birds sense the seasons changing. Also, they gather in large groups. Also, they fly toward "
                   "warmer regions. Also, a few stay behind and struggle to find food.' Rewrite it with "
                   "functional transitions (sequence for the steps, contrast for the last idea). Same move as "
                   "the photosynthesis paragraph, new topic. Scored on Organization.")),
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
