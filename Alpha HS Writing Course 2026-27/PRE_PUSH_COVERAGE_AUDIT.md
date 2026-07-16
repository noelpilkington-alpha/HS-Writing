# Pre-Push Coverage-Gap Audit — G9 pilot

**Date:** 2026-07-16
**Scope audited:** the G9 course (27 lessons) as the first push to Timeback.
**Method:** enumerate every dimension along which a lesson/course can fail, cross each against what our stack *actually* verifies, and rank the UNCHECKED dimensions by push risk. "Everything we check passes" ≠ "nothing is unchecked." Each finding below is grounded in a code/data check, not a guess.

**Bottom line:** G9 is in good shape on pedagogy + rendering + platform-XML (the push path exists and dry-runs clean). The go/no-go hinges on **one high-severity gap** (an unwired anti-fabrication check with 8 stimuli carrying unverified figures) and **one medium gap** (FRQ auto-scoring not wired). Neither is a lesson-quality problem; both are pipeline-wiring problems.

---

## Coverage matrix

| # | Dimension | Checked by | Status | Severity |
|---|---|---|---|---|
| 1 | Lesson pedagogy / SRSD shell / discrimination / grain | Tier A contract (26 gates) | ✅ 27/27 | — |
| 2 | Rendered artifact fidelity (options, placeholders, walls) | render_qc | ✅ | — |
| 3 | Register / childish openers / leaked jargon | register gate (lessons + stimulus passages) | ✅ | — |
| 4 | Mastery genre-match + Webb DOK | mastery_genre gate | ✅ 0 flags | — |
| 5 | Semantic defects (also-correct, phantom-draft, planner-grain) | Tier B Fable judge + calibration | ✅ calibrated | — |
| 6 | Diagnosis-after-write ordering | new gate + fixture | ✅ | — |
| 7 | Timeback QTI/XHTML (table-in-`<p>`, void self-close, namespace, 409) | g9_push_live sanitize+validate | ✅ dry-clean (646 objects) | — |
| 8 | Copyright / verbatim-PD posture | provenance gate + PD documentation | ✅ | — |
| **9** | **Fact verification (anti-fabrication)** | verify_facts → receipt → gate_fact_sources | ⚠️ **NOT WIRED + 8 G9 stimuli unverified** | **HIGH** |
| **10** | **FRQ auto-scoring (grader wired)** | g9_wire_grader | ⚠️ **exists but not attached; FRQs live as un-scored** | **MEDIUM** |
| 11 | Cross-lesson coherence (progression, dup skills, mnemonic consistency) | — | ❌ per-lesson only, no course-level check | LOW-MED |
| 12 | Accessibility (SVG alt-text, reading load, color-only cues) | — | ❌ not checked | LOW |
| 13 | Push idempotency / re-push safety / rollback | g9_push_live (409-as-success) | ✅ handled | — |
| 14 | Answer-key correctness on MCQ discriminations (beyond structure) | Tier B judge (spot) + contract | ⚠️ structural only; semantic key-correctness not swept course-wide | LOW-MED |

---

## The gaps that matter for a G9 push

### GAP 9 — Anti-fabrication check is not wired, and 8 G9 stimuli carry unverified figures  ·  **HIGH**

**Evidence.** `gate_fact_sources` reads a receipt at `pipeline/fact_verification.json`; the only receipt on disk is at `pipeline/_fact_verify/fact_verification.json` — **wrong path, so the check never fires in the QC run.** The gate currently passes on well-*formed* rows without confirming the figure is on the cited page.

Of the 25 stimuli G9 binds, **8 have figure rows the last verify pass (2026-07-14) marked "figure not on page (fabrication risk)":**

| Stimulus | Unverified figures | Reason |
|---|---|---|
| ARG-LESSON-PHONEBAN | 76.9%, 90.9%, 65.8% | verbatim + figure not found on page |
| INFO-LESSON-HIGHWAYS | 48,890 miles, 25% | verbatim + figure not found |
| ARG-LESSON-AIWORKFORCE | 3.1% / 5.2M, 33.5%, 19.7% | not found |
| ARG-LESSON-GRIDSPENDING | 43%, 16%, 10% | not found |
| INFO-LESSON-ENERGYMIX | 43%, 16%, 10% | not found |
| INFO-LESSON-WATER-CYCLE | 2 rows | not found |
| INFO-LESSON-RECYCLING | 1 row | verbatim not found |
| INFO-LESSON-VOLCANOES | 1 row | verbatim not found |

**Why it matters for a push:** these are student-facing numbers presented as fact. "Not on page" has three possible causes — genuine fabrication, source page drift since authoring, or a stale/wrong-URL verify run. All three are unresolved. This is the anti-fabrication control the whole `fact_sources` design exists for, and it is currently dark.

**Work to close (must-do before push):**
1. Wire the receipt into the gate's read path (symlink/copy `_fact_verify/fact_verification.json` → `pipeline/fact_verification.json`, or point the gate at the real path) so `gate_fact_sources` actually enforces it.
2. Re-run `verify_facts.py --grade G9` fresh (the receipt is 2 days stale) to separate real fabrication from source-drift/URL issues.
3. Triage each surviving unverified row: fix the figure, fix the citation URL, or reword to remove the unbacked number. Re-verify to green.
4. Add the wired fact-receipt check to the Tier-A runner so it can never go dark again.

### GAP 10 — FRQ auto-scoring not wired  ·  **MEDIUM**

**Evidence.** `g9_wire_grader.py` exists but FRQs are live as basic extended-text that *accept* responses without auto-scoring; the grader URL (`hs-writing-grading.onrender.com`) is not attached. rubricBlock/ExternalApiScore config is ready but unapplied.

**Why it matters:** students can submit the terminal writes, but nothing scores them, so PP100 mastery and the gate produce no signal. Whether this blocks *this* push depends on intent: a "content-live, scoring-next" pilot can ship without it; a "students get graded" pilot cannot.

**Work to close:** deploy/confirm the grader endpoint, run `g9_wire_grader.py --live` (GET→add config→PUT, preserving content per Timeback RULE 3), spot-check one scored response end-to-end.

### GAP 11 / 14 — course-level coherence + semantic key-correctness  ·  **LOW-MED**

No course-level check that the G9 skill sequence builds coherently (per-lesson gates only), and MCQ answer-key *correctness* is verified structurally + by Tier-B spot checks, not swept across all G9 discriminations. Lower risk (the Council/audit already reviewed sequence design), but a one-shot Fable sweep over every G9 discrimination key would close #14 cheaply.

### GAP 12 — accessibility  ·  **LOW**

Inline-SVG diagrams and color cues aren't checked for alt-text / color-independent meaning. Not a blocker for a pilot; worth a pass before scale.

---

## Recommendation

**Do not push until GAP 9 is resolved** — it's the one gap that is both high-severity (student-facing fabrication risk) and currently *silently unchecked*. It's also cheap: wire the receipt, re-run verify_facts, triage ~15 rows.

**Decide GAP 10 by push intent:** content-preview push can proceed without the grader; a graded pilot needs it wired first.

GAPs 11/12/14 are safe to defer to a fast-follow, but note them so they're not silently assumed covered.

**Suggested sequence:** wire + re-run fact verification (Gap 9) → decide grader (Gap 10) → optional one-shot G9 discrimination-key Fable sweep (Gap 14) → re-run `tier_a_regression.py G9` + full suite → push G9 on your go.
