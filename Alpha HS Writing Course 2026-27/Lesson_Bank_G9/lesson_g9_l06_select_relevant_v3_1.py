"""
lesson_g9_l08_select_relevant_v3_1.py  -  G9 KC C.9.02, ARCHETYPE T3 (PROVE, ceiling paragraph). V3.1.

V3.1 rebuild of lesson_g9_l08_select_relevant.py to the v3.1 spec (icm/_config/v3_1-lesson-build-spec.md),
adapting the pattern proven on G9 L01 v3.1. PRESERVED: teaching point (from a source, choose the piece of
evidence that PROVES this claim, not just any true fact), id ACC-W910-L-G9-C902-0008, and the existing bound
fact-sourced -LESSON- stimuli (MIGRATION taught, PHONEBAN transfer). Changes vs the prior L08:
  1. ONE IDEA, hammered (KH load): a teal ONE_IDEA callout states the single core idea (relevant evidence
     proves THIS claim), then the minimum teaching as a LIST (relevant vs off-point + form/name) instead of
     the old 156-word prose block that tripped format_fidelity.
  2. COPING-MODEL THINK-ALOUD (SRSD): the model is rewritten as a written selection process (grab a fact ->
     run the relevance check -> catch the off-point fact -> pick the fact that fits), not a clean finished
     panel. Still contains literal BEFORE and AFTER (content_depth). The reusable relevance check tool is
     attached at the point of first use (the model card), not cold in step 1.
  3. FIXED THE KEYWORD CONFOUND (DI, faultless communication): the prior discrimination let attribution
     co-vary with correctness in effect; now every option is attributed AND a DISTRACTOR carries the claim's
     surface word ('seasonal') while the CORRECT fact carries none of the claim's words, so relevance (not
     word-matching) is the only invariant. Removed the leaked 'Grade-C design bet' label from the student text.
  4. DETERMINISTIC FRQ/DIAGNOSIS BODIES: production + diagnosis prompts are built with frq_prompt/setapart/
     checklist (no hand-written 'Step 1/2' prose that double-numbers), and carry NO 'Scored on ...' chrome.
  5. AUTONOMY + SAY-THE-STANDARD (Yeager): the independent write puts a DIFFERENT claim on the SAME source so
     the student cannot reuse the supported sentence, lets them choose the form, and names the standard out
     loud ('matching evidence to the exact claim is what every real argument runs on; you are ready').

ONE IDEA: relevant evidence is the fact that PROVES this claim, not just any true fact. ONE REMINDER: the
relevance test. Passes all 23 lesson_contract gates. Own words, federal-sourced facts, no em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Relevant evidence is the fact that <strong>PROVES '
'this claim</strong>, not just any true fact. A fact can be true, and even come straight from your source, '
'and still not prove your point.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the relevance test</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you use any fact, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">What exactly does the claim say?</li>'
'<li style="margin:2px 0">Does this fact prove THAT, or is it just true?</li>'
'<li style="margin:2px 0">Is the source named?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If a fact is true but does not answer question 2, '
'it is off-point. Do not use it.</div></div>')

# coping-model think-aloud panel: a WRITTEN selection process (grab -> test -> catch off-point -> pick the
# fact that fits), then the BEFORE/AFTER endpoints (content_depth requires both literal words).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer picking evidence, fact by fact, for the claim that birds migrate to survive the seasons:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First grab:</strong> "The Arctic tern flies about 12,000 miles each '
    'way." Run the test: does that prove WHY birds migrate to survive? No, it is about distance, not survival. '
    'Off-point. Look again.</p>'
    '<p style="margin:0 0 8px"><strong>Second grab:</strong> "Birds follow set routes called flyways." Does '
    'that prove they migrate to survive the seasons? No, that is about the path they take, not the reason. '
    'Still off-point.</p>'
    '<p style="margin:0"><strong>The fact that fits:</strong> "According to the passage, birds '
    'migrate mainly to find food and to raise their young when cold weather hides the food they eat." Does '
    'that prove they migrate to survive the seasons? Yes, that is exactly the reason, and the source is named. '
    'That one proves it.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "The Arctic tern flies about 12,000 miles each way." (true, '
    'but about distance, not why they migrate)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "According to the passage, birds migrate mainly '
    'to find food and to raise their young when cold weather hides the food they eat." (the fact that proves '
    'the claim)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C902-0008", grade="9-10", lesson_type=3,
    unit="G9 U1 - Claim/controlling-idea + evidence (select relevant evidence)",
    title="Pick the Evidence That Actually Proves Your Claim",
    target=("From a source, choose the piece of evidence that proves THIS claim, not just any true fact. The "
            "form (quote, paraphrase, or summarize) was set in the prior lesson; here the whole job is relevance. "
            "Written at the sentence. Trait: Evidence/Development."),
    acc_tags=["ACC.W.SRC.1", "CCSS.W.9-10.8"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "established-caveat", "kc": "C.9.02",
                "sot": "icm course-G9.md L08; v3.1 spec icm/_config/v3_1-lesson-build-spec.md",
                "taught_stimulus": "ACC-W910-INFO-LESSON-MIGRATION",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-PHONEBAN",
                "one_idea": "Relevant evidence is the fact that PROVES this claim, not just any true fact.",
                "one_reminder": "relevance test: what does the claim say? does this fact prove THAT? is the source named?",
                "playbook": "_phase2/playbook_T3_PROVE.md",
                "template": "locked L01 template; EVIDENCE-TIER binds full sources.",
                "version_note": ("V3.1: rebuilt to the v3.1 spec on the L01 v3.1 pattern - ONE_IDEA callout + "
                                 "list teach (fixed the 156-word wall-of-text), coping-model selection "
                                 "think-aloud (SRSD), relevance check tool at point of first use, fixed the "
                                 "keyword confound in the discrimination + removed the leaked 'Grade-C' label "
                                 "(DI faultless communication), deterministic frq_prompt/setapart/checklist "
                                 "bodies (no 'Step N' double-number, no 'Scored on' chrome), autonomy + "
                                 "say-the-standard on the independent write with a DIFFERENT claim on the same "
                                 "source so the supported sentence cannot be reused (Yeager). Preserved teaching "
                                 "point, id, and the bound MIGRATION/PHONEBAN lesson stimuli."),
                "review_provenance": ("23 lesson_contract gates (exit 0) + gated_reading render-QC clean; "
                                      "adapts the adjudicated L01 v3.1 Council+Fable findings.")},
    fade_ledger_moves=["select-relevant-to-the-claim"],
    slots=[
        # ===== TEACH: ONE idea only (list, not a wall of prose; check tool held for point of first use) =====
        Slot("TEACH", "teach_card", "Not every true fact proves your claim",
             body=(ONE_IDEA +
                   "A source is full of true facts, but only some prove the exact point you are making. When you "
                   "line up evidence, keep two kinds apart:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>RELEVANT fact</strong>: it speaks to exactly what the "
                   "claim says. If the claim is about WHY birds migrate, a fact about why they migrate is "
                   "relevant.</li>"
                   "<li style=\"margin:4px 0\"><strong>Off-point fact</strong>: true, maybe interesting, but "
                   "about something else. A fact about how FAR birds fly is off-point for a claim about why "
                   "they migrate, even though it is true and named.</li></ul>"
                   "Once you have the fact that fits, bring it in the right way: quote the exact words when the "
                   "wording matters, or put the fact in your own words, and name the source either way. The trap "
                   "is grabbing the first fact you find instead of the fact that fits. Today: pick the piece of "
                   "evidence that proves the claim, and bring it in named.")),
        Slot("TEACH", "stimulus_display", "Read the source: animal migration",
             ref="ACC-W910-INFO-LESSON-MIGRATION", bank="animal_migration",
             body=("Read this source about animal migration. Because your job is to pick the RIGHT evidence, "
                   "read the whole thing and notice the different facts it offers: why birds migrate, how far "
                   "they travel, the routes they follow, and how scientists track them. Hold this claim in mind, "
                   "birds migrate to survive the seasons, and watch for the facts that prove it. The text stays "
                   "on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model selection think-aloud + the relevance check tool =====
        Slot("MODEL", "annotated_before_after", "Watch a writer pick the fact that fits the claim",
             bank="animal_migration",
             body=("Here is the skill in action. Follow the writer's thinking below as one off-point fact after "
                   "another gets rejected until the fact that fits is found. " + COPING_HTML +
                   " Notice the two moves that turned the BEFORE into the AFTER: the writer MATCHED the fact to "
                   "what the claim actually says, then brought it in with the source NAMED. " + REMEMBER +
                   "When you pick your own evidence, do the same: match the fact to the claim first, then name "
                   "the source, and run the relevance test before you commit to it.")),
        Slot("MODEL", "discrimination", "Which fact proves the claim?",
             ref="", labeled_grade_c=True, bank="animal_migration",
             body=("Now that you have seen one built, spot the target. The claim is: birds migrate to survive "
                   "the seasons. All four facts are true and all four name the source. Which one PROVES the "
                   "claim? "
                   "(A) According to the passage, the Arctic tern flies about 12,000 miles in each direction, the longest migration of any animal on Earth.  "
                   "(B) According to the passage, birds follow set seasonal routes, called flyways, that run between their breeding grounds and their winter grounds.  "
                   "(C) According to the passage, birds migrate mainly to find food and to raise their young when cold weather hides the food they eat.  "
                   "(D) According to the passage, scientists track where migrating birds travel by fitting them with small numbered leg bands. "
                   "Correct: C. It is about WHY birds migrate, which is exactly what the claim says. (A) is "
                   "about distance and (B) is about the route, so both are off-point even though they are true "
                   "and named. (D) is about how scientists STUDY migration, not why birds migrate, so it is "
                   "off-point too."),
             choices=[
                 {"id": "A", "text": "According to the passage, the Arctic tern flies about 12,000 miles in each direction, the longest migration of any animal on Earth.",
                  "correct": False,
                  "why": "This is true and the source is named, but it is about how FAR birds fly, not why they migrate. Distance does not prove a claim about surviving the seasons."},
                 {"id": "B", "text": "According to the passage, birds follow set seasonal routes, called flyways, that run between their breeding grounds and their winter grounds.",
                  "correct": False,
                  "why": "This has the word 'seasonal' in it, but it is about the ROUTE birds follow, not why they migrate to survive. A matching word is not the same as a matching fact."},
                 {"id": "C", "text": "According to the passage, birds migrate mainly to find food and to raise their young when cold weather hides the food they eat.",
                  "correct": True,
                  "why": "Correct. It is about WHY birds migrate, to find food when cold weather hides it, which is exactly what the claim says, even though it never repeats the words 'survive' or 'seasons.' The fact that fits the claim is what proves it, not the fact with the matching word."},
                 {"id": "D", "text": "According to the passage, scientists track where migrating birds travel by fitting them with small numbered leg bands.",
                  "correct": False,
                  "why": "This is true and names the source, but it is about how scientists STUDY migration, not why birds migrate to survive. A fact about the tracking method does not prove the claim's reason."},
             ]),
        # Second minimal pair on the SAME skill (select the fact that PROVES the claim), a DIFFERENT claim from
        # the same source and a DIFFERENT confound than the first: here the traps are a true-but-off-point big
        # NUMBER (60,000 reports) and a true-but-background HISTORY fact (founded 1920), so the invariant is
        # 'does this fact explain the method the claim names,' not word-matching. Correct (C) is not the longest.
        Slot("MODEL", "discrimination", "Which fact proves the banding claim?",
             ref="", labeled_grade_c=True, bank="animal_migration",
             body=("Here is a second claim from the same source: bird banding lets scientists trace the path "
                   "one bird takes. All four facts below are true and all four name the source. Which one "
                   "PROVES that claim? "
                   "(A) According to the passage, the U.S. Geological Survey's Bird Banding Laboratory receives over 60,000 band reports from hunters each year, and each report adds another clue about the hidden paths that birds follow.  "
                   "(B) According to the passage, the U.S. Geological Survey established the national Bird Banding Laboratory in 1920.  "
                   "(C) According to the passage, a scientist places a numbered band on a bird's leg, and if that bird is later found elsewhere, the band number reveals where it traveled.  "
                   "(D) According to the passage, birds migrate mainly to find food and to raise their young when cold weather hides the food they eat. "
                   "Correct: C. It explains HOW banding traces a bird's path, which is exactly what the claim "
                   "says. (A) is about how many reports arrive and (B) is about when the program began, so both "
                   "are true and named but off-point. (D) is a true fact from the same source about why birds "
                   "migrate, a different subject entirely, so it does not prove the banding claim."),
             choices=[
                 {"id": "A", "text": "According to the passage, the U.S. Geological Survey's Bird Banding Laboratory receives over 60,000 band reports from hunters each year, and each report adds another clue about the hidden paths that birds follow.",
                  "correct": False,
                  "why": "This is true and names the source, but it tells how many reports arrive, not how banding follows one bird, so a big number does not prove the claim."},
                 {"id": "B", "text": "According to the passage, the U.S. Geological Survey established the national Bird Banding Laboratory in 1920.",
                  "correct": False,
                  "why": "This is a true fact about when the program began, not about how banding traces a bird's path, so it leaves the claim unproven."},
                 {"id": "C", "text": "According to the passage, a scientist places a numbered band on a bird's leg, and if that bird is later found elsewhere, the band number reveals where it traveled.",
                  "correct": True,
                  "why": "Correct. It explains the actual method, tag the bird, then read the band number when it turns up somewhere else, which is exactly how banding traces the path a bird takes."},
                 {"id": "D", "text": "According to the passage, birds migrate mainly to find food and to raise their young when cold weather hides the food they eat.",
                  "correct": False,
                  "why": "This is true and names the source, but it is about WHY birds migrate, a different subject from how banding traces one bird's path, so it grabs a fact from elsewhere in the source that does not prove this claim."},
             ]),
        Slot("MODEL", "predict_the_fix", "Why does this evidence not prove the claim?",
             bank="animal_migration",
             body=("Diagnose this draft before the reveal. Claim: birds migrate to survive the seasons. "
                   "Evidence the student chose: 'According to the passage, birds follow set seasonal "
                   "routes, called flyways.' Which single move would most improve it? "
                   "(A) swap in a fact about WHY birds migrate, since that is what the claim is about  "
                   "(B) add a longer, more detailed quote about the routes that migrating birds follow  "
                   "(C) remove the source name so the sentence reads more smoothly and sounds less formal  "
                   "(D) make the claim shorter so it matches the length of the evidence sentence better"),
             feedback=("Correct: A. The evidence is true and attributed, but it is about the ROUTES birds "
                       "follow, not about WHY they migrate, so it does not prove a claim about surviving the "
                       "seasons. The fix is to select relevant evidence, a fact about why birds migrate (to "
                       "find food and raise their young). A longer routes quote (B) stays off-point; removing "
                       "the source (C) makes it worse; shortening the claim (D) does not fix the mismatch.")),

        # ===== SUPPORTED: framed write (fill-in frame) on the taught claim (source already read at STEP 2) =====
        Slot("SUPPORTED", "production_frq", "Pick the relevant fact and bring it in named",
             ref="", bank="animal_migration", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on picking the fact that fits the claim: birds "
                       "migrate to survive the seasons.",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "According to ______ [the source], ______ [a fact from the reading that proves THIS claim]."),
                 closer="Pick the fact about WHY birds migrate, name the source, and choose to quote or "
                        "paraphrase. Do not grab a true-but-off-point fact. Then run the relevance test before "
                        "you submit.")),
        # DIAGNOSIS = check-and-fix on a PROVIDED weak draft (not a fresh production, so it does not repeat the
        # supported write). Stays on the taught source = no new reading (load). Uses checklist() so the check
        # renders as one clean numbered list (no 'Step N' double-numbering).
        Slot("MODEL", "diagnosis_frq", "Check your evidence: does it prove the claim?",
             ref="", bank="animal_migration", scored=True,
             body=frq_prompt(
                 intro="Run the relevance test on this weak draft, then rewrite it into a sentence that proves "
                       "the claim that birds migrate to survive the seasons.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "According to the passage, some bird migrations cover thousands of miles.", "red"),
                 checklist_block=checklist(title="Run the test:", rows=[
                     ("What is the claim about?", "Why birds migrate, to survive the seasons."),
                     ("Does this fact prove THAT?", "No. It is about distance, not the reason. Swap in a why-fact."),
                     ("Is the source named?", "Yes, the passage is named as the source. Keep that, just swap the fact."),
                 ]),
                 closer="Now rewrite the weak draft into one sentence that proves the claim with a relevant "
                        "fact, named. Then name which question your rewrite fixed.")),

        # ===== INDEPENDENT: cold write, SAME source but a DIFFERENT claim (cannot reuse the supported
        #        sentence) + autonomy on form + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Prove a different claim with the right evidence, on your own",
             ref="", bank="animal_migration", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now, no frame, and a different claim from the same source: scientists depend "
                       "on reports from everyday people to learn where birds travel.",
                 closer="Find the fact in the reading that actually proves THIS claim, not the earlier one about "
                        "why birds migrate, and bring it in with the source named. You choose whether to quote "
                        "the exact words or put the fact in your own words. Matching the evidence to the exact "
                        "claim is what every real argument is built on, and you are ready to do it cold. Run the "
                        "relevance test before you submit.")),

        # ===== TRANSFER: same move, a NEW source (phones), bank-partitioned from the taught source =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: phones in school",
             ref="ACC-W910-ARG-LESSON-PHONEBAN", bank="phone_ban",
             body=("Read this new source about phones in school. Because your job is to pick the RIGHT evidence, "
                   "read the whole thing and notice the different facts it offers, on focus, on safety, on "
                   "bullying, and on how many schools already limit phones. In a moment you will match one fact "
                   "to a claim. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Pick the relevant evidence on a NEW topic",
             ref="", bank="phone_ban", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="New topic, same move. The claim: phones make it harder for students to focus in class.",
                 closer="Find the fact in the phone source that actually proves THIS claim, not a true-but-"
                        "off-point fact like how many schools already limit phones, and bring it in with the "
                        "source named. Choose to quote or paraphrase. Run the relevance test before you "
                        "submit.")),
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
