# G11/G12 CCSS Re-skin — replacement key

**Date:** 2026-07-17
**Decision (Noel):** Treat G11/G12 as **standard CCSS 11-12 writing courses**, not AP-track. Content is already in-band (Fable + CCSS audit); this is a **re-skin** — strip AP-exam vocabulary from student-facing text, keep every skill. `ACC.W.INQ.1` stays (additive differentiation, not removed).

**Scope:** STUDENT-FACING text only — lesson titles, slot titles, slot `body` HTML, and the PP100 mastery prompts. **Do NOT touch** code comments, `council:`/build-note strings, module docstrings, or internal metadata (those legitimately reference FRQ/Row C as authoring provenance).

**Golden rule:** replace the AP *label* with the CCSS *skill it already is*. Never change what the lesson teaches — only the words that frame it as exam prep.

---

## Replacement key (student-facing occurrences)

| AP term (count, student-facing) | CCSS-honest replacement | Rationale |
|---|---|---|
| **"sophistication" / "sophisticated"** (47 + 27) | **"complexity" / "nuance"** — or, where it's the graded quality, **"depth and significance"** | The AP "sophistication" quality = W.11-12.1a *establish significance* + W.11-12.1b *develop claims/counterclaims fairly, note strengths & limitations*. "Write with complexity/nuance" is the same skill in CCSS words. |
| **"the sophistication point" / "Row C"** (17) | **"the complexity move"** / **"the depth-and-significance criterion"** | Drop the rubric-cell label; keep the criterion. In self-score lessons: "predict whether your argument reaches real complexity," not "earned Row C." |
| **"FRQ" / "FRQ type"** (38) | **"writing task" / "writing task type"** | The skill is task-analysis: recognize whether a prompt calls for synthesis, rhetorical analysis, or argument. That's W.11-12.4 (task/purpose/audience) + W.11-12.7/9 — reading the task, not naming an exam item. |
| **"FRQ section" / "3-FRQ section"** (G12 gate) | **"a set of three writing tasks" / "the writing set"** | Keep the multi-task gate (writing across three modes = full W.11-12.1/7 + RI.11-12.6 range); drop "FRQ section." |
| **"full-write" / "full write"** (13) | **"full essay" / "complete essay"** | Plain CCSS term for a sustained piece (W.11-12.10). |
| **"AP Lang" / "AP Lang FRQ2 shape"** (2) | **remove the AP reference**; keep the shape as **"a full rhetorical-analysis essay"** | The RA essay = RI.11-12.6 applied in writing; the "FRQ2" tag is pure exam packaging. |
| **"the exam" / "exam conditions"** (4) | **"timed writing" / "a single sitting"** | W.11-12.10 Range of Writing names timed/single-sitting writing explicitly. Keep the timed-practice skill, drop "exam." |
| **"free-response"** (1) | **"written-response" / "essay"** | Generic term; "free-response" is a testing term. |
| **"Row A / Row B"** (rare, in trait labels like "Trait: Evidence and Commentary (Row B)") | drop the "(Row X)" parenthetical; keep the trait name | The trait names (Thesis, Evidence, Development) are CCSS-legible; the Row letters are AP rubric coordinates. |

---

## Per-lesson title changes (the 7 AP-worded titles, all G12)

| Lesson | Current title | Proposed CCSS title |
|---|---|---|
| C1201-0004 | Write a Full Argument That Earns Sophistication | Write a Full Argument With Real Complexity |
| C1201-0005 | Analyze the Rhetoric With Sophistication | Analyze the Rhetoric With Depth |
| C1201-0006 | Write a Full Synthesis That Earns Sophistication | Write a Full Synthesis That Weighs the Sources |
| C1201-0007 | Predict Whether You Earned Sophistication, Then Check | Predict Whether Your Essay Reaches Real Complexity |
| C1202-0012 | Name the FRQ Type Before You Write | Name the Writing Task Type Before You Write |
| C1202-0013 | Switch Move-Sets Between Two Different FRQs | Switch Move-Sets Between Two Different Writing Tasks |
| C1202-0016 | G12 Gate: Write a Full FRQ Section, Type by Type | G12 Gate: Write Across Three Writing Tasks, Type by Type |

(G11 titles are already CCSS-clean — no title changes needed there.)

---

## What does NOT change
- **Any skill or content** — every lesson keeps its teaching, model, discrimination, and write.
- **Timed-writing practice** — reframed as W.11-12.10 "single sitting" writing, not removed (Timeback is untimed anyway; the lessons already say "no platform timer / run your own budget").
- **`ACC.W.INQ.1`** on the 4 G11 lessons — kept as the documented additive differentiation tag; those lessons also carry CCSS 11-12 tags.
- **Internal authoring notes** (comments, `council:` strings, docstrings) — untouched; they may keep AP/FRQ/Row-C provenance.
- **Lesson IDs, refs, banks, rubric_ref, units** — stable.

## Verification after edits
- `python pipeline/tier_a_regression.py G11` and `G12` → both stay clean (this is copy-only; no structural change).
- `python -m pytest pipeline/tests/ -q` → green.
- Re-grep student-facing text for the AP terms → expect 0 remaining (comments/council excluded).
- Spot-render 2-3 reworded lessons to confirm the copy reads naturally.
