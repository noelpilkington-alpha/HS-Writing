# Sim-Student Audit — Finding Ledger (G9–G12)

**Date:** 2026-07-17
**Inputs:** 5 simulated-student walk reports (`pipeline/sim_student_eval/out/{g9_pilot_v3,g10_run,g11_run,g12_run,crossgrade}/SIM_STUDENT_EVAL_*.md`).
**Method:** triage protocol — classify each finding by the artifact its claim is about → verify against **that** artifact (production `gated_reading.build_lesson_html` for rendering claims; lesson source for content claims) → on machine-vs-agent disagreement, find the mechanism before assigning a verdict → route survivors to a fix-plan item. Nothing is bulk-adopted.

## Calibration facts that govern every verdict
1. **One model ran (Fable-5), two personas.** Nothing is cross-*model* corroborated. "Cross-persona" still shares Fable's ~3.3:1 over-flag bias.
2. **Both personas are high-retention.** "Nothing new / too easy" is partly a persona artifact; redundancy findings must be weighed against a *weaker* learner's needs.
3. **The audit lens diverged from production** (Class A, now fixed). Any "blank / cut-off / can't-answer" flag was confounded until that fix; rendering-class claims are verified against the production push, not the audit renderer.

## The epistemic correction that motivated this ledger
Last session I marked the "blank MC steps" finding **FALSE** and said discard. That verdict was **wrong**. I had verified against the QTI push path while the agent was walking `render_student_experience`; the two renderers diverge on exactly the flagged slots. **The students were right; my check measured the wrong artifact.** This ledger's "artifact verified" column exists so that class of error is visible on its face.

---

## The 7 finding classes (≈400 raw instance-flags collapse to these)

| Class | What it is | Verdict | Disposition |
|---|---|---|---|
| **A** | Rendering/harness artifacts (blank MC options) | **REAL bug, audit-lens only** — FIXED | Harness fixed + regression test; no course change |
| **B** | Answer leakage (7 sub-patterns) | **Partly confirmed deterministically; rest → adversarial** | New fix-plan item **F7** |
| **C** | Redundancy (relabel / triple-test / cross-grade / source-exhaustion) | **Real signal, persona-weighted** | Folds into **F3** + new **F8** |
| **D** | Sequencing / difficulty inversion | **Checkable; several confirmed** | New fix-plan item **F9** |
| **E** | Broken feedback loops (SUBMIT→grader that doesn't exist) | **CONFIRMED** | Corroborates existing **F1** |
| **F** | Content contradictions / gaps | **Item-by-item (below)** | Route per item |
| **G** | Unresolved conceptual questions ("no one to ask") | **Real, low-severity, persona-specific** | New fix-plan item **F10** (copy/tooltip) |

---

## Verified findings (deterministic checks run this session)

### Class A — RESOLVED
| Finding | Artifact verified | Verdict | Evidence |
|---|---|---|---|
| Blank MC options: g9 l02s6/l03s6/l04s5/l08s5, g11 l11s5, g12 l02s5 | both `render_student_experience` AND `build_lesson_html` | **REAL (lens only), FIXED** | 8 slots carry options only in `choices[]`; student-view rendered 0, pushed QTI renders 6 `qti-simple-choice` (=3 opts). Fixed in `lesson_review.py`; test `test_student_view_options.py`; full sweep now 0/129 broken. |

### Class B — Answer leakage
| Finding | Artifact verified | Verdict | Evidence |
|---|---|---|---|
| **B1 Recognition-not-application: correct MC option = a prior worked-example AFTER, verbatim** | lesson source (option text vs AFTER text, `SequenceMatcher`) | **CONFIRMED — 12 instances ≥0.70** | g9: C901-0001 s4 (.72), C902-0007 s4 (.93), C902-0009 s4 (.86), C906-0027 s4 (.78); g10: C1001-0001 s4 (.75), C1002-0008 s4 (.91); g11: C1101-0001 s5 (.85), C1101-0002 s4 (.84), C1101-0003 s4 (.85); g12: C1201-0001 s4 (.86), C1201-0002 s4 (.76), D1201-0015 s4 (.87). Spot-verified C902-0007: S3 AFTER *is* the S4 answer, verbatim. |
| **B2 Write task sits on the same source as its worked example** | lesson source (slot adjacency) | **INDETERMINATE — 281 heuristic hits** | Cannot deterministically separate the *defect* (example pre-writes the exact answer) from *intended SRSD guided practice* (write on the source just studied). → adversarial verify, NOT counted as 281 defects. |
| **B3 "Checks that run themselves"** (diagnosis prompt answers its own check) | lesson source | **INDETERMINATE — 67/94 diagnosis_frq self-answer** | Of 67, my `own_turn` regex split 34 coping-model / 33 give-away, but manual read shows most "give-away" are the sanctioned coping-model ("run the check on this *provided weak draft*, then rewrite"). Deterministic scan **cannot** separate the two. → adversarial verify. |

### Class E — Broken feedback loops (corroborates F1)
| Finding | Artifact verified | Verdict | Evidence |
|---|---|---|---|
| **Calibration lessons instruct SUBMIT→grader→compare, but no grader exists on the platform** | lesson source | **CONFIRMED** | g11 C1103-0015 ("SUBMIT: send the synthesis to the grader"; s8 "before the grader does"), g12 C1201-0007 ("SUBMIT: send the essay to the grader"), g12 C1202-0014 ("the grader returns them"). Independent student corroboration of the F1 self_score fiction. |

### Class F — Content contradictions / gaps
| Finding | Artifact verified | Verdict | Evidence |
|---|---|---|---|
| **F-a Counterclaim required by g9 l27 gate, never taught in G9** | all G9 lesson bodies + l27 gate + G9 mastery | **CONFIRMED — high severity; cross-audit corroborated** | "counterclaim" appears only in l27 (0× in l01–l26). l27 requires it in the task line, one-reminder, checklist, sentence frame, AND the PP100 pass criteria. Matches earlier readiness finding C904-0029. G10 opens with counterclaim (one grade too late). |
| **F-b G10 l02 checklist weakened q3 on the student's weakest skill** | l01 vs l02 checklists | **CONFIRMED** | l01 q3 = "Does the reason answer that objection, not just repeat your side?"; l02 q3 = "Is there a reason for the side you hold?" Standard genuinely lowered. |
| **F-c G12 l06 under-teaches synthesize/weight ("one sentence each")** | l06 slot order + teach word-counts | **REFUTED (overstated)** | weight/synthesis taught in s1, s2, and s4 (326 words, weight×5 synth×6) — all *before* the s8 composition. Thin-teaching *perception* by the average persona, not a content gap. No fix. |
| **F-d "Summarize" defined (g9 l05) but never practiced** | all G9 write prompts | **CONFIRMED — low severity** | No production_frq asks the student to summarize; 3 grades later warn "don't summarize." |
| **F-e g9 l13 Step 8 forces sequence signposts where the real relation is cause** | l13 write prompts | **JUDGMENT CALL** | Prompt says "use sequence signposts for the steps" on photosynthesis (are the steps sequence or cause? genuinely arguable). Real pedagogical tension, not a clean bug. → adversarial verify. |

---

## Findings NOT yet deterministically verified (routed, not adopted)

- **Class C redundancy** — hundreds of felt_repeated flags, all single-model, high-retention personas. The within-lesson triple-test (Steps 6/7/8) and cross-grade re-teach are the strongest; the l01→l02→l03 opening run and the analysis run (g10 l04→l06) are the costliest. → **adversarial verify against a weaker-learner lens**, then F3/F8.
- **Class D sequencing** — "which-type after lessons that require the type" (g11/g12), difficulty inversion (g9 l13, g10 l11), rubric shown too late (g11 l15). Checkable against lesson order. → **F9** (deterministic order check next).
- **Class G conceptual gaps** — good-vs-weak reason, scoped-vs-hedged, exception-sinks-claim, number-in-paraphrase. Real solo-student gaps, average persona. → **F10** (copy/tooltip answers).
- **G10 Chopin twist revealed only inside a wrong answer** (l05) — specific, checkable, not yet run.
- **Cross-grade source exhaustion** (AI-workforce, water, congestion-pricing, volcano reused as "cold" gate sources) — degrades transfer/gate validity; strongest structural signal in the cross-grade walk.

---

## Routing summary → fix plan (all HELD until user lifts the hold)

| Class | New/existing fix-plan item | Status |
|---|---|---|
| A | (harness) | **DONE** — committed |
| B1 (12 confirmed) | **F7** — regenerate the AFTER text or the correct option so they differ | drafted, HELD |
| B2/B3 (indeterminate) | **F7** — after adversarial verify | pending verify |
| C | **F3** (orphan planners) + **F8** (redundancy consolidation) | pending verify |
| D | **F9** (resequence) | pending order check |
| E | **F1** (self_score reframe) — corroborated | already in plan |
| F-a counterclaim | **F-a** — teach counterclaim in G9 U4 *or* drop it from the l27 gate + mastery to match what G9 teaches | HELD, high priority |
| F-b l02 checklist | restore q3 to the l01 standard | HELD |
| F-d summarize | teach/practice it once in G9, or stop warning against it | HELD, low |
| F-e l13, C, B2, B3 | adversarial verify before any fix | pending |
| G | **F10** — copy/tooltip answers to the recurring solo-student questions | HELD, low |

**Verified-real and high-value right now:** Class A (fixed), B1 (12 instances), E (corroborates F1), F-a (counterclaim gap), F-b (checklist weakening).
**Refuted / overstated:** F-c (G12 l06 under-teaching).
**Cannot be settled deterministically — must go to adversarial verify:** B2, B3, C, F-e.
