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
