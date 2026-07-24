"""
lesson_g10_l21_analysis_essay.py  -  G10 KC C.10.06, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD, ceiling essay). V3.1.

G10 course L21 (Unit 4, build), rebuilt to the v3.1 build spec (hand-authored). Teaching point (KEPT): plan and
write a full CROSS-TEXT ANALYSIS essay - ONE analytical claim about the authors' craft, supported with
device-effect-warrant woven across two texts, framed by an intro and a conclusion. Reaches the essay ceiling.
KC C.10.06. ANALYSIS/SYNTHESIS-TIER binds full sources; UNTIMED.

Preserved EXACTLY from the prior L21: id="ACC-W910-L-G10-C1006-0021", lesson_type=7, kc=C.10.06,
mnemonic_status="proposal", unit=G10 U4, the bound stimuli (HOUR + HIGHWAYS taught -> RECYCLING transfer, paired
with HIGHWAYS), and every production_frq unit= value (SUPPORTED plan = multi_paragraph, INDEPENDENT + TRANSFER
= essay). The unit ladder climbs to the essay, the type-7 ceiling.

V3.1 changes vs the prior L21 (the two failing gates + the spine polish):
  1. FIXED the leaked internal label: the discrimination no longer says "a Grade-C design bet we label as a
     bet"; it is a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}] (leaked_internal_label).
  2. FIXED the wall-of-text teach card: the prose block is now a ONE_IDEA teal callout + a real <ul> of the
     parts, plus a second teach card with the <ol> order of work (format_fidelity).
  3. Deterministic FRQ + diagnosis prompts via frq_prompt/setapart/checklist (no "Step 1/2" prose, no
     "Scored on ..." chrome); coping-model before/after kept; the reusable check tool folded in at the point of
     first use as a real <ol> REMEMBER box.
Own words, quotes verbatim from the bound sources, no fabricated figures, no em dashes. Passes all 23 gates + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A cross-text analysis essay does not review two texts. '
'It makes <strong>ONE analytical claim</strong> about the authors\' craft and supports that one claim with '
'evidence from <strong>both</strong> texts.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: reread the essay</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, reread the whole essay and ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Is there ONE analytical claim about a technique, carried across both texts?</li>'
'<li style="margin:2px 0">Does each text get device to effect to warrant, not a plot summary?</li>'
'<li style="margin:2px 0">Are the two texts woven, naming where they line up or differ?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you submit.</div></div>')

# coping-model before/after: a double summary rebuilt into one cross-text analytical claim supported from both
# texts. Contains BOTH a literal BEFORE and AFTER (content_depth). Quotes are verbatim from the bound sources.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> summarizes each text in turn, then rates them</span>'
    '<p style="margin:8px 0 0;font-size:15px">The first text is a story about a woman who is told her husband '
    'has died. The second text is an article about the interstate highways. Both texts are clearly written and '
    'interesting to read.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">This retells one text, then the other, and rates '
    'them. There is no single claim, no named technique, and no evidence tied to a point.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> one analytical claim, supported from both texts</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">CLAIM</span> Both authors open with something ordinary so that a hidden truth lands '
      'harder. '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">TEXT 1 + TEXT 2</span> Chopin wraps the news of death in ordinary spring life, the '
      '"tops of trees that were all aquiver with the new spring life," so that Mrs. Mallard\'s whispered '
      '"free, free, free!" startles the reader; the highways writer calls the interstate "part of the '
      'landscape," something drivers pass "without ever thinking about it," before revealing it is "one of the '
      'largest building projects in the nation\'s history." '
      '<span style="background:#dcfce7;color:#166534;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">WARRANT</span> That ordinary opening matters to each author\'s purpose: by hiding the '
      'truth inside the everyday, Chopin makes the reader feel how unnoticed Mrs. Mallard\'s longing for freedom '
      'had been, and the highways writer makes the reader see that a system they take for granted is a staggering '
      'achievement, so in both texts the plain surface is what forces the hidden truth to register.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">One claim about a shared technique, supported with '
    'device to effect to warrant from BOTH texts, woven together. That is a cross-text analysis.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1006-0021", grade="9-10", lesson_type=7,
    unit="G10 U4 - Cross-text synthesis (full analysis essay)",
    title="Write a Cross-Text Analysis Essay",
    target=("Plan and write a full cross-text analysis essay: one analytical claim about the authors' craft, "
            "supported with device-effect-warrant woven across two texts, framed by an intro and conclusion. "
            "Written at the essay. Trait: Evidence/Development/Organization."),
    acc_tags=["ACC.W.INFO.6", "ACC.W.SRC.1", "CCSS.W.9-10.9", "CCSS.W.9-10.7"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.06", "sot": "icm course-G10.md L21",
                "taught_stimulus": "ACC-W910-ANALYSIS-LESSON-HOUR",
                "taught_stimulus_2": "ACC-W910-INFO-LESSON-HIGHWAYS",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-RECYCLING",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": "v3.1 spine; ANALYSIS/SYNTHESIS-TIER binds full sources; UNTIMED (no Timeback timer).",
                "one_idea": "A cross-text analysis essay makes ONE analytical claim about craft and supports it from BOTH texts.",
                "one_reminder": "Reread check: one claim across both texts? each text device-effect-warrant, not summary? woven?",
                "version_note": ("V3.1 rebuild of L21. FIXED the two failing gates on the prior version: removed "
                                 "the leaked internal label ('a Grade-C design bet we label as a bet') from the "
                                 "discrimination and moved it to explicit choices=[]; broke the wall-of-text teach "
                                 "card into a ONE_IDEA callout + real <ul>/<ol> lists (format_fidelity). "
                                 "Deterministic frq_prompt/setapart/checklist bodies; coping-model before/after "
                                 "kept; check tool folded in at first use. Preserved id, type 7, kc=C.10.06, "
                                 "mnemonic_status=proposal, unit, bound stimuli, and every production_frq unit= "
                                 "value (SUPPORTED=multi_paragraph, INDEPENDENT/TRANSFER=essay); ladder climbs to essay."),
                "review_provenance": "built to the G9 L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["cross-text-analysis-essay", "one-claim-across-two-texts"],
    slots=[
        # ===== TEACH: the one idea + the parts (as a list), then the order of work (as a list) =====
        Slot("TEACH", "teach_card", "The one idea: one claim, supported across both texts",
             body=(ONE_IDEA +
                   "You have practiced each of these moves on one text. A cross-text analysis puts them together "
                   "across two texts, in these parts:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>The analytical claim</strong>: a claim about a technique "
                   "the two texts share, or use differently, not a rating of which text is better.</li>"
                   "<li style=\"margin:4px 0\"><strong>A device from each text</strong>: a device is a specific "
                   "technique an author chooses on purpose, such as an image, a comparison, or a repeated word.</li>"
                   "<li style=\"margin:4px 0\"><strong>Effect, then warrant</strong>: name what each device does "
                   "to the reader, then add a warrant. A warrant is a sentence that explains why that effect "
                   "matters to the author's purpose.</li>"
                   "<li style=\"margin:4px 0\"><strong>The weave</strong>: name where the two texts do the same "
                   "thing or differ, so the claim spans both instead of sitting on one.</li>"
                   "<li style=\"margin:4px 0\"><strong>Plan by points, not by sources</strong>: lay the plan out "
                   "as ordered body points under the claim, weaving each text into whichever point it serves. Let "
                   "the analysis set the paragraphs; do not give each text its own paragraph.</li></ul>"
                   "The trap is summarizing each text in turn instead of supporting one claim across both. Plan "
                   "the claim first, by points, then build.")),
        Slot("TEACH", "teach_card", "How to build it, part by part",
             body=("Here is the order of work. Follow it and the essay assembles itself from moves you already "
                   "own:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>PLAN</strong>: write the analytical claim, then, for each "
                   "text, the device you will analyze and its effect.</li>"
                   "<li style=\"margin:4px 0\"><strong>INTRO</strong>: name both texts and state the one "
                   "analytical claim.</li>"
                   "<li style=\"margin:4px 0\"><strong>BODY</strong>: run device to effect to warrant on each "
                   "text, and weave them, naming where the texts line up or differ.</li>"
                   "<li style=\"margin:4px 0\"><strong>CONCLUSION</strong>: land why the shared craft matters, "
                   "instead of repeating the claim.</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: reread against a short list, is there one "
                   "claim across both texts, is each text analyzed and not summarized, are the two woven?</li></ol>"
                   "You are assembling moves you already own, in this order, into one analytical essay.")),
        Slot("TEACH", "stimulus_display", "Read text 1: Kate Chopin, \"The Story of an Hour\" (1894)",
             ref="ACC-W910-ANALYSIS-LESSON-HOUR", bank="story_of_an_hour",
             body=("Read this short story. As you read, note one technique Chopin uses that you could analyze: "
                   "the spring imagery outside the open window, the irony of grief turning to relief, the "
                   "repetition of the word free. You will pair it with a technique from text 2. The text stays "
                   "on screen while you work.")),
        # tag="buy_in": this is the SECOND source-orientation read (a cross-text analysis binds two texts, so it
        # has two source displays). A get-familiar read is orientation, not a load-bearing teach segment that
        # needs an intervening check, so it counts 0 toward the check-cadence run (LS-feedback #3), keeping the
        # pre-check run of counted teach segments within the full_essay_build ceiling of 4. No teaching is cut.
        Slot("TEACH", "stimulus_display", "Read text 2: Building the Interstate Highway System",
             ref="ACC-W910-INFO-LESSON-HIGHWAYS", bank="interstate_highways", tag="buy_in",
             body=("Read this explanatory article. Note one authorial choice you could analyze: how the writer "
                   "opens with the road as an everyday thing that drivers pass without thinking, then sets that "
                   "against its vast scale and cost. You will pair a technique here with one from text 1. The "
                   "text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + check tool, then discrimination + predict =====
        Slot("MODEL", "annotated_before_after", "Watch a double summary become a cross-text analysis",
             bank="story_of_an_hour",
             body=("Here is the difference between summarizing two texts and analyzing across them. Read the "
                   "BEFORE, then the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE retells each text and rates them. The AFTER makes one claim about a technique "
                   "the two authors share and supports it with evidence woven from both. One claim across both "
                   "texts is the move." + REMEMBER +
                   "When you build your own, put the parts in this order, then run the check before you submit.")),
        Slot("MODEL", "discrimination", "Which one is a cross-text analysis?",
             ref="", labeled_grade_c=True, bank="story_of_an_hour",
             body=("You have watched a double summary become a cross-text analysis. Now spot the target: which "
                   "of these is a cross-text analysis of the two texts? "
                   "(A) One analytical claim names a technique both authors use, then each body paragraph runs "
                   "device to effect to warrant, drawing evidence from Chopin and from the highways article and "
                   "naming where the two texts line up.  "
                   "(B) One paragraph retells the plot of the Chopin story from start to finish, a second "
                   "paragraph lists the main points of the highways article in the order they appear, and a "
                   "closing line says both texts were clear and worth the time.  "
                   "(C) Every paragraph studies Chopin's spring imagery in close, quoted detail across both "
                   "texts, while the highways article is named once at the very end and is never actually "
                   "analyzed for any technique at all.  "
                   "(D) One paragraph analyzes a device in the Chopin story with its effect, the next analyzes a "
                   "device in the highways article with its effect, but no single claim ties the two texts "
                   "together into one point. "
                   "Correct: A. It makes one analytical claim and supports it with device-effect-warrant from "
                   "both texts. B double-summarizes; C analyzes only one text and leaves the other unexamined; "
                   "D analyzes each text well but never joins them under one cross-text claim."),
             choices=[
                 {"id": "A", "text": "One analytical claim names a technique both authors use, then each body paragraph runs device to effect to warrant, drawing evidence from Chopin and from the highways article and naming where the two texts line up.",
                  "correct": True,
                  "why": "Correct. One claim about a shared technique, supported with device-effect-warrant from both texts and woven together, is a cross-text analysis."},
                 {"id": "B", "text": "One paragraph retells the plot of the Chopin story from start to finish, a second paragraph lists the main points of the highways article in the order they appear, and a closing line says both texts were clear and worth the time.",
                  "correct": False,
                  "why": "This is a double summary. It retells each text in turn and rates them; there is no single analytical claim and no evidence tied to a point."},
                 {"id": "C", "text": "Every paragraph studies Chopin's spring imagery in close, quoted detail across both texts, while the highways article is named once at the very end and is never actually analyzed for any technique at all.",
                  "correct": False,
                  "why": "This analyzes only one text. A cross-text analysis must carry its claim into both texts, not leave one unexamined."},
                 {"id": "D", "text": "One paragraph analyzes a device in the Chopin story with its effect, the next analyzes a device in the highways article with its effect, but no single claim ties the two texts together into one point.",
                  "correct": False,
                  "why": "This is two single-text analyses side by side. Each text is analyzed, but with no one claim carried across both, so the texts are never actually connected. A cross-text analysis needs that shared claim."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this cross-text draft most need?",
             bank="story_of_an_hour",
             body=("Diagnose before the reveal. A draft has one paragraph summarizing the Chopin story and one "
                   "summarizing the highways article, ending with 'both were good.' Which single move would "
                   "most improve it as a cross-text analysis? "
                   "(A) make one analytical claim about a technique the two texts share, then support it with "
                   "device to effect to warrant from each text  "
                   "(B) retell the Chopin plot in even fuller detail and then list every fact in the highways "
                   "article again, this time strictly from the first point to the last  "
                   "(C) add a third article about roads so the finished essay has more sources to compare and "
                   "ends up covering more of the overall subject than it did before  "
                   "(D) state which of the two texts you personally enjoyed more and then explain, at length, "
                   "all of the reasons you happened to prefer that one over the other"),
             feedback=("Correct: A. Two summaries plus 'both were good' is not analysis. The fix is one "
                       "analytical claim about a shared technique, supported across both texts with device to "
                       "effect to warrant. Fuller summaries (B), a third text (C), or ranking the texts (D) do "
                       "not create a single analytical claim carried across both.")),

        # ===== SUPPORTED: plan the analysis (multi_paragraph) - the frame is the highest-value scaffold =====
        Slot("SUPPORTED", "production_frq", "Plan the analysis: claim plus a device from each text",
             ref="", bank="story_of_an_hour", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Plan a cross-text analysis pairing the Chopin story with the highways article before you write it.",
                 setapart_block=setapart("Fill in this plan:",
                                         "Claim: ______ (a technique both texts use, or use differently). Text 1 (Chopin): device ______, effect ______. Text 2 (highways): device ______, effect ______."),
                 closer="Write one analytical claim about a technique the texts share, then, for each text, name "
                        "the device you will analyze and its effect. Do not plan two summaries. This plan is "
                        "what you will build the essay from.")),
        # ===== INDEPENDENT: build the whole cross-text essay (essay ceiling) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write the full cross-text analysis essay",
             ref="", bank="story_of_an_hour", rubric_ref="rc.staar", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now, build the whole essay from your plan, pairing the Chopin story with the highways article.",
                 closer="Write a complete cross-text analysis essay: an introduction that names both texts and "
                        "states one analytical claim about the authors' craft, body paragraphs that run device "
                        "to effect to warrant on each text and weave them (naming where the texts line up or "
                        "differ), and a conclusion on why the shared craft matters. Then run the reread check "
                        "and fix any part that fails. One analytical claim carried across two texts is what "
                        "every real cross-text analysis is built on, and you are ready to do it cold. Take the "
                        "time you need.")),

        # COUNCIL FIX (2026-07-24): Option A (later-in-arc), check-only: this is a self-check on the student's OWN
        # just-written essay (a calibration/self-revision scaffold that runs AFTER the INDEPENDENT write), not a
        # separate graded rewrite, so there is no fresh draft to grade. The checklist is made READ-ONLY (plain-
        # string rows; the (question, answer) tuple form dropped and each row's conditional guidance folded into
        # one plain instruction). The slot stays a self-check. scored left as-is; no rewrite invented. Same
        # taught source (load balance).
        Slot("MODEL", "diagnosis_frq", "Check your essay: one claim across both texts?",
             ref="", bank="story_of_an_hour", scored=True,
             body=frq_prompt(
                 intro="Reread the essay you just wrote. Run this checklist on YOUR draft and fix any line that fails.",
                 checklist_block=checklist(title="Check your own draft against these (no need to type answers):", rows=[
                     "Is there ONE analytical claim about a technique, not a rating? If it rates the texts or calls them interesting, name a specific technique both authors use and say what it does.",
                     "Does each text supply a device that supports the claim? If a text gives only a topic like 'a sad story' or 'about roads', assign one named device from that text instead.",
                     "Is an effect tied to each device? If a device sits there unexplained, say what it makes the reader feel or realize, then add why it matters.",
                 ]),
                 closer="For every row that fails on your draft, fix it in the essay before you move on. Finish by "
                        "naming the shared technique your claim is about.")),
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
