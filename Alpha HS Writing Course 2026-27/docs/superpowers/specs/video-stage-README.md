# Video stage (Phase D): machinery-only, runs AFTER the next full content build

`pipeline/incept_video.py` is the post-lock VIDEO-stage machinery for the Incept integration. It
generates a short instructional voiceover video from a LOCKED lesson's teach text, fetches the mp4 +
captions + scene stills to a local dir, reconciles the video's embedded questions against our gated
discriminations, and records how a video would bind.

## This stage is machinery ONLY

Building and testing this stage does NOT generate or bind any video. Everything is dry-by-default: no
module makes a real Incept POST unless invoked with `live=True`, and the test suite never touches the
network.

Per Noel, video is POST-CONTENT-LOCK by design: it runs AFTER the next full content build, not during
it. The reason is ordering. A video is authored FROM a lesson's locked teach text; if we generated
video before the content settled, every content edit would strand a stale video. So we build the
machinery now and run the live path only once content is locked.

## Run order (all steps after content is locked)

1. Build and LOCK the content (author lessons, then freeze the teach text).
2. QC the content through the existing 30-gate contract + the advisory Incept QC (`incept_qc.py`).
3. Select the video targets. `VIDEO_TARGETS` in `incept_video.py` is a CURATED seed list of
   `(short_lesson_id, slot_idx)` tuples: the LS-flagged foundational lessons that get a video first
   (starting with G9 L01, `C901-0001`), NOT every lesson. `video_targets("g9")` returns the g9 subset.
4. `generate_video(lesson_id, live=True)` for each target. It derives the prompt from the locked
   lesson's teach text and POSTs a `video` generation (`options={"kind":"voiceover","mode":"content_only"}`).
   Honor `below_bar`: do not proceed with an artifact whose `below_bar` is true; regenerate instead.
5. `fetch_video(artifact_id, dest, live=True)` downloads the mp4, writes `captions.vtt` from the
   script narration, and downloads the scene stills into a LOCAL dir.
6. `reconcile_questions(video_json, lesson)` flags any embedded video questions that DUPLICATE an
   existing discrimination stem. A content-only voiceover carries no embedded questions and returns an
   empty list; a mode that DOES carry questions surfaces duplicates for the human to resolve so the
   video's checks never shadow our gated discriminations.
7. HUMAN REVIEW. A person watches the video, reviews the reconcile flags, and approves or rejects.
8. Bind the approved video as an OPENING STIMULUS CARD before the first teach segment.
   `bind_note(lesson_id, artifact_id)` records how the bind would work; actual binding is a separate,
   reviewed step.

## Delivery caveat

Interactive-video-in-Timeback is UNRESOLVED (the player question is open, not assumed). The near-term
delivery target is plain VOICEOVER-AS-STIMULUS: the mp4 plus its captions, bound as an opening
stimulus card, NOT an interactive in-player video. `bind_note` carries this caveat on every record.

## Secret hygiene

The Incept API key and the presigned S3 URLs in a video artifact (`output_file_url`, `files[].url`)
are secret-bearing. `fetch_video` downloads BYTES to a local dir only; no presigned URL, key, or other
secret is ever written into a committed file, a test fixture, a receipt, or this document. Test
fixtures use synthetic stems only.
