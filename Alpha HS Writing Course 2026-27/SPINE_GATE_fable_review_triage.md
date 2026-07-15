# Fable-5 gate review - triage (2026-07-15)

Fable reviewed the 6 rewritten scaffold-free gates from their RENDERED student-facing text. Verdict: fix_first, with 6 blocking issues. Triaged genuine-vs-artifact against the ACTUAL source/structure (not the truncated render Fable saw).

## ARTIFACTS (from the review harness truncating segments to 400 chars - NOT defects)
- **"Synthesis gates render only ONE source"** (called blocking): FALSE. Verified the held-out sources have multiple passages: CONGESTION=2, SYNTH-SET-0002=4, SYNTH-SET-0001=4. The extraction script showed only the first passage title, so Fable inferred a single source. Full multi-source sets ship. No fix.
- **"SUPPORTED is a graded teaching frame / double-write"** (called blocking, ALL gates): FALSE. Every gate's SUPPORTED plan slot is `scored=False` (the verdict's optional ungraded plan affordance); only the TRANSFER write is `scored=True`. So each gate is: unscored plan + ONE scored cold write = exactly the spec. Fable could not see the `scored` flag from rendered text. No fix.
- **"Pre-write bare moves cue not visible"** (ALL gates): FALSE. The teach_card carries the ONE_IDEA callout + a `<ul>` moves-checklist; the 400-char truncation cut it. No fix.
- **G12 "duplicate Cross of Gold / missing argument stimulus / 4 writes for 3 essays"**: FALSE. s02=unscored plan, s04/s06/s07 = the 3 cold FRQ writes; the argument FRQ carries its prompt inline via setapart (argument FRQ has NO source by design). Not duplicated. No fix.

## GENUINE (fixed in G12)
1. **G12 plan leaked the FRQ type labels** ("FRQ 1 (synthesis), FRQ 2 (rhetorical analysis), FRQ 3 (argument)") while the post-hoc self-score grades "did you name each type." Answer-giveaway at a gate. FIXED: the up-front plan is now BUDGET-ONLY (no type labels); naming each type moved to each FRQ's own moment where its tell is visible.
2. **G12 plan slot preceded any source** (s02 before s03) yet asked the student to "name its type from the tell" with no tell on screen. FIXED: the plan now sets only the time budget up front; type-naming happens at each FRQ. The three FRQ source/write slots no longer pre-name the type in title or body (naming is the assessed skill).

## STYLE NITPICK (declined, defensible)
- **"Predict, then see your grade -> reword to post-hoc self-score"**: declined. The self_score IS post-hoc (after the scored write). "Predict then reveal" is the deliberate calibration frame (the self_score's purpose is to train the student to predict their own result and compare to the grade). Changing it would contradict the calibration design (W&H: self-assessment overestimate bias is trained OUT by predict-then-compare).

## Net
5 of 6 gates needed NO change (the flags were truncation artifacts). G12 had 2 genuine answer-giveaway/sequencing issues, both fixed; G12 stays 1/1 + render + grain-conformant. All 6 gates remain green.

## PROCESS NOTE for future Fable reviews
The review harness truncated rendered segments to 400 chars and showed only the first passage title per source. That caused ~4 false "blocking" findings. NEXT Fable review (the full post-build readiness audit) must feed the FULL rendered text + explicitly state which slots are scored, or triage every "not visible"/"only one source" finding against the source before acting.
