"""
lesson_g9_l01_arguable_claim_v2.py  -  G9 KC C.9.01, ARCHETYPE T2 (STAND, sentence ceiling). REWORKED SPINE.

V2 rework (Noel 2026-07-14): every lesson must HAMMER one core idea + one core reminder, and run the
teach -> model -> DECOMPOSE-the-model spine as the dominant experience, then ONE discrimination check and a
lean set of scored writes. This is the same content/scope as v1 (arguable claim = SIDE + REASON; decode the
verb) but restructured to that spine. New beat vs v1 = an explicit DECOMPOSE-the-model card ("how did the
writer build this claim, part by part, against the skill"). Dense definitional prose is replaced by the two
authored inline-SVG diagrams (S01 fact/opinion/claim, S05 fact->claim), per visual-design-protocol Track A.
Redundant 4th write dropped (v1 had supported+diagnosis+independent+transfer = 4 scored; v2 = diagnosis +
independent + transfer = 3). ONE discrimination retained (discriminate-before-produce, load-bearing).

  - KC: C.9.01 (gateway) | unit: G9 U1 | funnel: argument | archetype: T2 (STAND) | ceiling: sentence
  - ONE IDEA: an arguable claim takes a SIDE and gives a REASON (not a fact, not a bare opinion).
  - ONE REMINDER: SIDE + REASON -> the 3-question test (side? could someone disagree? reason?).
  - acc: [ACC.W.ARG.1] ccss: [W.9-10.1a] | rc.staar
  - taught: phone_ban -> transfer: school_lunch (partitioned bank)

Timeback-safe: all HTML inline-styled (no <style>/JS/<table>-in-<p>); diagrams are inline <svg> (verified by
l01_diagrams.verify_svg). No near-peer coping model; no source markup; no prior-work reference; no em dashes.
Runs the QC harness on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report

# ---- the two hammered callouts, rendered as inline-styled panels (dominant, repeated) --------------------
ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">An arguable claim takes a '
'<strong>SIDE</strong> and gives a <strong>REASON</strong>. A fact or a bare opinion is not a claim.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Remember: SIDE + REASON</div>'
'<div style="color:#1f2a44;font-size:14px;margin-top:2px">Before you submit any claim, run the 3-question test: '
'<strong>1.</strong> Does it take a side?   <strong>2.</strong> Could someone disagree?   '
'<strong>3.</strong> Is there a reason?  If any answer is no, it is not an arguable claim yet.</div></div>')

# ---- the worked before/after (BOTH examples inline, in the annotated_before_after slot) -----------------
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> just a fact, not a claim</span>'
    '<p style="margin:8px 0 0;font-size:15px">"Students use phones during the school day."</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">Nothing to argue. It is true, nobody disputes it, '
    'and no reason is attached.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> an arguable claim, built in two moves</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">SIDE</span> Schools should ban phones for the whole day, '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">REASON</span> because constant alerts pull attention away from learning.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same topic, but now it takes a SIDE and gives a '
    'REASON, so someone could disagree with it. That is what makes it an arguable claim.</p>'
  '</div>'
'</div>')

# ---- the modelled claim, decomposed part-by-part (the NEW spine beat) -----------------------------------
DECOMPOSE_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#f0fdf4;padding:10px 14px;border-bottom:1px solid #bbf7d0;font-size:15px">'
    'The finished claim: <em>"Schools should ban phones all day, because constant alerts pull attention away from learning."</em></div>'
  '<div style="padding:12px 14px">'
    '<div style="margin:0 0 10px">'
      '<span style="display:inline-block;background:#dbeafe;color:#1e3a8a;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">MOVE 1 - SIDE</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px"><strong>"Schools should ban phones all day"</strong> '
      'The writer picks a position on the exact question the task asked (a full-day ban). It is a "should" '
      'sentence someone could reject, not a neutral fact. That is what makes it arguable.</div></div>'
    '<div>'
      '<span style="display:inline-block;background:#fef9c3;color:#854d0e;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">MOVE 2 - REASON</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px">"...<strong>because constant alerts pull attention '
      'away from learning</strong>." The writer attaches one because-reason so the side has support. Drop this '
      'clause and only the bare side is left, which a reader cannot yet weigh.</div></div>'
    '<div style="margin-top:10px;color:#0f766e;font-size:13px">Two moves, welded with <strong>because</strong>. '
    'That is the whole construction. Every claim you write is built the same way.</div>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C901-0001", grade="9-10", lesson_type=2,
    unit="G9 U1 - Claim/controlling-idea + evidence (arguable claim)",
    title="Take a Side Someone Could Argue With",
    target=("Write one arguable claim: read what the task asks, take a clear side, and give a reason. A claim "
            "is arguable when someone could disagree with it and you can back it up. Written at the sentence. "
            "Trait: Thesis/Purpose."),
    acc_tags=["ACC.W.ARG.1", "CCSS.W.9-10.1a"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-14",
                "mnemonic_status": "proposal",
                "kc": "C.9.01", "sot": "icm course-G9.md L01; KC_Map_and_Unit_Arch_G9-12.md (G9 U1)",
                "brief": "icm/stages/06-authoring/output/brief_G9_L01.md",
                "taught_stimulus": "ACC-W910-ARG-LESSON-PHONEBAN",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-SCHOOLLUNCH",
                "playbook": "_phase2/playbook_T2_STAND.md",
                "one_idea": "An arguable claim takes a SIDE and gives a REASON (not a fact, not a bare opinion).",
                "one_reminder": "SIDE + REASON -> 3-question test (side? disagree? reason?).",
                "revision_note": ("V2 spine rework (Noel 2026-07-14): hammer ONE idea + ONE reminder as repeated "
                                  "callouts; run teach -> model -> DECOMPOSE-the-model as the dominant experience; "
                                  "NEW explicit decompose card (part-by-part authorial choices vs the skill); dense "
                                  "prose replaced by S01/S05 inline-SVG diagrams; decode-the-verb folded into one "
                                  "line (no standalone card); dropped the redundant 4th scored write (kept diagnosis "
                                  "+ independent + transfer). ONE discrimination retained."),
                "council": ("Teach the fact/opinion/claim distinction visually (S01), then model the fact->claim "
                            "transform (S05), then DECOMPOSE the finished claim into SIDE + REASON authorial moves; "
                            "one Grade-C discrimination; predict-the-fix; scaffolded self-diagnosis; independent + "
                            "transfer writes on partitioned banks. Sentence ceiling flat.")},
    fade_ledger_moves=["decode-the-task-verb", "arguable-claim-vs-fact-vs-opinion", "side-plus-reason"],
    slots=[
        # ============ TEACH: one idea, taught visually (S01 diagram = slot 1) + one reminder ============
        Slot("TEACH", "teach_card", "The one idea: take a SIDE, give a REASON",
             body=(ONE_IDEA +
                   "Three kinds of sentence look alike but do different jobs, so keep them apart. A "
                   "<strong>FACT</strong> is something you can check and nobody argues about "
                   "('Most US schools limit phone use during the day'). An <strong>OPINION</strong> is a bare "
                   "preference with nothing behind it ('Phones are annoying'). An <strong>arguable claim</strong> "
                   "means a sentence that takes a side someone could disagree with AND backs it with a reason "
                   "('Schools should ban phones all day, because alerts pull focus from learning'). That is the "
                   "sentence an argument is built on. (Scoring sometimes calls this a "
                   "<dfn class=\"tb-glossary-term\" data-catalog-idref=\"def-thesis\" "
                   "title=\"Thesis: another name for the arguable claim your whole response defends. You do not "
                   "need it to finish this lesson.\">thesis</dfn>, but you do not need that word to do today's "
                   "task.) "
                   "One quick habit before any of this: read the task verb. 'Argue' or 'should schools ... ?' "
                   "means take a side; 'explain' means lay out how something works with no side. Today the task "
                   "asks you to argue, so your job is to take a side and give a reason." + REMEMBER)),
        Slot("TEACH", "stimulus_display", "The debate: phones in school",
             ref="ACC-W910-FRAME-PHONEBAN", bank="phone_ban",
             body=("Read the short framing of the debate, then you will practice spotting a real claim before you "
                   "write one. You only need the topic and the two sides.")),
        Slot("TEACH", "discrimination", "Which one is the arguable claim?",
             ref="", labeled_grade_c=True, bank="phone_ban",
             body=("Spot the target before you build it (a Grade-C design bet, labeled as a bet). Which sentence "
                   "is an arguable claim, not a fact and not a bare opinion? "
                   "(A) Most US public schools already have written rules limiting phone use during the school day.  "
                   "(B) Phones are one of the most irritating, annoying parts of the entire school day for everyone.  "
                   "(C) Schools should ban phones all day, because constant alerts pull attention from learning. "
                   "Correct: C. (A) is a FACT you can check and nobody disputes. (B) is a bare OPINION with no "
                   "reason. Only (C) takes a side someone could disagree with and gives a reason.")),

        # ============ MODEL + DECOMPOSE: the modelled claim (S05 = slot 4), then break it down ============
        Slot("MODEL", "annotated_before_after", "Model: watch a fact become an arguable claim",
             bank="phone_ban",
             body=("Here is the skill in action. The writer starts from a plain fact and rebuilds it into an "
                   "arguable claim by adding just two things: a SIDE and a REASON. Read the before, then the "
                   "after, and watch what got added. " + BEFORE_AFTER_HTML +
                   " The before only restates something true. The after takes a side someone could reject and "
                   "attaches a reason. Adding the side and the reason is the whole move.")),
        Slot("MODEL", "teach_card", "Decompose it: how the writer built the claim",
             body=("Now take the finished claim apart to see how it was constructed, piece by piece, against the "
                   "skill. Every arguable claim is welded from the same two moves." + DECOMPOSE_HTML +
                   "When you write your own in a moment, build it the same way: state the side first, then weld a "
                   "reason on with 'because.'")),
        Slot("MODEL", "predict_the_fix", "Is this an arguable claim, and if not, what fixes it?",
             bank="phone_ban",
             body=("Diagnose this draft before the reveal. The task asked the student to argue whether schools "
                   "should ban phones for the full day. The student wrote: 'Phone rules in schools have changed a "
                   "lot over the years.' Which single move would most improve it? "
                   "(A) take a side on the full-day ban and add a reason  "
                   "(B) add one more fact about how the phone rules changed  "
                   "(C) make the sentence longer and use more formal words  "
                   "(D) describe how phones work during the school day"),
             feedback=("Correct: A. The draft states a fact nobody disputes and never answers the question, "
                       "whether to ban phones all day, so it is not an arguable claim. The fix is the two moves "
                       "you just decomposed: take a side, then weld on a reason ('Schools should ban phones all "
                       "day, because alerts pull focus from learning'). Another fact (B), a longer sentence (C), "
                       "or explaining how phones work (D) never turn a fact into a claim.")),

        # ============ SUPPORTED: run the reminder on a weak draft, then on your own ============
        Slot("SUPPORTED", "diagnosis_frq", "Check a claim with the 3 questions, then your own",
             ref="", bank="phone_ban", scored=True,
             body=("First watch the 3-question checklist run on a weak draft, then run it on a fresh claim of "
                   "your own. Weak draft: 'Lots of schools have phone rules now.' Step 1, side: does it take a "
                   "side on the full-day ban? No, it reports a fact, so pick a side. Step 2, could someone "
                   "disagree? No, nobody argues with it. Step 3, reason: is there a because-reason? No, add one. "
                   "Now you: write one fresh claim on the phone task, then run the same three questions on it. For "
                   "each No, use the fix: pick a side, word it so someone could disagree, add 'because ____.' "
                   "Finish by naming which question your sentence still needs most.")),

        # ============ INDEPENDENT: one arguable claim, self-checked with the reminder ============
        Slot("INDEPENDENT", "production_frq", "Write one arguable claim on the phone task",
             ref="", bank="phone_ban", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("On your own. The task: argue whether schools should ban phones for the whole day. Write ONE "
                   "arguable claim sentence, built from the two moves: a SIDE, then a REASON welded on with "
                   "'because.' Before you submit, run the 3-question test (side? could someone disagree? reason?) "
                   "and fix any No. Do not restate a fact or drop a bare opinion. Scored on Thesis/Purpose.")),

        # ============ TRANSFER: same two moves, new topic, partitioned bank ============
        Slot("TRANSFER", "stimulus_display", "The debate: free school meals",
             ref="ACC-W910-FRAME-SCHOOLLUNCH", bank="school_lunch",
             body=("A new debate. Read the short framing, then take a side. Same two moves as the phone claim, new "
                   "topic. You only need the topic and the two sides.")),
        Slot("TRANSFER", "production_frq", "Write an arguable claim on a NEW topic",
             ref="", bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("New topic. The task: argue whether schools should give free meals to all students. Write ONE "
                   "arguable claim sentence using the same construction: SIDE, then REASON welded with 'because.' "
                   "Run the 3-question test before you submit. Do not restate a fact or drop a bare opinion. "
                   "Scored on Thesis/Purpose.")),
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
