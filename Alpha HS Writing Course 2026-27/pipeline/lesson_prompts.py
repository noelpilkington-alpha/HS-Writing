"""
lesson_prompts.py  -  DETERMINISTIC prompt/instruction builders for lesson FRQ + teach bodies.

WHY: the generator used to GUESS structure by regex-parsing prose bodies (split sentences into lines, detect a
"frame", group "Step N" runs). That is inherently fragile - every new phrasing broke it (merged lines, a stray
double "1.", a leaked trait name). This module removes the guessing: an author declares the STRUCTURE explicitly
(intro, a labeled set-apart block, a checklist of question/answer rows, a closer), and these helpers emit clean,
inline-styled HTML that the generator passes through VERBATIM (via _render_body, which preserves <p>/<ol>/<div>).

What you author is exactly what renders. No parser in the middle. All inline-styled (player-safe), no em dashes.
"""

FONT = "-apple-system,Segoe UI,Roboto,Arial,sans-serif"


def _p(text):
    return f'<p style="margin:0 0 8px;">{text}</p>'


def setapart(label, text, tone="amber"):
    """A visually SET-APART block for a copy-this frame, a weak draft, or an example. tone: amber (do-this) or
    red (weak/avoid). The label is the small heading; text is the quoted material, shown italic and distinct."""
    c = {"amber": ("#fffbeb", "#d97706", "#b45309"), "red": ("#fef2f2", "#dc2626", "#991b1b")}.get(tone,
         ("#f8fafc", "#0d9488", "#0f766e"))
    bg, border, head = c
    return (f'<div style="margin:8px 0;padding:10px 14px;background:{bg};border:1px dashed {border};'
            f'border-radius:8px;">'
            f'<div style="font-size:12px;font-weight:700;color:{head};margin-bottom:4px;">{label}</div>'
            f'<div style="font-size:15px;color:#1f2a44;font-style:italic;">{text}</div></div>')


def checklist(rows, title=""):
    """A numbered checklist rendered as a real <ol>. Each row is either a plain string (one instruction) or a
    (question, answer) tuple rendered as 'question' in bold with the modeled answer beneath. Renders ONCE with a
    single set of numbers (no double numbering)."""
    lis = []
    for r in rows:
        if isinstance(r, (tuple, list)):
            q, a = r
            lis.append(f'<li style="margin:5px 0;"><strong>{q}</strong><br/>'
                       f'<span style="color:#5a5d77;">{a}</span></li>')
        else:
            lis.append(f'<li style="margin:5px 0;">{r}</li>')
    head = (f'<div style="font-size:13px;font-weight:700;color:#0f766e;margin:4px 0 2px;">{title}</div>'
            if title else "")
    return (head + '<ol style="margin:6px 0;padding-left:22px;color:#1f2a44;line-height:1.6;">'
            + "".join(lis) + '</ol>')


def outline_table(rows, title="", tone="amber"):
    """Render a MULTI-PARAGRAPH OUTLINE (or any labeled plan) as a real 2-D <table> GRID, so an essay plan
    shows as an outline the student can see the shape of - NOT as run-on italic prose (the collapsed-frame
    defect Noel flagged on the MPO lessons). Each row is (label, cells) where cells is a string (one wide
    cell) or a list of strings (columns, e.g. Main Idea | Details). The label is the bold left column.

    Timeback-safe (verified 2026-07-16): a styled <table> with INLINE css renders on the platform, and it is
    emitted as its OWN block (never nested in <p>, the #1 table bug) because frq_prompt sequences blocks as
    siblings and gated_reading._rich_segments passes a top-level <table> through verbatim. The student types
    their filled-in outline in the response box beneath the grid (the platform FRQ input is a single text box).
    """
    c = {"amber": ("#fffbeb", "#d97706", "#b45309"), "teal": ("#f0fdfa", "#0d9488", "#0f766e")}.get(tone,
         ("#fffbeb", "#d97706", "#b45309"))
    bg, border, head = c
    trs = []
    for label, cells in rows:
        cell_list = cells if isinstance(cells, (list, tuple)) else [cells]
        tds = "".join(
            f'<td style="border:1px solid #cbd5e1;padding:6px 9px;font-size:14px;color:#1f2a44;'
            f'vertical-align:top;">{cell}</td>' for cell in cell_list)
        trs.append(
            f'<tr><td style="border:1px solid #cbd5e1;padding:6px 9px;background:{bg};font-weight:700;'
            f'font-size:12px;color:{head};white-space:nowrap;vertical-align:top;">{label}</td>{tds}</tr>')
    head_html = (f'<div style="font-size:12px;font-weight:700;color:{head};margin:8px 0 4px;">{title}</div>'
                 if title else "")
    return (head_html + '<table style="border-collapse:collapse;width:100%;margin:6px 0;">'
            + "".join(trs) + '</table>')


def frq_prompt(intro="", setapart_block="", checklist_block="", closer=""):
    """Assemble an FRQ task prompt from explicit, ordered structured pieces. Any piece may be empty. Returns
    inline-styled HTML the generator emits verbatim. NO rubric-trait chrome ('Scored on Thesis/Purpose') - that
    is not student content; the grader knows the trait from the item id.
    - intro:  1-2 sentence lead (plain string -> one <p>, or pre-built HTML)
    - setapart_block: output of setapart(...) (a frame / weak draft / example), or ""
    - checklist_block: output of checklist(...), or ""
    - closer: the final instruction (plain string -> one <p>, or HTML)
    """
    parts = []
    if intro:
        parts.append(intro if intro.lstrip().startswith("<") else _p(intro))
    if setapart_block:
        parts.append(setapart_block)
    if checklist_block:
        parts.append(checklist_block)
    if closer:
        parts.append(closer if closer.lstrip().startswith("<") else _p(closer))
    return "".join(parts)
