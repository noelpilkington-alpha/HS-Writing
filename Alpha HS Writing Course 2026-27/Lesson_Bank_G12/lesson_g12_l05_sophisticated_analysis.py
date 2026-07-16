"""
lesson_g12_l05_sophisticated_analysis.py  -  G12 KC C.12.01, ESSAY-ASSEMBLY (BUILD, ceiling essay). V3.1.

G12 course L05 (Unit 1, build), rebuilt to the v3.1 build spec (hand-authored). Teaching point (KEPT): write a
full RHETORICAL-ANALYSIS essay that analyzes the author's choices AND earns sophistication by SITUATING them in
the whole rhetorical situation and HOLDING the tension in the author's strategy, rather than running a mechanical
device-hunt. ANALYSIS-TIER binds a full PD speech (Douglass, 1852) as the taught text and reuses the G11 teaching
speech (a year removed, fresh to the G12 student) as the cold transfer.

Preserved EXACTLY from the current L05: id="ACC-W910-L-G12-C1201-0005", lesson_type=7, kc="C.12.01",
mnemonic_status="proposal", unit framing, the bound stimuli (DOUGLASS taught -> G11 ra_speech_1 transfer), and
every production_frq unit= value (SUPPORTED plan = multi_paragraph, INDEPENDENT + TRANSFER = essay). The unit
ladder climbs to the essay, the type-7 ceiling.

V3.1 changes vs the current L05 (the two failing gates + the spine polish):
  1. FIXED the leaked internal label: the discrimination no longer says "a Grade-C design bet we label as a bet";
     it is a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}] (leaked_internal_label).
  2. FIXED the two wall-of-text teach cards: the prose blocks are now a ONE_IDEA callout + real <ul>/<ol> lists
     (format_fidelity, and the v3.1 "parallel items as a list" rule).
  3. Deterministic FRQ + diagnosis prompts via frq_prompt/setapart/checklist (no "Step 1/2" prose, no "Scored on"
     chrome); coping-model before/after kept; the check tool (situate-and-hold reread) folded in at first use as
     a real <ol> REMEMBER box.
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
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Sophisticated analysis <strong>situates</strong> the '
'author\'s choices in the whole rhetorical situation and <strong>holds the tension</strong> in the strategy. '
'Naming techniques is the floor; explaining why THESE choices for THIS audience under THIS pressure is the '
'point.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: situate and hold</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, reread the analysis and ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Have I named the rhetorical situation, who the audience is and what the speaker needs from them?</li>'
'<li style="margin:2px 0">Have I named the tension the speaker must manage at once, the competing pressures?</li>'
'<li style="margin:2px 0">Is each choice tied to that situation and tension, not just labeled a technique?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you submit.</div></div>')

# coping-model before/after: a mechanical device-hunt rebuilt into analysis that situates the rhetoric and holds
# the strategic tension. Contains BOTH a literal BEFORE and AFTER (content_depth). No named writer (stateless).
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> a mechanical device-hunt</span>'
    '<p style="margin:8px 0 0;font-size:15px">First try: Douglass uses rhetorical questions, repetition, and '
    'strong diction. These techniques make his speech powerful and help him persuade the audience.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">Running the check: is the rhetorical situation named? '
    'No. Is a tension named? No. So this lists tools and calls the speech powerful. That is the competent floor, '
    'not sophistication.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> situates the strategy, holds its tension</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">SITUATED + HELD TENSION</span> Second try, then final: Douglass must praise the founders '
      'his audience reveres while indicting the nation they built, so his choice to voice their pride only to '
      'turn it into the measure of Black exclusion lets him accuse without alienating, holding a hostile crowd he '
      'cannot afford to lose.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Now the analysis places the choices in the speaker\'s '
    'bind and holds the tension in his strategy. Situating the rhetoric is the sophistication move.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G12-C1201-0005", grade="9-10", lesson_type=7,
    unit="G12 U1 - BUILD: sophisticated rhetorical analysis",
    title="Analyze the Rhetoric With Sophistication",
    target=("Write a full rhetorical-analysis essay that analyzes the author's choices AND earns sophistication "
            "by situating them in the whole rhetorical situation and holding the tension in the author's "
            "strategy, rather than a mechanical device-hunt. Written at the essay, untimed. Trait: "
            "Sophistication (Row C) with Evidence and Commentary."),
    acc_tags=["ACC.W.INFO.6", "CCSS.W.11-12.9", "CCSS.RI.11-12.6"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.12.01", "sot": "icm course-G12.md L05",
                "taught_stimulus": "ACC-W910-ANALYSIS-LESSON-DOUGLASS",
                "transfer_stimulus": "ACC-W910-RA-SINGLE-0001",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": ("v3.1 spine; ANALYSIS-TIER binds full PD speech; reuses G11 teaching speech (a year "
                             "removed, fresh to the G12 student); AP sophistication (Row C). Grain reconcile: map "
                             "tags DEW/T4 (analysis genre), but a full analysis ESSAY-write is essay-assembly, so "
                             "QC lesson_type=7 (matches G10 L21 analysis-essay precedent). UNTIMED (no Timeback "
                             "timer)."),
                "one_idea": "Sophisticated analysis situates the choices in the rhetorical situation and holds the strategic tension.",
                "one_reminder": "Situate-and-hold reread: rhetorical situation named? tension named? each choice tied, not just labeled?",
                "version_note": ("V3.1 rebuild of L05. FIXED the two failing gates on the prior version: removed "
                                 "the leaked internal label ('a Grade-C design bet we label as a bet') from the "
                                 "discrimination and moved it to explicit choices=[]; broke the two wall-of-text "
                                 "teach cards into a ONE_IDEA callout + real <ul>/<ol> lists (format_fidelity). "
                                 "Deterministic frq_prompt/setapart/checklist bodies (no 'Step 1/2' prose, no "
                                 "'Scored on' chrome); check tool folded in at first use. Preserved id, type 7, "
                                 "kc C.12.01, mnemonic_status=proposal, bound stimuli, and every production_frq "
                                 "unit= value (SUPPORTED=multi_paragraph, INDEPENDENT/TRANSFER=essay)."),
                "review_provenance": "built to the L01/L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["sophisticated-rhetorical-analysis", "situate-the-rhetorical-situation"],
    slots=[
        # ===== TEACH: the one idea + what sophistication is (as a list), then the order of work (as a list) =====
        Slot("TEACH", "teach_card", "The one idea: situate the rhetoric, do not hunt devices",
             body=(ONE_IDEA +
                   "The rhetorical situation is a set of pressures on the speaker: who the audience is, what the "
                   "speaker needs from them, and the bind the speaker is caught in. A device-hunt is when a writer "
                   "just lists techniques and calls the speech powerful. Sophistication asks a harder set of "
                   "questions:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Situate</strong>: place each choice in the audience and "
                   "purpose. Why THIS choice for THIS audience, and what does the speaker risk?</li>"
                   "<li style=\"margin:4px 0\"><strong>Hold the tension</strong>: name the competing pressures "
                   "the speaker must manage at once, such as praise and indict, or warn and keep hope, and show "
                   "how the choices manage both.</li>"
                   "<li style=\"margin:4px 0\"><strong>Not a catalogue</strong>: naming a technique like a "
                   "rhetorical question or repetition is the floor; it earns nothing on its own.</li></ul>"
                   "The trap is cataloguing techniques with no rhetorical situation behind them. Situate first, "
                   "then explain.")),
        Slot("TEACH", "teach_card", "How to build it: plan the situation, then the choices",
             body=("Here is the order of work. Follow it and the analysis situates the rhetoric instead of "
                   "listing tools:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>SITUATION</strong>: name the audience, the purpose, and "
                   "the speaker's bind in one or two lines.</li>"
                   "<li style=\"margin:4px 0\"><strong>TENSION</strong>: name the competing pressures the speaker "
                   "must hold at the same time.</li>"
                   "<li style=\"margin:4px 0\"><strong>CHOICES</strong>: pick the two or three moves that best "
                   "show how the speaker manages that tension, one per body paragraph.</li>"
                   "<li style=\"margin:4px 0\"><strong>TIE</strong>: in each paragraph, tie the choice back to "
                   "the situation and tension, do not just label it.</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: reread and ask whether the analysis "
                   "explains WHY the choices fit the moment.</li></ol>"
                   "This is the sophistication move applied to analysis, planned first, then built.")),
        Slot("TEACH", "stimulus_display", "Read the source: Frederick Douglass, 1852 address (excerpt)",
             ref="ACC-W910-ANALYSIS-LESSON-DOUGLASS", bank="douglass_1852",
             body=("Read this excerpt from Douglass's 1852 address. Because your job is to write a full "
                   "rhetorical analysis of it, name the rhetorical situation as you read, a mostly white "
                   "audience celebrating independence, and the bind Douglass is in, he must indict them without "
                   "losing them. Then plan an analysis that situates his choices in that tension. The text stays "
                   "on screen while you work.")),

        # ===== MODEL (before the discrimination): coping-model before/after + check tool, then the items =====
        Slot("MODEL", "annotated_before_after", "Watch a device-hunt become situated analysis",
             bank="douglass_1852",
             body=("Here is a device-hunt rebuilt into analysis that situates the rhetoric and holds its tension. "
                   "Watch the writer draft, run the check, catch the problem, and revise. Read the BEFORE, then "
                   "the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE lists techniques. The AFTER situates the choices in the audience and the "
                   "speaker's bind and holds the strategic tension. Situating the rhetoric is the move." +
                   REMEMBER +
                   "When you build your own, plan the situation and tension first, then run this check before you "
                   "submit.")),
        Slot("MODEL", "discrimination", "Which analysis situates the rhetoric?",
             ref="", labeled_grade_c=True, bank="douglass_1852",
             body=("You have watched a device-hunt become situated analysis. Now spot the target: which analysis "
                   "SITUATES the rhetoric in the audience and the speaker's bind, and which just lists techniques "
                   "or retells the speech? "
                   "(A) Because Douglass must indict a nation his audience reveres without losing that audience, "
                   "he voices their pride only to turn it into the very measure of Black exclusion, so he can "
                   "accuse the crowd while still holding it.  "
                   "(B) Douglass fills the address with rhetorical questions, repetition, vivid imagery, and "
                   "strong emotional diction, and because his audience expects patriotic oratory these techniques "
                   "work together to make the whole speech sound powerful, forceful, and deeply persuasive to "
                   "everyone present.  "
                   "(C) Douglass reminds his audience that the country loudly celebrates its own freedom even "
                   "while millions of people remain enslaved, retelling for the crowd how the promise of "
                   "independence has never actually reached every American. "
                   "Correct: A situates the rhetoric; B is a device-hunt and C is a summary. (A) places the "
                   "choices in the audience and the speaker's bind and holds the tension. (B) lists techniques "
                   "and calls the speech powerful. (C) retells what the speech says without analyzing any "
                   "choice."),
             choices=[
                 {"id": "A", "text": "Because Douglass must indict a nation his audience reveres without losing that audience, he voices their pride only to turn it into the very measure of Black exclusion, so he can accuse the crowd while still holding it.",
                  "correct": True,
                  "why": "Correct. This situates the choice in the audience and the speaker's bind and holds the strategic tension, indict without alienating."},
                 {"id": "B", "text": "Douglass fills the address with rhetorical questions, repetition, vivid imagery, and strong emotional diction, and because his audience expects patriotic oratory these techniques work together to make the whole speech sound powerful, forceful, and deeply persuasive to everyone present.",
                  "correct": False,
                  "why": "This is a device-hunt. It names techniques and calls the speech powerful, which is the competent floor, not sophistication."},
                 {"id": "C", "text": "Douglass reminds his audience that the country loudly celebrates its own freedom even while millions of people remain enslaved, retelling for the crowd how the promise of independence has never actually reached every American.",
                  "correct": False,
                  "why": "This retells what the speech says. Summary is not analysis; it never explains why a choice fits the audience or the speaker's bind."},
             ]),
        Slot("MODEL", "predict_the_fix", "What lifts this analysis to sophistication?",
             bank="douglass_1852",
             body=("Diagnose before the reveal. A draft correctly identifies Douglass's rhetorical questions and "
                   "parallelism and says they make the speech more forceful. Which single change would most "
                   "likely earn the sophistication point? "
                   "(A) situate those choices in the rhetorical situation, why they fit this audience and the "
                   "speaker's bind, and hold the tension in his strategy  "
                   "(B) identify still more techniques, adding the metaphors, allusions, and tone shifts the "
                   "first draft missed so the analysis lists a fuller set of moves  "
                   "(C) declare the speech even more forceful, calling it powerful, stirring, and unforgettable "
                   "so the analysis praises its emotional effect more strongly  "
                   "(D) summarize what Douglass argues, retelling his main points about freedom and hypocrisy so "
                   "a reader can follow the content of the speech clearly"),
             feedback=("Correct: A. Naming techniques and their force is competent, not sophisticated. The lift "
                       "situates the choices in the audience and purpose and holds the strategic tension, indict "
                       "without alienating. More techniques (B), stronger praise (C), or summary (D) do not "
                       "situate the rhetoric. There is no clock, so there is time to plan the situation.")),

        # ===== SUPPORTED: plan the analysis (multi_paragraph) - the frame is the highest-value scaffold =====
        Slot("SUPPORTED", "production_frq", "Plan the sophisticated analysis",
             ref="", bank="douglass_1852", rubric_ref="rc.ap", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Plan a sophisticated analysis of Douglass before you write the essay.",
                 setapart_block=setapart("Fill in this plan:",
                                         "Situation: ______ (audience, purpose, the speaker's bind). Tension: ______ (what he must manage at once). Choice 1: ______ tied to the situation. Choice 2: ______ tied to the situation. Choice 3: ______ tied to the situation."),
                 closer="Write the rhetorical SITUATION, the strategic TENSION he must manage, and the two or "
                        "three CHOICES, each tied to that situation. This plan is what you will build the "
                        "analysis from.")),
        # ===== INDEPENDENT: build the whole analysis essay from the plan (essay ceiling) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "BUILD: write the sophisticated analysis",
             ref="", bank="douglass_1852", rubric_ref="rc.ap", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now, build the whole analysis essay from your plan.",
                 closer="Write a complete rhetorical-analysis essay on Douglass: an introduction that situates the "
                        "speech in its rhetorical situation, body paragraphs that tie specific choices to the "
                        "audience and the speaker's bind and hold the strategic tension, and a conclusion on what "
                        "the strategy achieves. Then run the situate-and-hold check and fix any gaps. Situating "
                        "the rhetoric is what every strong analysis is built on, and you are ready to do it cold. "
                        "Take the time you need.")),

        # DIAGNOSIS = self-revision: reread your OWN just-written analysis essay and run the three-question
        # checklist on it, fixing any line that fails. Same taught source (load balance). Self-contained: the
        # checklist is the scaffold and the grader scores the diagnosis within the item.
        Slot("MODEL", "diagnosis_frq", "Check a plan before the full write",
             ref="", bank="douglass_1852", scored=True,
             body=frq_prompt(
                 intro="Reread the essay you just wrote. Run this checklist on YOUR draft and fix any line that fails.",
                 checklist_block=checklist(title="Check your own draft, row by row:", rows=[
                     ("Is the rhetorical situation named (audience, purpose, bind)?", "If it is missing or only implied, name who the audience is, what Douglass needs from them, and the bind he is in."),
                     ("Is a strategic tension named (what he must manage at once)?", "If no tension is named, name the competing pressures, such as praising the founders while indicting the nation."),
                     ("Is each choice tied to that situation, not just labeled?", "If a choice is only labeled as a technique, tie it to the audience and the tension instead."),
                 ]),
                 closer="For every row that fails on your draft, fix it in the essay before you submit. Finish by "
                        "naming the tension your analysis holds.")),
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
