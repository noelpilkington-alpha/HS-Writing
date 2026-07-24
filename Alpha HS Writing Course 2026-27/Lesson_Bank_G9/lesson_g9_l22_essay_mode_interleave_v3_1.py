"""
lesson_g9_l22_essay_mode_interleave_v3_1.py  -  G9 KC C.9.01 + C.9.05, ARCHETYPE T7 (essay-mode review). V3.1.

G9 course L22 (Unit 4, review), rebuilt to the v3.1 build spec. Teaching point (KEPT): given an ESSAY task,
decide from the task verb whether the whole essay should ARGUE (a thesis that takes a side) or EXPLAIN (a
controlling idea, no side), then plan the matching thesis. This is the ESSAY-level version of L06 (which runs
the same argue-vs-explain fork at the SENTENCE level). Interleaves C.9.01 + C.9.05 at essay scale. Written as
an essay plan; unit stays multi_paragraph. Binds issue_frames for topic context (the decision is which MODE +
thesis to plan, not source-mining). Taught frames: FRAME-PHONEBAN (argue) + FRAME-PHOTOSYNTHESIS (explain);
transfer FRAME-VOLCANOES (explain, partitioned). rc.staar. T7 STAND-family review = mnemonic_status proposal.

V3.1 (Noel 2026-07-14): applies the L01/L06 v3.1 pattern to the current L22. Changes vs the prior L22:
  1. LIST-TEACH the one idea (fixes the 172-word wall-of-text teach body): both gated products are now parallel
     <li> items, each defined with a cue word (arguable claim/thesis "is a"/"is called", controlling idea
     "means"), so define_before_use + format_fidelity both clear.
  2. DE-LEAK the discrimination (fixes the live 'Grade-C design bet, labeled as a bet' leak): the rationale
     lives in provenance/comments; the student prompt just says sort-the-mode-first.
  3. Discrimination now carries an explicit choices=[{id,text,correct,why}] set (reliable per-choice feedback);
     correct option is NOT the lone longest (Haladyna homogeneous-length rule).
  4. FRQ/diagnosis bodies use frq_prompt/setapart/checklist (no 'Step 1/2' prose, no 'Scored on ...' chrome).
  5. Added a decompose MODEL card (argue->thesis vs explain->controlling idea, essay scale) + the reusable verb
     check tool at point of first use, and autonomy + say-the-standard on the independent write (Yeager).
Passes all 23 lesson_contract gates. Own words, no fabricated figures, no em dashes, inline HTML.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">The task <strong>verb</strong> decides the whole '
'essay\'s <strong>mode</strong>. <strong>Argue</strong> wants an essay whose thesis takes a side; '
'<strong>explain</strong> wants an essay whose thesis is a focus with no side.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: read the verb first</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you plan the essay, ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">What is the verb, argue or explain?</li>'
'<li style="margin:2px 0">If argue: does the thesis take a side someone could reject, with a reason?</li>'
'<li style="margin:2px 0">If explain: is the thesis a focus that previews the parts and takes no side?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">Match the mode to the verb, or the whole essay answers the wrong task.</div></div>')

# MODEL worked example: an essay thesis in the WRONG mode for the verb, switched to the right one. Literal
# BEFORE + AFTER (content_depth). No named near-peer (Timeback stateless rule).
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

# Decompose: the two verbs, two essay modes, side by side (essay scale).
DECOMPOSE_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#eef2ff;padding:10px 14px;border-bottom:1px solid #c7d2fe;font-size:14px;color:#1f2a44">'
    'Same two verbs, two essay modes:</div>'
  '<div style="padding:12px 14px">'
    '<div style="margin:0 0 10px">'
      '<span style="display:inline-block;background:#fee2e2;color:#991b1b;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">ARGUE -&gt; ARGUMENT ESSAY</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px"><em>"Schools should ban phones all day, because '
      'constant access pulls attention away from learning."</em> The thesis takes a <strong>side</strong> '
      'someone could reject and gives a <strong>reason</strong>; every body paragraph defends it.</div></div>'
    '<div>'
      '<span style="display:inline-block;background:#dcfce7;color:#166534;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">EXPLAIN -&gt; INFORMATIONAL ESSAY</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px"><em>"Photosynthesis turns sunlight, water, and '
      'carbon dioxide into sugar and oxygen through steps in a plant\'s leaves."</em> The thesis is a focus that '
      'previews the <strong>parts</strong> and takes <strong>no side</strong>; the body walks through them.</div></div>'
    '<div style="margin-top:10px;color:#0f766e;font-size:13px">The verb decides which mode you plan.</div>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C901-0022", grade="9-10", lesson_type=7,
    unit="G9 U5 - Build essay (argue vs explain essay-mode interleave)",
    title="Argue or Explain? Choose the Essay Mode",
    target=("Given an essay task, decide from the verb whether the whole essay should ARGUE (a thesis that "
            "takes a side) or EXPLAIN (a controlling idea, no side), then plan the matching thesis. Written as "
            "an essay plan. Trait: Thesis/Purpose."),
    acc_tags=["ACC.W.ARG.1", "ACC.W.INFO.1", "CCSS.W.9-10.1a", "CCSS.W.9-10.2a"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-14",
                "mnemonic_status": "proposal", "kc": "C.9.01+C.9.05", "sot": "icm course-G9.md L22",
                "taught_stimulus": "ACC-W910-FRAME-PHONEBAN",
                "taught_stimulus_2": "ACC-W910-FRAME-PHOTOSYNTHESIS",
                "transfer_stimulus": "ACC-W910-FRAME-VOLCANOES",
                "playbook": "_phase2/playbook_T2_STAND.md",
                "one_idea": "The task verb decides the essay mode: argue -> a thesis that takes a side; explain -> a controlling idea, no side.",
                "one_reminder": "Read the verb first; plan the mode + thesis that match it.",
                "template": "locked L01 template; review interleave binds issue_frames (decision is mode+thesis, not source-mining).",
                "council": ("T2/STAND essay-mode review (spacing/retrieval at essay scale): the discrimination "
                            "is which MODE the essay task calls for (argue vs explain), keyed off the verb, "
                            "recycling the P1/P2 fork. right-mode-vs-wrong-mode discrimination labeled Grade-C."),
                "version_note": ("V3.1 rebuild of lesson_g9_l22_essay_mode_interleave.py. Fixed the two prior "
                                 "failures (leaked 'Grade-C design bet' in the discrimination prompt; 172-word "
                                 "wall-of-text teach body) and applied the L01/L06 v3.1 pattern: list-teach with "
                                 "cue-defined terms, choices-list discrimination (correct not lone-longest), "
                                 "frq_prompt/checklist/setapart bodies, decompose + reusable verb check, autonomy "
                                 "+ say-the-standard independent write. Teaching point + all Lesson field values "
                                 "preserved (id, lesson_type=7, unit=multi_paragraph, bound stimuli)."),
                "review_provenance": "built to the L01/L06 v3.1 pattern (Fable+Council adjudicated 2026-07-14)"},
    fade_ledger_moves=["choose-essay-mode-argue-vs-explain", "plan-the-matching-thesis"],
    slots=[
        # ===== TEACH: ONE idea, list-taught; both gated products defined with a cue word =====
        Slot("TEACH", "teach_card", "The one idea: the verb decides the whole essay's mode",
             body=(ONE_IDEA +
                   "You already made this choice at the sentence. Now you make it for a WHOLE essay, and the "
                   "task verb still decides it:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\">An <strong>arguable claim</strong> is a sentence that takes a "
                   "side someone could disagree with and gives a reason. When a whole essay is built on one, "
                   "that guiding claim is called its <strong>thesis</strong>, and every body paragraph defends "
                   "it. Plan an ARGUMENT essay when the verb is 'argue', 'persuade', or 'should ... ?'.</li>"
                   "<li style=\"margin:4px 0\">A <strong>controlling idea</strong> means a sentence that sets a "
                   "focus and previews the parts while taking no side. Plan an INFORMATIONAL essay when the verb "
                   "is 'explain', 'describe', or 'inform', and the body walks through the parts.</li></ul>"
                   "The costly mistake at essay scale is planning the wrong mode: building a whole argument on an "
                   "explain task, or a neutral explanation on an argue task. So read the verb first, then plan "
                   "the matching thesis.")),
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

        # ===== MODEL: sort the mode, watch it get fixed, decompose + get the check tool, predict the fix =====
        Slot("MODEL", "discrimination", "Which thesis matches the essay's verb?",
             ref="", labeled_grade_c=True, bank="photosynthesis",
             body=("Sort the mode before you plan. The task: EXPLAIN how photosynthesis works. Which planned "
                   "thesis matches that verb? "
                   "(A) Photosynthesis is easily the most important natural process on Earth, and it deserves far more study than any other topic in science.  "
                   "(B) Photosynthesis is honestly one of the most amazing and fascinating things that green plants are able to do.  "
                   "(C) Photosynthesis turns sunlight, water, and carbon dioxide into sugar and oxygen through steps in a plant's leaves.  "
                   "(D) This essay will be about photosynthesis and the many different things that green plants manage to do. "
                   "Correct: C. The verb is explain, so the right mode is informational: a thesis that sets a "
                   "focus and takes no side. (A) argues a side (most important, deserves study), an argument "
                   "mode, wrong for an explain task. (B) is a bare opinion with no focus. (D) only announces the "
                   "topic; it sets no focus and previews no parts, so a reader cannot tell what the essay will "
                   "explain. Only (C) sets a no-side focus that previews the parts."),
             choices=[
                 {"id": "A", "text": "Photosynthesis is easily the most important natural process on Earth, and it deserves far more study than any other topic in science.",
                  "correct": False,
                  "why": "This argues a side (most important, deserves study). That is an argument mode, the wrong mode for an explain task."},
                 {"id": "B", "text": "Photosynthesis is honestly one of the most amazing and fascinating things that green plants are able to do.",
                  "correct": False,
                  "why": "This is a bare opinion. It sets no focus and previews no parts, so it does not fit an explain essay either."},
                 {"id": "C", "text": "Photosynthesis turns sunlight, water, and carbon dioxide into sugar and oxygen through steps in a plant's leaves.",
                  "correct": True,
                  "why": "Correct. The verb is explain, so the thesis should be a controlling idea: a focus that previews the parts and takes no side. This one does."},
                 {"id": "D", "text": "This essay will be about photosynthesis and the many different things that green plants manage to do.",
                  "correct": False,
                  "why": "This only announces the topic. It sets no focus and previews none of the parts, so a reader cannot tell what the explain essay will actually cover."},
             ]),
        Slot("MODEL", "annotated_before_after", "Watch the essay mode get matched to the verb",
             bank="photosynthesis",
             body=("Here is an essay thesis in the wrong mode being switched to match the verb. Read the "
                   "BEFORE, then the AFTER, and notice the arguing thesis become a focusing one for an explain "
                   "task." + BEFORE_AFTER_HTML +
                   " The BEFORE argues a side on an explain task. The AFTER sets a focus with no side. Choosing "
                   "the mode the verb calls for is the move.")),
        Slot("MODEL", "teach_card", "Decompose it, and get your check tool",
             body=("See the two essay modes side by side so you can tell which verb each one answers, then keep "
                   "the tool you will use to check your own plan." + DECOMPOSE_HTML + REMEMBER +
                   "When you plan, always read the verb first, then plan the matching mode and thesis.")),
        Slot("MODEL", "predict_the_fix", "What does this essay plan most need?",
             bank="phone_ban",
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

        # ===== SUPPORTED: framed write (name the mode + plan the thesis) on the explain task =====
        Slot("SUPPORTED", "production_frq", "Name the mode and plan the thesis",
             ref="", bank="photosynthesis", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="The task: EXPLAIN how photosynthesis turns light into food. The verb is explain, so "
                       "plan an informational essay: a thesis that is a controlling idea, a focus with no side.",
                 setapart_block=setapart(
                     "Copy this frame, then fill in the blanks:",
                     "Mode: ______ [argument or informational]. Thesis: Photosynthesis ______ [set a focus that "
                     "previews the inputs and outputs, no side]."),
                 closer="Name the mode the verb calls for, then write the matching thesis sentence. Do not write "
                        "an argument thesis for an explain task. Then run the verb check.")),
        # DIAGNOSIS = check-and-fix on a PROVIDED plan (not a fresh production). Stays on the taught topic (no new
        # source to read). Scaffolded with a checklist + a set-apart weak plan (model_before_required).
        # COUNCIL FIX (2026-07-24): Option A (later-in-arc). Was a bundle: pre-answered check + rewrite + name.
        # Now ONE graded act (the thesis rewrite); checks print READ-ONLY beneath; the mode context moves into
        # the intro (it is given context, not a check to mark); "name which check" dropped.
        Slot("MODEL", "diagnosis_frq", "Fix a plan's thesis to match the verb", ref="", bank="photosynthesis",
             scored=True, unit="sentence", frq_type="writing", rubric_ref="rc.staar",
             body=frq_prompt(
                 intro="The verb here calls for EXPLAIN, so this plan needs an informational thesis: a focusing "
                       "thesis with no side. Rewrite the weak thesis into the right mode.",
                 setapart_block=setapart("Weak plan thesis to fix:",
                                         "Plants are amazing and we should protect them.", "red"),
                 checklist_block=checklist(title="Make your new thesis pass these (no need to type answers):",
                                           rows=["Does the thesis match the explain mode (no side)?",
                                                 "Does it set a focus that previews the parts?"]),
                 closer="Write one controlling idea that fits an explain essay: a focusing thesis, no side, that "
                        "previews the parts. Run the checks above before you submit.")),

        # ===== INDEPENDENT: no frame; autonomy + say-the-standard (Yeager). Explain task, photosynthesis. =====
        Slot("INDEPENDENT", "production_frq", "Choose the mode and plan the thesis (photosynthesis)",
             ref="", bank="photosynthesis", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now, no frame. Task: explain how photosynthesis turns light into food.",
                 closer="Name the mode the verb calls for, then write the one thesis sentence that mode calls "
                        "for. Choosing the essay mode from the verb is exactly what every real writing task asks "
                        "for, and you are ready to do it cold. Before you submit, check that the mode matches the "
                        "verb and the thesis fits that mode (focusing, no side).")),

        # ===== TRANSFER: same move, a NEW topic (volcanoes), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "The topic: volcanoes",
             ref="ACC-W910-FRAME-VOLCANOES", bank="volcanoes",
             body=("The next task is about volcanoes. Read this short orientation. The task will ask you to "
                   "explain, so decide which mode that calls for and plan the matching thesis.")),
        Slot("TRANSFER", "production_frq", "Choose the mode and plan the thesis on a NEW topic",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="New topic. Task: explain how volcanoes form and erupt.",
                 closer="Name the mode the verb calls for, then write the one thesis sentence that mode calls "
                        "for. Same choose-the-mode move as the photosynthesis task, new topic. Run the verb "
                        "check before you submit, and do not slip into taking a side.")),
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
