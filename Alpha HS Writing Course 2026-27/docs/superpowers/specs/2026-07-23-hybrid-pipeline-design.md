# Hybrid Test Pipeline (best-item-wins) + 3-Way Bake-Off - Design

**Date:** 2026-07-23
**Status:** Design (awaiting user review)
**Scope:** build a G9 test form from the best available item per blueprint slot across BOTH pipelines
(ours + Incept-adapted), then measure whether the hybrid beats ours-only and Incept-only. Builds on the
bake-off harness + adapter + gates + neutral judge shipped earlier today.

## Why (evidence from the live run)

The live-judge bake-off (2026-07-23) found: our pipeline wins overall (rank 79.4 vs 65.57) but ONLY on the
deterministic half (fidelity 1.0 vs 0.381 - our complete 21-item form vs Incept's 8; fatal-gate 1.0 vs 0.75).
On the neutral live judge, INCEPT'S ITEM QUALITY BEAT OURS (74.6 vs 58.8). Reading: our pipeline builds
COMPLETE, well-formed TESTS; Incept writes individually STRONGER ITEMS but incomplete forms. The hybrid tests
whether "best item per slot, source-blind, gate-floored" captures both strengths.

## Decisions (with the user)

1. **Selection rule:** an item is ELIGIBLE only if its FATAL gates pass (length-leak, valid key/binding;
   em-dash is FIXABLE so allowed, carried with a strip-flag). Among eligible items, pick the HIGHEST
   judge-scored per blueprint slot, SOURCE-BLIND. Gate floor first, then judge-rank.
2. **Evaluation:** score the hybrid form through the IDENTICAL fidelity + fatal-gate + judge scorecard used
   for ours and Incept; emit a 3-way comparison (ours | incept | hybrid). Apples-to-apples with prior verdicts.

## The honest constraint (report, do not hide)

The Incept-adapted pool is only 8 items from the one cached test: 6 SR tagged "evidence" + 1 SCR
(scr_analysis) + 1 CR (argument). The G9 blueprint needs SR across FOUR subskills
(evidence/organization/conventions/sentence, counts 4/4/5/4) + 3 SCR + 1 ECR. So Incept can only COMPETE for
the MC-evidence, SCR, and ECR slots; organization/conventions/sentence have NO Incept candidates and stay
ours by necessity. The hybrid will be MOSTLY OURS, with Incept winning only the few slots where it has an
eligible, higher-judged item. This is a proof-of-concept of the MECHANISM, bounded by a thin single-test
Incept pool - NOT a full hybrid at scale. The scorecard MUST report per-slot source composition so this is
transparent.

## Goals

1. A source-blind, gate-floored, judge-ranked item selector that feeds the existing assembler.
2. A 3-way scorecard (ours | incept | hybrid) on the same metrics, with hybrid source-composition reported.
3. Reuse the shipped pieces; no new judge, no new gates, no assembler rewrite.

## Non-goals (deferred)

- Generating MORE Incept items to deepen the pool (would need live Incept generation across subskills; the
  8-item pool is the honest current input).
- G10-12 hybrids; adopting the hybrid into production; student-outcome claims (needs a field test).
- Auto-repair of fixable (em-dash) items - flagged, not stripped, in this pass.

## Architecture

```
  ours bank (21) -----+
                      +--> MERGE (source-tagged) --> GATE FILTER (fatal-pass only) --> JUDGE-RANK per slot
  Incept-adapted (8) -+                                                                      |
                                                                                             v
                                          per-slot highest eligible --> render_model_tests.assemble --> HYBRID form
                                                                                             |
                                                                                             v
                                            3-WAY bake-off scorecard (ours | incept | hybrid) + HTML
```

## Components

- `pipeline/bakeoff_hybrid.py` - CREATE:
  - `merged_pool() -> list[Item]`: `_load_our_g9_items()` (each tagged provenance source="ours") + the
    Incept-adapted items from `parse(load_cached_output_json())` (source="incept"). Tagging via a wrapper or
    an added `provenance["bakeoff_source"]` field, NOT by mutating the judge input (judge stays source-blind).
  - `eligible(items) -> list[Item]`: keep items whose FATAL gates pass. Uses `item_contract.qc_item` +
    `incept_test_adapter.classify_gate_failure(..., cross_pipeline=True)` for Incept items (excludes
    our-internal acc_tags/binding, consistent with the bake-off) and `cross_pipeline=False` for ours.
  - `build_hybrid_pool(live) -> dict[section -> ranked list[Item]]`: for each blueprint section, gather
    eligible items matching its family+subskill/mode, judge-rank them (highest median first), source-blind.
  - `assemble_hybrid(live) -> form`: feed the ranked pool to `render_model_tests.assemble`-style selection
    (reuse its `_pool`/blueprint mechanics by supplying our merged ranked pool). Produce the hybrid form +
    a per-slot source map (which source won each slot).
  - `run_3way(live=False) -> dict`: score ours, incept, hybrid through the same
    `bakeoff_g9._score_side` + `_fidelity` + rank(25/25/50); write `C:/tmp/bakeoff_3way_scorecard.json` +
    `.html`; include the hybrid source composition ("N of M slots from incept").
  - CLI: `python pipeline/bakeoff_hybrid.py [--live]`.
- `pipeline/tests/test_bakeoff_hybrid.py` - CREATE. Offline-deterministic tests.

## Testing & honest scope

- Offline tests: merge tags sources; `eligible` drops a known length-leak item; within a slot a higher-judged
  eligible item outranks a lower one (source-blind); hybrid assembles to fidelity 1.0; `run_3way` returns all
  three entries + a source-composition field; hybrid never contains a fatal-gate-failing item.
- Offline judge is the deterministic heuristic (reproducible); `--live` uses the neutral Claude judge
  (cached/resumable), same as the bake-off.
- HONEST SCOPE: ranks TEST-ARTIFACT quality, not student outcomes. The hybrid's Incept share is capped by the
  8-item pool (a SCALE limit, reported per-slot, not a quality ceiling claim). Judge noise (live per-item
  stdev ~14-23 pts) carries over; the deterministic fidelity+gate half keeps the verdict stable.

## Global constraints

- Offline/default path + all tests: Python 3 stdlib only, network-free, deterministic.
- `anthropic` used only on the live judge path (via the existing `bakeoff_judge`), imported lazily there.
- No em dashes in authored code/comments/docstrings.
- Never log or persist any API key.
- The judge must stay SOURCE-BLIND: selection ranks by judge score without the judge seeing which pipeline
  authored an item (source tag lives in provenance, NOT in the judge prompt).
- Verdict metric unchanged: fidelity*25 + fatal_gate_pass*25 + judge_median_mean/100*50; fixable + excluded
  reported separately.

## Risks / open items

- **Thin Incept pool** (8 items, mostly "evidence"): the hybrid is mostly ours; the finding is the MECHANISM
  works + which slots Incept wins, not a scaled quality delta. Explicitly reported.
- **Assembler reuse:** `render_model_tests.assemble` loads items via its own `_load_items` (grade bank glob).
  The hybrid must inject its MERGED+RANKED pool instead - either a thin parameter/hook or a local reimpl of
  the same select-to-blueprint logic. Prefer a small local selector that reuses `_pool`/`BLUEPRINTS` so the
  committed assembler is not disturbed.
- **Judge noise:** a close ours-vs-hybrid gap will be within judge noise; report variance + flag close margins.
