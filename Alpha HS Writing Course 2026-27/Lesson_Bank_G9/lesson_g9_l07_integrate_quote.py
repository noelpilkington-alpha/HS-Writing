"""
lesson_g9_l07_integrate_quote.py  -  G9 KC C.9.02, ARCHETYPE T3: EVIDENCE-INTEGRATION (PROVE, ceiling paragraph).

G9 course L07. Intro to evidence integration: quote vs paraphrase vs summary (G1) + attributed evidence (I1,
name who said it). Authored to the T3/PROVE playbook + 19-gate contract + the LOCKED L01 template (student
register, one teach concept/card, visual Timeback-safe before/after, ONE signature-error discrimination).
EVIDENCE-TIER: binds the FULL source (the student needs the actual quotable text), NOT an issue_frame.
  - KC: C.9.02 | unit: G9 U1 (evidence) | funnel: evidence | archetype: T3 (PROVE) | ceiling: paragraph
  - moves INTRODUCED: G1 quote/paraphrase/summary, I1 attributed-evidence
  - acc: [ACC.W.SRC.2] ccss: [W.9-10.1b, W.9-10.8] | rc.staar
  - taught: ACC-W910-ARG-LESSON-SCHOOLLUNCH (full) -> transfer: ACC-W910-INFO-LESSON-MIGRATION (full, partitioned)
PROVE = established-caveat (shipped K-8, unverified there; verify before reuse). App-owned sentence mechanics
(the appositive that forms an attributive tag, comma rules) are GATED, not re-taught; this lesson teaches the
rhetorical USE only. No near-peer coping model; no source markup; no prior-work reference; no em dashes.
Runs the QC harness on execution.
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
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> a dropped quote, no source named</span>'
    '<p style="margin:8px 0 0;font-size:15px">Free meals help students. "The program served more than 4.8 '
    'billion lunches." This shows meals matter.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The quote is just dropped in. The reader is never '
    'told WHO said it, so there is no reason to trust the number. A dropped quote caps the Evidence score.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> the same quote, attributed to its source</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">WHO</span> According to the U.S. Department of Agriculture, '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">EVIDENCE</span> the National School Lunch Program "served more than 4.8 billion '
      'lunches" in a recent year.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Naming the source, the U.S. Department of '
    'Agriculture, tells the reader where the number comes from and why to trust it. That is attributed '
    'evidence.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C902-0007", grade="9-10", lesson_type=3,
    unit="G9 U1 - Claim/controlling-idea + evidence (integrate a quote)",
    title="Name Your Source: No Quote Stands Alone",
    target=("Bring a source into your writing the right way: choose whether to quote, paraphrase, or "
            "summarize, and always name who said it so the reader can trust it. Written at the sentence. "
            "Trait: Evidence/Development."),
    acc_tags=["ACC.W.SRC.2", "CCSS.W.9-10.1b", "CCSS.W.9-10.8"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12",
                "mnemonic_status": "established-caveat",
                "kc": "C.9.02", "sot": "icm course-G9.md L07",
                "taught_stimulus": "ACC-W910-ARG-LESSON-SCHOOLLUNCH",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-MIGRATION",
                "playbook": "_phase2/playbook_T3_PROVE.md",
                "template": "locked L01 template (BRIEF_SPEC.md): student register, one teach concept, visual before/after, one discrimination. EVIDENCE-TIER binds full sources.",
                "council": ("T3/PROVE intro: define quote/paraphrase/summary + attributed evidence before use; "
                            "dropped-quote-to-attributed before/after (no near-peer coping model); predict-the-"
                            "fix with reveal; dropped-vs-attributed discrimination labeled Grade-C; frame then "
                            "PROVE self-check. Appositive/comma mechanics app-owned + gated, taught by USE only. "
                            "PROVE = established-caveat; SRSD live ES not claimed for async.")},
    fade_ledger_moves=["quote-vs-paraphrase-vs-summary", "attributed-evidence-name-the-source"],
    slots=[
        Slot("TEACH", "teach_card", "Three ways to bring in a source, and always name who said it",
             body=("When you use a source, you have three choices, and each has a job. A quote uses the "
                   "source's exact words in quotation marks, best when the wording itself matters. A paraphrase "
                   "puts one idea from the source into your own words, best when you want the fact but not the "
                   "exact phrasing. A summary is a short retelling of the source's main point in your own "
                   "words, best when you need the big picture briefly. Whichever you choose, one rule never "
                   "changes: name who said it. An attributive tag is a short phrase that names the source, like "
                   "'According to the U.S. Department of Agriculture,' or 'the researchers report.' Here is the "
                   "trap that costs the most Evidence points: dropping a quote or fact into your writing with "
                   "no source named. A reader has no reason to trust a number that seems to come from nowhere. "
                   "Goal today: bring in one piece of evidence and name its source.")),
        Slot("TEACH", "stimulus_display", "Read the source: free school meals",
             ref="ACC-W910-ARG-LESSON-SCHOOLLUNCH", bank="school_lunch",
             body=("Read this source about free school meals. Because your job is to USE its evidence, read the "
                   "whole thing and notice the specific facts and who they come from, the U.S. Department of "
                   "Agriculture and the National Center for Education Statistics. Pick one fact you could bring "
                   "into a piece of writing. The text stays on screen while you work.")),
        Slot("TEACH", "discrimination", "Which sentence names its source?",
             ref="", labeled_grade_c=True, bank="school_lunch",
             body=("Sort these before you write (we practice spotting the target before producing it, a "
                   "Grade-C design bet we label as a bet, not a proven ingredient). Both use the same fact from "
                   "the source. Which one brings it in the right way, by naming who said it? "
                   "(A) Tons of school lunches get handed out through this program every single year, and "
                   "the total is so huge you can tell the whole thing really matters.  "
                   "(B) According to the U.S. Department of Agriculture, the National School Lunch Program "
                   "served more than 4.8 billion lunches in a recent year. "
                   "Correct: B. (A) gestures at the fact but names no source and gives no real number, so a "
                   "reader cannot trust or check it. (B) names the source (the U.S. Department of Agriculture) "
                   "and gives the fact, so it is attributed evidence a reader can trust.")),
        Slot("MODEL", "annotated_before_after", "Watch a dropped quote get a source",
             bank="school_lunch",
             body=("Here is a dropped quote being fixed by naming its source. Read the BEFORE, then the AFTER, "
                   "and notice the one thing that was added: WHO said it." + BEFORE_AFTER_HTML +
                   " The BEFORE drops the number in with no source. The AFTER names the U.S. Department of "
                   "Agriculture, so the reader knows where the fact comes from. Naming the source is the "
                   "move.")),
        Slot("MODEL", "predict_the_fix", "What does this dropped quote most need?",
             bank="school_lunch",
             body=("Diagnose this draft before the reveal. A student wrote: 'Free meals are a good idea. \"The "
                   "program served more than 4.8 billion lunches.\" That is a lot.' Which single move would "
                   "most improve how the evidence is used? "
                   "(A) name the source of the quote with an attributive tag, so the reader knows who said it  "
                   "(B) add a second quote from the source right after the first one to pile on more evidence  "
                   "(C) make the sentences longer and add more detail so the paragraph feels fuller and complete  "
                   "(D) remove the quotation marks so the number blends smoothly into the writer's own sentence"),
             feedback=("Correct: A. The quote is dropped in with no source named, so a reader has no reason to "
                       "trust the number. The fix is an attributive tag that names who said it: 'According to "
                       "the U.S. Department of Agriculture, the program served more than 4.8 billion lunches.' "
                       "A second quote (B) or longer sentences (C) do not fix the missing source; removing the "
                       "quotation marks (D) would make it worse by hiding that these are the source's words.")),
        Slot("SUPPORTED", "production_frq", "Bring in a fact and name its source",
             ref="", bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("Use this frame to bring one fact from the source into a sentence: 'According to ______ "
                   "[name the source], ______ [the fact, quoted or paraphrased].' Goal: name the source with an "
                   "attributive tag, and bring in one real fact from the reading (quote the exact words or "
                   "paraphrase them). Do not drop the fact in with no source. Write one sentence. Scored on "
                   "Evidence/Development.")),
        Slot("MODEL", "diagnosis_frq", "Check your evidence: is the source named?",
             ref="", bank="school_lunch", scored=True,
             body=("First watch the check run on a weak draft, then run it on a fresh sentence of your own. "
                   "Weak draft: '\"Free or reduced-price meals reach students under 185 percent of the poverty "
                   "line.\" This helps a lot of families.' Run the check step by step. Step 1, source named? "
                   "No, the fact is dropped in with no attributive tag, so add one (who reported it?). Step 2, "
                   "real fact from the source? Yes, the 185 percent figure is in the reading. Step 3, quote or "
                   "paraphrase clear? The quotation marks are there, so it reads as a quote. Now you: write one "
                   "fresh sentence that brings in a fact from the source, then run the same checks. For each "
                   "No, use the fix: add an attributive tag naming the source; make sure the fact is really in "
                   "the reading. Finish by naming which check your sentence still needs most.")),
        Slot("INDEPENDENT", "production_frq", "Bring in evidence and name its source, on your own",
             ref="", bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("On your own now. Bring one fact from the free-meals source into a sentence, and name its "
                   "source. Goal: an attributive tag that names who said it, plus a real fact from the reading "
                   "(quoted or paraphrased). Before you submit, check your sentence: did I name the source, is "
                   "the fact really in the reading, is it clear whether I quoted or paraphrased? If any answer "
                   "is no, fix it before you submit. Do not drop the fact in with no source. Scored on "
                   "Evidence/Development.")),
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: animal migration",
             ref="ACC-W910-INFO-LESSON-MIGRATION", bank="animal_migration",
             body=("Read this new source about animal migration. Because your job is to USE its evidence, read "
                   "the whole thing and notice the specific facts and who reports them. Pick one fact you could "
                   "bring into a sentence. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Bring in evidence and name its source (NEW topic)",
             ref="", bank="animal_migration", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("New topic. Bring one fact from the migration source into a sentence, and name its source "
                   "with an attributive tag. Goal: name who said it, plus a real fact from the reading (quoted "
                   "or paraphrased). Same move as the meals sentence, new topic. Do not drop the fact in with "
                   "no source. Scored on Evidence/Development.")),
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
