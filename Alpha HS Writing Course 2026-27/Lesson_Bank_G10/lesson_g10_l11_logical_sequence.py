"""
lesson_g10_l11_logical_sequence.py  -  G10 KC C.10.05, ARCHETYPE T6: EDITING-IN-CONTEXT (SPOT, ceiling sentence).
V3.1 rebuild of the pre-v3.1 L11 to the v3.1 lesson build spec (icm/_config/v3_1-lesson-build-spec.md), the
pattern that cleared all 23 lesson_contract gates + the Fable-5 reviewer on G9 L01/L15 v3.1.

TEACHING POINT (KEEP): logical sequence. Order the sentences of a draft so each one builds on the one before
(question then answer, cause then effect, earliest then latest), instead of leaving them in the order they
occurred to you. KC C.10.05. Bound stimuli unchanged: taught HIGHWAYS (interstate_highways) -> transfer
RECYCLING (recycling), bank-partitioned.

V3.1 changes from the current L11 (design pattern, not the teaching point):
  1. TEACH split to ONE idea in a callout + the building-orders contrast as a real LIST (was a 136-word wall of
     text that tripped format_fidelity).
  2. MODEL rebuilt as a coping-model think-aloud (draft -> run the check -> catch the out-of-order jump ->
     revise), still with a literal BEFORE and AFTER; the reusable 3-question check tool is folded in at first use.
  3. DISCRIMINATION uses explicit choices=[{id,text,correct,why}]; the "Grade-C design bet" jargon that leaked
     into the student prompt is gone (labeled_grade_c stays True in code only). Construct confound broken: the
     invariant is "each sentence builds on the one before," not "starts with the earliest word"; distractors are
     padded to homogeneous length so the correct option is not the lone longest.
  4. FRQ + diagnosis bodies built with frq_prompt / setapart / checklist (no "Step 1/Step 2" prose -> kills the
     render double-numbering fail; no "Scored on ..." chrome).
  5. INDEPENDENT names the standard out loud (Yeager). TRANSFER stays a partitioned new topic (recycling).

id, lesson_type=6, kc=C.10.05, and mnemonic_status="proposal" are the current L11's values, unchanged; every
production_frq unit="sentence" (T6 ceiling). Own words, no fabricated figures, no em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Order the sentences of a draft so each one '
'<strong>builds on the one before</strong>. Even clear sentences confuse a reader when they arrive out of order.</div></div>')

# reusable job-aid, folded in at point of first use (the decompose/model card), not cold in step 1 (KH load).
REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit a set of sentences, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does each sentence build on the one before it?</li>'
'<li style="margin:2px 0">If not, what order would build (question then answer, cause then effect, earliest then latest)?</li>'
'<li style="margin:2px 0">Reorder, then read it again to check.</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If the reader has to jump back to make sense of a sentence, it is not in order yet.</div></div>')

# coping-model think-aloud: a WRITTEN editing process (draft -> run the check -> catch the out-of-order jump ->
# revise), then the endpoints. Contains a literal BEFORE and AFTER (content_depth). No named person (Timeback rule).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer reordering one short draft, pass by pass:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Today the interstate carries most long-haul freight. '
    'In the 1950s the government began funding a national highway network. Planners first had to decide who would '
    'pay for it." Run the check: does each sentence build on the one before? No. It opens with the present-day '
    'result, then jumps back to the founding, then further back to the first question.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> I move the earliest step to the front: "Planners first '
    'had to decide who would pay for it. Today the interstate carries most long-haul freight. In the 1950s funding '
    'began." Better start, but the last two still jump: the present-day result lands before the 1950s founding '
    'that caused it.</p>'
    '<p style="margin:0"><strong>Final:</strong> "Planners first had to decide who would pay for it. In the 1950s '
    'the government began funding a national highway network. Today that network carries most long-haul freight." '
    'Question, then founding, then result: each sentence now leads into the next.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> result, then founding, then first question (the reader has to '
    'reassemble the timeline)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> first question, then founding, then result (each sentence builds '
    'on the one before)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1005-0011", grade="9-10", lesson_type=6,
    unit="G10 U3 - Rhetorical revision (logical sequence)",
    title="Order Sentences So Each Builds on the Last",
    target=("Revise a scrambled draft into a logical sequence: order the sentences so each builds on the one "
            "before (for example question then answer, or cause then effect). Written at the sentence. "
            "Trait: Organization."),
    acc_tags=["ACC.W.PROC.2", "CCSS.W.9-10.4"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.05", "sot": "icm course-G10.md L11",
                "taught_stimulus": "ACC-W910-INFO-LESSON-HIGHWAYS",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-RECYCLING",
                "playbook": "_phase2/playbook_T6_SPOT.md",
                "template": "v3.1 lesson build spec; REVISION-TIER, provided draft; source bound for context.",
                "one_idea": "Order the sentences so each one builds on the one before.",
                "one_reminder": "3-question check: does each build? if not, what order builds? reorder and reread.",
                "version_note": ("V3.1 rebuild of L11 to the v3.1 build spec: TEACH split into one-idea callout + "
                                 "building-orders list (fixes the format_fidelity wall of text); MODEL rebuilt as a "
                                 "coping-model think-aloud (first try / second try / final) with a literal BEFORE "
                                 "and AFTER and the 3-question check folded in at point of first use; discrimination "
                                 "moved to explicit choices with the 'Grade-C design bet' jargon removed and the "
                                 "distractors padded to homogeneous length; FRQ + diagnosis bodies use "
                                 "frq_prompt/setapart/checklist (kills the 'Step 1/2' render double-numbering and "
                                 "the 'Scored on' chrome); independent says the standard out loud (Yeager). "
                                 "Teaching point + bound stimuli unchanged."),
                "review_provenance": ("Rebuilt to icm/_config/v3_1-lesson-build-spec.md (the pattern that cleared "
                                      "all 23 lesson_contract gates + the Fable-5 reviewer on G9 v3.1 lessons)."),
                "council": ("T6/SPOT logical-sequence rung: introduces O1 (order so each builds). "
                            "builds-vs-jumps discrimination labeled Grade-C in code (not in student text). "
                            "SPOT=proposal; ceiling sentence.")},
    fade_ledger_moves=["logical-sequence", "order-so-each-builds"],
    slots=[
        # ===== TEACH: ONE idea in a callout + the building-orders contrast as a real LIST (no wall of text) =====
        Slot("TEACH", "teach_card", "Order should carry the reader forward",
             body=(ONE_IDEA +
                   "Logical sequence means arranging sentences (or points) so each one leads naturally into the "
                   "next, instead of jumping around. A few reliable building orders:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Cause then effect</strong>: state what happened before the "
                   "result it produced.</li>"
                   "<li style=\"margin:4px 0\"><strong>Question then answer</strong>: raise the question first, "
                   "then resolve it.</li>"
                   "<li style=\"margin:4px 0\"><strong>Earliest then latest</strong>: move through events in the "
                   "order they occurred.</li></ul>"
                   "The test is simple: does each sentence lead into the next, or does the reader have to jump "
                   "back to make sense of it? A draft that states a result, then its cause, then the first step "
                   "forces the reader to reassemble the order. The trap is leaving sentences in the order they "
                   "occurred to you. Goal today: reorder a scrambled draft so each sentence builds on the last.")),
        Slot("TEACH", "stimulus_display", "Read the source: Building the Interstate Highway System",
             ref="ACC-W910-INFO-LESSON-HIGHWAYS", bank="interstate_highways",
             body=("Read this source on the Interstate Highway System so the sequence of events is familiar. The "
                   "drafts you reorder are about highways. You are not writing about highways from scratch here; "
                   "you are reordering sentences that are given to you. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model think-aloud with the check tool folded in =====
        Slot("MODEL", "annotated_before_after", "Watch a scrambled draft get reordered",
             bank="interstate_highways",
             body=("Here is the skill in action. Follow the writer's reordering below. " + COPING_HTML +
                   " Notice the one move that turned the BEFORE into the AFTER: the writer put the earliest step "
                   "first and the present-day result last, so each sentence builds on the one before it. " +
                   REMEMBER +
                   "When you fix your own draft, do the same: find the sentence that jumps, decide what order "
                   "would build, and run the 3 questions before you submit.")),
        Slot("MODEL", "discrimination", "Which order builds?",
             ref="", labeled_grade_c=True, bank="interstate_highways",
             body=("Now that you have seen one built, spot the target. Each version uses the same three sentences "
                   "about the highway system. Which order lets each sentence build on the one before it? "
                   "Correct: C. It moves from the first question to the founding to the present-day result."),
             choices=[
                 {"id": "A", "text": "Today the interstate carries most long-haul freight. In the 1950s the government began funding a national network. Planners first had to decide who would pay for it.",
                  "correct": False,
                  "why": "This opens with the present-day result, then jumps back to the founding, then further back to the first question. The reader meets the effect before its cause and has to reassemble the timeline."},
                 {"id": "B", "text": "In the 1950s the government began funding a national network. Planners first had to decide who would pay for it. Today the interstate carries most long-haul freight.",
                  "correct": False,
                  "why": "The funding is stated before the planning question that had to come first, so the middle sentence jumps backward. The founding and its earlier question are out of order."},
                 {"id": "C", "text": "Planners first had to decide who would pay for it. In the 1950s the government began funding a national network. Today the interstate carries most long-haul freight.",
                  "correct": True,
                  "why": "Correct. Question, then founding, then present-day result: each sentence leads into the next, so the reader never has to jump back. Ordering to build is the move."},
             ]),
        # SECOND minimal pair, DIFFERENT confound than the first: the first pair permutes three plain sentences
        # (pure content order); this one dresses a wrong order in signpost words (First/Next/Finally) so students
        # who equate "has transition words" with "in order" pick it. The invariant is still "each sentence builds
        # on the one before," so the correct option carries the cause-to-effect content order with NO signposts and
        # is NOT the longest (the signpost-decorated wrong option is longest).
        Slot("MODEL", "discrimination", "Which draft is really in order?",
             ref="", labeled_grade_c=True, bank="interstate_highways",
             body=("Here is a different draft about highway wear. All three orderings below use the same facts. "
                   "Which one is actually in building order, where each sentence leads into the next? "
                   "Correct: B. It runs cause to effect even without any signpost words like First or Finally."),
             choices=[
                 {"id": "A", "text": "First, crews now repave long stretches of the road every summer. Next, heavy trucks pounded the pavement for years. Finally, that pavement cracked and broke into potholes.",
                  "correct": False,
                  "why": "The words First, Next, and Finally make it look ordered, but the content opens with today's repaving before the trucks and cracking that caused it, so it never builds."},
                 {"id": "B", "text": "Heavy trucks pounded the pavement for years. That pavement cracked and broke into potholes. Now crews repave long stretches of the road every summer.",
                  "correct": True,
                  "why": "Correct. Cause to effect: the trucks wear the pavement, the pavement cracks, and only then do crews repave, so each sentence leads into the next even with no signpost words."},
                 {"id": "C", "text": "That pavement cracked and broke into potholes. Heavy trucks pounded the pavement for years. Now crews repave long stretches of the road every summer.",
                  "correct": False,
                  "why": "This states the cracked pavement before the heavy trucks that caused it, so the reader meets the effect before its cause and has to work backward."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this draft most need?",
             bank="interstate_highways",
             body=("Diagnose this draft before the reveal. It reads: 'As a result, drivers reached distant cities "
                   "in hours. Engineers designed long, straight routes with gentle curves. The goal was to move "
                   "traffic fast and safely.' Which single revision most improves the order? "
                   "(A) put the goal first, then the design, then the result, so cause leads to effect  "
                   "(B) add another result sentence about one more way the fast routes helped drivers reach cities  "
                   "(C) make each sentence shorter and simpler so the writing is quicker and easier to read fast  "
                   "(D) combine all three sentences into one long sentence joined with commas and linking connectors"),
             feedback=("Correct: A. The draft states the result ('As a result ...') before the goal and design "
                       "that caused it, so the reader meets the effect before the cause. Reordering to goal, then "
                       "design, then result builds cause to effect. Another result (B) adds content, not order; "
                       "shorter sentences (C) and combining them (D) do not fix the sequence.")),

        # ===== SUPPORTED: framed reorder (fill-in frame) on the taught topic (source read at TEACH step 2) =====
        Slot("SUPPORTED", "production_frq", "Reorder a scrambled draft",
             ref="", bank="interstate_highways", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Reorder these three sentences so each builds on the one before, then write them in the "
                       "new order: 'Today the interstate carries most long-haul freight. In the 1950s the "
                       "government began funding a national network. Planners first had to decide who would pay "
                       "for it.'",
                 setapart_block=setapart("Copy this frame, then fill in each blank with one of the sentences:",
                                         "First: ______ (the earliest step). Next: ______ (what came after it). "
                                         "Last: ______ (the present-day result)."),
                 closer="Order them earliest to latest so each sentence leads into the next. Then run the "
                        "3-question check before you submit.")),
        # DIAGNOSIS = run the check on a PROVIDED weak draft, then rewrite it (not a fresh production, so it does
        # not repeat the Independent write). Stays on the taught topic = no new source to read (load balance).
        Slot("MODEL", "diagnosis_frq", "Check and fix a weak draft with the 3 questions",
             ref="", bank="interstate_highways", scored=True,
             body=frq_prompt(
                 intro="Run the 3-question check on this weak draft, then rewrite it so each sentence builds on "
                       "the one before.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "The network now links nearly every large city. Congress passed a major "
                                         "highway act to fund it. Before that, most long roads were local and "
                                         "disconnected.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Does each sentence build on the one before?", "No. It opens with the present-day network, then jumps back to the funding act, then further back to the roads before it."),
                     ("What order would build?", "Earliest to latest: the disconnected local roads, then the funding act, then today's network."),
                     ("Reorder, then reread.", "Before that, most long roads were local and disconnected. Then Congress passed a major highway act to fund a national network. Today it links nearly every large city."),
                 ]),
                 closer="Now rewrite the weak draft so the sentences run earliest to latest and each builds on "
                        "the last. Then name the building order you used (for example earliest to latest).")),

        # ===== INDEPENDENT: cold reorder on the taught topic + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Reorder a provided draft on your own",
             ref="", bank="interstate_highways", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="On your own now, no frame. Reorder these sentences so each builds on the one before, then "
                       "write them in the new order: 'Today, whole suburbs cluster around the interstate exits. "
                       "After the war, more Americans than ever bought cars. That growing crowd of drivers pushed "
                       "the country to build faster roads.'",
                 closer="Put the earliest point first and the present-day result last so each sentence leads into "
                        "the next. Logical order is what keeps any piece of writing easy to follow, and you are "
                        "ready to do this without a frame. Run the 3-question check before you submit.")),

        # ===== TRANSFER: same move, a NEW topic (recycling), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: how recycling works",
             ref="ACC-W910-INFO-LESSON-RECYCLING", bank="recycling",
             body=("The next draft to reorder is about recycling. Read this new source so the process order is "
                   "familiar. Again, you are reordering sentences that are given to you, not writing from "
                   "scratch. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Reorder a provided draft on a NEW topic",
             ref="", bank="recycling", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="New topic. Reorder these sentences so each builds on the one before, then write them in "
                       "the new order: 'Finally, factories turn the sorted material into new products. A truck "
                       "collects the bottles from the bin. At the plant, machines sort the material by type.'",
                 closer="Same order-to-build move as the highway draft, new topic: put the steps in the order "
                        "they happen so each sentence leads into the next. Run the 3-question check before you "
                        "submit.")),
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
