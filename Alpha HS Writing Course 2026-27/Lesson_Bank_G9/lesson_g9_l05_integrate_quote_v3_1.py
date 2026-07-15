"""
lesson_g9_l07_integrate_quote_v3_1.py  -  G9 KC C.9.02, ARCHETYPE T3: EVIDENCE-INTEGRATION (PROVE, paragraph
ceiling). V3.1 rebuild of lesson_g9_l07_integrate_quote.py.

V3.1 (Noel 2026-07-14): applies the L01 v3.1 pattern (icm/_config/v3_1-lesson-build-spec.md) to this
evidence-integration lesson. Same teaching point + lesson id + bound sources; the DELIVERY is rebuilt:
  1. ONE_IDEA teal callout states the single core idea (bring a source in + name who said it).
  2. TEACH is a LIST (quote / paraphrase / summary as <li> items), not the old 162-word wall of prose that
     tripped format_fidelity. The attributive-tag term is defined in plain words here (define-before-use).
  3. MODEL is a COPING-MODEL think-aloud (SRSD): a writer drops a quote, runs the check, catches the missing
     source, and revises, draft by draft. Still contains literal BEFORE and AFTER (content_depth). No near-peer.
  4. The 3-question check tool is folded into the model card as a real <ol>, at the POINT OF FIRST USE (KH
     load), not cold in step 1.
  5. DISCRIMINATION moved AFTER the model (KH: worked example before the quiz), with explicit per-option
     choices=[{id,text,correct,why}] for reliable per-choice feedback. Construct-confound broken: a distractor
     ("Experts say ...") carries attribution FLAVOR but names no checkable source, so the invariant the student
     must track is "names a specific source," not any single attribution word (DI faultless communication).
  6. DIAGNOSIS rebuilt with frq_prompt + setapart(weak draft, red) + checklist rows (no hand-written "Step 1 /
     Step 2" prose, which double-numbered in the render).
  7. AUTONOMY + say-the-standard on the independent write (Yeager).
  8. Removed the leaked "Grade-C design bet" label from the student-facing discrimination text.

ONE IDEA: bring a source into your writing by choosing to QUOTE, PARAPHRASE, or SUMMARIZE it, and always NAME
who said it. ONE REMINDER: the 3-question test. Passes all 23 lesson_contract gates + gated_reading render-QC.
EVIDENCE-TIER: binds the FULL sources (the student needs real quotable text), not issue_frames. Own words, no
fabricated figures, no em dashes. App-owned sentence mechanics (the appositive/comma rules inside an
attributive tag) stay gated, not re-taught; this lesson teaches the rhetorical USE only.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Bring a source into your writing by choosing to '
'<strong>QUOTE</strong>, <strong>PARAPHRASE</strong>, or <strong>SUMMARIZE</strong> it, and always '
'<strong>NAME</strong> who said it. A fact dropped in with no source gives the reader no reason to trust it.</div></div>')

# the reusable check tool, folded into the MODEL card at point of first use, as a real <ol>.
REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit a sentence that uses a source, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Did I name who said it?</li>'
'<li style="margin:2px 0">Did I choose to quote, paraphrase, or summarize on purpose?</li>'
'<li style="margin:2px 0">Is the fact really in the source?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, the evidence is not ready yet.</div></div>')

# coping-model think-aloud: a WRITTEN drafting process (drop the quote -> run the check -> catch the missing
# source -> revise), then the BEFORE/AFTER endpoints.
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer thinking it through, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Free meals help a lot of students. \'The program '
    'served more than 4.8 billion lunches.\' That number is huge." Check it: did I name who said it? No. The '
    'reader has no idea where that number came from, so there is no reason to trust it. Fix it.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "According to the U.S. Department of Agriculture, '
    'the National School Lunch Program \'served more than 4.8 billion lunches\' in a recent year." Better. Did '
    'I name who said it? Yes. Did I choose how to bring it in? Yes, I quoted the exact words because the number '
    'itself matters.</p>'
    '<p style="margin:0"><strong>Final:</strong> same sentence. It names the source and keeps the exact figure '
    'in quotation marks. Now the reader knows where the fact comes from and can check it. That passes.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "The program served more than 4.8 billion lunches." (a dropped '
    'quote, no source named)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> According to the U.S. Department of Agriculture, the National '
    'School Lunch Program "served more than 4.8 billion lunches" in a recent year. (attributed evidence)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C902-0007", grade="9-10", lesson_type=3,
    unit="G9 U1 - Claim/controlling-idea + evidence (integrate a quote)",
    title="Name Your Source: No Quote Stands Alone",
    target=("Bring a source into your writing the right way: choose whether to quote, paraphrase, or "
            "summarize, and always name who said it so the reader can trust it. Written at the sentence. "
            "Trait: Evidence/Development."),
    acc_tags=["ACC.W.SRC.2", "CCSS.W.9-10.1b", "CCSS.W.9-10.8"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "established-caveat",
                "kc": "C.9.02", "sot": "icm course-G9.md L07",
                "taught_stimulus": "ACC-W910-ARG-LESSON-SCHOOLLUNCH",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-MIGRATION",
                "one_idea": "Bring a source in by quoting, paraphrasing, or summarizing, and always name who said it.",
                "one_reminder": "3-question test: named the source? chose quote/paraphrase/summary on purpose? fact really in the source?",
                "version_note": ("V3.1: rebuilt to the L01 v3.1 pattern - ONE_IDEA callout; TEACH as a list "
                                 "(quote/paraphrase/summary), not the old 162-word wall; coping-model "
                                 "think-aloud (drop a quote, run the check, catch the missing source, revise) "
                                 "with literal BEFORE/AFTER; 3-question check tool folded into the model card as "
                                 "an <ol> at point of first use; discrimination moved AFTER the model (KH) with "
                                 "explicit per-option choices + a construct-confound break (an 'Experts say' "
                                 "distractor has attribution flavor but names no checkable source); diagnosis "
                                 "rebuilt with frq_prompt + setapart(weak draft) + checklist (no hand-written "
                                 "Step N prose); autonomy + say-the-standard on the independent write. Removed "
                                 "the leaked 'Grade-C design bet' label. PROVE = established-caveat."),
                "review_provenance": ("Rebuilt to the v3.1 spec (icm/_config/v3_1-lesson-build-spec.md); passes "
                                      "all 23 lesson_contract gates + gated_reading render-QC clean 2026-07-14.")},
    fade_ledger_moves=["quote-vs-paraphrase-vs-summary", "attributed-evidence-name-the-source"],
    slots=[
        # ===== TEACH: ONE idea, as a LIST (define attributive tag in plain words) =====
        Slot("TEACH", "teach_card", "Three ways to bring in a source, and always name who said it",
             body=(ONE_IDEA +
                   "When you use a source, you have three choices, and each has a job:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Quote</strong>: use the source's exact words inside "
                   "quotation marks. Best when the wording itself matters (an exact figure, a striking phrase).</li>"
                   "<li style=\"margin:4px 0\"><strong>Paraphrase</strong>: put one idea from the source into "
                   "your own words. Best when you want the fact but not the exact phrasing.</li>"
                   "<li style=\"margin:4px 0\"><strong>Summarize</strong>: retell the source's main point "
                   "briefly, in your own words. Best when you need the big picture in a line or two.</li></ul>"
                   "Whichever you choose, one rule never changes: name who said it. An attributive tag is a "
                   "short phrase that names the source, such as 'According to the U.S. Department of "
                   "Agriculture,' or 'the researchers report.' Here is the trap that costs the most Evidence "
                   "points: dropping a quote or a fact into your writing with no source named. A reader has no "
                   "reason to trust a number that seems to come from nowhere. Goal today: bring in one piece of "
                   "evidence and name its source.")),
        Slot("TEACH", "stimulus_display", "Read the source: free school meals",
             ref="ACC-W910-ARG-LESSON-SCHOOLLUNCH", bank="school_lunch",
             body=("Read this source about free school meals. Because your job is to USE its evidence, read the "
                   "whole thing and notice the specific facts and who they come from: the U.S. Department of "
                   "Agriculture and the National Center for Education Statistics. Pick one fact you could bring "
                   "into a piece of writing. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model think-aloud + the check tool folded in =====
        Slot("MODEL", "annotated_before_after", "Watch a writer bring a source in the right way",
             bank="school_lunch",
             body=("Here is the skill in action. Follow the writer's thinking below. " + COPING_HTML +
                   " Notice the one move that turned the BEFORE into the AFTER: the writer named who said it. " +
                   REMEMBER +
                   "When you write your own, do the same: pick the fact, decide whether to quote or paraphrase "
                   "it, name the source, and run the 3 questions before you submit.")),
        Slot("MODEL", "discrimination", "Which sentence names its source?",
             ref="", labeled_grade_c=True, bank="school_lunch",
             body=("You have seen a source brought in the right way. Now spot the target. All three sentences "
                   "use the same fact, but which one brings it in correctly by naming who said it? "
                   "(A) The program hands out a giant number of lunches every single year, and honestly the "
                   "total is so big that you can just tell the whole program really matters to students.  "
                   "(B) According to the U.S. Department of Agriculture, the National School Lunch Program "
                   "served more than 4.8 billion lunches in a recent year.  "
                   "(C) Experts say the program serves billions of lunches every year, which really goes to "
                   "show how much good it does for students across the country. "
                   "Correct: B. It names a specific source, the U.S. Department of Agriculture, so a reader can "
                   "trust and check the fact."),
             choices=[
                 {"id": "A", "text": "The program hands out a giant number of lunches every single year, and honestly the total is so big that you can just tell the whole program really matters to students.",
                  "correct": False,
                  "why": "This gestures at the fact but names no source and gives no exact number, so a reader cannot check it or trust it. A dropped fact is not attributed evidence."},
                 {"id": "B", "text": "According to the U.S. Department of Agriculture, the National School Lunch Program served more than 4.8 billion lunches in a recent year.",
                  "correct": True,
                  "why": "Correct. It names a specific source, the U.S. Department of Agriculture, so the reader knows where the fact comes from and can trust it. That is attributed evidence."},
                 {"id": "C", "text": "Experts say the program serves billions of lunches every year, which really goes to show how much good it does for students across the country.",
                  "correct": False,
                  "why": "'Experts say' sounds like attribution, but it names no specific source a reader could check. Naming who actually reported it is what makes evidence trustworthy, not a vague 'experts say.'"},
             ]),
        Slot("MODEL", "discrimination", "Which sentence reports the number the source really gives?",
             ref="", labeled_grade_c=True, bank="school_lunch",
             body=("You named the source and it checks out. Now run the last question: is the fact really in the "
                   "reading? All three sentences name the same source, the National Center for Education "
                   "Statistics, but only one reports the number the source actually gives. Which one? "
                   "(A) The National Center for Education Statistics reports that about 10.5 million students "
                   "attended high-poverty public schools in a recent year.  "
                   "(B) The National Center for Education Statistics reports that nearly 50 million students "
                   "attended high-poverty public schools, a shockingly large share of every student in the "
                   "whole country.  "
                   "(C) The National Center for Education Statistics reports that every student in the country "
                   "attends a high-poverty public school. "
                   "Correct: A. It names the source and reports the exact figure the reading gives, about 10.5 "
                   "million students, so a reader who checks the source will find it."),
             choices=[
                 {"id": "A", "text": "The National Center for Education Statistics reports that about 10.5 million students attended high-poverty public schools in a recent year.",
                  "correct": True,
                  "why": "Correct. It names the source and reports the exact number the reading gives, so a reader who checks the source will find the fact right there."},
                 {"id": "B", "text": "The National Center for Education Statistics reports that nearly 50 million students attended high-poverty public schools, a shockingly large share of every student in the whole country.",
                  "correct": False,
                  "why": "It names a real source, but 50 million is not the figure the reading gives, so a reader who checks the source would not find it. A named source only helps if the fact is actually there."},
                 {"id": "C", "text": "The National Center for Education Statistics reports that every student in the country attends a high-poverty public school.",
                  "correct": False,
                  "why": "It names a real source, but the reading never says every student attends such a school, so the sentence stretches the fact past what the source supports."},
             ]),
        Slot("MODEL", "predict_the_fix", "Is this evidence ready, and if not, what fixes it?",
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

        # ===== SUPPORTED: framed write (fill-in frame) on the taught source (already read at TEACH) =====
        Slot("SUPPORTED", "production_frq", "Bring in a fact and name its source",
             ref="", bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on the two moves: name the source, and bring in one real fact.",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "According to ______ [name the source], ______ [the fact, quoted in exact words or put in your own words]."),
                 closer="Bring in one real fact from the reading and name its source with an attributive tag. "
                        "Do not drop the fact in with no source. Then check your sentence against the 3 questions.")),
        # DIAGNOSIS = a CHECK-and-FIX on a PROVIDED weak draft (not a fresh production). Stays on the taught
        # source (no new source to read). Rebuilt with frq_prompt + setapart(red) + checklist so the check is a
        # real <ol>, not "Step 1 / Step 2" prose that double-numbers in the render.
        Slot("MODEL", "diagnosis_frq", "Check and fix a weak draft with the 3 questions",
             ref="", bank="school_lunch", scored=True,
             body=frq_prompt(
                 intro="Run the 3-question test on this weak draft, then rewrite it so the evidence is ready.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "Free or reduced-price meals reach students under 185 percent of the poverty line. This helps a lot of families.",
                                         "red"),
                 checklist_block=checklist(title="Run the test:", rows=[
                     ("Did the writer name who said it?", "No, the fact is dropped in with no source. Add an attributive tag naming who reported it."),
                     ("Did the writer choose quote, paraphrase, or summarize on purpose?", "It is a paraphrase (the writer's own words, no quotation marks), so that choice is fine, it just needs its source named."),
                     ("Is the fact really in the source?", "Yes, the 185 percent figure is in the reading."),
                 ]),
                 closer="Now rewrite the weak draft into one sentence that names its source. Then name which "
                        "question your rewrite fixed.")),

        # ===== INDEPENDENT: cold write on the taught source + autonomy + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Bring in evidence and name its source, on your own",
             ref="", bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="On your own now, no frame. Bring one fact from the free-meals source into a sentence.",
                 closer="Choose to quote the exact words or put the fact in your own words, then name who said "
                        "it with an attributive tag. Naming your source is what every piece of evidence in real "
                        "writing depends on, and you are ready to do it cold. Check your sentence against the 3 "
                        "questions before you submit.")),

        # ===== TRANSFER: same move, a NEW source (bird migration), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: bird migration",
             ref="ACC-W910-INFO-LESSON-MIGRATION", bank="animal_migration",
             body=("Read this new source about bird migration. Because your job is to USE its evidence, read "
                   "the whole thing and notice the specific facts and who reports them, such as the National "
                   "Park Service and the U.S. Geological Survey. Pick one fact you could bring into a sentence. "
                   "The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Bring in evidence and name its source (NEW topic)",
             ref="", bank="animal_migration", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="New topic. Bring one fact from the migration source into a sentence, and name its source with an attributive tag.",
                 closer="Same move as the meals sentence, new topic: name who said it, and bring in one real "
                        "fact from the reading, quoted or put in your own words. Check it against the 3 "
                        "questions before you submit.")),
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
