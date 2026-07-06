# Council of Writing Instruction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Claude Code skill that convenes 10 source-grounded pedagogy personas + a synthesis judge to design new writing lessons or review draft ones.

**Architecture:** A `SKILL.md` orchestrator drives a 4-step runtime flow (convene → deliberate in parallel subagents → adjudicate → emit). Each persona is a pre-built markdown "brief" grounded in a real book (extracted from on-disk PDFs) or the `Instructional_Design_KB/`. The judge adjudicates conflicts with a stated tie-break rule rather than averaging.

**Tech Stack:** Markdown (skill + persona briefs), `pdftotext` (mingw64, already installed) for PDF extraction, `pypdf` (installed) as fallback, the Agent tool for parallel persona deliberation. No compiled code, no test runner — this is a prose/prompt artifact. "Tests" are concrete acceptance checks (grep/structural/trial-run), defined per task.

## Global Constraints

- **Skill location:** `C:\Users\noelp\.claude\skills\council-of-writing-instruction\` (user scope, matches existing `writing-card-*` skills).
- **Provenance rule (HARD):** every substantive persona claim must carry a source tag traceable to a book+page/section or a KB section. No fabricated facts, stats, or quotes. (House rule: `lesson-content-provenance-rule`.)
- **No em dashes in generated lesson output** (Noel 2026-06-30) — use commas/colons/parens. Applies to the `design`-mode lesson draft the skill EMITS, not to the skill's own internal docs.
- **Frontmatter convention:** `name`, `version`, `description` (block scalar), `triggers` (list), `allowed-tools` (list). Copy shape from `writing-card-design/SKILL.md`.
- **Persona brief template is fixed** (identical shape for all 10): `Core commitments` · `Characteristic moves` · `Pushes AGAINST` · `Evidence grade` · `Source anchors` · `The "tell"`.
- **Grounding tiers:** seats 1–6 = book (on-disk PDF); seats 2,5,7,8 also cite KB; seats 9–10 = targeted web research.
- **Spec reference:** `docs/superpowers/specs/2026-07-06-council-of-writing-instruction-design.md`. Read it before starting.
- **On-disk source PDFs** (in `C:\Users\noelp\HS Writing\`):
  - TWR: `The Writing Revolution 2.0 ... (Judith C. Hochman, Natalie Wexler) (Z-Library).pdf`
  - TSIS: `They Say  I Say with Readings (Gerald Graff, Cathy Birkenstein etc.) (Z-Library).pdf`
  - DI: `Theory-of-Instruction-Principles-and-Applications.pdf`
  - Kirschner/Hendrick: `How Learning Happens ... .pdf` and `How Teaching Happens ... .pdf`
  - Yeager: `10 to 25. The Science of Motivating Young People ... (David Yeager) (Z-Library).pdf`
- **KB reference:** `Instructional_Design_KB/{00_Knowledge_Base,01_Applied_Toolkit,02_Framework_Audit,03_Sources}.md`.
- **Test lesson (for acceptance trials):** `Course review/L1_activity_corrected.html`.
- **Commit discipline:** commit after each task. Branch is `hs-writing-spec-baseline` (already off main) — commit there.

---

## File Structure

```
C:\Users\noelp\.claude\skills\council-of-writing-instruction\
  SKILL.md                          # frontmatter + orchestration (Task 12)
  personas/
    01-twr-hochman-wexler.md        # Task 3
    02-srsd-graham-harris.md        # Task 4
    03-tsis-graff-birkenstein.md    # Task 4
    04-di-engelmann.md              # Task 5
    05-kirschner-hendrick.md        # Task 5
    06-yeager.md                    # Task 6
    07-wiliam-hattie.md             # Task 7 (KB-grounded)
    08-ubd-wiggins-mctighe.md       # Task 7 (KB-grounded)
    09-hayes-flower.md              # Task 8 (research)
    10-elbow-gallagher.md           # Task 9 (research)
    judge.md                        # Task 10
  references/
    roster.md                       # Task 2 (seat index + convene cues)
    output-templates.md             # Task 11 (design-draft + review-list shapes)
    persona-brief-template.md       # Task 1 (the fixed shape)
    _extraction/                    # raw pdftotext dumps (build scratch, git-ignored)
```

Responsibilities: `SKILL.md` = orchestration only (no persona content inline). `personas/*` = one grounded expert each, self-contained. `references/roster.md` = the convening lookup the judge reads. `references/output-templates.md` = the two artifact shapes. Files that change together (all personas) live together.

---

### Task 1: Persona brief template + skill skeleton

**Files:**
- Create: `C:\Users\noelp\.claude\skills\council-of-writing-instruction\references\persona-brief-template.md`
- Create: `C:\Users\noelp\.claude\skills\council-of-writing-instruction\.gitignore-note.md` (documents that `_extraction/` is scratch)

**Interfaces:**
- Produces: the fixed brief template every persona task (3–10) fills in. Section headers are the contract: `## Core commitments`, `## Characteristic moves`, `## Pushes AGAINST`, `## Evidence grade`, `## Source anchors`, `## The "tell"`.

- [ ] **Step 1: Create the skill directory tree**

```bash
mkdir -p "C:/Users/noelp/.claude/skills/council-of-writing-instruction/personas"
mkdir -p "C:/Users/noelp/.claude/skills/council-of-writing-instruction/references/_extraction"
```

- [ ] **Step 2: Write the persona brief template**

Write `references/persona-brief-template.md` with this exact content:

```markdown
# <Seat Name> — <Layer>

<!-- Grounding tier: book | book+KB | KB | research -->

## Core commitments
<!-- 3–6 bullets: what this expert fundamentally believes about teaching writing -->
-

## Characteristic moves
<!-- concrete lesson-design moves they advocate; each is actionable in a lesson -->
-

## Pushes AGAINST
<!-- what they would object to in a lesson; THIS is the source of disagreement.
     Name the rival stance where possible (e.g. "against Elbow's low-structure openness"). -->
-

## Evidence grade
<!-- A / B / C from the KB, or "dissent (low-evidence)" for seat 10. One line + why. -->

## Source anchors
<!-- every core claim above maps to a source. Format: [claim] -> BookShort p.NN  OR  KB 00 §2.5 -->
-

## The "tell"
<!-- one line: how this persona SOUNDS, so deliberations stay in character and distinct -->
```

- [ ] **Step 3: Acceptance check — template has all six required sections**

Run:
```bash
grep -cE "^## (Core commitments|Characteristic moves|Pushes AGAINST|Evidence grade|Source anchors|The \"tell\")" "C:/Users/noelp/.claude/skills/council-of-writing-instruction/references/persona-brief-template.md"
```
Expected: `6`

- [ ] **Step 4: Commit**

```bash
cd "c:/Users/noelp/HS Writing"
git add "C:/Users/noelp/.claude/skills/council-of-writing-instruction/references/persona-brief-template.md"
git commit -m "feat(council): persona brief template + skill skeleton"
```

Note: the skill lives outside the repo working dir, so `git add` uses the absolute path. If git refuses the outside-repo path, that is expected — the skill dir is not version-controlled by this repo; in that case skip the commit and note it. (Verify with `git rev-parse --show-toplevel`.) **If the skill dir is not under the repo, commit only the plan/spec changes to the repo and treat skill files as delivered-in-place.**

---

### Task 2: Roster index (`roster.md`) with convene cues

**Files:**
- Create: `.../references/roster.md`

**Interfaces:**
- Consumes: nothing (first authored reference).
- Produces: the table the judge's CONVENE step reads to pick seats. Columns: `Seat`, `Layer`, `Convene when...`, `Bench when...`, `Brief file`. Seat IDs (`twr`, `srsd`, `tsis`, `di`, `kh`, `yeager`, `wh`, `ubd`, `hf`, `eg`) are the contract used by `--seats`.

- [ ] **Step 1: Write `roster.md`**

Write the file with a header explaining it drives convening, then this table (fill all 10 rows):

```markdown
# Council Roster & Convening Cues

The judge reads this at the CONVENE step to pick the 4–6 seats with genuine
stake in a given lesson. Seat IDs are used by the `--seats` override.

| ID | Seat | Layer | Convene when… | Bench when… | Brief |
|----|------|-------|---------------|-------------|-------|
| twr | Hochman & Wexler (TWR) | Writing pedagogy | sentence/paragraph-level craft, syntax, scaffolded writing structures | pure motivation or assessment-only lessons | personas/01-twr-hochman-wexler.md |
| srsd | Graham & Harris (SRSD) | Writing pedagogy | any lesson teaching a writing STRATEGY, mnemonics, self-regulation | non-strategy mechanical drills | personas/02-srsd-graham-harris.md |
| tsis | Graff & Birkenstein (TSIS) | Writing pedagogy | argument, academic moves, entering a conversation, templates for voice | narrative/creative or pre-argument grades | personas/03-tsis-graff-birkenstein.md |
| di | Engelmann (DI) | Instruction/structure | need for unambiguous sequencing, error-free design, faultless communication | open/exploratory creative tasks | personas/04-di-engelmann.md |
| kh | Kirschner & Hendrick | Learning science | cognitive load, worked examples, retrieval/spacing, novice sequencing | lessons already load-light with no sequencing question | personas/05-kirschner-hendrick.md |
| yeager | Yeager | Motivation | adolescent buy-in, autonomy/status, feedback tone, effortful tasks | low-stakes mechanical drills with no motivation dimension | personas/06-yeager.md |
| wh | Wiliam & Hattie | Assessment/feedback | any lesson with feedback, rubrics, formative checks, self-assessment | pure content-delivery with no assessment surface | personas/07-wiliam-hattie.md |
| ubd | Wiggins & McTighe (UbD) | Backward design | unit/lesson objective clarity, transfer goals, assessment-before-activity | single micro-skill drill with obvious goal | personas/08-ubd-wiggins-mctighe.md |
| hf | Hayes & Flower | Cognitive process | composing-process load, planning/translating/reviewing, working memory while writing | isolated non-composing sub-skills | personas/09-hayes-flower.md |
| eg | Elbow / Gallagher | Voice counterweight (dissent) | anything at risk of formula/voicelessness; open/authentic writing | tightly-specified mechanical mastery items | personas/10-elbow-gallagher.md |
```

- [ ] **Step 2: Acceptance check — 10 seats, all brief paths resolvable later**

Run:
```bash
grep -cE "^\| (twr|srsd|tsis|di|kh|yeager|wh|ubd|hf|eg) " "C:/Users/noelp/.claude/skills/council-of-writing-instruction/references/roster.md"
```
Expected: `10`

- [ ] **Step 3: Commit** (per Task 1 note on skill-dir git scope)

```bash
git add -A && git commit -m "feat(council): roster index with convene/bench cues" || echo "skill dir outside repo — delivered in place"
```

---

### Task 3: Extract + build TWR persona (proves the extraction method)

This task establishes the reusable extraction method; Tasks 4–6 repeat it.

**Files:**
- Create: `.../references/_extraction/twr.txt` (scratch)
- Create: `.../personas/01-twr-hochman-wexler.md`

**Interfaces:**
- Consumes: `persona-brief-template.md` (Task 1).
- Produces: `personas/01-twr-hochman-wexler.md`, first filled brief; sets the pattern (extract → skim → fill template with page anchors).

- [ ] **Step 1: Extract text from the TWR PDF**

```bash
cd "c:/Users/noelp/HS Writing"
pdftotext -layout "The Writing Revolution 2.0 A Guide to Advancing Thinking Through Writing in All Subjects and Grades (Judith C. Hochman, Natalie Wexler) (Z-Library).pdf" "C:/Users/noelp/.claude/skills/council-of-writing-instruction/references/_extraction/twr.txt"
wc -l "C:/Users/noelp/.claude/skills/council-of-writing-instruction/references/_extraction/twr.txt"
```
Expected: a line count in the thousands (non-empty extraction). If 0 lines, fall back to: `python -c "import pypdf,sys; r=pypdf.PdfReader(sys.argv[1]); open(sys.argv[2],'w',encoding='utf-8').write('\n'.join((p.extract_text() or '') for p in r.pages))" "<pdf>" "<out>"`.

- [ ] **Step 2: Read the extraction + KB to source the brief**

Read (via Read tool, in chunks): the `_extraction/twr.txt` table of contents and the sentence-level strategy chapters; and `Instructional_Design_KB/00_Knowledge_Base.md` §2.6 (sentence combining). Identify: because/but/so, sentence expansion, appositives, sentence types, single-paragraph outline (SPO), revising vs. editing. Note page numbers from the extraction.

- [ ] **Step 3: Write the TWR brief from the template**

Fill `personas/01-twr-hochman-wexler.md` using the Task-1 template. Requirements for a valid brief:
- `Core commitments`: 3–6 bullets (e.g., "writing is taught explicitly at the sentence level first; sentences before paragraphs before compositions").
- `Characteristic moves`: concrete (because/but/so; sentence expansion with question words; SPO before drafting).
- `Pushes AGAINST`: name a rival (e.g., "against Elbow's free-writing-first: unstructured writing leaves struggling writers behind").
- `Evidence grade`: `B` (practitioner method; sentence-combining component is KB Grade A) with one-line why.
- `Source anchors`: each core claim → `TWR2.0 p.NN` or `KB 00 §2.6`. At least 4 anchors.
- `The "tell"`: one line (e.g., "Relentlessly concrete: 'show me the sentence.'").

- [ ] **Step 4: Acceptance check — brief is complete + anchored**

Run:
```bash
F="C:/Users/noelp/.claude/skills/council-of-writing-instruction/personas/01-twr-hochman-wexler.md"
grep -cE "^## (Core commitments|Characteristic moves|Pushes AGAINST|Evidence grade|Source anchors|The \"tell\")" "$F"   # expect 6
grep -cE "TWR2\.0 p\.|KB 00" "$F"                                                                                        # expect >=4
grep -cE "against |unlike |not like " "$F"                                                                               # expect >=1 (named disagreement)
```
Expected: `6`, then `>=4`, then `>=1`.

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat(council): TWR persona brief (extraction method established)" || echo "skill dir outside repo — delivered in place"
```

---

### Task 4: Build SRSD + TSIS persona briefs

**Files:**
- Create: `.../references/_extraction/tsis.txt`
- Create: `.../personas/02-srsd-graham-harris.md`
- Create: `.../personas/03-tsis-graff-birkenstein.md`

**Interfaces:**
- Consumes: template (Task 1), extraction method (Task 3).
- Produces: briefs 02 and 03.

- [ ] **Step 1: SRSD brief (KB-grounded — no PDF)**

SRSD's primary grounding is the KB (Writing Next), not an on-disk book. Read `Instructional_Design_KB/00_Knowledge_Base.md` §2.5 and `02_Framework_Audit.md` §1. Fill `personas/02-srsd-graham-harris.md`:
- Core commitments: explicit strategy instruction; the six stages (Develop Background Knowledge, Discuss It, Model It, Memorize It, Support It, Independent Performance); teach self-regulation not just moves; biggest edge is for struggling writers.
- Characteristic moves: mnemonics (HIT/PROVE/S³); coping-model think-aloud with false starts; gradual release; self-monitoring cues.
- Pushes AGAINST: "against clean expert models (Model It must show messy decisions)"; "against fading support too fast for struggling writers."
- Evidence grade: `A` (ES 1.14 vs 0.62; WWC STRONG) — cite KB.
- Source anchors: `KB 00 §2.5`, `KB 00 §2.1`, `KB 02 §1`. ≥4.
- Tell: "Name the strategy, model it messy, then fade."

- [ ] **Step 2: Extract TSIS text**

```bash
cd "c:/Users/noelp/HS Writing"
pdftotext -layout "They Say  I Say with Readings (Gerald Graff, Cathy Birkenstein etc.) (Z-Library).pdf" "C:/Users/noelp/.claude/skills/council-of-writing-instruction/references/_extraction/tsis.txt"
wc -l "C:/Users/noelp/.claude/skills/council-of-writing-instruction/references/_extraction/tsis.txt"
```
Expected: thousands of lines (fallback to pypdf if 0).

- [ ] **Step 3: TSIS brief**

Read the extraction's templates chapters. Fill `personas/03-tsis-graff-birkenstein.md`:
- Core commitments: writing is entering a conversation ("they say / I say"); templates scaffold rhetorical moves, they don't stifle voice; start with what others say.
- Characteristic moves: the templates (they say ___, I say ___; "As X argues…"; naysayer/"but"; "so what? / who cares?"); metacommentary.
- Pushes AGAINST: "against DI's rigid scripting (templates are flexible scaffolds for voice, not fixed scripts)"; "against pure own-knowledge argument with no source to respond to."
- Evidence grade: `B` (widely-used practitioner framework; aligns with KB source-binding 2.4).
- Source anchors: `TSIS p.NN` ≥4.
- Tell: "Start with what they say; then your I-say has traction."

- [ ] **Step 2/3 acceptance check (run for BOTH new briefs)**

Run (repeat with F=02 and F=03):
```bash
for F in "02-srsd-graham-harris" "03-tsis-graff-birkenstein"; do
  P="C:/Users/noelp/.claude/skills/council-of-writing-instruction/personas/$F.md"
  echo "$F:"; grep -cE "^## (Core commitments|Characteristic moves|Pushes AGAINST|Evidence grade|Source anchors|The \"tell\")" "$P"
  grep -cE "p\.|KB " "$P"; grep -cE "against |unlike " "$P"
done
```
Expected each: `6`, then `>=4`, then `>=1`.

- [ ] **Step 4: Commit**

```bash
git add -A && git commit -m "feat(council): SRSD + TSIS persona briefs" || echo "skill dir outside repo — delivered in place"
```

---

### Task 5: Build DI (Engelmann) + Kirschner/Hendrick briefs

**Files:**
- Create: `.../references/_extraction/di.txt`, `.../references/_extraction/hlh.txt`
- Create: `.../personas/04-di-engelmann.md`, `.../personas/05-kirschner-hendrick.md`

**Interfaces:**
- Consumes: template, extraction method.
- Produces: briefs 04 and 05.

- [ ] **Step 1: Extract DI + How Learning Happens**

```bash
cd "c:/Users/noelp/HS Writing"
pdftotext -layout "Theory-of-Instruction-Principles-and-Applications.pdf" "C:/Users/noelp/.claude/skills/council-of-writing-instruction/references/_extraction/di.txt"
pdftotext -layout "How Learning Happens Seminal Works in Educational Psychology and What They Mean in Practice (Paul A. Kirschner, Carl Hendrick) (Z-Library).pdf" "C:/Users/noelp/.claude/skills/council-of-writing-instruction/references/_extraction/hlh.txt"
wc -l "C:/Users/noelp/.claude/skills/council-of-writing-instruction/references/_extraction/di.txt" "C:/Users/noelp/.claude/skills/council-of-writing-instruction/references/_extraction/hlh.txt"
```
Expected: both non-empty (fallback to pypdf per file if 0).

- [ ] **Step 2: DI brief**

Fill `personas/04-di-engelmann.md`:
- Core commitments: any child can be taught with faultless instruction; ambiguity is the enemy; sequences must be logically unambiguous (only one interpretation possible); every child masters before moving on.
- Characteristic moves: faultless communication / clear examples-and-nonexamples; scripted rapid pacing; anticipate and pre-specify error corrections; unison-response-style checks (adapt to self-paced: forced-response checks).
- Pushes AGAINST: "against Elbow/discovery openness (minimal guidance fails novices)"; "against TSIS's flexible templates where a step could be misread."
- Evidence grade: `A` for explicit-instruction principle (KB L1 / How Teaching Happens); DI-specific `B`.
- Source anchors: `ToI p.NN` (Theory of Instruction) + `KB` ≥4.
- Tell: "If a student can misread it, the design is broken."

- [ ] **Step 3: Kirschner/Hendrick brief**

Fill `personas/05-kirschner-hendrick.md` from `hlh.txt` + KB L1:
- Core commitments: working memory is the bottleneck; novices need guidance not discovery; prior knowledge is the biggest factor; performance ≠ learning (desirable difficulties).
- Characteristic moves: worked examples for novices; fade with expertise (expertise reversal); retrieval practice + spacing; integrate not split; remove redundancy for experts.
- Pushes AGAINST: "against unscaffolded discovery/blank-page tasks"; "against one-and-done teaching (no spacing)"; "against learning-styles matching."
- Evidence grade: `A` (KB L1 meta-analyses: expertise reversal d=0.505/-0.428; spacing g=0.74).
- Source anchors: `HLH p.NN`, `KB 00 §1.2/§1.3/§1.4` ≥4.
- Tell: "What is this design asking working memory to hold at once?"

- [ ] **Step 4: Acceptance check (both briefs)**

Run the Task-4 loop with F=`04-di-engelmann` and `05-kirschner-hendrick`. Expected each: `6`, `>=4`, `>=1`.

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat(council): DI + Kirschner/Hendrick persona briefs" || echo "skill dir outside repo — delivered in place"
```

---

### Task 6: Build Yeager brief

**Files:**
- Create: `.../references/_extraction/yeager.txt`, `.../personas/06-yeager.md`

**Interfaces:**
- Consumes: template, extraction method. Produces: brief 06.

- [ ] **Step 1: Extract**

```bash
cd "c:/Users/noelp/HS Writing"
pdftotext -layout "10 to 25. The Science of Motivating Young People A Groundbreaking Approach to Leading the Next Generation—And Making Your Own... (David Yeager) (Z-Library).pdf" "C:/Users/noelp/.claude/skills/council-of-writing-instruction/references/_extraction/yeager.txt"
wc -l "C:/Users/noelp/.claude/skills/council-of-writing-instruction/references/_extraction/yeager.txt"
```
Expected: non-empty (fallback to pypdf if 0).

- [ ] **Step 2: Yeager brief**

Fill `personas/06-yeager.md` from `yeager.txt` + existing `Learning Science Synthesis for Writing Brainlift.md` §3:
- Core commitments: adolescents are not deficient, they have different motivational priorities (status/respect); the mentor mindset = high standards + high support; achievement often drives motivation (not only reverse).
- Characteristic moves: "wise feedback" ("I have high standards and I believe you can meet them"); transparency about why a task matters; presume agency/autonomy (topic choice); acknowledge difficulty; avoid the compliment sandwich.
- Pushes AGAINST: "against person-praise feedback and controlling tone"; "against low-standards 'protective' framing."
- Evidence grade: `B` (Yeager RCTs; note some mindset replications are contested — flag in the line).
- Source anchors: `10to25 p.NN`, `LSS §3` ≥4.
- Tell: "High standards, high support — say the standard out loud."

- [ ] **Step 3: Acceptance check** — Task-4 loop with F=`06-yeager`. Expected: `6`, `>=4`, `>=1`.

- [ ] **Step 4: Commit**

```bash
git add -A && git commit -m "feat(council): Yeager persona brief" || echo "skill dir outside repo — delivered in place"
```

---

### Task 7: Build Wiliam/Hattie + UbD briefs (KB-grounded)

**Files:**
- Create: `.../personas/07-wiliam-hattie.md`, `.../personas/08-ubd-wiggins-mctighe.md`

**Interfaces:**
- Consumes: template, KB. Produces: briefs 07 and 08. No PDF extraction (KB-grounded).

- [ ] **Step 1: Wiliam/Hattie brief**

Read `Instructional_Design_KB/00_Knowledge_Base.md` §4.1–4.4. Fill `personas/07-wiliam-hattie.md`:
- Core commitments: feedback is a top lever (ES 0.79) but highly variable; grades-alone don't improve learning; formative assessment helps low achievers most; self-assessment is essential but must be trained.
- Characteristic moves: the 3 questions (Where going / Where now / Where next); target the process & self-regulation levels; single-point/analytic rubric choice by purpose; pair self-assessment with feedback + repetition.
- Pushes AGAINST: "against person-praise ('great job!') and grade-only feedback"; "against 'give them the rubric' as sufficient for calibration."
- Evidence grade: `A` (KB 4.1–4.4).
- Source anchors: `KB 00 §4.1/§4.2/§4.4` ≥4.
- Tell: "Where are you going, where are you now, what's the next move?"

- [ ] **Step 2: UbD brief**

Read `Instructional_Design_KB/00_Knowledge_Base.md` §3.1. Fill `personas/08-ubd-wiggins-mctighe.md`:
- Core commitments: plan backward from transfer goals; design the assessment before the activities; align all three stages; rote acquisition doesn't transfer.
- Characteristic moves: Stage 1 desired results → Stage 2 evidence → Stage 3 learning plan; T/M/A coding of activities; authentic performance task as culmination.
- Pushes AGAINST: "against activity-first design"; "against lessons that are all Acquisition with no transfer."
- Evidence grade: `B` (framework; no effect sizes — say so).
- Source anchors: `KB 00 §3.1` ≥3.
- Tell: "What's the transfer goal, and how will we know they hit it?"

- [ ] **Step 3: Acceptance check** — Task-4 loop with F=`07-wiliam-hattie` and `08-ubd-wiggins-mctighe`. (UbD anchor threshold `>=3`.)

- [ ] **Step 4: Commit**

```bash
git add -A && git commit -m "feat(council): Wiliam/Hattie + UbD persona briefs (KB-grounded)" || echo "skill dir outside repo — delivered in place"
```

---

### Task 8: Research + build Hayes & Flower brief

**Files:**
- Create: `.../references/_extraction/hayes-flower-research.md` (research notes w/ URLs)
- Create: `.../personas/09-hayes-flower.md`

**Interfaces:**
- Consumes: template. Produces: brief 09 + a research-notes file (source of anchors, since no book on disk).

- [ ] **Step 1: Research the Hayes-Flower model**

Use WebSearch + WebFetch (or a research subagent) for: "Hayes Flower 1980 cognitive process model of writing", "Hayes 1996 revised model working memory", "planning translating reviewing writing process". Capture in `_extraction/hayes-flower-research.md`: 3–5 sourced claims with URLs — the process components (planning/translating/reviewing), the monitor, working-memory constraints while composing, why novices' processes are not automatized.

- [ ] **Step 2: Hayes & Flower brief**

Fill `personas/09-hayes-flower.md`:
- Core commitments: writing is a set of recursive cognitive processes (plan/translate/review), not linear stages; the processes compete for limited working memory; expert and novice processes differ mainly in orchestration and automaticity.
- Characteristic moves: reduce simultaneous process demands for novices (e.g., separate planning from drafting); build transcription automaticity so WM frees for higher processes; make the recursive nature explicit.
- Pushes AGAINST: "against strictly linear 'stage' writing instruction"; converges with Kirschner/Hendrick on WM but focuses on the composing act itself.
- Evidence grade: `B` (foundational cognitive model; heavily cited, older empirical base).
- Source anchors: URLs from Step 1 (`HF-research #1` etc.) ≥3.
- Tell: "Which process is this lesson overloading — planning, translating, or reviewing?"

- [ ] **Step 3: Acceptance check** — Task-4 loop with F=`09-hayes-flower`; anchors `>=3`; also confirm research file has URLs: `grep -c "http" ".../hayes-flower-research.md"` expect `>=3`.

- [ ] **Step 4: Commit**

```bash
git add -A && git commit -m "feat(council): Hayes & Flower persona brief (researched)" || echo "skill dir outside repo — delivered in place"
```

---

### Task 9: Research + build Elbow/Gallagher (dissent) brief

**Files:**
- Create: `.../references/_extraction/elbow-gallagher-research.md`
- Create: `.../personas/10-elbow-gallagher.md`

**Interfaces:**
- Consumes: template. Produces: brief 10, explicitly fenced as dissent/low-evidence.

- [ ] **Step 1: Research**

WebSearch/WebFetch: "Peter Elbow freewriting voice writing without teachers", "Elbow believing doubting game", "Kelly Gallagher Readicide authentic writing", "Gallagher write like a writer mentor texts". Capture 3–5 sourced claims in `_extraction/elbow-gallagher-research.md` with URLs.

- [ ] **Step 2: Elbow/Gallagher brief (marked dissent)**

Fill `personas/10-elbow-gallagher.md`:
- Core commitments: voice and authentic purpose matter; low-stakes/free writing generates material and reduces fear; over-standardization kills real writing (Gallagher's "readicide"); students should write for real audiences.
- Characteristic moves: freewriting/low-stakes entries; mentor texts over formulas; choice of topic and form; believing-and-doubting.
- Pushes AGAINST: "against DI/TWR over-scripting and mastery-formula gates that squeeze out voice" (this is its whole job).
- Evidence grade: **`dissent (low-evidence)`** — say plainly: weak experimental base; included as a voice/authenticity check, not an authority. This matches spec §5.1 (fenced as dissent, never an evidence winner).
- Source anchors: URLs from Step 1 ≥3.
- Tell: "Yes, but where is the student's own voice in this?"

- [ ] **Step 3: Acceptance check** — Task-4 loop with F=`10-elbow-gallagher`; PLUS confirm dissent fence: `grep -ci "dissent" ".../personas/10-elbow-gallagher.md"` expect `>=1`.

- [ ] **Step 4: Commit**

```bash
git add -A && git commit -m "feat(council): Elbow/Gallagher dissent persona brief (researched)" || echo "skill dir outside repo — delivered in place"
```

---

### Task 10: Build the Synthesis Judge brief

**Files:**
- Create: `.../personas/judge.md`

**Interfaces:**
- Consumes: `roster.md` (Task 2), all persona briefs, KB. Produces: `judge.md` — the CONVENE + ADJUDICATE logic the orchestrator invokes.

- [ ] **Step 1: Write `judge.md`**

Sections (this brief is structural, not the persona template):
- `## Role`: convene the panel, then adjudicate — never average.
- `## CONVENE`: read topic/draft → consult `roster.md` cues → pick 4–6 seats with genuine stake → output convened + benched + one-line bench reason. Honor `--seats`/`--all` overrides.
- `## ADJUDICATE — tie-break rule` (verbatim from spec §5.1):
  1. Evidence grade first (A > B > C).
  2. Lesson goal second.
  3. Novice-support asymmetry third (prefer more support for novices; KB §1.2).
  4. Elbow/Gallagher = dissent, never an evidence winner; surfaces as "voice/authenticity risks to weigh."
- `## For each conflict`: state the tension (Seat A wants X vs Seat B wants Y) → apply rule → name the losing position (never silently drop).
- `## EMIT`: dispatch to the mode template (design draft or review list).

- [ ] **Step 2: Acceptance check — judge encodes the non-averaging rule**

Run:
```bash
J="C:/Users/noelp/.claude/skills/council-of-writing-instruction/personas/judge.md"
grep -cE "CONVENE|ADJUDICATE|EMIT" "$J"          # expect >=3
grep -ci "average" "$J"                          # expect >=1 (the 'never average' instruction)
grep -ci "evidence grade" "$J"                   # expect >=1 (tie-break rule present)
grep -ci "losing position" "$J"                  # expect >=1
```
Expected: `>=3`, `>=1`, `>=1`, `>=1`.

- [ ] **Step 3: Commit**

```bash
git add -A && git commit -m "feat(council): synthesis judge (convene + non-averaging adjudication)" || echo "skill dir outside repo — delivered in place"
```

---

### Task 11: Output templates (design draft + review list)

**Files:**
- Create: `.../references/output-templates.md`

**Interfaces:**
- Consumes: nothing new. Produces: the two artifact shapes the judge's EMIT step fills. Contract: a `## DESIGN MODE OUTPUT` section and a `## REVIEW MODE OUTPUT` section.

- [ ] **Step 1: Write `output-templates.md`**

```markdown
# Council Output Templates

## DESIGN MODE OUTPUT  (emit for `design`)
- **Lesson objective / target skill:** …
- **Named strategy (+ mnemonic if any):** …
- **Model (worked example + coping think-aloud):** …
- **Guided practice → independent (with fade trigger = demonstrated performance):** …
- **Assessment + feedback move (process-level):** …
- **Spacing/retrieval hook (where this recurs):** …
- **Council provenance:** which seat contributed each element.
- **Dissents noted:** voice/authenticity risks flagged by Elbow/Gallagher.
- (NO em dashes in this emitted lesson content — house rule.)

## REVIEW MODE OUTPUT  (emit for `review`)
Prioritized, deduplicated list. Each item:
| Priority (P1/P2/P3) | Issue | Raised by (seat) | Fix | Source anchor |
Followed by:
- **Conflicts adjudicated:** tension → ruling → losing position named.
- **Dissents noted:** Elbow/Gallagher voice risks (weigh, not blocking).
```

- [ ] **Step 2: Acceptance check**

```bash
grep -cE "^## (DESIGN MODE OUTPUT|REVIEW MODE OUTPUT)" "C:/Users/noelp/.claude/skills/council-of-writing-instruction/references/output-templates.md"
```
Expected: `2`

- [ ] **Step 3: Commit**

```bash
git add -A && git commit -m "feat(council): design + review output templates" || echo "skill dir outside repo — delivered in place"
```

---

### Task 12: SKILL.md orchestrator

**Files:**
- Create: `.../SKILL.md`

**Interfaces:**
- Consumes: every prior file (roster, personas, judge, templates).
- Produces: the entry point. Frontmatter + the 4-step flow + mode detection + overrides.

- [ ] **Step 1: Write the frontmatter**

```markdown
---
name: council-of-writing-instruction
version: 1.0.0
description: |
  Convenes a council of source-grounded writing/instruction pedagogy personas
  (TWR, SRSD, TSIS, DI/Engelmann, Kirschner & Hendrick, Yeager, Wiliam & Hattie,
  UbD, Hayes & Flower, Elbow/Gallagher) plus a synthesis judge to DESIGN a new
  writing lesson or REVIEW a draft one. The judge convenes only relevant seats
  and adjudicates their disagreements by evidence, never averaging. Use when
  asked to "convene the council", "council review this lesson", "council design",
  or "what would the writing experts say".
triggers:
  - convene the council
  - council of writing instruction
  - council review
  - council design
  - what would the writing experts say
allowed-tools:
  - Read
  - Glob
  - Grep
  - Agent
  - Write
  - Bash
---
```

- [ ] **Step 2: Write the orchestration body**

Sections:
- `## What this is` — one paragraph; points to the spec + `Instructional_Design_KB/`.
- `## Modes & invocation` — `design <topic|outline>` / `review <draft-file>`; mode detection (first token; else readable-file→review, else design); `--seats id,id` and `--all` overrides.
- `## Runtime flow` — the 4 steps, each pointing at the file that implements it:
  1. **Convene** — load `references/roster.md`, apply `personas/judge.md` CONVENE. Announce convened + benched + reason.
  2. **Deliberate** — for each convened seat, dispatch a parallel Agent whose prompt = that seat's `personas/NN-*.md` brief + the lesson/topic + this required structured return: `{take, source_anchors[], named_disagreement_with}`. All convened seats dispatched in ONE message (parallel).
  3. **Adjudicate** — pass all deliberations to a single judge Agent using `personas/judge.md` ADJUDICATE + tie-break rule.
  4. **Emit** — judge fills the matching section of `references/output-templates.md`.
- `## Provenance rule` — every persona claim must carry a source anchor; drop unanchored claims.
- `## Guardrails` — divergence requirement (if all convened seats agree, say so and note it as a signal, don't manufacture conflict); no fabricated quotes; em-dash ban in emitted lesson content.

- [ ] **Step 3: Acceptance check — frontmatter + flow present**

```bash
S="C:/Users/noelp/.claude/skills/council-of-writing-instruction/SKILL.md"
grep -cE "^name: council-of-writing-instruction" "$S"     # expect 1
grep -cE "Convene|Deliberate|Adjudicate|Emit" "$S"        # expect >=4
grep -ci "parallel" "$S"                                  # expect >=1
grep -ci "seats" "$S"                                     # expect >=1 (override documented)
```
Expected: `1`, `>=4`, `>=1`, `>=1`.

- [ ] **Step 4: Commit**

```bash
git add -A && git commit -m "feat(council): SKILL.md orchestrator (convene/deliberate/adjudicate/emit)" || echo "skill dir outside repo — delivered in place"
```

---

### Task 13: End-to-end acceptance trial on a real lesson

This is the real test of the spec's success criteria. No new files; it exercises the whole skill and captures evidence.

**Files:**
- Create: `.../references/_extraction/trial-review-L1.md` (captured trial output — scratch/evidence)

**Interfaces:**
- Consumes: the whole skill. Produces: pass/fail evidence against spec §1 success criteria.

- [ ] **Step 1: Run REVIEW mode on the test lesson**

Invoke the skill's flow manually against `Course review/L1_activity_corrected.html`:
- Judge CONVENE → record convened + benched seats + reasons.
- Dispatch convened personas in parallel with their briefs.
- Judge ADJUDICATE → emit review list.
Save the full output to `_extraction/trial-review-L1.md`.

- [ ] **Step 2: Acceptance check — divergence (spec success criterion 1)**

Confirm in the captured output: at least 2 convened personas raised DIFFERENT issues, and at least one named a disagreement with another seat. If all personas agreed on everything → FAIL: revisit the `Pushes AGAINST` fields (Tasks 3–9) and the deliberation prompt (Task 12) to sharpen divergence. Record result.

- [ ] **Step 3: Acceptance check — adjudication (criterion 2)**

Confirm the judge output NAMES at least one losing position and cites the tie-break rule (evidence grade / lesson goal). If it averaged → FAIL: sharpen `judge.md` (Task 10). Record result.

- [ ] **Step 4: Acceptance check — provenance (criterion 3)**

Confirm every persona claim in the output carries a source anchor. Grep the trial file: `grep -cE "p\.|KB |http|research" trial-review-L1.md` should be comfortably positive and no claim should be anchor-free. Record result.

- [ ] **Step 5: Run DESIGN mode smoke test**

Invoke `design "G9 U1: taking a defensible position"`. Confirm it emits the DESIGN MODE OUTPUT template filled, with council provenance and dissents-noted, and NO em dashes. Record result.

- [ ] **Step 6: Fix-and-rerun loop**

If any check failed, fix the responsible file and re-run Steps 1–5 for that mode. Repeat until criteria 1–3 pass in review and the design smoke test emits a valid draft.

- [ ] **Step 7: Commit the trial evidence**

```bash
git add -A && git commit -m "test(council): end-to-end trial on L1 (divergence/adjudication/provenance verified)" || echo "skill dir outside repo — delivered in place"
```

---

### Task 14: Memory pointer + spec/plan cross-link

**Files:**
- Create: `C:\Users\noelp\.claude\projects\c--Users-noelp-HS-Writing\memory\council-of-writing-instruction.md`
- Modify: `C:\Users\noelp\.claude\projects\c--Users-noelp-HS-Writing\memory\MEMORY.md` (add one pointer line)

**Interfaces:**
- Consumes: the finished skill. Produces: durable recall.

- [ ] **Step 1: Write the memory file**

`type: project`. One-liner: council skill built, where it lives, its two modes, that it front-ends the ID KB, and the tie-break rule. Link `[[instructional-design-kb]]` and `[[srsd-mnemonic-decision]]`.

- [ ] **Step 2: Add MEMORY.md pointer line** under Active Work:

`- [Council of Writing Instruction skill](council-of-writing-instruction.md) — 10 grounded pedagogy personas + synthesis judge; design & review modes; front-ends [[instructional-design-kb]]; smart-panel convening + non-averaging tie-break`

- [ ] **Step 3: Commit**

```bash
cd "c:/Users/noelp/HS Writing"
git add -A && git commit -m "docs(council): memory pointer + index"
```

---

## Self-Review

**1. Spec coverage:**
- §2 modes (design/review + detection + overrides) → Tasks 12, 13. ✓
- §3 roster (10 seats + judge) → Tasks 2–10. ✓
- §4 hybrid grounding (book/KB/research tiers + fixed template) → Tasks 1, 3–10. ✓
- §5 runtime flow (convene→deliberate→adjudicate→emit) → Task 12; judge logic Task 10. ✓
- §5.1 tie-break rule (verbatim) → Task 10. ✓
- §5.2 voice discipline / source-tagging → Task 12 provenance + every brief's Source anchors. ✓
- §6 file layout → File Structure section + task file paths. ✓
- §7 build plan (extraction, research, orchestration, test) → Tasks 3–13. ✓
- §8 risks (divergence, non-averaging, cost, provenance, weak seats 9–10 fenced) → Tasks 9, 10, 13 acceptance checks. ✓
- Success criteria 1–5 → Task 13 trial checks. ✓

**2. Placeholder scan:** No "TBD/TODO". Each brief task specifies exact sections, anchor thresholds, and the concrete content to source. Acceptance checks are runnable commands with expected values. ✓

**3. Type consistency:** Seat IDs (`twr, srsd, tsis, di, kh, yeager, wh, ubd, hf, eg`) are consistent between `roster.md` (Task 2), `--seats` (Task 12), and judge CONVENE (Task 10). Brief file numbering `01–10` + `judge.md` consistent between File Structure, roster table, and each task's output path. The six brief section headers are identical everywhere (Task 1 template → all brief tasks → acceptance greps). ✓

**Known adaptation (flagged honestly):** this is a markdown/prompt skill, so tasks use acceptance checks (grep/structural/trial) instead of unit tests, and the "failing test first" TDD rhythm doesn't apply to prose extraction. Task 13 is the genuine behavioral test (divergence/adjudication/provenance on a real lesson). One open runtime caveat: the skill directory is outside the git repo root, so per-task commits may not be possible from the repo — each commit step has a fallback and the skill is "delivered in place" regardless; only the repo-side plan/spec/memory changes are guaranteed committed.
