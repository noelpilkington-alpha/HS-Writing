"""
lesson_g11_l10_assess_credibility.py  -  G11 KC C.11.08, ARCHETYPE T3: SOURCE EVALUATION (PROVE, sentence).

G11 course L10 (Unit 3 source evaluation, intro). Rebuilt to the v3.1 build spec (hand-authored to the L01/G9
v3.1 pattern). Teaching point (kept): assess a source's credibility on GROUNDS, who produced it and whether its
claims are backed, rather than trusting it because it sounds official. Written at the sentence. KC C.11.08.
Binds full info sources: energy_transition (taught) -> water_infrastructure (transfer). PROVE=established-caveat.
v3.1 spine: ONE_IDEA teal callout + list teach, coping-model think-aloud (First/Second/Final + BEFORE/AFTER),
REMEMBER dashed 3-question check tool, explicit-choices discrimination, deterministic FRQ prompts. 23 gates.
No coping-model persona; no source markup; no prior-work ref; no em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Judge a source on <strong>grounds</strong>, not by feel. '
'Grounds are the two checkable reasons behind the verdict: <strong>who</strong> produced the source and whether its '
'claims are <strong>backed</strong>.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit a credibility judgment, run these three:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0"><strong>Who?</strong> Did I name the author or organization that produced it?</li>'
'<li style="margin:2px 0"><strong>Backed?</strong> Did I point to data or evidence a reader could check?</li>'
'<li style="margin:2px 0"><strong>Feel?</strong> Am I really resting on tone (sounds official)? If so, replace it with who plus backing.</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">Two Yes and no Feel: the verdict rests on grounds.</div></div>')

COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer judging the electricity-mix source, checking the work along the way:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "This source is reliable because it sounds official and '
    'confident." I run the check. Who produced it? I did not say. Backed? I did not say. Feel? Yes, "sounds official" '
    'is tone. This rests on feel.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "This source is credible because it comes from the U.S. '
    'Energy Information Administration." Better, now it names WHO. But I still have not said whether the claims can be '
    'checked, so a reader has to take the producer on trust.</p>'
    '<p style="margin:0"><strong>Final:</strong> "This source is credible on the U.S. electricity mix because it comes '
    'from the U.S. Energy Information Administration and reports figures that can be checked against public federal '
    'data." Now WHO and BACKED are both named. The verdict rests on grounds.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> Trusts by feel: "sounds official and confident" is tone, not a '
    'ground the reader can check.</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> Credible on grounds: names the producer (a federal energy agency) '
    'and checkable backing (public federal data).</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1108-0010", grade="9-10", lesson_type=3,
    unit="G11 U3 - Source evaluation (assess credibility)",
    title="Judge a Source on Grounds, Not by Feel",
    target=("Assess a source's credibility on grounds, who produced it and whether its claims are backed, "
            "rather than trusting it because it sounds official. Written at the sentence. Trait: Evidence "
            "(source evaluation)."),
    acc_tags=["ACC.W.INQ.1", "CCSS.W.11-12.8"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "established-caveat", "kc": "C.11.08", "sot": "icm course-G11.md L10",
                "taught_stimulus": "ACC-W910-INFO-LESSON-ENERGYMIX",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-WATERUSE",
                "one_idea": "Judge a source on grounds (who produced it + whether backed), not by feel/tone.",
                "one_reminder": "Run the 3 questions: Who? Backed? Feel? Two Yes and no Feel = rests on grounds.",
                "playbook": "_phase2/playbook_T3_PROVE.md",
                "template": "locked L01 template; binds full info sources.",
                "version_note": ("V3.1 rebuild (hand-authored to the L01/G9 v3.1 pattern). Replaced prose-wall body "
                                 "with the v3.1 spine: ONE_IDEA teal callout + list teach, coping-model think-aloud "
                                 "(First/Second/Final + literal BEFORE/AFTER), REMEMBER dashed 3-question check tool, "
                                 "explicit-choices discrimination (reveal in tail/feedback), deterministic FRQ "
                                 "prompts. SENTENCE unit throughout (T3 ceiling paragraph). Kept id/type/KC/unit/"
                                 "bound stimuli/teaching point."),
                "council": ("T3/PROVE G11 source-eval intro: introduces assess-credibility (grounds: who + backing, "
                            "not feel). credible-on-grounds-vs-trusted-by-feel discrimination, labeled internally. "
                            "PROVE=established-caveat.")},
    fade_ledger_moves=["assess-credibility", "grounds-not-feel"],
    slots=[
        Slot("TEACH", "teach_card", "The one idea: grounds, not feel",
             body=(ONE_IDEA +
                   "At the college level you do not just use sources; you judge them. Assessing credibility means "
                   "deciding whether a source can be trusted, and doing it on grounds you can point to:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Who produced it</strong>: the author or organization behind "
                   "it, and their expertise or stake. A federal statistics agency is a different kind of source than "
                   "an anonymous page.</li>"
                   "<li style=\"margin:4px 0\"><strong>Whether the claims are backed</strong>: data, figures, or "
                   "cited evidence a reader could actually check.</li></ul>"
                   "The trap is trust-by-feel: mistaking a confident, official tone for reliability. Tone is a "
                   "feeling, not a ground. The test is simple: could you point to WHO said it and WHAT backs it?")),
        Slot("TEACH", "stimulus_display", "Read the source: the U.S. electricity mix",
             ref="ACC-W910-INFO-LESSON-ENERGYMIX", bank="energy_transition",
             body=("Read this source on the U.S. electricity mix. Because your job is to assess credibility, note "
                   "who produced its figures (the U.S. Energy Information Administration) and whether they are the "
                   "kind of claims a reader could check. The text stays on screen while you work.")),
        Slot("MODEL", "annotated_before_after", "Watch a feel-based judgment become grounds-based",
             bank="energy_transition",
             body=("Here is the skill in action. Follow the writer take a trust-by-feel judgment and rebuild it on "
                   "grounds, checking the work at each step. " + COPING_HTML +
                   " Notice the shift: the BEFORE rests on tone; the AFTER names the producer and the checkable "
                   "backing. Judging on grounds is the move." + REMEMBER +
                   "When you write your own judgment, name who plus backing, then run the 3 questions.")),
        Slot("MODEL", "discrimination", "Which judgment rests on grounds?",
             ref="", labeled_grade_c=True, bank="energy_transition",
             body=("Spot the target before you write it. Which judgment rests on GROUNDS, and which rest on FEEL? "
                   "(A) The source is credible because its confident, professional tone reads exactly the way a "
                   "knowledgeable expert would sound to a careful reader.  "
                   "(B) The source is credible on the electricity mix because it comes from the U.S. Energy "
                   "Information Administration and reports checkable figures.  "
                   "(C) The source is trustworthy because it is long and detailed and cites a great many numbers, "
                   "which surely shows careful research stands behind it.  "
                   "(D) The source is credible because it is the top result in a search and many other websites "
                   "link to it, so that many people relying on it must mean it is right. "
                   "Correct: B rests on grounds; A, C, and D rest on feel."),
             choices=[
                 {"id": "A", "text": "The source is credible because its confident, professional tone reads exactly the way a knowledgeable expert would sound to a careful reader.",
                  "correct": False,
                  "why": "This rests on feel. 'Confident, professional tone' and 'sounds like an expert' are surface impressions, not a producer you can name or backing you can check."},
                 {"id": "B", "text": "The source is credible on the electricity mix because it comes from the U.S. Energy Information Administration and reports checkable figures.",
                  "correct": True,
                  "why": "Correct. It rests on grounds: it names WHO produced it (a federal energy agency) and points to BACKING a reader could check (verifiable figures), rather than to tone."},
                 {"id": "C", "text": "The source is trustworthy because it is long and detailed and cites a great many numbers, which surely shows careful research stands behind it.",
                  "correct": False,
                  "why": "This rests on feel too. Length and a pile of numbers are surface cues; they do not name who produced the source or show the claims can actually be checked."},
                 {"id": "D", "text": "The source is credible because it is the top result in a search and many other websites link to it, so that many people relying on it must mean it is right.",
                  "correct": False,
                  "why": "This rests on feel too. Ranking high and being widely linked is a popularity cue; it names neither who produced the source nor backing a reader could check."},
             ]),
        Slot("MODEL", "discrimination", "Which judgment names both grounds?",
             ref="", labeled_grade_c=True, bank="energy_transition",
             body=("One more pair, a closer call. Each judgment below names something real about the source. "
                   "Which one rests on GROUNDS by naming BOTH who produced it and backing a reader can check? "
                   "(A) The source is credible because the U.S. Energy Information Administration produced it and "
                   "lists the survey data behind each reported figure.  "
                   "(B) The source is credible because a well-respected federal agency produced it, and an agency "
                   "with that kind of reputation would surely never publish any figure that a reader would actually "
                   "need to double-check.  "
                   "(C) The source is credible because its figures come from studies, so the numbers behind them "
                   "can be trusted.  "
                   "(D) The source is credible because an expert clearly wrote it and it lists the survey data "
                   "behind each reported figure. "
                   "Correct: A names who plus checkable backing; B, C, and D each fall short on one ground."),
             choices=[
                 {"id": "A", "text": "The source is credible because the U.S. Energy Information Administration produced it and lists the survey data behind each reported figure.",
                  "correct": True,
                  "why": "Correct. It names who produced it (a federal energy agency) and points to backing a reader could check (the survey data behind each figure), so both grounds are present."},
                 {"id": "B", "text": "The source is credible because a well-respected federal agency produced it, and an agency with that kind of reputation would surely never publish any figure that a reader would actually need to double-check.",
                  "correct": False,
                  "why": "This names who produced it but leans on the agency's reputation instead of backing a reader can check, so only one ground is there."},
                 {"id": "C", "text": "The source is credible because its figures come from studies, so the numbers behind them can be trusted.",
                  "correct": False,
                  "why": "This gestures at studies but names no identifiable producer, so the who behind the claims is missing."},
                 {"id": "D", "text": "The source is credible because an expert clearly wrote it and it lists the survey data behind each reported figure.",
                  "correct": False,
                  "why": "This points to checkable backing (the survey data), but 'an expert' is not an identifiable producer a reader could point to, so the WHO ground is only gestured at, not named."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this credibility judgment most need?",
             bank="energy_transition",
             body=("Diagnose this draft before the reveal. A student wrote: 'I trust this source because it uses a "
                   "lot of big numbers and sounds like an expert wrote it.' Which single move would most improve it? "
                   "(A) Tie the judgment to grounds by naming who produced the source and whether its claims are "
                   "backed, not to its tone or numbers.  "
                   "(B) Count how many statistics and figures the source uses, since a piece that is full of specific "
                   "numbers is clearly backed by solid data.  "
                   "(C) Rewrite the judgment to stress how official, confident, and professional the source's overall "
                   "writing style sounds to the reader.  "
                   "(D) Trust the source because it is long and detailed, since a longer and fuller piece of writing "
                   "must have more evidence behind it."),
             feedback=("Correct: A. Big numbers and an expert tone are surface cues, not grounds. The fix names WHO "
                       "produced it and WHAT backs the claims (for example, a federal agency reporting verifiable "
                       "data). Counting numbers (B), stressing tone (C), and trusting length (D) are all "
                       "trust-by-feel.")),
        Slot("SUPPORTED", "production_frq", "Warm up: fill in the grounds",
             ref="", bank="energy_transition", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="Warm up with the frame. Fill both blanks so the verdict rests on grounds, not feel:",
                 setapart_block=setapart("Copy and complete this frame:",
                                         "This source is credible on ______ [what claim] because ______ [who produced it AND how the claims are backed]."),
                 closer="Write ONE sentence. The 'because' half must name WHO produced it and WHAT a reader could "
                        "check, not how official it sounds.")),
        Slot("MODEL", "diagnosis_frq", "Check a weak judgment, then write a clean one",
             ref="", bank="energy_transition", scored=True,
             body=frq_prompt(
                 intro="Run the 3-question check on this weak judgment, then write a fresh one of your own.",
                 setapart_block=setapart("Weak judgment to check:",
                                         "This source is reliable because it seems professional.", "red"),
                 checklist_block=checklist(title="Run the 3 questions:", rows=[
                     ("Who: is the producer named?", "No. Add who produced it (for example, the federal agency)."),
                     ("Backed: is checkable evidence named?", "No. Add what a reader could check."),
                     ("Feel: does it rest on tone?", "Yes, 'seems professional' is tone. Replace it with who plus backing."),
                 ]),
                 closer="Now write ONE fresh grounds-based credibility judgment about the electricity-mix source, "
                        "then name which of the three questions your version fixes.")),
        Slot("INDEPENDENT", "production_frq", "Assess credibility on your own",
             ref="", bank="energy_transition", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now, no frame. Write ONE credibility judgment about the electricity-mix source "
                       "that rests on grounds: name who produced it and how its claims are backed.",
                 closer="Judging a source on grounds is what every real piece of college-level source work is built "
                        "on, and you are ready to do it cold. Run the 3 questions (Who? Backed? Feel?) before you "
                        "submit.")),
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: U.S. water use",
             ref="ACC-W910-INFO-LESSON-WATERUSE", bank="water_infrastructure",
             body=("A new source. Read this passage on how the United States uses its water. Same job: note who "
                   "produced its figures (the U.S. Geological Survey) and whether they can be checked. The text "
                   "stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Assess credibility on a NEW source",
             ref="", bank="water_infrastructure", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="New source, same move. Write ONE credibility judgment about the water-use source that rests "
                       "on grounds: name who produced it and how its claims are backed.",
                 closer="Grounds, not feel, exactly as you did on the electricity source. Run the 3 questions before "
                        "you submit.")),
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
