# G11/G12 Test + Standard Demands, and the Replication Plan

**Purpose:** before building the G11/G12 test banks, state what the standardized tests + ACC/CCSS standards
require students to DO at those grades, so generation targets the right modes/anchors/stimuli. Synthesized
from already-verified evidence (ReleasedTests/batch2-5, skills_by_grade_crosswalk.html, TestDesign_Reference.md,
_evidence/kc_coverage_audit.md, 05_AlphaCommonCore_Writing_Spine.md, the KC map). No new research here.

**Decisions (Noel, 2026-07-08):** (1) **G12 = AP Lang only**; AP Lit (poetry/prose-fiction/literary analysis)
stays the named-but-deferred backlog. (2) **Gather G11 verbatim anchors FIRST**, then build stimuli + items
(blueprint L1 -> L3 -> L4 discipline; no generation before anchors).

---

## GRADE 11 - "the college-test year" (heaviest-tested writing year)

**Who tests it:** SBAC (CA/OR/WA/ID/HI/SD), ACT (~16 states), SAT (~10), NY Regents, AP Lang. Band = **1120-1300L**.

**The FOUR distinct writing tasks G11 must cover (not one EOC essay like G9/G10):**
| Task | Tests | Student must DO | KC |
|---|---|---|---|
| Multi-source SYNTHESIS | SBAC full-write (4 src), AP Lang synthesis (6 src), NY Regents Pt2 (4-text) | weave ONE argument across 4-6 sources (not source-by-source) | C.11.02 |
| RHETORICAL ANALYSIS | AP Lang RA FRQ, NH SAT essay, FL G11 | analyze author's rhetorical CHOICES + effect/purpose | C.11.03 |
| SOURCE-FREE argument | AP Lang Argument FRQ (33% of exam), ACT | argue from OWN knowledge, no source to cite | C.11.06 |
| MULTI-PERSPECTIVE argument | ACT Writing | weigh 3 GIVEN perspectives, position own | C.11.07 |
Plus: nuanced claim (C.11.01), source credibility/bias (C.11.08), rhetorical concision (C.11.04), timed strategy (C.11.05).
Plus SR editing tier: ACT English ~40% "Production of Writing" (transitions/add-delete/organization) - owned by C.9.06/C.10.05 (already built) + the Language course.

**Standards:** 11-12 band - W.11-12.1 (nuanced argument), W.11-12.7-8 (research/synthesis), W.11-12.9 (analysis),
L.11-12.3 (style). ACC adds INQ.1 tested slice (source evaluation).

**Why G11 is NOT a G9-style clone (the build implications):**
1. NEW anchor types: SBAC full-write, ACT Writing (3-perspective), AP Lang FRQ - NOT the STAAR/MCAS/Regents essays used for G9/G10.
2. NEW stimulus shapes: synthesis needs 4-6 source SETS; rhetorical-analysis needs nonfiction-with-analyzable-craft; source-free argument needs NO source (prompt only). Different stimulus_contract profile than single/opposing-pair.
3. NEW rubric config: rc.ap (Thesis 0-1 + Evidence/Commentary 0-4 + Sophistication 0-1 = 6) - exists in the contract, not yet exercised.

---

## GRADE 12 - "the AP mastery tier" (thin, depth-focused)

**Who tests it:** essentially NO state summative writing test - AP Lang/Lit only (+ some VA G12 technical). Band = **1185-1385L** (college-ready).

**What's genuinely new (only 3 KCs, by design - G12 rides on G11):**
- **AP sophistication** (C.12.01): significance/"so-what" + broader context + competing perspectives = the AP Row C point, the 5-vs-6 differentiator.
- **Sustained timed writing** (C.12.02): produce G11-level synthesis/analysis/argument in exam time. (Documented AP failure mode = timed transfer, not knowledge.)
- **Voice through syntactic choice** (D.12.01, woven).

**Scope: AP Lang ONLY.** AP Lit (poetry analysis, prose-fiction analysis, literary argument, literary devices) is DEFERRED - if un-deferred later, that is 3-5 new KCs + literary-text anchors/stimuli BEFORE a G12-Lit build.

---

## The replication plan (G11 first, then G12)

**G11 - Layer 1 (anchors) FIRST:**
- Gather verbatim anchors (forms + rubrics + annotated samples where public), own-words/reference-only per the copyright posture:
  - **SBAC full-write** (argument + explanatory, 4-source PT) - rubric: Org/Purpose 1-4 + Evidence/Elab 1-4 + Conv 0-2.
  - **ACT Writing** (3-perspective standalone) - 4 domains 1-6 (Ideas&Analysis / Development&Support / Organization / Language Use).
  - **AP Lang FRQ** (synthesis 6-src, rhetorical analysis, argument) - the 6-pt rubric (Thesis 0-1 + Ev&Comm 0-4 + Soph 0-1) = rc.ap.
  - Acceptance bar: >=2 with a complete anchor (form + rubric + annotated samples). AP Lang rubric is public; SBAC has released PTs + rubrics; ACT has released prompts + the 4-domain rubric.
- **Layer 3 stimuli:** synthesis 4-6-source SETS (own-authored federal-fact or PD, at 1120-1300L) + rhetorical-analysis nonfiction (PD speeches/essays) + source-free argument prompts (no passage). Grade-aware contract already supports grade="11".
- **Layer 4 items:** CR (synthesis/rhetorical-analysis/source-free-argument/multi-perspective) bound to the stimuli, rubric_ref="rc.ap" (+ rc.sbac/rc.act if added) ; SR carries over the Production-of-Writing families. IDs in a G11 range (e.g. 07xx+) to avoid G9/G10 collision.
- **Cross-check:** `testbank_kc_crosscheck.py G11` green.

**G12 - after G11 (reuses G11 stimuli):**
- Anchors: AP Lang FRQ (already gathered for G11). Stimuli: reuse G11 synthesis/analysis sets + AP-level source-free prompts. Items: sophistication-focused CR at rc.ap; timed-condition variants. Cross-check `G12` green.

**Open items:** rc.ap already in RUBRIC_CONFIGS; may add rc.sbac / rc.act configs. Lexile gate already supports G11 (1120-1300) + G12 (1185-1385). Anchor-gathering hits web-fetch friction on College Board/ACT (gated) - expect reference-only + own-words.
