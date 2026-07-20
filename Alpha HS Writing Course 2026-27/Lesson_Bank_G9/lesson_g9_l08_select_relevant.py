"""
lesson_g9_l08_select_relevant.py  -  G9 KC C.9.02, ARCHETYPE T3: EVIDENCE-INTEGRATION (PROVE, ceiling paragraph).

G9 course L08. Guided rung: select the RELEVANT evidence (G2) that proves THIS claim, and choose the right
form (G1 quote/paraphrase/summary). Recycles I1 (attribution). Locked L01 template; EVIDENCE-TIER binds full
sources. Taught: MIGRATION (full) -> transfer: PHONEBAN (full, partitioned). rc.staar, unit="sentence".
PROVE=established-caveat; mechanics gated; no coping-model persona; no source markup; no prior-work ref; no
em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report

BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> a real fact, but it does not prove the claim</span>'
    '<p style="margin:8px 0 0;font-size:15px">Claim: birds migrate to survive the seasons. Evidence: '
    '"According to the National Park Service, some birds fly across entire oceans."</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The fact is true and the source is named, but it '
    'is about how FAR birds fly, not about WHY they migrate. It does not prove this claim.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> the fact that actually proves the claim</span>'
    '<p style="margin:8px 0 0;font-size:15px">Claim: birds migrate to survive the seasons. '
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">RELEVANT</span> Evidence: According to the National Park Service, birds '
      'migrate mainly to find food and to raise their young when cold weather hides the insects and plants '
      'they eat.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">This fact is about WHY birds migrate, which is '
    'exactly what the claim is about. Picking the fact that fits the claim is the move.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C902-0008", grade="9-10", lesson_type=3,
    unit="G9 U1 - Claim/controlling-idea + evidence (select relevant evidence)",
    title="Pick the Evidence That Actually Proves Your Claim",
    target=("From a source, choose the piece of evidence that proves THIS claim, not just any true fact, and "
            "choose the right form (quote, paraphrase, or summarize). Written at the sentence. Trait: "
            "Evidence/Development."),
    acc_tags=["ACC.W.SRC.1", "CCSS.W.9-10.8"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12",
                "mnemonic_status": "established-caveat", "kc": "C.9.02", "sot": "icm course-G9.md L08",
                "taught_stimulus": "ACC-W910-INFO-LESSON-MIGRATION",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-PHONEBAN",
                "playbook": "_phase2/playbook_T3_PROVE.md",
                "template": "locked L01 template; EVIDENCE-TIER binds full sources.",
                "council": "T3/PROVE guided rung: introduces G2 select-relevant (relevant-to-the-claim vs true-but-off-point); recycles I1 attribution + G1 form."},
    fade_ledger_moves=["select-relevant-to-the-claim", "quote-paraphrase-or-summarize"],
    slots=[
        Slot("TEACH", "teach_card", "Not every true fact proves your claim",
             body=("A source is full of true facts, but only some of them prove YOUR claim. Selecting relevant "
                   "evidence means choosing the fact that actually supports the exact point you are making, not "
                   "just any interesting fact from the reading. Picture a claim that birds migrate to survive "
                   "the seasons. A fact about how far birds fly is true, and its source may be named, but it is "
                   "about distance, not about WHY they migrate, so it does not prove that claim. The fact about "
                   "why birds migrate does. You also still choose a form: quote the exact words when the wording "
                   "matters, paraphrase when you want the fact in your own words, or summarize for the big "
                   "picture, and you still name the source. The trap here is grabbing the first fact you find "
                   "instead of the fact that fits. Goal today: pick the piece of evidence that proves the claim, "
                   "and bring it in named.")),
        Slot("TEACH", "stimulus_display", "Read the source: animal migration",
             ref="ACC-W910-INFO-LESSON-MIGRATION", bank="animal_migration",
             body=("Read this source about animal migration. Because your job is to pick the RIGHT evidence, "
                   "read the whole thing and notice the different facts it offers: why birds migrate, how far "
                   "they travel, the routes they follow, and how scientists track them. Keep a claim in mind, "
                   "birds migrate to survive the seasons, and watch for the facts that prove it. The text stays "
                   "on screen while you work.")),
        Slot("TEACH", "discrimination", "Which fact proves the claim?",
             ref="", labeled_grade_c=True, bank="animal_migration",
             body=("Sort these before you write (spotting the target before producing it, a Grade-C design bet "
                   "we label as a bet, not a proven ingredient). The claim is: birds migrate to survive the "
                   "seasons. Both facts are true and both name a source. Which one PROVES the claim? "
                   "(A) According to the National Park Service, some birds fly across entire oceans, "
                   "covering thousands of miles without stopping when they migrate.  "
                   "(B) According to the National Park Service, birds migrate mainly to find food and "
                   "raise their young when cold weather hides the food they eat. "
                   "Correct: B. Both are true and attributed. But (A) is about how FAR birds fly, not why they "
                   "migrate, so it is off-point for this claim. (B) is about WHY birds migrate, which is exactly "
                   "what the claim says, so it proves it.")),
        Slot("MODEL", "annotated_before_after", "Watch off-point evidence get swapped for relevant evidence",
             bank="animal_migration",
             body=("Here is off-point evidence being swapped for evidence that actually proves the claim. Read "
                   "the BEFORE, then the AFTER, and notice the fact changed to match what the claim is about."
                   + BEFORE_AFTER_HTML +
                   " The BEFORE used a true fact that did not fit the claim. The AFTER picks the fact about WHY "
                   "birds migrate, which is what the claim argues. Matching the evidence to the claim is the "
                   "move.")),
        Slot("MODEL", "predict_the_fix", "Why does this evidence not prove the claim?",
             bank="animal_migration",
             body=("Diagnose this draft before the reveal. Claim: birds migrate to survive the seasons. "
                   "Evidence the student chose: 'According to the National Park Service, some birds "
                   "follow the same routes their parents used.' Which single move would most improve it? "
                   "(A) swap in a fact about WHY birds migrate, since that is what the claim is about  "
                   "(B) add a longer, more detailed quote about the routes that migrating birds follow  "
                   "(C) remove the source name so the sentence reads smoothly and sounds less formal  "
                   "(D) make the claim shorter so it matches the length of the evidence sentence better"),
             feedback=("Correct: A. The evidence is true and attributed, but it is about the ROUTES birds "
                       "follow, not about WHY they migrate, so it does not prove a claim about surviving the "
                       "seasons. The fix is to select relevant evidence, a fact about why birds migrate (to "
                       "find food and raise young). A longer routes quote (B) stays off-point; removing the "
                       "source (C) makes it worse; shortening the claim (D) does not fix the mismatch.")),
        Slot("SUPPORTED", "production_frq", "Pick the relevant fact and bring it in named",
             ref="", bank="animal_migration", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("Use this frame for the claim 'birds migrate to survive the seasons': 'According to ______ "
                   "[source], ______ [a fact from the reading that proves THIS claim].' Goal: pick the fact "
                   "that actually proves the claim (about WHY birds migrate), name the source, and choose to "
                   "quote or paraphrase. Do not grab a true-but-off-point fact. Write one sentence. Scored on "
                   "Evidence/Development.")),
        Slot("MODEL", "diagnosis_frq", "Check your evidence: does it prove the claim?",
             ref="", bank="animal_migration", scored=True,
             body=("First watch the check run on a weak draft, then run it on a fresh sentence of your own. "
                   "Claim: birds migrate to survive the seasons. Weak draft: 'According to the U.S. Fish and "
                   "Wildlife Service, some migrations cover thousands of miles.' Run the check step by step. "
                   "Step 1, does the fact match the claim? No, it is about distance, not why birds migrate, so "
                   "swap in a why-fact. Step 2, source named? Yes. Step 3, form clear? It reads as a "
                   "paraphrase, fine. Now you: for the same claim, write one fresh sentence that brings in a "
                   "fact that PROVES it, then run the same checks. For each No, use the fix: pick a fact that "
                   "matches what the claim argues; name the source. Finish by naming which check your sentence "
                   "still needs most.")),
        Slot("INDEPENDENT", "production_frq", "Prove a claim with the right evidence, on your own",
             ref="", bank="animal_migration", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("On your own now. For the claim 'birds migrate to survive the seasons,' write one sentence "
                   "that proves it with a relevant fact from the source, named. Goal: pick the fact that "
                   "actually proves the claim, name its source, and choose to quote or paraphrase. Before you "
                   "submit, check: does the fact match what the claim argues, is the source named, is the form "
                   "clear? If any answer is no, fix it before you submit. Do not use a true-but-off-point fact. "
                   "Scored on Evidence/Development.")),
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: phones in school",
             ref="ACC-W910-ARG-LESSON-PHONEBAN", bank="phone_ban",
             body=("Read this new source about phones in school. Because your job is to pick the RIGHT "
                   "evidence, read the whole thing and notice the different facts it offers for and against a "
                   "ban. You will match a fact to a claim. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Pick the relevant evidence on a NEW topic",
             ref="", bank="phone_ban", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("New topic. For the claim 'phones make it harder for students to focus in class,' write one "
                   "sentence that proves it with a relevant fact from the phone source, named. Goal: pick the "
                   "fact that actually proves the claim, name its source, and choose to quote or paraphrase. "
                   "Same move as the migration sentence, new topic. Do not use a true-but-off-point fact. "
                   "Scored on Evidence/Development.")),
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
