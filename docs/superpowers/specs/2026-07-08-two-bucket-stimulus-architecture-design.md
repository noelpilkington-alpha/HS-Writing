# Two-Bucket Stimulus Architecture — Design Spec

**Date:** 2026-07-08 · **Status:** DESIGN (spec only; no code yet) · **Author:** brainstormed with Noel
**Scope:** the stimulus layer of the G9-12 writing content machine. Grade-agnostic design; G10 is the seed grade.

## Problem

Two problems with the current stimulus layer, both confirmed by inspection of the G10 bank:

1. **Contamination.** 13 of 15 G10 stimuli are bound by BOTH a lesson and a test item. A student learns on a
   passage, then is tested on the same passage: the test measures recall of that text, not transferable skill.
   Our lesson contract enforces bank-partition *within* a lesson (transfer slot must be a new topic), but the
   lesson-to-test boundary leaks completely.

2. **Not inexhaustible.** Stimuli are hand-authored as monolithic units (a pair is one record with PASSAGE_A +
   PASSAGE_B built together). That does not scale: to get 200 opposing-pair test forms you would hand-build 200
   pairs. "Nearly inexhaustible for the average student" requires generation on demand, not a fixed hand-built set.

## Decisions locked (from the brainstorm)

- **Split driver = all four:** test security/no-contamination, different per-bucket constraints, exhaustibility,
  and reuse/rights. This is a genuine TWO-CONTRACT design, not one contract with a tag.
- **Two buckets:** `lesson` stimuli and `test` stimuli, as first-class separated pools.
- **Inexhaustible = on-demand generation.** Build a seed floor now; the machine mints QC-passed stimuli forever
  whenever a student's unseen pool runs low. Consequence: **QC gates become the ONLY quality guarantee** (no
  human in the loop at mint time). The gates are the product.
- **Contamination boundary = hard topic + text partition.** A student is never tested on a passage OR a topic
  they saw in lessons. Enforced per-student at serve time using Platform3 Events (topics-seen).
- **Multi-source = compose from tagged singles** (both opposing and complementary). The ATOM is a single tagged
  passage; pairs are composed on demand by a composition gate. Accepted residual risk: composed complementary
  pairs weave slightly less tightly than hand-crafted ones; mitigated by the connection_point gate + batch-audit
  sampling, flagged as monitored, not blocking.

## Consumption model (derived, sizes the pools)

From our own G10 design (~68-lesson course, 8 mastery gates, Timeback retake-until-mastered):

- **Lesson bucket:** ~68 lessons x ~2.5 stimulus-touch slots (Teach source, Model, discrimination, the
  contract-required different-topic transfer slot) ~= 170 slots if each lesson done once. Mastery repeats on
  high-demand types (evidence-integration, analysis) push a heavy student to **~200-400 distinct lesson stimuli/grade.**
- **Test bucket:** ~10-15 gates/grade x ~6 unseen equivalent forms per struggling student = **~60-90 test
  forms/grade**, none colliding with what that student already saw.

"Inexhaustible" is ultimately on-demand; the seed floor makes it feel infinite from day one.

## Architecture

### A. The atom: a single tagged passage
Both buckets are built from single passages. A pair is never authored as a unit; it is composed. Every single
carries the tags that make composition and partition mechanical (see registries).

### B. Shared base contract + two profiles (Approach B)
One engine, one `bucket` field ("lesson" | "test"). Shared base gates run for both; the bucket switches the rest.

**Shared base gates (identical both buckets):** structure/word-band, provenance (own_authored OR public_domain),
fact-sources anti-fabrication, Lexile band membership, content-appropriateness screen (strictest-state), no-em-dash.

**Profile differences:**

| Gate | `lesson` profile | `test` profile |
|---|---|---|
| Lexile | band with tolerance (+/-1 sub-band ok; a slightly harder teaching text is fine with scaffolding) | **hard lock** to the exact on-grade band, no tolerance (fairness: test difficulty must not vary) |
| Annotation / scaffold | **allowed** (teaching annotations, glossed terms, labeled before/after) | **forbidden** (clean passage; nothing that cues an answer) |
| Source-config rule | full range `single | complementary | opposing`, chosen by the lesson type's staging ladder (KH single->complementary->opposing); a single-source stimulus is VALID even for a mode that tests as a pair | source-config must MATCH the target form's demand (opposing-pair for pick-a-side, complementary-pair for synthesis); gate enforces the match |
| Equivalent-form calibration | n/a | **NEW test-only gate**: a test stimulus must be calibrated to its pool — same mode, same passage-count, Lexile within a tight window of its pool siblings, comparable length + task demand, so every retake form is genuinely equivalent (not "got an easier one") |
| Topic reservation | must be a `lesson_pool` or `shared_ok` topic | must be a `test_pool` topic (never a lesson topic) |

Note: source-configuration vocabulary (single/complementary/opposing) is SHARED. The profiles differ only in
whether the choice is pedagogy-driven (lesson) or form-dictated (test).

### C. Three registries (the partition + composition backbone)

1. **Topic registry** (`topic_registry`): every passage gets a `topic_id` + `domain`, and each topic is marked
   `lesson_pool` | `test_pool` | `shared_ok`. Test stimuli draw only from `test_pool`; at serve time the push
   layer filters against the student's topics-seen (Platform3 Events). This is what makes "unseen at test time"
   enforceable, not aspirational.

2. **Proposition registry** (opposing-pairs): a proposition = one arguable question (e.g. "the US should build
   more nuclear power"). Every argumentative single is tagged `proposition_id` + `stance` (pro | con | nuanced) +
   Lexile + length + source_org. The **opposing-pair composer** picks one pro + one con UNDER THE SAME
   proposition_id; the composition gate verifies: same proposition, opposite stance, Lexile within a tight window,
   comparable length, distinct source orgs. Same-question-opposite-side is mechanically guaranteed.

3. **Theme registry** (complementary-pairs): each explanatory single is tagged `theme_id` + `facet` (its sub-angle)
   + an author-supplied `connection_point` (the one idea that joins it to siblings). The **complementary composer**
   picks two singles, same `theme_id`, DIFFERENT facets; the gate requires the shared connection_point present in
   both. Reduces "do these combine?" to a checkable structural claim (same theme + distinct facets + declared
   shared thread) instead of a human judgment. Residual weave-quality risk flagged for batch audit.

### D. The composition gate (guarantees correlated multi-source selection)
Composition is never free-floating passage selection. A pair is only valid if it is assembled WITHIN a proposition
(opposing) or a theme (complementary) and passes the relationship checks above. Coherence becomes a property the
generator is forced to satisfy, same discipline as every other gate. Scale example: 20 pro + 20 con singles under
one proposition = up to 400 valid opposing pairs from 40 authored passages.

### E. On-demand generation loop (QC is the only guarantee)
1. **Signal** (Platform3 Events): a student's unseen pool for {grade, mode, bucket, proposition/theme} is low,
   filtered against topics-seen.
2. **Mint**: author a fresh single against the profile, tagged to the registries.
3. **Gate**: full contract runs. **Fail = discard silently + retry.** An ungated stimulus never reaches a student.
4. **Compose** (if a pair is needed): composition gate assembles from the enlarged single pool.
5. **Admit** to the bank; register topic-as-seen for that student when served.

### F. Seed floor (per grade — makes it inexhaustible from day one)

| Bucket | Seed floor / grade | Structure |
|---|---|---|
| Lesson singles | ~120-150 | across modes + the staging ladder; feeds 500+ composed configs |
| Test singles | ~80-100 | organized by proposition/theme, balanced pro/con per proposition |
| Propositions | ~15-20 test + ~15-20 lesson | each >=4 pro + >=4 con singles -> 16+ opposing pairs each |
| Themes | ~12-15 test + ~12-15 lesson | each >=3 facets -> complementary pairs |

## What changes vs. today

- `stimulus_contract.py` refactors: shared base + `bucket` profile switch; add the equivalent-form-calibration
  gate (test), the annotation-allowance (lesson), and the topic-reservation gate. `gate_two_sidedness` is
  replaced by the composition gate operating on tagged singles.
- New modules (later passes): `topic_registry.py`, `proposition_registry.py`, `theme_registry.py`,
  `composition.py` (the composer + gate), and the on-demand `mint_loop` (wired to Events at push time).
- Existing 16 G10 stimuli: re-expressed as tagged singles (the 6 opposing pairs decompose into 12 stance-tagged
  singles under 6 propositions; the 6 explanatory singles + 4 analysis texts carry over directly). Migration is
  mechanical; QC must still pass. Note: this yields ~22 singles, a fraction of the ~200-250 seed-single floor
  (lesson + test) — the seed is mostly NET-NEW authoring, with the existing bank as the first propositions/themes.
- The lesson/item contracts gain a check that a TEST item never binds a `lesson_pool`-only topic (closes the
  contamination leak at bind time, before it ever reaches a student).

## Non-goals (explicitly out of scope for this design)
- Live wiring of the on-demand loop to Platform3 Events (needs creds + the push layer live; deferred with the grader).
- The grader / rc.* scoring (already deferred by decision; downstream of push format).
- G9/G11/G12 generation (grade-agnostic design; G10 seeds first).

## Open questions / risks to monitor
- **Composed complementary weave quality** — the connection_point gate is a structural proxy for semantic
  coherence; sample-audit composed complementary pairs and tune the gate if weave is thin.
- **Equivalent-form calibration tightness** — the Lexile/length/demand window needs empirical tuning against real
  retake fairness; start tight, loosen only with evidence.
- **Topic exhaustion at the domain level** — hard topic partition means lesson and test compete for a finite topic
  space; the topic registry must be sized so test_pool never starves. Monitor domain coverage as grades fan out.
- **On-demand cost** — every mint is an LLM call + gate run; batch-mint during low-load windows where possible.
