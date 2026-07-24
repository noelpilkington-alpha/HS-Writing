"""
lesson_g12_l12_which_frq_type.py  -  G12 KC C.12.02, ARCHETYPE T5: RUBRIC-REVISION (CHECK, paragraph). V3.1.

G12 course L12 (Unit 2, review), rebuilt to the v3.1 build spec (icm/_config/v3_1-lesson-build-spec.md) from the
pre-v3.1 lesson_g12_l12_which_frq_type.py. Teaching point (KEPT): given an AP Lang FRQ, name whether it is
SYNTHESIS, RHETORICAL ANALYSIS, or ARGUMENT, and name the move-set + rubric rows it rewards, then plan for a fresh
FRQ rather than defaulting to the approach practiced last. Delivery UNTIMED. KC C.12.02.

Bound stimuli KEPT: taught = ACC-W910-SYNTH-SET-0001 (renewable-grid synthesis source set, bank
renewable_grid_synthesis) -> transfer = ACC-W910-RA-SINGLE-0002 (Cross of Gold single passage, bank ra_speech_2,
bank-partitioned). rc.ap, unit="paragraph" (T5 ceiling is paragraph, so every scored plan is a paragraph-level
write). CHECK=proposal.

V3.1 changes over the prior L12 (all prior gate failures fixed):
  1. TEACH is now ONE idea, hammered: a teal ONE_IDEA callout ("name the type before you write") + the three FRQ
     types and their tells as a real <ul> list (was two prose teach cards). "synthesize" defined with a "means"
     cue in TEACH (define-before-use).
  2. MODEL is a coping-model think-aloud: a writer's First try / Second try run the wrong move-set on the
     synthesis FRQ, catch the miss, then Final names the type and runs the moves (literal BEFORE + AFTER inline).
     The reusable check tool sits in the REMEMBER dashed box (<ol> 3-question checklist) at point of first use.
  3. NO leaked internal labels: the old discrimination prose said "a Grade-C design bet we label as a bet"
     (leaked_internal_label). Removed; the discrimination now uses explicit choices=[{id,text,correct,why}] with
     the correct option NOT the lone-longest, and the reveal lives in a "Correct: X" tail, not in option text.
  4. FRQ + diagnosis bodies built with frq_prompt / setapart / checklist (no "Step 1/2" prose, no "Scored on"
     chrome). SUPPORTED opens with a fill-in FRAME; diagnosis watches a check run on a PROVIDED weak plan first.
  5. self_score is a clean predict-the-type MCQ (short prompt + choices carrying the reveal), not a prose block.
     Own words, no fabricated figures (renewable-grid facts stay faithful to the bound source), no em dashes.
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
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Name the writing task type <strong>before</strong> you write. '
'The type decides the move-set, so running the wrong moves answers the wrong question, however strong the '
'writing.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: name the type from its tell</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you plan any writing task, ask these three questions:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0"><strong>A set of sources on one question?</strong> That is synthesis: combine them into one position and cite each source.</li>'
'<li style="margin:2px 0"><strong>One passage asking HOW the writer builds the case?</strong> That is rhetorical analysis: analyze the writer\'s choices and their effect.</li>'
'<li style="margin:2px 0"><strong>A general question with no passage?</strong> That is argument: defend a position with your own examples.</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">The trap is running the move-set you practiced last, so name the type first, every time.</div></div>')

# coping-model think-aloud: First try / Second try run the wrong move-set on the synthesis FRQ, then Final names it.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> the writer runs the wrong move-set</span>'
    '<p style="margin:8px 0 0;font-size:15px"><strong>First try:</strong> I see four sources on renewable energy, '
    'so I start summarizing source one, then source two, then the rest. <strong>Second try:</strong> that feels '
    'thin, so I switch to just arguing my own opinion about renewable energy and leave the sources out.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The catch: I never named the writing task type. A set of '
    'sources on one question is the synthesis tell, and summarizing one by one, or arguing with no sources, is '
    'not the move.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> the writer names the type, then runs its moves</span>'
    '<p style="margin:8px 0 0;font-size:15px"><strong>Final:</strong> '
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">NAMED THE TYPE</span> A set of sources on one question means synthesis. I take one '
      'position on whether the grid can run mostly on renewables, weave at least three of the sources to support '
      'it (for example, that renewables already supply about a fifth of US electricity but need far more storage '
      'to stay steady), and cite each source I use.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Naming the type first set the moves: weave one '
    'position from the sources and cite them. Two moves did the work, name the type from its tell, then run the '
    'move-set that type rewards.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G12-C1202-0012", grade="9-10", lesson_type=5,
    unit="G12 U2 - Which FRQ type is this? (3-genre discrimination)",
    title="Name the Writing Task Type Before You Write",
    target=("Given a writing task, identify whether it is synthesis, rhetorical analysis, or argument, name the "
            "move-set and rubric rows it rewards, then plan for a fresh writing task instead of defaulting to one "
            "approach. Delivery untimed. Written at the paragraph. Trait: task analysis and process."),
    acc_tags=["ACC.W.PROD.4", "CCSS.W.11-12.4", "CCSS.W.11-12.5"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.12.02", "sot": "icm course-G12.md L12",
                "taught_stimulus": "ACC-W910-SYNTH-SET-0001",
                "transfer_stimulus": "ACC-W910-RA-SINGLE-0002",
                "one_idea": "Name the FRQ type before you write; the type decides the move-set.",
                "one_reminder": "Sources set = synthesis; one passage asking how = analysis; general question = argument.",
                "playbook": "_phase2/playbook_T5_CHECK.md",
                "template": ("locked L01 template; binds mixed cold FRQ stimuli; 3-genre FRQ-type discrimination "
                             "+ calibration, delivery UNTIMED."),
                "version_note": ("V3.1 rebuild of the pre-v3.1 lesson_g12_l12_which_frq_type.py to the v3.1 build "
                                 "spec. Fixed the prior gate failures: (a) TEACH is now one hammered idea (ONE_IDEA "
                                 "callout + the three tells as a <ul>), 'synthesize' defined with a 'means' cue; "
                                 "(b) MODEL is a coping-model First try/Second try/Final think-aloud with literal "
                                 "BEFORE + AFTER, and the reusable check tool lives in a REMEMBER <ol> at point of "
                                 "first use; (c) the discrimination dropped the leaked 'Grade-C design bet' prose "
                                 "and now uses explicit choices with the correct option NOT the lone-longest and "
                                 "the reveal in a Correct: tail; (d) FRQ + diagnosis built with frq_prompt/setapart/"
                                 "checklist (fill-in frame first, no Step-N prose); (e) self_score is a clean "
                                 "predict-the-type MCQ. Kept id/type/kc/unit/bound stimuli; every production "
                                 "unit='paragraph' (T5 ceiling)."),
                "council": ("T5/CHECK G12 review: which-FRQ-type (synthesis vs rhetorical-analysis vs argument) "
                            "3-genre discrimination + calibration; predict, reveal, plan. self_score "
                            "calibration. names-type-vs-defaults discrimination labeled Grade-C in code. "
                            "CHECK=proposal; unit=paragraph."),
                "review_provenance": "built to the G9 L01/L25 v3.1 pattern (icm/_config/v3_1-lesson-build-spec.md)."},
    fade_ledger_moves=["identify-frq-type", "name-the-move-set"],
    slots=[
        # ===== TEACH: ONE idea, hammered (callout + the three tells as a list; 'synthesize' defined here) =====
        Slot("TEACH", "teach_card", "The one idea: name the type before you write",
             body=(ONE_IDEA +
                   "There are three writing task types, and each has a tell you can spot at once. "
                   "To synthesize means to combine several sources into one argument of your own. Watch for these "
                   "tells:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Synthesis</strong>: a SET of sources on one question. It "
                   "rewards weaving one position from the sources and citing each one, not summarizing them one "
                   "at a time.</li>"
                   "<li style=\"margin:4px 0\"><strong>Rhetorical analysis</strong>: ONE passage that asks HOW "
                   "the writer builds the case. It rewards analyzing the writer's choices and their effect, not "
                   "arguing whether the writer is right.</li>"
                   "<li style=\"margin:4px 0\"><strong>Argument</strong>: a general question with no passage. It "
                   "rewards a defensible position carried by your own specific examples.</li></ul>"
                   "Naming the type first sets the move-set and the rubric rows in play. The rubric rows are the "
                   "categories every writing task is scored on: a thesis row (a defensible position), an evidence row (the "
                   "support you supply and reason from), and a complexity row (the depth and nuance of the "
                   "argument). Today: name a fresh writing task's type, name its moves, and plan.")),
        Slot("TEACH", "stimulus_display", "Read the writing task: a source set on a renewable grid",
             ref="ACC-W910-SYNTH-SET-0001", bank="renewable_grid_synthesis", tag="buy_in",
             body=("Read this writing task. Notice its shape (a set of sources, one passage asking how, or a general "
                   "question with no passage) so you can name its type. The prompt stays on screen while you "
                   "work.")),

        # ===== MODEL (before the quiz): coping-model First try/Second try/Final + the check tool at first use =====
        Slot("MODEL", "annotated_before_after", "Watch a wrong move-set become a named writing task type",
             bank="renewable_grid_synthesis",
             body=("Here is the skill in action. Read the BEFORE, then the AFTER, and notice the writer catching "
                   "the miss and naming the type." + BEFORE_AFTER_HTML +
                   " The BEFORE runs the wrong moves; the AFTER names the type from its tell and runs the "
                   "move-set that type rewards. Naming the type is the move. " + REMEMBER +
                   "When you meet any writing task, run this three-question check before you plan.")),
        Slot("MODEL", "discrimination", "Which reading names the writing task type correctly?",
             ref="", labeled_grade_c=True, bank="renewable_grid_synthesis",
             body=("Spot the target before you plan. This writing task hands you four sources on one question. Which "
                   "reading NAMES THE TYPE from its tell, and which just defaults to a habit? "
                   "(A) It includes several passages, but I write more comfortably when I argue my own opinion, "
                   "so I will just argue my own view of the topic here.  "
                   "(B) It gives a set of sources on one question, so it is synthesis: I will weave one position "
                   "from the sources and cite each one I use.  "
                   "(C) It has multiple sources in front of me, so I will summarize what each source says in turn "
                   "so the reader learns all of them.  "
                   "(D) There are several sources here, so I will pick the single most persuasive one and analyze "
                   "how its author uses tone and word choice to convince the reader.  "
                   "Correct: B names the type from the tell (a set of sources on one question means synthesis); "
                   "A, C, and D ignore the tell or misread the type and default to the wrong move-set."),
             choices=[
                 {"id": "A", "text": "It includes several passages, but I write more comfortably when I argue my own opinion, so I will just argue my own view of the topic here.",
                  "correct": False,
                  "why": "This ignores the tell. A set of sources on one question is the synthesis tell, so arguing with the sources left out runs the wrong move-set."},
                 {"id": "B", "text": "It gives a set of sources on one question, so it is synthesis: I will weave one position from the sources and cite each one I use.",
                  "correct": True,
                  "why": "Correct. A set of sources on one question is the synthesis tell, and this names the moves synthesis rewards: weave one position from the sources and cite each."},
                 {"id": "C", "text": "It has multiple sources in front of me, so I will summarize what each source says in turn so the reader learns all of them.",
                  "correct": False,
                  "why": "Summarizing one source at a time is not synthesis. The tell is right (a source set), but the move is wrong: synthesis weaves the sources into one position, it does not list them."},
                 {"id": "D", "text": "There are several sources here, so I will pick the single most persuasive one and analyze how its author uses tone and word choice to convince the reader.",
                  "correct": False,
                  "why": "This misreads a source set as rhetorical analysis. Analyzing how one author writes is the move for one passage that asks how; a set of sources on one question calls for weaving them into one position, not studying a single author's style."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this writing task reading most need?",
             bank="renewable_grid_synthesis",
             body=("Predict before the reveal. A student is given one passage and asked how the author persuades "
                   "the audience, and starts arguing whether the author is right about the topic. Which single "
                   "move would most improve it? "
                   "(A) Recognize it is rhetorical analysis, since one passage asks how, and analyze the writer's "
                   "choices and their effect.  "
                   "(B) Argue the topic more forcefully and take a much stronger stand on whether the writer's "
                   "position on the issue is correct.  "
                   "(C) Add personal stories and examples from your own life that support your own opinion about "
                   "the topic under discussion.  "
                   "(D) Summarize the passage by retelling its main points in order so the reader knows what the "
                   "passage is about."),
             feedback=("Correct: A. One passage asking how is the rhetorical-analysis tell, so the fix analyzes "
                       "the writer's choices and their effect, not the topic. Arguing harder (B), personal "
                       "stories (C), or summary (D) all answer the wrong question.")),

        # ===== SUPPORTED: predict the type (calibration MCQ) -> then plan with a fill-in FRAME =====
        Slot("SUPPORTED", "self_score", "Predict a writing task's type, then see the reveal",
             ref="", bank="renewable_grid_synthesis",
             body=("Predict, then reveal. A new writing task gives a general question about whether communities should "
                   "work to preserve their old traditions. No passage is provided, and you are asked to take and "
                   "defend a position. Which type is it?"),
             choices=[
                 {"id": "argument", "text": "Argument", "correct": True,
                  "why": "Correct. A general question with no passage is the argument tell. It rewards a "
                         "defensible position carried by your own specific examples, not combining sources and "
                         "not analyzing a passage."},
                 {"id": "synthesis", "text": "Synthesis", "correct": False,
                  "why": "Synthesis needs a set of sources to combine. This writing task gives no sources, so there is "
                         "nothing to weave or cite; naming it synthesis would run the wrong moves."},
             ]),
        Slot("SUPPORTED", "production_frq", "Name the type and plan its moves",
             ref="", bank="renewable_grid_synthesis", rubric_ref="rc.4trait", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="You just read a set of four sources on whether the United States grid can run mostly on "
                       "renewable energy. Write a short plan that names this writing task's type and its first moves.",
                 setapart_block=setapart("Fill in this frame:",
                                         "This writing task is a ______ task because its tell is ______. The first moves it "
                                         "rewards are ______, and it asks me to cite ______."),
                 checklist_block=checklist(title="Before you submit:", rows=[
                     "Name the type from a real tell (a set of sources, one passage asking how, or a general question).",
                     "List the first moves that type rewards.",
                     "Name what the plan must include (for synthesis: a position, woven sources, and citations).",
                 ]),
                 closer="Write your plan as a short paragraph.")),
        # COUNCIL FIX (2026-07-24): Option A (later-in-arc), watch-then-do: demo preserved, produce is the graded
        # act. The task listed 0012 as check_only, but this slot is actually a watch-then-do: it watched a type
        # check run on a PROVIDED weak plan (pre-answered (q,a) tuple rows) and then bundled a fresh plan write + a
        # run-and-name-the-type tail in one box (the (q,a) rows leaked the answers). The coping-model demo is
        # PRESERVED as read-only narration (the type check shown running on the weak plan, in plain declarative
        # prose in the intro). The student's ONLY graded act is the fresh plan; the checks sit read-only beneath as
        # plain strings; the run-and-name tail is dropped. unit/frq_type/rubric_ref added to declare the paragraph
        # grain (matches this lesson's other production writes). Stays on the taught bank (no new source).
        Slot("MODEL", "diagnosis_frq", "Write a fresh writing task type read",
             ref="", bank="renewable_grid_synthesis", rubric_ref="rc.4trait", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="First, watch the type check run on the weak plan below. The plan sees text on the page and "
                       "jumps to summarizing it. Running the check: the writing task is a set of four sources on "
                       "one question, which is the synthesis tell, not a passage to summarize; summarizing is not "
                       "the move synthesis rewards, weaving one position and citing the sources is; so the plan "
                       "should name it a synthesis and plan to take a position, weave at least three sources, and "
                       "cite each. Now write a fresh plan of your own.",
                 setapart_block=setapart("Weak plan the check was run on:",
                                         "There is text on the page, so I will summarize what it says.", "red"),
                 checklist_block=checklist(title="Check your plan against these (no need to type answers):", rows=[
                     "Did you name the type from a real tell (a set of sources, one passage asking how, or a general question)?",
                     "Do the moves you named match that type?",
                     "Does the plan say what to include (for synthesis: a position, woven sources, and citations)?",
                 ]),
                 closer="Read the writing task again, then write one fresh plan that names its type from the tell "
                        "and lists the first moves that type rewards. Run the three checks above before you submit.")),

        # ===== INDEPENDENT: name-the-type-and-plan with no frame + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Name the type and plan on your own",
             ref="", bank="renewable_grid_synthesis", rubric_ref="rc.4trait", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now, no frame. For the writing task you read, write a short plan that names its type "
                       "from a real tell and lists the first moves that type rewards.",
                 closer="Before you submit, check that the type is named from a real tell and the moves match it. "
                        "This is what every real writing task answer is built on: name the type, then run its moves. You "
                        "are ready to do it cold.")),

        # ===== TRANSFER: same name-the-type move, a NEW FRQ (a single passage to analyze), bank-partitioned =====
        Slot("TRANSFER", "stimulus_display", "A NEW writing task: a single passage to analyze",
             ref="ACC-W910-RA-SINGLE-0002", bank="ra_speech_2",
             body=("Read this new writing task. It gives you the single passage below and then asks: write an essay that "
                   "analyzes the choices the speaker makes to persuade his audience, supporting your analysis "
                   "with evidence from the passage. Notice its shape (a set of sources, one passage asking how, "
                   "or a general question with no passage) so you can name its type from the tell yourself. The "
                   "prompt stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Name the type and plan on a NEW writing task",
             ref="", bank="ra_speech_2", rubric_ref="rc.4trait", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="New writing task, same move. The writing task gives you the single passage above and asks: write an essay "
                       "that analyzes the choices the speaker makes to persuade his audience, using evidence from "
                       "the passage. Write a short plan that names this writing task's type from its tell and lists the "
                       "first moves it rewards.",
                 closer="Before you submit, check that you named the type from a real tell in the passage and that "
                        "your first moves match that type. Run the same three-question check you used on the "
                        "renewable-energy writing task, now on a new one you diagnose yourself.")),
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
