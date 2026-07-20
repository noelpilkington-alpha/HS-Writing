"""
lesson_g11_l17_source_free_position.py  -  G11 KC C.11.06, ARCHETYPE T2 (STAND, sentence). V3.1.

G11 course L17 (Unit 4, intro). E3 source-free position: on a general prompt with NO passage, take a
defensible position AND anchor it to a specific example from your own knowledge, rather than staying general.
Taught: ACC-W1112-SFA-LESSON-0001 (curiosity vs usefulness) -> transfer: ACC-W910-SFA-PROMPT-0001 (tradition
vs progress). rc.ap, unit="sentence". STAND=proposal. No named persona (Timeback stateless rule); no source
markup; no prior-work reference; no em dashes.

V3.1: rebuilt from the pre-v3.1 prose-wall version onto the locked L01 v3.1 spine:
  1. TEACH is ONE hammered idea (teal ONE_IDEA callout) + the minimum teaching as a real list, not a wall.
  2. MODEL is a coping-model think-aloud (First try -> Second try -> Final) with a literal BEFORE and AFTER.
  3. The two moves are named + the reusable 3-question check tool is folded in as a dashed REMEMBER box.
  4. Discrimination uses explicit choices=[]; the correct option is not the lone longest and every option
     shares the same "Society should fund open inquiry, because..." stem so the specific example is the only
     invariant (no surface-token confound). No leaked internal labels ("Grade-C" / "design bet") in student text.
  5. Predict-the-fix reveal lives in feedback=, not in option text.
  6. Supported = a fill-in frame; diagnosis = watch a check on a PROVIDED weak draft (checklist, no Step-N prose)
     then rewrite; independent = no frame + say-the-standard; transfer = same move on the OTHER bound prompt.

ONE IDEA: on a source-free prompt YOU supply the evidence: take a position AND anchor it to one specific example.
ONE REMINDER: the 3-question anchor check. Passes all 23 lesson_contract gates. Own words, no fabricated figures.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">On a source-free prompt, <strong>you</strong> supply the '
'evidence: take a defensible <strong>POSITION</strong> and anchor it to one <strong>SPECIFIC example</strong> of '
'your own. A position with no example floats.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit any source-free position, run this test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does it take a defensible position (a side a reasonable person could reject)?</li>'
'<li style="margin:2px 0">Does it name one specific example you supply (a case, event, study, or experience)?</li>'
'<li style="margin:2px 0">Is that example concrete, not a generality like "it has helped many people"?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, it is not anchored yet.</div></div>')

# coping-model think-aloud panel: a WRITTEN drafting process (attempt -> check -> revise), then the endpoints.
# No named person (Timeback stateless rule). Both BEFORE and AFTER present (content_depth).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer thinking it through on the curiosity prompt, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Society should support curiosity because curiosity '
    'matters." Check it: does it name one specific example I supply? No. It just asserts the topic matters. It '
    'floats. Add a case.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "Society should fund curiosity-driven inquiry, '
    'because pure research often turns out to be useful later." Better, it takes a side. But "often turns out '
    'useful" is still a generality, not one concrete case. Name a real one.</p>'
    '<p style="margin:0"><strong>Final:</strong> "Society should fund curiosity-driven inquiry, because the pure '
    'mathematics of non-Euclidean geometry sat unused for decades before it became the language Einstein needed '
    'for general relativity." A side, plus one specific case I supplied. That passes.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "Society should support curiosity because curiosity matters." '
    '(a position with no example)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "Society should fund curiosity-driven inquiry, because the pure '
    'mathematics of non-Euclidean geometry sat unused for decades before it became the language Einstein needed '
    'for general relativity." (a position anchored to one specific example)</span></div>'
'</div>')

LESSON = Lesson(
    id="ACC-W1112-L-G11-C1104-0017", grade="9-10", lesson_type=2,
    unit="G11 U4 - Source-free position (anchor a claim to your own example)",
    title="Take a Position, Then Anchor It With Your Own Example",
    target=("On a general prompt with no provided source, take a defensible position and anchor it to a "
            "specific example from your own reading, studies, or experience, rather than arguing in "
            "generalities. Written at the sentence. Trait: Thesis and Evidence."),
    acc_tags=["ACC.W.ARG.1", "CCSS.W.11-12.1"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.06", "sot": "icm course-G11.md L17",
                "taught_stimulus": "ACC-W1112-SFA-LESSON-0001",
                "transfer_stimulus": "ACC-W910-SFA-PROMPT-0001",
                "playbook": "_phase2/playbook_T2_STAND.md",
                "one_idea": "On a source-free prompt you supply the evidence: position + one specific example.",
                "one_reminder": "3-question anchor check: position? specific example? concrete not general?",
                "template": "locked L01 v3.1 template; PROMPT-ONLY tier binds the source-free prompt (no fact table).",
                "version_note": ("V3.1: rebuilt the pre-v3.1 prose-wall body onto the L01 v3.1 spine - ONE_IDEA "
                                 "teal callout + list TEACH, coping-model think-aloud MODEL with BEFORE/AFTER, "
                                 "named moves + REMEMBER 3-question check, explicit-choices discrimination with a "
                                 "shared stem (no token confound, correct not lone longest), reveal in feedback, "
                                 "framed supported write, checklist diagnosis (no Step-N prose), say-the-standard "
                                 "independent write."),
                "council": ("T2/STAND G11 source-free intro: introduces E3 (source-free position anchored to an "
                            "own-knowledge example). anchored-vs-general discrimination labeled Grade-C in code "
                            "only (labeled_grade_c=True), never in student text. STAND=proposal.")},
    fade_ledger_moves=["source-free-position", "anchor-to-own-example"],
    slots=[
        # ===== TEACH: ONE idea, then the minimum teaching as a real list =====
        Slot("TEACH", "teach_card", "The one idea: take a POSITION, anchor it with your own example",
             body=(ONE_IDEA +
                   "Some prompts give you no passage at all, just a general question you argue from what you "
                   "already know. That is a source-free prompt, which means a prompt with no reading provided, "
                   "where the evidence has to come from your own reading, studies, observation, or experience. "
                   "Two moves make the answer strong:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\">Take a defensible <strong>POSITION</strong>, sometimes called a "
                   "<dfn class=\"tb-glossary-term\" data-catalog-idref=\"def-thesis\" "
                   "title=\"Thesis means the one arguable position your whole essay defends. You do not need this "
                   "word to finish today's task.\">thesis</dfn>, which is a one-sentence claim a reasonable "
                   "person could dispute, not a restatement of the question.</li>"
                   "<li style=\"margin:4px 0\">Anchor it to one <strong>SPECIFIC example</strong> you supply: a "
                   "named case, event, book, study, or experience, not \"curiosity has helped people in many "
                   "ways.\"</li></ul>"
                   "The trap is staying general, agreeing that the topic matters without ever landing on one "
                   "concrete case. Goal today: state a position and anchor it with one specific example of your own.")),
        Slot("TEACH", "stimulus_display", "Read the prompt: curiosity or usefulness?",
             ref="ACC-W1112-SFA-LESSON-0001", bank="sfa_curiosity_use",
             body=("Read this source-free prompt on whether a society should support inquiry that has no "
                   "foreseeable use. There is no passage, so the example must come from you. As you read, note "
                   "specific cases you know (from science, history, or your own studies) that could anchor a "
                   "position. The prompt stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model think-aloud + named moves + folded-in check tool =====
        Slot("MODEL", "annotated_before_after", "Watch a floating position get anchored",
             bank="sfa_curiosity_use",
             body=("Here is the skill in action. Follow the writer's thinking below." + COPING_HTML +
                   "Notice the two moves that turned the BEFORE into the AFTER. <strong>Move 1</strong>: the "
                   "writer took a <strong>position</strong> a reasonable person could reject. <strong>Move 2</strong>: "
                   "the writer anchored it to one <strong>specific example</strong> supplied from memory. " + REMEMBER +
                   "When you write your own, build it the same way: take the side first, then anchor it with one "
                   "concrete case, and run the 3 questions before you submit.")),
        Slot("MODEL", "discrimination", "Which position is anchored to a specific example?",
             ref="", labeled_grade_c=True, bank="sfa_curiosity_use",
             body=("Now that you have seen one built, spot the target. Each option takes the same side; which one "
                   "is ANCHORED to a specific example, and which stay GENERAL? "
                   "(A) Society should fund open inquiry, because curiosity has, all throughout the long history "
                   "of human civilization, helped many different people in countless important and lasting ways.  "
                   "(B) Society should fund open inquiry, because the study of prime numbers stayed pure "
                   "curiosity for centuries before it became the basis of modern encryption.  "
                   "(C) Society should fund open inquiry, because thoughtful people nearly everywhere agree that "
                   "funding research is a genuinely worthwhile public good.  "
                   "(D) Society should fund open inquiry, because history is full of discoveries that began as "
                   "pure curiosity and later proved useful. "
                   "Correct: B. B names one concrete case the writer supplies. A, C, and D take a side but never "
                   "land on a specific example, so they stay general."),
             choices=[
                 {"id": "A",
                  "text": "Society should fund open inquiry, because curiosity has, all throughout the long history of human civilization, helped many different people in countless important and lasting ways.",
                  "correct": False,
                  "why": "This takes a side, but 'helped many people in countless ways' is a generality. It names no specific case, so it stays general."},
                 {"id": "B",
                  "text": "Society should fund open inquiry, because the study of prime numbers stayed pure curiosity for centuries before it became the basis of modern encryption.",
                  "correct": True,
                  "why": "Correct. It takes a side AND anchors it to one concrete case the writer supplies (prime numbers becoming the basis of encryption). Naming the specific example is the move."},
                 {"id": "C",
                  "text": "Society should fund open inquiry, because thoughtful people nearly everywhere agree that funding research is a genuinely worthwhile public good.",
                  "correct": False,
                  "why": "An appeal to agreement is not an example. 'People agree it is worthwhile' names no specific case, so this stays general too."},
                 {"id": "D",
                  "text": "Society should fund open inquiry, because history is full of discoveries that began as pure curiosity and later proved useful.",
                  "correct": False,
                  "why": "This gestures at many discoveries at once but never names one. 'History is full of discoveries' is a whole category, not a single concrete case, so it stays general."},
             ]),
        Slot("MODEL", "discrimination", "Which one takes a defensible position?",
             ref="", labeled_grade_c=True, bank="sfa_curiosity_use",
             body=("One more, this time watch the POSITION. All four mention research, but a claim floats until "
                   "it takes a side a reasonable person could reject. Which one takes a defensible position, "
                   "rather than restating the topic or stating something no one would dispute? "
                   "(A) Whether a society should pay for research that has no clear use is a question with good "
                   "points on both sides, as the long-running debate over funding deep-space missions reminds us.  "
                   "(B) Society should keep funding basic research that has no clear use, because the laser began "
                   "as pure physics before it became essential to eye surgery.  "
                   "(C) Research has produced many useful tools, like the light bulb that most people rely on today.  "
                   "(D) This essay will look at the reasons a society might choose to fund research that has no "
                   "clear use. "
                   "Correct: B. B commits to a side a reasonable person could reject and anchors it to one concrete "
                   "case. A raises the topic but sits on the fence, C states an agreeable fact no one disputes, and "
                   "D announces what the essay will cover, so none of those takes a position."),
             choices=[
                 {"id": "A",
                  "text": "Whether a society should pay for research that has no clear use is a question with good points on both sides, as the long-running debate over funding deep-space missions reminds us.",
                  "correct": False,
                  "why": "This raises a real topic but says there are good points on both sides, so it never lands on a side a reasonable person could reject."},
                 {"id": "B",
                  "text": "Society should keep funding basic research that has no clear use, because the laser began as pure physics before it became essential to eye surgery.",
                  "correct": True,
                  "why": "Correct. It commits to a side a reasonable person could reject and anchors that side to one concrete case, the laser starting as pure physics."},
                 {"id": "C",
                  "text": "Research has produced many useful tools, like the light bulb that most people rely on today.",
                  "correct": False,
                  "why": "This states an agreeable fact no one would dispute, so it never takes the arguable funding position the prompt asks for."},
                 {"id": "D",
                  "text": "This essay will look at the reasons a society might choose to fund research that has no clear use.",
                  "correct": False,
                  "why": "This announces the topic the essay will cover instead of committing to a side. Saying what you will discuss is not the same as taking a position a reader could reject."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this source-free claim most need?",
             bank="sfa_curiosity_use",
             body=("Diagnose this draft before the reveal. A student wrote: 'I believe open-ended research is "
                   "worthwhile, and society should pay for it because it can lead to important discoveries "
                   "someday.' Which single move would most improve it? "
                   "(A) anchor the position to one specific example from the writer's own knowledge, such as a "
                   "named discovery, historical case, or study  "
                   "(B) replace the plain wording with stronger, more forceful phrasing so the claim sounds more "
                   "confident and certain to a reader  "
                   "(C) note that many people already accept that research is worthwhile, so widespread agreement "
                   "can stand in for the missing example  "
                   "(D) restate the same general point over again in slightly different words so that the whole "
                   "position simply reads as longer and more fully developed"),
             feedback=("Correct: A. 'Can lead to important discoveries someday' is exactly the generality that "
                       "weakens a source-free answer. The fix supplies one concrete case the writer knows (a "
                       "discovery, a historical example, an observation). Stronger wording (B), an appeal to "
                       "agreement (C), or extra length (D) never add the missing example.")),

        # ===== SUPPORTED: framed write on the taught prompt (source already read at TEACH) =====
        Slot("SUPPORTED", "production_frq", "Write a position anchored to your own example",
             ref="", bank="sfa_curiosity_use", rubric_ref="rc.ap", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on the two moves: take a side, then anchor it.",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "Society should ______ [your position on the curiosity prompt] because "
                                         "______ [one specific case from your reading, studies, or experience]."),
                 closer="Take a clear side AND name one concrete example you supply. Do not stay general. Then "
                        "check it against the 3 questions.")),
        # DIAGNOSIS = watch the check run on a PROVIDED weak draft, then write a fresh anchored position. Stays
        # on the taught prompt (no new source to read). checklist() renders one clean numbered list (no Step-N).
        Slot("MODEL", "diagnosis_frq", "Check a weak draft, then write a fresh anchored position",
             ref="", bank="sfa_curiosity_use", scored=True,
             body=frq_prompt(
                 intro="Watch the anchor check run on this weak draft, then write a fresh position of your own "
                       "and run the same check.",
                 setapart_block=setapart("Weak draft to diagnose:",
                                         "Curiosity is important and society should support it because it helps "
                                         "everyone.", "red"),
                 checklist_block=checklist(title="Run the anchor check:", rows=[
                     ("Does it take a defensible position?", "Loosely, yes, it takes a side."),
                     ("Does it name one specific example the writer supplies?", "No. Add one concrete case."),
                     ("Is the example concrete, not a generality?", "No. 'Helps everyone' is a generality; name a real case."),
                 ]),
                 closer="Now write a fresh position on the curiosity prompt that passes all three, then name the "
                        "specific example you anchored it to.")),

        # ===== INDEPENDENT: cold write, no frame, autonomy + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Anchor a position on your own",
             ref="", bank="sfa_curiosity_use", rubric_ref="rc.ap", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="On your own now, no frame. The prompt: should a society support inquiry that has no "
                       "foreseeable use?",
                 closer="Take the side you actually hold, then anchor it with one specific example from your own "
                        "reading, studies, or experience. This position-plus-anchor move is what every real "
                        "source-free argument is built on, and you are ready to do it cold. Run the 3 questions "
                        "before you submit.")),

        # ===== TRANSFER: same move, the OTHER bound prompt (bank-partitioned) =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW prompt: tradition or progress?",
             ref="ACC-W910-SFA-PROMPT-0001", bank="sfa_tradition_progress",
             body=("Read this new source-free prompt on tradition versus progress. Again there is no passage, so "
                   "the example must come from you. Note specific cases you know that could anchor a position. "
                   "The prompt stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Anchor a position on a NEW prompt",
             ref="", bank="sfa_tradition_progress", rubric_ref="rc.ap", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="New prompt. The task: does genuine progress require breaking with tradition?",
                 closer="Same position-plus-anchor move as the curiosity prompt, new topic. Take a defensible "
                        "side and anchor it to one specific example from your own knowledge. Do not stay general. "
                        "Run the 3 questions before you submit.")),
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
