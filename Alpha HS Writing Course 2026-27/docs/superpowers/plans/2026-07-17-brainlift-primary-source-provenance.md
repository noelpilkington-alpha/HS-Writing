# BrainLift Primary-Source Provenance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite the HS Writing Course Design BrainLift's Knowledge Tree to cite primary sources (external authorities + published experts) instead of derived artifact files, backed by a standalone Primary Source Register and a source-first spreadsheet.

**Architecture:** Four sequential deliverables. (1) A **harvest** step extracts every embedded authoritative URL from the derived files into a machine-readable JSON, and a **B-pass** attaches live authorities to the two zero-URL compilation files' load-bearing claims. (2) The **Primary Source Register** (`.md`) is authored from that JSON + the 17 experts already in the BrainLift. (3) The **`.docx` Knowledge Tree** `Sources:` lists are rewritten via python-docx to cite primary sources with artifacts demoted to back-pointers. (4) The existing **spreadsheet** is reoriented source-first. Each task ends with a concrete verification command; this is documentation generation, so "tests" are structural assertions over the produced files, not pytest of product code.

**Tech Stack:** Python 3 (stdlib `re`, `json`, `csv`; `python-docx` for the .docx; `openpyxl` for the xlsx — both confirmed installed), Git Bash, the WebFetch tool for the B-pass web-verification.

## Global Constraints

- **Two citable source types ONLY:** external authorities (state-DOE pages/PDFs, test-vendor blueprints/rubrics, released forms) and published experts (the 17 in the BrainLift Experts section). Internal decisions and conversation/research-run provenance are NEVER cited as a source — only as labels/back-pointers.
- **Design-bet claims:** cite the expert the bet derives from AND keep the honest grade label verbatim (e.g. "Grade-C / design bet, unvalidated for writing"). Never launder a bet into an evidence claim.
- **Register granularity: category-representative** — ~4–8 load-bearing sources per Knowledge-Tree category (~35–45 total), NOT an exhaustive harvest of all ~200 URLs.
- **Edit target:** ONLY `Brainlifts/HS Writing Course Design Brainlift - Stakeholder Edition.docx` (course folder). The original at `Writing_Brainlift/HS Writing Course Design Brainlift - Stakeholder Edition.md` is LEFT UNTOUCHED — never open it for write.
- **Edit scope inside the .docx:** ONLY the Knowledge Tree `Sources:` lists (Categories 1–7) and any Summary/Insight sentence that names a file *as a source*. Experts, Spiky POV, Research Insights, Timeback-vs-AlphaWrite, and Next Steps sections are OUT of scope.
- **No em dashes** in any authored prose (house rule): use commas/colons/parens.
- **B-pass fallback:** attach a live authority per load-bearing claim; only where genuinely unrecoverable after a real WebFetch attempt, record a dated gap note (documented C fallback, not the default).
- **Working dir for all commands:** `c:/Users/noelp/HS Writing/Alpha HS Writing Course 2026-27` (referred to below as `$COURSE`). Git repo root is `c:/Users/noelp/HS Writing`.
- Commit after each task. Branch: `hs-writing-spec-baseline` (already on it; not main).

---

### Task 1: Harvest authoritative URLs + build the source-index JSON

**Files:**
- Create: `$COURSE/pipeline/brainlift_sources/harvest_sources.py`
- Create (output): `$COURSE/pipeline/brainlift_sources/source_index.json`

**Interfaces:**
- Produces: `source_index.json` = `{"by_file": {relpath: [url,...]}, "all_urls": {url: [relpath,...]}}` — the deduplicated URL→files inverse index every later task consumes to pick load-bearing sources.

- [ ] **Step 1: Write the harvester**

Create `harvest_sources.py`. It scans the cited derived files, extracts `https?://` URLs, strips trailing punctuation, and writes the forward + inverse index.

```python
"""Harvest authoritative URLs embedded in the BrainLift's cited derived files.
Output: source_index.json  {by_file, all_urls}. Pure stdlib."""
import os, re, json

COURSE = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))

# The cited derived files that carry embedded primary-source URLs (Categories 1-2).
FILES = [
    "01_ccss_adherence_map.md", "02_deviation_states_deepdive.md",
    "04_item_formats_and_rubrics.md",
    "06a_deviation_AL_AR.md", "06b_deviation_ID_ME.md", "06c_deviation_ND_WI.md",
    "AnchorSets/G10_anchor_forms.md", "AnchorSets/G11_anchor_ACT.md",
    "AnchorSets/G11_anchor_AP_Lang.md", "AnchorSets/G11_anchor_SBAC.md",
    # zero-URL compilation files (B-pass targets): scanned so their empty result is explicit
    "03_state_assessment_format_map.md", "TestDesign_Reference.md", "TestBank_Blueprint.md",
]
URL_RE = re.compile(r'https?://[^\s)"\'>\]]+')

def clean(u):
    return u.rstrip('.,;:)]}>"\'')

by_file, all_urls = {}, {}
for rel in FILES:
    p = os.path.join(COURSE, rel)
    urls = []
    if os.path.isfile(p):
        with open(p, encoding="utf-8", errors="replace") as fh:
            urls = sorted({clean(u) for u in URL_RE.findall(fh.read())})
    by_file[rel] = urls
    for u in urls:
        all_urls.setdefault(u, []).append(rel)

out = {"by_file": by_file, "all_urls": {u: sorted(f) for u, f in sorted(all_urls.items())}}
dest = os.path.join(os.path.dirname(__file__), "source_index.json")
with open(dest, "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=2, ensure_ascii=False)

print(f"files scanned: {len(FILES)}")
print(f"unique URLs: {len(all_urls)}")
for rel, urls in by_file.items():
    print(f"  {len(urls):3d}  {rel}")
print(f"wrote {dest}")
```

- [ ] **Step 2: Run it and verify the harvest**

Run: `cd "$COURSE" && python pipeline/brainlift_sources/harvest_sources.py`
Expected: prints per-file counts matching the known baseline (01=51, 04=41, G10_anchor_forms=55, 03=0, TestDesign=0), a unique-URL total ~120-150, and "wrote …/source_index.json".

- [ ] **Step 3: Verify the JSON is well-formed and the zero-URL files are captured as empty**

Run: `cd "$COURSE" && python -c "import json;d=json.load(open('pipeline/brainlift_sources/source_index.json',encoding='utf-8'));print('unique',len(d['all_urls']));print('03 urls',len(d['by_file']['03_state_assessment_format_map.md']));print('TestDesign urls',len(d['by_file']['TestDesign_Reference.md']));print('01 urls',len(d['by_file']['01_ccss_adherence_map.md']))"`
Expected: `unique 12x`, `03 urls 0`, `TestDesign urls 0`, `01 urls 51`.

- [ ] **Step 4: Commit**

```bash
cd "c:/Users/noelp/HS Writing"
git add "Alpha HS Writing Course 2026-27/pipeline/brainlift_sources/harvest_sources.py" "Alpha HS Writing Course 2026-27/pipeline/brainlift_sources/source_index.json"
git commit -m "feat(brainlift-sources): harvest embedded authoritative URLs into source_index.json"
```

---

### Task 2: B-pass — attach live authorities to the two zero-URL files' load-bearing claims

**Files:**
- Create: `$COURSE/pipeline/brainlift_sources/bpass_claims.json`

**Interfaces:**
- Consumes: `source_index.json` (Task 1) for sibling-recovery.
- Produces: `bpass_claims.json` = list of `{"claim": str, "file": "03_…"|"TestDesign_…", "authority": str, "url": str, "recovery": "sibling"|"web"|"gap", "note": str}` — consumed by Task 3 (register) + Task 4 (docx) for Category-2 sourcing.

- [ ] **Step 1: Enumerate the load-bearing claims of the two files**

Read `03_state_assessment_format_map.md` and `TestDesign_Reference.md`. Extract the load-bearing claims (the grade→exam mapping, per-state assessment format rows, and rubric trait/scale facts). Read commands:
Run: `cd "$COURSE" && grep -nE "STAAR|Regents|SBAC|ACT|AP |MCAS|Keystone|ECR|PCR|TDA|rubric|trait|scale|holistic|analytic" 03_state_assessment_format_map.md | head -40`
Run: `cd "$COURSE" && grep -nE "STAAR|Regents|SBAC|ACT|AP |trait|scale|0-4|1-6|holistic|analytic|Conventions" TestDesign_Reference.md | head -40`
List the ~10-15 distinct load-bearing claims (write them down for Step 2).

- [ ] **Step 2: Sibling-recover each claim against source_index.json**

For each claim, check whether an authoritative URL already exists in `01`/`02`/`04`/`06`/anchor sets that grounds it (e.g. "STAAR English II = evidence-based ECR + SCR" → the TEA/texasassessment.gov URL in `04`). Inspect candidates:
Run: `cd "$COURSE" && python -c "import json;d=json.load(open('pipeline/brainlift_sources/source_index.json',encoding='utf-8'));[print(u) for u in d['all_urls'] if any(k in u.lower() for k in ('tea.texas','texasassessment','nysed','smarterbalanced','collegeboard','act.org','cognia','doe.'))]"`
Record each recovered claim as `{"recovery":"sibling","authority":...,"url":...}`.

- [ ] **Step 3: Web-verify the remainder**

For claims with NO home URL anywhere in the tree, use the WebFetch tool to fetch the authoritative source (state DOE assessment page or vendor blueprint) and capture the live URL + a one-line confirmation the page states the fact. Record as `{"recovery":"web",...}`. If a fetch genuinely fails (dead link, no authoritative page found after a real attempt), record `{"recovery":"gap","note":"traces to <authority> via <parent>; live URL not recovered 2026-07-17: <reason>"}`.

WebFetch targets to try (authoritative landing pages, verify then capture the exact deep link):
- STAAR (TX): `https://tea.texas.gov/student-assessment/testing/staar/staar-english-i-and-english-ii-resources`
- AP Lang: `https://apcentral.collegeboard.org/courses/ap-english-language-and-composition/exam`
- SBAC: `https://portal.smarterbalanced.org/library/en/elaliteracy-summative-assessment-blueprint.pdf`
- ACT Writing: `https://www.act.org/content/act/en/products-and-services/the-act/scores/writing-test-scores.html`
- NY Regents ELA: `https://www.nysedregents.org/hsela/`

- [ ] **Step 4: Write bpass_claims.json**

Create the file as the JSON list described in Interfaces, one object per load-bearing claim. Every object MUST have a non-empty `authority`; `url` non-empty unless `recovery=="gap"`.

- [ ] **Step 5: Verify no silent gaps and structural integrity**

Run: `cd "$COURSE" && python -c "import json;c=json.load(open('pipeline/brainlift_sources/bpass_claims.json',encoding='utf-8'));print('claims',len(c));print('gaps',sum(1 for x in c if x['recovery']=='gap'));assert all(x.get('authority') for x in c),'missing authority';assert all(x.get('url') or x['recovery']=='gap' for x in c),'missing url on non-gap';print('OK: every claim has an authority; every non-gap has a url')"`
Expected: prints claim count, gap count (ideally 0), and "OK: …". Any gap is printed for the record, not hidden.

- [ ] **Step 6: Commit**

```bash
cd "c:/Users/noelp/HS Writing"
git add "Alpha HS Writing Course 2026-27/pipeline/brainlift_sources/bpass_claims.json"
git commit -m "feat(brainlift-sources): B-pass live authorities for 03/TestDesign load-bearing claims"
```

---

### Task 3: Author the Primary Source Register

**Files:**
- Create: `$COURSE/BrainLift_Primary_Source_Register.md`

**Interfaces:**
- Consumes: `source_index.json` (Task 1), `bpass_claims.json` (Task 2), the Experts section of the `.docx`/`.md` BrainLift (the 17 experts + their publications, verbatim).
- Produces: the register `.md` — the audit artifact Task 4 points into and Task 5 mirrors.

- [ ] **Step 1: Pull the 17 expert citations verbatim**

Run: `cd "$COURSE" && python -c "import docx;d=docx.Document('Brainlifts/HS Writing Course Design Brainlift - Stakeholder Edition.docx');[print(p.text) for p in d.paragraphs if p.text.strip().startswith(('Expert ','Where:'))]"`
Expected: prints the 17 "Expert N: …" headers and their "Where:" publication lines. Use these verbatim as the Expert-type register entries (no drift).

- [ ] **Step 2: Select category-representative authorities**

For each Knowledge-Tree category, pick the ~4–8 load-bearing primary sources:
- **Cat 1 (Standards Backbone):** representative state-DOE standards URLs from `01`/`02`/`06` (e.g. TX TEKS, a CCSS-family exemplar, 2-3 deviation states) — pull from `source_index.json`.
- **Cat 2 (Exam Ground Truth):** vendor blueprints/rubrics + released forms from `04`/anchors + ALL `bpass_claims.json` authorities.
- **Cat 3 (Move Decomposition):** experts TWR, TSIS, Myhill, Anderson (+ label the shadow-inventory as internal-derived-from-TWR with grade label if applicable).
- **Cat 4 (Lesson Contract):** experts DI/Engelmann, Rosenshine, K&H, SRSD — design-bet claims (discrimination-before-production) cite Engelmann + KEEP the Grade-C label.
- **Cat 5 (Fading/Transfer/Calibration):** experts K&H (expertise reversal), Zimmerman, Wiliam & Hattie, SRSD.
- **Cat 6 (Scope/Ownership):** experts Hillocks (grammar-in-isolation), Myhill; authority = the CCSS/ACC standards for the ownership split.
- **Cat 7 (Progression/Architecture):** experts McCutchen (capacity theory), Hayes & Flower, UbD; authorities = the grade→exam mapping from `bpass_claims.json`.

- [ ] **Step 3: Write the register**

Create `BrainLift_Primary_Source_Register.md` with a header (purpose, date, the two-citable-types rule, granularity note) then one `## Category N` block per category. Under each, a table:

```markdown
| Source | Type | Grounds (claim / SPOV) | Reachable via | Compiled into (artifact, not source) |
|---|---|---|---|---|
| Texas TEA — STAAR English I/II assessment | Authority | Grade→exam map (G9/G10); ECR+SCR format | https://tea.texas.gov/... | 03_state_assessment_format_map.md, 04_item_formats_and_rubrics.md |
| Engelmann & Carnine, *Theory of Instruction* | Expert | Discrimination-before-production **(Grade-C / design bet, unvalidated for writing)** | NIFDI: nifdi.org | lesson_contract.py, G10_Model_Lesson_Specs.md |
```

Add a final `## B-pass recovery log` section listing every `bpass_claims.json` entry (claim · authority · url · recovery-type), so the audit trail for the two zero-URL files is explicit. No em dashes in prose.

- [ ] **Step 4: Verify coverage + honesty**

Run: `cd "$COURSE" && python -c "
t=open('BrainLift_Primary_Source_Register.md',encoding='utf-8').read()
import re
print('categories:',len(re.findall(r'^## Category',t,re.M)))
print('rows:',t.count('| Authority |')+t.count('| Expert |'))
print('grade-label preserved:', 'design bet' in t.lower() or 'grade-c' in t.lower())
print('bpass log present:', 'B-pass recovery log' in t)
print('no em-dash:', '—' not in t)
"`
Expected: `categories: 7`, rows ≥ 35, `grade-label preserved: True`, `bpass log present: True`, `no em-dash: True`.

- [ ] **Step 5: Commit**

```bash
cd "c:/Users/noelp/HS Writing"
git add "Alpha HS Writing Course 2026-27/BrainLift_Primary_Source_Register.md"
git commit -m "feat(brainlift): add Primary Source Register (category-representative audit artifact)"
```

---

### Task 4: Rewrite the Knowledge Tree `Sources:` lists in the .docx

**Files:**
- Modify: `$COURSE/Brainlifts/HS Writing Course Design Brainlift - Stakeholder Edition.docx`
- Create: `$COURSE/pipeline/brainlift_sources/rewrite_docx_sources.py`

**Interfaces:**
- Consumes: the register (Task 3) for the exact source strings per category; `source_index.json` + `bpass_claims.json` for URLs.
- Produces: the edited `.docx` (Knowledge Tree `Sources:` lists now cite primary sources).

- [ ] **Step 1: Map the Sources paragraphs to their categories**

Run: `cd "$COURSE" && python -c "
import docx;d=docx.Document('Brainlifts/HS Writing Course Design Brainlift - Stakeholder Edition.docx')
cat=None
for i,p in enumerate(d.paragraphs):
    t=p.text.strip()
    if t.startswith('Category '): cat=t[:40]
    if t=='Sources:' or t.startswith('Sources:'):
        # print the following bullet lines until next heading
        print(f'--- para {i} under [{cat}] ---')
"`
Expected: 7 `Sources:` anchors, each mapped to its Category heading. Note the paragraph indices.

- [ ] **Step 2: Back up the .docx**

Run: `cd "$COURSE" && cp "Brainlifts/HS Writing Course Design Brainlift - Stakeholder Edition.docx" "Brainlifts/HS Writing Course Design Brainlift - Stakeholder Edition.BACKUP.docx" && echo backed-up`
Expected: `backed-up`.

- [ ] **Step 3: Write the rewrite script**

Create `rewrite_docx_sources.py`. For each category it locates the `Sources:` paragraph and the artifact-bullet paragraphs that follow (until the next `Insights`/`Category`/heading), and rewrites them to primary-source citations with the artifact demoted to a "Compiled in:" tail. Because the source strings are category-specific and authored, encode them as an explicit `CATEGORY_SOURCES` dict in the script (filled from the register in Task 3 — copy the exact strings, do not regenerate).

```python
"""Rewrite the Knowledge Tree 'Sources:' lists in the .docx to cite primary
sources, artifacts demoted to a 'Compiled in:' back-pointer. Edits ONLY the
Sources lists of Categories 1-7. python-docx."""
import docx, sys, os

DOCX = os.path.join(os.path.dirname(__file__), "..", "..",
    "Brainlifts", "HS Writing Course Design Brainlift - Stakeholder Edition.docx")

# Exact strings copied from BrainLift_Primary_Source_Register.md (Task 3).
# key = the Category heading prefix; value = (primary_sources_line, compiled_in_line)
CATEGORY_SOURCES = {
    "Category 1": (
        "Sources (primary): [FILL from register Cat 1 — state-DOE standards authorities].",
        "Compiled in: 05_AlphaCommonCore_Writing_Spine.md, 01_ccss_adherence_map.md, 02_deviation_states_deepdive.md, 06a/06b/06c_deviation_*.md (artifacts; see Primary Source Register).",
    ),
    # ... Category 2..7, each filled verbatim from the register ...
}

def rewrite(dry=True):
    d = docx.Document(DOCX)
    cat = None
    changed = 0
    i = 0
    paras = d.paragraphs
    while i < len(paras):
        t = paras[i].text.strip()
        if t.startswith("Category "):
            cat = next((k for k in CATEGORY_SOURCES if t.startswith(k)), None)
        if cat and t.startswith("Sources:"):
            key = cat
            prim, comp = CATEGORY_SOURCES[key]
            # rewrite this paragraph as the primary-sources line
            paras[i].text = prim
            # delete following artifact bullets until the next heading, replace with the compiled-in line
            j = i + 1
            to_clear = []
            while j < len(paras):
                nt = paras[j].text.strip()
                if nt.startswith(("Insights", "Category ", "Sources:")) or paras[j].style.name.startswith("Heading"):
                    break
                if nt:
                    to_clear.append(j)
                j += 1
            if to_clear:
                paras[to_clear[0]].text = comp
                for k in to_clear[1:]:
                    paras[k].text = ""
            changed += 1
            cat = None
        i += 1
    if dry:
        print(f"[dry-run] would rewrite {changed} category Sources lists")
    else:
        d.save(DOCX)
        print(f"rewrote {changed} category Sources lists -> saved")

if __name__ == "__main__":
    rewrite(dry=("--apply" not in sys.argv))
```

- [ ] **Step 4: Fill CATEGORY_SOURCES from the register + dry-run**

Fill all 7 entries in `CATEGORY_SOURCES` with the exact primary-source strings from the register (Task 3). Then:
Run: `cd "$COURSE" && python pipeline/brainlift_sources/rewrite_docx_sources.py`
Expected: `[dry-run] would rewrite 7 category Sources lists`.

- [ ] **Step 5: Apply and verify**

Run: `cd "$COURSE" && python pipeline/brainlift_sources/rewrite_docx_sources.py --apply`
Expected: `rewrote 7 category Sources lists -> saved`.
Then verify the edit landed and no forbidden sections were touched:
Run: `cd "$COURSE" && python -c "
import docx;d=docx.Document('Brainlifts/HS Writing Course Design Brainlift - Stakeholder Edition.docx')
txt='\n'.join(p.text for p in d.paragraphs)
print('primary-source lines:', txt.count('Sources (primary):'))
print('compiled-in backpointers:', txt.count('Compiled in:'))
print('experts section intact:', 'Expert 11: Steve Graham' in txt)
print('POV section intact:', 'SPOV Truth 1' in txt)
print('grade label intact:', 'design bet' in txt.lower())
print('no em-dash added:', txt.count('—'))
"`
Expected: `primary-source lines: 7`, `compiled-in backpointers: 7`, experts/POV intact True, grade label True. (Em-dash count reflects only pre-existing ones in untouched sections; the rewritten lines add none.)

- [ ] **Step 6: Spot-check readability in the rendered doc**

Run: `cd "$COURSE" && python -c "
import docx;d=docx.Document('Brainlifts/HS Writing Course Design Brainlift - Stakeholder Edition.docx')
cap=False
for p in d.paragraphs:
    t=p.text.strip()
    if t.startswith('Category 4'): cap=True
    if cap and (t.startswith('Sources (primary):') or t.startswith('Compiled in:')):
        print(t); 
    if t.startswith('Insights on Category 4'): break
"`
Expected: prints Category 4's rewritten primary-source line (Engelmann/DI/K&H/SRSD with the Grade-C label) + the Compiled-in back-pointer to `lesson_contract.py`/`G10_Model_Lesson_Specs.md`.

- [ ] **Step 7: Commit (and remove the backup)**

```bash
cd "c:/Users/noelp/HS Writing"
rm "Alpha HS Writing Course 2026-27/Brainlifts/HS Writing Course Design Brainlift - Stakeholder Edition.BACKUP.docx"
git add "Alpha HS Writing Course 2026-27/Brainlifts/HS Writing Course Design Brainlift - Stakeholder Edition.docx" "Alpha HS Writing Course 2026-27/pipeline/brainlift_sources/rewrite_docx_sources.py"
git commit -m "feat(brainlift): rewrite Knowledge Tree Sources to cite primary sources (docx)"
```

---

### Task 5: Reorient the spreadsheet source-first

**Files:**
- Modify: `$COURSE/BrainLift_Knowledge_Tree_Sources.xlsx`
- Modify: `$COURSE/BrainLift_Knowledge_Tree_Sources.csv`
- Create: `$COURSE/pipeline/brainlift_sources/build_source_first_sheet.py`

**Interfaces:**
- Consumes: the register (Task 3), `source_index.json` + `bpass_claims.json`.
- Produces: the xlsx with a new source-first primary tab + the original artifact-first tab preserved.

- [ ] **Step 1: Write the source-first sheet builder**

Create `build_source_first_sheet.py`. It reads the register's rows (parse the category tables) + the two JSONs, and writes a workbook with two tabs: `Sources (primary-first)` — columns [Primary Source | Type | Grounds | Reachable via | Compiled into (artifacts) | Category] — and `Artifacts (original)` — the prior artifact-first sheet, preserved. Use `openpyxl`.

```python
"""Build the source-first spreadsheet twin of the Primary Source Register.
Tab 1 = primary-first; Tab 2 = the original artifact-first view (preserved)."""
import os, re, csv
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

COURSE = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
REG = os.path.join(COURSE, "BrainLift_Primary_Source_Register.md")
XLSX = os.path.join(COURSE, "BrainLift_Knowledge_Tree_Sources.xlsx")
CSV = os.path.join(COURSE, "BrainLift_Knowledge_Tree_Sources.csv")

def parse_register(md):
    """Yield (category, source, typ, grounds, via, compiled) from the register's category tables."""
    cat = None
    for line in md.splitlines():
        m = re.match(r'^##\s+Category\s+(.+)$', line)
        if m:
            cat = "Category " + m.group(1).strip()
            continue
        if line.startswith("|") and "---" not in line and cat:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) == 5 and cells[1] in ("Authority", "Expert"):
                yield (cat, cells[0], cells[1], cells[2], cells[3], cells[4])

rows = list(parse_register(open(REG, encoding="utf-8").read()))

wb = Workbook()
ws = wb.active; ws.title = "Sources (primary-first)"
hdr = ["Primary Source", "Type", "Grounds (claim / SPOV)", "Reachable via",
       "Compiled into (artifacts)", "Knowledge Tree Category"]
ws.append(hdr)
for c in range(1, len(hdr)+1):
    cell = ws.cell(row=1, column=c); cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor="1F4E78")
for (cat, src, typ, grounds, via, comp) in rows:
    ws.append([src, typ, grounds, via, comp, cat])
widths = [46, 10, 52, 40, 46, 30]
for i, w in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = w
ws.freeze_panes = "A2"

# preserve the original artifact-first sheet as a second tab, if present
if os.path.isfile(XLSX):
    old = load_workbook(XLSX)
    src_ws = old[old.sheetnames[0]]
    ws2 = wb.create_sheet("Artifacts (original)")
    for row in src_ws.iter_rows(values_only=True):
        ws2.append(row)

wb.save(XLSX)

with open(CSV, "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.writer(fh); w.writerow(hdr)
    for (cat, src, typ, grounds, via, comp) in rows:
        w.writerow([src, typ, grounds, via, comp, cat])

print(f"source-first rows: {len(rows)}")
print(f"tabs: {wb.sheetnames}")
```

- [ ] **Step 2: Run it and verify**

Run: `cd "$COURSE" && python pipeline/brainlift_sources/build_source_first_sheet.py`
Expected: `source-first rows:` ≥ 35 and `tabs: ['Sources (primary-first)', 'Artifacts (original)']`.

- [ ] **Step 3: Verify the workbook opens and is source-first**

Run: `cd "$COURSE" && python -c "from openpyxl import load_workbook;wb=load_workbook('BrainLift_Knowledge_Tree_Sources.xlsx');ws=wb['Sources (primary-first)'];print('header',[c.value for c in ws[1]][:2]);print('rows',ws.max_row);print('tabs',wb.sheetnames)"`
Expected: `header ['Primary Source', 'Type']`, rows ≥ 36, both tabs present.

- [ ] **Step 4: Commit**

```bash
cd "c:/Users/noelp/HS Writing"
git add "Alpha HS Writing Course 2026-27/BrainLift_Knowledge_Tree_Sources.xlsx" "Alpha HS Writing Course 2026-27/BrainLift_Knowledge_Tree_Sources.csv" "Alpha HS Writing Course 2026-27/pipeline/brainlift_sources/build_source_first_sheet.py"
git commit -m "feat(brainlift): reorient sources spreadsheet source-first (register twin)"
```

---

### Task 6: Final consistency pass + memory update

**Files:**
- Verify: all deliverables cross-reference correctly.
- Modify: `C:/Users/noelp/.claude/projects/c--Users-noelp-HS-Writing/memory/hs-writing-build-log.md`

- [ ] **Step 1: Cross-reference check — every register source resolves; every category cites primary sources**

Run: `cd "$COURSE" && python -c "
reg=open('BrainLift_Primary_Source_Register.md',encoding='utf-8').read()
import docx;d=docx.Document('Brainlifts/HS Writing Course Design Brainlift - Stakeholder Edition.docx')
docx_txt='\n'.join(p.text for p in d.paragraphs)
print('register categories:', reg.count('## Category'))
print('docx primary-source lines:', docx_txt.count('Sources (primary):'))
print('register referenced in docx:', 'Primary Source Register' in docx_txt)
print('gaps in register:', reg.lower().count('live url not recovered'))
"`
Expected: register categories 7, docx primary-source lines 7, register referenced True, gaps count printed (for the record).

- [ ] **Step 2: Verify the original .md BrainLift is untouched**

Run: `cd "c:/Users/noelp/HS Writing" && git status --short "Writing_Brainlift/" ; git log --oneline -1 -- "Writing_Brainlift/HS Writing Course Design Brainlift - Stakeholder Edition.md" 2>/dev/null | head -1`
Expected: no modification to the original `.md` in this task series (it is outside the course folder and was never written).

- [ ] **Step 3: Update the build-log memory**

Append a dated Decision Log entry to `hs-writing-build-log.md` summarizing: the provenance rewrite (Knowledge Tree now cites primary sources, artifacts demoted to back-pointers), the new Primary Source Register + source-first spreadsheet, the B-pass outcome (claims recovered vs gaps), and that the edit landed on the `.docx` copy with the original `.md` untouched. One paragraph, dates absolute.

- [ ] **Step 4: Commit**

```bash
cd "c:/Users/noelp/HS Writing"
git add "Alpha HS Writing Course 2026-27/docs/superpowers/plans/2026-07-17-brainlift-primary-source-provenance.md"
git -C "c:/Users/noelp/.claude/projects/c--Users-noelp-HS-Writing/memory" add hs-writing-build-log.md 2>/dev/null || true
git commit -m "docs(brainlift): finalize primary-source provenance pass + build-log entry" || true
```

---

## Self-Review

**Spec coverage:** D1 register → Task 3; D2 docx rewrite → Task 4; D3 source-first spreadsheet → Task 5; B-pass → Task 2; harvest prerequisite → Task 1; success-criteria verification + memory → Task 6. All spec sections mapped.

**Design-bet handling:** enforced in Task 3 Step 3 (register row example keeps "Grade-C / design bet") + Task 4 Step 5/6 (verify "design bet" survives in the docx). Covered.

**Edit-target guardrail:** original `.md` untouched — enforced by never referencing it for write + Task 6 Step 2 verification. Covered.

**Placeholder scan:** the one intentional fill-in is `CATEGORY_SOURCES` in Task 4 (must be filled from the register produced in Task 3 — it cannot be pre-written because it depends on Task 3's authored strings); Task 4 Step 4 makes filling it an explicit step, not a silent TODO. All other steps carry complete code/commands.

**Type/name consistency:** `source_index.json` shape ({by_file, all_urls}) consistent across Tasks 1/2/3/5; `bpass_claims.json` fields consistent across Tasks 2/3/5; the register table schema (5 cols: Source|Type|Grounds|Reachable via|Compiled into) is parsed with exactly those columns in Task 5's `parse_register`. Consistent.
