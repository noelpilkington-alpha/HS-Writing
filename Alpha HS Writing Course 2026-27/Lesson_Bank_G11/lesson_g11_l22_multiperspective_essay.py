"""
lesson_g11_l22_multiperspective_essay.py  -  G11 KC C.11.07, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD, ceiling essay). V3.1.

G11 course L22 (Unit 5, build), rebuilt to the v3.1 build spec (hand-authored). Teaching point (KEPT): plan and
write a complete MULTI-PERSPECTIVE essay - a thesis that stakes the writer's own position, body paragraphs that
weigh the given perspectives to build it (concede what a view gets right, name its limit, advance the thesis),
and a conclusion, rather than a paragraph-per-perspective tour. Written at the essay, untimed.

Preserved EXACTLY from the prior L22: id="ACC-W1112-L-G11-C1105-0022", lesson_type=7, mnemonic_status="proposal",
kc="C.11.07", the unit, the bound stimuli (MP-LESSON-0001 public streets taught -> MP-PERSP-0003 standardized
testing transfer), and the production_frq unit= values (SUPPORTED plan = multi_paragraph, INDEPENDENT + TRANSFER
= essay). The unit ladder still climbs to the essay, the type-7 ceiling.

V3.1 changes vs the prior L22:
  1. FIXED the leaked internal label: the discrimination no longer says "a Grade-C design bet we label as a bet";
     it is a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}] (leaked_internal_label);
     labeled_grade_c stays True in code only.
  2. FIXED the two wall-of-text teach cards: the prose blocks are now a ONE_IDEA callout + real <ul>/<ol> lists
     of the parts and the order of work (format_fidelity, and the v3.1 "parallel items as a list" rule).
  3. Deterministic FRQ + diagnosis prompts via frq_prompt/setapart/checklist (no "Step 1/2" prose, no "Scored on"
     chrome); coping-model before/after kept with literal BEFORE and AFTER; check tool folded in as a REMEMBER
     <ol> box at first use.
Own words, no fabricated figures, no em dashes, no named HTML entities. Passes all 23 lesson_contract gates +
render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A multi-perspective essay is <strong>one position, '
'built by weighing the views</strong>, not a tour of them. Your thesis stakes a stance; each body paragraph '
'weighs a given perspective to build that stance. You do not summarize each view in turn and retreat to '
'"it is complicated."</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: reread the essay</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, reread the whole essay and ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Is there a real position, not "it is complicated"?</li>'
'<li style="margin:2px 0">Does each body paragraph WEIGH a perspective (concede, limit, advance) instead of just explaining it?</li>'
'<li style="margin:2px 0">Does every paragraph push the same position forward?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you submit.</div></div>')

# coping-model before/after: a paragraph-per-perspective tour (no position) rebuilt into a staked essay whose
# thesis is built by weighing. Contains BOTH a literal BEFORE and AFTER (content_depth). Short structural sketch,
# not a whole essay - the point is the tour-vs-weigh contrast.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> a tour of the three views, no position</span>'
    '<p style="margin:8px 0 0;font-size:15px">Perspective One argues that a street\'s first job is to keep '
    'traffic and deliveries moving. Perspective Two argues that a street is a public room where people gather '
    'and linger. Perspective Three argues that the residents of a block should decide for themselves. All three '
    'raise fair points, and this is clearly a complicated issue with no easy answer.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">This is a guided tour: it summarizes each view in '
    'turn and then retreats to "the issue is complicated." The writer stakes no position, so the essay never '
    'weighs the views or enters the conversation.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> a position, built by weighing the views</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">POSITION (thesis)</span> "A city should let a block\'s residents decide, but inside a '
      'rule that guarantees room for people, because a street built for speed alone can hollow out the '
      'neighborhood it was meant to serve." '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">WEIGH PERSPECTIVE ONE</span> "Perspective One is right that clear roads protect the '
      'deliveries and commutes a working economy needs, so any plan that ignores traffic will strand the very '
      'workers and shops it claims to help; its limit is treating speed as the goal rather than a means, since '
      'a corridor built only for through-traffic loses the foot traffic those same businesses live on." '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">ADVANCE</span> "So I fold the public-room and local-control views into one stance: '
      'residents decide, but never below the floor of a walkable, economically live street."</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">The AFTER stakes one position, then runs beats that '
    'concede what a view gets right (including the economic case for keeping traffic moving), name its limit, '
    'and fold it into the thesis. Weighing the views to build one stance is the multi-perspective essay.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1105-0022", grade="9-10", lesson_type=7,
    unit="G11 U5 - BUILD: full multi-perspective essay",
    title="Write a Full Multi-Perspective Essay",
    target=("Plan and write a complete multi-perspective essay: a thesis that stakes the writer's own position, "
            "body paragraphs that weigh the given perspectives to build it (concede, limit, advance), and a "
            "conclusion, rather than a paragraph-per-perspective tour. Written at the essay, untimed. Trait: "
            "Thesis, Evidence, and Development."),
    acc_tags=["ACC.W.ARG.2", "ACC.W.ARG.4", "ACC.W.PROD.1", "CCSS.W.11-12.1", "CCSS.W.11-12.4"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.07", "sot": "icm course-G11.md L22",
                "taught_stimulus": "ACC-W1112-MP-LESSON-0001",
                "transfer_stimulus": "ACC-W910-MP-PERSP-0003",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": "v3.1 spine; PERSPECTIVE-SET tier binds the 3-perspective prompt; ESSAY grain, UNTIMED.",
                "one_idea": "A multi-perspective essay is one position, built by weighing the views, not a tour of them.",
                "one_reminder": "Reread check: a real position (not 'it is complicated')? each body paragraph weighs (concede, limit, advance)? every paragraph pushes the same position?",
                "council": ("T7/BUILD G11 multi-perspective essay: full essay (E2) with E1/N2/L1 recycle. "
                            "weigh-to-build-thesis-vs-perspective-tour discrimination labeled Grade-C internally. "
                            "Untimed. BUILD=proposal; unit=essay."),
                "version_note": ("V3.1 rebuild of L22. Removed the leaked internal label from the discrimination "
                                 "and moved it to explicit choices=[]; broke the two wall-of-text teach cards into "
                                 "a ONE_IDEA callout + real <ul>/<ol> lists (format_fidelity); deterministic "
                                 "frq_prompt/setapart/checklist bodies (no 'Step 1/2' prose, no 'Scored on' "
                                 "chrome); coping-model before/after kept with literal BEFORE/AFTER; check tool "
                                 "folded in as a REMEMBER <ol> box. Preserved id, type 7, kc C.11.07, "
                                 "mnemonic_status=proposal, unit, bound stimuli, and production_frq unit= values."),
                "review_provenance": "built to the L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["full-multi-perspective-essay", "weigh-to-build-a-thesis"],
    slots=[
        # ===== TEACH: the one idea + the parts (as a list), then the order of work (as a list) =====
        Slot("TEACH", "teach_card", "The one idea: weigh the views to build one position",
             body=(ONE_IDEA +
                   "You have practiced weighing a single perspective. A full essay puts the whole move together. "
                   "Here are the parts:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Thesis</strong>: a thesis is a one-sentence claim that "
                   "stakes your own position on the issue, and your whole essay builds it.</li>"
                   "<li style=\"margin:4px 0\"><strong>Weigh</strong>: to weigh a perspective means to concede "
                   "what it gets right, name its limit, and then advance your own position past it. Each body "
                   "paragraph weighs one given perspective.</li>"
                   "<li style=\"margin:4px 0\"><strong>Evidence</strong>: support each weighing with a specific "
                   "example from your own knowledge, since a perspective set gives you no passage.</li>"
                   "<li style=\"margin:4px 0\"><strong>Conclusion</strong>: land your stance instead of repeating "
                   "that the issue is complicated.</li></ul>"
                   "The trap is a <dfn class=\"tb-glossary-term\" data-catalog-idref=\"def-tour\" "
                   "title=\"a tour means an essay that summarizes each view in turn and takes no position\">tour</dfn>"
                   ": summarizing each view in turn and never committing. Stake a position, then weigh.")),
        Slot("TEACH", "teach_card", "How to plan the weighing before you draft",
             body=("Here is the order of work. Plan the weighing first and the essay assembles itself from moves "
                   "you already own:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>POSITION</strong>: write your own stance on the issue in "
                   "one line.</li>"
                   "<li style=\"margin:4px 0\"><strong>ASSIGN</strong>: for each body paragraph, note which given "
                   "perspective it weighs and what it will concede, limit, and advance.</li>"
                   "<li style=\"margin:4px 0\"><strong>DRAFT</strong>: write an intro that states the position, "
                   "one weighing paragraph per assigned perspective, and a conclusion that lands the stance.</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: reread and confirm the position is real, "
                   "every paragraph weighs rather than summarizes, and every paragraph pushes the same "
                   "position.</li></ol>"
                   "Two or three weighed paragraphs with specific examples beat a tour of all three. There is no "
                   "clock; plan the weighing, then build.")),
        Slot("TEACH", "stimulus_display", "Read the issue and three perspectives: public streets",
             ref="ACC-W1112-MP-LESSON-0001", bank="mp_public_space",
             body=("Read the streets issue and its three perspectives again. This is the build: fix your own "
                   "position, then plan which perspective each body paragraph will weigh and how it advances "
                   "your thesis. There is no passage; examples come from your own knowledge. The prompt stays on "
                   "screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + check tool, then the check items =====
        Slot("MODEL", "annotated_before_after", "Watch a perspective tour become a staked essay",
             bank="mp_public_space",
             body=("Here is the difference between touring the views and weighing them. Read the BEFORE, then the "
                   "AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE tours the three views and retreats to 'it is complicated.' The AFTER stakes a "
                   "thesis and builds it by weighing each view (concede, limit, advance). Weighing to build a "
                   "thesis is what the essay measures." + REMEMBER +
                   "When you build your own, plan the position first, then run the check before you submit.")),
        Slot("MODEL", "discrimination", "Which plan built the essay by weighing?",
             ref="", labeled_grade_c=True, bank="mp_public_space",
             body=("You have watched a tour become a staked essay. Now spot the target: which plan builds a "
                   "position by weighing the given perspectives? "
                   "(A) The writer states a single position, then plans body paragraphs that each take one given "
                   "perspective, concede what it gets right, name its limit, and advance the position, closing "
                   "with a conclusion that lands the stance.  "
                   "(B) The writer plans body paragraphs that each explain one given perspective fully and "
                   "fairly in turn, then closes with a conclusion noting that all three views raise valid points "
                   "and the issue itself stays genuinely complicated.  "
                   "(C) The writer picks the single perspective they agree with, argues it hard for the whole "
                   "essay, and dismisses the other two given perspectives as simply mistaken without conceding "
                   "anything they get right.  "
                   "(D) The writer states a position up front, then fills each body paragraph with their own "
                   "reasons for that position and never returns to the three given perspectives or weighs what "
                   "any of them gets right.  "
                   "Correct: A. A weighs each perspective (concede, limit, advance) to build one position, so the "
                   "essay enters the conversation. B explains the three fairly and stakes no position, so it "
                   "tours the views and never commits. C stakes a position but defends only one view and "
                   "dismisses the rest, so it never weighs what the other perspectives get right. D stakes a "
                   "position but ignores the given perspectives entirely, arguing from the writer's own reasons "
                   "instead of weighing the views."),
             choices=[
                 {"id": "A", "text": "The writer states a single position, then plans body paragraphs that each take one given perspective, concede what it gets right, name its limit, and advance the position, closing with a conclusion that lands the stance.",
                  "correct": True,
                  "why": "Correct. Each paragraph weighs a perspective (concede, limit, advance) in service of one staked position, so the essay builds a thesis and enters the conversation."},
                 {"id": "B", "text": "The writer plans body paragraphs that each explain one given perspective fully and fairly in turn, then closes with a conclusion noting that all three views raise valid points and the issue itself stays genuinely complicated.",
                  "correct": False,
                  "why": "This is a fair tour. Explaining each view and calling the issue complicated stakes no position, so the essay never weighs the views or commits to a stance."},
                 {"id": "C", "text": "The writer picks the single perspective they agree with, argues it hard for the whole essay, and dismisses the other two given perspectives as simply mistaken without conceding anything they get right.",
                  "correct": False,
                  "why": "This stakes a position but skips the weighing. Dismissing the other views without conceding what they get right is one-sided advocacy, not the concede-limit-advance move a multi-perspective essay is built on."},
                 {"id": "D", "text": "The writer states a position up front, then fills each body paragraph with their own reasons for that position and never returns to the three given perspectives or weighs what any of them gets right.",
                  "correct": False,
                  "why": "This has a position but ignores the given perspectives. Arguing only from the writer's own reasons means no paragraph weighs a view, so the essay never engages the perspectives it was asked to build from."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this multi-perspective essay most need?",
             bank="mp_public_space",
             body=("Diagnose before the reveal. A draft explains all three perspectives fairly, one per "
                   "paragraph, and concludes that the issue is complex. Which single change would most improve "
                   "it? "
                   "(A) stake the writer's own position and rebuild each body paragraph to weigh a perspective "
                   "in service of that position  "
                   "(B) explain each of the three perspectives in fuller detail, adding more background and an "
                   "example so every view is covered more thoroughly  "
                   "(C) add a fourth perspective and summarize it fairly beside the existing three so the essay "
                   "covers an even wider range of views on the issue  "
                   "(D) expand the conclusion into a fuller recap of all three perspectives that ends by "
                   "restating once more that the issue is genuinely complex"),
             feedback=("Correct: A. A fair tour that ends on 'it is complex' takes no position, which is what "
                       "the task penalizes. The fix stakes a thesis and turns each body paragraph into weighing "
                       "(concede, limit, advance) that builds it. Fuller explanations (B), another perspective "
                       "(C), or a longer conclusion (D) do not supply the missing position. There is no clock, "
                       "so there is time to plan the weighing.")),

        # ===== SUPPORTED: plan the essay (multi_paragraph) - the frame is the highest-value scaffold =====
        Slot("SUPPORTED", "production_frq", "Plan your multi-perspective essay",
             ref="", bank="mp_public_space", rubric_ref="rc.ap", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Plan your essay on the streets issue before you write a word of it.",
                 setapart_block=setapart("Fill in this plan:",
                                         "Position: ______ (your one-line stance). Paragraph 1 weighs Perspective ___: concede ______, limit ______, advance ______. Paragraph 2 weighs Perspective ___: concede ______, limit ______, advance ______."),
                 closer="Write your one-line position, then for each body paragraph note which perspective it "
                        "weighs and what it will concede, limit, and advance to build your position. This plan "
                        "is what you will build the essay from.")),
        # ===== INDEPENDENT: build the whole essay from the plan (essay ceiling) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write the full multi-perspective essay",
             ref="", bank="mp_public_space", rubric_ref="rc.ap", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now, build the whole essay from your plan.",
                 closer="Write a complete multi-perspective essay on the streets issue: an introduction that "
                        "stakes your position, body paragraphs that each weigh a given perspective (concede, "
                        "limit, advance with a specific example) to build that position, and a conclusion that "
                        "lands your stance. Then run the reread check and fix any part that fails. Weighing the "
                        "views to build one position is what every real multi-perspective essay is built on, and "
                        "you are ready to do it cold. Take the time you need.")),

        # DIAGNOSIS = self-revision: reread your OWN just-written essay and run the three-question checklist on it,
        # fixing any line that fails. Same taught bank (load balance). Self-contained: the checklist is the
        # scaffold and the grader scores the diagnosis within the item.
        Slot("MODEL", "diagnosis_frq", "Check your own multi-perspective essay",
             ref="", bank="mp_public_space", scored=True,
             body=frq_prompt(
                 intro="Reread the essay you just wrote. Run this checklist on YOUR draft and fix any line that fails.",
                 checklist_block=checklist(title="Check your own draft, row by row:", rows=[
                     ("Is the position a real stance, not 'it is complicated'?", "If it only says the issue is complicated or takes no side, commit to one position someone could reject."),
                     ("Does each body paragraph WEIGH a perspective (concede, limit, advance)?", "If a paragraph only explains the view, rebuild it to concede what it gets right, name its limit, and advance your position."),
                     ("Does every paragraph push the same position?", "If any paragraph drifts to a different stance, align them all to push the one position."),
                 ]),
                 closer="For every row that fails on your draft, fix it in the essay before you move on. Finish by "
                        "naming which part your essay still needs most.")),
        # TRANSFER routed out to the gate/PP100 (essay-grain verdict): the lesson ends at the INDEPENDENT write
        # plus its own-draft self-revision. The PP100 mastery task is a separate resource and is unaffected.
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
