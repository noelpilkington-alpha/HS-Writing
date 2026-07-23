# Incept Pool-Deepening for the Hybrid Bake-Off - Design

**Date:** 2026-07-23
**Status:** Design (awaiting user review)
**Scope:** generate Incept items across ALL 6 G9 blueprint slot-types so the hybrid pipeline can contest
every slot at depth, then re-run the 3-way bake-off on the deepened pool. Builds on the hybrid pipeline
(bakeoff_hybrid.py) + adapter + neutral judge shipped earlier today.

## Why

The live 3-way run (2026-07-23) showed the HYBRID WINS (81.05 > ours 79.4 > incept 65.57) - but bounded by a
thin Incept pool: 8 items from one cached test, almost all "evidence"-tagged. Incept could only contest 2 of
6 slot-types (MC-evidence + ECR); org/conventions/sentence/SCR had NO Incept candidates, so the hybrid was
mostly ours by AVAILABILITY, not merit. This step deepens the Incept pool across all 6 slot-types so the
hybrid contest is real everywhere, and we learn Incept's item quality PER subskill.

## Decisions (with the user)

1. **Scope: all 6 slot-types**, including conventions + sentence (see the scope caveat below).
2. **Volume:** one targeted Incept bank PER slot-type, count ~10 (~60 items total).
3. **Subskill mapping:** stamp each item with the intended subskill of the bank that produced it (we generate
   one bank per subskill on purpose), NOT content-inference. Deterministic; a QC/judge pass catches misfits.
4. **Live generation caching:** each generated bank fetched once and cached to `C:/tmp/incept_pool/<subskill>.json`;
   downstream loads from cache; the deepened bake-off is offline-reproducible. Generation is a one-time
   operator step (submit 6 -> poll -> fetch -> cache), mirroring the existing incept_test cache pattern.

## Scope caveat (state plainly; do NOT let this be mistaken for a course change)

Conventions + sentence-mechanics are EXTERNAL_OWNED in `course_sequence_g9_12.py` (EGUMPP + AlphaWrite own the
TEACHING; the writing test only MEASURES them). Deepening Incept across those two slots is a GENERATOR-CAPABILITY
SHOOT-OFF - "can Incept produce good items for these skills?" - NOT a decision to have the writing course own or
ship conventions/sentence content. Nothing here pushes Incept items into the course. The boundary stays: the
writing course owns composition (claim/evidence/reasoning/organization/essay); conventions/sentence remain
app-owned. This spec deepens the BAKE-OFF's input pool only.

## Goals

1. ~60 Incept items across the 6 G9 slot-types, cached + offline-reusable.
2. The hybrid can contest every slot; re-run the 3-way bake-off on the deepened pool.
3. Report Incept item quality PER subskill (it may excel at evidence and be weak at conventions - a finding).

## Non-goals (deferred)

- Shipping any Incept item into the G9 course (bake-off input only).
- Changing course ownership of conventions/sentence (they stay app-owned).
- Multiple disjoint hybrid forms / G10-12 / student-outcome claims (needs a field test).
- Auto-repair of fixable (em-dash) items - flagged, not stripped.

## Architecture

```
  6 targeted Incept bank calls (one per subskill, count~10):
    evidence, organization, conventions, sentence (question/MC bank);
    scr_writing (question/text_entry or article SCR); ECR-argument (test/article CR)
                          |  live, async ~3min each; submit -> poll -> fetch
                          v
    cache each bank -> C:/tmp/incept_pool/<subskill>.json  (resumable, offline-reusable)
                          v
    adapter parse -> Item objects, STAMP subskill_or_mode = bank's intended subskill
                          v
    deepened Incept pool (~60 items / 6 subskills) --> bakeoff_hybrid.merged_pool(deepened=True)
                          v
    re-run 3-way bake-off (ours | incept-deepened | hybrid) - every slot now contested
```

## Components

- `pipeline/incept_pool.py` - CREATE:
  - `SUBSKILL_PROMPTS: dict[str, dict]` - 6 entries keyed by our subskill (evidence, organization,
    conventions, sentence, scr_writing, argument), each: `{prompt, generation_type, options}`. Prompts
    engineered to elicit that subskill at G9 (English I) level. SR subskills -> `question` MC bank
    (structure=bank, interaction_type=multiple_choice, count 10); scr_writing -> `question` text_entry (or
    the SCR shape); argument -> a source-based CR prompt.
  - `generate_pool(live=False, client=None) -> dict[subskill -> request_info]` - submit the 6 calls via
    `InceptClient.generate`; returns request/status info. Live = operator step (async).
  - `fetch_pool(artifact_ids: dict, live=False, client=None) -> dict[subskill -> output_json]` - fetch each
    artifact, cache to `C:/tmp/incept_pool/<subskill>.json`. (Operator passes the succeeded artifact ids,
    mirroring incept_test's INCEPT_ARTIFACT_ID hand-off.)
  - `load_deepened_incept_pool(cache_dir="C:/tmp/incept_pool") -> list[Item]` - read the 6 cached bank JSONs,
    parse each via `incept_test_adapter.parse`, STAMP `item.subskill_or_mode` = the bank's intended subskill
    and set the right family (SR/SCR/CR) + rubric_ref, tag `provenance["bakeoff_source"]="incept"`. Returns
    the merged pool. Missing cache files -> a clear error listing which subskills are missing (not a silent
    partial pool).
- `pipeline/bakeoff_hybrid.py` - MODIFY (small, back-compatible): `merged_pool(deepened=False)` - when
  `deepened=True`, pull Incept items from `incept_pool.load_deepened_incept_pool()` instead of the single
  cached test; default `False` keeps the existing 8-item behavior so current tests/verdicts are unchanged.
  `select_hybrid` / `run_3way` gain a pass-through `deepened=False` param.
- `pipeline/tests/test_incept_pool.py` - CREATE. Offline-deterministic tests against small cached FIXTURE
  banks (committed or generated into C:/tmp by a test fixture builder), NOT live.

## Testing & honest scope

- Offline tests: each fixture bank parses; items are stamped with the correct subskill + family + rubric;
  `load_deepened_incept_pool` returns items across all 6 subskills; missing-cache raises a clear error;
  `merged_pool(deepened=True)` yields ours + the deepened Incept pool; `merged_pool()` (default) is unchanged.
- The deepened 3-way run is offline-reproducible once the 6 banks are cached (judge offline = deterministic
  heuristic; `--live` uses the neutral Claude judge, cached/resumable as before).
- Live generation (the 6 Incept calls) is a documented one-time operator step, NOT in the automated suite.
- HONEST SCOPE: ranks TEST-ARTIFACT quality, not student outcomes. Per-subskill Incept quality is a REPORTED
  FINDING (Incept may generate strong evidence items and weak conventions ones). The deepened pool tests the
  hybrid mechanism at depth; a field test remains the only proof of student-facing quality. Conventions/
  sentence deepening is a generator shoot-out, not a course-scope change (see caveat).

## Global constraints

- Offline/default path + all tests: Python 3 stdlib only, network-free, deterministic.
- `anthropic` only on the live judge path (via the existing bakeoff_judge), lazy. Incept calls go through
  `InceptClient` (curl --ssl-no-revoke, key redaction); never log a key.
- No em dashes in authored code/comments/docstrings.
- The judge stays SOURCE-BLIND: subskill/source tags live in the Item, never in the judge prompt.
- The default `merged_pool()` (8-item) behavior + all existing bake-off verdicts stay UNCHANGED (deepening
  is opt-in via `deepened=True`).

## Risks / open items

- **Incept off-prompt drift:** a bank generated "for organization" may contain items that are really
  evidence/other. We stamp by intent (deterministic) but a QC/judge pass should flag misfits; report any bank
  whose items the judge rates poorly as a per-subskill quality finding, not a silent pass.
- **Family/type per subskill:** SR subskills map to `question` MC banks; scr_writing + ECR need the right
  family + rubric on stamp. The loader must set family (SR/SCR/CR), qti_type, and rubric_ref consistently so
  the items pass our gates and match blueprint slots (verify against item_contract on the first fetched bank).
- **Live quota/latency:** 6 async calls ~3min each + judge cost on ~60 items x3 live samples. Caching makes
  it one-time; the plan runs generation as an operator step and everything else offline.
- **Slot over-supply:** ~10 Incept per subskill vs blueprint counts of 4-5 means real contests everywhere;
  the hybrid selector already handles surplus (ranks + takes count). No change needed.
