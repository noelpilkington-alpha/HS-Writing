"""
lesson_g11_l09_ra_paragraph_check.py  -  G11 KC C.11.03, ARCHETYPE T5: RUBRIC-REVISION (CHECK, paragraph). V3.1.

G11 L09 (Unit 2, check), rebuilt to the v3.1 build spec. Teaching point (KEPT): judge whether a paragraph
analyzes the author's rhetorical CHOICES (choice, framed evidence, audience effect, purpose) or slips into
summary, predict its score, see the reveal, then revise a summary paragraph into rhetorical analysis, plus a
faultless self-check on a fresh paragraph the student writes here. This is the STATELESS-LEGAL revision model:
work on PROVIDED paragraphs about a bound source + a self-check on ONE own submission, never a prior-draft look-
back. KC C.11.03. Bound stimuli KEPT: ACC-W910-ANALYSIS-LESSON-DOUGLASS (Douglass 1852, taught) ->
ACC-W910-RA-SINGLE-0001 (FDR First Inaugural 1933, transfer, bank-partitioned). rc.ap, unit="paragraph" (T5
ceiling). CHECK=proposal.

V3.1 changes over the pre-v3.1 L09 (all prior gate failures fixed):
  1. TEACH is now ONE idea, hammered: a teal ONE_IDEA callout + the tells of summary as a real <ul> list (was two
     prose teach cards). The check-predict-reveal-revise routine moved to the REMEMBER check tool at the model
     card (point of first use), not cold up front.
  2. NO leaked internal labels: the old discrimination prose said "a Grade-C design bet we label as a bet"
     (leaked_internal_label). Removed; the discrimination now uses explicit choices=[{id,text,correct,why}] with
     the correct option NOT the lone-longest and a quote in the summary distractor so a quotation, not a surface
     token, is not the invariant (the framed-analysis move is).
  3. FRQ + diagnosis bodies built with frq_prompt / setapart / checklist (no "Step N" prose, no "Scored on"
     chrome). The provided paragraph to revise sits in a setapart(...) block each time.
  4. self_score is a clean predict-the-score MCQ (short prompt + choices carrying the reveal), not a prose block.
     Coping before/after kept (literal BEFORE + AFTER inline). Own words, no fabricated figures, no em dashes.
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
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A rhetorical-analysis paragraph earns its score by '
'<strong>analyzing the author\'s choices</strong>, not by retelling what the author says. '
'Summary retells; analysis names a <strong>choice</strong> and what it does to the audience.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: run these four questions on any paragraph</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit a paragraph, ask these observable yes/no questions:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0"><strong>Choice?</strong> Does it name a rhetorical choice the author makes, not just the content?</li>'
'<li style="margin:2px 0"><strong>Framed evidence?</strong> Is a short quote set up and interpreted, not dropped in?</li>'
'<li style="margin:2px 0"><strong>Audience effect?</strong> Does it say what that choice does to the listeners?</li>'
'<li style="margin:2px 0"><strong>Purpose?</strong> Does it reach why the author made that choice?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">Smooth summary can read as if it is doing analytical work, so run the check even when a paragraph feels finished.</div></div>')

# coping-model before/after panel: a summary paragraph on the Douglass speech, revised into rhetorical analysis.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> a paragraph that slips into summary</span>'
    '<p style="margin:8px 0 0;font-size:15px">Douglass talks about how enslaved people are excluded from the '
    'Fourth of July. He mentions the Declaration and says the distance between the audience and him is large. '
    'He clearly feels strongly.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">This retells what Douglass says and how he feels. It '
    'names no choice, frames no quote, and reaches no purpose, so the rubric caps it.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> the same idea, revised into analysis of a choice</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">CHOICE + FRAMED QUOTE + PURPOSE</span> By naming the audience\'s "high independence" as '
      'the very thing that "reveals the immeasurable distance between us," Douglass turns their own pride into '
      'the measure of his exclusion, so his listeners cannot celebrate the day without indicting themselves.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">The revision names a choice, frames a trimmed quote, '
    'and reaches the purpose. Turning summary into analysis is the fix.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W1112-L-G11-C1103-0009", grade="9-10", lesson_type=5,
    unit="G11 U2 - Rhetorical analysis (paragraph check)",
    title="Check It: Rhetorical Analysis or Summary?",
    target=("Judge whether a paragraph analyzes the author's rhetorical choices (choice, framed evidence, "
            "audience effect, purpose) or slips into summary, predict its score, see the reveal, then revise a "
            "summary paragraph into rhetorical analysis, plus a faultless self-check on your own paragraph. "
            "Written at the paragraph. Trait: Evidence and Commentary."),
    acc_tags=["ACC.W.INFO.6", "CCSS.W.11-12.9", "CCSS.RI.11-12.6"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.03", "sot": "icm course-G11.md L09",
                "taught_stimulus": "ACC-W910-ANALYSIS-LESSON-DOUGLASS",
                "transfer_stimulus": "ACC-W910-RA-SINGLE-0001",
                "one_idea": "A rhetorical-analysis paragraph analyzes the author's choices; summary only retells.",
                "one_reminder": "Run the check: choice? framed evidence? audience effect? purpose?",
                "playbook": "_phase2/playbook_T5_CHECK.md",
                "template": "locked L01 template; ANALYSIS-TIER; provided paragraphs are the material, source bound for context.",
                "version_note": ("V3.1 rebuild of the pre-v3.1 L09 to the v3.1 build spec. Fixed the prior gate "
                                 "failures: (a) TEACH is now one hammered idea (ONE_IDEA callout + the tells of "
                                 "summary as a <ul>), the check-predict-reveal-revise routine moved to the REMEMBER "
                                 "check tool at point of first use (was two prose teach cards); (b) the "
                                 "discrimination dropped the leaked 'Grade-C design bet we label as a bet' prose and "
                                 "now uses explicit choices with the correct option NOT the lone-longest and a quote "
                                 "in the summary distractor to break the token confound; (c) FRQ + diagnosis built "
                                 "with frq_prompt/setapart/checklist (no Step-N prose, no 'Scored on' chrome), "
                                 "provided paragraph in a setapart block; (d) self_score is a clean predict-the-score "
                                 "MCQ, not a prose block. Kept bound stimuli + every production unit='paragraph' (T5 "
                                 "ceiling)."),
                "council": ("T5/CHECK G11 rhetorical-analysis capstone: calibrate analysis-vs-summary on a full RA "
                            "paragraph via rD1 predict-the-fix + K1 predict-then-reveal + R1 revise-provided-anchor "
                            "+ R3 self-check on ONE own fresh paragraph; NO prior-draft look-back. analyzes-choices-"
                            "vs-summarizes discrimination labeled Grade-C in code. CHECK=proposal; T5 ceiling "
                            "paragraph."),
                "review_provenance": "built to the G9 L25 v3.1 pattern (icm/_config/v3_1-lesson-build-spec.md)."},
    fade_ledger_moves=["calibrate-ra-vs-summary", "revise-summary-into-ra", "R3-self-check-own-paragraph"],
    slots=[
        # ===== TEACH: ONE idea, hammered (callout + the tells of summary as a list; routine moved to model card) =====
        Slot("TEACH", "teach_card", "The one idea: analyze the choice, do not retell",
             body=(ONE_IDEA +
                   "A rhetorical choice is a deliberate decision the author makes about words, structure, or tone "
                   "to move an audience. Framed evidence means a short quote that is set up and interpreted, not "
                   "dropped in. A paragraph can be perfectly accurate about the speech and still be summary. Watch "
                   "for these tells that a paragraph has slipped into summary:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>It retells the content</strong>: it reports what the author "
                   "says instead of naming a choice the author makes.</li>"
                   "<li style=\"margin:4px 0\"><strong>It labels a feeling</strong>: it says the speech is "
                   "\"powerful\" or that the author \"feels strongly\" without analyzing why.</li>"
                   "<li style=\"margin:4px 0\"><strong>It drops or skips the quote</strong>: no short quotation is "
                   "set up and interpreted.</li>"
                   "<li style=\"margin:4px 0\"><strong>It never reaches purpose</strong>: it never says what the "
                   "choice does to the audience or why the author made it.</li></ul>"
                   "You cannot always see the line yourself, so you will first practice on PROVIDED paragraphs: "
                   "predict the score, see the reveal, then revise. After that you run the same check on a "
                   "paragraph you write here.")),
        Slot("TEACH", "stimulus_display", "Read the source: Frederick Douglass, 1852 address (excerpt)",
             ref="ACC-W910-ANALYSIS-LESSON-DOUGLASS", bank="douglass_1852", tag="buy_in",
             body=("Read this excerpt so the material is familiar. The paragraphs you judge and revise are about "
                   "this speech, so knowing Douglass's choices lets you turn summary into analysis. The text "
                   "stays on screen while you work.")),

        # ===== MODEL (before the quiz): before/after worked example + the check tool at point of first use =====
        Slot("MODEL", "annotated_before_after", "Watch a summary paragraph become rhetorical analysis",
             bank="douglass_1852",
             body=("Here is the skill in action. Read the BEFORE, then the AFTER, and notice a choice, a framed "
                   "quote, and a purpose replacing the retelling." + BEFORE_AFTER_HTML +
                   " The BEFORE retells; the AFTER names a choice, frames a trimmed quote, and reaches the "
                   "purpose. Turning summary into analysis is the revision. " + REMEMBER +
                   "When you check a paragraph, run these four questions, then reread once more.")),
        Slot("MODEL", "discrimination", "Which paragraph analyzes the choice?",
             ref="", labeled_grade_c=True, bank="douglass_1852",
             body=("Spot the target before you revise. All four are accurate about the speech. Which one fully "
                   "ANALYZES a rhetorical choice (names a choice, frames a quote, states the audience effect, AND "
                   "reaches the purpose)? The other three fall short in different ways. "
                   "(A) Douglass explains that the holiday leaves out enslaved people and that his listeners "
                   "enjoy freedoms he is denied; he even calls the day \"yours, not mine,\" and he moves through "
                   "these points one by one, clearly feeling very strongly about all of them.  "
                   "(B) By calling the audience's \"high independence\" the very thing that \"reveals the "
                   "immeasurable distance between us,\" Douglass turns their pride into the measure of his "
                   "exclusion, so they cannot celebrate without indicting themselves.  "
                   "(C) This passage is powerful and deeply moving, and by the end the audience cannot help but "
                   "feel the full force of Douglass's anger and the weight of what he lays before them.  "
                   "(D) By naming the audience's \"high independence\" as the thing that \"reveals the "
                   "immeasurable distance between us,\" Douglass makes his listeners feel the sting of their own "
                   "pride. "
                   "Correct: B. Only B names a choice, frames the quote, states the effect, AND reaches the "
                   "purpose. (A) retells content and feeling around a dropped phrase; (C) praises a reaction and "
                   "names no choice; (D) names a choice, frames the quote, and states the effect but stops before "
                   "the purpose."),
             choices=[
                 {"id": "A",
                  "text": "Douglass explains that the holiday leaves out enslaved people and that his listeners enjoy freedoms he is denied; he even calls the day \"yours, not mine,\" and he moves through these points one by one, clearly feeling very strongly about all of them.",
                  "correct": False,
                  "why": "This is summary. It quotes the speech but only retells the content and labels a feeling; it names no choice, does not interpret the quote, and never reaches a purpose."},
                 {"id": "B",
                  "text": "By calling the audience's \"high independence\" the very thing that \"reveals the immeasurable distance between us,\" Douglass turns their pride into the measure of his exclusion, so they cannot celebrate without indicting themselves.",
                  "correct": True,
                  "why": "Correct. It names a choice (turning the audience's pride into the measure of his exclusion), frames a trimmed quote, states the audience effect, and reaches the purpose (they cannot celebrate without indicting themselves)."},
                 {"id": "C",
                  "text": "This passage is powerful and deeply moving, and by the end the audience cannot help but feel the full force of Douglass's anger and the weight of what he lays before them.",
                  "correct": False,
                  "why": "This is praise, not analysis. 'Powerful,' 'deeply moving,' and 'the full force of his anger' label a reaction to the passage; the paragraph names no choice, frames no quote, and reaches no purpose, so it caps low."},
                 {"id": "D",
                  "text": "By naming the audience's \"high independence\" as the thing that \"reveals the immeasurable distance between us,\" Douglass makes his listeners feel the sting of their own pride.",
                  "correct": False,
                  "why": "So close. It names a choice, frames the quote, and states the audience effect (the sting of their pride), but it stops there. Without reaching the purpose (why Douglass wants them to feel that sting), it lands in the middle band, not full analysis."},
             ]),
        Slot("MODEL", "predict_the_fix", "Why does this paragraph score as summary?",
             bank="douglass_1852",
             body=("Predict before the reveal. A provided paragraph reads: 'Douglass describes the injustice of "
                   "the holiday and lists the freedoms the audience has that he lacks. He wants things to "
                   "change.' Which judgment is correct? "
                   "(A) It reads as summary: it retells what Douglass describes and states his aim, but it names "
                   "no choice, quotes nothing, and reaches no purpose.  "
                   "(B) It reads as analysis, since it refers to the audience's freedoms and to his wish for "
                   "change, which is the kind of audience effect that real analysis is built on.  "
                   "(C) It reads as summary, but only because it is too short; adding several more sentences of "
                   "the same retelling kind would turn it into analysis.  "
                   "(D) It reads as analysis, since it accurately describes the injustice and the freedoms, and "
                   "getting the content right is the main thing an analysis paragraph has to do."),
             feedback=("Correct: A. Mentioning the audience (B) or being accurate about the content (D) is not "
                       "analysis, and length (C) is not the issue. The paragraph retells what Douglass describes "
                       "and wants, but names no choice, frames no quote, and reaches no purpose, so it stays "
                       "summary. To lift it, name a choice, frame a trimmed quote, and reach the purpose.")),

        # ===== SUPPORTED: predict the score (calibration MCQ) -> then revise a paragraph (frame + checklist) =====
        Slot("SUPPORTED", "self_score", "Predict the score, then see the real score",
             ref="", bank="douglass_1852",
             body=("Predict, then reveal. A provided paragraph reads: 'Douglass uses strong language and asks "
                   "many questions. This makes his speech powerful and memorable.' On a 2-point scale (2 = names "
                   "a choice with a framed quote, an audience effect, and a purpose; 1 = summary or vague), what "
                   "score does this paragraph earn?"),
             choices=[
                 {"id": "1", "text": "1 out of 2", "correct": True,
                  "why": "Correct. 'Strong language,' 'powerful,' and 'memorable' are praise labels with no named "
                         "choice, no framed quote, and no stated effect on the audience, so it caps at 1. A 2 "
                         "would name a specific choice (say, his rhetorical questions) and reach the purpose they "
                         "serve."},
                 {"id": "2", "text": "2 out of 2", "correct": False,
                  "why": "A 2 needs a named choice, a framed quote, and the audience effect it creates. Calling "
                         "the speech 'powerful' and 'memorable' labels a reaction without analyzing any choice, "
                         "so notice how praise words can pass for analysis."},
             ]),
        Slot("SUPPORTED", "production_frq", "Revise the summary paragraph into analysis",
             ref="", bank="douglass_1852", rubric_ref="rc.ap", scored=True, unit="paragraph", frq_type="revision",
             body=frq_prompt(
                 intro="Revise the summary paragraph below into rhetorical analysis. Keep it accurate, but make "
                       "it analyze a choice instead of retelling.",
                 setapart_block=setapart("Paragraph to revise:",
                                         "Douglass talks about how enslaved people are excluded from the Fourth "
                                         "of July and how far apart he and the audience are. He feels strongly."),
                 checklist_block=checklist(title="Build it in these moves:", rows=[
                     "Name a CHOICE Douglass makes (for example, turning the audience's pride into the measure of his exclusion).",
                     "Frame a trimmed quote from the speech and interpret it, rather than dropping it in.",
                     "State the effect on the AUDIENCE and reach his PURPOSE.",
                 ]),
                 closer="Write the full revised paragraph.")),
        # DIAGNOSIS: watch the check run on a provided paragraph, then run it on a fresh paragraph in this box
        # (stateless-safe; the material is provided, and the self-check is on the same item, not a prior submission).
        Slot("MODEL", "diagnosis_frq", "Self-check a fresh paragraph against the check",
             ref="", bank="douglass_1852", scored=True,
             body=frq_prompt(
                 intro="First watch the check run on a provided paragraph, then run it on a fresh paragraph you "
                       "write here.",
                 setapart_block=setapart("Provided paragraph to check:",
                                         "Douglass says the nation is hypocritical. He gives many examples.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Choice named?", "No. It reports what Douglass says but points to no choice he makes."),
                     ("Framed evidence?", "No. There is no quotation set up and interpreted. Add one."),
                     ("Audience effect and purpose?", "No. It never says what a choice does to listeners or why. Add both."),
                 ]),
                 closer="Now write a fresh rhetorical-analysis paragraph on the Douglass speech here, then run the "
                        "same four questions on it: choice? framed evidence? audience effect? purpose? For each "
                        "No, add that item, and finish by naming the choice you analyzed.")),

        # ===== INDEPENDENT: revise a PROVIDED paragraph with no scaffold + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Revise a provided paragraph on your own",
             ref="", bank="douglass_1852", rubric_ref="rc.ap", scored=True, unit="paragraph", frq_type="revision",
             body=frq_prompt(
                 intro="On your own now, no build list. Revise the summary paragraph below into rhetorical "
                       "analysis.",
                 setapart_block=setapart("Paragraph to revise:",
                                         "Douglass criticizes the country for celebrating freedom while denying it "
                                         "to others. He uses emotional language."),
                 closer="Name a choice, frame a trimmed quote, state the audience effect, and reach the purpose. "
                        "Then run the check: choice? framed evidence? audience effect? purpose? This is what "
                        "every real rhetorical-analysis paragraph is built on, and you are ready to do it "
                        "cold.")),

        # ===== TRANSFER: same summary-into-analysis move, a NEW speech (FDR 1933), bank-partitioned =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: a second speech",
             ref="ACC-W910-RA-SINGLE-0001", bank="ra_speech_1",
             body=("Read this new address so the material is familiar. The paragraph you revise is about this "
                   "text. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Revise a summary paragraph on a NEW text",
             ref="", bank="ra_speech_1", rubric_ref="rc.ap", scored=True, unit="paragraph", frq_type="revision",
             body=frq_prompt(
                 intro="New speaker, same move. Revise the summary paragraph below into rhetorical analysis.",
                 setapart_block=setapart("Paragraph to revise:",
                                         "Roosevelt says the country is in hard times and that people are afraid. "
                                         "He tells them things will get better and that the government will act."),
                 closer="Name a choice Roosevelt makes, frame a trimmed quote from the address, state the effect "
                        "on his anxious audience, and reach his purpose. Same summary-into-analysis revision as "
                        "the Douglass paragraph, on a new speech.")),
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
