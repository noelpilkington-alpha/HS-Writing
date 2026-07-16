# Simulated-Student Curriculum Evaluation Harness — Design (G9 pilot)

**Date:** 2026-07-16
**Status:** design approved (brainstorming), pending spec review → planning
**Scope of first build/run:** Grade 9 only (27 v3.1 lessons + the G9 test bank). Harness is built grade-general; G9 proves it, then G10–G12 reuse it.

---

## 1. Goal

Use LLM agents that impersonate real students **with no knowledge of the course's development** to evaluate the HS Writing curriculum (currently building in Vercel for Timeback). Each simulated student reads every lesson in sequence, attempts every check and writing task, and takes the test(s), then the harness answers four questions:

1. **Do the lessons make sense for a student?**
2. **Are there redundancies being taught?**
3. **Do the lessons fully prepare them for the full compositions?**
4. **Do the courses prepare them for the tests?**

This is a **curriculum evaluation from the student's lived experience**, not a grading exercise.

## 2. Decisions locked (from brainstorming)

| Decision | Choice | Why |
|---|---|---|
| **Grading gap** | **Do NOT score writing.** | Automated grading isn't wired into the platform. Rather than couple the eval to the production grader (which we'd also be validating), findings come from the student's *lived experience*: confusion, friction, "I couldn't do this because X was never taught." |
| **Run scope** | **Pilot G9 first, then scale.** | ~100 lessons across G9–G12 is a large spend on an unproven harness. Prove useful, non-slop output on G9's 27 lessons, let Noel read it, then run G10–G12 with the tuned harness. |
| **Student memory** | **Continuous learner with an external structured journal.** | Redundancy + composition-readiness require the student to remember earlier lessons. To avoid context contamination/drift, memory is an **on-disk JSON "learner journal,"** not a growing raw transcript. Next lesson sees only the distilled journal + the new lesson. |
| **Personas (pilot)** | **On-grade average G9 student** (the design's target student). | One persona proves the harness cheaply. High-achiever (sharpest redundancy detector) and struggling/distractible personas are built into the persona list and added at scale-up. |
| **Model roles** | **Both Fable-5 and OpenAI as independent students; Claude synthesizes.** | Same persona walked twice, independently. Findings both models raise = robust; findings one raises = flagged model-specific noise. |

## 3. The "no knowledge of development" constraint — how it's enforced structurally

A simulated student must experience what a real student experiences: **the rendered lesson, not the Python source.** Feeding source code would leak internal design (gate names, `mnemonic_status`, "Grade-C design bet" labels, archetype tags) and violate the constraint.

**Enforcement:** the student agent is fed the output of `lesson_review.render_student_experience(L)` — the existing, proven, ordered student-facing walkthrough. It renders:

- teach/model bodies as plain prose (callout/panel text preserved, diagrams named by role),
- sources with the once-per-topic treatment the real player uses,
- MCQ options stacked as the player shows them,
- write prompts as the student sees them,
- **answer-key reveals held back until after the student responds** (post-answer feedback), exactly matching the live player.

The student agent never receives the `Lesson` object, gate list, KC tags, or any `_v3_1.py` file. This is a hard architectural boundary, not a prompt instruction.

## 4. Architecture

Standalone Python program under `pipeline/sim_student_eval/`. **Not** the Claude Code Agent/Workflow tools — because Fable-5 is not available as a Claude Code agent model in this environment but **is** callable via the Anthropic API as `claude-fable-5` (the exact pattern `pipeline/lesson_review.py` already uses). The harness is a plain script driven by `.env` keys.

```
pipeline/sim_student_eval/
  models.py         # thin clients: Anthropic (claude-fable-5) + OpenAI, both used AS STUDENTS.
                    #   Reads ANTHROPIC_API_KEY + OPEN_AI_API_KEY from HS Writing/.env. Never echoes keys.
  render_course.py  # loads G9 v3.1 lessons IN SEQUENCE, renders each to student-view text.
                    #   Reuses lesson_review.render_student_experience(L). Loader = the g9_assemble glob:
                    #   sorted(glob "Lesson_Bank_G9/lesson_g9_l*_v3_1.py") -> import -> module.LESSON.
                    #   Filename number (l01..l27) IS the sequence order.
  journal.py        # the external structured memory: read/append/validate a bounded JSON journal.
  student_agent.py  # ONE persona-walk for ONE model: per lesson -> attempt tasks -> emit journal update.
  test_taker.py     # the same student takes the G9 test carrying only the journal; logs attemptability.
  analyst.py        # Claude synthesis pass over ALL journals+transcripts: corroborate cross-model, detect
                    #   redundancy, composition-readiness gaps, test-readiness gaps.
  run_eval.py       # orchestrator: 2 models x 1 persona x 27 lessons + test -> writes report + evidence.
```

### 4.1 Data flow (per model-student, per lesson)

```
render_student_experience(L_n)  ─┐
journal_state (after L_{n-1})  ──┼─►  student_agent(model, persona)  ──►  {response, journal_update}
persona spec                    ─┘                                            │
                                                                              ▼
                                            append journal_update to journal_<persona>_<model>.jsonl
                                            append full transcript to transcripts_<persona>_<model>.jsonl
```

Context fed to lesson *n* is **constant-size**: `persona + distilled journal + rendered lesson n`. It never includes lessons `1..n-1` raw text. This bounds cost and eliminates the drift/contamination Noel flagged.

### 4.2 The learner journal (schema)

One JSON object appended per lesson to `journal_<persona>_<model>.jsonl`. This is the *entire* memory carried forward — auditable on disk, so every downstream finding traces to a specific entry.

```json
{
  "lesson": "g9_l11_two_evidence",
  "seq": 11,
  "skills_i_can_now_do": ["develop one point with two facts that add up", "state a warrant"],
  "terms_learned": ["warrant", "attributive tag"],
  "where_i_struggled": ["the coping-model think-aloud moved fast on the revise step"],
  "felt_repeated": {"echoes_lesson": "g9_l09_warrant", "what": "warrant was taught here again"},
  "open_questions": ["is a warrant different from the reason in my claim?"],
  "confidence": {"arguable_claim": 0.9, "warrant": 0.5, "two_evidence": 0.7}
}
```

- `felt_repeated` is `null` when nothing echoed. When present it names the earlier lesson — this is the **lived** redundancy signal (distinct from the analyst's analytical one).
- `confidence` is a running per-skill dict the student updates; a skill that never rises is a readiness red flag.
- The journal is **distilled by the student agent**, not the harness — the harness only validates the shape and truncates runaway lists.

### 4.3 Composition-readiness probes

At the paragraph gate (**L18**, `fresh_paragraph_selfcheck`) and the essay lessons (**L23** full argument essay, **L24** full informational essay, **L26/L27** cold gate essays), the student attempts the composition carrying **only the journal**. The agent is asked, in-character: *"Using only what you've learned so far, attempt this. If you can't, say exactly which skill you're missing."* The transcript captures whether the upstream lessons actually supplied the needed skills — answering question 3 with a concrete "L23 needs X; X was last seen at L09 and my confidence was 0.4."

### 4.4 Test-readiness (question 4)

The same student takes the **G9 test** carrying the journal. G9 test surface, in priority order:
- `model_test_g9.html` — the assembled model form (rendered; currently ~7 choice items in 1 section).
- `Item_Bank_G9/` CR items (`cr_argument`, `cr_analysis`, `cr_explanatory`) + SR items (`sr_*`) + `pp100_*` — the fuller bank.

`test_taker.py` presents each item as a student sees it (stem + options, or CR prompt), records **attemptability** (can the student even engage the item with what the course taught?) and, for each item they can't attempt, traces the gap to a lesson or flags "never taught." **No scoring of correctness of writing** — for MCQ/SR we can log the student's chosen answer vs key (that's deterministic, not a writing grade), which is a legitimate signal for "did the course prepare them." CR items are attemptability + self-reported gap only.

> Spec note: the exact set of test items to administer in the pilot is `model_test_g9.html` + the CR items in `Item_Bank_G9`. If the model form is too thin to be a fair test-readiness probe, `run_eval.py` also assembles the CR items directly. This is a config list in `run_eval.py`, not hardcoded.

### 4.5 Models: both as students, Claude synthesizes

- **Student A:** Anthropic `claude-fable-5` (proven callable via `.env` `ANTHROPIC_API_KEY`; the `lesson_review.fable_review` call shape is the template — `messages.create`, structured output via a forced tool call).
- **Student B:** OpenAI (via `OPEN_AI_API_KEY`) — structured output via a JSON schema / tool call so journal updates are machine-valid.
- **Analyst/synthesis:** Claude (the harness's own model, or `claude-opus`). Reads both students' journals + transcripts and produces the report. It labels each finding **CORROBORATED** (both students) or **SINGLE-MODEL** (one student — kept but flagged).

Each student agent is forced to emit structured output (a tool/function call with the journal schema) so we never parse free-text JSON — the same reliability lesson `lesson_review.py` already banked.

## 5. Outputs

- **`SIM_STUDENT_EVAL_G9.md`** — the human-readable report, findings ranked most-severe-first, organized by the four questions:
  1. *Makes sense* — per-lesson verdict + the specific confusion points (with lesson + step).
  2. *Redundancies* — corroborated list, each with the two lessons involved and which student(s) flagged it.
  3. *Composition readiness* — for each composition probe, the skills that were / weren't in place, traced to lessons.
  4. *Test readiness* — items the student couldn't attempt and the missing-skill trace.
- **`journal_<persona>_<model>.jsonl`** (×2) — the external memory, one line per lesson.
- **`transcripts_<persona>_<model>.jsonl`** (×2) — full raw student utterances (the evidence every finding cites).

## 6. Honesty guardrails (non-negotiable, from project memory)

- **No writing scores.** Per the locked decision, writing is never rubric-scored. Findings are lived experience + deterministic MCQ-match only.
- **Coverage ≠ efficacy.** Two simulated students are not field data. The report states this explicitly at the top and frames findings as *design signal to investigate*, not proof.
- **Anti-slop.** The report is written to the `anti-ai-slop` guardrail (Noel's standing rule; no em dashes in generated docs). Findings must be specific ("L23 assumes multi-paragraph coherence; it was only touched at L21 and the student's confidence was 0.4"), never generic ("could be clearer").
- **Model-specific noise is labeled, not hidden.** Single-model findings are kept and marked, so a Fable-only or GPT-only artifact can't masquerade as a curriculum defect.

## 7. Non-goals (YAGNI)

- Not wiring the platform grader or the live submit loop (explicitly out per the grading decision).
- Not building a UI — outputs are Markdown + JSONL.
- Not running G10–G12 in the first build (built grade-general, but pilot is G9).
- Not simulating the LearnWith/Platform3 player runtime — we evaluate the *content* a student reads, which `render_student_experience` already produces faithfully.
- Not persona multiplication in the pilot (one persona; list is extensible).

## 8. Key file references (verified)

- `Alpha HS Writing Course 2026-27/pipeline/lesson_review.py` — `render_student_experience(L)` (student view) + `fable_review` (Anthropic call template, `MODEL = "claude-fable-5"`, `_load_env_key`).
- `Alpha HS Writing Course 2026-27/pipeline/g9_assemble_v3_1.py` — the lesson loader glob (`Lesson_Bank_G9/lesson_g9_l*_v3_1.py` → `module.LESSON`).
- `Alpha HS Writing Course 2026-27/Lesson_Bank_G9/lesson_g9_l*_v3_1.py` — 27 lessons, filename number = sequence.
- `Alpha HS Writing Course 2026-27/model_test_g9.html` + `Item_Bank_G9/` — the G9 test surface.
- `HS Writing/.env` — `ANTHROPIC_API_KEY`, `OPEN_AI_API_KEY`.
- Prior art (do not reuse directly): `HS Writing/simulated_student_agent.py` is a **static HTML validator** (checks answer keys parse), not a student-experience simulator. This harness supersedes it for the evaluation purpose.
```
