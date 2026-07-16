# Graded G9 Pilot — Deploy & Wiring Runbook

**Date:** 2026-07-16
**Goal:** every G9 FRQ a student submits routes to a working grader and returns a score + feedback.
**Status:** all code-side prep is done and dry-run-clean. The remaining steps touch the grader service (Render) and the live Timeback platform. **Nothing live-POSTs until Noel's explicit go.**

---

## What "grade all FRQs" covers

| Set | Count | Item id shape | Rubric | Grader path |
|---|---|---|---|---|
| In-lesson scored production FRQs | 75 | `<lesson>-S{i}-production_frq` | rc.staar | calibrated (panel_staar) |
| PP100 mastery instruments | 27 | `<lesson>-MASTERY-FRQ` | rc.staar | calibrated (panel_staar) |
| **Total graded items** | **102** | | all rc.staar | |

All 102 target the **verified 27-lesson v3.1 course** (same source of truth as the deterministic floor + fact-verification). rc.staar is the grader's **calibrated** STAAR path (Dev/Org 0-3 + Conventions 0-2 = 5). rc.ap is deliberately uncalibrated (503) — not used by G9.

---

## Prep already complete (committed)

- ✅ `g9_wire_grader.py` — endpoint fixed to live `/score` (was stale `/timeback/score`); glob fixed to the verified v3.1 set (was matching 55 stale/dup files → 158 phantom FRQs; now 75 real across 27 lessons). Dry-run clean.
- ✅ `g9_push_mastery_v3_1.py` — URL helper delegates to the fixed `normalize_grader_url`; already used the v3.1 glob. Dry-run clean (27 instruments).
- ✅ `grader_smoke.py` — end-to-end health + round-trip + strong-vs-weak accuracy sanity, against the real `/score` contract.

---

## Runbook (execute in order)

### Step 1 — Deploy the grader  · **blocker**
The service is **not currently reachable** (`writing-grader.onrender.com` returns 404 — our code isn't deployed there).
- Deploy `Writing_Test_Grader` (Dockerfile: `uvicorn api.app:app --host 0.0.0.0 --port $PORT`) to Render.
- Set env: `ANTHROPIC_PROVIDER` + **`ANTHROPIC_API_KEY`** (the WORKING key — the grader's `create_client` uses `setdefault`, so a stale/wrong deploy-env key silently wins; use the sk-ant-...`_Ku0` key confirmed working this session, or the deploy's own valid key).
- `healthCheckPath: /health`. Note the free plan spins down when idle (first request after idle is slow — warm it before the pilot).
- Record the real deployed base URL (e.g. `https://writing-grader.onrender.com`).

**Auth:** the grader auto-creates a stable default API key on every startup (`wg_9eeb…`, survives Render's ephemeral SQLite resets). The platform + smoke test use it via the `X-API-Key` header.

### Step 2 — Smoke-test the grader (our key)  · **blocker**
```
python pipeline/grader_smoke.py <DEPLOYED_BASE_URL> --key wg_9eeb30acb76544c3bfd28e715ccc25f1
```
Expect: health 200, strong > weak, maxScore 5, calibrated=true, non-empty feedback. **Do not proceed on FAIL.**

### Step 3 — Wire the grader into the 102 items  · **live PUT, needs go**
```
python pipeline/g9_wire_grader.py       <DEPLOYED_BASE_URL> --live   # 75 in-lesson FRQs
python pipeline/g9_push_mastery_v3_1.py  <DEPLOYED_BASE_URL> --live   # 27 PP100 mastery instruments
```
(Run each once without `--live` first to re-confirm the plan.) Both attach the ExternalApiScore customOperator + rubricBlock + the 5 outcome declarations; PUT is a full replace, rebuilt-from-source so content is preserved (timeback RULE 3).

### Step 4 — Confirm the PLATFORM wire-shape + auth  · **the one true unknown, needs a real submission**
The timeback contract documents only a **URL** in the customOperator — **no auth-header mechanism**. Before trusting the pilot:
- Submit ONE real response to a wired G9 FRQ **through the platform** and confirm a score comes back.
- If it 401s: the platform isn't sending our `X-API-Key`. Options: make `/score` accept unauthenticated platform calls (network-restricted), or embed the key in the grader URL if the platform forwards query params. **Resolve this before the pilot opens to students** — it's the difference between "grades" and "silently fails to grade."

### Step 5 — Grading-accuracy spot check (should-do)
Score 3-4 known strong/mid/weak G9 responses; confirm the bands are sane and differentiated. (Full blind human ground-truth is Tier D, out of pilot scope.)

---

## Go / no-go

**Ready now:** content (100% verified), wiring code (dry-run clean, correct endpoint + item set).
**Gates the pilot:** Step 1 (deploy), Step 2 (grader smoke), Step 4 (platform auth confirmation).
**Recommendation:** do Steps 1-2 first; if the grader smoke passes, wire (Step 3) and immediately do the single live platform submission (Step 4) before announcing the pilot. Step 4 is the last real risk — everything upstream is now verified.
