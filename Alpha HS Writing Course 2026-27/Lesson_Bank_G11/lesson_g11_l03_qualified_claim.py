"""
lesson_g11_l03_qualified_claim.py  -  G11 KC C.11.01, ARCHETYPE T2: CLAIM-BUILDING (STAND, ceiling sentence). V3.1.

G11 course L03 (Unit 1, independent). Qualified claim (N3): name the LIMIT of a position with a qualifier and
back it with a warrant ("when an industry is closing, ..., because ...") so the claim concedes its bound without
abandoning its commitment, vs a waffle that hedges until it says nothing. Recycles N1/N2. CLAIM-TIER binds
issue_frame. Taught: FRAME-AIWORKFORCE -> transfer: FRAME-INFRASTRUCTURE. rc.ap, unit="sentence". STAND=proposal.

V3.1 spine (Noel 2026-07-15): rebuilt from the PRE-v3.1 prose-wall body. Changes:
  1. TEACH = ONE idea (teal ONE_IDEA callout) + a real <ul> list, not a wall of prose. Warrant defined with a
     cue; thesis kept in a glossary tooltip (define_before_use).
  2. MODEL = coping-model think-aloud (First try -> run the check -> catch the waffle -> Final), with a LITERAL
     BEFORE and AFTER. No named person (Timeback stateless rule). The 3-question check folded in as a REMEMBER
     dashed box (the reusable job-aid).
  3. Discrimination distractors homogenised in length; the surface-token confound broken (both a distractor and
     the key carry "because"; both a distractor and the key open with a "when"-style clause), so bound+commit is
     the only invariant. No leaked internal labels; reveal in the "Correct:" tail.
  4. Predict-the-fix reveal lives in feedback=, not in the option text.
  5. Supported = fill-in FRAME; diagnosis = watch the check on a PROVIDED weak draft, then rewrite; independent =
     no frame + say-the-standard; transfer = same move on the OTHER bound stimulus.

ONE IDEA: a qualified claim names its LIMIT and still COMMITS, with a reason. ONE REMINDER: the 3-question test.
Passes all 23 lesson_contract gates. Own words, no fabricated figures, no em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A qualified claim names its '
'<strong>LIMIT</strong> and still <strong>COMMITS</strong>, with a reason. A waffle just hedges until it says '
'nothing.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit any qualified claim, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does it commit to a position, instead of hedging?</li>'
'<li style="margin:2px 0">Is the limit stated as a real bound (when ..., in most cases), not a vague "sometimes"?</li>'
'<li style="margin:2px 0">Is there a reason (a warrant) for the position?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, it is a waffle, not a qualified claim yet.</div></div>')

# coping-model think-aloud panel: a WRITTEN drafting process (attempt -> test -> revise), then the endpoints.
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer thinking it through, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Maybe the government should sometimes help some '
    'workers, but it really depends." Check it: does it commit? No, "maybe" and "sometimes" and "it depends" '
    'pile up until there is no position left. That is a waffle. Start over.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "The government should retrain workers." Now it '
    'commits, but it claims this for every worker in every case, which is easy to knock down, and it gives no '
    'reason. Bound it, and add a reason.</p>'
    '<p style="margin:0"><strong>Final:</strong> "When a worker\'s industry is closing, the government should '
    'fund retraining, because private hiring is too slow to catch a mid-career worker whose plant has shut." '
    'A stated limit, a commitment, and a reason. That passes.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "Maybe the government should sometimes help some workers, but '
    'it really depends." (a waffle: no position survives)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "When a worker\'s industry is closing, the government should '
    'fund retraining, because private hiring is too slow to catch a mid-career worker whose plant has shut." '
    '(a qualified claim: bounded, but committed, with a reason)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1101-0003", grade="9-10", lesson_type=2,
    unit="G11 U1 - Nuance (the qualified claim)",
    title="Qualify Without Waffling",
    target=("Write a qualified claim that names its limit with a qualifier and a reason (when/in most cases, "
            "because ...) yet still commits, rather than a waffle that hedges until it says nothing. Written at "
            "the sentence. Trait: Thesis."),
    acc_tags=["ACC.W.ARG.2", "CCSS.W.11-12.1"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.01", "sot": "icm course-G11.md L03",
                "taught_stimulus": "ACC-W910-FRAME-AIWORKFORCE",
                "transfer_stimulus": "ACC-W910-FRAME-INFRASTRUCTURE",
                "playbook": "_phase2/playbook_T2_STAND.md",
                "template": "v3.1 spine adapted from lesson_g9_l01_arguable_claim_v3_1.py; CLAIM-TIER binds issue_frame. G11 register.",
                "one_idea": "A qualified claim names its LIMIT and still COMMITS, with a reason.",
                "one_reminder": "3-question test: commit? limit stated as a bound? reason (warrant)?",
                "version_note": ("V3.1: rebuilt PRE-v3.1 prose-wall body to the v3.1 spine - ONE_IDEA teal "
                                 "callout + <ul> teach, coping-model think-aloud MODEL with literal BEFORE/AFTER, "
                                 "REMEMBER check-tool box, homogenised discrimination distractors with the "
                                 "surface-token confound broken, reveals moved to feedback/Correct tails, "
                                 "no leaked internal labels."),
                "council": ("T2/STAND G11 nuance independent rung: introduces N3 qualified claim (bound the "
                            "claim with a warrant, still commit). qualify-vs-waffle discrimination is a Grade-C "
                            "discriminate-before-produce bet (labeled in code only). STAND=proposal.")},
    fade_ledger_moves=["qualified-claim", "bound-with-a-warrant-still-commit"],
    slots=[
        # ===== TEACH: ONE idea only (teal callout + a real <ul>); warrant defined with a cue; thesis in a tooltip
        Slot("TEACH", "teach_card", "The one idea: name the limit, then still commit",
             body=(ONE_IDEA +
                   "Three sentence types look similar but do different jobs, so keep them apart:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>QUALIFIER</strong>: a phrase that marks where the claim "
                   "applies ('when a worker's industry is closing', 'in most cases'). It bounds the claim.</li>"
                   "<li style=\"margin:4px 0\"><strong>COMMIT + WARRANT</strong>: you still take the position "
                   "AND give the reason. A warrant is a reason that connects the position to why it holds "
                   "(usually the 'because ...' part).</li>"
                   "<li style=\"margin:4px 0\"><strong>WAFFLE</strong> (avoid this): stacking 'maybe', "
                   "'sometimes', 'it depends' until no position is left. Hedging is not the same as bounding.</li></ul>"
                   "A qualified claim does all three: it bounds the position, commits to it, and backs it with a "
                   "reason. (Scoring sometimes calls the governing claim a "
                   "<dfn class=\"tb-glossary-term\" data-catalog-idref=\"def-thesis\" "
                   "title=\"Thesis means the governing claim your whole response defends. You do not need this "
                   "word to finish today's task.\">thesis</dfn>, and a well-qualified one signals "
                   "real depth, but you do not need that word for today's task.) The trap is mistaking "
                   "hedging for nuance. Today: bound your claim, and still commit.")),
        Slot("TEACH", "stimulus_display", "The debate: government and the AI workforce",
             ref="ACC-W910-FRAME-AIWORKFORCE", bank="ai_workforce_policy",
             body=("Read the short framing of the debate. In a moment you will watch a claim get built, then "
                   "build your own within a stated limit (for example, only for certain workers). You only need "
                   "the topic and the two sides.")),

        # ===== MODEL (before the quiz): coping-model think-aloud + the reusable check tool folded in =====
        Slot("MODEL", "annotated_before_after", "Watch a waffle become a qualified claim",
             bank="ai_workforce_policy",
             body=("Here is the skill in action. Follow the writer's thinking below. " + COPING_HTML +
                   " Notice the two moves that turned the BEFORE into the AFTER: the writer added a "
                   "<strong>qualifier</strong> that bounds the claim, then kept the <strong>commitment</strong> "
                   "and a reason. " + REMEMBER +
                   "When you write your own, build it the same way: bound the claim, commit, add the reason, "
                   "then run the 3 questions before you submit.")),
        Slot("TEACH", "discrimination", "Which one is a qualified claim, not a waffle?",
             ref="", labeled_grade_c=True, bank="transit_fare_policy",
             body=("Now that you have seen one built, spot the target on a different debate: whether a city should "
                   "cut bus and train fares. Which sentence is a qualified claim, bounded but committed, and not "
                   "a waffle or a one-sided overreach? "
                   "(A) When it comes to fares, maybe the city should sometimes lower them, but honestly it "
                   "really depends and is hard to say for sure either way.  "
                   "(B) The city should always make every bus and train ride completely free, because free "
                   "transit beats asking riders to pay any fare at all under any circumstances.  "
                   "(C) When a bus route runs far below capacity, the city should cut its fares, because empty "
                   "seats cost the city the same to run as full ones.  "
                   "(D) When a bus route runs nearly empty, the city should cut its fares on that route. "
                   "Correct: C. It bounds the claim to a stated case AND still commits AND gives a reason. "
                   "(A) hedges until no position survives; (B) commits and has a reason but sets no limit, so "
                   "it overreaches to every ride in every case; (D) bounds and commits but gives no reason."),
             choices=[
                 {"id": "A", "text": "When it comes to fares, maybe the city should sometimes lower them, but honestly it really depends and is hard to say for sure either way.",
                  "correct": False,
                  "why": "This opens like it will set a limit, but then 'maybe', 'sometimes', 'it depends', and 'hard to say' pile up until no position is left. Hedging is not bounding."},
                 {"id": "B", "text": "The city should always make every bus and train ride completely free, because free transit beats asking riders to pay any fare at all under any circumstances.",
                  "correct": False,
                  "why": "This commits and even gives a reason ('because ...'), but it sets no limit: 'always' and 'every ride' overreach. A qualified claim bounds the case; this does not."},
                 {"id": "C", "text": "When a bus route runs far below capacity, the city should cut its fares, because empty seats cost the city the same to run as full ones.",
                  "correct": True,
                  "why": "Correct. It bounds the claim ('when a bus route runs far below capacity'), still commits ('should cut its fares'), and gives a reason. Bound plus commit plus reason is what makes it qualified, not any single word."},
                 {"id": "D", "text": "When a bus route runs nearly empty, the city should cut its fares on that route.",
                  "correct": False,
                  "why": "This bounds the claim to a real case and commits, but it stops there and never says why, so the reader is given no reason to accept it. A qualified claim also carries the warrant."},
             ]),
        Slot("MODEL", "discrimination", "Spot the qualified claim: real limit, a commitment, and a reason",
             ref="", labeled_grade_c=True, bank="ai_workforce_policy",
             body=("A fresh set, and they all sound careful. Which one is a genuinely qualified claim: it names a "
                   "real limit, commits to a position, AND gives a reason a reader could weigh, instead of faking "
                   "the limit, skipping the reason, or hedging away the position? "
                   "(A) The state should fund retraining seats every so often in various cases, because offering some form of assistance to workers who are affected is generally a reasonable step for a government to take.  "
                   "(B) When local factories automate their lines, the state should fund retraining seats, because laid-off workers cannot reskill fast enough on their own.  "
                   "(C) When local factories automate their lines, the state should fund retraining seats for displaced workers.  "
                   "(D) Perhaps the state should sometimes fund a few retraining seats, though in many cases it may be better not to. "
                   "Correct: B. It names a real condition (when factories automate), commits to funding "
                   "retraining, and gives a reason. (A) only pretends to set a limit with 'every so often in "
                   "various cases'; (C) sets a real limit and commits but never says why; (D) hedges until no "
                   "position is left."),
             choices=[
                 {"id": "A", "text": "The state should fund retraining seats every so often in various cases, because offering some form of assistance to workers who are affected is generally a reasonable step for a government to take.",
                  "correct": False,
                  "why": "This commits and gives a reason, but 'every so often in various cases' names no real condition, so it only pretends to set a limit."},
                 {"id": "B", "text": "When local factories automate their lines, the state should fund retraining seats, because laid-off workers cannot reskill fast enough on their own.",
                  "correct": True,
                  "why": "This names a real condition, commits to funding retraining, and gives a reason, so the limit, the position, and the reason are all present."},
                 {"id": "C", "text": "When local factories automate their lines, the state should fund retraining seats for displaced workers.",
                  "correct": False,
                  "why": "This sets a real limit and commits, but it stops there and never says why, so the reader is given no reason to accept it."},
                 {"id": "D", "text": "Perhaps the state should sometimes fund a few retraining seats, though in many cases it may be better not to.",
                  "correct": False,
                  "why": "'Perhaps', 'sometimes', and 'it may be better not to' hedge until no position survives. That is a waffle, not a bounded commitment: a qualified claim limits the case but still takes a side."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this waffle most need?",
             bank="ai_workforce_policy",
             body=("Diagnose this draft before the reveal. The task asked the student to argue whether the "
                   "government should steer workers toward growing fields. The student wrote: 'It might be good "
                   "for the government to help workers sometimes, though there are also reasons not to.' Which "
                   "single move would most improve it? "
                   "(A) commit to a position within a stated limit and give a reason for it  "
                   "(B) add another balancing phrase so the sentence shows even more sides  "
                   "(C) make the sentence longer by adding extra details and examples  "
                   "(D) delete the word 'might' and leave the rest of the sentence as it is"),
             feedback=("Correct: A. The draft hedges ('might', 'sometimes', 'reasons not to') until no claim "
                       "remains. The fix bounds AND commits: 'When an industry is closing, fund retraining, "
                       "because private hiring is too slow.' Another balancing phrase (B) or more length (C) "
                       "deepen the waffle; deleting one hedge word (D) adds neither a bound nor a reason.")),

        # ===== SUPPORTED: framed write (fill-in frame) on the taught topic (source already read at STEP 2) =====
        Slot("SUPPORTED", "production_frq", "Finish the claim: fill in the limit, the position, and the reason",
             ref="", bank="ai_workforce_policy", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on the three moves.",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "When ______ [the limit / which case], the government should ______ "
                                         "[commit to a position] because ______ [the reason]."),
                 closer="Bound the claim to a real case, still commit, and give a reason a reader could weigh. "
                        "Then check it against the 3 questions. Do not waffle. Write one sentence.")),
        # DIAGNOSIS = a CHECK-and-FIX on a PROVIDED draft (stays on the taught topic; no new source to read).
        Slot("MODEL", "diagnosis_frq", "Check and fix a weak draft with the 3 questions",
             ref="", bank="ai_workforce_policy", scored=True,
             body=frq_prompt(
                 intro="Run the 3-question test on this weak draft, then rewrite it into a real qualified claim.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "Perhaps the government could sometimes assist, depending on the situation.", "red"),
                 checklist_block=checklist(title="Run the test:", rows=[
                     ("Does it commit to a position?", "No, 'perhaps' and 'sometimes' hedge. Commit to one side."),
                     ("Is the limit stated as a bound (when ..., in most cases)?", "No, 'depending on the situation' is vague. Name the bound."),
                     ("Is there a reason (a warrant)?", "No. Add one with 'because'."),
                 ]),
                 closer="Now rewrite the weak draft into one qualified claim that passes all three. Then name "
                        "which limit your claim sets.")),

        # ===== INDEPENDENT: cold write on the taught topic, no frame + autonomy + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write a qualified claim on your own",
             ref="", bank="ai_workforce_policy", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now, no frame. The task: should the government steer workers toward growing "
                       "fields, or leave it to the market?",
                 closer="Pick the limited position you actually hold, then bound it, commit, and add a reason. "
                        "This bound-and-commit move is what every real qualified claim is built on, and you are "
                        "ready to do it cold. Check your sentence against the 3 questions before you submit.")),

        # ===== TRANSFER: same move, a DIFFERENT topic (energy spending), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "The debate: build capacity or fix the grid first",
             ref="ACC-W910-FRAME-INFRASTRUCTURE", bank="energy_spending_priority",
             body=("A different debate now, so you build a fresh claim instead of reusing the last one. Read the "
                   "short framing, then take a limited side (for example, only where the grid is already "
                   "strained). You only need the topic and the two sides.")),
        Slot("TRANSFER", "production_frq", "Write a qualified claim on a NEW topic",
             ref="", bank="energy_spending_priority", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="New topic. The task: should energy money go first to new clean-power capacity, or first "
                       "to the grid?",
                 closer="Write ONE qualified claim: bound it with a qualifier (for example, 'where the grid is "
                        "already strained'), commit, and give a reason. Same bound-and-commit move as the "
                        "AI-workforce claim, new topic. Check it against the 3 questions before you submit.")),
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
