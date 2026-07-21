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
| **B2 Write task sits on the same source as its worked example** | lesson source + **adversarial verify** | **REFUTED (high conf)** | Skeptic prompted to refute found 0 genuine copy-the-answer defects across 8 sampled lessons. Every lesson culminates in a NEW artifact the AFTER doesn't contain (own claim, fresh draft to fix, whole essay, synthesis position); several AFTERs are truncated stubs with nothing to copy. This is textbook SRSD guided-practice fade, not a defect. |
| **B3 "Checks that run themselves"** (diagnosis prompt answers its own check) | lesson source + **adversarial verify** | **REFUTED (high conf)** | Skeptic found 0 pure give-aways across 14 sampled items; all 14 are the sanctioned coping-model (the stated answers diagnose only a PROVIDED weak draft, then the student does an independent turn — 4 items explicitly re-run the checks on the student's OWN fresh writing). The "diagnosis is never tested" premise is false. |

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
| **F-e g9 l13 Step 8 forces sequence signposts where the real relation is cause** | l13 full lesson + **adversarial verify** | **REFUTED (high conf) — NOT a correctness bug** | "Sequence" is the *safer* choice, not wrong: a cause signpost ("sunlight in → as a result → water in") would be factually FALSE (sunlight doesn't cause water uptake). The lesson applies its own rule consistently — it correctly uses a CAUSE signpost at s5 where the link is a genuine consequence, and contrast for the energy-loss step. No student following it writes a logically wrong sentence. |

---

### Class D — Sequencing (deterministic order check, run 2026-07-17)
| Finding | Artifact verified | Verdict | Evidence |
|---|---|---|---|
| **D-a "Name the type" taught AFTER lessons that require choosing the type** | G11 + G12 lesson order + lesson TARGETS | **DOWNGRADED to felt-friction, NOT a broken dependency; F9 SKIPPED (Noel 2026-07-17)** | On inspection the rehearsal lessons each rehearse ONE *named* type (G12 l09 "Rehearse a Complete **Argument** Essay", l10 analysis, l11 synthesis; G11 l27 synthesis; l28 "Match the Moves to the Task Type" already teaches type-spotting before l29). The student is never asked to identify the type unaided before it is taught, so the prerequisite is not broken. Severity MEDIUM, and a renumber is a multi-file cascade (loader/push order + course_sequence self-test) with real regression surface. Decision: leave order as-is. |
| **D-b Difficulty inversion: ordering/transitions lesson after paragraph/essay work** | G9 + G10 order | **CONFIRMED but LOW** | g9 #21 "Order the Paragraphs" after 6 paragraph/essay lessons; g10 #11 "Order Sentences" after counterclaim-paragraph work. Real, but arguably defensible as a distinct sub-skill / spaced practice; not a correctness issue. |

### Class C — Source-set exhaustion (deterministic, run 2026-07-17)
| Finding | Artifact verified | Verdict | Evidence |
|---|---|---|---|
| **C-src Gate sources are NOT cold — the gate topic already appeared in ≥2 (here 6+) prior lessons** | topic-keyword scan across each grade | **CONFIRMED — strongest structural finding. G9 + G10 FIXED 2026-07-18; G11 needs a new source (flagged)** | g9 GATE #26 reused "volcano" (also 4,12,14,19,20,21,25) → **FIXED**: gate 2nd write swapped to HIGHWAYS (Interstate system, 0 prior G9 use, verified 46,876-mi figure). g10 GATE #24 reused "congestion pricing" (1,3,15,17,18,20,23) → **FIXED**: gate swapped to ARG-OPP-0003 nuclear power (0 prior G10 use, genuine two-sided source). g11 mid-gate #16 reused "workforce" (1,2,3,4,5,13) → **FIXED 2026-07-18**: authored a new 4-source synthesis set `ACC-W910-SYNTH-SET-0004` (national parks, use-vs-preservation; 0 prior G11 appearances) reusing the already-verified NPS/DOI fact table from `info_national_parks.py` (no new figures → no fabrication). All QC gates pass (4 sources in band, Lexile 1181-1237L, all figures backed). Mid-gate lesson now binds SET-0004. **Residual (flagged, not forced):** the mid-gate's PP100 *mastery* prompt still uses a water set — warm vs the unit but distinct from the lesson (national parks), which is the cold-vs-the-just-written-gate property mastery needs; making it cold-vs-unit too would need a *second* authored set. |

### G10 Chopin twist inside a wrong answer
| Finding | Artifact verified | Verdict | Evidence |
|---|---|---|---|
| **A wrong l05 option reveals the story's ending** | g10 l05 discrimination options | **UNCONFIRMED (low)** | Keyword scan of wrong options found no ending/twist spoiler. The report's specific claim does not reproduce deterministically; treat as low / not actionable without the exact quote. |

## Findings NOT yet deterministically verified (routed, not adopted)

- **Class C redundancy** — hundreds of felt_repeated flags, all single-model, high-retention personas. **Adversarial verify (weaker-learner lens) REFUTED the 5 strongest cross-grade/opening pairs (high conf):** each later lesson adds a genuine increment (arguable→specific+stakes; attribution→integration; produce-warrant→detect-circular-warrant; single-paragraph weave→whole-essay architecture; scope→value-tension), i.e. defensible spaced practice a weak learner needs, not pure duplication. **The high-retention personas flagged review that a struggling student requires.** NOT a redundancy-deletion mandate. Residual to still check: within-lesson triple-testing (Steps 6/7/8 same exercise 3×) — a *tightening* opportunity, distinct from cross-lesson redundancy — and source-set exhaustion (below).
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
| B2 | none — **REFUTED** | closed, no fix |
| B3 | none — **REFUTED** | closed, no fix |
| C (cross-grade/opening pairs) | none — **REFUTED** (defensible spaced practice) | closed, no fix |
| C (within-lesson triple-test + source exhaustion) | **F8** — tighten Steps 6/7/8; diversify gate/transfer sources | HELD, medium — still to verify |
| D-a | **F9 SKIPPED** — felt-friction, not a broken dependency (types are named in the rehearsal lessons); renumber blast-radius not justified | closed, no fix |
| D-b (low) | none — defensible as-is | closed, no fix |
| C-src (confirmed) | **F8** — G9 gate → HIGHWAYS, G10 gate → nuclear, G11 mid-gate → national parks (new authored SET-0004) — all DONE 2026-07-18 | **DONE** (G11 mastery-prompt cold-vs-unit residual flagged) |
| E | **F1** (self_score reframe) — corroborated | already in plan |
| F-a counterclaim | ~~DECIDED (Noel 2026-07-17): DROP from l27 gate + PP100; counterclaim stays G10.~~ **SUPERSEDED 2026-07-21 (Noel overturned S2): counterargument is now TAUGHT in G9 as a full 3-lesson unit (new KC C.9.07, G9 U4: recognize / concede-then-answer / answer-in-a-paragraph) and RE-ADDED to the G9 argument gate. G10 U1 stays as the deeper spiral (concede-vs-collapse + evidence rebuttal). Standards basis: CCSS W.9-10.1a is a 9-10 BAND standard incl. distinguishing opposing claims; the earlier G10-only split was a sequencing choice, not a mandate. See docs/plans/2026-07-21-g9-counterargument-add.md.** | SUPERSEDED -> BUILDING |
| F-b l02 checklist | restore q3 to the l01 standard | HELD |
| F-d summarize (S7) | **DONE 2026-07-18** — reframed g9 l05 so summarize is named as the mode for writing from a whole source (quote/paraphrase = today's focus); no false "you'll drill it later" promise | done |
| F-e l13 | none — **REFUTED** (not a correctness bug) | closed, no fix |
| G (S8/F10) | **PARTIAL DONE 2026-07-18** — added the highest-value note to g9 l01 (answers the average persona's carried "is my reason good enough?" by scoping it to later lessons). Remaining questions (scoped-vs-hedged g11, number-in-paraphrase, exception-sinks-claim) left as deferred-low: marginal, and adding tooltips across many lessons is scope not justified by severity. | l01 done; rest deferred-low |

**Verified-real and high-value right now:** Class A (fixed), B1 (12 instances), E (corroborates F1), F-a (counterclaim gap), F-b (checklist weakening).
**Refuted / overstated / closed:** F-c (G12 l06 under-teaching), **B2** (SRSD guided practice), **B3** (sanctioned coping-model), **C cross-grade/opening pairs** (defensible spaced practice), **F-e** (l13 sequence is defensible).
**Still open (deterministic checks not yet run):** D sequencing (order check), C within-lesson triple-test + source-set exhaustion (F8), G conceptual gaps, G10 Chopin-twist-in-wrong-answer.

## What the adversarial pass changed
Four "indeterminate/judgment" findings all **REFUTED at high confidence** by skeptics prompted to refute and shown the real (post-harness-fix) artifacts. This is the counterweight to my earlier error: last session I wrongly called a REAL finding false; here, the disciplined refute-pass correctly clears four findings that *looked* real to a fast-learner persona but don't survive a weaker-learner / correctness lens. The surviving high-value set is small and specific (B1, E→F1, F-a, F-b) — which is the point of triage: the raw ~400 flags reduce to a handful of genuine, actionable fixes, none bulk-adopted.
