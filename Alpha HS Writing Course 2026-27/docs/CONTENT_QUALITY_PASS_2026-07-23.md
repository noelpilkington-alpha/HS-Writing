# Content-Quality Pass (2026-07-23) - findings beyond delivery

The delivery-eval verifies MECHANICS (renders, video pauses, gate returns a score). This pass judges CONTENT
quality - the things "delivery-clean" does NOT cover. Multi-lens on a sample + the two deterministic audits
course-wide.

## Deterministic audits (course-wide, TRIAGED - raw counts are noisy)

### Semantic / provenance audit (lesson_content_audit.py): 4 raw flags / 129 files
Globs stale lesson versions, so some flags may be on superseded files. Candidates to check against CANONICAL
files:
- g9_l04_interleave: BINDING - a bound stimulus id looks malformed ('FRAME-VOLCANOES + FRAME-FOURDAYWEEK')
- g9_l05_integrate_quote: FIGURE '50 million' not in bound source (school-lunch)
- g10_l15_evidence_pool: ATTRIBUTION 'BLS' not in bound source (this is inside a STUDENT-DRAFT example, likely fine)
- g11_l27_synthesis_rehearsal: FIGURE '34 percent'/'23 percent' not in bound source (capacity factors)
-> ACTION: verify each against the canonical bound stimulus; fix any genuine provenance drift.

### Pedagogy defect audit (pedagogy_audit.py): raw 45 P1-C confounds -> 4 REAL after triage
The raw "45 discrimination confounds" is HEURISTIC NOISE (its 'longest option' compares against truncated
values; fires on near-equal-length options - the known over-flag pattern). Recomputed on CANONICAL lessons with
strict thresholds (correct >40% longer than the LONGEST wrong, OR the ONLY option with a connective):
4 real candidates, all "connective-only":
- g9_l01 (2nd discrim "takes a side AND gives a reason"): correct (C) is the ONLY option with a reason-
  connective ("since"). REAL confound - a student can match the connective token, not the side+reason
  structure. The lesson's OWN notes fixed this on the FIRST discrimination (added 'because' to a distractor)
  but NOT this second one. CONFIRMED, worth fixing.
- g9_l04, g9_l23, g9_l25: same "only-correct-has-a-connective" pattern - check whether pedagogically intended
  (some are order/plan tasks where the connective is incidental) vs a real token-match shortcut.
- P1-A GRAIN-LABEL DRIFT: 8 flags - grain-label vs task-body mismatch; check (may overlap known items).

## Key point on "clean"
The delivery-eval called g9_l01 CLEAN (renders, pauses at 82/131s, grades 3/3). The content pass found a real
ASSESSMENT-VALIDITY soft-spot in the SAME lesson (connective-only correct answer). Delivery-clean != content-
sound; both passes are needed.

## Still to run (LLM lenses, on the sample)
- lesson_review.py (Fable-5 per-lesson student-POV: clarity/engagement/necessity)
- council-of-writing-instruction (review mode: grounded pedagogy critique)

## LLM lens (Fable-5 lesson_review) on the sample - 4 lessons, 1/grade

Sample: G9 l01 (sentence/concept), G10 l07 (paragraph/analysis), G11 l02 (sentence/nuance), G12 l01 (essay).
RESULT: all 4 returned "revise" on ALL THREE axes (operational_necessity, formatting, engagement) - a
CONSISTENT COURSE-WIDE pattern, not per-lesson noise. The recurring items:

1. OPERATIONAL NECESSITY (padding): each teach step carries nice-to-know asides - thesis/rubric jargon,
   motivational pep-talk lines, future-skill disclaimers - beyond what the tasks require. Recommendation: cut
   or move to tooltips.
2. FORMATTING (dense walls): sources + prompts run together into unbroken blocks; source titles duplicated
   into the first sentence; multi-part instructions in one run-on. Recommendation: line breaks / bullets.
3. ENGAGEMENT (repetition + pre-answered checks): full sources reprinted verbatim at each write step
   immediately after being shown; the check-tool checklist restated 4-5x; three near-identical write tasks in
   a row; some worked examples pre-answer their own questions (student just copy-edits). Recommendation: show
   source once + a one-line reminder after; vary the check framing; ensure at least one write is genuinely cold.

CAVEAT (do NOT bulk-act): these are ADVISORY judgments. Some flagged "repetition" is likely DELIBERATE spaced
practice / worked-example scaffolding (the coping-model + check-tool reuse were intentional design decisions).
This is a triage-and-decide list for a human, not a defect count. But the CONSISTENCY across all 4 sampled
lessons/grades strongly suggests these are AUTHORING-TEMPLATE patterns worth a course-wide design decision
(especially the verbatim-source-reprint and pre-answered-check items, which the ORIGINAL Fable eval also
flagged as skim-drivers).

## Verdict of the content pass
The multi-lens sample EARNED ITS KEEP: it found (a) a confirmed assessment-validity confound (g9_l01 discrim 2),
(b) provenance flags to verify, and (c) a systematic prose/repetition pattern across every sampled lesson that
delivery-verification is structurally blind to. Recommend: scale the Fable-5 review to the full course (it is
the lens that surfaced the most, and the pattern looks systematic), triage against deliberate-design intent,
then decide fixes. The Council (grounded-pedagogy) lens is the natural adjudicator for the "is this repetition
deliberate or defect?" calls.

## COUNCIL ADJUDICATION - deliberate vs defect (6 seats: TWR, SRSD, DI, K&H, Yeager, Elbow/Gallagher)

Ruled by evidence strength, not averaged. Verdict per finding-family:

### F1 (padding) = SPLIT
- CUT (unanimous, all 6 seats): rubric/thesis jargon a step does not invoke + future-skill disclaimers. Pure
  extraneous load (load-additivity, A) / signal-diluting clutter (faultless communication, A) / autonomy-
  threatening test-prep register (Yeager, eg readicide).
- KEEP (reframed): exactly ONE motivational beat per lesson, tied to the real standard/strategy, in its own
  bounded frame, stated once, never bare "you're ready", never fused into a teach/check step. Resolution: the
  Yeager-vs-SRSD conflict dissolved once FORM/FUNCTION separated - Yeager's high-standards line = SRSD's
  strategy-tied self-instruction (both Grade A). Bare person-praise is inert (0.12 < no-praise 0.34), so the
  FORM must be standard-tied; a repeated pep-talk degrades into the seen-through compliment sandwich.

### F2 (dense formatting) = FIX (UNANIMOUS - all 6 seats)
Decompose the source+prompt+instruction wall into labeled blocks (SOURCE/PROMPT/YOUR WRITE); multi-part
instructions as one action per numbered line; delete the duplicated title. Guardrail: keep source ADJACENT to
its prompt, annotation ON its exemplar - do not over-split complementary content into a split-attention problem.
This is the safest, highest-certainty change (segmenting + split-attention + redundancy, all A). FORMATTING-ONLY.

### F3 (repetition + pre-answered checks) = SPLIT (4 sub-patterns, opposite rulings)
The reviewer's single uniform "revise" was the error. Corrected frame (K&H, endorsed even by DI): repetition of
a student RESPONSE is protected mastery practice; repetition of PRESENTED CONTENT is redundancy and cut; support
must FADE. Five-to-six seats converge on the fade.
- F3a verbatim source reprinted at each write -> FIX (redundancy effect, Kalyuga 1998, A + the MEASURED
  course fatigue). Show once, then pointer + collapsible + load-bearing excerpt only.
- F3b check-tool restated verbatim 4-5x -> FIX/FADE (expertise-reversal d=-0.428, A + Memorize-It). Teach once
  with coping think-aloud; then invoke by name + collapsible; final write self-invoked, no cue.
- F3c three near-identical writes -> KEEP the count (transfer needs multi-round varied practice, A), FADE the
  scaffold (write1 modeled -> write2 completion -> write3 independent + escalated or student-choice).
- F3d worked example pre-answering its check -> SPLIT: KEEP the pre-answer INSIDE the first Model-It only (show
  the messy coping self-talk, not a clean pre-fill); write2 = completion, write3 = a LIVE check with a real
  decision. A demonstration and a check may never be the same element.

### Losing positions named
- DI's "cut even the reframed motivational beat outright" - rejected (Yeager wise-feedback A shows a correctly
  framed high-standards line has measured positive effect).
- DI's "re-present the stimulus at every step / constant scaffold" - rejected on redundancy + expertise-reversal
  (both A); note DI's OWN filed position actually endorses the response-vs-content split, so the "DI wants
  constant repetition" caricature was not DI's real stance.
- Naive "cut to one write" - rejected (one-and-done buys retention, not transfer).

### KEY TAKEAWAY
The Fable-5 "revise on everything" was PARTLY right and PARTLY wrong, and the Council separated them:
- REAL defects (fix course-wide): verbatim source reprint (F3a), un-faded check-tool restatement (F3b),
  constant scaffold across the 3 writes (F3c), conflated pre-answered checks (F3d), non-invoked jargon +
  disclaimers (F1), dense walls (F2).
- DELIBERATE design to KEEP: the 3 distinct-topic writes (count), the check-tool re-invocation as a routine,
  the Model-It coping demonstration on first encounter, and one standard-tied motivation beat.

## Consolidated author ruleset (8 rules, ranked) - see judge output in session; P1 = present-once, fade-the-
scaffold, response-vs-content test, keep-count+escalate-last; P2 = one-element-one-function, every-sentence-
serves-the-step, chunk-the-surface; P3 = one bounded belief-beat.

## SPLIT: formatting-only (safe, batch) vs content/design (needs authoring judgment)
- FORMATTING-ONLY (schedule first, near-zero risk): all of F2 (walls->blocks, numbered instructions, dedupe
  title); the mechanical half of F3a/F3b (move full source + full check-tool behind a collapsible after first
  presentation).
- CONTENT/DESIGN (do NOT batch-automate): F1 pep-talk reframe + per-step jargon judgment; F3c descending
  scaffold + write-3 escalation; F3d fading pre-answered checks while preserving the coping-model process.
