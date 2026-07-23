# Timeback-Player Testing Agent Design

**Date:** 2026-07-23
**Status:** Design (awaiting review before build)
**Goal:** An agent that drives the live Timeback player against our lessons and evaluates them AS A STUDENT
SEES THEM: videos load and pause at each One-Beat cue, lesson content renders correctly, gated checkpoints
gate and unlock. Grading is deferred (see Scope).

## Why this surface is faithful to Timeback

The player at `content.platform.learnwith.ai/player` IS Timeback's current content renderer (not a
preview-only tool). It is a client-side SPA (`<div id="root">` + JS bundle) that fetches our public
`lesson.html` by `contentUrl` and renders it. Hosting the `lesson.html` on Vercel vs CloudFront does not change
how it renders. So driving this player against our lesson URLs is a faithful test of the Timeback presentation.

VERIFIED LIVE 2026-07-23 (G9 L01, artifact 11400) via the gstack `browse` (Playwright) daemon:
- The player loads with NO auth, returns 200, renders our lesson (title, `figure.tb-video`, video src).
- Playing the video to the 82s cue AUTO-PAUSES it (`video.paused === true` at `currentTime === 82`) and pops
  the One-Beat question ("Which question does it fail?") with all four options and the "Q1/1" badge.
- Clicking the correct option shows the confirmation and a Continue affordance.
This proves both the feature works end-to-end in the real player, and an agent can detect and drive it.

## Two player behaviors discovered (the agent must report these)

1. **The player gates video progression.** The footer shows "Watch all videos to continue" and Continue is
   disabled until the video is watched. So even though our One-Beat item XML is non-gating, the player will not
   let a student skip past the video. This is player behavior, not ours; the agent reports it, does not fail on
   it.
2. **The One-Beat renders with a Submit button and Q-of-N framing.** The player treats the tb-interaction as a
   submittable question (Submit button, "Q1/1"), not a zero-click "notice and continue." The agent records how
   the player actually presents each One-Beat.

## Scope

**In scope (testable on the player surface today):**
- VIDEO: the intro video loads (src resolves, non-zero duration), plays, and PAUSES at each authored One-Beat
  cue (compare to the cues in `data/one_beats.json` / `video_timing`).
- ONE-BEAT: at each pause, the expected question renders with the expected option count; the agent can answer
  and the video resumes. Wrong-answer behavior recorded (does the player block or continue).
- CONTENT: the lesson's teach cards, worked examples, and prose render with no broken markup, no leaked
  placeholder/al-text blobs, no raw HTML. (Reuses the render-QC defect classes as on-screen checks.)
- GATING: the gated Read-Check-Unlock discrimination checkpoints actually gate (Continue disabled until a
  correct answer) and unlock on a correct answer.

**Deferred (cannot be exercised on this surface):**
- GRADING (FRQ scoring). The 78 G9 FRQs render and accept typed input in the player, but scoring is an
  `ExternalApiScore` operation that runs server-side in the live Timeback QTI runtime, invoked only when the
  item is delivered as a scored QTI item inside the live course wired to the deployed grader. The player-preview
  path has no grader behind it. Grading evaluation is a SEPARATE later module against the live Timeback student
  runtime, added when the grader lands (adjacent grader session).

## Architecture

- **Driver:** the gstack `browse` daemon (Playwright-backed; compiled `browse.exe` + local Chromium). Commands
  used: `goto`, `js`/`eval` (read `video.currentTime`/`.paused`, query the DOM), `click`, `wait`, `screenshot`,
  `network`, `console`. No auth needed.
- **Target URLs:** built exactly like `render_course_preview_grade.article_player_url`:
  `LEARNWITH?contentUrl=<base>/<grade>/l<NN>/lesson.html&contentId=<L.id>&theme=indigo&ttsEnabled=true`.
- **Expected-state source of truth (offline, deterministic):** for each lesson we already know what SHOULD
  happen, from the repo:
  - One-Beat cues + option counts + correct option: `pipeline/data/one_beats.json`.
  - Gated checkpoints + correct answers: the lesson's `slots` (discrimination/predict_the_fix choices).
  - Content integrity: the `render_qc` defect classes (leaked placeholder, Cat-N, wall-of-text, etc.).
  The agent compares OBSERVED player state to this EXPECTED state and reports diffs. It never guesses truth
  from the page alone.

## Module layout

- `pipeline/player_test/expectations.py` — builds the per-lesson EXPECTED state from the repo (cues, option
  counts, correct answers, checkpoint answers, content assertions). Pure, offline, deterministic, tested.
- `pipeline/player_test/driver.py` — a thin Python wrapper over the `browse` CLI: goto, eval-JS, click-by-text,
  wait, screenshot, read-network. Returns structured observations. One place that knows the CLI.
- `pipeline/player_test/checks.py` — the check functions, each taking (observed, expected) -> Finding:
  - `check_video_loads`, `check_one_beat_pauses` (seek near each cue, play, assert pause + question + option
    count), `check_one_beat_answerable` (answer, assert resume), `check_content_renders`,
    `check_gate_locks_and_unlocks`.
- `pipeline/player_test/run.py` — orchestrates: for a grade, for each lesson, build expectations, drive the
  player, run the checks, collect Findings, write a report (JSON + a readable HTML/markdown summary + a
  screenshot per pause). Exit non-zero if any hard check fails.
- `pipeline/player_test/report.py` — renders the run into a per-lesson scorecard (pass/warn/fail per check,
  with the screenshot and the observed-vs-expected diff).

## What a "Finding" carries

`{lesson_id, grade, check, severity (pass|warn|fail), expected, observed, screenshot_path, note}`.
- **fail** = a real defect (video does not pause at a cue; wrong option count; broken content; gate does not
  lock).
- **warn** = player behavior worth knowing but not our bug (e.g. "player gates video progression",
  "One-Beat shows a Submit button").
- **pass** = observed matches expected.

## Personas (optional, phase 2)

The first build is a DETERMINISTIC checker (does the player do what the repo says it should). A later phase can
layer a Fable-5 "student" persona that navigates the lesson and rates clarity/experience, reusing
`sim_student_eval`'s persona models but pointed at the real player. Kept out of the first build to keep it
verifiable.

## Testing the tester

- `expectations.py` is unit-tested against `one_beats.json` + a known lesson (e.g. L01 -> 2 cues at 82/131,
  4 options each).
- `checks.py` functions are unit-tested with synthetic observed/expected pairs (no browser).
- `driver.py` gets one live smoke test (guarded so it is skipped when the daemon/network is unavailable).
- The whole run is exercised on ONE lesson (L01) end to end before fanning out to all 45.

## Guardrails

- Read-only against live surfaces: the agent navigates and clicks WITHIN a lesson; it never mutates the course,
  never touches the OneRoster/QTI APIs, never pushes.
- Deterministic truth: expected state comes from the repo, not from the page.
- Screenshots + observed JSON are saved for every pause so a human can audit any finding.
- No credentials used or required (the player surface is public).
- Grading stays deferred and clearly labeled; the agent never claims to have tested scoring.

## Build sequencing

1. `expectations.py` + tests.
2. `driver.py` + one live smoke test (already proven by hand today).
3. `checks.py` + tests.
4. `run.py` + `report.py`; exercise on L01 end to end.
5. Fan out to all G9 lessons, then G10-12; review the scorecard.
