"""Apply the frq_type backfill to live lesson files from the subagent classifications.

Reads _frq_classified_G9/G10/G11/G12.json (one record per scored sentence/paragraph production_frq slot:
file, slot_index_in_file, title, unit, frq_type, ...). The subagents parsed via Python AST, so
`slot_index_in_file` is the exact 0-based index among ALL Slot(...) calls in the file. We locate the Nth
Slot(...) the SAME way (AST) and insert `frq_type="<value>"` into that call's keyword list.

Why index-based (not title-match): titles repeat within a file ("... on your own" / "... on a NEW topic"),
so matching by title is ambiguous. The AST index is exact.

SAFETY:
- Re-derives each Slot's location via AST and cross-checks the record's title + unit against what's actually
  at that index. Mismatch -> REPORT + skip (never write on a mismatch).
- Idempotent: skips a slot that already has frq_type=.
- --dry (default) prints the plan; --apply writes, with a .bak per touched file.

Run:  python pipeline/_apply_frq_type_backfill.py            # dry report
      python pipeline/_apply_frq_type_backfill.py --apply    # write
"""
from __future__ import annotations
import ast, glob, json, os, sys

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")


def load_classifications():
    recs = []
    for g in ("G9", "G10", "G11", "G12"):
        p = os.path.join(ROOT, f"_frq_classified_{g}.json")
        if os.path.isfile(p):
            recs += json.load(open(p, encoding="utf-8"))
        else:
            print(f"  [warn] missing {os.path.basename(p)} — that grade not applied")
    return recs


def find_file(fname):
    for sub in ("Lesson_Bank_G9", "Lesson_Bank_G10", "Lesson_Bank_G11", "Lesson_Bank_G12"):
        p = os.path.join(ROOT, sub, fname)
        if os.path.isfile(p):
            return p
    return None


def slot_calls_in_order(tree):
    """All ast.Call nodes for Slot(...) in source order."""
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
             and ((isinstance(n.func, ast.Name) and n.func.id == "Slot"))]
    calls.sort(key=lambda n: (n.lineno, n.col_offset))
    return calls


def _kw(call, name):
    for k in call.keywords:
        if k.arg == name:
            return k
    return None


def _str_arg(call, pos):
    if len(call.args) > pos and isinstance(call.args[pos], ast.Constant):
        return call.args[pos].value
    return None


def apply(dry=True):
    recs = load_classifications()
    if not recs:
        print("no classifications found; run the classifier agents first."); return 1
    by_file = {}
    for r in recs:
        by_file.setdefault(r["file"], []).append(r)

    total = inserted = skipped_present = problems = 0
    # collect (path, list of (byte_or_char insertion) ) — we insert by re-serialising via text offsets
    for fname, slots in sorted(by_file.items()):
        path = find_file(fname)
        if not path:
            print(f"  [MISS] file not found: {fname} ({len(slots)} slots)"); problems += len(slots); continue
        src = open(path, encoding="utf-8").read()
        try:
            tree = ast.parse(src)
        except SyntaxError as e:
            print(f"  [PARSE FAIL] {fname}: {e}"); problems += len(slots); continue
        calls = slot_calls_in_order(tree)
        lines = src.splitlines(keepends=True)
        # compute insertions as (lineno, col, text) then apply back-to-front to keep offsets valid
        edits = []
        for r in slots:
            total += 1
            idx, title, unit, ftype = r["slot_index_in_file"], r["title"], r["unit"], r["frq_type"]
            if ftype not in ("revision", "writing"):
                print(f"  [BAD ftype] {fname} idx{idx}: {ftype!r}"); problems += 1; continue
            if idx >= len(calls):
                print(f"  [IDX OOR] {fname}: idx {idx} >= {len(calls)} Slot calls"); problems += 1; continue
            call = calls[idx]
            # cross-check: this Slot's 3rd positional arg (title) and unit kw match the record
            got_title = _str_arg(call, 2)
            unit_kw = _kw(call, "unit")
            got_unit = unit_kw.value.value if (unit_kw and isinstance(unit_kw.value, ast.Constant)) else None
            if got_title != title or got_unit != unit:
                print(f"  [MISMATCH] {fname} idx{idx}: record=({title[:30]!r},{unit}) "
                      f"but AST=({(got_title or '')[:30]!r},{got_unit}) — skip"); problems += 1; continue
            if _kw(call, "frq_type") is not None:
                skipped_present += 1; continue
            # insert after the `unit=` keyword node's end (end_lineno/end_col_offset available in py3.8+)
            uk = unit_kw
            edits.append((uk.value.end_lineno, uk.value.end_col_offset, f', frq_type="{ftype}"'))
            inserted += 1
        # apply edits back-to-front
        if edits and not dry:
            for (ln, col, text) in sorted(edits, reverse=True):
                line = lines[ln - 1]
                lines[ln - 1] = line[:col] + text + line[col:]
            open(path + ".bak", "w", encoding="utf-8").write(src)
            open(path, "w", encoding="utf-8").write("".join(lines))

    print(f"\n{'DRY ' if dry else ''}backfill: {total} classified | insert={inserted} | "
          f"already-present={skipped_present} | problems={problems}")
    if problems:
        print("!! resolve problems (miss/oor/mismatch/bad-ftype are NOT written)")
    return 0 if problems == 0 else 2


if __name__ == "__main__":
    sys.exit(apply(dry="--apply" not in sys.argv))
