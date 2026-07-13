# Writing MCQ / Selected-Response Item-Type Catalog (assessment x format x Timeback feasibility)

**Purpose:** catalog the SELECTED-RESPONSE item FORMATS the reference standardized tests use to measure writing/sentence skills, cross-referenced against Timeback QTI deliverability. Answers "in what item types are writing skills actually tested, and can we build each in Timeback?" Feeds three consumers: (1) format-faithful lesson discrimination/transfer items, (2) the two-bucket test-bank SR emitter, (3) the Timeback push pipeline (JSON vs XML vs PCI routing).

**Sources:**
- Item formats: the 5 released-test batches (`ReleasedTests/batch1-5*.md`), consolidated in `_evidence/sentence_skill_assessment_evidence.md`, + `TestDesign_Reference.md` §3.
- Timeback feasibility: the timeback skill `references/interaction-types.md` (QTI Interaction Type Status Matrix) + `references/create-mcq.md` (multiselect support).

**No copyrighted item text.** Formats, option-counts, and shell names only.

---

## 1. The item formats states actually use for writing SR (with which tests)

| Format (test's term) | QTI interaction type | Which reference tests use it for WRITING skills (cited) |
|---|---|---|
| 4-option MC, "NO CHANGE" option | `choice` (maxChoices 1) | ACT English [batch4 L30-42]; TN Editing Task [batch1 L162-164]; STAAR editing/revising [batch1 L61-63]; SAT single-MC per short passage [batch4 L85-95]; AP Lang MC "evaluate revisions" [batch4 L127]. THE workhorse. |
| Passage-based MC (underlined span in a draft) | `choice` | ACT [batch4 L30-42]; STAAR revising/editing passages [batch1 L61-63]; SAT 25-150-word passage + 1 MC [batch4 L85-95]. |
| Multiselect (choose N correct) | `choice` (cardinality multiple, maxChoices 2+) | STAAR new-question-types [batch1 L62]; FL FAST [batch3 L166-172]; SBAC [batch3 L69]. |
| Inline-choice / dropdown (pick the correct form in-text) | `inline-choice` | STAAR new-question-types [batch1 L62]. (Classic conventions/formation shell.) |
| Hot text (select the word/phrase/sentence) | `hottext` | STAAR Hot Text [batch1 L62]; SBAC hot-text [batch3 L69]; FL FAST Hot Text [batch3 L166-172]. Used for error-spotting + evidence selection. |
| Two-part EBSR (Part A + Part B evidence) | `choice` x2 (two linked choice items) | FL FAST EBSR [batch3 L166-172]; MD MCAP 2-part [batch2 L196-197]; SBAC. Mostly reading/evidence, but the shell applies to evidence-in-draft. |
| Match table grid (match options across rows/cols) | `match` | STAAR Match Table Grid [batch1 L62]; OH table matching [batch1 L106]; SBAC matching-table [batch3 L69]. |
| Text entry (type a short word/phrase) | `text-entry` | STAAR Text Entry [batch1 L62]. |
| Hot spot (click an image region) | `hotspot` | STAAR Hot Spot [batch1 L62]. Rare for writing (more reading/graphic). |
| MC two-part (2 pts) | `choice` x2 | MA MCAS Language SR [batch5 L76]. |
| Technology-enhanced (drag-and-drop etc., CBT only) | `gap-match` / `graphic-gap-match` | MA MCAS Tech-Enhanced [batch5 L76]; FL FAST Multimedia [batch3 L166-172]. |

**Not an SR format (scored in the essay rubric instead):** NY Regents, LA LEAP, MD MCAP, SC (essay), SBAC full-write, FL B.E.S.T. essay, NJ, MA essay all fold conventions into a holistic Conventions/Language rubric DIMENSION, NOT discrete SR items [assessment-evidence §per-system]. So for those systems the "item type" for sentence skills is the CR essay + rubric (external grader), not MCQ.

---

## 2. Item-type x Timeback QTI deliverability (the gate)

From the Timeback interaction-type matrix. This determines push cost, NOT whether we build the item.

| Format | Timeback type | JSON-safe? | Deliverability verdict |
|---|---|---|---|
| 4-option MC / NO CHANGE / passage-based MC | `choice` | YES | GREEN. JSON POST. Most reliable. The default for all sentence-skill SR. |
| Multiselect | `choice` (cardinality=multiple, maxChoices 2+) | YES | GREEN. JSON POST supported (create-mcq: "Multi-select IS supported ... XML correctly stores max-choices"). |
| Text entry (word/phrase) | `text-entry` | YES | GREEN. JSON POST. Good for "type the corrected word." |
| Order / sequencing | `order` | YES | GREEN (not a common writing-SR shell, but available for sentence-ordering). |
| Inline-choice / dropdown | `inline-choice` | NO | AMBER. Deliverable but XML POST REQUIRED (JSON corrupts). Higher build cost. |
| Hot text (select words/sentences) | `hottext` | NO | AMBER. XML POST REQUIRED. Deliverable; the key error-spotting shell, worth the XML cost. |
| Match table grid | `match` | NO | AMBER. XML POST REQUIRED (JSON corrupts directedPair scoring). Deliverable. |
| Two-part EBSR | 2 linked `choice` | YES (each) | AMBER. Each part is JSON-safe `choice`, but linking Part A->B correctly is a two-item build + response dependency; doable, more assembly. |
| Hot spot / select-point | `hotspot`/`select-point` | NO | AMBER. XML REQUIRED. Rare for writing; skip unless needed. |
| Technology-enhanced drag-drop | `gap-match`/`graphic-gap-match` | NO | RED-ish. XML REQUIRED + `graphic-gap-match` has a known 1-association-at-a-time bug. Avoid for production; substitute `match` or `choice`. |
| Adaptive difficulty (SAT-style) | `adaptive` | n/a | RED. "API accepts but renderer incomplete" -> appears broken to students. Do NOT replicate SAT adaptivity at item level; sequence difficulty at the bank/test-assembly layer instead. |
| Essay + rubric (the EOC-state pattern) | `extended-text` + external grader | YES (text) | GREEN for capture; scoring is the EXTERNAL grader (rc.* configs), not QTI auto-key. This is how most states actually score sentence skills. |

---

## 3. Recommended emitter policy (what the SR bank should produce)

Ranked by cost-adjusted fidelity to real tests:

1. **Default GREEN tier (build first, JSON POST):** 4-option MC with NO-CHANGE (covers ACT/SAT/STAAR/TN/AP), multiselect, text-entry. This alone faithfully covers the single most common writing-SR shell across every discrete-editing system.
2. **High-value AMBER tier (build, XML POST):** hot-text (error-spotting / select-the-sentence, heavily used by STAAR/SBAC/FL) and inline-choice dropdown (STAAR conventions). Worth the XML cost because they are distinct cognitive tasks students will face, not cosmetic variants of MC.
3. **Assembly AMBER tier (build when evidence-in-draft is targeted):** two-part EBSR as two linked `choice` items.
4. **Match `match` (XML):** only where a test genuinely uses grid-matching for a writing skill (limited; STAAR/OH/SBAC). Low priority for sentence-level.
5. **AVOID:** `graphic-gap-match` (known bug), `adaptive` (renderer incomplete), hot-spot for writing (rare). Replicate SAT adaptivity at the test-assembly layer, not the item.

**Bottom line for feasibility:** every writing SR format states use is deliverable in Timeback EXCEPT item-level adaptivity and drag-to-graph. The real cost distinction is JSON (MC/multiselect/text-entry) vs XML (hot-text/inline-choice/match). Nothing writing-relevant is infeasible; the SR emitter must therefore support an XML path, not JSON-only.

---

## 4. Consequences for the progression map + lessons

- **Map exemplars were all 4-option MC**, which understates real variety. They should span at least: MC/NO-CHANGE, hot-text (select-the-error / select-the-best-sentence), and inline-choice dropdown, so lesson designers see the true format set. (Applied to `Sentence_Progression_G9-12.md` exemplar section.)
- **Lesson discrimination/transfer items** should rehearse students in the SAME shells they will be tested in: NO-CHANGE MC + hot-text error-spotting are the two highest-frequency, so lessons should default to those, not generic MC only.
- **Timeback QTI limits already in the lesson gates hold:** stimuli display-only, items stateless, choice=select->submit->feedback, extended-text->external grader. The new fact this catalog adds: the SR emitter must route hot-text/inline-choice/match through XML POST, and must NOT emit adaptive or graphic-gap-match.

## 5. Open follow-ups (non-blocking)
- MA MCAS item library (`mcas.cognia.org/item-catalog/`, browsable by L.1/2/3 standard) is the one source that could confirm which exact shells MA uses per sentence sub-skill. Fetch if we want tighter shell-per-skill mapping.
- SBAC/SC exact per-shell counts were COULD_NOT_VERIFY in mining; refine if the bank needs precise shell proportions.
