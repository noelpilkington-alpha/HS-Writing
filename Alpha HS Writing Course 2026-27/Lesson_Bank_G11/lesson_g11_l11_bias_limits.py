"""
lesson_g11_l11_bias_limits.py  -  G11 KC C.11.08, lesson_type 3 source-evaluation (PROVE, sentence tier). V3.1.

G11 L11 (Unit 3, guided), rebuilt to the v3.1 build spec. Teaching point (kept): detect a source's slant (what
it omits or how it frames) and name its STRENGTHS and LIMITS (what to trust it for, where it falls short),
rather than accepting or rejecting it wholesale. Written at the sentence. KC C.11.08. Keeps bound fact-sourced
stimuli (water_infrastructure taught -> energy_transition transfer). Deterministic FRQ prompts, coping-model
think-aloud with a literal BEFORE/AFTER, explicit-choices discrimination. 23 gates.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

FONT = "-apple-system,Segoe UI,Roboto,Arial,sans-serif"

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:' + FONT + '">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A source is trustworthy for some things and limited '
'for others. The college move is to name <strong>both</strong>: what to trust it <strong>for</strong> and where '
'it <strong>falls short</strong>, instead of accepting or rejecting the whole source at once.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:' + FONT + '">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit an evaluation, ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0"><strong>Strength</strong>: have I named what to trust this source FOR?</li>'
'<li style="margin:2px 0"><strong>Limit</strong>: have I named where it falls short or what it leaves out?</li>'
'<li style="margin:2px 0"><strong>Verdict</strong>: did I avoid an all-or-nothing "trust everything" or "trust nothing"?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">Miss the strength or the limit, and it collapses back into a blanket verdict.</div></div>')

COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;font-family:' + FONT + '">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer weighing the water-use source, one pass at a time:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "This source is completely reliable, so I will trust '
    'everything it says." Now run the check. What do I trust it FOR? I only said "everything," which names no real '
    'use. Where does it fall short? I never said. This is all-or-nothing.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "The source is strong evidence for national water-use '
    'totals." Better, that names a strength. But the check still has a gap: I have not said where it falls short, '
    'so it is only half the move.</p>'
    '<p style="margin:0"><strong>Final:</strong> "The source is strong evidence for national water-use totals, '
    'but because it reports national averages it says little about any single region\'s shortage." Now it names a '
    'strength AND a limit.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> An all-or-nothing verdict: "completely reliable, trust '
    'everything." It names no specific use and no limit.</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> Strengths AND limits: strong FOR national totals, but limited '
    'on any single region. That split verdict is the move.</span></div>'
'</div>')

SLANT_DFN = ('<dfn class="tb-glossary-term" data-catalog-idref="def-slant" title="slant means the way a source '
             'leaves things out or frames them to favor one side">slant</dfn>')

LESSON = Lesson(
    id="ACC-W1112-L-G11-C1108-0011", grade="9-10", lesson_type=3,
    unit="G11 U3 - Source evaluation (bias, strengths and limits)",
    title="Name What a Source Is Good For and Where It Falls Short",
    target=("Detect a source's slant (what it omits or how it frames) and name its strengths AND limits (what "
            "to trust it for, where it falls short), rather than accepting or rejecting it wholesale. Written "
            "at the sentence. Trait: Evidence (source evaluation)."),
    acc_tags=["ACC.W.INQ.1", "CCSS.W.11-12.8"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "established-caveat", "kc": "C.11.08", "sot": "icm course-G11.md L11",
                "taught_stimulus": "ACC-W910-INFO-LESSON-WATERUSE",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-ENERGYMIX",
                "playbook": "_phase2/playbook_T3_PROVE.md",
                "template": "locked L01 v3.1 template; binds full info sources.",
                "one_idea": "A source is trustworthy for some things, limited for others; name both, not a blanket verdict.",
                "one_reminder": "Check 3: named a strength (trust it FOR)? named a limit (falls short)? avoided all-or-nothing?",
                "version_note": ("V3.1 rebuild: replaced the prose-wall body with the v3.1 spine (ONE_IDEA teal "
                                 "callout + <ul> teach; coping-model think-aloud with literal BEFORE/AFTER; "
                                 "REMEMBER dashed 3-question checklist; explicit-choices discrimination; "
                                 "predict-the-fix reveal in feedback; fill-in frame SUPPORTED write; scaffolded "
                                 "diagnosis; autonomy INDEPENDENT + transfer). Kept id/type/kc/unit/bound stimuli."),
                "council": ("T3/PROVE G11 source-eval guided rung: V2 detect-bias + V3 strengths-and-limits. "
                            "strengths-and-limits-vs-all-or-nothing discrimination labeled_grade_c in code only. "
                            "PROVE=established-caveat."),
                "review_provenance": "built to the L01 v3.1 pattern"},
    fade_ledger_moves=["detect-bias", "name-strengths-and-limits"],
    slots=[
        Slot("TEACH", "teach_card", "The one idea: strengths AND limits",
             body=(ONE_IDEA +
                   "You have two jobs when you weigh a source. First, spot its " + SLANT_DFN + ": what it leaves "
                   "out, or how it frames things to favor one side. Then name its strengths and its limits:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Slant</strong>: what a source omits, or how it frames "
                   "things (a group with a stake emphasizes what helps it).</li>"
                   "<li style=\"margin:4px 0\"><strong>Strength</strong>: what to trust the source FOR (a "
                   "national dataset is strong evidence for country-wide totals).</li>"
                   "<li style=\"margin:4px 0\"><strong>Limit</strong>: where it falls short (that same national "
                   "dataset says little about any one region's situation).</li></ul>"
                   "All-or-nothing verdicts ('completely reliable', 'totally biased') are the weak move, because "
                   "how far to trust a source depends on the use. Goal today: name what a source is good for and "
                   "where it falls short.")),
        Slot("TEACH", "stimulus_display", "Read the source: U.S. water use",
             ref="ACC-W910-INFO-LESSON-WATERUSE", bank="water_infrastructure",
             body=("Read this source on U.S. water use. Because your job is to name strengths and limits, notice "
                   "what its figures are strong evidence for and what they cannot tell you (for example, national "
                   "totals versus one region). The text stays on screen while you work.")),
        Slot("MODEL", "annotated_before_after", "Watch a blanket verdict become a strengths-and-limits verdict",
             bank="water_infrastructure",
             body=("Here is the move in action. Follow the writer draft a verdict, run the check, catch the gap, "
                   "and revise, pass by pass. " + COPING_HTML +
                   " Notice the difference: the first verdict accepts everything; the final one names a strength "
                   "AND a limit. That split is the college move." + REMEMBER +
                   "When you write your own, name both parts, then run the 3-question check.")),
        Slot("MODEL", "discrimination", "Which verdict names strengths AND limits?",
             ref="", labeled_grade_c=True, bank="water_infrastructure",
             body=("Spot the target before you write. Which verdict names STRENGTHS AND LIMITS, and which are "
                   "ALL-OR-NOTHING? "
                   "(A) The source is completely reliable because it is an official federal report, so every "
                   "single figure in it can be trusted and used to support any claim a writer might ever want to "
                   "make about water.  "
                   "(B) The source is strong evidence for national water-use totals, but because it reports "
                   "national averages it says little about any single region's own shortage.  "
                   "(C) The source is clearly slanted toward large federal agencies, so none of its figures can "
                   "be trusted and the whole report should be dropped from an argument.  "
                   "(D) The source is strong evidence for national water-use totals, and its figures come from a "
                   "careful federal survey that measured water use across the country. "
                   "Correct: B. B names a strength (national totals) AND a limit (a single region). A and C are "
                   "all-or-nothing (trust everything, trust nothing). D names only a strength and never says "
                   "where the source falls short."),
             choices=[
                 {"id": "A",
                  "text": "The source is completely reliable because it is an official federal report, so every single figure in it can be trusted and used to support any claim a writer might ever want to make about water.",
                  "correct": False,
                  "why": "All-or-nothing accept. It trusts everything and names no limit, so it never says where the source falls short."},
                 {"id": "B",
                  "text": "The source is strong evidence for national water-use totals, but because it reports national averages it says little about any single region's own shortage.",
                  "correct": True,
                  "why": "Correct. It names a strength (trust it FOR national totals) AND a limit (it falls short on any single region). That split verdict is the move."},
                 {"id": "C",
                  "text": "The source is clearly slanted toward large federal agencies, so none of its figures can be trusted and the whole report should be dropped from an argument.",
                  "correct": False,
                  "why": "All-or-nothing reject. Spotting a slant does not make every figure worthless; this names no use the source is still strong for."},
                 {"id": "D",
                  "text": "The source is strong evidence for national water-use totals, and its figures come from a careful federal survey that measured water use across the country.",
                  "correct": False,
                  "why": "Names a strength only. It never states a limit, so it is half the move, not a strengths-and-limits verdict."},
             ]),
        Slot("MODEL", "discrimination", "Which verdict names a strength AND a real gap?",
             ref="", labeled_grade_c=True, bank="water_infrastructure",
             body=("One more before you write. Which verdict names what to trust the source FOR and also points "
                   "to a real gap in what it cannot tell you, not just something you dislike about it?"),
             choices=[
                 {"id": "A",
                  "text": "The report is solid evidence for how national water use has changed since 1990, but because its figures stop at 2020 it cannot show whether the recent drought changed that trend.",
                  "correct": True,
                  "why": "Correct. It names what to trust it for (the long-term water-use trend) and a real limit (its figures stop at 2020, so it says nothing about the recent drought)."},
                 {"id": "B",
                  "text": "The report comes from a federal agency and is packed with detailed tables, so it is exactly the kind of official document a careful writer can cite as completely settled on every water question.",
                  "correct": False,
                  "why": "This treats the whole source as settled and points to no gap, so it accepts everything instead of naming a limit."},
                 {"id": "C",
                  "text": "The report is trustworthy for water-use totals, but its writing is dry and technical, so that flaw drags the whole source down.",
                  "correct": False,
                  "why": "Being hard to read is a style complaint, not a gap in what the source can tell you, so this never names a real limit on its evidence."},
                 {"id": "D",
                  "text": "The report's figures stop at 2020, so it cannot show whether the recent drought changed water use, which means it is out of date and should be set aside.",
                  "correct": False,
                  "why": "This names a real gap (the figures stop at 2020), but it never says what to trust the source FOR and slides into setting it aside, so it is only the limit half, not a strengths-and-limits verdict."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this verdict most need?",
             bank="water_infrastructure",
             body=("Diagnose this draft before the reveal. A student wrote: 'This source is biased, so it is "
                   "useless.' Which single move would most improve it? "
                   "(A) name what the source is still good for AND where it falls short, instead of rejecting it "
                   "wholesale  "
                   "(B) call it biased even more strongly and treat that slant as proof the entire source has no "
                   "value at all  "
                   "(C) drop the source from the argument completely, since anything with any slant simply "
                   "cannot be used at all  "
                   "(D) declare it completely reliable instead and trust every figure without ever checking what "
                   "it leaves out"),
             feedback=("Correct: A. 'Biased, so useless' is all-or-nothing in the other direction. Even a "
                       "slanted source may be strong for some facts (figures it has no motive to distort) and "
                       "limited for others (how it frames a debate). The fix names both. A stronger dismissal "
                       "(B), dropping it (C), or flipping to blanket trust (D) all skip the strengths-and-limits "
                       "move.")),
        Slot("SUPPORTED", "production_frq", "Warm up: fill in a strengths-and-limits frame",
             ref="", bank="water_infrastructure", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="Warm up with a frame. Here is the shape of a strengths-and-limits sentence:",
                 setapart_block=setapart("Copy this frame:",
                                         "The source is strong evidence for ______ (what to trust it for), but ______ (where it falls short)."),
                 closer="Fill in both blanks using the water-use source. Name one use it is strong evidence for "
                        "and one place it falls short. Do not give an all-or-nothing verdict. Write ONE sentence.")),
        # COUNCIL FIX (2026-07-24): Option A (later-in-arc). One graded rewrite; checks read-only beneath; name-act
        # dropped. Was a bundle: 3 pre-answered (q,a) tuple rows (which leaked the answers) + a fresh evaluation +
        # run-the-same-check + name-the-limit in one box (unscoreable, wired to no grader). Now ONE graded act (the
        # rewrite); the 3 strengths-and-limits questions print READ-ONLY beneath (no typed yes/no, no scrolling
        # back), and the run-again + name-the-limit tail is dropped. Kept as diagnosis_frq with the grader tuple
        # declared (sentence:writing). Stays on the taught source (no new read).
        Slot("MODEL", "diagnosis_frq", "Fix a weak evaluation into a strengths-and-limits one",
             ref="", bank="water_infrastructure", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="Rewrite this weak evaluation of the water-use source into one that names both a strength "
                       "and a limit.",
                 setapart_block=setapart("Weak draft to fix:", "This source is trustworthy.", "red"),
                 checklist_block=checklist(title="Make your rewrite pass these (no need to type answers):", rows=[
                     "Strength: does it say what to trust the source FOR?",
                     "Limit: does it say where the source falls short or what it leaves out?",
                     "Verdict: did it avoid an all-or-nothing 'trust everything' or 'trust nothing'?",
                 ]),
                 closer="This draft gives a blanket verdict: 'trustworthy' names no specific use and no limit. "
                        "Write one strengths-and-limits evaluation of the water-use source that names one use it is "
                        "strong evidence for and one place it falls short. Run the three checks above before you "
                        "submit.")),
        Slot("INDEPENDENT", "production_frq", "Evaluate strengths and limits on your own",
             ref="", bank="water_infrastructure", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now. Write ONE evaluation of the water-use source that names a strength (what "
                       "to trust it for) and a limit (where it falls short).",
                 closer="Naming what a source is good for and where it falls short is what every real source "
                        "evaluation is built on, and you are ready to do it cold. Before you submit, check it "
                        "names both, not a blanket accept or reject.")),
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: the U.S. electricity mix",
             ref="ACC-W910-INFO-LESSON-ENERGYMIX", bank="energy_transition",
             body=("A new source. Read it and, because your job is to name strengths and limits, notice what it "
                   "is strong evidence for and what it cannot tell you. Same strengths-and-limits move, new "
                   "topic. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Evaluate strengths and limits on a NEW source",
             ref="", bank="energy_transition", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="New source. Write ONE evaluation of the electricity-mix source that names a strength and a limit.",
                 closer="Same strengths-and-limits move as the water-use evaluation, new source. Do not give an "
                        "all-or-nothing verdict. Run the 3-question check before you submit.")),
    ],
)

LESSONS = [LESSON]

if __name__ == "__main__":
    ok = True
    for L in LESSONS:
        qc_lesson(L); print(qc_report(L)); print(); ok = ok and L.qc["passed"]
    print(f"{sum(1 for L in LESSONS if L.qc['passed'])}/{len(LESSONS)} PASS")
    sys.exit(0 if ok else 1)
