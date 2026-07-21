# Add Counterargument to G9 (overturns S2)

**Date:** 2026-07-21
**Status:** PLAN (awaiting build)
**Decision owner:** Noel

## What this overturns
S2 (Noel, 2026-07-17) DROPPED counterclaim from the G9 L27 argument gate + PP100, on the rule "it
belongs where the standards/tests place it (G10) unless irrefutable evidence it earns its keep in G9."
Noel is now OVERTURNING that: teach counterargument in G9 as a FULL unit (2-3 lessons), and keep G10's
Counterargument unit as the DEEPER treatment (a spiral).

## Why the overturn is standards-DEFENSIBLE (not fighting the standards)
The original S2 rationale leaned on "standards place counterclaim at G10." On inspection that is only
half-true, and the half that matters supports teaching it in G9:
- **CCSS `W.9-10.1a`** (the standard mapped to BOTH C.9.01 and C.10.01) reads: "Introduce precise
  claim(s), DISTINGUISH the claim(s) from alternate or OPPOSING claims..." The opposing-claims clause IS
  counterargument, and it is a **9-10 BAND** standard, not a grade-10-only standard.
- So CCSS covers counterargument across the whole 9-10 band. The G9/G10 split was a SEQUENCING CHOICE
  (TEKS English II placement + the SRSD "say-show-so-what only" deferral), not a standards mandate.
- Overturning it therefore re-aligns G9 to the CCSS band standard it already claims (W.9-10.1a), rather
  than contradicting the standards. G9 = introduce/handle a counterargument; G10 = counterclaim-aware
  claim + full rebuttal weighing (the depth spiral). Both trace to W.9-10.1a at increasing sophistication.

## The change (4 parts)

### Part 1: New G9 KC
Add `C.9.07` (or next free G9 id) to HS_KCS in pipeline/course_sequence_g9_12.py:
- id="C.9.07", grade="G9", type="D->P" (discriminate-then-produce, matches the recognition->use arc),
  gateway=False (not a course gate; feeds the U4 argument gate), funnel="counterargument",
  name="Acknowledge and answer a counterargument", acc=["ACC.W.ARG.2"] (the same "develop claims AND
  counterclaims fairly" ACC code C.10.01 uses -> shared skill, grade-scaled), ccss=["W.9-10.1a"],
  teks=[] (TEKS places it at English II; G9 leans on the CCSS band + ACC), sec=["ACT.2"].
- NOTE the G9/G10 boundary: C.10.01 stays "Counterclaim-aware CLAIM" (embedding the opposing view INTO
  the thesis + fuller rebuttal). C.9.07 is the INTRODUCTORY handle: name the other side, concede a
  point, answer it in a paragraph. Update C.10.01's name/description if needed so the spiral reads as
  "G9 = handle one; G10 = claim that anticipates + weighs" (deeper), not a duplicate.

### Part 2: New G9 Unit
Insert a Counterargument unit into UNITS for G9. Placement: AFTER U3 (cohesion/paragraph mastery),
BEFORE U4 (the essay gate) -- because the argument gate essay should now REQUIRE a counterargument move,
so it must be taught first. Renumber: current U4 (essay+gate) becomes U5.
- dict(id="G9.U4", title="Counterargument", kcs=["C.9.07"], gateway="C.9.07", course_gate=False)
- (old G9.U4 essay+gate -> G9.U5)
DAG check: C.9.07 depends on C.9.01/02/03 (claim, evidence, reasoning) all taught earlier -> ordering
holds. course_sequence_g9_12.py has a topo_order validator; run it to confirm no DAG violation.

### Part 3: The 2-3 G9 counterargument lessons
Mirror the ARCHETYPE of G10 U1 (which is the proven shape) but at G9 recognition->intro depth. G10 U1 =
[Concede a Point Then Hold / Concede Without Giving Up / Answer the Counterclaim in a Full Paragraph].
G9 version (introductory):
1. **Recognize the other side** (type 2 concept): name a counterargument to a given claim; discriminate
   a real opposing claim from a non-objection. (discrimination-heavy, recognition-first per SRSD.)
2. **Concede then hold** (type 2 concept): the "Although X, Y because Z" move -- acknowledge a valid
   point, then reassert your claim with a reason. Built target sentence shown (writing-course rule).
3. **Answer it in a paragraph** (type 3 or 5): fold the concede+hold into a short paragraph; check it.
Each follows the concept-lesson shape (opening teach_card "The one idea" + worked example +
discrimination + write/self-check) so it inherits the diagram + (eventual) video treatment.
G10 U1 STAYS -- reframed as the deeper treatment: counterclaim embedded in the thesis + full rebuttal +
weighing (verify G10 U1 lesson bodies now reference "you introduced this in G9; here we go deeper").

### Part 4: Re-add counterargument to the G9 argument gate (reverse the S2 removal)
S2 stripped counterclaim from `ACC-W910-L-G9-C904-0029` ("G9 Gate: Write a Complete Argument Essay") --
its task line, one-reminder, checklist item, sentence frame, and PP100 pass criteria. Now that G9 TEACHES
it (Part 3), RE-ADD it to that gate as a required move, at G9 (introductory) depth: the argument essay must
acknowledge and answer at least one counterargument. The informational gate (C904-0026) is UNCHANGED
(counterargument is an argument move, not informational). This makes the gate coherent WITH the new unit
(the original S2 finding was "required but never taught" -- Part 3 removes that contradiction the other way).

## Gate / test integrity
- New lessons must pass the full tier_a_regression floor (all ~30 gates) + anti-slop + provenance.
- course_sequence_g9_12 topo_order + the per-grade unit-ordering DAG check must stay green.
- G9 lesson count 26 -> ~28-29; renumbering U4->U5 shifts the gate lesson numbers (the essay gates move
  later). Lesson IDs are stable skill codes (C904-*), so only display/file numbers shift -- same care as
  the G11 L30/L31 swap.

## Records to update (overturn cleanly, no contradictory docs)
- SIM_STUDENT_FINDING_LEDGER.md line ~101 (S2 "DECIDED: DROP... stays G10") -> mark SUPERSEDED
  2026-07-21: counterargument now TAUGHT in G9 (new C.9.07 unit) + re-added to the gate. Link this plan.
- COURSE_FIX_PLAN_synthesis.md S2 entry (lines ~167-169, 195) -> same supersede note.
- The SRSD design record ("counterargument deferred out of G9 spine") -> note the deferral is reversed;
  G9 now includes an introductory counterargument unit, G10 remains the deeper treatment.

## Open sub-decisions (resolve in build)
- Exact new KC id (C.9.07 assumed; confirm no collision).
- Whether the G9 counterargument unit is 2 or 3 lessons (plan assumes 3: recognize / concede-hold /
  answer-in-paragraph; could compress to 2 if the gate only needs concede-hold + answer).
- G10 U1 rewording extent (light "you saw this in G9, now deeper" framing vs. genuine content deepening
  -- verify G10 U1 isn't now too close to the new G9 unit; deepen if it is).
