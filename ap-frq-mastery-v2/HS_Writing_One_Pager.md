# High School Writing — Proposal One-Pager

**DRI:** Noel Pilkington · Writing | **Date:** June 2026 | **Status:** for approval

---

### The problem

Alpha has **no high-school writing curriculum** between where AlphaWrite Read caps
(grade 8) and AP. Students are dropped straight into AP courses that are truncated
textbooks plus FRQ practice questions — with the writing instruction stripped out.
They fail the FRQs not for lack of content alone, but because **the average Alpha
student entering AP has not written enough to do it.** We currently have no way to
build, or even verify, a writing floor before that point.

### The proposal

A **High School Writing course (grades 9–12)** on the existing AlphaWrite engine,
picking up exactly where grade 8 leaves off and scaling on a sliding ramp:

> **English I (G9) → English II (G10) → ACT Writing readiness → downstream AP FRQ preparation**

One seamless humanities-writing course, not subject-specific AP tracks. Each stage
is a real grade level with its own gate; a student progresses through writing
proficiency, not through a single one-shot target.

### What test does it pass?

| Stage | Gate (the verifiable outcome) |
|-------|-------------------------------|
| **English I (G9)** | **STAAR English I**–aligned writing EOC (passage-based composition) |
| **English II (G10)** | **STAAR English II**–aligned writing EOC |
| **G11+ readiness** | **ACT Writing** rubric (4 domains), timed |
| **Downstream** | Prepares students for AP FRQ writing — **not a promise of AP scores** |

STAAR English I/II are grade-9/10 writing tests Alpha does not currently
administer but reasonably should; the course maps to **both STAAR and CCSS** 9–10
standards, so it is portable across either accountability frame. **The honest,
self-evident claim:** Alpha should
not throw students into AP/college-level work until they clear a 9–10 writing
floor — and today there is neither a course that builds it nor a test that verifies
it. This proposal supplies both.

### Why we can build it efficiently

- **The design is complete, not just sketched.** The full G9–G10 **lesson map (40
  lessons), a dual STAAR + CCSS standards crosswalk, the passage spec, and verified
  assessment rubrics** are done — targets verified verbatim against the **official
  STAAR English I/II rubrics, the ACT Writing rubric, six released STAAR forms, and
  real AP FRQ failure data** (Timeback). The rubrics reward exactly the skills the
  sequence teaches. Only lesson content remains to author. *(The course is net-new —
  see "What we are building.")*
- **Reuses existing infrastructure** — the paragraph- and essay-writing
  architectures; no new engine required for the core composition lessons.
- **Clear scope boundary.** The curriculum team builds the **content and assessment
  specifications**; the dev team owns lesson delivery, the AI grader, and the tests.

### What the student actually does

Every lesson is **one piece of writing run through the AlphaWrite cycle** — Setup →
Outline → Draft → Revise → Polish → Submit — on the existing **paragraph-writing**
architecture (early, faster reps) and **essay-writing** architecture (the core).
Instruction is delivered *inside* the cycle: the **AI Tutor** teaches the move and
shows a worked example (with a deliberate false start → correction), the **Outline**
is a structured form, the **Revise/Polish checklists** are AI-validated meaning-
before-surface, and **Submit is AI-graded** against the real rubric — then the
student rewrites the single weakest part and re-scores. Reps are **passage-based**:
the student reads a source (or paired sources) at Setup and writes in response to it.

**The writing tasks built for the English I + II MVP** — and the goal each serves:

| Writing task (what the student produces) | Builds toward |
|------------------------------------------|---------------|
| **Expository / informational response-to-text** — read a passage, form a controlling idea about its content, support with explained textual evidence | STAAR English I ECR (informational) |
| **Argumentative response-to-text** — take a defensible position on a passage's issue; claim → evidence → reasoning → counterargument | STAAR English I/II ECR (argumentative) |
| **Synthesis essay** — weave a position across **paired/multiple** passages (not source-by-source) | STAAR top-band (paired passages) + AP synthesis prep |
| **Multi-perspective (ACT-style) essay** — analyze 3 given perspectives, stake and qualify your own | ACT Writing (G11+ readiness) |
| **Short constructed responses** — sentence-combining; "answer + cite text evidence" | STAAR writing SCR + reading SCR |

The line is direct: each task is scored on the **same rubric rows the target test
scores** (STAAR ECR's Organization & Development + Conventions; ACT's four
domains), and the moves drilled inside it — explaining evidence, synthesizing,
analyzing perspectives — are exactly the rows where students currently lose points.
The cycle's discrimination beats, coping models, and rescore loop are how each move
is taught to mastery rather than merely assigned.

### The skills it targets (verified writing-movable)

Reasoning that explains *how* evidence supports a claim (not restating) · selecting
and **explaining** text evidence from a source passage · synthesis across multiple
passages · analyzing and qualifying **multiple perspectives** (ACT) · controlling
structure, transitions, and a unified thesis · precise language and conventions ·
composing under time. *(Content-dependent AP rows — sourcing, complexity, outside
evidence — are explicitly out of scope: a writing course cannot teach the history.)*

### What we are NOT claiming

This is not an AP course, does not replace AP content instruction, and will not by
itself produce 4s and 5s. It builds the **writing floor** that makes AP, ACT, and
college work achievable — the step that does not exist today.

### What we are building (this is a net-new course)

There is no high-school writing course in production today — students have only the
truncated AP-textbook courses. This builds the missing course. Curriculum-team
deliverables: **(1)** a locked English I + II lesson map (STAAR content-response
framing, with passage-based reading integrated); **(2)** a **dual STAAR + CCSS**
standards crosswalk per lesson; **(3)** ~40 lessons of instructional content
(teaching, worked examples, discrimination items, checklists, prompts); **(4)** a
grade-9/10 **passage/stimulus bank** with anchored writing tasks; **(5)** the
**assessment specifications** the dev team's grader and tests are built from (STAAR
ECR 2-trait, sentence-combining SCR, ACT 4-domain). Dev team owns lesson delivery,
the AI grader, and the STAAR-aligned tests, built to our specs.

### The ask

Approval to build the **MVP: English I + English II**, gated to STAAR-aligned
writing EOCs, with the architecture extending to ACT readiness and downstream AP
FRQ preparation. Open decisions to confirm: where the diagnostic/gate lives (in-app
vs. Alpha test), and whether to invest in multimodal supports (video, outside
reading) as the course matures.

---
*Targeting verified against official STAAR (TEA) and ACT rubrics, College Board SAT
specs, and the existing A1/A2 lesson maps. SAT is not a writing target (no essay
since 2021). Full assessment: `Target_Skills_Assessment.md`.*
