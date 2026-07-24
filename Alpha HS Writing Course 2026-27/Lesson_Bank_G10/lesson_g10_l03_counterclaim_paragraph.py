"""
lesson_g10_l03_counterclaim_paragraph.py  -  G10 KC C.10.01, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD, ceiling essay). V3.1.

Rebuild of the pre-v3.1 lesson to the v3.1 lesson-build standard (icm/_config/v3_1-lesson-build-spec.md), using
G9 L17 v3.1 as the structural exemplar. Teaching point is UNCHANGED: build the counterargument into a full
paragraph, state your POSITION, fairly CONCEDE the counterclaim, then ANSWER it with evidence and reasoning (not
just a repeat of the claim). KC C.10.01. Bound stimuli kept: SCHOOLYEAR (full opposing-pair source, taught) ->
CONGESTION (full opposing-pair source, transfer, partitioned). Preserved verbatim from the current L03:
id="ACC-W910-L-G10-C1001-0003", lesson_type=7, provenance mnemonic_status="proposal", every production_frq
unit="paragraph" (type-7 ceiling is 'essay', so paragraph is within ceiling).

V3.1 changes applied to the current L03:
  1. ONE-IDEA callout + LIST teach (was a 130-plus-word wall of prose -> format_fidelity fail). The three parts
     are a real <ul>; the term COUNTERCLAIM is defined in plain words in the TEACH body (faultless communication).
  2. MODEL BEFORE THE QUIZ (KH): the coping-model think-aloud + check tool now PRECEDE the discrimination, and the
     discrimination is MODEL-role, with explicit choices=[].
  3. COPING-MODEL THINK-ALOUD (SRSD): a writer drafts a paragraph that only NAMES the objection, runs the check,
     catches that it never answered, and revises. Carries a literal BEFORE and AFTER (content_depth). No named peer.
  4. FIXED THE SURFACE-TOKEN CONFOUND (DI, faultless communication) + explicit choices=[]: a wrong distractor also
     uses a "Yet ... source fact" shape, so "has a connective and a fact" is no longer a cue; only the option that
     actually engages the cost objection is correct. Correct option is NOT the lone longest. No leaked 'Grade-C'.
  5. STRUCTURED FRQ / DIAGNOSIS bodies via lesson_prompts (frq_prompt/setapart/checklist): no 'Step 1/2' prose, no
     'Scored on ...' rubric chrome.
  6. AUTONOMY + SAY-THE-STANDARD (Yeager) on the independent write.

ONE IDEA: a counterargument paragraph does not just name the other side, it ANSWERS it (position, concede, answer).
ONE REMINDER: the 3-part check (position clear? counterclaim fairly conceded? truly answered with evidence + reason?).
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
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A counterargument paragraph does not just <strong>name</strong> '
'the other side, it <strong>answers</strong> it. Name the objection and stop, and the objection still stands.</div></div>')

# the reusable 3-part CHECK TOOL, attached at the model (point of first use), as a real <ol>.
REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 parts</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit any counterargument paragraph, run this quick check:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Is the POSITION (what you argue) clear?</li>'
'<li style="margin:2px 0">Is the counterclaim fairly CONCEDED, named as the strongest objection, not a weak one?</li>'
'<li style="margin:2px 0">Is it truly ANSWERED with a fact and a reason, not just a repeat of your claim?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If the objection is only named and never answered, the paragraph is not finished yet.</div></div>')

# coping-model think-aloud: a WRITTEN drafting process (draft a paragraph that only NAMES the objection -> run the
# check -> catch that it never answered -> revise), then the literal BEFORE and AFTER endpoints (content_depth needs
# BOTH inline). No named near-peer (Timeback stateless rule).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer building the counterargument paragraph, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "The school year should be longer. Some people say the '
    'added weeks cost too much. But a longer year would help students learn more." Run the check: position clear? '
    'Yes. Counterclaim conceded? Yes, the cost. Answered? No, it names the cost and then just repeats the claim, so '
    'the cost worry is still standing. Not finished.</p>'
    '<p style="margin:0"><strong>Second try, answers it:</strong> "Critics fairly note the cost falls on tight school '
    'budgets. Yet the source ties that time to the summer slide, which hits '
    'low-income students hardest, so the added weeks buy back the learning those students lose most." Now the '
    'objection is answered with a fact and a reason. That passes.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> names the cost objection, then repeats the claim, so the objection is never answered.</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> '
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;font-weight:700">POSITION</span> '
      'The school year should be longer. '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;font-weight:700">CONCEDE</span> '
      'Critics fairly note the added weeks cost tight school budgets. '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;font-weight:700">ANSWER</span> '
      'Yet the source ties that time to the summer slide that hits low-income '
      'students hardest, so the spending targets the very gap it aims to close. (position, concession, and a real answer)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1001-0003", grade="9-10", lesson_type=7,
    unit="G10 U1 - Counterargument (build the counterclaim into a paragraph)",
    title="Answer the Counterclaim in a Full Paragraph",
    target=("Build a counterargument paragraph: state your position, fairly concede the counterclaim, then "
            "answer it with evidence and reasoning, not just a repeat of your claim. Written at the paragraph. "
            "Trait: Development/Organization."),
    acc_tags=["ACC.W.ARG.2", "CCSS.W.9-10.1"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.01", "sot": "icm course-G10.md L03",
                "taught_stimulus": "ACC-W910-ARG-OPP-LESSON-SCHOOLYEAR",
                "transfer_stimulus": "ACC-W910-ARG-OPP-LESSON-CONGESTION",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "one_idea": "A counterargument paragraph does not just name the other side, it answers it (position, concede, answer).",
                "one_reminder": "3-part check: position clear? counterclaim fairly conceded? truly answered with evidence + reason?",
                "spiral_note": ("2026-07-21 spiral reframe: G9 now OWNS introductory counterargument (G9 L21 answers a "
                                "counterargument with a REASON in a short paragraph). This G10 lesson is the deeper "
                                "rung: answer with EVIDENCE from the source plus reasoning in a FULL paragraph, and "
                                "weigh it. Light touch: one opener line ties it to the G9 build; no content surgery, "
                                "id/type/slots/gates unchanged."),
                "template": "locked L01 template; EVIDENCE-TIER binds the full opposing-pair sources. T7 BUILD works at paragraph here (below essay ceiling).",
                "version_note": ("V3.1: rebuilt to the v3.1 standard (G9 L17 v3.1 exemplar). ONE-IDEA + list teach "
                                 "(fixed the prose-wall body), model+check-tool BEFORE the quiz (KH), coping-model "
                                 "think-aloud answering the objection (SRSD), fixed the connective/fact confound with "
                                 "explicit choices (DI faultless communication), removed the leaked 'Grade-C/design "
                                 "bet' label, structured FRQ/diagnosis bodies via lesson_prompts (no Step 1/2 prose, "
                                 "no 'Scored on' chrome), autonomy + say-the-standard on the independent write."),
                "council": ("T7/BUILD counterargument paragraph: position -> concede counterclaim -> ANSWER it "
                            "with evidence + reasoning (not a repeat). answers-vs-names-only discrimination "
                            "labeled Grade-C in code. BUILD=proposal; unit=paragraph (within essay ceiling)."),
                "review_provenance": ("v3.1 build spec (icm/_config/v3_1-lesson-build-spec.md); 23 lesson_contract "
                                      "gates + gated_reading render-QC, 2026-07-15.")},
    fade_ledger_moves=["counterclaim-paragraph", "answer-not-just-name-the-counterclaim"],
    slots=[
        # ===== TEACH: ONE idea + the three parts as a LIST; define COUNTERCLAIM in plain words =====
        Slot("TEACH", "teach_card", "Naming the other side is not answering it",
             body=(ONE_IDEA +
                   "In G9 you answered a counterargument with a reason inside a short paragraph. Here you answer "
                   "with EVIDENCE and reasoning in a full paragraph, and you weigh that answer against the "
                   "objection so your position clearly wins. "
                   "A counterclaim is a point that someone who disagrees with you would make, the strongest "
                   "objection to your position. A full counterargument paragraph has three parts:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>POSITION</strong>: the point you are arguing.</li>"
                   "<li style=\"margin:4px 0\"><strong>CONCEDE</strong>: fairly name the counterclaim, the "
                   "strongest objection from the other side.</li>"
                   "<li style=\"margin:4px 0\"><strong>ANSWER</strong>: respond to that objection with a fact "
                   "from the source and a reason, showing why your position still holds.</li></ul>"
                   "The common failure is naming the objection and then ignoring it: <em>Some say it costs too "
                   "much. But it would help students.</em> That mentions the counterclaim without answering it, so "
                   "the cost worry is still standing. Answering means engaging the objection head on, often by "
                   "showing the cost is worth it, smaller than it seems, or outweighed by a benefit, backed by a "
                   "fact and a reason. You are not learning a new move today; you are building the concede-then-"
                   "answer move into one solid paragraph.")),
        Slot("TEACH", "stimulus_display", "Read the source: a longer school year (both sides)",
             ref="ACC-W910-ARG-OPP-LESSON-SCHOOLYEAR", bank="school_year",
             body=("Read this source, which argues both sides of whether the school year should be longer. "
                   "Because your job is to ANSWER a counterclaim with evidence, read the whole thing and note a "
                   "position plus one fact you can use to answer the strongest objection from the other side. "
                   "The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model think-aloud + the reusable 3-part check tool =====
        Slot("MODEL", "annotated_before_after", "Watch a named counterclaim get answered",
             bank="school_year",
             body=("Here is the build in action. A writer drafts a paragraph that only names the objection, runs "
                   "the check, catches that it never answered, and revises. Follow the thinking below. " + COPING_HTML +
                   " The BEFORE names the cost and drops it. The AFTER concedes the cost and answers it with a "
                   "fact and a reason, so the objection no longer stands. " + REMEMBER +
                   "When you build your own, use this same check before you submit.")),
        Slot("MODEL", "discrimination", "Which paragraph answers the counterclaim?",
             ref="", labeled_grade_c=True, bank="school_year",
             body=("Now that you have seen one built, spot the target. All three concede the cost. Which one "
                   "actually ANSWERS it? "
                   "(A) The school year should be longer. Some say the added weeks cost districts too much and "
                   "strain tight budgets. But a longer year would help students learn more, which is the whole "
                   "point of school, so we should make it longer anyway.  "
                   "(B) The school year should be longer. Critics fairly note the added weeks fall on tight "
                   "budgets. Yet the source ties that time to the summer slide that hits low-income students "
                   "hardest, so the weeks buy back the learning those students lose most.  "
                   "(C) The school year should be longer. Critics fairly note the added weeks fall on tight "
                   "budgets. Yet the source says many high-performing countries run longer calendars, so a longer "
                   "year would clearly make our students far more competitive with the rest of the world.  "
                   "(D) The school year should be longer. Critics fairly note the added weeks fall on tight "
                   "budgets. Yet that expense is honestly not a big deal, and districts can surely find the money "
                   "somewhere if they just make it a real priority. "
                   "Correct: B answers the cost objection; A only names it, C changes the subject, and D waves "
                   "the objection away without evidence."),
             choices=[
                 {"id": "A", "text": "The school year should be longer. Some say the added weeks cost districts too much and strain tight budgets. But a longer year would help students learn more, which is the whole point of school, so we should make it longer anyway.",
                  "correct": False,
                  "why": "Partial. It names the cost objection and then just repeats the claim ('would help students learn more'), so the cost worry is never answered."},
                 {"id": "B", "text": "The school year should be longer. Critics fairly note the added weeks fall on tight budgets. Yet the source ties that time to the summer slide that hits low-income students hardest, so the weeks buy back the learning those students lose most.",
                  "correct": True,
                  "why": "Correct. It concedes the cost and then engages it directly with a fact (the summer slide) and a reason (the spending targets the gap it aims to close). Answering, not just naming, is the move."},
                 {"id": "C", "text": "The school year should be longer. Critics fairly note the added weeks fall on tight budgets. Yet the source says many high-performing countries run longer calendars, so a longer year would clearly make our students far more competitive with the rest of the world.",
                  "correct": False,
                  "why": "It uses a connective and a real source fact, but the fact is about competitiveness, not about cost. It changes the subject instead of answering the cost objection it named."},
                 {"id": "D", "text": "The school year should be longer. Critics fairly note the added weeks fall on tight budgets. Yet that expense is honestly not a big deal, and districts can surely find the money somewhere if they just make it a real priority.",
                  "correct": False,
                  "why": "It concedes the cost and then just waves it away ('not a big deal'), with no fact from the source and no real reason. Dismissing an objection is not the same as answering it."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this counterargument most need?",
             bank="school_year",
             body=("Diagnose before the reveal. A paragraph reads: 'The school year should be longer. People "
                   "worry it is too expensive. Still, learning is important, so we should do it.' Which single "
                   "move would most improve it as a counterargument paragraph? "
                   "(A) answer the cost worry directly with a fact and a reason, not just restate that learning matters  "
                   "(B) add a second objection from the other side, such as teacher pay or scheduling, on top of the cost worry  "
                   "(C) make the position sound more forceful with stronger wording and a confident tone that repeats the claim  "
                   "(D) move the objection to the end so it comes after the claim, changing only the order of the sentences here"),
             feedback=("Correct: A. The paragraph names the cost worry and then just repeats that learning "
                       "matters, so the objection is never answered. The fix answers it directly: concede the "
                       "cost, then show it targets the summer slide that hurts low-income students most, a fact "
                       "plus a reason. A second objection (B), a more forceful tone (C), or reordering (D) do not "
                       "answer the cost worry.")),

        # ===== SUPPORTED: framed write, build the concede + answer onto a given position =====
        Slot("SUPPORTED", "production_frq", "Concede and answer in two sentences", ref="", bank="school_year",
             rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="Warm up the build. Start from the given position, then add the two parts that answer the other side.",
                 setapart_block=setapart("Start from this position, then build onto it:",
                                         "POSITION (given): The school year should be longer. Now write the "
                                         "CONCEDE sentence (fairly name the strongest objection from the source) "
                                         "and the ANSWER sentence (respond with a fact from the source plus a reason)."),
                 closer="Write those two sentences so the answer truly engages the objection, not just repeats "
                        "the claim. You are building the concede-then-answer onto the given position.")),
        # COUNCIL FIX (2026-07-24): Option A (later-in-arc), watch-then-do: demo preserved, produce is the graded
        # act. The old diagnosis_frq bundled a watched 3-part check-run demo (pre-answered (q,a) tuple rows) + a
        # fresh paragraph + a run-the-check-and-name tail in one box (unscoreable, wired to no grader, and the
        # (q,a) rows leaked the answers). The coping-model demo is PRESERVED as read-only narration (the 3-part
        # check shown running on the weak draft, in plain declarative prose). The student's ONLY graded act is the
        # fresh paragraph; the three checks sit read-only beneath as plain-string reminders; the run-and-name tail
        # is deleted. Stays on the taught topic (no new source).
        Slot("MODEL", "diagnosis_frq", "Write a fresh counterargument that answers the objection", ref="",
             bank="school_year", rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="First, watch the 3-part check run on the weak draft below. The POSITION is clear ('a longer "
                       "year is good' states the point). The counterclaim is fairly CONCEDED (the cost is named). "
                       "But it is not truly ANSWERED: 'still a good idea' just repeats the claim, so a stronger "
                       "version would answer the cost with a fact from the source and a reason. Now write a fresh "
                       "concede-then-answer paragraph of your own that does not fall into that trap.",
                 setapart_block=setapart("Weak draft the check was run on:",
                                         "A longer year is good. Critics say it costs money. But it is still a good idea.", "red"),
                 checklist_block=checklist(title="Check your paragraph against these (no need to type answers):", rows=[
                     "Is the POSITION clear?",
                     "Is the counterclaim fairly CONCEDED?",
                     "Is it truly ANSWERED with evidence and reasoning, not just a repeat of the claim?",
                 ]),
                 closer="Write one fresh concede-then-answer for the school-year position: state the POSITION, "
                        "fairly CONCEDE the strongest objection, then ANSWER it with a fact from the source and a "
                        "reason. Run the three checks above before you submit.")),

        # ===== INDEPENDENT: cold full-paragraph build on the taught topic + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Write a full counterargument paragraph", ref="", bank="school_year",
             rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now, build the whole paragraph.",
                 closer="Write ONE counterargument paragraph on whether the school year should be longer, with all "
                        "three parts: state your POSITION, fairly CONCEDE the strongest counterclaim, then ANSWER "
                        "it with a fact from the source and a reason. Before you submit, run the 3-part check and "
                        "fix any part that fails. Answering the counterclaim is what every real argument paragraph "
                        "is built on, and you are ready to do it cold.")),

        # ===== TRANSFER: same move, a NEW source (congestion pricing), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: congestion pricing (both sides)",
             ref="ACC-W910-ARG-OPP-LESSON-CONGESTION", bank="congestion_pricing",
             body=("Read this new source, which argues both sides of congestion pricing (charging tolls to drive "
                   "downtown at busy hours). Because your job is to ANSWER a counterclaim with evidence, read the "
                   "whole thing and note a position plus one fact to answer the strongest objection. The text "
                   "stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Write a counterargument paragraph on a NEW topic", ref="",
             bank="congestion_pricing", rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="New topic, same build. The task: argue a position on congestion pricing.",
                 closer="Write ONE counterargument paragraph on congestion pricing with all three parts: state "
                        "your POSITION, fairly CONCEDE the strongest counterclaim (for example the burden on "
                        "low-income drivers), then ANSWER it with a fact from the source and a reason. Same concede-"
                        "then-answer build as the school-year paragraph, fresh topic. Do not stop at naming the "
                        "objection. Run the 3-part check before you submit.")),
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
