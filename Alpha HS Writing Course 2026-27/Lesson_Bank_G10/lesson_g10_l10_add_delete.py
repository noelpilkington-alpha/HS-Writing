"""
lesson_g10_l10_add_delete.py  -  G10 KC C.10.05, ARCHETYPE T6: EDITING-IN-CONTEXT (SPOT, ceiling sentence).
V3.1 rebuild of the pre-v3.1 L10 to the v3.1 lesson build spec (icm/_config/v3_1-lesson-build-spec.md), the
pattern that cleared all 23 lesson_contract gates + the Fable-5 reviewer on G9 L01/L15 v3.1.

TEACHING POINT (KEEP): rhetorical revision by two moves. Add for purpose: supply the piece the reader needs to
follow or believe the point. Delete off purpose: cut a sentence that does not serve the point, even if it is
true. The test for every sentence: does this help the reader with THIS point? KC C.10.05. Bound stimuli
unchanged: taught WETLANDS -> transfer HIGHWAYS (bank-partitioned).

V3.1 changes from the pre-v3.1 L10 (design pattern, not the teaching point):
  1. TEACH split into ONE idea in a teal callout + the add/delete contrast as a real LIST (was a ~130-word wall
     of prose that tripped format_fidelity).
  2. MODEL rebuilt as a coping-model think-aloud (draft -> run the check -> catch the off-purpose line + thin
     detail -> revise), still with a literal BEFORE and AFTER; the reusable 3-question check tool is folded in
     at point of first use (REMEMBER dashed box).
  3. DISCRIMINATION uses explicit choices=[{id,text,correct,why}]; the leaked "Grade-C design bet" jargon is
     gone from the student prompt (labeled_grade_c stays True in code only). Confound broken: two options are
     both true wetlands facts, so the invariant is "serves THIS point," not "is false." Correct option is not
     the lone longest (options padded to homogeneous length).
  4. PREDICT-THE-FIX reveal lives in feedback= (no leaked answer cue in the option text).
  5. FRQ + diagnosis bodies built with frq_prompt / setapart / checklist (no "Step 1/Step 2" prose -> kills the
     render double-numbering; no "Scored on ..." chrome).
  6. INDEPENDENT names the standard out loud (Yeager). TRANSFER stays a partitioned new topic (highways).

id, lesson_type=6, kc=C.10.05, and mnemonic_status="proposal" are the current L10's values, unchanged; every
production_frq unit="sentence" (T6 ceiling). Own words, faithful to the bound federal sources (no fabricated
figures), no em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Every sentence should serve the point. '
'<strong>Add</strong> the piece the reader needs to follow the point, and <strong>delete</strong> the piece '
'that does not serve it, even when that piece is true.</div></div>')

# reusable job-aid, folded in at point of first use (the model card), not cold in step 1 (KH load management).
REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit a revised draft, run this quick test on it:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">What is the point of this draft?</li>'
'<li style="margin:2px 0">Does each sentence help the reader with THAT point?</li>'
'<li style="margin:2px 0">If a sentence wanders off the point, cut it; if a needed piece is missing, add it.</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">A true fact that does not serve the point still has to go.</div></div>')

# coping-model think-aloud: a WRITTEN revising process (draft -> run the check -> catch the off-purpose line and
# the thin detail -> revise), then the endpoints. Contains a literal BEFORE and AFTER (content_depth). No named
# near-peer (Timeback stateless rule). Facts are faithful to the bound wetlands source.
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer revising a draft, one pass at a time. The point is: wetlands protect against floods.</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First draft:</strong> "Wetlands protect against floods. Some people think '
    'swamps look ugly. They hold rain." Run the check: does each sentence serve the flood point? The line about '
    'swamps looking ugly does not, so it has to go. And "they hold rain" is too thin to show HOW.</p>'
    '<p style="margin:0 0 8px"><strong>Second pass:</strong> I cut the ugly line: "Wetlands protect against '
    'floods. They hold rain." Better, the off-purpose sentence is gone. But "they hold rain" still does not show '
    'the reader HOW the protection works. A needed detail is missing, so I add one.</p>'
    '<p style="margin:0"><strong>Final:</strong> "Wetlands protect against floods. They soak up heavy rain like '
    'a sponge and release it slowly, so nearby rivers rise less sharply." Now every sentence serves the point.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "Wetlands protect against floods. Some people think swamps look '
    'ugly. They hold rain." (one off-purpose line, one thin detail)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "Wetlands protect against floods. They soak up heavy rain like a '
    'sponge and release it slowly, so nearby rivers rise less sharply." (off-purpose line deleted, needed detail '
    'added)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1005-0010", grade="9-10", lesson_type=6,
    unit="G10 U3 - Rhetorical revision (add for purpose, delete off purpose)",
    title="Add What the Point Needs, Cut What It Does Not",
    target=("Revise for purpose: add the piece the reader needs to follow the point, and delete the piece that "
            "does not serve it. Written at the sentence. Trait: Organization/Development."),
    acc_tags=["ACC.W.PROC.2", "CCSS.W.9-10.5"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.05", "sot": "icm course-G10.md L10",
                "taught_stimulus": "ACC-W910-INFO-LESSON-WETLANDS",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-HIGHWAYS",
                "playbook": "_phase2/playbook_T6_SPOT.md",
                "template": "v3.1 lesson build spec; REVISION-TIER, material is a provided draft (inline); source bound for authentic context.",
                "one_idea": "Every sentence should serve the point: add what the point needs, cut what does not.",
                "one_reminder": "3-question check: what is the point? does each sentence serve it? cut wanderers, add missing pieces.",
                "version_note": ("V3.1 rebuild of L10 to the v3.1 build spec: TEACH split into one-idea callout + "
                                 "add/delete list (fixes the format_fidelity wall of text); MODEL rebuilt as a "
                                 "coping-model think-aloud with the 3-question check folded in at point of first "
                                 "use; discrimination moved to explicit choices with the 'Grade-C design bet' "
                                 "jargon removed and the true-fact confound broken (DI faultless communication); "
                                 "FRQ + diagnosis bodies use frq_prompt/setapart/checklist (kills the 'Step 1/2' "
                                 "render double-numbering and the 'Scored on' chrome); independent says the "
                                 "standard out loud (Yeager). Teaching point + bound stimuli unchanged."),
                "review_provenance": ("Rebuilt to icm/_config/v3_1-lesson-build-spec.md (the pattern that cleared "
                                      "all 23 lesson_contract gates + the Fable-5 reviewer on G9 v3.1)."),
                "council": ("T6/SPOT rhetorical revision intro: introduces oS1 add-for-purpose + oS2 delete-off-"
                            "purpose (serves-the-point vs does-not). serves-vs-off-purpose discrimination labeled "
                            "Grade-C in code (not in student text). SPOT=proposal; ceiling sentence.")},
    fade_ledger_moves=["add-for-purpose", "delete-off-purpose"],
    slots=[
        # ===== TEACH: ONE idea in a callout + the add/delete contrast as a real LIST (no wall of text) =====
        Slot("TEACH", "teach_card", "Every sentence should serve the point",
             body=(ONE_IDEA +
                   "Revising for purpose means changing a draft so it serves its point better, and two moves do "
                   "most of the work. The test for each sentence is one question: does this help the reader with "
                   "THIS point? Two moves answer it:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>ADD for purpose</strong>: supply the piece a reader needs "
                   "to follow or believe the point, a specific detail, a missing step, or the reason behind a "
                   "claim (adding 'they soak up heavy rain like a sponge' shows HOW wetlands stop floods).</li>"
                   "<li style=\"margin:4px 0\"><strong>DELETE off purpose</strong>: cut a sentence that does not "
                   "serve the point, even when it is true or interesting ('some people think swamps look ugly' is "
                   "true, but it does nothing for a point about flood protection).</li></ul>"
                   "The trap is leaving in a true-but-off-purpose line, or leaving out the one detail that would "
                   "make the point land. Goal: on a provided draft, add what the point needs and delete what it "
                   "does not.")),
        Slot("TEACH", "stimulus_display", "Read the source: what wetlands do",
             ref="ACC-W910-INFO-LESSON-WETLANDS", bank="wetlands",
             body=("Read this explanatory source on wetlands so the topic is familiar. The drafts you revise are "
                   "about wetlands; you will decide what serves a given point and what does not. You are not "
                   "writing about wetlands from scratch here; you are revising a draft that is given to you. The "
                   "text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model think-aloud with the check tool folded in =====
        Slot("MODEL", "annotated_before_after", "Watch a draft get an add and a delete",
             bank="wetlands",
             body=("Here is the skill in action. Follow the writer's revising below. " + COPING_HTML +
                   " Notice the two moves that turned the BEFORE into the AFTER: the writer deleted the sentence "
                   "that did not serve the flood point, and added a detail that showed HOW the protection works. "
                   + REMEMBER +
                   "When you revise a draft of your own, do the same: name the point, cut any sentence that wanders "
                   "off it, and add the piece the reader still needs. Run the 3 questions before you submit.")),
        Slot("MODEL", "discrimination", "Which sentence should be cut?",
             ref="", labeled_grade_c=True, bank="wetlands",
             body=("Now that you have seen one built, spot the target first. The point of this draft is: wetlands "
                   "support wildlife. Which one sentence does NOT serve that point and should be cut? "
                   "(A) Wetlands give fish, birds, and frogs places to feed, hide, and nest.  "
                   "(B) More than one-third of the nation's rarest species live only in wetlands.  "
                   "(C) Much of the country's wetland was drained for farms and roads long ago.  "
                   "(D) Salamanders and turtles also raise their young in the shallow water of the marsh. "
                   "Correct: C. Draining for farms and roads is about land loss, not about supporting wildlife."),
             choices=[
                 {"id": "A", "text": "Wetlands give fish, birds, and frogs places to feed, hide, and nest.",
                  "correct": False,
                  "why": "This sentence names the animals wetlands support and what they do there, so it serves the wildlife point. Keep it."},
                 {"id": "B", "text": "More than one-third of the nation's rarest species live only in wetlands.",
                  "correct": False,
                  "why": "This is a true fact from the source, and it directly supports the point that wetlands support wildlife. Keep it."},
                 {"id": "C", "text": "Much of the country's wetland was drained for farms and roads long ago.",
                  "correct": True,
                  "why": "Correct. This is true, but it is about how wetland was lost, not about supporting wildlife. A true fact that does not serve the point still gets cut."},
                 {"id": "D", "text": "Salamanders and turtles also raise their young in the shallow water of the marsh.",
                  "correct": False,
                  "why": "This looks like it repeats sentence A, so it is tempting to cut it as extra. But it names different animals doing something for the wildlife point, so it serves the point and stays. Deleting on-purpose detail because it feels repetitive is the wrong cut."},
             ]),
        # Second minimal pair: the OTHER move (ADD for purpose). Different confound from the delete pair above:
        # here two options are on-topic wetlands content, but only one supplies the missing HOW the point needs.
        Slot("MODEL", "discrimination", "Which sentence should be added?",
             ref="", labeled_grade_c=True, bank="wetlands",
             body=("Now the other move: adding. The point of this draft is: wetlands protect the shoreline from "
                   "storm waves. The draft names the point but does not yet show the reader HOW. Which sentence, "
                   "if added, best serves that point? "
                   "(A) The plants and soft ground soak up the force of the waves before they reach dry land. "
                   "(B) Wetlands can be found along the coasts, rivers, and lakes in nearly every part of the country, from north to south. "
                   "(C) Storms have become a growing worry for many towns built near the water.  "
                   "(D) This is why wetlands really are so good at protecting the shoreline from storm waves. "
                   "Correct: A. It shows HOW the wetland stops the waves, which is what the point needs."),
             choices=[
                 {"id": "A", "text": "The plants and soft ground soak up the force of the waves before they reach dry land.",
                  "correct": True,
                  "why": "Correct. It shows HOW the wetland stops the waves, so it gives the reader the very piece the point needs."},
                 {"id": "B", "text": "Wetlands can be found along the coasts, rivers, and lakes in nearly every part of the country, from north to south.",
                  "correct": False,
                  "why": "This is true and on topic, but it tells where wetlands are, not how they guard the shore, so it does not serve this point."},
                 {"id": "C", "text": "Storms have become a growing worry for many towns built near the water.",
                  "correct": False,
                  "why": "This sets a mood about storms but never shows how a wetland protects the shore, so the point stays unsupported."},
                 {"id": "D", "text": "This is why wetlands really are so good at protecting the shoreline from storm waves.",
                  "correct": False,
                  "why": "This just restates the point in bigger words; it adds no new information about HOW the wetland stops the waves. Repeating the claim is not the same as adding the piece the point needs."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this draft most need?",
             bank="wetlands",
             body=("Diagnose this draft before the reveal. Point: wetlands clean water. Draft: 'Wetlands clean "
                   "water as it moves slowly through them. The country has lost more than half of its original "
                   "wetlands. The plants take up pollution and the soil traps dirt.' Which single revision would "
                   "most serve the point? "
                   "(A) delete the sentence about how much wetland the country has lost, since it does not serve the cleaning point  "
                   "(B) add the exact number of acres lost so the sentence about wetland loss gives the reader a fuller figure  "
                   "(C) make all three sentences longer so the whole paragraph feels fuller and more fully developed for the reader  "
                   "(D) move the loss sentence to the front so the paragraph opens by saying how much wetland has been lost"),
             feedback=("Correct: A. The point is that wetlands clean water; the loss fact is true but off-purpose "
                       "here, so it should be cut. The other two sentences already serve the point. Adding an "
                       "acreage (B) or length (C) only pads an off-purpose line, and moving it (D) leaves it off "
                       "the point.")),

        # ===== SUPPORTED: framed edit (fill-in frame) on the taught topic (source read at TEACH step 2) =====
        Slot("SUPPORTED", "production_frq", "Revise: one delete, one add",
             ref="", bank="wetlands", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="revision",
             body=frq_prompt(
                 intro="Revise this draft so every sentence serves the point. Point: wetlands protect against "
                       "floods. Draft: 'Wetlands protect against floods. Some people think swamps look ugly. They "
                       "hold rain.'",
                 setapart_block=setapart("Copy this frame, then fill in the blank:",
                                         "Wetlands protect against floods. They ______ [a detail that shows HOW they protect against floods]. (Delete the sentence that does not serve the point.)"),
                 closer="Cut the off-purpose sentence and add one detail that shows HOW wetlands protect against "
                        "floods. Then run the 3-question check: does every sentence now serve the point?")),
        # COUNCIL FIX (2026-07-24): Option B (first-in-arc). Graded recognition + graded fresh-draft rewrite;
        # name-act dropped. The old single diagnosis_frq bundled 3 acts in one box (run a 3-question check as
        # pre-answered (q,a) rows + rewrite + name-which-sentence-you-cut) - unscoreable, wired to no grader,
        # and the (q,a) tuple rows leaked the answers. First diagnosis item in this arc -> two single-act items.
        # Item 1 = graded RECOGNITION on a minimal-pair draft that fails EXACTLY ONE check (single-select is
        # faultless; DI constraint): the draft states its point and shows HOW (so the point-check and the
        # add-check pass), but one true off-purpose sentence wanders (so only the delete-check fails). Item 2 =
        # graded FRESH-draft rewrite, with the 3 questions printed READ-ONLY beneath the prompt. The
        # name-which-sentence-you-cut third act is deleted.
        Slot("MODEL", "discrimination", "Diagnose the draft: which check does it fail?",
             ref="", labeled_grade_c=True, bank="wetlands",
             body=("Run the 3-question check on this draft. Point: wetlands shelter wildlife. Draft: 'Wetlands "
                   "give many animals a place to live. Birds, fish, and frogs feed and nest in the shallow "
                   "water and reeds. Wetlands were once drained for farmland.' It fails exactly one check. "
                   "Which one? "
                   "(A) It never states the point the draft is about.  "
                   "(B) It is missing a detail that shows HOW, so a needed piece must be added.  "
                   "(C) One true sentence does not serve the point and should be deleted.  "
                   "(D) It fails none of the checks; every sentence already serves the point. "
                   "Correct: C. The draft states its point and shows how animals use the wetland, so the "
                   "point-check and the add-check pass. But the last sentence, about wetlands being drained for "
                   "farmland, is true yet off the wildlife point, so only the delete-check fails."),
             choices=[
                 {"id": "A", "text": "It never states the point the draft is about.",
                  "correct": False,
                  "why": "The first sentence states the point clearly: wetlands give animals a place to live. That check passes; look for the one that fails."},
                 {"id": "B", "text": "It is missing a detail that shows HOW, so a needed piece must be added.",
                  "correct": False,
                  "why": "The second sentence already shows how animals use the wetland (they feed and nest in the shallow water and reeds), so no piece needs adding here."},
                 {"id": "C", "text": "One true sentence does not serve the point and should be deleted.",
                  "correct": True,
                  "why": "Correct. The draining-for-farmland line is a true fact, but it does not serve the wildlife point, so it should be cut. A true fact that is off the point still has to go."},
                 {"id": "D", "text": "It fails none of the checks; every sentence already serves the point.",
                  "correct": False,
                  "why": "Not quite. Two sentences serve the point, but the draining-for-farmland line wanders off it, so one check still fails."},
             ]),
        Slot("MODEL", "production_frq", "Now fix a draft: add what is missing",
             ref="", bank="wetlands", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="Here is a different weak draft. Rewrite it so every sentence serves the point.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "Wetlands help protect nearby towns from floods. Wetlands can be found on every continent except Antarctica. They soak up heavy rain and release it slowly, so rivers rise less sharply.", "red"),
                 checklist_block=checklist(title="Check your rewrite against these (no need to type answers):", rows=[
                     "What is the point of this draft?",
                     "Does each sentence help the reader with THAT point?",
                     "Cut any sentence that wanders off the point; add any needed piece that is missing.",
                 ]),
                 closer="The point is that wetlands protect towns from floods. One sentence is a true fact that "
                        "wanders off that point. Rewrite the draft so every sentence serves the flood point. Run "
                        "the 3-question check above before you submit.")),

        # ===== INDEPENDENT: cold edit on the taught topic + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Revise a provided draft on your own",
             ref="", bank="wetlands", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="revision",
             body=frq_prompt(
                 intro="On your own now, no frame. Point: wetlands clean water. Draft: 'Wetlands clean the water "
                       "that flows through them. Wetlands were once seen as wasted ground. The plants and soil "
                       "trap pollution before the water moves on.' Revise so every sentence serves the cleaning "
                       "point: delete the off-purpose sentence, and add a detail if it helps.",
                 closer="Before you submit, check each sentence: does it serve the point? Cut or fix any that does "
                        "not. Adding what the point needs and cutting what it does not is what every clear piece "
                        "of writing is built on, and you are ready to do it without a frame. Run the 3-question "
                        "check before you submit.")),

        # ===== TRANSFER: same move, a NEW topic (highways), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: Building the Interstate Highway System",
             ref="ACC-W910-INFO-LESSON-HIGHWAYS", bank="interstate_highways",
             body=("Read this new source on the Interstate Highway System so the topic is familiar. The draft you "
                   "revise is about highways; you will add what serves the point and delete what does not. Again, "
                   "you are revising a provided draft, not writing from scratch. The text stays on screen while "
                   "you work.")),
        Slot("TRANSFER", "production_frq", "Revise a provided draft on a NEW topic",
             ref="", bank="interstate_highways", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="revision",
             body=frq_prompt(
                 intro="New topic. Point: the interstate system moves goods efficiently. Draft: 'The interstate "
                       "lets trucks cross the country quickly. The first interstates were funded in 1956. This "
                       "keeps store shelves stocked and prices lower.' Revise so every sentence serves the point.",
                 closer="Same add-and-delete move as the wetlands drafts, new topic: delete the sentence that does "
                        "not serve the point, and add a detail if it helps. Run the 3-question check before you "
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
