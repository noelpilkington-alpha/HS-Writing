"""
lesson_g11_l29_which_task_type.py  -  G11 KC C.11.05, ARCHETYPE T5: RUBRIC-REVISION (CHECK, paragraph). V3.1.

G11 L29 (Unit 6, review), rebuilt to the v3.1 build spec (icm/_config/v3_1-lesson-build-spec.md), from the
pre-v3.1 lesson_g11_l29_which_task_type.py. Teaching point (KEPT): given a prompt, name whether it is SYNTHESIS
(a source set to combine), SOURCE-FREE (a general question answered from own knowledge), or MULTI-PERSPECTIVE
(set perspectives to weigh), name the moves it rewards, then plan for a fresh prompt rather than defaulting to
one approach. Delivery UNTIMED. KC C.11.05. Bound stimuli KEPT: ACC-W910-SYNTH-SET-0002 (taught, AI-workforce
synthesis) -> ACC-W910-MP-PERSP-0003 (transfer, standardized-testing multi-perspective, bank-partitioned).
rc.ap, unit="paragraph" (T5 ceiling is paragraph, so every scored plan is written at the paragraph). CHECK=proposal.

V3.1 changes over the pre-v3.1 L29 (all prior gate failures fixed):
  1. TEACH is now ONE idea, hammered: a teal ONE_IDEA callout + the three task types as a real <ul> list (was two
     prose teach cards). The name-predict-reveal-plan routine moved to the REMEMBER check tool at the model card
     (point of first use), not cold up front (KH load).
  2. NO leaked internal labels: the old discrimination prose said "a Grade-C design bet we label as a bet"
     (leaked_internal_label). Removed; the discrimination now uses explicit choices=[{id,text,correct,why}] with
     the correct option NOT the lone-longest, and a distractor carries the token "combine" on a non-synthesis
     read so the TELL (source set), not a surface word, is the invariant (DI faultless communication).
  3. PREDICT-THE-FIX reveal lives in feedback= (not in option text; leaked_answer_cue). FRQ + diagnosis bodies
     built with frq_prompt / setapart / checklist (no "Step 1/2" prose, no "Scored on" chrome).
  4. self_score is a clean predict-the-type MCQ (short prompt + choices carrying the reveal), not a wall-of-text
     prose block. "synthesize" defined with an "is when" cue in TEACH (define-before-use). Coping before/after
     kept (literal BEFORE + AFTER inline). Own words, faithful to the bound sources, no fabricated figures, no em
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
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">The wrong task type means the wrong moves, however well '
'you write. So <strong>name the type first</strong> from its tell, then run the moves that type rewards.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: name the type before you plan</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you write a single move, ask these three questions in order:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0"><strong>A source SET?</strong> If several sources are given to combine, it is synthesis: weave one argument and weight each source.</li>'
'<li style="margin:2px 0"><strong>NO passage at all?</strong> If only a general question is given, it is source-free: take a position and anchor it with your own examples.</li>'
'<li style="margin:2px 0"><strong>Printed PERSPECTIVES?</strong> If set views are printed, it is multi-perspective: weigh those views and stake your own in relation.</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">Writers default to whatever they practiced last, so run the check even when the moves feel obvious.</div></div>')

# coping-model before/after panel: a writer defaults to opinion, runs the check, catches the tell, names synthesis.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> jumps in without naming the type</span>'
    '<p style="margin:8px 0 0;font-size:15px">First try: The prompt gives four sources on AI and the workforce, '
    'but I just start giving my personal opinion with examples from my own life, and I never combine the sources '
    'into one argument.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">Second try, running the check: wait, are there several '
    'sources to combine? Yes, four of them. That is the synthesis tell, and I am writing a source-free opinion. '
    'The moves do not match the type.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> names the type, then the moves</span>'
    '<p style="margin:8px 0 0;font-size:15px">Final: '
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">TYPE + MOVES</span> Four sources to combine, so this is synthesis. Moves: build one '
      'argument from the set, weight each source, and cite each one. (Not a source-free opinion.)</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">The revision changes nothing about the writing skill; '
    'it changes the type the writer named, and so the moves. Naming the type from its tell is the fix.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1103-0029", grade="9-10", lesson_type=5,
    unit="G11 U6 - Which task type is this prompt? (3-genre discrimination)",
    title="Name the Task Type Before You Write",
    target=("Given a prompt, identify whether it is synthesis (a source set to combine), source-free (a general "
            "question answered from own knowledge), or multi-perspective (set perspectives to weigh), name the "
            "moves it rewards, then plan for a fresh prompt rather than defaulting to one approach. Delivery "
            "untimed. Written at the paragraph. Trait: task analysis and process."),
    acc_tags=["ACC.W.PROD.4", "CCSS.W.11-12.4", "CCSS.W.11-12.5"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.05", "sot": "icm course-G11.md L29",
                "taught_stimulus": "ACC-W910-SYNTH-SET-0002",
                "transfer_stimulus": "ACC-W910-MP-PERSP-0003",
                "one_idea": "Name the task type first from its tell; the wrong type means the wrong moves.",
                "one_reminder": "Source SET = synthesis; NO passage = source-free; printed PERSPECTIVES = multi-perspective.",
                "playbook": "_phase2/playbook_T5_CHECK.md",
                "template": ("locked L01 template; binds cold mixed prompts; 3-genre task-type discrimination + "
                             "calibration, delivery UNTIMED."),
                "version_note": ("V3.1 rebuild of the pre-v3.1 lesson_g11_l29_which_task_type.py to the v3.1 build "
                                 "spec. Fixed the prior failures: (a) TEACH is now one hammered idea (ONE_IDEA "
                                 "callout + the three task types as a <ul>), the name-predict-reveal-plan routine "
                                 "moved to the REMEMBER check tool at point of first use (was two prose teach "
                                 "cards); (b) the discrimination dropped the leaked 'Grade-C design bet we label "
                                 "as a bet' prose and now uses explicit choices with the correct option NOT the "
                                 "lone-longest and a 'combine' distractor to break the token confound; (c) FRQ + "
                                 "diagnosis built with frq_prompt/setapart/checklist (no Step-N prose, no 'Scored "
                                 "on' chrome); (d) self_score is a clean predict-the-type MCQ, not a wall-of-text "
                                 "block; 'synthesize' defined with an 'is when' cue. Kept bound stimuli + every "
                                 "production unit='paragraph' (T5 ceiling)."),
                "council": ("T5/CHECK G11 review: which-task-type (synthesis vs source-free vs multi-perspective) "
                            "3-genre discrimination + calibration; name, predict, reveal, plan. self_score "
                            "calibration. names-type-vs-defaults discrimination labeled Grade-C in code. "
                            "CHECK=proposal; T5 ceiling paragraph, so plans are written at the paragraph."),
                "review_provenance": "built to the G9 L25 v3.1 pattern (icm/_config/v3_1-lesson-build-spec.md)."},
    fade_ledger_moves=["identify-task-type", "name-the-moves-it-rewards"],
    slots=[
        # ===== TEACH: ONE idea, hammered (callout + the three task types as a list; routine moved to model card) =====
        Slot("TEACH", "teach_card", "The one idea: name the type before you write",
             body=(ONE_IDEA +
                   "In these writing tasks you meet three argument task types, and each has a tell you can spot in seconds. "
                   "To synthesize is when you combine several sources into one argument of your own. Watch for "
                   "these three types and their tells:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Synthesis</strong>: the tell is a SET of sources given to "
                   "combine. It rewards weaving one argument from the set and weighting each source.</li>"
                   "<li style=\"margin:4px 0\"><strong>Source-free</strong>: the tell is a general question with "
                   "NO passage. It rewards a clear position anchored to specific examples from your own knowledge.</li>"
                   "<li style=\"margin:4px 0\"><strong>Multi-perspective</strong>: the tell is set PERSPECTIVES "
                   "printed under the issue. It rewards weighing those views and staking your own in relation.</li></ul>"
                   "You cannot fix the moves once you have committed to the wrong type, so you will first practice "
                   "naming the type on PROVIDED prompts: name it, predict its moves, see the reveal. After that you "
                   "plan for a fresh prompt using the same check.")),
        Slot("TEACH", "stimulus_display", "The prompt: a source set on AI and the workforce",
             ref="ACC-W910-SYNTH-SET-0002", bank="ai_workforce_synthesis",
             body=("Read this prompt and note its shape: how many sources it gives, whether perspectives are "
                   "printed, whether a passage is provided at all. That shape is the tell you use to name the task "
                   "type. The prompt stays on screen while you work.")),

        # ===== MODEL (before the quiz): before/after coping model + the check tool at point of first use =====
        Slot("MODEL", "annotated_before_after", "Watch a default become a named task type",
             bank="ai_workforce_synthesis",
             body=("Here is the skill in action. Read the BEFORE, then the AFTER, and notice the writer catch the "
                   "tell and switch from a default opinion to the synthesis moves." + BEFORE_AFTER_HTML +
                   " The BEFORE jumps in with one approach. The AFTER names the type from its tell and sets the "
                   "moves. Naming the type is the move. " + REMEMBER +
                   "When you meet any prompt, run this check, then plan.")),
        Slot("MODEL", "discrimination", "Which reading names the task type correctly?",
             ref="", labeled_grade_c=True, bank="ai_workforce_synthesis",
             body=("Sort these before you plan. A prompt gives four sources on AI and the workforce. Which reading "
                   "names the type from its tell, and which one just defaults? "
                   "(A) It gives four sources to combine, so it is source-free: I will state my own position and "
                   "combine examples from my own life to back it up.  "
                   "(B) It gives a SET of four sources, so it is synthesis: weave one argument from the set and "
                   "weight each source.  "
                   "(C) There is a lot of text here, so I will just summarize each source in turn and stop there. "
                   "Correct: B."),
             choices=[
                 {"id": "A", "text": "It gives four sources to combine, so it is source-free: I will state my own position and combine examples from my own life to back it up.",
                  "correct": False,
                  "why": "This misreads the tell. Four given sources is the synthesis tell, not source-free. Notice the word 'combine' here: it is combining personal examples, not the given sources, so the moves are still the wrong ones."},
                 {"id": "B", "text": "It gives a SET of four sources, so it is synthesis: weave one argument from the set and weight each source.",
                  "correct": True,
                  "why": "Correct. A set of sources to combine is the synthesis tell, and the moves named (weave one argument, weight each source) are exactly what synthesis rewards."},
                 {"id": "C", "text": "There is a lot of text here, so I will just summarize each source in turn and stop there.",
                  "correct": False,
                  "why": "Summarizing each source one by one is not synthesis. Synthesis is when you combine the sources into one argument of your own; a string of summaries names no type and runs no argument."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this prompt-reading most need?",
             bank="ai_workforce_synthesis",
             body=("Predict before the reveal. A student sees a general question with no passage and no printed "
                   "perspectives, then starts trying to weigh three perspectives that are not there. Which single "
                   "move would most improve the reading? "
                   "(A) Recognize that with no passage and no perspectives it is source-free, then take a position "
                   "and anchor it with examples.  "
                   "(B) Invent three perspectives on the question, weigh those made-up views against each other, "
                   "and only afterward stake a view of one's own.  "
                   "(C) Go back through the prompt slowly to hunt for the source set that must have been missed, "
                   "then weave those imagined sources together into one argument.  "
                   "(D) Stop planning the type altogether and simply write faster, pushing out as many words as "
                   "possible before running out of room."),
             feedback=("Correct: A. No passage and no printed perspectives is the source-free tell, so the fix runs "
                       "position-plus-examples. Inventing perspectives (B) or hunting for a source set (C) misreads "
                       "the type; writing faster (D) does not fix the misread.")),

        # ===== SUPPORTED: predict the TYPE (calibration MCQ) -> then plan the SAME prompt (frame + checklist) =====
        Slot("SUPPORTED", "self_score", "Predict a prompt's type, then see the reveal",
             ref="", bank="ai_workforce_synthesis",
             body=("Predict, then reveal. A prompt reads: 'An issue is stated, followed by Perspective One, "
                   "Perspective Two, and Perspective Three.' Which task type is it?"),
             choices=[
                 {"id": "MP", "text": "Multi-perspective", "correct": True,
                  "why": "Correct. The tell is the printed perspectives, so it is multi-perspective. It rewards "
                         "weighing the given views and staking your own in relation, not a source-free opinion and "
                         "not synthesizing a source set."},
                 {"id": "SF", "text": "Source-free", "correct": False,
                  "why": "Source-free has NO passage and no printed views, just a general question. Here the "
                         "perspectives are printed for you, and that changes the task to multi-perspective."},
             ]),
        Slot("SUPPORTED", "production_frq", "Name the type and plan its moves",
             ref="", bank="ai_workforce_synthesis", rubric_ref="rc.ap", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro=("The AI-workforce prompt gives you this directive above the sources: \"Using the four "
                        "sources below on how artificial intelligence will reshape the American workforce, write "
                        "an essay that develops your own position, drawing on at least three of them.\" Write a "
                        "short plan that names the task type and lists the first moves it rewards."),
                 checklist_block=checklist(title="Use this check:", rows=[
                     "Name the type from a real tell (source set, no passage, or printed perspectives).",
                     "List the first moves that type rewards (for synthesis: weave one argument, weight each source, cite each).",
                 ]),
                 closer="Write your plan as one paragraph: name the type, name its tell, and list the first moves.")),
        # DIAGNOSIS: watch the check run on a provided weak read, then run it on a fresh prompt read
        # (stateless-safe; the material is provided, and the self-check is on the same item, not a prior submission).
        Slot("MODEL", "diagnosis_frq", "Check a fresh task-type read",
             ref="", bank="ai_workforce_synthesis", scored=True,
             body=frq_prompt(
                 intro="First watch the check run on a weak read, then run it on your own fresh read of the "
                       "AI-workforce prompt.",
                 setapart_block=setapart("Weak read to check:",
                                         "It has some text, so I will just summarize it.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("A source SET?", "Yes. Four sources are given to combine. That is the synthesis tell."),
                     ("Do the named moves match?", "No. Summarizing is not synthesizing. Switch to weaving one argument and weighting each source."),
                 ]),
                 closer="Now you: read the AI-workforce prompt, name its type and the tell that gives it away, "
                        "list the moves it rewards, then run the same two questions on your read. Finish by naming "
                        "the task type.")),

        # ===== INDEPENDENT: plan for the prompt with no checklist scaffold + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Name the type and plan on your own",
             ref="", bank="ai_workforce_synthesis", rubric_ref="rc.ap", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="On your own now, no checklist. The AI-workforce prompt directs: \"Using the four sources "
                       "below, write an essay that develops your own position, drawing on at least three of "
                       "them.\" Write a short plan that names its task type (with the tell that gives it away) and "
                       "lists the first moves that type rewards.",
                 closer="Before you submit, check yourself: is the type named from a real tell, and do the moves "
                        "match it? Naming the type before you plan is what every real written response is built on, "
                        "and you are ready to do it cold.")),

        # ===== TRANSFER: same name-the-type move, a NEW prompt (standardized testing), bank-partitioned =====
        Slot("TRANSFER", "stimulus_display", "A NEW prompt: standardized testing (with perspectives)",
             ref="ACC-W910-MP-PERSP-0003", bank="mp_standardized_testing",
             body=("Read this new prompt on standardized testing. Note its shape, whether a source set, a bare "
                   "question, or printed perspectives, so you can name its task type from the tell. The prompt "
                   "stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Name the type and plan on a NEW prompt",
             ref="", bank="mp_standardized_testing", rubric_ref="rc.ap", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="New prompt, same move. For the standardized-testing prompt, write a short plan that names "
                       "its task type (with its tell) and lists the first moves it rewards.",
                 closer="Check yourself: is the type named from a real tell, and do the moves match it? Same "
                        "name-the-type-then-plan move as the AI-workforce prompt, on a new prompt.")),
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
