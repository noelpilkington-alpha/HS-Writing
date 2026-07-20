"""
lesson_g9_l11_warrant_v3_1.py  -  G9 KC C.9.03, ARCHETYPE T3: EVIDENCE-INTEGRATION/REASONING (PROVE, sentence). V3.1.

V3.1 rebuild of lesson_g9_l11_warrant.py, applying the v3.1 lesson build spec (see icm/_config/
v3_1-lesson-build-spec.md), the same pattern G9 L01 cleared. Teaching point + KC + id + bound stimuli are
UNCHANGED: write a WARRANT, the reasoning sentence that states WHY the evidence supports the claim, matured
from a bare because to a causal subordinator (because/since/as) plus a real why-expansion. KC C.9.03.
Taught on COMMUNITYSERVICE (full source); transfer on PHONEBAN (full source, partitioned).

V3.1 changes vs the prior L11:
  1. TEACH is now ONE idea, hammered: a teal ONE-IDEA box + the minimum teaching as LISTS (causal-word +
     restate-vs-explain contrast), not a 165-word prose wall (the old teach_card tripped format_fidelity).
     "warrant" is still defined in plain words in a TEACH body (define-before-use), with the cue word "means".
  2. MODEL BEFORE THE QUIZ (KH worked-example effect): the discrimination check now follows the model instead
     of preceding it, so the student sees a warrant built before being asked to spot one.
  3. COPING-MODEL THINK-ALOUD (SRSD): the model is a written drafting process (claim+fact -> restate-trap ->
     revise to a real why), then the clean BEFORE/AFTER endpoints, then the reusable check tool. No named peer.
  4. STRUCTURED FRQ/DIAGNOSIS bodies (lesson_prompts.frq_prompt/setapart/checklist): the old diagnosis was a
     "Step 1, ... Step 2, ..." prose run that render-QC flagged as double-numbering; it is now a real checklist.
     No "Scored on ..." rubric-trait chrome in any student-facing prompt (the grader knows the trait from the id).
  5. CLEAN DISCRIMINATION: explicit choices=[{id,text,correct,why}]; the internal "Grade-C design bet" label is
     gone from the student text (kept only as labeled_grade_c=True in code); all three options carry a causal
     word, so "because" cannot co-vary with the key (DI faultless communication) - the invariant is explain-vs-restate.
  6. AUTONOMY + SAY-THE-STANDARD (Yeager) on the independent write.

ONE IDEA: a warrant says WHY the evidence supports the claim. ONE REMINDER: the 3-question warrant check.
Passes all 23 lesson_contract gates + render-QC. Own words, federal-sourced facts, no fabricated figures, no em dashes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A <strong>warrant</strong> is the sentence that says '
'<strong>WHY</strong> your evidence supports your claim. A claim and a fact sitting side by side, with no '
'warrant, is only half an argument.</div></div>')

# coping-model think-aloud panel: a WRITTEN drafting process (claim+fact -> restate-trap -> real why).
COPING_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fff7ed;padding:10px 14px;border-bottom:1px solid #fed7aa;color:#7c2d12;font-size:13px">'
    'A writer thinking it through, draft by draft:</div>'
  '<div style="padding:12px 14px;color:#1f2a44;font-size:14px;line-height:1.6">'
    '<p style="margin:0 0 8px"><strong>First try:</strong> "Schools should require service, and most high '
    'schools already run service programs." Check it: does this state WHY that fact supports requiring service? '
    'No. It puts the claim and the fact side by side and stops. That is claim-plus-fact, not a warrant.</p>'
    '<p style="margin:0 0 8px"><strong>Second try:</strong> "Schools should require service because it really '
    'should be required." There is a because now. But does it explain WHY, or just restate the claim? It '
    'restates it. Swap the restatement for a real reason.</p>'
    '<p style="margin:0"><strong>Final:</strong> "Schools should require service because most high schools '
    'already run service programs, so a requirement would just extend a workable opportunity to every student." '
    'Now the because carries a reason that links the fact to the claim. That passes.</p>'
  '</div>'
'</div>')

BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> claim + evidence, but no warrant</span>'
    '<p style="margin:8px 0 0;font-size:15px">Schools should require service. A federal survey found that most '
    'high schools already have students doing service.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The claim and the evidence are both here, but the '
    'writer never says WHY that fact supports requiring service. The reasoning is missing.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> a warrant sentence states WHY it supports the claim</span>'
    '<p style="margin:8px 0 0;font-size:15px">Schools should require service, and the fact that most high '
    'schools already run service programs supports this '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">WARRANT</span> because a requirement would simply extend to every student an '
      'opportunity that schools have already shown they can organize.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">The warrant connects "most schools already do this" '
    'to "so requiring it is workable." Reaching the why is the move.</p>'
  '</div>'
'</div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the 3 warrant questions</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit any warrant, run this quick test:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Is there a causal word (because, since, or as)?</li>'
'<li style="margin:2px 0">Does it explain WHY, or just restate the claim?</li>'
'<li style="margin:2px 0">Does it use a fact from the source?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, the reasoning is not a warrant yet.</div></div>')


LESSON = Lesson(
    id="ACC-W910-L-G9-C903-0011", grade="9-10", lesson_type=3,
    unit="G9 U2 - Reasoning (the warrant sentence)",
    title="Say Why the Evidence Supports Your Claim (the Warrant)",
    target=("Write a warrant: the reasoning sentence that states WHY your evidence supports your claim, using a "
            "because, since, or as clause plus a why-explanation. Written at the sentence. Trait: "
            "Evidence/Development (reasoning)."),
    acc_tags=["ACC.W.ARG.2", "CCSS.W.9-10.1b"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "established-caveat", "kc": "C.9.03", "sot": "icm course-G9.md L11",
                "taught_stimulus": "ACC-W910-ARG-LESSON-COMMUNITYSERVICE",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-PHONEBAN",
                "playbook": "_phase2/playbook_T3_PROVE.md",
                "template": "locked L01 template; EVIDENCE-TIER binds full sources.",
                "one_idea": "A warrant says WHY the evidence supports the claim.",
                "one_reminder": "3-question warrant check: causal word? explains (not restates)? source fact?",
                "version_note": ("V3.1: rebuilt to the v3.1 spec (pattern from G9 L01 v3.1). Teaching point, KC "
                                 "C.9.03, id, and bound stimuli unchanged. Split the teach into a ONE-IDEA box "
                                 "plus lists (fixed the 165-word wall of text); moved the discrimination AFTER "
                                 "the model (KH worked-example effect); added a coping-model think-aloud (SRSD); "
                                 "structured the FRQ/diagnosis bodies with frq_prompt/setapart/checklist (fixed "
                                 "the 'Step 1/2/3' double-numbering render-QC fail); dropped 'Scored on ...' "
                                 "chrome; clean discrimination with explicit choices and no leaked Grade-C label "
                                 "(all options carry a causal word so 'because' cannot cue the key); autonomy + "
                                 "say-the-standard on the independent write (Yeager)."),
                "council": ("T3/PROVE reasoning guided rung: the matured warrant (why-the-evidence-supports-the-"
                            "claim), written with causal subordinators + why-expansion, maturing W2. warrant-"
                            "present vs warrant-absent discrimination labeled Grade-C in code. Subordinator "
                            "mechanic app-owned + gated, taught by USE only."),
                "review_provenance": "v3.1 spec rebuild; 23 lesson_contract gates + gated_reading render-QC clean."},
    fade_ledger_moves=["warrant-state-the-why", "causal-subordinator-why-expansion"],
    slots=[
        # ===== TEACH: ONE idea only (ONE-IDEA box + lists; warrant defined with the cue word "means") =====
        Slot("TEACH", "teach_card", "The sentence that says WHY the evidence fits",
             body=(ONE_IDEA +
                   "A claim and a fact do not argue anything by themselves. The reader still asks: so what, why "
                   "does that fact prove your point? A <strong>warrant</strong> means the reasoning a reader "
                   "needs to accept that your fact really backs your claim. You build it two ways:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\">Start it with a causal word: <strong>because</strong>, "
                   "<strong>since</strong>, or <strong>as</strong>.</li>"
                   "<li style=\"margin:4px 0\">Then give a real reason that connects the fact to the claim, not "
                   "a restatement of the claim.</li></ul>"
                   "Two sentences can both use because, but only one reasons:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Restates (not a warrant)</strong>: 'Service should be "
                   "required because it should be required.' That says the same thing twice.</li>"
                   "<li style=\"margin:4px 0\"><strong>Explains (a real warrant)</strong>: 'Service should be "
                   "required because most schools already run service programs, so a rule would extend a "
                   "workable option to everyone.' That says WHY the fact supports the claim.</li></ul>"
                   "The trap is stopping at claim-plus-fact with no why. Today you write the warrant sentence "
                   "that explains why your evidence fits your claim.")),
        Slot("TEACH", "stimulus_display", "Read the source: required community service",
             ref="ACC-W910-ARG-LESSON-COMMUNITYSERVICE", bank="community_service",
             body=("Read this source about required community service. Your job is to explain WHY a fact "
                   "supports a claim, so read the whole thing and note one fact, then think about the reason it "
                   "backs a claim about requiring service. The text stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model think-aloud + clean before/after + the check tool. =====
        Slot("MODEL", "annotated_before_after", "Watch a writer build a warrant",
             bank="community_service",
             body=("Here is the skill in action. Follow the writer's thinking, then read the clean before and "
                   "after. " + COPING_HTML + BEFORE_AFTER_HTML +
                   " Notice the one move that turned the BEFORE into the AFTER: the writer stopped restating and "
                   "gave a reason that links the fact to the claim. " + REMEMBER +
                   "When you write your own, build it the same way: causal word, then a real why, using a fact "
                   "from the source, and run the 3 questions before you submit.")),
        Slot("MODEL", "discrimination", "Which sentence is a real warrant?",
             ref="", labeled_grade_c=True, bank="community_service",
             body=("Now that you have seen one built, spot the target. All four attach a causal word to the "
                   "same claim. Which one is a real warrant, the sentence that explains WHY "
                   "the evidence supports the claim? "
                   "(A) Schools should require service because a service requirement is exactly the sort of firm rule that a genuinely responsible school really ought to put in place.  "
                   "(B) Schools should require service because most high schools already run service programs, so a rule would extend that workable option to every student.  "
                   "(C) Schools should require service because a federal survey happened to find that most high schools already have some of their students taking part in service.  "
                   "(D) Schools should require service because helping other people is one of the most rewarding experiences a young person can have. "
                   "Correct: B. It uses the fact to explain WHY requiring service is workable. (A) uses because "
                   "but only restates the claim, so it explains nothing. (C) states the fact with because but "
                   "never says why that fact supports requiring it, so it stops at claim-plus-fact. (D) gives a "
                   "real reason, but it rests on a personal value, not on a fact from the source."),
             choices=[
                 {"id": "A", "text": "Schools should require service because a service requirement is exactly the sort of firm rule that a genuinely responsible school really ought to put in place.",
                  "correct": False,
                  "why": "This has because, but it only restates the claim ('require service because a requirement should be in place'). Restating the claim is not reasoning, so it is not a warrant."},
                 {"id": "B", "text": "Schools should require service because most high schools already run service programs, so a rule would extend that workable option to every student.",
                  "correct": True,
                  "why": "Correct. It uses the source fact to explain WHY requiring service is workable, so it is a real warrant, the reasoning a reader needs. The reason links the fact to the claim, not any single word."},
                 {"id": "C", "text": "Schools should require service because a federal survey happened to find that most high schools already have some of their students taking part in service.",
                  "correct": False,
                  "why": "This drops in the fact with because but never says why that fact supports requiring service. It stops at claim-plus-fact, so the warrant, the why, is still missing."},
                 {"id": "D", "text": "Schools should require service because helping other people is one of the most rewarding experiences a young person can have.",
                  "correct": False,
                  "why": "This explains a why, but the reason is a personal value with no fact from the source behind it, so it is not the reasoning that links the source's evidence to the claim."},
             ]),
        Slot("MODEL", "discrimination", "Which reason actually uses a source fact?",
             ref="", labeled_grade_c=True, bank="community_service",
             body=("Here is a different trap. Each sentence states the same claim and attaches a reason with a "
                   "causal word. Only one reasons from a real source fact to explain WHY the claim holds. Which "
                   "is the real warrant? "
                   "(A) A graduation requirement would change most schools, because it just feels like the bold sort of policy that shakes schools out of their routines.  "
                   "(B) A graduation requirement would change most schools, as a federal survey already found that a strong majority of high schools have at least some of their students regularly taking part in community service in one form or another.  "
                   "(C) A graduation requirement would change most schools, since fewer than half now build service into their coursework, so a rule would push the majority to do something new.  "
                   "(D) A graduation requirement would change most schools, since the source makes it very clear that this is exactly the kind of policy schools need right now. "
                   "Correct: C. It uses a source fact, the low share of high schools that build service into their "
                   "coursework, to explain WHY a requirement would change most of them. (A) attaches a causal word "
                   "to a feeling, not a fact, so there is nothing to reason from. (B) cites a real fact, but that "
                   "fact shows service is already common, which does not explain why a rule would change most "
                   "schools. (D) points at the source but pulls no actual fact from it, only a vague claim about what it shows."),
             choices=[
                 {"id": "A", "text": "A graduation requirement would change most schools, because it just feels like the bold sort of policy that shakes schools out of their routines.",
                  "correct": False,
                  "why": "This ties a causal word to a feeling, not to any fact from the source, so the reason has no evidence to work from."},
                 {"id": "B", "text": "A graduation requirement would change most schools, as a federal survey already found that a strong majority of high schools have at least some of their students regularly taking part in community service in one form or another.",
                  "correct": False,
                  "why": "This uses a real source fact, but that fact shows service is already common, which is the opposite of a reason it would change most schools."},
                 {"id": "C", "text": "A graduation requirement would change most schools, since fewer than half now build service into their coursework, so a rule would push the majority to do something new.",
                  "correct": True,
                  "why": "Correct. It reasons from a real source fact, the low share of schools that build service into their coursework, to explain why a requirement would change most of them."},
                 {"id": "D", "text": "A graduation requirement would change most schools, since the source makes it very clear that this is exactly the kind of policy schools need right now.",
                  "correct": False,
                  "why": "This name-drops the source but never pulls an actual fact from it, so there is no real evidence in the reason, only a vague claim about what the source shows."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this claim-plus-evidence most need?",
             bank="community_service",
             body=("Diagnose this draft before the reveal. A student wrote: 'Schools should require service. "
                   "Most high schools already have students doing service.' Which single move would most "
                   "improve the reasoning? "
                   "(A) add a warrant that explains why that fact supports requiring service  "
                   "(B) add a second fact about how many students volunteer at their own schools before they graduate  "
                   "(C) restate the claim more forcefully so that it sounds a great deal more convincing to the reader  "
                   "(D) describe exactly how a typical school service program is set up and then run"),
             feedback=("Correct: A. The claim and evidence are both present, but the writer never explains why "
                       "'most schools already do this' supports requiring it. The fix is a warrant: 'because a "
                       "requirement would simply extend to every student an opportunity schools already run "
                       "well.' A second fact (B), a stronger restatement (C), or a description of the program "
                       "(D) never supply the missing reasoning.")),

        # ===== SUPPORTED: framed write (fill-in frame) on the taught topic (source read at TEACH step) =====
        Slot("SUPPORTED", "production_frq", "Write the warrant: explain why the evidence fits",
             ref="", bank="community_service", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="Use the frame below so you can focus on the reasoning.",
                 setapart_block=setapart("Copy this frame, then fill in the blanks:",
                                         "Schools should require service because ______ [a fact from the source] so ______ [explain WHY that fact supports requiring service]."),
                 closer="Use because, since, or as, then give a real reason, do not just restate the claim. "
                        "Write one warrant sentence, then check it against the 3 questions.")),
        # DIAGNOSIS = check-and-fix on a PROVIDED weak draft (self-contained, no look-back at prior work).
        Slot("MODEL", "diagnosis_frq", "Check and fix a weak warrant with the 3 questions",
             ref="", bank="community_service", scored=True,
             body=frq_prompt(
                 intro="Run the 3-question warrant check on this weak draft, then rewrite it into a real warrant.",
                 setapart_block=setapart("Weak draft to fix:", "Service should be required because requiring it is a good idea.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Is there a causal word (because, since, as)?", "Yes, because. That part is fine."),
                     ("Does it explain WHY, or just restate the claim?", "It restates ('required because it is a good idea'). Replace that with a real reason."),
                     ("Does it use a fact from the source?", "No. Add one, such as the share of high schools already running service programs."),
                 ]),
                 closer="Now write one fresh warrant sentence for a claim about requiring service that passes "
                        "all three, then name which check the weak draft failed hardest.")),

        # ===== INDEPENDENT: cold write on the taught topic, no frame + autonomy + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Write a warrant on your own",
             ref="", bank="community_service", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="On your own now, no frame. Take whichever side on the service requirement you actually "
                       "hold.",
                 closer="State the claim, then use because, since, or as to explain WHY a fact from the source "
                        "supports it. This move, saying why your evidence fits, is what turns a claim and a fact "
                        "into a real argument, and you are ready to do it cold. Check your sentence against the "
                        "3 questions before you submit.")),

        # ===== TRANSFER: same move, a NEW topic (phones), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: phones in school",
             ref="ACC-W910-ARG-LESSON-PHONEBAN", bank="phone_ban",
             body=("A new debate now, so you reason from fresh evidence instead of reusing the last one. Read "
                   "this source about phones in school and note one fact, then think about the reason it backs a "
                   "claim about phones. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Write a warrant on a NEW topic",
             ref="", bank="phone_ban", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=frq_prompt(
                 intro="New topic. Write one warrant for a claim about phones in school.",
                 closer="State the claim, then use because, since, or as to explain WHY a fact from the source "
                        "supports it. Same move as the service warrant, a fresh topic. Check it against the 3 "
                        "questions before you submit.")),
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
