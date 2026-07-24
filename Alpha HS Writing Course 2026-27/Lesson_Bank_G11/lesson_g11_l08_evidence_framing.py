"""
lesson_g11_l08_evidence_framing.py  -  G11 KC C.11.03, ARCHETYPE T3: EVIDENCE-INTEGRATION (PROVE, ceiling paragraph). V3.1.

G11 course L08 (Unit 2, intro), rebuilt to the v3.1 build spec. Teaching point (kept): use evidence well in
analysis by TRIMMING to the smallest phrase that earns its place and FRAMING it (set it up before, interpret it
after), instead of dumping a long quote that floats. KC C.11.03, lesson_type=3, mnemonic_status=established-caveat.
Bound stimuli preserved: Douglass 1852 speech taught (douglass_1852) -> Emerson "Self-Reliance" transfer
(ra_essay_1, cold). Unit climbs sentence -> paragraph (type-3 ceiling = paragraph). v3.1 spine: ONE_IDEA teal
callout + list teach, coping-model think-aloud (First/Second/Final, literal BEFORE/AFTER), REMEMBER dashed
check-tool, explicit-choices discrimination, deterministic FRQ prompts. No named person, no source markup, no
prior-work ref, no em dashes. Runs QC on execution (23 gates).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">Quote less, and frame what you quote. '
'<strong>Trim</strong> to the smallest phrase that carries your point, then <strong>frame</strong> it: '
'framing a quote means setting it up before and interpreting it after, so it never floats alone.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, run every quote through these three:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0"><strong>Trimmed?</strong> Have you quoted only the load-bearing phrase, not a whole passage?</li>'
'<li style="margin:2px 0"><strong>Set up?</strong> Is there a lead-in before the quote that says what to notice?</li>'
'<li style="margin:2px 0"><strong>Interpreted?</strong> Is there a follow after the quote that says what it does?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">A "no" on any one, and the quote is dumped or floating. Fix it.</div></div>')

COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer using one Douglass line as proof, drafting and checking as they go:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Douglass says, \'I am not included within the pale of '
    'this glorious anniversary. Your high independence only reveals the immeasurable distance between us.\' This '
    'shows he feels left out." Check: is it trimmed? No, two full sentences quoted. Is it framed? No, just a flat '
    'label after it. Too much quoted, no set-up, no real interpretation.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "Douglass calls their \'high independence\' the thing '
    'that \'reveals the immeasurable distance between us.\'" Check: trimmed now, good. Set up? Interpreted? No. The '
    'phrase still floats: I never say what to notice or what it does.</p>'
    '<p style="margin:0"><strong>Final:</strong> "To measure the gap he means, Douglass borrows the audience\'s own '
    'pride, calling their \'high independence\' the very thing that \'reveals the immeasurable distance between '
    'us,\' so their celebration becomes the yardstick of his exclusion." Trimmed, set up, and interpreted.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> A long quote dumped in with no lead-in and a flat label: the '
    'reader hunts for what matters and never learns why it matters.</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> One trimmed phrase, set up before and interpreted after, so the '
    'quote carries a clear point instead of floating.</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1103-0008", grade="9-10", lesson_type=3,
    unit="G11 U2 - Rhetorical analysis (trim and frame the evidence)",
    title="Trim the Quote, Then Frame It",
    target=("Use evidence well in analysis: trim to the smallest phrase that earns its place, and frame it (set "
            "it up before, interpret it after), instead of dumping a long quote that floats. Written at the "
            "sentence, building to the paragraph. Trait: Evidence and Commentary."),
    acc_tags=["ACC.W.SRC.2", "CCSS.W.11-12.8"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "established-caveat", "kc": "C.11.03", "sot": "icm course-G11.md L08",
                "taught_stimulus": "ACC-W910-ANALYSIS-LESSON-DOUGLASS",
                "transfer_stimulus": "ACC-W910-RA-SINGLE-0003",
                "playbook": "_phase2/playbook_T3_PROVE.md",
                "one_idea": "Quote less, and frame what you quote: trim to the smallest proof, set it up, interpret it.",
                "one_reminder": "Run each quote through 3 checks: trimmed? set up? interpreted?",
                "template": "locked L01 template; ANALYSIS/EVIDENCE-TIER binds full sources.",
                "version_note": ("V3.1 rebuild: replaced prose-wall body + leaked Grade-C labels with the v3.1 "
                                  "spine (ONE_IDEA teal callout + list teach, coping-model First/Second/Final "
                                  "with literal BEFORE/AFTER, REMEMBER dashed check-tool, explicit-choices "
                                  "discrimination, deterministic FRQ prompts). Kept id/type/KC/unit/bound stimuli "
                                  "+ the trim-and-frame teaching point. Fixed doubled distractor text in "
                                  "predict-the-fix."),
                "council": ("T3/PROVE G11 evidence rung: introduces trim-to-smallest-proof + frame-the-evidence. "
                            "trimmed-and-framed-vs-dumped discrimination labeled_grade_c in code only (not "
                            "student-facing). PROVE=established-caveat.")},
    fade_ledger_moves=["trim-to-smallest-proof", "frame-the-evidence"],
    slots=[
        Slot("TEACH", "teach_card", "The one idea: trim, then frame",
             body=(ONE_IDEA +
                   "In analysis, how you use a quote matters as much as which quote you pick. Two moves do the "
                   "work:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Trim to the smallest proof</strong>: quote only the exact "
                   "phrase that carries your point, not a whole paragraph. A dumped long quote makes the reader "
                   "hunt for what matters.</li>"
                   "<li style=\"margin:4px 0\"><strong>Frame the evidence</strong>: set the quote up before (say "
                   "what to notice) and follow it after (say what it does), so the quote never floats alone.</li>"
                   "</ul>"
                   "The trap is the over-quoted, unframed dump followed by a flat label like \"this shows he "
                   "feels excluded.\" Goal today: trim to the load-bearing phrase, then frame it before and "
                   "after.")),
        Slot("TEACH", "stimulus_display", "Read the source: Frederick Douglass, 1852 address (excerpt)",
             ref="ACC-W910-ANALYSIS-LESSON-DOUGLASS", bank="douglass_1852",
             body=("Read this excerpt. Find a short phrase (not a whole passage) you could quote as proof for an "
                   "analytical point, and think about how to set it up and follow it. The text stays on screen "
                   "while you work.")),
        Slot("MODEL", "annotated_before_after", "Watch a writer trim and frame a quote",
             bank="douglass_1852",
             body=("Here is the skill in action. Follow the writer draft a sentence, run the check, catch the "
                   "problem, and fix it. " + COPING_HTML +
                   " Notice the difference: the first try dumps a long quote and labels it; the final version "
                   "trims to the key phrase and frames it before and after." + REMEMBER +
                   "When you use your own quote, trim first, then set it up and interpret it, then run the "
                   "3-question check.")),
        Slot("MODEL", "discrimination", "Which handles the quote well?",
             ref="", labeled_grade_c=True, bank="douglass_1852",
             body=("Spot the target before you write. Which option TRIMS and FRAMES the quote, rather than "
                   "dumping it or dropping the proof? "
                   "(A) Douglass says, \"I am not included within the pale of this glorious anniversary. Your "
                   "high independence only reveals the immeasurable distance between us.\" This long quote shows "
                   "that Douglass clearly feels excluded from the celebration on this day.  "
                   "(B) To measure the gap he means, Douglass borrows the audience's own pride, calling their "
                   "\"high independence\" the very thing that \"reveals the immeasurable distance between us,\" "
                   "so their celebration becomes the measure of his exclusion.  "
                   "(C) Douglass talks about independence and distance and celebration in this part of the "
                   "speech, and he clearly wants the audience to understand that he feels a great deal of "
                   "separation from all of them on this particular day.  "
                   "(D) Douglass says the audience's \"high independence\" \"reveals the immeasurable distance "
                   "between us,\" and that phrase stands out in the passage. "
                   "Correct: B. It trims and frames. A dumps a long quote and adds a flat label; C quotes no "
                   "phrase at all; D trims to the phrase but drops it in bare, with no set-up and no "
                   "interpretation, so it still floats."),
             choices=[
                 {"id": "A", "text": ("Douglass says, \"I am not included within the pale of this glorious "
                                      "anniversary. Your high independence only reveals the immeasurable distance "
                                      "between us.\" This long quote shows that Douglass clearly feels excluded "
                                      "from the celebration on this day."),
                  "correct": False,
                  "why": ("Dumped. It quotes two full sentences and adds a flat label, so nothing is trimmed and "
                          "the quote is not framed.")},
                 {"id": "B", "text": ("To measure the gap he means, Douglass borrows the audience's own pride, "
                                      "calling their \"high independence\" the very thing that \"reveals the "
                                      "immeasurable distance between us,\" so their celebration becomes the "
                                      "measure of his exclusion."),
                  "correct": True,
                  "why": ("Correct. It trims to the load-bearing phrases, sets them up (\"To measure the gap he "
                          "means\"), and interprets them after (\"so their celebration becomes the measure of "
                          "his exclusion\"). Trimmed and framed.")},
                 {"id": "C", "text": ("Douglass talks about independence and distance and celebration in this "
                                      "part of the speech, and he clearly wants the audience to understand that "
                                      "he feels a great deal of separation from all of them on this particular "
                                      "day."),
                  "correct": False,
                  "why": ("It paraphrases everything and quotes no phrase at all, so there is no trimmed proof to "
                          "frame. Framing needs an actual quoted phrase to set up and interpret.")},
                 {"id": "D", "text": ("Douglass says the audience's \"high independence\" \"reveals the "
                                      "immeasurable distance between us,\" and that phrase stands out in the "
                                      "passage."),
                  "correct": False,
                  "why": ("Trimmed but not framed. It quotes the load-bearing phrase, so the trim is right, but it "
                          "drops the phrase in bare: no lead-in that says what to notice and no follow that says "
                          "what it does. A trimmed quote that is not set up and interpreted still floats.")},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this quote handling most need?",
             bank="douglass_1852",
             body=("Diagnose before the reveal. A student wrote: 'Douglass writes: \"Are the great principles of "
                   "political freedom and of natural justice, embodied in that Declaration of Independence, "
                   "extended to us?\" This is a good question.' Which single move would most improve it? "
                   "(A) trim to the load-bearing phrase and frame it, setting up what to notice before it and "
                   "interpreting what it does after it, instead of quoting the whole sentence and calling it 'a "
                   "good question'  "
                   "(B) quote the sentence that comes right after this one as well, adding more of Douglass's own "
                   "words so that the reader is given the full surrounding context of the whole passage before "
                   "any comment at all is offered on it  "
                   "(C) delete the quotation marks from around the borrowed line so that it blends smoothly into "
                   "your own sentence, since the punctuation is really what makes this handling feel clunky to "
                   "the reader  "
                   "(D) add a sentence stating that this is a powerful and important question, so that the "
                   "reader clearly understands the quoted line matters a great deal here in the argument"),
             feedback=("Correct: A. The full-sentence quote with 'a good question' after it is over-quoted and "
                       "unframed. The fix trims to the load-bearing phrase (say, 'extended to us?') and frames "
                       "it: set up that Douglass turns the audience's revered Declaration into a test, then "
                       "interpret the effect. Adding a second quote (B), dropping the marks (C), or a vague "
                       "'important' label (D) neither trim nor frame.")),
        Slot("SUPPORTED", "production_frq", "Warm up: trim and frame one quote",
             ref="", bank="douglass_1852", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="Warm up with a single framed sentence. Here is the shape to fill in:",
                 setapart_block=setapart("Fill-in frame:",
                                         "[set up what to notice], \"[a short quoted phrase]\", [interpret what it does]."),
                 closer="Write ONE sentence that uses a TRIMMED Douglass quote, framed before and after. Quote "
                        "only the load-bearing phrase, not a long passage. Then run the 3-question check on it.")),
        # COUNCIL FIX (2026-07-24): Option A (later-in-arc), watch-then-do: demo preserved, produce is the graded
        # act. The old diagnosis_frq bundled a watched 3-question check demo (pre-answered (q,a) tuple rows) + a
        # fresh sentence + a run-and-name tail in one box (unscoreable, wired to no grader, the (q,a) rows leaked
        # the answers). The coping-model demo is PRESERVED as read-only narration (the three checks shown running
        # on the weak draft, in plain declarative prose). The student's ONLY graded act is now the fresh
        # trimmed-and-framed sentence; the three checks sit read-only beneath as plain-string reminders; the
        # run-and-name tail is deleted. Kept at the sentence grain of its own fresh write (a diagnosis_frq is
        # present, which model_sequence needs at this lesson's paragraph grain). Stays on the taught source.
        Slot("MODEL", "diagnosis_frq", "Write a strong trimmed-and-framed quote sentence",
             ref="", bank="douglass_1852", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="First, watch the 3-question check run on the weak draft below. It is not trimmed to a "
                       "load-bearing phrase: there is no real quote, so nothing is pulled out. It is not set up: "
                       "there is no lead-in saying what to notice. And it is not interpreted: 'very meaningful' is "
                       "a flat label rather than a statement of what the phrase actually does. A stronger version "
                       "would quote one short phrase, set it up, and interpret it. Now write a fresh sentence of "
                       "your own that does not fall short that way.",
                 setapart_block=setapart("Weak draft the check was run on:",
                                         "Douglass says a lot about freedom in this long passage, which is very meaningful.", "red"),
                 checklist_block=checklist(title="Check your sentence against these (no need to type answers):", rows=[
                     "Trimmed to a load-bearing phrase?",
                     "Set up before the quote?",
                     "Interpreted after the quote?",
                 ]),
                 closer="Write ONE fresh trimmed-and-framed sentence of your own on the Douglass excerpt: quote a "
                        "short load-bearing phrase, set it up, and interpret what it does. Run the three checks "
                        "above before you submit.")),
        Slot("INDEPENDENT", "production_frq", "Trim and frame quotes in a full paragraph",
             ref="", bank="douglass_1852", rubric_ref="rc.4trait", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now. Write a short analytical paragraph about the Douglass excerpt that uses "
                       "one or two TRIMMED quotes, each framed (set up and interpreted), to support one "
                       "analytical point.",
                 closer="Trimming and framing every quote is what every real piece of rhetorical analysis is "
                        "built on, and you are ready to do it cold. Run the 3-question check on each quote before "
                        "you submit, and fix any that are dumped or floating.")),
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: Emerson, \"Self-Reliance\" (1841, excerpt)",
             ref="ACC-W910-RA-SINGLE-0003", bank="ra_essay_1",
             body=("A new source. Read this excerpt from Emerson's \"Self-Reliance.\" Find short phrases you could "
                   "quote as proof, and think about how to trim and frame them. The text stays on screen while "
                   "you work.")),
        Slot("TRANSFER", "production_frq", "Trim and frame quotes on a NEW text",
             ref="", bank="ra_essay_1", rubric_ref="rc.4trait", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="New text. Write a short analytical paragraph about the Emerson excerpt that uses one or "
                       "two TRIMMED quotes, each framed, to support one analytical point.",
                 closer="Same trim-and-frame move as the Douglass paragraph, new text. Do not dump long quotes. "
                        "Run the 3-question check on each quote before you submit.")),
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
