# HS Writing Grading Engine -- Architecture Spec (v1)

## 1. Current State

### What exists

**HS Writing API** (`HS Writing/api/`):
- FastAPI app, single `/grade` endpoint
- A1 rubrics only (20 lessons, ~30 rubric definitions in `grading_rubrics.py`)
- Criteria-based scoring: each criterion is met/not-met, weighted
- Single Claude call per submission (no consensus)
- Returns: criteria results, overall feedback, next step
- Feedback principles: wise feedback, specific quotes, no cheerleading, one next step, brief model

**Writing Test Grader** (`Writing_Test_Grader/`):
- Grades G3-G8 standardized tests (Edulastic PDFs)
- 3-run consensus engine (unanimous/majority/judge)
- Ideas + Conventions scoring model
- FastAPI + SQLite + background worker
- Robust JSON parsing, score clamping, retry logic

### What's missing

1. **Rubrics for A2, B1L, B2** (~62 lessons with gradable tasks)
2. **AP rubric scoring** (Row A 0-1, Row B 0-4, Row C 0-1) for B1L and B2
3. **Consensus** on the HS Writing API (currently single-call)
4. **Response type diversity** -- the existing system handles one type (criteria met/not-met); HS Writing needs multiple scoring models
5. **Passage context** -- many tasks require the grader to see the source passage to evaluate the response
6. **Gateway/gate decisions** -- pass/fail logic based on scores

---

## 2. Scoring Models

The 82 lessons produce 6 distinct types of gradable responses. Each needs its own scoring model.

### Model A: Criteria Checklist (existing)
**Used by:** A1 L01-L19 (all non-gate tasks)
**Scoring:** Each criterion is met (1) or not met (0), with weights. Total = weighted sum.
**Output:** `{ criteria_results: [{id, met, feedback}], criteria_met, criteria_total, overall_feedback, next_step }`
**Already implemented.** Extend to A2 non-AP tasks.

### Model B: AP Rubric (Row A / Row B / Row C)
**Used by:** B1L L07, L11, L16 (gateways); B1L L19-L20 (gate); B2 L08-L10 (speed runs); B2 L11-L12 (plan-to-essay); B2 L21-L22 (gate)
**Scoring:**
- Row A (Thesis): 0 or 1
- Row B (Evidence & Commentary): 0, 1, 2, 3, or 4
- Row C (Sophistication): 0 or 1
- Total: 0-6

**Row A criteria** (all FRQ types):
- 0: No thesis, or thesis restates prompt, or thesis is not defensible
- 1: Defensible thesis that establishes a line of reasoning

**Row B criteria** (varies by FRQ type):

| Score | Rhetorical Analysis | Argument | Synthesis |
|---|---|---|---|
| 0 | No evidence or irrelevant | No evidence | Fewer than 2 sources |
| 1 | Evidence without commentary | Evidence without commentary | Evidence from sources without commentary |
| 2 | Evidence + feature-spotting (names devices without explaining function) | Evidence + explanation but generic | Evidence + explanation but superficial |
| 3 | Evidence + S-F-E analysis (explains function and effect) | Specific evidence + commentary explaining significance | Evidence from 3+ sources + analysis of how sources support argument |
| 4 | Evidence + S-F-E analysis + consistent line of reasoning | Specific evidence + commentary + consistent line of reasoning | Evidence from 3+ sources + sustained analysis + line of reasoning |

**Row C criteria** (all FRQ types -- must demonstrate ONE):
- Broader context (historical, cultural, literary)
- Alternative interpretation acknowledged and addressed
- Tension/complexity explored without false resolution
- Consistently vivid and persuasive prose style

**Output:**
```json
{
  "row_a": { "score": 0|1, "reasoning": "..." },
  "row_b": { "score": 0-4, "reasoning": "..." },
  "row_c": { "score": 0|1, "sophistication_type": null|"broader_context"|"alternative"|"tension"|"style", "reasoning": "..." },
  "total": 0-6,
  "frq_type": "rhetorical_analysis"|"argument"|"synthesis",
  "feedback": "...",
  "weakest_row": "A"|"B"|"C",
  "next_step": "..."
}
```

### Model C: Hybrid (Criteria + AP Preview)
**Used by:** A2 (most tasks), B1L L01-L06, L08-L10, L12-L18
**Scoring:** Criteria checklist (Model A) for specific lesson objectives, PLUS an AP rubric preview score for essay-length responses. The criteria score drives the lesson feedback; the AP preview score tracks trajectory.
**Output:** Model A output + optional `ap_preview: { row_a, row_b, row_c, total }` for essay-length tasks.

### Model D: Discrimination Scoring
**Used by:** Sort exercises, calibration tasks (e.g., A1 L09 analysis-vs-summary sort, B1L L04 feature-spotting sort, B2 L14 expert calibration)
**Scoring:** Compare student's classifications/scores to the answer key. Accuracy percentage.
**Output:**
```json
{
  "items": [{ "item_id": "...", "student_answer": "...", "correct_answer": "...", "correct": true|false }],
  "accuracy": 0.0-1.0,
  "feedback": "..."
}
```
**Note:** Some of these are already handled client-side by `lesson-engine.js`. Only include server-side grading for items that require LLM judgment (e.g., "Is this student's thesis scoring accurate?").

### Model E: Planning/Outline Scoring
**Used by:** A1 L12-L13 (outlines), B1L L15 (synthesis planning), B2 L07 (sophistication planning), B2 L11-L12 (plan-to-essay bridge)
**Scoring:** Criteria checklist focused on plan completeness, evidence selection, structural logic.
**Output:** Same as Model A, but with planning-specific criteria.

### Model F: Revision Scoring
**Used by:** A1 L16 (three-pass revision), B1L L18 (weakest row revision), B2 L16-L17 (surface vs. substantive, multi-pass)
**Scoring:** Requires seeing BOTH the original and revised text. Evaluates: what changed, whether changes are substantive, whether the revision improved the target dimension.
**Output:**
```json
{
  "original_assessment": "...",
  "revision_assessment": "...",
  "changes_identified": ["..."],
  "substantive": true|false,
  "improvement_score": 0-3,
  "feedback": "...",
  "next_step": "..."
}
```

---

## 3. Architecture

### 3.1 Unified API

Merge the HS Writing API into a single service that handles all 4 courses.

```
POST /grade
  body: { course, lesson, task_id, student_text, context? }
  returns: GradeResponse (model-specific)

POST /grade/ap
  body: { frq_type, student_text, passage?, prompt? }
  returns: APGradeResponse (Row A/B/C)

POST /grade/revision
  body: { course, lesson, task_id, original_text, revised_text }
  returns: RevisionGradeResponse

GET /rubrics
GET /rubrics/{course}
GET /rubrics/{course}/{lesson}
```

### 3.2 Rubric Registry

Extend `grading_rubrics.py` pattern to all 4 courses. Each rubric entry specifies:

```python
{
    "id": "B1L_L07_gateway_essay",
    "course": "B1L",
    "lesson": "L07",
    "task_type": "rhetorical_analysis_essay",
    "scoring_model": "ap_rubric",          # A | B | C | D | E | F
    "frq_type": "rhetorical_analysis",     # for Model B only
    "gateway": True,
    "gateway_threshold": {"row_a": 1, "row_b": 2},
    "description": "Full rhetorical analysis essay on Frances Harper",
    "passage_id": "SP-024",                # optional: passage context needed
    "criteria": [...],                      # for Models A/C/E
    "common_pitfalls": [...],
    "min_words": 250,
}
```

### 3.3 Scoring Pipeline

```
Request → Validate → Load Rubric → Route to Scoring Model → [Consensus?] → Format Response
```

**Consensus:** Apply the 3-run consensus from the Writing Test Grader engine for:
- All AP rubric scoring (Model B) -- Row scores can vary between graders
- All gateway/gate assessments -- high-stakes decisions need reliability
- All full essay grading (Model A essays with >= 250 min_words)

**Single-call:** Use single Claude call for:
- Short responses (paragraphs, thesis statements, outlines)
- Discrimination scoring (answer-key comparison)
- Low-stakes practice tasks

### 3.4 Passage Context

Many tasks require the grader to see the source passage. Options:

1. **Client sends passage** -- lesson HTML includes passage text, JS sends it with the grade request
2. **Server stores passages** -- passage bank indexed by ID (SP-001, SYN-07, etc.)
3. **Hybrid** -- server has passage bank, client can override

**Recommendation:** Option 3. Build a passage bank from `Passage_Bank.md` and the synthesis source sets. Client sends `passage_id` or raw `passage_text`.

### 3.5 Feedback Principles

All scoring models share the same feedback principles (from `grading_prompts.py`):

1. **Specific, not vague** -- quote student's words
2. **Criterion-by-criterion** -- evaluate each dimension independently
3. **Wise feedback tone** -- high standards + belief in capability
4. **No cheerleading** -- only praise what genuinely meets criteria
5. **One next step** -- single most impactful revision
6. **Brief model** -- 1-sentence example of what revision could look like
7. **Grade-appropriate language** -- A1: Grade 9; A2: Grade 10; B1L/B2: Grade 11-12

**AP-specific feedback additions** (Models B and C):
- Name the specific Row that needs improvement
- Distinguish feature-spotting from analysis (Row B)
- Identify whether sophistication attempt is organic or tacked-on (Row C)
- Reference specific rubric language ("Row B 3 requires S-F-E analysis, not just naming devices")

---

## 4. Prompt Templates

### 4.1 AP Rubric Prompt (Model B)

```
SYSTEM: You are an AP English Language exam reader scoring a student essay.
Score on the official AP rubric (Rows A, B, C). Be calibrated: a Row B 3
requires genuine S-F-E analysis, not just naming devices with evidence.

USER:
FRQ TYPE: {rhetorical_analysis | argument | synthesis}
PASSAGE: {passage_text or "N/A for argument"}
PROMPT: {the writing prompt}
STUDENT ESSAY:
---
{student_text}
---

Score this essay on the AP rubric. Respond in JSON:
{
  "row_a": { "score": 0|1, "reasoning": "..." },
  "row_b": { "score": 0-4, "reasoning": "..." },
  "row_c": { "score": 0|1, "sophistication_type": null|"broader_context"|"alternative"|"tension"|"style", "reasoning": "..." },
  "total": <sum>,
  "feedback": "<2-3 sentences: name the weakest row and one specific revision>",
  "weakest_row": "A"|"B"|"C",
  "next_step": "<1 actionable revision instruction>"
}
```

### 4.2 Criteria Prompt (Model A -- existing, extended)

Already implemented in `grading_prompts.py`. Extend the SYSTEM_PROMPT to be course-aware (adjust grade level and analytical expectations).

### 4.3 Revision Prompt (Model F)

```
SYSTEM: You are evaluating a student's revision of their own writing.
Focus on whether the changes are SUBSTANTIVE (transforming ideas,
deepening analysis) or SURFACE (fixing grammar, changing words).

USER:
REVISION TARGET: {what the student was asked to improve}
ORIGINAL:
---
{original_text}
---
REVISED:
---
{revised_text}
---

Evaluate the revision. Respond in JSON:
{
  "changes_identified": ["..."],
  "substantive": true|false,
  "improvement_score": 0-3,
  "feedback": "...",
  "next_step": "..."
}
```

---

## 5. Rubric Coverage Plan

### Priority 1: Gateway and Gate assessments (high-stakes, need consensus)

| Course | Lesson | Task | Scoring Model | Consensus |
|---|---|---|---|---|
| A1 | L20 | Gate essay | A (criteria) | Yes (3-run) |
| A2 | L07 | Argument essay gateway | A (criteria) | Yes |
| A2 | L12 | Synthesis essay gateway | A (criteria) | Yes |
| A2 | L20 | Gate (synthesis + ACT) | A (criteria) | Yes |
| B1L | L07 | Rhetorical analysis gateway | B (AP rubric) | Yes |
| B1L | L11 | Argument gateway | B (AP rubric) | Yes |
| B1L | L16 | Synthesis gateway | B (AP rubric) | Yes |
| B1L | L19-L20 | Gate (3 FRQs) | B (AP rubric) | Yes |
| B2 | L21-L22 | Gate (3 FRQs) | B (AP rubric) | Yes |

### Priority 2: Full essay tasks (non-gateway)

| Course | Lessons | Tasks | Scoring Model |
|---|---|---|---|
| A1 | L05, L18 | Argument essay, practice essay | A (criteria) |
| A2 | L06, L18-L19 | Full essays | A/C (hybrid) |
| B1L | L12 | Sophistication moves | C (hybrid) |
| B2 | L08-L10 | Speed runs (3 full essays) | B (AP rubric) |
| B2 | L11-L12 | Plan-to-essay bridges | B (AP rubric) |
| B2 | L13 | Recovery drill | B (AP rubric) |

### Priority 3: Paragraph and short-form tasks

| Course | Lessons | Tasks | Scoring Model |
|---|---|---|---|
| A1 | L01-L04, L06-L10, L14 | Paragraphs, drills, S-F-E | A (criteria) |
| A2 | L01-L05, L08-L11 | Paragraphs, synthesis drills | A (criteria) |
| B1L | L01-L06, L08-L10, L13-L15 | Drills, paragraphs, planning | A/E (criteria/planning) |
| B2 | L01-L07, L14-L20 | Sophistication drills, voice, revision | A/E/F |

### Priority 4: Discrimination/calibration tasks

These are partially handled client-side by `lesson-engine.js`. Server-side grading only for:
- Calibration accuracy (student scores sample essays → compare to official)
- Open-ended discrimination (e.g., "Is this feature-spotting or analysis?" with explanation)

---

## 6. Implementation Sequence

### Phase 1: Unify and extend existing infrastructure
1. Port consensus engine from Writing_Test_Grader into HS Writing API
2. Add AP rubric scoring model (Model B) with prompt template
3. Add passage bank (indexed by ID)
4. Write B1L/B2 gateway rubrics (Priority 1 — 9 assessments)

### Phase 2: Full essay coverage
5. Write A2 rubrics for all gradable tasks
6. Write B1L non-gateway rubrics
7. Write B2 rubrics (speed runs, plan-to-essay, voice)
8. Add revision scoring model (Model F)

### Phase 3: Short-form and calibration
9. Extend A1 rubrics to remaining uncovered tasks
10. Add calibration scoring for B1L L17, B2 L14
11. Wire lesson HTML to call grading API (add JS integration to lesson-engine.js)

### Phase 4: Production hardening
12. Add rate limiting and API key auth
13. Add SQLite result storage (port from Writing_Test_Grader)
14. Add batch grading endpoint
15. Add scoring analytics (track student progress across lessons)

---

## 7. Integration with Lesson HTML

The lesson HTML files need a JS integration layer to:
1. Capture student text from textareas
2. POST to the grading API with the correct rubric_id
3. Display structured feedback inline (criteria results, overall feedback, next step)
4. For AP rubric: display Row A/B/C scores visually
5. For gateways: display pass/fail determination

This lives in `lesson-engine.js` as a new module (e.g., `gradeSubmission(rubricId, studentText)`).

The API URL should be configurable (localhost for dev, deployed URL for production).

---

## 8. Cost Estimates

| Scoring Type | Tokens/call | Calls/submission | Cost (Sonnet) |
|---|---|---|---|
| Short criteria (paragraph) | ~2K in + ~500 out | 1 | ~$0.01 |
| Full essay criteria | ~4K in + ~1K out | 1 | ~$0.02 |
| AP rubric (single) | ~5K in + ~1K out | 1 | ~$0.02 |
| AP rubric (3-run consensus) | ~5K in + ~1K out | 3-4 | ~$0.08 |
| Revision scoring | ~6K in + ~1K out | 1 | ~$0.03 |

**Per-student full course cost estimate:**
- A1 (20 lessons, ~30 gradable tasks): ~$0.50
- A2 (20 lessons, ~25 gradable tasks): ~$0.50
- B1L (20 lessons, ~25 gradable tasks + 3 FRQ gate): ~$0.75
- B2 (22 lessons, ~20 gradable tasks + 3 FRQ gate): ~$0.75
- **Full program (A1+A2+B1L+B2): ~$2.50/student**

---

*Architecture Spec v1 -- March 2026*
