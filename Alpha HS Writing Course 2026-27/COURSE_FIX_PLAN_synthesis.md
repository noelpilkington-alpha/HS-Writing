# HS Writing Course Fix Plan — synthesis of the two assessments

**Date:** 2026-07-17
**Inputs:** (1) Fable-5's "what survives contact with Timeback" audit (platform-floor); (2) Fable-5's "what to learn from AP One" audit (pedagogy-ceiling). This plan is the intersection: fix what the platform breaks, adopt what the competitor does better, and do the overlap **first**.

---

## The one insight that ties both assessments together

Both audits, reached independently, point at the **same lever: feedback resolution.**

- The Timeback audit named our two worst-degraded moves as **multi-trait rubric grading** ("the rubric is real on the grader's side, invisible as structured feedback on the student's side") and **MPO planning** (structured scaffold in → one undifferentiated aggregate out).
- The AP One audit named their single genuine advantage as **per-row rubric feedback, anchored to the student's own text, routed to named misconceptions** — and noted it is "embarrassing for us because our grader already computes the rows internally, then compresses them into one aggregate and throws the signal away."

So the highest-value fix is not new content and not a platform change. It is: **stop discarding the per-row signal the grader already produces, and format it back to the student as row-by-row, quote-anchored feedback.** Everything else in this plan is sequenced around that.

Confirmed while writing this: the grader's `ScoreResponse` already returns `breakdown={development, conventions, ...}` with per-trait scores — we currently render only the single aggregate. The change is output-formatting, not new grading.

---

## Grounding: the survival assessment (every finding → its fix)

The full Fable-5 "what survives contact with Timeback" audit, verbatim by category, each item tagged with the plan item that addresses it. This is the audit trail — nothing below is left unrouted.

### WORKS AS-IS — protect, do not touch (→ Tier 3)
| Move | Finding | Disposition |
|---|---|---|
| Discrimination minimal pairs (129) | "The strongest-fitting move in the whole course." Native MCQ + per-wrong-choice feedback + hard-gate retry is exactly what it needs. | **KEEP** (Tier 3). T1-C *enriches* it (distractor = named misconception) without changing the mechanic. |
| Predict-the-fix (94) | Diagnose → pick fix → reveal maps cleanly. | **KEEP** (Tier 3). T1-C targets each item at one misconception code. |
| Teach / stimulus / annotated before-after (404) | Static styled HTML covers it; annotations frozen (no progressive reveal) but it is fundamentally a reading move, nothing real lost. | **KEEP** (Tier 3). T1-D adds *scored* exemplars alongside. |
| Independent + transfer essays, holistic AI grading | One box, one aggregate score, one feedback blob = a legitimate **summative** essay experience. | **KEEP** (Tier 3). T1-A/T1-B upgrade the *feedback text* (still one item, still one outcome). |
| SRSD as a *fixed* ladder | "Gradual release survives as long as nobody expects it to be *responsive* release." | **KEEP** (Tier 3) — and protect it as our edge over AP One (they lack the strategy-instruction half). |

### DEGRADED — fix within the ceiling (ranked by severity, as Fable ranked them)
| # | Move | Finding | Fix |
|---|---|---|---|
| 1 | **MPO planning** — badly degraded | "We show a structured grid, then hand them one undifferentiated plain-text box; the structure exists only in their willingness to retype it." Aggregate score gives no signal about which row failed. Our table-grid is "a workaround, not the design." | **F3 — RE-ARCHITECTED** (retire the 2 orphan whole-essay-plan lessons, fold their teaching into the essay lessons that write from a plan). Root cause was the *standalone orphan lesson* + an outline scored on the essay rubric, not the feedback string. Dissolves the mismatch; own plan doc. |
| 2 | **Multi-trait rubric grading** — significantly degraded | STAAR/AP traits are "marketed as the assessment spine," but the student gets one aggregate + prose; no per-trait scores → "your Evidence row improved" tracking impossible. "The rubric is real on the grader's side; invisible as structured feedback on the student's side." | **T1-A** (surface the rows the grader already computes, as feedback text) + **T1-B** (quote-anchor them). This is the plan's #1 lever. |
| 3 | **Diagnosis / self-revision** (94) — near the fiction line | Card can't embed the student's just-written draft (they scroll/copy-paste); grader scores the revision **standalone** — never sees the original, so cannot assess improvement, and an unchanged resubmit scores identically, undetected. | **F2**: target the diagnosis at the T1-A row breakdown; reword any copy implying the system detects improvement (it does not). True improvement-scoring = a platform gap, not a course fix. |
| 4 | **Supported write** — mildly degraded | "A sentence starter sheet, not a writing coach... acceptable if we stop describing it as guided." | **F5 (new)**: copy sweep — stop calling the static scaffold "guided"/"coaching"; frame it honestly as a starter frame. Folds into the F4 copy pass. |

### FICTION — does not function; must not ship as-is
| Move | Finding | Fix |
|---|---|---|
| **self_score calibration** (21 slots) | The one that genuinely won't work: predict-your-score → system-compares-to-grader **cannot close** (no branching, no way to pipe the grader result into the self_score item). "What ships is an ungated rating click followed by nothing." | **F1**: reframe as calibration *against the T1-A row breakdown* ("compare to your self-score; the row you missed by >1 point is your revision target"). Converts a dead click into a real move without branching. True closed loop waits on external-app/platform. |
| **Per-part scoring anywhere** | Any lesson copy implying "each outline row / rubric section is assessed" is false — composite items return one aggregate. Promising part-level accountability misleads the student. | **F4**: copy sweep across essay/MPO lessons — reword to what the platform actually delivers (one aggregate + row-by-row *feedback text*, not row *scores*). |

**Net:** every WORKS item is protected, every DEGRADED item has a within-ceiling fix, and both FICTION items are either reframed (self_score) or corrected in copy (per-part). Nothing in the assessment is left unaddressed.

---

## What we are NOT doing (decided by the two audits)

- **Not** copying XP / day-streaks / a single "accuracy" number — Fable: engagement veneer; "psychometrically incoherent for a construct like rhetorical analysis; the rows are the real signal."
- **Not** adding mastery gates on noisy AI 0/1 rubric rows — false pass/fails.
- **Not** rebuilding as an external app *in this plan* — that's a separate strategic fork (documented elsewhere). This plan makes the **current Timeback courses** as good as the ceiling allows.
- **Not** shipping the one FICTION move as-is (see F1).

---

## TIER 1 — Adopt within the Timeback ceiling NOW (no platform change)

**T1-A · Per-row rubric feedback string.** [biggest impact; grader-side]
The grader already computes rows (STAAR: Development/Organization + Conventions; AP: Row A Thesis / Row B Evidence&Commentary / Row C Sophistication). Change the grader's `feedback` output from one prose blob to a **row-by-row breakdown**: each row's score + one targeted sentence. Timeback blocks structured per-row *scores* in the item outcome, but not the *text* of the feedback string. 
- Where: `Writing_Test_Grader` grader output formatting (`external_score` / panel feedback assembly). Zero course-repo change.
- Blocker note: `rc.ap` (G11/G12 AP rows) is still stubbed/uncalibrated — the AP panel must be wired + calibrated for the AP rows to be real. STAAR rows (G9/G10) exist now.

**T1-B · Quote-anchored feedback.** [high impact; grader-side]
Instruct the grader to quote 1–2 of the student's OWN sentences per row as the anchor, not a generic description. Fable's example: not "name the device's effect" but "Your sentence 'Swift uses irony to make his point' names the device but never its effect — this is where Row B stalls at description." Loses the visual inline overlay (blocked), keeps ~80% of the value.
- Where: grader prompt. Pairs with T1-A in the same change.

**T1-C · Misconception taxonomy as an authoring asset.** [high impact; content-side, no runtime]
Build the curated error catalog AP One has (theirs: coded misconceptions like `mc_tone_is_just_word_choice`). ~15–25 codes cover AP Lang; a similar set for G9/G10 argument/analysis. Use it three ways, all within the ceiling:
  1. Every MCQ **distractor = a named misconception**, its feedback names + corrects that specific error.
  2. **predict-the-fix** items each target one code.
  3. **Seed the grader prompt** so essay feedback names the pattern ("this is the device-spotting trap"), not just the symptom.
- Where: a content-team spreadsheet → wired into discrimination `choices[].why` + grader prompt. No classifier runtime needed (that part is blocked; the taxonomy is the asset).

**T1-D · Scored exemplar study.** [medium impact; content-side]
We have annotated before/after cards; AP One has *scored* exemplars with row-tagged annotations ("what a Row B 4 looks like vs a 2"). Add, for the essay lessons: a static exemplar card with row-tagged callouts → an MCQ sequence interrogating it ("Which sentence earns the Sophistication point?"; "This scored 2/4 on Row B — which revision moves it to 3?"). Studying scored worked-examples before producing is well-supported and we underuse it.
- Where: new slots in the essay-grain lessons (teach/display + discrimination), all native kinds.

---

## TIER 2 — Fix the degraded/fiction moves the Timeback audit flagged

**F1 · self_score calibration (21 slots) — the one FICTION move.** [must-fix: currently misleads]
The predict-your-score → compare-to-grader loop **cannot close on Timeback** (no branching, no way to pipe the grader result back into the self_score item). Today it ships as an ungated rating click followed by nothing.
- Fix within ceiling (from the AP One synthesis, A5): reframe it as a **calibration-against-the-row-breakdown** exercise. The grader feedback (now row-by-row, per T1-A) opens with: "Compare this to your self-score. The row you were off by more than a point is your revision target." Converts a dead step into a real calibration move without needing branching.
- If we later go external-app: this becomes a true adaptive loop. For now, T1-A is its prerequisite.

**F2 · Diagnosis / self-revision (94 slots) — degraded, near-fiction.** [important]
The diagnosis card can't see the student's just-written draft, and the grader scores the revision standalone (never sees the original → can't assess *improvement*; an unchanged resubmit scores identically, undetected).
- Fix within ceiling: (a) the diagnosis prompt must restate the checklist against the row breakdown the student just received (so revision is targeted, not generic); (b) reword any copy that implies the system detects improvement — it doesn't. Honest framing: "revise, then resubmit for a fresh score," not "show your improvement."
- True improvement-scoring needs the platform to pass the prior draft — a gap, not a course fix.

**F3 · MPO / orphan whole-essay planning — DONE 2026-07-18 (retire + fold + reframe).** [RESOLVED]
> Executed via `docs/superpowers/plans/2026-07-17-retire-orphan-planning-lessons.md`. Retired the 2 standalone whole-essay-plan orphans — `C904-0019` (G9 MPO) and `C1006-0020` (G10 cross-text planner) — moving each to a `_deprecated_orphan_planning/` dir and dropping its mastery entry (no dangling id). Folded their teaching into the essay lessons that plan AND write (G9 C904-0023/0024 now teach the two-level SPO→MPO plan; G10 C1006-0021/0022 now teach "plan by points, not by sources"). Reframed `C901-0022` (mode-decision, a different KC — KEPT) so its graded write is the mode decision + one thesis sentence (unit sentence), not an orphan whole-essay plan. Orphan test now returns NONE. Course 100 → 98 lessons (G9 27→26, G10 26→25). All grades tier-A clean; 121 tests pass. The rubric-mismatch dissolves: no outline is scored standalone on an essay rubric anymore.

*Original analysis (kept for the record):* [important; own implementation plan]
Deeper look (Noel, 2026-07-17) found the real problem is not the grid or the rubric — it is that the MPO is taught as a **standalone lesson where the student plans a whole essay and then never writes it**. Grading that orphan plan on the STAAR *essay* rubric (Development/Organization + Conventions) is also a category error: an outline is note-form, so Conventions is noise and Dev/Org does not decompose into the MPO's own rows. T1-A alone would only have put essay-grading resolution on a planning artifact — a patch on the wrong layer.
- **Verified scope:** exactly TWO true whole-essay-plan orphans — `ACC-W910-L-G9-C904-0019` (MPO) and `ACC-W910-L-G10-C1006-0020` (cross-text planner). (L21 order-paragraphs and L22 intro/conclusion are genuine paragraph *sub-skills*, KEPT; `C901-0022` is a different KC — mode-decision — reframed, not retired.)
- **Fix (Timeback-honest, no platform dependency):** fold each orphan's teaching into the essay lessons that *already* run teach→model→plan→write in ONE lesson (G9 C904-0023/0024; G10 C1006-0021/0022), then retire the standalone + drop its mastery. Within-KC only (C904, C1006); no pipeline/gate/renderer change.
- **This dissolves the rubric-mismatch entirely** — outlines are no longer scored standalone; the plan becomes the SUPPORTED scaffold *inside* the essay lesson, feeding the scored essay. The already-shipped outline-table grid stays as that in-lesson scaffold.
- **Full implementation plan:** `docs/superpowers/plans/2026-07-17-retire-orphan-planning-lessons.md` (6 tasks, content-loss-guarded, verified by tier_a_regression + tests; course 100 → 98 lessons).

**F4 · Per-part promises — copy audit.** [cheap, do with T1-A]
Any lesson text implying "each outline row / rubric section will be scored" is false on Timeback (one aggregate). Sweep the essay/MPO lessons and reword to what the platform actually delivers.

**F5 · Supported-write honesty — copy fix.** [cheap, do with F4]
The "supported write" scaffold is a static starter frame, not responsive coaching (Timeback forbids mid-draft feedback). Fable: "a sentence starter sheet, not a writing coach... acceptable if we stop describing it as guided." Sweep the supported-write slots and drop any "guided"/"coaching"/"as you write" language; frame it as a starter frame. Same copy pass as F4.

**F6 · G11/G12 CCSS re-skin — strip AP-exam wording (student-facing only).** [copy-only; own replacement key]
*Source: the standards-alignment investigation (2026-07-17), not the two audits.* Concern raised: are G11/G12 "beyond CCSS"? **Verdict (Fable, move-by-move vs CCSS 11-12 anchors): NOT valid — the content is in-band.** Every taught skill maps onto CCSS 11-12 (W.11-12.1/1a/1b/4/5/7/8/9, RI.11-12.6, L.11-12.3; timed writing = W.11-12.10). The AP layer is *packaging*, not extra content. Decision (Noel): **treat G11/G12 as standard CCSS courses**, so the AP-exam framing becomes an optional overlay, not the default vocabulary — a **re-skin**, keeping every skill.
- **Scope (student-facing text ONLY — titles, slot bodies, mastery prompts; NOT code comments / `council:` notes / docstrings, which legitimately keep AP provenance):** ~20 lessons; 7 AP-worded G12 titles + AP terms in bodies (sophistication×74, FRQ×38, Row C×17, full-write×13, "the exam"×4, AP Lang×2).
- **Replacement key (full mapping + the 7 title rewrites):** `CCSS_RESKIN_G11_G12_key.md`. Core swaps: sophistication→complexity/nuance/depth-and-significance; FRQ (type)→writing task (type); "the exam"→timed writing / single sitting; full-write→full essay; drop "(Row C/B/A)" rubric coordinates, keep the trait names.
- **Keeps everything:** no skill removed, no lesson retired, timed practice reframed as W.11-12.10 (not deleted), and **`ACC.W.INQ.1`** stays on its 4 G11 lessons as the documented additive §3 differentiation tag (those lessons also carry CCSS 11-12 tags — the course is not "non-CCSS" for keeping it; just do not market it as beyond-CCSS).
- **Verify:** copy-only, so `tier_a_regression.py G11/G12` stays clean; re-grep student-facing text → 0 remaining AP terms (comments excluded); spot-render.
- **Note:** the standards-alignment grep also confirmed there is **no "beyond CCSS" inflation language** describing the courses to correct — the only "beyond CCSS" phrases in the docs accurately label the deliberate §3 differentiation tier. So F6 is purely the AP-wording re-skin, nothing else.

---

## TIER 3 — Keep as-is (both audits agree these WORK)

No action — verified strong on Timeback: **discrimination minimal pairs** (best-fit move), **predict-the-fix**, **teach/stimulus/annotated before-after display**, **independent + transfer essays with holistic AI grading**, **SRSD as a fixed ladder**. And the thing AP One *lacks* that we should protect: **explicit SRSD strategy instruction** (they have rich feedback, no strategy-teaching half — our genuine edge; do not dilute it chasing their feedback features).

---

## TIER 4 — Learning-science integration (from the BrainLift audit, 2026-07-17)

*Source: `BRAINLIFT_INTEGRATION.md` — five-reader audit of the Learning Scientists' BrainLift canon against this course. These items are all Timeback-fixable NOW (authoring / copy / QC / grader-prompt / item-metadata). Deeper items that need cross-session state are logged there as the external-app fork, not here. Several items VALIDATE and sharpen the Tier-1/2 fixes above; the rest are new and independently corroborated by the G9 sim-student eval.*

**B1 · Check-validity: novel-stimulus rule + sync-check taxonomy.** [top lever; free; own gate] The sim-student eval found in-lesson MCQs pass ~100% for the wrong reason — the correct option is the worked-example's AFTER sentence verbatim (~16 lessons); the check measures recognition, not skill. BrainLift standard: a valid item is answerable *from the stem alone* and must not reuse just-read material. Fix: a new deterministic gate `gate_sync_check_novelty` (no verbatim-echo correct option; no self-confessing distractor; ≥1 check-for-understanding per lesson on a NEW example), plus a copy rule that stops calling a checkpoint pass "mastery." **Full spec in `BRAINLIFT_INTEGRATION.md` Part 4. This is the executable next step.**

**B2 · Misconception-mapped distractors REQUIRE coupled feedback.** [sharpens T1-C] "Distractor quality and feedback quality are coupled — you cannot set one without the other"; a plausible distractor without feedback *implants* the error. Hardens T1-C: every distractor maps to one NAMED error and its feedback corrects that specific error. Seed the taxonomy from the discipline's catalogued writing misconceptions (persuasion=emotion, evidence-speaks-for-itself, counterclaim=weakness-to-hide, more-devices=better-analysis).

**B3 · Grade the logic; zero out unexplained warrants + generic evidence.** [sharpens T1-A/B — the #1 lever] Adopt the AP-History/Social-Studies scoring rule into the grader prompt + rubric: a conclusion without a mechanism earns zero; a below-specificity claim earns zero; sourcing scores as *explanation of significance to the argument*, not label-spotting. Give each production KC an **Assessment Pack** (decisive attributes + named forbidden shortcuts + near-misses) so the external grader is defensible.

**B4 · Add stateless item TYPES beyond MCQ.** [new mechanics] Ordering (unscramble sentences into a coherent argument), cloze (supply the missing thesis/transition/warrant), claim↔evidence matching, tri-state sort with a "Neither" bin, and level-tagged MCQ (each option = a rubric level 0/1/2). All auto-scorable + stateless; measure writing structure, not recognition. The level-tagged MCQ also powers T1-D and B5.

**B5 · self_score as a prediction-gap (not a verdict).** [completes F1] Capture a confidence prior before the check; after revealing the T1-A row breakdown, show the gap between predicted and actual row scores — the gap IS the calibration signal, and it closes statelessly. This is the concrete mechanic F1's reframe was reaching for.

**B6 · Name the tools; teach moves as named procedures.** [copy + sequence] The sim-student tracked "6+ unnamed 3-question checklists" (extraneous load). Consolidate + NAME recurring tools the way we name HIT/PROVE/S³. Teach counterclaim/analysis/synthesis as named, reusable routines with acceptance criteria BEFORE the integrated essay assembles them.

**B7 · Cheap MCQ QC + multimedia wins.** [fold into `writing-card-qc`] Balance the answer key (correct answers cluster in B/C); ban all-of/none-of-the-above + T/F in summative pools; run a cue-sweep for self-confessing distractors. Build SVG diagrams element-by-element with narration (never show the final state first); write narration in conversational "you/we" register.

**M2 · Pre-write comprehension gate (reading-access risk).** [new; important] A student who can't parse the stimulus writes a weak essay — and the grader misattributes it to weak *writing*. Add a fast stimulus-comprehension check gating each FRQ, so a reading failure isn't scored as a writing failure. Consider a few anchor topics taught in depth over many shallow ones.

**M4 · Motivation layer (the underbuilt whole component).** [copy + config; high leverage] Attribution-engineered per-choice feedback (credit strategy not ability; "Not quite — here's why," never "Wow, you got it!"); practice-vs-assessment error climate (no red X on practice); XP tied to mastery not completion, personal-best not leaderboards; a stateless "approval/LFG" rationale-then-acknowledge beat at lesson open; author checks toward an ~80-85% first-try success rate.

**M5 · Retry rotates a fresh item.** [important] Hard-gate retry currently re-shows the identical MCQ → certifies grind-through, not repair. Give each checkpoint a small item POOL that rotates a fresh variant on each retry.

**M6 · Expert difficulty bands (NOT IRT).** [metadata] Tag each item with a KDT-rubric difficulty band + provenance. At our volume, data-driven calibration is statistically impossible and LLMs underestimate difficulty — so use expert-set bands, and treat "90% to pass" as a convention to calibrate, not a fixed truth.

**M1-partial · Convert redundancy into interleaved cumulative retrieval.** [sequence] The ~11 whole-lesson repeats are *massed* practice; the fix is not deletion but conversion — later lessons should RECRUIT earlier KCs to do new work (interleaved retrieval), turning redundancy productive. (Full spacing + a fluency stage need the external app — logged there.)

---

## TIER 5 — Simulated-student audit findings (2026-07-17, all five grades)

*Source: the 5 simulated-student walk reports (G9/G10/G11/G12/cross-grade), triaged in `SIM_STUDENT_FINDING_LEDGER.md`. Method: classify each finding by the artifact it concerns → verify against THAT artifact → adversarial refute-pass on judgment-class findings → route only survivors here. Calibration: one model (Fable), two high-retention personas, so nothing is cross-model corroborated and "too easy / nothing new" is partly a persona artifact. **~400 raw instance-flags reduced to the short list below; nothing bulk-adopted.** The harness bug that confounded every rendering claim was found and FIXED first (see S0).*

**S0 · Audit-harness rendering bug — FIXED (not a course fix).** [done] `render_student_experience` (the renderer the sim-student + readiness audits walk) parsed MCQ options from slot `body` prose only; 8 discrimination slots (G9:4, G10:2, G11:1, G12:1) carry options only in `choices[]` with an empty body, so the audit lens showed a prompt with ZERO options — which the students reported as "blank/unanswerable MC steps." The pushed QTI renders those options correctly (verified: 6 `qti-simple-choice` each), so this was an audit-lens divergence from production, **not a ship defect.** Fixed in `pipeline/lesson_review.py` + regression test `test_student_view_options.py`; full sweep now 0/129 broken. *This corrects a prior wrong "FALSE/discard" verdict — the students were right; the check had verified the wrong render path.*

**S1 · Recognition-not-application: correct MC option == a prior worked-example AFTER, verbatim.** [CONFIRMED — 12 instances; sharpens Tier-4 B1] Deterministically verified (text-overlap ≥0.70): g9 C901-0001 s4, C902-0007 s4 (.93), C902-0009 s4, C906-0027 s4; g10 C1001-0001 s4, C1002-0008 s4 (.91); g11 C1101-0001 s5, C1101-0002 s4, C1101-0003 s4; g12 C1201-0001 s4, C1201-0002 s4, D1201-0015 s4. The student picks by memory, not skill. **Fix:** regenerate either the AFTER text or the correct-option wording so they differ (the discrimination must be answerable from the stem, testing the skill not recall). This is exactly the `gate_sync_check_novelty` gate Tier-4 **B1** specifies — these 12 are its concrete initial worklist.

**S2 · Counterclaim required by the G9 gate but never taught in G9.** [CONFIRMED — high severity; cross-audit corroborated] "counterclaim" appears 0× in G9 l01–l26 but `ACC-W910-L-G9-C904-0029` (l27 gate) requires it in the task line, the one-reminder, the checklist, the sentence frame, AND the PP100 mastery pass criteria. Independently corroborates the earlier readiness finding (C904-0029) and Tier-4 B6.
- ~~**DECISION (Noel, 2026-07-17): DROP counterclaim from the G9 l27 gate + its PP100; counterclaim stays in G10.**~~ **SUPERSEDED 2026-07-21 (Noel overturned S2).**
- **NEW DECISION (Noel, 2026-07-21): ADD counterargument to G9 as a full unit; RE-ADD it to the argument gate.** The overturn is standards-defensible: the earlier decision leaned on "standards place it at G10," but CCSS **W.9-10.1a** (mapped to BOTH C.9.01 and C.10.01) is a **9-10 BAND** standard whose text includes distinguishing a claim from *opposing* claims = counterargument. So the G9/G10 split was a sequencing choice (TEKS Eng II + SRSD deferral), not a standards mandate; teaching it in G9 re-aligns to the band standard. Corroborated by the course's own A1 map already carrying an opposing-position / Counter-Thesis move.
- **Build (docs/plans/2026-07-21-g9-counterargument-add.md):** new KC **C.9.07** (funnel counterargument, W.9-10.1a, ACC.W.ARG.2); new **G9 U4 "Counterargument"** before the essay gate (old U4 essay+gate renumbered to U5, lesson files l19,l21-l27 -> l22-l29); **3 new G9 lessons** l19/l20/l21 (recognize / concede-then-answer / answer-in-a-paragraph) at introductory depth; **re-add** counterargument to the G9 argument gate (now l29, id stable ACC-W910-L-G9-C904-0029). **G10 U1 stays, reframed as the deeper spiral** (concede-vs-collapse + strawman + evidence rebuttal). The original "required but never taught" contradiction is resolved the other way: now it is both taught AND required.

**S3 · G10 l02 checklist weakened its q3 on the student's weakest skill.** [CONFIRMED] `ACC-W910-L-G10-C1001-0002` q3 = "Is there a reason for the side you hold?" vs l01's stronger q3 = "Does the reason answer that objection, not just repeat your side?" The l02 version drops the answer-the-objection bar precisely where the student struggles. **Fix:** restore q3 to the l01 standard (answer-the-objection, not merely reason-exists). One-slot copy edit.

**S4 · Calibration lessons instruct SUBMIT→grader→compare, but no such loop exists.** [CONFIRMED — corroborates F1] g11 C1103-0015, g12 C1201-0007, g12 C1202-0014 literally say "SUBMIT: send to the grader… the grader returns its score… compare against it." This is the F1 self_score fiction, independently confirmed by the students. **No new fix — folds into F1** (reframe as calibration against the T1-A row breakdown). Confirms F1 is must-fix, not optional.

**S5 · "Name the task type" taught AFTER lessons that require choosing the type.** [CONFIRMED — G11 + G12] G12: "Name the FRQ Type" is #12, but #9/#10/#11 (rehearse a complete argument / analysis / synthesis) already presuppose it. G11: "Match the Moves to the Task Type" (#28) / "Name the Task Type" (#29) follow the full multi-perspective essay (#22) + rehearsal (#27). **Fix (F9 — new):** move the type-identification lesson BEFORE the rehearsal/timed lessons in both grades. Resequencing only (lesson IDs stable; reorder the course_sequence + any unit framing). Medium priority.

**S6 · Gate sources are not cold — the gate topic already appeared in 6+ prior lessons.** [CONFIRMED — strongest structural finding; sharpens M1] g9 gate #26 reuses "volcano" (also 4,12,14,19,20,21,25); g10 gate #24 reuses "congestion pricing" (1,3,15,17,18,20,23); g11 mid-gate #16 reuses "workforce" (1,2,3,4,5,13). A gate meant to test cold transfer runs on a memorized topic, inflating the pass. **Fix (F8 — new):** swap each gate's (and late transfer steps') stimulus to a genuinely-unseen topic from the Source Cache. High priority — this is gate *validity*, and it is the productive half of the redundancy signal (the source-exhaustion Tier-4 M1 flags). Content-swap within existing slots; no structural change.

**S7 · "Summarize" defined (g9 l05) but never practiced, then warned against for 3 grades.** [CONFIRMED — low] No G9 production task asks the student to summarize, yet g10/g11 lean on "analysis is not summary." **Fix (low):** either add one summarize practice task in G9, or stop framing summarize as a taught mode in l05. Defer unless a copy pass is already touching l05.

**S8 · Unresolved solo-student conceptual questions ("no one to ask").** [CONFIRMED — low, persona-specific (average_fable)] Recurring open questions the course never closes: good-vs-weak reason (g9 l01), scoped-vs-hedged / "does most count?" (g11 l01–l02), does one exception sink a claim, can an exact number sit in a paraphrase (g9 l05). **Fix (F10 — new, low):** add a one-line answer or a tooltip/aside at the point each question first arises. Copy-only; batch into the F4/F5 copy pass.

### Sim-student findings REFUTED (verified NOT defects — do not act)
- **Write task on same source as its worked example** — SRSD guided-practice fade; adversarial refute-pass found 0 copy-the-answer defects (several AFTERs are truncated stubs). REFUTED high-conf.
- **"Checks that run themselves"** — all sampled are the sanctioned coping-model (modeled think-aloud on a PROVIDED weak draft, then an independent student turn; several re-run the checks on the student's own writing). REFUTED high-conf.
- **Cross-grade / opening-run redundancy (5 strongest pairs)** — each later lesson adds a genuine increment (arguable→specific+stakes; attribution→integration; produce-warrant→detect-circular-warrant; single-paragraph weave→whole-essay architecture; scope→value-tension). High-retention personas flagged review a *weak* learner needs. REFUTED high-conf. (The productive residue — within-lesson triple-testing + gate source reuse — is handled by S6/F8 and Tier-4 M1, not by deleting lessons.)
- **G12 l06 under-teaches synthesize/weight** — REFUTED: weight taught 326 words across s1/s2/s4, all before the composition. A thin-teaching *perception*, not a gap.
- **g9 l13 sequence-vs-cause** — REFUTED: "sequence" is the safer, correct choice (a cause signpost would be factually false); the lesson applies its own rule consistently.
- **G10 l05 Chopin twist in a wrong answer** — UNCONFIRMED: the specific claim did not reproduce; no wrong option leaks the ending. Low / not actionable.

### New fix items introduced by Tier 5 (all HELD until go)
| Item | What | Priority | Scope |
|---|---|---|---|
| **S1→B1** | de-duplicate correct option vs worked-example AFTER (12 instances) | high | content, within-lesson |
| **S2** | ~~DROP counterclaim (stays G10)~~ **SUPERSEDED 2026-07-21: ADD counterargument to G9 (new KC C.9.07 + U4, 3 lessons) + RE-ADD to gate; G10 U1 -> deeper spiral** | **overturned -> building** | new KC + unit + renumber |
| **S3** | restore G10 l02 checklist q3 to the answer-the-objection standard | medium | 1-slot copy |
| **S4→F1** | (folds into F1) | — | — |
| **F8 (S6)** | swap gate/late-transfer sources to unseen topics (all 3 grades) | **high — gate validity** | content-swap in slots |
| **F9 (S5)** | move "name the type" before the rehearsal/timed lessons (G11+G12) | medium | resequence |
| **F10 (S8)** | one-line/tooltip answers to recurring solo-student questions | low | copy, batch w/ F4/F5 |
| **S7** | summarize: practice once in G9 or stop warning against it | low | copy |

---

## Sequencing (do in this order)

1. **T1-A + T1-B + F4 + F5** (one grader-output change + a single copy sweep covering both per-part promises and "guided"-write language) — highest impact, no platform work, unblocks F1. **Start here.**
2. **F6 CCSS re-skin** (G11/G12 AP-wording → CCSS, student-facing only) — copy-only, has its own replacement key; can run in the same copy pass as F4/F5 or standalone. Independent of the grader work.
3. **F3 re-architecture** (retire the 2 orphan planners, fold into the essay lessons) — its own plan doc; independent of the grader work, can run in parallel with #1. Removes redundancy + the outline-rubric mismatch.
4. **T1-C** (misconception taxonomy) — content-team spreadsheet, then wire into distractors + grader prompt.
5. **F1 + F2** (reframe self_score + diagnosis around the new row feedback) — course-copy edits.
6. **T1-D** (scored exemplars) — new native slots in essay lessons.
7. **Wire + calibrate `rc.ap`** so the AP rows in T1-A are real for G11/G12 (deferred grader work; STAAR rows work now).

**Tier-5 sim-student fixes — interleave by cost, gated on the audit-review sign-off:**
- **S0** audit-harness fix — **DONE** (committed; unblocks all future audits).
- **S2 counterclaim + F8 gate-sources** — **high priority, decide first.** S2 needs a routing decision (teach-in-G9 vs drop-from-gate); F8 (swap gate/transfer sources to unseen topics) is the single biggest validity win and pairs naturally with the Source Cache. Do these before re-running any readiness/graded pilot, since both distort the gate result.
- **S1→B1** (de-dup the 12 recognition items) — fold into the Tier-4 **B1** `gate_sync_check_novelty` build; these 12 are its first worklist.
- **S3 (l02 checklist), S5→F9 (resequence type lessons), S7, S8→F10** — batch the copy/1-slot edits into the F4/F5 copy sweep; F9 resequence is a separate small course_sequence change.
- **S4** — already covered by F1.

## Honest scope line
Tiers 1–2 make the Timeback courses materially better *within the ceiling* and kill the one misleading move. What they **cannot** fix (per-section scores surfaced structurally, live mid-draft coaching, true improvement-aware revision, a closed adaptive calibration loop) are the exact things the external-app option would unlock — so this plan and the platform decision are complementary, not competing: ship these fixes now regardless of the platform call.
