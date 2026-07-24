# Incept Pool-Deepening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate Incept items across all 6 G9 slot-types (cached, intent-stamped by subskill) and wire an opt-in `deepened=True` pool into the hybrid bake-off so the hybrid contests every slot; the default 8-item behavior stays unchanged.

**Architecture:** New `pipeline/incept_pool.py` holds 6 subskill prompt templates, a live generate/fetch+cache path, a shape-normalizer that flattens any Incept artifact (single-question / items[] / forms[].items[]) into raw item dicts, and `load_deepened_incept_pool()` that parses + STAMPS each item with its bank's intended subskill/family/rubric. `pipeline/bakeoff_hybrid.py` gets a back-compatible `deepened=False` flag threaded through `merged_pool` / `select_hybrid` / `run_3way`.

**Tech Stack:** Python 3 stdlib for the offline/default/tested path; live Incept generation via the existing `InceptClient` (curl). pytest. Offline tests run against small cached FIXTURE bank JSONs, never live.

## Global Constraints

- Offline/default path + all tests: Python 3 stdlib only, network-free, deterministic.
- Incept calls go through `InceptClient` (handles curl --ssl-no-revoke + key redaction); NEVER log a key.
- `anthropic` only on the live judge path (unchanged, via bakeoff_judge); not touched here.
- No em dashes ( -  or -) in authored code/comments/docstrings (use `\u2014`/`\u2013` escapes when referencing).
- The default `merged_pool()` (8-item single-test pool) + ALL existing bake-off verdicts stay UNCHANGED; deepening is opt-in via `deepened=True`.
- The judge stays SOURCE-BLIND: subskill/source tags live in the Item, never in the judge prompt.
- Conventions/sentence deepening is a GENERATOR SHOOT-OUT (bake-off input), NOT a course-scope change; nothing here ships Incept items into the course.

---

## File Structure

- `pipeline/incept_pool.py` - CREATE. Prompts, generate/fetch+cache, shape-normalizer, intent-stamping loader.
- `pipeline/bakeoff_hybrid.py` - MODIFY. Thread `deepened=False` through `merged_pool` / `select_hybrid` / `run_3way`.
- `pipeline/tests/test_incept_pool.py` - CREATE. Offline tests against fixture banks written to `C:/tmp/incept_pool/`.

**Verified facts (do not re-derive):**
- `incept_test_adapter.parse(output_json) -> (list[Item], list[str])` reads `output_json["items"]` (flat list) and per-item builds `Item` via `_mc_item` (family="SR", qti_type="choice", stamps subskill "evidence") or `_constructed_item` (family="CR"/"SCR" by heuristic). So `parse` handles ONLY the flat `items[]` shape.
- Incept artifact shapes DIVERGE by type: a single `question` -> `output_json` IS the item (stem/answer/options at top level); a `test` bank -> `output_json["forms"][].["items"]`; a `question` bank (structure=bank) -> shape UNCONFIRMED (likely flat `items[]` or `questions[]`) - the normalizer must handle all, and the loader logs which shape each cached bank actually had (verify on first live fetch).
- `InceptClient.generate(prompt, generation_type, options=None, grade_levels=None, subject=None, state=None, live=False)`, `.artifact(artifact_id, live=False)`. Non-live returns cached/would-send data.
- `bakeoff_hybrid.merged_pool()` (line 26), `select_hybrid(live)` (56), `run_3way(live)` (129) each independently call `parse(load_cached_output_json())` for the Incept side - ALL THREE need the deepened branch.
- Blueprint subskills (BLUEPRINTS["G9"]): SR needs evidence/organization/conventions/sentence; SCR needs scr_writing; CR (ECR) needs argument/explanatory.
- Item fields: `family` ("SR"|"SCR"|"CR"), `subskill_or_mode`, `qti_type`, `rubric_ref`, `acc_tags`, `provenance`.
- Per-subskill family/qti/rubric the loader must stamp: SR subskills -> family "SR", qti "choice", rubric "" ; scr_writing -> family "SCR", qti "text-entry", rubric "rc.scr1" ; argument -> family "CR", qti "extended-text", rubric "rc.staar". (Mirror `incept_test_adapter._mc_item`/`_constructed_item`.)

---

## Task 1: Prompts + shape-normalizer + intent-stamping loader

**Files:**
- Create: `pipeline/incept_pool.py`
- Test: `pipeline/tests/test_incept_pool.py`

**Interfaces:**
- Consumes: `incept_test_adapter` (Item/Option construction reference), `item_contract.Item`, `item_contract.Option`.
- Produces:
  - `SUBSKILL_PROMPTS: dict` - 6 entries keyed by subskill.
  - `SUBSKILL_STAMP: dict` - subskill -> `{"family","qti_type","rubric_ref"}`.
  - `_normalize_items(output_json) -> list[dict]` - flatten single-item / `items[]` / `forms[].items[]` / `questions[]` to a flat list of raw item dicts.
  - `load_deepened_incept_pool(cache_dir="C:/tmp/incept_pool") -> list[Item]` - read the 6 cached bank JSONs, normalize, build Items STAMPED with the bank's subskill/family/qti/rubric, tag `provenance["bakeoff_source"]="incept"`; raise a clear error naming any missing subskill bank.

- [ ] **Step 1: Write the failing tests**

Create `pipeline/tests/test_incept_pool.py`:

```python
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import incept_pool as ip

CACHE = "C:/tmp/incept_pool"
SUBSKILLS = ["evidence", "organization", "conventions", "sentence", "scr_writing", "argument"]

def _write_fixture_banks():
    """Small deterministic fixture banks, one per subskill, in the shapes Incept can emit."""
    os.makedirs(CACHE, exist_ok=True)
    def mc(stem, key):
        return {"stem": stem, "interaction_type": "multiple_choice",
                "options": [key, "a distractor about weather", "an off-topic fact", "a vague opinion"],
                "answer": key, "explanations": {key: "correct", "a distractor about weather": "off topic",
                "an off-topic fact": "off topic", "a vague opinion": "vague"},
                "metadata": {"dok": "2", "difficulty": "medium", "standards": ["CCSS.W.9-10.1"]}}
    # SR subskills -> flat items[] shape
    for sk in ["evidence", "organization", "conventions", "sentence"]:
        items = [mc(f"{sk} question {i}: which choice is correct?", f"the correct {sk} choice {i}") for i in range(3)]
        json.dump({"items": items}, open(f"{CACHE}/{sk}.json", "w", encoding="utf-8"))
    # scr_writing -> text_entry items[]
    json.dump({"items": [{"stem": "Rewrite the sentence to fix the modifier.", "interaction_type": "text_entry",
               "answer": "A clear rewrite that fixes the modifier.", "metadata": {"difficulty": "medium"}}]},
              open(f"{CACHE}/scr_writing.json", "w", encoding="utf-8"))
    # argument -> a forms[].items[] shape (a test-style artifact) with one long constructed prompt
    json.dump({"forms": [{"items": [{"stem": "Write an argumentative essay on whether schools should adopt a "
               "four-day week, citing the passage. " + ("Develop your claim fully. " * 20),
               "interaction_type": "text_entry", "answer": "A full argument essay model.",
               "metadata": {"difficulty": "hard"}, "stimulus": {"article": "some passage text"}}]}]},
              open(f"{CACHE}/argument.json", "w", encoding="utf-8"))

def test_normalize_handles_three_shapes():
    single = {"stem": "s", "interaction_type": "multiple_choice", "options": ["a"], "answer": "a"}
    flat = {"items": [single, single]}
    formed = {"forms": [{"items": [single]}, {"items": [single, single]}]}
    assert len(ip._normalize_items(single)) == 1     # single question IS the item
    assert len(ip._normalize_items(flat)) == 2       # items[]
    assert len(ip._normalize_items(formed)) == 3     # forms[].items[]

def test_load_deepened_pool_stamps_subskills():
    _write_fixture_banks()
    pool = ip.load_deepened_incept_pool(CACHE)
    got = {it.subskill_or_mode for it in pool}
    assert {"evidence", "organization", "conventions", "sentence", "scr_writing", "argument"} <= got
    # every item is tagged incept + has the right family per subskill
    for it in pool:
        assert it.provenance.get("bakeoff_source") == "incept"
    fam = {it.subskill_or_mode: it.family for it in pool}
    assert fam["evidence"] == "SR" and fam["conventions"] == "SR"
    assert fam["scr_writing"] == "SCR" and fam["argument"] == "CR"

def test_load_deepened_pool_missing_bank_raises():
    os.makedirs(CACHE, exist_ok=True)
    # remove one bank and confirm a clear error names it
    p = f"{CACHE}/organization.json"
    _write_fixture_banks()
    os.remove(p)
    try:
        ip.load_deepened_incept_pool(CACHE)
        assert False, "expected a missing-bank error"
    except Exception as e:
        assert "organization" in str(e)
    _write_fixture_banks()  # restore for other tests
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd "c:/Users/noelp/HS Writing/Alpha HS Writing Course 2026-27" && python -m pytest pipeline/tests/test_incept_pool.py -v`
Expected: FAIL (`incept_pool` not found). Use `py` if `python` missing.

- [ ] **Step 3: Implement incept_pool.py (prompts + normalizer + loader)**

Create `pipeline/incept_pool.py`:

```python
"""
incept_pool.py  -  deepen the Incept item pool across all 6 G9 slot-types for the hybrid bake-off.

Generate one targeted Incept bank per subskill (count ~10), cache each to C:/tmp/incept_pool/<subskill>.json,
then load + STAMP each item with its bank's intended subskill/family/rubric (we generate one bank per
subskill on purpose, so intent-stamping is deterministic). Feeds bakeoff_hybrid via deepened=True.

Scope note: conventions + sentence are app-owned skills (EGUMPP/AlphaWrite); generating Incept items for them
here is a GENERATOR SHOOT-OUT (bake-off input), NOT a course-scope change. Nothing here ships into the course.
"""
from __future__ import annotations
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from item_contract import Item, Option

SUBSKILLS = ["evidence", "organization", "conventions", "sentence", "scr_writing", "argument"]

# how each stamped subskill maps to our contract family/qti/rubric (mirrors incept_test_adapter)
SUBSKILL_STAMP = {
    "evidence":     {"family": "SR",  "qti_type": "choice",        "rubric_ref": ""},
    "organization": {"family": "SR",  "qti_type": "choice",        "rubric_ref": ""},
    "conventions":  {"family": "SR",  "qti_type": "choice",        "rubric_ref": ""},
    "sentence":     {"family": "SR",  "qti_type": "choice",        "rubric_ref": ""},
    "scr_writing":  {"family": "SCR", "qti_type": "text-entry",    "rubric_ref": "rc.scr1"},
    "argument":     {"family": "CR",  "qti_type": "extended-text", "rubric_ref": "rc.staar"},
}

# one targeted generation call per subskill (prompt engineered to elicit THAT subskill at G9)
SUBSKILL_PROMPTS = {
    "evidence": {"generation_type": "question",
                 "options": {"interaction_type": "multiple_choice", "structure": "bank", "count": 10},
                 "prompt": "Grade 9 argumentative writing: multiple-choice items where the student picks the "
                           "sentence that best supports a given claim with relevant evidence. Distractors: "
                           "off-claim, restates the topic, supports the opposing view."},
    "organization": {"generation_type": "question",
                     "options": {"interaction_type": "multiple_choice", "structure": "bank", "count": 10},
                     "prompt": "Grade 9 argumentative writing: multiple-choice items on organization and "
                               "cohesion, e.g. which transition or sentence order makes a paragraph flow."},
    "conventions": {"generation_type": "question",
                    "options": {"interaction_type": "multiple_choice", "structure": "bank", "count": 10},
                    "prompt": "Grade 9 editing: multiple-choice items on grammar, usage, punctuation, "
                              "capitalization, and spelling in the context of a short draft."},
    "sentence": {"generation_type": "question",
                 "options": {"interaction_type": "multiple_choice", "structure": "bank", "count": 10},
                 "prompt": "Grade 9 editing: multiple-choice items on sentence structure and boundaries "
                           "(run-ons, fragments, comma splices, combining)."},
    "scr_writing": {"generation_type": "question",
                    "options": {"interaction_type": "text_entry", "structure": "bank", "count": 10},
                    "prompt": "Grade 9 writing short-constructed-response: rewrite a flawed sentence to fix a "
                              "modifier or combine two sentences, preserving meaning."},
    "argument": {"generation_type": "test",
                 "options": {"purpose": "mastery", "grain": "grade_level", "structure": "single"},
                 "prompt": "A grade 9 source-based argumentative essay prompt with a reading passage on whether "
                           "schools should adopt a four-day week."},
}

def _normalize_items(output_json: dict) -> list[dict]:
    """Flatten any Incept artifact shape into a flat list of raw item dicts:
    single-question (the object IS the item), items[] (flat bank), or forms[].items[] (test bank),
    or questions[] (alt bank key)."""
    oj = output_json or {}
    if "items" in oj and isinstance(oj["items"], list):
        return list(oj["items"])
    if "questions" in oj and isinstance(oj["questions"], list):
        return list(oj["questions"])
    if "forms" in oj and isinstance(oj["forms"], list):
        out = []
        for f in oj["forms"]:
            out += list(f.get("items") or [])
        return out
    if "stem" in oj:            # a single-question artifact: the object itself is the item
        return [oj]
    return []

def _build_item(idx: int, subskill: str, raw: dict) -> Item:
    stamp = SUBSKILL_STAMP[subskill]
    md = raw.get("metadata") or {}
    stem = str(raw.get("stem", "")).strip()
    acc = list(md.get("standards") or ["CCSS.W.9-10.1"])
    prov = {"copyright": "incept_generated", "bakeoff_source": "incept", "dok": md.get("dok"),
            "difficulty": md.get("difficulty"), "intended_subskill": subskill}
    if stamp["family"] == "SR":
        opts_text = raw.get("options") or []
        ans = str(raw.get("answer", "")).strip()
        expl = raw.get("explanations") or {}
        options, correct = [], []
        for k, t in enumerate(opts_text):
            oid = chr(65 + k); tt = str(t).strip()
            if tt == ans: correct.append(oid)
            options.append(Option(id=oid, text=tt, correct=(tt == ans), rationale=str(expl.get(t, "")).strip()))
        return Item(id=f"INCEPT-{subskill}-{idx:02d}", family="SR", grade="9-10", stem=stem,
                    qti_type="choice", subskill_or_mode=subskill, acc_tags=acc,
                    options=options, answer_key=list(correct), provenance=prov)
    # SCR / CR: model answer in answer_key, no options
    model = str(raw.get("answer", "")).strip()
    return Item(id=f"INCEPT-{subskill}-{idx:02d}", family=stamp["family"], grade="9-10", stem=stem,
                qti_type=stamp["qti_type"], subskill_or_mode=subskill, acc_tags=acc,
                answer_key=[model] if model else [],
                stimulus_ref=("INCEPT-STIMULUS" if stamp["family"] == "CR" else ""),
                rubric_ref=stamp["rubric_ref"], provenance=prov)

def load_deepened_incept_pool(cache_dir: str = "C:/tmp/incept_pool") -> list[Item]:
    """Read the 6 cached subskill banks, normalize each, build stamped Items. Raise if any bank is missing."""
    missing = [sk for sk in SUBSKILLS if not os.path.exists(os.path.join(cache_dir, f"{sk}.json"))]
    if missing:
        raise FileNotFoundError(f"deepened Incept pool missing banks: {missing} (generate them first)")
    pool = []
    for sk in SUBSKILLS:
        with open(os.path.join(cache_dir, f"{sk}.json"), encoding="utf-8") as fh:
            oj = json.load(fh)
        raws = _normalize_items(oj)
        for i, raw in enumerate(raws, 1):
            pool.append(_build_item(i, sk, raw))
    return pool
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest pipeline/tests/test_incept_pool.py -v`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add pipeline/incept_pool.py pipeline/tests/test_incept_pool.py
git commit -m "feat(pool): Incept subskill prompts + shape-normalizer + intent-stamping loader"
```

---

## Task 2: Live generate/fetch + cache (operator path)

**Files:**
- Modify: `pipeline/incept_pool.py`

**Interfaces:**
- Consumes: `incept_client.InceptClient`; `SUBSKILL_PROMPTS`.
- Produces:
  - `generate_pool(live=False, client=None) -> dict[subskill -> submit_response]` - submit the 6 calls.
  - `fetch_pool(artifact_ids: dict, live=False, client=None, cache_dir="C:/tmp/incept_pool") -> dict[subskill -> path]` - fetch each artifact's output_json, cache to `<cache_dir>/<subskill>.json`.

- [ ] **Step 1: Write the failing test**

Add to `pipeline/tests/test_incept_pool.py`:

```python
def test_generate_pool_dry_returns_six_bodies():
    import incept_pool as ip
    from incept_client import InceptClient
    subs = ip.generate_pool(live=False, client=InceptClient())   # dry: no network
    assert set(subs) == set(ip.SUBSKILLS)   # one submission per subskill
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest pipeline/tests/test_incept_pool.py::test_generate_pool_dry_returns_six_bodies -v`
Expected: FAIL (`generate_pool` not defined).

- [ ] **Step 3: Implement generate_pool + fetch_pool**

Append to `pipeline/incept_pool.py`:

```python
def generate_pool(live: bool = False, client=None) -> dict:
    """Submit the 6 targeted bank generations. Dry mode returns the would-send bodies (no network).
    Live mode returns the 201 responses (request_id/status_url); polling to terminal is the operator step."""
    from incept_client import InceptClient
    client = client or InceptClient()
    out = {}
    for sk, spec in SUBSKILL_PROMPTS.items():
        out[sk] = client.generate(spec["prompt"], spec["generation_type"], options=dict(spec["options"]),
                                  grade_levels=["g9"], subject="writing", live=live)
    return out

def fetch_pool(artifact_ids: dict, live: bool = False, client=None, cache_dir: str = "C:/tmp/incept_pool") -> dict:
    """artifact_ids: {subskill -> succeeded artifact id}. Fetch each artifact's output_json and cache it to
    <cache_dir>/<subskill>.json. Operator passes the ids after polling (mirrors incept_test's hand-off)."""
    from incept_client import InceptClient
    client = client or InceptClient()
    os.makedirs(cache_dir, exist_ok=True)
    paths = {}
    for sk, aid in artifact_ids.items():
        art = client.artifact(aid, live=live)
        oj = (art or {}).get("output_json", {})
        path = os.path.join(cache_dir, f"{sk}.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(oj, fh, indent=1)
        paths[sk] = path
    return paths
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest pipeline/tests/test_incept_pool.py -v`
Expected: PASS (4 passed).

- [ ] **Step 5: Commit**

```bash
git add pipeline/incept_pool.py pipeline/tests/test_incept_pool.py
git commit -m "feat(pool): live generate/fetch + per-subskill cache (operator path)"
```

---

## Task 3: Wire deepened pool into the hybrid (opt-in)

**Files:**
- Modify: `pipeline/bakeoff_hybrid.py`
- Test: `pipeline/tests/test_incept_pool.py`

**Interfaces:**
- Consumes: `incept_pool.load_deepened_incept_pool`.
- Produces: `merged_pool(deepened=False)`, `select_hybrid(live=False, deepened=False)`, `run_3way(live=False, deepened=False)` - the deepened Incept pool replaces the single-test pool when `deepened=True`.

- [ ] **Step 1: Write the failing test**

Add to `pipeline/tests/test_incept_pool.py`:

```python
def test_merged_pool_deepened_uses_six_subskill_banks():
    _write_fixture_banks()
    import importlib, bakeoff_hybrid
    importlib.reload(bakeoff_hybrid)
    default_pool = bakeoff_hybrid.merged_pool()               # unchanged 8-item incept behavior
    deep_pool = bakeoff_hybrid.merged_pool(deepened=True)     # uses the 6 fixture banks
    inc_default = [it for it in default_pool if it.provenance.get("bakeoff_source") == "incept"]
    inc_deep = [it for it in deep_pool if it.provenance.get("bakeoff_source") == "incept"]
    # deepened incept pool spans multiple subskills (default is mostly 'evidence')
    assert len({it.subskill_or_mode for it in inc_deep}) >= 4
    assert len(inc_deep) > len(inc_default)
    # ours side identical in both
    assert sum(1 for it in default_pool if it.provenance.get("bakeoff_source") == "ours") == \
           sum(1 for it in deep_pool if it.provenance.get("bakeoff_source") == "ours")
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest pipeline/tests/test_incept_pool.py::test_merged_pool_deepened_uses_six_subskill_banks -v`
Expected: FAIL (`merged_pool` takes no `deepened` arg).

- [ ] **Step 3: Thread the deepened flag**

In `pipeline/bakeoff_hybrid.py`:

3a. Add the import at the top (after the existing imports):

```python
import incept_pool
```

3b. `merged_pool`:

```python
def merged_pool(deepened=False):
    """Ours (source=ours) + Incept (source=incept), each tagged in provenance (NOT in judge input).
    deepened=True pulls the 6-subskill deepened Incept pool; default pulls the single cached test (8 items)."""
    pool = []
    for it in bg._load_our_g9_items():
        it = copy.copy(it); it.provenance = dict(it.provenance or {}); it.provenance["bakeoff_source"] = "ours"
        pool.append(it)
    if deepened:
        inc = incept_pool.load_deepened_incept_pool()
        for it in inc:
            it = copy.copy(it); it.provenance = dict(it.provenance or {}); it.provenance["bakeoff_source"] = "incept"
            pool.append(it)
    else:
        inc, _warnings = parse(load_cached_output_json())
        for it in inc:
            it = copy.copy(it); it.provenance = dict(it.provenance or {}); it.provenance["bakeoff_source"] = "incept"
            pool.append(it)
    return pool
```

3c. `select_hybrid` - add the param + pass through:

```python
def select_hybrid(live: bool = False, deepened: bool = False):
    pool = [it for it in merged_pool(deepened=deepened) if is_eligible(it)]
    # ... rest unchanged ...
```

3d. `run_3way` - add the param; use the deepened pool for BOTH the incept side and the hybrid:

```python
def run_3way(live: bool = False, deepened: bool = False) -> dict:
    ours = bg._load_our_g9_items()
    if deepened:
        incept = incept_pool.load_deepened_incept_pool()
    else:
        incept, _w = parse(load_cached_output_json())
    hybrid_items, srcmap = select_hybrid(live=live, deepened=deepened)
    # ... rest unchanged (scoring, ranks, verdict, write) ...
```

3e. CLI: add a `--deepened` flag:

```python
if __name__ == "__main__":
    live = "--live" in sys.argv
    deep = "--deepened" in sys.argv
    sc = run_3way(live=live, deepened=deep)
    # ... existing prints ...
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest pipeline/tests/test_incept_pool.py -v`
Expected: PASS (5 passed).

- [ ] **Step 5: Confirm the default hybrid path is unchanged**

Run: `python -m pytest pipeline/tests/test_bakeoff_hybrid.py -v`
Expected: still all pass (the `deepened=False` default preserves the 8-item behavior).

- [ ] **Step 6: Commit**

```bash
git add pipeline/bakeoff_hybrid.py pipeline/tests/test_incept_pool.py
git commit -m "feat(hybrid): opt-in deepened=True pool (6 subskill banks) threaded through merged_pool/select/run_3way"
```

---

## Task 4: Verification sweep

**Files:** none (verification only)

- [ ] **Step 1: New + existing bake-off tests pass**

Run: `python -m pytest pipeline/tests/test_incept_pool.py pipeline/tests/test_bakeoff_hybrid.py pipeline/tests/test_bakeoff_adapter.py -v`
Expected: all pass.

- [ ] **Step 2: Full suite (no regressions)**

Run: `python -m pytest pipeline/tests/ -q`
Expected: all pass.

- [ ] **Step 3: Default (non-deepened) offline 3-way unchanged + deepened offline runs**

Run:
```bash
python pipeline/bakeoff_hybrid.py            # default: ours/incept(8)/hybrid, unchanged
python -c "import sys;sys.path.insert(0,'pipeline');import incept_pool as ip,json,os; os.makedirs('C:/tmp/incept_pool',exist_ok=True)"  # ensure dir
```
Expected: default run prints the unchanged verdict (winner=ours, hybrid ties). (The deepened offline run needs the 6 real banks; that happens after live generation - Step 4 documents it.)

- [ ] **Step 4: Document the live generation + deepened run (operator steps, not automated)**

Confirm the operator sequence works end to end (this DOES hit the API; run only if keys are configured):
```bash
# with HS Writing .env loaded (ANTHROPIC + Incept keys):
# 1) generate: python -c "import sys;sys.path.insert(0,'pipeline');import incept_pool as ip;print(ip.generate_pool(live=True))"
# 2) poll each request to succeeded, collect artifact ids
# 3) fetch+cache: python -c "...; ip.fetch_pool({'evidence':<id>,...}, live=True)"
# 4) deepened 3-way: python pipeline/bakeoff_hybrid.py --deepened            (offline judge)
#    or: (load .env) python pipeline/bakeoff_hybrid.py --deepened --live      (neutral judge)
```
Expected (record, do not assert): the deepened run reports a real contest in every slot + per-subskill Incept quality. This is the payoff finding; capture it in the ledger.

- [ ] **Step 5: House-rule sweep**

Run: `grep -n " - \|-" pipeline/incept_pool.py pipeline/bakeoff_hybrid.py`
Expected: no matches.

- [ ] **Step 6: Commit (if any note added)**

```bash
git add -A && git commit -m "test(pool): verification sweep - deepened opt-in, default unchanged, offline green"
```

---

## Self-Review

**Spec coverage:**
- 6 subskill prompts + intent-stamping loader + shape-normalizer → Task 1. ✓
- Live generate/fetch + per-subskill cache (resumable, operator step) → Task 2. ✓
- Opt-in `deepened=True` threaded through merged_pool/select_hybrid/run_3way; default unchanged → Task 3. ✓
- Missing-bank raises a clear error → Task 1 (`load_deepened_incept_pool`) + test. ✓
- All 3 shapes (single/items[]/forms[].items[]) normalized → Task 1 `_normalize_items` + test. ✓
- Per-subskill family/qti/rubric stamped correctly → Task 1 `SUBSKILL_STAMP` + `_build_item` + test. ✓
- Offline-deterministic tests against fixture banks (no live) → Tasks 1-3. ✓
- Live generation documented as operator step, per-subskill quality a reported finding → Task 4 Step 4. ✓

**Deferred (per spec non-goals):** shipping Incept items into the course; changing conventions/sentence ownership; multiple disjoint forms; G10-12; field test.

**Placeholder scan:** none. The Task 4 Step 4 operator sequence is intentionally a documented manual path (live API), not an automated assertion.

**Type consistency:** `_normalize_items(dict)->list[dict]`, `load_deepened_incept_pool(cache_dir)->list[Item]`, `generate_pool(live,client)->dict`, `fetch_pool(artifact_ids,live,client,cache_dir)->dict`, `merged_pool(deepened)`, `select_hybrid(live,deepened)`, `run_3way(live,deepened)` consistent across tasks. Item family/qti/rubric per `SUBSKILL_STAMP` matches item_contract + blueprint slot rules.
