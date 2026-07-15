"""
lesson_g10_l12_strong_weak_twin.py  -  G10 KC C.10.05, ARCHETYPE T5: RUBRIC-REVISION (CHECK, sentence). V3.1.

G10 course L12 (Unit 3, intro). Strong/weak twin (rD2): given two drafts that differ on ONE move, pick the
stronger one and NAME the specific reason it is better, then apply that judgment to improve a weak draft.
Teaching point (KEPT): the better draft is the one that gives a specific, checkable reason where the other is
vague or circular; naming that one difference is the skill, and once named you make the same fix in your own
draft. KC C.10.05. Bound stimuli KEPT: ACC-W910-INFO-LESSON-RECYCLING (taught) -> ACC-W910-INFO-LESSON-WEATHER
(transfer, bank-partitioned). rc.staar, unit="sentence" (T5 sentence-grain: every scored rewrite is a single
sentence, add a specific reason). CHECK=proposal; self_score calibration.

V3.1 rebuild of the PRE-v3.1 file (all prior gate failures fixed):
  1. TEACH is now ONE idea, hammered: a teal ONE_IDEA callout + the check as a real <ul> list (was a 125-word
     prose wall that failed format_fidelity). "circular reason" defined with an "is when" cue (define-before-use).
  2. NO leaked internal labels: the old discrimination prose said "a Grade-C design bet we label as a bet"
     (leaked_internal_label failed). Removed; discrimination now uses explicit choices=[{id,text,correct,why}]
     with the correct option NOT the lone-longest, and 'because'/'specific' tokens seeded across distractors so
     the checkable reason, not a surface word, is the invariant (DI faultless communication). labeled_grade_c
     stays True in code only.
  3. The reusable judge tool is a REMEMBER dashed box with a real <ol> 3-question checklist, at point of first
     use (the model card).
  4. Coping-model before/after panel: a writer drafts, runs the check, catches the circular reason, and revises
     (FIRST TRY / SECOND TRY / FINAL, literal BEFORE + AFTER). No named person (Timeback stateless).
  5. FRQ + diagnosis bodies built with frq_prompt / setapart / checklist (no "Step 1/2" prose, no "Scored on"
     chrome). Own words, faithful to the EPA/NWS sources, no fabricated figures, no em dashes.
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
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">The better draft is not the one that <em>sounds</em> nicer. '
'It is the one that gives a <strong>specific, checkable reason</strong> where the other is vague or circular.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: judge any reason in a draft</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you call one twin stronger, ask these three observable yes/no questions about its reason:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0"><strong>Reason, not feeling?</strong> Does it name a reason, not just say it is good or important?</li>'
'<li style="margin:2px 0"><strong>Specific and checkable?</strong> Could a reader verify the reason (a fact, a cause, an effect)?</li>'
'<li style="margin:2px 0"><strong>Circular?</strong> Or does it just restate the claim in new words? If so, it is the weaker twin.</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">A draft can feel finished and still be circular, so run the check even when a sentence sounds fine.</div></div>')

# Coping-model panel: a writer drafts a circular reason, runs the check, catches it, and revises to a specific one.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">FIRST TRY (BEFORE)</span>'
    '<p style="margin:8px 0 0;font-size:15px">Recycling is good and everyone should do it because it matters so '
    'much for the planet.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">Run the check: does it give a reason, not a feeling? '
    'It uses "because," so it looks like one. Is that reason specific and checkable? No. "Because it matters" just '
    'restates "is good." Nothing here a reader could verify. This reason is circular.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">SECOND TRY / FINAL (AFTER)</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">SPECIFIC REASON</span> Recycling is good and everyone should do it because materials like '
      'glass and aluminum can be remade into new products instead of being buried.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">The circular reason is replaced with one a reader '
    'could check: sorted materials are sold to factories and become new goods instead of ending in a landfill. '
    'That single move, the specific reason, is the whole difference between the weak twin and the strong twin.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1005-0012", grade="9-10", lesson_type=5,
    unit="G10 U3 - Rhetorical revision (strong/weak twin)",
    title="Pick the Better Draft and Say Why",
    target=("Compare two drafts that differ on one move, pick the stronger one, and name the specific reason "
            "it is better, then apply that judgment to improve a weak draft. Written at the sentence. Trait: "
            "Development."),
    acc_tags=["ACC.W.PROC.2", "CCSS.W.9-10.5"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.05", "sot": "icm course-G10.md L12",
                "taught_stimulus": "ACC-W910-INFO-LESSON-RECYCLING",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-WEATHER",
                "one_idea": "The stronger draft gives a specific, checkable reason where the other is vague or circular.",
                "one_reminder": "Judge the reason: reason not feeling? specific and checkable? or circular?",
                "playbook": "_phase2/playbook_T5_CHECK.md",
                "template": "locked L01 template; REVISION-TIER, provided drafts; source bound for context.",
                "version_note": ("V3.1 rebuild of the PRE-v3.1 lesson to the v3.1 build spec. Fixed the prior gate "
                                 "failures: (a) TEACH is now one hammered idea (ONE_IDEA callout + the check as a "
                                 "<ul>), was a 125-word prose wall that failed format_fidelity; (b) removed the leaked "
                                 "'Grade-C design bet we label as a bet' prose (leaked_internal_label) and rebuilt the "
                                 "discrimination with explicit choices, correct option NOT lone-longest, tokens spread "
                                 "across distractors; (c) coping before/after panel with FIRST TRY/SECOND TRY/FINAL "
                                 "and literal BEFORE+AFTER; (d) REMEMBER 3-question judge tool at point of first use; "
                                 "(e) FRQ + diagnosis built with frq_prompt/setapart/checklist. Kept id, KC, unit, "
                                 "bound stimuli, and every production unit='sentence'."),
                "council": ("T5/CHECK strong/weak twin: introduces rD2 (pick the better of two drafts differing "
                            "on one move, say why). better-for-a-reason-vs-guess discrimination labeled Grade-C in "
                            "code only. self_score calibration. CHECK=proposal; unit=sentence (single-sentence "
                            "rewrites, add a specific reason)."),
                "review_provenance": "built to the G9 L25 v3.1 pattern (icm/_config/v3_1-lesson-build-spec.md)."},
    fade_ledger_moves=["strong-weak-twin", "name-why-one-is-better"],
    slots=[
        # ===== TEACH: ONE idea, hammered (callout + the judge questions as a list) =====
        Slot("TEACH", "teach_card", "The one idea: judge the reason, not the feeling",
             body=(ONE_IDEA +
                   "A revision skill worth owning is comparing two drafts that differ on just ONE move and naming "
                   "which is stronger and why. A circular reason is when a sentence just restates its claim in new "
                   "words (\"important because it matters\") instead of naming something a reader could check. When "
                   "two drafts differ on that one move, the reason for your choice is visible. Watch for these "
                   "signals when you judge a reason:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Specific and checkable</strong>: it names a fact, cause, or "
                   "effect a reader could verify (\"reduces landfill waste because glass and aluminum can be "
                   "remade\").</li>"
                   "<li style=\"margin:4px 0\"><strong>Circular</strong>: it just restates the claim (\"good "
                   "because it matters\") and gives no real reason.</li>"
                   "<li style=\"margin:4px 0\"><strong>The trap</strong>: judging by feel (\"this one flows "
                   "better\") without naming the move.</li></ul>"
                   "Once you can name the exact difference, you can make the same fix in your own drafts. That is "
                   "the goal today: pick the stronger twin, name the reason, and use it to improve a weak draft.")),
        Slot("TEACH", "stimulus_display", "Read the source: how recycling works",
             ref="ACC-W910-INFO-LESSON-RECYCLING", bank="recycling",
             body=("The draft twins you judge are about recycling. Read this source so the topic is familiar. You "
                   "are not writing a recycling essay from scratch here; you are judging and improving single "
                   "sentences. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping before/after + the judge tool at point of first use =====
        Slot("MODEL", "annotated_before_after", "Watch a writer catch a circular reason and fix it",
             bank="recycling",
             body=("Here is the skill in action. A writer drafts a sentence, runs the check, catches that the "
                   "reason is circular, and revises to a specific one. Read the FIRST TRY, then the FINAL." +
                   BEFORE_AFTER_HTML +
                   " The two versions differ on ONE move, the reason. Naming that move, then making the same fix, "
                   "is the revision. " + REMEMBER +
                   "When you judge two twins, run these three questions on each reason before you pick.")),
        Slot("TEACH", "discrimination", "Which twin is stronger, and why?",
             ref="", labeled_grade_c=True, bank="recycling",
             body=("Two twins keep the SAME claim and differ on ONE move, the reason. Twin A: \"Recycling matters "
                   "because it is important for the planet.\" Twin B: \"Recycling matters because glass and aluminum "
                   "can be remade into new products instead of being buried.\" Which statement about them is correct?"),
             choices=[
                 {"id": "A", "text": "Twin A, because a shorter, simpler sentence gets the point across faster and does not slow the reader down.",
                  "correct": False,
                  "why": "Shorter is not the measure. Twin A gives no reason a reader could check; \"important for "
                         "the planet\" just restates \"matters,\" so it is the circular, weaker twin."},
                 {"id": "B", "text": "Twin B, because it names a specific reason a reader could check, while Twin A only restates its claim in new words.",
                  "correct": True,
                  "why": "Correct. The one move they differ on is the reason. Twin B names a specific, checkable "
                         "reason (materials remade instead of buried); Twin A is circular. Naming that is the skill."},
                 {"id": "C", "text": "They are equally strong, since both sentences give a specific-sounding reason and make the same basic point about recycling.",
                  "correct": False,
                  "why": "They are not equal. Only Twin B gives a reason a reader could verify; Twin A sounds like "
                         "it has a reason but only restates the claim, so the twins differ on that one move."},
             ]),
        Slot("MODEL", "predict_the_fix", "Which revision turns the weak twin into a strong one?",
             bank="recycling",
             body=("Predict before the reveal. A weak draft reads: \"Recycling saves energy because it is good.\" "
                   "Which single revision turns it into a strong twin? "
                   "(A) Replace the vague reason: making a can from recycled aluminum uses far less energy than "
                   "making one from raw ore.  "
                   "(B) Make the sentence noticeably longer and add several more words about why recycling is good "
                   "for everyone living on the planet.  "
                   "(C) State the claim in bolder, more forceful wording, since a stronger claim makes the whole "
                   "point feel more convincing to any reader.  "
                   "(D) Break it into two shorter sentences so the draft reads faster and is a little bit easier "
                   "for a reader to follow along with."),
             feedback=("Correct: A. The twins differ on one move, the reason. A replaces the circular reason (\"good\") "
                       "with a specific, checkable one straight from the source: recycled aluminum uses far less "
                       "energy than raw ore. Length (B), a bolder claim (C), or shorter sentences (D) leave the "
                       "circular reason in place. Naming and fixing that one move is the skill.")),
        # Second minimal pair, DIFFERENT confound: value-laden/persuasive tone (and "more general" wording) can
        # look like a reason. The invariant stays the checkable reason, not how confident or broad the sentence sounds.
        Slot("MODEL", "discrimination", "Persuasive tone or a checkable reason?",
             ref="", labeled_grade_c=True, bank="recycling",
             body=("Two twins share ONE claim and differ only on the reason. Twin P: \"Recycling paper is good "
                   "because it is a smart, responsible choice.\" Twin Q: \"Recycling paper is good because used "
                   "paper can be pulped into new sheets instead of cut trees.\" Which is the stronger twin?"),
             choices=[
                 {"id": "A", "text": "Twin P, because calling recycling a smart, responsible choice gives it a more persuasive, positive tone that is more likely to convince a reader to recycle.",
                  "correct": False,
                  "why": "A warmer or more persuasive tone is not a reason; \"smart, responsible choice\" just "
                         "restates that recycling is worth it, so Twin P is still circular."},
                 {"id": "B", "text": "Twin Q, because it names a checkable cause, used paper becoming new sheets, while Twin P only calls the choice smart and responsible.",
                  "correct": True,
                  "why": "Correct. Twin Q points to a cause a reader could check, used paper pulped into new sheets, "
                         "while Twin P only labels the choice, so Twin Q is the stronger twin."},
                 {"id": "C", "text": "Twin P, because a general reason like smart and responsible fits any material, so it covers more ground.",
                  "correct": False,
                  "why": "Being general is not the same as being strong; Twin P names nothing a reader could verify, "
                         "while Twin Q gives a specific, checkable cause."},
             ]),

        # ===== SUPPORTED: predict the score (calibration MCQ) -> then rewrite with a fill-in frame =====
        Slot("SUPPORTED", "self_score", "Score a twin, then see the verdict",
             ref="", bank="recycling",
             body=("Predict, then reveal. A draft reads: \"Recycling saves resources because it is good for the "
                   "environment.\" On a 2-point scale (2 = a specific, checkable reason; 1 = vague or circular), "
                   "what does it earn?"),
             choices=[
                 {"id": "1", "text": "1 out of 2", "correct": True,
                  "why": "Correct. \"Good for the environment\" just restates \"saves resources,\" so the reason is "
                         "circular and caps it at 1. A 2 would add a checkable reason, for example that making a can "
                         "from recycled aluminum uses far less energy than making one from raw ore."},
                 {"id": "2", "text": "2 out of 2", "correct": False,
                  "why": "A 2 needs a specific, checkable reason. Here \"good for the environment\" only restates the "
                         "claim, so it is circular. Notice how a sentence can sound finished while its reason is "
                         "empty."},
             ]),
        Slot("SUPPORTED", "production_frq", "Rewrite the weak twin using the frame",
             ref="", bank="recycling", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Turn this weak twin into a strong one: \"Recycling is important because it matters for the "
                       "planet.\" Keep the claim, but replace the circular reason with a specific, checkable one. "
                       "Start from the frame.",
                 setapart_block=setapart("Fill-in frame:",
                                         "Recycling [your claim] because [a specific reason a reader could check, "
                                         "for example a fact from the source]."),
                 checklist_block=checklist(title="Check your reason:", rows=[
                     "Keep the same claim that recycling is important.",
                     "The reason must be specific and checkable (a fact, cause, or effect), not a restatement.",
                 ]),
                 closer="Write your strong twin as one sentence.")),
        # DIAGNOSIS: watch the check run on a provided weak draft, then run it on a fresh sentence in this box.
        Slot("MODEL", "diagnosis_frq", "Check a fresh draft: specific reason, or circular?",
             ref="", bank="recycling", scored=True,
             body=frq_prompt(
                 intro="First watch the check run on a provided draft, then run it on a fresh sentence you write "
                       "here.",
                 setapart_block=setapart("Provided draft to check:",
                                         "Recycling helps communities because it is beneficial.", "red"),
                 checklist_block=checklist(title="Run the judge check:", rows=[
                     ("Reason, not feeling?", "It uses \"because,\" so it looks like a reason."),
                     ("Specific and checkable?", "No. \"Beneficial\" just restates \"helps.\" There is nothing to verify."),
                     ("Circular?", "Yes. Replace it with a checkable reason, for example that it keeps reusable materials out of the landfill."),
                 ]),
                 closer="Now write one fresh sentence about recycling with a specific reason, then run the same "
                        "three questions on it: reason not feeling? specific and checkable? circular? If it is "
                        "circular, fix it, and finish by naming the specific reason you gave.")),

        # ===== INDEPENDENT: rewrite a weak twin with no frame + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Improve a weak draft on your own",
             ref="", bank="recycling", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="On your own now, no frame. Turn this weak twin into a strong one:",
                 setapart_block=setapart("Weak draft:", "Recycling programs are good because they help."),
                 closer="Rewrite it as one sentence that keeps the claim but gives a specific, checkable reason. "
                        "Before you submit, run the check: is the reason specific (something a reader could verify) "
                        "rather than circular? Fix it if not. Naming and giving a specific reason is what every "
                        "strong draft is built on, and you are ready to do it cold.")),

        # ===== TRANSFER: same strong/weak twin move, a NEW topic (weather forecasts), bank-partitioned =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: how weather forecasts work",
             ref="ACC-W910-INFO-LESSON-WEATHER", bank="weather",
             body=("The next weak draft is about weather forecasting. Read this new source so the topic is "
                   "familiar. Again, you are improving a single sentence by giving it a specific reason. The text "
                   "stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Improve a weak draft on a NEW topic",
             ref="", bank="weather", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="New topic, same move. Turn this weak twin into a strong one:",
                 setapart_block=setapart("Weak draft:", "Weather forecasts are useful because they are important."),
                 closer="Rewrite it as one sentence with a specific, checkable reason, for example that a warning "
                        "lets people prepare for a storm or flood before it arrives. Same replace-the-circular-"
                        "reason move as the recycling drafts, on a new topic.")),
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
