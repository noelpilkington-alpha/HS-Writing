"""
lesson_g9_l25_essay_revision.py  -  G9 KC C.9.04, ARCHETYPE T5: RUBRIC-REVISION (CHECK, ceiling paragraph).

G9 course L25 (Unit 4, check). Essay-level revision, the STATELESS-LEGAL revision model: revise a PROVIDED
anchor essay against the rubric (rD1 predict-the-fix + R1 revise-anchor + K1 predict-then-reveal), then run an
R3 self-check on the student's ONE fresh essay. This is how "revise your own essay" is delivered inside
Timeback's statelessness: work on PROVIDED anchors + a faultless self-check on one own submission, never a
prior-draft look-back. Locked L01 template. REVISION-TIER binds issue_frames (the material is the provided
anchor essay, inline). Taught: FRAME-VOLCANOES -> transfer: FRAME-SCHOOLLUNCH (partitioned). rc.staar.
CHECK=proposal. NOTE: T5 ceiling is paragraph, so the scored REVISION targets are paragraph-level fixes on the
provided essay (unit="paragraph"); whole-essay drafting was L23/L24. No coping-model persona; no source markup;
no prior-work ref; no em dashes. Runs QC on execution.
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
    unit="G9 U4 - Build essay (revise a provided essay + self-check your own)",
    title="Revise Against the Rubric, Then Check Your Own Essay",
    target=("Find the specific gap in a provided essay paragraph, predict its score, see the reveal, and revise "
            "it against the rubric, then run a faultless self-check on your own essay. Written at the "
            "paragraph. Trait: Development/Organization."),
    acc_tags=["ACC.W.PROC.2", "ACC.W.PROC.1", "CCSS.W.9-10.5"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12",
                "mnemonic_status": "proposal", "kc": "C.9.04", "sot": "icm course-G9.md L25",
                "taught_stimulus": "ACC-W910-FRAME-VOLCANOES",
                "transfer_stimulus": "ACC-W910-FRAME-SCHOOLLUNCH",
                "playbook": "_phase2/playbook_T5_CHECK.md",
                "template": "locked L01 template; REVISION-TIER binds issue_frames (material is the provided anchor essay, inline).",
                "council": ("T5/CHECK essay-revision: the STATELESS-LEGAL revision model = revise a PROVIDED "
                            "anchor (rD1 predict-the-fix + R1 revise-anchor + K1 predict-then-reveal) + R3 self-"
                            "check on ONE own fresh piece; NO prior-draft look-back. gap-found-vs-missed "
                            "discrimination labeled Grade-C. CHECK=proposal; T5 ceiling paragraph, so revision "
                            "targets are paragraph-level (whole-essay drafting was L23/L24).")},
    fade_ledger_moves=["revise-provided-anchor-to-rubric", "R3-self-check-own-essay"],
    slots=[
        Slot("TEACH", "teach_card", "Revising means finding the specific gap and fixing it",
             body=("Revising is not rereading and hoping it sounds better; it is finding the specific gap "
                   "against the rubric and fixing that gap. The rubric rewards complete paragraphs (claim, "
                   "evidence, and a warrant that explains why the evidence supports the claim, cohered) inside "
                   "a planned essay. So revising means checking each paragraph for a missing part and repairing "
                   "it: add the warrant if it stops at evidence, attribute the evidence if the source is "
                   "missing, fix a filler transition, anchor a vague reference. Because you cannot see your own "
                   "gaps easily, you will first practice on PROVIDED essays: predict the score, see the reveal, "
                   "then revise. Then you will run a faultless self-check on your OWN essay, a list of "
                   "observable yes/no items, not a vague 'is it good?'. Goal today: find and fix the specific "
                   "gap in a provided paragraph, then self-check your own essay.")),
        Slot("TEACH", "teach_card", "How the check works: predict, reveal, revise, self-check",
             body=("Run this routine. First, read a provided paragraph and PREDICT its score against the "
                   "rubric. Second, see the REVEAL, the real score and the specific gap. Third, REVISE the "
                   "paragraph to close that gap. Fourth, turn the same list on your OWN essay as a self-check: "
                   "go paragraph by paragraph asking the observable questions (claim? attributed evidence? "
                   "warrant? transitions?). Predicting before the reveal trains your eye, because writers "
                   "usually rate their own work higher than a scorer would, so a specific checklist catches "
                   "what a quick reread misses.")),
        Slot("TEACH", "stimulus_display", "The topic: volcanoes",
             ref="ACC-W910-FRAME-VOLCANOES", bank="volcanoes",
             body=("The provided essay paragraphs you revise are about volcanoes. Read this short orientation "
                   "so the topic is familiar. You are not writing a volcano essay from scratch here; you are "
                   "finding and fixing gaps in paragraphs that are given to you.")),
        Slot("TEACH", "discrimination", "Which revision fixed the real gap?",
             ref="", labeled_grade_c=True, bank="volcanoes",
             body=("Sort before you revise (spotting the target first, a Grade-C design bet we label as a bet, "
                   "not a proven ingredient). A provided paragraph has a claim and attributed evidence but no "
                   "warrant. Which revision fixes the REAL gap? "
                   "(A) The writer makes each sentence longer and adds a second fact from the source about the small quakes.  "
                   "(B) The writer adds a sentence explaining WHY the evidence supports the claim (the missing "
                   "warrant). "
                   "Correct: B. The gap was a missing warrant, so (B) fixes exactly that. (A) adds length and "
                   "another fact but still never explains why the evidence supports the claim, so the real gap "
                   "remains. Fixing the specific gap is the revision.")),
        Slot("MODEL", "annotated_before_after", "Watch a paragraph get revised to close its gap",
             bank="volcanoes",
             body=("Here is a provided paragraph, missing its warrant, being revised to add exactly that. Read "
                   "the BEFORE, then the AFTER, and notice the specific gap being closed." + BEFORE_AFTER_HTML +
                   " The BEFORE stops at evidence. The AFTER adds the warrant that explains why the evidence "
                   "supports the claim. Closing the specific gap is the revision.")),
        Slot("MODEL", "predict_the_fix", "What is the specific gap in this paragraph?",
             bank="volcanoes",
             body=("Predict before the reveal. A provided paragraph reads: 'Living near a volcano is risky. "
                   "Ash can bury homes and lava can destroy roads.' Which single revision closes its main gap? "
                   "(A) attribute the evidence to a source and add a warrant explaining why these dangers "
                   "support the claim that living nearby is risky  "
                   "(B) add a third danger such as choking gas so the paragraph lists even more of the harmful "
                   "things a volcano can do to a nearby town  "
                   "(C) rewrite the claim in much stronger, more dramatic wording so a reader can really feel "
                   "how frightening living near a volcano is  "
                   "(D) break the two long sentences into several shorter ones so the paragraph reads faster "
                   "and is easier for a reader to get through"),
             feedback=("Correct: A. The paragraph asserts a claim and lists dangers, but the dangers are not "
                       "attributed to a source and it never explains why they make the claim true (the "
                       "warrant). The revision attributes the evidence and adds the warrant. A third danger "
                       "(B), a more dramatic claim (C), or shorter sentences (D) leave the real gaps, the "
                       "missing source and warrant, in place.")),
        Slot("SUPPORTED", "self_score", "Score a provided paragraph, then see the real score",
             ref="", bank="volcanoes",
             body=("Predict, then reveal. Provided paragraph: 'An eruption can be dangerous. The source "
                   "explains that a volcano bursts out lava, ash, and gas.' On a 2-point scale (2 = complete: "
                   "claim + attributed evidence + warrant; 1 = missing a part), what score would you give it? "
                   "Commit, then read the reveal. Reveal: this scores 1. It has a claim and attributed evidence "
                   "but no warrant, it never says why lava, ash, and gas make an eruption dangerous. A 2 would "
                   "add the warrant (for example, because lava, ash, and gas can burn, bury, or choke what lies "
                   "near the volcano). If you predicted 2, notice how a paragraph can look finished while "
                   "missing the warrant.")),
        Slot("SUPPORTED", "production_frq", "Revise the provided paragraph",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=("Revise this provided paragraph to close its gap: 'An eruption can be dangerous. The source "
                   "explains that a volcano bursts out lava, ash, and gas.' Add the missing WARRANT, a sentence "
                   "explaining WHY lava, ash, and gas make an eruption dangerous, keeping the claim and the "
                   "attributed evidence. Rewrite the paragraph. Scored on Development/Organization.")),
        Slot("MODEL", "diagnosis_frq", "Self-check a fresh paragraph against the rubric list",
             ref="", bank="volcanoes", scored=True,
             body=("First watch the check run on a provided paragraph, then run it on a fresh paragraph you "
                   "write here. Provided paragraph: 'Monitoring volcanoes saves lives. It is a good idea.' Run "
                   "the rubric check step by step. Claim? Yes. Attributed evidence? No, add a source fact. "
                   "Warrant? No, 'it is a good idea' is not a warrant, add why. Transitions? n/a for one "
                   "paragraph. Now you: write a fresh body paragraph about volcanoes here, then run the same "
                   "observable checklist on the paragraph you just wrote in this box: claim? attributed "
                   "evidence? warrant? For each No, fix that part. Finish by naming which part you had to "
                   "add.")),
        Slot("INDEPENDENT", "production_frq", "Revise a provided paragraph and self-check your fix",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=("On your own now. Revise this provided paragraph to close its gap: 'Volcanoes can erupt with "
                   "little warning. Some towns sit right at their base.' Add what the rubric rewards, attribute "
                   "any fact and add a warrant explaining why these points support a clear claim (for example, "
                   "that towns near volcanoes face real danger). Then run the checklist on your revision: "
                   "claim? attributed evidence? warrant? Fix any No before you submit. Scored on "
                   "Development/Organization.")),
        Slot("TRANSFER", "stimulus_display", "The topic: free school meals",
             ref="ACC-W910-FRAME-SCHOOLLUNCH", bank="school_lunch",
             body=("The next provided paragraph to revise is about free school meals. Read this short "
                   "orientation so the topic is familiar. Again, you are finding and fixing a gap in a paragraph "
                   "that is given to you, then self-checking your revision.")),
        Slot("TRANSFER", "production_frq", "Revise a provided paragraph on a NEW topic",
             ref="", bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=("New topic. Revise this provided paragraph to close its gap: 'Free meals help students. Many "
                   "schools offer them.' Attribute the evidence to a source and add a warrant explaining why it "
                   "supports the claim that free meals help students. Then run the checklist on your revision: "
                   "claim? attributed evidence? warrant? Same find-and-fix-the-gap move as the volcano "
                   "paragraphs, new topic. Scored on Development/Organization.")),
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
