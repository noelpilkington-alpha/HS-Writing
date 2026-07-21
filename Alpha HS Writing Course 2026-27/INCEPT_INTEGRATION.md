# Incept Integration Strategy

**Date:** 2026-07-20
**Author:** with Noel (HS Writing)
**Status:** Phases A-E BUILT + first live batch run (T7, 2026-07-21). 10 drawio diagrams bound; QC pass run + shelved (judge artifact); video machinery ready, runs after next full build. See "First live batch (T7)" below.
**Inputs:** `Incept/Incept API — Agent Guide.md`, live `GET /api/v1/options` (fetched 2026-07-20), 3 live probe calls, and our existing pipeline (`pipeline/lesson_contract.py` gates, `visual-design-protocol.md`, the Timeback QTI ceiling).

> **Access note:** the Incept API is reachable from this environment only with curl's `--ssl-no-revoke` flag (a Windows schannel cert-revocation quirk, not an auth issue). Base URL `https://v2.incept.school`; key in `Incept/Incept Production details.md`. Re-fetch `https://v2.incept.school/docs/agent-guide.md` each session (it changes often). No documented quota endpoint; check the developer portal (`/library/developer/`) for balance.

## What Incept is (and what it is NOT for us)

Incept is a **generation + independent-QC engine** for educational content: `article_text`, `article_with_diagram`, `image` (incl. editable `drawio`), `video` (voiceover/talking-head, content-only/interactive), `test_spec`, `test`, `question`, `worked_example`, `storyboard`. Covers subject `writing`, grades g9–g12. It has a **judge pipeline** (the `below_bar` flag + `judge_axes`) AND a standalone **QC-as-a-service** endpoint that scores content *we* author.

**The load-bearing constraint:** our lessons are not free-form content. They are `Lesson`/`Slot` objects that must pass 29 deterministic gates and render to Timeback-native QTI. Incept emits its own artifact shapes. So the correct architecture is almost never "let Incept author a whole lesson and push it." It is: **use Incept for the pieces our pipeline is weakest at, then run those pieces through our gates.** Incept is an upstream content source + an independent judge, not a replacement for our contract or our push.

## Probe results (3 live calls, 2026-07-20)

| Probe | Type / options | Result | Verdict |
|---|---|---|---|
| **QC** (req 5415) | `POST /qc`, `question`, our real G9 L01 slot-4 discrimination | **93/100, PASS**; correctness 97, type_contract 92, grade_fit 92 | ✅ independent judge confirms the T9 pilot fix; solved the item cold, read all 4 options incl. our deliberate because-trap + fence-sitter/question distractors |
| **drawio image** (req 5414, artifact 10890) | `image`, `image_subtype: drawio` | **100/100, below_bar false**; editable `.drawio` + deterministic PNG; exact crisp labels (SIDE / REASON / ARGUABLE CLAIM / "because"), 3-box color-coded layout, worked examples | ✅ delivers the editable-diagram capability our visual-design-protocol wanted and said image models CAN'T (no text garble) |
| **video** (req 5413, artifact 10892) | `video`, `kind: voiceover`, `mode: interactive` | **98/100, below_bar false**; `.mp4` (kling-v3.0-pro) + `captions.vtt` + 6 scene PNGs + `output_json` with `script` + **3 embedded `questions[]`** | ✅ generates the LS #5 Peter-Bates-style setup video WITH embedded questions; generation solved, DELIVERY still open (see below) |

All three cleared the quality bar with high scores on the first attempt. Grounding: the fast lane (QC ~instant, image ~5 min) and slow lane (video ~7 min here vs 45 min ETA) behaved as documented.

---

## Question 1 — Better course/lesson content

Three uses, ranked, all feeding our existing gated pipeline (not bypassing it):

**(a) QC-as-a-service = a free, independent second judge [highest value; use now].**
`POST /api/v1/qc` scores an artifact WE author (as JSON in our output shapes) and returns per-axis, per-quote `actionable` repair objects (`evidence_quote` → `why_it_fails` → `fix` → `pass_when`) — the same shape as our Tier-B adversarial judge, but from a model we didn't train and can't over-fit to. The probe proved it works on our real items (93/100). **Use it to double-judge:** the ~126 discrimination items from the #8 rollout, the FRQ/mastery prompts, and any lesson copy. It is a genuine second opinion on correctness/grade-fit that we would otherwise have to build. v1 is text/JSON only — perfect for our items.
- Integration point: a thin `pipeline/incept_qc.py` that posts a `Slot`/item as `question`/`article_text` JSON and records the verdict alongside our own gate results. Advisory, not a hard gate (external dependency; don't block the build on a network call).

**(b) `question` generation as distractor-authoring assist [directly relevant to the #8 rollout].**
The #8 rollout needs a 4th named-misconception distractor on 126 discriminations. Incept's `question` type (`interaction_type: multiple_choice`, `dok`, `difficulty`, `structure: bank` for 10–30 at once) can seed candidate distractors. Its interaction types (multiple_choice, text_entry, order, match, inline_choice, hottext) all map to Timeback-native QTI.
- **Guardrail:** seeds feed our authoring agents as raw material; they do NOT get pushed directly. They still pass `gate_structural_item` (exactly 4, one key, no lone-longest), anti-slop, and provenance. Incept accelerates authoring; our gates keep the bar.

**(c) `article_with_diagram` / `image (drawio)` for teach content [fills a real gap].**
Our teach cards are hand-authored prose + hand-SVG (Track A). The drawio probe shows Incept produces an **editable** diagram with exact labels — the thing the visual-design-protocol wanted and warned image models garble. Use it for the abstract writing-structure diagrams (claim anatomy, PROVE, weave, etc.) as editable sources we can tweak and re-render.

**Hard constraint on all three:** everything Incept generates re-enters through our contract (becomes `Slot` objects, passes the 29 gates, renders Timeback-native). Incept is upstream, not the push.

---

## Question 2 — Video content

**Incept generates the video the LS asked for (#5) — proven at 98/100.** The artifact is a bundle: `.mp4` + `captions.vtt` + scene PNGs + a segmented `script` + an embedded `questions[]` payload. So generation is solved, including the interactive/embedded-question variant.

**The open question is DELIVERY, not generation.** Whether Timeback's gated-reading player plays an *interactive* video (with in-video questions) versus stripping to a plain `.mp4` stimulus is unresolved — it is the same iframe/PCI ceiling flagged in the LS #5 analysis. Two sub-cases:
- Plain **voiceover `.mp4` as a stimulus slot** — most likely to render in the current player. Safe near-term target.
- **Interactive embedded-question video** — likely still needs the external-app / Platform3 player; log there, do not assume.

**Also: the video's `questions[]` may be redundant with our lesson checks.** Probe Q1 ("Which sentence is an arguable claim?") is nearly identical to our L01 slot-4 discrimination. So a binding step must RECONCILE the video's questions with the lesson's existing gated checks (dedupe, or use the video as pure teach and let the lesson's checkpoints assess). This is a curation decision — another reason video is its own stage.

### DECISION: video is a separate DOWNSTREAM stage, NOT in the generation loop

Add video **after the course is generated, QC-passed, and content-locked** — as its own deterministic stage keyed off the locked `Lesson` objects, never interleaved into the text/item build. Reasons:

1. **Content-lock:** a video narrates final copy. Generate it while copy still churns (which ours does — mid LS-fixes, mid #8 rollout) and every script edit re-renders a video. Lock the words, then film them.
2. **Don't couple a fast layer to a slow one:** text/items/diagrams iterate in minutes and are regenerated constantly; video is ~45 min/unit, slow lane, sequential drain. Baking video in makes a 98-lesson regeneration video-bound, so you stop iterating freely. Decoupled, you can rev the course 20× without touching video.
3. **Selection is a feature:** the LS ask is targeted (setup videos for foundational, visually-supportable concepts), not one-per-lesson. A post-pass is naturally a curation step (~10-20 videos); an in-build path drifts to "every lesson gets one."
4. **Delivery is an open bet:** don't couple shippable course content to an unresolved delivery dependency. A separate pass lets the course ship regardless; video slots in when delivery resolves.
5. **Two QC regimes stay clean:** course QC judges structure/items; video QC judges narration-matches-script/audio. Separate passes keep each honest.

**"Post-pass" is NOT manual/ad-hoc** — it is a dedicated pipeline stage: `video_targets` selection (which lessons + which slot) → Incept generate from the locked teach content → QC the result → reconcile embedded questions vs. lesson checks → bind (as an opening stimulus) + resolve delivery. The only thing that would tempt in-build video is "it interactive-plays in Timeback today," which is exactly what is still unverified — itself the argument for keeping it decoupled.

**Sequenced:**
1. Generate + QC + gate the course (text/items/diagrams) → **lock it** (in progress: LS-feedback rollout).
2. **Select** setup-video candidates (start L01 "arguable claim" — the diagram probe already proves the visual concept).
3. Generate video from the *locked* lesson → QC → confirm Timeback display → reconcile questions → bind.
4. If interactive-embedded-question video is blocked by the player, fall back to plain voiceover-as-stimulus; log the interactive version to the external-app/Platform3 track.

---

## Question 3 — Best use of OpenAI in our pipeline

`OPEN_AI_API_KEY` confirmed present in `HS Writing/.env` (Track B provider). Today the visual-design-protocol scopes OpenAI to **Track B — rare wordless illustrations only** (gpt-image-1), explicitly NOT diagrams (image models garble exact text like "thesis"/"because").

**Incept's drawio now covers the diagram/editable-image niche far better than anything OpenAI does for us.** So OpenAI's role narrows:
- **Track B wordless illustrations** (its current job): rare decorative/contextual pictures where no exact text matters. Incept also has `image_subtype: photo|illustration`, so even this may migrate to Incept — making OpenAI's *image* role largely superseded.
- **The durable, higher-value OpenAI use is as a cross-model DIVERSITY check in our ensemble — not images at all.** Our generation + Tier-B judging lean on Claude/Fable; Incept QC adds a second judge; adding **GPT as an independent second author or second judge** (the way the council uses multiple grounded perspectives) reduces single-model blind spots. Same logic as using Incept QC: model diversity catches what one model's bias misses.

**Net:** retire OpenAI's image role in favor of Incept drawio/image; keep OpenAI as an ensemble diversity model (author or judge), used sparingly where a second architecture genuinely de-risks a decision.

---

## Integration roadmap (BUILT — commits on `hs-writing-spec-baseline`)

| Phase | Work | Status |
|---|---|---|
| **A** | `incept_qc.py` — advisory second-judge; redacted receipts (scores/axes/flag only) | ✅ built `444bade` + `d72705d`; **ran live T7a, result shelved** (see below) |
| **B** | `incept_diagram.py` + `incept_diagrams.py` (`_INCEPT_DIAGRAMS`) — drawio → PNG, bound via `_content_card(img=)` | ✅ built `d6e87c5`; `fetch` live-shape fix `e46fa3d`; **10 diagrams bound `ad11cc8`** |
| **C** | `incept_question_seeds.py` — distractor seeds (raw material, gated downstream) | ✅ built `7a14149` (dry; not exercised live) |
| **D** | `incept_video.py` — post-lock video machinery (select → generate → fetch → reconcile → bind-note) | ✅ machinery built `a9534d6`; **runs AFTER next full build** (not exercised live) |
| **E** | `openai_diverse.py` — cross-model diversity author/judge; image role retired in favor of Incept drawio | ✅ built `b950c54` (dry; not exercised live) |

Shared transport `incept_client.py` (`35e7ecf`): dry-by-default, `--live` to spend, key redaction. 178 tests green; G9/G10/G11/G12 tier_a all clean.

## First live batch (T7, 2026-07-21)

**Diagrams (T7b/c) — SHIPPED.** 10 abstract writing-structure drawio diagrams generated live, all score 100 / below_bar false / labels verify_drawio-clean, bound into teach cards across G9-G12 (`Generated_Content/incept_diagrams/`, registry in `incept_diagrams.py`). Display-only, zero gate impact.
- **Noel review applied:** dropped the "weave vs LIST" split (no *what-NOT-to-do* panel in a first-encounter teach diagram — now a standing rule); regenerated weave positive-only. Kept the relevant_evidence funnel (set-aside facts ARE the concept).
- **em-dash discipline:** Incept's raw `alt_text` carried em dashes → alt is now HAND-AUTHORED in the registry (alt renders into the DOM). 4 diagrams also had em-dash captions → regenerated with a no-dash instruction.

**QC pass (T7a) — RUN, then SHELVED as a judge artifact.** All 219 canonical discrimination+predict items QC'd live (concurrent, 0 errors, ~26 min). Result: 209/219 "flagged" (mean 45) — **not actionable.** The same verified item (G9 L01 s3) scored 68 in the batch but 85/88/88/86/88 in 5 isolated re-runs (0/5 flagged, stdev 1.3): the judge is **non-deterministic + load-sensitive**, and `grade_fit` penalizes deliberate foundational simplicity ("grade 4-6, too easy") — the same over-flag pattern as the Fable-5 readiness judge. Receipts NOT committed (would imply meaning). If revisited: neutral prompt + 3-sample median + correctness-only triage (~3× quota). **QC is best treated as directional-only, not a shortlist.**

**Live-learned facts (confirmed vs the plan's guessed field names):**
- QC POST returns `{request_id, status:pending}`; poll to terminal `status:"succeeded"`; **score/axes are NESTED under `verdict`** (was read top-level → fixed `d72705d`).
- Generate poll terminal envelope carries the artifact id under **`artifact_id`**, not `id`.
- Discrimination options live in **prose/bank** for 154/299 slots (empty `choices[]`); QC now resolves them like the renderer (`d72705d`).
- drawio is **slow-lane**: 3-4 min/diagram, and under concurrency several exceeded a 3-min poll window and needed re-polling. Latency: QC ~25-31s/item; POST ~0.8s.
- Artifact files arrive under `files[]` as **presigned S3 URLs** (secrets), not inline bytes → `fetch` downloads by extension (`e46fa3d`).

## Guardrails (standing)
- Everything Incept generates re-enters our contract and passes the 29 gates + anti-slop + provenance before it ships. Incept output is a SOURCE, not a bypass.
- Honor `below_bar: true` — never treat a below-bar artifact as vetted; re-generate or human-review.
- Generation/QC POSTs are outward-facing calls that spend quota and send our content to an external service — each requires explicit go, per the standing push rule. Reads (`/options`, docs, artifact detail) are safe.
- Never bind an artifact by prompt/title — always by `request_id`/`artifact_id`.

## Open items
- **Diagram deploy path** — bound img src resolves to `{base_url}/{lesson-slug}/incept_diagrams/<file>.png`; the next real course deploy must serve `Generated_Content/incept_diagrams/` reachable under each lesson base. Confirm at push time.
- **Video stage (Phase D)** — machinery built + tested; runs AFTER the next full content lock. Delivery in Timeback (interactive vs plain voiceover-as-stimulus) still unresolved — test one `.mp4` as a stimulus end-to-end first.
- **QC judge recalibration** — if we want an actionable QC shortlist, needs neutral prompt + multi-sample median + correctness-only triage. Until then, QC is directional-only, not a bulk-fix source.
- **Incept quota/billing** — no API endpoint; confirm via the developer portal.
- **Live artifacts (T7):** 10 bound diagrams = Incept artifacts 11267/11272/11278/11280/11290/11295/11301/11306/11314/11285; PNGs committed under `Generated_Content/incept_diagrams/`. Probe artifacts still at `C:/tmp/incept_probe/`.
