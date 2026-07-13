# C4 — Passage / Stimulus Bank Spec (English I + II MVP)

The grade-9/10 source material the lessons and gates write from. Derived from the
C1 lesson map's stimulus requirements and the C2 standards crosswalk. This spec
defines **what passages to acquire/commission, to what spec, and which lesson each
serves** — it is the build order and acceptance criteria for the bank, not the
passages themselves (those are acquired/written against it).

**Status:** v1 for review. Feeds C3 (each lesson's stimulus) and the dev team's
gate/test stimuli (D3). Reading-level and reserved-stimulus discipline are the two
load-bearing constraints.

## Why a new bank (not the existing one)

The existing passage bank (`Passage_Bank.md`, ~177 candidates) is **AP-level and
selected for rhetorical-analysis** (historical speeches chosen for "brevity as a
choice," "understatement," etc. — Chief Joseph, Patrick Henry, Douglass). The MVP
needs the opposite: **grade-9/10 reading-level passages selected for their CONTENT/
ideas** (so a student can form a controlling idea about what the text *says*, per
the STAAR 5.B/10.B re-aim), not the author's craft. A handful of the most
accessible existing items may be reusable for EI single-passage reps; the synthesis
sets and the reading-level floor are net-new.

## Load-bearing constraints (acceptance criteria for every passage)

1. **Reading level: grade 9–10, on-grade.** Target Lexile ~1010–1150 (the CCSS
   9–10 band) for EI, trending to the upper half for EII. NOT AP/college-level. A
   typical on-grade G9 must be able to comprehend it without the reading load
   consuming the cognitive budget needed for writing (the diagnosed failure mode).
   **Each passage ships with its measured Lexile + a 1-line readability note.**
2. **Content-bearing, low prior-knowledge.** The passage must contain a real idea a
   student can take a position on or explain, **without requiring outside content
   knowledge** (this is a writing course, not a content course). Informational
   topics should be self-contained (science/society/history-of-an-idea explained
   *within* the passage).
3. **Mode-appropriate.** Informational/analytical-response passages (the primary
   STAAR mode) must support a controlling idea about their content. Argumentative
   passages must present a debatable issue. Synthesis sets must be designed so the
   sources genuinely combine (see §Synthesis design).
4. **Copyright-clear.** Public-domain, openly-licensed, or commissioned/original.
   Flag licensing per item. (The dev team can't ship un-cleared text.)
5. **Reserved-stimulus discipline.** Gate passages (1.5, 4.6, 5.6, 8.3, 8.4, 8.5)
   are **held out of all instruction** — never shown in a teaching lesson. A leak
   makes "cold transfer" fiction (the prior B1L build leaked a source set). Reserved
   items are tagged RESERVED and stored separately.
6. **Length to spec.** Single passages ~500–800 words (EI), paired/multi-source
   sets sized to the STAAR ~6,000-word total reading-load ceiling across a form.

## Bank inventory — by lesson (from C1)

Legend: **type** P=single passage · PAIR=paired set · MULTI=3+ source set ·
PERSP=ACT-style issue + 3 perspectives (no passage) · SCRp=short SCR passage.
**R**=reserved (held out for a gate).

### English I

| Lesson | Stimulus needed | Type | Spec notes |
|--------|-----------------|------|------------|
| 1.1 Reason not restate | short content passage + a claim to attach evidence to | P (short) | accessible; just enough content for one point + evidence |
| 1.2 Read for the idea | 1 grade-9 passage + comprehension key | P | clear single controlling idea; + "what's it saying / position" key |
| 1.3 Cite + explain | reuse 1.2 passage (or sibling) | P | evidence-rich enough for 2–3 citable points |
| 1.4 Controlling idea | 1 passage (fresh) | P | content supports a defensible controlling idea |
| 1.5 **Bridge gate** | fresh reserved passage | **P · R** | informational/analytical; short-ECR length |
| 2.1 Structure the response | 1 passage | P | supports a 3-part body structure |
| 2.2 Explain to standard | 1 passage | P | rich evidence; designed so "drop the quote" is tempting (for the coping model) |
| 2.3 Revise meaning | reuse 2.1/2.2 draft | — | no new passage (works on prior draft) |
| 2.4 **Full expository ECR, cold** | fresh reserved passage | **P · R** | full informational ECR |
| 3.1 Defensible position | 1 issue-bearing passage | P | presents a debatable issue (argumentative) |
| 3.2 Line of reasoning | reuse 3.1 (or sibling issue) | P | issue with multiple supportable sub-claims |
| 3.3 Counterargument | 1 issue passage (+ optional opposing snippet) | P (+snippet) | a fair opposing view available |
| 3.4 Evidence accuracy | 1 issue passage | P | precise facts that can be mis-cited (for the precise-vs-vague pair) |
| 3.5 **Full argumentative ECR, cold** | fresh reserved issue passage | **P · R** | full argumentative ECR |
| 4.1 Sentence boundaries | short item set (run-ons/fragments) | SCRp | engineered error items, not a passage |
| 4.2 Sentence-combining SCR | combine-item set | SCRp | 2–3-sentence inputs to combine |
| 4.3 Reading SCR | short passage + analysis question | SCRp | inference answerable + citable |
| 4.4 Revising/editing | a draft-with-flaws + item set | SCRp | student-style draft to strengthen |
| 4.5 Pre-gate ECR | 1 passage (info or arg) | P | full ECR practice |
| 4.6 **ENGLISH I GATE** | reserved passage set: 1 ECR passage + 1 reading-SCR passage + writing-SCR items | **P · SCRp · R** | the gate stimulus set |

### English II

| Lesson | Stimulus needed | Type | Spec notes |
|--------|-----------------|------|------------|
| 5.1 Source stance | paired/multi set + stance key | **PAIR/MULTI** | 2–3 sources, distinct stances on one topic + credibility/bias angle (C2 Gap 3) |
| 5.2 Serial vs synthesis | reuse 5.1 set | MULTI | sources designed to cross on shared themes (for the matrix) |
| 5.3 Thesis across sources | reuse 5.1/5.2 set | MULTI | a position is possible *across* the set |
| 5.4 Weave sources | 1 fresh multi set | MULTI | ≥3 sources, weave-able (not redundant) |
| 5.5 Revise synthesis | reuse 5.4 draft | — | no new set |
| 5.6 **Full synthesis essay, cold** | fresh reserved paired/multi set | **MULTI · R** | STAAR EII top-band synthesis |
| 6.1 Nuance ladder | 1 issue passage | P | issue affording qualification (scope/conditions) |
| 6.2 Engage opposing views | 1 issue passage (+ opposing views) | P (+views) | multiple real positions present |
| 6.3 Concede + rebut | reuse 6.2 (or sibling) | P | a genuinely conceivable opposing point |
| 6.4 Full nuanced argument, cold | fresh reserved issue passage | **P · R** | nuanced argumentative |
| 7.1 Decompose 3 perspectives | ACT-style issue + 3 perspectives | **PERSP** | no source passage; 3 labeled stances (ACT format) |
| 7.2 Stake position | reuse 7.1 prompt | PERSP | — |
| 7.3 Qualify + reasoning | 1 fresh PERSP prompt | PERSP | issue affording qualification |
| 7.4 Timed ACT #1 | 1 PERSP prompt | PERSP | full ACT-style |
| 7.5 Timed ACT #2 | fresh reserved PERSP prompt | **PERSP · R** | cold ACT-style |
| 8.1 Timing strategy | 1 PERSP or passage | P/PERSP | any prior type |
| 8.2 Self-diagnosis | reuse | — | works on a prior rep |
| 8.3 Pre-gate synthesis (timed) | fresh reserved multi set | **MULTI · R** | cold synthesis |
| 8.4 Pre-gate ACT (timed) | fresh reserved PERSP prompt | **PERSP · R** | cold ACT-style |
| 8.5 **ENGLISH II GATE** | reserved: 1 synthesis multi-set + 1 ACT PERSP prompt + conventions items | **MULTI · PERSP · R** | the gate stimulus set |

## Counts (acquire/commission targets)

| Item type | Instructional | Reserved (gates) | Total |
|-----------|--------------|------------------|-------|
| EI single passages (P) | ~10 (some reused across reps) | ~4 (1.5, 2.4, 3.5, 4.6) | ~14 |
| EI SCR passages/item sets (SCRp) | ~4 | (in 4.6 set) | ~4 |
| EII paired/multi synthesis sets (PAIR/MULTI) | ~3 | ~3 (5.6, 8.3, 8.5) | ~6 |
| EII issue passages (P) | ~3 | ~1 (6.4) | ~4 |
| ACT-style PERSP prompts | ~3 | ~3 (7.5, 8.4, 8.5) | ~6 |

Net ~**34 stimulus units** (≈19 instructional + ≈11 reserved + reuse). A passage
reused across a lesson cluster (e.g. 5.1→5.2→5.3) counts once.

## Synthesis-set design (the part most likely to fail if under-specified)

A synthesis set is not "3 passages on a topic" — it must be **engineered to
combine**:
- **One topic, distinct angles.** Each source takes a different stance/lens (e.g.
  for/against/qualified, or data/anecdote/policy) so combining them is meaningful,
  not redundant.
- **Shared themes across sources** (so a sources × themes matrix has real cells).
- **A built-in credibility/bias contrast** for at least one set (covers C2 Gap 3,
  TEKS 11(G)(i)) — e.g. one source clearly opinion/advocacy, one neutral/informational.
- **Cross-able, not parallel.** Sources must agree *and* diverge on the themes, so
  a student can build a position across them (not just summarize each).
- **Reading-level held** even with multiple sources (total set within the load ceiling).

## ACT-style PERSP prompt design

- One **contemporary, accessible issue** (no specialized knowledge).
- **Three distinct perspectives**, each a short labeled paragraph with a clear
  stance (one pro, one con, one qualified/reframing — mirroring the ACT format).
- Issue must **afford qualification/complication** (so the "qualify" move at 7.3 is
  real, not forced).
- Constructed-support friendly: a student can develop it from general knowledge/
  reasoning (no source passages — this is the ACT, not STAAR synthesis).

## SCR item design

- **Sentence-combining (writing SCR):** sets of 2–3 short sentences that combine
  naturally via coordination/subordination/semicolon; each item has a clear "best
  combine" + weak-combine distractors (for the gated discrimination).
- **Reading SCR:** a short passage + an inference/analysis question whose answer is
  both correct-able and **text-evidence-citable** (the 0–2 rubric needs both).
- **Boundary items (4.1):** engineered run-ons and fragments in context, with fixes.

## Open dependencies

- **Acquisition path (decision needed):** public-domain/openly-licensed selection
  vs **commissioned/AI-generated original passages** (cleaner for reading-level
  control + copyright, but must be quality-checked). Recommend **commissioned/
  original for synthesis sets and ACT prompts** (precise control of stance/level/
  combinability) and **curated open-license for single informational passages**
  where good ones exist. Confirm.
- **Reading-level verification:** who runs the Lexile/readability check, and the
  exact target band per grade (EI vs EII).
- **Paired-passage surface (D1):** the synthesis sets assume the engine can present
  multiple sources at Setup — the same engineering unknown flagged in Build_Scope
  and C1. Confirm before committing synthesis-set production.
- **Gate-stimulus ownership (D3):** reserved gate sets may need to live with the
  dev team's test system, not the lesson content — coordinate.

## Handoff

- **C3** pulls each lesson's stimulus from this bank; author lessons only against
  passages that meet the acceptance criteria.
- **C5** (assessment specs): the **reserved gate passages** must be paired with
  anchor papers at the right score points — coordinate C4 reserved items with C5
  exemplars.
- **D3** (dev/tests): reserved gate stimuli + their rubrics are the test-build input.
