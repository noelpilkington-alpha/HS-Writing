# SIM_STUDENT_EVAL_G9 — accuracy check (are the findings real?)

**Date:** 2026-07-17
**Purpose:** Noel asked whether the G9 simulated-student eval's findings are accurate before we fold them into the course fix plan. Each finding below is checked against ground truth (the actual lessons, rendered items, and source bindings) — not taken at face value.

**Key calibration fact:** the sim-student walks ran under **Fable-5** (both personas, "one model" per the report). That is the SAME model whose readiness audit this session was shown to over-flag ~3.3:1, and specifically to HALLUCINATE "blank/broken multiple-choice items" because it cannot see the rendered option set. So Fable-sourced claims about *rendering/missing options* are suspect by default; claims about *content/sequence/redundancy* are the model's real signal and must be judged on merits.

---

## Verdicts

### ✅ REAL (CORRECTED 2026-07-17) — "Broken/blank multiple-choice steps" (Q1 + Q4)
Claim: options never rendered in g9_l02 s6, l03 s6, l04 s5, l08 s5 — "literally could not answer, had to skip."
**This verdict was originally recorded as ❌ FALSE. That was wrong.** The original "ground truth" checked the QTI *push* path (`build_lesson_html`), which does render the options — but the sim-student agent is fed `render_student_experience(L)` (the audit lens), and I never checked that. On checking the correct artifact: all four flagged slots (plus g11 l11 s5, g12 l02 s5) carry their options **only in the structured `choices[]` array with an empty `body`**, and the audit renderer parsed options out of `body` — so it emitted **0 options**. The student reported truthfully about what it saw.
- **Verified both paths:** student view = 0 options; pushed QTI = 6 `qti-simple-choice` (3 opts) each. So this is a **real defect in the audit lens**, not a ship defect (a Timeback student sees the options) and NOT a Fable hallucination.
- **Fixed** in `pipeline/lesson_review.py` (fall back to `choices[]` when `body` has no inline markers); regression test `pipeline/tests/test_student_view_options.py`; full sweep now 0/129 broken slots.
- **Lesson:** artifact-verification ≠ experience-verification. When a deterministic check and an agent disagree, find the mechanism (here: two renderers diverge) before ranking one over the other. See `SIM_STUDENT_FINDING_LEDGER.md`.

### ✅ REAL — Counterclaim required by the g9_l27 gate but never taught (Q3 + Q4, the eval's headline readiness gap)
Claim: no G9 lesson teaches naming/answering a counterclaim, yet the l27 argument gate requires it.
**Ground truth:** across ALL G9 v3.1 lessons, "counterclaim/counterargument" appears **only in l27 itself** (5×, as a required move); **0 mentions in l01–l26.** Confirmed. This also corroborates the earlier-this-session finding on the same gate (C904-0029). Nuance: G10 *opens* with counterclaim lessons (C1001), so the skill exists in the course — one grade too late for the G9 gate. **Genuine, high-severity. Fix: either teach counterclaim in G9 U4 before the gate, or drop the counterclaim requirement from the G9 gate to match what G9 teaches** (the latter is what the earlier C904-0029 fix already did to the gate's PP100 — verify the gate LESSON body matches).

### ⚠️ OVERSTATED — "g9_l07 repeats g9_l05, nothing new, even the same 76.9% phone source" (Q2, called the "most severe repeat")
**Ground truth:** related but NOT the same skill. l05 = "name your source: choose quote/paraphrase/summarize + attribution"; l07 = "fold the quote INTO your own sentence (integration)." Distinct SRSD sub-skills (attribution → integration). And they use **different sources** (l05: migration + school-lunch; l07: phoneban + water-cycle) — so the specific claim "even the same 76.9% phone source" is **false**. The cluster IS tightly related and can feel repetitive to a fast reader, but "nothing new taught" is exaggerated. **Partly real (tight sequencing), specific claims wrong.** Treat as a "consider consolidating/《differentiating the source-use cluster" signal, not a verified duplicate.

### ⚠️ NEEDS TRIAGE (not yet verified) — the two systemic Q1 patterns
These are the eval's most repeated flags; they are plausible and match known design choices, but I have NOT yet verified each instance:
- **"Checks that run themselves"** (prompt answers its own diagnostic before asking) — flagged across ~15 lessons. This overlaps the readiness-audit's "step gives away the answer" class, of which SOME were genuine (fixed this session in the 45-defect pass) and some were the coping-model design (a PROVIDED weak draft the check runs on, which is intentional per the expected-exception registry). **Must triage instance-by-instance: genuine give-away vs sanctioned coping-model.**
- **"Recognition not application: Step-4 MC correct answer = the Step-3 worked-example AFTER sentence verbatim"** — flagged across ~16 lessons. If true, the discrimination measures memory of a sentence read minutes earlier, not the skill. This is a REAL design-quality concern worth checking deterministically (compare each Step-4 correct option against the Step-3 AFTER text). **High-value to verify; likely partly real.**
- **"Identically named checklists ('the 3 questions' ×5)"** — plausible and matches the course's repeated 3-question framing; a naming/numbering fix (call them distinct tools) is cheap and sensible if confirmed. Overlaps AP One's misconception-taxonomy lesson (T1-C) — naming tools is the same discipline.
- **"Which ONE check did your rewrite fix" when a draft fails multiple** — plausible item-design nit; verify wording.
- **l13 Step 8 "use sequence signposts where the real relation is cause"** — a specific, checkable contradiction; verify (if real, it's a genuine correctness bug like the ones in the 45-defect pass).

### ⚠️ PLAUSIBLE — sequencing/redundancy structural flags (Q2, Q3)
- **l26 gate topic-reuse (3rd volcano lesson in a row → memorized, not cold)** — plausible and a real transfer-validity concern; verify the held-out gate source vs the preceding lessons' topics.
- **l25 "revise a 2-sentence paragraph right after two full essays" (mountain → tricycle)** — a real grain-regression smell; verify l25's terminal unit vs l23/l24.
- **l19 repeats l03 / l23 re-teaches 5 lessons / l24 repeats l23** — these are the "review before the capstone" lessons; some review is intentional SRSD, but the eval's "over-prepared, teach steps are 90% review" is a coherent signal worth weighing (it aligns with the F3 orphan-planning finding — the essay arc has redundant planning teaching).

---

## Bottom line for folding into the fix plan (later)
- **CORRECTION (2026-07-17):** the "blank MC steps" finding, first recorded as FALSE, is **REAL** — an audit-lens rendering bug (now fixed), not a Fable hallucination. The students were right. See the corrected verdict above and `SIM_STUDENT_FINDING_LEDGER.md`. This reversal is why the whole finding set was re-triaged against the correct artifact.
- **1 finding is REAL and high-severity** (counterclaim gap at the g9_l27 gate) — corroborated independently; already partially touched by the C904-0029 fix, needs the gate LESSON checked.
- **1 finding is OVERSTATED** (l07≠l05; specific "same source" claim false).
- **The rest need per-instance triage** — especially "recognition-not-application Step-4 MC" (deterministically checkable, likely partly real) and "checks that run themselves" (must separate genuine give-aways from sanctioned coping-models).
- **Method note:** because this is a Fable walk, apply the SAME triage discipline as the readiness audit — deterministic verification first, then adversarial check — before treating any finding as a fix item. Do NOT bulk-adopt the raw list.
