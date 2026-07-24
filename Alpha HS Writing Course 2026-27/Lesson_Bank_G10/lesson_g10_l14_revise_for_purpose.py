"""
lesson_g10_l14_revise_for_purpose.py  -  G10 KC C.10.05, ARCHETYPE T5: RUBRIC-REVISION (CHECK, paragraph). V3.1.

G10 course L14 (Unit 3 capstone, check), rebuilt to the v3.1 build spec (icm/_config/v3_1-lesson-build-spec.md)
from the pre-v3.1 prose-wall version. Teaching point (KEPT): revise a PROVIDED paragraph for purpose by combining
the moves (ADD what the point needs, DELETE what is off-purpose, REORDER so it builds), then self-check the
result. REVISION-TIER, provided drafts; source bound for context. KC C.10.05. Bound stimuli KEPT: WETLANDS
(taught) -> RECYCLING (transfer, bank-partitioned). rc.staar, unit="paragraph" (T5 ceiling). CHECK=proposal.

V3.1 changes over the pre-v3.1 L14 (all prior gate failures fixed):
  1. TEACH is now ONE idea, hammered: a teal ONE_IDEA callout + the three combined moves as a real <ul> list
     (was two prose teach cards). "purpose" and "off-purpose line" defined with "means"/"is a" cues.
  2. MODEL is a coping-model think-aloud: a writer drafts, fixes only the obvious problem (FIRST TRY), runs the
     check, catches the other two gaps (SECOND TRY), then applies all three moves (FINAL), with a literal BEFORE
     and AFTER inline. The reusable check tool folds in as a REMEMBER dashed box (a real 3-question <ol>).
  3. NO leaked internal labels: dropped the old "a Grade-C design bet we label as a bet" prose. Discrimination
     now uses explicit choices=[{id,text,correct,why}] with the correct option NOT the lone-longest, and the move
     words add/delete appear in a WRONG distractor too, so the served purpose (not a surface token) is the
     invariant. Reveal sits in a "Correct: B ..." tail, not in an option label.
  4. FRQ + diagnosis bodies built with frq_prompt/setapart/checklist (no "Step 1/2" prose, no "Scored on"
     chrome). self_score is a clean predict-the-score MCQ. Own words, faithful to the bound federal source, no
     fabricated figures, no em dashes.
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
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Revising for purpose is not fixing one thing and stopping. '
'It is walking the <strong>whole draft</strong> and making <strong>every sentence serve the point</strong>, using '
'add, delete, and reorder together.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: run it on any draft</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you call a paragraph done, ask these observable yes/no questions:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0"><strong>Serve the purpose?</strong> Does every sentence help make the point? Delete any that wander.</li>'
'<li style="margin:2px 0"><strong>Missing detail?</strong> Is the one detail the point needs actually there? Add it if it is not.</li>'
'<li style="margin:2px 0"><strong>Order builds?</strong> Does the point lead and the support follow it? Reorder if it does not.</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">A draft that made sense to the writer often hides these gaps, so run the check even when it feels finished.</div></div>')

# coping-model before/after panel: a flood-protection draft with all three problems, revised with all three moves.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> an off-purpose line, a weak order, and a missing detail</span>'
    '<p style="margin:8px 0 0;font-size:15px">Wetlands are found worldwide. They protect against floods by '
    'holding water. Swamps can smell bad. This is why coastal towns value them.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The smell line is off-purpose (delete), the flood '
    'point buries under the worldwide line (reorder), and the flood claim has no concrete detail (add).</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> add, delete, and reorder, all serving the purpose</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">POINT FIRST</span> Coastal towns value wetlands for flood protection. '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">ADDED DETAIL</span> A healthy wetland acts like a giant sponge, soaking up heavy rain '
      'and river overflow and then releasing the water slowly, so the flood downstream is smaller.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">The off-purpose smell line is cut, the flood point '
    'leads, and one specific detail is added. All three moves serve the flood-protection purpose.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1005-0014", grade="9-10", lesson_type=5,
    unit="G10 U3 - Rhetorical revision (revise a draft for purpose)",
    title="Revise a Whole Draft for Its Purpose",
    target=("Revise a provided paragraph for purpose by combining the moves: add what the point needs, delete "
            "what is off-purpose, and reorder so it builds, then self-check the result. Written at the "
            "paragraph. Trait: Organization/Development."),
    acc_tags=["ACC.W.PROC.2", "CCSS.W.9-10.5"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.05", "sot": "icm course-G10.md L14",
                "taught_stimulus": "ACC-W910-INFO-LESSON-WETLANDS",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-RECYCLING",
                "one_idea": "Revising for purpose is walking the whole draft and making every sentence serve the point, using add, delete, and reorder together.",
                "one_reminder": "Run the check: serve the purpose? missing detail? order builds?",
                "playbook": "_phase2/playbook_T5_CHECK.md",
                "template": "locked L01 template; REVISION-TIER, provided drafts; source bound for context.",
                "version_note": ("V3.1 rebuild of the pre-v3.1 prose-wall L14 to the v3.1 build spec, structured "
                                 "on the G9 L25 T5 template. Fixed the prior gate failures: (a) TEACH is now one "
                                 "hammered idea (ONE_IDEA callout + the three combined moves as a <ul>), was two "
                                 "prose teach cards; (b) MODEL is a coping-model think-aloud (first try fixes only "
                                 "the obvious problem, the check catches the rest, the final applies all three "
                                 "moves) with a literal BEFORE + AFTER and the check tool folded in as a REMEMBER "
                                 "<ol>; (c) dropped the leaked 'Grade-C design bet we label as a bet' prose, the "
                                 "discrimination now uses explicit choices with the correct option NOT the lone-"
                                 "longest and add/delete appearing in a wrong distractor to break the token "
                                 "confound; (d) FRQ + diagnosis built with frq_prompt/setapart/checklist, self_"
                                 "score is a clean predict-the-score MCQ. Kept bound stimuli + every production "
                                 "unit='paragraph' (T5 ceiling)."),
                "council": ("T5/CHECK Unit-3 capstone: revise a provided draft for purpose (oS1 add + oS2 delete "
                            "+ O1 order) with R1 revise-anchor + K1 predict-then-reveal. purpose-served-vs-not "
                            "discrimination labeled Grade-C in code. self_score calibration. CHECK=proposal; T5 "
                            "ceiling paragraph, so every scored revision is a paragraph-level fix."),
                "review_provenance": "built to the G9 L25 v3.1 T5 pattern (icm/_config/v3_1-lesson-build-spec.md)."},
    fade_ledger_moves=["revise-for-purpose-combined", "add-delete-reorder"],
    slots=[
        # ===== TEACH: ONE idea, hammered (callout + the three combined moves as a list) =====
        Slot("TEACH", "teach_card", "The one idea: make every sentence serve the point",
             body=(ONE_IDEA +
                   "A paragraph's purpose means the single point it exists to make. An off-purpose line is a "
                   "sentence that does not help make that point. Revising for purpose is deciding what the "
                   "paragraph is trying to do, then working through it with three moves together:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Add</strong> the one specific detail the point needs to "
                   "land.</li>"
                   "<li style=\"margin:4px 0\"><strong>Delete</strong> any line that does not serve the point.</li>"
                   "<li style=\"margin:4px 0\"><strong>Reorder</strong> so the point leads and the support "
                   "builds behind it.</li></ul>"
                   "You already know each move on its own. The trap in real revision is fixing only the most "
                   "obvious problem and leaving the other two. Today you combine all three on one draft, then "
                   "check that every sentence now serves the purpose.")),
        Slot("TEACH", "stimulus_display", "Read the source: what wetlands do",
             ref="ACC-W910-INFO-LESSON-WETLANDS", bank="wetlands", tag="buy_in",
             body=("The provided drafts you revise are about wetlands. Read this source so the topic is "
                   "familiar. You are not writing a wetlands essay from scratch here; you are revising drafts "
                   "that are given to you. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + the check tool at point of first use =====
        Slot("MODEL", "annotated_before_after", "Watch a writer revise a whole draft for its purpose",
             bank="wetlands",
             body=("Watch a writer revise a flood-protection paragraph. FIRST TRY: they spot the obvious problem, "
                   "the smell line, delete it, and stop, thinking they are done. Running the check catches two "
                   "more gaps: the flood point is buried under the worldwide line (order), and the flood claim "
                   "has no concrete detail (add). SECOND TRY: they move the flood point to the front and cut the "
                   "smell line, but the detail is still thin. FINAL: they add one specific detail on how a "
                   "wetland holds and slowly releases water. Read the BEFORE, then the AFTER." + BEFORE_AFTER_HTML +
                   " Combining all three moves, not just the easy one, is the revision. " + REMEMBER +
                   "When you revise a draft, run this check, then reread once more.")),
        Slot("MODEL", "discrimination", "Which revision served the purpose?",
             ref="", labeled_grade_c=True, bank="wetlands",
             body=("Spot the target before you revise. Purpose: explain why coastal towns value wetlands for "
                   "flood protection. Which revision served that purpose? "
                   "(A) The writer corrected the spelling mistakes, fixed the punctuation, and combined the "
                   "short choppy sentences into longer, smoother ones so the whole paragraph reads better.  "
                   "(B) The writer cut the off-purpose smell line, added a detail on how a wetland holds and "
                   "slowly releases water, and moved the flood point to the front.  "
                   "(C) The writer deleted the flood-protection point and added two new sentences about how "
                   "pretty marshes look in spring, giving the paragraph more colorful description.  "
                   "(D) The writer deleted the off-purpose smell line and then stopped there, so the flood point "
                   "still trails at the end and no detail on how wetlands hold back floods was ever added. "
                   "Correct: B. (A) polishes surface features but leaves the off-purpose line, the missing "
                   "detail, and the weak order. (C) uses delete and add, but on the wrong material, cutting the "
                   "very point and padding with off-purpose description. (D) makes the right first move but stops "
                   "at one, leaving the missing detail and the weak order untouched. Only (B) applies all three "
                   "moves so every sentence serves the flood-protection purpose."),
             choices=[
                 {"id": "A", "text": "The writer corrected the spelling mistakes, fixed the punctuation, and combined the short choppy sentences into longer, smoother ones so the whole paragraph reads better.",
                  "correct": False,
                  "why": "This polishes surface features but leaves the off-purpose smell line, the missing flood detail, and the weak order. A cleaner-reading paragraph that still does not serve the purpose has not been revised for purpose."},
                 {"id": "B", "text": "The writer cut the off-purpose smell line, added a detail on how a wetland holds and slowly releases water, and moved the flood point to the front.",
                  "correct": True,
                  "why": "Correct. All three moves land on the right material: the off-purpose line is deleted, the specific flood detail is added, and the point leads. Every sentence now serves the flood-protection purpose."},
                 {"id": "C", "text": "The writer deleted the flood-protection point and added two new sentences about how pretty marshes look in spring, giving the paragraph more colorful description.",
                  "correct": False,
                  "why": "This uses delete and add, the right moves, but on the wrong material: it cuts the very point the paragraph exists to make and pads it with off-purpose description. The moves only count when they serve the purpose."},
                 {"id": "D", "text": "The writer deleted the off-purpose smell line and then stopped there, so the flood point still trails at the end and no detail on how wetlands hold back floods was ever added.",
                  "correct": False,
                  "why": "This fixes only the most obvious problem and stops. The off-purpose line is gone, but the missing detail and the weak order remain, so the paragraph is not yet revised for purpose. Combining all three moves is the revision."},
             ]),
        Slot("MODEL", "predict_the_fix", "What set of moves does this draft need?",
             bank="wetlands",
             body=("Diagnose before the reveal. Purpose: explain how wetlands clean water. Draft: 'Wetlands are "
                   "pretty in spring. Water passes through wetlands. Wetlands trap pollutants in the mud and "
                   "plants.' Which set of moves best serves that purpose? "
                   "(A) delete the off-purpose 'pretty in spring' line, and reorder so 'water passes through' "
                   "leads into 'traps pollutants'  "
                   "(B) add two more sentences describing how pretty the wetlands look in spring, with details "
                   "about the flowers and the birds that visit  "
                   "(C) rewrite every sentence so they are all about the same length and match in style, with "
                   "the wording kept smooth and even throughout  "
                   "(D) change the word 'wetlands' to 'marshes' every single time it appears so the naming stays "
                   "consistent all the way through the paragraph"),
             feedback=("Correct: A. The purpose is to explain cleaning, so the beauty line is off-purpose "
                       "(delete), and the process reads in order as water-passes-through then traps-pollutants "
                       "(reorder). More beauty sentences (B), uniform length (C), or a word swap (D) do not "
                       "serve the cleaning purpose.")),

        # ===== SUPPORTED: predict the score (calibration MCQ) -> then revise the draft (frame + checklist) =====
        Slot("SUPPORTED", "self_score", "Predict the score, then see the verdict",
             ref="", bank="wetlands",
             body=("Predict, then reveal. A student revised the flood-protection draft to: 'Wetlands are found "
                   "worldwide. They protect against floods. Swamps can smell bad sometimes.' On a 2-point scale "
                   "(2 = off-purpose line cut, needed detail added, order builds; 1 = problems remain), what "
                   "score does this earn?"),
             choices=[
                 {"id": "1", "text": "1 out of 2", "correct": True,
                  "why": "Correct. The revision kept the off-purpose smell line, added no flood detail, and still "
                         "leads with the worldwide line, so the purpose is not served. A 2 would cut the smell "
                         "line, add a specific flood detail, and put the flood point first."},
                 {"id": "2", "text": "2 out of 2", "correct": False,
                  "why": "A 2 needs all three moves. This draft only changed a little: the smell line is still "
                         "there, no flood detail was added, and the order still buries the point. Notice how a "
                         "lightly-changed draft can look revised without being fixed."},
             ]),
        Slot("SUPPORTED", "production_frq", "Revise the draft for purpose",
             ref="", bank="wetlands", rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="revision",
             body=frq_prompt(
                 intro="Purpose: explain why coastal towns value wetlands for flood protection. Revise the draft "
                       "below by combining all three moves.",
                 setapart_block=setapart("Draft to revise:",
                                         "Wetlands are found worldwide. They protect against floods by holding water. Swamps can smell bad. This is why coastal towns value them."),
                 checklist_block=checklist(title="Use this check:", rows=[
                     "Delete the off-purpose line that does not serve flood protection.",
                     "Add one specific detail on HOW wetlands reduce floods (the source describes a sponge that soaks up water and releases it slowly).",
                     "Reorder so the flood point leads and the support builds behind it.",
                 ]),
                 closer="Rewrite the whole paragraph with all three moves applied.")),
        # COUNCIL FIX (2026-07-24): Option A (later-in-arc), watch-then-do: demo preserved, produce is the graded
        # act. The old diagnosis_frq bundled a watched purpose-check demo (pre-answered (q,a) tuple rows) + a
        # fresh paragraph + a run-and-name-which-move tail in one box (unscoreable, wired to no grader, and the
        # (q,a) rows leaked the answers). The coping-model demo is PRESERVED as read-only narration (the three
        # purpose questions shown running on the weak draft, in plain declarative prose). The student's ONLY
        # graded act is now the fresh paragraph; the three checks sit read-only beneath as plain-string
        # reminders; the run-and-name tail is deleted. Stays on the taught topic (no new source).
        Slot("MODEL", "diagnosis_frq", "Write a fresh draft that serves the purpose",
             ref="", bank="wetlands", rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="First, watch the purpose check run on the weak draft below. Purpose: explain how wetlands "
                       "shelter wildlife. The land-area line and the legal line wander from the shelter point, so "
                       "they would be cut; one specific detail on the shelter is missing, such as which animals "
                       "feed, hide, or breed there; and once the wandering lines are gone the paragraph should "
                       "lead with the shelter point and let the detail follow. Now write a fresh paragraph of "
                       "your own that does not need those fixes.",
                 setapart_block=setapart("Weak draft the check was run on:",
                                         "Wetlands cover little land. They give birds and fish food and nesting spots. Some are protected by law.", "red"),
                 checklist_block=checklist(title="Check your paragraph against these (no need to type answers):", rows=[
                     "Serve the purpose? Every sentence works toward the shelter point.",
                     "Missing detail? One specific detail names which animals feed, hide, or breed there.",
                     "Order builds? It leads with the shelter point, then the supporting detail follows.",
                 ]),
                 closer="Write a fresh short paragraph explaining how wetlands shelter wildlife, with every "
                        "sentence serving that purpose, one specific shelter detail included, and an order that "
                        "builds. Run the three questions above before you submit.")),

        # ===== INDEPENDENT: revise a PROVIDED draft with no checklist scaffold + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Revise a provided draft on your own",
             ref="", bank="wetlands", rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="revision",
             body=frq_prompt(
                 intro="On your own now, no checklist. Purpose: explain how wetlands clean water. Revise the "
                       "draft below by combining the moves.",
                 setapart_block=setapart("Draft to revise:",
                                         "Wetlands look nice in photos. Water flows through them. They cover part of the country. Plants and mud trap pollution as the water passes."),
                 closer="Delete any off-purpose line, add a detail if the cleaning point needs one, and reorder "
                        "so it builds. Then check: does every sentence serve the cleaning purpose, and does the "
                        "order build? This combined revision is what every real revision for purpose is built "
                        "on, and you are ready to do it cold.")),

        # ===== TRANSFER: same combined-revision move, a NEW topic (recycling), bank-partitioned =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: how recycling works",
             ref="ACC-W910-INFO-LESSON-RECYCLING", bank="recycling",
             body=("The next draft to revise is about recycling. Read this new source so the topic is familiar. "
                   "Again, you are revising a draft that is given to you, then checking your revision. The text "
                   "stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Revise a provided draft on a NEW topic",
             ref="", bank="recycling", rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="revision",
             body=frq_prompt(
                 intro="New topic, same move. Purpose: explain how materials recovery turns old material into new "
                       "products. Revise the draft below by combining the moves.",
                 setapart_block=setapart("Draft to revise:",
                                         "Recycling bins come in many colors. Trucks collect the bottles. Recycling has grown over the years. Machines and factories sort the material and remake it into new goods."),
                 closer="Delete any off-purpose line, add a detail if the recovery point needs one (the source "
                        "describes sorting on conveyor belts and baling before factories remake it), and reorder "
                        "so it builds. Then check: serve the purpose? missing detail? order builds? Same combined "
                        "revision as the wetlands drafts, on a new topic.")),
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
