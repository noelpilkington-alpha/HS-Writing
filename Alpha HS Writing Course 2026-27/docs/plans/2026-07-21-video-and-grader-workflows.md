# Two Concurrent Workflows: Video Generation + Grader Evaluation

**Date:** 2026-07-21
**Status:** SCOPING (decisions captured; execution gated where noted)

Two independent workstreams, planned together so dependencies are explicit. Neither is fully
executable today: video is gated on the gated-reading course going live; the grader bake-off can
start now but its verdict needs a G9-12 human-scored set that does not yet exist.

---

## WORKFLOW 1: Video Generation

### 1.1 Target set (DECIDED: all concept lessons)
Noel's default = videos in all granular CONCEPT lessons. Derived from `lesson_type` via
`lesson_contract.archetype_of`:
- **concept** (types 1/2/3/4/6): **42 lessons** -> G9 14, G10 9, G11 15, G12 4  <- THE VIDEO TARGET SET
- checking_revision (type 5): 13 -> no video (these are practice/calibration, not new teaching)
- full_essay_build (types 7/8): 43 -> no video (assembly/production, not concept teaching)

Open sub-decision for the plan: G12 has only 4 concept lessons (it is voice/nuance/essay-heavy).
Confirm whether the seed run does all 42 at once or ramps G9 first (G9 is the near-term ship grade).

### 1.2 What the video replaces (DECIDED: per-archetype rule, below)
Every concept lesson opens with a `teach_card` ("The one idea: ..."). Proposed per-archetype rule
(for Noel approval in the build pass):

| Concept sub-type | Video role | Prose teach fate |
|---|---|---|
| type 1/2/3 (source-reading, claim-building, evidence-integration) | Video FRONTS the opening teach segment (plays first, as the "teach") | Prose teach segment KEPT as the readable equivalent + captions transcript (accessibility + skimmers + no-audio contexts) |
| type 4 (text-dependent-analysis) | Same: video fronts the DEVICE->EFFECT->WARRANT teach | Prose kept |
| type 6 (editing-in-context) | Video OPTIONAL (editing is procedural; a diagram may serve better) | Prose kept; video only if it demonstrably beats prose+diagram |

Rationale: "supplement, do not delete" is the low-risk default (the brainlift's over-caution instinct
applies to instruction too: removing verified prose teach for an unverified video is the wrong-direction
risk). The video ADDS a modality; the prose stays as the fallback. Revisit "video replaces prose" only
after videos are proven to render + teach as well.

### 1.3 Delivery (RESOLVED 2026-07-21 - see incept-t7-first-batch memory)
Host on the Incept bucket (upload.inceptstore.com -> streamable public_url), reference as a SEPARATE
OneRoster component-resource (type=video), NOT embedded in lesson.html, NOT QTI. Machinery built +
validated live (incept_upload.py, incept_video.video_resource_plan). NO player/sanitizer/CORS blocker.

### 1.4 HARD DEPENDENCY (gates execution)
The video stage only makes sense on the GATED-READING course. The live "Writing G9"
(hs-writing-g9-2026) is the OLD QTI-quiz build; the gated-reading + 35-diagram course was never pushed
live (blocker = lesson.html article hosting, still open from July). So:
- Video TARGETING can be finalized now (this doc).
- Video EXECUTION waits until the gated-reading course is live.
- Sequencing: [get gated-reading course live] -> [generate/host/wire 42 videos] -> [per-archetype teach restructure].

### 1.5 Video stage steps (per target lesson, all machinery built)
generate_video -> fetch_video -> reconcile_questions (flag video Qs that dup our gated checks) ->
upload_files (inceptstore) -> video_resource_plan -> POST resource + component-resource -> verify renders.
Cost: ~3-4 min generation/video slow-lane; 42 videos ~= a few hours background + review.

---

## WORKFLOW 2: Grader Evaluation (DECIDED: bake-off all 3, decide by evidence)

### 2.1 The three candidates
| Option | What | Where |
|---|---|---|
| **A. Ilma's production grader** | Per-criterion AP FRQ grader, Timeback-integrated via ExternalApiScore | ap-grader.inceptstore.com/{slug}/grade; English essay route (Row A/B/C EssayGrader) is the closest to our writing FRQs |
| **B. Our grader** | Writing_Test_Grader (CJ/holistic prompts, G3-8 tuned) | c:/Users/noelp/Writing_Test_Grader/grader/ |
| **C. Timeback native** | Platform built-in SCR scoring | UNKNOWN - investigate first (does it score short-constructed-response accurately?) |

### 2.2 The brainlift's transferable lessons (apply to whichever wins)
From `WF - AI FRQ Grading System Brai` (Ilma's production grader, validated discipline):
1. **Per-criterion, not holistic** - one LLM call per rubric criterion, temp 0.0, {earned,evidence,reasoning}.
   Our grader is holistic/CJ -> the brainlift argues this is the wrong primitive (SPOV1).
2. **Fail asymmetrically against inflation** - over-scoring is silently accepted + corrupts placement;
   track mean SIGNED error, not just RMSE; hard |bias| ceiling (SPOV2).
3. **Blind human validation is the ONLY accuracy gate** - not confidence, not self-consistency (SPOV4).
4. **The rubric is the program** - atomic one-criterion-per-block; most failures are rubric-shape, not model (SPOV6).
5. **Fail closed, never retry a verdict** - errored criterion = earned=False + internal_error, never a fabricated pass (SPOV3).

### 2.3 The accuracy bake-off (the core of this workflow)
Run all three on the SAME student responses, compare to a human-scored blind set (per SPOV4).
- **Instrument EXISTS**: Writing_Test_Grader/_blind_set_groundtruth.json has Noel-scored ground truth
  (noel_ideas / noel_org / noel_conv per response) + a _gold_comparison.py harness.
- **THE GAP (must resolve first)**: that blind set is **G3-G8 only**. Our course is **G9-12**. There is
  NO G9-12 human-scored blind set yet. The bake-off's verdict is only trustworthy on a G9-12 set with
  our rubrics (rc.staar / rc.ohio / rc.mcas / rc.ap).
- So the bake-off has a PREREQUISITE: assemble a small G9-12 blind set (N student responses across the 4
  rubrics, Noel- or SME-scored blind) before the three-way comparison means anything.

### 2.4 Bake-off steps
1. **Investigate Timeback native SCR grading** (read-only): does the platform natively score SCR/short
   items, on what rubric model, with what accuracy claim? Determine if it removes the need for an external
   grader on checkpoint discriminations + short FRQs (leaving only full essays needing A or B).
2. **Assemble a G9-12 blind set**: N (~20-40) real student responses across rc.staar/ohio/mcas/ap, scored
   blind by a human (Noel/SME). This is the prerequisite instrument.
3. **Run all 3 on that set**: (A) Ilma's English essay route, (B) our grader, (C) Timeback native where
   applicable. Score each vs the human on within-1, mean signed error (bias direction), per-criterion match.
4. **Decide by evidence** (not by preference): lowest inflation bias + tightest human agreement wins.
   Fold the brainlift's per-criterion + fail-closed discipline into the winner if it lacks it.
5. **Wire the winner**: our pipeline ALREADY has g9_wire_grader.py (attaches ExternalApiScore + rubric-block
   via PUT, no content re-push). If A wins -> point it at ap-grader route. If B wins -> deploy our grader +
   point there. If C wins -> native, possibly no external grader for short items.

### 2.5 What already exists (do not rebuild)
- `g9_wire_grader.py` - attaches the grader to live FRQs via PUT (Timeback RULE 3 safe: rebuild-from-source
  -> add config -> PUT). Waiting only for a grader /score URL.
- `grader_smoke.py` - grader smoke test.
- g9_push_live already pushes FRQs as basic extended-text (accept responses, no auto-score yet) with the
  rubric_ref in metadata; the grader route is a PUT away.

---

## Dependency summary
- **Video**: targeting DONE (this doc); execution GATED on gated-reading course going live.
- **Grader**: bake-off can START now (step 1 Timeback-native investigation + step 2 blind-set assembly are
  independent of the course going live); verdict GATED on the G9-12 blind set existing.
- **Shared prerequisite for BOTH ships**: get the gated-reading + diagrams course live on Timeback
  (resolve lesson.html article hosting - the one open dependency from July). This is upstream of both.
