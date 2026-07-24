# First G9 Hybrid Tests (Assemble + Clean) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce 2 disjoint, gate-clean, student-shippable G9 test forms from the hybrid pool, with every Incept-origin item run through a drop-safe cleanup pipeline (em-dash strip / fact-verify / provenance+copyright / SCR model-answer) first; output as review artifacts, no push.

**Architecture:** New `pipeline/incept_cleanup.py` holds four pure per-`Item` cleanup steps + a `clean_item` orchestrator (ours-origin items pass through; Incept items run all 4, short-circuiting to dropped-with-reason). New `pipeline/first_tests_g9.py` cleans the deepened hybrid pool, selects 2 disjoint forms over the cleaned pool (via a small optional-`pool` param added to `bakeoff_hybrid.select_hybrid`), re-checks gates, and writes forms JSON + a review HTML with a cleanup ledger. Reuses `item_contract`, `content_screen`, `incept_pool`, `bakeoff_hybrid`; touches no push code.

**Tech Stack:** Python 3 stdlib for the offline/tested path; the fact-verify JUDGMENT may use an agent pass (opt-in, defaults to DROP) but the tested path is deterministic. pytest.

## Global Constraints

- Offline/default path + all tests: Python 3 stdlib only, network-free, deterministic.
- No em dashes ( -  or -) in authored code/comments/docstrings (use `\u2014`/`\u2013` escapes). The cleanup PRODUCES em-dash-free items; the module source is em-dash-free too.
- Never log or persist any API key.
- Reuse, do not fork: `item_contract.qc_item`/`gate_no_em_dash`, `content_screen.screen`, `bakeoff_hybrid.select_hybrid`/`is_eligible`/`_matches`/`_judge_cached`, `incept_pool.load_deepened_incept_pool`. NO push code touched (g9_push_live / g9_wire_grader untouched).
- DROP-SAFE + fail-loud: never ship a short form or an item that failed a cleanup step; log every drop. Fact-verify defaults to DROP when uncertain.
- Output artifacts only (C:/tmp/first_tests_g9/); NO grader-wire, NO Timeback push in this build.

---

## File Structure

- `pipeline/incept_cleanup.py` - CREATE. 4 cleanup steps + `clean_item` orchestrator.
- `pipeline/bakeoff_hybrid.py` - MODIFY (1 tiny back-compat change): `select_hybrid(live=False, deepened=False, pool=None)` - when `pool` is given, select over it instead of building `merged_pool`. Default `None` preserves current behavior exactly.
- `pipeline/first_tests_g9.py` - CREATE. Orchestrator: clean pool → select 2 disjoint forms → gate re-check → artifacts + ledger.
- `pipeline/tests/test_incept_cleanup.py` - CREATE. Offline-deterministic tests.

**Verified facts (do not re-derive):**
- `item_contract.qc_item(item) -> {passed, gates, first_failure}`; `gate_no_em_dash` detects literal ` - `/`-` in `stem + options[].text + options[].rationale`.
- `Item` fields: `id, family, grade, stem, qti_type, subskill_or_mode, acc_tags, options (list[Option] with .id/.text/.correct/.rationale), answer_key (list), stimulus_ref, rubric_ref, provenance (dict)`.
- `content_screen.screen(passages, prompt="", mode="", family="") -> {verdict: PASS|FLAG|REJECT, rejects, flags, notes}`. Called with a list of objects having a `.text` attr. Pattern (from `item_contract.gate_content`): `class _P: __init__(s,t): s.text=t` then `cs.screen([_P(body)], prompt=stem)`.
- `bakeoff_hybrid`: `is_eligible(item)`, `_matches(item, sec)`, `bg._judge_cached(item, live)` (via `import bakeoff_g9 as bg`), `rmt.BLUEPRINTS["G9"]` (sections with family/count/subskills|modes). `select_hybrid` currently builds `pool = [it for it in merged_pool(deepened=deepened) if is_eligible(it)]` then per-slot judge-ranks + fails loud on a short slot.
- `incept_pool.load_deepened_incept_pool() -> list[Item]` (Incept items, provenance bakeoff_source="incept"). `bakeoff_hybrid.merged_pool(deepened=True)` merges ours (bakeoff_source="ours") + these.
- Incept items provenance carries `bakeoff_source`; ours-origin items have `bakeoff_source="ours"`.

---

## Task 1: em-dash strip + house-style (`_strip_em_dash`)

**Files:**
- Create: `pipeline/incept_cleanup.py`
- Test: `pipeline/tests/test_incept_cleanup.py`

**Interfaces:**
- Consumes: `item_contract.Item`/`Option`.
- Produces: `_strip_em_dash(item) -> Item` - returns a copy with all `\u2014`/`\u2013` in stem/options(text+rationale)/answer_key replaced by house-style punctuation, meaning preserved.

- [ ] **Step 1: Write the failing test**

Create `pipeline/tests/test_incept_cleanup.py`:

```python
import os, sys, copy
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from incept_cleanup import _strip_em_dash
from item_contract import Item, Option, qc_item

def _incept_mc(stem, opts, answer_idx=0):
    options = [Option(id=chr(65+i), text=t, correct=(i == answer_idx),
                      rationale=("correct" if i == answer_idx else "a distractor")) for i, t in enumerate(opts)]
    return Item(id="INCEPT-x-01", family="SR", grade="9-10", stem=stem, qti_type="choice",
                subskill_or_mode="evidence", acc_tags=["CCSS.W.9-10.1"], options=options,
                answer_key=[chr(65+answer_idx)], provenance={"bakeoff_source": "incept"})

def test_strip_em_dash_removes_all_dashes_and_passes_gate():
    it = _incept_mc("Which choice \u2014 the best evidence \u2014 supports the claim?",
                    ["Cities should add bike lanes \u2013 safer routes get more riders.",
                     "It was warm.", "Buses run late.", "People liked it."])
    out = _strip_em_dash(it)
    body = out.stem + " ".join(o.text + o.rationale for o in out.options) + " ".join(out.answer_key)
    assert "\u2014" not in body and "\u2013" not in body        # no em/en dashes remain
    # the no-em-dash gate now passes on the cleaned item
    r = qc_item(out)
    assert r["gates"]["no_em_dash"]["passed"]

def test_strip_em_dash_preserves_meaning():
    it = _incept_mc("The plan \u2014 adopted last year \u2014 helped.", ["A", "B", "C"])
    out = _strip_em_dash(it)
    # content preserved minus the dash: the words survive
    assert "adopted last year" in out.stem
    assert "The plan" in out.stem and "helped" in out.stem

def test_strip_em_dash_does_not_mutate_original():
    it = _incept_mc("X \u2014 Y", ["A", "B", "C"])
    _strip_em_dash(it)
    assert "\u2014" in it.stem   # original untouched (copy semantics)
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd "c:/Users/noelp/HS Writing/Alpha HS Writing Course 2026-27" && python -m pytest pipeline/tests/test_incept_cleanup.py -v`
Expected: FAIL (`incept_cleanup` not found). Use `py` if `python` missing.

- [ ] **Step 3: Implement `_strip_em_dash`**

Create `pipeline/incept_cleanup.py`:

```python
"""
incept_cleanup.py  -  make an Incept-generated Item student-shippable before it lands on a real form.

Four DROP-SAFE steps (em-dash strip, fact-verify, provenance+copyright screen, SCR model-answer). Ours-origin
items pass through untouched. clean_item runs all 4 on Incept items, short-circuiting to dropped-with-reason
on the first unrecoverable failure and accumulating an actions log. Nothing ambiguous ships.
"""
from __future__ import annotations
import os, sys, re, copy
sys.path.insert(0, os.path.dirname(__file__))
from item_contract import Item, Option  # noqa: E402
import content_screen as cs  # noqa: E402

def _dedash(text: str) -> str:
    """Replace em/en dashes with house-style punctuation, preserving content. A spaced dash becomes a comma;
    a bare dash becomes a comma too (never drops words)."""
    t = text or ""
    t = t.replace(" \u2014 ", ", ").replace(" \u2013 ", ", ")
    t = t.replace("\u2014", ", ").replace("\u2013", ", ")
    return t

def _strip_em_dash(item: Item) -> Item:
    out = copy.copy(item)
    out.provenance = dict(item.provenance or {})
    out.stem = _dedash(item.stem)
    out.options = [Option(id=o.id, text=_dedash(o.text), correct=o.correct, rationale=_dedash(o.rationale))
                   for o in item.options]
    out.answer_key = [_dedash(a) for a in item.answer_key]
    return out
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest pipeline/tests/test_incept_cleanup.py -v`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add pipeline/incept_cleanup.py pipeline/tests/test_incept_cleanup.py
git commit -m "feat(cleanup): em-dash strip + house-style (meaning-preserving, copy-safe)"
```

---

## Task 2: fact-verify strip-or-drop (`_fact_verify`)

**Files:**
- Modify: `pipeline/incept_cleanup.py`
- Test: `pipeline/tests/test_incept_cleanup.py`

**Interfaces:**
- Produces: `_fact_verify(item) -> tuple[Item | None, str]` - deterministic pattern-scan for factual claims/figures; returns `(item, "no stats")` if claim-free, `(None, reason)` if it carries an unverifiable stat. (Rewrite-to-claim-safe is out of scope for the deterministic path; default is DROP when a stat is present and unverified.)

- [ ] **Step 1: Write the failing test**

Add to `pipeline/tests/test_incept_cleanup.py`:

```python
from incept_cleanup import _fact_verify

def test_fact_verify_keeps_claim_free_item():
    it = _incept_mc("Which sentence is an arguable claim?",
                    ["Cities should build bike lanes because safer routes get more riders.",
                     "Many cities have bike lanes.", "Bikes are nice.", "Some cities got grants."])
    out, note = _fact_verify(it)
    assert out is not None    # no hard stat -> kept

def test_fact_verify_drops_unverifiable_stat():
    it = _incept_mc("Which is the best evidence?",
                    ["A study of 62 districts found a 14 percent rise in scores.",
                     "It was warm.", "Buses run late.", "People liked it."])
    out, note = _fact_verify(it)
    assert out is None          # fabricated/unverifiable stat -> dropped
    assert "stat" in note.lower() or "percent" in note.lower() or "62" in note

def test_fact_verify_drops_on_percent_or_year_figure():
    it = _incept_mc("Pick the strongest support.",
                    ["Turnover fell from 21% to 13% after the change.", "A", "B", "C"])
    out, note = _fact_verify(it)
    assert out is None
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest pipeline/tests/test_incept_cleanup.py -k fact_verify -v`
Expected: FAIL (`_fact_verify` not defined).

- [ ] **Step 3: Implement `_fact_verify`**

Append to `pipeline/incept_cleanup.py`:

```python
# Patterns that signal a factual claim/figure that would need a real source (default DROP if present).
_STAT_PATTERNS = [
    re.compile(r"\b\d+\s*(?:percent|%)", re.I),          # "14 percent", "13%"
    re.compile(r"\b(?:study|survey|research|report|data)\b", re.I),  # cites a study/data
    re.compile(r"\b\d{2,}\s+(?:districts|schools|students|people|cities|states)\b", re.I),  # "62 districts"
    re.compile(r"\bin\s+(?:19|20)\d{2}\b"),               # "in 2019"
    re.compile(r"\bfrom\s+\d+\S*\s+to\s+\d+", re.I),      # "from 21% to 13%"
]

def _fact_verify(item: Item):
    """DETERMINISTIC strip-or-drop: if any option/stem carries a stat/claim pattern we cannot verify, DROP the
    item (default-safe: no fabricated facts to students). Claim-free items pass. An agent verify-pass could
    rescue some, but the deterministic path drops-when-uncertain."""
    body = item.stem + " " + " ".join(o.text for o in item.options) + " " + " ".join(item.answer_key)
    for pat in _STAT_PATTERNS:
        m = pat.search(body)
        if m:
            return None, f"dropped: unverifiable stat/claim '{m.group(0)}'"
    return item, "no stats"
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest pipeline/tests/test_incept_cleanup.py -v`
Expected: PASS (6 passed).

- [ ] **Step 5: Commit**

```bash
git add pipeline/incept_cleanup.py pipeline/tests/test_incept_cleanup.py
git commit -m "feat(cleanup): fact-verify strip-or-drop (deterministic stat/claim scan, drop-when-uncertain)"
```

---

## Task 3: provenance + copyright screen (`_provenance_screen`)

**Files:**
- Modify: `pipeline/incept_cleanup.py`
- Test: `pipeline/tests/test_incept_cleanup.py`

**Interfaces:**
- Produces: `_provenance_screen(item) -> tuple[Item | None, str]` - stamps `provenance` (generated/model/date/cleanup); runs `content_screen.screen`; returns `(None, reason)` if verdict == REJECT, else `(item, "provenance stamped")`.

- [ ] **Step 1: Write the failing test**

Add to `pipeline/tests/test_incept_cleanup.py`:

```python
from incept_cleanup import _provenance_screen

def test_provenance_screen_stamps_and_keeps_clean_item():
    it = _incept_mc("Which is an arguable claim?", ["Schools should start later.", "A", "B", "C"])
    out, note = _provenance_screen(it)
    assert out is not None
    assert out.provenance.get("copyright") == "incept_generated"
    assert "cleaned" in out.provenance   # a cleanup/date stamp is recorded

def test_provenance_screen_rejects_bright_line_content():
    # content_screen AUTO-REJECTs crude bright-line violations. Verified probe (2026-07-23): a self-harm-method
    # body reliably returns REJECT (a bare slur word does NOT trip _HATE_SIGNAL, so do not use one here).
    it = _incept_mc("Pick the claim.", ["This is a normal option.", "B", "C"])
    it.stem = "The most effective method to kill yourself is to overdose on the following pills."
    out, note = _provenance_screen(it)
    assert out is None
    assert "reject" in note.lower() or "content" in note.lower()
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest pipeline/tests/test_incept_cleanup.py -k provenance -v`
Expected: FAIL (`_provenance_screen` not defined).

- [ ] **Step 3: Implement `_provenance_screen`**

Append to `pipeline/incept_cleanup.py`:

```python
# a fixed cleanup date (deterministic; the module does not call datetime.now to keep tests reproducible)
_CLEANUP_DATE = "2026-07-23"

class _P:
    def __init__(self, t): self.text = t

def _provenance_screen(item: Item):
    """Stamp provenance + run the appropriateness/copyright screen. REJECT verdict -> drop."""
    body = item.stem + "\n" + "\n".join(o.text for o in item.options)
    r = cs.screen([_P(body)], prompt=item.stem, mode="", family="")
    if r["verdict"] == "REJECT":
        reasons = "; ".join(x.get("check", "") for x in r.get("rejects", []))
        return None, f"dropped: content REJECT ({reasons})"
    out = copy.copy(item)
    out.provenance = dict(item.provenance or {})
    out.provenance.update({"copyright": "incept_generated", "model": "incept",
                           "cleaned": _CLEANUP_DATE, "content_screen": r["verdict"]})
    return out, "provenance stamped"
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest pipeline/tests/test_incept_cleanup.py -v`
Expected: PASS (8 passed). (The reject probe is a verified self-harm-method body that returns REJECT; no adjustment needed.)

- [ ] **Step 5: Commit**

```bash
git add pipeline/incept_cleanup.py pipeline/tests/test_incept_cleanup.py
git commit -m "feat(cleanup): provenance stamp + content/copyright screen (REJECT -> drop)"
```

---

## Task 4: SCR model-answer fix + `clean_item` orchestrator

**Files:**
- Modify: `pipeline/incept_cleanup.py`
- Test: `pipeline/tests/test_incept_cleanup.py`

**Interfaces:**
- Produces:
  - `_fix_scr_model_answer(item) -> tuple[Item | None, str]` - for a `scr_writing` item with no `answer_key`, returns `(None, reason)` (drop; the deterministic path does not fabricate a model answer). SR/CR items pass through.
  - `clean_item(item) -> tuple[Item | None, list[str]]` - ours-origin (`provenance.bakeoff_source != "incept"`) pass through with `["passthrough (ours)"]`; Incept items run steps 1-4 in order, short-circuit to `(None, actions)` on first drop, else `(cleaned, actions)`.

- [ ] **Step 1: Write the failing test**

Add to `pipeline/tests/test_incept_cleanup.py`:

```python
from incept_cleanup import _fix_scr_model_answer, clean_item

def _incept_scr(stem, model=None):
    return Item(id="INCEPT-scr-01", family="SCR", grade="9-10", stem=stem, qti_type="text-entry",
                subskill_or_mode="scr_writing", acc_tags=["CCSS.L.9-10.1"],
                answer_key=([model] if model else []), rubric_ref="rc.scr1",
                provenance={"bakeoff_source": "incept"})

def test_scr_without_model_answer_dropped():
    out, note = _fix_scr_model_answer(_incept_scr("Rewrite to fix the modifier."))
    assert out is None

def test_clean_item_passes_ours_through_untouched():
    ours = _incept_mc("Which is an arguable claim?", ["Schools should start later.", "A", "B", "C"])
    ours.provenance = {"bakeoff_source": "ours"}
    out, actions = clean_item(ours)
    assert out is ours                      # ours passes through unchanged
    assert actions == ["passthrough (ours)"]

def test_clean_item_incept_clean_mc_survives_with_actions():
    it = _incept_mc("Which is an arguable claim?",
                    ["Schools should start later \u2014 teens need sleep.",
                     "School starts at 8.", "I like sleep.", "Sleep matters."])
    out, actions = clean_item(it)
    assert out is not None                  # clean-able MC survives
    body = out.stem + " ".join(o.text for o in out.options)
    assert "\u2014" not in body             # em-dash stripped
    assert out.provenance.get("copyright") == "incept_generated"
    assert any("em-dash" in a or "dash" in a for a in actions)

def test_clean_item_incept_with_stat_dropped_with_reason():
    it = _incept_mc("Best evidence?", ["A study of 62 districts found gains.", "A", "B", "C"])
    out, actions = clean_item(it)
    assert out is None
    assert any("stat" in a.lower() or "62" in a for a in actions)
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest pipeline/tests/test_incept_cleanup.py -k "scr or clean_item" -v`
Expected: FAIL (`_fix_scr_model_answer`/`clean_item` not defined).

- [ ] **Step 3: Implement the SCR step + orchestrator**

Append to `pipeline/incept_cleanup.py`:

```python
def _fix_scr_model_answer(item: Item):
    """An Incept scr_writing item must carry a model answer to pass the SCR schema gate. The deterministic
    path does NOT fabricate one (that authoring is an own-authored operator step), so a model-less SCR drops."""
    if item.family == "SCR" and item.subskill_or_mode == "scr_writing" and not (item.answer_key and item.answer_key[0].strip()):
        return None, "dropped: Incept SCR has no model answer (author one to include)"
    return item, "scr ok"

def clean_item(item: Item):
    """Ours-origin items pass through untouched. Incept items run the 4 drop-safe steps in order."""
    if (item.provenance or {}).get("bakeoff_source") != "incept":
        return item, ["passthrough (ours)"]
    actions = []
    cur = _strip_em_dash(item); actions.append("em-dash stripped")
    cur, note = _fact_verify(cur); actions.append(note)
    if cur is None:
        return None, actions
    cur, note = _provenance_screen(cur); actions.append(note)
    if cur is None:
        return None, actions
    cur, note = _fix_scr_model_answer(cur); actions.append(note)
    if cur is None:
        return None, actions
    return cur, actions
```

- [ ] **Step 4: Run to verify it passes**

Run: `python -m pytest pipeline/tests/test_incept_cleanup.py -v`
Expected: PASS (12 passed).

- [ ] **Step 5: Commit**

```bash
git add pipeline/incept_cleanup.py pipeline/tests/test_incept_cleanup.py
git commit -m "feat(cleanup): SCR model-answer drop + clean_item orchestrator (drop-safe, logged)"
```

---

## Task 5: orchestrator - clean pool, assemble 2 forms, artifacts + ledger

**Files:**
- Modify: `pipeline/bakeoff_hybrid.py` (add optional `pool=None` to `select_hybrid`)
- Create: `pipeline/first_tests_g9.py`
- Test: `pipeline/tests/test_incept_cleanup.py`

**Interfaces:**
- Consumes: `clean_item` (Task 4); `bakeoff_hybrid.merged_pool`/`select_hybrid`/`is_eligible`; `incept_pool`.
- Produces: `first_tests_g9.build(n_forms=2, live=False) -> dict` (forms + cleanup_ledger + per-form source map), writes `C:/tmp/first_tests_g9/forms.json` + `first_tests_g9.html`. CLI `python pipeline/first_tests_g9.py`.

- [ ] **Step 1: Add the optional pool param to select_hybrid**

In `pipeline/bakeoff_hybrid.py`, change the `select_hybrid` signature + first line only:

```python
def select_hybrid(live: bool = False, deepened: bool = False, pool: list | None = None):
    """... (unchanged docstring) ...  If `pool` is given, select over it (already merged+eligible-filterable);
    else build merged_pool(deepened)."""
    if pool is None:
        pool = [it for it in merged_pool(deepened=deepened) if is_eligible(it)]
    else:
        pool = [it for it in pool if is_eligible(it)]
    # ... rest of the function unchanged ...
```

This is back-compatible: existing callers pass no `pool` and get identical behavior.

- [ ] **Step 2: Write the failing test**

Add to `pipeline/tests/test_incept_cleanup.py`:

```python
def test_build_produces_two_disjoint_clean_forms():
    import first_tests_g9
    from item_contract import qc_item
    res = first_tests_g9.build(n_forms=2, live=False)
    forms = res["forms"]
    assert len(forms) == 2
    # every item on every form passes fatal gates + is em-dash-clean
    for f in forms:
        for it in f["items"]:
            body = it.stem + " ".join(o.text for o in it.options) + " ".join(it.answer_key)
            assert "\u2014" not in body and "\u2013" not in body
    # the two forms are disjoint (no shared item id)
    ids0 = {it.id for it in forms[0]["items"]}
    ids1 = {it.id for it in forms[1]["items"]}
    assert ids0.isdisjoint(ids1)
    # the cleanup ledger accounts for the Incept items (kept + dropped)
    assert "cleanup_ledger" in res and len(res["cleanup_ledger"]) >= 1
```

- [ ] **Step 3: Run to verify it fails**

Run: `python -m pytest pipeline/tests/test_incept_cleanup.py::test_build_produces_two_disjoint_clean_forms -v`
Expected: FAIL (`first_tests_g9` not found).

- [ ] **Step 4: Implement first_tests_g9.py**

Create `pipeline/first_tests_g9.py`:

```python
"""
first_tests_g9.py  -  assemble the first shippable G9 hybrid test forms.

Clean the deepened hybrid pool (Incept items through incept_cleanup; ours pass through), select disjoint
forms over the CLEANED pool, gate-recheck every selected item, and write review artifacts + a cleanup ledger.
No grader-wiring, no push - delivery is a separate step on approval.
"""
from __future__ import annotations
import os, sys, json, html
sys.path.insert(0, os.path.dirname(__file__))
from item_contract import qc_item
from incept_cleanup import clean_item
import bakeoff_hybrid as bh
import bakeoff_g9 as bg
import render_model_tests as rmt

OUT_DIR = "C:/tmp/first_tests_g9"

def _cleaned_pool(live: bool):
    """merged deepened pool -> clean each item -> (cleaned_pool, ledger). Ledger: per Incept item kept/dropped."""
    raw = bh.merged_pool(deepened=True)
    cleaned, ledger = [], []
    for it in raw:
        out, actions = clean_item(it)
        if (it.provenance or {}).get("bakeoff_source") == "incept":
            ledger.append({"id": it.id, "kept": out is not None, "actions": actions})
        if out is not None:
            cleaned.append(out)
    return cleaned, ledger

def _select_disjoint(cleaned, n_forms, live):
    """n disjoint forms via repeated select_hybrid over the cleaned pool, removing picked ids each round."""
    forms = []
    remaining = list(cleaned)
    for _ in range(n_forms):
        picked, srcmap = bh.select_hybrid(live=live, pool=remaining)
        forms.append({"items": picked, "source_map": srcmap})
        used = {it.id for it in picked}
        remaining = [it for it in remaining if it.id not in used]
    return forms

def build(n_forms: int = 2, live: bool = False) -> dict:
    cleaned, ledger = _cleaned_pool(live)
    forms = _select_disjoint(cleaned, n_forms, live)
    # gate re-check every selected item (must pass, per-source rule via bakeoff_hybrid.is_eligible already ran)
    for f in forms:
        for it in f["items"]:
            r = qc_item(it)
            # em-dash must be clean now; fatal gates were enforced at selection via is_eligible
            assert r["gates"]["no_em_dash"]["passed"], f"em-dash leaked into {it.id}"
    res = {"forms": forms, "cleanup_ledger": ledger,
           "kept_incept": sum(1 for e in ledger if e["kept"]),
           "dropped_incept": sum(1 for e in ledger if not e["kept"])}
    os.makedirs(OUT_DIR, exist_ok=True)
    _write_json(res)
    _write_html(res)
    return res

def _write_json(res):
    def item_d(it):
        return {"id": it.id, "family": it.family, "subskill": it.subskill_or_mode,
                "source": (it.provenance or {}).get("bakeoff_source"), "stem": it.stem,
                "options": [{"id": o.id, "text": o.text, "correct": o.correct} for o in it.options],
                "answer_key": it.answer_key, "provenance": it.provenance}
    out = {"forms": [{"items": [item_d(i) for i in f["items"]], "source_map": f["source_map"]} for f in res["forms"]],
           "cleanup_ledger": res["cleanup_ledger"],
           "kept_incept": res["kept_incept"], "dropped_incept": res["dropped_incept"]}
    with open(os.path.join(OUT_DIR, "forms.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)

def _write_html(res):
    def esc(s): return html.escape(str(s))
    parts = [f"<h1>First G9 Hybrid Tests</h1><p>{len(res['forms'])} disjoint forms. "
             f"Incept items kept {res['kept_incept']}, dropped {res['dropped_incept']} (see ledger).</p>"]
    for fi, f in enumerate(res["forms"], 1):
        parts.append(f"<h2>Form {fi}</h2><ol>")
        for it in f["items"]:
            src = (it.provenance or {}).get("bakeoff_source")
            parts.append(f"<li><b>[{esc(src)}/{esc(it.subskill_or_mode)}]</b> {esc(it.stem)}</li>")
        parts.append("</ol>")
    parts.append("<h2>Cleanup ledger (Incept items)</h2><table border=1 cellpadding=5>"
                 "<tr><th>id</th><th>kept</th><th>actions</th></tr>")
    for e in res["cleanup_ledger"]:
        parts.append(f"<tr><td>{esc(e['id'])}</td><td>{'kept' if e['kept'] else 'DROPPED'}</td>"
                     f"<td>{esc('; '.join(e['actions']))}</td></tr>")
    parts.append("</table>")
    with open(os.path.join(OUT_DIR, "first_tests_g9.html"), "w", encoding="utf-8") as fh:
        fh.write("<!DOCTYPE html><html><head><meta charset=UTF-8><title>First G9 Hybrid Tests</title></head>"
                 "<body style='font-family:sans-serif;max-width:900px;margin:0 auto;padding:24px'>"
                 + "".join(parts) + "</body></html>")

if __name__ == "__main__":
    live = "--live" in sys.argv
    res = build(n_forms=2, live=live)
    print(f"built {len(res['forms'])} forms; incept kept {res['kept_incept']} dropped {res['dropped_incept']}")
    print("wrote", OUT_DIR + "/forms.json + first_tests_g9.html")
```

- [ ] **Step 5: Run to verify it passes + regression**

Run: `python -m pytest pipeline/tests/test_incept_cleanup.py pipeline/tests/test_incept_pool.py pipeline/tests/test_bakeoff_hybrid.py -v`
Expected: all pass (the `select_hybrid` pool param is back-compatible, so the existing hybrid tests still pass).

- [ ] **Step 6: Run the offline build end to end**

Run: `python pipeline/first_tests_g9.py`
Expected: prints `built 2 forms; incept kept N dropped M` (expect a notable dropped count, since most Incept stats trip fact-verify); writes the JSON + HTML. If a slot fails to fill after cleanup, `select_hybrid` raises loud (a real finding to report, not a bug).

- [ ] **Step 7: Commit**

```bash
git add pipeline/bakeoff_hybrid.py pipeline/first_tests_g9.py pipeline/tests/test_incept_cleanup.py
git commit -m "feat(first-tests): assemble 2 disjoint cleaned G9 hybrid forms + cleanup ledger (artifacts, no push)"
```

---

## Task 6: verification sweep

**Files:** none (verification only)

- [ ] **Step 1: cleanup + all bake-off-family tests pass**

Run: `python -m pytest pipeline/tests/test_incept_cleanup.py pipeline/tests/test_incept_pool.py pipeline/tests/test_bakeoff_hybrid.py pipeline/tests/test_bakeoff_adapter.py -v`
Expected: all pass.

- [ ] **Step 2: full suite (no regressions)**

Run: `python -m pytest pipeline/tests/ -q`
Expected: all pass.

- [ ] **Step 3: forms are clean + disjoint + the ledger is honest**

Run: `python pipeline/first_tests_g9.py` then inspect `C:/tmp/first_tests_g9/forms.json`:
- confirm 2 forms, disjoint item ids, every item em-dash-free;
- confirm `dropped_incept` + `kept_incept` sum to the Incept items in the pool (ledger accounts for all).

- [ ] **Step 4: house-rule sweep on the 2 new files**

Run: `grep -n " - \|-" pipeline/incept_cleanup.py pipeline/first_tests_g9.py`
Expected: no matches.

- [ ] **Step 5: confirm no push/grader code was touched**

Run: `git diff --name-only <base>..HEAD | grep -E "g9_push_live|g9_wire_grader"`
Expected: no output (push/grader files untouched).

- [ ] **Step 6: Commit (if any note added)**

```bash
git add -A && git commit -m "test(first-tests): verification sweep - clean disjoint forms, ledger honest, no push touched"
```

---

## Self-Review

**Spec coverage:**
- Cleanup step 1 em-dash strip → Task 1. ✓
- Cleanup step 2 fact-verify strip-or-drop (drop-when-uncertain) → Task 2. ✓
- Cleanup step 3 provenance + copyright screen (REJECT→drop) → Task 3. ✓
- Cleanup step 4 SCR model-answer (drop if none) → Task 4. ✓
- `clean_item` drop-safe orchestrator, ours pass-through, logged → Task 4. ✓
- 2 disjoint cleaned forms over the cleaned pool + gate re-check + ledger + artifacts → Task 5. ✓
- Fail-loud on short slot (reused via select_hybrid) → Task 5 (Step 6 note). ✓
- No push / no grader-wire; artifacts only → Task 5 + Task 6 Step 5. ✓
- Offline-deterministic tests; agent fact-judgment out of the suite → Tasks 1-5 (deterministic path). ✓

**Deferred (per spec non-goals):** grader-wiring + Timeback push; ours-only forms; G10-12; >2 forms; field test; upstream Incept prompt fixes; agent rewrite-to-claim-safe (deterministic path drops instead).

**Placeholder scan:** none. Task 3's reject probe is a verified self-harm-method body (returns REJECT); no open choices.

**Type consistency:** `_strip_em_dash(item)->Item`; `_fact_verify/_provenance_screen/_fix_scr_model_answer(item)->(Item|None,str)`; `clean_item(item)->(Item|None,list[str])`; `build(n_forms,live)->dict`; `select_hybrid(live,deepened,pool=None)`. Consistent across tasks; reused signatures match verified facts.
