# AP FRQ Mastery — SAQ Module Lesson Map (Graft 3, standalone, NON-spine)

The short-answer (SAQ) module: a **separate, non-spine** module in the hybrid plan
(Graft 3). It is shipped in v1 because SAQ is ~20% of the APUSH score and an APUSH
student who skips it is not exam-ready — but it is **NOT folded onto the
argument-essay spine**, because the shared transfer matrix proves the spine barely
reaches it (History thesis 2%; defensible-thesis and evidence-integration do not
transfer; S-F-E does not transfer). It inverts the spine: **no thesis, no line of
reasoning, one bounded point per part.**

A History/APUSH student takes the kept argument backbone (Bridge + Units 0/2/3/4)
**and** this module. The module is built standalone so a future pass can extend it
to the Gov SAQ-family and HuGeo without refactoring the History units.

- **Format:** same field set as the spliced `ap-essay-course/stages/02-lesson-map/
  output/ap-lesson-map.md`, so this block can be appended as a separate module
  section after Unit 4.
- **Hours:** ~3.5h. **Lessons:** 3 (S1, S2, S3).
- **Calibration source:** verified against the AMSCO AP World / APUSH SAQ
  instruction (the A/B/C bounded-response format, the identify/describe/explain
  verb ladder, 1-point-per-part). Gov SAQ-family + HuGeo are **provisional** (see
  Verification, below).

---

## What this module reuses from the core vs what is genuinely new

| Reuses from the Bridge/Core (taught, not re-taught) | Genuinely new (the core never teaches) |
|------------------------------------------------------|-----------------------------------------|
| The **reasoning because-clause** (Bridge B1 / Unit 0 Reasoning row) — the SAQ "explain" part IS the "reach Effect" move shrunk to one sentence | **Verb-bound answering**: identify < describe < explain — the verb itself is the scored object; the signature miss is answering the wrong verb |
| The **evidence-accuracy self-check** (Unit 2: "name it precisely — who/what/when") — becomes the SAQ "one specific named example per part" rule | The **bounded A/B/C format**: 1 pt/part all-or-nothing, **no thesis, no line of reasoning**, 1–2 complete sentences (not bullets), ~12–14 min/question |
| The **4-move practice loop** (judge[gated] → coping-model false start → write → AI-score → rewrite-weakest) — reused unchanged, rep shrunk from essay to a 3-part response | **One specific named example per part** (proper event/date/figure, not a category): "the Columbian Exchange," not "trade" |
| The **calibration ladder** (binary self-score vs grader) — the SAQ 1/0-per-part is the cleanest binary anchor | **Read the stimulus for the part it feeds** (Q1 secondary / Q2 primary) WITHOUT HIPP sourcing — a light, contained move |

---

## SAQ Module (standalone, ~3.5h, 3 lessons)

*NON-spine module. Inverts the argument spine: NO thesis, NO line of reasoning,
one bounded point per part. Builds: answer the exact task verb (identify <
describe < explain) in 1–2 complete sentences, each backed by one specific named
example; read a source stimulus for the part it feeds without sourcing it.
Frontier = the bounded answer itself. Timing enters only at S3 (mirrors the core
deferring timing to its higher-order unit). Reuses the 4-move loop and the
reasoning because-clause; needs its OWN per-part binary scorer (NOT the
line-of-reasoning essay scorer). Gate: cold timed A/B/C, >=2 of 3 parts on >=2
reps, self-score within 1 part of the grader.*

### Lesson S1 - The bounded answer: verb discrimination + the one-sentence rep

| Field | Spec |
|-------|------|
| Rep type | Partial: 6-8 single-PART micro-reps (one correct identify, one describe, one explain to given prompts), then 1 full A/B/C rep on a NO-source (Q3/Q4-type) prompt |
| New move | Verb-bound answering on the tiered ladder (identify = name it < describe = name + a characteristic, NO causation < explain = a causal because-clause), and the one-point-per-part / no-thesis format. Framed AGAINST the core: "You spent the Core building a line of reasoning. SAQ forbids it. Each part is one bounded sentence that does exactly what its verb says." |
| Scaffold | **Heavy** - **Rung-0 gated discrimination FIRST:** sort 8-10 responses as describe-vs-explain and earns-vs-misses, using the official 0-point patterns ("answered the wrong verb", "stated a generality not a named example", "wrote a bullet/outline not a complete sentence") as negative exemplars; **production unlocks only after a correct classification** (hard time cap on the sort). Then a verb-ladder reference card + 1-2 sentence-frame stems per verb |
| Frontier | The bounded answer (one part, one verb, one sentence) |
| MM | **S-F-E** (the "explain" part = "reach Effect" in one sentence); no Claim Hierarchy (SAQ has no line of reasoning - this absence is taught explicitly) |
| Cross-cutting strands | Verb-bound answering (introduced); Self-assessment (binary 1/0 per part); Discrimination (gated, describe-vs-explain + earns-vs-misses) |
| Gate | SAQ Part scoring: **1 point per part, all-or-nothing** - task accomplished as the verb demands. Maps to the official "earn one point for a successful response to each task; 0 for any task not accomplished" |
| Generate | 8-10 discrimination items built verbatim from the official failing patterns (wrong-verb, generality-not-named-example, bullet-not-sentence); 1 coping-model worked example with a false start (answers "describe" to an "explain" prompt -> catches it -> corrects to a because-clause); a verb-ladder reference card (identify = name it; describe = name + characteristic; explain = name + causal "because"); 6-8 single-part micro-prompts + 1 no-source A/B/C prompt. **Engine:** discrimination items need the new `Verdict: Earns|Misses` / `Classification: Describe|Explain` sort handlers (see Engineering Handoff); wire reps to `data-rubric="SAQ_S1_parts"` |

### Lesson S2 - The specific named example + the causal "explain why" (full reps with a stimulus)

| Field | Spec |
|-------|------|
| Rep type | Full: 3 complete A/B/C SAQs - one secondary-source (Q1-type), one primary-source (Q2-type), one no-source (Q3/Q4-type). Plus the rewrite-the-weakest-PART rescore loop |
| New move | One specific named example per part (proper event/date/figure, not a category) AND the causal "explain" part rendered as the core's reasoning because-clause shrunk to one sentence. Stimulus-reading: use a secondary/primary source to anchor the source-fed part (Q1/Q2) WITHOUT doing HIPP sourcing |
| Scaffold | **Medium** - Rung-0 discrimination on "named specific example vs correct-but-generic" and "explain = causal because-clause vs restating the describe-answer" (built from the named anti-pattern); reference card faded to a checklist; stimulus-reading scaffolded with a one-line "what does this source claim?" prompt, then faded |
| Frontier | The bounded answer + reading the stimulus for the part it feeds |
| MM | **S-F-E** (the explain because-clause); still no Claim Hierarchy |
| Cross-cutting strands | Verb-bound answering (to fluency); Specific-named-example (introduced); Self-assessment (binary per part); Stimulus-reading (introduced, no HIPP); Discrimination (named-vs-generic, explain-vs-restate); the **rescore-the-weakest-PART loop** (grader names the single part that missed; student rewrites ONLY that part and rescores - turns 1 SAQ into 4-6 graded part-reps at near-zero clock cost) |
| Gate | SAQ Part scoring (1/0 per part): "explain" parts require a causal/relevant reason (the core Reasoning row); "describe/identify" parts require a specific named example; source-fed parts must use the stimulus |
| Generate | 3 full A/B/C SAQ prompts (1 secondary-source stimulus ~150-250 wds, 1 primary-source, 1 no-source) on reserved-from-instruction topics; each part tagged with its reasoning process (comparison / causation / continuity-and-change); a discrimination set on named-vs-generic and explain-vs-restate; 1 coping-model with a false start (gives "trade increased" -> catches the missing named example -> corrects to "the Columbian Exchange"). **Engine:** wire each SAQ to `data-rubric="SAQ_S2_full"`; enable the rewrite-weakest-part rescore path (grader returns which part missed) |

### Lesson S3 - Cold timed gate (+ Gov SAQ-family branch)

| Field | Spec |
|-------|------|
| Rep type | 2-3 COLD, single-attempt, timed full A/B/C reps on reserved held-out stimuli (History: 1 secondary-source + 1 no-source; Gov branch: 1 Concept Application + 1 SCOTUS Comparison). Self-score binary per part BEFORE the grader, then compare (calibration-accuracy signal) |
| New move | Two thin additions, both reusing everything prior: (1) **TIMING enters** - the only timed reps in the module, ~12-14 min per 3-part question, deferred to the end exactly as the core defers timing; (2) **GOV FEEDSTOCK BRANCH** (Gov students only) - Concept Application (apply a named course concept to a scenario) + SCOTUS Comparison (name the shared clause/principle, explain the connection to a non-required case), same verb-bound 1-point-per-part discipline. **Gov is PROVISIONAL - see Verification.** |
| Scaffold | **Light -> None** for the gate reps. A brief pacing cue card (~4-5 min/part, write the bounded sentence, move on - do not over-write). For Gov, one Rung-0 discrimination set on the Gov signature miss ("named the concept but did not apply it to the scenario" / "described the cases but did not name the shared principle"), then cold production |
| Frontier | Cold bounded answer under the clock |
| MM | S-F-E (automatic in the explain part); no Claim Hierarchy |
| Cross-cutting strands | Verb-bound answering (cold, timed); Self-assessment at top level (binary self-score vs grader = the calibration check, NOT a progression lock per the hybrid decision); Timing/process (pacing); Discrimination (Gov-specific, apply-vs-name / compare-vs-summarize) |
| Gate | **SAQ Module gate:** SAQ Part scoring (1/0 per part) under the clock on a cold reserved stimulus. PASS = **>=2 of 3 parts earned on each of >=2 cold timed reps**, AND self-score within 1 part of the grader (calibration check). Gov-track students gate on a Concept Application + a SCOTUS Comparison rep against those families' part criteria. **Single-attempt cold - no rescore on gate reps** (the rewrite-weakest-part loop is S1/S2 only), so transfer not local patching unlocks completion |
| Generate | 2-3 reserved cold SAQ stimuli + prompts held out of S1/S2 (History) and 2 Gov-family prompts (1 Concept Application scenario, 1 SCOTUS Comparison pairing a non-required case to a clause); a pacing cue card; 1 Gov-specific discrimination set (apply-vs-name, compare-vs-summarize). **Engine:** wire gate reps to `data-rubric="SAQ_gate"` `data-gateway="true"` `data-scoring-model="saq_binary"` with gateway-lock-until-pass; add a self-score input compared to the grader's part scores |

### SAQ Module coverage check

- **Inversion taught explicitly:** S1 frames the whole archetype against the spine
  ("SAQ forbids the line of reasoning") so the student does not import essay habits.
  No thesis, no Claim Hierarchy anywhere in the module - by design.
- **Verb ladder is the spine of the module:** identify < describe < explain, with
  the wrong-verb answer as the #1 negative exemplar (gated sort, S1).
- **Reuse honored:** the explain because-clause = the Bridge B1 / Unit 0 reasoning
  move; the named-example rule = the Unit 2 evidence-accuracy check; the 4-move loop
  and rescore-weakest-PART loop are the same engine as the essay units.
- **Timing deferred to S3** (mirrors the core's timing-in-the-last-unit rule).
- **Gated discrimination on every new move:** S1 describe-vs-explain (gated, locks
  production); S2 named-vs-generic + explain-vs-restate; S3 Gov apply-vs-name.
- **Scaffold fades:** S1 Heavy -> S2 Medium -> S3 Light/None.
- **One new move per lesson:** S1 verb-bound answering; S2 named-example + causal
  explain + stimulus-reading (note: these are facets of one "complete the part
  correctly" move on the SAME bounded format, not three independent essay moves -
  the format is fixed from S1, so this is not a 2.2-style stack); S3 timing + the
  Gov branch.
- **Calibration is coached, not a lock** (hybrid decision): the self-score-vs-grader
  check is surfaced and is part of the gate's PASS condition as a *calibration*
  signal, but advancement is by the cold part-score, consistent with the rest of
  the course.

---

## Engineering handoff (the two confirmed engine gaps — these are real, verified in `lesson-engine.js`)

The SAQ module CANNOT run on the current engine unchanged. Two concrete extensions
are required (both were flagged in the spec; confirmed here by reading the engine):

1. **New sort handlers in `initSortItems()`** (`Generated_Content/Lessons_HTML/
   lesson-engine.js`, ~line 116). The function currently auto-detects only
   `Classification: Expository|Argumentative` and `Classification: Analysis|Summary`.
   The SAQ gated sorts use `Verdict: Earns|Misses` and `Classification:
   Describe|Explain` (and, for Gov, `apply-vs-name` / `compare-vs-summarize`). **Add
   these category pairs** to the detection + button-building logic (the existing
   `classify-wrap` / `classify-correct` / `classify-wrong` + `addScore(SCORE_CLASSIFY)`
   gating machinery is reused unchanged; only the category list needs extending). Without this, the SAQ discrimination sorts will not gate.

2. **A new `saq_binary` scoring model + per-part scorer.** `findScoringModel()`
   (~line 786) already reads `data-scoring-model` and would return `"saq_binary"`,
   but there is **no server-side `saq_binary` handler** — the default path is
   `"criteria"` (the essay rubric scorer). The SAQ scorer is a DIFFERENT contract,
   NOT the line-of-reasoning rows:
   - **Per part (A/B/C): binary 1/0** keyed to (a) verb-match (did the answer DO what
     identify/describe/explain demands?), (b) one specific named example present,
     (c) for "explain" parts, a causal/relevant reason (because-clause).
   - **Returns which part(s) missed** so the rewrite-weakest-PART rescore loop can
     target one part (S1/S2 only; never on the gate).
   - **Rubric IDs to register server-side:** `SAQ_S1_parts`, `SAQ_S2_full`,
     `SAQ_gate` (History 3-part), `SAQ_gov` (Concept Application / SCOTUS part
     criteria).
   - **Gateway behavior:** `SAQ_gate` returns pass = >=2 of 3 parts on the cold rep,
     driving `data-gateway="true"` gateway-lock.

3. **Re-verify the grading backend** (the hard-coded `hs-writing-grading...` URL/key
   in `lesson-engine.js` may be stale) and confirm the new rubric IDs exist before
   relying on gateway-lock.

---

## Verification needed before authoring SAQ content (against the LIVE CED)

- **SAQ section composition per subject:** AP World = 4 SAQs, answer 3 (Q1+Q2
  required, choose Q3 or Q4); APUSH = 3 SAQs (Q1+Q2 required, choose Q3 or Q4); AP
  Euro = confirm count/choice pattern. Confirm the ~40-min section / ~12-14 min-per-
  question budget is current.
- **Stimulus-by-question pattern** (Q1 secondary source, Q2 primary source, Q3/Q4 no
  source) against the current CED — it drives which reps are source-fed vs
  recall-only.
- **Official task-verb definitions + binary 1-point-per-part scoring** against the
  current CED/scoring guidelines (AMSCO reproduces the CED but is secondary; confirm
  identify/describe/explain tier definitions and the no-thesis / complete-sentences-
  not-bullets requirement verbatim).
- **The three reasoning processes** (comparison, causation, continuity-and-change) as
  per-part skill labels — confirm naming and that each part targets one.
- **Gov SAQ-family (PROVISIONAL):** confirm Concept Application + SCOTUS Comparison
  part structures and point allocations, and whether Gov still uses "SAQ" or
  "free-response" for these, against the live AP Gov CED. **If unverified at build
  time, ship the History gate only and hold the Gov branch.**
- **HuGeo (PROVISIONAL / light):** confirm its A/B/C verb-bound structure matches
  closely enough to reuse these lessons, or scope it out.
- **Reserved stimuli:** the S3 gate stimuli must be genuinely held out of S1/S2 (the
  prior B1L build leaked a source set) or "cold transfer" is fiction.

---

## Append instructions

1. Append this module as a new section after Unit 4 in `ap-lesson-map.md` (heading:
   "## SAQ Module (standalone, NON-spine) - Graft 3"), OR keep it as this separate
   file referenced from the map. **Recommended: keep separate** — it is non-spine and
   not every student takes it; a separate file keeps the spine map clean.
2. Update the map's lesson totals note: an **APUSH (full exam-ready)** student =
   Bridge 6 + Units 0/2/3/4 (13, incl. the 3.0 reading rep) + **SAQ Module 3 = 22
   lessons**. A History-essays-only student skips the module (19).
3. Gate Stage 03 SAQ content on the Engineering Handoff (the two engine extensions)
   and the Verification list above.
