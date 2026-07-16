"""
lesson_g11_l31_rhetorical_analysis_essay.py  -  G11 KC C.11.03, ESSAY-ASSEMBLY (BUILD, ceiling essay). V3.1.

G11 L31, authored to the v3.1 build spec (hand-authored, structure mirrored from the G9 L23 full-essay lesson).
Teaching point: plan AND write a complete rhetorical-analysis essay in the AP Lang FRQ2 shape - a thesis that
names the author's OVERALL rhetorical purpose, body paragraphs that each move from a CHOICE to its EFFECT on the
audience to that PURPOSE (the L06/L07 move, sustained across a whole essay), and an intro and conclusion. KC
C.11.03. This is the C.11.03 gateway capstone the rhetorical-analysis lessons (L06-L09) build toward at essay
grain; it recycles the whole G11 RA stack and reaches the essay ceiling.

Bound sources are VERBATIM PUBLIC-DOMAIN speeches (rhetorical analysis needs a real author's choices):
  taught    = ACC-W910-RA-SINGLE-0001  (FDR, First Inaugural Address, 1933)   bank "ra_speech_1"
  transfer  = ACC-W910-RA-SINGLE-0002  (Bryan, "Cross of Gold" speech, 1896)  bank "ra_speech_2"
Scored production_frq slots route to rc.ap (G11). Own words in all authored prose; short quotes from the bound
speeches are verbatim. No em dashes, no named HTML entities, no <style>/JS. Passes all lesson_contract gates.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A rhetorical-analysis essay is <strong>one move, '
'built out</strong>: a thesis that names the author\'s overall purpose, then body paragraphs that each carry one '
'choice from what the author did, to how it works on the audience, to how it serves that purpose. You plan the '
'purpose and the choices first; you do not list devices and hope.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: reread the essay</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, reread the whole essay and ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does the thesis name the author\'s overall purpose, not just the topic?</li>'
'<li style="margin:2px 0">Does each body paragraph run choice, then effect on the audience, then purpose?</li>'
'<li style="margin:2px 0">Is every quote trimmed and set up, never dropped in bare?</li>'
'<li style="margin:2px 0">Does the conclusion tie the choices back to the one purpose instead of listing devices?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you submit.</div></div>')

# coping-model before/after: a wandering RA essay (thesis names no purpose, body lists devices and content with
# no audience effect, conclusion repeats) rebuilt into a planned essay whose thesis names a purpose and whose
# body moves choice -> effect -> purpose. Contains BOTH a literal BEFORE and AFTER. Short structural sketch, not
# a full essay - the point is the plan-a-purpose-then-build contrast. Quotes from FDR are verbatim.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> no purpose, a list of devices, a repeated ending</span>'
    '<p style="margin:8px 0 0;font-size:15px"><i>Thesis:</i> Roosevelt gave his First Inaugural during the Great '
    'Depression and talks about a lot of problems. <i>Body:</i> He mentions fear. He uses the phrase "money '
    'changers." He talks about banks, farmers, and taxes, and he repeats words. <i>Conclusion:</i> So Roosevelt '
    'uses many rhetorical choices in his speech.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The thesis names a topic, not a purpose; the body '
    'lists devices and content with no effect on the audience; the conclusion just repeats. Nothing is built '
    'toward a point.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> rebuilt so the thesis names a purpose and the body moves choice to effect to purpose</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">THESIS (purpose)</span> "In his First Inaugural, Roosevelt works to turn a paralyzed '
      'nation\'s fear into trust in his leadership so that his listeners will accept swift federal action." '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">CHOICE to EFFECT to PURPOSE (body)</span> "Roosevelt names the enemy when he declares '
      'that the only thing we have to fear is fear itself. By shrinking the vague dread gripping his audience '
      'into a single named thing they can defeat, he hands frightened listeners something to conquer, which '
      'readies them to follow him instead of freezing." '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">CONCLUSION (ties to purpose)</span> "Each choice serves one end: a people convinced '
      'their real enemy is fear itself, not one another, is a people ready to say yes to action now."</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same speech, but now the thesis names a purpose, the '
    'body carries one choice from a trimmed quote to its effect on the audience to that purpose, and the '
    'conclusion ties back to the purpose instead of listing devices. Every part is built from the plan.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1103-0031", grade="9-10", lesson_type=7,
    unit="G11 U2 - Rhetorical-analysis essay (C.11.03 gateway capstone)",
    title="Write a Full Rhetorical-Analysis Essay",
    target=("Plan and write a complete rhetorical-analysis essay (AP Lang FRQ2 shape): a thesis that names the "
            "author's overall rhetorical purpose, body paragraphs that each move choice to effect on the "
            "audience to purpose, and an intro and conclusion. Written at the essay. Trait: Thesis (Row A) and "
            "Evidence and Commentary (Row B)."),
    acc_tags=["ACC.W.INFO.6", "ACC.W.PROD.1", "CCSS.W.11-12.9", "CCSS.RI.11-12.6"],
    provenance={"copyright": "own_authored", "authored": "2026-07-14", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.03",
                "unit-context": ("G11 U2 rhetorical analysis. This is the C.11.03 gateway capstone the RA "
                                 "lessons L06-L09 build toward: L06/L07 teach the choice-effect-purpose move at "
                                 "sentence grain; this lesson sustains it across a full AP Lang FRQ2 essay."),
                "taught_stimulus": "ACC-W910-RA-SINGLE-0001",
                "transfer_stimulus": "ACC-W910-RA-SINGLE-0002",
                "one_idea": ("A rhetorical-analysis essay is one move built out: a thesis naming the author's "
                             "overall purpose, then body paragraphs that each carry a choice to its effect on "
                             "the audience to that purpose."),
                "one_reminder": ("Reread check: thesis names a purpose (not the topic)? each body paragraph "
                                 "runs choice, effect, purpose? quotes trimmed and framed? conclusion ties back "
                                 "to the purpose instead of listing devices?"),
                "version_note": ("NEW lesson added per the design audit: the C.11.03 rhetorical-analysis stack "
                                 "(L06-L09) had no essay-tier capstone, so the gateway skill was taught only at "
                                 "sentence and paragraph grain. This type-7 essay-assembly lesson closes that "
                                 "gap. Authored to the v3.1 spine using the G9 L23 full-essay lesson for "
                                 "structure only; content is fresh for rhetorical analysis. Binds the two G11 "
                                 "verbatim public-domain RA speeches (FDR taught, Bryan transfer); scored writes "
                                 "route to rc.ap; SUPPORTED plan = multi_paragraph, INDEPENDENT/TRANSFER = "
                                 "essay, so the unit ladder climbs to the type-7 essay ceiling.")},
    fade_ledger_moves=["plan-then-draft-ra-essay", "sustain-choice-effect-purpose-across-an-essay"],
    slots=[
        # ===== TEACH: the one idea + the parts (as a list), then the order of work (as a list) =====
        Slot("TEACH", "teach_card", "The one idea: an RA essay is one move, built out",
             body=(ONE_IDEA +
                   "You have practiced the choice-effect-purpose move at the sentence and the paragraph. A full "
                   "rhetorical-analysis essay sustains that one move across the whole piece. Its parts:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Thesis</strong>: a thesis is a one-sentence claim that "
                   "your whole essay defends. In a rhetorical-analysis essay, the thesis names the author's "
                   "overall rhetorical purpose, that is, what the author is trying to make the audience feel, "
                   "believe, or do.</li>"
                   "<li style=\"margin:4px 0\"><strong>Body</strong>: one paragraph per rhetorical choice, and "
                   "each paragraph runs the same move: name the CHOICE with a trimmed, set-up quote, explain its "
                   "EFFECT on the specific audience, then tie that effect to the PURPOSE.</li>"
                   "<li style=\"margin:4px 0\"><strong>Intro and conclusion</strong>: the intro orients the "
                   "reader to the author and occasion and states the thesis; the conclusion ties the choices "
                   "back to the one purpose.</li></ul>"
                   "The trap is listing devices with no purpose, which reads like a scavenger hunt instead of an "
                   "argument about how the text works. Name the purpose, then build.")),
        Slot("TEACH", "teach_card", "How to build it, part by part",
             body=("Here is the order of work. Follow it and the essay assembles itself from the move you "
                   "already own:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>PLAN</strong>: write the thesis (the author's overall "
                   "purpose), then pick two or three of the author's strongest choices, in a sensible order.</li>"
                   "<li style=\"margin:4px 0\"><strong>INTRO</strong>: name the author and occasion, then state "
                   "the thesis.</li>"
                   "<li style=\"margin:4px 0\"><strong>BODY</strong>: write each planned choice as a full "
                   "paragraph that runs choice (with a trimmed, framed quote), then effect on the audience, then "
                   "purpose, and open each paragraph after the first with a transition.</li>"
                   "<li style=\"margin:4px 0\"><strong>CONCLUSION</strong>: tie the choices back to the one "
                   "purpose.</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: reread against a short list, does the "
                   "thesis name a purpose, does each body paragraph run choice to effect to purpose, are quotes "
                   "trimmed and framed, does the conclusion tie back to the purpose?</li></ol>"
                   "You are sustaining one move you already own, in this order, across a whole essay.")),
        Slot("TEACH", "stimulus_display", "Read the source: Roosevelt's First Inaugural (1933)",
             ref="ACC-W910-RA-SINGLE-0001", bank="ra_speech_1",
             body=("Read this excerpt from Franklin D. Roosevelt's First Inaugural Address, delivered in 1933 to "
                   "a fearful national audience at the depth of the Great Depression. Because your job is to "
                   "write a full rhetorical-analysis essay from it, read once for his overall purpose, then "
                   "again for two or three CHOICES he makes (his naming of fear, his catalog of hardships, his "
                   "money-changers image, his call for action) and how each works on that audience. The text "
                   "stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + check tool, then the check items =====
        Slot("MODEL", "annotated_before_after", "Watch a purpose turn a device list into a built essay",
             bank="ra_speech_1",
             body=("Here is the difference between listing devices and building an essay around a purpose. Read "
                   "the BEFORE, then the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE names a topic and lists devices with no effect and no purpose. The AFTER states "
                   "a purpose, then carries one choice from a trimmed quote to its effect on the audience to "
                   "that purpose. Name the purpose, then build, is the move." + REMEMBER +
                   "When you build your own, put the parts in this order, then run the check before you submit.")),
        Slot("MODEL", "discrimination", "Which writer built an RA essay around a purpose?",
             ref="", labeled_grade_c=True, bank="ra_speech_1",
             body=("You have watched a purpose turn a device list into a built essay. Now spot the target: which "
                   "writer built a rhetorical-analysis essay around a purpose, and which did not? "
                   "(A) The writer first writes a thesis naming Roosevelt's overall purpose, then plans two or three choices that each pair a quote with its effect on the audience and tie back to that purpose, then drafts.  "
                   "(B) The writer reads the speech once and starts writing down every device that gets noticed, in the order it turns up, adding one more each time another device appears and stopping only when the essay finally seems long enough to hand in.  "
                   "(C) The writer retells what the speech says paragraph by paragraph, walking through Roosevelt's content from the opening line all the way to the close, and then calls that careful retelling a rhetorical analysis. "
                   "Correct: A. It fixes the purpose first, so every body paragraph carries a choice to its effect "
                   "to that purpose; B lists devices with no purpose and C summarizes content, so neither analyzes how the speech works."),
             choices=[
                 {"id": "A", "text": "The writer first writes a thesis naming Roosevelt's overall purpose, then plans two or three choices that each pair a quote with its effect on the audience and tie back to that purpose, then drafts.",
                  "correct": True,
                  "why": "Correct. This writer names the purpose first, so every body paragraph carries a choice to its effect to that one purpose. That is a built rhetorical-analysis essay."},
                 {"id": "B", "text": "The writer reads the speech once and starts writing down every device that gets noticed, in the order it turns up, adding one more each time another device appears and stopping only when the essay finally seems long enough to hand in.",
                  "correct": False,
                  "why": "This is a device scavenger hunt, not analysis. Listing devices with no purpose never explains how the speech works on its audience."},
                 {"id": "C", "text": "The writer retells what the speech says paragraph by paragraph, walking through Roosevelt's content from the opening line all the way to the close, and then calls that careful retelling a rhetorical analysis.",
                  "correct": False,
                  "why": "This is summary. Retelling the content, however accurately, names no choice, no effect on the audience, and no purpose."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this essay approach most need?",
             bank="ra_speech_1",
             body=("Diagnose before the reveal. A student says: 'For the essay I will just point out every "
                   "device Roosevelt uses and explain what each device is.' For a full "
                   "rhetorical-analysis essay, which single change would most improve the result? "
                   "(A) write a thesis that names Roosevelt's overall purpose first, then make each body "
                   "paragraph move from a choice to its effect on the audience to that purpose  "
                   "(B) find and label even more devices scattered throughout the speech so that the finished "
                   "essay clearly covers a longer, fuller, and more complete list of the techniques the author uses  "
                   "(C) add a much longer introduction that carefully explains the whole history of the Great "
                   "Depression before the analysis of the speech begins  "
                   "(D) swap in bigger, more impressive vocabulary words throughout the essay so that the "
                   "writing sounds smarter and more advanced to a reader"),
             feedback=("Correct: A. Listing and defining devices is the most common cause of essays that name "
                       "techniques but never explain how the text works. The fix is to name the purpose first, "
                       "then make every body paragraph carry a choice to its effect on the audience to that "
                       "purpose. A longer device list (B), a longer intro (C), or bigger words (D) do not give "
                       "the essay the purpose-and-effect spine it needs.")),

        # ===== SUPPORTED: plan the RA essay (multi_paragraph) - the frame is the highest-value scaffold =====
        Slot("SUPPORTED", "production_frq", "Plan the essay: purpose and ordered choices",
             ref="", bank="ra_speech_1", rubric_ref="rc.ap", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Plan your rhetorical-analysis essay on Roosevelt's First Inaugural before you write a "
                       "word of it.",
                 setapart_block=setapart("Fill in this plan:",
                                         "Thesis (Roosevelt's overall purpose): ______. Choice 1: ______ (quote) + its effect on the audience + how it serves the purpose. Choice 2: ______ (quote) + effect + purpose. Choice 3: ______ (quote) + effect + purpose."),
                 closer="Write one line naming Roosevelt's overall purpose, then list two or three choices, each "
                        "naming the trimmed quote it will use, the effect that choice has on his audience, and "
                        "how that effect serves the purpose. This plan is what you will build the essay from.")),
        # ===== INDEPENDENT: build the whole essay from the plan (essay ceiling) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write the full rhetorical-analysis essay",
             ref="", bank="ra_speech_1", rubric_ref="rc.ap", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now, build the whole essay from your plan.",
                 closer="Write a complete rhetorical-analysis essay on Roosevelt's First Inaugural: an "
                        "introduction that names the author and occasion and states a thesis naming his overall "
                        "purpose, two or three body paragraphs that each run choice (with a trimmed, framed "
                        "quote) to effect on the audience to purpose, and a conclusion that ties the choices "
                        "back to the one purpose. Then run the reread check and fix any part that fails. "
                        "Sustaining the choice-to-effect-to-purpose move across a whole essay is the real skill, "
                        "and you are ready to do it. Take the time you need.")),

        # DIAGNOSIS = self-revision: reread your OWN just-written essay and run the 3-question check on it,
        # fixing any line that fails. Same taught source (load balance). Self-contained: the checklist is the
        # scaffold and the grader scores the diagnosis within the item.
        Slot("MODEL", "diagnosis_frq", "Reread your finished essay and run the checklist",
             ref="", bank="ra_speech_1", scored=True,
             body=frq_prompt(
                 intro="Reread the essay you just wrote. Run this checklist on YOUR draft and fix any line that fails.",
                 checklist_block=checklist(title="Check your own draft, line by line:", rows=[
                     ("Does your thesis name an overall purpose?", "If it only names the topic (like 'talks about the Depression'), say instead what Roosevelt is trying to make the audience feel, believe, or do."),
                     ("Does each choice name a quote and its effect on the audience?", "If a choice names a device with no quote and no effect (like 'mentions fear' or 'uses repetition'), attach a trimmed quote and the effect on his listeners to each."),
                     ("Does each choice tie back to the purpose?", "If nothing connects the choices to one end, show how each effect serves the purpose named in the thesis."),
                 ]),
                 closer="For every line that fails on your draft, name what is off in one sentence and make the "
                        "fix. Finish by naming the overall purpose your essay is built to prove.")),
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
