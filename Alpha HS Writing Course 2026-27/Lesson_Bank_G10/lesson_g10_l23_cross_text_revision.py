"""
lesson_g10_l23_cross_text_revision.py  -  G10 KC C.10.06, ARCHETYPE T5: RUBRIC-REVISION (CHECK, paragraph). V3.1.

G10 L23 (Unit 4, check), rebuilt to the v3.1 build spec (icm/_config/v3_1-lesson-build-spec.md), from the
pre-v3.1 lesson_g10_l23_cross_text_revision.py.
Teaching point (KEPT): find the synthesis-specific gaps in a PROVIDED cross-text draft (source-by-source;
unanswered counterclaim), predict its score, see the reveal, and revise, then run a faultless self-check on the
student's own cross-text writing. STATELESS-LEGAL revision model: work on PROVIDED anchors + a self-check on one
own submission, never a prior-draft look-back. KC C.10.06. Bound stimuli KEPT: ARG-OPP-LESSON-CONGESTION
(taught) -> ARG-OPP-LESSON-SCHOOLYEAR (transfer, bank-partitioned). rc.staar, unit="paragraph" (T5 ceiling).
CHECK=proposal.

V3.1 changes over the pre-v3.1 L23 (all prior gate failures fixed):
  1. TEACH is now ONE idea, hammered: a teal ONE_IDEA callout + the two synthesis gaps as a real <ul> list (was
     two prose teach cards). The check-predict-reveal-revise routine moved to the REMEMBER check tool at the
     model card (point of first use), not cold up front (KH load).
  2. NO leaked internal labels: the old discrimination prose said "a Grade-C design bet we label as a bet"
     (leaked_internal_label). Removed; the discrimination now uses explicit choices=[{id,text,correct,why}] with
     the correct option NOT the lone-longest, and a distractor carries the token 'answered' on a non-synthesis
     fix so the synthesis move, not a surface word, is the invariant (DI faultless communication).
  3. FRQ + diagnosis bodies built with frq_prompt / setapart / checklist (no "Step 1/2" prose, no "Scored on"
     chrome). The provided draft to revise sits in a setapart(...) block each time.
  4. self_score is a clean predict-the-score MCQ (short prompt + choices carrying the reveal), not a prose wall.
     "synthesize" and "counterclaim" defined with an "is a"/"means" cue in TEACH (define-before-use). Coping
     before/after kept (literal BEFORE + AFTER inline). Own words, no fabricated figures, no em dashes.
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
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Revising a cross-text draft is not tidying sentences. '
'It is finding the <strong>synthesis gap</strong> against the rubric and fixing <strong>exactly that gap</strong>.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: run it on any cross-text paragraph</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, ask these observable yes/no questions:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0"><strong>Woven?</strong> Are the sources connected on one shared claim, not listed in separate blocks?</li>'
'<li style="margin:2px 0"><strong>Counterclaim answered?</strong> Is the strongest objection the sources raise conceded and then answered?</li>'
'<li style="margin:2px 0"><strong>Attributed?</strong> Is each fact tied to the source it came from?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">Writers rate their own drafts higher than a scorer would, so run the check even when the paragraph feels finished.</div></div>')

# coping-model before/after panel: a source-by-source draft with an unanswered counterclaim, revised to close
# exactly those two synthesis gaps. No named person (stateless rule).
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> source-by-source, counterclaim not answered</span>'
    '<p style="margin:8px 0 0;font-size:15px">Source 1 says tolls cut traffic. Source 2 says tolls are unfair to '
    'some drivers. Tolls are a good idea.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">Two separate reports, then a bare claim. The sources '
    'are not woven and the fairness objection is never answered, the two synthesis gaps.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> woven on one claim, and the counterclaim answered</span>'
    '<p style="margin:8px 0 0;font-size:15px">Tolls are worth their cost: they cut traffic (Source 1). '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">WOVEN + ANSWERED</span> The fairness worry (Source 2) can be met by spending the toll '
    'money on transit for the very drivers who bear the charge.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">The revision weaves the two sources on one claim and '
    'answers the objection. Closing those two synthesis gaps is the revision.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1006-0023", grade="9-10", lesson_type=5,
    unit="G10 U4 - Cross-text synthesis (revise a provided draft + self-check your own)",
    title="Revise a Cross-Text Draft, Then Check Your Own",
    target=("Find the synthesis-specific gaps in a provided cross-text draft (source-by-source; unanswered "
            "counterclaim), predict its score, see the reveal, and revise, then run a faultless self-check on "
            "your own cross-text writing. Written at the paragraph. Trait: Development (use of sources)."),
    acc_tags=["ACC.W.SRC.1", "ACC.W.PROC.1", "CCSS.W.9-10.5", "CCSS.W.9-10.7"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.06", "sot": "icm course-G10.md L23",
                "taught_stimulus": "ACC-W910-ARG-OPP-LESSON-CONGESTION",
                "transfer_stimulus": "ACC-W910-ARG-OPP-LESSON-SCHOOLYEAR",
                "one_idea": "Revising a cross-text draft is finding the synthesis gap against the rubric and fixing exactly that gap.",
                "one_reminder": "Run the synthesis check: woven? counterclaim answered? attributed?",
                "playbook": "_phase2/playbook_T5_CHECK.md",
                "template": "locked L01 template; REVISION-TIER, provided draft; source set bound for context.",
                "version_note": ("V3.1 rebuild of the pre-v3.1 L23 to the v3.1 build spec. Fixed the prior gate "
                                 "failures: (a) TEACH is now one hammered idea (ONE_IDEA callout + the two "
                                 "synthesis gaps as a <ul>), the check-predict-reveal-revise routine moved to the "
                                 "REMEMBER check tool at point of first use (was two prose teach cards); (b) the "
                                 "discrimination dropped the leaked 'Grade-C design bet we label as a bet' prose "
                                 "and now uses explicit choices with the correct option NOT the lone-longest and "
                                 "an 'answered' distractor to break the token confound; (c) FRQ + diagnosis built "
                                 "with frq_prompt/setapart/checklist (no Step-N prose, no 'Scored on' chrome), "
                                 "provided draft in a setapart block; (d) self_score is a clean predict-the-score "
                                 "MCQ; 'synthesize' and 'counterclaim' defined with a cue in TEACH. Kept bound "
                                 "stimuli + every production unit='paragraph' (T5 ceiling)."),
                "council": ("T5/CHECK cross-text revision: the STATELESS-LEGAL revision model = revise a PROVIDED "
                            "cross-text draft (rD1 predict-the-fix + R1 revise-anchor + K1 predict-then-reveal) + "
                            "R3 self-check on ONE own fresh piece; NO prior-draft look-back. gaps-found-vs-missed "
                            "discrimination labeled Grade-C in code. CHECK=proposal; unit=paragraph."),
                "review_provenance": "built to the G9 L25 v3.1 pattern (icm/_config/v3_1-lesson-build-spec.md)."},
    fade_ledger_moves=["revise-cross-text-for-synthesis-gaps", "R3-self-check-cross-text"],
    slots=[
        # ===== TEACH: ONE idea, hammered (callout + the two synthesis gaps as a list; routine moved to model) =====
        Slot("TEACH", "teach_card", "The one idea: find the synthesis gap, fix exactly that",
             body=(ONE_IDEA +
                   "To synthesize means to combine sources into one argument. A counterclaim is a source's "
                   "strongest objection to your position. Cross-text drafts usually fail in two specific ways, "
                   "so a good revision checks for both:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Source-by-source</strong>: the sources sit in separate "
                   "blocks instead of being woven into one point; the fix is to connect them on a shared claim.</li>"
                   "<li style=\"margin:4px 0\"><strong>Unanswered counterclaim</strong>: the draft states a "
                   "position but never concedes and answers the strongest objection the sources raise; the fix "
                   "is to add that concede-and-answer move.</li></ul>"
                   "You cannot see your own gaps easily, so you will first practice on PROVIDED drafts: predict "
                   "the score, see the reveal, then revise. After that you run the same observable check on a "
                   "cross-text paragraph you write here.")),
        # tag="buy_in": this is a get-familiar source-orientation read (the drafts you revise combine this set),
        # not a load-bearing teach segment that needs an intervening check, so it counts 0 toward the
        # check-cadence run (LS-feedback #3). That keeps the pre-check run (teach card + worked example) within
        # the checking_revision ceiling of 2. No teaching is cut.
        Slot("TEACH", "stimulus_display", "Read the source set: congestion pricing (both sides)",
             ref="ACC-W910-ARG-OPP-LESSON-CONGESTION", bank="congestion_pricing", tag="buy_in",
             body=("The provided drafts you revise combine this two-source set on congestion pricing. Read it so "
                   "the material is familiar. You are not writing a congestion essay from scratch here; you are "
                   "finding and fixing synthesis gaps in drafts that are given to you. The texts stay on screen "
                   "while you work.")),

        # ===== MODEL (before the quiz): before/after worked example + the check tool at point of first use =====
        Slot("MODEL", "annotated_before_after", "Watch a cross-text draft get revised for the gaps",
             bank="congestion_pricing",
             body=("Here is the skill in action. Read the BEFORE, then the AFTER, and notice the two synthesis "
                   "gaps being closed." + BEFORE_AFTER_HTML +
                   " The BEFORE lists the sources and drops the objection; the AFTER weaves the sources on one "
                   "claim and answers the objection. Closing the synthesis gaps is the revision. " + REMEMBER +
                   "When you revise a cross-text paragraph, run this check, then reread once more.")),
        Slot("MODEL", "discrimination", "Which revision closed the synthesis gaps?",
             ref="", labeled_grade_c=True, bank="congestion_pricing",
             body=("Spot the target before you revise. A provided draft was source-by-source with an unanswered "
                   "counterclaim. Which revision CLOSED both synthesis gaps? "
                   "(A) The writer fixed the grammar and spelling, then made each source's own summary block "
                   "longer by adding extra detail to it.  "
                   "(B) The writer wove the two sources on one claim (tolls cut traffic; the money can fund "
                   "transit) and answered the fairness objection.  "
                   "(C) The writer added a bold closing line that answered the reader by restating the whole "
                   "position much more forcefully, and then chose to say the very same thing over once more.  "
                   "(D) The writer wove the two sources on one claim, but named the fairness objection only in "
                   "passing and never actually conceded or answered it.  "
                   "Correct: B."),
             choices=[
                 {"id": "A", "text": "The writer fixed the grammar and spelling, then made each source's own summary block longer by adding extra detail to it.",
                  "correct": False,
                  "why": "This polishes and pads each source's separate block, but the sources are still listed instead of woven and the objection is still unanswered, so both synthesis gaps remain."},
                 {"id": "B", "text": "The writer wove the two sources on one claim (tolls cut traffic; the money can fund transit) and answered the fairness objection.",
                  "correct": True,
                  "why": "Correct. This weaves the two sources on a shared claim and concedes then answers the objection, closing exactly the two synthesis gaps."},
                 {"id": "C", "text": "The writer added a bold closing line that answered the reader by restating the whole position much more forcefully, and then said the very same thing once more.",
                  "correct": False,
                  "why": "Restating the position louder does not close either gap. The sources are still in separate blocks and the real objection is still not conceded and answered. Notice 'answered' here sits on the reader, not on the counterclaim."},
                 {"id": "D", "text": "The writer wove the two sources on one claim, but named the fairness objection only in passing and never actually conceded or answered it.",
                  "correct": False,
                  "why": "This closes the source-by-source gap but not the counterclaim gap. Naming an objection is not answering it; you must concede the fairness point, then say why the claim still holds. One gap remains, so it does not close both."},
             ]),
        Slot("MODEL", "predict_the_fix", "Which synthesis gap does this draft have?",
             bank="congestion_pricing",
             body=("Predict before the reveal. A provided draft reads: 'Source 1 gives the traffic benefit. "
                   "Source 2 gives the cost concern. Tolls are worth it.' Which single revision most improves it? "
                   "(A) Weave the two sources on the shared claim and answer the cost concern, closing the "
                   "source-by-source and unanswered-counterclaim gaps.  "
                   "(B) Add a third source that also supports tolls, so the paragraph rests on more evidence and "
                   "covers even more of what the readings offer.  "
                   "(C) Restate 'tolls are worth it' in bolder wording and say it again at the end, so the "
                   "reader is left with no doubt about the writer's position.  "
                   "(D) Fix the punctuation and clean up any spelling slips, so the three sentences read more "
                   "smoothly and the paragraph looks more polished."),
             feedback=("Correct: A. The draft reports each source separately (source-by-source) and never "
                       "answers the cost concern (unanswered counterclaim), the two synthesis gaps. The fix "
                       "weaves the sources on the shared claim and answers the objection. A third source (B), "
                       "louder wording (C), or punctuation (D) close neither gap.")),

        # ===== SUPPORTED: predict the score (calibration MCQ) -> then revise the provided draft (frame+checklist) =====
        Slot("SUPPORTED", "self_score", "Predict the score, then see the real score",
             ref="", bank="congestion_pricing",
             body=("Predict, then reveal. A provided draft reads: 'Source 1 shows tolls reduce congestion. "
                   "Source 2 shows tolls cost drivers money. Congestion pricing is a good policy.' On a 2-point "
                   "synthesis scale (2 = sources woven AND counterclaim answered; 1 = a gap remains), what score "
                   "does this draft earn?"),
             choices=[
                 {"id": "1", "text": "1 out of 2", "correct": True,
                  "why": "Correct. The two sources are listed, not woven, and the cost objection is stated but "
                         "never answered, so a synthesis gap remains and that caps it at 1. A 2 would connect "
                         "the sources on one claim and concede then answer the objection."},
                 {"id": "2", "text": "2 out of 2", "correct": False,
                  "why": "A 2 needs the sources woven AND the counterclaim answered. This draft names both sides "
                         "but leaves them in separate blocks and never answers the cost objection. Notice how a "
                         "draft that names both sides can still leave both synthesis gaps open."},
             ]),
        Slot("SUPPORTED", "production_frq", "Revise the provided cross-text draft",
             ref="", bank="congestion_pricing", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="Revise the draft below to close both synthesis gaps. Keep the facts from each source; "
                       "weave them and answer the objection.",
                 setapart_block=setapart("Draft to revise:",
                                         "Source 1 says tolls cut traffic. Source 2 says tolls are unfair to some drivers. Tolls are a good idea."),
                 checklist_block=checklist(title="Use this check:", rows=[
                     "Weave the two sources on one shared claim, not in separate blocks.",
                     "Concede the fairness objection, then answer it (say why the claim still holds).",
                 ]),
                 closer="Rewrite the whole paragraph with the sources woven and the objection answered.")),
        # DIAGNOSIS: watch the check run on a provided draft, then run it on a fresh paragraph in this box
        # (stateless-safe; the material is provided, and the self-check is on the same item, not a prior submission).
        Slot("MODEL", "diagnosis_frq", "Self-check a fresh cross-text paragraph against the list",
             ref="", bank="congestion_pricing", scored=True,
             body=frq_prompt(
                 intro="First watch the check run on a provided draft, then run it on a fresh cross-text "
                       "paragraph you write here.",
                 setapart_block=setapart("Provided draft to check:",
                                         "Source A supports the plan. Source B opposes it. I support it.", "red"),
                 checklist_block=checklist(title="Run the synthesis check:", rows=[
                     ("Woven?", "No. Source A and Source B sit in separate sentences. Connect them on one claim."),
                     ("Counterclaim answered?", "No. Source B's objection is named but never answered. Concede it, then answer it."),
                     ("Attributed?", "Partly. The claim 'I support it' names no source fact. Tie each point to its source."),
                 ]),
                 closer="Now write a fresh cross-text paragraph on congestion pricing here, then run the same "
                        "three questions on it: woven? counterclaim answered? attributed? For each No, fix that "
                        "part, and finish by naming which gap you had to close.")),

        # ===== INDEPENDENT: revise a PROVIDED draft with no checklist scaffold + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Revise a provided cross-text draft on your own",
             ref="", bank="congestion_pricing", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="On your own now, no checklist. Revise the draft below to close both synthesis gaps.",
                 setapart_block=setapart("Draft to revise:",
                                         "The pro source lists benefits. The con source lists costs. Overall tolls help cities."),
                 closer="Weave the two sources on one claim and concede then answer the cost objection. Then "
                        "check your revision: woven? counterclaim answered? attributed? This is what every real "
                        "cross-text paragraph is built on, and you are ready to do it cold.")),

        # ===== TRANSFER: same close-the-gaps move, a NEW source set (longer school year), bank-partitioned =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source set: a longer school year (both sides)",
             ref="ACC-W910-ARG-OPP-LESSON-SCHOOLYEAR", bank="school_year",
             body=("The next provided draft to revise combines this new two-source set on a longer school year. "
                   "Read it so the material is familiar. Again, you are finding and closing the synthesis gaps "
                   "in a draft that is given to you, then self-checking your revision. The texts stay on screen "
                   "while you work.")),
        Slot("TRANSFER", "production_frq", "Revise a cross-text draft on a NEW set",
             ref="", bank="school_year", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="New set, same move. Revise the draft below to close both synthesis gaps.",
                 setapart_block=setapart("Draft to revise:",
                                         "Source 1 says a longer year closes learning gaps. Source 2 says it costs a lot. A longer year is worth it."),
                 closer="Weave the two sources on one claim and concede then answer the cost objection. Then "
                        "check your revision: woven? counterclaim answered? attributed? Same close-the-gaps "
                        "revision as the congestion draft, on a new topic.")),
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
