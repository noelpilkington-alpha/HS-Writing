# Cross-Grade Sentence-Progression + Course-Arc Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce two source-verified design artifacts: (1) the cross-grade G9-12 sentence-skill progression map (inherited-vs-new, two layers, every cell justified against 4 sources), and (2) the course-arc architecture doc it implies (per-grade phase sequence + retrieval-gate prerequisite declarations).

**Architecture:** This is a RESEARCH + DESIGN deliverable, not software. Each task VERIFIES a slice of the provisional map against the four authoritative sources, records the citation + verdict, and escalates genuine conflicts to a narrow council. The output is Markdown docs + one machine-readable prerequisite table, committed. No lesson regeneration, no gate code (those are follow-on specs).

**Tech Stack:** Markdown design docs; one Python data module (`course_sequence_g10_12.py`) that encodes the verified map + prerequisites as importable data (so later gate code + the generator read ONE source of truth, not prose). Verification uses the existing repo docs + persona files (read, cite); the council uses the council-of-writing-instruction skill only where sources conflict.

## Global Constraints

- **Every map cell (NEW/INHERITED, per skill, per grade) must carry a citation** to at least one of the 4 sources: the crosswalk (`skills_by_grade_crosswalk.html` / `TestDesign_Reference.md`), TWR sequence (`personas/01-twr-hochman-wexler.md`), CCSS/ACC grade bands (`05_AlphaCommonCore_Writing_Spine.md` / `01_ccss_adherence_map.md`). No cell asserted from intuition.
- **Council only on genuine conflict.** If the crosswalk, TWR, and standards AGREE on a placement, record the consensus and move on (do not convene). Convene a narrow council (TWR + KH + the relevant seat) ONLY where two sources give different grade placements for the same skill.
- **The draft map in the spec is a HYPOTHESIS, not the answer.** A task may move a skill's grade if the sources say so; record the change + why.
- **No em dashes** in authored doc prose (house rule; use commas/colons/parens).
- **Scope fence:** deliver the map + arc + the prerequisite data module ONLY. Do NOT write gate code, do NOT regenerate/re-scope lessons, do NOT generate course lessons. Those are explicitly downstream (spec non-goals).
- All artifacts live in `Alpha HS Writing Course 2026-27/`. Spec of record: `docs/superpowers/specs/2026-07-08-cross-grade-sentence-progression-and-course-arc.md`.

## File Structure

- `Alpha HS Writing Course 2026-27/Sentence_Progression_G9-12.md` (NEW) — the verified map: both layers, all four grades, each cell with NEW/INHERITED + citation + verdict. The human-readable authoritative artifact.
- `Alpha HS Writing Course 2026-27/Course_Arc_G9-12.md` (NEW) — the per-grade course arc (Layer-1 phase -> per-genre Layer-2 sentence -> paragraph phase -> essay/composite phase) + each grade's explicit inherited-skill prerequisite list.
- `Alpha HS Writing Course 2026-27/pipeline/course_sequence_g9_12.py` (NEW) — machine-readable encoding: `SKILL_OWNERSHIP` (skill -> owning grade + layer), `INHERITED_BY_GRADE` (grade -> skills to retrieval-gate), `COURSE_PHASES` (grade -> ordered phase list). Dependency-free; a self-test asserts internal consistency (no skill both new and inherited at the same grade; every inherited skill is owned by an earlier grade). This is the single source of truth later gate code + the generator import.
- `Alpha HS Writing Course 2026-27/course_arc_g9_12.html` (NEW) — browsable render of the arc + map for review.

**Task order:** verify Layer 1 (Task 2) and Layer 2 (Task 3) map cells -> resolve conflicts via council (Task 4, conditional) -> author the map doc (Task 5) -> author the arc doc + prerequisites (Task 6) -> encode the machine-readable module + self-test (Task 7) -> render for review (Task 8). Task 1 assembles the source evidence all later tasks cite.

---

## Task 1: Assemble the source-evidence sheet

**Files:**
- Create: `Alpha HS Writing Course 2026-27/_evidence/sentence_skill_sources.md` (a working evidence sheet, not a deliverable)

**Interfaces:**
- Consumes: `skills_by_grade_crosswalk.html`, `TestDesign_Reference.md`, `personas/01-twr-hochman-wexler.md`, `05_AlphaCommonCore_Writing_Spine.md`, `01_ccss_adherence_map.md`.
- Produces: for each sentence skill (both layers), a row recording what EACH of the 3 documentary sources says about its grade placement (verbatim-cited), so Tasks 2-3 rule from evidence, not memory.

- [ ] **Step 1: Extract the crosswalk's per-grade SR/sentence tags**

Read `skills_by_grade_crosswalk.html` (strip tags) and `TestDesign_Reference.md`. For each grade G9-G12, list every sentence-level / conventions / knowledge-of-language skill the crosswalk marks TESTED or LADDER at that grade, with the naming systems. Record verbatim (own-words summary + the systems named).

- [ ] **Step 2: Extract TWR's skill sequence**

Read `personas/01-twr-hochman-wexler.md`. List TWR's documented sentence-skill ordering (kernel -> expansion -> combining -> subordinating conjunctions -> appositives -> transitions -> SPO), with the loc citations. Note which TWR marks as "Level 1" (novice) vs "Level 2" (advanced) since that is TWR's own grade-agnostic difficulty signal.

- [ ] **Step 3: Extract the CCSS/ACC grade-band expectations**

Read `05_AlphaCommonCore_Writing_Spine.md` + `01_ccss_adherence_map.md`. Record the CONV.1-3 / Language-strand grade-band expectations (CCSS L.9-10 vs L.11-12; ACC CONV codes), which give the standards' own grade boundary.

- [ ] **Step 4: Write the evidence sheet**

Create `_evidence/sentence_skill_sources.md` as a table: one row per sentence skill, columns = [skill, crosswalk says, TWR says, standards say]. Every cell cites its source. Leave a blank "verdict" column for Tasks 2-3.

- [ ] **Step 5: Commit**

```bash
git add "Alpha HS Writing Course 2026-27/_evidence/sentence_skill_sources.md"
git commit -m "docs(progression): assemble source-evidence sheet for sentence-skill grade placement"
```

---

## Task 2: Verify the Layer-1 (genre-general mechanics) cells

**Files:**
- Modify: `Alpha HS Writing Course 2026-27/_evidence/sentence_skill_sources.md` (fill the verdict column for Layer-1 skills)

**Interfaces:**
- Consumes: the evidence sheet (Task 1).
- Produces: a NEW/INHERITED grade verdict for each Layer-1 mechanics skill (expansion, combining, appositives, subordinating conjunctions, fragment/run-on/comma-splice, because/but/so, parallelism, modifier placement, concision/precision, rhetorical syntax, AP sophistication syntax), plus a `CONFLICT` flag where the 3 sources disagree.

- [ ] **Step 1: Rule each Layer-1 skill's owning grade**

For each Layer-1 skill, compare the three source cells. Assign the owning grade = the earliest grade where the sources agree it is TESTED or expected. Record verdict: `NEW @ G<n>` + one-line justification citing the sources. Mark `CONFLICT` if crosswalk and standards disagree by a grade (e.g. one source puts parallelism at G10, another at G11).

- [ ] **Step 2: Check the draft-map hypothesis against the verdicts**

Compare your verdicts to the spec's draft Layer-1 table. For each cell that MOVED from the draft, note the move + why. Confirm or refute the spec's key claim that "G10 has almost no new Layer-1 mechanics."

- [ ] **Step 3: Record verdicts in the evidence sheet + list conflicts**

Fill the verdict column for all Layer-1 rows. At the bottom, list every `CONFLICT` row (these feed Task 4).

- [ ] **Step 4: Commit**

```bash
git add "Alpha HS Writing Course 2026-27/_evidence/sentence_skill_sources.md"
git commit -m "docs(progression): verify Layer-1 mechanics grade placements against sources"
```

---

## Task 3: Verify the Layer-2 (genre-specific sentence-move) cells

**Files:**
- Modify: `Alpha HS Writing Course 2026-27/_evidence/sentence_skill_sources.md` (fill the verdict column for Layer-2 skills)

**Interfaces:**
- Consumes: the evidence sheet (Task 1) + Layer-1 verdicts (Task 2).
- Produces: a NEW/INHERITED grade verdict for each Layer-2 genre-sentence move (claim sentence, nuanced/counterclaim-aware claim, attributed-evidence sentence, controlling-idea sentence, device->effect->warrant sentence, cross-source/synthesis sentence, rhetorical-analysis sentence, AP-level moves), each tied to the grade its GENRE enters per the reconciled spine.

- [ ] **Step 1: Map each genre-sentence move to the grade its genre enters**

Read `G9-12_Course_Spines_RECONCILED.md` for which genres are tested at which grade (argument+explanatory @ G9-10; analysis @ G10; synthesis+rhetorical-analysis @ G11; AP @ G12). Assign each Layer-2 move `NEW @ G<n>` = the grade its genre first demands it. Cite the spine + crosswalk.

- [ ] **Step 2: Confirm the two spec findings**

Confirm/refute: (a) the nuanced/counterclaim-aware claim and the device->effect->warrant sentence are G10-NEW (analysis enters at G10); (b) the cross-source sentence is G11-NEW. Note any move.

- [ ] **Step 3: Record verdicts + conflicts, commit**

Fill the verdict column for Layer-2 rows; add any `CONFLICT` rows to the conflict list.

```bash
git add "Alpha HS Writing Course 2026-27/_evidence/sentence_skill_sources.md"
git commit -m "docs(progression): verify Layer-2 genre-sentence grade placements against sources"
```

---

## Task 4: Council-adjudicate conflicts (CONDITIONAL - only if Task 2/3 flagged any)

**Files:**
- Modify: `Alpha HS Writing Course 2026-27/_evidence/sentence_skill_sources.md` (resolve CONFLICT rows)

**Interfaces:**
- Consumes: the `CONFLICT` list from Tasks 2-3.
- Produces: a resolved grade verdict for each conflicted skill, with the council's adjudication recorded.

- [ ] **Step 1: If there are ZERO conflicts, skip this task**

If Tasks 2-3 produced no `CONFLICT` rows, write "no conflicts; all placements are source-consensus" in the evidence sheet and skip to Task 5. (Do NOT convene the council on consensus - that violates the council guardrail.)

- [ ] **Step 2: Convene a narrow council on the conflicted placements only**

For the conflicted skills only, invoke the council-of-writing-instruction skill in design mode with `--seats twr,kirschner-hendrick` plus the relevant genre seat, asking ONLY: "at which grade should skill X be taught as new, given source A says G<a> and source B says G<b>?" The judge adjudicates by evidence strength, names the winner.

- [ ] **Step 3: Record each resolution + commit**

Write the resolved grade + the council's reasoning into the evidence sheet for each conflict.

```bash
git add "Alpha HS Writing Course 2026-27/_evidence/sentence_skill_sources.md"
git commit -m "docs(progression): council-adjudicate conflicted sentence-skill placements"
```

---

## Task 5: Author the verified progression map

**Files:**
- Create: `Alpha HS Writing Course 2026-27/Sentence_Progression_G9-12.md`

**Interfaces:**
- Consumes: the fully-verified evidence sheet (Tasks 1-4).
- Produces: the authoritative map doc: two tables (Layer 1, Layer 2), each with columns [skill, NEW @ grade, INHERITED at grades, source citation]. This is the human-readable single source of truth for the skill-by-grade progression.

- [ ] **Step 1: Write the two verified tables**

Transcribe the verified verdicts into two clean tables (Layer 1 mechanics, Layer 2 genre-sentences). Each row: the skill, the grade it is NEW, the grades that INHERIT it (retrieval-gate), and the source citation. Add a short header stating the basis (4-source triangulation) and that these cells are now VERIFIED (not the spec's provisional draft).

- [ ] **Step 2: Write the "what changed from the draft" note**

A short section listing every cell that moved from the spec's provisional draft, with the source reason. If nothing moved, say so.

- [ ] **Step 3: Verify internal consistency by hand**

Check: no skill is marked NEW at two grades; every INHERITED entry points to a grade that OWNS it earlier; G9 has no inherited Layer-1 mechanics (entry grade). Fix any contradiction.

- [ ] **Step 4: Commit**

```bash
git add "Alpha HS Writing Course 2026-27/Sentence_Progression_G9-12.md"
git commit -m "docs(progression): author verified G9-12 sentence-skill progression map"
```

---

## Task 6: Author the course-arc doc + per-grade prerequisites

**Files:**
- Create: `Alpha HS Writing Course 2026-27/Course_Arc_G9-12.md`

**Interfaces:**
- Consumes: the verified map (Task 5) + the reconciled spine (`G9-12_Course_Spines_RECONCILED.md`).
- Produces: the per-grade course arc (Layer-1 phase -> per-genre [Layer-2 sentence -> paragraph phase] -> essay/composite phase) AND each grade's explicit inherited-skill prerequisite list (what to retrieval-gate at entry).

- [ ] **Step 1: Write the arc for each grade**

For G9, G10, G11, G12, write the ordered phase list per the spec's Section-D template, populated with THAT grade's new skills from the map. State, per grade, which genres run and in what order. Explicitly mark G10's Layer-1 phase as thin (per the verified finding).

- [ ] **Step 2: Write each grade's inherited-skill prerequisite declaration**

For each grade, list the skills it INHERITS (from the map) that must be retrieval-gated at entry, and for each, name the grade that owns it (the remediation-routing target, which may be >1 grade down).

- [ ] **Step 3: Write the ordering law + the composite-exception note**

State the ordering law (no lesson before the phase teaching its prerequisites) and the note that essay-assembly/synthesis internal rungs are composing-process steps assuming prior paragraph fluency, not unit re-teaching.

- [ ] **Step 4: Commit**

```bash
git add "Alpha HS Writing Course 2026-27/Course_Arc_G9-12.md"
git commit -m "docs(arc): author G9-12 course arc + per-grade retrieval-gate prerequisites"
```

---

## Task 7: Encode the machine-readable course-sequence module

**Files:**
- Create: `Alpha HS Writing Course 2026-27/pipeline/course_sequence_g9_12.py`

**Interfaces:**
- Consumes: the verified map (Task 5) + arc (Task 6).
- Produces: importable data + a self-test:
  - `SKILL_OWNERSHIP: dict[str, dict]` — skill_id -> `{"grade": "G<n>", "layer": 1|2, "genre": str|None}`
  - `INHERITED_BY_GRADE: dict[str, list[str]]` — grade -> skill_ids to retrieval-gate at entry
  - `COURSE_PHASES: dict[str, list[str]]` — grade -> ordered phase labels
  - `owning_grade(skill_id) -> str`, `is_new_at(skill_id, grade) -> bool`, `inherited_at(grade) -> list[str]`

- [ ] **Step 1: Write the failing self-test**

Create the file with ONLY this `__main__` (module body empty), so it fails first:

```python
if __name__ == "__main__":
    # every inherited skill must be OWNED by an earlier grade (no forward/self inheritance)
    order = {"G9": 0, "G10": 1, "G11": 2, "G12": 3}
    for grade, skills in INHERITED_BY_GRADE.items():
        for sk in skills:
            own = SKILL_OWNERSHIP[sk]["grade"]
            assert order[own] < order[grade], f"{sk} inherited at {grade} but owned at {own} (not earlier)"
    # no skill is 'new' at two grades: ownership is single-valued (dict enforces) - assert each is reachable
    for sk, meta in SKILL_OWNERSHIP.items():
        assert meta["grade"] in order, f"{sk} has bad owning grade {meta['grade']}"
        assert meta["layer"] in (1, 2)
    # G9 (entry) inherits no Layer-1 mechanics
    g9_inh = INHERITED_BY_GRADE.get("G9", [])
    assert not any(SKILL_OWNERSHIP[s]["layer"] == 1 for s in g9_inh), "G9 should inherit no Layer-1 mechanics"
    # helpers agree with the data: for every skill, is_new_at is True at its owning grade and False elsewhere
    for sk, meta in SKILL_OWNERSHIP.items():
        assert is_new_at(sk, meta["grade"]), f"is_new_at wrong for {sk} at its owning grade"
        for g in order:
            if g != meta["grade"]:
                assert not is_new_at(sk, g), f"is_new_at should be False for {sk} at {g}"
        assert owning_grade(sk) == meta["grade"]
    # every grade that inherits a skill returns it from inherited_at
    for grade, skills in INHERITED_BY_GRADE.items():
        assert set(inherited_at(grade)) == set(skills)
    print("course_sequence_g9_12 self-test PASS")
    import sys; sys.exit(0)
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd "c:/Users/noelp/HS Writing/Alpha HS Writing Course 2026-27" && python pipeline/course_sequence_g9_12.py`
Expected: FAIL (`NameError: INHERITED_BY_GRADE`).

- [ ] **Step 3: Encode the verified data + helpers**

Above the `__main__`, write the module docstring, then `SKILL_OWNERSHIP`, `INHERITED_BY_GRADE`, `COURSE_PHASES` populated EXACTLY from the verified map (Task 5) and arc (Task 6) - not from the spec's provisional draft. Then:

```python
def owning_grade(skill_id: str) -> str:
    return SKILL_OWNERSHIP[skill_id]["grade"]

def is_new_at(skill_id: str, grade: str) -> bool:
    return SKILL_OWNERSHIP[skill_id]["grade"] == grade

def inherited_at(grade: str) -> list[str]:
    return list(INHERITED_BY_GRADE.get(grade, []))
```

- [ ] **Step 4: Run to verify it passes**

Run: `python pipeline/course_sequence_g9_12.py`
Expected: `course_sequence_g9_12 self-test PASS`, exit 0. Fix any consistency failure (they indicate a real contradiction between the map and arc - reconcile in the docs too).

- [ ] **Step 5: Commit**

```bash
git add "Alpha HS Writing Course 2026-27/pipeline/course_sequence_g9_12.py"
git commit -m "feat(progression): machine-readable G9-12 course-sequence data + consistency self-test"
```

---

## Task 8: Render the map + arc for review

**Files:**
- Create: `Alpha HS Writing Course 2026-27/pipeline/render_course_arc.py`
- Create (generated): `Alpha HS Writing Course 2026-27/course_arc_g9_12.html`

**Interfaces:**
- Consumes: `course_sequence_g9_12.py` (imports the verified data - so the render cannot drift from the source of truth).
- Produces: a browsable HTML showing, per grade, the phase arc + the inherited-vs-new skill map, color-coded by layer, with the source citations.

- [ ] **Step 1: Write the renderer**

Create `render_course_arc.py` that imports `course_sequence_g9_12` and renders: (a) a G9-G12 columns view of the sentence-skill map (NEW cells highlighted, INHERITED cells muted with a "retrieval-gate" tag), and (b) each grade's phase arc as an ordered list. Match the house style (the `--accent` purple etc. used by the other renders). Read data live from the module.

- [ ] **Step 2: Run + confirm content**

Run: `python pipeline/render_course_arc.py`
Expected: writes `course_arc_g9_12.html`; grep-confirm every grade G9-G12 appears and both layers render.

- [ ] **Step 3: Commit**

```bash
git add "Alpha HS Writing Course 2026-27/pipeline/render_course_arc.py" "Alpha HS Writing Course 2026-27/course_arc_g9_12.html"
git commit -m "feat(progression): browsable G9-12 course-arc + progression-map render"
```

---

## Deferred to follow-on specs (explicitly NOT in this plan)
- The gate-code redesign (`gate_unit_ladder` -> one-unit-per-lesson; `gate_type_ceiling` -> course-phase ordering; the retrieval-gate check). A separate spec after this map is reviewed.
- Re-scoping the existing G10 lessons (T6 shrink, T2 refocus) against the verified arc.
- Generating the full G9-12 course from the arc (the seed run).
- Cut scores / field-test efficacy (needs student data).
