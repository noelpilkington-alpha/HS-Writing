"""
_fix_diag_order.py  -  ONE-TIME transform: move the self-revision diagnosis_frq to AFTER the
INDEPENDENT write in essay-grain lessons (fixes the phantom-draft ordering defect).

DEFECT: the spine re-architecture (084ff7e) reworded the diagnosis to "Reread the essay you just
wrote... run this checklist on YOUR draft", but left the diagnosis_frq slot POSITIONED BEFORE the
INDEPENDENT write. So the student is told to reread an essay they have not written yet. The independent
write already closes with "then run the reread check and fix any part that fails", so the diagnosis
belongs immediately AFTER it.

APPROACH (safe, deterministic): parse each file with ast, locate the slots=[...] list, find the
diagnosis_frq element and the immediately-following INDEPENDENT production_frq element, and swap their
exact source-line blocks (each block extended UP to include a leading '# ====='/comment line, and the
trailing comma line). After the swap: re-parse, reload, and re-run the full contract QC; if anything
fails, REVERT that file and report. Only lessons where diagnosis immediately precedes the independent
write are touched (verified: all 25 are that shape).

Run:  python pipeline/_fix_diag_order.py            # apply + verify
      python pipeline/_fix_diag_order.py --dry-run  # report only
"""
from __future__ import annotations
import ast, os, sys, glob, importlib.util, io, contextlib

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
from mastery_targets_grade import _GRADE_GLOB  # noqa: E402


def _slots_list(tree):
    found = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            for kw in node.keywords:
                if kw.arg == "slots" and isinstance(kw.value, ast.List):
                    found = kw.value
    return found


def _role_kind(call):
    args = [a.value for a in call.args if isinstance(a, ast.Constant)]
    return (args[0] if len(args) > 0 else "", args[1] if len(args) > 1 else "")


def _block_span(elt, lines):
    """1-indexed [start, end] source line span for a slot element, EXTENDING the start UP over any
    immediately-preceding comment lines (the '# ===== INDEPENDENT ...' banner) and the end DOWN to
    include the trailing comma line if the comma sits on its own / at the element's last line."""
    start = elt.lineno
    end = elt.end_lineno
    # absorb a leading comment/banner block directly above (contiguous lines starting with #)
    i = start - 2  # 0-indexed line just above the element's first line
    while i >= 0 and lines[i].strip().startswith("#"):
        start = i + 1
        i -= 1
    # absorb a blank line above the comment block? no - keep blanks as separators, handled by join.
    return start, end


def _extract(lines, span):
    return lines[span[0] - 1: span[1]]


def process_file(path, dry=False):
    src = open(path, encoding="utf-8").read()
    lines = src.splitlines(keepends=True)
    tree = ast.parse(src)
    slots = _slots_list(tree)
    if slots is None:
        return ("skip", "no slots list")
    elts = [e for e in slots.elts if isinstance(e, ast.Call)]
    # find diagnosis_frq immediately followed by INDEPENDENT production_frq
    di = ii = None
    for idx, e in enumerate(elts):
        r, k = _role_kind(e)
        if k == "diagnosis_frq":
            di = idx
        if r == "INDEPENDENT" and k == "production_frq" and ii is None:
            ii = idx
    if di is None or ii is None:
        return ("skip", "no diagnosis or no independent write")
    if ii != di + 1:
        return ("skip", f"not adjacent (diag elt {di}, indep elt {ii})")
    # confirm the diagnosis references an already-written draft (the defect signature)
    diag_src = ast.get_source_segment(src, elts[di]) or ""
    if "you just wrote" not in diag_src.lower() and "reread the essay" not in diag_src.lower():
        return ("skip", "diagnosis does not reference an already-written draft")

    diag_span = _block_span(elts[di], lines)
    indep_span = _block_span(elts[ii], lines)
    # the two blocks must be contiguous (diag block ends right before indep block starts, modulo blanks)
    diag_block = _extract(lines, diag_span)
    indep_block = _extract(lines, indep_span)
    between = lines[diag_span[1]: indep_span[0] - 1]  # blank lines between the two blocks
    if any(s.strip() and not s.strip().startswith("#") for s in between):
        return ("skip", f"non-trivial content between diag and indep blocks: {between!r}")

    # rebuild: [ ...before diag... ] + indep_block + between + diag_block + [ ...after indep... ]
    before = lines[: diag_span[0] - 1]
    after = lines[indep_span[1]:]
    new_lines = before + indep_block + between + diag_block + after
    new_src = "".join(new_lines)

    if dry:
        return ("would-fix", f"diag lines {diag_span} <-> indep lines {indep_span}")

    # write, then VERIFY (re-parse + reload + full contract QC); revert on any failure
    open(path, "w", encoding="utf-8").write(new_src)
    ok, why = _verify(path)
    if not ok:
        open(path, "w", encoding="utf-8").write(src)  # revert
        return ("REVERTED", why)
    return ("fixed", why)


def _verify(path):
    """Reload the file and assert: (1) it parses/imports, (2) diagnosis now comes AFTER the independent
    write, (3) the full contract QC still passes."""
    try:
        spec = importlib.util.spec_from_file_location("verif_" + os.path.basename(path)[:-3], path)
        m = importlib.util.module_from_spec(spec)
        with contextlib.redirect_stdout(io.StringIO()):
            spec.loader.exec_module(m)
    except SystemExit:
        pass
    except Exception as e:
        return False, f"import failed: {e!r}"
    L = getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0]
    if L is None:
        return False, "no LESSON after rewrite"
    slots = L.slots
    di = [i for i, s in enumerate(slots) if getattr(s, "kind", "") == "diagnosis_frq"]
    ii = [i for i, s in enumerate(slots) if getattr(s, "role", "") == "INDEPENDENT" and getattr(s, "kind", "") == "production_frq"]
    if di and ii and di[0] < ii[0]:
        return False, "diagnosis STILL before independent write after rewrite"
    import lesson_contract as LC
    qc = LC.qc_lesson(L)
    if not qc["passed"]:
        return False, f"contract QC failed after rewrite: {qc['first_failure']}"
    return True, "diagnosis now after write; contract QC green"


def main():
    dry = "--dry-run" in sys.argv
    results = {"fixed": [], "REVERTED": [], "skip": [], "would-fix": []}
    for grade, (sub, pat) in _GRADE_GLOB.items():
        for f in sorted(glob.glob(os.path.join(ROOT, sub, pat))):
            if "_deprecated" in f:
                continue
            status, why = process_file(f, dry=dry)
            results.setdefault(status, []).append((os.path.basename(f), why))
    for status in ("fixed", "would-fix", "REVERTED"):
        if results[status]:
            print(f"\n=== {status.upper()} ({len(results[status])}) ===")
            for name, why in results[status]:
                print(f"  {name}: {why}")
    if results["REVERTED"]:
        print("\n!! some files were REVERTED (verify failed) - investigate before proceeding")
        return 1
    print(f"\n{'DRY-RUN: ' if dry else ''}fixed={len(results['fixed'])} would-fix={len(results['would-fix'])} "
          f"reverted={len(results['REVERTED'])} skipped={len(results['skip'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
