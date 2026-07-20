# LS-Feedback Pipeline Encoding — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Encode the learning-scientist feedback into the generation pipeline (shared helpers + archetype playbooks + deterministic gates) so new lessons comply by construction and drift fails the build, then pilot on 2 lessons before a gated course-wide rollout.

**Architecture:** Three enforcement layers. **L1** shared helpers (`pipeline/lesson_prompts.py`) fix a structural default once. **L2** archetype playbooks (`_phase2/playbook_T*.md`) guide generation. **L3** deterministic gates (`pipeline/lesson_contract.py`, registry `_GATES`, run by `pipeline/tier_a_regression.py`) hard-block violations. Every gate ships paired KNOWN-BAD + KNOWN-GOOD fixtures (verify-the-verifier). Cadence thresholds come from the council ruling; archetype is DERIVED from `Lesson.lesson_type` (no new lesson field); only card exceptions (buy-in, memorizable-tool) get a new optional `Slot.tag`.

**Tech Stack:** Python lesson banks + `pipeline/lesson_contract.py` gates + `pipeline/tests/` (pytest); verified by `python pipeline/tier_a_regression.py {G9|G10|G11|G12}` and `python -m pytest pipeline/tests/ -q`.

## Global Constraints

- **No em dashes** in any student-facing text. Use commas/colons/parentheses.
- **Lesson IDs, mastery keys, `rubric_ref`, `acc_tags` are STABLE** — never renamed.
- **No fabricated facts/figures** — reuse only verified figures already in a bound source.
- **Timeback-native only** — display / extended-text FRQ / choice slot kinds; no new interaction types.
- **Every touched lesson ends clean on `tier_a_regression.py`; full `pytest pipeline/tests/` stays green.**
- **Verify-the-verifier:** every new/changed gate ships a KNOWN-BAD fixture that MUST trip it AND a KNOWN-GOOD that must NOT. A gate with only passing fixtures is a plan failure.
- **Gates go in GREEN but INERT for rollout:** a new gate must not fail existing lessons until the pilot is signed off. Achieve this by (a) building the gate + fixtures first (Tasks 2-8), (b) applying it to the 2 pilot lessons (Task 9), (c) ONLY THEN running it course-wide (Task 11). If a gate would fail existing lessons the moment it lands in `_GATES`, register it behind a flag or land it in the same task as the pilot fix — see Task sequencing note.
- **Archetype tiers (council):** concept-teaching = `lesson_type ∈ {1,2,3,4,6}` (type 4 = DEW text-dependent-analysis, a concept-teaching move: device→effect→warrant — 7 lessons, classify explicitly, NOT via fallback); checking-revision = `{5}`; full-essay-build = `{7,8}`. Cadence ceilings: concept **3** (→**2** right after a memorizable-tool card), checking-revision **2**, full-essay-build **4** (milestones only). Verified type distribution across all grades: {2:13, 3:15, 4:7, 5:13, 6:7, 7:26, 8:17} — no type 1 currently in the banks, but keep it mapped to concept for safety.
- **Pilot lessons:** `Lesson_Bank_G9/lesson_g9_l01_arguable_claim_v3_1.py` (C901-0001) + `Lesson_Bank_G9/lesson_g9_l03_controlling_idea_v3_1.py` (exercises #7 stem wording + #9 repeat-gloss).

---

### Task 1: Add the `Slot.tag` field + archetype/cadence helpers (foundation, no behavior change yet)

**Files:**
- Modify: `pipeline/lesson_contract.py` (Slot dataclass + module-level helpers)
- Test: `pipeline/tests/test_cadence_helpers.py` (create)

**Interfaces:**
- Produces: `Slot.tag: str = ""` (optional; values: `""` ordinary, `"buy_in"`, `"memorizable_tool"`, `"worked_example"` — note `annotated_before_after` kind already implies worked-example, so `tag` is mainly for buy-in + memorizable-tool on `teach_card`s).
- Produces: `archetype_of(L) -> str` returning `"concept" | "checking_revision" | "full_essay_build"` from `L.lesson_type`.
- Produces: `CADENCE_CEILING = {"concept": 3, "checking_revision": 2, "full_essay_build": 4}` and `MEMORIZABLE_TOOL_CEILING = 2`.

- [ ] **Step 1: Write the failing test**

```python
# pipeline/tests/test_cadence_helpers.py
import os, sys
PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path: sys.path.insert(0, PIPE)
from lesson_contract import Slot, Lesson, archetype_of, CADENCE_CEILING, MEMORIZABLE_TOOL_CEILING

def _L(lt): return Lesson(id="X", grade="9-10", lesson_type=lt, unit="U", title="T", target="t", slots=[])

def test_archetype_mapping():
    assert archetype_of(_L(1)) == "concept"
    assert archetype_of(_L(2)) == "concept"
    assert archetype_of(_L(3)) == "concept"
    assert archetype_of(_L(4)) == "concept"   # DEW text-dependent-analysis
    assert archetype_of(_L(6)) == "concept"
    assert archetype_of(_L(5)) == "checking_revision"
    assert archetype_of(_L(7)) == "full_essay_build"
    assert archetype_of(_L(8)) == "full_essay_build"

def test_ceilings():
    assert CADENCE_CEILING["concept"] == 3
    assert CADENCE_CEILING["checking_revision"] == 2
    assert CADENCE_CEILING["full_essay_build"] == 4
    assert MEMORIZABLE_TOOL_CEILING == 2

def test_slot_tag_defaults_empty_and_accepts_values():
    s = Slot("TEACH", "teach_card", "t")
    assert s.tag == ""
    s2 = Slot("TEACH", "teach_card", "t", tag="memorizable_tool")
    assert s2.tag == "memorizable_tool"
```

- [ ] **Step 2: Run it, verify failure** — `python -m pytest pipeline/tests/test_cadence_helpers.py -v` → FAIL (`archetype_of` not defined, `Slot` has no `tag`).

- [ ] **Step 3: Implement** — in `pipeline/lesson_contract.py`:
  - Add to the `Slot` dataclass (after `choices`): `tag: str = ""  # "" | "buy_in" | "memorizable_tool" | "worked_example"; cadence-gate hints (buy_in counts 0; memorizable_tool tightens the ceiling)`.
  - Add module-level, near the archetype-name map (the `{1:("source-reading",...)}` dict around line 56):
```python
CADENCE_CEILING = {"concept": 3, "checking_revision": 2, "full_essay_build": 4}
MEMORIZABLE_TOOL_CEILING = 2
_ARCHETYPE_BY_TYPE = {1: "concept", 2: "concept", 3: "concept", 4: "concept", 6: "concept",
                      5: "checking_revision", 7: "full_essay_build", 8: "full_essay_build"}
def archetype_of(L) -> str:
    """Council cadence tier from lesson_type. Type 4 = DEW text-dependent-analysis (concept-teaching).
    Unknown types default to concept (the tightest ceiling, safest for novices)."""
    return _ARCHETYPE_BY_TYPE.get(getattr(L, "lesson_type", 0), "concept")
```

- [ ] **Step 4: Run tests, verify pass** — `python -m pytest pipeline/tests/test_cadence_helpers.py -v` → PASS.

- [ ] **Step 5: Verify no regression** — `python -m pytest pipeline/tests/ -q` (expect 124 passed: prior 121 + 3 new). Then `python pipeline/tier_a_regression.py G9 2>&1 | tail -1` (adding an optional field must not change any lesson's result → still 26/26).

- [ ] **Step 6: Commit**
```bash
git add "Alpha HS Writing Course 2026-27/pipeline/lesson_contract.py" "Alpha HS Writing Course 2026-27/pipeline/tests/test_cadence_helpers.py"
git commit -m "feat(gates): add Slot.tag + archetype_of/cadence-ceiling helpers (foundation for LS-feedback gates)"
```

---

### Task 2: `gate_frame_comma` (#2 — no comma before "because"/"so" in a fill-in frame)

**Files:**
- Modify: `pipeline/lesson_contract.py` (new gate + register in `_GATES`)
- Test: `pipeline/tests/test_gate_frame_comma.py` (create)

**Interfaces:**
- Consumes: `Slot.body` HTML; targets set-apart FRAME blocks only (a frame is a `setapart` block containing fill-in blanks `______`).
- Produces: `gate_frame_comma(L) -> tuple[bool, str]` registered as `("frame_comma", gate_frame_comma)`.

- [ ] **Step 1: Write the failing test**

```python
# pipeline/tests/test_gate_frame_comma.py
import os, sys
PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path: sys.path.insert(0, PIPE)
from lesson_contract import Slot, Lesson, gate_frame_comma

def _L(*slots): return Lesson(id="X", grade="9-10", lesson_type=2, unit="U", title="T", target="t", slots=list(slots))

def test_bad_comma_before_because_in_frame():
    # a fill-in frame with the offending comma
    s = Slot("SUPPORTED", "production_frq", "w",
             body='<div>Copy this frame: Schools should ______ [your side], because ______ [your reason].</div>')
    ok, msg = gate_frame_comma(_L(s))
    assert not ok and "because" in msg.lower()

def test_good_frame_no_comma():
    s = Slot("SUPPORTED", "production_frq", "w",
             body='<div>Copy this frame: Schools should ______ [your side] because ______ [your reason].</div>')
    ok, _ = gate_frame_comma(_L(s))
    assert ok

def test_ordinary_prose_comma_before_because_is_fine():
    # NOT a fill-in frame (no blanks) -> a normal sentence with ", because" must NOT be flagged
    s = Slot("TEACH", "teach_card", "t",
             body='<div>A claim is arguable, because someone could disagree with it.</div>')
    ok, _ = gate_frame_comma(_L(s))
    assert ok
```

- [ ] **Step 2: Run, verify failure** — `pytest pipeline/tests/test_gate_frame_comma.py -v` → FAIL (`gate_frame_comma` undefined).

- [ ] **Step 3: Implement** — in `lesson_contract.py`, near the other copy gates:

```python
# a fill-in frame = student-facing text with fill blanks; comma before a restrictive because/so clause in
# a FRAME reads as a punctuation model the student copies. Flag ", because"/", so" ONLY inside a frame
# (a chunk containing "______"), never in ordinary prose.
_FRAME_COMMA_RE = re.compile(r",\s+(because|so)\b", re.I)
def gate_frame_comma(L) -> tuple[bool, str]:
    hits = []
    for i, s in enumerate(L.slots, 1):
        body = s.body or ""
        if "______" not in body:            # only fill-in frames
            continue
        # scan each frame-ish sentence containing a blank
        for seg in re.split(r"(?<=[.!?])\s+", re.sub(r"<[^>]+>", " ", body)):
            if "______" in seg and _FRAME_COMMA_RE.search(seg):
                hits.append(f"slot {i}: '{seg.strip()[:60]}'")
    if hits:
        return False, "comma before 'because'/'so' in a fill-in frame (drop it): " + "; ".join(hits[:4])
    return True, "no frame punctuation-model errors"
```
Register in `_GATES`: `("frame_comma", gate_frame_comma),`.

- [ ] **Step 4: Run tests, verify pass** — `pytest pipeline/tests/test_gate_frame_comma.py -v` → 3 PASS.

- [ ] **Step 5: Scan (do NOT fix yet) which existing lessons this flags** — `python pipeline/tier_a_regression.py G9 2>&1 | grep -A1 frame_comma | head`. Record the count. (Expected: the ~5 files with the `[your side], because` frame. These are fixed in the pilot/rollout, NOT here.)
- Because this gate WILL fail existing lessons the moment it registers, this task's commit lands the gate + fixtures; the pilot (Task 9) fixes the pilot lessons; the rollout (Task 11) fixes the rest. Between Task 2 and Task 9, `tier_a_regression G9` will show frame_comma failures on the ~5 legacy files — that is expected and is the gate's worklist. Note it in the commit.

- [ ] **Step 6: Commit**
```bash
git add "Alpha HS Writing Course 2026-27/pipeline/lesson_contract.py" "Alpha HS Writing Course 2026-27/pipeline/tests/test_gate_frame_comma.py"
git commit -m "feat(gates): gate_frame_comma (#2) - no comma before because/so in fill-in frames; flags ~5 legacy G9 frames for rollout"
```

---

### Task 3: `gate_min_four_options` (#8 — discrimination MCQs need exactly 4 options)

**Files:**
- Modify: `pipeline/lesson_contract.py` — tighten the option-count rule inside `gate_structural_item` (do NOT add a separate gate; the count check lives there).
- Test: `pipeline/tests/test_gate_four_options.py` (create)

**Interfaces:**
- Consumes: discrimination slots' options (via existing `_slot_options`).
- Produces: `gate_structural_item` fails a `discrimination` slot with != 4 options; `self_score` (2-point predict) and `predict_the_fix` keep their existing allowances.

- [ ] **Step 1: Write the failing test**

```python
# pipeline/tests/test_gate_four_options.py
import os, sys
PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path: sys.path.insert(0, PIPE)
from lesson_contract import Slot, Lesson, gate_structural_item

def _disc(nopts):
    ch = [{"id": chr(65+i), "text": f"option {i} with enough words to be real here", "correct": i==nopts-1,
           "why": "because reasons"} for i in range(nopts)]
    s = Slot("MODEL", "discrimination", "q", body="Pick one.", choices=ch)
    return Lesson(id="X", grade="9-10", lesson_type=2, unit="U", title="T", target="t", slots=[s])

def test_three_option_discrimination_fails():
    ok, msg = gate_structural_item(_disc(3))
    assert not ok and ("4" in msg or "four" in msg.lower())

def test_four_option_discrimination_passes():
    ok, _ = gate_structural_item(_disc(4))
    assert ok

def test_self_score_two_option_still_passes():
    ch = [{"id":"pass","text":"yes all present and correct here","correct":True,"why":"y"},
          {"id":"gap","text":"no at least one missing or weak","correct":False,"why":"n"}]
    s = Slot("INDEPENDENT","self_score","score",body="predict",choices=ch)
    L = Lesson(id="X",grade="9-10",lesson_type=7,unit="U",title="T",target="t",slots=[s])
    ok, _ = gate_structural_item(L)
    assert ok
```

- [ ] **Step 2: Run, verify failure** — `pytest pipeline/tests/test_gate_four_options.py -v` → `test_three_option_discrimination_fails` FAILS (current rule allows 2-4).

- [ ] **Step 3: Implement** — in `gate_structural_item`, find the option-count block (currently `if n < 2 or n > 4:` around line 899-901). Change the discrimination branch to require exactly 4 while leaving self_score/predict_the_fix as-is. Concretely, inside the per-slot loop where `s.kind == "discrimination"`:
```python
        n = len(opts)
        if s.kind == "discrimination":
            if n != 4:
                problems.append(f"{tag}: discrimination has {n} options (need exactly 4; each a named misconception)")
        elif n < 2 or n > 4:
            problems.append(f"{tag}: {n} options (a choice item needs 2-4)")
```
(Keep the duplicate-option and single-key checks unchanged.)

- [ ] **Step 4: Run tests, verify pass** — `pytest pipeline/tests/test_gate_four_options.py -v` → 3 PASS. Also `pytest pipeline/tests/test_render_fidelity.py -q` (the golden lesson there uses 3-option items — see Step 5).

- [ ] **Step 5: Fix the fixtures/goldens that now break** — the existing `golden_lesson()` fixture and any in-repo test lesson with 3-option discriminations will now fail. Update ONLY the test fixtures (`pipeline/fixtures.py` golden + the demo lesson in `lesson_contract.__main__`) to 4 options so the test suite reflects the new rule. Do NOT touch real lessons here.
- [ ] **Step 5b: Register the new rule in the in-flight allowlist** — the 4-option rule flags ~118 legacy lessons via the EXISTING `structural_item` gate, which cannot be allowlisted by gate-name. In `pipeline/tests/test_tier_a_regression.py`, add your exact new failure-message substring to `_INFLIGHT_MSG_SUBSTRINGS` (e.g. `("need exactly 4",)` if your message says "need exactly 4"). Then `python -m pytest pipeline/tests/test_tier_a_regression.py -q` must PASS (the course-clean invariants tolerate the known 4-option flags but still catch anything else). Keep the substring SPECIFIC to this rule so it can't mask a real structural_item defect.
- Record the course-wide flag count (the ~118 real items): `python pipeline/tier_a_regression.py G9 2>&1 | grep -c "options (need exactly 4"` and same for G10/G11/G12. This is the Task-11 rollout worklist.

- [ ] **Step 6: Commit**
```bash
git add "Alpha HS Writing Course 2026-27/pipeline/lesson_contract.py" "Alpha HS Writing Course 2026-27/pipeline/tests/test_gate_four_options.py" "Alpha HS Writing Course 2026-27/pipeline/fixtures.py"
git commit -m "feat(gates): gate_structural_item requires 4 options on discrimination (#8); ~118 legacy 3-opt items flagged for rollout"
```

---

### Task 4: `gate_self_answered_check` (#6 — a diagnosis must not pre-answer its own check)

**Files:**
- Modify: `pipeline/lesson_contract.py` (new gate + register)
- Test: `pipeline/tests/test_gate_self_answered_check.py` (create)

**Interfaces:**
- Consumes: `diagnosis_frq` slot bodies.
- Produces: `gate_self_answered_check(L)` — fails a diagnosis_frq whose prompt states its own check answers (`? No,` / `? Yes,`) UNLESS it is the sanctioned coping-model (a PROVIDED weak draft explicitly labeled, followed by an independent student turn signalled by "now write"/"now you"/"your own"/"a fresh").

- [ ] **Step 1: Write the failing test**

```python
# pipeline/tests/test_gate_self_answered_check.py
import os, sys
PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path: sys.path.insert(0, PIPE)
from lesson_contract import Slot, Lesson, gate_self_answered_check

def _L(body): return Lesson(id="X",grade="9-10",lesson_type=2,unit="U",title="T",target="t",
                            slots=[Slot("MODEL","diagnosis_frq","check",body=body)])

def test_pure_giveaway_fails():
    # prompt answers its own checks AND gives the student no independent turn
    body=("Run the 3-question test on this draft. Does it take a side? No, it just reports a fact. "
          "Is there a reason? No. Now you have the fixed version.")
    ok, msg = gate_self_answered_check(_L(body))
    assert not ok

def test_coping_model_then_own_turn_passes():
    # the modeled check runs on a PROVIDED weak draft, THEN the student does their own -> sanctioned
    body=("Run the check on this provided weak draft. Does it take a side? No, add one. "
          "Now write a fresh claim of your own and run the same three checks on it.")
    ok, _ = gate_self_answered_check(_L(body))
    assert ok

def test_clean_diagnosis_no_selfanswers_passes():
    body=("Run the 3-question test on your draft, then rewrite it so it passes all three.")
    ok, _ = gate_self_answered_check(_L(body))
    assert ok
```

- [ ] **Step 2: Run, verify failure** — `pytest pipeline/tests/test_gate_self_answered_check.py -v` → FAIL (undefined).

- [ ] **Step 3: Implement**
```python
_SELF_ANSWER_RE = re.compile(r"\?\s*(yes|no)[,\.\s]", re.I)
_OWN_TURN_RE = re.compile(r"\b(now (write|you|revise)|your own|a fresh|write and check)\b", re.I)
def gate_self_answered_check(L) -> tuple[bool, str]:
    """#6: a diagnosis must make the student ANSWER the check, not read pre-answered ones. A prompt that
    answers its own check questions is only OK when it is a coping-model demo on a PROVIDED draft that is
    THEN followed by an independent student turn (own-turn signal)."""
    for i, s in enumerate(L.slots, 1):
        if s.kind != "diagnosis_frq":
            continue
        text = re.sub(r"<[^>]+>", " ", s.body or "")
        if _SELF_ANSWER_RE.search(text) and not _OWN_TURN_RE.search(text):
            return False, (f"slot {i}: diagnosis pre-answers its own check with no independent student turn "
                           f"(make the student answer the check, or add a 'now write your own' turn)")
    return True, "diagnosis checks are student-answered (or sanctioned coping-model + own turn)"
```
Register `("self_answered_check", gate_self_answered_check),`.

- [ ] **Step 4: Run tests, verify pass** — 3 PASS.
- [ ] **Step 5: Record course-wide flags** (the "checks that run themselves" instances) for the rollout worklist. Do not fix here.
- [ ] **Step 6: Commit**
```bash
git add "Alpha HS Writing Course 2026-27/pipeline/lesson_contract.py" "Alpha HS Writing Course 2026-27/pipeline/tests/test_gate_self_answered_check.py"
git commit -m "feat(gates): gate_self_answered_check (#6) - diagnosis must not pre-answer its own check; coping-model carve-out"
```

---

### Task 5: HARD-TERM re-gloss (#9) — ALREADY ENFORCED (no-op, closed 2026-07-20)

**Outcome:** BLOCKED-then-closed. The task's premise was wrong: `gate_define_before_use` is NOT course-first-only — it is ALREADY fully per-lesson (takes a single `Lesson`, checks THIS lesson's TEACH bodies for a `_DEF_CUE` near each `_TECH_TERMS` term), and all four hard terms (controlling idea, warrant, synthesis, counterclaim) are ALREADY in `_TECH_TERMS`. Verified end-to-end: a lesson using "controlling idea" with no in-lesson gloss already FAILS today; a glossed one passes; course-wide `define_before_use` flags = 0. So #9 (an odd term must be glossed in every lesson that uses it) is already enforced. No code added (adding a redundant HARD_TERMS set + a "re-gloss" message that can never fire would be dead code, and the required guard test would force a course-memory regression).

**Residual (routed to T8 playbook, not a gate):** the LS asked specifically for a *bracketed* re-gloss on re-introduction; the gate accepts any definitional cue on first in-lesson use, not specifically brackets, and does not force a re-gloss on every later mention within one lesson. That bracketing/style nuance is a playbook authoring note (T8), not worth a hard gate. **#9 rollout worklist = 0.**

<details><summary>Original task text (superseded)</summary>

#### (superseded) Extend gate_define_before_use for HARD-TERM re-gloss (#9)

**Files:**
- Modify: `pipeline/lesson_contract.py` (`gate_define_before_use` + a `HARD_TERMS` set)
- Test: `pipeline/tests/test_gate_reglossing.py` (create)

**Interfaces:**
- Consumes: teach-slot bodies.
- Produces: for terms in `HARD_TERMS = {"controlling idea", "warrant", "synthesis", "counterclaim"}`, the gate requires a definitional cue (existing `_DEF_CUE`) on the term's first student-facing use **within each lesson that uses it** (not only the course-first lesson). Existing non-hard-term behavior unchanged.

- [ ] **Step 1: Write the failing test**

```python
# pipeline/tests/test_gate_reglossing.py
import os, sys
PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path: sys.path.insert(0, PIPE)
from lesson_contract import Slot, Lesson, gate_define_before_use

def _L(*bodies):
    slots=[Slot("TEACH","teach_card",f"t{i}",body=b) for i,b in enumerate(bodies)]
    return Lesson(id="X",grade="9-10",lesson_type=2,unit="U",title="T",target="t",slots=slots)

def test_hard_term_used_without_gloss_fails():
    L=_L("Write a controlling idea that names your focus.")   # used, never glossed in-lesson
    ok,msg=gate_define_before_use(L)
    assert not ok and "controlling idea" in msg.lower()

def test_hard_term_reglossed_passes():
    L=_L("A controlling idea is a sentence that names the focus of your explanation with no side. "
         "Write a controlling idea for this source.")
    ok,_=gate_define_before_use(L)
    assert ok
```

- [ ] **Step 2: Run, verify failure** — the first test FAILS (today's gate only checks course-first use, so a later lesson using "controlling idea" bare passes).

- [ ] **Step 3: Implement** — add `HARD_TERMS = {"controlling idea", "warrant", "synthesis", "counterclaim"}` near `_TECH_TERMS`. In `gate_define_before_use`, after the existing logic, add: for each HARD_TERM appearing in any student-facing slot of THIS lesson, require `_teach_defines(term_regex, teach_bodies)` to be true (a `_DEF_CUE` near the term in a TEACH body of this lesson). Fail with a clear message if used-but-not-glossed in-lesson.

- [ ] **Step 4: Run tests, verify pass** — 2 PASS + rerun `test_cadence_helpers` and the existing define-before-use coverage.
- [ ] **Step 5: Record course-wide flags** (later lessons using a hard term with no in-lesson gloss). Rollout worklist.
- [ ] **Step 6: Commit**
```bash
git add "Alpha HS Writing Course 2026-27/pipeline/lesson_contract.py" "Alpha HS Writing Course 2026-27/pipeline/tests/test_gate_reglossing.py"
git commit -m "feat(gates): define_before_use re-glosses HARD_TERMS per-lesson (#9)"
```

</details>

---

### Task 6: `gate_check_cadence` (#3 — archetype-ceiling of teach segments before a check)

**Files:**
- Modify: `pipeline/lesson_contract.py` (new gate + register)
- Test: `pipeline/tests/test_gate_check_cadence.py` (create)

**Interfaces:**
- Consumes: `L.slots`, `archetype_of(L)`, `CADENCE_CEILING`, `MEMORIZABLE_TOOL_CEILING`, `Slot.tag`, `Slot.kind`, `L.lesson_class`.
- Produces: `gate_check_cadence(L)` — fails if a run of COUNTED segments exceeds the effective ceiling with no intervening qualifying check.
- Counting rules (from spec): teach_card/stimulus_display/annotated_before_after = +1; `tag=="buy_in"` counts 0; a run of consecutive `annotated_before_after` counts as 1 worked example (do not split); checks = discrimination/predict_the_fix/self_score reset the counter to 0. Effective ceiling = `min(archetype_ceiling, MEMORIZABLE_TOOL_CEILING)` while the most recent counted card had `tag=="memorizable_tool"`. Exempt `lesson_class=="gate"` entirely; the final production/diagnosis write block is not a teach segment.

- [ ] **Step 1: Write the failing test**

```python
# pipeline/tests/test_gate_check_cadence.py
import os, sys
PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path: sys.path.insert(0, PIPE)
from lesson_contract import Slot, Lesson, gate_check_cadence

def _mk(lt, kinds_tags, lesson_class="practice"):
    slots=[]
    for k,tag in kinds_tags:
        slots.append(Slot("TEACH" if k in ("teach_card","stimulus_display","annotated_before_after") else "MODEL",
                          k, "s", body="x"*120, tag=tag,
                          choices=[{"id":"A","text":"a","correct":True,"why":"y"}] if k=="discrimination" else []))
    return Lesson(id="X",grade="9-10",lesson_type=lt,unit="U",title="T",target="t",slots=slots,lesson_class=lesson_class)

def test_concept_four_teach_no_check_fails():
    L=_mk(2, [("teach_card",""),("teach_card",""),("teach_card",""),("teach_card","")])
    ok,msg=gate_check_cadence(L); assert not ok

def test_concept_three_then_check_passes():
    L=_mk(2, [("teach_card",""),("teach_card",""),("teach_card",""),("discrimination","")])
    ok,_=gate_check_cadence(L); assert ok

def test_memorizable_tool_tightens_to_two():
    # tool card, then 2 more teach with no check -> exceeds min(3,2)=2
    L=_mk(2, [("teach_card","memorizable_tool"),("teach_card",""),("teach_card","")])
    ok,_=gate_check_cadence(L); assert not ok

def test_worked_example_run_counts_as_one():
    # 3 consecutive annotated_before_after = ONE worked example, +1 teach, then check -> ok under N=3
    L=_mk(2, [("annotated_before_after",""),("annotated_before_after",""),("annotated_before_after",""),
              ("teach_card",""),("discrimination","")])
    ok,_=gate_check_cadence(L); assert ok

def test_buy_in_counts_zero():
    L=_mk(2, [("teach_card","buy_in"),("teach_card","buy_in"),("teach_card",""),("teach_card",""),("teach_card",""),("discrimination","")])
    ok,_=gate_check_cadence(L); assert ok  # only 3 counted before the check

def test_gate_class_exempt():
    L=_mk(7, [("teach_card",""),("teach_card",""),("teach_card",""),("teach_card","")], lesson_class="gate")
    ok,_=gate_check_cadence(L); assert ok
```

- [ ] **Step 2: Run, verify failure** — undefined.

- [ ] **Step 3: Implement**
```python
_CHECK_KINDS = {"discrimination", "predict_the_fix", "self_score"}
_COUNTED_KINDS = {"teach_card", "stimulus_display", "annotated_before_after"}
def gate_check_cadence(L) -> tuple[bool, str]:
    """#3 (council): a run of counted teach segments may not exceed the archetype ceiling with no
    intervening check. Worked-example run = 1; buy_in = 0; memorizable_tool tightens the ceiling to 2
    until the next check. Gate-class lessons + the final write block are exempt."""
    if getattr(L, "lesson_class", "practice") == "gate":
        return True, "gate-class lesson exempt from cadence"
    ceiling = CADENCE_CEILING[archetype_of(L)]
    count = 0; eff = ceiling; prev_worked = False; run_start = None
    for i, s in enumerate(L.slots, 1):
        if s.kind in _CHECK_KINDS:
            count = 0; eff = ceiling; prev_worked = False; continue
        if s.kind not in _COUNTED_KINDS:
            continue                              # production/diagnosis writes are not teach segments
        if s.tag == "buy_in":
            continue
        # collapse a consecutive run of annotated_before_after into one worked example
        if s.kind == "annotated_before_after" and prev_worked:
            continue
        prev_worked = (s.kind == "annotated_before_after")
        count += 1
        if count == 1: run_start = i
        eff = min(ceiling, MEMORIZABLE_TOOL_CEILING) if s.tag == "memorizable_tool" else eff
        if count > eff:
            return False, (f"slots {run_start}-{i}: {count} counted teach segments with no check "
                           f"(archetype {archetype_of(L)} ceiling {eff})")
    return True, f"cadence ok (ceiling {ceiling})"
```
Register `("check_cadence", gate_check_cadence),`.

- [ ] **Step 4: Run tests, verify pass** — 6 PASS.
- [ ] **Step 5: Record course-wide flags** for the rollout worklist (lessons with too-long teach runs). Do not fix here.
- [ ] **Step 6: Commit**
```bash
git add "Alpha HS Writing Course 2026-27/pipeline/lesson_contract.py" "Alpha HS Writing Course 2026-27/pipeline/tests/test_gate_check_cadence.py"
git commit -m "feat(gates): gate_check_cadence (#3) - per-archetype teach-before-check ceiling; worked-example + buy-in + memorizable-tool rules"
```

---

### Task 7: L1 helper — a comma-free side/reason frame builder (#2, generation-side)

**Files:**
- Modify: `pipeline/lesson_prompts.py` (add `claim_frame` helper)
- Test: `pipeline/tests/test_claim_frame_helper.py` (create)

**Interfaces:**
- Produces: `claim_frame(side_label, reason_label, stem="") -> str` emitting a `setapart` frame with NO comma before "because", so future lessons call the helper instead of hand-writing the frame.

- [ ] **Step 1: Write the failing test**
```python
# pipeline/tests/test_claim_frame_helper.py
import os, sys
PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path: sys.path.insert(0, PIPE)
from lesson_prompts import claim_frame
def test_frame_has_no_comma_before_because():
    out = claim_frame("your side on the four-day week", "your reason")
    assert ", because" not in out
    assert "because" in out and "______" in out
```
- [ ] **Step 2: Run, verify failure** — undefined.
- [ ] **Step 3: Implement** in `lesson_prompts.py`:
```python
def claim_frame(side_label, reason_label, stem="Schools should"):
    """A side+reason fill-in frame with NO comma before 'because' (a punctuation model students copy)."""
    return setapart("Copy this frame, then fill in the blanks:",
                    f"{stem} ______ [{side_label}] because ______ [{reason_label}].")
```
- [ ] **Step 4: Run test, verify pass.**
- [ ] **Step 5: Commit**
```bash
git add "Alpha HS Writing Course 2026-27/pipeline/lesson_prompts.py" "Alpha HS Writing Course 2026-27/pipeline/tests/test_claim_frame_helper.py"
git commit -m "feat(helpers): claim_frame() emits comma-free side/reason frame (#2 generation-side)"
```

---

### Task 8: Update the archetype playbooks (L2 — generation guidance)

**Files:**
- Modify: `_phase2/playbook_T2_STAND.md`, `_phase2/playbook_T3_PROVE.md`, `_phase2/playbook_T4_DEW.md`, `_phase2/playbook_T5_CHECK.md`, `_phase2/playbook_T6_SPOT.md`, `_phase2/playbook_T7_BUILD.md`, `_phase2/playbook_T8_WEAVE.md` (and `playbook_T1_MARK.md` if present)

**Interfaces:** documentation only; no code. Each playbook gets a new "## Retrieval + item rules (LS feedback 2026-07)" section.

- [ ] **Step 1: Add to EACH playbook** a section stating, in that archetype's terms:
  - The cadence ceiling for this archetype (concept T1/T2/T3/T4/T6 = 3, tighten to 2 after a named tool; checking T5 = 2; build T7/T8 = 4 at milestones). Reference `gate_check_cadence`.
  - **4 options per discrimination, each a named misconception** (never filler). Reference `gate_structural_item`.
  - **Diagnosis = student answers the check, then improves** (coping-model demo may pre-answer a PROVIDED draft, but must be followed by an independent turn). Reference `gate_self_answered_check`.
  - **No comma before "because"/"so" in fill-in frames**; use `claim_frame()`. Reference `gate_frame_comma`.
  - **Re-gloss HARD_TERMS** (controlling idea, warrant, synthesis, counterclaim): the `gate_define_before_use` gate ALREADY requires an in-lesson gloss for these (they are in `_TECH_TERMS`), so this is enforced, not optional. Playbook nuance (#9, LS): prefer a BRACKETED gloss right after the term on re-introduction in a later lesson (the gate accepts any definitional cue, but brackets are the LS-requested style). Reference `gate_define_before_use`.
  - **Stem wording (#7):** name the move directly ("Which sentence explains?"), not meta-phrasings ("which fits the verb"). [playbook-only]
  - **Tone (#5/Yeager):** state the standard up front; per-choice reveal uses wise-feedback (no person-praise). [playbook-only]
  - **Pair a stand-alone improve-write with a predict_the_fix (#4)** where feasible. [playbook-only]
  - **Cross-lesson spacing note (#3/KH):** the in-lesson gate is not sufficient; the same tools must recur in later lessons (sequence-builder concern).

- [ ] **Step 2: Commit**
```bash
git add "Alpha HS Writing Course 2026-27/_phase2/playbook_T2_STAND.md" "Alpha HS Writing Course 2026-27/_phase2/playbook_T3_PROVE.md" "Alpha HS Writing Course 2026-27/_phase2/playbook_T4_DEW.md" "Alpha HS Writing Course 2026-27/_phase2/playbook_T5_CHECK.md" "Alpha HS Writing Course 2026-27/_phase2/playbook_T6_SPOT.md" "Alpha HS Writing Course 2026-27/_phase2/playbook_T7_BUILD.md" "Alpha HS Writing Course 2026-27/_phase2/playbook_T8_WEAVE.md"
git commit -m "docs(playbooks): encode LS-feedback retrieval + item rules per archetype (L2)"
```

---

### Task 9: Pilot lesson 1 — G9 L01 `arguable_claim` (bring to full compliance)

**Files:**
- Modify: `Lesson_Bank_G9/lesson_g9_l01_arguable_claim_v3_1.py`

**Interfaces:** consumes all Task 2-7 gates; this lesson must end clean on ALL gates including the new ones.

- [ ] **Step 1: Run the lesson's own QC to see every new-gate failure** — `python "Alpha HS Writing Course 2026-27/Lesson_Bank_G9/lesson_g9_l01_arguable_claim_v3_1.py"` and note each new blocker (frame_comma, discrimination option counts, cadence, self_answered_check, re-gloss).
- [ ] **Step 2: Fix #2 (frame comma)** — replace the hand-written `[your side], because` frame with `claim_frame(...)` or drop the comma. No fabricated content.
- [ ] **Step 3: Fix #8 (4 options)** — for each 3-option discrimination in this lesson, author a 4th option that is a NAMED MISCONCEPTION (a real wrong-move a G9 student makes), with its `why`. Preserve single-key, minimal-pair structure, no lone-longest key (`gate_distractor_length_cue`).
- [ ] **Step 4: Fix #6 (answer-then-improve)** — convert the "Check and fix a weak draft with the 3 questions" diagnosis so the student ANSWERS the checks (as a discrimination/predict checkpoint, or an explicit own-turn), not reads pre-answered ones.
- [ ] **Step 5: Fix #3 (cadence)** — tag buy-in cards `tag="buy_in"`, tag the "3-question test" card `tag="memorizable_tool"`, and insert a checkpoint where a run exceeds the ceiling. Do not split a worked example.
- [ ] **Step 6: Verify** — `python pipeline/tier_a_regression.py G9 2>&1 | grep C901-0001` → clean; the lesson passes ALL gates. `python -m pytest pipeline/tests/ -q` green.
- [ ] **Step 7: Render for review** — `python pipeline/render_course_preview_grade.py G9 --deploy c:/tmp/ls_pilot --base-url http://localhost` (local; not published). Note the output path.
- [ ] **Step 8: Commit**
```bash
git add "Alpha HS Writing Course 2026-27/Lesson_Bank_G9/lesson_g9_l01_arguable_claim_v3_1.py"
git commit -m "content(g9): pilot L01 to full LS-feedback compliance (#2,#3,#6,#8)"
```

---

### Task 10: Pilot lesson 2 — G9 L03 `controlling_idea` (adds #7 + #9 coverage)

**Files:**
- Modify: `Lesson_Bank_G9/lesson_g9_l03_controlling_idea_v3_1.py` (confirm exact filename with `ls Lesson_Bank_G9/ | grep l03`)

- [ ] **Step 1: Run its QC**, note new-gate failures (expect: 4-option, cadence, plus #9 re-gloss of "controlling idea" and #7 odd stem wording).
- [ ] **Step 2: Fix #9** — ensure "controlling idea" is re-glossed in-lesson (a `_DEF_CUE` definition on first use here).
- [ ] **Step 3: Fix #7** — reword any "which fits the verb" style stems to name the move ("Which sentence explains?").
- [ ] **Step 4: Fix #8, #6, #3, #2** as in Task 9 for this lesson's instances.
- [ ] **Step 5: Verify** — `tier_a_regression G9` clean for C905-0004 (confirm the id); full pytest green.
- [ ] **Step 6: Render for review** (same local deploy dir as Task 9).
- [ ] **Step 7: Commit**
```bash
git add "Alpha HS Writing Course 2026-27/Lesson_Bank_G9/lesson_g9_l03_controlling_idea_v3_1.py"
git commit -m "content(g9): pilot L03 to full LS-feedback compliance (#2,#3,#6,#7,#8,#9)"
```

**STOP — human review gate.** Open both pilot lessons before/after for Noel. Do NOT proceed to Task 11 (course-wide rollout) until Noel signs off on the pilot voice + the gate behavior.

---

### Task 11: Gated course-wide rollout (AFTER pilot sign-off)

**Files:** all remaining lessons flagged by the new gates (esp. the ~118 3-option discriminations for #8).

**Interfaces:** the new gates ARE the worklist; `tier_a_regression.py {G9,G10,G11,G12}` emits the exact failing lessons per gate.

- [ ] **Step 1: Produce the worklist** — run all four grades; capture every failing lesson+gate into a checklist. Group by gate.
- [ ] **Step 2: #8 4th-distractor pass (largest)** — dispatch parallel subagents (per the subagent-driven-development skill), one batch per lesson-cluster, each authoring a named-misconception 4th option for every 3-option discrimination in its files. Each agent: preserve single-key + minimal-pair + no-lone-longest-key + no-em-dash + no-fabrication; run the lesson's QC to green before returning. Cap ~4 lessons/agent.
- [ ] **Step 3: The cheaper fixes (#2/#3/#6/#9)** — targeted edits across the flagged lessons (can run in the same agent wave, per file).
- [ ] **Step 4: Full verification + REMOVE the in-flight allowlist** — `python pipeline/tier_a_regression.py {G9,G10,G11,G12}` ALL clean (no new-gate failures remain). Then in `pipeline/tests/test_tier_a_regression.py` empty `_INFLIGHT_GATES = ()` (the allowlist added during the gate-build phase, Tasks 2-6, so the course-clean invariants tolerated known-but-not-yet-fixed gate flags) and confirm `test_g9_is_fully_clean` + `test_non_fact_verify_floor_is_clean_course_wide` now pass with a genuinely-clean course. `python -m pytest pipeline/tests/ -q` green; re-run the S1 recognition detector + option sweeps to confirm no regressions introduced.
- [ ] **Step 5: Update the ledger + fix plan** — mark the LS-feedback items done in `COURSE_FIX_PLAN_synthesis.md`; log the #4/#5 external-app items.
- [ ] **Step 6: Commit per grade** (atomic per-grade commits).

---

### Task 12: Cross-lesson spacing note (KH caveat) — sequence-builder flag, not a gate

**Files:**
- Modify: `pipeline/course_sequence_g9_12.py` (a documented note) OR `SIM_STUDENT_FINDING_LEDGER.md`

- [ ] **Step 1:** Record the council's grade-A caveat: the in-lesson cadence gate is necessary but not sufficient; the same taught tools must be retrieved in LATER lessons (spacing g=0.74), which is a sequence-builder responsibility. This is a flag for a future spacing/interleaving pass, not built here.
- [ ] **Step 2: Commit** the note.

## Self-Review notes (author)
- **Sequencing hazard handled:** gates that fail existing lessons (frame_comma #2, four-options #8, cadence #3, self-answered #6, re-gloss #9) land in Tasks 2-8 and WILL turn `tier_a_regression` red on legacy lessons between Task 2 and Task 11. This is intended (the red IS the worklist), but it means the "full pytest green / grade clean" checks in Tasks 2-8 verify the GATE'S FIXTURES + the pilot, not the whole course. The whole course only returns green at Task 11 Step 4. Every task's verify step is scoped accordingly (fixtures + named lesson, not course-wide) to avoid a false "done."
- **Tagging surface is small by design:** archetype is DERIVED from lesson_type (no tagging); only buy-in + memorizable-tool cards need an explicit `tag` (a handful per lesson), so the "tagging integrity" risk the council flagged is bounded — untagged cards default to the safe "counted, ordinary" behavior.
- **#8 is the cost center:** ~118 items need a quality 4th distractor; that is the bulk of Task 11 and is deliberately gated behind pilot sign-off.
- **Not built (logged):** embedded-question video (#5) and answer-adaptive reveal (#4 full form) → external-app/PCI track; test-out UX (#5/Yeager) → product enhancement; cross-lesson spacing → sequence-builder (Task 12 flag).
