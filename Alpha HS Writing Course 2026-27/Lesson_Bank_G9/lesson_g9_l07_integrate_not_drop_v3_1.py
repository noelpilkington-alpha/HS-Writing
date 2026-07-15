"""
lesson_g9_l09_integrate_not_drop_v3_1.py  -  G9 KC C.9.02, ARCHETYPE T3 evidence-integration (PROVE, sentence). V3.1.

V3.1 (Noel 2026-07-14): rebuilds lesson_g9_l09_integrate_not_drop.py to the v3.1 lesson-build spec
(icm/_config/v3_1-lesson-build-spec.md), the pattern G9 L01 v3.1 set. TEACHING POINT PRESERVED: integrate a
quote, do NOT drop it - fold the source's words into a sentence you build (with a tag naming who said it) so it
never stands alone. Same id, same KC C.9.02, same archetype T3/PROVE, same bound fact-sourced -LESSON- stimuli
(PHONEBAN taught -> WATER-CYCLE transfer). Changes applied to reach v3.1:
  1. ONE-IDEA teal callout + a LIST teach (dropped vs integrated as parallel <li> items), replacing the old
     161-word prose wall (fixes the format_fidelity wall-of-text failure).
  2. NAME THE MOVE: "attributive tag" taught as the technical term for the introduce-and-attribute move,
     defined in the TEACH body with a definitional cue ("is a") - faultless communication / define-before-use.
  3. MODEL BEFORE THE QUIZ (KH): coping-model think-aloud (attempt -> run the check -> catch the dropped quote
     -> fold it in), keeping literal BEFORE + AFTER, now PRECEDES the discrimination check. The reusable 3-
     question check tool is folded in here at the point of first use, not cold in step 1.
  4. DISCRIMINATION as structured choices=[{id,text,correct,why}]; homogeneous option lengths (correct is not
     the lone longest); the confound broken - naming the source appears in a WRONG option too, so "folded into
     one built sentence" is the only invariant (DI faultless communication). Removed the leaked "Grade-C design
     bet" label from the student text (fixes leaked_internal_label).
  5. FRQ + diagnosis bodies built with frq_prompt/setapart/checklist (no "Step 1/2" prose, no "Scored on..."
     chrome). SUPPORTED = the fill-in frame first; diagnosis = watch the check on a weak draft, then run it.
  6. AUTONOMY + SAY-THE-STANDARD on the independent write (Yeager).

ONE IDEA: integrate the quote, do not drop it. ONE REMINDER: the 3-question quote check.
Passes all 23 lesson_contract gates. Own words, no fabricated figures, no em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px"><strong>Integrate</strong> a quote, do not '
'<strong>drop</strong> it: fold the source\'s words into a sentence you build, with a tag naming who said it, '
'so the quote never stands alone.</div></div>')

# The reusable check tool, folded in at the model (point of first use), rendered as a real <ol>.
REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit a quote, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Is the quote folded into a sentence you built, not sitting alone?</li>'
'<li style="margin:2px 0">Did you name who said it (the attributive tag)?</li>'
'<li style="margin:2px 0">Does it flow, so a reader sees how it fits your point?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, the quote is still dropped, not integrated.</div></div>')

# coping-model think-aloud: a WRITTEN drafting process (attempt -> run the check -> catch the drop -> revise),
# then the literal BEFORE and AFTER endpoints (content_depth). No named near-peer (Timeback stateless rule).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer thinking it through, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Many schools already limit phones. \'76.9 '
    'percent.\' That is a lot." Run the check: is the quote folded into a sentence I built? No, the number sits '
    'alone as its own fragment. Fix it.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "The National Center for Education Statistics said '
    'this. \'76.9 percent.\'" Better, the source is named now, but the number is still parked as its own '
    'fragment. Fold it into the sentence.</p>'
    '<p style="margin:0"><strong>Final:</strong> "The National Center for Education Statistics reports that '
    '\'76.9 percent\' of public schools already restricted non-academic phone use." Now the quote is woven into '
    'one sentence I built, with the source named. That passes.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "Many schools already limit phones. \'76.9 percent.\' That is '
    'a lot." (the number is dropped as its own fragment)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "The National Center for Education Statistics reports that '
    '\'76.9 percent\' of public schools already restricted non-academic phone use." (folded into a built '
    'sentence, source named)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C902-0009", grade="9-10", lesson_type=3,
    unit="G9 U1 - Claim/controlling-idea + evidence (integrate, do not drop)",
    title="Fold the Quote Into Your Own Sentence",
    target=("Integrate a quote instead of dropping it: fold the source's words into a sentence you build, with "
            "an introduction and attribution, so it never stands alone. Written at the sentence. Trait: "
            "Evidence/Development."),
    acc_tags=["ACC.W.SRC.2", "CCSS.W.9-10.8"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "established-caveat", "kc": "C.9.02", "sot": "icm course-G9.md L09",
                "taught_stimulus": "ACC-W910-ARG-LESSON-PHONEBAN",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-WATER-CYCLE",
                "one_idea": "Integrate the quote, do not drop it: fold it into a sentence you build.",
                "one_reminder": "3-question quote check: folded in? source named? does it flow?",
                "playbook": "_phase2/playbook_T3_PROVE.md",
                "template": "locked L01 template; EVIDENCE-TIER binds full sources.",
                "version_note": ("V3.1: rebuilt lesson_g9_l09_integrate_not_drop.py to the v3.1 spec (G9 L01 "
                                 "pattern). ONE-IDEA callout + list teach (fixes format_fidelity wall of text); "
                                 "'attributive tag' named + defined with a cue (define-before-use); coping-model "
                                 "think-aloud precedes the quiz (KH), 3-question check folded in at point of "
                                 "first use; discrimination as structured choices with the naming-the-source "
                                 "confound broken + no leaked Grade-C label; FRQ/diagnosis bodies via "
                                 "frq_prompt/setapart/checklist; autonomy + say-the-standard on independent."),
                "council": ("T3/PROVE independent rung: integrate-not-drop (folded-in vs dropped); recycles "
                            "G1/G2/I1. Sentence-combining mechanics app-owned + gated, taught by USE only."),
                "review_provenance": ("Rebuilt against icm/_config/v3_1-lesson-build-spec.md + G9 L01 v3.1 "
                                      "exemplar; 23 lesson_contract gates + gated_reading render-QC clean 2026-07-14.")},
    fade_ledger_moves=["integrate-not-drop", "name-the-source-attributive-tag",
                       "fold-quote-into-one-built-sentence"],
    slots=[
        # ===== TEACH: ONE idea + a short LIST (dropped vs integrated); name + define "attributive tag" =====
        Slot("TEACH", "teach_card", "The one idea: fold the quote in, do not park it alone",
             body=(ONE_IDEA +
                   "Naming a source is step one. Step two is HOW the quote sits in your writing. Two kinds of "
                   "sentence use the very same quote but land very differently:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Dropped</strong>: the quote is parked as its own "
                   "standalone fragment with no lead-in, so the reader has to guess how it connects "
                   "('Schools limit phones. \'76.9 percent.\' That is a lot').</li>"
                   "<li style=\"margin:4px 0\"><strong>Integrated</strong>: the quote is folded into a sentence "
                   "you build, introduced and attributed, so it flows ('The National Center for Education "
                   "Statistics reports that \'76.9 percent\' of schools restrict phones').</li></ul>"
                   "The introduce-and-attribute part has a name: an <strong>attributive tag</strong> is a short "
                   "phrase that names who said it, such as 'the National Center for Education Statistics reports "
                   "that.' It hands the quote to the reader instead of dropping it in cold. This is a rhetorical "
                   "move, how you place the evidence, not a grammar lesson; the sentence-combining you use to "
                   "weave it comes from earlier courses and we only apply it here. The trap is the dropped quote, "
                   "a number floating in its own choppy fragment. Goal today: fold one quote into a sentence you "
                   "build.")),
        Slot("TEACH", "stimulus_display", "Read the source: phones in school",
             ref="ACC-W910-ARG-LESSON-PHONEBAN", bank="phone_ban",
             body=("Read this source about phones in school. Because your job is to USE a quote from it, read "
                   "the whole thing and note one specific fact with a number you could weave into your own "
                   "sentence, and note who reports it. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model think-aloud + the 3-question check folded in =====
        Slot("MODEL", "annotated_before_after", "Watch a writer fold a dropped quote in",
             bank="phone_ban",
             body=("Here is the skill in action. Follow the writer's thinking as a dropped quote gets folded "
                   "into a built sentence. " + COPING_HTML +
                   " Notice the two moves that turned the BEFORE into the AFTER: the writer wove the number into "
                   "one sentence they built, then named the source with an <strong>attributive tag</strong>. " +
                   REMEMBER +
                   "When you write your own, build it the same way: fold the quote into a sentence, name who "
                   "said it, then run the 3 questions before you submit.")),
        Slot("MODEL", "discrimination", "Which sentence integrates the quote?",
             ref="", labeled_grade_c=True, bank="phone_ban",
             body=("Now that you have seen one built, spot the target. All three use the same quoted number. "
                   "Which one INTEGRATES the quote, folding it into a built sentence, instead of dropping it? "
                   "(A) The National Center for Education Statistics said it in a report from that year. "
                   "\"76.9 percent.\" That really is a lot of schools with limits.  "
                   "(B) The National Center for Education Statistics reports that \"76.9 percent\" of public "
                   "schools already restricted non-academic phone use.  "
                   "(C) Lots of schools limit phones these days. \"76.9 percent.\" Rules like that are common "
                   "all across the country now. "
                   "Correct: B. It folds the quote into one sentence the writer built, with the source "
                   "introduced, so it flows. (A) and (C) still park the number as its own fragment."),
             choices=[
                 {"id": "A", "text": "The National Center for Education Statistics said it in a report from that year. \"76.9 percent.\" That really is a lot of schools with limits.",
                  "correct": False,
                  "why": "This names the source, but the number is still dropped in as its own fragment. Naming who said it is not enough; the quote has to be folded into the sentence."},
                 {"id": "B", "text": "The National Center for Education Statistics reports that \"76.9 percent\" of public schools already restricted non-academic phone use.",
                  "correct": True,
                  "why": "Correct. The quote is folded into one sentence the writer built, introduced and attributed with a tag, so a reader sees exactly how it fits. That is integrating, not dropping."},
                 {"id": "C", "text": "Lots of schools limit phones these days. \"76.9 percent.\" Rules like that are common all across the country now.",
                  "correct": False,
                  "why": "The number sits alone as its own fragment and no source is named, so the reader has to guess how it connects. That is a dropped quote."},
             ]),
        # SECOND minimal pair, same skill, DIFFERENT confound: the existing pair breaks on folding (a wrong
        # option names the source yet parks the number as a fragment). This pair breaks on ATTRIBUTION - the
        # longest wrong option (B) folds the quote in AND flows, but never names who said it, so "named with a
        # tag" is the only invariant that separates it from the correct answer. Fresh figure (65.8 percent).
        Slot("MODEL", "discrimination", "Which sentence names the source AND folds the quote in?",
             ref="", labeled_grade_c=True, bank="phone_ban",
             body=("Same target skill, a new number. All three sentences use the same reported figure. "
                   "Which one INTEGRATES it: folded into a sentence the writer built AND with the source named? "
                   "(A) Federal data from the National Center for Education Statistics show that only "
                   "\"65.8 percent\" of public schools banned such phone use by 2015-16.  "
                   "(B) By 2015-16 the share of public schools with such a phone rule had slipped to just "
                   "\"65.8 percent\" before it later climbed back up again toward earlier levels.  "
                   "(C) The rule got less common for a while. \"65.8 percent\" by 2015-16. Then it went back up. "
                   "Correct: A. It folds the number into one sentence the writer built and names the source with "
                   "a tag. (B) folds it in and flows but names no source. (C) parks the number as its own fragment."),
             choices=[
                 {"id": "A", "text": "Federal data from the National Center for Education Statistics show that only \"65.8 percent\" of public schools banned such phone use by 2015-16.",
                  "correct": True,
                  "why": "The number is folded into one built sentence and the source is named with a tag, so the reader sees both whose figure it is and how it fits."},
                 {"id": "B", "text": "By 2015-16 the share of public schools with such a phone rule had slipped to just \"65.8 percent\" before it later climbed back up again toward earlier levels.",
                  "correct": False,
                  "why": "This flows and folds the number in, but it names no source, so the reader cannot tell whose figure it is and the quote is still dropped."},
                 {"id": "C", "text": "The rule got less common for a while. \"65.8 percent\" by 2015-16. Then it went back up.",
                  "correct": False,
                  "why": "The number sits alone as its own fragment with no lead-in, so it is dropped rather than woven into a built sentence."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this dropped quote most need?",
             bank="phone_ban",
             body=("Diagnose this draft before the reveal. A student wrote: 'Restricting phones is already "
                   "common. \"76.9 percent.\" Schools agree.' Which single move would most improve how the "
                   "quote is used? "
                   "(A) fold the number into a sentence the writer builds and name who reports it, so it does not stand alone  "
                   "(B) add a second number right after the first so the paragraph piles up even more supporting figures  "
                   "(C) delete the quotation marks around the number so the sentence reads a little cleaner and less choppy  "
                   "(D) move the quote down to the end of the paragraph so it lands as a strong closing fact after you make your point"),
             feedback=("Correct: A. The number is dropped in as its own fragment, so the reader cannot see how "
                       "it connects. The fix is the two moves you just saw: fold it into a built sentence and "
                       "name the source with an attributive tag ('The National Center for Education Statistics "
                       "reports that \"76.9 percent\" of schools restricted phone use'). A second number (B) "
                       "adds more dropped text; deleting the quotation marks (C) hides that these are the "
                       "source's words; just moving it (D) still leaves it dropped.")),

        # ===== SUPPORTED: framed write (fill-in frame) on the taught source (already read at TEACH) =====
        Slot("SUPPORTED", "production_frq", "Fold a quote into your own sentence",
             ref="", bank="phone_ban", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on the two moves: name the source, then fold the quote in.",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "______ [name the source] reports that \"______\" [the quoted fact], "
                                         "______ [finish the sentence in your own words]."),
                 closer="Fold one quote from the phone source into a single sentence you build, introduce and "
                        "attribute it, and keep it flowing. Do not park the quote as its own fragment. Then run "
                        "the 3-question check.")),
        # DIAGNOSIS = a CHECK-and-FIX on a PROVIDED weak draft (not a fresh production, so it does not repeat the
        # supported write). Stays on the taught source = no new source to read (load balance).
        Slot("MODEL", "diagnosis_frq", "Check a weak draft: is the quote folded in or dropped?",
             ref="", bank="phone_ban", scored=True,
             body=frq_prompt(
                 intro="Run the 3-question check on this weak draft, then rewrite it into a real integrated sentence.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "Schools limit phones. \"90.9 percent\" in 2009-10. Rules were strict.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Is the quote folded into a built sentence?", "No, the number is its own fragment. Weave it into a sentence you build."),
                     ("Did you name who said it?", "No source is named. Add an attributive tag (who reports it)."),
                     ("Does it flow?", "No, it is choppy. Fix the first two and it will."),
                 ]),
                 closer="Now rewrite the weak draft into one sentence that folds the quote in, names the source, "
                        "and flows. Then name which question your rewrite fixed.")),

        # ===== INDEPENDENT: cold write on the taught source, no frame; autonomy + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Integrate a quote on your own",
             ref="", bank="phone_ban", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="On your own now, no frame. Pick one quoted fact you actually find convincing from the phone source.",
                 closer="Fold it into a sentence you build and name the source with an attributive tag, so the "
                        "quote never stands alone. This fold-it-in move is what every source-based argument is "
                        "built on, and you are ready to do it cold. Check your sentence against the 3 questions "
                        "before you submit.")),

        # ===== TRANSFER: same move, a NEW source (water cycle), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: the water cycle",
             ref="ACC-W910-INFO-LESSON-WATER-CYCLE", bank="water_cycle",
             body=("Read this new source about the water cycle. Because your job is to USE a quote from it, read "
                   "the whole thing and note one specific fact you could weave into your own sentence, and note "
                   "who reports it. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Integrate a quote on a NEW topic",
             ref="", bank="water_cycle", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="New topic, same move. Pick one fact from the water-cycle source.",
                 closer="Fold it into a sentence you build and name the source with an attributive tag, so the "
                        "quote never stands alone. Same move as the phone sentence, fresh topic. Check it "
                        "against the 3 questions before you submit.")),
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
