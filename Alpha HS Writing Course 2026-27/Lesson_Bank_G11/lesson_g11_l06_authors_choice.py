"""
lesson_g11_l06_authors_choice.py  -  G11 KC C.11.03, ARCHETYPE T4: TEXT-DEPENDENT ANALYSIS (DEW, ceiling paragraph). V3.1.

V3.1 rebuild of the G11 rhetorical-analysis intro (Unit 2) to the v3.1 spec, adapting the pattern proven on the
G9 L06/L08 v3.1 lessons. PRESERVED EXACTLY: teaching point (do rhetorical analysis - name a CHOICE the author
makes and explain its effect on the AUDIENCE, not the content/subject of the text), id
ACC-W1112-L-G11-C1103-0006, lesson_type=4, kc=C.11.03, mnemonic_status=proposal, unit, and the bound verbatim
public-domain stimuli (Douglass 1852 taught -> FDR First Inaugural 1933 transfer). Changes vs the prior L06:
  1. ONE IDEA, hammered (KH load): a teal ONE_IDEA callout states the single core idea (analyze the CHOICE and
     its audience effect, not the content), then the minimum teaching as a real LIST (content analysis vs
     rhetorical analysis) instead of the old wall-of-prose teach body that tripped format_fidelity.
  2. COPING-MODEL THINK-ALOUD (SRSD): the model is rewritten as a writer drafting, running a check, catching the
     problem, and revising (First try -> Second try -> Final), with a literal BEFORE and AFTER (content_depth).
     No named person (Timeback stateless rule). The reusable check tool is attached at point of first use.
  3. FIXED THE SURFACE-TOKEN CONFOUND (DI, faultless communication): every discrimination option is attributed
     to Douglass AND names the audience/listeners, so mentioning the audience no longer co-varies with the
     correct answer; naming a CHOICE plus its effect is the only invariant. Correct option is not the lone
     longest. Removed the leaked 'Grade-C design bet' label from the student text (kept labeled_grade_c=True).
  4. DETERMINISTIC FRQ/DIAGNOSIS BODIES: supported + diagnosis + independent + transfer prompts are built with
     frq_prompt/setapart/checklist (no hand-written 'Step 1/2' prose that double-numbers), and carry NO
     'Scored on ...' rubric chrome.
  5. AUTONOMY + SAY-THE-STANDARD (Yeager): the independent write drops the frame, lets the student choose which
     choice to analyze, and names the standard out loud ('naming a choice and its effect on the audience is
     what every real rhetorical analysis is built on; you are ready to do it cold').

ONE IDEA: rhetorical analysis names a CHOICE the author makes and its effect on the AUDIENCE, not the content.
ONE REMINDER: the choice-and-effect check. Passes all 23 lesson_contract gates. Own words, PD-sourced, no em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Rhetorical analysis is when you name a <strong>CHOICE '
'the author makes</strong> and explain how that choice works on the <strong>AUDIENCE</strong>, not just what '
'the author argues. A sentence can be true about the text and still only report the content.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the choice-and-effect test</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you commit to any analysis sentence, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">What CHOICE does the author make (a question, a contrast, a repeated word, a shift in tone)?</li>'
'<li style="margin:2px 0">Does my sentence NAME that choice, or does it just report what the author argues?</li>'
'<li style="margin:2px 0">What is the effect on the AUDIENCE, the specific listeners or readers?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If the sentence answers only what the author argues, '
'it is content analysis. Name the choice and its audience effect instead.</div></div>')

# coping-model think-aloud: a writer DRAFTS a rhetorical-analysis sentence, runs the check, catches the problem,
# and REVISES (First try -> Second try -> Final), then the BEFORE/AFTER endpoints (content_depth needs both words).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer drafting one analysis sentence about how Douglass opens his address, testing each try:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Douglass argues that the Fourth of July belongs to '
    'free citizens, not to the enslaved." Run the check: does it NAME a choice he makes? No. It reports what he '
    'argues. That is content. Look again at HOW he opens.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "Douglass opens with a string of questions." Does it '
    'name a choice? Yes, the opening questions. Does it give the effect on the AUDIENCE? No, it stops at naming '
    'the choice. Add what the questions do to his listeners.</p>'
    '<p style="margin:0"><strong>Final:</strong> "Douglass opens with a string of questions ("why am I called '
    'upon to speak here?") to force his celebrating audience to feel the distance between them and him before he '
    'names it, so they cannot dismiss his point as abstract." Choice named, audience effect named. That is '
    'rhetorical analysis.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "Douglass argues that the Fourth of July belongs to free '
    'citizens, not to the enslaved." (reports the content, names no choice)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "Douglass opens with a string of questions to force his '
    'celebrating audience to feel the distance between them and him, so they cannot dismiss his point as '
    'abstract." (names a choice and its effect on the audience)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1103-0006", grade="9-10", lesson_type=4,
    unit="G11 U2 - Rhetorical analysis (author's choice vs content)",
    title="Analyze the Choice and Its Effect on the Audience",
    target=("Do rhetorical analysis: name a rhetorical choice the author makes and explain why it works on the "
            "AUDIENCE, rather than analyzing the content or subject of the text. Written at the sentence. "
            "Trait: Evidence and Commentary."),
    acc_tags=["ACC.W.INFO.6", "CCSS.W.11-12.9", "CCSS.RI.11-12.6"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.03",
                "sot": "icm course-G11.md L06; v3.1 spec icm/_config/v3_1-lesson-build-spec.md",
                "taught_stimulus": "ACC-W910-ANALYSIS-LESSON-DOUGLASS",
                "transfer_stimulus": "ACC-W910-RA-SINGLE-0001",
                "one_idea": "Rhetorical analysis names a CHOICE the author makes and its effect on the AUDIENCE, not the content.",
                "one_reminder": "choice-and-effect test: what choice? does my sentence name it or just report content? what is the audience effect?",
                "playbook": "_phase2/playbook_T4_DEW.md",
                "template": "locked L01 template; ANALYSIS-TIER binds full verbatim PD sources.",
                "version_note": ("V3.1: rebuilt to the v3.1 spec on the G9 L06/L08 v3.1 pattern - ONE_IDEA "
                                 "callout + list teach (fixed the wall-of-text), coping-model draft/check/revise "
                                 "think-aloud with literal BEFORE/AFTER (SRSD), choice-and-effect check tool at "
                                 "point of first use, fixed the surface-token confound in the discrimination "
                                 "(every option names the audience so it does not co-vary) + removed the leaked "
                                 "'Grade-C' label (DI faultless communication), deterministic "
                                 "frq_prompt/setapart/checklist bodies (no 'Step N' double-number, no 'Scored on' "
                                 "chrome), autonomy + say-the-standard on the independent write (Yeager). "
                                 "Preserved teaching point, id, type, KC, unit, and the bound Douglass/FDR PD "
                                 "stimuli."),
                "council": ("T4 G11 rhetorical-analysis intro: author's-choice-vs-content (why the choice + "
                            "effect on audience, not the subject). Discrimination is a labeled design bet in "
                            "code only. DEW=proposal."),
                "review_provenance": ("23 lesson_contract gates (exit 0) + gated_reading render-QC clean; "
                                      "adapts the adjudicated L01/L06 v3.1 Council+Fable findings.")},
    fade_ledger_moves=["authors-choice-vs-content", "effect-on-the-audience"],
    slots=[
        # ===== TEACH: ONE idea only (list, not a wall of prose; check tool held for point of first use) =====
        Slot("TEACH", "teach_card", "Analyze the choice, not the topic",
             body=(ONE_IDEA +
                   "Ordinary analysis reports what a text says. Rhetorical analysis asks a sharper question: "
                   "WHY did the author make a particular choice, and how does it work on the people receiving "
                   "it? Keep two kinds of sentence apart:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Content analysis</strong>: it reports WHAT the author "
                   "argues. 'Douglass argues that the holiday is not his.' True, but it is about the subject.</li>"
                   "<li style=\"margin:4px 0\"><strong>Rhetorical analysis</strong>: it names a deliberate "
                   "CHOICE (a question, a contrast, a repeated word, a shift in tone) and explains its effect "
                   "on the specific audience. 'Douglass opens with questions to make a celebrating crowd feel "
                   "the distance he names.'</li></ul>"
                   "The audience is the hinge: a choice works because of who is receiving it. The trap is "
                   "analyzing the subject instead of the crafting. Today: name a choice and explain its effect "
                   "on the audience, not what the author argues.")),
        Slot("TEACH", "stimulus_display", "Read the source: Frederick Douglass, 1852 address (excerpt)",
             ref="ACC-W910-ANALYSIS-LESSON-DOUGLASS", bank="douglass_1852",
             body=("Read this excerpt from Frederick Douglass's 1852 Fourth of July address, delivered to a "
                   "celebrating audience. Because your job is rhetorical analysis, read it once for what he "
                   "argues, then again for one CHOICE he makes (a question, a repeated word, a shift in tone, a "
                   "contrast) and how it works on that audience. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model draft/check/revise think-aloud + the check tool =====
        Slot("MODEL", "annotated_before_after", "Watch content analysis become rhetorical analysis",
             bank="douglass_1852",
             body=("Here is the skill in action. Follow the writer's thinking below as one draft after another "
                   "gets tested and fixed until the sentence names a choice and its audience effect. "
                   + COPING_HTML +
                   " Notice the two moves that turned the BEFORE into the AFTER: the writer NAMED a choice "
                   "Douglass makes, then explained its effect on the AUDIENCE. " + REMEMBER +
                   "When you write your own, do the same: name the choice first, then the audience effect, and "
                   "run the check before you commit to it.")),
        Slot("MODEL", "discrimination", "Which is rhetorical analysis, not content analysis?",
             ref="", labeled_grade_c=True, bank="douglass_1852",
             body=("Now that you have seen one built, spot the target. Every sentence below is true about "
                   "Douglass and every one mentions his audience. Which one does RHETORICAL analysis, naming a "
                   "CHOICE he makes and its effect on that audience, rather than reporting his content? "
                   "(A) Douglass tells his listeners that the blessings of the Fourth of July are shared by them and not by the enslaved people whom he speaks for.  "
                   "(B) Douglass piles up sharp questions at the very opening to make his listeners feel the distance between them and him before he states it.  "
                   "(C) Douglass points out to the crowd that the great principles of freedom named in the Declaration were never truly extended to enslaved Americans.  "
                   "(D) Douglass's decision to open with sharp questions is a powerful and effective technique that surely made a strong impression on everyone in his audience. "
                   "Correct: B. It names a CHOICE (the opening questions) and its effect on the audience "
                   "(feeling the distance before he states it). (A) and (C) address the audience but only report "
                   "what Douglass argues, so they stay on content, and (D) names the choice but only praises it "
                   "instead of naming what it does to the audience."),
             choices=[
                 {"id": "A", "text": "Douglass tells his listeners that the blessings of the Fourth of July are shared by them and not by the enslaved people whom he speaks for.",
                  "correct": False,
                  "why": "This is true and it names the listeners, but it only reports what Douglass argues (the content). It names no choice he makes and no effect that choice has on them."},
                 {"id": "B", "text": "Douglass piles up sharp questions at the very opening to make his listeners feel the distance between them and him before he states it.",
                  "correct": True,
                  "why": "Correct. It names a CHOICE (piling up questions at the opening) and its effect on the AUDIENCE (making them feel the distance before he states it). Naming the choice and its effect is the move."},
                 {"id": "C", "text": "Douglass points out to the crowd that the great principles of freedom named in the Declaration were never truly extended to enslaved Americans.",
                  "correct": False,
                  "why": "This mentions the crowd, but it reports what Douglass argues about the Declaration (his content). It never names a choice he makes or its effect on those listeners."},
                 {"id": "D", "text": "Douglass's decision to open with sharp questions is a powerful and effective technique that surely made a strong impression on everyone in his audience.",
                  "correct": False,
                  "why": "This names a choice (the opening questions), but it only praises it as 'powerful' and 'effective' and never says what specific effect it has on the audience. Judging a choice is not the same as analyzing how it works on the listeners."},
             ]),
        # SECOND minimal pair, DIFFERENT confound: here every option stays on the crafting (no content trap).
        # The two wrong options each do only HALF the move (name the choice with no effect / assert an effect
        # with no choice); only the correct one supplies BOTH. Fresh sentences on the closing storm passage.
        Slot("MODEL", "discrimination", "Which sentence does the WHOLE move, not half of it?",
             ref="", labeled_grade_c=True, bank="douglass_1852",
             body=("Naming a choice is only half the move. Each sentence below is about how Douglass crafts his "
                   "closing storm imagery, not its content. Which one does the full move, naming his CHOICE and "
                   "its effect on the audience, not just one half? "
                   "(A) Douglass escalates his images from a gentle shower to thunder, a storm, a whirlwind, and an earthquake as the passage builds.  "
                   "(B) Douglass leaves his comfortable holiday audience feeling shaken and unsettled, no longer able to enjoy their celebration as calmly as they did when the speech began.  "
                   "(C) Douglass escalates from a gentle shower to thunder and an earthquake to jolt his celebrating audience into feeling the violent scale of change he demands.  "
                   "(D) Douglass escalates from a gentle shower to thunder and an earthquake to show how furious he himself has become by the close of his address. "
                   "Correct: C. It names a CHOICE (escalating the weather images) and its effect on the audience "
                   "(jolting them into feeling the scale of change). (A) names the choice but stops before any "
                   "audience effect, (B) asserts an effect but names no choice, and (D) names the choice but "
                   "points its effect at Douglass himself rather than the audience, so none of the three does "
                   "the whole move."),
             choices=[
                 {"id": "A", "text": "Douglass escalates his images from a gentle shower to thunder, a storm, a whirlwind, and an earthquake as the passage builds.",
                  "correct": False,
                  "why": "This names a real choice, the escalating storm images, but it stops there and never says what that escalation does to his listeners, so it delivers only half the move."},
                 {"id": "B", "text": "Douglass leaves his comfortable holiday audience feeling shaken and unsettled, no longer able to enjoy their celebration as calmly as they did when the speech began.",
                  "correct": False,
                  "why": "This describes a feeling in the audience but points to no specific choice Douglass makes, so a reader cannot tell what crafting produced the effect."},
                 {"id": "C", "text": "Douglass escalates from a gentle shower to thunder and an earthquake to jolt his celebrating audience into feeling the violent scale of change he demands.",
                  "correct": True,
                  "why": "Correct. It names the CHOICE (escalating from a gentle shower to thunder and an earthquake) and its effect on the AUDIENCE (jolting them into feeling the scale of change he demands), which is the whole move."},
                 {"id": "D", "text": "Douglass escalates from a gentle shower to thunder and an earthquake to show how furious he himself has become by the close of his address.",
                  "correct": False,
                  "why": "This names the choice and an effect, but the effect lands on Douglass's own feelings, not on the audience. Rhetorical analysis has to say what the choice does to the listeners, not what it reveals about the speaker."},
             ]),
        Slot("MODEL", "predict_the_fix", "What turns this into rhetorical analysis?",
             bank="douglass_1852",
             body=("Diagnose this draft before the reveal. A student wrote: 'Douglass explains that the promises "
                   "of the Declaration were never extended to enslaved people.' Which single move would most "
                   "improve it as rhetorical analysis? "
                   "(A) name a rhetorical CHOICE Douglass makes and explain its effect on his listeners, rather than only reporting what he explains  "
                   "(B) add a second idea that Douglass argues, such as the claim that this celebrated holiday belongs to the free citizens in his audience and not to him  "
                   "(C) summarize the whole speech from its opening to its close so the sentence captures everything Douglass says  "
                   "(D) say that the speech is powerful and moving because Douglass clearly cares a great deal about his subject"),
             feedback=("Correct: A. The draft reports content (what he explains). Rhetorical analysis names a "
                       "choice, for example his invoking the Declaration his audience reveres, and its effect "
                       "on those listeners (turning their own founding document into the measure of their "
                       "failure). Another argued idea (B), a summary (C), or a vague 'powerful' (D) all stay on "
                       "content.")),

        # ===== SUPPORTED: framed write (fill-in frame) on the taught source (already read at the TEACH step) =====
        Slot("SUPPORTED", "production_frq", "Analyze a choice and its audience effect",
             ref="", bank="douglass_1852", rubric_ref="rc.ap", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on the move: name a choice Douglass makes and "
                       "explain its effect on his celebrating audience.",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "Douglass ______ [a rhetorical choice he makes] to ______ [its effect on his specific audience]."),
                 closer="Name the choice and its audience effect. Do not report the content of what he argues. "
                        "Write one sentence, then run the choice-and-effect check before you submit.")),
        # DIAGNOSIS = check-and-fix on a PROVIDED weak draft (not a fresh production, so it does not repeat the
        # supported write). Stays on the taught source = no new reading (load). Uses checklist() so the check
        # renders as one clean numbered list (no 'Step N' double-numbering).
        Slot("MODEL", "diagnosis_frq", "Check your analysis: the choice, or the content?",
             ref="", bank="douglass_1852", scored=True,
             body=frq_prompt(
                 intro="Run the choice-and-effect check on this weak draft, then rewrite it into a sentence "
                       "that analyzes a choice Douglass makes and its effect on his audience.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "Douglass points out that slavery goes against the nation's stated ideals.", "red"),
                 checklist_block=checklist(title="Run the test:", rows=[
                     ("Does it name a CHOICE Douglass makes?", "No. It reports his content. Name a choice, such as his string of questions or his sharp contrast."),
                     ("Is there an effect on the AUDIENCE?", "No. Add what that choice does to his celebrating listeners."),
                     ("Does it stay on the choice, not the subject?", "Not yet. Keep the focus on the crafting, not on slavery as a topic."),
                 ]),
                 closer="Now rewrite the weak draft into one rhetorical-analysis sentence, choice plus audience "
                        "effect. Then name which question your rewrite fixed.")),

        # ===== INDEPENDENT: cold write, no frame, student picks the choice + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Write a rhetorical-analysis sentence on your own",
             ref="", bank="douglass_1852", rubric_ref="rc.ap", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="On your own now, no frame. Pick any one choice Douglass makes in the excerpt.",
                 closer="Write ONE rhetorical-analysis sentence: name the choice and explain its effect on his "
                        "audience. You decide which choice to analyze, a question, a contrast, a repeated word, "
                        "or a shift in tone. Naming a choice and its effect on the audience is what every real "
                        "rhetorical analysis is built on, and you are ready to do it cold. Run the "
                        "choice-and-effect check before you submit.")),

        # ===== TRANSFER: same move, a NEW source (FDR 1933), bank-partitioned from the taught source =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: a president's inaugural address",
             ref="ACC-W910-RA-SINGLE-0001", bank="ra_speech_1",
             body=("Read this new excerpt, delivered by a new president to an anxious national audience during "
                   "a severe economic crisis. Because your job is rhetorical analysis, read it once for what "
                   "the speaker argues, then again for one CHOICE he makes and its effect on that audience. The "
                   "text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Write a rhetorical-analysis sentence on a NEW text",
             ref="", bank="ra_speech_1", rubric_ref="rc.ap", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="New text, same move as the Douglass sentence. Analyze one choice the speaker makes.",
                 closer="Write ONE rhetorical-analysis sentence about a choice the speaker makes: name the "
                        "choice and explain its effect on his audience. Do not report the content of what he "
                        "argues. Run the choice-and-effect check before you submit.")),
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
