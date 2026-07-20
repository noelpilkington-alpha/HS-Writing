"""
lesson_g9_l18_fresh_paragraph_selfcheck.py  -  G9 KC C.9.06/build, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD, ceiling essay).

G9 course L18 (Unit 3, independent). Write a fresh complete body paragraph (B1) from scratch, then run R3, the
self-check-own-fresh move: apply a faultless yes/no checklist to your ONE new paragraph. This is the first
lesson to feature R3 (the stateless-legal own-work self-check: observable meets/misses items, NOT "is my
reasoning strong?"). Locked L01 template. EVIDENCE-TIER binds full sources. Taught: COMMUNITYSERVICE (full) ->
transfer: MIGRATION (full, partitioned). rc.staar. BUILD=proposal. The self-check runs on the paragraph
written IN THIS SAME slot (no prior-work look-back; stateless-safe). No coping-model persona; no source markup;
no em dashes. Runs QC on execution.
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
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> a self-check that guesses instead of checking</span>'
    '<p style="margin:8px 0 0;font-size:15px">Self-check: "Is my paragraph good? Yes, it feels strong."</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">"Does it feel strong" cannot be answered by '
    'looking, so it just confirms what the writer already hoped. A vague self-check catches nothing.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> a checklist of observable yes/no items</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">CHECKABLE</span> 1) Is there a claim? 2) Is there a fact with its source named? '
      '3) Is there a warrant that says WHY the fact supports the claim? 4) Do the sentences connect with '
      'functional transitions?</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Each item can be answered by looking at the '
    'paragraph, yes or no. A checkable self-check finds the missing part; a vague one does not.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C906-0018", grade="9-10", lesson_type=7,
    unit="G9 U3 - Build (write a fresh paragraph + self-check)",
    title="Write a Fresh Paragraph, Then Check It Yourself",
    target=("Write a complete body paragraph from scratch, then run a faultless yes/no checklist on your own "
            "paragraph to catch any missing part before you submit. Written at the paragraph. Trait: "
            "Development/Organization."),
    acc_tags=["ACC.W.PROD.1", "ACC.W.PROC.1", "CCSS.W.9-10.1", "CCSS.W.9-10.5"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12",
                "mnemonic_status": "proposal", "kc": "C.9.06", "sot": "icm course-G9.md L18",
                "taught_stimulus": "ACC-W910-ARG-LESSON-COMMUNITYSERVICE",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-MIGRATION",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": "locked L01 template; EVIDENCE-TIER binds full sources. Features R3 self-check-own-fresh (BND, 1 item, stateless-safe).",
                "council": ("T7/BUILD independent rung: write a fresh complete body paragraph + run R3 self-"
                            "check (faultless observable yes/no items on the student's OWN paragraph, in-slot; "
                            "NOT 'is it good?'). checkable-vs-vague-self-check discrimination labeled Grade-C. "
                            "Self-check operates on the paragraph written in THIS slot, no prior-work look-back "
                            "(stateless-safe). BUILD=proposal.")},
    fade_ledger_moves=["write-fresh-complete-paragraph", "R3-self-check-own-fresh"],
    slots=[
        Slot("TEACH", "teach_card", "Write it, then check it against a real list",
             body=("Today you write a complete body paragraph on your own, with all three parts: a claim, "
                   "attributed evidence, and a warrant. A warrant is a sentence that explains WHY the evidence "
                   "supports the claim. All three are connected so they flow. Then you do something writers often skip: you check your own work "
                   "against a real list before you submit. A good self-check uses observable yes/no items, "
                   "things you can answer just by looking, like 'Is there a warrant?' A bad self-check asks "
                   "'Is it good?' or 'Does it feel strong?', which you cannot answer by looking, so it just "
                   "confirms what you already hoped. The reason to self-check with a real list is that writers "
                   "usually rate their own work higher than a scorer would, so a vague check catches nothing. "
                   "Goal today: build a fresh paragraph, then run a checkable list on it and fix any missing "
                   "part.")),
        Slot("TEACH", "stimulus_display", "Read the source: required community service",
             ref="ACC-W910-ARG-LESSON-COMMUNITYSERVICE", bank="community_service",
             body=("Read this source about required community service. Because your job is to BUILD a paragraph "
                   "with real evidence, read the whole thing and pick one fact you can quote or paraphrase, and "
                   "note who reports it. The text stays on screen while you work.")),
        Slot("TEACH", "discrimination", "Which self-check actually checks?",
             ref="", labeled_grade_c=True, bank="community_service",
             body=("Sort these before you write (spotting the target first, a Grade-C design bet we label as a "
                   "bet, not a proven ingredient). Which self-check uses observable yes/no items you can answer "
                   "by looking? "
                   "(A) Does my paragraph sound good, feel strong and convincing, and read like the best, "
                   "most impressive work I am able to do?  "
                   "(B) Does my paragraph have a claim, a fact with its source named, and a warrant that says "
                   "why the fact supports the claim? "
                   "Correct: B. (A) asks about feelings ('strong,' 'sounds good') that cannot be answered by "
                   "looking, so it confirms whatever the writer hoped. (B) names observable parts, each a "
                   "yes-or-no you can check on the page. A checkable list is the one that finds a missing "
                   "part.")),
        Slot("MODEL", "annotated_before_after", "Watch a vague self-check become a checkable one",
             bank="community_service",
             body=("Here is a vague self-check being rebuilt into a checkable list. Read the BEFORE, then the "
                   "AFTER, and notice the feeling-question replaced with observable yes/no items."
                   + BEFORE_AFTER_HTML +
                   " The BEFORE asks 'does it feel strong,' which cannot catch a missing part. The AFTER lists "
                   "the actual parts, each a yes-or-no you can see. Turning the check into observable items is "
                   "the move.")),
        Slot("MODEL", "predict_the_fix", "What does this self-check most need?",
             bank="community_service",
             body=("Diagnose before the reveal. A student's self-check reads: 'I read it over and it seems "
                   "clear and pretty good, so I think it is done.' Which single change would most improve the "
                   "self-check? "
                   "(A) replace the feeling-based judgment with observable yes/no items (claim? evidence with "
                   "source? warrant? transitions?)  "
                   "(B) read the whole paragraph over slowly one more time and trust that any missing part will jump out at you as you reread  "
                   "(C) ask whether the paragraph is long enough yet and keep adding more sentences until it looks like a finished chunk  "
                   "(D) check the spelling carefully and fix every last typo so the finished paragraph looks clean and correct on the page"),
             feedback=("Correct: A. 'Seems clear and pretty good' is a feeling, not a check, so it cannot catch "
                       "a missing warrant or an unattributed fact. The fix is a list of observable items: is "
                       "there a claim, a fact with its source named, a warrant, and functional transitions? "
                       "Rereading (B), checking length (C), or checking only spelling (D) do not verify the "
                       "parts of a complete paragraph.")),
        Slot("SUPPORTED", "production_frq", "Build a complete paragraph to check",
             ref="", bank="community_service", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=("Write ONE complete body paragraph arguing a claim about required community service, with "
                   "all three parts: CLAIM, EVIDENCE (a fact from the source, attributed and folded in), and "
                   "WARRANT (why the evidence supports the claim), connected with functional transitions. This "
                   "is the paragraph you will self-check in the next step. Scored on Development/Organization.")),
        Slot("MODEL", "diagnosis_frq", "Run the checklist on a fresh paragraph you write here",
             ref="", bank="community_service", scored=True,
             body=("First watch the checklist run on a provided draft, then run it on a fresh paragraph you "
                   "write right here. Provided draft: 'Required service builds character. Schools should adopt "
                   "it.' Run the four-item check step by step. Item 1, claim? Yes. Item 2, fact with source "
                   "named? No, add attributed evidence. Item 3, warrant? No, add the why. Item 4, functional "
                   "transitions? Not yet. Now you: write a fresh complete body paragraph on required service "
                   "here, then run the same four yes/no items on the paragraph you just wrote in this box: "
                   "claim? evidence with source? warrant? transitions? For each No, fix that part. Finish by "
                   "naming which item you had to fix.")),
        Slot("INDEPENDENT", "production_frq", "Write a fresh paragraph and self-check it",
             ref="", bank="community_service", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=("On your own now. Write ONE complete body paragraph arguing a claim about required community "
                   "service (claim, attributed evidence, warrant, connected). Then run this checklist on the "
                   "paragraph you just wrote in this box, answering each yes or no: 1) Is there a claim? 2) Is "
                   "there a fact with its source named? 3) Is there a warrant that says why the fact supports "
                   "the claim? 4) Do the sentences connect with functional transitions? For every No, fix that "
                   "part before you submit. Scored on Development/Organization.")),
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: animal migration",
             ref="ACC-W910-INFO-LESSON-MIGRATION", bank="animal_migration",
             body=("Read this new source about animal migration. Because your job is to BUILD a paragraph with "
                   "real evidence, read the whole thing and pick one fact you can quote or paraphrase, and note "
                   "who reports it. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Write a fresh paragraph and self-check it (NEW topic)",
             ref="", bank="animal_migration", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=("New topic. Write ONE complete body paragraph making a point about animal migration (claim, "
                   "attributed evidence, warrant, connected). Then run the same four-item checklist on this "
                   "paragraph: claim? fact with source? warrant? functional transitions? "
                   "Fix every No before you submit. Same build-and-self-check move as the service paragraph, "
                   "new topic. Scored on Development/Organization.")),
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
