"""
lesson_g10_l04_analytical_claim.py  -  G10 KC C.10.02, ARCHETYPE T4: TEXT-DEPENDENT ANALYSIS (DEW, ceiling paragraph). V3.1.

V3.1 rebuild of the pre-v3.1 lesson to the v3.1 spec (icm/_config/v3_1-lesson-build-spec.md), on the pattern
proven by the G9 L06/L08 v3.1 lessons. PRESERVED: teaching point (read the task verb, then write an analytical
claim - a claim ABOUT the author's craft, a choice and its purpose, not a retelling of the content), id
ACC-W910-L-G10-C1002-0004, lesson_type=4, kc C.10.02, mnemonic_status proposal, unit, and the existing bound
-LESSON- stimuli (story_of_an_hour taught, interstate_highways transfer). Changes vs the prior L04:
  1. ONE IDEA, hammered (KH load): a teal ONE_IDEA callout states the single core idea (an analytical claim is
     about what the author is DOING, not what happens), then the minimum teaching as a LIST (craft claim vs
     summary) instead of the old 137-word prose block that tripped format_fidelity.
  2. COPING-MODEL THINK-ALOUD (SRSD): the model is rewritten as a writer drafting a claim -> running the craft
     check -> catching that it is still summary -> revising (First try / Second try / Final), with literal
     BEFORE and AFTER endpoints (content_depth). The reusable craft check tool is attached at the point of first
     use (the model card), not cold in the teach.
  3. REMOVED the leaked internal label: the prior discrimination said "a Grade-C design bet we label as a bet"
     in the student text (leaked_internal_label FAIL); labeled_grade_c stays True in code only.
  4. EXPLICIT DISCRIMINATION choices=[] with the author name present in every option (no surface-token confound)
     and distractors padded so the correct option is not the lone longest.
  5. DETERMINISTIC FRQ/DIAGNOSIS bodies via frq_prompt/setapart/checklist (no hand-written "Step 1/2" prose that
     double-numbers), and NO "Scored on ..." chrome.
  6. AUTONOMY + SAY-THE-STANDARD (Yeager): the independent write drops the frame, lets the student choose the
     choice, and names the standard out loud.

ONE IDEA: an analytical claim is a claim about what the author is DOING (a choice and its purpose), not a
retelling of what happens. ONE REMINDER: the craft check. Passes all 23 lesson_contract gates. Own words,
faithful to the bound public-domain source, no em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">An analytical claim is a claim about what the author '
'is <strong>DOING</strong>, a choice the author makes and the purpose behind it, not a retelling of what '
'happens. A sentence can be perfectly accurate about the plot and still not be analysis.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the craft check</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you commit to any claim, run this quick check:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">What choice did the author make (an image, a word, an order, a moment of irony)?</li>'
'<li style="margin:2px 0">What is that choice DOING, and to what end (its effect or purpose)?</li>'
'<li style="margin:2px 0">Is my claim about that craft, not just about what happens?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If your sentence only reports what happens, it is '
'summary. Name the choice AND its purpose to turn it into analysis.</div></div>')

# coping-model think-aloud panel: a WRITTEN drafting process (draft -> run the check -> catch the summary ->
# revise), then the BEFORE/AFTER endpoints (content_depth requires both literal words). Faithful to the source
# (spring trees, breath of rain, patches of blue sky, the whispered "free"): the real words are the material.
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer trying to write an analytical claim about the view through Mrs. Mallard\'s open window:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Mrs. Mallard sits by the open window and sees the '
    'spring trees, the rain, and the patches of blue sky." Run the check: is that about what Chopin is DOING, or '
    'about what happens? Just what happens. That is summary. Try again.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "Chopin describes the trees, the rain, and the blue '
    'sky outside the window." Better, it at least names Chopin describing something. But does it say to what END? '
    'No, it stops at reporting that she describes. Still not a claim about the craft.</p>'
    '<p style="margin:0"><strong>Final:</strong> "Chopin fills the window view with fresh spring imagery to tilt '
    'a scene of grief toward renewal, priming the reader for the sense of freedom Mrs. Mallard is about to feel." '
    'Run the check: it names the choice (the spring imagery) AND what it is doing (turning grief toward renewal). '
    'That is an analytical claim.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "Mrs. Mallard sits by the open window and sees the spring '
    'trees, the rain, and the patches of blue sky." (retells what happens)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "Chopin fills the window view with fresh spring imagery to tilt '
    'a scene of grief toward renewal." (claims the choice and its purpose)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1002-0004", grade="9-10", lesson_type=4,
    unit="G10 U2 - Text-dependent analysis (the analytical claim)",
    title="Claim What the Author Is Doing, Not Just What Happens",
    target=("Read the task verb (analyze vs summarize), then write an analytical claim: a claim ABOUT the "
            "author's craft (a choice and its purpose), not a retelling of the content. Written at the "
            "sentence. Trait: Evidence/Development (analysis)."),
    acc_tags=["ACC.W.INFO.6", "ACC.W.SRC.3", "CCSS.W.9-10.9", "CCSS.RI.9-10.6"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.02", "sot": "icm course-G10.md L04; v3.1 spec icm/_config/v3_1-lesson-build-spec.md",
                "taught_stimulus": "ACC-W910-ANALYSIS-LESSON-HOUR",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-HIGHWAYS",
                "one_idea": "An analytical claim is a claim about what the author is DOING (a choice and its purpose), not a retelling of what happens.",
                "one_reminder": "craft check: what choice did the author make? what is it doing, to what end? is my claim about the craft, not the plot?",
                "playbook": "_phase2/playbook_T4_DEW.md",
                "template": "locked L01 template; ANALYSIS-TIER binds full sources (verbatim PD text is the material).",
                "version_note": ("V3.1: rebuilt to the v3.1 spec on the G9 L06/L08 v3.1 pattern - ONE_IDEA callout "
                                 "+ list teach (fixed the 137-word wall-of-text that tripped format_fidelity), "
                                 "coping-model drafting think-aloud (SRSD) with First/Second/Final tries and "
                                 "literal BEFORE/AFTER, craft check tool at point of first use, removed the leaked "
                                 "'Grade-C design bet' label from the student text (kept labeled_grade_c in code), "
                                 "explicit discrimination choices=[] with the author name in every option (no "
                                 "surface-token confound) and the correct option not the lone longest, "
                                 "deterministic frq_prompt/setapart/checklist bodies (no 'Step N' double-number, "
                                 "no 'Scored on' chrome), autonomy + say-the-standard on the independent write. "
                                 "Preserved teaching point, id, KC, type, unit, and the bound HOUR/HIGHWAYS "
                                 "lesson stimuli."),
                "council": ("T4/DEW intro: introduces the decode (analyze vs summarize) + the analytical claim "
                            "(a claim ABOUT craft, not content). analysis-claim-vs-summary discrimination "
                            "labeled Grade-C internally. DEW=proposal; ceiling paragraph."),
                "review_provenance": ("23 lesson_contract gates (exit 0) + gated_reading render-QC clean.")},
    fade_ledger_moves=["decode-analyze-vs-summarize", "analytical-claim-about-craft"],
    slots=[
        # ===== TEACH: ONE idea only (list, not a wall of prose; craft check held for point of first use) =====
        Slot("TEACH", "teach_card", "Analyze means claim what the author is doing",
             body=(ONE_IDEA +
                   "An analysis task asks a different question than a summary. Read the task verb first: "
                   "'analyze' or 'how does the author ...' wants a claim about the craft; 'summarize' or 'what "
                   "happens' wants the content. Keep two kinds of sentence apart:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Analytical claim</strong>: it names a choice the author "
                   "makes AND the effect or purpose behind it. It answers what the author is DOING and why.</li>"
                   "<li style=\"margin:4px 0\"><strong>Summary</strong>: it retells what happens. It can be "
                   "completely accurate and still not be analysis, because it never says what the author is "
                   "doing.</li></ul>"
                   "The costly mistake on an analysis task is answering with summary, which caps the score no "
                   "matter how accurate it is. Today: decode the verb, then write a claim about the author's "
                   "craft, not about what happens.")),
        Slot("TEACH", "stimulus_display", "Read the source: Kate Chopin, \"The Story of an Hour\" (1894)",
             ref="ACC-W910-ANALYSIS-LESSON-HOUR", bank="story_of_an_hour",
             body=("Read this short public-domain story. Mrs. Mallard learns her husband has died, then sits "
                   "alone by an open window. Because your job is to ANALYZE the craft, read it once for what "
                   "happens, then again for one CHOICE Chopin makes, an image she lingers on, a moment of "
                   "irony, a repeated word, that you could make a claim about. The text stays on screen while "
                   "you work.")),

        # ===== MODEL (before the quiz): coping-model drafting think-aloud + the craft check tool =====
        Slot("MODEL", "annotated_before_after", "Watch a summary become an analytical claim",
             bank="story_of_an_hour",
             body=("Here is the skill in action. Follow the writer's thinking below as one summary sentence after "
                   "another gets caught and rebuilt until it becomes a claim about the craft. " + COPING_HTML +
                   " Notice the two moves that turned the BEFORE into the AFTER: the writer NAMED a choice Chopin "
                   "makes (the spring imagery), then claimed what that choice is DOING (turning grief toward "
                   "renewal). " + REMEMBER +
                   "When you write your own claim, do the same: name the choice, then name its purpose, and run "
                   "the craft check before you commit to it.")),
        Slot("MODEL", "discrimination", "Which one is an analytical claim?",
             ref="", labeled_grade_c=True, bank="story_of_an_hour",
             body=("Now that you have seen one built, spot the target. The task is to ANALYZE the story. All "
                   "three sentences below name Chopin. Which one is an analytical claim (about the craft), and "
                   "which are summary (about the content) or opinion? "
                   "(A) Chopin has Mrs. Mallard hear that her husband has died, weep at once in her sister's "
                   "arms, then go away to her room alone and sink into the comfortable, roomy armchair that faces "
                   "the wide open window.  "
                   "(B) Chopin fills the view through the open window with fresh spring imagery, tilting a scene "
                   "of grief toward renewal and priming the reader for the freedom Mrs. Mallard is about to feel.  "
                   "(C) Chopin wrote a moving and genuinely surprising story, and by the final line a great many "
                   "readers find that they are still thinking hard about it long after reaching the very last page.  "
                   "(D) Chopin uses imagery, irony, and symbolism at several points across the story. "
                   "Correct: B is analytical; A is summary, C is opinion, and D just lists devices. (A) retells "
                   "what happens. (C) judges the story overall. (D) names techniques in general but points to no "
                   "specific choice and no effect. (B) names a choice (the spring imagery) AND what it is doing "
                   "(turning grief toward renewal), which is the analytical claim."),
             choices=[
                 {"id": "A", "text": "Chopin has Mrs. Mallard hear that her husband has died, weep at once in her sister's arms, then go away to her room alone and sink into the comfortable, roomy armchair that faces the wide open window.",
                  "correct": False,
                  "why": "This retells what happens, step by step. It is accurate summary, but it never says what Chopin is DOING with any of it, so it is not an analytical claim."},
                 {"id": "B", "text": "Chopin fills the view through the open window with fresh spring imagery, tilting a scene of grief toward renewal and priming the reader for the freedom Mrs. Mallard is about to feel.",
                  "correct": True,
                  "why": "Correct. It names a choice Chopin makes (the spring imagery) AND what that choice is doing (turning grief toward renewal). A claim about the choice and its purpose is the analytical claim."},
                 {"id": "C", "text": "Chopin wrote a moving and genuinely surprising story, and by the final line a great many readers find that they are still thinking hard about it long after reaching the very last page.",
                  "correct": False,
                  "why": "This is an opinion about the story as a whole. It names no specific choice and no effect of a choice, so it is a judgment, not analysis of the craft."},
                 {"id": "D", "text": "Chopin uses imagery, irony, and symbolism at several points across the story.",
                  "correct": False,
                  "why": "This lists techniques in general but points to no one specific choice and says what none of them is doing. Naming devices is not the same as claiming a choice and its purpose."},
             ]),
        # SECOND minimal pair, DIFFERENT confounds than the first (which was summary vs opinion): here the two
        # traps are (B) naming a real craft choice but only REPORTING it, no purpose, and (C) a bare thematic
        # interpretation that names NO specific choice. Fresh sentences (the ironic turn from grief to freedom,
        # the heart-trouble opening, a theme statement), not the window/spring imagery used elsewhere. The
        # correct choice stays WITHIN the provided excerpt (which ends at "Free! Body and soul free!"), so a
        # solo student can verify it. Correct option (A) is not the lone longest; the theme distractor (C) is
        # the longest.
        Slot("MODEL", "discrimination", "Which one claims a choice AND its purpose?",
             ref="", labeled_grade_c=True, bank="story_of_an_hour",
             body=("Same skill, a new set. The task is still to ANALYZE the story, and all three sentences name "
                   "Chopin. Only one is an analytical claim, a claim that names a choice AND its purpose. Which one? "
                   "(A) Chopin has the newly widowed Mrs. Mallard feel a rising sense of freedom rather than "
                   "only grief, turning the moment we expect to be pure mourning into release and making us feel "
                   "how confining her marriage had been.  "
                   "(B) Chopin opens the story by telling us in its very first line that Mrs. Mallard has heart "
                   "trouble.  "
                   "(C) Chopin suggests that a person can feel quietly trapped inside a marriage even when nothing "
                   "looks wrong from the outside, and that a first taste of freedom can be so overwhelming it is "
                   "impossible to hold on to for very long.  "
                   "(D) Chopin has Mrs. Mallard weep in her sister's arms, then go alone to her room and slowly "
                   "begin to whisper the word free. "
                   "Correct: A is the analytical claim. (A) names a choice (the ironic turn from expected grief to "
                   "a rising sense of freedom) AND what it does (making the reader feel how confining the marriage "
                   "had been). (B) names a choice but only reports it, never saying what it accomplishes. (C) "
                   "states the story's overall meaning but points to no specific choice, so it is a claim about "
                   "theme, not craft. (D) retells what happens, step by step, so it is summary, not analysis."),
             choices=[
                 {"id": "A", "text": "Chopin has the newly widowed Mrs. Mallard feel a rising sense of freedom rather than only grief, turning the moment we expect to be pure mourning into release and making us feel how confining her marriage had been.",
                  "correct": True,
                  "why": "Correct. It names a choice Chopin makes (the ironic turn from expected grief to a rising sense of freedom) and says what that choice does (making the reader feel how confining the marriage had been), so it is a claim about the craft."},
                 {"id": "B", "text": "Chopin opens the story by telling us in its very first line that Mrs. Mallard has heart trouble.",
                  "correct": False,
                  "why": "This names a real choice, opening on her heart trouble, but only reports that she does it; without saying what the choice accomplishes, it is not yet an analytical claim."},
                 {"id": "C", "text": "Chopin suggests that a person can feel quietly trapped inside a marriage even when nothing looks wrong from the outside, and that a first taste of freedom can be so overwhelming it is impossible to hold on to for very long.",
                  "correct": False,
                  "why": "This interprets the story's overall meaning but points to no specific choice the author makes, so it is a claim about theme rather than about the craft."},
                 {"id": "D", "text": "Chopin has Mrs. Mallard weep in her sister's arms, then go alone to her room and slowly begin to whisper the word free.",
                  "correct": False,
                  "why": "This retells what happens, step by step. It is accurate summary, but it names no choice and no purpose, so it is not an analytical claim."},
             ]),
        Slot("MODEL", "predict_the_fix", "What turns this summary into analysis?",
             bank="story_of_an_hour",
             body=("Diagnose this draft before the reveal. The task is to ANALYZE the story. A student wrote: "
                   "'Chopin describes the trees, the sky, and the rain that Mrs. Mallard sees through the "
                   "window.' Which single move would most improve it as an analytical claim? "
                   "(A) claim what Chopin is DOING with that imagery and to what end, the choice and its purpose, "
                   "instead of only reporting that she describes it  "
                   "(B) list two or three more things Mrs. Mallard sees through the open window, such as the "
                   "clouds and the twittering sparrows, so the sentence feels fuller and more complete  "
                   "(C) add what happens next in the plot, such as how Mrs. Mallard reacts and what she does "
                   "once she finally turns away from the open window and its view  "
                   "(D) make the sentence longer by piling on more adjectives and extra clauses so that it "
                   "reads as more detailed, more developed, and more impressive to a reader"),
             feedback=("Correct: A. The draft names what the text describes, which is summary. The fix claims the "
                       "author's choice and its purpose: 'Chopin uses that spring imagery to tilt a scene of "
                       "grief toward renewal.' Listing more details (B), adding plot (C), or adding length (D) "
                       "all stay in summary; none of them say what the author is doing.")),

        # ===== SUPPORTED: framed write (fill-in frame) on the taught source (already read at STEP 2) =====
        Slot("SUPPORTED", "production_frq", "Write a claim about the craft",
             ref="", bank="story_of_an_hour", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on the move: name a choice Chopin makes, then name "
                       "what it is doing. Pick one of these choices to write about: the open-window imagery, the "
                       "irony of Mrs. Mallard's reaction, or the repetition of the word free.",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "Chopin uses ______ [the choice from the story] to ______ [its effect or purpose]."),
                 closer="Claim what Chopin is DOING and to what end, not what happens. Do not retell the plot. "
                        "Write one sentence, then run the craft check before you submit.")),
        # DIAGNOSIS = check-and-fix on a PROVIDED weak draft (not a fresh production, so it does not repeat the
        # supported write). Stays on the taught source = no new reading (load). Uses checklist() so the check
        # renders as one clean numbered list (no 'Step N' double-numbering).
        Slot("MODEL", "diagnosis_frq", "Check your claim: about the craft, or about the plot?",
             ref="", bank="story_of_an_hour", scored=True,
             body=frq_prompt(
                 intro="Run the craft check on this weak draft, then rewrite it into a sentence that claims what "
                       "Chopin is doing, not just what happens.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "Chopin repeats the word free three times near the end of the story.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("What choice does it name?", "The repetition of the word free. Good, a real craft choice is named."),
                     ("Does it say what that choice is DOING, or only that it happens?", "Only that it happens. Add the effect: what the repetition does to the meaning or the reader."),
                     ("Is it about the craft, not just the plot?", "It points at a choice but stops at reporting it. Name the purpose to make it analytical."),
                 ]),
                 closer="Now rewrite the weak draft into one sentence that names the choice AND what it is doing. "
                        "Then name which question your rewrite fixed.")),

        # ===== INDEPENDENT: cold write, no frame, a DIFFERENT choice + autonomy + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write an analytical claim on your own",
             ref="", bank="story_of_an_hour", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="On your own now, no frame. Write ONE analytical claim about a DIFFERENT choice Chopin "
                       "makes than the one you used above, so you cannot reuse that sentence.",
                 closer="Name the choice and claim its effect or purpose. Do not retell the plot. Claiming what "
                        "the author is doing is what every real analysis is built on, and you are ready to do it "
                        "cold. Run the craft check before you submit: is it about the craft rather than the plot, "
                        "and does it name a choice AND an effect?")),

        # ===== TRANSFER: same move, a NEW source (highways), bank-partitioned from the taught source =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: Building the Interstate Highway System",
             ref="ACC-W910-INFO-LESSON-HIGHWAYS", bank="interstate_highways",
             body=("Read this new source, an explanatory article on the Interstate Highway System. It is not a "
                   "story, so the author's choices are about STRUCTURE and wording: how it opens, the order of "
                   "the sections, the questions used to organize it. Read it once for what it says, then find "
                   "one such choice you could make a claim about. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Write an analytical claim on a NEW text",
             ref="", bank="interstate_highways", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="New text, different genre, same move. Write ONE analytical claim about a STRUCTURAL or "
                       "wording choice the highways author makes: name the choice and claim its effect or purpose.",
                 closer="For example, you might claim what the author is doing by opening with something readers "
                        "pass 'without ever thinking about it', or by organizing the article around questions "
                        "like who paid for it and what it does. Same claim-about-the-craft move as the Chopin "
                        "claim, new text. Do not summarize the content. Run the craft check before you submit.")),
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
