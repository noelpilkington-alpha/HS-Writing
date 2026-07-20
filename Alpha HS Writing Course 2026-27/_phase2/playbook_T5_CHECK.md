# Authoring Playbook: T5 Rubric-Revision (CHECK)

> How to build a Type-5 lesson that teaches a student to revise a PROVIDED draft against rubric criteria,
> with calibration (predict-then-reveal) as the engine, inside Timeback's display-only, stateless, no-human
> delivery. Every move below is anchored to the internal extraction (`extract_T5_CHECK.md`, cited as EXT-Pnn)
> or to a verified research brief (cited by author/title/URL). House rules observed: own words, cited anchors,
> no em dashes.

---

## 0. Archetype identity (fixed facts, do not drift)

- Type 5, slug `rubric-revision`, mnemonic **CHECK**, status **proposal**. The provenance block must declare
  `mnemonic_status: "proposal"` or the `mnemonic_status` gate rejects the lesson (EXT-P1; `lesson_contract.py`
  `LESSON_TYPES[5]`).
- CHECK expansion (proposal): **C**riteria (name the trait), **H**unt (meet or miss), **E**xplain the gap,
  **C**orrect, **K**eep-score (predict then reveal) (EXT, archetype identity).
- What it teaches: revise for SUBSTANCE against the rubric. The deeper engine is CALIBRATION
  (predict-then-reveal). Explicitly DISTINCT from T6 editing-in-context, which fixes mechanics (EXT-P4).

---

## 1. Terminal deliverable + production ceiling

**Terminal deliverable.** One fresh, self-contained PARAGRAPH revision, scored by the external rubric grader.
The student is handed a provided lower-scoring paragraph inline in the item stem and rewrites it to hit a named
score point on a named trait. Because the archetype's whole point is calibration, the paragraph task is
preceded by the four-stage judge-then-reveal ladder run on OTHER people's anchors, so by the time the student
revises, they have already practiced predicting scores and seeing the gap.

**Production ceiling = paragraph.** `TYPE_CEILING_UNIT[5] = "paragraph"`; the `type_ceiling` gate rejects any
scored production above a paragraph. Whole-essay calibration is out of type: it belongs to T7 essay-assembly,
which reuses T5's Stage C and Stage D on a full draft (EXT-P15, EXT archetype identity).

**Honesty ceiling on the claim we make for it.** T5's power rests on CALIBRATION-SPECIFIC evidence, NOT on a
global feedback aggregate and NOT on SRSD's live-enacted effect near 1.14. Do not anchor T5 on Hattie and
Timperley's roughly 0.79 GLOBAL feedback aggregate: that figure folds in feedback modes (a coach reading an
evolving draft, peer and oral conferencing) that are BLOCKED in stateless Timeback, so it overclaims here.
Cite instead the calibration and self-assessment warrant that survives the stateless boundary, matching the KB
Layer-4 calibration evidence:
- self-assessment against explicit criteria carried a weighted effect near 0.62 for writing, close to teacher
  feedback and above automated feedback (Graham, Hebert and Harris, 2015, Formative Assessment and Writing: A
  Meta-Analysis, https://digitalcommons.unl.edu/specedfacpub/222/);
- calibration is a small-but-real TRAINABLE skill (g near 0.177 in the internal KB Layer-4 read);
- students systematically OVER-rate their own work (over-estimation bias g near 0.206), which is exactly what
  the judge-others-first ladder is built to correct.
The async passive-read model does not inherit the 1.14. State this honestly or the `effect_size_honesty` gate
rejects it (EXT-P7, EXT gate table row 6).

---

## 2. The spine within the spine: the four-stage judge-then-reveal engine

T5 does not run a plain support ladder. Its ladder IS the validated calibration progression, run as four full
"student judges, THEN the grader or AI reveals the gap" loops (EXT, spine section; Toolkit D4 progression shape):

- **Stage A** binary single-trait (meets / does not meet).
- **Stage B** 3-point.
- **Stage C** full analytic on the REAL test scale (STAAR 0 to 3; MCAS Idea-Development 0 to 5 plus
  Conventions 0 to 3).
- **Stage D** self-diagnosis with NO rubric shown: predict the scores, THEN reveal the gap.

Judging OTHERS' anchors before one's own is the built-in defense against the overestimation bias (bias g near
0.206 in the internal KB read) (EXT-P10). This ordering is not optional decoration; it is the pedagogy.

---

## 3. Per-SRSD-stage authoring guide

Each stage below gives: the exact moves, the worked-example shape, and the stateless/async delivery method
(display-only stimuli + stateless choice or extended-text items + external grader).

### TEACH (Develop and activate background knowledge + Discuss it)

**Moves.**
1. Define every rubric term in plain student words BEFORE any anchor paper appears. "Rubric trait" and the
   meaning of each score point are taught first, in student words (EXT-P1; `define_before_use` gate lists
   "rubric trait"). This is faultless-communication sequencing: the concept is unambiguous before it is used.
2. Make CHECK's "Criteria" step the REAL test scale, with a specific product goal, never "improve it." State a
   concrete target such as "raise this paragraph from a 2 to a 3 on the Development trait by tying each piece
   of evidence back to the claim" (EXT-P2). Specific product goals beat "do your best": the internal Toolkit
   pins product-goal instruction near 0.70 (corroborated in Graham and Perin, 2007, Writing Next, Specific
   Product Goals 0.70, https://www.thewritingrevolution.org/wp-content/uploads/2017/05/WritingNext.pdf).
3. Teach the gating principle as CONTENT, not just a scoring mechanic: conventions serve substance, so do not
   polish commas on a thin essay. Deliver it with a 4-anchor discrimination set (clean-conventions/no-content,
   messy-conventions/strong-content, both-strong, both-weak) and have students predict the gate outcomes
   (EXT-P3).
4. Firewall revision (substance against rubric) from editing (T6 mechanics) up front, because the whole
   archetype is substantive revision (EXT-P4).

**Worked-example shape.** No new worked model here; TEACH is a short expository card plus one discrimination
set. The "discussion" of what makes writing effective becomes worked contrasts and choice questions, not a live
conversation (research_async-srsd, Section 2: Discuss it survives only if reconverted from dialogue to media
plus choice items).

**Stateless/async delivery.** A display-only stimulus card states the trait, the scale, and the gating
principle. Concept checks are isolated choice items. Nothing carries state; each item re-states its own trait
definition in-stem.

**Keep it short.** One Teach card that names the trait, the scale, and the gating principle. Do not re-teach
the writing move itself (that was T2/T3/T4). The `content_depth` floor (teach card of at least ~200 chars) is a
MINIMUM, not a target (EXT, Teach "keep it short" note).

### MODEL (Model it + Memorize it): the annotated worked-example + predict-the-fix sequence

**Moves.**
1. The worked example is a LOW-score anchor beside a HIGH-score anchor, annotated ON the sentence, never in a
   separate legend (EXT-P5; split-attention). Show a literal BEFORE (the lower anchor, which drops the
   substantive move) and a literal AFTER (the higher anchor, which makes the move). Use published or
   own-authored anchor papers at each score point.
2. A predict-the-fix item asks the student to name the ONE move that separates the two score points BEFORE the
   reveal (EXT-P6). This is CHECK's Hunt plus Explain as a forced-response choice item with a feedback-block
   reveal. The commitment before the reveal is the mechanism, not wasted motion: generating an answer and then
   getting corrective feedback beats error-free study, and the reveal must explain the reasoning, not just
   flash the right answer (Metcalfe, 2017, Learning from Errors, Annual Review of Psychology,
   https://www.columbia.edu/cu/psychology/metcalfe/PDFs/Learning%20from%20errorsAnnual%20ReviewMetcalfe2016.pdf).
3. Deliver error-recovery as a clean over-rating recalibration contrast delivered as ANNOTATED WORKED EXAMPLE,
   NOT a near-peer persona or a fake-student self-talk monologue, and do not claim SRSD's coping-model effect
   size (EXT-P7). The recovery model: a PROVIDED anchor is shown with a self-awarded 3, the reveal shows the
   real score is a 2, and the gap is named as an author-voice LABELED ANNOTATION on the anchor itself ("problem:
   this anchor claims a 3 but never explains after a quote; the anchor that actually earned a 3 explains after
   every quote"). No simulated peer, no false-start monologue, no inner think-aloud voice. Keep predict-then-
   reveal: the student names the over-rated gap BEFORE the reveal. This is the screen-validated worked-example
   effect, needs no human and no state, and shows the common error plus its fix as labeled annotations (IES
   Practice Guide Recommendation 1, Strong evidence, recommends modeling with identified errors and corrections,
   Graham et al., 2016, Teaching Secondary Students to Write Effectively, https://ies.ed.gov/ncee/wwc/PracticeGuide/22).
4. The student-generated diagnosis slot must be SCAFFOLDED with named steps or a frame, never a blank "diagnose
   it" (EXT-P8). Use a fill-in frame: "The lower version lacked ___; the fix adds ___; it now scores higher
   because ___." An ordered self-question script drives more self-regulation than a bare rubric (Panadero,
   Alonso-Tapia and Huertas, 2012, Rubrics and self-assessment scripts,
   https://www.sciencedirect.com/science/article/abs/pii/S1041608012000672).
5. Memorize CHECK with a mnemonic plus retrieval-practice choice items (match the letter to its move; pick the
   step that comes next). Memorization is necessary but low-value alone, so pair it with application
   (research_async-srsd, Section 2, Memorize it).

**Worked-example shape.** One before/after anchor pair (rung 0 of the fade), annotated on the sentence with
consistent subgoal-style labels naming the FUNCTION of each move ("state the claim," "ground it in evidence,"
"explain the link"). Reuse the SAME functional labels across the whole ladder so the labels become the
through-line a stateless sequence otherwise lacks (research_worked-example-fading, Claim 5, Margulieux and
Catrambone, 2016, https://bpb-us-e1.wpmucdn.com/sites.gatech.edu/dist/b/1555/files/2020/09/MargulieuxandCatrambone2016.pdf).

**Stateless/async delivery.** The two anchors are display-only XHTML (read-and-note framing, never "mark up the
anchor," EXT-P19; `no_source_markup` gate). The predict-the-fix and the scaffolded diagnosis are isolated QTI
items; the reveal lives in the SAME item's feedback block as author-voice annotation on the provided anchor,
not as a simulated persona or think-aloud (research_async-srsd, Section 3). No item references any prior item.

**Keep it short.** One before/after pair, one predict-the-fix, one scaffolded diagnosis. Reuse an existing
anchor rather than authoring a long new one (EXT, Model "keep it short" note; redundancy risk).

### SUPPORTED (Support it): the calibration ladder, performance-faded

**Moves.**
1. Boundary-pair discrimination is the highest-value SUPPORTED move; label it Grade-C. Put a 2 next to a 3 (or
   a 4 next to a 5) and ask which single move separates them. This must appear BEFORE any production and must
   set `labeled_grade_c=True` (EXT-P9; `discrimination_before_production` gate). Note honestly that
   discrimination-before-production is an internally UNVALIDATED heuristic, kept and labeled, not a proven law.
2. Students judge OTHERS' anchors before judging their own (EXT-P10). This is the overestimation-bias defense.
3. Every self-score is a predict-then-reveal loop paired with grader or expert feedback on the gap; the rubric
   alone is never left to "grade yourself." A `self_score` slot must PRECEDE a graded reveal (EXT-P11). Handing
   over a rubric with no feedback reveal did NOT improve calibration in the internal KB read (rubrics-alone was
   non-significant); feedback is the only significant moderator.
4. Run Stages A to B to C as the fade ladder, faded on demonstrated PERFORMANCE, not on lesson number. Remove a
   scaffold only when a scored performance shows readiness, and when uncertain keep the scaffold one rung
   longer (the humanities under-support asymmetry) (EXT-P12).

**Worked-example shape.** A backward-faded completion ladder. Blank the LAST move first and keep the earlier
worked moves visible in the same item as built-in scaffolding: item 1 shows Claim + Evidence + Warrant and asks
only for the Link; item 2 shows Claim + Evidence and asks for Warrant + Link. Backward fading is the direction
with the far-transfer win (Renkl, Atkinson, Maier and Staley, 2002, From Example Study to Problem Solving,
https://www.davidlewisphd.com/courses/EDD8121/readings/2002-Renkl_et_al.pdf; corroborated Education Endowment
Foundation, Working with worked examples, https://educationendowmentfoundation.org.uk/news/eef-blog-working-with-worked-examples-simple-techniques-to-enhance-their-effectiveness).

**Stateless/async delivery.** Each rung is a self-contained completion item that PRINTS its own partial solution
in the stem, so nothing is carried from a prior item (research_worked-example-fading, Claim 3, van Merrienboer
et al., 2002, https://www.sciencedirect.com/science/article/pii/S0959475201000202). Self-scores are choice items
whose feedback block is the reveal. The external grader plays the "conferencing" role on any short production
(research_async-srsd, Section 4). Fade lives in the item SEQUENCE, not in per-student state, and it is still a
documented win even without adaptivity: the original fading studies used a fixed, pre-scripted schedule
(research_worked-example-fading, Claim 1).

### INDEPENDENT (Independent performance): Stage D + the paragraph revision

**Moves.**
1. Stage D self-diagnosis runs with NO rubric on screen: predict the scores, then reveal the gap. This is
   CHECK's Keep-score at full independence and the top rung of the calibration progression (EXT-P13).
2. The production task is a FRESH, self-contained paragraph revision, NEVER "revise your earlier draft." QTI
   items are stateless and a retake starts blank, so the student cannot see their own prior submission. The
   prompt must SUPPLY the draft to revise inline (a provided anchor) and stand alone (EXT-P14;
   `no_prior_work_reference` gate). Route the production item to a valid `rc.*` config (`grader_routing` gate;
   rc.staar for the 2-trait STAAR scale, rc.mcas for the 0-to-5 plus 0-to-3 MCAS scale).
3. Do not exceed the paragraph ceiling. The scored revision tops out at a paragraph; a whole-essay revision is
   out of type (EXT-P15; `type_ceiling` and `unit_ladder` gates). Every scored production must declare a unit,
   and the declared units must be non-decreasing.

**Worked-example shape.** A deeper completion item (more moves blank) leading into full paragraph production.
Optionally attach a short self-question script the student runs on the ONE paragraph they just wrote (within-item
self-monitoring, since cross-item monitoring is impossible), for example: "Did each piece of evidence tie back
to the claim? Did I explain after every quote?" (research_async-srsd, Section 5c; research_feedback-as-teaching,
Part 3, self-questioning script).

**Stateless/async delivery.** Stage D is a choice/short-response item with the reveal in its feedback block. The
paragraph revision is an extended-text item scored once by the external grader on the provided (in-stem) draft;
the goal is baked INTO the prompt because no stored personal goal can be carried (research_async-srsd, Section
5d).

### TRANSFER (novel content, hard bank-partition)

**Moves.**
1. Calibrate and revise an anchor on a DIFFERENT content bank than anything taught, so the student transfers the
   calibration SKILL, not the recalled material. The transfer bank must not overlap any Model or Supported bank
   (EXT-P16; `bank_partition` gate). Still at the paragraph ceiling.

**Worked-example shape.** A fresh low-score anchor on new content, to score-and-revise.

**Stateless/async delivery.** A new display-only anchor plus a production item routed to the grader. Any coarse
"adaptivity" at the SEAM between lessons (a grader score routing the student to a more-worked or less-worked
next lesson variant) is UNBUILT and assumed-pending-eng, NOT a delivered capability: it depends on the platform
actually supporting next-lesson routing on a grader score, which is not confirmed. This lesson ships as a
complete, self-sufficient FIXED-FADE sequence that requires ZERO routing to function; the seam-routing is a
contingent enhancement only (research_worked-example-fading, Claims 6 and 7; expertise-reversal is real, so
mis-fitted scaffolding backfires, Kyun, Kalyuga and Sweller, 2013, https://eric.ed.gov/?id=EJ1011878).

---

## 4. Feedback-as-teaching HERE, within the stateless boundary

T5 IS a feedback archetype, so the boundary matters more here than anywhere.

**Deliverable (build on these).**
- Grader feedback on a PROVIDED anchor: a single evaluation of a fixed input, so statelessness is a non-issue
  (research_feedback-as-teaching, 2.1 item 1).
- Predict-the-fix then reveal INSIDE one item: commit to a judgment, then the same item reveals the fix and the
  WHY (research_feedback-as-teaching, 2.1 item 2; Metcalfe, 2017).
- Erroneous-example and strong/weak comparison items on provided text; highlight the flawed span in-stem for
  weaker students (research_feedback-as-teaching, 2.1 item 3; Booth et al., 2015,
  https://files.eric.ed.gov/fulltext/ED566953.pdf).
- Rubric self-score of a provided anchor with the real score revealed, so the student calibrates
  (research_feedback-as-teaching, Part 3).
- Elaborated, PROCESS-level reveals that name the move and give a reusable self-check, never a bare verdict
  (research_feedback-as-teaching, 1.1, Hattie and Timperley, 2007, https://journals.sagepub.com/doi/10.3102/003465430298487;
  Shute, 2008, elaboration beats verification, https://andymatuschak.org/files/papers/Shute%20-%202008%20-%20Focus%20on%20Formative%20Feedback.pdf).

**Blocked by statelessness (do NOT design around these; flag as Timeback limits).**
- Feedback on the student's EVOLVING draft across turns: item B cannot see the student's answer to item A, and
  a retake starts blank. The natural coaching loop (draft, feedback, revise the SAME draft, feedback again) is
  not deliverable turn to turn (research_feedback-as-teaching, 2.2 item 1). This is exactly why T5 revises
  PROVIDED anchors, not the student's own prior draft.
- Any feedback that references an earlier answer or score ("last time you...", "compared to your Step 2 draft")
  (research_feedback-as-teaching, 2.2 item 3).
- True within-lesson adaptive fading tuned to this student's running performance (research_feedback-as-teaching,
  2.2 item 4). We ship FIXED fading only.

**Feedback voice gate.** All authored feedback is GOAL / NOW / NEXT at the process and self-regulation level.
Ban person-praise ("great job") and grade-only reveals; the `calibration_discipline` gate auto-rejects
person-praise regex (EXT-P17; self-level praise is the weakest level, effect near 0.09 to 0.14 in Hattie and
Timperley, 2007).

**Reader-based beat.** Place at least one reader-based feedback moment across the arc ("here is how this landed
for a reader"), additive and non-overriding, to answer the logged expressivist dissent while the
criterion/scorer loop stays primary (EXT-P21).

---

## 5. Worked-example fading without statefulness

The fade is a SEQUENCE property, not an item property, so it drops straight into stateless QTI (research_worked-
example-fading, Synthesis point 1). Deliver it as:

1. Rung 0: the fully worked before/after anchor with subgoal labels (the Model stage).
2. Rung 1..n: backward-faded COMPLETION items. Each item prints its own partial solution in the stem, so it is
   self-sufficient and isolation-safe. Blank the LAST move first; keep earlier moves visible as built-in
   scaffolding (Claims 2 and 3).
3. Principle-naming self-explanation delivered as SCORED discrimination items ("which rhetorical move is this
   sentence doing?"), not free "explain what you did" prompts. Generic self-explanation stacked on other cues
   can hurt via redundancy; prompt for the structural principle only (Claim 4; Barbieri et al., 2023,
   https://danamillercotto.com/uploads/4/7/7/2/47725475/barbieri_et_al__2023__we_meta-analysis.pdf).
4. Consistent subgoal labels across the whole ladder as the through-line (Claim 5).
5. End the ladder in full paragraph production scored by the rc.* grader.
6. Any adaptivity at the seams (an external-grader production score routing the next lesson variant) is UNBUILT
   and assumed-pending-eng, never inside an item (Claims 6, 7, 9). The lesson ships as a self-sufficient fixed-
   fade sequence requiring zero routing; seam-routing is contingent on the platform actually supporting next-
   lesson routing on a grader score. The fixed-fade benefit is captured with or without it.

---

## 6. Function-over-form device instruction (limited relevance here)

Function-over-form is a T6/sentence-craft concern, not T5's core. It applies to T5 only in the narrow case
where the substantive gap the rubric flags is a MISSING sentence-level move (for example, the higher anchor
credentials its source with an appositive and the lower one does not). When that is the gap:

- Frame the device by the JOB it does, not by its grammatical name, and require the student to USE it in the
  revision. Teaching devices as forms to identify or define has null-to-negative effects; function-plus-
  application is what worked (research_function-over-form, Headline 1 and 3; Fearn and Farnan, 2005, When Is a
  Verb?, https://files.eric.ed.gov/fulltext/EJ787964.pdf; sentence-combining d near 0.50 in Graham and Perin,
  2007).
- Bake the "why this structure creates this effect" talk INTO the worked example and the answer rationales,
  because there is no live teacher to supply it and the contextualised-grammar gains depended on that talk
  (research_function-over-form, Synthesis; Myhill et al., 2012, https://eric.ed.gov/?id=EJ959614).

**The modifiers-by-function become the "what to check" list for a provided draft (light touch).** T5 does not
teach these moves; it treats them as the concrete REVISION TARGETS a student hunts for in a provided anchor.
When a rubric gap is sentence-level, check the provided draft for whether each move is present and doing its job:
- because / but / so -> is the claim-to-reason-to-consequence link made explicit?
- appositive -> does the draft credential its source with AUTHORITY (name the researcher or source)?
- prepositional phrase -> does it add CONTEXT or narrow SCOPE where the claim is vague?
- relative clause -> does it introduce the CONSEQUENCE the "so-what" needs?
Score whether the FUNCTION landed in the revision, never whether the student can label the structure.

Gate note: mechanics are app-owned. AlphaWrite owns sentence-combining craft (G3-8) and EGUMPP owns conventions
(G3-10); T5 treats them as retrieval-gated, already-applied prerequisites and never re-teaches the mechanics
from scratch. It checks only whether the rhetorical FUNCTION was executed in the provided draft.

Do NOT build "which of these is the appositive?" identification items as a revision route; that is the approach
the evidence rejects. Keep the rubric scoring whether the FUNCTION was executed, not whether the student can
label the structure.

---

## 7. The 19 lesson_contract gates: sharpest risks for T5 and how to satisfy them

The contract runs 19 gates (`shell_completeness, model_sequence, discrimination_before_production,
binding_integrity, bank_partition, calibration_discipline, grader_routing, timeback_native, no_source_markup,
no_prior_work_reference, define_before_use, content_depth, model_before_required, no_ambiguous_reference,
unit_ladder, type_ceiling, effect_size_honesty, mnemonic_status, no_em_dash`). Ranked by how sharply they bite
THIS archetype (EXT gate table):

| Rank | Gate | Why it bites T5 | How to satisfy it |
|---|---|---|---|
| 1 | `no_prior_work_reference` | T5 is literally "revise a draft," but stateless QTI + blank retake mean you can NEVER say "revise your paragraph from Step X." | Supply the draft to revise INLINE as a provided anchor; write the prompt to stand alone. Revision runs on PROVIDED pairs, not look-back. |
| 2 | `calibration_discipline` | The archetype IS a predict-then-reveal engine; person-praise and grade-only reveals are auto-rejected. | Every `self_score` precedes a graded reveal. Feedback is GOAL/NOW/NEXT at process level. No "great job," no bare score. |
| 3 | `type_ceiling` / `unit_ladder` | Temptation to "calibrate a whole essay" is out of type (that is T7). | Cap scored production at a paragraph. Every production declares a unit; units are non-decreasing. |
| 4 | `discrimination_before_production` | Boundary-pair discrimination (a 2 next to a 3) is the highest-value T5 move and must come first. | Place the boundary pair BEFORE the paragraph FRQ; set `labeled_grade_c=True`. |
| 5 | `no_ambiguous_reference` | T5 shows several anchor papers at once, so "this version / that draft" ambiguity is constant. | Quote the referent inline or bind a stimulus ref inside the SAME slot; never rely on "the anchor above." |
| 6 | `effect_size_honesty` | Calibration rests on self-assessment for writing (near 0.62), calibration trainability (g near 0.177) and the over-estimation bias (g near 0.206), NOT SRSD's 1.14 and NOT Hattie and Timperley's roughly 0.79 GLOBAL feedback aggregate (which folds in stateless-blocked feedback modes). | Do not claim 1.14 or the 0.79 global figure for the async engine; cite the calibration/self-assessment-specific warrant instead. |
| 7 | `model_sequence` / `model_before_required` | The before/after must be low-anchor vs high-anchor with a predict-the-fix and a SCAFFOLDED diagnosis. | Include a literal BEFORE and AFTER, a predict-the-fix carrying a `feedback` reveal, and a diagnosis slot with a fill-in frame (not a blank "diagnose it"). |
| 8 | `grader_routing` | The paragraph FRQ must carry a real `rc.*` config matching the test. | Route to rc.staar (2-trait) or rc.mcas (0-5 + 0-3). |
| 9 | `no_source_markup` | Anchors are display-only; JavaScript is stripped, so students cannot highlight. | Use read-and-note framing; never instruct "mark up" or "highlight" the anchor. |
| 10 | `mnemonic_status` / `define_before_use` / `bank_partition` / `content_depth` / `no_em_dash` / `shell_completeness` / `binding_integrity` / `timeback_native` | Standing hygiene gates. | Declare CHECK as `"proposal"`; define "rubric trait" before use; partition the transfer bank; clear the depth floors; no em dashes; complete all five SRSD stages; ensure every ref resolves in a bank; use only supported QTI item types. |

---

## 8. T5-specific kill-list (do NOT do)

- Do NOT hand the rubric and say "grade yourself" with no feedback reveal (overestimation bias; rubrics-alone
  non-significant) (EXT kill-list; `calibration_discipline`).
- Do NOT ask the student to revise their OWN earlier submission (stateless retake) (`no_prior_work_reference`).
- Do NOT let the student self-score their own draft before judging external anchors (EXT-P10).
- Do NOT scale to a whole-essay revision (out of type) (`type_ceiling`).
- Do NOT teach mechanics-fixing as if it were substantive revision (that is T6) (EXT-P4).
- Do NOT claim SRSD's 1.14 for the async calibration engine (`effect_size_honesty`).
- Do NOT use person-praise or grade-only feedback (`calibration_discipline`).

---

## Retrieval + item rules (LS feedback 2026-07)

These encode the 2026-07 learning-scientist pass as T5 authoring defaults so a fresh rubric-revision lesson clears the new gates by construction. For T5 the checks ARE the content, so the ceiling is the tightest of any type.

- **Cadence ceiling: CHECKING-REVISION tier, ceiling 2** (`gate_check_cadence`). T5 is a checking-and-revision type: a run of COUNTED teach cards may not exceed TWO before a check (a `discrimination`, `predict_the_fix`, or `self_score`). This is by design, because the four-stage judge-then-reveal ladder (A binary, B 3-point, C full analytic, D no-rubric self-diagnosis) is the lesson, not a preamble to it: keep expository teach to the single trait card, then run checks. The before/after anchor pair counts as ONE worked example even if chunked; do not split it. Tag any pure buy-in card `tag="buy_in"` so it counts 0. The memorizable-tool tightening barely applies here (ceiling is already 2), but if a card names CHECK, tag it `tag="memorizable_tool"` and get to the boundary pair fast.
- **Four options per discrimination, each a NAMED MISCONCEPTION** (`gate_structural_item`). The boundary-pair discrimination (a 2 next to a 3) and the gating-principle set each carry exactly four choices; every distractor is a real calibration error (over-rating the thin draft, crediting clean conventions over substance, mistaking length for development), never filler.
- **Diagnosis: the student ANSWERS the check, then improves** (`gate_self_answered_check`). The over-rating recovery model may pre-answer a PROVIDED anchor (name it: "this anchor claims a 3 but never explains after a quote"), but MUST then hand the student an independent turn: predict the score on a fresh anchor, then reveal. Never print a self-check that answers its own "? No," questions and stops. Judging OTHERS' anchors before one's own is the overestimation-bias defense, so the independent turn is non-negotiable.
- **No comma before "because"/"so" in a fill-in frame** (`gate_frame_comma`). The diagnosis frame ("... it now scores higher because ______") drops the comma before because. Emit any side/reason fill-in with `claim_frame()` from `lesson_prompts` rather than hand-writing it.
- **Re-gloss the hard terms.** If the lesson uses controlling idea, warrant, synthesis, or counterclaim, `gate_define_before_use` already forces an in-lesson gloss (rubric-trait terms are defined first anyway). On a later-lesson re-introduction prefer a BRACKETED gloss right after the term (LS #9 style).
- **Stem wording (playbook-only, #7):** name the move directly ("Which single move separates the 2 from the 3?"), never a meta-phrasing.
- **Tone (playbook-only, #5 / Yeager):** state the standard up front; every reveal is GOAL / NOW / NEXT wise-feedback that names the MOVE, no person-praise, no compliment-sandwich. This reinforces the existing `calibration_discipline` gate.
- **Pair a stand-alone improve-write with a `predict_the_fix`** where feasible (playbook-only, #4); in T5 the paragraph revision naturally follows a predict-the-fix on the same trait.
- **Cross-lesson spacing (KH caveat, #3):** the in-lesson cadence gate is necessary but NOT sufficient; the calibration skill must recur in later lessons on new anchors. That durability is a sequence-builder concern, not visible to this lesson's gates.

---

## 9. Keep-it-short note

T5 is worked-example-first and lean. One Teach card (name the trait, the scale, the gating principle). One
before/after anchor pair, one predict-the-fix, one scaffolded diagnosis in Model. A short boundary-pair ladder
(A to B to C) in Supported, reusing anchors rather than authoring long new ones. Stage D plus one paragraph
revision in Independent. One fresh partitioned anchor in Transfer. Every anchor transforms exactly ONE dimension
for the contrast (length, topic, and position must not correlate with correctness), and each step uses a single
interaction type (EXT-P20). Depth floors are minimums, not targets. Reusing published or already-authored
anchors keeps redundancy and cognitive load down and keeps the lesson short.

---

## Open risks and Timeback blocks (flagged honestly)

- BLOCKED: iterative revise-and-recheck on the student's OWN text across items, and any feedback that references
  a prior answer or score. Re-engineered as predict/judge on PROVIDED anchors plus one self-assessed fresh
  submission (research_feedback-as-teaching, 2.2 and 2.3). The self-fix-when-prompted coaching statistic depends
  on a coach seeing the live draft; that turn-to-turn loop is not deliverable.
- BLOCKED: true within-lesson adaptive fading. Only fixed fading ships. Between-lesson routing on a grader
  score is UNBUILT / assumed-pending-eng, not a delivered capability; it is contingent on the platform actually
  supporting next-lesson routing. The lesson is a self-sufficient fixed-fade sequence requiring ZERO routing to
  function (research_worked-example-fading, Claims 7 and 9).
- BLOCKED: cross-session goal-setting and longitudinal self-monitoring/graphing. Substitutes: bake the goal into
  the prompt; collapse self-monitoring to a within-item self-check script (research_async-srsd, Section 5d).
- CAVEAT: CHECK is a `proposal` mnemonic, unverified; keep it labeled as such.
- CAVEAT: discrimination-before-production is an internally UNVALIDATED heuristic (kept and labeled), not a
  proven law.
- CAVEAT: the appositive-equals-authority style function map is a design convention we impose for clarity, not
  a finding lifted from a study; pick the cleanest exemplar function per device and do not overclaim
  (research_function-over-form, honest-gaps).
