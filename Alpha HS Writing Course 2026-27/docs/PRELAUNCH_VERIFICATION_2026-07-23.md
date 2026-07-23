# Pre-Launch Verification (2026-07-23)

Full read-only check that all four AlphaWriting courses are up to date in Timeback and grading is functional,
before launching student agents to evaluate the courses.

## 1. Courses up to date (ALL PASS)
Every course: correct title, active, published, timebackVisible, correct tree.
- AlphaWriting G9  (hs-writing-g9-2026):  5 units / 29 topics
- AlphaWriting G10 (hs-writing-g10-2026): 4 units / 25 topics
- AlphaWriting G11 (hs-writing-g11-2026): 8 units / 31 topics
- AlphaWriting G12 (hs-writing-g12-2026): 2 units / 16 topics

## 2. Resources resolve (101/101 lessons PASS)
For every lesson in all 4 courses: the ARTICLE resource resolves and its LearnWith contentUrl fetches a live
gated lesson.html (tb-* markup confirmed = current format), AND the PP100 mastery test + its MASTERY-FRQ item
both exist. G9 29/29, G10 25/25, G11 31/31, G12 16/16.

## 3. Grading functional (12/12 combos PASS)
Every distinct (rubric, grain, frq_type, mode) combination the live courses use returns a real non-zero,
correctly-scaled score over the live grader (hs-writing-grading.onrender.com/score):

  rc.4trait essay writing (default)        -> 11/24    (panel_ccss argument)
  rc.4trait essay writing analysis         -> 14/16    (panel_ccss analysis)
  rc.4trait multi_paragraph writing        -> 8/24
  rc.4trait paragraph revision             -> 6/10
  rc.4trait paragraph writing              -> 6/10
  rc.4trait sentence writing               -> 3/3
  rc.staar  essay writing                  -> 3.5/5
  rc.staar  multi_paragraph writing        -> 2/5
  rc.staar  paragraph revision             -> 6/10
  rc.staar  paragraph writing              -> 6/10
  rc.staar  sentence revision              -> 2/2
  rc.staar  sentence writing               -> 3/3

All grain routing correct (sentence/paragraph no longer mis-routed to the essay engine), rc.4trait scores in
both modes, rc.ap correctly deprecated (503). Grading is functional across all four courses.

## Verdict
GREEN for launch. Courses current, resources resolve, grading works end to end.

## Note on "student agents"
The Timeback-player testing agent is SPEC-ONLY (docs/superpowers/specs/2026-07-23-timeback-player-testing-agent-design.md);
pipeline/player_test/ is NOT built. "Launch student agents" = build that agent first (a separate task), then run it.
