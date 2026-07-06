# Council of Writing Instruction — Design Spec

**Date:** 2026-07-06
**Status:** Approved (brainstorming), pending spec review
**Type:** New Claude Code skill
**Depends on:** `Instructional_Design_KB/` (built 2026-07-06); on-disk primary-source PDFs

---

## 1. Purpose

A skill that convenes a "council" of grounded expert personas — the notable
writing-instruction and general-instruction pedagogues — plus a synthesis judge,
to either **design** a new writing lesson or **review** a draft one. It is the
interactive, generative front-end to the `Instructional_Design_KB/` reference
document.

The value is NOT "ask an AI for teaching advice." It is **structured
disagreement between characteristically distinct, source-grounded experts, then
principled adjudication** — surfacing the tensions (Engelmann's tight scripting
vs. Elbow's openness; TWR's sentence-level build vs. 4C/ID whole-task) that a
single voice would flatten, and resolving them by evidence and lesson goal.

### Success criteria
1. On a real lesson, the convened personas **genuinely diverge** — each says
   something the others would not, and each names at least one disagreement with
   another named seat. (If they all agree, the skill failed.)
2. The judge **adjudicates, not averages** — conflicts are resolved with a stated
   rule, and the losing position is named, not silently dropped.
3. Every persona claim is **source-tagged** and auditable back to a book or KB
   entry (honors the house provenance rule).
4. Both modes produce a **concrete artifact**: `design` → a lesson draft;
   `review` → a prioritized, deduplicated revision list with each item traced to
   the expert(s) who raised it.
5. Cost is controlled: the smart-panel convening keeps a typical run to 4–6
   seats, not 10.

### Non-goals (YAGNI)
- Not a general chatbot / not a replacement for the KB reference doc.
- Not a lesson *renderer* — it produces lesson content/critique; `craft-lesson`
  (or the render pipeline) turns a design into final HTML.
- No live web calls at runtime — grounding is pre-extracted into persona briefs.
- Not a grader — it critiques lesson *design*, not student work.

---

## 2. Modes

One skill, two modes (single roster + judge shared; modes differ only at entry
and exit).

### `design <topic | skill | outline>`
- **Input:** a lesson topic, a target skill/KC, or a canonical outline.
- **Flow:** convene → each persona proposes lesson moves for that target →
  judge synthesizes ONE coherent lesson draft.
- **Output:** a lesson draft (structured: objective, named strategy, model,
  practice/fade, assessment) ready to hand to `craft-lesson` for rendering.

### `review <draft-file>`
- **Input:** path to a draft lesson (md or html).
- **Flow:** convene → each persona critiques the draft through its lens →
  judge produces a prioritized, deduplicated revision list.
- **Output:** revision list, each item = {priority, issue, which expert(s)
  raised it, the fix, source anchor}.

### Invocation
```
/council-of-writing-instruction design "G9 U1 L2: taking a position"
/council-of-writing-instruction review Course review/L1_activity_corrected.html
```
Optional overrides (safety valves on the smart panel):
- `--seats TWR,Engelmann,Wiliam-Hattie` — convene exactly these seats.
- `--all` — convene all 10.

Mode is the first token; if omitted and the arg is a readable file path, default
to `review`; otherwise `design`.

---

## 3. The Roster (10 seats + 1 judge)

| # | Seat | Layer | Grounding source | Grounding tier |
|---|---|---|---|---|
| 1 | Hochman & Wexler (TWR) | Writing pedagogy | *The Writing Revolution 2.0* (on disk) | book |
| 2 | Graham & Harris (SRSD) | Writing pedagogy | Writing Next + KB 2.5 | book+KB |
| 3 | Graff & Birkenstein (TSIS) | Writing pedagogy | *They Say / I Say* (on disk) | book |
| 4 | Engelmann (DI) | Instruction/structure | *Theory of Instruction* (on disk) | book |
| 5 | Kirschner & Hendrick | Learning science | *How Learning/Teaching Happens* (on disk) + KB L1 | book+KB |
| 6 | Yeager | Motivation | *10 to 25* (on disk) | book |
| 7 | Wiliam & Hattie | Assessment/feedback | KB 4.1–4.2 (Hattie 2007; Black & Wiliam 1998) | KB |
| 8 | Wiggins & McTighe (UbD) | Backward design | KB 3.1 (UbD white paper) | KB |
| 9 | Hayes & Flower | Cognitive process of writing | Targeted research pass (not on disk) | research |
| 10 | Elbow / Gallagher | Authentic-voice counterweight | Targeted research pass (low-evidence, by design) | research |
| — | **Synthesis Judge** | Adjudication | KB cross-layer synthesis | KB |

Notes:
- Seats 7–8 are the assessment/structure gaps the current KB fills but the
  original 7-seat idea lacked.
- Seat 10 is a **deliberate dissenter** — its authority is low (flagged as such
  in its brief) but its job is to guard against the "formula factory" risk the KB
  itself raised (mastery standards squeezing out voice). The judge weights it as
  dissent, not evidence.

---

## 4. Grounding Model (hybrid — "option 3")

Each persona reasons at runtime from a **pre-built brief**, not from re-reading a
book each run. The brief is built ONCE (build-time extraction pass) and every
runtime claim carries a source tag pointing back into it.

### Build-time: the extraction pass
- **Seats 1–6:** extract core principles from the actual on-disk PDFs, with
  page/section anchors. Lean on the PDFs + the existing
  `Learning Science Synthesis for Writing Brainlift.md`.
- **Seats 7–8:** ground to the KB entries (already cited to primary sources).
- **Seats 9–10:** short targeted research fetch to build the brief (Hayes/Flower
  cognitive-process model; Elbow/Gallagher voice/low-stakes writing).

### Persona brief structure (fixed template — every seat identical shape)
```markdown
# <Seat name> — <Layer>
## Core commitments        (3–6 bullets: what this expert fundamentally believes)
## Characteristic moves    (concrete lesson-design moves they advocate)
## Pushes AGAINST           (what they'd object to — the source of disagreement)
## Evidence grade           (A/B/C from KB, or "dissent/low-evidence")
## Source anchors           (book+page / KB section for each core claim)
## The "tell"               (one line — how this persona sounds, to stay in character)
```
The `Pushes AGAINST` and `The tell` fields are what force genuine divergence
rather than 10 flavors of generic advice.

---

## 5. Runtime Flow (how we avoid mush)

```
1. CONVENE
   Judge reads the topic/draft. Picks the 4–6 seats with genuine stake.
   Emits: convened seats + benched seats + one-line reason for the bench.
   (Overridden by --seats / --all if provided.)

2. DELIBERATE  (parallel subagents, one per convened seat)
   Each persona produces STRUCTURED output:
     - its take on the lesson (design: proposed moves | review: critique)
     - explicit source anchor(s) for each claim
     - >=1 named disagreement with another specific seat
   Parallel because the seats are independent at this stage.

3. ADJUDICATE  (judge — single agent, sees all deliberations)
   Judge does NOT average. For each conflict:
     - state the tension (Seat A wants X, Seat B wants Y)
     - resolve with the tie-break rule (see 5.1)
     - name the losing position; do not silently drop it
   Judge composes the mode artifact.

4. EMIT
   design  -> one coherent lesson draft (+ "dissents noted" footer)
   review  -> prioritized dedup'd revision list, each item traced to expert(s)
```

### 5.1 Judge tie-break rule (stated, not vibes)
1. **Evidence grade first** — higher KB grade (A > B > C) wins a direct conflict.
2. **Lesson goal second** — if grades tie, the position better serving the
   stated lesson objective / target skill wins.
3. **Novice-support asymmetry third** — if still tied, prefer more support for
   novices (expertise-reversal asymmetry from KB L1.2).
4. Elbow/Gallagher (seat 10) is **dissent**, never an evidence winner; its points
   surface as "voice/authenticity risks to weigh," not as rulings.

### 5.2 Persona voice discipline
Characterful but disciplined: personas *sound* distinct (the "tell") and name
disagreements, but every substantive claim is source-tagged. No theatrical
fabrication, no invented statistics — same no-slop rule as the rest of the
courses.

---

## 6. File Layout

```
.claude/skills/council-of-writing-instruction/
  SKILL.md                          # frontmatter + orchestration (convene→deliberate→adjudicate→emit)
  personas/
    01-twr-hochman-wexler.md
    02-srsd-graham-harris.md
    03-tsis-graff-birkenstein.md
    04-di-engelmann.md
    05-kirschner-hendrick.md
    06-yeager.md
    07-wiliam-hattie.md
    08-ubd-wiggins-mctighe.md
    09-hayes-flower.md
    10-elbow-gallagher.md
    judge.md
  references/
    roster.md                       # seat -> layer -> source -> "when to convene" cues
    output-templates.md             # design-draft template + review-list template
```

Skill lives in `.claude/skills/` (user scope, matches existing `writing-card-*`
skills). Frontmatter follows the existing convention: `name`, `version`,
`description`, `triggers`, `allowed-tools`.

---

## 7. Build Plan (what it takes to pull off)

1. **Extraction pass** (the real work): build 10 persona briefs + judge brief.
   - Seats 1–6 from on-disk PDFs (parallel subagents, one per book).
   - Seats 7–8 from KB.
   - Seats 9–10 from ~2 short research fetches.
2. **roster.md + output-templates.md** — the convening cues and artifact shapes.
3. **SKILL.md orchestration** — the 4-step runtime flow + `--seats`/`--all`
   overrides + mode detection.
4. **Test on one real lesson** (both modes) — e.g. current L1A or
   `L1_activity_corrected.html`:
   - Divergence check: do convened personas actually disagree? (fail if uniform)
   - Adjudication check: does the judge name losing positions + apply the
     tie-break rule?
   - Provenance check: does every persona claim carry a source tag?

---

## 8. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| 10 personas → 10 flavors of generic advice | `Pushes AGAINST` + forced named-disagreement in every deliberation; smart-panel convening; divergence test as acceptance gate |
| Judge averages instead of adjudicating | Explicit stated tie-break rule (5.1); requirement to name the losing position |
| Token cost of a full council | Smart panel (4–6 seats default), not all 10 |
| Provenance drift / fabrication | Hybrid grounding; every claim source-tagged; briefs auditable to book/KB |
| Seats 9–10 weakly grounded | Explicitly graded low-evidence in their briefs; Elbow/Gallagher fenced as dissent-only in the tie-break rule |
| Skill duplicates the KB | Skill is the generative front-end; KB stays the reference. Personas cite INTO the KB, don't restate it. |

---

## 9. Open sub-decisions (defaulted, override at spec review)
- Judge tie-break rule = evidence grade → lesson goal → novice-support asymmetry
  (§5.1). **Default accepted.**
- Persona voice = characterful-but-source-tagged (§5.2). **Default accepted.**
- Skill scope = user (`.claude/skills/`), matching existing writing skills.
