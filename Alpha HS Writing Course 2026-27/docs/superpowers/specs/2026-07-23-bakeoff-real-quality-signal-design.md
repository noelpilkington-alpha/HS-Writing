# Bake-Off Real Quality Signal - Design

**Date:** 2026-07-23
**Status:** Design (awaiting user review)
**Scope:** upgrade the G9 test bake-off's verdict from measuring *conformance* to measuring real
*test-item quality*, so a "which pipeline produces the highest-quality tests" verdict is trustworthy.
Builds on the bake-off harness shipped earlier today (commits 3345f09..0742d6d).

## Problem

The current verdict = `fidelity*25 + fatal_gate_pass*25 + heuristic_judge*25 + grader_discrimination*25`
(after the earlier fairness fixes). Two flaws for the stated goal (highest quality):

1. The live judge calls **Incept's** QC-as-a-service to score both pipelines - a competitor grading a
   contest it is in (house-style bias risk).
2. The "grader_discrimination" dimension is **circular and unfounded**: we author the model answer + weak
   foils ourselves and feed them to a generic rubric engine; a high-model / low-foil result proves the
   GRADER discriminates, not that the generated ITEM is good. And there is **no test-specific grading
   engine** for G9-12 generated tests - only generic rubric configs (panel_sbac/panel_ccss). Measuring
   "gradeability" this way tests a capability we do not have.

## Decisions (with the user)

1. **Neutral judge:** replace Incept-QC with OUR OWN Claude judge (same prompt + model for both pipelines).
2. **Drop grader-discrimination entirely** (circular + no test-specific grader). Fold *gradeability* in as a
   SUB-AXIS of the neutral Claude judge: "is this item's prompt specific enough and its expected response
   clear enough that a scorer could reliably separate a strong answer from a weak one?" - a design judgment,
   needs no grading engine, not circular.
3. **Verdict weights:** `fidelity*25 + fatal_gate_pass*25 + neutral_judge*50`. Quality stays 50% (the goal),
   carried by one REAL signal. Judge does not dominate (so one noisy LLM read cannot flip the winner alone);
   the two deterministic conformance signals are a reliable floor AND genuine quality prerequisites (a
   wrong-shape or leak-ridden test is a bad test regardless of item cleverness).
4. **Live run:** cache every live call to disk keyed by input, so runs are resumable and re-scoring is free.
   Incept *generation* stays the operator hand-off (submit -> poll -> pass artifact id); judge runs
   automatically over the cached test.

## Goals

1. The live verdict's quality half is a real, neutral, anchor-grounded pedagogical judgment - not a proxy,
   not the competitor's judge.
2. The harness stays offline-reproducible by default (the tested path); live is opt-in + resumable.
3. Honest scope preserved: ranks TEST-ARTIFACT quality, not student outcomes.

## Non-goals (deferred)

- A test-specific G9-12 grading engine (does not exist; not built here).
- Grading real student responses / any student-outcome claim (needs a field test with item statistics).
- G10-12 bake-offs; format reconciliation; adopting a winner into production generation.

## Architecture

```
                              +- fidelity (25) --------------- existing, count-aware, deterministic
  a G9 test (ours | Incept) --+- fatal_gate_pass (25) -------- existing, deterministic
                              +- NEUTRAL CLAUDE JUDGE (50) --- NEW: our anchored item-quality rubric,
                                                               incl. a gradeability sub-axis; same prompt
                                                               + model for BOTH pipelines; 3-sample median
```

The grader-discrimination dimension and the `bakeoff_grader.py` module from the prior design are NOT built.

## Components

- `pipeline/bakeoff_judge.py` - MODIFY. Keep the signature `judge_item(item, anchor, n=3, live=False,
  client=None) -> {median, samples, variance}`. Offline (default/tests) keeps the deterministic heuristic.
  LIVE path CHANGES: stop calling `InceptClient.qc`; instead call Claude directly via the grader's proven
  `grader/engine/client.py::create_client()` + `get_model()`. Build an anchor-grounded rubric prompt from the
  Item (stem, options, answer, rationales) scoring item-quality axes: (a) distractor plausibility, (b)
  discrimination (does it separate a skilled from an unskilled G9 student), (c) GRADEABILITY (prompt
  specific enough + expected response clear enough to score reliably), (d) fit to the G9 STAAR-English-I
  anchor. Return a 0-100 per sample; run n=3; median + real variance. SAME prompt+model for both pipelines
  (the fairness invariant). Cache each verdict keyed by (item id + rubric-version hash).
- `pipeline/bakeoff_g9.py` - MODIFY. Remove the grader-discrimination dimension and its scorecard fields.
  Verdict formula -> `fidelity*25 + fatal_gate_pass*25 + judge_median_mean/100*50`. Update `verdict.primary_rank`
  string + the HTML/CLI. Add a resumable disk-cache wrapper (under `C:/tmp/bakeoff_cache/`) around live
  calls. Offline default unchanged + fully deterministic.
- `pipeline/tests/test_bakeoff_adapter.py` - MODIFY. Update the verdict-formula test to the 25/25/50 weights;
  keep the offline judge determinism test. Remove/aged-out any grader-discrimination assertions (that
  dimension no longer exists). If the prior task already added grader-discrimination code/tests, delete them.

## Live-call caching

A small dict-on-disk cache under `C:/tmp/bakeoff_cache/` (JSON files keyed by a hash of the call input):
judge verdicts keyed by (item id + rubric-version). A killed or quota-limited run resumes without re-calling;
re-scoring an already-judged test is free. Incept generation is NOT auto-run live (the ~20-min async step
stays an operator hand-off via `INCEPT_ARTIFACT_ID`); the judge runs over whatever test JSON is loaded.

## Testing & honest scope

- Offline path stays network-free + deterministic: `judge_item(live=False)` returns the heuristic; the
  orchestrator's offline run is byte-reproducible. All unit tests run offline.
- The live Claude-judge path is documented + smoke-tested manually (needs `ANTHROPIC_API_KEY` / Bedrock),
  NOT in the automated suite.
- **Honest scope (restated in code + verdict):** even with a real neutral judge, this ranks TEST-ARTIFACT
  quality, not student outcomes. The judge is an LLM (noise mitigated by 3-sample median + variance report +
  close-margin flag), not ground truth. A field test with item statistics (p-value, point-biserial,
  distractor selection) remains the only real proof of item quality.

## Global constraints

- Offline/default path: Python 3 stdlib only (unchanged, tested path).
- LIVE judge path introduces an `anthropic` dependency (already used by the grader engine) - imported
  LAZILY inside the live branch so the offline path + test suite stay stdlib-only and network-free.
- No em dashes in any authored code/comments/docstrings.
- Never log or persist any API key (Anthropic or Incept); the judge reuses the grader's key handling.
- SAME judge prompt + model for both pipelines; any per-pipeline difference invalidates the comparison.
- The verdict's primary rank is `fidelity*25 + fatal_gate_pass*25 + neutral_judge*50`; fixable + excluded
  gate failures still reported SEPARATELY, never in the rank.

## Risks / open items

- **Judge noise at 50% weight:** mitigated by 3-sample median + variance reporting + flagging a close margin
  as noise-sensitive. If live variance is high, the deterministic 50% (fidelity + gate) is the tiebreaker.
- **Anthropic access in this repo:** the grader's `create_client()` handles direct-API vs Bedrock; the judge
  must not hardcode one. If neither is configured, the live judge fails LOUD (never silently falls back to
  the heuristic in live mode, which would masquerade a proxy as a real judge).
- **Rubric-version hash in the cache key:** if the judge rubric prompt changes, the cache must invalidate
  (stale verdicts would score old items against a new rubric) - hence keying on a rubric-version hash.
