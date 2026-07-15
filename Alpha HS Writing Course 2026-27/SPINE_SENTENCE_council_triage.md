# Sentence-grain Council review - triage (2026-07-15)

3 lenses reviewed the 35 newly-added second discriminations: TWR + K&H (subagents) + DI (done in the main loop
after the subagent died twice in a Bedrock timeout window; main-loop DI could read the full per-option "why"
strings the subagent surface omitted, so it was a MORE complete faultless-communication review).

## Verdicts: all three go_with_fixes
- TWR: 1 concern (C901-0006 also-correct). 32/35 clean; type-3 evidence pairs a soft note only.
- K&H: 0 blocking. Confirmed cue-stripping interleaving is the right design; no literal near-duplicates. 6
  lessons "acceptable, not rejects" (same axis + new content; cheap-to-strengthen, NOT required).
- DI (main loop): 34/35 clean faultless-communication minimal pairs; each "why" isolates the criterial feature.
  1 genuine also-correct: C901-0006.

## GENUINE FIX (1) - applied
ACC-W910-L-G9-C901-0006, added discrimination "Argue task: which sentence is the right product?": the stem
asked only "which sentence fits the ARGUE verb?" - option B ("Schools should switch to a four-day week") takes
a side and thus fits the literal verb, so B was also-correct; the key C turns on having a REASON the stem never
required. FIX: stem now states "An argue task calls for a claim that takes a side AND backs it with a reason.
Which sentence is that finished product?" so B (side, no reason) is unambiguously wrong and C is the only
correct answer. Re-verified 1/1 + render + grain-conformant.

## DECLINED (not defects)
- K&H's 6 "same-axis" lessons (C902-0008, C903-0013, C1005-0012, C1107-0025, C1107-0026, D1201-0015): K&H
  itself rated these acceptable varied practice, not rejects. For content-bound skills (relevance, warrant)
  new content IS defensible practice. No change.
- TWR's soft note on the type-3 evidence pairs (C902-0007/0008): legitimate analytical reps; the discriminator
  is fact-accuracy/relevance, correctly keyed. No change.

## Process note
The subagent review surface omitted per-option "why" strings (K&H flagged this gap). Doing DI in the main loop
with full whys closed it. For future reviews under API instability, prefer main-loop review of the highest-risk
grain over fragile subagents.
