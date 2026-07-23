# In-Video One-Beat Check Design

**Date:** 2026-07-22
**Status:** Design (awaiting review before implementation plan)
**Owner:** HS Writing pipeline
**Supersedes/extends:** the video-placement council rule (2026-07-21) that fronts a lesson with its intro video and compresses the opening teach prose.

## Problem

The 45 Grade 9-12 concept lessons now each carry an intro video (~2-3 min) that
teaches the one idea and sits BEFORE the compressed teach prose. Timeback can now
deliver an INTERACTIVE video: the player pauses at a timestamped cue, shows a QTI
question, and resumes after it is answered. The question is whether to add such
in-video questions given that every concept lesson ALREADY has gated
Read-Check-Unlock discrimination checkpoints downstream, and if so, how.

A prior Fable-5 evaluation of THIS course measured redundancy fatigue: students
disengage when made to do the same check twice. So a naive "quiz inside the video
too" risks re-triggering the exact fatigue the course was tuned to remove.

## Decision (from the council of writing instruction, 2026-07-22)

Convened seats: Kirschner & Hendrick (segmenting / redundancy / CLT), Wiliam &
Hattie (formative assessment / retrieval), Direct Instruction (frequent response /
faultless communication), Yeager (adolescent motivation / error climate). Full
adjudication is recorded in the session; the binding rule follows.

Add a single, first-encounter, NON-GATING in-video comprehension anchor (the
**One-Beat Check**) to the intro videos of QUALIFYING concept lessons, sourced from
the lesson's own locked teach text, delivered as a timestamped `tb-interaction`
overlay on the EXISTING hosted video. It is DIFFERENT IN KIND from the downstream
discrimination gate and never a copy of it.

### The four answers

1. **Add in-video questions: YES, complementary.** A 2-3 min video with zero
   required response is the passivity failure; the One-Beat Check converts the
   passive stream into one active beat. The measured fatigue lives in the
   same-item-twice failure mode, not in pausing itself.
2. **Different in kind: YES, categorically.** In-video = a light recognition /
   comprehension anchor on the move the video has already shown on screen.
   Downstream = the harder minimal-pair discrimination mastery gate. Never reuse a
   downstream item (that pre-exposes the gate, destroys its validity, and is the
   redundancy the eval measured).
3. **Which lessons: an ARCHETYPE gate, not all 45.** Include only intro videos that
   demonstrate a discrete target move on screen. Exempt: pure hook/motivation
   videos, recap/review videos, clips under 90 seconds, and any lesson whose
   downstream checkpoints already densely cover that exact beat.
4. **Source: AUTHOR NEW from the locked lesson teach text**, hand-keyed to the
   video cue point, delivered as an overlay. Do NOT regenerate videos. Do NOT mine
   the discrimination bank. (DI's "simplify from the vetted bank" lost the source
   call; its control concern was adopted as the QC template below.)

### Conflicts resolved (by evidence grade, not averaged)

- **Gating -> NON-GATING wins.** A must-pass gate at first encounter tests
  not-yet-taught content (validity failure) and reads as the respect gap to a teen.
  The one hard gate per micro-skill stays downstream. DI's forced overt response is
  kept; DI's block-Continue-on-error is rejected.
- **Retrieval/spacing credit -> not claimed at the video.** At first encounter
  nothing is in long-term memory to retrieve; the beat is credited only with
  attention-anchoring and priming recognition. Spacing/retrieval is booked to the
  downstream checkpoint (cross-session).
- **Item kind -> recognition anchor (right-answerable) over pure open prediction.**
  It satisfies the no-audio/skim constraint (answerable from on-screen text/visual)
  and yields a confirmable signal; Yeager's low-stakes "your call" framing and
  no-penalty line are kept.

## The One-Beat Check specification

**Count.** RULE UPDATED 2026-07-22 (Noel): "cover every your-turn beat, no
exceptions." Every segment where the video explicitly tells the student to pause and
act (role try_it / your_turn) gets ONE non-gating in-video question. This OVERRIDES
the council's original cap of two per video: the operating principle is that a
scripted your-turn beat that dangles with no question is the passivity failure the
interactivity is meant to fix. The only skips are MECHANICAL, not design exceptions:
  - a beat at the very END of the video (final segment) has no runtime left to
    resume, so it cannot carry a pause.
  - `recap` is a summary, not a your-turn beat, so it gets no question (unless a
    future rule adds retrieval checks on recaps).
Observed scope: 45 videos, 96 your-turn beats (39 videos have 2, 6 have 3).

**Placement.** Immediately AFTER the video's first complete on-screen positive
instance of the target move. In cue-derivation terms, this is the first natural
"your turn"/recap beat (see `video_timing.py`). The rule NARROWS the current timing
map: default to a single cue at the first post-instance check-role beat, not one
cue per check-role segment.

**Kind.** A light recognition or comprehension anchor on the single idea the video
has already shown. Binary or 1-of-2. Answerable from on-screen text or visual (never
audio-only). Commit-then-reveal with a one-line process-level "why" that feeds
forward into the teach prose, plus a one-line no-penalty transparency note.

**Example stem (no em dashes):** "You just watched the writer add a sentence. Was
that sentence the CLAIM, or a REASON backing it up? Make your call, then we will
confirm why in one line."

**Gating.** NON-GATING. It never blocks Continue and can never be marked wrong to
advance. Concretely: the item's response processing does NOT drive
`INTERACTION_VISIBILITY` off a correct answer, and the player's progression is not
gated on it. This is the key departure from `checkpoint_xml`, which hard-gates via
`INTERACTION_VISIBILITY` + `completionStatus`.

**Source.** Authored from the lesson's own locked teach text (the same source the
video script was built from), to the QC template below. Bound to what the video
actually shows.

### QC template (adopted from DI's faultless-communication concern)

Every One-Beat item must satisfy, or it is not emitted:

- Exactly ONE distinguishing feature varies between the options.
- One interpretation only (no ambiguous stem).
- The stem references NOTHING shown after the cue point (never test ahead of
  instruction).
- The correct answer is resolvable from on-screen text/visual, not narration alone.
- No em dashes in any student-facing text (project hard rule).
- The item is recognizably DISTINCT from the lesson's downstream discrimination
  items (no shared stem or option set).

## Delivery mechanism (decoded from live MS Chemistry, courseId
2673f489-fabd-4b88-ad04-6eea46c99479)

Interactive video is the SAME `tb-*` family as gated-reading, not a separate video
system and not PCI. The intro-video segment becomes a `tb-video` figure:

```
<figure class="tb-video" id="video-<lid>" data-duration-seconds="<total>">
  <video src="<mp4>" crossorigin="anonymous" controls="controls" preload="metadata">
    <track kind="captions" srclang="en" src="<vtt>" default="default"/>
  </video>
  <div class="tb-interaction tb-qti-assessment-item"
       data-timestamp-seconds="<cue>" data-catalog-idref="vq-<lid>-1"></div>
</figure>
```

and the catalog gains one `tb-qti-config` per One-Beat item, mounted exactly like a
checkpoint:

```
<div class="tb-qti-config" id="vq-<lid>-1"><a href="<base_url>/items/vq-<lid>-1.xml"
     type="application/xml"></a></div>
```

The One-Beat item XML is a choice interaction, authored by a NEW non-gating builder
(a sibling of `checkpoint_xml`) that omits the `INTERACTION_VISIBILITY` hard-gate
machinery. `data-timestamp-seconds` comes from `video_timing.cue_points` (first
post-instance check-role cue). `data-duration-seconds` comes from the video probe's
total.

## Architecture / integration points

All video behavior remains PREVIEW-SCOPED and prod-safe. The production push passes
no `video_map` and the module-level `_INCEPT_VIDEOS` ships empty, so `tier_a` and
the real push stay byte-identical to today.

- **`pipeline/gated_reading.py`**
  - The existing plain-`<video>` intro segment (lines ~710-724) is replaced, WHEN a
    One-Beat item exists for the lesson, by a `tb-video` figure carrying the
    timestamped `tb-interaction`. When no One-Beat item exists (exempt archetype),
    the plain-`<video>` segment is emitted exactly as today.
  - A new non-gating item builder `one_beat_xml(vq_id, item)` (sibling of
    `checkpoint_xml`), producing a choice interaction with per-choice feedback and a
    persistent correct-feedback block, but WITHOUT the `INTERACTION_VISIBILITY`
    gate.
  - The One-Beat item is appended to the returned `checkpoints` list (so the push
    pipeline hosts `items/vq-<lid>-1.xml` alongside the cp/frq items), and its
    `tb-qti-config` is added to the catalog.
- **`pipeline/video_timing.py`** — the cue used for the One-Beat is the FIRST
  post-instance check-role cue. A thin helper returns the single default cue (and up
  to two for the ~3-min exception) rather than one-per-check-role. It derives the
  cue from the artifact's `output_json.script` segment durations (already the input
  shape `cue_points` consumes).
- **Timing source (corrected).** The current per-grade `<grade>_videos.json` entries
  carry ONLY `{mp4, vtt}`, and the per-lesson dest folders retain only the
  mp4/vtt/scene-PNGs. The artifact's `output_json` (with per-segment
  `duration_seconds` and total) is fetched during `fetch_video` to build the VTT but
  is NOT persisted. To set `data-duration-seconds` and the `tb-interaction` cue
  WITHOUT a re-probe, `fetch_video` must additionally persist the artifact's
  `output_json` (or just the derived `{total_seconds, segment_ends, check_ends}`)
  next to the mp4, and the video map entry must carry `duration_seconds` (+ the
  chosen cue). This is a small addition to the fetch/manifest step, not a
  regeneration.
- **The artifact's OWN model-written questions are NOT used.** Incept video
  artifacts carry an `output_json.questions[]` list (the model's own in-video
  question candidates). Per the council source ruling, the One-Beat is authored NEW
  from the locked lesson teach text; the artifact's questions are ignored (using
  them would be uncontrolled regeneration). `video_timing`'s question-consuming
  paths are used only for CUE derivation (segment ends), not for question content.
- **One-Beat authoring** — a builder that reads a lesson's locked teach text and the
  first-encounter target move, and emits ONE recognition item (stem + 2 options +
  per-option why + correct why) to the QC template, for qualifying lessons only.
  **Review posture (decided 2026-07-22):** trust the QC template as the gate; the
  drafted stems are NOT hand-reviewed before push for now. (Revisit if a batch shows
  quality drift.)

## Build sequencing (decided 2026-07-22)

Prototype ONE G9 concept lesson end-to-end in the preview FIRST (see it pause and
resume in the player), then generalize the authoring + render across the qualifying
45. The prototype validates the `tb-video` + `tb-interaction` render shape, the
non-gating item XML, and the cue timing before any fan-out.

## Archetype qualification (which of the 45)

A lesson qualifies for a One-Beat Check when ALL hold:

- It has an intro video in the video map.
- The video's runtime is >= 90 seconds.
- The video demonstrates a discrete target move on screen (concept archetype:
  lesson types 1/2/3/4/6), i.e. it is not a pure hook, recap, or procedural-review
  video.
- Its downstream checkpoints do not already densely cover the identical beat.

Exempt lessons keep today's plain intro `<video>` segment with no `tb-interaction`.

## Testing

- `video_timing`: a helper that returns the single default cue (and the two-cue
  exception) is unit-tested against the probe fixture; existing tests stay green.
- `one_beat_xml`: emits valid QTI (parses via `ET.fromstring`), is NON-gating
  (asserts absence of the `INTERACTION_VISIBILITY` hidden-on-correct machinery),
  carries per-choice feedback, and contains no em dashes.
- `gated_reading`: a lesson WITH a One-Beat item renders a `tb-video` figure with a
  `tb-interaction[data-timestamp-seconds]` and a matching `tb-qti-config`; a lesson
  WITHOUT one renders the plain `<video>` segment; the production path (no
  `video_map`, empty registry) is byte-identical to today.
- Archetype gate: exempt archetypes (hook/recap/<90s) emit no `tb-interaction`.

## Non-goals / guardrails

- No regeneration of the hosted videos.
- No reuse or paraphrase of downstream discrimination items.
- No second hard gate: the One-Beat never blocks progression.
- Prod push path unaffected: preview-scoped `video_map`, empty prod registry.
- Ceiling of two is an exception, not a target; default is one.
- The in-video beat is logged as attention/comprehension only, never as
  spacing/retrieval, so downstream mastery metrics are not distorted.

## Anticipated pitfalls (carried from the council)

1. Silent drift back to the discrimination bank under time pressure. Enforce the QC
   template at authoring, not as a guideline.
2. Gate creep: a "non-gating" item that still withholds Continue is a gate. Verify
   the `tb-interaction` is non-blocking and non-scored in the player.
3. Testing ahead of instruction: the cue must follow the first complete on-screen
   positive instance.
4. Audio-dependence: every stem and answer must be resolvable from on-screen
   text/visual.
5. Overcounting: treat the two-cue case as rare; default is one.
6. Roster thinking: applying to all 45 recreates the redundancy the rule prevents.
   Honor the exemptions.
