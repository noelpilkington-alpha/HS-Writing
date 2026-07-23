"""
lesson_g11_l26_concision_pass.py  -  G11 KC C.11.04, ARCHETYPE T6: EDITING-IN-CONTEXT (SPOT, ceiling sentence).
V3.1 rebuild of the pre-v3.1 L26 to the v3.1 lesson build spec (icm/_config/v3_1-lesson-build-spec.md), the
pattern that cleared all 23 lesson_contract gates + the Fable-5 reviewer on G9 L01/L15 v3.1.

TEACHING POINT (KEEP): run a concision pass. Cut the words that do no work (empty intensifiers, redundant
pairs, throat-clearing openers) without losing meaning, rather than padding, editing the given sentence in
place. KC C.11.04. Bound stimuli unchanged: taught ACC-W910-INFO-LESSON-WATERUSE (bank water_infrastructure)
-> transfer ACC-W910-INFO-LESSON-ENERGYMIX (bank energy_transition), bank-partitioned.

V3.1 changes from the pre-v3.1 L26 (design pattern, not the teaching point):
  1. TEACH split to ONE idea in a callout + the three filler types as a real LIST (was a 150-word prose wall
     that tripped format_fidelity).
  2. MODEL rebuilt as a coping-model think-aloud (draft -> run the concision check -> catch the filler ->
     revise, First/Second/Final), still with a literal BEFORE and AFTER; the reusable 3-question check tool is
     folded in at point of first use.
  3. DISCRIMINATION uses explicit choices=[{id,text,correct,why}]; the leaked "Grade-C design bet" jargon is
     gone from the student prompt (labeled_grade_c stays True in code only). Confound broken: the correct
     option is neither the longest nor the shortest, so "shortest = concise" does not co-vary with the key.
  4. PREDICT-THE-FIX reveal lives in feedback= (not in an option label). FRQ + diagnosis bodies use
     frq_prompt/setapart/checklist (kills the "Step 1/Step 2" render double-numbering and the "Scored on"
     chrome). INDEPENDENT names the standard out loud (Yeager). TRANSFER stays a partitioned new topic.

id, lesson_type=6, kc="C.11.04", and mnemonic_status="proposal" are the current L26's values, unchanged; every
production_frq unit="sentence" (T6 ceiling). Own words, faithful to the bound USGS/EIA facts, no fabricated
figures, no em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A concision pass means going back over a sentence and '
'cutting the words that do no work, so every word left carries meaning. Cutting filler is not the same as '
'cutting content: you keep the claim and drop the padding.</div></div>')

# reusable job-aid, folded in at point of first use (the model card), not cold in step 1 (KH load).
REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Run this quick test on any sentence before you submit it:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Are there empty intensifiers (really, very, truly, actually, basically)?</li>'
'<li style="margin:2px 0">Is there a throat-clearing opener (In my opinion, It is important to understand that)?</li>'
'<li style="margin:2px 0">After cutting them, is the claim still there? If yes, the cut is safe.</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If a word can go without losing meaning, it does no work. Cut it.</div></div>')

# coping-model think-aloud: a WRITTEN editing process (draft -> run the check -> catch the filler -> revise),
# then the endpoints. Contains a literal BEFORE and AFTER (content_depth). No named person (Timeback rule).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer running a concision pass on one sentence, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "In my own personal opinion, I really do think that it '
    'is very important to basically understand that thermoelectric power plants use a truly large amount of water '
    'for cooling." Run the check: which words carry meaning? "Really," "very," "basically," and "truly" add no '
    'content. Cut the intensifiers first.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "It is important to understand that thermoelectric '
    'power plants use a large amount of water for cooling." Better, the intensifiers are gone. But "It is '
    'important to understand that" is a throat-clearing opener that delays the point. Cut it too.</p>'
    '<p style="margin:0"><strong>Final:</strong> "Thermoelectric power plants use a large amount of water for '
    'cooling." Every word left now carries meaning, and the claim is intact. That is a finished concision pass.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "In my own personal opinion, I really do think that it is very '
    'important to basically understand that thermoelectric power plants use a truly large amount of water for '
    'cooling." (stuffed with filler)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "Thermoelectric power plants use a large amount of water for '
    'cooling." (same claim, filler gone)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1107-0026", grade="9-10", lesson_type=6,
    unit="G11 U6 - Concision pass (cut words that do no work)",
    title="Cut the Words That Do No Work",
    target=("Run a concision pass on a sentence: cut empty intensifiers, redundant pairs, and throat-clearing "
            "openers without losing meaning, rather than padding, editing the given sentence in place. Written "
            "at the sentence. Trait: Language (concision)."),
    acc_tags=["ACC.W.LANG.2", "CCSS.W.11-12.4", "CCSS.L.11-12.3"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.11.04", "sot": "icm course-G11.md L26",
                "taught_stimulus": "ACC-W910-INFO-LESSON-WATERUSE",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-ENERGYMIX",
                "playbook": "_phase2/playbook_T6_SPOT.md",
                "template": "v3.1 lesson build spec; binds full info source (sentence material); editing-in-context.",
                "one_idea": "A concision pass cuts the words that do no work and keeps the claim.",
                "one_reminder": "3-question check: empty intensifiers? throat-clearing opener? claim still intact after cutting?",
                "version_note": ("V3.1 rebuild of the pre-v3.1 L26 to the v3.1 build spec: TEACH split into a "
                                 "one-idea callout + the three filler types as a list (fixes the format_fidelity "
                                 "wall of text); MODEL rebuilt as a coping-model think-aloud with the 3-question "
                                 "check folded in at point of first use; discrimination moved to explicit choices "
                                 "with the leaked Grade-C jargon removed and the length confound broken (correct "
                                 "option neither longest nor shortest); FRQ + diagnosis bodies use "
                                 "frq_prompt/setapart/checklist (kills the 'Step 1/2' render double-numbering and "
                                 "the 'Scored on' chrome); independent says the standard out loud (Yeager). "
                                 "Teaching point + bound stimuli unchanged."),
                "review_provenance": ("Rebuilt to icm/_config/v3_1-lesson-build-spec.md (the pattern that cleared "
                                      "all 23 lesson_contract gates + the Fable-5 reviewer on G9 v3.1)."),
                "council": ("T6/SPOT G11 concision-pass guided rung: R2 cut-words-that-do-no-work (intensifiers, "
                            "redundancy, throat-clearing) without losing meaning. concise-vs-padded discrimination "
                            "labeled Grade-C in code (not in student text). SPOT=proposal; ceiling sentence.")},
    fade_ledger_moves=["concision-pass", "cut-words-that-do-no-work"],
    slots=[
        # ===== TEACH: ONE idea in a callout + the three filler types as a real LIST (no wall of text) =====
        Slot("TEACH", "teach_card", "Cut what carries no meaning",
             body=(ONE_IDEA +
                   "Padded writing feels serious, but the extra words only slow the reader down. Three kinds of "
                   "filler are the usual targets, and each has a plain-words definition you can spot:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Empty intensifiers</strong> are words like 'really,' "
                   "'very,' 'truly,' 'actually,' and 'basically' that add emphasis but no content.</li>"
                   "<li style=\"margin:4px 0\"><strong>Redundant pairs</strong> say one thing twice, such as "
                   "'own personal,' 'end result,' or 'first and foremost.'</li>"
                   "<li style=\"margin:4px 0\"><strong>Throat-clearing openers</strong> delay the point, such as "
                   "'In my opinion, I think that' or 'It is important to understand that.'</li></ul>"
                   "The test for each word is simple: if cutting it loses no meaning, it does no work, so cut it. "
                   "This is an editing move on a sentence that already exists, so you find the filler and delete "
                   "it in place, keeping the words that carry the claim. The trap is padding to sound formal. "
                   "Goal today: tighten a sentence by cutting the words that do no work.")),
        Slot("TEACH", "stimulus_display", "Read the source: how America uses its water",
             ref="ACC-W910-INFO-LESSON-WATERUSE", bank="water_infrastructure",
             body=("The sentences you will tighten state facts from this source on U.S. water use, so you can cut "
                   "filler while keeping the real claim intact. Read it and note the largest uses. You are not "
                   "writing about water from scratch here; you are running a concision pass on a sentence that is "
                   "given to you, and the text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model think-aloud with the check tool folded in =====
        Slot("MODEL", "annotated_before_after", "Watch a padded sentence get tightened",
             bank="water_infrastructure",
             body=("Here is the skill in action. Follow the writer's concision pass below. " + COPING_HTML +
                   " Notice the moves that turned the BEFORE into the AFTER: cut the empty intensifiers, then cut "
                   "the throat-clearing opener, and check that the claim survived. " + REMEMBER +
                   "When you tighten your own sentence, do the same: spot the filler, cut it, and run the 3 "
                   "questions before you submit.")),
        Slot("MODEL", "discrimination", "Which version has had its filler cut?",
             ref="", labeled_grade_c=True, bank="water_infrastructure",
             body=("Now that you have seen one built, spot the target. All three versions try to state the same "
                   "fact from the source: thermoelectric power plants are the country's largest single use of "
                   "water. Which one has had its filler cut without losing that claim? "
                   "(A) In my own personal opinion, I really do think that thermoelectric power plants are very "
                   "truly the single biggest use of water in this entire country.  "
                   "(B) Power plants use a lot of water.  "
                   "(C) Thermoelectric power plants are the country's largest single use of water.  "
                   "(D) It is important to understand that thermoelectric power plants are the country's largest "
                   "single use of water. "
                   "Correct: C. It cuts the filler and keeps the claim."),
             choices=[
                 {"id": "A", "text": "In my own personal opinion, I really do think that thermoelectric power plants are very truly the single biggest use of water in this entire country.",
                  "correct": False,
                  "why": "This one is stuffed with a throat-clearing opener ('In my own personal opinion, I really do think that'), a redundant pair ('own personal'), and empty intensifiers ('very truly'). None of that does any work; it is padded, not concise."},
                 {"id": "B", "text": "Power plants use a lot of water.",
                  "correct": False,
                  "why": "This one is short, but a concision pass keeps the claim. It cut too far: the real point, that thermoelectric power plants are the LARGEST single water use in the country, is gone. Cutting content is not concision."},
                 {"id": "C", "text": "Thermoelectric power plants are the country's largest single use of water.",
                  "correct": True,
                  "why": "Correct. The filler is gone and the claim is intact: it still says thermoelectric power plants are the largest single water use, which matches the source (about 133 billion gallons a day, the biggest of the three main uses). That is what a concision pass does, cut the padding, keep the meaning."},
                 {"id": "D", "text": "It is important to understand that thermoelectric power plants are the country's largest single use of water.",
                  "correct": False,
                  "why": "This one keeps the claim but still opens with a throat-clearing phrase ('It is important to understand that'). A concision pass is only done when every filler word is gone, and this one left the opener in, so the pass is unfinished."},
             ]),
        # SECOND minimal pair, DIFFERENT confound: not "did you cut too far" (all three keep the claim here) but
        # "is there leftover filler". A short option (B) still leads with an intensifier; a long option (A) buries
        # the point behind a throat-clearing opener; so length alone does not tell you a sentence is clean. Correct
        # (C) is neither the longest (A is) nor meaningfully shorter than (B), so length is not a usable cue.
        Slot("MODEL", "discrimination", "Which version cut every filler word?",
             ref="", labeled_grade_c=True, bank="water_infrastructure",
             body=("One more, a subtler case. All three versions state the same fact, that just three activities "
                   "account for about 90 percent of the country's daily water use, and none of them lose that "
                   "claim. The trap now is leftover filler: which one has cut every filler word, not just some? "
                   "(A) It is important to understand that just three activities account for the vast majority, "
                   "roughly 90 percent, of the nation's daily water use.  "
                   "(B) Basically, three activities take about 90 percent of the nation's daily water use.  "
                   "(C) Three activities account for about 90 percent of the nation's daily water use.  "
                   "(D) First and foremost, three activities account for about 90 percent of the nation's daily "
                   "water use. "
                   "Correct: C. It is the only version with no filler left."),
             choices=[
                 {"id": "A", "text": "It is important to understand that just three activities account for the vast majority, roughly 90 percent, of the nation's daily water use.",
                  "correct": False,
                  "why": "It keeps the claim, but it still opens with a throat-clearing phrase ('It is important to understand that') and pads the number with extra words, so the filler was never cut."},
                 {"id": "B", "text": "Basically, three activities take about 90 percent of the nation's daily water use.",
                  "correct": False,
                  "why": "It is short, but it still leads with the empty intensifier 'Basically,' which does no work, so a short sentence is not automatically a clean one."},
                 {"id": "C", "text": "Three activities account for about 90 percent of the nation's daily water use.",
                  "correct": True,
                  "why": "Every filler word is gone and the claim survives: it still says three activities take about 90 percent of daily water use, which matches the source (around 90 percent from just three categories)."},
                 {"id": "D", "text": "First and foremost, three activities account for about 90 percent of the nation's daily water use.",
                  "correct": False,
                  "why": "It keeps the claim but opens with the redundant pair 'First and foremost,' which says one thing twice and does no work. One kind of filler left in means the concision pass is not finished."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this sentence most need?",
             bank="water_infrastructure",
             body=("Diagnose this draft before the reveal. A student wrote: 'It is basically very important for "
                   "people to really understand the actual fact that farms use a lot of water.' Which single move "
                   "would most improve it? "
                   "(A) Cut the filler ('basically,' 'very,' 'really,' 'the actual fact that') and keep the claim "
                   "that farms use a lot of water.  "
                   "(B) Add more emphasis words like 'extremely,' 'seriously,' and 'truly' so the point lands on "
                   "the reader with a great deal more force.  "
                   "(C) Make the sentence longer by adding more formal-sounding phrases so the writing reads as "
                   "more serious and more academic to a grader.  "
                   "(D) Replace the claim about farm water use with a different, more surprising fact from the "
                   "source that will grab the reader's attention right away."),
             feedback=("Correct: A. 'Basically,' 'very,' 'really,' and 'the actual fact that' are filler; the "
                       "claim is 'farms use a lot of water.' The fix cuts the filler and keeps the claim ('Farms "
                       "use a lot of water'). Adding emphasis words (B) or length (C) is more padding; changing "
                       "the fact (D) is not a concision pass at all.")),

        # ===== SUPPORTED: framed edit (fill-in frame) on the taught topic (source read at TEACH step 2) =====
        Slot("SUPPORTED", "production_frq", "Tighten this sentence",
             ref="", bank="water_infrastructure", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="revision",
             body=frq_prompt(
                 intro="Run a concision pass on this padded sentence, keeping the claim. Here is the sentence to "
                       "fix: 'In my own personal opinion, I really think it is very important to basically realize "
                       "that water is actually a truly limited resource.'",
                 setapart_block=setapart("Copy this frame, then fill in the blank:",
                                         "Water is ______ [the claim, with no filler words]."),
                 closer="Cut every empty intensifier, redundant pair, and throat-clearing opener, and keep the "
                        "claim that water is a limited resource. Then run the 3-question check before you submit.")),
        # DIAGNOSIS = run the check on a PROVIDED weak draft, then rewrite it (not a fresh production, so it does
        # not repeat the Independent write). Stays on the taught topic = no new source to read (load balance).
        Slot("MODEL", "diagnosis_frq", "Check and fix a weak draft with the 3 questions",
             ref="", bank="water_infrastructure", scored=True,
             body=frq_prompt(
                 intro="Run the 3-question check on this weak draft, then rewrite it so the filler is gone and the "
                       "claim is intact.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "It is really quite important to truly understand that U.S. water use is very high.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Are there empty intensifiers?", "Yes: 'really,' 'quite,' 'truly,' 'very.' Cut them."),
                     ("Is there a throat-clearing opener?", "Yes: the 'It is ... important to ... understand that' frame. Cut the whole opener."),
                     ("Is the claim still there after cutting?", "The claim to keep is that U.S. water use is high."),
                 ]),
                 closer="Now write out the tightened sentence yourself, keeping that claim and dropping every "
                        "flagged word. Then name one filler word you cut and say why it did no work.")),

        # ===== INDEPENDENT: cold write on the taught topic + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Run a concision pass on your own",
             ref="", bank="water_infrastructure", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now, no frame. Take one fact from the water-use source, write it first as a "
                       "padded sentence, then tighten it: cut the empty intensifiers, redundant pairs, and "
                       "throat-clearing openers, keeping the claim.",
                 closer="Before you submit, check that every remaining word carries meaning; if not, cut more. A "
                        "sentence where every word does work is what every clear piece of writing is built on, and "
                        "you are ready to do this cold. Run the 3-question check before you submit.")),

        # ===== TRANSFER: same move, a NEW topic (electricity mix), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: the U.S. electricity mix",
             ref="ACC-W910-INFO-LESSON-ENERGYMIX", bank="energy_transition",
             body=("The next sentence to fix draws on this new source about where U.S. electricity comes from and "
                   "how the mix is shifting. Read it and note one fact, such as a share of the mix. Again, you are "
                   "running a concision pass on a sentence, not writing from scratch, and the text stays on screen "
                   "while you work.")),
        Slot("TRANSFER", "production_frq", "Run a concision pass on a NEW source",
             ref="", bank="energy_transition", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="New source. Take one fact from the electricity-mix source, write it first as a padded "
                       "sentence, then run a concision pass to cut the words that do no work.",
                 closer="Same cut-the-filler move as the water sentence, new source: keep the claim, drop the "
                        "padding. Run the 3-question check before you submit.")),
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
