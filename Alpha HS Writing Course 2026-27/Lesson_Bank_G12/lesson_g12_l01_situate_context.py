"""
lesson_g12_l01_situate_context.py  -  G12 KC C.12.01, ARCHETYPE T2 (STAND, sentence). AP SOPHISTICATION. V3.1.

G12 course L01 (Unit 1, intro). cS2 situate-in-broader-context: place the specific question inside the larger
one it belongs to (the AP sophistication move, Row C), then answer within that frame, rather than answering only
the narrow prompt. Binds the G12 argument LESSON source. Taught: automation_policy (WATERTRADEOFF, full) ->
transfer: public_health (WORKFORCEINVEST, full). rc.ap, unit=sentence (the situate move is practiced at the
sentence before the full essay). STAND=proposal. No named persona (Timeback stateless rule); no source markup;
no prior-work ref; no em dashes.

V3.1 (2026-07-15): rebuilt from the PRE-v3.1 prose-wall version onto the v3.1 spine (mirrors the G9 L01 T2
template). Changes: TEACH split to ONE idea hammered + a real list (no wall of text); a coping-model think-aloud
(First try -> check -> catch -> Final) with a literal BEFORE and AFTER; the reusable 3-question check folded in
as a REMEMBER box; discrimination uses explicit homogeneous-length choices with the token confound broken (an
over-broad distractor also names a larger question, so "names a bigger question" is not the discriminator,
committing within it is); the leaked "Grade-C design bet" label removed from student text (kept in code only);
predict-the-fix reveal moved to feedback; supported write is a fill-in frame; diagnosis watches a check on a
provided weak draft then rewrites; independent says the standard.

ONE IDEA: to earn sophistication, SITUATE the question, name the larger one it belongs to, then answer within it.
ONE REMINDER: the 3-question situate check. Passes all 23 lesson_contract gates. Own words, no fabricated figures.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">To reach real complexity, '
'<strong>SITUATE</strong> the question: name the broader question your specific prompt is one instance of, '
'then answer <strong>within</strong> that frame.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit a situated claim, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">What larger question is this prompt one instance of?</li>'
'<li style="margin:2px 0">Is that larger question named inside the claim?</li>'
'<li style="margin:2px 0">Does the claim still commit to an answer within it?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, it is not yet situated.</div></div>')

# coping-model think-aloud: a WRITTEN drafting process (attempt -> test -> catch -> revise), then the endpoints.
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer thinking it through, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "The country should protect its water for food, '
    'because people need to eat." Check it: what larger question is this an instance of? I have not named one, '
    'I just answered the literal prompt as a standalone puzzle. That adds no complexity. Go deeper.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> Name the larger question. This choice is really '
    'about how a society rations a necessity it can no longer fully supply. Good, but is that frame in the '
    'claim, and does the claim still commit to an answer? The frame is there; the answer is not yet. Join them.</p>'
    '<p style="margin:0"><strong>Final:</strong> "The food-or-power choice is one instance of how a society '
    'rations a necessity it can no longer fully supply, so protecting food first is defensible only alongside a '
    'rule for the grid the food supply itself depends on." Larger question named, and a committed answer inside '
    'it. That situates.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "The country should protect its water for food, because '
    'people need to eat." (answers only the narrow prompt)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "The food-or-power choice is one instance of how a society '
    'rations a necessity it can no longer fully supply, so protecting food first is defensible only alongside a '
    'rule for the grid the food supply itself depends on." (a situated claim)</span></div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G12-C1201-0001", grade="9-10", lesson_type=2,
    unit="G12 U1 - Sophistication (situate in a broader context)",
    title="Situate the Question in the Larger One It Belongs To",
    target=("Place the specific prompt inside the broader question it is an instance of, then answer within "
            "that frame, rather than treating the prompt as a standalone puzzle. The complexity move. "
            "Written at the sentence (a situated thesis; the move is practiced at the sentence before "
            "the full essay). Trait: Depth and Significance."),
    acc_tags=["ACC.W.ARG.2", "CCSS.W.11-12.1"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.12.01", "sot": "icm course-G12.md L01",
                "taught_stimulus": "ACC-W910-ARG-LESSON-WATERTRADEOFF",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-WORKFORCEINVEST",
                "playbook": "_phase2/playbook_T2_STAND.md",
                "one_idea": "To earn sophistication, situate the question: name the larger one, then answer within it.",
                "one_reminder": "3-question situate check: which larger question? named in the claim? still commits within it?",
                "template": "locked L01 template; binds G12 argument LESSON source; AP sophistication (Row C).",
                "version_note": ("V3.1 2026-07-15: rebuilt from the PRE-v3.1 prose-wall version onto the G9-L01 "
                                 "v3.1 spine. ONE idea + list, coping-model think-aloud with literal BEFORE/AFTER, "
                                 "3-question check folded in as REMEMBER, discrimination via explicit choices with "
                                 "the token confound broken (over-broad distractor also names a larger question), "
                                 "predict-the-fix reveal in feedback, fill-in frame on the supported write, "
                                 "internal Grade-C label removed from student text (labeled_grade_c kept in code)."),
                "council": ("T2/STAND G12 sophistication intro: cS2 situate-in-broader-context (place the question "
                            "in a larger one). Discrimination is a Grade-C design bet (labeled in code, never in "
                            "student text). STAND=proposal; unit=sentence at intro (situate practiced at the "
                            "sentence before the full essay).")},
    fade_ledger_moves=["situate-in-broader-context", "answer-within-the-larger-question"],
    slots=[
        # ===== TEACH: ONE idea, then the minimum teaching as a real list (no wall of text) =====
        Slot("TEACH", "teach_card", "The one idea: name the larger question, then answer within it",
             body=(ONE_IDEA +
                   "At the mastery level, a top essay reaches real complexity, which the rubric names depth and "
                   "significance. One reliable way to reach it is to situate the prompt. Three kinds of answer look similar but do "
                   "different jobs, so keep them apart:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>NARROW</strong>: takes a side on the literal prompt only "
                   "(protect food, or protect power) and defends it as a standalone puzzle.</li>"
                   "<li style=\"margin:4px 0\"><strong>SITUATED</strong>: names the larger question the prompt is "
                   "one instance of (how a society rations a necessity it can no longer fully supply), then "
                   "commits to a position inside that frame.</li>"
                   "<li style=\"margin:4px 0\"><strong>THE TRAP</strong>: going so broad you never answer the "
                   "actual prompt. So situate, then commit.</li></ul>"
                   "The situated answer is what reaches real complexity. Scoring calls the single sentence stating your "
                   "position a <dfn class=\"tb-glossary-term\" data-catalog-idref=\"def-thesis\" "
                   "title=\"Thesis means the one-sentence claim your whole response defends.\">thesis</dfn>; a "
                   "thesis is a claim, so a situated thesis is a claim that names the larger question before it "
                   "commits. Today's task asks you to situate, then commit.")),
        Slot("TEACH", "stimulus_display", "Read the source: water for food or power?",
             ref="ACC-W910-ARG-LESSON-WATERTRADEOFF", bank="automation_policy",
             body=("Read this source on whether a drying region should protect its scarce water for growing food "
                   "or for generating power. As you read, ask what LARGER question this trade-off is one instance "
                   "of (about rationing, dependence, or shared systems), so you can situate your answer. The text "
                   "stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model think-aloud + the check tool folded in =====
        Slot("MODEL", "annotated_before_after", "Watch a narrow claim get situated",
             bank="automation_policy",
             body=("Here is the move in action. Follow the writer's thinking below. " + COPING_HTML +
                   " Notice the two moves that turned the BEFORE into the AFTER. "
                   "<strong>Move 1, name the larger question</strong>: the writer says what broader question the "
                   "prompt is one instance of. <strong>Move 2, answer within it</strong>: the writer commits to a "
                   "position inside that frame instead of answering the literal prompt alone. " + REMEMBER +
                   "When you write your own, build it the same way: name the larger question first, commit inside "
                   "it, then run the 3 questions before you submit.")),
        Slot("MODEL", "discrimination", "Which claim situates the question?",
             ref="", labeled_grade_c=True, bank="school_phone_policy",
             body=("Now that you have seen one built, spot the target, this time on a different question. A school "
                   "is deciding whether to ban phones during the school day. Which claim SITUATES that question in "
                   "a broader one AND still answers it? "
                   "(A) A school should ban phones during the day, because phones pull students' attention away "
                   "from the teacher and the lesson in front of them.  "
                   "(B) The phone-ban question is one instance of when an institution may limit a personal freedom "
                   "for the good of the group, so a ban is fair only if it leaves alone the freedoms that cost the "
                   "group nothing.  "
                   "(C) This question is really about the single largest issue there is, namely how much say any "
                   "authority anywhere should ever be allowed to have over the private, personal choices of every "
                   "individual living in a genuinely free society.  "
                   "(D) Whether to ban phones is one instance of when an institution may limit a personal freedom "
                   "for the good of the group, and both sides raise fair points, so the school should study the "
                   "question closely and weigh all the arguments before it settles on any policy. "
                   "Correct: B situates and commits. (A) answers only the literal prompt; (C) names a larger "
                   "question but is so broad it never answers this one; (D) names the larger question but then "
                   "hedges and never commits to a position within it."),
             choices=[
                 {"id": "A", "text": "A school should ban phones during the day, because phones pull students' attention away from the teacher and the lesson in front of them.",
                  "correct": False,
                  "why": "This is a clear, defensible answer, but it is NARROW: it takes a side on the literal phone prompt only and never names the larger question the choice belongs to."},
                 {"id": "B", "text": "The phone-ban question is one instance of when an institution may limit a personal freedom for the good of the group, so a ban is fair only if it leaves alone the freedoms that cost the group nothing.",
                  "correct": True,
                  "why": "Correct. It names the broader question (when an institution may limit a personal freedom for the group's good) AND commits to a position inside it. Naming plus committing is what situating means."},
                 {"id": "C", "text": "This question is really about the single largest issue there is, namely how much say any authority anywhere should ever be allowed to have over the private, personal choices of every individual living in a genuinely free society.",
                  "correct": False,
                  "why": "This names a larger question, but it falls into the trap: it goes so broad it never answers the actual phone prompt. Situating requires you to commit within the frame, not just gesture at a big idea."},
                 {"id": "D", "text": "Whether to ban phones is one instance of when an institution may limit a personal freedom for the good of the group, and both sides raise fair points, so the school should study the question closely and weigh all the arguments before it settles on any policy.",
                  "correct": False,
                  "why": "This names the larger question correctly, but then it hedges: it calls for more study instead of committing to a position within the frame. Situating means naming the larger question AND answering inside it, so a claim that never commits is not yet situated."},
             ]),
        Slot("MODEL", "discrimination", "A closer pair: which claim actually situates?",
             ref="", labeled_grade_c=True, bank="automation_policy",
             body=("One more, a closer call. Both of these sound like they zoom out, but only one names a "
                   "genuinely LARGER question and then answers inside it. Which claim actually situates the "
                   "water choice? "
                   "(A) Deciding whether a drying region should spend its scarce water on growing food or on "
                   "generating power is one of the most urgent and important questions our society faces today, "
                   "and I firmly believe we must always put food ahead of power.  "
                   "(B) The water choice is one instance of how a community ranks its needs when it cannot meet "
                   "all of them at once, so food should come first and power should take only what is left.  "
                   "(C) This really comes down to the bigger question of whether food matters more than "
                   "electricity, and because food clearly matters more, the region should protect its water for crops.  "
                   "(D) The water choice is one instance of how a community ranks the needs it cannot all meet, and "
                   "a community should always rank its most basic survival needs ahead of everything else. "
                   "Correct: B. (A) only piles urgent, important-sounding words onto the narrow prompt and never "
                   "names a larger question the choice belongs to. (C) sounds broader, but its bigger question "
                   "just reworks the same food-or-power prompt, so the frame is not truly larger. (D) names a "
                   "genuinely larger question but only answers it in the abstract and never comes back to commit "
                   "on the water. Only B names a genuinely larger question and commits inside it."),
             choices=[
                 {"id": "A", "text": "Deciding whether a drying region should spend its scarce water on growing food or on generating power is one of the most urgent and important questions our society faces today, and I firmly believe we must always put food ahead of power.",
                  "correct": False,
                  "why": "This only piles urgent, important-sounding words onto the narrow prompt and never names the larger question the choice belongs to, so it has not situated anything."},
                 {"id": "B", "text": "The water choice is one instance of how a community ranks its needs when it cannot meet all of them at once, so food should come first and power should take only what is left.",
                  "correct": True,
                  "why": "Correct. It names a genuinely larger question, how a community ranks needs it cannot all meet, and then commits to a position inside that frame."},
                 {"id": "C", "text": "This really comes down to the bigger question of whether food matters more than electricity, and because food clearly matters more, the region should protect its water for crops.",
                  "correct": False,
                  "why": "The bigger question it names just reworks the same food-or-power prompt in other words, so the frame is not actually larger and the claim has not zoomed out."},
                 {"id": "D", "text": "The water choice is one instance of how a community ranks the needs it cannot all meet, and a community should always rank its most basic survival needs ahead of everything else.",
                  "correct": False,
                  "why": "This names a genuinely larger question, but it only answers in the abstract and never comes back to commit on the actual water choice. Situating means answering the specific prompt within the larger frame, not abandoning the prompt for the principle."},
             ]),
        Slot("MODEL", "predict_the_fix", "What gives this claim real complexity?",
             bank="automation_policy",
             body=("Diagnose before the reveal. A student wrote a clear, correct position: 'Protect power first, "
                   "because everything depends on the grid.' It is defensible but adds no complexity. Which "
                   "single move would most likely reach real complexity? "
                   "(A) situate the choice in the larger question it is one instance of, then answer within it  "
                   "(B) restate the same position in stronger, more forceful words so its urgency lands harder  "
                   "(C) add another federal statistic about water or power use to back the identical position  "
                   "(D) stretch the sentence with extra clauses and formal vocabulary so it reads as developed"),
             feedback=("Correct: A. The position is fine but freestanding; complexity comes from placing it in "
                       "the larger question (how a society rations shared necessities) so the answer speaks to the "
                       "real stakes. Stronger words (B), another statistic (C), or added length (D) never situate "
                       "the argument.")),

        # ===== SUPPORTED: framed write (fill-in frame) on the taught source =====
        Slot("SUPPORTED", "production_frq", "Situate the question, then stake a claim",
             ref="", bank="automation_policy", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on the two moves: name the larger question, then commit.",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "The choice between ______ and ______ is really one instance of ______ "
                                         "(the larger question) so I hold that ______ (my position within that frame)."),
                 closer="Name the broader question AND answer within it. Do not answer only the narrow prompt. "
                        "Then check it against the 3 questions.")),
        # DIAGNOSIS = watch a check on a PROVIDED weak draft, then rewrite a fresh one (self-contained; no look-back).
        Slot("MODEL", "diagnosis_frq", "Check your claim: situated, or narrow?",
             ref="", bank="automation_policy", scored=True,
             body=frq_prompt(
                 intro="Watch the situate check run on a weak draft, then run it on a fresh claim of your own.",
                 setapart_block=setapart("Weak draft to fix:", "We should protect food, because food is important.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("What larger question is this prompt one instance of?",
                      "It never names one. Name it: how a society rations a necessity it cannot fully supply."),
                     ("Is that larger question named inside the claim?",
                      "your call: yes / no"),
                     ("Does the claim still commit to an answer within that frame?",
                      "Not yet. Connect the commitment to the frame you named."),
                 ]),
                 closer="Now write a fresh situated claim for the water trade-off, then run the same three checks. "
                        "Finish by naming the larger question you used.")),

        # ===== INDEPENDENT: cold write on the water prompt, no frame + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Situate on your own",
             ref="", bank="automation_policy", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now, no frame. The prompt: when water is scarce, should a region protect its "
                       "water for growing food or for generating power?",
                 closer="Situating a question inside the larger one it belongs to is what every complex "
                        "argument is built on, and you are ready to do it cold. Before you submit, check: is the "
                        "larger question named, and does the claim still commit to an answer within it? If not, "
                        "fix it first.")),

        # ===== TRANSFER: same move, a NEW source, partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: a workforce trade-off",
             ref="ACC-W910-ARG-LESSON-WORKFORCEINVEST", bank="public_health",
             body=("Read this new source on whether a society should invest first in preparing more people for "
                   "fast-growing technical fields or first in protecting the workers the change leaves behind. "
                   "Ask what LARGER question its specific choice is one instance of, so you can situate your "
                   "answer. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Situate on a NEW source",
             ref="", bank="public_health", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="New source. The prompt: should a society invest first in preparing more people for the "
                       "growing technical fields, or first in protecting the workers the change leaves behind?",
                 closer="Same situate-then-commit move as the water trade-off, new source. Name the broader "
                        "question this choice is one instance of, then commit to a position within it. Do not "
                        "answer only the narrow prompt. Check it against the 3 questions before you submit.")),
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
