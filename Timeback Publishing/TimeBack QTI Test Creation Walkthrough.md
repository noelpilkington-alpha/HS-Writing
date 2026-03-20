# Test Creation Guide

## Part 1: For Humans

### What Are We Building?

A **test** is a set of questions that a student takes. In TimeBack (and 1EdTech), we build tests in two steps:

1. **Create the questions** — each question is stored separately in the system as an "assessment item"
2. **Create the test** — the test is a container that says "this test includes question 1, question 2, question 3..." by referencing their IDs

Think of it like a playlist: you upload songs (questions) first, then create a playlist (test) that references which songs to include and in what order.

### The Structure of a Test

```
Test
  └── Part (you'll almost always have just one)
        └── Section (you'll almost always have just one)
              ├── Question 1
              ├── Question 2
              ├── Question 3
              └── ...
```

Most tests are simple: one part, one section, many questions. You only need multiple parts or sections if you want different rules for different groups of questions (e.g., a timed section and an untimed section).

### Step 1: Write Your Questions

Each question needs:

- **The question text** — what the student sees
- **The answer choices** (for multiple choice) or the expected answer (for fill-in-the-blank)
- **Which answer is correct**
- **Metadata** — subject, grade level, and optionally the learning standard it covers

Here are the **question types** available:

| Type | What It Looks Like |
|------|-------------------|
| **choice** | Multiple choice — pick one answer from a list |
| **text-entry** | Type a short answer (a number, a word) |
| **extended-text** | Write a longer response (a sentence, a paragraph) |
| **inline-choice** | A dropdown menu embedded in a sentence ("The capital of France is [Paris / London / Berlin]") |
| **gap-match** | Drag words or phrases into blanks in a sentence |
| **hottext** | Click on the correct word(s) within a passage |
| **order** | Arrange items in the correct sequence |
| **match** | Sort items into categories (e.g., "classify these as renewable or nonrenewable") |
| **hotspot** | Click on the correct area of an image |
| **graphic-gap-match** | Drag items onto specific zones on an image |
| **portable-custom** | Fraction editor or histogram — rendered by a built-in PCI plugin |
| **upload** | Student uploads a file as their response |

### Step 2: Create Each Question in the System

Questions are created by sending them to the API as XML. You don't need to write the XML by hand — you can:

1. **Copy an existing question** — search the API for a similar question, copy its XML, and change the text and answers
2. **Use an LLM** — give an AI assistant this guide and ask it to generate the questions for you
3. **Write it yourself** — use the template in Part 2 below

When you create a question, the system gives you back an **identifier** (a unique ID like `_89393d74-b77b-47e7-8d2d-b68e6ff834d9`). Save this — you'll need it for the test.

To find existing questions to copy:
- Go to `https://qti.alpha-1edtech.ai/docs/` and use the search endpoint
- Or ask an LLM to fetch examples: "Get me 3 multiple choice Math questions for Grade 5"

### Step 3: Assemble the Test

Once all your questions are created and you have their IDs, you create the test. The test needs:

- **A title** — e.g., "Alpha STAAR G5 Math Practice Test v1"
- **Subject and grade** — must match your questions
- **The list of question IDs** — in the order you want students to see them
- **Test settings:**
  - `linear` navigation = students go question by question, can't go back
  - `nonlinear` navigation = students can skip around and return to questions
  - `simultaneous` submission = all answers submitted at the end
  - `individual` submission = each answer submitted as the student goes

### Step 4: Preview and Validate

After creating the test, you can preview it at:
```
https://alphatest.alpha.school/tests/{your-test-identifier}
```

Always validate your XML before creating. The API has a validate endpoint that checks your XML against the QTI standard and tells you if anything is wrong.

### Timed Tests and Fluency

**Timed test** — a regular test with a countdown clock. You add a `timeLimit` (in seconds) at the test level; students still navigate normally and all other settings remain your choice. Use this when you just want to enforce a time limit without changing how the test behaves.

**Fluency test** — a timed test designed to measure speed. It adds `"fluency": true` in the metadata on top of the time limit. Navigation should be `nonlinear` and submission `individual` so that answers are recorded as the student goes (since time may run out before they finish). Items are typically `text-entry` with simple numeric answers (e.g., `5 + 3 = ___`).

### Important Rules

1. **Subject names must be exact.** Use `Math`, not `Mathematics` or `math`. Use `Language`, not `English`. See the full list in Part 2.

2. **Grade is a string number.** Kindergarten = `"0"`, First Grade = `"1"`, PreK = `"-1"`, etc.

3. **You can only edit your own questions.** If someone else created a question, you can view it and copy it, but you can't change it.

4. **Always validate before creating.** One missing bracket in the XML will cause the question to fail silently or render incorrectly.

5. **Search before you create.** There are thousands of existing questions in the system. If you need a Grade 3 Math multiple choice question about fractions, there's probably one already. Search, copy, and modify.

---

## Part 2: LLM Technical Reference

This section is for AI assistants creating questions and tests via the API. Read this entire section before starting work.

### API

**Base URL:** `https://qti.alpha-1edtech.ai/api`
**Interactive Docs:** `https://qti.alpha-1edtech.ai/docs/`
**Auth:** OAuth2 Bearer token (see credentials.env in this project)

### Endpoints

| Action | Method | Endpoint |
|--------|--------|----------|
| Search items | GET | `/assessment-items` |
| Create item | POST | `/assessment-items` |
| Get item | GET | `/assessment-items/{identifier}` |
| Update item | PUT | `/assessment-items/{identifier}` |
| Delete item | DELETE | `/assessment-items/{identifier}` |
| Bulk update metadata | PUT | `/assessment-items/metadata` |
| Validate XML | POST | `/validate` |
| Validate batch | POST | `/validate/batch` |
| Search tests | GET | `/assessment-tests` |
| Create test | POST | `/assessment-tests` |
| Get test | GET | `/assessment-tests/{identifier}` |
| Update test | PUT | `/assessment-tests/{identifier}` |
| Delete test | DELETE | `/assessment-tests/{identifier}` |
| Get all questions in a test | GET | `/assessment-tests/{identifier}/questions` |
| Add item to section | POST | `/assessment-tests/{testId}/test-parts/{partId}/sections/{sectionId}/items` |
| Remove item from section | DELETE | `/assessment-tests/{testId}/test-parts/{partId}/sections/{sectionId}/items/{itemId}` |
| Reorder items in section | PUT | `/assessment-tests/{testId}/test-parts/{partId}/sections/{sectionId}/items/order` |
| Create stimulus | POST | `/stimuli` |
| Get stimulus | GET | `/stimuli/{identifier}` |

### Step-by-Step: Creating Items and a Test

Follow this exact sequence. Do not skip steps.

#### Step 0: Fetch a real example for your question type

This is the most important step. Do not write XML from memory or from the template alone. Fetch an existing item from the API and use its `rawXml` as your starting point.

```
GET /assessment-items?type=choice&subject=Math&grade=5&limit=1
GET /assessment-items?type=text-entry&subject=Math&limit=1
GET /assessment-items?type=extended-text&limit=1
GET /assessment-items?type=inline-choice&limit=1
GET /assessment-items?type=match&limit=1
GET /assessment-items?type=order&limit=1
GET /assessment-items?type=gap-match&limit=1
GET /assessment-items?type=hottext&limit=1
GET /assessment-items?type=hotspot&limit=1
GET /assessment-items?type=graphic-gap-match&limit=1
GET /assessment-items?type=portable-custom&limit=1
GET /assessment-items?type=upload&limit=1
```

Type names are **kebab-case** (e.g., `text-entry`, not `textEntry`).

From the response, use only the `rawXml` field. Ignore the `content` field (it's a parsed duplicate).

#### Step 1: Build the item XML

Start from the fetched `rawXml`. Modify:
- The `identifier` attribute on `<qti-assessment-item>` — generate a new UUID prefixed with `_`
- The question text inside `<qti-prompt>` or `<qti-item-body>`
- The answer choices and their `identifier` attributes — generate new UUIDs for each
- The correct answer in `<qti-correct-response>` — must match one of the choice UUIDs
- Remove any audio/TTS catalog entries (`<qti-catalog>` block) unless you have audio files
- Remove any `data-audio-stimulus` or `data-audio-options` attributes from the root element

Keep everything else from the original: the namespace declarations, schema locations, outcome declarations, and response processing template.

#### Step 2: Validate the XML

```json
POST /validate
{
  "schema": "item",
  "xml": "your complete XML string here"
}
```

Fix any errors before proceeding. Common validation errors:
- Missing namespace declaration
- Mismatched identifier references (correct response doesn't match any choice)
- Malformed XML (unclosed tags, bad escaping)

#### Step 3: Build the JSON payload

Construct the payload **in Python or equivalent** — never in shell. The payload has two top-level fields:

```python
import json
import uuid

# Your XML from step 1 (properly escaped as a Python string)
xml_string = '''<qti-assessment-item ...>...</qti-assessment-item>'''

payload = {
    "format": "xml",
    "xml": xml_string,
    "metadata": {
        "subject": "Math",          # Must match allowed values exactly
        "grade": "5",               # String, not integer
        "learningObjectiveSet": [
            {
                "source": "CASE",
                "learningObjectiveIds": ["5.NF.B.7"]
            }
        ]
    }
}

# Write to file — this preserves all escaping correctly
with open("payload.json", "w") as f:
    json.dump(payload, f)
```

Why Python? Because shell heredocs and variable interpolation will corrupt backslashes in LaTeX (`\frac` becomes form feed + `rac`), break on special characters in XML, and silently produce invalid JSON.

#### Step 4: POST the item

```
POST /assessment-items
Content-Type: application/json
Authorization: Bearer {token}
Body: contents of payload.json
```

The response includes the created item with its `identifier`. Save this identifier.

#### Step 5: Repeat for all questions

Create all items before creating the test. Collect all returned identifiers.

#### Step 6: Create the test

```json
POST /assessment-tests
{
  "identifier": "_test-GENERATE-UUID",
  "title": "Your Test Title",
  "qtiVersion": "3.0",
  "metadata": {
    "subject": "Math",
    "grade": "5"
  },
  "qti-test-part": [
    {
      "identifier": "_testpart-GENERATE-UUID",
      "navigationMode": "linear",
      "submissionMode": "simultaneous",
      "qti-assessment-section": [
        {
          "identifier": "_section-GENERATE-UUID",
          "title": "Main Section",
          "visible": true,
          "required": true,
          "fixed": true,
          "sequence": 1,
          "qti-assessment-item-ref": [
            { "identifier": "ITEM-ID-1", "href": "ITEM-ID-1.xml" },
            { "identifier": "ITEM-ID-2", "href": "ITEM-ID-2.xml" },
            { "identifier": "ITEM-ID-3", "href": "ITEM-ID-3.xml" }
          ]
        }
      ]
    }
  ],
  "qti-outcome-declaration": [
    { "identifier": "SCORE", "cardinality": "single", "baseType": "float" }
  ]
}
```

The `identifier` in each `qti-assessment-item-ref` is the item identifier returned when you created it. The `href` is `{identifier}.xml`.

#### Step 7: Preview

```
https://alphatest.alpha.school/tests/{test-identifier}
```

### Minimal XML Template (Multiple Choice)

Use this only if you cannot fetch a real example. A fetched example is always better.

```xml
<qti-assessment-item
  xmlns="http://www.imsglobal.org/xsd/imsqtiasi_v3p0"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.imsglobal.org/xsd/imsqtiasi_v3p0 https://purl.imsglobal.org/spec/qti/v3p0/schema/xsd/imsqti_itemv3p0p1_v1p0.xsd"
  identifier="_GENERATE-UUID"
  title="Multiple Choice Question"
  time-dependent="false"
  xml:lang="en-US">

  <qti-response-declaration identifier="RESPONSE" cardinality="single" base-type="identifier">
    <qti-correct-response>
      <qti-value>CORRECT-CHOICE-UUID</qti-value>
    </qti-correct-response>
  </qti-response-declaration>

  <qti-outcome-declaration identifier="SCORE" cardinality="single" base-type="float">
    <qti-default-value>
      <qti-value>0</qti-value>
    </qti-default-value>
  </qti-outcome-declaration>

  <qti-item-body>
    <qti-prompt>
      <p><span style="font-size: 16px;">Question text here</span></p>
    </qti-prompt>
    <qti-choice-interaction response-identifier="RESPONSE" shuffle="false" max-choices="1">
      <qti-simple-choice identifier="UUID-A"><p><span style="color: rgb(0, 0, 0);">Answer A</span></p></qti-simple-choice>
      <qti-simple-choice identifier="UUID-B"><p><span style="color: rgb(0, 0, 0);">Answer B</span></p></qti-simple-choice>
      <qti-simple-choice identifier="UUID-C"><p><span style="color: rgb(0, 0, 0);">Answer C</span></p></qti-simple-choice>
      <qti-simple-choice identifier="UUID-D"><p><span style="color: rgb(0, 0, 0);">Answer D</span></p></qti-simple-choice>
    </qti-choice-interaction>
  </qti-item-body>

  <qti-response-processing template="https://purl.imsglobal.org/spec/qti/v3p0/rptemplates/match_correct"/>
</qti-assessment-item>
```

### Key Structural Differences by Question Type

You must fetch a real example for each type, but here's what changes structurally:

**choice** (multiple choice, single answer):
- `base-type="identifier"`, `cardinality="single"`
- `<qti-choice-interaction max-choices="1">`
- Correct response is one choice UUID
- For multiple-select variant: set `cardinality="multiple"` and `max-choices="0"`

**text-entry** (short answer):
- `base-type="string"`, `cardinality="single"`
- `<qti-text-entry-interaction response-identifier="RESPONSE" expected-length="20"/>`
- Correct response is the expected string (e.g., `"3"` or `"Paris"`)

**extended-text** (long answer):
- `base-type="string"`, `cardinality="single"`
- `<qti-extended-text-interaction>` with optional `expected-length`
- Usually no correct response (manually graded)

**inline-choice** (dropdown in text):
- `base-type="identifier"`, `cardinality="single"`
- `<qti-inline-choice-interaction>` embedded within a `<p>` element
- Each `<qti-inline-choice>` has an identifier

**match** (classify/categorize):
- `base-type="directedPair"`, `cardinality="multiple"`
- `<qti-match-interaction>` with two `<qti-simple-match-set>` elements (sources and targets)
- Correct response is pairs: `"sourceUUID targetUUID"`

**order** (sequence/arrange):
- `base-type="identifier"`, `cardinality="ordered"`
- `<qti-order-interaction>`
- Correct response lists identifiers in the correct order

**gap-match** (drag to fill blanks):
- `base-type="directedPair"`, `cardinality="multiple"`
- `<qti-gap-match-interaction>` with `<qti-gap-text>` (draggable items) and `<qti-gap>` (blanks in text)
- Correct response pairs gap-text IDs with gap IDs

**hottext** (select text):
- `base-type="identifier"`, `cardinality="single"` or `"multiple"`
- `<qti-hottext-interaction>` with `<qti-hottext>` wrapping selectable spans
- Correct response is the hottext identifier(s)

**hotspot** (click on image area):
- `base-type="identifier"`, `cardinality="single"` or `"multiple"`
- `<qti-hotspot-interaction>` with `<qti-hotspot-choice>` elements defining clickable regions
- Requires an image (`<object>` or `<img>`) as part of the interaction

**graphic-gap-match** (drag onto image zones):
- `base-type="directedPair"`, `cardinality="multiple"`
- `<qti-graphic-gap-match-interaction>` with an image, `<qti-gap-img>` elements (draggable items), and `<qti-associable-hotspot>` elements (target zones on the image)
- Correct response pairs gap-img IDs with hotspot IDs (e.g., `"gapImg1 hotspot2"`)

**portable-custom** (Portable Custom Interaction — PCI):
- `base-type="string"`, `cardinality="single"`
- Element: `<qti-portable-custom-interaction>` (always this element, not a custom tag)
- The `custom-interaction-type-identifier` attribute (URN) determines which PCI subtype
- Two subtypes are supported:
  - **fractionEditor** (`urn:fdc:edulastic.com:2024:pci:fractionEditor`): fraction visualization; config via `data-fraction-type` (rectangles|circles), `data-rows`, `data-columns`, `data-sectors`, `data-selected-segments` (JSON)
  - **histogram** (`urn:fdc:edulastic.com:2024:pci:histogram`): interactive chart; config via `data-chart-data` (JSON array of `{x,y}`), `data-x-axis-label`, `data-y-axis-label`, `data-y-axis-min/max`, `data-step-size`
- Always contains `<qti-interaction-modules>` (plugin loader) and `<qti-interaction-markup>` (HTML placeholder)
- Correct response is a JSON string matched against the player's output
- Fetch a real example — the `data-*` attributes vary between subtypes

**upload** (file upload):
- `base-type="file"`, `cardinality="single"`
- `<qti-upload-interaction>`
- No correct response (manually graded)

### Math Expressions

Use the `input__math` span with a `data-latex` attribute:

```xml
<span class="input__math" data-latex="\\frac{1}{8}"></span>
```

Common patterns:
- Fractions: `\\frac{numerator}{denominator}` → renders as a fraction
- Exponents: `x^{2}` → renders as x squared
- Square root: `\\sqrt{16}` → renders as square root of 16
- Mixed: `3\\frac{1}{4}` → renders as 3 and one quarter
- Multiplication: `\\times` → renders as ×
- Division: `\\div` → renders as ÷

**Critical escaping rule:** In your Python string, write `\\\\frac` so that `json.dump` produces `\\frac` in the JSON, which becomes `\frac` in the XML. If you see `\f` anywhere in the output, you have an escaping bug. Test by checking the JSON file for the literal characters `\frac` — if you see them, it's correct.

Alternatively, place the LaTeX in a Python raw string (`r"\\frac{1}{8}"`) and let `json.dump` handle the rest.

To add a math expression inline with text, use `&#160;` for spacing:

```xml
<p>
  <span style="font-size: 16px;">A baker used&#160;</span>
  <span class="input__math" data-latex="\\frac{1}{8}"></span>
  <span style="font-size: 16px;">&#160;pound of flour per cake.</span>
</p>
```

### Timed Tests and Fluency

**Timed test** — add a `timeLimit` (in seconds) to the test JSON. The clock counts down; all other settings (navigation, submission mode) are your choice:

```json
{
  "timeLimit": 3600
}
```

**Fluency test** — a timed test that measures speed. Adds `"fluency": true` in metadata; use `nonlinear` navigation and `individual` submission so answers are saved as the clock runs out:

```json
{
  "timeLimit": 60,
  "metadata": {
    "fluency": true
  },
  "qti-test-part": [
    {
      "navigationMode": "nonlinear",
      "submissionMode": "individual"
    }
  ]
}
```

Fluency items are typically `text-entry` type with simple numeric answers (e.g., `5 + 3 = ___`).

### Stimuli (Reading Passages)

If your questions share a common reading passage, image, or context, create it as a **stimulus** and reference it from the items.

```json
POST /stimuli
{
  "format": "xml",
  "xml": "<qti-assessment-stimulus ...>passage text here</qti-assessment-stimulus>",
  "metadata": {
    "subject": "Reading",
    "grade": "5"
  }
}
```

Then reference it in the item XML:
```xml
<qti-assessment-stimulus-ref identifier="STIMULUS-ID" href="stimuli/STIMULUS-ID" title="Passage Title"/>
```

### Allowed Values

#### Subjects

```
ELA, FastMath, Language, Language-athena, Language-ISEE, Language-unit,
Math, Math-athena, Math-ISEE, Math-unit, Phonetic, Reading,
Reading-athena, Reading-ISEE, Reading-unit, Science, Science-athena,
Science-unit, Social Studies, Vocabulary, Writing
```

#### Grades

`"-1"` (PreK), `"0"` (Kindergarten), `"1"` through `"12"`. Always a string in the JSON payload.

#### Question Types (API `type` parameter values)

`choice`, `text-entry`, `hottext`, `inline-choice`, `extended-text`, `gap-match`, `order`, `match`, `graphic-gap-match`, `portable-custom`, `hotspot`, `upload`

Note: Type names are **kebab-case** in the API (e.g., `text-entry`, not `textEntry`).

### Rules and Pitfalls

1. **Subject must match the allowed values exactly.** `Math` not `Mathematics`. `Language` not `English`. Case-sensitive.

2. **All identifiers must be UUIDs.** Item identifiers are prefixed with `_` (e.g., `_89393d74-b77b-47e7-8d2d-b68e6ff834d9`). Choice identifiers are plain UUIDs (no prefix). Generate fresh UUIDs for every new item and every choice — never reuse identifiers across items.

3. **LaTeX escaping is the #1 source of bugs.** `\frac` in XML, `\\frac` in JSON string values, `\\\\frac` in Python string literals (or `r"\\frac"` in raw strings). If the test player shows "Math input error", your LaTeX escaping is wrong. Always verify the final JSON file contains the literal text `\frac`, not a form feed character.

4. **Always use `"format": "xml"`.** JSON item format is experimental and not supported.

5. **Always validate before creating.** `POST /validate` with `"schema": "item"` for items, `"schema": "test"` for tests. Do not skip this step. A validation error caught here saves debugging a broken test in the player.

6. **Use the `match_correct` response processing template** for all standard question types:
   ```
   https://purl.imsglobal.org/spec/qti/v3p0/rptemplates/match_correct
   ```
   Do not write custom `<qti-response-condition>` logic. The template handles scoring.

7. **Non-breaking spaces in XML.** Use `&#160;` (not `&nbsp;`) for spacing around inline math expressions. `&nbsp;` is not valid in XML without an HTML entity declaration.

8. **Ownership.** The API enforces ownership: you can only update/delete items created by your API client (`admin.own` scope). Items created by others are read-only. You can still read and copy them.

9. **Fetch real examples before writing.** Always start from a fetched `rawXml` for the question type you need. Adapting a real item is faster and less error-prone than writing from scratch or from the template.

10. **Build JSON payloads programmatically.** Use Python (`json.dump`), Node.js (`JSON.stringify`), or equivalent. Never construct JSON with shell heredocs, string concatenation, or template literals that involve XML with backslashes. Shell interpolation will silently corrupt your payload.

11. **Strip audio/TTS when cloning items.** Fetched items may include `<qti-catalog>` blocks with audio file references and `data-audio-*` attributes. Remove these unless you have corresponding audio files. They won't break the item, but they'll cause 404 errors in the player's audio features.

12. **Test the item in the player after creating.** Validation checks XML structure, but it doesn't verify that the question renders correctly, that math expressions display, or that the correct answer is actually correct. Always preview.
