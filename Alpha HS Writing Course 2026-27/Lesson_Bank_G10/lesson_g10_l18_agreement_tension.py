"""
lesson_g10_l18_agreement_tension.py  -  G10 KC C.10.06, TYPE 8: CROSS-SOURCE-SYNTHESIS (WEAVE, ceiling essay). V3.1.

G10 course L18 (Unit 4, guided), rebuilt to the v3.1 build spec (hand-authored). Teaching point (KEPT): name
agreement / tension (the X2 move): state where the sources AGREE and where they CONFLICT, rather than reporting
each in turn. Recycles X1. KC C.10.06. SYNTHESIS-TIER binds full source sets. Taught: congestion (set) ->
transfer: daylight_saving (set, partitioned). Writes stay at the sentence (the early synthesis move is practiced
at the sentence; unit ladder non-decreasing, well within the type-8 essay ceiling).

Preserved EXACTLY from the prior L18: id="ACC-W910-L-G10-C1006-0018", lesson_type=8, kc="C.10.06",
mnemonic_status="proposal", unit, the bound stimuli (CONGESTION taught -> DST transfer), and every
production_frq unit= value (all "sentence"). WEAVE=proposal. No named coping-model persona (Timeback stateless);
no source markup; no prior-work reference; no em dashes.

V3.1 changes vs the prior L18 (the two failing gates + the spine polish):
  1. FIXED the leaked internal label: the discrimination no longer says "a Grade-C design bet we label as a bet";
     it is a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}] (leaked_internal_label).
  2. FIXED the wall-of-text teach card: the prose block is now a ONE_IDEA callout + real <ul>/<ol> lists of the
     parts and the order of work (format_fidelity, and the v3.1 "parallel items as a list" rule).
  3. Deterministic FRQ + diagnosis prompts via frq_prompt/setapart/checklist (no "Step 1/2" prose, no "Scored
     on ..." chrome); coping-model before/after kept + upgraded to First try / Second try / Final; the reusable
     check tool folded in at first use as a real <ol> REMEMBER box.
Own words, faithful to the bound sources, no fabricated figures, no em dashes. Passes all 23 gates + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Strong synthesis <strong>names the relationship</strong> '
'between the sources: where they agree and where they clash. It does not just report one source and then the '
'other and leave the reader to guess how they connect.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the relationship check</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, reread your sentence and ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does it name where the sources AGREE (not just report one of them)?</li>'
'<li style="margin:2px 0">Does it name where they CLASH (not just say "they differ")?</li>'
'<li style="margin:2px 0">Does it pinpoint the real point of disagreement?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you submit.</div></div>')

# coping-model think-aloud: a writer DRAFTS a plain list (First try), runs the relationship check, catches that
# the relationship is unnamed, tries a vague "they disagree" (Second try), catches that it is still not specific,
# and lands a named tension (Final). Contains a LITERAL BEFORE and AFTER (content_depth). Faithful to the bound
# congestion source: both passages accept downtown congestion is a real problem and clash on who pays / fairness
# (the con source frames "the traffic clears" as the supporters' claim, so the shared point is the problem, not
# that tolls work).
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> First try: reports each source, never names how they relate</span>'
    '<p style="margin:8px 0 0;font-size:15px">The pro source says tolls reduce downtown traffic. The con source '
    'says tolls burden low-income drivers who pay the same daily charge.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">I run the relationship check. Two true reports, but I '
    'never told the reader whether the sources agree, disagree, or where exactly they clash. Not named yet.</p>'
  '</div>'
  '<div style="background:#fffbeb;padding:12px 14px;border-bottom:1px solid #fde68a">'
    '<span style="display:inline-block;background:#d97706;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">SECOND TRY</span>'
    '<span style="color:#b45309;font-size:13px;font-weight:600"> closer, but still vague</span>'
    '<p style="margin:8px 0 0;font-size:15px">The two sources disagree about congestion pricing.</p>'
    '<p style="margin:6px 0 0;color:#b45309;font-size:13px">Better, but "disagree" names no specific point. I '
    'still have not said where they agree or exactly what they clash over. Pinpoint the real issue.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> Final: names the agreement and the tension</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">RELATIONSHIP NAMED</span> Both sources agree that downtown congestion is a real problem; '
      'they clash on who would bear the cost of a toll, so the real disagreement is about fairness, not whether '
      'the traffic problem is real.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Now the reader is told exactly where the sources '
    'agree (congestion is a real problem) and where they clash (who pays). Naming the relationship is the move.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1006-0018", grade="9-10", lesson_type=8,
    unit="G10 U4 - Cross-text synthesis (name agreement and tension)",
    title="Name Where the Sources Agree and Where They Clash",
    target=("State the relationship between sources: where they AGREE and where they CONFLICT, rather than "
            "reporting each in turn. Written across a multi-source plan. Trait: Development (use of sources)."),
    acc_tags=["ACC.W.SRC.1", "CCSS.W.9-10.7"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.06", "sot": "icm course-G10.md L18",
                "taught_stimulus": "ACC-W910-ARG-OPP-LESSON-CONGESTION",
                "transfer_stimulus": "ACC-W910-ARG-OPP-LESSON-DST",
                "playbook": "_phase2/playbook_T8_WEAVE.md",
                "template": "v3.1 spine; SYNTHESIS-TIER binds full source sets; writes at the sentence.",
                "one_idea": "Strong synthesis names the relationship between sources (where they agree, where they clash).",
                "one_reminder": "Relationship check: names where they agree? names where they clash? pinpoints the real issue?",
                "council": ("T8/WEAVE agreement/tension rung: introduces X2 (name where sources agree or conflict). "
                            "relationship-named-vs-listed discrimination labeled Grade-C. WEAVE=proposal."),
                "version_note": ("V3.1 rebuild of L18. FIXED the leaked internal label ('a Grade-C design bet we "
                                 "label as a bet') by moving the choices to explicit choices=[] and removing the "
                                 "jargon from student text; broke the wall-of-text teach card into a ONE_IDEA "
                                 "callout + real <ul>/<ol> lists (format_fidelity). Deterministic "
                                 "frq_prompt/setapart/checklist bodies (no 'Step 1/2' prose, no 'Scored on' "
                                 "chrome); coping-model upgraded to First try / Second try / Final; the "
                                 "relationship check folded in at first use as a real <ol> REMEMBER box. Preserved "
                                 "id, type 8, kc C.10.06, mnemonic_status=proposal, unit, bound stimuli, and every "
                                 "production_frq unit= value (all sentence)."),
                "review_provenance": "built to the G9 L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["name-agreement-tension", "state-the-relationship"],
    slots=[
        # ===== TEACH: the one idea + what a relationship is (list), then the order of work (list) =====
        Slot("TEACH", "teach_card", "The one idea: relate the sources, do not just report them",
             body=(ONE_IDEA +
                   "To synthesize means to combine several sources into one argument. The move today is to name "
                   "how the sources relate. There are two parts to name:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Agreement</strong>: the point the sources both accept, even "
                   "if they take opposite sides overall.</li>"
                   "<li style=\"margin:4px 0\"><strong>Tension</strong>: the exact point where they clash, and the "
                   "real disagreement underneath it.</li></ul>"
                   "The trap is a list of separate reports (source A says this; source B says that) that leaves "
                   "the reader to guess whether the sources support each other, contradict each other, or "
                   "disagree on only one narrow point. Naming the relationship does that thinking for the reader.")),
        Slot("TEACH", "teach_card", "How to name the relationship, step by step",
             body=("Here is the order of work. Follow it and one relationship sentence assembles itself:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>READ BOTH</strong> sources with one question in mind: how "
                   "do they relate?</li>"
                   "<li style=\"margin:4px 0\"><strong>FIND THE AGREEMENT</strong>: the fact or point both "
                   "sources accept.</li>"
                   "<li style=\"margin:4px 0\"><strong>FIND THE CLASH</strong>: the exact point where they part "
                   "ways.</li>"
                   "<li style=\"margin:4px 0\"><strong>PINPOINT</strong> the real disagreement underneath the "
                   "clash.</li>"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: reread and make sure the sentence names "
                   "the agreement, names the clash, and pinpoints the real issue.</li></ol>"
                   "Often two sources agree on the facts and differ only on what to do about them, and naming "
                   "that is the whole insight.")),
        Slot("TEACH", "stimulus_display", "Read the source set: congestion pricing (both sides)",
             ref="ACC-W910-ARG-OPP-LESSON-CONGESTION", bank="congestion_pricing",
             body=("Read this two-source set on congestion pricing (whether cities should charge tolls to drive "
                   "downtown at busy hours). Because your job is to name the RELATIONSHIP, read both and ask: "
                   "where do they agree, and where exactly do they clash? The texts stay on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model First/Second/Final + the check tool, then the check items =====
        Slot("MODEL", "annotated_before_after", "Watch a list become a named tension",
             bank="congestion_pricing",
             body=("Here is a writer turning a source-by-source list into a named tension. Read the BEFORE (a "
                   "first try), watch the check run, and read the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE reports each source. The AFTER names where they agree and where they clash, and "
                   "pinpoints the real issue. Naming the relationship is the move." + REMEMBER +
                   "When you write your own, run this same relationship check before you submit.")),
        Slot("MODEL", "discrimination", "Which one names the relationship?",
             ref="", labeled_grade_c=True, bank="congestion_pricing",
             body=("You have watched a list become a named tension. Now spot the target: which sentence NAMES "
                   "the relationship between the sources, and which two do not? "
                   "(A) The first source says that tolls cut downtown traffic, and the second source says that tolls burden low-income drivers, so the two sources clearly disagree with one another about congestion pricing overall.  "
                   "(B) Both sources agree that downtown congestion is a real problem, but they clash on who should pay for a toll, so the real disagreement is about fairness rather than whether the traffic problem is real.  "
                   "(C) The first source is much longer and packs in far more detail than the second one, so it gives the reader the fuller and far more trustworthy picture of what these tolls actually do downtown.  "
                   "(D) Both sources agree that a toll is unfair to drivers, so there is really no disagreement between the two of them at all. "
                   "Correct: B. It names where the sources agree (congestion is a real problem) and where they clash (who pays), "
                   "pinpointing the real issue; A only lists the two reports and slaps on 'disagree' without "
                   "saying where, C compares the sources' length, which is not their relationship, and D invents "
                   "a shared position the sources do not hold, erasing the real clash instead of naming it."),
             choices=[
                 {"id": "A", "text": "The first source says that tolls cut downtown traffic, and the second source says that tolls burden low-income drivers, so the two sources clearly disagree with one another about congestion pricing overall.",
                  "correct": False,
                  "why": "This lists the two reports and adds a bare 'disagree.' It never names where they agree or the exact point they clash over."},
                 {"id": "B", "text": "Both sources agree that downtown congestion is a real problem, but they clash on who should pay for a toll, so the real disagreement is about fairness rather than whether the traffic problem is real.",
                  "correct": True,
                  "why": "Correct. It names the agreement (congestion is a real problem), names the clash (who pays), and pinpoints the real issue (fairness)."},
                 {"id": "C", "text": "The first source is much longer and packs in far more detail than the second one, so it gives the reader the fuller and far more trustworthy picture of what these tolls actually do downtown.",
                  "correct": False,
                  "why": "This compares the length of the sources. Length is not the relationship between their ideas, so nothing is named."},
                 {"id": "D", "text": "Both sources agree that a toll is unfair to drivers, so there is really no disagreement between the two of them at all.",
                  "correct": False,
                  "why": "This invents an agreement the sources do not share: the pro source does not call the toll unfair. Manufacturing a fake consensus erases the real clash over who pays instead of naming it."},
             ]),
        # SECOND minimal pair, DIFFERENT confound than the first: the first pair tested named-relationship vs.
        # bare list vs. off-target (length). This one tests a FULL relationship (agreement + clash + real issue)
        # against sentences that name only ONE HALF (agreement only, or clash only). Fresh sentences; correct
        # option (B) is not the lone longest (the clash-only distractor C is longest).
        Slot("MODEL", "discrimination", "Which one names both the agreement and the clash?",
             ref="", labeled_grade_c=True, bank="congestion_pricing",
             body=("Naming the relationship means naming BOTH where the sources agree AND where they clash. Which "
                   "sentence below does both, and which two name only one half? "
                   "(A) Both sources agree that downtown gridlock wastes commuters' time and the city's money, and they treat that shared worry as the reason the toll question is worth debating at all.  "
                   "(B) Both sources agree that downtown gridlock is a genuine problem, but they clash over whether a flat daily toll is a fair fix, so the real split is about fairness, not the traffic itself.  "
                   "(C) Both sources clash over the flat daily toll, since the first source treats it as a fair price that every driver should pay for smoother streets while the second treats it as an unfair burden on low-income commuters.  "
                   "(D) Both sources agree downtown gridlock is a real problem, and they clash over the flat daily toll, though what deeper issue that clash comes down to is left for the reader to work out. "
                   "Correct: B. It names the agreement (downtown gridlock is a real problem), the clash (whether a "
                   "flat toll is fair), and the real issue underneath (fairness); A names only the shared worry and "
                   "never reaches the clash, C names only the clash and leaves out the common ground, and D names "
                   "the agreement and the clash but stops short of pinpointing the real disagreement."),
             choices=[
                 {"id": "A", "text": "Both sources agree that downtown gridlock wastes commuters' time and the city's money, and they treat that shared worry as the reason the toll question is worth debating at all.",
                  "correct": False,
                  "why": "This names only the shared worry and never says where the two sources part ways, so half the relationship is missing."},
                 {"id": "B", "text": "Both sources agree that downtown gridlock is a genuine problem, but they clash over whether a flat daily toll is a fair fix, so the real split is about fairness, not the traffic itself.",
                  "correct": True,
                  "why": "Correct. It names the agreement, names the clash over a flat toll, and pinpoints the real issue of fairness."},
                 {"id": "C", "text": "Both sources clash over the flat daily toll, since the first source treats it as a fair price that every driver should pay for smoother streets while the second treats it as an unfair burden on low-income commuters.",
                  "correct": False,
                  "why": "This names only the clash and leaves out the common ground both sources accept, so the shared point is missing."},
                 {"id": "D", "text": "Both sources agree downtown gridlock is a real problem, and they clash over the flat daily toll, though what deeper issue that clash comes down to is left for the reader to work out.",
                  "correct": False,
                  "why": "This names the agreement and the clash but stops there, leaving the reader to figure out the real issue. Naming the relationship means pinpointing that underlying disagreement (fairness), not handing that last step back to the reader."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this pair of reports most need?",
             bank="congestion_pricing",
             body=("Diagnose before the reveal. A draft reads: 'The first source supports tolls. The second "
                   "source opposes them. They have different views.' Which single move would most improve it? "
                   "(A) name exactly where the sources agree and where they clash, instead of just saying they differ  "
                   "(B) add a note telling the reader which of the two sources happens to be longer and packs in more detail  "
                   "(C) add more direct quotations from each of the two sources so the reader can see exactly what each one says  "
                   "(D) decide which one of the two sources is right and then argue at length that the other one is simply wrong"),
             feedback=("Correct: A. 'They have different views' names no specific relationship. The fix pinpoints "
                       "it: the sources may agree downtown congestion is a real problem but clash on fairness, so "
                       "the disagreement is narrower than 'support versus oppose.' Source length (B), more quotes "
                       "(C), or picking a winner (D) do not name where the sources agree and clash.")),

        # ===== SUPPORTED: name the relationship with a fill-in FRAME (the highest-value scaffold) =====
        Slot("SUPPORTED", "production_frq", "Name the agreement and the tension",
             ref="", bank="congestion_pricing", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="Using the congestion-pricing set, write ONE sentence that names the relationship between "
                       "the two sources.",
                 setapart_block=setapart("Fill in this frame:",
                                         "The sources agree that ______, but they clash on ______ so the real disagreement is about ______."),
                 closer="State where the sources agree, where they conflict, and the real issue underneath. Do "
                        "not just report each source in turn.")),
        # COUNCIL FIX (2026-07-24): Option A (later-in-arc), watch-then-do: demo preserved, produce is the graded
        # act. The old diagnosis_frq bundled a watched relationship-check demo (pre-answered (q,a) tuple rows) +
        # a fresh sentence + a run-and-name-the-real-issue tail in one box (unscoreable, wired to no grader, and
        # the (q,a) rows leaked the answers). The coping-model demo is PRESERVED as read-only narration (the
        # three relationship checks shown running on the weak draft, in plain declarative prose). The student's
        # ONLY graded act is now the fresh sentence; the three checks sit read-only beneath as plain-string
        # reminders; the run-and-name tail is deleted. Stays on the taught source (load balance).
        Slot("MODEL", "diagnosis_frq", "Name the relationship, do not just list the sides",
             ref="", bank="congestion_pricing", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="First, watch the relationship check run on the weak draft below. It names no point the "
                       "sources AGREE on, only that one is for tolls and one is against; 'for and against' is not "
                       "a specific CLASH; and it never pinpoints the real disagreement. A stronger version would "
                       "name the shared point (both accept downtown congestion is a real problem), the exact "
                       "clash (who pays), and the real issue underneath (fairness, not whether tolls work). Now "
                       "write a fresh sentence of your own that names all three.",
                 setapart_block=setapart("Weak draft the check was run on:",
                                         "One source is for tolls and one is against.", "red"),
                 checklist_block=checklist(title="Check your sentence against these (no need to type answers):", rows=[
                     "Does it name where the sources AGREE?",
                     "Does it name where they CLASH (a specific point, not just for-and-against)?",
                     "Is the real disagreement underneath pinpointed?",
                 ]),
                 closer="Write ONE fresh sentence about the congestion-pricing set that names where the sources "
                        "agree, names the exact point where they clash, and pinpoints the real issue underneath. "
                        "Run the three checks above before you submit.")),

        # ===== INDEPENDENT: name the relationship on your own (no frame) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Name agreement and tension on your own",
             ref="", bank="congestion_pricing", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now, no frame. Using the congestion-pricing set, write ONE sentence that names "
                       "the relationship between the sources.",
                 closer="Name where the sources agree, name where they clash, and pinpoint the real "
                        "disagreement. Then run the relationship check and fix any part that fails. Naming the "
                        "relationship is what every real piece of synthesis is built on, and you are ready to do "
                        "it cold.")),

        # ===== TRANSFER: same name-the-relationship move, a NEW set (daylight saving), partitioned bank =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source set: daylight saving (both sides)",
             ref="ACC-W910-ARG-OPP-LESSON-DST", bank="daylight_saving",
             body=("Read this new two-source set on daylight saving (whether the country should stop the "
                   "twice-yearly clock change and keep one clock). Because your job is to name the relationship, "
                   "read both and ask where they agree and where they clash. The texts stay on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Name agreement and tension on a NEW set",
             ref="", bank="daylight_saving", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="New set. Using the daylight-saving sources, write ONE sentence naming the relationship "
                       "between them.",
                 closer="Name where they agree, name where they clash, and pinpoint the real disagreement (for "
                        "example, both may accept the twice-yearly switch is disruptive but clash on which fixed "
                        "clock to keep). Same name-the-relationship move as the congestion set, a new topic. Run "
                        "the relationship check before you submit.")),
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
