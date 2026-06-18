# Acceptance Rubrics — the "Definition of Best" for the HS Writing course

**Why this exists.** Per the *Verification Is the Product* brainlift: the first move is to **write down what good means** as an inspectable artifact, *before* generating the thing — so quality is a checked bar, not an assertion. This doc is that bar for two deliverables: **(A) the unit-to-unit skills map** and **(B) the sourced direct instruction + passages.** Every later artifact (C1 as amended, each C3 lesson, each passage) is graded against these.

**Standard of proof chosen (2026-06-18):** verify **SOUND against the bar** for the map (+ instrument the cold gates as the empirical post-launch test); **acceptance-rubric + adversarial per-item verification** for DI/passages. No generate-and-judge tournaments (MVP scope). Honest claim this licenses: *"meets an explicit, inspectable bar,"* NOT *"beat all alternatives."*

**Scoring convention.** Each criterion = **PASS / CONDITIONAL / FAIL** with the evidence cited. Any FAIL blocks the artifact until fixed. CONDITIONAL ships with a logged follow-up. Golden anchors (a concrete passing AND failing example) accompany the subjective criteria so a judge — human or LLM — has something to calibrate against.

---

# Rubric A — Unit-to-Unit Skills Map

Graded once on C1 (as amended); re-checked whenever the sequence changes.

| # | Criterion | PASS bar | How checked | Evidence source |
|---|-----------|----------|-------------|-----------------|
| A1 | **Coverage** | Every assessed STAAR EI/EII + ACT skill has a dedicated teaching home (not just "reinforced"). | Walk the C2 crosswalk; every load-bearing SE = ✅ (dedicated beat). ◐ allowed only for holistically-scored conventions sub-SEs. Zero ✗. | C2_Standards_Crosswalk |
| A2 | **Dependency integrity** | No lesson requires a skill taught later (no backward edges). Each lesson installs exactly **one** new move. | Build the prerequisite graph from C1's "new move" column; assert it's a DAG with no forward references; confirm 1-new-move-per-lesson. | C1 + Verify_Architecture_LearningSci |
| A3 | **Difficulty / acquisition gradient** | Order matches a real difficulty+prerequisite ladder (lower-load before higher-load; paragraph before essay; single-source before paired/multi; untimed before timed). | Check each transition against the ladder; flag any inversion. | TWR ladder (corpus), Verify_Architecture_LearningSci A1 |
| A4 | **Mode correctness** | The primary-taught mode matches the verified assessment mode (expository/analytical primary for STAAR EI/EII; argument secondary/ACT). | Confirm U1–2 expository-primary, U3 argument, against the six-released-form evidence. | C2 §86–98 (VERIFIED) |
| A5 | **Curricular alignment** | Sequence is consistent with how credible real curricula scaffold (not idiosyncratic). | Compare to CommonLit 360 / Odell / CCSS progression. | Verify_Architecture_Curricula (ALIGNED) |
| A6 | **Retention architecture** | The map installs strategies to **automaticity** (Memorize-It) and uses **cross-unit retrieval/interleaving** — not just within-thread fade — so the cold gate isn't the first cumulative experience. | Confirm Amendments 1 & 2 are present: FACT/STOP+DARE carried to internal-before-timed; a prior essay type interleaved into later units. | C1_Amendments 1–2; Verify_Architecture_LearningSci "missing #1/#2" |
| A7 | **Transfer integrity (gates)** | Gates are cold, single-attempt, on reserved (never-taught) stimuli; rescore-loop runs only on practice. | Confirm C1 gate rows + C4 reserved-stimulus discipline; a stated re-gate policy exists. | C1 gates summary; C4 §reserved; Verify_Architecture_LearningSci #6 |
| A8 | **Scoped-out honesty** | Anything NOT covered (narrative, correspondence, research-location, etc.) is **explicitly declared** out-of-scope with reason — never silently omitted. | Confirm C2's ⊘ rows + rationale. | C2 §149–179 |

**The empirical "best" determinant (post-launch, instrumented now).** Soundness-against-bar is the pre-launch ceiling; the *real* proof the sequence taught is **cold-gate transfer**. Instrument from day one: (1) **gate pass-rate** per gate (the sequence works if cold single-attempt passes clear target); (2) **C5 self-vs-grader calibration delta** (shrinking delta = students internalized the criteria, i.e. the strategy transferred); (3) **rescore-loop frequency** per trait (which move students most re-enter = where the sequence is weakest). These turn "best" from claim into measurement.

**Skills-map golden anchors:**
- *PASS exemplar:* "U1 1.1 reason-not-restate → 1.3 cite+explain → 1.4 controlling-idea" — each step one new move, no backward edge, lower-load (working claim) before higher (refined thesis). ✅ A2/A3.
- *FAIL exemplar:* the pre-amendment build's "L2 take-a-position before L3 reasoning" — required defending a position before the reasoning move that justifies it (backward dependency); and "L5 full essay" before the component moves were automatic (gradient inversion + the brainlift's named failure mode). ✗ A2/A3.

---

# Rubric B — Sourced Direct Instruction + Passages

Graded **per item** (each DI block, each passage). Adversarial verification: a checker tries to FAIL each criterion before passing it.

## B-DI — Direct Instruction quality

| # | Criterion | PASS bar | How checked |
|---|-----------|----------|-------------|
| D1 | **Grounding label (honest)** | Carries one of: **real-lesson** (a source teaches it this way, cited verbatim + page/URL) / **our-synthesis** (assembled from sources) / **new-ground+nearest-cousin** (no clean source; nearest fit named). No claim is dressed up beyond what the source supports. | Each `quote/url` resolves to content the source actually contains (the L3/L4/CCSS mis-citation class is an automatic FAIL). |
| D2 | **Engelmann conformance** | Example/non-example pairs hold one dimension constant and vary only the target; includes a **sameness set** (2–3 maximally-different positives under one label, so students don't over-stipulate); the "test" applies the move to a **new** example, not the modeled one. | Audit each DI block's pair + test against Engelmann pp.63–66; the "model on topic B, test on topic A" / scaffold-fade structure satisfies test-on-new. |
| D3 | **Teaches the scored lever** | The DI targets the move the C5 rubric actually scores — for expository, the **evidence-explanation 3→2→1 lever** ("Clarify": explain HOW the evidence supports the controlling idea, not drop the quote). | Map each DI block to a C5 discriminator / negative exemplar; a block that teaches an unscored flourish (e.g. tone/imagery in U1) is a FAIL. |
| D4 | **Copy-resistance** | A student cannot pass by copying the model; independence is forced (scaffold-fade: model removed + new source in later rounds; mnemonic self-check is internal at the gate). | Confirm the fade phase is present; the production rep uses a stimulus the model didn't. |
| D5 | **Mnemonic fidelity** | Uses the house mnemonic exactly (FACT for expository; STOP+DARE for argument) — consistent wording everywhere; no invented variant. | Check letter expansions against SRSD Activity Specs / Integration Brainlift; no drift across lessons. |
| D6 | **Coping model** | The model shows the move **failing then repaired** (dropped quote → "this shows…" link added), not a flawless exemplar. | Confirm the DI model includes the false-start/repair beat. |
| D7 | **Voice (Yeager)** | Feedback/coaching follows "high standards + I believe you can meet them"; names the move with shared vocabulary; never bare "wrong." | Spot-check coach strings against the C5 feedback contract + Yeager tone. |

**B-DI golden anchors:**
- *PASS:* "Clarify the evidence" DI — rule (warrant defined, cited Toulmin), coping model (dropped quote → repaired with "which shows the passage's point that…"), pair (explained vs. dropped, one constant topic), test on a **new** passage. real-lesson label. ✅ D1–D4,D6.
- *FAIL:* a DI block citing K20/Edutopia for content those pages don't contain (✗D1); a model demonstrated on phones then tested on phones (✗D4); teaching "defensible position / argue-vs-persuade" inside the expository U1 (✗D3 — unscored mode).

## B-PASS — Passage / stimulus quality

C4 already defines these acceptance criteria; this restates them as a per-passage checklist.

| # | Criterion | PASS bar | Source |
|---|-----------|----------|--------|
| P1 | **Reading level on-grade** | Measured Lexile in the CCSS 9–10 band (~1010–1150 EI, upper half EII); ships with measured Lexile + 1-line readability note. NOT AP/college. | C4 §constraint 1 |
| P2 | **Content-bearing, low prior-knowledge** | Contains a real idea a student can form a controlling idea about / explain, with no required outside knowledge (self-contained). | C4 §2 |
| P3 | **Mode-appropriate** | Informational/analytical passages support a controlling idea about content; argumentative present a debatable issue; synthesis sets genuinely combine (cross, not parallel; shared themes; a credibility/bias contrast in ≥1 set). | C4 §3, §synthesis-design |
| P4 | **Copyright-clear** | Public-domain / openly-licensed / commissioned-original; licensing flagged per item. | C4 §4 |
| P5 | **Reserved discipline** | Gate passages tagged RESERVED, stored separately, never shown in instruction. | C4 §5 |
| P6 | **Facts verified (no slop)** | Every figure/claim in the passage traces to a real, cited source; anything unverifiable is omitted, not invented. | (our no-slop rule; the phones/four-day/AI passages already follow this) |
| P7 | **Length to spec** | Single ~500–800 words (EI); sets within the STAAR ~6,000-word form ceiling. | C4 §6 |

**B-PASS golden anchors:**
- *PASS:* the verified phones passage — on-grade, self-contained, debatable, every figure cited (Beland&Murphy/Birkenstein... wait: Beland&Murphy/Birmingham/UNESCO), licensing notable. ✅ (note: currently argument-mode → relocate to U3; an *expository* sibling is needed for U1).
- *FAIL:* a passage with an invented statistic (the original "6% / discipline referrals drop"); an AP-level rhetorical-analysis speech selected for craft (✗P1/P3 — wrong level + wrong mode for the STAAR re-aim).

---

## How these rubrics get used (the workflow)
1. **Map:** run C1+amendments through Rubric A → fix any FAIL → record PASS/CONDITIONAL per criterion. (Mostly confirmation; A6 depends on Amendments 1–2 being approved.)
2. **C3 authoring:** every DI block authored *to* B-DI; every passage acquired/written *to* B-PASS.
3. **Adversarial pass:** a verifier tries to FAIL each item against its criteria + golden anchors before it ships.
4. **Post-launch:** the A-section gate instrumentation turns "sound" into measured "best."

## Open
- Rubric A criterion **A6** (retention architecture) only passes if Amendments 1 & 2 are approved — so the amendment-approval gate and this rubric are coupled.
- B-DI **D3** assumes the C5 levers are the definition of "scored" — correct for STAAR/ACT; AP levers differ and are out of MVP scope (honestly capped, per the brainlift).
