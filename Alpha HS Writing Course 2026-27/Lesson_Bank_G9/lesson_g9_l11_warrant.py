"""
lesson_g9_l11_warrant.py  -  G9 KC C.9.03, ARCHETYPE T3: EVIDENCE-INTEGRATION/REASONING (PROVE, paragraph).

G9 course L11. Guided rung: the matured warrant (W1) - a reasoning sentence that states WHY the evidence
supports the claim, written with a causal subordinator (because/since/as) plus a why-expansion. Recycles W2.
Locked L01 template; EVIDENCE-TIER binds full sources. Taught: COMMUNITYSERVICE (full) -> transfer: PHONEBAN
(full, partitioned). rc.staar, unit="sentence". "warrant" is a gated tech term (defined in TEACH). The
subordinator mechanic is app-owned + gated; taught by USE (the reasoning job) only. PROVE=established-caveat;
no coping-model persona; no source markup; no prior-work ref; no em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report

BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> claim + evidence, but no warrant</span>'
    '<p style="margin:8px 0 0;font-size:15px">Schools should require service. The National Center for '
    'Education Statistics reports that most high schools already have students doing service.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The claim and the evidence are here, but the '
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
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">The warrant is the sentence that explains WHY: it '
    'connects "most schools already do this" to "so requiring it is workable." Reaching the why is the move.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C903-0011", grade="9-10", lesson_type=3,
    unit="G9 U2 - Reasoning (the warrant sentence)",
    title="Say Why the Evidence Supports Your Claim (the Warrant)",
    target=("Write a warrant: the reasoning sentence that states WHY your evidence supports your claim, using a "
            "because, since, or as clause plus a why-explanation. Written at the sentence. Trait: "
            "Evidence/Development (reasoning)."),
    acc_tags=["ACC.W.ARG.2", "CCSS.W.9-10.1b"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12",
                "mnemonic_status": "established-caveat", "kc": "C.9.03", "sot": "icm course-G9.md L11",
                "taught_stimulus": "ACC-W910-ARG-LESSON-COMMUNITYSERVICE",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-PHONEBAN",
                "playbook": "_phase2/playbook_T3_PROVE.md",
                "template": "locked L01 template; EVIDENCE-TIER binds full sources.",
                "council": ("T3/PROVE reasoning guided rung: introduces W1 the matured warrant (why-the-"
                            "evidence-supports-the-claim), written with causal subordinators + why-expansion, "
                            "maturing W2. warrant-present vs warrant-absent discrimination labeled Grade-C. "
                            "Subordinator mechanic app-owned + gated, taught by USE only.")},
    fade_ledger_moves=["warrant-state-the-why", "causal-subordinator-why-expansion"],
    slots=[
        Slot("TEACH", "teach_card", "The sentence that explains WHY the evidence fits",
             body=("You can link a fact to a claim with because. Now make that link do real work. A warrant "
                   "means the reasoning sentence that states WHY your evidence supports your claim, the "
                   "explanation a reader needs to accept the connection. A claim plus a fact is not enough; the "
                   "warrant is what turns them into an argument. You write it with a causal word, because, "
                   "since, or as, followed by a real explanation, not just a restatement. Weak: 'Service should "
                   "be required because it is required.' That restates, it does not explain. Strong: 'Service "
                   "should be required because most schools already run service programs, so a requirement "
                   "would extend a workable opportunity to every student.' That says WHY the fact supports the "
                   "claim. The causal word is a sentence skill you already own; here we use it to carry "
                   "reasoning. The trap is stopping at claim-plus-evidence with no why. Goal today: write the "
                   "warrant sentence that explains why your evidence fits your claim.")),
        Slot("TEACH", "stimulus_display", "Read the source: required community service",
             ref="ACC-W910-ARG-LESSON-COMMUNITYSERVICE", bank="community_service",
             body=("Read this source about required community service. Because your job is to explain WHY a "
                   "fact supports a claim, read the whole thing and pick one fact, then think about the reason "
                   "it backs a claim about requiring service. The text stays on screen while you work.")),
        Slot("TEACH", "discrimination", "Which sentence is a real warrant?",
             ref="", labeled_grade_c=True, bank="community_service",
             body=("Sort these before you write (spotting the target before producing it, a Grade-C design bet "
                   "we label as a bet, not a proven ingredient). Both attach a because to the same claim and "
                   "fact. Which one is a real WARRANT, explaining WHY the evidence supports the claim? "
                   "(A) Schools should require service because doing service is something students really should be required to do, which shows a service requirement is a rule schools should have.  "
                   "(B) Schools should require service because most high schools already run service programs, "
                   "which shows a requirement would extend a workable opportunity to every student. "
                   "Correct: B. (A) uses because but only restates the claim ('required because it should be "
                   "required'), so it explains nothing. (B) uses the fact to explain WHY requiring service is "
                   "workable, so it is a real warrant, the reasoning a reader needs.")),
        Slot("MODEL", "annotated_before_after", "Watch a warrant get added to claim-plus-evidence",
             bank="community_service",
             body=("Here is a claim-plus-evidence pair getting a warrant added. Read the BEFORE, then the "
                   "AFTER, and notice the sentence that explains WHY the fact supports the claim."
                   + BEFORE_AFTER_HTML +
                   " The BEFORE stops at claim and evidence. The AFTER adds the warrant, the because-explanation "
                   "of why the fact backs the claim. Reaching the why is the move.")),
        Slot("MODEL", "predict_the_fix", "What does this claim-plus-evidence most need?",
             bank="community_service",
             body=("Diagnose this draft before the reveal. A student wrote: 'Schools should require service. "
                   "Most high schools already have students doing service.' Which single move would most "
                   "improve the reasoning? "
                   "(A) add a warrant sentence that explains WHY that fact supports requiring service  "
                   "(B) add a second fact about how many students already volunteer at their own schools  "
                   "(C) restate the claim more forcefully so it sounds more convincing to readers  "
                   "(D) name a specific school so that the single fact sounds more concrete and real"),
             feedback=("Correct: A. The claim and evidence are both present, but the writer never explains why "
                       "'most schools already do this' supports requiring it. The fix is a warrant: 'because a "
                       "requirement would simply extend to every student an opportunity schools already run "
                       "well.' A second fact (B), a stronger restatement (C), or a school name (D) do not "
                       "supply the missing reasoning.")),
        Slot("SUPPORTED", "production_frq", "Write the warrant: explain why the evidence fits",
             ref="", bank="community_service", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("Use this frame for a claim about requiring service: '______ [claim], because ______ [a "
                   "fact from the source] ______ [explain WHY that fact supports the claim].' Goal: use "
                   "because, since, or as, then explain the reason, do not just restate the claim. Write one "
                   "warrant sentence. Scored on Evidence/Development.")),
        Slot("MODEL", "diagnosis_frq", "Check your warrant: does it explain the why?",
             ref="", bank="community_service", scored=True,
             body=("First watch the check run on a weak draft, then run it on a fresh sentence of your own. "
                   "Weak draft: 'Service should be required because requiring it is a good idea.' Run the check "
                   "step by step. Step 1, causal word present? Yes, because. Step 2, does it explain WHY, or "
                   "just restate? It restates ('required because it is a good idea'), so replace the restatement "
                   "with a real reason. Step 3, is a source fact used? No, add one. Now you: write one fresh "
                   "warrant sentence for a claim about requiring service, then run the same checks. For each "
                   "No, use the fix: after because, give a real reason (not a restatement); use a fact from the "
                   "source. Finish by naming which check your sentence still needs most.")),
        Slot("INDEPENDENT", "production_frq", "Write a warrant on your own",
             ref="", bank="community_service", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("On your own now. Write one warrant sentence for a claim about required community service: "
                   "state the claim, then use because, since, or as to explain WHY a fact from the source "
                   "supports it. Before you submit, check your sentence: is there a causal word, does it "
                   "explain the why (not just restate), is a source fact used? If any answer is no, fix it "
                   "before you submit. Scored on Evidence/Development.")),
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: phones in school",
             ref="ACC-W910-ARG-LESSON-PHONEBAN", bank="phone_ban",
             body=("Read this new source about phones in school. Because your job is to explain WHY a fact "
                   "supports a claim, read the whole thing and pick one fact, then think about the reason it "
                   "backs a claim about phones. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Write a warrant on a NEW topic",
             ref="", bank="phone_ban", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("New topic. Write one warrant sentence for a claim about phones in school: state the claim, "
                   "then use because, since, or as to explain WHY a fact from the source supports it. Same move "
                   "as the service warrant, new topic. Do not just restate the claim. Scored on "
                   "Evidence/Development.")),
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
