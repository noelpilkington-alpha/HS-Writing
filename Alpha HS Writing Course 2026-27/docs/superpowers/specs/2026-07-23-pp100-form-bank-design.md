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

### Empirical probe result (2026-07-23) — bank STRUCTURE confirmed; runtime SELECTION still unverified

Ran an isolated live probe (all `TEST-PP100PROBE-*` ids, since deleted — env clean). Findings:

- **CONFIRMED (data layer):** the API accepts a bank resource with `metadata.selectionCount: 1` +
  `metadata.resources: ["TEST-A","TEST-B"]` (201) and PERSISTS both fields intact on read-back. So the
  Assessment Bank Pattern is real on the live API, not just docs. Two variant single-item tests + their FRQ
  items also created cleanly. `vendorResourceId` is REQUIRED on the bank resource (a 422 otherwise — that was
  the initial probe error, unrelated to the bank fields).
- **NEGATIVE (test-level selection):** a single assessment-test carrying a section-level `qti-selection`
  {select:1} / `selectionCount` was accepted, but the API SILENTLY DROPPED the selection directive — the
  stored test kept both item-refs with NO select. So "pick 1 of N inside one test" is NOT the mechanism; the
  pool + selectionCount must live on the BANK RESOURCE, not the test.
- **STILL UNVERIFIED (runtime rendering):** whether the student runtime actually serves a DIFFERENT form per
  attempt cannot be observed from the anonymous LearnWith player — loading a raw QTI test/bank URL directly
  returns `401` (the player only anonymously fetches `kind=text` article `contentUrl`s from CloudFront/Vercel;
  QTI tests are delivered only INSIDE a course through the AUTHENTICATED student runtime). To observe selection
  behavior we would need the bank wired into a course component and delivered through an authenticated student
  session (a heavier live experiment, or a direct platform-team answer).

**Net:** the bank structure is proven to store; the selection-on-retry behavior is a platform-runtime property
we still need confirmed (authenticated student-runtime observation, or a platform-team answer). The build can
proceed to STAGE the banks (structure is known-good) but must not be presented as "rotating on retry" until the
runtime behavior is confirmed.

### Timeback Documentation review (2026-07-23) — reframes the mechanism

Read the project's Timeback docs (`HS Writing/Timeback documentation/timeback-api-guide.md`, `qti-api.yaml`,
`oneroster-api.yaml`; `Writing Custom Courses/Timeback documentation/alphatest-claude-code-context.md`). Key
findings that change the design:

1. **PP100 is driven by the PowerPath ENGINE, not by QTI test structure** (api-guide §7): "PP100 is not a
   separate content type... the PowerPath engine handles the adaptive behavior." So retry/attempt behavior is a
   PowerPath-layer concern, not something a QTI `selectionCount` on the test controls.
2. **`FastFailConfig` reveals the real PP100 model** (oneroster-api.yaml `FastFailConfig`): PP100 adapts at the
   QUESTION level WITHIN one test — `consecutive_failures` (e.g. 3 wrong in a row) and `stagnation_limit`
   (e.g. 5 questions without score improvement) auto-finalize an attempt. This is a **question-pool-in-one-test**
   mastery model (serve questions until pass or fast-fail), NOT a "rotate across separate equivalent essay
   forms" model. Implication for a WRITING PP100: the natural fit may be a POOL OF FRQ FORMS INSIDE ONE PP100
   test that the engine draws from across attempts, rather than N separate single-item tests behind a bank
   resource.
3. **`selectionCount`/`qti-selection` are NOT in the formal QTI spec** (grep of qti-api.yaml: absent) — they are
   Timeback metadata conventions. Consistent with the probe: the field persisted on the RESOURCE but was
   dropped from the TEST. So if selection happens, it is a PowerPath/Timeback behavior over the resource-level
   pool, not QTI-standard test selection.
4. **`assessment-bank` is the correct resource type** (api-guide "Handling Assessment Banks"):
   `metadata.type == "assessment-bank"`, `resources: [test-id...]`. My probe used `type:"qti"` — for a real
   bank use `type:"assessment-bank"`.
5. **A delivery-layer rotation exists too** (alphatest "Assignment Variants" v4/v5): "assigns FIRST UNTAKEN test
   for grade/subject", and "completed or abandoned assignments can be reassigned." So at the assignment layer,
   the platform can hand out an untaken form from a set. This is a SECOND possible rotation mechanism, at the
   MasteryTrack/alphatest delivery layer, distinct from in-course PowerPath.

**Revised understanding of the options for "more forms":**
- **(a) Question-pool inside one PP100 test** — put multiple FRQ forms as items in ONE test; let the PowerPath
  engine + FastFailConfig serve/adapt. Closest to the documented PP100 model. Needs: confirm the engine serves
  a DIFFERENT FRQ across attempts (vs re-serving the same first item).
- **(b) assessment-bank resource over N single-item tests** — the bank pattern (probe-confirmed to store). Needs:
  confirm PowerPath/runtime picks among them per attempt.
- **(c) alphatest delivery "first untaken"** — a delivery-layer assign of an untaken form. Different integration
  surface (the alphatest assign API), likely not how the in-course student runtime already delivers our PP100s.

**All three still require the SAME unanswered fact:** does the engine actually serve a different form on a
retry? The docs describe mechanisms but none states the retry-form-selection behavior explicitly. The cleanest
remaining path to certainty is a PLATFORM-TEAM ANSWER (the PowerPath API is a separate service,
`api.alpha-1edtech.ai/scalar?api=powerpath-api`, whose attempt/next-question semantics are not in these docs),
or an authenticated student-runtime observation. HOLD bank-depth + build until this is answered.

### ANSWERED (2026-07-23) — PowerPath API spec confirms round-robin form rotation on retry

Fetched the PowerPath OpenAPI spec (`GET api.alpha-1edtech.ai/powerpath/openapi.yaml`, authed, 352KB). The
`/powerpath/createNewAttempt` endpoint states the behavior VERBATIM:

> "For Assessment Bank lessons: ... If the lesson is taken again by the student, a different test may be served
> ... The sub-test is determined using **round-robin logic over the sub-resources of the lesson's Assessment
> Bank Resource object**. So for example, if a lesson configures 2 sub-tests, the first attempt serves test 1,
> the second attempt serves test 2, the third attempt serves test 1 again, and so on."

This RESOLVES the design. The decided mechanism + semantics:

- **Mechanism = Assessment Bank (option b), NOT question-pool-in-one-test (option a).** The engine rotates over
  the SUB-RESOURCES of an `assessment-bank` Resource, one whole test per attempt. So each PP100 form is its own
  single-item test, and the lesson's PP100 ComponentResource points at an `assessment-bank` Resource whose
  `resources: [<form-test ids>]`. (`getNextQuestion` serves questions one at a time WITHIN the currently-served
  test; `createNewAttempt` picks WHICH test for the new attempt.) The `type:"assessment-bank"` value from the
  api-guide is the correct resource type (probe used type:"qti").
- **Selection = ROUND-ROBIN, deterministic, by attempt number** (not random). Attempt 1 -> form 1, attempt 2 ->
  form 2, ... attempt N+1 wraps to form 1. `createNewAttempt` only issues a new attempt when the current one is
  completed.
- **Retries are gated by attempt completion; `resetAttempt` soft-deletes responses + zeroes the score** (a
  reset, distinct from a new attempt). No documented hard attempt cap in these endpoints.
- **A single-test PP100 (our CURRENT shape) does NOT rotate** — a retake re-serves the same one test. This is
  exactly the gap Noel flagged; the fix is to convert each lesson's PP100 into an assessment-bank of N form-tests.

**Bank-depth is now a clean decision:** with round-robin, depth N = "a student sees a form again only on attempt
N+1." So depth is chosen by "how many distinct attempts before repeat is acceptable," bounded by the
anti-over-coverage concern and the source pool. The spec's recommended **3** means a form repeats only on the
4th attempt — ample for an honest test-out. (Depth can now be SET; the runtime unknown that blocked it is
resolved.)

### Build shape (decided, ready after grader fix)

Per lesson, the PP100 becomes:
- N form-tests: `<lesson>-MASTERY-f{k}` -> `<lesson>-MASTERY-FRQ-f{k}` (k=1..N), each a single-item test over one
  authored equivalent FRQ form (grader-wired, held-out source, per the equivalence contract above).
- One `assessment-bank` Resource `res-<lesson>-pp100` with `type:"assessment-bank"`,
  `resources: [<the N form-test ids>]`, `vendorResourceId` REQUIRED.
- The lesson topic's PP100 component-resource points at the bank Resource (not a single test).
- `course_push_mastery_v3_1.py` pushes N form-tests + N FRQ items per lesson; `course_assemble_v3_1.py` emits
  the bank Resource + the CR link to it. A bank of 1 == today (prod-safe fallback).

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


### Depth requirement refined (2026-07-23) — hole-filling reassignment, not just in-session retries

Noel's binding requirement: a student can be REASSIGNED a lesson as hole-filling after failing a test, and on
a redo they must NOT see the same prompts. And: actively DEFEND against repeat-farming (favor deeper banks).
So depth is driven by anti-repeat across the student's WHOLE history on a lesson, not just one sitting.

PowerPath mechanics that make round-robin fit this (from the spec):
- The round-robin is keyed to a PERSISTENT, ACCUMULATING attempt number. `getAttempts` returns ALL attempts
  for a student+lesson ("each attempt may represent a different sub-test"); `createNewAttempt` advances to a
  new attempt number (new sub-test by round-robin) when the current attempt is completed. So a hole-filling
  REDO = a new attempt = the NEXT form. A reassigned student does NOT restart at form 1.
- `resetAttempt` keeps the SAME bank test for the current attempt (does not advance, does not reset to form 1).
- No max-attempts cap / cooldown exists in the API. Round-robin never blocks; it wraps at N.

Consequence for depth: a student sees a REPEAT only once their CUMULATIVE attempt count on that lesson exceeds
N (initial mastery retries + every later hole-filling reassignment, summed). So:

  DEPTH N should cover:  (typical attempts to pass initial mastery)  +  (max hole-filling reassignments of the
                          same lesson)  +  a small margin.

This is why 3 is likely INSUFFICIENT under the hole-filling requirement: a student who fails initial mastery
(say 1-2 attempts) and is then hole-filling-reassigned the lesson 2-3 times would wrap and re-see form 1.
The number that matters is an ALPHA POLICY fact we must pin: how many times can hole-filling reassign the SAME
lesson, and how many mastery attempts are typical before pass? Depth = that sum + margin. Pending that, a
defensible planning default is depth 5-6 (covers ~2 initial + ~3 hole-filling redoes + margin), NOT 3.
Escalate gate/essay lessons further if the source pool allows; those are the highest farming value.


### DEPTH MODEL DECIDED (2026-07-23, Noel) — per-grain, defends against uncapped hole-filling

Binding facts: hole-filling reassignment has NO cap (a lesson can be reassigned any number of times), and we
DEFEND against repeat-farming. Round-robin over an assessment-bank means a student re-sees a form only after N
intervening distinct forms, so depth = how many distinct redoes before a repeat. The "~30 question bank" norm
Noel referenced traces to MCQ contexts (ALEKS adaptive diagnostic 25-30 Qs; Spearman-Brown reliability for a
20-30 *MCQ* summative; AlphaTest 5x24-item MCQ forms) — cheap items averaged for reliability. It does NOT map
1:1 to writing (our form = ONE rubric-graded composition, not 1 of 30 cheap items). Translated to writing +
sized to farming-risk and sourcing-cost, the decided depths are:

  DEPTH by grain:  sentence = 30   |   paragraph = 10   |   multi_paragraph = 10   |   essay = 10

Rationale (farming-risk x sourcing-cost aligns perfectly):
- SENTENCE is the MOST farmable (a student can memorize one sentence) AND its source is the CHEAPEST (an
  issue-FRAME = a one-line topic prompt, e.g. "Should social media apps check users' ages?", not a passage).
  So the deepest bank (30) runs on the cheapest fuel. We have 16 frames; reaching 30 = author ~14+ more short
  frames (trivial sourcing, own-words/public-domain).
- ESSAY/PARAGRAPH is the LEAST farmable (writing a full essay each attempt is real work) and the MOST expensive
  to source (a full Lexile-banded federal/public-domain LESSON passage). Depth 10 is the right ceiling: 10
  intervening forms before repeat is ample for compositions, without sourcing hundreds of passages.

Load (measured across 101 lessons): sentence 38 x30=1140, paragraph 26 x10=260, multi_paragraph 7 x10=70,
essay 30 x10=300  ->  ~1,770 total forms. Per grade: G9 590, G10 450, G11 510, G12 220. The load is dominated
by sentence forms, which are the cheapest to source (frames), so the effort is front-loaded on cheap assets.

Sourcing appetite (Noel): BOUNDED new sourcing approved. Plan: (1) reuse the existing pool first (16 frames,
37 single passages, etc.); (2) author new ISSUE-FRAMES to bring sentence lessons to 30 (cheap, own-words);
(3) source new vetted LESSON passages (Source Cache method: federal/public-domain, 480-word floor, Lexile in
band) only where an essay/paragraph family is too thin to reach 10. A coverage report will list exactly which
lessons/families need new sources and how many, before authoring.

Repeat guarantee under this model: no finite bank can guarantee zero repeats forever with uncapped reassignment;
depth 30 (sentence) / 10 (essay) means a repeat occurs only after 30 / 10 intervening distinct forms — rare and
pedagogically harmless (a re-seen form after that many redoes is effectively fresh). This is the honest target,
not "never repeat."
