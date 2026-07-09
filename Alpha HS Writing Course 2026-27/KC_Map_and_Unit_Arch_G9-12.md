# G9-12 Writing KC Map + Unit Architectures (GAP-SCOPED, RECONCILED)

**Status:** DRAFT for review. Reconciles the prior KC scheme (`A1/A2/B1L/B2_Lesson_Map.md`, 68 KCs) with the gap-scoped roster (`Sentence_Skill_Roster_FINAL.md`) + app-ownership gap analysis (`_evidence/app_stack_ownership_gap.md`). Anchor-text binding: G10 first (Section D), then G9/G11/G12.
**Date:** 2026-07-08
**Decisions baked in (Noel):** (1) RECONCILE - keep the prior `Strand.Grade.Number` coding + D/P/S/I types (grader + knowledge-graph already use it); re-derive the KC set gap-scoped; drop/re-gate every KC an existing app owns. (2) Map KCs + unit archs for all 4 grades together (the DAG spans grades); bind anchor texts G10-first.

## Coding scheme (unchanged, reused from prior work)
- **ID = Strand.Grade.Number.** Strand: C=Composition, M=Mechanics, D=Discourse/voice. (Kept for grader + knowledge-graph compatibility.)
- **KC type:** D=Discrimination · P=Production · S=Structure(rule) · I=Integrative. Rule: discrimination precedes production; 80%+ to advance; gateway KCs block downstream.
- **NEW status columns (gap-scope):** `HS-OWNED` (we teach it) · `GATED` (app owns it; retrieval-check + apply, never teach) · funnel = the tested capability it serves.

---

## A. The reconciliation verdict (what changed from the 68 prior KCs)

| Prior KC(s) | Prior status | Reconciled status | Why |
|-------------|--------------|-------------------|-----|
| **M.9.02 Sentence Imitation, M.9.03 Spot Wordiness, M.9.04 Revise Concision, M.9.05 Parallelism, M.9.06 Sentence Combining** | A1 taught (Unit 6) | **GATED (EGUMPP/AlphaWrite own)** - removed as taught KCs | App-stack gap analysis: EGUMPP owns parallelism/combining/wordiness G3-10; AlphaWrite owns combining/sentence craft G3-8. HS gates + applies, does not teach. (Exception: M.9.04 concision's RHETORICAL tier survives as the G11 concision delta, folded into revision.) |
| **M.9.01 Spot Stylistic Strengths, D.9.01/02 Voice** | A1 taught | **HS-OWNED but DEMOTED to woven/applied** | Style/voice recognition is not a tested discrete skill; it is exercised in composition + flagged in revision, not a standalone lesson. Kept as woven, not a gateway. |
| **C.9.B01-B05 Bridge KCs, C.9.01-12 analytical, C.10.x, C.AP.L.x, C.HS.x** | taught | **HS-OWNED (retained, re-mapped to the 12 roster skills)** | Composition/analysis/synthesis/AP tiers: no app owns these. This is the genuine HS gap. |
| **C.10.14, C.AP.L.15, C.HS.04 Timed strategy** | taught | **HS-OWNED (retained)** | Timed-transfer is the documented AP/ACT failure mode (AP Deep Dive); no app owns it. |

**Net:** the 5 A1 sentence-mechanics KCs (M.9.02-06) move from taught -> gated. Everything composition/analysis-level is retained. This is exactly the redundancy the gap analysis flagged, now removed from the KC layer too.

---

## B. The reconciled KC map (HS-OWNED KCs only; app-owned mechanics gated, listed in Section B0)

### B0. GATED substrate (app-owned; retrieval-check at entry, never a KC lesson)
`GATE.SENT` = the app-owned sentence substrate: kernel expansion, combining, appositives, because/but/so, subordinating conjunctions, fragment/run-on/comma-splice, parallelism, phrase/clause types, modifiers, basic wordiness, topic sentence, spelling/punctuation/agreement. Owners: EGUMPP (conventions G3-10) + AlphaWrite (sentence craft G3-8). Per-grade gate probes are timed-production, not worksheets (K&H). Failure routes to the owning app.

### B1. Grade 9 (A1) — foundations of source-based composition

| KC ID | Name | Type | Gateway? | Funnels into (tested) | Roster skill | Gated prereqs (GATE.SENT subset) |
|-------|------|------|----------|------------------------|--------------|-----------------------------------|
| C.9.01 | Defensible claim (prompt-responsive position) | D->P | GATEWAY | STAAR Eng I claim; all EOC argument | G9-1 | declarative sentence, fragment control, topic sentence |
| C.9.02 | Attributed-evidence sentence (integrate + credit source) | P | | STAAR/EOC research-evidence | G9-2 | appositive, "according to" prep phrase, combining; quotation punct (only if direct quote) |
| C.9.03 | Reason/warrant sentence (WHY evidence supports claim) | P | GATEWAY | EOC development trait; AP.5 | G9-3 | causal subordinating conjunctions (since/because/as), WHY-question expansion |
| C.9.04 | Single-source argument/informative essay strategy | I | GATEWAY | STAAR Eng I ECR | G9-4 | + SPO, transitions, paragraph structure (gated); staged: paragraph->multi-para->timed |
| D.9.01 | Voice/style (woven, not gateway) | woven | | ACT.11 tone/voice (later) | (applied) | (gated substrate) |

**A1 gate:** single-source source-based essay (argument OR informational) + entry GATE.SENT check. Pass = essay >= threshold; conventions scored holistically inside it.

### B2. Grade 10 (A2) — the modal-EOC year: analysis + counterargument

| KC ID | Name | Type | Gateway? | Funnels into | Roster skill | Gated prereqs |
|-------|------|------|----------|--------------|--------------|---------------|
| C.10.01 | Counterclaim-aware claim ("Although X, Y because Z") | P | GATEWAY | STAAR Eng II counterclaim | G10-1 | concessive subordinators although/while, adverb clause, combining |
| C.10.02 | Device->effect->warrant sentence (text-dependent analysis) | P | GATEWAY | SC-TDA, PA Keystone, MA, Regents | G10-2 | device-naming vocab (content layer), relative clause, causal clause (from C.9.03) |
| C.10.03 | Analysis essay strategy | I | GATEWAY | the modal G10 EOC | G10-3 | + paragraph structure (from C.9.04); staged paragraph->essay->timed |
| C.10.04 | Precision-in-argument (applied revision pass, NOT standalone) | woven | | EOC knowledge-of-language | G10-4 (revision pass) | word choice/wordiness (gated) |

**A2 gate:** text-dependent analysis essay (the STAAR Eng II mode) + counterclaim-aware argument + GATE.SENT check (G9+G10 subset).

### B3. Grade 11 (B1) — the college-test year: synthesis + rhetorical analysis + style

| KC ID | Name | Type | Gateway? | Funnels into | Roster skill | Gated prereqs |
|-------|------|------|----------|--------------|--------------|---------------|
| C.11.01 | Nuanced claim (qualification embedded) | P | GATEWAY | SBAC/ACT/Regents/AP Lang | G11-1 | appositives, relative clauses (participials optional) |
| C.11.02 | Cross-source/synthesis sentence + essay strategy | I | GATEWAY (Track B gate) | SBAC synthesis, AP Lang 6-source | G11-2 | coordinating/correlative conjunctions, transitions |
| C.11.03 | Rhetorical-analysis sentence + essay (author's choices) | I | GATEWAY | AP Lang rhet-analysis, NH SAT, FL G11 | G11-3 | device-naming vocab, appositives/clauses |
| C.11.04 | Rhetorical concision/style (applied revision pass) | woven | | ACT KoL, SAT Expression | G11-4 (revision pass) | wordiness, parallel structure (gated) |
| C.11.05 | Timed-writing strategy | P | | ACT/AP timing | (roster: cross-cutting) | — |

**B1 gate:** AP-style practice set — rhetorical analysis + synthesis + argument (or the ACT/SBAC equivalent for the non-AP path). Track B enrollment gated here.

### B4. Grade 12 (B2) — AP tier

| KC ID | Name | Type | Gateway? | Funnels into | Roster skill | Gated prereqs |
|-------|------|------|----------|--------------|--------------|---------------|
| C.12.01 | AP sophistication (significance "so-what" + context + competing perspectives) | I | GATEWAY | AP FRQ Row C; ACT.5/AP.2 gaps | G12-1 | (rides on C.11.01/02/03) |
| C.12.02 | Sustained AP writing under timed conditions | I | GATEWAY | AP Lang/Lit FRQ | G12-2 | staged: untimed->extended->exam-timed |
| D.12.01 | Voice through syntactic choice (woven) | woven | | AP style/sophistication | (applied) | (gated substrate) |

**B2 gate:** full timed AP practice exam, 5+ target.

**Reconciled KC totals (HS-OWNED taught KCs):** G9 = 4 + 1 woven · G10 = 3 + 1 revision-pass · G11 = 5 · G12 = 2 + 1 woven. ~14 taught KCs + woven/revision passes, down from 68 (the difference = app-owned mechanics now gated + the AP sub-tracks consolidated to the tested spine). This matches the 12-skill roster (the extra are the timed-strategy + woven-voice cross-cutters).

---

## C. Unit architectures (all four grades; KCs grouped in DAG order + the locked scaffold)

Every unit follows the locked scaffold: ENTRY retrieval-gate (GATE.SENT subset) -> genre-specific sentence move (just-in-time) -> paragraph phase -> essay phase (staged, per K&H) -> calibration/revision woven. Ordering law: no unit before the unit teaching its prerequisites.

### G9 (A1) — 4 units
- **U1 Claim + Evidence foundations** (C.9.01, C.9.02): gate GATE.SENT(G9); teach defensible claim + attributed-evidence sentences -> single-paragraph. Gateway: C.9.01.
- **U2 Reasoning** (C.9.03): teach warrant sentence (causal-clause orchestration) -> claim+evidence+warrant paragraph. Gateway: C.9.03.
- **U3 Single-source essay** (C.9.04, staged): body-paragraph assembly -> multi-paragraph coherence -> timed single-source essay. Gateway: C.9.04 (course gate).
- **U4 Style woven** (D.9.01): applied in U1-U3 revision, not a standalone unit block.

### G10 (A2) — 3 units
- **U1 Counterargument** (C.10.01): gate GATE.SENT(G9+G10); teach counterclaim-aware claim -> argument paragraph with concession. Gateway: C.10.01.
- **U2 Text-dependent analysis** (C.10.02): teach device->effect->warrant sentence -> analysis paragraph. Gateway: C.10.02.
- **U3 Analysis essay** (C.10.03, staged; C.10.04 revision pass woven): analysis-essay strategy staged to timed. Gateway: C.10.03 (course gate).

### G11 (B1) — 4 units
- **U1 Nuance** (C.11.01): gate GATE.SENT(all); teach nuanced claim -> nuanced argument paragraph. Gateway: C.11.01.
- **U2 Rhetorical analysis** (C.11.03): teach rhetorical-analysis sentence -> rhet-analysis essay (staged). Gateway: C.11.03.
- **U3 Synthesis** (C.11.02, staged): cross-source sentence -> synthesis essay. Gateway: C.11.02 (Track B gate).
- **U4 Timing + calibration** (C.11.05, C.11.04 revision pass): timed strategy + concision-for-effect woven.

### G12 (B2) — 2 units
- **U1 Sophistication** (C.12.01): teach significance + context + competing-perspectives moves atop G11 essays. Gateway: C.12.01.
- **U2 Timed AP mastery** (C.12.02, staged untimed->exam-timed; D.12.01 voice woven). Gateway: C.12.02 (course gate).

---

## D. Anchor-text binding — G10 FIRST (proves the KC -> arch -> anchor pipeline)

Bound from the existing G10 stimulus bank (`Stimulus_Bank_G10/`, 24 QC-verified stimuli, Lexile 1050-1185L). **Bucket discipline:** lesson-bucket (`lesson_*`) stimuli bind to LESSONS; test-bucket (`arg_*`/`info_*`/`analysis_*`) reserved for the gate/test bank (contamination partition, per `pipeline/contamination_check.py`). No stimulus binds to both.

| G10 Unit | KC | Anchor text (LESSON bucket) | Bucket / rights |
|----------|-----|------------------------------|-----------------|
| U1 Counterargument | C.10.01 | `lesson_arg_congestion_pricing.py`, `lesson_arg_school_year.py`, `lesson_arg_daylight_saving.py` (opposing-view argument, own-authored, federal-fact-sourced) | lesson · shippable |
| U2 Text-dependent analysis | C.10.02 | `lesson_analysis_story_of_an_hour.py` (Chopin, PD, 764w/1123L) | lesson · shippable (PD) |
| U3 Analysis essay | C.10.03 | `lesson_info_recycling.py`, `lesson_info_highways.py`, `lesson_info_weather.py`, `lesson_info_wetlands.py` (single-source informational, own-authored) | lesson · shippable |
| **GATE (reserved)** | course gate | `arg_*` (6), `info_*` (6), `analysis_*` (4) — TEST bucket, NEVER bound to a lesson | test · reserved |

**Anchor-binding rule (carry to G9/G11/G12):** each unit's anchor must (a) be lesson-bucket (never test), (b) match the unit's genre + the grade's Lexile band, (c) be copyright-clean (own-authored federal-fact or PD), (d) support the KC's specific move (e.g. an analysis anchor must have >=3 analyzable authorial choices). G9/G11/G12 anchor binding follows once their stimulus banks are built to the same 6-gate QC standard (G10 bank is furthest along; G9/G11/G12 banks are the next stimulus-generation targets).

---

## E. What this map deliberately does + does NOT do
- DOES keep the prior coding scheme (grader/knowledge-graph compatible) and retain every composition/analysis KC that no app owns.
- DOES re-gate the 5 A1 sentence-mechanics KCs (M.9.02-06) to app-owned (the reconciliation's core move).
- DOES bind G10 anchors from the verified lesson-bucket, honoring the test-partition.
- Does NOT teach any app-owned mechanic; does NOT bind test-bucket stimuli to lessons; does NOT re-introduce the pre-gap-analysis redundancy.
- OPEN (carried): confirm EGUMPP/AlphaWrite enrolled at HS (gate-remediation routing depends on it); build G9/G11/G12 stimulus banks before their anchor binding; the prior maps' standards tags (CCSS/TEKS/ACT/AP per KC) should be re-attached to the reconciled KCs in the machine-readable encoding step.
