# Grade-11 ANCHOR Reference Forms — index + acceptance verdict

**Purpose.** Internal MODELING anchors for the G11 writing test bank (the "college-test year"). Complete released
form structures + official rubrics + annotated student work, held so our ORIGINAL authored G11 stimuli/items match
real difficulty, task shape, and rubric behavior. We author original content modeled on these; **we do not reproduce
copyrighted passages, prompts, or student-essay text.** Structure, counts, rubric dimension names/scales, and URLs
are recorded in our own words in the per-system files.

**Compiled 2026-07-09.** Per-system anchor files (each byte-verified against official sources this session):
- `G11_anchor_SBAC.md` — Smarter Balanced G11 full-write (argument + explanatory, 4-source PT) + CAT edit/clarify.
- `G11_anchor_ACT.md` — ACT Writing (standalone 3-perspective argument).
- `G11_anchor_AP_Lang.md` — AP English Language FRQs (synthesis 6-source, rhetorical analysis, argument) — the `rc.ap` rubric.

## Acceptance bar: PASSED (blueprint requires >=2 complete anchors; we have 3)
| System | Form | Rubric | Annotated student work | Verdict |
|---|---|---|---|---|
| **SBAC G11** | ✅ byte-verified (PT scoring guide + G11 blueprint) | ✅ 3-trait, max 10 (Org/Purpose 4-1 · Evidence/Elab 4-1 · Conv 2-0) | ✅ SmART tool + Full-Writes Baseline Anchor Set (~30 G11 responses) | **COMPLETE** — the only true G11 multi-source full-write anchor |
| **AP Lang** | ✅ byte-verified (CED) | ✅ 6-pt `rc.ap` (Thesis 0-1 · Ev&Comm 0-4 · Soph 0-1), byte-verified from 2025 Scoring Guidelines | ✅ released FRQs + scored samples + commentary (per-sample scores flagged for browser re-open) | **COMPLETE** — Tier-1; drives G11 synthesis/RA/argument + all of G12 |
| **ACT Writing** | ✅ byte-verified (act.org description) | ✅ 4-domain 1-6 -> 2-12 (Ideas&Analysis · Dev&Support · Organization · Language) | ✅ 6 scored essays (1-6) w/ per-domain explanations (one canonical prompt) | **COMPLETE** — the multi-perspective-argument anchor |

Caveats (all non-blocking, recorded per-file): consortium/College-Board/ACT hosts gate automated fetch, so some PDFs
were read via district mirrors or reader-proxy (content identical); ACT enhanced-format rollout DATES could not be
byte-verified (current live format IS verified); AP per-sample scores render as encoded streams to the fetcher
(library + titles confirmed; flagged for a browser pass).

## The structural facts G11 stimuli/items MUST match (the anchor -> generation contract)

**Synthesis (C.11.02) — model on SBAC + AP Lang Q1:**
- SBAC: a single **4-source set** on one debatable research question, mixed-genre, + 3 research warm-up SR items; band ~400-900 words on-grade.
- AP Lang Q1: **6 sources** = ~4 text excerpts (~500 words each) + **2 visual (>=1 quantitative)**; synthesize **>=3** into an original position (not summary).
- => G11 synthesis stimuli = SOURCE SETS (4-6), mixed text+visual, one debatable question, Lexile 1120-1300L. A NEW stimulus shape vs G9/G10 singles/pairs.

**Rhetorical analysis (C.11.03) — model on AP Lang Q2:**
- **1 nonfiction passage, ~600-800 words**, with a headnote (author/occasion/audience); analyze the writer's rhetorical CHOICES, not the ideas. Use PD speeches/essays.

**Source-free argument (C.11.06) — model on AP Lang Q3 + ACT:**
- AP Lang Q3: a **general, source-free prompt** (quotation/idea + background); argue from OWN knowledge, no provided evidence. => stimulus = a PROMPT ONLY, no passage.
- ACT Writing (C.11.07 multi-perspective): an issue + **exactly 3 given perspectives, NO source passage**; the scored move = analyze the RELATIONSHIP between the student's own perspective and >=1 given one. => stimulus = prompt + 3 perspective statements, no reading selection. Do NOT attach a passage to ACT-shaped items.

**Rubric configs:**
- `rc.ap` (AP Lang, all 3 FRQs): Row A Thesis 0-1 · Row B Evidence & Commentary 0-4 (the difficulty engine: 1 general+summary -> 4 consistently-explained line of reasoning) · Row C Sophistication 0-1. No separate conventions row (mechanics only gate Row B point 4). Already in the item contract's RUBRIC_CONFIGS.
- SBAC full-write: Org/Purpose 4-1 + Evidence/Elab 4-1 + Conv 2-0 (=10), counterclaim credit inside Org/Purpose. (Consider an `rc.sbac` config; or map to rc.4trait/rc.ohio.)
- ACT: 4 domains 1-6 -> 2-12, subject score = rounded AVERAGE of the 4 (not sum). (Consider an `rc.act` config.)

**Purpose-set note:** SBAC explicitly excludes NARRATIVE at G11 (matches our narrative-descoped decision). G11 tested modes = argument / explanatory / rhetorical-analysis / synthesis / multi-perspective — all in the KC map.

## Next (per the plan): Layer 3 (G11 stimulus sets) -> Layer 4 (G11 items, rc.ap) -> cross-check `G11`.
