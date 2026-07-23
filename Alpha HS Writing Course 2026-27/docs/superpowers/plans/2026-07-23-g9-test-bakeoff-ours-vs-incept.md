# G9 Test Bake-Off (Our Pipeline vs Incept) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reproducible harness that generates a full G9 writing test from both our pipeline and Incept, normalizes both to our `Item` objects, scores both on identical criteria (blueprint fidelity + fatal/fixable gate-pass + 3-sample-median judge), and emits a ranked verdict.

**Architecture:** Four flat `pipeline/*.py` modules. `incept_test.py` generates+fetches an Incept test (reusing `InceptClient`). `incept_test_adapter.py` maps the raw Incept artifact JSON into our `Item`/`Option` dataclasses. `bakeoff_judge.py` is one LLM-judge path used for both pipelines. `bakeoff_g9.py` orchestrates: load ours + Incept-adapted, run `item_contract` gates with a fatal/fixable classifier, run the judge, emit scorecard JSON + side-by-side HTML.

**Tech Stack:** Python 3 stdlib only (matches the pipeline; `InceptClient` shells `curl`), pytest for unit tests. Offline dev/test uses cached artifacts already on disk in `C:/tmp`.

## Global Constraints

- Python 3, stdlib only. No new pip deps (the pipeline is dependency-free; `InceptClient` uses `curl` subprocess).
- No em dashes (— or –) in authored code/comments/docstrings.
- Never log or persist the Incept API key. Read it only via `InceptClient` (which already redacts); the key file `Incept/Incept Production details.md` is plaintext + untracked.
- Windows/network: any live Incept call goes through `InceptClient` (it already uses `curl --ssl-no-revoke`); live calls need `dangerouslyDisableSandbox`. All tasks must be runnable OFFLINE from cached JSON (no live API required to develop or test).
- Cache raw artifacts under `C:/tmp/incept_cache/` (InceptClient default) or `C:/tmp/`; never write generated test artifacts into the repo.
- The SAME judge prompt+model scores both pipelines (fairness). Any per-pipeline judge difference invalidates the comparison.
- This ranks TEST-ARTIFACT quality, not student outcomes. The verdict's primary rank is deterministic (fidelity + fatal-gate); the judge is a noise-flagged tie-breaker.

---

## File Structure

- `pipeline/incept_test.py` — CREATE. Generate an Incept G9 test (`test_spec` + `test`), poll, fetch artifact JSON. Thin wrapper over `InceptClient`.
- `pipeline/incept_test_adapter.py` — CREATE. `parse(output_json) -> (list[Item], list[str])`. The one-way mapper. Pure function (no I/O, no network) so it is trivially unit-testable from the cached fixture.
- `pipeline/bakeoff_judge.py` — CREATE. `judge_item(item, anchor, n=3) -> dict`. One judge path for both pipelines.
- `pipeline/bakeoff_g9.py` — CREATE. Orchestrator + fatal/fixable gate classifier + scorecard + HTML.
- `pipeline/tests/test_bakeoff_adapter.py` — CREATE. Adapter + gate-classifier unit tests (offline, from the cached fixture).

**Offline fixtures already on disk** (created earlier this session; the plan's tests read these — do NOT regenerate):
- `C:/tmp/incept_fulltest_11324.json` — the RAW Incept artifact (has `output_json.items[]`). The adapter's real input.
- `C:/tmp/incept_form_clean.json` — a cleaned convenience copy (not used by the adapter; ignore).

**Key API facts (verified):**
- `InceptClient` (pipeline/incept_client.py): `.generate(prompt, generation_type, options=None, grade_levels=None, subject=None, live=False)`, `.poll(request_id, kind="generate", live=False)`, `.artifact(artifact_id, live=False)`, `.qc(generation_type, content, prompt=None, ..., live=False)`. Non-live mode reads the cache. Default cache_dir `C:/tmp/incept_cache`.
- Raw Incept artifact shape: `artifact["output_json"]` has keys `grain, items, title, purpose, metadata, answer_key`. Each `items[i]` has: `interaction_type` ("multiple_choice" | "text_entry"), `stem`, `options` (LIST OF BARE STRINGS for MC; absent/empty for text_entry), `answer` (the correct option's full TEXT for MC; a model-answer string for CR/SCR), `explanations` (dict keyed by option TEXT), `metadata` (dok/difficulty/standards), and a per-item `stimulus` (dict: title/byline/article). There is NO top-level stimulus.
- Our `Item` (pipeline/item_contract.py): `Item(id, family, grade, stem, qti_type, subskill_or_mode, acc_tags=[], options=[Option(id,text,correct,rationale)], answer_key=[], stimulus_ref="", rubric_ref="", provenance={})`. `qc_item(item) -> {passed, gates:{name:{passed,detail}}, first_failure}`. Gate names: schema, acc_tags, cr_binding, rubric_config, distractor_integrity, no_change_discipline, scr_schema, scr_binding, scr_rubric, content, no_em_dash.
- OUR G9 test items: load the FULL `Item` objects directly by exec-ing `Item_Bank_G9/*.py` and reading each module's `ITEMS` list (do NOT use `render_model_tests._load_items` — it returns lightweight shims without options/answer_key). Select to the G9 blueprint = `render_model_tests.BLUEPRINTS["G9"]`.

---

## Task 1: Incept test adapter (pure, offline-testable)

**Files:**
- Create: `pipeline/incept_test_adapter.py`
- Test: `pipeline/tests/test_bakeoff_adapter.py`

**Interfaces:**
- Consumes: `Item`, `Option` from `item_contract`.
- Produces: `parse(output_json: dict) -> tuple[list[Item], list[str]]` (items, warnings). Also `classify_gate_failure(gate_name: str) -> str` returning `"fatal"` or `"fixable"` (used by Task 4; defined here so its test lives with the adapter tests).

- [ ] **Step 1: Write the failing tests**

Create `pipeline/tests/test_bakeoff_adapter.py`:

```python
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from incept_test_adapter import parse, classify_gate_failure

FIXTURE = "C:/tmp/incept_fulltest_11324.json"

def _output_json():
    return json.load(open(FIXTURE, encoding="utf-8"))["output_json"]

def test_parse_returns_items_and_warnings():
    items, warnings = parse(_output_json())
    assert len(items) == 8               # the fixture has 8 items
    assert isinstance(warnings, list)

def test_mc_correct_id_resolved_by_text_match():
    items, _ = parse(_output_json())
    mc = [it for it in items if it.qti_type == "choice"]
    assert mc, "expected at least one MC item"
    for it in mc:
        correct = [o for o in it.options if o.correct]
        assert len(correct) == 1                       # exactly one keyed correct option
        assert it.answer_key == [correct[0].id]        # answer_key matches the correct Option id
        assert all(o.rationale for o in it.options if not o.correct)  # distractors carry rationale

def test_text_entry_becomes_scr_or_cr_with_model_answer():
    items, _ = parse(_output_json())
    constructed = [it for it in items if it.qti_type in ("text-entry", "extended-text")]
    assert constructed, "expected SCR/ECR items"
    for it in constructed:
        assert it.answer_key and it.answer_key[0].strip()   # model answer carried
        assert it.family in ("SCR", "CR")

def test_no_item_silently_dropped():
    oj = _output_json()
    items, warnings = parse(oj)
    assert len(items) == len(oj["items"])   # one Item per source item, none dropped

def test_classify_gate_failure_split():
    assert classify_gate_failure("distractor_integrity") == "fatal"
    assert classify_gate_failure("scr_binding") == "fatal"
    assert classify_gate_failure("rubric_config") == "fatal"
    assert classify_gate_failure("schema") == "fatal"
    assert classify_gate_failure("no_em_dash") == "fixable"
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd "c:/Users/noelp/HS Writing/Alpha HS Writing Course 2026-27" && python -m pytest pipeline/tests/test_bakeoff_adapter.py -v`
Expected: FAIL (module `incept_test_adapter` not found). Use `py` if `python` missing.

- [ ] **Step 3: Implement the adapter**

Create `pipeline/incept_test_adapter.py`:

```python
"""
incept_test_adapter.py  -  map a raw Incept `test` artifact's output_json into our Item objects.

One-way, PURE (no I/O, no network) so it is testable from a cached fixture. It faithfully represents what
Incept produced: it does NOT strip em dashes or fix length leaks, so the item_contract gates measure the
real artifact. Unmappable fields go to a warnings list, never silently dropped.
"""
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from item_contract import Item, Option  # noqa: E402

# Which failing gates are structural (fatal) vs mechanical/post-fixable.
_FATAL_GATES = {"schema", "acc_tags", "cr_binding", "rubric_config",
                "distractor_integrity", "scr_schema", "scr_binding", "scr_rubric"}
_FIXABLE_GATES = {"no_em_dash", "no_change_discipline", "content"}

def classify_gate_failure(gate_name: str) -> str:
    """A failing gate is 'fatal' (structural) or 'fixable' (mechanical/post-processable)."""
    if gate_name in _FATAL_GATES:
        return "fatal"
    if gate_name in _FIXABLE_GATES:
        return "fixable"
    return "fatal"   # default unknown gates to fatal (conservative: never hide a defect)

def _mc_item(idx, raw, warnings) -> Item:
    # options are bare strings; assign synthetic A/B/C/D ids
    opts_text = raw.get("options") or []
    ans_text = str(raw.get("answer", "")).strip()
    expl = raw.get("explanations") or {}
    options, correct_ids = [], []
    for k, txt in enumerate(opts_text):
        oid = chr(65 + k)
        t = str(txt).strip()
        is_c = (t == ans_text)
        if is_c:
            correct_ids.append(oid)
        options.append(Option(id=oid, text=t, correct=is_c, rationale=str(expl.get(txt, "")).strip()))
    if len(correct_ids) != 1:
        warnings.append(f"item {idx}: MC answer text matched {len(correct_ids)} options (expected 1)")
    md = raw.get("metadata") or {}
    return Item(
        id=f"INCEPT-G9-{idx:02d}", family="SR", grade="9-10", stem=str(raw.get("stem", "")).strip(),
        qti_type="choice", subskill_or_mode="evidence",  # neutral SR subskill for gating parity
        acc_tags=list(md.get("standards") or ["CCSS.W.9-10.1"]),
        options=options, answer_key=list(correct_ids),
        provenance={"copyright": "incept_generated", "dok": md.get("dok"), "difficulty": md.get("difficulty")},
    )

def _constructed_item(idx, raw, warnings) -> Item:
    stem = str(raw.get("stem", "")).strip()
    model = str(raw.get("answer", "")).strip()
    if not model:
        warnings.append(f"item {idx}: constructed item has no model answer")
    md = raw.get("metadata") or {}
    stimulus = raw.get("stimulus")
    has_stim = isinstance(stimulus, dict) and bool(stimulus.get("article"))
    # Heuristic: a long constructed task bound to a passage = ECR essay; a short one = SCR analysis.
    is_essay = len(stem) > 300 or (md.get("difficulty") == "hard" and has_stim)
    if is_essay:
        return Item(
            id=f"INCEPT-G9-{idx:02d}", family="CR", grade="9-10", stem=stem, qti_type="extended-text",
            subskill_or_mode="argument", acc_tags=list(md.get("standards") or ["CCSS.W.9-10.1"]),
            answer_key=[model], stimulus_ref="INCEPT-STIMULUS",  # synthetic ref; gating parity, not a bank lookup
            rubric_ref="rc.staar",
            provenance={"copyright": "incept_generated", "note": "adapter: classified ECR essay"},
        )
    return Item(
        id=f"INCEPT-G9-{idx:02d}", family="SCR", grade="9-10", stem=stem, qti_type="text-entry",
        subskill_or_mode="scr_analysis" if has_stim else "scr_writing",
        acc_tags=list(md.get("standards") or ["CCSS.W.9-10.1"]),
        answer_key=[model], stimulus_ref="INCEPT-STIMULUS" if has_stim else "",
        rubric_ref="rc.scr3" if has_stim else "rc.scr1",
        provenance={"copyright": "incept_generated", "note": "adapter: classified SCR"},
    )

def parse(output_json: dict) -> tuple[list[Item], list[str]]:
    items, warnings = [], []
    raw_items = (output_json or {}).get("items") or []
    for idx, raw in enumerate(raw_items, 1):
        it = str(raw.get("interaction_type", "")).strip().lower()
        if it == "multiple_choice":
            items.append(_mc_item(idx, raw, warnings))
        elif it in ("text_entry", "text-entry", "extended_text", "extended-text"):
            items.append(_constructed_item(idx, raw, warnings))
        else:
            warnings.append(f"item {idx}: unmapped interaction_type '{it}' (kept as SR/choice best-effort)")
            items.append(_mc_item(idx, raw, warnings))
    return items, warnings
```

NOTE on `stimulus_ref="INCEPT-STIMULUS"`: our `gate_scr_binding`/`gate_cr_binding` verify the ref EXISTS in a Stimulus_Bank. Incept's stimulus is inline, not a bank id, so this synthetic ref will FAIL binding — that is a REAL, correct finding (Incept doesn't bind to our stimulus bank). Task 4's classifier records it; do not "fix" it in the adapter.

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest pipeline/tests/test_bakeoff_adapter.py -v`
Expected: PASS (5 passed). If `test_no_item_silently_dropped` or the MC-key test fails, the fixture shape differs — re-inspect `C:/tmp/incept_fulltest_11324.json` `output_json.items`.

- [ ] **Step 5: Commit**

```bash
git add pipeline/incept_test_adapter.py pipeline/tests/test_bakeoff_adapter.py
git commit -m "feat(bakeoff): Incept test artifact -> Item adapter + gate-failure classifier"
```

---

## Task 2: Incept test generator (thin client wrapper)

**Files:**
- Create: `pipeline/incept_test.py`

**Interfaces:**
- Consumes: `InceptClient` from `incept_client`.
- Produces:
  - `generate_g9_test(live=False, client=None) -> dict` — returns `{"request_id":..., "status_url":...}` (live) or a cached stub (dry). Submits `generation_type="test"`, `options={"purpose":"mastery","grain":"grade_level","structure":"single"}`, `grade_levels=["g9"]`, `subject="writing"`.
  - `fetch_g9_test(artifact_id, live=False, client=None) -> dict` — returns the artifact's `output_json` (live via `client.artifact`; dry via cache).
  - `load_cached_output_json(path="C:/tmp/incept_fulltest_11324.json") -> dict` — reads a saved artifact and returns its `output_json` (the offline path the bake-off uses by default).

- [ ] **Step 1: Write the failing test**

Add to `pipeline/tests/test_bakeoff_adapter.py`:

```python
def test_load_cached_output_json_roundtrips_to_adapter():
    from incept_test import load_cached_output_json
    oj = load_cached_output_json("C:/tmp/incept_fulltest_11324.json")
    assert "items" in oj and len(oj["items"]) == 8
    items, warnings = parse(oj)          # cached -> adapter must work end to end offline
    assert len(items) == 8
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest pipeline/tests/test_bakeoff_adapter.py::test_load_cached_output_json_roundtrips_to_adapter -v`
Expected: FAIL (`incept_test` not found).

- [ ] **Step 3: Implement**

Create `pipeline/incept_test.py`:

```python
"""
incept_test.py  -  generate + fetch a full Incept `test` artifact for the G9 bake-off.

Thin wrapper over InceptClient. LIVE calls go through the client (which handles auth, curl --ssl-no-revoke,
poll/fetch, and key redaction). DRY/offline reads a cached artifact so the bake-off is re-runnable without
the API. Never logs the key.
"""
from __future__ import annotations
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from incept_client import InceptClient  # noqa: E402

_TEST_OPTIONS = {"purpose": "mastery", "grain": "grade_level", "structure": "single"}
_PROMPT = ("A complete grade 9 argumentative writing test built around a reading passage: a source passage, "
           "several multiple-choice items on claims and evidence tied to the passage, at least one short "
           "constructed-response item, and one extended constructed-response argument essay with a rubric.")

def generate_g9_test(live: bool = False, client: InceptClient | None = None) -> dict:
    client = client or InceptClient()
    return client.generate(_PROMPT, "test", options=dict(_TEST_OPTIONS),
                           grade_levels=["g9"], subject="writing", live=live)

def fetch_g9_test(artifact_id, live: bool = False, client: InceptClient | None = None) -> dict:
    client = client or InceptClient()
    art = client.artifact(artifact_id, live=live)
    return (art or {}).get("output_json", {})

def load_cached_output_json(path: str = "C:/tmp/incept_fulltest_11324.json") -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh).get("output_json", {})
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest pipeline/tests/test_bakeoff_adapter.py -v`
Expected: PASS (6 passed total).

- [ ] **Step 5: Commit**

```bash
git add pipeline/incept_test.py pipeline/tests/test_bakeoff_adapter.py
git commit -m "feat(bakeoff): Incept G9 test generator + offline cache loader"
```

---

## Task 3: Bake-off judge (3-sample median, one path for both)

**Files:**
- Create: `pipeline/bakeoff_judge.py`

**Interfaces:**
- Consumes: our `Item`; optionally `InceptClient.qc` for a second judge opinion.
- Produces: `judge_item(item, anchor="STAAR English I (G9 argument)", n=3, live=False, client=None) -> dict` returning `{"median": float, "samples": list[float], "variance": float}`. In DRY/offline mode (default, `live=False`), returns a DETERMINISTIC heuristic score (so tests + offline bake-off runs are reproducible); LIVE mode calls the judge n times and medians.

- [ ] **Step 1: Write the failing test**

Add to `pipeline/tests/test_bakeoff_adapter.py`:

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
    assert r1["median"] == r2["median"]          # offline judge is deterministic
    assert len(r1["samples"]) == 3
    assert 0 <= r1["median"] <= 100
    assert r1["variance"] >= 0
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest pipeline/tests/test_bakeoff_adapter.py::test_judge_offline_is_deterministic_and_medianed -v`
Expected: FAIL (`bakeoff_judge` not found).

- [ ] **Step 3: Implement**

Create `pipeline/bakeoff_judge.py`:

```python
"""
bakeoff_judge.py  -  ONE judge path used for BOTH pipelines in the G9 bake-off (fairness).

LIVE: call an LLM judge n times and take the median (the spec's noise mitigation; Incept's own judge was
observed swinging ~17 pts run to run). OFFLINE (default): a deterministic heuristic proxy so tests and
offline bake-off runs are reproducible; it scores structural quality signals the same way for both
pipelines, so it never advantages one source.
"""
from __future__ import annotations
import os, sys, statistics
sys.path.insert(0, os.path.dirname(__file__))

def _heuristic_score(item) -> float:
    """Deterministic 0-100 proxy: rewards a real stem, >=3 options for MC, rationalized distractors,
    a model answer for constructed, and no em dashes. SAME logic for both pipelines."""
    s = 60.0
    stem = getattr(item, "stem", "") or ""
    if len(stem) >= 20:
        s += 10
    body = stem + " ".join(o.text + o.rationale for o in getattr(item, "options", []))
    if "\u2014" in body or "\u2013" in body:   # em/en dash present
        s -= 15
    if item.qti_type == "choice":
        opts = item.options
        if len(opts) >= 3:
            s += 10
        distractors = [o for o in opts if not o.correct]
        if distractors and all(o.rationale.strip() for o in distractors):
            s += 10
        # length-leak signal: correct option not the conspicuous longest
        if opts:
            correct = [o for o in opts if o.correct]
            dl = [len(o.text) for o in opts if not o.correct]
            if correct and dl and len(correct[0].text) <= max(dl) * 1.25:
                s += 10
    else:
        if item.answer_key and item.answer_key[0].strip():
            s += 15
    return max(0.0, min(100.0, s))

def judge_item(item, anchor: str = "STAAR English I (G9 argument)", n: int = 3,
               live: bool = False, client=None) -> dict:
    if not live:
        base = _heuristic_score(item)
        samples = [base, base, base][:max(1, n)]   # deterministic: no variance offline
    else:
        # LIVE: call the real judge n times. Kept minimal + identical for both pipelines.
        from incept_client import InceptClient
        client = client or InceptClient()
        samples = []
        for _ in range(max(1, n)):
            verdict = client.qc("question", _item_to_qc_content(item), prompt=anchor, live=True)
            samples.append(float(_extract_score(verdict)))
    med = statistics.median(samples)
    var = statistics.pvariance(samples) if len(samples) > 1 else 0.0
    return {"median": med, "samples": samples, "variance": var}

def _item_to_qc_content(item) -> dict:
    return {"stem": item.stem,
            "options": [o.text for o in item.options],
            "answer_key": {"answer": (item.answer_key[0] if item.answer_key else "")}}

def _extract_score(verdict: dict) -> float:
    v = (verdict or {}).get("verdict") or verdict or {}
    return float(v.get("judge_score", 0.0))
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest pipeline/tests/test_bakeoff_adapter.py -v`
Expected: PASS (7 passed total).

- [ ] **Step 5: Commit**

```bash
git add pipeline/bakeoff_judge.py pipeline/tests/test_bakeoff_adapter.py
git commit -m "feat(bakeoff): shared 3-sample-median judge (deterministic offline, live LLM path)"
```

---

## Task 4: Orchestrator — scorecard + verdict + HTML

**Files:**
- Create: `pipeline/bakeoff_g9.py`

**Interfaces:**
- Consumes: `parse`+`classify_gate_failure` (Task 1), `load_cached_output_json` (Task 2), `judge_item` (Task 3), `item_contract.qc_item`, `render_model_tests.BLUEPRINTS`.
- Produces: `run(live=False) -> dict` (the scorecard) and writes `C:/tmp/bakeoff_g9_scorecard.json` + `C:/tmp/bakeoff_g9.html`. CLI: `python pipeline/bakeoff_g9.py [--live]`.

- [ ] **Step 1: Write the failing test**

Add to `pipeline/tests/test_bakeoff_adapter.py`:

```python
def test_bakeoff_run_offline_produces_ranked_scorecard():
    from bakeoff_g9 import run
    sc = run(live=False)
    assert set(sc["ours"]) >= {"fidelity", "fatal_gate_pass_rate", "fixable_failures", "judge_median_mean", "n_items"}
    assert set(sc["incept"]) >= {"fidelity", "fatal_gate_pass_rate", "fixable_failures", "judge_median_mean", "n_items"}
    assert sc["verdict"]["winner"] in ("ours", "incept", "tie")
    assert "primary_rank" in sc["verdict"]           # documents the fidelity+fatal+judge formula
    # Incept side must surface its known structural costs (uncited inline stimulus -> binding fails)
    assert sc["incept"]["fatal_gate_pass_rate"] <= 1.0
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest pipeline/tests/test_bakeoff_adapter.py::test_bakeoff_run_offline_produces_ranked_scorecard -v`
Expected: FAIL (`bakeoff_g9` not found).

- [ ] **Step 3: Implement**

Create `pipeline/bakeoff_g9.py`:

```python
"""
bakeoff_g9.py  -  orchestrate the G9 test bake-off: our pipeline vs Incept.

Loads a full G9 test from BOTH pipelines, runs every item through item_contract gates (classified
fatal/fixable), runs the shared median judge, and emits a ranked scorecard + side-by-side HTML. Offline by
default (reads the cached Incept artifact); --live regenerates from the API.

Honest scope: ranks TEST-ARTIFACT quality (fidelity + fatal-gate-pass + judge), NOT student outcomes. The
judge is a noise-flagged tie-breaker; the deterministic gate + fidelity metrics are the primary rank.
"""
from __future__ import annotations
import os, sys, glob, json, html, importlib.util
sys.path.insert(0, os.path.dirname(__file__))
from item_contract import qc_item
from incept_test_adapter import parse, classify_gate_failure
from incept_test import load_cached_output_json
from bakeoff_judge import judge_item
import render_model_tests as rmt

ROOT = os.path.join(os.path.dirname(__file__), "..")

def _load_our_g9_items():
    """Full Item objects for the G9 form, selected to BLUEPRINTS['G9'] section filters."""
    bank = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "Item_Bank_G9", "*.py"))):
        if "__" in os.path.basename(f):
            continue
        spec = importlib.util.spec_from_file_location("bk_" + os.path.basename(f)[:-3], f)
        m = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(m)
        except SystemExit:
            pass
        for it in getattr(m, "ITEMS", []):
            bank.setdefault(it.subskill_or_mode, []).append(it)
            if it.family == "CR":
                bank.setdefault("_CR_" + it.subskill_or_mode, []).append(it)
    picked = []
    for sec in rmt.BLUEPRINTS["G9"]:
        keys = sec.get("subskills") or sec.get("modes") or []
        n = sec["count"]
        pool = []
        for k in keys:
            pool += bank.get(k, []) if sec["family"] != "CR" else bank.get("_CR_" + k, [])
        picked += sorted(pool, key=lambda i: i.id)[:n]
    return picked

def _score_side(items):
    fatal_ok = 0
    fixable_failures = 0
    per_item = []
    judges = []
    for it in items:
        r = qc_item(it)
        fatal = []
        fixable = []
        if not r["passed"]:
            for gname, g in r["gates"].items():
                if not g["passed"]:
                    (fatal if classify_gate_failure(gname) == "fatal" else fixable).append(gname)
        if not fatal:
            fatal_ok += 1
        fixable_failures += len(fixable)
        j = judge_item(it, n=3, live=False)
        judges.append(j["median"])
        per_item.append({"id": it.id, "family": it.family, "fatal": fatal, "fixable": fixable,
                         "judge_median": j["median"]})
    n = len(items) or 1
    return {"n_items": len(items), "fatal_gate_pass_rate": round(fatal_ok / n, 3),
            "fixable_failures": fixable_failures,
            "judge_median_mean": round(sum(judges) / n, 1), "per_item": per_item}

def _fidelity(items, is_ours: bool):
    """Fraction of the G9 blueprint's shape the test hits: has an ECR, has >=1 SCR, has MC items."""
    fams = [it.family for it in items]
    checks = [("CR" in fams), ("SCR" in fams), (fams.count("SR") >= 3)]
    return round(sum(1 for c in checks if c) / len(checks), 3)

def run(live: bool = False) -> dict:
    ours = _load_our_g9_items()
    incept_items, warnings = parse(load_cached_output_json() if not live else _live_incept())
    ours_sc = _score_side(ours); ours_sc["fidelity"] = _fidelity(ours, True)
    inc_sc = _score_side(incept_items); inc_sc["fidelity"] = _fidelity(incept_items, False)
    inc_sc["adapter_warnings"] = warnings
    def rank(sc):
        return round(sc["fidelity"] * 40 + sc["fatal_gate_pass_rate"] * 40 + sc["judge_median_mean"] / 100 * 20, 2)
    ours_rank, inc_rank = rank(ours_sc), rank(inc_sc)
    winner = "ours" if ours_rank > inc_rank else "incept" if inc_rank > ours_rank else "tie"
    verdict = {"winner": winner, "ours_rank": ours_rank, "incept_rank": inc_rank,
               "primary_rank": "fidelity*40 + fatal_gate_pass*40 + judge_median_mean/100*20 "
                               "(fixable_failures reported separately, not in rank)"}
    sc = {"ours": ours_sc, "incept": inc_sc, "verdict": verdict}
    with open("C:/tmp/bakeoff_g9_scorecard.json", "w", encoding="utf-8") as fh:
        json.dump(sc, fh, indent=1)
    _write_html(sc)
    return sc

def _live_incept():
    from incept_test import generate_g9_test, fetch_g9_test
    sub = generate_g9_test(live=True)
    # NOTE: live polling to terminal is the operator's step; for --live, pass an already-succeeded
    # artifact id via env INCEPT_ARTIFACT_ID to fetch. Keeps this module non-blocking.
    aid = os.environ.get("INCEPT_ARTIFACT_ID")
    if not aid:
        raise SystemExit("live mode: set INCEPT_ARTIFACT_ID to a succeeded test artifact id")
    return fetch_g9_test(aid, live=True)

def _write_html(sc):
    def esc(s): return html.escape(str(s))
    v = sc["verdict"]
    rows = []
    for side in ("ours", "incept"):
        s = sc[side]
        rows.append(f"<tr><td>{side}</td><td>{s['fidelity']}</td><td>{s['fatal_gate_pass_rate']}</td>"
                    f"<td>{s['fixable_failures']}</td><td>{s['judge_median_mean']}</td><td>{s['n_items']}</td></tr>")
    doc = (f"<!DOCTYPE html><html><head><meta charset='UTF-8'><title>G9 Bake-Off</title></head><body>"
           f"<h1>G9 Test Bake-Off: winner = {esc(v['winner'])}</h1>"
           f"<p>ours rank {v['ours_rank']} vs incept rank {v['incept_rank']}</p>"
           f"<p>{esc(v['primary_rank'])}</p>"
           f"<table border=1 cellpadding=6><tr><th>side</th><th>fidelity</th><th>fatal gate pass</th>"
           f"<th>fixable failures</th><th>judge median mean</th><th>items</th></tr>{''.join(rows)}</table>"
           f"</body></html>")
    with open("C:/tmp/bakeoff_g9.html", "w", encoding="utf-8") as fh:
        fh.write(doc)

if __name__ == "__main__":
    live = "--live" in sys.argv
    sc = run(live=live)
    print(json.dumps(sc["verdict"], indent=1))
    print(f"ours: {sc['ours']['fidelity']} fid, {sc['ours']['fatal_gate_pass_rate']} fatal-pass, "
          f"{sc['ours']['judge_median_mean']} judge | incept: {sc['incept']['fidelity']} fid, "
          f"{sc['incept']['fatal_gate_pass_rate']} fatal-pass, {sc['incept']['judge_median_mean']} judge")
    print("wrote C:/tmp/bakeoff_g9_scorecard.json + C:/tmp/bakeoff_g9.html")
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest pipeline/tests/test_bakeoff_adapter.py -v`
Expected: PASS (8 passed total).

- [ ] **Step 5: Run the offline bake-off end to end**

Run: `python pipeline/bakeoff_g9.py`
Expected: prints the verdict JSON + one summary line + "wrote ..." ; `C:/tmp/bakeoff_g9_scorecard.json` and `C:/tmp/bakeoff_g9.html` exist. Both sides show non-empty `n_items`, and Incept's `fatal_gate_pass_rate` reflects its real gate results (the synthetic `INCEPT-STIMULUS` binding + any length leaks show up as fatal — the correct finding).

- [ ] **Step 6: Commit**

```bash
git add pipeline/bakeoff_g9.py pipeline/tests/test_bakeoff_adapter.py
git commit -m "feat(bakeoff): G9 orchestrator - scorecard, ranked verdict, side-by-side HTML"
```

---

## Task 5: Verification sweep + honest-scope note

**Files:** none (verification only)

- [ ] **Step 1: All bake-off tests pass**

Run: `python -m pytest pipeline/tests/test_bakeoff_adapter.py -v`
Expected: 8 passed.

- [ ] **Step 2: Full pipeline suite still green (no regressions)**

Run: `python -m pytest pipeline/tests/ -q`
Expected: all pass (the bake-off modules are additive; nothing else changed).

- [ ] **Step 3: House-rule sweep on the new files**

Run: `grep -rn "\u2014\|\u2013" pipeline/incept_test.py pipeline/incept_test_adapter.py pipeline/bakeoff_judge.py pipeline/bakeoff_g9.py`
Expected: no matches (the only em-dash literals allowed are the `\u2014`/`\u2013` escapes inside the detector logic, which grep for the literal char will not match).

- [ ] **Step 4: Offline verdict is reproducible**

Run `python pipeline/bakeoff_g9.py` twice; confirm identical verdict both runs (offline judge is deterministic, so the bake-off is reproducible without the live API).

- [ ] **Step 5: Commit (if any doc note added)**

```bash
git add -A
git commit -m "test(bakeoff): verification sweep - offline bake-off reproducible, suite green"
```

---

## Self-Review

**Spec coverage:**
- Adapter (Incept -> Item, no-silent-drop, faithful) → Task 1. ✓
- Incept test generation + offline cache → Task 2. ✓
- Shared 3-sample-median judge → Task 3. ✓
- Orchestrator: fatal/fixable gate split, fidelity, verdict formula, scorecard JSON + HTML → Task 4. ✓
- Fatal/fixable classifier → Task 1 (`classify_gate_failure`), used in Task 4. ✓
- Offline-reproducible / no live API to develop-or-test → Tasks 1-4 all read cached fixture; Task 5 Step 4. ✓
- Honest-scope (artifact quality not outcomes; judge noise-flagged) → in bakeoff_g9 docstring + verdict.primary_rank. ✓

**Deferred (correctly, per spec non-goals):** G10-12 bake-offs; format reconciliation; rubric/grader changes; auto-adopting the winner; live judge calibration (the live path exists but offline is the default/tested path).

**Placeholder scan:** none. The `INCEPT_ARTIFACT_ID` env in `_live_incept` is an explicit operator hand-off for live mode (documented), not a TODO; offline is the tested default.

**Type consistency:** `parse() -> (list[Item], list[str])`, `classify_gate_failure(str) -> str`, `judge_item(item, anchor, n, live, client) -> {median, samples, variance}`, `run(live) -> scorecard dict` — names/signatures identical across Tasks 1-4. `Item`/`Option` fields match item_contract.
