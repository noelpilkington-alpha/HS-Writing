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
