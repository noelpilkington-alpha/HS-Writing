# Authoring Playbook: T7 Essay-Assembly (mnemonic BUILD, ceiling = essay)

> **What this entry is.** A teachable, author-facing playbook for building a T7 essay-assembly lesson that
> passes all 19 `lesson_contract.py` gates on the first sitting. It fuses the internal archetype extract
> (`extract_T7_BUILD.md`, cited as [EXTRACT §n]) with the four verified Phase-2 research briefs
> (async-SRSD, worked-example fading, feedback-as-teaching, function-over-form; cited by brief + claim). A
> passing reference instance already exists at `Lesson_Bank_G10/lesson_t7_essay_assembly.py` (all 19 gates
> PASS, re-confirmed 2026-07-10) and is cited as [REF] where its wording shows how a principle survives a
> gate. All prose is own-authored. No em dashes. Cite external claims by author/year; accessible URLs live
> in the research briefs.

---

## 0. Terminal deliverable and production ceiling

**Terminal deliverable.** A single-source (or opposing-pair) argumentative essay, planned and drafted under
test conditions: the student brainstorms to the prompt, writes an SPO plan (a one-line thesis plus ordered
body lines with named evidence), scales it to a multi-paragraph outline, drafts from the plan with a funnel
opening and a significance conclusion, answers one counterclaim, and self-reviews to the rubric. This is
"the composite the other types feed" and "IS the test" [EXTRACT §0]; the STAAR single-source ECR is the
exact task.

**Production ceiling = `essay`.** T7 is one of only two types (with T8 synthesis) that `TYPE_CEILING_UNIT`
permits to reach the `essay` unit; every component type tops out at paragraph or sentence [EXTRACT §0;
`lesson_contract.py` TYPE_CEILING_UNIT = {7: "essay"}]. The essay is licensed here precisely because the
parts are already fluent: this is TWR parts-before-whole ("a writer who cannot compose a decent sentence
will never produce a decent essay") made machine-checkable in `UNIT_LADDER`.

**The one governing fact.** T7 is the HIGHEST-composite-load task in the course. Hayes and Flower: planning,
translating (drafting), and reviewing compete for the same working memory at once [EXTRACT §0]. Every
authoring move is therefore a working-memory-management move: keep the intrinsic load (composing a whole
argued essay) from colliding with any avoidable extraneous load.

**Mnemonic.** BUILD = Brainstorm to the prompt, Underline (write out) the plan, Lay out paragraphs,
Integrate the moves you already own, Double-check to the rubric. `gate_mnemonic_status` REQUIRES
`mnemonic_status = "proposal"`; claiming it is established is an automatic reject [EXTRACT §0]. BUILD is the
"Memorize It" artifact of SRSD, which Harris (2024) notes reduces load but does not by itself create good
writing, so it must be paired with application (async-SRSD Claim 1, §2).

---

## 1. TEACH stage

**SRSD map.** Develop Background Knowledge + Discuss It, delivered as a short display teach card plus the
test-demand orientation. Async-SRSD confirms both survive intact on a stateless screen: background/discuss
becomes "short expository teaching plus discrimination items," not a live conversation (async-SRSD Claim 1,
§2, VERIFIED).

**Moves.**

1. **Name the composing-process problem first, then the fix.** State WHY planning matters in load terms:
   three jobs (deciding what to say, turning it into sentences, checking it) fight for room at once, and the
   fix is to make them separate phases (write your plan in the plan box, then draft, then review) [EXTRACT §1
   move 1]. The plan is written ON-PLATFORM in an extended-text plan box, never on off-platform paper, so the
   external grader can see it. [REF] does this in plain student words. This is the T7-specific "purpose and
   when/why" that WWC Rec 1 (explicit strategy instruction via Model-Practice-Reflect, STRONG evidence) calls
   for (feedback brief §1.8, VERIFIED).
2. **Teach the SPO as the working-memory offload, not a formatting ritual.** Frame it as "a written plan
   holds the order for you so your head is free to build good sentences" [EXTRACT §1 move 2]. This is the
   CLT worked-example / externalization rationale stated for the student.
3. **Cue the owned sub-skills; do NOT re-teach them.** The Integrate step points at the Types 2-4 moves the
   student already owns (defensible position, evidence tied to claim, answered counterclaim) AND the
   sentence-level TWR moves that were taught and faded in the component types: because/but/so as the
   reasoning hinge (T2/T3) and modifiers-by-function (appositive for source authority, relative clause for
   consequence, prepositional phrase for context; T3/T4). T7 assembles; it does not re-teach these. Reference
   them by their JOB inside the plan ("hinge the reason with because/but/so; name the source with an
   appositive"), so the student draws on already-faded prerequisites while planning. Re-explaining is
   redundant load for a student who has faded those scaffolds [EXTRACT §1 move 3; redundancy effect]. The
   expertise-reversal literature is explicit that heavy worked support helps novices but HURTS more
   knowledgeable learners (fading brief Claim 6, Kyun/Kalyuga/Sweller 2013 for writing specifically,
   VERIFIED). Teach references the owned moves by name and moves on.

   *App-owned gate:* AlphaWrite owns sentence-combining craft G3-8 and EGUMPP owns conventions G3-10; T7
   APPLIES these as retrieval-gated prerequisites and cues their rhetorical USE, never the mechanics from
   scratch.
4. **Teach the two top-band framing moves explicitly** (the funnel opening: context, THEN thesis; the
   reverse-funnel conclusion: synthesize, THEN significance / "so what," not a summary) [EXTRACT §1 move 4].
   These separate mid-band from top-band and are the easiest to skip under time pressure, so they are
   taught, not assumed. [REF] teach card 2 delivers both.
5. **Set a specific product goal** [EXTRACT §1 move 5; Writing Next product goals ES 0.70]: "a context intro
   with a clear thesis, 2-3 evidence-based body paragraphs each tying evidence to the thesis, one answered
   counterclaim, and a significance conclusion." Never "write a good essay."

**Worked-example shape at Teach.** None yet. Teach names the strategy, the terms, and the goal; the worked
artifact lives in Model [EXTRACT §1]. Keep Teach to definitions + purpose + goal.

**Stateless/async delivery.** Two `teach_card` display slots (native HTML display) plus one
`stimulus_display` binding the source. The source is display-only XHTML with JS stripped, so the read is
framed as "read and note the strongest fact on each side," never "mark up the source" (see gate risk 4).
BLOCKED: no live discussion; the "discuss it" is reconstructed as expository teaching that feeds the later
discrimination item.

---

## 2. MODEL stage

**SRSD map.** The async Model sequence built around a worked example, NOT a passive-read messy think-aloud
and NOT a near-peer persona (`gate_model_sequence`). Static screen text cannot reconstruct the live human
social-modeling that the coping-model evidence depends on, so T7 drops the persona / visible-false-start /
self-talk device entirely and carries the Model on the screen-validated worked-example effect: a weak BEFORE
and a strong AFTER, with the common error and its fix shown as labeled author-voice annotations on the
exemplar (async-SRSD §3; worked-example fading brief, VERIFIED). `gate_effect_size_honesty` forbids claiming
SRSD's live ES 1.14 for the async model, so the design cites the modality-flexible ingredients (annotated
worked example, forced response, personalized process feedback) instead [EXTRACT §2].

**Moves.**

6. **Mechanism 1, the clean annotated before/after, contrasts a PLUNGED-IN pile against a PLANNED essay.**
   The BEFORE is a no-plan draft: the writer plunged into drafting and produced "three paragraphs that build
   toward nothing." The AFTER shows the SPO written first, then the drafted funnel intro and reverse-funnel
   conclusion. The common error and its fix are shown as labeled author-voice annotations ON the two texts
   ("problem: no plan, so the body has no order" / "fix: SPO fixes the order before a sentence is written"),
   not as any writer's inner monologue [EXTRACT §2 move 6]. `gate_content_depth` REQUIRES both BEFORE and
   AFTER present inline. [REF] shows BEFORE as a fact/counter-fact pile that shrugs at the end, and AFTER as
   an SPO plan then a drafted funnel intro and reverse-funnel conclusion. This is an annotated worked example,
   not a persona monologue, which is the screen-validated choice (async-SRSD §3a).
7. **Mechanism 2, predict-the-fix, targets the failure the student will actually commit:** no plan, so the
   body has no order and the conclusion only restates the intro. Distractors are the plausible wrong
   diagnoses (sentences too short, too many facts, drop the counterclaim) so the item teaches that the
   problem is structural, not surface [EXTRACT §2 move 7]. This is the errorful-generation / hypercorrection
   mechanism: committing to a prediction before the reveal is the mechanism, not wasted motion (feedback
   brief §1.6, Metcalfe 2017, VERIFIED). `gate_model_sequence` requires the predict-the-fix carry a
   non-empty `feedback` reveal, and the reveal must explain WHY (elaboration beats verification; Shute 2008,
   feedback brief §1.2).
8. **Mechanism 4, a student-generated diagnosis, is required somewhere in the lesson** (`gate_model_sequence`
   fails without a `diagnosis_frq`). For T7 this is a diagnosis of a flawed intro + conclusion against the
   context / thesis / significance checklist [EXTRACT §2 move 8]. In [REF] this slot lives under SUPPORTED
   but satisfies the mechanism-4 requirement.

**Worked-example shape (the single most important T7 design decision).**

9. **Model the PLAN plus the two framing moves, NOT a full essay transcript** [EXTRACT §2 move 9]. The AFTER
   shows the compact SPO (thesis line + ordered body lines with evidence), the drafted funnel intro, and the
   drafted reverse-funnel conclusion. It does NOT print a full five-paragraph essay. The plan carries the
   organizational load compactly; the two framing moves are the highest-value drafted prose. This is the
   worked-example effect applied within the load ceiling, and it is what lets a whole-essay model survive
   `gate_content_depth`'s 220-char floor without becoming unreadably long.
10. **Annotate ON the exemplar, integrated, not in a separate legend** [EXTRACT §2 move 10; split-attention].
    Inline bracket labels ([context], [thesis], [synthesis], [significance]) sit in the AFTER text itself.
    These are subgoal labels: they tag groups of sentences by the FUNCTION they accomplish, which chunks
    working memory and externally prompts the right self-explanation without decaying over time (fading brief
    Claim 5, Margulieux and Catrambone 2016, VERIFIED). Use the SAME functional labels across the whole
    ladder so the labels become the through-line a stateless sequence otherwise lacks (fading brief §Synthesis
    move 4).

**Stateless/async delivery.** `annotated_before_after` renders as native HTML display; `predict_the_fix`
renders as a choice item with a feedback-block reveal. Both are self-contained: the flawed draft the student
diagnoses is PRINTED IN the item stem, never the student's own prior work (feedback brief §2.1 pattern 2;
this is stateless because the object judged is fixed and inside one item).

---

## 3. SUPPORTED stage

**SRSD map.** Support It, delivered as the KH worked-example then completion-problem then independent ladder,
with the fade gated by performance from the shared fade ledger [EXTRACT §3]. Async-SRSD: author the
scaffolding as a decreasing-support item sequence and let the external grader carry the formative-feedback /
conferencing role (async-SRSD §4, VERIFIED).

**Moves.**

11. **Discrimination before any production** (`gate_discrimination_before_production`; must set
    `labeled_grade_c = True`). The T7 contrast is a planned/funnel opening versus openings that show no plan
    (a fact-list with no position, a topic announcement with no context, an off-source personal story). This
    teaches "an ordered argument vs a pile of paragraphs" before the student plans [EXTRACT §3 move 11]. It
    is a Grade-C design bet, not a proven law [Framework Audit item 4], so the slot must say so. The
    discrimination itself is the observe-and-compare mechanism (Braaksma: learners extract the criteria for
    good writing by comparing models; async-SRSD §3a, VERIFIED), and it is a strong/weak exemplar contrast
    (WWC Rec 2; feedback brief §1.8).
12. **Completion-problem planning: hand a PARTIAL SPO and have the student finish it.** [REF] gives the
    thesis and Body 1 and asks the student to write Body 2 and Body 3 with named source evidence in build
    order [EXTRACT §3 move 12]. The completion problem is the ideal stateless rung because ALL the context
    the student needs is printed in the item stem, so the item is self-sufficient by construction (fading
    brief Claim 3, van Merrienboer 2002, VERIFIED). This scaffold (the plan) is the one that fades LAST.
13. **Modeled diagnosis, then the student runs the same checklist.** The `diagnosis_frq` first shows the
    check running on a flawed intro and conclusion (against the context / thesis / significance checklist),
    then asks the student to name the missing moves and write one repair sentence for each [EXTRACT §3 move
    13]. The checklist must be IN the prompt (`gate_model_before_required`). This is a self-assessment SCRIPT
    (an ordered set of self-questions), which raises self-regulation more than a bare rubric and is fully
    stateless because it lives inside the item (async-SRSD §5c and feedback brief §1.7, Panadero 2012,
    VERIFIED). Self-assessment against criteria carries a large writing effect (ES 0.62), close to teacher
    feedback and above automated feedback (feedback brief §1.3, Graham/Hebert/Harris 2015, VERIFIED).

**Worked-example shape at Supported.** The partial SPO IS the faded worked example (worked-example to
completion-problem) [EXTRACT §3]. Fade BACKWARD: the provided lines model the earliest, still-worked steps
and stay visible as contextual scaffolding while the student generates the LAST, unblanked steps (Body 2,
Body 3). Backward fading is the direction with the significant far-transfer gain and the efficiency win
(fading brief Claim 2, Renkl 2002 Exp 3, VERIFIED).

**Stateless/async delivery.** One `discrimination` choice item (a four-option minimal pair with the reveal
built in), one `production_frq` at `unit="sentence"` (an outline line is sentence-sized, so the student does
short high-value planning reps, not a whole essay under scaffold; [REF] sets this), and the scaffolded
`diagnosis_frq`. Every prompt is self-contained: the diagnosis runs on a PROVIDED flawed intro/conclusion,
never "diagnose YOUR intro" (`gate_no_prior_work_reference`).

---

## 4. INDEPENDENT stage

**SRSD map.** Independent Performance on fresh items. This is the payoff stage; SRSD's strongest results
appear when scaffolding is withdrawn and the student writes independently (async-SRSD §2, VERIFIED as the
goal stage).

**Moves.**

14. **Climb the unit ladder inside Independent: plan (sentence), then one body paragraph, then the full
    essay.** [REF] runs three Independent FRQs, each self-contained: build the full SPO from scratch
    (`unit="sentence"`); write a one-line mini-plan (claim + named evidence) THEN draft the body paragraph
    from it in ONE extended-text box (`unit="paragraph"`); then draft the full essay (`unit="essay"`)
    [EXTRACT §4 move 14]. The body-paragraph FRQ NEVER says "draft from the plan you wrote above" (a
    `gate_no_prior_work_reference` violation across stateless items); the student re-states a fresh mini-plan
    inside the same item, so the paragraph is built from context the item itself supplies. This realizes
    parts-before-whole WITHIN one lesson: prove you can plan the whole, then build one part, then build all
    of it.
15. **Fade the planning scaffold LAST.** Planning offloads the most working memory, so the outline is the
    last support removed [EXTRACT §4 move 15]. At Independent the outline is now student-generated, but
    planning is still required as an explicit phase, not dropped. Asymmetry rule: when unsure, keep the
    scaffold one rung longer [Framework Audit item 3: scaffold fading for writing is a grounded
    extrapolation, not a proven writing result].
16. **Every production prompt is self-contained.** Each FRQ re-states what to do from scratch ("build your
    own SPO ... then draft") rather than "use the plan you wrote above," because QTI retakes start blank and
    no item can see prior responses (`gate_no_prior_work_reference`) [EXTRACT §4 move 16]. The composing
    sequence is taught as a described process inside each self-contained prompt.
17. **Route every production to a real rubric config** (`gate_grader_routing`): [REF] uses `rc.4trait` for
    the plan reps and `rc.staar` for the paragraph and essay. Each `production_frq` MUST carry an `rc.*` from
    `RUBRIC_CONFIGS` [EXTRACT §4 move 17].

**Worked-example shape at Independent.** None; scaffolds are faded [EXTRACT §4]. The student produces.
Feedback on the student's own draft (async Mechanism 3) is delivered by the external grader, not by an
authored model.

**Stateless/async delivery.** Three `production_frq` extended-text slots, each routed to the external
rc.* grader. The grader IS the reconstructed conferencing loop: intelligent writing tutors deliver strategy
instruction then score student essays with NLP feedback and no teacher in the loop (async-SRSD §4b, W-Pal;
feedback brief §1.9, Fleckenstein 2023 g = 0.55, VERIFIED). Keep the teach/model load high, because W-Pal
found students who got strategy instruction (not just more essays) made the substantive revisions that
implemented the automated feedback (async-SRSD §4b, VERIFIED).

**Between-lesson adaptivity is UNBUILT (assumed-pending-eng), not a delivered capability.** You cannot fade
adaptively within a stateless lesson. Score-based routing (using the external-grader score on the essay FRQ
to send the student to a more/less-worked next rung or lesson variant) is an ASSUMED capability pending eng,
contingent on the platform actually supporting next-lesson routing on a grader score; it is NOT something
this lesson delivers. T7 therefore ships as a complete, self-sufficient FIXED-FADE sequence requiring ZERO
routing to function (fading brief Claims 6-7: fixed fading already beats no fading, and adaptive fading is an
improvement on top, not a precondition, VERIFIED). If seam-routing is later built, it recovers coarse
expertise-reversal adaptivity without any item reading another item's response.

---

## 5. TRANSFER stage

**SRSD map.** Novel-transfer slot from a DIFFERENT content bank, DI hard bank-partition
(`gate_bank_partition`).

**Moves.**

18. **Transfer is a WHOLE timed essay on a partitioned topic.** [REF] teaches on congestion pricing and
    transfers to daylight saving time; the transfer prompt runs the entire BUILD process on a source the
    student has not practiced [EXTRACT §5 move 18]. This is genuine transfer, not recall.
19. **Bank-partition the timed prompt from ALL taught prompts.** Near transfer (same genre, new prompt) is
    the reliable claim and far transfer is weaker, so T7 transfer stays within the genre (source-based
    argument) but on a fresh source, which is the near-transfer band we can claim confidently [EXTRACT §5
    move 19]. Give the transfer FRQ its own `rc.*` and declare `unit="essay"` so the ladder and ceiling
    gates still pass [EXTRACT §5 move 20].

**Worked-example shape at Transfer.** None; transfer is a clean-room performance on new material.

**Stateless/async delivery.** One self-contained `production_frq` bound to a new stimulus id, scored by the
grader. Do NOT add new teaching at transfer; if a move needs re-teaching it belonged earlier in the shell.

---

## 6. Feedback-as-teaching within the stateless boundary

The precise line: feedback-as-teaching survives when the object judged is fixed and self-contained within a
single item (a text we provide, or one fresh submission scored once). It breaks the moment the design needs
to carry the student's own words, judgment, or score from one item to the next (feedback brief §2.3).

**DELIVERABLE in T7 (build these):**
- **Grader feedback on the student's own single essay submission** (async Mechanism 3), routed to rc.* on
  each `production_frq`. A single evaluation of one input, so statelessness is a non-issue (feedback brief
  §2.1 pattern 1).
- **Predict-the-fix then reveal, inside ONE item** (the Model mechanism-2 slot). Show the flawed
  no-plan draft, ask for the single biggest problem, then reveal the fix and the WHY. Errorful generation +
  hypercorrection is the mechanism (feedback brief §2.1 pattern 2, Metcalfe 2017).
- **Strong/weak exemplar contrast** as the SUPPORTED discrimination (four openings, pick the funnel that
  shows a plan, reveal why the others fail). Fully stateless; both texts provided (feedback brief §2.1
  pattern 3).
- **Self-assessment SCRIPT on a provided flawed intro/conclusion, then on the student's own single draft**
  (the diagnosis slot's checklist). Stateless; it applies to a provided text or one fresh submission but
  cannot compare that submission to a prior draft (feedback brief §2.1 pattern 5).
- **Elaborated, process-level reveals that name the MOVE and give a reusable self-check**, not bare
  correct/incorrect (Hattie and Timperley 2007: process and self-regulation feedback teach, self-praise does
  not; feedback brief §1.1). `gate_calibration_discipline` enforces this from the other side by banning
  person-praise.

**BLOCKED by statelessness (do not design around these) [feedback brief §2.2]:**
- Feedback on the student's EVOLVING draft across turns (draft, feedback, revise the SAME draft, feedback
  again). The 80-90 percent self-fix-when-prompted loop depends on a coach seeing the current draft; that
  turn-to-turn loop is not deliverable. This is the deepest T7 tension: the composing process is inherently
  sequential (plan, then draft from your plan), yet the delivery is stateless [EXTRACT §4]. The workaround is
  to teach the sequence as a DESCRIBED process inside each self-contained prompt.
- Iterative revise-and-recheck on the student's own text; any reference to an earlier answer or score
  ("compared to your plan in step 2"); progress monitoring over time. All need cross-item state
  (`gate_no_prior_work_reference` rejects them).

---

## 7. Worked-example fading without statefulness

The fade is a SEQUENCE property, not a within-item adaptive loop. The foundational fading studies used a
FIXED, pre-scripted schedule and it worked; adaptivity is an improvement on top, not a precondition (fading
brief Claim 1, Renkl 2002, VERIFIED). So author the fade as an ordered set of isolated items at fixed
scaffolding levels. In T7 the ladder is:

- **Model (rung 0):** the fully worked exemplar with subgoal labels (the annotated before/after: SPO +
  labeled framing moves).
- **Supported (backward-faded completion problem):** the PARTIAL SPO. Thesis + Body 1 are provided and stay
  visible (the still-worked earlier steps); the student generates Body 2 and Body 3 (the last steps). This is
  backward fading, the direction with the far-transfer and efficiency wins (fading brief Claim 2), delivered
  as a self-sufficient completion item because the partial plan is printed in the stem (fading brief Claim 3).
- **Supported (scored discrimination):** the principle-naming self-explanation as a SCORED choice item
  ("which opening shows a plan driving the essay?"), not a free "explain what you did" prompt. Prompt for the
  structural principle, because generic self-explanation prompts can trigger a redundancy/overload effect and
  hurt (fading brief Claim 4, Barbieri 2023, VERIFIED).
- **Independent (deeper fade):** SPO from scratch (sentence), then one body paragraph (paragraph), then the
  full essay (essay). More is blanked at each rung.
- **Transfer (full production):** externally graded; score-based routing to the next lesson is an UNBUILT /
  assumed-pending-eng capability, not delivered here (fading brief §Synthesis move 7).

**Through-line device:** use the SAME functional subgoal labels ([context], [thesis], [synthesis],
[significance]) across every rung so the stateless sequence coheres (fading brief Claim 5). BLOCKED:
per-student adaptive fading inside the lesson. The lesson ships as a self-sufficient fixed-fade sequence
requiring zero routing; any coarse adaptivity at the routing seam is UNBUILT / assumed-pending-eng, not
delivered (§4 above).

---

## 8. Function-over-form device instruction (limited but real relevance)

T7 does NOT teach syntactic devices as forms; those were taught and faded in the component types (T2 claim,
T3 evidence, T6 editing), and re-teaching them here is redundant load [EXTRACT §1 move 3]. So the
function-over-form research applies to T7 in two narrow, high-value ways, both of which follow the
brief's core finding: teach by the JOB a structure does, make the link between structure and effect explicit
IN the material, and never ask the student to label a form (function-over-form §Synthesis, VERIFIED;
isolated grammar has null-to-negative effects while function + application beats definition, Fearn and Farnan
2005).

1. **The two framing moves are themselves taught by function, not form.** The funnel opening is taught as
   "give context so the claim lands in a setting" and the reverse-funnel conclusion as "synthesize, then
   answer so-what" [EXTRACT §1 move 4]. These are rhetorical-function labels (Kolln's "grammatical choices,
   rhetorical effects" framing; function-over-form source 9), not structural rules. The worked example states
   in-line WHY the reader experiences the intended effect, which bakes in the teacher's mediating "why does
   this create this effect" talk that Myhill's gains depended on and that a no-human product must supply in
   the material itself (function-over-form §3, Myhill 2012, VERIFIED with caveat: small effect, skewed to
   abler writers, so over-scaffold and state the function concretely).
2. **Source-authority devices are CUED by function, not re-taught.** When the Integrate step points at
   evidence tied to the thesis, the attributive tag / appositive that "names and credentials the source" is
   referenced by its job (add authority) [function-over-form §7, TWR; source 2]. T7 cues it; it does not run
   a device lesson.

Honest gap: the one-to-one device-to-function map is a teachable DESIGN CHOICE, not a finding lifted from a
study, and must be flagged as such under the provenance rule (function-over-form §Where the evidence is thin).

---

## 9. The 19 gates, ranked by how hard they bite T7, and how to satisfy each

All 19 must pass; [REF] passes all 19 (confirmed 2026-07-10). Ranked most-to-least T7-specific:

1. **`gate_unit_ladder`** (T7-signature). The scored productions must be NON-DECREASING (sentence to
   paragraph to essay). Satisfy: order the Independent FRQs plan (sentence) -> body paragraph (paragraph) ->
   full essay (essay); never place a smaller unit after a larger one. [REF] declares `unit=` on every scored
   FRQ and climbs sentence, sentence, paragraph, essay, essay.
2. **`gate_no_prior_work_reference`** (T7-signature). Plan-then-draft-from-your-plan is the natural composing
   sequence but is stateless-illegal. Satisfy: make each of the five productions self-contained ("build your
   own SPO ... then draft"), and phrase revision/diagnosis on a PROVIDED example, never "your plan above."
3. **`gate_type_ceiling`** (T7-defining). Satisfy: declare `lesson_type=7` so the `essay` unit is licensed;
   the same essay FRQ inside any component type would be rejected.
4. **`gate_no_source_markup`** (T7-trap). The BUILD U-step "Underline the plan" reads as source markup on a
   display-only stimulus. Satisfy: word it "write your plan in the plan box below, not a mark on the source"
   so the plan lands in an on-platform extended-text item the external grader can see, never on off-platform
   paper. Also keep the `stimulus_display` read framed as "read and note," not "underline the strongest fact."
5. **`gate_content_depth`**. The whole-essay `annotated_before_after` (BEFORE + AFTER inline, 220-char floor)
   is the longest slot in the course. Satisfy: model the PLAN + the two framing moves, not a full essay
   transcript (§2 move 9); include both the literal words BEFORE and AFTER.
6. **`gate_bank_partition`**. Satisfy: build a whole SECOND essay-grade source set (opposing pair) on a
   different topic for Transfer, engineered to admit a defensible ordered thesis. Component types partition a
   short item; T7 must partition an entire source set. [REF]: congestion pricing taught, daylight saving
   transfer.
7. **`gate_grader_routing`**. T7 has the MOST production FRQs (five), so this gate checks the most surface
   area. Satisfy: give every `production_frq` a valid `rc.*` (plan reps rc.4trait, essays rc.staar/rc.ohio).
8. **`gate_define_before_use`**. T7 inherits the most jargon (thesis, controlling idea, SPO, counterclaim,
   synthesize; all appear in `_TECH_TERMS`). Satisfy: define all of them in plain words with a definitional
   cue inside a TEACH slot before first student-facing use. [REF] defines all five in teach card 1.
9. **`gate_model_sequence`**. Satisfy: include an `annotated_before_after` (with BEFORE + AFTER), a
   `predict_the_fix` with a non-empty `feedback` reveal, and a `diagnosis_frq` somewhere in the lesson.
10. **`gate_model_before_required`**. Satisfy: model the plan/diagnose moves before requiring them, and put
    the diagnosis checklist (named steps / frame / "Step 1 ...") IN the `diagnosis_frq` body. A blank
    "diagnose it" is rejected.
11. **`gate_discrimination_before_production`**. T7 has five production FRQs; the discrimination must precede
    the FIRST of them (`min(disc_idx) <= min(prod_idx)`). Satisfy: place the labeled Grade-C discrimination
    in SUPPORTED before any FRQ, and set `labeled_grade_c=True`.
12. **`gate_effect_size_honesty`**. T7 leans on the SRSD shell. Satisfy: never claim ES 1.14 / 1.02 or say
    the model "inherits SRSD's evidence"; cite the annotated worked example, forced response, and
    personalized feedback instead. Do NOT claim a coping-model effect: the async Model is a static annotated
    worked example, not a reconstructed near-peer coping model.
13. **`gate_mnemonic_status`**. Satisfy: set `provenance["mnemonic_status"] = "proposal"` for BUILD.
14. **`gate_shell_completeness`**. Satisfy: all five stages present and in order (baseline).
15. **`gate_calibration_discipline`**. Only bites if a `self_score` is included; if so it must PRECEDE the
    graded reveal, and no person-praise anywhere in any body/feedback. [REF] ships without a self_score, so it
    passes n/a; if you add whole-essay calibration (via a Type-5 style predict-then-reveal), keep the order.
16. **`gate_binding_integrity`**. Satisfy: the taught + transfer stimulus ids must actually exist in the
    banks (>=1 bound ref). T7 needs both its congestion source and its partitioned transfer source present.
17. **`gate_timeback_native`**. Satisfy: use only mapped slot kinds (all of T7's kinds are native and
    JSON-safe: stimulus, choice, extended-text).
18. **`gate_no_ambiguous_reference`**. Satisfy: any "the draft above / this version" must show its referent
    inline (a quoted example, a BEFORE/AFTER, or an option list).
19. **`gate_no_em_dash`**. Satisfy: commas/colons/parens only (house rule, baseline).

---

## Retrieval + item rules (LS feedback 2026-07)

These encode the 2026-07 learning-scientist pass as T7 authoring defaults so a fresh essay-assembly lesson clears the new gates by construction.

- **Cadence ceiling: FULL-ESSAY-BUILD tier, ceiling 4, checks at production milestones only** (`gate_check_cadence`). T7 assembles a whole essay, so its checks land at production milestones (the discrimination before the first FRQ, the predict-the-fix, the diagnosis), not after every card. A run of COUNTED teach cards (the two teach cards, the stimulus_display, the annotated before/after) may not exceed FOUR before a check. The whole-essay before/after counts as ONE worked example even though it is the longest slot in the course; never split it to pad the run. Tag any pure buy-in / orientation card `tag="buy_in"` so it counts 0. The "memorizable tool" tightening is LESS relevant here: T7 cues the owned sub-skills rather than introducing new named tools, so it will rarely trigger; if a card genuinely introduces a new memorizable device, tag it `tag="memorizable_tool"`.
- **Four options per discrimination, each a NAMED MISCONCEPTION** (`gate_structural_item`). The planned-opening-vs-no-plan discrimination carries exactly four choices; distractors are real no-plan openings (a fact-list with no position, a topic announcement with no context, an off-source personal story), never filler.
- **Diagnosis: the student ANSWERS the check, then improves** (`gate_self_answered_check`). The modeled diagnosis may pre-answer a PROVIDED flawed intro/conclusion (name that specimen and run the context / thesis / significance checklist on it), but MUST then hand the student an independent turn: name the missing moves and write one repair sentence for each. Never print a diagnosis that answers its own questions and stops.
- **No comma before "because"/"so" in a fill-in frame** (`gate_frame_comma`). Any side/reason fill-in in the SPO or a thesis frame drops the comma before because. Emit it with `claim_frame()` from `lesson_prompts` rather than hand-writing it.
- **Re-gloss the hard terms.** T7 inherits the most jargon (thesis, controlling idea, SPO, counterclaim, synthesize); `gate_define_before_use` already forces an in-lesson gloss for controlling idea, warrant, synthesis, and counterclaim. On a later-lesson re-introduction prefer a BRACKETED gloss right after the term (LS #9 style).
- **Stem wording (playbook-only, #7):** name the move directly ("Which opening shows a plan driving the essay?"), never a meta-phrasing.
- **Tone (playbook-only, #5 / Yeager):** state the standard up front; each per-choice reveal is process-level wise-feedback that names the MOVE, no person-praise, no compliment-sandwich (reinforces `gate_calibration_discipline`).
- **Pair a stand-alone improve-write with a `predict_the_fix`** where feasible (playbook-only, #4); T7's predict-the-fix on the no-plan draft pairs with the completion-problem planning rep.
- **Cross-lesson spacing (KH caveat, #3):** the in-lesson cadence gate is necessary but NOT sufficient; the BUILD move (and the sub-skills it assembles) must be retrieved again in later lessons and the transfer essay. That durability is a sequence-builder concern, not visible to this lesson's gates.

---

## 10. Keep it short

The instruction stays short even though the OUTPUT is a whole essay: the length lives in the student's
response, not the lesson prose [EXTRACT §1, §4].

- **Split Teach into two short cards** (terms + why-plan; then BUILD + the two framing moves) rather than one
  wall of text; each clears the 200-char floor without becoming a chapter [EXTRACT §1].
- **The plan-plus-framing-moves model shape is the primary length control**: never draft the full essay in
  the Model; the compact SPO carries the organizational load [EXTRACT §2].
- **Cue, do not re-teach**, the owned sub-skills; the fade ledger lets T7 be short because Types 1-6 already
  taught them [EXTRACT §1 move 3].
- **One before/after, one predict-the-fix, one discrimination**; do not stack multiple worked essays, the
  intrinsic load is already at ceiling [EXTRACT §2].
- **Scaffold at the PLAN unit, not the essay unit, at Supported**; short high-value planning reps, not a
  whole essay under scaffold [EXTRACT §3].
- **Do not re-model at Independent, and add no new teaching at Transfer** [EXTRACT §4, §5].
- Backward fading is also the efficient direction (about 6 minutes saved with no transfer loss in Renkl 2002;
  fading brief Claim 2), so the short design is also the better-learning design.

---

## 11. Honesty and copyright ledger

- **BUILD is a design proposal, not sourced** (`gate_mnemonic_status` = "proposal") [EXTRACT §8].
- **Discrimination-before-production is Grade C / UNVALIDATED for writing** [Framework Audit item 4]; the T7
  discrimination slot must carry `labeled_grade_c=True`.
- **No effect size from a delivery mode the element is not delivered in** (`gate_effect_size_honesty`); the
  async Model cites the annotated worked example, forced response, and personalized process feedback, not
  SRSD's live ES 1.14 and not a coping-model effect (the near-peer coping model does not transfer to static
  screen text, so it is not claimed) [EXTRACT §8; async-SRSD §2].
- **Scaffold fading in writing is a grounded extrapolation, not a proven writing result** [Framework Audit
  item 3]; fade the plan on demonstrated performance, and when unsure keep it one rung longer.
- **The device-to-function map is a design choice, not a study finding**, and must be flagged as such
  (function-over-form §Where the evidence is thin).
- **Research-brief caveats to respect:** Harris (2024) is paywalled, so the six SRSD success characteristics
  and the "results peak at stages 5-6" line are UNVERIFIED-as-cited (async-SRSD verification); rely on the
  WWC six-stage description and "independent performance is the goal stage" instead. Myhill's contextualized-
  grammar effect is small (0.21) and skewed to abler writers, so over-scaffold the framing moves for weaker
  writers (function-over-form §3).
- **Copyright:** all example prose (congestion-pricing / daylight-saving essays, SPO, intros, conclusions) is
  own-authored on public-issue topics; no third-party lesson text is reproduced. Cite external sources
  (Writing Next, WWC, Hayes and Flower, TWR, Renkl, Schunk/Hanson/Cox, Metcalfe, Panadero, Margulieux and
  Catrambone, Fearn and Farnan, Myhill, Kolln) by author/year; accessible URLs are in the four research
  briefs.

## 12. Corpus and research anchors used

- Internal extraction: `_phase2/extract_T7_BUILD.md` (archetype definition, per-stage moves, gate ranking,
  honesty ledger).
- Contract + reference: `pipeline/lesson_contract.py` (19 gates, 9 slot kinds, UNIT_LADDER,
  TYPE_CEILING_UNIT, LESSON_TYPES type 7 = essay-assembly / BUILD / proposal);
  `Lesson_Bank_G10/lesson_t7_essay_assembly.py` (passing reference, all 19 gates PASS).
- Research briefs (verified 2026-07-10): `_phase2/research_async-srsd.md` (async-valid SRSD subset,
  coping-model reconstruction, self-assessment scripts, statelessness limits);
  `_phase2/research_worked-example-fading.md` (fixed schedule, backward fade, completion problems, subgoal
  labels, seam-level adaptivity); `_phase2/research_feedback-as-teaching.md` (deliverable vs blocked feedback,
  predict-then-reveal, elaborated process-level reveals); `_phase2/research_function-over-form.md`
  (teach by function not form, bake structure-to-effect talk into the material).
