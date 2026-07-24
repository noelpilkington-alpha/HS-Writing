# Native vs Render grader — prompt authoring + offline comparison

**Date:** 2026-07-24
**Answers the three questions from the grader-split work:**
1. How do we turn our sentence grading specs into native-grader prompts?
2. How do we test those against our Render grader?
3. How do we compare native vs Render at paragraph + essay grain?

**Companion specs:** `2026-07-24-grader-split-native-vs-render.md` (the routing decision),
`2026-07-24-grader-allowlist-and-wiring-fix.md` (allowlist + XML wiring).

---

## Key finding that shrank the work: sentence scoring is rubric-agnostic

Our Render sentence scorer (`grader_engine/panel.py`) scores `rc.staar` and `rc.4trait` **identically** at
sentence grain — the rubric label is cosmetic; only `frq_type` changes the scale. So the split spec's "4
sentence prompts" collapse to **2**:

| native prompt | scale | routes it covers |
|---|---|---|
| **sentence-writing** | Answer Quality 0-2 + Conventions 0-1 = 3 | (writing, rc.staar) + (writing, rc.4trait) = 165 responses |
| **sentence-revision** | Skill Application 0-1 + Conventions 0-1 = 2 | (revision, rc.staar) + (revision, rc.4trait) = 21 responses |

---

## Q1 — Sentence specs → native prompts (DONE)

**Native format** (extracted verbatim from a shipped G3 STC item): a grading prompt embedded in the item as
`<qti-rubric-block use="ext:grading-prompt" view="scorer"><qti-content-body><pre>…</pre></qti-content-body>`,
with `{{passage}}` / `{{question}}` / `{{response}}` placeholders and a strict single-JSON output block; the
score scale rides on `<qti-outcome-declaration identifier="SCORE" normal-maximum="N" normal-minimum="0">`. The
customOperator uses Timeback's own hosted `definition=https://alphatest.alpha.school/prod/ai-grading` (that
host is inherently allowlist-approved — no allowlist add needed).

**Translation:** our Render prompts already have the exact craft shape the native format wants (pre-scoring
gates → per-trait rubric bands → JSON), so the mapping is mechanical. Authored:
- `pipeline/native_grader/native_prompts.py` — the 2 sentence prompts (writing /3, revision /2), each folding
  the Render scorer's gates (blank/gibberish/off-topic/verbatim) + per-dimension rubrics + one-sentence rule
  + clarity-gate conventions into one single-call prompt.
- `pipeline/native_grader/native_prompts_long.py` — paragraph (/10 + content gate) + essay (rc.staar SBAC→/5,
  rc.4trait argument /24 & analysis /16) prompts, for the Q3 comparison.

**Wiring (DONE):** `g9_wire_grader.wire_payload` now routes SENTENCE grain to the native grader — sets the
native operator URL + embeds the authored prompt as `<qti-rubric-block use="ext:grading-prompt">` + writes the
SCORE `normal-maximum` — emitted as XML (a JSON push strips the operator; CRITICAL RULE 1). Paragraph+ keeps
the Render operator. `native=True/False` overrides the auto-decision. Regression tests in
`tests/test_grader_xml_wiring.py` (sentence→native w/ grading-prompt+normal-maximum; paragraph→Render;
render-path-still-available-via-flag). Full suite: 321 pass.

---

## Q2 & Q3 — Testing native against Render (offline harness)

**Hard constraint:** the live native grader is **server-invoked only** (direct POST → 405; a real native score
needs an authenticated enrolled-student submit — see `CODEX_AUTHENTICATED_SESSION.md`). So testing is two
layers:

- **Layer 1 (offline, no platform):** run the AUTHORED native prompt through the SAME model the Render grader
  uses (Opus 4.8, Anthropic-direct), parse its JSON, and compare to the live Render `/score` on the same
  inputs — and to the corpus's official human score where present. This is the fidelity proof we can get now.
- **Layer 2 (live, needs enrolled session):** once wired, an enrolled student submits; read the native score
  from OneRoster `assessmentResults.metadata.responseResult`; compare to Render on the same text. Deferred to
  the authenticated-session run.

**Harness:** `pipeline/native_grader/native_vs_render_harness.py`. Per case: median-of-N (both graders are
temperature 1) native% vs render% vs official%; reports mean |native−render|, signed bias, Spearman rank
correlation, and each grader's Δ vs official. Corpora: the CCSS_G910 groundtruth JSONs (staar /5, mcas
idea-dev /5, regents L1-6, sbac /10). Sentence has no real scored corpus → a hand-authored probe set
(`sentence_probes.py`) checks discrimination + trap-flooring, not absolute accuracy.

### Results (offline, native-via-Opus vs live Render, all runs complete 2026-07-24)

| grain / route | corpus | n | cases | mean \|nat−ren\| | signed bias (nat−ren) | rank corr nat↔ren | \|Δ\| vs official (nat / ren) | rank vs official (nat / ren) |
|---|---|---|---|---|---|---|---|---|
| **sentence-revision** | probe | 3 | 5 | **0.0%** | +0.0% | **1.00** | 15% / 15% | 0.93 / 0.93 |
| **sentence-writing** | probe | 3 | 8 | **0.0%** | +0.0% | **1.00** | 10.4% / 10.4% | 0.98 / 0.98 |
| paragraph (rc.staar) | mcas | 3 | 12 | 8.3% | **+8.3%** | 0.92 | 22.5% / **15.8%** | 0.62 / **0.79** |
| essay rc.staar | staar | 3 | 12 | 7.5% | **+7.5%** | 0.95 | 17.5% / **11.7%** | 0.81 / **0.88** |
| essay rc.4trait (argument) | regents | 3 | 9 | 7.9% | −0.5% | 0.78 | 18.5% / **13.4%** | 0.55 / **0.73** |

**Read:**
- **Sentence (both routes): native IS Render.** 0.0% mean delta, Spearman 1.00, and identical |Δ| vs official.
  Both flagged every trap (gibberish→0, off-topic→low, "because of"/two-sentence→mid). The authored sentence
  prompts reproduce the Render scorer exactly. **Sentence→native is safe to ship.**
- **Paragraph + essay: native scores systematically HIGHER than Render** (+7.5% to +8.3% signed bias) and
  tracks the official human score MEASURABLY WORSE (native |Δ| 17.5-22.5% vs Render 11.7-15.8%; rank corr
  native 0.55-0.81 vs Render 0.73-0.88). The divergence concentrates at the LOW-QUALITY band — e.g. paragraph
  rows 5/6/12 (official 40/20/40%): native 80/70/90% vs Render 60/40/70%. Native's single-call prompt does not
  apply the content gate as forcefully as Render's panel+judge, so it **inflates weak extended writing** — the
  exact failure the Render content gate was built to stop.

### How to reproduce
```
cd pipeline/native_grader
python -u native_vs_render_harness.py --grain sentence --frq_type writing --n 3
python -u native_vs_render_harness.py --grain sentence --frq_type revision --n 3
python -u native_vs_render_harness.py --grain paragraph --rubric rc.staar --corpus mcas --n 3
python -u native_vs_render_harness.py --grain essay --rubric rc.staar --corpus staar --n 3 --limit 12
python -u native_vs_render_harness.py --grain essay --rubric rc.4trait --mode argument --corpus regents --n 3
```
Needs the funded `ANTHROPIC_API_KEY` in `../../../.env` (the harness OVERRIDES a stale shell key — the
setdefault/credit-balance gotcha) and network to the Render grader. `-u` (unbuffered) so background output
streams; do NOT add a `> file` redirect on a backgrounded run (the buffered output is lost).

---

## Recommendation — KEEP THE SPLIT (evidence-backed)

**Sentence → native, paragraph+ → Render.** The data confirms the split spec's quality judgment with numbers:

- **Sentence → native: confirmed.** Native reproduces the Render sentence scorer exactly (0% delta, rank 1.00,
  equal official accuracy) across both routes and all traps. Ship the 2 authored sentence prompts to native;
  it removes the allowlist/AWS dependency for the 186 sentence responses with no measurable quality loss.
- **Paragraph + essay → stay on Render.** Native inflates weak extended writing (+7.5-8.3% bias, worse
  official rank corr, low-band divergence). At the grain where the rubric carries real weight, that is the
  wrong direction. Native is NOT trustworthy enough to take paragraph+ off Render — do not promote it.
  Render's panel+judge + content gate is doing measurable work (holding down clean-but-empty extended
  responses) that the single-call native prompt does not replicate.

So the split is not just an allowlist workaround — it's the correct quality architecture: native for the
compact-rubric sentence slice, Render's purpose-built engine for rubric-weighted extended writing.

**Two caveats, stated honestly:**
1. **Layer-1 only.** This proves the AUTHORED PROMPT reproduces (or diverges from) the Render scorer via the
   SAME model. It does NOT prove the live Timeback platform runs the prompt identically — the enrolled-session
   run (Layer 2) is the final proof for both graders (still pending creds).
2. **Small n + temp=1.** 5-12 cases/grain, median-of-3. The sentence result (0% delta) is unambiguous; the
   paragraph/essay inflation is a consistent DIRECTION across 33 extended-writing cases, not a precise
   magnitude. It is strong enough to keep the split, not to publish an exact bias figure.

**If we ever want native to take paragraph+** (e.g. to fully drop Render): the lever is porting the content
gate into the native paragraph/essay prompts (make the low-Ideas cap explicit and mechanical, as the Render
engine does post-hoc) and re-running this harness until native's low-band inflation closes. Not needed now.

---

## Files

- `pipeline/native_grader/native_prompts.py` — 2 sentence prompts + render/rubric-block helpers
- `pipeline/native_grader/native_prompts_long.py` — paragraph + essay prompts
- `pipeline/native_grader/native_vs_render_harness.py` — the offline comparison harness
- `pipeline/native_grader/sentence_probes.py` — sentence probe set (no real corpus exists)
- `pipeline/g9_wire_grader.py` — `wire_payload` native/Render split + `item_to_xml_payload` grading-prompt block
- `pipeline/tests/test_grader_xml_wiring.py` — native + Render wiring regression tests
- corpus: `Writing_Test_Grader/Grading Standards Documentation/CCSS_G910/*_groundtruth.json`
