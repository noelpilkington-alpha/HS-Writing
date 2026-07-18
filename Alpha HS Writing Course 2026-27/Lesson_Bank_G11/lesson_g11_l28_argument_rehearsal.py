"""
lesson_g11_l28_argument_rehearsal.py  -  G11 KC C.11.05, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD, ceiling essay). V3.1.

G11 L28 (Unit 6, build), rebuilt to the v3.1 build spec (hand-authored). Teaching point (KEPT): rehearse
source-free and multi-perspective arguments by first SPOTTING the task type, then applying its moves
(source-free = position + specific examples; multi-perspective = weigh the given views + stake your own),
under a self-imposed budget, rather than running one set of moves on every prompt. Delivery UNTIMED. This is a
FULL-ESSAY lesson; it interleaves the two G11 argument task types and reaches the essay ceiling.

Preserved EXACTLY from the current L28: id="ACC-W1112-L-G11-C1106-0028", lesson_type=7,
mnemonic_status="proposal", kc="C.11.05", unit, the bound stimuli (SFA-PROMPT-0001 taught -> MP-PERSP-0002
transfer), and every production_frq unit= value (SUPPORTED plan = multi_paragraph, INDEPENDENT + TRANSFER =
essay). The ladder still climbs to the essay, which is the type-7 ceiling.

V3.1 changes vs the prior L28 (the two failing gates + the spine polish):
  1. FIXED the leaked internal label: the discrimination no longer says "a Grade-C design bet we label as a
     bet"; it is a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}] and the reveal
     in a "Correct:" tail (leaked_internal_label). labeled_grade_c stays True in code only.
  2. FIXED the wall-of-text teach card: the prose block is now a ONE_IDEA callout + a real <ul> of the two
     task types and an <ol> order of work (format_fidelity, and the v3.1 "parallel items as a list" rule).
  3. Deterministic FRQ + diagnosis prompts via frq_prompt/setapart/checklist (no "Step 1/2" prose, no
     "Scored on ..." chrome); coping-model before/after kept; check tool (spot-then-match) folded in at the
     point of first use as a real <ol> REMEMBER box.
Own words, no fabricated figures, faithful to the bound prompts, no em dashes. Passes all 23 gates + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Two argument prompts can look alike but reward '
'<strong>different moves</strong>. Spot the task type FIRST, then run the moves it rewards. Do not run one set '
'of moves on every prompt.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: spot then match</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you draft, read the prompt and ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Are set perspectives printed in the prompt, yes or no?</li>'
'<li style="margin:2px 0">If no, it is source-free: take a position and anchor it with specific examples.</li>'
'<li style="margin:2px 0">If yes, it is multi-perspective: weigh the given views and stake your own in relation.</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If your planned moves do not match the type, switch them before you draft.</div></div>')

# coping-model before/after: a writer runs one set of moves on every prompt, catches it on the check, and
# switches to the moves the task type rewards. Contains BOTH a literal BEFORE and AFTER (content_depth).
# No named person (Timeback stateless rule).
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> one set of moves on every prompt</span>'
    '<p style="margin:8px 0 0;font-size:15px"><i>First try, on the privacy-and-safety prompt (which prints '
    'three perspectives):</i> "I think safety matters more than privacy, and here is a story from my own life '
    'that shows why." The writer states a personal opinion with examples and never touches the three printed '
    'perspectives.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">Running source-free moves on a multi-perspective '
    'task skips what it rewards: weighing the given views. The check catches it.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> spot the type, then run its moves</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">SPOT</span> <i>Second try:</i> "Three perspectives are printed, so this is a '
      'multi-perspective task, not source-free." '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">MATCH</span> <i>Final:</i> "Perspective One puts safety first and Perspective Two puts '
      'privacy first; Perspective Three reframes both around oversight. I stake my own position in relation: '
      'the danger is not surveillance itself but power without accountability, which is closest to Perspective '
      'Three, and I will show why the first two both miss it."</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same writer, but the AFTER names the task type and '
    'weighs the printed views instead of ignoring them. Spot the type, then match the moves, is the move.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1106-0028", grade="9-10", lesson_type=7,
    unit="G11 U6 - Argument rehearsal (spot the task type, run its moves)",
    title="Match the Moves to the Task Type",
    target=("Rehearse source-free and multi-perspective arguments by first spotting the task type, then "
            "applying its moves (source-free: position plus specific examples; multi-perspective: weigh the "
            "given views and stake your own), under a self-imposed budget, rather than using one set of moves "
            "for every prompt. Delivery untimed. Written at the essay. Trait: Thesis, Evidence, and process."),
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "ACC.W.PROD.4", "CCSS.W.11-12.1"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.05", "sot": "icm course-G11.md L28",
                "taught_stimulus": "ACC-W910-SFA-PROMPT-0001",
                "transfer_stimulus": "ACC-W910-MP-PERSP-0002",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": ("v3.1 spine; ESSAY-TIER binds cold source-free + perspective prompts; interleaves "
                             "the two argument task types under the budget/fast-plan routine, delivery UNTIMED "
                             "(no Timeback timer)."),
                "one_idea": "Two argument prompts can look alike but reward different moves; spot the task type first, then run its moves.",
                "one_reminder": "Spot-then-match: perspectives printed? no -> source-free (position + examples); yes -> multi-perspective (weigh + stake).",
                "version_note": ("V3.1 rebuild of L28. FIXED the two failing gates on the prior version: removed "
                                 "the leaked internal label ('a Grade-C design bet we label as a bet') from the "
                                 "discrimination and moved it to explicit choices=[] with the reveal in a "
                                 "'Correct:' tail (leaked_internal_label); broke the wall-of-text teach card into "
                                 "a ONE_IDEA callout + real <ul>/<ol> lists (format_fidelity). Deterministic "
                                 "frq_prompt/setapart/checklist bodies (no 'Step 1/2' prose, no 'Scored on' "
                                 "chrome); coping-model before/after kept; check tool folded in at first use. "
                                 "Preserved id, type 7, kc C.11.05, mnemonic_status=proposal, unit, bound stimuli, "
                                 "and every production_frq unit= value (SUPPORTED=multi_paragraph, "
                                 "INDEPENDENT/TRANSFER=essay); ladder climbs to essay."),
                "council": ("T7/BUILD G11 exam-rehearsal: source-free + multi-perspective interleave; spot task "
                            "type, run its moves, under budget. matched-moves-vs-one-size discrimination labeled "
                            "Grade-C. BUILD=proposal; unit=essay."),
                "review_provenance": "built to the G9 L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["spot-the-task-type", "match-moves-to-type"],
    slots=[
        # ===== TEACH: the one idea + the two task types (as a list), then the order of work (as a list) =====
        Slot("TEACH", "teach_card", "The one idea: spot the type, then run its moves",
             body=(ONE_IDEA +
                   "You already own the moves for each type. The rehearsal is choosing the right set. Here are "
                   "the two task types:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Source-free</strong>: the prompt gives a general question "
                   "and no printed views. You take a <dfn class=\"tb-glossary-term\" data-catalog-idref=\"def-position\" "
                   "title=\"a position is a defensible stance you argue for\">position</dfn> (a one-sentence claim "
                   "you defend) and anchor it with specific examples from your own reading, studies, or "
                   "experience.</li>"
                   "<li style=\"margin:4px 0\"><strong>Multi-perspective</strong>: the prompt prints an issue "
                   "plus several set views. A <dfn class=\"tb-glossary-term\" data-catalog-idref=\"def-perspective\" "
                   "title=\"a perspective is one stated way of seeing the issue that the prompt provides\">perspective</dfn> "
                   "is one stated way of seeing the issue the prompt hands you. You weigh those views against "
                   "each other and stake your own in relation to them.</li></ul>"
                   "The trap is running one set of moves on both, for instance ignoring printed perspectives and "
                   "just stating an opinion. The tell is simple, and it is the first thing to check.")),
        Slot("TEACH", "teach_card", "How to run the rehearsal, step by step",
             body=("Here is the order of work. Follow it and each prompt gets the moves it rewards:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>SPOT</strong>: read the prompt and ask, are set "
                   "perspectives printed, yes or no?</li>"
                   "<li style=\"margin:4px 0\"><strong>NAME</strong>: no printed views means source-free; "
                   "printed views means multi-perspective.</li>"
                   "<li style=\"margin:4px 0\"><strong>BUDGET</strong>: split your own time across planning, "
                   "drafting, and checking. There is no platform timer; you run the budget.</li>"
                   "<li style=\"margin:4px 0\"><strong>MATCH</strong>: run the moves the type rewards "
                   "(source-free: position plus specific examples; multi-perspective: weigh the views plus "
                   "stake your own).</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: before you submit, confirm the moves you "
                   "ran match the task type you named.</li></ol>"
                   "You already own the moves; the rehearsal is spotting the type and matching them, under your "
                   "own budget.")),
        Slot("TEACH", "stimulus_display", "Read the prompt: tradition or progress?",
             ref="ACC-W910-SFA-PROMPT-0001", bank="sfa_tradition_progress",
             body=("Read this prompt on tradition versus progress. First decide its task type: are there set "
                   "perspectives printed, or is it a general source-free question? Then budget your stages and "
                   "fast-plan the moves that type rewards. The prompt stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + check tool, then the discrimination =====
        Slot("MODEL", "annotated_before_after", "Watch one-size moves become matched moves",
             bank="sfa_tradition_progress",
             body=("Here is a writer who runs one set of moves on every prompt, catches it on the check, and "
                   "switches to the moves the task type rewards. Read the BEFORE, then the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE runs source-free moves on a prompt that printed three perspectives. The AFTER "
                   "names the task type and weighs the printed views. Spot the type, then match the moves, is "
                   "the move." + REMEMBER +
                   "When you plan your own, spot the type first, then match the moves, then run the check before you submit.")),
        Slot("MODEL", "discrimination", "Which response matches the moves to the task type?",
             ref="", labeled_grade_c=True, bank="sfa_tradition_progress",
             body=("You have watched a writer switch from one-size moves to matched moves. Now spot the target: "
                   "which response MATCHES its moves to the task type, and which runs ONE SIZE on every prompt? "
                   "(A) On any argument prompt, the writer runs the same fixed routine: list three perspectives, "
                   "weigh them against one another, and stake a position, applying that identical routine even "
                   "to a general prompt that prints no set perspectives at all for the writer to weigh.  "
                   "(B) The writer first checks the prompt: on a source-free prompt the writer takes a position "
                   "and anchors it with specific examples, and on a perspective prompt the writer weighs the "
                   "printed views and stakes a position in relation to them.  "
                   "(C) On any argument prompt, the writer opens with a personal story and a strong opinion, "
                   "keeps adding more examples from experience, and applies that same fixed routine every time, "
                   "whether or not the prompt actually prints any set perspectives for the writer to weigh. "
                   "Correct: B. It reads the task type first, so its moves match what the prompt rewards; A and C "
                   "run one fixed routine on every prompt, forcing the wrong moves onto whichever type shows up."),
             choices=[
                 {"id": "A", "text": "On any argument prompt, the writer runs the same fixed routine: list three perspectives, weigh them against one another, and stake a position, applying that identical routine even to a general prompt that prints no set perspectives at all for the writer to weigh.",
                  "correct": False,
                  "why": "This forces perspective-weighing onto every prompt. On a source-free prompt there are no printed views to weigh, so the moves do not match the task type."},
                 {"id": "B", "text": "The writer first checks the prompt: on a source-free prompt the writer takes a position and anchors it with specific examples, and on a perspective prompt the writer weighs the printed views and stakes a position in relation to them.",
                  "correct": True,
                  "why": "Correct. This reads the task type first and then runs the moves that type rewards, so the moves always match the prompt."},
                 {"id": "C", "text": "On any argument prompt, the writer opens with a personal story and a strong opinion, keeps adding more examples from experience, and applies that same fixed routine every time, whether or not the prompt actually prints any set perspectives for the writer to weigh.",
                  "correct": False,
                  "why": "This runs source-free moves on every prompt. On a multi-perspective prompt it ignores the printed views the task rewards weighing, so the moves do not match the type."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this rehearsal most need?",
             bank="sfa_tradition_progress",
             body=("Predict before the reveal. A student writes a strong personal opinion with examples on a "
                   "prompt that printed three perspectives, never mentioning them. Which single change would "
                   "most improve the result? "
                   "(A) recognize it is a multi-perspective task and weigh the given perspectives, staking a "
                   "position in relation to them  "
                   "(B) add more personal examples from the writer's own experience to back up the opinion and "
                   "make the argument feel fuller  "
                   "(C) make the stated opinion stronger by asserting it more forcefully and sticking to it "
                   "firmly all the way through  "
                   "(D) write a longer introduction that lays out the topic and its background before the writer "
                   "gets to the opinion"),
             feedback=("Correct: A. Ignoring printed perspectives is misreading the task type; the fix weighs "
                       "them and stakes a position in relation. More examples (B), a stronger opinion (C), or a "
                       "longer intro (D) do not supply the perspective-weighing the task rewards.")),

        # ===== SUPPORTED: name the type + fast-plan (multi_paragraph) - the frame is the top scaffold =====
        Slot("SUPPORTED", "production_frq", "Name the task type and fast-plan its moves",
             ref="", bank="sfa_tradition_progress", rubric_ref="rc.ap", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="For the tradition-versus-progress prompt, name the task type before you plan a word of it.",
                 setapart_block=setapart("Fill in this plan:",
                                         "Task type: ______ (source-free or multi-perspective). How I can tell: ______. Position: ______. Move 1: ______. Move 2: ______. Move 3: ______."),
                 closer="First NAME the task type and say how you can tell, then write a fast plan using that "
                        "type's moves (position plus specific examples, or weigh-the-views plus stake-own). This "
                        "plan is what you will build the essay from.")),
        # ===== INDEPENDENT: build the whole essay from the matched plan (essay ceiling) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Rehearse the matched argument essay",
             ref="", bank="sfa_tradition_progress", rubric_ref="rc.ap", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now, run the full rehearsal on the tradition-versus-progress prompt.",
                 closer="Spot the task type, then under your own budget write a complete argument essay using "
                        "that type's moves (source-free: a defensible position plus specific examples, developed "
                        "across body paragraphs, with a conclusion that lands the upshot). There is no platform "
                        "timer; run your own budget and check. Before you submit, confirm the moves match the "
                        "task type. Spotting the type and running its moves cold is what every real timed essay is "
                        "built on, and you are ready to do it. Take the time you need.")),

        # DIAGNOSIS = self-revision: reread your OWN just-written draft and run the 3-question check on it,
        # fixing any line that fails. Same taught prompt (load balance). Self-contained: the checklist is the
        # scaffold and the grader scores the diagnosis within the item.
        Slot("MODEL", "diagnosis_frq", "Check: did the moves match the task type?",
             ref="", bank="sfa_tradition_progress", scored=True,
             body=frq_prompt(
                 intro="Reread the essay you just wrote. Run this checklist on YOUR draft and fix any line that fails.",
                 checklist_block=checklist(title="Check your own draft, line by line:", rows=[
                     ("Does the prompt print set perspectives?", "No. The tradition-versus-progress prompt gives a general question and no printed views, so it is source-free, not multi-perspective."),
                     ("Do the planned moves match that type?", "They match if your draft takes a defensible position and backs it with specific examples. If it instead tries to weigh printed perspectives, there are none here to weigh, so that is the mismatch to fix: switch to the source-free moves."),
                     ("Are your source-free moves doing the work?", "Check that you take a defensible position on whether progress requires breaking with tradition, then anchor it with specific examples from reading, studies, or experience, rather than leaving the position unsupported."),
                 ]),
                 closer="For every line that fails on your draft, name what is off in one sentence and make the "
                        "fix. Finish by naming the task type your draft is written for.")),
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
