"""
lesson_g12_l15_voice_syntax.py  -  G12 KC D.12.01, ARCHETYPE T6: EDITING-IN-CONTEXT (SPOT, ceiling sentence).
V3.1 rebuild of the pre-v3.1 L15 to the v3.1 lesson build spec (icm/_config/v3_1-lesson-build-spec.md), which
cleared all 23 lesson_contract gates + the Fable-5 reviewer on G9 L01/L15 v3.1.

TEACHING POINT (KEEP): voice through syntactic choice. Revise a flat compound string by a deliberate syntactic
move (subordinate the minor idea, place the point at the emphatic end) so the sentence carries voice and
emphasis, instead of stringing equal clauses with "and." KC D.12.01. Editing-in-context, unit=sentence.
Bound stimuli unchanged: taught WORKFORCEINVEST (public_health) -> transfer WATERTRADEOFF (automation_policy).

V3.1 changes from the pre-v3.1 L15 (design pattern, not the teaching point):
  1. TEACH split into ONE idea in a teal callout + the flat/shaped contrast as a real LIST (was a ~130-word wall
     of prose that tripped format_fidelity). "syntax" and "voice" defined in plain words up front.
  2. MODEL rebuilt as a coping-model think-aloud (First try -> run the check -> catch the flat string -> Final),
     still with a literal BEFORE and AFTER; the reusable 3-question check tool folded in at point of first use.
  3. DISCRIMINATION uses explicit choices=[{id,text,correct,why}]; the "Grade-C design bet" jargon that leaked
     into the student prompt is gone (labeled_grade_c stays True in code only). Surface-token confound broken: a
     distractor ALSO opens with "Although," so the invariant is "subordinates the MINOR idea and ends on the
     point," not "contains although." Correct option is not the lone longest.
  4. PREDICT-THE-FIX reveal lives in feedback= (not in the option text).
  5. SUPPORTED + diagnosis bodies built with frq_prompt / setapart / checklist (no "Step 1/Step 2" prose -> kills
     the render double-numbering; no "Scored on ..." chrome).
  6. INDEPENDENT names the standard out loud (Yeager). TRANSFER stays a partitioned new topic (water trade-off).

id, lesson_type=6, kc=D.12.01, mnemonic_status="proposal", unit are the pre-v3.1 L15's values, unchanged; every
production_frq unit="sentence" (T6 ceiling). Own words, no fabricated figures, no em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">When a sentence just strings clauses together with '
'<strong>and</strong>, every idea carries equal weight and nothing stands out. A deliberate arrangement, '
'<strong>subordinating the smaller idea and ending on the point</strong>, is what gives a sentence emphasis and '
'voice.</div></div>')

# reusable job-aid, folded in at point of first use (the model/decompose card), not cold in step 1 (KH load).
REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit any sentence, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Are the ideas strung together with "and" at equal weight?</li>'
'<li style="margin:2px 0">Is the point you want remembered placed last, at the emphatic end?</li>'
'<li style="margin:2px 0">If not, subordinate a minor idea and move the point to the end.</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If every clause reads as equally important, the sentence is not shaped yet.</div></div>')

# coping-model think-aloud: a WRITTEN editing process (draft -> run the check -> catch the flat string -> revise),
# then the endpoints. Contains a literal BEFORE and AFTER (content_depth). No named near-peer (Timeback rule).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer reshaping one flat sentence, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Training helps the next generation, and it does not '
    'help the displaced worker, and a budget has to choose, and that is the hard part." Run the check: four '
    'clauses joined by "and" at equal weight, so nothing stands out. Shape it.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "Although training helps the next generation, it does '
    'not help the displaced worker, and a budget has to choose." Better, the minor idea is subordinated now. But '
    'the point I want remembered, the hard choice, is sitting in the middle. Move it to the end.</p>'
    '<p style="margin:0"><strong>Final:</strong> "Although training helps the next generation, it does nothing '
    'for the worker displaced today, and that is the choice a fixed budget cannot avoid." Now the point lands '
    'last, at the emphatic spot. Shaped.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "Training helps the next generation, and it does not help the '
    'displaced worker, and a budget has to choose, and that is the hard part." (flat string, nothing lands)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "Although training helps the next generation, it does nothing '
    'for the worker displaced today, and that is the choice a fixed budget cannot avoid." (minor idea '
    'subordinated, point placed last)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G12-D1201-0015", grade="9-10", lesson_type=6,
    unit="G12 U2 - Voice through syntactic choice (applied style pass)",
    title="Shape Voice With a Syntactic Choice",
    target=("Revise a flat compound string by a deliberate syntactic move (subordinate the minor idea, place the "
            "point at the emphatic end) so the sentence carries voice and emphasis, instead of stringing equal "
            "clauses with 'and.' Editing the given sentence in place. Written at the sentence. Trait: Language "
            "and voice."),
    acc_tags=["ACC.W.LANG.3", "CCSS.W.11-12.4", "CCSS.L.11-12.3"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "D.12.01", "sot": "icm course-G12.md L15",
                "taught_stimulus": "ACC-W910-ARG-LESSON-WORKFORCEINVEST",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-WATERTRADEOFF",
                "playbook": "_phase2/playbook_T6_SPOT.md",
                "template": "v3.1 lesson build spec; binds full argument source (sentence material); editing-in-context style pass.",
                "one_idea": "A flat 'and' string carries no emphasis; subordinate the minor idea and end on the point.",
                "one_reminder": "3-question check: equal 'and' clauses? point at an emphatic spot? if not, subordinate + move the point to the end.",
                "version_note": ("V3.1 rebuild of the pre-v3.1 L15 to the v3.1 build spec: TEACH split into a "
                                 "one-idea callout + a flat/shaped LIST (fixes the format_fidelity wall of text); "
                                 "MODEL rebuilt as a coping-model think-aloud with the 3-question check folded in "
                                 "at point of first use; discrimination moved to explicit choices with the "
                                 "'Grade-C design bet' jargon removed and the 'although' surface-token confound "
                                 "broken; SUPPORTED + diagnosis bodies use frq_prompt/setapart/checklist (kills "
                                 "the 'Step 1/2' render double-numbering and the 'Scored on' chrome); independent "
                                 "says the standard out loud (Yeager). Teaching point + bound stimuli unchanged."),
                "review_provenance": ("Rebuilt to icm/_config/v3_1-lesson-build-spec.md (the pattern that cleared "
                                      "all 23 lesson_contract gates + the Fable-5 reviewer on G9 L01/L15 v3.1)."),
                "council": ("T6/SPOT G12 style review: D.12.01 voice through syntactic choice (subordinate the "
                            "minor idea, emphatic end) vs flat compound string. shaped-vs-flat discrimination "
                            "labeled Grade-C in code (not in student text). SPOT=proposal; ceiling sentence.")},
    fade_ledger_moves=["voice-through-syntax", "subordinate-and-emphasize"],
    slots=[
        # ===== TEACH: ONE idea in a callout + the flat/shaped contrast as a real LIST (no wall of text) =====
        Slot("TEACH", "teach_card", "Syntax is a choice that carries voice",
             body=(ONE_IDEA +
                   "Syntax means the way you arrange the words and clauses in a sentence, and voice is when that "
                   "arrangement makes your point land instead of sitting flat. The weak default is the flat "
                   "compound string: clause and clause and clause, joined by 'and,' so every idea carries equal "
                   "weight and nothing stands out. A syntactic choice fixes that. Two versions to keep apart:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>FLAT STRING</strong>: equal clauses joined by 'and,' with "
                   "the point buried somewhere in the chain ('X, and Y, and Z, and that is hard').</li>"
                   "<li style=\"margin:4px 0\"><strong>SHAPED FOR EMPHASIS</strong>: the minor idea is "
                   "subordinated (put in an 'although' or 'because' clause) and the point is placed last, at the "
                   "emphatic spot ('Although X, Y, and that is the real choice').</li></ul>"
                   "This is an editing move on a sentence that already exists: you spot the flat structure and "
                   "reshape it, keeping the meaning. The trap is stringing clauses with 'and' and hoping emphasis "
                   "appears on its own. Goal today: revise a flat sentence with a syntactic choice that gives it "
                   "emphasis and voice.")),
        Slot("TEACH", "stimulus_display", "Read the source: prepare workers or protect them?",
             ref="ACC-W910-ARG-LESSON-WORKFORCEINVEST", bank="public_health",
             body=("Read this source on preparing more workers for growing fields or protecting the workers the "
                   "change leaves behind. The sentences you reshape state ideas from it, so you can change the "
                   "arrangement while keeping the meaning. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model think-aloud with the check tool folded in =====
        Slot("MODEL", "annotated_before_after", "Watch a flat string gain voice",
             bank="public_health",
             body=("Here is the skill in action. Follow the writer's editing below. " + COPING_HTML +
                   " Notice the two moves that turned the BEFORE into the AFTER: the writer subordinated the "
                   "minor idea in an 'although' clause and placed the point at the end. " + REMEMBER +
                   "When you fix your own sentence, do the same: find the flat 'and' string, subordinate a minor "
                   "idea, and move the point to the emphatic spot before you submit.")),
        Slot("MODEL", "discrimination", "Which sentence uses syntax for emphasis?",
             ref="", labeled_grade_c=True, bank="school_phone_policy",
             body=("You have watched one built. Now spot the target on a different idea. A school is weighing a "
                   "phone ban, and all three sentences state the same idea. Which one uses a SYNTACTIC choice for "
                   "emphasis, and which are FLAT or bury the point? "
                   "(A) A phone ban helps students focus, and it takes away the tool a student needs in an "
                   "emergency, and a school still has to set one rule, and that last part is the hard one.  "
                   "(B) Although a phone ban helps students focus, it strips away the tool a student needs in an "
                   "emergency, and that is the cost a single rule cannot escape.  "
                   "(C) Although a school must in the end set one rule, a phone ban helps students focus and "
                   "keeping phones helps students stay reachable.  "
                   "(D) A phone ban clearly and importantly helps students focus, and it obviously takes away the "
                   "tool a student needs in an emergency, and the school truly must set one rule.  "
                   "Correct: B uses syntax for emphasis. B subordinates the minor idea and ends on the point; "
                   "A strings equal clauses with 'and,' C subordinates the main decision so its point is "
                   "buried, and D just piles on emphasis words over a flat 'and' string."),
             choices=[
                 {"id": "A", "text": "A phone ban helps students focus, and it takes away the tool a student needs in an emergency, and a school still has to set one rule, and that last part is the hard one.",
                  "correct": False,
                  "why": "This is the flat compound string: four clauses joined by 'and' at equal weight, so the point never stands out, no matter how long the sentence runs."},
                 {"id": "B", "text": "Although a phone ban helps students focus, it strips away the tool a student needs in an emergency, and that is the cost a single rule cannot escape.",
                  "correct": True,
                  "why": "Correct. It subordinates the minor idea in an 'although' clause and ends on the point, so the cost lands. That arrangement is the voice move."},
                 {"id": "C", "text": "Although a school must in the end set one rule, a phone ban helps students focus and keeping phones helps students stay reachable.",
                  "correct": False,
                  "why": "It opens with 'although,' but it subordinates the main decision and ends on a flat list of both goods, so the point is buried. Subordinating the MINOR idea is what carries emphasis."},
                 {"id": "D", "text": "A phone ban clearly and importantly helps students focus, and it obviously takes away the tool a student needs in an emergency, and the school truly must set one rule.",
                  "correct": False,
                  "why": "Words like 'clearly' and 'obviously' cannot do the work of arrangement. This is still a flat 'and' string with emphasis words dropped in, so the point still sits at equal weight and never lands."},
             ]),
        Slot("MODEL", "discrimination", "Which sentence saves the last spot for the point?",
             ref="", labeled_grade_c=True, bank="public_health",
             body=("You spotted one already. Here is a second, on a different point in the same debate. All "
                   "three carry one idea: automation raises factory output but erases the entry-level jobs new "
                   "workers start in. Which one saves the last, emphatic spot for the point? "
                   "(A) Although automation raises the plant's output, it erases the entry-level jobs, and the "
                   "new machines now run quietly through every shift.  "
                   "(B) Although automation raises the plant's output, it erases the entry-level jobs where new "
                   "workers have to start.  "
                   "(C) Automation raises the plant's output, and it erases the entry-level jobs, and new "
                   "workers lose their first step, and that step matters.  "
                   "(D) It erases the entry-level jobs where new workers start, although automation does raise "
                   "the plant's output across every shift. "
                   "Correct: B saves the emphatic spot for the point. B subordinates the minor idea and ends on "
                   "the point; A subordinates the minor idea but trails off on a routine detail, so the point "
                   "sits buried; C strings equal clauses with 'and,' so nothing lands; and D leads with the point "
                   "and ends on the minor idea, so the last, emphatic spot is wasted."),
             choices=[
                 {"id": "A", "text": "Although automation raises the plant's output, it erases the entry-level jobs, and the new machines now run quietly through every shift.",
                  "correct": False,
                  "why": "The minor idea is subordinated correctly, but the sentence trails off on a routine detail, so the point about lost jobs no longer sits in the emphatic last spot."},
                 {"id": "B", "text": "Although automation raises the plant's output, it erases the entry-level jobs where new workers have to start.",
                  "correct": True,
                  "why": "Correct. It subordinates the minor idea and ends on the point about the jobs new workers depend on, so the point lands in the emphatic last spot."},
                 {"id": "C", "text": "Automation raises the plant's output, and it erases the entry-level jobs, and new workers lose their first step, and that step matters.",
                  "correct": False,
                  "why": "Every clause is joined by 'and' at equal weight, so even the last one carries no extra force and the point never stands out."},
                 {"id": "D", "text": "It erases the entry-level jobs where new workers start, although automation does raise the plant's output across every shift.",
                  "correct": False,
                  "why": "This subordinates the minor idea correctly, but it leads with the point and ends on the raised output, so the emphatic last spot goes to the minor idea and the point about lost jobs does not land."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this sentence's syntax most need?",
             bank="public_health",
             body=("Diagnose this draft before the reveal. A writer wrote: 'The pipeline matters, and older "
                   "workers need help, and a budget is limited, and it is a problem.' Which single move would "
                   "most improve it? "
                   "(A) subordinate the minor ideas and end on the point, instead of stringing equal clauses with 'and'  "
                   "(B) add one more 'and' clause so every separate idea still keeps its own equal place in the long string  "
                   "(C) make every clause the exact same length so the whole sentence reads with a steady, even rhythm  "
                   "(D) swap the plain everyday words for longer, more formal synonyms so the sentence sounds more advanced"),
             feedback=("Correct: A. Four equal 'and' clauses flatten the emphasis; the fix subordinates the minor "
                       "ideas and ends on the point (for example, 'Because a limited budget cannot fund "
                       "everything, the real problem is deciding whom to help first'). Another 'and' clause (B), "
                       "equal lengths (C), or fancier synonyms (D) add words but not emphasis.")),

        # ===== SUPPORTED: framed edit (fill-in frame) on the taught topic (source read at TEACH step 2) =====
        Slot("SUPPORTED", "production_frq", "Reshape this sentence for emphasis",
             ref="", bank="public_health", rubric_ref="rc.ap", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Reshape this flat string with a syntactic choice. Flat sentence to fix: 'Training helps "
                       "the young, and it does not help older workers, and a budget must choose, and that is "
                       "hard.'",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "Although training helps the young, it ______ , and that is ______ ."),
                 closer="Put the minor idea in the 'although' clause, then end on the point you want the reader to "
                        "remember. Write one sentence, keeping the meaning. Then run the 3-question check before "
                        "you submit.")),
        # DIAGNOSIS = run the check on a PROVIDED weak draft, then rewrite it (not a fresh production, so it does
        # not repeat the Independent write). Stays on the taught topic = no new source to read (load balance).
        Slot("MODEL", "diagnosis_frq", "Check and fix a weak draft with the 3 questions",
             ref="", bank="public_health", scored=True,
             body=frq_prompt(
                 intro="Run the 3-question check on this weak draft, then rewrite it so the point lands.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "Workers matter, and jobs matter, and change is hard, and we must decide.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Are the ideas strung together with 'and' at equal weight?", "Yes. Four clauses joined by 'and,' so nothing stands out."),
                     ("Is the point placed last, at the emphatic end?", "No. The equal 'and' chain flattens even the last clause."),
                     ("What is the fix?", "Subordinate the minor ideas and end on the point, for example 'Because workers and jobs are both at stake, the hard part is deciding.'"),
                 ]),
                 closer="Now rewrite the weak draft into one sentence whose point lands at the end. Then name the "
                        "syntactic move you used.")),

        # ===== INDEPENDENT: cold edit on the taught topic + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Shape voice with syntax on your own",
             ref="", bank="public_health", rubric_ref="rc.ap", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="On your own now, no frame. Take one idea from the workforce source, write it as a flat "
                       "compound string, then reshape it with a syntactic choice: subordinate the minor idea and "
                       "place the point at the emphatic end.",
                 closer="Shaping a sentence so the point lands is what every strong piece of writing is built on, "
                        "and you are ready to do it cold. Run the 3-question check before you submit.")),

        # ===== TRANSFER: same move, a NEW topic (water trade-off), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "A NEW source: water for food or power?",
             ref="ACC-W910-ARG-LESSON-WATERTRADEOFF", bank="automation_policy",
             body=("Read this new source on protecting scarce water for growing food or for generating power. You "
                   "will state an idea from it and reshape the sentence for emphasis. The text stays on screen "
                   "while you work.")),
        Slot("TRANSFER", "production_frq", "Shape voice with syntax on a NEW source",
             ref="", bank="automation_policy", rubric_ref="rc.ap", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="New source. Take one idea from the water source, write it as a flat 'and' string, then "
                       "reshape it with a syntactic choice for emphasis.",
                 closer="Same subordinate-and-emphasize move as the workforce sentence, new source: subordinate "
                        "the minor idea and end on the point. Run the 3-question check before you submit.")),
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
