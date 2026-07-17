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

**F3 · MPO / orphan whole-essay planning — RE-ARCHITECTED (retire + fold), not patched.** [important; own implementation plan]
Deeper look (Noel, 2026-07-17) found the real problem is not the grid or the rubric — it is that the MPO is taught as a **standalone lesson where the student plans a whole essay and then never writes it**. Grading that orphan plan on the STAAR *essay* rubric (Development/Organization + Conventions) is also a category error: an outline is note-form, so Conventions is noise and Dev/Org does not decompose into the MPO's own rows. T1-A alone would only have put essay-grading resolution on a planning artifact — a patch on the wrong layer.
- **Verified scope:** exactly TWO true whole-essay-plan orphans — `ACC-W910-L-G9-C904-0019` (MPO) and `ACC-W910-L-G10-C1006-0020` (cross-text planner). (L21 order-paragraphs and L22 intro/conclusion are genuine paragraph *sub-skills*, KEPT; `C901-0022` is a different KC — mode-decision — reframed, not retired.)
- **Fix (Timeback-honest, no platform dependency):** fold each orphan's teaching into the essay lessons that *already* run teach→model→plan→write in ONE lesson (G9 C904-0023/0024; G10 C1006-0021/0022), then retire the standalone + drop its mastery. Within-KC only (C904, C1006); no pipeline/gate/renderer change.
- **This dissolves the rubric-mismatch entirely** — outlines are no longer scored standalone; the plan becomes the SUPPORTED scaffold *inside* the essay lesson, feeding the scored essay. The already-shipped outline-table grid stays as that in-lesson scaffold.
- **Full implementation plan:** `docs/superpowers/plans/2026-07-17-retire-orphan-planning-lessons.md` (6 tasks, content-loss-guarded, verified by tier_a_regression + tests; course 100 → 98 lessons).

**F4 · Per-part promises — copy audit.** [cheap, do with T1-A]
Any lesson text implying "each outline row / rubric section will be scored" is false on Timeback (one aggregate). Sweep the essay/MPO lessons and reword to what the platform actually delivers.

**F5 · Supported-write honesty — copy fix.** [cheap, do with F4]
The "supported write" scaffold is a static starter frame, not responsive coaching (Timeback forbids mid-draft feedback). Fable: "a sentence starter sheet, not a writing coach... acceptable if we stop describing it as guided." Sweep the supported-write slots and drop any "guided"/"coaching"/"as you write" language; frame it as a starter frame. Same copy pass as F4.

---

## TIER 3 — Keep as-is (both audits agree these WORK)

No action — verified strong on Timeback: **discrimination minimal pairs** (best-fit move), **predict-the-fix**, **teach/stimulus/annotated before-after display**, **independent + transfer essays with holistic AI grading**, **SRSD as a fixed ladder**. And the thing AP One *lacks* that we should protect: **explicit SRSD strategy instruction** (they have rich feedback, no strategy-teaching half — our genuine edge; do not dilute it chasing their feedback features).

---

## Sequencing (do in this order)

1. **T1-A + T1-B + F4 + F5** (one grader-output change + a single copy sweep covering both per-part promises and "guided"-write language) — highest impact, no platform work, unblocks F1. **Start here.**
2. **F3 re-architecture** (retire the 2 orphan planners, fold into the essay lessons) — its own plan doc; independent of the grader work, can run in parallel with #1. Removes redundancy + the outline-rubric mismatch.
3. **T1-C** (misconception taxonomy) — content-team spreadsheet, then wire into distractors + grader prompt.
4. **F1 + F2** (reframe self_score + diagnosis around the new row feedback) — course-copy edits.
5. **T1-D** (scored exemplars) — new native slots in essay lessons.
6. **Wire + calibrate `rc.ap`** so the AP rows in T1-A are real for G11/G12 (deferred grader work; STAAR rows work now).

## Honest scope line
Tiers 1–2 make the Timeback courses materially better *within the ceiling* and kill the one misleading move. What they **cannot** fix (per-section scores surfaced structurally, live mid-draft coaching, true improvement-aware revision, a closed adaptive calibration loop) are the exact things the external-app option would unlock — so this plan and the platform decision are complementary, not competing: ship these fixes now regardless of the platform call.
