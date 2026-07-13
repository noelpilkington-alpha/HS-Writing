# HS Writing Course — Build Scope (what actually needs to be built)

Defines exactly what must be built for the proposed **High School Writing** course
(English I + English II MVP; ACT readiness + downstream AP FRQ prep).

## Ground truth (corrected 2026-06-11)

- **Nothing is in production.** The only high-school writing courses students
  actually have are the truncated AP-textbook courses (FRQ practice, no writing
  instruction).
- **The A1/A2/B1L/B2 lesson maps and the HTML files in `Generated_Content/` are
  PLANNING / PROTOTYPE artifacts, not built lessons.** They are design reference.
  The earlier "~80% already built" framing was wrong and has been corrected in the
  one-pager.
- **What IS de-risked:** the skill sequence is planned and its targets are verified
  against the STAAR English I/II + ACT rubrics and Timeback AP-failure data. We build
  from a validated plan, not a blank page — but the course itself is **net-new**.

## Locked build decisions (2026-06-11)

1. **All content is net-new.** Lesson maps = planning; prototypes = throwaway. Build
   from the (re-aimed) skill sequence + standards, not by refining old HTML.
2. **Curriculum team scope = content + assessment specs ONLY.** The dev team owns
   lesson delivery (the app/engine), the AI grader, and the tests. We specify WHAT to
   assess (rubric rows, feedback targets, eval exemplars); they build HOW.
3. **Reading integration is IN the MVP** (passage-based writing-about-reading, per
   Graham *Writing to Read* + because STAAR/ACT are reading-dependent). **Video and
   document-markup are DEFERRED** to v2.
4. **Standards:** dual **STAAR + CCSS** crosswalk per lesson.

---

## The build, by ownership

### CURRICULUM TEAM builds (our deliverables)

| # | Deliverable | What it is | Net-new? |
|---|-------------|------------|----------|
| **C1** | **Locked English I + II lesson map** | Consolidate the planned sequence into one G9–G10 map, **re-aimed** from rhetorical-analysis to **STAAR content-response** (controlling idea about a passage's content + textual evidence), with **passage-based reading integrated** and an **expository response-to-text** thread added. One new move per lesson; scaffold fade; gates per stage. | Re-aim of a plan → **build** |
| **C2** | **Dual standards crosswalk** | Per-lesson mapping to **TEKS/STAAR English I & II** AND **CCSS 9–10**. CCSS partially drafted; **STAAR is net-new** (Texas is not a CCSS state — codes don't transfer). | STAAR = **net-new** |
| **C3** | **Instructional content (~40 lessons)** | For each lesson: the teaching beat, a coping-model worked example (false start → correction), gated discrimination items, checklists, revision protocols, and the student-facing prompt. The bulk of the work. | **Net-new** |
| **C4** | **Passage / stimulus bank** | Grade-9/10 source passages + **paired sets** (STAAR uses paired passages at the top band), each with an anchored writing task. Must be reading-level-appropriate for a typical on-grade G9 (NOT the AP-level, rhetorical-analysis-oriented passages in the current bank). Plus **reserved** passages held out for gates. | **Net-new** |
| **C5** | **Assessment specifications** (handoff to dev) | The rubric definitions + feedback targets + scored exemplars (anchor papers) the grader and tests are built from: **STAAR ECR 2-trait** (Org & Development 0–3, Conventions 0–2), **sentence-combining SCR** (0–1), **reading SCR** (0–2, claim + cited evidence), **ACT 4-domain** (2–12). This is a spec, not the grader itself. | **Net-new** |

### DEV TEAM builds (our dependencies — we spec, they build)

| # | Deliverable | Our input | Risk |
|---|-------------|-----------|------|
| **D1** | **Lesson delivery in the production app** | Lessons run on the existing paragraph- + essay-writing architectures; reading-integration may need a passage/stimulus surface. | Reuse for composition is low-risk; the **passage surface + reading-integration UI is the open engineering question**. |
| **D2** | **AI graders** (prompts + eval sets per task) | C5 specs + anchor papers. The ensemble-grader *architecture* exists; per-activity grading prompts + eval sets do not. **Hard launch gate: calibrate against anchor papers** before any gated lesson ships. | The grader's reliability on the subtle rows is the single point of failure. |
| **D3** | **STAAR-aligned writing tests / gates** | C5 specs + reserved stimuli. English I & II EOC-style writing tests + an ACT-style gate — the "what test does it pass?" answer. | **Cross-team (Tiago/Andy):** whether tests are new or adapted, and where they live (in-app vs Alpha test) — unresolved. |

### DEFERRED to v2 (not in MVP)

- Video instruction; required outside-reading + its assessment; document markup /
  print-and-annotate. (Flagged in the product jam as the lever between "expanded
  textbook" and a genuinely good course — but out of MVP scope.)
- AP-specific overlays (Lang/History DBQ sourcing/complexity, SAQ module, EBQ/Gov/
  Lit). Downstream, post-MVP.

---

## The activities, by essay type (what C3/C4/C5 must produce per task)

Every lesson is **one piece of writing through the live engine cycle** — Setup →
Outline → Draft → Revise → Polish → Submit — on the **paragraph-writing**
architecture (early/faster reps) or the **essay-writing** architecture (the core).
The template is fixed per essay type; only the prompt, the stimulus, and the
**scaffold level** (heavy → faded) change across reps. Direct instruction is
delivered through the engine's own surfaces: the **AI Tutor** (tutorial + in-stage
narration, skippable once mastered), the **structured Outline form**, **inline
Tips**, and the **AI-validated Revise/Polish checklists**. The ★ marks each essay
type's **frontier stage** (heaviest instruction — the year's hard new move).

Notation: each row is what the student DOES at that stage; the build columns name
the C3 content (instruction + items), C4 stimulus, and C5 spec each stage requires.

### Essay type 1 — Expository response-to-text *(STAAR English I, informational)*
*Read a passage; form and defend a controlling idea about its content. ★ Draft.*

| Stage | What the student does | Build needs |
|-------|----------------------|-------------|
| **Setup** | Read the source passage; comprehension pre-read ("what is this about? what's the author's position?"); confirm task/audience | C4: 1 grade-9 passage + comprehension key · C3: pre-read Tip |
| **Outline** | Structured form: **controlling-idea box** (about the passage's content, not the author's craft) → intro sequence → body cards (each: point + a **text-evidence slot** + an "explain how it supports the idea" sub-prompt) → conclusion | C3: weak/strong controlling-idea discrimination pair (gated); Outline field prompts · C5: which fields map to Org & Development |
| **★ Draft** | Compose body paragraphs: point → cited text evidence → **explanation tying it to the controlling idea** (not dropped quotes) | C3: Teach + coping model (false start = drops the quote → correction adds the "because/this shows" link); inline Tip |
| **Revise** | Altitude-ordered checklist — **(meaning, gating)** controlling idea clear & consistent? every paragraph explains its evidence? unified? → **(surface)** transitions, sentence flow | C3: checklist items · C5: meaning items = STAAR Trait-1 rows |
| **Polish** | Checklist: conventions in-context (sentence boundaries — run-ons/fragments — punctuation, spelling) so errors don't impede clarity | C3: Polish checklist · C5: STAAR Trait-2 (Conventions 0–2) |
| **Submit** | AI-graded on the STAAR ECR rubric; **rewrite the single weakest trait, re-score** | C5: ECR 2-trait spec + anchor papers |

### Essay type 2 — Argumentative response-to-text *(STAAR English I/II, argumentative)*
*Take a defensible position on the passage's issue. ★ Draft (carries from type 1) → counterargument is the new move.*

| Stage | What the student does | Build needs |
|-------|----------------------|-------------|
| **Setup** | Read passage; identify the issue and the positions available | C4: 1 issue-bearing passage (+ optional opposing snippet) |
| **Outline** | Form: **defensible-thesis box** (debatable/specific/supportable) → claim hierarchy (sub-claims ordered to build, not list) → **counterargument card** (acknowledge / concede / respond) → conclusion | C3: weak/strong thesis pair + "builds vs lists" discrimination (gated); counterargument frame |
| **★ Draft** | Claim → evidence → reasoning per body; **place the counterargument as a move**; evidence accuracy (name it precisely) | C3: Teach + coping model (false start = strawman / unlinked reason → correction) |
| **Revise** | **(meaning)** position defensible & consistent? reasoning links evidence to claim? counter addressed fairly? → **(surface)** transitions | C3: checklist · C5: STAAR Trait-1 rows |
| **Polish** | Conventions in-context | C3: Polish checklist · C5: Trait-2 |
| **Submit** | AI-graded (STAAR ECR argumentative); rewrite weakest trait | C5: ECR spec + argumentative anchor papers |

### Essay type 3 — Synthesis essay *(STAAR top-band paired passages; AP synthesis prep)*
*Weave a position across paired/multiple passages — organized by argument, not source-by-source. ★ Outline.*

| Stage | What the student does | Build needs |
|-------|----------------------|-------------|
| **Setup** | Read **paired/multiple** passages; note each source's stance/perspective | C4: **paired/multi-source set** (grade-appropriate) + stance key |
| **★ Outline** | Form: **synthesis matrix** (sources × themes) as a fielded grid → thesis that answers across sources → body cards organized **by theme/claim**, each pulling from ≥2 sources | C3: serial-vs-synthesis discrimination (gated); matrix field prompts · C4: pairing designed for synthesis |
| **Draft** | Weave sources into the line of reasoning (writer's idea + source → one sentence, no dropped quotes); attribution/signal phrases | C3: Teach + coping model (false start = source-by-source summary → re-weave by theme) |
| **Revise** | **(meaning)** synthesis not serial summary? evidence from **both/all** texts? position consistent? → **(surface)** attribution variety, transitions | C3: checklist incl. "synthesis or serial summary?" check · C5: rows incl. both-texts evidence |
| **Polish** | Conventions in-context | C3 · C5: Trait-2 |
| **Submit** | AI-graded; rewrite weakest part | C5: synthesis spec + anchor papers |

### Essay type 4 — Multi-perspective (ACT-style) essay *(ACT Writing, G11+ readiness)*
*Analyze 3 given perspectives; stake and qualify your own. Constructed support (no source passages). ★ Outline → analysis/qualification is the new move. Timed.*

| Stage | What the student does | Build needs |
|-------|----------------------|-------------|
| **Setup** | Read the issue + **3 given perspectives**; decompose each (core claim / assumption / value / blind spot) | C4: ACT-style issue + 3-perspective prompts |
| **★ Outline** | Form: **perspective-map** (each perspective's strength/limit) → own position **related to** the given perspectives → where to **qualify/complicate** | C3: "engage vs restate" + "real qualification vs empty gesture" discrimination (gated) |
| **Draft** | Develop an **integrated line of reasoning** with constructed support (examples, reasoning chains); convey significance | C3: Teach + coping model (false start = "some disagree" with no payoff → real qualification) |
| **Revise** | **(meaning)** engages multiple perspectives? position nuanced not binary? significance conveyed? → **(surface)** transitions, precise diction | C3: checklist mapped to ACT domains · C5: ACT 4-domain |
| **Polish** | Conventions (errors don't impede); timing recovery | C3 · C5: ACT Language Use |
| **Submit** | AI-graded on ACT 4-domain (2–12), timed; rewrite weakest domain | C5: ACT 4-domain spec + anchor papers |

### Short constructed responses *(STAAR SCR — not full essays; paragraph architecture)*
*Bounded items run on the paragraph/short-response surface, not the 6-stage cycle.*

| Item | What the student does | Build needs |
|------|----------------------|-------------|
| **Sentence-combining (writing SCR, 0–1)** | Combine 2–3 sentences into one clear, effective complete sentence (coordination/subordination/semicolon) | C3: gated weak/strong combine items + Teach · C5: SCR 0–1 spec |
| **Reading SCR (0–2)** | Answer an inference/analysis question accurately **+ cite/paraphrase text evidence** | C4: short passage + question · C3: "claim + evidence present?" check · C5: reading SCR 0–2 spec |

### What every lesson reuses (the fixed wrapper, built once)
- The **AI-Tutor DI sequence** (Teach → Model-with-coping → Guided → Independent →
  a 15–30s discrimination beat), concentrated on the ★ frontier stage and light on
  the already-fluent stages.
- The **rescore-the-weakest-part loop** at Submit (one part rewritten and re-scored
  → 2–3 graded reps per essay at near-zero clock cost).
- **Scaffold fade**: Outline fields pre-filled + worked example on rep 1 → blank by
  the final rep ("Skip tutorial" is the fade control for the Teach beat).
- **Meaning-before-surface gating** in the Revise checklist (a broken argument
  can't be "polished"; mirrors STAAR's Trait-1=0 → Trait-2=0 rule).

> **Engine caveat:** the stage surfaces above (structured Outline form, validated
> checklists, AI Tutor) are taken from `HS_Writing_Cycle_Based_Redesign.md`, which
> was reconciled against AlphaWrite screen recordings. Confirm the current
> production engine still matches before C3 authoring — especially whether it
> supports a **paired-passage stimulus panel** (needed for essay type 3 and the
> reading SCR). This is dependency **D1**.

## Build sequence (curriculum team)

1. **C1 lesson map** (re-aimed to STAAR + reading integration) — lock first; nothing
   downstream is safe until the skill sequence and gates are fixed.
2. **C2 dual crosswalk** — in parallel with C1; it validates coverage of both
   standards and surfaces any STAAR skill the sequence misses.
3. **C5 assessment specs** — before content, so lessons are written to the rubric
   rows the grader will score (write-to-the-gate discipline).
4. **C4 passage bank** — feeds C3; gate stimuli reserved from the start.
5. **C3 lesson content** — the bulk; built English I first, then English II.
6. Handoff **C5 + reserved stimuli** to dev for **D2 grader** and **D3 tests**;
   coordinate **D1 delivery** (especially the reading-integration surface).

## Open dependencies to resolve (not curriculum-team decisions)

- **Gate location:** in-app vs Alpha test (D3).
- **Test build path:** adapt existing tests vs create new (Tiago/Andy).
- **Reading-integration surface:** does the production engine support a passage/
  paired-passage stimulus panel for writing-about-reading? (D1 — the main
  engineering unknown.)

## Honest sizing note

This is a **net-new ~40-lesson course** with a net-new passage bank, a net-new STAAR
crosswalk, and net-new assessment specs — de-risked by a validated design, scoped to
content + specs (dev owns delivery/grader/tests), with reading integrated and
video/markup deferred. It is *not* a re-alignment of existing built work, because no
built work exists.
