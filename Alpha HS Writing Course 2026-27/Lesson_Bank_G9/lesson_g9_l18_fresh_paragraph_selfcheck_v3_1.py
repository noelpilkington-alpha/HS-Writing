"""
lesson_g9_l18_fresh_paragraph_selfcheck_v3_1.py  -  G9 KC C.9.06, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD, ceiling essay). V3.1.

V3.1 (Noel 2026-07-14): rebuild of lesson_g9_l18_fresh_paragraph_selfcheck.py to the v3.1 spine
(icm/_config/v3_1-lesson-build-spec.md), on the canonical L01 v3.1 pattern. Same teaching point: write a
complete body paragraph from scratch, then run a faultless yes/no self-check (R3) on your OWN paragraph.
Changes vs v3:
  1. MODEL BEFORE THE QUIZ (KH): the coping-model before/after now PRECEDES the discrimination (worked
     example before the check); the discrimination moved from TEACH into the MODEL role.
  2. COPING-MODEL THINK-ALOUD (SRSD): the model is rewritten as a writer running her OWN self-check draft by
     draft (vague check catches nothing -> switch to a checkable list -> the checkable item finds the missing
     source -> fix). Still contains literal BEFORE and AFTER (content_depth). No named near-peer.
  3. STRUCTURED DISCRIMINATION (DI faultless communication): choices=[{id,text,correct,why}]; the correct
     option is NOT the lone longest; NO leaked internal label (the v3 'Grade-C design bet' text is gone from
     student view - the design rationale lives in provenance/comments).
  4. FIXED THE 'reread' ANSWER CUE (Fable finding): the v3 predict-the-fix distractor (B) contained 'reread';
     reworded so no option carries retry/feedback phrasing (leaked_answer_cue).
  5. FRQ/DIAGNOSIS BODIES rebuilt with frq_prompt/checklist/setapart (no 'Step N' prose, no 'Scored on ...'
     chrome); the 4-item self-check renders as a real <ol> via checklist(...).
  6. TEACH split into a list (no wall of text); the reusable 4-item check tool (REMEMBER) is attached at the
     MODEL card, its point of first use, not cold in step 1 (KH load).
  7. AUTONOMY + SAY-THE-STANDARD (Yeager) on the independent write.

ONE IDEA: a real self-check asks only what you can SEE on the page, yes or no. ONE REMINDER: the 4-item check.
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
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A real self-check asks only what you can '
'<strong>SEE</strong> on the page, answered <strong>yes or no</strong>. "Does it feel strong?" checks nothing. '
'"Is there a fact with its source named?" checks something you can fix.</div></div>')

# the reusable check tool, folded in at the MODEL card (point of first use), as a real <ol> list.
REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 4 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit any body paragraph, run this on it:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Is there a claim?</li>'
'<li style="margin:2px 0">Is there a fact with its source named?</li>'
'<li style="margin:2px 0">Is there a warrant that says why the fact supports the claim?</li>'
'<li style="margin:2px 0">Do the sentences connect with functional transitions?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix that part before you submit.</div></div>')

# coping-model think-aloud: a writer running her OWN self-check draft by draft, then the literal endpoints.
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer checking her own paragraph, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First check:</strong> "Is my paragraph good? It reads strong, so I '
    'think it is done." Wait, can I answer "does it read strong" just by looking? No. That only repeats what '
    'I hoped. It caught nothing. Ask something I can see.</p>'
    '<p style="margin:0 0 8px"><strong>Second check:</strong> "Is there a claim? Yes. Is there a fact with its '
    'source named? ... No. I gave a fact but never said who reported it." That one I could answer by looking, '
    'and it found a real miss.</p>'
    '<p style="margin:0"><strong>Fix:</strong> I name the source on the fact, and now the same item reads Yes. '
    'The checkable question found the gap; the vague one hid it.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> a check that guesses: "Is my paragraph good? Yes, it feels '
    'strong." (cannot be answered by looking, so it catches nothing)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> a list of observable yes/no items: claim? fact with its source '
    'named? warrant (why the fact supports the claim)? transitions connect the sentences? (each answered just '
    'by looking)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C906-0018", grade="9-10", lesson_type=7,
    unit="G9 U3 - Build (write a fresh paragraph + self-check)",
    title="Write a Fresh Paragraph, Then Check It Yourself",
    target=("Write a complete body paragraph from scratch, then run a faultless yes/no checklist on your own "
            "paragraph to catch any missing part before you submit. Written at the paragraph. Trait: "
            "Development/Organization."),
    acc_tags=["ACC.W.PROD.1", "ACC.W.PROC.1", "CCSS.W.9-10.1", "CCSS.W.9-10.5"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-14",
                "mnemonic_status": "proposal", "kc": "C.9.06", "sot": "icm course-G9.md L18",
                "taught_stimulus": "ACC-W910-ARG-LESSON-COMMUNITYSERVICE",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-MIGRATION",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": ("v3.1 rebuild on the L01 v3.1 pattern; EVIDENCE-TIER binds full sources. Features "
                             "R3 self-check-own-fresh (faultless observable yes/no items on the student's OWN "
                             "paragraph, in-slot, stateless-safe)."),
                "one_idea": "A real self-check asks only what you can SEE on the page, yes or no.",
                "one_reminder": "The 4-item paragraph check: claim? fact with source? warrant? transitions?",
                "version_note": ("V3.1: rebuilt to the v3.1 spine (L01 v3.1 pattern). Model precedes the "
                                 "discrimination (KH worked-example-before-quiz); coping-model think-aloud on the "
                                 "self-check (vague -> checkable); discrimination moved to MODEL with structured "
                                 "choices (no leaked Grade-C/design-bet label, correct not lone-longest); "
                                 "predict-the-fix distractor reworded to drop the 'reread' answer cue; FRQ/diagnosis "
                                 "bodies rebuilt with frq_prompt/checklist/setapart (no Step-N prose, no 'Scored on' "
                                 "chrome); teach split into a list (no wall of text); the 4-item check tool attached "
                                 "at the model (point of first use); autonomy + say-the-standard on the independent "
                                 "write (Yeager)."),
                "council": ("T7/BUILD independent rung: write a fresh complete body paragraph + run R3 self-"
                            "check (faultless observable yes/no items on the student's OWN paragraph, in-slot; "
                            "NOT 'is it good?'). checkable-vs-vague-self-check discrimination labeled Grade-C in "
                            "code (not in student text). Self-check operates on the paragraph written in THIS slot, "
                            "no prior-work look-back (stateless-safe). BUILD=proposal."),
                "review_provenance": ("v3.1 rebuild against v3_1-lesson-build-spec.md + lesson_contract 23 gates "
                                      "+ gated_reading render-QC, 2026-07-14.")},
    fade_ledger_moves=["write-fresh-complete-paragraph", "R3-self-check-own-fresh"],
    slots=[
        # ===== TEACH: ONE idea + the parts of a complete paragraph + checkable-vs-vague (as a list) =====
        Slot("TEACH", "teach_card", "Write it, then check what you can see",
             body=(ONE_IDEA +
                   "Today you write a complete body paragraph on your own. A complete body paragraph has three "
                   "parts that work together:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>CLAIM</strong>: the point you are arguing about the "
                   "topic.</li>"
                   "<li style=\"margin:4px 0\"><strong>EVIDENCE</strong>: a fact from the source, with the "
                   "person or group who reported it named.</li>"
                   "<li style=\"margin:4px 0\">A <strong>warrant</strong> is a sentence that explains why the "
                   "fact supports the claim (the reason it counts).</li></ul>"
                   "Connect the three so they flow. Then you do the move writers usually skip: you check your "
                   "own work against a real list. A good self-check uses observable yes/no items, things you "
                   "can answer just by looking, like 'Is there a warrant?' A weak self-check asks 'Is it "
                   "good?' or 'Does it feel strong?', which you cannot answer by looking, so it just confirms "
                   "what you already hoped. Writers usually rate their own work higher than a scorer would, so "
                   "a vague check catches nothing. Goal today: build a fresh paragraph, then run a checkable "
                   "list on it and fix any missing part.")),
        Slot("TEACH", "stimulus_display", "Read the source: required community service",
             ref="ACC-W910-ARG-LESSON-COMMUNITYSERVICE", bank="community_service",
             body=("Read this source about required community service. Because your job is to BUILD a paragraph "
                   "with real evidence, read the whole thing and pick one fact you can quote or paraphrase, and "
                   "note who reports it. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model think-aloud + the check tool folded in at first use =====
        Slot("MODEL", "annotated_before_after", "Watch a writer check her own paragraph",
             bank="community_service",
             body=("Here is the move in action. Follow the writer's thinking below. " + COPING_HTML +
                   " The two checks asked different kinds of question: one she could answer by looking, one she "
                   "could not. Only the observable, yes/no version found the missing source. " + REMEMBER +
                   "When you write your own paragraph, build all three parts, then run these four questions "
                   "before you submit.")),
        Slot("MODEL", "discrimination", "Which self-check actually checks?",
             ref="", labeled_grade_c=True, bank="community_service",
             body=("Now that you have seen both kinds of check, spot the target. Which self-check uses "
                   "observable yes/no items you can answer just by looking? "
                   "(A) Does my paragraph sound good, feel strong and convincing, and read like the best, most "
                   "impressive work I can do?  "
                   "(B) Does my paragraph have a claim, a fact with its source named, and a warrant?  "
                   "(C) Is my paragraph at least five or six sentences long, so it clearly counts as a full "
                   "paragraph?  "
                   "(D) Are all the words spelled correctly and the sentences free of grammar mistakes? "
                   "Correct: B. It names parts you can see on the page, each a yes-or-no. (A) asks about "
                   "feelings you cannot check by looking; (C) measures length, which does not tell you whether "
                   "the parts are there; (D) checks spelling and grammar, not whether the paragraph has a claim, "
                   "evidence, and a warrant."),
             choices=[
                 {"id": "A",
                  "text": "Does my paragraph sound good, feel strong and convincing, and read like the best, most impressive work I can do?",
                  "correct": False,
                  "why": "This asks about feelings ('sounds good,' 'feels strong') that you cannot answer just by looking, so it only confirms whatever you hoped. It catches no missing part."},
                 {"id": "B",
                  "text": "Does my paragraph have a claim, a fact with its source named, and a warrant?",
                  "correct": True,
                  "why": "Correct. Each part is something you can see on the page, a yes-or-no you can check. A checkable list is the one that finds a missing part."},
                 {"id": "C",
                  "text": "Is my paragraph at least five or six sentences long, so it clearly counts as a full paragraph?",
                  "correct": False,
                  "why": "Length is observable, but it does not tell you whether the parts are there. A paragraph can run five or six sentences and still be missing its warrant or leave a fact unattributed."},
                 {"id": "D",
                  "text": "Are all the words spelled correctly and the sentences free of grammar mistakes?",
                  "correct": False,
                  "why": "This checks spelling and grammar, not whether the paragraph has a claim, a fact with its source named, and a warrant. A clean paragraph can still be missing a required part."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this self-check most need?",
             bank="community_service",
             body=("Diagnose before the reveal. A student's self-check reads: 'I read it over and it seems "
                   "clear and pretty good, so I think it is done.' Which single change would most improve the "
                   "self-check? "
                   "(A) replace the feeling-based judgment with observable yes/no items (claim? evidence with "
                   "source? warrant? transitions?)  "
                   "(B) read the whole paragraph over slowly one more time and simply trust that any missing part will somehow jump out at you on its own  "
                   "(C) ask whether the paragraph is long enough yet and keep adding more sentences until it looks like a finished chunk  "
                   "(D) check the spelling carefully and fix every last typo so the finished paragraph looks clean and correct on the page"),
             feedback=("Correct: A. 'Seems clear and pretty good' is a feeling, not a check, so it cannot catch "
                       "a missing warrant or an unattributed fact. The fix is a list of observable items: is "
                       "there a claim, a fact with its source named, a warrant, and functional transitions? "
                       "Reading it again (B), checking length (C), or checking only spelling (D) do not verify "
                       "the parts of a complete paragraph.")),

        # ===== SUPPORTED: framed write (fill-in frame) on the taught topic =====
        Slot("SUPPORTED", "production_frq", "Build a complete paragraph to check",
             ref="", bank="community_service", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on getting all three parts in.",
                 setapart_block=setapart("Fill in each part of this frame:",
                                         "Required community service should ______ [your claim]. According to ______ [the source], ______ [a fact]. This supports the claim because ______ [your warrant]."),
                 closer="Write ONE complete body paragraph about required community service with a claim, a fact "
                        "from the source with its source named, and a warrant, connected so they flow. This is "
                        "the paragraph you will self-check next.")),
        # ===== INDEPENDENT: cold write on the taught topic + autonomy + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write a fresh paragraph and self-check it",
             ref="", bank="community_service", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="On your own now, no frame. Write ONE complete body paragraph arguing a claim about "
                       "required community service: a claim, a fact from the source with its source named, and "
                       "a warrant, all connected so they flow.",
                 checklist_block=checklist(
                     title="Then run this check on the paragraph you just wrote in this box, answering each yes or no:",
                     rows=[
                         "Is there a claim?",
                         "Is there a fact with its source named?",
                         "Is there a warrant that says why the fact supports the claim?",
                         "Do the sentences connect with functional transitions?",
                     ]),
                 closer="For every No, fix that part before you submit. This build-it-then-check-it move is what "
                        "strong writers do on every paragraph, and you are ready to run it on your own.")),

        # DIAGNOSIS = watch the check run on a PROVIDED weak draft, then run it on a FRESH paragraph written in
        # this same slot (no prior-work look-back; stateless-safe). Produces no reused claim.
        Slot("MODEL", "diagnosis_frq", "Run the checklist on a fresh paragraph you write here",
             ref="", bank="community_service", scored=True,
             body=frq_prompt(
                 intro="First watch the four-item check run on a weak draft, then run it on a fresh paragraph you write here.",
                 setapart_block=setapart("Weak draft:", "Required service builds character. Schools should adopt it.", "red"),
                 checklist_block=checklist(title="Run the check on the weak draft:", rows=[
                     ("Is there a claim?", "Yes, 'schools should adopt it' takes a side."),
                     ("Is there a fact with its source named?", "No. Add a fact and name who reports it."),
                     ("Is there a warrant that says why the fact supports the claim?", "No. Add the why."),
                     ("Do the sentences connect with functional transitions?", "Not yet. Add connectors so they flow."),
                 ]),
                 closer="Now write a fresh complete body paragraph on required service here, then run the same "
                        "four yes/no items on the paragraph you just wrote in this box. For each No, fix that "
                        "part. Finish by naming which item you had to fix.")),

        # ===== TRANSFER: same move, a NEW topic (animal migration), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: animal migration",
             ref="ACC-W910-INFO-LESSON-MIGRATION", bank="animal_migration",
             body=("Read this new source about animal migration. Because your job is to BUILD a paragraph with "
                   "real evidence, read the whole thing and pick one fact you can quote or paraphrase, and note "
                   "who reports it. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Write a fresh paragraph and self-check it (NEW topic)",
             ref="", bank="animal_migration", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="New topic. Write ONE complete body paragraph making a point about animal migration: a "
                       "claim, a fact from the source with its source named, and a warrant, all connected.",
                 checklist_block=checklist(
                     title="Then run the same four-item check on this paragraph, answering each yes or no:",
                     rows=[
                         "Is there a claim?",
                         "Is there a fact with its source named?",
                         "Is there a warrant that says why the fact supports the claim?",
                         "Do the sentences connect with functional transitions?",
                     ]),
                 closer="Fix every No before you submit. Same build-and-self-check move as the service "
                        "paragraph, on a fresh topic.")),
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
