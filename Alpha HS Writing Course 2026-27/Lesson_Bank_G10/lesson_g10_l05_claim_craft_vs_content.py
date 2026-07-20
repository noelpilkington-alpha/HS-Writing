"""
lesson_g10_l05_claim_craft_vs_content.py  -  G10 KC C.10.02, ARCHETYPE T4: TEXT-DEPENDENT ANALYSIS (DEW, paragraph).

V3.1 rebuild of the pre-v3.1 L05 to the v3.1 spec (icm/_config/v3_1-lesson-build-spec.md), adapting the pattern
proven on the G9 v3.1 lessons. PRESERVED: teaching point (on close calls, tell a claim about the author's CRAFT
from a content claim dressed up with 'the author shows'), id ACC-W910-L-G10-C1002-0005, lesson_type=4, kc
C.10.02, mnemonic_status=proposal, unit, and the bound -LESSON- stimuli (story_of_an_hour taught, recycling
transfer). Changes vs the prior L05:
  1. ONE IDEA, hammered (KH load): a teal ONE_IDEA callout states the single core idea (a craft claim names
     what the AUTHOR does and its effect; a content claim only names the feeling), then the minimum teaching as
     a LIST (craft claim vs content claim, both defined in plain words) instead of the old 150+ word prose block
     that tripped format_fidelity.
  2. COPING-MODEL THINK-ALOUD (SRSD): the model is rewritten as a written drafting process (First try -> run the
     check -> catch the dressed-up content -> Second try -> Final craft claim), not a clean finished panel. Still
     contains literal BEFORE and AFTER (content_depth). The reusable craft-test tool is attached at the point of
     first use (the model card), not cold in the teach slot.
  3. FIXED THE KEYWORD CONFOUND (DI, faultless communication): the discrimination now uses explicit choices,
     every option leads with an author verb (so the author-verb is not the tell), and a DISTRACTOR quotes the
     text word 'free' while the CORRECT option is judged on technique+effect, so quoting a source word (not
     reasoning) can no longer pick the answer. Removed the leaked 'Grade-C design bet' label from the student
     text; labeled_grade_c=True stays in code only.
  4. DETERMINISTIC FRQ/DIAGNOSIS BODIES: supported + diagnosis prompts are built with frq_prompt/setapart/
     checklist (no hand-written 'Step 1/2' prose that double-numbers), and carry NO 'Scored on ...' chrome.
  5. AUTONOMY + SAY-THE-STANDARD (Yeager): the independent write puts the same move on a DIFFERENT technique in
     the same source so the supported sentence cannot be reused, lets the student choose the technique, and names
     the standard out loud.

ONE IDEA: a craft claim names what the AUTHOR does and its effect; a content claim only names the feeling.
ONE REMINDER: the craft test. Passes all 23 lesson_contract gates. Own words, source-faithful, no em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A craft claim names <strong>what the author DOES</strong> '
'and its effect on the reader. A content claim only names <strong>what the character feels</strong>. Putting '
'"Chopin shows" in front of a feeling does not turn content into craft.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the craft test</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you commit to any claim, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does it name a TECHNIQUE, something the author DID (a placement, a repeated word, an image, the point of view)?</li>'
'<li style="margin:2px 0">Does it name the EFFECT that choice has on the reader?</li>'
'<li style="margin:2px 0">Or does it only report what the character feels?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If it only reports a feeling, even with "Chopin shows" '
'in front, it is content, not craft. Fix it by naming the technique and its effect.</div></div>')

# coping-model think-aloud panel: a WRITTEN drafting process (draft -> run the check -> catch dressed-up content
# -> revise), then the BEFORE/AFTER endpoints (content_depth requires both literal words).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer building a claim about the moment Mrs. Mallard whispers the word "free":</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Chopin shows that Mrs. Mallard feels free after she '
    'hears the news." Run the craft test: does it name a technique Chopin uses? No, it only names the feeling. '
    'That is content wearing "Chopin shows." Try again.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "Chopin uses the word free to show she feels free." '
    'Run the test: it names a word now, but the effect is still just "she feels free," which is only the '
    'character. Closer, but still content.</p>'
    '<p style="margin:0"><strong>Final:</strong> "Chopin places the whispered word free right after the grief so '
    'the release seems to surface on its own before Mrs. Mallard can judge it." Run the test: it names a '
    'technique (placing free against the grief) AND an effect on the reader (the release seems to surface on its '
    'own). That is a craft claim.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "Chopin shows that Mrs. Mallard feels free after she hears the '
    'news." (only the feeling, with an author verb in front)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "Chopin places the whispered word free right after the grief so '
    'the release seems to surface on its own." (a technique plus its effect)</span></div>'
'</div>')

# discrimination options (reused in the body reveal AND the explicit choices=). Every option leads with an
# author verb so the verb is not the tell; option C quotes the source word 'free' but stays content, so
# quoting a text word cannot pick the answer. Correct (B) is not the lone longest.
DISC_A = ("Chopin shows that Mrs. Mallard is relieved and even joyful once she imagines the long free years now "
          "ahead of her.")
DISC_B = ("Chopin places the word 'free' right after the grief so the release seems to surface before she names "
          "it.")
DISC_C = ("Chopin makes it clear that the single word 'free' captures just how happy and relieved Mrs. Mallard "
          "feels inside.")
DISC_D = ("Chopin makes the reader feel a sudden rush of hope near the middle of the unfolding story.")

# SECOND discrimination options - a DIFFERENT confound than the first pair. The first pair's distractors name no
# technique at all (only a feeling). This pair's key distractor (D2_A) DOES name a real technique (the open-window
# image) but stops there with no reader effect (the 'half-craft, forgot the effect' trap the craft test warns
# about), while D2_C is pure feeling. Correct D2_B names the technique AND its effect. Fresh sentences on the open
# window (not the 'free'-placement sentences above). D2_C (a wrong option) is the longest, so the key is not the
# lone longest.
D2_A = ("Chopin uses the open-window image, picturing the treetops and the patches of blue sky outside Mrs. "
        "Mallard's room.")
D2_B = ("Chopin sets the open window in front of Mrs. Mallard so its view of new life turns the reader toward her "
        "coming rebirth before she admits it.")
D2_C = ("Chopin makes it clear that Mrs. Mallard feels lighter and far more hopeful than she has felt in years "
        "while she keeps gazing out at the bright open sky beyond her small, quiet room.")
D2_D = ("Chopin sets the open window before Mrs. Mallard so that she begins to feel her own freedom returning.")

LESSON = Lesson(
    id="ACC-W910-L-G10-C1002-0005", grade="9-10", lesson_type=4,
    unit="G10 U2 - Text-dependent analysis (craft vs content, close calls)",
    title="Tell a Craft Claim From a Content Claim",
    target=("On close calls, tell an analytical claim (about the author's technique and its effect) from a "
            "content claim dressed up with 'the author shows.' Written at the sentence. Trait: "
            "Evidence/Development (analysis)."),
    acc_tags=["ACC.W.INFO.6", "ACC.W.SRC.3", "CCSS.W.9-10.9", "CCSS.RI.9-10.6"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.02", "sot": "icm course-G10.md L05",
                "taught_stimulus": "ACC-W910-ANALYSIS-LESSON-HOUR",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-RECYCLING",
                "one_idea": "A craft claim names what the author DOES and its effect; a content claim only names the feeling.",
                "one_reminder": "craft test: does it name a technique? does it name the effect? or only the character's feeling?",
                "playbook": "_phase2/playbook_T4_DEW.md",
                "template": "locked L01 template; ANALYSIS-TIER binds full sources. DEW=proposal.",
                "version_note": ("V3.1: rebuilt to the v3.1 spec on the G9 v3.1 pattern - ONE_IDEA callout + "
                                 "list teach (fixed the prose-wall body), coping-model drafting think-aloud "
                                 "(First/Second/Final) with literal BEFORE/AFTER, craft-test tool at point of "
                                 "first use, explicit-choices discrimination with the keyword confound broken + "
                                 "the leaked 'Grade-C design bet' label removed (labeled_grade_c stays in code), "
                                 "deterministic frq_prompt/setapart/checklist bodies (no 'Step N' double-number, "
                                 "no 'Scored on' chrome), autonomy + say-the-standard on the independent write "
                                 "with a DIFFERENT technique on the same source so the supported sentence cannot "
                                 "be reused (Yeager). Preserved teaching point, id, KC, type, unit, and the bound "
                                 "story_of_an_hour / recycling lesson stimuli."),
                "council": ("T4/DEW guided rung: deepen the craft-vs-content boundary on close calls, the 'the "
                            "author shows X' trap that claims content while sounding analytical."),
                "review_provenance": ("23 lesson_contract gates (exit 0) + gated_reading render-QC clean; "
                                      "adapts the adjudicated G9 v3.1 Council+Fable findings.")},
    fade_ledger_moves=["craft-claim-vs-content-claim", "the-author-shows-trap"],
    slots=[
        # ===== TEACH: ONE idea only (list, not a wall of prose; craft-test tool held for point of first use) =====
        Slot("TEACH", "teach_card", "The author shows is not automatically analysis",
             body=(ONE_IDEA +
                   "A close-call trap in analysis is the sentence that sounds analytical but still reports "
                   "content. Keep two kinds of claim apart:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Craft claim</strong>: this is a claim that names something "
                   "the author DID (a word placement, a repeated word, an image, the point of view) and the "
                   "EFFECT that choice has on the reader.</li>"
                   "<li style=\"margin:4px 0\"><strong>Content claim</strong>: this is a claim that only reports "
                   "what a character feels or what happens, even when it opens with 'Chopin shows' or 'Chopin "
                   "reveals.'</li></ul>"
                   "The trap is starting with an author verb and then finishing with a feeling. That reads like "
                   "analysis but claims content. Today: on close calls, keep your claim on the author's "
                   "technique and its effect, not on the character's experience.")),
        Slot("TEACH", "stimulus_display", "Read the source: Kate Chopin, \"The Story of an Hour\" (1894)",
             ref="ACC-W910-ANALYSIS-LESSON-HOUR", bank="story_of_an_hour",
             body=("Read this short public-domain story with one question in mind: for any claim you might make, "
                   "is it about what Chopin DOES (a technique) or about what Mrs. Mallard feels (content)? Notice "
                   "the choices Chopin makes, the open-window imagery, the placement of the whispered word 'free' "
                   "against the earlier grief, the point of view that keeps us inside her head. Find one such "
                   "technique to claim about. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model drafting think-aloud + the craft-test tool =====
        Slot("MODEL", "annotated_before_after", "Watch a content claim become a craft claim",
             bank="story_of_an_hour",
             body=("Here is the skill in action. Follow the writer's thinking below as a dressed-up content claim "
                   "gets caught and rebuilt into a craft claim. " + COPING_HTML +
                   " Notice the two moves that turned the BEFORE into the AFTER: the writer named the TECHNIQUE "
                   "(the placement of 'free' against the grief), then named its EFFECT on the reader. " + REMEMBER +
                   "When you write your own claim, do the same: name the technique, name the effect, and run the "
                   "craft test before you commit to it.")),
        Slot("MODEL", "discrimination", "Which claim is about the craft?",
             ref="", labeled_grade_c=True, bank="story_of_an_hour",
             body=("Now that you have seen one built, spot the target. All three claims lead with an author verb. "
                   "Which one claims the CRAFT (a technique plus its effect), and which are dressed-up CONTENT? "
                   "(A) " + DISC_A + "  "
                   "(B) " + DISC_B + "  "
                   "(C) " + DISC_C + "  "
                   "(D) " + DISC_D + " "
                   "Correct: B. It names a technique (placing 'free' right after the grief) and its effect (the "
                   "release seems to surface before she names it). (A) and (C) only report what Mrs. Mallard "
                   "feels, just with an author verb in front, so they are content. (D) names an effect on the "
                   "reader but never names the technique that creates it, so it is only half a craft claim. "
                   "Quoting the word 'free,' as (C) does, does not make a claim about craft."),
             choices=[
                 {"id": "A", "text": DISC_A, "correct": False,
                  "why": "This leads with 'Chopin shows,' but it only reports what Mrs. Mallard feels (relieved, joyful). It names no technique and no effect on the reader, so it is dressed-up content."},
                 {"id": "B", "text": DISC_B, "correct": True,
                  "why": "Correct. It names a technique Chopin uses (placing 'free' right after the grief) and its effect (the release seems to surface before she names it). Naming the technique and its effect is the craft claim."},
                 {"id": "C", "text": DISC_C, "correct": False,
                  "why": "This quotes the word 'free' and sounds close, but it still only reports how happy Mrs. Mallard feels. Quoting a text word is not the same as naming a technique and its effect, so this is content."},
                 {"id": "D", "text": DISC_D, "correct": False,
                  "why": "This names an effect on the reader (a rush of hope), but it never names the technique Chopin uses to create it, so it is only half a craft claim. An effect with no technique is not yet analysis."},
             ]),
        # SECOND discrimination: a DIFFERENT confound. The first pair's wrong options name NO technique (only a
        # feeling). Here the key distractor (A) DOES name a real technique (the open-window image) but stops with
        # no reader effect - the 'half-craft, forgot the effect' trap. (C) is pure feeling and is the longest, so
        # the correct option (B) is not the lone longest.
        Slot("MODEL", "discrimination", "Which claim names a technique AND its effect?",
             ref="", labeled_grade_c=True, bank="story_of_an_hour",
             body=("Here is a second close call. All three claims point at the same open-window moment, but only "
                   "one names a technique AND says what it does to the reader. Which is the craft claim? "
                   "(A) " + D2_A + "  "
                   "(B) " + D2_B + "  "
                   "(C) " + D2_C + "  "
                   "(D) " + D2_D + " "
                   "Correct: B. It names a technique (setting the open window in front of Mrs. Mallard) and its "
                   "effect (the view of new life turns the reader toward her coming rebirth). (A) names the same "
                   "image but stops before any effect, so it is only half the claim. (C) only reports how Mrs. "
                   "Mallard feels, with an author verb in front, so it is content. (D) names the technique but "
                   "its 'so that' effect lands on the character, what Mrs. Mallard feels, not on the reader, so "
                   "it slides back into content."),
             choices=[
                 {"id": "A", "text": D2_A, "correct": False,
                  "why": "This names a real technique, the open-window image, but it never says what that choice does to the reader, so it is only half of a craft claim."},
                 {"id": "B", "text": D2_B, "correct": True,
                  "why": "Correct. It names a technique (setting the open window in front of Mrs. Mallard) and its effect on the reader (the view of new life turns the reader toward her coming rebirth), which is what makes a claim about craft."},
                 {"id": "C", "text": D2_C, "correct": False,
                  "why": "This only reports how Mrs. Mallard feels, hopeful and light, even with an author verb in front, so it names no technique and stays content."},
                 {"id": "D", "text": D2_D, "correct": False,
                  "why": "This names the technique, but its 'so that' effect is only what Mrs. Mallard feels, not an effect on the reader, so the claim slides back into content."},
             ]),
        Slot("MODEL", "predict_the_fix", "Why is this claim still content, not craft?",
             bank="story_of_an_hour",
             body=("Diagnose this draft before the reveal. A student wrote: 'Chopin reveals that Mrs. Mallard is "
                   "not as trapped as she used to feel.' Which single move would most improve it into a craft "
                   "claim? "
                   "(A) name the technique Chopin uses and the effect it has on the reader, instead of only what the character feels  "
                   "(B) add what Josephine and Richards do when they first hear the news, so the claim covers more of the characters  "
                   "(C) restate the same feeling more forcefully, adding words like 'truly' and 'deeply' so the point lands with more weight  "
                   "(D) add a later plot detail, such as how Mrs. Mallard reacts when her husband walks back in through the front door"),
             feedback=("Correct: A. 'Chopin reveals that Mrs. Mallard is not as trapped' still reports the "
                       "character's feeling, just with an author verb in front, so it is dressed-up content. The "
                       "fix names a technique and its effect, for example: 'Chopin keeps us inside Mrs. Mallard's "
                       "own thoughts so we hear her relief surface in her words before she can judge it.' More "
                       "characters (B), a stronger tone (C), or a plot detail (D) all keep the claim on content.")),

        # ===== SUPPORTED: framed write (fill-in frame) on a Chopin technique (source already read at TEACH) =====
        Slot("SUPPORTED", "production_frq", "Write a craft claim on a close call",
             ref="", bank="story_of_an_hour", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on keeping the claim on the author's craft, not on "
                       "the character's feeling.",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "Chopin ______ [a specific technique: a placement, a repeated word, an image, or the point of view] so ______ [its effect on the reader]."),
                 closer="Name the technique and its effect. Do not settle for 'Chopin shows' plus a feeling. "
                        "Write one sentence, then run the craft test before you submit.")),
        # DIAGNOSIS = check-and-fix on a PROVIDED weak draft (not a fresh production, so it does not repeat the
        # supported write). Stays on the taught source = no new reading (load). Uses checklist() so the check
        # renders as one clean numbered list (no 'Step N' double-numbering).
        Slot("MODEL", "diagnosis_frq", "Check your claim: technique, or feeling?",
             ref="", bank="story_of_an_hour", scored=True,
             body=frq_prompt(
                 intro="Run the craft test on this weak draft, then rewrite it into a claim about a Chopin "
                       "technique and its effect.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "Chopin shows that Mrs. Mallard feels trapped in her marriage.", "red"),
                 checklist_block=checklist(title="Run the test:", rows=[
                     ("Does it name a technique (something the author did)?", "No. It names only a feeling (trapped). Name the technique that creates it."),
                     ("Does it name an effect on the reader?", "No. Add what that choice makes the reader feel or notice."),
                     ("Or does it only report the character's feeling?", "Yes, right now it does. That is why it is content, not craft."),
                 ]),
                 closer="Now rewrite the weak draft into one sentence that names a Chopin technique and its "
                        "effect. Then name which question your rewrite fixed.")),

        # ===== INDEPENDENT: cold write, SAME source but a DIFFERENT technique (cannot reuse the supported
        #        sentence) + autonomy on the technique + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write a craft claim on your own",
             ref="", bank="story_of_an_hour", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="On your own now, no frame. Pick a Chopin technique you have not written about yet (the "
                       "open-window imagery, the irony of the calm before the whispered word, or the point of "
                       "view that keeps us inside her head).",
                 closer="Write ONE claim that names that technique and its effect on the reader. Check it "
                        "yourself: does it name what the AUTHOR does (not just what the character feels), and "
                        "does it name an effect? Do not settle for 'Chopin shows' plus a feeling. Keeping a claim "
                        "on the author's craft is what every real literary analysis is built on, and you are "
                        "ready to do it cold. Run the craft test before you submit.")),

        # ===== TRANSFER: same move, a NEW source (recycling), bank-partitioned from the taught source =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: how recycling works",
             ref="ACC-W910-INFO-LESSON-RECYCLING", bank="recycling",
             body=("Read this new explanatory source on recycling. Its author makes choices too, but about "
                   "STRUCTURE and wording: how it opens, the order it explains the chain, the comparisons it "
                   "uses. Read it once, then find one such choice to claim about, not just what recycling is. The "
                   "text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Write a craft claim on a NEW text",
             ref="", bank="recycling", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="New text, same move. Write ONE claim about a STRUCTURAL or wording choice the recycling "
                       "author makes, not about what recycling is.",
                 closer="Name the choice and its effect, for example: opening with a bottle in a bin that 'looks "
                        "like the end of a story' so the reader is set up to see recycling as a beginning instead. "
                        "Keep the claim on the author's craft. Run the craft test before you submit.")),
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
