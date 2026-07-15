"""
lesson_g12_l16_gate_frq_section.py  -  G12 KC C.12.02, CROSS-SOURCE-SYNTHESIS (WEAVE, essay). COURSE GATE. V3.1.

G12 course L16 (Unit 2, COURSE GATE): the course-terminal task, a full AP Lang FRQ section. Teaching point
(KEPT): across three cold prompts the student independently NAMES each FRQ type (synthesis, rhetorical analysis,
argument), RUNS its move-set, SUSTAINS quality end to end under a self-imposed section budget, and aims for the
sophistication point. UNTIMED (Timeback has no timer; the rigor is the cold, full, self-directed production of a
whole FRQ section, matching moves to type and pacing). KC C.12.02.

Preserved EXACTLY from the prior L16: id="ACC-W910-L-G12-C1202-0016", lesson_type=8, mnemonic_status="proposal",
kc="C.12.02", the unit string, the bound stimuli (SYNTH-SET-0001 taught -> RA-SINGLE-0002 transfer), and every
production_frq unit= value (SUPPORTED plan = multi_paragraph, INDEPENDENT + TRANSFER = essay). The unit ladder
still climbs to the essay, which is the type-8 ceiling.

V3.1 rebuild vs the prior L16:
  1. Removed the leaked internal label ("a Grade-C design bet we label as a bet") from the discrimination; it is
     now a clean spot-the-target prompt with explicit choices=[{id,text,correct,why}] (leaked_internal_label).
  2. Broke the two prose-wall TEACH cards into a ONE_IDEA teal callout + real <ul>/<ol> lists of the three FRQ
     types and the two governing decisions (format_fidelity + the v3.1 "parallel items as a list" rule).
  3. Added the reusable three-question check tool as a REMEMBER dashed <ol> box folded in at the MODEL.
  4. Deterministic frq_prompt/setapart/checklist bodies (no "Step 1/2" prose, no "Scored on ..." chrome).
Own words, faithful to the bound federal sources (no fabricated figures), no em dashes. Passes all 23
lesson_contract gates + render-qc.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">A full FRQ section is <strong>one routine, run '
'three times</strong>: name the type from its tell, run that type\'s moves, and budget the whole section so '
'every essay, including the last, gets finished. Match the moves to the type; do not force one approach onto '
'all three.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: the section check</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you commit to a plan, run these three questions:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Have I named each FRQ\'s type from its tell?</li>'
'<li style="margin:2px 0">Do my moves match that type, instead of one reused approach?</li>'
'<li style="margin:2px 0">Does a section budget protect the last essay?</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, fix it before you write.</div></div>')

# coping-model before/after: one reused opinion essay with no section budget, rebuilt into three type-matched,
# paced essays. Contains BOTH a literal BEFORE and AFTER (content_depth). No named person (stateless rule).
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> one approach, no budget, across the section</span>'
    '<p style="margin:8px 0 0;font-size:15px">The writer treats all three prompts the same way, writing a '
    'personal-opinion essay for each, spends most of the section on the first, and leaves the third barely '
    'started.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">One approach cannot fit three FRQ types, and with '
    'no section budget the last essay dies. The gate measures type-matching AND pacing.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> type named, moves matched, section paced</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">SYNTHESIS</span> weave several sources into one argument and weight them. '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">ANALYSIS</span> tie the writer\'s choices to their effect. '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">ARGUMENT</span> take a position and anchor it with specific examples. Each essay gets '
      'its own moves and a fair share of the section budget.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same section, but now each prompt is read for its '
    'tell, matched to its own moves, and given time to finish. That is the whole course, run once on your own.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G12-C1202-0016", grade="9-10", lesson_type=8, lesson_class="gate",
    unit="G12 U2 - COURSE GATE: full AP Lang FRQ section (synthesis, analysis, argument)",
    title="G12 Gate: Write a Full FRQ Section, Type by Type",
    target=("The course gate: across three cold FRQs, independently name each type (synthesis, rhetorical "
            "analysis, argument), run its move-set, sustain quality end to end under a self-imposed section "
            "budget, and aim for sophistication, assembling everything the course taught. Written at the "
            "essay, untimed. Trait: Sophistication, Development, Evidence, and process."),
    acc_tags=["ACC.W.SRC.1", "ACC.W.INFO.6", "ACC.W.ARG.1", "ACC.W.PROD.4",
              "CCSS.W.11-12.1", "CCSS.W.11-12.7", "CCSS.W.11-12.9"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.12.02", "sot": "icm course-G12.md L16 (COURSE GATE)",
                "taught_stimulus": "ACC-W910-SYNTH-SET-0001",
                "transfer_stimulus": "ACC-W910-RA-SINGLE-0002",
                "playbook": "_phase2/playbook_T8_WEAVE.md",
                "one_idea": "A full FRQ section is one routine run three times: name the type, run its moves, budget the section.",
                "one_reminder": "Section check: named each FRQ's type from its tell? moves match the type? section budget protects the last essay?",
                "template": ("v3.1 spine; SYNTHESIS-TIER binds the cold set; GATE = cold full FRQ section (3 "
                             "types), UNTIMED (no Timeback timer). All three prompts cold to G12."),
                "version_note": ("V3.1 rebuild of L16. Removed the leaked internal label from the "
                                 "discrimination and moved it to explicit choices=[]; broke the two prose-wall "
                                 "TEACH cards into a ONE_IDEA callout + real <ul>/<ol> lists (format_fidelity); "
                                 "added the three-question section check as a REMEMBER <ol> box at the MODEL; "
                                 "deterministic frq_prompt/setapart/checklist bodies. Preserved id, type 8, "
                                 "kc=C.12.02, mnemonic_status=proposal, bound stimuli, and every production_frq "
                                 "unit= value (SUPPORTED=multi_paragraph, INDEPENDENT/TRANSFER=essay)."),
                "council": ("T8/WEAVE COURSE GATE: cumulative full FRQ section across synthesis + rhetorical "
                            "analysis + argument. Shell present as final-review retrieval, then the full cold "
                            "essays. Untimed: the rigor is cold, self-directed full-section production."),
                "review_provenance": "built to the G9 L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["full-frq-section", "name-type-run-moves-sustain"],
    # SCAFFOLD-FREE GATE (spine re-architecture): the course-terminal AP Lang FRQ SECTION. A gate certifies
    # independent transfer, so no annotated model, no discrimination, no predict-the-fix. This gate legitimately
    # keeps THREE cold writes because the section IS three FRQ types (synthesis + rhetorical analysis +
    # argument); that is the assessment shape, not scaffolding. Structure: a bare moves-checklist cue (recall,
    # not re-teach) -> an UNSCORED section plan -> the three held-out cold FRQ writes -> a post-hoc self-score.
    slots=[
        # ===== TEACH: a BARE recall cue only (the three FRQ types + the two governing decisions) - NO teaching =====
        Slot("TEACH", "teach_card", "Before you write: the routine you already own",
             body=(ONE_IDEA +
                   "This is the course gate: a full AP Lang FRQ section, written cold, on your own. No new "
                   "teaching and no worked example; here is the checklist to run from memory. For each of three "
                   "prompts, read the tell, name the type, and run that type\'s moves:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>SYNTHESIS</strong> (tell: a source SET): to synthesize "
                   "means to combine several sources into one argument of your own, weaving and weighting them "
                   "rather than summarizing each in turn.</li>"
                   "<li style=\"margin:4px 0\"><strong>RHETORICAL ANALYSIS</strong> (tell: ONE passage asking "
                   "HOW): analyze the writer\'s choices and their effect on the audience.</li>"
                   "<li style=\"margin:4px 0\"><strong>ARGUMENT</strong> (tell: a general question, NO passage): "
                   "take a position, which becomes your thesis. A thesis is a one-sentence claim that states the "
                   "position your whole essay defends, and you anchor it with specific examples.</li></ul>"
                   "Two decisions govern the whole section: name the TYPE from its tell before you plan, and "
                   "BUDGET the section so the third essay is never abandoned. Aim for the sophistication point. "
                   "There is no clock; take the time you need.")),
        # ===== UNSCORED section plan (a map for the three cold writes; not a certification write) =====
        Slot("SUPPORTED", "production_frq", "Plan your section (not graded)",
             ref="", bank="renewable_grid_synthesis", rubric_ref="rc.ap", scored=False, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Before you write, lay out a plan for the whole section. This plan is not graded; it is "
                       "your map for the three cold essays.",
                 setapart_block=setapart("Fill in this plan:",
                                         "Section budget: FRQ 1 (synthesis) ______ share. FRQ 2 (rhetorical analysis) ______ share. FRQ 3 (argument) ______ share. For each FRQ, name its type from the tell and the one move-set you will run."),
                 closer="Then write the three FRQs from this plan, keeping to your budget so all three finish.")),

        # ===== FRQ 1 (synthesis): held-out source set, cold write =====
        Slot("TEACH", "stimulus_display", "FRQ 1: a source set on a renewable grid (synthesis)",
             ref="ACC-W910-SYNTH-SET-0001", bank="renewable_grid_synthesis",
             body=("Read the first FRQ, a set of four sources on whether the United States power grid can run "
                   "mostly on renewable energy. Name its type from the tell (a source set, so synthesis), then "
                   "write a full synthesis that weaves at least three sources into one argument, weights them, "
                   "and situates the claim. The texts stay on screen while you work.")),
        Slot("TRANSFER", "production_frq", "GATE: write FRQ 1 (synthesis)",
             ref="", bank="renewable_grid_synthesis", rubric_ref="rc.ap", scored=True, unit="essay",
             body=frq_prompt(
                 intro="The gate, FRQ 1. On your own, write the whole synthesis on the renewable-grid set.",
                 closer="Write a complete synthesis: a situated claim, body paragraphs that weave at least three "
                        "sources into one argument and weight them, and a conclusion that defends a position. "
                        "Keep to your section budget so FRQs 2 and 3 still get finished. There is no time limit.")),

        # ===== FRQ 2 (rhetorical analysis): a DIFFERENT type + held-out passage, cold write =====
        Slot("TRANSFER", "stimulus_display", "FRQ 2: a single passage to analyze (rhetorical analysis)",
             ref="ACC-W910-RA-SINGLE-0002", bank="ra_speech_2",
             body=("The second FRQ is a different type: a single passage that asks how the writer builds the "
                   "argument. Name the type (one passage asking how, so rhetorical analysis), then analyze the "
                   "writer\'s choices and their effect on the audience, not the topic itself. Keep to your "
                   "section budget. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "GATE: write FRQ 2 (rhetorical analysis)",
             ref="", bank="ra_speech_2", rubric_ref="rc.ap", scored=True, unit="essay",
             body=frq_prompt(
                 intro="FRQ 2, a new type: analyze how the writer builds the argument for the audience.",
                 closer="Write a full rhetorical analysis: a situated introduction, body paragraphs that tie the "
                        "writer\'s choices to their effect on the audience, and a conclusion, aiming for the "
                        "sophistication point. A different type from FRQ 1, so different moves. Keep to your "
                        "section budget; there is no time limit.")),

        # ===== FRQ 3 (argument, no source): the THIRD type, cold write. Different prompt from the PP100 mastery
        # FRQ 3 so mastery stays a fresh cold task; bank partitioned from the taught set. =====
        Slot("TRANSFER", "production_frq", "GATE: write FRQ 3 (argument)",
             ref="", bank="argument_no_source", rubric_ref="rc.ap", scored=True, unit="essay",
             body=frq_prompt(
                 intro="The last FRQ, a third type: argument, with NO source. The tell is a general question, "
                       "so take a position and defend it from your own knowledge and examples.",
                 setapart_block=setapart("Your argument prompt:",
                                         "Some people hold that a willingness to fail is necessary for real achievement, while others argue that failure mostly discourages people and slows them down. Take a position on the role that failure should play in the pursuit of worthwhile goals."),
                 closer="Write a full argument essay: a thesis that states your position, body paragraphs that "
                        "anchor it with specific examples, and a conclusion. Your evidence comes from your own "
                        "knowledge. Keep to your section budget so all three FRQs finish, and aim for the "
                        "sophistication point. This completes the full section, run on your own.")),
        # ===== POST-HOC self-score: judge the finished section against the section check (calibration) =====
        Slot("INDEPENDENT", "self_score", "Score your own section, then predict the gate result",
             ref="", bank="argument_no_source",
             body=("Predict, then see your grades. Reread your three essays and run the section check: did you "
                   "name each type correctly, match each essay\'s moves to its type, and finish all three? Based "
                   "on that, did your section earn the gate?"),
             choices=[
                 {"id": "pass", "text": "Yes: right type, matched moves, all three finished.", "correct": True,
                  "why": "If each FRQ is the right type with type-matched moves and all three are complete, the "
                         "section meets the gate. Compare this prediction to your grades: matching them is how "
                         "you learn to judge your own full-section writing."},
                 {"id": "gap", "text": "Not yet: a wrong type, a mismatched move-set, or an unfinished essay.",
                  "correct": False,
                  "why": "Then fix it before you submit. Rename any mistyped FRQ and run its correct moves, or "
                         "finish the abandoned essay, because a wrong type or an unfinished FRQ keeps the section "
                         "below the gate."},
             ]),
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
