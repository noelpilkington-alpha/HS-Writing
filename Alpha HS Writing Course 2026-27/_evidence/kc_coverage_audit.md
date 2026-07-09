# KC Map Coverage Audit — Adversarial Backward-Trace (findings)

**Method:** 4 test-family finders (STAAR, ACT/SAT, AP Lang/Lit, SBAC/Regents/state-EOC) each decomposed real released-item DEMANDS (from the documented item structure + public rubrics; NO copyrighted item text) and traced each demanded skill to a KC / GATED app / UNCOVERED. Plus 1 red-team constructing own-words breakers. Run 2026-07-08. This validates COVERAGE (every tested skill has a home), NOT efficacy (that needs student field data).

**Headline:** the reconciled KC map is INCOMPLETE. Multiple independent agents converged on the same gaps (convergence = high confidence). The gaps fall into two classes: (1) genuine genre/skill holes, (2) skills the gap-analysis reframe over-gated to apps that the apps may not actually deliver.

---

## CONFIRMED GAPS (ranked; corroboration in brackets)

### CRITICAL

**G1. Narrative writing — ZERO KCs.** [SBAC/Regents finder + red-team, highest-confidence for both]
7 systems test narrative as a scored CR genre with dedicated craft rubrics (LA LEAP NWT, MD MCAP, TN Eng I/II, NJ NJSLA NWT, SBAC option, MS MAAP, IA ISASP), 15-24 pts. The entire HS map is argument/analysis/synthesis. CCSS W.3 (narrative) is a core standard, parallel to W.1/W.2. Narrative craft (plot, characterization, dialogue, POV, scene) is NOT gated (not sentence mechanics, not reading) and NOT owned by any KC. **Decision needed: descope explicitly (document the 7 systems we skip) OR add G9-10 narrative KCs.** Note: prior work (College Essay/SCENE) is the only narrative artifact and it's a separate add-on.

**G2. Informational/explanatory thesis has no clean home.** [STAAR finder, sharpest STAAR gap]
STAAR's DOMINANT ECR mode is informational (all 2023-25 released ECRs were informational), demanding a controlling-idea/thesis ("The author develops the idea that X") distinct from an arguable claim. C.9.01 is "defensible claim" (argument-coded); C.9.04 blurs "argument/informative" at the essay level with no sentence-level informational-thesis KC. The most-tested STAAR mode lacks a home. **Fix: add a G9 informational controlling-idea KC (sibling to C.9.01), and de-blur C.9.04 into distinct argument vs informational strategies.**

**G3. AP Lang Q3 argue-from-own-knowledge (source-free) — UNCOVERED.** [AP finder, sharpest AP gap; red-team Breaker 7]
AP Lang Argument FRQ (33% of Section II) + ACT Writing are STANDALONE: no source, generate evidence from own knowledge. ALL HS-owned KCs are source-based (C.9.02 attributed-evidence, C.9.04 single-source, C.11.02 synthesis, C.11.03 rhetorical-analysis). The prior B1L map HAD C.AP.L.08 "Generate Evidence from Knowledge" - lost in reconciliation. **Fix: restore a source-free argument-from-knowledge KC at G11.**

**G4. Entire AP Literature track — ZERO KCs.** [AP finder + red-team Breakers 5-6]
AP Lit = poetry analysis + prose-fiction analysis + literary argument. Our analysis KCs (C.10.02 device->effect, C.11.03 rhetorical-analysis) are explicitly NONFICTION/rhetorical. No poetry (meter, volta, form), no fiction (characterization, narrative POV, symbolism), no literary interpretation. The KC map is AP-Lang-only. **Decision needed: descope AP Lit explicitly (and remove the "alternate track" reference) OR add 3-5 literary-analysis KCs.** (Note: this aligns with the prior decision to exclude the AP Lit sub-track "for now" - but the map still names an alternate track, so it must be reconciled.)

### HIGH

**G5. "Production of Writing / Expression of Ideas" (add-delete-for-purpose, transitions/cohesion, organization) — UNCOVERED, no owner.** [ACT/SAT finder sharpest gap + SBAC finder mis-gating #1 + red-team Breakers 3, 9 - QUADRUPLE corroboration]
This is 38-43% of ACT English + a full SAT domain + a large share of STAAR revising items. It is NOT sentence conventions (EGUMPP doesn't own it) and NOT essay composition (our KCs don't cover it) - it sits in no-man's-land between GATED and HS-OWNED. Demanded skills: should this sentence be added/deleted for relevance? which transition fits the logical relationship? what is the most logical sentence/paragraph order? **This is the single most corroborated gap. Fix: add a discourse-level rhetorical-revision KC family (transitions/cohesion, add-delete-for-purpose, organization/sequencing), likely G10-G11, taught as discrimination (SR shells) + applied in revision.**

**G6. Multi-source (2-3 text) writing at G10 — straddles the single/synthesis gap.** [SBAC/Regents finder, 2nd-sharpest]
The modal G10 EOC is 2-4 SOURCE cross-text writing (NY, FL, MA, MD, SC, LA, NJ). Our map has only C.9.04 "single-source" (G9) and C.11.02 "synthesis" (G11, 6-source AP model). The 2-3 source G10 middle ground (cross-text comparative evidence integration, short of full synthesis) is uncovered. **Fix: add a G10 multi-source argument/analysis KC OR explicitly widen C.10.03 to cross-text (2-3 source).**

### MEDIUM

**G7. AP sophistication (Row C) taught only at G12 - too late.** [AP finder + red-team Breaker 4]
Row C (significance/context/complexity) is the 5-vs-6 differentiator on EVERY AP FRQ, and G11 is the Track-B gate where students first hit FRQs. Teaching it only at G12 (C.12.01) means G11 FRQ practice encounters an untaught criterion. Also: ACT Writing (G11, often G10) scores "context/significance" from score-3. **Fix: introduce significance/context at G11 (woven into C.11.02/C.11.03), master at G12.**

**G8. Source credibility/bias evaluation — UNCOVERED.** [red-team Breaker 2; prior Skills_Standards_Gap_Analysis flagged 11(G)(i)/(H) as the two real actionable gaps]
Tested in SBAC/PARCC/research-simulation performance tasks (evaluate which source to trust + why). Our KCs USE sources (attribute, synthesize) but never EVALUATE them. The prior gap analysis already flagged credibility/bias + citation/plagiarism as the two actionable research gaps to add to the synthesis unit. **Fix: add a source-evaluation KC to the G11 synthesis unit (cheap; the read-the-source step exists).**

### LOW / NON-ISSUES (noted, no rebuild)
- **Short-CR vs full-essay** (NY Regents Part 3, PA Keystone): same skill, different length. Interpret C.10.03 as "analysis extended-response," not strictly 5-paragraph. No action unless the platform hard-codes essay length.
- **Precision/concision item-FORMAT transfer** (ACT/SAT SR vs essay revision): skill covered (C.10.04/C.11.04); ensure lessons practice the SR shell too. Pedagogical, not a skill gap.

---

## MIS-GATING (skills gated to apps that the apps may NOT deliver - VERIFY before trusting the gate)
1. **Discourse-level revision** (organization/coherence/unity/evidence-in-context) gated to EGUMPP/AlphaWrite, but those are sentence-CONVENTIONS apps; they likely do NOT teach paragraph/discourse revision. This is the flip side of G5. **Must verify what EGUMPP/AlphaWrite actually cover before relying on the gate.**
2. **Vocabulary-for-effect** (precision/concision/tone) gated to AlphaRead/AlphaWrite, but their vocab is G3-8-scoped; may not reach HS rhetorical word-choice. **Verify.**
3. **Reading comprehension at AP Lexile (1200-1400L)** gated to AlphaRead, but if AlphaRead is G3-8-scoped it may not reach college-level text. **Verify AlphaRead's ceiling.**

These three mis-gatings share ONE root cause + fix: the "gate to app" decisions assumed the apps cover the HS band. That assumption is the SAME open item already flagged in the roster (confirm EGUMPP/AlphaWrite/AlphaRead HS enrollment + ceiling). The audit RAISES its priority from "nice to confirm" to "blocking" - because if the apps stop at G8, several "GATED = covered" cells are actually UNCOVERED.

---

## What the audit CONFIRMED is correct (survives - don't over-correct)
- Argument spine G9-G12 (claim -> evidence -> reasoning -> counterclaim -> nuanced -> synthesis -> rhetorical-analysis): cleanly traces to KCs, well-covered.
- Sentence CONVENTIONS gated to EGUMPP: correct (IF enrolled at HS - see mis-gating).
- Reading comprehension + vocab gated to AlphaRead: correct in principle (IF HS-scoped).
- The AP synthesis + rhetorical-analysis FRQs (Lang): covered by C.11.02/C.11.03.
- Counterclaim @ G10: covered (STAAR Eng II, SBAC, MD all trace to C.10.01).

## Honest ceiling
This proves COVERAGE (no tested skill is homeless), not EFFICACY (that a student taught these KCs passes). Efficacy needs field data with real students, which we do not have. A clean coverage audit means "no student fails for a reason we failed to cover" - the necessary condition, not the sufficient one.
