"""
lesson_g11_l07_choice_audience_purpose.py  -  G11 KC C.11.03, ARCHETYPE T4: TEXT-DEPENDENT ANALYSIS (DEW, paragraph). V3.1.

V3.1 rebuild of the pre-v3.1 L07 to the v3.1 spec (icm/_config/v3_1-lesson-build-spec.md), adapting the pattern
proven on G9 L06/L08 v3.1. PRESERVED: teaching point (chain the move all the way, choice -> effect on the
audience -> the PURPOSE that effect serves), id ACC-W1112-L-G11-C1103-0007, lesson_type=4, kc C.11.03,
mnemonic_status=proposal, unit, and the bound ANALYSIS-TIER lesson stimuli (Douglass 1852 taught, Bryan "Cross
of Gold" 1896 transfer). Changes vs the prior L07:
  1. ONE IDEA, hammered (KH load): a teal ONE_IDEA callout states the single core idea (the full move reaches
     the PURPOSE, not just the effect), then the minimum teaching as a LIST (effect vs purpose) instead of the
     old ~110-word prose block that tripped format_fidelity.
  2. COPING-MODEL THINK-ALOUD (SRSD): the model is rewritten as a written revision process (first try -> run
     the check -> catch that it stalls at the effect -> reach the purpose), not a clean finished panel. Still
     contains literal BEFORE and AFTER (content_depth). The reusable purpose check is attached at the point of
     first use (the model card) as a REMEMBER box, not cold in step 1.
  3. FIXED THE SURFACE CONFOUND (DI, faultless communication): the discrimination now uses explicit choices=[]
     with the word "so" carried by BOTH a distractor and the key (relevance, reaching-the-purpose, is the only
     invariant, not the connective). Removed the leaked "Grade-C design bet" label from the student text
     (labeled_grade_c=True stays in code only); the reveal lives in a "Correct: X" tail, not in option text.
  4. DETERMINISTIC FRQ/DIAGNOSIS BODIES: production + diagnosis prompts are built with frq_prompt/setapart/
     checklist (no hand-written "Step 1/2" prose that double-numbers), and carry NO "Scored on ..." chrome.
  5. AUTONOMY + SAY-THE-STANDARD (Yeager): the independent write drops the frame, hands over choice of which
     Douglass move to analyze, and names the standard out loud.

ONE IDEA: the full move reaches the PURPOSE the effect serves, not just the effect. ONE REMINDER: the purpose
check. Passes all 23 lesson_contract gates. Own words, public-domain source text, no em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">The full move reaches the <strong>PURPOSE</strong> the '
'effect serves. Naming a choice and what it does to the audience is only the middle of the chain; you are not '
'done until you reach WHY the author wants that effect.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the purpose check</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you call an analysis finished, run this quick check:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Did I name the choice the author made?</li>'
'<li style="margin:2px 0">Did I name its effect on the audience?</li>'
'<li style="margin:2px 0">Did I reach the purpose, WHY the author wants that effect?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If you stop after question 2, the analysis stalls at '
'the effect. Add the purpose before you commit to it.</div></div>')

# coping-model think-aloud panel: a WRITTEN revision process (first try -> run the check -> catch that it
# stalls at the effect -> reach the purpose), then the BEFORE/AFTER endpoints (content_depth requires both
# literal words). No named person (Timeback stateless rule).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer building an analysis of one Douglass choice, the way he repeats the word "your":</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Douglass repeats the word \'your\' again and again." '
    'Run the check: did I name the effect on the audience? No, I only named the choice. That is not enough yet.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "Douglass repeats \'your,\' which makes the audience '
    'feel singled out, as if the whole holiday is being handed to them alone." Run the check again: choice named, '
    'effect named. Did I reach the purpose, WHY he wants that effect? No. It stalls at the effect.</p>'
    '<p style="margin:0"><strong>Final:</strong> "Douglass repeats \'your,\' which makes the audience feel the '
    'holiday belongs to them and not to him, so that they cannot enjoy their own celebration without confronting '
    'the exclusion he is exposing." Run the check: choice, effect, and now the purpose. That reaches the end of '
    'the chain.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "Douglass repeats \'your,\' which makes the audience feel '
    'singled out." (names the choice and the effect, then stops)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "Douglass repeats \'your,\' which makes the audience feel the '
    'holiday belongs to them and not to him, so that they cannot celebrate without confronting the exclusion he '
    'is exposing." (reaches the purpose the effect serves)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1103-0007", grade="9-10", lesson_type=4,
    unit="G11 U2 - Rhetorical analysis (choice to effect to purpose)",
    title="From Choice to Audience Effect to Purpose",
    target=("Chain the move all the way: name the author's choice, its effect on the audience, and the PURPOSE "
            "that effect serves. Written at the paragraph. Trait: Evidence and Commentary."),
    acc_tags=["ACC.W.INFO.6", "CCSS.W.11-12.9", "CCSS.RI.11-12.6"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.03", "sot": "icm course-G11.md L07",
                "taught_stimulus": "ACC-W910-ANALYSIS-LESSON-DOUGLASS",
                "transfer_stimulus": "ACC-W910-RA-SINGLE-0002",
                "one_idea": "The full move reaches the PURPOSE the effect serves, not just the effect.",
                "one_reminder": "purpose check: choice named? effect named? purpose (why he wants that effect) reached?",
                "playbook": "_phase2/playbook_T4_DEW.md",
                "template": "locked L01 template; ANALYSIS-TIER binds full verbatim PD sources.",
                "version_note": ("V3.1: rebuilt to the v3.1 spec on the L06/L08 v3.1 pattern - ONE_IDEA callout + "
                                 "list teach (fixed the prose-wall body), coping-model revision think-aloud "
                                 "(SRSD), purpose check tool at point of first use, explicit choices=[] "
                                 "discrimination with the 'so' confound broken + the leaked 'Grade-C design bet' "
                                 "label removed (DI faultless communication), deterministic frq_prompt/setapart/"
                                 "checklist bodies (no 'Step N' double-number, no 'Scored on' chrome), autonomy + "
                                 "say-the-standard on the independent write. Preserved teaching point, id, KC, "
                                 "lesson_type, mnemonic_status, unit, and the bound Douglass/Bryan stimuli."),
                "council": ("T4/DEW G11 guided rung: choice -> effect on the audience -> purpose. "
                            "reaches-purpose-vs-stops-at-effect discrimination labeled Grade-C (code only). "
                            "DEW=proposal; unit ladder sentence->paragraph within the type-4 paragraph ceiling."),
                "review_provenance": ("23 lesson_contract gates (exit 0) + gated_reading render-QC clean; "
                                      "adapts the adjudicated L01 v3.1 Council+Fable findings.")},
    fade_ledger_moves=["choice-effect-purpose", "reach-the-authors-purpose"],
    slots=[
        # ===== TEACH: ONE idea only (list, not a wall of prose; purpose check held for point of first use) =====
        Slot("TEACH", "teach_card", "Reach the purpose the effect serves",
             body=(ONE_IDEA +
                   "You already do the first two links of the chain: you name a choice the author makes, and you "
                   "name its effect on the audience. The top-band step is the third link, the purpose. Keep the "
                   "two later links apart:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Effect</strong> means what the choice does to the "
                   "listeners: how it makes them feel or what it makes them notice. Example: the repeated 'your' "
                   "makes them feel singled out.</li>"
                   "<li style=\"margin:4px 0\"><strong>Purpose</strong> means why the author wants that effect: "
                   "what the effect accomplishes for the argument. Example: so the audience cannot celebrate "
                   "without confronting the exclusion he is exposing.</li></ul>"
                   "An analysis that stops at the effect ('the repetition makes them feel singled out') is "
                   "mid-band. Adding the purpose ('so they cannot celebrate without facing the exclusion') lifts "
                   "it. The trap is stalling at the effect. Today: write analysis that reaches the author's "
                   "purpose, not just the effect.")),
        Slot("TEACH", "stimulus_display", "Read the source: Frederick Douglass, 1852 address (excerpt)",
             ref="ACC-W910-ANALYSIS-LESSON-DOUGLASS", bank="douglass_1852",
             body=("Read this excerpt. Because your job is to reach the purpose behind a choice, notice the "
                   "different choices Douglass makes: the repeated 'your,' the pointed questions he opens with, "
                   "the contrast between 'you may rejoice' and 'I must mourn,' and the contrast between the "
                   "nation's stated ideals and its actual practice. Pick one and be ready to run choice, effect "
                   "on the audience, and purpose. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model revision think-aloud + the purpose check tool =====
        Slot("MODEL", "annotated_before_after", "Watch an analysis reach the purpose it was missing",
             bank="douglass_1852",
             body=("Here is the skill in action. Follow the writer's thinking as one draft after another gets "
                   "tested against the check until the analysis finally reaches the purpose. " + COPING_HTML +
                   " Notice the two moves that turned the BEFORE into the AFTER: the writer kept the choice and "
                   "the effect, then reached the PURPOSE the effect serves. " + REMEMBER +
                   "When you build your own analysis, do the same: name the choice, name its effect, then run "
                   "the purpose check before you commit to it.")),
        Slot("MODEL", "discrimination", "Which one reaches the purpose?",
             ref="", labeled_grade_c=True, bank="douglass_1852",
             body=("Now that you have seen one built, spot the target. All four analyze the same choice: "
                   "Douglass opens the speech with pointed questions. All four name that choice and its effect. "
                   "Which one reaches the PURPOSE? "
                   "(A) Douglass opens the speech with pointed questions, which makes his listeners stop short "
                   "and feel the sharp discomfort of being put on the spot right at the very start of the address.  "
                   "(B) Douglass opens the speech with pointed questions, so his listeners feel uneasy and unsure "
                   "of the way they are supposed to respond to him.  "
                   "(C) Douglass opens the speech with pointed questions, so his listeners must answer for "
                   "themselves that the day is not his to share, and face that exclusion.  "
                   "(D) Douglass opens the speech with pointed questions that unsettle his listeners, so that they "
                   "will agree with him and support his cause. "
                   "Correct: C. It reaches the purpose, why he wants that discomfort: to force the audience to "
                   "admit he has no part in the celebration. (A) and (B) name the choice and stop at the effect "
                   "(discomfort, unease), even though (B) uses the word 'so,' and (D) swaps in the generic goal "
                   "of any speech instead of the specific purpose these questions serve."),
             choices=[
                 {"id": "A", "text": "Douglass opens the speech with pointed questions, which makes his listeners stop short and feel the sharp discomfort of being put on the spot right at the very start of the address.",
                  "correct": False,
                  "why": "This names the choice (the questions) and its effect (discomfort), but it stops at the effect. It never reaches WHY Douglass wants the audience uncomfortable."},
                 {"id": "B", "text": "Douglass opens the speech with pointed questions, so his listeners feel uneasy and unsure of the way they are supposed to respond to him.",
                  "correct": False,
                  "why": "The word 'so' is here, but what follows is still just the effect (unease), not the purpose. A connective is not the same as reaching the purpose."},
                 {"id": "C", "text": "Douglass opens the speech with pointed questions, so his listeners must answer for themselves that the day is not his to share, and face that exclusion.",
                  "correct": True,
                  "why": "Correct. This reaches the purpose: the questions force the audience to supply the answer themselves and admit he has no share in the day. That is WHY Douglass wants the discomfort, which is the end of the chain."},
                 {"id": "D", "text": "Douglass opens the speech with pointed questions that unsettle his listeners, so that they will agree with him and support his cause.",
                  "correct": False,
                  "why": "This reaches for a purpose but names the generic goal of almost any speech (win agreement), not the specific purpose these questions serve. A purpose that would fit any choice in any speech has not reached THIS choice's purpose."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this analysis most need?",
             bank="douglass_1852",
             body=("Diagnose this draft before the reveal. A writer analyzing Douglass wrote: 'Douglass contrasts "
                   "the nation's stated ideals with its actual practice, which makes the gap between them "
                   "impossible to ignore.' Which single move would most improve it? "
                   "(A) reach the purpose, why Douglass wants that gap to feel impossible for this audience to ignore  "
                   "(B) name a second contrast Douglass draws so the paragraph can point to more of his choices  "
                   "(C) restate the effect in stronger words so the gap between ideals and practice sounds even wider  "
                   "(D) summarize the whole passage first so the reader knows what Douglass is arguing about overall"),
             feedback=("Correct: A. The draft names a choice (the contrast) and its effect (the gap is "
                       "impossible to ignore) but stops there. Reaching the purpose says WHY: so his listeners, "
                       "who honor those ideals, must either give up the ideals or condemn the practice. A second "
                       "contrast (B), a stronger restatement (C), or a summary (D) never reach the purpose.")),

        # ===== SUPPORTED: framed write (fill-in frame) on the taught source (already read at STEP 2) =====
        Slot("SUPPORTED", "production_frq", "Chain choice, effect, and purpose (with a frame)",
             ref="", bank="douglass_1852", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on reaching the purpose. Pick one Douglass choice "
                       "(the repeated 'your,' the pointed questions, or the ideals-versus-practice contrast).",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "Douglass ______ [the choice], which ______ [its effect on the audience] "
                                         "so that ______ [the purpose that effect serves]."),
                 closer="Fill all three blanks. The last blank is the one that matters most: reach the purpose, "
                        "do not stop at the effect. Then run the purpose check before you submit.")),
        # DIAGNOSIS = check-and-fix on a PROVIDED weak draft (not a fresh production, so it does not repeat the
        # supported write). Stays on the taught source = no new reading (load). Uses checklist() so the check
        # renders as one clean numbered list (no "Step N" double-numbering).
        Slot("MODEL", "diagnosis_frq", "Check the analysis: is the purpose reached?",
             ref="", bank="douglass_1852", scored=True,
             body=frq_prompt(
                 intro="Run the purpose check on this weak draft, then rewrite it into an analysis that reaches "
                       "the purpose behind the choice.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "Douglass asks pointed questions, which grabs the audience's attention.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Is the choice named?", "Yes, the pointed questions."),
                     ("Is the effect named?", "Yes, it grabs the audience's attention."),
                     ("Is the purpose reached (why he wants that effect)?", "No. It stops at the effect. Add why he wants their attention: so they must face a question they cannot answer without admitting the exclusion."),
                 ]),
                 closer="Now rewrite the weak draft into a short analysis that reaches the purpose the attention "
                        "serves. Then name which check question your rewrite fixed.")),

        # ===== INDEPENDENT: cold write, no frame, own choice of move + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Reach the purpose on your own",
             ref="", bank="douglass_1852", rubric_ref="rc.4trait", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now, no frame. Choose one Douglass choice you have not used yet and write a "
                       "short analytical passage that runs the full chain: the choice, its effect on the "
                       "audience, and the purpose that effect serves.",
                 closer="Before you submit, check all three links: choice named, effect named, and purpose "
                        "reached (not stopping at the effect). Reaching the purpose is what every real rhetorical "
                        "analysis is built on, and you are ready to do it cold. Run the purpose check before you "
                        "submit.")),

        # ===== TRANSFER: same move, a NEW source (Bryan 1896), bank-partitioned from the taught source =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: the \"Cross of Gold\" speech (1896)",
             ref="ACC-W910-RA-SINGLE-0002", bank="ra_speech_2",
             body=("Read this new speech excerpt. Because your job is to reach the purpose behind a choice, "
                   "notice the choices the speaker makes: the way he redefines who counts as a business man, the "
                   "pioneer passage, the repeated 'we have petitioned, we have entreated, we have begged,' and "
                   "the line 'We defy them.' Pick one and be ready to run choice, effect on the audience, and "
                   "purpose. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Reach the purpose on a NEW text",
             ref="", bank="ra_speech_2", rubric_ref="rc.4trait", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="New text, same move. Choose one of the speaker's choices in the \"Cross of Gold\" "
                       "excerpt and write a short analytical passage on it.",
                 closer="Run the full chain: name the choice, its effect on the audience, and the purpose that "
                        "effect serves. Do not stop at the effect. Run the purpose check before you submit.")),
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
