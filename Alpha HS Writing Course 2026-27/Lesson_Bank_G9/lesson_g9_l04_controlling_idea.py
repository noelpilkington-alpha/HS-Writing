"""
lesson_g9_l04_controlling_idea.py  -  G9 KC C.9.05, ARCHETYPE T2: CLAIM-BUILDING (STAND, ceiling = sentence).

G9 course L04. The EXPOSITORY fork: a controlling idea (P2) vs an argument claim, plus decode-the-verb.
REVISED 2026-07-12 to the locked L01 template. Taught frame = FRAME-WATER-CYCLE; transfer frame =
FRAME-PHOTOSYNTHESIS (bank-partitioned). rc.staar, unit="sentence". Still T2 (claim at the sentence) but in
the informational mode: the product is a focusing controlling idea, no side. STAND labeled proposal; mechanics
gated; no coping-model persona; no source markup; no prior-work reference; no em dashes. Runs QC on execution.
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
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> a broad topic label, focuses nothing</span>'
    '<p style="margin:8px 0 0;font-size:15px">"The water cycle is important."</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">It names the topic but no angle, so a reader has '
    'no idea what the explanation will cover. "Important" also leans toward a side no one asked for.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> a controlling idea: clear focus, no side</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">FOCUS</span> The water cycle moves water through four connected stages, '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">PREVIEW</span> evaporation, condensation, precipitation, and collection, in one '
      'continuous loop.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">It sets a focus a reader can follow and previews '
    'the parts, and it takes no side. That is a controlling idea.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C905-0004", grade="9-10", lesson_type=2,
    unit="G9 U1 - Claim/controlling-idea + evidence (controlling idea)",
    title="Set a Focus, Not a Side (Explaining)",
    target=("Write one controlling idea for an explain task: a focusing angle that previews the parts and "
            "takes no side. Tell it apart from an argument claim. Written at the sentence. Trait: "
            "Thesis/Purpose (Central Idea)."),
    acc_tags=["ACC.W.INFO.1", "CCSS.W.9-10.2a"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-12",
                "mnemonic_status": "proposal", "kc": "C.9.05", "sot": "icm course-G9.md L04",
                "taught_stimulus": "ACC-W910-FRAME-WATER-CYCLE",
                "transfer_stimulus": "ACC-W910-FRAME-PHOTOSYNTHESIS",
                "playbook": "_phase2/playbook_T2_STAND.md",
                "revision_note": "Locked L01 template: student register, one teach concept, visual before/after, one discrimination, bound issue_frame (orientation, no side).",
                "council": "T2/STAND informational: introduces P2 controlling-idea + decode-the-verb; signature discrimination = controlling-idea vs argument-claim (explain vs argue)."},
    fade_ledger_moves=["decode-explain-vs-argue", "controlling-idea-vs-argument-claim"],
    slots=[
        Slot("TEACH", "teach_card", "Explain tasks want a controlling idea, not a side",
             body=("Not every task asks you to take a side. When a task says explain, describe, or inform, it "
                   "wants a controlling idea, not an argument. A controlling idea is when one sentence names "
                   "the focusing angle your writing will take on a topic, without taking a side a reader could "
                   "dispute. Compare the two: an arguable claim is a sentence that takes a side someone could "
                   "reject ('the water cycle is the most important process'); a controlling idea instead sets "
                   "a focus everyone can follow ('the water cycle moves water through four connected stages'). "
                   "The scoring may call this your thesis or central idea, which is a name for the controlling "
                   "idea your explanation develops. The trap on an explain task: either arguing a side no one "
                   "asked for, or writing a label so broad it focuses nothing ('the water cycle is "
                   "important'). Read the verb first, explain means no side, then set a clear focus and preview "
                   "the parts.")),
        Slot("TEACH", "stimulus_display", "The topic: the water cycle",
             ref="ACC-W910-FRAME-WATER-CYCLE", bank="water_cycle",
             body=("Read the short orientation to the topic, then write your controlling idea. You only need "
                   "the topic and its main parts. Remember, this is an explain task, so you take no side.")),
        Slot("TEACH", "discrimination", "Controlling idea or argument claim?",
             ref="", labeled_grade_c=True, bank="water_cycle",
             body=("Sort these before you write (spotting the target before producing it, a Grade-C design bet "
                   "we label as a bet, not a proven ingredient). The task is to EXPLAIN how the water cycle "
                   "works. Which sentence is a controlling idea (a focus, no side), not an argument claim? "
                   "(A) The water cycle is the most important natural process on the whole planet, more essential to life than any other system we study in science.  "
                   "(B) The water cycle is a really interesting topic to learn about, and it may be the most fascinating thing we have studied in science class all year.  "
                   "(C) The water cycle moves water through four connected stages, evaporation, condensation, "
                   "precipitation, and collection, in one continuous loop. "
                   "Correct: C. (A) takes an arguable SIDE (most important), which an explain task did not ask "
                   "for. (B) is a bare opinion. Only (C) sets a clear focus a reader can follow and takes no "
                   "side.")),
        Slot("MODEL", "annotated_before_after", "Watch a topic label become a controlling idea",
             bank="water_cycle",
             body=("Here is a broad topic label being rebuilt into a controlling idea. Read the BEFORE, then "
                   "the AFTER, and notice it now sets a focus and previews the parts, with no side."
                   + BEFORE_AFTER_HTML +
                   " The BEFORE focuses nothing. The AFTER names a followable angle and previews the stages. "
                   "Setting a focus, not a label and not an argument, is the move.")),
        Slot("MODEL", "predict_the_fix", "Is this a controlling idea, and if not, what fixes it?",
             bank="water_cycle",
             body=("Diagnose this draft before the reveal. The task is to EXPLAIN how the water cycle works. "
                   "The student wrote: 'The water cycle is the most important thing for life on Earth.' Which "
                   "single move would most improve it for this task? "
                   "(A) drop the arguable judgment and set a focus on how the cycle actually works, naming its "
                   "stages  "
                   "(B) add the supporting fact that Earth's oceans hold most of the water on the whole planet  "
                   "(C) cut the sentence down to only a handful of words so it is shorter and quicker to read  "
                   "(D) make the argument stronger by explaining why the water cycle beats every other natural "
                   "process"),
             feedback=("Correct: A. The draft takes an arguable side ('most important') on a task that asked "
                       "for an explanation, so it is off-task, and it names no focus for how the cycle works. "
                       "The fix is a controlling idea: drop the judgment and set a followable angle, for "
                       "example 'The water cycle moves water through four connected stages ...' A fact about "
                       "oceans (B) or a shorter sentence (C) do not set a focus; arguing a side (D) doubles "
                       "down on the off-task move.")),
        Slot("SUPPORTED", "production_frq", "Set the focus, preview the parts",
             ref="", bank="water_cycle", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("Finish this controlling idea for explaining the water cycle: 'The water cycle ______ [what "
                   "it does overall], through ______ [name the connected stages].' Goal: set a clear focus and "
                   "preview the parts, take NO side, and answer the explain task. Do not argue that the cycle "
                   "is important or best. Write one sentence. Scored on Thesis/Purpose (Central Idea).")),
        Slot("MODEL", "diagnosis_frq", "Check your controlling idea: focus set, no side?",
             ref="", bank="water_cycle", scored=True,
             body=("First watch the check run on a weak draft, then run it on a fresh controlling idea of your "
                   "own. Weak draft: 'The water cycle is a very important process.' Run the check step by step. "
                   "Step 1, focus: does it set a focusing angle on how the cycle works? No, 'important process' "
                   "names no angle, so name the stages or the loop. Step 2, no side: does it avoid an arguable "
                   "judgment? No, 'important' leans to a side, so cut it. Step 3, previews the parts? No, add "
                   "them. Now you: write one fresh controlling idea for the water cycle, then run the same "
                   "checks. For each No, use the fix: name the stages; cut the judgment; preview the parts. "
                   "Finish by naming which check your sentence still needs most.")),
        Slot("INDEPENDENT", "production_frq", "Write one controlling idea for the water cycle",
             ref="", bank="water_cycle", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("On your own now. The task: explain how the water cycle works. Write ONE controlling idea "
                   "sentence. Goal: set a clear focus, preview the stages, and take NO side. Before you submit, "
                   "check your sentence: does it set a focus a reader can follow, does it avoid arguing a side, "
                   "does it answer the explain task? If any answer is no, fix it before you submit. Scored on "
                   "Thesis/Purpose (Central Idea).")),
        Slot("TRANSFER", "stimulus_display", "The topic: photosynthesis",
             ref="ACC-W910-FRAME-PHOTOSYNTHESIS", bank="photosynthesis",
             body=("Read the short orientation to this new topic, then write your controlling idea. You only "
                   "need the topic and its main parts. Remember, this is an explain task, so you take no "
                   "side.")),
        Slot("TRANSFER", "production_frq", "Write a controlling idea on a NEW topic",
             ref="", bank="photosynthesis", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("New topic. The task: explain how photosynthesis turns light into food. Write ONE "
                   "controlling idea sentence. Goal: set a clear focus, name the connected steps, and take NO "
                   "side. Same move as the water-cycle idea, new topic. Do not argue that photosynthesis is "
                   "important or best. Scored on Thesis/Purpose (Central Idea).")),
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
