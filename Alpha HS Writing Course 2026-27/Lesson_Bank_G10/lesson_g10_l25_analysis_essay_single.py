"""
lesson_g10_l25_analysis_essay_single.py  -  G10 KC C.10.03, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD, ceiling essay). V3.1.

NEW G10 lesson (added per the design audit) built to the v3.1 build spec (hand-authored). Teaching point: plan and
write a complete SINGLE-TEXT analysis essay - an analytical thesis (a claim about the author's craft, not a
retelling), body paragraphs that each run device to effect to warrant, and an intro and conclusion. This is the
C.10.03 GATEWAY essay that the analysis strand (L04-L09) builds toward, BEFORE the cross-text essays. It reaches
the essay ceiling. ANALYSIS-TIER binds full sources; UNTIMED.

Spec (verbatim): id="ACC-W910-L-G10-C1003-0025", lesson_type=7, kc=C.10.03, mnemonic_status="proposal",
unit="G10 U4 - Single-text analysis essay (C.10.03 gateway)". taught_stimulus=ACC-W910-ANALYSIS-LESSON-HOUR
(Kate Chopin, "The Story of an Hour", 1894); transfer_stimulus=ACC-W910-ANALYSIS-LESSON-DOUGLASS (Frederick
Douglass, "What to the Slave Is the Fourth of July?", 1852). rubric_ref="rc.staar" on the scored production_frq
slots (G10; "rc.ap" is the G11 variant). SUPPORTED plan = multi_paragraph; INDEPENDENT + TRANSFER = essay; the
unit ladder climbs to the essay, the type-7 ceiling.

Own words, quotes verbatim from the bound sources, no fabricated figures, no em dashes, no named HTML entities.
Passes all lesson_contract gates + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A single-text analysis essay does not retell what a text '
'says. It makes <strong>one analytical thesis</strong> about how the author writes, and every body paragraph '
'proves that thesis by running <strong>device to effect to warrant</strong>.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: reread the essay</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, reread the whole essay and ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Is the thesis a claim about the author\'s craft, not a plot summary?</li>'
'<li style="margin:2px 0">Does every body paragraph run device to effect to warrant, tied to the thesis?</li>'
'<li style="margin:2px 0">Is each device a real quoted or named choice from the text, not a topic?</li>'
'<li style="margin:2px 0">Does the conclusion say why the craft matters instead of repeating the thesis?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you submit.</div></div>')

# coping-model before/after: a plot retelling rebuilt into one analytical thesis proved with device-effect-warrant.
# Contains BOTH a literal BEFORE and AFTER (content_depth). Quotes are verbatim from the bound Chopin source.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> retells the plot, then rates the story</span>'
    '<p style="margin:8px 0 0;font-size:15px"><i>Thesis:</i> "The Story of an Hour" is about a woman who hears '
    'her husband died and then feels free. <i>Body:</i> First she cries in her sister\'s arms, then she goes to '
    'her room and looks out the window and starts to feel better, and she keeps saying she is free. <i>Conclusion:</i> '
    'So the story is about a woman who finds out her husband died and ends up feeling free.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The thesis just summarizes the plot, the body walks '
    'through events in order, and the conclusion repeats the summary. No authorial choice is named and no claim '
    'about craft is proved.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> one analytical thesis, proved with device to effect to warrant</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">THESIS</span> Chopin frames Mrs. Mallard\'s turn toward freedom with images of new life '
      'so that a forbidden joy reads as something natural rather than monstrous. '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">DEVICE + EFFECT + WARRANT</span> Just as the feeling reaches her, Chopin fills the window '
      'with spring: the "tops of trees that were all aquiver with the new spring life" and "the delicious breath '
      'of rain." The outside world is bursting into renewal at the exact moment she whispers "free, free, free!" '
      'By tying her private awakening to visible new life, Chopin makes the reader feel the freedom as growth, '
      'which is why the moment lands as release and not betrayal.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same story, but now the thesis claims something about '
    'Chopin\'s craft, the body quotes a real device and names its effect, and the warrant explains why that '
    'choice serves her purpose. That is analysis.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1003-0025", grade="9-10", lesson_type=7,
    unit="G10 U4 - Single-text analysis essay (C.10.03 gateway)",
    title="Write a Single-Text Analysis Essay",
    target=("Plan and write a complete single-text analysis essay: an analytical thesis about the author's craft "
            "(not a retelling), body paragraphs that each run device to effect to warrant, and an intro and "
            "conclusion. Written at the essay. Trait: Evidence/Development/Organization."),
    acc_tags=["ACC.W.INFO.6", "ACC.W.SRC.3", "CCSS.W.9-10.9", "CCSS.RL.9-10.4"],
    provenance={"copyright": "own_authored", "authored": "2026-07-14", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.03", "sot": "icm course-G10.md (design audit add)",
                "unit-context": "G10 U4 - Single-text analysis essay (C.10.03 gateway)",
                "taught_stimulus": "ACC-W910-ANALYSIS-LESSON-HOUR",
                "transfer_stimulus": "ACC-W910-ANALYSIS-LESSON-DOUGLASS",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": "v3.1 spine; ANALYSIS-TIER binds full sources; UNTIMED (no Timeback timer).",
                "one_idea": "A single-text analysis essay makes ONE analytical thesis about craft and proves it with device-effect-warrant.",
                "one_reminder": "Reread check: thesis about craft not plot? every paragraph device-effect-warrant? real quoted devices? conclusion earns an upshot?",
                "version_note": ("NEW lesson added per the design audit: the C.10.03 gateway single-text analysis "
                                 "essay was missing between the analysis strand (L04-L09) and the cross-text "
                                 "essays. Built to the G9 L23 / G10 L21 v3.1 pattern: ONE_IDEA teal callout + real "
                                 "<ul>/<ol> teach lists (no walls), coping-model before/after with literal BEFORE "
                                 "and AFTER quoted from the bound Chopin source, discrimination with explicit "
                                 "choices=[] (no leaked internal label), predict-the-fix, then the SUPPORTED plan "
                                 "(multi_paragraph), diagnosis check, INDEPENDENT essay, and a TRANSFER essay on "
                                 "the Douglass text. rubric_ref=rc.staar on the scored writes (G10; rc.ap is the "
                                 "G11 variant). Preserved id, type 7, kc=C.10.03, mnemonic_status=proposal, unit."),
                "review_provenance": "built to the G10 L21 v3.1 pattern; lesson_contract gates + render-qc clean"},
    fade_ledger_moves=["single-text-analysis-essay", "analytical-thesis-not-summary"],
    slots=[
        # ===== TEACH: the one idea + the parts (as a list), then the order of work (as a list) =====
        Slot("TEACH", "teach_card", "The one idea: an analytical thesis, proved by device to effect to warrant",
             body=(ONE_IDEA +
                   "You have practiced each of these moves on a single line or paragraph. A full analysis essay "
                   "puts them together, in these parts:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>The analytical thesis</strong>: an analytical thesis is a "
                   "one-sentence claim about how the author writes and to what end, not a summary of what happens.</li>"
                   "<li style=\"margin:4px 0\"><strong>A device</strong>: a device is a specific technique the "
                   "author chooses on purpose, such as an image, an ironic reversal, a repeated word, or point of "
                   "view.</li>"
                   "<li style=\"margin:4px 0\"><strong>The effect</strong>: the effect means what that device does "
                   "to the reader, what it makes the reader feel, notice, or realize.</li>"
                   "<li style=\"margin:4px 0\"><strong>The warrant</strong>: a warrant is a sentence that explains "
                   "why that effect serves the author's purpose, tying the device back to the thesis.</li></ul>"
                   "The trap is retelling the plot instead of proving a claim about craft. Plan the thesis first, "
                   "then build.")),
        Slot("TEACH", "teach_card", "How to build it, part by part",
             body=("Here is the order of work. Follow it and the essay assembles itself from moves you already "
                   "own:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>PLAN</strong>: write the analytical thesis, then two or "
                   "three devices you will analyze, each with the effect it creates.</li>"
                   "<li style=\"margin:4px 0\"><strong>INTRO</strong>: name the author and text, and state the one "
                   "analytical thesis.</li>"
                   "<li style=\"margin:4px 0\"><strong>BODY</strong>: write one paragraph per device, each running "
                   "device to effect to warrant, and open each paragraph after the first with a transition linking "
                   "it to the thesis.</li>"
                   "<li style=\"margin:4px 0\"><strong>CONCLUSION</strong>: land why the craft matters instead of "
                   "repeating the thesis.</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: reread against a short list, is the thesis "
                   "about craft and not plot, does every paragraph run device to effect to warrant, is each device "
                   "a real choice from the text?</li></ol>"
                   "You are assembling moves you already own, in this order, into one analytical essay.")),
        Slot("TEACH", "stimulus_display", "Read the source: Kate Chopin, \"The Story of an Hour\" (1894)",
             ref="ACC-W910-ANALYSIS-LESSON-HOUR", bank="story_of_an_hour",
             body=("Read this excerpt from Kate Chopin's 1894 short story \"The Story of an Hour.\" Because your "
                   "job is to write a full analysis essay from it, read the whole excerpt and gather two or three "
                   "authorial choices you could analyze: the spring imagery "
                   "outside the open window, the irony of grief turning to relief, the repetition of the word "
                   "free, or the point of view that lets the reader inside Mrs. Mallard's thoughts. The text "
                   "stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + check tool, then discrimination + predict =====
        Slot("MODEL", "annotated_before_after", "Watch a plot retelling become an analysis",
             bank="story_of_an_hour",
             body=("Here is the difference between retelling a story and analyzing it. Read the BEFORE, then the "
                   "AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE summarizes the plot and rates the story. The AFTER makes one claim about a choice "
                   "Chopin makes and proves it with a quoted device, its effect, and a warrant. An analytical "
                   "thesis proved by device to effect to warrant is the move." + REMEMBER +
                   "When you build your own, put the parts in this order, then run the check before you submit.")),
        Slot("MODEL", "discrimination", "Which one is a single-text analysis?",
             ref="", labeled_grade_c=True, bank="story_of_an_hour",
             body=("You have watched a plot retelling become an analysis. Now spot the target: which of these is "
                   "an analysis of Chopin's craft? "
                   "(A) The essay states one analytical thesis about a choice Chopin makes, then each body "
                   "paragraph quotes a device, names its effect on the reader, and gives a warrant tying that "
                   "effect to the thesis.  "
                   "(B) The essay walks through the story from the news of the death, to the room, to the window, "
                   "to the final line, carefully retelling each event in the order it happens and adding that the "
                   "story was moving and beautifully written.  "
                   "(C) The essay opens with a long paragraph explaining who Kate Chopin was and when she lived, "
                   "then briefly mentions that the story uses imagery, without ever quoting a line or saying what "
                   "any image does to the reader. "
                   "Correct: A. It states one analytical thesis and proves it with quoted device, effect, and "
                   "warrant; B retells the plot and rates it, and C gives biography and a label with no analyzed "
                   "evidence."),
             choices=[
                 {"id": "A", "text": "The essay states one analytical thesis about a choice Chopin makes, then each body paragraph quotes a device, names its effect on the reader, and gives a warrant tying that effect to the thesis.",
                  "correct": True,
                  "why": "Correct. One analytical thesis about craft, proved with quoted device to effect to warrant in each paragraph, is a single-text analysis."},
                 {"id": "B", "text": "The essay walks through the story from the news of the death, to the room, to the window, to the final line, carefully retelling each event in the order it happens and adding that the story was moving and beautifully written.",
                  "correct": False,
                  "why": "This is a plot retelling plus a rating. It never names an authorial choice or proves a claim about how the text works."},
                 {"id": "C", "text": "The essay opens with a long paragraph explaining who Kate Chopin was and when she lived, then briefly mentions that the story uses imagery, without ever quoting a line or saying what any image does to the reader.",
                  "correct": False,
                  "why": "Biography plus an unproven label is not analysis. A device must be quoted and its effect explained, then tied to the thesis with a warrant."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this analysis draft most need?",
             bank="story_of_an_hour",
             body=("Diagnose before the reveal. A draft opens with 'This story is about a woman who learns her "
                   "husband died and then feels free,' and each paragraph retells the next event. Which single "
                   "move would most improve it as a single-text analysis? "
                   "(A) rewrite the thesis as a claim about a choice Chopin makes, then prove it with a quoted "
                   "device, its effect, and a warrant in each paragraph  "
                   "(B) retell the plot in even fuller detail so the reader can follow every single thing that "
                   "happens in the story from beginning to end  "
                   "(C) add a long opening paragraph about Kate Chopin's life and the year the story was first "
                   "published so the essay has more background up front  "
                   "(D) swap in bigger, more impressive vocabulary words throughout so the writing sounds smarter "
                   "and more advanced to the reader"),
             feedback=("Correct: A. Retelling the plot is the most common cause of essays that never analyze. The "
                       "fix is a thesis about an authorial choice, proved with quoted device to effect to warrant "
                       "in each paragraph. A fuller retelling (B), added biography (C), or bigger words (D) do not "
                       "turn the draft into a claim about craft with evidence.")),

        # ===== SUPPORTED: plan the analysis (multi_paragraph) - the frame is the highest-value scaffold =====
        Slot("SUPPORTED", "production_frq", "Plan the analysis: thesis plus two or three devices",
             ref="", bank="story_of_an_hour", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Plan your analysis of the excerpt from \"The Story of an Hour\" before you write a word of it.",
                 setapart_block=setapart("Fill in this plan:",
                                         "Thesis: ______ (a claim about a choice Chopin makes, and to what end). Device 1: ______, effect ______. Device 2: ______, effect ______. Device 3 (optional): ______, effect ______."),
                 closer="Write one analytical thesis about how Chopin writes, then name two or three devices you "
                        "will analyze, each with the effect it creates on the reader. Do not plan a plot summary. "
                        "This plan is what you will build the essay from.")),
        # DIAGNOSIS = self-revision of the student's OWN just-written draft (not a check on a provided weak
        # draft). Same taught source (load balance). Scaffolded by the 3-row checklist run on their own essay.
        Slot("MODEL", "diagnosis_frq", "Check your essay: a claim about craft, not a summary?",
             ref="", bank="story_of_an_hour", scored=True,
             body=frq_prompt(
                 intro="Reread the essay you just wrote. Run this checklist on YOUR draft and fix any line that fails.",
                 checklist_block=checklist(title="Check your own draft, row by row:", rows=[
                     ("Is the thesis a claim about a choice the author makes?", "If it rates the story or summarizes the plot, name what Chopin does on purpose and to what end, such as pairing the news of the death with spring imagery."),
                     ("Is each device a real authorial choice, not an event?", "If a line just reports something that happens, name the device instead: the spring imagery, the irony of grief turning to relief, or the repetition of the word free."),
                     ("Is an effect tied to each device?", "If a device sits there unexplained, say what it makes the reader feel or realize, then add a warrant on why it matters."),
                 ]),
                 closer="For every row that fails on your draft, fix it in the essay before you submit. Finish by "
                        "naming which part your essay still needs most.")),

        # ===== INDEPENDENT: build the whole analysis essay from the plan (essay ceiling) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write the full single-text analysis essay",
             ref="", bank="story_of_an_hour", rubric_ref="rc.staar", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now, build the whole essay from your plan.",
                 closer="Write a complete analysis essay on the excerpt from \"The Story of an Hour\": an "
                        "introduction that names the author and text and states one analytical thesis, body "
                        "paragraphs that each run "
                        "device to effect to warrant (each device quoted from the text and tied back to the "
                        "thesis), and a conclusion that lands why the craft matters. Then run the reread check and "
                        "fix any part that fails. An analytical thesis proved with device to effect to warrant is "
                        "what every real analysis essay is built on, and you are ready to do it cold. Take the "
                        "time you need.")),
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
