"""
lesson_g10_l13_error_autopsy.py  -  G10 KC C.10.05, ARCHETYPE T5: RUBRIC-REVISION (CHECK, paragraph). V3.1.

G10 course L13 (Unit 3, guided). Rebuilt to the v3.1 build spec (icm/_config/v3_1-lesson-build-spec.md) from
the prior prose-wall version. Teaching point (KEPT): diagnose a PROVIDED draft by naming the TYPE of error (too
general, off-purpose, circular reason, out of order) and the fix that type calls for, instead of a vague "it is
weak." STATELESS-LEGAL: work on PROVIDED drafts + one self-check on a fresh draft the student writes here, never
a prior-draft look-back. KC C.10.05, lesson_type=5, mnemonic_status=proposal (all KEPT). Bound stimuli KEPT:
ACC-W910-INFO-LESSON-WEATHER (taught) -> ACC-W910-INFO-LESSON-WETLANDS (transfer, bank-partitioned). rc.staar,
unit="paragraph" (T5 ceiling). CHECK=proposal.

V3.1 changes over the prior L13 (all prior gate/format failures fixed):
  1. TEACH is now ONE idea, hammered: a teal ONE_IDEA callout + the four error types as a real <ul> list (was a
     >45-word prose wall). The name-the-type-then-fix routine moved to the REMEMBER check tool at the model card
     (point of first use), not a cold prose block up front.
  2. NO leaked internal labels: the old discrimination prose said "a Grade-C design bet we label as a bet"
     (leaked_internal_label). Removed; the discrimination now uses explicit choices=[{id,text,correct,why}] with
     the correct option NOT the lone-longest, and every option names a TYPE + a FIX so the invariant is the match
     to the draft, not a surface token (DI faultless communication). labeled_grade_c stays True in code only.
  3. The prior predict_the_fix option C had a garbled duplicated clause; rewritten clean, reveal moved to
     feedback= (leaked_answer_cue). FRQ + diagnosis bodies built with frq_prompt / setapart / checklist (no
     "Step 1/Step 2" prose, no "Scored on" chrome); the provided draft sits in a setapart(...) block each time.
  4. self_score is a clean predict-the-TYPE MCQ (short prompt + choices carrying the reveal), not a prose wall.
     Coping before/after kept (literal BEFORE + AFTER inline). Facts faithful to the bound federal sources; own
     words, no fabricated figures, no em dashes, no named HTML entities.
Passes all 23 lesson_contract gates + gated_reading render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A vague verdict like "this is weak" cannot guide a '
'revision. Naming the <strong>error TYPE</strong> points straight at the <strong>fix</strong> that type calls '
'for.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: name the type before you fix</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Run these three questions on any draft. The first No tells you the type, and the type tells you the fix:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0"><strong>Any specifics?</strong> Does the draft name a real detail, or only general '
'words like "science" or "helpful"? Only general means the type is <strong>too general</strong>; the fix is to '
'add specifics.</li>'
'<li style="margin:2px 0"><strong>Does every sentence serve the point?</strong> A sentence that wanders is '
'<strong>off-purpose</strong> (fix: cut it); a reason that just restates the claim is <strong>circular</strong> '
'(fix: give a real reason).</li>'
'<li style="margin:2px 0"><strong>Are the steps in order?</strong> Scrambled steps are <strong>out of '
'order</strong>; the fix is to reorder them into a logical sequence.</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">Name the type first. "Weak" names nothing, so it '
'guides no repair.</div></div>')

# coping-model before/after panel: a vague verdict replaced by a named error type plus its fix.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> a vague verdict that names no type</span>'
    '<p style="margin:8px 0 0;font-size:15px">Draft: "Forecasts are made with science and they help people." '
    'Verdict: this paragraph is weak and needs work.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">"Weak and needs work" names no error type, so the '
    'writer does not know what to change. A vague verdict cannot guide a revision.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> name the error TYPE, then the fix</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">ERROR TYPE</span> Too general: it names no specific tool or use (which science? helps '
      'how?). '
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">FIX</span> Add specifics: "Forecasters use satellite and radar data, which lets people '
      'prepare for storms before they arrive."</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Naming the type (too general) points straight at '
    'the fix (add specifics). A named type is a diagnosis; "weak" is not.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1005-0013", grade="9-10", lesson_type=5,
    unit="G10 U3 - Rhetorical revision (name the error type)",
    title="Name the Error Type, Not Just That It Is Wrong",
    target=("Diagnose a provided draft by naming the TYPE of error (too general, off-purpose, circular reason, "
            "out of order) and the fix that type calls for, rather than a vague 'it is weak.' Written at the "
            "paragraph. Trait: Organization/Development."),
    acc_tags=["ACC.W.PROC.2", "CCSS.W.9-10.5"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.05", "sot": "icm course-G10.md L13",
                "taught_stimulus": "ACC-W910-INFO-LESSON-WEATHER",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-WETLANDS",
                "one_idea": "A vague verdict cannot guide a revision; naming the error TYPE points at the fix.",
                "one_reminder": "Any specifics? Does every sentence serve the point? Are the steps in order?",
                "playbook": "_phase2/playbook_T5_CHECK.md",
                "template": "locked L01 template; REVISION-TIER, provided drafts; source bound for context.",
                "version_note": ("V3.1 rebuild to the v3.1 build spec. Fixed the prior failures: (a) TEACH is now "
                                 "one hammered idea (ONE_IDEA callout + the four error types as a <ul>), the "
                                 "name-the-type-then-fix routine moved to the REMEMBER check tool at point of "
                                 "first use (was a prose wall); (b) the discrimination dropped the leaked "
                                 "'Grade-C design bet' prose and now uses explicit choices with the correct "
                                 "option NOT the lone-longest and every option naming a TYPE+FIX to break the "
                                 "token confound; (c) predict_the_fix rewritten clean (the prior option C had a "
                                 "garbled duplicated clause), reveal in feedback; (d) FRQ + diagnosis built with "
                                 "frq_prompt/setapart/checklist, provided draft in a setapart block; (e) "
                                 "self_score is a clean predict-the-TYPE MCQ. Kept id, lesson_type, KC, unit, "
                                 "bound stimuli + every production unit='paragraph' (T5 ceiling)."),
                "council": ("T5/CHECK error-autopsy: names the error TYPE (too general, off-purpose, circular, "
                            "out of order) + its fix, not just 'it is wrong.' named-type-vs-vague-verdict "
                            "discrimination labeled Grade-C in code. self_score calibration. CHECK=proposal; "
                            "T5 ceiling paragraph, so revision targets are paragraph-level."),
                "review_provenance": "built to the G9 L25 v3.1 pattern (icm/_config/v3_1-lesson-build-spec.md)."},
    fade_ledger_moves=["erroneous-model-autopsy", "name-error-type-and-fix"],
    slots=[
        # ===== TEACH: ONE idea, hammered (callout + the four error types as a list) =====
        Slot("TEACH", "teach_card", "The one idea: name the type, then the fix",
             body=(ONE_IDEA +
                   "Revising well starts with naming the TYPE of problem, because each type has its own fix. "
                   "There are four error types you will diagnose today, and each points at a different repair:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Too general</strong>: the draft names no specific detail. "
                   "The fix is to add specifics (which tool, helps how).</li>"
                   "<li style=\"margin:4px 0\"><strong>Off-purpose</strong>: a sentence wanders away from the "
                   "point. The fix is to cut or replace the wandering part.</li>"
                   "<li style=\"margin:4px 0\"><strong>Circular reason</strong>: the reason just restates the "
                   "claim (\"useful because it is helpful\"). The fix is to give a real, specific reason.</li>"
                   "<li style=\"margin:4px 0\"><strong>Out of order</strong>: the steps run in the wrong "
                   "sequence. The fix is to reorder them into a logical order.</li></ul>"
                   "So an error autopsy has two parts: name the error TYPE, then give the fix that type calls "
                   "for. The trap is a vague verdict (\"it is weak\") that names no type and guides no repair.")),
        Slot("TEACH", "stimulus_display", "The topic: how weather forecasts work",
             ref="ACC-W910-INFO-LESSON-WEATHER", bank="weather", tag="buy_in",
             body=("The drafts you diagnose are about weather forecasting. Read this short source so the topic "
                   "is familiar. You are not writing a forecasting essay from scratch here; you are naming the "
                   "error type in drafts that are given to you, then giving each one its fix.")),

        # ===== MODEL (before the quiz): before/after worked example + the check tool at point of first use =====
        Slot("MODEL", "annotated_before_after", "Watch a vague verdict become a named diagnosis",
             bank="weather",
             body=("Here is the skill in action. Read the BEFORE, then the AFTER, and notice a vague verdict "
                   "being replaced by a named error type plus its fix." + BEFORE_AFTER_HTML +
                   " The BEFORE says only 'weak and needs work.' The AFTER names the type (too general) and the "
                   "fix (add specifics). Naming the type is the diagnosis. " + REMEMBER +
                   "When you diagnose a draft, run this three-question check, then name the type and its fix.")),
        Slot("MODEL", "discrimination", "Which diagnosis names the error type?",
             ref="", labeled_grade_c=True, bank="weather",
             body=("Sort these before you diagnose. A draft reads: 'Forecasts are made with science and they "
                   "help people.' Which diagnosis names the error TYPE and points at a fix? "
                   "(A) The draft is out of order: its sentences are scrambled out of their proper sequence, so "
                   "the fix is to reorder them into a clear, logical order.  "
                   "(B) The draft is too general: it names no specific tool or use, so the fix is to add "
                   "concrete, specific details.  "
                   "(C) The draft is off-purpose: one sentence wanders away from the main topic, so the fix is "
                   "to cut the straying part.  "
                   "(D) The draft has a circular reason: 'made with science' and 'help people' just restate each "
                   "other, so the fix is to give a real, specific reason.  "
                   "Correct: B. (A), (C), and (D) name real error types, but none fits this draft: nothing is "
                   "scrambled, nothing wanders, and no reason is even given. (B) names the type that fits (too "
                   "general) and the fix it calls for (add specifics). A named type points straight at the repair."),
             choices=[
                 {"id": "A",
                  "text": "The draft is out of order: its sentences are scrambled out of their proper sequence, so the fix is to reorder them into a clear, logical order.",
                  "correct": False,
                  "why": "Out of order is a real type, but it does not fit this draft: there is no scrambled sequence to reorder. The real problem is that the draft names no specifics."},
                 {"id": "B",
                  "text": "The draft is too general: it names no specific tool or use, so the fix is to add concrete, specific details.",
                  "correct": True,
                  "why": "Correct. The draft names no specific tool or use (which science? helps how?), so the type is too general and the fix is to add specifics."},
                 {"id": "C",
                  "text": "The draft is off-purpose: one sentence wanders away from the main topic, so the fix is to cut the straying part.",
                  "correct": False,
                  "why": "Off-purpose is a real type, but nothing here wanders off the topic. Both sentences stay on forecasting; they are simply too general."},
                 {"id": "D",
                  "text": "The draft has a circular reason: 'made with science' and 'help people' just restate each other, so the fix is to give a real, specific reason.",
                  "correct": False,
                  "why": "Circular reason is a real type, but it does not fit here: the draft never even gives a reason, circular or not. It just states two general facts, so the type is too general, not circular."},
             ]),
        Slot("MODEL", "predict_the_fix", "What error type is this, and what fixes it?",
             bank="weather",
             body=("Diagnose before the reveal. Draft: 'Radar forecasting is useful because forecasts made with "
                   "radar are helpful.' Which diagnosis correctly names the type and its fix? "
                   "(A) Circular reason: 'useful because ... helpful' just restates the claim, so the fix is "
                   "a specific reason.  "
                   "(B) Off-purpose: a sentence wanders onto an unrelated topic, so the fix is to cut the "
                   "straying part and refocus on the point.  "
                   "(C) Out of order: the sentences run out of their proper sequence, so the fix is to reorder "
                   "them into a logical order.  "
                   "(D) Too general: the draft names no specific tool or use, so the fix is to add specifics."),
             feedback=("Correct: A. The reason is circular: 'useful because forecasts made with radar are "
                       "helpful' just restates that forecasting is useful, so the fix is a specific reason (for "
                       "example, radar shows storms early enough for people to prepare). It is not off-purpose "
                       "(B, nothing wanders) or out of order (C, one sentence). (D) does not fit: the draft "
                       "names a specific tool (radar), so it is not too general; the flaw is a reason that "
                       "circles back on the claim. Naming the type points at the fix.")),

        # ===== SUPPORTED: predict the TYPE (calibration MCQ) -> then name-and-fix a draft (frame + checklist) =====
        Slot("SUPPORTED", "self_score", "Predict the error type, then see the answer",
             ref="", bank="weather",
             body=("Predict, then reveal. Draft: 'Forecasters launch weather balloons to measure the upper air. "
                   "Forecasting has existed for a long time. Then computers run those readings through models to "
                   "produce the forecast.' Which error type does this draft show?"),
             choices=[
                 {"id": "off", "text": "Off-purpose", "correct": True,
                  "why": "Correct. Run the check: the specifics are there (weather balloons, computers, models), "
                         "so the first No is not at 'Any specifics?' It is at 'Does every sentence serve the "
                         "point?' The middle sentence, about forecasting's history, wanders off a draft "
                         "explaining how a forecast is made. The type is off-purpose and the fix is to cut it "
                         "(keeping launch-then-model in order)."},
                 {"id": "gen", "text": "Too general", "correct": False,
                  "why": "Not this one. The on-point sentences name specific tools and steps (weather balloons, "
                         "computers, models), so 'Any specifics?' gets a Yes. The real problem is the wandering "
                         "history sentence, which is off-purpose, a different type with a different fix (cut the "
                         "straying sentence, not add specifics)."},
             ]),
        Slot("SUPPORTED", "production_frq", "Name the type and fix the draft",
             ref="", bank="weather", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="Diagnose the draft below, then fix it. Run the check to find the error type yourself, "
                       "then rewrite the draft so the fix matches that type.",
                 setapart_block=setapart("Draft to diagnose:",
                                         "Forecasts are made with science and they help people."),
                 checklist_block=checklist(title="Run the check to find the type:", rows=[
                     "Any specifics? Does the draft name a real tool or step, or only general words?",
                     "Does every sentence serve the point?",
                     "Are the steps in order?",
                 ]),
                 closer="The first No names the type. Start your answer by naming that type, then rewrite the "
                        "draft as a short paragraph so the fix matches it.")),
        # DIAGNOSIS: watch the check run on a provided draft, then run it on a fresh draft written in this box
        # (stateless-safe; the material is provided, and the self-check is on the same item, not a prior submission).
        Slot("MODEL", "diagnosis_frq", "Diagnose a fresh draft by naming its type",
             ref="", bank="weather", scored=True,
             body=frq_prompt(
                 intro="First watch the check run on a provided draft, then run it on a fresh draft you write "
                       "here.",
                 setapart_block=setapart("Provided draft to check:",
                                         "Weather matters because it is important, and forecasts are made carefully.", "red"),
                 checklist_block=checklist(title="Run the type check:", rows=[
                     ("Any specifics?", "Barely. 'Made carefully' names no tool or step. Leans too general."),
                     ("Does every part serve the point?", "The first clause is circular: 'matters because it is important' restates the claim."),
                     ("Name the type and fix.", "Circular reason. Fix: replace it with a specific reason, such as a forecast lets people prepare for storms."),
                 ]),
                 closer="Now write one short draft about forecasting that contains a deliberate error, then run "
                        "the same three questions on it. Finish by naming the error type you built in and the "
                        "fix that type calls for.")),

        # ===== INDEPENDENT: name-and-fix a PROVIDED draft with no checklist scaffold + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Name the type and fix a draft on your own",
             ref="", bank="weather", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="On your own now, no checklist. Diagnose the draft below, then fix it.",
                 setapart_block=setapart("Draft to diagnose:",
                                         "Forecasting is a good thing. Radar has been used for decades. It helps people know what to expect."),
                 closer="Run the three questions in your head to find the error type yourself, name it, then "
                        "rewrite the draft so the fix matches that type. Before you submit, check: did I name "
                        "the type, and does my fix match it? This name-the-type-then-fix move is what every real "
                        "revision is built on, and you are ready to do it cold.")),

        # ===== TRANSFER: same name-the-type-then-fix move, a NEW topic (wetlands), bank-partitioned =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: what wetlands do",
             ref="ACC-W910-INFO-LESSON-WETLANDS", bank="wetlands",
             body=("The next draft to diagnose is about wetlands. Read this new source so the topic is familiar. "
                   "Again, you are naming the error type in a draft that is given to you, then giving it the fix "
                   "that type calls for.")),
        Slot("TRANSFER", "production_frq", "Name the type and fix a draft on a NEW topic",
             ref="", bank="wetlands", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="New topic, same move. Diagnose the draft below, then fix it.",
                 setapart_block=setapart("Draft to diagnose:",
                                         "Wetlands are important because they matter. They also cover part of the country."),
                 closer="Run the three questions to find the error type yourself, name it, then rewrite the draft "
                        "so the fix matches that type (for example, a real reason such as that wetlands store "
                        "floodwater and filter the water that moves through them). Same name-the-type-then-fix "
                        "move as the weather drafts, on a new topic.")),
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
