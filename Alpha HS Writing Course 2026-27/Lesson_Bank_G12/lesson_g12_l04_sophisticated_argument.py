"""
lesson_g12_l04_sophisticated_argument.py  -  G12 KC C.12.01, ESSAY-ASSEMBLY (BUILD, ceiling essay). V3.1.

G12 course L04 (Unit 1, build), rebuilt to the v3.1 build spec (hand-authored). Teaching point (KEPT): plan
and write a complete ARGUMENT essay that BOTH situates the question in a broader context AND holds the tension
without flattening it, so the essay earns sophistication (AP Row C) carried across the whole piece, not a single
clever line. KC C.12.01. FULL-ESSAY lesson (type 7); recycles the G12 sophistication stack and reaches the
essay ceiling.

Preserved EXACTLY from the prior L04: id="ACC-W910-L-G12-C1201-0004", lesson_type=7, kc="C.12.01",
mnemonic_status="proposal", unit, the bound stimuli (WORKFORCEINVEST taught -> WATERTRADEOFF transfer, banks
public_health -> automation_policy), rubric rc.ap, and every production_frq unit= value (SUPPORTED plan =
multi_paragraph, INDEPENDENT + TRANSFER = essay). The ladder still climbs to the essay ceiling for type 7.

V3.1 changes vs the prior L04 (the two failing gates + spine polish):
  1. FIXED the leaked internal label: the discrimination no longer says "a Grade-C design bet we label as a
     bet"; it is a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}]
     (leaked_internal_label). labeled_grade_c stays True in code only.
  2. FIXED the two wall-of-text teach cards: the two prose blocks are now a ONE_IDEA teal callout + real
     <ul>/<ol> lists of the parts and the order of work (format_fidelity + the v3.1 parallel-items rule).
  3. Deterministic FRQ + diagnosis prompts via frq_prompt/setapart/checklist (no "Step 1/2" prose, no
     "Scored on ..." chrome); coping-model before/after kept; the check tool (situate / hold / defend) folded
     in at first use as a real <ol> REMEMBER box.
Own words, no fabricated figures (all facts trace to the bound WORKFORCEINVEST/WATERTRADEOFF sources), no em
dashes. Passes all 23 lesson_contract gates + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Sophistication is <strong>carried across the whole '
'essay</strong>, not dropped in as one clever line. The reader rewards it when every part of the piece situates '
'the question, holds the tension, and defends a real position.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: reread the whole essay</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, reread the whole piece and ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does the thesis SITUATE the choice inside a larger question, not just answer the narrow prompt?</li>'
'<li style="margin:2px 0">Does each body paragraph HOLD the tension, keeping both true things live instead of dismissing a side?</li>'
'<li style="margin:2px 0">Does the conclusion DEFEND a rule or priority a thoughtful opponent would still respect?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you submit.</div></div>')

# coping-model before/after: a competent-but-flat essay (narrow thesis, dismissed opponent, restated ending)
# rebuilt to carry sophistication across all three parts. Contains BOTH a literal BEFORE and AFTER
# (content_depth). Short structural sketch, not a whole essay - the point is the flat-vs-sophisticated contrast.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> competent, but not sophisticated</span>'
    '<p style="margin:8px 0 0;font-size:15px"><i>Thesis:</i> The country should fund job training, because '
    'training helps people get the new jobs. <i>Body:</i> Training works and gives people skills. The other '
    'side says we should help displaced workers, but that view is wrong. <i>Conclusion:</i> So the country '
    'should fund training.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">Clear and organized, but it answers only the narrow '
    'prompt and calls the other side wrong. It never situates the question and it flattens the tension, so it '
    'earns no sophistication.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> sophistication woven through the essay</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">SITUATE (thesis)</span> "Whether to fund training or protect displaced workers is one '
      'case of how a society splits a fixed budget between the future and the present, and it should fund '
      'training only if it also cushions those the change leaves behind." '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">HOLD TENSION (body)</span> "Training aims at the next generation, yet the same dollar '
      'could steady a fifty-year-old whose industry is closing now, so the real question is not which side is '
      'right but how much of each a budget can carry." '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">DEFEND (conclusion)</span> "A rule that spends first on training but reserves a share '
      'for transition support answers both needs, so even a reader who favors the displaced would have to take '
      'it seriously."</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same prompt, but the thesis situates the question, '
    'the body holds the tension instead of dismissing a side, and the conclusion defends a rule. Sophistication '
    'carried across the whole essay is the move.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G12-C1201-0004", grade="9-10", lesson_type=7,
    unit="G12 U1 - BUILD: sophisticated argument full-write",
    title="Write a Full Argument That Earns Sophistication",
    target=("Plan and write a complete argument essay that situates the question in a broader context and holds "
            "the tension without flattening it, so sophistication is carried across the whole piece, rather than "
            "a competent essay that answers only the narrow prompt. Written at the essay, untimed. Trait: "
            "Sophistication (Row C) with Development and Evidence."),
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "ACC.W.PROD.1", "CCSS.W.11-12.1", "CCSS.W.11-12.4"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.12.01", "sot": "icm course-G12.md L04",
                "taught_stimulus": "ACC-W910-ARG-LESSON-WORKFORCEINVEST",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-WATERTRADEOFF",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": "v3.1 spine; ESSAY-TIER binds full G12 argument sources; UNTIMED (no Timeback timer). "
                            "AP sophistication (Row C) at essay scale.",
                "one_idea": "Sophistication is carried across the whole essay (situate + hold the tension + defend), not one clever line.",
                "one_reminder": "Reread check: thesis situated? every body paragraph holds the tension? conclusion defends a rule an opponent respects?",
                "version_note": ("V3.1 rebuild of L04. FIXED the two failing gates on the prior version: removed "
                                 "the leaked internal label ('a Grade-C design bet we label as a bet') from the "
                                 "discrimination and moved it to explicit choices=[]; broke the two wall-of-text "
                                 "teach cards into a ONE_IDEA callout + real <ul>/<ol> lists (format_fidelity). "
                                 "Deterministic frq_prompt/setapart/checklist bodies (no 'Step 1/2' prose, no "
                                 "'Scored on' chrome); situate/hold/defend check tool folded in at first use. "
                                 "Preserved id, type 7, kc C.12.01, mnemonic_status=proposal, unit, bound stimuli, "
                                 "rc.ap, and every production_frq unit= value (SUPPORTED=multi_paragraph, "
                                 "INDEPENDENT/TRANSFER=essay); ladder climbs to essay."),
                "council": ("T7/BUILD G12 sophistication build: situate + hold-the-tension across a full ARGUMENT "
                            "write. sophisticated-vs-competent discrimination is a Grade-C design bet, labeled in "
                            "code only. BUILD=proposal; unit=essay."),
                "review_provenance": "built to the L01/G9 L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["sophisticated-argument-essay", "situate-and-hold-across-the-essay"],
    slots=[
        # ===== TEACH: the one idea + the three moves (as a list), then the order of work (as a list) =====
        Slot("TEACH", "teach_card", "The one idea: sophistication runs through the whole essay",
             body=(ONE_IDEA +
                   "You have met each of these moves on its own. A sophisticated argument puts them together and "
                   "keeps them running from the first line to the last:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>SITUATE</strong>: your thesis is a one-sentence statement "
                   "of the position your whole essay defends, and here it frames the narrow prompt as one "
                   "instance of a larger question.</li>"
                   "<li style=\"margin:4px 0\"><strong>HOLD THE TENSION</strong>: each body paragraph keeps both "
                   "true things live and reasons from their conflict, rather than calling one side wrong and "
                   "setting it aside.</li>"
                   "<li style=\"margin:4px 0\"><strong>DEFEND</strong>: your conclusion lands a real position, "
                   "often a rule or a priority that a thoughtful opponent would still have to respect.</li></ul>"
                   "A competent essay (clear thesis, evidence, organization) is the floor. Sophistication is what "
                   "lifts it, and it has to run through the whole piece.")),
        Slot("TEACH", "teach_card", "How to build it, part by part",
             body=("Here is the order of work. Plan the sophistication first, then draft from the plan:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>PLAN</strong>: write your situated thesis (the larger "
                   "question plus your position within it), then the tension each body paragraph will hold and "
                   "the evidence it uses, then the rule your conclusion will defend.</li>"
                   "<li style=\"margin:4px 0\"><strong>INTRO</strong>: frame the choice as one case of the larger "
                   "question, and state the situated thesis.</li>"
                   "<li style=\"margin:4px 0\"><strong>BODY</strong>: write each planned point as a full "
                   "paragraph that holds its tension and reasons from it with evidence, not one that flattens the "
                   "tension into a tidy dismissal.</li>"
                   "<li style=\"margin:4px 0\"><strong>CONCLUSION</strong>: defend the rule or priority.</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: reread and confirm the thesis situates, "
                   "every paragraph holds its tension, and the conclusion defends a real position.</li></ol>"
                   "Plan the sophistication, draft from the plan, then self-check that it runs through the whole "
                   "essay.")),
        Slot("TEACH", "stimulus_display", "Read the source: prepare workers or protect them?",
             ref="ACC-W910-ARG-LESSON-WORKFORCEINVEST", bank="public_health",
             body=("Read this source on preparing more workers for growing fields or protecting those a change "
                   "displaces. Because your job is to write a full sophisticated argument from it, read the whole "
                   "thing and gather the larger question you can situate the choice in, plus the real tension the "
                   "body will hold and the federal figures you can use as evidence. The text stays on screen "
                   "while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + check tool, then discrimination + predict =====
        Slot("MODEL", "annotated_before_after", "Watch a competent essay gain sophistication",
             bank="public_health",
             body=("Here is a competent-but-flat essay rebuilt to carry sophistication across all three parts. "
                   "Read the BEFORE, then the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE is organized but narrow and dismissive. The AFTER situates the question, holds "
                   "the tension, and defends a rule. Sophistication carried across the whole essay is the move." +
                   REMEMBER +
                   "When you build your own, run these three questions before you submit.")),
        Slot("MODEL", "discrimination", "Which essay plan earns sophistication?",
             ref="", labeled_grade_c=True, bank="public_health",
             body=("You have watched a competent essay gain sophistication. Now spot the target: which plan earns "
                   "sophistication, and which is only competent? "
                   "(A) Open with one clear thesis, give three tidy paragraphs of evidence that all back the same "
                   "side, treat the opposing view as simply mistaken and set it quietly aside, then restate the "
                   "opening thesis in fresh words to close the whole essay out neatly.  "
                   "(B) Situate the choice inside the larger question of how a society splits a fixed budget "
                   "between the future and the present workforce, hold that tension in every paragraph, and "
                   "defend a splitting rule the other side would still respect.  "
                   "(C) Load the essay with more advanced vocabulary and longer, more formal sentences, add a "
                   "fourth supporting paragraph that stacks on one more example for the same side, and write a "
                   "much longer conclusion that walks back through every reason once again in fuller detail. "
                   "Correct: B earns sophistication; A and C are only competent. (A) is organized but narrow and "
                   "flattens the other side; (C) polishes the surface but never situates or holds the tension. "
                   "(B) situates, holds the tension, and defends. Sophistication across the essay is the move."),
             choices=[
                 {"id": "A", "text": "Open with one clear thesis, give three tidy paragraphs of evidence that all back the same side, treat the opposing view as simply mistaken and set it quietly aside, then restate the opening thesis in fresh words to close the whole essay out neatly.",
                  "correct": False,
                  "why": "This is competent, not sophisticated. It is organized, but it answers only the narrow prompt and flattens the other side by calling it mistaken, so no sophistication is carried."},
                 {"id": "B", "text": "Situate the choice inside the larger question of how a society splits a fixed budget between the future and the present workforce, hold that tension in every paragraph, and defend a splitting rule the other side would still respect.",
                  "correct": True,
                  "why": "Correct. It situates the choice in a larger question, holds the tension paragraph by paragraph instead of dismissing a side, and defends a rule an opponent must respect. Sophistication runs through the whole essay."},
                 {"id": "C", "text": "Load the essay with more advanced vocabulary and longer, more formal sentences, add a fourth supporting paragraph that stacks on one more example for the same side, and write a much longer conclusion that walks back through every reason once again in fuller detail.",
                  "correct": False,
                  "why": "Fancier words, one more paragraph, and a longer conclusion polish the surface but never situate the question or hold the tension. The reader rewards the reasoning, not the packaging."},
             ]),
        Slot("MODEL", "predict_the_fix", "What lifts this essay to sophistication?",
             bank="public_health",
             body=("Diagnose before the reveal. A draft is well organized with a clear thesis and solid evidence, "
                   "but it answers only the literal prompt and calls the other side mistaken. Which single change "
                   "would most likely earn sophistication? "
                   "(A) situate the question in its broader frame and hold the tension across the body instead of "
                   "dismissing the other side  "
                   "(B) add a fourth body paragraph that stacks one more supporting example onto the same "
                   "position the draft already argues  "
                   "(C) swap in more advanced academic vocabulary and build longer sentences so the writing "
                   "sounds more scholarly and formal  "
                   "(D) write a much longer conclusion that restates the thesis and walks back through each body "
                   "reason in fuller detail"),
             feedback=("Correct: A. Organization and evidence make it competent, not sophisticated. The lift comes "
                       "from situating the question and holding the tension throughout, then defending a position "
                       "that answers it. More evidence (B), bigger vocabulary (C), or a longer conclusion (D) do "
                       "not carry sophistication. There is no clock, so there is time to plan the sophistication.")),

        # ===== SUPPORTED: plan the sophisticated argument (multi_paragraph) - the frame is the top scaffold =====
        Slot("SUPPORTED", "production_frq", "Plan the sophisticated argument",
             ref="", bank="public_health", rubric_ref="rc.ap", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Plan a sophisticated argument on the workforce prompt before you draft a word of it.",
                 setapart_block=setapart("Fill in this plan:",
                                         "Situated thesis: ______ (the larger question + my position). Body 1: tension ______ + evidence ______. Body 2: tension ______ + evidence ______. Conclusion: the rule I defend ______."),
                 closer="Write your situated thesis (larger question plus position), then for each body paragraph "
                        "the real tension it holds and its evidence, then the rule your conclusion defends. This "
                        "plan is what you will build the essay from.")),
        # ===== INDEPENDENT: build the whole sophisticated essay from the plan (essay ceiling) + say-standard =====
        Slot("INDEPENDENT", "production_frq", "Write the full sophisticated argument",
             ref="", bank="public_health", rubric_ref="rc.ap", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now, build the whole essay from your plan.",
                 closer="Write a complete argument essay on the workforce prompt: an introduction that situates "
                        "the choice in its broader question, body paragraphs that each hold a real tension and "
                        "reason from it with evidence, and a conclusion that defends a rule or priority a "
                        "thoughtful opponent must respect. Then run the reread check (situated, tension held, "
                        "position defended) and fix any part that fails. Carrying sophistication across a whole "
                        "argument is what every strong AP essay is built on, and you are ready to do it cold. "
                        "There is no time limit; take the time you need.")),

        # DIAGNOSIS = self-revision: reread your OWN just-written essay and run the 3-question check on it,
        # fixing any line that fails. Same taught source (load balance). Self-contained: the checklist is the
        # scaffold and the grader scores the diagnosis within the item.
        Slot("MODEL", "diagnosis_frq", "Self-check your own essay against the three moves",
             ref="", bank="public_health", scored=True,
             body=frq_prompt(
                 intro="Reread the essay you just wrote. Run this checklist on YOUR draft and fix any line that fails.",
                 checklist_block=checklist(title="Check your own draft, line by line:", rows=[
                     ("Is the thesis situated in a larger question?", "If it only answers the narrow prompt (like just picking whether to fund training), frame it inside the larger question of how a society splits a fixed budget between the future and the present."),
                     ("Does each body paragraph hold a tension?", "If a paragraph just stacks reasons for one side or calls the other side wrong, give it a real tension it keeps live instead of a dismissal."),
                     ("Does the conclusion defend a real position?", "If it only restates the thesis, name the rule or priority a thoughtful opponent would still have to respect."),
                 ]),
                 closer="For every line that fails on your draft, name what is off in one sentence and make the "
                        "fix. Finish by naming the larger question your essay situates the choice in.")),
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
