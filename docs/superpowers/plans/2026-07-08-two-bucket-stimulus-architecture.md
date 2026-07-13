# Two-Bucket Stimulus Architecture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Split the stimulus layer into two buckets (lesson vs test), make it inexhaustible via compose-from-tagged-singles + on-demand minting, and enforce a hard lesson-to-test contamination partition.

**Architecture:** One shared-base stimulus contract with a `bucket` profile switch ("lesson" | "test"); the ATOM is a single tagged passage; multi-source stimuli are COMPOSED on demand from singles under a shared proposition (opposing) or theme (complementary), gated for combinability; test difficulty is calibrated against a human-scored anchor set; topic partition + reservation prevents a student being tested on a learned topic.

**Tech Stack:** Python 3.11+, standard library ONLY (no pip installs). Tests are assertion-based self-tests in `if __name__ == "__main__"` blocks run with `python <file>.py`, exiting 0 on pass / non-zero on fail. This is the established codebase idiom (see `pipeline/stimulus_contract.py`, `item_contract.py`, `lesson_contract.py`). Do NOT introduce pytest.

## Global Constraints

- Python stdlib only; dependency-free except sibling `pipeline/` modules (`readability_gate`, `content_screen`). Copied verbatim from the codebase pattern.
- NO em dashes in any authored prose or docstrings (house rule; there is a gate for it).
- Every new module ends with an `if __name__ == "__main__":` self-test that asserts behavior and `sys.exit(0 if ok else 1)`.
- All work lives under `Alpha HS Writing Course 2026-27/pipeline/` unless a path says otherwise.
- Run everything from the `Alpha HS Writing Course 2026-27/` directory (so `python pipeline/<f>.py` resolves sibling imports via the files' own `sys.path.insert`).
- Existing 16 G10 stimuli must still pass QC after every task (regression: `python pipeline/bank_loader.py` exits 0).
- Spec of record: `docs/superpowers/specs/2026-07-08-two-bucket-stimulus-architecture-design.md`.
- Grade-agnostic: all IDs/params carry `grade`; G10 is the seed grade but nothing hard-codes it.

---

## File Structure

- `pipeline/topic_registry.py` (NEW) — topic_id + domain + pool assignment (lesson_pool | test_pool | shared_ok); reservation + starvation alarm.
- `pipeline/proposition_registry.py` (NEW) — proposition_id -> arguable question; stance-tagged single membership; opposing-pair candidate enumeration.
- `pipeline/theme_registry.py` (NEW) — theme_id -> facets; connection_point tagging; complementary-pair candidate enumeration.
- `pipeline/calibration_anchors.py` (NEW) — human-scored anchor set per {grade, mode, form}; the equivalent-form band + gate.
- `pipeline/composition.py` (NEW) — the composer + composition gate (structural checks + combinability judge hook).
- `pipeline/stimulus_contract.py` (MODIFY) — add `bucket` + tagging fields to `StimulusRecord`; split gates into shared-base + per-profile; replace `gate_two_sidedness` with a composition-aware check.
- `Stimulus_Bank_G10/*` (MIGRATE) — decompose the 6 opposing pairs into 12 stance-tagged singles; tag all singles with bucket/topic/proposition/theme.
- `pipeline/bank_loader.py` (MODIFY) — load singles + composed views; keep the 152-object regression green.

**Dependency order:** registries + anchors (leaf modules, no deps on each other) -> composition (uses registries) -> contract refactor (uses bucket + composition) -> migration (uses the refactored contract) -> loader update. Tasks are ordered so each builds only on earlier ones.

---

## Task 1: Topic registry

**Files:**
- Create: `pipeline/topic_registry.py`

**Interfaces:**
- Consumes: nothing (leaf module).
- Produces:
  - `POOL_LESSON = "lesson_pool"`, `POOL_TEST = "test_pool"`, `POOL_SHARED = "shared_ok"` (str constants)
  - `@dataclass Topic{ topic_id: str, domain: str, pool: str, grade: str }`
  - `class TopicRegistry` with:
    - `add(topic: Topic) -> None`
    - `reserve_test_first(domain: str, topic_ids: list[str], grade: str, n_test: int) -> None` (assigns first `n_test` to test_pool, rest to lesson_pool)
    - `pool_of(topic_id: str) -> str | None`
    - `topics_for(pool: str, grade: str, domain: str | None = None) -> list[str]`
    - `starvation(grade: str, domain: str, bucket_pool: str, projected_use: int) -> dict` returns `{"remaining": int, "alarm": bool}` (alarm True when remaining < projected_use)

- [ ] **Step 1: Write the failing self-test**

Create `pipeline/topic_registry.py` with ONLY this `__main__` block at the bottom (module body empty for now):

```python
if __name__ == "__main__":
    r = TopicRegistry()
    r.reserve_test_first("energy", ["nuclear_power", "solar", "wind", "coal"], "9-10", n_test=2)
    assert r.pool_of("nuclear_power") == POOL_TEST, "first reserved -> test"
    assert r.pool_of("wind") == POOL_LESSON, "remainder -> lesson"
    assert set(r.topics_for(POOL_TEST, "9-10", "energy")) == {"nuclear_power", "solar"}
    assert r.pool_of("unknown") is None
    st = r.starvation("9-10", "energy", POOL_TEST, projected_use=5)
    assert st["remaining"] == 2 and st["alarm"] is True, "2 test topics < 5 projected -> alarm"
    st2 = r.starvation("9-10", "energy", POOL_TEST, projected_use=1)
    assert st2["alarm"] is False
    print("topic_registry self-test PASS")
    import sys; sys.exit(0)
```

- [ ] **Step 2: Run to verify it fails**

Run: `python pipeline/topic_registry.py`
Expected: FAIL (`NameError: name 'TopicRegistry' is not defined`).

- [ ] **Step 3: Write the minimal implementation**

Above the `__main__` block:

```python
"""topic_registry.py - topic partition + reservation for the two-bucket stimulus layer.

A topic is coarser than a passage (one topic supports many passages). Each topic is assigned to a pool:
lesson-only, test-only, or shared. Test gets first claim on a domain's topics (test needs unseen-per-student
depth and cannot borrow lesson topics). Dependency-free (stdlib only)."""
from __future__ import annotations
from dataclasses import dataclass

POOL_LESSON = "lesson_pool"
POOL_TEST = "test_pool"
POOL_SHARED = "shared_ok"

@dataclass
class Topic:
    topic_id: str
    domain: str
    pool: str
    grade: str

class TopicRegistry:
    def __init__(self) -> None:
        self._topics: dict[str, Topic] = {}

    def add(self, topic: Topic) -> None:
        self._topics[topic.topic_id] = topic

    def reserve_test_first(self, domain: str, topic_ids: list[str], grade: str, n_test: int) -> None:
        for i, tid in enumerate(topic_ids):
            pool = POOL_TEST if i < n_test else POOL_LESSON
            self.add(Topic(topic_id=tid, domain=domain, pool=pool, grade=grade))

    def pool_of(self, topic_id: str) -> str | None:
        t = self._topics.get(topic_id)
        return t.pool if t else None

    def topics_for(self, pool: str, grade: str, domain: str | None = None) -> list[str]:
        return [t.topic_id for t in self._topics.values()
                if t.pool == pool and t.grade == grade and (domain is None or t.domain == domain)]

    def starvation(self, grade: str, domain: str, bucket_pool: str, projected_use: int) -> dict:
        remaining = len(self.topics_for(bucket_pool, grade, domain))
        return {"remaining": remaining, "alarm": remaining < projected_use}
```

- [ ] **Step 4: Run to verify it passes**

Run: `python pipeline/topic_registry.py`
Expected: `topic_registry self-test PASS` and exit 0.

- [ ] **Step 5: Commit**

```bash
git add "Alpha HS Writing Course 2026-27/pipeline/topic_registry.py"
git commit -m "feat(stimulus): topic registry with test-first reservation + starvation alarm"
```

---

## Task 2: Proposition registry (opposing-pair candidates)

**Files:**
- Create: `pipeline/proposition_registry.py`

**Interfaces:**
- Consumes: nothing (leaf module).
- Produces:
  - `@dataclass Single{ single_id: str, proposition_id: str, stance: str, lexile: int, words: int, source_org: str }` where `stance in {"pro","con","nuanced"}`
  - `class PropositionRegistry` with:
    - `add(single: Single) -> None`
    - `singles(proposition_id: str, stance: str | None = None) -> list[Single]`
    - `opposing_candidates(proposition_id: str, lexile_window: int = 100, len_ratio: float = 1.4) -> list[tuple[Single, Single]]` returns every (pro, con) pair under the proposition whose Lexile differ by <= `lexile_window`, whose word counts are within `len_ratio`, and whose `source_org` differ.

- [ ] **Step 1: Write the failing self-test**

```python
if __name__ == "__main__":
    r = PropositionRegistry()
    P = "prop_nuclear"
    r.add(Single("s_pro1", P, "pro", 1120, 300, "US EIA"))
    r.add(Single("s_con1", P, "con", 1150, 320, "US GAO"))
    r.add(Single("s_con2", P, "con", 1400, 900, "US GAO"))   # too hard + too long -> excluded
    r.add(Single("s_pro2", P, "pro", 1130, 305, "US EIA"))   # same org as s_pro1 (n/a, pro vs con only)
    cands = r.opposing_candidates(P, lexile_window=100, len_ratio=1.4)
    ids = {(a.single_id, b.single_id) for a, b in cands}
    assert ("s_pro1", "s_con1") in ids, "close pro/con, distinct orgs -> candidate"
    assert all("s_con2" not in pair for pair in ids), "s_con2 out of Lexile/len window -> excluded"
    assert all(a.stance == "pro" and b.stance == "con" for a, b in cands)
    assert all(a.source_org != b.source_org for a, b in cands), "distinct orgs required"
    print("proposition_registry self-test PASS")
    import sys; sys.exit(0)
```

- [ ] **Step 2: Run to verify it fails**

Run: `python pipeline/proposition_registry.py`
Expected: FAIL (`NameError: PropositionRegistry`).

- [ ] **Step 3: Write the minimal implementation**

```python
"""proposition_registry.py - opposing-pair composition backbone.

A proposition is one arguable question. Argumentative SINGLE passages are tagged with proposition_id + stance.
An opposing pair is composed by picking one pro + one con UNDER THE SAME proposition, with Lexile/length parity
and distinct source orgs. Same-question-opposite-side is mechanical, not a human judgment. Stdlib only."""
from __future__ import annotations
from dataclasses import dataclass

VALID_STANCES = {"pro", "con", "nuanced"}

@dataclass
class Single:
    single_id: str
    proposition_id: str
    stance: str
    lexile: int
    words: int
    source_org: str

class PropositionRegistry:
    def __init__(self) -> None:
        self._by_prop: dict[str, list[Single]] = {}

    def add(self, single: Single) -> None:
        if single.stance not in VALID_STANCES:
            raise ValueError(f"bad stance '{single.stance}' (must be one of {VALID_STANCES})")
        self._by_prop.setdefault(single.proposition_id, []).append(single)

    def singles(self, proposition_id: str, stance: str | None = None) -> list[Single]:
        rows = self._by_prop.get(proposition_id, [])
        return [s for s in rows if stance is None or s.stance == stance]

    def opposing_candidates(self, proposition_id: str, lexile_window: int = 100,
                            len_ratio: float = 1.4) -> list[tuple[Single, Single]]:
        pros = self.singles(proposition_id, "pro")
        cons = self.singles(proposition_id, "con")
        out: list[tuple[Single, Single]] = []
        for a in pros:
            for b in cons:
                if abs(a.lexile - b.lexile) > lexile_window:
                    continue
                hi, lo = max(a.words, b.words), min(a.words, b.words)
                if lo == 0 or hi / lo > len_ratio:
                    continue
                if a.source_org == b.source_org:
                    continue
                out.append((a, b))
        return out
```

- [ ] **Step 4: Run to verify it passes**

Run: `python pipeline/proposition_registry.py`
Expected: `proposition_registry self-test PASS` and exit 0.

- [ ] **Step 5: Commit**

```bash
git add "Alpha HS Writing Course 2026-27/pipeline/proposition_registry.py"
git commit -m "feat(stimulus): proposition registry + opposing-pair candidate composition"
```

---

## Task 3: Theme registry (complementary-pair candidates)

**Files:**
- Create: `pipeline/theme_registry.py`

**Interfaces:**
- Consumes: nothing (leaf module).
- Produces:
  - `@dataclass ThemeSingle{ single_id: str, theme_id: str, facet: str, connection_point: str, lexile: int, words: int }`
  - `class ThemeRegistry` with:
    - `add(single: ThemeSingle) -> None`
    - `singles(theme_id: str) -> list[ThemeSingle]`
    - `complementary_candidates(theme_id: str, lexile_window: int = 100) -> list[tuple[ThemeSingle, ThemeSingle]]` returns pairs under the theme with DIFFERENT facets, the SAME non-empty connection_point, and Lexile within window. (The shared connection_point is the structural proxy for "genuinely combines"; the semantic combinability judge is applied later in composition.)

- [ ] **Step 1: Write the failing self-test**

```python
if __name__ == "__main__":
    r = ThemeRegistry()
    T = "theme_pollinators"
    CP = "pollinator decline threatens the food supply"
    r.add(ThemeSingle("t1", T, "causes", CP, 1100, 300))
    r.add(ThemeSingle("t2", T, "consequences", CP, 1130, 310))
    r.add(ThemeSingle("t3", T, "causes", CP, 1110, 305))          # same facet as t1 -> not with t1
    r.add(ThemeSingle("t4", T, "solutions", "unrelated thread", 1120, 300))  # different connection_point
    cands = r.complementary_candidates(T, lexile_window=100)
    ids = {frozenset((a.single_id, b.single_id)) for a, b in cands}
    assert frozenset(("t1", "t2")) in ids, "different facet + shared connection_point -> candidate"
    assert frozenset(("t1", "t3")) not in ids, "same facet -> excluded"
    assert all("t4" not in {a.single_id, b.single_id} for a, b in cands), "different connection_point -> excluded"
    assert all(a.facet != b.facet for a, b in cands)
    print("theme_registry self-test PASS")
    import sys; sys.exit(0)
```

- [ ] **Step 2: Run to verify it fails**

Run: `python pipeline/theme_registry.py`
Expected: FAIL (`NameError: ThemeRegistry`).

- [ ] **Step 3: Write the minimal implementation**

```python
"""theme_registry.py - complementary-pair composition backbone.

A theme is one topic several passages illuminate from different facets. Complementary singles are tagged with
theme_id + facet + a connection_point (the one idea joining them). A complementary pair = two singles, same theme,
DIFFERENT facets, SAME connection_point. This is the structural proxy for combinability; a semantic combinability
judge is applied downstream in composition.py. Stdlib only."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class ThemeSingle:
    single_id: str
    theme_id: str
    facet: str
    connection_point: str
    lexile: int
    words: int

class ThemeRegistry:
    def __init__(self) -> None:
        self._by_theme: dict[str, list[ThemeSingle]] = {}

    def add(self, single: ThemeSingle) -> None:
        self._by_theme.setdefault(single.theme_id, []).append(single)

    def singles(self, theme_id: str) -> list[ThemeSingle]:
        return list(self._by_theme.get(theme_id, []))

    def complementary_candidates(self, theme_id: str,
                                 lexile_window: int = 100) -> list[tuple[ThemeSingle, ThemeSingle]]:
        rows = self.singles(theme_id)
        out: list[tuple[ThemeSingle, ThemeSingle]] = []
        for i in range(len(rows)):
            for j in range(i + 1, len(rows)):
                a, b = rows[i], rows[j]
                if a.facet == b.facet:
                    continue
                if not a.connection_point or a.connection_point != b.connection_point:
                    continue
                if abs(a.lexile - b.lexile) > lexile_window:
                    continue
                out.append((a, b))
        return out
```

- [ ] **Step 4: Run to verify it passes**

Run: `python pipeline/theme_registry.py`
Expected: `theme_registry self-test PASS` and exit 0.

- [ ] **Step 5: Commit**

```bash
git add "Alpha HS Writing Course 2026-27/pipeline/theme_registry.py"
git commit -m "feat(stimulus): theme registry + complementary-pair candidate composition"
```

---

## Task 4: Calibration anchor set + equivalent-form gate

**Files:**
- Create: `pipeline/calibration_anchors.py`

**Interfaces:**
- Consumes: nothing (leaf module; anchor values are supplied by a human, hard-coded/loaded).
- Produces:
  - `@dataclass Anchor{ anchor_id: str, grade: str, mode: str, form: str, lexile: int, passage_count: int, task_demand: int }` (`task_demand` = a human-assigned 1-5 profile score)
  - `@dataclass Band{ lexile_min: int, lexile_max: int, passage_count: int, demand_min: int, demand_max: int }`
  - `class AnchorSet` with:
    - `add(anchor: Anchor) -> None`
    - `band(grade: str, mode: str, form: str) -> Band | None` (min-max envelope of the human anchors on each axis)
    - `equivalent_form_ok(grade: str, mode: str, form: str, lexile: int, passage_count: int, task_demand: int) -> tuple[bool, str]` (True iff the candidate sits inside the anchor band on every axis)

- [ ] **Step 1: Write the failing self-test**

```python
if __name__ == "__main__":
    a = AnchorSet()
    # two human-scored anchors define the STAAR argument band
    a.add(Anchor("anc1", "9-10", "argument", "staar", lexile=1080, passage_count=2, task_demand=3))
    a.add(Anchor("anc2", "9-10", "argument", "staar", lexile=1160, passage_count=2, task_demand=4))
    band = a.band("9-10", "argument", "staar")
    assert band.lexile_min == 1080 and band.lexile_max == 1160
    assert band.passage_count == 2 and band.demand_min == 3 and band.demand_max == 4
    ok, _ = a.equivalent_form_ok("9-10", "argument", "staar", lexile=1120, passage_count=2, task_demand=3)
    assert ok, "inside band on every axis -> ok"
    bad_lex, why = a.equivalent_form_ok("9-10", "argument", "staar", lexile=1300, passage_count=2, task_demand=3)
    assert not bad_lex and "lexile" in why.lower()
    bad_pc, _ = a.equivalent_form_ok("9-10", "argument", "staar", lexile=1120, passage_count=1, task_demand=3)
    assert not bad_pc, "wrong passage count -> fail"
    none_band = a.band("9-10", "argument", "mcas")
    assert none_band is None, "no anchors for that form -> None"
    print("calibration_anchors self-test PASS")
    import sys; sys.exit(0)
```

- [ ] **Step 2: Run to verify it fails**

Run: `python pipeline/calibration_anchors.py`
Expected: FAIL (`NameError: AnchorSet`).

- [ ] **Step 3: Write the minimal implementation**

```python
"""calibration_anchors.py - human-scored anchor set that DEFINES on-grade test-form difficulty.

Test-form equivalence is anchored to human judgment, not sibling-pool statistics. Per {grade, mode, form} a human
scores a small reference set; the band is the min-max envelope of those anchors on each axis (Lexile, passage
count, task-demand 1-5). A candidate test stimulus is an equivalent form only if it sits inside the band on every
axis. Widening the band is a deliberate human act (add/adjust anchors), never a silent constant. Stdlib only."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Anchor:
    anchor_id: str
    grade: str
    mode: str
    form: str
    lexile: int
    passage_count: int
    task_demand: int   # human-assigned 1-5 profile

@dataclass
class Band:
    lexile_min: int
    lexile_max: int
    passage_count: int
    demand_min: int
    demand_max: int

class AnchorSet:
    def __init__(self) -> None:
        self._anchors: list[Anchor] = []

    def add(self, anchor: Anchor) -> None:
        self._anchors.append(anchor)

    def _for(self, grade: str, mode: str, form: str) -> list[Anchor]:
        return [a for a in self._anchors if a.grade == grade and a.mode == mode and a.form == form]

    def band(self, grade: str, mode: str, form: str) -> Band | None:
        rows = self._for(grade, mode, form)
        if not rows:
            return None
        pcs = {a.passage_count for a in rows}
        # anchors for one form should agree on passage_count; take the common value (min if human error)
        pc = min(pcs)
        return Band(
            lexile_min=min(a.lexile for a in rows),
            lexile_max=max(a.lexile for a in rows),
            passage_count=pc,
            demand_min=min(a.task_demand for a in rows),
            demand_max=max(a.task_demand for a in rows),
        )

    def equivalent_form_ok(self, grade: str, mode: str, form: str,
                           lexile: int, passage_count: int, task_demand: int) -> tuple[bool, str]:
        band = self.band(grade, mode, form)
        if band is None:
            return False, f"no anchor set for {grade}/{mode}/{form}; cannot certify equivalence"
        if not (band.lexile_min <= lexile <= band.lexile_max):
            return False, f"lexile {lexile} outside anchor band {band.lexile_min}-{band.lexile_max}"
        if passage_count != band.passage_count:
            return False, f"passage_count {passage_count} != anchor {band.passage_count}"
        if not (band.demand_min <= task_demand <= band.demand_max):
            return False, f"task_demand {task_demand} outside anchor band {band.demand_min}-{band.demand_max}"
        return True, "inside anchor band on every axis"
```

- [ ] **Step 4: Run to verify it passes**

Run: `python pipeline/calibration_anchors.py`
Expected: `calibration_anchors self-test PASS` and exit 0.

- [ ] **Step 5: Commit**

```bash
git add "Alpha HS Writing Course 2026-27/pipeline/calibration_anchors.py"
git commit -m "feat(stimulus): human-calibrated anchor set + equivalent-form gate"
```

---

## Task 5: Composition (composer + composition gate)

**Files:**
- Create: `pipeline/composition.py`

**Interfaces:**
- Consumes:
  - `proposition_registry.PropositionRegistry.opposing_candidates(...)`
  - `theme_registry.ThemeRegistry.complementary_candidates(...)`
- Produces:
  - `@dataclass ComposedPair{ family: str, left_id: str, right_id: str, source: str }` (`family in {"opposing","complementary"}`, `source` = proposition_id or theme_id)
  - `def compose_opposing(prop_reg, proposition_id, lexile_window=100, len_ratio=1.4) -> list[ComposedPair]`
  - `def compose_complementary(theme_reg, theme_id, judge=None, lexile_window=100) -> list[ComposedPair]` where `judge` is an optional callable `judge(left_single, right_single) -> bool` (the combinability judge; when None, structural checks alone decide; when provided, a pair is admitted only if the judge returns True). This is the seam where the LLM combinability judge plugs in at mint time.

- [ ] **Step 1: Write the failing self-test**

```python
if __name__ == "__main__":
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from proposition_registry import PropositionRegistry, Single
    from theme_registry import ThemeRegistry, ThemeSingle

    pr = PropositionRegistry()
    pr.add(Single("p1", "prop_x", "pro", 1100, 300, "US EIA"))
    pr.add(Single("c1", "prop_x", "con", 1120, 310, "US GAO"))
    opp = compose_opposing(pr, "prop_x")
    assert len(opp) == 1 and opp[0].family == "opposing"
    assert opp[0].left_id == "p1" and opp[0].right_id == "c1" and opp[0].source == "prop_x"

    tr = ThemeRegistry()
    CP = "shared thread"
    tr.add(ThemeSingle("a", "theme_y", "causes", CP, 1100, 300))
    tr.add(ThemeSingle("b", "theme_y", "effects", CP, 1120, 310))
    # structural-only: 1 candidate
    comp = compose_complementary(tr, "theme_y")
    assert len(comp) == 1 and comp[0].family == "complementary"
    # with a judge that rejects everything: 0 admitted
    comp_rejected = compose_complementary(tr, "theme_y", judge=lambda l, r: False)
    assert comp_rejected == [], "combinability judge veto drops the pair"
    # with a judge that accepts: 1 admitted
    comp_ok = compose_complementary(tr, "theme_y", judge=lambda l, r: True)
    assert len(comp_ok) == 1
    print("composition self-test PASS")
    sys.exit(0)
```

- [ ] **Step 2: Run to verify it fails**

Run: `python pipeline/composition.py`
Expected: FAIL (`NameError: compose_opposing`).

- [ ] **Step 3: Write the minimal implementation**

Above the `__main__` block:

```python
"""composition.py - compose multi-source stimuli from tagged singles, on demand.

A pair is never authored as a unit; it is composed WITHIN a proposition (opposing) or a theme (complementary),
so combinability is guaranteed by construction. Opposing-pairs are purely structural (pick-a-side needs no
point-by-point rebuttal). Complementary-pairs add an optional combinability judge (an LLM at mint time) on top of
the structural connection_point check, because 'genuinely combines' is semantic. Stdlib only; the judge is injected."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class ComposedPair:
    family: str      # "opposing" | "complementary"
    left_id: str
    right_id: str
    source: str      # proposition_id or theme_id

def compose_opposing(prop_reg, proposition_id: str, lexile_window: int = 100,
                     len_ratio: float = 1.4) -> list[ComposedPair]:
    cands = prop_reg.opposing_candidates(proposition_id, lexile_window=lexile_window, len_ratio=len_ratio)
    return [ComposedPair("opposing", a.single_id, b.single_id, proposition_id) for a, b in cands]

def compose_complementary(theme_reg, theme_id: str, judge=None,
                          lexile_window: int = 100) -> list[ComposedPair]:
    cands = theme_reg.complementary_candidates(theme_id, lexile_window=lexile_window)
    out: list[ComposedPair] = []
    for a, b in cands:
        if judge is not None and not judge(a, b):
            continue
        out.append(ComposedPair("complementary", a.single_id, b.single_id, theme_id))
    return out
```

- [ ] **Step 4: Run to verify it passes**

Run: `python pipeline/composition.py`
Expected: `composition self-test PASS` and exit 0.

- [ ] **Step 5: Commit**

```bash
git add "Alpha HS Writing Course 2026-27/pipeline/composition.py"
git commit -m "feat(stimulus): composer + composition gate (opposing structural, complementary judge seam)"
```

---

## Task 6: Add bucket + tagging fields to StimulusRecord (backward-compatible)

**Files:**
- Modify: `pipeline/stimulus_contract.py` (the `StimulusRecord` dataclass, currently ends at line ~61 with `qc: dict = field(default_factory=dict)`)

**Interfaces:**
- Consumes: the existing `StimulusRecord`.
- Produces: `StimulusRecord` with NEW optional fields (all defaulted so existing 16 stimuli still construct):
  - `bucket: str = "lesson"` (`"lesson" | "test"`)
  - `topic_id: str = ""`
  - `proposition_id: str = ""`
  - `stance: str = ""` (`"" | "pro" | "con" | "nuanced"`)
  - `theme_id: str = ""`
  - `facet: str = ""`
  - `connection_point: str = ""`
  - `task_demand: int = 0` (1-5 when set; 0 = unset)
  - `annotated: bool = False` (lesson may annotate; test may not)
  - `form: str = ""` (which rc form this test stimulus mirrors: "staar"|"mcas"|"ohio"|"4trait")

- [ ] **Step 1: Add a self-test asserting the new fields default correctly**

Append to the `__main__` block in `stimulus_contract.py`, immediately BEFORE the final `sys.exit(...)`:

```python
    # two-bucket fields: backward-compatible defaults
    assert demo.bucket == "lesson", "default bucket is lesson"
    assert demo.topic_id == "" and demo.proposition_id == "" and demo.task_demand == 0
    assert demo.annotated is False and demo.form == ""
    _t = StimulusRecord(id="X", grade="9-10", mode="argument", family="single", prompt="p",
                        passages=[Passage("t", "w " * 500)], fact_sources=[], provenance={},
                        bucket="test", topic_id="nuclear_power", form="staar", task_demand=3)
    assert _t.bucket == "test" and _t.topic_id == "nuclear_power" and _t.form == "staar"
    print("stimulus_contract two-bucket fields OK")
```

- [ ] **Step 2: Run to verify it fails**

Run: `python pipeline/stimulus_contract.py`
Expected: FAIL (`TypeError: __init__() got an unexpected keyword argument 'bucket'`).

- [ ] **Step 3: Add the fields to the dataclass**

In `StimulusRecord`, replace the line `    qc: dict = field(default_factory=dict)` with:

```python
    # two-bucket architecture fields (all defaulted -> backward compatible with the existing 16 stimuli)
    bucket: str = "lesson"           # "lesson" | "test"
    topic_id: str = ""
    proposition_id: str = ""
    stance: str = ""                 # "" | "pro" | "con" | "nuanced"
    theme_id: str = ""
    facet: str = ""
    connection_point: str = ""
    task_demand: int = 0             # 1-5 when set; 0 = unset
    annotated: bool = False          # lesson bucket may annotate; test bucket may not
    form: str = ""                   # test bucket: which rc form this mirrors ("staar"|"mcas"|"ohio"|"4trait")
    qc: dict = field(default_factory=dict)
```

- [ ] **Step 4: Run to verify it passes**

Run: `python pipeline/stimulus_contract.py`
Expected: existing demo prints `-> PASS`, then `stimulus_contract two-bucket fields OK`, exit 0.

- [ ] **Step 5: Regression + commit**

Run: `python pipeline/bank_loader.py`
Expected: `ALL PASSED: True`, exit 0 (existing 16 stimuli unaffected).

```bash
git add "Alpha HS Writing Course 2026-27/pipeline/stimulus_contract.py"
git commit -m "feat(stimulus): add two-bucket + tagging fields to StimulusRecord (backward-compatible)"
```

---

## Task 7: Profile-switched gates (lesson vs test)

**Files:**
- Modify: `pipeline/stimulus_contract.py` (the gate functions + the `GATES` list around line 193)

**Interfaces:**
- Consumes: `StimulusRecord.bucket`, `.annotated`, `.form`, `.task_demand`; `calibration_anchors.AnchorSet`.
- Produces:
  - `gate_bucket_profile(s) -> tuple[bool, str]` (validates the bucket + its profile rules: test may not be annotated; test needs a `form`; lesson may be annotated)
  - `gate_equivalent_form(s, anchor_set=None) -> tuple[bool, str]` (test bucket only; when an `AnchorSet` is provided and has anchors for {grade, mode, form}, the stimulus's Lexile/passage_count/task_demand must sit in the band; when no anchors exist yet, returns True with a "no anchors; uncertified" note so the seed can be built before anchors are scored; lesson bucket returns True n/a)
  - Both added to the `GATES` list.

- [ ] **Step 1: Write the failing self-test**

Append to the `__main__` block in `stimulus_contract.py`, before the final `sys.exit(...)`:

```python
    # profile gate: a TEST stimulus may not be annotated and must carry a form
    _bad = StimulusRecord(id="B", grade="9-10", mode="argument", family="single", prompt="p",
                          passages=[Passage("t", "w " * 500)], fact_sources=[], provenance={},
                          bucket="test", annotated=True, form="staar")
    ok, why = gate_bucket_profile(_bad)
    assert not ok and "annotat" in why.lower(), "test bucket cannot be annotated"
    _bad2 = StimulusRecord(id="B2", grade="9-10", mode="argument", family="single", prompt="p",
                           passages=[Passage("t", "w " * 500)], fact_sources=[], provenance={},
                           bucket="test", form="")
    ok2, why2 = gate_bucket_profile(_bad2)
    assert not ok2 and "form" in why2.lower(), "test bucket needs a form"
    _lesson_annot = StimulusRecord(id="L", grade="9-10", mode="argument", family="single", prompt="p",
                                   passages=[Passage("t", "w " * 500)], fact_sources=[], provenance={},
                                   bucket="lesson", annotated=True)
    ok3, _ = gate_bucket_profile(_lesson_annot)
    assert ok3, "lesson bucket may be annotated"

    # equivalent-form gate against an anchor set
    import calibration_anchors as ca
    aset = ca.AnchorSet()
    aset.add(ca.Anchor("a1", "9-10", "argument", "staar", 1080, 1, 3))
    aset.add(ca.Anchor("a2", "9-10", "argument", "staar", 1160, 1, 4))
    _testfit = StimulusRecord(id="T", grade="9-10", mode="argument", family="single", prompt="p",
                              passages=[Passage("t", "w " * 500)], fact_sources=[], provenance={},
                              bucket="test", form="staar", task_demand=3)
    # single passage -> passage_count 1 matches anchors; lexile of "w "*500 will be low, so expect a band failure msg
    ok4, why4 = gate_equivalent_form(_testfit, anchor_set=aset)
    assert ("lexile" in why4.lower()) or ok4, "equivalent-form gate consults the anchor band"
    # no anchors for a different form -> uncertified pass (seed can be built pre-calibration)
    ok5, why5 = gate_equivalent_form(
        StimulusRecord(id="T2", grade="9-10", mode="argument", family="single", prompt="p",
                       passages=[Passage("t", "w " * 500)], fact_sources=[], provenance={},
                       bucket="test", form="ohio", task_demand=3), anchor_set=aset)
    assert ok5 and "uncertified" in why5.lower()
    # lesson bucket -> n/a pass
    ok6, _ = gate_equivalent_form(_lesson_annot, anchor_set=aset)
    assert ok6
    print("stimulus_contract profile gates OK")
```

- [ ] **Step 2: Run to verify it fails**

Run: `python pipeline/stimulus_contract.py`
Expected: FAIL (`NameError: gate_bucket_profile`).

- [ ] **Step 3: Implement the two gates + register them**

In `stimulus_contract.py`, add these two functions immediately after `gate_content` (before the `GATES = [` list):

```python
def gate_bucket_profile(s: StimulusRecord) -> tuple[bool, str]:
    """Profile rules that differ by bucket. Test: no annotation, must carry a form. Lesson: annotation allowed."""
    if s.bucket not in ("lesson", "test"):
        return False, f"bucket must be 'lesson' or 'test', got '{s.bucket}'"
    if s.bucket == "test":
        if s.annotated:
            return False, "test bucket stimulus must not be annotated (annotation can cue the answer)"
        if not s.form.strip():
            return False, "test bucket stimulus must carry a form (staar|mcas|ohio|4trait) for calibration"
    return True, f"{s.bucket} profile ok"

def gate_equivalent_form(s: StimulusRecord, anchor_set=None) -> tuple[bool, str]:
    """Test bucket only: the stimulus must sit inside the human-scored anchor band for {grade, mode, form}.
    When no anchor_set is supplied, or it has no anchors for that form yet, pass as UNCERTIFIED so the seed pool
    can be built before anchors are scored. Lesson bucket is n/a."""
    if s.bucket != "test":
        return True, "n/a (lesson bucket)"
    if anchor_set is None:
        return True, "no anchor set supplied; test form UNCERTIFIED (calibrate before go-live)"
    passage_count = len(s.passages)
    lexile = rg.analyze_text(s.passages[0].text)["lexile_estimate"] if s.passages else 0
    band = anchor_set.band(s.grade, s.mode, s.form)
    if band is None:
        return True, f"no anchors for {s.grade}/{s.mode}/{s.form}; test form UNCERTIFIED (calibrate before go-live)"
    ok, why = anchor_set.equivalent_form_ok(s.grade, s.mode, s.form, lexile, passage_count, s.task_demand or band.demand_min)
    return ok, why
```

Then in the `GATES` list, add these two entries after `("content", gate_content),`:

```python
    ("bucket_profile", gate_bucket_profile),
    ("equivalent_form", gate_equivalent_form),
```

Add the import at the top of the file (near the other imports, after `import readability_gate as rg`):

```python
import calibration_anchors as ca  # noqa: F401  (available for gate_equivalent_form callers)
```

Note: `gate_equivalent_form` takes `anchor_set` as a parameter; the `GATES` runner calls gates with just `(s)`, so it will run with `anchor_set=None` (uncertified pass) during normal QC. The anchor-checked path is exercised by callers who pass an `AnchorSet` explicitly (the mint loop). This keeps seed-building unblocked while wiring the calibration seam.

- [ ] **Step 4: Run to verify it passes**

Run: `python pipeline/stimulus_contract.py`
Expected: demo `-> PASS`, `two-bucket fields OK`, `profile gates OK`, exit 0.

- [ ] **Step 5: Regression + commit**

Run: `python pipeline/bank_loader.py`
Expected: `ALL PASSED: True` (existing 16 are bucket="lesson", not annotated, so both new gates pass).

```bash
git add "Alpha HS Writing Course 2026-27/pipeline/stimulus_contract.py"
git commit -m "feat(stimulus): profile-switched gates (bucket profile + equivalent-form calibration)"
```

---

## Task 8: Replace gate_two_sidedness with a composition-aware source-config gate

**Files:**
- Modify: `pipeline/stimulus_contract.py` (`gate_two_sidedness`, ~line 150, and its `GATES` entry)

**Interfaces:**
- Consumes: `StimulusRecord.bucket`, `.family`, `.mode`, `.passages`, `.proposition_id`, `.stance`, `.theme_id`, `.facet`, `.connection_point`.
- Produces: `gate_source_config(s) -> tuple[bool, str]` replacing `gate_two_sidedness`, with these rules:
  - A `single`-family stimulus tagged as an opposing/complementary MEMBER (has `proposition_id`+`stance`, or `theme_id`+`facet`+`connection_point`) is valid: it is a composable single. (This is how decomposed singles pass.)
  - A `single`-family stimulus with NO composition tags is valid only for `bucket="lesson"` (lesson may teach on a lone single) OR when `mode="explanatory"`/`"analysis"` (single-source is the form). A `test` + `argument` + untagged single FAILS (a pick-a-side test needs an opposing pair, so an argument test single must be a proposition member).
  - An `opposing`/`complementary` family stimulus (a pre-composed pair, e.g. legacy) keeps the old checks: 2 passages, distinct angles, >=2 orgs (opposing).

- [ ] **Step 1: Write the failing self-test**

Append to `__main__` in `stimulus_contract.py`, before the final `sys.exit(...)`:

```python
    # composable single: argument single tagged as a proposition member (pro) -> valid
    _member = StimulusRecord(id="M", grade="9-10", mode="argument", family="single", prompt="p",
                             passages=[Passage("t", "w " * 500)], fact_sources=[], provenance={},
                             bucket="test", form="staar", proposition_id="prop_x", stance="pro")
    okm, _ = gate_source_config(_member)
    assert okm, "argument single tagged to a proposition is a valid composable single"
    # untagged argument single in TEST bucket -> fail (pick-a-side test needs a pair)
    _untagged = StimulusRecord(id="U", grade="9-10", mode="argument", family="single", prompt="p",
                               passages=[Passage("t", "w " * 500)], fact_sources=[], provenance={},
                               bucket="test", form="staar")
    oku, whyu = gate_source_config(_untagged)
    assert not oku and "proposition" in whyu.lower(), "untagged argument test single must be a proposition member"
    # untagged explanatory single -> valid (single-source IS the form)
    _info = StimulusRecord(id="I", grade="9-10", mode="explanatory", family="single", prompt="p",
                           passages=[Passage("t", "w " * 500)], fact_sources=[], provenance={},
                           bucket="test", form="mcas")
    oki, _ = gate_source_config(_info)
    assert oki, "explanatory single is a valid single-source form"
    print("stimulus_contract source-config gate OK")
```

- [ ] **Step 2: Run to verify it fails**

Run: `python pipeline/stimulus_contract.py`
Expected: FAIL (`NameError: gate_source_config`).

- [ ] **Step 3: Replace the gate**

In `stimulus_contract.py`, replace the entire `gate_two_sidedness` function with:

```python
def gate_source_config(s: StimulusRecord) -> tuple[bool, str]:
    """Source-configuration validity. Replaces gate_two_sidedness for the compose-from-singles world.

    - A composable SINGLE (tagged proposition+stance, or theme+facet+connection_point) is always valid.
    - An untagged single is valid for lesson bucket, or for explanatory/analysis mode (single-source IS the form).
      An untagged single in test+argument fails (a pick-a-side test must be a composed opposing pair).
    - A pre-composed opposing/complementary pair keeps the legacy checks (2 passages, distinct angles, >=2 orgs)."""
    is_prop_member = bool(s.proposition_id and s.stance)
    is_theme_member = bool(s.theme_id and s.facet and s.connection_point)

    if s.family == "single":
        if is_prop_member or is_theme_member:
            return True, "composable single (tagged to a proposition or theme)"
        if s.bucket == "lesson" or s.mode in ("explanatory", "analysis"):
            return True, "valid single-source (lesson teaching single, or explanatory/analysis form)"
        return False, ("untagged argument single in test bucket: a pick-a-side test needs a composed opposing "
                       "pair, so this single must carry a proposition_id + stance")

    # pre-composed pair (legacy path)
    if s.family in ("complementary", "opposing"):
        if len(s.passages) != 2 or not all(p.angle.strip() for p in s.passages):
            return False, "paired set needs 2 passages each with a recorded angle"
        if s.passages[0].angle.strip().lower() == s.passages[1].angle.strip().lower():
            return False, "the two angles are identical (not genuinely two-sided)"
        if s.family == "opposing":
            orgs = {f.org for f in s.fact_sources}
            if len(orgs) < 2:
                return False, "opposing set should draw on >=2 distinct source orgs (credibility contrast)"
        return True, "pre-composed pair with distinct angles"
    return False, f"unknown family '{s.family}'"
```

Then in the `GATES` list, change the entry `("two_sidedness", gate_two_sidedness),` to:

```python
    ("source_config", gate_source_config),
```

- [ ] **Step 4: Run to verify it passes**

Run: `python pipeline/stimulus_contract.py`
Expected: demo `-> PASS` (the nuclear demo is `opposing` family, legacy path), all prior asserts, `source-config gate OK`, exit 0.

- [ ] **Step 5: Regression + commit**

Run: `python pipeline/bank_loader.py`
Expected: `ALL PASSED: True` (the 6 opposing stimuli are still `opposing` family -> legacy path; explanatory/analysis singles pass the single-source clause).

```bash
git add "Alpha HS Writing Course 2026-27/pipeline/stimulus_contract.py"
git commit -m "feat(stimulus): replace two-sidedness with compose-aware source-config gate"
```

---

## Task 9: Migrate the 6 opposing pairs into stance-tagged singles

**Files:**
- Create: `Stimulus_Bank_G10/singles/` (new dir) with 12 single files, OR add a `SINGLES: list[StimulusRecord]` export to each existing arg file. Use the second approach (keeps provenance co-located). Modify: `Stimulus_Bank_G10/arg_nuclear_power.py` and the 5 other `arg_*.py`.
- Reference existing: `Stimulus_Bank_G10/arg_nuclear_power.py` (has `PASSAGE_A`, `PASSAGE_B`, `rec`).

**Interfaces:**
- Consumes: the refactored `StimulusRecord` (Task 6-8), `proposition_registry` conventions.
- Produces: in each `arg_*.py`, a `SINGLES: list[StimulusRecord]` of the two decomposed stance singles, each `family="single"`, `bucket="test"`, tagged `proposition_id` + `stance` + `topic_id` + `form`. The legacy `rec` (opposing pair) stays for backward compatibility.

- [ ] **Step 1: Write the failing self-test (in the nuclear file first)**

Append to the `__main__` block of `Stimulus_Bank_G10/arg_nuclear_power.py`, before its final `sys.exit(...)`:

```python
    # decomposed stance singles
    assert len(SINGLES) == 2, "nuclear decomposes into 2 stance singles"
    stances = {x.stance for x in SINGLES}
    assert stances == {"pro", "con"}, "one pro, one con"
    for x in SINGLES:
        assert x.family == "single" and x.bucket == "test"
        assert x.proposition_id and x.topic_id and x.form
        qc_stimulus(x)
        assert x.qc["passed"], f"single {x.id} must pass QC: {x.qc.get('first_failure')}"
    print("nuclear SINGLES decomposition OK")
```

- [ ] **Step 2: Run to verify it fails**

Run: `python Stimulus_Bank_G10/arg_nuclear_power.py`
Expected: FAIL (`NameError: SINGLES`).

- [ ] **Step 3: Add the SINGLES export**

In `arg_nuclear_power.py`, after the existing `rec = StimulusRecord(...)` block, add (reusing the existing `PASSAGE_A`/`PASSAGE_B` and fact sources; split the fact_sources by which passage cites them):

```python
SINGLES = [
    StimulusRecord(
        id="ACC-W910-ARG-SINGLE-NUCLEAR-PRO",
        grade="9-10", mode="argument", family="single", bucket="test",
        modeling_anchor="Ohio ELA II / MD MCAP (opposing-view member)",
        acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "CCSS.W.9-10.1"],
        prompt="Read this source arguing in favor of building more nuclear power.",
        passages=[Passage(title="The Case for Building More Nuclear Power",
                          angle="pro-expansion; EIA/DOE operations and reliability data", text=PASSAGE_A)],
        fact_sources=[f for f in rec.fact_sources if f.org in ("US EIA", "US DOE")],
        provenance=dict(rec.provenance),
        topic_id="nuclear_power", proposition_id="prop_nuclear_power", stance="pro",
        form="staar", task_demand=3),
    StimulusRecord(
        id="ACC-W910-ARG-SINGLE-NUCLEAR-CON",
        grade="9-10", mode="argument", family="single", bucket="test",
        modeling_anchor="Ohio ELA II / MD MCAP (opposing-view member)",
        acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "CCSS.W.9-10.1"],
        prompt="Read this source arguing against building more nuclear power.",
        passages=[Passage(title="The Unsolved Problem of Nuclear Waste",
                          angle="anti-expansion; GAO oversight watchdog", text=PASSAGE_B)],
        fact_sources=[f for f in rec.fact_sources if f.org in ("US GAO", "US NRC")],
        provenance=dict(rec.provenance),
        topic_id="nuclear_power", proposition_id="prop_nuclear_power", stance="con",
        form="staar", task_demand=3),
]
```

- [ ] **Step 4: Run to verify it passes**

Run: `python Stimulus_Bank_G10/arg_nuclear_power.py`
Expected: legacy pair `-> PASS`, `nuclear SINGLES decomposition OK`, exit 0.
(If a single fails `citable_facts` because <3 facts landed in its half, move enough fact_sources rows to that stance's list; each single needs >=3 own-authored citable facts per `gate_citable_facts`.)

- [ ] **Step 5: Repeat Steps 1-4 for the other 5 arg files, then commit**

Apply the same pattern to `arg_ev_mandates.py`, `arg_minimum_wage.py`, `arg_school_start.py`, `arg_social_media_age.py`, `arg_space_spending.py` (proposition_id = `prop_<topic>`, stances pro/con, topic_id = the topic slug, form per each file's modeling anchor). Each must print its `SINGLES decomposition OK` and exit 0.

```bash
git add "Alpha HS Writing Course 2026-27/Stimulus_Bank_G10/arg_"*.py
git commit -m "feat(stimulus): decompose 6 opposing pairs into 12 stance-tagged test singles"
```

---

## Task 10: Loader loads singles + a two-bucket summary; final regression

**Files:**
- Modify: `pipeline/bank_loader.py` (the stimulus load loop + `BankIR.summary`)

**Interfaces:**
- Consumes: each stimulus file's `rec` and (new) optional `SINGLES` list.
- Produces:
  - `BankIR.singles: list` (new field) holding all `SINGLES` across files.
  - `BankIR.summary()` gains `"singles"`, `"lesson_stimuli"`, `"test_stimuli"` counts (bucket split over `stimuli + singles`).

- [ ] **Step 1: Write the failing self-test**

Add to the `__main__` block of `bank_loader.py`, before the final `sys.exit(...)`:

```python
    s = ir.summary()
    assert s["singles"] >= 12, f"expected >=12 decomposed singles, got {s['singles']}"
    assert s["test_stimuli"] >= 12, "the 12 stance singles are test-bucket"
    assert s["lesson_stimuli"] >= 1, "legacy explanatory/analysis stimuli are lesson-ish"
    print(f"two-bucket summary: {s['lesson_stimuli']} lesson / {s['test_stimuli']} test / {s['singles']} singles")
```

- [ ] **Step 2: Run to verify it fails**

Run: `python pipeline/bank_loader.py`
Expected: FAIL (`KeyError: 'singles'`).

- [ ] **Step 3: Implement**

In `bank_loader.py`: add `singles: list = field(default_factory=list)` to the `BankIR` dataclass. In the stimulus load loop (where `rec` is appended), after appending `rec`, also load its singles:

```python
            for sng in getattr(mod, "SINGLES", []):
                if run_qc:
                    qc_stimulus(sng)
                ir.singles.append(sng)
                ir.stimulus_by_id[sng.id] = sng
```

In `BankIR.summary`, add to the returned dict:

```python
            "singles": len(self.singles),
            "lesson_stimuli": sum(1 for x in (self.stimuli + self.singles) if getattr(x, "bucket", "lesson") == "lesson"),
            "test_stimuli": sum(1 for x in (self.stimuli + self.singles) if getattr(x, "bucket", "lesson") == "test"),
```

Also include singles in `all_passed()`: change the `objs` line to
`objs = self.stimuli + self.singles + self.items + self.lessons`.

- [ ] **Step 4: Run to verify it passes**

Run: `python pipeline/bank_loader.py`
Expected: `ALL PASSED: True` and `two-bucket summary: N lesson / >=12 test / >=12 singles`, exit 0.

- [ ] **Step 5: Full-pipeline regression + commit**

Run each and confirm exit 0 / expected output:
```bash
python pipeline/topic_registry.py
python pipeline/proposition_registry.py
python pipeline/theme_registry.py
python pipeline/calibration_anchors.py
python pipeline/composition.py
python pipeline/stimulus_contract.py
python pipeline/bank_loader.py
python pipeline/push_targets.py both
```
Expected: all exit 0; `push_targets.py both` still prints the dependency check OK (the push layer is unaffected by the stimulus refactor).

```bash
git add "Alpha HS Writing Course 2026-27/pipeline/bank_loader.py"
git commit -m "feat(stimulus): loader loads decomposed singles + two-bucket summary"
```

---

## Deferred to a later plan (explicitly NOT in this plan)
- The on-demand `mint_loop` wired to Platform3 Events (needs the push layer live + creds).
- The LLM combinability judge implementation (the `judge` seam exists in `composition.py`; the actual LLM call is deferred with the grader / mint loop).
- Human scoring of the real anchor sets (the machinery is built; a human populates `calibration_anchors` from `AnchorSets/` before go-live).
- Seeding the full ~120-150 lesson / ~80-100 test single floor per grade (this plan proves the machine on the existing 16 -> 12 singles; the bulk seed is a generation run, same pattern as the original stimulus fan-out).
- The lesson/item contract check that a test item never binds a lesson-only topic (small follow-up once topics are assigned on real content).
- **Facet-distance rule** (spec risk-solution #1, layer 2): the theme registry currently gates on DISTINCT facet + shared connection_point; the finer "distance" score (complementary-but-not-redundant, not-disjoint) is deferred until we have enough themes to calibrate distances against. The distinct-facet check is the floor; distance is a refinement.
- **Cross-grade topic isolation** (spec risk-solution #3, item 4): the topic registry is grade-scoped in this plan; namespacing topic-use by student-cohort TRAJECTORY across grades is deferred to when G11/G12 exist (no cross-grade data until then).
