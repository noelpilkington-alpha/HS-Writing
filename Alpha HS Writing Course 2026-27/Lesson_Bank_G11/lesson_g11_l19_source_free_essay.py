"""
lesson_g11_l19_source_free_essay.py  -  G11 KC C.11.06, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD, ceiling essay). V3.1.

G11 course L19 (Unit 4, build). Full SOURCE-FREE argument essay: plan and write a complete argument from own
knowledge, a defensible thesis carried by specific developed examples across body paragraphs, rather than
repeated general assertions. Written at the essay, UNTIMED. Trait: Thesis, Evidence, and Development.

Preserved EXACTLY from the prior L19: id="ACC-W1112-L-G11-C1104-0019", lesson_type=7, kc="C.11.06",
mnemonic_status="proposal", unit, the bound stimuli (SFA-LESSON-0001 curiosity/usefulness taught ->
SFA-PROMPT-0003 ambition/contentment transfer), and the TEACHING POINT (a thesis carried by specific examples,
one per body paragraph, not repeated assertion). Every production_frq unit= value preserved (SUPPORTED plan =
multi_paragraph, INDEPENDENT + TRANSFER = essay); the ladder climbs to the essay, the type-7 ceiling.

V3.1 rebuild vs the prior (prose-wall) version:
  1. REMOVED the leaked internal label: the discrimination no longer says "a Grade-C design bet we label as a
     bet"; it is a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}] (leaked_internal_label).
  2. BROKE the two wall-of-text teach cards into a ONE_IDEA teal callout + real <ul>/<ol> lists of the parts and
     the order of work (format_fidelity + the v3.1 "parallel items as a list" rule).
  3. Deterministic FRQ + diagnosis prompts via frq_prompt/setapart/checklist (no "Step 1/2" prose, no "Scored on"
     chrome); coping-model before/after kept (literal BEFORE + AFTER); the check tool (the 3-question reread)
     folded in at first use as a real <ol> REMEMBER box.
Own words, no fabricated figures (Faraday 1830s magnet/current is the sourced anchor). No em dashes, no named
HTML entities. Passes all 23 lesson_contract gates + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist, outline_table

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A source-free essay is <strong>carried by specific '
'examples</strong>, not by repeating your opinion. One defensible thesis, then each body paragraph develops '
'<strong>one named case</strong> and ties it back. If the reader has nothing concrete to weigh, the essay has '
'not made its argument.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: reread the essay</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, reread the whole essay and ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does the thesis take a defensible side someone could reject?</li>'
'<li style="margin:2px 0">Does each body paragraph develop ONE specific, named example, not a restated opinion?</li>'
'<li style="margin:2px 0">Is each example tied back to the thesis rather than drifting to a new claim?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you submit.</div></div>')

# coping-model before/after: an opening of repeated assertions (no case) rebuilt into a thesis carried by one
# developed, sourced case (Faraday, 1830s, moving magnet -> current -> later generators/motors). Contains BOTH a
# literal BEFORE and AFTER (content_depth). Short structural sketch, not a whole essay - the point is the
# assertion-vs-example contrast.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> an opening of repeated assertions</span>'
    '<p style="margin:8px 0 0;font-size:15px">Curiosity is one of the most important things a society can '
    'have. Throughout history, curiosity has always helped people make progress and move forward. When people '
    'stay curious, they end up discovering things that matter a great deal, so society should support '
    'curiosity.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">Every sentence restates that curiosity is '
    'important without naming a single case. The reader gets one opinion in new words, with nothing concrete '
    'to weigh.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> a thesis carried by one developed case</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">THESIS</span> Society should fund inquiry even when no one can name its use, because '
      'the research that later proves most valuable rarely looks practical while it is underway. '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">EXAMPLE</span> In the 1830s Michael Faraday studied how a moving magnet could produce '
      'an electric current, a question with no application anyone could point to at the time. Decades later '
      'that same principle became the foundation for the generators and motors that now power modern life, '
      'which is exactly why a society should back inquiry with no foreseeable use: the payoff often arrives '
      'long after the curiosity that earned it.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">One defensible thesis, then a single named case '
    'developed and tied straight back to it. That is what a source-free essay measures, and it is what the '
    'BEFORE never delivers.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1104-0019", grade="9-10", lesson_type=7,
    unit="G11 U4 - BUILD: full source-free argument essay",
    title="Write a Full Source-Free Argument From Your Own Knowledge",
    target=("Plan and write a complete source-free argument essay: a defensible thesis carried by specific, "
            "developed examples from your own knowledge across the body paragraphs, rather than repeated general "
            "assertions. Written at the essay, untimed. Trait: Thesis, Evidence, and Development."),
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.3", "ACC.W.PROD.1", "CCSS.W.11-12.1", "CCSS.W.11-12.4"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.06", "sot": "icm course-G11.md L19",
                "taught_stimulus": "ACC-W1112-SFA-LESSON-0001",
                "transfer_stimulus": "ACC-W910-SFA-PROMPT-0003",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": "v3.1 spine; PROMPT-ONLY tier binds the source-free prompt; ESSAY grain, UNTIMED.",
                "one_idea": "A source-free essay is carried by specific examples, one developed named case per body paragraph, not repeated opinion.",
                "one_reminder": "Reread check: defensible thesis? each body paragraph one specific named example? each tied to the thesis?",
                "version_note": ("V3.1 rebuild of L19. Removed the leaked internal label ('a Grade-C design bet "
                                 "we label as a bet') from the discrimination and moved the reasoning to explicit "
                                 "choices=[]; broke the two wall-of-text teach cards into a ONE_IDEA callout + "
                                 "real <ul>/<ol> lists (format_fidelity). Deterministic frq_prompt/setapart/"
                                 "checklist bodies (no 'Step 1/2' prose, no 'Scored on' chrome); coping-model "
                                 "before/after kept; check tool folded in at first use as an <ol> REMEMBER box. "
                                 "Preserved id, type 7, kc C.11.06, mnemonic_status=proposal, unit, bound stimuli, "
                                 "and every production_frq unit= value (SUPPORTED=multi_paragraph, "
                                 "INDEPENDENT/TRANSFER=essay); ladder climbs to essay."),
                "council": ("T7/BUILD G11 source-free essay: full source-free argument (E3) with N/L/B recycle. "
                            "examples-carry-thesis-vs-repeat-assertion discrimination labeled Grade-C in code. "
                            "Untimed. BUILD=proposal; unit=essay."),
                "review_provenance": "built to the G9 L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["full-source-free-essay", "examples-carry-the-thesis"],
    slots=[
        # ===== TEACH: the one idea + the parts (as a list), then the order of work (as a list) =====
        Slot("TEACH", "teach_card", "The one idea: the essay is carried by examples",
             body=(ONE_IDEA +
                   "You already practiced taking a source-free position and developing one specific example. A "
                   "full source-free essay puts those together. A source-free essay is an argument with no "
                   "provided passage, so every example comes from your own reading, studies, or experience. Here "
                   "are its parts:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Thesis</strong>: a thesis is a one-sentence claim that "
                   "takes a defensible side, and your whole essay defends it.</li>"
                   "<li style=\"margin:4px 0\"><strong>Body</strong>: one paragraph per point, each carried by "
                   "ONE specific example, that is, a named, detailed case you develop and tie back to the "
                   "thesis.</li>"
                   "<li style=\"margin:4px 0\"><strong>Conclusion</strong>: land the upshot instead of repeating "
                   "the thesis in new words.</li></ul>"
                   "The failure mode is an essay that restates the same general assertion for three paragraphs "
                   "and never names a case. Examples carry the thesis; opinion repeated louder does not.")),
        Slot("TEACH", "teach_card", "Plan the examples before you draft",
             body=("Here is the order of work. Plan first, then draft from the plan, then self-check:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>POSITION</strong>: pick the side of the prompt you will "
                   "defend.</li>"
                   "<li style=\"margin:4px 0\"><strong>EXAMPLES</strong>: list the specific examples you will "
                   "use, one per body paragraph, and check each is a real named case you can develop with detail "
                   "(not 'many discoveries'). Two well developed examples beat five vague gestures.</li>"
                   "<li style=\"margin:4px 0\"><strong>ORDER</strong>: sequence them so the argument builds, and "
                   "make sure each ties back to the same thesis rather than drifting to a new claim.</li>"
                   "<li style=\"margin:4px 0\"><strong>DRAFT, then CHECK</strong>: write from the plan, then "
                   "reread against a short list before you submit.</li></ol>"
                   "There is no clock; take the time you need. This is the whole unit, run once on your own.")),
        Slot("TEACH", "stimulus_display", "Read the prompt: curiosity or usefulness?",
             ref="ACC-W1112-SFA-LESSON-0001", bank="sfa_curiosity_use",
             body=("Read this source-free prompt on whether society should support inquiry with no foreseeable "
                   "use. There is no passage; every example is yours. Gather your position and two or three "
                   "specific cases, and plan before you draft. The prompt stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + check tool, then the check items =====
        Slot("MODEL", "annotated_before_after", "Watch general assertions become an example-carried essay",
             bank="sfa_curiosity_use",
             body=("Here is the difference between restating an opinion and building from examples. Read the "
                   "BEFORE, then the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE repeats the assertion and names no case. The AFTER carries one thesis with a "
                   "specific example, developed and tied back. Examples carrying the thesis is the move." +
                   REMEMBER +
                   "When you build your own, plan the examples first, then run this check before you submit.")),
        Slot("TEACH", "discrimination", "Which essay plan is carried by examples?",
             ref="", labeled_grade_c=True, bank="sfa_curiosity_use",
             body=("You have watched examples turn a wall of assertions into an argument. Now spot the target: "
                   "which plan will produce a source-free essay that earns the score? "
                   "(A) State a position, then plan one body paragraph per specific named case (Fleming and "
                   "penicillin; non-Euclidean geometry feeding relativity), each developed and tied to the "
                   "thesis, then a conclusion.  "
                   "(B) State a position, then plan three body paragraphs that each restate that curiosity is "
                   "important, with broad claims about history and progress but no single named case, then a "
                   "conclusion.  "
                   "(C) State a position, then plan three body paragraphs that each add stronger adjectives and "
                   "more forceful phrasing about curiosity, with sweeping claims about progress but no named "
                   "case, then a conclusion.  "
                   "(D) State a position, then plan three body paragraphs that each develop one named case, but "
                   "let each paragraph drift into a different point of its own, so the cases never tie back to the "
                   "single thesis, then a conclusion. "
                   "Correct: A. Plan A gives each paragraph a specific case developed and tied to the thesis, so "
                   "the reader has something concrete to weigh; B and C only restate the opinion, one plainly "
                   "and one loudly, and name nothing, and D has cases but lets them drift instead of tying back."),
             choices=[
                 {"id": "A", "text": "State a position, then plan one body paragraph per specific named case (Fleming and penicillin; non-Euclidean geometry feeding relativity), each developed and tied to the thesis, then a conclusion.",
                  "correct": True,
                  "why": "Correct. Each body paragraph is carried by one specific, named case, developed and tied to the thesis, so the reader has something concrete to weigh."},
                 {"id": "B", "text": "State a position, then plan three body paragraphs that each restate that curiosity is important, with broad claims about history and progress but no single named case, then a conclusion.",
                  "correct": False,
                  "why": "This repeats the assertion in new words and names no case. The reader gets one opinion three times with nothing concrete to weigh."},
                 {"id": "C", "text": "State a position, then plan three body paragraphs that each add stronger adjectives and more forceful phrasing about curiosity, with sweeping claims about progress but no named case, then a conclusion.",
                  "correct": False,
                  "why": "Louder wording is still restated opinion, not evidence. With no named case in any paragraph, this is the same failure as B, just more forceful."},
                 {"id": "D", "text": "State a position, then plan three body paragraphs that each develop one named case, but let each paragraph drift into a different point of its own, so the cases never tie back to the single thesis, then a conclusion.",
                  "correct": False,
                  "why": "This plan does supply named cases, but the essay fails the tie-back check: each example drifts to its own point instead of defending the one thesis, so the paragraphs never add up to a single argument."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this source-free essay most need?",
             bank="sfa_curiosity_use",
             body=("Diagnose before the reveal. A draft essay takes a clear position, but every paragraph "
                   "restates 'curiosity has always mattered' with no cases. Which single change would most "
                   "improve it? "
                   "(A) give each body paragraph one specific, developed example tied to the thesis  "
                   "(B) add a fourth body paragraph that restates the thesis one more time in new words  "
                   "(C) swap in stronger adjectives and more forceful wording throughout each paragraph  "
                   "(D) make the introduction longer by adding more general background about curiosity"),
             feedback=("Correct: A. A source-free essay lives or dies on specific examples; restated assertions "
                       "give the reader nothing to weigh. The fix puts one developed case in each body "
                       "paragraph, tied to the thesis. Another restatement (B), adjectives (C), or a longer "
                       "intro (D) do not supply the missing evidence. There is no clock, so there is time to "
                       "plan the examples.")),

        # ===== SUPPORTED: plan the essay (multi_paragraph) - the frame is the highest-value scaffold =====
        Slot("SUPPORTED", "production_frq", "Plan your source-free essay",
             ref="", bank="sfa_curiosity_use", rubric_ref="rc.4trait", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Use the outline grid below to plan your source-free essay on the curiosity prompt "
                       "before you write a word of it. Copy it into the box and fill in each blank.",
                 setapart_block=outline_table(title="Copy this outline, then fill in each blank:", rows=[
                     ("THESIS", "______ (your defensible side)"),
                     ("EXAMPLE 1", ["______ (a named case)", "the detail that makes it count: ______"]),
                     ("EXAMPLE 2", ["______ (a named case)", "its detail: ______"]),
                     ("EXAMPLE 3 (optional)", ["______ (a named case)", "its detail: ______"]),
                 ]),
                 closer="List a one-line thesis that takes a side, then two or three specific examples from your "
                        "own knowledge, one per body paragraph, each a named case you can develop and tie to the "
                        "thesis. This plan is what you will build the essay from.")),
        # ===== INDEPENDENT: build the whole essay from the plan (essay ceiling) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write the full source-free essay",
             ref="", bank="sfa_curiosity_use", rubric_ref="rc.4trait", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now, build the whole essay from your plan.",
                 closer="Write a complete source-free argument essay on the curiosity prompt: an introduction "
                        "that states the thesis, body paragraphs each carried by one specific, developed example "
                        "from your own knowledge (tied to the thesis), and a conclusion that lands the upshot. "
                        "Then run the reread check and fix any part that fails. A thesis carried by specific "
                        "examples is what every real source-free essay is built on, and you are ready to do it "
                        "cold. Take the time you need.")),

        # COUNCIL FIX (2026-07-24): Option A (later-in-arc), check-only: this is a self-check on the student's OWN
        # just-written essay (a calibration/self-revision scaffold that runs AFTER the INDEPENDENT write), not a
        # separate graded rewrite, so there is no fresh draft to grade. The checklist is made READ-ONLY (plain-
        # string rows; the (question, answer) tuple form dropped and each row's conditional guidance folded into
        # one plain instruction). The slot stays a self-check. scored left as-is; no rewrite invented. Same
        # taught bank (load balance).
        Slot("MODEL", "diagnosis_frq", "Check your own source-free essay",
             ref="", bank="sfa_curiosity_use", scored=True,
             body=frq_prompt(
                 intro="Reread the essay you just wrote. Run this checklist on YOUR draft and fix any line that fails.",
                 checklist_block=checklist(title="Check your own draft against these (no need to type answers):", rows=[
                     "Does your thesis take a defensible side? If it only rates the topic (like 'X is good'), sharpen it into a real position someone could reject.",
                     "Is each body point a specific NAMED example? If a body point just restates the opinion (like 'it helps' or 'it is important'), replace it with a real named case you can develop.",
                     "Does each example tie back to the thesis? If an example drifts to a new claim instead of linking back, add a sentence tying it to the thesis.",
                 ]),
                 closer="For every row that fails on your draft, fix it in the essay before you submit. Finish by "
                        "naming which part your essay still needs most.")),
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
