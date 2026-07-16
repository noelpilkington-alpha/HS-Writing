"""
lesson_g10_l26_precision_pass.py  -  G10 KC C.10.04, ARCHETYPE T5: RUBRIC-REVISION (CHECK, paragraph). V3.1.

NEW G10 L26, authored to the v3.1 build spec (icm/_config/v3_1-lesson-build-spec.md), added per the design
audit. STRUCTURE mirrors the G9 v3.1 template lesson_g9_l25_essay_revision_v3_1.py (same T5 archetype); the
CONTENT is fresh for THIS skill.

Teaching point (C.10.04, the woven precision-in-argument revision pass): revise a provided argument/analysis
draft for PRECISION without changing the position. Run three moves: (1) replace a vague or overreaching claim
word with an exact one, (2) cut a hedge or an empty intensifier that weakens the point, (3) tighten one loose
sentence. Then run the same precision pass on your own draft. STATELESS-LEGAL: every scored write is a fresh,
self-contained piece written in the box, never a prior-draft look-back.

Bound stimuli: WETLANDS (taught) -> HIGHWAYS (transfer, bank-partitioned). rc.staar (G10). unit="paragraph"
(T5 ceiling). mnemonic_status="proposal" (T5/CHECK). Every figure faithful to the bound federal-sourced
passages. No em dashes, no named HTML entities, inline styles only.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A precision pass keeps your <strong>position</strong> and '
'sharpens your <strong>words</strong>. You swap vague or overreaching words for exact ones, cut the hedges and '
'empty intensifiers, and tighten one loose sentence. You never switch sides.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your precision pass: run it on any draft</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit an argument, run these four checks:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0"><strong>Vague or overreaching word?</strong> Swap it for the exact function the source names.</li>'
'<li style="margin:2px 0"><strong>Hedge or empty intensifier?</strong> Cut it.</li>'
'<li style="margin:2px 0"><strong>Loose sentence?</strong> Tighten it to one exact, complete statement.</li>'
'<li style="margin:2px 0"><strong>Same position?</strong> A precision pass sharpens words, it never switches sides.</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">Vague and puffed-up wording feels strong to the writer but reads as weak to a scorer, so run the pass even when a draft feels finished.</div></div>')

# coping-model before/after: an overreaching, hedged, loose claim, revised to exact wording (position unchanged).
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> vague, hedged, and loose</span>'
    '<p style="margin:8px 0 0;font-size:15px">Wetlands are honestly one of the most important things on the '
    'entire planet, and they basically help with all kinds of environmental problems and stuff.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The position (wetlands matter) is fine, but the '
    'words are not: "one of the most important things on the entire planet" overreaches, "honestly" adds heat '
    'but no meaning, "basically" is a hedge, and the sentence trails off at "and stuff."</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> same position, exact words</span>'
    '<p style="margin:8px 0 0;font-size:15px">Wetlands are worth protecting because they '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;'
      'font-weight:700">store floodwater</span>. The EPA notes that one stretch of the '
      'Mississippi River once held 60 days of floodwater but could store only 12 days after most nearby '
      'wetlands were drained.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Three edits, same side of the argument: the '
    'overreaching phrase became the exact function the source names (store floodwater), the empty word '
    '("honestly") and the hedge ("basically") were cut, and the loose "and stuff" sentence was tightened into '
    'one sourced statement.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1004-0026", grade="9-10", lesson_type=5,
    unit="G10 U4 - Precision-in-argument (applied revision pass, woven)",
    title="Run a Precision Pass on Your Argument",
    target=("Revise a provided argument draft for precision without changing the position: replace a vague or "
            "overreaching claim word with an exact one, cut a hedge or empty intensifier, and tighten one loose "
            "sentence. Then run the precision pass on your own draft. Written at the paragraph. Trait: "
            "Language/Precision."),
    acc_tags=["ACC.W.PROC.2", "CCSS.W.9-10.4", "CCSS.W.9-10.5"],
    provenance={"copyright": "own_authored", "authored": "2026-07-14",
                "mnemonic_status": "proposal", "kc": "C.10.04",
                "unit-context": "G10 U4 - Precision-in-argument (applied revision pass, woven)",
                "taught_stimulus": "ACC-W910-INFO-LESSON-WETLANDS",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-HIGHWAYS",
                "one_idea": ("A precision pass keeps your position and sharpens your words: swap vague or "
                             "overreaching words for exact ones, cut hedges and empty intensifiers, tighten one "
                             "loose sentence."),
                "one_reminder": ("Run the precision pass: vague/overreaching word? hedge/empty intensifier? "
                                 "loose sentence? same position?"),
                "version_note": ("NEW lesson added per the design audit (the woven C.10.04 precision-in-argument "
                                 "revision pass was missing from the G10 bank). Authored to the v3.1 build spec "
                                 "using the G9 L25 T5 rubric-revision lesson as the STRUCTURAL template; content is "
                                 "fresh for the precision skill. STATELESS-LEGAL: revise a PROVIDED draft + run the "
                                 "same pass on a fresh self-contained piece, never a prior-draft look-back. Bound "
                                 "WETLANDS (taught) -> HIGHWAYS (transfer, bank-partitioned); rc.staar; every "
                                 "production unit='paragraph' (T5 ceiling)."),
                "review_provenance": "built to the G9 L25 v3.1 T5 pattern (icm/_config/v3_1-lesson-build-spec.md)."},
    fade_ledger_moves=["precision-pass-on-provided-draft", "precision-pass-self-check-own-draft"],
    slots=[
        # ===== TEACH: ONE idea, hammered (callout + the three precision moves as a real list) =====
        Slot("TEACH", "teach_card", "The one idea: sharpen the words, keep the position",
             body=(ONE_IDEA +
                   "A precise argument names exactly what the source shows and cuts words that add heat but no "
                   "meaning. Running a precision pass means making three targeted edits and nothing more. Watch "
                   "for these three fixes:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Replace a vague or overreaching word with an exact one.</strong> "
                   "A vague word (like \"important\" or \"helps\") names nothing specific. An overreaching word (like "
                   "\"everything\" or \"always\") claims more than the source shows. Swap it for the exact function "
                   "the source names.</li>"
                   "<li style=\"margin:4px 0\"><strong>Cut a hedge or an empty intensifier.</strong> A hedge is a "
                   "word that softens a claim so it commits to less, such as \"kind of,\" \"probably,\" or \"in my "
                   "opinion.\" An empty intensifier is a word that adds heat but no information, such as \"very,\" "
                   "\"really,\" or \"super.\"</li>"
                   "<li style=\"margin:4px 0\"><strong>Tighten one loose sentence.</strong> A loose sentence "
                   "wanders or trails off (\"and stuff,\" long strings of \"and\"). Rewrite it as one exact, "
                   "complete statement.</li></ul>"
                   "The rule that guards all three: keep the position. A precision pass changes the words, never "
                   "the side you argue. You will first practice on PROVIDED drafts, then run the same pass on a "
                   "draft you write here.")),
        Slot("TEACH", "stimulus_display", "The topic: wetlands",
             ref="ACC-W910-INFO-LESSON-WETLANDS", bank="wetlands",
             body=("The provided drafts you revise are about wetlands. Read this short orientation so the topic is "
                   "familiar. A wetland is land where water covers the soil for much of the year, and the source "
                   "reports that wetlands store floodwater (one Mississippi River stretch once held 60 days of it, "
                   "then only 12 after draining), clean water, and shelter more than one-third of the country's "
                   "threatened and endangered species. You are not writing a wetlands essay from scratch here; you "
                   "are running a precision pass on drafts that are given to you.")),

        # ===== MODEL (before the quiz): before/after worked example + the precision pass at point of first use =====
        Slot("MODEL", "annotated_before_after", "Watch a claim get a precision pass",
             bank="wetlands",
             body=("Here is the skill in action. Read the BEFORE, then the AFTER, and notice that the position "
                   "never changes, only the words." + BEFORE_AFTER_HTML +
                   " The BEFORE argues the right side with fuzzy, puffed-up words; the AFTER argues the same side "
                   "with exact ones. Sharpening the words is the precision pass. " + REMEMBER +
                   "When you revise, run this pass, then reread once more.")),
        Slot("MODEL", "discrimination", "Which revision is a precision pass?",
             ref="", labeled_grade_c=True, bank="wetlands",
             body=("Spot the real move before you revise. A provided sentence reads: \"Wetlands are extremely "
                   "important and really help the whole planet in every possible way.\" The position (wetlands are "
                   "valuable) is fine, but the words are vague, overreaching, and puffed up. Which revision is a "
                   "precision pass? "
                   "(A) Rewrite the claim to say that wetlands are the single most important landscape anywhere on "
                   "the entire planet, because a bolder and bigger claim will make the whole sentence land much "
                   "harder with the reader.  "
                   "(B) Cut 'extremely' and 'really,' and replace 'help the whole planet in every possible way' "
                   "with an exact function the source names, such as storing floodwater and sheltering rare "
                   "wildlife.  "
                   "(C) Leave the wording as it is but attach three more facts from the source, since a sentence "
                   "carrying more detail overall will read as more precise. "
                   "Correct: B."),
             choices=[
                 {"id": "A", "text": "Rewrite the claim to say that wetlands are the single most important landscape anywhere on the entire planet, because a bolder and bigger claim will make the whole sentence land much harder with the reader.",
                  "correct": False,
                  "why": "This goes the wrong way: 'the single most important landscape anywhere on the entire planet' overreaches even further than the original. A precision pass narrows an overreaching word to what the source shows; it does not inflate it. Notice the word 'because' here sits on a reason to overreach, not on a precise claim."},
                 {"id": "B", "text": "Cut 'extremely' and 'really,' and replace 'help the whole planet in every possible way' with an exact function the source names, such as storing floodwater and sheltering rare wildlife.",
                  "correct": True,
                  "why": "Correct. This runs the pass: it cuts the empty intensifiers ('extremely,' 'really') and swaps the vague, overreaching phrase for the exact functions the source names, all while keeping the same position."},
                 {"id": "C", "text": "Leave the wording as it is but attach three more facts from the source, since a sentence carrying more detail overall will read as more precise.",
                  "correct": False,
                  "why": "Adding facts is not a precision pass. The vague, overreaching, puffed-up words are still there, so the sentence is longer but no more exact. Precision comes from sharpening the words you have, not piling on more."},
             ]),
        Slot("MODEL", "predict_the_fix", "What is the precision fix for this sentence?",
             bank="wetlands",
             body=("Predict before the reveal. A provided sentence reads: 'The source basically shows that "
                   "wetlands are, in my opinion, probably one of the most useful things nature has ever made.' "
                   "Which single edit runs the precision pass? "
                   "(A) Cut the hedges ('basically,' 'in my opinion,' 'probably') and replace the vague phrase "
                   "with an exact claim the source supports, such as that wetlands store floodwater and clean it.  "
                   "(B) Add more and more praise for wetlands all the way through the sentence, so the reader can "
                   "really feel just how remarkable, valuable, and one of a kind these muddy wet places have "
                   "always truly been.  "
                   "(C) Make the sentence much longer by listing every single job that wetlands do, one after "
                   "another, all inside one continuous sentence.  "
                   "(D) Replace the word 'useful' with the word 'amazing' to give the whole sentence a stronger "
                   "and far more exciting overall feeling."),
             feedback=("Correct: A. The sentence hedges three times ('basically,' 'in my opinion,' 'probably') "
                       "and stays vague ('one of the most useful things nature has ever made'). Cutting the "
                       "hedges and naming an exact function the source supports is the precision pass. More praise "
                       "(B), a longer list-sentence (C), or a hotter word like 'amazing' (D) all leave the "
                       "vagueness and the hedging in place.")),

        # ===== SUPPORTED: predict the score (calibration MCQ) -> then run the pass on the SAME draft =====
        Slot("SUPPORTED", "self_score", "Predict the score, then see the real score",
             ref="", bank="wetlands",
             body=("Predict, then reveal. A provided sentence reads: 'Wetlands are really very important, and "
                   "they basically save the environment.' On a 2-point precision rubric (2 = exact wording with "
                   "no hedges or empty intensifiers and a clear position; 1 = a vague or overreaching word or a "
                   "hedge still remains), what score does this sentence earn?"),
             choices=[
                 {"id": "1", "text": "1 out of 2", "correct": True,
                  "why": "Correct. The position is clear, but the words are not exact: 'really very' stacks two "
                         "empty intensifiers, 'basically' is a hedge, and 'save the environment' overreaches "
                         "past what the source shows. A 2 would cut those and name an exact function (for example, "
                         "that wetlands store floodwater and shelter rare wildlife)."},
                 {"id": "2", "text": "2 out of 2", "correct": False,
                  "why": "A 2 needs exact wording. This sentence still carries empty intensifiers ('really very'), "
                         "a hedge ('basically'), and an overreaching claim ('save the environment'). Notice how a "
                         "sentence can feel strong while its words stay vague."},
             ]),
        Slot("SUPPORTED", "production_frq", "Run a precision pass on the provided draft",
             ref="", bank="wetlands", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="Run a precision pass on the paragraph below. Keep the position (wetlands matter and are "
                       "worth protecting); sharpen the words.",
                 setapart_block=setapart("Paragraph to revise:",
                                         "Wetlands are honestly one of the most important things on the entire planet. They really help with all kinds of environmental problems. Basically, everyone should care about them a lot."),
                 checklist_block=checklist(title="Run the pass:", rows=[
                     "Replace the overreaching 'one of the most important things on the entire planet' with an exact claim the source supports (for example, that wetlands store floodwater or shelter rare wildlife).",
                     "Cut the hedges and empty intensifiers ('honestly,' 'really,' 'basically,' 'a lot').",
                     "Tighten the loose sentences into exact, complete statements.",
                 ]),
                 closer="Rewrite the whole paragraph with the words sharpened and the position unchanged.")),
        # DIAGNOSIS: watch the pass run on a provided draft, then run it on a fresh piece written here
        # (stateless-safe; the material is provided, and the self-check is on the same fresh item).
        Slot("MODEL", "diagnosis_frq", "Self-check a fresh draft with the precision pass",
             ref="", bank="wetlands", scored=True,
             body=frq_prompt(
                 intro="First watch the precision pass run on a provided sentence, then run it on a fresh "
                       "argument you write here.",
                 setapart_block=setapart("Provided sentence to check:",
                                         "Wetlands are super important and stuff.", "red"),
                 checklist_block=checklist(title="Run the precision pass:", rows=[
                     ("Vague or overreaching word?", "Yes. 'important and stuff' names no exact function. Replace it with what the source says wetlands do, such as store floodwater."),
                     ("Hedge or empty intensifier?", "Yes. 'super' adds heat, not meaning. Cut it."),
                     ("Loose sentence?", "Yes. 'and stuff' trails off. Tighten it to one exact, complete statement."),
                 ]),
                 closer="Now write a fresh argument sentence or two about wetlands here, then run the same three "
                        "questions on it: vague or overreaching word? hedge or empty intensifier? loose sentence? "
                        "For each Yes, make the fix, and finish by naming which of the three edits you had to "
                        "make.")),

        # ===== INDEPENDENT: run the pass on a PROVIDED draft with no checklist scaffold + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Run the precision pass on your own",
             ref="", bank="wetlands", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="On your own now, no checklist. Run a precision pass on the paragraph below.",
                 setapart_block=setapart("Paragraph to revise:",
                                         "Wetlands are extremely valuable, and honestly losing them is a really big deal for the whole country. They basically do everything."),
                 closer="Replace each vague or overreaching word with an exact one the source supports, cut every "
                        "hedge and empty intensifier, and tighten the loose sentences, all without changing the "
                        "position. Say the standard: a precise argument names exact functions and cuts words that "
                        "add heat but no meaning. You are ready to run this pass cold.")),

        # ===== TRANSFER: same precision pass, a NEW topic (interstate highways), bank-partitioned =====
        Slot("TRANSFER", "stimulus_display", "The topic: interstate highways",
             ref="ACC-W910-INFO-LESSON-HIGHWAYS", bank="highways",
             body=("The next provided draft to revise is about the Interstate Highway System. Read this short "
                   "orientation so the topic is familiar. The source reports that a 1956 law launched the system, "
                   "that it now runs about 46,876 miles, that the federal government paid 90 percent of the "
                   "construction cost, and that about one quarter of all miles driven in the country happen on it. "
                   "Again, you are running a precision pass on a draft that is given to you.")),
        Slot("TRANSFER", "production_frq", "Run a precision pass on a NEW topic",
             ref="", bank="highways", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="New topic, same move. Run a precision pass on the paragraph below.",
                 setapart_block=setapart("Paragraph to revise:",
                                         "The interstate highway system is honestly one of the most amazing things America has ever built, and it basically changed everything about how people live."),
                 closer="Replace the vague or overreaching words with exact ones the source supports (for "
                        "example, that the system runs about 46,876 miles or carries about one quarter of the "
                        "country's driving), cut the hedges and empty intensifiers, and tighten the loose "
                        "sentence, all without changing the position. Same precision pass as the wetlands drafts, "
                        "on a new topic.")),
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
