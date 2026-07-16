"""
lesson_g11_l13_woven_synthesis.py  -  G11 KC C.11.02, ARCHETYPE T8: CROSS-SOURCE-SYNTHESIS (WEAVE, ceiling essay). V3.1.

G11 course L13 (Unit 3, guided), rebuilt to the v3.1 build spec (hand-authored). Teaching point (KEPT): at three
or more sources, organize by POINT with several sources meeting on each (woven), rather than by source with a
paragraph per source (source-by-source), written across a multi-source plan. KC C.11.02. Trait: Development
(synthesis). This is a SYNTHESIS-TIER lesson that recycles the G11 synthesis stack.

Preserved EXACTLY from the current L13: id="ACC-W1112-L-G11-C1102-0013", lesson_type=8, kc="C.11.02",
mnemonic_status="proposal", unit, the bound stimuli (SYNTH-LESSON-0001 water taught -> SYNTH-SET-0002 AI-workforce
transfer), and every production_frq unit= value (all multi_paragraph, within the T8 essay ceiling).

V3.1 changes vs the prior L13 (the two failing gates + the spine polish):
  1. FIXED the leaked internal labels: the discrimination no longer says "signature error", "Grade-C", or
     "design bet"; it is a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}]
     (leaked_internal_label). labeled_grade_c stays True in CODE only.
  2. FIXED the wall-of-text teach card: the prose block is now a ONE_IDEA teal callout + a real <ul> list of
     the two shapes, plus a second TEACH card with the order of work as an <ol> (format_fidelity).
  3. Deterministic FRQ + diagnosis prompts via frq_prompt/setapart/checklist (no "Step 1/2" prose, no "Scored
     on ..." chrome); the coping-model before/after (First try -> check -> Final) is kept with a LITERAL BEFORE
     and AFTER; the reusable check tool (the 3-question weave check) is folded in as a real <ol> REMEMBER box.
Own words, faithful to the bound USGS/EPA/EIA source facts, no fabricated figures, no em dashes. Passes all 23
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
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A woven synthesis is organized by <strong>POINT</strong>, '
'not by source: each paragraph makes one claim and pulls in whichever sources bear on it, so <strong>several '
'sources meet on the same point</strong>. If your paragraphs are named after the sources, you are touring them, '
'not weaving them.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the weave check</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit a paragraph, ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Is this paragraph built around a POINT, not a single source?</li>'
'<li style="margin:2px 0">Do at least two sources meet on that point?</li>'
'<li style="margin:2px 0">Have I shown how the sources connect (corroborate, qualify, or answer each other), not just listed them?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you submit.</div></div>')

# coping-model before/after: a writer's FIRST try tours the sources (a paragraph per source), runs the weave
# check, catches the source-tour, and rebuilds it woven-by-point in the FINAL try. Contains BOTH a literal
# BEFORE and AFTER (content_depth). Figures are faithful to the bound water set (USGS/EPA).
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> First try: a paragraph per source (a source tour)</span>'
    '<p style="margin:8px 0 0;font-size:15px">Paragraph 1: Source 1 says the country withdraws about 322 billion '
    'gallons of water a day. Paragraph 2: Source 2 says cooling the power plants took about 41 percent of that. '
    'Paragraph 3: Source 3 says irrigation took about 42 percent.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">Writer runs the weave check: "Is each paragraph built '
    'around a point, or around a source?" Around a source. Three sources, three boxes, and they never meet. That '
    'is a survey, not a synthesis.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> Final try: one point, three sources meeting on it</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">POINT (sources meet here)</span> The scarcity is what turns two ordinary demands into a '
      'genuine conflict: because Source 1 reports that only about 1 percent of Earth\'s water is available for '
      'human use, the near-equal draws in Source 2 (about 41 percent for cooling) and Source 3 (about 42 percent '
      'for irrigation) cannot both be met in a dry year, so all three meet on the single claim that a drying '
      'country must ration between two essential uses.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same facts, but now the paragraph is built around one '
    'point, and three sources connect on it. Woven, not toured.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1102-0013", grade="9-10", lesson_type=8,
    unit="G11 U3 - Synthesis (woven vs source-by-source at scale)",
    title="Weave the Sources, Do Not Tour Them",
    target=("At three or more sources, organize by POINT with several sources meeting on each (woven), rather "
            "than by source with a paragraph per source (source-by-source). Written across a multi-source "
            "plan. Trait: Development (synthesis)."),
    acc_tags=["ACC.W.SRC.1", "CCSS.W.11-12.7"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.02", "sot": "icm course-G11.md L13",
                "taught_stimulus": "ACC-W1112-SYNTH-LESSON-0001",
                "transfer_stimulus": "ACC-W910-SYNTH-SET-0002",
                "playbook": "_phase2/playbook_T8_WEAVE.md",
                "template": "v3.1 spine; SYNTHESIS-TIER binds full 3+ source sets; UNTIMED (no Timeback timer).",
                "one_idea": "A woven synthesis is organized by POINT, not by source: several sources meet on each point.",
                "one_reminder": "Weave check: built around a POINT (not one source)? do >=2 sources meet on it? are they connected, not just listed?",
                "version_note": ("V3.1 rebuild of L13. FIXED the two failing gates on the prior version: removed the "
                                 "leaked internal labels ('signature error', 'a Grade-C design bet we label as a bet') "
                                 "from the teach card + discrimination and moved the sort to explicit choices=[]; broke "
                                 "the 117-word wall-of-text teach card into a ONE_IDEA callout + real <ul> list plus an "
                                 "order-of-work <ol> (format_fidelity). Deterministic frq_prompt/setapart/checklist "
                                 "bodies; coping-model before/after kept; the weave check folded in as a REMEMBER <ol>. "
                                 "Preserved id, type 8, kc C.11.02, mnemonic_status=proposal, unit, bound stimuli, and "
                                 "every production_frq unit= value (all multi_paragraph, within the T8 essay ceiling)."),
                "council": ("T8/WEAVE G11 guided rung: woven-vs-source-by-source at 3+ sources (organize by point, "
                            "sources meet on each). Discrimination is Grade-C in code (labeled_grade_c=True) but no "
                            "internal label reaches the student. WEAVE=proposal."),
                "review_provenance": "built to the G9 L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["woven-by-point-at-scale", "sources-meet-on-each-point"],
    slots=[
        # ===== TEACH: the one idea + the two shapes (as a list), then the order of work (as a list) =====
        Slot("TEACH", "teach_card", "The one idea: organize by point, not by source",
             body=(ONE_IDEA +
                   "To synthesize means to combine several sources into one argument. At three or more sources "
                   "there are two shapes your paragraphs can take, and only one is real synthesis:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Source-by-source (the tour)</strong>: one paragraph reports "
                   "Source 1, the next reports Source 2, the next reports Source 3. Each source stays boxed in its "
                   "own block, and the reader never sees the sources meet.</li>"
                   "<li style=\"margin:4px 0\"><strong>Woven (by point)</strong>: each paragraph states one claim "
                   "and brings in whichever sources bear on it, so several sources corroborate, qualify, or answer "
                   "each other on the same point.</li></ul>"
                   "The quick test is what your paragraphs are named after: your claims (woven) or the sources "
                   "(the tour). The trap at scale is the source tour, and it caps your Development score.")),
        Slot("TEACH", "teach_card", "How to weave a point-organized paragraph",
             body=("Here is the order of work for one woven paragraph. Follow it and the sources meet instead of "
                   "lining up:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>NAME THE POINT</strong>: write the one claim this paragraph "
                   "will defend, before you touch a source.</li>"
                   "<li style=\"margin:4px 0\"><strong>GATHER THE SOURCES THAT BEAR ON IT</strong>: find the two "
                   "or three sources that speak to that point, not everything each source says.</li>"
                   "<li style=\"margin:4px 0\"><strong>CONNECT THEM</strong>: show how they relate on the point, "
                   "one corroborating another, or one qualifying or answering another, and cite each.</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: reread and ask whether the paragraph is "
                   "built around the point (not one source) and whether the sources actually meet on it.</li></ol>"
                   "You are organizing around a claim and letting the sources gather to it, in this order.")),
        Slot("TEACH", "stimulus_display", "Read the source set: competing water uses (3 sources)",
             ref="ACC-W1112-SYNTH-LESSON-0001", bank="water_competing_uses",
             body=("Read this three-source set on one question: when water grows scarce, should the country protect "
                   "the water that cools its power plants or the water that grows its crops? The three sources "
                   "appear in order below: Source 1 is \"Where the Nation's Water Goes,\" Source 2 is \"The Water "
                   "That Keeps the Lights On,\" and Source 3 is \"The Water That Grows the Food.\" Because your job "
                   "is woven synthesis, read for a single point that more than one source bears on, so they can "
                   "meet in one paragraph. The texts stay on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + the weave check, then the check items =====
        Slot("MODEL", "annotated_before_after", "Watch a source tour become woven by point",
             bank="water_competing_uses",
             body=("Here is a writer catching a source tour and rebuilding it. Read the BEFORE (the first try), then "
                   "the AFTER (the final try)." + BEFORE_AFTER_HTML +
                   " The BEFORE gives each source its own paragraph, so the sources never meet. The AFTER names one "
                   "point and lets three sources gather to it. Weaving by point is the move." + REMEMBER +
                   "When you build your own, name the point first, gather the sources to it, then run this check "
                   "before you submit.")),
        Slot("MODEL", "discrimination", "Which paragraph is woven by point?",
             ref="", labeled_grade_c=True, bank="water_competing_uses",
             body=("You have watched a source tour become woven. Now spot the target: which paragraph is WOVEN "
                   "(organized by a point that several sources meet on), and which two only tour the sources? "
                   "(A) The writer gives Source 1 a paragraph that reports everything it says, then hands Source 2 "
                   "a paragraph of its own, then lets Source 3 fill a third, so each source stays in a box.  "
                   "(B) The writer states one claim about scarcity, then brings Source 1, Source 2, and Source 3 "
                   "onto that single claim, so the three sources meet on the same point in one paragraph.  "
                   "(C) The writer opens with the source that has the biggest figure, then walks down through the "
                   "others in order of size, giving each its own separate summary in turn. "
                   "Correct: B is woven. (A) and (C) are both source tours, organized by source; (B) is organized "
                   "by a point that several sources meet on."),
             choices=[
                 {"id": "A", "text": "The writer gives Source 1 a paragraph that reports everything it says, then hands Source 2 a paragraph of its own, then lets Source 3 fill a third, so each source stays in a box.",
                  "correct": False,
                  "why": "This is a source tour. Each source keeps its own paragraph, so the sources never meet on a shared point."},
                 {"id": "B", "text": "The writer states one claim about scarcity, then brings Source 1, Source 2, and Source 3 onto that single claim, so the three sources meet on the same point in one paragraph.",
                  "correct": True,
                  "why": "Correct. This paragraph is built around a point, and three sources gather to it. That is weaving, not touring."},
                 {"id": "C", "text": "The writer opens with the source that has the biggest figure, then walks down through the others in order of size, giving each its own separate summary in turn.",
                  "correct": False,
                  "why": "Reordering the sources by size is still a tour. Each source gets its own summary, so they still do not meet on one point."},
             ]),
        Slot("MODEL", "predict_the_fix", "What turns this source tour into woven synthesis?",
             bank="water_competing_uses",
             body=("Diagnose before the reveal. A plan reads: 'P1: summarize the cooling-water source. P2: "
                   "summarize the farm-water source. P3: summarize the scarcity source.' Which single move would "
                   "most improve it? "
                   "(A) reorganize by POINT so each paragraph makes one claim and brings in the sources that bear on it  "
                   "(B) add a fourth paragraph that summarizes one more source so the essay covers more of the reading  "
                   "(C) make each source summary longer and more detailed so every paragraph reports its source in full  "
                   "(D) reorder the three source paragraphs so the strongest source comes first and the weakest one last"),
             feedback=("Correct: A. A paragraph-per-source plan is a survey no matter how it is arranged. The fix "
                       "reorganizes by point: for example, a scarcity paragraph that draws on all three sources, "
                       "then a tradeoff paragraph that does the same. A fourth source paragraph (B), longer "
                       "summaries (C), or reordering (D) all keep the source-by-source shape.")),

        # ===== SUPPORTED: write one woven paragraph from a frame (multi_paragraph) =====
        Slot("SUPPORTED", "production_frq", "Write one point-organized paragraph (framed)",
             ref="", bank="water_competing_uses", rubric_ref="rc.ap", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Write ONE woven paragraph on the water set. Plan the point before you write it.",
                 setapart_block=setapart("Fill in this frame:",
                                         "Point (my claim): ______. Sources that bear on it: Source ___, Source ___ (and Source ___). How they connect on the point: ______ (one corroborates, or one qualifies or answers the other)."),
                 closer="Now write the paragraph: state the point, bring in the two or three sources that bear on "
                        "it, and show how they connect, citing each. Aim for several sources meeting on ONE point, "
                        "not a paragraph per source.")),
        # DIAGNOSIS = watch the weave check run on a PROVIDED weak draft, then write fresh + run it (load balance,
        # same taught source). Scaffolded by the checklist run on the weak draft.
        Slot("MODEL", "diagnosis_frq", "Check a paragraph: woven by point, or by source?",
             ref="", bank="water_competing_uses", scored=True,
             body=frq_prompt(
                 intro="First watch the weave check run on a weak draft, then run it on your own.",
                 setapart_block=setapart("Weak draft to check:",
                                         "This paragraph is about Source 3. Source 3 says irrigation uses about 42 percent of the water. That is a lot of water for farms.", "red"),
                 checklist_block=checklist(title="Run the weave check:", rows=[
                     ("Is it built around a POINT, not one source?", "No. It is built around Source 3. Name a claim (for example, about scarcity or tradeoffs) and organize around it."),
                     ("Do at least two sources meet on that point?", "No. Only Source 3 appears. Bring in the sources that also bear on the claim."),
                     ("Are the sources connected, not just listed?", "No. It reports one figure. Show how the sources corroborate, qualify, or answer each other on the point."),
                 ]),
                 closer="Now write a fresh point-organized paragraph on the water set, run the same three checks, "
                        "and fix any that fail. Finish by naming the point your sources meet on.")),

        # ===== INDEPENDENT: weave a paragraph with no frame + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Weave by point on your own",
             ref="", bank="water_competing_uses", rubric_ref="rc.ap", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="On your own now, with no frame.",
                 closer="Write ONE point-organized paragraph on the water set: state a claim and support it with "
                        "several sources meeting on it, connected and cited. Then run the weave check and fix any "
                        "part that fails. Weaving sources onto one point is what every real synthesis is built on, "
                        "and you are ready to do it cold. Take the time you need.")),

        # ===== TRANSFER: same weave-by-point move, a NEW source set (AI + workforce), partitioned bank =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source set: AI and the workforce (sources)",
             ref="ACC-W910-SYNTH-SET-0002", bank="ai_workforce_synthesis",
             body=("Read this new source set on one question: how will artificial intelligence reshape the American "
                   "workforce? Because your job is woven synthesis, read for a point that several sources bear on, "
                   "so they can meet in one paragraph. The texts stay on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Weave by point on a NEW set",
             ref="", bank="ai_workforce_synthesis", rubric_ref="rc.ap", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="New set. Same weave-by-point move as the water set, a new topic.",
                 closer="Write ONE point-organized paragraph on the AI-and-workforce sources: state a claim and "
                        "support it with several sources meeting on it, connected and cited. Do not write a "
                        "paragraph per source. Run the weave check before you submit. Take the time you need.")),
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
