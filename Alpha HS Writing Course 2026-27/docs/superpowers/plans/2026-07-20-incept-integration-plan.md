# Incept Integration Implementation Plan (Phases A-E)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wire Incept into the HS Writing pipeline per the strategy doc: an independent second judge (QC), editable diagrams (drawio), question-seed assist, an OpenAI diversity check, and a post-lock video stage — every module dry-by-default with an explicit `--live` gate, and everything Incept produces re-entering our 30-gate contract.

**Architecture:** Incept is an UPSTREAM content source + independent judge, never a bypass. Each module follows the proven `verify_facts.py` pattern (networked pass → cached receipt/artifact → offline consumer reads the cache) and the `g9_push_dryrun`/`g9_push_live` split (dry by default; real POST only with `--live`). Diagrams bind through the existing `_content_card(img=...)` slot via a new `_INCEPT_DIAGRAMS` registry parallel to `_DIAGRAMS`. QC is advisory (writes a receipt; never blocks the build).

**Tech Stack:** Python (stdlib + `requests` or `curl` subprocess), the existing `pipeline/` modules, `pipeline/tests/` (pytest). Live calls hit `https://v2.incept.school` and REQUIRE curl `--ssl-no-revoke` (a Windows schannel cert-revocation quirk verified 2026-07-20). Key in `Incept/Incept Production details.md` (read from env/file, NEVER hardcode or log).

## Global Constraints

- **Dry by default; `--live` to spend.** No module makes a real Incept POST unless invoked with `--live`. Dry mode validates the request shape and uses cached artifacts. Tests NEVER hit the network.
- **Secrets:** read `INCEPT_API_KEY` from `Incept/Incept Production details.md` or env; never hardcode, never write it into any committed file, log, or artifact. Presigned S3 URLs in Incept responses are also secret-bearing — do not commit them.
- **Everything Incept generates re-enters our contract:** any diagram/question/text that will ship must pass the relevant `lesson_contract.py` gates + anti-slop + provenance before binding. Incept output is raw material, not a bypass.
- **Honor `below_bar`:** if an artifact's `below_bar` is `true`, do NOT bind it — re-generate or human-review.
- **QC is advisory only** (Noel's decision): it writes a receipt; the build/gates never hard-fail on an Incept verdict.
- **No em dashes** in any student-facing text produced or bound.
- **No fabricated facts:** generated content reuses verified sources; diagrams' labels must trace to vetted prose.
- **Transport:** all live curl calls use `--ssl-no-revoke --max-time <n>`; poll etiquette per the API (fast lane ~15s, slow lane minutes). Match artifacts by `request_id`/`artifact_id`, never prompt/title.
- **Full `pytest pipeline/tests/` stays green; touched lessons stay `tier_a_regression` clean.**

---

### Task 1: `incept_client.py` — the shared transport + dry/live core

**Files:**
- Create: `pipeline/incept_client.py`
- Test: `pipeline/tests/test_incept_client.py`

**Interfaces:**
- Produces: `class InceptClient` with `options()`, `generate(prompt, generation_type, options=None, **scope)`, `poll(request_id, kind="generate")`, `artifact(artifact_id)`, `qc(generation_type, content, prompt=None, **scope)`. Every method takes `live: bool` (default False). In dry mode: `generate`/`qc` return a synthetic `{"request_id": None, "status": "dry", "would_send": <the request body>}` WITHOUT calling the network; `options`/`artifact`/`poll` read from a local cache dir (`C:/tmp/incept_cache/` or a configurable path) and raise a clear error if a cache miss occurs in dry mode.
- Produces: `_key()` reads INCEPT_API_KEY from env or `Incept/Incept Production details.md`; raises if absent. Never logged.
- Produces: `_curl(method, path, body=None, live=False)` wrapping `curl --ssl-no-revoke` (subprocess) — the only transport (verified working); returns parsed JSON.

- [ ] **Step 1: Write the failing test** (dry mode makes NO network call, returns the would-send body; key redaction)
```python
# pipeline/tests/test_incept_client.py
import os, sys
PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path: sys.path.insert(0, PIPE)
from incept_client import InceptClient

def test_generate_dry_makes_no_call_and_echoes_body():
    c = InceptClient(cache_dir="C:/tmp/incept_cache_test")
    r = c.generate("teach arguable claim", "image", options={"image_subtype": "drawio"},
                   grade_levels=["g9"], subject="writing", live=False)
    assert r["status"] == "dry"
    assert r["would_send"]["generation_type"] == "image"
    assert r["would_send"]["options"]["image_subtype"] == "drawio"
    assert r["request_id"] is None  # nothing was submitted

def test_qc_dry_echoes_payload():
    c = InceptClient(cache_dir="C:/tmp/incept_cache_test")
    r = c.qc("question", {"stem": "x", "options": ["a","b","c","d"], "answer_key": {"answer":"a"}},
             prompt="assess claim id", grade_levels=["g9"], subject="writing", live=False)
    assert r["status"] == "dry" and r["would_send"]["generation_type"] == "question"

def test_key_never_appears_in_repr():
    c = InceptClient(cache_dir="C:/tmp/incept_cache_test")
    assert "ik_" not in repr(c) and "ik_" not in str(vars(c))
```
- [ ] **Step 2: Run → fail** (`incept_client` undefined). `python -m pytest pipeline/tests/test_incept_client.py -v`
- [ ] **Step 3: Implement** `pipeline/incept_client.py`:
  - `_key()`: try `os.environ["INCEPT_API_KEY"]`, else parse the `## API Key` line from `../Incept/Incept Production details.md`. Store on the instance as a private attr excluded from `__repr__`.
  - `_curl(method, path, body, live)`: if not live and method == "POST", return the dry stub; else `subprocess.run(["curl","-s","--ssl-no-revoke","--max-time","40","-X",method, base+path, "-H", f"Authorization: Bearer {key}", ...])`, parse JSON. Never echo the key in any error string.
  - `generate`/`qc`: build the request body; if `live` POST it, else return `{"status":"dry","would_send":body,"request_id":None}`.
  - `poll`/`artifact`/`options`: GET (reads are cheap but still gated — in dry mode read the cache dir; in live mode fetch and write-through to cache).
- [ ] **Step 4: Run → pass.** `python -m pytest pipeline/tests/test_incept_client.py -v`
- [ ] **Step 5: Verify no regression + no network in tests.** `python -m pytest pipeline/tests/ -q` (expect prior + 3). Confirm the 3 new tests make zero network calls (they use live=False).
- [ ] **Step 6: Commit**
```bash
git add "Alpha HS Writing Course 2026-27/pipeline/incept_client.py" "Alpha HS Writing Course 2026-27/pipeline/tests/test_incept_client.py"
git commit -m "feat(incept): incept_client.py - shared transport, dry-by-default + --live, key redaction"
```

---

### Task 2 (Phase A): `incept_qc.py` — advisory second judge + receipt

**Files:**
- Create: `pipeline/incept_qc.py`, `pipeline/incept_qc_receipts.json` (created on first live run; committed WITHOUT any URL/secret)
- Test: `pipeline/tests/test_incept_qc.py`

**Interfaces:**
- Consumes: `InceptClient`; a `Slot`/item → the QC `content` JSON (the probe proved `{stem, options[], answer_key:{answer,explanation}}` for a discrimination).
- Produces: `slot_to_qc_content(slot) -> dict` (discrimination/production → the QC shape). `qc_item(lesson_id, slot_idx, live=False) -> verdict|dry`. `record(receipt)` appends to `incept_qc_receipts.json` keyed by `f"{lesson_id}:s{idx}"` storing ONLY `{judge_score, passed, axes:[{id,score,pass}], flagged:bool}` — NO prompts, NO URLs, NO content.
- Advisory: nothing here raises or fails a build; a helper `low_scoring(threshold=85)` lists receipts below the bar for human review.

- [ ] **Step 1: Write the failing test** — `slot_to_qc_content` maps a real discrimination slot to the `{stem, options, answer_key}` shape (build a Slot in-test; assert 4 options + answer present); `record`/`low_scoring` round-trip a synthetic verdict without network.
- [ ] **Step 2: Run → fail.**
- [ ] **Step 3: Implement.** `slot_to_qc_content` reuses the proven probe mapping. `qc_item` in dry mode returns the would-send; in live mode POSTs, polls `/api/v1/qc/<id>`, and writes the redacted receipt. `low_scoring` reads the receipt file.
- [ ] **Step 4: Run → pass.**
- [ ] **Step 5:** `python -m pytest pipeline/tests/ -q` green.
- [ ] **Step 6: Commit** (`feat(incept): incept_qc.py - advisory second-judge, redacted receipts`).

---

### Task 3 (Phase B): `incept_diagram.py` + `_INCEPT_DIAGRAMS` binding

**Files:**
- Create: `pipeline/incept_diagram.py`, `pipeline/incept_diagrams.py` (the `_INCEPT_DIAGRAMS` registry module)
- Modify: `pipeline/gated_reading.py` (look up `_INCEPT_DIAGRAMS` for a slot's PNG, bind via `_content_card(img=...)`)
- Test: `pipeline/tests/test_incept_diagram.py`

**Interfaces:**
- Produces: `incept_diagram.py` — `request_diagram(spec, live=False)` (POST `image`/`drawio`), `fetch(artifact_id, dest_dir, live=False)` (download the `.drawio` + PNG to a LOCAL hosted dir, return local relative paths), `verify_drawio(drawio_path, expected_labels)` (parse the XML, assert every expected label appears verbatim — the anti-garble check, mirrors `verify_svg`).
- Produces: `pipeline/incept_diagrams.py` — `INCEPT_DIAGRAMS: dict[(lesson_id, slot_idx_1based)] -> (png_url_or_path, alt_caption)`. Populated by the bind step; consumed by gated_reading.
- Modifies: in `gated_reading.build_lesson_html`, after the existing `_DIAGRAMS` lookup, add `incept_png = _INCEPT_DIAGRAMS.get((L.id, idx+1))` and pass `img=incept_png` to `_content_card` when present (SVG stays `svg=`; Incept PNG uses `img=`). A slot never gets both.

- [ ] **Step 1: Write the failing test** — `verify_drawio` PASSES on the probe's saved `C:/tmp/incept_probe/arguable_claim.drawio` (labels SIDE/REASON/ARGUABLE CLAIM present) and FAILS on a drawio with a missing expected label; `_content_card(img=...)` renders the PNG into the card (import from gated_reading).
- [ ] **Step 2: Run → fail.**
- [ ] **Step 3: Implement** the three `incept_diagram` fns + the registry module + the gated_reading hook (mirror the `_DIAGRAMS` line already at gated_reading.py ~L580).
- [ ] **Step 4: Run → pass.**
- [ ] **Step 5:** full pytest green; `python pipeline/tier_a_regression.py G9` still clean (adding an empty `_INCEPT_DIAGRAMS` changes nothing).
- [ ] **Step 6: Commit** (`feat(incept): incept_diagram.py + _INCEPT_DIAGRAMS binding via _content_card(img=)`).

---

### Task 4 (Phase C): `incept_question_seeds.py` — distractor assist (seed-only)

**Files:**
- Create: `pipeline/incept_question_seeds.py`
- Test: `pipeline/tests/test_incept_question_seeds.py`

**Interfaces:**
- Produces: `seed_distractors(skill_prompt, existing_options, n=3, live=False)` — POST `question` (`interaction_type: multiple_choice`, `structure: bank`), returns candidate distractor texts. These are RAW MATERIAL for an authoring agent, never pushed directly.
- Produces: a clear docstring + a `SEEDS_ARE_NOT_ITEMS` guard note: seeds must pass `gate_structural_item` + anti-slop + provenance after an author selects/edits them.

- [ ] **Step 1: Write the failing test** — dry mode returns the would-send body for a `question` bank request with the skill prompt; a parse helper turns a synthetic Incept `question` response into a list of distractor strings.
- [ ] **Step 2-4: TDD** implement + pass.
- [ ] **Step 5:** full pytest green.
- [ ] **Step 6: Commit** (`feat(incept): incept_question_seeds.py - distractor seeds (raw material, gated downstream)`).

---

### Task 5 (Phase E): `openai_diverse.py` — cross-model diversity check

**Files:**
- Create: `pipeline/openai_diverse.py`
- Test: `pipeline/tests/test_openai_diverse.py`

**Interfaces:**
- Produces: `second_opinion(kind, content, prompt, live=False)` — a thin OpenAI (gpt) call that acts as an independent AUTHOR-or-JUDGE second opinion on an item/claim, for diversity against Claude/Fable/Incept. Dry by default; reads `OPEN_AI_API_KEY` from `HS Writing/.env` (confirmed present; never log). Advisory only.
- Produces: doc note that OpenAI's IMAGE role is retired in favor of Incept drawio (per strategy doc); this module is the diversity-check role only.

- [ ] **Step 1: Write the failing test** — dry mode returns the would-send request; key read + redacted (no `sk-` in repr).
- [ ] **Step 2-4: TDD** implement + pass (dry-mode only tested; live path exercised in Task 7).
- [ ] **Step 5:** full pytest green.
- [ ] **Step 6: Commit** (`feat(incept): openai_diverse.py - cross-model second-opinion (diversity), dry-by-default`).

---

### Task 6: Phase D — the post-lock VIDEO stage (machinery only; runs after next full build)

**Files:**
- Create: `pipeline/incept_video.py`, `docs/superpowers/specs/video-stage-README.md`
- Test: `pipeline/tests/test_incept_video.py`

**Interfaces:**
- Produces: `video_targets(grade) -> list[(lesson_id, slot_idx)]` — the curated selection (starts with a hardcoded seed list: the LS-flagged foundational lessons, e.g. G9 L01); NOT every lesson.
- Produces: `generate_video(lesson_id, live=False)` (POST `video`, voiceover, from the LOCKED lesson's teach text), `fetch_video(artifact_id, dest)` (download mp4 + captions.vtt + scene PNGs), `reconcile_questions(video_json, lesson)` (flag embedded `questions[]` that DUPLICATE the lesson's existing discriminations — the probe showed Q1 ≈ our slot-4), `bind_note(...)` (records HOW the video would bind as an opening stimulus + the DELIVERY caveat: interactive-in-Timeback is unresolved; plain voiceover-as-stimulus is the near-term target).
- **This stage does NOT run in this plan's execution** beyond building + testing the machinery; per Noel it runs AFTER the next full build (video is post-content-lock by design). The README documents the run order.

- [ ] **Step 1: Write the failing test** — `reconcile_questions` flags a video question whose stem ~matches an existing discrimination stem (use the probe's Q1 vs our L01 slot-4); `video_targets("g9")` returns the seed list incl. C901-0001; dry `generate_video` echoes a `video` request body.
- [ ] **Step 2-4: TDD** implement + pass.
- [ ] **Step 5:** full pytest green.
- [ ] **Step 6: Commit** (`feat(incept): incept_video.py - post-lock video stage machinery (runs after next full build)`).

---

### Task 7: First real batch — deliberate `--live` generation (Noel-gated)

**Files:** writes into `pipeline/incept_diagrams.py` (registry), `pipeline/incept_qc_receipts.json`, and a local hosted-asset dir; may modify the target lesson files to bind diagrams.

**This task makes REAL Incept calls (spends quota, sends content out). It runs only on Noel's explicit go, as a `--live` invocation.**

- [ ] **Step 1: QC the 126 rollout discriminations (advisory).** `python pipeline/incept_qc.py --grade all --live` → writes redacted receipts. Then `low_scoring(85)` → the human-review shortlist. Report the shortlist; do NOT auto-change lessons — surface for review.
- [ ] **Step 2: Generate drawio diagrams for the ~10 highest-value teach slots.** Seed list (abstract writing-structure diagrams that beat prose): G9 L01 claim anatomy, G9 warrant, G10 device→effect→warrant, G11/G12 synthesis weave, etc. `python pipeline/incept_diagram.py --targets <seedfile> --live`. For each: `verify_drawio` (labels present), confirm `below_bar` false, download PNG to the hosted dir.
- [ ] **Step 2b:** review each PNG (open them); reject any below-bar or garbled; re-generate as needed.
- [ ] **Step 3: Bind the approved diagrams.** Populate `_INCEPT_DIAGRAMS` with the (lesson, slot)→PNG entries; re-run `tier_a_regression` for the touched grades → still clean (the PNG is display-only, no gate impact); spot-render the lessons.
- [ ] **Step 4: Verify + commit** — full pytest green; touched grades clean. Commit the registry + bound lessons + the redacted QC receipts (NO URLs/secrets). Report quota spent (count of live calls).

---

### Task 8: Update strategy doc + roadmap status

**Files:** Modify `INCEPT_INTEGRATION.md` (mark phases A-E built; record the first-batch results + QC shortlist), `pipeline/course_sequence_g9_12.py` (no change; the spacing TODO already there).

- [ ] **Step 1:** update the roadmap table (phase → built/generated), note the video stage is machinery-ready and runs after the next full build, and link the QC shortlist for the review that feeds the next content pass.
- [ ] **Step 2: Commit** (`docs: Incept phases A-E built + first-batch results`).

## Self-Review notes (author)
- **Dry/live discipline is the spine:** Tasks 1-6 build + test everything with ZERO network calls (all tests use live=False). Only Task 7 is live, and it's explicitly Noel-gated. This is what makes "build machinery now, generate a first batch" safe.
- **Secret hygiene is a hard constraint, repeated per task:** the Incept key and the presigned S3 URLs are secret-bearing; receipts store scores/axes only, never URLs/prompts/content. A test asserts the key never appears in repr.
- **QC advisory, not blocking (Noel):** no Incept verdict fails the build; `low_scoring` surfaces a review shortlist that feeds the NEXT content pass, keeping our build offline-deterministic.
- **Video is post-lock (Noel):** Task 6 builds + tests the machinery but does NOT generate/bind video in this plan; it runs after the next full build. The reconcile_questions step guards against the video's embedded questions duplicating our gated checks.
- **Everything re-enters the contract:** diagrams pass verify_drawio + display-only (no student-facing text to garble); question-seeds are raw material gated downstream; nothing Incept makes is pushed unreviewed.
- **Not built here:** interactive-video delivery in Timeback (unresolved player question — flagged, not assumed); bulk diagram generation beyond the ~10 seed slots (waits for review of the first batch).
