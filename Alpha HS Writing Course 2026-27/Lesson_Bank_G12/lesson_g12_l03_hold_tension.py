"""
lesson_g12_l03_hold_tension.py  -  G12 KC C.12.01, lesson_type 3 (PROVE, ceiling paragraph). AP sophistication.

G12 course L03 (Unit 1, intro), rebuilt to the v3.1 build spec. Teaching point (kept): in a body paragraph,
HOLD the tension (keep both true things in view and reason from their conflict) rather than flattening it into
one tidy side by calling the other side weak. KC C.12.01. Binds the G12 argument LESSON source. Taught:
automation_policy (WATERTRADEOFF, full) -> transfer: public_health (WORKFORCEINVEST, full). rubric rc.ap,
unit climbs sentence->paragraph. PROVE=established-caveat. v3.1 spine: ONE_IDEA teal callout + REMEMBER dashed
check tool + coping-model think-aloud (BEFORE/AFTER) + explicit-choice discrimination + deterministic FRQ
prompts. No named persona (stateless). No source markup. No prior-work reference. No em dashes. 23 gates.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Hold the tension. Holding the tension '
'<strong>means</strong> keeping both true things in view and reasoning from the conflict between them, '
'instead of flattening the problem by calling one side weak.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, run your paragraph past all three:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0"><strong>Both truths live?</strong> Are both true things still in view, with neither one dismissed as weak?</li>'
'<li style="margin:2px 0"><strong>Reason from the conflict?</strong> Does the claim argue FROM the clash between them, not around it?</li>'
'<li style="margin:2px 0"><strong>Land on a position?</strong> Does it reach a rule or a priority that answers the difficulty, not just a tidy winner?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">A No on any one means you flattened the tension somewhere. Rebuild that part.</div></div>')

COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer working through the water trade-off, drafting then checking:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Water should go to food, because eating is the most '
    'basic need. The power argument is weak and does not really matter when people are hungry." That reads tidy. '
    'Let me run the check on it.</p>'
    '<p style="margin:0 0 8px"><strong>Check:</strong> Are both truths still live? No. I called the power side '
    '"weak" and dropped it, so only one truth is left standing. I flattened the tension instead of holding it.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "Food is the more basic need, and yet the pumps that '
    'irrigate the crops run on the grid." Better, both truths are back, but I have not reasoned from the clash yet.</p>'
    '<p style="margin:0"><strong>Final:</strong> "Food is the more basic need, and yet the pumps that irrigate '
    'the crops run on the grid, so protecting food already requires protecting some power; the two are not rivals '
    'to rank but one system to keep standing, which is why a shared rationing rule beats naming a winner." Now '
    'both truths stay live and the claim reasons straight from their conflict to a rule.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> the first try dismisses one side as weak, so the paragraph '
    'reads tidy but shallow.</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> the final keeps both truths live and reasons from the conflict '
    'to a rationing rule, which is the harder and stronger move.</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G12-C1201-0003", grade="9-10", lesson_type=3,
    unit="G12 U1 - Sophistication (hold the tension, do not flatten)",
    title="Hold the Tension Instead of Flattening It",
    target=("In a body paragraph, hold a real tension (keep both true things in view and reason from their "
            "conflict) rather than flattening it by dismissing one side as weak. The complexity move (nuance). "
            "Sentence then paragraph. Trait: Depth and Significance."),
    acc_tags=["ACC.W.ARG.2", "ACC.W.ARG.4", "CCSS.W.11-12.1"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "established-caveat", "kc": "C.12.01", "sot": "icm course-G12.md L03",
                "taught_stimulus": "ACC-W910-ARG-LESSON-WATERTRADEOFF",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-WORKFORCEINVEST",
                "playbook": "_phase2/playbook_T3_PROVE.md",
                "one_idea": "Hold the tension: keep both truths in view and reason from their conflict, do not flatten.",
                "one_reminder": "Check 3: both truths live? reason from the conflict? land on a rule/priority?",
                "template": "locked L01 template; binds G12 argument LESSON source; sophistication (nuance).",
                "version_note": ("V3.1 rebuild: replaced the prose-wall body + leaked Grade-C labels with the v3.1 "
                                 "spine (ONE_IDEA teal callout, minimum-teach list, coping-model think-aloud with "
                                 "literal BEFORE/AFTER, named moves + REMEMBER dashed 3-question check, "
                                 "explicit-choice discrimination with reveal in the tail, deterministic FRQ "
                                 "prompts). SUPPORTED = sentence warm-up, INDEPENDENT + TRANSFER = paragraph "
                                 "(unit ladder sentence->paragraph, type-3 ceiling paragraph). No persona."),
                "council": ("T3/PROVE G12 sophistication intro: hold-the-tension vs flatten-into-one-side. "
                            "hold-vs-flatten discrimination labeled Grade-C in code only. PROVE=established-caveat; "
                            "unit=paragraph.")},
    fade_ledger_moves=["hold-the-tension", "reason-from-the-conflict", "land-on-a-rule"],
    slots=[
        Slot("TEACH", "teach_card", "The one idea: hold the tension",
             body=(ONE_IDEA +
                   "Flattening is the easy move: dismiss the opposing point, and the essay reads tidy but shallow. "
                   "Holding the tension is harder and scores higher. It comes down to three moves:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Keep both truths live</strong>: state one true thing, then "
                   "grant the opposing true thing instead of calling it weak.</li>"
                   "<li style=\"margin:4px 0\"><strong>Reason from the conflict</strong>: argue from the clash "
                   "between the two truths, not around it.</li>"
                   "<li style=\"margin:4px 0\"><strong>Land on a position</strong>: reach a rule or a priority that "
                   "answers the difficulty, rather than just naming a winner.</li></ul>"
                   "The test: after your paragraph, does the reader still feel the difficulty, and see how your "
                   "claim addresses it? The trap is resolving the tension by pretending one side does not count.")),
        Slot("TEACH", "stimulus_display", "Read the source: water for food or power?",
             ref="ACC-W910-ARG-LESSON-WATERTRADEOFF", bank="automation_policy",
             body=("Read this source on protecting scarce water for growing food or for generating power. As you "
                   "read, find the tension the source itself points to: each side has to grant the other's central "
                   "fact. Note it, so your paragraph can hold that tension rather than flatten it. The text stays "
                   "on screen while you work.")),
        Slot("MODEL", "annotated_before_after", "Watch a writer catch a flattened point and hold it",
             bank="automation_policy",
             body=("Here is the move in action. Follow a writer draft a flattened paragraph, run the check, catch "
                   "the problem, and rebuild it to hold the tension. " + COPING_HTML +
                   "Name the moves you just saw: <strong>Move 1</strong>, grant the other truth ('and yet ...'); "
                   "<strong>Move 2</strong>, reason from the conflict between them; <strong>Move 3</strong>, land "
                   "on a rule or priority that answers it. Fold those into one check tool:" + REMEMBER +
                   "When you build your own, make the three moves, then run the 3-question check.")),
        Slot("MODEL", "discrimination", "Which paragraph holds the tension?",
             ref="", labeled_grade_c=True, bank="automation_policy",
             body=("Spot the target before you build it. Which option HOLDS the tension, and which three FLATTEN or "
                   "dodge it? "
                   "(A) Water should protect food first, because eating is the most basic need there is, and the "
                   "power side is a weak, secondary argument that does not really hold up once people go hungry.  "
                   "(B) Food is the more basic need, and yet the pumps that irrigate the crops run on the grid, so "
                   "protecting food already requires protecting some power, which is why a rationing rule fits.  "
                   "(C) Power should come first, because nearly everything runs on the grid, and next to that the "
                   "food argument is sentimental and emotional and does not carry any serious weight at all here.  "
                   "(D) Both food and power clearly matter a great deal, so the fair answer is simply to split the "
                   "scarce water evenly between them and give each use exactly the same share going forward. "
                   "Correct: B. B keeps both truths live and reasons straight from the conflict to a rule. A and C "
                   "flatten by dismissing the opposing side as weak or sentimental; D keeps both sides but dodges "
                   "the conflict with an even split, so it never reasons from the clash."),
             choices=[
                 {"id": "A", "text": "Water should protect food first, because eating is the most basic need there is, and the power side is a weak, secondary argument that does not really hold up once people go hungry.",
                  "correct": False,
                  "why": "It flattens the tension by dismissing the power side as weak, so only one truth is left standing and there is no reasoning from the conflict."},
                 {"id": "B", "text": "Food is the more basic need, and yet the pumps that irrigate the crops run on the grid, so protecting food already requires protecting some power, which is why a rationing rule fits.",
                  "correct": True,
                  "why": "Correct. Both truths stay live (food is basic AND farms run on power), the claim reasons from their conflict, and it lands on a rule instead of naming a winner."},
                 {"id": "C", "text": "Power should come first, because nearly everything runs on the grid, and next to that the food argument is sentimental and emotional and does not carry any serious weight at all here.",
                  "correct": False,
                  "why": "It flattens the tension the other way, calling the food side sentimental and dropping it, so it never reasons from the clash between the two needs."},
                 {"id": "D", "text": "Both food and power clearly matter a great deal, so the fair answer is simply to split the scarce water evenly between them and give each use exactly the same share going forward.",
                  "correct": False,
                  "why": "It does keep both truths in view, but it dodges the conflict with an even split instead of reasoning from it. The point is that farms run on the grid, so an equal share ignores the clash rather than holding it."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this paragraph most need?",
             bank="automation_policy",
             body=("Diagnose before the reveal. A student wrote: 'Protecting power is clearly right. The food "
                   "argument is emotional and not serious, so we can set it aside.' Which single move would most "
                   "improve it? "
                   "(A) keep the food need in view as a real truth and reason from how it conflicts with the power need  "
                   "(B) state even more firmly that the food argument is too emotional to matter, so it can be set aside for good  "
                   "(C) add a specific statistic about how much power the whole region consumes, so the case for power looks stronger  "
                   "(D) trim the wording and tighten every sentence so the whole paragraph reads shorter and moves along faster"),
             feedback=("Correct: A. Calling the food argument 'emotional and not serious' flattens a real tension. "
                       "The fix keeps the food need live and reasons from how it clashes with the power need, "
                       "landing on a position that answers the difficulty. A firmer dismissal (B), a statistic "
                       "(C), or shorter wording (D) all leave the tension flattened.")),
        Slot("SUPPORTED", "production_frq", "Warm up: write the pivot sentence",
             ref="", bank="automation_policy", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="Warm up with just the pivot, the sentence that keeps both truths live. Here is one truth "
                       "to start from:",
                 setapart_block=setapart("Truth to start from:",
                                         "Food is the more basic need, so scarce water should protect the crops."),
                 closer="Write ONE sentence that starts 'and yet ...' and grants the opposing truth from the "
                        "source (that irrigation runs on electric pumps, so protecting food depends on power). "
                        "Check that both truths are now live in your sentence.")),
        Slot("MODEL", "diagnosis_frq", "Check a flattened draft, then write one that holds",
             ref="", bank="automation_policy", scored=True,
             body=frq_prompt(
                 intro="First watch the check run on a weak draft, then write a fresh paragraph and run the same check.",
                 setapart_block=setapart("Weak draft to diagnose:",
                                         "Food matters most; the power point is not important and can be set aside.", "red"),
                 checklist_block=checklist(title="Run the 3-question check:", rows=[
                     ("Both truths live?", "No. The power point is dismissed as not important, so one truth is dropped. Restore it."),
                     ("Reason from the conflict?", "No. It avoids the clash instead of arguing from it. Build the claim out of the clash."),
                     ("Land on a position?", "No. It just names a winner. Reach a rule or a priority that answers the difficulty."),
                 ]),
                 closer="Now write a fresh paragraph on the water trade-off that holds the tension, then run the "
                        "same three questions on it. Finish by naming the tension you held.")),
        Slot("INDEPENDENT", "production_frq", "Hold the tension on your own",
             ref="", bank="automation_policy", rubric_ref="rc.4trait", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now. Write ONE body paragraph on the water trade-off.",
                 closer="Keep both true things in view, reason from the conflict between them, and land on a rule "
                        "or a priority, rather than dismissing one side. Holding a real tension is what every "
                        "complex argument is built on, and you are ready to do it cold. Run the 3-question "
                        "check before you submit.")),
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: prepare workers or protect them?",
             ref="ACC-W910-ARG-LESSON-WORKFORCEINVEST", bank="public_health",
             body=("A new source. Read it on whether a society should invest first in preparing more people for "
                   "fast-growing technical fields, or first in protecting the workers the change leaves behind. "
                   "Find the tension: each side has to grant the other's central fact. Note it, so your paragraph "
                   "can hold it. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Hold the tension on a NEW source",
             ref="", bank="public_health", rubric_ref="rc.4trait", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="New source, same move. Write ONE body paragraph on the workforce prompt.",
                 closer="Hold the tension between preparing the next generation and protecting displaced workers: "
                        "keep both truths live, reason from their conflict, and land on a priority. Do not flatten "
                        "one side. Run the 3-question check before you submit.")),
    ],
)

LESSONS = [LESSON]

if __name__ == "__main__":
    ok = True
    for L in LESSONS:
        qc_lesson(L); print(qc_report(L)); print(); ok = ok and L.qc["passed"]
    print(f"{sum(1 for L in LESSONS if L.qc['passed'])}/{len(LESSONS)} PASS")
    sys.exit(0 if ok else 1)
