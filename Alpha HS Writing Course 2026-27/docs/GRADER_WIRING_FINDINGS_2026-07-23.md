# Grader End-to-End Check — Findings (2026-07-23)

Focused verification of grading on the freshly-pushed AlphaWriting G9-G12 courses. Grader:
`https://hs-writing-grading.onrender.com/score`. Two defects found; one is grader-side, one is our-side.

## What passed

- **Wiring present.** Every live mastery FRQ carries the `ExternalApiScore` customOperator, the grader URL with
  routing params (`?grain=<unit>&frq_type=<type>`), and the rubric in metadata. Verified on live items.
- **Essay engine works.** An essay-length `rc.staar` argument scored 4.0/5 (SBAC 8/10 breakdown), calibrated.
- **`rc.4trait` works.** An essay-length `rc.4trait` response scored 12.0/24 via `panel_ccss` (Regents
  4-criterion). This is the rubric G11/G12 SHOULD use (see Defect 2).
- **Grader reachable.** 200 after a cold-start (Render free tier, ~40s first hit).

## Defect 1 (GRADER-SIDE) — rc.staar ignores `grain`; sentence/paragraph tasks score 0

**Repro:** POST `/score?grain=sentence&frq_type=writing` with a valid one-sentence arguable claim:
```json
{"response":"Schools should ban phones during class, because constant notifications pull students attention away from learning.",
 "rubric":"rc.staar","grade":"9","prompt":"Write one arguable claim: take a side and give a reason.","passage":""}
```
**Result:** `score 0.0 / 5.0`, feedback *"too short to score as a full essay yet"*, note *"rc.staar item scored
via SBAC engine (argumentative)"*.
**Confirmed cause:** `grain=sentence` and `grain=essay` return the IDENTICAL 0.0 for the same short response.
The grader routes ALL `rc.staar` tasks to the SBAC **essay** engine regardless of the `grain` query param, and
the essay engine rejects anything under essay length.

**Impact (large):** sentence- and paragraph-grain mastery is the majority of early lessons. Every such PP100
would score 0 and NO student could test out, even with a perfect answer. Affected mastery-task counts:
- G9: 12 sentence-writing + 3 sentence-revision + 5 paragraph-writing + 3 paragraph-revision = **23 of 29**
- G10: 7 sentence-writing + 3 sentence-revision + 3 paragraph-writing + 5 paragraph-revision = **18 of 25**
- G11: 10 sentence + 8 paragraph (rc.ap, also Defect 2) = **18 of 31**
- G12: 3 sentence + 2 paragraph (rc.ap, also Defect 2) = **5 of 16**

**Owner:** the grader service (`Writing_Test_Grader/grader`, `api/external_score.py` routing / SBAC alias).
Our Timeback items correctly send `grain=sentence`; the grader is not honoring it. The grader's regeneration
contract note (in `g9_wire_grader.py`) says sentence -> "panel sentence scorers (Skill/Answer + Conv)" and
"paragraph is reserved (grader 501 until G9-12 calibrated)" — so the intended sentence/paragraph engines exist
in design but the live route ignores grain and falls through to SBAC essay.

**Fix (grader-side):** route `rc.staar` (and `rc.4trait`) by the `grain` param to the sentence/paragraph
scorers; only `grain=essay|multi_paragraph` should hit the essay engines. Until then, sentence/paragraph
mastery is un-passable.

## Defect 2 (OUR-SIDE) — G11/G12 wired with deprecated `rc.ap` (503)

**Repro:** POST `/score` with `"rubric":"rc.ap"` (any grain):
**Result:** `HTTP 503`, `{"detail":"rc.ap (AP Lang Row A/B/C) is uncalibrated and superseded: G11/G12 now use
rc.4trait (Regents 4-criterion CCSS). Live: rc.sbac (G9/10), rc.staar (G9/10), rc.4trait (G11/12)."}`

**Confirmed:** the live G11 item `ACC-W1112-L-G11-C1101-0001-MASTERY-FRQ` carries `metadata rubric: rc.ap`.
All G11 (31) + G12 (16) mastery items were wired with `rc.ap`, which the grader now rejects with 503. So
EVERY G11/G12 mastery task fails, at all grains, not just sentence.

**Impact:** all 47 G11/G12 mastery tasks return no score (503).

**Owner:** OURS. The G11/G12 lessons declare `rubric_ref="rc.ap"`; the grader deprecated it to `rc.4trait`.
Verified `rc.4trait` scores correctly (12/24, panel_ccss). Fix on our side: change the G11/G12 lessons'
`rubric_ref` from `rc.ap` to `rc.4trait`, then re-wire (PUT) the 47 live mastery FRQs (no content re-push;
`g9_wire_grader`-style PUT of the customOperator + rc.4trait rubricBlock). `_RUBRIC_BLOCKS` in
`g9_wire_grader.py` also needs an `rc.4trait` block (currently only has rc.staar / rc.ap).

## Layer 3 (runtime roundtrip) — DEFERRED

Verifying a score flowing back through the live Timeback player (not just a direct grader curl) is deferred
until Defect 1 is fixed (per Noel) — testing sentence-grain now would only confirm the 0. Once sentence-grain
scores, run the full player-submit -> grader -> score-return roundtrip (this is what the Timeback-player
testing agent will automate).

## Summary for the grader session

1. **Grader-side (blocking):** `rc.staar`/`rc.4trait` must route by `grain`; today all non-essay grains fall to
   the essay engine and score 0. Sentence + paragraph mastery is un-passable across all grades.
2. **Our-side (we fix):** G11/G12 must move `rc.ap` -> `rc.4trait` (deprecated, 503) in the lessons + re-wire
   the 47 live items. `rc.4trait` is confirmed live and scoring.

Nothing about the course structure or content is wrong; both issues are in the scoring layer.
