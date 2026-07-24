"""
lesson_g9_l27_formal_tone_v3_1.py  -  G9 KC C.9.06, ARCHETYPE T6: EDITING-IN-CONTEXT (SPOT, ceiling sentence).
V3.1. NEW LESSON added 2026-07-14 per the Fable-5 course-design audit (formal-tone gap): ACC.W.ARG.4 /
CCSS W.9-10.1d "establish and maintain a formal style and objective tone" was owned by NO course at the
composition tier. Noel's decision: own it at G9 (flip ARG.4 external->hs on C.9.06; add this lesson).

TEACHING POINT: register-as-a-rhetorical-choice. Strip informal register and first-person editorializing from a
claim/warrant sentence so it reads as formal and objective, WITHOUT changing the position. Scope: this is the
DRAFTING-TIME rhetorical decision (no "I think," no slang, no reader-address, an objective stance), NOT the
grammar/mechanics of style (that stays app-owned: EGUMPP + HS Language). Bound stimuli from the approved slate:
taught FRAME-FOURDAYWEEK (bank four_day_week) -> transfer FRAME-FREETRANSIT (bank free_transit), partitioned.

Built to icm/_config/v3_1-lesson-build-spec.md (the pattern that clears all 23 lesson_contract gates + the
Fable-5 reviewer). Own words, no fabricated figures, no em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">An essay keeps a <strong>formal, objective</strong> '
'tone: state the position as a fact about the issue, not as your personal feeling. Cut <strong>I think</strong>, '
'slang, and talking to the reader; the claim itself gets stronger, not weaker.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit a claim or reason sentence, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Did I cut the first person (I think, in my opinion, I feel)?</li>'
'<li style="margin:2px 0">Did I cut slang and casual words (kids, stuff, totally, a ton of)?</li>'
'<li style="margin:2px 0">Did I stop talking to the reader (you, we, come on) and state it about the issue?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, the tone is still informal. The position can stay the same; only the register changes.</div></div>')

# coping-model think-aloud: a WRITTEN editing process (draft -> run the check -> catch the informal register ->
# revise), then the endpoints. Literal BEFORE and AFTER (content_depth). No named near-peer (Timeback rule).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer editing one claim sentence for tone, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First draft:</strong> "I honestly think a four-day week would be way '
    'better for kids, and you can totally see why." Run the check: any first person? Yes, "I honestly think." '
    'Any slang? Yes, "way better," "kids," "totally." Talking to the reader? Yes, "you can see." Fix all three.</p>'
    '<p style="margin:0 0 8px"><strong>Second draft:</strong> "A four-day week would be better for students." '
    'Better, the I-think, the slang, and the "you" are gone. But "better" alone is thin; keep the real reason '
    'from the first draft so the position still has weight.</p>'
    '<p style="margin:0"><strong>Final:</strong> "A four-day week would benefit students because the extra day '
    'gives them time to rest and recover." Same position, now stated as a claim about the issue: formal and '
    'objective, and stronger for it.</p>'
  '</div>'
  '<div style="background:#fef2f2;padding:10px 14px;border-top:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px"> "I honestly think a four-day week would be way better for kids, '
    'and you can totally see why." (first person, slang, talks to the reader)</span></div>'
  '<div style="background:#f0fdf4;padding:10px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px"> "A four-day week would benefit students because the extra day '
    'gives them time to rest and recover." (formal, objective, same position)</span></div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C906-0027", grade="9-10", lesson_type=6,
    unit="G9 U3 - Cohesion, tone & paragraph mastery (formal objective tone)",
    title="Sound Like an Essay: Formal, Objective Tone",
    target=("Strip informal register and first-person editorializing from a claim or reason sentence so it "
            "reads as formal and objective, without changing the position: cut 'I think,' slang, and talking to "
            "the reader, and state the point about the issue. Written at the sentence. Trait: Style/Tone."),
    acc_tags=["ACC.W.ARG.4", "CCSS.W.9-10.1d"],
    provenance={"copyright": "own_authored", "authored": "2026-07-14", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.9.06", "sot": "COURSE_DESIGN_AUDIT_2026-07-14.md (formal-tone gap)",
                "taught_stimulus": "ACC-W910-FRAME-FOURDAYWEEK",
                "transfer_stimulus": "ACC-W910-FRAME-FREETRANSIT",
                "template": "v3.1 lesson build spec; cloned from L15 (T6/SPOT sentence-edit). COHESION-TIER binds a lightweight issue_frame (material is a provided sentence, inline).",
                "one_idea": "An essay states its position with a formal, objective tone (no I-think, slang, or reader-address).",
                "one_reminder": "3-question check: cut first person? cut slang? stop talking to the reader?",
                "version_note": ("NEW lesson (design-audit gap): ACC.W.ARG.4 / W.9-10.1d formal-tone was unowned "
                                 "at the composition tier. Flipped ARG.4 external->hs on C.9.06 and authored this "
                                 "T6 sentence-edit lesson to the v3.1 spec. Scope = the rhetorical register "
                                 "decision at drafting (I-think / slang / reader-address / objective stance); the "
                                 "grammar of style stays app-owned (EGUMPP + HS Language). Discrimination confound "
                                 "broken: a distractor is formal-sounding but abandons the position, so the "
                                 "invariant is 'formal AND same position,' not 'shortest/plainest.'"),
                "review_provenance": "built to icm/_config/v3_1-lesson-build-spec.md (pattern clearing all 23 gates + Fable-5).",
                "council": "T6/SPOT tone: register-as-rhetorical-choice; mechanics of style gated (app-owned); taught by the tone JOB. formal-vs-informal discrimination labeled Grade-C in code. SPOT=proposal; ceiling sentence."},
    fade_ledger_moves=["formal-objective-register", "cut-first-person-and-slang"],
    slots=[
        # ===== TEACH: ONE idea in a callout + the informal/formal contrast as a real LIST (no wall of text) =====
        Slot("TEACH", "teach_card", "State the position, do not narrate your feelings",
             body=(ONE_IDEA +
                   "An argument or explanation is read as a piece about the issue, not as a diary entry, so its "
                   "sentences keep a formal, objective tone. That does not mean stiff or fancy; it means you "
                   "state the point as a claim about the world, and you leave out three things that make writing "
                   "sound casual. Two versions to keep apart:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>INFORMAL</strong>: leans on the first person, slang, or "
                   "the reader ('I really think schools should totally do this, you know?').</li>"
                   "<li style=\"margin:4px 0\"><strong>FORMAL and objective</strong>: the same position stated "
                   "about the issue, with the I-think, the slang, and the 'you' removed ('Schools should adopt a "
                   "four-day week because it gives students time to recover').</li></ul>"
                   "Three things to cut: (1) first person, 'I think,' 'in my opinion,' 'I feel'; (2) slang and "
                   "casual words, 'kids,' 'stuff,' 'totally,' 'a ton of'; (3) talking to the reader, 'you,' 'we,' "
                   "'come on.' Keep the position and the reason exactly, change only the register. The polish of "
                   "grammar comes from your other courses; today's job is the tone move. Goal: rewrite a provided "
                   "sentence into a formal, objective one without changing what it claims.")),
        Slot("TEACH", "stimulus_display", "The topic: a four-day school week",
             ref="ACC-W910-FRAME-FOURDAYWEEK", bank="four_day_week",
             body=("The sentences you will fix are about the four-day school week. Read this short orientation so "
                   "the topic is familiar. You are not writing about the four-day week from scratch here; you are "
                   "fixing the tone of a sentence that is given to you, keeping its position the same.")),

        # ===== MODEL (before the quiz): coping-model think-aloud with the check tool folded in =====
        Slot("MODEL", "annotated_before_after", "Watch a writer fix an informal claim",
             bank="four_day_week",
             body=("Here is the skill in action. Follow the writer's editing below. " + COPING_HTML +
                   " Notice the moves that turned the BEFORE into the AFTER: the writer cut the first person, the "
                   "slang, and the reader-address, and kept the position and its reason. " + REMEMBER +
                   "When you fix your own sentence, do the same: cut the three informal markers, keep the point, "
                   "and run the 3 questions before you submit.")),
        Slot("MODEL", "discrimination", "Which version is formal and keeps the position?",
             ref="", labeled_grade_c=True, bank="four_day_week",
             body=("Now that you have seen one built, spot the target. Here is a DIFFERENT informal draft: 'Trust "
                   "me, cramming five days into four is gonna wear kids out big time, so it is honestly a bad "
                   "move.' Which rewrite is formal and objective AND keeps the same position? "
                   "(A) A compressed four-day week is honestly just too rough on kids, and anyone can see the days "
                   "would drag on forever and leave everyone worn out.  "
                   "(B) Many districts have experimented with compressed weekly calendars over the past decade.  "
                   "(C) A compressed four-day week would tire students, because packing five days of instruction "
                   "into four lengthens each school day.  "
                   "(D) It is my firm belief that a compressed four-day week would exhaust students by lengthening "
                   "each school day. "
                   "Correct: C. It drops the 'trust me,' the slang, and the reader-address while keeping the claim "
                   "and its reason. (A) stays informal; (B) is formal but drops the position; (D) sounds dressed "
                   "up but keeps the first person ('my firm belief')."),
             choices=[
                 {"id": "A", "text": "A compressed four-day week is honestly just too rough on kids, and anyone can see the days would drag on forever and leave everyone worn out.",
                  "correct": False,
                  "why": "Still informal: 'honestly,' 'too rough on kids,' and 'anyone can see' keep the casual, reader-directed tone. Sounding certain is not the same as sounding formal and objective."},
                 {"id": "B", "text": "Many districts have experimented with compressed weekly calendars over the past decade.",
                  "correct": False,
                  "why": "This IS formal and objective, but it changed the point: it no longer takes the position that a compressed week tires students. Formal tone must keep the original claim, not drop it."},
                 {"id": "C", "text": "A compressed four-day week would tire students, because packing five days of instruction into four lengthens each school day.",
                  "correct": True,
                  "why": "Correct. The 'trust me,' the slang, and the direct address are gone, and the position plus its reason are intact. Formal tone AND same claim is the target."},
                 {"id": "D", "text": "It is my firm belief that a compressed four-day week would exhaust students by lengthening each school day.",
                  "correct": False,
                  "why": "The wording sounds dressed up, but 'It is my firm belief' is still first person. Formal tone states the point as a claim about the issue, not as your personal belief, however formal the phrasing looks."},
             ]),
        Slot("MODEL", "discrimination", "Which rewrite removes every informal marker?",
             ref="", labeled_grade_c=True, bank="four_day_week",
             body=("A second quick check, a different slip this time. The informal draft was: 'In my opinion a "
                   "four-day week is honestly a game changer for kids, so you should really get behind it.' Which "
                   "rewrite removes every informal marker so the sentence reads as formal and objective while "
                   "keeping the position? "
                   "(A) A four-day week is a strong improvement, so you should really get behind it once you "
                   "notice how run down students actually get by Friday.  "
                   "(B) A four-day week is a strong improvement for students because it gives them a full day to rest.  "
                   "(C) In my opinion a four-day week is a real game changer for students because they get a full day to rest.  "
                   "(D) A four-day week is a total game changer for students because it gives them a full day to rest. "
                   "Correct: B. It cuts the first person, the slang, and the reader-address together, while the "
                   "others each leave one behind: (A) keeps the reader-address, (C) keeps the first person and "
                   "slang, and (D) keeps the slang ('total game changer')."),
             choices=[
                 {"id": "A", "text": "A four-day week is a strong improvement, so you should really get behind it once you notice how run down students actually get by Friday.",
                  "correct": False,
                  "why": "This still speaks to the reader with 'you should really get behind it,' so the tone stays informal even though the first person and the slang are gone."},
                 {"id": "B", "text": "A four-day week is a strong improvement for students because it gives them a full day to rest.",
                  "correct": True,
                  "why": "Correct. It removes the first person, the slang, and the reader-address all at once while keeping the position and its reason."},
                 {"id": "C", "text": "In my opinion a four-day week is a real game changer for students because they get a full day to rest.",
                  "correct": False,
                  "why": "This stops talking to the reader but keeps 'In my opinion' and 'game changer,' so first person and slang still make it informal."},
                 {"id": "D", "text": "A four-day week is a total game changer for students because it gives them a full day to rest.",
                  "correct": False,
                  "why": "The first person and reader-address are gone, but 'total game changer' is still slang. One informal marker is enough to keep the tone casual."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this sentence most need for tone?",
             bank="four_day_week",
             body=("Diagnose this draft before the reveal. A sentence reads: 'In my opinion schools should totally "
                   "switch, because honestly the current schedule is a mess for a lot of families.' Which single "
                   "edit would most improve its tone for an essay? "
                   "(A) cut the first person and the slang and state it about the issue, keeping the reason: "
                   "'Schools should switch because the current schedule strains many families'  "
                   "(B) add an exclamation point at the end so the sentence sounds more confident and forceful, "
                   "the way you would say it out loud to a friend who already agrees with you  "
                   "(C) delete the whole 'because' clause so the sentence is shorter and quicker to read, even "
                   "though that throws away the reason the position rests on entirely  "
                   "(D) swap 'schools' for 'we' so the sentence feels warmer and casually pulls the reader onto "
                   "your side, the opposite of the objective stance an essay wants"),
             feedback=("Correct: A. The tone problem is 'In my opinion,' 'totally,' 'honestly,' and 'a mess,' not "
                       "the length. Cutting them and stating the point about the issue keeps the position and its "
                       "reason while making the register formal. An exclamation point (B) makes it more casual; "
                       "deleting the reason (C) weakens the claim; 'we' (D) adds reader-address, the opposite of "
                       "objective.")),

        # ===== SUPPORTED: framed edit (fill-in frame) on the taught topic (source read at TEACH step 2) =====
        Slot("SUPPORTED", "production_frq", "Rewrite the claim in a formal tone",
             ref="", bank="four_day_week", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="revision",
             body=frq_prompt(
                 intro="Rewrite the sentence in a formal, objective tone, keeping the position. Here is the "
                       "informal sentence to fix: 'I really think a four-day week is a great idea because kids "
                       "are just way too burned out these days.'",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "A four-day week ______ [state the position about the issue, no I-think] because ______ [keep the reason, no slang]."),
                 closer="Cut the first person and the slang, state the point about the issue, and keep the reason. "
                        "Do not change what the sentence claims. Then run the 3-question check before you submit.")),
        # COUNCIL FIX (2026-07-24): Option A (later-in-arc). One graded rewrite; checks read-only beneath; name-act dropped.
        # The old diagnosis_frq bundled a part-pre-answered 3-question check + a rewrite + a name-which-question tail
        # in one box (unscoreable, wired to no grader). Now: ONE graded rewrite of the provided weak draft; the checks
        # are plain read-only reminders (no self-answered yes/no fields); the name-act is deleted. Stays on the taught
        # topic = no new source to read (load balance).
        Slot("MODEL", "diagnosis_frq", "Fix an informal draft: make the tone formal",
             ref="", bank="four_day_week", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="writing",
             body=frq_prompt(
                 intro="The draft below is informal on all three counts: 'I think' is first person, 'no-brainer' "
                       "and 'way more' are slang, and 'you can tell' talks to the reader. Rewrite it into one "
                       "formal, objective sentence that keeps the same position and reason.",
                 setapart_block=setapart("Weak draft to fix:",
                                         "I think you can tell a four-day week is a no-brainer, because kids these days just need way more of a break.", "red"),
                 checklist_block=checklist(title="Make your rewrite pass these (no need to type answers):", rows=[
                     "Did you cut the first person (I think, in my opinion, I feel)?",
                     "Did you cut slang and casual words (no-brainer, kids, way more)?",
                     "Did you stop talking to the reader (you) and state it about the issue?",
                 ]),
                 closer="Rewrite it into one formal, objective sentence that keeps the same position and its "
                        "reason. Change only the register. Run the checks above before you submit.")),

        # ===== INDEPENDENT: cold edit on the taught topic + say-the-standard (Yeager) =====
        Slot("INDEPENDENT", "production_frq", "Fix the tone on your own",
             ref="", bank="four_day_week", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="revision",
             body=frq_prompt(
                 intro="On your own now, no frame. Rewrite this sentence in a formal, objective tone, keeping its "
                       "position: 'I feel like schools totally should keep five days, because honestly kids need "
                       "the class time to not fall behind.'",
                 closer="Cut the first person, the slang, and any reader-address, and state the point about the "
                        "issue with its reason intact. A formal, objective tone is what makes an essay read as an "
                        "argument and not a text message, and you are ready to do this without a frame. Run the "
                        "3-question check before you submit.")),

        # ===== TRANSFER: same move, a NEW topic (free transit), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "The topic: free public transit",
             ref="ACC-W910-FRAME-FREETRANSIT", bank="free_transit",
             body=("The next sentence to fix is about free public transit. Read this short orientation so the "
                   "topic is familiar. Again, you are fixing the tone of a provided sentence, keeping its "
                   "position, not writing from scratch.")),
        Slot("TRANSFER", "production_frq", "Fix the tone on a NEW topic",
             ref="", bank="free_transit", rubric_ref="rc.staar", scored=True, unit="sentence", frq_type="revision",
             body=frq_prompt(
                 intro="New topic. Rewrite this sentence in a formal, objective tone, keeping its position and "
                       "its reason: 'Honestly I think free transit would be awesome, because it would get a ton "
                       "more people onto the buses.'",
                 closer="Same tone move, new topic: cut the first person (I think), the hedge (Honestly), and the "
                        "slang (awesome, a ton), and state the point about the issue. Keep the reason (more "
                        "riders). Run the 3-question check before you submit.")),
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
