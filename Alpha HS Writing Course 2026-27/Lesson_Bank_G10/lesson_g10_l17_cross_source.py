"""
lesson_g10_l17_cross_source.py  -  G10 KC C.10.06, ARCHETYPE T8: CROSS-SOURCE-SYNTHESIS (WEAVE, ceiling essay). V3.1.

G10 L17 (Unit 4, guided), rebuilt to the v3.1 build spec (hand-authored). Teaching point (KEPT): cross-source
integration (X1) - use two or three sources TOGETHER to build ONE point (woven), rather than parking each source
in its own separate chunk (source-by-source). Recycles P5. Practiced at the sentence (write ONE point that uses
both sources). Taught on the school-year set -> transfer to the congestion-pricing set (bank-partitioned).

Preserved EXACTLY from the prior L17: id="ACC-W910-L-G10-C1006-0017", lesson_type=8, kc="C.10.06",
mnemonic_status="proposal", unit, the bound stimuli (SCHOOLYEAR taught -> CONGESTION transfer), rc.staar, and every
production_frq unit= value (unit="sentence"; T8 ceiling is essay, so the sentence grain sits within ceiling).

V3.1 changes vs the prior L17 (both were the failing gates + the spine polish):
  1. FIXED the leaked internal label: the discrimination no longer says "a Grade-C design bet we label as a bet";
     it is a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}] (leaked_internal_label).
  2. FIXED the wall-of-text teach card: the prose block is now a ONE_IDEA callout + real <ul>/<ol> lists of what
     weaving is and the order of work (format_fidelity + the v3.1 "parallel items as a list" rule).
  3. Deterministic FRQ + diagnosis prompts via frq_prompt/setapart/checklist (no "Step 1/2" prose, no "Scored on"
     chrome); coping-model BEFORE/AFTER kept; the reusable check tool (3-question weave check) folded in at first
     use as a real <ol> REMEMBER box.
Own words, no fabricated figures (facts trace to the bound US federal sources), no em dashes. Passes all 23
lesson_contract gates + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Cross-source integration means using two or three '
'sources <strong>together, in the same point</strong>, so their facts meet and back one claim. You do not park '
'each source in its own separate chunk and hope the reader connects them.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: is it woven?</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit a point, reread it and ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Do both sources appear in the SAME point, not in separate sentences?</li>'
'<li style="margin:2px 0">Are the two facts connected, so one meets or answers the other, not just listed side by side?</li>'
'<li style="margin:2px 0">Does that connection build ONE claim?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you submit.</div></div>')

# coping-model BEFORE/AFTER: a source-by-source pair (two summaries side by side) rebuilt into one woven point.
# Contains BOTH a literal BEFORE and AFTER (content_depth). No named person (Timeback stateless rule).
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> source-by-source: one source per chunk</span>'
    '<p style="margin:8px 0 0;font-size:15px">The first source says summer learning loss sets low-income '
    'students back. The second source says a longer school year would cost districts a lot of money. Both are '
    'important points.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The two sources sit in separate sentences. The '
    'reader gets two summaries side by side but never one point built from both.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> woven: both sources back ONE point</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">ONE POINT</span> A longer year is worth its cost: '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">SOURCE 1 MEETS SOURCE 2</span> the summer-slide harm the first source documents lands on '
      'exactly the low-income students the second source grants a longer year would reach, so the money the '
      'second source worries about is aimed straight at the gap the first source describes.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Now the two facts meet in one sentence to build a '
    'single claim (the cost is justified by the harm it targets). That is cross-source integration, not '
    'source-by-source.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1006-0017", grade="9-10", lesson_type=8,
    unit="G10 U4 - Cross-text synthesis (cross-source integration)",
    title="Use Two Sources Together for One Point",
    target=("Integrate sources: use two or three of them TOGETHER to build one point (woven), rather than "
            "giving each source its own separate chunk (source-by-source). Written across a multi-source plan. "
            "Trait: Development (use of sources)."),
    acc_tags=["ACC.W.SRC.1", "CCSS.W.9-10.7"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.06", "sot": "icm course-G10.md L17",
                "taught_stimulus": "ACC-W910-ARG-OPP-LESSON-SCHOOLYEAR",
                "transfer_stimulus": "ACC-W910-ARG-OPP-LESSON-CONGESTION",
                "playbook": "_phase2/playbook_T8_WEAVE.md",
                "template": "v3.1 spine; SYNTHESIS-TIER binds full source sets; UNTIMED (no Timeback timer).",
                "one_idea": "Cross-source integration = use two or three sources together, in one point, so their facts meet and back one claim.",
                "one_reminder": "Weave check: both sources in the SAME point? connected, not listed? build ONE claim?",
                "council": ("T8/WEAVE cross-source rung: introduces X1 (use 2-3 sources together for one point). "
                            "woven-vs-source-by-source discrimination is the Grade-C move (labeled_grade_c in code)."),
                "version_note": ("V3.1 rebuild of L17. FIXED the leaked internal label ('a Grade-C design bet we "
                                 "label as a bet') by moving it out of the discrimination prompt into explicit "
                                 "choices=[]; broke the wall-of-text teach card into a ONE_IDEA callout + real "
                                 "<ul>/<ol> lists (format_fidelity). Deterministic frq_prompt/setapart/checklist "
                                 "bodies (no 'Step 1/2' prose, no 'Scored on' chrome); coping-model BEFORE/AFTER "
                                 "kept; the 3-question weave check folded in at first use as an <ol> REMEMBER box. "
                                 "Preserved id, type 8, kc C.10.06, mnemonic_status=proposal, unit, bound stimuli, "
                                 "rc.staar, and every production_frq unit= value (unit='sentence')."),
                "review_provenance": "built to the G9 L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["cross-source-integration", "woven-not-source-by-source"],
    slots=[
        # ===== TEACH: the one idea + what weaving looks like (list), then the order of work (list) =====
        Slot("TEACH", "teach_card", "The one idea: weave sources, do not list them",
             body=(ONE_IDEA +
                   "You have practiced using sources one at a time. Weaving puts two of them to work in the same "
                   "point. Here is the contrast:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Woven</strong> sounds like: the harm the first source "
                   "documents lands on the very group the second source says the plan would reach. Two facts, one "
                   "point.</li>"
                   "<li style=\"margin:4px 0\"><strong>Source-by-source</strong> sounds like: the first source "
                   "says X. The second source says Y. Two summaries, never connected.</li></ul>"
                   "The trap is the source-by-source list: it reads like a book report, not an argument. The move "
                   "is to make the two facts meet on one claim.")),
        Slot("TEACH", "teach_card", "How to weave, step by step",
             body=("Here is the order of work. Follow it and one point built from two sources assembles itself:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>READ</strong> both sources and find one fact in each that "
                   "touches the same issue.</li>"
                   "<li style=\"margin:4px 0\"><strong>PICK</strong> a single claim those two facts can support "
                   "together.</li>"
                   "<li style=\"margin:4px 0\"><strong>CONNECT</strong>: write one sentence where the fact from "
                   "the first source meets the fact from the second, showing how they relate (one confirms, "
                   "answers, or targets the other).</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: reread, are both sources in the same "
                   "point, connected rather than listed, and do they build one claim?</li></ol>"
                   "You are not summarizing two sources in turn. You are building one point out of both.")),
        Slot("TEACH", "stimulus_display", "Read the source set: a longer school year (both sides)",
             ref="ACC-W910-ARG-OPP-LESSON-SCHOOLYEAR", bank="school_year",
             body=("Read this two-source set on a longer school year. Because your job is to weave, read both and "
                   "look for a point you could build using BOTH at once, a place where one source's fact meets "
                   "the other's (for example, the summer-slide harm one side documents and the cost the other "
                   "side warns about). The texts stay on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + check tool, then discrimination, then predict =====
        Slot("MODEL", "annotated_before_after", "Watch source-by-source become one woven point",
             bank="school_year",
             body=("Here is a source-by-source pair rebuilt into one woven point. Read the BEFORE, then the "
                   "AFTER, and notice both sources used together for a single claim." + BEFORE_AFTER_HTML +
                   " The BEFORE lists two sources in separate sentences. The AFTER makes their facts meet on one "
                   "claim. Weaving the sources is the move." + REMEMBER +
                   "When you build your own point, run this check before you submit.")),
        Slot("MODEL", "discrimination", "Which one weaves the sources?",
             ref="", labeled_grade_c=True, bank="school_year",
             body=("You have watched source-by-source become one woven point. Now spot the target: which of these "
                   "uses the two sources TOGETHER (woven), and which do not? "
                   "(A) The summer-slide harm the first source documents lands on the very low-income students "
                   "the second source grants a longer year would reach, so the added days aim straight at the gap "
                   "the sources describe.  "
                   "(B) The first source reports that summer learning loss keeps setting some students back year "
                   "after year. The second source reports that stretching the year would cost districts a great "
                   "deal of money.  "
                   "(C) The first source explains that summer learning loss builds over the long break, and the "
                   "writer then keeps pulling more and more detail from that same first source without bringing "
                   "the second source into the point at all.  "
                   "(D) Both the first source and the second source talk about the longer school year, and "
                   "together they give the reader plenty of useful information about the whole debate. "
                   "Correct: A. It makes a fact from each source meet on one claim; B lists the two in separate "
                   "sentences, C leans on only one source and never brings the second in, and D mentions both "
                   "but connects no specific facts and builds no claim, so it stays a vague comment."),
             choices=[
                 {"id": "A", "text": "The summer-slide harm the first source documents lands on the very low-income students the second source grants a longer year would reach, so the added days aim straight at the gap the sources describe.",
                  "correct": True,
                  "why": "Correct. A fact from each source meets in one sentence to build a single claim, the cost is justified because it targets the very harm. That is woven."},
                 {"id": "B", "text": "The first source reports that summer learning loss keeps setting some students back year after year. The second source reports that stretching the year would cost districts a great deal of money.",
                  "correct": False,
                  "why": "This is source-by-source. Each source gets its own sentence and the two are never connected on one claim, so it reads like two summaries side by side."},
                 {"id": "C", "text": "The first source explains that summer learning loss builds over the long break, and the writer then keeps pulling more and more detail from that same first source without bringing the second source into the point at all.",
                  "correct": False,
                  "why": "This leans on only one source. Weaving needs a fact from each source meeting on one claim; the second source never enters the point."},
                 {"id": "D", "text": "Both the first source and the second source talk about the longer school year, and together they give the reader plenty of useful information about the whole debate.",
                  "correct": False,
                  "why": "This names both sources but connects no specific fact from either and states no claim. Mentioning that two sources both cover a topic is not weaving them; the facts never meet on one point."},
             ]),
        # SECOND minimal pair: a DIFFERENT confound than the first discrimination. The first tested woven vs
        # separate sentences and woven vs single-source. This one holds BOTH sources in one sentence in every
        # option, so the trap is co-mention (glued with "and", facts never relate) and two-claims (both sources
        # named but each backs a separate reason), not source-by-source spacing. Same taught bank, fresh sentences.
        Slot("MODEL", "discrimination", "Both name two sources: which one actually weaves?",
             ref="", labeled_grade_c=True, bank="school_year",
             body=("Here is a subtler test. All three sentences name BOTH school-year sources, but only one makes "
                   "their facts actually meet on a single claim. Which one weaves? "
                   "(A) The first source reports that a longer year lifts reading scores, and the second source "
                   "reports that it pushes up the district's budget.  "
                   "(B) The reading gains the first source measures come from the very added weeks the second "
                   "source says taxpayers fund, so the spending buys the learning summer would erase.  "
                   "(C) The first source shows a longer year is worth adopting because students remember more, and "
                   "the second source shows it is worth adopting because working families gain reliable childcare, "
                   "so two separate reasons support it.  "
                   "(D) The first source shows a longer year raises reading scores, and the second source agrees "
                   "that a longer year is a good idea, so both sources back the same conclusion. "
                   "Correct: B. Only B makes a fact from each source meet on one claim; A merely joins the two with "
                   "'and,' C splits into two separate reasons instead of one woven point, and D uses only the first "
                   "source's fact while the second just echoes agreement, adding no fact of its own to meet it."),
             choices=[
                 {"id": "A", "text": "The first source reports that a longer year lifts reading scores, and the second source reports that it pushes up the district's budget.",
                  "correct": False,
                  "why": "Both sources sit in one sentence, but they are only joined by 'and,' so the two facts never relate and it stays a list."},
                 {"id": "B", "text": "The reading gains the first source measures come from the very added weeks the second source says taxpayers fund, so the spending buys the learning summer would erase.",
                  "correct": True,
                  "why": "Correct. A fact from each source meets on a single claim, the paid weeks are what produce the gains, so the two build one point together."},
                 {"id": "C", "text": "The first source shows a longer year is worth adopting because students remember more, and the second source shows it is worth adopting because working families gain reliable childcare, so two separate reasons support it.",
                  "correct": False,
                  "why": "Both sources appear, but each backs a separate reason, so the sentence builds two claims rather than weaving into one."},
                 {"id": "D", "text": "The first source shows a longer year raises reading scores, and the second source agrees that a longer year is a good idea, so both sources back the same conclusion.",
                  "correct": False,
                  "why": "Only the first source supplies a fact; the second merely echoes agreement and adds no fact of its own. With nothing from the second source to meet the first, the two facts never connect, so it is not woven."},
             ]),
        Slot("MODEL", "predict_the_fix", "What turns this into cross-source integration?",
             bank="school_year",
             body=("Diagnose before the reveal. A draft reads: 'The first source explains the learning slide. The "
                   "second source explains the cost. Both are important points.' Which single move would most "
                   "improve it? "
                   "(A) connect the two sources on ONE point, showing how the slide and the cost relate, instead "
                   "of listing them separately  "
                   "(B) add a third sentence that brings in a whole new topic, so the paragraph ends up covering "
                   "even more ground on the school year  "
                   "(C) quote each source at greater length, pulling in more of the exact words from the first "
                   "source and then again from the second  "
                   "(D) put the sources in a different order, moving the cost sentence ahead of the "
                   "learning-slide sentence in the draft"),
             feedback=("Correct: A. The draft gives each source its own sentence and only says 'both are "
                       "important,' which is source-by-source. The fix makes them meet: show that the slide the "
                       "first source documents is the very harm the second source's spending would target. More "
                       "sentences (B), more quoting (C), or reordering (D) do not connect the sources on one point.")),

        # ===== SUPPORTED: weave one point (sentence) - the fill-in frame is the highest-value scaffold =====
        Slot("SUPPORTED", "production_frq", "Weave two sources into one point",
             ref="", bank="school_year", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="Weave the two school-year sources into one point before you write it out.",
                 setapart_block=setapart("Fill in this frame:",
                                         "______ (my point) because ______ (a fact from the first source) meets ______ (a fact from the second source) in a way that ______ (why the two build one claim)."),
                 closer="Write ONE point that puts both school-year sources in the service of a single claim: "
                        "connect a fact from each, do not list them in separate sentences.")),
        # COUNCIL FIX (2026-07-24): Option A (later-in-arc), watch-then-do: demo preserved, produce is the graded
        # act. The old diagnosis_frq bundled a watched weave-check demo (pre-answered (q,a) tuple rows) + a fresh
        # woven point + a run-and-name-the-claim tail in one box (unscoreable, wired to no grader, and the (q,a)
        # rows leaked the answers). The coping-model demo is PRESERVED as read-only narration (the three weave
        # checks shown running on the weak point, in plain declarative prose). The student's ONLY graded act is
        # now the fresh woven point; the three checks sit read-only beneath as plain-string reminders; the
        # run-and-name tail is deleted. Stays on the taught source (load balance).
        Slot("MODEL", "diagnosis_frq", "Write a woven point, not source-by-source",
             ref="", bank="school_year", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="First, watch the weave check run on the weak point below. Both sources appear, but in "
                       "separate sentences rather than one point; the two facts are just listed, not connected, "
                       "so the harm and the cost never meet; and no single claim is built from them. A stronger "
                       "version would pull both into one point where the summer-loss harm and the added cost "
                       "relate and build one claim. Now write a fresh woven point of your own.",
                 setapart_block=setapart("Weak point the check was run on:",
                                         "The first source says summer learning loss is a problem. The second source says a longer year costs money.", "red"),
                 checklist_block=checklist(title="Check your point against these (no need to type answers):", rows=[
                     "Do both sources appear in the SAME point?",
                     "Are the two facts connected, not just listed?",
                     "Does the connection build one claim?",
                 ]),
                 closer="Write ONE fresh point from the school-year sources that uses both together, connecting "
                        "a fact from each so they build a single claim rather than sitting in separate sentences. "
                        "Run the three checks above before you submit.")),

        # ===== INDEPENDENT: weave a point cold (sentence ceiling for this grain) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write a woven point on your own",
             ref="", bank="school_year", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now, no frame.",
                 closer="Using the school-year sources, write ONE point that uses both together to build a single "
                        "claim, connected rather than listed. Making two sources meet on one claim is what every "
                        "real multi-source argument is built on, and you are ready to do it cold. Run the weave "
                        "check before you submit.")),

        # ===== TRANSFER: same weave move, a NEW source set (congestion), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source set: congestion pricing (both sides)",
             ref="ACC-W910-ARG-OPP-LESSON-CONGESTION", bank="congestion_pricing",
             body=("Read this new two-source set on congestion pricing, charging drivers a toll to enter a "
                   "crowded downtown at busy hours. Because your job is to weave, read both and find a point you "
                   "could build using BOTH at once, a place where one source's fact meets the other's. The texts "
                   "stay on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Write a woven point on a NEW set",
             ref="", bank="congestion_pricing", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="New set. The task: keep the same weave-two-sources move on congestion pricing.",
                 closer="Using the congestion-pricing sources, write ONE point that uses both together to build a "
                        "single claim, for example that the toll money one source describes can be aimed at the "
                        "very drivers the other source worries cannot afford it. Connect a fact from each source; "
                        "do not list them separately. Run the weave check before you submit.")),
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
