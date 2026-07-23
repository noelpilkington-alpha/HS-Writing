# PP100 Form-Bank Design

**Date:** 2026-07-23
**Status:** Design (awaiting review before any authoring/build)
**Trigger:** Noel — each PP100 test-out currently has only ONE form; a test-out gate needs an equivalent-form
bank so retries are honest and non-repeating.

## The problem, stated precisely

Each lesson's PP100 mastery test-out is a **single-item assessment-test** pointing at **one authored FRQ**
(`<lesson>-MASTERY` -> `<lesson>-MASTERY-FRQ`). Verified: every mastery bank entry
(`mastery_prompts_g{9,10,11,12}.py`) has exactly one `prompt_html` + one held-out `source`. So the test-out
"bank" is a bank of one.

Why that breaks a test-out gate:
1. **Retries repeat the identical prompt.** A student who fails re-attempts the exact same task; they can
   iterate one answer toward a pass rather than demonstrate the skill on a fresh case.
2. **No equivalent forms exist.** The platform's mastery-gate retry contract expects
   `retry: same_or_equivalent_form` (Platform3 adapter, `push_targets.py`). With one form, "equivalent" is
   impossible.
3. **Seen-in-lesson leakage.** The single held-out source is fixed; once known, the one form is known.

This is not a content bug (the one form is correct and held-out); it is a **bank-depth** gap that must be
closed before real students hit the test-out.

## What "equivalent form" means here (the equivalence contract)

Two PP100 forms for a lesson are EQUIVALENT iff they hold constant:
- the **taught skill / move** (the lesson's target — e.g. "write one arguable claim: side + reason"),
- the **grain** (`unit`: sentence / paragraph / multi_paragraph / essay),
- the **rubric** (`rubric_ref`: rc.staar for G9/10, rc.4trait for G11/12) and its grader routing
  (`grain`, `frq_type`, and `mode` where applicable),
- the **cognitive demand** (a `writing` form stays writing; a `revision` form stays revision on a provided
  draft of comparable difficulty),
and VARY only:
- the **held-out source / topic** (a different stimulus the article never used),
- the surface wording of the task stem (mechanically parallel, not a harder/easier ask).

A form that changes the grain, rubric, or demand is NOT equivalent and must not enter the bank. This
equivalence contract is the spec's central invariant and the QC gate enforces it.

## Bank size — decided by evidence + constraints, NOT a guessed norm

There is NO documented PowerPath bank-depth standard (searched repo + timeback skill; none found). So size is
bounded by three real facts, not a number pulled from the air:

1. **A test-out needs at least one fresh retry form.** Minimum defensible depth to make a retry non-repeating
   is 2 (one shown attempt + one distinct retry). 3 gives a second retry before any repeat.
2. **Anti-over-coverage constraint (Alpha, Brainlift line ~4177).** The documented Alpha concern is PP100
   banks that OVER-cover — too many items relative to the core knowledge — inflating student testing time
   (Becky's diagnostic-algorithm BrainLift targets minimizing testing time). So "more forms" is a cost, not a
   free good; depth must be justified, not maximized.
3. **Source-pool ceiling.** Genuinely-equivalent forms require distinct held-out sources of the SAME topic
   family + grain. The current stimulus bank is finite: 83 stimuli (37 single, 16 issue_frame, 13 opposing, 7
   prompt_only, 5 synthesis_set, 4 perspective_set, 1 complementary). A lesson can only have as many equivalent
   forms as there are suitable distinct sources for its family; some families are thin (perspective_set = 4).

**Recommended target (for review): 3 equivalent forms per PP100**, one presented + two held for retries. Rationale:
satisfies the non-repeating-retry requirement with a margin, stays well under the over-coverage line (a
test-out is pass/fail, not a diagnostic sweep), and is achievable against the source pool for most families.
Escalate to 4 ONLY for the highest-stakes gate lessons (unit/course GATE) IF the source pool supports it.
Do NOT set a uniform 5 — there is no basis for it and it risks over-coverage + source exhaustion.

**Open question for Noel/platform:** does the PP100 runtime SELECT among bank forms randomly / per-attempt, or
does it just group links? The timeback skill documents the bank STRUCTURE (parent resource with
`metadata.resources:[ids]`, link only the bank) but NOT the selection semantics. If the runtime does not rotate
forms on retry, a bank buys us nothing and this whole effort should pause until that is confirmed. VERIFY FIRST.

## Delivery mechanism (platform-native, already documented)

Use the timeback **Assessment Bank Pattern** (create-course.md):
- For each lesson, create N variant sub-resources (`res-<lesson>-pp100-f1..fN`), each pointing at its own
  single-item mastery test (`<lesson>-MASTERY-f{k}` -> `<lesson>-MASTERY-FRQ-f{k}`).
- Create ONE parent bank resource `res-<lesson>-pp100` with `metadata.resources = [f1..fN ids]`.
- Link ONLY the bank resource to the topic (individual variants NOT linked directly — the documented
  "3 links per topic instead of 1" defect is exactly this).
- This REPLACES the current single-resource PP100 in `course_assemble_v3_1.py` (the PP100 CR points at the bank
  instead of one test). Backward-compatible fallback: a bank of 1 renders as today.

## Where the forms come from (source strategy)

Author each additional form by pairing the lesson's skill+grain+rubric with a DIFFERENT held-out source drawn
from the existing vetted stimulus bank, matched by topic family + grain — the SAME method the current single
form already uses (`mastery_prompts_g{N}` `source` + a cold instruction). Preferred order:
1. **Reuse vetted held-out sources** first (deterministic, no fabrication, already QC-passed). Cap = how many
   distinct suitable sources exist per family.
2. **Source new stimuli** only where a family is too thin to reach the target depth (a bounded sourcing task
   against the Source Cache, not free LLM fabrication). Flag which lessons need this.
3. LLM-drafting of the task STEM is fine (it is mechanically parallel to the existing stem); the SOURCE must be
   a real vetted stimulus, never invented (own-words / public-domain / federal rule still applies).

## QC gate (deterministic, blocks a form from entering the bank)

Each candidate form is gated on the equivalence contract:
- grain matches the lesson's mastery grain; rubric_ref matches; frq_type matches; mode matches (where set).
- held-out source EXISTS in the stimulus bank, is DISTINCT from every other form's source in this lesson, and
  is NOT the article's taught source (the existing gate_bank_partition rule).
- no em dash; source in Lexile band; stem is parallel (not a different/harder task).
- reuses `one_beat_extract`-style deterministic checks where applicable; new checks for source-distinctness.

## Module layout (build, after spec approval)

- Extend `mastery_prompts_g{N}.py`: each entry's value gains a `forms: [{source, prompt_html}, ...]` list
  (the current single `source`+`prompt_html` becomes `forms[0]`, so nothing regresses).
- `pp100_forms.py` (new): builds the per-lesson form list from the bank, runs the QC gate, reports coverage
  (which lessons hit target depth, which are source-limited).
- `course_push_mastery_v3_1.py`: push N FRQ items + N tests per lesson (one per form).
- `course_assemble_v3_1.py`: emit the parent bank resource + variant sub-resources; PP100 CR -> the bank.
- Tests: equivalence-contract QC, bank-structure assembly, coverage report, prod-safety (bank of 1 == today).

## Sequencing note (depends on the grader)

The grader currently mis-routes sentence/paragraph grains (Defect 1, findings doc) and is being fixed. Form
banks multiply the number of FRQs hitting the grader, so this build should land AFTER the grader grain-routing
fix is deployed and verified — otherwise we would be multiplying un-scorable items.

## Non-goals / guardrails

- Not a diagnostic item bank; PP100 is a pass/fail test-out. Depth serves honest retries, not coverage.
- No fabricated sources; equivalent forms reuse vetted stimuli or bounded new sourcing.
- Prod-safe: a lesson with only forms[0] behaves exactly as today (bank of 1).
- Confirm the runtime's form-selection semantics BEFORE authoring at scale.

## Decisions needed from Noel before build

1. Target depth (recommended 3; 4 for gate lessons if sources allow) — confirm or set.
2. Confirm the PP100 runtime rotates forms on retry (or how it selects) — the load-bearing platform fact.
3. OK to source new stimuli for thin families, or cap those lessons at whatever the pool supports.
