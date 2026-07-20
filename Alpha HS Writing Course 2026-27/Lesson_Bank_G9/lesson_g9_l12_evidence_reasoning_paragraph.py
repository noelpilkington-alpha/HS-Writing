"""
lesson_g9_l12_evidence_reasoning_paragraph.py  -  G9 KC C.9.03, ARCHETYPE T3: EVIDENCE-INTEGRATION (PROVE, paragraph).

G9 course L12. Independent capstone of Unit 2 + the FIRST grain climb (sentence -> paragraph): put evidence and
reasoning TOGETHER in a complete claim-evidence-warrant paragraph (W1 + G/I). Recycles G1/G2/I1/I2 + W1/W2.
Locked L01 template; EVIDENCE-TIER binds full sources. Taught: WATER-CYCLE (full) -> transfer: MIGRATION (full,
partitioned). rc.staar. The INDEPENDENT + TRANSFER productions declare unit="paragraph" (the climb); earlier
slots stay sentence, so the unit ladder is non-decreasing and tops at paragraph (T3 ceiling). PROVE=
established-caveat; no coping-model persona; no source markup; no prior-work ref; no em dashes.
Runs QC on execution.
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
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> the parts are there but not built together</span>'
    '<p style="margin:8px 0 0;font-size:15px">The water cycle recycles water. "The same water has circled for '
    'billions of years." It is important.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">There is a point, a dropped quote, and a vague "it '
    'is important." Nothing is attributed, nothing explains why the quote proves the point. The parts do not '
    'form a paragraph.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> a built paragraph: point, evidence, warrant</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">POINT</span> The water cycle constantly reuses the planet\'s water. '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">EVIDENCE</span> As the U.S. Geological Survey explains, "the same water has been '
      'circling the planet for billions of years," moving from surface to sky and back. '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">WARRANT</span> This matters because it shows the supply is not created or used up but '
      'recycled, which is why protecting water quality protects a fixed, shared resource.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Point, then attributed evidence folded in, then a '
    'warrant explaining why it proves the point. Built together, the parts form a paragraph.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C903-0012", grade="9-10", lesson_type=3,
    unit="G9 U2 - Reasoning (evidence + reasoning together: the paragraph)",
    title="Build It Together: Point, Evidence, Warrant",
    target=("Put the moves together into one complete paragraph: state a point, fold in attributed evidence, "
            "and add a warrant that explains why the evidence proves the point. Climbs from the sentence to the "
            "paragraph. Trait: Evidence/Development."),
    acc_tags=["ACC.W.ARG.2", "CCSS.W.9-10.1b"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12",
                "mnemonic_status": "established-caveat", "kc": "C.9.03", "sot": "icm course-G9.md L12",
                "taught_stimulus": "ACC-W910-INFO-LESSON-WATER-CYCLE",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-MIGRATION",
                "playbook": "_phase2/playbook_T3_PROVE.md",
                "template": "locked L01 template; EVIDENCE-TIER binds full sources. First grain climb: paragraph ceiling.",
                "council": ("T3/PROVE independent capstone + grain climb: combines W1 warrant + G/I evidence "
                            "into a complete claim-evidence-warrant paragraph. built-together vs parts-not-"
                            "connected discrimination labeled Grade-C. unit=paragraph on the independent + "
                            "transfer productions (non-decreasing ladder; T3 ceiling=paragraph).")},
    fade_ledger_moves=["point-evidence-warrant-paragraph", "combine-evidence-and-reasoning"],
    slots=[
        Slot("TEACH", "teach_card", "Put the moves together into a paragraph",
             body=("You have practiced the moves one at a time: name a source, pick relevant evidence, fold it "
                   "in, and explain your reasoning. Now build them into one complete paragraph. A strong "
                   "evidence-and-reasoning paragraph has three parts in order: the POINT, one sentence stating "
                   "the claim the paragraph makes; the EVIDENCE, a fact from the source, attributed and folded "
                   "into your own sentence; and the WARRANT. A warrant is a sentence that explains WHY that "
                   "evidence proves the point, the reasoning a reader needs to accept the connection. Point, "
                   "evidence, warrant. The trap at this step is listing the parts without "
                   "building them together: a point, then a dropped quote, then a vague 'it is important,' with "
                   "no attribution and no reasoning. That reads as scattered pieces, not a paragraph. Goal "
                   "today: write one paragraph that states a point, folds in attributed evidence, and warrants "
                   "why the evidence proves the point.")),
        Slot("TEACH", "stimulus_display", "Read the source: the water cycle",
             ref="ACC-W910-INFO-LESSON-WATER-CYCLE", bank="water_cycle",
             body=("Read this source about the water cycle. Because your job is to build a full paragraph, read "
                   "the whole thing and pick one point you could make plus a fact that supports it, and note "
                   "who reports the fact. The text stays on screen while you work.")),
        Slot("TEACH", "discrimination", "Which one is a built paragraph, not scattered parts?",
             ref="", labeled_grade_c=True, bank="water_cycle",
             body=("Sort these before you write (spotting the target before producing it, a Grade-C design bet "
                   "we label as a bet, not a proven ingredient). Both use the same point and fact. Which one is "
                   "built together as a point-evidence-warrant paragraph? "
                   "(A) The water cycle recycles water. Water is found everywhere on the planet in many "
                   "different forms. \"The same water has circled for billions of years.\" Rain falls, rivers "
                   "flow, and clouds keep forming over and over. It is important. Water is a big deal.  "
                   "(B) The water cycle constantly reuses the planet's water. As the U.S. Geological Survey "
                   "explains, the same water has circled the planet for billions of years. This matters because "
                   "it shows the supply is recycled, not created or used up. "
                   "Correct: B. (A) lists a point, a dropped quote, and a vague 'it is important,' with no "
                   "source and no reasoning. (B) states the point, folds in attributed evidence, and warrants "
                   "why it proves the point. Built together, it is a paragraph.")),
        Slot("MODEL", "annotated_before_after", "Watch scattered parts become a built paragraph",
             bank="water_cycle",
             body=("Here are scattered parts being built into a point-evidence-warrant paragraph. Read the "
                   "BEFORE, then the AFTER, and notice the three labeled parts in order." + BEFORE_AFTER_HTML +
                   " The BEFORE lists pieces. The AFTER builds them: POINT, then attributed EVIDENCE folded in, "
                   "then a WARRANT explaining why. Building the parts together is the move.")),
        Slot("MODEL", "predict_the_fix", "What does this scattered draft most need?",
             bank="water_cycle",
             body=("Diagnose this draft before the reveal. A student wrote: The water cycle is a loop. \"The "
                   "same water has been circling for billions of years.\" Water is everywhere. Which single "
                   "move would most improve it as a paragraph? "
                   "(A) attribute the quote and add a warrant explaining why it proves the point, building the "
                   "parts into a point-evidence-warrant paragraph  "
                   "(B) add two or three more facts about water from the source so the paragraph has more "
                   "evidence to back up the point it makes about the cycle  "
                   "(C) expand the point sentence with more detail about the water cycle so it is longer and "
                   "reads as more fully developed and complete  "
                   "(D) move the quote to the start of the paragraph so the strongest evidence comes first and "
                   "grabs the reader before the point is made"),
             feedback=("Correct: A. The draft has a point and a dropped quote but no attribution and no warrant, "
                       "so it reads as scattered parts. The fix is to build the paragraph: attribute the quote "
                       "(the U.S. Geological Survey) and add a warrant ('this matters because it shows the "
                       "supply is recycled, not used up'). More facts (B), a longer point (C), or reordering "
                       "(D) do not connect the parts into a paragraph.")),
        Slot("SUPPORTED", "production_frq", "Assemble two of the three parts",
             ref="", bank="water_cycle", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("Warm up the build in one sentence first. Take this point: 'The water cycle reuses the same "
                   "water.' Write ONE sentence that folds in an attributed fact from the source AND begins the "
                   "warrant: '______ [source] explains that ______ [fact], which matters because ______.' Goal: "
                   "evidence attributed and folded in, plus the start of a warrant. Write one sentence. Scored "
                   "on Evidence/Development.")),
        Slot("MODEL", "diagnosis_frq", "Check the parts before you build the whole paragraph",
             ref="", bank="water_cycle", scored=True,
             body=("First watch the check run on a weak draft, then run it on a fresh sentence of your own. "
                   "Weak draft: 'The water cycle matters. \"Water circles for billions of years.\"' Run the "
                   "three-part check step by step. Step 1, POINT clear? Yes, but vague ('matters'), sharpen it. "
                   "Step 2, EVIDENCE attributed and folded in? No, it is a dropped quote with no source, so "
                   "attribute and weave it. Step 3, WARRANT present? No, add the why. Now you: write one fresh "
                   "sentence that folds in attributed evidence and begins a warrant, then run the same three "
                   "checks. For each No, use the fix: sharpen the point; attribute and fold the evidence; add "
                   "the because-why. Finish by naming which part your paragraph will still need most.")),
        Slot("INDEPENDENT", "production_frq", "Write a full point-evidence-warrant paragraph",
             ref="", bank="water_cycle", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=("On your own now, build the whole paragraph. Write ONE paragraph about the water cycle with "
                   "all three parts in order: (1) POINT, state your claim in a sentence; (2) EVIDENCE, fold in "
                   "an attributed fact from the source; (3) WARRANT, explain WHY that evidence proves your "
                   "point. Before you submit, check the paragraph: is the point clear, is the evidence "
                   "attributed and folded in (not dropped), does the warrant explain the why? If any answer is "
                   "no, fix it before you submit. Scored on Evidence/Development.")),
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: animal migration",
             ref="ACC-W910-INFO-LESSON-MIGRATION", bank="animal_migration",
             body=("Read this new source about animal migration. Because your job is to build a full paragraph, "
                   "read the whole thing and pick one point plus a supporting fact, and note who reports it. "
                   "The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Write a point-evidence-warrant paragraph on a NEW topic",
             ref="", bank="animal_migration", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=("New topic. Write ONE paragraph about animal migration with all three parts in order: POINT "
                   "(your claim), EVIDENCE (an attributed fact from the source, folded in), and WARRANT (why "
                   "the evidence proves the point). Same build as the water-cycle paragraph, new topic. Do not "
                   "list scattered parts. Scored on Evidence/Development.")),
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
