# Bake-Off Real Quality Signal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the G9 bake-off's proxy quality signal with a neutral, anchor-grounded Claude judge (same prompt+model for both pipelines) and rebalance the verdict to `fidelity*25 + fatal_gate_pass*25 + neutral_judge*50`, keeping the harness offline-reproducible by default and resumable when live.

**Architecture:** Two files change. `bakeoff_judge.py` gets a new LIVE branch that calls Claude directly (lazily importing `anthropic`) with a fixed item-quality rubric, replacing the Incept-QC call; offline stays the deterministic heuristic. `bakeoff_g9.py` reweights the verdict to 25/25/50 and wraps live judge calls in a resumable disk cache. No new module; the grader-discrimination dimension from an earlier draft was never built, so there is nothing to remove.

**Tech Stack:** Python 3 stdlib for the offline/default/tested path; `anthropic` (already a grader dependency) imported LAZILY only inside the live judge branch. pytest for tests. Offline fixture on disk: `C:/tmp/incept_fulltest_11324.json`.

## Global Constraints

- Offline/default path + all automated tests: Python 3 stdlib only, network-free, deterministic.
- The `anthropic` import is LAZY (inside the live branch only) so offline + tests never import it.
- No em dashes (— or –) in authored code/comments/docstrings (use `\u2014`/`\u2013` escapes when referencing).
- Never log or persist any API key (Anthropic or Incept).
- SAME judge prompt + model for BOTH pipelines (fairness invariant); no per-pipeline branching in the judge.
- Verdict primary rank = `fidelity*25 + fatal_gate_pass*25 + judge_median_mean/100*50`; fixable + excluded gate failures reported SEPARATELY, never in the rank.
- Live mode must FAIL LOUD if no Anthropic provider is configured; it must NEVER silently fall back to the heuristic (that would masquerade a proxy as a real judge).

---

## File Structure

- `pipeline/bakeoff_judge.py` — MODIFY. New live branch (neutral Claude judge + rubric + lazy `anthropic` client helper). Offline heuristic unchanged. Remove the now-unused `_item_to_qc_content` / `_extract_score` (Incept-QC helpers) once the live branch no longer calls Incept.
- `pipeline/bakeoff_g9.py` — MODIFY. Verdict formula 40/40/20 -> 25/25/50; `primary_rank` string, HTML, CLI updated. Add a resumable disk cache wrapper around live judge calls.
- `pipeline/tests/test_bakeoff_adapter.py` — MODIFY. Update the verdict-formula assertion to 25/25/50; keep the offline-judge determinism test; add a test that live mode fails loud with no provider (monkeypatched, no network).

**Verified current state:** the harness is 3-signal (40/40/20). `bakeoff_grader.py` does NOT exist and no grader-discrimination code/tests exist — the spec's "delete them if present" is a confirmed no-op. `bakeoff_judge.judge_item(item, anchor, n=3, live=False, client=None)` currently: offline -> heuristic; live -> `InceptClient.qc`. The grader's client pattern (for reference, NOT imported cross-repo): `ANTHROPIC_PROVIDER` (bedrock|direct), `ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL`, default model `claude-sonnet-4-6`.

---

## Task 1: Neutral Claude judge (replace Incept-QC live path)

**Files:**
- Modify: `pipeline/bakeoff_judge.py`
- Test: `pipeline/tests/test_bakeoff_adapter.py`

**Interfaces:**
- Consumes: an `Item` (duck-typed: `.stem`, `.qti_type`, `.options[].text/.correct/.rationale`, `.answer_key`, `.family`, `.subskill_or_mode`).
- Produces (unchanged signature): `judge_item(item, anchor="STAAR English I (G9 argument)", n=3, live=False, client=None) -> {"median": float, "samples": list[float], "variance": float}`. New helpers: `_anthropic_client()`, `_judge_prompt(item, anchor) -> str`, `_parse_score(text) -> float`, and `RUBRIC_VERSION` (a string constant used by Task 2's cache key).

- [ ] **Step 1: Write/adjust the failing tests**

In `pipeline/tests/test_bakeoff_adapter.py`, replace `test_judge_offline_is_deterministic_and_medianed` (keep its offline-determinism intent) and ADD a live-fails-loud test:

```python
def test_judge_offline_is_deterministic_and_medianed():
    from bakeoff_judge import judge_item
    from item_contract import Item, Option
    it = Item(id="X", family="SR", grade="9-10", stem="Which is an arguable claim?",
              qti_type="choice", subskill_or_mode="evidence", acc_tags=["CCSS.W.9-10.1"],
              options=[Option("A","Schools should start later, because teens need sleep.",True,""),
                       Option("B","School starts at 8am.",False,"a fact")],
              answer_key=["A"])
    r1 = judge_item(it, n=3, live=False)
    r2 = judge_item(it, n=3, live=False)
    assert r1["median"] == r2["median"]
    assert len(r1["samples"]) == 3 and 0 <= r1["median"] <= 100 and r1["variance"] >= 0

def test_judge_has_rubric_version_and_prompt_is_source_neutral():
    import bakeoff_judge as bj
    from item_contract import Item, Option
    assert isinstance(bj.RUBRIC_VERSION, str) and bj.RUBRIC_VERSION
    it = Item(id="X", family="SR", grade="9-10", stem="Pick the arguable claim.", qti_type="choice",
              subskill_or_mode="evidence", acc_tags=["CCSS.W.9-10.1"],
              options=[Option("A","Schools should start later, because teens need sleep.",True,""),
                       Option("B","School starts at 8am.",False,"a fact")], answer_key=["A"])
    p = bj._judge_prompt(it, "STAAR English I (G9 argument)")
    # prompt must NOT leak which pipeline authored the item (fairness): no provenance words
    low = p.lower()
    assert "incept" not in low and "own_authored" not in low and "our pipeline" not in low
    assert "arguable claim" in low   # it embeds the actual item content

def test_judge_live_fails_loud_without_provider(monkeypatch):
    import bakeoff_judge as bj
    from item_contract import Item, Option
    # no provider configured -> live must raise, never silently heuristic-fallback
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("ANTHROPIC_PROVIDER", "direct")   # direct needs a key; none set -> must raise
    it = Item(id="X", family="SR", grade="9-10", stem="s", qti_type="choice",
              subskill_or_mode="evidence", acc_tags=["CCSS.W.9-10.1"],
              options=[Option("A","x",True,""),Option("B","y",False,"z")], answer_key=["A"])
    import pytest
    with pytest.raises(Exception):
        bj.judge_item(it, n=1, live=True)

def test_parse_score_extracts_number():
    from bakeoff_judge import _parse_score
    assert _parse_score('{"score": 82}') == 82.0
    assert _parse_score("Score: 74 / 100") == 74.0
    assert _parse_score("no number here") == 0.0
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd "c:/Users/noelp/HS Writing/Alpha HS Writing Course 2026-27" && python -m pytest pipeline/tests/test_bakeoff_adapter.py -k judge -v`
Expected: FAIL (`RUBRIC_VERSION`/`_judge_prompt`/`_parse_score` not defined; live-fails-loud not yet enforced). Use `py` if `python` missing.

- [ ] **Step 3: Rewrite the live branch + add helpers**

In `pipeline/bakeoff_judge.py`: keep the module docstring/offline `_heuristic_score` as-is. Add near the top (after imports):

```python
import re, json

RUBRIC_VERSION = "g9-item-quality-v1"

_RUBRIC = (
    "You are scoring the QUALITY of a single grade 9 argumentative-writing TEST ITEM, as a neutral "
    "assessment reviewer. Anchor: {anchor}. Score 0-100 on these axes, weighted equally: "
    "(1) distractor plausibility (for MC: are the wrong options tempting but defensibly wrong, each a real "
    "misconception, not filler); (2) discrimination (does the item separate a student who has the skill from "
    "one who does not); (3) gradeability (is the prompt specific enough and the expected response clear "
    "enough that a scorer could reliably tell a strong answer from a weak one); (4) fit to the anchor and "
    "grade 9. Judge ONLY the item shown. Reply with a single JSON object: {{\"score\": <0-100 integer>}}."
)

def _judge_prompt(item, anchor: str) -> str:
    lines = [f"STEM: {getattr(item, 'stem', '')}"]
    if getattr(item, "options", None):
        for o in item.options:
            mark = " [KEY]" if o.correct else ""
            rat = f"  (rationale: {o.rationale})" if o.rationale else ""
            lines.append(f"OPTION {o.id}{mark}: {o.text}{rat}")
    if getattr(item, "answer_key", None):
        lines.append(f"MODEL ANSWER: {item.answer_key[0] if item.answer_key else ''}")
    return _RUBRIC.format(anchor=anchor) + "\n\nITEM:\n" + "\n".join(lines)

def _parse_score(text: str) -> float:
    try:
        obj = json.loads(text)
        if isinstance(obj, dict) and "score" in obj:
            return max(0.0, min(100.0, float(obj["score"])))
    except Exception:
        pass
    m = re.search(r"(\d+(?:\.\d+)?)", text or "")
    return max(0.0, min(100.0, float(m.group(1)))) if m else 0.0

def _anthropic_client():
    """Self-contained Anthropic client (mirrors the grader engine's provider logic; NOT a cross-repo import).
    FAILS LOUD if no provider is usable (live judge must never silently fall back to the heuristic)."""
    import anthropic   # lazy: only imported on the live path
    provider = os.environ.get("ANTHROPIC_PROVIDER", "bedrock").strip().lower()
    if provider == "bedrock":
        region = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")).strip()
        return anthropic.AnthropicBedrock(aws_region=region), _model()
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        raise ValueError("live judge needs ANTHROPIC_API_KEY (provider=direct) or ANTHROPIC_PROVIDER=bedrock")
    return anthropic.Anthropic(api_key=key), _model()

def _model() -> str:
    explicit = os.environ.get("ANTHROPIC_MODEL", "").strip()
    if explicit:
        return explicit
    prov = os.environ.get("ANTHROPIC_PROVIDER", "bedrock").strip().lower()
    return "us.anthropic.claude-sonnet-4-6" if prov == "bedrock" else "claude-sonnet-4-6"
```

Replace the live branch of `judge_item` (delete the InceptClient block, `_item_to_qc_content`, `_extract_score`):

```python
def judge_item(item, anchor: str = "STAAR English I (G9 argument)", n: int = 3,
               live: bool = False, client=None) -> dict:
    if not live:
        base = _heuristic_score(item)
        samples = [base] * max(1, n)   # deterministic: no variance offline
    else:
        cli, model = (client if client else _anthropic_client())
        prompt = _judge_prompt(item, anchor)
        samples = []
        for _ in range(max(1, n)):
            msg = cli.messages.create(model=model, max_tokens=64,
                                      messages=[{"role": "user", "content": prompt}])
            text = "".join(getattr(b, "text", "") for b in msg.content)
            samples.append(_parse_score(text))
    med = statistics.median(samples)
    var = statistics.pvariance(samples) if len(samples) > 1 else 0.0
    return {"median": med, "samples": samples, "variance": var}
```

(NOTE: `client` in live mode is now a `(client, model)` tuple when a test injects one; the default `_anthropic_client()` returns that tuple. Keep this consistent — the test injects nothing and expects the no-provider path to raise.)

Add `import re, json` to the existing import line. Ensure no em dashes anywhere.

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest pipeline/tests/test_bakeoff_adapter.py -v`
Expected: PASS (all, including the 4 judge tests). The live-fails-loud test passes because `provider=direct` with no key raises `ValueError`.

- [ ] **Step 5: Confirm offline path never imports anthropic**

Run: `python -c "import sys; sys.path.insert(0,'pipeline'); import bakeoff_judge; print('anthropic' in sys.modules)"`
Expected: `False` (lazy import; offline import of the module must not pull in anthropic).

- [ ] **Step 6: Commit**

```bash
git add pipeline/bakeoff_judge.py pipeline/tests/test_bakeoff_adapter.py
git commit -m "feat(bakeoff): neutral own-Claude judge replaces Incept-QC (fair, lazy, fails-loud)"
```

---

## Task 2: Reweight verdict to 25/25/50 + resumable live cache

**Files:**
- Modify: `pipeline/bakeoff_g9.py`
- Test: `pipeline/tests/test_bakeoff_adapter.py`

**Interfaces:**
- Consumes: `judge_item` + `RUBRIC_VERSION` from Task 1; existing `_score_side`, `_fidelity`, `run`.
- Produces: `run(live=False) -> dict` (unchanged signature) with the new rank; a cache helper `_judge_cached(item, live) -> dict` used inside `_score_side`.

- [ ] **Step 1: Update the failing test**

In `pipeline/tests/test_bakeoff_adapter.py`, update `test_bakeoff_run_offline_produces_ranked_scorecard` to assert the new formula string and that the offline verdict still ranks ours >= incept:

```python
def test_bakeoff_run_offline_produces_ranked_scorecard():
    from bakeoff_g9 import run
    sc = run(live=False)
    for side in ("ours", "incept"):
        assert set(sc[side]) >= {"fidelity", "fatal_gate_pass_rate", "fixable_failures",
                                 "judge_median_mean", "n_items"}
    assert sc["verdict"]["winner"] in ("ours", "incept", "tie")
    assert "25" in sc["verdict"]["primary_rank"] and "50" in sc["verdict"]["primary_rank"]
    # ours (full 21-item blueprint, clean) should not lose to incept offline
    assert sc["verdict"]["ours_rank"] >= sc["verdict"]["incept_rank"]
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest pipeline/tests/test_bakeoff_adapter.py::test_bakeoff_run_offline_produces_ranked_scorecard -v`
Expected: FAIL (primary_rank still says "40"/"20").

- [ ] **Step 3: Reweight the rank + add the cache**

In `pipeline/bakeoff_g9.py`, change the `rank` function and `primary_rank` string inside `run`:

```python
    def rank(sc):
        return round(sc["fidelity"] * 25 + sc["fatal_gate_pass_rate"] * 25
                     + sc["judge_median_mean"] / 100 * 50, 2)
    ours_rank, inc_rank = rank(ours_sc), rank(inc_sc)
    winner = "ours" if ours_rank > inc_rank else "incept" if inc_rank > ours_rank else "tie"
    verdict = {"winner": winner, "ours_rank": ours_rank, "incept_rank": inc_rank,
               "primary_rank": "fidelity*25 + fatal_gate_pass*25 + judge_median_mean/100*50 "
                               "(fixable + excluded failures reported separately, not in rank)",
               "judge_note": "offline runs use a deterministic structural-heuristic proxy (variance 0); "
                             "live runs use the neutral own-Claude 3-sample median",
               "excluded_gates_note": "acc_tags + cr/scr_binding excluded from Incept fatal-gate "
                                       "(our-internal taxonomy/bank; not test-design defects)"}
```

Add a resumable cache helper (near the top of the module, after imports) and use it in `_score_side`:

```python
_CACHE_DIR = "C:/tmp/bakeoff_cache"

def _judge_cached(item, live):
    """Resumable judge: offline is free + deterministic (no cache needed); live results are cached to disk
    keyed by (item id + rubric version) so a killed/quota-limited run resumes without re-calling."""
    from bakeoff_judge import judge_item, RUBRIC_VERSION
    if not live:
        return judge_item(item, n=3, live=False)
    os.makedirs(_CACHE_DIR, exist_ok=True)
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in f"{item.id}_{RUBRIC_VERSION}")
    path = os.path.join(_CACHE_DIR, f"judge_{safe}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    result = judge_item(item, n=3, live=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(result, fh)
    return result
```

In `_score_side`, replace the direct `judge_item(it, n=3, live=live)` call with `_judge_cached(it, live)`. Leave everything else (gate classification, fidelity, fixable/excluded) unchanged.

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest pipeline/tests/test_bakeoff_adapter.py -v`
Expected: PASS (all).

- [ ] **Step 5: Run the offline bake-off + confirm the new rank**

Run: `python pipeline/bakeoff_g9.py`
Expected: prints the verdict with `primary_rank` = the 25/25/50 string; `ours_rank >= incept_rank`; writes `C:/tmp/bakeoff_g9_scorecard.json` + `.html`. Report the new ours vs incept numbers (they WILL differ from the old 98.58/61.36 because the weights changed; that is expected).

- [ ] **Step 6: Commit**

```bash
git add pipeline/bakeoff_g9.py pipeline/tests/test_bakeoff_adapter.py
git commit -m "feat(bakeoff): reweight verdict to 25/25/50 (quality=50%) + resumable live judge cache"
```

---

## Task 3: Verification sweep

**Files:** none (verification only)

- [ ] **Step 1: Bake-off tests pass**

Run: `python -m pytest pipeline/tests/test_bakeoff_adapter.py -v`
Expected: all pass.

- [ ] **Step 2: Full suite (no regressions)**

Run: `python -m pytest pipeline/tests/ -q`
Expected: all pass (~249+; the changes are additive/edit-in-place to bake-off files only).

- [ ] **Step 3: Offline determinism + no-anthropic sweep**

Run:
```bash
python pipeline/bakeoff_g9.py >/dev/null && python -c "import json;d=json.load(open('C:/tmp/bakeoff_g9_scorecard.json'));print(d['verdict']['winner'],d['verdict']['ours_rank'],d['verdict']['incept_rank'])"
python pipeline/bakeoff_g9.py >/dev/null && python -c "import json;d=json.load(open('C:/tmp/bakeoff_g9_scorecard.json'));print(d['verdict']['winner'],d['verdict']['ours_rank'],d['verdict']['incept_rank'])"
python -c "import sys; sys.path.insert(0,'pipeline'); import bakeoff_judge, bakeoff_g9; print('anthropic loaded:', 'anthropic' in sys.modules)"
```
Expected: identical verdict both runs (deterministic offline); `anthropic loaded: False`.

- [ ] **Step 4: House-rule sweep**

Run: `grep -n "—\|–" pipeline/bakeoff_judge.py pipeline/bakeoff_g9.py`
Expected: no matches (only `\u2014`/`\u2013` escapes inside the heuristic detector, which grep for the literal char will not match).

- [ ] **Step 5: Commit (if any doc note added)**

```bash
git add -A && git commit -m "test(bakeoff): verification sweep - 25/25/50 verdict, offline deterministic, anthropic lazy"
```

---

## Self-Review

**Spec coverage:**
- Neutral own-Claude judge replaces Incept-QC, same prompt+model both sides, gradeability sub-axis in the rubric → Task 1. ✓
- Live fails loud without a provider (never silent heuristic fallback) → Task 1 (test + `_anthropic_client` raise). ✓
- Verdict reweighted to fidelity*25 + fatal_gate*25 + neutral_judge*50 → Task 2. ✓
- Grader-discrimination dropped / not built → confirmed no-op (verified: no such file/code exists). ✓
- Resumable live cache keyed by (item id + rubric version) → Task 2 (`_judge_cached` + `RUBRIC_VERSION`). ✓
- Offline stays stdlib-only, network-free, deterministic; anthropic imported lazily → Task 1 Step 5 + Task 3 Step 3. ✓
- Honest scope (artifact quality, judge noise) → carried in `verdict.judge_note` + existing docstrings. ✓

**Deferred (per spec non-goals):** test-specific grading engine; student-outcome grading; G10-12; adopting a winner.

**Placeholder scan:** none. The `(client, model)` tuple convention in live mode is documented in Task 1 Step 3.

**Type consistency:** `judge_item(...) -> {median,samples,variance}` unchanged; `RUBRIC_VERSION` (str), `_judge_prompt(item,anchor)->str`, `_parse_score(text)->float`, `_anthropic_client()->(client,model)`, `_judge_cached(item,live)->dict` consistent across Tasks 1-2.
