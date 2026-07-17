# Primary-Source Provenance for the HS Writing BrainLift Knowledge Tree — Design

**Date:** 2026-07-17
**Status:** Approved (design), ready for implementation plan.
**Author context:** follows the BrainLift audit + the artifact-consolidation spreadsheet. This design does the inverse of the spreadsheet: it points the Knowledge Tree *up* to primary sources instead of *sideways* to the derived artifact files.

---

## Problem

The "HS Writing Course Design Brainlift — Stakeholder Edition" Knowledge Tree (Categories 1–7) cites **derived artifact files** (`05_AlphaCommonCore_Writing_Spine.md`, `KC_Map_and_Unit_Arch_G9-12.md`, etc.) as its Sources. Those files are **research outputs**, not sources — they are the knowledge we compiled, not the ground truth we compiled it from. For a **provenance/audit trail**, a claim resting on "our own compiled file" is not defensible; it must rest on an authoritative external source or a published expert.

## Goal

Rewrite the Knowledge Tree so each category's `Sources:` cite **primary sources**, creating a defensible chain: *design claim → research → authoritative source*. A standalone **Primary Source Register** becomes the audit artifact the tree points into.

## Locked decisions (from brainstorming)

1. **Purpose:** provenance/audit trail (not portability, not authoring-context). The chain must be defensible to an auditor (e.g. HOA/academics).
2. **Valid source types — TWO only:**
   - **External authorities** — state-DOE standards pages/PDFs, test-vendor blueprints & rubrics (STAAR/AP/SBAC/ACT/NAEP/Regents), released test forms.
   - **Published experts** — the 17 named researchers/publications already in the BrainLift's Experts section (TWR, SRSD, DI, UbD, McCutchen, Hayes & Flower, etc.).
   - **NOT citable as sources:** internal decisions (council rulings, the KC scheme) and conversation/research-run provenance. These may appear as *labels/back-pointers*, never as a "source."
3. **Design bets** (e.g. discrimination-before-production, the plans:essays ratio): cite the **expert the bet derives from** AND **keep the honest grade label** ("Grade-C / design bet, unvalidated for writing"). No laundering a bet into an evidence claim (honors BrainLift Insight 3).
4. **Register granularity: category-representative** — for each category, the handful of *load-bearing* primary sources that actually drive its claims (~4–8 per category, ~35–45 total), NOT an exhaustive harvest of all ~200 embedded URLs.
5. **Unrecoverable-file handling: Approach B (close the gap).** The two zero-URL compilation files (`03_state_assessment_format_map.md`, `TestDesign_Reference.md`) get a targeted pass that attaches a **live authoritative source to each load-bearing claim**, via sibling-recovery then targeted web-fetch. C (record the gap) is the documented fallback ONLY where B genuinely fails after a real attempt — not the default.
6. **Edit target:** the **`.docx` copy** at `Brainlifts/HS Writing Course Design Brainlift - Stakeholder Edition.docx` (in the course folder). The original `.md` at `Writing_Brainlift/HS Writing Course Design Brainlift - Stakeholder Edition.md` is **left untouched**.

## Source-recoverability findings (why the design is shaped this way)

Embedded-URL counts across the cited derived files (measured):

| File | URLs | Provenance type |
|---|---|---|
| `01_ccss_adherence_map.md` | 51 | Research-compilation — sources embedded (state DOEs) |
| `04_item_formats_and_rubrics.md` | 41 | Research-compilation — sources embedded (vendor blueprints/rubrics) |
| `AnchorSets/G10_anchor_forms.md` | 55 | Research-compilation — released forms |
| `AnchorSets/G11_anchor_AP_Lang.md` / `_SBAC.md` / `_ACT.md` | 21 / 17 / 5 | Research-compilation |
| `02_deviation_states_deepdive.md` | 16 | Research-compilation |
| `06a/06b/06c_deviation_*.md` | 4 / 7 / 4 | Research-compilation |
| `03_state_assessment_format_map.md` | **0** | **Second-order compilation** (from 01/02/04 + released forms) → **B pass** |
| `TestDesign_Reference.md` | **0** | **Second-order compilation** (from `ReleasedTests/` batches) → **B pass** |
| `TestBank_Blueprint.md` | 0 | Internal spec (derives from the above) |
| `KC_Map_and_Unit_Arch_G9-12.md`, `LESSON_DESIGN_PLAN.md`, `G10_Model_Lesson_Specs.md`, `syntactic-moves-crosswalk.md`, `Sentence_Progression_G9-12.md`, `lesson_contract.py` | 0 | **Original synthesis / design** — primary sources are the 17 EXPERTS + labeled internal bets |

**Consequence, by category:**
- **Categories 1–2** (Standards Backbone, Exam Ground Truth) → route to **external authorities** (URLs already embedded in 01/02/04/06/anchors, plus the B-pass live URLs for 03/TestDesign).
- **Categories 3–7** (Move decomposition, Lesson Contract, Fading/Transfer/Calibration, Scope, Progression) → route mostly to **published experts** (TWR, DI, SRSD, McCutchen, Hayes & Flower, UbD, K&H, Wiliam & Hattie), with the design-bet claims carrying the derived-from expert + grade label.

## Deliverables (3)

### D1 — `BrainLift_Primary_Source_Register.md` (new; the audit artifact)
Location: course root (`Alpha HS Writing Course 2026-27/`).
Organized by the 7 Knowledge-Tree categories. Each entry:

> **Source** — the authority or expert publication
> **Type** — `Authority` | `Expert`
> **Grounds** — the specific claim / SPOV / category insight it supports
> **Reachable via** — a live URL (authorities) or full citation (experts)
> **Compiled into** — the derived artifact(s) it flows through (back-pointer, explicitly labeled "artifact, not source")

- Category-representative: ~4–8 load-bearing entries per category.
- A dedicated sub-block records the **B-pass results** for `03` / `TestDesign` claims (each load-bearing claim → its recovered live authority). Any claim that fails recovery after a real attempt is listed with an explicit gap note (documented C fallback).
- The register is the single place an auditor reads to verify the whole tree.

### D2 — Rewritten Knowledge Tree `Sources:` lists (edit the `.docx`)
For each of Categories 1–7 in the `.docx`, replace the `Sources:` list:

> **Sources (primary):** [authority / expert] · [authority / expert] … *— Compiled in: `artifact.md` (see Primary Source Register).*

- Primary sources lead; the artifact survives only as the "Compiled in" tail-note.
- Design-bet claims: cite the derived-from expert **and retain the grade label** verbatim.
- Category **Insights (DOK 3)** and the **Summary** prose are left as-is unless a sentence explicitly names a file as a *source* (then reworded to name the source, file demoted to back-pointer).
- **Out of scope for edits:** the Experts, Spiky POV, Research Insights, Timeback-vs-AlphaWrite, and Next Steps sections. The Spiky POVs already cite artifacts inline with line numbers; those are left untouched in this pass (a later pass may reconcile them — noted, not done).

### D3 — Source-first spreadsheet
Reorient the existing `BrainLift_Knowledge_Tree_Sources.xlsx` (+ `.csv`):
- Lead column = **Primary Source** (authority/expert); supporting column = the artifact(s) it feeds.
- Becomes the machine-readable twin of the register (same rows, source-first ordering).
- Keep the original artifact-first sheet as a second tab (so the earlier consolidation isn't lost).

## The B pass (feeds D1 + D2)

Scoped to the **load-bearing claims** of `03_state_assessment_format_map.md` and `TestDesign_Reference.md` (the grade→exam mapping, per-state assessment formats, rubric trait/scale facts). Per claim, in order:
1. **Sibling-recover (free):** if an authoritative URL for the claim already exists in `01`/`02`/`04`/`06`/anchor sets, cite it.
2. **Targeted web-verify:** for claims with no home URL anywhere in the tree, fetch the authoritative source (state DOE assessment page / vendor blueprint) and attach the live link.
3. **Document the gap (fallback):** if genuinely unrecoverable after a real fetch attempt, record it in the register as "traces to [authority] via [parent]; live URL not recovered [date/reason]."

This is NOT an exhaustive URL harvest — it targets the claims those two files uniquely assert.

## Explicitly out of scope
- No edits to lessons, pipeline, standards content, or the grader.
- No exhaustive harvest of all embedded URLs (category-representative only).
- No rewrite of non–Knowledge-Tree sections of the BrainLift.
- No edit to the original `.md` BrainLift.

## Success criteria
1. Every Knowledge-Tree category in the `.docx` cites primary sources (authorities and/or experts) with artifacts demoted to back-pointers.
2. The Primary Source Register exists, is category-organized, and every register entry resolves to a live URL or a full expert citation (or a documented gap).
3. The two zero-URL files' load-bearing claims each have an attached authoritative source (or a documented gap) via the B pass.
4. Every design-bet claim retains its honest grade label — no bet is laundered into an evidence claim.
5. The original `.md` BrainLift is unchanged; the spreadsheet is reoriented source-first with the artifact-first view preserved.

## Risks / open notes
- **Web reachability (B pass):** some state-DOE links rot; the design accepts documented gaps rather than blocking on them.
- **Expert-citation exactness:** the Experts section already gives publication + venue for all 17; the register reuses those verbatim to avoid drift.
- **Spiky-POV inline file cites** remain (line-numbered references to artifacts); reconciling them is a possible follow-up, deliberately not in this pass.
