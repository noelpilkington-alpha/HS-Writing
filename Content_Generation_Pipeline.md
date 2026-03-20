# HS Writing Course: Content Generation Pipeline

## Following the Ilma Production Methodology | 3 Claude Models | QTI Output

---

# I. PIPELINE OVERVIEW

## The 6 Stages

```
Stage 1: Curriculum Spec .............. DONE (HS_Writing_Course_Blueprint.md)
Stage 2: Content Generation .......... THIS DOCUMENT
Stage 3: Build Comparison ............. Rubric scoring + 3 evaluators
Stage 4: QC & Fix Pipeline ........... Binary checks + fix loops
Stage 5: Item Tournament .............. 3 models compete per slot
Stage 6: Timeback Push ................ QTI API + OneRoster API
```

## Content Inventory

Before building anything, here's exactly what we need to produce:

| Phase | Course | Stimuli (Instruction) | Discrimination Items | Production Items | Gate Items | Total Items |
|---|---|---|---|---|---|---|
| Phase 1 (G9) | A1 | 4 articles | ~40 items | ~25 prompts | 1 essay + 15 conventions | ~82 |
| Phase 2 (G10) | A2 | 3 articles | ~35 items | ~20 prompts | 1 synthesis + 1 ACT essay + 22 conventions | ~82 |
| Phase 2-ACT (G10) | A2 | 1 article | ~11 items | ~17 prompts | (included in Phase 2 gate) | ~29 |
| Phase 3L (AP Lang) | B1 | 3 articles | ~25 items | ~20 prompts | 3 essays | ~51 |
| Phase 3T (AP Lit) | B1 | 3 articles | ~25 items | ~20 prompts | 3 essays | ~51 |
| Phase 4 (G12) | B2 | 4 articles | ~20 items | ~15 prompts | 3 essays | ~42 |
| SAT/ACT Grammar | A1-A2 | 1 article | ~60 items | 2 passages | -- | ~63 |
| **Totals** | | **19 articles** | **~216 items** | **~119 prompts** | **~12 essays + 37 conv.** | **~400** |

Plus: ~15 AP-level passages (stimuli) for Phase 3-4 analysis exercises.

### Phase 2-ACT Content Breakdown (NEW)

The ACT Writing content in Course A2 adds:
- 1 instruction stimulus: ACT Writing format + perspective analysis
- 3 Perspective Decomposition items (production)
- 3 Strength/Limitation Analysis items (production)
- 5 Perspective Relationship Mapping items (discrimination)
- 3 Position Development drills (production)
- 3 Constructed Support drills (production)
- 2 Engaging the Opposition items (production)
- 3 ACT Planning Sprint items (timed production)
- 2 Full ACT essays (timed production)
- 3 ACT Rubric Calibration items (discrimination)
- 3 ACT-style prompts with perspectives (stimuli)

---

# II. CONTENT TYPES AND QTI MAPPING

## Type 1: Instruction Stimuli

**What:** 3-5 minute instructional articles that teach one analytical move, including a coping model.

**QTI Format:** `<qti-assessment-stimulus>` with HTML body.

**Structure:**
```
1. Hook (1-2 sentences): Why this move matters
2. The Move (2-3 sentences): Concise rule/principle
3. Coping Model (1 worked example):
   - First attempt (with visible false start or weakness)
   - Self-correction thinking ("Wait, I'm just summarizing...")
   - Revised attempt (strong version)
4. Quick Check: Force-correct question embedded as stimulus text
   (The actual check is a separate QTI item linked to this stimulus)
```

**Count:** 18 articles across all phases.

## Type 2: Discrimination Items

**What:** Items where students identify, classify, or evaluate — seeing quality before producing it.

**QTI Formats:**
- `choiceInteraction` (multiple choice) — for sort/classify tasks
- `matchInteraction` — for matching (e.g., structure to purpose)
- `hottextInteraction` — for identifying elements within a passage
- `orderInteraction` — for sequencing (e.g., ordering argument steps)
- `inlineChoiceInteraction` — for passage-based editing (SAT-style)

**Structure per item:**
```
- Stimulus: passage excerpt, essay excerpt, or analytical sentence(s)
- Stem: clear question targeting the discrimination skill
- Options: 4-5 choices (for choice), or matched pairs
- Correct answer + rationale
- Distractor rationale (why each wrong answer is wrong)
```

**Count:** ~205 items across all phases.

## Type 3: Production Items (Extended-Text)

**What:** Items where students write — plans, paragraphs, or full essays.

**QTI Format:** `<extendedTextInteraction>` with optional time limit.

**Sub-types:**

| Sub-type | Time | What Student Produces | Scoring |
|---|---|---|---|
| Essay Plan | 5-10 min | Thesis + outline + evidence notes | Checklist rubric |
| Paragraph Sprint | 7 min | One analytical body paragraph | Mini-rubric (claim, evidence, analysis, connection) |
| Full Essay | 35-55 min | Complete analytical essay | AP-aligned rubric (Rows A, B, C) |
| Revision Exercise | 10 min | Revised version of weak text | Before/after comparison rubric |

**Structure per item:**
```
- Stimulus: passage + prompt (for essays/paragraphs)
         OR weak text + revision instructions (for revision exercises)
         OR planning template (for plans)
- Prompt: clear task with time limit stated
- Rubric: scoring criteria appropriate to sub-type
- Exemplar response: one sample at "meets expectations" level
```

**Count:** ~100 prompts across all phases.

## Type 4: Passage Stimuli

**What:** Literary and nonfiction passages used as source material for analysis exercises.

**QTI Format:** `<qti-assessment-stimulus>` with passage text.

**Requirements:**
- Public domain or original (no copyright issues)
- 400-1000 words for nonfiction; 200-600 words for poetry
- Rich enough to support multiple analytical angles
- Phase-appropriate complexity (Lexile 1100-1400 for G9-10; AP-level for G11-12)

**Count:** ~15 passages for Phase 3-4, plus excerpts embedded in Phase 1-2 items.

## Type 5: Gate Assessment Tests

**What:** Timed assessments combining essays and convention items.

**QTI Format:** `<qti-assessment-test>` containing test parts and sections.

**Structure:**
```
Test
├── Part 1: Essay Section (timed)
│   └── Item: extended-text with passage stimulus
└── Part 2: Conventions Section (timed)
    └── Items: choice/inline-choice/hottext (15-22 items)
```

**Count:** 4 gate tests + optional retake variants.

---

# III. GENERATION AGENTS

Each agent is a structured prompt sent to the Claude API. Three models generate competing versions:
- **Claude Opus 4.6** — highest quality, best for complex content
- **Claude Sonnet 4.6** — strong quality, faster
- **Claude Haiku 4.5** — fastest, good for simpler items

## Agent Architecture

```
                    ┌──────────────────┐
                    │  Blueprint Spec   │
                    │  (this course)    │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  Content Router   │
                    │  (assigns work)   │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼───┐  ┌──────▼─────┐  ┌────▼────────┐
     │ Stimulus   │  │ Item       │  │ Passage     │
     │ Agent      │  │ Agent      │  │ Agent       │
     └────────────┘  └────────────┘  └─────────────┘
              │              │              │
              │    ┌─────────┼──────────┐   │
              │    │         │          │   │
              ▼    ▼         ▼          ▼   ▼
           ┌─────────────────────────────────┐
           │       QTI Assembly Agent        │
           │   (wraps content in valid QTI)  │
           └─────────────────────────────────┘
```

---

## Agent 1: Stimulus Generation Agent

### System Prompt

```
You are an expert instructional designer creating brief, high-impact writing
instruction for high school students. You follow the Writing Brainlift
principles and SRSD methodology.

Your output is a single instructional article (3-5 minute read) that:
1. Teaches ONE analytical writing move
2. Includes ONE coping model (false start → self-correction → strong version)
3. Uses direct, respectful tone (mentor mindset)
4. Never exceeds 600 words
5. Ends with a brief "Check yourself" prompt (not a full question — that's a separate item)

CRITICAL RULES:
- Coping models MUST include a visible struggle. Never show only the perfect version.
- Instruction must be concise. If you can say it in 2 sentences, don't use 4.
- Use concrete examples from analytical writing, not abstract explanations.
- All examples must involve analytical/argumentative prose (not creative writing).
- Use shared vocabulary: thesis, line of reasoning, evidence, commentary,
  sophistication, concision, synthesis.
```

### User Prompt Template

```
Create an instructional stimulus for the following:

PHASE: {phase_number} ({phase_name})
KC: {kc_code} — {kc_name}
SKILL TYPE: {skill_type} (Discrimination / Production / Integration)
LESSON CONTEXT: {lesson_context}
PREREQUISITES: Students have already mastered {prerequisites}
GRADE LEVEL: {grade_level}
CALIBRATION: {calibration_standard}

The article should teach students how to {specific_skill_description}.

Include a coping model where the writer:
- First attempt: {common_mistake_pattern}
- Self-correction: realizes the problem and names it
- Revised attempt: demonstrates the correct move

Format as HTML suitable for a QTI stimulus body.
```

### Output Format

```html
<div class="instruction-stimulus">
  <h2>[Title: The Move Name]</h2>

  <div class="hook">
    <p>[1-2 sentence hook]</p>
  </div>

  <div class="the-move">
    <h3>The Move</h3>
    <p>[Concise instruction]</p>
  </div>

  <div class="coping-model">
    <h3>Watch This</h3>
    <div class="attempt-1">
      <p class="label">First try:</p>
      <blockquote>[Weak attempt]</blockquote>
    </div>
    <div class="self-correction">
      <p class="thinking">[Self-correction thinking]</p>
    </div>
    <div class="attempt-2">
      <p class="label">Revised:</p>
      <blockquote>[Strong version]</blockquote>
    </div>
  </div>

  <div class="check-yourself">
    <p><strong>Check yourself:</strong> [Brief self-check prompt]</p>
  </div>
</div>
```

---

## Agent 2: Discrimination Item Agent

### System Prompt

```
You are an expert assessment designer creating discrimination items for a high
school analytical writing course. These items test whether students can SEE
quality differences before they PRODUCE quality writing.

Your items follow these principles:
- Discrimination before production (Writing Brainlift SPOV)
- 5 items per set (minimum effective dose)
- Force-correct mechanism: wrong answers get feedback + retry
- All distractors are plausible and represent common student errors
- Rationales explain WHY each option is correct or incorrect

ITEM QUALITY RULES:
- Stems must be clear and unambiguous
- Correct answer must be defensibly correct (no "best answer" ambiguity)
- Distractors must represent real student misconceptions, not obviously wrong filler
- Reading load per item: under 150 words (stem + options combined, excluding passage)
- Every item must test the specific KC, not general reading comprehension
```

### User Prompt Template

```
Create a set of {item_count} discrimination items for:

PHASE: {phase_number} ({phase_name})
KC: {kc_code} — {kc_name}
EXERCISE: {exercise_name}
EXERCISE DESCRIPTION: {exercise_description}
QTI ITEM TYPE: {qti_type} (choice / match / hottext / order / inline-choice)
PASSAGE (if applicable): {passage_or_none}
GRADE LEVEL: {grade_level}
CALIBRATION: {calibration_standard}

Each item should test whether the student can {discrimination_skill}.

For each item, provide:
1. Stimulus text (if needed beyond the shared passage)
2. Stem (the question)
3. Response options with correct answer marked
4. Rationale for correct answer
5. Rationale for each distractor (what misconception it represents)

Common student errors for this KC:
{common_errors}

Output as structured JSON (will be converted to QTI XML separately).
```

### Output Format (JSON)

```json
{
  "item_set": {
    "kc_code": "C.9.04",
    "exercise": "Thesis Triage",
    "qti_type": "choiceInteraction",
    "items": [
      {
        "id": "C.9.04-disc-001",
        "stimulus": "Read the following thesis statement from a student essay about social media's impact on teenagers.",
        "stem": "Which category best describes this thesis?",
        "prompt_text": "\"Social media has both positive and negative effects on teenagers.\"",
        "options": [
          {"id": "A", "text": "Strong — arguable and specific", "correct": false},
          {"id": "B", "text": "Weak — vague and not arguable", "correct": true},
          {"id": "C", "text": "Fixable — has a position but needs sharpening", "correct": false},
          {"id": "D", "text": "Strong — covers both sides of the issue", "correct": false}
        ],
        "correct_rationale": "This thesis merely states that something has 'both positive and negative effects' — a claim so broad it's impossible to argue against. A strong thesis takes a specific, defensible position.",
        "distractor_rationales": {
          "A": "Students who choose this may confuse 'balanced' with 'arguable.' A thesis that says 'both good and bad' doesn't commit to a position.",
          "C": "'Fixable' would apply if the thesis had a direction but was imprecise. This thesis has no direction at all.",
          "D": "'Covering both sides' is not the same as being strong. A thesis needs to ARGUE something, not just acknowledge complexity exists."
        },
        "force_correct_feedback": "This thesis is too vague to argue. Try again — look for the one that names the specific problem."
      }
    ]
  }
}
```

---

## Agent 3: Production Item Agent

### System Prompt

```
You are an expert assessment designer creating production prompts for a high
school analytical writing course. These items ask students to WRITE — plans,
paragraphs, or full essays.

Your prompts follow these principles:
- The 4:2:1 ratio: plans are most common, then paragraphs, then full essays
- Every prompt includes a clear rubric so students know what "good" looks like
- Exemplar responses demonstrate "meets expectations" (not perfection)
- Prompts specify time limits to build exam stamina
- All writing tasks are analytical/argumentative (not creative)

PROMPT QUALITY RULES:
- Task must be specific enough that two competent raters would agree on quality
- Rubric criteria must be observable (not "shows understanding" but "identifies
  at least 2 specific strategies and explains how each serves the author's purpose")
- Passage selection must allow multiple valid interpretive angles
- Exemplar must be realistic student work at the target level, not professional prose
```

### User Prompt Template

```
Create a production item for:

PHASE: {phase_number} ({phase_name})
KC: {kc_code} — {kc_name}
EXERCISE: {exercise_name}
PRODUCTION TYPE: {type} (essay_plan / paragraph_sprint / full_essay / revision)
TIME LIMIT: {time_limit}
PASSAGE: {passage_text_or_reference}
GRADE LEVEL: {grade_level}
CALIBRATION: {calibration_standard}
RUBRIC TYPE: {rubric_type} (checklist / mini-rubric / AP-aligned)

The student should {task_description}.

Sentence frames available to students (may reference but don't require):
{relevant_sentence_frames}

Provide:
1. Stimulus (passage + any setup text)
2. Prompt (the writing task)
3. Time limit
4. Scoring rubric
5. Exemplar response at "meets expectations" level
6. Common pitfalls to watch for in scoring

Output as structured JSON.
```

### Output Format (JSON)

```json
{
  "production_item": {
    "id": "C.9.07-prod-001",
    "kc_code": "C.9.07",
    "exercise": "Analytical Sentence Drill",
    "production_type": "paragraph_sprint",
    "time_limit_minutes": 7,
    "stimulus": {
      "type": "passage",
      "title": "From 'Letter from Birmingham Jail' by Martin Luther King Jr.",
      "text": "[passage excerpt, ~300 words]",
      "source": "Public domain"
    },
    "prompt": "Write ONE analytical body paragraph examining how King uses a specific rhetorical strategy in this excerpt to advance his argument. Your paragraph should include: a claim identifying the strategy, specific quoted evidence, analysis explaining HOW the strategy works on the reader, and a connection to King's larger purpose.",
    "rubric": {
      "type": "mini-rubric",
      "criteria": [
        {"name": "Claim", "points": 1, "descriptor": "Clear claim identifying a specific strategy (not just naming a device)"},
        {"name": "Evidence", "points": 1, "descriptor": "Specific, properly integrated quotation from the passage"},
        {"name": "Analysis", "points": 1, "descriptor": "Explains HOW the strategy affects the reader or serves King's purpose (not just WHAT it is)"},
        {"name": "Connection", "points": 1, "descriptor": "Links the analysis back to King's larger argument or purpose"}
      ],
      "total": 4,
      "passing": 3
    },
    "exemplar": {
      "level": "meets_expectations",
      "text": "[Sample student paragraph scoring 3/4]",
      "scoring_notes": "Earns Claim (1), Evidence (1), Analysis (1). Loses Connection — the final sentence restates the claim rather than connecting to King's larger purpose."
    },
    "common_pitfalls": [
      "Feature-spotting: 'King uses a metaphor' without explaining its effect",
      "Summary: retelling what King says instead of analyzing how he says it",
      "Missing connection: strong analysis of a moment but no link to the larger argument"
    ]
  }
}
```

---

## Agent 4: Passage Curation Agent

### System Prompt

```
You are an expert passage curator selecting and preparing texts for a high school
analytical writing course. Passages serve as source material for analysis exercises.

PASSAGE REQUIREMENTS:
- Public domain OR original composition (no copyrighted material)
- Rich enough to support 3+ valid analytical angles
- Appropriate complexity for the target grade level
- Nonfiction: 400-1000 words | Poetry: 10-40 lines | Prose fiction: 200-600 words
- Must contain identifiable rhetorical/literary strategies worth analyzing
- Must be engaging to high school students (no dry academic prose unless it's
  brilliantly argued)

FOR AP LANGUAGE PASSAGES:
- Nonfiction: speeches, essays, letters, editorials, memoir excerpts
- Must have a clear rhetorical situation (speaker, audience, purpose, context)
- Must employ identifiable rhetorical strategies

FOR AP LITERATURE PASSAGES:
- Prose fiction with rich characterization, imagery, narrative technique
- Poetry with identifiable formal choices that create meaning
- Must reward close reading (not all surface-level)

SOURCE PRIORITIES:
1. Public domain texts (pre-1928 US, or government documents)
2. Government speeches and documents
3. Original compositions written specifically for this course
4. Creative Commons licensed texts
```

### User Prompt Template

```
Select or compose a passage for:

PHASE: {phase_number}
EXERCISE: {exercise_name}
PASSAGE TYPE: {type} (nonfiction_speech / nonfiction_essay / prose_fiction / poetry)
TARGET LENGTH: {word_count} words
GRADE LEVEL: {grade_level}
ANALYTICAL FOCUS: Students will practice {analytical_skill}

The passage should:
- Allow analysis of {target_strategies}
- Be accessible to students at the {grade_level} level
- Have a clear enough rhetorical situation / literary context for productive analysis
- NOT be one of these commonly used passages: {exclusion_list}

Provide:
1. Full passage text
2. Source and copyright status
3. Rhetorical/literary situation summary
4. 3 viable analytical angles students might take
5. Key strategies/elements present in the passage

Output as structured JSON.
```

---

## Agent 5: QTI Assembly Agent

### System Prompt

```
You are a QTI 3.0 XML specialist. You convert structured JSON content into
valid QTI 3.0 XML that can be pushed to the Timeback QTI API.

You produce three types of QTI XML:
1. Assessment Items (discrimination + production items)
2. Assessment Stimuli (instruction articles + passages)
3. Assessment Tests (gate assessments assembling items into timed sections)

CRITICAL RULES:
- Output must be valid QTI 3.0 XML
- Use correct namespaces: xmlns="http://www.imsglobal.org/xsd/imsqtiasi_v3p0"
- Item identifiers must follow pattern: {kc_code}-{type}-{number}
- All items must include responseDeclaration and outcomeDeclaration
- Extended-text items must include rubric markup
- Timed items must use timeLimits element
- Stimuli must use qti-assessment-stimulus element
- Tests must use qti-assessment-test with proper testPart and assessmentSection structure
```

This agent is deterministic — it doesn't compete in the tournament. It runs after the winning content is selected and wraps it in valid QTI.

---

# IV. GENERATION WORKFLOW

## Step-by-Step Process

### Step 1: Build the Content Manifest

Parse the Blueprint to create a JSON manifest of every item needed:

```json
{
  "manifest": [
    {
      "id": "phase1-essay-arch-stim",
      "type": "stimulus",
      "phase": 1,
      "topic": "Essay Architecture",
      "kc_codes": ["C.9.01", "C.9.02", "C.9.03"],
      "agent": "stimulus",
      "description": "Instruction on essay structures beyond 5-paragraph"
    },
    {
      "id": "C.9.01-disc-set",
      "type": "discrimination_set",
      "phase": 1,
      "topic": "Essay Architecture",
      "kc_code": "C.9.01",
      "exercise": "Structure Sort",
      "item_count": 5,
      "qti_type": "choiceInteraction",
      "agent": "discrimination"
    },
    ...
  ]
}
```

### Step 2: Generate Passages First

Passages are dependencies — many items reference them. Generate all passages before items.

```
Passage Agent → 15 AP passages + embedded excerpts
                 ↓
         Review for:
         - Copyright clearance
         - Analytical richness
         - Grade-level appropriateness
         - No duplicates of commonly-used AP passages
```

### Step 3: Generate Stimuli (Instruction Articles)

Run 3 models in parallel on each stimulus slot:

```
For each stimulus in manifest:
  ├── Claude Opus 4.6   → Version A
  ├── Claude Sonnet 4.6 → Version B
  └── Claude Haiku 4.5  → Version C
```

### Step 4: Generate Discrimination Items

Run 3 models in parallel on each item set:

```
For each discrimination_set in manifest:
  ├── Claude Opus 4.6   → Version A (5 items)
  ├── Claude Sonnet 4.6 → Version B (5 items)
  └── Claude Haiku 4.5  → Version C (5 items)
```

### Step 5: Generate Production Items

Run 3 models in parallel on each production item:

```
For each production_item in manifest:
  ├── Claude Opus 4.6   → Version A
  ├── Claude Sonnet 4.6 → Version B
  └── Claude Haiku 4.5  → Version C
```

### Step 6: Assemble Gate Tests

After winning items are selected (post-tournament), assemble into QTI tests.

---

# V. QC CHECK DEFINITIONS

## Stimulus QC Checks (10 binary checks)

| # | Check | Pass Criteria | Fix Type |
|---|---|---|---|
| S1 | Word count | 200-600 words | Programmatic trim/expand |
| S2 | Coping model present | Contains false start + correction | LLM fix |
| S3 | Coping model shows struggle | False start is recognizably weak, not just slightly different | LLM fix |
| S4 | Single move focus | Teaches exactly 1 analytical move, not 2+ | LLM fix |
| S5 | Concise instruction | Teach section ≤ 150 words | Programmatic trim |
| S6 | Shared vocabulary | Uses terms from the shared vocabulary list | LLM fix |
| S7 | No creative writing examples | All examples are analytical/argumentative | LLM fix |
| S8 | Mentor mindset tone | No condescension, no hedging, direct and respectful | LLM fix |
| S9 | HTML valid | Valid HTML that renders correctly | Programmatic fix |
| S10 | KC alignment | Content teaches the specific KC, not a related but different skill | LLM fix |

## Discrimination Item QC Checks (16 binary checks)

| # | Check | Pass Criteria | Fix Type |
|---|---|---|---|
| D1 | Correct answer defensible | Correct answer is unambiguously the best answer | LLM fix |
| D2 | Distractors plausible | Each distractor represents a real student error | LLM fix |
| D3 | No "all of the above" | No lazy option construction | Programmatic fix |
| D4 | Stem clarity | Question is clear without the options | LLM fix |
| D5 | Reading load | Stem + options ≤ 150 words (excluding passage) | Programmatic trim |
| D6 | KC alignment | Tests the specific KC, not general comprehension | LLM fix |
| D7 | Option length balance | Options are similar in length (longest ≤ 2x shortest) | LLM fix |
| D8 | No negative stems | Avoids "Which is NOT..." (cognitively confusing) | LLM fix |
| D9 | Rationale present | Correct and distractor rationales included | Programmatic check |
| D10 | Force-correct feedback | Feedback present, specific, non-answer-revealing | LLM fix |
| D11 | No answer pattern | Correct answers distributed across positions | Programmatic fix |
| D12 | Grammatical consistency | All options grammatically parallel | LLM fix |
| D13 | No clues in stem | Stem doesn't inadvertently reveal the answer | LLM fix |
| D14 | Passage relevance | If passage-based, answer requires the passage (not general knowledge) | LLM fix |
| D15 | Difficulty appropriate | Matches grade level (not trivially easy, not impossibly hard) | LLM fix |
| D16 | Valid QTI type | Item matches the specified QTI interaction type | Programmatic fix |

## Production Item QC Checks (12 binary checks)

| # | Check | Pass Criteria | Fix Type |
|---|---|---|---|
| P1 | Prompt specificity | Task is specific enough for reliable scoring | LLM fix |
| P2 | Rubric observability | All criteria are observable, not inferential | LLM fix |
| P3 | Exemplar quality | Exemplar matches the stated rubric score | LLM fix |
| P4 | Exemplar realism | Exemplar reads like student work, not professional prose | LLM fix |
| P5 | Time limit reasonable | A competent student at target level can complete in allotted time | LLM fix |
| P6 | Passage appropriateness | Passage is rich enough for the analytical task | LLM fix |
| P7 | Multiple valid responses | Task allows multiple valid approaches (not one right answer) | LLM fix |
| P8 | KC alignment | Prompt tests the specific KC skill | LLM fix |
| P9 | Sentence frames available | Relevant frames referenced in scoring, not required | LLM fix |
| P10 | Common pitfalls listed | At least 2 common pitfalls identified for scoring guidance | LLM fix |
| P11 | Copyright clear | Passage is public domain, government, or original | Programmatic check |
| P12 | No creative writing | Task is analytical/argumentative, not creative | LLM fix |

## Passage QC Checks (8 binary checks)

| # | Check | Pass Criteria | Fix Type |
|---|---|---|---|
| X1 | Copyright clear | Public domain, government, CC, or original | Programmatic check |
| X2 | Length appropriate | Within specified word count range | Programmatic trim |
| X3 | Analytical richness | Supports 3+ valid analytical angles | LLM fix |
| X4 | Grade-level complexity | Appropriate reading level for target phase | LLM fix |
| X5 | Not commonly used | Not a standard AP exam passage or overused in test prep | LLM check |
| X6 | Engaging content | Content is interesting to high school students | LLM fix |
| X7 | Strategies present | Contains identifiable rhetorical/literary strategies | LLM check |
| X8 | Context sufficient | Enough context for students to analyze without external knowledge | LLM fix |

---

# VI. QC PIPELINE EXECUTION

## The Fix Loop

```
For each content item:
  Round 1:
    Run all applicable QC checks → get pass/fail for each
    If ALL PASS → item approved
    If ANY FAIL:
      - Programmatic fixes applied first (word count, HTML, answer distribution)
      - LLM fix prompt sent for remaining failures
      → produces fixed version

  Round 2:
    Re-run all QC checks on fixed version
    If ALL PASS → item approved
    If ANY FAIL → one more LLM fix attempt

  Round 3:
    Final QC check
    If ALL PASS → item approved
    If ANY FAIL → item flagged for manual review
```

## LLM Fix Prompt Template

```
The following content item FAILED these QC checks:

ITEM: {item_json}

FAILED CHECKS:
{list_of_failed_checks_with_descriptions}

Fix the item so it passes all checks. Return the complete fixed item in the
same JSON format. Change ONLY what is necessary to pass the failed checks —
do not alter passing aspects of the item.
```

## Programmatic Fix Functions

| Fix | Logic |
|---|---|
| Word count trim | Truncate to limit, ending at sentence boundary |
| Word count expand | Flag for LLM expansion (cannot be purely programmatic) |
| HTML validation | Run through HTML parser, fix unclosed tags |
| Answer distribution | Shuffle correct answer positions across item set |
| "All of the above" removal | Delete option, replace with LLM-generated distractor |
| QTI type validation | Check interaction type matches spec |
| Copyright check | Regex for known copyrighted sources + date check |
| Rationale presence | Check JSON fields exist and are non-empty |

---

# VII. MULTI-MODEL TOURNAMENT

## Tournament Design

Each content slot gets up to 15 attempts (3 models x 5 rounds).

```
Round 1:
  Opus → Item A₁    Sonnet → Item B₁    Haiku → Item C₁
  QC all three → any that pass all checks are candidates

Round 2 (if no winner):
  Opus → Item A₂    Sonnet → Item B₂    Haiku → Item C₂
  (Each model gets the QC feedback from its Round 1 attempt)
  QC all → candidates pool grows

... up to Round 5

Selection:
  From all candidates that passed QC:
  - If 1 candidate → winner
  - If 2+ candidates → evaluation round (see below)
  - If 0 candidates after 5 rounds → manual review flag
```

## Evaluation Round (When Multiple Candidates Pass QC)

Three evaluators score each candidate on a 5-point rubric:

| Criterion | Weight | What It Measures |
|---|---|---|
| Analytical Accuracy | 30% | Is the content analytically sound? Would an AP reader agree? |
| Coping Model Quality | 20% | Does the worked example show genuine struggle + correction? |
| Brainlift Alignment | 15% | Does it follow discrimination-before-production, minimum dose, etc.? |
| AP Rubric Alignment | 20% | Does it train the specific rubric row it targets? |
| Student Engagement | 15% | Would a HS student find this clear and worth doing? |

**Evaluators:**
1. Claude API (different model than the one that generated — e.g., if Opus generated, Sonnet evaluates)
2. ChatGPT web (manual evaluation for a sample — not every item)
3. Gemini web (manual evaluation for a sample)

For automated evaluation at scale, use evaluator #1 (Claude cross-model). Manual evaluation (#2 and #3) applies to a random 10% sample for calibration.

---

# VIII. EXECUTION PLAN

## Batch Order

Content must be generated in dependency order:

```
Batch 1: Passages (all phases)           ~15 items    → 45 generations
Batch 2: Instruction Stimuli (all phases) ~18 items    → 54 generations
Batch 3: Discrimination Items (Phase 1)   ~40 items    → 120 generations
Batch 4: Production Items (Phase 1)       ~25 items    → 75 generations
Batch 5: Discrimination Items (Phase 2)   ~35 items    → 105 generations
Batch 6: Production Items (Phase 2)       ~20 items    → 60 generations
Batch 7: Discrimination Items (Phase 3L)  ~25 items    → 75 generations
Batch 8: Production Items (Phase 3L)      ~20 items    → 60 generations
Batch 9: Discrimination Items (Phase 3T)  ~25 items    → 75 generations
Batch 10: Production Items (Phase 3T)     ~20 items    → 60 generations
Batch 11: Phase 4 Items (all types)       ~35 items    → 105 generations
Batch 12: SAT/ACT Grammar Items           ~63 items    → 189 generations
Batch 13: Gate Assessments (assembly)      ~4 tests     → 12 generations
                                          ─────────
                                Total:    ~1,035 API calls (Round 1 only)
```

With QC fix rounds and tournament continuation, expect ~1,500-2,500 total API calls.

## Cost Estimate (Claude API)

| Model | Input Cost | Output Cost | Est. Calls | Est. Cost |
|---|---|---|---|---|
| Opus 4.6 | $15/M tokens | $75/M tokens | ~500 | ~$150-300 |
| Sonnet 4.6 | $3/M tokens | $15/M tokens | ~500 | ~$30-60 |
| Haiku 4.5 | $0.80/M tokens | $4/M tokens | ~500 | ~$10-20 |
| QC evaluations (Sonnet) | $3/M tokens | $15/M tokens | ~1,000 | ~$60-120 |
| **Total estimate** | | | **~2,500** | **~$250-500** |

## API Implementation

All API calls go through a single Python runner script:

```python
# Pseudocode for the generation runner
import anthropic

client = anthropic.Anthropic()

def generate_content(manifest_item, model="claude-sonnet-4-6-20250514"):
    """Generate content for a single manifest item."""
    agent_prompt = get_agent_prompt(manifest_item)

    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=agent_prompt["system"],
        messages=[{"role": "user", "content": agent_prompt["user"]}]
    )

    return parse_response(response, manifest_item["type"])

def run_tournament_round(manifest_item, round_num, previous_feedback=None):
    """Run one tournament round: 3 models compete."""
    models = [
        "claude-opus-4-6-20250514",
        "claude-sonnet-4-6-20250514",
        "claude-haiku-4-5-20251001"
    ]

    results = []
    for model in models:
        prompt = get_agent_prompt(manifest_item)
        if previous_feedback and model in previous_feedback:
            prompt["user"] += f"\n\nPREVIOUS ATTEMPT FEEDBACK:\n{previous_feedback[model]}"

        result = generate_content(manifest_item, model=model)
        qc_result = run_qc_checks(result, manifest_item["type"])
        results.append({
            "model": model,
            "content": result,
            "qc": qc_result,
            "passed": all(qc_result.values())
        })

    return results

def run_qc_checks(content, content_type):
    """Run all applicable QC checks."""
    checks = get_checks_for_type(content_type)
    results = {}
    for check in checks:
        if check["fix_type"] == "programmatic":
            results[check["id"]] = run_programmatic_check(check, content)
        else:
            results[check["id"]] = run_llm_check(check, content)
    return results
```

---

# IX. OUTPUT DIRECTORY STRUCTURE

```
HS_Writing_Content/
├── manifest.json                    # Full content manifest
├── passages/
│   ├── nonfiction/
│   │   ├── passage-nf-001.json     # Passage + metadata
│   │   └── ...
│   └── poetry/
│       ├── passage-po-001.json
│       └── ...
├── stimuli/
│   ├── phase1/
│   │   ├── essay-architecture-stim.json
│   │   ├── essay-architecture-stim.html
│   │   └── ...
│   └── ...
├── items/
│   ├── phase1/
│   │   ├── discrimination/
│   │   │   ├── C.9.01-disc-set.json
│   │   │   └── ...
│   │   └── production/
│   │       ├── C.9.07-prod-001.json
│   │       └── ...
│   └── ...
├── qti/
│   ├── stimuli/                     # Final QTI XML for stimuli
│   ├── items/                       # Final QTI XML for items
│   └── tests/                       # Final QTI XML for gate tests
├── qc_logs/
│   ├── round1/
│   ├── round2/
│   └── flagged/                     # Items that failed after 3 rounds
├── tournament/
│   ├── round1_results.json
│   ├── round2_results.json
│   └── winners.json
└── push_log/                        # Timeback API push results
    ├── stimuli_push.json
    ├── items_push.json
    └── course_structure.json
```

---

# X. IMPLEMENTATION SEQUENCE

## What to Build First

1. **Content Manifest Generator** — Python script that parses the Blueprint and outputs manifest.json
2. **Agent Prompt Builder** — Functions that construct the full prompt for each agent given a manifest entry
3. **API Runner** — Handles Claude API calls, rate limiting, retries
4. **QC Engine** — Runs binary checks (programmatic + LLM-based)
5. **Tournament Runner** — Orchestrates multi-round, multi-model competition
6. **QTI Assembler** — Converts winning JSON content to QTI 3.0 XML
7. **Timeback Pusher** — Pushes final QTI to Timeback APIs

Build and test each component sequentially. Don't start generating content until the QC engine works.

---

---

# XI. GENERATION LOG

| Batch | Category | Items | Course | Output File | Status |
|---|---|---|---|---|---|
| B1 | Thesis Statements | 15 | A1 | Generated_Content/P1_Discrimination/C1_Thesis_Triage_Items.md | Complete |
| B2 | Analysis vs Summary | 20 | A1 | Generated_Content/P1_Discrimination/C1_Analysis_vs_Summary_Items.md | Complete |
| B3 | Binary Sample Paragraphs | 10 pairs | A1 | Generated_Content/P1_Discrimination/C1_Binary_Sample_Paragraphs.md | Complete |
| B4 | 3-Point Sample Paragraphs | 8 sets | A2 | Generated_Content/P1_Discrimination/C2_ThreePoint_Sample_Paragraphs.md | Complete |
| B5 | AP-Style Prompts | 14 | B1 | Generated_Content/P2_AP_Prompts/AP_Style_Prompts.md | Complete |
| B6 | Coping Models | 12 | A1-B2 | Generated_Content/P4_Coping_Models/Coping_Models.md | Complete |
| B7 | Supplementary Items | ~37 | A1-A2 | Generated_Content/P5_Supplementary/Supplementary_Items.md | Complete |
| B8 | Mentor Sentences | 18 | A1-A2 | Generated_Content/P5_Supplementary/Mentor_Sentences.md | Complete |
| B9a | Scored AP Lang Essays | 22 (12+6+4) | B1-B2 | Generated_Content/P3_Sample_Essays/AP_Lang_Scored_Essays.md | Complete |
| B9b | Scored AP Lit Essays | 22 (12+6+4) | B1-B2 | Generated_Content/P3_Sample_Essays/AP_Lit_Scored_Essays.md | Complete |
| B10 | ACT Writing Prompts | 6 | A2 | Generated_Content/P6_ACT_Writing/ACT_Writing_Prompts.md | Complete |
| B11 | ACT Practice Items | 22 (11 disc + 8 prod + 3 cal) | A2 | Generated_Content/P6_ACT_Writing/ACT_Practice_Items.md | Complete |
| B12 | ACT Scored Essays | 12 (6 exemplars + 6 fine-line) | A2 | Generated_Content/P6_ACT_Writing/ACT_Scored_Essays.md | Complete |

## Content Mapping: Old Course Names → New Track/Course Names

| Old Name | New Name | Track |
|---|---|---|
| Course 1 / C1 (G9) | Course A1 | Track A (Core) |
| Course 2 / C2 (G10) | Course A2 | Track A (Core) |
| Course 3L / C3 (G11 AP Lang) | Course B1L | Track B (AP) |
| Course 3T / C3 (G11 AP Lit) | Course B1T | Track B (AP) |
| Course 4 / C4 (G12) | Course B2 | Track B (AP) |

All previously generated content (B1-B9) maps cleanly to the new structure. No content needs to be regenerated — it just maps to new course codes. New content required: B10-B12 (ACT Writing material for Course A2).

---

*Content Generation Pipeline v3*
*Updated: March 2026*
*For: HS Writing Courses (2 Tracks, 4 Courses) | Alpha School / 2 Hour Learning*
*Method: Ilma Production Methodology adapted for 3 Claude models*
