"""
lesson_g9_l17_build_paragraph_v3_1.py  -  G9 KC C.9.06/build, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD, ceiling essay). V3.1.

Rebuild of lesson_g9_l17_build_paragraph.py to the v3.1 lesson-build standard (icm/_config/v3_1-lesson-build-spec.md),
using G9 L01 v3.1 as the canonical exemplar. Teaching point is UNCHANGED: assemble one COMPLETE body paragraph with
all three parts joined so they connect (CLAIM + EVIDENCE + WARRANT, cohesive). KC C.9.06. Bound stimuli kept:
PHONEBAN (full source, taught) -> SCHOOLLUNCH (full source, transfer, partitioned). Preserved verbatim from the
current L17: id="ACC-W910-L-G9-C906-0017", lesson_type=7, provenance mnemonic_status="proposal", every
production_frq unit="paragraph" (type-7 ceiling is 'essay', so paragraph is within ceiling).

V3.1 changes applied to the current L17:
  1. ONE-IDEA callout + LIST teach (was a 132-word wall of text -> format_fidelity fail). The three parts are a
     real <ul>; the term WARRANT is defined in plain words in the TEACH body (faultless communication).
  2. MODEL BEFORE THE QUIZ (KH): the annotated before/after now PRECEDES the discrimination, and the discrimination
     is MODEL-role. The reusable 3-part CHECK TOOL is attached at the model, at the point of first use.
  3. COPING-MODEL THINK-ALOUD (SRSD): the before/after is rewritten as a written drafting process (draft partial ->
     run the check -> catch the missing warrant -> add it). Still carries a literal BEFORE and AFTER (content_depth).
     No named near-peer (Timeback stateless rule).
  4. FIXED THE 'BECAUSE' CONFOUND (DI, faultless communication) + explicit choices=[]: the complete (correct) option
     joins the warrant WITHOUT the word 'because'; a WRONG distractor uses 'because' on a survey-scope clause that is
     not a warrant. Correct option is NOT the lone longest. No leaked internal label ('Grade-C'/'design bet' removed).
  5. STRUCTURED FRQ / DIAGNOSIS bodies via lesson_prompts (frq_prompt/setapart/checklist): no 'Step 1/2' prose (was
     the render-QC double-numbering fail), no 'Scored on ...' rubric chrome.
  6. AUTONOMY + SAY-THE-STANDARD (Yeager) on the independent write.

ONE IDEA: a complete body paragraph joins three parts so they connect: CLAIM, EVIDENCE, WARRANT.
ONE REMINDER: the 3-part check (claim stated? evidence attributed? warrant present?).
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
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A complete body paragraph joins <strong>three parts</strong> '
'so they connect: a <strong>CLAIM</strong>, the <strong>EVIDENCE</strong>, and a <strong>WARRANT</strong>. Stop before '
'the warrant and the paragraph is only partly built.</div></div>')

# the reusable 3-part CHECK TOOL, attached at the model (point of first use), as a real <ol>.
REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 parts</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit any body paragraph, run this quick check:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Is the CLAIM (your point) stated?</li>'
'<li style="margin:2px 0">Is the EVIDENCE a fact from the source, attributed and folded in?</li>'
'<li style="margin:2px 0">Is the WARRANT there, explaining why the evidence supports the claim?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any part is missing, the paragraph is not finished yet.</div></div>')

# coping-model think-aloud: a WRITTEN drafting process (draft the partial -> run the check -> catch the missing
# warrant -> add it), then the literal BEFORE and AFTER endpoints (content_depth needs BOTH inline). No named peer.
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer building the paragraph, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First draft:</strong> "Schools should limit phone use during class. The '
    'National Center for Education Statistics reports that about 76.9 percent of public schools already prohibited '
    'non-academic cell phone use." Run the check: claim? Yes. Evidence, attributed? Yes. Warrant? No, it stops after '
    'the fact and never says why that number supports the claim. Not finished.</p>'
    '<p style="margin:0"><strong>Adds the warrant:</strong> "That figure matters because it shows the limit is '
    'already workable rather than radical: when more than three out of four schools have made the rule stick, a new '
    'school can reasonably expect to enforce it too." Now all three parts are joined. That passes.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> claim and attributed evidence, but no warrant, so the paragraph is only partly built.</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> '
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;font-weight:700">CLAIM</span> '
      'Schools should limit phone use during class. '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;font-weight:700">EVIDENCE</span> '
      'The National Center for Education Statistics reports that about 76.9 percent of public schools already '
      'prohibited non-academic cell phone use during the school day. '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;font-weight:700">WARRANT</span> '
      'That figure matters because it shows the limit is already workable rather than radical, so a new school can '
      'reasonably expect to enforce it too. (all three parts, joined)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C906-0017", grade="9-10", lesson_type=7,
    unit="G9 U3 - Build (assemble a complete body paragraph)",
    title="Build a Body Paragraph That Connects: Claim, Evidence, Warrant + Cohesion",
    target=("Assemble a complete body paragraph AND connect it: the three parts (claim, attributed evidence, "
            "warrant) now joined with the cohesion tools from this unit, a transition that names the real "
            "relationship and no vague reference. This is the paragraph-build from Unit 2, upgraded with the "
            "connective tissue. Written at the paragraph. Trait: Development/Organization/Cohesion."),
    acc_tags=["ACC.W.PROD.1", "CCSS.W.9-10.1"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-14",
                "mnemonic_status": "proposal", "kc": "C.9.06", "sot": "icm course-G9.md L17",
                "taught_stimulus": "ACC-W910-ARG-LESSON-PHONEBAN",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-SCHOOLLUNCH",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "one_idea": "A complete body paragraph joins three parts so they connect: CLAIM, EVIDENCE, WARRANT.",
                "one_reminder": "3-part check: claim stated? evidence attributed? warrant present?",
                "template": "locked L01 template; EVIDENCE-TIER binds full sources. T7 BUILD works at paragraph here (below essay ceiling).",
                "version_note": ("V3.1: rebuilt to the v3.1 standard (L01 v3.1 exemplar). ONE-IDEA + list teach (fixed "
                                 "the 132-word wall of text), model+check-tool BEFORE the quiz (KH), coping-model "
                                 "think-aloud drafting the missing warrant (SRSD), fixed the 'because' confound with "
                                 "explicit choices (DI faultless communication), removed the leaked 'Grade-C/design "
                                 "bet' label, structured FRQ/diagnosis bodies via lesson_prompts (no Step 1/2 prose, "
                                 "no 'Scored on' chrome), autonomy + say-the-standard on the independent write."),
                "council": ("T7/BUILD first rung: assemble B1 complete body paragraph (claim+evidence+warrant, "
                            "cohered), pulling together every Unit 1-3 move. complete-vs-partial-paragraph "
                            "discrimination labeled Grade-C in code. BUILD=proposal; unit=paragraph (within essay ceiling)."),
                "review_provenance": ("v3.1 build spec (icm/_config/v3_1-lesson-build-spec.md); 23 lesson_contract "
                                      "gates + gated_reading render-QC, 2026-07-14.")},
    fade_ledger_moves=["assemble-complete-body-paragraph", "claim-evidence-warrant-cohered"],
    slots=[
        # ===== TEACH: ONE idea + the three parts as a LIST; define WARRANT in plain words =====
        Slot("TEACH", "teach_card", "The three parts of a complete body paragraph",
             body=(ONE_IDEA +
                   "You have practiced every part; today you assemble them. A complete body paragraph has three "
                   "parts, joined so they connect:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>CLAIM</strong>: the point this paragraph argues.</li>"
                   "<li style=\"margin:4px 0\"><strong>EVIDENCE</strong>: a fact from a source, attributed (name "
                   "who reports it) and folded into your own sentence.</li>"
                   "<li style=\"margin:4px 0\"><strong>WARRANT</strong>: this is a sentence that explains WHY that "
                   "evidence supports the claim.</li></ul>"
                   "The most common problem at this step is the partial paragraph: a claim and evidence, but no "
                   "warrant, so the reader never learns why the fact matters. You are not learning new moves today; "
                   "you are building the moves you know into one solid unit of writing.")),
        Slot("TEACH", "stimulus_display", "Read the source: phones in school",
             ref="ACC-W910-ARG-LESSON-PHONEBAN", bank="phone_ban",
             body=("Read this source about phones in school. Because your job is to BUILD a paragraph with real "
                   "evidence, read the whole thing and note one fact you can quote or paraphrase, and who reports "
                   "it. You will use it as the evidence in your paragraph. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model think-aloud + the reusable 3-part check tool =====
        Slot("MODEL", "annotated_before_after", "Watch a writer finish a partial paragraph",
             bank="phone_ban",
             body=("Here is the build in action. A writer drafts a partial paragraph, runs the check, catches the "
                   "missing warrant, and adds it. Follow the thinking below. " + COPING_HTML +
                   " The BEFORE stops after the evidence. The AFTER adds the warrant that explains why the fact "
                   "supports the claim, so all three parts connect. " + REMEMBER +
                   "When you build your own, use this same check before you submit.")),
        Slot("MODEL", "discrimination", "Which paragraph is complete, and which is partial?",
             ref="", labeled_grade_c=True, bank="phone_ban",
             body=("Now that you have seen one built, spot the target. All three start the same way. Which is a "
                   "COMPLETE body paragraph (claim + evidence + warrant)? "
                   "(A) Schools should limit phones in class. The National Center for Education Statistics reports that most public schools already restrict non-academic phone use during the school day.  "
                   "(B) Schools should limit phones in class. The National Center for Education Statistics reports most public schools already restrict such use, and that wide adoption shows the limit is workable, not radical.  "
                   "(C) Schools should limit phones in class. The National Center for Education Statistics reports most public schools already restrict such use, because the survey gathered responses from thousands of public school districts.  "
                   "(D) Schools should limit phones in class. The National Center for Education Statistics reports most public schools already restrict such use, and phones can pull students' attention away during lessons. "
                   "Correct: B. It has the claim, attributed evidence, AND a warrant that says why the fact supports the claim."),
             choices=[
                 {"id": "A", "text": "Schools should limit phones in class. The National Center for Education Statistics reports that most public schools already restrict non-academic phone use during the school day.",
                  "correct": False,
                  "why": "Partial. It has a claim and attributed evidence but no warrant, so it never says why the fact supports the claim."},
                 {"id": "B", "text": "Schools should limit phones in class. The National Center for Education Statistics reports most public schools already restrict such use, and that wide adoption shows the limit is workable, not radical.",
                  "correct": True,
                  "why": "Correct. Claim, attributed evidence, AND a warrant (why the fact supports the claim), joined so they connect, even without the word 'because.' All three parts is what makes it complete."},
                 {"id": "C", "text": "Schools should limit phones in class. The National Center for Education Statistics reports most public schools already restrict such use, because the survey gathered responses from thousands of public school districts.",
                  "correct": False,
                  "why": "It has the word 'because,' but the clause only explains how the survey was run, not why the fact supports limiting phones. A because-clause is not automatically a warrant."},
                 {"id": "D", "text": "Schools should limit phones in class. The National Center for Education Statistics reports most public schools already restrict such use, and phones can pull students' attention away during lessons.",
                  "correct": False,
                  "why": "The added clause is a second reason for the claim, not a warrant. It never links back to the reported fact to say why that fact (most schools already restrict phones) supports limiting phones, so the evidence and its explanation are still not connected."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this partial paragraph most need?",
             bank="phone_ban",
             body=("Diagnose before the reveal. A paragraph reads: 'Phones distract students during lessons. "
                   "The National Center for Education Statistics reports that most schools now restrict phone "
                   "use.' Which single move would most improve it as a body paragraph? "
                   "(A) add a warrant explaining WHY that fact supports limiting phones, finishing the three-part paragraph  "
                   "(B) add a second piece of evidence from another source so the paragraph stacks up even more facts behind the phone claim  "
                   "(C) restate the claim about phones once more at the very end so the paragraph circles back and reminds readers of its point  "
                   "(D) make the sentences shorter and simpler so the two facts read a little more smoothly and feel less crowded on the page"),
             feedback=("Correct: A. The paragraph has a claim and attributed evidence but no warrant, so it is "
                       "partial. The fix completes it, for example: 'This widespread restriction matters because "
                       "it shows schools already treat phones as a real distraction worth managing.' A second fact "
                       "(B) or a restated claim (C) do not supply the missing reasoning, and shorter sentences (D) "
                       "do not add the warrant.")),

        # ===== SUPPORTED: framed write, build two of the three parts onto a given claim =====
        Slot("SUPPORTED", "production_frq", "Build two of the three parts", ref="", bank="phone_ban",
             rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="Warm up the build. Start from the given claim, then add the other two parts.",
                 setapart_block=setapart("Start from this claim, then build onto it:",
                                         "CLAIM (given): Schools should limit phones during class. Now write the "
                                         "EVIDENCE (a fact from the source, attributed and folded in) and the "
                                         "WARRANT (why that fact supports the claim)."),
                 closer="Write those two sentences so the evidence and warrant connect with a linking word. You "
                        "are building two of the three parts onto the given claim.")),
        # DIAGNOSIS: run the 3-part check on a PROVIDED weak draft, then on a fresh paragraph of your own. Stays on
        # the taught topic (no new source to read). Structured via checklist (no 'Step N' prose).
        Slot("MODEL", "diagnosis_frq", "Check the parts, then build a fresh paragraph", ref="", bank="phone_ban",
             scored=True,
             body=frq_prompt(
                 intro="First watch the 3-part check run on a weak draft, then run it on a fresh paragraph of your own.",
                 setapart_block=setapart("Weak draft to check:", "Phones hurt focus. Most schools restrict them.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Is the CLAIM clear?", "Yes, 'phones hurt focus' states the point."),
                     ("Is the EVIDENCE attributed and folded in?", "No, the fact is dropped with no source. Name who reports it."),
                     ("Is the WARRANT there?", "No. Add a sentence saying why that fact supports the claim."),
                 ]),
                 closer="Now write one fresh claim-plus-evidence-plus-warrant for the phone topic, then run the "
                        "same three checks and fix any part that fails. Finish by naming which of the three parts "
                        "your paragraph needed most.")),

        # ===== INDEPENDENT: cold full-paragraph build on the taught topic + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Build a complete body paragraph", ref="", bank="phone_ban",
             rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="On your own now, build the whole paragraph.",
                 closer="Write ONE complete body paragraph arguing a claim about phones in class, with all three "
                        "parts in order: CLAIM (your point), EVIDENCE (a fact from the source, attributed and "
                        "folded in), and WARRANT (why the evidence supports the claim), connected so they flow. "
                        "Before you submit, run the 3-part check and fix any part that fails. This three-part build "
                        "is what every body paragraph in a real argument rests on, and you are ready to do it cold.")),

        # ===== TRANSFER: same build, a NEW source (free meals), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: free school meals",
             ref="ACC-W910-ARG-LESSON-SCHOOLLUNCH", bank="school_lunch",
             body=("Read this new source about free school meals. Because your job is to BUILD a paragraph with real "
                   "evidence, read the whole thing and note one fact you can quote or paraphrase, and who reports "
                   "it. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Build a complete body paragraph on a NEW topic", ref="",
             bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=frq_prompt(
                 intro="New topic, same build. The task: argue a claim about free school meals.",
                 closer="Write ONE complete body paragraph with all three parts in order: CLAIM, EVIDENCE "
                        "(attributed and folded in), and WARRANT (why the evidence supports the claim), connected "
                        "so they flow. Same build as the phone paragraph, fresh topic. Do not stop at a partial "
                        "paragraph that skips the warrant. Run the 3-part check before you submit.")),
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
