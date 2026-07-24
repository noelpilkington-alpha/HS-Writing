"""
lesson_g12_l02_genuine_complexity.py  -  G12 KC C.12.01, ARCHETYPE T2 (STAND, sentence). V3.1. AP SOPHISTICATION.

G12 course L02 (Unit 1, guided). Rebuilt to the v3.1 spine (Noel 2026-07-15): ONE_IDEA teal callout + a real
teaching LIST (no prose wall), a coping-model think-aloud (First try -> Second try -> Final, with a literal
BEFORE and AFTER), the moves named + a REMEMBER 3-question check tool, a confound-broken discrimination (the
tension words "yet/so" appear in a DISTRACTOR too, so naming a REAL cost is the only invariant), predict-the-fix
with the reveal in feedback, a framed SUPPORTED write, a scaffolded DIAGNOSIS check, an autonomy INDEPENDENT
write, and a bank-partitioned TRANSFER. No leaked "Grade-C"/"design bet" labels, no named persona, no source
markup, no prior-work reference, no em dashes, no fabricated figures.

ONE IDEA: genuine complexity names a REAL tension the sources create and lets it shape the claim.
ONE REMINDER: the 3-question tension check. Passes all 23 lesson_contract gates.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Genuine complexity <strong>means</strong> naming a '
'<strong>REAL tension</strong> the sources create, a place where two things you value actually pull against each '
'other, and letting it shape your claim. A formulaic "on the other hand" that concedes nothing is not '
'complexity.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit a claim, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does it name a SPECIFIC cost your own side pays?</li>'
'<li style="margin:2px 0">Is the tension real (not just "some people disagree")?</li>'
'<li style="margin:2px 0">Does the tension shape the claim?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, the complexity is still a formula, not genuine yet.</div></div>')

# coping-model think-aloud: a WRITTEN drafting process (attempt -> test -> revise), then the endpoints.
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer thinking it through, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "We should fund training for growing fields. On the '
    'other hand, some people disagree. But overall, training is best." Check it: does the complexity name a real '
    'cost? No. "Some people disagree" names nothing my side has to answer. That is a formula. Start over.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "We should fund training, yet protecting the workers '
    'displaced now also matters." Better, it points at the other aim. But does it say what choosing training '
    'COSTS the present worker, and does that shape the claim? Not yet. Sharpen it.</p>'
    '<p style="margin:0"><strong>Final:</strong> "Funding training aims at the next generation, yet the same '
    'dollar could protect the worker displaced now, so funding preparation is defensible only if it admits it '
    'chooses the future workforce over the present one." A specific cost, and it shapes the claim. That passes.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "On the other hand, some people disagree. But overall, training '
    'is best." (a formula that concedes nothing)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "Funding training aims at the next generation, yet the same '
    'dollar could protect the worker displaced now, so funding preparation is defensible only if it admits it '
    'chooses the future workforce over the present one." (a real tension that shapes the claim)</span></div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G12-C1201-0002", grade="9-10", lesson_type=2,
    unit="G12 U1 - Sophistication (genuine complexity, not formula)",
    title="Show a Real Tension, Not a Formulaic Both-Sides",
    target=("Show genuine complexity by naming a real tension the sources create and letting it shape the "
            "claim, rather than a formulaic 'on the other hand' that concedes nothing real. The complexity "
            "move. Written at the sentence. Trait: Depth and Significance."),
    acc_tags=["ACC.W.ARG.2", "CCSS.W.11-12.1"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.12.01", "sot": "icm course-G12.md L02",
                "taught_stimulus": "ACC-W910-ARG-LESSON-WORKFORCEINVEST",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-WATERTRADEOFF",
                "playbook": "_phase2/playbook_T2_STAND.md",
                "one_idea": "Genuine complexity names a REAL tension the sources create and lets it shape the claim.",
                "one_reminder": "3-question tension check: specific cost? real tension? shapes the claim?",
                "template": "locked L01 template; binds G12 argument LESSON source; AP sophistication (Row C).",
                "version_note": ("V3.1 rebuild (2026-07-15): replaced the prose-wall body with the v3.1 spine "
                                 "(ONE_IDEA + teaching list, coping-model think-aloud with BEFORE/AFTER, named "
                                 "moves + REMEMBER 3-question tool, confound-broken discrimination via explicit "
                                 "choices=, predict reveal in feedback, framed supported write, scaffolded "
                                 "diagnosis, autonomy independent write, bank-partitioned transfer). Removed the "
                                 "leaked 'Grade-C'/'design bet' student text; labeled_grade_c stays in code only."),
                "council": ("T2/STAND G12 sophistication guided rung: cS2 genuine-complexity vs formulaic "
                            "on-the-other-hand. STAND=proposal; unit=sentence (T2 ceiling).")},
    fade_ledger_moves=["genuine-complexity", "name-a-real-tension"],
    slots=[
        # ===== TEACH: ONE idea, then the minimum teaching as a real list =====
        Slot("TEACH", "teach_card", "The one idea: name a REAL tension, not a formula",
             body=(ONE_IDEA +
                   "Two moves look alike on the page but do opposite work, so keep them apart:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Formula</strong>: an empty gesture at balance that "
                   "concedes nothing your argument has to answer ('On the other hand, some people disagree, but "
                   "overall I am right'). A transition word does the work; no real cost is named.</li>"
                   "<li style=\"margin:4px 0\"><strong>Genuine complexity</strong>: it names a specific cost your "
                   "own side pays ('funding training means choosing the future worker over the one displaced "
                   "now') and lets that cost shape the position.</li></ul>"
                   "The test is simple: does your complexity name a real cost your side pays? 'Some disagree' does "
                   "not; 'this dollar cannot also protect the displaced worker' does. Today's task: state a claim "
                   "whose complexity names a real, specific tension the sources create.")),
        Slot("TEACH", "stimulus_display", "Read the source: prepare workers or protect them?",
             ref="ACC-W910-ARG-LESSON-WORKFORCEINVEST", bank="public_health",
             body=("Read this source on whether public money should first prepare more people for growing fields "
                   "or first protect the workers a change is displacing. As you read, look for the REAL tension "
                   "(what favoring either aim costs the other), so your claim can name it. The text stays on "
                   "screen while you work.")),

        # ===== MODEL: coping-model think-aloud, the two moves named, the check tool folded in =====
        Slot("MODEL", "annotated_before_after", "Watch a formula become genuine complexity",
             bank="public_health",
             body=("Here is the skill in action. Follow the writer's thinking as a formula gets rebuilt into a "
                   "real tension. " + COPING_HTML +
                   " Notice the two moves that turned the BEFORE into the AFTER: the writer <strong>named the "
                   "specific cost</strong> the position pays (the same dollar cannot also protect the displaced "
                   "worker), then <strong>let that cost shape the claim</strong> (the position holds only if it "
                   "admits the choice). " + REMEMBER +
                   "When you write your own, build it the same way: name the real cost first, then let it shape "
                   "the position, and run the 3 questions before you submit.")),
        Slot("MODEL", "discrimination", "Which claim shows genuine complexity?",
             ref="", labeled_grade_c=True, bank="school_phone_policy",
             body=("Now that you have seen one built, spot the target on a different question. A school is deciding "
                   "whether to ban phones during the day. Which claim shows GENUINE complexity (names a real cost "
                   "the position pays), and which only runs a formula? "
                   "(A) A school should ban phones during the day, yet other people clearly disagree with that "
                   "rule, so after weighing every side a full ban is still the strongest choice for the school "
                   "overall.  "
                   "(B) A phone ban protects the lesson, yet the same rule cuts off the one tool a student in "
                   "crisis reaches for, so a ban is fair only if it admits it trades away that safety for focus.  "
                   "(C) A school phone ban is clearly the smartest, most responsible policy there is, and nobody "
                   "who genuinely cares about students could reasonably argue against putting the rule in place "
                   "right away.  "
                   "(D) A school should ban phones during the day, because leaving phones on only pulls students "
                   "off the lesson and wastes class time, so once you see what the alternative costs, a full ban "
                   "is plainly the better call.  "
                   "Correct: B names a real, specific cost (the ban cuts off the tool a student in crisis reaches "
                   "for) and lets it shape the claim. A uses 'yet' and 'so' but concedes nothing real; C just "
                   "asserts force; D names a real cost but pins it on the other option, so the ban itself still "
                   "concedes nothing. Genuine complexity is the move."),
             choices=[
                 {"id": "A", "text": "A school should ban phones during the day, yet other people clearly disagree with that rule, so after weighing every side a full ban is still the strongest choice for the school overall.",
                  "correct": False,
                  "why": "This has the tension words 'yet' and 'so,' but 'other people disagree' names no real cost the position pays. A transition on an empty gesture is still a formula, not genuine complexity."},
                 {"id": "B", "text": "A phone ban protects the lesson, yet the same rule cuts off the one tool a student in crisis reaches for, so a ban is fair only if it admits it trades away that safety for focus.",
                  "correct": True,
                  "why": "Correct. It names a real, specific cost (the ban cuts off the tool a student in crisis reaches for) and lets that cost shape the claim. The tension is genuine, not a transition word standing in for one."},
                 {"id": "C", "text": "A school phone ban is clearly the smartest, most responsible policy there is, and nobody who genuinely cares about students could reasonably argue against putting the rule in place right away.",
                  "correct": False,
                  "why": "This just asserts the position more forcefully and denies any real opposing cost. Force is not complexity; it names no tension the argument has to answer."},
                 {"id": "D", "text": "A school should ban phones during the day, because leaving phones on only pulls students off the lesson and wastes class time, so once you see what the alternative costs, a full ban is plainly the better call.",
                  "correct": False,
                  "why": "This does name a real cost, but it is the cost of the OTHER option (leaving phones on). The ban it argues for still pays no cost, so the position concedes nothing. Genuine complexity names a cost your OWN side pays."},
             ]),
        Slot("MODEL", "discrimination", "Which claim lets the tension change the position?",
             ref="", labeled_grade_c=True, bank="public_health",
             body=("Here is a harder case. All four sentences below admit that preparing workers and "
                   "protecting displaced workers pull against each other, but only one lets that tension "
                   "actually change the position it argues for. Which one shows genuine complexity?"),
             choices=[
                 {"id": "A", "text": "Retraining takes years the displaced worker does not have, but a growing economy still needs a prepared workforce, so we should simply fund as much retraining as we possibly can right now.",
                  "correct": False,
                  "why": "This names a real cost, but the claim then ignores it and funds training anyway, so the tension is decoration and never shapes the position."},
                 {"id": "B", "text": "Retraining takes years the displaced worker does not have, so a program earns support only if it also pays that worker a livable income while the training happens.",
                  "correct": True,
                  "why": "Correct. It names a specific cost and lets that cost reshape the claim into a conditional one, so the tension does real work in the position."},
                 {"id": "C", "text": "Retraining matters and protecting workers matters, and reasonable people can weigh both of these important considerations carefully before they decide.",
                  "correct": False,
                  "why": "This only says both aims matter and never names a specific cost or commits to a position, so it weighs nothing and stays a vague both-sides gesture."},
                 {"id": "D", "text": "Retraining takes years the displaced worker does not have, which we should keep in mind, but we should still fund as much retraining as possible.",
                  "correct": False,
                  "why": "This names the specific cost and even promises to 'keep it in mind,' but the position stays unconditional and unchanged. Gesturing at the tension is not the same as letting it reshape the claim, so it is not yet genuine complexity."},
             ]),
        Slot("MODEL", "predict_the_fix", "What makes this complexity genuine?",
             bank="public_health",
             body=("Diagnose this draft before the reveal. A student wrote: 'Protecting displaced workers is "
                   "right. However, there are other views. Still, protection is best.' Which single move would "
                   "most improve it? "
                   "(A) replace 'there are other views' with the real cost (protection now does nothing to "
                   "prepare the next generation) and say how that cost shapes the priority  "
                   "(B) add one more transition such as 'on the other hand' just before the final sentence so the "
                   "draft signals even more back-and-forth balance between the two sides  "
                   "(C) state the position far more forcefully by adding words like 'clearly' and 'without a "
                   "doubt' so the claim sounds much more certain that it is the correct one  "
                   "(D) remove the opposing side completely so the draft only argues that protecting displaced "
                   "workers is right and never once mentions any other view at all"),
             feedback=("Correct: A. 'There are other views' is the empty formula; genuine complexity names the "
                       "specific cost (protection does not prepare the young) and lets it shape the claim. "
                       "Another transition (B), more force (C), or dropping the other side (D) never create real "
                       "complexity.")),

        # ===== SUPPORTED: framed write on the taught source =====
        Slot("SUPPORTED", "production_frq", "State a claim that names a real tension",
             ref="", bank="public_health", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on the one move: naming a real cost, then letting it shape the claim.",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "______ [your position on the workforce prompt], yet ______ [the specific cost that choice pays the other side] so ______ [how the position still holds]."),
                 closer="Name a genuine, specific tension, not 'on the other hand.' Write one sentence, then check "
                        "it against the 3 questions.")),
        # COUNCIL FIX (2026-07-24): Option A (later-in-arc). Was a bundle: mark 3 yes/no checks + rewrite + name
        # the tension in one box (unscoreable, wired to no grader; the (q,a) "your call: yes / no" rows leaked the
        # marking act). Now ONE graded act (the rewrite); the 3 checks print READ-ONLY beneath as plain strings
        # (no typed yes/no), and the "name which tension" tail is dropped.
        Slot("MODEL", "diagnosis_frq", "Fix a formulaic claim into one that names a real tension",
             ref="", bank="public_health", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="This weak draft gestures at both sides but names no real cost. Rewrite it into one claim "
                       "whose complexity names a real tension.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "Training is best, though others may disagree, but I still think training wins.", "red"),
                 checklist_block=checklist(title="Make your rewrite pass these (no need to type answers):", rows=[
                     "Does it name a SPECIFIC cost the position pays?",
                     "Is the tension real, not just a transition word?",
                     "Does the tension shape the claim?",
                 ]),
                 closer="This draft only says others disagree. Rewrite it into one claim on the workforce prompt "
                        "that names a specific cost your side pays and lets it shape the position. Run the three "
                        "checks above before you submit.")),

        # ===== INDEPENDENT: cold write, autonomy + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Show genuine complexity on your own",
             ref="", bank="public_health", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now, no frame. The task: as the workforce shifts, should a society invest first in preparing more people, or first in protecting the workers displaced now?",
                 closer="Pick the priority you can actually defend, then write ONE claim whose complexity names a "
                        "real, specific cost that choice pays and lets it shape the position. This tension-naming "
                        "move is what every genuinely complex argument is built on, and you are ready to do it "
                        "cold. Check it against the 3 questions before you submit.")),

        # ===== TRANSFER: same move, the OTHER bound source (bank-partitioned) =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: water for food or power?",
             ref="ACC-W910-ARG-LESSON-WATERTRADEOFF", bank="automation_policy",
             body=("A different debate now, so you build a fresh claim. Read this new source on protecting scarce "
                   "water for growing food or for generating power. Find the REAL tension (what favoring either "
                   "use costs the other), so your claim can name it. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Show genuine complexity on a NEW source",
             ref="", bank="automation_policy", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="New source. The task: when water is scarce, should a region protect it first for food or first for power?",
                 closer="Write ONE claim whose complexity names a real, specific cost the choice pays and lets it "
                        "shape the position. Same tension-naming move as the workforce claim, new source. Do not "
                        "use a formulaic 'on the other hand.' Check it against the 3 questions before you submit.")),
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
