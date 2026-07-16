# Platform3 Gap: AI rubric / essay scoring for writing constructed-response

**Filed:** 2026-07-08 · **Surface:** Content / Results (scoring) · **Status:** OPEN, external scorer built as interim
**Decision (Noel):** File it as a Platform3 gap AND build it externally now, so generated writing courses function.

## The gap in one sentence
Platform3 declares scoring as surface-owned ("fix gaps on the platform, not in your app"; Content clients
must not implement scoring; `scoring_plan` is provenance-only; Results owns settled outcomes), but there is
**no platform-owned capability that scores a free-text writing essay against a rubric.** Selected-response
items score on the surface via `match_correct`; a constructed-response WRITING essay needs an AI/rubric
scorer, and today that logic has nowhere platform-owned to live.

## Why this is a platform concern, not an app concern
Per the global skill pack Non-Negotiables: "Do not decide a business semantic in app code. The data
dictionary or lower platform layer declares semantics; implementation mechanically serves them." A rubric
(which traits, what scale, which gate rule) is exactly such a business semantic. Every consumer app that
renders a writing course would otherwise re-implement the same scoring, drift apart, and violate the
single-source rule. Rubric scoring belongs beside `scoring_plan` and Results.

## What the platform should expose (proposed contract)
A surface-owned scorer keyed by a **rubric config id** on the item's `scoring_plan`, callable in the same
external-grader seam QTI already uses (submit response -> score + feedback -> Results settled outcome).

The portable contract is a **config-driven 4-trait engine**: the canonical traits are fixed
(Thesis/Purpose, Evidence/Development, Organization/Coherence, Conventions/Language); the trait COUNT,
SCALE, WEIGHTING, and GATE are per-form config. Validated against real released tests
(`TestDesign_Reference.md`). The five configs G9-12 needs:

| config id | models | traits x scale | total | special rule |
|---|---|---|---|---|
| `rc.staar` | STAAR English II | Org&Dev 0-3 + Conventions 0-2, x2 scorers | 10 | **GATE: 0 Org&Dev -> Conventions forced to 0** |
| `rc.mcas` | MCAS Grade 10 | Idea Development 0-5 + Conventions 0-3 | 8 | - |
| `rc.ohio` | Ohio ELA II | Purpose/Focus/Org 0-4 + Evidence/Elab 0-4 + Conventions 0-2 | 10 | - |
| `rc.4trait` | generic G10 analytic | 4 traits 0-4 | 16 | own-target default |
| `rc.ap` | AP Lang/Lit | Thesis 0-1 + Evidence&Commentary 0-4 + Sophistication 0-1 | 6 | Sophistication = the significance ("so what") row |

Scoring should return, per submission: each trait score + reasoning, the applied gate, the total and
max, one calibrated feedback string, the weakest trait, one next step. That maps directly onto a Results
settled outcome plus a QTI feedback payload.

## Interim: the external scorer we built (so courses work now)
Until the platform absorbs this, our external grader implements the contract above and plugs into the
existing external-grader seam. This is deliberately the SAME table the platform can adopt; when the gap
closes, the table moves onto the surface unchanged and our grader becomes a thin client (or is retired).

- **Engine:** `api/rubric_scorer.py` (`RUBRIC_CONFIGS` table + `score_rubric_essay`), mirroring the AP
  scorer idiom. Pure logic (config integrity, scale totals, the STAAR gate, out-of-range clamping) is
  unit-verified; live end-to-end verified on a strong essay (8/10) and a weak essay (0/10, gate fired).
- **Endpoints (`api/main.py`):** `POST /grade/rubric` (config-driven, 3-run consensus by default),
  `GET /rubric-configs` (introspection), and CR routing inside `POST /timeback/score` so G10 CR items
  (`ACC-W910-CR-*`) score live: family -> mode+config by default, overridable per-item via
  `TIMEBACK_CR_REGISTRY` at push time.
- **Deployment:** `hs-writing-grading.onrender.com`. Model id fixed to `claude-sonnet-4-5`
  (old `claude-sonnet-4-20250514` returned 404). **Still needs redeploy** for the new endpoints to go live.

## Ask for the platform team (Andy)
1. Confirm rubric/essay scoring should be a **Platform3 surface capability** (Content `scoring_plan` +
   Results), not permanently an external app grader.
2. If yes, adopt the `rc.*` config table as the initial rubric-config registry (it is standards-validated).
3. Define where the AI call runs (platform-hosted scorer vs. registered external grader the platform
   calls) and the exact settled-outcome shape a writing rubric score maps to in Results.
4. Until then, our external grader is the interim scorer; keep the config contract identical on both sides
   so migration is a lift-and-shift, not a rewrite.

---

# Platform3 Gap 2: per-SECTION (multi-field) AI rubric scoring of a structured writing artifact

**Filed:** 2026-07-16 · **Surface:** Content (QTI interactions) + Results (scoring) · **Status:** OPEN, no interim
**Decision (Noel):** log as a Platform3 surface gap. NOT built externally (it is a platform-capability gap, not an app gap); the pilot ships with whole-artifact scoring, which the platform DOES support.

## The gap in one sentence
Timeback can AI-rubric-score a writing artifact **only as one whole extended-text response**; there is
**no supported path to collect a STRUCTURED artifact as separate fields (e.g. the cells of an essay
outline: Thesis / Intro / each Body row / Conclusion) and get an AI rubric score PER FIELD.** You can have
per-cell inputs, or AI rubric scoring, but not both together.

## Concrete case that surfaced it
The Multiple-Paragraph Outline (MPO) essay-planning lessons (G9 L20 + 7 more G9-G12). Pedagogically the
outline is a 2-D grid (Thesis; Intro; Body rows pairing Main Idea + Details; Conclusion). Ideal would be
per-cell inputs AND a per-section score ("your thesis is strong, your body development is thin"). Today it
ships as a **display grid + one extended-text box scored holistically** (rc.staar, 5 pts) via the
ExternalApiScore seam - the only config that yields AI feedback. Per-section AI scoring is not expressible.

## Why neither existing mechanism closes it (verified against the timeback skill)
1. **Composite FRQ (multiple interactions in one item).** Supported for INPUT: an item may hold several
   interactions with distinct response ids (`RESPONSE_A`, `RESPONSE_B`, ...). BUT scoring collapses:
   ExternalApiScore fires once and returns ONE aggregate score - "Platform does NOT support per-part
   scoring natively; external grader returns a single aggregate score" (create-frq.md). So multiple boxes
   != multiple scores.
2. **PCI (Portable Custom Interaction).** Can render arbitrary per-cell UI, BUT PCI scoring is
   **string-match only**: "PCI-side scoring is the ONLY working pattern. Platform only supports
   `match_correct` string comparison" and `getResponse()` "MUST return a plain string" (create-pci.md
   gotchas #4, #6). A PCI self-evaluates to `correct`/`incorrect`; there is **no route from a PCI response
   to the ExternalApiScore rubric grader.** So a PCI outline could give binary/deterministic feedback
   (e.g. "all sections present"), never per-section AI trait scoring.

Net: per-cell inputs -> a multi-field AI rubric grader -> a score per section is **not achievable** on the
current platform. It needs either (a) per-part scoring on composite items (each response id routed to the
external grader, scores returned per part), or (b) a PCI-response -> external-grader route (let a PCI hand
a structured payload to ExternalApiScore instead of only match_correct).

## What the platform could expose (either is sufficient)
- **Per-part external scoring:** a composite item's ExternalApiScore call carries each `RESPONSE_*` and the
  grader returns a score+feedback per response id, settled as per-part outcomes in Results; OR
- **PCI -> external-grader seam:** allow a PCI's `getResponse()` structured payload (not just a match string)
  to be POSTed to the registered external grader, so custom interactions can be AI-rubric-scored.

## Ask for the platform team (Andy)
1. Confirm whether per-SECTION (per-field) AI rubric scoring of one structured writing artifact is on the
   Platform3 roadmap, or intentionally out of scope (holistic-only).
2. If in scope, decide which seam: per-part scoring on composite FRQs, or a PCI->external-grader route.
3. Until then we ship whole-artifact holistic scoring (no interim built) - this gap does not block the
   pilot; it bounds how granular writing feedback can be.
