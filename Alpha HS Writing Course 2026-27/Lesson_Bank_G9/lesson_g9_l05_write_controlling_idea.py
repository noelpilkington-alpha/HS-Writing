"""
lesson_g9_l05_write_controlling_idea.py  -  G9 KC C.9.05, ARCHETYPE T2: CLAIM-BUILDING (STAND, ceiling=sentence).

G9 course L05. Guided practice writing an informational controlling idea that answers the specific explain
task (recycles P2, deepens prompt-responsive in the informational mode). REVISED 2026-07-12 to the locked L01
template. Taught frame = FRAME-PHOTOSYNTHESIS; transfer frame = FRAME-VOLCANOES (bank-partitioned). rc.staar,
unit="sentence". STAND labeled proposal; mechanics gated; no coping-model persona; no source markup; no
prior-work reference; no em dashes. Runs QC on execution.
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
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> names the topic, answers nothing</span>'
    '<p style="margin:8px 0 0;font-size:15px">"Photosynthesis is a process that plants do."</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The task asks HOW plants turn light into food. '
    'This previews none of that, so a reader gets no roadmap for the explanation.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> answers the question, previews the parts</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">FOCUS</span> Photosynthesis turns sunlight, water, and carbon dioxide '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">PREVIEW</span> into sugar and oxygen through steps in a plant\'s leaves.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">It answers how light becomes food and previews '
    'the inputs and outputs. That is the roadmap a reader needs.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C905-0005", grade="9-10", lesson_type=2,
    unit="G9 U1 - Claim/controlling-idea + evidence (write a controlling idea)",
    title="Write a Controlling Idea That Answers the Task",
    target=("Write one controlling idea that answers the specific explain task: a focus that previews the "
            "parts and takes no side. Written at the sentence. Trait: Thesis/Purpose (Central Idea)."),
    acc_tags=["ACC.W.INFO.1", "CCSS.W.9-10.2a"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-12",
                "mnemonic_status": "proposal", "kc": "C.9.05", "sot": "icm course-G9.md L05",
                "taught_stimulus": "ACC-W910-FRAME-PHOTOSYNTHESIS",
                "transfer_stimulus": "ACC-W910-FRAME-VOLCANOES",
                "playbook": "_phase2/playbook_T2_STAND.md",
                "revision_note": "Locked L01 template: student register, one teach concept, visual before/after, one discrimination, bound issue_frame (orientation).",
                "council": "T2/STAND informational guided rung: recycles controlling-idea, deepens responsive (answers THIS explain task; previews the parts)."},
    fade_ledger_moves=["controlling-idea-answers-the-task", "preview-the-parts"],
    slots=[
        Slot("TEACH", "teach_card", "A controlling idea that answers the exact task",
             body=("You already know a controlling idea: one sentence that names the focusing angle your "
                   "writing takes on a topic, with no side. Today's focus is making it answer the SPECIFIC "
                   "task, not the general topic. An explain task asks a particular question, 'explain how "
                   "photosynthesis turns light into food,' and a strong controlling idea previews exactly that, "
                   "the inputs and outputs, not a loose fact about plants. The scoring calls this your thesis "
                   "or central idea, which is a name for the controlling idea your explanation develops. The "
                   "trap: naming the topic ('photosynthesis is a process in plants') without previewing what "
                   "the explanation will actually walk through, so the reader gets no roadmap. Today you will "
                   "write one controlling idea that answers the exact task and previews the parts.")),
        Slot("TEACH", "stimulus_display", "The topic: photosynthesis",
             ref="ACC-W910-FRAME-PHOTOSYNTHESIS", bank="photosynthesis",
             body=("Read the short orientation to the topic, then write your controlling idea. You only need "
                   "the topic and its main parts. This is an explain task, so you take no side.")),
        Slot("TEACH", "discrimination", "Which controlling idea answers the task?",
             ref="", labeled_grade_c=True, bank="photosynthesis",
             body=("Sort these before you write (spotting the target before producing it, a Grade-C design bet "
                   "we label as a bet, not a proven ingredient). The task is to EXPLAIN how photosynthesis "
                   "turns light into food. Which sentence answers the exact task and previews the parts? "
                   "(A) Photosynthesis is something that happens in plants, and it is a process that takes place in "
                   "almost all green plants on Earth.  "
                   "(B) Plants are amazing living things, and they are some of the most beautiful and incredible "
                   "organisms in all of nature.  "
                   "(C) Photosynthesis turns sunlight, water, and carbon dioxide into sugar and oxygen through "
                   "steps in a plant's leaves. "
                   "Correct: C. (A) names the topic but answers nothing specific and previews no parts. (B) is "
                   "a bare opinion off the task. Only (C) answers how light becomes food and previews the "
                   "inputs and outputs.")),
        Slot("MODEL", "annotated_before_after", "Watch a topic label become a controlling idea that answers the task",
             bank="photosynthesis",
             body=("Here is a topic label being rebuilt into a controlling idea. Read the BEFORE, then the "
                   "AFTER, and notice it now answers the exact task and previews the parts." + BEFORE_AFTER_HTML +
                   " The BEFORE gives no roadmap. The AFTER answers how light becomes food and previews the "
                   "inputs and outputs. Answering the task and previewing the parts is the move.")),
        Slot("MODEL", "predict_the_fix", "Does this answer the task, and if not, what fixes it?",
             bank="photosynthesis",
             body=("Diagnose this draft before the reveal. The task is to EXPLAIN how photosynthesis turns "
                   "light into food. The student wrote: 'Photosynthesis is very important for plants and for "
                   "us.' Which single move would most improve it for this task? "
                   "(A) answer the exact question, how light becomes food, and preview the inputs and outputs  "
                   "(B) add the extra fact that green plants are found all over the world in almost every habitat  "
                   "(C) make the sentence sound more formal by swapping in longer, more academic-sounding words  "
                   "(D) argue that photosynthesis is the single most important natural process on the whole planet"),
             feedback=("Correct: A. The draft says why photosynthesis matters but never answers the task, HOW "
                       "light becomes food, and previews no parts. The fix is a controlling idea that answers "
                       "the exact task and names the inputs and outputs, for example 'Photosynthesis turns "
                       "sunlight, water, and carbon dioxide into sugar and oxygen ...' A fact about where "
                       "plants grow (B) or a formal tone (C) do not answer the task; arguing importance (D) "
                       "takes a side the explain task did not ask for.")),
        Slot("SUPPORTED", "production_frq", "Answer the task, preview the parts",
             ref="", bank="photosynthesis", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("Finish this controlling idea for explaining photosynthesis: 'Photosynthesis ______ [what "
                   "it does] by turning ______ [inputs] into ______ [outputs] ______ [where or how].' Goal: "
                   "answer the exact task (how light becomes food), preview the parts, and take NO side. Do "
                   "not just name the topic. Write one sentence. Scored on Thesis/Purpose (Central Idea).")),
        Slot("MODEL", "diagnosis_frq", "Check your controlling idea: answers the task, previews the parts?",
             ref="", bank="photosynthesis", scored=True,
             body=("First watch the check run on a weak draft, then run it on a fresh controlling idea of your "
                   "own. Weak draft: 'Photosynthesis is a natural process in plants.' Run the check step by "
                   "step. Step 1, task: does it answer the exact question, how light becomes food? No, it "
                   "names the topic, so state the conversion. Step 2, preview: does it preview the inputs and "
                   "outputs? No, add them. Step 3, no side: does it avoid an arguable judgment? Yes. Now you: "
                   "write one fresh controlling idea for photosynthesis, then run the same checks. For each "
                   "No, use the fix: state how light becomes food; list the inputs and outputs. Finish by "
                   "naming which check your sentence still needs most.")),
        Slot("INDEPENDENT", "production_frq", "Write one controlling idea for photosynthesis",
             ref="", bank="photosynthesis", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("On your own now. The task: explain how photosynthesis turns light into food. Write ONE "
                   "controlling idea sentence. Goal: answer the exact task, preview the inputs and outputs, "
                   "and take NO side. Before you submit, check your sentence: does it answer how light becomes "
                   "food, does it preview the parts, does it avoid arguing a side? If any answer is no, fix it "
                   "before you submit. Scored on Thesis/Purpose (Central Idea).")),
        Slot("TRANSFER", "stimulus_display", "The topic: volcanoes",
             ref="ACC-W910-FRAME-VOLCANOES", bank="volcanoes",
             body=("Read the short orientation to this new topic, then write your controlling idea. You only "
                   "need the topic and its main parts. This is an explain task, so you take no side.")),
        Slot("TRANSFER", "production_frq", "Write a controlling idea on a NEW topic",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("New topic. The task: explain how volcanoes form and erupt. Write ONE controlling idea "
                   "sentence. Goal: answer the exact task, preview the parts (causes and stages), and take NO "
                   "side. Same move as the photosynthesis idea, new topic. Do not just name the topic. Scored "
                   "on Thesis/Purpose (Central Idea).")),
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
