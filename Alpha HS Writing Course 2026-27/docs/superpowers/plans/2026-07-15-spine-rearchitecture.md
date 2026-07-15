# Lesson-Spine Re-Architecture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the uniform 10-11 slot arc used by all 156 G9-12 lessons with a grain-differentiated spine and scaffold-free gate lessons, per the Council + Fable-5 verdict (SPINE_DELIBERATION_verdict.md), while keeping all lessons green on the existing QC + render harness and pushing nothing to Timeback without approval.

**Architecture:** The lesson data model (`pipeline/lesson_contract.py`), the gated-reading renderer (`pipeline/gated_reading.py`), and the preview renderers stay. We (1) teach the contract a lesson CLASS (practice vs gate) and a GRAIN (derived from the terminal production unit), (2) make the three arc-enforcing gates class-aware so a scaffold-free gate and a transfer-free essay are valid, (3) add a grain-spine crosscheck that becomes the test for authoring, (4) rewrite lessons grain by grain (gates first), and (5) fix the issue-frame source formatting. All changes live inside the existing gated-reading + QTI contract confirmed compliant in SPINE_REARCH_platform_compliance.md.

**Tech Stack:** Python 3 (stdlib only for contract/crosscheck; the lessons import `lesson_contract` + `lesson_prompts`); the render/preview layer is stdlib + the live LearnWith player. No new dependencies.

## Global Constraints

- NO em dashes anywhere in student-facing lesson content or authored prompts (use commas, colons, parentheses). Enforced by `gate_no_em_dash`.
- Lesson IDs are STABLE (grader + mastery keyed by id). Every rewrite is IN PLACE; never change `L.id`.
- Every lesson must pass all lesson_contract gates (currently 23; this plan adds `gate_gate_shape`, so 24) with exit 0, AND `gated_reading.render_qc` with exit 0, AND the new `grain_spine_crosscheck` with exit 0. Verify by EXIT CODE, never by self-report.
- Content provenance rule holds: facts + teaching moves trace to the bound source; no fabricated figures (lesson-content-provenance-rule).
- Nothing is pushed to Timeback. The deliverable is updated source files + a re-rendered Vercel review preview. The live push is a separate approval-gated step.
- Grain is derived from data, not title: `grain(L)` = the highest `UNIT_RANK` among the lesson's scored `production_frq` slots (sentence < paragraph < multi_paragraph < essay). A lesson with `lesson_class == "gate"` uses the GATE template regardless of grain.
- The verdict's priority order is binding: P1 (gates) first, then P2b (boxed source), P3 (drop essay transfer), P4 (grain density), P5 (own-draft diagnosis), P6 (planning). Smallest-highest-value first.

---

## File Structure

**Modified (infrastructure, Phase A):**
- `pipeline/lesson_contract.py` - add `Lesson.lesson_class` field + `grain(L)` helper + `GRAIN_TEMPLATES` spec; make `gate_shell_completeness`, `gate_model_sequence`, `gate_discrimination_before_production` class-aware; add `gate_gate_shape`.
- `pipeline/gated_reading.py` - add boxed (capped-scrollable) source mode to `frq_xml`; add an essay/gate boxed-source assertion to `render_qc`.

**Created (infrastructure, Phase A):**
- `pipeline/grain_spine_crosscheck.py` - validates every lesson's slot shape against its grain/class template; self-tested, HTML-viewable, exit-coded (mirrors `scaffold_crosscheck.py`).
- `pipeline/tests/test_contract_classes.py` - unit tests for the contract changes.
- `pipeline/tests/test_frq_boxed.py` - unit tests for the boxed-source renderer.

**Modified (authoring, Phase B):** lesson files under `Lesson_Bank_G9/`, `Lesson_Bank_G10/`, `Lesson_Bank_G11/`, `Lesson_Bank_G12/`, grain by grain. Each rewrite is in place.

**Modified (formatting, Phase C):**
- 11 issue-frame stimuli under `Stimulus_Bank_G9..G12/` (the `Here is the question for your claim:` lead-in).
- `pipeline/gated_reading.py` (`frq_xml` / `_content_card` source block), `pipeline/mastery_targets_grade.py`, `pipeline/g9_push_mastery_v3_1.py` - the 3 source-block render sites: bold label + italic question + line break.

**Untouched:** `course_sequence_g9_12.py` (source of truth stays), the mastery prompt banks (`mastery_prompts_g*.py`) except where a rewrite changes a lesson's terminal write, the push adapters.

---

## Task 1: Teach the contract lesson-class + grain, make arc-gates class-aware

**Files:**
- Modify: `pipeline/lesson_contract.py`
- Test: `pipeline/tests/test_contract_classes.py`

**Interfaces:**
- Produces: `Lesson.lesson_class: str = "practice"` (values `"practice"` | `"gate"`); `grain(L: Lesson) -> str` returning one of `UNIT_LADDER`; `GRAIN_TEMPLATES: dict[str, dict]` (grain/class -> required slot shape); `gate_gate_shape(L) -> tuple[bool,str]`.
- Consumes: existing `Slot`, `Lesson`, `SHELL_ORDER`, `UNIT_RANK`, `GATES`.

**Scope note (contract changes belong HERE, not in later tasks):** ALL contract-gate edits the re-architecture needs are made in this task, so the contract is complete and stable before any lesson is rewritten. That means five gates become class/grain-aware in this task: `gate_shell_completeness`, `gate_model_sequence`, `gate_discrimination_before_production` (all -> gate-aware), `gate_bank_partition` (-> returns pass for essay-grain practice lessons, since their transfer is routed to the gate/PP100), and `gate_model_sequence` again (-> diagnosis_frq required only at paragraph grain and above, since sentence-grain lessons fold diagnosis into predict_the_fix). The later authoring tasks (5-7) rely on these but do NOT edit the contract.

- [ ] **Step 1: Write the failing tests**

```python
# pipeline/tests/test_contract_classes.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lesson_contract import Lesson, Slot, grain, qc_lesson

def _slot(role, kind, unit="", bank="", **kw):
    return Slot(role=role, kind=kind, title=kind, unit=unit, bank=bank,
                scored=(kind in ("production_frq", "diagnosis_frq")), **kw)

def _practice_essay():
    # the CANONICAL post-rearchitecture essay shape: ONE full write + self-revision, NO in-article transfer.
    return Lesson(id="X-PRACTICE", grade="9-10", lesson_type=7, unit="U", title="T", target="t",
        lesson_class="practice",
        slots=[
            _slot("TEACH","teach_card"),
            _slot("MODEL","stimulus_display", bank="a"),
            _slot("MODEL","annotated_before_after", bank="a"),
            _slot("MODEL","discrimination", bank="a", labeled_grade_c=True),
            _slot("MODEL","predict_the_fix", bank="a", feedback="reveal"),
            _slot("SUPPORTED","production_frq", unit="multi_paragraph", bank="a", rubric_ref="rc.staar"),  # outline
            _slot("INDEPENDENT","production_frq", unit="essay", bank="a", rubric_ref="rc.staar"),          # one write
            _slot("INDEPENDENT","diagnosis_frq", unit="essay", bank="a", rubric_ref="rc.staar"),           # self-revision (own draft = INDEPENDENT-stage, not MODEL)
            _slot("INDEPENDENT","self_score"),
        ])

def _practice_sentence():
    # sentence grain: dense discrimination, 3 short writes, near-variation transfer, NO diagnosis required.
    return Lesson(id="X-SENT", grade="9-10", lesson_type=2, unit="U", title="T", target="t",
        lesson_class="practice",
        slots=[
            _slot("TEACH","teach_card"),
            _slot("MODEL","stimulus_display", bank="a"),
            _slot("MODEL","annotated_before_after", bank="a"),
            _slot("MODEL","discrimination", bank="a", labeled_grade_c=True),
            _slot("MODEL","discrimination", bank="a", labeled_grade_c=True),
            _slot("MODEL","predict_the_fix", bank="a", feedback="reveal"),
            _slot("SUPPORTED","production_frq", unit="sentence", bank="a", rubric_ref="rc.staar"),
            _slot("INDEPENDENT","production_frq", unit="sentence", bank="a", rubric_ref="rc.staar"),
            _slot("TRANSFER","production_frq", unit="sentence", bank="a-var", rubric_ref="rc.staar"),
            _slot("INDEPENDENT","self_score"),
        ])

def _gate():
    # scaffold-free: bare TEACH cue, UNSCORED plan affordance, held-out cold write, post-hoc self_score.
    # NO model/discrimination/predict. The plan slot is scored=False (a pure affordance, not a certification write).
    plan = Slot(role="SUPPORTED", kind="production_frq", title="plan", unit="essay", bank="held",
                rubric_ref="rc.ap", scored=False)
    return Lesson(id="X-GATE", grade="9-10", lesson_type=8, unit="U", title="Gate", target="t",
        lesson_class="gate",
        slots=[
            _slot("TEACH","teach_card"),
            plan,                                                                              # unscored plan
            _slot("TRANSFER","production_frq", unit="essay", bank="held", rubric_ref="rc.ap"), # cold scored write
            _slot("INDEPENDENT","self_score"),                                                 # post-hoc calibration
        ])

def test_grain_from_terminal_unit():
    assert grain(_practice_essay()) == "essay"
    assert grain(_practice_sentence()) == "sentence"

def test_practice_essay_passes_without_transfer():
    # essay grain: no in-article TRANSFER write, bank_partition must not fail it
    r = qc_lesson(_practice_essay())
    assert r["passed"], (r["first_failure"], {k: v for k, v in r["gates"].items() if not v["passed"]})

def test_practice_sentence_passes_without_diagnosis():
    # sentence grain: no diagnosis_frq required; model_sequence must not fail it
    r = qc_lesson(_practice_sentence())
    assert r["passed"], (r["first_failure"], {k: v for k, v in r["gates"].items() if not v["passed"]})

def test_gate_passes_when_scaffold_free():
    r = qc_lesson(_gate())
    assert r["passed"], (r["first_failure"], {k: v for k, v in r["gates"].items() if not v["passed"]})

def test_gate_rejects_smuggled_scaffold():
    g = _gate()
    g.slots.insert(1, _slot("MODEL","annotated_before_after", bank="held"))
    r = qc_lesson(g)
    assert not r["passed"]
    assert r["first_failure"] == "gate_gate_shape"
```

- [ ] **Step 2: Run to verify they fail**

Run: `cd "Alpha HS Writing Course 2026-27" && python -m pytest pipeline/tests/test_contract_classes.py -q`
Expected: FAIL (Lesson has no `lesson_class`; `grain` undefined).

- [ ] **Step 3: Add the field, grain helper, and template spec**

In `pipeline/lesson_contract.py`, add `lesson_class: str = "practice"` to the `Lesson` dataclass (after `qc`). Add near `UNIT_LADDER`:

```python
def grain(L) -> str:
    """The lesson's grain = the highest unit-ladder rank among its scored production_frq slots.
    Falls back to 'sentence' if no scored production exists."""
    units = [s.unit for s in L.slots if s.kind == "production_frq" and getattr(s, "unit", "")]
    if not units:
        return "sentence"
    return max(units, key=lambda u: UNIT_RANK.get(u, 0))

# Required slot shape per (class, grain). "min"/"max" bound the COUNT of a kind; roles list what must exist.
# Gate is class-level (grain-independent). See SPINE_DELIBERATION_verdict.md.
GRAIN_TEMPLATES = {
    "gate": {
        "banned_kinds": {"annotated_before_after", "discrimination", "predict_the_fix"},
        "require_kinds": {"production_frq"},   # a cold write
        "max_scored_writes": 1,                 # ONLY the cold write is scored; the plan is a scored=False affordance
    },
    # paragraph and above accept EITHER an own-draft diagnosis (default) OR exactly one coached TRANSFER write
    # (transfer-flagged lessons), never both. Encoded as "revision_or_coached_transfer": True.
    ("practice", "sentence"): {"discrimination_min": 2, "production_writes": (2, 3)},
    ("practice", "paragraph"): {"discrimination_min": 1, "production_writes": (2, 3), "revision_or_coached_transfer": True},
    ("practice", "multi_paragraph"): {"discrimination_min": 1, "production_writes": (1, 3), "revision_or_coached_transfer": True},
    ("practice", "essay"): {"discrimination_max": 1, "production_writes": (1, 1), "revision_or_coached_transfer": True,
                             "no_transfer_write": True},
}
# multi_paragraph is treated as PARAGRAPH-family (verdict language: "paragraph grain and above"); its lessons
# are authored in Task 6 alongside paragraph grain. It is a documented interpolation, not a verdict grain.
```

Note on "no_transfer_write" vs "revision_or_coached_transfer" at essay grain: essay grain forbids an in-article TRANSFER write (transfer -> gate/PP100) AND requires the own-draft revision (a diagnosis_frq). So at essay grain the "revision_or_coached_transfer" resolves to the revision branch only (the coached-transfer branch is unavailable because no_transfer_write is set). At paragraph/multi_paragraph grain both branches are allowed.

- [ ] **Step 4: Make the three arc-gates class-aware + add gate_gate_shape**

Edit `gate_shell_completeness`: at the top, if `L.lesson_class == "gate"`, require only `{"TEACH", "TRANSFER"}` present (a gate is the Independent-Performance endpoint: a cue + a cold write), and return early:

```python
def gate_shell_completeness(L) -> tuple[bool, str]:
    roles = [s.role for s in L.slots]
    if getattr(L, "lesson_class", "practice") == "gate":
        need = {"TEACH", "TRANSFER"}
        missing = need - set(roles)
        if missing:
            return False, f"gate missing {missing} (needs a cue + a cold TRANSFER write)"
        return True, "gate shell (cue + cold write) present"
    for r in SHELL_ORDER:
        if r not in roles:
            return False, f"SRSD shell incomplete: missing '{r}' stage"
    firsts = [roles.index(r) for r in SHELL_ORDER]
    if firsts != sorted(firsts):
        return False, f"shell stages out of order: {[(r, roles.index(r)) for r in SHELL_ORDER]}"
    return True, "SRSD shell complete + in order (Teach->Model->Supported->Independent->Transfer)"
```

Edit `gate_model_sequence`: first line `if getattr(L, "lesson_class", "practice") == "gate": return True, "gate: model sequence not required (scaffold-free by design)"`.

Edit `gate_discrimination_before_production`: first line `if getattr(L, "lesson_class", "practice") == "gate": return True, "gate: discrimination intentionally absent (scaffold-free)"`.

Edit `gate_bank_partition` (needed by Task 5, made here): after the `taught`/`transfer` computation, allow essay-grain practice lessons to have NO transfer write (their transfer is routed to the gate + PP100). Replace the `if not transfer: return False, "no TRANSFER slot"` with:

```python
    if not transfer:
        if getattr(L, "lesson_class", "practice") == "practice" and grain(L) == "essay":
            return True, "essay grain: in-article transfer routed to gate/PP100 (no TRANSFER slot expected)"
        return False, "no TRANSFER slot"
```

Edit `gate_model_sequence` (needed by Tasks 6+7, made here): the diagnosis_frq requirement applies only at paragraph grain and above, AND accepts the coached-transfer alternative (a transfer-flagged paragraph lesson may carry one coached TRANSFER write instead of the own-draft revision). Change the diagnosis check to:

```python
    rank = UNIT_RANK.get(grain(L), 0)
    needs_revision = getattr(L, "lesson_class", "practice") == "practice" and rank >= UNIT_RANK["paragraph"]
    has_diag = any(s.kind == "diagnosis_frq" for s in L.slots)
    has_coached_transfer = any(s.kind == "production_frq" and s.role == "TRANSFER" and s.feedback.strip()
                               for s in L.slots)
    if needs_revision and not (has_diag or has_coached_transfer):
        return False, ("paragraph grain or above needs EITHER an own-draft diagnosis_frq OR one coached "
                       "(feedback-bearing) TRANSFER write")
```

(At sentence grain the diagnosis mechanism folds into predict_the_fix, so neither is required. At essay grain `no_transfer_write` is set, so the coached-transfer branch is unavailable and a diagnosis_frq is required.)

Add the new gate and register it in `GATES` (append after `no_em_dash`):

```python
def gate_gate_shape(L) -> tuple[bool, str]:
    """A gate lesson must be scaffold-free: no annotated_before_after / discrimination / predict_the_fix,
    a cold TRANSFER production write on a held-out bank, and at most a brief plan before it."""
    if getattr(L, "lesson_class", "practice") != "gate":
        return True, "not a gate"
    spec = GRAIN_TEMPLATES["gate"]
    banned = spec["banned_kinds"] & {s.kind for s in L.slots}
    if banned:
        return False, f"gate contains banned teaching scaffold(s): {sorted(banned)}"
    scored_writes = [s for s in L.slots if s.kind == "production_frq" and getattr(s, "scored", False)]
    if not scored_writes:
        return False, "gate has no scored (cold) production write"
    if len(scored_writes) > spec["max_scored_writes"]:
        return False, (f"gate has {len(scored_writes)} scored writes (max {spec['max_scored_writes']}: only the "
                       f"cold write is scored; the plan must be scored=False)")
    if not any(s.role == "TRANSFER" for s in scored_writes):
        return False, "gate has no TRANSFER (cold, held-out) scored write"
    return True, "gate is scaffold-free (cue + unscored plan + one scored cold write)"
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python -m pytest pipeline/tests/test_contract_classes.py -q`
Expected: PASS (4 passed).

- [ ] **Step 6: Regression - the current 156 lessons must still all pass (they are class='practice' by default)**

Run: `python pipeline/run_all_lesson_qc.py` if it exists, else:
`for f in Lesson_Bank_G*/lesson_*.py; do python "$f" >/dev/null 2>&1 || echo "FAIL $f"; done; echo done`
Expected: no `FAIL` lines (default `lesson_class="practice"` preserves today's behavior; the current gate lessons are still practice-class here and unchanged, so they still pass the old way).

- [ ] **Step 7: Commit**

```bash
git add pipeline/lesson_contract.py pipeline/tests/test_contract_classes.py
git commit -m "feat(contract): lesson_class + grain + class-aware arc gates (gate = scaffold-free)"
```

---

## Task 2: Boxed (capped-scrollable) source mode in frq_xml + render_qc assertion

**Files:**
- Modify: `pipeline/gated_reading.py` (`frq_xml`, `render_qc`)
- Test: `pipeline/tests/test_frq_boxed.py`

**Interfaces:**
- Consumes: `frq_xml(fr_id, slot, source_text, source_reminder)` (existing).
- Produces: `frq_xml(..., boxed_source=False)` new kwarg; when `True`, the inlined source renders in a `max-height:230px; overflow:auto` wrapper. `render_qc` gains a check that essay/gate writing prompts carrying a full source use the boxed wrapper.

Rationale: SPINE_REARCH_renderQA_result.md - a naive full re-inline pushes the text box 395-587px below the fold; the capped scrollable panel keeps the box top on screen at all tested viewports.

- [ ] **Step 1: Write the failing test**

```python
# pipeline/tests/test_frq_boxed.py
import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lesson_contract import Slot
from gated_reading import frq_xml

SRC = ["A Title", "Para one is long. " * 30, "Para two is also long. " * 30]

def test_boxed_source_wraps_in_capped_scroller():
    s = Slot(role="TRANSFER", kind="production_frq", title="Write", body="Write the essay.",
             unit="essay", rubric_ref="rc.ap", scored=True)
    xml = frq_xml("frq-x", s, source_text=SRC, boxed_source=True)
    prompt = re.search(r"<qti-prompt>(.*)</qti-prompt>", xml, re.S).group(1)
    assert "overflow:auto" in prompt and "max-height:" in prompt, "boxed source must be a capped scroller"

def test_default_source_unchanged():
    s = Slot(role="SUPPORTED", kind="production_frq", title="Write", body="Write.", unit="sentence",
             rubric_ref="rc.staar", scored=True)
    xml = frq_xml("frq-y", s, source_text=SRC)  # boxed_source defaults False
    prompt = re.search(r"<qti-prompt>(.*)</qti-prompt>", xml, re.S).group(1)
    assert "overflow:auto" not in prompt, "short-grain source must not be boxed"
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest pipeline/tests/test_frq_boxed.py -q`
Expected: FAIL (`frq_xml` has no `boxed_source` kwarg / no overflow wrapper).

- [ ] **Step 3: Implement boxed mode**

In `frq_xml`, change the signature to `def frq_xml(fr_id, slot, source_text="", source_reminder="", boxed_source=False):`. In the `if source_text:` branch, when `boxed_source` is true, wrap the assembled `body_html` in the capped scroller and use a "Source (scroll within this box)" label instead of the plain block:

```python
    if source_text:
        blocks = source_text if isinstance(source_text, list) else [source_text]
        body_html = ""
        for k, b in enumerate(blocks):
            if k == 0 and len(blocks) > 1:
                body_html += f'<div style="font-weight:700;margin:0 0 4px;">{esc(b)}</div>'
            else:
                body_html += f'<p style="margin:0 0 8px;">{esc(b)}</p>'
        if boxed_source:
            prompt_html += (
                '<div style="font-size:12px;font-weight:700;letter-spacing:.04em;color:#0f766e;'
                'text-transform:uppercase;margin-bottom:4px;">Source (scroll within this box)</div>'
                '<div style="max-height:230px;overflow:auto;border:1px solid #99f6e4;background:#f8fafc;'
                f'border-radius:8px;padding:10px 14px;color:#1f2a44;line-height:1.6;">{body_html}</div>')
        else:
            prompt_html += (f'<div class="tb-source" style="border-left:4px solid #0d9488;background:#f8fafc;'
                            f'border-radius:8px;padding:10px 14px;margin:0 0 12px;">'
                            f'<div style="font-size:12px;font-weight:700;letter-spacing:.04em;color:#0f766e;'
                            f'text-transform:uppercase;margin-bottom:4px;">Source</div>'
                            f'<div style="color:#1f2a44;line-height:1.6;">{body_html}</div></div>')
    elif source_reminder:
        ...  # unchanged
```

Then, in `build_lesson_html`, box the source for writes at `multi_paragraph`+ unit OR any gate lesson. Where it calls `frq_xml(fr_id, s, source_text=src_arg, source_reminder=reminder)`, compute:

```python
        boxed = (getattr(L, "lesson_class", "practice") == "gate"
                 or getattr(s, "unit", "") in ("multi_paragraph", "essay"))
```

and pass `boxed_source=boxed`. EXPLICIT RULE (state it in a comment): boxing is keyed on the WRITE slot's unit being multi_paragraph or essay, OR the lesson being a gate. This intentionally boxes the essay template's SUPPORTED outline slot (unit="multi_paragraph") too, which is desirable (planning benefits from the full source visible). Also, for boxed writes, force full-source re-inline (do not degrade to the one-line reminder): when `boxed` and `cur_source`, set `src_arg, reminder = cur_source, ""` even if the source was already inlined earlier. Add a test in `test_frq_boxed.py` for the multi_paragraph outline-slot case so this behavior is intentional, not incidental.

- [ ] **Step 4: Add the render_qc assertion**

The check must target the SOURCE-BLOCK size, not the whole prompt, so legitimate long paragraph-grain prompts (P2a, deliberately un-boxed) are not false-flagged. Detect a `tb-source`-style block, measure ITS words, and require the boxed wrapper only when that block is large:

```python
        # 6. a LARGE inlined source block must be in a capped scroller (overflow:auto), not stacked full-height,
        #    or it pushes the write box below the fold (see SPINE_REARCH_renderQA_result.md).
        for srcblock in re.findall(r'class="tb-source"[^>]*>(.*?)</div>\s*</div>', p, re.S):
            words = len(re.findall(r"[A-Za-z]+", re.sub(r"<[^>]+>", " ", srcblock)))
            if words > SOURCE_BOX_WORD_MAX and "overflow:auto" not in p:
                problems.append(f"{pid}: {words}-word inlined source not in a capped scroller "
                                f"(use boxed_source; box pushed below fold)")
```

BASELINE-FIRST (Step 4a, before enabling as a failure): add `SOURCE_BOX_WORD_MAX` as a module constant and run the check in REPORT-ONLY mode over all 156 current lessons to find the largest legitimately un-boxed source block; set `SOURCE_BOX_WORD_MAX` just above that (the render-QA showed 741 words fails; short first-use sources are well under). Document the chosen number in a comment. Only then treat it as a hard failure. This prevents the Task 2 Step 6 and Task 6 regressions Fable flagged.

- [ ] **Step 5: Run tests to verify pass**

Run: `python -m pytest pipeline/tests/test_frq_boxed.py -q`
Expected: PASS (2 passed).

- [ ] **Step 6: Regression - render every current lesson, expect no new render-QC failures**

Run: `for f in Lesson_Bank_G*/lesson_*.py; do python pipeline/gated_reading.py "$f" >/dev/null 2>&1 || echo "RENDERFAIL $f"; done; echo done`
Expected: no `RENDERFAIL` lines. (Current lessons keep short sources or already-inlined blocks under 250 words; the new check only bites the naive-full-reinline case this task prevents.)

- [ ] **Step 7: Commit**

```bash
git add pipeline/gated_reading.py pipeline/tests/test_frq_boxed.py
git commit -m "feat(render): boxed capped-scroll source for essay/gate writes (P2b) + render_qc guard"
```

---

## Task 3: grain_spine_crosscheck.py (the authoring test)

**Files:**
- Create: `pipeline/grain_spine_crosscheck.py`

**Interfaces:**
- Consumes: `lesson_contract.grain`, `GRAIN_TEMPLATES`, `Lesson`; the four `Lesson_Bank_G*` dirs.
- Produces: CLI `python pipeline/grain_spine_crosscheck.py [--grade G10] [--html out.html]`; exit 0 iff every checked lesson matches its grain/class template; a `check_lesson(L) -> list[str]` function (empty = conforms).

- [ ] **Step 1: Write the failing test (a conformance function with a known-good and known-bad lesson)**

Add to `pipeline/tests/test_contract_classes.py`:

```python
def test_grain_crosscheck_flags_essay_with_transfer():
    from grain_spine_crosscheck import check_lesson
    L = _practice_essay()  # has a TRANSFER write -> essay template forbids it
    probs = check_lesson(L)
    assert any("transfer" in p.lower() for p in probs), probs

def test_grain_crosscheck_passes_clean_gate():
    from grain_spine_crosscheck import check_lesson
    assert check_lesson(_gate()) == []
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m pytest pipeline/tests/test_contract_classes.py -q -k grain_crosscheck`
Expected: FAIL (module does not exist).

- [ ] **Step 3: Implement the crosscheck** (mirror the structure/CLI/exit-code discipline of `pipeline/scaffold_crosscheck.py`)

```python
# pipeline/grain_spine_crosscheck.py
"""Validate each lesson's slot shape against its (class, grain) template from GRAIN_TEMPLATES.
Runs as the authoring test for the spine re-architecture. Self-tested, HTML-viewable, exit-coded."""
from __future__ import annotations
import sys, os, glob, re, argparse
HERE = os.path.dirname(__file__); ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
from lesson_contract import grain, GRAIN_TEMPLATES
from g9_push_dryrun import _load

def check_lesson(L) -> list:
    """Mirror the contract's grain/class rules so the punch-list tool is never weaker than QC."""
    from lesson_contract import UNIT_RANK
    probs = []
    cls = getattr(L, "lesson_class", "practice")
    kinds = [s.kind for s in L.slots]
    writes = [s for s in L.slots if s.kind == "production_frq"]
    scored_writes = [s for s in writes if getattr(s, "scored", False)]
    if cls == "gate":
        spec = GRAIN_TEMPLATES["gate"]
        bad = spec["banned_kinds"] & set(kinds)
        if bad: probs.append(f"gate has banned scaffold {sorted(bad)}")
        if len(scored_writes) > spec["max_scored_writes"]:
            probs.append(f"gate has {len(scored_writes)} scored writes > {spec['max_scored_writes']}")
        if not any(s.role == "TRANSFER" for s in scored_writes):
            probs.append("gate has no TRANSFER (cold, held-out) scored write")  # mirror gate_gate_shape fully
        return probs
    g = grain(L); spec = GRAIN_TEMPLATES.get((cls, g))
    if not spec:
        return probs  # grains without a template are unconstrained here
    dcount = sum(1 for k in kinds if k == "discrimination")
    if "discrimination_min" in spec and dcount < spec["discrimination_min"]:
        probs.append(f"{g}: {dcount} discrimination slots < min {spec['discrimination_min']}")
    if "discrimination_max" in spec and dcount > spec["discrimination_max"]:
        probs.append(f"{g}: {dcount} discrimination slots > max {spec['discrimination_max']}")
    lo, hi = spec.get("production_writes", (0, 99))
    if not (lo <= len(writes) <= hi):
        probs.append(f"{g}: {len(writes)} production writes outside [{lo},{hi}]")
    if spec.get("no_transfer_write") and any(s.role == "TRANSFER" for s in writes):
        probs.append(f"{g}: has an in-article TRANSFER write (verdict: route transfer to gate/PP100)")
    # paragraph grade and above: EITHER an own-draft diagnosis OR one coached (feedback-bearing) TRANSFER write
    if spec.get("revision_or_coached_transfer") and UNIT_RANK.get(g, 0) >= UNIT_RANK["paragraph"]:
        has_diag = any(s.kind == "diagnosis_frq" for s in L.slots)
        has_coached_transfer = any(s.role == "TRANSFER" and s.kind == "production_frq" and s.feedback.strip()
                                   for s in L.slots)
        if not (has_diag or has_coached_transfer):
            probs.append(f"{g}: needs EITHER an own-draft diagnosis_frq OR one coached TRANSFER write")
    return probs

def _iter(grade=None):
    grades = [grade] if grade else ["G9", "G10", "G11", "G12"]
    for gd in grades:
        for f in sorted(glob.glob(os.path.join(ROOT, f"Lesson_Bank_{gd}", "lesson_*.py"))):
            if "_deprecated" in f: continue
            try: m = _load(f); L = getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0]
            except Exception: L = None
            if L: yield f, L

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--grade"); ap.add_argument("--html")
    a = ap.parse_args(); bad = 0; rows = []
    for f, L in _iter(a.grade):
        probs = check_lesson(L)
        rows.append((L.id, getattr(L, "lesson_class", "practice"), grain(L), probs))
        if probs: bad += 1; print(f"FAIL {L.id} [{getattr(L,'lesson_class','practice')}/{grain(L)}]: {probs}")
    print(f"\ngrain-spine crosscheck: {len(rows)-bad}/{len(rows)} conform")
    if a.html:
        open(a.html, "w", encoding="utf-8").write("<h1>Grain-spine crosscheck</h1><ul>" +
            "".join(f"<li>{i} [{c}/{g}] {'OK' if not p else p}</li>" for i,c,g,p in rows) + "</ul>")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify pass**

Run: `python -m pytest pipeline/tests/test_contract_classes.py -q -k grain_crosscheck`
Expected: PASS.

- [ ] **Step 5: Baseline the current course (expected to FAIL loudly - that is the work list)**

Run: `python pipeline/grain_spine_crosscheck.py`
Expected: many `FAIL` lines (current lessons are the uniform arc). CAPTURE this output to `docs/superpowers/plans/_grain_baseline.txt` - it is the per-lesson punch list Phase B works through.

- [ ] **Step 6: Commit**

```bash
git add pipeline/grain_spine_crosscheck.py pipeline/tests/test_contract_classes.py
git commit -m "feat(crosscheck): grain-spine conformance check (authoring test for re-architecture)"
```

---

## Task 4: P1 - rewrite the gate lessons to scaffold-free (highest value, smallest)

**Files:**
- Modify (the gate lessons; verify the live set first, see Step 1):
  - `Lesson_Bank_G9/lesson_g9_l26_gate_essay_v3_1.py`, `Lesson_Bank_G9/lesson_g9_l27_gate_argument_essay_v3_1.py`
  - `Lesson_Bank_G10/lesson_g10_l24_gate_cross_text.py`
  - `Lesson_Bank_G11/lesson_g11_l16_midgate_synthesis.py`, `Lesson_Bank_G11/lesson_g11_l30_gate_capstone.py`
  - `Lesson_Bank_G12/lesson_g12_l16_gate_frq_section.py`

**GATE template (per verdict + Task 1 GRAIN_TEMPLATES["gate"]):**
```
TEACH     teach_card       = a BARE moves-checklist / mnemonic recall cue (no worked model, no new teaching)
TEACH     stimulus_display = the held-out source (boxed_source renders it capped-scrollable)
SUPPORTED production_frq   = a brief PLANNING affordance ("outline your thesis + moves"), scored=False (NOT a certification write)
TRANSFER  production_frq   = the COLD write on the held-out source (the certification), scored=True, bank != any taught bank
INDEPENDENT self_score     = POST-HOC calibration against the rubric (after the write; role INDEPENDENT, not TRANSFER)
```
Set `lesson_class="gate"` on each. The plan slot MUST be `scored=False` (an affordance, not a scored write) so only the cold write is scored (`gate_gate_shape` caps scored writes at 1). REMOVE `annotated_before_after`, all `discrimination`, all `predict_the_fix`, and the `diagnosis_frq`. Keep the ONE_IDEA callout only as a compact reminder. Preserve `L.id`, `kc`, `unit`, `acc_tags`, `mastery`, and the held-out bound source.

- [ ] **Step 1: Positively enumerate ALL live gate lessons + reconcile the count against the verdict's 7**

Run: `python -c "import glob,sys; sys.path.insert(0,'pipeline'); from g9_push_dryrun import _load; seen={}; [seen.setdefault(_load(f).LESSON.id,[]).append(f) for f in glob.glob('Lesson_Bank_G*/lesson_*.py') if '_deprecated' not in f and _load(f) and getattr(_load(f),'LESSON',None) and (('gate' in (_load(f).LESSON.title or '').lower()) or getattr(_load(f).LESSON,'lesson_type',0)==8)]; [print(k, v) for k,v in seen.items()]"`
This lists every lesson that is title-"gate" OR lesson_type 8 (the WEAVE/synthesis type that includes the gates), grouped by id so duplicate files (e.g. a stale non-`_v3_1` twin of `ACC-W910-L-G9-C904-0026`) are visible. RECONCILE: the verdict named 7 gate lessons; confirm exactly which type-8 lessons are true unit GATES (a certification write) vs regular synthesis practice lessons. Only the true gates get `lesson_class="gate"`; the rest stay practice-class and are handled by their grain in Tasks 5-8. If the count is not 7, resolve WHY (stale twin, or a gate the verdict miscounted) before rewriting. Rewrite only live files (ignore non-`_v3_1` duplicates).

**RECONCILED 2026-07-15 (executed):** the LIVE set has **6 true gate lessons** (title contains "Gate"/"Mid-Gate"), NOT 7. The verdict's "7" over-counted by including a superseded G9 single-source-essay gate (`lesson_g9_l26_gate_essay.py`, non-`_v3_1`); the live G9 set has exactly two gates (informational C904-0026 + argument C904-0029). The 6 true gates to rewrite:
  1. `ACC-W910-L-G9-C904-0026` - lesson_g9_l26_gate_essay_v3_1.py (G9 informational)
  2. `ACC-W910-L-G9-C904-0029` - lesson_g9_l27_gate_argument_essay_v3_1.py (G9 argument)
  3. `ACC-W910-L-G10-C1006-0024` - lesson_g10_l24_gate_cross_text.py (G10 cross-text)
  4. `ACC-W1112-L-G11-C1102-0016` - lesson_g11_l16_midgate_synthesis.py (G11 mid-gate)
  5. `ACC-W1112-L-G11-C1102-0030` - lesson_g11_l30_gate_capstone.py (G11 capstone)
  6. `ACC-W910-L-G12-C1202-0016` - lesson_g12_l16_gate_frq_section.py (G12 FRQ section)
The other 13 type-8 lessons are synthesis PRACTICE (weave/calibrate/rehearse), NOT gates; they stay practice-class and are handled at their grain in Tasks 5-8.

- [ ] **Step 2: Rewrite one gate as the proof-of-concept (G10 cross-text)**

Edit `Lesson_Bank_G10/lesson_g10_l24_gate_cross_text.py`: add `lesson_class="gate"` to the `Lesson(...)`; replace the `slots=[...]` list with the 5-slot GATE template above, reusing the existing held-out stimulus ref and the existing REMEMBER checklist as the bare cue. Keep prompts em-dash-free and provenance-faithful.

- [ ] **Step 3: Verify the one lesson (24 gates + render-QC + grain crosscheck)**

Run: `python Lesson_Bank_G10/lesson_g10_l24_gate_cross_text.py && python pipeline/gated_reading.py Lesson_Bank_G10/lesson_g10_l24_gate_cross_text.py && python pipeline/grain_spine_crosscheck.py --grade G10 | grep C1006-0024`
Expected: `1/1 PASS`, render-QC exit 0, and no FAIL line for `C1006-0024`.

- [ ] **Step 4: Rewrite the remaining live gate lessons the same way**

Apply the identical transformation to the other confirmed-live gate files (G9 x1-2, G11 x2, G12 x1). Each keeps its own held-out source, KC, and mnemonic.

- [ ] **Step 5: Verify all gates**

Run: `for f in <the confirmed gate files>; do python "$f" >/dev/null 2>&1 && python pipeline/gated_reading.py "$f" >/dev/null 2>&1 && echo "OK $f" || echo "FAIL $f"; done`
Expected: all `OK`. Then `python pipeline/grain_spine_crosscheck.py` shows all gate lessons conform.

- [ ] **Step 6: Commit**

```bash
git add Lesson_Bank_G*/lesson_*gate*.py Lesson_Bank_G*/lesson_*midgate*.py
git commit -m "feat(lessons): P1 scaffold-free gates (cue + held-out source + plan + cold write + self-score)"
```

---

## Task 5: P3 + P4 essay grain - drop in-article transfer, one write + self-revision (T7 and essay-grain T8 non-gate)

**Files:** Modify all `lesson_type == 7` lessons and essay-grain `lesson_type == 8` NON-gate lessons across the four banks (~55-58 lessons). Identify the exact set in Step 1.

**ESSAY template (practice, essay grain):**
```
TEACH    teach_card        = retrieval-style reminder (sub-skills pre-taught upstream), ONE_IDEA callout
MODEL    stimulus_display  = the source (boxed_source at render)
MODEL    annotated_before_after = ONE essay-level worked move (thesis / evidence integration / structure)
MODEL    discrimination    = ONE, light (essay-level move); labeled_grade_c=True
MODEL    predict_the_fix   = 0 or 1 (optional; keep if it carries a distinct essay-level fix), feedback set
SUPPORTED production_frq    = the OUTLINE step (unit="multi_paragraph"): plan the essay, not a full draft
INDEPENDENT production_frq  = ONE full essay (unit="essay"), source boxed
MODEL     diagnosis_frq     = self-revision of the student's OWN essay (P5): "reread what you just wrote, run the check, fix any line that fails"
INDEPENDENT/TRANSFER self_score = analytic rubric, post-write
```
REMOVE the second `stimulus_display` (TRANSFER source) and the `TRANSFER production_frq` (the in-article transfer write). Transfer now lives in the gate + PP100. This satisfies `GRAIN_TEMPLATES[("practice","essay")]` (production_writes (1,1), no_transfer_write, diagnosis_on_own, discrimination_max 1).

NOTE: `gate_bank_partition` was already made essay-aware in Task 1 (returns pass for essay-grain practice lessons with no TRANSFER slot), so removing the in-article transfer here does not fail QC.

- [ ] **Step 1: Enumerate the essay-grain practice lessons**

Run: `python -c "import glob,sys,re; sys.path.insert(0,'pipeline'); from g9_push_dryrun import _load; from lesson_contract import grain; [print(f) for f in sorted(glob.glob('Lesson_Bank_G*/lesson_*.py')) if '_deprecated' not in f and (lambda L: L and getattr(L,'lesson_class','practice')!='gate' and grain(L)=='essay')(getattr(_load(f),'LESSON',None))]"`
Save the list; this is the task's work set.

- [ ] **Step 2: Rewrite ONE essay lesson as proof-of-concept, verify**

Pick one T7 (e.g. `Lesson_Bank_G10/lesson_g10_l21_analysis_essay.py`). Apply the ESSAY template. Verify:
`python Lesson_Bank_G10/lesson_g10_l21_analysis_essay.py && python pipeline/gated_reading.py Lesson_Bank_G10/lesson_g10_l21_analysis_essay.py && python pipeline/grain_spine_crosscheck.py --grade G10 | grep -i fail`
Expected: `1/1 PASS`, render exit 0, no FAIL for that id.

- [ ] **Step 4: Rewrite the rest of the essay-grain set** (batch by grade; this is subagent-parallelizable, 1 agent per lesson).

- [ ] **Step 5: Verify the whole essay-grain set** (all `1/1 PASS`, render exit 0, grain crosscheck clean for essay lessons). Then SCRIPT the mastery-integrity check over the FULL rewritten set (not a sample): for every rewritten essay lesson, assert (a) its `mastery_prompts_g*.py` entry still resolves for `L.id`, and (b) the mastery's held-out source bank differs from every taught/independent bank in the rewritten lesson. PP100 validity is a named verdict risk and IDs key the grader, so this must cover all, not 3.
Run: `python -c "import glob,sys; sys.path.insert(0,'pipeline'); from mastery_targets_grade import _authored; [print('MISSING', ...) ...]"` (author a small script `pipeline/verify_mastery_integrity.py` that loads each grade's MASTERY + lessons and prints any id whose mastery is missing or whose source bank overlaps a taught bank). Expected: zero problems.

- [ ] **Step 6: Commit** `git commit -m "feat(lessons): P3+P4 essay grain - one full write + self-revision, transfer routed to gate/PP100"`

---

## Task 6: P4 paragraph grain - plan, draft, revise (T3 + paragraph-grain lessons)

**Files:** Modify `lesson_type == 3` and other paragraph-grain practice lessons (~25).

**PARAGRAPH template (practice, paragraph grain):**
```
TEACH    teach_card
MODEL    stimulus_display (source, boxed if long)
MODEL    annotated_before_after (ONE paragraph-level model)
MODEL    discrimination (1-2)
MODEL    predict_the_fix (1), feedback set
SUPPORTED production_frq (unit="paragraph") = outline-first frame
INDEPENDENT production_frq (unit="paragraph") = plan-then-write
MODEL     diagnosis_frq = self-revision of OWN paragraph (P5)
INDEPENDENT self_score
```
Default: transfer routed to gate/PP100 (no in-article TRANSFER write). For lessons explicitly flagged transfer-critical, substitute ONE coached (feedback-bearing) TRANSFER write for the revision, never both. Matches `GRAIN_TEMPLATES[("practice","paragraph")]`.

- [ ] **Step 1: Enumerate paragraph-grain lessons** (same one-liner as Task 5 Step 1 with `grain(L)=='paragraph'`).
- [ ] **Step 2: Rewrite one, verify (1/1 PASS + render + crosscheck).**
- [ ] **Step 3: Rewrite the rest (subagent-parallel).**
- [ ] **Step 4: Verify the whole set.**
- [ ] **Step 5: Commit** `git commit -m "feat(lessons): P4 paragraph grain - plan/draft/revise with own-draft diagnosis"`

---

## Task 7: P4 sentence grain - compress model, multiply discrimination (T2 + sentence-grain T1/T6)

**Files:** Modify `lesson_type == 2` and sentence-grain `lesson_type in (1, 6)` lessons (~39).

**SENTENCE template (practice, sentence grain):**
```
TEACH    teach_card (compact)
MODEL    stimulus_display (short source)
MODEL    annotated_before_after (ONE short before/after)
MODEL    discrimination x2-3 (minimal pairs; this is where the reps live), labeled_grade_c=True
MODEL    predict_the_fix x1, feedback set
SUPPORTED production_frq (unit="sentence")
INDEPENDENT production_frq (unit="sentence")
TRANSFER production_frq (unit="sentence") = NEAR-VARIATION (new CONSTRAINT, not a new source) - cheap fluency rep
INDEPENDENT self_score (binary/single-point)
```
KEEP the 3 short writes (only grain that does). The TRANSFER is a near-variation, so it must carry a distinct `bank` slug (e.g. `<topic>-var`) so `gate_bank_partition` passes. Matches `GRAIN_TEMPLATES[("practice","sentence")]` (discrimination_min 2, production_writes (2,3)). `gate_model_sequence` was already relaxed in Task 1 so sentence-grain lessons need no `diagnosis_frq` (the diagnosis mechanism folds into predict_the_fix at this grain).

- [ ] **Step 1: Enumerate sentence-grain lessons** (same one-liner as Task 5 Step 1 with `grain(L)=='sentence'`).
- [ ] **Step 2: Rewrite one, verify (1/1 PASS + render + crosscheck).**
- [ ] **Step 3: Rewrite the rest (subagent-parallel).**
- [ ] **Step 4: Verify the whole set.**
- [ ] **Step 5: Commit** `git commit -m "feat(lessons): P4 sentence grain - dense discrimination + near-variation transfer reps"`

---

## Task 8: Align remaining types (T4 analysis, T5 revision) to nearest grain

**Files:** `lesson_type == 4` (11) + `lesson_type == 5` (19).

These were outside the deliberation's explicit scope (FLAG this to Noel at Task 11 Step 5 as an extrapolation beyond the deliberated verdict). Apply the LEAST-CHANGE alignment: derive each lesson's grain from its terminal production unit and conform it to that grain's template. T5 revision lessons are already revision-centric; mainly confirm they satisfy the revision-or-coached-transfer rule and the write-count bound, and remove any redundant in-article transfer at essay grain. Do NOT invent new pedagogy for these; just bring them under the same grain rules.

FALLBACK if T4/T5 rewrites prove non-trivial: rather than block the course-wide crosscheck (Task 9 Step 3), have `grain_spine_crosscheck.py` support a `--exempt-types 4,5` report-only mode for these two types, ship P1-P4 green, and schedule T4/T5 as a follow-up. Decide with Noel before forcing hard conformance on types the verdict never examined.

- [ ] **Step 1: Enumerate T4 + T5; print each one's grain + current crosscheck problems.**
- [ ] **Step 2: For each, make the minimal edits to clear its grain-crosscheck problems; verify (1/1 PASS + render + crosscheck).**
- [ ] **Step 3: Commit** `git commit -m "feat(lessons): align analysis + revision lessons to grain templates"`

---

## Task 9: Full-course regression (all four grades green on every harness)

**Files:** none (verification only).

- [ ] **Step 1: Every lesson passes its 24 contract gates.**
Run: `for f in Lesson_Bank_G*/lesson_*.py; do case "$f" in *_deprecated*) continue;; esac; python "$f" >/dev/null 2>&1 || echo "QCFAIL $f"; done; echo done`
Expected: no `QCFAIL`.

- [ ] **Step 2: Every lesson renders clean.**
Run: `for f in Lesson_Bank_G*/lesson_*.py; do case "$f" in *_deprecated*) continue;; esac; python pipeline/gated_reading.py "$f" >/dev/null 2>&1 || echo "RENDERFAIL $f"; done; echo done`
Expected: no `RENDERFAIL`.

- [ ] **Step 3: Grain-spine crosscheck fully green.**
Run: `python pipeline/grain_spine_crosscheck.py; echo "exit $?"`
Expected: `... N/N conform`, `exit 0`.

- [ ] **Step 4: Existing crosschecks still green (no standards/scaffold regressions).**
Run: `python pipeline/scaffold_crosscheck.py; python pipeline/ccss_crosscheck.py; python pipeline/ccss_1112_crosscheck.py; echo "done"`
Expected: each exit 0 (or unchanged from pre-plan baseline; compare to a captured baseline if any were already non-zero).

- [ ] **Step 5: Commit any incidental fixes** `git commit -m "test: full-course regression green after spine re-architecture"` (or note clean).

---

## Task 10: Source-formatting fix (issue-frame question lead-in)

**Files:**
- Modify: the 11 issue-frame stimuli containing `Here is the question for your claim:` (enumerate in Step 1).
- Modify: `pipeline/gated_reading.py` (`frq_xml` + `_content_card`/`_stim_html` source block), `pipeline/mastery_targets_grade.py`, `pipeline/g9_push_mastery_v3_1.py` (the 3 source-block render sites).

Goal (from Noel's report): the question must be a styled structural lead-in, not buried in the passage prose: bold label ("Here is the question for your claim:"), the question itself italicized, and a line break before the passage.

- [ ] **Step 1: Enumerate the 11 stimuli.**
Run: `grep -rl "Here is the question for your claim" Stimulus_Bank_G*/*.py`

- [ ] **Step 2: Move the question out of the passage `text` into the record's `prompt` field (or a dedicated leading block).** For each stimulus, strip the `Here is the question for your claim: <Q?> ` prefix from the passage `text`, and ensure the `prompt` field holds the question (most already do). Re-run each stimulus file's QC: `python Stimulus_Bank_XX/<file>.py` -> PASS (issue_frame is floor/Lexile-exempt).

- [ ] **Step 3: Render the question as a styled lead-in at the source-block sites.** In `_stim_html` (or the source-block builders in the 3 render sites), when a record has a `prompt`, emit above the passage:
`<div style="font-weight:700;margin:0 0 2px;">Here is the question for your claim:</div><div style="font-style:italic;margin:0 0 8px;">{prompt}</div>` then the passage paragraphs. Keep it em-dash-free and entity-safe (`_xml_safe_entities`).

- [ ] **Step 4: Verify render.** Re-render one affected lesson (`gated_reading.py` on a lesson binding a fixed stimulus) and one mastery page; confirm the label is bold, the question italic, and a break separates it from the passage. Run render-QC exit 0.

- [ ] **Step 5: Commit** `git commit -m "fix(stimuli): issue-frame question as styled lead-in (bold label + italic question + break)"`

---

## Task 11: Re-render + redeploy the Vercel review preview (all 4 courses)

**Files:** none (regenerates deploy artifacts under the linked `vercel_deploy` project).

- [ ] **Step 1: Re-render all four course previews.**
Run: `python pipeline/render_course_preview.py && for g in G10 G11 G12; do python pipeline/render_course_preview_grade.py $g; done`
Expected: each prints its article + mastery-page counts; RENDER-QC exit 0 for all.

- [ ] **Step 2: Deploy to production alias.**
Run: `cd /c/Users/noelp/AppData/Local/Temp/vercel_deploy && vercel deploy --prod --yes`
Expected: `status ok`, aliased to `verceldeploy-five-tan.vercel.app`.

- [ ] **Step 3: Verify live (python urllib, not curl - Windows schannel cert quirk).**
Confirm 200s for the four course indexes + a sample gated article per grade + a sample mastery page; confirm a gate lesson's article now shows the scaffold-free shape and an essay lesson shows one write + self-revision.

- [ ] **Step 4: Update the build log + memory.**
Append the re-architecture to `hs-writing-build-log` memory and note the new lesson_class/grain contract fields.

- [ ] **Step 5: Present to Noel for review.** Do NOT push to Timeback. Surface the preview URL + a summary of what changed per grain; await approval for the live push (separate step).
