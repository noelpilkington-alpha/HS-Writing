# Authoring Playbook: T8 Cross-Source Synthesis (WEAVE)

> **Archetype:** Type 8, cross-source-synthesis. **Mnemonic:** WEAVE (status:
> proposal, NOT sourced). **Production ceiling:** essay. **Core move:** put two
> or more sources in conversation and combine them into ONE argument, tracking
> which idea came from which source. **Defining failure it discriminates
> against:** "summary + summary" (Source A reported, then Source B reported,
> never joined).
>
> This entry is grounded in the internal extraction (`extract_T8_WEAVE.md`,
> principles P1 to P20), the 19 gates in `pipeline/lesson_contract.py`, the two
> combinable gold exemplars in `AnchorSets/`, and the four verified Phase-2
> research briefs. Every move carries an anchor. House rule: no em dashes; own
> words; cite every external source.

---

## 1. Terminal deliverable and production ceiling

**Terminal deliverable:** a synthesized paragraph, then a full multi-source
essay, on a bound paired set. The student states ONE claim that BOTH sources
support (or, in the opposing variant, weighs one against the other and picks),
attributes each idea to its source, and writes at least one explicit sentence
that says HOW the two connect. The essay is an extended-text item scored by an
external `rc.*` rubric grader.

**Ceiling: essay.** T8 is one of only two archetypes allowed to reach the essay
unit (`TYPE_CEILING_UNIT[8] = "essay"`; only T7 essay-assembly and T8 synthesis
reach it; every component type tops out at paragraph or sentence). This is the
direct foundation for G11 AP synthesis (6 sources), so the moves taught here must
scale (extract, section 0).

**Why this archetype is the highest-load of the eight:** it takes the
evidence-integration move (T3/PROVE) and multiplies it by the number of sources,
so intrinsic load is HIGH (extract section 0; KB 00 section 1.1
element-interactivity). Two consequences drive the whole design: (a) staging is
non-negotiable, never introduce the second source until single-source
integration is fluent; (b) the lesson is built end to end to discriminate
genuine synthesis from summary-plus-summary (extract section 0).

**Rubric routing:** `rc.mcas` for complementary (same-side) sets, `rc.ohio` for
opposing sets, the AP overlay (`rc.ap`) for G11-target items. These are the only
configs the deployed grader implements (`RUBRIC_CONFIGS` in lesson_contract).

---

## 2. The SRSD shell, stage by stage

The shell is machine-required in order (`gate_shell_completeness`: TEACH ->
MODEL -> SUPPORTED -> INDEPENDENT -> TRANSFER, first occurrence of each role
monotonically increasing). Async-SRSD research confirms which stages survive a
stateless, no-human screen: TEACH, MEMORIZE, and INDEPENDENT port largely
intact; DISCUSS must be reconverted from dialogue into media plus choice items;
MODEL and SUPPORT are the human-dependent stages that must be reconstructed
(research_async-srsd section 2, verified against WWC 2017 SRSD Intervention
Report). Below, each stage gives the T8 moves, the worked-example shape, and the
stateless delivery method.

### TEACH (develop background knowledge, discuss it, orient the demand)

**Moves.**

- **Define "synthesis" in plain words in a TEACH slot before it appears
  anywhere else.** This is the signature constraint for T8: `synthes(is|ize|ise)`
  is a `_TECH_TERMS` entry, so `gate_define_before_use` REJECTS the lesson the
  moment "synthesis" (or the mnemonic gloss) appears in any body or feedback
  without a TEACH definition carrying a definitional cue ("means", "is when",
  "in other words") within about 120 characters. Author it as: "To synthesize
  means to combine ideas from more than one source into a single argument, in
  other words to make the sources talk to each other instead of taking turns."
  (extract P1; lesson_contract `gate_define_before_use`.)
- **Name the ONE strategy and its cue, and state a countable product goal.**
  State WEAVE (Which source says what, Establish the shared thread, Attribute
  each idea, Voice your own claim across them, Explain how they combine) and give
  a concrete target, not "do your best": for example "one claim supported by
  evidence from BOTH sources, each idea attributed to its source, plus one
  sentence that explains how the two connect." Named strategy plus specific
  product goal are two separate documented levers (Graham and Perin 2007,
  Writing Next: strategy instruction mean ES 0.82, SRSD variant 1.14, specific
  product goals 0.70, "study of models" alone only 0.25;
  https://www.thewritingrevolution.org/wp-content/uploads/2017/05/WritingNext.pdf).
  (extract P2.)
- **Orient the test demand and the staging ladder up front.** Tell the student
  this is the MCAS "use information from both articles" move and the Ohio
  "synthesize then pick" move, and that the ladder runs single -> complementary
  (same-side) -> opposing (hardest: synthesize, weigh, pick). Naming the
  culminating performance first is UbD Stage-1/Stage-2 backward design (extract
  P3).
- **If the opposing variant is taught, define "counterclaim" here too.** It is
  also a `_TECH_TERMS` entry; the Ohio opposing form asks the student to weigh
  and pick, which pulls the word in. Define it in TEACH or do not use it
  (extract P4).
- **Do NOT tell the student to mark up either source.** T8 is the type most
  tempted to write "underline the shared idea in each article" because the core
  move is "which source says what." `gate_no_source_markup` REJECTS
  underline/circle/highlight/annotate imperatives on any display slot, because
  Timeback stimuli are display-only XHTML with JavaScript stripped. Use "read
  and note" framing, or push the mapping into a discrete choice/hottext item
  (extract P5; lesson_contract `gate_no_source_markup`).

**Worked-example shape here:** a short teach card (>= 200 chars,
`_DEPTH_FLOOR`) that names the strategy, defines synthesis, and shows the demand.
No source markup.

**Stateless delivery:** display stimulus for the concept, plus discrimination
(choice) items that check the target concepts. This is exactly the async-valid
reconversion of DISCUSS from live conversation to media-plus-choice
(research_async-srsd section 2).

### MODEL (the four-mechanism async sequence, not a passive-read think-aloud)

The live teacher coping-model think-aloud is the single most human-feeling SRSD
move, and a solo student passively reading a "messy think-aloud" does NOT inherit
SRSD's live-enacted effect size. Only the informational/worked-example
ingredient survives cold text, so error-recovery is delivered through mechanisms
that survive async delivery (extract section on MODEL; research_async-srsd
section 3). `gate_model_sequence` requires, in the MODEL role, an
`annotated_before_after` AND a `predict_the_fix` with a non-empty feedback
reveal, plus a `diagnosis_frq` somewhere in the lesson.

**Moves.**

- **The worked example is the summary+summary -> woven contrast, with BOTH
  source ideas present in BOTH the BEFORE and the AFTER.**
  `gate_content_depth` requires the `annotated_before_after` body to contain the
  literal tokens BEFORE and AFTER and clear 220 chars. Put the annotation ON the
  exemplar sentence, not in a separate legend (KB section 1.1 split-attention).
  (extract P6; worked-example section below.)
- **Predict-the-fix targets the join, and it must carry a reveal.** The choice
  item asks the student to diagnose the weak (side-by-side) version BEFORE the
  answer shows: "Which single move would most improve this: (A) add a sentence
  stating how the two sources' ideas connect and attribute each, or (B) add more
  detail from Source B?" then the SAME item reveals the fix and the WHY.
  Committing to a prediction before the reveal is the mechanism, not wasted
  motion (Metcalfe 2017, Learning from Errors: errorful generation plus
  corrective feedback beats error-free study, largest for high-confidence
  errors;
  https://www.columbia.edu/cu/psychology/metcalfe/PDFs/Learning%20from%20errorsAnnual%20ReviewMetcalfe2016.pdf).
  `gate_model_sequence` rejects a `predict_the_fix` with empty feedback (extract
  P7).
- **Include a student-generated diagnosis slot, and scaffold HOW to diagnose.**
  A `diagnosis_frq` is required by `gate_model_sequence` (mechanism 4) and by
  `gate_model_before_required`, which rejects a diagnosis_frq that has no MODEL
  before it AND one whose body gives no frame/checklist/named steps. Provide a
  frame: "Name what was missing (no connecting sentence, or an unattributed
  idea?); say what you added; say why the woven version is stronger." A
  self-question SCRIPT beats a bare rubric for driving self-regulation (Panadero,
  Alonso-Tapia and Huertas 2012: scripts > rubrics > no tool on the online
  self-regulation index;
  https://repositorio.uam.es/handle/10486/710139). (extract P8.)
- **Every "which source" reference must show its referent in the same slot, or
  bind the source.** With two sources, deictic phrases ("the passage above",
  "this version", "the summary") multiply the "which one?" ambiguity.
  `gate_no_ambiguous_reference` rejects such phrases unless the slot quotes the
  referent inline, shows a BEFORE/AFTER, lists options, or binds a ref. Name
  sources distinctly (Source A / Source B, or their titles) everywhere (extract
  P9).

**Stateless delivery:** the MODEL is a FIXED annotated before/after worked
example, NOT a live or simulated human performance. Show the summary+summary
BEFORE and the woven AFTER, and label the common error and its fix as
author-voice annotations printed ON the exemplar sentence ("problem: two ideas
reported side by side, no connecting claim" / "fix: one sentence stating how
Source A and Source B connect, each idea attributed"). Pair it with the
predict-the-fix choice item so the learner diagnoses the flaw before the reveal.
There is NO near-peer persona and NO coping self-talk or false-start monologue:
static screen text cannot carry the live social-modeling mechanism, so the async
adaptation is an annotated worked example with labeled error annotation plus
predict-the-fix, not a coping model reconstructed as fixed media. The IES/WWC
Secondary Writing guide makes explicit modeling with identified errors and
corrections a STRONG-evidence recommendation (Rec 1, Model-Practice-Reflect;
https://ies.ed.gov/ncee/wwc/PracticeGuide/22), and that is the modality-flexible
ingredient that survives cold text. Do NOT claim SRSD's live coping-model effect
size for it; keep the effect-size-honesty discipline (research_async-srsd
section 3; research_feedback-as-teaching 1.10).

### SUPPORTED (guided practice on a fade ladder, discrimination first)

**Moves.**

- **Discrimination precedes production, and it is LABELED a Grade-C design
  bet.** `gate_discrimination_before_production` requires at least one
  `discrimination` slot before any production/diagnosis FRQ AND requires
  `labeled_grade_c=True` on it. For T8 the discrimination is the defining
  contrast: a "two summaries in sequence" response next to a genuinely combined
  one, and a correctly-attributed vs source-confused pair. Write into the body
  that discrimination-before-production is a design bet, not a proven law
  (KB 02 section 4: UNVALIDATED, keep + label + A/B test). (extract P10.)
- **Ship a FIXED-FADE ladder staged by source-count and source-relationship;
  performance-based routing between rungs is UNBUILT (assumed pending eng).** The
  fade ladder is a fixed, pre-scripted sequence: worked synthesis exemplar ->
  claim given plus student combines two PROVIDED evidence pieces -> student finds
  and combines across both gated sources -> independent; and the
  source-relationship climbs single -> complementary -> opposing. This runs as a
  self-sufficient sequence that needs zero routing to function. Fading the ladder
  or source-count adaptively on the student's demonstrated performance would
  require between-lesson score-based routing, which is NOT a delivered capability;
  it is contingent on the platform actually supporting next-lesson routing on a
  grader score. Keep the fixed scaffold one rung longer when unsure (humanities
  under-support caveat; expertise-reversal is asymmetric, Kalyuga 2007;
  https://www.uky.edu/~gmswan3/EDC608/Kalyuga2007_Article_ExpertiseReversalEffectAndItsI.pdf).
  (extract P11.)
- **CUE the sentence-level TWR moves as ALREADY-FADED prerequisites; do NOT
  re-teach them here.** T8 SYNTHESIZES; its sentence-level sub-skills were built
  and faded earlier: because/but/so as the reasoning hinge (T2/T3), and the
  modifiers by function drawn on when integrating each source (appositive =
  attribute AUTHORITY, name and credential the source; prepositional phrase = add
  CONTEXT / narrow scope; relative clause = introduce a CONSEQUENCE, from
  T3/T4). At the point where the student fuses cross-source evidence into ONE
  sentence and attributes each idea, REFERENCE these moves as tools the student
  already owns, do not re-scaffold them (shared fade ledger; sentence-combining ES
  0.50, Writing Next). Gate, do not re-teach, the mechanical substrate: AlphaWrite
  owns sentence-combining craft G3-8 and EGUMPP owns conventions G3-10; T8 applies
  them as retrieval-gated prerequisites and teaches only the rhetorical USE. Do
  not stack a second mnemonic on WEAVE (extract P12).
- **The unit of production must not drop back down.** `gate_unit_ladder`
  requires every scored `production_frq` to declare a unit and requires the
  sequence to be non-decreasing (sentence -> paragraph -> multi_paragraph ->
  essay). Fusing at the sentence level, then a synthesized paragraph, then a
  two-source essay is legal; a sentence AFTER an essay is rejected (extract P13).

**Worked-example shape here:** backward-faded completion items (see section 4).

**Stateless delivery:** the fade is authored as a decreasing-support SEQUENCE of
isolated items (worked example -> completion/choice item -> independent
production), with the external grader carrying the formative-feedback role. The
fixed-schedule fade needs no prior-response memory and is empirically validated
(Renkl et al. 2002;
https://www.davidlewisphd.com/courses/EDD8121/readings/2002-Renkl_et_al.pdf).
Intelligent writing tutors already deliver strategy instruction plus automated
feedback with no teacher in the loop (Writing Pal;
https://files.eric.ed.gov/fulltext/ED585788.pdf). (research_async-srsd section 4;
research_worked-example-fading Claim 1.)

### INDEPENDENT (perform with scaffolds removed)

**Moves.**

- **Independent performance is a synthesized paragraph or essay on the SAME
  gated sources, scaffolds gone.** The student maps both sources, states one
  claim across them, attributes each idea, and explains the connection with no
  frames. This is a scored `production_frq` routed to a real `rc.*` config
  (`gate_grader_routing`). Independent performance is the goal stage of SRSD
  (WWC 2017 six-stage description). (extract P14.)
- **Self-score before the grader reveal (judge, THEN reveal), never
  self-grade-alone, never person-praise.** If a `self_score` slot is used it
  must precede a graded reveal (`gate_calibration_discipline`), and no authored
  body or feedback may contain person-praise ("great job", "nice work" are
  regex-rejected). Feedback is GOAL / NOW / NEXT at the process level. Self-
  assessment against explicit criteria is a strong, stateless writing lever
  (Graham, Hebert and Harris 2015: self-feedback ES about 0.62, near teacher
  0.87 and above automated 0.38;
  https://digitalcommons.unl.edu/specedfacpub/222/), but rubrics alone do not
  calibrate and students overestimate (bias g about 0.206), so feedback is the
  lever. Person-praise (self-level) is the weakest feedback level, ES about 0.09
  to 0.14 (Hattie and Timperley 2007;
  https://journals.sagepub.com/doi/10.3102/003465430298487). (extract P15.)
- **Calibrate synthesis with boundary pairs.** The highest-value calibration
  item is a "two summaries" response placed next to a synthesized one, asking
  what ONE move joins them (a score 2 vs 3 boundary). Calibration is trainable
  (extract P16).

**Stateless delivery:** extended-text production scored once by the external
grader; put the GOAL in the prompt (goal-setting cannot be carried across
stateless items, so it is baked into the item stem). A self-question script the
student runs on the one draft they just wrote collapses self-monitoring to
WITHIN the item (research_async-srsd section 5).

### TRANSFER (novel content, hard bank-partition)

**Moves.**

- **TRANSFER must use a DIFFERENT content bank, which for synthesis means a
  WHOLE new combinable paired set.** `gate_bank_partition` rejects a TRANSFER
  slot whose content bank overlaps any MODEL/SUPPORTED bank, and rejects an
  untagged transfer bank. This bites unusually hard for T8: a component type
  needs one new single source for transfer, but T8 needs an entire second
  engineered-to-combine PAIRED set from a different topic. Route its
  `production_frq` to a valid `rc.*` config (extract P17).
- **Transfer here is near transfer (same synthesis genre, new paired topic).**
  Claim it confidently; do not claim far transfer (KB section 1.5; extract P18).

**Stateless delivery:** a full production item on the new paired set, externally
graded. Coarse expertise-reversal adaptivity at the SEAM between lessons
(grader's score on this item routing the student to a next rung or lesson
variant) is an UNBUILT capability, assumed pending eng, NOT a delivered one.
Ship the transfer item as part of the fixed-fade sequence that stands on its own;
any seam-level routing is contingent on the platform actually supporting
next-lesson routing on a grader score (research_worked-example-fading Claims
6, 7, 9).

---

## 3. The worked-example shape for T8 (the single most important artifact)

The `annotated_before_after` for synthesis is a **minimal pair on exactly one
dimension: the JOIN.** Hold topic, both source facts, and length constant; vary
only whether the two ideas are combined.

- **BEFORE (drops the move):** two adjacent sentences, one reporting Source A,
  one reporting Source B, with no connecting claim and (optionally) a missing
  attribution. Reads as summary + summary.
- **AFTER (explains HOW):** one claim that BOTH source ideas support, each idea
  attributed to its source, plus one explicit sentence stating how the two
  connect. Complementary: "both point the same way." Opposing: "A weighs more
  than B because..."
- **Annotation ON the sentence** (not a separate legend), labeling the
  connecting move and each attribution.

**Concrete grounding.** The two bound gold templates show what "combinable"
means. The MCAS complementary pair (`G10_EXEMPLAR_MCAS_complementary.md`, EPA +
DOE, public domain) is engineered so Article 2 ("How Electric Vehicles Use
Energy") explicitly links back to Article 1's clean-air line ("The efficiency
argument runs alongside the clean-air one"), so a real essay must combine both,
not summarize each. The nuclear opposing pair
(`G10_EXEMPLAR_paired_argument_nuclear.md`) supplies shared theme + divergence +
credibility contrast for the "weigh and pick" variant. `gate_content_depth`
enforces BEFORE + AFTER inline at depth >= 220 chars (extract worked-example
section).

**Do NOT reproduce copyrighted lesson text.** Author the exemplar sentences in
own words. The federal-fact sources above are public domain and shippable; NYT /
ProCon and textbook expression are reference-only.

---

## 4. Worked-example fading without statefulness

Timeback has no per-student memory, so the adaptive within-lesson fade loop is
impossible. It is not needed: the core learning benefit of fading does NOT depend
on real-time adaptivity. The original fading studies used a FIXED pre-scripted
schedule and it beat unfaded practice (Renkl et al. 2002, near-transfer partial
eta-squared .12/.08/.19 across three experiments). Deliver the fade as a designed
SEQUENCE of isolated items, each self-contained at a fixed scaffolding level
(research_worked-example-fading Claim 1).

Rules for T8:

- **Every rung is a COMPLETION item that carries its own context.** A completion
  problem prints the partial solution in the stem, so it is isolation-safe by
  construction. This is the key structural fit between the fading literature and
  Timeback's isolation constraint (van Merrienboer et al. 2002;
  https://www.sciencedirect.com/science/article/pii/S0959475201000202).
- **Fade BACKWARD (blank the LAST move first).** For a synthesis paragraph built
  as [Source A idea + attribution] -> [Source B idea + attribution] ->
  [connecting sentence] -> [claim across both], the first completion item shows
  everything except the connecting sentence and asks the student to generate only
  that join; the next item blanks the join AND Source B's integration; and so on
  toward full production. Backward fading is the only direction that produced a
  significant far-transfer gain and it saved study time (Renkl et al. 2002, Exp
  3, backward-vs-control far transfer partial eta-squared .27). The earlier
  worked moves stay visible in the SAME item as built-in scaffolding, which is
  what lets one isolated item "scaffold" without referencing anything external
  (research_worked-example-fading Claim 2).
- **Annotate with consistent SUBGOAL LABELS across the whole ladder.** Label the
  moves ("Which source says what", "Establish the shared thread", "Voice the
  claim across both", "Explain the join"). Labels are static text: they survive
  display-only rendering and give the stateless sequence a through-line
  (Margulieux and Catrambone 2016, subgoal labels d about .2 to .3, do not decay
  like self-explanation training;
  https://bpb-us-e1.wpmucdn.com/sites.gatech.edu/dist/b/1555/files/2020/09/MargulieuxandCatrambone2016.pdf).
- **Deliver self-explanation as a SCORED principle-naming choice item, not a
  free "explain what you did" prompt.** Ask "Which move is this sentence doing?"
  with distractors, targeting the structural principle. Generic self-explanation
  prompts can HURT (Barbieri et al. 2023, self-explanation a significant negative
  moderator when it just restates the obvious;
  https://danamillercotto.com/uploads/4/7/7/2/47725475/barbieri_et_al__2023__we_meta-analysis.pdf).
- **Seam routing is UNBUILT; ship the fixed fade.** Routing the student to a
  different rung or lesson variant on an external-grader production score (or a
  short first-step diagnostic) is an assumed-pending-eng capability, NOT a
  delivered one; it is contingent on the platform actually supporting next-lesson
  routing on a grader score. The lesson ships as a complete, self-sufficient
  FIXED-FADE sequence requiring zero routing to function. Fixed fading still beats
  no fading; the adaptive increment is the only thing statelessness forfeits, and
  it is deferred, not assumed (research_worked-example-fading Claims 6, 7, 9).

---

## 5. Feedback-as-teaching within the stateless boundary

The precise line: feedback-as-teaching survives when the object being judged is
FIXED and self-contained within a single item (a text we provide, or one fresh
submission scored once). It BREAKS the moment the design needs to carry the
student's own words, judgment, or score from one item to the next
(research_feedback-as-teaching 2.3).

**DELIVERABLE for T8 (build these):**

1. Grader feedback on a PROVIDED text (an anchor synthesis essay we author),
   scored against the rubric and returned as elaborated, process-level feedback.
   A single evaluation of a fixed input, so statelessness is a non-issue.
2. Predict-the-fix then reveal, inside ONE item (the join-diagnosis item in
   MODEL). Show the side-by-side BEFORE, ask which move joins the sources, then
   the same item reveals the fix and WHY. Elaborated feedback beats bare
   verification (Shute 2008;
   https://andymatuschak.org/files/papers/Shute%20-%202008%20-%20Focus%20on%20Formative%20Feedback.pdf).
3. Erroneous-example and correct-vs-incorrect comparison items: a
   "two-summaries" model next to a woven one, student picks the stronger and says
   why. Fully stateless (both texts provided). Highlight the weak span for
   lower-knowledge students (Booth et al. 2015;
   https://files.eric.ed.gov/fulltext/ED566953.pdf).
4. Self-assessment against a rubric or self-question SCRIPT applied to the
   student's ONE fresh submission (the boundary-pair calibration item).
5. Elaborated answer reveals that NAME the process move (the join, the
   attribution) and give a reusable self-check, not just "correct/incorrect"
   (Hattie and Timperley 2007, process and self-regulation levels beat task-only
   and self-level).

**BLOCKED by statelessness (do not design around these):**

1. Feedback on the student's EVOLVING synthesis draft across turns. No item can
   show item B the student's response to item A; a retake starts blank. The
   coaching loop "draft -> feedback -> revise the SAME draft -> feedback again"
   cannot be reproduced turn to turn.
2. Iterative revise-and-recheck on the student's own two-source essay. We can
   flag errors on a PROVIDED essay (indirect feedback) but cannot watch the
   student revise their live draft across items.
3. Feedback that references the student's earlier answer or score ("last time
   you...", "compared to your draft in step 2..."). `gate_no_prior_work_reference`
   rejects "revise your paragraph", "the essay you wrote", "from step N", etc.
4. Adaptive fading tuned to this student's running performance (ship FIXED fading
   only; seam-level routing is UNBUILT / assumed pending eng, not a fallback we
   can rely on, section 4).
5. Cross-session goal-setting and longitudinal progress monitoring. Bake the goal
   into the prompt; collapse self-monitoring to a within-item self-check.

The re-engineered form is not a weak substitute: self-assessment against criteria
(about 0.62) and errorful-generation-plus-reveal are strong, evidence-based
mechanisms in their own right (research_feedback-as-teaching 2.3).

---

## 6. Function-over-form device instruction (where it applies here)

T8 is a synthesis archetype, not a sentence-craft archetype, so device
instruction is NOT re-taught here: the sentence-level TWR moves enter T8 ALREADY
FADED from T2/T3/T4 (the shared fade ledger, extract P12). T8 only REFERENCES
them where cross-source evidence is fused into ONE sentence and where each idea
is attributed. Gate, do not re-teach: AlphaWrite owns sentence-combining craft
G3-8; EGUMPP owns conventions G3-10; T8 draws on them as retrieval-gated
prerequisites and cues only their rhetorical USE.

- **Reference the already-faded move by the JOB it does; do NOT re-teach or
  label it.** Isolated grammar (identify/define the appositive) has a null-to-
  negative effect on writing quality (Graham and Perin 2007, traditional grammar
  small significant NEGATIVE effect; Andrews et al. 2006; Hillocks 1986).
  Sentence-combining, which is the actual fusion mechanism, has a moderate
  positive effect (ES 0.50, Writing Next). Teaching by function plus application
  beats teaching by definition (Fearn and Farnan 2005;
  https://files.eric.ed.gov/fulltext/EJ787964.pdf), but at T8 that teaching has
  already happened, so the entry cues application only.
  (research_function-over-form headline answer.)
- **For T8, the function anchors the student already owns and now applies are:**
  because/but/so hinge = give the reason/contrast/consequence that links the two
  sources (the strongly attested TWR mapping); appositive = attribute AUTHORITY,
  name and credential the source so the reader knows WHOSE idea it is ("According
  to the EPA, ..." / "the U.S. Department of Energy, the federal agency that
  tracks energy use, reports..."); prepositional phrase = add CONTEXT / narrow
  scope on where or when a source's finding holds; relative clause = introduce a
  CONSEQUENCE that ties one source's point to the other. A discrimination item
  asks "Which revision makes clear that this idea comes from Source B AND connects
  it to Source A's point?" with distractors that are the right grammatical form
  doing the wrong job (Fearn-and-Farnan pattern).
- **Bake the "why this creates this effect" talk INTO the worked example and the
  answer rationales.** Myhill's contextualised-grammar gains were small (about
  0.21), skewed to abler writers, and MEDIATED by a knowledgeable teacher's
  discussion (Myhill et al. 2012; Jones, Myhill and Bailey 2013). We have no
  teacher, so that mediating talk must live in the material or the effect
  evaporates; over-scaffold the function for weaker writers
  (research_function-over-form synthesis + design implication, verified as a
  sound design inference). Flag the appositive = authority / hinge = reasoning
  map as a DESIGN CHOICE imposed for clarity, not a finding lifted from a study.

---

## 7. The gates that bite HARDEST for T8 (ranked, with how to satisfy)

1. **`define_before_use` (signature gate for T8).** The archetype's own name,
   "synthesis/synthesize", is a `_TECH_TERMS` entry, so the lesson self-rejects
   unless a TEACH slot defines it with a definitional cue before any use. Also
   catches "counterclaim" (opposing variant), "attributive tag", "appositive",
   "warrant" if used. FIX: a plain-words definition slot up front (section 2
   TEACH; P1, P4).

2. **`bank_partition` (2x stimulus cost).** Transfer needs an entire second
   engineered-to-combine PAIRED set from a different bank, not one new single
   source. Easy to accidentally reuse the taught topic and get rejected. FIX:
   author/allocate a distinct combinable paired set and tag its `bank` (P17).

3. **`binding_integrity` + combinability.** T8 must bind two or more real paired
   stimuli that actually combine (shared theme + a genuine connection point). A
   ref not in the banks, or a pair that does not truly combine, fails here or
   produces an unteachable worked example. FIX: bind verified paired sets like
   the MCAS and nuclear exemplars (section 3).

4. **`no_ambiguous_reference`.** Two sources multiply "which one?" ambiguity;
   deictic phrases ("the summary", "this version") without an inline referent are
   rejected. FIX: name Source A / Source B distinctly and quote/bind referents
   (P9).

5. **`no_source_markup`.** The "which source says what" mapping tempts
   underline/circle/highlight imperatives on display-only stimuli. FIX: "read and
   note" framing, or a hottext/choice mapping item (P5).

6. **`content_depth` on `annotated_before_after`.** Must show BOTH the
   summary+summary BEFORE and the woven AFTER inline, with both source ideas in
   each, above the 220-char floor. FIX: write the full minimal-pair worked
   example (section 3, P6).

7. **`model_sequence` + `model_before_required`.** Needs annotated before/after +
   predict-the-fix (with reveal) + a scaffolded diagnosis_frq. FIX: P6 to P8.

8. **`unit_ladder` / `type_ceiling`.** T8 is permitted to reach "essay" (only
   T7/T8 are), but units must climb non-decreasingly and every scored production
   must declare a unit. FIX: declare units, keep them monotonic (P13).

9. **`effect_size_honesty` + `mnemonic_status`.** WEAVE is a "proposal" (must be
   declared in provenance as `mnemonic_status="proposal"`), and no slot may claim
   SRSD's live ES 1.14/1.02 or that the async model "inherits" SRSD's evidence.
   FIX: declare the status; cite modality-flexible mechanisms only (extract gate
   ledger 9).

10. **`grader_routing`, `calibration_discipline`, `no_prior_work_reference`,
    `no_em_dash`, `timeback_native`.** Standard shell gates: route production to a
    valid `rc.*` config (rc.mcas / rc.ohio / rc.ap); self-score precedes reveal
    and no person-praise; never reference the student's own prior work (retake is
    blank); no em/en dashes; all slot kinds map to native Timeback interactions.

**T8-specific anti-patterns (evidence-backed "don't"):** summary+summary
masquerading as synthesis; introducing the second source before single-source
integration is fluent; a blank "now synthesize these two sources" with no worked
join and no scaffold (rejected by `gate_model_before_required`; write-about-text
fails low achievers without explicit instruction); marking up the source;
claiming SRSD's ES for the async model; voicelessness convergence (keep at least
one student-choice point: topic/source/stance) (extract anti-pattern section).

---

## Retrieval + item rules (LS feedback 2026-07)

These encode the 2026-07 learning-scientist pass as T8 authoring defaults so a fresh synthesis lesson clears the new gates by construction.

- **Cadence ceiling: FULL-ESSAY-BUILD tier, ceiling 4, checks at production milestones only** (`gate_check_cadence`). T8 reaches the essay unit, so checks land at production milestones (the discrimination before the first FRQ, the predict-the-fix, the diagnosis), not after every card. A run of COUNTED teach cards (teach card, the two paired stimulus_display slots, the annotated before/after) may not exceed FOUR before a check. The summary+summary -> woven before/after counts as ONE worked example; never split it to pad the run. Tag any pure buy-in / orientation card `tag="buy_in"` so it counts 0. The "memorizable tool" tightening is LESS relevant here: T8 CUES the already-faded sentence moves rather than introducing new named tools, so it rarely triggers; if a card genuinely introduces a new memorizable device (WEAVE itself), tag it `tag="memorizable_tool"`.
- **Four options per discrimination, each a NAMED MISCONCEPTION** (`gate_structural_item`). The synthesis-vs-summary+summary contrast and the attributed-vs-source-confused pair each carry exactly four choices; distractors are real synthesis failures (two summaries in sequence with no join, a claim across both with no attribution, one source's idea credited to the other), never filler.
- **Diagnosis: the student ANSWERS the check, then improves** (`gate_self_answered_check`). The modeled diagnosis may pre-answer a PROVIDED side-by-side specimen (name it: "two ideas reported side by side, no connecting claim"), but MUST then hand the student an independent turn: name what was missing, add it, and say why the woven version is stronger on a fresh pair. Never print a diagnosis that answers its own questions and stops.
- **No comma before "because"/"so" in a fill-in frame** (`gate_frame_comma`). Any side/reason fill-in (the opposing "A weighs more than B because ______" frame) drops the comma before because. Emit it with `claim_frame()` from `lesson_prompts` rather than hand-writing it.
- **Re-gloss the hard terms.** "Synthesis/synthesize" is T8's signature `_TECH_TERMS` entry and counterclaim enters in the opposing variant, so `gate_define_before_use` already forces an in-lesson gloss (also controlling idea, warrant). On a later-lesson re-introduction prefer a BRACKETED gloss right after the term (LS #9 style), for example "synthesis [combining both sources into one argument]."
- **Stem wording (playbook-only, #7):** name the move directly ("Which sentence states how the two sources connect?"), never a meta-phrasing.
- **Tone (playbook-only, #5 / Yeager):** state the standard up front; each per-choice reveal is process-level wise-feedback that names the MOVE (the join, the attribution), no person-praise, no compliment-sandwich (reinforces `gate_calibration_discipline`).
- **Pair a stand-alone improve-write with a `predict_the_fix`** where feasible (playbook-only, #4); T8's join-diagnosis predict-the-fix pairs with the connecting-sentence completion item.
- **Cross-lesson spacing (KH caveat, #3):** the in-lesson cadence gate is necessary but NOT sufficient; the join move (and the shared because/but/so fusion) must recur across sessions with delayed, multi-round retrieval (spacing g about 0.74, section 8). That durability is a sequence-builder concern, not visible to this lesson's gates.

---

## 8. Keep it short (CLT budget on a high-load type)

T8 has the highest intrinsic load of the eight types, so every bit of extraneous
load removed is capacity for the actual join. Load is additive (KB section 1.1).
Concretely:

- Keep the two sources at the Lexile gate (about 1050 to 1185L reading-load cap)
  and short (the gold exemplars run about 440 words each).
- One interaction type per step (response-signal standardization).
- ONE named strategy (WEAVE). Do not stack a second synthesis mnemonic on top.
- Teach the join by CONTRAST (the before/after minimal pair) rather than by long
  prose.
- Space and retrieve the join across sessions; do not teach it once. Schedule
  WEAVE (and the shared because/but/so fusion) to reappear, and use delayed,
  multi-round retrieval for transfer, not a single immediate quiz (spacing
  g about 0.74; extract P19, P20).

Short, worked-example-first, discrimination-before-production: that is the whole
lesson.

---

## Open risks and honest flags

- **WEAVE is a proposal mnemonic, NOT sourced.** It must be declared
  `mnemonic_status="proposal"` and never presented as validated
  (`gate_mnemonic_status`; extract, LESSON_TYPES[8]).
- **discrimination-before-production is UNVALIDATED** (Grade-C design bet): keep
  it, label it in the body, A/B test it (KB 02 section 4; P10).
- **Blocked by Timeback:** live coaching on the student's evolving synthesis
  draft; cross-item revise-and-recheck; adaptive within-lesson fading; cross-
  session goals and longitudinal progress monitoring; any reference to the
  student's prior work. These are reconstructed (annotated before/after worked
  example, completion-item fixed fade, goal-in-prompt, within-item self-check) or
  dropped, per sections 2, 4, 5. Seam-level score-based routing is NOT a
  reconstruction we rely on: it is UNBUILT / assumed pending eng, and the lesson
  ships as a self-sufficient fixed-fade sequence requiring zero routing.
- **Lexile is CONDITIONAL** on both exemplar sets: run the pipeline Lexile tool
  before ship (both gold templates are marked CONDITIONAL).
- **Function-over-form map (appositive = authority, hinge = reasoning) is a
  DESIGN CHOICE**, not a finding; flag it under the provenance rule. The
  teacher-mediated "why this creates this effect" talk must be baked into the
  material, since the product has no teacher (research_function-over-form).
- **Async MODEL does not inherit SRSD's live ES**; the async adaptation is an
  annotated before/after worked example with labeled error annotation plus
  predict-the-fix, NOT a coping model reconstructed as fixed media, and it may
  not claim SRSD's live coping-model effect size. Cite only modality-flexible
  mechanisms (worked examples, predict-then-reveal, self-assessment scripts)
  (`gate_effect_size_honesty`; research_async-srsd).
