# Encoding the Learning-Scientist Feedback into the Generation Pipeline — Design

**Date:** 2026-07-20
**Author:** with Noel (HS Writing)
**Status:** DRAFT for review → implementation plan

## Problem

A learning scientist reviewed the G9–G12 course and gave 9 pieces of feedback (praise + 8 change requests). The changes are correct, but the risk is that we fix them as **one-off edits to existing lessons** — which does nothing for **continued generation**. Every future lesson would reintroduce the same defects. This spec encodes the feedback into the layers that *drive* generation, so new lessons comply by construction and drift is caught by the build.

**Decision (Noel, 2026-07-20):** enforcement posture = **gate everything mechanically checkable.** Where a rule can be checked deterministically, it becomes a hard build-blocker (`tier_a_regression` fails), which also yields the exact list of non-compliant existing lessons for a complete rollout.

## The enforcement chain (three layers)

The course already enforces quality through three layers. Each fix must land in the correct layer or it will not stick.

| Layer | File(s) | Role |
|---|---|---|
| **L1 · Shared helpers** | `pipeline/lesson_prompts.py` (`setapart`, `frq_prompt`, `checklist`, `outline_table`) — imported by 98 lessons | Fix a structural default once; all callers inherit it |
| **L2 · Archetype playbooks** | `_phase2/playbook_T*.md` (T2 STAND, T3 PROVE, T5 CHECK, T6 SPOT, T7 BUILD) — the spec authoring agents follow when generating a lesson of that archetype | New lessons comply by construction |
| **L3 · Deterministic gates** | `pipeline/lesson_contract.py` (26 gates today; registry `_GATES`) — build fails on violation, verified by `tier_a_regression.py` | Catches drift; makes rollout complete + verifiable |

**Verify-the-verifier doctrine (non-negotiable):** every new/changed gate ships with paired fixtures in `pipeline/tests/` — a KNOWN-BAD lesson slot that MUST trip the gate, and a KNOWN-GOOD one that must NOT. A gate with only passing fixtures validates nothing.

## Per-item mapping

Praise (#1) needs no action. The other 8:

### Gated (mechanically checkable) — hard build-blockers

**#2 — No comma before "because" in a fill-in frame.**
- Claim: `Schools should ______ [your side], because ______ [your reason]` — the comma is wrong in a restrictive fill-in frame.
- L1: fix the frame text in the ~5 G9 files that hardcode it; going forward, add an optional `frame=` builder to `lesson_prompts` that emits side/reason frames without the comma so authors stop hand-writing it.
- L3: new `gate_frame_comma` — flags `, because ___` / `, so ___` patterns inside `setapart` frame blocks (student-facing). Scope: frames only (a comma before "because" in ordinary prose is fine), so the gate keys on the set-apart-frame context, not all prose.
- Fixtures: BAD = a frame with `, because ___`; GOOD = a frame with ` because ___` and a normal sentence that legitimately has `, because`.

**#3 — Check cadence: flip card→check often enough to force recall.**
- Claim: students scroll past great content; we want frequent small checks so they recall tools (e.g. the 3-question test).
- L2: playbook rule — no more than N consecutive teach/stimulus segments without an intervening checkpoint (discrimination / predict_the_fix / self_score). Propose **N = 3** (tunable in review).
- L3: new `gate_check_cadence` — walk the slot sequence; fail if > N teach-family slots occur with no checkpoint between them. Exempt scaffold-free GATE lessons (they are certification, not instruction) and the final write block.
- Fixtures: BAD = 4 teach cards in a row, no check; GOOD = teach, teach, check, teach.
- Open question for review: is N=3 right, or per-archetype?

**#6 — "Check and fix" must make the student ANSWER the 3 questions, not read pre-answered ones.**
- Claim: the diagnosis prompt currently answers its own check ("Does it take a side? No…"); the student should answer each check AND then improve.
- This is the "checks that run themselves" pattern. The Timeback-honest structure: convert the pre-answered diagnostic into a real **checkpoint** — a discrimination/predict item where the student answers the check question(s) and gets reveal feedback — placed BEFORE the improve-write. The improve-write stays an extended-text box.
- L2: playbook rule for the CHECK/diagnosis beat — the check questions are posed as an answerable item; the modeled answer is post-answer reveal, never inline in the prompt the student reads first. (Coping-model demos on a PROVIDED weak draft remain legitimate; the rule targets the student's OWN check turn.)
- L3: extend `gate_leaked_answer_cue` (or a sibling `gate_self_answered_check`) — a diagnosis_frq whose prompt states its own check answers ("? No," / "? Yes,") with no separate answerable item fails. Must NOT fire on the sanctioned coping-model (a provided weak draft explicitly labeled as a demo followed by an independent student turn) — this is the exact confound the sim-student adversarial pass identified, so the gate needs the coping-model carve-out and a fixture proving it.
- Fixtures: BAD = diagnosis prompt with `Does it take a side? No. Pick one.` and no answerable item; GOOD = a checkpoint that asks the question + a coping-model demo that is NOT flagged.

**#8 — Four options per summative MCQ, each a real distractor.**
- Claim: 3 options → higher guess rate; use 4.
- L2: playbook rule — discrimination items author **4 options**, each 4th a *named misconception*, never filler (filler is worse than 3 per our distractor-quality rule; ties to the T1-C misconception taxonomy).
- L3: change `gate_structural_item` option-count from "2–4 allowed" to **"discrimination requires exactly 4"** (self_score keeps its 2-point predict form; predict_the_fix keeps its form). This immediately flags ~118 existing 3-option discriminations as failing — expected under the gate-everything posture; that failure list IS the rollout worklist.
- Fixtures: BAD = a 3-option discrimination; GOOD = a 4-option one; self_score 2-option still passes.
- Scope note: this is the largest downstream authoring surface. The gate is the backstop; the rollout (adding a quality 4th distractor to each item) is a separate parallel-agent authoring pass AFTER the pilot, not part of the pilot.

**#9 — Repeat the "controlling idea" gloss, not just first-use.**
- Claim: the term is glossed once then dropped; being an odd phrase, re-gloss it periodically.
- L2: playbook rule — for a designated set of HARD terms (controlling idea, warrant, synthesis, counterclaim), re-gloss in brackets on re-introduction in a later lesson, not only first use.
- L3: extend `gate_define_before_use` → for HARD_TERMS, require a gloss on first student-facing use *within each lesson that uses the term* (not just the first lesson in the course). Keeps the existing first-use logic; adds per-lesson re-gloss for the hard-term subset.
- Fixtures: BAD = a later lesson using "controlling idea" with no gloss; GOOD = one that re-glosses it.

### Playbook-only (not mechanically checkable)

**#4 — Click-to-reveal on sentence-improving (light interaction).**
- The *separable* form is buildable now: pair each improve-write with a `predict_the_fix` (diagnose → click → reveal). L2 playbook rule to author that pairing where an improve-write stands alone.
- The *full* form (a reveal tuned to the student's OWN typed sentence) needs branching → **external-app / PCI track**, logged, NOT gated.

**#7 — "Which sentence fits that verb" reads oddly → "Which sentence explains?"**
- Phrasing quality is not mechanically gateable. L2 playbook wording rule: discrimination stems name the move directly ("Which sentence explains?" / "Which addresses the question?"), not meta-phrasings ("fits that verb"). Verified in review.

**#5 — Setup video with embedded questions; animate side+reason as puzzle pieces.**
- Static **SVG** (puzzle-piece "arguable claim = side + reason") + narration audio: buildable now via the existing visual-design-protocol Track A; L2 playbook note.
- Hosted/embedded-question **video** (Peter Bates style): the player strips `iframe`/script, so NOT possible in the current gated format. Log to the external-app track. NOT auto-solved by Platform3 (that is a content-surface change, not a confirmed richer player) — do not promise it there without evidence.

## Pilot-first workflow

1. **Build L1 helper changes + L3 gates + L2 playbook edits**, each gate with its paired BAD/GOOD fixtures. Gates go in green (fixtures pass) but are NOT yet applied course-wide.
2. **Apply to ONE pilot lesson: G9 L01 `arguable_claim`** (`lesson_g9_l01_arguable_claim_v3_1.py`). It exercises the most new gates at once: the side+reason frame (#2), the "check and fix" diagnosis (#6), 3-option MCQs (#8), teach→check cadence (#3). Also the highest-traffic foundational lesson, so its "voice" sets the template.
3. **Render before/after; Noel compares.**
4. **On sign-off:** run `tier_a_regression.py` course-wide → the new gates emit the exact non-compliant-lesson list → roll out (parallel-agent authoring pass for #8's ~118 items; targeted edits for the rest), gate as backstop.

**Pilot coverage gap (flagged):** #7 lives in l04/l06 and #9 in l03, so the G9 L01 pilot will not show those two. Verify them on a second spot-check lesson (l03 or l04) before full rollout.

## What we are NOT doing
- Not adding gates for phrasing quality (#7) or visual choices (#5/#4-partial) — not mechanically checkable; playbook + review.
- Not building embedded-question video or answer-adaptive reveal in this work — external-app/PCI track, logged.
- Not doing the #8 course-wide 4th-distractor authoring pass inside the pilot — the pilot proves the gate + the pattern on one lesson; the pass follows sign-off.
- Not touching lesson IDs, mastery keys, or the grader.

## Success criteria
- New gates each have a passing BAD+GOOD fixture pair; full `pytest` green.
- Pilot lesson G9 L01 passes all gates (old + new) and renders cleanly.
- Noel approves the before/after.
- The gates, run course-wide, produce a concrete, complete rollout worklist (no silent misses).
- Playbooks updated so a fresh authoring agent generating a new lesson would comply without seeing this doc.

## Open questions for review
1. **Check cadence N** (#3): N=3 global, or per-archetype (e.g. denser for T5 CHECK)?
2. **#8 rollout sequencing:** do the ~118-item 4th-distractor pass immediately after the pilot, or batch it as its own tracked project after the cheaper items ship?
3. **Pilot scope:** G9 L01 only, or L01 + one of {l03, l04} so #7/#9 are also piloted before rollout?
