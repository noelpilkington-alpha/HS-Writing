# G9 SCR Diversification + Writing-Only Test Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the G9 writing-only test assess only G9-taught skills, backed by a diversified writing-domain SCR bank, a new `SCR` item family, a counterclaim-recognition teach beat, and a points-weighted G9 blueprint.

**Architecture:** Add a third item family (`SCR`) to `pipeline/item_contract.py` with subtype-conditional gates and short-CR rubric configs. Migrate the 10 existing modifier-repair items out of the SR `scr` subskill into a new diversified `Item_Bank_G9/scr_writing.py` (SCR family, subtype `scr_writing`, ~15-20 items). Add a counterclaim-recognition beat to the G9 lesson bank. Rebalance `render_model_tests.py` `BLUEPRINTS["G9"]` (the file that actually assembles the G9 form) to a points-weighted writing-only shape.

**Tech Stack:** Python 3 (stdlib only — the item/lesson banks and contract are dependency-free), pytest for the contract test suite (`pipeline/tests/`).

## Global Constraints

- **No em dashes** (— or –) in any authored item/lesson prose — enforced by `gate_no_em_dash`; house rule (Noel).
- **Own-authored only**: every item carries `provenance={"copyright": "own_authored", ...}`; no third-party expression.
- **Dependency-free**: item/lesson banks import only stdlib + `item_contract`/`lesson_contract`; no new pip deps.
- **Every item file self-tests**: `python <file>.py` runs the QC harness and prints `N/N PASS`, exit 0 iff all pass.
- **ACC + CCSS tags required**: every item needs ≥1 `ACC.W*` tag; `acc_tags` includes the CCSS code.
- **G9 grade string is `"9-10"`**; item IDs use the `ACC-W910-...` prefix.
- **Scope**: G9 only. G10 `scr_analysis`/`scr_research` item authoring is a follow-up plan (the SCR family + `rc.scr2`/`rc.scr3` configs are built here as shared infra but only `scr_writing`/`rc.scr1` is exercised on the G9 form).
- **Coverage, not efficacy**: success = the G9 test only assesses G9-taught skills + all self-tests/crosschecks pass. It does NOT claim proven 90-100% mastery (needs a field test).

---

## File Structure

- `pipeline/item_contract.py` — MODIFY. Add `SCR` family, `SCR_SUBTYPES`, short-CR rubric configs, SCR gates, dispatch. Remove `scr` from `SR_SUBSKILLS`.
- `pipeline/tests/test_scr_family.py` — CREATE. Pytest coverage for the SCR family gates.
- `Item_Bank_G9/scr_writing.py` — CREATE. ~15-20 `scr_writing` (0-1) items: migrated modifier-repair + 4 new task types.
- `Item_Bank_G9/sr_scr_modifier.py` — DELETE after migration (its items move to `scr_writing.py`).
- `pipeline/render_model_tests.py` — MODIFY. `BLUEPRINTS["G9"]` SCR section → SCR family; rebalance to writing-only points shape.
- `pipeline/assemble_test.py` — MODIFY. Its G10 blueprint SCR section switches to the SCR family (consistency only; not a G10 rebalance).
- `pipeline/testbank_kc_crosscheck.py` — MODIFY. Add `rc.scr1/2/3` to `KNOWN_RUBRICS`; teach SCR family.
- `pipeline/coverage_matrix.py` — INSPECT/MODIFY if it filters on the `scr` subskill.
- `Lesson_Bank_G9/lesson_g9_l20_counterclaim_recognition_v3_1.py` — CREATE. Counterclaim-recognition beat.

**Migration blast radius (verified):** files referencing `sr_scr_modifier` or the `["scr"]` subskill: `pipeline/item_contract.py` (SR_SUBSKILLS + `__main__`), `pipeline/assemble_test.py:39`, `pipeline/render_model_tests.py:30`. (The `sim_student_eval/out/*.json` matches are frozen run artifacts — do NOT edit.)

---

## Task 1: Add the `SCR` family + short-CR rubric configs to the contract

**Files:**
- Modify: `pipeline/item_contract.py`
- Test: `pipeline/tests/test_scr_family.py`

**Interfaces:**
- Consumes: existing `Item`, `Option`, `qc_item`, `qc_report`, `GATES` from `item_contract.py`.
- Produces:
  - `Family = Literal["SR", "CR", "SCR"]`
  - `SCR_SUBTYPES = {"scr_writing", "scr_analysis", "scr_research"}`
  - `SCR_RUBRICS = {"rc.scr1", "rc.scr2", "rc.scr3"}` added into `RUBRIC_CONFIGS`
  - `SCR_BINDING = {"scr_writing": False, "scr_analysis": True, "scr_research": True}` (True = must bind a stimulus)
  - `SCR_RUBRIC_FOR = {"scr_writing": "rc.scr1", "scr_research": "rc.scr2", "scr_analysis": "rc.scr3"}`
  - gates `gate_scr_schema`, `gate_scr_binding`, `gate_scr_rubric` (each `(Item) -> tuple[bool, str]`)

- [ ] **Step 1: Write the failing test**

Create `pipeline/tests/test_scr_family.py`:

```python
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from item_contract import Item, qc_item

def _scr_writing(**kw):
    base = dict(id="ACC-W910-SCR-WRIT-0001", family="SCR", grade="9-10",
                subskill_or_mode="scr_writing", qti_type="text-entry",
                stem="Rewrite the sentence to fix the dangling modifier.",
                acc_tags=["ACC.W.CONV.1", "CCSS.L.9-10.1"],
                answer_key=["Running to catch the bus, I felt my backpack fall open."],
                rubric_ref="rc.scr1", provenance={"copyright": "own_authored"})
    base.update(kw); return Item(**base)

def test_valid_scr_writing_passes():
    it = _scr_writing()
    r = qc_item(it)
    assert r["passed"], r["gates"]

def test_scr_writing_must_not_bind_stimulus():
    it = _scr_writing(stimulus_ref="ACC-W910-ARG-OPP-0007")
    r = qc_item(it)
    assert not r["passed"]
    assert r["first_failure"] == "scr_binding"

def test_scr_analysis_must_bind_stimulus():
    it = _scr_writing(id="ACC-W910-SCR-ANAL-0001", subskill_or_mode="scr_analysis",
                      rubric_ref="rc.scr3", stimulus_ref="")
    r = qc_item(it)
    assert not r["passed"]
    assert r["first_failure"] == "scr_binding"

def test_scr_wrong_rubric_fails():
    it = _scr_writing(rubric_ref="rc.staar")
    r = qc_item(it)
    assert not r["passed"]
    assert r["first_failure"] == "scr_rubric"

def test_scr_requires_model_answer():
    it = _scr_writing(answer_key=[])
    r = qc_item(it)
    assert not r["passed"]
    assert r["first_failure"] == "scr_schema"

def test_scr_em_dash_rejected():
    it = _scr_writing(stem="Rewrite the sentence — fix the modifier.")
    r = qc_item(it)
    assert not r["passed"]
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `cd "Alpha HS Writing Course 2026-27" && python -m pytest pipeline/tests/test_scr_family.py -v`
Expected: FAIL — `Item.__init__` rejects `family="SCR"` (or gates missing), errors/assertion failures.

- [ ] **Step 3: Implement the contract changes**

In `pipeline/item_contract.py`:

3a. Widen the family type and add SCR vocab near the top constants (after `SR_SUBSKILLS`):

```python
Family = Literal["SR", "CR", "SCR"]
QTI_SR = {"choice", "inline-choice", "hottext", "text-entry"}
QTI_CR = {"extended-text"}
QTI_SCR = {"text-entry"}
RUBRIC_CONFIGS = {"rc.staar", "rc.mcas", "rc.ohio", "rc.4trait", "rc.ap",
                  "rc.scr1", "rc.scr2", "rc.scr3"}
CR_MODES = {"argument", "explanatory", "analysis"}
SR_SUBSKILLS = {"conventions", "sentence", "organization", "evidence", "language"}  # 'scr' REMOVED -> SCR family
SCR_SUBTYPES = {"scr_writing", "scr_analysis", "scr_research"}
SCR_BINDING = {"scr_writing": False, "scr_analysis": True, "scr_research": True}
SCR_RUBRIC_FOR = {"scr_writing": "rc.scr1", "scr_research": "rc.scr2", "scr_analysis": "rc.scr3"}
```

3b. Add three gates (place after `gate_no_change_discipline`, before `gate_content`):

```python
def gate_scr_schema(it: Item) -> tuple[bool, str]:
    if it.family != "SCR":
        return True, "n/a (not SCR)"
    if it.subskill_or_mode not in SCR_SUBTYPES:
        return False, f"SCR subtype '{it.subskill_or_mode}' not in {SCR_SUBTYPES}"
    if it.qti_type not in QTI_SCR:
        return False, f"SCR qti_type '{it.qti_type}' not in {QTI_SCR}"
    if not it.stem.strip():
        return False, "empty stem"
    if not it.answer_key:
        return False, "SCR needs a model answer_key"
    if it.options:
        return False, "SCR (text-entry) takes no options"
    return True, f"schema ok (SCR {it.subskill_or_mode})"

def gate_scr_binding(it: Item) -> tuple[bool, str]:
    if it.family != "SCR":
        return True, "n/a (not SCR)"
    must_bind = SCR_BINDING.get(it.subskill_or_mode, False)
    has_ref = bool(it.stimulus_ref.strip())
    if must_bind and not has_ref:
        return False, f"{it.subskill_or_mode} must bind a stimulus (stimulus_ref empty)"
    if not must_bind and has_ref:
        return False, f"{it.subskill_or_mode} must NOT bind a stimulus (sentence-level)"
    if must_bind:
        # reuse CR's stimulus-existence scan
        ok, detail = gate_cr_binding(_as_cr_for_binding(it))
        if not ok:
            return False, detail
    return True, ("bound to " + it.stimulus_ref) if must_bind else "no stimulus (correct)"

def gate_scr_rubric(it: Item) -> tuple[bool, str]:
    if it.family != "SCR":
        return True, "n/a (not SCR)"
    want = SCR_RUBRIC_FOR.get(it.subskill_or_mode)
    if it.rubric_ref != want:
        return False, f"SCR {it.subskill_or_mode} needs rubric_ref '{want}', got '{it.rubric_ref}'"
    return True, f"rubric {it.rubric_ref}"
```

3c. Add the tiny helper `_as_cr_for_binding` (lets us reuse `gate_cr_binding`'s stimulus scan without duplicating the glob). Place directly above `gate_scr_binding`:

```python
def _as_cr_for_binding(it: Item) -> Item:
    """A shim so SCR binding reuses gate_cr_binding's stimulus-existence scan."""
    return Item(id=it.id, family="CR", grade=it.grade, stem=it.stem,
                qti_type="extended-text", subskill_or_mode="argument",
                stimulus_ref=it.stimulus_ref, rubric_ref="rc.staar")
```

3d. Register the SCR gates in the `GATES` list (insert after `no_change_discipline`, before `content`):

```python
    ("scr_schema", gate_scr_schema),
    ("scr_binding", gate_scr_binding),
    ("scr_rubric", gate_scr_rubric),
```

3e. In `gate_cr_binding` and `gate_rubric_config`, the guard `if it.family != "CR"` already returns early for SCR — leave them. In `gate_schema`, add an early pass-through so SCR skips SR/CR schema logic:

```python
def gate_schema(it: Item) -> tuple[bool, str]:
    if it.family not in ("SR", "CR", "SCR"):
        return False, f"bad family '{it.family}'"
    if it.family == "SCR":
        return True, "schema ok (SCR — validated by scr_schema gate)"
    if not it.stem.strip():
        return False, "empty stem"
    # ... existing SR/CR logic unchanged ...
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python -m pytest pipeline/tests/test_scr_family.py -v`
Expected: PASS (6 passed).

- [ ] **Step 5: Run the existing contract self-test (regression)**

Run: `python pipeline/item_contract.py`
Expected: the built-in SR + CR examples still print PASS, exit 0.

- [ ] **Step 6: Commit**

```bash
git add pipeline/item_contract.py pipeline/tests/test_scr_family.py
git commit -m "feat(contract): add SCR family with subtype-conditional gates + short-CR rubrics"
```

---

## Task 2: Author the diversified `scr_writing` bank

**Files:**
- Create: `Item_Bank_G9/scr_writing.py`
- Delete: `Item_Bank_G9/sr_scr_modifier.py` (after migrating its 10 items)

**Interfaces:**
- Consumes: `Item`, `qc_item`, `qc_report` from `item_contract`; the `SCR` family from Task 1.
- Produces: module-level `ITEMS: list[Item]` (~15-20 items, all `family="SCR"`, `subskill_or_mode="scr_writing"`, `rubric_ref="rc.scr1"`, no `stimulus_ref`). IDs `ACC-W910-SCR-WRIT-0501..05NN`.

- [ ] **Step 1: Create the file with the builder + migrated items + new task types**

Create `Item_Bank_G9/scr_writing.py`. Header docstring (no em dashes), then:

```python
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from item_contract import Item, qc_item, qc_report  # noqa: E402

ACC_CONV = ["ACC.W.CONV.1", "CCSS.L.9-10.1"]
ACC_LANG = ["ACC.W.CONV.3", "CCSS.L.9-10.3"]   # precise word choice / knowledge of language
ACC_COH  = ["ACC.W.ARG.3", "CCSS.W.9-10.1c"]   # cohesion / transitions in revision
PROV = {"copyright": "own_authored", "authored": "2026-07-21"}

def scr(idnum, instruction, flawed, model, task_type, acc, note=""):
    """Build one writing-domain SCR (0-1, text-entry, no stimulus)."""
    stem = instruction + (f" ({note})" if note else "") + f'\n\nSentence: "{flawed}"'
    return Item(id=idnum, family="SCR", grade="9-10", subskill_or_mode="scr_writing",
                qti_type="text-entry", stem=stem, acc_tags=list(acc), options=[],
                answer_key=[model], rubric_ref="rc.scr1",
                provenance=dict(PROV, task_type=task_type))

ITEMS = [
    # --- migrated: modifier-repair (from sr_scr_modifier.py), 10 items ---
    scr("ACC-W910-SCR-WRIT-0501",
        "Rewrite the sentence to correct the dangling participle. Keep the original meaning.",
        "Running to catch the bus, my backpack fell open.",
        "Running to catch the bus, I felt my backpack fall open.",
        "modifier_repair", ACC_CONV),
    # ... (migrate the remaining 9 modifier items verbatim from sr_scr_modifier.py, new IDs 0502-0510) ...

    # --- NEW: sentence-combining (4 items) ---
    scr("ACC-W910-SCR-WRIT-0511",
        "Combine the two sentences into one clear sentence, keeping all the information.",
        "The library extended its hours. Students now have more time to study after practice.",
        "The library extended its hours, so students now have more time to study after practice.",
        "sentence_combining", ACC_CONV),
    # ... 3 more sentence-combining ...

    # --- NEW: precise word choice (4 items) ---
    scr("ACC-W910-SCR-WRIT-0515",
        "Replace the vague underlined word with a more precise one that fits the sentence's meaning.",
        "The new policy had a really big effect on how students got to school.",
        "The new policy sharply changed how students got to school.",
        "precise_word_choice", ACC_LANG),
    # ... 3 more precise-word-choice ...

    # --- NEW: revise-for-cohesion (4 items) ---
    scr("ACC-W910-SCR-WRIT-0519",
        "Rewrite the second sentence so it connects clearly to the first, without repeating words awkwardly.",
        "The city added bike lanes downtown. The city hoped the bike lanes downtown would cut traffic.",
        "The city added bike lanes downtown, hoping they would cut traffic.",
        "revise_for_cohesion", ACC_COH),
    # ... 3 more revise-for-cohesion ...

    # --- NEW: add/sharpen a transition (4 items) ---
    scr("ACC-W910-SCR-WRIT-0523",
        "Rewrite the second sentence to open with a transition that shows its logical link to the first.",
        "The team practiced every morning for months. They lost in the first round.",
        "The team practiced every morning for months. Even so, they lost in the first round.",
        "transition", ACC_COH),
    # ... 3 more transition ...
]

def main() -> int:
    passed = 0
    for it in ITEMS:
        qc_item(it)
        print(qc_report(it)); print()
        if it.qc["passed"]:
            passed += 1
    print(f"{passed}/{len(ITEMS)} PASS")
    return 0 if passed == len(ITEMS) else 1

if __name__ == "__main__":
    sys.exit(main())
```

Author the full set (target 18-20 items): migrate all 10 modifier items with verbatim wording (renumber to 0501-0510), then write 8-10 new items across the four task types shown. Every stem/model/note MUST be em-dash-free.

- [ ] **Step 2: Run the bank self-test**

Run: `python "Item_Bank_G9/scr_writing.py"`
Expected: prints each item's QC, ends `18/18 PASS` (or your final N/N), exit 0.

- [ ] **Step 3: Delete the superseded modifier file**

```bash
git rm "Item_Bank_G9/sr_scr_modifier.py"
```

- [ ] **Step 4: Grep for stragglers**

Run: `grep -rn "sr_scr_modifier" pipeline/ Item_Bank_G9/ --include=*.py`
Expected: only matches are in `assemble_test.py`/`render_model_tests.py` (fixed in Tasks 3-4). If any other `.py` imports it, note for Task 3.

- [ ] **Step 5: Commit**

```bash
git add "Item_Bank_G9/scr_writing.py"
git commit -m "feat(g9-items): diversified scr_writing bank (migrate modifier + 4 new SCR task types)"
```

---

## Task 3: Update crosscheck + coverage tools for the SCR family

**Files:**
- Modify: `pipeline/testbank_kc_crosscheck.py` (add `rc.scr1/2/3` to `KNOWN_RUBRICS`; recognize SCR family)
- Modify: `pipeline/coverage_matrix.py` (only if it filters on subskill `"scr"`)

**Interfaces:**
- Consumes: `SCR_SUBTYPES`, `SCR_RUBRICS` from Task 1.
- Produces: crosschecks that PASS with the migrated bank.

- [ ] **Step 1: Inspect the two tools for `scr`/rubric references**

Run: `grep -n "scr\|KNOWN_RUBRICS\|sr_scr_modifier\|subskill" pipeline/testbank_kc_crosscheck.py pipeline/coverage_matrix.py`
Expected: locate `KNOWN_RUBRICS = {...}` and any `"scr"` subskill mapping.

- [ ] **Step 2: Add the SCR rubrics to `KNOWN_RUBRICS`**

In `pipeline/testbank_kc_crosscheck.py`, extend the set:

```python
KNOWN_RUBRICS = {"rc.staar", "rc.mcas", "rc.ohio", "rc.4trait", "rc.ap", "rc.sc", "rc.fl",
                 "rc.scr1", "rc.scr2", "rc.scr3"}
```

If it maps item families/subskills to ACC codes, map `scr_writing` → `ACC.W.CONV.1` (mirroring how `sr_scr_modifier`/`scr` mapped). If `coverage_matrix.py` references `sr_scr_modifier` or `"scr"` in a "measured by" list, replace with `scr_writing`.

- [ ] **Step 3: Run both crosschecks**

Run: `python pipeline/testbank_kc_crosscheck.py && python pipeline/coverage_matrix.py`
Expected: both PASS (`PASS: item bank aligns...`, `N tested skills | N fully covered | 0 with a coverage gap`).

- [ ] **Step 4: Commit**

```bash
git add pipeline/testbank_kc_crosscheck.py pipeline/coverage_matrix.py
git commit -m "chore(crosscheck): recognize SCR family + rc.scr rubrics"
```

---

## Task 4: Rebalance the G9 blueprint to writing-only (points-weighted)

**Files:**
- Modify: `pipeline/render_model_tests.py` — `BLUEPRINTS["G9"]` (this is the file that assembles the G9 form)
- Modify: `pipeline/assemble_test.py:39` — switch the G10 blueprint's SCR section to the SCR family (consistency; no G10 rebalance)

**Interfaces:**
- Consumes: the `scr_writing` items (Task 2) discoverable via glob in `Item_Bank_G9/`.
- Produces: a G9 model form of shape ~15-18 MCQ + 2-4 `scr_writing` SCR + 1 single-source ECR, points-weighted.

- [ ] **Step 1: Read the current G9 blueprint + how sections filter items**

Run: `sed -n '20,60p' pipeline/render_model_tests.py`
Confirm each blueprint row is `{section, label, family, subskills|modes, count, scoring}` and how the assembler pools by `family` + `subskills`/`modes`.

- [ ] **Step 2: Rewrite `BLUEPRINTS["G9"]`**

Replace the G9 list with the writing-only, points-weighted shape. Change the SCR row from `family="SR", subskills=["scr"]` to the SCR family, and set counts per the design:

```python
    "G9": [
        {"section": "ECR", "label": "Extended Constructed Response (single-source essay, argument OR informational)",
         "family": "CR", "modes": ["argument", "explanatory"], "count": 1,
         "scoring": "rc.staar (Org/Dev 0-3 + Conv 0-2, x2 = 10)"},
        {"section": "SCR", "label": "Writing Short Constructed Response (repair/revision, 0-1)",
         "family": "SCR", "subskills": ["scr_writing"], "count": 3, "scoring": "rc.scr1 (0-1)"},
        {"section": "MC-evid", "label": "Evidence in context (add/delete/relevance)",
         "family": "SR", "subskills": ["evidence"], "count": 4, "scoring": "auto-key"},
        {"section": "MC-org", "label": "Organization & cohesion",
         "family": "SR", "subskills": ["organization"], "count": 4, "scoring": "auto-key"},
        {"section": "MC-conv", "label": "Conventions & mechanics",
         "family": "SR", "subskills": ["conventions"], "count": 5, "scoring": "auto-key"},
        {"section": "MC-sent", "label": "Sentence structure & boundaries",
         "family": "SR", "subskills": ["sentence"], "count": 4, "scoring": "auto-key"},
    ],
```

This yields ~17 MC + 3 SCR + 1 ECR.

**REQUIRED code change (verified):** `render_model_tests.py`'s `_pool` (around lines 81-85) only matches `family == "CR"` (by `modes`) or `family == "SR"` (by `subskills`). An SCR row would pool ZERO items. Widen it to add an SCR branch that filters by subtype (SCR uses the `subskills` key to hold subtype names, matching the blueprint rows above):

Full corrected function (copy verbatim):

```python
def _pool(items, spec):
    idc = spec.get("id_contains")
    out = [it for it in items if it.family == spec["family"] and (
        (spec["family"] == "CR" and it.mode in spec.get("modes", [])) or
        (spec["family"] == "SR" and it.mode in spec.get("subskills", [])) or
        (spec["family"] == "SCR" and it.mode in spec.get("subskills", []))) and (
        idc is None or idc in it.id)]
    return sorted(out, key=lambda i: i.id)
```

`_load_items` copies `it.family` and `it.mode = it.subskill_or_mode` onto its slotted objects (verified ~line 74), so SCR items surface with `family="SCR"` and `mode="scr_writing"` — the new branch matches them.

- [ ] **Step 3: Fix the G10 blueprint SCR row in `assemble_test.py` (consistency only)**

`assemble_test.py:39` currently reads `{"family": "SR", ... "subskills": ["scr"], ...}`. Since `scr` no longer exists as an SR subskill, and G10 keeps `sr_scr_modifier.py`, either (a) migrate G10's `sr_scr_modifier.py` to `scr_writing` in a follow-up, OR (b) for now point this row at `family="SCR", subskills=["scr_writing"]` and note G10 items migrate later. Choose (b) to keep the crosscheck green; add a `# TODO(G10 follow-up): migrate Item_Bank_G10 scr items` comment.

- [ ] **Step 4: Assemble the G9 form**

Run: `python pipeline/render_model_tests.py G9`
Expected: prints a blueprint-conformant G9 form, blueprint check OK, no "item does not exist" errors, disjoint-form line present.

- [ ] **Step 5: Regression — G10 form still assembles**

Run: `python pipeline/assemble_test.py --forms 1`
Expected: still prints a valid G10 form (blueprint OK, disjoint). If it errors on the SCR family, the pool filter needs the `"SCR"` widening from Step 2.

- [ ] **Step 6: Commit**

```bash
git add pipeline/render_model_tests.py pipeline/assemble_test.py
git commit -m "feat(g9-test): rebalance G9 blueprint to points-weighted writing-only shape"
```

---

## Task 5: Add the G9 counterclaim-recognition lesson beat

**Files:**
- Create: `Lesson_Bank_G9/lesson_g9_l20_counterclaim_recognition_v3_1.py`
- Reference: `Lesson_Bank_G10/lesson_g10_l01_counterclaim_claim.py` (the G10 full-counterclaim lesson — model the *recognition-only* subset on it, do NOT copy the refutation depth)

**Interfaces:**
- Consumes: `Lesson`, `Slot`, `qc_lesson`, `qc_report` from `pipeline/lesson_contract.py` (same imports the other `lesson_g9_l*_v3_1.py` files use).
- Produces: a `LESSON` object (+ `LESSONS = [LESSON]`) that passes `qc_lesson`'s gates; teaches recognize + acknowledge an opposing view (NOT refute).

- [ ] **Step 1: Read a sibling G9 lesson + the contract to mirror structure exactly**

Run: `sed -n '1,60p' Lesson_Bank_G9/lesson_g9_l02_sharpen_stakes_v3_1.py` and `grep -n "def qc_lesson\|class Lesson\|class Slot\|gates\|SLOT" pipeline/lesson_contract.py | head`
Confirm the `Lesson(...)` fields (id, grade, lesson_type, unit, title, target, acc_tags, provenance, slots=[Slot(...)]) and the SRSD slot roles (TEACH/MODEL/SUPPORTED/INDEPENDENT/TRANSFER).

- [ ] **Step 2: Author the lesson**

Create the file mirroring `lesson_g9_l02_..._v3_1.py`'s structure. Content requirements:
- ONE idea: "A strong argument shows it knows the other side exists. Naming an opposing view fairly (not knocking it down yet) makes your own claim look considered."
- TEACH: define an opposing view / counterclaim; show acknowledge language ("Some argue...", "It is true that..."). Explicitly scope: recognition + fair acknowledgment only; full refutation is a later (G10) skill.
- MODEL: a coping-model think-aloud spotting the opposing view in a short argument, then acknowledging it in one sentence.
- MODEL/discrimination: which sentence fairly ACKNOWLEDGES an opposing view vs. (a) ignores it, (b) attacks a strawman, (c) just restates the writer's claim. Distractors carry misconception rationales.
- SUPPORTED then INDEPENDENT + TRANSFER: student writes one acknowledgment sentence for a given claim, on a partitioned topic.
- `acc_tags=["ACC.W.ARG.2", "CCSS.W.9-10.1a"]`; provenance `{"copyright":"own_authored","authored":"2026-07-21","kc":"C.9.01","scope_note":"counterclaim RECOGNITION only; full acknowledge+refute deferred to C.10.01/G10"}`.
- No em dashes.

- [ ] **Step 3: Run the lesson self-test**

Run: `python "Lesson_Bank_G9/lesson_g9_l20_counterclaim_recognition_v3_1.py"`
Expected: prints `qc_report`, ends `1/1 PASS`, exit 0.

- [ ] **Step 4: Commit**

```bash
git add "Lesson_Bank_G9/lesson_g9_l20_counterclaim_recognition_v3_1.py"
git commit -m "feat(g9-lesson): counterclaim-recognition beat (recognize+acknowledge; refute stays G10)"
```

---

## Task 6: Add a counterclaim-recognition test item + wire it to the G9 form

**Files:**
- Create or extend: `Item_Bank_G9/sr_organization.py` OR a small `Item_Bank_G9/sr_counterclaim_recognition.py` (SR family, subskill `organization`, `choice`) — pick per how the assembler pools (a distinct file is cleaner; use subskill `organization` since it is a discourse-structure recognition item, OR add a new SR subskill if the design warrants — default: reuse `organization`).
- Modify: `pipeline/render_model_tests.py` `BLUEPRINTS["G9"]` if a dedicated section is wanted.

**Interfaces:**
- Consumes: the SR family (unchanged), the counterclaim-recognition lesson (Task 5) as its taught source.
- Produces: ≥3 selected-response items where the student identifies the sentence that fairly acknowledges an opposing view.

- [ ] **Step 1: Write the items**

Create `Item_Bank_G9/sr_counterclaim_recognition.py` mirroring `sr_evidence.py`'s builder style. ≥3 `choice` items: stem asks which sentence fairly acknowledges the opposing view; correct = a fair acknowledgment; distractors = ignores it / strawman / restates own claim (each with a misconception rationale). `acc_tags=["ACC.W.ARG.2","CCSS.W.9-10.1a"]`, `subskill_or_mode="organization"`, length-balanced options (no length leak), no em dashes.

- [ ] **Step 2: Run the bank self-test**

Run: `python "Item_Bank_G9/sr_counterclaim_recognition.py"`
Expected: `N/N PASS`, exit 0.

- [ ] **Step 3: Add one recognition item to the G9 form**

In `render_model_tests.py` `BLUEPRINTS["G9"]`, add:

```python
        {"section": "MC-counter", "label": "Recognize a fair acknowledgment of the opposing view",
         "family": "SR", "subskills": ["organization"], "count": 1, "scoring": "auto-key"},
```

(If these items share the `organization` subskill with the existing org set, give them a distinguishable ID prefix like `-CCR-` and, if the assembler supports `id_contains`, filter on it; otherwise ensure the org pool ordering surfaces them.)

- [ ] **Step 4: Re-assemble + verify**

Run: `python pipeline/render_model_tests.py G9`
Expected: form now includes the counterclaim-recognition section, blueprint OK.

- [ ] **Step 5: Commit**

```bash
git add "Item_Bank_G9/sr_counterclaim_recognition.py" pipeline/render_model_tests.py
git commit -m "feat(g9-items): counterclaim-recognition SR items + wire into G9 form"
```

---

## Task 7: Final verification sweep

**Files:** none (verification only)

- [ ] **Step 1: All new/changed self-tests pass**

Run:
```bash
python pipeline/item_contract.py
python "Item_Bank_G9/scr_writing.py"
python "Item_Bank_G9/sr_counterclaim_recognition.py"
python "Lesson_Bank_G9/lesson_g9_l20_counterclaim_recognition_v3_1.py"
python -m pytest pipeline/tests/test_scr_family.py -v
```
Expected: every one exits 0 / all PASS.

- [ ] **Step 2: Crosschecks + coverage green**

Run:
```bash
python pipeline/testbank_kc_crosscheck.py
python pipeline/kc_coverage_matrix.py
python pipeline/coverage_matrix.py
python pipeline/render_model_tests.py G9
python pipeline/assemble_test.py --forms 1
```
Expected: all PASS; G9 form is writing-only shape (~17 MC + 3 SCR + 1 ECR + counterclaim-recognition), G10 form still valid.

- [ ] **Step 3: House-rule sweep — no em dashes in new files**

Run: `grep -rn "—\|–" "Item_Bank_G9/scr_writing.py" "Item_Bank_G9/sr_counterclaim_recognition.py" "Lesson_Bank_G9/lesson_g9_l20_counterclaim_recognition_v3_1.py"`
Expected: no matches.

- [ ] **Step 4: Confirm the audit claim holds — every G9-tested skill is G9-taught**

Manually confirm the G9 form's sections each map to a G9 KC that a G9 lesson teaches: ECR→C.9.04, SCR(scr_writing)→C.9.06/CONV, evidence→C.9.02, organization→C.9.06, conventions/sentence→C.9.06 (woven/external), counterclaim-recognition→C.9.01 + Task 5 lesson. No section requires C.10.* (analysis/synthesis/full-counterclaim).

- [ ] **Step 5: Final commit (if any doc/notes updated)**

```bash
git add -A
git commit -m "test(g9): final verification sweep for SCR diversification + writing-only rebalance"
```

---

## Self-Review

**Spec coverage:**
- Component 1 (SCR family + gates) → Task 1. ✓
- Component 2 (rc.scr1/2/3 configs) → Task 1 (defined) + Task 3 (crosscheck known). ✓
- Component 3 (scr_writing bank) → Task 2. ✓
- Component 4 (counterclaim-recognition teach) → Task 5. ✓
- Component 5 (G9 blueprint rebalance in render_model_tests.py) → Task 4. ✓
- Migration blast radius (item_contract, assemble_test, render_model_tests, crosschecks) → Tasks 1,3,4. ✓
- Counterclaim-recognition *tested* fairly → Task 6 (item follows Task 5 lesson). ✓
- Verification / coverage-not-efficacy → Task 7. ✓

**Deferred (correctly, per spec non-goals):** G10 scr_analysis/scr_research authoring; live grader wiring of rc.scr*; G10 form rebalance.

**Placeholder scan:** No "TBD/handle appropriately"; the two intentional `# TODO(G10 follow-up)` markers are explicit deferrals named in the spec non-goals, not gaps in this plan.

**Type consistency:** `family="SCR"`, `subskill_or_mode` ∈ `SCR_SUBTYPES`, `rubric_ref` per `SCR_RUBRIC_FOR`, `SCR_BINDING` gate — names identical across Tasks 1, 2, 4, 6. `scr()` builder signature consistent within Task 2.
