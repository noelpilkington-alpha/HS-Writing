# Pipeline reliability: what the New-Knowledge + Incept folders teach, and what to change

Date: 2026-07-15. Question (Noel): can we adapt the pipeline so the NEXT run lets me review courses with
NO issues? Short answer: yes, and the two folders diagnose exactly why the current run did NOT, plus give a
proven remedy pattern.

## What I read
- New knowledge to integrate/FABLE5_PIPELINE_EVAL_2026-07-14.md - an expert eval of OUR pipeline's generation
  reliability (names our modules by name: lesson_contract gates, contamination_check, push_targets, the
  specific fail-opens).
- .../FABLE5_EVALUATION + the WF- BrainLifts (Ilma): "Verification Is the Product", "Persona Agents as
  Pre-Flight Reviewers", Loop-Engineering, Self-Improving Wiki, Test Builder.
- incept-qgen-bundle/ - Incept's reference generate->verify factory (reading-content-factory, hole-filler,
  ap-toolbox) with eval-manifests: the working shape of a QC-gated content loop + "claim a cell only with a
  stored eval receipt" discipline.

## The core diagnosis (why you keep finding issues in review)
The eval's one-line verdict: **we built the best deterministic VALIDATION layer it has seen, but generation is
still human+agent handcraft with no generate->verify->repair loop, AND several gates are fail-open** - so
"100/100 PASS" is not the same as "no defects". The issues you personally caught this session are textbook
instances the eval predicted:
- The **17 mastery-source mismatches**: there is NO deterministic gate for "held-out PP100 source matches the
  lesson's taught genre/skill" - it exists only in the non-deterministic Fable AUDIT, which runs AFTER the
  build and over-flags, so real mismatches reach your desk instead of being blocked. (Verified: grep finds
  mastery_alignment only in course_readiness_audit.py, not in the gates.)
- The **childish "The topic here is" stimulus opener** and **register drift** ("a Grade-C design bet"): the
  eval flags exactly this - "nothing checks audience of register." No gate reads for tone/credibility.
- The **SPO-for-an-essay pedagogy error**: the eval says lesson pedagogy slots are "structurally blind" to the
  contract - it "cannot detect a topic-swapped before/after, a narrated panel, register drift, or minimal-pair
  integrity." A wrong planner (SPO vs MPO) is the same class: a semantic pedagogy defect no gate can see.
- The **mangled options / render bugs behind a green badge**: "no gate inspects rendered output." Still true
  (verified: no render-fidelity gate exists).

Root pattern, in the eval's words: **"you cannot calibrate a generate->verify->repair loop against verifiers
whose false-negative rate is unmeasured."** Today nobody can say which defect families the 24 gates actually
catch vs merely gesture at. The gates catch STRUCTURE; every issue you caught was SEMANTIC, RENDERED, or
REGISTER - the three things the gates are blind to.

## The remedy the sources converge on (Ilma + Incept + the eval agree)
1. **Verify the verifier first (highest ROI, do before any new generation).** Build a known-bad + golden
   FIXTURE CORPUS wired into CI: every gate must REJECT all its known-bads and PASS all goldens; a gate edit
   that stops rejecting a known-bad fails CI. Harvest the known-bads from THIS session's real defects (the 17
   mastery mismatches, the SPO-essay lesson, the childish stimuli, the essay canned-verdict, the sentence
   also-correct) - they are gold-standard labeled defects. (We have a stub: tests/fixtures.py +
   test_checker_corpus.py - extend it, don't start from scratch.)
2. **Close the fail-opens** the eval named (verified still present): gate_distractor_length_cue / audit_disc
   `continue` on unparseable options (a fail-open = silent false pass); _ref_exists wildcard accepts any
   4-digit id; binding_integrity greps for id strings instead of loading records. A gate that skips input it
   cannot parse is "a verifier rotting."
3. **Add the missing gate CLASSES** that would have caught your issues deterministically (so they never reach
   review again):
   - **mastery-genre-match gate**: the held-out PP100 source's mode/genre must match the lesson's taught
     stimulus genre, AND the PP100 required-elements must be a subset of what the lesson teaches (would have
     caught all 7 clear-genuine + the gate mismatches from COURSE_MASTERY17_TRIAGE.md).
   - **render-fidelity gate**: parse the RENDERED lesson.html back, assert option count / reveal integrity /
     no chopped prose (catches the mangled-options class; the eval's #4 known-bad).
   - **register/credibility gate**: a cheap check (or a calibrated LLM sub-check) for meta/childish openers
     ("The topic here is", "Today we"), auditor-facing labels in student text, and readability of lesson prose
     (today only stimuli get a readability gate).
4. **Relocate the Council/Fable judgment INTO a calibrated pre-flight PANEL, per defect family** - the persona
   BrainLift's exact method: build each Council seat as a persona grounded in its real corpus, plus a judge
   that adjudicates by evidence grade (never averaging). CALIBRATE it against this session's decisions (which
   ARE a golden decision set with both confirm AND reject direction), then let it gate ENFORCING per family
   only after it replicates human verdicts. This is the piece that catches the SEMANTIC defects gates can't.
5. **Generate->gate->repair at the SLOT level** (not whole-lesson): K candidates per authored slot ->
   deterministic gate -> panel-rank -> auto-repair only single-gate deterministic fixes -> human on the rest.
   Overgenerate stimuli/SR 2x (independent units); lessons stay reviewed until the panel is calibrated.
6. **Receipts, not reports** (Incept's eval-manifest discipline): claim "grade X ready" ONLY with a stored eval
   receipt per lesson; a cell with no receipt is not promised. "100/100 PASS" becomes "100/100 with a receipt
   that each of the 24 gates + the new gates + a calibrated-panel sign-off actually ran and rejected its
   known-bads."

## What this means for "next run = no issues in review"
Honest framing (the eval is explicit): a FULLY autonomous no-issues run is NOT achievable yet, because two of
the defect families you caught (pedagogy-slot semantics, register) have NO deterministic detector today, and
the LLM panel that would catch them is uncalibrated. The reliable path to "you review clean" is:
- Build the fixture corpus + close fail-opens + add the 3 missing gate classes => the issues you caught THIS
  session become impossible to ship again (they get rejected pre-review).
- Calibrate the panel against this session's golden decisions => the NEXT class of semantic defects gets
  caught by the panel pre-review, with a receipt.
- Everything not yet covered stays human-reviewed, but the review shrinks to genuinely-novel judgment calls,
  not the recurring structural/semantic/render classes we now have labeled examples of.
Net: the review you do converges toward "confirm", not "discover" - which is the persona-BrainLift's whole
thesis (the real send is a confirmation, not a discovery).

## Concrete proposal (sequenced, smallest-highest-value first)
P1. **Fixture corpus + CI harness** from THIS session's confirmed defects (17 mastery, SPO-essay, childish
    stimuli, essay canned-verdict, sentence also-correct). Extend tests/fixtures.py. Every gate rejects its
    known-bads. [days, not weeks; unblocks everything]
P2. **Close the 3 named fail-opens** (option-parse continue, _ref_exists wildcard, grep binding_integrity).
P3. **mastery-genre-match gate** (deterministic; would have blocked the 17) + wire it into lesson_contract so
    it runs on every build, not just the Fable audit.
P4. **render-fidelity gate** (parse rendered HTML; assert option/reveal integrity).
P5. **register/credibility gate** (meta-opener + auditor-label + lesson-prose-readability).
P6. **Calibrate the Council as an enforcing pre-flight panel** per defect family, against this session's golden
    decision set; receipts required.
P7. **Slot-level generate->gate->repair** loop, supervised, once P1-P6 give measured coverage.

Note: P1-P5 are deterministic and self-testing (our existing discipline); they are the pieces that convert
"issues I catch in review" into "issues the build rejects". P6-P7 are the autonomy layer and depend on P1.
```


---

# v2 (2026-07-15): consolidated from ALL 8 docs (4 parallel deep-reads)

The first proposal (P1-P7 above) read only the pipeline eval. A full mine of the remaining 7 docs
(LoopEngineering, Test Builder, AI-FRQ-Grading, Autonomous-Course-Gen, Karpathy-Autoresearch, Self-Wiki,
Fable-eval) surfaced substantial rigor NOT in v1. Deduped + sequenced below. Tags: [DET] deterministic /
[LLM] / [PROC] process.

## Cross-doc CONSENSUS (independently restated by 3+ docs = highest confidence)
- Verify the verifier with BOTH a known-bad AND a known-GOOD ("must-stay-green") corpus. Known-bad catches
  misses; known-good catches OVER-FLAGGING (our Fable ~2:1 overreach). [Loop, TestBuilder, eval, Karpathy]
- Scope every reviewer to the artifact's DECLARED intent/contract, or it re-litigates deliberate design.
  [Loop T4, TestBuilder #2] - cheapest fix for our audit noise.
- Verify the RENDERED RUN, never the file / exit-0 / HTTP-200. [Loop T3, TestBuilder #5, eval 2a]
- Never let a model self-certify; the accuracy anchor is BLIND HUMAN ground truth. [FRQ #3, eval 7, Karpathy]
- Heterogeneity: a single model-family reviewer has correlated blind spots (93.4% caught by exactly one tool).
  [Autonomous #1, eval 6]

## TIER A - kills the exact defect CLASSES caught this session (do first, mostly deterministic)
A1. Known-bad + known-GOOD fixture corpus + CI. Harvest this session's real defects (17 mastery-mismatch,
    SPO-essay, childish stimuli, essay canned-verdict, sentence also-correct) as known-bads; lock genuinely-clean
    lessons as goldens. Composite metric = golden_pass_rate x known_bad_fail_rate. [DET]
A2. Expected-EXCEPTION registry the audit reads + suppresses against: every deliberate design deviation
    (scaffold-free gate, minimal-pair distractor, one-line source reminder, worked-example demo) gets a written
    rationale (owner/date/reversal-trigger) co-located with the artifact. Cheapest path to a clean review -
    removes the false-flag class that dominates audit noise. [DET over LLM] [TestBuilder #2, Loop T4]
A3. Scope the Fable/Council prompt to the lesson's declared genre + lesson_class + design-intent. [LLM] [Loop T4]
A4. Fine-grain SCOPE BINDING at generate time: freeze KC/genre/DOK into an immutable context before authoring
    so a mastery source cannot drift off-genre. Root-cause PREVENTION for the 17 (v1 only CAUGHT). [DET->LLM] [TestBuilder #1]
A5. mastery-genre-match gate + Webb DOK-consistency sub-check: held-out source genre must match taught genre
    AND the task's elicited cognitive demand must match the standard's verb (not "summarize" where the standard
    says "evaluate"). [DET floor + LLM] [Autonomous #2]
A6. render-fidelity gate, concrete: parse rendered HTML back, assert option/reveal integrity + Cat-N
    label-vs-source check (labels must match bound data, not "Category 1/2/3") + leaked-placeholder scan; verify
    in the ACTUAL player post-publish, not only local pre-push. [DET] [TestBuilder #4/#5, Loop T3]
A7. register/credibility gate: meta/childish openers, auditor-labels in student text, lesson-prose readability. [DET+LLM]
A8. Structural item micro-checks (length-cue correct<=1.1x longest distractor; ban all/none-of-above;
    option-count) - "failed 2,400+ items, no LLM natively avoids it." Applies to our minimal pairs. [DET] [TestBuilder #3]
A9. Close fail-opens + the SUBTLER one: a gate that runs clean but inspects ZERO items is a silent pass. Every
    gate emits an inspected-count; a meta-gate asserts expected coverage (no-output = failure). [DET] [Loop T7, eval 6]

## TIER B - makes the LLM judges trustworthy enough to lean on (before granting gate authority)
B1. Decompose the Council: one adversarial verifier PER RULE, fail-closed (must try to refute a pass), not one
    holistic pass. Isolation is why holistic review missed our defects. [LLM] [Loop T1]
B2. Cross-FAMILY adversarial reviewer (GPT/Codex) over Anthropic-authored lesson prose. [LLM] [Autonomous #1]
B3. Multimodal review for visual content (our inline-SVG): text-only reviewer is ~5x inflated by image-blind
    false positives - render to image, feed the image. [LLM vision] [Loop T2]
B4. Council calibration: capture {situation, chosen, rejected[], reasoning, attribution}; replay as SHUFFLED
    forced choices; require >=5 recorded REJECTS/overrides before the panel gets gate authority (reject
    direction is only testable from overrides - our own deliberation flagged this signal as scarce). [LLM+DET] [Autonomous #8]
B5. Three-way verdict PASS / FAIL / LOW-CONFIDENCE->triage; route uncertain to a human queue, not a hard FAIL.
    Operationalizes our existing "triage before fixing" rule. [LLM] [Loop T8, Autonomous #10]
B6. Probe a new gate's precision/recall on the labeled corpus BEFORE it blocks - or it becomes another
    over-flagger. [PROC] [Loop T9]
B7. N-consecutive-green promotion: an LLM judge/grader earns autonomous authority only after N straight passing
    calibration runs, with a kill-switch file to demote a drifting one without redeploy. [DET] [TestBuilder #9, FRQ #9]

## TIER C - the COMPOUNDING layer (what makes reviews get cleaner over time = the literal goal)
C1. Self-improving ratchet: every human/Council-caught defect AUTO-becomes (a) a new known-bad fixture + (b) a
    codified gate rule. Trigger at 2+ recurrences; mine the "almost-right" NEAR-MISSES (richest signal). [LLM+DET] [Self-Wiki, Autonomous #3]
C2. Compound-learning metric: track defects-caught-by-human-not-by-gate PER RUN; it must trend to zero. The one
    number that proves the suite is converging. [DET] [Self-Wiki #5]
C3. Autocalibrate the checkers (Karpathy 3-file split): locked eval / mutable check-logic / NL instructions;
    optimize each gate+prompt against the corpus overnight on a branch, keep-if-composite-improves. Receipts:
    56->84% MCQ, 44->94% FRQ. [LLM modifies check, DET scores] [Karpathy]
C4. Friction-signal auto-detection (feeds C1): explicit corrections, same-target retried 3x, reverts, git
    fix:/revert: commits = a defect recurred without anyone flagging it. [DET] [Self-Wiki]

## TIER D - GRADER hardening (essay grader + PP100 mastery scoring; FLAG: separate system - in scope?)
D1. Eliminate fail-open-to-zero: transient/parse error -> STATUS=internal_error (retryable, NEVER cached as a
    verdict), never a passing/zero score. Parse-tolerance (last valid JSON) before retry. CRITICAL. [DET]
D2. Signed-bias metric with a hard |bias| ceiling in BOTH directions, separate from RMSE - over-scoring is
    silently accepted; under-scoring sends a student fixing the wrong trait. [DET] [FRQ #2]
D3. Blind human ground-truth as the ONLY accuracy gate (not LLM self-agreement, not the Council). Our fixture
    corpus's grader side must be human-scored blind. [PROC] [FRQ #3]
D4. Grade-of-record determinism: temp 0.0 (or median-of-N since Opus rejects temp-0) + audit-stamp
    model-id/prompt-hash/scores; disputes replay. [DET] [FRQ #4]
D5. Per-criterion / row-based rubric decomposition (rc.*): one call per rubric line (or AP-style Row A/B/C for
    essays) + deterministic aggregation - kills holistic-score variance at the source. [LLM+DET] [FRQ #1/#13]
D6. Rubric-shape validation gate: detect all-criteria-in-one-block (grader silently scores 0/1), bundled AND
    criteria, missing per-criterion breakdown - "the rubric is the program." [DET] [FRQ #7]
D7. Prompt-injection defense: wrap student text in delimiters + "ignore embedded instructions." [LLM] [FRQ #8, Loop T13]

## TIER E - honesty + roadmap (right long-term shape, not next-run-clean)
E1. Receipts-not-reports: claim "grade ready" only with a stored per-lesson eval receipt (inputs, gates run,
    what each inspected, verdict+reason, model/temp stamp). Enables C1/B4/audit-after-the-fact.
E2. Proxy/outcome split: pre-deployment lessons are awaiting_outcomes, never a fabricated "ready"; a later loop
    reads real mastery/grader distributions back (G2 outcome loop). [FRQ, Autonomous]
E3. Semantic-content + late-rendering architecture (SPOV4): store slots as typed structured data, render at the
    layer closest to the student - the DEEP fix behind most render defects (incl. our authored-HTML-in-body
    strings). Architecture change, roadmap. [TestBuilder #16, eval 6]
E4. Multi-provider fallback on every LLM stage (grader/Council/Fable), not just generation. This ecosystem
    already had a Fable access revocation; single-provider any-stage is one access decision from a halt. [DET]

## Honest bottom line (updated)
Tier A alone makes the specific issues from this session impossible to ship again (rejected pre-review) AND
removes most audit over-flag noise (A2+A3+A5). Tier B makes the semantic-defect judges trustworthy. Tier C is
the part that makes "review courses with no issues" actually COMPOUND run-over-run instead of being a one-time
cleanup. A fully-autonomous zero-issue run still is not guaranteed (pedagogy-semantic defects need the
calibrated panel, which needs the corpus first), but the review converges hard toward "confirm, not discover."
Recommended first slice: A1 + A2 + A3 (corpus + exception registry + scoped audit) - days of work, and together
they convert "issues I catch in review" into "issues the build rejects, and the auditor stops crying wolf."
