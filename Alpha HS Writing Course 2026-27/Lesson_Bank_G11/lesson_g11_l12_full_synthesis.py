"""
lesson_g11_l12_full_synthesis.py  -  G11 KC C.11.02, ARCHETYPE T8: CROSS-SOURCE-SYNTHESIS (WEAVE, ceiling essay). V3.1.

G11 course L12 (Unit 3, intro), rebuilt to the v3.1 build spec (hand-authored). Teaching point (KEPT): do full
synthesis - draw three or more sources into ONE argument the set builds that no source states alone, rather than
surveying the sources one by one. KC C.11.02. SYNTHESIS-TIER binds the teaching synthesis set
(lesson_synth_water_uses, 3 sources): taught SYNTH-LESSON-0001 -> transfer SYNTH-SET-0001 (cold renewable-grid set).

Preserved EXACTLY from the prior L12: id="ACC-W1112-L-G11-C1102-0012", lesson_type=8, kc="C.11.02",
mnemonic_status="proposal", unit=G11 U3, the bound stimuli, and the production unit= values (multi_paragraph).

V3.1 changes vs the prior L12 (the two failing gates + the spine polish):
  1. FIXED the leaked internal label: the discrimination no longer says "a Grade-C design bet we label as a bet";
     it is a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}] (leaked_internal_label).
  2. FIXED the wall-of-text teach card: the 122-word prose block is now a ONE_IDEA callout + real <ul>/<ol> lists
     of the parts and the order of work (format_fidelity, and the v3.1 "parallel items as a list" rule).
  3. Deterministic FRQ + diagnosis prompts via frq_prompt/setapart/checklist (no "Step 1/2" prose, no "Scored on"
     chrome); coping-model before/after kept; the reusable synthesis check folded in at first use as a real <ol>
     REMEMBER box. Facts stay faithful to the bound USGS/EPA/EIA source set (no fabricated figures).
Own words, no fabricated figures, no em dashes. Passes all 23 lesson_contract gates + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Full synthesis is <strong>the whole set building ONE '
'argument</strong> that no single source states on its own. You do not tour the sources one by one; you connect '
'them so their combination forces a conclusion.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: synthesized, or surveyed?</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, reread your claim and ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Is there ONE argument the whole set builds, or just a tour of the sources?</li>'
'<li style="margin:2px 0">Does the claim go beyond what any single source states on its own?</li>'
'<li style="margin:2px 0">Does it connect two or more sources, showing how their combination forces the point?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you submit.</div></div>')

# coping-model before/after: a survey (a tour of the three sources with no argument of its own) rebuilt into a
# synthesized claim that combines them. Contains BOTH a literal BEFORE and AFTER (content_depth). Figures trace
# to the bound set: scarcity from Source 1 (EPA 1 percent), power 41 percent (Source 2), farming 42 percent
# (Source 3). No named person (Timeback stateless rule).
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> surveys the three sources one by one</span>'
    '<p style="margin:8px 0 0;font-size:15px"><i>Draft:</i> Source 1 explains where the nation\'s water goes. '
    'Source 2 explains that power plants use a lot of water for cooling. Source 3 explains that farms use a lot '
    'of water for irrigation. All three sources are about water use.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">A tour of three sources with no argument of its own. '
    'It ends on "they are all about water," which is a topic, not a claim. Nothing is built from the set.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> rebuilt as one argument the whole set builds</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">SYNTHESIZED CLAIM (from the whole set)</span> "Because only about 1 percent of Earth\'s '
      'water is fresh and available (Source 1), yet cooling power plants and irrigating crops already draw about '
      '41 and 42 percent of the nation\'s water (Sources 2 and 3), a drying country cannot fully protect both '
      'giant uses at once and must decide which one to feed first."</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same three sources, but now they are connected: '
    'scarcity plus two near-equal demands forces a tradeoff conclusion that no single source states alone. '
    'Synthesized, not surveyed.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1102-0012", grade="9-10", lesson_type=8,
    unit="G11 U3 - Synthesis (full synthesis)",
    title="Draw the Whole Set Into One Argument",
    target=("Do full synthesis: draw three or more sources into ONE argument the set builds that no source "
            "states alone, rather than surveying the sources one by one. Written across a multi-source plan. "
            "Trait: Development (synthesis)."),
    acc_tags=["ACC.W.SRC.1", "CCSS.W.11-12.7"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.02", "sot": "icm course-G11.md L12",
                "taught_stimulus": "ACC-W1112-SYNTH-LESSON-0001",
                "transfer_stimulus": "ACC-W910-SYNTH-SET-0001",
                "playbook": "_phase2/playbook_T8_WEAVE.md",
                "template": "v3.1 spine; SYNTHESIS-TIER binds full 3+ source sets; UNTIMED (no Timeback timer).",
                "one_idea": "Full synthesis is the whole set building ONE argument no single source states alone.",
                "one_reminder": "Synthesized-check: one argument the set builds? beyond any single source? connects two or more?",
                "version_note": ("V3.1 rebuild of L12. FIXED the two failing gates on the prior version: removed "
                                 "the leaked internal label ('a Grade-C design bet we label as a bet') from the "
                                 "discrimination and moved it to explicit choices=[]; broke the 122-word wall-of-"
                                 "text teach card into a ONE_IDEA callout + real <ul>/<ol> lists (format_fidelity). "
                                 "Deterministic frq_prompt/setapart/checklist bodies (no 'Step 1/2' prose, no "
                                 "'Scored on' chrome); coping-model before/after + the synthesis check folded in "
                                 "at first use. Preserved id, type 8, kc C.11.02, mnemonic_status=proposal, bound "
                                 "stimuli, and the production unit= values (multi_paragraph). Figures faithful to "
                                 "the bound USGS/EPA/EIA source set (no fabrication)."),
                "council": ("T8/WEAVE G11 full-synthesis intro: introduces X3 (3+ sources into one argument the "
                            "set builds). synthesized-vs-surveyed discrimination labeled Grade-C in code only. "
                            "WEAVE=proposal.")},
    fade_ledger_moves=["full-synthesis", "one-argument-the-set-builds"],
    slots=[
        # ===== TEACH: the one idea + what synthesis is (as a list), then the order of work (as a list) =====
        Slot("TEACH", "teach_card", "The one idea: the whole set builds one argument",
             body=(ONE_IDEA +
                   "To synthesize means to combine several sources into one argument, not to report them in turn. "
                   "Here is what that looks like and what it is not:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Synthesis</strong> means combining the sources so their "
                   "combination yields a conclusion: because one source establishes a fact and others show its "
                   "consequences, a claim follows that none of them states on its own.</li>"
                   "<li style=\"margin:4px 0\"><strong>Surveying</strong> is when you tour the sources one at a "
                   "time, 'Source 1 says X, Source 2 says Y, Source 3 says Z,' and stop at a topic instead of an "
                   "argument.</li>"
                   "<li style=\"margin:4px 0\"><strong>The set does the work</strong>: the argument comes from "
                   "how the sources connect, so you must draw on two or more of them together, not lean on one.</li>"
                   "</ul>"
                   "The trap is the survey. Goal today: state one argument the whole set builds, drawing on the "
                   "sources together.")),
        Slot("TEACH", "teach_card", "How to synthesize a set, step by step",
             body=("Here is the order of work. Follow it and the set turns into one argument instead of a tour:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>READ ALL of it</strong>: read every source and note what "
                   "each one establishes.</li>"
                   "<li style=\"margin:4px 0\"><strong>FIND THE LINK</strong>: ask what the sources, put "
                   "together, force that none states alone (a tension, a tradeoff, a consequence).</li>"
                   "<li style=\"margin:4px 0\"><strong>STATE ONE CLAIM</strong>: write the conclusion the "
                   "combination builds, naming the sources it draws on.</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: reread and ask, is this one argument the "
                   "set builds, does it go beyond any single source, and does it connect two or more of them?</li>"
                   "</ol>"
                   "You are combining the sources into one claim, in this order, not summarizing them one by one.")),
        Slot("TEACH", "stimulus_display", "Read the source set: competing water uses (3 sources)",
             ref="ACC-W1112-SYNTH-LESSON-0001", bank="water_competing_uses",
             body=("Read this three-source set on competing water uses (the water that cools power plants vs the "
                   "water that irrigates crops vs the scarcity of usable fresh water). Because your job is full "
                   "synthesis, read all three and ask what conclusion their combination forces that none states "
                   "alone. The texts stay on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + the check tool, then the check items =====
        Slot("MODEL", "annotated_before_after", "Watch a survey become a synthesis",
             bank="water_competing_uses",
             body=("Here is the difference between touring the sources and synthesizing them. Read the BEFORE, "
                   "then the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE lists what each source says and stops at a topic. The AFTER connects scarcity to "
                   "two near-equal demands and lands a conclusion none of the sources states alone. Synthesize "
                   "the set, do not survey it, is the move." + REMEMBER +
                   "When you build your own, follow the order, then run the check before you submit.")),
        Slot("MODEL", "discrimination", "Which one synthesizes the set?",
             ref="", labeled_grade_c=True, bank="water_competing_uses",
             body=("You have watched a survey become a synthesis. Now spot the target: which claim SYNTHESIZES "
                   "the set (one argument the whole set builds), and which three do not? "
                   "(A) Because fresh water is scarce while cooling power plants and irrigating crops each already claim over forty percent of the supply, a drying country cannot protect both giant uses and must decide which one to feed first.  "
                   "(B) Source 1 lays out where the nation's water goes overall, Source 2 describes how thermoelectric power plants draw water for cooling, and Source 3 describes how farms draw water for irrigation, and all three of the sources are clearly about water use.  "
                   "(C) The first source gives a broad overview of national water use, the second source is all about electricity and the water it needs to run, and the third source is all about farming and the water that it needs, adding more facts each time.  "
                   "(D) Because Source 3 shows irrigation alone already draws about 42 percent of the nation's water, farms are the country's biggest water problem and should be the first use forced to cut back. "
                   "Correct: A. It connects scarcity to two near-equal demands and lands a tradeoff conclusion "
                   "the set builds that no single source states. B and C walk through the sources one at a time "
                   "and stop at the topic of water, so nothing is built from the set; D makes an argument but "
                   "rests on one source instead of drawing the set together."),
             choices=[
                 {"id": "A", "text": "Because fresh water is scarce while cooling power plants and irrigating crops each already claim over forty percent of the supply, a drying country cannot protect both giant uses and must decide which one to feed first.",
                  "correct": True,
                  "why": "Correct. It combines what the sources establish (scarcity plus two near-equal demands) into one conclusion the set builds that no single source states."},
                 {"id": "B", "text": "Source 1 lays out where the nation's water goes overall, Source 2 describes how thermoelectric power plants draw water for cooling, and Source 3 describes how farms draw water for irrigation, and all three of the sources are clearly about water use.",
                  "correct": False,
                  "why": "This surveys the set. It tours the three sources one at a time and stops at a topic ('all about water use'), which is not an argument."},
                 {"id": "C", "text": "The first source gives a broad overview of national water use, the second source is all about electricity and the water it needs to run, and the third source is all about farming and the water that it needs, adding more facts each time.",
                  "correct": False,
                  "why": "This also surveys the set. It adds facts source by source without connecting them, so the sources never combine into one claim."},
                 {"id": "D", "text": "Because Source 3 shows irrigation alone already draws about 42 percent of the nation's water, farms are the country's biggest water problem and should be the first use forced to cut back.",
                  "correct": False,
                  "why": "This makes an argument, but it leans on a single source (Source 3) and never draws the set together, so it fails the check that a synthesis must connect two or more sources."},
             ]),
        Slot("MODEL", "predict_the_fix", "What turns this survey into synthesis?",
             bank="water_competing_uses",
             body=("Diagnose before the reveal. A draft reads: 'The first source is about scarcity. The second "
                   "is about cooling water. The third is about irrigation. They all relate to water use.' Which "
                   "single move would most improve it? "
                   "(A) connect the sources into ONE argument the set builds that no single source states alone  "
                   "(B) add a fourth outside source so the set brings in even more separate information about water  "
                   "(C) summarize each of the three sources much more fully so that no single detail gets left out  "
                   "(D) say which one of the three sources is the most interesting overall and explain why it stands out"),
             feedback=("Correct: A. The draft surveys the three sources and only says 'they all relate to water,' "
                       "which is a topic, not an argument. The fix synthesizes: because scarcity meets two "
                       "near-equal demands, a tradeoff conclusion follows that none of the sources states. A "
                       "fourth source (B), fuller summaries (C), or ranking them (D) do not build one argument "
                       "from the set.")),

        # ===== SUPPORTED: draw the set into one claim with a fill-in FRAME (the highest-value scaffold) =====
        Slot("SUPPORTED", "production_frq", "Draw the set into one argument",
             ref="", bank="water_competing_uses", rubric_ref="rc.ap", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Using all three sources in the set, draw them into ONE claim the set builds.",
                 setapart_block=setapart("Fill in this frame:",
                                         "Because ______ [what one source establishes] and ______ [what the "
                                         "others show], ______ [the conclusion the set forces that no single "
                                         "source states alone]."),
                 closer="Write one synthesized claim that draws across the set, naming the sources it uses. It "
                        "should be one argument the combination builds, not a tour of the sources one by one.")),
        # DIAGNOSIS = check-and-fix on a PROVIDED weak claim (not a fresh production), so it does not repeat the
        # supported write. Same taught source (load balance). Scaffolded by the synthesis check run on the draft.
        Slot("MODEL", "diagnosis_frq", "Check your claim: synthesized, or surveyed?",
             ref="", bank="water_competing_uses", scored=True,
             body=frq_prompt(
                 intro="First watch the check run on a weak draft, then run it on a fresh claim of your own.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "Source 1 says one thing about water, source 2 says another, and source "
                                         "3 says another. They all relate to water use.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Is there ONE argument the set builds, or a tour?", "A tour. It walks through the sources and stops at 'they all relate to water.' Build one claim the combination forces."),
                     ("Does the claim go beyond any single source?", "No. It only restates that each source is about water. Make it a conclusion no single source states."),
                     ("Does it connect two or more sources?", "No. The sources sit side by side, unlinked. Connect scarcity to the competing demands so they combine."),
                 ]),
                 closer="Now write a fresh synthesized claim from the set, run the same three checks, and fix any "
                        "that fail. Finish by naming the conclusion the set builds that no single source states.")),

        # ===== INDEPENDENT: synthesize the set with no frame + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Synthesize the set on your own",
             ref="", bank="water_competing_uses", rubric_ref="rc.ap", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="On your own now, with no frame.",
                 closer="Using the three-source set, write ONE synthesized argument the set builds that no single "
                        "source states alone. Then run the synthesis check and fix any part that fails. Drawing "
                        "a whole set into one argument is what every real synthesis is built on, and you are "
                        "ready to do it cold. Take the time you need.")),

        # ===== TRANSFER: same synthesize-the-set move, a NEW source set, partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source set: a renewable grid (4 sources)",
             ref="ACC-W910-SYNTH-SET-0001", bank="renewable_grid_synthesis",
             body=("Read this new four-source set on whether the United States grid can run mostly on renewable "
                   "energy. Because your job is full synthesis, read all of it and ask what conclusion the set "
                   "forces that no single source states alone. The texts stay on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Synthesize a NEW set",
             ref="", bank="renewable_grid_synthesis", rubric_ref="rc.ap", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="New set. The question: can the United States grid run mostly on renewable energy?",
                 closer="Using the renewable-grid sources, write ONE synthesized argument the set builds that no "
                        "single source states alone. Same synthesize-the-set move as the water set, a new topic. "
                        "Do not survey the sources. Run the synthesis check before you submit.")),
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
