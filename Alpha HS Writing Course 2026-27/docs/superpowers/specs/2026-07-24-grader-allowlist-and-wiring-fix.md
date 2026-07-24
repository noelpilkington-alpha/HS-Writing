# Grader allowlist + item-wiring fix

**Date:** 2026-07-24
**For:** the grader session (Noel will fix the grader there)
**Trigger:** Live review of G9 L01 on Timeback surfaced three grading-related defects. Investigation traced the
core one to the grader host not being on Timeback's approved-grader allowlist.

## The three reported symptoms (G9 L01, live)

1a. **Article awards no XP / reports no accuracy.**
1b. **In-article written responses are not graded** (so they don't prepare students for the mastery check).
2.  **Submitting the first mastery-check response fails** with "Something went wrong / Failed to submit answer."

## Root cause (evidence-backed)

**All auto-grading is blocked because the grader hostname is not on Timeback's approved-grader allowlist.**

Verified by POSTing a minimal grader item as XML to `https://qti.alpha-1edtech.ai/api/assessment-items`. The
API returned HTTP 500 with the exact message:

> Custom operator "com.alpha-1edtech.ExternalApiScore" definition URL hostname is not in the approved grader
> allowlist: "hs-writing-grading.onrender.com"
> at Object.validateCustomOperatorUrls (/app/src/utils/qti-xml-item-processor.ts:267:15)

Consequences observed on live items:
- **JSON-format push** (what our pipeline uses via `wire_payload`): the API accepts the item (200/201) but
  **silently strips** the disallowed `customOperator`. The stored `rawXml` ends up with only an empty template:
  `<qti-response-processing template="https://purl.imsglobal.org/spec/qti/v3p0/rptemplates/custom.xml"/>` —
  no grader. The grader config survives ONLY in the item's JSON `responseProcessing` field (cosmetic; the
  runtime executes the rawXml). This is why our earlier "grading wired" verification passed (it checked the
  JSON field) while the live item cannot grade.
- **XML-format push**: hard 500 with the allowlist error above.
- Net: the runtime finds no grader operator in the executable XML → mastery submit fails (symptom 2), and
  in-article writes were never wired at all (symptom 1b).

The grader **service itself is healthy** — `GET https://hs-writing-grading.onrender.com/score` returns 405
(Method Not Allowed; it wants POST) in ~0.4s. The block is purely the Timeback allowlist, not the grader.

Currently wired definition on live items (JSON field only, stripped from XML):
`https://hs-writing-grading.onrender.com/score?grain=sentence&frq_type=writing`

## What the grader session needs to do

**PRIMARY: get the grader host onto Timeback's approved-grader allowlist.** Other external graders ARE
allowlisted on this platform (e.g. the AP builds used external graders), so this is a known, supported path —
our host simply isn't registered yet. Options, in preference order:
1. **Add `hs-writing-grading.onrender.com` to the allowlist** via whoever manages Timeback's grader allowlist
   (the validator is `qti-xml-item-processor.ts::validateCustomOperatorUrls`). Confirm whether the allowlist is
   global or per-tenant, and get the exact approved value/pattern back.
2. **OR re-host / proxy the grader on an already-approved host pattern** (find what patterns are allowed —
   likely `*.alpha-1edtech.ai` and/or `*.lambda-url.*.on.aws`, matching the AP graders) so no allowlist change
   is needed. If we take this route, the grader URL baked into items changes and every mastery item must be
   re-wired to the new host.

Either way, the deliverable back to the course session is **the exact approved grader base URL** to bake into
items.

### Grader routing contract (unchanged; for reference when re-hosting)

Items route the grader by query params baked into the definition URL (see `pipeline/g9_wire_grader.py`):
- `?grain=sentence|paragraph` (essay/multi_paragraph omit grain → grader defaults to essay)
- `&frq_type=writing|revision`
- `&mode=analysis` only for rc.4trait analysis tasks (else grader defaults argument)
- `rubric_ref` stays in the item's `rubricBlock` (rc.staar for G9/10, rc.4trait for G11/12).

The approved host must serve the same `POST /score` rubric-based contract
(`{response, rubric, grade, prompt, passage}`), so re-hosting is host-swap only, not a contract change.

## What the COURSE session will fix once the approved host is known (tracked separately, not here)

- **`wire_payload` must emit XML-format items**, not JSON. Per Timeback CRITICAL RULE 1 the JSON→XML converter
  drops the customOperator even for allowlisted hosts, so the operator must be written literally as
  `<qti-custom-operator class="com.alpha-1edtech.ExternalApiScore" definition="<approved-url>">` inside the
  `<qti-response-processing>` block, POSTed/PUT as `{"format":"xml","xml":...}`. Verify post-push that the
  stored `rawXml` contains `custom-operator` + the grader URL (the check our earlier verification missed).
- **Fix the doubled query-param bug**: the L01 pilot passed an already-parameterized URL into `wire_payload`,
  which appended params again (`...&grain=sentence&frq_type=writing&grain=sentence&frq_type=writing`).
  `_grader_url_for` / `normalize_grader_url` must be idempotent on an already-parameterized URL.
- **Re-push mastery items** (L01's 30 forms + the 59 quick-bank lessons' forms + all single-form mastery items
  across G9-G12) once the host + XML wiring are correct.
- **Decide in-article write grading (symptom 1b):** in-article `production_frq`/`diagnosis_frq` items currently
  wire NO grader (only `completionStatus=completed`). Decide whether to wire the same external grader into
  in-article scored writes so they give feedback and prepare students for the mastery check (the reported
  desire), or keep them ungraded practice. This is a content/build decision, gated on the same allowlist.

## Open question for symptom 1a (article XP / accuracy) — needs a platform answer

The article resource carries `metadata.xp = 28` but is `kind=text` (a reading) with no scored questions, so the
platform reports no accuracy and (apparently) awards no XP. Clarify with the platform how a reading/article
awards XP: is XP gated on an accuracy signal that a pure-text article cannot produce, or does completion of the
gated reading (the checkpoint gates) award XP through a different mechanism? This is a platform/config question,
not a course-content defect — no item edit on our side changes it. (Possibly related: the article component-
resource has no `lessonType` set; worth confirming whether a reading needs a specific lessonType to accrue XP.)

## Status of the live pilot banks (caveat)

L01's 30-form mastery bank and the 59 depth-3 quick banks are LIVE and correctly wired at the OneRoster/bank
layer (round-robin structure is sound). But NONE of them will grade until the allowlist is resolved — so
Codex mastery testing + the round-robin observation are blocked until then. The article/reading half (video,
checkpoints, gating) is unaffected and testable now.
```
