"""
lesson_g11_l18_specific_example.py  -  G11 KC C.11.06, ARCHETYPE T3: EVIDENCE-INTEGRATION (PROVE, ceiling paragraph).

G11 course L18 (Unit 4, guided), rebuilt to the v3.1 build spec. Teaching point (kept): on a source-free
prompt, support a claim with ONE specific, developed own-knowledge example (named, detailed, tied to the
claim), rather than a vague generality. Written at the paragraph. Trait: Evidence and Commentary. KC C.11.06.
PROMPT-ONLY tier binds the source-free teaching prompt (SFA-LESSON-0001, curiosity vs usefulness) -> transfer
prompt (SFA-PROMPT-0002, individual vs community). rc.ap. PROVE=established-caveat.
v3.1 spine: ONE_IDEA teal callout + <ul> teach, coping-model First-try/Final with BEFORE/AFTER, REMEMBER
dashed 3-question checklist, explicit-choices discrimination, deterministic FRQ prompts. No coping persona
name (stateless). No source markup. No prior-work ref. No em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">On a source-free prompt, the strongest support is '
'<strong>one specific example</strong>, developed and tied to your claim, not a sweep of vague ones. A '
'specific example names the case, gives a telling detail, and says what it shows.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, run your example past all three:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0"><strong>Named?</strong> Is there ONE specific case named (a person, event, study, or experience)?</li>'
'<li style="margin:2px 0"><strong>Detailed?</strong> Is there a telling detail a reader could picture or check?</li>'
'<li style="margin:2px 0"><strong>Tied?</strong> Does a sentence say what the case shows about your claim?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">Any No, and you still have a generality, not an example.</div></div>')

COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer drafting support for the curiosity claim, then checking it:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Throughout history, many discoveries that seemed '
    'useless at first turned out to be very important later, which shows curiosity is worth supporting." That '
    'feels safe, but let me run the check.</p>'
    '<p style="margin:0 0 8px"><strong>Check it:</strong> Is there ONE named case? No, just "many discoveries." '
    'A telling detail? No. So a reader cannot picture or weigh anything. That is a generality, not an example.</p>'
    '<p style="margin:0"><strong>Final:</strong> "When Alexander Fleming noticed mold killing bacteria on a '
    'dish he had left out, he was following idle curiosity, not chasing a cure; that accident became penicillin, '
    'which shows why open-ended inquiry can pay off in ways no one could fund on purpose." One named case, a '
    'real detail, tied to the claim.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> A vague generality: "many discoveries" and "very important" '
    'name nothing a reader can check.</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> One specific, developed example: named case, telling detail, '
    'tied to the claim, so a reader can actually weigh it.</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1104-0018", grade="9-10", lesson_type=3,
    unit="G11 U4 - Source-free evidence (specific example, not generality)",
    title="Develop One Specific Example, Not a Vague Generality",
    target=("On a source-free prompt, support a claim with one specific, developed example from your own "
            "knowledge (named and detailed, tied to the claim), rather than a vague generality. Written at the "
            "paragraph. Trait: Evidence and Commentary."),
    acc_tags=["ACC.W.ARG.3", "CCSS.W.11-12.1"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "established-caveat", "kc": "C.11.06", "sot": "icm course-G11.md L18",
                "taught_stimulus": "ACC-W1112-SFA-LESSON-0001",
                "transfer_stimulus": "ACC-W910-SFA-PROMPT-0002",
                "one_idea": "On a source-free prompt, one specific developed example beats a pile of generalities.",
                "one_reminder": "Check the example: named case? telling detail? tied to the claim?",
                "playbook": "_phase2/playbook_T3_PROVE.md",
                "template": "locked L01 template; PROMPT-ONLY tier binds the source-free prompt (no fact table).",
                "version_note": ("V3.1 rebuild: replaced prose-wall body with the v3.1 spine (ONE_IDEA teal "
                                 "callout + <ul> teach, coping-model First-try/Final with BEFORE/AFTER, REMEMBER "
                                 "dashed 3-question checklist, explicit-choices discrimination, deterministic FRQ "
                                 "prompts). Removed leaked Grade-C labels. Kept id/type/KC/unit/bound stimuli."),
                "council": ("T3/PROVE G11 source-free guided rung: develops the specific own-knowledge example "
                            "vs vague generality move at the paragraph. PROVE=established-caveat."),
                "review_provenance": "built to the L01 v3.1 pattern"},
    fade_ledger_moves=["specific-own-example", "develop-and-tie-example"],
    slots=[
        Slot("TEACH", "teach_card", "The one idea: one specific example, developed and tied",
             body=(ONE_IDEA +
                   "On a source-free prompt you supply the evidence yourself, so the choice is yours: a sweep of "
                   "vague generalities, or one case built out. A specific example does three things:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Names the case</strong>: a person, event, study, or "
                   "experience a reader can picture (Fleming and the mold dish, not 'many discoveries').</li>"
                   "<li style=\"margin:4px 0\"><strong>Gives a telling detail</strong>: enough that a reader "
                   "could check it or feel its weight, not just a label.</li>"
                   "<li style=\"margin:4px 0\"><strong>Ties it to the claim</strong>: a sentence that says what "
                   "the case shows ('which shows ...'), so the example is not left hanging.</li></ul>"
                   "The move is develop-and-tie: state the example, give the detail, then say what it shows. The "
                   "trap is the vague generality that gestures at history without landing on a single case a "
                   "reader can actually weigh.")),
        Slot("TEACH", "stimulus_display", "Read the prompt: curiosity or usefulness?",
             ref="ACC-W1112-SFA-LESSON-0001", bank="sfa_curiosity_use",
             body=("Read this source-free prompt on whether society should support inquiry with no foreseeable "
                   "use. There is no passage; the example is yours to supply. As you read, pick ONE specific case "
                   "you could develop (a discovery, a historical event, something from your studies). The prompt "
                   "stays on screen while you work.")),
        Slot("MODEL", "annotated_before_after", "Watch a generality become a specific example",
             bank="sfa_curiosity_use",
             body=("Here is the move in action. Follow the writer draft a vague generality, run the check, catch "
                   "the problem, and rebuild it into one specific, developed example. " + COPING_HTML +
                   " Notice the difference: the first try gestures at 'many discoveries'; the final develops one "
                   "named case and ties it back. A specific developed example is what a reader can weigh." +
                   REMEMBER +
                   "When you build your own, name the case, add the detail, tie it back, then run the check.")),
        Slot("MODEL", "discrimination", "Which support is a specific developed example?",
             ref="", labeled_grade_c=True, bank="sfa_curiosity_use",
             body=("Spot the target before you write. For the curiosity claim, which option is a SPECIFIC, "
                   "developed example, and which are not? "
                   "(A) Across history, countless discoveries that once looked useless ended up mattering "
                   "enormously, and that pattern has repeated in field after field for centuries, which proves "
                   "curiosity always pays off.  "
                   "(B) Alexander Fleming was a Scottish scientist who worked in a large London hospital "
                   "laboratory and spent much of his long career studying many different kinds of bacteria.  "
                   "(C) Fleming, chasing no cure, noticed mold killing bacteria on a dish he had left out, and "
                   "that accident became penicillin, which shows open-ended inquiry can pay off unpredictably.  "
                   "(D) Fleming discovered penicillin by accident, which shows that open-ended inquiry is worth "
                   "supporting. "
                   "Correct: C."),
             choices=[
                 {"id": "A", "text": "Across history, countless discoveries that once looked useless ended up mattering enormously, and that pattern has repeated in field after field for centuries, which proves curiosity always pays off.",
                  "correct": False,
                  "why": "This is the vague generality. 'Countless discoveries' names no single case a reader can check, and the closing 'which proves' is tacked onto a sweep, not a developed example."},
                 {"id": "B", "text": "Alexander Fleming was a Scottish scientist who worked in a large London hospital laboratory and spent much of his long career studying many different kinds of bacteria.",
                  "correct": False,
                  "why": "It names a specific person with detail, but it never ties him to the claim: it is biography, not an example that shows anything about whether curiosity is worth supporting."},
                 {"id": "C", "text": "Fleming, chasing no cure, noticed mold killing bacteria on a dish he had left out, and that accident became penicillin, which shows open-ended inquiry can pay off unpredictably.",
                  "correct": True,
                  "why": "Correct. One named case, a telling detail (the mold on the left-out dish), and a tie to the claim ('which shows open-ended inquiry can pay off unpredictably'). That is the develop-and-tie move."},
                 {"id": "D", "text": "Fleming discovered penicillin by accident, which shows that open-ended inquiry is worth supporting.",
                  "correct": False,
                  "why": "This names the case and ties it to the claim, but it skips the telling detail: it never shows the mold on the left-out dish, so the example is asserted rather than developed. A reader cannot picture or weigh it."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this support most need?",
             bank="sfa_curiosity_use",
             body=("Diagnose before the reveal. A student wrote: 'A lot of great inventions came from people just "
                   "exploring ideas, and this happens all the time, which is why curiosity matters.' Which single "
                   "move would most improve it? "
                   "(A) replace the sweep with ONE specific case, named and developed, then tie it to the claim  "
                   "(B) add several more sweeping and general examples like this one so the paragraph covers still more of history  "
                   "(C) restate that this happens all the time more emphatically so that the central claim simply sounds much stronger  "
                   "(D) note that many experts and scholars now agree curiosity matters, so the overall point ends up feeling more backed"),
             feedback=("Correct: A. 'A lot of great inventions' and 'happens all the time' are the generality "
                       "problem. The fix develops one named case (who, what happened, why it matters) instead of "
                       "gesturing at many. More sweeps (B), emphasis (C), or appeals to experts (D) do not supply "
                       "the specific example.")),
        Slot("SUPPORTED", "production_frq", "Warm up: build the example with a frame",
             ref="", bank="sfa_curiosity_use", rubric_ref="rc.4trait", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="Warm up the move with a frame. Pick ONE specific case for the curiosity prompt, then fill "
                       "each blank:",
                 setapart_block=setapart("Fill in this frame:",
                                         "Claim: ____. When ____ (name the case), ____ (the telling detail); this shows ____ (tie back to the claim)."),
                 closer="Write out the filled-in frame as a short paragraph. Goal: one named case, one real "
                        "detail, one clear tie, not a generality.")),
        Slot("MODEL", "diagnosis_frq", "Check your example: specific, or general?",
             ref="", bank="sfa_curiosity_use", scored=True,
             body=frq_prompt(
                 intro="First watch the 3-question check run on a weak draft, then run it on a fresh paragraph of "
                       "your own.",
                 setapart_block=setapart("Weak draft to check:",
                                         "History shows many curious people made big discoveries that helped everyone, which is why society should back curiosity.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Named: is there ONE specific case named?", "No. 'Many curious people' names no one. Name a single case."),
                     ("Detailed: a telling detail a reader could picture?", "No. 'Big discoveries' is a label, not a detail. Add one."),
                     ("Tied: does a sentence say what it shows?", "Vaguely. 'Which is why' is attached to a sweep, so make the tie land on the named case."),
                 ]),
                 closer="Now write a fresh paragraph on ONE specific example, then run the same three questions. "
                        "For each No, use the fix: name it, detail it, tie it. Finish by naming the example you "
                        "developed.")),
        Slot("INDEPENDENT", "production_frq", "Develop a specific example on your own",
             ref="", bank="sfa_curiosity_use", rubric_ref="rc.4trait", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now, with no frame. Write ONE body paragraph for the curiosity prompt built "
                       "on a single specific, developed example from your own knowledge, tied to your claim.",
                 closer="Developing one real example, instead of gesturing at many, is what every strong "
                        "source-free argument is built on, and you are ready to do it cold. Run the 3-question "
                        "check (named? detailed? tied?) before you submit.")),
        Slot("TRANSFER", "stimulus_display", "Read a NEW prompt: the individual or the community?",
             ref="ACC-W910-SFA-PROMPT-0002", bank="sfa_individual_community",
             body=("A new source-free prompt on individual freedom versus the good of the community. Again there "
                   "is no passage; the example is yours to supply. Pick ONE specific case you can develop. Same "
                   "develop-and-tie move, new topic. The prompt stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Develop a specific example on a NEW prompt",
             ref="", bank="sfa_individual_community", rubric_ref="rc.4trait", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="New topic. Write ONE body paragraph for the individual-versus-community prompt built on a "
                       "single specific, developed example from your own knowledge, tied to your claim.",
                 closer="Same move as the curiosity paragraph: name the case, give the telling detail, tie it "
                        "back. Do not stay general. Run the 3-question check before you submit.")),
    ],
)

LESSONS = [LESSON]

if __name__ == "__main__":
    ok = True
    for L in LESSONS:
        qc_lesson(L); print(qc_report(L)); print(); ok = ok and L.qc["passed"]
    print(f"{sum(1 for L in LESSONS if L.qc['passed'])}/{len(LESSONS)} PASS")
    sys.exit(0 if ok else 1)
