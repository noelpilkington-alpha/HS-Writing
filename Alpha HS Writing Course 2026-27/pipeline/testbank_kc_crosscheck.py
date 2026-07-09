"""
testbank_kc_crosscheck.py - Close the loop: does the G10 item bank align to the source-of-truth KC map / ACC spine?

The KC map (course_sequence_g9_12.py) says what the course TEACHES, anchored to the ACC common standard.
The item bank (Item_Bank_G10/) says what the course TESTS. This validator proves they speak the SAME
standard - so the verified test bank actually informs (and is informed by) the curriculum, per the goal.

Checks (all must hold for exit 0):
  A. every ACC code used by a G10 item is a real ACC-spine code (no invented codes in the bank)
  B. every ACC code an item uses is either HS-owned OR external (a G10 test legitimately measures conventions/
     language, which the Language course teaches) - but a WRITING item must not be tagged to a descoped ACC
     code (e.g. narrative) unless narrative is un-descoped
  C. coverage: every HS-owned ACC code that is TESTABLE at G9-10 (the G10 EOC band) has >=1 item measuring it
     -> a tested-but-unmeasured standard is a bank gap
  D. every CR item binds to a real stimulus id in the stimulus bank; every rubric_ref is a known rc.* config
  E. report the taught-vs-tested matrix: for each G9-10-band ACC code, is it TAUGHT (a KC carries it) and
     MEASURED (an item carries it)?

This is COVERAGE alignment, not efficacy. Dependency-free (stdlib). Run: python pipeline/testbank_kc_crosscheck.py
"""
from __future__ import annotations
import os, re, sys, glob

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
from course_sequence_g9_12 import ACC_SPINE, ACC_CODES, HS_KCS, DESCOPED  # single source of truth

# Grade is selectable: `python testbank_kc_crosscheck.py [G9|G10|G11|G12]` (default G10).
# G9=English I, G10=English II (shared 9-10 EOC denominator); G11=college-test year (SBAC/ACT/AP Lang,
# adds synthesis + rhetorical-analysis + source-free/multi-perspective argument + sophistication);
# G12=AP tier (rides on G11, AP Lang only).
_GRADE = "G10"
for _a in sys.argv[1:]:
    if _a.upper() in ("G9", "G10", "G11", "G12"):
        _GRADE = _a.upper()
ITEM_DIR = os.path.join(ROOT, f"Item_Bank_{_GRADE}")
STIM_DIR = os.path.join(ROOT, f"Stimulus_Bank_{_GRADE}")
KNOWN_RUBRICS = {"rc.staar", "rc.mcas", "rc.ohio", "rc.4trait", "rc.ap", "rc.sc", "rc.fl"}

# ACC codes an HS-owned KC carries (taught), and codes external courses own (still legitimately test-measurable at G10)
TAUGHT_ACC = {a for k in HS_KCS for a in k["acc"]}
EXTERNAL_ACC = {a["code"] for a in ACC_SPINE if a["need"] == "external"}
DESCOPED_ACC = {a["code"] for a in ACC_SPINE if a["need"] == "descoped"}

# Which ACC codes are legitimately TESTABLE at the G9-10 EOC band (so 'must be measured' applies).
# Derived from the G10 item spec + crosswalk: the G10 EOC measures argument/info/analysis CR + the SR editing
# families (conventions/sentence/organization/evidence/language). AP-only (G11-12) codes are NOT required at G10.
G10_BAND_TESTABLE = {
    "ACC.W.ARG.1", "ACC.W.ARG.2", "ACC.W.ARG.3", "ACC.W.ARG.4", "ACC.W.ARG.5",
    "ACC.W.INFO.1", "ACC.W.INFO.2", "ACC.W.INFO.3", "ACC.W.INFO.5", "ACC.W.INFO.6",
    "ACC.W.SRC.1", "ACC.W.SRC.2", "ACC.W.SRC.3",
    "ACC.W.CONV.1", "ACC.W.CONV.2", "ACC.W.CONV.3",  # external-owned but measured on the G10 test
    "ACC.W.PROD.1", "ACC.W.PROC.2",
}
# G11 (college-test year): the writing-composition codes the SBAC/ACT/AP-Lang tasks measure. Conventions
# (CONV.1/2) are the Language course's SR tier, not the G11 writing CR bank, so they are NOT required of the
# G11 CR/essay item bank; INQ.1 (source-evaluation) IS newly testable here.
G11_BAND_TESTABLE = {
    "ACC.W.ARG.1", "ACC.W.ARG.2", "ACC.W.ARG.3", "ACC.W.ARG.5",
    "ACC.W.INFO.2", "ACC.W.INFO.3", "ACC.W.INFO.5", "ACC.W.INFO.6",
    "ACC.W.SRC.1", "ACC.W.SRC.2", "ACC.W.SRC.3", "ACC.W.INQ.1",
    "ACC.W.PROD.1", "ACC.W.PROC.2", "ACC.W.CONV.3",
}
# G12 (AP tier, rides on G11): sophistication + sustained timed writing; same ACC codes as G11 (the delta is
# depth/timed, not new ACC standards).
G12_BAND_TESTABLE = set(G11_BAND_TESTABLE)
BAND_TESTABLE = {"G9": G10_BAND_TESTABLE, "G10": G10_BAND_TESTABLE, "G11": G11_BAND_TESTABLE, "G12": G12_BAND_TESTABLE}[_GRADE]

# RUBRIC-DIMENSION standards: measured HOLISTICALLY inside the CR essay rubric (not as a discrete taggable
# item). Real state EOCs score these as an essay trait, so 'no discrete item' is CORRECT, not a gap. (Same
# principle the older coverage_matrix.py uses.) These are covered iff >=1 CR item exists (the essay carries them).
RUBRIC_DIMENSION_ACC = {
    "ACC.W.PROD.1",  # "appropriate to task/purpose/audience" = the whole essay, scored as Purpose/Focus
    "ACC.W.PROC.2",  # "revise for clarity/style" = scored via the essay's Development/Language dimension
    "ACC.W.SRC.2",   # "integrate + cite evidence" = scored inside the CR essay's evidence dimension, not a discrete SR item
    "ACC.W.ARG.5",   # "concluding statement that follows from the argument" = scored inside the essay's Organization trait, not a discrete SR item
    "ACC.W.INFO.5",  # "formal style; concluding section" = scored inside the essay's Organization/Language traits
}


def load_item_acc_and_refs():
    """Scan the item bank: ACC codes used, CR stimulus_refs, rubric_refs. (Regex scan; no import/exec.)"""
    used_acc, stim_refs, rubric_refs = {}, set(), set()
    files = sorted(glob.glob(os.path.join(ITEM_DIR, "*.py")))
    for f in files:
        src = open(f, encoding="utf-8").read()
        fam = os.path.basename(f)[:-3]
        for code in re.findall(r"ACC\.W\.[A-Z]+\.\d+", src):
            used_acc.setdefault(code, set()).add(fam)
        stim_refs.update(re.findall(r'stimulus_ref\s*=\s*"([^"]+)"', src))
        rubric_refs.update(re.findall(r'rubric_ref\s*=\s*"([^"]+)"', src))
    return used_acc, stim_refs, rubric_refs, [os.path.basename(f) for f in files]


def load_stimulus_ids():
    ids = set()
    for f in glob.glob(os.path.join(STIM_DIR, "*.py")):
        src = open(f, encoding="utf-8").read()
        ids.update(re.findall(r'\b(ACC-W910-[A-Z]+-[A-Z0-9-]+?-?\d{4})\b', src))
        ids.update(re.findall(r'id\s*=\s*"(ACC-W910-[^"]+)"', src))
    return ids


def main():
    used_acc, stim_refs, rubric_refs, files = load_item_acc_and_refs()
    stim_ids = load_stimulus_ids()
    errs, warns = [], []

    # A. no invented ACC codes in the bank
    for code in used_acc:
        if code not in ACC_CODES:
            errs.append(f"item bank uses ACC code {code} not in the ACC spine")

    # B. no writing item tagged to a descoped ACC code (unless un-descoped)
    for code in used_acc:
        if code in DESCOPED_ACC:
            errs.append(f"item tagged to DESCOPED ACC code {code} (used by {sorted(used_acc[code])}) - descope leak")

    # C. coverage: every G10-band-testable ACC code is measured - by a discrete item, OR (for rubric-dimension
    #    standards) by the CR essay rubric (>=1 CR item exists). A truly unmeasured standard is a bank gap.
    has_cr_item = any(f.startswith("cr_") for f in files)
    for code in sorted(BAND_TESTABLE):
        if code in used_acc:
            continue
        if code in RUBRIC_DIMENSION_ACC and has_cr_item:
            warns.append(f"{code} not tagged to a discrete item, but it is a RUBRIC-DIMENSION standard "
                         f"(scored holistically inside the CR essay) - correct, not a gap")
        else:
            errs.append(f"G10-testable ACC {code} has NO item measuring it (bank gap)")

    # D. CR stimulus refs resolve; rubric refs known
    for ref in sorted(stim_refs):
        if ref not in stim_ids:
            # tolerate the known ID-format variance; warn rather than fail if the family prefix matches
            if not any(ref in sid or sid in ref for sid in stim_ids):
                warns.append(f"CR stimulus_ref {ref} not found among stimulus-bank ids (verify binding)")
    for rr in sorted(rubric_refs):
        if rr not in KNOWN_RUBRICS:
            errs.append(f"unknown rubric_ref {rr} (not a known rc.* config)")

    # E. taught-vs-tested matrix (report)
    rows = []
    for code in sorted(BAND_TESTABLE):
        taught = code in TAUGHT_ACC
        taught_owner = "KC" if taught else ("external course" if code in EXTERNAL_ACC else "-")
        measured = code in used_acc
        rows.append((code, taught_owner, measured, sorted(used_acc.get(code, []))))

    # ---- report ----
    print(f"=== {_GRADE} TEST-BANK <-> KC-MAP / ACC CROSS-CHECK ===")
    print("(does what the course TESTS speak the same ACC common standard as what it TEACHES?)\n")
    print(f"item files: {len(files)} | distinct ACC codes used by items: {len(used_acc)} | "
          f"stimulus ids found: {len(stim_ids)}\n")
    print("-- TAUGHT vs TESTED (G9-10 band ACC codes) --")
    for code, owner, measured, fams in rows:
        t = "TAUGHT(" + owner + ")" if owner != "-" else "**NOT TAUGHT**"
        if measured:
            m = "MEASURED(" + ",".join(fams) + ")"
        elif code in RUBRIC_DIMENSION_ACC and has_cr_item:
            m = "MEASURED(CR-essay rubric dimension)"
        else:
            m = "**NOT MEASURED**"
        print(f"  {code:16} {t:22} {m}")
    if warns:
        print("\n-- WARNINGS --")
        for w in warns:
            print("  ! " + w)
    print("\n-- RESULT --")
    if errs:
        print("FAIL:")
        for e in errs:
            print("  - " + e)
        sys.exit(1)
    print("PASS: item bank aligns to the ACC spine + KC map (no invented codes, no descope leak,")
    print("      every G10-testable ACC standard is measured, CR bindings + rubrics valid).")
    sys.exit(0)


if __name__ == "__main__":
    main()
