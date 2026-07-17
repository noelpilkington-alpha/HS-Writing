# Retire Orphan Whole-Essay-Plan Lessons Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eliminate "orphan" lessons that make a student plan a whole essay and then never write it, by folding the planning teaching into the essay lessons that already write from a plan — so no plan is a dead artifact and no outline is scored on an essay rubric.

**Architecture:** A content re-architecture in the lesson banks + mastery maps. No pipeline/renderer/gate code changes. Every move is teach→model→plan→write inside ONE lesson — the pattern the full-essay lessons already ship — so it is Timeback-native (only existing display + FRQ + choice slot kinds).

**Tech Stack:** The `Alpha HS Writing Course 2026-27` Python lesson banks (`Lesson_Bank_G9/`, `Lesson_Bank_G10/`), mastery maps (`pipeline/mastery_prompts_g9.py`, `pipeline/mastery_prompts_g10.py`, `pipeline/g9_push_mastery_v3_1.py`), verified by `pipeline/tier_a_regression.py` + `pipeline/tests/`.

## Global Constraints

- **Lesson IDs are STABLE** (grader + mastery keyed by id). Do NOT rename a surviving lesson's id. Retiring a lesson = move its file to a `_deprecated_*` dir AND remove its mastery entries, never leave a dangling id.
- **No em dashes** in student-facing text.
- **Copyright:** own-words only; TWR labels used as structure, Appendix/Exhibit cites internal only.
- **Timeback-native only:** display / extended-text FRQ / choice slot kinds. No new interaction types.
- **Every touched lesson must end 100/100 clean on `tier_a_regression.py`** and the full `pytest pipeline/tests/` suite stays green.
- **KC discipline:** the C-code in the id IS the KC. Retiring within a KC is a within-KC re-sequence; do NOT retire the last lesson carrying a KC without confirming the KC is still represented.
- **Verified orphan set (do NOT expand without re-running the orphan test in Task 1):** exactly TWO true whole-essay-plan orphans — `ACC-W910-L-G9-C904-0019` (MPO) and `ACC-W910-L-G10-C1006-0020` (cross-text planner). `ACC-W910-L-G9-C901-0022` is a SEPARATE case (different KC, mode-decision skill) handled in Task 4, NOT retired.

---

### Task 1: Confirm the orphan set + fold targets against current code (no edits)

**Files:**
- Read only: `Lesson_Bank_G9/lesson_g9_l20_spo_plan_v3_1.py`, `Lesson_Bank_G9/lesson_g9_l23_full_argument_essay_v3_1.py`, `Lesson_Bank_G9/lesson_g9_l24_full_informational_essay_v3_1.py`, `Lesson_Bank_G10/lesson_g10_l20_plan_cross_text.py`, `Lesson_Bank_G10/lesson_g10_l21_analysis_essay.py`, `Lesson_Bank_G10/lesson_g10_l22_argument_essay.py`

**Interfaces:**
- Consumes: the orphan-detection query below.
- Produces: a confirmed map `{orphan_id -> fold_target_lesson_id}`:
  - `ACC-W910-L-G9-C904-0019` → fold its "two-level planning (SPO→MPO)" teaching into BOTH `C904-0023` (argument) and `C904-0024` (informational); retire the standalone.
  - `ACC-W910-L-G10-C1006-0020` → fold its "plan cross-text point-by-point" teaching into `C1006-0021` (analysis) and `C1006-0022` (argument); retire the standalone.

- [ ] **Step 1: Re-run the orphan test to confirm exactly 2 whole-essay-plan orphans (+ the C901-0022 edge case) still hold**

Run:
```
python - <<'PY'
import sys, re, glob; sys.path.insert(0,'pipeline')
from g9_push_dryrun import _load
from mastery_targets_grade import _GRADE_GLOB
def plain(h): return re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',h or '')).strip().lower()
hits=[]
for g in ['G9','G10','G11','G12']:
    sub,pat=_GRADE_GLOB[g]
    for f in sorted(glob.glob(sub+'/'+pat)):
        if '_deprecated' in f: continue
        m=_load(f); L=getattr(m,'LESSON',None) or (getattr(m,'LESSONS',[None]) or [None])[0]
        if not L: continue
        prods=[s for s in L.slots if s.kind=='production_frq']; units=[getattr(s,'unit','') for s in prods]
        if 'essay' in units: continue
        ind=[s for s in prods if s.role=='INDEPENDENT']
        if not ind: continue
        b=plain(ind[0].body)
        if ('outline' in b or 'plan' in b) and 'essay' in b and ('thesis' in b or 'controlling idea' in b or 'body point' in b or 'body paragraph' in b):
            hits.append((L.id, L.title))
for x in hits: print(x)
PY
```
Expected: exactly `C904-0019`, `C901-0022`, `C1006-0020`. If the set differs, STOP and reconcile with the human before proceeding.

- [ ] **Step 2: Confirm each fold target already teaches + writes plan→essay in one lesson**

Run (for each of C904-0023, C904-0024, C1006-0021, C1006-0022):
```
python -c "import sys,re;sys.path.insert(0,'pipeline');from g9_push_dryrun import _load;m=_load('<FILE>');L=getattr(m,'LESSON',None) or (getattr(m,'LESSONS',[None]) or [None])[0];print(L.id,[(s.role,s.kind,getattr(s,'unit','')) for s in L.slots if s.kind in ('teach_card','production_frq')])"
```
Expected: each has a TEACH teach_card + a SUPPORTED multi_paragraph plan write + an INDEPENDENT essay write. Confirms the fold target is real. No edits this task.

---

### Task 2: Fold the MPO teaching into the G9 essay lessons (C904-0023, C904-0024)

**Files:**
- Read: `Lesson_Bank_G9/lesson_g9_l20_spo_plan_v3_1.py` (source of the teaching to migrate)
- Modify: `Lesson_Bank_G9/lesson_g9_l23_full_argument_essay_v3_1.py`, `Lesson_Bank_G9/lesson_g9_l24_full_informational_essay_v3_1.py`

**Interfaces:**
- Consumes: the MPO "two-level planning" teach content — the ONE_IDEA beat: *"An essay is planned at two levels: one thesis that governs the whole essay, then a multiple-paragraph outline under it (introduction, ordered body paragraphs each pairing a main idea with its details, and a conclusion). The single-paragraph outline plans ONE paragraph; the MPO arranges several into an essay."*
- Produces: each essay lesson's opening teach now names the two-level MPO concept before its existing plan→write arc. No new slots if the concept fits the existing first teach_card; else add ONE teach_card at the front.

- [ ] **Step 1: Verify current C904-0023 teaching does NOT already state the two-level MPO concept**

Run:
```
python -c "import sys,re;sys.path.insert(0,'pipeline');from g9_push_dryrun import _load;m=_load('Lesson_Bank_G9/lesson_g9_l23_full_argument_essay_v3_1.py');L=m.LESSON if hasattr(m,'LESSON') else m.LESSONS[0];print(re.sub(r'<[^>]+>',' ',L.slots[0].body)[:300])"
```
Expected: it says "an essay is a plan, built out" but does NOT explicitly contrast the SPO (one-paragraph) vs MPO (whole-essay) two-level distinction. If it already does, this task is a no-op for that lesson — record and skip to Task 3.

- [ ] **Step 2: Add the two-level MPO sentence to C904-0023's opening teach_card**

Edit the first teach_card's ONE_IDEA body to include (own words, no em dash): a sentence establishing that an argument essay is planned at two levels — one governing thesis, then an outline of ordered body paragraphs (each a claim + its evidence) framed by an intro and conclusion — and that this is bigger than the single-paragraph outline they already know. Keep the existing "plan, built out" framing; this augments, does not replace.

- [ ] **Step 3: Add the parallel two-level sentence to C904-0024 (informational variant)**

Same as Step 2 but for the explain mode: thesis = a controlling idea (no side), body rows = ordered stages each with details from the source.

- [ ] **Step 4: Verify both lessons pass contract + render**

Run for each file:
```
python -c "import sys,re;sys.path.insert(0,'pipeline');from g9_push_dryrun import _load;import lesson_contract as LC;from gated_reading import build_lesson_html,render_qc;m=_load('<FILE>');L=m.LESSON if hasattr(m,'LESSON') else m.LESSONS[0];qc=LC.qc_lesson(L);h,c=build_lesson_html(L,base_url='https://x/y');print(L.id,'contract',qc['passed'],qc['first_failure'],'render',render_qc(h,c,lessons=L) or 'CLEAN')"
```
Expected: `contract True None render CLEAN` for both.

- [ ] **Step 5: Commit**
```
git add "Alpha HS Writing Course 2026-27/Lesson_Bank_G9/lesson_g9_l23_full_argument_essay_v3_1.py" "Alpha HS Writing Course 2026-27/Lesson_Bank_G9/lesson_g9_l24_full_informational_essay_v3_1.py"
git commit -m "content(g9): fold two-level MPO teaching into the full-essay lessons (pre-retire the standalone MPO)"
```

---

### Task 3: Retire the standalone G9 MPO lesson (C904-0019) + drop its mastery

**Files:**
- Move: `Lesson_Bank_G9/lesson_g9_l20_spo_plan_v3_1.py` → `Lesson_Bank_G9/_deprecated_orphan_planning/lesson_g9_l20_spo_plan_v3_1.py`
- Modify: `pipeline/mastery_prompts_g9.py` (remove the `ACC-W910-L-G9-C904-0019` entry), `pipeline/g9_push_mastery_v3_1.py` (remove its HELDOUT line)

**Interfaces:**
- Consumes: the fold from Task 2 (the teaching now lives in C904-0023/0024).
- Produces: C904-0019 no longer loads as a live lesson; no mastery entry references it; the C904 KC is still represented by C904-0020…0029.

- [ ] **Step 1: Confirm the MPO teaching is now in the fold targets (guard against losing content)**

Run: grep the two-level concept in C904-0023 and C904-0024 bodies; both must contain it (from Task 2). If either is missing, STOP — do not retire until the content is preserved.

- [ ] **Step 2: Move the lesson file to the deprecated dir**
```
mkdir -p "Lesson_Bank_G9/_deprecated_orphan_planning"
git mv "Lesson_Bank_G9/lesson_g9_l20_spo_plan_v3_1.py" "Lesson_Bank_G9/_deprecated_orphan_planning/lesson_g9_l20_spo_plan_v3_1.py"
```
(The `_deprecated` substring is already excluded by every loader's glob filter — verified in `_GRADE_GLOB` consumers.)

- [ ] **Step 3: Remove the mastery entries for C904-0019**

In `pipeline/mastery_prompts_g9.py`: delete the `"ACC-W910-L-G9-C904-0019": {...}` dict entry (lines ~208-215).
In `pipeline/g9_push_mastery_v3_1.py`: delete the `"ACC-W910-L-G9-C904-0019": "ACC-W910-INFO-LESSON-HIGHWAYS",` HELDOUT line (~136).

- [ ] **Step 4: Verify the id is fully gone + G9 still clean**

Run:
```
grep -rn "C904-0019" pipeline/ Lesson_Bank_G9/*.py || echo "no live references"
python pipeline/tier_a_regression.py G9 2>&1 | grep "=== TIER-A"
python -c "import sys;sys.path.insert(0,'pipeline');from mastery_targets_grade import _authored;print('C904-0019 in mastery:', 'ACC-W910-L-G9-C904-0019' in _authored('G9'))"
```
Expected: no live references (only the deprecated file + this plan), G9 27→26 lessons all clean, `C904-0019 in mastery: False`.

- [ ] **Step 5: Commit**
```
git add -A "Alpha HS Writing Course 2026-27/Lesson_Bank_G9" "Alpha HS Writing Course 2026-27/pipeline/mastery_prompts_g9.py" "Alpha HS Writing Course 2026-27/pipeline/g9_push_mastery_v3_1.py"
git commit -m "content(g9): retire standalone MPO lesson C904-0019 (teaching folded into C904-0023/0024); drop its mastery"
```

---

### Task 4: G9 mode-decision lesson (C901-0022) — honest reframe, NOT retire

**Files:**
- Read then Modify: `Lesson_Bank_G9/lesson_g9_l19_essay_mode_interleave_v3_1.py`

**Interfaces:**
- Consumes: nothing from prior tasks.
- Produces: C901-0022 stays live (it is a distinct KC — C901 claim/mode-decision — teaching "the task verb decides the essay's mode," not MPO planning). Its terminal write produces a mode-appropriate plan; the fix is to make that write HONEST, not to retire it.

- [ ] **Step 1: Read the lesson + decide keep-vs-fold with the human's Task-1 map**

Confirm C901-0022 teaches mode-classification (argue vs explain from the verb), a genuinely different skill from MPO planning. Because it is a different KC and a real sub-skill, the decision is KEEP. Its only defect is the same orphan-plan-write shape.

- [ ] **Step 2: Reframe its plan-write to a mode-decision deliverable (not a full-essay plan that goes nowhere)**

Edit the INDEPENDENT (and SUPPORTED/TRANSFER) production_frq bodies so the graded product is the MODE DECISION + a one-line thesis of the right mode (the actual skill), NOT a full multi-paragraph outline. This removes the "plan a whole essay, never write it" shape while keeping the mode-classification skill intact. Keep unit as-is unless the write is clearly now a sentence-grain product (then set `unit="sentence"` to match).

- [ ] **Step 3: Verify + commit**

Run the contract+render check (as Task 2 Step 4). Expected clean.
```
git add "Alpha HS Writing Course 2026-27/Lesson_Bank_G9/lesson_g9_l19_essay_mode_interleave_v3_1.py"
git commit -m "content(g9): reframe C901-0022 write to the mode-decision deliverable (kill the orphan whole-essay plan; keep the KC)"
```

---

### Task 5: Apply the same collapse to the G10 cross-text planner (C1006-0020)

**Files:**
- Read: `Lesson_Bank_G10/lesson_g10_l20_plan_cross_text.py` (teaching to migrate)
- Modify: `Lesson_Bank_G10/lesson_g10_l21_analysis_essay.py`, `Lesson_Bank_G10/lesson_g10_l22_argument_essay.py` (fold targets)
- Move: `Lesson_Bank_G10/lesson_g10_l20_plan_cross_text.py` → `Lesson_Bank_G10/_deprecated_orphan_planning/`
- Modify: `pipeline/mastery_prompts_g10.py`, and the G10 HELDOUT map (find it: `grep -rn "C1006-0020" pipeline/`)

**Interfaces:**
- Consumes: the same pattern proven in Tasks 2-3.
- Produces: C1006-0020's "plan cross-text point-by-point, not source-by-source" teaching folded into the cross-text essay lessons; standalone retired; mastery dropped.

- [ ] **Step 1: Confirm C1006-0021 and C1006-0022 each teach + write a cross-text essay (fold target real)**

Run the slot-arc check (Task 1 Step 2 form) on both. Expected: teach + SUPPORTED plan + INDEPENDENT essay.

- [ ] **Step 2: Fold the "point-by-point not source-by-source" teaching into C1006-0021 and C1006-0022**

Add the cross-text planning beat (own words) to each lesson's opening teach: plan a cross-text essay as ordered POINTS that each weave the sources, not one source then the next. Augment, do not replace existing teaching.

- [ ] **Step 3: Verify the teaching is preserved, then retire C1006-0020**
```
mkdir -p "Lesson_Bank_G10/_deprecated_orphan_planning"
git mv "Lesson_Bank_G10/lesson_g10_l20_plan_cross_text.py" "Lesson_Bank_G10/_deprecated_orphan_planning/lesson_g10_l20_plan_cross_text.py"
```
Remove the `C1006-0020` entry from `pipeline/mastery_prompts_g10.py` and its HELDOUT line (path from the grep above).

- [ ] **Step 4: Verify id gone + G10 clean**

Run: `grep -rn "C1006-0020" pipeline/ Lesson_Bank_G10/*.py || echo none`; `python pipeline/tier_a_regression.py G10 | grep "=== TIER-A"`. Expected: no live refs, G10 26→25 all clean.

- [ ] **Step 5: Commit**
```
git add -A "Alpha HS Writing Course 2026-27/Lesson_Bank_G10" "Alpha HS Writing Course 2026-27/pipeline/mastery_prompts_g10.py"
git commit -m "content(g10): fold cross-text planning into the essay lessons; retire standalone planner C1006-0020"
```

---

### Task 6: Full-course regression + preview + plan-doc update

**Files:**
- Read/verify: whole course via `pipeline/tier_a_regression.py`, `pipeline/tests/`
- Modify: `COURSE_FIX_PLAN_synthesis.md` (replace F3 with a pointer to this completed re-architecture)

- [ ] **Step 1: Full deterministic floor + test suite**
```
python pipeline/tier_a_regression.py all 2>&1 | grep "=== TIER-A"
python -m pytest pipeline/tests/ -q 2>&1 | tail -2
```
Expected: `TIER-A: 98/98 lessons clean` (100 − 2 retired), all tests green. If any lesson fails, fix before continuing.

- [ ] **Step 2: Confirm lesson counts dropped exactly as intended**
```
python -c "import sys,glob;sys.path.insert(0,'pipeline');from mastery_targets_grade import _GRADE_GLOB;[print(g, len([f for f in glob.glob(_GRADE_GLOB[g][0]+'/'+_GRADE_GLOB[g][1]) if '_deprecated' not in f])) for g in ['G9','G10','G11','G12']]"
```
Expected: G9 26 (was 27), G10 25 (was 26), G11 31, G12 16.

- [ ] **Step 3: Re-render all 4 grades + redeploy the Vercel preview**
```
DEPLOY="c:/Users/noelp/AppData/Local/Temp/vercel_deploy"
for g in G9 G10 G11 G12; do python pipeline/render_course_preview_grade.py $g --deploy "$DEPLOY"; done
cd "$DEPLOY" && vercel deploy --prod --yes
```
Expected: renders clean, deploy READY + aliased.

- [ ] **Step 4: Update F3 in the fix plan to reflect the re-architecture**

In `COURSE_FIX_PLAN_synthesis.md`, replace the F3 entry (which said "MPO rides on T1-A") with: "RESOLVED by retiring the orphan whole-essay-plan lessons (C904-0019, C1006-0020) and folding their teaching into the essay lessons that write from a plan — see docs/superpowers/plans/2026-07-17-retire-orphan-planning-lessons.md. The rubric-mismatch dissolves: outlines are no longer scored standalone."
```
git add "Alpha HS Writing Course 2026-27/COURSE_FIX_PLAN_synthesis.md"
git commit -m "docs: F3 resolved by orphan-planning retire/fold re-architecture"
```

## Self-Review notes (author)

- **Scope corrected during planning:** the orphan set is 2 true whole-essay-plan lessons (C904-0019, C1006-0020), NOT the "3 G9 planners" first proposed — L21 (order paragraphs) and L22 (intro/conclusion) are genuine sub-skills whose paragraph writes are real deliverables, so they are KEPT untouched. C901-0022 is a separate KC handled by reframe, not retire. This is why Task 1 re-confirms before any edit.
- **Content-loss guard:** every retire (Task 3, Task 5) is gated on a Step that verifies the teaching now lives in the fold target first.
- **Blast radius:** within-KC only (C904, C1006); ids retired cleanly (file moved + mastery removed), never left dangling. No pipeline/gate/renderer code touched.
- **Not addressed here (deliberately):** the broader T1-A/B feedback-resolution work — separate plan; this one only removes the orphan-planning redundancy the human flagged.
