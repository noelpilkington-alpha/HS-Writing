# Colleague Review - G9 L01 "Take a Side" (2026-07-23)

Source: "Lesson checked_ AlphaWriting G9 _ Unit 1_ ... Take a Side Someone Could Argue With.docx" (18 notes +
9 screenshots). A human colleague walked the LIVE Timeback lesson. Triaged below; several are LAUNCH-BLOCKING
and my automated delivery-eval MISSED them (see "gap" note).

## P0 - LAUNCH-BLOCKING (real, confirmed on the live course)

### 1. Every G9 lesson serves the OLD per-item QTI "quiz" ALONGSIDE the new article + PP100 (root cause found)
Colleague: "First question I got is broken" (screenshot = raw literal HTML `<div style=...>` shown as
Question 1 of 12), "Other questions are broken too". ROOT CAUSE (verified on the live API): the L01 topic has
THREE active component-resources - cr-<id> (lessonType=quiz -> the OLD July per-item teaching test, which
renders teach-card HTML as raw text), PLUS cr-<id>-article (the new gated-reading article) and cr-<id>-pp100.
The G9 v3.1 overlay push created the new article+pp100 CRs but never RETIRED the old quiz CR on the surviving
topics. SCOPE: 23 of 29 G9 lessons carry the stale old quiz-CR (the 6 new counterargument lessons are clean).
G10/G11/G12 are UNAFFECTED (pushed fresh, no old tree).
FIX: delete (soft-delete) the 23 old cr-<id> quiz links (+ their old res-<id> resources) from the live G9
course, leaving only article + pp100 per lesson. This is the same class as the "4 stale topics" cleanup, but
for the CRs on surviving topics.

### 2. GAP IN MY DELIVERY-EVAL (honest)
My eval tested the ARTICLE url directly and reported G9 "clean" - but a student opening the lesson sees the
whole component tree, including the stale quiz CR. The eval must walk the OneRoster lesson tree (all CRs per
topic) and flag extra/stale resources, not just fetch the article. Add this check before re-certifying.

## P1 - real defects (some already fixed in the L01 Council prototype)

- Non-student-facing text shown to students: the video caption line "...It pauses 2 times for a quick,
  no-penalty check" plus (screenshot image2) the teach card rendered as RAW HTML in the old quiz. The raw-HTML
  is subsumed by P0#1 (kill the old quiz). The caption line is an authored string in gated_reading's video
  card - reword or drop the meta ("pauses N times") half.
- One-Beat check "gameable / matchable to narration": colleague suggests 4 re-worded statements where the
  student weighs which has BOTH a side and a reason. NOTE: the SECOND One-Beat already IS 4 options
  (screenshot image5 - "what two moves turn it into a claim", 4 choices). The FIRST beat ("which question does
  it fail") is more narration-matchable. Worth strengthening beat 1 toward genuine discrimination.
- "Getting a question wrong immediately reveals the answer, no retries, no feedback for wrong answers"
  (One-Beat): this is the non-gating design (correct by council ruling - it's a low-stakes first-encounter
  check, not a mastery gate). But "reveals the answer with no retry" is worth a UX look - a brief "not quite,
  look again" before reveal. NON-BLOCKING; partly a platform behavior.

## P1 - GRADING / XP (real, overlaps known work)

- "Article write did not fire the autograder / no submit button / no feedback on input" (screenshots image8,
  image9): the ARTICLE's in-lesson write tasks are extended-text with NO grader wiring (only the PP100 mastery
  FRQ is grader-wired). So in-article writes accept text but do not score. This is BY DESIGN today (grader
  wired only to PP100 test-out), but the colleague rightly flags the student gets no feedback in the article.
  Decision needed: wire the in-article writes to the grader too, or make clear they are practice (no score).
- "No XP awarded for completing the article section": the article CR carries metadata xp:N but the colleague
  saw no XP. Check whether kind=text article CRs award XP on the platform (may need a different XP field or the
  platform only awards on scored items).
- "Diagnosis check pre-answers itself" (image8: 'No, it just reports a fact. Pick a side.' under each question):
  CONFIRMED the Council + L01-prototype finding. Already fixed in the _proto_ (rows -> 'your call: yes/no').
- Article write "gameable by copy-pasting the paragraph above": the grader could detect/penalise; ties to the
  grader-prompting work.

## P2 - positives + minor
- Video "well scripted, clear, examples of each" (colleague praise).
- Diagrams "clearly labelled + read aloud via TTS for accessibility" (positive).
- "1:20 before the first anchoring question may be long; earlier facts could carry a question" - pacing note;
  ties to the One-Beat cue placement (could add an earlier beat).

## Priority vs the Council content fixes
P0#1 (stale old quiz on 23 lessons) is a HARD LAUNCH BLOCKER and should be fixed BEFORE the Council content
fixes - a student literally sees broken raw-HTML questions today. It is also a small, mechanical, low-risk fix
(delete 23 stale CRs + resources). The Council content fixes are quality improvements; this is a correctness
break visible to every G9 student right now.
