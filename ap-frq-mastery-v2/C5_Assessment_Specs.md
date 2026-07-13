# C5 — Assessment Specifications (handoff to dev grader + tests)

The rubric definitions, score-band discriminators, feedback targets, and
anchor-paper exemplar seeds the **dev team's AI grader (D2)** and **STAAR-aligned
tests (D3)** are built from. The curriculum team specifies WHAT to assess; the dev
team owns HOW (model, pipeline). This is also the source of truth C3 authors
discrimination items + Revise checklists against (write-to-the-gate discipline).

**Status:** v1. Rubric language **verified verbatim** against official TEA rubric
PDFs (`tx-staar-informational-rubric-g6-e2.pdf`,
`tx-staar-arg-opinion-rubric-g6-e2.pdf`, Fall 2022) and TEA's "Scoring Process for
STAAR Constructed Responses." ACT rubric verified verbatim against the official ACT
Writing rubric. Anchor-paper discriminators from TEA scoring guides (EI 2023/24/25,
EII 2024). Local PDF copies saved under the session `tool-results/` dir if a future
pass needs full-paragraph SCR verbatim.

## The four specs at a glance

| Spec | Rubric | Scale | Scores which tasks | Source |
|------|--------|-------|--------------------|--------|
| **S-INF** | STAAR Informational ECR (2-trait) | Org & Dev 0–3 + Conventions 0–2 | E1 expository + E3 synthesis (10.B / 5.B — **primary** STAAR mode) | TEA Informational rubric |
| **S-ARG** | STAAR Argumentative/Opinion ECR (2-trait) | Dev & Org 0–3 + Conventions 0–2 | E2 argumentative (10.C — eligible/secondary) | TEA Argumentative rubric |
| **S-SCR** | STAAR SCR pair | reading 0–2 · writing 0–1 | reading SCR + sentence-combining SCR | TEA scoring process + guides |
| **S-ACT** | ACT Writing (4-domain) | each 1–6 per rater (2–12 reported) | E4 multi-perspective (ACT readiness) | ACT official rubric |

> **Weighting (from 6 released forms):** S-INF is the **primary** STAAR ECR scorer
> (every released EI/EII ECR is informational 10.B or analytical-response 5.B).
> S-ARG is eligible-but-unseen on released forms — built for the EI argumentative
> reps + the eligible-mode hedge. The grader must support **both** and select by
> task mode.

---

## S-INF — STAAR Informational ECR (verbatim + discriminators)

**Trait 1 — Organization & Development of Ideas (0–3).** Four sub-elements scored
holistically: controlling idea/thesis · organization · evidence · expression.

| Score | Controlling idea/thesis | Organization | Evidence | Expression |
|------:|-------------------------|--------------|----------|------------|
| **3** | clear and **fully developed**; focus consistent → unified | **effective**; purposeful structure w/ **effective** intro + conclusion; ideas logically connected in purposeful, highly effective ways | specific, well chosen, relevant; **clearly explained**; consistently supports/develops; *(pairs)* drawn from **both texts**; thorough understanding | clear and effective; word choice specific/purposeful; almost all sentences effectively crafted |
| **2** | present and **partially developed**; may not be clearly identifiable; focus may waver | **limited**; intro + conclusion **present**; structure may not be consistent; sentence-to-sentence connections may be lacking | limited, some irrelevant; **insufficiently explained**; *(pairs)* from **at least one** text; partial understanding | basic; word choice general/imprecise; sentences at times ineffective |
| **1** | **evident but not developed** | minimal/weak; intro **or** conclusion may be present; logical structure not always evident | insufficient/mostly irrelevant; explanation insufficient/vague; *(pairs)* from **only one** text; limited understanding | ineffective; word choice vague/limited |
| **0** | may be evident | **lacks BOTH intro and conclusion; no structure** | **not provided or irrelevant**; lack of understanding | unclear/incoherent |

**Trait 2 — Conventions (0–2):** 2 = **consistent command** (sentence construction,
punctuation, capitalization, grammar, spelling); "few errors, but those errors do
not impact clarity." 1 = **inconsistent command**; "several errors, but the reader
can understand." 0 = **little to no command**; "many errors, and these errors impact
clarity and understanding."

**HARD-COUPLING RULE (must encode):** *if Trait 1 = 0, Trait 2 is also forced to 0.*

**The discriminators (the levers C3 builds items against, dev grader scores on):**
- **Evidence EXPLANATION is the dominant 3→2→1 lever.** The hinge word is
  *explained*: 3 = "clearly explained" · 2 = "insufficiently explained" · 1 =
  explanation "insufficient/vaguely related." → *The single highest-leverage thing
  the course teaches and the grader must detect: does commentary explain HOW the
  evidence supports the idea, or just drop the quote?*
- **Thesis development, not presence.** A thesis is present at all of 1/2/3; what
  moves it up is *developed* (1 evident → 2 partial → 3 full) and *consistent focus*.
- **Pairs: number of texts is a discrete, checkable discriminator.** 3 = both texts ·
  2 = at least one · 1 = only one. (Drives the E3 synthesis "evidence from all
  sources" gate.)
- **Organization 3→2 line = "effective" intro/conclusion vs merely "present."**
- **The 1→0 floor is structural: missing BOTH intro and conclusion / no structure.**

## S-ARG — STAAR Argumentative/Opinion ECR (differences from S-INF only)

Structurally identical 2-trait rubric (same organization/evidence/expression
ladders, same pairs rule, same 0-floor, same Conventions trait verbatim, same
hard-coupling). **Two differences a grader/spec must encode:**

1. **Position language swap:** Trait 1 keys on **"argument/opinion"** (clearly
   identifiable → present/partially developed → evident but not developed) in place
   of "controlling idea/thesis." (Title is "Development and Organization of Ideas.")
2. **Counterargument is the load-bearing extra discriminator** (grades 8–EII only):
   - **3** = counterarguments **identified AND refuted**
   - **2** = counterarguments **identified but NOT refuted**
   - **1** = counterarguments **NOT identified**
   → *For an EI/EII argumentative essay, refuting the counterargument is what
   separates a 3 from a 2; failing to identify one pushes toward 1.* (This is why
   C1 lesson 3.3 teaches acknowledge/concede/**respond** as a scored move.)

## S-SCR — Short Constructed Response specs

**Reading SCR (0–2)** — item-specific (correct answer named per item):
- **2** = complete/correct answer **+** ≥1 accurate, relevant text-based evidence
  (quoted or paraphrased), accurately used to support.
- **1 (partial)** = accurate answer **without** sufficient evidence, **OR** relevant
  evidence **without** an accurate answer.
- **0** = incorrect / not based on the text / no response.
- *Discriminator:* the point is **claim + cited evidence together** — either alone
  caps at 1. (C1 lesson 4.3.)

**Writing SCR (0–1)** — sentence-combining/revision, generic rubric:
- **1** = "a **complete sentence** that combines [or expresses] the ideas in a
  **clear and effective** way."
- **0** = "not a complete sentence, **or** does not express the ideas clearly and
  effectively."
- *Two failure axes the 0 encodes:* (1) **not a complete sentence** (fragment /
  run-on / comma splice) · (2) **doesn't combine/express clearly** (meaning lost,
  awkward, redundant). Minor spelling/punctuation slips do NOT cost the point if the
  combine is effective. (C1 lesson 4.2.)

## S-ACT — ACT Writing (4-domain, verbatim discriminators)

Four domains, each scored **1–6 per rater × 2 raters → 2–12 per domain**; reported
Writing score = rounded average of the four domains. Top-vs-middle gap across **all
four** domains is **analysis/integration**, not grammar (grammar only gates the
bottom).

| Domain | Top (5–6) | Middle (3–4) | Low (1–2) |
|--------|-----------|--------------|-----------|
| **Ideas & Analysis** | critically/productively **engages multiple perspectives**; thesis "reflects nuance and precision"; **insightful context**; examines implications/tensions/assumptions | "engages"/"responds to" perspectives; thesis "clarity"/"some clarity"; context "relevant"/"limited"; analysis "recognizes"/"simplistic" | "weakly responds"; thesis little clarity; analysis ≈ **restatement** of the issue/perspectives |
| **Development & Support** | **integrated line of reasoning** conveys **significance**; qualifications/complications **enrich** | reasoning "adequately conveys significance"; qualifications "extend" | support "general/simplistic" → "weak, confused, circular" |
| **Organization** | **unifying controlling idea** + logical progression; transitions **strengthen** relationships | "clear"/"basic" structure; emergent controlling idea; transitions "sometimes clarify" | rudimentary/no structure; transitions "misleading" |
| **Language Use** | precise/varied; tone strategic; errors **don't impede** | adequate/clear; some variety; errors "rarely impede" | imprecise; little variety; errors **impede understanding** |

**The ACT discriminators C3 builds toward:** (1) **engage + evaluate multiple
perspectives** (not restate them) — the #1 top-vs-mid lever; (2) **qualify/complicate**
the thesis (enriching, not "some disagree" with no payoff); (3) convey **significance**
via an integrated line of reasoning; (4) a **unifying controlling idea** with
strengthening transitions. (Maps to C1 Unit 7.)

---

## Feedback targets (what the grader returns — same contract every essay)

Per the practice engine, every full rep returns:
- **Per-trait/domain score + plain-language reasoning** for each.
- **The single weakest trait/row, named** — the rescore loop targets exactly one.
- **One concrete, move-specific next step** tied to that weakest row — phrased as
  the discriminator, e.g. *"Your commentary drops the quote — add a sentence saying
  HOW it supports your controlling idea"* (S-INF evidence-explanation lever);
  *"You named the opposing view but didn't refute it — add the rebuttal"* (S-ARG
  counterargument lever).
- **Self-vs-grader delta** per trait (drives the surfaced, non-gating calibration).
- **Gateway pass/threshold JSON** on gate reps (drives lock-until-pass).

## Anchor-paper exemplar seeds (for grader eval sets + C3 discrimination items)

The concrete "what moves a score up/down" reasons from TEA scoring-guide
annotations — these become the grader's eval-set labels AND C3's gated
discrimination items (the negative exemplars students sort against). The **four
highest-value negative exemplars** (down-moves to train detection on):

1. **Drops quotes/evidence without explanation** — annotation: *"Instead of
   explaining the evidence…"* → the S-INF evidence 3→1 lever; the C1 1.1 / 2.2
   restate-vs-reason and summary-vs-explanation sorts.
2. **Missing or token conclusion** — *"lacks a conclusion"* / *"a weak introduction
   consisting of only the thesis"* → the organization 1→0 structural floor.
3. **Text references in place of transitions** — *"lacks transitions"* / *"references
   to the text are used in place of transitions"* → organization/connection lever.
4. **Irrelevant/extraneous evidence padding** — *"additional but irrelevant textual
   evidence."*

Plus for **S-ARG**: **counterargument identified but not refuted** (caps at 2) and
**not identified** (toward 1). For **S-ACT**: **restating perspectives instead of
analyzing** (caps Ideas & Analysis at low/mid).

Positive exemplar seeds (up-moves): "clear thesis established in the first
paragraph"; "specific, relevant, and thoroughly explained" evidence; "a meaningful
conclusion that circles back to the introduction"; "transitions used throughout,
supporting the development of the thesis."

## Grader build requirements (handoff to D2)

- **Two ECR scorers** (S-INF primary, S-ARG) selectable by task mode; **S-SCR**
  per-part scorers (reading 0–2, writing 0–1); **S-ACT** 4-domain. NOT one generic
  essay scorer.
- **Encode the hard-coupling rule** (Trait 1 = 0 → Trait 2 = 0) for both ECR scorers.
- **Encode the discrete checkable discriminators:** pairs evidence = both/one/only-one
  text; S-ARG counterargument identified/refuted state; S-SCR claim-AND-evidence.
- **HARD LAUNCH GATE (blocking):** calibrate each scorer against **official AP/STAAR
  anchor papers** on the subtle rows — S-INF/S-ARG **evidence-explanation (3-vs-2)**,
  S-ARG **counterargument-refuted**, S-ACT **Ideas & Analysis (engage-vs-restate)** —
  to within 1 point on ≥80% of a held-out set **before any gateway-locked lesson
  ships**. Until then, cap the rescore multiplier on those rows / route through the
  human-authored discrimination key.
- **Known limit:** the grader scores written reasoning, not reading comprehension —
  a misread looks like a weak response. The C1 comprehension pre-read (scored
  separately) carries that load; the grader only sees output.
- **Rubric drift:** store each rubric as patchable config keyed to a TEA-rubric
  build-date (Fall 2022 verified here).

## Open items

- **Full-paragraph SCR-reading verbatim:** the reading-SCR 0–2 long descriptor was
  partly reconstructed from prose (proxy quote cap). Re-extract from the saved local
  PDFs with pdftotext/PyMuPDF if the dev team needs exact full-sentence wording.
- **Anchor papers themselves:** TEA scoring-guide sample essays are image-based
  (handwritten) and didn't text-extract — the **discriminator annotations** are
  captured (above), but if the grader eval set needs the actual scored essay TEXT,
  someone must transcribe a sample set from the rendered PDFs (or commission
  equivalents). Flag for D2.
- **EII gate split (from C1):** confirm whether the EII gate's S-INF (synthesis) +
  S-ACT halves are scored as one gate or two.

## Handoff

- **C3:** author every Revise checklist + discrimination item to these rows and the
  four negative exemplars; phrase grader next-steps as the named levers.
- **C4:** reserved gate passages pair with anchor exemplars at each score point.
- **D2 (grader):** build the four scorers to the requirements above; hit the
  calibration launch gate.
- **D3 (tests):** the gates score on S-INF (primary) / S-ARG / S-SCR (EI) and S-INF
  + S-ACT (EII).
