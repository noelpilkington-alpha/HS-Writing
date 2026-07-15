"""
lesson_g9_l04_controlling_idea_v3_1.py  -  G9 KC C.9.05, ARCHETYPE T2 (STAND, sentence). V3.1.

G9 L04, rebuilt to the v3.1 build spec (icm/_config/v3_1-lesson-build-spec.md). Teaching point PRESERVED
(distinct from L01/L02): this is an INFORMATIONAL / EXPLAIN lesson (KC C.9.05), NOT argument. It teaches
writing a CONTROLLING IDEA for an explain task, a focusing angle that previews the parts and takes NO side,
and telling it apart from an argument claim. Because it is an EXPLAIN lesson it correctly uses SCIENCE-EXPLAIN
topics, NOT the argument debate slate: taught = water cycle (ACC-W910-FRAME-WATER-CYCLE, bank "water_cycle");
transfer = photosynthesis (ACC-W910-FRAME-PHOTOSYNTHESIS, bank "photosynthesis"), bank-partitioned.

Spine: one idea + list-formatted teach (FACT / argument claim / controlling idea) -> source -> coping-model
think-aloud (attempt -> check -> catch the label -> revise to a focus that previews the parts, no side) ->
decompose + check tool at point of first use -> discrimination AFTER the model (Grade-C labeled in code, no
leaked labels; the "names the parts" surface token is broken by a distractor that names the parts yet takes a
side) -> predict-the-fix (reveal in feedback) -> framed write -> diagnosis -> independent (autonomy of angle +
say the standard) -> transfer (partitioned). Tooltip demotes the non-operational scoring aside ("thesis").
All authored HTML inline-styled with real lists. 23 gates. Own words, no fabricated figures, no em dashes.

ONE IDEA: a controlling idea sets a FOCUS and previews the PARTS, and takes NO side.
ONE REMINDER: the 3-question check (focus? previews parts? no side?).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A controlling idea sets a <strong>FOCUS</strong> and '
'previews the <strong>PARTS</strong>, and it takes <strong>NO side</strong>. A broad label or an argument is '
'not a controlling idea.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit any controlling idea, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does it set a focus a reader can follow (an angle, not a broad label)?</li>'
'<li style="margin:2px 0">Does it preview the parts?</li>'
'<li style="margin:2px 0">Does it take no side (no arguable judgment)?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, it is not a controlling idea yet.</div></div>')

# coping-model think-aloud panel: a WRITTEN drafting process (attempt -> test -> revise), then the endpoints.
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer thinking it through, draft by draft (the task: explain how the water cycle works):</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "The water cycle is important." '
    'Check it: does it set a focus a reader can follow? No, it names no angle, and "important" even leans '
    'toward a side no one asked for. Start over.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "The water cycle moves water around the planet." '
    'Better, that sets a focus and takes no side. Does it preview the parts? Not yet. Add the stages.</p>'
    '<p style="margin:0"><strong>Final:</strong> "The water cycle moves water through four connected stages, '
    'evaporation, condensation, precipitation, and collection, in one continuous loop." A focus, the parts '
    'previewed, and no side.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "The water cycle is important." (a broad label, focuses nothing)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "The water cycle moves water through four connected stages, '
    'evaporation, condensation, precipitation, and collection, in one continuous loop." (a controlling idea)</span></div>'
'</div>')

DECOMPOSE_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#f0fdf4;padding:10px 14px;border-bottom:1px solid #bbf7d0;font-size:15px">'
    'The finished controlling idea: <em>"The water cycle moves water through four connected stages, evaporation, '
    'condensation, precipitation, and collection, in one continuous loop."</em></div>'
  '<div style="padding:12px 14px">'
    '<div style="margin:0 0 10px">'
      '<span style="display:inline-block;background:#dbeafe;color:#1e3a8a;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">MOVE 1 - FOCUS</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px"><strong>"The water cycle moves water through four '
      'connected stages"</strong> sets a clear angle a reader can follow, not a broad label like "important."</div></div>'
    '<div style="margin:0 0 10px">'
      '<span style="display:inline-block;background:#fef9c3;color:#854d0e;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">MOVE 2 - PREVIEW</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px">"...<strong>evaporation, condensation, '
      'precipitation, and collection, in one continuous loop</strong>." names the parts the explanation will cover.</div></div>'
    '<div>'
      '<span style="display:inline-block;background:#e0e7ff;color:#3730a3;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">TAKES NO SIDE</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px">Notice there is no "important" or "best." It '
      'reports the focus and the parts without any judgment a reader could dispute.</div></div>'
    '<div style="margin-top:10px;color:#0f766e;font-size:13px">Set a focus, preview the parts, take no side. '
    'That is the whole construction.</div>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C905-0004", grade="9-10", lesson_type=2,
    unit="G9 U1 - Claim/controlling-idea + evidence (controlling idea)",
    title="Set a Focus, Not a Side (Explaining)",
    target=("Write one controlling idea that answers the EXACT explain task: a focusing angle that previews the "
            "parts, takes no side, and matches the specific task asked (not just the topic). Tell it apart from "
            "an argument claim. Written at the sentence. Trait: Thesis/Purpose (Central Idea)."),
    acc_tags=["ACC.W.INFO.1", "CCSS.W.9-10.2a"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-14",
                "mnemonic_status": "proposal", "kc": "C.9.05",
                "sot": "icm course-G9.md L04; KC_Map_and_Unit_Arch_G9-12.md (G9 U1)",
                "taught_stimulus": "ACC-W910-FRAME-WATER-CYCLE",
                "transfer_stimulus": "ACC-W910-FRAME-PHOTOSYNTHESIS",
                "one_idea": "A controlling idea answers the EXACT task with a FOCUS that previews the PARTS, and takes NO side.",
                "one_reminder": "3-question check: focus (answers the exact task)? previews parts? no side?",
                "merged_from": "L05 (write-a-controlling-idea-that-answers-the-task) folded in 2026-07-14 per design audit; L05 removed",
                "version_note": ("V3.1 rebuild per icm/_config/v3_1-lesson-build-spec.md, adapted to the EXPLAIN "
                                 "skill (not argument): spine + list-formatted teach (fact / argument claim / "
                                 "controlling idea) + coping-model think-aloud + decompose + check-tool-at-point-"
                                 "of-use + thesis tooltip. Kept the science-explain topics (water cycle taught, "
                                 "photosynthesis transfer, bank-partitioned) because this is an informational, "
                                 "no-side task. Discrimination confound broken: a distractor names the parts yet "
                                 "takes a side, so 'previews the parts' does not co-vary with the correct answer; "
                                 "no-side is the invariant. Removed the leaked 'Grade-C design bet' label and the "
                                 "wall-of-text teach body that failed v1."),
                "review_provenance": "built to the L01/L02 v3.1 pattern (Fable+Council adjudicated 2026-07-14)"},
    fade_ledger_moves=["decode-explain-vs-argue", "controlling-idea-vs-argument-claim", "focus-plus-preview"],
    slots=[
        # ===== TEACH: ONE idea only, list-formatted; verb habit trimmed; thesis demoted to a tooltip =====
        Slot("TEACH", "teach_card", "The one idea: set a FOCUS, preview the PARTS, take NO side",
             body=(ONE_IDEA +
                   "Not every task asks you to pick a side. When a task says explain, describe, or inform, it "
                   "wants a controlling idea, not an argument. Three kinds of sentence look alike but do "
                   "different jobs, so keep them apart:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>FACT</strong>: something you can check and nobody argues "
                   "about ('The water cycle has several stages').</li>"
                   "<li style=\"margin:4px 0\"><strong>Argument claim</strong>: a sentence that takes a side "
                   "someone could dispute ('The water cycle is the most important process on Earth').</li>"
                   "<li style=\"margin:4px 0\"><strong>Controlling idea</strong>: this is a sentence that sets "
                   "the focusing angle your explanation will take and previews its parts, without taking any "
                   "side ('The water cycle moves water through four connected stages, evaporation, condensation, "
                   "precipitation, and collection').</li></ul>"
                   "That last one is the sentence an explanation is built on. (Scoring may call it your "
                   "<dfn class=\"tb-glossary-term\" data-catalog-idref=\"def-thesis\" "
                   "title=\"Thesis means the single controlling idea your whole explanation develops. You do not "
                   "need this word to finish today's task.\">thesis</dfn> or central idea, but you do not need "
                   "that word for today's task.) One habit first: read the verb. 'Explain' or 'describe' wants "
                   "no side; 'argue' or 'should ... ?' wants a side. Today's task asks you to explain.")),
        Slot("TEACH", "stimulus_display", "The topic: the water cycle",
             ref="ACC-W910-FRAME-WATER-CYCLE", bank="water_cycle",
             body=("Read the short orientation to the topic. In a moment you will watch a controlling idea get "
                   "built, then build your own. You only need the topic and its main parts. Remember, this is an "
                   "explain task, so you take no side.")),

        # ===== MODEL first (before the quiz): coping-model think-aloud -> decompose + the check tool ===
        Slot("MODEL", "annotated_before_after", "Watch a writer build a controlling idea",
             bank="water_cycle",
             body=("Here is the skill in action. Follow the writer's thinking below. " + COPING_HTML +
                   " Notice what turned the BEFORE into the AFTER: the writer dropped the broad label, set a "
                   "focus a reader can follow, previewed the parts, and took no side.")),
        Slot("MODEL", "teach_card", "Decompose it, and get your check tool",
             body=("Now take the finished controlling idea apart to see how it is built, then keep the tool you "
                   "will use to check your own." + DECOMPOSE_HTML + REMEMBER +
                   "When you write your own, do the same: set the focus first, preview the parts, keep any side "
                   "out, then run the 3 questions before you submit.")),
        Slot("MODEL", "discrimination", "Which one is the controlling idea?",
             ref="", labeled_grade_c=True, bank="water_cycle",
             body=("Now that you have seen one built, spot the target. The task is to EXPLAIN how the water cycle "
                   "works. Which sentence is a controlling idea (a focus, previews the parts, no side), not an "
                   "argument claim? "
                   "(A) The water cycle is the single most important natural process on the entire planet, more "
                   "essential to life than any other system we ever get to study in science class all year.  "
                   "(B) The water cycle moves through evaporation, condensation, and precipitation, which clearly "
                   "proves it matters far more than any other natural cycle a student could possibly study.  "
                   "(C) The water cycle moves water through four connected stages, evaporation, condensation, "
                   "precipitation, and collection, in one continuous loop. "
                   "Correct: C. Watch the trap: (A) takes an arguable SIDE ('most important'), which an explain "
                   "task did not ask for. (B) does name the parts, but it still argues a side ('matters far "
                   "more'), so previewing the parts alone does not make a controlling idea. Only (C) sets a focus "
                   "a reader can follow, previews the parts, AND takes no side. It is the no-side focus that "
                   "makes it a controlling idea, not simply listing the stages.")),
        Slot("MODEL", "discrimination", "Which one previews the parts, not just a true fact?",
             ref="", labeled_grade_c=True, bank="water_cycle",
             body=("A different test now: every choice below takes no side, so no-side will not decide it. The "
                   "task is to explain how the water cycle keeps water moving. Which one is a controlling idea: "
                   "it sets a focus and previews the stages?"),
             choices=[
                 {"id": "A",
                  "text": ("Water is found nearly everywhere on the planet, in the oceans, high in the air, deep "
                           "underground, and even locked away frozen inside the polar ice caps."),
                  "correct": False,
                  "why": ("This states a true fact about where water sits, but it sets no focus on how the cycle "
                          "works and previews none of its stages.")},
                 {"id": "B",
                  "text": "The water cycle keeps the planet's water moving all the time.",
                  "correct": False,
                  "why": ("This sets a focus and takes no side, but it never names the stages, so a reader cannot "
                          "tell what parts the explanation will cover.")},
                 {"id": "C",
                  "text": ("The water cycle keeps water moving as it warms into vapor, cools into clouds, and "
                           "falls back to the ground."),
                  "correct": True,
                  "why": ("This sets a clear focus on how the cycle keeps water moving and previews its stages, "
                          "all while taking no side, so it is a controlling idea.")},
             ]),
        Slot("MODEL", "predict_the_fix", "Is this a controlling idea, and if not, what fixes it?",
             bank="water_cycle",
             body=("Diagnose this draft before the reveal. The task is to EXPLAIN how the water cycle works. The "
                   "student wrote: 'The water cycle is the most important thing for life on Earth.' Which single "
                   "move would most improve it for this task? "
                   "(A) drop the arguable judgment and set a focus on how the cycle actually works, naming its stages  "
                   "(B) add the supporting fact that Earth's oceans hold most of the water on the whole planet  "
                   "(C) cut the sentence down to only a handful of words so it is shorter and quicker to read  "
                   "(D) make the argument stronger by explaining why the water cycle beats every other natural process"),
             feedback=("Correct: A. The draft takes an arguable side ('most important') on a task that asked for "
                       "an explanation, so it is off-task, and it names no focus for how the cycle works. The fix "
                       "is a controlling idea: drop the judgment and set a followable angle that previews the "
                       "parts, for example 'The water cycle moves water through four connected stages ...' A fact "
                       "about oceans (B) or a shorter sentence (C) do not set a focus; arguing a side (D) doubles "
                       "down on the off-task move.")),

        # ===== SUPPORTED: framed write (fill-in frame) =====
        Slot("SUPPORTED", "production_frq", "Finish the controlling idea: set the focus, preview the parts",
             ref="", bank="water_cycle", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on the two moves.",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "The water cycle ______ [what it does overall], through ______ [name the connected stages]."),
                 closer="Set a clear focus and preview the parts, take NO side. Do not argue that the cycle is "
                        "important or best. Then check it against the 3 questions.")),
        Slot("MODEL", "diagnosis_frq", "Check your controlling idea: focus set, parts previewed, no side?",
             ref="", bank="water_cycle", scored=True,
             body=frq_prompt(
                 intro="Run the 3-question check on this weak draft, then rewrite it into a real controlling idea.",
                 setapart_block=setapart("Weak draft to fix:", "The water cycle is a very important process.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Does it set a focus (an angle on how the cycle works)?",
                      "No, 'important process' names no angle. Name the stages or the loop."),
                     ("Does it preview the parts?", "No. Add the connected stages."),
                     ("Does it take no side?", "No, 'important' leans to a side. Cut the judgment."),
                 ]),
                 closer="Now rewrite the weak draft into one controlling idea that passes all three. "
                        "Then name which question your rewrite fixed.")),

        # ===== INDEPENDENT: autonomy (own angle) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write one controlling idea for the water cycle",
             ref="", bank="water_cycle", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="On your own now, no frame. Read the EXACT task and answer it, not just the topic. The "
                       "task: explain how the water cycle RECYCLES the same water again and again.",
                 closer="Notice the task is narrower than the whole topic: it asks about recycling the same "
                        "water. Write ONE controlling idea that answers THAT exact task: set a focus on the "
                        "recycling, preview the stages that make it a loop, take NO side. Answering the exact "
                        "task (not just naming the topic) is the move every strong explanation is built on. "
                        "Check your sentence against the 3 questions before you submit.")),

        # ===== TRANSFER: same move, new topic, partitioned bank =====
        Slot("TRANSFER", "stimulus_display", "The topic: photosynthesis",
             ref="ACC-W910-FRAME-PHOTOSYNTHESIS", bank="photosynthesis",
             body=("A new topic. Read the short orientation, then write your controlling idea. Same move as "
                   "before, new topic. You only need the topic and its main parts. Remember, this is an explain "
                   "task, so you take no side.")),
        Slot("TRANSFER", "production_frq", "Write a controlling idea on a NEW topic",
             ref="", bank="photosynthesis", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="New topic, and again answer the EXACT task, not the whole topic. The task: explain what "
                       "photosynthesis MAKES and RELEASES.",
                 closer="The task asks specifically about the outputs (what the plant makes and releases), not "
                        "everything about photosynthesis. Write ONE controlling idea that answers THAT exact "
                        "task: set a focus on the outputs, name them, and take NO side. Do not argue that "
                        "photosynthesis is important or best. Check it against the 3 questions before you submit.")),
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
