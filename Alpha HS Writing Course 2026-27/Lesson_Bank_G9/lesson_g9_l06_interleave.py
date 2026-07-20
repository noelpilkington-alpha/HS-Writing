"""
lesson_g9_l06_interleave.py  -  G9 KC C.9.01/C.9.05, ARCHETYPE T2: CLAIM-BUILDING (STAND, ceiling=sentence).

G9 course L06. REVIEW lesson interleaving the two Unit-1 products: argument claim (P1) vs controlling idea
(P2), decided by the task verb. REVISED 2026-07-12 to the locked L01 template. Taught frames = FRAME-VOLCANOES
(explain) + FRAME-PHONEBAN (argue); transfer frame = FRAME-MIGRATION (explain, bank-partitioned). rc.staar,
unit="sentence". The student first DECIDES which product the task calls for, then produces it. STAND labeled
proposal; mechanics gated; no coping-model persona; no source markup; no prior-work reference; no em dashes.
Runs QC on execution.
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
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> wrong product for the verb</span>'
    '<p style="margin:8px 0 0;font-size:15px">Task: <i>Argue whether schools should ban phones all day.</i><br>'
    'Draft: "Schools have many different rules about phones during the day."</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The verb is ARGUE, but this takes no side, it just '
    'sets up to explain the rules. On an argue task, a no-side sentence cannot score.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> right product: the verb is argue, so take a side</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">SIDE</span> Schools should ban phones for the full day, '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">REASON</span> because constant alerts pull attention away from learning.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">The verb decided the product: argue means take a '
    'side. Match the product to the verb first, then build it.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C901-0006", grade="9-10", lesson_type=2,
    unit="G9 U1 - Claim/controlling-idea + evidence (interleave review)",
    title="Argue or Explain? Choose the Right Sentence",
    target=("Given a task, decide from the verb whether it wants an argument claim (take a side) or a "
            "controlling idea (set a focus, no side), then write the right one. Written at the sentence. "
            "Trait: Thesis/Purpose."),
    acc_tags=["ACC.W.ARG.1", "ACC.W.INFO.1", "CCSS.W.9-10.1a", "CCSS.W.9-10.2a"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-12",
                "mnemonic_status": "proposal", "kc": "C.9.01+C.9.05", "sot": "icm course-G9.md L06 (interleave)",
                "taught_stimulus": "ACC-W910-FRAME-VOLCANOES",
                "taught_stimulus_2": "ACC-W910-FRAME-PHONEBAN",
                "transfer_stimulus": "ACC-W910-FRAME-MIGRATION",
                "playbook": "_phase2/playbook_T2_STAND.md",
                "revision_note": "Locked L01 template: student register, one teach concept, visual before/after, one discrimination, bound issue_frames.",
                "council": "T2/STAND interleave review (spacing/retrieval): discrimination = which product the task calls for (argue vs explain), keyed off the verb."},
    fade_ledger_moves=["decode-verb-argue-vs-explain", "choose-claim-or-controlling-idea"],
    slots=[
        Slot("TEACH", "teach_card", "The verb tells you which sentence to write",
             body=("Unit 1 taught you two sentence products, and the task verb decides which one a task wants. "
                   "An arguable claim is a sentence that takes a side someone could disagree with, backed by a "
                   "reason; you write one when the verb is argue, persuade, or 'should ... ?'. A controlling "
                   "idea is a sentence that sets a focusing angle on a topic and takes no side; you write one "
                   "when the verb is explain, describe, or inform. The scoring calls whichever one you write "
                   "your thesis or central idea, which is a name for the governing sentence your response "
                   "develops. The mistake this lesson targets: writing the wrong product for the verb, arguing "
                   "on an explain task or explaining on an argue task. So step one is always the same: read the "
                   "verb, decide which product it calls for, then write it.")),
        Slot("TEACH", "stimulus_display", "Two tasks: volcanoes (explain) and phones (argue)",
             ref="ACC-W910-FRAME-VOLCANOES", bank="volcanoes",
             body=("Two short framings, two different verbs. First, an EXPLAIN task: explain how volcanoes form "
                   "and erupt (that framing is here). Second, an ARGUE task: argue whether schools should ban "
                   "phones for the full day (framing in the next slot). As you read, decide which sentence "
                   "product each task calls for.")),
        Slot("TEACH", "stimulus_display", "The argue task: phones in school",
             ref="ACC-W910-FRAME-PHONEBAN", bank="phone_ban",
             body=("Here is the second task's framing: argue whether schools should ban phones for the full "
                   "day. The verb is argue, so this one calls for a side. You only need the topic and the two "
                   "sides.")),
        Slot("TEACH", "discrimination", "Which product does each task call for?",
             ref="", labeled_grade_c=True, bank="phone_ban",
             body=("Sort before you write (spotting the target before producing it, a Grade-C design bet we "
                   "label as a bet, not a proven ingredient). Match each task to the product it calls for. "
                   "Task 1: 'Explain how volcanoes form and erupt.' Task 2: 'Argue whether schools should ban "
                   "phones for the full day.' "
                   "(A) Both tasks call for an arguable claim, since each verb asks you to argue a position someone could dispute.  "
                   "(B) Task 1 calls for a controlling idea (explain, no side); Task 2 calls for an arguable "
                   "claim (argue, take a side).  "
                   "(C) Both tasks call for a controlling idea, since each verb just asks you to lay out a topic with no side.  "
                   "(D) Task 1 calls for an arguable claim (argue, take a side); Task 2 calls for a controlling idea (explain, no side). "
                   "Correct: B. The verb decides: 'explain' wants a controlling idea with no side; 'argue "
                   "whether ... should' wants an arguable claim that takes a side. (D) reverses them, the exact "
                   "mistake this lesson guards against.")),
        Slot("MODEL", "annotated_before_after", "Watch a draft matched to the wrong verb, then fixed",
             bank="phone_ban",
             body=("Here the error is choosing the wrong PRODUCT for the verb, and the fix. Read the BEFORE, "
                   "then the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE wrote a no-side sentence on an argue task. The AFTER matches the verb: argue "
                   "means take a side. The reverse mistake, arguing on an explain task, fails the same way. "
                   "Match the product to the verb first.")),
        Slot("MODEL", "predict_the_fix", "Is this the right product for the verb?",
             bank="volcanoes",
             body=("Diagnose this draft before the reveal. Task: 'Explain how volcanoes form and erupt.' The "
                   "student wrote: 'Volcanoes are the most dangerous natural force and should be taken more "
                   "seriously.' Which single move would most improve it for this task? "
                   "(A) switch to a controlling idea that sets a no-side focus on HOW volcanoes form and erupt, "
                   "since the verb is explain  "
                   "(B) add another reason volcanoes are dangerous, such as the damage eruptions cause to "
                   "nearby towns, to back up the point  "
                   "(C) make the sentence shorter by cutting extra words so it reads more smoothly and gets to "
                   "the point faster  "
                   "(D) name a specific famous volcano, such as Mount St. Helens, so the reader gets a concrete "
                   "example to picture"),
             feedback=("Correct: A. The verb is explain, which calls for a controlling idea with no side, but "
                       "the draft argues a side ('most dangerous ... should be taken more seriously'). That is "
                       "the wrong product for the verb. The fix is to switch to a controlling idea that sets a "
                       "focus on how volcanoes form and erupt. Another reason (B), a shorter sentence (C), or "
                       "naming a volcano (D) all keep the wrong product.")),
        Slot("SUPPORTED", "production_frq", "Decode the verb, then write the right product",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("For the EXPLAIN task on volcanoes ('explain how volcanoes form and erupt'), first name the "
                   "product the verb calls for (a controlling idea, no side). Then finish: 'Volcanoes ______ "
                   "[what happens] through ______ [the process or stages].' Goal: match the verb (a "
                   "controlling idea, no side), set a focus, and preview the parts. Do not argue a side. Write "
                   "one sentence. Scored on Thesis/Purpose.")),
        Slot("MODEL", "diagnosis_frq", "Check it: right product, built right?",
             ref="", bank="volcanoes", scored=True,
             body=("First watch the check run on a weak draft, then run it on a fresh sentence of your own. "
                   "Task: explain how volcanoes form and erupt. Weak draft: 'Volcanoes are amazing and should "
                   "be respected.' Run the check step by step. Step 1, decode: what product does the verb call "
                   "for? Explain, so a controlling idea with no side; this draft argues, so switch products. "
                   "Step 2, focus: does it set a focus on HOW volcanoes work? No, add one. Step 3, no side: "
                   "does it avoid arguing? No, cut the judgment. Now you: for the same explain task, write one "
                   "fresh controlling idea, then run the same checks. For each No, use the fix: decode the verb "
                   "and match the product; set a focus on the process; cut any side. Finish by naming which "
                   "check your sentence still needs most.")),
        Slot("INDEPENDENT", "production_frq", "Choose the product and write it (volcanoes, explain)",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("On your own now. Task: explain how volcanoes form and erupt. First decide from the verb "
                   "which product this calls for, then write ONE sentence of that product. Goal: match the "
                   "verb (explain wants a controlling idea, no side), set a clear focus, and preview the "
                   "parts. Before you submit, check: did I write the product the verb calls for, does it set a "
                   "focus, did I avoid taking a side? If any answer is no, fix it before you submit. Scored on "
                   "Thesis/Purpose.")),
        Slot("TRANSFER", "stimulus_display", "The topic: animal migration",
             ref="ACC-W910-FRAME-MIGRATION", bank="animal_migration",
             body=("Read the short orientation to this new topic. The task will ask you to explain, so decide "
                   "which product that calls for. You only need the topic and its main parts.")),
        Slot("TRANSFER", "production_frq", "Choose the product and write it on a NEW topic",
             ref="", bank="animal_migration", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("New topic. Task: explain how and why animals migrate. Decide from the verb which product "
                   "this calls for, then write ONE sentence of it. Goal: match the verb (explain wants a "
                   "controlling idea, no side), set a focus, and preview the parts. Same decide-then-write "
                   "move as the volcanoes task, new topic. Scored on Thesis/Purpose.")),
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
