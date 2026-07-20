"""
lesson_g9_l17_build_paragraph.py  -  G9 KC C.9.06/build, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD, ceiling essay).

G9 course L17 (Unit 3, build). Assemble a COMPLETE body paragraph (B1): claim + evidence + warrant, cohered.
This is the first T7 lesson; it works at the paragraph (unit="paragraph"), the step below the essay ceiling,
pulling together every Unit 1-3 move. Locked L01 template. EVIDENCE-TIER: binds the FULL source (the student
needs real quotable evidence). Taught: PHONEBAN (full) -> transfer: SCHOOLLUNCH (full, partitioned). rc.staar.
BUILD=proposal. No coping-model persona; no source markup; no prior-work ref; no em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report

BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> a partial paragraph: claim and evidence, but no warrant</span>'
    '<p style="margin:8px 0 0;font-size:15px">Schools should limit phone use during class. The National Center '
    'for Education Statistics reports that in the 2019 to 2020 school year, about 76.9 percent of public schools '
    'already prohibited non-academic cell phone use during the school day.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">There is a claim and an attributed fact, but the '
    'paragraph stops there. It never explains WHY that fact supports the claim, so it is only partly built.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> a complete, cohered body paragraph</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">CLAIM</span> Schools should limit phone use during class. '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">EVIDENCE</span> The National Center for Education Statistics reports that in the 2019 to '
      '2020 school year, about 76.9 percent of public schools already prohibited non-academic cell phone use '
      'during the school day. '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">WARRANT</span> That figure matters because it shows the limit is already workable rather '
      'than radical: when more than three out of four schools have made the rule stick, a new school can '
      'reasonably expect to enforce it too.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Claim, attributed evidence, and a warrant that '
    'explains why the fact supports the claim, joined so they connect. That is a complete body paragraph.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C906-0017", grade="9-10", lesson_type=7,
    unit="G9 U3 - Build (assemble a complete body paragraph)",
    title="Build a Complete Body Paragraph: Claim, Evidence, Warrant",
    target=("Assemble one complete body paragraph that has all three parts, joined so they connect: a claim, "
            "attributed evidence, and a warrant that explains why the evidence supports the claim. Written at "
            "the paragraph. Trait: Development/Organization."),
    acc_tags=["ACC.W.PROD.1", "CCSS.W.9-10.1"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12",
                "mnemonic_status": "proposal", "kc": "C.9.06", "sot": "icm course-G9.md L17",
                "taught_stimulus": "ACC-W910-ARG-LESSON-PHONEBAN",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-SCHOOLLUNCH",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": "locked L01 template; EVIDENCE-TIER binds full sources. T7 BUILD works at paragraph here (below essay ceiling).",
                "council": ("T7/BUILD first rung: assemble B1 complete body paragraph (claim+evidence+warrant, "
                            "cohered), pulling together every Unit 1-3 move. complete-vs-partial-paragraph "
                            "discrimination labeled Grade-C. BUILD=proposal; unit=paragraph (within essay ceiling).")},
    fade_ledger_moves=["assemble-complete-body-paragraph", "claim-evidence-warrant-cohered"],
    slots=[
        Slot("TEACH", "teach_card", "The three parts of a complete body paragraph",
             body=("You have practiced every part; now assemble them. A complete body paragraph has three "
                   "parts, joined so they connect: the CLAIM, the point this paragraph argues; the EVIDENCE, a "
                   "fact from a source, attributed and folded into your own sentence; and the WARRANT, a "
                   "sentence explaining WHY that evidence supports the claim. Claim, evidence, warrant. The most "
                   "common problem at this step is the partial paragraph, one that has a claim and evidence but "
                   "stops before the warrant, so the reader never learns why the fact matters. A complete "
                   "paragraph also connects its parts with functional transitions, no floating 'this.' You are "
                   "not learning new moves today; you are building the ones you know into one solid unit of "
                   "writing. Goal today: build a complete body paragraph with all three parts, cohered.")),
        Slot("TEACH", "stimulus_display", "Read the source: phones in school",
             ref="ACC-W910-ARG-LESSON-PHONEBAN", bank="phone_ban",
             body=("Read this source about phones in school. Because your job is to BUILD a paragraph with real "
                   "evidence, read the whole thing and pick one fact you can quote or paraphrase, and note who "
                   "reports it. You will use it as the evidence in your paragraph. The text stays on screen "
                   "while you work.")),
        Slot("TEACH", "discrimination", "Which paragraph is complete, and which is partial?",
             ref="", labeled_grade_c=True, bank="phone_ban",
             body=("Sort these before you build (spotting the target first, a Grade-C design bet we label as a "
                   "bet, not a proven ingredient). Both start the same way. Which is a COMPLETE body paragraph "
                   "(claim + evidence + warrant), and which is PARTIAL? "
                   "(A) Schools should limit phones in class. In a recent federal survey, the National Center for Education Statistics reported that most public schools, roughly three out of four, already restrict non-academic phone use during the school day.  "
                   "(B) Schools should limit phones in class. The National Center for Education Statistics "
                   "reports most public schools already restrict non-academic phone use. This wide adoption "
                   "matters because it shows the limit is workable, not radical. "
                   "Correct: B is complete; A is partial. (A) has a claim and attributed evidence but no "
                   "warrant, so it never says why the fact supports the claim. (B) adds the warrant, so all "
                   "three parts are present. A partial paragraph is the trap this lesson trains you to finish.")),
        Slot("MODEL", "annotated_before_after", "Watch a partial paragraph get completed",
             bank="phone_ban",
             body=("Here is a partial paragraph being completed by adding the missing warrant. Read the BEFORE, "
                   "then the AFTER, and notice the third part appear." + BEFORE_AFTER_HTML +
                   " The BEFORE stops after the evidence. The AFTER adds the warrant that explains why the fact "
                   "supports the claim, and connects the parts. Finishing all three parts is the build.")),
        Slot("MODEL", "predict_the_fix", "What does this partial paragraph most need?",
             bank="phone_ban",
             body=("Diagnose before the reveal. A paragraph reads: 'Phones distract students during lessons. "
                   "The National Center for Education Statistics reports that most schools now restrict phone "
                   "use.' Which single move would most improve it as a body paragraph? "
                   "(A) add a warrant explaining WHY that fact supports limiting phones, completing the "
                   "claim-evidence-warrant paragraph  "
                   "(B) add a second piece of evidence from another source so the paragraph piles up even more facts backing the phone claim  "
                   "(C) restate the claim about phones once more at the very end so the paragraph circles back and reminds readers of its point  "
                   "(D) make the sentences shorter and simpler so the two facts read more smoothly and feel a little less crowded on the page"),
             feedback=("Correct: A. The paragraph has a claim and attributed evidence but no warrant, so it is "
                       "partial. The fix completes it: 'This widespread restriction matters because it shows "
                       "schools already treat phones as a real distraction worth managing.' A second fact (B) "
                       "or a restated claim (C) do not supply the missing reasoning; shorter sentences (D) do "
                       "not add the warrant.")),
        Slot("SUPPORTED", "production_frq", "Build two of the three parts",
             ref="", bank="phone_ban", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=("Warm up the build. Start from this claim: 'Schools should limit phones during class.' Write "
                   "the EVIDENCE sentence (a fact from the source, attributed and folded in) AND the WARRANT "
                   "sentence (why that fact supports the claim), connected with a functional transition. Goal: "
                   "attributed evidence plus a real warrant, cohered. You are building two of the three parts "
                   "onto the given claim. Scored on Development/Organization.")),
        Slot("MODEL", "diagnosis_frq", "Check the parts before building the whole paragraph",
             ref="", bank="phone_ban", scored=True,
             body=("First watch the check run on a provided draft, then run it on a fresh paragraph of your "
                   "own. Provided draft: 'Phones hurt focus. Most schools restrict them.' Run the three-part "
                   "check step by step. Step 1, CLAIM clear? Yes. Step 2, EVIDENCE attributed and folded in? "
                   "No, the fact is dropped with no source, so attribute it. Step 3, WARRANT present? No, add "
                   "the why. Now you: write one fresh claim-plus-evidence-plus-start-of-warrant for the phone "
                   "topic, then run the same three checks. For each No, use the fix: attribute the evidence; "
                   "add the warrant. Finish by naming which of the three parts your paragraph still needs "
                   "most.")),
        Slot("INDEPENDENT", "production_frq", "Build a complete body paragraph",
             ref="", bank="phone_ban", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=("On your own now, build the whole paragraph. Write ONE complete body paragraph arguing a "
                   "claim about phones in class, with all three parts in order: CLAIM (your point), EVIDENCE "
                   "(a fact from the source, attributed and folded in), and WARRANT (why the evidence supports "
                   "the claim), connected with functional transitions. Before you submit, check the paragraph: "
                   "are all three parts present, is the evidence attributed, does the warrant explain the why, "
                   "do the parts connect? Fix any that fail before you submit. Scored on "
                   "Development/Organization.")),
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: free school meals",
             ref="ACC-W910-ARG-LESSON-SCHOOLLUNCH", bank="school_lunch",
             body=("Read this new source about free school meals. Because your job is to BUILD a paragraph with "
                   "real evidence, read the whole thing and pick one fact you can quote or paraphrase, and note "
                   "who reports it. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Build a complete body paragraph on a NEW topic",
             ref="", bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=("New topic. Write ONE complete body paragraph arguing a claim about free school meals, with "
                   "all three parts in order: CLAIM, EVIDENCE (attributed, folded in), and WARRANT (why the "
                   "evidence supports the claim), connected with functional transitions. Same build as the "
                   "phone paragraph, new topic. Do not stop at a partial paragraph. Scored on "
                   "Development/Organization.")),
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
