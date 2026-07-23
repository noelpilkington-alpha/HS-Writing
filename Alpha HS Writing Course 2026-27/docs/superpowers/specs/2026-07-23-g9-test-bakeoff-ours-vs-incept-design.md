# G9 Test Bake-Off: Our Pipeline vs. Incept — Design

**Date:** 2026-07-23
**Status:** Design (awaiting user review)
**Scope:** the ONE genuinely-new piece of the "establish G9-12 test format / pipeline / rubrics / grader"
request — a head-to-head comparison of our test-generation pipeline vs. Incept's, on G9, to decide which
produces the best standardized writing test. Format, rubrics, and grader already exist (see Context) and
feed in as the evaluation criteria; each gets its own short follow-up spec only if it needs changes.

## Context: what already exists (do NOT rebuild)

- **Format (per-grade blueprints, live in code):** G9 = 1 ECR + 3 SCR + 17 MC (writing-only, rebalanced
  2026-07-21); G10 = 1 ECR + 1 SCR + 25 revise/edit MC (STAAR EII); G11 = 4 essays; G12 = 3 AP-Lang FRQs.
  In `pipeline/render_model_tests.py` (G9/G11/G12) + `pipeline/assemble_test.py` (G10).
- **Rubrics (bake-off-validated 2026-07-21):** rc.sbac (G9/10 CCSS, winner), rc.staar (G9/10 exam-prep,
  route-aliased to the SBAC engine), rc.4trait (G11/12 Regents 4-criterion), rc.scr1/2/3 (SCR), plus
  sentence/paragraph bands. rc.ap deprecated -> 503.
- **Grader (live FastAPI):** `Writing_Test_Grader/api/external_score.py` `/score` ExternalApiScore endpoint,
  panel engines (panel_sbac, panel_ccss, panel_staar, panel_joey), grain routing (sentence/paragraph/essay).
  Wired to G9 items via `pipeline/g9_wire_grader.py`.
- **Incept integration (exists for other artifact types):** `incept_client.py` (auth + poll/fetch, needs
  `--ssl-no-revoke` on Windows), `incept_qc.py`, `incept_diagram.py`, `incept_video.py`, etc. **Test /
  test_spec generation is NOT integrated** — that is the new work here.

## Locked decisions (with the user)

1. **Win criterion:** rank on (a) blueprint fidelity to the grade's anchor exam, (b) % items passing our
   `item_contract` gates, (c) an LLM-judge quality/gradeability score.
2. **Grade scope:** G9 only for the first bake-off; clone to G10-12 after the harness + criteria are proven.
3. **Normalization:** a one-way adapter maps Incept test JSON -> our `Item` objects, so BOTH pipelines'
   output runs through the identical gates + judge.
4. **Gate weighting:** split FATAL (structural) vs FIXABLE (mechanical, e.g. em-dash) failures; rank on
   fatal-gate-pass + fidelity + judge; report fixable failures as a separate "post-processing cost" line.
5. **Judge hardening (author recommendation, accepted):** the judge runs 3 samples per item and takes the
   MEDIAN; the scorecard reports judge variance. Rationale: Incept's own judge was observed swinging ~17 pts
   run-to-run this session (the 209/219 non-deterministic "flagged" artifact); a single pass could hand the
   verdict to noise. Deterministic gate + fidelity metrics remain the primary rank; the median judge is a
   tie-breaker, not the decider.

## Goals

1. A reproducible harness that generates a full G9 test from BOTH pipelines against the same blueprint,
   normalizes both to `Item` objects, scores both on identical criteria, and emits a ranked verdict.
2. A defensible answer to "which pipeline produces the best standardized G9 writing test."
3. Reusable parts: the Incept test client + adapter become the ingestion path if Incept wins.

## Non-goals (deferred)

- G10-12 bake-offs (clone after G9 proves the harness).
- Format reconciliation across grades / making G10-12 writing-only (separate follow-up spec).
- Rubric changes (already decided) and grader changes (already live).
- Student-outcome / efficacy claims (needs a field test — this ranks test-artifact quality only).
- Auto-adopting the winner into production generation (a decision for after the verdict).

## Architecture & data flow

```
                    +- OURS:  render_model_tests.py G9 ---> our Item objects -+
G9 blueprint  ------+                                                          +--> GATE (item_contract,
(agreed shape)      +- INCEPT: incept_test (test_spec+test) --> adapter --> Item +      fatal|fixable split)
                                                                                        |
                                                                                        v
                                                                        JUDGE panel (3-sample median)
                                                                                        |
                                                                                        v
                            SCORECARD: fidelity . fatal-gate-pass . fixable-cost . judge-median+variance
                                                                                        |
                                                                                        v
                                                          VERDICT (ranked) + side-by-side HTML
```

## Components (files)

Flat `pipeline/*.py` convention; reuse `incept_client` + `incept_qc` patterns.

- `pipeline/incept_test.py` — CREATE. Generate a full G9 test via Incept: submit `test_spec` (grain=unit or
  grade_level) + `test` (purpose=mastery, structure=single, grade_levels=["g9"], subject="writing"), poll to
  `succeeded`, fetch artifact JSON. Reuses `incept_client` for auth/poll/fetch (mirrors `incept_video.py`).
  Caches raw JSON under `C:/tmp/incept_cache/` so a run is re-scoreable offline (no re-generation to re-judge).
- `pipeline/incept_test_adapter.py` — CREATE. `parse(incept_json) -> (list[Item], list[str] warnings)`. The
  one-way mapper (contract below). Does NOT strip em-dashes or fix leaks — faithful representation so gates
  measure the real artifact.
- `pipeline/bakeoff_judge.py` — CREATE. `judge_item(item, anchor_ctx, n=3) -> {median, samples, variance}`.
  ONE judge path used for BOTH pipelines (fairness). Prompt scores pedagogical quality + gradeability against
  the G9 anchor (STAAR English I). May call our own model and/or Incept QC-as-a-service; the SAME judge for both.
- `pipeline/bakeoff_g9.py` — CREATE. Orchestrator: load ours (`render_model_tests` G9) + Incept
  (generate -> adapt); run `item_contract.qc_item` on every item of both with the fatal/fixable classifier;
  run the judge; compute the scorecard; emit `C:/tmp/bakeoff_g9_scorecard.json` + `C:/tmp/bakeoff_g9.html`
  (side-by-side, reusing the earlier comparison-page style). Offline-re-scoreable from cached JSON.
- `pipeline/tests/test_bakeoff_adapter.py` — CREATE. Adapter + gate-classifier unit tests.

## Adapter contract (the load-bearing unit)

`incept_test_adapter.parse(incept_json) -> (list[Item], warnings)`:

- **MC item** -> `Item(family="SR", qti_type="choice")`. Options are bare strings in Incept output; assign
  synthetic A/B/C/D ids; resolve the correct id by matching option text == the Incept `answer` string (this
  exact text-match is the bug hit earlier this session when options were bare strings — it MUST be a unit
  test). `explanations{}` (keyed by option text) -> each `Option.rationale`. Map DOK/difficulty/standards
  from `metadata` into `provenance`.
- **SCR (2-pt)** -> `Item(family="SCR")`. Classify subtype by task shape: an evidence/analysis paragraph tied
  to the passage -> `scr_analysis` (rc.scr3); a repair/revision -> `scr_writing` (rc.scr1). Model answer ->
  `answer_key`; bound stimulus -> `stimulus_ref` for analysis (none for writing).
- **ECR essay** -> `Item(family="CR", qti_type="extended-text", subskill_or_mode="argument" or "explanatory")`.
  Shared op-ed stimulus -> `stimulus_ref`. Incept's model rubric is recorded in `provenance` but OUR rubric
  assignment (rc.staar/rc.sbac) is applied for scoring parity.
- **Unmappable field** -> appended to `warnings`, NEVER silently dropped, so the scorecard reports "N fields
  the adapter could not map" (an honesty signal + an Incept-shape-drift alarm).

## Scoring, fatal/fixable split, verdict

- **Gate run:** every `Item` (both pipelines) -> `item_contract.qc_item`. Classify each FAILING gate:
  - FATAL (structural): `distractor_integrity` (length leak / dup options), `schema` / answer-key mismatch,
    `scr_binding` / `cr_binding`, `scr_rubric` / `rubric_config`.
  - FIXABLE (mechanical): `no_em_dash`, formatting-only.
- **Fidelity:** compare each test's section makeup to the agreed G9 blueprint — section counts, item types,
  DOK tiering present, single-source ECR present, counterargument coverage present/absent (note: our audit
  found counterargument is assessed only inside the argument-ECR rubric across anchors, so ECR-embedded
  counts, a discrete MC counterargument item does not).
- **Judge:** per-item median of 3 samples (0-100) + variance; a test-level gradeability read.
- **Verdict formula (documented, reproducible):** primary rank = `fidelity_score` + `fatal_gate_pass_rate`
  + `judge_median_mean`. `fixable_failure_count` reported as a separate "post-processing cost" line, never
  in the primary rank. Judge variance reported so a close verdict is flagged as judge-noise-sensitive.
- **Outputs:** `bakeoff_g9_scorecard.json` (machine-readable, the full per-item breakdown) +
  `bakeoff_g9.html` (side-by-side render for human confirmation).

## Testing & honest scope

- Adapter unit tests: answer-key-by-text resolution (incl. the bare-string-options case), SCR/ECR subtype
  classification, warnings on unmappable fields, no-silent-drop.
- Gate-classifier test: a known length-leak item lands in FATAL; a known em-dash item lands in FIXABLE.
- Orchestrator smoke test: runs offline from a cached Incept JSON (no live API needed to re-score).
- **Honest scope:** ranks TEST-ARTIFACT quality (fidelity + gate + judge), NOT student outcomes. The judge
  is non-deterministic (Incept's own judge swung ~17 pts this session); the median + variance mitigate but do
  not eliminate this, so the deterministic gate + fidelity metrics are the primary rank and a close judge gap
  is reported as noise-sensitive, not decisive.

## Risks / open items

- **Incept generation latency/variance:** `test` runs took ~9-20 min and Incept's mastery/single form was
  only 8 items in the earlier eval. If Incept underperforms on item COUNT vs the blueprint, that is a real
  fidelity finding, not a harness bug — report it.
- **Adapter drift:** if Incept changes its output shape, the adapter's `warnings` list is the early alarm;
  the adapter test pins the shapes we rely on.
- **Judge fairness:** the SAME judge prompt + model must score both pipelines; any per-pipeline prompt
  difference invalidates the comparison. Enforced by a single `judge_item` used for both.
- **Live-key handling:** the Incept API key lives in `Incept/Incept Production details.md` (plaintext,
  untracked). `incept_test` must read it the same redaction-safe way `incept_client` already does; never log it.
