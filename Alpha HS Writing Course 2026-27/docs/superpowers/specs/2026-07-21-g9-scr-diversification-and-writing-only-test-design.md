# G9 SCR Diversification + Writing-Only Test Rebalance — Design

**Date:** 2026-07-21
**Status:** Design (awaiting user review)
**Scope of this spec:** the three **G9** workstreams. The G10 `scr_analysis`/`scr_research`
item build is explicitly deferred to a follow-up spec (the shared item-contract SCR family is
built here because G9 needs it).

## Problem & motivation

A side-by-side comparison of our assembled G9 test vs. an Incept-generated test exposed that our
Short Constructed Response (SCR) bank is monotonous: 10 items, all one task type (modifier-repair).
Noel: "diversify the SCR bank a lot."

Two prior investigations reshaped a naive "add more SCRs" into this design:

1. **Cross-state SCR assessment** (AnchorSets/G10_anchor_forms.md + ReleasedTests/batch1-5): the
   anchor exams are **full ELA** (reading + writing). Their MCQ bulk is *reading comprehension*,
   which a **writing-only** test drops. Weighting must therefore be by **points**, not item count.
   Short-CR is really two species: (a) a STAAR **writing-domain** repair/revision SCR (0-1), and
   (b) a **short text-analysis / research** SCR (Regents Part 3, Keystone, SBAC) — the species we
   have zero coverage of.

2. **G9 course↔test coverage audit**: the pipeline's coverage tools pass structurally but are
   coverage-not-efficacy. The G9 course (26 v3.1 lessons, KCs C.9.01-06) tops out at a
   **single-source** essay. It does **not** teach counterclaim, text-dependent analysis, or
   cross-source synthesis — those are **intentional G10 deferrals** (C.10.01/02/03/06). Therefore a
   G9 writing-only test may only assess G9-taught skills, or a 90-100% mastery target is impossible.

**Decisions locked with Noel (2026-07-21):**
- G9 writing-only test assesses **G9-taught skills only**.
- `scr_analysis`/`scr_research` are still built, but as **G10** items on the G10 form (follow-up spec).
- Add a **counterclaim-recognition** beat to G9 (recognition only; full acknowledge+refute stays
  C.10.01/G10) to match the STAAR English I anchor ("counterargument expected grades 8-EII").
- New **SCR family** in the item contract; scored by **model answer + short-CR rubric**, grader-wired later.
- SCR items authored **in-repo through our gates** (no Incept; no em-dashes).

## Goals

1. G9 writing-only test is provably fair: it assesses only what G9 teaches, so 90-100% is a
   defensible target (pending efficacy field data, which remains out of scope).
2. Diversify the G9 writing-domain SCR (`scr_writing`, 0-1) beyond modifier-repair.
3. Close the G9 counterclaim-recognition gap against the STAAR anchor.
4. Rebalance the G9 test blueprint from inherited full-ELA bulk (25 MCQ / 1 SCR / 1 ECR) to a
   points-weighted writing-only shape.
5. Add the shared `SCR` family + gates + rubric configs to the item contract (reused by G10 later).

## Non-goals (deferred)

- G10 `scr_analysis` (0-3) / `scr_research` (0-2) item authoring — follow-up spec.
- Full counterclaim acknowledge+refute at G9 (stays C.10.01/G10).
- Grader wiring of the new rubric configs to the live scoring API (later grader pass).
- Efficacy validation / cut scores (needs a field test).
- G10/G11/G12 test rebalances.

## Design

### Component 1 — `SCR` family in `pipeline/item_contract.py`

A third family alongside `SR` and `CR`.

- `Family = Literal["SR", "CR", "SCR"]`
- SCR `qti_type` = `text-entry`; `subskill_or_mode` ∈ {`scr_writing`, `scr_analysis`, `scr_research`}.
- SCR carries: `answer_key` (a **model exemplar answer**, required), `rubric_ref` (a short-CR config),
  and `stimulus_ref` (**conditional** — see gates).
- The existing auto-keyed modifier items currently live in SR as subskill `scr`; they **migrate** to
  the SCR family as subtype `scr_writing`. Remove `scr` from `SR_SUBSKILLS`.

New/changed gates:
- `gate_scr_schema`: subtype valid, `qti_type == "text-entry"`, non-empty model `answer_key`.
- `gate_scr_binding` (**subtype-conditional**): `scr_analysis`/`scr_research` MUST bind a stimulus
  present in a Stimulus_Bank; `scr_writing` MUST NOT bind one (sentence-level).
- `gate_scr_rubric`: `rubric_ref` ∈ the short-CR configs (below); `scr_writing`→`rc.scr1`,
  `scr_analysis`→`rc.scr3`, `scr_research`→`rc.scr2`.
- Reused unchanged: `gate_acc_tags`, `gate_content`, `gate_no_em_dash`.
- `GATES` list gains SCR-aware dispatch; `qc_item` unchanged in shape (still returns pass + per-gate
  detail + first_failure). Each item file self-tests to `N/N PASS`.

### Component 2 — short-CR rubric configs

Add to `RUBRIC_CONFIGS` and the grader wire's `_RUBRIC_BLOCKS`:
- `rc.scr1` — writing-domain SCR, 0-1 (generic; STAAR writing SCR model).
- `rc.scr2` — research short-answer, 0-2 (SBAC model). *(defined now; used by G10 build)*
- `rc.scr3` — text-analysis SCR, 0-3 (Regents/Keystone model). *(defined now; used by G10 build)*

Configs are data-only in this spec; live grader wiring is deferred. `testbank_kc_crosscheck.py`'s
`KNOWN_RUBRICS` set is updated so the crosscheck still passes.

### Component 3 — G9 `scr_writing` bank (`Item_Bank_G9/scr_writing.py`)

~15-20 items, subtype `scr_writing`, 0-1, no stimulus. Task-type coverage:
- modifier-repair (migrate the 10 existing from `sr_scr_modifier.py`)
- sentence-combining
- precise word choice
- revise-for-cohesion
- add / sharpen a transition

Each: own-authored provenance, ACC.W + CCSS tags, model answer, `rubric_ref="rc.scr1"`. No em-dashes.
`sr_scr_modifier.py` retired (or reduced to a re-export shim) once migrated; update any importers.

### Component 4 — G9 counterclaim-recognition (teach-side)

A light lesson beat teaching students to **recognize and acknowledge** an opposing view (not refute).
Delivered as a G9 lesson slot addition (recognition only). This is what makes a counterclaim-recognition
**test item** fair. Exact lesson placement is an implementation-plan detail; design requirement =
the skill is taught before it is tested, and framed as recognition (full refutation remains G10).

### Component 5 — G9 test rebalance (`pipeline/assemble_test.py`)

Replace the inherited STAAR-full-ELA blueprint with a **points-weighted writing-only** G9 form:

| Tier | ~Items | ~Points | ~% points | Source |
|---|---|---|---|---|
| MCQ (evidence, organization, conventions, sentence + 1 counterclaim-recognition) | ~15-18 | ~16-18 | ~35-45% | existing SR banks + new recognition item |
| SCR (`scr_writing` 0-1) | ~2-4 | ~2-4 | ~10-15% | Component 3 |
| ECR (single-source essay) | 1 | ~10 | ~40-45% | existing cr_argument / cr_explanatory |

Weighting by points (the MC-cap principle), not item count. Assembler still proves disjoint parallel
forms; SCR pool of ~15-20 supports several disjoint forms. (The 6-SCR/2-per-type target applies to the
**G10** form in the follow-up spec, which has all three SCR types.)

## Data flow

ACC standard → G9 KC → G9 lesson (teaches skill, incl. counterclaim-recognition) → stimulus →
item (SR / SCR / CR), each gate-clean → `assemble_test.py` selects to the writing-only blueprint →
disjoint parallel forms. Every tested skill traces back to a G9 lesson that teaches it.

## Testing / verification

- Each new/changed item file self-tests: gate harness prints `N/N PASS`.
- `pipeline/item_contract.py` `__main__` self-test extended with an SCR example (all 3 subtypes).
- `assemble_test.py` validates blueprint conformance + disjointness on the new G9 form.
- `testbank_kc_crosscheck.py` + `kc_coverage_matrix.py` still PASS (no invented codes; the
  counterclaim-recognition skill has a G9 owner; every G9-tested skill is G9-taught).
- Regression: existing SR banks + G9 lessons still pass their own self-tests after `scr` migration.
- **Coverage, not efficacy** remains the honest ceiling: this proves the test only assesses G9-taught
  skills; it does not prove students hit 90-100% (that needs a field test).

## Risks / open items

- **`scr` → SCR migration**: any code importing `sr_scr_modifier` or filtering `SR_SUBSKILLS` for `scr`
  (e.g. coverage_matrix, assemble_test, grader wire) must be updated in lockstep. Enumerate importers
  in the plan.
- **Counterclaim-recognition placement**: which G9 lesson(s) gain the beat, and whether it needs its
  own lesson vs. a slot in an existing argument lesson — resolve in the plan.
- **ECR rubric for G9 single-source**: current cr_argument uses `rc.ohio`; confirm the G9 form's ECR
  rubric choice (rc.staar vs rc.ohio) during rebalance.
