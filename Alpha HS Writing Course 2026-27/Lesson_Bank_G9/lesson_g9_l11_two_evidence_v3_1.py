"""
lesson_g9_l28_two_evidence_v3_1.py  -  G9 KC C.9.03, ARCHETYPE T3: EVIDENCE-INTEGRATION (PROVE, ceiling
paragraph). V3.1. NEW LESSON added 2026-07-14 per the Fable-5 course-design audit (evidence-development gap):
every G9 paragraph capped at ONE piece of evidence, leaving CCSS W.9-10.2b ("develop the topic with well-chosen,
relevant, and SUFFICIENT facts") untaught. Noel's decision: add one G9 lesson. C.9.03 now claims INFO.2 +
W.9-10.2b (Wave-1 SoT edit).

TEACHING POINT: develop ONE point with TWO complementary pieces of evidence. Select two facts that add up (not
two versions of the same fact), order them so the second builds on the first, and write ONE warrant that ties
BOTH to the point. This is the step from a formulaic one-fact paragraph to a developed one. Bound to a real
fact-sourced stimulus (needs two citable facts): taught ARG-LESSON-AIWORKFORCE -> transfer ARG-LESSON-GRIDSPENDING,
partitioned. Sentence-then-paragraph ladder (SUPPORTED = pick+order the two; INDEPENDENT/TRANSFER = full
paragraph). PROVE mnemonic (established-caveat).

Built to icm/_config/v3_1-lesson-build-spec.md. Own words, facts drawn faithfully from the bound sources (BLS
figures as stated in the source), no fabricated figures, no em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">One fact makes a point; <strong>two that add up</strong> '
'develop it. Pick two pieces of evidence that build on each other, order them, and write one '
'<strong>warrant</strong> that ties BOTH to your point.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit a two-evidence paragraph, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Do the two pieces ADD something (not just repeat the same fact)?</li>'
'<li style="margin:2px 0">Are they ordered so the second builds on the first?</li>'
'<li style="margin:2px 0">Does one warrant tie BOTH pieces to the point?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">Two facts that say the same thing are still one piece of evidence. They must add up.</div></div>')

# coping-model think-aloud: a WRITTEN build (pick fact 1 -> test if fact 2 adds -> order -> one warrant for both),
# then the endpoints. Literal BEFORE and AFTER (content_depth). No named near-peer (Timeback rule). Facts as
# stated in ARG-LESSON-AIWORKFORCE (BLS: ~3.1% overall growth; data scientists 33.5%).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer developing one point with two facts (point: technology jobs are growing far faster than jobs overall):</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First fact:</strong> "The Bureau of Labor Statistics projects data-science '
    'jobs will grow about 33.5 percent from 2024 to 2034." That is a big number, but big compared to what? On its '
    'own it does not show the gap.</p>'
    '<p style="margin:0 0 8px"><strong>Second fact that ADDS:</strong> "The Bureau projects total employment '
    'across all jobs will grow only about 3.1 percent over the same decade." Now the two ADD UP: one is the tech '
    'rate, the other the baseline. Order them baseline-then-tech, or tech-then-baseline, so the contrast lands.</p>'
    '<p style="margin:0"><strong>One warrant for both:</strong> "Because data-science jobs are growing more than '
    'ten times faster than the job market as a whole, the growth in technology is not ordinary, it is a real '
    'shift." One warrant ties BOTH numbers to the point.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> One fact only: "data-science jobs will grow about 33.5 percent." '
    '(a number with nothing to compare it to)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> Two facts that add up (33.5 percent for tech vs about 3.1 percent '
    'overall) plus one warrant, so the point is developed, not just stated.</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C903-0028", grade="9-10", lesson_type=3,
    unit="G9 U2 - Reasoning + the complete paragraph (develop a point with two pieces of evidence)",
    title="Two Pieces of Evidence, One Point",
    target=("Develop one point with TWO complementary pieces of evidence: select two facts that add up (not two "
            "versions of one fact), order them so the second builds on the first, and write one warrant that ties "
            "BOTH to the point. Sentence then paragraph. Trait: Development/Evidence."),
    acc_tags=["ACC.W.INFO.2", "CCSS.W.9-10.2b"],
    provenance={"copyright": "own_authored", "authored": "2026-07-14",
                "mnemonic_status": "established-caveat", "kc": "C.9.03",
                "sot": "COURSE_DESIGN_AUDIT_2026-07-14.md (evidence-development gap); C.9.03 now claims INFO.2 + W.9-10.2b",
                "taught_stimulus": "ACC-W910-ARG-LESSON-AIWORKFORCE",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-GRIDSPENDING",
                "template": "v3.1 lesson build spec; cloned from L12 (T3/PROVE paragraph build). EVIDENCE-TIER binds a full fact-sourced source (needs two citable facts).",
                "one_idea": "Develop a point with two facts that ADD UP, ordered, tied by one warrant.",
                "one_reminder": "3-question check: do the two facts add? ordered so the second builds? one warrant for both?",
                "version_note": ("NEW lesson (design-audit gap): every G9 paragraph capped at one piece of "
                                 "evidence, so CCSS W.9-10.2b 'sufficient facts' was untaught. Teaches selecting + "
                                 "ordering + jointly-warranting TWO complementary facts. Facts drawn faithfully "
                                 "from ARG-LESSON-AIWORKFORCE (BLS ~3.1% overall vs 33.5% data science, as stated "
                                 "in the source). Sentence-then-paragraph ladder preserved (T3 ceiling paragraph). "
                                 "Discrimination confound broken: a distractor gives TWO facts that only repeat "
                                 "the same idea, so the invariant is 'the two facts ADD UP,' not 'has two facts.'"),
                "review_provenance": "built to icm/_config/v3_1-lesson-build-spec.md (pattern clearing all 23 gates + Fable-5).",
                "council": "T3/PROVE evidence-development: extends single-PEW to two-evidence development (W.9-10.2b). two-add-up-vs-two-repeat discrimination labeled Grade-C in code. PROVE=established-caveat; ceiling paragraph."},
    fade_ledger_moves=["select-two-complementary-facts", "order-evidence", "one-warrant-for-two"],
    slots=[
        # ===== TEACH: ONE idea in a callout + the add-up vs repeat contrast as a real LIST =====
        Slot("TEACH", "teach_card", "The one idea: two facts that add up, one warrant",
             body=(ONE_IDEA +
                   "You can already build a paragraph with a point, one fact, and a warrant. A developed "
                   "paragraph often needs more than one fact, but only if the second fact ADDS something. Keep "
                   "two kinds apart:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Two that ADD UP</strong>: each fact does a different job "
                   "for the point, for example one gives a rate and the other gives the baseline it should be "
                   "compared to, so together they show more than either alone.</li>"
                   "<li style=\"margin:4px 0\"><strong>Two that REPEAT</strong>: both facts make the same point "
                   "in slightly different words, so the second adds no new information. Two repeats still count "
                   "as one piece of evidence.</li></ul>"
                   "When two facts add up, order them so the second builds on the first, then write ONE warrant "
                   "that ties BOTH to your point (not one warrant per fact). A warrant is a reasoning sentence "
                   "that says WHY the evidence supports the point, the move you practiced earlier. Goal: develop "
                   "a point with two complementary facts, ordered, tied by a single warrant.")),
        Slot("TEACH", "stimulus_display", "The source: steering workers toward growing fields",
             ref="ACC-W910-ARG-LESSON-AIWORKFORCE", bank="ai_workforce",
             body=("Read this source. It gives several real figures from the Bureau of Labor Statistics. You will "
                   "develop one point from it using two facts that add up, so as you read, look for a pair of "
                   "figures that belong together.")),

        # ===== MODEL (before the quiz): coping-model think-aloud with the check tool folded in =====
        Slot("MODEL", "annotated_before_after", "Watch a writer develop a point with two facts",
             bank="ai_workforce",
             body=("Here is the skill in action. Follow the writer choosing and ordering two facts, then tying "
                   "both to the point. " + COPING_HTML +
                   " Notice the move: the second fact was chosen because it ADDS a baseline the first fact needs, "
                   "and one warrant ties both to the point. " + REMEMBER +
                   "When you build your own, pick a second fact that adds, order the two, and write one warrant "
                   "for both, then run the 3 questions.")),
        Slot("MODEL", "discrimination", "Which paragraph develops the point with two facts that add up?",
             ref="", labeled_grade_c=True, bank="ai_workforce",
             body=("Now that you have seen one built, spot the target. The point is: technology jobs are growing "
                   "far faster than jobs overall. Which option develops it with two facts that ADD UP (not two "
                   "that repeat)? "
                   "(A) Technology jobs are growing fast. The source says that data-science jobs will grow a great "
                   "deal over the coming decade, and it also says, in another sentence a little later on, that "
                   "data-science jobs are one of the quickest-expanding fields around right now, which really "
                   "goes to show just how fast these particular technology jobs are growing overall.  "
                   "(B) Technology jobs are growing far faster than jobs overall. The Bureau projects data-science "
                   "jobs will grow about 33.5 percent while all jobs grow only about 3.1 percent. Because the tech "
                   "rate is more than ten times the overall rate, the growth is not part of a general boom but a "
                   "shift concentrated in a few fields.  "
                   "(C) Technology jobs are growing fast, which is honestly pretty exciting to think about, and "
                   "lots of students seem to be really interested in going into them these days, so studying one "
                   "of those fields is probably a smart and sensible idea for just about anyone who happens to be "
                   "thinking ahead about the future. "
                   "Correct: B. Two facts that add up (the tech rate AND the overall baseline), ordered, plus a warrant sentence that explains why the gap matters."),
             choices=[
                 {"id": "A", "text": "Technology jobs are growing fast. The source says that data-science jobs will grow a great deal over the coming decade, and it also says, in another sentence a little later on, that data-science jobs are one of the quickest-expanding fields around right now, which really goes to show just how fast these particular technology jobs are growing overall.",
                  "correct": False,
                  "why": "It has two sentences of evidence, but both say the same thing (data-science jobs grow fast). Two facts that repeat are still one piece of evidence; nothing is added."},
                 {"id": "B", "text": "Technology jobs are growing far faster than jobs overall. The Bureau projects data-science jobs will grow about 33.5 percent while all jobs grow only about 3.1 percent. Because the tech rate is more than ten times the overall rate, the growth is not part of a general boom but a shift concentrated in a few fields.",
                  "correct": True,
                  "why": "Correct. The 33.5 percent tech rate and the 3.1 percent overall baseline do different jobs and add up, and the last sentence is a real warrant: it explains WHY the gap matters (the growth is concentrated, not general), not just a restatement of the point."},
                 {"id": "C", "text": "Technology jobs are growing fast, which is honestly pretty exciting to think about, and lots of students seem to be really interested in going into them these days, so studying one of those fields is probably a smart and sensible idea for just about anyone who happens to be thinking ahead about the future.",
                  "correct": False,
                  "why": "No attributed facts from the source at all, just opinions and asides. Developing a point needs real evidence that adds up, not general enthusiasm."},
             ]),
        Slot("MODEL", "predict_the_fix", "This paragraph has two facts. What does it most need?",
             bank="ai_workforce",
             body=("Diagnose this draft: 'Technology jobs are growing far faster than jobs overall. The Bureau "
                   "projects data-science jobs will grow about 33.5 percent, and all jobs only about 3.1 "
                   "percent.' Which single move would most improve it? "
                   "(A) add one warrant that ties both figures to the point, explaining what the gap between the two rates shows  "
                   "(B) delete the second figure so the paragraph is shorter and rests on just one clear number instead of two  "
                   "(C) add a third and a fourth figure from the source so the paragraph simply has as many facts as possible  "
                   "(D) move the point sentence to the very end so the two figures come first and the reader reaches the claim last"),
            feedback=("Correct: A. The two facts already add up (the tech rate and the overall baseline it "
                       "should be compared to), but no sentence says what the gap between them shows, so the "
                       "reader supplies the link. One warrant fixes it: 'so technology jobs are growing more "
                       "than ten times faster than the market as a whole.' Deleting a fact (B) loses "
                       "development; piling on facts (C) is not development; reordering (D) does not add the "
                       "missing warrant.")),

        # ===== SUPPORTED: framed build (pick + order the two facts) on the taught source =====
        Slot("SUPPORTED", "production_frq", "Warm up: pick and order the second fact",
             ref="", bank="ai_workforce", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Warm up the build. Here is a point and its first fact, from the source:",
                 setapart_block=setapart("Point + first fact given:",
                                         "Point: technology jobs are growing far faster than jobs overall. First fact: the Bureau projects data-science jobs will grow about 33.5 percent from 2024 to 2034."),
                 closer="From the source, choose a SECOND fact that ADDS to the first (a baseline to compare it "
                        "to), and write the two facts in an order where the second builds on the first. Then "
                        "check the two add up before you submit.")),
        # DIAGNOSIS = run the 3-part check on a PROVIDED weak paragraph, then fix it. Taught source = no new read.
        Slot("MODEL", "diagnosis_frq", "Check and fix a two-evidence paragraph",
             ref="", bank="ai_workforce", scored=True,
             body=frq_prompt(
                 intro="Run the 3-question check on this weak paragraph, then fix what is missing.",
                 setapart_block=setapart("Weak paragraph to fix:",
                                         "Technology jobs are booming. The Bureau projects data-science jobs will grow about 33.5 percent, and data-science jobs are one of the fastest-growing fields around.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Do the two pieces ADD something?", "No, both say data-science jobs grow fast. Swap the second for a fact that adds, like the overall growth rate."),
                     ("Are they ordered so the second builds on the first?", "Cannot tell yet, they repeat. Fix the second fact first."),
                     ("Does one warrant tie both to the point?", "No warrant at all. Add one that says what the two figures show together."),
                 ]),
                 closer="Now rewrite it as a developed paragraph: point, two facts that add up (in order), and one "
                        "warrant tying both to the point. Then name which part your rewrite fixed.")),

        # ===== INDEPENDENT: full paragraph on the taught source + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Develop the whole paragraph with two facts",
             ref="", bank="ai_workforce", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="On your own now, develop one paragraph from the source using two facts that add up.",
                 closer="Write ONE paragraph: a point, two attributed facts from the source that add up (ordered "
                        "so the second builds on the first), and one warrant that ties both to the point. "
                        "Developing a point with sufficient, complementary evidence is what separates a real body "
                        "paragraph from a formula, and you are ready to do it cold. Run the 3 questions before "
                        "you submit.")),

        # ===== TRANSFER: same move, a NEW source (grid spending), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "The source: build the power, or build the grid?",
             ref="ACC-W910-ARG-LESSON-GRIDSPENDING", bank="grid_spending",
             body=("A new source. Read it and find two facts that add up for a point you could make. Same "
                   "two-evidence build, new topic.")),
        Slot("TRANSFER", "production_frq", "Develop a paragraph on a NEW source",
             ref="", bank="grid_spending", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="New source. Develop ONE paragraph from it with two facts that add up.",
                 closer="Point, two attributed facts that add up (ordered), and one warrant tying both to the "
                        "point. Run the 3 questions before you submit.")),
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
