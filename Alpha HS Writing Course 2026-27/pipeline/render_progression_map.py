"""Render a progression/catalog Markdown doc to a standalone styled HTML for review.

Dependency-free (no markdown lib). Handles the subset of Markdown these docs use:
headers (#..####), pipe tables, **bold**, `code`, horizontal rules, blank-line
paragraphs, and blockquotes. House style: purple accent, readable tables.
Run: python pipeline/render_progression_map.py [source.md ...]
  (no args -> renders the default map + the item-type catalog)
Writes: <source>.html next to each source.
"""
import html
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DEFAULT_SOURCES = [
    BASE / "Sentence_Progression_G9-12.md",
    BASE / "_evidence" / "writing_item_type_catalog.md",
]

ACCENT = "#6d28d9"       # house purple
ACCENT_SOFT = "#ede9fe"  # muted highlight
INK = "#1f2430"


def inline(text: str) -> str:
    """Escape, then apply inline **bold** and `code`."""
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


def grade_badge(cell: str) -> str:
    """Wrap a bare G9/G10/G11/G12 owning-grade cell in a colored badge."""
    m = re.fullmatch(r"\*\*(G9|G10|G11|G12)\*\*", cell.strip())
    if m:
        g = m.group(1)
        return f'<span class="badge badge-{g.lower()}">{g}</span>'
    return inline(cell)


def render_table(rows):
    header = rows[0]
    body = rows[2:]  # rows[1] is the --- separator
    out = ['<table>', '<thead><tr>']
    for cell in header:
        out.append(f"<th>{inline(cell)}</th>")
    out.append("</tr></thead><tbody>")
    for r in body:
        out.append("<tr>")
        for i, cell in enumerate(r):
            # second column is the "NEW @" grade in both tables -> badge it
            if i == 1:
                out.append(f"<td>{grade_badge(cell)}</td>")
            else:
                out.append(f"<td>{inline(cell)}</td>")
        out.append("</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def split_row(line: str):
    line = line.strip().strip("|")
    return [c.strip() for c in line.split("|")]


def convert(md: str) -> str:
    lines = md.splitlines()
    html_parts = []
    i = 0
    para = []

    def flush_para():
        if para:
            text = " ".join(para).strip()
            if text:
                html_parts.append(f"<p>{inline(text)}</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # table block
        if stripped.startswith("|") and i + 1 < len(lines) and set(lines[i + 1].strip()) <= set("|-: "):
            flush_para()
            table_rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_rows.append(split_row(lines[i]))
                i += 1
            html_parts.append(render_table(table_rows))
            continue

        if not stripped:
            flush_para()
            i += 1
            continue

        if stripped.startswith("#"):
            flush_para()
            level = len(stripped) - len(stripped.lstrip("#"))
            content = stripped[level:].strip()
            html_parts.append(f"<h{level}>{inline(content)}</h{level}>")
            i += 1
            continue

        if stripped.startswith("---"):
            flush_para()
            html_parts.append("<hr/>")
            i += 1
            continue

        if stripped.startswith(">"):
            flush_para()
            html_parts.append(f'<blockquote>{inline(stripped.lstrip("> ").rstrip())}</blockquote>')
            i += 1
            continue

        if re.match(r"^[-*] ", stripped):
            flush_para()
            items = []
            while i < len(lines) and re.match(r"^[-*] ", lines[i].strip()):
                items.append(inline(lines[i].strip()[2:]))
                i += 1
            html_parts.append("<ul>" + "".join(f"<li>{it}</li>" for it in items) + "</ul>")
            continue

        para.append(stripped)
        i += 1

    flush_para()
    return "\n".join(html_parts)


def render_one(src: Path):
    md = src.read_text(encoding="utf-8")
    body = convert(md)
    # title = first H1 in the doc, else the filename
    m = re.search(r"^#\s+(.+)$", md, re.MULTILINE)
    title = html.escape(m.group(1)) if m else src.stem
    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{title}</title>
<style>
  :root {{ --accent: {ACCENT}; --accent-soft: {ACCENT_SOFT}; --ink: {INK}; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
         color: var(--ink); line-height: 1.55; max-width: 1180px; margin: 0 auto;
         padding: 40px 32px 96px; background: #fafafb; }}
  h1 {{ font-size: 30px; border-bottom: 4px solid var(--accent); padding-bottom: 12px; }}
  h2 {{ font-size: 23px; color: var(--accent); margin-top: 40px;
        border-bottom: 1px solid #e5e7eb; padding-bottom: 6px; }}
  h3 {{ font-size: 18px; margin-top: 28px; }}
  code {{ background: #f1f0f6; padding: 1px 6px; border-radius: 4px;
          font-size: 0.9em; color: #4c1d95; }}
  hr {{ border: none; border-top: 1px solid #e5e7eb; margin: 34px 0; }}
  blockquote {{ background: var(--accent-soft); border-left: 4px solid var(--accent);
                margin: 16px 0; padding: 12px 18px; border-radius: 0 8px 8px 0;
                font-size: 0.95em; }}
  table {{ border-collapse: collapse; width: 100%; margin: 18px 0; font-size: 14px;
           background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,.06); border-radius: 8px;
           overflow: hidden; }}
  th {{ background: var(--accent); color: #fff; text-align: left; padding: 10px 12px;
        font-weight: 600; vertical-align: top; }}
  td {{ padding: 10px 12px; border-top: 1px solid #eee; vertical-align: top; }}
  tr:nth-child(even) td {{ background: #fbfbfd; }}
  td:first-child {{ font-weight: 600; width: 18%; }}
  blockquote {{ font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 13px; }}
  .badge {{ display: inline-block; padding: 3px 11px; border-radius: 999px;
            font-weight: 700; font-size: 13px; color: #fff; white-space: nowrap; }}
  .badge-g9  {{ background: #2563eb; }}
  .badge-g10 {{ background: #7c3aed; }}
  .badge-g11 {{ background: #db2777; }}
  .badge-g12 {{ background: #b45309; }}
  strong {{ color: #111; }}
  ul {{ margin: 12px 0; }}
  li {{ margin: 5px 0; }}
  .legend {{ margin: 8px 0 24px; font-size: 13px; color: #555; }}
  .legend .badge {{ margin-right: 6px; }}
</style></head>
<body>
<div class="legend">
  Owning-grade legend:
  <span class="badge badge-g9">G9</span>
  <span class="badge badge-g10">G10</span>
  <span class="badge badge-g11">G11</span>
  <span class="badge badge-g12">G12</span>
  &nbsp;&mdash;&nbsp; each skill is taught to automaticity at its owning grade, then retrieval-gated (not re-taught) at later grades.
</div>
{body}
</body></html>
"""
    out = src.with_suffix(".html")
    out.write_text(doc, encoding="utf-8")
    print(f"wrote {out}")


def main():
    args = sys.argv[1:]
    sources = [Path(a) for a in args] if args else DEFAULT_SOURCES
    for src in sources:
        if not src.is_absolute():
            src = BASE / src
        render_one(src)


if __name__ == "__main__":
    main()
