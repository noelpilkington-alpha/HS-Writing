# Authoring Playbook: Archetype T3 Evidence-Integration (PROVE)

> Author-facing playbook for building T3 lessons on the Timeback delivery surface.
> Every move below is grounded in either the internal extraction
> (`_phase2/extract_T3_PROVE.md`, which itself anchors to `pipeline/lesson_contract.py`,
> `G10_Model_Lesson_Specs.md`, and the ID Knowledge Base) or a verified web-research
> claim (`_phase2/research_*.md`, adversarial-verification pass 2026-07-10). External
> sources are cited by author/title/year/URL. All prose is own words; no copyrighted
> lesson text is reproduced. No em dashes (house rule; gate `no_em_dash`).

---

## 0. What this archetype teaches (one line)

Integrate a source quote so no bare quote stands alone: attribution (an appositive
attributive tag naming who said it) PLUS a because/but/so hinge that ties the fact to
the claim, delivered inside the frame-the-quotation pattern (introduce / cite /
explain). Source: extract P (identity) and the contract demo `target`
(`lesson_contract.py` loc ~534): "Integrate a source quote with attribution + a
because/but/so hinge tied to the claim."

---

## 1. Terminal deliverable and production ceiling

- **Terminal deliverable:** one claim developed with an integrated source quote: a
  named source (appositive/attributive tag) plus a because/but/so hinge that states
  why the quote supports the claim. Trait scored = Evidence / Development.
  Source: extract §1; `G10_Model_Lesson_Specs.md` Type 3 Target and Trait.
- **Production ceiling = PARAGRAPH.** `TYPE_CEILING_UNIT[3] = "paragraph"`
  (`lesson_contract.py` loc ~416). T3 is a COMPONENT type, not a composite-essay
  type. The unit ladder climbs sentence then paragraph and STOPS: a full essay
  belongs to T7/T8. Source: extract §1 (P: ceiling), P14; contract
  `gate_type_ceiling` (loc ~447), `gate_unit_ladder` (loc ~421).
- **Load class: HIGH.** The council ranks evidence-integration just below analysis in
  intrinsic load, above claim/rubric/source-reading/editing. So T3 gets DEEP
  scaffolding, and when in doubt keep a scaffold one rung longer (humanities
  under-support asymmetry). Source: extract §1 (load class); KB `00` §1.1/§1.2;
  Toolkit Rule 3.
- **Evidence-honesty posture:** the legacy spec labels T3 "SRSD flagship, ES 1.14."
  For our async, AI-graded, read-alone delivery we may NOT claim that live-enacted
  effect size. T3's moves are evidence-INFORMED, citing modality-flexible ingredients
  (worked example, forced response, retrieval, personalized process feedback), never
  "inherits SRSD's evidence." We likewise do NOT claim the coping-model /
  social-modeling effect size: that mechanism depends on live or video human modeling (a
  peer visibly struggling and self-talking) and does not transfer to fixed screen text,
  so the async MODEL rests on the screen-validated worked-example effect instead, not on
  a simulated coping persona. Source: extract §1 (honesty flag); modality correction;
  gate `effect_size_honesty`. The Writing Next number itself (SRSD variant averaged
  1.14 vs 0.62 for non-SRSD strategy studies) is real and verified (Graham & Perin,
  2007, Writing Next, https://www.thewritingrevolution.org/wp-content/uploads/2017/05/WritingNext.pdf,
  research_async-srsd claim 4 CONFIRMED); it just cannot be attributed to OUR
  screen-only build.

---

## 2. Per-SRSD-stage authoring (moves, worked-example shape, async delivery)

The shell is fixed and ordered (gate `shell_completeness`): Teach, Model, Supported,
Independent, Transfer. Content swaps; the frame does not (extract §2; Model Specs
"the constant shell").

### TEACH (Develop Background Knowledge + Discuss It)

**Moves.**
- Define the three gated terms in plain words BEFORE any use: `attributive tag`,
  `appositive`, `because/but/so hinge`. All three sit in the contract `_TECH_TERMS`
  list, so gate `define_before_use` REJECTS any student-facing use without a
  plain-words definition first. T3 owns more gated jargon than any other type, so
  this gate bites hardest here. Source: extract P1, §5 rank 2; contract `_TECH_TERMS`
  (loc ~310-324), `gate_define_before_use` (loc ~338-354); Engelmann faultless
  communication; KB Rule 1.
- State PROVE as the ONE named strategy (Point, Reference, Observe, Verify, Extend)
  plus the test-demand consequence: a bare quote with no hinge caps the Evidence
  score because the reader never sees why the quote supports the point. Source:
  extract P2; contract demo teach_card (loc ~539-544); Toolkit Rule 1; KB `00` §2.5
  "Memorize It."
- Give a specific, checkable product goal, not "do your best": sentence rung =
  "attribute the fact AND tie it to a claim with a because/but/so hinge"; paragraph
  rung = "one claim developed with an integrated source quote (named source + hinge)."
  Product goals are a verified strategy ingredient (Writing Next: Specific Product
  Goals ES 0.70, CONFIRMED, research_async-srsd claim 4). Source: extract P3; Toolkit
  Rule 4.
- Present the source as READ-AND-NOTE, never mark-it-up. T3 pulls a quote from a
  passage, but Timeback stimuli are display-only XHTML with JS stripped, so the
  student cannot highlight, underline, or circle. Author "read the source and note
  where the strongest fact sits," never "underline the quote you will use." Source:
  extract P4; gate `no_source_markup` (loc ~278-290).

**Worked-example shape / delivery.** A short `teach_card` (>= 200 chars, gate
`content_depth`) plus a `stimulus_display` slot that renders the source passage
read-only. The "discuss it" of SRSD becomes expository micro-teaching plus the
downstream discrimination item, not a live conversation. Source: research_async-srsd
§2 (Discuss it survives only if reconverted from dialogue to media + choice items).

**Timeback flag.** The live teacher discussion and in-the-moment differentiation of
SRSD's TEACH/Discuss stage cannot be delivered; it is reconstructed as fixed media +
choice. Source: research_async-srsd §1-2 (three of six SRSD success characteristics
are human-dependent and cannot be delivered by a stateless screen).

### MODEL (annotated before/after worked example + Memorize It)

**Moves.** SRSD's live coping-model think-aloud is the most human-feeling move, but it
cannot be delivered async: the coping-model / social-modeling mechanism (Schunk, Hanson
& Cox, 1987, Peer-model attributes and children's achievement behaviors, JEP 79(1),
54-61, https://files.eric.ed.gov/fulltext/ED278499.pdf, research_async-srsd claim 8)
depends on a LIVE or video human peer visibly struggling and voicing self-talk, and that
self-efficacy effect does not transfer to static screen text. A near-peer persona,
fake-student inner monologue, or "visible false start + self-talk" beat is therefore
REMOVED. What DOES transfer, and is screen-validated, is the WORKED-EXAMPLE effect
(including erroneous / annotated examples). So the MODEL is built from four stateless
mechanisms anchored on an annotated worked example (extract P5; Model Specs MODALITY
CORRECTION; Principle A; gate `model_sequence` requires `annotated_before_after` +
`predict_the_fix` in MODEL and a `diagnosis_frq` somewhere):

1. **Annotated before/after worked example (rung 0 of the fade).** Show a weak BEFORE and
   a strong AFTER inline, with the common error and its fix carried as LABELED
   author-voice ANNOTATIONS ON the exemplar sentence, not as any persona's inner
   monologue. BEFORE drops the move ("The author says reefs are dying. This proves my
   point."); AFTER names the source in an appositive and adds a because-hinge tying the
   fact to the claim; the annotations read as author-voice labels ("problem: quote
   dropped in with no attribution" / "fix: name the source in an appositive" / "fix: add
   the because-hinge that ties the fact to the claim"). Gate `content_depth` requires
   the literal words BEFORE and AFTER inside the slot (>= 220 chars); the
   split-attention rule forbids a separate legend. Source: extract P6; contract demo
   (loc ~547-551); KB `00` §1.1 worked-example + split-attention; Booth et al. (2015),
   Simple Practice Doesn't Always Make Perfect,
   https://files.eric.ed.gov/fulltext/ED566953.pdf (worked examples free working
   memory; erroneous/annotated examples teach), research_feedback claim 5 CONFIRMED.
2. **Predict-the-fix (diagnose BEFORE the reveal).** Show a dropped quote (no name, no
   tie); ask which single move fixes it (add attribution + because-hinge) versus a
   decoy (make it longer); the reveal names the fix as the R and V of PROVE and
   carries a non-empty `feedback` block. This is the errorful-generation /
   hypercorrection mechanism: committing to a prediction before the reveal is the
   mechanism, not wasted motion, and the reveal must explain the reasoning, not flash
   the answer (Metcalfe, 2017, Learning from Errors, Annu. Rev. Psychol. 68, 465-489,
   https://www.columbia.edu/cu/psychology/metcalfe/PDFs/Learning%20from%20errorsAnnual%20ReviewMetcalfe2016.pdf,
   research_feedback claim 6 CONFIRMED; elaborated > verification feedback, Shute,
   2008, Focus on Formative Feedback, RER 78(1), 153-189,
   https://andymatuschak.org/files/papers/Shute%20-%202008%20-%20Focus%20on%20Formative%20Feedback.pdf,
   research_feedback claim 2 CONFIRMED). Source: extract P7; contract demo
   (loc ~552-559).
3. **Personalized AI revise-feedback on the student's OWN submission (Option-E /
   upgrade-only).** This is the async substitute for SRSD's in-the-moment conferencing.
   It is NOT stock Timeback; ship it only as an upgrade. Keep it strictly a ONE-SHOT
   grader eval of a SINGLE fresh submission (one paragraph scored once, returning 1-3
   feedback cards), never an iterative revise-the-same-draft-and-recheck loop. No
   required slot depends on it: the lesson passes every gate with this engine absent.
   Source: extract §3 item 6; Model Specs finalized structure; Principle vet-minor.
4. **Student-generated diagnosis (`diagnosis_frq`).** See SUPPORTED below; it must be
   scaffolded, never a blank "diagnose it."

The MODEL example must be a true MINIMAL PAIR (faultless slot): same quote, integrated
vs bare, differing ONLY on framing; the appositive slot is referent-guaranteed (the
author's name is available in the source). Source: extract P8; Model Specs Type 3
faultless-slot + build rule 2 (DI faultless communication, machine-checkable).

**Memorize It.** The PROVE mnemonic plus retrieval-practice choice items (match the
letter to its move, pick the step that comes next). Necessary but low-value alone; the
mnemonic reduces load so the writer can engage the process, it does not create good
writing, so always pair it with application. Source: research_async-srsd §2 (Memorize
it survives as mnemonic + retrieval choice items; Harris 2024).

**Timeback flag.** The live coping think-aloud (near-peer voice, visible false start +
coping self-talk + repair) is NOT reconstructed as fixed media; a screen cannot carry
the social-modeling mechanism, so it is dropped (Principle A). What ships instead is the
annotated before/after worked example with author-voice error labels plus predict-the-fix.
The model-comparison "which draft is stronger and why" work is offloaded to the
discrimination item so the learner does the evaluating. IES Rec 1 (modeling with
identified errors, Strong evidence) is satisfied by the annotated exemplar, not by a
persona. Source: research_async-srsd §3 (Braaksma observational learning; IES Rec 1).

### SUPPORTED (Support It: worked example, then completion, then fade)

**Moves.**
- **Discriminate integrated vs dropped BEFORE producing, and LABEL it a Grade-C design
  bet.** A `discrimination` slot must precede any production, and at least one must set
  `labeled_grade_c=True`. The core T3 contrast is bare quote-drop vs integrated (and
  quote-that-fits-claim vs does-not). Discrimination-before-production is UNVALIDATED
  for writing, so it is kept, labeled, and A/B-flagged, never sold as evidence.
  Source: extract P9; gate `discrimination_before_production` (loc ~172-183); KB `02`
  §4; contract demo (loc ~560-565). Correct-vs-incorrect comparison on PROVIDED text
  is fully stateless and teaches the target discrimination (Booth et al., 2015,
  research_feedback claim 5 CONFIRMED; WWC exemplar-contrast Example 2.7, Graham et al.
  2016, Teaching Secondary Students to Write Effectively, WWC 2017-4002,
  https://ies.ed.gov/ncee/wwc/PracticeGuide/22, research_feedback claim 8 CONFIRMED).
- **Give the sentence-rung production FIRST, sized "sentence."** One integrated PROVE
  sentence on the source (attribute + hinge). Sentence-first is the settled
  developmental axis (TWR) and the low rung of the ladder. Source: extract P11;
  contract demo Supported `production_frq` `unit="sentence"` (loc ~566-569).
- **Scaffold the self-diagnosis; do not ask for a blank "diagnose it."** The
  `diagnosis_frq` must supply a frame, checklist, or named steps: "The weak version
  lacked ___; I added ___; it is stronger because ___." Gate `model_before_required`
  rejects an unscaffolded diagnosis and requires a prior MODEL of how to diagnose.
  This is a self-assessment SCRIPT, which raises observed self-regulation more than a
  bare rubric (Panadero, Alonso-Tapia & Huertas, 2012, Learning and Individual
  Differences 22(6), 806-813, https://doi.org/10.1016/j.lindif.2012.04.007,
  research_feedback claim 7 / research_async-srsd claim 12 CONFIRMED, with the caveat
  that the script advantage held on the online self-regulation measure). Source:
  extract P12; gate `model_before_required` (loc ~374-391); contract demo
  (loc ~570-575).

**Worked-example shape / delivery: the fade ladder.** Fully integrated exemplar
(rung 0, in MODEL), then a completion item (student supplies the blanked frame-slots:
the appositive, then the because/but/so hinge), then independent. See §4 for the
stateless fade mechanics. The fade CRITERION is scripted and machine-checkable, but
its TIMING is performance-triggered, never lesson-number. A shared `fade_ledger_moves`
carries because/but/so and the attributive tag across types, so a mastered move does
not re-scaffold. Source: extract P10; Model Specs Type 3 fade ladder + Conflict B
ruling; Toolkit Rule 3 + KB `02` §3 (fade on data, not schedule); contract demo
`fade_ledger_moves=["because/but/so", "attributive-tag"]` (loc ~537).

**Timeback flag.** SRSD's collaborative guided practice and live conferencing are
reconstructed as a decreasing-support item sequence plus the external grader as the
feedback engine; there is no peer, no teacher, no back-and-forth. Source:
research_async-srsd §4; research_worked-example-fading synthesis.

### INDEPENDENT (Independent Performance on a fresh item)

**Moves.**
- Independent production is the full PROVE PARAGRAPH, sized "paragraph": a claim
  developed with an integrated source quote (named source + because/but/so hinge),
  scaffolds gone. This is the payoff stage; strategy research shows the strongest
  results appear once scaffolding is withdrawn and students write independently.
  Source: extract P13; contract demo Independent `production_frq` `unit="paragraph"`
  (loc ~576-579); KB `00` §2.5. (Note: the sharper "results peak at stages 5-6" phrasing
  was REJECTED in verification as an unverifiable attribution; state only the
  supported "independent performance is the goal stage," research_async-srsd claim 3
  REJECTED.)
- Do NOT exceed the paragraph ceiling and do NOT drop back down. Gate `type_ceiling`
  rejects any scored production above "paragraph" for type 3; gate `unit_ladder`
  rejects a later slot smaller than an earlier one. Source: extract P14; contract
  `TYPE_CEILING_UNIT[3]="paragraph"`, `gate_type_ceiling` (loc ~447), `gate_unit_ladder`
  (loc ~421).
- Never reference the student's own prior work. QTI is stateless and isolated; a
  retake starts blank, so the student cannot see or revise an earlier submission.
  Author each production slot self-contained: never "revise your dropped quote from
  above" or "look back at your sentence." T3 hits this wall hardest because "revise
  the bare quote you wrote" is the instinctive revision framing. Source: extract P15;
  gate `no_prior_work_reference` (loc ~292-303).

**Worked-example shape / delivery.** An `extended-text` production item routed to an
`rc.*` rubric config. The external grader plays the "conferencing" role (Roscoe &
McNamara, 2013, Writing Pal feasibility, JEP,
https://link.springer.com/chapter/10.1007/978-3-642-39112-5_27, research_feedback
claim 10 CONFIRMED; automated feedback g approx 0.55, Fleckenstein et al. 2023,
Frontiers in AI, https://www.frontiersin.org/articles/10.3389/frai.2023.1162454/full,
research_feedback claim 9 CONFIRMED). Put the GOAL inside the prompt, since a
cross-session goal cannot be stored. Source: research_async-srsd §5d.

### TRANSFER (novel bank, DI hard partition)

**Moves.**
- Transfer to a DIFFERENT content bank, same PROVE move, so transfer is genuine rather
  than recall of the taught material. Gate `bank_partition` enforces that the TRANSFER
  bank differs from every MODEL/SUPPORTED bank. Claim only NEAR transfer (same move,
  new source); do not overclaim far transfer. Source: extract P16; gate `bank_partition`
  (loc ~200-213); contract demo Transfer `bank="nuclear_power"` vs taught
  `coral_reefs` (loc ~580); KB `00` §1.5.
- Route each scored production to a valid rubric config the deployed grader implements.
  TRANSFER may use a SECOND test's config (e.g. `rc.ohio`) to reinforce format-agnostic
  transfer. Feedback must be process-level GOAL/NOW/NEXT, no person-praise. Source:
  extract P17; gate `grader_routing` (loc ~232-240); contract demo Transfer
  `rubric_ref="rc.ohio"` (loc ~584); Toolkit D1 / Rule 7.

**Worked-example shape / delivery.** A fresh `extended-text` production on a
bank-partitioned source, externally graded. Its score COULD route the next lesson, but
that between-lesson routing is UNBUILT / assumed-pending-eng, not delivered (see §4); the
lesson ships as a self-sufficient fixed-fade sequence requiring zero routing.

---

## 3. Feedback-as-teaching HERE (deliverable vs blocked)

The precise line: feedback-as-teaching survives when the object being judged is fixed
and self-contained within a single item (a text we provide, or one fresh submission
scored once). It breaks the moment the design needs to carry the student's own words,
judgment, or score across items. Source: research_feedback §2.3.

**Deliverable for T3:**
- Grader feedback on the student's ONE fresh PROVE sentence/paragraph, scored once
  against an `rc.*` rubric that targets the deep feature (is the source named AND is
  the hinge tying the fact to the claim), returning elaborated process-level feedback,
  not a bare score. Source: research_feedback §2.1 item 1, §1.1 (Hattie & Timperley,
  2007, The Power of Feedback, RER 77(1), 81-112,
  https://journals.sagepub.com/doi/10.3102/003465430298487, claim 1 CONFIRMED: process
  and self-regulation feedback teach; self/person praise is weakest, approx 0.09-0.14).
- Predict-the-fix then reveal, inside ONE item (the MODEL mechanism 2). Show a dropped
  quote, ask which fix (attribution + hinge), reveal the fix and the WHY. Source:
  research_feedback §2.1 item 2 (Metcalfe 1.6; Shute 1.2).
- Erroneous-example autopsy and integrated-vs-dropped comparison on PROVIDED text (the
  SUPPORTED discrimination). Highlight the weak span for lower-knowledge students so
  they do not have to locate the error first. Source: research_feedback §2.1 item 3,
  §1.5 (Booth et al. 2015; Grosse & Renkl).
- Self-assessment SCRIPT applied to the student's ONE submission (the `diagnosis_frq`
  frame). Self-assessment against explicit criteria is a large writing effect (approx
  0.62, near teacher feedback and above automated) and is stateless because the student
  scores a text present in the item. Source: research_feedback §1.3 (Graham, Hebert &
  Harris, 2015, Formative Assessment and Writing, Elementary School Journal 115(4),
  https://digitalcommons.unl.edu/specedfacpub/222/, claim 3 CONFIRMED), §1.7.

**Blocked by statelessness (do not design around these):**
- Feedback on the student's EVOLVING draft across turns (draft, feedback, revise the
  same draft, feedback again). The coaching "self-fix 80-90 percent when prompted" loop
  depends on a coach seeing the student's current draft turn to turn; not deliverable.
  Source: research_feedback §2.2 item 1.
- Iterative revise-and-recheck on the student's own text across items; we can flag
  errors on a PROVIDED pair (indirect feedback) but not on the student's live draft and
  then watch the revision across items. Source: research_feedback §2.2 item 2 (Lim &
  Renandya, 2020, TESL-EJ 24(3), https://files.eric.ed.gov/fulltext/EJ1275821.pdf).
- Any feedback referencing an earlier answer or score ("last time you dropped the
  quote..."). No item can read prior-item state. Source: research_feedback §2.2 item 3;
  gate `no_prior_work_reference`.
- Growth/progress feedback over time; needs longitudinal state and is the
  weakest-evidence practice anyway (WWC Rec 3, Minimal). Source: research_feedback §2.2
  item 6.

**T3-specific re-engineering:** the coaching win moves from "iterate on your dropped
quote" into "predict/judge the fix on a provided dropped-quote pair, then reveal" plus
"self-assess your one PROVE submission against the script." Both are strong,
evidence-based mechanisms in their own right, not weak substitutes. Source:
research_feedback §2.3.

---

## 4. Worked-example fading without statefulness

The core learning benefit of fading does NOT depend on real-time adaptivity. The
foundational fading studies used a FIXED, pre-scripted schedule sequenced across items,
and it beat example-problem pairs on near transfer (Renkl, Atkinson, Maier & Staley,
2002, From Example Study to Problem Solving, J. Exp. Education 70(4),
https://www.davidlewisphd.com/courses/EDD8121/readings/2002-Renkl_et_al.pdf,
research_worked-example-fading claim 1 CONFIRMED). So the fade is a SEQUENCE property,
authored as an ordered set of isolated items at fixed scaffolding levels, and drops
straight into stateless QTI.

**The T3 fade ladder (each rung a self-contained item):**
1. Rung 0 (MODEL): fully integrated PROVE exemplar with the annotated before/after and
   subgoal labels (Point / Reference / Observe / Verify).
2. Completion item, faded BACKWARD: print a PROVE sentence with the source quote and
   the appositive already supplied, blank ONLY the because/but/so hinge (the last
   move). The next rung down blanks the appositive + hinge. Backward fading (blank the
   last step first, keep earlier worked steps visible as contextual scaffolding on the
   SAME item) is the direction that produced the significant far-transfer gain and saved
   study time (Renkl et al. 2002 Exp 3, backward vs control far-transfer partial
   eta-squared = .27; forward non-significant; research_worked-example-fading claim 2
   CONFIRMED). The completion problem is the ideal stateless unit because ALL context
   the learner needs is printed in the stem, not carried from a prior item (van
   Merrienboer et al. 2002, Learning and Instruction 12(1),
   https://www.sciencedirect.com/science/article/pii/S0959475201000202, claim 3
   CONFIRMED).
3. Independent production (full paragraph), externally graded (the ceiling).

**Deliver the completion rung as a stateless choice/short item:** e.g. show the
sentence with the hinge blanked and ask which continuation ties the quote to the claim,
with distractors that are the right grammatical form doing the wrong job. Principle-
naming self-explanation should be a SCORED discrimination item ("which rhetorical move
is this step doing / why does it work"), NOT a free "explain what you did" prompt.
Pairing a fade with principle-naming prompts helped near and far transfer (Atkinson,
Renkl & Merrill, 2003, JEP 95(4), https://eric.ed.gov/?id=EJ678596, claim 4 CONFIRMED),
but generic "explain yourself" prompts NEGATIVELY moderated the worked-example effect in
a 55-study meta-analysis (Barbieri et al. 2023,
https://danamillercotto.com/uploads/4/7/7/2/47725475/barbieri_et_al__2023__we_meta-analysis.pdf,
claim 5 CONFIRMED): prompt for the structural principle, not the obvious.

**Subgoal labels are the through-line.** Tag the exemplar's clusters with the same
functional labels across the whole ladder (name the source / state the fact / tie it to
the claim). Labels chunk steps and consistently cue the right self-explanation, they are
static text that survives display-only rendering with no interactivity or state, and
externally-prompted self-explanation via labels does not decay the way self-explanation
training does (Margulieux & Catrambone, 2016, Learning and Instruction 42,
https://bpb-us-e1.wpmucdn.com/sites.gatech.edu/dist/b/1555/files/2020/09/MargulieuxandCatrambone2016.pdf,
claim 6 CONFIRMED). PROVE itself is the label set.

**Adaptivity at the SEAMS is UNBUILT / assumed-pending-eng.** True within-lesson adaptive
fading beats fixed fading, but it needs state we do not have. It COULD be approximated
with between-lesson branch-on-score routing (the external `rc.*` grader's score on a
production item, or a one-item first-step-style diagnostic, choosing the entry rung or a
more/less-worked next lesson variant). Treat that routing as an UNBUILT capability,
contingent on the platform actually supporting next-lesson routing on a grader score, NOT
as delivered. The lesson SHIPS as a complete, self-sufficient FIXED-FADE sequence that
requires ZERO routing to function; adaptive variant-selection is a pending-eng increment
layered on top only if the seam exists. Fixed fading still beats no fading, so the default
path loses only that increment. Source: research_worked-example-fading claims 7-9
(Salden et al. 2010; Kalyuga 2007 first-step method, correlations up to .92);
Kyun, Kalyuga & Sweller 2013 (https://eric.ed.gov/?id=EJ1011878, claim 7 CONFIRMED:
worked-example advantage is strongest for lowest-knowledge writers, so leveling matters
even statelessly).

---

## 5. Function-over-form device instruction (directly relevant to T3)

T3 is, at its core, a FUNCTION-OVER-FORM archetype: both taught devices are syntactic
structures taught by the rhetorical JOB they do, not by grammatical label.
- The **appositive attributive tag** is T3's ATTRIBUTION tool: APPOSITIVE -> AUTHORITY.
  It names and credentials the source with an appositive or adjectival phrase, lending
  authority to the quote. Teach it as "add authority by naming who said it in an
  appositive" (e.g. "Dr. Reyes, a marine biologist who has studied reefs for two
  decades, says..."), never "identify the appositive." This is the move that supplies
  the R (Reference) of PROVE.
- The **because/but/so hinge** is T3's REASONING hinge (the core move here): the reason /
  contrast / consequence link that ties the fact to the claim. because = give the reason;
  but = give the counter or limit; so = give the consequence. This maps almost
  one-to-one onto a stateless item: the function is the prompt, the structure is the
  answer. It is the O and V (Observe, Verify) of PROVE: the writer states why the quote
  proves the point instead of leaving a bare quote to stand alone.
Source: research_function-over-form §7 (TWR/Hochman because-but-so and appositive as
function-anchored moves) and the synthesis design moves.

**Gate note (app-owned mechanics).** Mechanical sentence-combining craft is
AlphaWrite-owned G3-8; T3 GATES it as a retrieval-gated prerequisite and APPLIES it in
service of attribution + hinge, and never re-teaches the mechanics from scratch.
Source: Principle B gate.

**What the evidence lets us claim:**
- Do NOT build "which of these is the appositive?" label-identification items. Isolated
  traditional grammar has a small but significant NEGATIVE effect on writing quality
  across the ability range (Writing Next, "A Note About Grammar Instruction,"
  research_function-over-form claim 2 CONFIRMED VERBATIM; corroborated by Andrews et al.
  2006 and Hillocks 1986).
- DO teach the device by its job and make the student USE it in composing. Function +
  application beat definition in a controlled tenth-grade experiment (Fearn & Farnan,
  2005, When Is a Verb?, https://files.eric.ed.gov/fulltext/EJ787964.pdf,
  research_function-over-form claim 4 CONFIRMED VERBATIM), and sentence-combining /
  expansion is the mechanism with the best warrant (Writing Next d = 0.50; Saddler &
  Graham 2005; research_function-over-form claims 1, 5 CONFIRMED). The PROVE sentence
  APPLIES sentence-combining in context (fuse the quote, the attribution, and the hinge
  into one integrated sentence); the combining mechanics are AlphaWrite-owned G3-8 and
  gated as a prerequisite here, not re-taught (see the gate note above).
- DO bake the "why this structure creates this effect" talk INTO the worked example and
  the answer rationales. Contextualised "grammar as choice" worked, but the effect was
  small (approx 0.21), skewed to abler writers, and MEDIATED by a knowledgeable teacher's
  discussion (Myhill et al. 2012; Jones, Myhill & Bailey 2013,
  https://link.springer.com/article/10.1007/s11145-012-9416-1,
  research_function-over-form claims 5-6 CONFIRMED). We have no teacher, so that
  mediating talk must live in the annotated before/after and the reveal rationales, and
  weaker writers need the function stated very concretely and over-scaffolded.

**Delivery pattern (stateless):** discrimination items use the Fearn-and-Farnan "does
this structure do the job here?" shape: "Which revision makes the source sound
authoritative?" with the key being an appositive that names/credentials the source and
distractors that are the right grammatical form doing a different job. Each item carries
its own kernel sentence and function prompt in-stem. Source: research_function-over-form
synthesis (Supported / Independent / Transfer design moves).

**Honest provenance flag:** the tidy one-to-one device-to-function map is a DESIGN
CHOICE imposed for clarity, not a finding lifted from a single study. because/but/so ->
reason/contrast/consequence is strongly attested (TWR); appositive -> authority is clean;
looser mappings (relative clause -> consequence) should be avoided in favor of the
cleanest exemplar function per device. Source: research_function-over-form §"honest gaps."

---

## 6. The 19 lesson_contract gates: sharpest risks for T3 and how to satisfy

The contract runs exactly 19 gates in order (`lesson_contract.py` GATES list,
loc ~483-503). Ranked by how hard they bite T3 (extract §5):

1. **`effect_size_honesty`** (loc ~256). T3 is THE type the spec labels "ES 1.14," so
   it is the single most tempting over-claim. SATISFY: never print "ES 1.14 / 1.02" or
   "inherits SRSD's evidence" in student- or author-facing lesson text; frame moves as
   evidence-INFORMED, citing modality-flexible ingredients.
2. **`define_before_use`** (loc ~338). T3 owns three gated terms (attributive tag,
   appositive, because/but/so hinge). SATISFY: give each a plain-words definition in a
   TEACH slot before first use.
3. **`type_ceiling` + `unit_ladder`** (loc ~447, ~421). SATISFY: cap scored production
   at paragraph; climb sentence then paragraph, non-decreasing; never an essay, never a
   drop back to a smaller unit.
4. **`no_prior_work_reference`** (loc ~292). SATISFY: teach revision on PROVIDED pairs;
   never "revise the bare quote you wrote."
5. **`model_sequence`** (loc ~154). SATISFY: MODEL contains `annotated_before_after` +
   `predict_the_fix` (with non-empty feedback), and a scaffolded `diagnosis_frq` exists;
   no passive-read think-aloud transcript.
6. **`no_source_markup`** (loc ~278). SATISFY: "read and note," never "underline /
   highlight the quote." The quote-selection instruction is where this creeps in.
7. **`mnemonic_status`** (loc ~468). SATISFY: declare provenance `mnemonic_status =
   "established-caveat"` (PROVE is unverified-shipped K-8; verify before reuse), not
   "proposal."
8. **`content_depth`** (loc ~360). SATISFY: teach_card >= 200 chars;
   annotated_before_after >= 220 chars and contains BOTH the literal words BEFORE and
   AFTER inline.
9. **`discrimination_before_production`** (loc ~172). SATISFY: a `discrimination` slot
   precedes any production and at least one sets `labeled_grade_c=True`.

Shared-but-required (must still pass): `shell_completeness`, `binding_integrity`,
`bank_partition`, `grader_routing`, `timeback_native`, `calibration_discipline`,
`model_before_required`, `no_ambiguous_reference`, `no_em_dash`. Note
`calibration_discipline`: never "here is the rubric, grade yourself" with no reveal
(self-assessment overestimate bias), and never person-praise ("great job") instead of
GOAL/NOW/NEXT process feedback. Source: extract §5-6; Toolkit Rules 7-8.

**Kill-list (T3 anti-patterns):** claiming SRSD's ES 1.14 for the async model; claiming
the coping-model / social-modeling effect size for the screen build; a near-peer coping
persona, fake-student inner monologue, or "visible false start + self-talk" beat (dropped
per Principle A); a clean final exemplar with no error-recovery contrast;
"underline/highlight the quote you will use"; "revise your dropped quote from Step 2"; an
iterative revise-the-same-draft loop in the Option-E engine; treating between-lesson
score-routing as delivered rather than UNBUILT; using appositive / attributive tag /
because-but-so cold and undefined; re-teaching mechanical sentence-combining (AlphaWrite
G3-8, gate and apply only); a full-essay production; "grade yourself" with no reveal;
person-praise; bolting a second mnemonic (a parallel TSIS system) on top of PROVE.
Source: extract §6.

---

## Retrieval + item rules (LS feedback 2026-07)

These encode the 2026-07 learning-scientist pass as T3 authoring defaults so a fresh evidence-integration lesson clears the new gates by construction.

- **Cadence ceiling: CONCEPT tier, ceiling 3** (`gate_check_cadence`). T3 is a concept-teaching type: a run of COUNTED teach cards (teach_card, stimulus_display, annotated_before_after) may not exceed THREE before a check (`discrimination` / `predict_the_fix` / `self_score`). The annotated before/after counts as ONE worked example, do not split it to pad the run. Tag a pure buy-in card `tag="buy_in"` so it counts 0. TIGHTEN to 2 right after the card that introduces a named memorizable tool (the PROVE mnemonic, the because/but/so hinge, the appositive attributive tag): tag that card `tag="memorizable_tool"` and place the integrated-vs-dropped discrimination immediately behind it.
- **Four options per discrimination, each a NAMED MISCONCEPTION** (`gate_structural_item`). The integrated-vs-dropped minimal pair carries exactly four choices, each a real T3 wrong move (a dropped quote with no attribution, a named quote with no hinge, a hinge that restates instead of tying to the claim), never filler.
- **Diagnosis: the student ANSWERS the check, then improves** (`gate_self_answered_check`). The modeled self-check may pre-answer a PROVIDED weak specimen ("The author says reefs are dying. This proves my point."), but name that specimen AND then require an independent student turn (run the same check on a fresh PROVE sentence of their own). Do not print a diagnosis that answers its own questions and stops.
- **No comma before "because"/"so" in a fill-in frame** (`gate_frame_comma`). The completion frame ("... ______ because ______ ...") drops the comma before because, since the frame is a punctuation model the student copies. Emit it with `claim_frame()` from `lesson_prompts` rather than hand-writing it.
- **Re-gloss the hard terms.** T3 owns the most gated jargon (attributive tag, appositive, because/but/so hinge); `gate_define_before_use` already forces an in-lesson gloss for controlling idea, warrant, synthesis, and counterclaim if they appear. On a later-lesson re-introduction prefer a BRACKETED gloss right after the term (LS #9 style).
- **Stem wording (playbook-only, #7):** name the move directly ("Which sentence explains why the quote supports the point?"), never a meta-phrasing ("which fits the verb").
- **Tone (playbook-only, #5 / Yeager):** state the standard up front; each per-choice reveal is wise-feedback that names the MOVE, no person-praise, no compliment-sandwich.
- **Pair a stand-alone improve-write with a `predict_the_fix`** where feasible (playbook-only, #4).
- **Cross-lesson spacing (KH caveat, #3):** the in-lesson cadence gate is necessary but NOT sufficient; the PROVE moves (attribution, the hinge) must recur in later T7/T8 lessons. That durability is a sequence-builder concern, not visible to this lesson's gates.

---

## 7. Keep it short

- **One strategy, one contrast.** T3 teaches exactly one move (integrate a quote) and
  drills one minimal-pair contrast (integrated vs dropped). TSIS frame-the-quotation
  lives as CONTENT inside the PROVE slots, never as a parallel mnemonic (build rule 8).
- **Worked-example-first, not explanation-first.** Lead with the annotated before/after
  and predict-the-fix; hold teach prose to what P1-P3 require. Extra explanation on a
  self-evident annotated example HURTS (redundancy effect, KB `00` §1.1). Meet the depth
  floors without padding.
- **Sentence rung before paragraph rung.** One integrated sentence first is shorter and
  lower-load and satisfies the ladder; the paragraph is the ceiling, reached once, at
  Independent.
- **Let the shell and the fade ledger do the work.** Five stages, each a small set of
  items; because/but/so and the attributive tag arrive partly faded from earlier types
  via the shared `fade_ledger_moves`, so T3 need not re-teach them from zero.

Source: extract §4.

---

## 8. The flagship item sequence (D-baseline, copy this shape)

From the finalized per-type structure (Model Specs; extract §3) and the working contract
demo (`lesson_contract.py` loc ~529-586, which PASSES all 19 gates):

1. `teach_card` (PROVE cue + product goal; define the three terms).
2. `stimulus_display` (source passage, read-and-note framing).
3. `annotated_before_after` (MODEL rung 0: same quote, BEFORE bare / AFTER integrated,
   annotation on the sentence, both inline).
4. `predict_the_fix` (choice + feedback-block reveal; diagnose before answer).
5. `discrimination` (integrated vs dropped minimal pair; `labeled_grade_c=True`).
6. `production_frq` sentence (attribute + hinge), routed to an `rc.*` config.
7. `diagnosis_frq` (scaffolded self-check frame: lacked ___ / added ___ / stronger
   because ___).
8. `production_frq` paragraph (INDEPENDENT: claim + integrated quote), `rc.*` config.
9. `production_frq` paragraph on a bank-partitioned NEW topic (TRANSFER), second config
   (e.g. `rc.ohio`).
10. Native retake (stock `allowRetake`; blank box; nothing to build).
11. Option-E / upgrade-only: revise-feedback engine gives 1-3 cards on the student's OWN
    paragraph as a ONE-SHOT eval of that single fresh submission (async substitute for
    live conferencing; NOT stock Timeback; never an iterative revise-same-draft loop; no
    required slot depends on it).

Timeback flags carried through this shape: no markup on the stimulus (step 2), no
cross-item reference (steps 6-9 are self-contained), retake starts blank (step 10),
personalized revision is upgrade-only (step 11).
