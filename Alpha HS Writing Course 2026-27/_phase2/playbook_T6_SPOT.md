# Authoring Playbook: T6 Editing-in-Context (SPOT)

> **Archetype:** Type 6, editing-in-context. **Mnemonic:** SPOT = Scan, Pinpoint the error type, weigh Options, Test the fix (the fix must correct the error AND preserve the writer's meaning, or it is a new error). **Status:** `LESSON_TYPES[6] = ("editing-in-context", "SPOT", "proposal")`; SPOT is a design proposal, not a sourced mnemonic, and must be declared `"proposal"`. **What it teaches:** spot and repair conventions and syntax faults in composed text (applied, not isolated grammar drill), on two tiers, mechanics first then style.

This entry synthesizes the internal extraction (`extract_T6_SPOT.md`) with four verified research briefs (`research_async-srsd.md`, `research_worked-example-fading.md`, `research_feedback-as-teaching.md`, `research_function-over-form.md`). Every move is grounded in one of those and cited. All prose is own-words; no copyrighted lesson text is reproduced; no em dashes.

---

## 0. The evidence posture that governs everything about T6 (read this first)

T6 is the developmentally LOWEST-load type and the one LEAST suited to SRSD. Its warrant is NOT the SRSD strategy effect. It rests on exactly two evidence-based routes, and the whole design must ride on them:

- **Sentence-combining / expansion, about d = 0.50** (Graham & Perin, Writing Next, 2007, verified verbatim: "Sentence Combining (Effect Size = 0.50)"; 0.46 for weaker writers). This is the mechanism with the best quantitative warrant for building syntactic maturity. URL: https://www.thewritingrevolution.org/wp-content/uploads/2017/05/WritingNext.pdf
- **Grammar taught IN CONTEXT, not in isolation.** Isolated/traditional grammar instruction had a small but statistically significant NEGATIVE effect on writing quality across the ability range (Writing Next, verified: "surprisingly, this effect was negative ... statistically significant"; individual negatives, e.g. Saddler & Graham -0.42, Anderson -1.40). Andrews et al. (2006) and Hillocks (1986) independently corroborate. The correct rule is "no isolated grammar drills as a path to better writing," never "never address conventions." URLs: https://bera-journals.onlinelibrary.wiley.com/doi/abs/10.1080/01411920500401997 ; https://files.eric.ed.gov/fulltext/ED265552.pdf

Consequence: T6 must never borrow SRSD's ES 1.14 / 1.02 language, and every taught edit must sit on real composed text. Two gates enforce this (`effect_size_honesty`, `binding_integrity`). This is the single discipline that most defines T6.

---

## 1. Terminal deliverable and production ceiling

**Terminal deliverable:** a short, self-contained SENTENCE-level constructed-response repair. The student is shown one flawed sentence (quoted inline), runs SPOT, and rewrites it so that (a) the convention/syntax fault is fixed, (b) the sentence is correctly bounded and complete, and (c) the writer's original meaning is unchanged. Scored by the external grader against a valid `rc.*` config (rc.staar for the STAAR short-constructed-response sub-type; extract GAP #21, modifier repair).

**Production ceiling:** SENTENCE. `TYPE_CEILING_UNIT[6] = "sentence"` (confirmed in `pipeline/lesson_contract.py`). This is a hard, T6-defining wall: an editing lesson cannot demand a paragraph or essay before the essay-assembly type (T7) has taught composition. Gates `type_ceiling` + `unit_ladder` reject any production above a sentence. This encodes parts-before-whole ordering (Kirschner & Hendrick element-interactivity; TWR sentence-first).

---

## 2. SRSD stage-by-stage authoring (moves, worked-example shape, stateless delivery)

The constant shell is Teach -> Model -> Supported -> Independent -> Transfer. For T6 the shell is the SHORTEST in the pack (Section 7). Every stage below states the exact moves, the worked-example shape, and how it ships on display-only stimuli + stateless choice/extended-text items + external grader.

### TEACH

**Moves.**
1. Present SPOT as a runnable four-step routine (Scan, Pinpoint the error type, weigh Options, Test the fix), and make the Test step carry the weight: a fix that is grammatical but changes meaning is a NEW error, not a repair. Then split the routine into a mechanics tier ("is it correct?") and, above it, a style tier ("is it precise, varied, register-appropriate?"). This "grammar as a choice with an effect" framing (not "label the form") is exactly what the function-over-form evidence supports: Fearn & Farnan (2005) got significantly better holistic writing from teaching what a structure DOES vs defining it (verified from EJ787964); Myhill et al. (2012) got a small positive RCT effect from grammar-as-choice (e = 0.21, Jones et al. 2013). URLs: https://files.eric.ed.gov/fulltext/EJ787964.pdf ; https://link.springer.com/article/10.1007/s11145-012-9416-1
2. Front-load a DEFINITIONS card for every convention term BEFORE any item names or repairs that error, because naming the error IS the Pinpoint (P) step. Define complete sentence, fragment, run-on, comma splice, misplaced modifier, and appositive in plain words with a one-line worked micro-example each. ("appositive" is explicitly in the `define_before_use` term list.)
3. State the evidence-honesty flag inside the teaching content itself: tell the student (and the build) plainly that this lesson's support is sentence-combining (about 0.50) and in-context grammar, NOT the SRSD strategy result.
4. Orient the student to the test demand: conventions is scored on its own trait and, on the real tests, is gated behind development (STAAR Conventions 0-2 gated; MCAS 0-3).

**Worked-example shape.** None yet; TEACH is expository plus definitions. Function-first framing per device: name the FUNCTION, then show the form doing that job (function-over-form synthesis, Section 5).

**Stateless / async delivery.** All static display + a couple of retrieval-practice choice items ("match the error name to its example"). The async-SRSD brief confirms Develop/activate background knowledge and Discuss-it port directly to display stimulus plus discrimination items; "discussion" becomes worked contrasts and choice questions, not a live conversation. Because grammar-as-choice gains rode on a knowledgeable teacher's structure-to-effect talk that we do not have, that talk must be BAKED INTO the worked examples and answer rationales (function-over-form design implication, verified as sound).

### MODEL

**Moves (the 4-mechanism async sequence, never a passive read).**
1. Clean annotated before/after (an unambiguous worked example).
2. Interactive predict-the-fix (student diagnoses BEFORE the reveal).
3. Student-generated diagnosis somewhere in the lesson (write what was wrong, how it was fixed, why it is stronger).
Gate `model_sequence` requires `annotated_before_after` + `predict_the_fix` + a `diagnosis_frq`; `model_before_required` requires modeling before any required diagnosis. Do NOT claim SRSD's ES for this (`effect_size_honesty`).

**Worked-example shape (T6-specific: a meaning-preservation contrast, not a right/wrong contrast).** The before/after shows TWO grammatical edits of ONE flawed sentence drawn from the bound passage:
- **Flawed sentence** with the error type named inline (a comma splice / a run-on / a misplaced modifier).
- **Edit that CHANGES the meaning** (grammatically correct, but REJECT): annotate exactly what it quietly severed or invented, labeled "correct grammar, WRONG meaning."
- **Edit that corrects the error AND preserves the meaning** (ACCEPT): annotate why the boundary is now correct and the writer's chain survives.
- **Takeaway line:** both edits are grammatical; only the meaning-preserving one passes the Test step.
This differs from every higher-load type, whose worked example contrasts weak-move vs strong-move. In T6 both versions are grammatical, so the discriminating dimension is meaning-preservation. The error and its fix are carried as LABELED author-voice annotations placed ON the exemplar sentence (labels like "problem: the phrase describes the wrong noun" / "fix: move the phrase next to the word it modifies"), never in a separate legend (split-attention effect) and never as a near-peer persona's inner monologue or a simulated student false start. Static screen text cannot reproduce the social-modeling / self-efficacy mechanism a live coping model relies on, so T6 does not stage one and does not claim its effect; the async adaptation is an annotated worked example plus predict-the-fix, which IS screen-validated (errorful generation). Gate `content_depth` requires a literal BEFORE and AFTER inline.

**Stateless / async delivery.**
- The before/after is fixed text with labeled author-voice annotations, not a live think-aloud and not a near-peer persona monologue (text on a screen cannot carry the human coping-model mechanism). Predict-the-fix is a stateless select item that reveals WHY the meaning-changing distractor fails even though it is grammatical. This is the errorful-generation / hypercorrection mechanism: committing to a prediction before the reveal IS the learning mechanism, and it needs no cross-item memory (Metcalfe 2017, verified). URL: https://www.columbia.edu/cu/psychology/metcalfe/PDFs/Learning%20from%20errorsAnnual%20ReviewMetcalfe2016.pdf
- CRITICAL Timeback boundary: deliver "spot the error" as a plain CHOICE item, NEVER as an instruction to mark up the passage. Author the Scan/Pinpoint move by presenting the candidate sentences or spans as discrete choice OPTIONS (for example, four numbered sentences from the passage; the student selects the one that contains the error). Hottext (select-within-passage) is NOT among the confirmed native interaction kinds (only stimulus/choice/extended-text are confirmed); do NOT design on it unless the platform explicitly confirms hottext as a native interaction. Note the degradation: a plain choice list cannot make the student scan a full running passage to LOCATE the fault the way hottext would; it hands them a pre-segmented candidate set, which lowers the search demand. Author around this by keeping the candidate set plausible and matched, and by using read-and-note framing on display slots. Stimuli are display-only (JS stripped); the student cannot underline, circle, or highlight. Gate `no_source_markup` blocks "underline/circle/highlight/annotate the source." This bites T6 harder than any other type because "mark the errors" is the intuitive editing verb.

### SUPPORTED

**Moves.**
1. Discrimination FIRST, labeled Grade-C (`discrimination_before_production`, `labeled_grade_c=True`). For T6 this bet is MORE defensible than in generative types, because selected-response recognition IS the actual test format, but it is still labeled and still A/B-testable (framework audit: discrimination-before-production is UNVALIDATED, keep and label).
2. Include a NO-CHANGE option as the correct answer on at least one item: teach "do not fix what is not broken" (over-editing correct text is a real error mode).
3. Target run-ons, fragments, and comma splices FIRST; sentence-boundary errors are the ones most likely to fail the conventions gate. Then finer moves.
4. Add ONE style-tier select above mechanics: the cleanest style move here is sentence COMBINING applied in context (pick the rewrite that combines two choppy or redundant grammatical sentences from the passage into one tighter, more mature sentence) or the most precise / formal rewrite of an already-grammatical sentence. Style still passes the Test step (it sharpens meaning and cuts redundancy, it does not drift). This APPLIES the app-owned combining craft; it does not re-teach it (see Section 5 boundary).
5. Build every choice item to the faultless-slot spec: minimal pairs differing on EXACTLY the error dimension; distractors plausible and matched on length/topic/position (no covert co-variation with correctness); one interaction type (select) per step.
6. Model the diagnosis on a broken fix BEFORE handing the student a self-contained diagnosis, and scaffold it with a numbered checklist (`model_before_required`; a bare "diagnose this" fails).

**Worked-example shape / fading.** This is the fade rung. Deliver support as COMPLETION items that carry their own context in the stem (the partial repair is printed, so the item is self-sufficient and isolation-safe: van Merrienboer et al. 2002, the key structural fit). Fade BACKWARD: blank the LAST move first, keep earlier worked moves visible in the same item as built-in scaffolding (Renkl et al. 2002, verified: backward fade uniquely produced far-transfer, partial eta-squared = .27, and saved study time). URLs: https://www.sciencedirect.com/science/article/pii/S0959475201000202 ; https://www.davidlewisphd.com/courses/EDD8121/readings/2002-Renkl_et_al.pdf

**Stateless / async delivery.** Author the scaffold as a DECREASING-support SEQUENCE of isolated items: select -> select-then-produce -> produce-in-context (fixed fade, no prior-response memory needed; the fixed-schedule fade is validated, adaptivity is an increment on top). Self-explanation is delivered as a SCORED discrimination item ("which rhetorical move / why does this fix work?"), targeting the STRUCTURAL principle, never a free "explain what you did" prompt (Barbieri et al. 2023 flag redundant generic self-explanation as a negative moderator, beta = -0.24). Use consistent SUBGOAL LABELS across the whole ladder (the same functional labels), because static labels survive display-only rendering and give the stateless sequence a through-line (Margulieux & Catrambone 2016). URLs: https://danamillercotto.com/uploads/4/7/7/2/47725475/barbieri_et_al__2023__we_meta-analysis.pdf ; https://bpb-us-e1.wpmucdn.com/sites.gatech.edu/dist/b/1555/files/2020/09/MargulieuxandCatrambone2016.pdf . The distributed-practice bonus for T6: the sentence moves taught in Types 1-5 (boundaries, because/but/so, appositives, combining, precise word choice) recur here as in-context editing, so SUPPORTED doubles as spaced retrieval; fade is performance-triggered from the shared fade ledger, not by lesson number.

### INDEPENDENT

**Moves.**
1. A SHORT constructed-response at the SENTENCE unit only: revise one flawed sentence (a modifier-repair-with-meaning-preservation item, STAAR SCR sub-type, extract GAP #21). Must declare `unit="sentence"` and must NOT climb (`type_ceiling` + `unit_ladder`).
2. Make the prompt fully self-contained: quote the flawed sentence inline; never say "revise the sentence you wrote" or "look back at your answer" (QTI is stateless; a retake starts blank).
3. Give an explicit multi-part product goal (opening phrase attaches to the right word; the sentence is complete and correctly bounded; original meaning unchanged; change only what you must) and route to a real `rc.*` config. Product goals carry ES about 0.70 (Writing Next); ban "do your best." Have the prompt tell the student to run SPOT (self-instruction cue).

**Worked-example shape / fading.** A deeper completion rung: more of the repair blanked than in SUPPORTED, still with the earlier worked context visible (backward fade continues into Independent).

**Stateless / async delivery.** The external grader plays the "conferencing" role on this one fresh submission. Precede the submit with a self-assessment SCRIPT the student runs on their own draft ("Did I fix the boundary? Is the sentence complete? Is the meaning unchanged? Did I change only what I must?"), because scripts drive self-regulation more than rubrics and self-assessment against criteria is a large writing effect (about 0.62), close to teacher feedback and above automated feedback (Graham, Hebert & Harris 2015; Panadero et al. 2012, both verified). The script lives IN the item, so it needs no memory. URLs: https://digitalcommons.unl.edu/specedfacpub/222/ ; https://repositorio.uam.es/handle/10486/710139

### TRANSFER

**Moves.**
1. Transfer to a NEW, bank-partitioned passage: same move (sentence repair with meaning preserved), unpracticed topic. The TRANSFER slot must carry a content-bank tag that differs from every taught (MODEL/SUPPORTED) bank (`bank_partition`; DI hard partition), so the transfer is genuine, not recall of the same passage.
2. Hold the sentence ceiling: transfer production stays at `unit="sentence"`; do not escalate the unit.

**Worked-example shape / fading.** Full (near-independent) production on the new passage: the end state of every fade ladder (complete example -> completion -> full problem).

**Stateless / async delivery.** Extended-text scored by the `rc.*` grader. This lesson ships as a complete, self-sufficient FIXED-FADE sequence that requires ZERO routing to function. Any between-lesson, score-based routing (using the transfer score or a first-step-style diagnostic to send the student to a more-worked or less-worked next-lesson variant) is an UNBUILT / assumed-pending-eng capability, NOT a delivered one: it is contingent on the platform actually supporting next-lesson routing on a grader score. IF that seam is ever built, it would recover expertise-reversal adaptivity WITHOUT reading another item's response (Kalyuga 2007 first-step method; Salden et al. 2010) and would respect statelessness because the decision happens in the sequencing layer, not inside any item. Until then, treat it as absent.

---

## 3. Feedback-as-teaching HERE, within the stateless boundary

**Deliverable for T6 (build these):**
- Elaborated reveals, not bare "correct/incorrect." Every predict-the-fix and select reveal must name the MOVE (process level) and give a reusable one-line rule, because process and self-regulation feedback teach and self/task-only feedback is weak (Hattie & Timperley 2007; Shute 2008, both verified). URLs: https://journals.sagepub.com/doi/10.3102/003465430298487 ; https://andymatuschak.org/files/papers/Shute%20-%202008%20-%20Focus%20on%20Formative%20Feedback.pdf
- Predict-the-fix then reveal WHY, inside ONE item (errorful generation / hypercorrection; elaboration beats verification). This is T6's core teaching engine and it is fully stateless.
- Erroneous-model autopsy and strong/weak twin items on PROVIDED text: since the object judged is fixed and printed in the stem, statelessness is a non-issue. For weaker students, name/point to WHERE the fault is rather than making them locate it first (Grosse & Renkl, via Booth et al. 2015). URL: https://files.eric.ed.gov/fulltext/ED566953.pdf
- Rubric/script self-score of the single fresh submission (the Independent script above).
- Grader feedback on the fresh SCR as the "reveal."

**Blocked by statelessness for T6 (do NOT design around):**
- Iterative revise-and-recheck on the student's OWN draft across turns. The classic editing loop (student edits, gets feedback, re-edits the same text, gets feedback again) cannot be reproduced turn to turn; item B cannot see item A's response and a retake starts blank. The written-corrective-feedback in-draft accuracy gains (Lim & Renandya 2020) are earned by revising a flagged live draft, which we cannot watch. URL: https://files.eric.ed.gov/fulltext/EJ1275821.pdf
- Any feedback that references a prior answer or prior score ("last time you", "compared to your earlier fix").
- Adaptive fading tuned to this student's running performance (fixed fade only; between-lesson score-based routing is an UNBUILT / assumed-pending-eng seam per Section 2 TRANSFER, not a delivered fallback).
- Dialogic/Socratic back-and-forth, and longitudinal progress monitoring (also the weakest-evidence practice).

**The precise line for T6:** feedback teaches when the thing being judged is fixed and self-contained inside one item (a provided flawed sentence, or one fresh SCR scored once), and it teaches by (a) making the student commit to a fix before the reveal and (b) revealing the reasoning, not a bare verdict. It breaks the moment the design needs to carry the student's own words/score from one item to the next. The re-engineered form (predict/judge on provided text, then reveal; self-assess one submission) is not a weak substitute; it is itself evidence-based.

---

## 4. Worked-example fading without statefulness

- **Treat the fade as a designed item SEQUENCE, not a within-item adaptive loop.** The fixed-schedule fade is empirically validated and needs no prior-response memory, so it drops straight into stateless QTI (Renkl et al. 2002).
- **Every rung is a COMPLETION item that prints its own partial repair in the stem** (van Merrienboer et al. 2002). This is the key structural fit between fading and Timeback isolation: the item is self-sufficient by construction.
- **Fade BACKWARD** (blank the last move first; keep earlier worked moves visible in the same item as scaffolding). This lets a single isolated item still "scaffold" without referencing anything external (Renkl et al. 2002, backward fade uniquely drove far transfer).
- **Consistent subgoal labels across the whole ladder** are static text, survive display-only rendering, and give the stateless sequence its through-line (Margulieux & Catrambone 2016).
- **Principle-naming self-explanation as SCORED discrimination items,** not free "explain yourself" prompts (Atkinson, Renkl & Merrill 2003 for the benefit; Barbieri et al. 2023 for the caution).
- **Adaptivity at the SEAMS is UNBUILT / assumed-pending-eng:** the fixed-schedule fade is the delivered mechanism and the lesson is complete without any routing. Between-lesson routing (an external-grader production score or a first-step-style diagnostic selecting the next rung/lesson variant; Kalyuga 2007; Salden et al. 2010) is contingent on the platform supporting next-lesson routing on a grader score; it is not a delivered capability. No item reads another item's response either way.
- The T6 fade concretely: MODEL = the fully worked meaning-preservation before/after (rung 0) + subgoal labels. SUPPORTED = backward-faded completion select (last move blank) + scored principle-discrimination + NO-CHANGE item. INDEPENDENT = deeper completion SCR (more blanked). TRANSFER = full sentence repair on a partitioned passage, externally graded.

---

## 5. Function-over-form device instruction (where it applies here)

It applies directly, because T6 repairs are syntactic. Teach each device by the JOB it does, not by its label, and make the student USE it in composing:
- **Sentence boundaries via because / but / so** (reason / contrast / consequence) as the reasoning move, per the TWR framing (cite the method, not a single page). This is the cleanest, best-attested function map. URL: https://www.thewritingrevolution.org/twr_resource/because-but-so/
- **Sentence combining = concision + syntactic maturity, APPLIED in context.** T6's central style-tier move: take two or three choppy or redundant sentences already sitting in the bound passage and combine them into one tighter sentence that says the same thing with less repetition and a more mature structure. Teach it by the JOB (fix the choppiness / cut the redundancy), never as an isolated combining drill. This is the move with the best quantitative warrant for the type (sentence combining, about 0.50; Writing Next), and it belongs on real composed text.
- **Appositive = name and credential a source (adds authority).**
- **Modifier / phrase = supply context and narrow scope; attach it to the right word** (the misplaced-modifier repair is the Independent SCR).
- Discrimination items follow the Fearn & Farnan "does the structure do the job HERE?" pattern: the correct option performs the named function; distractors are the right grammatical FORM doing the WRONG job.

**CRITICAL app-ownership boundary (make this explicit in the build).** The mechanical conventions substrate and the sentence-combining CRAFT are APP-OWNED, not T6-owned: EGUMPP owns conventions across G3-10 and AlphaWrite owns sentence-combining craft across G3-8. T6 does NOT re-teach either from scratch. It GATES them as retrieval-gated prerequisites (the student has already met combining and the relevant conventions in the app) and APPLIES them in context, teaching only the rhetorical USE (repair the choppy/redundant sentence to improve concision and syntactic maturity here, in this passage). Any slot that drifts into isolated grammar or a decontextualized combining exercise violates this boundary and the in-context-grammar evidence; every combining or convention move must ride on the bound passage and turn on function.

Two honest guardrails from the research: (1) the exact one-to-one device-to-function map is a DESIGN CHOICE we impose for clarity, not a finding lifted from a study, and must be flagged under the provenance rule; pick the cleanest exemplar function per device and do not overclaim ("relative clause = consequence" is loose; because/but/so is solid). (2) Do NOT ship "which of these is the appositive?" identification items as a route to better writing; isolated form-labeling has null-to-negative effects. Every device item must ride on the bound passage and turn on function.

---

## 6. The lesson_contract gates that bite hardest for T6 (ranked) and how to satisfy them

Of the 19 machine gates in `lesson_contract.py`, ranked most-severe first for editing-in-context:

1. **`effect_size_honesty`** (sharpest). T6 is the least-SRSD type, so the temptation to borrow SRSD's strength is strongest and is explicitly forbidden. SATISFY: cite only sentence-combining (about 0.50) + in-context grammar; never write "ES 1.14" or "inherits SRSD."
2. **`no_source_markup`.** "Spot the errors / underline the run-on / mark up the passage" is the natural editing verb and it is banned (display-only stimuli). SATISFY: every scan/pinpoint is a plain CHOICE item (candidate sentences/spans presented as discrete options); do not author on hottext unless the platform confirms it as a native interaction; display slots say read-and-note.
3. **`define_before_use`.** Editing needs a dense error vocabulary and Pinpoint requires naming. "appositive" is explicitly in `_TECH_TERMS`. SATISFY: define fragment, run-on, comma splice, modifier, appositive, complete sentence in a TEACH card before any item uses them.
4. **`type_ceiling` + `unit_ladder`.** The sentence ceiling (`TYPE_CEILING_UNIT[6]="sentence"`) is a hard T6 wall; the ladder must be non-decreasing and within the ceiling. SATISFY: every scored production declares `unit="sentence"`; never author a paragraph/essay production.
5. **`content_depth`.** The meaning-preservation worked example must show a literal BEFORE and AFTER inline; no slot may be a stub. The "no isolated grammar" pressure makes thin decontextualized items tempting. SATISFY: meet the floors (teach_card >= 200, annotated_before_after >= 220 with BEFORE+AFTER, predict_the_fix >= 120, productions >= 90) with real content, then stop.
6. **`discrimination_before_production`.** A labeled Grade-C discrimination must precede production; easy to forget on the SR-heavy editing type. SATISFY: place an explicit `labeled_grade_c=True` discrimination slot before any production.
7. **`no_prior_work_reference` / `no_ambiguous_reference`.** "Revise your sentence from before" and "fix the sentence above" are natural editing phrasings and both are banned (stateless, isolated; every referent inline). SATISFY: quote every target sentence in-stem; no back-references.
8. **`model_sequence` / `model_before_required`.** The diagnosis must be modeled and scaffolded before it is required; a bare "diagnose this edit" fails. SATISFY: annotated_before_after + predict_the_fix (with non-empty feedback) + a scaffolded diagnosis_frq, in that order.

Lower-friction but still mandatory: **`grader_routing`** (SCR needs a valid rc.* config), **`bank_partition`** (transfer passage differs from taught banks), **`binding_integrity`** (bind at least one real bank stimulus; every edit rides on it), **`mnemonic_status`** (SPOT declared `"proposal"`), **`calibration_discipline`** (single-trait conventions binary; no person-praise, praise about the person is near 0.09-0.14), **`timeback_native`** (one interaction type per step), **`shell_completeness`**, and **`no_em_dash`** (house rule).

---

## Retrieval + item rules (LS feedback 2026-07)

These encode the 2026-07 learning-scientist pass as T6 authoring defaults so a fresh editing-in-context lesson clears the new gates by construction.

- **Cadence ceiling: CONCEPT tier, ceiling 3** (`gate_check_cadence`). T6 is a concept-teaching type, but it is also the lowest-load, SHORTEST type, so it will rarely approach the ceiling: a run of COUNTED teach cards may not exceed THREE before a check (a `discrimination`, `predict_the_fix`, or `self_score`). The meaning-preservation before/after counts as ONE worked example; do not split it. Tag any pure buy-in card `tag="buy_in"` so it counts 0. TIGHTEN to 2 right after the card that names the memorizable tool (the SPOT routine, or a named error type at the Pinpoint step): tag that card `tag="memorizable_tool"` and put the first select discrimination right behind it.
- **Four options per discrimination, each a NAMED MISCONCEPTION** (`gate_structural_item`). Each select item carries exactly four choices; distractors are real editing misreads (the correct-grammar-but-meaning-changed edit, an over-edit of already-correct text, the wrong error type named), and at least one item keeps a NO-CHANGE option as the key. No filler options.
- **Diagnosis: the student ANSWERS the check, then improves** (`gate_self_answered_check`). The modeled diagnosis may pre-answer a PROVIDED broken fix (name that specimen and why the fix changed meaning), but MUST then hand the student an independent turn: run the numbered SPOT checklist on a fresh flawed sentence of their own. Never print a diagnosis that answers itself and stops.
- **No comma before "because"/"so" in a fill-in frame** (`gate_frame_comma`). Any side/reason fill-in ("... stronger because ______") drops the comma before because. Emit it with `claim_frame()` from `lesson_prompts` rather than hand-writing it. (This is separate from teaching because/but/so as a sentence-boundary tool, which is fine in prose.)
- **Re-gloss the hard terms.** T6 defines a dense error vocabulary already; if the lesson uses controlling idea, warrant, synthesis, or counterclaim, `gate_define_before_use` forces an in-lesson gloss. On a later-lesson re-introduction prefer a BRACKETED gloss right after the term (LS #9 style).
- **Stem wording (playbook-only, #7):** name the move directly ("Which rewrite fixes the run-on and keeps the meaning?"), never a meta-phrasing ("which fits the verb").
- **Tone (playbook-only, #5 / Yeager):** state the standard up front; each per-choice reveal is wise-feedback that names the MOVE and gives a one-line reusable rule, no person-praise, no compliment-sandwich.
- **Pair a stand-alone improve-write with a `predict_the_fix`** where feasible (playbook-only, #4); the sentence-repair SCR pairs naturally with the meaning-preservation predict-the-fix.
- **Cross-lesson spacing (KH caveat, #3):** the in-lesson cadence gate is necessary but NOT sufficient; the sentence moves T6 repairs recur across the course as in-context editing (T6 SUPPORTED already doubles as spaced retrieval). That durability is a sequence-builder concern, not visible to this lesson's gates.

---

## 7. Keep-it-short note (T6 must be the SHORTEST type)

- It is the lowest-load type: scaffold depth is shallowest and fade is FAST. Do not stage extra rungs the way analysis (T4) does. Match support to expertise.
- ONE passage carries every taught edit (no new reading load per item; respect the 1050-1185L Lexile cap).
- One interaction type per step: each SUPPORTED item is a single select, not a compound task.
- Do not over-explain a low-load type; redundant explanation harms once the material is intelligible on its own (redundancy effect). Keep teach cards tight.
- Treat the content-depth floors as a MINIMUM, not a license to pad: meet the floor with real content, then stop.

---

## 8. Anti-pattern kill-list (do NOT)

- Isolated grammar worksheets or decontextualized error-ID (negative effect). Every item rides on the bound passage.
- Claiming or implying SRSD's ES 1.14 / "inherits SRSD" for this async, SR-driven type.
- Telling the student to underline/circle/highlight/annotate the passage.
- A right-vs-wrong worked example. The T6 contrast is grammatical-but-meaning-changing vs correct-and-meaning-preserving.
- Any production above a sentence.
- Referencing the student's own earlier sentence/draft, or a dangling "the sentence above."
- A blank "diagnose it" with no modeled check and no checklist.
- Free "explain what you did" self-explanation (redundant generic prompts hurt); prompt for the structural PRINCIPLE via a scored choice item instead.
- Person-praise ("nice work") in any feedback.
- "Which of these is the appositive?" as a route to better writing (form-labeling, negative effect).

---

## 9. What is honestly BLOCKED by Timeback for T6

- The natural editing coaching loop (edit -> feedback -> re-edit the SAME text -> feedback) cannot run across items; stateless, isolated QTI, retake starts blank. Re-engineered as predict-the-fix-on-provided-text + self-assess-one-submission.
- Student markup/highlight/annotate of a display-only stimulus is impossible; all spotting is a plain CHOICE item (hottext / select-within-passage is unconfirmed as native, so it is not relied on). Degradation noted: choice hands the student a pre-segmented candidate set instead of a full-passage scan.
- True within-lesson adaptive fading needs state; only fixed fading ships. Between-lesson routing seams are an UNBUILT / assumed-pending-eng capability (contingent on the platform supporting next-lesson routing on a grader score), so the lesson is authored to be complete and self-sufficient with zero routing.
- Longitudinal self-monitoring / progress graphing and history-based self-reinforcement need state; collapsed to a within-item self-check script and criterion-referenced reinforcement.
- Real-time teacher differentiation and the grammar-as-choice "structure-to-effect" discussion (which mediated Myhill's gains) cannot be delivered live; they must be baked into worked examples and answer rationales, and weaker writers over-scaffolded.

---

## 10. Source anchor index

- **Internal:** `extract_T6_SPOT.md` (Type 6 principles P1-P22, worked-example shape, gate ranking, kill-list); `pipeline/lesson_contract.py` (19 gates; `TYPE_CEILING_UNIT[6]="sentence"`; `_DEPTH_FLOOR`; `_TECH_TERMS`; `LESSON_TYPES[6]=("editing-in-context","SPOT","proposal")`); Instructional_Design_KB (Rules 1,3,4,5,6,7,10; CLT effects); G10_Model_Lesson_Specs (Type 6 spec, GAP #21 SCR, GAP #43 style tier); Lesson_Bank_G10 reference lesson (highways passage).
- **Sentence-combining / in-context grammar:** Graham & Perin, Writing Next (2007) https://www.thewritingrevolution.org/wp-content/uploads/2017/05/WritingNext.pdf ; Andrews et al. (2006) https://bera-journals.onlinelibrary.wiley.com/doi/abs/10.1080/01411920500401997 ; Hillocks (1986) https://files.eric.ed.gov/fulltext/ED265552.pdf ; Saddler & Graham (2005) https://eric.ed.gov/?id=EJ688034
- **Function-over-form:** Fearn & Farnan (2005) https://files.eric.ed.gov/fulltext/EJ787964.pdf ; Myhill et al. (2012) https://eric.ed.gov/?id=EJ959614 ; Jones, Myhill & Bailey (2013) https://link.springer.com/article/10.1007/s11145-012-9416-1 ; TWR because/but/so https://www.thewritingrevolution.org/twr_resource/because-but-so/ ; Kolln & Gray, Rhetorical Grammar https://www.pearson.com/en-us/subject-catalog/p/rhetorical-grammar-grammatical-choices-rhetorical-effects/P200000002254
- **Worked-example fading:** Renkl, Atkinson, Maier & Staley (2002) https://www.davidlewisphd.com/courses/EDD8121/readings/2002-Renkl_et_al.pdf ; van Merrienboer et al. (2002) https://www.sciencedirect.com/science/article/pii/S0959475201000202 ; Atkinson, Renkl & Merrill (2003) https://eric.ed.gov/?id=EJ678596 ; Margulieux & Catrambone (2016) https://bpb-us-e1.wpmucdn.com/sites.gatech.edu/dist/b/1555/files/2020/09/MargulieuxandCatrambone2016.pdf ; Barbieri et al. (2023) https://danamillercotto.com/uploads/4/7/7/2/47725475/barbieri_et_al__2023__we_meta-analysis.pdf ; Kalyuga (2007) https://www.uky.edu/~gmswan3/EDC608/Kalyuga2007_Article_ExpertiseReversalEffectAndItsI.pdf ; Kyun, Kalyuga & Sweller (2013) https://eric.ed.gov/?id=EJ1011878 ; Salden et al. (2010) https://www.jstor.org/stable/23372797
- **Feedback-as-teaching:** Hattie & Timperley (2007) https://journals.sagepub.com/doi/10.3102/003465430298487 ; Shute (2008) https://andymatuschak.org/files/papers/Shute%20-%202008%20-%20Focus%20on%20Formative%20Feedback.pdf ; Graham, Hebert & Harris (2015) https://digitalcommons.unl.edu/specedfacpub/222/ ; Lim & Renandya (2020) https://files.eric.ed.gov/fulltext/EJ1275821.pdf ; Booth et al. (2015) https://files.eric.ed.gov/fulltext/ED566953.pdf ; Metcalfe (2017) https://www.columbia.edu/cu/psychology/metcalfe/PDFs/Learning%20from%20errorsAnnual%20ReviewMetcalfe2016.pdf ; Panadero et al. (2012) https://repositorio.uam.es/handle/10486/710139
- **Async-SRSD / modeling:** Harris (2024) https://link.springer.com/article/10.1007/s10648-024-09921-x ; WWC SRSD (2017) https://ies.ed.gov/ncee/wwc/Docs/InterventionReports/wwc_srsd_111417.pdf ; WWC Secondary Writing Practice Guide (2016) https://ies.ed.gov/ncee/wwc/PracticeGuide/22 ; Schunk, Hanson & Cox (1987) https://files.eric.ed.gov/fulltext/ED278499.pdf ; Braaksma et al. https://l1research.org/article/view/215

Verification note: two async-SRSD claims were flagged in the source brief as UNVERIFIED-as-cited (the "results peak at stages 5-6" assertion and the "0.48 SD self-regulation added value" figure); neither is used in this entry. The device-to-function map is a flagged design choice, not a study finding.
