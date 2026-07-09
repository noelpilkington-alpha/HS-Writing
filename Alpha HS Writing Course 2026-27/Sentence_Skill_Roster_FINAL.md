# Finalized HS Writing Skill Roster + Scaffold (G9-12) — GAP-SCOPED

**Status:** DECISION-LOCKED (gap-scoped) + ACC-RECONCILED (2026-07-09). This roster's skills are now encoded, ACC-anchored, in the SINGLE SOURCE OF TRUTH: `pipeline/course_sequence_g9_12.py` (self-testing) + `KC_Map_and_Unit_Arch_G9-12.md`. **Where this doc and the module differ, the MODULE is authoritative** (this doc is the human-readable rationale). The roster's original skill labels (G9-1, G10-2, ...) map to the module's KC ids (C.9.01, C.10.02, ...) via the crosswalk in Section 1A below.
**Date:** 2026-07-08 (roster) · 2026-07-09 (ACC reconciliation)
**Anchor:** the AlphaCommonCore spine (>=2-state union); every owned skill carries a primary `ACC.W.*` code. CCSS/TEKS are subsets; AP/ACT are overlays.
**The governing principle (Noel):** HS Writing covers ONLY the tested writing skills that existing Alpha ELA apps do NOT own. Skills an app already teaches are RETRIEVAL-GATED and APPLIED in composition (cross-pollination), never re-taught. Focus = the writing skills students must execute on standardized tests that no current app provides.

**Evidence base:** app ownership (`_evidence/app_stack_ownership_gap.md`, from the NY Standards -> Timeback app-stack xlsx + EGUMPP correction memo); tested capabilities + item formats (`_evidence/sentence_skill_assessment_evidence.md`, `_evidence/writing_item_type_catalog.md`); G3-8 inheritance (`_evidence/g3-8_inherited_sentence_skills.md`); council rulings (`_evidence/sentence_skill_sources.md`).

---

## 0. What existing apps OWN (gated at HS entry, never re-taught)

The Alpha app stack is K-8 and, for two apps, spirals into the 9-10 band. HS Writing gates these and applies them in composition; failure routes remediation to the owning app.

| Owned by | Skills (gated + applied at HS, NOT taught as HS lessons) |
|----------|----------------------------------------------------------|
| **EGUMPP** (conventions, CCSS G3-10 spiral) | parallel structure (L.9-10.1a) · phrase/clause types incl. prepositional/participial/gerund/infinitive + relative/adverbial/noun clauses (L.9-10.1b) · misplaced/dangling modifiers (L.7.1c) · appositives · semicolons/colons (L.9-10.2a) · fragments/run-ons · agreement · verb voice/mood · basic wordiness/redundancy (L.7.3a) · commonly-confused words |
| **AlphaWrite** (TWR sentence craft + composition, G3-8) | kernel expansion · sentence combining · appositives · because/but/so · basic subordinating conjunctions · sentence types · topic/controlling-idea sentence · G3-8 argument/informative/narrative composition |
| **AlphaRead** (reading + vocabulary) | reading comprehension of stimuli · vocabulary · figurative language |

**HS Writing teaches NONE of the above.** It assumes them (gate at entry), applies them inside composition, and flags them holistically in the essay Conventions rubric (the lowest-weight trait, scored by error density, not taught as lessons).

---

## 1. What HS Writing OWNS (the genuine gap: tested writing skills no app covers)

The gap is the COMPOSITION + RHETORICAL tier: turning mechanically-correct sentences (EGUMPP) and basic composition (AlphaWrite G8) into test-winning source-based argument / analysis / synthesis writing. Every owned skill funnels into a tested capability and is owned by NO app.

## 1A. ACC crosswalk — roster labels -> source-of-truth KC ids (authoritative)

This roster was authored before the KC map + ACC anchoring + the backward-trace coverage audit. The audit ADDED 7 KCs the roster's original 14-skill framing lacked (informational thesis, transitions/cohesion, cross-text, source-free argument, multi-perspective, source-evaluation). The definitive per-grade skill set + ACC codes now lives in `course_sequence_g9_12.py`; this table reconciles the roster's labels to it.

| Roster label (this doc) | Module KC id | Primary ACC code(s) | Note |
|-------------------------|--------------|---------------------|------|
| G9-1 defensible claim | **C.9.01** | ACC.W.ARG.1 | |
| (none — audit-added) | **C.9.05** | ACC.W.INFO.1 | NEW: informational controlling-idea (STAAR's dominant mode) |
| G9-2 attributed-evidence | **C.9.02** | ACC.W.SRC.2 | |
| G9-3 reason/warrant | **C.9.03** | ACC.W.ARG.2 | |
| (none — audit-added) | **C.9.06** | ACC.W.ARG.3, ACC.W.INFO.3 | NEW: transitions & cohesion (ACT Production-of-Writing gap) |
| G9-4 single-source essay | **C.9.04** | ACC.W.PROD.1 (+ARG.5/INFO.2/3/5) | |
| G10-1 counterclaim-aware claim | **C.10.01** | ACC.W.ARG.2 | |
| G10-2 device->effect->warrant | **C.10.02** | ACC.W.INFO.6, ACC.W.SRC.3 | |
| G10-3 analysis essay | **C.10.03** | ACC.W.INFO.6, ACC.W.INFO.2, ACC.W.SRC.3 | |
| G10-4 precision-in-argument (revision pass) | **C.10.04** | ACC.W.PROC.2 | woven |
| (none — audit-added) | **C.10.05** | ACC.W.PROC.2 | NEW: rhetorical revision add/delete/reorder + organization |
| (none — audit-added) | **C.10.06** | ACC.W.SRC.1 | NEW: cross-text 2-3 source (modal G10 EOC) |
| G11-1 nuanced claim | **C.11.01** | ACC.W.ARG.1 | |
| G11-2 synthesis | **C.11.02** | ACC.W.SRC.1 | |
| G11-3 rhetorical-analysis | **C.11.03** | ACC.W.INFO.6 | |
| G11-4 rhetorical concision (revision pass) | **C.11.04** | ACC.W.PROC.2 | woven |
| (none — cross-cutting) | **C.11.05** | ACC.W.PROC.1 | timed-writing strategy |
| (none — audit-added) | **C.11.06** | ACC.W.ARG.1 | NEW: argue from own knowledge (AP Lang Q3, source-free) |
| (none — audit-added) | **C.11.07** | ACC.W.ARG.2 | NEW: multi-perspective argument (ACT, 3 given perspectives) |
| (none — audit-added) | **C.11.08** | ACC.W.SRC.1, ACC.W.INQ.1 | NEW: evaluate source credibility/bias |
| G12-1 AP sophistication | **C.12.01** | ACC.W.ARG.2 | significance/context/competing perspectives; introduced G11, mastered G12 |
| G12-2 sustained timed AP writing | **C.12.02** | ACC.W.PROD.1 | |
| (voice, woven) | **D.12.01** | ACC.W.CONV.3 | applied, not owned |

**Reconciled totals:** 23 module KCs (was 14 in this doc's original framing; +7 audit KCs +2 revision-pass/timed cross-cutters made explicit). The gated substrate (Section 0) is unchanged. Every KC's ACC code is validated owned by `pipeline/kc_coverage_matrix.py` (35 ACC codes, 0 un-owned) and the module self-test.

### GRADE 9 (A1) - foundations of source-based composition

| # | HS-owned skill | Tested by | Not owned by any app because... |
|---|----------------|-----------|--------------------------------|
| G9-1 | **Defensible claim sentence** (position on a source-based prompt) | STAAR Eng I, VA G9, all EOC argument | AlphaWrite G8 does general opinion writing, not source-based EOC claim |
| G9-2 | **Attributed-evidence sentence** (integrate + cite quoted/paraphrased source evidence) | STAAR, all EOC research/evidence | source-integration is HS-tested; no app teaches quote/cite-into-argument |
| G9-3 | **Reason/warrant sentence** (because-link matured: why the evidence supports the claim) | EOC argument (development trait); AP.5 | the reasoning MOVE (not the connective, which AlphaWrite owns) is composition-level |
| G9-4 | **Single-source argument + informative essay** (claim -> evidence -> reasoning -> conclusion) | STAAR Eng I ECR, all G9 EOC | the source-based EOC essay is the HS gap; AlphaWrite stops at G8 general composition |

### GRADE 10 (A2) - the modal EOC year: analysis + counterargument

| # | HS-owned skill | Tested by | Not owned because... |
|---|----------------|-----------|----------------------|
| G10-1 | **Counterclaim-aware claim** ("Although some argue X, Y because Z") | STAAR Eng II ("develop claim AND counterclaim fairly"), EOCs | composition move above AlphaWrite; EGUMPP owns the subordinator mechanic, not the argumentative use |
| G10-2 | **Device -> effect -> warrant sentence** (text-dependent analysis) | SC-TDA, PA Keystone, MA, GA, Regents G10 analysis | analytical writing about a text; no app teaches it |
| G10-3 | **Text-dependent analysis essay** (analyze a text's ideas/craft with evidence) | the modal G10 EOC | the analysis essay is a pure HS gap |
| G10-4 | **Rhetorical precision delta** (word choice for argumentative accuracy, above EGUMPP's mechanical word-choice) | EOC knowledge-of-language; ACT/SAT prep | EGUMPP does confused-words/wordiness; argumentative precision-for-effect is composition |

### GRADE 11 (B1) - the college-test year: synthesis + rhetorical analysis + style

| # | HS-owned skill | Tested by | Not owned because... |
|---|----------------|-----------|----------------------|
| G11-1 | **Nuanced claim** (qualification/complexity embedded in the claim) | SBAC, ACT, NY Regents, AP Lang | top-tier composition; no app |
| G11-2 | **Cross-source / synthesis sentence + essay** (connect 2+ sources into one argument) | SBAC explanatory, AP Lang 6-source synthesis, Regents | synthesis is HS-only |
| G11-3 | **Rhetorical-analysis sentence + essay** (name author's choice -> analyze effect/purpose) | AP Lang rhetorical analysis, NH SAT essay, FL G11 | rhetorical analysis is HS-only |
| G11-4 | **Rhetorical concision / style-for-effect** (cut for emphasis + rhetorical goal, above EGUMPP wordiness) | ACT Knowledge of Language, SAT Expression "meet rhetorical goals" | EGUMPP owns mechanical wordiness; the rhetorical tier is the HS delta |

### GRADE 12 (B2) - AP tier

| # | HS-owned skill | Tested by | Not owned because... |
|---|----------------|-----------|----------------------|
| G12-1 | **AP sophistication** (convey significance / "so what"; establish context; integrate competing perspectives) | AP FRQ Row C; ACT.5 significance; AP.2/ACT.3 context | the two audit gaps N2/N3 + AP ceiling; no app |
| G12-2 | **Sustained AP-level argument/synthesis/rhetorical-analysis** under timed conditions | AP Lang/Lit FRQ | AP composition; no app |

---

## 2. Cross-pollination: where app-owned mechanics meet HS composition

HS Writing does NOT re-teach app-owned mechanics, but it DOES exercise them inside composition and teach only the tested DELTA above the app's ceiling:

| App-owned mechanic | HS treatment |
|--------------------|--------------|
| Parallelism, phrase/clause variety, modifiers (EGUMPP) | GATE at entry; APPLY in essays (sentence variety supports the Development + rhetorical traits); flag in revision feedback; NO HS lesson. Remediation -> EGUMPP. |
| Sentence combining, appositives, because/but/so (AlphaWrite/EGUMPP) | GATE; the reasoning USE of because/but/so is matured into claim-evidence-reasoning (G9-3), but the connective mechanic is not re-taught. |
| Basic wordiness / word choice (EGUMPP) | GATE; HS teaches only rhetorical concision/precision-for-effect (G10-4, G11-4), the delta EGUMPP does not cover. |
| Conventions (grammar/punct/spelling) | Scored HOLISTICALLY in the essay rubric (lowest-weight trait); flagged in feedback, never a lesson. |

**Retrieval-gate mechanism:** at each grade's entry, a fast check on the inherited app-owned substrate. Pass -> proceed. Fail -> Platform routes remediation to the owning app (EGUMPP for conventions, AlphaWrite for sentence craft), which may be a lower grade's content.

---

## 2A. Prerequisite decomposition (each HS-owned skill = orchestration of gated granular tools)

**The principle (Noel):** an HS-owned composition skill is NOT atomic. It orchestrates granular sentence tools that the apps already own. Each HS skill declares: (a) its **gated granular prerequisites** (app-owned components the retrieval-gate verifies), (b) its **HS-owned prerequisite** (an earlier HS skill), (c) the **ONE new discrimination** it teaches (DI faultless-communication: exactly one new boundary per skill), and (d) for essay skills, the **genre STRATEGY** it teaches (SRSD: a named plan + self-monitoring; the sentence moves are prerequisites TO the strategy, not a substitute for it).

**Reviewed by the council 2026-07-08** (TWR + Kirschner & Hendrick + DI + SRSD + judge), which found the architecture sound but the first-cut execution flawed. This version applies all 13 adjudicated fixes; full record in `_evidence/decomposition_council_review.md`. Two conflicts were adjudicated by evidence grade: SRSD (A) won "add a genre-strategy layer" over TWR (B); K&H (A) won "essays must be decomposed into stages" over TWR (B).

Canonical example (Noel's): TWR's **because/but/so** is an analytical-THINKING / comprehension prompt, NOT a warrant-writing tool (TWR seat correction). The warrant is written with **subordinating conjunctions for causation** (since/because/as) + WHY-question expansion. HS never re-teaches those (apps own them); HS teaches the *argumentative orchestration* - using a causal clause to state WHY evidence supports the claim.

### Component (sentence-move) skills

| HS skill | Gated granular prerequisites (owning app) | HS prereq | The ONE new discrimination HS teaches |
|----------|-------------------------------------------|-----------|----------------------------------------|
| **G9-1 defensible claim** | declarative sentence + fragment control (EGUMPP); topic/controlling-idea sentence (AlphaWrite) | - | **claim vs non-claim**: a defensible, prompt-responsive POSITION (arguable) vs a topic-announcing or factual sentence |
| **G9-2 attributed-evidence** | appositive for attribution (EGUMPP/AlphaWrite); prepositional phrase "according to" (EGUMPP); **sentence combining** (AlphaWrite); quotation punctuation *(optional, only for direct quotes; paraphrase/summary uses none)* | - | **attributed vs bare evidence**: source material woven in + credited vs dropped-in |
| **G9-3 reason/warrant** | **subordinating conjunctions for causation** since/because/as (EGUMPP/AlphaWrite); WHY-question sentence expansion (AlphaWrite) *(NOT because/but/so, which is a comprehension prompt)* | G9-1 | **warrant vs restatement**: a clause stating WHY the evidence supports the claim vs merely repeating the evidence |
| **G10-1 counterclaim-aware claim** | concessive subordinators although/while/whereas + adverb clause (EGUMPP); combining (AlphaWrite) | G9-1 | **counterclaim-aware vs claim-only**: concede the opposing view then reassert ("Although X, Y because Z") |
| **G10-2 device->effect->warrant** | device-NAMING vocabulary *(content layer: metaphor/anaphora/juxtaposition - taught/gated separately, NOT an appositive use)*; relative clause "which creates..." (EGUMPP); causal clause (from G9-3) | G9-3 | **analysis vs summary**: name the author's device -> its effect -> why it matters, vs restating what the text says |
| **G10-4 (reclassified: applied revision-in-genre, NOT a new composition skill)** | word choice / confused-words / wordiness (EGUMPP) | G9-1 | *(no new orchestration; a REVISION pass applying EGUMPP precision inside argument drafts. Folded into essay revision, not a standalone skill.)* |
| **G11-1 nuanced claim** | appositives + relative clauses (EGUMPP); participial phrases *(optional - one tool for embedding, not required)* | G10-1 | **nuanced vs binary claim**: multi-dimensional qualification embedded in the claim vs a single concession |
| **G11-3 rhetorical-analysis** | device-naming vocabulary; appositives/clauses (EGUMPP) | G10-2 | **author's-choices vs text's-ideas**: analyze WHY the author made a rhetorical choice + its effect on the audience, vs analyzing the content (the delta over G10-2) |
| **G11-4 (reclassified: applied revision-in-genre)** | wordiness/unclear-elements + parallel structure (EGUMPP) | G10-4 pass | *(no new orchestration; a REVISION pass cutting for rhetorical emphasis. Folded into essay revision.)* |

### Genre-STRATEGY skills (SRSD layer: named plan + self-monitoring; sentence moves above are prerequisites TO these)

| HS strategy skill | Component prereqs | Genre strategy taught (plan + self-monitoring) | Staged decomposition (K&H: essay != one skill) |
|-------------------|-------------------|------------------------------------------------|-------------------------------------------------|
| **G9-4 single-source argument/informative essay** | G9-1, G9-2, G9-3 | a NAMED argument strategy (plan for what goes where + how much + order) + self-monitoring cues ("Did I state WHY each piece of evidence supports my claim?") | **(a)** body-paragraph assembly (claim+evidence+warrant, one paragraph) -> **(b)** multi-paragraph coherence (intro+body+conclusion, transitions) -> **(c)** timed single-source essay. Each stage GATES the sentence tools it uses (combining, subordination, appositive) as timed-production probes (cumulative review). |
| **G10-3 analysis essay** | G10-2; G9-4 stage-(b) paragraph structure | a NAMED analysis strategy (thesis about a text's craft + device-chain body plan) + self-monitoring ("Does each body paragraph name a device, its effect, and why it matters?") | (a) single device-chain paragraph -> (b) multi-device analysis essay -> (c) timed. Gates G10-2 + G9 sentence tools. |
| **G11-2 synthesis essay** | G9-2, G11-1; coordinating/correlative conjunctions + transitions (EGUMPP) | a NAMED synthesis strategy (put 2+ sources in conversation around one claim) + self-monitoring ("Have I connected sources, not just listed them?") | (a) cross-source sentence -> (b) multi-source paragraph -> (c) synthesis essay, timed. Gates attribution + nuance. |
| **G12-1 AP sophistication** | G11-1, G11-2, G11-3 | the significance + context + competing-perspectives moves (closes audit gaps N2/N3) + self-monitoring ("Have I said why this matters + situated it?") | (a) significance/"so-what" move -> (b) context-establishing move -> (c) integrate competing perspectives. |
| **G12-2 sustained timed AP FRQ** | G12-1 + all G11 | putting the AP strategy under timed conditions | (a) untimed full FRQ -> (b) extended-time -> (c) exam-timed. Sustain + timed are separated loads, not stacked at once. |

*Every skill (component + strategy) is taught via gradual release: worked example -> labeled model -> partial fade -> independent (K&H within-skill fade; SRSD model-messy/memorize/support/fade). Discrimination before production.*

**Three structures fall out (all feed the machine-readable module + gate design):**

1. **The retrieval-gate spec (per grade), upgraded to timed-production / dual-task probes (K&H: a worksheet check proves accessibility, not in-composition automaticity):**
   - **G9 gate:** sentence types + fragment control, topic sentence, appositive, prepositional phrase, subordinating conjunctions for causation, combining, SPO/transitions, paragraph structure. *(quotation punctuation only if direct quotes used.)*
   - **G10 gate:** G9 set + concessive subordinators/adverb clauses, relative clauses, device-naming vocabulary, word-choice/wordiness.
   - **G11 gate:** G10 set + participial phrases *(optional)*, coordinating/correlative conjunctions, parallel structure, unclear-elements.
   - **G12 gate:** G11 set (all mature).
   - Each probe is timed production in composition context, not isolated identification. Failure routes to the owning app (EGUMPP conventions / AlphaWrite sentence craft), possibly a lower grade's content.

2. **The internal HS prerequisite DAG** (component + strategy skills; G10-4/G11-4 now revision passes inside G10-3/G11-2, not standalone nodes):
   `G9-1 -> {G9-3, G10-1}` · `G9-2 -> G9-4` · `G9-3 -> {G9-4, G10-2}` · `{G9-1,G9-2,G9-3} -> G9-4` · `G9-4 -> G10-3` · `G10-2 -> {G10-3, G11-3}` · `G10-1 -> G11-1` · `{G9-2,G11-1} -> G11-2` · `{G11-1,G11-2,G11-3} -> G12-1 -> G12-2`. Ordering law: no HS skill before its HS prereq; no HS skill before its gated granular prereqs pass; essay skills gate their component sentence tools cumulatively.

3. **The essay-decomposition rule:** no "essay" is a single teachable unit (K&H element-interactivity: 6+ interacting elements). Every essay skill (G9-4, G10-3, G11-2, G12-2) is taught in three stages (single-paragraph -> multi-paragraph -> timed), each stage gating the sentence tools it deploys.

**Why the council WAS convened here (vs. the placement questions):** this was REVIEW mode on a concrete artifact, not a placement dispute - the seats found real execution flaws (missing discriminations, essay overload, missing strategy layer, false prerequisites), which is exactly what review is for, not manufactured conflict. The principle (gated components + HS orchestration) survived unchallenged; the execution was corrected.

---

## 3. The scaffold (how HS-owned skills are sequenced)

Per Noel's prior decision: front-load the genre-general composition moves, distribute genre-specific moves just-in-time before each genre's paragraph/essay phase.

```
GRADE N COURSE
  0. ENTRY RETRIEVAL-GATE (fast; no re-teach)
     - Check the app-owned substrate: EGUMPP conventions + AlphaWrite sentence craft.
     - PASS -> proceed. FAIL -> route to the owning app (EGUMPP / AlphaWrite).

  1. PER-GENRE STRANDS (argument, informative, analysis, [synthesis/rhetorical @G11+])
     For each genre the grade runs:
     a. GENRE-SPECIFIC SENTENCE MOVE (claim, evidence, counterclaim, analysis, synthesis
        sentence) - taught JUST-IN-TIME right before...
     b. that genre's PARAGRAPH phase (build the genre paragraph; scaffold-fade
        worked -> completion -> independent; discrimination BEFORE production)
     c. the genre's ESSAY phase (assemble; composing-process rungs, NOT unit re-teaching)

  2. RHETORICAL / STYLE DELTA (the concision/precision-for-effect HS owns) - threaded
     into the revision phase, applied to whatever essay is current.

  3. CALIBRATION / REVISION - threaded across; conventions flagged holistically here.
```

**Ordering law:** no lesson before the phase teaching its prerequisites (genre-specific sentence move before its genre paragraph; essay after paragraph fluency).
**Within-lesson scaffold:** worked -> completion -> independent, discrimination before production. Discrimination/transfer items default to Timeback-deliverable shells (NO-CHANGE MC + hot-text, per the item-type catalog); production is external-grader-scored.
**Note:** because HS owns the COMPOSITION tier (not sentence mechanics), most HS lessons are paragraph/essay-unit, with genre-specific sentence moves as their just-in-time on-ramps. There is no front-loaded sentence-mechanics phase at HS - that work lives in EGUMPP/AlphaWrite.

---

## 4. Per-grade one-line summary

- **G9 (A1):** GATE EGUMPP+AlphaWrite substrate; OWN source-based claim + attributed-evidence + reasoning sentences -> single-source argument/informative essay.
- **G10 (A2):** GATE substrate; OWN counterclaim-aware claim + device->effect->warrant analysis sentence -> text-dependent analysis essay + argumentative precision delta. (Modal EOC year.)
- **G11 (B1):** GATE substrate; OWN nuanced claim + synthesis + rhetorical-analysis sentences/essays + rhetorical concision delta. (ACT/SAT year.)
- **G12 (B2):** GATE substrate; OWN AP sophistication (significance, context, competing perspectives) + sustained timed AP FRQ writing. (AP year.)

**HS-owned skill counts (after the council review reclassification):** 12 taught skills = 7 component sentence-moves (G9-1/2/3, G10-1/2, G11-1/3) + 5 genre strategies (G9-4, G10-3, G11-2, G12-1, G12-2). The former G10-4 and G11-4 "precision/concision deltas" are RECLASSIFIED as applied revision passes folded into the essay-revision phase (not standalone composition skills), per the TWR+DI finding that revision != orchestration. Each of the 5 genre-strategy skills is taught in 3 stages (single-paragraph -> multi-paragraph -> timed), so the buildable lesson count is larger than 12; the SKILL count is 12. All atop the fully-gated EGUMPP + AlphaWrite substrate.

---

## 5. Guardrails honored
- Teaches NO skill an existing app owns (parallelism/phrases/clauses/modifiers/substrate = EGUMPP/AlphaWrite, gated not taught).
- Every HS-owned skill funnels into a tested capability AND is owned by no app.
- Cross-pollination is explicit: app-owned mechanics are gated + applied, remediation routed to the owning app.
- Conventions scored holistically (not taught), matching how the tests score them.
- Timeback-deliverable item shells only (NO-CHANGE MC + hot-text default; no adaptive/graphic-gap-match).
- Every HS-owned skill is DECOMPOSED into its gated granular prerequisites (Section 2A): HS teaches the orchestration, the apps own the components. Council-reviewed 2026-07-08 (13 fixes applied): component vs genre-strategy skills separated; each skill names its ONE new discrimination (DI); essay skills carry a named genre strategy + self-monitoring (SRSD) and are decomposed into 3 stages (K&H); gates upgraded to timed-production probes; false prerequisites removed. The revised HS prerequisite DAG (12 nodes) is re-validated acyclic + forward-only.

## 6. Open verification (non-blocking, flagged)
- The app-stack mapping is K-8; confirm EGUMPP + AlphaWrite are actually ENROLLED for HS students in Timeback (not merely capable of spanning the 9-10 band) before finalizing the gate-remediation routing. If they are NOT deployed at HS, a thin HS conventions safety-net returns to scope. (Noel chose the gate-only reframe; this is the one assumption to verify with the Timeback/enrollment team.)
