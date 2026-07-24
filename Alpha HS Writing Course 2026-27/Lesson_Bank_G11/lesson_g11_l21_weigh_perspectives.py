"""
lesson_g11_l21_weigh_perspectives.py  -  G11 KC C.11.07, ARCHETYPE T3: EVIDENCE-INTEGRATION (PROVE, ceiling paragraph).

G11 course L21 (Unit 5, guided), REBUILT to the v3.1 build spec. Teaching point (kept): build a body paragraph
that WEIGHS a given perspective against the writer's own position (concede what holds, name the limit, advance
the writer's own view with an example), rather than summarizing the perspective. KC C.11.07.
mnemonic_status=established-caveat (PROVE). PERSPECTIVE-SET tier binds the multi-perspective teaching prompt.
Taught: MP-LESSON-0001 (public streets) -> transfer: MP-PERSP-0002 (cold privacy vs safety). rc.ap.
V3.1 spine: ONE_IDEA teal callout + minimum-teach list, bound source, coping-model before/after think-aloud,
named-moves decompose + REMEMBER dashed checklist, explicit-choices discrimination (no length/token confound,
no leaked labels), predict-the-fix with feedback reveal, fill-in SUPPORTED frame, scaffolded diagnosis, cold
INDEPENDENT, bank-partitioned TRANSFER. Deterministic FRQ prompts. No em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">To <strong>weigh</strong> a perspective means to do '
'three moves in order: <strong>concede</strong> what it gets right, name its <strong>limit</strong>, and '
'<strong>advance</strong> your own position against it with an example. Restating the perspective and calling '
'it reasonable is only a summary.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 moves</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, check your paragraph does all three, in order:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0"><strong>Concede</strong>: name what the perspective gets right, so you are fair.</li>'
'<li style="margin:2px 0"><strong>Limit</strong>: name where it falls short or what it ignores.</li>'
'<li style="margin:2px 0"><strong>Advance</strong>: state your own position against it, with a specific example.</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">Concede but never limit or advance, and you have agreed, not weighed.</div></div>')

COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer weighing Perspective One (streets should move traffic efficiently), thinking it through:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Perspective One argues streets should move traffic '
    'efficiently, because commutes and deliveries matter, and that is a fair point." Let me run the check: did I '
    'concede? Yes. Did I name a limit? No. Did I advance my own view? No. I only agreed.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> I keep the concede and add the limit. "Perspective '
    'One is right that reliable travel matters, but it treats a street as only a route." Better, but I still have '
    'not advanced a position of my own.</p>'
    '<p style="margin:0"><strong>Final:</strong> now I advance with an example. "...but it treats a street as '
    'only a route; a downtown that emptied once its shops lost foot traffic shows that pure efficiency can starve '
    'the street life a city depends on, which is why I would keep some blocks for people." Concede, limit, '
    'advance.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> Concede only: it restates Perspective One and calls it fair, so '
    'it is agreement, not weighing.</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> Concede + limit + advance: it grants the point, names what the '
    'view ignores, and advances the writer\'s own position with an example.</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W1112-L-G11-C1105-0021", grade="9-10", lesson_type=3,
    unit="G11 U5 - Weigh a perspective (concede, limit, advance)",
    title="Weigh a Perspective Against Your Own",
    target=("Build a body paragraph that weighs a given perspective against the writer's position (concede what "
            "holds, show where it falls short, advance the writer's own view with an example), rather than "
            "summarizing the perspective. Written at the paragraph. Trait: Evidence and Commentary."),
    acc_tags=["ACC.W.ARG.2", "ACC.W.ARG.4", "CCSS.W.11-12.1"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "established-caveat", "kc": "C.11.07", "sot": "icm course-G11.md L21",
                "taught_stimulus": "ACC-W1112-MP-LESSON-0001",
                "transfer_stimulus": "ACC-W910-MP-PERSP-0002",
                "playbook": "_phase2/playbook_T3_PROVE.md",
                "template": "locked L01 template; PERSPECTIVE-SET tier binds the 3-perspective prompt (no passage).",
                "one_idea": "To weigh a perspective = concede what it gets right, name its limit, advance your own position with an example.",
                "one_reminder": "Check the 3 moves: concede? limit? advance with an example?",
                "version_note": ("V3.1 rebuild (hand-authored). Replaced the pre-v3.1 prose-wall body + leaked "
                                 "'Grade-C'/'design bet' student text with the v3.1 spine: ONE_IDEA teal callout "
                                 "+ minimum-teach list, coping-model BEFORE/AFTER think-aloud, named-moves "
                                 "decompose + REMEMBER dashed checklist, explicit-choices discrimination, "
                                 "predict-the-fix reveal in feedback, fill-in SUPPORTED frame, scaffolded "
                                 "diagnosis, cold INDEPENDENT, bank-partitioned TRANSFER. Kept id/kc/type/unit/"
                                 "bound stimuli/teaching point."),
                "council": ("T3/PROVE G11 multi-perspective guided rung: develops E2 (weigh a perspective: "
                            "concede, limit, advance) at the paragraph. weigh-vs-summarize discrimination "
                            "labeled Grade-C in code only. PROVE=established-caveat.")},
    fade_ledger_moves=["weigh-a-perspective", "concede-limit-advance"],
    slots=[
        Slot("TEACH", "teach_card", "The one idea: concede, limit, advance",
             body=(ONE_IDEA +
                   "A perspective is a stated way of seeing the issue that the prompt hands you. On a "
                   "multi-perspective prompt, a body paragraph has to WEIGH one perspective, not report it. "
                   "Weighing is three moves, in order:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Concede</strong>: name what the perspective gets right, so "
                   "you are fair to it.</li>"
                   "<li style=\"margin:4px 0\"><strong>Limit</strong>: name where it falls short or what it "
                   "ignores.</li>"
                   "<li style=\"margin:4px 0\"><strong>Advance</strong>: state your own position against it, "
                   "ideally with a specific example.</li></ul>"
                   "'Perspective One is reasonable' is a summary. 'Perspective One is right that travel matters, "
                   "but it treats a street as only a route, which is why ...' is weighing. The trap is the polite "
                   "restatement that concedes everything and advances nothing.")),
        Slot("TEACH", "stimulus_display", "Read the issue and three perspectives: public streets",
             ref="ACC-W1112-MP-LESSON-0001", bank="mp_public_space",
             body=("Read the streets issue and its three perspectives. Pick ONE perspective to weigh in a "
                   "paragraph, and hold your own position in mind so you can advance it against that view. There "
                   "is no passage, so your example comes from your own knowledge. The prompt stays on screen "
                   "while you work.")),
        Slot("MODEL", "annotated_before_after", "Watch a summary become a weighed paragraph",
             bank="mp_public_space",
             body=("Here is the move in action. Follow the writer weigh Perspective One, running the check after "
                   "each try. " + COPING_HTML +
                   " Notice the difference: conceding alone is agreement; adding the limit and the advance is what "
                   "makes it weighing." + REMEMBER +
                   "When you build your own, do the three moves in order, then run the check.")),
        Slot("MODEL", "discrimination", "Which paragraph weighs the perspective?",
             ref="", labeled_grade_c=True, bank="mp_public_space",
             body=("Spot the target before you build it. Which option WEIGHS Perspective One (concede, limit, "
                   "advance), rather than summarizing or praising it? "
                   "(A) Perspective One makes a clear case that streets should move traffic efficiently, since "
                   "commutes and deliveries matter to the local economy, and that is a fair and well-argued point "
                   "worth taking seriously.  "
                   "(B) Perspective One is right that reliable travel matters, but it treats a street as only a "
                   "route; a downtown that emptied when its shops lost foot traffic is why I would keep some "
                   "blocks open to people.  "
                   "(C) Perspective One says streets should move traffic efficiently, and while some readers "
                   "disagree, it lays out its reasoning about commutes and deliveries fully, so it is one of the "
                   "stronger perspectives here.  "
                   "(D) Perspective One is right that reliable travel matters, but it treats a street as only a "
                   "route and ignores the people who live and shop along it. "
                   "Correct: B."),
             choices=[
                 {"id": "A", "text": "Perspective One makes a clear case that streets should move traffic efficiently, since commutes and deliveries matter to the local economy, and that is a fair and well-argued point worth taking seriously.",
                  "correct": False,
                  "why": "This concedes and then praises the view, but it never names a limit and never advances the writer's own position. Conceding alone is agreement, not weighing."},
                 {"id": "B", "text": "Perspective One is right that reliable travel matters, but it treats a street as only a route; a downtown that emptied when its shops lost foot traffic is why I would keep some blocks open to people.",
                  "correct": True,
                  "why": "Correct. It concedes what holds (reliable travel matters), names the limit (a street is treated as only a route), and advances the writer's own position with a specific example. That is concede, limit, advance."},
                 {"id": "C", "text": "Perspective One says streets should move traffic efficiently, and while some readers disagree, it lays out its reasoning about commutes and deliveries fully, so it is one of the stronger perspectives here.",
                  "correct": False,
                  "why": "This restates the view and rates it as strong. Noting that some readers disagree is not the same as naming a limit, and it advances no position of the writer's own."},
                 {"id": "D", "text": "Perspective One is right that reliable travel matters, but it treats a street as only a route and ignores the people who live and shop along it.",
                  "correct": False,
                  "why": "This concedes and names a real limit, but it stops at the objection. It never advances the writer's own position with an example, so it does two of the three moves and leaves the paragraph half-weighed."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this paragraph most need?",
             bank="mp_public_space",
             body=("Diagnose before the reveal. A student wrote: 'Perspective Two makes a strong case that streets "
                   "are public rooms, and I agree it is a good point that gathering matters.' Which single move "
                   "would most improve it? "
                   "(A) name where Perspective Two falls short, then advance the writer's own position against it "
                   "with a specific example  "
                   "(B) agree with Perspective Two even more warmly and add a line about how much the writer likes "
                   "that gathering matters  "
                   "(C) restate what Perspective Two says about streets being public rooms in fuller and more "
                   "complete detail  "
                   "(D) repeat that the point about gathering is very strong and one of the best perspectives the "
                   "prompt offers"),
             feedback=("Correct: A. The draft concedes but never limits or advances, so it is agreement, not "
                       "weighing. The fix names where Two falls short (perhaps it ignores the deliveries that "
                       "Perspective One cares about) and advances the writer's own position with an example. "
                       "Warmer agreement (B), fuller restatement (C), or more praise (D) add no weighing.")),
        Slot("SUPPORTED", "production_frq", "Warm up: write the limit-and-advance turn",
             ref="", bank="mp_public_space", rubric_ref="rc.4trait", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="Warm up with just the turn. Here is a concede clause already written for you:",
                 setapart_block=setapart("Concede clause given:",
                                         "Perspective Two is right that streets can be public rooms where people gather ..."),
                 closer="Write ONE sentence that finishes the turn: name a LIMIT of Perspective Two (what it "
                        "ignores), then ADVANCE your own position with a specific example. Start with 'but' or "
                        "'yet'. Then check it names a limit and advances a position, not just more agreement.")),
        # COUNCIL FIX (2026-07-24): Option A (later-in-arc), watch-then-do: demo preserved, produce is the graded
        # act. The old diagnosis_frq bundled a watched 3-move check demo (pre-answered (q,a) tuple rows that leaked
        # the answers) + a fresh weighed paragraph + a "use the limit you identified" tail in one box (unscoreable,
        # wired to no grader). The coping-model demo is PRESERVED as read-only narration (the concede/limit/advance
        # check shown running on the provided draft, in plain declarative prose). The student's ONLY graded act is
        # now the fresh weighed paragraph; the three moves sit read-only beneath as plain-string reminders; the
        # run-and-name tail is dropped. Kept as diagnosis_frq (paragraph grain needs an own-draft diagnosis for
        # model_sequence). Stays on the taught source (load balance).
        Slot("MODEL", "diagnosis_frq", "Weigh a perspective yourself, all three moves",
             ref="", bank="mp_public_space", rubric_ref="rc.4trait", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="First, watch the 3-move check run on the provided draft below. Its concede move is only "
                       "vague: calling the view an 'interesting idea' is praise, not a real concession of what it "
                       "gets right. It names no limit, so it never says where leaving the choice to users falls "
                       "short. And it advances no position of the writer's own, with no example. The draft only "
                       "restates Perspective Three, so it summarizes instead of weighing. Now write a fresh "
                       "paragraph of your own that does all three moves in order.",
                 setapart_block=setapart("Provided draft the check was run on:",
                                         "Perspective Three says users should decide what a street is for, which is an interesting idea worth considering.", "red"),
                 checklist_block=checklist(title="Check your paragraph against these (no need to type answers):", rows=[
                     "Concede: does it name what the perspective gets right?",
                     "Limit: does it name where the perspective falls short or what it ignores?",
                     "Advance: does it state your own position against it, with a specific example?",
                 ]),
                 closer="Write a fresh weighed paragraph on ONE perspective from the streets prompt, doing all "
                        "three moves in order: concede what it gets right, name its limit, then advance your own "
                        "position with a specific example. Run the three checks above before you submit.")),
        Slot("INDEPENDENT", "production_frq", "Weigh a perspective on your own",
             ref="", bank="mp_public_space", rubric_ref="rc.4trait", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now, weigh one perspective on the streets issue in a full paragraph.",
                 closer="Write ONE body paragraph that does all three moves in order: concede what the perspective "
                        "gets right, name its limit, and advance your own position with a specific example. "
                        "Weighing a perspective is what every real multi-perspective essay is built on, and you "
                        "are ready to do it cold. Run the 3-move check before you submit.")),
        Slot("TRANSFER", "stimulus_display", "Read a NEW perspective set: privacy and safety",
             ref="ACC-W910-MP-PERSP-0002", bank="mp_privacy_safety",
             body=("A new issue on privacy and public safety, with three given perspectives. Read it and pick ONE "
                   "perspective to weigh. There is no passage, so your example comes from your own knowledge. The "
                   "prompt stays on screen while you work. Same three moves, new topic.")),
        Slot("TRANSFER", "production_frq", "Weigh a perspective on a NEW set",
             ref="", bank="mp_privacy_safety", rubric_ref="rc.4trait", scored=True, unit="paragraph", frq_type="writing",
             body=frq_prompt(
                 intro="New set. Weigh one perspective on the privacy-and-safety issue in a full paragraph.",
                 closer="Write ONE body paragraph that concedes what the perspective gets right, names its limit, "
                        "and advances your own position with a specific example. Same concede-limit-advance move "
                        "as the streets paragraph, new topic. Run the 3-move check before you submit.")),
    ],
)

LESSONS = [LESSON]

if __name__ == "__main__":
    ok = True
    for L in LESSONS:
        qc_lesson(L); print(qc_report(L)); print(); ok = ok and L.qc["passed"]
    print(f"{sum(1 for L in LESSONS if L.qc['passed'])}/{len(LESSONS)} PASS")
    sys.exit(0 if ok else 1)
