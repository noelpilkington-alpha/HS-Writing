# Pipeline Hardening Checkpoint (Tiers A–C)

**Date:** 2026-07-16
**Goal (Noel):** *"our next run can lead to me reviewing courses with no issues"* — and reviews get **cleaner over time**, not re-finding the same defect classes.
**Scope this pass:** harden the pipeline + course-side (Tiers A–C) and re-verify existing G9. Grader / Tier D deferred by decision.

---

## The one-paragraph version

Every defect this session surfaced now has (1) an automated check that catches it and (2) a permanent fixture so it cannot silently come back. The deterministic floor (Tier A) **independently rediscovered exactly the 4 real content defects** the human review + Fable audit found — with zero false alarms. The semantic defects that no fixed rule can judge (also-correct distractor, wrong-grain planner, phantom draft) are covered by an LLM judge that has to **earn** the right to block. And there is now one honest number — `caught_by_human_not_by_gate` — that is **0**, verified against the live corpus, not self-reported.

---

## Tier A — the deterministic floor (offline, no LLM)

One runner, `pipeline/tier_a_regression.py`, runs every deterministic gate on every lesson and emits a per-lesson receipt:

- **25 contract gates** (shell, binding, discrimination-before-production, length-cue, em-dash, gate-shape, …)
- **render-fidelity** on the actually-rendered artifact (with the source lesson, so the option-count cross-check is live)
- **register / credibility** (childish openers + leaked auditor jargon)
- **mastery genre-match + Webb DOK**
- **10 stimulus-contract gates** for every bound source

**New gates added this session:** mastery-genre/DOK (A5), render-fidelity (A6), register (A7), structural-item (A8).

**Fail-opens closed:** discrimination `any()`→`all()`; `distractor_length_cue` (caught a real lone-longest key); and the **register-gate hole** — it scanned lesson slots but the childish "The topic here is…" actually lived in the *stimulus passage*, so as first shipped it would **not** have caught the exact defect you flagged. Now scanned at the source.

**Result on the live course:**

| Grade | Lessons | Clean | Blockers |
|---|---|---|---|
| G9 | 27 | **27** | 0 |
| G10 | 26 | 24 | 2 (mastery-genre) |
| G11 | 31 | 30 | 1 (mastery-genre) |
| G12 | 16 | 15 | 1 (mastery-genre) |
| **Total** | **100** | **96** | **4** |

The only 4 blockers are the genuine mastery-genre mismatches (`C1006-0021`, `C1003-0025`, `C1102-0030`, `C1202-0012`) — the same set the manual triage found. **No noise.** The one over-flag the runner initially produced (issue_frame orientation cards failing the full source-passage contract) was resolved with a written exemption: those short claim-tier cards are Lexile/fact-table exempt by design, but their register/content/provenance gates stay enforced.

**G9 receipt:** `COURSE_G9_TIER_A_RECEIPTS.json` — 1,286 individual gate checks across 27 lessons, all passing.

---

## Tier B — make the LLM judges trustworthy before they can block

`pipeline/tier_b_judge.py`. The semantic defects need an LLM, and an LLM judge rots. So a judge must **earn** block authority:

- **B1 adversarial per-rule verifier** — fail-closed: it must try to *refute* a pass and defaults to FLAG when unsure.
- **B5 three-way verdict** — PASS / FAIL / **LOW_CONFIDENCE→human triage** (never a silent hard-fail).
- **B6 probe-before-block** — a judge is scored on the labeled calibration key; it clears only at recall 1.0 **and** precision 1.0.
- **B7 promotion + kill-switch** — block authority only after **3 consecutive clean probes**; one bad run resets the streak; a kill-switch file demotes a drifting judge instantly with no code change.

**Live check:** the Fable-5 adversarial verifier **clears the probe** under the stricter fail-closed framing (recall 1.0, precision 1.0), currently `streak 1/3, can_block=false` — cleared once, not yet promoted, exactly as designed. This also confirms the correct `.env` API key works end-to-end.

*(B2 cross-family GPT review, B3 vision review, B4 ≥5-override calibration are interface-ready but need external providers / scarce override data — not faked.)*

---

## Tier C — the compounding layer (what makes reviews get cleaner)

`pipeline/compound_learning.py`. **C2 is the one number:** `caught_by_human_not_by_gate` = defects with no verified automated coverage. It must trend to 0.

The honesty guarantee: `verify_coverage()` checks each tracked defect's claimed anchor **against the live corpus** — does that fixture / gate / calibration case actually exist? A record that claims "covered" but whose anchor is missing counts as **uncovered**. You cannot lie the metric green.

**Current state:** 8 defects tracked (this session's set), **8/8 verified covered, `caught_by_human_not_by_gate = 0`, coverage 100%.** The suite has caught up to every known defect. **C1 ratchet:** when a human catches a new defect, `next_actions()` surfaces the exact fixture/case to add — the mechanism that converts a review catch into a build rejection.

---

## Verify-the-verifier status

- **90 tests green** (contract corpus, register, mastery-genre, render-fidelity, judge calibration, Tier-B machinery, compound-learning, Tier-A runner).
- **Checker corpus 20/20** — every gate proven to reject the defect it claims to catch.
- **Judge calibration** — live Fable scored composite 1.00 against the semantic-defect answer key.

---

## Honest caveats (what this does *not* claim)

1. **G10–G12 still have 4 real content defects** (the mastery-genre mismatches). G9 is clean; the other grades need the mastery source swapped before they ship. The gate now *flags* them every run — fixing them is content work, not pipeline work.
2. **A fully-autonomous zero-issue run is not yet guaranteed.** Pedagogy-semantic defects still route through the LLM judge, which is trustworthy on the *known* classes but has not earned autonomous block authority yet (streak 1/3). New, never-seen defect classes will still need a human the first time — then the ratchet makes them automatic.
3. **Grader / Tier D is untouched** (deferred by your decision).
4. Nothing has been pushed. Direct-to-Timeback + Platform3 prep remain gated on your approval.

---

## What I recommend next

- **Fix the 4 mastery-genre mismatches in G10–G12** (swap each held-out mastery source to the taught genre) so all four grades reach the G9 clean bar.
- **Then re-run `tier_a_regression.py all`** → expect 100/100.
- Optionally, run a full G9→G12 generation to see the hardened output end-to-end before any push.
