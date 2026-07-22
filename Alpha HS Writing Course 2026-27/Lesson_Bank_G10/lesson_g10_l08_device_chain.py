"""
lesson_g10_l08_device_chain.py  -  G10 KC C.10.02, ARCHETYPE T4: TEXT-DEPENDENT ANALYSIS (DEW, paragraph). V3.1.

V3.1 rebuild of the pre-v3.1 device-chain lesson to the v3.1 spec (icm/_config/v3_1-lesson-build-spec.md),
adapting the pattern proven on G9 L06/L08 v3.1. PRESERVED: teaching point (link two or more of the author's
choices that build ONE analytical point, rather than one observation and stop), id ACC-W910-L-G10-C1002-0008,
lesson_type=4, kc=C.10.02, mnemonic_status=proposal, unit="paragraph", and the bound lesson stimuli
(RECYCLING taught, WEATHER transfer). Changes vs the prior L08:
  1. ONE IDEA, hammered (KH load): a teal ONE_IDEA callout states the single core idea (a device-chain links
     several choices to build one point), then the minimum teaching as a LIST (chain vs single-shot) instead
     of the old ~150-word prose block that tripped format_fidelity.
  2. COPING-MODEL THINK-ALOUD (SRSD): the model is a WRITTEN drafting process (draft single-shot -> run the
     chain check -> catch the one-and-done -> revise into a chain), not a clean finished panel. Contains literal
     BEFORE and AFTER (content_depth). The reusable chain check is folded in at the point of first use.
  3. FIXED THE LENGTH/CONFOUND (DI, Haladyna): the discrimination uses explicit choices=[], all options
     attributed to "the author" and padded homogeneous so the correct one is NOT the lone longest, and a
     distractor also links two choices (so "two choices" no longer co-varies with correct; the invariant is
     whether they build the SAME point). Removed the leaked "Grade-C design bet" label from the student text.
  4. DETERMINISTIC FRQ/DIAGNOSIS BODIES: production + diagnosis built with frq_prompt/setapart/checklist (no
     hand-written "Step 1/2" prose that double-numbers), and carry no "Scored on ..." chrome.
  5. AUTONOMY + SAY-THE-STANDARD (Yeager): the independent write drops the frame, lets the student choose the
     choices, and names the standard out loud.

ONE IDEA: a device-chain links two or more of the author's choices that build ONE point. ONE REMINDER: the
chain check. Passes all 23 lesson_contract gates. Own words, federal-sourced facts, no em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A device-chain is when you link <strong>two or more '
'of the author\'s choices that build ONE point</strong>, instead of naming a single choice and stopping. One '
'sharp observation cannot carry a whole analytical paragraph; a chain can.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the chain check</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you commit to an analytical paragraph, run this:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">How many of the author\'s choices am I analyzing? (I need two or more.)</li>'
'<li style="margin:2px 0">Do those choices build the SAME one point?</li>'
'<li style="margin:2px 0">Have I named that one point out loud?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If you can only find one choice, or the choices pull '
'toward different ideas, it is not yet a chain. Find a second choice that builds the same point.</div></div>')

# coping-model think-aloud panel: a WRITTEN drafting process (draft single-shot -> run the check -> catch the
# one-and-done -> revise into a chain), then the BEFORE/AFTER endpoints (content_depth requires both words).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer building one analytical paragraph about the recycling text, choice by choice:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "The author calls a bottle in the bin the beginning '
    'of a story, which makes recycling sound like a journey." Run the chain check: how many of the author\'s '
    'choices did I analyze? Just one, the opening image. That is single-shot. One choice and stop.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> Look back at the text for a SECOND choice that '
    'builds the same point. The author then traces the bottle through "trucks, machines, and factories." Does '
    'that build the same idea as the opening image? Yes, both make recycling feel like something that keeps '
    'going, not a finished act.</p>'
    '<p style="margin:0"><strong>Final:</strong> Link the two choices and name the one point. "The author calls '
    'the bottle the beginning of a story, then traces it through trucks, machines, and factories, so recycling '
    'reads as an ongoing process rather than an endpoint." Two choices, one point, named.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "The author calls a bottle the beginning of a story, which '
    'makes recycling sound like a journey." (one choice, then stop)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "The author calls the bottle the beginning of a story, then '
    'traces it through trucks, machines, and factories, so recycling reads as an ongoing process rather than an '
    'endpoint." (two linked choices, one point)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1002-0008", grade="9-10", lesson_type=4,
    unit="G10 U2 - Text-dependent analysis (device-chain)",
    title="Link Several Choices to Build One Point",
    target=("Sustain an analysis across a paragraph with a device-chain: link two or more of the author's "
            "choices that build ONE analytical point, rather than making a single observation and stopping. "
            "Written at the paragraph. Trait: Evidence/Development (analysis)."),
    acc_tags=["ACC.W.INFO.6", "CCSS.W.9-10.9"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.02",
                "sot": "icm course-G10.md L08; v3.1 spec icm/_config/v3_1-lesson-build-spec.md",
                "taught_stimulus": "ACC-W910-INFO-LESSON-RECYCLING",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-WEATHER",
                "one_idea": "A device-chain links two or more of the author's choices that build ONE point.",
                "one_reminder": "chain check: how many choices? do they build one point? have I named that point?",
                "playbook": "_phase2/playbook_T4_DEW.md",
                "template": "locked L01 template; ANALYSIS-TIER binds full sources.",
                "version_note": ("V3.1: rebuilt to the v3.1 spec on the L06/L08 v3.1 pattern - ONE_IDEA callout "
                                 "+ list teach (fixed the wall-of-text), coping-model drafting think-aloud "
                                 "(SRSD), chain check tool folded in at point of first use, fixed the "
                                 "length/two-choice confound in the discrimination + removed the leaked "
                                 "'Grade-C' label (DI faultless communication), deterministic frq_prompt/"
                                 "setapart/checklist bodies (no 'Step N' double-number, no 'Scored on' chrome), "
                                 "autonomy + say-the-standard on the independent write. Preserved teaching "
                                 "point, id, lesson_type, kc, mnemonic_status, unit, and the bound "
                                 "RECYCLING/WEATHER lesson stimuli."),
                "council": ("T4/DEW device-chain rung: introduces linking multiple choices building one "
                            "analytical point. chain-vs-single-shot discrimination (labeled_grade_c in code). "
                            "DEW=proposal; unit=paragraph."),
                "review_provenance": ("23 lesson_contract gates (exit 0) + gated_reading render-QC clean; "
                                      "adapts the adjudicated L01 v3.1 Council+Fable findings.")},
    fade_ledger_moves=["device-chain", "several-choices-one-point"],
    slots=[
        # ===== TEACH: ONE idea only (list, not a wall of prose; chain check held for point of first use) =====
        Slot("TEACH", "teach_card", "One device is not a paragraph",
             body=(ONE_IDEA +
                   "A single observation, even a sharp one, reads thin across a whole paragraph. When you build "
                   "an analytical paragraph, keep two shapes apart:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Device-chain</strong>: you name one choice the author "
                   "makes, then a second choice, and show that BOTH build the same point. Choice one sets "
                   "something up; choice two extends it; together they create the effect you claim.</li>"
                   "<li style=\"margin:4px 0\"><strong>Single-shot</strong>: you name one choice and stop, or "
                   "you pile up choices that pull toward different ideas. Either way the point is not built "
                   "up.</li></ul>"
                   "The chained choices must build the SAME point, not just stack unrelated observations. The "
                   "trap is grabbing one good observation and calling it done. Today: link two or more of the "
                   "author's choices to build ONE point across a paragraph, and name that point.")),
        Slot("TEACH", "stimulus_display", "Read the source: how recycling works",
             ref="ACC-W910-INFO-LESSON-RECYCLING", bank="recycling",
             body=("Read this explanatory source on recycling. Because your job is to chain choices, read the "
                   "whole thing and notice the different choices the author makes: a framing image, an order of "
                   "steps, a comparison, a warning. Look for two or more that push toward the SAME point, and be "
                   "ready to link them. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model drafting think-aloud + the chain check tool =====
        Slot("MODEL", "annotated_before_after", "Watch single-shot analysis become a device-chain",
             bank="recycling",
             body=("Here is the skill in action. Follow the writer's thinking below as a one-and-done observation "
                   "gets caught and rebuilt into a chain. " + COPING_HTML +
                   " Notice the two moves that turned the BEFORE into the AFTER: the writer FOUND a second choice "
                   "in the text, then checked that both choices build the SAME point and NAMED it. " + REMEMBER +
                   "When you build your own paragraph, do the same: find a second choice, confirm both build one "
                   "point, and run the chain check before you commit.")),
        Slot("MODEL", "discrimination", "Which one is a device-chain?",
             ref="", labeled_grade_c=True, bank="recycling",
             body=("Now that you have seen one built, look at a DIFFERENT part of the same text, the section on "
                   "contamination, and spot the target. Which one CHAINS the author's choices toward a single "
                   "point, and which does not? "
                   "(A) The author names the household mistake with the recycling industry's own word, calling it 'contamination,' a precise and technical term that instantly makes the writing sound authoritative and gives the whole passage a serious, credible, expert tone.  "
                   "(B) The author lists the ordinary items that foul a load, a greasy box and a jar of food, then shows how the bags jam the machines and the food ruins the paper, so a small household slip reads as a real threat to the whole system.  "
                   "(C) The author warns that a dirty load can be sent to the landfill, and elsewhere notes that recycling supports jobs and wages across the country, two separate points that each tell the reader something different.  "
                   "(D) The author both calls the everyday mistake by the industry's own word, 'contamination,' and lists the greasy box and the jar of food that cause it, giving the reader two separate details about what can foul a load. "
                   "Correct: B. It links two choices, the list of items that foul a load and the account of how they jam the machines and ruin the paper, and both build the "
                   "SAME point: a small household slip threatens the whole load. (A) names one choice and only praises it, so it "
                   "is single-shot. (C) names two choices, but they pull toward different ideas and are not "
                   "linked to one point. (D) links two choices that do point the same way, but it never names the "
                   "single point they build, so the chain is left unfinished."),
             choices=[
                 {"id": "A", "text": "The author names the household mistake with the recycling industry's own word, calling it 'contamination,' a precise and technical term that instantly makes the writing sound authoritative and gives the whole passage a serious, credible, expert tone.",
                  "correct": False,
                  "why": "This names one choice, the industry term 'contamination,' and then only praises it. One choice and stop is single-shot; nothing is built across the paragraph."},
                 {"id": "B", "text": "The author lists the ordinary items that foul a load, a greasy box and a jar of food, then shows how the bags jam the machines and the food ruins the paper, so a small household slip reads as a real threat to the whole system.",
                  "correct": True,
                  "why": "Correct. Two of the author's choices, the list of items that foul a load and the account of how they jam the machines and ruin the paper, are linked, and both build the SAME point: a small household slip threatens the whole load. That is a chain."},
                 {"id": "C", "text": "The author warns that a dirty load can be sent to the landfill, and elsewhere notes that recycling supports jobs and wages across the country, two separate points that each tell the reader something different.",
                  "correct": False,
                  "why": "This names two choices, but they pull toward different ideas (the risk of a contaminated load and the economic benefits of recycling) and are not linked to one point. Stacking unrelated choices is not a chain."},
                 {"id": "D", "text": "The author both calls the everyday mistake by the industry's own word, 'contamination,' and lists the greasy box and the jar of food that cause it, giving the reader two separate details about what can foul a load.",
                  "correct": False,
                  "why": "This links two choices that do point the same way, but it stops before naming the single point they build. A chain is not finished until you say the one point out loud, so this is still incomplete."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this single-shot analysis most need?",
             bank="recycling",
             body=("Diagnose this draft before the reveal. A student wrote: 'The author compares recycling to a "
                   "story, which makes the process sound interesting.' Which single move would most improve it "
                   "into a device-chain? "
                   "(A) link a second choice from the text that builds the SAME point, so the analysis carries "
                   "across the paragraph  "
                   "(B) add a sentence defining what the word 'story' means before getting into the author's "
                   "actual choices in the text  "
                   "(C) bring in a separate choice from another part of the text, even though it points to a "
                   "completely different idea  "
                   "(D) restate the very same effect again in stronger, more forceful words so the single point "
                   "lands harder on the reader"),
             feedback=("Correct: A. One choice (the story comparison) cannot sustain a paragraph. The fix links a "
                       "second choice that builds the same point, for example, 'and by walking the bottle "
                       "through trucks and factories, the author makes that story feel like a real, ongoing "
                       "process.' A definition (B) adds no analysis; an unrelated choice (C) stacks rather than "
                       "chains; restating (D) does not extend the point.")),

        # ===== SUPPORTED: framed write (fill-in frame) on the taught source (already read at STEP 2) =====
        Slot("SUPPORTED", "production_frq", "Chain two choices toward one point",
             ref="", bank="recycling", rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on linking two of the recycling author's choices "
                       "toward ONE point.",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "The author ______ [choice 1], then ______ [choice 2] so ______ [the single point the two choices build]."),
                 closer="Pick two choices that push toward the SAME point, name each one, and name the point they "
                        "build together. Do not make one observation and stop. Then run the chain check before "
                        "you submit.")),
        # DIAGNOSIS = check-and-fix on a PROVIDED weak draft (not a fresh production, so it does not repeat the
        # supported write). Stays on the taught source = no new reading (load). Uses checklist() so the check
        # renders as one clean numbered list (no 'Step N' double-numbering).
        Slot("MODEL", "diagnosis_frq", "Check your analysis: chained, or single-shot?",
             ref="", bank="recycling", scored=True,
             body=frq_prompt(
                 intro="Run the chain check on this weak draft, then rewrite it into a passage that chains two of "
                       "the recycling author's choices toward one point.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "The author opens with a vivid image of a bottle dropping into the bin.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("How many of the author's choices does it analyze?", "Just one, the opening image. That is single-shot."),
                     ("Do the choices build one shared point?", "They cannot; there is only one. Add a second choice that builds the same point."),
                     ("Is that one point named?", "No. After you chain a second choice, name the single point the two build."),
                 ]),
                 closer="Now rewrite the weak draft into a passage that links two choices toward one point. Then "
                        "name which question your rewrite fixed.")),

        # ===== INDEPENDENT: cold write, no frame + autonomy on which choices + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write a device-chain paragraph on your own",
             ref="", bank="recycling", rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now, no frame. Write a short analytical paragraph that chains two or more of "
                       "the recycling author's choices toward ONE point.",
                 closer="You choose which choices to link. Name each choice and name the single point they build "
                        "together. Before you submit, check: are two or more choices analyzed, do they build the "
                        "SAME point, and is that point named? Linking the author's choices to build one point is "
                        "what every real analysis paragraph is built on, and you are ready to do it cold. Run the "
                        "chain check before you submit.")),

        # ===== TRANSFER: same move, a NEW source (weather), bank-partitioned from the taught source =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: how weather forecasts are made",
             ref="ACC-W910-INFO-LESSON-WEATHER", bank="weather",
             body=("Read this new explanatory source on weather forecasting. Because your job is to chain "
                   "choices, read the whole thing and notice the different choices the author makes: a framing "
                   "of forecasts as 'ordinary,' an order of steps from balloon to alert, a comparison, a "
                   "definition. Look for two or more that build the SAME point, and be ready to link them. The "
                   "text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Write a device-chain paragraph on a NEW text",
             ref="", bank="weather", rubric_ref="rc.staar", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="New text, same move. Write a short analytical paragraph that chains two or more of the "
                       "weather author's choices toward ONE point.",
                 closer="For example, you might link the way the author opens by calling forecasts 'ordinary' "
                        "with the way the author then details the hourly measurement behind them, to build the "
                        "point that an ordinary forecast rests on serious science. Name each choice and name the "
                        "single point they build. Run the chain check before you submit.")),
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
