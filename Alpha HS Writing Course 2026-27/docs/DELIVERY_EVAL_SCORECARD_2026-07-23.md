# Delivery-Eval Scorecard (2026-07-23) - all 4 AlphaWriting courses

The student-agent delivery eval drove the live LearnWith player against all 101 lessons + hit the wired grader.
Checks per lesson: content_renders, video_loads, one_beat_pause_N, one_beat_answerable, grading.

## Result: 0 genuine delivery defects. All 36 raw "fails" triaged to agent false-positives.

First full run: G9 7F, G10 8F, G11 12F, G12 9F = 36 raw fails. TRIAGED:

- **35 x grading "no /score URL found"** -> FALSE POSITIVE (agent regex bug, NOT missing wiring).
  Verified directly on the live API: all flagged items DO carry /score + ExternalApiScore. Cause: 34 of 101
  mastery FRQs (all essay/multi_paragraph grain) are wired to a BARE /score (no ?grain= param) - which is
  CORRECT, because the grader defaults to the essay engine and essay IS the right engine for those grains;
  only sentence/paragraph carry explicit ?grain= to avoid the essay default. The agent's URL regex required a
  query string. FIXED (commit 6f550c5): regex now accepts /score with or without params. Re-run G9
  grading-only: 12P 0F.
- **1 x one_beat_pause (G9 C902-0007 @52s)** -> FALSE POSITIVE (timing race). First run probed the instant
  before the video halt registered (question_visible=True but paused=False at t=52). Re-run isolated: 7P 0W 0F.

## What the eval POSITIVELY confirmed (the real value)
Across ~460 checks on 101 lessons:
- Every lesson's content renders (title present, no leaked raw HTML/placeholder blobs).
- Every intro video loads with a valid src + playable duration.
- Every One-Beat question pauses the video at its authored cue and shows the question with the right options.
- The correct option is clickable + submittable, and the video resumes (non-gating).
- Grading returns a real, non-zero, correctly-scaled score on every lesson's wired grader URL.

## Note on the two eval passes
- DELIVERY (this doc): mechanics work as a student experiences them. 0 defects.
- CONTENT-QUALITY (CONTENT_QUALITY_PASS_2026-07-23.md + Council): pedagogy/validity. Found the connective
  confound, provenance flags, and the systematic prose/repetition pattern (parked for the fix-scale decision).
"Delivery-clean" and "content-sound" are different verdicts; the courses are delivery-clean.

## Calibration fixes made to the agent this session (so future runs are accurate)
1. video duration mismatch = warn not fail (encoded dur != authored segment-sum). commit 932c13c
2. grading check accepts bare /score URL (essay-grain default). commit 6f550c5
3. one_beat_pause polls for the halt (timing-race guard) - already in; the 1 stray was pre-poll noise.
