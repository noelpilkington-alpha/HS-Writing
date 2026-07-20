"""
lesson_g10_l15_evidence_pool.py  -  G10 KC C.10.06, ARCHETYPE 8: CROSS-SOURCE-SYNTHESIS (WEAVE, ceiling essay). V3.1.

G10 course L15 (Unit 4 Cross-text synthesis, intro), rebuilt to the v3.1 build spec (hand-authored).
Teaching point (KEPT): given a set of sources, map the evidence pool (Dd3): decide which sources are usable for
your point and what each one lets you say, instead of grabbing one and ignoring the rest. First WEAVE lesson.
SYNTHESIS-TIER binds the FULL opposing-pair sources (real 2-source sets): taught = congestion (full set) ->
transfer = daylight_saving (full set, partitioned). rc.staar, unit="multi_paragraph".

Preserved EXACTLY from the prior L15: id="ACC-W910-L-G10-C1006-0015", lesson_type=8, mnemonic_status="proposal",
kc="C.10.06", the unit, the bound stimuli (CONGESTION taught -> DST transfer), and every production_frq unit=
value (multi_paragraph). The unit ladder is non-decreasing and stays under the essay ceiling for the type.

V3.1 changes vs the prior L15 (the two failing gates + the spine polish):
  1. FIXED the leaked internal label: the discrimination no longer says "a Grade-C design bet we label as a
     bet"; it is a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}] (leaked_internal_label).
  2. FIXED the wall-of-text teach card: the prose block is now a ONE_IDEA callout + real <ul>/<ol> lists of
     the parts and the order of work (format_fidelity, and the v3.1 "parallel items as a list" rule).
  3. Deterministic frq_prompt/setapart/checklist bodies (no "Step 1/2" prose, no "Scored on ..." chrome);
     coping-model before/after kept with a literal BEFORE + AFTER; the check tool (the 3-question pool check)
     folded in at the point of first use as a real <ol> REMEMBER box.
Own words, faithful to the bound sources, no fabricated figures, no em dashes. Passes all 23 gates + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">When a task hands you a <strong>set of sources</strong>, '
'the first move is to <strong>map the pool</strong>: check every source and decide what each one lets you say, '
'before you write. You do not grab one source and ignore the rest.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: check the pool</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you plan, look at your pool map and ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Did I check every source in the set, not just one?</li>'
'<li style="margin:2px 0">For each source, did I name the claim it supports or the objection it raises?</li>'
'<li style="margin:2px 0">Did I name the objection I will answer?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you write.</div></div>')

# coping-model before/after: a writer maps the congestion set, catches that only one source was used, and
# rebuilds the map so each source gets a job. Contains BOTH a literal BEFORE and AFTER (content_depth). Facts
# trace to the bound source (FHWA/EPA on the pro side; BLS/Census on the con side); nothing fabricated.
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> grabs one source, ignores what the other offers</span>'
    '<p style="margin:8px 0 0;font-size:15px">First try: "The pro source says congestion pricing cuts traffic '
    'and emissions, so I will build the whole plan from that one source." The con source is never opened.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The writer runs the pool check and catches the gap: '
    'only one source was used, so the cost-to-drivers objection goes unnamed and unanswered.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> maps the pool: each source gets a job</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">SOURCE 1 (pro)</span> lets me say tolls on peak driving cut traffic and emissions and '
      'raise money for buses and trains (FHWA and EPA data). '
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">SOURCE 2 (con)</span> raises the objection I will answer: a flat toll hits low-income '
      'drivers hardest, and transportation is already a top household cost (BLS and Census data). Now I plan to '
      'draw on both.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same set, but now every source has a job. The pro '
    'source supplies the case, and the con source supplies the objection to answer. That is a mapped pool.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1006-0015", grade="9-10", lesson_type=8,
    unit="G10 U4 - Cross-text synthesis (map the evidence pool)",
    title="Map the Sources Before You Write",
    target=("Given a set of sources, decide which are usable and what each one lets you say (the evidence "
            "pool), instead of grabbing one and ignoring the rest. Written across a multi-source plan. Trait: "
            "Development (use of sources)."),
    acc_tags=["ACC.W.SRC.1", "CCSS.W.9-10.7", "CCSS.W.9-10.8"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.06", "sot": "icm course-G10.md L15",
                "taught_stimulus": "ACC-W910-ARG-OPP-LESSON-CONGESTION",
                "transfer_stimulus": "ACC-W910-ARG-OPP-LESSON-DST",
                "playbook": "_phase2/playbook_T8_WEAVE.md",
                "template": "v3.1 spine; SYNTHESIS-TIER binds full opposing-pair sources (2-source sets); UNTIMED.",
                "one_idea": "When a task hands you a set of sources, map the pool: decide what each one lets you say before you write.",
                "one_reminder": "Pool check: every source checked, not just one? claim/objection named per source? objection to answer named?",
                "version_note": ("V3.1 rebuild of L15. FIXED the two failing gates on the prior version: removed "
                                 "the leaked internal label ('a Grade-C design bet we label as a bet') from the "
                                 "discrimination and moved it to explicit choices=[]; broke the wall-of-text teach "
                                 "card into a ONE_IDEA callout + real <ul>/<ol> lists (format_fidelity). "
                                 "Deterministic frq_prompt/setapart/checklist bodies (no 'Step 1/2' prose, no "
                                 "'Scored on' chrome); coping-model before/after kept; the pool check folded in "
                                 "as a real <ol> REMEMBER box at first use. Preserved id, type 8, "
                                 "mnemonic_status=proposal, kc, unit, bound stimuli, and every production_frq "
                                 "unit= value (multi_paragraph); ladder non-decreasing, under the essay ceiling."),
                "review_provenance": "built to the L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["map-the-evidence-pool", "what-each-source-lets-you-say"],
    slots=[
        # ===== TEACH: the one idea + the parts (as a list), then the order of work (as a list) =====
        Slot("TEACH", "teach_card", "The one idea: a set of sources is a pool to map",
             body=(ONE_IDEA +
                   "A cross-text task hands you two or more sources on one question. Mapping the pool means "
                   "doing this for the set before you write:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Check every source</strong>, not just the first one you "
                   "agree with.</li>"
                   "<li style=\"margin:4px 0\"><strong>Give each source a job</strong>: name the claim it can "
                   "support, or the objection it raises against your position.</li>"
                   "<li style=\"margin:4px 0\"><strong>Expect a split in a pro-and-con set</strong>: one source "
                   "usually supplies the case FOR a position, and the other supplies the counterclaim you must "
                   "answer. A counterclaim is a reader's strongest objection to your position, the point you "
                   "have to answer.</li></ul>"
                   "The trap is grabbing one source and ignoring the rest, which wastes evidence and leaves the "
                   "other side unanswered.")),
        Slot("TEACH", "teach_card", "How to map the pool, step by step",
             body=("Here is the order of work. Follow it and you use the whole set instead of one piece of it:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>READ</strong> every source in the set.</li>"
                   "<li style=\"margin:4px 0\"><strong>LABEL</strong> each source: what claim can it support, or "
                   "what objection does it raise?</li>"
                   "<li style=\"margin:4px 0\"><strong>DECIDE</strong> which sources are usable for the point you "
                   "want to make.</li>"
                   "<li style=\"margin:4px 0\"><strong>PICK</strong> the objection you will answer.</li>"
                   "<li style=\"margin:4px 0\"><strong>THEN</strong> plan and write, drawing on the whole "
                   "pool.</li></ol>"
                   "You are deciding what each source lets you say, in this order, before you commit to a plan.")),
        Slot("TEACH", "stimulus_display", "Read the source set: congestion pricing (both sides)",
             ref="ACC-W910-ARG-OPP-LESSON-CONGESTION", bank="congestion_pricing",
             body=("Read this two-source set on congestion pricing, a pro source and a con source. Because your "
                   "job is to MAP the pool, read both and note what each one lets you say: which claim each "
                   "supports, and what objection the other raises. The texts stay on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model before/after + the pool check, then the check items =====
        Slot("MODEL", "annotated_before_after", "Watch a one-source grab become a mapped pool",
             bank="congestion_pricing",
             body=("Here is a writer mapping the congestion set. Read the BEFORE, then the AFTER, and notice each "
                   "source getting a job." + BEFORE_AFTER_HTML +
                   " The BEFORE uses only the pro source, so the objection goes unnamed. The AFTER labels what "
                   "each source lets you say, then plans to use both. Mapping the pool is the move." + REMEMBER +
                   "When you build your own map, run this check before you commit to a plan.")),
        Slot("MODEL", "discrimination", "Which writer mapped the pool?",
             ref="", labeled_grade_c=True, bank="congestion_pricing",
             body=("You have watched a one-source grab become a mapped pool. Now spot the target: which writer "
                   "used the whole POOL, and which did not? "
                   "(A) The writer opens only the pro source, builds the whole plan from its traffic-and-emissions "
                   "case, and never opens the con source to see what it might add or challenge.  "
                   "(B) The writer notes the pro source supports the traffic-and-transit case and the con source "
                   "raises the cost-to-drivers objection, then plans to draw on both.  "
                   "(C) The writer skims both sources and copies several long quotes from each, but never decides "
                   "what claim each source can support or what objection it raises.  "
                   "(D) The writer reads both sources and treats them as making the same case, filing the con "
                   "source under support alongside the pro source, so the objection it raises is never named. "
                   "Correct: B mapped the pool. It gives each source a job, so the objection is named and the "
                   "plan can use both. A grabs one source and leaves the objection unanswered; C reads both but "
                   "never decides what each one lets you say; D reads both but misses the pro-and-con split and "
                   "files the con source as more support, so the objection still goes unnamed."),
             choices=[
                 {"id": "A", "text": "The writer opens only the pro source, builds the whole plan from its traffic-and-emissions case, and never opens the con source to see what it might add or challenge.",
                  "correct": False,
                  "why": "This grabs one source. The con source is never opened, so the cost-to-drivers objection goes unnamed and unanswered."},
                 {"id": "B", "text": "The writer notes the pro source supports the traffic-and-transit case and the con source raises the cost-to-drivers objection, then plans to draw on both.",
                  "correct": True,
                  "why": "Correct. Each source gets a job: the pro source supplies the case, the con source supplies the objection to answer. That is a mapped pool."},
                 {"id": "C", "text": "The writer skims both sources and copies several long quotes from each, but never decides what claim each source can support or what objection it raises.",
                  "correct": False,
                  "why": "Reading both is not enough. Without deciding what each source lets you say, the pool is not mapped and the quotes have no job."},
                 {"id": "D", "text": "The writer reads both sources and treats them as making the same case, filing the con source under support alongside the pro source, so the objection it raises is never named.",
                  "correct": False,
                  "why": "This reads both but misses the pro-and-con split. Filing the con source as more support hides the objection it raises, so the pool is not mapped and the other side goes unanswered."},
             ]),
        Slot("MODEL", "predict_the_fix", "What does this cross-text plan most need?",
             bank="congestion_pricing",
             body=("Diagnose before the reveal. A student plans: 'I will use the con source to argue tolls are "
                   "unfair and just quote it a lot.' The pro source is never mentioned. Which single move would "
                   "most improve the plan? "
                   "(A) map both sources, noting what each one lets you say (the con source's objection and the "
                   "pro source's case to weigh against it)  "
                   "(B) keep working from the con source and pack in more of its quotes so the fairness objection "
                   "feels fully backed up  "
                   "(C) drop this question and pick a different topic where the con source by itself already makes "
                   "a clear enough argument  "
                   "(D) add several more sentences to the plan so it comes out longer and looks more developed, "
                   "without changing which sources it draws on"),
             feedback=("Correct: A. Using only the con source leaves the pro case unexamined, so the argument "
                       "cannot weigh both sides. The fix maps the whole pool: note that the con source raises the "
                       "fairness objection and the pro source offers the traffic-and-transit case, then plan to "
                       "use both. More con quotes (B), a new topic (C), or extra length (D) do not map the pool.")),

        # ===== SUPPORTED: map the pool with a fill-in frame (the highest-value scaffold) =====
        Slot("SUPPORTED", "production_frq", "Map what each source lets you say",
             ref="", bank="congestion_pricing", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="For the congestion-pricing set, map the pool before you plan a word of the essay.",
                 setapart_block=setapart("Fill in this pool map:",
                                         "Source 1 (pro) lets me say: ______. Source 2 (con) raises this objection I will answer: ______."),
                 closer="Name what each source lets you say, so you plan to draw on both, not one. Say the claim "
                        "the pro source supports and the objection the con source raises.")),
        # DIAGNOSIS = check-and-fix on a PROVIDED weak map (not a fresh production), scaffolded by a checklist
        # run on the weak map. Same taught source (load balance).
        Slot("MODEL", "diagnosis_frq", "Check a weak pool map before you plan",
             ref="", bank="congestion_pricing", scored=True,
             body=frq_prompt(
                 intro="First watch the check run on a weak pool map, then run it on your own.",
                 setapart_block=setapart("Weak map to fix:",
                                         "Use source 1 for the reasons tolls are good.", "red"),
                 checklist_block=checklist(title="Run the check:", rows=[
                     ("Did the writer check every source, not just one?", "No. Only source 1 is used. Add what source 2 lets you say."),
                     ("Is a claim or objection named for each source?", "No. Name the objection the con source raises."),
                     ("Is the objection to answer named?", "No. Name the objection you will answer."),
                 ]),
                 closer="Now write a fresh pool map for the congestion set that names what each source lets you "
                        "say, run the same three checks, and fix any that fail. Finish by naming the objection "
                        "you will answer.")),

        # ===== INDEPENDENT: map the pool cold (no frame) + say-the-standard =====
        Slot("INDEPENDENT", "production_frq", "Map the evidence pool on your own",
             ref="", bank="congestion_pricing", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="On your own now. For the congestion-pricing set, map the whole pool with no frame.",
                 closer="Write a pool map that names what EACH source lets you say (the claim the pro source "
                        "supports and the objection the con source raises), and name the objection you will "
                        "answer. Then run the pool check and fix any part that fails. Mapping the pool is what "
                        "every strong cross-text argument is built on, and you are ready to do it cold.")),

        # ===== TRANSFER: same map-the-pool move, a NEW set (daylight saving), partitioned from the taught bank =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source set: daylight saving (both sides)",
             ref="ACC-W910-ARG-OPP-LESSON-DST", bank="daylight_saving",
             body=("Read this new two-source set on daylight saving, a source for ending the twice-yearly switch "
                   "and one raising cautions. Because your job is to MAP the pool, read both and note what each "
                   "one lets you say. The texts stay on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Map the evidence pool on a NEW set",
             ref="", bank="daylight_saving", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="New set. The question: should the United States abolish daylight saving time and keep one clock year round?",
                 closer="For the daylight-saving sources, write a pool map that names what EACH source lets you "
                        "say (the case for ending the switch, and the caution the other source raises), and name "
                        "the objection you will answer. Same map-the-pool move as the congestion set, a new "
                        "topic. Run the pool check before you submit.")),
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
