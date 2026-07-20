"""
lesson_g10_l09_analysis_check.py  -  G10 KC C.10.03, ARCHETYPE T5: RUBRIC-REVISION (CHECK, paragraph). V3.1.

G10 course L09 (Unit 2, check), rebuilt to the v3.1 build spec (icm/_config/v3_1-lesson-build-spec.md), from
the pre-v3.1 lesson_g10_l09_analysis_check.py. Teaching point (KEPT): judge whether a PROVIDED paragraph analyzes
(device, effect, warrant) or only summarizes, predict its score, see the reveal, then revise a summary paragraph
into analysis, plus a faultless self-check on a fresh paragraph the student writes here. STATELESS-LEGAL: work on
PROVIDED anchors + a self-check on one own submission, never a prior-draft look-back. KC C.10.03. Bound stimuli
KEPT: ACC-W910-INFO-LESSON-WEATHER (taught) -> ACC-W910-INFO-LESSON-WETLANDS (transfer, bank-partitioned).
rc.staar, unit="paragraph" (T5 ceiling). CHECK=proposal.

V3.1 changes over the prior L09 (all prior gate failures fixed):
  1. TEACH is now ONE idea, hammered: a teal ONE_IDEA callout + the analysis-vs-summary tells as a real <ul>
     list (was two >45-word prose teach cards that failed format_fidelity as walls of text). The
     check-predict-reveal-revise routine moved to the REMEMBER check tool at the model card (point of first
     use), not cold up front.
  2. NO leaked internal labels: the old discrimination prose said "a Grade-C design bet we label as a bet"
     (leaked_internal_label failed). Removed; the discrimination now uses explicit choices=[{id,text,correct,
     why}] with the correct option NOT the lone-longest, and 'the author' carried on BOTH options so naming a
     CHOICE, not a surface token, is the invariant (DI faultless communication). labeled_grade_c=True kept in
     code only.
  3. FRQ + diagnosis bodies built with frq_prompt / setapart / checklist (no "Step 1/2" prose, no "Scored on"
     chrome). The provided paragraph to revise sits in a setapart(...) block each time.
  4. self_score is a clean predict-the-score MCQ (short prompt + choices carrying the reveal), not a prose
     block. "warrant" defined with an "is a" cue in TEACH (define-before-use). Coping before/after kept
     (literal BEFORE + AFTER inline). Own words, faithful to the bound source, no fabricated figures, no em
     dashes.
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
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A paragraph can be accurate, detailed, and smooth and '
'still be <strong>summary</strong>. Analysis names a <strong>choice</strong> the author made, states its '
'<strong>effect</strong>, and reaches the <strong>warrant</strong>.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: run it on any paragraph</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you call a paragraph analysis, ask these observable yes/no questions:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0"><strong>Choice?</strong> Does one sentence name something the AUTHOR did (an opening, an order, a comparison)?</li>'
'<li style="margin:2px 0"><strong>Effect?</strong> Does it say what that choice does to the reader?</li>'
'<li style="margin:2px 0"><strong>Warrant?</strong> Does it say why that effect matters to the author\'s purpose?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">Summary that reads smoothly is easy to overrate, so run the check even when a paragraph feels finished.</div></div>')

# coping-model before/after panel: a summary paragraph on the weather text, revised into device-effect-warrant.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> a paragraph that summarizes, not analyzes</span>'
    '<p style="margin:8px 0 0;font-size:15px">The weather article explains that forecasters collect data every '
    'hour, use satellites and models, and then share the forecast. It covers a lot of steps.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">Every sentence retells what the article says. It '
    'never names an authorial choice, its effect, or why it matters, so it is summary, not analysis.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> revised to name a choice, effect, and warrant</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">CHOICE</span> The author opens by calling forecasts "so ordinary," '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">EFFECT</span> which lowers the reader\'s guard, '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">WARRANT</span> and that matters because the hourly science the article describes next '
      'lands as a real surprise against that low expectation.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">The revision names a choice, its effect, and why '
    'it matters. Turning summary into choice, effect, and warrant is the fix.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1003-0009", grade="9-10", lesson_type=5,
    unit="G10 U2 - Text-dependent analysis (analysis vs summary check)",
    title="Check It: Does This Paragraph Analyze or Summarize?",
    target=("Judge whether a provided paragraph analyzes (device, effect, warrant) or only summarizes, predict "
            "its score, see the reveal, then revise a summary paragraph into analysis, plus a faultless "
            "self-check on a fresh paragraph. Written at the paragraph. Trait: Evidence/Development (analysis)."),
    acc_tags=["ACC.W.INFO.6", "ACC.W.INFO.2", "ACC.W.SRC.3", "CCSS.W.9-10.2", "CCSS.W.9-10.9"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.03", "sot": "icm course-G10.md L09",
                "taught_stimulus": "ACC-W910-INFO-LESSON-WEATHER",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-WETLANDS",
                "one_idea": "A paragraph can retell a text perfectly and still be summary; analysis names a choice, its effect, and the warrant.",
                "one_reminder": "Run the check: choice named? effect stated? warrant reached?",
                "playbook": "_phase2/playbook_T5_CHECK.md",
                "template": "locked L01 template; the material is the PROVIDED paragraph; source bound for authentic craft references.",
                "version_note": ("V3.1 rebuild to the v3.1 build spec (structural template lesson_g9_l25_essay_"
                                 "revision_v3_1.py). Fixed the prior gate failures: (a) TEACH is now one hammered "
                                 "idea (ONE_IDEA callout + the analysis-vs-summary tells as a <ul>), the "
                                 "check-predict-reveal-revise routine moved to the REMEMBER check tool at point of "
                                 "first use (was two prose teach cards that failed format_fidelity as walls of "
                                 "text); (b) the discrimination dropped the leaked 'Grade-C design bet we label as "
                                 "a bet' prose and now uses explicit choices with the correct option NOT the "
                                 "lone-longest and 'the author' on both options to break the token confound; (c) "
                                 "FRQ + diagnosis built with frq_prompt/setapart/checklist (no Step-N prose, no "
                                 "'Scored on' chrome), provided paragraph in a setapart block; (d) self_score is a "
                                 "clean predict-the-score MCQ; 'warrant' defined with an 'is a' cue. Kept bound "
                                 "stimuli + every production unit='paragraph' (T5 ceiling)."),
                "council": ("T5/CHECK analysis capstone: calibrate a full paragraph on the analysis-vs-summary "
                            "line (predict-then-reveal self_score), then revise summary into device-effect-"
                            "warrant, + a self-check on ONE own fresh paragraph (NO prior-draft look-back). "
                            "analyzes-vs-summarizes discrimination labeled Grade-C in code. CHECK=proposal; T5 "
                            "ceiling paragraph."),
                "review_provenance": "built to the G9 L25 v3.1 pattern (icm/_config/v3_1-lesson-build-spec.md)."},
    fade_ledger_moves=["calibrate-analysis-vs-summary", "revise-summary-into-analysis"],
    slots=[
        # ===== TEACH: ONE idea, hammered (callout + the summary tells as a list; routine moved to the model card) =====
        Slot("TEACH", "teach_card", "The one idea: analysis names a choice, effect, and warrant",
             body=(ONE_IDEA +
                   "The single line that decides an analysis score is analysis versus summary. Summary retells "
                   "WHAT the text says, step by step. Analysis names an authorial CHOICE, states its EFFECT on "
                   "the reader, and reaches the warrant. A warrant is a sentence that says why that effect "
                   "matters to the author's purpose. Watch for these summary tells:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>It retells the content</strong>: it walks through the "
                   "steps or facts the text gives, in order.</li>"
                   "<li style=\"margin:4px 0\"><strong>It names no choice</strong>: it never points to something "
                   "the AUTHOR did, such as an opening, an order, or a comparison.</li>"
                   "<li style=\"margin:4px 0\"><strong>It states no effect</strong>: it never says what a choice "
                   "does to the reader.</li>"
                   "<li style=\"margin:4px 0\"><strong>It reaches no warrant</strong>: it never says why that "
                   "effect matters to the author's purpose.</li></ul>"
                   "Summary that reads smoothly is easy to overrate, so you will first judge PROVIDED "
                   "paragraphs on this line, predict their scores, and see the reveal. Then you revise summary "
                   "into analysis and run the same check on a paragraph you write here.")),
        Slot("TEACH", "stimulus_display", "Read the source: how weather forecasts work",
             ref="ACC-W910-INFO-LESSON-WEATHER", bank="weather", tag="buy_in",
             body=("Read this explanatory source on weather forecasting. The paragraphs you judge and revise "
                   "are about this text, so knowing its choices (its 'so ordinary' opening, its step-by-step "
                   "order, its comparisons) lets you turn summary into real analysis. The text stays on screen "
                   "while you work.")),

        # ===== MODEL (before the quiz): before/after worked example + the check tool at point of first use =====
        Slot("MODEL", "annotated_before_after", "Watch a summary paragraph become analysis",
             bank="weather",
             body=("Here is the skill in action. Read the BEFORE, then the AFTER, and notice choice, effect, and "
                   "warrant replacing the retelling." + BEFORE_AFTER_HTML +
                   " The BEFORE retells the steps; the AFTER names a choice, its effect, and its significance. "
                   "Turning summary into choice, effect, and warrant is the fix. " + REMEMBER +
                   "When you judge or revise a paragraph, run this check, then reread once more.")),
        Slot("MODEL", "discrimination", "Which paragraph analyzes, and which summarizes?",
             ref="", labeled_grade_c=True, bank="weather",
             body=("Spot the target before you revise. Which paragraph fully ANALYZES (names a choice, its "
                   "effect, AND why it matters)? The other three fall short in different ways. "
                   "(A) The author's article says forecasters gather data every hour from satellites and radar, "
                   "run all of it through computer models, and then release the finished forecast to the "
                   "public.  "
                   "(B) The author opens by calling forecasts 'so ordinary,' which lowers the reader's guard, so "
                   "the hourly science described next lands as a genuine surprise.  "
                   "(C) The author's writing is clear and well organized, moving smoothly from one forecasting "
                   "step to the next so the whole explanation is easy for a reader to follow.  "
                   "(D) The author opens by calling forecasts 'so ordinary,' which makes the everyday forecast "
                   "feel familiar to the reader. "
                   "Correct: B. Only B names a choice, its effect, AND the warrant. (A) retells the steps; (C) "
                   "praises the craft; (D) names a choice and effect but stops before the warrant."),
             choices=[
                 {"id": "A", "text": "The author's article says forecasters gather data every hour from satellites and radar, run all of it through computer models, and then release the finished forecast to the public.",
                  "correct": False,
                  "why": "This retells the steps accurately, but it names no choice the author made, no effect on the reader, and no warrant, so it is summary."},
                 {"id": "B", "text": "The author opens by calling forecasts 'so ordinary,' which lowers the reader's guard, so the hourly science described next lands as a genuine surprise.",
                  "correct": True,
                  "why": "Correct. It names a choice (the 'ordinary' opening), its effect (a lowered guard), and why it matters (setting up the surprise). That is choice, effect, and warrant, so it analyzes."},
                 {"id": "C", "text": "The author's writing is clear and well organized, moving smoothly from one forecasting step to the next so the whole explanation is easy for a reader to follow.",
                  "correct": False,
                  "why": "This praises the writing (clear, organized, easy to follow), but praising craft is not analysis. It names no specific authorial choice and no effect on meaning, so it does not analyze."},
                 {"id": "D", "text": "The author opens by calling forecasts 'so ordinary,' which makes the everyday forecast feel familiar to the reader.",
                  "correct": False,
                  "why": "This names a choice (the 'ordinary' opening) and its effect (feels familiar), but it stops there. Without a warrant saying why that effect matters to the author's purpose, it lands in the middle band, not full analysis."},
             ]),
        Slot("MODEL", "predict_the_fix", "Why does this paragraph score as summary?",
             bank="weather",
             body=("Predict before the reveal. A provided paragraph reads: 'The author describes satellites, "
                   "radar, and weather balloons, and explains how each one gathers information for the "
                   "forecast.' Which single judgment is correct? "
                   "(A) summary, it retells what the article describes but names no authorial choice, effect, or "
                   "significance  "
                   "(B) analysis, it names several specific tools and clearly explains what each instrument does "
                   "for the forecast  "
                   "(C) summary, but only because it is too short, and adding a few more sentences would make it "
                   "count as analysis  "
                   "(D) analysis, it is accurate about the tools and correctly explains what each one does for "
                   "the forecast"),
             feedback=("Correct: A. The paragraph accurately retells the content (the tools and what they do) "
                       "but never names a CHOICE the author made, its effect, or why it matters, so it scores "
                       "as summary. Naming specific tools (B) or being accurate (D) is not analysis; length (C) "
                       "is not the issue. To lift it, name an authorial choice and reach its significance.")),

        # ===== SUPPORTED: predict the score (calibration MCQ) -> then revise a summary paragraph (frame + checklist) =====
        Slot("SUPPORTED", "self_score", "Predict the score, then see the real score",
             ref="", bank="weather",
             body=("Predict, then reveal. A provided paragraph reads: 'The article explains that forecasting has "
                   "improved over the years and now helps people plan their days.' On a 2-point scale (2 = "
                   "analysis with a choice, effect, and warrant; 1 = summary), what score does this paragraph "
                   "earn?"),
             choices=[
                 {"id": "1", "text": "1 out of 2", "correct": True,
                  "why": "Correct. It retells a fact about forecasting but never names a choice the author made "
                         "or its effect, so it is summary and that caps it at 1. A 2 would name a choice (say, "
                         "the confident closing) and reach why it matters."},
                 {"id": "2", "text": "2 out of 2", "correct": False,
                  "why": "A 2 needs a choice, an effect, and a warrant. This paragraph retells a fact about "
                         "forecasting and names no authorial choice or effect. Notice how smooth summary invites "
                         "an overrate."},
             ]),
        Slot("SUPPORTED", "production_frq", "Revise the summary paragraph into analysis",
             ref="", bank="weather", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="Revise the summary paragraph below into analysis. Keep it accurate to the weather text, "
                       "but make it analyze, not retell.",
                 setapart_block=setapart("Paragraph to revise:",
                                         "The weather article explains that forecasters collect data every hour, "
                                         "use satellites and models, and then share the forecast."),
                 checklist_block=checklist(title="Use this check:", rows=[
                     "Name a CHOICE the author made (for example the 'so ordinary' opening, the step-by-step order).",
                     "State its EFFECT on the reader.",
                     "Reach the WARRANT: one sentence saying why that effect matters to the author's purpose.",
                 ]),
                 closer="Rewrite the whole paragraph so it names a choice, its effect, and the warrant.")),
        # DIAGNOSIS: watch the check run on a provided paragraph, then run it on a fresh paragraph in this box
        # (stateless-safe; the material is provided, and the self-check is on the same item, not a prior submission).
        Slot("MODEL", "diagnosis_frq", "Self-check a fresh paragraph on the analysis line",
             ref="", bank="weather", scored=True,
             body=frq_prompt(
                 intro="First watch the check run on a provided paragraph, then run it on a fresh paragraph you "
                       "write here.",
                 setapart_block=setapart("Provided paragraph to check:",
                                         "The author lists many uses of forecasts, from farming to flights.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Choice named?", "No. It lists content the article gives, not something the author did."),
                     ("Effect stated?", "No. It never says what any choice does to the reader."),
                     ("Warrant reached?", "No. It never says why an effect matters, so it is summary."),
                 ]),
                 closer="Now write a fresh analytical paragraph about the weather text here, then run the same "
                        "three questions on it: choice? effect? warrant? For each No, add that part, and finish "
                        "by naming the choice your paragraph analyzes.")),

        # ===== INDEPENDENT: revise a PROVIDED paragraph with no checklist scaffold + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Revise a provided paragraph on your own",
             ref="", bank="weather", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="On your own now, no checklist. Revise the summary paragraph below into analysis.",
                 setapart_block=setapart("Paragraph to revise:",
                                         "The article describes how forecasts are made and why they are useful "
                                         "to people."),
                 closer="Name an authorial choice, state its effect, and reach the warrant. Then check your "
                        "revision: choice named? effect stated? warrant reached? Fix any No before you submit. "
                        "This is what every real analysis paragraph is built on, and you are ready to do it "
                        "cold.")),

        # ===== TRANSFER: same summary-into-analysis move, a NEW text (wetlands), bank-partitioned =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: what wetlands do",
             ref="ACC-W910-INFO-LESSON-WETLANDS", bank="wetlands",
             body=("Read this new explanatory source on wetlands. The paragraph you revise is about this text, "
                   "so knowing its choices (its 'wasted ground' opening, its order, its comparisons) lets you "
                   "turn summary into analysis. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Revise a summary paragraph on a NEW text",
             ref="", bank="wetlands", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="New text, same move. Revise the summary paragraph below into analysis.",
                 setapart_block=setapart("Paragraph to revise:",
                                         "The wetlands article explains that wetlands filter water, store "
                                         "floodwater, and shelter wildlife."),
                 closer="Name an authorial choice (for example the 'wasted ground' opening that the article "
                        "corrects), state its effect, and reach the warrant. Then check your revision: choice "
                        "named? effect stated? warrant reached? Same summary-into-analysis move as the weather "
                        "paragraphs, on a new text.")),
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
