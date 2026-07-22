"""
lesson_g10_l07_significance.py  -  G10 KC C.10.02, ARCHETYPE T4: TEXT-DEPENDENT ANALYSIS (DEW, paragraph). V3.1.

V3.1 rebuild of the prior lesson_g10_l07_significance.py to the v3.1 spec (icm/_config/v3_1-lesson-build-spec.md),
adapting the pattern proven on G9 L06/L08 v3.1. PRESERVED: teaching point (after naming a device and its effect,
reach the WARRANT, why that effect matters to the author's purpose, the D-E-W top-band lift), id
ACC-W910-L-G10-C1002-0007, lesson_type 4, kc C.10.02, mnemonic_status proposal, unit, and the bound
fact-sourced -LESSON- stimuli (HIGHWAYS taught, WETLANDS transfer, partitioned). Changes vs the prior L07:
  1. ONE IDEA, hammered (KH load): a teal ONE_IDEA callout states the single core idea (reach WHY the effect
     matters, not just WHAT it does), then the minimum teaching as a LIST (effect-only vs warrant-reached)
     instead of the old ~140-word prose block that tripped format_fidelity.
  2. COPING-MODEL THINK-ALOUD (SRSD): the model is rewritten as a written drafting process (draft an effect
     statement -> run the check -> catch that it stops at the effect -> reach the warrant), First try / Second
     try / Final, with a literal BEFORE and AFTER (content_depth). No named person (Timeback stateless rule).
  3. THE CHECK TOOL AT POINT OF FIRST USE: the reusable Device-Effect-Warrant check is a REMEMBER dashed box
     with a real <ol> 3-question checklist, folded into the model card, not left cold in the teach step.
  4. FIXED THE TOKEN CONFOUND (DI, faultless communication): the discrimination now carries a DISTRACTOR that
     uses the word "because" to explain why the opening FEELS familiar (restating the effect), while the CORRECT
     option uses "because" to reach the author's PURPOSE, so reaching-significance (not the word "because") is
     the only invariant. Removed the leaked "Grade-C design bet" label from the student-facing text.
  5. DETERMINISTIC FRQ/DIAGNOSIS BODIES: production + diagnosis prompts are built with frq_prompt/setapart/
     checklist (no hand-written "Step 1/2" prose that double-numbers), and carry NO "Scored on ..." chrome.
  6. AUTONOMY + SAY-THE-STANDARD (Yeager): the independent write drops the frame, lets the student pick any
     authorial choice, and names the standard out loud ("reaching the significance is what every real analysis
     is built on; you are ready to do it cold").

ONE IDEA: after the effect, reach the WARRANT, why that effect matters to the author's purpose. ONE REMINDER:
the Device-Effect-Warrant check. "warrant" is a gated tech term (defined in TEACH). Passes all 23
lesson_contract gates. Own words, federal-sourced facts, no em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">After you name a device and its effect, take one more '
'step: reach the <strong>warrant</strong>, why that effect matters to the author\'s purpose. Naming the effect '
'is the middle band. Reaching why it matters is the lift into the top band.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: Device to Effect to Warrant</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you commit to an analysis sentence, run these three:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">DEVICE: what choice did the author make?</li>'
'<li style="margin:2px 0">EFFECT: what does that choice do for the reader?</li>'
'<li style="margin:2px 0">WARRANT: why does that effect matter to the author\'s purpose?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If you can answer 1 and 2 but not 3, you have '
'stopped at the effect. Reach the warrant before you commit.</div></div>')

# coping-model think-aloud panel: a WRITTEN drafting process (draft the effect -> run the check -> catch that
# it stops at the effect -> reach the warrant), then the BEFORE/AFTER endpoints (content_depth requires both
# literal words). No named person (Timeback stateless rule).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer analyzing one choice in the highways article: the author opens with an everyday stretch of road '
    'readers pass without thinking about it.</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "The author opens with something readers pass '
    'without ever thinking about it, which makes the interstate feel familiar." Run the check: DEVICE named '
    '(the ordinary opening), EFFECT named (feels familiar). WARRANT reached? No, it never says why that '
    'feeling matters to the author. It stops at the effect.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "...which makes the interstate feel familiar, and '
    'that is an interesting way to start." Run the check again: "interesting" is just praise, not a purpose. '
    'Still no warrant. Ask instead: what is the author trying to do?</p>'
    '<p style="margin:0"><strong>Final:</strong> "...which makes the interstate feel familiar, and that '
    'matters because the author wants a system readers overlook to suddenly seem worth understanding, so the '
    'ordinary opening sets up the surprise of its true scale." Now the check clears all three: device, effect, '
    'and the warrant that reaches the author\'s purpose.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "The author opens with something readers pass without ever '
    'thinking about it, which makes the interstate feel familiar." (stops at the effect)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "...which makes the interstate feel familiar, and that '
    'matters because the author wants a system readers overlook to suddenly seem worth understanding, so the '
    'ordinary opening sets up the surprise of its true scale." (reaches the warrant)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1002-0007", grade="9-10", lesson_type=4,
    unit="G10 U2 - Text-dependent analysis (warrant the significance)",
    title="Reach the Significance: Why the Effect Matters",
    target=("After naming a device and its effect, reach the warrant: explain WHY that effect matters to the "
            "author's purpose. This is the lift into the top band. Written at the sentence, building to the "
            "paragraph. Trait: Evidence/Development (analysis)."),
    acc_tags=["ACC.W.INFO.6", "ACC.W.SRC.3", "CCSS.W.9-10.9", "CCSS.RI.9-10.6"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.02",
                "sot": "icm course-G10.md L07; v3.1 spec icm/_config/v3_1-lesson-build-spec.md",
                "taught_stimulus": "ACC-W910-INFO-LESSON-HIGHWAYS",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-WETLANDS",
                "one_idea": "After the effect, reach the WARRANT: why that effect matters to the author's purpose.",
                "one_reminder": "Device-Effect-Warrant check: what device? what effect? why does it matter to the purpose?",
                "playbook": "_phase2/playbook_T4_DEW.md",
                "template": "locked L01 template; ANALYSIS-TIER binds full sources.",
                "version_note": ("V3.1: rebuilt to the v3.1 spec on the G9 L06/L08 v3.1 pattern - ONE_IDEA "
                                 "callout + list teach (fixed the wall-of-text that tripped format_fidelity), "
                                 "coping-model drafting think-aloud (SRSD, no named person), Device-Effect-"
                                 "Warrant check tool as a REMEMBER box at point of first use, fixed the "
                                 "'because' token confound in the discrimination + removed the leaked 'Grade-C' "
                                 "label (DI faultless communication), deterministic frq_prompt/setapart/"
                                 "checklist bodies (no 'Step N' double-number, no 'Scored on' chrome), autonomy "
                                 "+ say-the-standard on the independent write. Preserved teaching point, id, "
                                 "type, kc, mnemonic_status, and the bound HIGHWAYS/WETLANDS lesson stimuli."),
                "council": ("T4/DEW significance rung: rS1 warrant-the-significance (why the effect serves the "
                            "author's purpose), the D-E-W top-band lift. warrant defined in TEACH. "
                            "significance-reached-vs-effect-only discrimination labeled Grade-C in code only. "
                            "DEW=proposal.")},
    fade_ledger_moves=["warrant-the-significance", "device-effect-warrant"],
    slots=[
        # ===== TEACH: ONE idea only (list, not a wall of prose; warrant defined here for define_before_use) =====
        Slot("TEACH", "teach_card", "Go past the effect to why it matters",
             body=(ONE_IDEA +
                   "You can already name a device and say what it does. A warrant is a sentence that explains "
                   "WHY the effect matters to the author's purpose, how you know the choice is doing real work. "
                   "Think of it as three beats, Device to Effect to Warrant. Keep two kinds of analysis apart:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Effect only</strong>: names the choice and says what it "
                   "does. 'The author opens with something familiar, which makes the highway feel ordinary.' "
                   "True, but it stalls in the middle band.</li>"
                   "<li style=\"margin:4px 0\"><strong>Warrant reached</strong>: adds why that effect serves "
                   "the purpose. 'and that matters because the author wants an overlooked system to suddenly "
                   "seem worth understanding.' That reach is the lift to the top band.</li></ul>"
                   "Most analysis stops at the effect. Today: after the effect, reach the warrant, why the "
                   "effect serves the author's purpose.")),
        Slot("TEACH", "stimulus_display", "Read the source: Building the Interstate Highway System",
             ref="ACC-W910-INFO-LESSON-HIGHWAYS", bank="interstate_highways",
             body=("Read this explanatory article. Pick one authorial choice, how it opens, the order of its "
                   "sections, an organizing question, and be ready to name its effect AND reach why that effect "
                   "matters to what the author is trying to do. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model drafting think-aloud + the Device-Effect-Warrant check ====
        Slot("MODEL", "annotated_before_after", "Watch an effect statement reach its warrant",
             bank="interstate_highways",
             body=("Here is the skill in action. Follow the writer's thinking as an effect-only statement gets "
                   "checked, caught, and lifted until it reaches the warrant. " + COPING_HTML +
                   " Notice the two moves that turned the BEFORE into the AFTER: the writer ran the check and "
                   "caught that it stopped at the effect, then reached the WARRANT by asking what the author was "
                   "trying to do. " + REMEMBER +
                   "When you write your own analysis, do the same: name the device, state the effect, then reach "
                   "why that effect matters to the author's purpose before you commit.")),
        Slot("MODEL", "discrimination", "Which one reaches the significance?",
             ref="", labeled_grade_c=True, bank="interstate_highways",
             body=("Now that you have seen one built, spot the target. All three name the same device (the "
                   "ordinary opening) and the same effect (the interstate feels familiar). Which one reaches "
                   "the WARRANT, why that familiar feeling matters to what the author is trying to do? "
                   "(A) According to the article, the author opens with an everyday stretch of road that readers pass without a second thought, which makes the interstate feel familiar and ordinary, like plain background scenery a reader already knows well and barely notices.  "
                   "(B) According to the article, the author opens with an everyday stretch of road, which makes the interstate feel familiar because it is something readers see on nearly every drive and already recognize on sight.  "
                   "(C) According to the article, the author opens with an everyday stretch of road, which makes the interstate feel familiar, and that matters because the author wants an overlooked system to suddenly seem worth a careful look.  "
                   "(D) According to the article, the author opens with an everyday stretch of road, which makes the interstate feel familiar, and that matters because highways are one of the most important parts of the country's economy. "
                   "Correct: C. Its 'because' reaches the author's purpose (making an overlooked system seem "
                   "worth attention), which is the warrant. (A) adds more detail about the effect but stops "
                   "there; (B) uses 'because' only to explain why the road FEELS familiar, still restating the "
                   "effect, not the purpose; (D) reaches for why the topic matters in the real world, not why the "
                   "author's choice matters to the author's purpose."),
             choices=[
                 {"id": "A", "text": "According to the article, the author opens with an everyday stretch of road that readers pass without a second thought, which makes the interstate feel familiar and ordinary, like plain background scenery a reader already knows well and barely notices.",
                  "correct": False,
                  "why": "This describes the opening and its effect in fuller detail, but it never says WHY that familiar feeling matters to what the author is doing. More detail about the effect is still the effect."},
                 {"id": "B", "text": "According to the article, the author opens with an everyday stretch of road, which makes the interstate feel familiar because it is something readers see on nearly every drive and already recognize on sight.",
                  "correct": False,
                  "why": "This has the word 'because', but it only explains why the road feels familiar (readers see it often). That restates the effect. It does not reach the author's purpose."},
                 {"id": "C", "text": "According to the article, the author opens with an everyday stretch of road, which makes the interstate feel familiar, and that matters because the author wants an overlooked system to suddenly seem worth a careful look.",
                  "correct": True,
                  "why": "Correct. Its 'because' reaches WHY the effect matters to the author's purpose, to make an overlooked system seem worth attention. That is the warrant, the lift into the top band."},
                 {"id": "D", "text": "According to the article, the author opens with an everyday stretch of road, which makes the interstate feel familiar, and that matters because highways are one of the most important parts of the country's economy.",
                  "correct": False,
                  "why": "This reaches for significance, but it warrants why the topic matters in the real world, not why the author's choice serves the author's purpose. The warrant has to point back to what the author is doing, not to how important highways are."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this effect statement most need?",
             bank="interstate_highways",
             body=("Diagnose this draft before the reveal. A writer wrote: 'The author uses questions like who "
                   "would pay for it, which makes the article easy to follow.' Which single move would most "
                   "improve it? "
                   "(A) reach the warrant, why that easy-to-follow effect matters to the author's purpose  "
                   "(B) point out another organizing question the author asks somewhere else in the article  "
                   "(C) add a line saying the article is interesting and fun to read from start to finish  "
                   "(D) add a fact about how much the interstate highway system cost the government to build"),
             feedback=("Correct: A. The statement names a device (organizing questions) and an effect (easy to "
                       "follow) but stops there, in the middle band. The warrant reaches why: 'and that matters "
                       "because it walks a reader through a huge, complex system one plain question at a time, "
                       "making the scale feel manageable.' Another question (B), a vague 'interesting' (C), or "
                       "an extra fact (D) never reach the significance.")),

        # ===== SUPPORTED: framed write (fill-in frame) on the taught source (already read at STEP 2) =====
        Slot("SUPPORTED", "production_frq", "Add the warrant to a device-to-effect statement",
             ref="", bank="interstate_highways", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="Start from this device and effect: the author opens with something readers overlook, "
                       "which makes the interstate feel familiar. Use the frame so you can focus on the warrant.",
                 setapart_block=setapart("Copy this frame, then finish it:",
                                         "The author opens with something readers overlook, which makes the interstate feel familiar, and that matters because ______ [why that effect serves the author's purpose]."),
                 closer="Reach the warrant: say WHY the familiar feeling matters to what the author is trying to "
                        "do, do not just restate the effect. Write one sentence. Run the Device-Effect-Warrant "
                        "check before you submit.")),
        # DIAGNOSIS = check-and-fix on a PROVIDED weak draft (not a fresh production, so it does not repeat the
        # supported write). Stays on the taught source = no new reading (load). Uses checklist() so the check
        # renders as one clean numbered list (no 'Step N' double-numbering).
        Slot("MODEL", "diagnosis_frq", "Check your analysis: effect only, or warrant reached?",
             ref="", bank="interstate_highways", scored=True,
             body=frq_prompt(
                 intro="Run the Device-Effect-Warrant check on this weak draft, then rewrite it into a sentence "
                       "that reaches the warrant.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "The author ends by saying the interstate is easy to overlook because it works so well, which is a nice closing line.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("DEVICE named?", "Yes, the closing turn (calling the interstate easy to overlook)."),
                     ("EFFECT named?", "Loosely, 'a nice closing line' gestures at an effect but does not really name one."),
                     ("WARRANT reached?", "No. 'A nice line' says nothing about the author's purpose. Reach why the closing matters."),
                 ]),
                 closer="Now rewrite the weak draft into one sentence that names the device, states its effect, "
                        "and reaches the warrant (why the effect serves the author's purpose). Then name the "
                        "significance you reached.")),

        # ===== INDEPENDENT: cold write, no frame, free choice of device + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write a device-effect-warrant passage on your own",
             ref="", bank="interstate_highways", rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now, no frame. Choose any one authorial choice in the highways article, how "
                       "it opens, the order of its sections, an organizing question it asks.",
                 closer="Write a short analytical passage that runs the full move: name the DEVICE, state its "
                        "EFFECT, and reach the WARRANT (why that effect matters to the author's purpose). "
                        "Reaching the significance, not stopping at the effect, is what every real analysis is "
                        "built on, and you are ready to do it cold. Run the Device-Effect-Warrant check before "
                        "you submit.")),

        # ===== TRANSFER: same move, a NEW source (wetlands), bank-partitioned from the taught source =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: what wetlands do",
             ref="ACC-W910-INFO-LESSON-WETLANDS", bank="wetlands",
             body=("Read this new explanatory source on wetlands. Its author's choices are about structure and "
                   "wording, an opening that calls a swamp 'wasted ground,' the order of the explanation, the "
                   "comparisons it draws. Read it once, then find one choice and be ready to reach why its "
                   "effect matters to the author's purpose. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Write a device-effect-warrant passage on a NEW text",
             ref="", bank="wetlands", rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="New text, same move. Pick one choice the wetlands author makes, for example opening with "
                       "the old 'wasted ground' view of a swamp.",
                 closer="Write a short analytical passage that names the DEVICE, states its EFFECT, and reaches "
                        "the WARRANT (why it matters to the author's purpose, for example opening with the old "
                        "'wasted ground' view so the reader feels the correction that follows). Same "
                        "Device-Effect-Warrant move as the highways passage, new text. Run the check before you "
                        "submit.")),
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
