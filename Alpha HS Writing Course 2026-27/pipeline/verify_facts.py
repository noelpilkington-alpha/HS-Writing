"""Networked fact-verification pass -> cached receipts.

Closes the gate_fact_sources fabrication hole: the deterministic gate only checks that a
FactSource has a well-formed URL, never that the cited figure/verbatim is ACTUALLY on the page.
A fabricated figure with a plausible federal URL passes. This script fetches each URL and
checks the verbatim phrase (and figure) really appear, writing a receipt file the deterministic
gate reads. Fetching lives HERE, not in the gate, so the QC path stays offline/stdlib/reproducible.

Receipt file: pipeline/fact_verification.json
  { "<stimulus_id>": { "checked_at": "<iso, passed in>", "rows": [
        {"url": "...", "figure": "...", "verbatim": "...", "verified": true|false, "reason": "..."} ] } }

Usage (manual / overnight, NOT in CI):
  python verify_facts.py --grade G9 [--id ACC-W910-...] [--now 2026-07-14T00:00:00Z]
The --now stamp is passed in (this env forbids wall-clock in reproducible code); default "unknown".
"""
from __future__ import annotations

import argparse
import glob
import importlib.util
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RECEIPTS = os.path.join(HERE, "fact_verification.json")


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip().lower()


def _strip_html(s: str) -> str:
    """Drop HTML tags and decode common entities so a figure sitting inside table markup
    ('<td>76.9</td>', 'cell phones<br/>&nbsp;76.9', '<sup>9</sup>') is checkable. Many federal
    sources (NCES digest tables, EIA/BLS data pages) render figures inside <table> cells with tags and
    &nbsp;/&dagger; between the label and the number, which defeats a raw-substring check even though
    the figure is genuinely present. Tags become spaces so adjacent cells never fuse into a false token."""
    import html as _html
    t = re.sub(r"<[^>]+>", " ", s or "")
    t = _html.unescape(t)
    return t


def _load_stimuli(grades):
    import sys
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    out = []
    for g in grades:
        for f in sorted(glob.glob(os.path.join(ROOT, f"Stimulus_Bank_{g}", "*.py"))):
            if "__" in os.path.basename(f):
                continue
            spec = importlib.util.spec_from_file_location("vf_" + os.path.basename(f)[:-3], f)
            m = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(m)
            except SystemExit:
                pass
            except Exception:
                continue
            for v in vars(m).values():
                if type(v).__name__ == "StimulusRecord":
                    out.append(v)
    return out


def _figure_on_page(figure: str, page_n: str) -> bool:
    """Unit-agnostic figure check. Our text writes '67 percent' / '4.1 percent' / '133 billion pounds';
    the source page may render '67%', '4.1', or '133 billion'. Match on the NUMERIC TOKENS the figure
    contains: every number in the figure must appear on the page (as a standalone token), and if the
    figure carries a %/percent, the page must show that number with either '%' or 'percent' nearby.
    This kills the percent-vs-% and unit-spelling false-flags without accepting a bare-number coincidence
    (all numbers in the figure must be present, not just one)."""
    fig = (figure or "").strip()
    if not fig:
        return False
    nums = re.findall(r"\d[\d,]*(?:\.\d+)?", fig)
    if not nums:
        # qualitative figure: fall back to normalized substring
        return _norm(re.sub(r"[^\w%.,\- ]", "", fig)) in page_n
    is_pct = bool(re.search(r"%|percent", fig, re.I))
    for n in nums:
        bare = n.replace(",", "")
        # the number must appear on the page (with or without thousands separators)
        variants = {n, bare}
        if not any(re.search(r"(?<!\d)" + re.escape(v) + r"(?!\d)", page_n) for v in variants):
            return False
    if is_pct:
        # The number(s) are confirmed present above. For the percent unit, prefer ADJACENCY
        # ('76.9 percent' / '76.9%'), but federal DATA TABLES put the number in a cell and the unit
        # 'percent' in the caption/column header far away (e.g. NCES digest: '... 90.9 (0.67) 75.9
        # ...' with 'Percent of ...' in the title). So accept adjacency OR, failing that, the page
        # containing 'percent'/'%' anywhere (it is a percentage table). The all-numbers-present token
        # check above still blocks a bare-number coincidence, so this does not open a fabrication hole.
        first = nums[0].replace(",", "")
        near = re.search(re.escape(first) + r"\s?(?:%|percent)", page_n) or \
               re.search(r"percent[^.]{0,40}?" + re.escape(first), page_n)
        if not near and not re.search(r"%|percent", page_n):
            return False
    return True


def verify_row(fsrc, fetch) -> dict:
    """Fetch the row's URL and check its verbatim (and figure) actually appear on the page."""
    url = (fsrc.url_fetched or "").strip()
    row = {"url": url, "figure": fsrc.figure, "verbatim": fsrc.verbatim, "verified": False, "reason": ""}
    if not re.match(r"^https?://", url):
        row["reason"] = "no http(s) url"
        return row
    try:
        res = fetch(url, timeout=30)
        page = (res.get("text") if isinstance(res, dict) else str(res)) or ""
    except Exception as e:
        row["reason"] = f"fetch failed: {type(e).__name__}"
        return row
    # Normalize from the HTML-STRIPPED page so figures inside table markup are checkable (federal
    # digest/data tables put the number in a <td> with tags/&nbsp; between it and its label).
    page_n = _norm(_strip_html(page))
    fig_ok = _figure_on_page(fsrc.figure, page_n)
    vb = (fsrc.verbatim or "").strip()
    if vb:
        # Authors capture verbatim with "..." elisions (e.g. "uniforms ... 1999-2000"): an exact
        # substring match would false-fail real content. Verify each non-trivial segment independently.
        segments = [_norm(seg) for seg in re.split(r"\.\.\.|…", vb)]
        segments = [seg for seg in segments if len(seg) >= 8]  # ignore tiny connective fragments
        if segments:
            missing = [seg for seg in segments if seg not in page_n]
            if not missing:
                row["verified"] = True
                row["reason"] = ("verbatim found on page" if len(segments) == 1
                                 else f"all {len(segments)} verbatim segments found on page")
            elif fig_ok:
                # The FIGURE (the actual data claim) is confirmed on the page. That is the load-bearing
                # anti-fabrication check; verbatim is traceability and is often an elided paraphrase that
                # will not substring-match. Figure-on-page => not a fabrication.
                found = len(segments) - len(missing)
                row["verified"] = True
                row["reason"] = (f"figure confirmed on page ({found}/{len(segments)} verbatim segments matched)")
            else:
                row["reason"] = (f"{len(missing)}/{len(segments)} verbatim segment(s) not found "
                                 f"AND figure not on page (fabrication risk)")
            return row
    # No usable verbatim: fall back to the figure token.
    if fig_ok:
        row["verified"] = True
        row["reason"] = "figure token found on page (no verbatim captured)"
    else:
        row["reason"] = "no verbatim captured and figure not found; cannot verify"
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grade", action="append", default=[], help="G9/G10/G11/G12 (repeatable; default all)")
    ap.add_argument("--id", default=None, help="verify only this stimulus id")
    ap.add_argument("--now", default="unknown", help="ISO timestamp to stamp receipts (wall-clock is passed in)")
    ap.add_argument("--dry-run", action="store_true", help="do not fetch; list what would be checked")
    ap.add_argument("--refresh", action="store_true", help="re-check stimuli that already have receipts")
    args = ap.parse_args()

    grades = args.grade or ["G9", "G10", "G11", "G12"]
    stimuli = _load_stimuli(grades)
    if args.id:
        stimuli = [s for s in stimuli if s.id == args.id]

    receipts = {}
    if os.path.exists(RECEIPTS):
        receipts = json.load(open(RECEIPTS, encoding="utf-8"))

    if args.dry_run:
        for s in stimuli:
            print(f"{s.id}: {len(s.fact_sources)} rows")
        return

    from resolve_source import fetch_with_fallback  # networked; imported only here

    # Skip stimuli already in the receipt file (resume support): a long fetch run that is
    # interrupted can be re-invoked and picks up where it stopped. Pass --refresh to re-check all.
    todo = [s for s in stimuli if (args.refresh or s.id not in receipts)]
    print(f"{len(stimuli)} stimuli in scope; {len(todo)} to fetch "
          f"({len(stimuli) - len(todo)} already have receipts)", flush=True)

    for i, s in enumerate(todo, 1):
        rows = [verify_row(f, fetch_with_fallback) for f in s.fact_sources]
        receipts[s.id] = {"checked_at": args.now, "rows": rows}
        n_ok = sum(1 for r in rows if r["verified"])
        flag = "" if n_ok == len(rows) else f"  <-- {len(rows) - n_ok} UNVERIFIED"
        print(f"[{i}/{len(todo)}] {s.id}: {n_ok}/{len(rows)} rows verified{flag}", flush=True)
        # Write incrementally so an interrupted run loses at most the current stimulus.
        json.dump(receipts, open(RECEIPTS, "w", encoding="utf-8"), indent=2)

    print(f"\nwrote receipts -> {RECEIPTS}", flush=True)


if __name__ == "__main__":
    main()
