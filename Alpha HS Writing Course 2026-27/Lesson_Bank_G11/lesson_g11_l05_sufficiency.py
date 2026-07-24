"""
lesson_g11_l05_sufficiency.py  -  G11 KC C.11.01, ARCHETYPE T5: RUBRIC-REVISION (CHECK, ceiling paragraph). V3.1.

G11 course L05 (Unit 1, check), rebuilt to the v3.1 build spec. Teaching point (KEPT): judge whether a claim
has ENOUGH reasoning to carry it (developed) or is an under-argued assertion (thin), predict the score, see the
reveal, then develop a thin claim so it is earned. Written at the paragraph. Trait: Evidence and Commentary.
KC C.11.01. Bound stimuli KEPT: ACC-W910-ARG-LESSON-AIWORKFORCE (taught) -> ACC-W910-ARG-LESSON-GRIDSPENDING
(transfer, bank-partitioned). rc.ap, unit="paragraph" (T5 ceiling). CHECK=proposal.

V3.1 changes over the prior L05 (all prior gate risks fixed):
  1. TEACH is now ONE idea, hammered: a teal ONE_IDEA callout + the developed-vs-thin signals as a real <ul>
     list (was two prose teach cards). The check/predict/reveal/develop routine moved to the REMEMBER check
     tool at the model card (point of first use), not cold up front (KH load).
  2. NO leaked internal labels: the old discrimination prose said "a Grade-C design bet we label as a bet"
     (leaked_internal_label). Removed; the discrimination now uses explicit choices=[{id,text,correct,why}]
     with the correct option NOT the lone-longest (the thin distractor is padded to match) and the token
     'because' carried on the THIN option too, so proportional reasoning, not a surface word, is the invariant.
  3. MODEL is a coping-model think-aloud: a writer's first try is thin, runs the check, catches the gap, and
     develops it, with a literal BEFORE and AFTER inline. FRQ + diagnosis bodies built with frq_prompt /
     setapart / checklist (no "Step 1/2" prose, no "Scored on" chrome); the weak draft sits in a setapart block.
  4. self_score is a clean predict-the-score MCQ (short prompt + choices carrying the reveal), not a prose wall.
     No technical term used without a plain-words definition first. Own words, no fabricated figures, no em dashes.
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
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A claim is only as strong as the reasoning under it. '
'A big claim needs reasoning <strong>proportional to its size</strong>, or it stays an assertion, not an '
'argument.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: is the claim earned?</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you commit to a paragraph, ask these three questions:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0"><strong>Size?</strong> How big is the claim, and how much would a fair reader need to believe it?</li>'
'<li style="margin:2px 0"><strong>Reasoning?</strong> Is there real reasoning under the claim, or just a restatement of it in confident words?</li>'
'<li style="margin:2px 0"><strong>Proportional?</strong> Does that reasoning actually carry a claim this size, or would a reader still ask "why should I believe that"?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">Writers feel their own claims are obvious, so run the check even when a claim already sounds settled.</div></div>')

# coping-model think-aloud: a writer drafts a thin claim, runs the check, catches the gap, and develops it.
# Literal BEFORE and AFTER inline (content_depth gate requires both words present).
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> first try: the claim is asserted, not earned</span>'
    '<p style="margin:8px 0 0;font-size:15px">The government should fund retraining for displaced workers. It '
    'is the right thing to do.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The writer runs the check: the claim is big (public '
    'money, a whole program), but the only support is "it is the right thing to do." That restates the claim '
    'in confident words; it does not reason for it. Caught it: this is thin.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> final: reasoning proportional to the claim</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">CLAIM + ENOUGH REASONING</span> The government should fund retraining for displaced '
      'workers, because the source shows private markets are slow to retrain a mid-career worker whose plant '
      'has closed, and a decade is too long to leave that sorting to chance while the fastest-growing work '
      'clusters in a few technical fields.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Now the claim is carried by reasoning that fits its '
    'size (why markets fall short; why the delay costs). The writer earned the claim instead of asserting it.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W1112-L-G11-C1101-0005", grade="9-10", lesson_type=5,
    unit="G11 U1 - Nuance (sufficiency check)",
    title="Earn the Claim: Enough Reasoning to Carry It",
    target=("Judge whether a claim has ENOUGH reasoning to carry it (developed) or is an under-argued "
            "assertion (thin), predict the score, see the reveal, then develop a thin claim so it is earned. "
            "Written at the paragraph. Trait: Evidence and Commentary (development)."),
    acc_tags=["ACC.W.ARG.2", "CCSS.W.11-12.1"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.01", "sot": "icm course-G11.md L05",
                "taught_stimulus": "ACC-W910-ARG-LESSON-AIWORKFORCE",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-GRIDSPENDING",
                "one_idea": "A claim is only as strong as the reasoning under it; a big claim needs reasoning proportional to its size.",
                "one_reminder": "Run the earn-the-claim check: size? reasoning? proportional?",
                "playbook": "_phase2/playbook_T5_CHECK.md",
                "template": "locked L01 template; EVIDENCE-TIER binds full sources. G11 register.",
                "version_note": ("V3.1 rebuild of the prose-wall L05 to the v3.1 build spec. Fixed prior gate "
                                 "risks: (a) TEACH is now one hammered idea (ONE_IDEA callout + developed-vs-thin "
                                 "signals as a <ul>), the check/predict/reveal/develop routine moved to the "
                                 "REMEMBER check tool at point of first use (was two prose teach cards); (b) the "
                                 "discrimination dropped the leaked 'Grade-C design bet we label as a bet' prose "
                                 "and now uses explicit choices with the correct option NOT the lone-longest and "
                                 "'because' carried on the thin option to break the token confound; (c) MODEL is a "
                                 "coping think-aloud (first try -> run check -> catch -> develop); (d) FRQ + "
                                 "diagnosis built with frq_prompt/setapart/checklist (no Step-N prose, no 'Scored "
                                 "on' chrome); (e) self_score is a clean predict-the-score MCQ. Kept id/type/kc/"
                                 "mnemonic_status/unit/bound stimuli + every production unit='paragraph' (T5 ceiling)."),
                "council": ("T5/CHECK G11 sufficiency: calibrate on developed-vs-thin (is the reasoning "
                            "proportional to the claim), then develop a thin claim. self_score calibration. "
                            "CHECK=proposal; T5 ceiling paragraph."),
                "review_provenance": "built to the G9 L25 v3.1 pattern (icm/_config/v3_1-lesson-build-spec.md)."},
    fade_ledger_moves=["sufficiency-developed-vs-thin", "earn-the-claim"],
    slots=[
        # ===== TEACH: ONE idea, hammered (callout + developed-vs-thin signals as a list; routine -> model card) =====
        Slot("TEACH", "teach_card", "The one idea: a claim is only as strong as the reasoning under it",
             body=(ONE_IDEA +
                   "Sufficiency is the match between a claim and the reasoning under it. A claim is DEVELOPED "
                   "when the reasoning is proportional to it, enough to make the claim believable. It is THIN "
                   "when a big claim rests on a bare assertion, so the claim is stated, not earned. Watch for "
                   "these signals:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Thin</strong>: the support just restates the claim in "
                   "confident words (\"it is the right thing to do\", \"that is how it works best\").</li>"
                   "<li style=\"margin:4px 0\"><strong>Thin</strong>: a big claim rests on one general reason "
                   "that would fit any claim (\"it helps people\").</li>"
                   "<li style=\"margin:4px 0\"><strong>Developed</strong>: the reasoning gives a specific WHY "
                   "that a fair reader could not have written without knowing the claim.</li>"
                   "<li style=\"margin:4px 0\"><strong>Developed</strong>: the reasoning fits the size of the "
                   "claim, so a skeptical reader stops asking \"why should I believe that?\"</li></ul>"
                   "A thin claim is not fixed by making it louder; it is fixed by adding the reasoning it needs. "
                   "Today you will judge whether provided claims are developed or thin, predict the score, see "
                   "the reveal, and develop a thin one.")),
        Slot("TEACH", "stimulus_display", "Read the source: government and the AI workforce",
             ref="ACC-W910-ARG-LESSON-AIWORKFORCE", bank="ai_workforce_policy", tag="buy_in",
             body=("Read this source on AI and the workforce so you have real reasons to draw on. The claims "
                   "you judge and develop are about this topic, and the source supplies the reasoning you can "
                   "add. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping think-aloud before/after + the check tool at point of first use =====
        Slot("MODEL", "annotated_before_after", "Watch a writer catch a thin claim and develop it",
             bank="ai_workforce_policy",
             body=("Here is the skill in action. A writer drafts a claim, runs the check, catches that it is "
                   "thin, and develops it. Read the BEFORE, then the AFTER, and notice the reasoning added to "
                   "earn the claim." + BEFORE_AFTER_HTML +
                   " The BEFORE asserts; the AFTER carries the claim with reasoning proportional to it. "
                   "Developing until the claim is earned is the fix. " + REMEMBER +
                   "Run this check on any claim before you commit to it.")),
        Slot("MODEL", "discrimination", "Which claim is developed, and which is thin?",
             ref="", labeled_grade_c=True, bank="ai_workforce_policy",
             body=("Sort these before you develop one. All four take the same side. Which one is DEVELOPED "
                   "(reasoning fits the claim), and which three are THIN (a bare assertion)? "
                   "(A) The government should fund retraining for displaced workers, because it is the right "
                   "thing to do, and because helping people who lost their jobs is simply what a decent, fair "
                   "country ought to do for the workers it counts on.  "
                   "(B) The government should fund retraining for displaced workers, because markets are slow to "
                   "retrain a mid-career worker whose plant has closed, and leaving that to chance wastes a "
                   "decade of a worker's earning years.  "
                   "(C) The government should fund retraining for displaced workers, because it helps people and "
                   "doing things that help people is a good use of public money.  "
                   "(D) The government clearly must fund retraining for displaced workers, because this is "
                   "obviously the correct and necessary policy for the country. "
                   "Correct: B is developed; A, C, and D are thin."),
             choices=[
                 {"id": "A", "text": "The government should fund retraining for displaced workers, because it is the right thing to do, and because helping people who lost their jobs is simply what a decent, fair country ought to do for the workers it counts on.",
                  "correct": False,
                  "why": "Thin. It is long and uses 'because' twice, but every clause just restates that "
                         "funding is right and fair. That is the claim in confident words, not reasoning that "
                         "carries it. A fair reader still asks 'why should the government be the one to do it?'"},
                 {"id": "B", "text": "The government should fund retraining for displaced workers, because markets are slow to retrain a mid-career worker whose plant has closed, and leaving that to chance wastes a decade of a worker's earning years.",
                  "correct": True,
                  "why": "Correct. This carries the claim with reasoning proportional to it: a specific WHY "
                         "(markets are slow to retrain mid-career workers) and what it costs (a decade of "
                         "earning years). The claim is earned, not just asserted."},
                 {"id": "C", "text": "The government should fund retraining for displaced workers, because it helps people and doing things that help people is a good use of public money.",
                  "correct": False,
                  "why": "Thin. 'It helps people' is a general reason that would fit almost any funding claim, so "
                         "it never says why THIS claim, about retraining displaced workers, is worth public "
                         "money. Reasoning that fits every claim carries none of them."},
                 {"id": "D", "text": "The government clearly must fund retraining for displaced workers, because this is obviously the correct and necessary policy for the country.",
                  "correct": False,
                  "why": "Thin. 'Clearly' and 'obviously' turn up the volume, but 'the correct and necessary "
                         "policy' just asserts the claim again. A thin claim is not fixed by making it louder; "
                         "it needs the reasoning that earns it."},
             ]),
        Slot("MODEL", "predict_the_fix", "Why does this claim score as thin?",
             bank="ai_workforce_policy",
             body=("Predict before the reveal. A writer drafts: 'The market should decide, not the government. "
                   "That is just how it works best.' Which judgment is correct? "
                   "(A) thin, because the claim rests on a bare assertion ('that is just how it works best') and "
                   "offers no reasoning that actually carries a claim this size  "
                   "(B) developed, because it takes a firm and clear side and leaves no doubt about where the "
                   "writer stands on who should do the deciding here  "
                   "(C) thin, but only because it is too short, since a longer restatement of the very same "
                   "idea would count as developed once it filled a bit more space  "
                   "(D) developed, because it names both the market and the government, which are the two rival "
                   "sides in the ongoing debate over who should decide how displaced workers get sorted"),
             feedback=("Correct: A. Taking a side (B) or naming the market and the government (D) is not the "
                       "same as arguing for the claim, and length (C) is not the issue. The claim is thin "
                       "because 'that is just how it works best' asserts rather than reasons. To develop it, add "
                       "WHY markets sort workers better than programs do (for example, that employers feel "
                       "shifts first and respond faster than a central plan can).")),

        # ===== SUPPORTED: predict the score (calibration MCQ) -> then develop a thin claim (frame + checklist) =====
        Slot("SUPPORTED", "self_score", "Predict the score, then see the real score",
             ref="", bank="ai_workforce_policy",
             body=("Predict, then reveal. A writer drafts: 'Retraining programs are worth funding because they "
                   "help people.' On a 2-point scale (2 = reasoning proportional to the claim; 1 = thin), what "
                   "score does this earn?"),
             choices=[
                 {"id": "1", "text": "1 out of 2", "correct": True,
                  "why": "Correct. 'They help people' is a general reason that would fit almost any funding "
                         "claim, so the claim is stated, not earned. A 2 would say HOW and WHY they help enough "
                         "to justify public money (for example, that markets retrain displaced mid-career "
                         "workers slowly). Notice how a 'because' clause can look like reasoning while only "
                         "restating the claim's appeal."},
                 {"id": "2", "text": "2 out of 2", "correct": False,
                  "why": "A 2 needs reasoning proportional to the claim. 'They help people' is a general "
                         "assertion, not a specific WHY that carries a claim about public funding. A confident "
                         "'because' clause can read as finished while the claim is still thin."},
             ]),
        Slot("SUPPORTED", "production_frq", "Develop the thin claim",
             ref="", bank="ai_workforce_policy", rubric_ref="rc.4trait", scored=True, unit="paragraph", frq_type="revision",
             body=frq_prompt(
                 intro="Develop the thin claim below so its reasoning is proportional to it. Keep the position; "
                       "add the reasoning that earns it.",
                 setapart_block=setapart("Thin claim to develop:",
                                         "The government should fund retraining for displaced workers. It is the right thing to do."),
                 checklist_block=checklist(title="Use this check:", rows=[
                     "Keep the position: the government should fund retraining for displaced workers.",
                     "Add reasoning from the source that fits the size of the claim (why markets fall short; why the delay costs).",
                     "Do not just make it louder; add the specific WHY a skeptical reader would need.",
                 ]),
                 closer="Rewrite the whole claim as a paragraph with proportional reasoning added.")),
        # COUNCIL FIX (2026-07-24): Option A (later-in-arc), watch-then-do: demo preserved, produce is the graded
        # act. The old diagnosis_frq bundled a watched earn-the-claim
        # demo (pre-answered (q,a) tuple rows) + a fresh develop + a run-and-name tail in one box (unscoreable,
        # wired to no grader, the (q,a) rows leaked the answers). The coping-model demo is PRESERVED as read-only
        # narration (the three sufficiency checks shown running on the provided draft, in plain declarative prose).
        # The student's ONLY graded act is now the fresh developed claim; the three checks sit read-only beneath as
        # plain-string reminders; the run-and-name tail is deleted. Kept as diagnosis_frq (paragraph grain needs an
        # own-draft diagnosis for model_sequence). Stays on the taught source (load balance).
        Slot("MODEL", "diagnosis_frq", "Develop a fresh claim so its reasoning is proportional",
             ref="", bank="ai_workforce_policy", rubric_ref="rc.4trait", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="First, watch the earn-the-claim check run on the provided draft below. Its claim is big: "
                       "it asks the government to do nothing at all in the job market. Its reason, that freedom is "
                       "important, is a slogan rather than a reason aimed at this claim, so it is not proportional: "
                       "a reader still asks why a hands-off approach actually serves workers. A stronger version "
                       "would add a specific WHY, for example that employers adapt faster than central plans. Now "
                       "write a fresh claim of your own that does not fall short that way.",
                 setapart_block=setapart("Provided draft the check was run on:",
                                         "The government should stay out of the job market because freedom is important.", "red"),
                 checklist_block=checklist(title="Check your claim against these (no need to type answers):", rows=[
                     "Size: how big is the claim, and how much reasoning would carry it?",
                     "Reasoning: is there a specific reason aimed at this claim, not a slogan?",
                     "Proportional: is the reasoning enough for the size of the claim?",
                 ]),
                 closer="Write a fresh claim about the government's role in the AI workforce and develop it into a "
                        "paragraph with proportional reasoning, drawing on the source. Run the three checks above "
                        "before you submit.")),

        # ===== INDEPENDENT: develop a claim with no frame + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Develop a claim on your own",
             ref="", bank="ai_workforce_policy", rubric_ref="rc.4trait", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now, no frame. Write a claim about the government's role in the AI workforce "
                       "and develop it with reasoning proportional to the claim, drawing on the source.",
                 closer="Before you submit, check it: size? reasoning? proportional? If the claim is thin, add "
                        "the reasoning it needs before you submit. Earning the claim with proportional reasoning "
                        "is what every real argument is built on, and you are ready to do it cold.")),

        # ===== TRANSFER: same earn-the-claim move, a NEW topic (grid spending), bank-partitioned =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: build the power, or build the grid",
             ref="ACC-W910-ARG-LESSON-GRIDSPENDING", bank="grid_investment_priority",
             body=("Read this new source on energy-spending priorities so you have real reasons to draw on. The "
                   "claim you develop is about this topic. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Develop a claim on a NEW topic",
             ref="", bank="grid_investment_priority", rubric_ref="rc.4trait", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="New topic, same move. Write a claim about energy-spending priorities (build clean "
                       "capacity first, or strengthen the grid first) and develop it with reasoning "
                       "proportional to the claim, drawing on the source.",
                 closer="Do not leave it thin: add the specific WHY a skeptical reader would need. Then check "
                        "it: size? reasoning? proportional? Same earn-the-claim move as the AI-workforce "
                        "paragraph, on a new topic.")),
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
