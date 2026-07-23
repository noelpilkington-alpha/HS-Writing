"""
player_test/report.py  -  render a run's Findings into a scorecard (JSON already saved by run.py; this makes
a readable markdown summary: per-check pass/warn/fail counts, then every non-pass finding grouped by lesson).
"""
from __future__ import annotations


def summarize(findings: list) -> dict:
    by_sev = {"pass": 0, "warn": 0, "fail": 0, "skipped": 0}
    by_check = {}
    for f in findings:
        sev = f.get("severity", "skipped")
        by_sev[sev] = by_sev.get(sev, 0) + 1
        c = f.get("check", "?")
        by_check.setdefault(c, {"pass": 0, "warn": 0, "fail": 0, "skipped": 0})
        by_check[c][sev] = by_check[c].get(sev, 0) + 1
    return {"by_severity": by_sev, "by_check": by_check}


def markdown(grade: str, findings: list, meta: dict) -> str:
    s = summarize(findings)
    bs = s["by_severity"]
    lines = [f"# Student-Agent Course Eval - {grade} ({meta.get('base_url','')})",
             "",
             f"Lessons evaluated: {meta.get('lessons_run','?')} / {meta.get('lessons_total','?')}"
             + ("  (SAMPLE)" if meta.get("sample") else ""),
             f"Browser: {'available' if meta.get('browser') else 'UNAVAILABLE (expectations + grading only)'}",
             "",
             f"**Totals:** {bs['pass']} pass, {bs['warn']} warn, {bs['fail']} fail, {bs['skipped']} skipped",
             "",
             "## By check",
             "", "| check | pass | warn | fail | skipped |", "|---|---|---|---|---|"]
    for c, d in sorted(s["by_check"].items()):
        lines.append(f"| {c} | {d['pass']} | {d['warn']} | {d['fail']} | {d['skipped']} |")
    # non-pass findings, grouped by lesson
    nonpass = [f for f in findings if f.get("severity") not in ("pass",)]
    lines += ["", f"## Findings needing attention ({len([f for f in nonpass if f['severity']=='fail'])} fail, "
              f"{len([f for f in nonpass if f['severity']=='warn'])} warn, "
              f"{len([f for f in nonpass if f['severity']=='skipped'])} skipped)", ""]
    if not nonpass:
        lines.append("All checks passed. No issues.")
    else:
        cur = None
        for f in sorted(nonpass, key=lambda x: (x.get("lesson_id", ""), x.get("check", ""))):
            if f["lesson_id"] != cur:
                cur = f["lesson_id"]
                lines.append(f"\n### {cur}")
            sh = f"  (screenshot: {f['screenshot']})" if f.get("screenshot") else ""
            note = f" - {f['note']}" if f.get("note") else ""
            lines.append(f"- **{f['severity'].upper()}** `{f['check']}`: expected _{f.get('expected','')}_, "
                         f"observed _{f.get('observed','')}_{note}{sh}")
    return "\n".join(lines)
