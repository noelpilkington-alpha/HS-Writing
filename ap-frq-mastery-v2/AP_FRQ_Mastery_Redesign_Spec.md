# AP FRQ Mastery — Hybrid Build Plan (v3, for approval)

A standalone path from a **typical on-grade 8th-grade writer** to **AP FRQ
performance**. This plan **keeps the existing `ap-essay-course` Track-1 audited
lesson map as the backbone** and **grafts on three additions** that fix the three
things the prior work was missing — without scrapping finished, audit-passed work.

> **How this came to be.** The first redesign (v2) proposed a clean rebuild
> ("exam-agnostic core + 6 overlays"). An adversarial scope evaluation (two
> advocates + a neutral judge, 7 criteria) scored v2 and the existing V1 backbone
> a **dead tie, 48–48**, and concluded the honest answer is **a hybrid**: V1 wins
> decisively on transfer discipline, build-readiness, and time honesty; v2 wins
> decisively on exactly the user's three complaints (G8 bridge, practice depth,
> coverage). The grafts are **additive to V1's map, not a rebuild**. This document
> is that hybrid.

---

## 0. The decision and the locked constraints

**Decision:** do **not** rebuild. **Keep** V1's completed Stage-02 lesson map
(`ap-essay-course/stages/02-lesson-map/output/ap-lesson-map.md` — 27 lessons,
audit-passed, "Ready for Stage 03") and its transfer-respecting scope boundary.
**Graft** the three fixes. **Defer** the unverified families.

| Element | Disposition | Why |
|---------|-------------|-----|
| V1 Unit 0 + Units 1–4 (feedstock-routed Lang/History) | **KEEP** | Audited; one stage from content. Its spine is the genuinely transferable core. |
| V1 transfer discipline (essay families on the spine; SAQ/EBQ/Lit/Gov as **separate non-spine modules**) | **KEEP** | The transfer matrix proves the spine barely reaches non-essay families; bundling them is the "all-14-subjects" anti-pattern. |
| **Graft 1 — G8 bridge, built FIRST** | **ADD** | V1's bridge scored a 2/10: it exists only as deferred prose, scheduled last. This is the user's fix #1. |
| **Graft 2 — rescore loop + mandatory reasoning-gating** | **ADD** | V1 gates *sourcing* but not the reasoning/analytical sentence — the exact moves the course exists to fix. This is fix #2. |
| **Graft 3 — standalone History SAQ module** | **ADD** | An APUSH student in V1 is missing SAQ (20% of the score). Shipped as a separate non-spine module, the right way. Fix #3, bounded. |
| Per-rep minute accounting + content-vs-writing boundary | **ADOPT** | Makes V1's (uncapped) timing auditable. |
| Grader-calibration launch gate | **ADOPT** | The rescore multiplier depends on a reliable grader on the noisy rows; calibrate before any gateway-locked lesson ships. |
| EBQ, Gov, AP Lit | **DEFER** | CEDs not in the repo / unverified. Each is its own future design pass with a verification gate — **not a named promise now**. |
| 6 tracked mental models → 2 + 1 | **APPLIED (2026-06-10)** | Done in the splice: keep S-F-E + Claim Hierarchy; fold M1+M5 → the Function Question; demote M3 → "rhetorical situation" and M6 → "HIPP-as-procedure". Recovers Teach-beat time. |

**Locked decisions carried from your earlier answers:** standalone from a typical
on-grade G8 writer; reliable AI grader assumed; fixed linear path; mental models
kept (consolidation optional); spec-first then build. **Time:** single-exam fits
~22–26h; multi-exam costs more and is **stated openly** (§7) — but note the hybrid
*lowers* the multi-exam blowout vs v2, because we are not building six overlays.

### The three fixes, mapped to grafts

1. **Weak G8 bridge →** Graft 1: a real 6-lesson bridge from the CCSS W.8.1 floor,
   built **first**, prepended to V1's Unit 0 (§3).
2. **Too little real practice →** Graft 2: the Judgment Ladder rescore loop added to
   V1's existing Revise beat, + mandatory discrimination-gating on every new move
   including reasoning (§4).
3. **Too narrow →** Graft 3: the standalone History SAQ module (§5), closing the
   APUSH gap. EBQ/Gov/Lit follow as verified future passes, not now.

---

## 1. Architecture at a glance

```
TYPICAL G8 WRITER
   │
   ▼
GRAFT 1 — G8 BRIDGE  (6 lessons, ~6.5h, built FIRST)
   │   B1→B6: reasoning-link → fluency → function-lens(own) → function-lens(text) → thesis-refinement → cold knowledge-essay gate
   │   gate: argue-from-KNOWLEDGE short essay, Thesis + Reasoning, cold  ── compatible with V1 Unit 0 gate
   ▼
V1 BACKBONE (KEPT — audited Stage-02 map, feedstock-routed by subject)
   Unit 0  SPINE          claim→evidence→reasoning; thesis as refinement      [Lang + History]
   Unit 1  ANALYZE (RA)   read author's choices via S-F-E                     [Lang only]
   Unit 2  ARGUE/KNOWLEDGE Lang Argument / History LEQ                        [Lang + History]
   Unit 3  ARGUE/SOURCES  Lang Synthesis / History DBQ (+ a dedicated         [Lang + History]
                          document-reading rep before the first DBQ)
   Unit 4  HIGHER-ORDER   Sophistication (Lang) / Complexity (History), timed [Lang + History]
   │   Lang = all 5 units (15 lessons) · History = Units 0,2,3,4 (12 lessons)
   │   GRAFT 2 runs inside every unit's Revise beat (rescore loop) and gates every new move
   ▼
GRAFT 3 — SAQ MODULE  (standalone, ~3.5h, NON-spine)
   History SAQ (World/USH/Euro): verb-bound A/B/C, no thesis, own per-part scorer
   (an APUSH student takes History units + this module)

DEFERRED (own future verification pass each): Psych EBQ · AP Gov Argument · AP Lit
```

**The transfer logic that keeps this honest:** the argument-essay spine (Thesis →
Evidence → Reasoning → Higher-Order) is the high-leverage, genuinely transferable
core, so it carries Lang + History. SAQ inverts the spine (no thesis, no line of
reasoning), so it is **not folded onto it** — it is a separate module with its own
scorer. That is V1's firewall instinct preserved, while still shipping SAQ now.

---

## 2. What changes in the existing pipeline (concretely)

This plan operates on the existing `ap-essay-course/stages/` pipeline. Nothing in
V1's audited Unit 0–4 map is discarded; the edits are surgical.

| File / artifact | Change |
|-----------------|--------|
| `stages/02-lesson-map/output/ap-lesson-map.md` | **Prepend** a Bridge block (B1–B6) ahead of Unit 0; **add** to each lesson's *Generate* row the rescore-loop + (where the lesson introduces a new move) a **gated** discrimination sort; **add** the History dedicated document-reading rep before 3.1. |
| `stages/01-course-outline/output/ap-course-outline-v2.md` | Update §3 (unit spine) to show the Bridge as the entry phase, built first; update the build sequence (Bridge → Unit 0 → … not "Track 1 first, foundational phase last"). |
| **New:** a standalone **SAQ module** lesson block (3 lessons) + its per-part binary scorer spec. | Lives outside the spine; History/APUSH students take it after Unit 4 (or interleaved). |
| `references/04-course-design/*` | Record the hybrid decision; mark EBQ/Gov/Lit as deferred future passes (not v1.1 promises). |
| Mental models | Optional: demote M3/M6 to operational procedures (rhetorical situation, HIPP-as-procedure) and the M1+M5 fold (§9). |

> **What we are NOT doing:** no "supersede the Track-1 spec," no relabeling Units
> A/B/C, no six-overlay commitment, no broken 20–30h promise. The earlier v2
> spec's restructure was forced by its own accounting failure; the hybrid avoids
> that by keeping V1's structure intact.

---

## 3. Graft 1 — The G8 bridge (6 lessons, ~6.5h, BUILT FIRST)

**This is the highest-priority graft and it must be built first, not deferred the
way V1 deferred its foundational phase.** The single biggest risk of the hybrid is
that the team keeps the audited backbone, declares victory, and re-shelves the
bridge — recreating V1's exact failure under a hybrid banner.

**The G8 floor (don't re-teach):** per CCSS W.8.1 a typical on-grade G8 writer can
already state a claim, distinguish it from an opposing claim, attach evidence, give
a reason, and conclude; per W.8.2 write a structured expository essay; per W.8.7–9
quote/paraphrase/cite. **The three true deltas the bridge installs:** (1) write
reasoning that *explains how* evidence supports a claim, not restates it; (2) read
a text for what its parts *do* (function), not what they *say*; (3) read and
self-score against a real AP rubric.

| # | Lesson | New move (one only) | Rep | Scaffold |
|---|--------|--------------------|-----|----------|
| B1 | **Reason, not restate** | Write the sentence that *links* evidence to claim ("so what? / why does this prove it?"). **Gated** restate-vs-reason sort first, then write 3 reasoning sentences from knowledge. | Partial-plan | Heavy |
| B2 | **Reason to fluency** | Same move, 2–3 fresh knowledge prompts, until automatic (the #1-documented G8 deficit gets its own consolidation — not stacked under a new abstraction). | Partial | Heavy→Medium |
| B3 | **Your essay is a set of choices** (the function lens) | Turn the **function question** ("what is this sentence *doing* here?") on the student's OWN paragraph — **no new production**; the lens *is* the move (mirrors A1 L06). | Lens-only | Heavy |
| B4 | **Same lens, someone else's text** | Apply the function question to a SHORT, accessible published argument (~200 wds). **Pre-read comprehension check first**, then a gated content-vs-function sort, then write 3 function sentences. | Partial-para | Medium |
| B5 | **Thesis as a refinement + the paragraph** | Sharpen a position into a defensible thesis (60-sec refinement of a claim they already wrote), then write one full claim/evidence/reasoning paragraph; self-score 3-point. | Partial-para | Medium |
| B6 | **Bridge gate — full short argument, cold** | *No new move.* Thesis + 2 reasoning-bearing body paragraphs + close on a fresh **argue-from-knowledge** prompt, cold, AI-scored. | Full, cold | Light→None |

**Bridge gate is knowledge-only** (Thesis + Reasoning), which is **exactly
compatible with V1's existing Unit 0 gate** (also Thesis + Reasoning) — so the
bridge slots in front of Unit 0 with no seam. The first text-analysis *essay* is
deliberately deferred to Unit 1 (Lang) / the dedicated reading rep (History), never
cold-gated before it is taught.

**Comprehension scored separately from writing** (B4 + the History reading rep): a
failed rep routes by *root cause* (re-read support vs more reasoning reps), because
the diagnosed population reads 2–3 grades behind and the grader sees only output.

---

## 4. Graft 2 — The practice engine (the rescore loop + mandatory gating)

V1 already has solid practice (~14–16 Lang / ~11–12 History reps, discrimination
beats, coping-model false starts, weak/strong sourcing pairs). Graft 2 adds the
**two things V1 lacks**, both as Stage-03 generation requirements layered onto
V1's existing AlphaWrite cycle — **no structural change to the map**.

### 4a. The rescore-the-weakest-row loop (into V1's existing Revise beat)

Every full rep already POSTs to the AI grader in V1's design. The graft: the grader
names the **single weakest row**, the student **rewrites that row only and
rescores**. One essay → **2–3 graded reps** of the highest-leverage move at near-
zero clock cost (a row rewrite is ~10–15 min on reasoning/sourcing rows, not a
fresh 40-min essay — counted honestly in §7, *not* "free"). **Guard:** rescore is
same-essay, never on a gate; gates are single-attempt cold reserved passages, so
**transfer, not local patching, unlocks progression**.

### 4b. Mandatory discrimination-gating on EVERY new move (including reasoning)

This is the sharpest finding of the evaluation: V1 gates *sourcing* (3.2 has 2–3
weak/strong pairs) but the **reasoning-link sentence (0.1)** has only a binary
self-check and the **analytical sentence (1.1)** likewise — *the very moves the
course exists to repair are the ones it leaves ungated.* The graft makes a **gated
Rung-0 sort a non-negotiable Generate-row deliverable for every new-move lesson**,
verified in the Stage-02 re-audit:

- **0.1 / B1** — restate-vs-reason sort, **locks the write** until classified.
  (Negative exemplars are authoritative: the LEQ failing example "The Khmer Empire
  adopted Buddhism" = bare evidence; the Lang Row B 1-pt "summarizes without
  explaining.")
- **1.1** — feature-spot-vs-function sort, locks the write.
- **4.1** — "however some disagree (no payoff)" vs real qualification, locks the
  timed write.
- (Sourcing 3.1/3.2 already gate — keep as-is.)

### The loop, stated once (runs in every lesson)

`JUDGE (gated sort, 2–4 min, hard cap) → MODEL (one coping-model worked example
with a deliberate false start, then the correction) → WRITE the rep → AI-SCORE +
REWRITE THE WEAKEST ROW`. Scaffold fades Heavy → Medium → Light → None within and
across units (V1's existing fade). This is the "Judgment Ladder."

### Calibration ladder (coached/surfaced, NOT a progression lock)

Binary self-check (bridge) → 3-point (Unit 0) → AP-rubric self-score (Units 2–4) →
self-diagnosis under the clock (Unit 4). On every full rep the student self-scores
*before* the grader returns; the engine surfaces the `|self − grader|` gap.
**Decision (locked):** the **cold gate alone gates advancement** — a strong writer
who is a weak self-scorer is never stalled. Calibration accuracy is tracked, shown,
and feeds self-diagnosis training, but does not by itself unlock the next unit.
**Guard:** on rows the grader is known-noisy (Row B 3-vs-4, sourcing, complexity),
calibration is measured against the **human-authored weak/strong key**, not the raw
grader score.

### AI-grader contract (curriculum specifies WHAT; dev team owns HOW)

- **Assesses** the real AP rubric rows per feedstock, swapped by `data-rubric` ID
  (Lang Row A/B/C; DBQ 7-pt; LEQ 6-pt; **SAQ per-part binary** — its own scorer).
  Highest-leverage judgment: the **Row B 2→3→4 line-of-reasoning gate** and the
  **History sourcing because-clause** (HIPP named *and* relevance explained;
  naming alone = 0).
- **Returns** per-row score + reasoning; the **single weakest row** named; one
  concrete next step; the self-vs-grader delta; pass/fail JSON on gateway reps.
- **Modes:** grade; **rescore** (one named row after a targeted rewrite — the
  multiplier); **gateway** (pass/threshold for cold gates).
- **HARD LAUNCH GATE:** before any gateway-locked lesson ships, **calibrate the
  grader against official AP anchor papers** on the noisy rows to within 1 point on
  ≥80% of a held-out set. Until then, cap the rescore multiplier on those rows or
  route feedback through the human key.
- **Known limits:** grades *written reasoning, not reading comprehension* (a
  misread looks like a sourcing failure → the comprehension pre-check carries that
  load); rubric **drift** → store rubrics as **patchable config keyed to a CED
  build-date**; SAQ needs its **own bounded per-part scorer**, not the spine rows.

---

## 5. Graft 3 — The standalone SAQ module (History, ~3.5h, NON-spine)

SAQ is the highest-volume FRQ type and ~20% of the APUSH score; a "Lang+APUSH"
student who skips it is not exam-ready. It is shipped **now** but **as a separate
non-spine module** — because the shared transfer matrix proves the spine barely
reaches it (History thesis 2%; evidence-integration and S-F-E don't transfer).

| Distinct moves (the spine does NOT teach these) | Reuses from the spine |
|--------------------------------------------------|------------------------|
| **Verb-bound answering**: identify < describe < explain (the signature failure is answering "describe" when the prompt says "explain") | The reasoning *sentence* (causal because-clause) = the "explain" move shrunk to one sentence |
| **Bounded A/B/C format**: 1 pt/part, all-or-nothing, **no thesis, no line of reasoning**, 1–2 sentences/part | Evidence-accuracy self-check = the "one specific named example per part" rule |
| **One specific named example per part** (proper-named event/date/person, not a category) | The same 4-move practice loop, rep shrunk from essay to 3-part response |
| Read the stimulus for the part it feeds (no HIPP sourcing) | — |

- **3 lessons** (~3.5h): S1 verb-bound answering (gated identify/describe/explain
  sort) → S2 full 3-part response with stimulus → S3 cold timed gate.
- **Gate:** cold timed A/B/C; ≥2 of 3 parts on ≥2 reps; self-score within 1 part of
  the grader.
- **Needs its own per-part binary scorer** (`SAQ_*` rubric IDs): per-part 1/0 keyed
  to verb-match + named-example-present + causal-reason, with a describe-vs-explain
  discriminator and "which part missed" for the rewrite loop. **Specify this to the
  dev team as a distinct scorer, not the essay scorer.**
- **Extensible:** built standalone so a future pass can add Gov SAQ-family (Concept
  Application, SCOTUS Comparison) and HuGeo without refactoring the History units.

---

## 6. The kept V1 backbone (summary — full detail in the audited map)

Unchanged from `ap-lesson-map.md` except for the Graft-2 additions (rescore loop on
every Revise beat; gated sorts on 0.1/1.1/4.1) and the History dedicated reading
rep before 3.1. Summarized here so the whole plan reads in one place.

| Unit | Builds | Subjects | Reps | Gate (real rubric row) |
|------|--------|----------|------|------------------------|
| **0 Spine** | claim→evidence→reasoning; thesis as a *refinement* (taught last) | Lang + Hist | 2 partial + 1 full | Thesis + Reasoning, cold |
| **1 Analyze (RA)** | read an author's choices via S-F-E (analysis, not feature-spotting) | Lang only | 1 + 2 | AP Lang RA Row A + Row B |
| **2 Argue/Knowledge** | line of reasoning + counterargument + evidence accuracy | Lang + Hist | 1 + 2 | Lang Argument / AP World LEQ |
| **3 Argue/Sources** | triage → source (HIPP relevance-frame) → contextualize → synthesize; **+ a dedicated document-reading rep first** (History) | Lang + Hist | 1 partial + 3 full | Lang Synthesis / AP World DBQ 7-pt |
| **4 Higher-Order** | Sophistication (Lang) / Complexity (History) as a concrete 2-route procedure; **timing enters here** | Lang + Hist | 0 + 2 timed | Row C / Complexity + lower rows, on ≥2 timed reps |

V1's data-driven detail is **kept as-is** (it's already mapped): the sourcing
relevance-frame stem + weak/strong pairs targeting the 65%-miss row; evidence as
three separately-scored sub-moves (describe ≥3 / use ≥4 / outside); the 3-step
contextualization; complexity as a 2-route procedure with worked examples and the
"however some disagree" anti-pattern; coping-model false starts; named anti-pattern
cards. These are the reason V1 scored 9/10 on transfer discipline — we keep them.

---

## 7. Time budget — auditable, single-exam fits; multi-exam stated

Adopting v2's per-rep minute accounting makes V1's (previously uncapped) timing
auditable. Per-rep minutes (honest set): partial 30–40; full untimed unsourced
50–60; full untimed sourced 70–80 (a 7-doc packet is ~15 min of reading alone);
timed FRQ 55–65; **rescore counted explicitly** (10–15 min on reasoning/sourcing
rows); plus a **gate-retry buffer** (this population fails the gated skill — budget
~1 retry on hard gates).

| Student path | Bridge | Backbone units | + SAQ | + buffer | **Total** | Inside? |
|--------------|--------|----------------|-------|----------|-----------|---------|
| **AP Lang** | 6.5 | U0 2.5 + U1 3 + U2 3.5 + U3 4.5 + U4 4 = 17.5 | — | ~2 | **~26h** | Yes |
| **APUSH (essays only)** | 6.5 | U0 2.5 + U2 3.5 + U3 6 + U4 4 = 16 | — | ~2 | **~24.5h** | Yes |
| **APUSH (full: + SAQ)** | 6.5 | 16 | 3.5 | ~2 | **~28h** | Yes (tight) |
| **Two exams: Lang + APUSH** | 6.5 once | Lang 17.5 + Hist 16 (Bridge+U0 shared) − U0 2.5 dup | 3.5 | ~3 | **~38h** | Multi-exam, stated |

**The honest line:** every **single-exam** path fits ~24–28h — *including full
APUSH with SAQ*, which the v2 design could not do inside budget. The hybrid even
**lowers the two-exam total** (~38h vs v2's ~46.5h) because we are not building six
overlays — the shared bridge + Unit 0 are done once and only the two subjects'
units differ. Multi-exam is stated openly: *"~24–28h to master your first AP FRQ;
roughly +12–14h per additional exam, since the foundation carries over."*

---

## 8. Verification gates before content is built (non-negotiable)

1. **Grader calibration on the hard rows** (Row B 3-vs-4, sourcing, complexity)
   against AP anchor papers — the hard launch gate in §4. The rescore multiplier
   and every gateway lock depend on it.
2. **Reserve the gate stimuli** — gate passages/packets held out of instruction
   (the prior B1L build leaked a source set between lessons), or "cold transfer" is
   fiction.
3. **Deferred families verify at their own design pass** — EBQ/Gov/Lit CEDs are not
   in the repo; do **not** author them until the current official scoring guidelines
   are stored and diffed. They are future passes, not v1.1 promises.

**Content-vs-writing boundary (state explicitly):** this is a *writing/structure*
course — it teaches how to deploy and source evidence, not which historical facts
are true. A History student must bring content knowledge from their AP content
course; the grader can flag obvious misattribution but cannot verify content
accuracy, so History gates score evidence-beyond/outside-evidence against a
**per-prompt acceptable-evidence key**, not generically.

---

## 9. Build sequence + decisions

**Build order (highest-leverage-first, lowest-risk):**

1. **Bridge (B1–B6)** — built FIRST. Closes fix #1; nothing downstream changes.
2. **Graft 2 into the existing map** — add the rescore loop to every Revise beat
   and the gated sorts to 0.1 / 1.1 / 4.1; re-run the Stage-02 audit. Closes fix #2.
3. **SAQ module** (standalone) + its per-part scorer spec. Closes fix #3 (bounded).
4. **History dedicated reading rep** before 3.1.
5. Then Stage 03 content generation on the (kept) Lang + History backbone.

**Decisions — resolved:**
- Scope = **hybrid**: keep V1 backbone + transfer discipline; graft bridge / rescore
  loop / SAQ; defer EBQ/Gov/Lit. ✅
- Multi-exam time **stated openly** (single-exam ~24–28h; ~+12–14h/exam). ✅
- Calibration **coached, not a lock**; cold gate alone gates. ✅
- Reuse + extend `lesson-engine.js` (add handlers for restate-vs-reason and
  verb-bound SAQ sorts; re-verify grader URL/key + register new `data-rubric` IDs). ✅

**Decision — resolved (applied in the splice, 2026-06-10):**
- **Mental-model consolidation — DONE.** Keep **S-F-E** and **Claim Hierarchy** as
  the scored moves they already are; fold **M1 + M5** into one "Function Question"
  lens (introduced in the Bridge); demote **M3 Force Field** → "the rhetorical
  situation" and **M6 Who Benefits?** → "HIPP-as-procedure" (taught operationally,
  not as named tracked models). Applied map-wide across the Bridge + Units 0–4 in
  `ap-lesson-map.md` (Legend + every lesson MM field + coverage checks + audit).

---

## 10. The one risk to manage

The evaluation named it precisely: **the hybrid is the right answer on paper, but
its value is entirely in the bridge and rescore loop actually being BUILT — not
deferred the way V1 already deferred its foundational phase.** If the team keeps
the audited backbone, declares victory, and re-shelves the two grafts that fix the
user's top two complaints, the hybrid recreates V1's exact failure under a new
banner. Mitigation is in the build order: **the bridge is item #1, not last.**

---

*Provenance: this hybrid is the output of an adversarial scope evaluation (two
advocates steelmanning V1 and the earlier v2 redesign + a neutral judge across 7
criteria; result: 48–48 tie → hybrid). It keeps V1's audit-passed Stage-02 lesson
map and transfer matrix, grafts the three inventions the judge identified as the
highest-leverage additive fixes (bridge-first, rescore loop with mandatory
reasoning-gating, standalone SAQ), and defers EBQ/Gov/Lit to their own verification
passes. Caveats: grader reliability on the subtlest rows is the single point of
failure and a hard launch gate; the deferred families' CEDs are unverified.*
