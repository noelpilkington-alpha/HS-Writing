"""
lesson_g12_l13_interleaved_pair.py  -  G12 KC C.12.02, ESSAY-ASSEMBLY (BUILD, ceiling essay). V3.1.

G12 course L13 (Unit 2, build), rebuilt to the v3.1 build spec (hand-authored). Teaching point (KEPT):
rehearse two different FRQ types back to back, re-naming each type and SWITCHING the move-set between them
(argument then synthesis), under a self-imposed budget, rather than carrying one move-set into the next
prompt. Interleaved retrieval (switching types) is the point. Delivery UNTIMED (no Timeback timer). Binds two
cold-to-G12 stimuli of different types: taught = WATERTRADEOFF (single-source argument on water for food vs
power); transfer = SYNTH-SET-0003 (five-source synthesis on water scarcity). Written at the essay ceiling.

Preserved EXACTLY from the prior L13: id="ACC-W910-L-G12-C1202-0013", lesson_type=7, kc="C.12.02",
mnemonic_status="proposal", unit, the bound stimuli (WATERTRADEOFF argument taught -> SYNTH-SET-0003 synthesis
transfer), and the teaching point (interleaved pair, re-name type + switch move-set).

V3.1 changes vs the prior L13 (the two failing gates + the spine polish):
  1. FIXED the leaked internal label: the discrimination no longer says "a Grade-C design bet we label as a
     bet"; it is a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}] and a "Correct:"
     tail outside the option text (leaked_internal_label / leaked_answer_cue).
  2. FIXED the wall-of-text teach card: the prose block is now a ONE_IDEA callout + a real <ul> list of the two
     move-sets and the trap (format_fidelity + the v3.1 "parallel items as a list" rule).
  3. Deterministic FRQ + diagnosis prompts via frq_prompt/setapart/checklist (no "Step 1/2" prose, no "Scored
     on ..." chrome); coping-model before/after kept (literal BEFORE + AFTER); the switch check folded in at the
     point of first use as a real <ol> REMEMBER box.
Own words, no fabricated figures (facts trace to the bound USGS/USDA sources), no em dashes. Passes all 23
lesson_contract gates + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">On the real exam two prompts of different kinds come '
'back to back. Before you plan the second one, <strong>re-name its type and switch the move-set</strong>, or '
'the moves from the first prompt bleed into the second.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the switch check</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Between two back-to-back prompts, ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Have I named the next prompt from its tell (a source set is a synthesis; a general question is an argument)?</li>'
'<li style="margin:2px 0">Do my planned moves match that type, not the last prompt I just wrote?</li>'
'<li style="margin:2px 0">For a synthesis, am I weaving one argument from the sources and weighting them, not stating a personal opinion?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you plan.</div></div>')

# coping-model before/after: a writer finishes the argument prompt, then opens the synthesis prompt and starts
# it the SAME way (personal opinion + own examples). A quick check catches it, and the writer switches to
# weave-and-weight. Contains BOTH a literal BEFORE and AFTER (content_depth). Facts trace to the bound sources.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> first try: carries the argument moves into the synthesis</span>'
    '<p style="margin:8px 0 0;font-size:15px">Just off a strong argument prompt, the writer opens the synthesis '
    'prompt the same way: "In my opinion the country should protect its farms first, and I have seen how much a '
    'harvest means to a family." No source is named, nothing is woven or weighted.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">Running the switch check: the next prompt is a '
    'synthesis, but the planned moves are the argument moves (personal position, own examples). The move-set '
    'bled forward. Fix it before planning.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> second try: re-named as synthesis, move-set switched</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">SWITCH THE MOVE-SET</span> "The USGS source shows irrigation water mostly leaves the '
      'supply for good, while the USDA source shows those same irrigated farms produce more than half of U.S. '
      'crop value. Weighing the two, the nation should protect food water but tie it to strict efficiency '
      'rules." The sources are woven and weighted, not a personal opinion.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same writer, next prompt re-named as a synthesis '
    'and the moves switched to weave-and-weight. Re-name the type, switch the move-set: that is what interleaved '
    'practice builds.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G12-C1202-0013", grade="9-10", lesson_type=7,
    unit="G12 U2 - Interleaved FRQ pair (switch move-sets)",
    title="Switch Move-Sets Between Two Different FRQs",
    target=("Rehearse two different FRQ types back to back, re-naming the type and switching the move-set "
            "between them (argument then synthesis), under a self-imposed budget, rather than carrying one "
            "move-set into the next prompt. Delivery untimed. Written at the essay. Trait: task analysis, "
            "Development, and process."),
    acc_tags=["ACC.W.ARG.1", "ACC.W.SRC.1", "ACC.W.PROD.4", "CCSS.W.11-12.1", "CCSS.W.11-12.7"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.12.02", "sot": "icm course-G12.md L13",
                "taught_stimulus": "ACC-W910-ARG-LESSON-WATERTRADEOFF",
                "transfer_stimulus": "ACC-W910-SYNTH-SET-0003",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": ("v3.1 spine; ESSAY-TIER binds two cold-to-G12 stimuli of different types; "
                             "interleaved retrieval (switch move-sets), delivery UNTIMED (no Timeback timer)."),
                "one_idea": "Between two back-to-back prompts, re-name the type and switch the move-set, or the moves bleed.",
                "one_reminder": "Switch check: named the next prompt from its tell? moves match that type? for synthesis, weaving and weighting sources?",
                "version_note": ("V3.1 rebuild of L13. FIXED the leaked internal label (removed 'a Grade-C "
                                 "design bet we label as a bet' from the discrimination; moved options to "
                                 "choices=[] with the reveal in a 'Correct:' tail). Broke the wall-of-text teach "
                                 "card into a ONE_IDEA callout + a real <ul> list (format_fidelity). "
                                 "Deterministic frq_prompt/setapart/checklist bodies (no 'Step 1/2' prose, no "
                                 "'Scored on' chrome); coping-model before/after kept; switch check folded in at "
                                 "first use as an <ol> REMEMBER box. Preserved id, type 7, kc C.12.02, "
                                 "mnemonic_status=proposal, unit, bound stimuli, and the interleaved teaching "
                                 "point; unit ladder SUPPORTED=multi_paragraph -> INDEPENDENT/TRANSFER=essay."),
                "review_provenance": "built to the G9 L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["interleaved-frq-pair", "re-name-type-and-switch-moves"],
    slots=[
        # ===== TEACH: the one idea + the two move-sets (as a list); define thesis + synthesis here =====
        Slot("TEACH", "teach_card", "The one idea: re-name the type, switch the move-set",
             body=(ONE_IDEA +
                   "Practicing one type at a time lets a move-set bleed: you finish an argument, then start the "
                   "next prompt the same way and forget it is a different task. Between prompts, name the type "
                   "from its tell and switch to that type's moves:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Argument</strong> (a general question, no source set): "
                   "take a position and carry it with specific examples and reasons.</li>"
                   "<li style=\"margin:4px 0\"><strong>Synthesis</strong> (a set of sources): synthesis means "
                   "building one argument out of several sources, weaving them together and weighting which "
                   "ones matter most, instead of stating a personal opinion.</li>"
                   "<li style=\"margin:4px 0\"><strong>The trap is momentum</strong>: running the last prompt's "
                   "moves on the next one.</li></ul>"
                   "Each type still needs a thesis, which is a one-sentence claim that states the position your "
                   "essay defends. Delivery here has no clock. Goal today: rehearse two different prompts, "
                   "re-naming the type and switching the move-set each time.")),
        Slot("TEACH", "stimulus_display", "The first prompt: water for food or power? (argument)",
             ref="ACC-W910-ARG-LESSON-WATERTRADEOFF", bank="water_tradeoff",
             body=("Read this first prompt, a general argument on protecting scarce water for growing food or "
                   "for generating power. Name its type (an argument) and its moves (a position carried by "
                   "examples), then plan. After it, you will switch to a different prompt type. The text stays "
                   "on screen while you work.")),

        # ===== MODEL (before the discrimination): coping-model before/after + the switch check =====
        Slot("MODEL", "annotated_before_after", "Watch a bled move-set become a clean switch",
             bank="water_tradeoff",
             body=("Here is a bled move-set caught and rebuilt into a clean switch between prompt types. Read "
                   "the BEFORE, then the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE carries the argument moves forward; the AFTER re-names the type and switches to "
                   "weave-and-weight. Re-name the type, switch the move-set." + REMEMBER +
                   "Run this switch check between your two prompts before you plan the second one.")),
        Slot("MODEL", "discrimination", "Which approach switches the move-set?",
             ref="", labeled_grade_c=True, bank="water_tradeoff",
             body=("You have watched a bled move-set become a clean switch. Now spot the target: which approach "
                   "SWITCHES the move-set for the second prompt, and which lets it BLEED from the first? "
                   "(A) After the argument prompt, name the next one as a synthesis from its source set, then "
                   "weave one argument from those sources and weight them before you plan.  "
                   "(B) After the argument prompt, open the next one the very same way, giving a personal "
                   "opinion backed by examples drawn from your own life and experience.  "
                   "(C) After the argument prompt, reuse that essay's exact thesis and carry the identical "
                   "position straight into the next prompt without reading its sources or naming its type. "
                   "Correct: A switches; B and C bleed. (A) re-names the type and moves to weave-and-weight; "
                   "(B) carries the argument moves forward; (C) carries the whole position forward."),
             choices=[
                 {"id": "A", "text": "After the argument prompt, name the next one as a synthesis from its source set, then weave one argument from those sources and weight them before you plan.",
                  "correct": True,
                  "why": "Correct. This re-names the next prompt from its tell (a source set) and switches to the synthesis move-set, weaving and weighting the sources."},
                 {"id": "B", "text": "After the argument prompt, open the next one the very same way, giving a personal opinion backed by examples drawn from your own life and experience.",
                  "correct": False,
                  "why": "This carries the argument moves forward. A personal opinion plus own examples is the argument move-set, not the synthesis one the source set calls for."},
                 {"id": "C", "text": "After the argument prompt, reuse that essay's exact thesis and carry the identical position straight into the next prompt without reading its sources or naming its type.",
                  "correct": False,
                  "why": "This carries the whole position forward and never names the new type. Without reading the sources, there is nothing to weave or weight."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this interleaved pair most need?",
             bank="water_tradeoff",
             body=("Predict before the reveal. A writer has just finished a strong argument prompt. They open "
                   "the next prompt, a synthesis built on a source set, and begin by stating a personal opinion "
                   "and citing examples from their own life. Which single change would most improve the second "
                   "essay? "
                   "(A) re-name the prompt as a synthesis and switch to weaving one argument from the sources, weighting each  "
                   "(B) state the personal opinion far more forcefully and back it with stronger reasons of your own  "
                   "(C) add several more personal examples and everyday stories drawn from your own life so the opinion is developed in fuller detail  "
                   "(D) reuse the argument thesis word for word and carry that same position straight into this essay"),
             feedback=("Correct: A. The moves bled from the argument prompt; the fix re-names the type and "
                       "switches to weave-and-weight the sources. A more forceful opinion (B), more personal "
                       "examples (C), or reusing the thesis (D) all keep the wrong move-set.")),

        # ===== SUPPORTED: plan the argument prompt + flag the switch (multi_paragraph) - frame scaffold =====
        Slot("SUPPORTED", "production_frq", "Plan the argument prompt, then flag the switch",
             ref="", bank="water_tradeoff", rubric_ref="rc.ap", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Plan the first prompt (the water argument) before you write, and flag the switch to the "
                       "next prompt.",
                 setapart_block=setapart("Fill in this plan:",
                                         "Type: ______ (name it). Moves: ______. Thesis: ______ (my position). Switch flag: the next prompt is a ______, so before planning it I will switch to ______."),
                 closer="Name this prompt's type and its moves (a position carried by examples), write a "
                        "one-line thesis, then write the switch flag reminding yourself the next prompt is a "
                        "different type you will re-name before planning.")),
        # DIAGNOSIS = self-revision: reread your OWN just-written draft and run the 3-question switch check on it,
        # fixing any line that fails. Same taught bank (load balance). Self-contained: the checklist is the
        # scaffold and the grader scores the diagnosis within the item.
        Slot("MODEL", "diagnosis_frq", "Run the switch check on your own draft",
             ref="", bank="water_tradeoff", scored=True,
             body=frq_prompt(
                 intro="Reread the essay you just wrote. Run this checklist on YOUR draft and fix any line that fails.",
                 checklist_block=checklist(title="Run the switch check:", rows=[
                     ("Is the next prompt's type named from its tell?", "No. A source set signals a synthesis. Name it before planning."),
                     ("Do the planned moves match that type, not the last one?", "No. The argument moves (personal position, own examples) are carried over. Switch to weaving and weighting the sources."),
                     ("For a synthesis, is one argument built from the sources and weighted?", "No. Add the weave-and-weight move the synthesis needs."),
                 ]),
                 closer="For every line that fails on your draft, name what is off in one sentence and make the "
                        "fix. Finish by naming the new move-set you will switch to for the synthesis prompt.")),

        # ===== INDEPENDENT: rehearse the first prompt end to end (essay ceiling) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Rehearse the first prompt (argument)",
             ref="", bank="water_tradeoff", rubric_ref="rc.ap", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now. Under your own budget, rehearse the first prompt end to end.",
                 closer="Write a complete argument essay on the water trade-off: a thesis that takes a "
                        "defensible position, body paragraphs that carry it with specific examples, and a "
                        "conclusion that holds the tension. There is no platform timer. Switching the move-set "
                        "between two back-to-back prompts is what every real exam pair is built on, and you are "
                        "ready to do it cold. When you finish, note that the next prompt is a synthesis and you "
                        "will switch move-sets.")),
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
