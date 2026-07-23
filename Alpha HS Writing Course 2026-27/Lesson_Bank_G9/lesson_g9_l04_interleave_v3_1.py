"""
lesson_g9_l06_interleave_v3_1.py  -  G9 KC C.9.01 + C.9.05, ARCHETYPE T2 (sentence). V3.1 INTERLEAVE/REVIEW.

G9 L06, rebuilt to the v3.1 build spec. Teaching point (kept): READ THE VERB to decide which product a task
wants, then write it - "argue"/"should...?" -> an arguable CLAIM (a side + reason); "explain" -> a CONTROLLING
IDEA (a focus that previews the parts, NO side). Interleaves both modes (C.9.01 + C.9.05). Sentence ceiling.
Topics: argue side = four-day-week (was phones); explain side = volcanoes; transfer = animal migration (explain).
Both "arguable claim" and "controlling idea" are defined with cue words. 23 gates. Inline HTML, real lists, no
em dashes, no leaked labels, homogeneous distractor lengths.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">The task <strong>verb</strong> tells you which sentence '
'to write. <strong>Argue</strong> wants a claim with a side; <strong>explain</strong> wants a focus with no side.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: read the verb first</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you write, ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">What is the verb, argue or explain?</li>'
'<li style="margin:2px 0">If argue: did I take a side with a reason?</li>'
'<li style="margin:2px 0">If explain: did I set a focus that previews the parts and takes no side?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">Match the product to the verb, or you answer the wrong question.</div></div>')

# coping-model think-aloud: a writer reads the verb, drafts the WRONG product, catches it, switches.
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer thinking it through (the task: EXPLAIN how a volcano erupts):</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Volcanoes should be studied more because they are '
    'dangerous." Check the verb: the task says EXPLAIN, but I took a side, that is an argue move. Wrong product. '
    'Switch.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "A volcano erupts." Now it takes no side, but it sets '
    'no focus and previews no parts. Add the focus and the stages.</p>'
    '<p style="margin:0"><strong>Final:</strong> "A volcano erupts when pressure from rising magma is released '
    'through the surface in a series of stages." A focus, the parts previewed, no side, that fits EXPLAIN.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "Volcanoes should be studied more because they are dangerous." '
    '(a claim with a side, wrong product for EXPLAIN)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "A volcano erupts when pressure from rising magma is released '
    'through the surface in a series of stages." (a controlling idea, right product)</span></div>'
'</div>')

DECOMPOSE_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#eef2ff;padding:10px 14px;border-bottom:1px solid #c7d2fe;font-size:14px;color:#1f2a44">'
    'Same two verbs, two different products:</div>'
  '<div style="padding:12px 14px">'
    '<div style="margin:0 0 10px">'
      '<span style="display:inline-block;background:#fee2e2;color:#991b1b;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">ARGUE -&gt; CLAIM</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px"><em>"Schools should switch to a four-day week, '
      'because a longer weekend gives students rest."</em> Takes a <strong>side</strong> someone could reject '
      'and adds a <strong>reason</strong>.</div></div>'
    '<div>'
      '<span style="display:inline-block;background:#dcfce7;color:#166534;font-size:11px;font-weight:700;'
      'padding:2px 8px;border-radius:4px">EXPLAIN -&gt; CONTROLLING IDEA</span>'
      '<div style="color:#1f2a44;font-size:14px;margin-top:4px"><em>"A volcano erupts through a series of connected '
      'stages."</em> Sets a <strong>focus</strong> and previews the <strong>parts</strong>, takes <strong>no '
      'side</strong>.</div></div>'
    '<div style="margin-top:10px;color:#0f766e;font-size:13px">The verb decides which one you build.</div>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C901-0006", grade="9-10", lesson_type=2,
    unit="G9 U1 - Claim/controlling-idea + evidence (arguable claim)",
    title="Argue or Explain? Choose the Right Sentence",
    target=("Given a task, decide from the verb whether it wants an argument claim (take a side) or a controlling "
            "idea (set a focus, no side), then write the right product. Written at the sentence. Interleaves "
            "C.9.01 and C.9.05. Trait: Thesis/Purpose."),
    acc_tags=["ACC.W.ARG.1", "CCSS.W.9-10.1a"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.9.01+C.9.05",
                "sot": "icm course-G9.md L06; KC_Map_and_Unit_Arch_G9-12.md (G9 U1)",
                "taught_stimulus": "ACC-W910-FRAME-VOLCANOES + ACC-W910-FRAME-FOURDAYWEEK",
                "transfer_stimulus": "ACC-W910-FRAME-MIGRATION",
                "one_idea": "The task verb decides the product: argue -> claim with a side; explain -> controlling idea, no side.",
                "one_reminder": "Read the verb first; match the product to it.",
                "version_note": ("V3.1 rebuild (hand-authored; the parallel agent stalled). Interleave/review of "
                                 "C.9.01+C.9.05: decode the verb, then write the matching product. Spine + "
                                 "list-teach + coping-model (drafts the wrong product, catches it, switches) + "
                                 "decompose (argue->claim vs explain->controlling idea side by side) + leak-free "
                                 "discrimination + autonomy independent write. Argue topic swapped phones->four-"
                                 "day-week; explain topic volcanoes; transfer migration."),
                "review_provenance": "built to the L01/L02 v3.1 pattern (Fable+Council adjudicated 2026-07-14)"},
    fade_ledger_moves=["decode-the-task-verb", "arguable-claim-vs-fact-vs-opinion", "controlling-idea-vs-claim"],
    slots=[
        Slot("TEACH", "teach_card", "The one idea: read the verb, pick the product",
             body=(ONE_IDEA +
                   "You already know both products. This lesson is about choosing the right one from the task's "
                   "verb:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\">An <strong>arguable claim</strong> means a sentence that takes a "
                   "side someone could disagree with and gives a reason. Build it when the verb is 'argue' or "
                   "'should ... ?'.</li>"
                   "<li style=\"margin:4px 0\">A <strong>controlling idea</strong> means a sentence that sets a "
                   "focus and previews the parts while taking no side. Build it when the verb is 'explain' or "
                   "'describe'.</li></ul>"
                   "The most common mistake is matching the wrong product to the verb: arguing when the task said "
                   "explain, or staying neutral when it said argue. So read the verb first, every time.")),
        Slot("TEACH", "stimulus_display", "Two tasks: a four-day week (argue) and volcanoes (explain)",
             ref="ACC-W910-FRAME-FOURDAYWEEK", bank="four_day_week",
             body=("Here are two tasks side by side. One says argue whether schools should switch to a four-day "
                   "week. The other says explain how a volcano erupts. Same student, two different products. The "
                   "four-day-week framing below is written as an argue prompt, so it invites you to pick a side "
                   "and a reason. You are not writing either one here; you are studying them to see which product "
                   "each verb calls for.")),
        Slot("TEACH", "stimulus_display", "The explain task: how volcanoes erupt",
             ref="ACC-W910-FRAME-VOLCANOES", bank="volcanoes",
             body=("Read this short framing of the volcano topic. Notice the verb is explain, so this task wants a "
                   "focus that previews the parts, not a side.")),
        Slot("MODEL", "discrimination", "Which product does each task call for?",
             ref="", labeled_grade_c=True, bank="four_day_week",
             body=("Read the verb, then pick the sentence that is the RIGHT product. The task: EXPLAIN how a "
                   "volcano erupts. Which sentence fits that verb? "
                   "(A) Studying volcanoes really should matter a lot more to schools than it currently seems to.  "
                   "(B) Volcanoes are honestly one of the most fascinating and exciting topics in all of science.  "
                   "(C) A volcano erupts through a series of connected stages, from rising magma to release.  "
                   "(D) This explanation will be about volcanoes and the different things that happen with them. "
                   "Correct: C. The verb is explain, so the right product is a controlling idea: a focus that "
                   "previews the parts and takes no side. (A) takes a side (an argue move, wrong verb). (B) is a "
                   "bare opinion. (D) only announces the topic; it sets no focus and previews none of the stages, "
                   "so a reader still cannot tell what the explanation will do. Only (C) sets a no-side focus that "
                   "previews the stages.")),
        Slot("MODEL", "discrimination", "Argue task: which sentence is the right product?",
             ref="", labeled_grade_c=True, bank="four_day_week",
             body=("Read the verb, then pick the sentence that is the RIGHT product. The task: ARGUE whether "
                   "schools should switch to a four-day week. An argue task calls for a claim that takes a side "
                   "AND backs it with a reason. Which sentence is that finished product?"),
             choices=[
                 {"id": "A",
                  # COUNCIL FIX (confound): distractor A now carries a connective ('because') on a NEUTRAL,
                  # side-less sentence, so the connective no longer signals the correct answer; the student must
                  # test for a SIDE, not spot 'because'. Mirrors the L01 confound fix.
                  "text": "A four-day school week touches students, teachers, and families in many ways, because "
                          "the schedule shapes how everyone spends their time.",
                  "correct": False,
                  "why": "This has a connective ('because'), but it only links two neutral facts and takes no "
                         "side, so it answers an explain task, not an argue task. The connective is not what "
                         "makes a claim; the side is."},
                 {"id": "B",
                  "text": "Schools should switch to a four-day week.",
                  "correct": False,
                  "why": "This picks a side but gives no reason, so it is only half of an arguable claim."},
                 {"id": "C",
                  "text": "Schools should switch to a four-day week because a longer weekend gives students time "
                          "to rest.",
                  "correct": True,
                  "why": "This takes a side someone could dispute and backs it with a reason, which is exactly "
                         "what an argue task calls for."},
                 {"id": "D",
                  "text": "People make good points on both sides of whether schools should switch to a four-day "
                          "week.",
                  "correct": False,
                  "why": "This names the debate but refuses to commit to a side, so it is not an arguable claim "
                         "at all; an argue task needs you to pick one side."},
             ]),
        Slot("MODEL", "annotated_before_after", "Watch a writer match the product to the verb",
             bank="volcanoes",
             body=("Here is the skill in action. Follow the writer's thinking below. " + COPING_HTML +
                   " Notice what turned the BEFORE into the AFTER: the writer read the verb, saw the first draft "
                   "was the wrong product (a claim with a side for an EXPLAIN task), and switched to a controlling "
                   "idea.")),
        Slot("MODEL", "teach_card", "Decompose it, and get your check tool",
             body=("See the two products side by side so you can tell which verb each one answers, then keep the "
                   "tool you will use to check your own." + DECOMPOSE_HTML + REMEMBER +
                   "When you write, always read the verb first, then build the matching product.")),
        Slot("MODEL", "predict_the_fix", "Is this the right product for the verb?",
             bank="volcanoes",
             body=("Diagnose this draft before the reveal. The task said EXPLAIN how a volcano erupts. The student "
                   "wrote: 'Volcanoes should be protected areas because they are dangerous.' Which single move "
                   "would most improve it? "
                   "(A) switch to a no-side focus that previews the stages  "
                   "(B) add one more reason that volcanoes should be protected  "
                   "(C) make the sentence longer and use more scientific words  "
                   "(D) give an even stronger opinion about how dangerous they are"),
             feedback=("Correct: A. The verb is explain, but the draft takes a side (should be protected, because "
                       "...), which is an argue product, the wrong one. The fix is to switch to a controlling "
                       "idea: a no-side focus that previews the parts ('A volcano erupts through a series of "
                       "stages'). More reasons (B), a longer sentence (C), or a stronger opinion (D) all keep it "
                       "an argue product, still wrong for this verb.")),
        Slot("SUPPORTED", "production_frq", "Decode the verb, then write the right product",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="The task: EXPLAIN how a volcano erupts. The verb is explain, so the product is a "
                       "controlling idea: a focus that previews the parts, no side.",
                 setapart_block=setapart("Copy this frame, then fill in the blank:",
                                         "A volcano erupts ______ [set a focus that previews the stages]."),
                 closer="Set a focus, preview the parts, take no side. Write one sentence, then run the verb "
                        "check.")),
        Slot("MODEL", "diagnosis_frq", "Check it: right product for the verb?",
             ref="", bank="volcanoes", scored=True,
             body=frq_prompt(
                 intro="Run the verb check on this weak draft, then rewrite it into the right product.",
                 setapart_block=setapart("Weak draft to fix:", "Volcanoes should be studied more.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("What is the verb, argue or explain?", "Explain, so I need a controlling idea, not a claim."),
                     ("Is this a no-side focus?", "your call: yes / no"),
                     ("Does it preview the parts?", "your call: yes / no"),
                 ]),
                 closer="Now rewrite the weak draft into one controlling idea that fits EXPLAIN, then name which "
                        "check your rewrite fixed.")),
        Slot("INDEPENDENT", "production_frq", "Choose the product and write it (volcanoes)",
             ref="", bank="volcanoes", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now, no frame. The task: EXPLAIN how a volcano erupts.",
                 closer="Read the verb, decide the product, and write ONE sentence that fits it: a controlling "
                        "idea, a focus that previews the parts, no side. Matching the product to the verb is "
                        "exactly what every real writing task asks for, and you are ready to do it cold. Run the "
                        "verb check before you submit.")),
        Slot("TRANSFER", "stimulus_display", "The topic: animal migration",
             ref="ACC-W910-FRAME-MIGRATION", bank="animal_migration",
             body=("A new topic. Read the short framing. The task will name a verb, and your job is to write the "
                   "product that verb calls for.")),
        Slot("TRANSFER", "production_frq", "Choose the product and write it on a NEW topic",
             ref="", bank="animal_migration", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="New topic. The task: EXPLAIN why some animals migrate.",
                 closer="Read the verb, decide the product, and write ONE sentence that fits it: here, a "
                        "controlling idea, a focus that previews the parts, no side. Run the verb check before you "
                        "submit, and do not slip into taking a side.")),
    ],
)

LESSONS = [LESSON]

if __name__ == "__main__":
    ok = True
    for L in LESSONS:
        qc_lesson(L); print(qc_report(L)); print(); ok = ok and L.qc["passed"]
    print(f"{sum(1 for L in LESSONS if L.qc['passed'])}/{len(LESSONS)} PASS")
    sys.exit(0 if ok else 1)
