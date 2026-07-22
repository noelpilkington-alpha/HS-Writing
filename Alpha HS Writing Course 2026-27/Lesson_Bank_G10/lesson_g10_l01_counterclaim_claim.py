"""
lesson_g10_l01_counterclaim_claim.py  -  G10 KC C.10.01, ARCHETYPE T2: CLAIM-BUILDING (STAND, sentence). V3.1.

G10 course L01 (Unit 1 Counterargument, intro). The counterclaim-aware claim (E1): concede the strongest real
point on the other side, then hold your position with a reason that answers it, in the shape "Although X, Y
because Z". Locked L01 template. CLAIM-TIER binds an issue_frame. Taught bank = congestion_pricing ->
transfer bank = daylight_saving (DI bank-partition). rc.staar, unit="sentence". STAND=proposal.

V3.1 spine (matches the G9 L01 v3.1 archetype): TEACH one idea (teal ONE_IDEA callout + a real <ul>, "counterclaim"
defined with a cue phrase) -> SOURCE (bound frame) -> MODEL coping-model think-aloud with literal BEFORE/AFTER ->
moves named + a REMEMBER 3-question checklist -> discrimination (Grade-C in code only, no leaked label, "because"
and "although" both appear on distractors so no surface-token confound) -> predict-the-fix (reveal in feedback) ->
SUPPORTED fill-in frame -> DIAGNOSIS check-and-fix on a provided weak draft -> INDEPENDENT cold write + say-the-
standard -> TRANSFER same move on the daylight-saving frame.

ONE IDEA: a counterclaim-aware claim concedes the strongest opposing point, then holds. ONE REMINDER: the 3
questions (concede? hold? does the reason answer it?). Passes all 23 lesson_contract gates. Own words, no
fabricated figures, no em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">In G9 you learned the basic move: concede a real '
'point, then answer it. Here you fold that whole move <strong>into the claim itself</strong>. A counterclaim-aware '
'claim <strong>CONCEDES</strong> the strongest point on the other side and <strong>HOLDS</strong> your position in '
'the same sentence, so your argument anticipates the objection from its very first line. The shape is '
'<strong>Although X, Y because Z</strong>.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit any claim, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Does it name the other side\'s strongest point (concede)?</li>'
'<li style="margin:2px 0">Does it hold your own position?</li>'
'<li style="margin:2px 0">Does the reason answer that objection, not just repeat your side?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, it is not counterclaim-aware yet.</div></div>')

# coping-model think-aloud panel: a WRITTEN drafting process (attempt -> test -> revise), then the endpoints.
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer thinking it through, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Cities should charge downtown tolls because traffic '
    'is bad." Check it: does it answer the other side? No, it never mentions the drivers a toll would hurt. '
    'Anyone worried about cost is left out. Rebuild it.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "Although some drivers cannot shift their hours, '
    'cities should charge downtown tolls." Better, it concedes a real objection. Does it hold my position? Yes. '
    'Does the reason answer the objection? There is no reason yet. Add one that speaks to those drivers.</p>'
    '<p style="margin:0"><strong>Final:</strong> "Although congestion tolls can burden drivers who cannot shift '
    'their hours, cities should still charge them, because the toll money can fund the buses and trains those '
    'same drivers need." Concede, hold, and the reason answers the objection. That passes.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "Cities should charge downtown tolls because traffic is bad." '
    '(one-sided; ignores the objection)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "Although congestion tolls can burden drivers who cannot shift '
    'their hours, cities should still charge them, because the toll money can fund the buses and trains those '
    'drivers need." (counterclaim-aware: concede, then hold)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1001-0001", grade="9-10", lesson_type=2,
    unit="G10 U1 - Counterargument (counterclaim-aware claim)",
    title="Concede a Point, Then Hold Your Ground",
    target=("Write a counterclaim-aware claim: name the strongest point on the other side, then hold your "
            "position with a reason that answers it, in the shape Although X, Y because Z. Written at the "
            "sentence. Trait: Thesis/Purpose."),
    acc_tags=["ACC.W.ARG.2", "CCSS.W.9-10.1a"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.01", "sot": "icm course-G10.md L01",
                "taught_stimulus": "ACC-W910-FRAME-CONGESTION",
                "transfer_stimulus": "ACC-W910-FRAME-DST",
                "playbook": "_phase2/playbook_T2_STAND.md",
                "template": "locked L01 template; CLAIM-TIER binds issue_frame.",
                "one_idea": "A counterclaim-aware claim concedes the strongest opposing point, then holds.",
                "one_reminder": "3 questions: concede the other side? hold your position? does the reason answer it?",
                "spiral_note": ("2026-07-21 spiral reframe: G9 now OWNS introductory counterargument (G9 L19 recognize, "
                                "L20 concede+answer at the sentence, L21 answer in a short paragraph with a reason). "
                                "This G10 lesson is the deeper rung: it no longer re-teaches the basic concede+answer "
                                "as brand-new, it folds the whole move INTO the claim sentence (counterclaim-aware "
                                "claim that anticipates the objection). ONE_IDEA + teach intro + goal reframed to open "
                                "on the G9 build; id/type/slots/gates unchanged."),
                "version_note": ("V3.1: rebuilt to the G9 L01 v3.1 archetype - teal ONE_IDEA callout + a real <ul> "
                                 "teach list (no prose wall), coping-model think-aloud with literal BEFORE/AFTER "
                                 "(SRSD model-it), REMEMBER 3-question check tool, discrimination broke the "
                                 "surface-token confound (both 'although' and 'because' appear on distractors), "
                                 "removed the leaked Grade-C/design-bet labels from student text (labeled_grade_c "
                                 "held in code only), autonomy + say-the-standard on the independent write."),
                "council": ("T2/STAND counterargument intro: introduces E1 counterclaim-aware claim (concede-"
                            "then-hold, Although X Y because Z). counterclaim defined in TEACH. concede-and-hold-"
                            "vs-ignore discrimination is the Grade-C discriminate-before-produce move, labeled in "
                            "code only. STAND=proposal; sentence ceiling.")},
    fade_ledger_moves=["counterclaim-aware-claim", "although-X-Y-because-Z"],
    slots=[
        # ===== TEACH: ONE idea only (teal callout + a real list; counterclaim defined with a cue phrase) =====
        Slot("TEACH", "teach_card", "The one idea: concede, then hold",
             body=(ONE_IDEA +
                   "In G9 you built the concede-then-answer move as two beats: name the other side's point, then "
                   "answer it. This year you make it tighter. You fold the concession and the stand into a single "
                   "claim sentence, so the claim itself already anticipates the objection. Two moves do that work:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>CONCEDE</strong>: name the strongest objection out loud "
                   "with an 'although' clause. A <strong>counterclaim</strong> is a point that someone who "
                   "disagrees with you would make, and naming it shows you have thought the issue through.</li>"
                   "<li style=\"margin:4px 0\"><strong>HOLD</strong>: state your position in that same sentence, "
                   "and back it with a reason that answers the objection you just named, not just a fresh point "
                   "for your own side.</li></ul>"
                   "Put together, that is the shape <strong>Although X, Y because Z</strong>: <em>Although X (the "
                   "other side's real point), Y (your position) because Z (a reason that still wins).</em> The "
                   "trap is the one-sided claim that ignores the obvious objection, which a reader notices at "
                   "once. Goal today: write a claim that folds the counterclaim in and holds your ground.")),
        Slot("TEACH", "stimulus_display", "The debate: congestion pricing",
             ref="ACC-W910-FRAME-CONGESTION", bank="congestion_pricing",
             body=("Read the short framing of the debate, then take a side. Notice the strongest point on the "
                   "other side, because you will concede it inside your claim. You only need the topic and the "
                   "two sides.")),

        # ===== MODEL (before the quiz): coping-model think-aloud, with the check tool folded in =====
        Slot("MODEL", "annotated_before_after", "Watch a one-sided claim become counterclaim-aware",
             bank="congestion_pricing",
             body=("Here is the skill in action. Follow the writer's thinking below. " + COPING_HTML +
                   " Notice the two moves that turned the BEFORE into the AFTER: the writer <strong>conceded</strong> "
                   "the strongest objection with an 'although' clause, then <strong>held</strong> the position "
                   "with a reason that answered it. " + REMEMBER +
                   "When you write your own, build it the same way: concede first, then hold with a reason that "
                   "answers the objection, and run the 3 questions before you submit.")),
        Slot("MODEL", "discrimination", "Which claim answers the other side?",
             ref="", labeled_grade_c=True, bank="congestion_pricing",
             body=("Now that you have seen one built, spot the target on a fresh angle of the same debate. Which "
                   "claim is counterclaim-aware: it concedes a real point AND then holds the position with a "
                   "reason that answers it? "
                   "(A) The city should charge every driver a toll to enter downtown at rush hour because it clears the crowded streets, cuts the smog that hangs over the blocks, keeps the sidewalks safer, and lets the buses and delivery trucks run on time for everyone.  "
                   "(B) Although a downtown toll would keep the busiest streets clear, it could still drive away the shoppers whom downtown stores depend on to survive.  "
                   "(C) Although a downtown toll could scare off some shoppers who dislike paying to drive in, the city should still charge it because the toll money can fund frequent buses that bring even more customers to those same stores.  "
                   "(D) Although a downtown toll could annoy some drivers who resent paying new fees, the city should still charge it to enter downtown at rush hour. "
                   "Correct: C. (A) piles on same-side reasons but never concedes the objection, so a reader "
                   "worried about losing shoppers is unanswered. (B) opens with 'although' but then holds the OTHER side, so "
                   "it never states your position. (D) concedes and holds but stops there, giving no reason at all, "
                   "so it never answers the objection. (C) concedes the objection and then holds the position with a "
                   "reason that answers it. Concede and hold is the move, not any single word."),
             choices=[
                 {"id": "A", "text": "The city should charge every driver a toll to enter downtown at rush hour because it clears the crowded streets, cuts the smog that hangs over the blocks, keeps the sidewalks safer, and lets the buses and delivery trucks run on time for everyone.",
                  "correct": False,
                  "why": "This has 'because' and four reasons, but every one is on your side. It never concedes the objection, so a reader worried about downtown stores losing shoppers is left unanswered. Piling on same-side reasons is not conceding."},
                 {"id": "B", "text": "Although a downtown toll would keep the busiest streets clear, it could still drive away the shoppers whom downtown stores depend on to survive.",
                  "correct": False,
                  "why": "This opens with 'although' but then swings to the OTHER side and holds their point, so it never states or holds your position. An 'although' clause alone is not counterclaim-aware."},
                 {"id": "C", "text": "Although a downtown toll could scare off some shoppers who dislike paying to drive in, the city should still charge it because the toll money can fund frequent buses that bring even more customers to those same stores.",
                  "correct": True,
                  "why": "Correct. It concedes the strongest objection ('although ...'), holds the position ('the city should still charge it'), and the reason answers the objection (the toll money funds frequent buses that bring even more customers to those same stores). Concede, hold, and answer."},
                 {"id": "D", "text": "Although a downtown toll could annoy some drivers who resent paying new fees, the city should still charge it to enter downtown at rush hour.",
                  "correct": False,
                  "why": "This concedes an objection and holds the position, but it stops there with no 'because' reason at all, so nothing answers the objection. Concede-and-hold without a reason is only two of the three moves."},
             ]),
        # SECOND minimal pair: all three keep the same Although X, Y because Z surface (both cue words present),
        # so the confound is now semantic, not the surface tokens. Different axis than the slot above (which
        # tested whether a concession was present and which side was held): this tests whether the concession is
        # a REAL opposing point (Q1) and whether the reason ANSWERS the objection rather than adding a same-side
        # point (Q3). Correct (C) is deliberately NOT the longest option.
        Slot("MODEL", "discrimination", "Spot the claim whose reason answers the objection",
             ref="", labeled_grade_c=True, bank="congestion_pricing",
             body=("All three take a side on the downtown toll and use the Although X, Y because Z shape. Which one "
                   "is fully counterclaim-aware: it concedes a real objection, holds the position, and gives a "
                   "reason that answers that objection? "
                   "(A) Although a downtown toll would cost daily commuters more money out of pocket each and every week, the city should still charge it because rush-hour traffic downtown keeps getting worse and slower for everyone.  "
                   "(B) Although a downtown toll is a smart, forward-looking policy, the city should charge it because the money can fund the cheaper buses that low-income riders need.  "
                   "(C) Although a downtown toll would cost daily commuters more, the city should charge it because the revenue can fund cheaper transit passes those commuters can switch to.  "
                   "(D) Although drivers would have to set up a new toll account before entering downtown, the city should still charge the toll because the revenue can repave the worn downtown streets. "
                   "Correct: C. (A) concedes a real cost but the reason only adds a same-side point and never "
                   "answers that cost. (B) praises your own policy instead of naming the other side's objection, "
                   "so nothing is actually conceded. (D) concedes only a minor setup hassle, not the strongest "
                   "objection, so it dodges the real cost concern. (C) concedes the real objection, holds the "
                   "position, and the reason answers it. The move is semantic, not the words although or because."),
             choices=[
                 {"id": "A", "text": "Although a downtown toll would cost daily commuters more money out of pocket each and every week, the city should still charge it because rush-hour traffic downtown keeps getting worse and slower for everyone.",
                  "correct": False,
                  "why": "This concedes a real cost and holds its side, but the reason only adds a fresh point for your own side and never answers the cost the toll puts on those commuters."},
                 {"id": "B", "text": "Although a downtown toll is a smart, forward-looking policy, the city should charge it because the money can fund the cheaper buses that low-income riders need.",
                  "correct": False,
                  "why": "The opening clause praises your own policy instead of naming the other side's objection, so nothing is actually conceded even though it holds a position and gives a reason."},
                 {"id": "C", "text": "Although a downtown toll would cost daily commuters more, the city should charge it because the revenue can fund cheaper transit passes those commuters can switch to.",
                  "correct": True,
                  "why": "Correct. It concedes the real objection that the toll costs commuters more, holds the position, and the reason answers that objection because the revenue funds cheaper transit those same commuters can use."},
                 {"id": "D", "text": "Although drivers would have to set up a new toll account before entering downtown, the city should still charge the toll because the revenue can repave the worn downtown streets.",
                  "correct": False,
                  "why": "This concedes only a minor setup hassle instead of the strongest objection, so it sidesteps the real cost concern. Conceding a weak point and ignoring the strong one is not a fair concession."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this one-sided claim most need?",
             bank="congestion_pricing",
             body=("Diagnose this draft before the reveal. A student wrote: 'Cities should charge downtown tolls "
                   "because traffic is bad.' The strongest objection, that tolls hit low-income drivers hardest, "
                   "is never mentioned. Which single move would most improve the claim? "
                   "(A) concede the objection about low-income drivers, then hold the position with a reason that answers it (Although X, Y because Z)  "
                   "(B) pile on a second reason for your own side, such as that tolls also cut pollution and speed up downtown traffic for everyone else  "
                   "(C) reword the claim in much stronger, more forceful language so it sounds more confident and harder for any reader to argue against  "
                   "(D) remove the 'because' reason so the claim is short and direct and simply states the position without any extra explanation"),
             feedback=("Correct: A. The claim is one-sided: it never answers the obvious objection that tolls "
                       "burden drivers who cannot shift their hours. The fix is the counterclaim-aware shape: "
                       "'Although tolls can burden those drivers, cities should charge them because the money "
                       "funds transit they need.' A second same-side reason (B) or a more forceful tone (C) still "
                       "ignore the other side; removing the reason (D) makes it weaker.")),

        # ===== SUPPORTED: framed write (fill-in frame) on the taught topic =====
        Slot("SUPPORTED", "production_frq", "Finish the claim: concede, then hold",
             ref="", bank="congestion_pricing", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on the two moves.",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "Although ______ [the other side's strongest point], ______ [your "
                                         "position] because ______ [a reason that answers the objection]."),
                 closer="Concede a real point, then hold your position with a reason that answers it. Do not "
                        "ignore the other side. Then check it against the 3 questions.")),
        # DIAGNOSIS = a CHECK-and-FIX exercise on a PROVIDED weak draft (stays on the taught topic; no new source).
        Slot("MODEL", "diagnosis_frq", "Check and fix a weak draft with the 3 questions",
             ref="", bank="congestion_pricing", scored=True,
             body=frq_prompt(
                 intro="Run the 3-question test on this weak draft, then rewrite it into a counterclaim-aware claim.",
                 setapart_block=setapart("Weak draft to fix:", "Tolls are a good idea because they reduce traffic.", "red"),
                 checklist_block=checklist(title="Run the test:", rows=[
                     ("Does it name the other side's strongest point?",
                      "No, it never mentions the drivers the toll burdens. Add an 'although' clause that concedes it."),
                     ("Does it hold a clear position?", "Yes, it backs the toll."),
                     ("Does the reason answer that objection?",
                      "No. 'Reduce traffic' just repeats a same-side point. Tie the reason to the objection you conceded."),
                 ]),
                 closer="Now rewrite the weak draft into one counterclaim-aware claim that passes all three. Then "
                        "name the objection your claim concedes.")),

        # ===== INDEPENDENT: cold write on the taught topic (no frame) + autonomy + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write a counterclaim-aware claim on your own",
             ref="", bank="congestion_pricing", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="On your own now, no frame. The task: should cities charge a toll to drive downtown at "
                       "rush hour?",
                 closer="Pick the side you actually hold, concede the strongest objection, then hold your "
                        "position with a reason that answers it (Although X, Y because Z). This concede-then-hold "
                        "move is what every real argument that takes the other side seriously is built on, and "
                        "you are ready to do it cold. Check your sentence against the 3 questions before you "
                        "submit.")),

        # ===== TRANSFER: same move, a NEW topic (daylight saving), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "The debate: daylight saving time",
             ref="ACC-W910-FRAME-DST", bank="daylight_saving",
             body=("A different debate now, so you build a fresh claim instead of reusing the last one. Read the "
                   "short framing, then take a side. Notice the strongest point on the other side to concede. You "
                   "only need the topic and the two sides.")),
        Slot("TRANSFER", "production_frq", "Write a counterclaim-aware claim on a NEW topic",
             ref="", bank="daylight_saving", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="New topic. The task: should the United States stop switching the clocks twice a year?",
                 closer="Write ONE counterclaim-aware claim: concede the strongest point on the other side, then "
                        "hold your position with a reason that answers it (Although X, Y because Z). Same concede-"
                        "then-hold move as the congestion claim, new topic. Do not ignore the other side. Check it "
                        "against the 3 questions before you submit.")),
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
