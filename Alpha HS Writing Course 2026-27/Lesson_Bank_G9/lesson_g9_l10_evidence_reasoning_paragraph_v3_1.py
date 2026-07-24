"""
lesson_g9_l12_evidence_reasoning_paragraph_v3_1.py  -  G9 KC C.9.03, PEW paragraph (sentence->paragraph). V3.1.

G9 L12, rebuilt to the v3.1 build spec (hand-authored; parallel agent stalled). Teaching point (kept): put the
moves together into ONE COMPLETE PARAGRAPH - state a Point, fold in attributed Evidence, add a Warrant (the
reasoning). KC C.9.03. This lesson CLIMBS the unit ladder: the SUPPORTED write is a sentence warm-up, the
INDEPENDENT + TRANSFER writes are a full paragraph (unit= values preserved so unit_ladder + type_ceiling pass).
Keeps bound fact-sourced stimuli (water_cycle taught -> animal_migration transfer). Deterministic FRQ prompts,
coping-model at paragraph grain, explicit-choices discrimination. 23 gates.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A body paragraph is three moves in order: '
'<strong>Point</strong>, then <strong>Evidence</strong>, then <strong>Warrant</strong>. A warrant is a '
'reasoning sentence that explains why the evidence supports the point.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 parts</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, check your paragraph has all three, in order:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0"><strong>Point</strong>: a claim sentence that says your position.</li>'
'<li style="margin:2px 0"><strong>Evidence</strong>: an attributed fact from the source, folded in.</li>'
'<li style="margin:2px 0"><strong>Warrant</strong>: a sentence saying why that evidence supports the point.</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">Missing one, or out of order, and the paragraph does not hold together.</div></div>')

COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer building the paragraph, part by part:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>Point:</strong> "The water cycle reuses the same water again and again." '
    'That is my claim. Now it needs evidence.</p>'
    '<p style="margin:0 0 8px"><strong>Evidence:</strong> "The source explains that water evaporates, '
    'condenses, and falls again in a continuous loop." Attributed and folded in. But a reader still needs to '
    'know why that proves my point.</p>'
    '<p style="margin:0"><strong>Warrant:</strong> "Because the same water keeps moving through those stages, no '
    'new water is made, which is exactly what \'reuse\' means." Now the three parts connect.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> Point + Evidence only: the reader is left to guess why the '
    'evidence proves the point.</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> Point + Evidence + Warrant: the warrant sentence spells out the '
    'link, so the paragraph holds together.</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C903-0012", grade="9-10", lesson_type=3,
    unit="G9 U2 - Evidence and reasoning (build the paragraph)",
    title="Build It Together: Point, Evidence, Warrant",
    target=("Put the moves together into one complete paragraph: state a point, fold in attributed evidence, and "
            "add a warrant that explains why the evidence supports the point. Sentence then paragraph. Trait: "
            "Development/Evidence."),
    acc_tags=["ACC.W.ARG.3", "CCSS.W.9-10.1b"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-14",
                "mnemonic_status": "established-caveat", "kc": "C.9.03",
                "sot": "icm course-G9.md L12; KC_Map_and_Unit_Arch_G9-12.md (G9 U2)",
                "taught_stimulus": "ACC-W910-INFO-LESSON-WATER-CYCLE",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-MIGRATION",
                "one_idea": "A body paragraph = Point, then Evidence, then Warrant, in order.",
                "one_reminder": "Check the 3 parts: point? attributed evidence? warrant that links them?",
                "version_note": ("V3.1 rebuild (hand-authored; parallel agent stalled). PARAGRAPH-level: SUPPORTED "
                                 "write = sentence warm-up, INDEPENDENT + TRANSFER = full paragraph (unit ladder "
                                 "sentence->paragraph PRESERVED). Kept bound fact-sourced stimuli. v3.1 spine + "
                                 "paragraph-grain coping-model + deterministic FRQ prompts."),
                "review_provenance": "built to the L01 v3.1 pattern"},
    fade_ledger_moves=["point-evidence-warrant", "paragraph-assembly", "warrant"],
    slots=[
        Slot("TEACH", "teach_card", "The one idea: Point, Evidence, Warrant",
             body=(ONE_IDEA +
                   "You have practiced each move on its own. A body paragraph puts three of them together, in "
                   "order:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Point</strong>: the claim sentence that opens the "
                   "paragraph and says your position.</li>"
                   "<li style=\"margin:4px 0\"><strong>Evidence</strong>: an attributed fact from the source, "
                   "folded into your own sentence.</li>"
                   "<li style=\"margin:4px 0\"><strong>Warrant</strong>: a warrant is the reasoning sentence that "
                   "says WHY that evidence supports the point.</li></ul>"
                   "The order matters: point first so the reader knows your position, then evidence, then the "
                   "warrant that links them. Leave out the warrant and the reader has to guess the connection.")),
        Slot("TEACH", "stimulus_display", "The source: the water cycle",
             ref="ACC-W910-INFO-LESSON-WATER-CYCLE", bank="water_cycle",
             body=("Read this source about the water cycle. You will build a paragraph from it, so pick a point "
                   "you could make and a fact that supports it.")),
        Slot("MODEL", "annotated_before_after", "Watch a writer build the paragraph",
             bank="water_cycle",
             body=("Here is the skill in action. Follow the writer building the paragraph part by part. " +
                   COPING_HTML +
                   " Notice the difference: point + evidence alone leaves the link unstated; adding the warrant "
                   "makes the paragraph hold together." + REMEMBER +
                   "When you build your own, put the three parts in order, then run the check.")),
        Slot("MODEL", "discrimination", "Which paragraph has all three parts, in order?",
             ref="", labeled_grade_c=True, bank="water_cycle",
             body=("Spot the target before you build it. Which option is a complete Point-Evidence-Warrant "
                   "paragraph? "
                   "(A) The water cycle reuses water. The source explains that water evaporates, condenses, and falls again. It is an interesting natural process to learn.  "
                   "(B) The source explains that water evaporates, condenses, and falls again. So the water cycle matters a great deal to all of us on Earth.  "
                   "(C) The water cycle reuses the same water. The source explains that water evaporates, condenses, and falls, which shows no new water is made.  "
                   "(D) The source explains that water evaporates, condenses, and falls, which shows no new water is made, so the water cycle reuses the same water. "
                   "Correct: C. (D) has all three parts but leads with the evidence and buries the point at the end, so the order is wrong."),
             choices=[
                 {"id": "A", "text": "The water cycle reuses water. The source explains that water evaporates, condenses, and falls again. It is an interesting natural process to learn.",
                  "correct": False,
                  "why": "Point and evidence are there, but the last sentence is a filler comment, not a warrant, so the link between the evidence and the point is never stated."},
                 {"id": "B", "text": "The source explains that water evaporates, condenses, and falls again. So the water cycle matters a great deal to all of us on Earth.",
                  "correct": False,
                  "why": "It leads with evidence and has no clear point sentence, and the closing line is a vague significance claim, not a warrant tying the evidence to a position."},
                 {"id": "C", "text": "The water cycle reuses the same water. The source explains that water evaporates, condenses, and falls, which shows no new water is made.",
                  "correct": True,
                  "why": "Correct. Point (reuses water), attributed evidence (the paraphrased stages, named to the source), then a warrant ('which shows no new water is made') that links the evidence to the point, in order."},
                 {"id": "D", "text": "The source explains that water evaporates, condenses, and falls, which shows no new water is made, so the water cycle reuses the same water.",
                  "correct": False,
                  "why": "All three parts are here, but they are out of order: it opens with the evidence and leaves the point for the end, so the reader does not know your position until the paragraph is over. The point has to come first."},
             ]),
        Slot("MODEL", "predict_the_fix", "This paragraph is missing a part. Which one?",
             bank="water_cycle",
             body=("Diagnose this draft before the reveal. A student wrote: 'The water cycle reuses the same "
                   "water. The source explains that water evaporates, condenses, and falls again.' Which single move "
                   "would most improve it? "
                   "(A) add a warrant sentence saying why the evidence proves the point  "
                   "(B) add a second, entirely separate quoted fact from the source right after the first one  "
                   "(C) move the point sentence all the way down to the very end of the whole paragraph  "
                   "(D) make the opening point sentence quite a bit longer and much more detailed"),
             feedback=("Correct: A. The paragraph has a point and evidence but no warrant, so the reader must "
                       "guess why the stages prove that water is reused. The fix is one warrant sentence: '...which "
                       "shows no new water is made, so the same water is reused.' A second fact (B), reordering "
                       "(C), or a longer point (D) do not supply the missing reasoning link.")),
        Slot("SUPPORTED", "production_frq", "Warm up: write the warrant sentence",
             ref="", bank="water_cycle", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="Warm up the build with just the warrant. Here is a point and its evidence:",
                 setapart_block=setapart("Point + evidence given:",
                                         "The water cycle reuses the same water. The source explains that water evaporates, condenses, and falls again."),
                 closer="Write ONE warrant sentence that says why that evidence supports the point (start with "
                        "'which shows' or 'because'). Then check it links the two.")),
        # COUNCIL FIX (2026-07-24): Option A (later-in-arc). One graded rewrite; checks read-only beneath; name-act dropped.
        Slot("MODEL", "diagnosis_frq", "Fix a paragraph that is missing a part",
             ref="", bank="water_cycle", rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="This weak paragraph is missing a part. Its point is vague ('is important' takes no real "
                       "position), and it has no warrant to link the evidence to the point. Rewrite it as a "
                       "complete paragraph with all three parts in order.",
                 setapart_block=setapart("Weak paragraph to fix:",
                                         "The water cycle is important. The source explains that water evaporates, condenses, and falls again.", "red"),
                 checklist_block=checklist(title="Make your rewrite pass these (no need to type answers):", rows=[
                     "Point: a clear claim sentence that takes a position?",
                     "Evidence: an attributed fact from the source, folded in?",
                     "Warrant: a sentence that says why the evidence supports the point?",
                 ]),
                 closer="Put the point first, then the attributed evidence, then a warrant. Run the 3-part check "
                        "above before you submit.")),
        Slot("INDEPENDENT", "production_frq", "Build the whole paragraph on the water cycle",
             ref="", bank="water_cycle", rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now, build the whole paragraph about the water cycle.",
                 closer="Write ONE paragraph with all three parts in order: Point (your claim), Evidence (an "
                        "attributed fact from the source), Warrant (why it supports the point). Assembling the "
                        "parts into a paragraph is the real move, and you are ready to do it cold. Run the "
                        "3-part check before you submit.")),
        Slot("TRANSFER", "stimulus_display", "The source: animal migration",
             ref="ACC-W910-INFO-LESSON-MIGRATION", bank="animal_migration",
             body=("A new source. Read it and pick a point you could make plus a fact that supports it. Same "
                   "three-part build, new topic.")),
        Slot("TRANSFER", "production_frq", "Build a paragraph on a NEW topic",
             ref="", bank="animal_migration", rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="New topic. Build ONE paragraph about animal migration.",
                 closer="Put all three parts in order: Point, Evidence (attributed), Warrant. Run the 3-part "
                        "check before you submit.")),
    ],
)

LESSONS = [LESSON]

if __name__ == "__main__":
    ok = True
    for L in LESSONS:
        qc_lesson(L); print(qc_report(L)); print(); ok = ok and L.qc["passed"]
    print(f"{sum(1 for L in LESSONS if L.qc['passed'])}/{len(LESSONS)} PASS")
    sys.exit(0 if ok else 1)
