# Instructional Design Knowledge Base — Four Layers

Reference document. Every principle is graded A/B/C (see `README.md`) and cited
to `03_Sources.md` by short key (e.g. [WWC-22], [WritingNext], [Hattie2007]).
Effect sizes are reported as the source states them (writing meta-analyses use
average weighted ES on writing quality; learning-science meta-analyses use
Hedges g or Cohen d — the two are NOT directly comparable).

Where a finding was proven outside writing, it is marked **[extrapolated to
writing]** so we never pretend a math/vocabulary result is a writing result.

---

## LAYER 1 — Learning-Science Foundations

The cognitive machinery under every design decision. Novice writers have the
same working memory as expert writers; the whole game is managing what we ask
that working memory to hold at once.

### 1.1 Cognitive Load Theory (CLT) — Grade A (applied rules)

**Core model.** Working memory is severely limited; long-term memory is not.
Learning = building schemas in long-term memory that let working memory treat
many elements as one. Three loads:

- **Intrinsic load** — the inherent difficulty of the material, set by *element
  interactivity* (how many things must be held in mind at once). A vocabulary
  word is low-interactivity; composing an argued paragraph from a source is
  very high.
- **Extraneous load** — load imposed by *how* material is presented. Wasted
  effort. The designer's job is to minimize it.
- **Germane load / processing** — working-memory resources actually spent
  building schemas.

**The load-additivity rule [A].** Intrinsic and extraneous load are additive.
Minimizing extraneous load "may permit an increase in the working resources
devoted to intrinsic cognitive load (also called germane processing)"
[Paas-vanMerrienboer2020]. → Every bit of extraneous load you remove is
capacity the student can spend on the actual writing move.

> Theory note: scholars dispute the deeper "three-types-of-load" architecture
> and whether germane load is a separate reservoir (Ton de Jong; "How Many
> Types of Load"). This dispute is about CLT's internal theory, **not** about
> the applied design rules below, which are robust. [Grade A for the rules,
> C for the internal architecture.]

**Worked-example effect [A].** "Novice students learn more from studying worked
examples that provide them with a solution than from solving the equivalent
problems" [Paas-vanMerrienboer2020]. For writing: annotated worked models,
labeled exemplars, and completed think-alouds beat throwing a novice at a blank
page. **[extrapolated to writing — proven mostly in math/science, but the SRSD
"Model It" stage is the writing-native version and is separately A-rated.]**

**Split-attention effect [A].** Learners learn more from a single integrated
source than from multiple sources separated in space or time
[Kalyuga1998]. For writing: put the annotation ON the exemplar sentence, not in
a separate legend the student must cross-reference.

**Redundancy effect [A].** Information that is already intelligible on its own
becomes harmful when you add redundant explanation. For an experienced learner,
explanatory text bolted onto a self-explanatory diagram *impairs* learning
[Kalyuga1998].

**Modality.** Presenting complementary information across visual + auditory
channels can expand effective working memory — but only for genuinely
complementary (not redundant) information.

### 1.2 The Expertise-Reversal Effect — Grade A (this is the engine of scaffold fading)

The single most important learning-science result for how we sequence support.

**The finding [A].** A 2025 PRISMA meta-analysis (176 effect sizes, 60 studies,
5,924 participants) [ExpertiseReversal2025]:
- Low-prior-knowledge learners learn **better** under high-assistance
  instruction: **d = 0.505**.
- High-prior-knowledge learners learn **better** under low-assistance
  instruction: **d = -0.428**.
- "Robust across a wide variety of contexts."

**The asymmetry [A].** The effect is NOT symmetrical: "providing novices with
assistance has a stronger effect than withholding assistance from experts."
→ **Design consequence: prioritize giving beginners strong support over
aggressively stripping scaffolds from advanced students.** When unsure whether
a student is ready to lose a scaffold, keep it a bit longer — the downside of
over-support is smaller than the downside of under-support.

**The format shifts with expertise [A].** As expertise rises, the optimal
design changes — from physically integrating diagram + explanatory text
(reduces split-attention for novices) to eliminating the text entirely (removes
redundancy for experts) [Kalyuga1998]. The same content needs a *different
package* for a novice vs. an expert.

**The boundary condition we must not hide [C for writing].** The 2025
meta-analysis explicitly flags that evidence is **weaker for younger students
and for humanities / language-learning** — which is exactly where high-school
writing sits. So: expertise-reversal / scaffold fading is a **well-grounded
extrapolation** to writing, not a domain-proven result. Fade **gradually and
principled**, not abruptly, and validate locally with our own student data.

### 1.3 Spacing — Grade A

**Spaced beats massed [A].** Distributing practice on the same content over
time produces durable gains: spaced vs. massed retrieval **g = 0.74**
[Latimier2021]. Confirmed across ages and domains — math for 11-12 year-olds,
university physics homework over a term, 8th-grade history retained over 9
months, adult vocabulary over 5 years [Carpenter2022].

**Do NOT bother engineering expanding intervals [A].** Expanding schedules
(progressively longer gaps) show **no meaningful advantage** over simple uniform
spacing (expanding vs. uniform g = 0.034, non-significant) [Latimier2021]. The
common belief that intervals must lengthen is not supported. (Minor moderator:
expanding becomes slightly better only under many test sessions.) → **Uniform
spacing is fine. Don't overbuild the schedule.**

**Design consequence.** Revisit each writing strategy / rhetorical move across
multiple sessions rather than teaching it once and moving on. Successive
relearning (spacing + retrieval combined) is a distinct, effective technique
[Carpenter2022]. **[extrapolated — proven on facts/concepts, not composing
skills; see open question in `02`.]**

### 1.4 Retrieval Practice — Grade A (with a conditional boundary)

**Retrieval aids retention AND can support transfer [A].** Low-stakes
retrieval/quizzing improves retention and can support transfer/application of
*complex* concepts, not just verbatim recall [Corral-Carpenter2025;
Carpenter2022].

**But transfer is conditional, not automatic [A — this is the key boundary].**
- One practice round + immediate test (8 min): retrieval beat restudy on
  *repeated* questions but showed **NO advantage on application/transfer
  questions** (Exp 1, N=309).
- Three practice rounds + one-week delay: retrieval outperformed restudy on BOTH
  repeated AND application questions (Exp 2-3) [Corral-Carpenter2025].

→ **Design consequence: to get transfer, use spaced, multi-round retrieval with
delayed application items. One-and-done quizzes buy retention, not transfer.**
Retrieval seems to help chiefly by strengthening the *recognition* component —
recognizing when a concept applies. **[extrapolated — proven on research-methods
concepts, not writing.]**

### 1.5 Transfer of Learning — Grade B

- Retrieval "can promote" far transfer (inferential questions in a new domain)
  [Carpenter2022] — but "can," not "reliably does." Far transfer is real but
  moderate and weakens with distance (Pan & Rickard 2018, ~d = 0.40).
- **Rote acquisition does not transfer** [UbD]: students taught mechanically
  solve familiar decontextualized problems but fail novel/complex ones. This is
  the whole rationale for designing toward transfer explicitly (see Layer 3,
  UbD's T/M/A coding).
- Transfer must be **designed for**, not assumed. Near transfer (same genre,
  new prompt) is far more reliable than far transfer (argument skill → lab
  report). Our courses should claim near transfer confidently and far transfer
  cautiously.

### 1.6 Learning Styles — the myth, precisely stated — Grade B

Do NOT design instruction around matching to "preferred learning styles." A 2024
meta-analysis (21 studies) found a small detectable matching effect (g = 0.31)
but the authors conclude it is "too small and too inconsistent to justify
designing instruction around" [LearningStyles2024]. Only 26% of effect sizes
showed the crossover pattern the theory actually requires, mostly in low-quality
studies; all studies were single-session (no durable benefit shown).

**The design win instead: multimodal instruction** — presenting content in
complementary modes for *all* students — is stronger and more cost-effective
(modality effect g ≈ 0.70, roughly double) [LearningStyles2024]. Design for the
content's demands and use multiple modes for everyone; don't sort students.

---

## LAYER 2 — Writing-Specific Pedagogy

What actually improves adolescent writing, from the meta-analyses and the WWC.
This is where the strongest, most directly-applicable evidence lives.

### 2.1 The WWC top-tier recommendation — Grade A

WWC Practice Guide #22, *Teaching Secondary Students to Write Effectively*
(grades 6-12), gives its **STRONG** rating (11 supporting studies) to exactly
one thing [WWC-22]:

> **Recommendation 1 (STRONG): Explicitly teach appropriate writing strategies
> using a Model-Practice-Reflect instructional cycle.**

The other two recommendations are weaker:
- Rec 2 — Integrate writing and reading to emphasize key writing features:
  **MODERATE**.
- Rec 3 — Use assessments of student writing to inform instruction and
  feedback: **MINIMAL**.

→ This is the strongest single validation of our teach → model → guided-practice
→ independent → transfer spine. The Model-Practice-Reflect cycle IS our spine.

### 2.2 The Writing Next ranked menu — Grade A (use it as a build-priority list)

Graham & Perin (2007), meta-analysis of 123 documents / 154 effect sizes,
grades 4-12. Average weighted effect size on **writing quality**
[WritingNext]:

| Rank | Element | ES | Design read |
|---|---|---|---|
| 1 | **Strategy instruction** | **0.82** | Top lever. This is SRSD territory. Build here first. |
| 2 | **Summarization** | **0.82** | Teach summarizing explicitly; it's not a freebie skill. |
| 3 | **Collaborative / peer writing** | **0.75** | Peer structures work — adapt for self-paced (see `02`). |
| 4 | **Setting product goals** | **0.70** | Give specific product goals ("add 2 counterarguments"), not "do your best." |
| 5 | Word processing | 0.55 | Compose digitally; especially helps low achievers. |
| 6 | **Sentence combining** | **0.50** | The evidence-based route to syntactic maturity. |
| 7 | Inquiry | 0.32 | Analyze concrete data before writing. |
| 8 | Prewriting | 0.32 | Planning helps, modestly. |
| 9 | Process writing approach | 0.32 | Modest on its own; not a substitute for strategy instruction. |
| 10 | Study of models | 0.25 | Real but smaller — pair with strategy instruction, don't rely on alone. |
| 11 | **Grammar instruction** | **-0.32** | NEGATIVE. See 2.3. |

Treat this as a **menu of options to combine in an optimal mix**, explicitly not
a full curriculum and not a single fix [WritingNext / adlit summary].

### 2.3 The grammar-in-isolation trap — Grade A (with a crucial nuance)

Traditional grammar instruction had a **statistically significant NEGATIVE**
effect on writing quality: **-0.32**, robust to outlier trimming (-0.34, CI
-0.46 to -0.23) [WritingNext].

**The nuance the source itself flags — do not overread this:**
- Grammar was the *control* condition in 10 of 11 studies (so the comparison is
  partly "grammar vs. a real writing intervention").
- **In-context** grammar (Fearn & Farnan) produced *positive* effects.

→ **The correct design rule is "no isolated grammar drills as a path to better
writing," NOT "never address conventions."** Address conventions in the context
of composing, and build syntax through **sentence combining (0.50)**, which is
the evidence-based route. This validates our "grammar as a separate thread /
build automaticity, then compose" instinct — with the caveat that the thread
must reconnect to real writing.

### 2.4 Writing about text (reading-writing link) — Grade A

Graham & Hebert, *Writing to Read* (Carnegie) [WritingToRead]:
- Writing about text improves reading comprehension: **ES 0.40** (norm-referenced,
  11 studies) to **0.51** (researcher-designed, 50 studies). 57/61 outcomes
  (93%) positive, grades 2-12, across science/social studies/English.
- **Extended writing** (personal response + analysis/interpretation) had the
  **strongest and most consistent** impact — stronger than summary or
  note-taking.
- Summary writing helped middle/high schoolers **less** than elementary (0.33
  vs 0.79); note-taking ≈ 0.47-0.48.
- **CRITICAL for us:** for lower-achieving students, writing about text worked
  (ES 0.63) **only when they were explicitly taught how** to use the writing
  activity; without explicit instruction the effect was **not greater than
  zero.**

→ Validates source-bound, read-then-write-about-it designs (our Issue-Card →
real-source evolution). And it independently validates that unscaffolded "just
write about this text" tasks fail for the students who need help most —
explicit instruction is a *requirement*, not a nicety.

### 2.5 SRSD — Self-Regulated Strategy Development — Grade A (our spine, validated)

The best-evidenced framework in adolescent writing.

- **Magnitude [A]:** SRSD's average weighted ES = **1.14** vs **0.62** for
  non-SRSD strategy instruction (Q-between = 14.65, p < .001) [WritingNext].
  Especially large for **struggling writers** (1.02 vs 0.70 for general
  students in the broader strategy pool).
- Research base: 170+ studies; a meta-analysis found SRSD ~3× more effective
  than traditional instruction, effect sizes well over 1.0; a 2023 meta-analysis
  confirmed gains specifically in grades 6-12, reportedly without disparity by
  race/ethnicity/SES [SRSDonline].

**The SRSD six stages** (this is the operational spine — memorize it):
1. **Develop Background Knowledge** — pre-teach what students need to use the
   strategy.
2. **Discuss It** — the strategy, its purpose, when/why to use it; build buy-in.
3. **Model It** — teacher/expert think-aloud, including self-talk (the
   worked-example + coping-model stage).
4. **Memorize It** — commit the mnemonic/steps to memory so they don't consume
   working memory during writing.
5. **Support It** — guided practice with scaffolds (charts, prompts) gradually
   faded.
6. **Independent Performance** — student uses the strategy alone; scaffolds gone.

This is a **gradual release of responsibility** (collaborative modeling →
supported practice → independent performance) that *explicitly teaches
self-regulation* (goal-setting, self-monitoring, self-instruction,
self-reinforcement) — not just the writing moves. Our HIT / PROVE / S³ mnemonics
are the "Memorize It" artifacts of exactly this framework.

> Caveat carried from verification: a parenthetical mis-attributed the exact
> grade ranges of the 1.14 figure (it's a Writing Next moderator subset, not the
> separate Graham & Harris 2003 SRSD meta-analysis). The ES comparison itself is
> exact.

### 2.6 Sentence Combining & Syntactic Development — Grade A (within Writing Next)

Sentence combining (ES 0.50) is the evidence-based route to syntactic maturity —
students combine short kernel sentences into more complex ones, building
sentence-level control without isolated grammar drill. This is the mechanism
that makes "grammar as a separate thread" productive rather than harmful (2.3).
The Writing Revolution / Hochman method's sentence-level work
(because/but/so, sentence expansion, appositives) operationalizes this at the
sentence and paragraph level before the essay. **[Hochman/TWR is on-disk primary
source; its specific method is practitioner-validated, graded B pending its own
meta-analytic base.]**

---

## LAYER 3 — Instructional-Design Process & Models

How to structure a course. NOTE: none of these models survived the workflow's
final adversarial cut as *effect-size-backed* — they are design *frameworks*,
validated by use and by theory more than by RCT. Graded accordingly. Use them as
scaffolding for our own design, not as evidence claims.

### 3.1 Backward Design / Understanding by Design (UbD) — Grade B (framework)

Wiggins & McTighe [UbD]. Plan in reverse of activity-first habits:

1. **Stage 1 — Desired Results.** What should students understand and be able to
   do (transfer)?
2. **Stage 2 — Evidence / Assessment.** How will we know? Design the assessment
   *before* the instruction ("think like an assessor first"). Authentic
   performance tasks are culminating, unit-level — not daily.
3. **Stage 3 — Learning Plan.** The activities that build toward Stage 1,
   assessed by Stage 2.

**All three stages must align** — Stage 1 content is what Stage 2 assesses and
Stage 3 teaches. Misalignment is the #1 curriculum defect UbD catches.

**T/M/A coding [useful tool]:** in Stage 3, code every learning event as
**T**ransfer, **M**eaning-making, or **A**cquisition, to guarantee instruction
moves past information delivery (Acquisition) into meaning-making and transfer.
Rote acquisition does not transfer.

**Six Facets of Understanding** (explain, interpret, apply, demonstrate
perspective, empathize, self-knowledge) — indicators for designing assessments.
Deliberately NOT a hierarchy (unlike Bloom); pick the facets that fit.

> The UbD white paper provides **no effect sizes** — it claims a two-stream
> evidence base (cognitive psych + achievement studies) but points elsewhere for
> the data. Treat UbD as a disciplined planning *process*, not an evidence
> claim.

### 3.2 4C/ID — Four-Component Instructional Design — Grade B (best fit for complex-skill / whole-task writing)

van Merriënboer; *Ten Steps to Complex Learning* (4th ed. 2024) [TenSteps;
4cid.org]. Purpose-built for **complex skills / professional competencies** —
which is exactly what writing is (many interacting sub-skills, not discrete
facts). The four components:

1. **Learning Tasks** — authentic **whole-task** practice, the organizing
   backbone. Students work on real, whole writing tasks from early on (in
   simplified/supported form), not a long march of isolated part-tasks.
2. **Supportive Information** — the "theory" for the non-routine, problem-solving
   aspects (how to reason about audience, argument, evidence). Available for
   study.
3. **Procedural Information** — just-in-time "how-to" for the routine aspects,
   delivered *during* task performance (e.g., a formatting rule shown at the
   moment of need).
4. **Part-task Practice** — only when a routine component needs very high
   automaticity (multiplication-tables analogue: e.g., sentence-combining reps,
   comma rules). NOT the default.

**Built-in scaffold fading:** procedural support is gradually withdrawn as the
learner masters routine aspects — 4C/ID has scaffold fading in its DNA, matching
our design.

**Why this matters for us:** 4C/ID is the model that says *start with whole
writing tasks and simplify them*, rather than teaching sentences → paragraphs →
essays in strict isolation. It's the theoretical counterweight to a purely
bottom-up build, and worth weighing when we sequence a unit. (See `02` for the
whole-task vs. part-task decision rule.)

### 3.3 Mastery Learning & the 2-Sigma Problem (Bloom) — Grade B (as general method), C (for writing)

Bloom (1984) [Bloom1984]:
- **1:1 tutoring ≈ +2 sigma** over conventional group instruction (average
  tutored student > ~98% of a control class).
- **Mastery Learning** (formative testing + feedback-corrective loop) ≈
  **+1 sigma** (average student > ~84% of conventionally taught).
- Alterable-variables leverage: tutoring 2.00, reinforcement 1.20,
  feedback-corrective mastery learning 1.00, cues & explanations 1.00.
- Time-on-task rises: ~65% conventional → 75% mastery → 90%+ tutoring.
- The "2-sigma problem" is the still-open challenge of finding *group/scalable*
  methods that match tutoring. Combining mastery learning with 1-2 other
  variables *approaches* but has not exceeded 2 sigma.

**This is the theoretical backbone of the whole 2 Hour Learning / self-paced
mastery model** — an AI tutor + mastery gating is a direct attempt to
operationalize Bloom's alterable variables at scale.

**BUT — two hard caveats:**
1. **The 2-sigma figure itself is contested.** Later replications generally find
   1:1 tutoring effects well below 2 sigma; 2 sigma was from small studies with
   mastery-based comparisons. Treat "+2 sigma" as aspirational lore, not a
   settled effect size.
2. **Mastery is not proven for writing, and is actively critiqued for it** (see
   Layer-2/Audit). No verified claim in our research supports mastery/self-paced
   delivery for *writing* specifically.

### 3.4 ADDIE & Gagné's Nine Events — Grade C (process scaffolds, low evidentiary weight)

- **ADDIE** (Analyze, Design, Develop, Implement, Evaluate) — a generic
  project-management skeleton for building instruction. Useful as a checklist for
  *our production pipeline*, not a learning theory. No effect-size base.
- **Gagné's Nine Events of Instruction** (gain attention → inform objective →
  stimulate recall of prior learning → present content → provide guidance →
  elicit performance → give feedback → assess → enhance retention/transfer) — a
  lesson-level sequence that maps almost 1:1 onto our teach/model/guided/
  independent spine and Rosenshine's principles. Use it as a **lesson-completeness
  checklist** (did we do all nine?), not as an evidence claim.

### 3.5 Learning Progressions — Grade B (framework)

A learning progression is an evidence-informed, ordered description of
increasingly sophisticated ways of reasoning/performing in a domain, from novice
to target. For writing this is our skill map / knowledge graph: prerequisites
before dependents, each rung a demonstrable performance. Aligns with mastery
gating (Layer 4) and with the Math-Academy-style knowledge-graph the team
already references. The design obligation: make each rung an *observable writing
performance*, and pin prerequisites so remediation is targeted.

---

## LAYER 4 — Assessment & Measurement

How we know it worked, and how assessment itself drives learning.

### 4.1 Feedback that works — Hattie & Timperley — Grade A

*The Power of Feedback* (2007), 12 meta-analyses / 196 studies / 6,972 effect
sizes [Hattie2007]:

- **Feedback average ES ≈ 0.79** on achievement — roughly double the 0.40 average
  effect of schooling; top 5-10 influences. **But highly variable** — some
  feedback is negative.
- **The three questions** effective feedback answers:
  1. **"Where am I going?"** (feed up — the goal)
  2. **"How am I going?"** (feed back — current status vs. goal)
  3. **"Where to next?"** (feed forward — the next move)
- **Four levels** feedback can target, in rough order of power:
  - **Task** (correct/incorrect, more information) — useful.
  - **Process** (the strategy/process behind the task) — powerful, transfers.
  - **Self-regulation** (metacognition, self-monitoring) — powerful.
  - **Self / personal** ("Good girl!", "great effort!") — **ineffective**;
    carries no task information. Teacher praise correlates only ~0.12 with
    achievement; no-praise conditions show higher effect (0.34).
- **Least effective:** programmed instruction, praise, punishment, extrinsic
  rewards. Extrinsic tangible rewards correlated **negatively** with performance
  (-0.34) and undermined intrinsic motivation on interesting tasks (-0.68),
  worse when controlling (-0.78).

→ **Design rule: our AI/rubric feedback must target the process and
self-regulation levels ("here's the move to fix, here's how to check it
yourself"), answer the three questions, and avoid person-praise and
grade-only feedback.**

### 4.2 Formative assessment — Black & Wiliam — Grade A

*Inside the Black Box* (~580 studies) [BlackWiliam1998]:
- Strengthening classroom formative assessment produces gains of **ES ≈
  0.4-0.7** — "larger than most educational interventions."
- **Disproportionately helps low achievers**, narrowing gaps while raising
  overall attainment.
- **Marks/grades alone do not improve learning.** Effective feedback is
  task-focused, describes qualities of the work, gives specific improvement
  advice. (Converges exactly with Hattie.)
- **Student self-assessment is essential, not optional.** The main barrier is
  that pupils lack a clear picture of the learning target — so effective
  feedback requires (a) recognizing the goal, (b) knowing the present position,
  (c) understanding a way to close the gap. (This IS the Hattie three-questions
  model, from the assessment side.)

### 4.3 Rubric design — Grade B (types) / C (single-point specifics)

Three types [CultOfPedagogy; and see 4.4 for the calibration evidence]:

- **Holistic** — one overall judgment. Fast to score; **no targeted feedback**.
  Good for gating throughput, bad for growth.
- **Analytic** — itemized criteria × quality levels grid. Shows students *why*
  they got a score; time-consuming; students may not read the dense grid. Our
  AP-style multi-trait rubrics are analytic.
- **Single-point** — describes ONLY the proficiency criteria (one middle
  column); "areas of concern" and "evidence of exceeding" are open-ended columns
  for feedback. A 2010 action-research review (Fluckiger) found achievement
  increased with single-point rubrics, **especially when students co-created them
  and used them to self-assess** [CultOfPedagogy]. Prescribing the top level can
  cap creativity; leaving it open lets students exceed expectations.

→ Design read: use **analytic** rubrics where diagnostic feedback and calibration
matter (most instruction); consider **single-point** for open/creative tasks and
to drive self-assessment; reserve **holistic** for fast gate throughput only.
**Caution (see 4.4): rubrics alone do not fix calibration.**

### 4.4 Self-assessment & calibration — Grade A (effect) / A (the limits)

Two large meta-analyses:

**Self-assessment works [A].** Self-assessment interventions: **g = 0.585**;
peer-assessment: **g = 0.606**; combined self+peer smaller (g = 0.448 — mixing
is not additive). 626 effect sizes / 175 studies / 19,383 participants
[SelfPeerAssessment2022]. Online delivery boosts peer- but not self-assessment.

**But students are miscalibrated, and here's how to fix it [A].** 160 articles /
29,352 participants [SelfAssessmentAccuracy2023]:
- Students systematically **overestimate** their work vs. the expert (bias g =
  0.206), but self and expert scores share meaningful variance (correlation z =
  0.472). → Self-scores are informative but skew high; don't take them at face
  value.
- **Feedback is THE lever for calibration accuracy** — the only moderator
  significant in both analyses; it moves self-scores toward the expert's. Pair
  self-assessment with external feedback + repeated practice.
- **Rubrics alone did NOT significantly improve calibration** (with-rubric bias
  g = 0.185 vs 0.231 without — non-significant difference). Rubrics nudge but
  don't guarantee valid self-judgment. → *Tempers* any claim that "give them the
  rubric" fixes self-assessment.
- **Calibration is trainable** — prior self-assessment experience improved
  accuracy (g = 0.177). Build a calibration *progression*, don't expect accuracy
  on day one.
- Accuracy **varies by level** — primary/secondary students correlated with
  experts far better (z = 0.79 / 0.72) than undergrads (0.44). Encouraging for
  HS; caution against importing college self-assessment findings.

→ **Design rule: build a scaffolded self-assessment progression, and always pair
student self-scoring with expert (AI/teacher) feedback. The rubric is necessary
but not sufficient — the feedback + repetition is what calibrates.** This
validates our calibration progression (binary → 3-point → AP → self-diagnosis)
AND corrects a likely over-reliance on "the rubric will teach them to
self-assess."

### 4.5 Mastery gating & validity/reliability — Grade B/C

- **Mastery gating** (don't advance until you demonstrate the skill) follows
  directly from Bloom's feedback-corrective loop (3.3) and learning progressions
  (3.5). Strongly motivated by theory; **not writing-proven**. The design risk
  for writing: what counts as "mastered" is far fuzzier than in math, and a poorly
  set gate mislabels slower students as deficient (see Audit).
- **Reliability** (would another rater/occasion give the same score?) is the
  central measurement problem for writing assessment — writing scores are
  notoriously rater-dependent. For an AI grader this means **inter-rater
  agreement with expert humans is the validity check that matters**, and gates
  should be set with the grader's reliability envelope in mind (don't gate on a
  1-point difference the grader can't reliably detect).
- **Validity** (are we measuring writing skill, or formula compliance?) is the
  deep risk the mastery critique raises: standards so tight they can be gamed
  measure conformity, not writing. Build gates on traits that require genuine
  composition, not surface features.

---

## Cross-layer synthesis — the four layers as one design logic

1. **CLT** says: manage working memory. →
2. **SRSD / WWC / Writing Next** give the writing-native way to do it: explicitly
   teach a strategy, model it, memorize it (offload to LTM), practice with fading
   support. →
3. **Expertise reversal + spacing + retrieval** say: match support to expertise,
   fade it as schemas build, and revisit across time with multi-round delayed
   retrieval so it sticks and transfers. →
4. **UbD / 4C/ID / mastery / progressions** give the course-level container:
   backward-designed from transfer goals, built around authentic whole tasks,
   sequenced as a progression, gated by demonstrated mastery. →
5. **Hattie / Black & Wiliam / self-assessment** close the loop: process-level
   feedback + trained self-assessment drive each next step and calibrate the
   learner — which is itself the "self-regulation" that SRSD is named for.

The frameworks aren't competing. SRSD is the lesson engine; 4C/ID and UbD are the
course container; CLT and expertise-reversal set the support curve; spacing and
retrieval set the timeline; feedback and self-assessment run the control loop.
