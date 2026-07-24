# HS Writing Grader — AWS Lambda deploy package

**Purpose:** deploy the existing G9-12 writing grader (the FastAPI app in `api/`) behind an **AWS Lambda
function URL**, so Timeback's QTI grader allowlist accepts it. This is the same service that runs on Render
today (`hs-writing-grading.onrender.com`) — no app-logic changes, just a Lambda entrypoint.

## Why this move (context for the engineer)

Timeback validates the grader hostname on every graded QTI item (`validateCustomOperatorUrls` in
`qti-xml-item-processor.ts`). Empirically verified 2026-07-24:

| Host pattern | Allowlist |
|---|---|
| `*.onrender.com` (current) | ❌ blocked → items can't carry the grader |
| `*.alpha-1edtech.ai`, `*.cloudfront.net`, bare apexes | ❌ blocked |
| **`*.lambda-url.*.on.aws`** | ✅ approved |
| `*.execute-api.*.amazonaws.com` (API Gateway) | ✅ approved |

A Lambda **function URL** is the simplest approved option and needs no allowlist request. It also *is* the
planned AWS migration, not a throwaway step.

## What the service does

- One endpoint matters for Timeback: **`POST /score`** (the `com.alpha-1edtech.ExternalApiScore` target).
  It is **keyless** by design (the customOperator can't send an API key) — the app exempts `/score` and
  `/timeback/*` from auth. Everything else stays behind the `GRADING_API_KEY`.
- Request (defensive superset): `{response, rubric, grade, prompt, passage}` + query params baked into the
  URL by the course wirer: `?grain=sentence|paragraph`, `&frq_type=writing|revision`, `&mode=analysis`
  (rc.4trait analysis tasks only).
- Engine: the vendored `grader_engine/` (SBAC / Regents-4trait essay engines + sentence/paragraph panels +
  grain routing). **Anthropic-direct** (no Bedrock/boto3).

## Package contents

```
api/                          <- zip/container root = this whole dir
├── main.py                   FastAPI app (unchanged; /score exemption confirmed)
├── external_score.py         the /score ExternalApiScore endpoint
├── grader_engine/            vendored scoring engine (panels + routing)
├── requirements.txt          Render/local deps
└── deploy/aws-lambda/
    ├── lambda_handler.py      Mangum entrypoint  ->  handler = lambda_handler.handler
    ├── requirements-lambda.txt runtime deps (adds mangum)
    └── README.md              this file
```

The Lambda deployment package must include `main.py`, `external_score.py`, `grader_engine/`, and this handler.
Simplest: zip the whole `api/` dir (it already contains everything), install `requirements-lambda.txt` into
the package, set the handler path below.

## Deploy steps (function URL)

1. **Build the package** (container image recommended for size; zip works too):
   - Handler: `lambda_handler.handler` (i.e. `api/deploy/aws-lambda/lambda_handler.py`). If your build flattens
     to the zip root, adjust the handler path accordingly — `lambda_handler.py` puts the `api/` root on
     `sys.path` itself, so it's robust to either layout.
   - Runtime: Python 3.12. Install `deploy/aws-lambda/requirements-lambda.txt`.
2. **Env vars on the function:**
   - `ANTHROPIC_API_KEY` = the funded key (same one Render uses; sha8 on file with Noel). REQUIRED.
   - `ANTHROPIC_PROVIDER` = `anthropic`  (explicit; guards against a Bedrock default).
   - `GRADING_API_KEY` = optional; only gates the non-`/score` admin routes. Leave unset for a pure grader.
   - Do NOT set a second/stray `ANTHROPIC_API_KEY` anywhere — a duplicate silently shadows the funded key.
3. **Config:** memory ≥ 1024 MB, timeout ≥ 60s (Opus scoring calls take ~10-30s; the platform's grader call
   should tolerate this). Reserved/provisioned concurrency optional — cold start adds a few seconds.
4. **Create a function URL** (Auth type: NONE — the endpoint is keyless by design; Timeback calls it directly).
   This yields `https://<id>.lambda-url.<region>.on.aws/`.
5. **Smoke test** (keyless, real HTTP):
   ```bash
   curl -sX POST "https://<id>.lambda-url.<region>.on.aws/score?grain=sentence&frq_type=writing" \
     -H "Content-Type: application/json" \
     -d '{"response":"Schools should ban phones, because notifications pull attention from learning.",
          "rubric":"rc.staar","grade":9,"prompt":"Write one arguable claim.","passage":""}'
   # expect: {"score":3.0,"maxScore":3.0,...,"note":"grain=sentence ... sentence_writing ..."}
   ```
   Then the essay path: same body without `?grain=` → scores on the essay engine.

## Hand the URL back to the course session

The deliverable is the **function URL base** (e.g. `https://<id>.lambda-url.us-east-1.on.aws`). The course
wirer bakes `/score` + the routing query params onto it and re-wires every mastery item (as XML — see below).
Give that base URL to the course session; nothing else on the course side needs the engineer.

## Note for the course-side re-wire (already coded, not the engineer's job)

Once the URL is known, `pipeline/g9_wire_grader.py` + `course_push_mastery_v3_1.py` re-wire the live items.
Two fixes already landed there (2026-07-24): (a) the wirer now emits **XML-format** items so the customOperator
survives in the executable rawXml (a JSON push silently strips it — CRITICAL RULE 1), and (b) the URL builder
is idempotent (no doubled query params). The re-wire is gated only on this URL.
