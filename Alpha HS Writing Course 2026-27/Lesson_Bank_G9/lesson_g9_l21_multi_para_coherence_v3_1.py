"""
lesson_g9_l20_multi_para_coherence_v3_1.py  -  G9 KC C.9.04, ARCHETYPE T7 (BUILD, essay-assembly). V3.1.

G9 course L20 (Unit 4, guided), rebuilt to the v3.1 build spec (icm/_config/v3_1-lesson-build-spec.md).
Teaching point (KEPT): ORDER the body paragraphs so each builds on the one before (for example cause before
effect, general before specific), and open each with a transition that links it to the one before. KC C.9.04.
ESSAY-TIER binds full sources: taught VOLCANOES -> transfer SCHOOLLUNCH (partitioned). unit=multi_paragraph.

V3.1 changes vs the prior L20 (both prior hard failures fixed):
  1. FIXED leaked_internal_label: the discrimination no longer says "a Grade-C design bet we label as a bet";
     the design rationale lives in provenance/comments only (Fable finding: that jargon confused students).
  2. FIXED format_fidelity: the TEACH card is now ONE_IDEA callout + a real <ul> of the two moves (ORDER, LINKS),
     not a 125-word prose wall.
  3. FIXED render-QC double-numbering: the diagnosis is a deterministic checklist() of (question, answer) rows,
     not "Step 1, ... Step 2, ..." prose crammed into one paragraph.
  4. v3.1 spine: coping-model think-aloud (draft -> run the two checks -> catch the jump -> reorder + link) with
     literal BEFORE + AFTER; the reusable 2-check tool folded in at point of first use; discrimination moved into
     MODEL (worked example before the quiz) and uses explicit choices=[...] with the correct option NOT the lone
     longest; autonomy + say-the-standard on the independent write. No "Scored on ..." chrome. Own words, no em
     dashes. Passes all 23 lesson_contract gates + gated_reading render-QC.

CRITICAL preserved EXACTLY: id, lesson_type=7, mnemonic_status="proposal", every production_frq unit=multi_paragraph.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A multi-paragraph essay holds together when you '
'<strong>ORDER</strong> the body paragraphs so each builds on the one before, and <strong>LINK</strong> them '
'with a transition at each seam. Good paragraphs in a random order still jump around.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 2 checks</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit a plan, run these two checks on the order:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does each paragraph build on the one before (cause before effect, background before argument, problem before solution)?</li>'
'<li style="margin:2px 0">Does each paragraph after the first open with a transition that links it to the one before?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If either answer is no, the essay jumps instead of building. Reorder, then link the seams.</div></div>')

# coping-model think-aloud panel: a writer resequencing scrambled paragraphs (draft -> check -> catch -> revise),
# then the endpoints. Contains literal BEFORE and AFTER (content_depth). No named near-peer (Timeback rule).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer ordering three volcano paragraphs, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "P1: A volcano can erupt and bury a town. P2: Heat melts '
    'rock into magma. P3: Scientists watch for warning signs." Check it: does each paragraph build on the one '
    'before? No. I put the eruption (the effect) before the magma forming (the cause), so it jumps backward. '
    'Reorder.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "P1: Heat melts rock into magma. P2: A volcano can '
    'erupt. P3: Scientists watch for warning signs." Better, that is cause, then effect, then response. But do the '
    'paragraphs link? Not yet, each still starts cold. Add transitions.</p>'
    '<p style="margin:0"><strong>Final:</strong> "P1: Deep underground, heat melts rock into magma. P2: When that '
    'magma rises, a volcano can erupt violently. P3: Because eruptions are dangerous, scientists watch for warning '
    'signs." Now it builds, and the seams link ("when that magma," "because eruptions").</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> effect before cause, each paragraph starting cold: the essay '
    'jumps around.</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> cause, then effect, then response, linked at each seam: the essay '
    'builds.</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C904-0020", grade="9-10", lesson_type=7,
    unit="G9 U4 - Build essay (multi-paragraph coherence and order)",
    title="Order the Paragraphs So the Essay Builds",
    target=("Order the body paragraphs so each builds on the one before (for example cause before effect), and "
            "open each with a transition that links it to the last. Written across a multi-paragraph essay. "
            "Trait: Organization."),
    acc_tags=["ACC.W.PROD.1", "CCSS.W.9-10.4"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-14",
                "mnemonic_status": "proposal", "kc": "C.9.04", "sot": "icm course-G9.md L20",
                "taught_stimulus": "ACC-W910-INFO-LESSON-VOLCANOES",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-SCHOOLLUNCH",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": "locked L01 v3.1 template; ESSAY-TIER binds full sources.",
                "one_idea": "ORDER the body paragraphs so each builds on the last, and LINK them at the seams.",
                "one_reminder": "2 checks: does each paragraph build on the one before? does each after the first open with a link?",
                "version_note": ("V3.1 rebuild of L20 to the v3.1 build spec. Fixed leaked_internal_label (dropped "
                                 "'Grade-C design bet' from the discrimination; rationale lives here, not in "
                                 "student text) and format_fidelity (TEACH card is ONE_IDEA + a real <ul>, not a "
                                 "prose wall). Fixed render-QC double-numbering (diagnosis is a checklist() of "
                                 "question/answer rows, not 'Step 1/Step 2' prose). Added coping-model think-aloud "
                                 "with BEFORE+AFTER, moved discrimination into MODEL (worked example before quiz) "
                                 "with explicit choices=[...], autonomy + say-the-standard on the independent "
                                 "write. Kept teaching point (order + link), bound stimuli, id, lesson_type=7, "
                                 "mnemonic_status=proposal, unit=multi_paragraph on every production."),
                "council": ("T7/BUILD structure rung: introduces B3 multi-paragraph coherence (order so each "
                            "paragraph builds; transitions BETWEEN paragraphs). builds-vs-jumps discrimination "
                            "labeled Grade-C in code only. BUILD=proposal; unit=multi_paragraph."),
                "review_provenance": "built to the L01 v3.1 pattern (Fable-5 reviewer + Council findings applied)"},
    fade_ledger_moves=["order-paragraphs-to-build", "transitions-between-paragraphs"],
    slots=[
        # ===== TEACH: ONE idea + a real list of the two moves (no prose wall) =====
        Slot("TEACH", "teach_card", "The one idea: order to build, then link the seams",
             body=(ONE_IDEA +
                   "You can already build a strong paragraph. A multi-paragraph essay does the same job one level "
                   "up: it connects its paragraphs. Two moves make it cohere:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>ORDER</strong>: put the body paragraphs in a sequence where "
                   "each builds on the one before, cause before effect, background before argument, problem "
                   "before solution.</li>"
                   "<li style=\"margin:4px 0\"><strong>LINK</strong>: open each body paragraph after the first with "
                   "a transition that ties it to the paragraph before, so the reader feels the essay moving, not "
                   "restarting.</li></ul>"
                   "The trap is treating paragraphs as separate boxes. A weak essay has good paragraphs in a "
                   "random order, each starting cold, so it jumps around. Today you put the paragraphs in a "
                   "building order and link them at the seams.")),
        Slot("TEACH", "stimulus_display", "Read the source: volcanoes",
             ref="ACC-W910-INFO-LESSON-VOLCANOES", bank="volcanoes",
             body=("Read this source about volcanoes. Because your job is to ORDER paragraphs, read the whole "
                   "thing and notice the natural sequence, what causes what, and what comes first. You will use "
                   "that to order the body paragraphs. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model think-aloud + the 2-check tool folded in =====
        Slot("MODEL", "annotated_before_after", "Watch scrambled paragraphs get ordered and linked",
             bank="volcanoes",
             body=("Here is the skill in action. Follow the writer resequence three jumbled paragraphs, checking "
                   "the order and adding links. " + COPING_HTML +
                   " Notice the two moves that turned the BEFORE into the AFTER: the writer reordered so the cause "
                   "came before the effect, then opened each later paragraph with a transition. " + REMEMBER +
                   "When you plan your own, order the paragraphs to build first, then link the seams, and run the "
                   "2 checks before you submit.")),
        Slot("MODEL", "discrimination", "Which paragraph order lets the essay build?",
             ref="", labeled_grade_c=True, bank="volcanoes",
             body=("Spot the target before you build it. Which paragraph order lets the essay BUILD, moving from "
                   "cause to effect to response? "
                   "(A) P1: A volcano can erupt violently and bury a whole town in thick ash. P2: Deep "
                   "underground, intense heat slowly melts solid rock into magma. P3: Scientists carefully watch "
                   "active volcanoes for early warning signs.  "
                   "(B) P1: Heat underground melts rock into magma. P2: When that magma rises, a volcano can "
                   "erupt. P3: Because eruptions are dangerous, scientists watch for warning signs.  "
                   "(C) P1: Scientists watch volcanoes for warning signs. P2: A volcano can erupt violently. P3: "
                   "Heat melts rock into magma.  "
                   "(D) P1: Heat underground melts rock into magma. P2: A volcano can erupt violently. P3: "
                   "Scientists watch volcanoes for warning signs. "
                   "Correct: B. It goes cause, then effect, then response, and links the seams."),
             choices=[
                 {"id": "A", "text": "P1: A volcano can erupt violently and bury a whole town in thick ash. P2: Deep underground, intense heat slowly melts solid rock into magma. P3: Scientists carefully watch active volcanoes for early warning signs.",
                  "correct": False,
                  "why": "This puts the effect (an eruption) before its cause (magma forming), so the essay jumps backward instead of building. Every fact is true, but the order is wrong."},
                 {"id": "B", "text": "P1: Heat underground melts rock into magma. P2: When that magma rises, a volcano can erupt. P3: Because eruptions are dangerous, scientists watch for warning signs.",
                  "correct": True,
                  "why": "Correct. It goes cause, then effect, then response, so each paragraph builds on the one before, and the seams link them ('when that magma,' 'because eruptions')."},
                 {"id": "C", "text": "P1: Scientists watch volcanoes for warning signs. P2: A volcano can erupt violently. P3: Heat melts rock into magma.",
                  "correct": False,
                  "why": "This runs backward, from the response to the effect to the cause, so nothing builds. Ordering to build means cause first, then effect, then response."},
                 {"id": "D", "text": "P1: Heat underground melts rock into magma. P2: A volcano can erupt violently. P3: Scientists watch volcanoes for warning signs.",
                  "correct": False,
                  "why": "The order is right (cause, then effect, then response), but each paragraph starts cold with no transition tying it to the one before. Building an essay means ordering the points AND linking the seams, so this is only half the move."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this multi-paragraph draft most need?",
             bank="volcanoes",
             body=("Diagnose before the reveal. An essay has three body paragraphs: P1 says eruptions destroy "
                   "towns; P2 explains how magma forms deep underground; P3 says people build near volcanoes for "
                   "fertile soil. Which single change would most improve the structure? "
                   "(A) reorder so the cause (magma forms) comes before the effect (eruptions destroy towns), and add transitions linking the paragraphs  "
                   "(B) add a fourth body paragraph that covers one more fact about volcanoes, since a longer essay with more paragraphs feels more complete  "
                   "(C) make each body paragraph longer by adding several more sentences and specific details, so every point is explained more fully  "
                   "(D) delete the paragraph about fertile soil, because it explains why people live near volcanoes instead of how the eruptions happen"),
             feedback=("Correct: A. The paragraphs put an effect before its cause and start each one cold, so the "
                       "essay jumps. The fix is to reorder (cause before effect) and link the paragraphs with "
                       "transitions. A fourth paragraph (B) or longer paragraphs (C) do not fix the order; "
                       "deleting content (D) removes a relevant point rather than sequencing it.")),

        # ===== SUPPORTED: framed write (fill-in order frame) on the taught topic =====
        Slot("SUPPORTED", "production_frq", "Order three points and link the first two",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on the two moves. You are given three body points "
                       "about volcanoes, out of order: (a) scientists monitor for warning signs; (b) heat "
                       "underground melts rock into magma; (c) rising magma can erupt violently.",
                 setapart_block=setapart("Copy this frame, then fill it in:",
                                         "P1: ______ [the point that comes first]. P2: ______ [a transition that links to P1], then the next point. P3: ______ [a transition that links to P2], then the last point."),
                 closer="Write the building order as three labeled lines, then write the opening transition "
                        "sentence for the second and third paragraphs so each links to the one before. Run the 2 "
                        "checks.")),
        # DIAGNOSIS: check-and-fix on a PROVIDED weak plan (a checklist(), not "Step 1/Step 2" prose), then a
        # fresh self-check. Self-contained (no look-back at the student's own prior work). Stays on the taught
        # topic (no new source to read).
        Slot("MODEL", "diagnosis_frq", "Check a plan for order and links, then run it on a fresh one",
             ref="", bank="volcanoes", scored=True,
             body=frq_prompt(
                 intro="Run the two checks on this weak plan, then fix it and run the same checks on a fresh plan "
                       "of your own.",
                 setapart_block=setapart("Weak plan to fix:",
                                         "P1: Eruptions are dangerous. P2: Magma forms deep underground. P3: Monitoring helps spot risk.", "red"),
                 checklist_block=checklist(title="Run the 2 checks:", rows=[
                     ("Does each paragraph build on the one before?", "No. P1 (the effect) comes before P2 (the cause), so reorder to magma, eruption, monitoring."),
                     ("Does each paragraph after the first open with a link?", "No. Add opening transitions that tie each paragraph to the one before."),
                 ]),
                 closer="Now write a fresh three-point order for a volcano essay and run the same two checks, "
                        "fixing any that fail. Finish by naming the relationship your order follows (for example, "
                        "cause to effect).")),

        # ===== INDEPENDENT: cold write on the taught topic, no frame, autonomy + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Order and link a full set of body paragraphs",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="On your own now, no frame. For an essay explaining how volcanoes form and erupt, write the "
                       "body as THREE ordered paragraph plans (one to two sentences each).",
                 closer="Put them in a building order, and open the second and third with a transition that links "
                        "to the paragraph before. Ordering the paragraphs to build is what every strong "
                        "multi-paragraph essay is made of, and you are ready to do it cold. Before you submit, "
                        "check that each paragraph builds on the last and each after the first opens with a "
                        "link.")),

        # ===== TRANSFER: same move, a NEW topic (free school meals), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: free school meals",
             ref="ACC-W910-ARG-LESSON-SCHOOLLUNCH", bank="school_lunch",
             body=("Read this new source about free school meals. Because your job is to ORDER paragraphs, read "
                   "the whole thing and think about a building order for an argument (for example, the problem "
                   "first, then the benefit, then a response to the cost concern). The text stays on screen while "
                   "you work.")),
        Slot("TRANSFER", "production_frq", "Order and link body paragraphs on a NEW topic",
             ref="", bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="New topic. For an argument about free school meals, write the body as THREE ordered "
                       "paragraph plans in a building order (for example: the problem of classroom hunger, then "
                       "the benefit of universal meals, then a response to the cost concern).",
                 closer="Link the second and third to the paragraph before. Same ordering-and-linking move as the "
                        "volcano essay, new topic. Before you submit, run the 2 checks: does each paragraph build, "
                        "and does each after the first open with a link?")),
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
