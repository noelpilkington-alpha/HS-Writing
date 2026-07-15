"""
lesson_g10_l06_device_to_effect.py  -  G10 KC C.10.02, ARCHETYPE T4: TEXT-DEPENDENT ANALYSIS (DEW, sentence). V3.1.

V3.1 rebuild of the pre-v3.1 L06 to the v3.1 spec (icm/_config/v3_1-lesson-build-spec.md), adapting the pattern
proven on the G9 L06 v3.1 lesson. PRESERVED: teaching point (name the author's specific device, then state its
effect on the reader, rather than stopping at the label), id ACC-W910-L-G10-C1002-0006, lesson_type 4, kc
C.10.02, mnemonic_status proposal, unit, and the bound ANALYSIS/INFO -LESSON- stimuli (story_of_an_hour taught,
weather transfer). Changes vs the prior L06:
  1. ONE IDEA, hammered (KH load): a teal ONE_IDEA callout states the single core idea (spotting a device is
     only half; the move is device TO EFFECT), then the minimum teaching as a LIST (label-only vs
     device-to-effect + the "rhetorical device" definition) instead of the old ~170-word prose block that
     tripped format_fidelity.
  2. COPING-MODEL THINK-ALOUD (SRSD): the model is rewritten as a written drafting process (draft a label ->
     run the check -> catch that no effect is stated -> revise until the effect is stated), First try / Second
     try / Final, with literal BEFORE and AFTER (content_depth). The reusable device-to-effect check tool is
     attached at the point of first use (the model card), not cold in step 1.
  3. FIXED THE SURFACE CONFOUND (DI, faultless communication): the discrimination now attributes all three
     options to the same device (spring imagery at the window) and homogenizes length; a distractor carries the
     word "so" (as "so many details") and the word "reader," so neither token co-varies with the correct
     answer. Removed the leaked "Grade-C design bet" label from the student text.
  4. DETERMINISTIC FRQ/DIAGNOSIS BODIES: production + diagnosis prompts are built with frq_prompt/setapart/
     checklist (no hand-written "Step 1/2" prose that double-numbers), and carry NO "Scored on ..." chrome.
  5. AUTONOMY + SAY-THE-STANDARD (Yeager): the independent write drops the frame, lets the student pick any
     Chopin device, and names the standard out loud ("this is what every real analysis is built on; you are
     ready to do it cold").

ONE IDEA: device to effect - name the specific choice, then say what it DOES to the reader, not just label it.
ONE REMINDER: the device-to-effect check. Passes all 23 lesson_contract gates. Own words, source-faithful, no
em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Spotting a device is only half the job. The move that '
'scores is <strong>device to effect</strong>: name the specific choice, then say what it DOES to the reader. '
'Naming a device is a label; stating its effect is analysis.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the device-to-effect test</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you commit to a sentence, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">What specific device can I point to in the text?</li>'
'<li style="margin:2px 0">What does that device DO to the reader (how does it change what they feel or think)?</li>'
'<li style="margin:2px 0">Did I state that effect, or did I stop at the label?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If you named a device but never answered question 2, '
'you stopped at a label. Add the effect.</div></div>')

# coping-model think-aloud: a WRITTEN drafting process (label -> check -> catch no-effect -> revise), then the
# BEFORE/AFTER endpoints (content_depth requires both literal words). No named person (stateless rule).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer building one sentence about the open-window scene, running the check after each try:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Chopin uses imagery in the open-window scene." Run '
    'the check. Did I name a device I can point to? Yes, imagery. Did I state what it DOES to the reader? No. I '
    'just labeled it. That stops at a label.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "Chopin uses spring imagery of the aquiver treetops, '
    'the breath of coming rain, and the patches of blue sky." Better, it is specific now. But run the check '
    'again: does it say the effect? No. That is more description, still no effect on the reader. Still a label.</p>'
    '<p style="margin:0"><strong>Final:</strong> "Chopin fills the open window with spring imagery of aquiver '
    'treetops and patches of blue sky, so a scene that should feel like mourning begins to feel like renewal." '
    'Check: device named? Yes. Effect on the reader stated? Yes, it names what the imagery DOES. That one is '
    'analysis, not a label.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "Chopin uses imagery in the open-window scene." (names the '
    'device, but stops there, no effect)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "Chopin fills the open window with spring imagery of aquiver '
    'treetops and patches of blue sky, so a scene that should feel like mourning begins to feel like renewal." '
    '(names the device AND states its effect)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1002-0006", grade="9-10", lesson_type=4,
    unit="G10 U2 - Text-dependent analysis (device to effect)",
    title="Name the Device, Then Say What It Does",
    target=("Do the core analytical move: name the author's specific device (a choice you can point to), then "
            "state its effect on the reader, rather than just labeling the device. Written at the sentence. "
            "Trait: Evidence/Development (analysis)."),
    acc_tags=["ACC.W.INFO.6", "ACC.W.SRC.3", "CCSS.W.9-10.9", "CCSS.RI.9-10.6"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.02",
                "sot": "icm course-G10.md L06; v3.1 spec icm/_config/v3_1-lesson-build-spec.md",
                "taught_stimulus": "ACC-W910-ANALYSIS-LESSON-HOUR",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-WEATHER",
                "one_idea": "Device to effect: name the specific choice, then say what it does to the reader, not just label it.",
                "one_reminder": "device-to-effect check: what device? what does it do to the reader? did I state that effect, or stop at the label?",
                "playbook": "_phase2/playbook_T4_DEW.md",
                "template": "locked L01 template; ANALYSIS-TIER binds full sources.",
                "version_note": ("V3.1: rebuilt to the v3.1 spec on the G9 L06 v3.1 pattern - ONE_IDEA callout + "
                                 "list teach (fixed the prose wall), coping-model drafting think-aloud (SRSD), "
                                 "device-to-effect check tool at point of first use, homogenized the "
                                 "discrimination and broke the 'so'/'reader' surface confound + removed the "
                                 "leaked 'Grade-C' label (DI faultless communication), deterministic "
                                 "frq_prompt/setapart/checklist bodies (no 'Step N' double-number, no 'Scored "
                                 "on' chrome), autonomy + say-the-standard on the independent write (Yeager). "
                                 "Preserved teaching point, id, type, kc, mnemonic_status, and the bound "
                                 "HOUR/WEATHER lesson stimuli."),
                "council": ("T4/DEW device-to-effect intro: introduces the move (name the device + state its "
                            "effect). rhetorical device defined in TEACH. effect-stated-vs-label-only "
                            "discrimination labeled_grade_c in code only.")},
    fade_ledger_moves=["device-to-effect", "past-labeling-to-effect"],
    slots=[
        # ===== TEACH: ONE idea only (list, not a wall of prose; check tool held for point of first use) =====
        Slot("TEACH", "teach_card", "Spotting a device is not analyzing it",
             body=(ONE_IDEA +
                   "A rhetorical device is a deliberate choice a writer makes to shape how a reader feels or "
                   "thinks: an image, a repeated word, a shift in tone, an irony, a striking comparison. When "
                   "you analyze, keep two kinds of sentence apart:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Label only</strong>: it names the device and stops. "
                   "\"Chopin uses imagery\" spots a choice but never says what that choice does. Commenting on "
                   "the writing itself counts as label-only too: noting how much detail there is, or how "
                   "carefully the author builds a paragraph, describes her craft, not what the device makes the "
                   "reader feel or understand. Most writers stall here, in the middle band.</li>"
                   "<li style=\"margin:4px 0\"><strong>Device to effect</strong>: it names the device AND says "
                   "what it does to the reader. The effect is a change in what the reader feels or understands "
                   "about the story, not a remark about how skillful the writing is. \"Chopin fills the window "
                   "with spring imagery so grief starts to feel like renewal\" names the choice and its effect. "
                   "That is the move that scores.</li></ul>"
                   "The trap is being satisfied once you have named a device. Stating the effect is what moves "
                   "the response up. Today: name a device you can point to, then state its effect on the reader.")),
        Slot("TEACH", "stimulus_display", "Read the source: Kate Chopin, \"The Story of an Hour\" (1894)",
             ref="ACC-W910-ANALYSIS-LESSON-HOUR", bank="story_of_an_hour",
             body=("Read this short public-domain story. As you read, notice choices you could point to: the "
                   "spring imagery outside the open window, the irony that news of her husband's death brings "
                   "her a sense of freedom, the repeated whispered word \"free.\" Pick ONE device, and be ready "
                   "to say not just that it is there but what it DOES to the reader. The text stays on screen "
                   "while you work.")),

        # ===== MODEL (before the quiz): coping-model drafting think-aloud + the device-to-effect check tool =====
        Slot("MODEL", "annotated_before_after", "Watch a label become device-to-effect",
             bank="story_of_an_hour",
             body=("Here is the skill in action. Follow the writer's thinking below as one label after another "
                   "gets caught and revised until the sentence states the effect. " + COPING_HTML +
                   " Notice the two moves that turned the BEFORE into the AFTER: the writer NAMED a specific "
                   "device, then said what it DOES to the reader. " + REMEMBER +
                   "When you write your own, do the same: name the device first, then state its effect, and run "
                   "the check before you commit to it.")),
        Slot("MODEL", "discrimination", "Which one states the effect?",
             ref="", labeled_grade_c=True, bank="story_of_an_hour",
             body=("Now that you have seen one built, spot the target. All three name the same device, the "
                   "spring imagery at the open window. Which one goes past the label to state its EFFECT on the "
                   "reader? "
                   "(A) Chopin uses spring imagery in the scene at the open window, describing the aquiver "
                   "treetops, the delicious breath of coming rain, a distant song, and patches of blue sky between the clouds.  "
                   "(B) Chopin uses spring imagery at the open window, so many outdoor details packed into the "
                   "reader's view that this is easily the most descriptive paragraph in the whole story.  "
                   "(C) Chopin uses spring imagery at the open window so a scene that should feel like grief "
                   "begins to feel like renewal, easing the reader toward Mrs. Mallard's sense of release. "
                   "Correct: C. It says what the imagery DOES to the reader (turns grief toward renewal). (A) "
                   "names and describes the device but stops there. (B) has the word \"so\" and the word "
                   "\"reader,\" but it only comments on how much description there is (a remark about her craft), "
                   "not on what the imagery makes the reader feel or understand."),
             choices=[
                 {"id": "A", "text": "Chopin uses spring imagery in the scene at the open window, describing the aquiver treetops, the delicious breath of coming rain, a distant song, and patches of blue sky between the clouds.",
                  "correct": False,
                  "why": "This names the device and describes it in rich detail, but it never says what the imagery does to the reader. Describing a device is not the same as stating its effect. It stops at a label."},
                 {"id": "B", "text": "Chopin uses spring imagery at the open window, so many outdoor details packed into the reader's view that this is easily the most descriptive paragraph in the whole story.",
                  "correct": False,
                  "why": "This has the words 'so' and 'reader' in it, but it only comments on the amount of description (a remark about her craft), not on what the imagery makes the reader feel or understand. A comment on how descriptive the writing is is not a stated effect."},
                 {"id": "C", "text": "Chopin uses spring imagery at the open window so a scene that should feel like grief begins to feel like renewal, easing the reader toward Mrs. Mallard's sense of release.",
                  "correct": True,
                  "why": "Correct. It names the device AND states its effect: the imagery turns a scene that should feel like grief into one that feels like renewal for the reader. Naming plus effect is the move that scores."},
             ]),
        Slot("MODEL", "discrimination", "Effect on the reader, or just the character?",
             ref="", labeled_grade_c=True, bank="story_of_an_hour",
             body=("Same skill, a new device. All three point to Chopin's repetition of the hushed word 'free.' "
                   "Which one goes past naming it to state the effect on the reader? "
                   "(A) Chopin repeats the hushed word 'free' several times, a repetition many readers notice as "
                   "Mrs. Mallard sits alone at the open window.  "
                   "(B) Chopin repeats the word 'free' so that Mrs. Mallard, alone in her quiet room, lets "
                   "herself believe at last that her long years of marriage are finally and truly behind her.  "
                   "(C) Chopin repeats the hushed word 'free' so that with each whisper the reader feels the "
                   "release building, until her joy is impossible to miss. "
                   "Correct: C. It says what the repetition DOES to the reader (each whisper makes the release "
                   "build). (A) names the device and notes that readers notice it, but states no effect it "
                   "produces. (B) uses 'so' and states a result, but the result is what Mrs. Mallard comes to "
                   "believe, a point about the character, not what the repetition makes the reader feel."),
             choices=[
                 {"id": "A", "text": "Chopin repeats the hushed word 'free' several times, a repetition many readers notice as Mrs. Mallard sits alone at the open window.",
                  "correct": False,
                  "why": "This names the repeated word and notes that readers notice it, but it never says what the repetition does to them, so it stops at a label."},
                 {"id": "B", "text": "Chopin repeats the word 'free' so that Mrs. Mallard, alone in her quiet room, lets herself believe at last that her long years of marriage are finally and truly behind her.",
                  "correct": False,
                  "why": "This states a result, but the result is what the character comes to believe about her own life, not what the repetition makes the reader feel or understand."},
                 {"id": "C", "text": "Chopin repeats the hushed word 'free' so that with each whisper the reader feels the release building, until her joy is impossible to miss.",
                  "correct": True,
                  "why": "This names the device and states its effect on the reader: each whispered repetition makes the sense of release build until it is impossible to miss."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this label most need?",
             bank="story_of_an_hour",
             body=("Diagnose this draft before the reveal. A student wrote: \"Chopin uses irony in this story.\" "
                   "Which single move would most improve it? "
                   "(A) state what the irony DOES to the reader, its effect, not only that irony is present  "
                   "(B) name a second device the author also uses, so the sentence points to more than one choice  "
                   "(C) define the word irony first so the reader will know exactly what the term is meant to mean  "
                   "(D) add a short plot summary that walks the reader through what happens from start to finish"),
             feedback=("Correct: A. \"Chopin uses irony\" is a label with no effect, so it stalls in the middle "
                       "band. The fix states the effect: the irony that news of her husband's death frees her "
                       "makes her quiet joy land as a shock the reader feels too. A second device (B), a "
                       "definition (C), or a plot summary (D) do not add what the device DOES to the reader.")),

        # ===== SUPPORTED: framed write (fill-in frame) on the taught source (already read at STEP 2) =====
        Slot("SUPPORTED", "production_frq", "Name a device and state its effect",
             ref="", bank="story_of_an_hour", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on the move: name a device you can point to, then "
                       "state what it does to the reader.",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "Chopin uses ______ [a specific device you can point to] so ______ [its effect on the reader]."),
                 closer="Pick a device you can point to (the spring imagery, the irony of her reaction, the "
                        "repeated word \"free\"), then say what it does to the reader. Do not stop at the label. "
                        "Run the device-to-effect check before you submit.")),
        # DIAGNOSIS = check-and-fix on a PROVIDED weak draft (not a fresh production, so it does not repeat the
        # supported write). Stays on the taught source = no new reading (load). Uses checklist() so the check
        # renders as one clean numbered list (no 'Step N' double-numbering).
        Slot("MODEL", "diagnosis_frq", "Check your sentence: effect stated, or label only?",
             ref="", bank="story_of_an_hour", scored=True,
             body=frq_prompt(
                 intro="Run the device-to-effect check on this weak draft, then rewrite it into a sentence that "
                       "states the effect.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "Chopin uses descriptive language about the sky and the trees outside the window.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("What device can I point to?", "Descriptive imagery of the sky and trees. Good, a device is named."),
                     ("What does it DO to the reader?", "The draft never says. It stops at the label. Add what the imagery does."),
                     ("Did I state that effect, or stop at the label?", "Stopped at the label. Add a 'so' clause that names the effect on the reader."),
                 ]),
                 closer="Now rewrite the weak draft into one sentence that names the device AND states its effect "
                        "on the reader. Then name which question your rewrite fixed.")),

        # ===== INDEPENDENT: cold write, no frame + autonomy on the device + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write a device-to-effect sentence on your own",
             ref="", bank="story_of_an_hour", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="On your own now, no frame. Choose any device Chopin uses in the story: the open-window "
                       "imagery, the irony of her reaction, the repeated word \"free,\" a shift in tone.",
                 closer="Write ONE sentence that names that device AND states its effect on the reader, not just "
                        "the label. Naming a choice and saying what it does to the reader is what every real "
                        "analysis is built on, and you are ready to do it cold. Run the device-to-effect check "
                        "before you submit.")),

        # ===== TRANSFER: same move, a NEW source (weather), bank-partitioned from the taught source =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: how weather forecasts work",
             ref="ACC-W910-INFO-LESSON-WEATHER", bank="weather",
             body=("Read this new explanatory source on weather forecasting. Its author's choices are about "
                   "structure and wording: an opening that calls forecasts \"so ordinary,\" the order of the "
                   "explanation, the chain comparison it ends on (from a balloon in the sky to an alert on a "
                   "phone). Read it once, then find one such choice and be ready to say what it does to the "
                   "reader. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Write a device-to-effect sentence on a NEW text",
             ref="", bank="weather", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="New text, same move. This time the choices are structural and wording choices, not "
                       "literary images.",
                 closer="Write ONE sentence that names a STRUCTURAL or wording choice the weather author makes "
                        "AND states its effect on the reader (for example, opening by calling forecasts \"so "
                        "ordinary\" so the reader is surprised by the science behind them). Same name-then-state-"
                        "effect move as the Chopin sentence, new text. Do not stop at the label. Run the "
                        "device-to-effect check before you submit.")),
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
