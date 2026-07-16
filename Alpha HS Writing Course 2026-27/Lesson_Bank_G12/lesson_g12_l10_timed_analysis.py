"""
lesson_g12_l10_timed_analysis.py  -  G12 KC C.12.02, ESSAY-ASSEMBLY (BUILD, ceiling essay). V3.1.

G12 course L10 (Unit 2, build), rebuilt to the v3.1 build spec (hand-authored). Teaching point (KEPT):
rehearse a COMPLETE AP rhetorical-analysis essay under a self-imposed budget, capping annotation and pacing
the writing so a situated, choice-to-effect analysis is finished end to end, rather than over-reading and
rushing. Delivery UNTIMED (transferable pacing strategy). ANALYSIS-TIER binds a cold-to-G12 speech.
Taught: ra_speech_1 (RA-SINGLE-0001, FDR First Inaugural) -> transfer: ra_speech_2 (RA-SINGLE-0002, Bryan
Cross of Gold). This is a FULL-ANALYSIS ESSAY lesson (essay-assembly), so lesson_type=7.

Preserved EXACTLY from the prior L10: id="ACC-W910-L-G12-C1202-0010", lesson_type=7, kc="C.12.02",
mnemonic_status="proposal", unit, the bound stimuli (RA-SINGLE-0001 taught -> RA-SINGLE-0002 transfer), the
teaching point, and every production_frq unit= value (SUPPORTED plan = multi_paragraph, INDEPENDENT +
TRANSFER = essay). The unit ladder climbs to the essay, the type-7 ceiling.

V3.1 changes vs the prior L10:
  1. FIXED the leaked internal label: the discrimination no longer says "a Grade-C design bet we label as a
     bet"; it is a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}].
  2. FIXED the two wall-of-text teach cards: replaced with a ONE_IDEA callout + real <ul>/<ol> lists of the
     parts and the order of work (format_fidelity, "parallel items as a list").
  3. Deterministic FRQ + diagnosis prompts via frq_prompt/setapart/checklist (no "Step 1/2" prose, no
     "Scored on ..." chrome); coping-model before/after kept; the reread check tool folded in as a REMEMBER box.
Own words, no fabricated figures, faithful to the bound public-domain source. No em dashes. Runs QC.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A complete rhetorical analysis is a <strong>paced '
'build, not an endless read</strong>: cap the reading, then spend most of your time writing an analysis that '
'ties each choice to its effect and reaches the purpose. Over-reading is what leaves the essay unfinished.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: reread the analysis</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, reread the whole analysis and ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does each body paragraph name a real choice the speaker makes?</li>'
'<li style="margin:2px 0">Does it tie that choice to its effect on the audience?</li>'
'<li style="margin:2px 0">Does the analysis reach the speaker\'s purpose, not stop at a retell?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you submit.</div></div>')

# coping-model before/after: an over-annotated approach (a retell that names no choice) rebuilt into a paced,
# situated analysis. Contains BOTH a literal BEFORE and AFTER (content_depth). Faithful to the bound FDR text.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> summary of what the speaker says</span>'
    '<p style="margin:8px 0 0;font-size:15px">Roosevelt tells the country that the only thing to fear is fear '
    'itself, lists the hardships people are facing, and says the nation must act now to put people back to '
    'work.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">A writer who spends the window marking the speech '
    'often has time only to retell it. This names no choice and no effect, so it stays summary, not analysis.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> analysis of a choice and its effect</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">CHOICE</span> By naming the enemy as "fear itself" rather than the ruined markets and '
      'lost savings around his listeners, '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">EFFECT</span> Roosevelt shrinks an overwhelming collapse into a single feeling the '
      'audience can master, steadying citizens who are on the edge of panic, '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">PURPOSE</span> so that a frightened nation will trust his leadership and accept the '
      'vigorous federal action he is about to demand.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same speech, but this names a choice, ties it to its '
    'effect on the audience, and reaches the purpose. That is a finished analysis, not a summary.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G12-C1202-0010", grade="9-10", lesson_type=7,
    unit="G12 U2 - Sustain a full rhetorical-analysis FRQ",
    title="Rehearse a Complete Rhetorical Analysis, End to End",
    target=("Rehearse a full AP rhetorical-analysis essay under a self-imposed budget, capping annotation and "
            "pacing the writing so a situated, choice-to-effect analysis is finished end to end, rather than "
            "over-reading and rushing. Delivery untimed. Written at the essay. Trait: Sophistication, Evidence "
            "and Commentary, and process."),
    acc_tags=["ACC.W.INFO.6", "ACC.W.PROD.4", "CCSS.W.11-12.9", "CCSS.RI.11-12.6"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.12.02", "sot": "icm course-G12.md L10",
                "taught_stimulus": "ACC-W910-RA-SINGLE-0001",
                "transfer_stimulus": "ACC-W910-RA-SINGLE-0002",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": ("v3.1 spine; ANALYSIS-TIER binds cold-to-G12 speech; full RA FRQ rehearsal under own "
                             "budget; Timeback delivery UNTIMED. Grain: full analysis essay = essay-assembly -> "
                             "lesson_type=7."),
                "one_idea": "A complete rhetorical analysis is a paced build, not an endless read: cap the reading, pace the writing.",
                "one_reminder": "Reread check: each paragraph names a real choice? ties it to an effect? reaches the purpose?",
                "version_note": ("V3.1 rebuild of L10. FIXED the leaked internal label (removed 'a Grade-C design "
                                 "bet we label as a bet' from the discrimination, moved to explicit choices=[]); "
                                 "broke the wall-of-text teach cards into a ONE_IDEA callout + real <ul>/<ol> lists "
                                 "(format_fidelity); deterministic frq_prompt/setapart/checklist bodies (no "
                                 "'Step 1/2' prose, no 'Scored on' chrome); coping-model before/after kept; reread "
                                 "check folded in as a REMEMBER box. Preserved id, type 7, kc C.12.02, "
                                 "mnemonic_status=proposal, unit, bound stimuli, and every production_frq unit= "
                                 "value (SUPPORTED=multi_paragraph, INDEPENDENT/TRANSFER=essay)."),
                "council": ("T7/BUILD G12 sustain build: full rhetorical-analysis FRQ rehearsal end to end under "
                            "budget, delivery untimed. paced-vs-over-annotate discrimination labeled Grade-C in "
                            "code only. BUILD=proposal; unit=essay."),
                "review_provenance": "built to the G9 L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["full-analysis-rehearsal", "cap-annotation-pace-the-writing"],
    slots=[
        # ===== TEACH: the one idea + the parts (as a list), then the order of work (as a list) =====
        Slot("TEACH", "teach_card", "The one idea: cap the reading so the analysis gets written",
             body=(ONE_IDEA +
                   "You have practiced choice-to-effect analysis on single paragraphs. A full rehearsal puts the "
                   "whole essay together in one paced sitting, and the first trap is over-reading: every extra "
                   "minute spent marking the speech is a minute the analysis does not get written. A paced "
                   "rehearsal has four parts:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Cap the reading</strong>: read only until you can name the "
                   "situation and two or three choices worth analyzing, then stop. A rhetorical analysis means "
                   "explaining the choices a speaker makes and the effect each one has on the audience.</li>"
                   "<li style=\"margin:4px 0\"><strong>Situated introduction</strong>: place the reader in the "
                   "moment of the speech and state a thesis. A thesis is a one-sentence line that names the "
                   "choices you will analyze and the overall effect they create.</li>"
                   "<li style=\"margin:4px 0\"><strong>Body paragraphs</strong>: one choice each, tied to its "
                   "effect on the listeners.</li>"
                   "<li style=\"margin:4px 0\"><strong>Conclusion</strong>: reach the speaker's purpose, the "
                   "goal the choices serve.</li></ul>"
                   "The failure mode is a beautifully marked speech and a one-paragraph essay. Cap the reading; "
                   "pace the writing.")),
        Slot("TEACH", "teach_card", "The order of work, part by part",
             body=("Here is the order of work for a paced rehearsal. The rhetorical situation is when you know "
                   "who is speaking, to whom, on what occasion, and toward what purpose. Follow this order and "
                   "most of your time goes to writing, not marking:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>BUDGET AND READ</strong>: cap the reading; find the "
                   "situation and two or three choices, then stop reading.</li>"
                   "<li style=\"margin:4px 0\"><strong>PLAN</strong>: jot the thesis and the two or three choices "
                   "in the order you will analyze them.</li>"
                   "<li style=\"margin:4px 0\"><strong>DRAFT</strong>: a situated introduction, one body "
                   "paragraph per choice (name the choice, then its effect on the audience), and a conclusion "
                   "that reaches the purpose.</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: reread against a short list, does each "
                   "paragraph name a real choice, tie it to an effect, and reach the purpose?</li></ol>"
                   "You are pacing moves you already own into one finished analysis.")),
        Slot("TEACH", "stimulus_display", "Read the source: a speech to analyze",
             ref="ACC-W910-RA-SINGLE-0001", bank="ra_speech_1",
             body=("Read this speech excerpt. Picture a full rhetorical-analysis task: budget the reading to find "
                   "the rhetorical situation and the two or three choices worth analyzing, then plan the whole "
                   "analysis. Do not read forever. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + check tool, then discrimination + predict ==
        Slot("MODEL", "annotated_before_after", "Watch over-annotation become a paced analysis",
             bank="ra_speech_1",
             body=("Here is an over-annotated approach rebuilt into a paced full-write. Read the BEFORE, then the "
                   "AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE marks the speech and stalls at a retell. The AFTER caps the reading and finishes "
                   "a real analysis, naming a choice, its effect on the audience, and the purpose. Cap the "
                   "reading, pace the writing, is the move." + REMEMBER +
                   "When you write your own, put the parts in this order, then run the check before you submit.")),
        Slot("MODEL", "discrimination", "Which rehearsal finishes the analysis?",
             ref="", labeled_grade_c=True, bank="ra_speech_1",
             body=("You have watched an over-annotated attempt become a paced analysis. Now sort these before you "
                   "write: which rehearsal FINISHES the analysis, and which OVER-READS? "
                   "(A) Spend most of the working window annotating the speech, marking every appeal instead of picking a few choices, then write a single rushed paragraph and stop before the analysis is finished.  "
                   "(B) Budget the reading to find the rhetorical situation and two or three choices, then move to a fast plan and draft the whole analysis, choice to effect to purpose, and check it.  "
                   "(C) Budget almost no time for the reading, skim the speech once for its topic, then write a long personal opinion about the speaker's ideas instead of analyzing the choices. "
                   "Correct: B budgets the reading and paces the writing to a finished analysis; A spends the "
                   "window marking and never finishes; C skips the analysis for personal opinion."),
             choices=[
                 {"id": "A", "text": "Spend most of the working window annotating the speech, marking every appeal instead of picking a few choices, then write a single rushed paragraph and stop before the analysis is finished.",
                  "correct": False,
                  "why": "This over-reads. Marking the whole speech eats the window, so the essay is one rushed paragraph and never a finished analysis."},
                 {"id": "B", "text": "Budget the reading to find the rhetorical situation and two or three choices, then move to a fast plan and draft the whole analysis, choice to effect to purpose, and check it.",
                  "correct": True,
                  "why": "Correct. It caps the reading and paces the writing, so the situated, choice-to-effect analysis is finished end to end."},
                 {"id": "C", "text": "Budget almost no time for the reading, skim the speech once for its topic, then write a long personal opinion about the speaker's ideas instead of analyzing the choices.",
                  "correct": False,
                  "why": "This under-reads and drifts into opinion. With no choices found, there is nothing to analyze, so it is a reaction, not an analysis."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this analysis rehearsal most need?",
             bank="ra_speech_1",
             body=("Diagnose before the reveal. A writer produces pages of detailed annotations every time but "
                   "never a finished analysis, because the reading eats the whole window. Which single change "
                   "would most improve the result? "
                   "(A) budget the reading and start drafting once the situation and two or three choices are found  "
                   "(B) annotate the speech even more thoroughly, marking every appeal and figure of speech before any drafting begins  "
                   "(C) hunt for even more choices across the passage before deciding what to analyze  "
                   "(D) go back through the whole passage a third time to be sure no detail was missed"),
             feedback=("Correct: A. The problem is over-reading; the fix caps annotation and starts the writing "
                       "once the situation and a few choices are identified. More annotation (B), more choices "
                       "(C), or another pass through the passage (D) only crowd out the essay further.")),

        # ===== SUPPORTED: plan the analysis (multi_paragraph) - the frame is the highest-value scaffold =====
        Slot("SUPPORTED", "production_frq", "Budget the reading and plan the analysis",
             ref="", bank="ra_speech_1", rubric_ref="rc.ap", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Plan your rhetorical analysis of this speech before you write a word of the essay.",
                 setapart_block=setapart("Fill in this plan:",
                                         "Situation: ______ (speaker, audience, occasion). Choice 1: ______ + its effect. Choice 2: ______ + its effect. Choice 3: ______ + its effect. Thesis: ______."),
                 closer="Write your budget (with a capped reading share) and a fast plan: the rhetorical "
                        "situation, the two or three choices with the effect you will analyze for each, and a "
                        "one-line thesis. This plan is what leaves you time to finish the analysis.")),
        # ===== INDEPENDENT: rehearse the whole analysis from the plan (essay ceiling) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Rehearse the full analysis",
             ref="", bank="ra_speech_1", rubric_ref="rc.ap", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now, rehearse the whole analysis from the plan and budget you just checked, applying any process fix you named.",
                 closer="Write a complete rhetorical analysis of this speech end to end: a situated introduction "
                        "with a thesis, body paragraphs that each tie a choice to its effect on the audience, and "
                        "a conclusion that reaches the speaker's purpose. Then run the reread check. There is no "
                        "platform timer; run your own budget and capped reading. This is what every real "
                        "rhetorical analysis is built on, and you are ready to do it cold. Take the time you need.")),

        # DIAGNOSIS = self-check on the student's OWN just-written PLAN and budget (not a check on a provided
        # weak draft). The rows are pacing/process rows, so fixes carry into the NEXT write, not a finished
        # draft. Self-contained: the checklist is the scaffold and the grader scores the diagnosis within the item.
        Slot("MODEL", "diagnosis_frq", "Check the plan leaves time to finish",
             ref="", bank="ra_speech_1", scored=True,
             body=frq_prompt(
                 intro="Reread the plan and budget you just wrote. Run this checklist on it before you draft.",
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Is the reading capped to a small share of the time?", "If your budget gives the reading most of the window, cap it: read only until you have the situation and two or three choices."),
                     ("Are just two or three choices chosen, not every appeal?", "If the plan tries to cover every appeal, narrow it to the two or three choices with the clearest effect."),
                     ("Is time reserved to finish the analysis with a conclusion?", "If little time is left for drafting, reserve most of it to write choice to effect to purpose, conclusion included."),
                 ]),
                 closer="These are process fixes, not draft edits: for every line that fails, name in one sentence "
                        "what you will change about your budget or plan, and carry that adjustment into the full "
                        "analysis you are about to write. Finish by naming the two or three choices you will analyze.")),
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
