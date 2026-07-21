"""
lesson_g9_l21_intro_conclusion_v3_1.py  -  G9 KC C.9.04, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD, ceiling essay). V3.1.

Rebuild of lesson_g9_l21_intro_conclusion.py to the v3.1 build spec. Teaching point KEPT: write an
INTRODUCTION that orients the reader and states the thesis, and a CONCLUSION that lands the upshot (why it
matters), not a restatement. KC C.9.04. Bound stimuli KEPT: SCHOOLLUNCH (taught) -> PHOTOSYNTHESIS (transfer,
partitioned). id / lesson_type=7 / mnemonic_status="proposal" / every production_frq unit="multi_paragraph"
are COPIED EXACT from the current L21.

V3.1 changes over the current L21:
  1. TEACH split into a ONE_IDEA callout + a real <ul> list of the two jobs (fixes the 140-word wall of text
     format_fidelity flagged); "thesis" defined in-body with an "is a" cue (define-before-use).
  2. MODEL BEFORE THE QUIZ (KH): the coping-model before/after worked example + the reusable check tool now
     PRECEDE the discrimination (worked example before the quiz), which moves into the MODEL role.
  3. COPING-MODEL THINK-ALOUD (SRSD): the model is a draft -> check -> revise process for both the intro and
     the conclusion; still contains literal BEFORE and AFTER (content_depth). No named near-peer.
  4. Discrimination uses explicit choices=[{id,text,correct,why}] with the correct option NOT the lone longest,
     and NO leaked internal label (fixes the current "Grade-C design bet" leak).
  5. Deterministic FRQ/diagnosis prompts (frq_prompt/setapart/checklist), no "Scored on ..." chrome; autonomy +
     say-the-standard on the independent write (Yeager).

Passes all 23 lesson_contract gates. Own words, no fabricated figures, no em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist, outline_table

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">An <strong>introduction</strong> frames the '
'<strong>thesis</strong> (orient the reader, then state it); a <strong>conclusion</strong> lands the '
'<strong>upshot</strong> (why it matters), not a restatement.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 2 jobs</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, check the opening and the ending each do their job:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0"><strong>Intro</strong>: does it orient the reader and state the thesis, not just announce the topic?</li>'
'<li style="margin:2px 0"><strong>Conclusion</strong>: does it land an upshot (why the argument matters or what follows), instead of repeating?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If either just announces or repeats, it is not doing real work yet.</div></div>')

# coping-model think-aloud panel: a WRITTEN drafting process (draft -> check -> revise) for both the intro and
# the conclusion, then the literal endpoints (content_depth needs BOTH a BEFORE and an AFTER).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer building the opening and the ending, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>Intro, first try:</strong> "This essay is about free school meals, and I '
    'will give some reasons." Check it: does it frame a thesis? No, it only announces the topic. Rewrite it.</p>'
    '<p style="margin:0 0 8px"><strong>Intro, better:</strong> "For a student who comes to school hungry, lunch '
    'decides whether the afternoon is a class or a countdown to the next meal. Because hunger and focus cannot '
    'share one desk, schools should offer free meals to every student." Now it orients the reader and states the '
    'thesis.</p>'
    '<p style="margin:0 0 8px"><strong>Conclusion, first try:</strong> "In conclusion, free meals are a good idea, '
    'like I said." Check it: does it land an upshot? No, it just repeats. Add why it matters.</p>'
    '<p style="margin:0"><strong>Conclusion, better:</strong> "A school that feeds every student removes one real '
    'barrier between a child and a fair chance to learn." Now it says why the argument matters.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> an intro that announces the topic and a conclusion that just '
    'repeats the claim</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> an intro that frames the thesis and a conclusion that lands the '
    'upshot</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C904-0021", grade="9-10", lesson_type=7,
    unit="G9 U5 - Build essay (introductions and conclusions)",
    title="Frame the Thesis, Land the Upshot",
    target=("Write an introduction that orients the reader and states the thesis, and a conclusion that lands "
            "the upshot (why it matters) instead of just repeating the claim. Written across an essay. Trait: "
            "Organization."),
    acc_tags=["ACC.W.INFO.5", "CCSS.W.9-10.2a"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-14",
                "mnemonic_status": "proposal", "kc": "C.9.04", "sot": "icm course-G9.md L21",
                "taught_stimulus": "ACC-W910-ARG-LESSON-SCHOOLLUNCH",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-PHOTOSYNTHESIS",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": "v3.1 build spec (L01 pattern); ESSAY-TIER binds full sources.",
                "one_idea": "An introduction frames the thesis; a conclusion lands the upshot, not a restatement.",
                "one_reminder": "Check the 2 jobs: intro orients + states thesis? conclusion lands an upshot?",
                "version_note": ("V3.1 rebuild of lesson_g9_l21_intro_conclusion.py. Kept teaching point + all "
                                 "Lesson() field values + bound stimuli. Applied the v3.1 spine: TEACH split into "
                                 "a ONE_IDEA callout + a real list (fixed the wall-of-text format_fidelity fail), "
                                 "model+check-tool now precede the discrimination (KH), coping-model think-aloud "
                                 "(SRSD) for both intro and conclusion, explicit-choices discrimination with the "
                                 "leaked 'Grade-C design bet' label removed, deterministic FRQ/diagnosis prompts "
                                 "with no 'Scored on' chrome, autonomy + say-the-standard on the independent write."),
                "review_provenance": "built to the L01 v3.1 pattern; 23 lesson_contract gates + gated_reading render-QC",
                "council": ("T7/BUILD framing rung: introduces B4 introductions and conclusions (intro frames the "
                            "thesis; conclusion lands the upshot, not a restatement). lands-vs-repeats "
                            "discrimination labeled Grade-C in code (not in student text). BUILD=proposal; "
                            "unit=multi_paragraph.")},
    fade_ledger_moves=["intro-frames-the-thesis", "conclusion-lands-the-upshot"],
    slots=[
        # ===== TEACH: ONE idea + the two jobs as a real list (no wall of text); thesis defined with a cue =====
        Slot("TEACH", "teach_card", "Openings orient, endings land the upshot",
             body=(ONE_IDEA +
                   "An essay's first and last paragraphs are not filler; each has a job:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>INTRODUCTION</strong>: it orients the reader and states the "
                   "thesis. The thesis is a single sentence that states the position (or, on an explain task, the "
                   "focusing idea) your whole essay defends. A stalling intro just announces 'this essay is about "
                   "X, I will talk about it,' which frames nothing.</li>"
                   "<li style=\"margin:4px 0\"><strong>CONCLUSION</strong>: it lands the upshot. It says why the "
                   "argument matters or what follows from it, instead of repeating the thesis in new words. 'In "
                   "conclusion, free meals are good, like I said' does no work; 'feeding every student is a "
                   "condition for learning, not charity' lands.</li></ul>"
                   "The trap is a stalling intro and a repeating conclusion, the two weakest habits in student "
                   "essays. Today: write an intro that frames the thesis and a conclusion that lands the upshot.")),
        Slot("TEACH", "stimulus_display", "Read the source: free school meals",
             ref="ACC-W910-ARG-LESSON-SCHOOLLUNCH", bank="school_lunch",
             body=("Read this source about free school meals. Because your job is to FRAME an essay, read the "
                   "whole thing and think about why this issue matters (for the intro) and what follows from the "
                   "argument (for the conclusion). The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + the reusable check tool =====
        Slot("MODEL", "annotated_before_after", "Watch a stalling frame become a working one",
             bank="school_lunch",
             body=("Here is the skill in action. Follow the writer draft the opening and the ending, catch the "
                   "problem, and fix it. " + COPING_HTML +
                   " The BEFORE announces and repeats; the AFTER orients the reader to the thesis and ends on why "
                   "it matters. Framing the thesis and landing the upshot are the two moves. " + REMEMBER +
                   "When you write your own, run this 2-job check before you submit.")),
        Slot("MODEL", "discrimination", "Which conclusion lands the upshot?",
             ref="", labeled_grade_c=True, bank="school_lunch",
             body=("Now that you have seen one built, spot the target first. The thesis was: schools should offer "
                   "free meals to all students. Which conclusion LANDS the upshot instead of just repeating the "
                   "thesis? "
                   "(A) In conclusion, as I explained, schools should offer free meals to all students, because "
                   "the reasons I already gave clearly show that free meals really do help students in many ways.  "
                   "(B) Feeding every student is not charity: a school that removes hunger removes one real "
                   "barrier between a child and a fair chance to learn.  "
                   "(C) In conclusion, plenty of students eat lunch at school each day, so free meals are a good "
                   "idea that helps them succeed.  "
                   "(D) In conclusion, free meals help students, and schools should also add later start times, "
                   "because more sleep would help students focus even more. "
                   "Correct: B. It says why the argument matters and what follows, while (A) restates, (C) only "
                   "adds a fact, and (D) opens a brand-new argument."),
             choices=[
                 {"id": "A", "text": "In conclusion, as I explained, schools should offer free meals to all students, because the reasons I already gave clearly show that free meals really do help students in many ways.",
                  "correct": False,
                  "why": "This just restates the thesis (offer free meals because they help students) and adds nothing, so the reader gains nothing new. A restatement is not an upshot."},
                 {"id": "B", "text": "Feeding every student is not charity: a school that removes hunger removes one real barrier between a child and a fair chance to learn.",
                  "correct": True,
                  "why": "Correct. It says why the argument matters and what follows from it (removing hunger removes a barrier to a fair chance), which is exactly what landing the upshot means."},
                 {"id": "C", "text": "In conclusion, plenty of students eat lunch at school each day, so free meals are a good idea that helps them succeed.",
                  "correct": False,
                  "why": "This ends on an extra fact and a vague 'good idea,' not an upshot. A conclusion lands when it says why the argument matters, not when it adds one more detail."},
                 {"id": "D", "text": "In conclusion, free meals help students, and schools should also add later start times, because more sleep would help students focus even more.",
                  "correct": False,
                  "why": "This opens a brand-new argument (later start times) the essay never made. A conclusion lands the point you already argued; raising a fresh claim leaves the reader with an idea that was never supported."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this conclusion most need?",
             bank="school_lunch",
             body=("Diagnose before the reveal. An essay ends: 'In conclusion, free school meals help students, "
                   "so schools should offer them. That is what I argued.' Which single change would most improve "
                   "the conclusion? "
                   "(A) replace the restatement with an upshot, why the argument matters or what follows from it  "
                   "(B) add one more fact about school meals, like how many students eat lunch at school each day  "
                   "(C) make it two sentences longer by restating the main reasons from the body paragraphs  "
                   "(D) start it with 'To sum up' instead of 'In conclusion' so it sounds more formal and polished"),
             feedback=("Correct: A. The conclusion just repeats the thesis ('help students, so offer them, that is "
                       "what I argued'), so it does no work. The fix is an upshot: say why it matters (for example, "
                       "that removing hunger removes a barrier to learning) or what follows. Another fact (B), more "
                       "length (C), or a different opener phrase (D) do not turn a restatement into an upshot.")),

        # ===== SUPPORTED: framed write (fill-in frame) on the taught topic =====
        Slot("SUPPORTED", "production_frq", "Write a framing intro", ref="", bank="school_lunch",
             rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on the two moves: orient the reader, then state the thesis.",
                 setapart_block=outline_table(title="Copy this frame, then fill in the blanks:", rows=[
                     ("ORIENT", "______ [one sentence showing why free meals matter for a hungry student]."),
                     ("THESIS", "That is why schools should offer free meals to every student because ______ [your reason]."),
                 ]),
                 closer="Write the INTRODUCTION for an essay arguing that schools should offer free meals to all "
                        "students. Orient the reader in a sentence, then state the thesis. Do not announce 'this "
                        "essay is about ...'; frame the thesis instead.")),
        # DIAGNOSIS (mechanism 4): watch the 2-job check run on a weak draft, then run it on a fresh conclusion.
        Slot("MODEL", "diagnosis_frq", "Check an intro and conclusion for their jobs", ref="", bank="school_lunch",
             scored=True,
             body=frq_prompt(
                 intro="Watch the check run on a weak draft, then run it on a fresh conclusion of your own.",
                 setapart_block=setapart("Weak draft to fix:",
                     "Intro: This essay will discuss free school meals and give reasons. Conclusion: In "
                     "conclusion, free meals are a good idea.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Intro: does it FRAME the thesis (orient, then state it)?",
                      "No, it only announces the topic. Set up why meals matter, then state the thesis."),
                     ("Conclusion: does it LAND an upshot (why it matters or what follows)?",
                      "No, it just repeats. Add why it matters, for example that removing hunger removes a barrier to learning."),
                 ]),
                 closer="Now you: write a fresh CONCLUSION for the free-meals essay, then check it, does it land "
                        "an upshot rather than repeat? Fix it if not, and name the upshot your conclusion delivers.")),

        # ===== INDEPENDENT: cold write (no frame) on the taught topic + autonomy + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write an intro and a conclusion", ref="", bank="school_lunch",
             rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="On your own now, no frame. For an essay arguing that schools should offer free meals to all students:",
                 closer="Write BOTH an INTRODUCTION that frames the thesis (orient the reader, then state it) and "
                        "a CONCLUSION that lands the upshot (why it matters or what follows), not a restatement. "
                        "Framing the thesis and landing the upshot are what every strong essay opens and closes "
                        "with, and you are ready to do it cold. Before you submit, check: does the intro frame "
                        "rather than announce, and does the conclusion land an upshot rather than repeat?")),

        # ===== TRANSFER: same move, a NEW topic (photosynthesis), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: photosynthesis",
             ref="ACC-W910-INFO-LESSON-PHOTOSYNTHESIS", bank="photosynthesis",
             body=("Read this new source about photosynthesis. Because your job is to FRAME an essay, read the "
                   "whole thing and think about why the topic matters (for the intro) and what the reader should "
                   "take away (for the conclusion). This is an explain task, so the thesis sets a focus and takes "
                   "no side. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Write an intro and conclusion on a NEW topic", ref="",
             bank="photosynthesis", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="New topic. For an essay explaining how photosynthesis turns light into food:",
                 closer="Write an INTRODUCTION that frames the thesis, a focusing idea that takes no side (orient "
                        "the reader, then state it), and a CONCLUSION that lands the upshot (why understanding it "
                        "matters), not a restatement. Same framing-and-landing move as the meals essay, new topic. "
                        "Run the 2-job check before you submit.")),
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
