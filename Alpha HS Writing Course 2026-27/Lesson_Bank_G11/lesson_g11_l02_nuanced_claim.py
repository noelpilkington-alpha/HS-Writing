"""
lesson_g11_l02_nuanced_claim.py  -  G11 KC C.11.01, ARCHETYPE T2 (STAND, sentence). V3.1.

G11 course L02 (Unit 1, guided). The nuanced claim (N2): the not-X-but-Y shape, naming the close rival position
you reject so your exact stance is unmistakable, vs a flat one-sided assertion or fence-sitting. Recycles N1.
CLAIM-TIER binds issue_frame. Taught: FRAME-INFRASTRUCTURE -> transfer: FRAME-AIWORKFORCE. rc.ap,
unit="sentence". STAND=proposal.

V3.1: rebuilt from the pre-v3.1 prose-wall body onto the v3.1 spine (mirrors lesson_g9_l01 v3.1):
  1. TEACH = ONE_IDEA teal callout + a real <ul> list (no wall of text); thesis in a glossary tooltip.
  2. MODEL BEFORE THE QUIZ: coping-model think-aloud (draft -> check -> catch -> revise) with literal BEFORE
     and AFTER, then a named-MOVES decompose, then the REMEMBER check tool. Discrimination + predict-the-fix
     follow the model.
  3. Discrimination uses explicit choices=[]; correct option is NOT the lone longest; a DISTRACTOR carries the
     word "not" (fence-sitting) so the not-X-but-Y STRUCTURE, not the token "not", is the only invariant.
  4. No leaked internal labels ("Grade-C"/"design bet") in student text (labeled_grade_c stays True in code).
  5. SUPPORTED = fill-in frame; DIAGNOSIS = check-then-rewrite on a provided weak draft; INDEPENDENT = cold
     write + say-the-standard; TRANSFER = same move on the other bound stimulus.

ONE IDEA: a nuanced claim names what your position is NOT, then what it IS (not-X-but-Y).
ONE REMINDER: the 3-question nuance check. Own words, no fabricated figures, no em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A <strong>nuanced claim</strong> names what your '
'position is <strong>NOT</strong>, then what it <strong>IS</strong>: the <strong>not-X-but-Y</strong> shape. '
'A flat one-sided assertion and a fence-sitting "both matter" both skip that move.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit any claim, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does it commit to one side (not fence-sit)?</li>'
'<li style="margin:2px 0">Does it name the close position it is NOT?</li>'
'<li style="margin:2px 0">Does it say what it IS instead?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, it is not a nuanced claim yet.</div></div>')

# coping-model think-aloud: a WRITTEN drafting process (attempt -> test -> catch -> revise), then the endpoints.
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer thinking it through, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "The country should spend its energy money on the '
    'grid." Check it: does it name the close position it is NOT? No. A careless reader could not tell it apart '
    'from someone who just wants to build less. The stance is fuzzy.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "The problem is not that the country builds too '
    'little clean power, so spend on the grid." Better: it now names what it is NOT. But it never says what the '
    'real problem IS, so the but-Y half is missing.</p>'
    '<p style="margin:0"><strong>Final:</strong> "The problem is not that the country builds too little clean '
    'power, but that it cannot move and store what it builds, so energy money should go first to the grid." '
    'Not-X, then but-Y. That pins the exact stance.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "The country should spend its energy money on the grid." '
    '(flat and one-sided)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "The problem is not that the country builds too little clean '
    'power, but that it cannot move and store what it builds, so energy money should go first to the grid." '
    '(a nuanced claim)</span></div>'
'</div>')

DECOMPOSE_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#f0fdf4;padding:10px 14px;border-bottom:1px solid #bbf7d0;font-size:15px">'
    'The finished claim: <em>"The problem is not that the country builds too little clean power, but that it '
    'cannot move and store what it builds, so energy money should go first to the grid."</em></div>'
  '<div style="padding:12px 14px">'
    '<div style="margin:0 0 10px">'
      '<span style="display:inline-block;background:#dbeafe;color:#1e3a8a;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">MOVE 1 - NOT X</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px"><strong>"The problem is not that the country '
      'builds too little clean power"</strong> The writer names the close rival position and rejects it, so a '
      'reader cannot confuse the two.</div></div>'
    '<div>'
      '<span style="display:inline-block;background:#fef9c3;color:#854d0e;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">MOVE 2 - BUT Y</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px">"...<strong>but that it cannot move and store '
      'what it builds, so energy money should go first to the grid</strong>." Now the exact stance is stated: '
      'a grid problem, not a capacity shortage.</div></div>'
    '<div style="margin-top:10px;color:#0f766e;font-size:13px">Not-X, then but-Y. That is the whole shape. '
    'Every nuanced claim you write is built the same way.</div>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1101-0002", grade="9-10", lesson_type=2,
    unit="G11 U1 - Nuance (the nuanced claim)",
    title="Nuance: Say What Your Position Is NOT",
    target=("Write a nuanced claim in the not-X-but-Y shape: name the close position you are rejecting so your "
            "exact stance is unmistakable, instead of a flat one-sided assertion or fence-sitting. Written at "
            "the sentence. Trait: Thesis."),
    acc_tags=["ACC.W.ARG.1", "CCSS.W.11-12.1a"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.01", "sot": "icm course-G11.md L02",
                "taught_stimulus": "ACC-W910-FRAME-INFRASTRUCTURE",
                "transfer_stimulus": "ACC-W910-FRAME-AIWORKFORCE",
                "one_idea": "A nuanced claim names what your position is NOT, then what it IS (not-X-but-Y).",
                "one_reminder": "3-question nuance check: commit? name what it is NOT? say what it IS?",
                "playbook": "_phase2/playbook_T2_STAND.md",
                "template": "v3.1 spine (mirrors lesson_g9_l01_arguable_claim_v3_1); CLAIM-TIER binds issue_frame. G11 register.",
                "version_note": ("V3.1: rebuilt pre-v3.1 prose-wall body onto the v3.1 spine - ONE_IDEA callout + "
                                 "<ul> teach (format_fidelity), coping-model think-aloud w/ literal BEFORE+AFTER, "
                                 "named-MOVES decompose + REMEMBER check tool, choices=[] discrimination with a "
                                 "'not'-carrying fence-sitting distractor to break the token confound, no leaked "
                                 "'Grade-C'/'design bet' in student text, frame + checklist writes."),
                "council": ("T2/STAND G11 nuance guided rung: introduces N2 nuanced claim (not-X-but-Y). "
                            "nuanced-vs-flat discrimination kept labeled_grade_c in code (no leaked label). The "
                            "appositive/relative clause for embedding is app-owned, applied not re-taught. "
                            "STAND=proposal.")},
    fade_ledger_moves=["nuanced-claim-not-x-but-y", "distinguish-from-close-position"],
    slots=[
        # ===== TEACH: ONE idea only (callout + list; no wall of text) =====
        Slot("TEACH", "teach_card", "The one idea: name what your position is NOT, then what it IS",
             body=(ONE_IDEA +
                   "A nuanced claim is when you set your position apart from the close rival, the one a careless "
                   "reader might confuse it with. Three sentences look like they take a stand, but only one pins "
                   "the exact stance:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Flat one-sided</strong>: picks a side but never says what "
                   "it is NOT ('spend on the grid'). A reader cannot tell it from the near alternative.</li>"
                   "<li style=\"margin:4px 0\"><strong>Fence-sitting</strong>: refuses to commit ('both "
                   "matter'). It never takes a side at all.</li>"
                   "<li style=\"margin:4px 0\"><strong>Nuanced (not-X-but-Y)</strong>: names the close position "
                   "it rejects, then states its own ('The problem is not X, but Y, so ...'). It commits, and it "
                   "commits precisely.</li></ul>"
                   "Nuance is not wishy-washy: it still takes a side, but it does so by rejecting the near "
                   "alternative out loud. (Scoring calls your governing claim a "
                   "<dfn class=\"tb-glossary-term\" data-catalog-idref=\"def-thesis\" "
                   "title=\"Thesis means the arguable claim your whole response defends. You do not need this "
                   "word to finish today's task.\">thesis</dfn>, and a nuanced one reads with more depth, "
                   "but you do not need that word for today's task.) Goal today: write one not-X-but-Y claim "
                   "that pins your position against the close one.")),
        Slot("TEACH", "stimulus_display", "The debate: build capacity or fix the grid first",
             ref="ACC-W910-FRAME-INFRASTRUCTURE", bank="energy_spending_priority",
             body=("Read the short framing of the debate. Notice the two close positions (build capacity vs fix "
                   "the grid); your nuanced claim will name which one it is NOT. You only need the topic and "
                   "the two sides.")),

        # ===== MODEL (before the quiz): coping-model think-aloud + named-MOVES decompose + check tool =====
        Slot("MODEL", "annotated_before_after", "Watch a flat claim become nuanced",
             bank="energy_spending_priority",
             body=("Here is the skill in action. Follow the writer's thinking as a flat claim is rebuilt into a "
                   "nuanced not-X-but-Y claim. " + COPING_HTML +
                   " Now name the two moves that turned the BEFORE into the AFTER: " + DECOMPOSE_HTML + REMEMBER +
                   "When you write your own, build it the same way: name what it is NOT, state what it IS, then "
                   "run the 3 questions before you submit.")),
        Slot("MODEL", "discrimination", "Which claim is nuanced, not flat or fence-sitting?",
             ref="", labeled_grade_c=True, bank="voting_age_policy",
             body=("Now that you have seen one built, spot the target on a different debate: lowering the voting "
                   "age to sixteen. Which sentence is NUANCED (not-X-but-Y), not a flat one-sided claim and not "
                   "fence-sitting? "
                   "(A) The country should lower the voting age to sixteen, because teenagers pay attention to the news and clearly care a great deal about the issues that will shape their own future.  "
                   "(B) Extending the vote to sixteen-year-olds and keeping it at eighteen are both genuinely reasonable positions, and honestly it is not at all easy to say which one is truly right.  "
                   "(C) The real question is not whether sixteen-year-olds care enough to vote but whether the ballot alone can reach them, so schools should register students to vote.  "
                   "(D) The real problem is not that sixteen-year-olds are too young or too uninformed to cast a ballot. "
                   "Correct: C. It names what its position is NOT (a question of whether teens care), then what it "
                   "IS (a question of reach). A only picks a side, B has the word 'not' but never commits to one, "
                   "and D rejects a rival but never says what it IS."),
             choices=[
                 {"id": "A", "text": "The country should lower the voting age to sixteen, because teenagers pay attention to the news and clearly care a great deal about the issues that will shape their own future.",
                  "correct": False,
                  "why": "This commits to a side and even gives a reason, but it never names the close rival it is rejecting, so it is flat, not nuanced. A reader still cannot tell it from anyone who simply likes the idea."},
                 {"id": "B", "text": "Extending the vote to sixteen-year-olds and keeping it at eighteen are both genuinely reasonable positions, and honestly it is not at all easy to say which one is truly right.",
                  "correct": False,
                  "why": "This has the word 'not,' but it fence-sits: it says both sides are reasonable and refuses to pick one. Nuance is not the same as refusing to commit."},
                 {"id": "C", "text": "The real question is not whether sixteen-year-olds care enough to vote but whether the ballot alone can reach them, so schools should register students to vote.",
                  "correct": True,
                  "why": "Correct. It names what its position is NOT (a question of whether teens care), then states what it IS (a question of reach). Not-X-but-Y is the nuance, and it is the structure, not any single word, that makes it work."},
                 {"id": "D", "text": "The real problem is not that sixteen-year-olds are too young or too uninformed to cast a ballot.",
                  "correct": False,
                  "why": "This names what its position is NOT and stops there, so the but-Y half is missing: the reader never learns what it thinks the real problem IS. Not-X alone is only half the move."},
             ]),
        Slot("MODEL", "discrimination", "Which one names the rival AND states its own side?",
             ref="", labeled_grade_c=True, bank="energy_spending_priority",
             body=("One more, on the other side of the debate. Which sentence is the full nuanced claim: it both "
                   "rejects the close rival AND states what it stands for? "
                   "(A) The country should absolutely pour its energy budget into building as much new solar and wind capacity as it possibly can over the next decade, without any further delay.  "
                   "(B) The real issue is not that the country builds too little wind and solar power each year.  "
                   "(C) The smarter move is not to keep patching the aging grid but to build far more clean capacity now, so the country finally has surplus power to draw on.  "
                   "(D) Both building new clean power and upgrading the grid are important, and reasonable people land on either side. "
                   "Correct: C. It rejects the close rival (patching the grid), then states its own side (build more capacity). A commits but never names the rival, B names what it rejects but never says what it stands for, and D fence-sits."),
             choices=[
                 {"id": "A", "text": "The country should absolutely pour its energy budget into building as much new solar and wind capacity as it possibly can over the next decade, without any further delay.",
                  "correct": False,
                  "why": "This commits hard to building capacity but never names the rival it is rejecting, so it stays flat: a reader cannot tell it from someone who simply wants more of everything."},
                 {"id": "B", "text": "The real issue is not that the country builds too little wind and solar power each year.",
                  "correct": False,
                  "why": "This rejects a close position but then stops, so the reader never learns what it stands for; the but-Y half that states your own side is missing."},
                 {"id": "C", "text": "The smarter move is not to keep patching the aging grid but to build far more clean capacity now, so the country finally has surplus power to draw on.",
                  "correct": True,
                  "why": "Correct. It rejects the close rival (patching the grid) and then states its own side (build more capacity), which is the complete not-X-but-Y move."},
                 {"id": "D", "text": "Both building new clean power and upgrading the grid are important, and reasonable people land on either side.",
                  "correct": False,
                  "why": "This fence-sits: it calls both sides important and refuses to pick one, so it never rejects a rival or commits. A nuanced claim takes a side by naming what it is NOT."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this flat claim most need?",
             bank="energy_spending_priority",
             body=("Diagnose this draft before the reveal. A student wrote: 'The country should build more solar "
                   "and wind.' Which single move would most improve it into a nuanced claim? "
                   "(A) name the close position it rejects (not-X-but-Y), so its exact stance is clear  "
                   "(B) add a supporting fact about how much cheaper solar and wind power have become lately  "
                   "(C) restate exactly the same side again using stronger and more confident sounding wording  "
                   "(D) turn it into an open question and let the reader work out the answer on their own"),
             feedback=("Correct: A. The claim states a side but never distinguishes it from the near alternative "
                       "(fix the grid), so its exact position is fuzzy. The nuanced fix names what it is NOT: "
                       "'The problem is not that the country cannot move the clean power it has, but that it "
                       "builds too little of it, so build more capacity.' A supporting fact (B), more confidence "
                       "(C), or a question (D) never add the not-X-but-Y distinction.")),

        # ===== SUPPORTED: framed write (fill-in frame) on the taught topic =====
        Slot("SUPPORTED", "production_frq", "Finish the claim: fill in the not-X and the but-Y",
             ref="", bank="energy_spending_priority", rubric_ref="rc.ap", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on the two moves.",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "The problem is not ______ [the close position you reject], but ______ "
                                         "[your position] so ______ [what follows]."),
                 closer="Name the close rival you reject, then commit to your own side. Do not write a flat "
                        "one-sided claim or fence-sit. Then check it against the 3 questions.")),
        # DIAGNOSIS = a CHECK-and-FIX exercise on a PROVIDED weak draft (no new source to read; taught topic).
        Slot("MODEL", "diagnosis_frq", "Check and fix a weak draft with the 3 questions",
             ref="", bank="energy_spending_priority", scored=True,
             body=frq_prompt(
                 intro="Run the 3-question nuance check on this weak draft, then rewrite it into a real nuanced claim.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "Both building power and fixing the grid are important.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Does it commit to one side?", "No, it fence-sits. Pick a side."),
                     ("Does it name the close position it is NOT?", "No. Add the rejected rival with 'not'."),
                     ("Does it say what it IS instead?", "No. State your own position with 'but'."),
                 ]),
                 closer="Now rewrite the weak draft into one nuanced claim that passes all three. "
                        "Then name the X your rewrite rejects.")),

        # ===== INDEPENDENT: cold write on the same topic, no frame + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write a nuanced claim on your own",
             ref="", bank="energy_spending_priority", rubric_ref="rc.ap", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="On your own now, no frame. The task: should energy money go first to new clean-power "
                       "capacity, or first to the grid?",
                 closer="Write ONE nuanced claim in the not-X-but-Y shape: name the close position you reject, "
                        "then commit to yours. This not-X-but-Y move is what every nuanced thesis is built "
                        "on, and you are ready to do it cold. Check it against the 3 questions before you submit.")),

        # ===== TRANSFER: same move, the OTHER bound stimulus (partitioned bank) =====
        Slot("TRANSFER", "stimulus_display", "The debate: government and the AI workforce",
             ref="ACC-W910-FRAME-AIWORKFORCE", bank="ai_workforce_policy",
             body=("A different debate now, so you build a fresh claim instead of reusing the last one. Read the "
                   "short framing, then notice the two close positions; your nuanced claim will name which it is "
                   "NOT. You only need the topic and the two sides.")),
        Slot("TRANSFER", "production_frq", "Write a nuanced claim on a NEW topic",
             ref="", bank="ai_workforce_policy", rubric_ref="rc.ap", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="New topic. The task: should the government steer workers toward growing fields, or leave "
                       "it to the market?",
                 closer="Write ONE nuanced claim in the not-X-but-Y shape (for example, 'the goal is not to "
                        "control careers but to widen access to retraining, so ...'). Same move as the energy "
                        "claim, new topic. Do not write a flat claim or fence-sit. Check it against the 3 "
                        "questions before you submit.")),
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
