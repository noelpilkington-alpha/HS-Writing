"""
lesson_g11_l15_calibrate_own_synthesis.py  -  G11 KC C.11.02, ARCHETYPE T8: CROSS-SOURCE-SYNTHESIS (WEAVE,
essay) with a K2 CHECK / calibration overlay. V3.1.

G11 course L15 (Unit 3, check), rebuilt to the v3.1 build spec (hand-authored). Teaching point (KEPT):
predict your OWN synthesis's rubric score row by row with reasons, submit it to the grader, then name the GAP
between your prediction and the real score. K2 own-work calibration is stateless-safe (the student's fresh
writing is routed to the grader; nothing depends on stored prior state).

Preserved EXACTLY from the prior L15: id="ACC-W1112-L-G11-C1103-0015", lesson_type=8,
mnemonic_status="proposal", kc="C.11.02", unit, the bound stimuli (SYNTH-LESSON-0001 water set taught ->
SYNTH-SET-0002 AI-workforce set transfer), and the essay production ceiling. Grain note: the map tags this
T5|essay|check, but T5 caps at paragraph, so the QC lesson_type is 8 (WEAVE, essay ceiling) since the
calibration operates on a full synthesis essay; the predict-then-reveal calibration pedagogy is enforced by
the self_score / calibration gate independent of type.

V3.1 changes vs the prior L15 (the two wall-of-text teach cards + the leaked internal label + the spine polish):
  1. FIXED the two prose-wall teach cards: they are now a ONE_IDEA teal callout + real <ul>/<ol> lists (the
     parts, then the routine), so no >45-word block runs without a break (format_fidelity).
  2. FIXED the leaked internal label: the discrimination no longer says "a Grade-C design bet we label as a
     bet"; it is a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}].
  3. Deterministic FRQ + diagnosis bodies via frq_prompt/setapart/checklist (no "Step N" prose, no "Scored on"
     chrome); coping-model before/after kept; the calibration check folded in at first use as a REMEMBER <ol> box.
Own words, facts faithful to the bound USGS/EPA/EIA source set, no fabricated figures, no em dashes. Passes all
23 lesson_contract gates + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A strong writer can predict their own synthesis '
'score <strong>before the grader does</strong>, but only by predicting on the rubric <strong>rows</strong> with '
'reasons, never on a feeling.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: calibrate the prediction</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you trust a prediction, ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Did I give a number for each rubric row (Development and Evidence)?</li>'
'<li style="margin:2px 0">Did I write the reason for each number from what my writing actually does?</li>'
'<li style="margin:2px 0">After the row check, did I name the gap on every row where my number was off?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, the prediction is a guess, not a calibration.</div></div>')

# the rubric the student predicts against: the two rows (Development, Evidence) with what each 1-to-4 level means.
# Descriptors are consistent with the lesson's own worked examples (self_score sample = Development 2 / Evidence 2;
# before/after = Development 3, Evidence 2 for leaning on one source). Shown in TEACH so prediction is grounded.
RUBRIC = (
'<div style="border:1px solid #99f6e4;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f0fdfa;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The two rows you predict on (each scored 1 to 4)</div>'
'<div style="color:#1f2a44;font-size:14px;margin:6px 0 2px"><strong>Development</strong> (does it weave ONE argument from the set?)</div>'
'<ul style="color:#1f2a44;font-size:13px;margin:2px 0 6px;padding-left:22px">'
'<li style="margin:2px 0"><strong>4</strong>: one clear argument the whole synthesis builds; every source serves it.</li>'
'<li style="margin:2px 0"><strong>3</strong>: one argument, but a source or two sit to the side instead of serving it.</li>'
'<li style="margin:2px 0"><strong>2</strong>: it names or tours the sources, but no single argument ties them together.</li>'
'<li style="margin:2px 0"><strong>1</strong>: a list or summary, with no argument.</li></ul>'
'<div style="color:#1f2a44;font-size:14px;margin:6px 0 2px"><strong>Evidence</strong> (does it use and weight the sources?)</div>'
'<ul style="color:#1f2a44;font-size:13px;margin:2px 0 0;padding-left:22px">'
'<li style="margin:2px 0"><strong>4</strong>: it uses several sources and weights each by what it can carry, so the strongest carry the most.</li>'
'<li style="margin:2px 0"><strong>3</strong>: it uses several sources but leans on them about equally, without weighting.</li>'
'<li style="margin:2px 0"><strong>2</strong>: it leans on one source harder than it can carry, or drops a figure without weighting.</li>'
'<li style="margin:2px 0"><strong>1</strong>: it barely uses the sources, or uses only one.</li></ul></div>')

# coping-model before/after: a feel-guess rebuilt into a row-by-row prediction with the gap named after the
# reveal. Contains BOTH a literal BEFORE and AFTER (content_depth). No named person (stateless rule).
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> a guess with no reasons</span>'
    '<p style="margin:8px 0 0;font-size:15px">I think my synthesis is a 5 because it felt strong and I used all '
    'three sources.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">A number with no rubric reasons cannot be compared '
    'to the grader. "Felt strong" and "used the sources" are not the rows the grader scores.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> a prediction tied to the rows, then the gap</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">PREDICT + REASON</span> I predict Development 3 and Evidence 3, because I state one '
      'argument and weave three sources, but I do not weight them. '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">GAP</span> Re-scored carefully against the rubric, Evidence is a 2, not the 3 I first '
      'guessed; the gap is that two body points lean on one source beyond what it can carry.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">The prediction names rows and reasons, so when I '
    're-score against the rubric the gap is specific and fixable. Predict on the rows, then name the gap.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1103-0015", grade="9-10", lesson_type=8,
    unit="G11 U3 - Calibrate your own synthesis (predict, grader-reveal, name the gap)",
    title="Predict Your Own Score, Then Name the Gap",
    target=("Predict your own synthesis's rubric score row by row with reasons, submit it to the grader, then "
            "name the gap between your prediction and the real score. Written at the essay. Trait: self-"
            "assessment against Development (synthesis) and Evidence."),
    acc_tags=["ACC.W.PROD.3", "CCSS.W.11-12.5"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.02", "sot": "icm course-G11.md L15",
                "taught_stimulus": "ACC-W1112-SYNTH-LESSON-0001",
                "transfer_stimulus": "ACC-W910-SYNTH-SET-0002",
                "playbook": "_phase2/playbook_T5_CHECK.md",
                "one_idea": "You can predict your own synthesis score before the grader, if you predict on the rows with reasons.",
                "one_reminder": "Calibration check: a number for each row? a reason from the writing? the gap named on every off row?",
                "template": ("v3.1 spine; SYNTHESIS-TIER binds full sources; K2 own-work calibration is "
                             "stateless-safe (fresh writing routed to grader, no stored prior state); "
                             "lesson_type=8 because the calibration operates on a full synthesis essay "
                             "(T5 caps at paragraph). UNTIMED (no Timeback timer)."),
                "version_note": ("V3.1 rebuild of L15. FIXED the two prose-wall teach cards (now ONE_IDEA "
                                 "callout + real <ul>/<ol> lists, format_fidelity) and removed the leaked "
                                 "internal label ('a Grade-C design bet we label as a bet') from the "
                                 "discrimination, moving the options to explicit choices=[]. Deterministic "
                                 "frq_prompt/setapart/checklist bodies; coping-model before/after kept; the "
                                 "calibration check folded in at first use as an <ol> REMEMBER box. Preserved "
                                 "id, type 8, mnemonic_status=proposal, kc=C.11.02, unit, bound stimuli "
                                 "(water taught -> AI-workforce transfer), and the essay ceiling."),
                "council": ("T8/WEAVE G11 own-work calibration (K2, map role = check): predict-own-score -> "
                            "grader-reveal -> name-gap on a synthesis essay. self_score calibration enforced by "
                            "judge-then-reveal gate. predict-on-rows-vs-guess discrimination. unit=essay. "
                            "Stateless-safe."),
                "review_provenance": "built to the L01/L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["predict-own-rubric-score", "name-the-gap-to-grader"],
    slots=[
        # ===== TEACH: the one idea + the two terms (as a list), then the routine (as an ordered list) =====
        Slot("TEACH", "teach_card", "The one idea: predict on the rows, not on a feeling",
             body=(ONE_IDEA +
                   "You have written synthesis essays. Now you learn to score your own before anyone else does. "
                   "Two words to pin down first:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>A synthesis</strong> is a piece of writing that combines "
                   "several sources into one argument, so it is scored on two rows: Development (does it weave "
                   "ONE argument from the set?) and Evidence (does it use and weight the sources well?).</li>"
                   "<li style=\"margin:4px 0\"><strong>Calibration</strong> means predicting your score on those "
                   "rubric rows with reasons, not a gut number, then comparing to the grader and naming the "
                   "gap.</li></ul>"
                   "The weak move is guessing a number from feel. Predicting on the rows is what turns a grade "
                   "into information you can act on.")),
        Slot("TEACH", "teach_card", "The routine: predict with reasons, submit, name the gap",
             body=("Run this routine on your own writing, in order:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>PREDICT</strong>: give a number for each rubric row and "
                   "write the reason ('Evidence 3 because I weave three sources but do not weight them').</li>"
                   "<li style=\"margin:4px 0\"><strong>SUBMIT</strong>: send the synthesis to the grader.</li>"
                   "<li style=\"margin:4px 0\"><strong>READ THE REVEAL</strong>: look at the grader's real row "
                   "scores.</li>"
                   "<li style=\"margin:4px 0\"><strong>NAME THE GAP</strong>: for every row where your number "
                   "differed, say what you missed ('I counted weaving as enough; the grader wanted the sources "
                   "weighted').</li></ol>"
                   "You cannot predict on a row you cannot see, so here are the two rows and what each score from "
                   "1 to 4 means. Predict against these descriptors, not a feeling:" + RUBRIC +
                   "Committing to a row-by-row prediction before the reveal is what surfaces the blind spot; a "
                   "bare number hides it.")),
        Slot("TEACH", "stimulus_display", "Read the source set: competing water uses (3 sources)",
             ref="ACC-W1112-SYNTH-LESSON-0001", bank="water_competing_uses",
             body=("Read this three-source set on whether a drying country should protect the water that cools "
                   "its power plants or the water that grows its crops. You will write a synthesis on it, then "
                   "predict your own score before the grader returns one. Read for the argument the set builds "
                   "and how each source helps. The texts stay on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + the calibration check, then the items =====
        Slot("MODEL", "annotated_before_after", "Watch a feel-guess become a row-by-row prediction",
             bank="water_competing_uses",
             body=("Here is a feel-guess rebuilt into a prediction tied to the rows, with the gap named after a "
                   "careful re-score against the rubric. Read the BEFORE, then the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE guesses from feel. The AFTER predicts on the rows with reasons, then names the "
                   "gap. Predicting on the rows is the move." + REMEMBER +
                   "When you predict your own, run this check before you trust the number.")),
        Slot("MODEL", "discrimination", "Which self-prediction can be compared to the grader?",
             ref="", labeled_grade_c=True, bank="water_competing_uses",
             body=("You have watched a feel-guess become a row prediction. Now spot the target: which "
                   "self-prediction is TIED TO THE ROWS, and which is a GUESS the grader cannot check? "
                   "(A) I predict a 5 overall because the piece felt strong when I read it back and I managed to bring in all three of the sources somewhere in it.  "
                   "(B) I predict Development 3 because I weave one argument from the set, and Evidence 2 because I lean on one source harder than it can carry.  "
                   "(C) I predict a high score because I spent a long time on this piece and worked much harder on it than I did on the last one I wrote.  "
                   "(D) I predict Development 4 because I wrote about all three water topics, and Evidence 4 because I mentioned every source somewhere in the essay. "
                   "Correct: B. Only B names each row, a number, and the reason from what the writing does, so "
                   "the gap to the grader is specific. A gives a feeling, C gives effort, and D names the rows "
                   "but reasons from coverage the rows do not score."),
             choices=[
                 {"id": "A", "text": "I predict a 5 overall because the piece felt strong when I read it back and I managed to bring in all three of the sources somewhere in it.",
                  "correct": False,
                  "why": "A feel-number tied to nothing the grader scores. 'Felt strong' and 'used the sources' are not the Development or Evidence rows, so the gap cannot be measured."},
                 {"id": "B", "text": "I predict Development 3 because I weave one argument from the set, and Evidence 2 because I lean on one source harder than it can carry.",
                  "correct": True,
                  "why": "Correct. Each row gets a number and a reason drawn from what the writing does, so the gap to the grader is specific and fixable."},
                 {"id": "C", "text": "I predict a high score because I spent a long time on this piece and worked much harder on it than I did on the last one I wrote.",
                  "correct": False,
                  "why": "Effort and time are not rubric rows. A prediction built on hard work still hides the blind spot, because the grader scores the writing, not the hours."},
                 {"id": "D", "text": "I predict Development 4 because I wrote about all three water topics, and Evidence 4 because I mentioned every source somewhere in the essay.",
                  "correct": False,
                  "why": "It names the rows and numbers, which looks right, but the reasons come from coverage, not the rubric. Development 4 wants ONE woven argument, not three topics touched; Evidence 4 wants sources weighted by what they carry, not just mentioned. Covering and mentioning are the wrong descriptors, so the gap stays hidden."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this self-prediction most need?",
             bank="water_competing_uses",
             body=("Diagnose before the reveal. A student wrote about their own synthesis: 'I think I did well "
                   "because I really cared about this topic.' Which single move would most improve the prediction? "
                   "(A) predict a number for each rubric row, Development and Evidence, and give the reason from what the writing does  "
                   "(B) predict one higher overall number instead, on the grounds that caring this much about a topic should lift the score  "
                   "(C) count how many hours the writing took and describe how much effort went into finishing the whole piece on time  "
                   "(D) skip predicting for now and simply wait for the grader to hand back the real score before thinking about it at all"),
             feedback=("Correct: A. Caring about a topic is a feeling, a higher overall number (B) is still a "
                       "guess, and hours of effort (C) are not rows the grader scores. Skipping the prediction "
                       "(D) throws away the calibration. Only A ties a number to each row with a reason, so the "
                       "gap to the grader becomes specific and fixable.")),

        # ===== SUPPORTED: self-score a sample (predict THEN reveal), then write + predict your own =====
        Slot("SUPPORTED", "self_score", "Score a sample synthesis, then see the real score",
             ref="", bank="water_competing_uses",
             body=("Predict, then reveal. Sample synthesis: 'Source 1 is about water use, Source 2 is about "
                   "power plants, Source 3 is about farms. So we should save water.' On the Development row "
                   "(1 to 4: does it weave ONE argument?), predict a score, then check the reveal."),
             choices=[
                 {"id": "d2", "text": "Development 2, it names the sources but does not weave one argument",
                  "correct": True,
                  "why": "Correct. It walks through the sources one at a time and ends on a vague 'save water,' so it never weaves ONE argument. That is a Development 2, and the Evidence row is also a 2, since it drops a figure without weighting energy against farming."},
                 {"id": "d4", "text": "Development 4, it uses all the sources so the argument is fully woven",
                  "correct": False,
                  "why": "Look again. Naming the sources is not the same as weaving them. This piece surveys Source 1, 2, and 3 in turn and never builds ONE argument across them, so it scores Development 2, not 4."},
             ]),
        Slot("SUPPORTED", "production_frq", "Write your synthesis, then predict its score",
             ref="", bank="water_competing_uses", rubric_ref="rc.4trait", scored=True, unit="essay",
             body=frq_prompt(
                 intro="Write a synthesis on the water set, then predict its score before the grader does.",
                 setapart_block=setapart("Predict on the rows like this:",
                                         "Development __ because __; Evidence __ because __."),
                 closer="Write a synthesis that weaves ONE argument from the water sources and weights each "
                        "source by what it can carry. Then, in one line, predict your own score on each row with "
                        "a reason, using the rubric descriptors you were shown. That written prediction is what "
                        "you will compare against when you re-score your draft next.")),
        # ===== INDEPENDENT: predict + name the gap with no frame + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Calibrate on your own",
             ref="", bank="water_competing_uses", rubric_ref="rc.4trait", scored=True, unit="essay",
             body=frq_prompt(
                 intro="On your own now. No frame this time.",
                 closer="Write a fresh synthesis on the water set, predict your score on each row with a reason, "
                        "then re-score your finished draft carefully against the rubric descriptors and name the "
                        "gap on every row where your prediction differed. Before you submit, check: did I predict "
                        "on the ROWS with reasons, not a feel number, and can I name one specific gap? Predicting "
                        "your own score and naming the gap is what every calibrated writer does before a grader "
                        "ever sees the work, and you are ready to do it cold.")),

        # DIAGNOSIS = self-revision on the student's OWN just-written draft. A single labeled EXAMPLE shows what
        # naming a gap looks like (an example, NOT the student's essay); the student then names and fixes the gap
        # on THEIR OWN draft. Same taught source (load balance). Self-contained: the grader scores the diagnosis.
        Slot("MODEL", "diagnosis_frq", "Name the gap between your prediction and the grader",
             ref="", bank="water_competing_uses", scored=True,
             body=frq_prompt(
                 intro="Reread the essay you just wrote and re-score it carefully against the rubric descriptors, "
                       "then compare that honest score with the prediction you made.",
                 setapart_block=setapart("Here is what naming a gap looks like:",
                     "Evidence, off by two: I predicted a 4, but re-scoring against the rubric it is a 2, because "
                     "I leaned on one source harder than it could carry and never weighted the energy use against "
                     "the farming use. My blind spot was counting 'used the source' as 'weighted the source.' "
                     "Fix: weight each source by what it can carry."),
                 closer="Now do this on YOUR draft. For every row where your number was off, name the gap in one "
                        "line the same way, then make the fix. Finish by naming your single biggest gap.")),
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
