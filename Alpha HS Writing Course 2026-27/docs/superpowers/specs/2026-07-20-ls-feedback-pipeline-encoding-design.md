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
- **Cadence decided by the council-of-writing-instruction (2026-07-20; KH/WH/DI/SRSD/Yeager, adjudicated by evidence, losers named).** N is a per-archetype CEILING, not a quota:

  | Archetype | N ceiling (max consecutive counted segments before a mandatory check) |
  |---|---|
  | concept-teaching | **3**, tightened to **2** in the window right after any memorizable-tool card |
  | checking/revision | **2** |
  | full-essay-build | **4**, at production milestones only (after-plan, after-paragraph), never mid-draft |

- L2 playbook: author to these ceilings; check-type shifts along the arc (recall → apply → self-regulation).
- L3: new `gate_check_cadence` — walk the slot sequence; fail if a run of counted segments exceeds the archetype ceiling with no intervening qualifying check.
  - **Segment counting:** each teach_card / annotated_before_after / stimulus_display = +1; a worked example (annotated_before_after) counts as **ONE** regardless of length; buy-in/Discuss-It teach cards count **+0** (tagged); narration/glossary not counted.
  - **What resets the counter (a qualifying check):** a discrimination / predict_the_fix / self_score that is a use/apply item (not verbatim recall of the last card) AND has per-choice reveal for every option. (The "per-choice reveal exists" half is gateable via `structural_item`; the "is a use item / genuinely process-level" half is playbook + review — see PLAYBOOK-NOT-GATE.)
  - **Memorizable-tool trigger:** if the most recent counted card introduces a named tool/mnemonic (e.g. the 3-question test), the effective ceiling until the next check = min(archetype-N, 2), and that check should be a recall item.
  - **Worked-example rule (firm, near-unanimous):** NEVER place a check inside a worked example; the check fires at the seam immediately after, on a NEW prompt (tests transfer, not echo).
  - **Exemptions:** scaffold-free GATE/assessment lessons (no teaching checks required); mid-worked-example; the final independent write/draft block; buy-in/Discuss-It cards (count 0).
- Fixtures: BAD = 4 counted teach cards in a row, no check (concept archetype); BAD = a check placed inside a worked example; GOOD = teach, teach, check, teach; GOOD = a worked example (long, multi-card) counted as one, check at the seam after.
- **Requires a card/lesson tagging layer** (archetype + per-card type incl. memorizable-tool, buy-in, worked-example, production-block). Tagging integrity is load-bearing per the council (mis-tag → wrong gate); add a tagging-presence check.

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

**Council items that are authoring guidance, NOT the deterministic gate (go to the playbook + review):**
- **Feedback quality wording** (WH): the gate enforces per-choice reveal *exists* for every option; it cannot enforce that the wording is genuinely process-level / feed-up-back-forward. Authoring rule + review.
- **Tone / status-respect framing** (Yeager): say the standard out loud up front; presume competence in item difficulty; wise-feedback reveal (no person-praise, no compliment-sandwich). If ignored, a frequent-check cadence reads as surveillance and backfires — but it is not a build check.
- **Test-out / skip-ahead** (Yeager): pass a cold check → skip intervening cards. Recommended as an OPTIONAL UX enhancement, NOT part of the deterministic minimum gate; it also answers SRSD's worry (a *real* cold check is self-gating, so struggling writers can't skip past the retrieval they most need). Log as a product enhancement, not built here.

## Pilot-first workflow

1. **Build L1 helper changes + L3 gates + L2 playbook edits**, each gate with its paired BAD/GOOD fixtures. Gates go in green (fixtures pass) but are NOT yet applied course-wide.
2. **Apply to TWO pilot lessons (Noel):**
   - **G9 L01 `arguable_claim`** (`lesson_g9_l01_arguable_claim_v3_1.py`) — exercises the most new gates at once: the side+reason frame (#2), the "check and fix" diagnosis (#6), MCQ option count (#8), teach→check cadence (#3). Highest-traffic foundational lesson; sets the "voice."
   - **one of `l03` (controlling_idea) or `l04` (interleave)** — chosen so #7 (odd stem wording) and #9 (repeat-gloss of "controlling idea") are also piloted. `l03` is the stronger pick (it re-uses "controlling idea," directly exercising #9); confirm during planning.
3. **Render before/after for both; Noel compares.**
4. **On sign-off:** run `tier_a_regression.py` course-wide → the new gates emit the exact non-compliant-lesson list → roll out. The #8 4th-distractor pass (~118 items) runs **immediately after the pilot** (Noel) as a parallel-agent authoring pass with the gate as backstop; the cheaper edits (#2/#3/#6/#9) roll out in the same wave.

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

## Decisions (open questions resolved)
1. **Check cadence N** (#3): **per-archetype ceiling** (concept 3→2-after-tool / checking 2 / build 4), decided by the council — see #3 above. NOT a global N.
2. **#8 rollout sequencing** (Noel): do the ~118-item 4th-distractor authoring pass **immediately after the pilot**.
3. **Pilot scope** (Noel): **G9 L01 + one of {l03, l04}** so #7 (odd stem wording) and #9 (repeat-gloss) are also piloted before rollout.

## Cross-lesson caveat (council, grade A — do not lose)
The in-lesson cadence gate is **necessary but not sufficient** for durable recall (spacing g=0.74). The same tools must be retrieved again in *later* lessons — a course-sequence-level requirement owned by `pipeline/course_sequence_g9_12.py` / the sequence builder, NOT the per-lesson gate. The cadence gate must not create false confidence that retention is handled.
