# Adversarial Verification — C1 English I/II Architecture vs. Learning Science

**Mandate.** Audit the *architecture* of `ap-frq-mastery-v2/C1_English_I_II_Lesson_Map.md` (the ~40-lesson, 8-unit English I/II writing sequence) against the learning-science evidence we hold, and try to BREAK it. Default to skepticism. Eight named architectural decisions are under test; every claim cites a source verbatim where possible.

**Sources read in full (verbatim):** `C1_English_I_II_Lesson_Map.md`; `Corpus_Mining/SRSD_Mining.md`; `Corpus_Mining/TWR_Mining.md`; `Corpus_Mining/Engelmann_DI_Mining.md`; `Corpus_Mining/LearningSci_and_House_Docs_Mining.md`; `curriculum_resource_base.md`; the governing `HS Writing Brainlift — English I-II Source-Bound Argument (MVP).md`; and the prior verdict files `Verify_ReasoningBeforeThesis.md` and `Verify_Structure.md`.

---

## Overall verdict: **SOUND-WITH-GAPS**

The architecture's *core moves* — one-skill-per-lesson, comprehension scored separately, discrimination-before-production, paragraph-before-essay, cold transfer gates, frontier concentration — are each independently supported by primary sources we hold, often verbatim and at large effect sizes. I could not break the spine. **But the architecture has three real, load-bearing omissions that learning science says matter and that the lesson map does not encode** (memorization-to-automaticity, retrieval/spacing/interleaving across units, and transcription/timing fluency), plus **two decisions that survive only under a narrower reading than the map states** (reasoning-before-thesis, and per-thread scaffold re-set). The map is not pedagogically wrong; it is pedagogically *incomplete in ways the evidence flags as important for a no-teacher, timed-exam-targeted build*. Hence SOUND-WITH-GAPS, not SOUND.

A structural caveat about the whole audit: the strongest single warrant for several of these decisions is the **internal MVP brainlift**, not external research — and where I lean on the brainlift I say so, because an internal design assertion is weaker evidence than a meta-analytic effect size. The genuinely externally-grounded decisions (CLT, worked examples, comprehension-precedes-production, testing effect, fade) are flagged as such and are the strong ones.

---

## Per-decision verdicts

### 1. Acquisition order (expository U1-2 → argument U3 → synthesis U5 → multi-perspective/ACT U7 → timed U8): **SUPPORTED**

There is a real difficulty/dependency gradient under this order, and it is sourced.

- **Expository before argument** is the TWR ladder verbatim: *"Opinion: … the easiest and is generally assigned to elementary students. … Argumentative: … presents the evidence for both sides but also decides which position has more merit"* and *"Education experts consider argumentative writing the most complex and cognitively demanding form of composition."* (`TWR_Mining.md` lines 138, 142). TWR explicitly calls the lower rungs a *scaffold*: *"Opinion and pro/con writing assignments constitute a scaffold leading to the argumentative essay"* (`TWR_Mining.md` line 217). The C1 map's E1→E2 ordering (U2 expository → U3 argument) sits directly on this.
- **Synthesis after single-source argument** is the brainlift's developmental target made concrete: synthesis is *"the creation of an argument no single source contains"* (`MVP.md` SPOV 6, line 153) and *"knowledge-transforming is a ceiling, not a floor"* (line 83) — i.e. it presupposes the single-source evidence-explanation move. C1 places synthesis at U5, after the U1-U3 spine. Correct dependency.
- **Timed last** is supported by guidance-fading + automaticity: the map withholds the clock until U7.4 and makes it the U8 variable (`C1` lines 215, 166-177). This matches the brainlift through-line *"Manage time … Enters late, once the moves are automatic"* (`MVP.md` line 189) and CLT (a timed task adds extraneous load that a non-automatic spine cannot absorb — `LearningSci` lines 13-15).

**Attempt to break it — backwards dependency search.** I looked for a skill a lesson needs that is taught *later*. The closest real find: **U7 (multi-perspective, constructed support, no source passage) sits AFTER U5 synthesis, but its support is *constructed from knowledge*, not source-bound** (`C1` line 158). That is a genre *discontinuity*, not a backward dependency — U7 reuses the reasoning/line-of-reasoning spine built in U1-U6, it just drops the passage. It does not require a skill taught after it. **No fatal backward dependency found.** One minor wrinkle: counterargument is introduced at U3 (3.3) but the *expository* gate (4.6) is the English I gate, so counterargument is taught then not gate-assessed at EI — that is intentional (argumentative is the "eligible-mode hedge," `C1` lines 67-69), not a dependency fault.

**Caveat (interleaving):** the order is *blocked by essay type* (all E1, then all E2, then all E3…). Dunlosky's interleaving finding warns blocking can underbuild the judgment of *which move to use when*: interleaving *"helps the learner to choose the correct strategy … leads to increased transfer"* (`LearningSci` line 59). This is not enough to downgrade the order — blocking-to-acquire then interleaving-to-transfer is defensible — but see Gap #2: the map never interleaves earlier essay types back in.

---

### 2. "Reasoning before thesis" (reason-not-restate at 1.1, controlling idea at 1.4): **CAVEAT**

This is the one decision where C1 **inherits the brainlift's overstatement**, exactly as the prior verdict file predicted. The earlier `Verify_ReasoningBeforeThesis.md` reached **SUPPORTED-WITH-CAVEAT** and its reasoning applies cleanly to C1.

C1's ordering is: 1.1 "Reason, not restate" (Draft frontier) → 1.2 read-for-idea → 1.3 cite+explain → 1.4 "Controlling idea … thesis-as-refinement" (`C1` lines 78-81). The map's audit row asserts *"Reasoning before thesis: 1.1 (reasoning) precedes 1.4 (controlling idea)"* (`C1` line 211).

**Does C1 also overstate it? Partially yes, partially no — and it is better than the brainlift.** The reconciliation the prior verdict demanded is *working-claim-early, refined-controlling-idea-late*:
> "a working claim is fine early; the **refined controlling idea** is taught after reasoning, and reasoning gets the instructional weight because it is the harder, higher-leverage move." (`Verify_ReasoningBeforeThesis.md` line 93)

C1 **gets the refined-thesis half right**: 1.4 is explicitly *"refine a response into a clear controlling idea … (thesis-as-refinement)"* (`C1` line 81). That is the source-backed move (RWT: *"arrived at the claim as a result of careful reading"*; UNC: *"A thesis is the result of a lengthy thinking process"* — `Verify_ReasoningBeforeThesis.md` lines 35, 89).

**But C1 still risks the literal "no claim to reason about" trap at 1.1.** Lesson 1.1 teaches *"write the sentence that explains how evidence supports a point"* (`C1` line 78) before any lesson hands the student a working claim — 1.2 (read-for-idea) and 1.3 (cite+explain) come *after*. The prior verdict's core objection bites here: *"you cannot judge 'does this evidence support the point?' with no point"* and *every* production curriculum we hold (TREE, CER, TWR's SPO) puts the claim/topic-sentence FIRST (`Verify_ReasoningBeforeThesis.md` lines 51-65, 93). The brainlift itself contradicts the ordering in three other places — its through-line table lists *"Form a controlling idea"* before *"Explain the evidence"* (`MVP.md` line 184), its engine lists Outline-controlling-idea before Draft-explain (`MVP.md` lines 236-237), and TREE is glossed *"topic sentence, reasons, explain reasons, ending"* — claim first (`MVP.md` line 250).

**Verdict: CAVEAT.** The *spine* (reasoning is the frontier move, gets the heaviest instruction, refined thesis comes late) is sound and well-evidenced (STAAR 3-vs-2 lever, `MVP.md` SPOV 4 line 147). The *literal 1.1-before-any-claim ordering* is unsupported by every external curriculum and contradicted by the brainlift's own structural tables. **Fix:** 1.1's discrimination/practice must supply a provisional claim + evidence so the reasoning move has a point to attach to (the gated restate-vs-reason sort at 1.1 can do this), and the map's audit line should be reworded to "reasoning is the unit frontier and is weighted first; a working claim is supplied; the refined controlling idea is sharpened at 1.4" rather than the bald "reasoning before thesis."

---

### 3. "One new move per lesson" + scaffold fade within each thread: **SUPPORTED**

Cognitive Load Theory backs the granularity directly and at the right grain.
> "Our working memory is very small: it can hold between four and seven pieces of new information at any one time. … Always offer small amounts of information, then help students practice it and only go to the next step if the previous one is mastered." (`LearningSci` line 15, Sweller via Rosenshine)
> "Isolate ONE sub-skill per lesson screen … gate progression (don't reveal the next move until the current one is demonstrated)." (`LearningSci` line 16, design implication)

Engelmann's DI corroborates the cap from the other side: *"Only 15% of content in each lesson is new. 85% is prior content through review, practice, application, and testing"* (`LearningSci` line 66). C1's consolidation/gate lessons (1.5, 2.4, 3.5, 4.6, 5.6, 6.4, 7.5, 8.3-8.5) introduce *no* new move by design (`C1` lines 206-207) — that is the 85%-review discipline encoded structurally.

**Attempt to break it — too slow / arbitrary?** Writing Next does *not* prescribe lesson granularity (it scores intervention *types*: strategy instruction d=0.82, SRSD d=1.14 — `MVP.md` line 258), so "one move per lesson" is not *directly* a Writing Next result. But it is a clean application of CLT + DI's faultlessness, and the map respects the *recursive* caveat (TWR Principle 2: *"not necessarily waiting for 'mastery' of one kind of strategy before moving on"* — `TWR_Mining.md` line 25) by having through-line skills grow across lessons while one *new* move is added. **Not too slow:** Rosenshine's own qualifier is that step size adapts — *"when teaching older, brighter students … the steps are larger"* (`LearningSci` line 72). C1 is fixed-step, which is mildly conservative for an on-grade G9-10 writer, but the fade (Heavy→None) is the adaptation lever, so the risk is low. **Verdict: SUPPORTED.** The one-move cap is correct; the granularity is principled, not arbitrary.

---

### 4. Paragraph architecture early (U1, U4) → essay architecture later: **SUPPORTED**

This is one of the best-grounded decisions in the map, triangulated across all three production sources.
- TWR: the Single-Paragraph Outline is Chapter 6; the Multiple-Paragraph Outline is a *later* chapter (`TWR_Mining.md` lines 96-120; `Verify_Structure.md` line 50). TWR's prerequisite gate: *"Students should also have learned how to outline a paragraph or an essay before being asked to write one independently"* (`TWR_Mining.md` line 25).
- The brainlift's engine: *"Early reps use the paragraph-writing architecture; the core uses the essay-writing architecture"* (`MVP.md` line 231).
- SRSD: paragraph-grain mnemonic (TREE) precedes essay-grain (STOP+DARE) — *"TREE (used … mostly for opinion paragraphs); … STOP+DARE … built for full persuasive/argumentative essays"* (`SRSD_Mining.md` lines 219-220).

C1 uses `Arch: Para` for 1.1-1.4, 4.1-4.4, then `Essay` from 1.5 / 2.1 onward (`C1` lines 78-110). Correct grain progression.

**Attempt to break it — is the jump too abrupt?** The prior `Verify_Structure.md` flagged the real risk: *"Essay STRUCTURE / paragraph TRANSITIONS are owned by no Unit-1 lesson"* (its G1 gap, `Verify_Structure.md` line 65). C1 *solves* this — 2.1 "Structure the response" owns the intro/body/conclusion move (`C1` line 88) *before* any cold full-essay demand. So the connective tissue has an owner. **Verdict: SUPPORTED**, provided 2.1 ships before any multi-paragraph product is gated (it does: gate is 4.6).

---

### 5. Comprehension pre-read scored SEPARATELY from writing on every passage-based rep: **SUPPORTED**

Strongly grounded, and the separation (not just the pre-read) is the load-bearing part.
- Graham *Writing to Read* / reciprocity: writing about content improves comprehension at ~d=0.40 (`MVP.md` line 264), and the brainlift makes scoring separation explicit: *"a misread is not a writing failure … Every passage-based rep therefore opens with a comprehension pre-read scored apart from the writing, and a misread routes to re-read support rather than to writing remediation"* (`MVP.md` SPOV 5, line 151).
- CLT/diagnosis: Engelmann's stimulus-locus rule says diagnose the *communication/input* before blaming the producer — separating comprehension is exactly this (don't mis-attribute a reading failure to writing). And the Hot-Text precedent proves separate comprehension scoring is auto-checkable at scale (`curriculum_resource_base.md` line 23, STAAR Hot Text).

**Attempt to break it — overhead?** The adversarial case: scoring comprehension on *every* rep is friction that could be sampled instead. But the cost is low (a pre-read MCQ/highlight, `C1` lines 79, 140) and the diagnostic payoff is high precisely *because there is no teacher* to notice "this is a reading problem, not a writing problem." For a no-teacher app this is not overhead — it is the only mechanism that routes a misread correctly. **Verdict: SUPPORTED.** The one refinement: the map should confirm the pre-read is *cumulative-light* (a quick check), not a second full task, or it does become load.

---

### 6. Cold single-attempt gates on reserved passages; rescore-weakest-part only on practice: **SUPPORTED**

The testing/transfer literature backs *testing on new* and cold transfer.
- Engelmann's testing principle: *"The test segment should repeat some examples … The segment should also contain new examples"* and the test must use *"examples that bear no predictable relationship to each other"* (`Engelmann_DI_Mining.md` lines 69-72). Reserved gate passages held out of instruction = testing on genuinely new items.
- Brainlift: *"Every gate is single-attempt, on reserved passages held out of instruction, so a pass is genuine cold transfer rather than local patching. The rescore-the-weakest-part loop runs on practice reps only, never on a gate"* (`MVP.md` line 225; `C1` line 189). The split — patching-loop on practice, none on the gate — is the testing effect applied correctly (retrieval/transfer is the gate's job; corrective feedback is practice's job).

**Attempt to break it — false-fail risk?** This is the sharpest adversarial target, and it has teeth. A *single* cold attempt has high variance: a student who has the skill can fail one gate passage on an off day or a single misread, and the research the map relies on (Bloom, Hattie) is emphatic that *formative* assessment should be decoupled from judgment — *"formative evaluation tests should be regarded as part of the learning process, and should in no way be confused with the judgement of the student's capabilities"* (`LearningSci` line 92). A one-shot gate is *summative*, which is fine, but single-attempt summative judgment risks the very false-fail that demotivates the teen the Yeager evidence warns about (a low score is a *status threat*, `LearningSci` line 104). **Mitigants already in the map that defuse this:** (a) the comprehension pre-read is scored separately, so a misread does *not* fail the writing gate — it routes to re-read (`C1` line 210), removing the single largest false-fail cause; (b) pre-gate self-score lessons (4.5, 7.4, 8.3-8.4) rehearse the cold form first; (c) calibration is surfaced, not gating (`C1` line 192). **Residual risk:** the map does not state a *re-gate* policy (can a student who fails 4.6 retry on a *different* reserved passage?). Single-attempt-per-passage is right; single-attempt-*ever* would be a false-fail hazard. **Verdict: SUPPORTED, with one required clarification** — specify that a failed gate re-routes to targeted practice then a *fresh* reserved passage, so "cold transfer" is preserved without one bad day ending the course. The architecture's logic supports this; the map just needs to say it.

---

### 7. "Discrimination before production" (gated sorts before each production move): **SUPPORTED**

The single best-evidenced decision in the architecture. Three independent sources converge:
- Wood/Bruner/Ross: *"Comprehension of the solution must precede production. … the learner must be able to recognise a solution to a particular class of problems before he is himself able to produce the steps"* (`LearningSci` line 49).
- Engelmann: *"the component discriminations involved in a cognitive routine should be pretaught before the routine is introduced"* (`Engelmann_DI_Mining.md` line 162).
- Brainlift SPOV 7: *"Discrimination is the gateway to production. You cannot write what you cannot recognize"* (`MVP.md` line 157).
- Real-curriculum proof of existence: Excelsior's auto-graded strong-vs-weak MCQ with teaching feedback, ATC annotate-then-compare, Quill (`curriculum_resource_base.md` LT2, lines 46-50, 64).

C1 puts a gated sort before every production move: restate-vs-reason (1.1), summary-vs-explanation (2.2), build-vs-list (3.2), strawman-vs-fair (3.3), serial-vs-synthesis (5.2), binary-vs-nuanced (6.1), engage-vs-restate (7.2) (`C1` lines 78, 89, 98, 99, 141, 151, 164). Faithful to the principle throughout.

**Attempt to break it — does the map honor Engelmann's *full* discrimination spec?** The `Engelmann_DI_Mining.md` audit found our DI blocks under-serve the **sameness** principle (we show difference pairs but not *multiple maximally-different positives under one label*, risking the stipulation misrule "argues = has a number" — `Engelmann_DI_Mining.md` lines 166, 218). The C1 *map* only names the sorts; whether each generated sort includes the sameness demo is a C3-authoring concern, not a map-architecture flaw. **Verdict: SUPPORTED** at the architecture level; flag the sameness-demo requirement forward to C3 (already logged in the DI mining doc).

---

### 8. Frontier concentration (the ★ stage carries the heaviest instruction each unit): **SUPPORTED**

This is "concentrate the worked-example / Teach-Model fire on the unit's hard move," and it is sound.
- Worked-example + guidance-fading: *"Start with worked-out examples … Then move to completion assignments … Subsequently remove – one by one – the presented steps"* (`LearningSci` line 21) — and the heaviest guidance belongs on the hardest, least-automatic element. C1 marks one ★ frontier stage per unit (Draft for EI, Outline for EII — `C1` lines 64, 121) and routes the Teach/coping-model there.
- Brainlift: *"The AI-Tutor direct-instruction sequence … concentrated on each unit's frontier stage"* (`MVP.md` line 244).
- This also enacts CLT: spend novel-element budget on the one element with the highest intrinsic load, strip the rest to review.

**Attempt to break it.** No source contradicts concentrating instruction on the hard move; the only risk is *mis-identifying* the frontier. The map's choices are defensible: EI frontier = Draft/explain-evidence (the STAAR 3-vs-2 lever, `MVP.md` SPOV 4); EII frontier = Outline/synthesis-matrix (synthesis is *"the frontier move of English II,"* `MVP.md` line 155). Both match the brainlift's own frontier calls. **Verdict: SUPPORTED.**

---

### Bonus target — Per-thread scaffold fade RE-SET at each new essay type: **CAVEAT**

The brief asks specifically: is re-scaffolding Heavy→None at *each* new essay type supported by expertise-reversal, or does it waste reps?

C1 resets the fade per thread: U1 fades Heavy(1.1)→Light(1.5); U2 restarts Medium→Light; U3 restarts Heavy(3.1)→Light(3.5); U5 restarts Heavy(5.1)→Light(5.6); U7 restarts Heavy(7.1)→None(7.5) (`C1` lines 78-177, 208).

**The case FOR re-setting (expertise-reversal):** Kalyuga's expertise-reversal effect is *relative to the specific task* — *"A teaching approach that works well with an expert will most probably not work well with a beginner"* (`LearningSci` line 27). A student fluent at *expository* explain-evidence is a *relative novice* at *synthesis* (weaving multiple sources), so re-providing Heavy scaffold at U5 is correct: they are not an expert at *that* move. The brainlift's *"Scaffold fade, from Heavy to Medium to Light to None across each unit"* (`MVP.md` line 247) endorses per-unit fade explicitly.

**The case AGAINST (wasted reps):** the *through-line* skills (read-for-idea, explain-evidence, structure) are NOT reset — they grow across the whole course (`MVP.md` line 180). So the question is only whether the *shared spine* gets needless Heavy scaffold at each new essay type. Here the map is actually careful: U2 restarts at *Medium* not Heavy (2.1, `C1` line 88), U3 restarts Heavy only on the *new* move (defensible position, 3.1) — and the genuinely-shared moves (cite+explain) are *not* re-taught Heavy, they appear as `Heavy *(on move)*` only where the move is new to that genre (2.2 explain-to-standard, 5.4 weave-sources — `C1` lines 89, 143). So the re-set is **scoped to the new move, not the whole spine.**

**Verdict: CAVEAT (leaning supported).** Per-essay-type re-scaffolding is defensible under expertise-reversal *because each new essay type contains a genuinely new frontier move*. The waste risk is real only if a *through-line* skill gets re-taught Heavy — and the map mostly avoids this by restarting at Medium and tagging Heavy `*(on move)*`. **The one place to watch:** confirm in C3 that the shared explain-evidence spine is NOT re-modeled from scratch at U3/U5/U7 (the student should carry it forward); if it is, that is the expertise-reversal *harm* (re-showing a frame to someone who has internalized it — `LearningSci` line 28). As architected, the decision is sound; the implementation must not over-scaffold the carried spine.

---

## What learning science says is MISSING from the architecture (ranked)

### MISSING #1 (highest) — "Memorize It" to automaticity, and a carried mnemonic. The single biggest omission for a TIMED, no-reference exam target.

The architecture's endpoint is a *cold, timed, no-reference* essay (U8 gate). SRSD's Stage 4 "Memorize It" is *the* mechanism that makes timed no-reference performance possible, and the C1 map has **no analog** — it fades the *visible* scaffold (checklist) but never installs the *internal* one.
> "Stage four: Memorize it. … students memorize the steps of the strategy, relevant mnemonic devices … 'You can't use it if you can't remember it!'" (`SRSD_Mining.md` lines 109-110)
> "the instructor … emphasized that students needed to be able to remember the strategy because they cannot bring physical reminders of HIT SONGS3 with them when taking the ACT test." (`SRSD_Mining.md` line 113)

And the documented **failure case** is exactly what a fade-without-memorization produces: students who *"merely wrote the mnemonic at the top of their paper, using it as a prompt"* because it was never internalized (`SRSD_Mining.md` line 201). The brainlift names STOP+DARE / TREE / HIT BOOKS³ as the load-bearing mnemonics (`MVP.md` line 250) — **but the C1 map never names a mnemonic, never schedules memorization, and sets no recall criterion.** It fades the checklist (Light→None) without ever confirming the strategy moved into the student's head. This is the gap most likely to cause a *false-fail at the timed gate*: a student who relied on the visible checklist through U1-U7 hits U8 with nothing to retrieve. **Fix:** add an explicit Memorize-It beat (name one carried strategy, low-stakes retrieval openers, criterion = "articulate each step AND its purpose from memory," `SRSD_Mining.md` line 229) reaching criterion *before* timing enters at U7.4.

### MISSING #2 — Cross-unit retrieval practice, spacing, and interleaving.

The map has *no* retrieval/spacing structure across units. The within-lesson reps are present, but Dunlosky's two highest-utility techniques are *practice testing* and *distributed practice* (`LearningSci` line 33), and interleaving *"leads to increased transfer"* (`LearningSci` line 59). The architecture blocks each essay type (all E1, then all E2…) and **never re-tests an earlier essay type until the U8 gate.** The brainlift's own engine note (Dunlosky design implication) calls for *"low-stakes recall into the app … open each session with a quick quiz on the prior session's move … make retrieval cumulative"* (`LearningSci` line 34). The map's audit even claims the engine handles retrieval, but the *lesson map itself* schedules no cumulative retrieval and no interleaved re-rep of E1 while teaching E3. **Fix:** add cumulative retrieval openers and interleave a prior-essay-type rep into later units (e.g. a single expository rep inside U5) so transfer is built before the gate, not tested cold for the first time.

### MISSING #3 — Transcription/handwriting/typing fluency and explicit timing-strategy practice depth.

The brief asks specifically about transcription fluency. The architecture targets a *timed typed essay* but treats fluency only as "Manage time … enters late" (`MVP.md` line 189) and gives U8 just two timing lessons (8.1 timing strategy, 8.2 self-diagnosis). Transcription fluency (the automaticity of getting words down) is a known constraint on composing quality under time (the McCutchen working-memory line the brainlift cites — knowledge/automaticity free capacity, `MVP.md` line 113), and sentence-combining (d=0.50, `MVP.md` line 258) is the fluency lever. C1 *has* sentence-combining (4.2) but as a one-off SCR skill, not as a fluency thread that builds toward timed throughput. **Fix:** thread sentence-level fluency (combining, dictation-style speed reps) lightly across units so transcription is not a hidden bottleneck at the timed gate. Lower priority than #1-#2 because the population is on-grade G9-10 (not the dysgraphic/LD population where transcription dominates), but still a real omission for a timed target.

### MISSING #4 (present but under-specified) — Yeager motivational tone / wise-feedback at the gate.

The map is a skeleton and correctly defers feedback *copy* to C3/C5, so this is not strictly a map gap. But the architecture's *cold single-attempt gate* is precisely the *"adolescent predicament"* status-threat moment (`LearningSci` line 104), and the map should at minimum flag that the gate-fail experience needs the transparency/wise-feedback + re-route mechanism (Gap #1 in decision 6). Noting it here because the *architecture* (single-attempt cold gate) creates the motivational risk even though the *copy* lives downstream.

### NOT missing (checked and present): self-regulation/goal-setting and self-assessment calibration.

These ARE in the architecture — self-assessment progresses binary→3-point→AP→self-diagnosis (the calibration through-line, `MVP.md` line 187; C1 4.5, 7.4-7.5, 8.2), and goal-setting is implicit in the rescore-weakest-part loop. So the self-regulation half of SRSD is represented even though the *memorization* half (Gap #1) is not. Worth stating to avoid over-claiming the gaps.

---

## Strongest case that the architecture is WRONG (steelman the critique)

A determined skeptic would build the attack like this:

**"This is an internally-coherent design dressed as a research-derived one, and its single most distinctive choice is contradicted by the very sources it cites."**

1. **The distinctive ordering claim ('reasoning before thesis') is an internal assertion, not a research finding.** The prior verdict file already established that the *only* warrant for it is one sentence in the brainlift, that the brainlift contradicts itself three times, and that *every* external production curriculum (TREE, CER, TWR's SPO) teaches the claim FIRST (`Verify_ReasoningBeforeThesis.md` lines 15, 51-65). C1 propagates this contradiction into 1.1-before-1.4. So the architecture's marquee differentiator rests on the weakest evidence in the file.

2. **The architecture optimizes for cold transfer but omits the mechanism that makes cold transfer possible.** It targets a timed no-reference gate and *removes* the visible scaffold to force transfer — but never installs the *internal* scaffold (memorization to automaticity) that the SRSD literature says is the precondition for no-reference performance (`SRSD_Mining.md` lines 110, 113, 201). A skeptic says: this is fade-without-internalization, and the literature's own documented failure case is students with nothing to retrieve at the test. The cold gate could therefore be *systematically* false-failing students who learned the moves but were never helped to memorize them.

3. **Blocking + no cross-unit retrieval means the gate is the first interleaved/spaced test the student ever sees.** Dunlosky says spacing and interleaving are *high-utility for transfer* (`LearningSci` lines 33, 59); the architecture blocks every essay type and never re-tests E1/E2 until U8. So the U8 synthesis-AND-ACT gate is simultaneously the first cumulative, first interleaved, first timed, AND first cold experience — four novel load sources at once, which is the opposite of CLT's "add one element at a time." A student could pass every unit and fail the gate purely from the *combination* being novel.

4. **It is mostly verified against itself.** Of the eight decisions, the strongest external grounding clusters on the *generic* moves (CLT, comprehension-precedes-production, discrimination, worked examples, testing-on-new) that *any* good sequence would have. The *specific* architectural bets — reasoning-before-thesis, the exact 8-unit order, per-thread fade reset, the expository-primary weighting — lean on the internal brainlift and the STAAR form analysis, not on writing-science meta-analysis. Writing Next scores intervention *types*, not *sequences*; it cannot validate this sequence.

**Why the steelman does not sink the architecture (the honest rebuttal):** Points 1, 2, 3 are *fixable gaps*, not structural errors — none requires re-ordering the 8 units, only adding memorization (Gap #1), cross-unit retrieval/interleaving (Gap #2), and a re-gate policy (decision 6). Point 4 is true but unavoidable: no meta-analysis validates *any* specific lesson sequence; the right standard is "is each decision consistent with the principles?" and they are. The steelman proves the architecture is *incomplete*, which is why the verdict is SOUND-WITH-GAPS rather than SOUND — but it does not prove any decision is *wrong*.

---

## Net recommendation: **KEEP the architecture; MODIFY in five specific ways.**

The 8-unit spine, the one-move cap, paragraph-before-essay, separate comprehension scoring, discrimination-before-production, cold gates, and frontier concentration are all sound and should ship as architected. Make these five changes before C3 authoring:

1. **Add a "Memorize It" beat and name one carried strategy (HIGHEST PRIORITY).** Pick one mnemonic per genre (the brainlift's STOP+DARE / TREE — `MVP.md` line 250), introduce it where its structure first appears, schedule low-stakes retrieval, and set the criterion (*"articulate each step AND its purpose from memory,"* `SRSD_Mining.md` line 229) to be met *before* timing enters at U7.4. Without this the cold timed gate risks false-failing students who learned the moves. (Closes Gap #1.)

2. **Add cross-unit cumulative retrieval and interleave a prior essay type into later units.** A quick prior-move recall opener on every lesson, and at least one E1/E2 rep folded into U5/U7, so the U8 gate is not the first spaced/interleaved/cumulative experience. (Closes Gap #2; supported by Dunlosky `LearningSci` lines 33, 59.)

3. **State a re-gate policy for the cold gates.** Single-attempt *per reserved passage* is correct; specify that a fail re-routes to targeted practice then a *fresh* reserved passage, so one off-day or one misread does not end the course. The separate comprehension score already removes the largest false-fail cause — make the re-gate explicit too. (Closes the decision-6 residual risk; Bloom/Yeager `LearningSci` lines 92, 104.)

4. **Reword the "reasoning before thesis" rationale, and supply a working claim at 1.1.** Keep the sequence (reasoning is the weighted frontier; refined controlling idea at 1.4) but reword the audit line to the working-claim/refined-thesis framing the prior verdict established, and ensure 1.1's gated sort/practice provides a provisional claim+evidence so the reasoning move has a point to attach to. (Closes the decision-2 caveat; `Verify_ReasoningBeforeThesis.md` lines 93, 105.)

5. **Thread sentence-level fluency lightly across units (lower priority).** Promote sentence-combining from a one-off SCR (4.2) to a light recurring fluency beat, so transcription throughput is not a hidden bottleneck at the timed gate. (Closes Gap #3; sentence-combining d=0.50, `MVP.md` line 258.)

And forward to C3 (already logged, not new): each generated discrimination sort must include Engelmann's **sameness demo** (2-3 maximally-different positives under one label), not just a difference pair, to avoid the stipulation misrule (`Engelmann_DI_Mining.md` lines 166, 218).
