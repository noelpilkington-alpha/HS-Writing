# Deploy the HS Writing grader to AWS Lambda — click-by-click console walkthrough

**Goal:** get the grader running at a `https://<id>.lambda-url.<region>.on.aws/` URL — an allowlist-approved
host Timeback accepts (unlike our current Render host). ~20-30 min. Region: use **us-east-1** unless the
platform lives elsewhere.

**Only one step isn't pure clicking:** building the deployment zip must happen on Linux (Lambda is Linux; a
Windows-built zip fails at import on the `pydantic-core` binary). You'll do that in **AWS CloudShell** — one
paste, still inside your console. Everything else is console clicks.

---

## STEP 0 — Get the code into CloudShell + build the Linux zip

CloudShell is the `>_` terminal icon in the top-right nav bar of the console. Click it; wait for the shell.

You need the `api/` folder in CloudShell. Two options:

- **If the grader repo is on GitHub** (the HS-Writing repo): in CloudShell run
  `git clone <repo-url> hsw && cd hsw/api`  (you may need a token for a private repo).
- **If not / simpler:** in CloudShell click **Actions → Upload file**, upload a zip of your local
  `c:\Users\noelp\HS Writing\api` folder, then `unzip` it and `cd` into it.
  ⚠ Before zipping locally, DELETE `api/.env` from that copy — it holds the funded key and must not travel in
  the code bundle (the key goes in as a Lambda env var in Step 3). Also skip `__pycache__/`.

Then build the zip (paste as one block):

```bash
# from inside the api/ directory
rm -rf build && mkdir build
pip install -r deploy/aws-lambda/requirements-lambda.txt -t build/   # deps, Linux-correct
cp -r *.py grader_engine build/                                       # app code (no .env, no deploy/)
rm -f build/.env
cd build && zip -r ../grader-lambda.zip . -x '*/__pycache__/*' '*.pyc' && cd ..
ls -lh grader-lambda.zip     # note the size; if >50MB you'll upload via S3 (Step 2 note)
```

Leave CloudShell open — you'll grab the zip from here in Step 2.

---

## STEP 1 — Create the function

1. Console → search **Lambda** → open it. Confirm the **region** (top-right) is us-east-1.
2. **Create function** (orange button).
3. Choose **Author from scratch**.
4. **Function name:** `hs-writing-grader`
5. **Runtime:** **Python 3.12**
6. **Architecture:** **x86_64** (leave default — must match how the zip was built; CloudShell is x86_64, so this is correct).
7. **Permissions** → expand *Change default execution role*:
   - Leave **Create a new role with basic Lambda permissions** selected (this is the common case — it makes a
     role that can write CloudWatch logs, which is all the grader needs).
   - *If your org blocks role creation* and you get an error here, that's the one thing to escalate: ask for an
     existing Lambda execution role with basic logging and pick **Use an existing role** instead.
8. **Create function.** You land on the function's page.

---

## STEP 2 — Upload the code

1. On the function page, the **Code** tab is open. On the right, **Upload from ▾**.
2. If `grader-lambda.zip` is **≤ 50 MB**: choose **.zip file**, **Upload**, and pick the zip.
   - To get the zip out of CloudShell to your laptop: in CloudShell, **Actions → Download file**, path
     `~/hsw/api/grader-lambda.zip` (or wherever you built it). Then upload it here.
3. If it's **> 50 MB** (likely, with all deps): upload via S3 instead —
   - In CloudShell: `aws s3 cp grader-lambda.zip s3://<some-bucket-you-can-write>/grader-lambda.zip`
     (use any bucket in the same account/region, or create one: `aws s3 mb s3://hsw-grader-deploy-<something>`).
   - Back in Lambda: **Upload from ▾ → Amazon S3 location**, paste the `s3://…/grader-lambda.zip` URL.
4. **Save.** The console shows the uploaded files.

---

## STEP 3 — Point Lambda at the handler + set config

1. **Configuration** tab → **General configuration** → **Edit**:
   - **Handler:** `lambda_handler.handler`   ← critical; this file is at the zip root.
   - **Memory:** **1024 MB** (or more).
   - **Timeout:** **1 min 0 sec** (Opus scoring calls take ~10-40s; the default 3s WILL fail).
   - **Save.**
2. **Configuration** tab → **Environment variables** → **Edit** → **Add environment variable** for each:
   - `ANTHROPIC_API_KEY` = the **funded** key (the one in `c:\Users\noelp\HS Writing\.env`, sha8 61cc625b —
     the value, not the fingerprint). ⚠ Add it ONCE; a duplicate/stray key silently shadows it → "credit
     balance too low" even though it's funded.
   - `ANTHROPIC_PROVIDER` = `anthropic`   (guards against a Bedrock default → no boto3/AWS-creds path needed).
   - (Do NOT set `GRADING_API_KEY` — leaving it unset keeps `/score` open, which is what Timeback needs.)
   - **Save.**

---

## STEP 4 — Create the function URL (this is the deliverable)

1. **Configuration** tab → **Function URL** → **Create function URL**.
2. **Auth type:** **NONE**.
   - Correct and intended: Timeback's ExternalApiScore customOperator calls the grader **keyless** (it has no
     way to send an API key). The `/score` route is safe to expose this way; the grader stores nothing.
3. **Additional settings → CORS:** you can leave CORS off — Timeback calls this server-to-server, not from a
   browser. (Enabling it does no harm.)
4. **Save.** Copy the **Function URL** it shows: `https://<id>.lambda-url.<region>.on.aws/`. **This is what
   you paste back to me.**

---

## STEP 5 — Smoke test (CloudShell, keyless)

Paste in CloudShell, substituting your URL. First hit warms a cold start (a few seconds):

```bash
URL="https://<id>.lambda-url.us-east-1.on.aws"
# sentence-grain: expect score 3.0 / maxScore 3.0
curl -sX POST "$URL/score?grain=sentence&frq_type=writing" -H "Content-Type: application/json" \
  -d '{"response":"Schools should ban phones, because notifications pull attention from learning.",
       "rubric":"rc.staar","grade":9,"prompt":"Write one arguable claim.","passage":""}'
echo
# essay-grain (no grain=): a short answer scores ~0 (too short for the essay engine) — proves routing
curl -sX POST "$URL/score" -H "Content-Type: application/json" \
  -d '{"response":"Phones are bad.","rubric":"rc.staar","grade":9,"prompt":"Write an essay.","passage":""}'
```

Expected: the first returns JSON with `"score":3.0` and a `note` mentioning `sentence_writing`; the second
returns a low score. If you get a 5xx or an import error, see Troubleshooting.

---

## STEP 6 — Hand back

Paste the **Function URL** into the chat. I will then:
- smoke-test it live from my side,
- re-point the wirer's Render base to it (paragraph/essay items → this Lambda; sentence items already route to
  the native grader),
- re-wire the live mastery items and verify the operator lands in each item's stored XML.

---

## Troubleshooting (only if a step errors)

- **"Unable to import module 'lambda_handler'"** → the handler string is wrong, OR the zip was built on
  Windows (wrong `pydantic-core` binary). Rebuild in CloudShell (Step 0); confirm handler = `lambda_handler.handler`.
- **502 / "Internal Server Error" on first call** → almost always the timeout (raise to 60s+) or a missing
  `ANTHROPIC_API_KEY`. Check **Monitor → View CloudWatch logs** on the function for the real error.
- **"credit balance too low"** despite a funded key → a duplicate/stray `ANTHROPIC_API_KEY` env var is
  shadowing it, or you pasted the unfunded key. Confirm the value matches the `.env` one (sha8 61cc625b).
- **403 on create-function (role)** → your account blocks IAM role creation; ask for an existing Lambda
  execution role and use **Use an existing role** in Step 1.7.
- **Cold starts** feel slow (~2-5s first hit after idle). Fine for testing. For production, set **provisioned
  concurrency** later (Configuration → Concurrency) — not needed now.
```
