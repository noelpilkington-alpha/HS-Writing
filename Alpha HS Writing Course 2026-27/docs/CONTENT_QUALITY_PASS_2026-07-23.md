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
