"""
lesson_g10_l22_argument_essay.py  -  G10 KC C.10.06, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD, ceiling essay). V3.1.

G10 course L22 (Unit 4, build), rebuilt to the v3.1 build spec (hand-authored). Teaching point (KEPT): plan and
write a full CROSS-TEXT ARGUMENT essay - a synthesis claim defended across a source set, weaving the sources and
answering the counterclaim, framed by an intro and conclusion. Reaches the essay ceiling. KC C.10.06.

Preserved EXACTLY from the PRE-v3.1 L22: id="ACC-W910-L-G10-C1006-0022", lesson_type=7, kc=C.10.06,
mnemonic_status="proposal", unit, the bound stimuli (daylight_saving taught -> school_year transfer, partitioned),
and every production_frq unit= value (SUPPORTED plan = multi_paragraph, INDEPENDENT + TRANSFER = essay). The unit
ladder still climbs to the essay, which is the type-7 ceiling. UNTIMED (no Timeback timer).

V3.1 changes vs the PRE-v3.1 L22:
  1. Replaced the wall-of-text teach prose with a ONE_IDEA teal callout + real <ul>/<ol> lists (format_fidelity).
  2. Removed the leaked internal label ("a Grade-C design bet we label as a bet") from the discrimination; it is
     now a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}] (leaked_internal_label).
  3. Coping-model before/after kept, with a literal BEFORE and AFTER (content_depth); the reusable check tool
     folded in at first use as a real <ol> REMEMBER box.
  4. Deterministic FRQ + diagnosis via frq_prompt/setapart/checklist (no "Step 1/2" prose -> no render-qc double
     numbering; no "Scored on ..." chrome).
Own words, no fabricated figures, faithful to the bound sources, no em dashes. Passes all 23 gates + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist, outline_table

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A cross-text argument essay defends <strong>one '
'position across the whole set</strong>: it weaves the sources together and answers the other side. A one-sided '
'essay that leans on a single source and ignores the objection is not the same thing.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: reread the essay</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, reread the whole essay and ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does it state one clear position the whole set supports?</li>'
'<li style="margin:2px 0">Are both sources woven together, not used one at a time?</li>'
'<li style="margin:2px 0">Is the strongest objection named and answered, not ignored?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you submit.</div></div>')

# coping-model before/after: a one-sided draft (uses only the health source, never answers the objection) rebuilt
# into a cross-text argument (synthesis claim, both sources woven, counterclaim answered). Contains BOTH a literal
# BEFORE and AFTER (content_depth). Short structural sketch, not a whole essay - the point is the contrast.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> one-sided, one source at a time</span>'
    '<p style="margin:8px 0 0;font-size:15px"><i>Position:</i> The country should end the twice-yearly clock '
    'switch. <i>Body:</i> Source 1 (the health source) says most teens already lack sleep and the spring shift '
    'is linked to more car crashes, so the switch is harmful. It says this for three paragraphs. <i>Conclusion:</i> '
    'The switch is bad for health, so we should end it.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">It leans on one source and never touches the second '
    'source, so it never weaves them and never answers the objection. That is a single-source essay.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> synthesis claim, both sources woven, objection answered</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">CLAIM</span> "The country should stop switching the clocks and keep one setting all year." '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">WOVEN + ANSWERED</span> "The health source shows the spring shift costs sleep and is '
      'linked to more crashes. The second source warns that evening daylight has real value, but its own point '
      'is that the harm comes from the switching, not from any one clock, so it argues for picking one steady '
      'setting too, not for keeping the switch."</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Now one position runs through the whole essay, both '
    'sources are woven on the same question, and the strongest objection is named and answered. That is a '
    'cross-text argument.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1006-0022", grade="9-10", lesson_type=7,
    unit="G10 U4 - Cross-text synthesis (full argument essay)",
    title="Write a Cross-Text Argument Essay",
    target=("Plan and write a full cross-text argument essay: a synthesis claim defended across the source "
            "set, weaving sources and answering the counterclaim, framed by an intro and conclusion. Written "
            "at the essay. Trait: Development/Organization/Purpose."),
    acc_tags=["ACC.W.SRC.1", "ACC.W.ARG.2", "CCSS.W.9-10.1", "CCSS.W.9-10.7"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.06", "sot": "icm course-G10.md L22",
                "taught_stimulus": "ACC-W910-ARG-OPP-LESSON-DST",
                "transfer_stimulus": "ACC-W910-ARG-OPP-LESSON-SCHOOLYEAR",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": "v3.1 spine; SYNTHESIS-TIER binds full source sets; UNTIMED (no Timeback timer).",
                "one_idea": "A cross-text argument defends one position across the set: weave the sources, answer the other side.",
                "one_reminder": "Reread check: one position the set supports? both sources woven? objection named and answered?",
                "version_note": ("V3.1 rebuild of L22. Replaced the wall-of-text teach prose with a ONE_IDEA "
                                 "callout + real <ul>/<ol> lists (format_fidelity); removed the leaked internal "
                                 "label ('a Grade-C design bet we label as a bet') from the discrimination and "
                                 "moved options to explicit choices=[]; deterministic frq_prompt/setapart/"
                                 "checklist bodies (no 'Step 1/2' prose -> no render-qc double numbering; no "
                                 "'Scored on' chrome); coping-model before/after kept; check tool folded in at "
                                 "first use as a real <ol> REMEMBER box. Preserved id, type 7, kc=C.10.06, "
                                 "mnemonic_status=proposal, unit, bound stimuli, and every production_frq unit= "
                                 "value (SUPPORTED=multi_paragraph, INDEPENDENT/TRANSFER=essay); ladder climbs to essay."),
                "council": ("T7/BUILD full cross-text argument essay: synthesis claim defended across the set, "
                            "sources woven, counterclaim answered. woven-and-answered-vs-one-sided "
                            "discrimination labeled Grade-C in CODE only. BUILD=proposal; unit=essay. Untimed."),
                "review_provenance": "built to the G9 L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["cross-text-argument-essay", "synthesis-claim-weave-answer-counterclaim"],
    slots=[
        # ===== TEACH: the one idea + the parts (as a list), then the order of work (as a list) =====
        Slot("TEACH", "teach_card", "The one idea: defend one position across the set",
             body=(ONE_IDEA +
                   "You have practiced each of these moves on its own. A cross-text argument puts them together. "
                   "First, some words for the job:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Synthesize</strong>: to synthesize means to combine "
                   "several sources into one argument instead of handling them one at a time.</li>"
                   "<li style=\"margin:4px 0\"><strong>Synthesis claim</strong>: your one position that the "
                   "whole source set supports, the claim the whole essay defends.</li>"
                   "<li style=\"margin:4px 0\"><strong>Counterclaim</strong>: a counterclaim is a strong "
                   "objection from the other side, often the point one of the sources makes against your "
                   "position. You concede it, then answer it.</li>"
                   "<li style=\"margin:4px 0\"><strong>Weave, and plan by points</strong>: use the sources "
                   "together on a shared point, not one source per paragraph in isolation. Lay the plan out as "
                   "ordered body points under the synthesis claim, weaving each source into whichever point it "
                   "serves. Let the argument set the paragraphs, not the number of sources.</li></ul>"
                   "The trap is a one-sided essay that leans on a single source and ignores the objection. "
                   "Defend one position, weave the sources, and answer the other side.")),
        Slot("TEACH", "teach_card", "How to build it, part by part",
             body=("Here is the order of work. Follow it and the essay assembles itself from moves you already "
                   "own:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>PLAN</strong>: write the synthesis claim, then the body "
                   "points that weave the sources, each naming the evidence it will use.</li>"
                   "<li style=\"margin:4px 0\"><strong>INTRO</strong>: frame the question and state the synthesis "
                   "claim.</li>"
                   "<li style=\"margin:4px 0\"><strong>BODY</strong>: write each planned point as a full "
                   "paragraph that uses both sources on the shared point, not one source alone.</li>"
                   "<li style=\"margin:4px 0\"><strong>ANSWER</strong>: give one paragraph that concedes the "
                   "strongest objection, then answers it.</li>"
                   "<li style=\"margin:4px 0\"><strong>CONCLUSION</strong>: land the upshot instead of repeating "
                   "the claim.</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: reread against a short list, does the "
                   "essay hold one position, weave both sources, and answer the objection?</li></ol>"
                   "You are assembling moves you already own, in this order, into one essay.")),
        Slot("TEACH", "stimulus_display", "Read the source set: daylight saving (both sides)",
             ref="ACC-W910-ARG-OPP-LESSON-DST", bank="daylight_saving",
             body=("Read this two-source set on daylight saving. Because your job is to write a cross-text "
                   "argument, read both and gather a synthesis claim plus the objection (carried by one of the "
                   "sources) you will answer. The texts stay on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + check tool, then the check items =====
        Slot("MODEL", "annotated_before_after", "Watch a one-sided draft become a cross-text argument",
             bank="daylight_saving",
             body=("Here is the difference between a one-sided draft and a cross-text argument. Read the BEFORE, "
                   "then the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE uses one source across several paragraphs and never touches the other. The AFTER "
                   "states one position, weaves both sources, and answers the objection. Weave-and-answer is the "
                   "move." + REMEMBER +
                   "When you build your own, put the parts in this order, then run the check before you submit.")),
        Slot("MODEL", "discrimination", "Which one is a cross-text argument?",
             ref="", labeled_grade_c=True, bank="daylight_saving",
             body=("You have watched a one-sided draft become a cross-text argument. Now spot the target: which "
                   "essay is a real cross-text argument, and which three are not? "
                   "(A) The essay holds one position on the switch, uses both sources together on each point, and "
                   "spends one paragraph naming the strongest objection and then answering it head on.  "
                   "(B) The essay argues to end the switch by quoting the health source across several paragraphs, "
                   "piling up its points about sleep and safety, and it never once mentions the second source.  "
                   "(C) The essay lays out the first source in full, then lays out the second source in full, and "
                   "summarizes each in turn without ever picking a side or answering either one of them.  "
                   "(D) The essay takes one position and pulls evidence from both sources on each point, but it "
                   "never brings up the strongest objection from the other side, so it leaves that counterclaim "
                   "unanswered. "
                   "Correct: A. It holds one position, weaves both sources, and answers the objection. (B) uses "
                   "one source and ignores the other; (C) summarizes both but takes no position and answers "
                   "nothing; (D) weaves both sources but never names or answers the objection."),
             choices=[
                 {"id": "A", "text": "The essay holds one position on the switch, uses both sources together on each point, and spends one paragraph naming the strongest objection and then answering it head on.",
                  "correct": True,
                  "why": "Correct. One position runs through it, both sources are woven, and the objection is named and answered. That is a cross-text argument."},
                 {"id": "B", "text": "The essay argues to end the switch by quoting the health source across several paragraphs, piling up its points about sleep and safety, and it never once mentions the second source.",
                  "correct": False,
                  "why": "This is one-sided. It leans on a single source and never brings in or answers the other, so it does not weave the set or answer the objection."},
                 {"id": "C", "text": "The essay lays out the first source in full, then lays out the second source in full, and summarizes each in turn without ever picking a side or answering either one of them.",
                  "correct": False,
                  "why": "Summarizing each source in turn is not an argument. It takes no position, never weaves the sources on a shared point, and answers no objection."},
                 {"id": "D", "text": "The essay takes one position and pulls evidence from both sources on each point, but it never brings up the strongest objection from the other side, so it leaves that counterclaim unanswered.",
                  "correct": False,
                  "why": "This weaves the sources under one position but skips the counterclaim. A cross-text argument must also concede and answer the strongest objection; leaving it unanswered is the common half-finished version."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this cross-text argument most need?",
             bank="daylight_saving",
             body=("Diagnose before the reveal. A draft argues to end the switch, quotes the health source at "
                   "length, and never mentions the caution the second source raises. Which single move would most "
                   "improve it as a cross-text argument? "
                   "(A) add one paragraph that concedes and answers the objection the other source raises, "
                   "weaving it together with the health case  "
                   "(B) add several more quotations from the health source so that one side of the case runs "
                   "longer and lands with more force  "
                   "(C) restate the position more forcefully and repeat it a few more times so the argument as a "
                   "whole sounds more confident  "
                   "(D) add a personal story about how the twice-yearly time change throws off your own morning "
                   "routine so that the draft feels much more relatable"),
             feedback=("Correct: A. The draft is one-sided; it never brings in or answers the second source's "
                       "objection, so it is not yet a cross-text argument. The fix concedes and answers that "
                       "objection, weaving both sources. More health quotes (B), a louder claim (C), or a "
                       "personal story (D) never bring in and answer the other side.")),

        # ===== SUPPORTED: plan the cross-text argument (multi_paragraph) - the frame is the top scaffold =====
        Slot("SUPPORTED", "production_frq", "Plan the argument: claim, weave, and the objection",
             ref="", bank="daylight_saving", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Use the outline grid below so you can see the shape of the plan. Copy it into the box and "
                       "fill each blank to plan your cross-text argument on daylight saving before you write a word of it.",
                 setapart_block=outline_table(title="Copy this plan, then fill in each blank:", rows=[
                     ("SYNTHESIS CLAIM", "______ (your position the set supports)"),
                     ("WOVEN POINT", "______ (a point that uses BOTH sources)"),
                     ("OBJECTION TO ANSWER", "______ (the strongest point from the side you do not take, and how you will answer it)"),
                 ]),
                 closer="Write the synthesis claim, one body point that weaves both sources, and one objection "
                        "you will concede and answer. This plan is what you will build the essay from. Do not "
                        "plan a one-source essay.")),
        # ===== INDEPENDENT: build the whole cross-text essay (essay ceiling) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write the full cross-text argument essay",
             ref="", bank="daylight_saving", rubric_ref="rc.staar", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now, build the whole essay from your plan.",
                 closer="Write a complete cross-text argument essay on daylight saving: an introduction that "
                        "frames the question and states the synthesis claim, body paragraphs that weave both "
                        "sources, one paragraph that concedes and answers the objection, and a conclusion that "
                        "lands the upshot. Then run the reread check and fix any part that fails. This weave-"
                        "and-answer build is what every real cross-text argument is made of, and you are ready "
                        "to do it cold. Take the time you need.")),

        # COUNCIL FIX (2026-07-24): Option A (later-in-arc), check-only: this is a self-check on the student's OWN
        # just-written essay (a calibration/self-revision scaffold that runs AFTER the INDEPENDENT write), not a
        # separate graded rewrite, so there is no fresh draft to grade. The checklist is made READ-ONLY (plain-
        # string rows; the (question, answer) tuple form dropped and each row's conditional guidance folded into
        # one plain instruction). The slot stays a self-check. scored left as-is; no rewrite invented. Same
        # taught source (load balance).
        Slot("MODEL", "diagnosis_frq", "Check your essay: woven and answered?",
             ref="", bank="daylight_saving", scored=True,
             body=frq_prompt(
                 intro="Reread the essay you just wrote. Run this checklist on YOUR draft and fix any line that fails.",
                 checklist_block=checklist(title="Check your own draft against these (no need to type answers):", rows=[
                     "Does it state one position the whole SET supports? If it is soft like 'the switch is bad' or it leans on one source, sharpen the position and draw on both.",
                     "Are both sources woven, not used one at a time? If one source runs for several paragraphs on its own, that is single-source. Use both together on a shared point.",
                     "Is the strongest objection named and answered? If the other side never appears, add one paragraph that concedes its point and answers it.",
                 ]),
                 closer="For every row that fails on your draft, fix it in the essay before you move on. Finish by "
                        "naming the objection you will answer.")),
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
