# Authoring Playbook: T4 Text-Dependent Analysis (DEW, ceiling = paragraph)

**Archetype:** T4 text-dependent-analysis. Mnemonic **DEW = Device -> Effect -> Warrant**.
**Core move taught:** analyze an author's choice by naming the choice (Device), saying what it does to the reader (Effect), then reaching significance (Warrant, the "so what" that ties the effect to the author's purpose).
**Reference implementation that passes all 19 gates:** `Lesson_Bank_G10/lesson_t4_analysis.py` (Kate Chopin, "The Story of an Hour", 1894, public domain; transfer to a US-federal weather-forecasting explanatory text).

This entry is written in own words. Every move is grounded in either the internal extraction (`_phase2/extract_T4_DEW.md`, which cites the KB, the 10 decision rules, `G10_Model_Lesson_Specs.md`, and `lesson_contract.py`) or a verified external research claim. External claims carry an author/year and an accessible URL. No copyrighted lesson text is reproduced. No em dashes.

---

## 1. Terminal deliverable and production ceiling

**Terminal deliverable:** one full analytical **paragraph** on a taught text in which the student names an authorial choice, explains its effect on the reader, and reaches a warrant (why that effect serves the author's purpose). All three DEW elements are required and the paragraph is scored by the external rubric grader.

**Production ceiling: paragraph.** This is enforced: `TYPE_CEILING_UNIT[4] = "paragraph"` and `gate_type_ceiling` rejects any scored production that declares `unit="essay"` (extract T4-11, T4-14; `lesson_contract.py`). Analysis does not reach the whole-essay tier (that is T7). The scored top-band move is **W**, the significance step, which is the documented 4-to-5 lift / AP Sophistication point (extract T4-3, GAP #22).

**Why this archetype is the hardest to author.** Analysis is the highest-intrinsic-load move in the course (extract "Why this archetype is the hardest"; KB element-interactivity ranking). At the same time the instinct every analysis teacher reaches for, "mark up the passage, underline the device, annotate the shift," is physically impossible on Timeback because stimuli are display-only and JS is stripped (`gate_no_source_markup`). T4 is therefore a workaround for a delivery constraint that fights its native pedagogy, which is why the extraction prescribes a thorough worked example plus one extra support rung by default. Author that worked example as a few SHORT chunks (BEFORE, then AFTER split by D/E/W), not one long block: length is not a virtue and a long example raises load, so chunk it and keep each chunk tight.

---

## 2. Per-SRSD-stage authoring (moves, worked-example shape, stateless/async delivery)

The async-valid subset of SRSD is the spine here: TEACH/background and Discuss survive as display + choice items; MODEL is reconstructed as an annotated before/after worked example (labeled author-voice error annotations, no near-peer persona) plus a compare-models choice item; SUPPORT is reconstructed as a faded item sequence plus the external grader; INDEPENDENT/TRANSFER is extended-text scored by the grader (research_async-srsd.md Section 6; Braaksma 2006 https://l1research.org/article/view/215 ; Schunk, Hanson & Cox 1987 https://files.eric.ed.gov/fulltext/ED278499.pdf ; IES/WWC Rec 1 Strong https://ies.ed.gov/ncee/wwc/PracticeGuide/22 ).

### TEACH (Develop Background Knowledge + Discuss It)

**Moves.**
- Define the three-way distinction first: **summary vs paraphrase vs analysis.** State the trap in plain words: on an analysis task a correct summary still sits in the low band because it never says what the author is DOING or why (extract T4-1). This is the number-one misread the type scores against.
- Teach DEW one letter at a time, each with a right AND a wrong example: Device = the specific choice you can point to (not "good description"); Effect = what the choice does to the reader (not a label like "this is imagery"); Warrant = why the effect serves the author's purpose and how you know (not stopping at "it feels hopeful") (extract T4-2).
- Name W as the scored top-band move up front: tell the student most writers stall at E, and reaching W is the lift into the top band (extract T4-3). Making the product goal visible before production is a specific-product-goals move (Writing Next, product goals ES 0.70, https://www.thewritingrevolution.org/wp-content/uploads/2017/05/WritingNext.pdf ).
- Use read-and-note framing on the display, never mark-the-source imperatives: "read once for what happens, then reread and keep ONE choice in mind" (extract T4-4).

**Worked-example shape at Teach:** short right/wrong pairs per DEW letter (a correct move beside the plausible-but-wrong reflex). This pre-trains the discrimination the SUPPORTED stage will test.

**Stateless/async delivery:** a display stimulus (the plain-words definitions and DEW letters) plus retrieval-style choice items that check the target concept ("Which of these is analysis, not summary?"). No state, no human, no markup. This is the async form of SRSD's Discuss stage: the "discussion" of what makes writing effective becomes worked contrasts and choice questions (research_async-srsd.md Section 2).

### MODEL (four-mechanism async sequence, NOT a passive-read think-aloud)

The modality correction governs: no near-peer coping model or fake-student self-talk is staged (static screen text cannot carry the social-modeling mechanism), and no slot may claim SRSD's live-enacted effect size (extract MODEL header; `gate_effect_size_honesty`). What survives text is the fixed worked example, forced response, and self-explanation (research_async-srsd.md Section 3; research_feedback-as-teaching.md 1.10). `gate_model_sequence` hard-requires the clean annotated before/after AND a predict-the-fix (with a feedback reveal) AND a diagnosis slot.

**Mechanism 1: the clean annotated before/after (the load-bearing worked example, delivered in short chunks).**
- Deliver it as short chunks, not one long block: present the BEFORE as its own chunk, then reveal the AFTER split into a Device chunk, an Effect chunk, and a Warrant chunk. A long worked example raises load; chunking is the load-reducing move, so keep each chunk tight.
- BEFORE = a competent summary that also spots the device by label ("the author uses a lot of nature description"); annotate WHY it caps at the middle band (it retells or labels, never says what the choice does or why it matters).
- AFTER = the same content run through Device -> Effect -> Warrant, with `[DEVICE: ...]`, `[EFFECT: ...]`, `[WARRANT: ...]` bracketed inline ON the sentences (annotation ON the exemplar, not in a separate legend, to avoid split attention).
- Close by pointing at the final sentence: the Warrant/significance is the top-band move.
- Grounding: worked-example effect (research_worked-example-fading.md Claim 1; MIT TLL https://tll.mit.edu/teaching-resources/how-people-learn/worked-examples/ ). `gate_content_depth` requires `annotated_before_after` >= 220 chars and BOTH a literal BEFORE and AFTER inline (extract T4-5).
- These bracketed inline tags ARE **subgoal labels**, the most transferable and most stateless-compatible worked-example upgrade: they chunk steps and externally prompt the right self-explanation, and unlike self-explanation training they do not decay (Margulieux & Catrambone 2016, subgoal-label effect d ~ .2-.3, https://bpb-us-e1.wpmucdn.com/sites.gatech.edu/dist/b/1555/files/2020/09/MargulieuxandCatrambone2016.pdf ). Use the SAME D/E/W labels across the whole ladder so they become the through-line a stateless sequence otherwise lacks (research_worked-example-fading.md Claim 5).

**Mechanism 2: predict-the-fix (forced diagnosis before the reveal).** Give a draft that names a real device but stalls at summary/labeling; ask which single move most improves it; the correct option is "explain what it DOES and why it matters (reach effect and warrant)." Distractors are the plausible-but-wrong analysis reflexes: add another quote, name more devices, make sentences longer or more formal (extract T4-6). This is errorful-generation-plus-reveal: committing to a prediction before the reveal is the mechanism, not wasted motion, and it is strongest for high-confidence errors (Metcalfe 2017, hypercorrection, https://www.columbia.edu/cu/psychology/metcalfe/PDFs/Learning%20from%20errorsAnnual%20ReviewMetcalfe2016.pdf ). `gate_model_sequence` requires the `predict_the_fix` slot to carry a non-empty `feedback` reveal.

**Mechanism 3: AI feedback on the student's OWN draft** is delivered by the production FRQ's external grader, NOT authored as a slot (extract T4-7 note; `KIND_QTI["production_frq"]` -> extended-text + ExternalApiScore).

**Mechanism 4: student-generated diagnosis, modeled first, then run on the student's own response, and it must ship a scaffold.** Show the DEW self-check running step by step on a flawed draft (D partly met, E met, W missing, so it stalls in the middle band), THEN ask the student to run the same three-item checklist on their own response, with a frame ("This choice matters to the author's purpose because ____"). `gate_model_before_required` rejects any `diagnosis_frq` that appears before a MODEL or that gives no scaffold (frames / checklist / named steps) (extract T4-7). This is the async form of SRSD self-regulation: a self-assessment SCRIPT (ordered self-questions) inside a single item, which raises self-regulation more than a bare rubric and needs no cross-item memory (Panadero, Alonso-Tapia & Huertas 2012, https://repositorio.uam.es/handle/10486/710139 ; research_async-srsd.md 5c).

**No near-peer / human coping model.** Do NOT stage a near-peer persona or a fake-student think-aloud (visible false start + coping self-talk + repair): static screen text cannot carry the social-modeling / self-efficacy mechanism that only transfers from live or video human modeling, so no slot may claim the coping-model effect. What ships instead is a STRONG ANNOTATED before/after worked example (Mechanism 1): the common error appears as LABELED AUTHOR-VOICE ANNOTATIONS on the exemplar ("problem: stalls at labeling the device" / "fix: say what the choice does and why it matters"), NOT as a persona's inner monologue, paired with predict-the-fix so the learner does the evaluating (research_worked-example-fading.md; research_async-srsd.md Section 3).

### SUPPORTED (Support It: worked -> completion -> independent, with ONE EXTRA rung)

**Author TWO discriminations, not one, and label both as Grade-C design bets** (extract T4-8). Expertise-reversal evidence is thin in humanities/language, so when uncertain keep the scaffold and default to +1 rung (research_worked-example-fading.md Claim 6, Kyun, Kalyuga & Sweller 2013 for writing, https://eric.ed.gov/?id=EJ1011878 ).
- Discrimination A: a minimal set isolating the analytical-move dimension (analysis vs summary vs paraphrase vs personal-reaction).
- Discrimination B: a top-band boundary pair isolating exactly the 4-to-5 lift (effect-stated vs significance-reached). This boundary pair is the highest-value calibration move for this type.
- `gate_discrimination_before_production` requires >= 1 discrimination before any production AND `labeled_grade_c=True` on the discrimination slots. Discrimination-before-production is UNVALIDATED for writing, so it is built, labeled, and A/B-flagged, never sold as evidence (extract T4-8).
- These discriminations ARE the async substitute for the compare-two-models move and for principle-naming self-explanation: deliver self-explanation as a scored choice item ("which draft reaches significance, and why"), not a free "explain what you did" prompt, because generic self-explanation prompts can negatively moderate the worked-example effect while principle-naming ones help (research_worked-example-fading.md Claim 4, Barbieri et al. 2023, https://danamillercotto.com/uploads/4/7/7/2/47725475/barbieri_et_al__2023__we_meta-analysis.pdf ).

**The completion rung gives the Device and makes the student supply only Effect + Warrant** (extract T4-9). This isolates the hard part so working memory spends only on the E + W generation (completion-problem effect, van Merrienboer et al. 2002, https://www.sciencedirect.com/science/article/pii/S0959475201000202 ). Set a two-sentence product goal (sentence one = effect on the reader, not a retelling; sentence two = why it matters to the author's purpose). Reference lesson SUPPORTED `production_frq` uses `unit="sentence"`.

**Faultless-slot construction is the strongest DI rigor for this type** (extract T4-10): the summary-vs-analysis minimal pair must differ on EXACTLY the analytical-move dimension; positive (analysis) examples share Device -> Effect -> Warrant and vary only the device; the non-example bank is dominated by plausible summaries (anticipate the #1 misread). `gate_no_ambiguous_reference` bites here: any "this version / the example above" must show its referent inline.

**Fade backward and keep it stateless.** Blank the LAST step first: the completion item shows Device + Effect fully modeled and asks the student to generate only the Warrant; the next rung shows Device and asks for Effect + Warrant. Backward fading produced the only significant far-transfer gain and saved study time in the founding experiment; earlier worked steps stay visible on the SAME item as built-in scaffolding, which is exactly what lets an isolated item scaffold without referencing anything external (research_worked-example-fading.md Claims 2-3, Renkl et al. 2002, https://www.davidlewisphd.com/courses/EDD8121/readings/2002-Renkl_et_al.pdf ).

### INDEPENDENT (scaffolds removed, self-contained)

**One full analytical paragraph on the taught text, all three DEW elements required, self-contained** (extract T4-11). Let the student CHOOSE which authorial choice to analyze (imagery, irony, repetition, a described shift), which satisfies the student-choice audit (EG >= 1 student-choice point). Product goal names all three: Device with short evidence, Effect on the reader, Warrant reaching significance. Include a within-item STATIC one-pass conditional self-check printed in the single prompt (one submission, no loop): "Before you submit: if your final sentence only states the effect, add one sentence beginning 'This matters to the author's purpose because ____.'" `gate_unit_ladder` requires this production to declare `unit="paragraph"` and to be non-decreasing after the sentence-level completion.

**The prompt must be self-contained and must not reference the student's own prior work** (extract T4-12). Because QTI is stateless and a retake starts blank, the prompt cannot say "revise the paragraph you wrote earlier." `gate_no_prior_work_reference` bites "revise your paragraph" / "your response from step N." The recognition half of revision is taught by discrimination on PROVIDED pairs (Discriminations A and B above); the production half cannot be delivered as look-back (research_feedback-as-teaching.md 2.2).

### TRANSFER (novel content bank, same DEW move)

**Transfer to a DIFFERENT author, DIFFERENT genre, DIFFERENT content bank; same DEW move** (extract T4-13). The reference lesson goes from Chopin narrative (imagery/irony) to a US-federal weather-forecasting explanatory text where the analyzable choices are STRUCTURE and SEQUENCE, not imagery. This proves the move is genre-portable, not memorized on one passage; keep all three DEW elements required. `gate_bank_partition` REJECTS any TRANSFER slot whose content bank overlaps a MODEL/SUPPORTED bank; it must carry its own `bank` tag. Near-to-moderate transfer must be designed (KB, Grade B; extract T4-13).

**Route the transfer production to a real rubric config at the paragraph ceiling, scored on Evidence/Development and Organization** (extract T4-14). `gate_grader_routing` requires every `production_frq.rubric_ref` to be in `RUBRIC_CONFIGS = {rc.staar, rc.mcas, rc.ohio, rc.4trait, rc.ap}`. Test map: STAAR analyze single source, MCAS analyze across two, Ohio analyze both moves before picking.

---

## 3. Feedback-as-teaching inside the stateless boundary (deliverable vs blocked)

Feedback teaches when the object being judged is fixed and self-contained within one item; it breaks the moment the design needs to carry the student's own words or score from one item to the next (research_feedback-as-teaching.md 2.3). For T4 specifically:

**DELIVERABLE here:**
- Grader feedback on a PROVIDED anchor paragraph: the external grader scores an author-supplied text against the rubric and returns elaborated, process-level feedback so students see what good feedback looks like before they submit. This is a single evaluation of a fixed input, so statelessness is a non-issue (Hattie & Timperley 2007 process-level > task-level, https://journals.sagepub.com/doi/10.3102/003465430298487 ; Shute 2008 elaboration > verification, https://andymatuschak.org/files/papers/Shute%20-%202008%20-%20Focus%20on%20Formative%20Feedback.pdf ).
- Predict-the-fix then reveal inside ONE item (the MODEL Mechanism 2 slot): the reveal must name the process move (reach effect and warrant) and give a reusable rule, not flash a bare answer (Metcalfe 2017; Shute 2008).
- Erroneous-example autopsy and strong/weak twin items: the BEFORE (summary-plus-labeling) is the marked erroneous example; the boundary pair (effect-stated vs significance-reached) is the strong/weak twin. Highlight the weak span in-stem for lower-knowledge students so they do not have to locate the flaw first (Booth et al. 2015, https://files.eric.ed.gov/fulltext/ED566953.pdf ).
- Self-assessment SCRIPT on the student's single fresh submission: the DEW self-check (Mechanism 4) run within the production item. Self-assessment against explicit criteria carries a large writing effect (~0.62) close to teacher feedback and above automated feedback (Graham, Hebert & Harris 2015, https://digitalcommons.unl.edu/specedfacpub/222/ ).

**BLOCKED by statelessness (do NOT design around these) (research_feedback-as-teaching.md 2.2):**
- Feedback on the student's EVOLVING draft across turns (draft -> feedback -> revise same draft -> feedback again). The self-fix-when-prompted loop that depends on a coach seeing the student's current draft is not deliverable item-to-item.
- Iterative revise-and-recheck on the student's own text: we can flag errors on a PROVIDED text (indirect feedback), not on the student's live draft across items.
- Any reveal that references an earlier answer or score ("compared to your draft in step 2").
- Adaptive fading tuned to this student's running performance; progress/growth feedback over time.

**Net for T4:** the coaching win is re-engineered from "iterate on your draft" into "predict/judge the analytical move on a provided pair, then reveal the why" plus "run the DEW self-check on your one submission." The literature says this re-engineered form is not a weak substitute (self-assessment 0.62; errorful-generation-plus-reveal are strong in their own right).

---

## 4. Worked-example fading without statefulness

Fading is a SEQUENCE property, not a within-item adaptive loop, and the fixed pre-scripted fade is empirically validated with no prior-response memory (research_worked-example-fading.md Claim 1, Renkl et al. 2002). For T4 the fixed ladder is:
- **Rung 0 (MODEL):** the fully worked D->E->W annotated before/after with subgoal labels.
- **Rung 1 (SUPPORTED completion):** Device given, student supplies Effect + Warrant (backward fade, last step blank; delivered as a completion item whose partial solution is printed in the stem so it is self-sufficient and isolation-safe, research_worked-example-fading.md Claim 3).
- **Rung 2 (deeper completion / early INDEPENDENT):** less given, student supplies more of D->E->W.
- **Rung 3 (INDEPENDENT/TRANSFER):** full paragraph, externally graded.

Two static devices carry the fade across isolated items: the completion problem (all needed context printed in the stem) and the consistent D/E/W subgoal labels (the through-line). Principle-naming self-explanation is delivered as the scored discrimination items (Discriminations A and B), not as free prompts.

**Coarse between-lesson routing is UNBUILT (assumed-pending-eng), never inside an item.** The lesson SHIPS as a complete, self-sufficient FIXED-FADE sequence that requires ZERO routing to function; the fixed ladder above is the whole deliverable. Score-based adaptation at the seam BETWEEN lessons (an end-of-lesson production score from the rc.* grader, or a first-step-style single-item diagnostic, routing the student to a more-worked or less-worked variant) is an ASSUMED capability pending engineering, NOT a delivered one: it is contingent on the platform actually supporting next-lesson routing on a grader score. If that capability lands it would recover a coarse version of adaptive fading (adaptive > fixed > unfaded) without violating item isolation, but nothing in this lesson depends on it (research_worked-example-fading.md Claims 6-9, Salden et al. 2010 https://www.jstor.org/stable/23372797 ; Kalyuga 2007 first-step method https://www.uky.edu/~gmswan3/EDC608/Kalyuga2007_Article_ExpertiseReversalEffectAndItsI.pdf ).

---

## 5. Where function-over-form device instruction applies

This is directly relevant to T4, because DEW's E and W steps ARE the function-over-form thesis applied to close reading. The research verdict: teaching devices as FORMS to identify or label has null-to-negative effects on writing quality, while teaching a device by the JOB it does (and requiring the student to reason about that job) is what works (research_function-over-form.md: Writing Next traditional grammar small significant NEGATIVE effect, https://www.thewritingrevolution.org/wp-content/uploads/2017/05/WritingNext.pdf ; Fearn & Farnan function-beats-definition, https://files.eric.ed.gov/fulltext/EJ787964.pdf ).

Concrete authoring consequences for T4:
- Do NOT reward or test device-spotting/labeling as the goal. "The author uses imagery" (naming the form) is exactly the BEFORE that caps at the middle band. Naming more devices is a designed distractor in predict-the-fix, not a correct answer (extract T4-6).
- The Effect step is the function: what the choice DOES to the reader. The Warrant is the function raised to purpose. Reward the job, not the label.
- Use the Fearn & Farnan "does it do the job here?" pattern for the discrimination distractors: the right device doing the WRONG analytical job (a real device correctly named but stalled at summary/labeling). This isolates the analytical-move dimension the faultless slot requires (extract T4-10).
- Because Myhill's contextualised-choice gains depended on a knowledgeable teacher doing the structure-to-effect talk, and we have no teacher, that "why this choice creates this effect" talk must be BAKED INTO the worked example and the answer rationales, stated concretely, and over-scaffolded for weaker writers (research_function-over-form.md, Myhill et al. 2012 effect small ~0.20 and skewed to abler writers, teacher subject knowledge a mediator, https://eric.ed.gov/?id=EJ959614 ). This is what the inline D/E/W subgoal labels and the elaborated reveals are for.

**Sentence-level Warrant tools (TWR moves taught by rhetorical FUNCTION).** The W step is where two specific sentence moves earn their place, taught by the JOB they do (never as grammar labels):
- **relative clause -> CONSEQUENCE:** the Warrant sentence names what the effect leads to, using a "which ..." / "that ..." construction to attach the consequence to the effect ("the image of the open window, which signals the freedom she has just glimpsed, ...").
- **prepositional phrase -> CONTEXT / SCOPE:** a "by ...", "in ...", "for ..." phrase narrows the effect to the author's purpose and adds the missing context ("for a reader who expected grief, ...").
Model both as the concrete shape the "This matters to the author's purpose because ____" frame can take; reward the function (reaching consequence and context), not the construction name.

One-line gate note: the mechanical substrate is APP-OWNED and gated, not re-taught here. Conventions belong to EGUMPP (G3-10) and sentence-combining craft to AlphaWrite (G3-8); this playbook treats both as retrieval-gated prerequisites and teaches only the rhetorical USE.

Note: the specific device-to-function mappings are a design choice we impose for clarity, flagged under the provenance rule, not a finding lifted verbatim from a study.

---

## 6. Sharpest gate risks for T4 and how to satisfy them

All 19 gates run and the reference lesson passes all 19. Ranked most-biting first for a naive T4 draft (extract "gates that bite hardest"):

1. **`no_source_markup`** (the defining T4 trap). Analysis pedagogy wants "underline the device / annotate the shift"; stimuli are display-only. Satisfy: use read-and-note framing ("read once for what happens, then reread and keep ONE choice in mind"); put any "scan for / pinpoint the choice" marking inside a discrete item authored as a plain CHOICE item (present candidate spans as labeled options), never as an instruction to mark the display. Do NOT author it as hottext unless the platform confirms hottext is native: hottext is NOT among the confirmed native kinds (stimulus / choice / extended-text). `_MARKUP_VERBS` fires on teach_card / stimulus_display / annotated_before_after bodies.
2. **`define_before_use`.** DEW's own vocabulary (`warrant`, `rhetorical device`) is on the enforced `_TECH_TERMS` list, and `analysis`/`paraphrase`/`summary` must be distinguished. Satisfy: put a plain-words definitional cue ("means", "is when", "refers to") next to each term inside a TEACH body before any student-facing use. This gate bites T4 harder than any other type because the mnemonic's own words are enforced terms.
3. **`model_before_required`.** The `diagnosis_frq` must follow a MODEL and ship a scaffold (frame / checklist / named steps / "step 1"). Satisfy: model the DEW self-check on a flawed draft first, then hand the student the same checklist plus the "This matters because ____" frame. A blank "diagnose it" is auto-rejected.
4. **`content_depth`.** `annotated_before_after` must be >= 220 chars AND contain BOTH a literal BEFORE and a literal AFTER. A stub fails here first. Satisfy: write the full BEFORE (summary-plus-labeling) and the full AFTER (D->E->W with inline bracket labels), delivered as short chunks (do not pad into one long block; chunking lowers load).
5. **`model_sequence`.** Requires the clean annotated before/after AND a predict-the-fix (with a non-empty `feedback` reveal) AND a diagnosis slot somewhere. Missing any one rejects. Satisfy: ship all three MODEL mechanisms (1, 2, 4); mechanism 3 is the grader, not a slot.
6. **`bank_partition`.** TRANSFER must not reuse a taught content bank. Satisfy: the narrative -> explanatory genre shift with its own `bank` tag. A lazy "analyze another passage from the same author" fails.
7. **`discrimination_before_production`.** >= 1 discrimination before any production, `labeled_grade_c=True`. Satisfy: author the two discriminations and set the Grade-C label on both.
8. **`type_ceiling` + `unit_ladder`.** T4 caps at paragraph; declaring `unit="essay"` or a non-decreasing violation rejects. Satisfy: sentence-level completion, then paragraph-level independent/transfer, never higher.
9. **`no_ambiguous_reference`.** Passage-heavy analysis tempts "the example above / this version"; the referent must be shown inline or bound. Satisfy: quote the referent in the same slot body.
10. **`effect_size_honesty` + `mnemonic_status`.** DEW status must be declared `"proposal"` and no slot may claim SRSD's live-enacted effect size for the async model. Satisfy: label DEW a design proposal; attribute only the modality-flexible effects (worked-example, retrieval, forced response, self-assessment) to the async build.

The remaining gates (`shell_completeness`, `binding_integrity`, `calibration_discipline`, `grader_routing`, `timeback_native`, `no_prior_work_reference`, `no_em_dash`) apply uniformly; they still must pass but are not T4-specific pressure points, except `no_prior_work_reference`, which bites the moment an author tries to build "revise your analysis" (impossible on stateless QTI; see stage INDEPENDENT).

---

## Retrieval + item rules (LS feedback 2026-07)

These encode the 2026-07 learning-scientist pass as T4 authoring defaults so a fresh analysis lesson clears the new gates by construction.

- **Cadence ceiling: CONCEPT tier, ceiling 3** (`gate_check_cadence`). T4 (device -> effect -> warrant) is a concept-teaching type: a run of COUNTED teach cards may not exceed THREE before a check (`discrimination` / `predict_the_fix` / `self_score`). The chunked D/E/W annotated before/after counts as ONE worked example even though it is delivered in short chunks; do not let the BEFORE chunk plus the three AFTER chunks read as four separate counted cards that blow the ceiling. Tag a pure buy-in card `tag="buy_in"` so it counts 0. TIGHTEN to 2 right after the card that names the memorizable tool (the DEW mnemonic): tag it `tag="memorizable_tool"` and put Discrimination A right behind it.
- **Four options per discrimination, each a NAMED MISCONCEPTION** (`gate_structural_item`). Discrimination A (analysis vs summary vs paraphrase vs personal-reaction) and Discrimination B (effect-stated vs significance-reached) each carry exactly four choices; every distractor is a real analysis misread (a plausible summary, device-labeling, stopping at effect, a personal reaction), never filler.
- **Diagnosis: the student ANSWERS the DEW check, then improves** (`gate_self_answered_check`). The modeled DEW self-check may pre-answer a PROVIDED weak draft (name it, e.g. "D partly met, E met, W missing"), but MUST then hand the student an independent turn: run the same three-item checklist on their own response with the "This matters to the author's purpose because ____" frame. Never print a check that answers itself and stops.
- **No comma before "because"/"so" in a fill-in frame** (`gate_frame_comma`). The warrant frame reads "This matters to the author's purpose because ______" with NO comma before because. Emit any side/reason fill-in with `claim_frame()` from `lesson_prompts` rather than hand-writing it.
- **Re-gloss the hard terms.** DEW's own vocabulary (warrant) plus controlling idea, synthesis, and counterclaim are in `_TECH_TERMS`, so `gate_define_before_use` already forces an in-lesson gloss. On a later-lesson re-introduction prefer a BRACKETED gloss right after the term (LS #9 style).
- **Stem wording (playbook-only, #7):** name the move directly ("Which sentence explains what the choice does to the reader?"), never a meta-phrasing ("which fits the verb").
- **Tone (playbook-only, #5 / Yeager):** state the standard up front; each per-choice reveal is wise-feedback that names the MOVE (reach effect, reach warrant), no person-praise, no compliment-sandwich.
- **Pair a stand-alone improve-write with a `predict_the_fix`** where feasible (playbook-only, #4).
- **Cross-lesson spacing (KH caveat, #3):** the in-lesson cadence gate is necessary but NOT sufficient; the D/E/W move must recur in later lessons on fresh texts. That durability is a sequence-builder concern, not visible to this lesson's gates.

---

## 7. Keep it short

- **Isolate the hard part, do not lengthen the lesson.** The completion rung gives the Device so working memory spends only on Effect + Warrant (extract T4-9; completion-problem effect). A well-decomposed lesson beats a long one.
- **One passage carries most of the lesson.** Teach, model, both discriminations, completion, and independent all sit on the SAME text (the reference lesson uses one Chopin excerpt for six slots); the student re-loads a new passage only at Transfer. This is contamination-free because the lesson binds only LESSON-pool stimuli.
- **Extra rung, not extra prose.** The "one extra rung" is two short choice items, not more Teach copy. Depth comes from the worked example and the discriminations, the highest-value slots; redundancy harms once the point is made.
- **The mnemonic offloads the procedure.** DEW is three letters; keep each letter to one job. Do not stack a second mnemonic system: TSIS-style metacommentary is delivered as CONTENT inside the DEW slots, not as a parallel mnemonic.

---

## Honesty ledger (proven vs extrapolated)

- **SRSD spine, explicit strategy, worked example, product goals:** Grade A, directly applicable (KB; Writing Next).
- **DEW itself:** a DESIGN PROPOSAL, not a sourced or established mnemonic (`LESSON_TYPES[4]` status "proposal"). It is the "Memorize It" artifact of SRSD; the specific letters are ours.
- **The two discriminations (discrimination-before-production):** UNVALIDATED for writing; a labeled Grade-C design bet aligned with contrasting cases, to be A/B tested.
- **Scaffold fading / the extra rung:** expertise reversal is Grade A generally but EXTRAPOLATED for humanities/language, so fade on demonstrated performance and default to +1 rung when uncertain.
- **The async Model sequence:** its ingredients (worked-example ~0.60, retrieval, forced response, personalized process-feedback) are separately backed and modality-flexible; it does NOT inherit SRSD's live-enacted effect size.
- **Function-over-form for the E/W steps:** the direction (reward function, not form-labeling) is well supported by a synthesis (Fearn & Farnan + sentence-combining meta-analyses + Myhill), not a single decisive trial; Myhill's effect was small and teacher-mediated, so the mediating talk must be baked into worked examples and rationales and over-scaffolded for weaker writers.
- **Copyright:** the reference lesson uses public-domain Chopin (1894) and a US-federal-sourced explanatory text, quoting only short verbatim phrases with the analysis in own words.

### Blocked by Timeback (flagged honestly)

- **Student markup of the passage** (underline/annotate the device): impossible; display-only stimuli. Reconstructed with read-and-note framing + plain CHOICE items (candidate spans as labeled options); do not rely on hottext, which is not among the confirmed native kinds (stimulus / choice / extended-text).
- **Feedback on an evolving draft and revise-recheck loops:** impossible across stateless items; recognition half of revision taught on provided pairs, production half not deliverable as look-back.
- **Within-lesson adaptive fading and longitudinal progress feedback:** impossible; only fixed fading in-lesson. Coarse between-lesson routing on an external-grader score is UNBUILT / assumed-pending-eng, not delivered; the lesson ships fully self-sufficient with zero routing required.
- **Reference to the student's own prior work or score:** impossible; every production slot must be self-contained (`gate_no_prior_work_reference`).
