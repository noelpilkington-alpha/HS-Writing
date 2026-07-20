# Authoring Playbook: T2 Claim-Building (STAND, ceiling = sentence)

How to author a T2 lesson that teaches a student to STATE A DEFENSIBLE, PROMPT-RESPONSIVE
CLAIM at the sentence level, inside Timeback's hard delivery limits (display-only stimuli,
stateless isolated items, external-grader production, no human). Every move below is anchored
to the internal extraction or to a verified research claim. Citations use these short keys:

- EXTRACT = `_phase2/extract_T2_STAND.md` (internal corpus synthesis; itself anchored to KB, GATE, SPEC, BUILT)
- GATE = `pipeline/lesson_contract.py` (the 19 machine-enforced gates)
- SPEC = `G10_Model_Lesson_Specs.md`, TYPE 2 section
- BUILT = `Lesson_Bank_G10/lesson_t2_claim_building.py` (the QC-passing model lesson)
- R-SRSD = `_phase2/research_async-srsd.md`
- R-FADE = `_phase2/research_worked-example-fading.md`
- R-FDBK = `_phase2/research_feedback-as-teaching.md`
- R-FORM = `_phase2/research_function-over-form.md`

House rules honored throughout: own words only, no reproduced copyrighted lesson text, every
external source carries author/title/URL in the research files cited, and no em dashes.

---

## 1. Terminal deliverable and production ceiling

**Terminal deliverable:** ONE defensible, prompt-responsive claim sentence, scored by the
external grader on the Thesis/Purpose trait. The claim must do four jobs at once: take a clear
Stance, make an Assertion a reasonable reader could reject, attach an I-say reason via a
because/but/so hinge drawn from the sources, and answer "so what" by naming the stakes (SPEC
TYPE 2 target; BUILT target string; EXTRACT §1).

**Production ceiling = sentence. This is the archetype's signature constraint.**
`TYPE_CEILING_UNIT[2] = "sentence"` (GATE). Every scored `production_frq` must declare
`unit="sentence"`, and the `type_ceiling` gate REJECTS any scored production that climbs to
paragraph or essay (GATE `gate_type_ceiling`; BUILT: all four scored slots carry
`unit="sentence"`). The `unit_ladder` gate additionally requires the unit to be non-decreasing,
but for T2 that means it must hold flat at sentence, never climb (GATE `gate_unit_ladder`).
Rationale: element-interactivity says do not force the whole before the parts are fluent, and
part-task ordering puts claim control below paragraph and essay assembly (EXTRACT §1, citing
KB 1.1 / 3.2). Claim assembly is the part; T7 essay-assembly is the whole.

**Mnemonic STAND is a labeled PROPOSAL, not sourced.** `LESSON_TYPES[2]` status = "proposal"
(GATE); `gate_mnemonic_status` REJECTS any other declared status, and `gate_effect_size_honesty`
forbids claiming SRSD's live-enacted effect sizes (the 1.14 / 1.02 figures) for this async STAND
shell. STAND = Stance, Territory (the they-say answered), Assertion (arguable), Nuance
(agree-with-a-difference), Defensible (SPEC; BUILT; EXTRACT §1). The letters are an unvalidated
design bet, so provenance must say so, and the strategy earns its keep only when paired with
application, not as a name to memorize (R-SRSD §2: memorize-it survives but is "necessary but
low-value on its own," Harris 2024).

---

## 2. Per-stage authoring moves, worked-example shape, and stateless delivery

The lesson is the SRSD shell in order: Teach, Model, Supported, Independent, Transfer
(GATE `gate_shell_completeness`; the async-valid subset in R-SRSD §2 and §6). The async subset
that survives with no human and no state is: teach/background as display plus discrimination,
model as an annotated before/after worked example plus a compare item, memorize as the mnemonic,
supported as a decreasing-support item sequence with an in-item self-assessment script, and
independent/transfer as extended-text scored by the grader (R-SRSD §6).

### TEACH (SRSD Discuss It + Develop Background Knowledge)

**Moves:**
- Card 1 defines the dense vocabulary this archetype cannot avoid, each in plain words with a
  definitional cue: thesis, controlling idea, arguable claim, they-say, I-say, the three
  stances, the because/but/so hinge, and the "so what" test (BUILT card 1). This is not polish.
  `gate_define_before_use` keys on `they-say/I-say`, `controlling idea`, `thesis`,
  `arguable claim`, and `because/but/so` and REJECTS the lesson if any appears in student-facing
  text without a TEACH definition first (GATE `_TECH_TERMS`; Engelmann faultless communication,
  EXTRACT §2). T2 is the most term-dense archetype in the set, so this gate bites here first.
- Card 2 defines STAND letter by letter with a RIGHT and a WRONG example per letter (BUILT card
  2). Showing the boundary of each move, not just its name, is DI faultless communication at the
  strategy level (EXTRACT §2).
- State the one named strategy in a single sentence plus its mnemonic, and give the specific
  product goal up front ("write a defensible claim that takes a stance and answers so what"),
  never "do your best" (EXTRACT §2, citing KB Rules 1 and 4; strategy instruction and specific
  product goals are the high-leverage levers, R-SRSD §2 reporting Writing Next: strategies 0.82,
  product goals 0.70).

**Two distinctive pre-production slots live in TEACH:**
- A source display: read-and-note the they-say for each side. It must NOT tell the student to
  mark up the source, because Timeback stimuli are display-only with JavaScript stripped
  (GATE `gate_no_source_markup`; BUILT stimulus body uses "read and note"; EXTRACT §2).
- A discrimination WARM-UP `choice` item ("which of these is a claim, and which is just a gut
  reaction?"), placed BEFORE any model. This REPLACES the old pre-model unscored freewrite. The
  freewrite is cut because it only elicited a gut opinion that no stateless item downstream can
  revisit or reshape, so it did no instructional work; a discrimination warm-up primes the same
  claim-vs-opinion distinction while staying a scorable, revisitable stateless item that feeds
  the fact/claim/opinion sort. It carries the discrimination `labeled_grade_c=True` flag and an
  elaborated feedback reveal, not an `rc.*` grader config (it is a `choice`, not a
  `production_frq`).

**Worked-example shape here:** none yet. TEACH names, defines, and primes; the worked example
lives in MODEL (R-FADE fit-to-SRSD: Teach states the move plus its subgoal labels; Model is
rung 0 of the fade).

**Stateless/async delivery:** all TEACH slots render as `stimulus` (teach cards, source
display) plus two `choice` items (the claim-vs-opinion warm-up and the fact/claim/opinion sort)
(GATE `KIND_QTI`). Nothing requires memory of a prior item. Each `choice` is self-contained: the
text under judgment is printed in its own stem, never a look-back (GATE
`gate_no_prior_work_reference`).

### MODEL (SRSD Model It, modality-corrected to async)

**Moves:** the async model (GATE `gate_model_sequence`): a clean annotated before/after PLUS a
predict-the-fix, with a student-generated diagnosis somewhere in the lesson. There is NO human
persona, no near-peer self-talk, and no false-start-as-monologue. The common error and its
repair live entirely as LABELED author-voice annotations on the exemplar (labels like "problem:
states a fact no one disputes" / "fix: pick a side and give a reason"), and the predict-the-fix
stem makes the student do the diagnosing (EXTRACT §2, citing KB3 §1). This is defensible because
the WORKED-EXAMPLE effect is robust and screen-validated: observing a strong-vs-weak example and
then comparing and evaluating it is the active ingredient (R-SRSD §3a, Braaksma; R-FADE). The
social self-efficacy mechanism behind a live coping model does not transfer to static screen
text, so we do NOT reconstruct a near-peer voice and do NOT claim the coping-model effect size
here. Deliver it as a fixed annotated before/after plus predict-the-fix (Principle A).

**Worked-example shape (archetype-specific):** the before/after is a FACT-that-cannot-be-a-claim
turning INTO an arguable stanced claim with a "so what" stakes beat, STAND-annotated inline
(BUILT `annotated_before_after`).
- BEFORE: a checkable fact ("A typical American public school runs about 180 days a year") shown
  to FAIL STAND (no Stance, no rejectable Assertion, no so-what).
- AFTER: a claim that picks a side, states a rejectable Assertion, attaches a because-hinge (the
  I-say reason), and names the stakes (the so-what), with each part labeled S / A / because /
  so-what INLINE, not in a separate legend. Split-attention theory puts the labels on the
  example, not in a detached key (EXTRACT §2, citing KB 1.1; subgoal labels printed in the
  worked example are the most stateless-compatible upgrade, R-FADE Claim 5 / Margulieux and
  Catrambone 2016).
- `gate_content_depth` REQUIRES a literal "BEFORE" and "AFTER" in the slot body and a 220-char
  floor (GATE `_DEPTH_FLOOR`).

The predict-the-fix presents a fact-masquerading-as-thesis and asks for its single biggest
problem, with the reveal in the feedback field (BUILT: draft "The summer break lasts about two
to three months," correct answer = it states a fact no one disputes; traps B/C/D are length,
citation, and numerals). `gate_model_sequence` REJECTS a predict-the-fix with no feedback
reveal. The predict-then-reveal structure is itself evidence-based: committing to a prediction
before the correction is the mechanism, not wasted motion (R-FDBK §1.6, Metcalfe errorful
generation and hypercorrection), and the reveal must explain WHY, not just flash the answer
(R-FDBK §1.2, Shute: elaboration beats verification).

**Stateless/async delivery:** `annotated_before_after` renders as `stimulus`; `predict_the_fix`
renders as `choice` with a feedback-block reveal (GATE `KIND_QTI`). Both are self-contained: the
draft under diagnosis is quoted inline, so `gate_no_ambiguous_reference` is satisfied ("this
draft" shows its text). No prior response is referenced.

**Keep it short:** ONE before/after pair and ONE predict-the-fix carry the whole model. Do NOT
model all three stances separately; SPEC is explicit that TSIS stance variants live as
DISCRIMINATION items, not extra production rungs (SPEC fade ladder; EXTRACT §2).

### SUPPORTED (SRSD Support It, guided practice with a fading scaffold)

**Moves:**
- The distinctive two-part discrimination completes here. The fact-vs-arguable-claim-vs-
  ungrounded-opinion sort runs in TEACH; the SUPPORTED discrimination is the "so what" minimal
  pair: two claims taking the SAME stance that differ on exactly one move, the stakes beat
  (BUILT SUPPORTED discrimination; SPEC discrimination C; EXTRACT §2). Both discrimination slots
  set `labeled_grade_c=True`, because discriminate-before-produce is UNVALIDATED and must be
  labeled a design bet; `gate_discrimination_before_production` REJECTS unlabeled discrimination
  or any production that precedes it (GATE; EXTRACT §2 citing KB3 §4).
- The guided production is ONE claim sentence WITH A FRAME PROVIDED: "The US should ___ [Stance +
  rejectable Assertion], because ___ [I-say reason, a because/but/so hinge from the sources],
  which matters because ___ [so what]" (BUILT SUPPORTED `production_frq`, `unit="sentence"`).
  The frame is the novice scaffold. The completion is TWR sentence-combining anchored to
  function, which has the best quantitative warrant among syntactic-practice methods (R-FORM
  headline and Claim 1, Writing Next sentence-combining d = 0.50). The product goal names all
  four required moves explicitly (EXTRACT §2, KB Rule 4).
- The MODELED diagnosis lives here: the STAND four-point self-check is first run step by step on
  a flawed claim ("A longer school year would be good") with a repair frame for each failed
  check, THEN the student runs the same checklist on a fresh claim of their own (BUILT
  `diagnosis_frq`). `gate_model_before_required` REJECTS a diagnosis not preceded by a model and
  not scaffolded with frames, a checklist, or named steps (GATE).

**Worked-example shape:** the diagnosis is a WORKED CHECKLIST run. Each STAND letter becomes a
yes/no check with a matching repair frame ("Step 3, I-say/because: is there a reason? No; add one
with 'because ___'."). This is the completion-problem rung between the full worked example
(MODEL) and independent performance. A completion problem is the ideal stateless unit because ALL
the context the learner needs is printed in the stem, not carried from a prior item (R-FADE
Claim 3, van Merrienboer; the key structural fit with Timeback isolation). The self-question
script the student runs on the draft is the async substitute for a tutor walking a student
through the checklist, and scripts drive more self-regulation than a bare rubric (R-FDBK §1.7 and
R-SRSD §5c, Panadero 2012).

**Stateless/async delivery:** `discrimination` and the checklist run as `choice`; the guided
production and the diagnosis run as `extended-text` to the grader (GATE `KIND_QTI`). The self-
check runs INSIDE the same slot on the claim the student just wrote THERE, never "your claim from
Step 5," which QTI statelessness forbids (GATE `gate_no_prior_work_reference`, regex `_PRIOR_WORK`;
EXTRACT §2). Statelessness collapses all self-monitoring to within a single item (R-SRSD §5d).

### INDEPENDENT (SRSD Independent Performance, scaffold removed)

**Moves:** the SAME claim sentence, NO frame (BUILT INDEPENDENT `production_frq`,
`unit="sentence"`, no fill-in template in the body). The product goal still names all four
required moves so the student can self-monitor. A STAND self-check is embedded in the prompt
("S, did I pick a side? A, could a reasonable reader reject it? because, did I give a reason?
so-what, did I name why it matters? If any No, revise before you submit"), which builds the
self-regulation half of SRSD as an in-item self-assessment script (EXTRACT §2, KB 2.5 / KB3 §1;
R-SRSD §5c; R-FDBK §1.7). Metacognitive prompts must be task-specific, tied to the exact genre
move, not generic "did you check your work" prompts (R-SRSD §5b, Guo 2022).

**Worked-example shape:** none. This is the fade point. The frame present in SUPPORTED is removed
here (R-FADE synthesis fit-to-SRSD: Independent is a deeper completion / removal of scaffold;
Renkl 2002 fixed fade). Because you cannot read prior responses within a lesson, ANY expertise
adaptation would have to happen at the seam between lessons, not inside an item. Score-based
between-lesson routing to a more-worked or less-worked variant is UNBUILT and assumed-pending-eng;
it is NOT a delivered capability, so this INDEPENDENT slot must stand on its own as the frameless
fade rung with no routing (R-FADE Claims 6 and 7 motivate it; expertise reversal is real and
mis-fitted scaffolding backfires, Kyun, Kalyuga and Sweller 2013).

**Stateless/async delivery:** one `extended-text` production to the grader, routed to a valid
`rc.*` config (BUILT uses `rc.ohio`; GATE `gate_grader_routing`). The self-check is baked into the
prompt, not a separate slot, and operates only on this slot's own response.

### TRANSFER (near transfer, bank-partitioned)

**Moves:** run the identical STAND move on a NEW topic the student has not practiced. BUILT
teaches on `longer_school_year` and transfers to `congestion_pricing`. `gate_bank_partition`
REJECTS the lesson if the TRANSFER content bank overlaps any MODEL/SUPPORTED bank, so transfer is
genuine near transfer, not recall of the same material (GATE; EXTRACT §2 citing KB 1.5). TRANSFER
carries its own read-and-note source display plus one claim-sentence production with the same
four-move product goal.

**Worked-example shape:** none. TRANSFER re-invokes the already-modeled STAND move on fresh
content; the schema, not the topic, carries over. Do not re-teach STAND, only re-invoke it.
Ceiling stays at sentence (BUILT TRANSFER `unit="sentence"`).

**Cross-lesson spacing note (not enforced by single-lesson gates):** durability needs STAND to
REAPPEAR as a retrieval hook inside later evidence-integration (T3) and essay-assembly (T7)
lessons (EXTRACT §2, KB Rule 6 and KB 1.3 / 1.4 spacing and retrieval). Track this in the unit
map; the per-lesson gates cannot see it.

---

## 3. Feedback-as-teaching within the stateless boundary

The coaching loop where a student drafts, gets feedback, revises the SAME draft, and gets
feedback again CANNOT be reproduced across items: no item can show item B the student's response
to item A, and a retake starts blank (R-FDBK §2.2, the blocked list). So feedback-as-teaching is
re-engineered from "iterate on your own draft" into two moves that survive statelessness (R-FDBK
§2.3, the precise line).

**Deliverable in T2:**
- Predict-the-fix then reveal, inside ONE item (the MODEL slot). Show the fact-as-thesis, ask for
  its single biggest problem, then reveal the fix and the WHY in the same item's feedback-block.
  Errorful generation plus corrective feedback beats error-free study, and the reveal must
  surface the reasoning, not just the answer (R-FDBK §1.6 Metcalfe; §1.2 Shute elaboration over
  verification). The BUILT predict-the-fix does exactly this and its feedback names the process
  move (turn the fact into Stance + Assertion + because-hinge + so-what).
- The two discrimination items (fact/claim/opinion, then the so-what minimal pair) are stateless
  strong-vs-weak and correct-vs-incorrect comparisons on PROVIDED text; both texts are printed in
  the stem, so isolation is a non-issue (R-FDBK §1.5 and §2.1; R-SRSD §3a compare-two-models).
  For the so-what minimal pair, both claims take the same stance and differ on exactly one move,
  which targets the structural principle rather than surface features.
- Elaborated, process-level reveals, not "correct/incorrect." Every reveal names the MOVE and
  gives a reusable rule, because process and self-regulation feedback teach and bare verification
  does not (R-FDBK §1.1 Hattie and Timperley; §1.2 Shute).
- The in-item STAND self-assessment script the student runs on their own single fresh submission
  (SUPPORTED diagnosis, INDEPENDENT self-check). Self-assessment against explicit criteria is a
  large, stateless writing effect (R-FDBK §1.3, Graham, Hebert and Harris self-feedback ~0.62,
  above automated ~0.38), and a step-by-step script beats a bare rubric for self-regulation
  (R-FDBK §1.7 Panadero). It can judge the student's one submission but cannot compare it to a
  prior draft.
- The external grader is the "conferencing" engine on the final production, targeting deep
  features (Thesis/Purpose), preceded by the self-assessment script (R-FDBK §2.1; R-SRSD §4b
  W-Pal / AWE).

**Blocked in T2 (flag honestly, design around):**
- Feedback on an evolving draft across turns, and iterative revise-and-recheck on the student's
  own text (R-FDBK §2.2 items 1-2). We can flag errors on a provided text, never on the
  student's live draft across items.
- Any reveal that references the student's earlier answer or score ("last time you...",
  "compared to your draft in step 2"). Enforced by `gate_no_prior_work_reference` (GATE).
- Dialogic back-and-forth Socratic feedback, and longitudinal progress feedback ("your thesis
  score is trending up"), which needs stored state and is the weakest-evidence practice anyway
  (R-FDBK §2.2 items 5-6).

Person-praise is banned in every body and feedback field: `gate_calibration_discipline` rejects
"great job" and similar (praise effect ~0.12; GATE regex; R-FDBK §1.1). If a `self_score` slot is
used, it must precede a graded reveal (predict THEN reveal); the BUILT lesson uses an embedded
script rather than a scored `self_score` slot, which also satisfies the gate.

---

## 4. Worked-example fading without statefulness

Fading normally adapts to the learner's running performance, which needs memory. The core
learning benefit does NOT depend on real-time adaptivity: the original fading studies used a
FIXED pre-scripted schedule and it worked (R-FADE Claim 1, Renkl 2002). So author the fade as a
designed SEQUENCE of self-contained items, not a within-item adaptive loop (R-FADE synthesis
point 1).

**The T2 fade ladder (all sentence-tier, since the ceiling is a sentence):**
1. MODEL: the fully worked, STAND-annotated before/after with subgoal labels on the example.
   This is rung 0 (R-FADE fit-to-SRSD; subgoal labels are static text that survive display-only
   rendering, Claim 5).
2. SUPPORTED discrimination: the so-what minimal pair, a scored principle-naming choice item, not
   a free "explain yourself" prompt (R-FADE Claim 4; and avoid the generic self-explanation that
   the Barbieri 2023 meta-analysis flags as harmful when redundant).
3. SUPPORTED guided production: the FRAME-provided claim. This is the completion problem: the
   student completes the because/but/so hinge and the so-what while the Stance frame carries the
   context in-stem (R-FADE Claim 3; van Merrienboer completion strategy).
4. SUPPORTED diagnosis: the modeled-then-student STAND checklist, a completion rung between the
   full worked example and independent performance (EXTRACT §2, KB 1.2 expertise reversal).
5. INDEPENDENT: the frameless claim, scaffold removed (R-FADE fixed fade).
6. TRANSFER: full claim production on a bank-partitioned topic, externally graded, ending the
   ladder in full production (R-FADE synthesis point 7). Any use of its score to route the next
   lesson is UNBUILT / assumed-pending-eng, not part of what this lesson delivers.

**Fade BACKWARD:** when you remove worked steps, remove the LAST step first and keep the earlier
steps visible as built-in scaffolding on the same item (R-FADE Claim 2, Renkl 2002 backward fade
produced the significant far-transfer gain and saved study time). For the claim, the frame keeps
Stance modeled first and asks the student to generate the later moves (the because-hinge and the
so-what), which is exactly what the BUILT SUPPORTED frame does: "The US should ___ [given shape],
because ___ [student], which matters because ___ [student]."

**Use the SAME functional labels (S / A / because / so-what) across the whole ladder** so the
labels are the through-line a stateless sequence otherwise lacks (R-FADE Claim 5). BUILT does
this: the STAND letters annotate the MODEL, name the moves in both discriminations, structure the
diagnosis checklist, and headline the INDEPENDENT self-check.

**Any adaptivity would live at the seam, never inside an item, and is UNBUILT.** In principle a
short first-step diagnostic or the grader's production score could route the student to a more-
worked or less-worked lesson variant (R-FADE Claims 6 and 7), but between-lesson score-based
routing is an assumed-pending-eng capability, NOT delivered. The lesson therefore ships as a
complete, self-sufficient FIXED-FADE sequence that requires ZERO routing to function; adaptive
variant-selection is contingent on the platform actually supporting next-lesson routing on a
grader score. No item ever reads another item's response, so isolation holds regardless.

---

## 5. Function-over-form device instruction (directly relevant to T2)

T2 is a function-over-form archetype, because the because/but/so hinge that completes the I-say IS
the canonical function-anchored syntactic move. Teach it by the JOB it does, never as a form to
label (R-FORM headline: isolated grammar has null-to-negative effects; function-plus-application
beats definition, Fearn and Farnan 2005; sentence-combining is the mechanism with the best effect
sizes, Writing Next d = 0.50).

**The two TWR moves that operationalize claim-building in T2 (taught by FUNCTION):**
- because / but / so builds the claim AND its reason: because supplies the reason that makes the
  claim defensible, but supplies the contrast or concession, so supplies the consequence
  (R-FORM Claim 7, TWR because/but/so; the "N" of STAND, Nuance / agree-with-a-difference, is the
  "but" concession move). Anchor each connector to the reasoning job it does, not its part of
  speech. This is the hinge that turns a bare stance into a stance-plus-reason.
- Sentence expansion via the who / what / when / where / why / how questions makes a VAGUE claim
  SPECIFIC: "school should change" answers who/what/why to become "US public high schools should
  add twenty instructional days because concentrated summer learning loss widens the achievement
  gap." Teach it as the job of naming the specific actor, action, and stakes, not as adding words
  (R-FORM function-over-form; the specificity the grader scores on Thesis/Purpose). A specific
  claim is a scored requirement, so expansion is a targeted revision move, not decoration.

**Gate note (mechanical substrate is app-owned, gated not re-taught):** the mechanical craft of
sentence combining is AlphaWrite-owned G3-8 and EGUMPP-owned conventions G3-10; T2 GATES these as
retrieval-verified prerequisites and APPLIES them in context, teaching only the rhetorical USE
(build the reason, make the claim specific). It never re-teaches sentence mechanics from scratch.

**Where it applies in T2:**
- The because/but/so hinge maps one-to-one onto reasoning moves: because gives the reason, but
  gives the contrast or concession, so gives the consequence (R-FORM Claim 7, TWR because/but/so;
  the "N" of STAND, Nuance / agree-with-a-difference, is the "but" concession move). Anchor each
  connector to its function, not its part of speech.
- The AFTER in the MODEL and the frame in SUPPORTED show the same idea WITH the hinge doing its
  job, and state in the annotation WHY the reader experiences the intended effect (the because-
  clause supplies the reason that makes the claim defensible). This bakes in the "structure-to-
  effect" talk that, in the research, only a knowledgeable teacher supplied; with no teacher it
  MUST live in the worked example and the answer rationales or the effect evaporates (R-FORM
  synthesis, the single most important design implication; Myhill 2012 mediation).
- Discrimination items follow the "does the word do the job here?" pattern: the correct option is
  the claim whose because-hinge actually supplies a reason and stakes; distractors are the right
  grammatical shape doing the wrong job (a claim that stops at Stance, a fact, a bare opinion), as
  in the BUILT so-what minimal pair (R-FORM Claim 2 Fearn and Farnan slot pattern; R-FORM design
  moves for Supported).
- The grader scores whether the named FUNCTION was executed (did the claim reach stakes; is the
  reason tied to the claim), not whether the student can name a subordinate clause (R-FORM design
  move for Independent).

**Honest limits (flag under the provenance rule):** the function map is a teachable DESIGN CHOICE,
not a finding lifted verbatim; because/but/so to reason/contrast/consequence is strongly attested,
but looser device-to-function claims should not be overclaimed (R-FORM honest-gaps). The Myhill
effect was small (~0.20) and skewed to abler writers, so over-scaffold the hinge for weaker
writers rather than leaving the function implicit (R-FORM caveats). Do NOT build "which of these
is the appositive" style label-identification items; that is the approach the evidence rejects
(R-FORM synthesis).

---

## 6. The 19 gates ranked by sharpest risk for T2, and how to satisfy each

Ranked by how hard the gate bites THIS archetype (EXTRACT §3).

1. **type_ceiling + unit_ladder (the T2 signature).** Ceiling is "sentence"; every scored
   production must declare `unit="sentence"` and must never climb to paragraph or essay. SATISFY:
   set `unit="sentence"` on all four scored slots (guided, diagnosis-adjacent production,
   independent, transfer) and never write "write a paragraph." A claim lesson that drifts into a
   paragraph is rejected (GATE `TYPE_CEILING_UNIT[2]`).
2. **define_before_use.** The most jargon-dense archetype: thesis, controlling idea, arguable
   claim, they-say/I-say, because/but/so all trip `_TECH_TERMS`. SATISFY: define each in a TEACH
   card with a definitional cue (means, is when, is a, that is) BEFORE first use (BUILT card 1).
3. **discrimination_before_production.** The claim-vs-opinion warm-up and the fact/claim/opinion
   sort must be labeled Grade-C and precede production. SATISFY: put the warm-up and the sort in
   TEACH with `labeled_grade_c=True`, both before any scored production (GATE; BUILT slot order).
4. **model_sequence.** Annotated before/after (fact to stanced claim) + predict-the-fix WITH a
   feedback reveal + a diagnosis slot, all present. SATISFY: include all three; the predict-the-
   fix `feedback` field must be non-empty (GATE `gate_model_sequence`).
5. **model_before_required.** The STAND self-check diagnosis must be modeled on a flawed claim
   and frame-scaffolded before the student runs it. SATISFY: run the four-point check on
   "A longer school year would be good" with a repair frame per step, THEN ask for the student's
   fresh claim; keep the checklist and frames in the `diagnosis_frq` body (GATE; BUILT diagnosis).
6. **mnemonic_status + effect_size_honesty.** STAND must be declared "proposal"; no claiming
   SRSD's live ES. SATISFY: `provenance={"mnemonic_status": "proposal", ...}`; never write "ES 1.14"
   or "inherits SRSD's evidence" (GATE regexes).
7. **content_depth.** Teach cards (200 chars), before/after (220 chars, with literal BEFORE and
   AFTER), and prompts must be finished student-facing text, not stubs. SATISFY: write them out;
   ensure the `annotated_before_after` body contains both the words BEFORE and AFTER (GATE
   `_DEPTH_FLOOR`).
8. **grader_routing.** Every `production_frq` needs a valid `rc.*` config. SATISFY: give the four
   scored production slots (guided, diagnosis, independent, transfer) an `rc.*` such as `rc.ohio`
   (GATE `RUBRIC_CONFIGS`; BUILT). The claim-vs-opinion warm-up is a `choice`, so it needs no
   grader config.
9. **calibration_discipline.** Self-check present, no person-praise; any `self_score` precedes a
   graded reveal. SATISFY: use the embedded STAND self-check; scrub "great job / nice work" from
   every body and feedback (GATE regex).
10. **no_prior_work_reference.** The in-prompt self-check must operate on the response written in
    that SAME slot, never a look-back to earlier work. SATISFY: phrase as "run the check on your
    claim" inside the slot, never "your claim from Step 5" (GATE `_PRIOR_WORK`).
11. **bank_partition.** TRANSFER bank must differ from taught banks. SATISFY: teach on one topic,
    transfer on another (BUILT: longer_school_year -> congestion_pricing); tag every MODEL,
    SUPPORTED, and TRANSFER slot with its `bank` (GATE).
12. **no_source_markup.** Source displays say read-and-note, not mark up. SATISFY: use "read and
    note the they-say," never "underline / highlight / annotate the source" (GATE `_MARKUP_VERBS`).
13. **no_ambiguous_reference.** Every "this claim / this draft" shows its text inline. SATISFY:
    quote the draft under diagnosis inline in every predict/discrimination/diagnosis slot (GATE).
14-19. **shell_completeness, binding_integrity, timeback_native, no_em_dash (plus the two ladder
    gates already at rank 1).** Standing gates satisfied by the shell shape (all five stages in
    order), at least one real bank ref (the two `stimulus_display` slots bind to real stimulus
    ids), native choice/extended-text/stimulus kinds only, and comma/colon/paren punctuation with
    no em or en dashes (GATE).

---

## Retrieval + item rules (LS feedback 2026-07)

These encode the 2026-07 learning-scientist pass as T2 authoring defaults, so a fresh claim lesson clears the new gates by construction.

- **Cadence ceiling: CONCEPT tier, ceiling 3** (`gate_check_cadence`). T2 is a concept-teaching type, so a run of COUNTED teach cards may not exceed THREE before a check (a `discrimination`, `predict_the_fix`, or `self_score`). The STAND-annotated before/after counts as ONE worked example even if chunked; do not split it into separate teach cards to pad the run. Tag any pure buy-in / motivation card `tag="buy_in"` so it counts 0. TIGHTEN to 2 right after the card that introduces a named memorizable tool (the STAND mnemonic, the because/but/so hinge): tag that card `tag="memorizable_tool"` and put the claim-vs-opinion warm-up right behind it.
- **Four options per discrimination, each a NAMED MISCONCEPTION** (`gate_structural_item`). The claim-vs-opinion warm-up and the so-what minimal pair each carry exactly four choices, and every distractor is a real wrong move a G9 writer makes (a checkable fact, a bare gut opinion, a stance with no stakes), never filler like "none of the above."
- **Diagnosis: the student ANSWERS the STAND check, then improves** (`gate_self_answered_check`). The modeled STAND self-check may pre-answer a PROVIDED weak claim (name that specimen, e.g. "A longer school year would be good"), but it MUST then hand the student an independent turn: run the same four checks on a fresh claim of their own. Never print a diagnosis that answers its own "? No," questions and stops there.
- **No comma before "because"/"so" in a fill-in frame** (`gate_frame_comma`). The SUPPORTED claim frame reads "... ______ [Stance] because ______ [reason] ..." with NO comma before because (that comma reads as a punctuation model the student copies). Emit it with `claim_frame()` from `lesson_prompts` instead of hand-writing it.
- **Re-gloss the hard terms.** If the lesson uses controlling idea, warrant, synthesis, or counterclaim, `gate_define_before_use` already requires an in-lesson gloss (they sit in `_TECH_TERMS`). On a later-lesson re-introduction prefer a BRACKETED gloss right after the term (LS #9 style).
- **Stem wording (playbook-only, #7):** name the move directly ("Which sentence takes a side a reader could reject?"), never a meta-phrasing ("which one fits the verb").
- **Tone (playbook-only, #5 / Yeager):** state the high standard up front; each per-choice reveal is wise-feedback that names the MOVE, with no person-praise and no compliment-sandwich.
- **Pair a stand-alone improve-write with a `predict_the_fix`** where feasible (playbook-only, #4).
- **Cross-lesson spacing (KH caveat, #3):** the in-lesson cadence gate is necessary but NOT sufficient; STAND must recur as a retrieval hook inside later T3 and T7 lessons. That durability is a sequence-builder concern, not something this lesson's gates can see.

---

## 7. Keep it short

T2 is a moderate-load, sentence-ceiling archetype; the lesson must feel short and worked-example-
first (R-SRSD short-lesson requirement; R-FADE worked-example-first). Concrete economies, all from
EXTRACT:
- TWO teach cards only. Define terms in-line with the right/wrong pair doing double duty
  (definition plus boundary), not a separate glossary. Hit the 200-char `content_depth` floor
  without bloating past it.
- ONE before/after and ONE predict-the-fix carry the whole MODEL.
- The three stances are practiced by DISCRIMINATION, never by three separate guided writes (SPEC).
- Because the ceiling is a sentence, every production is one sentence; the frame does the
  scaffolding so the prompt can be brief.
- The self-check is baked INTO the production prompt, not a separate slot.
- TRANSFER is one new source pair and one claim sentence: re-invoke STAND, do not re-teach it.

Build recipe in one line (EXTRACT §5): TEACH = two cards + read-and-note source + claim-vs-opinion
warm-up + fact/claim/opinion discrimination; MODEL = one STAND-annotated fact-to-claim before/after
+ one predict-the-fix with reveal; SUPPORTED = so-what minimal-pair discrimination (Grade-C) +
frame-provided one-sentence claim + modeled-then-student STAND self-check; INDEPENDENT = one
frameless claim with an embedded self-check; TRANSFER = bank-partitioned new source + one claim.
Everything scored stays at `unit="sentence"`; STAND stays a labeled proposal; no em dashes.

---

## Blocked-by-Timeback ledger (honest flags)

- Live coping-model think-aloud / near-peer self-talk: BLOCKED, and NOT reconstructed as a human
  persona. Static screen text cannot carry the social self-efficacy mechanism, so we replace it
  with an annotated before/after worked example (labeled author-voice error and fix annotations)
  plus the predict-the-fix (Principle A; R-FADE worked-example effect; no coping-model effect
  size claimed).
- Iterate-on-your-own-draft coaching loop: BLOCKED across items. Re-engineered as predict-then-
  reveal on provided text plus an in-item self-assessment script on one fresh submission (R-FDBK
  §2.2, §2.3).
- Within-lesson adaptive fading: BLOCKED. Only FIXED fading ships, and it ships as a complete,
  self-sufficient sequence requiring zero routing. Between-lesson score-based routing to a more/
  less-worked variant is UNBUILT / assumed-pending-eng, contingent on the platform supporting
  next-lesson routing on a grader score, NOT a delivered capability (R-FADE Claims 6-7).
- Cross-session goals and longitudinal self-monitoring/graphing: BLOCKED. The goal is baked into
  the product-goal line of each prompt; self-monitoring is collapsed to a within-item self-check
  (R-SRSD §5d).
- Student markup of the source: BLOCKED (display-only, JS stripped). Read-and-note framing only
  (GATE `gate_no_source_markup`).
- Real-time teacher differentiation and relationship-based motivation: BLOCKED and NOT fully
  rebuildable statelessly; front-load strategy instruction and lean on the annotated worked
  example plus specific product goals rather than any human coping voice (Principle A; R-SRSD §6
  "what we lose").
