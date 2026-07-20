"""
lesson_g9_l09_integrate_not_drop.py  -  G9 KC C.9.02, ARCHETYPE T3: EVIDENCE-INTEGRATION (PROVE, ceiling paragraph).

G9 course L09. Independent rung: integrate, do NOT drop (I2) - fold the quote into your own sentence rather
than parking it as a standalone sentence. Recycles G1/G2/I1. Locked L01 template; EVIDENCE-TIER binds full
sources. Taught: PHONEBAN (full) -> transfer: WATER-CYCLE (full, partitioned). rc.staar, unit="sentence".
PROVE=established-caveat; mechanics gated; no coping-model persona; no source markup; no prior-work ref; no
em dashes. Runs QC on execution.
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
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> the quote is dropped as its own sentence</span>'
    '<p style="margin:8px 0 0;font-size:15px">Many schools already restrict phones. "76.9 percent." This is a '
    'lot of schools.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The number sits alone as its own choppy sentence. '
    'The reader has to guess how it connects to the point. A dropped quote reads as a stray fact.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> the quote is folded into the writer\'s own sentence</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">WRITER\'S WORDS</span> Phone limits are already the norm: '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">EVIDENCE FOLDED IN</span> the National Center for Education Statistics reports that '
      '"76.9 percent" of public schools restricted non-academic phone use.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">The number is now woven into a sentence the writer '
    'built, introduced and attributed, so the reader sees exactly how it fits. That is integrating, not '
    'dropping.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C902-0009", grade="9-10", lesson_type=3,
    unit="G9 U1 - Claim/controlling-idea + evidence (integrate, do not drop)",
    title="Fold the Quote Into Your Own Sentence",
    target=("Integrate a quote instead of dropping it: fold the source's words into a sentence you build, with "
            "an introduction and attribution, so it never stands alone. Written at the sentence. Trait: "
            "Evidence/Development."),
    acc_tags=["ACC.W.SRC.2", "CCSS.W.9-10.8"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12",
                "mnemonic_status": "established-caveat", "kc": "C.9.02", "sot": "icm course-G9.md L09",
                "taught_stimulus": "ACC-W910-ARG-LESSON-PHONEBAN",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-WATER-CYCLE",
                "playbook": "_phase2/playbook_T3_PROVE.md",
                "template": "locked L01 template; EVIDENCE-TIER binds full sources.",
                "council": "T3/PROVE independent rung: introduces I2 integrate-not-drop (folded-in vs dropped); recycles G1/G2/I1. Sentence-combining mechanics app-owned + gated, taught by USE only."},
    fade_ledger_moves=["integrate-not-drop", "introduce-and-attribute-in-one-sentence"],
    slots=[
        Slot("TEACH", "teach_card", "Weave the quote in, do not park it alone",
             body=("Naming the source is step one; step two is HOW the quote sits in your writing. Integrating "
                   "a quote means folding the source's words into a sentence you build, with a short "
                   "introduction and the source named, so it flows. Dropping a quote means parking it as its "
                   "own standalone sentence with no lead-in, so the reader has to guess how it connects. "
                   "Compare: dropped is 'Schools restrict phones. \"76.9 percent.\" That is a lot.' Integrated "
                   "is 'The National Center for Education Statistics reports that \"76.9 percent\" of schools "
                   "restrict phones.' The exact same quote lands far better when it is woven in. This is a "
                   "rhetorical move, how you place the evidence, not a grammar lesson; the sentence-combining "
                   "skill you use to weave it comes from your earlier courses and we only apply it here. The "
                   "trap is the dropped quote, a number floating in its own choppy sentence. Goal today: fold "
                   "one quote into a sentence you build.")),
        Slot("TEACH", "stimulus_display", "Read the source: phones in school",
             ref="ACC-W910-ARG-LESSON-PHONEBAN", bank="phone_ban",
             body=("Read this source about phones in school. Because your job is to USE a quote from it, read "
                   "the whole thing and pick one specific fact with a number you could weave into your own "
                   "sentence, and note who reports it. The text stays on screen while you work.")),
        Slot("TEACH", "discrimination", "Which sentence integrates the quote?",
             ref="", labeled_grade_c=True, bank="phone_ban",
             body=("Sort these before you write (spotting the target before producing it, a Grade-C design bet "
                   "we label as a bet, not a proven ingredient). Both use the same quoted number and name the "
                   "source. Which one INTEGRATES the quote instead of dropping it? "
                   "(A) Phones are common in schools these days. The National Center for Education Statistics "
                   "said this in a report. \"76.9 percent.\" That is a lot of schools all across the country.  "
                   "(B) The National Center for Education Statistics reports that \"76.9 percent\" of public "
                   "schools already restricted non-academic phone use. "
                   "Correct: B. (A) names the source but the number is still dropped in as its own choppy "
                   "fragment, so it does not flow. (B) folds the quote into one sentence the writer built, with "
                   "the source introduced, so it reads smoothly. That is integrating, not dropping.")),
        Slot("MODEL", "annotated_before_after", "Watch a dropped quote get folded in",
             bank="phone_ban",
             body=("Here is a dropped quote being folded into the writer's own sentence. Read the BEFORE, then "
                   "the AFTER, and notice the number is no longer a standalone fragment." + BEFORE_AFTER_HTML +
                   " The BEFORE parks the number alone. The AFTER weaves it into a sentence the writer built, "
                   "introduced and attributed. Folding it in is the move.")),
        Slot("MODEL", "predict_the_fix", "What does this dropped quote most need?",
             bank="phone_ban",
             body=("Diagnose this draft before the reveal. A student wrote: 'Restricting phones is already "
                   "common. \"76.9 percent.\" Schools agree.' Which single move would most improve how the "
                   "quote is used? "
                   "(A) fold the number into a sentence the writer builds, introducing and attributing it, so "
                   "it does not stand alone  "
                   "(B) add a second number right after the first one so the paragraph piles up more figures "
                   "that back the point  "
                   "(C) delete the quotation marks around the number so the sentence reads a little cleaner and "
                   "less choppy overall  "
                   "(D) move the quote down to the end of the paragraph so it lands as a strong closing fact "
                   "after the writer's point"),
             feedback=("Correct: A. The number is dropped in as its own fragment, so the reader cannot see how "
                       "it connects. The fix is to integrate it: 'The National Center for Education Statistics "
                       "reports that \"76.9 percent\" of schools restricted phone use.' A second number (B) "
                       "adds more dropped text; deleting the quotation marks (D) hides that these are the "
                       "source's words; just moving it (D) still leaves it dropped.")),
        Slot("SUPPORTED", "production_frq", "Fold a quote into your own sentence",
             ref="", bank="phone_ban", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("Use this frame to integrate a quote from the source: '______ [name the source] reports "
                   "that \"______\" [the quoted fact], ______ [finish the sentence in your own words].' Goal: "
                   "fold the quote into one sentence you build, introduce and attribute it, and keep it "
                   "flowing. Do not park the quote as its own fragment. Write one sentence. Scored on "
                   "Evidence/Development.")),
        Slot("MODEL", "diagnosis_frq", "Check your quote: is it folded in or dropped?",
             ref="", bank="phone_ban", scored=True,
             body=("First watch the check run on a weak draft, then run it on a fresh sentence of your own. "
                   "Weak draft: 'Schools limit phones. \"90.9 percent\" in 2009-10. Rules were strict.' Run "
                   "the check step by step. Step 1, folded in or dropped? Dropped, the number is its own "
                   "fragment, so weave it into a built sentence. Step 2, introduced and attributed? No source "
                   "named, add one. Step 3, does it flow? No, it is choppy. Now you: write one fresh sentence "
                   "that folds a quote from the source in, then run the same checks. For each No, use the fix: "
                   "weave the quote into a sentence you build; introduce and name the source. Finish by naming "
                   "which check your sentence still needs most.")),
        Slot("INDEPENDENT", "production_frq", "Integrate a quote on your own",
             ref="", bank="phone_ban", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("On your own now. Pick one quoted fact from the phone source and fold it into a sentence you "
                   "build. Goal: introduce and attribute the quote and weave it in so it never stands alone. "
                   "Before you submit, check your sentence: is the quote folded into a sentence I built, is the "
                   "source introduced, does it flow? If any answer is no, fix it before you submit. Do not park "
                   "the quote as its own fragment. Scored on Evidence/Development.")),
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: the water cycle",
             ref="ACC-W910-INFO-LESSON-WATER-CYCLE", bank="water_cycle",
             body=("Read this new source about the water cycle. Because your job is to USE a quote from it, "
                   "read the whole thing and pick one specific fact you could weave into your own sentence, and "
                   "note who reports it. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Integrate a quote on a NEW topic",
             ref="", bank="water_cycle", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("New topic. Pick one fact from the water-cycle source and fold it into a sentence you build, "
                   "introduced and attributed. Goal: weave the quote into your own sentence so it never stands "
                   "alone. Same move as the phone sentence, new topic. Do not park the quote as its own "
                   "fragment. Scored on Evidence/Development.")),
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
