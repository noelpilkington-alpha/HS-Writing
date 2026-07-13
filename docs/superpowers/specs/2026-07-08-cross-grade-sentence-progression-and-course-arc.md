# Cross-Grade Sentence-Skill Progression + Course-Arc Architecture (G9-12)

**Date:** 2026-07-08 · **Status:** DESIGN (spec only; no code, no lesson regeneration yet) · brainstormed with Noel
**Scope:** the developmental architecture of the whole G9-12 writing course sequence. Governs all four grades.
**Supersedes on this point:** the within-lesson `gate_unit_ladder` reading (see "Gate reframe" below).

## Problem

The sentence -> paragraph -> essay mastery scaffold is a COURSE-level progression, but it was (partly) built as
a within-LESSON climb. Noel caught this. Two consequences of the misread:
1. Cramming sentence->paragraph->essay into one lesson fights Kirschner & Hendrick's core mechanism (build a
   component to automaticity in long-term memory, THEN combine; that needs spacing across sessions, not one
   sitting). The within-lesson climb has no interval for the smaller unit to become automatic first.
2. Without a cross-grade map, "each grade opens with a sentence phase" would re-teach the same moves (appositives,
   because/but/so) to a more-expert student every year, which the expertise-reversal effect shows actively
   depresses learning (d ~= -0.428 for over-supporting the advanced learner, ExpertiseReversal2025).

The missing artifact: a cross-grade sentence-skill progression (what is NEW vs INHERITED at each grade) and the
course arc it implies. Our spine states the principle ("G9 sentence-level -> G12 rhetorical; families escalate,
don't multiply") but never breaks the sentence skills out by grade.

## Decisions locked (from the brainstorm)

- **The COURSE, not the lesson, carries the sentence -> paragraph -> essay scaffold.** Most lessons hold ONE
  dominant unit; the within-lesson fade is about SCAFFOLDING (worked -> completion -> independent), not climbing
  units. Composite lessons (essay-assembly, synthesis) are the flagged exception; their internal rungs are
  COMPOSING-PROCESS steps that assume prior fluency, not unit re-teaching.
- **Authoritative basis = triangulation of four sources.** A skill's grade placement must be justified by: (1)
  the state test crosswalks (what is tested per grade), (2) TWR's own documented skill sequence, (3) the
  CCSS/ACC Language & Writing grade-band standards, and (4) the Council of Writing Instruction ONLY where those
  three conflict. No placement is asserted from intuition.
- **Two-layer sentence phase.** Layer 1 = genre-GENERAL mechanics substrate (combining, expansion, appositives,
  subordinating conjunctions, boundaries, because/but/so), taught ONCE at the grade it is new, to automaticity.
  Layer 2 = genre-SPECIFIC sentence moves (claim, attributed-evidence, controlling-idea, device->effect->warrant,
  cross-source), taught JUST-IN-TIME immediately before that genre's paragraph phase.
- **Inheritance = retrieval-gate, do not re-teach.** Inherited skills get a fast retrieval CHECK (spaced
  retrieval + placement signal), not a re-teaching lesson. Pass -> proceed; fail -> platform routes remediation
  to the grade that OWNS the skill (may descend more than one grade). New skills get full lessons.
- **G10 is deliberately thin on new mechanics.** G10's newness is genre-specific (nuanced/counterclaim-aware
  claim; analysis device->effect->warrant), not mechanical. A G10 course that re-teaches combining/appositives
  would be redundant.
- **The map re-scopes existing G10 lessons** (accepted): notably T6 editing (shrinks: retrieval-gate G9
  substrate + teach only G10-new editing) and T2 claim (re-scoped to the nuanced/counterclaim-aware claim). T7/T8
  rungs are kept but re-labeled as composing-process steps.

## Architecture

### A. The two-layer sentence phase (within a grade)
- **Layer 1 (genre-general mechanics):** one front-loaded block, teaching only the grade's NEW mechanics;
  inherited mechanics are retrieval-gated. Genre-neutral, so it transfers to every strand.
- **Layer 2 (genre-specific sentence move):** distributed, not front-loaded. Each genre strand opens with its
  own load-bearing sentence move, taught just before that genre's paragraph phase (KH just-in-time).

### B. The cross-grade inherited-vs-new map (DRAFT cut)

> PROVISIONAL: the cells below are a triangulated first cut, NOT final. The build step must verify each
> NEW/INHERITED placement against all four sources (crosswalk, TWR sequence, CCSS/ACC grade bands, council for
> conflicts) before it is authoritative. Treat this table as the hypothesis the build tests, not the answer.

**Layer 1 - genre-general mechanics:**

| Grade | NEW (teach to automaticity) | INHERITED (retrieval-gate only) |
|---|---|---|
| G9  | full TWR substrate: expansion, combining, appositives, subordinating conjunctions, fragment/run-on/comma-splice control, because/but/so | (entry grade) |
| G10 | thin: complex combining, parallelism, modifier placement (STAAR editing targets not owned by G9) | all G9 substrate |
| G11 | sentence-level concision, precision, rhetorical syntax (ACT/SAT "knowledge of language" band) | G9 + G10 |
| G12 | AP sophistication-level syntactic control (varied, purposeful sentences AS a rhetorical choice) | G9-G11 |

**Layer 2 - genre-specific sentence moves:**

| Grade | NEW genre-sentence moves | INHERITED |
|---|---|---|
| G9  | claim sentence, attributed-evidence sentence, controlling-idea sentence (argument + explanatory enter) | (entry) |
| G10 | nuanced/counterclaim-aware claim sentence; device->effect->warrant sentence (analysis enters) | G9 claim/evidence/controlling-idea |
| G11 | cross-source (synthesis) sentence; rhetorical-analysis sentence move | G9-G10 genre-sentences |
| G12 | AP-level moves ride on G11 (depth, not new sentence TYPES) | G9-G11 |

**Two findings the map surfaces (features, not bugs):** (1) G10 has almost no new Layer-1 mechanics -> its
sentence phase is thin-on-mechanics, focused on the nuanced-claim + analysis sentences. (2) The map retro-scopes
existing G10 lessons (T6, T2 shrink/re-focus) -> see section E.

### C. Retrieval-gate inheritance mechanism
For every INHERITED skill at a grade: a fast retrieval check at the start of the grade/strand.
- Pass -> proceed; the skill is used, never re-taught.
- Fail -> platform routes remediation to the grade that OWNS the skill (Platform3 mastery-gate + prerequisite;
  routing may descend more than one grade, e.g. a new G11 student sent to a G9 lesson).
- Each grade's course declares its inherited-skill prerequisites EXPLICITLY (machine-readable), so the platform
  can wire the gates + remediation routing. This prerequisite declaration is part of the course-arc artifact.
- Limit: G9 (entry) has nothing below it, so its substrate is taught outright, not gated.

### D. The course arc per grade (what the map produces)
```
GRADE N COURSE
  Layer-1 sentence phase   : teach NEW mechanics, retrieval-gate inherited   (thin @ G10, thick @ G9/G11)
  per genre (arg, explanatory, analysis, [synthesis G11+]):
    Layer-2 genre-sentence : the genre's load-bearing sentence move (just-in-time)
    paragraph phase        : build that genre's paragraph (single-unit lessons, scaffold-fade)
  essay/composite phase    : essay-assembly + synthesis (composing-process rungs live HERE)
  calibration/revision     : threads across, applied to whatever unit is current
```
Ordering law: no lesson appears before the phase that teaches its prerequisites (genre-sentence before
genre-paragraph; essay after paragraph fluency).

### E. Gate reframe + impact on existing G10 lessons (flagged for the follow-on gate-redesign spec, NOT built here)
- `gate_unit_ladder`: reinterpret from "non-decreasing WITHIN a lesson" to "each lesson declares ONE dominant
  unit; climbing is the flagged composite exception." The scaffold moves to the course sequence.
- `gate_type_ceiling` -> promote to a COURSE-PHASE ORDERING gate (a lesson cannot precede the phase that teaches
  its prerequisites).
- New: a per-grade prerequisite-declaration + retrieval-gate check.
- Existing G10 lessons are RE-SCOPED, not discarded:
  - T6 editing: re-scope to "retrieval-gate G9 substrate + teach only G10-new editing (parallelism, modifiers)"; likely shrinks.
  - T2 claim: re-scope to the nuanced/counterclaim-aware claim (assume the basic claim sentence from G9).
  - T7/T8: keep the internal rungs, re-label as composing-process steps that assume paragraph fluency.
  - T1, T3, T4, T5: mostly intact (already paragraph-unit, genre-appropriate).

## What this spec delivers
1. The cross-grade sentence-skill progression map (both layers, G9-12, inherited-vs-new), with each cell
   justified against the 4 sources and any conflict council-adjudicated.
2. The course-arc architecture (the section-D arc per grade + the retrieval-gate prerequisite declarations).

## Non-goals (explicitly out of scope here)
- The gate-code redesign (section E) - a follow-on spec after this is approved.
- Regenerating/re-scoping the existing G10 lessons - follows the gate redesign.
- Generating the full ~68+ lesson course - the seed run, later.
- Cut scores / field-test efficacy - needs student data.

## Open questions / risks to monitor
- **Placement accuracy per cell.** The draft cut is triangulated but not yet source-verified cell-by-cell; the
  spec's build step must confirm each NEW/INHERITED placement against crosswalk + standards + TWR, and convene a
  narrow council only where they conflict (candidate conflict: exactly which mechanics are "G10-new" vs "G9").
- **Cross-grade remediation depth.** Routing must reach down >1 grade for mid-sequence entrants; confirm
  Platform3 prerequisite routing supports non-adjacent descent.
- **Spiral vs strict phase.** The 4:2:1 ratio implies smaller-unit work CONTINUES after essays begin
  (interleaving), so the arc is dominant-phase-ordered, not a hard gate; watch that paragraph/sentence retrieval
  keeps recurring in the essay phase rather than stopping.
- **G10-first artifact risk.** We proved the machine on G10, but the progression is anchored at G9; expect the
  map to trim some current G10 sentence content once G9 ownership is fixed.
