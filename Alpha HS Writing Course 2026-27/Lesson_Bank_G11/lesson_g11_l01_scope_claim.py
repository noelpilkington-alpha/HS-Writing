"""
lesson_g11_l01_scope_claim.py  -  G11 KC C.11.01, ARCHETYPE T2 (STAND, sentence). V3.1.

G11 course L01 (Unit 1 Nuance, intro). Scope the claim (N1): narrow WHICH case, whom, or when it covers, so
the claim is defensible instead of a sweeping everyone/always overreach. Locked L01 template; CLAIM-TIER binds
issue_frame. Taught: FRAME-AIWORKFORCE -> transfer: FRAME-INFRASTRUCTURE (bank-partitioned). rc.ap, sentence
ceiling. STAND=proposal. G11 register.

V3.1 spine (Noel 2026-07-14 pattern, ported to G11): ONE_IDEA teal callout + a real teaching LIST (no prose
wall); coping-model think-aloud (First try -> Second try -> Final, literal BEFORE/AFTER); MOVES decompose that
folds in a REMEMBER 3-question check tool; discrimination (homogeneous-length options, no surface-token
confound, no leaked internal label); predict-the-fix with the reveal in feedback; a fill-in FRAME supported
write; a scaffolded diagnosis (watch the check on a provided weak draft, then rewrite); a cold independent
write that says the standard; and a bank-partitioned transfer on the energy-spending debate.

ONE IDEA: a scoped claim narrows whom/which/when and is defensible; a sweeping one is not.
ONE REMINDER: the 3-question scope test. Passes all 23 lesson_contract gates. Own words, no fabricated
figures, no em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A <strong>scoped</strong> claim narrows '
'<strong>whom</strong>, <strong>which case</strong>, or <strong>when</strong> it covers, so it is defensible. '
'A <strong>sweeping</strong> claim (everyone, always, all) is not: one exception sinks it.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 scope questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit any claim, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does a sweeping word (always, everyone, all) overreach?</li>'
'<li style="margin:2px 0">Is whom or which case it covers actually named?</li>'
'<li style="margin:2px 0">Could one exception sink it?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If a sweeping word overreaches, or nobody is named, or one exception sinks it, narrow it until it holds.</div></div>')

# coping-model think-aloud: a WRITTEN drafting process (draft -> run the check -> catch the overreach -> revise),
# then the two literal endpoints. No named person (Timeback stateless rule).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer thinking it through, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "The government should always control which jobs '
    'people train for." Check it: does a sweeping word overreach? Yes, "always" plus "which jobs" claims far '
    'more than anyone can defend. One worker who should not be steered sinks it. Narrow it.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "The government should help workers train for '
    'growing fields." Better, but whom is still not named, and it could still mean everyone. Name the case.</p>'
    '<p style="margin:0"><strong>Final:</strong> "For workers whose industries are shrinking, the government '
    'should fund retraining toward growing fields." Now it names whom (displaced workers) and what (fund '
    'retraining, not assign jobs). One exception no longer sinks it. That holds.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "The government should always control which jobs people train '
    'for." (a sweeping overreach)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "For workers whose industries are shrinking, the government '
    'should fund retraining toward growing fields." (a scoped, defensible claim)</span></div>'
'</div>')

DECOMPOSE_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#f0fdf4;padding:10px 14px;border-bottom:1px solid #bbf7d0;font-size:15px">'
    'The scoped claim: <em>"For workers whose industries are shrinking, the government should fund retraining '
    'toward growing fields."</em></div>'
  '<div style="padding:12px 14px">'
    '<div style="margin:0 0 10px">'
      '<span style="display:inline-block;background:#dbeafe;color:#1e3a8a;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">MOVE 1 - NARROW WHOM/WHICH/WHEN</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px"><strong>"For workers whose industries are '
      'shrinking"</strong> The writer names exactly whom the claim covers, instead of "everyone."</div></div>'
    '<div>'
      '<span style="display:inline-block;background:#fef9c3;color:#854d0e;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">MOVE 2 - NARROW WHAT IT ASKS</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px">"...the government should <strong>fund '
      'retraining toward growing fields</strong>." The action is limited (fund access to training), not the '
      'sweeping "control which jobs people train for."</div></div>'
    '<div style="margin-top:10px;color:#0f766e;font-size:13px">Narrow whom, then narrow what it asks. That is '
    'the whole move. Every claim you scope is tightened the same way.</div>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1101-0001", grade="9-10", lesson_type=2,
    unit="G11 U1 - Nuance (scope the claim)",
    title="Scope the Claim: Narrow It to What You Can Defend",
    target=("Scope a claim by narrowing which case, whom, or when it covers, so it is defensible rather than a "
            "sweeping everyone/always overreach. Written at the sentence. Trait: Thesis."),
    acc_tags=["ACC.W.ARG.1", "CCSS.W.11-12.1a"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.01", "sot": "icm course-G11.md L01",
                "taught_stimulus": "ACC-W910-FRAME-AIWORKFORCE",
                "transfer_stimulus": "ACC-W910-FRAME-INFRASTRUCTURE",
                "one_idea": "A scoped claim narrows whom/which/when and is defensible; a sweeping one is not.",
                "one_reminder": "3-question scope test: sweeping word overreaches? whom/which named? one exception sinks it?",
                "playbook": "_phase2/playbook_T2_STAND.md",
                "template": "locked L01 template; CLAIM-TIER binds issue_frame. G11 register.",
                "version_note": ("V3.1: rebuilt from the PRE-v3.1 prose-wall version to the v3.1 spine - "
                                 "ONE_IDEA callout + teaching list (no wall), coping-model think-aloud with "
                                 "literal BEFORE/AFTER, MOVES decompose folding in the REMEMBER 3-question check, "
                                 "homogeneous-length discrimination with no surface-token confound and no leaked "
                                 "internal label, predict-the-fix reveal moved to feedback, fill-in FRAME "
                                 "supported write, scaffolded diagnosis, cold independent write that says the "
                                 "standard, bank-partitioned transfer."),
                "council": ("T2/STAND G11 nuance intro: introduces N1 scope-the-claim (narrow which/whom/when). "
                            "The qualifying phrase is an app-owned mechanic, applied not re-taught. "
                            "STAND=proposal; sentence ceiling.")},
    fade_ledger_moves=["scope-the-claim", "narrow-which-whom-when"],
    slots=[
        # ===== TEACH: ONE idea only, then the minimum teaching as a real LIST (no prose wall) =====
        Slot("TEACH", "teach_card", "The one idea: narrow whom, which case, or when",
             body=(ONE_IDEA +
                   "At this level, precision is power. A claim can be narrowed on three axes, so keep them in "
                   "mind:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>WHOM</strong>: which people it covers (\"for displaced "
                   "workers,\" not \"everyone\").</li>"
                   "<li style=\"margin:4px 0\"><strong>WHICH case</strong>: which situations it covers (\"in "
                   "shrinking industries,\" not \"in every job\").</li>"
                   "<li style=\"margin:4px 0\"><strong>WHEN</strong>: the conditions under which it holds "
                   "(\"while a field is contracting,\" not \"always\").</li></ul>"
                   "The trap is sounding bold by being broad: broad is fragile, because a single counterexample "
                   "collapses it. A scoped claim survives, because it only asserts what you can back up. On the "
                   "scoring, the governing claim your whole response defends is called a "
                   "<dfn class=\"tb-glossary-term\" data-catalog-idref=\"def-thesis\" "
                   "title=\"Thesis means the single governing claim your whole response defends. You do not need "
                   "this word to finish today's task.\">thesis</dfn>, but you do not need that word for today's "
                   "task. Today: narrow a sweeping claim to a case you can defend.")),
        Slot("TEACH", "stimulus_display", "The debate: government and the AI workforce",
             ref="ACC-W910-FRAME-AIWORKFORCE", bank="ai_workforce_policy",
             body=("Read the short framing of the debate. In a moment you will watch a sweeping claim get scoped, "
                   "then scope your own. You only need the topic and the two sides.")),

        # ===== MODEL (before the quiz): coping-model think-aloud, then a MOVES decompose folding in the REMEMBER
        # check tool, then discrimination, then predict-the-fix. =====
        Slot("MODEL", "annotated_before_after", "Watch a sweeping claim get scoped",
             bank="ai_workforce_policy",
             body=("Here is the skill in action. Follow the writer's thinking as one sweeping claim is narrowed "
                   "to a defensible one. " + COPING_HTML +
                   " Read the BEFORE, then the AFTER: the writer narrowed whom it covers and what it asks. That "
                   "narrowing is the whole move.")),
        Slot("MODEL", "teach_card", "The two moves, and the check that catches an overreach",
             bank="ai_workforce_policy",
             body=("Break the scoped claim into its two moves, then keep the check tool for your own writing. " +
                   DECOMPOSE_HTML +
                   "Notice the writer never made the claim louder or added a fact; the writer narrowed it. " +
                   REMEMBER +
                   "When you write your own, do the same: narrow whom, then narrow what it asks, and run the 3 "
                   "scope questions before you submit.")),
        Slot("MODEL", "discrimination", "Which claim is scoped, not sweeping?",
             ref="", labeled_grade_c=True, bank="college_access_policy",
             body=("Now that you have seen one scoped, spot the target on a different debate: public funding for "
                   "college. Which claim is SCOPED (defensible), and which two overreach? "
                   "(A) The government should always cover the full cost of any degree for every student, no matter the program or its price.  "
                   "(B) For students from low-income families, the government should cover tuition at in-state public colleges.  "
                   "(C) In today's economy, the government should pay whatever tuition any student is charged at any college they choose. "
                   "Correct: B. It names whom (students from low-income families) and which case (in-state public "
                   "colleges), so one exception cannot sink it."),
             choices=[
                 {"id": "A", "text": "The government should always cover the full cost of any degree for every student, no matter the program or its price.",
                  "correct": False,
                  "why": "This overreaches: 'always' plus 'every student' claims more than anyone can defend, and one exception sinks it."},
                 {"id": "B", "text": "For students from low-income families, the government should cover tuition at in-state public colleges.",
                  "correct": True,
                  "why": "Correct. It names whom (students from low-income families) and narrows which case it covers (in-state public colleges), so a single counterexample no longer collapses it."},
                 {"id": "C", "text": "In today's economy, the government should pay whatever tuition any student is charged at any college they choose.",
                  "correct": False,
                  "why": "The opening phrase sounds narrow, but 'any student' plus 'any college' is still a sweeping overreach. A qualifier at the front does not scope a claim if the action stays universal."},
             ]),
        Slot("MODEL", "discrimination", "Which claim is scoped, not just softened?",
             ref="", labeled_grade_c=True, bank="ai_workforce_policy",
             body=("One more, since softening a claim is not the same as scoping it. Which claim is actually "
                   "SCOPED (it names whom or which case), not just hedged or sweeping? "
                   "(A) The government should probably try to help nearly everyone get ready for future careers in some way.  "
                   "(B) When a local industry shuts down, the government should offer the laid-off workers free retraining.  "
                   "(C) The government must guarantee that every single adult in the country is placed into a secure, high-paying job in whatever field they personally prefer. "
                   "Correct: B. It names which case (a local industry shutting down) and whom (the laid-off "
                   "workers), so one exception cannot sink it."),
             choices=[
                 {"id": "A", "text": "The government should probably try to help nearly everyone get ready for future careers in some way.",
                  "correct": False,
                  "why": "Softer words like 'probably' and 'in some way' lower the tone, but 'nearly everyone' still covers almost every worker, so nothing has actually been narrowed."},
                 {"id": "B", "text": "When a local industry shuts down, the government should offer the laid-off workers free retraining.",
                  "correct": True,
                  "why": "Correct. It names which case (a local industry shutting down) and whom it covers (the laid-off workers), so a single exception no longer collapses it."},
                 {"id": "C", "text": "The government must guarantee that every single adult in the country is placed into a secure, high-paying job in whatever field they personally prefer.",
                  "correct": False,
                  "why": "Guaranteeing 'every single adult' a job in any field they prefer overreaches, and one person who cannot be placed sinks it."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this sweeping claim most need?",
             bank="ai_workforce_policy",
             body=("Diagnose this draft before the reveal. A student wrote: 'Government programs should train "
                   "everyone for technology jobs.' Which single move would most improve it? "
                   "(A) scope it, so it names whom it covers and what it asks and one exception cannot sink it  "
                   "(B) state it far more forcefully so the claim takes a much bolder and more sweeping stand  "
                   "(C) add the plain fact that technology jobs tend to pay well and grow quickly these days  "
                   "(D) reword the sentence to sound smoother and more polished without changing what it actually covers"),
             feedback=("Correct: A. 'Everyone' and 'technology jobs' overreach, so a single exception (a worker "
                       "who should not retrain into tech) sinks it. The fix scopes it: name whom (for example, "
                       "workers whose fields are shrinking) and what (fund access to training, not assign jobs). "
                       "A more forceful tone (B) or a supporting fact (C) do not narrow it, and rewording it to "
                       "read more smoothly (D) leaves what it covers exactly as broad.")),

        # ===== SUPPORTED: fill-in FRAME on the taught topic (source already read) =====
        Slot("SUPPORTED", "production_frq", "Scope the claim: fill in whom and what",
             ref="", bank="ai_workforce_policy", rubric_ref="rc.ap", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on the two moves.",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "For ______ [narrow whom or which case], the government should ______ [a narrowed action]."),
                 closer="Name whom it covers and narrow what it asks, so a single exception could not sink it. "
                        "Then check it against the 3 scope questions.")),
        # DIAGNOSIS: watch the check run on a PROVIDED weak draft, then rewrite. Stays on the taught topic (no new
        # source to read). No "Step 1/Step 2" prose; the checklist() renders the moves once.
        Slot("MODEL", "diagnosis_frq", "Check and fix a weak draft with the scope questions",
             ref="", bank="ai_workforce_policy", scored=True,
             body=frq_prompt(
                 intro="Run the 3 scope questions on this weak draft, then rewrite it into a scoped claim.",
                 setapart_block=setapart("Weak draft to fix:", "The government should always manage the job market.", "red"),
                 checklist_block=checklist(title="Run the test:", rows=[
                     ("Does a sweeping word overreach?", "Yes, 'always' claims too much. Drop it and add a condition."),
                     ("Is whom or which case named?", "No. Name the workers or the situation it covers."),
                     ("Could one exception sink it?", "Yes. Narrow it until a single counterexample no longer collapses it."),
                 ]),
                 closer="Now rewrite the weak draft into one scoped claim that passes all three. Then name what "
                        "your claim is scoped to (whom, which case, or when).")),

        # ===== INDEPENDENT: cold write, no frame, autonomy + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Scope a claim on your own",
             ref="", bank="ai_workforce_policy", rubric_ref="rc.ap", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="On your own now, no frame. The question: should the government steer workers toward "
                       "growing fields, or leave it to the market?",
                 closer="Take the side you actually hold, then scope it: name whom or which case it covers so it "
                        "is defensible. Scoping a claim to a case you can defend is what every real thesis is "
                        "built on, and you are ready to do it cold. Run the 3 scope questions before you submit.")),

        # ===== TRANSFER: same move, a new topic (energy spending), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "The debate: build capacity or fix the grid first",
             ref="ACC-W910-FRAME-INFRASTRUCTURE", bank="energy_spending_priority",
             body=("A different debate now, so you scope a fresh claim instead of reusing the last one. Read the "
                   "short framing, then take a scoped position on where energy money should go first. You only "
                   "need the topic and the two sides.")),
        Slot("TRANSFER", "production_frq", "Scope a claim on a NEW topic",
             ref="", bank="energy_spending_priority", rubric_ref="rc.ap", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="New topic. The question: should energy money go first to new clean-power capacity, or "
                       "first to the grid that carries and stores it?",
                 closer="Write ONE scoped claim: narrow which case, whom, or when it covers (for example, 'in "
                        "regions where the grid is already strained, spend first on ...'). Same scoping move you "
                        "used on the workforce claim, new topic. Run the 3 scope questions before you submit.")),
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
