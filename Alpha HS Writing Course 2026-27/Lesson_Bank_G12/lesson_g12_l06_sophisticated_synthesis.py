"""
lesson_g12_l06_sophisticated_synthesis.py  -  G12 KC C.12.01, ARCHETYPE T8: CROSS-SOURCE-SYNTHESIS (WEAVE, essay). AP SOPHISTICATION. V3.1.

G12 course L06 (Unit 1, build), rebuilt to the v3.1 build spec (hand-authored). Teaching point (KEPT): write a
full SYNTHESIS that weaves one argument from the set and weights each source AND earns sophistication (Row C) by
situating the synthesized claim in a broader question and holding the tension the sources create, rather than a
competent-but-flat synthesis. KC C.12.01, type 8. SYNTHESIS-TIER binds the G11 teaching synth set (reused, fresh
to the G12 student): taught SYNTH-LESSON-0001 (water) -> transfer SYNTH-SET-0002 (AI workforce, cold-to-G12).

Preserved EXACTLY from the prior L06: id="ACC-W1112-L-G12-C1201-0006", lesson_type=8, mnemonic_status="proposal",
kc="C.12.01", unit, the bound stimuli, rubric_ref="rc.ap", and the production_frq unit= ladder (SUPPORTED plan =
multi_paragraph, INDEPENDENT + TRANSFER = essay). The unit ladder still climbs to the essay, the type-8 ceiling.

V3.1 changes vs the prior L06 (the two failing gates + the spine polish):
  1. FIXED the leaked internal label: the discrimination no longer says "a Grade-C design bet we label as a bet";
     it is a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}] (leaked_internal_label).
  2. FIXED the two wall-of-text teach cards: the two prose blocks are now a ONE_IDEA callout + real <ul>/<ol>
     lists of the parts and the order of work (format_fidelity + the v3.1 "parallel items as a list" rule).
  3. Deterministic FRQ + diagnosis prompts via frq_prompt/setapart/checklist (no "Step 1/2" prose, no "Scored on"
     chrome); coping-model before/after kept; the check tool (the 3-question synthesis check) folded in at first
     use as a real <ol> REMEMBER box.
Own words, faithful to the bound source, no fabricated figures, no em dashes. Passes all 23 gates + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A synthesis reaches real complexity when it does more '
'than weave the sources correctly: it <strong>situates</strong> the claim it builds in the larger question that '
'claim is one case of, and <strong>holds the tension</strong> the sources create instead of flattening it into '
'a plain "do less".</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: read the synthesis for depth and significance</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, reread the whole synthesis and ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Is there ONE woven argument, with each source weighted for how much it carries?</li>'
'<li style="margin:2px 0">Is the woven claim SITUATED in the larger question it is one case of?</li>'
'<li style="margin:2px 0">Does the essay HOLD the sources'
"'"
' tension and reason from it, instead of ending on a flat "use less"?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you submit.</div></div>')

# coping-model before/after: a competent-but-flat synthesis rebuilt to situate its claim and hold the sources'
# tension. Contains BOTH a literal BEFORE and AFTER (content_depth). Faithful to the bound water set (scarcity;
# power and farming both draw heavily; cutting either use starves the other). No fabricated figures, no persona.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> a competent weave with no complexity</span>'
    '<p style="margin:8px 0 0;font-size:15px">The sources show water is scarce and that power plants and farms '
    'both draw heavily on it, so the country should use less water. The essay weaves the three sources and gives '
    'the farm source the most weight, then stops there.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">A real woven, weighted argument, but flat. It never '
    'names the larger question the claim answers, and it flattens the tension (cutting either use starves the '
    'other) into a plain "use less".</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> synthesis situated, tension held</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">SITUATED SYNTHESIS</span> Read together, the sources make water scarcity one case of a '
      'society outrunning a shared resource, and because cutting either power or farming starves the other, the '
      'set supports not a call to "use less" but a rationing rule that ranks the two uses, the only answer that '
      'survives the tension the three sources build.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same weighted weave, but now the claim is placed in '
    'a larger question and the essay reasons from the tension to a real position. Situating the synthesis and '
    'holding the tension is the complexity move.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G12-C1201-0006", grade="9-10", lesson_type=8,
    unit="G12 U1 - BUILD: sophisticated synthesis full-write",
    title="Write a Full Synthesis That Weighs the Sources",
    target=("Write a full synthesis that weaves one argument from the set and weights each source AND reaches "
            "real complexity by situating the synthesized claim in a broader question (cS2) and holding the "
            "tension the sources create (rS2), rather than a competent-but-flat synthesis. Written at the "
            "essay, untimed. Trait: Depth and Significance with Development (synthesis) and Evidence."),
    acc_tags=["ACC.W.SRC.1", "ACC.W.ARG.2", "CCSS.W.11-12.7", "CCSS.W.11-12.1"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.12.01", "sot": "icm course-G12.md L06",
                "taught_stimulus": "ACC-W1112-SYNTH-LESSON-0001",
                "transfer_stimulus": "ACC-W910-SYNTH-SET-0002",
                "playbook": "_phase2/playbook_T8_WEAVE.md",
                "template": ("v3.1 spine; SYNTHESIS-TIER binds the G11 teaching synth set (reused, fresh to the "
                             "G12 student); AP sophistication (Row C) on a synthesis full-write; UNTIMED."),
                "one_idea": "A synthesis earns sophistication by situating the woven claim and holding the sources' tension.",
                "one_reminder": "Row C check: one weighted weave? claim situated in a larger question? tension held, not flattened?",
                "version_note": ("V3.1 rebuild of L06. FIXED the two failing gates on the prior version: removed "
                                 "the leaked internal label ('a Grade-C design bet we label as a bet') from the "
                                 "discrimination and moved it to explicit choices=[]; broke the two wall-of-text "
                                 "teach cards into a ONE_IDEA callout + real <ul>/<ol> lists (format_fidelity). "
                                 "Deterministic frq_prompt/setapart/checklist bodies (no 'Step 1/2' prose, no "
                                 "'Scored on' chrome); coping-model before/after kept; the synthesis check tool "
                                 "folded in at first use as a real <ol> REMEMBER box. Preserved id, type 8, "
                                 "mnemonic_status=proposal, kc, unit, bound stimuli, rubric_ref=rc.ap, and the "
                                 "production_frq unit= ladder (SUPPORTED=multi_paragraph, INDEPENDENT/TRANSFER=essay)."),
                "council": ("T8/WEAVE G12 sophistication build: rS2 + cS2 on a full SYNTHESIS write (situate the "
                            "synthesized claim + hold the tension the sources create). situated-vs-flat "
                            "discrimination labeled Grade-C in code. WEAVE=proposal; unit=essay."),
                "review_provenance": "built to the G9 L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["sophisticated-synthesis", "situate-and-hold-the-synthesized-claim"],
    slots=[
        # ===== TEACH: the one idea + what the two moves are (as a list), then the order of work (as a list) =====
        Slot("TEACH", "teach_card", "The one idea: a complex synthesis situates the claim it builds",
             body=(ONE_IDEA +
                   "You already own the two moves this needs. A full essay puts them on top of a correct weave:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Synthesize</strong>: to synthesize means to combine "
                   "several sources into one argument the whole set builds, assigning each point to the source "
                   "that carries it.</li>"
                   "<li style=\"margin:4px 0\"><strong>Weight</strong>: to weight a source means to give it more "
                   "or less emphasis based on how much it actually carries, not treat all three as equal.</li>"
                   "<li style=\"margin:4px 0\"><strong>Situate</strong>: to situate a claim means to name the "
                   "larger question the claim is one case of (water scarcity as one case of a society outrunning "
                   "a shared resource).</li>"
                   "<li style=\"margin:4px 0\"><strong>Hold the tension</strong>: to hold the tension means to "
                   "keep the conflict the sources create live (cutting either use starves the other) and reason "
                   "from it toward a real position, often a rule.</li></ul>"
                   "The trap is a correct weave with no larger frame, which lands flat on \"use less\". Weave and "
                   "weight, then situate and hold the tension.")),
        Slot("TEACH", "teach_card", "How to build it, part by part",
             body=("Here is the order of work. Plan first; there is no clock, so take the time to plan before "
                   "you draft:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>WEAVE</strong>: write the ONE argument the set builds and "
                   "which source carries each point.</li>"
                   "<li style=\"margin:4px 0\"><strong>QUESTION</strong>: name the broader question that woven "
                   "claim is one case of.</li>"
                   "<li style=\"margin:4px 0\"><strong>TENSION</strong>: name the conflict the sources create "
                   "and refuse to flatten it.</li>"
                   "<li style=\"margin:4px 0\"><strong>POSITION</strong>: decide the position you defend within "
                   "that question and tension, then draft intro, body-by-point, and conclusion from the plan.</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: reread for depth and significance, is it one weighted "
                   "weave, is the claim situated, is the tension held?</li></ol>"
                   "This is the unit applied to synthesis, run once on your own.")),
        Slot("TEACH", "stimulus_display", "Read the source set: competing water uses (3 sources)",
             ref="ACC-W1112-SYNTH-LESSON-0001", bank="water_competing_uses",
             body=("Read this three-source set on competing water uses. Because your job is to write a full, "
                   "complex synthesis from it, find the one argument the set builds, the broader question "
                   "it is one case of, and the tension the sources create, then plan a synthesis that situates "
                   "the claim and holds that tension. The texts stay on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + check tool, then the discrimination + predict =====
        Slot("MODEL", "annotated_before_after", "Watch a flat synthesis gain complexity",
             bank="water_competing_uses",
             body=("Here is a competent-but-flat synthesis rebuilt to situate its claim and hold the sources' "
                   "tension. Read the BEFORE, then the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE weaves and weights but stops at \"use less\". The AFTER situates the claim in a "
                   "larger question and reasons from the tension to a rule. Situating and holding the tension is "
                   "the move." + REMEMBER +
                   "When you build your own, put the parts in that order, then run the check before you submit.")),
        Slot("MODEL", "discrimination", "Which synthesis is complex?",
             ref="", labeled_grade_c=True, bank="water_competing_uses",
             body=("You have watched a flat synthesis gain complexity. Now spot the target: which of these "
                   "closings is complex, and which are competent-but-flat weaves? "
                   "(A) Read together, the sources make scarcity one case of outrunning a shared resource, and "
                   "because cutting either use starves the other, the set supports a rationing rule that ranks "
                   "the two uses over any plain call to use less.  "
                   "(B) Read together, the sources show water is scarce and that power plants and farms both draw "
                   "heavily on it, and since each source repeats that basic point, the whole set adds up to one "
                   "clear takeaway: the country should use less water.  "
                   "(C) Read together, the sources each explain a different way water gets used, and after laying "
                   "out what all three say in turn, the essay concludes that water clearly matters a great deal "
                   "to the country and should be managed with care.  "
                   "(D) Read together, the sources raise the larger question of how a society should share a "
                   "strained resource, and since power and farming each have a real claim on the water, the essay "
                   "concludes that the country must weigh both needs and balance them carefully going forward. "
                   "Correct: A situates the woven claim in a larger question and reasons from the sources' "
                   "conflict to a real position; B and C land flat on 'use less' and 'water matters', and D names "
                   "the question but dissolves the tension into a vague call to balance both needs, so none of B, "
                   "C, or D reaches complexity."),
             choices=[
                 {"id": "A", "text": "Read together, the sources make scarcity one case of outrunning a shared resource, and because cutting either use starves the other, the set supports a rationing rule that ranks the two uses over any plain call to use less.",
                  "correct": True,
                  "why": "Correct. This situates the woven claim in a larger question (outrunning a shared resource) and reasons from the sources' conflict to a real position (a rationing rule). That is the complexity move."},
                 {"id": "B", "text": "Read together, the sources show water is scarce and that power plants and farms both draw heavily on it, and since each source repeats that basic point, the whole set adds up to one clear takeaway: the country should use less water.",
                  "correct": False,
                  "why": "This weaves the sources but lands flat on 'use less'. It names no larger question and treats the conflict as if it were not there, so it is competent, not complex."},
                 {"id": "C", "text": "Read together, the sources each explain a different way water gets used, and after laying out what all three say in turn, the essay concludes that water clearly matters a great deal to the country and should be managed with care.",
                  "correct": False,
                  "why": "This summarizes each source in turn and ends on 'water matters'. Summary is not synthesis, and 'matters' is flat, so it reaches no complexity."},
                 {"id": "D", "text": "Read together, the sources raise the larger question of how a society should share a strained resource, and since power and farming each have a real claim on the water, the essay concludes that the country must weigh both needs and balance them carefully going forward.",
                  "correct": False,
                  "why": "This one does name the larger question, but then it dissolves the tension into a vague 'balance both needs'. Because cutting either use starves the other, 'balance' is not a real position; holding the tension means reasoning to a rule that ranks the uses, so this stays flat."},
             ]),
        Slot("MODEL", "predict_the_fix", "What lifts this synthesis to real complexity?",
             bank="water_competing_uses",
             body=("Diagnose before the reveal. A draft correctly weaves the three sources into one argument and "
                   "weights them, but ends on a plain 'the country should conserve water.' Which single change "
                   "would most likely reach real complexity? "
                   "(A) situate the woven claim in the broader question it is one case of and reason from the "
                   "tension the sources create toward a real position  "
                   "(B) bring in a fourth source and weave it alongside the other three so the finished argument "
                   "rests on more evidence than the set had before  "
                   "(C) summarize each of the three sources more fully so the reader sees the whole point that "
                   "every source makes before the woven claim finally arrives  "
                   "(D) restate the conservation call more strongly at the close, using firmer, more forceful "
                   "wording so the essay ends on a clearer demand to use less water"),
             feedback=("Correct: A. A correct weave that ends flat is competent, not complex. The lift "
                       "situates the claim in the larger question and reasons from the sources' tension to a "
                       "real position (a rule). A fourth source (B), fuller summaries (C), or a stronger "
                       "restatement (D) do not add complexity. There is no clock, so there is time to plan "
                       "the frame before you draft.")),

        # ===== SUPPORTED: plan the sophisticated synthesis (multi_paragraph) - the frame is the top scaffold =====
        Slot("SUPPORTED", "production_frq", "Plan the complex synthesis",
             ref="", bank="water_competing_uses", rubric_ref="rc.ap", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Plan a complex synthesis of the water set before you draft a word of it.",
                 setapart_block=setapart("Fill in this plan:",
                                         "Woven claim: ______ (and which source carries each point). Broader question it is one case of: ______. Tension the sources create: ______. Position I defend: ______."),
                 closer="Write the ONE argument the set builds and which source carries each point, then the "
                        "broader question it is one case of and the tension the sources create, then the "
                        "position you defend within it. This plan is what you will build the essay from.")),
        # ===== INDEPENDENT: build the whole synthesis from the plan (essay ceiling) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "BUILD: write the complex synthesis",
             ref="", bank="water_competing_uses", rubric_ref="rc.ap", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now, build the whole synthesis from your plan.",
                 closer="Write a complete synthesis essay on the water set: an introduction that states the "
                        "woven claim and situates it in the broader question, body paragraphs organized by point "
                        "that weave and weight the sources and hold their tension, and a conclusion that defends "
                        "a position the tension forces. Then run the depth-and-significance check and fix any part that fails. "
                        "Situating a woven claim and holding the sources' tension is what every genuinely "
                        "complex synthesis is built on, and you are ready to do it cold. Take the time you "
                        "need.")),

        # DIAGNOSIS = self-revision: reread your OWN just-written draft and run the three-question check on it,
        # fixing any line that fails. Same taught source (load balance). Self-contained: the checklist is the
        # scaffold and the grader scores the diagnosis within the item.
        Slot("MODEL", "diagnosis_frq", "Check your own synthesis: woven, situated, tension held?",
             ref="", bank="water_competing_uses", scored=True,
             body=frq_prompt(
                 intro="Reread the essay you just wrote. Run this checklist on YOUR draft and fix any line that fails.",
                 checklist_block=checklist(title="Check your own draft, row by row:", rows=[
                     ("Is there ONE woven argument with sources weighted?", "If it just says the sources agree (like 'all three say water matters'), that is summary, not a weave with weights. Assign each point to the source that carries it and weight them."),
                     ("Is the claim situated in a larger question?", "If the claim stands alone with no larger frame, name the broader question this claim is one case of, so the reader sees the stakes."),
                     ("Is the tension held rather than flattened?", "If it ends flat (like a plain call to 'conserve'), name the conflict (cutting either use starves the other) and reason from it to a real position."),
                 ]),
                 closer="For every row that fails on your draft, name the gap in one line and make the fix. "
                        "Finish by naming the larger question your synthesis answers.")),
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
