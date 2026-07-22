"""
lesson_g9_l25_essay_revision_v3_1.py  -  G9 KC C.9.04, ARCHETYPE T5: RUBRIC-REVISION (CHECK, paragraph). V3.1.

G9 L25, rebuilt to the v3.1 build spec (icm/_config/v3_1-lesson-build-spec.md), from lesson_g9_l25_essay_revision.py.
Teaching point (KEPT): find the specific gap in a PROVIDED essay paragraph, predict its score, see the reveal,
then revise it against the rubric, plus a faultless self-check on a fresh paragraph the student writes here. This
is the STATELESS-LEGAL revision model: work on PROVIDED anchors + a self-check on one own submission, never a
prior-draft look-back. KC C.9.04. Bound stimuli KEPT: FRAME-VOLCANOES (taught) -> FRAME-SCHOOLLUNCH (transfer,
bank-partitioned). rc.staar, unit="paragraph" (T5 ceiling is paragraph, so every scored revision is a
paragraph-level fix on the provided essay; whole-essay drafting was L23/L24). CHECK=proposal.

V3.1 changes over the current L25 (all prior gate failures fixed):
  1. TEACH is now ONE idea, hammered: a teal ONE_IDEA callout + the common gaps as a real <ul> list (was two
     prose teach cards). The predict-reveal-revise-self-check routine moved to the REMEMBER check tool at the
     model card (point of first use), not cold up front (KH load).
  2. NO leaked internal labels: the old discrimination prose said "a Grade-C design bet we label as a bet"
     (leaked_internal_label failed 3x). Removed; the discrimination now uses explicit choices=[{id,text,correct,
     why}] with the correct option NOT the lone-longest, and a distractor carries the token 'because' on a
     non-warrant so the warrant, not a surface word, is the invariant (DI faultless communication).
  3. FRQ + diagnosis bodies built with frq_prompt / setapart / checklist (no "Step 1/2" prose, no "Scored on"
     chrome). The provided paragraph to revise sits in a setapart(...) block each time.
  4. self_score is a clean predict-the-score MCQ (short prompt + choices carrying the reveal), not a 120-word
     prose block (which rendered as a wall-of-text checkpoint). "warrant" defined with an "is a" cue in TEACH
     (define-before-use). Coping before/after kept (literal BEFORE + AFTER inline). Own words, no fabricated
     figures, no em dashes.
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
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Revising is not rereading and hoping it sounds better. '
'It is finding the <strong>specific gap</strong> against the rubric and fixing <strong>exactly that gap</strong>.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: run the rubric on any paragraph</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit a paragraph, ask these observable yes/no questions:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0"><strong>Claim?</strong> Does one sentence take a clear position?</li>'
'<li style="margin:2px 0"><strong>Attributed evidence?</strong> Is a fact given, and is its source named?</li>'
'<li style="margin:2px 0"><strong>Warrant?</strong> Does a sentence say why that evidence supports the claim?</li>'
'<li style="margin:2px 0"><strong>Transitions?</strong> Do the links name the real relationship (for more than one paragraph)?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">Writers rate their own work higher than a scorer would, so run the check even when a paragraph feels finished.</div></div>')

# coping-model before/after panel: a body paragraph missing its warrant, revised to add exactly that warrant.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> a body paragraph missing its warrant</span>'
    '<p style="margin:8px 0 0;font-size:15px">Volcanoes are worth monitoring. The source explains that scientists '
    'track ground swelling and small quakes near active volcanoes.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">Claim and attributed evidence are here, but the '
    'paragraph never says WHY tracking those signs supports monitoring. The rubric caps a paragraph with no '
    'warrant.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> the same paragraph, revised to add the warrant</span>'
    '<p style="margin:8px 0 0;font-size:15px">Volcanoes are worth monitoring. The source explains that scientists '
    'track ground swelling and small quakes near active volcanoes. '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">ADDED WARRANT</span> These signs matter because they often appear before an eruption, '
      'so tracking them can warn a nearby town in time to act.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">The revision adds the missing warrant, the sentence '
    'that explains why the evidence supports the claim. Fixing the specific gap is the revision.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C904-0025", grade="9-10", lesson_type=5,
    unit="G9 U5 - Build essay (revise a provided essay + self-check your own)",
    title="Revise Against the Rubric, Then Check Your Own Essay",
    target=("Find the specific gap in a provided essay paragraph, predict its score, see the reveal, and revise "
            "it against the rubric, then run a faultless self-check on your own essay. Written at the "
            "paragraph. Trait: Development/Organization."),
    acc_tags=["ACC.W.PROC.2", "ACC.W.PROC.1", "CCSS.W.9-10.5"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-14",
                "mnemonic_status": "proposal", "kc": "C.9.04", "sot": "icm course-G9.md L25",
                "taught_stimulus": "ACC-W910-FRAME-VOLCANOES",
                "transfer_stimulus": "ACC-W910-FRAME-SCHOOLLUNCH",
                "one_idea": "Revising is finding the specific gap against the rubric and fixing exactly that gap.",
                "one_reminder": "Run the rubric check: claim? attributed evidence? warrant? transitions?",
                "playbook": "_phase2/playbook_T5_CHECK.md",
                "template": "locked L01 template; REVISION-TIER binds issue_frames (material is the provided anchor essay, inline).",
                "version_note": ("V3.1 rebuild of lesson_g9_l25_essay_revision.py to the v3.1 build spec. Fixed the "
                                 "prior gate failures: (a) TEACH is now one hammered idea (ONE_IDEA callout + the "
                                 "common gaps as a <ul>), the predict-reveal-revise-self-check routine moved to the "
                                 "REMEMBER check tool at point of first use (was two prose teach cards); (b) the "
                                 "discrimination dropped the leaked 'Grade-C design bet we label as a bet' prose and "
                                 "now uses explicit choices with the correct option NOT the lone-longest and a "
                                 "'because' distractor to break the token confound; (c) FRQ + diagnosis built with "
                                 "frq_prompt/setapart/checklist (no Step-N prose, no 'Scored on' chrome), provided "
                                 "paragraph in a setapart block; (d) self_score is a clean predict-the-score MCQ, not "
                                 "a wall-of-text prose block; 'warrant' defined with an 'is a' cue. Kept bound stimuli "
                                 "+ every production unit='paragraph' (T5 ceiling)."),
                "council": ("T5/CHECK essay-revision: the STATELESS-LEGAL revision model = revise a PROVIDED "
                            "anchor (rD1 predict-the-fix + R1 revise-anchor + K1 predict-then-reveal) + R3 self-"
                            "check on ONE own fresh piece; NO prior-draft look-back. gap-found-vs-missed "
                            "discrimination labeled Grade-C in code. CHECK=proposal; T5 ceiling paragraph, so "
                            "revision targets are paragraph-level (whole-essay drafting was L23/L24)."),
                "review_provenance": "built to the G9 L01 v3.1 pattern (icm/_config/v3_1-lesson-build-spec.md)."},
    fade_ledger_moves=["revise-provided-anchor-to-rubric", "R3-self-check-own-essay"],
    slots=[
        # ===== TEACH: ONE idea, hammered (callout + the common gaps as a list; routine moved to the model card) =====
        Slot("TEACH", "teach_card", "The one idea: find the specific gap, fix exactly that",
             body=(ONE_IDEA +
                   "The rubric rewards a complete paragraph: a claim, evidence, and a warrant. A warrant is a "
                   "sentence that explains why the evidence supports the claim. So revising means checking a "
                   "paragraph for a missing part and repairing exactly that part. Watch for these common gaps:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>No warrant</strong>: the paragraph stops at the evidence "
                   "and never says why that evidence supports the claim.</li>"
                   "<li style=\"margin:4px 0\"><strong>Unattributed evidence</strong>: a fact appears with no "
                   "source named.</li>"
                   "<li style=\"margin:4px 0\"><strong>A vague reference</strong>: a \"this\" or \"it\" that "
                   "points to no clear noun.</li>"
                   "<li style=\"margin:4px 0\"><strong>A filler transition</strong>: \"also\" where the real "
                   "relationship is a cause or a contrast.</li></ul>"
                   "You cannot see your own gaps easily, so you will first practice on PROVIDED paragraphs: "
                   "predict the score, see the reveal, then revise. After that you run the same observable "
                   "checklist on a paragraph you write here.")),
        # tag="buy_in": this is a get-familiar topic-orientation read (the provided paragraphs you revise are on
        # this topic), not a counted teach segment, so it does not tighten the checking_revision cadence ceiling.
        Slot("TEACH", "stimulus_display", "The topic: volcanoes",
             ref="ACC-W910-FRAME-VOLCANOES", bank="volcanoes", tag="buy_in",
             body=("The provided paragraphs you revise are about volcanoes. Read this short orientation so the "
                   "topic is familiar. You are not writing a volcano essay from scratch here; you are finding "
                   "and fixing gaps in paragraphs that are given to you.")),

        # ===== MODEL (before the quiz): before/after worked example + the check tool at point of first use =====
        Slot("MODEL", "annotated_before_after", "Watch a paragraph get revised to close its gap",
             bank="volcanoes",
             body=("Here is the skill in action. Read the BEFORE, then the AFTER, and notice the specific gap, "
                   "the missing warrant, being closed." + BEFORE_AFTER_HTML +
                   " The BEFORE stops at evidence; the AFTER adds the warrant that explains why the evidence "
                   "supports the claim. Closing the specific gap is the revision. " + REMEMBER +
                   "When you revise a paragraph, run this checklist, then reread once more.")),
        Slot("MODEL", "discrimination", "Which revision fixes the real gap?",
             ref="", labeled_grade_c=True, bank="volcanoes",
             body=("Spot the target before you revise. A provided paragraph has a claim and attributed evidence, "
                   "but no warrant, the sentence that says why the evidence supports the claim. Which revision "
                   "fixes that real gap? "
                   "(A) Add a second fact from the source about the small quakes, and also make every sentence "
                   "noticeably longer and more detailed.  "
                   "(B) Add a sentence explaining why the tracked signs support the claim that the volcano is "
                   "worth monitoring.  "
                   "(C) Restate the claim in bolder wording, because a stronger claim can make the whole "
                   "paragraph feel convincing.  "
                   "(D) Add a transition like 'therefore' between the two sentences so the paragraph flows more "
                   "smoothly. "
                   "Correct: B."),
             choices=[
                 {"id": "A", "text": "Add a second fact from the source about the small quakes, and also make every sentence noticeably longer and more detailed.",
                  "correct": False,
                  "why": "This adds length and one more fact, but it still never explains why the evidence supports the claim, so the real gap, the missing warrant, is still there."},
                 {"id": "B", "text": "Add a sentence explaining why the tracked signs support the claim that the volcano is worth monitoring.",
                  "correct": True,
                  "why": "Correct. The gap was a missing warrant, and this adds exactly that: a sentence saying why the tracked signs support the claim."},
                 {"id": "C", "text": "Restate the claim in bolder wording, because a stronger claim can make the whole paragraph feel convincing.",
                  "correct": False,
                  "why": "A bolder claim does not close the gap. The paragraph still never explains why the evidence supports the claim, so the warrant is still missing. Notice the word 'because' here sits on the claim, not on a warrant."},
                 {"id": "D", "text": "Add a transition like 'therefore' between the two sentences so the paragraph flows more smoothly.",
                  "correct": False,
                  "why": "A smoother link between the sentences is a cohesion fix, not the gap here. The paragraph still never says why the tracked signs support the claim, so the missing warrant is still missing."},
             ]),
        Slot("MODEL", "predict_the_fix", "What is the specific gap in this paragraph?",
             bank="volcanoes",
             body=("Predict before the reveal. A provided paragraph reads: 'Living near a volcano is risky. Ash "
                   "can bury homes and lava can destroy roads.' Which single revision closes its main gap? "
                   "(A) Attribute the dangers to a source and add a warrant explaining why they make living near "
                   "a volcano risky.  "
                   "(B) Add a third danger, such as choking gas, so the paragraph lists even more of the harms a "
                   "volcano can cause.  "
                   "(C) Rewrite the claim in stronger, more dramatic wording so the reader really feels how "
                   "frightening it would be.  "
                   "(D) Break the two long sentences into several shorter ones so the paragraph reads faster and "
                   "is easier to follow."),
             feedback=("Correct: A. The paragraph asserts a claim and lists dangers, but the dangers are not "
                       "attributed to a source and it never explains why they make the claim true (the warrant). "
                       "Attributing the evidence and adding the warrant is the fix. A third danger (B), more "
                       "dramatic wording (C), or shorter sentences (D) leave the real gaps in place.")),

        # ===== SUPPORTED: predict the score (calibration MCQ) -> then revise the SAME paragraph (frame + checklist) =====
        Slot("SUPPORTED", "self_score", "Predict the score, then see the real score",
             ref="", bank="volcanoes",
             body=("Predict, then reveal. A provided paragraph reads: 'An eruption can be dangerous. The source "
                   "explains that a volcano bursts out lava, ash, and gas.' On a 2-point rubric (2 = claim, "
                   "attributed evidence, and a warrant; 1 = a part is missing), what score does this paragraph "
                   "earn?"),
             choices=[
                 {"id": "1", "text": "1 out of 2", "correct": True,
                  "why": "Correct. It states a claim and gives attributed evidence, but it never says WHY lava, "
                         "ash, and gas make an eruption dangerous, so the warrant is missing and that caps it at 1. "
                         "A 2 would add the warrant (for example, because lava, ash, and gas can burn, bury, or "
                         "choke what lies near the volcano)."},
                 {"id": "2", "text": "2 out of 2", "correct": False,
                  "why": "A 2 needs the warrant too. This paragraph has a claim and attributed evidence, but it "
                         "never explains why lava, ash, and gas make an eruption dangerous. Notice how a paragraph "
                         "can look finished while missing the warrant."},
             ]),
        Slot("SUPPORTED", "production_frq", "Revise the provided paragraph",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="revision",
             body=frq_prompt(
                 intro="Revise the paragraph below to close its gap. Keep the claim and the attributed evidence; "
                       "add the missing warrant.",
                 setapart_block=setapart("Paragraph to revise:",
                                         "An eruption can be dangerous. The source explains that a volcano bursts out lava, ash, and gas."),
                 checklist_block=checklist(title="Use this check:", rows=[
                     "Keep the claim and the attributed evidence that are already there.",
                     "Add the warrant: one sentence saying WHY lava, ash, and gas make an eruption dangerous.",
                 ]),
                 closer="Rewrite the whole paragraph with the warrant added.")),
        # DIAGNOSIS: watch the check run on a provided paragraph, then run it on a fresh paragraph in this box
        # (stateless-safe; the material is provided, and the self-check is on the same item, not a prior submission).
        Slot("MODEL", "diagnosis_frq", "Self-check a fresh paragraph against the rubric list",
             ref="", bank="volcanoes", scored=True,
             body=frq_prompt(
                 intro="First watch the check run on a provided paragraph, then run it on a fresh paragraph you "
                       "write here.",
                 setapart_block=setapart("Provided paragraph to check:",
                                         "Monitoring volcanoes saves lives. It is a good idea.", "red"),
                 checklist_block=checklist(title="Run the rubric check:", rows=[
                     ("Claim?", "Yes. 'Monitoring volcanoes saves lives' takes a position."),
                     ("Attributed evidence?", "No. There is no source fact. Add one."),
                     ("Warrant?", "No. 'It is a good idea' is not a warrant. Add why the evidence supports the claim."),
                 ]),
                 closer="Now write a fresh body paragraph about volcanoes here, then run the same three questions "
                        "on it: claim? attributed evidence? warrant? For each No, fix that part, and finish by "
                        "naming which part you had to add.")),

        # ===== INDEPENDENT: revise a PROVIDED paragraph with no checklist scaffold + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Revise a provided paragraph and self-check your fix",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="revision",
             body=frq_prompt(
                 intro="On your own now, no checklist. Revise the paragraph below to close its gap.",
                 setapart_block=setapart("Paragraph to revise:",
                                         "Volcanoes can erupt with little warning. Some towns sit right at their base."),
                 closer="Attribute any fact to a source and add a warrant explaining why these points support a "
                        "clear claim (for example, that towns near volcanoes face real danger). Then check your "
                        "revision: claim? attributed evidence? warrant? Fixing the specific gap is the revision, "
                        "and you are ready to do it cold.")),

        # ===== TRANSFER: same find-and-fix-the-gap move, a NEW topic (free school meals), bank-partitioned =====
        Slot("TRANSFER", "stimulus_display", "The topic: free school meals",
             ref="ACC-W910-FRAME-SCHOOLLUNCH", bank="school_lunch",
             body=("The next provided paragraph to revise is about free school meals. Read this short "
                   "orientation so the topic is familiar. Again, you are finding and fixing a gap in a paragraph "
                   "that is given to you, then self-checking your revision.")),
        Slot("TRANSFER", "production_frq", "Revise a provided paragraph on a NEW topic",
             ref="", bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="revision",
             body=frq_prompt(
                 intro="New topic, same move. Revise the paragraph below to close its gap.",
                 setapart_block=setapart("Paragraph to revise:",
                                         "Free meals help students. Many schools offer them."),
                 closer="Attribute the evidence to a source and add a warrant explaining why it supports the "
                        "claim that free meals help students. Then check your revision: claim? attributed "
                        "evidence? warrant? Same find-and-fix-the-gap move as the volcano paragraphs, on a new "
                        "topic.")),
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
