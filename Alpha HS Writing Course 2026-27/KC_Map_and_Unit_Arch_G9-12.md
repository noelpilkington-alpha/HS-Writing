# G9-12 Writing KC Map + Unit Architectures (GAP-SCOPED, RECONCILED)

**Status:** DRAFT for review. Reconciles the prior KC scheme (`A1/A2/B1L/B2_Lesson_Map.md`, 68 KCs) with the gap-scoped roster (`Sentence_Skill_Roster_FINAL.md`) + app-ownership gap analysis (`_evidence/app_stack_ownership_gap.md`). Anchor-text binding: G10 first (Section D), then G9/G11/G12.

**⭐ ANCHOR = the AlphaCommonCore (ACC) spine** (`05_AlphaCommonCore_Writing_Spine.md`) — the empirical ≥2-state union of all 50 states' writing standards (the project-start common-standards work). CCSS/TEKS are SUBSETS of ACC; AP/ACT are thin overlays. Every KC carries a primary `ACC.W.*` code.

**⭐ SOURCE OF TRUTH = `pipeline/course_sequence_g9_12.py`** (the machine-readable, self-testing module encoding this map: ACC spine, KCs+tags, unit architecture, prerequisite DAG, gate spec). This doc is the human-readable RENDER of that module; the module is authoritative. Coverage is machine-verified by `pipeline/kc_coverage_matrix.py` (imports the module): 35 ACC codes + 24 tested capabilities all owned, 0 un-owned, self-test PASS. Coverage ≠ efficacy (efficacy needs student field data).
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

## A2. Coverage-audit revisions (2026-07-08, adversarial backward-trace)

The reconciled map was audited by tracing real released-item DEMANDS backward to the KCs (`_evidence/kc_coverage_audit.md`, 4 test-family finders + red-team). It found the forward-built map INCOMPLETE. Decisions applied below (Noel, 2026-07-08):

**FIXED (added/corrected KCs - clear coverage holes in tested skills):**
- **G2 Informational controlling-idea** -> new **C.9.05** (STAAR's DOMINANT ECR mode is informational; C.9.01 was argument-coded, C.9.04 blurred the modes).
- **G5 Production-of-Writing / discourse revision** -> new **C.9.06** (transitions & cohesion) + **C.10.05** (add/delete/reorder for rhetorical purpose + organization). This is 38-43% of ACT English + STAAR revising items; it was owned by NOBODY (not conventions-gated, not essay-KC). Quadruple-corroborated - the single biggest gap.
- **G6 Multi-source (2-3 text) writing at G10** -> new **C.10.06** (cross-text comparative argument/analysis, between single-source C.9.04 and G11 synthesis C.11.02). The modal G10 EOC is 2-4 source.
- **G3 Source-free / multi-perspective argument** -> new **C.11.06** (argue from own knowledge, AP Lang Q3, no given material) + **C.11.07** (engage multiple GIVEN perspectives + position own — ACT Writing). **Noel clarification: ACT Writing is NOT source-free — it supplies 3 perspectives on the issue; the student weighs them + positions their own. AP Lang Q3 IS source-free. Two distinct KCs.** (Restores the prior C.AP.L.08 + C.10.15-21 intent.)
- **G7 AP sophistication taught too late** -> C.12.01 sophistication is now INTRODUCED at G11 (woven into C.11.02/C.11.03), MASTERED at G12. Row C is the 5-vs-6 differentiator on the G11 Track-B gate.
- **G8 Source credibility/bias** -> new **C.11.08** (evaluate source credibility/bias) in the G11 synthesis unit. (Matches the prior gap analysis's two actionable research flags.)

**DESCOPED / DEFERRED (explicit, documented - not hidden holes):**
- **G1 Narrative writing** -> DESCOPED for the current build, BACKLOGGED for phase 2. 7 systems test it (LA/MD/TN/NJ/SBAC-option/MS/IA); we consciously focus the core on argument/analysis/synthesis (dominant + highest-leverage) and queue narrative as a fast-follow. Prior College Essay/SCENE work seeds it. **This is a conscious descope, recorded so it is not a silent gap.**
- **G4 AP Literature** -> NAMED-BUT-DEFERRED backlog. AP Lang is the primary tested track; AP Lit (poetry/prose-fiction/literary analysis) is a distinct analytical mode + literary stimuli, queued not cut. The B-track alternate-AP-Lit reference stays, marked DEFERRED.

**BLOCKING VERIFICATION (raised from nice-to-have by the audit):**
- The mis-gating findings share one root cause: several "GATED = covered" cells assume EGUMPP/AlphaWrite/AlphaRead teach the HS band (discourse revision, vocab-for-effect, AP-Lexile reading). If those apps stop at G8, those cells are actually UNCOVERED. **Confirm EGUMPP/AlphaWrite/AlphaRead HS enrollment + grade ceiling BEFORE relying on the gate** (was flagged in the roster; the audit makes it blocking).

**LOW / no action:** short-CR vs full-essay (same skill, interpret "essay" as extended-response); precision/concision SR-format transfer (add SR practice, skill already covered).

---

## B. The reconciled KC map (HS-OWNED KCs only; app-owned mechanics gated, listed in Section B0)

### B0. GATED substrate (app-owned; retrieval-check at entry, never a KC lesson)
`GATE.SENT` = the app-owned sentence substrate: kernel expansion, combining, appositives, because/but/so, subordinating conjunctions, fragment/run-on/comma-splice, parallelism, phrase/clause types, modifiers, basic wordiness, topic sentence, spelling/punctuation/agreement. Owners: EGUMPP (conventions G3-10) + AlphaWrite (sentence craft G3-8). Per-grade gate probes are timed-production, not worksheets (K&H). Failure routes to the owning app.

### B1. Grade 9 (A1) — foundations of source-based composition

| KC ID | Name | Type | Gateway? | Funnels into (tested) | Roster skill | Gated prereqs (GATE.SENT subset) |
|-------|------|------|----------|------------------------|--------------|-----------------------------------|
| C.9.01 | Defensible claim (prompt-responsive ARGUMENT position) | D->P | GATEWAY | STAAR Eng I argument claim; all EOC argument | G9-1 | declarative sentence, fragment control, topic sentence |
| C.9.05 | **Informational controlling-idea** (thesis that names topic + organizing angle for EXPLANATION, not a stance) *(NEW - audit G2)* | D->P | GATEWAY | STAAR Eng I/II informational ECR (the DOMINANT mode) | (new) | topic sentence (gated); sibling to C.9.01 - discriminate claim vs controlling-idea |
| C.9.02 | Attributed-evidence sentence (integrate + credit source) | P | | STAAR/EOC research-evidence | G9-2 | appositive, "according to" prep phrase, combining; quotation punct (only if direct quote) |
| C.9.03 | Reason/warrant sentence (WHY evidence supports claim/controlling idea) | P | GATEWAY | EOC development trait; AP.5 | G9-3 | causal subordinating conjunctions (since/because/as), WHY-question expansion |
| C.9.06 | **Transitions & cohesion** (select the transition matching the logical relationship; connect ideas across sentences) *(NEW - audit G5)* | D->P | | ACT Production of Writing, SAT Expression of Ideas, STAAR revising | (new) | NOT gated (rhetorical glue, not sentence conventions); discrimination-first (SR shells) |
| C.9.04 | Single-source essay strategy — SEPARATED by mode: (a) argument essay (on C.9.01) · (b) informational essay (on C.9.05) | I | GATEWAY | STAAR Eng I ECR (both modes) | G9-4 | + SPO, transitions (C.9.06), paragraph structure (gated); staged: paragraph->multi-para->timed |
| D.9.01 | Voice/style (woven, not gateway) | woven | | ACT.11 tone/voice (later) | (applied) | (gated substrate) |

**A1 gate:** single-source source-based essay (argument OR informational — both modes now have distinct thesis KCs) + entry GATE.SENT check. Pass = essay >= threshold; conventions scored holistically inside it.

### B2. Grade 10 (A2) — the modal-EOC year: analysis + counterargument

| KC ID | Name | Type | Gateway? | Funnels into | Roster skill | Gated prereqs |
|-------|------|------|----------|--------------|--------------|---------------|
| C.10.01 | Counterclaim-aware claim ("Although X, Y because Z") | P | GATEWAY | STAAR Eng II counterclaim | G10-1 | concessive subordinators although/while, adverb clause, combining |
| C.10.02 | Device->effect->warrant sentence (text-dependent analysis) | P | GATEWAY | SC-TDA, PA Keystone, MA, Regents | G10-2 | device-naming vocab (content layer), relative clause, causal clause (from C.9.03) |
| C.10.03 | Analysis essay strategy | I | GATEWAY | the modal G10 EOC | G10-3 | + paragraph structure (from C.9.04); staged paragraph->essay->timed |
| C.10.05 | **Rhetorical revision: add/delete/reorder for purpose + organization** (should this sentence be added? most logical sequence?) *(NEW - audit G5)* | D->P | | ACT Production of Writing (38-43%), SAT Expression of Ideas, STAAR revising | (new) | NOT gated (discourse-level, above sentence conventions); discrimination-first via SR shells + applied in revision |
| C.10.06 | **Cross-text (2-3 source) argument/analysis** (integrate + compare evidence across sources, short of full synthesis) *(NEW - audit G6)* | I | GATEWAY | modal G10 EOC (NY/FL/MA/MD/SC/LA/NJ all 2-4 source) | (new) | on C.9.02 + C.10.03; between single-source C.9.04 and G11 synthesis C.11.02 |
| C.10.04 | Precision-in-argument (applied revision pass, NOT standalone) | woven | | EOC knowledge-of-language | G10-4 (revision pass) | word choice/wordiness (gated) |

**A2 gate:** cross-text (2-3 source) text-dependent analysis essay (the STAAR Eng II + modal-EOC mode) + counterclaim-aware argument + rhetorical-revision SR + GATE.SENT check (G9+G10 subset).

### B3. Grade 11 (B1) — the college-test year: synthesis + rhetorical analysis + style

| KC ID | Name | Type | Gateway? | Funnels into | Roster skill | Gated prereqs |
|-------|------|------|----------|--------------|--------------|---------------|
| C.11.01 | Nuanced claim (qualification embedded) | P | GATEWAY | SBAC/ACT/Regents/AP Lang | G11-1 | appositives, relative clauses (participials optional) |
| C.11.02 | Cross-source/synthesis sentence + essay strategy | I | GATEWAY (Track B gate) | SBAC synthesis, AP Lang 6-source | G11-2 | coordinating/correlative conjunctions, transitions |
| C.11.03 | Rhetorical-analysis sentence + essay (author's choices) | I | GATEWAY | AP Lang rhet-analysis, NH SAT, FL G11 | G11-3 | device-naming vocab, appositives/clauses |
| C.11.04 | Rhetorical concision/style (applied revision pass) | woven | | ACT KoL, SAT Expression | G11-4 (revision pass) | wordiness, parallel structure (gated) |
| C.11.05 | Timed-writing strategy | P | | ACT/AP timing | (roster: cross-cutting) | — |
| C.11.06 | **Argue from own knowledge** (source-free: generate evidence/examples from knowledge, observation, reading — NO given material) *(NEW - audit G3)* | P->I | GATEWAY | AP Lang Argument FRQ (33% of Section II) | (new; restores prior C.AP.L.08) | on C.9.01 + C.9.03; the reasoning spine minus the source dependency |
| C.11.07 | **Multi-perspective argument** (analyze 2-3 GIVEN perspectives on an issue, weigh strengths/limits, position own relative to them) *(NEW - audit G3; Noel: ACT is NOT source-free, it supplies perspectives)* | P->I | | ACT Writing (3-perspective, ~26 ACT/SAT states) | (new; restores prior C.10.15-21 intent) | on C.10.01 counterclaim-aware; distinct from source-text analysis |
| C.11.08 | **Evaluate source credibility/bias** (judge author credentials, bias, evidence quality; which source to trust + why) *(NEW - audit G8)* | D | | SBAC/PARCC research-simulation tasks; ACC 11(G)(i)/(H) | (new) | in the synthesis unit; the read-the-source step already exists |
| — | *(AP sophistication C.12.01 is now INTRODUCED here at G11, woven into C.11.02/C.11.03; mastered at G12 — audit G7)* | | | AP Row C (5-vs-6 on the G11 Track-B gate) | | |

**B1 gate:** AP-style practice set — rhetorical analysis + synthesis + argument (source-based AND source-free C.11.06) + multi-perspective (C.11.07) for the ACT path. Sophistication (C.12.01) introduced + surfaced on the gate rubric. Track B enrollment gated here.

### B4. Grade 12 (B2) — AP tier

| KC ID | Name | Type | Gateway? | Funnels into | Roster skill | Gated prereqs |
|-------|------|------|----------|--------------|--------------|---------------|
| C.12.01 | AP sophistication (significance "so-what" + context + competing perspectives) — INTRODUCED G11 (woven), MASTERED G12 *(audit G7)* | I | GATEWAY | AP FRQ Row C; ACT.5/AP.2 gaps | G12-1 | (rides on C.11.01/02/03) |
| C.12.02 | Sustained AP writing under timed conditions | I | GATEWAY | AP Lang/Lit FRQ | G12-2 | staged: untimed->extended->exam-timed |
| D.12.01 | Voice through syntactic choice (woven) | woven | | AP style/sophistication | (applied) | (gated substrate) |

**B2 gate:** full timed AP practice exam, 5+ target.

**Reconciled KC totals (HS-OWNED taught KCs), post-audit:** G9 = 6 (C.9.01/05/02/03/06/04) + 1 woven · G10 = 5 (C.10.01/02/03/05/06) + 1 revision-pass · G11 = 8 (C.11.01/02/03/05/06/07/08 + sophistication-intro) + 1 revision-pass · G12 = 2 + 1 woven. ~21 taught KCs (was ~14 pre-audit; the audit added 7: C.9.05, C.9.06, C.10.05, C.10.06, C.11.06, C.11.07, C.11.08). Still down from the prior 68 because app-owned mechanics stay gated; the additions are genuine tested-skill holes the forward map missed, not restored redundancy.

---

## C. Unit architectures (all four grades; KCs grouped in DAG order + the locked scaffold)

Every unit follows the locked scaffold: ENTRY retrieval-gate (GATE.SENT subset) -> genre-specific sentence move (just-in-time) -> paragraph phase -> essay phase (staged, per K&H) -> calibration/revision woven. Ordering law: no unit before the unit teaching its prerequisites.

### G9 (A1) — 5 units (post-audit)
- **U1 Claim/controlling-idea + Evidence foundations** (C.9.01 argument claim, C.9.05 informational controlling-idea, C.9.02): gate GATE.SENT(G9); teach BOTH thesis modes (discriminate claim vs controlling-idea) + attributed-evidence -> single-paragraph. Gateway: C.9.01 + C.9.05.
- **U2 Reasoning** (C.9.03): teach warrant sentence (causal-clause orchestration) -> claim/idea+evidence+warrant paragraph. Gateway: C.9.03.
- **U3 Cohesion** (C.9.06): teach transitions/cohesion (discrimination-first) -> connect ideas across a paragraph. *(NEW - audit G5)*
- **U4 Single-source essay** (C.9.04, staged, both modes): body-paragraph assembly -> multi-paragraph coherence -> timed single-source essay (argument OR informational). Gateway: C.9.04 (course gate).
- **U5 Style woven** (D.9.01): applied in U1-U4 revision, not a standalone block.

### G10 (A2) — 4 units (post-audit)
- **U1 Counterargument** (C.10.01): gate GATE.SENT(G9+G10); teach counterclaim-aware claim -> argument paragraph with concession. Gateway: C.10.01.
- **U2 Text-dependent analysis** (C.10.02): teach device->effect->warrant sentence -> analysis paragraph. Gateway: C.10.02.
- **U3 Rhetorical revision** (C.10.05): teach add/delete/reorder-for-purpose + organization (discrimination via SR shells) -> applied in essay revision. *(NEW - audit G5; the 38-43%-of-ACT-English gap)*
- **U4 Cross-text analysis essay** (C.10.06 + C.10.03, staged; C.10.04 revision pass woven): 2-3 source comparative analysis/argument, staged to timed. Gateway: C.10.06 (course gate). *(C.10.06 NEW - audit G6)*

### G11 (B1) — 6 units (post-audit)
- **U1 Nuance** (C.11.01): gate GATE.SENT(all); teach nuanced claim -> nuanced argument paragraph. Gateway: C.11.01.
- **U2 Rhetorical analysis** (C.11.03): teach rhetorical-analysis sentence -> rhet-analysis essay (staged). Sophistication (C.12.01) INTRODUCED here (woven). Gateway: C.11.03.
- **U3 Synthesis + source evaluation** (C.11.02 + C.11.08, staged): evaluate source credibility/bias, then cross-source sentence -> synthesis essay. Gateway: C.11.02 (Track B gate). *(C.11.08 NEW - audit G8)*
- **U4 Source-free argument** (C.11.06): argue from own knowledge, no given material -> AP-Lang-Q3-style essay. Gateway: C.11.06. *(NEW - audit G3)*
- **U5 Multi-perspective argument** (C.11.07): analyze 3 given perspectives + position own -> ACT-Writing-style essay. *(NEW - audit G3; Noel: ACT supplies perspectives, not source-free)*
- **U6 Timing + calibration** (C.11.05, C.11.04 revision pass): timed strategy + concision-for-effect woven; sophistication surfaced on the gate rubric.

### G12 (B2) — 2 units (+ deferred AP Lit track)
- **U1 Sophistication mastery** (C.12.01, introduced at G11): master significance + context + competing-perspectives atop G11 essays. Gateway: C.12.01.
- **U2 Timed AP mastery** (C.12.02, staged untimed->exam-timed; D.12.01 voice woven). Gateway: C.12.02 (course gate).
- **[DEFERRED] AP Literature track** — poetry/prose-fiction/literary-analysis KCs NOT built (named-but-deferred backlog, audit G4). B2 currently = AP Lang only.

---

## D. Anchor-text binding — G10 FIRST (proves the KC -> arch -> anchor pipeline)

Bound from the existing G10 stimulus bank (`Stimulus_Bank_G10/`, 24 QC-verified stimuli, Lexile 1050-1185L). **Bucket discipline:** lesson-bucket (`lesson_*`) stimuli bind to LESSONS; test-bucket (`arg_*`/`info_*`/`analysis_*`) reserved for the gate/test bank (contamination partition, per `pipeline/contamination_check.py`). No stimulus binds to both.

| G10 Unit | KC | Anchor text (LESSON bucket) | Bucket / rights |
|----------|-----|------------------------------|-----------------|
| U1 Counterargument | C.10.01 | `lesson_arg_congestion_pricing.py`, `lesson_arg_school_year.py`, `lesson_arg_daylight_saving.py` (opposing-view argument, own-authored, federal-fact-sourced) | lesson · shippable |
| U2 Text-dependent analysis | C.10.02 | `lesson_analysis_story_of_an_hour.py` (Chopin, PD, 764w/1123L) | lesson · shippable (PD) |
| U3 Rhetorical revision (C.10.05, NEW) | C.10.05 | own-words draft passages built FROM the lesson_info_* stimuli (revision targets: weak transitions, misordered sentences, off-topic sentence to delete) — authored, not a new stimulus | lesson · shippable *(to build)* |
| U4 Cross-text analysis essay (C.10.06, NEW) | C.10.06, C.10.03 | a PAIR of lesson-bucket stimuli (e.g. `lesson_info_recycling.py` + `lesson_info_highways.py`) for 2-source comparison | lesson · shippable |
| **GATE (reserved)** | course gate | `arg_*` (6), `info_*` (6), `analysis_*` (4) — TEST bucket, NEVER bound to a lesson | test · reserved |

**Anchor-binding rule (carry to G9/G11/G12):** each unit's anchor must (a) be lesson-bucket (never test), (b) match the unit's genre + the grade's Lexile band, (c) be copyright-clean (own-authored federal-fact or PD), (d) support the KC's specific move (e.g. an analysis anchor must have >=3 analyzable authorial choices). G9/G11/G12 anchor binding follows once their stimulus banks are built to the same 6-gate QC standard (G10 bank is furthest along; G9/G11/G12 banks are the next stimulus-generation targets).

---

## E. What this map deliberately does + does NOT do
- DOES keep the prior coding scheme (grader/knowledge-graph compatible) and retain every composition/analysis KC that no app owns.
- DOES re-gate the 5 A1 sentence-mechanics KCs (M.9.02-06) to app-owned (the reconciliation's core move).
- DOES close the 7 tested-skill coverage holes the backward-trace audit found (C.9.05, C.9.06, C.10.05, C.10.06, C.11.06, C.11.07, C.11.08 + early-sophistication).
- DOES bind G10 anchors from the verified lesson-bucket, honoring the test-partition.
- Does NOT teach any app-owned mechanic; does NOT bind test-bucket stimuli to lessons; does NOT re-introduce the pre-gap-analysis redundancy.

### E1. Explicitly DESCOPED / DEFERRED (conscious, documented — not hidden holes)
- **Narrative writing (audit G1):** DESCOPED for the current build, BACKLOGGED for phase 2. 7 systems test it (LA/MD/TN/NJ/SBAC-option/MS/IA). We ship the argument/analysis/synthesis core first; narrative is a queued fast-follow (seeded by prior College Essay/SCENE work). Students in narrative-testing states will NOT be covered for that task until phase 2 — recorded so it is a decision, not an accident.
- **AP Literature track (audit G4):** NAMED-BUT-DEFERRED. B2 = AP Lang only in this build; the poetry/prose-fiction/literary-analysis KCs are queued, not cut. The alternate-AP-Lit reference stays, marked DEFERRED.

### E2. Mis-gating RESOLVED (Noel, 2026-07-08): separate HS courses own the adjacent bands
The audit's mis-gating worry ("do the K-8 apps reach the HS band?") is resolved: the HS ecosystem has **separate HS Language, Vocabulary, and (question below) AP courses**, so the gated skills are owned by real HS courses, not only the K-8 apps. Ownership:
- **Conventions + "Knowledge of Language"** (precision/concision/style-tone as SR editing of a given passage) -> HS **Language** course. GATED, safe.
- **Vocabulary / vocabulary-for-effect** -> HS **Vocabulary** course. GATED, safe.
- **Reading comprehension at HS Lexile** -> reading course / AlphaRead. GATED, safe.
- **STAYS with WRITING (not language):** "Production of Writing" — transitions/cohesion (C.9.06), add/delete/reorder-for-purpose + organization (C.10.05). This is composition/rhetorical structure, not language mechanics, so it is correctly HS-writing-owned (the audit's biggest gap, kept in-scope). Precision/concision AS APPLIED IN THE STUDENT'S OWN ESSAY (C.10.04/C.11.04 revision passes) stays with writing; the same skill AS SR editing of someone else's passage is the Language course's.
- **Net:** the writing course's job is WRITING (compose/structure/revise-for-meaning); conventions, language-knowledge, and vocabulary are owned by the Language + Vocabulary courses. This confirms the gate is safe and sharpens the scope.

### E2b. Scope + standards anchor (Noel, 2026-07-08)
- **The writing course spans G9-12** (B1/B2 ARE our AP writing courses; the AP tier stays in scope). NOT descoped to G9-10.
- **Anchor = the common standards** (CCSS, TEKS, and the reconciled AlphaCommonCore spine from the earlier research), NOT AP-rubric-first. AP (and ACT/SAT) are **thin overlays** on a CCSS/TEKS-aligned core — the exam-agnostic-core + thin-overlays architecture. Consequence: every KC must carry a CCSS/TEKS tag (the primary alignment), with AP/ACT as secondary tags. The coverage matrix validates STANDARDS coverage first, tested-capability coverage second.

### E3. OPEN (non-blocking, carried)
- Build G9/G11/G12 stimulus banks (incl. the new C.10.05 revision-passage set) before their anchor binding.
- **Re-attach per-KC standards tags with CCSS/TEKS PRIMARY** (AP/ACT secondary) to all 21 KCs in the machine-readable encoding step, per E2b.
- Rebuild `coverage_matrix.py` against this corrected map (done next: regression-checks all 21 KCs vs both the common-standards denominator AND the tested-capability set).
