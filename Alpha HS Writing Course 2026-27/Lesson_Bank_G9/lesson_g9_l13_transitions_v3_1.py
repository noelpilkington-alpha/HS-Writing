"""
lesson_g9_l14_transitions_v3_1.py  -  G9 KC C.9.06, ARCHETYPE T3 (cohesion), ceiling paragraph. V3.1.

Rebuild of lesson_g9_l14_transitions.py to the v3.1 pattern (icm/_config/v3_1-lesson-build-spec.md, derived
from G9 L01 v3.1). Teaching point PRESERVED: connect sentences with the transition that names the TRUE
relationship (add / contrast / cause / sequence), not a filler like "also" or "then". KC C.9.06. Bound stimuli
PRESERVED: taught FRAME-PHOTOSYNTHESIS -> transfer FRAME-MIGRATION (bank-partitioned). All Lesson() field
values kept from the current L14 (id, lesson_type=3, mnemonic_status established-caveat, every production_frq
unit='paragraph').

What changed to reach v3.1:
  1. TEACH split to ONE idea, hammered: a teal ONE_IDEA callout + the relationship types as a real <ul> list
     (fixes the 142-word wall-of-text the old teach_card was). The check tool is NOT cold in TEACH; it is folded
     into the MODEL card at the point of first use (KH load).
  2. MODEL rewritten as a coping-model think-aloud: a writer drafts the paragraph with filler "also," runs the
     2-question check, catches that the links are really a sequence plus a contrast, and revises. Still contains
     literal BEFORE and AFTER inline (content_depth). No named near-peer (Timeback stateless rule).
  3. DISCRIMINATION uses explicit choices=[{id,text,correct,why}]; the internal "Grade-C design bet" label is
     REMOVED from student text (leaked_internal_label); the correct option is the SHORTEST, not the lone longest,
     and all three options are legitimate transitions signalling different relationships so the only invariant is
     "names the true relationship" (DI faultless communication - no surface confound).
  4. SUPPORTED / DIAGNOSIS / production FRQs built with frq_prompt / setapart / checklist: fill-in frame first,
     then the check as a real <ol> (no "Step 1/2" prose that double-numbered in render-QC), no "Scored on ..."
     rubric chrome.
  5. INDEPENDENT names the standard out loud (Yeager) and hands the check over.

Passes all 23 lesson_contract gates + render-QC clean. Own words, no fabricated figures, no em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A transition should name the '
'<strong>TRUE relationship</strong> between two ideas, not fill space. Filler like "also" or "then" hides the '
'relationship; the right signpost shows it.</div></div>')

# the reusable check tool, folded into the MODEL card at the point of first use (not cold in TEACH).
REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: 2 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">At every link between two ideas, ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">What is the real relationship here: add, contrast, cause, or sequence?</li>'
'<li style="margin:2px 0">Does the transition name that relationship, or is it filler?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If it is filler, swap in the signpost that matches the relationship.</div></div>')

# coping-model think-aloud: a WRITTEN drafting process (draft with filler -> run the check -> catch -> revise),
# then the literal BEFORE and AFTER endpoints (content_depth).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer thinking it through, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First draft:</strong> "Plants take in sunlight. Also, they take in water. '
    'Also, they make sugar. Also, some of that energy is later lost." Run the check: is every link really adding '
    'a similar idea? No. Taking in sunlight, then water, then making sugar are steps in a sequence. And losing '
    'energy goes against making it, that is a contrast. One filler word hid all of that.</p>'
    '<p style="margin:0 0 8px"><strong>Fix the steps:</strong> the first three are a sequence, so use sequence '
    'signposts: "Plants take in sunlight. Next, they take in water. Then they make sugar."</p>'
    '<p style="margin:0"><strong>Fix the contrast:</strong> the last idea pulls the other way, so use a contrast '
    'signpost: "However, some of that energy is later lost." Now each transition names the real relationship.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "Plants take in sunlight. Also, they take in water. Also, they '
    'make sugar. Also, some of that energy is later lost." (every link is filler "also")</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "Plants take in sunlight. Next, they take in water. Then they '
    'make sugar. However, some of that energy is later lost." (sequence for the steps, contrast for the loss)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C906-0014", grade="9-10", lesson_type=3,
    unit="G9 U3 - Cohesion (transition by function)",
    title="Pick the Transition the Logic Needs",
    target=("Connect sentences with the transition that names the true relationship, add, contrast, cause, "
            "sequence, or conclude, instead of a filler like 'also' or 'then'. Written at the paragraph. "
            "Trait: Organization."),
    acc_tags=["ACC.W.ARG.3", "CCSS.W.9-10.1c"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-14",
                "mnemonic_status": "established-caveat", "kc": "C.9.06", "sot": "icm course-G9.md L14",
                "taught_stimulus": "ACC-W910-FRAME-PHOTOSYNTHESIS",
                "transfer_stimulus": "ACC-W910-FRAME-MIGRATION",
                "one_idea": "A transition should name the true relationship (add/contrast/cause/sequence), not fill space.",
                "one_reminder": "2-question check: what is the real relationship? does the transition name it?",
                "playbook": "_phase2/playbook_T3_PROVE.md",
                "template": "v3.1 pattern (G9 L01 v3.1); COHESION-TIER binds a lightweight issue_frame (material is a provided paragraph, inline).",
                "version_note": ("V3.1: rebuilt to the v3.1 spec - TEACH split to ONE idea + a relationship list "
                                 "(fixes the wall-of-text teach_card); MODEL rewritten as a coping-model "
                                 "think-aloud with literal BEFORE/AFTER; discrimination moved to explicit choices "
                                 "with the internal 'Grade-C' label removed and the correct option no longer the "
                                 "longest; FRQ/diagnosis bodies built with frq_prompt/setapart/checklist (no "
                                 "'Step N' prose, no 'Scored on' chrome); say-the-standard on the independent write."),
                "council": ("Cohesion intro: introduces oC1 transition-by-function (right-function vs filler "
                            "transition). Transition words app-owned + gated; taught by the RELATIONSHIP they "
                            "signal, not as a word list. Right-vs-filler discrimination is the discriminate-before-"
                            "produce move (labeled_grade_c in code, never in student text).")},
    fade_ledger_moves=["transition-by-function", "name-the-real-relationship"],
    slots=[
        # ===== TEACH: ONE idea, hammered - callout + the relationship types as a real list (no wall of text) =====
        Slot("TEACH", "teach_card", "The one idea: name the relationship, do not fill space",
             body=(ONE_IDEA +
                   "A transition is a signpost telling the reader how one idea relates to the next. Most "
                   "relationships fall into a few kinds, each with its own signposts:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>ADD</strong> a similar idea: also, in addition.</li>"
                   "<li style=\"margin:4px 0\"><strong>CONTRAST</strong>, ideas that pull apart: however, but, on "
                   "the other hand.</li>"
                   "<li style=\"margin:4px 0\"><strong>CAUSE</strong>, one idea leads to another: because, as a "
                   "result, so.</li>"
                   "<li style=\"margin:4px 0\"><strong>SEQUENCE</strong> or time, steps in order: first, next, "
                   "finally.</li></ul>"
                   "The trap is filler, mostly 'also' and 'then' dropped in everywhere, which signals nothing. "
                   "The move: name the real relationship first, then pick the signpost that matches it. You "
                   "already know these words from earlier courses; here you choose the one the logic needs.")),
        Slot("TEACH", "stimulus_display", "The topic: photosynthesis",
             ref="ACC-W910-FRAME-PHOTOSYNTHESIS", bank="photosynthesis",
             body=("The paragraph you will fix is about photosynthesis. Read this short orientation so the topic "
                   "is familiar. You are not writing about photosynthesis from scratch; you are improving the "
                   "transitions in a paragraph that is given to you. You only need the gist of the steps.")),

        # ===== MODEL (before the quiz): coping-model think-aloud + the check tool folded in at first use =====
        Slot("MODEL", "annotated_before_after", "Watch a writer fix filler transitions",
             bank="photosynthesis",
             body=("Here is the skill in action. Follow the writer's thinking as filler 'also' becomes signposts "
                   "that fit. " + COPING_HTML +
                   " Notice the move that turned the BEFORE into the AFTER: the writer named the real "
                   "relationship at each link, then chose the signpost that matched it. " + REMEMBER +
                   "When you fix a paragraph of your own, do the same: name the relationship first, then pick the "
                   "transition that names it.")),
        Slot("MODEL", "discrimination", "Which transition names the real relationship?",
             ref="", labeled_grade_c=True, bank="photosynthesis",
             body=("Spot the target before you revise. The idea before: 'A plant makes sugar for energy.' The "
                   "idea after: 'some of that energy is lost as the plant uses it.' Which transition names the "
                   "real relationship between them? "
                   "(A) In addition, some of that energy is lost as the plant uses it.  "
                   "(B) As a result, some of that energy is lost as the plant uses it.  "
                   "(C) However, some of that energy is lost as the plant uses it. "
                   "Correct: C. The second idea contrasts with the first."),
             choices=[
                 {"id": "A", "text": "In addition, some of that energy is lost as the plant uses it.",
                  "correct": False,
                  "why": "'In addition' signals adding a similar idea, so it hides the real relationship. The second idea does not add to the first; it goes against it."},
                 {"id": "B", "text": "As a result, some of that energy is lost as the plant uses it.",
                  "correct": False,
                  "why": "'As a result' signals cause and effect, but the loss is not caused by making sugar. The two ideas pull in opposite directions, so this names the wrong relationship."},
                 {"id": "C", "text": "However, some of that energy is lost as the plant uses it.",
                  "correct": True,
                  "why": "Correct. The second idea contrasts with the first (the plant makes energy, then loses some), so 'however' names the true relationship."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this transition most need?",
             bank="photosynthesis",
             body=("Diagnose this before the reveal. A paragraph reads: 'Plants need sunlight to make food. Then, "
                   "without enough light, a plant cannot make enough food and may die.' The word 'then' is used. "
                   "Which single change would most improve the transition? "
                   "(A) replace 'then' with a cause-and-effect signpost like 'as a result' or 'so,' because the "
                   "second idea is the consequence of the first  "
                   "(B) delete the second sentence completely, since the first sentence already states the point "
                   "and the extra idea is not really needed here  "
                   "(C) add another 'then' at the start of the first sentence too, so both sentences begin the "
                   "same way and the pair feels balanced to read  "
                   "(D) make both sentences shorter and simpler, since the transition reads badly mostly because "
                   "the two sentences run on for too long"),
             feedback=("Correct: A. The second idea is the RESULT of the first (no light, so no food), but 'then' "
                       "signals mere time sequence, not cause. A cause signpost, 'as a result' or 'so,' names the "
                       "true relationship. Deleting the sentence (B) loses the idea; another 'then' (C) adds "
                       "filler; shorter sentences (D) do not fix the wrong signpost.")),

        # ===== SUPPORTED: framed write (fill-in frame) on the taught topic =====
        Slot("SUPPORTED", "production_frq", "Fix the transitions using the frame",
             ref="", bank="photosynthesis", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="Revise this paragraph so each transition names the real relationship. The frame shows "
                       "where the transitions go.",
                 setapart_block=setapart("Copy this paragraph, then replace each blank with a transition that fits:",
                                         "Plants take in sunlight. ______ they take in water and carbon dioxide. "
                                         "______ they make sugar. ______ some energy is lost as the plant uses the sugar."),
                 closer="Use a sequence signpost (next, then) for the steps and a contrast signpost (however, "
                        "but) for the loss. Keep the ideas; change only the transitions.")),
        # DIAGNOSIS = watch the check run on a PROVIDED draft, then run it on a fresh paragraph. Scaffolded with a
        # real checklist (no "Step N" prose). Stays on the taught topic = no new source to read (load balance).
        Slot("MODEL", "diagnosis_frq", "Check the transitions in a fresh paragraph",
             ref="", bank="photosynthesis", scored=True,
             body=frq_prompt(
                 intro="Run the 2-question check on this provided draft, then write and check your own.",
                 setapart_block=setapart("Provided draft to check:",
                                         "Sunlight reaches the leaf. Also, the leaf absorbs it. Also, this can be blocked by shade."),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("What is the real relationship at each link?",
                      "Sunlight then absorb is a sequence; absorb versus blocked-by-shade is a contrast."),
                     ("Does the transition match it?",
                      "No, both are 'also,' so replace them (next, however)."),
                 ]),
                 closer="Now write a fresh two-or-three-sentence paragraph on photosynthesis. Check each "
                        "transition against the two questions and fix any filler before you submit. Finish by "
                        "naming which relationship each transition signals.")),

        # ===== INDEPENDENT: revise a provided paragraph, no frame, say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Revise a provided paragraph on your own",
             ref="", bank="photosynthesis", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="On your own now, no frame. Revise this paragraph so every transition names the real relationship.",
                 setapart_block=setapart("Paragraph to revise:",
                                         "Leaves capture light. Also, they use it to split water. Also, this "
                                         "releases oxygen. Also, too little light slows the whole process."),
                 closer="Use sequence signposts for the steps and a contrast signpost for the last idea. Naming "
                        "the real relationship is what real writing does to stay clear, and you are ready to do "
                        "it without a frame. Before you submit, check each transition: does it name the "
                        "relationship, or is it filler?")),

        # ===== TRANSFER: same move, a NEW topic (animal migration), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "The topic: animal migration",
             ref="ACC-W910-FRAME-MIGRATION", bank="animal_migration",
             body=("The next paragraph to fix is about animal migration. Read this short orientation so the topic "
                   "is familiar. Again, you are improving the transitions in a provided paragraph, not writing "
                   "from scratch. You only need the gist.")),
        Slot("TRANSFER", "production_frq", "Revise a provided paragraph on a NEW topic",
             ref="", bank="animal_migration", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="New topic, same move. Revise this paragraph so every transition names the real relationship.",
                 setapart_block=setapart("Paragraph to revise:",
                                         "Birds sense the seasons changing. Also, they gather in large groups. "
                                         "Also, they fly toward warmer regions. Also, a few stay behind and "
                                         "struggle to find food."),
                 closer="Use sequence signposts for the steps and a contrast signpost for the last idea. Check "
                        "each transition against the two questions before you submit.")),
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
