# Simulated-Student Curriculum Evaluation Harness (G9 pilot) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a standalone Python harness in which LLM "students" (Fable-5 and OpenAI), with no knowledge of the course's development, walk the G9 course in sequence, attempt every task, take the test, and produce a report answering the four curriculum questions.

**Architecture:** Six focused modules under `pipeline/sim_student_eval/`. A course loader renders each G9 v3.1 lesson to a development-free student view (reusing `lesson_review.render_student_experience`). Each of 4 course-walks (2 models × 2 personas) processes lessons in order, carrying a bounded on-disk JSON "learner journal" as its only memory — the next lesson sees `persona + journal + rendered lesson`, never prior raw transcripts. Composition probes and a test-readiness pass produce evidence; a Claude analyst synthesizes a corroborated report. No writing is scored.

**Tech Stack:** Python 3.14, `anthropic` 0.84.0 (installed, `claude-fable-5`), `openai` (NOT installed — Task 0 installs it), stdlib (`json`, `glob`, `importlib`, `argparse`, `os`, `re`). No new frameworks.

## Global Constraints

- **No writing scores.** Writing (FRQ/CR/essay) is NEVER rubric-scored. Findings are lived experience + deterministic MCQ answer-vs-key only. (Spec §2, §6.)
- **No knowledge of development.** Student agents receive ONLY `render_student_experience(L)` output — never the `Lesson` object, `.py` source, gate names, KC tags, or internal labels. Hard architectural boundary. (Spec §3.)
- **No em dashes** in any generated doc/report (Noel standing rule). Use commas, colons, parens.
- **Anti-slop.** Report findings must be specific and traceable to a student utterance + lesson/step, never generic ("could be clearer"). (Spec §6.)
- **Never echo API keys.** Read from `HS Writing/.env` (`ANTHROPIC_API_KEY`, `OPEN_AI_API_KEY`); never print them. Follow the `lesson_review._load_env_key` pattern.
- **Coverage ≠ efficacy.** The report states at the top that 4 simulated students are design signal, not field data.
- **All paths are relative to the pipeline dir** `Alpha HS Writing Course 2026-27/pipeline/` unless absolute. The repo root for lessons is `os.path.join(HERE, "..")`.
- **Verify by exit code / actual output, never self-report** (project discipline).

### Verified interfaces (do not re-derive)

- `lesson_review.render_student_experience(L) -> str` — the dev-free student view. Imports at module load pull in `g9_push_dryrun` (sets `STIM` registry) and `gated_reading`; importing `lesson_review` is sufficient to make `render_student_experience` work. Verified end-to-end on `lesson_g9_l09_warrant_v3_1.py` (produces "STEP 1 (TEACH...)" ... 21142 chars, no source code).
- Lesson loader (from `g9_assemble_v3_1.py:78-82`): `sorted(glob.glob(os.path.join(ROOT, "Lesson_Bank_G9", "lesson_g9_l*_v3_1.py")))` → `importlib` load each → `getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0]`. Filename number `l01..l27` = sequence order.
- `Lesson` dataclass fields (used, read-only): `.id` (e.g. `ACC-W910-L-G9-C903-0011`), `.title`, `.lesson_type` (int 1..8), `.slots` (list), `.mastery` (dict — EMPTY on the object; real mastery lives in `mastery_prompts_g9.MASTERY[L.id]` with fields `source, unit, rubric_ref, prompt_html`), `.lesson_class` ("practice"|"gate").
- `mastery_prompts_g9.MASTERY` — dict keyed by lesson id; entry fields `source, unit, rubric_ref, prompt_html`. (Not needed by students; the harness does not surface mastery to students in the pilot — mastery is the held-out grader instrument, out of scope for lived-experience.)
- `Item` dataclass (`item_contract.py`): `.id, .grade, .stem, .qti_type, .subskill_or_mode, .options (list[Option]), .answer_key (list[str]), .stimulus_ref, .rubric_ref`. `Option`: `.id, .text, .correct (bool), .rationale`.
- Item banks: `Item_Bank_G9/*.py` each expose `ITEMS` (list of `Item`). CR files (`cr_argument`, `cr_analysis`, `cr_explanatory`) = `extended-text` (no options). SR files (`sr_*`) = `choice`/`hottext` (have options + answer_key). `pp100_*` = MCQ.
- Anthropic call template (`lesson_review.fable_review:163-201`): `client = anthropic.Anthropic(api_key=key)`; `client.messages.create(model="claude-fable-5", max_tokens=..., tools=[tool], tool_choice={"type":"tool","name":...}, messages=[{"role":"user","content":prompt}])`; read the `tool_use` block's `.input`.
- `model_test_g9.html` = rendered form, ~7 `choice` items (thin). The fuller test surface is `Item_Bank_G9`.

### File structure

```
pipeline/sim_student_eval/
  __init__.py       # empty; makes it a package
  personas.py       # PERSONAS dict: persona_id -> {label, system_preamble}. Task 2.
  models.py         # StudentClient protocol + FableClient + GptClient (structured output). Tasks 3-4.
  journal.py        # JournalStore: append/read/validate bounded journal entries. Task 1.
  render_course.py  # load_g9_lessons() + student_view(L). Task 5.
  student_agent.py  # walk_lesson(client, persona, view, journal_so_far) -> (transcript, journal_update). Task 6.
  test_taker.py     # load_g9_test_items() + take_test(client, persona, items, journal) -> attempt log. Task 7.
  analyst.py        # synthesize(all_walk_dirs) -> report markdown. Task 8.
  run_eval.py        # orchestrator CLI. Task 9.
tests/sim_student_eval/
  test_journal.py       # Task 1
  test_render_course.py # Task 5
  test_test_taker.py    # Task 7
  test_smoke.py         # Task 10 (offline, mocked clients)
```

Outputs land in `pipeline/sim_student_eval/out/<run_id>/`:
`journal_<persona>_<model>.jsonl`, `transcript_<persona>_<model>.jsonl`, `test_<persona>_<model>.json`, and `SIM_STUDENT_EVAL_G9.md`.

---

## Task 0: Environment setup

**Files:**
- Create: `pipeline/sim_student_eval/__init__.py` (empty)
- Create: `tests/sim_student_eval/__init__.py` (empty)

- [ ] **Step 1: Install the OpenAI SDK**

Run (from `Alpha HS Writing Course 2026-27/`):
```bash
python -m pip install openai
```
Expected: installs `openai` (any recent 1.x). Verify:
```bash
python -c "import openai; print('openai', openai.__version__)"
```
Expected: prints a version, no ModuleNotFoundError.

- [ ] **Step 2: Confirm anthropic + bs4 present**

Run:
```bash
python -c "import anthropic, bs4; print('anthropic', anthropic.__version__, '| bs4 ok')"
```
Expected: `anthropic 0.84.0 | bs4 ok`.

- [ ] **Step 3: Create empty package files**

Create `pipeline/sim_student_eval/__init__.py` with a single line:
```python
"""Simulated-student curriculum evaluation harness (G9 pilot). See docs/superpowers/plans/2026-07-16-simulated-student-curriculum-eval.md."""
```
Create `tests/sim_student_eval/__init__.py` empty.

- [ ] **Step 4: Confirm pytest available**

Run:
```bash
python -m pytest --version
```
Expected: prints a pytest version. If missing: `python -m pip install pytest`.

- [ ] **Step 5: Commit**

```bash
git add pipeline/sim_student_eval/__init__.py tests/sim_student_eval/__init__.py
git commit -m "chore(sim-student-eval): scaffold package + install openai SDK"
```

---

## Task 1: Journal store (the external bounded memory)

**Files:**
- Create: `pipeline/sim_student_eval/journal.py`
- Test: `tests/sim_student_eval/test_journal.py`

**Interfaces:**
- Produces:
  - `validate_entry(entry: dict) -> dict` — returns a shape-normalized copy: ensures keys `lesson, seq, skills_i_can_now_do (list), terms_learned (list), where_i_struggled (list), felt_repeated (dict|None), open_questions (list), confidence (dict)`; truncates each list to 12 items and each string to 400 chars; coerces missing keys to defaults. Raises `ValueError` if `lesson` or `seq` missing.
  - `class JournalStore(path: str)` with:
    - `.append(entry: dict) -> None` — validate then append one JSON line to `path`.
    - `.entries() -> list[dict]` — read all lines back as dicts (empty list if file absent).
    - `.digest() -> str` — a compact human-readable running memory string built from all entries so far, for feeding to the next lesson call. Format below.

- [ ] **Step 1: Write the failing test**

```python
# tests/sim_student_eval/test_journal.py
import os, sys, json, tempfile
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "..", "Alpha HS Writing Course 2026-27", "pipeline"))
from sim_student_eval.journal import validate_entry, JournalStore


def test_validate_fills_defaults_and_requires_lesson():
    e = validate_entry({"lesson": "g9_l01", "seq": 1})
    assert e["skills_i_can_now_do"] == []
    assert e["felt_repeated"] is None
    assert e["confidence"] == {}
    import pytest
    with pytest.raises(ValueError):
        validate_entry({"seq": 1})


def test_validate_truncates_long_lists_and_strings():
    e = validate_entry({"lesson": "x", "seq": 2,
                        "open_questions": ["q"] * 50,
                        "where_i_struggled": ["z" * 999]})
    assert len(e["open_questions"]) == 12
    assert len(e["where_i_struggled"][0]) == 400


def test_store_append_and_readback():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "j.jsonl")
        s = JournalStore(p)
        assert s.entries() == []
        s.append({"lesson": "g9_l01", "seq": 1, "skills_i_can_now_do": ["state a claim"]})
        s.append({"lesson": "g9_l02", "seq": 2, "felt_repeated": {"echoes_lesson": "g9_l01", "what": "claim again"}})
        rows = s.entries()
        assert len(rows) == 2
        assert rows[1]["felt_repeated"]["echoes_lesson"] == "g9_l01"


def test_digest_is_compact_and_mentions_prior_skills():
    with tempfile.TemporaryDirectory() as d:
        s = JournalStore(os.path.join(d, "j.jsonl"))
        s.append({"lesson": "g9_l01", "seq": 1, "skills_i_can_now_do": ["state a claim"],
                  "confidence": {"claim": 0.8}})
        dig = s.digest()
        assert "state a claim" in dig
        assert "g9_l01" in dig
        assert len(dig) < 4000  # bounded
```

- [ ] **Step 2: Run test to verify it fails**

Run (from `Alpha HS Writing Course 2026-27/`):
```bash
python -m pytest ../../tests/sim_student_eval/test_journal.py -v
```
Expected: FAIL — `ModuleNotFoundError: No module named 'sim_student_eval.journal'`.

> Note: tests add `pipeline/` to `sys.path`, so `sim_student_eval` is importable as a package. Run pytest from the course dir; the test file computes its own paths.

- [ ] **Step 3: Write minimal implementation**

```python
# pipeline/sim_student_eval/journal.py
"""The external, bounded, on-disk learner memory. One JSON line per lesson.
This is the ONLY memory carried between lessons (no raw transcripts), so context
stays constant-size and every downstream finding traces to an inspectable entry."""
import json, os

_LIST_KEYS = ("skills_i_can_now_do", "terms_learned", "where_i_struggled", "open_questions")
_MAX_LIST = 12
_MAX_STR = 400


def _clip_str(s):
    return str(s)[:_MAX_STR]


def validate_entry(entry: dict) -> dict:
    if "lesson" not in entry or "seq" not in entry:
        raise ValueError("journal entry needs 'lesson' and 'seq'")
    out = {"lesson": str(entry["lesson"]), "seq": int(entry["seq"])}
    for k in _LIST_KEYS:
        vals = entry.get(k) or []
        if not isinstance(vals, list):
            vals = [vals]
        out[k] = [_clip_str(v) for v in vals[:_MAX_LIST]]
    fr = entry.get("felt_repeated")
    if isinstance(fr, dict) and fr.get("echoes_lesson"):
        out["felt_repeated"] = {"echoes_lesson": _clip_str(fr.get("echoes_lesson", "")),
                                "what": _clip_str(fr.get("what", ""))}
    else:
        out["felt_repeated"] = None
    conf = entry.get("confidence") or {}
    out["confidence"] = {str(k)[:60]: float(v) for k, v in conf.items()
                         if isinstance(v, (int, float))} if isinstance(conf, dict) else {}
    return out


class JournalStore:
    def __init__(self, path: str):
        self.path = path

    def append(self, entry: dict) -> None:
        e = validate_entry(entry)
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    def entries(self) -> list:
        if not os.path.exists(self.path):
            return []
        rows = []
        for line in open(self.path, encoding="utf-8"):
            line = line.strip()
            if line:
                rows.append(json.loads(line))
        return rows

    def digest(self) -> str:
        """A compact running-memory string for the NEXT lesson call. Bounded: only the
        cumulative skill list, current confidence, and the last 5 lessons' struggles/questions."""
        rows = self.entries()
        if not rows:
            return "(You are starting the course. You have learned nothing yet.)"
        skills = []
        conf = {}
        for r in rows:
            for s in r.get("skills_i_can_now_do", []):
                if s not in skills:
                    skills.append(s)
            conf.update(r.get("confidence", {}))
        recent = rows[-5:]
        lines = ["LESSONS DONE: " + ", ".join(r["lesson"] for r in rows)]
        lines.append("SKILLS I CAN DO: " + ("; ".join(skills[:20]) or "none yet"))
        lines.append("MY CONFIDENCE: " + ("; ".join(f"{k}={v:.1f}" for k, v in list(conf.items())[:15]) or "n/a"))
        struggles = [s for r in recent for s in r.get("where_i_struggled", [])]
        if struggles:
            lines.append("RECENT STRUGGLES: " + "; ".join(struggles[:6]))
        opens = [q for r in recent for q in r.get("open_questions", [])]
        if opens:
            lines.append("MY OPEN QUESTIONS: " + "; ".join(opens[:6]))
        return "\n".join(lines)[:4000]
```

- [ ] **Step 4: Run test to verify it passes**

Run:
```bash
python -m pytest ../../tests/sim_student_eval/test_journal.py -v
```
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add pipeline/sim_student_eval/journal.py tests/sim_student_eval/test_journal.py
git commit -m "feat(sim-student-eval): bounded on-disk learner journal store"
```

---

## Task 2: Persona definitions

**Files:**
- Create: `pipeline/sim_student_eval/personas.py`

**Interfaces:**
- Produces: `PERSONAS: dict[str, dict]` where each value has `label: str` and `system_preamble: str`. Keys for the pilot: `"average"`, `"achiever"`. Each preamble is an in-character student brief. It must NOT mention curriculum design, rubrics, gates, or that this is an evaluation — the student thinks they are learning.

- [ ] **Step 1: Write the implementation**

```python
# pipeline/sim_student_eval/personas.py
"""Student personas for the sim-student eval. Each is an in-character brief. The student
believes it is a real 9th grader learning to write; it has NO idea this is a curriculum
evaluation, sees NO design internals. The average student is the readiness signal; the
high-achiever is the sharpest redundancy detector (confirmed in the L01 evals)."""

_COMMON = (
    "You are a 9th-grade student (about 14 years old) taking a self-paced online writing "
    "course. You work ALONE: there is no teacher to ask. You read each lesson and do exactly "
    "what it asks. You have never seen this course before and know nothing about how it was "
    "made. Speak in the first person, like a real student thinking out loud. Be honest: if "
    "something is confusing, boring, or repeats something you already did, say so plainly."
)

PERSONAS = {
    "average": {
        "label": "On-grade average G9 student",
        "system_preamble": _COMMON + " " + (
            "You are a typical incoming 9th grader. You can write a basic five-paragraph "
            "essay from school, but you have NOT been taught to analyze texts or build a "
            "formal argument with evidence and reasoning. You are motivated enough to finish, "
            "but you get lost when a step assumes knowledge you do not have. When you cannot "
            "do a task, say exactly what you are missing rather than faking it."
        ),
    },
    "achiever": {
        "label": "High-achieving / fast learner",
        "system_preamble": _COMMON + " " + (
            "You are a strong reader who picks up new skills fast and gets impatient with "
            "busywork. Once you understand something, being made to redo it feels like a "
            "waste of time. You are the kind of student who notices when a lesson is teaching "
            "something an earlier lesson already taught, and you will name which earlier "
            "lesson it repeats. You still do every task, but you flag repetition and padding."
        ),
    },
}
```

- [ ] **Step 2: Verify it imports and has both personas**

Run (from `Alpha HS Writing Course 2026-27/pipeline/`):
```bash
python -c "from sim_student_eval.personas import PERSONAS; print(sorted(PERSONAS)); assert 'design' not in str(PERSONAS).lower() and 'rubric' not in str(PERSONAS).lower(); print('no design/rubric leak OK')"
```
Expected: `['achiever', 'average']` then `no design/rubric leak OK`.

- [ ] **Step 3: Commit**

```bash
git add pipeline/sim_student_eval/personas.py
git commit -m "feat(sim-student-eval): average + high-achiever G9 personas"
```

---

## Task 3: Model client protocol + Fable (Anthropic) student

**Files:**
- Create: `pipeline/sim_student_eval/models.py`

**Interfaces:**
- Produces:
  - `STUDENT_TOOL: dict` — the JSON tool schema forcing structured student output. Shape: an object with `response` (string — what the student writes/answers, in character) and `journal_update` (object with the journal fields from Task 1's `validate_entry`).
  - `class FableClient(api_key: str, model: str = "claude-fable-5")` with `.name -> str` (returns `"fable"`) and `.ask(system: str, user: str) -> dict` returning `{"response": str, "journal_update": dict}` by forcing a `report_student_turn` tool call.
  - `load_keys() -> dict` — reads `ANTHROPIC_API_KEY` and `OPEN_AI_API_KEY` from `HS Writing/.env` (following `lesson_review._load_env_key`), returns `{"anthropic": "...", "openai": "..."}`; never prints them.

- [ ] **Step 1: Write the implementation**

```python
# pipeline/sim_student_eval/models.py
"""Thin model clients used AS STUDENTS. Both Fable-5 (Anthropic) and GPT (OpenAI) implement
the same .ask(system, user) -> {response, journal_update} contract via forced structured output,
so journal updates are always machine-valid (never free-text JSON parsing)."""
import os

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..", "..")  # -> Alpha HS Writing Course 2026-27/


def _read_env_val(names):
    for base in (os.path.join(ROOT, ".env"), os.path.join(ROOT, "..", ".env")):
        if os.path.exists(base):
            for line in open(base, encoding="utf-8"):
                line = line.strip()
                for n in names:
                    if line.startswith(n) and "=" in line:
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
    for n in names:
        if os.environ.get(n):
            return os.environ[n]
    return ""


def load_keys() -> dict:
    return {"anthropic": _read_env_val(["ANTHROPIC_API_KEY"]),
            "openai": _read_env_val(["OPEN_AI_API_KEY", "OPENAI_API_KEY"])}


_JOURNAL_SCHEMA = {
    "type": "object",
    "properties": {
        "skills_i_can_now_do": {"type": "array", "items": {"type": "string"}},
        "terms_learned": {"type": "array", "items": {"type": "string"}},
        "where_i_struggled": {"type": "array", "items": {"type": "string"}},
        "felt_repeated": {
            "type": "object",
            "properties": {"echoes_lesson": {"type": "string"}, "what": {"type": "string"}},
        },
        "open_questions": {"type": "array", "items": {"type": "string"}},
        "confidence": {"type": "object", "additionalProperties": {"type": "number"}},
    },
    "required": ["skills_i_can_now_do", "where_i_struggled", "open_questions", "confidence"],
}

STUDENT_TOOL = {
    "name": "report_student_turn",
    "description": "Report what you did on this lesson and update your running memory.",
    "input_schema": {
        "type": "object",
        "properties": {
            "response": {"type": "string",
                         "description": "In character: your answers to the checks, your attempt at "
                                        "the writing tasks, and your honest reactions."},
            "journal_update": _JOURNAL_SCHEMA,
        },
        "required": ["response", "journal_update"],
    },
}


class FableClient:
    def __init__(self, api_key: str, model: str = "claude-fable-5"):
        import anthropic
        self._c = anthropic.Anthropic(api_key=api_key)
        self._model = model

    @property
    def name(self) -> str:
        return "fable"

    def ask(self, system: str, user: str) -> dict:
        r = self._c.messages.create(
            model=self._model, max_tokens=3000, system=system,
            tools=[STUDENT_TOOL], tool_choice={"type": "tool", "name": "report_student_turn"},
            messages=[{"role": "user", "content": user}])
        for b in r.content:
            if getattr(b, "type", "") == "tool_use" and getattr(b, "name", "") == "report_student_turn":
                return dict(b.input)
        return {"response": "", "journal_update": {}, "error": "no tool call"}
```

- [ ] **Step 2: Verify import + key load (no network)**

Run (from `pipeline/`):
```bash
python -c "from sim_student_eval.models import load_keys, STUDENT_TOOL, FableClient; k=load_keys(); print('anthropic key present:', bool(k['anthropic'])); print('openai key present:', bool(k['openai'])); print('tool name:', STUDENT_TOOL['name'])"
```
Expected: both keys present `True` (they are in `.env`), tool name `report_student_turn`. The keys themselves must NOT appear in output.

- [ ] **Step 3: Commit**

```bash
git add pipeline/sim_student_eval/models.py
git commit -m "feat(sim-student-eval): Fable client + student structured-output tool + key loader"
```

---

## Task 4: OpenAI (GPT) student client

**Files:**
- Modify: `pipeline/sim_student_eval/models.py`

**Interfaces:**
- Consumes: `STUDENT_TOOL` (Task 3).
- Produces: `class GptClient(api_key: str, model: str = "gpt-5.5")` with `.name -> "gpt"` and the same `.ask(system, user) -> {"response": str, "journal_update": dict}` contract, using OpenAI function-calling (tool) with the same schema so output is structured identically.

- [ ] **Step 1: Add the GptClient to models.py**

Append to `pipeline/sim_student_eval/models.py`:
```python
class GptClient:
    def __init__(self, api_key: str, model: str = "gpt-5.5"):
        import openai
        self._c = openai.OpenAI(api_key=api_key)
        self._model = model

    @property
    def name(self) -> str:
        return "gpt"

    def ask(self, system: str, user: str) -> dict:
        import json as _json
        tool = {"type": "function", "function": {
            "name": STUDENT_TOOL["name"], "description": STUDENT_TOOL["description"],
            "parameters": STUDENT_TOOL["input_schema"]}}
        r = self._c.chat.completions.create(
            model=self._model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            tools=[tool], tool_choice={"type": "function", "function": {"name": STUDENT_TOOL["name"]}},
            max_completion_tokens=3000)
        msg = r.choices[0].message
        if msg.tool_calls:
            return dict(_json.loads(msg.tool_calls[0].function.arguments))
        return {"response": msg.content or "", "journal_update": {}, "error": "no tool call"}
```

> Note on model id: `gpt-5.5` is the current OpenAI model referenced in the Platform3 ai-grading-audit rows (build log). If `run_eval.py` reports an invalid-model error at run time, the model id is a `--gpt-model` CLI override (Task 9) — do not hardcode a fallback here.

- [ ] **Step 2: Verify import**

Run (from `pipeline/`):
```bash
python -c "from sim_student_eval.models import GptClient; print('GptClient import OK')"
```
Expected: `GptClient import OK`.

- [ ] **Step 3: Commit**

```bash
git add pipeline/sim_student_eval/models.py
git commit -m "feat(sim-student-eval): OpenAI GPT student client (same structured contract)"
```

---

## Task 5: Course loader + student view

**Files:**
- Create: `pipeline/sim_student_eval/render_course.py`
- Test: `tests/sim_student_eval/test_render_course.py`

**Interfaces:**
- Produces:
  - `load_g9_lessons() -> list` — returns the 27 G9 v3.1 `Lesson` objects in filename (sequence) order.
  - `short_id(L) -> str` — a stable short lesson label from the filename stem, e.g. `"g9_l09_warrant"` (strip `lesson_` prefix and `_v3_1` suffix). Used as the journal `lesson` key so students never see the internal `ACC-W910-...` id.
  - `student_view(L) -> str` — the dev-free student experience (delegates to `lesson_review.render_student_experience`).

- [ ] **Step 1: Write the failing test**

```python
# tests/sim_student_eval/test_render_course.py
import os, sys
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "..", "Alpha HS Writing Course 2026-27", "pipeline"))
from sim_student_eval.render_course import load_g9_lessons, student_view, short_id


def test_loads_27_lessons_in_order():
    ls = load_g9_lessons()
    assert len(ls) == 27
    # first is l01 arguable claim, last is l27 gate argument essay (filename order)
    assert short_id(ls[0]).startswith("g9_l01")
    assert short_id(ls[-1]).startswith("g9_l27")


def test_short_id_has_no_internal_id():
    ls = load_g9_lessons()
    sid = short_id(ls[8])  # l09 warrant
    assert "ACC-" not in sid and "_v3_1" not in sid and "lesson_" not in sid
    assert sid.startswith("g9_l09")


def test_student_view_is_dev_free_and_nonempty():
    ls = load_g9_lessons()
    view = student_view(ls[8])
    assert len(view) > 500
    assert "STEP 1" in view
    # NONE of these development internals may leak to a student:
    for banned in ("lesson_type", "acc_tags", "Slot(", "Lesson(", "qc_lesson",
                   "mnemonic_status", "lesson_class", "ACC-W910", "design bet", "Grade-C"):
        assert banned not in view, f"dev internal leaked into student view: {banned}"
```

- [ ] **Step 2: Run test to verify it fails**

Run (from `Alpha HS Writing Course 2026-27/`):
```bash
python -m pytest ../../tests/sim_student_eval/test_render_course.py -v
```
Expected: FAIL — `ModuleNotFoundError: No module named 'sim_student_eval.render_course'`.

- [ ] **Step 3: Write minimal implementation**

```python
# pipeline/sim_student_eval/render_course.py
"""Load the G9 v3.1 course in sequence and render each lesson to the DEVELOPMENT-FREE
student experience. Students see student_view(L) output ONLY - never the Lesson object,
the .py source, or any internal id/label."""
import os, sys, glob, importlib.util

HERE = os.path.dirname(__file__)
PIPE = os.path.join(HERE, "..")           # Alpha HS Writing Course 2026-27/pipeline
ROOT = os.path.join(PIPE, "..")           # Alpha HS Writing Course 2026-27
sys.path.insert(0, PIPE)

import lesson_review  # noqa: E402  (import side effects wire STIM + gated_reading)


def _load_module(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def load_g9_lessons() -> list:
    lessons = []
    pattern = os.path.join(ROOT, "Lesson_Bank_G9", "lesson_g9_l*_v3_1.py")
    for f in sorted(glob.glob(pattern)):
        m = _load_module(f)
        L = getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0]
        if L is not None:
            L._src_file = os.path.basename(f)  # for short_id; not shown to students
            lessons.append(L)
    return lessons


def short_id(L) -> str:
    stem = getattr(L, "_src_file", "") or ""
    stem = stem[:-3] if stem.endswith(".py") else stem
    if stem.startswith("lesson_"):
        stem = stem[len("lesson_"):]
    if stem.endswith("_v3_1"):
        stem = stem[:-len("_v3_1")]
    return stem


def student_view(L) -> str:
    return lesson_review.render_student_experience(L)
```

- [ ] **Step 4: Run test to verify it passes**

Run:
```bash
python -m pytest ../../tests/sim_student_eval/test_render_course.py -v
```
Expected: 3 passed. (This proves the dev-free boundary — the constraint the whole design rests on.)

- [ ] **Step 5: Commit**

```bash
git add pipeline/sim_student_eval/render_course.py tests/sim_student_eval/test_render_course.py
git commit -m "feat(sim-student-eval): G9 course loader + dev-free student view (boundary test)"
```

---

## Task 6: Student agent (walk one lesson)

**Files:**
- Create: `pipeline/sim_student_eval/student_agent.py`

**Interfaces:**
- Consumes: a client with `.ask(system, user) -> {response, journal_update}` (Tasks 3-4); a persona dict (Task 2); `short_id`/`student_view` (Task 5); `JournalStore.digest()` (Task 1).
- Produces:
  - `COMPOSITION_LESSONS: set[str]` — short-id prefixes that are composition probes: `{"g9_l18", "g9_l23", "g9_l24", "g9_l26", "g9_l27"}` (paragraph gate + full essays + cold gate essays, per spec §4.3).
  - `build_user_prompt(sid, view, digest, is_composition) -> str`.
  - `walk_lesson(client, persona, L, digest) -> dict` returning `{"lesson": sid, "response": str, "journal_update": dict(validated w/ lesson+seq set)}`.

- [ ] **Step 1: Write the implementation**

```python
# pipeline/sim_student_eval/student_agent.py
"""Walk ONE lesson as ONE student. The student sees only: persona + running-memory digest +
the dev-free lesson view. It attempts every check/write in character and emits a journal update.
Composition-probe lessons add the 'use only what you've learned; name what you're missing' ask."""
from sim_student_eval.render_course import short_id, student_view
from sim_student_eval.journal import validate_entry

COMPOSITION_LESSONS = {"g9_l18", "g9_l23", "g9_l24", "g9_l26", "g9_l27"}


def _is_composition(sid: str) -> bool:
    return any(sid.startswith(p) for p in COMPOSITION_LESSONS)


def build_user_prompt(sid: str, view: str, digest: str, is_composition: bool) -> str:
    extra = ""
    if is_composition:
        extra = (
            "\n\nTHIS LESSON ASKS YOU TO WRITE A FULL PIECE. Use ONLY the skills you have "
            "actually learned in earlier lessons (see YOUR MEMORY above). Attempt it fully. "
            "If you find you are missing a skill you were never taught, write your best attempt "
            "anyway and then say clearly, in your response, which skill you are missing and that "
            "you do not remember a lesson that taught it.")
    return (
        "YOUR MEMORY FROM EARLIER LESSONS:\n" + digest +
        "\n\n===== TODAY'S LESSON (read it and do every step) =====\n" + view + extra +
        "\n\n=====\nNow: (1) actually answer the checks and attempt the writing tasks in your "
        "`response`, in character as a 9th grader. (2) In `journal_update`, honestly record what "
        "you can now do, terms you learned, where you struggled, whether anything felt like a "
        "repeat of an earlier lesson (set felt_repeated.echoes_lesson to that lesson's name like "
        "'g9_l03...' if so), any open questions, and your confidence per skill (0.0-1.0). "
        "Use the earlier-lesson NAMES exactly as they appear in YOUR MEMORY.")


def walk_lesson(client, persona: dict, L, digest: str) -> dict:
    sid = short_id(L)
    view = student_view(L)
    user = build_user_prompt(sid, view, digest, _is_composition(sid))
    out = client.ask(persona["system_preamble"], user)
    upd = dict(out.get("journal_update") or {})
    upd["lesson"] = sid
    # seq is assigned by the orchestrator (it knows position); default 0 here, overwritten in run_eval
    upd.setdefault("seq", 0)
    return {"lesson": sid, "response": out.get("response", ""),
            "journal_update": upd, "raw_error": out.get("error", "")}
```

- [ ] **Step 2: Verify import + prompt build (no network)**

Run (from `pipeline/`):
```bash
python -c "
from sim_student_eval.student_agent import build_user_prompt, COMPOSITION_LESSONS, _is_composition
p = build_user_prompt('g9_l23_full_argument_essay', 'STEP 1 ...', 'SKILLS I CAN DO: state a claim', True)
assert 'missing a skill' in p and 'YOUR MEMORY' in p
assert _is_composition('g9_l23_full_argument_essay') and not _is_composition('g9_l09_warrant')
print('prompt + composition detection OK')"
```
Expected: `prompt + composition detection OK`.

- [ ] **Step 3: Commit**

```bash
git add pipeline/sim_student_eval/student_agent.py
git commit -m "feat(sim-student-eval): student agent walks one lesson w/ journal + composition probe"
```

---

## Task 7: Test taker (test-readiness pass)

**Files:**
- Create: `pipeline/sim_student_eval/test_taker.py`
- Test: `tests/sim_student_eval/test_test_taker.py`

**Interfaces:**
- Produces:
  - `load_g9_test_items() -> list[dict]` — loads `Item_Bank_G9` SR + CR items into plain dicts the student can see: `{"id", "kind" ("choice"|"extended-text"|...), "stem", "options" (list of {"id","text"} — NO correct flag/rationale leaked), "answer_key" (list[str], kept SEPARATE for the harness, not shown to student), "mode"}`. Excludes `pp100_*` (mastery, out of scope).
  - `present_item(item: dict) -> str` — the student-facing text (stem + lettered options for MCQ; stem only for extended-text). Never includes the answer key or rationales.
  - `take_test(client, persona, items, digest) -> dict` — student attempts each item carrying its journal digest; returns `{"attempts": [ {"id","kind","student_answer","can_attempt" (bool),"missing_skill" (str)} ], "mcq_scored": {"correct": int, "total": int}}`. MCQ correctness is a deterministic answer-vs-key match (allowed: not a writing score). Extended-text items are attemptability + self-reported missing-skill only.

- [ ] **Step 1: Write the failing test**

```python
# tests/sim_student_eval/test_test_taker.py
import os, sys
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "..", "Alpha HS Writing Course 2026-27", "pipeline"))
from sim_student_eval.test_taker import load_g9_test_items, present_item


def test_loads_items_with_separated_answer_key():
    items = load_g9_test_items()
    assert len(items) > 10  # G9 bank has many SR + CR items
    mcq = [i for i in items if i["kind"] == "choice"]
    assert mcq, "expected some choice items"
    m = mcq[0]
    # answer key is stored for the harness, but options carry NO correctness signal
    assert "answer_key" in m and m["answer_key"]
    for opt in m["options"]:
        assert set(opt.keys()) == {"id", "text"}, "option leaked correct/rationale to student"


def test_present_item_hides_the_key():
    items = load_g9_test_items()
    mcq = next(i for i in items if i["kind"] == "choice")
    shown = present_item(mcq)
    assert mcq["stem"][:20] in shown
    # the correct-answer rationale text must never appear in what the student sees
    assert "rationale" not in shown.lower()


def test_extended_text_items_present_stem_only():
    items = load_g9_test_items()
    et = [i for i in items if i["kind"] == "extended-text"]
    assert et, "expected CR extended-text items"
    shown = present_item(et[0])
    assert et[0]["stem"][:20] in shown
```

- [ ] **Step 2: Run test to verify it fails**

Run (from `Alpha HS Writing Course 2026-27/`):
```bash
python -m pytest ../../tests/sim_student_eval/test_test_taker.py -v
```
Expected: FAIL — `ModuleNotFoundError: No module named 'sim_student_eval.test_taker'`.

- [ ] **Step 3: Write minimal implementation**

```python
# pipeline/sim_student_eval/test_taker.py
"""Test-readiness pass. The student takes the G9 test bank items carrying only its journal.
For MCQ we log a deterministic answer-vs-key match (allowed - not a writing score). For
extended-text (CR) we log attemptability + the student's self-reported missing skill only."""
import os, sys, glob, importlib.util, json

HERE = os.path.dirname(__file__)
PIPE = os.path.join(HERE, "..")
ROOT = os.path.join(PIPE, "..")
sys.path.insert(0, PIPE)

_SKIP_PREFIXES = ("pp100_",)  # mastery instruments: out of scope for lived test-readiness


def _load_module(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def load_g9_test_items() -> list:
    items = []
    for f in sorted(glob.glob(os.path.join(ROOT, "Item_Bank_G9", "*.py"))):
        if os.path.basename(f).startswith(_SKIP_PREFIXES):
            continue
        try:
            m = _load_module(f)
        except Exception:
            continue
        for it in getattr(m, "ITEMS", []):
            items.append({
                "id": it.id,
                "kind": it.qti_type,
                "stem": it.stem,
                "mode": it.subskill_or_mode,
                "options": [{"id": o.id, "text": o.text} for o in it.options],
                "answer_key": list(it.answer_key),  # harness-only, never shown
            })
    return items


def present_item(item: dict) -> str:
    lines = [item["stem"]]
    if item["options"]:
        for i, o in enumerate(item["options"]):
            lines.append(f"  ({chr(65 + i)}) {o['text']}")
    return "\n".join(lines)


_TEST_TOOL = {
    "name": "report_item_attempt",
    "description": "Report your attempt at one test question.",
    "input_schema": {"type": "object", "properties": {
        "answer_letter": {"type": "string", "description": "For multiple choice: the single letter you pick (A/B/C/D). Empty for written items."},
        "written_answer": {"type": "string", "description": "For written items: your attempt."},
        "can_attempt": {"type": "boolean", "description": "Can you attempt this at all with what the course taught you?"},
        "missing_skill": {"type": "string", "description": "If you cannot, name the skill you were never taught. Else empty."}},
        "required": ["can_attempt", "missing_skill"]}}


def _letter_to_option_id(item, letter):
    if not letter:
        return ""
    idx = ord(letter.strip().upper()[:1]) - ord("A")
    if 0 <= idx < len(item["options"]):
        return item["options"][idx]["id"]
    return ""


def take_test(client, persona: dict, items: list, digest: str) -> dict:
    attempts = []
    correct = 0
    total_mcq = 0
    for item in items:
        user = ("YOUR MEMORY FROM THE COURSE:\n" + digest +
                "\n\n===== TEST QUESTION =====\n" + present_item(item) +
                "\n\nAttempt this question in character. If it is multiple choice, pick one letter. "
                "If you cannot do it with what the course taught you, set can_attempt false and name "
                "the missing skill.")
        out = _ask_tool(client, persona["system_preamble"], user)
        rec = {"id": item["id"], "kind": item["kind"], "mode": item["mode"],
               "student_answer": out.get("answer_letter") or out.get("written_answer", ""),
               "can_attempt": bool(out.get("can_attempt", False)),
               "missing_skill": out.get("missing_skill", "")}
        if item["kind"] == "choice" and item["answer_key"]:
            total_mcq += 1
            picked = _letter_to_option_id(item, out.get("answer_letter", ""))
            rec["mcq_correct"] = picked in item["answer_key"]
            if rec["mcq_correct"]:
                correct += 1
        attempts.append(rec)
    return {"attempts": attempts, "mcq_scored": {"correct": correct, "total": total_mcq}}


def _ask_tool(client, system, user):
    """Use the client's underlying model with the item-attempt tool. Falls back to .ask
    if the client does not expose a raw tool path (keeps the protocol simple)."""
    fn = getattr(client, "ask_tool", None)
    if callable(fn):
        return fn(system, user, _TEST_TOOL)
    # default: reuse .ask (student turn) and read answer text; can_attempt inferred True
    out = client.ask(system, user)
    return {"written_answer": out.get("response", ""), "can_attempt": True, "missing_skill": ""}
```

> Note: to keep MCQ scoring meaningful, add a small `ask_tool(system, user, tool)` method to `FableClient` and `GptClient` in a follow-up commit within this task (Step 4b). It mirrors `.ask` but takes the tool schema as a parameter and returns the tool input dict.

- [ ] **Step 4: Run test to verify it passes**

Run:
```bash
python -m pytest ../../tests/sim_student_eval/test_test_taker.py -v
```
Expected: 3 passed.

- [ ] **Step 4b: Add `ask_tool` to both clients (enables real MCQ scoring)**

In `pipeline/sim_student_eval/models.py`, add to `FableClient`:
```python
    def ask_tool(self, system: str, user: str, tool: dict) -> dict:
        r = self._c.messages.create(
            model=self._model, max_tokens=1500, system=system,
            tools=[tool], tool_choice={"type": "tool", "name": tool["name"]},
            messages=[{"role": "user", "content": user}])
        for b in r.content:
            if getattr(b, "type", "") == "tool_use":
                return dict(b.input)
        return {}
```
And to `GptClient`:
```python
    def ask_tool(self, system: str, user: str, tool: dict) -> dict:
        import json as _json
        ot = {"type": "function", "function": {"name": tool["name"],
              "description": tool["description"], "parameters": tool["input_schema"]}}
        r = self._c.chat.completions.create(
            model=self._model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            tools=[ot], tool_choice={"type": "function", "function": {"name": tool["name"]}},
            max_completion_tokens=1500)
        msg = r.choices[0].message
        if msg.tool_calls:
            return dict(_json.loads(msg.tool_calls[0].function.arguments))
        return {}
```
Verify import still works:
```bash
python -c "from sim_student_eval.models import FableClient, GptClient; print(hasattr(FableClient,'ask_tool') and hasattr(GptClient,'ask_tool'))"
```
Expected: `True`.

- [ ] **Step 5: Commit**

```bash
git add pipeline/sim_student_eval/test_taker.py tests/sim_student_eval/test_test_taker.py pipeline/sim_student_eval/models.py
git commit -m "feat(sim-student-eval): test-readiness pass (MCQ match + CR attemptability)"
```

---

## Task 8: Analyst (synthesis + report)

**Files:**
- Create: `pipeline/sim_student_eval/analyst.py`

**Interfaces:**
- Consumes: the run's output dir with `journal_*.jsonl`, `transcript_*.jsonl`, `test_*.json`.
- Produces:
  - `gather(run_dir: str) -> dict` — loads all journals, transcripts, and test results into an in-memory structure keyed by `(persona, model)`.
  - `detect_redundancies(gathered: dict) -> list[dict]` — deterministic pre-pass: every `felt_repeated` across all walks, grouped by `(lesson, echoes_lesson)`, tagged with which walks raised it (for the CORROBORATED vs SINGLE tags).
  - `synthesize(run_dir: str, anthropic_key: str, model: str = "claude-opus-4-8") -> str` — builds the analyst prompt from the gathered evidence + deterministic redundancy table, calls Claude with a structured report tool, returns the finished `SIM_STUDENT_EVAL_G9.md` markdown (findings ranked most-severe-first, organized by the four questions, with corroboration labels and no em dashes).

- [ ] **Step 1: Write the implementation**

```python
# pipeline/sim_student_eval/analyst.py
"""Synthesis pass. Reads all four course-walks' journals + transcripts + test logs, runs a
deterministic redundancy pre-pass (from felt_repeated), then asks Claude to write the report
answering the four curriculum questions. Findings are corroboration-labeled; nothing is scored."""
import os, json, glob


def gather(run_dir: str) -> dict:
    out = {"walks": {}, "tests": {}}
    for f in glob.glob(os.path.join(run_dir, "journal_*.jsonl")):
        key = os.path.basename(f)[len("journal_"):-len(".jsonl")]  # persona_model
        out["walks"].setdefault(key, {})["journal"] = [json.loads(l) for l in open(f, encoding="utf-8") if l.strip()]
    for f in glob.glob(os.path.join(run_dir, "transcript_*.jsonl")):
        key = os.path.basename(f)[len("transcript_"):-len(".jsonl")]
        out["walks"].setdefault(key, {})["transcript"] = [json.loads(l) for l in open(f, encoding="utf-8") if l.strip()]
    for f in glob.glob(os.path.join(run_dir, "test_*.json")):
        key = os.path.basename(f)[len("test_"):-len(".json")]
        out["tests"][key] = json.load(open(f, encoding="utf-8"))
    return out


def detect_redundancies(gathered: dict) -> list:
    groups = {}
    for walk_key, data in gathered["walks"].items():
        for entry in data.get("journal", []):
            fr = entry.get("felt_repeated")
            if fr and fr.get("echoes_lesson"):
                k = (entry["lesson"], fr["echoes_lesson"])
                groups.setdefault(k, {"lesson": entry["lesson"], "echoes_lesson": fr["echoes_lesson"],
                                      "what": fr.get("what", ""), "raised_by": []})
                groups[k]["raised_by"].append(walk_key)
    rows = list(groups.values())
    for r in rows:
        models = {w.split("_")[-1] for w in r["raised_by"]}
        personas = {w.rsplit("_", 1)[0] for w in r["raised_by"]}
        r["corroboration"] = ("CORROBORATED (cross-model)" if len(models) > 1 else
                              "CORROBORATED (cross-persona)" if len(personas) > 1 else "SINGLE")
    return sorted(rows, key=lambda r: -len(r["raised_by"]))


_REPORT_TOOL = {
    "name": "write_report",
    "description": "Write the curriculum-evaluation report sections.",
    "input_schema": {"type": "object", "properties": {
        "makes_sense": {"type": "string", "description": "Q1 findings: per-lesson clarity, specific confusion points with lesson+step. Markdown."},
        "redundancies": {"type": "string", "description": "Q2 findings: corroborated redundancy list, each with the two lessons + which walks flagged it. Markdown."},
        "composition_readiness": {"type": "string", "description": "Q3: for each composition probe (l18/l23/l24/l26/l27), which skills were/weren't in place, traced to lessons. Markdown."},
        "test_readiness": {"type": "string", "description": "Q4: items students couldn't attempt + missing-skill trace; MCQ match rates as context. Markdown."},
        "top_findings": {"type": "string", "description": "The 5-10 most severe findings, ranked, each traceable to a student utterance. Markdown."}},
        "required": ["makes_sense", "redundancies", "composition_readiness", "test_readiness", "top_findings"]}}


def _build_evidence(gathered: dict, redundancies: list) -> str:
    parts = ["DETERMINISTIC REDUNDANCY TABLE (from students' own felt_repeated flags):"]
    for r in redundancies:
        parts.append(f"- {r['lesson']} felt like a repeat of {r['echoes_lesson']} ({r['corroboration']}; raised by {', '.join(r['raised_by'])}): {r['what']}")
    for wk, data in gathered["walks"].items():
        parts.append(f"\n===== WALK: {wk} =====")
        for e in data.get("journal", []):
            parts.append(f"[{e['lesson']}] can_do={e.get('skills_i_can_now_do')}; struggled={e.get('where_i_struggled')}; open={e.get('open_questions')}; conf={e.get('confidence')}")
        for t in data.get("transcript", []):
            if any(t["lesson"].startswith(p) for p in ("g9_l18", "g9_l23", "g9_l24", "g9_l26", "g9_l27")):
                parts.append(f"[COMPOSITION {t['lesson']}] response: {t['response'][:1200]}")
    for tk, tr in gathered["tests"].items():
        na = [a for a in tr["attempts"] if not a["can_attempt"]]
        parts.append(f"\n===== TEST {tk} ===== mcq {tr['mcq_scored']}; cannot-attempt {len(na)}: " +
                     "; ".join(f"{a['id']}:{a['missing_skill']}" for a in na[:20]))
    return "\n".join(parts)[:120000]


def synthesize(run_dir: str, anthropic_key: str, model: str = "claude-opus-4-8") -> str:
    import anthropic
    gathered = gather(run_dir)
    redundancies = detect_redundancies(gathered)
    evidence = _build_evidence(gathered, redundancies)
    prompt = (
        "You are an instructional-design analyst. Four simulated 9th-grade students (two personas: "
        "on-grade average and high-achiever; each run once by Fable-5 and once by GPT) walked the "
        "G9 writing course in order, carrying a running memory. Below is their evidence. Write a "
        "curriculum evaluation answering four questions: (1) do the lessons make sense? (2) are there "
        "redundancies? (3) do the lessons prepare students for the full compositions? (4) do they "
        "prepare students for the tests?\n\n"
        "RULES: Every finding must be specific and cite a lesson (and step if possible) and the walk "
        "that raised it. Label redundancy/readiness findings CORROBORATED (raised across models or "
        "personas) vs PERSONA-SPECIFIC vs SINGLE-MODEL. Do NOT invent findings not in the evidence. "
        "Do NOT score writing. NO em dashes anywhere (use commas, colons, parentheses). Be blunt and "
        "concrete, never generic.\n\n" + evidence)
    c = anthropic.Anthropic(api_key=anthropic_key)
    r = c.messages.create(model=model, max_tokens=6000, tools=[_REPORT_TOOL],
                          tool_choice={"type": "tool", "name": "write_report"},
                          messages=[{"role": "user", "content": prompt}])
    rep = {}
    for b in r.content:
        if getattr(b, "type", "") == "tool_use":
            rep = b.input
    md = ["# Simulated-Student Curriculum Evaluation - G9 Pilot", "",
          "> Signal, not proof. Four simulated students are a design signal to investigate, "
          "NOT field evidence of efficacy. No writing was scored (grading is not yet wired); "
          "findings are the students' lived experience plus deterministic multiple-choice matches.", "",
          "## Most severe findings (ranked)", "", rep.get("top_findings", "(none)"), "",
          "## 1. Do the lessons make sense?", "", rep.get("makes_sense", ""), "",
          "## 2. Are there redundancies?", "", rep.get("redundancies", ""), "",
          "## 3. Do the lessons prepare them for the full compositions?", "", rep.get("composition_readiness", ""), "",
          "## 4. Do the courses prepare them for the tests?", "", rep.get("test_readiness", "")]
    return "\n".join(md)
```

- [ ] **Step 2: Verify import + deterministic redundancy pre-pass (no network)**

Run (from `pipeline/`):
```bash
python -c "
from sim_student_eval.analyst import detect_redundancies
g = {'walks': {
  'average_fable': {'journal': [{'lesson':'g9_l11','felt_repeated':{'echoes_lesson':'g9_l09','what':'warrant again'}}]},
  'average_gpt':   {'journal': [{'lesson':'g9_l11','felt_repeated':{'echoes_lesson':'g9_l09','what':'warrant again'}}]}}, 'tests': {}}
r = detect_redundancies(g)
assert r[0]['corroboration'].startswith('CORROBORATED (cross-model)'), r
print('redundancy corroboration OK:', r[0]['corroboration'])"
```
Expected: `redundancy corroboration OK: CORROBORATED (cross-model)`.

- [ ] **Step 3: Commit**

```bash
git add pipeline/sim_student_eval/analyst.py
git commit -m "feat(sim-student-eval): analyst synthesis + deterministic redundancy pre-pass"
```

---

## Task 9: Orchestrator CLI

**Files:**
- Create: `pipeline/sim_student_eval/run_eval.py`

**Interfaces:**
- Consumes: everything above.
- Produces: a CLI. `python -m sim_student_eval.run_eval [--limit N] [--personas average,achiever] [--models fable,gpt] [--gpt-model gpt-5.5] [--no-test] [--run-id NAME]`. Writes all outputs under `pipeline/sim_student_eval/out/<run_id>/` and prints the report path. Continues past a single failed lesson call (logs the error into the transcript, keeps walking) so one API hiccup does not kill a 27-lesson walk.

- [ ] **Step 1: Write the implementation**

```python
# pipeline/sim_student_eval/run_eval.py
"""Orchestrator: 2 models x 2 personas x 27 G9 lessons + test -> report.
Each (persona, model) is an independent course-walk with its own journal. The next lesson
sees ONLY persona + journal digest + rendered lesson (never prior raw transcripts)."""
import os, sys, json, argparse

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, ".."))

from sim_student_eval.personas import PERSONAS
from sim_student_eval.models import load_keys, FableClient, GptClient
from sim_student_eval.render_course import load_g9_lessons, short_id
from sim_student_eval.journal import JournalStore
from sim_student_eval.student_agent import walk_lesson
from sim_student_eval.test_taker import load_g9_test_items, take_test
from sim_student_eval.analyst import synthesize

OUT_ROOT = os.path.join(HERE, "out")


def _client(model_name, keys, gpt_model):
    if model_name == "fable":
        return FableClient(keys["anthropic"])
    if model_name == "gpt":
        return GptClient(keys["openai"], model=gpt_model)
    raise ValueError(model_name)


def run_walk(persona_id, model_name, lessons, run_dir, keys, gpt_model, do_test):
    persona = PERSONAS[persona_id]
    client = _client(model_name, keys, gpt_model)
    tag = f"{persona_id}_{model_name}"
    jstore = JournalStore(os.path.join(run_dir, f"journal_{tag}.jsonl"))
    tpath = os.path.join(run_dir, f"transcript_{tag}.jsonl")
    for seq, L in enumerate(lessons, 1):
        try:
            res = walk_lesson(client, persona, L, jstore.digest())
        except Exception as e:  # keep the walk alive on a single API failure
            res = {"lesson": short_id(L), "response": "", "journal_update": {"lesson": short_id(L), "seq": seq}, "raw_error": repr(e)}
        res["journal_update"]["seq"] = seq
        res["journal_update"]["lesson"] = res["lesson"]
        jstore.append(res["journal_update"])
        with open(tpath, "a", encoding="utf-8") as f:
            f.write(json.dumps({"lesson": res["lesson"], "seq": seq, "response": res["response"], "error": res.get("raw_error", "")}, ensure_ascii=False) + "\n")
        print(f"  [{tag}] {seq}/{len(lessons)} {res['lesson']}" + (" ERROR" if res.get("raw_error") else ""))
    if do_test:
        items = load_g9_test_items()
        tres = take_test(client, persona, items, jstore.digest())
        json.dump(tres, open(os.path.join(run_dir, f"test_{tag}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"  [{tag}] test: mcq {tres['mcq_scored']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="only the first N lessons (smoke)")
    ap.add_argument("--personas", default="average,achiever")
    ap.add_argument("--models", default="fable,gpt")
    ap.add_argument("--gpt-model", default="gpt-5.5")
    ap.add_argument("--no-test", action="store_true")
    ap.add_argument("--run-id", default="g9_pilot")
    a = ap.parse_args()

    keys = load_keys()
    lessons = load_g9_lessons()
    if a.limit:
        lessons = lessons[:a.limit]
    run_dir = os.path.join(OUT_ROOT, a.run_id)
    os.makedirs(run_dir, exist_ok=True)
    print(f"Run dir: {run_dir}  |  lessons: {len(lessons)}")

    for persona_id in a.personas.split(","):
        for model_name in a.models.split(","):
            print(f"WALK: {persona_id} x {model_name}")
            run_walk(persona_id.strip(), model_name.strip(), lessons, run_dir, keys, a.gpt_model, not a.no_test)

    print("Synthesizing report...")
    md = synthesize(run_dir, keys["anthropic"])
    rp = os.path.join(run_dir, "SIM_STUDENT_EVAL_G9.md")
    open(rp, "w", encoding="utf-8").write(md)
    print("REPORT:", rp)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verify the CLI parses + dry structure (no network)**

Run (from `pipeline/`):
```bash
python -m sim_student_eval.run_eval --help
```
Expected: argparse help listing `--limit`, `--personas`, `--models`, `--gpt-model`, `--no-test`, `--run-id`.

- [ ] **Step 3: Commit**

```bash
git add pipeline/sim_student_eval/run_eval.py
git commit -m "feat(sim-student-eval): orchestrator CLI (2 models x 2 personas x 27 lessons)"
```

---

## Task 10: Offline smoke test (mocked clients, no API cost)

**Files:**
- Create: `tests/sim_student_eval/test_smoke.py`

**Interfaces:**
- Consumes: `walk_lesson`, `take_test`, `JournalStore`, `detect_redundancies` with a FAKE client (no network) to prove the full data path end-to-end without spending tokens.

- [ ] **Step 1: Write the smoke test**

```python
# tests/sim_student_eval/test_smoke.py
import os, sys, tempfile
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "..", "Alpha HS Writing Course 2026-27", "pipeline"))
from sim_student_eval.render_course import load_g9_lessons, short_id
from sim_student_eval.student_agent import walk_lesson
from sim_student_eval.journal import JournalStore


class FakeClient:
    name = "fake"
    def __init__(self):
        self.seen = []
    def ask(self, system, user):
        self.seen.append(user)
        return {"response": "I picked B. My claim: schools should X because Y.",
                "journal_update": {"skills_i_can_now_do": ["state a claim"],
                                   "where_i_struggled": [], "open_questions": [],
                                   "confidence": {"claim": 0.7},
                                   "felt_repeated": {"echoes_lesson": "g9_l01", "what": "claim again"}}}
    def ask_tool(self, system, user, tool):
        return {"answer_letter": "B", "can_attempt": True, "missing_skill": ""}


def test_walk_three_lessons_builds_journal_and_bounds_context():
    lessons = load_g9_lessons()[:3]
    fc = FakeClient()
    with tempfile.TemporaryDirectory() as d:
        js = JournalStore(os.path.join(d, "j.jsonl"))
        for seq, L in enumerate(lessons, 1):
            res = walk_lesson(fc, {"system_preamble": "you are a student"}, L, js.digest())
            res["journal_update"]["seq"] = seq
            js.append(res["journal_update"])
        rows = js.entries()
        assert len(rows) == 3
        assert rows[0]["lesson"].startswith("g9_l01")
        # the SECOND lesson's prompt must contain the digest from lesson 1 (memory carried)
        assert "state a claim" in fc.seen[1]
        # but must NOT contain lesson 1's raw response text (no transcript contamination)
        assert "I picked B" not in fc.seen[1]


def test_dev_internals_never_reach_the_client():
    lessons = load_g9_lessons()[:2]
    fc = FakeClient()
    with tempfile.TemporaryDirectory() as d:
        js = JournalStore(os.path.join(d, "j.jsonl"))
        walk_lesson(fc, {"system_preamble": "s"}, lessons[0], js.digest())
    joined = "\n".join(fc.seen)
    for banned in ("ACC-W910", "lesson_type", "Slot(", "Grade-C", "mnemonic_status"):
        assert banned not in joined
```

- [ ] **Step 2: Run the smoke test**

Run (from `Alpha HS Writing Course 2026-27/`):
```bash
python -m pytest ../../tests/sim_student_eval/test_smoke.py -v
```
Expected: 2 passed. This proves: (a) memory is carried via digest, (b) raw transcripts do NOT leak into the next lesson's context (the contamination guard), (c) no dev internals reach the client.

- [ ] **Step 3: Run the full offline test suite**

Run:
```bash
python -m pytest ../../tests/sim_student_eval/ -v
```
Expected: all tests pass (journal 4, render 3, test_taker 3, smoke 2 = 12).

- [ ] **Step 4: Commit**

```bash
git add tests/sim_student_eval/test_smoke.py
git commit -m "test(sim-student-eval): offline end-to-end smoke (memory carry + contamination guard)"
```

---

## Task 11: Live 2-lesson pilot smoke (real APIs, tiny cost) + README

**Files:**
- Create: `pipeline/sim_student_eval/README.md`

- [ ] **Step 1: Run a 2-lesson, 1-persona, 1-model live smoke**

Run (from `pipeline/`):
```bash
python -m sim_student_eval.run_eval --limit 2 --personas average --models fable --no-test --run-id smoke_fable
```
Expected: prints `[average_fable] 1/2 g9_l01...` and `2/2 ...`, then synthesizes and prints a REPORT path. Then verify the outputs exist and are non-empty:
```bash
python -c "import json,os; d='sim_student_eval/out/smoke_fable'; j=[l for l in open(os.path.join(d,'journal_average_fable.jsonl'),encoding='utf-8')]; print('journal lines:', len(j)); print('report exists:', os.path.exists(os.path.join(d,'SIM_STUDENT_EVAL_G9.md')))"
```
Expected: `journal lines: 2` and `report exists: True`. If the Anthropic call fails (quota/credits), STOP and report to Noel — do not proceed to the GPT smoke or full run.

- [ ] **Step 2: Run a 2-lesson GPT smoke (validates the OpenAI path + gpt model id)**

Run:
```bash
python -m sim_student_eval.run_eval --limit 2 --personas average --models gpt --no-test --run-id smoke_gpt
```
Expected: 2 journal lines for `average_gpt`. If OpenAI reports an invalid model, re-run with `--gpt-model <valid-id>` and note the working id in the README. Do NOT hardcode.

- [ ] **Step 3: Inspect one journal entry by eye (quality gate before spending the full run)**

Run:
```bash
python -c "import json; print(json.dumps(json.loads(open('sim_student_eval/out/smoke_fable/journal_average_fable.jsonl',encoding='utf-8').readlines()[-1]), indent=2))"
```
Confirm by eye: `skills_i_can_now_do` reflects the actual lesson, `confidence` is populated, no dev internals. If the student output is empty or generic, the prompts need tuning before the full run (fix in `student_agent.build_user_prompt`, re-smoke).

- [ ] **Step 4: Write the README**

Create `pipeline/sim_student_eval/README.md`:
```markdown
# Simulated-Student Curriculum Evaluation (G9 pilot)

LLM "students" (Fable-5 + GPT), with no knowledge of course development, walk the G9 course
in sequence, attempt every task, take the test bank, and produce a report answering:
1. Do the lessons make sense?  2. Are there redundancies?
3. Do they prepare students for the full compositions?  4. Do they prepare students for the tests?

## Design boundary
Students see ONLY `render_student_experience(L)` (the dev-free view) plus a bounded on-disk
learner journal (their only memory between lessons). They never see source, ids, gates, or labels.
No writing is scored (grading is not wired); findings are lived experience + deterministic MCQ matches.

## Run
    # full pilot: 2 models x 2 personas x 27 lessons + test
    python -m sim_student_eval.run_eval

    # cheap smoke first (2 lessons, 1 model, no test)
    python -m sim_student_eval.run_eval --limit 2 --personas average --models fable --no-test --run-id smoke

Options: --limit N, --personas average,achiever, --models fable,gpt, --gpt-model <id>, --no-test, --run-id NAME.
Outputs land in `out/<run_id>/`: journal_*.jsonl, transcript_*.jsonl, test_*.json, SIM_STUDENT_EVAL_G9.md.

## Working GPT model id
<record the id that worked in Task 11 Step 2 here>

## Scaling to G10-G12
The harness is grade-general in shape; the loaders (`render_course.load_g9_lessons`,
`test_taker.load_g9_test_items`) are G9-hardcoded. Generalize by parameterizing the grade
glob before running other grades. Add the struggling + distractible personas in personas.py.
```

- [ ] **Step 5: Commit**

```bash
git add pipeline/sim_student_eval/README.md
git commit -m "docs(sim-student-eval): README + record live smoke results"
```

---

## Task 12: Full G9 pilot run (gated on Noel's go)

**Files:** none (produces `out/g9_pilot/`).

- [ ] **Step 1: Confirm with Noel before spending the full run**

The full run is 4 walks × 27 lessons + 4 test passes ≈ 112 lesson calls + 4 test batches across two paid APIs. Report the smoke results and estimated scope; get explicit go.

- [ ] **Step 2: Run the full pilot**

Run (from `pipeline/`):
```bash
python -m sim_student_eval.run_eval --run-id g9_pilot
```
Expected: 4 walks complete (average/achiever × fable/gpt), each 27 lessons + test, then a report at `out/g9_pilot/SIM_STUDENT_EVAL_G9.md`.

- [ ] **Step 3: Read the report and sanity-check against the raw journals**

Open `out/g9_pilot/SIM_STUDENT_EVAL_G9.md`. Spot-check 3 findings: each must trace to an actual journal/transcript line (the analyst is instructed not to invent, but verify — same discipline as the readiness-audit triage). Flag any finding that does not trace, and any generic/slop finding, for a re-synthesis with a tightened prompt.

- [ ] **Step 4: Commit the pilot artifacts**

```bash
git add pipeline/sim_student_eval/out/g9_pilot/
git commit -m "chore(sim-student-eval): G9 pilot run artifacts + report"
```

---

## Self-Review

**1. Spec coverage:**
- §2 grading gap (no scoring) → Global Constraints + Task 7 (MCQ match only, CR attemptability) + analyst rules. ✓
- §2 run scope (G9 pilot) → Tasks 5/7 G9-hardcoded, Task 12 full G9 run, README scaling note. ✓
- §2 student memory (external journal) → Task 1 + smoke test proves contamination guard. ✓
- §2 personas (average + achiever) → Task 2 + orchestrator matrix. ✓
- §2 model roles (both as students, Claude synthesizes) → Tasks 3/4 students, Task 8 Claude analyst. ✓
- §3 no-knowledge-of-development boundary → Task 5 boundary test + Task 10 smoke assertion. ✓
- §4.2 journal schema → Task 1 validate_entry matches spec fields. ✓
- §4.3 composition probes (L18/23/24/26/27) → Task 6 COMPOSITION_LESSONS + prompt. ✓
- §4.4 test-readiness → Task 7. ✓
- §4.5 corroboration labels → Task 8 detect_redundancies + report rules. ✓
- §5 outputs (journal/transcript/test/report files) → Task 9 file names + Task 8 report. ✓
- §6 honesty guardrails (coverage≠efficacy banner, anti-slop, no em dash) → analyst report header + prompt rules. ✓

**2. Placeholder scan:** No TBD/TODO/"handle appropriately". The two "record the working id here" notes are deliberate run-time outputs, not code placeholders. ✓

**3. Type consistency:** `.ask(system, user) -> {"response", "journal_update"}` consistent across FableClient/GptClient/FakeClient and student_agent. `ask_tool(system, user, tool) -> dict` consistent across both clients + test_taker. `validate_entry` fields match the journal_update schema in models.py `_JOURNAL_SCHEMA`. `short_id` output shape (`g9_lNN_...`) consistent across render_course, student_agent, analyst, smoke test. ✓

One consistency note applied: `student_agent.walk_lesson` sets `journal_update["seq"]=0` as a default, and `run_eval.run_walk` overwrites it with the real seq before `append` — the smoke test also sets seq before append, matching.
