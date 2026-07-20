"""
lesson_g10_l16_synthesis_claim.py  -  G10 KC C.10.06, ARCHETYPE T8: CROSS-SOURCE-SYNTHESIS (WEAVE, ceiling essay). V3.1.

G10 course L16 (Unit 4, intro), rebuilt to the v3.1 build spec (hand-authored). Teaching point (KEPT): write a
SYNTHESIS CLAIM (P5) - your own position that the SET of sources jointly supports, not a summary of any single
source. Taught on the daylight_saving source set, transferred to the partitioned school_year set.

Preserved EXACTLY from the prior L16: id="ACC-W910-L-G10-C1006-0016", lesson_type=8, kc="C.10.06",
mnemonic_status="proposal", unit, title, acc_tags, the bound stimuli (DST taught -> SCHOOLYEAR transfer),
rubric_ref="rc.staar", and unit="multi_paragraph" on the scored writes.

V3.1 changes vs the prior L16:
  1. FIXED the leaked internal label: the discrimination no longer says "a Grade-C design bet we label as a
     bet"; it is a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}]. Correct option is
     not the lone longest, and "should" no longer co-varies with the correct answer (a distractor carries it too).
  2. FIXED the wall-of-text teach card: the prose block is now a ONE_IDEA callout + real <ul>/<ol> lists.
     "synthesis" is defined with a cue phrase ("means" / "is a") in TEACH before use.
  3. Deterministic FRQ + diagnosis prompts via frq_prompt/setapart/checklist (no "Step 1/2" prose, no
     "Scored on ..." chrome); coping-model BEFORE/AFTER kept; the synthesis check tool folded in as a REMEMBER box.
Own words, no fabricated figures (facts trace to the bound DST/SCHOOLYEAR sources), no em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A synthesis claim is <strong>YOUR position that the '
'whole SET of sources together builds</strong>, not a report of what any single source says. You weave the '
'sources into one stance of your own; you do not echo one of them.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: is it a synthesis claim?</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit a synthesis claim, reread it and ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does it state YOUR position, instead of reporting what one source says?</li>'
'<li style="margin:2px 0">Does it draw on the SET, more than one source, not just one?</li>'
'<li style="margin:2px 0">Is it one clear position a reader could disagree with?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you submit.</div></div>')

# coping-model before/after: a single-source summary caught and rebuilt into a synthesis claim. Contains BOTH a
# literal BEFORE and AFTER (content_depth). Facts trace to the bound DST source set (CDC sleep; the switching-
# vs-setting reframe from the objection source).
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> a summary of one source, not a claim of my own</span>'
    '<p style="margin:8px 0 0;font-size:15px"><i>First try:</i> "The first source says the twice-a-year clock '
    'switch hurts people\'s sleep and health."</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">Run the check. Question 1: is this MY position, or a '
    'report of one source? It only reports source 1. Question 2: does it draw on more than one source? No. This '
    'is a single-source summary, not a synthesis claim.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> a position the two sources jointly build</span>'
    '<p style="margin:8px 0 0;font-size:15px"><i>Second try, then final:</i> '
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">SYNTHESIS CLAIM</span> "The country should stop switching the clocks: the health case '
      'against the switch is strong, and the objection about darker commutes is really an argument over which '
      'fixed time to keep, not a reason to keep changing twice a year."</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Now it passes the check. It states my own position, '
    'and it draws on the SET, the health source AND the objection source, reframed. That is a synthesis claim.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1006-0016", grade="9-10", lesson_type=8,
    unit="G10 U4 - Cross-text synthesis (the synthesis claim)",
    title="State a Claim the Sources Together Build",
    target=("Write a synthesis claim: your own position that the set of sources jointly supports, not a "
            "summary of any single source. Written across a multi-source plan. Trait: Thesis/Purpose "
            "(synthesis)."),
    acc_tags=["ACC.W.SRC.1", "CCSS.W.9-10.7"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.06", "sot": "icm course-G10.md L16",
                "taught_stimulus": "ACC-W910-ARG-OPP-LESSON-DST",
                "transfer_stimulus": "ACC-W910-ARG-OPP-LESSON-SCHOOLYEAR",
                "playbook": "_phase2/playbook_T8_WEAVE.md",
                "template": "v3.1 spine; SYNTHESIS-TIER binds full source sets. WEAVE=proposal.",
                "one_idea": "A synthesis claim is your own position that the whole set of sources together builds.",
                "one_reminder": "Synthesis check: is it MY position (not one source)? does it draw on the SET? is it one arguable position?",
                "council": ("T8/WEAVE synthesis-claim intro: introduces P5 (a position the sources jointly "
                            "build, not a single-source summary). synthesis defined in TEACH. jointly-built-vs-"
                            "single-source-summary discrimination labeled Grade-C in code only. WEAVE=proposal."),
                "version_note": ("V3.1 rebuild of L16. Removed the leaked internal label from the discrimination "
                                 "and moved it to explicit choices=[]; broke the wall-of-text teach card into a "
                                 "ONE_IDEA callout + real <ul>/<ol> lists (format_fidelity); deterministic "
                                 "frq_prompt/setapart/checklist bodies; coping-model BEFORE/AFTER kept; synthesis "
                                 "check tool folded in as a REMEMBER box. Preserved id, type 8, kc, "
                                 "mnemonic_status=proposal, unit, title, bound stimuli, and multi_paragraph units."),
                "review_provenance": "built to the G9 L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["synthesis-claim", "position-sources-jointly-build"],
    slots=[
        # ===== TEACH: the one idea + what a synthesis claim is (list), then how to build one (ordered list) =====
        Slot("TEACH", "teach_card", "The one idea: a synthesis claim is yours, built from the set",
             body=(ONE_IDEA +
                   "When you write from several sources, your thesis has a special name and a special job. Here "
                   "are the parts:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Thesis</strong>: a thesis is a one-sentence claim that "
                   "takes a side, and your whole piece defends it.</li>"
                   "<li style=\"margin:4px 0\"><strong>To synthesize</strong>: to synthesize means to combine "
                   "what different sources offer into one position of your own.</li>"
                   "<li style=\"margin:4px 0\"><strong>Synthesis claim</strong>: a synthesis claim is a thesis "
                   "that the SET of sources together supports, drawing on more than one source, not echoing "
                   "any single one.</li>"
                   "<li style=\"margin:4px 0\"><strong>The trap</strong>: reporting what one source says ('Source "
                   "1 says the switch hurts sleep') is a single-source summary, not a synthesis claim.</li></ul>"
                   "Goal today: state a position the whole set builds, in your own words.")),
        Slot("TEACH", "teach_card", "How to build a synthesis claim, step by step",
             body=("Here is the order of work. Follow it and the claim comes from the set, not from one source:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>READ THE SET</strong>: read every source and note what "
                   "each one offers.</li>"
                   "<li style=\"margin:4px 0\"><strong>FIND THE JOINT POSITION</strong>: ask what stance the "
                   "sources together let you take or support.</li>"
                   "<li style=\"margin:4px 0\"><strong>STATE IT AS YOURS</strong>: write one sentence that takes "
                   "that side, in your own words, not a source's words.</li>"
                   "<li style=\"margin:4px 0\"><strong>NAME THE SOURCES</strong>: make sure the claim leans on "
                   "more than one source, so it is built from the set.</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: reread and ask, is it MY position, does it "
                   "draw on the SET, and is it one arguable stance?</li></ol>"
                   "You are weaving several sources into one position of your own.")),
        Slot("TEACH", "stimulus_display", "Read the source set: daylight saving (both sides)",
             ref="ACC-W910-ARG-OPP-LESSON-DST", bank="daylight_saving",
             body=("Read this two-source set on daylight saving. Because your job is to write a synthesis claim, "
                   "read both and ask: what position do they together support or let me argue? The texts stay on "
                   "screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + check tool, then the discrimination + fix ====
        Slot("MODEL", "annotated_before_after", "Watch a source summary become a synthesis claim",
             bank="daylight_saving",
             body=("Here is a writer catching a single-source summary and rebuilding it into a synthesis claim. "
                   "Read the BEFORE, then the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE reports one source and fails the check. The AFTER states a position drawing on "
                   "both, and passes. Building a claim from the SET is the move." + REMEMBER +
                   "When you write your own, run this same check before you submit.")),
        Slot("MODEL", "discrimination", "Which one is a synthesis claim?",
             ref="", labeled_grade_c=True, bank="daylight_saving",
             body=("You have watched a summary become a synthesis claim. Now spot the target: which of these is a "
                   "SYNTHESIS claim (your position, drawn from the SET), and which are single-source summaries? "
                   "(A) The first source explains that the twice-a-year clock change disrupts sleep and, according to health experts, harms people for days afterward with tiredness and low mood.  "
                   "(B) The country should stop switching the clocks, because the health case against the switch is strong and the main objection is really about which fixed time to keep.  "
                   "(C) The second source suggests people should think twice before ending the switch, since both permanent clock options carry real costs and could just move the risk around.  "
                   "(D) The country should stop switching the clocks, because the twice-a-year change disrupts people's sleep and mood. "
                   "Correct: B is a synthesis claim; A and C each report a single source, and D takes a position "
                   "but leans on only one. A synthesis claim states your own position AND draws on more than one "
                   "source; A and C only relay what one source says, and D uses just the health source, so none "
                   "of the three is a claim the whole set jointly builds."),
             choices=[
                 {"id": "A", "text": "The first source explains that the twice-a-year clock change disrupts sleep and, according to health experts, harms people for days afterward, causing daytime tiredness, low mood, and extra strain during that first groggy week.",
                  "correct": False,
                  "why": "This reports what source 1 says. It relays one source's information and states no position of your own, so it is a single-source summary, not a synthesis claim."},
                 {"id": "B", "text": "The country should stop switching the clocks, because the health case against the switch is strong and the main objection turns out to be about which fixed time to keep, not whether to keep changing.",
                  "correct": True,
                  "why": "Correct. This states your own position and draws on the SET, the health source AND the reframed objection source, so the sources jointly build it."},
                 {"id": "C", "text": "The second source suggests people should think twice before ending the switch, since both permanent clock options carry real costs and could move the daylight risk from one part of the day to another.",
                  "correct": False,
                  "why": "This reports what source 2 suggests. Even with the word 'should', it relays one source's stance instead of taking your own, so it is a single-source summary."},
                 {"id": "D", "text": "The country should stop switching the clocks, because the twice-a-year change disrupts people's sleep and mood.",
                  "correct": False,
                  "why": "This one does take your own position, but it leans on only the health source and never draws in the objection source. A synthesis claim has to be built from the SET, so a position resting on a single source is not there yet."},
             ]),
        Slot("MODEL", "predict_the_fix", "What turns this summary into a synthesis claim?",
             bank="daylight_saving",
             body=("Diagnose before the reveal. A student wrote as their thesis: 'The second source says "
                   "permanent evening light has trade-offs.' Which single move would most improve it into a "
                   "synthesis claim? "
                   "(A) state a position of your own that both sources together support, instead of reporting "
                   "one source  "
                   "(B) add a long direct quotation from the second source so its list of trade-offs is spelled "
                   "out in full  "
                   "(C) also summarize what the first source says, so the thesis reports both sources, not just "
                   "the second  "
                   "(D) turn the sentence into a question asking whether the evening-light trade-offs are worth "
                   "keeping"),
             feedback=("Correct: A. Reporting what one source says is a summary, not a thesis. A synthesis claim "
                       "states a position the set builds, for example 'the switch should end, and the trade-offs "
                       "the second source raises are really about which time to keep.' Quoting (B), summarizing "
                       "the other source too (C), or asking a question (D) still do not state your own jointly-"
                       "built position.")),

        # ===== SUPPORTED: write a synthesis claim with a fill-in FRAME (highest-value scaffold) =====
        Slot("SUPPORTED", "production_frq", "Write a synthesis claim",
             ref="", bank="daylight_saving", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Using both daylight-saving sources, write ONE synthesis claim, a position the two "
                       "sources together support.",
                 setapart_block=setapart("Fill in this frame:",
                                         "The sources together show that ______ (your position on whether the switch should end) because ______ (a point from the health source) and ______ (the objection source's point, reframed)."),
                 closer="Turn the frame into one clean sentence in your own words. It must be YOUR position (not "
                        "a report of one source) and must draw on both sources, the health case AND the reframed "
                        "objection.")),
        # DIAGNOSIS = watch the check run on a PROVIDED weak draft, then write a fresh claim and run it yourself.
        Slot("MODEL", "diagnosis_frq", "Check a thesis: synthesis, or single-source summary?",
             ref="", bank="daylight_saving", scored=True,
             body=frq_prompt(
                 intro="First watch the check run on a weak draft, then run it on a fresh claim of your own.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "Source 1 argues the switch is bad for health.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Does it state YOUR position, or report a source?", "It reports source 1. State your own position on whether the switch should end."),
                     ("Does it draw on more than one source?", "No. It uses only source 1. Bring in a point from the objection source too."),
                     ("Is it one clear position a reader could disagree with?", "No. It is a report. Turn it into a stance someone could argue against."),
                 ]),
                 closer="Now write a fresh synthesis claim on the daylight-saving set, run the same three checks, "
                        "and fix any that fail. Finish by naming which sources your claim draws on.")),

        # ===== INDEPENDENT: write a synthesis claim cold, no frame + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write a synthesis claim on your own",
             ref="", bank="daylight_saving", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="On your own now. Using both daylight-saving sources, write ONE synthesis claim, your "
                       "position that the set together supports.",
                 closer="No frame this time. Write the claim, then run the check: is it YOUR position (not a "
                        "report of one source), does it draw on more than one source, and is it one arguable "
                        "stance? A synthesis claim is what every real multi-source essay is built on, and you "
                        "are ready to write one cold. Take the time you need.")),

        # ===== TRANSFER: same synthesis-claim move, a NEW source set, partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source set: a longer school year (both sides)",
             ref="ACC-W910-ARG-OPP-LESSON-SCHOOLYEAR", bank="school_year",
             body=("Read this new two-source set on a longer school year. Because your job is to write a "
                   "synthesis claim, read both and ask what position they together let you argue. The texts "
                   "stay on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Write a synthesis claim on a NEW set",
             ref="", bank="school_year", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="New set. Using both school-year sources, write ONE synthesis claim: your position on "
                       "whether to lengthen the school year.",
                 closer="Draw on the SET, the equity and summer-slide case AND the cost or quality objection, "
                        "not a summary of one source. Same synthesis-claim move as the daylight-saving set, a "
                        "new topic. Run the check before you submit.")),
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
