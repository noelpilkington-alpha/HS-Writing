"""
lesson_g9_l22_essay_mode_interleave.py  -  G9 KC C.9.01/C.9.05, ARCHETYPE T2 (essay-mode review).

G9 course L22 (Unit 4, review). Interleave the two essay MODES: argument (take a side) vs informational
(explain, no side), decided by the task verb, now at the ESSAY level (thesis + plan choice). Recycles the
whole claim/controlling-idea fork at essay scale. Locked L01 template. Binds issue_frames for topic context
(the decision is which MODE + thesis to plan, not source-mining). Taught frames: FRAME-PHONEBAN (argue) +
FRAME-PHOTOSYNTHESIS (explain); transfer: FRAME-VOLCANOES (explain, partitioned). rc.staar,
unit="multi_paragraph". T2 STAND=proposal. No coping-model persona; no source markup; no prior-work ref; no
em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report

BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> wrong mode for the verb, at the essay level</span>'
    '<p style="margin:8px 0 0;font-size:15px">Task: <i>Explain how photosynthesis works.</i> Thesis planned: '
    '"Photosynthesis is the most important process on Earth and should be taught more."</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The verb is EXPLAIN, but the thesis argues a side '
    '(most important, should be taught more). A whole essay built on this thesis answers the wrong task.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> the mode matches the verb</span>'
    '<p style="margin:8px 0 0;font-size:15px">Task: Explain how photosynthesis works. '
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">EXPLAIN MODE</span> Thesis planned: "Photosynthesis turns sunlight, water, and carbon '
      'dioxide into sugar and oxygen through steps in a plant\'s leaves."</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">The verb is explain, so the thesis is a focusing '
    'idea with no side. Now the whole essay will answer the task the verb set.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C901-0022", grade="9-10", lesson_type=7,
    unit="G9 U4 - Build essay (argue vs explain essay-mode interleave)",
    title="Argue or Explain? Choose the Essay Mode",
    target=("Given an essay task, decide from the verb whether the whole essay should ARGUE (a thesis that "
            "takes a side) or EXPLAIN (a controlling idea, no side), then plan the matching thesis. Written as "
            "an essay plan. Trait: Thesis/Purpose."),
    acc_tags=["ACC.W.ARG.1", "ACC.W.INFO.1", "CCSS.W.9-10.1a", "CCSS.W.9-10.2a"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12",
                "mnemonic_status": "proposal", "kc": "C.9.01+C.9.05", "sot": "icm course-G9.md L22",
                "taught_stimulus": "ACC-W910-FRAME-PHONEBAN",
                "taught_stimulus_2": "ACC-W910-FRAME-PHOTOSYNTHESIS",
                "transfer_stimulus": "ACC-W910-FRAME-VOLCANOES",
                "playbook": "_phase2/playbook_T2_STAND.md",
                "template": "locked L01 template; review interleave binds issue_frames (decision is mode+thesis, not source-mining).",
                "council": ("T2/STAND essay-mode review (spacing/retrieval at essay scale): the discrimination "
                            "is which MODE the essay task calls for (argue vs explain), keyed off the verb, "
                            "recycling the P1/P2 fork. right-mode-vs-wrong-mode discrimination labeled Grade-C.")},
    fade_ledger_moves=["choose-essay-mode-argue-vs-explain", "plan-the-matching-thesis"],
    slots=[
        Slot("TEACH", "teach_card", "The verb decides the whole essay's mode",
             body=("You learned to choose between two products at the sentence. An arguable claim is a sentence "
                   "that takes a side someone could reject; a controlling idea sets a focus and takes no side. At "
                   "the essay level the same choice decides the MODE of the whole essay, so it is worth getting "
                   "right before you plan. If the task verb is argue, persuade, or 'should ... ?', the essay is "
                   "an ARGUMENT: its thesis takes a side someone could reject, and every body paragraph "
                   "defends it. If the verb is explain, describe, or inform, the essay is INFORMATIONAL: its "
                   "thesis is a controlling idea that sets a focus and takes no side, and the body walks "
                   "through the parts. A controlling idea means one sentence that names a focusing angle "
                   "without taking a side. The costly mistake at essay scale is planning the wrong mode: "
                   "building a whole argument on an explain task, or a neutral explanation on an argue task. "
                   "Goal today: read the verb, choose the mode, and plan the matching thesis.")),
        Slot("TEACH", "stimulus_display", "Two tasks: phones (argue) and photosynthesis (explain)",
             ref="ACC-W910-FRAME-PHONEBAN", bank="phone_ban",
             body=("Two essay tasks with different verbs. First, an ARGUE task on phones: argue whether schools "
                   "should ban phones for the full day (framing here). Second, an EXPLAIN task on "
                   "photosynthesis: explain how it turns light into food (framing in the next slot). As you "
                   "read, decide which mode each essay should be.")),
        Slot("TEACH", "stimulus_display", "The explain task: photosynthesis",
             ref="ACC-W910-FRAME-PHOTOSYNTHESIS", bank="photosynthesis",
             body=("Here is the second task's framing: explain how photosynthesis turns light into food. The "
                   "verb is explain, so this essay should be informational, a focusing thesis with no side. You "
                   "only need the topic and its parts.")),
        Slot("TEACH", "discrimination", "Which thesis matches the essay's verb?",
             ref="", labeled_grade_c=True, bank="photosynthesis",
             body=("Sort before you plan (spotting the target first, a Grade-C design bet we label as a bet, "
                   "not a proven ingredient). The task: EXPLAIN how photosynthesis works. Which planned thesis "
                   "matches that verb? "
                   "(A) Photosynthesis is easily the most important natural process on Earth, and it truly deserves far more attention than any other topic.  "
                   "(B) Photosynthesis turns sunlight, water, and carbon dioxide into sugar and oxygen through "
                   "steps in a plant's leaves. "
                   "Correct: B. The verb is explain, which calls for a focusing thesis with no side. (A) argues "
                   "a side (most important, deserves attention), the wrong mode for an explain task. (B) sets a "
                   "focus and takes no side. Matching the mode to the verb is the move.")),
        Slot("MODEL", "annotated_before_after", "Watch the essay mode get matched to the verb",
             bank="photosynthesis",
             body=("Here is an essay thesis in the wrong mode being switched to match the verb. Read the "
                   "BEFORE, then the AFTER, and notice the arguing thesis become a focusing one for an explain "
                   "task." + BEFORE_AFTER_HTML +
                   " The BEFORE argues a side on an explain task. The AFTER sets a focus with no side. Choosing "
                   "the mode the verb calls for is the move.")),
        Slot("MODEL", "predict_the_fix", "What does this essay plan most need?",
             bank="photosynthesis",
             body=("Diagnose before the reveal. Task: 'Argue whether schools should ban phones all day.' A "
                   "student plans this thesis: 'Phones are common in schools, and there are many rules about "
                   "them.' Which single change would most improve the plan? "
                   "(A) switch to an argument thesis that takes a side on the full-day ban, since the verb is "
                   "argue  "
                   "(B) add more background about how common phones are in schools and the many rules that "
                   "cover them  "
                   "(C) plan several more body paragraphs so there are enough sections to fill out a complete "
                   "essay  "
                   "(D) explain how phones actually work and what students use them for throughout the school "
                   "day"),
             feedback=("Correct: A. The verb is argue, which calls for a thesis that takes a side, but the plan "
                       "sets up a neutral explanation of phone rules, the wrong mode. The fix is an argument "
                       "thesis ('Schools should ban phones all day, because ...'). More background (B), more "
                       "paragraphs (C), or explaining how phones work (D) all keep the wrong mode.")),
        Slot("SUPPORTED", "production_frq", "Name the mode and plan the thesis",
             ref="", bank="photosynthesis", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=("For the EXPLAIN task on photosynthesis, first name the mode the verb calls for (argument or "
                   "informational). Then write the planned THESIS that matches it. Goal: name the correct mode, "
                   "then a thesis that fits (a focusing idea, no side). Do not plan an argument thesis for an "
                   "explain task. Scored on Thesis/Purpose.")),
        Slot("MODEL", "diagnosis_frq", "Check a plan: does the thesis match the verb?",
             ref="", bank="photosynthesis", scored=True,
             body=("First watch the check run on a provided plan, then run it on a fresh one of your own. "
                   "Task: explain how photosynthesis works. Provided plan thesis: 'Plants are amazing and we "
                   "should protect them.' Run the check step by step. Step 1, what mode does the verb call for? "
                   "Explain, so a focusing thesis with no side. Step 2, does the thesis match? No, it argues a "
                   "side (should protect them), so switch to a focusing idea. Now you: for the same explain "
                   "task, plan a fresh thesis, then check it, does its mode match the verb? Fix it if not. "
                   "Finish by naming the mode and confirming your thesis matches.")),
        Slot("INDEPENDENT", "production_frq", "Choose the mode and plan the thesis (photosynthesis)",
             ref="", bank="photosynthesis", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=("On your own now. Task: explain how photosynthesis turns light into food. Name the mode the "
                   "verb calls for, then plan the matching THESIS and a one-line note on what the body will "
                   "cover. Before you submit, check: does the mode match the verb, and does the thesis fit that "
                   "mode (focusing, no side)? Fix any that fail before you submit. Scored on Thesis/Purpose.")),
        Slot("TRANSFER", "stimulus_display", "The topic: volcanoes",
             ref="ACC-W910-FRAME-VOLCANOES", bank="volcanoes",
             body=("The next task is about volcanoes. Read this short orientation. The task will ask you to "
                   "explain, so decide which mode that calls for and plan the matching thesis.")),
        Slot("TRANSFER", "production_frq", "Choose the mode and plan the thesis on a NEW topic",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=("New topic. Task: explain how volcanoes form and erupt. Name the mode the verb calls for, "
                   "then plan the matching THESIS plus a one-line note on the body. Same choose-the-mode move "
                   "as the photosynthesis task, new topic. Scored on Thesis/Purpose.")),
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
