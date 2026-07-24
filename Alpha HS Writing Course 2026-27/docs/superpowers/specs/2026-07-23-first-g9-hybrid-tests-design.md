# First G9 Hybrid Tests: Assemble + Clean - Design

**Date:** 2026-07-23
**Status:** Design (awaiting user review)
**Scope:** produce 2 disjoint, gate-clean, student-shippable G9 test forms from the hybrid pipeline
(bake-off winner), with every Incept-origin item run through a pre-ship CLEANUP pipeline first. Output =
reviewable artifacts. NO grader-wiring, NO push (delivery is a separate later step on Noel's approval).

## Why

The deepened live bake-off (2026-07-23) found the HYBRID wins (89.2 > ours 79.4 > incept 76.03): Incept's
MC item-craft beat ours across editing/evidence subskills; ours owns constructed response (ECR + SCR) +
assembly. To ship the hybrid, the Incept-origin items that land on a form must first be made
student-safe - they currently carry em-dashes (house-rule violation), uncited/fabricated stats (fact-check
liability), no provenance/copyright record, and (for SCR) no model answer. That cleanup pipeline is the new
build; the hybrid selector, gates, and disjoint-form assembly already exist and are reused.

## Decisions (with the user)

1. **Source:** HYBRID (best gate-passing, highest-judged item per slot; includes Incept items).
2. **Cleanup steps (all 4 in scope):** em-dash strip + house-style; fact-verify (strip-or-flag); provenance +
   copyright screen; SCR model-answer fix.
3. **Fact-verification:** STRIP-OR-FLAG - remove/rewrite any unverifiable stat so the item is claim-safe;
   DROP the item if it cannot be made claim-safe. Default to DROP when uncertain (fail-safe).
4. **Batch:** 1 primary + 1 parallel retake = 2 disjoint forms (pool supports ~4).
5. **Delivery:** ASSEMBLE + CLEAN ONLY - produce cleaned forms + a review page. No grader-wiring, no push.

## Non-goals (deferred)

- Grader-wiring + live Timeback push (separate step, on approval; g9_wire_grader + g9_push_live already exist).
- Ours-only forms (the hybrid is the chosen source; ours items still flow through untouched).
- G10-12; more than 2 forms; student-outcome claims (needs a field test).
- Fixing Incept's generation shape upstream (we clean the OUTPUT here, not Incept's prompts).

## Architecture

```
  deepened hybrid pool (ours + Incept, from the bake-off / incept_pool)
                |
                v
  CLEANUP PIPELINE  (Incept-origin items only; ours pass through untouched)
     1. em-dash strip + house-style normalize
     2. fact-verify: strip/rewrite unverifiable stats -> DROP if not claim-safe
     3. provenance + copyright screen (content_screen): tag generated/model/date; REJECT third-party expression
     4. SCR model-answer fix: author a model answer if an Incept SCR is used, else DROP
     (each step is DROP-SAFE: returns a cleaner item or signals cannot-ship; short-circuit + log the reason)
                |
                v
  cleaned pool -> select_hybrid (existing) -> 2 disjoint forms (primary + parallel retake)
                |
                v
  qc_item re-check every selected item (fatal gates PASS + now em-dash-clean)
                |
                v
  artifacts: forms JSON + review HTML (per-item source, cleanup actions, provenance, cleanup ledger). NO push.
```

## Components

- `pipeline/incept_cleanup.py` - CREATE. Pure per-`Item` steps + orchestrator:
  - `_strip_em_dash(item) -> item` - replace `\u2014`/`\u2013` in stem/options/rationales/answer_key with
    house-style (comma/colon/paren); matches `item_contract.gate_no_em_dash`'s detection exactly.
  - `_fact_verify(item) -> (item | None, note)` - deterministic pattern-scan for factual claims/figures
    (digits, "percent|study|survey|data|% |in <year>"); strip/rewrite so the item carries no unverifiable
    stat; return None (drop) if it cannot be made claim-safe. Judgment calls may use an agent pass, defaulting
    to DROP when uncertain.
  - `_provenance_screen(item) -> (item | None, note)` - stamp provenance {generated:"incept", model, date,
    cleanup_actions}; run `content_screen.screen()`; return None if verdict==REJECT (third-party/bright-line).
  - `_fix_scr_model_answer(item) -> (item | None, note)` - if a `scr_writing` item lacks answer_key, author a
    model answer; else return None (drop) to satisfy the SCR schema gate.
  - `clean_item(item) -> (item | None, actions: list[str])` - ours-origin items pass through unchanged; Incept
    items run all 4 steps in order, short-circuiting to None on the first unrecoverable failure, accumulating
    an `actions` log (kept-with-actions or dropped-with-reason).
- `pipeline/first_tests_g9.py` - CREATE. Orchestrator:
  - load the deepened hybrid pool (incept_pool + our items, source-tagged);
  - `clean_item` each -> cleaned pool + a cleanup ledger (per Incept item: kept/dropped + reasons);
  - feed the cleaned pool to `bakeoff_hybrid.select_hybrid`-style selection for 2 DISJOINT forms (primary +
    retake); reuse the existing fail-loud short-slot guard;
  - `item_contract.qc_item` re-check every selected item (must PASS fatal gates + be em-dash-clean);
  - write `C:/tmp/first_tests_g9/forms.json` + `first_tests_g9.html` (per-item: source, cleanup actions,
    provenance, judge score; + the cleanup ledger). CLI `python pipeline/first_tests_g9.py`.
- `pipeline/tests/test_incept_cleanup.py` - CREATE. Offline-deterministic tests.

## Cleanup contract (drop-safe, logged)

Each step returns a cleaner item OR signals cannot-ship. `clean_item` short-circuits on the first
unrecoverable failure and records WHY (e.g. `"dropped: unverifiable stat '62-district study'"`). Nothing
ambiguous ships. The orchestrator emits a CLEANUP LEDGER accounting for every Incept item. Dropped Incept
items free their slot for the next-best eligible item (often ours); the `select_hybrid` fail-loud guard still
raises if a slot cannot fill after cleanup rather than shipping a short form.

## Testing & honest scope

- Offline-deterministic tests: em-dash strip clears all dashes; a fabricated-stat item is dropped or rewritten
  claim-free; a third-party-quote item is REJECTed by content_screen; an Incept SCR with no model answer is
  dropped unless one is authored; the orchestrator yields 2 disjoint forms where every item passes qc_item +
  is em-dash-clean; the cleanup ledger accounts for every Incept item.
- Fact-verification DETECTION is deterministic (pattern-scan); the JUDGMENT may use an agent pass, documented
  as non-deterministic and defaulting to DROP when uncertain (fail-safe) - so the tested path is deterministic.
- HONEST SCOPE: these are SHIP-READY ARTIFACTS, not pushed - the Timeback push is a separate later step on
  approval. Gate-clean + fact-safe + provenance-tagged is the strongest pre-ship bar we have; real quality is
  still only proven by a field test.

## Global constraints

- Offline/default path + all tests: Python 3 stdlib only, network-free, deterministic.
- Any agent-assisted fact-judgment is opt-in + defaults to DROP; the automated tests use the deterministic path.
- No em dashes in authored code/comments/docstrings (the cleanup PRODUCES em-dash-free items; the module's own
  source is em-dash-free too).
- Never log or persist any API key.
- Reuse (do not fork): `item_contract.qc_item`/`gate_no_em_dash`, `content_screen.screen`,
  `bakeoff_hybrid.select_hybrid`/`is_eligible`, `incept_pool.load_deepened_incept_pool`. No push code touched.
- DROP-SAFE + fail-loud: never ship a short form or an item that failed a cleanup step; log every drop.

## Risks / open items

- **Most Incept stats are fabricated** - fact-verify may DROP many Incept items. That is correct (no fabricated
  facts to students) and re-routes slots to ours; the ledger makes the drop rate visible. If drops leave a slot
  unfillable, fail loud (a real finding: that slot has no shippable Incept item + insufficient ours depth).
- **Em-dash rewrite must not change meaning** - use punctuation substitution only (comma/colon/paren/period),
  never drop content; a test asserts the rewrite preserves the option/answer text minus the dash.
- **Agent fact-judgment nondeterminism** - kept out of the automated suite; defaults to DROP; any agent pass is
  a documented operator step, not part of the deterministic build.
- **SCR model-answer authoring** - if we author a model answer for an Incept SCR, that answer is OURS
  (own-authored), tagged as such in provenance; the item is then a genuine hybrid artifact.
