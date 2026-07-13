"""
render_test_content.py  -  Full-content view of the G10 model test, SIDE BY SIDE with the real STAAR
English II skill/rubric it models.

WHY: item IDs are not enough to judge whether we translated the tested writing skills accurately. This
renders the ACTUAL content of every item on Form 01 (stems, options, rationales, answer keys, the bound
source passage, the SCR model answer) next to a description, IN OUR OWN WORDS plus the live TEA link, of
what the matching STAAR item/rubric does, and a fidelity note on the translation.

COPYRIGHT: our item content is ours and shown in full. STAAR's actual item/passage/prompt text is NOT
reproduced (own-words-only rule; the anchor doc forbids copying copyrighted item text). The STAAR column
gives (a) the public rubric criteria (public scoring text, quoted briefly from TEA), (b) a structural
description in our words, and (c) the live TEA URL so the reader can read the genuine article directly.

Dependency-free (stdlib + bank_loader + assemble_test). Run: python pipeline/render_test_content.py
"""
from __future__ import annotations
import os, sys, html

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
from bank_loader import load_bank
from assemble_test import assemble_forms

def esc(s): return html.escape(str(s or ""))

# STAAR reference, in our words + public rubric criteria + live links. NOT copyrighted item text.
STAAR_LINKS = {
    "arg_rubric": "https://tea.texas.gov/data-reports/staar/tx-staar-arg-opinion-rubric-g6-e2.pdf",
    "info_rubric": "https://tea.texas.gov/data-reports/staar/tx-staar-informational-rubric-g6-e2.pdf",
    "scoring_guide": "https://tea.texas.gov/data-reports/staar/2025-staar-english-ii-scoring-guide.pdf",
    "released": "https://www.texasassessment.gov/practice-tests.html",
    "blueprint": "https://tea.texas.gov/data-reports/staar/staar-english-ii-blueprint-schematic.pdf",
}

STAAR_REF = {
    "ECR": {
        "what": ("STAAR English II gives ONE Extended Constructed Response: a source-based essay attached to "
                 "a provided reading selection, with the mode (argumentative or informational) fixed by the "
                 "prompt. The prompt pattern is 'read the selection, then write a [mode] essay.'"),
        "rubric": ("Scored on TWO traits by two scorers (x2 = 10 pts total): (1) Development and Organization "
                   "of Ideas 0-3 and (2) Conventions 0-2. Argument top band (point 3) requires a clear, fully "
                   "developed argument with a consistent focus, an effective introduction and conclusion, "
                   "text-based evidence that is clearly explained and DRAWN FROM BOTH TEXTS in a pair, and "
                   "purposeful word choice. For grades 8 through English II, COUNTERARGUMENTS must be "
                   "identified AND refuted. GATING RULE: a response scoring 0 in Development and Organization "
                   "also earns 0 in Conventions."),
        "skills": ["defensible position/controlling idea", "text-based evidence, explained",
                   "evidence from BOTH source texts", "counterargument identified + refuted (G8-EII)",
                   "effective intro + conclusion", "conventions as a light 0-2 band (ideas weighted over mechanics)"],
        "link": "arg_rubric",
        "fidelity": ("Our ECR prompt names the mode explicitly, binds a provided paired source, and asks the "
                     "student to weigh both sources and respond to an objection, matching STAAR's "
                     "counterargument + both-texts requirements. Our rc.staar scoring config implements the "
                     "exact same two traits, scale (0-3 + 0-2, x2 = 10), and the 0-in-Org-forces-0-Conventions "
                     "gating rule verbatim."),
    },
    "SCR": {
        "what": ("STAAR English II includes short constructed responses. The WRITING-domain SCR is a brief, "
                 "generically-scored production task (0-1) targeting a specific writing/editing move (for "
                 "example, revising a flawed sentence while preserving its meaning)."),
        "rubric": "Writing SCR scored 0-1 on a generic rubric (the move is either accomplished or not).",
        "skills": ["short production", "sentence-level revision that preserves meaning"],
        "link": "scoring_guide",
        "fidelity": ("Our SCR is the STAAR every-year 'revise a flawed sentence, keep the meaning' task "
                     "(here a dangling-modifier repair). It is short PRODUCTION scored by the grader, not a "
                     "multiple-choice item, matching the STAAR writing-SCR format."),
    },
    "SR": {
        "what": ("STAAR English II carries a discrete editing/revising set: two REVISING passages + two "
                 "EDITING passages, delivered as a mix of 4-option multiple choice (including 'NO CHANGE'), "
                 "multiselect, inline-choice dropdown, hot-text, text-entry, and match-table items. Revising "
                 "targets organization, development, evidence, and transitions; editing targets sentence "
                 "boundaries, grammar, usage, and mechanics IN CONTEXT (never isolated grammar drill)."),
        "rubric": "Auto-scored (machine key). MC is capped at <=75% of test points (HB 3906), forcing the SCR/ECR mix.",
        "skills": ["conventions in context", "sentence boundaries (fragments/run-ons)",
                   "organization + transitions", "add/delete/select best evidence", "word choice/precision (language)"],
        "link": "released",
        "fidelity": ("Each of our SR items embeds a short in-context draft (never isolated grammar), offers a "
                     "'NO CHANGE' option where apt, and every distractor names a real misconception, matching "
                     "the STAAR editing/revising shell. Our five SR sub-skills map onto STAAR's revising "
                     "(organization, evidence, language) + editing (conventions, sentence) passages."),
    },
}
SECTION_KIND = {"ECR": "ECR", "SCR": "SCR", "EDIT-conv": "SR", "EDIT-sent": "SR",
                "REV-org": "SR", "REV-evid": "SR", "REV-lang": "SR"}


def _item_content(item_index, it_id):
    it = item_index.get(it_id)
    if not it:
        return f"<i>item {esc(it_id)} not found</i>"
    parts = [f'<div class="stem">{esc(it.stem)}</div>']
    if it.options:
        parts.append('<ul class="opts">')
        for o in it.options:
            tag = '<span class="key">correct</span>' if o.correct else '<span class="dis">distractor</span>'
            rat = f'<span class="rat">why: {esc(o.rationale)}</span>' if o.rationale else ""
            parts.append(f'<li><b>{esc(o.id)}</b> {esc(o.text)} {tag}{rat}</li>')
        parts.append("</ul>")
        parts.append(f'<div class="ak">answer key: {esc(", ".join(it.answer_key))}</div>')
    elif it.answer_key:  # text-entry / SCR model answer
        parts.append(f'<div class="model">model answer: {esc(it.answer_key[0])}</div>')
    if getattr(it, "rubric_ref", ""):
        parts.append(f'<div class="rub">scored by: {esc(it.rubric_ref)}</div>')
    return "".join(parts)


def render():
    ir = load_bank(run_qc=False)
    item_index = {it.id: it for it in ir.items}
    stim_index = {s.id: s for s in (ir.stimuli + ir.singles)}
    forms, _cap = assemble_forms(ir, 1)
    form = forms[0]

    blocks = []
    for sec in form["sections"]:
        kind = SECTION_KIND[sec["section"]]
        ref = STAAR_REF[kind]
        # our column: full content of every item in the section
        ours = []
        for it in sec["items"]:
            src_html = ""
            if it.get("stimulus"):
                st = stim_index.get(it["stimulus"])
                if st:
                    passages = "".join(
                        f'<div class="ptitle">{esc(p.title)}</div><div class="ptext">{esc(p.text)}</div>'
                        for p in st.passages)
                    src_html = (f'<details class="src"><summary>Bound source: {esc(it["stimulus"])} '
                                f'({len(st.passages)} passage[s])</summary>{passages}</details>')
            ours.append(f'<div class="item"><div class="iid">{esc(it["id"])}</div>'
                        f'{_item_content(item_index, it["id"])}{src_html}</div>')
        # STAAR column: our-words description + public rubric + skills + link + fidelity
        skills = "".join(f"<li>{esc(s)}</li>" for s in ref["skills"])
        staar = (f'<div class="what">{esc(ref["what"])}</div>'
                 f'<div class="rlabel">How STAAR scores it</div><div class="rtext">{esc(ref["rubric"])}</div>'
                 f'<div class="rlabel">Skills it targets</div><ul class="skills">{skills}</ul>'
                 f'<a class="tea" href="{esc(STAAR_LINKS[ref["link"]])}" target="_blank">Read the real STAAR source at TEA &rarr;</a>')
        fidelity = f'<div class="fid"><b>Translation fidelity:</b> {esc(ref["fidelity"])}</div>'
        blocks.append(
            f'<section class="sec"><h2>{esc(sec["label"])}</h2>'
            f'<div class="cols"><div class="col ours"><div class="ch">OUR ITEM(S) &mdash; full content</div>{"".join(ours)}</div>'
            f'<div class="col staar"><div class="ch">REAL STAAR ENGLISH II &mdash; what it does (our words + TEA link)</div>{staar}</div></div>'
            f'{fidelity}</section>')

    doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0"><title>G10 Model Test Content vs Real STAAR English II</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:#1e293b;line-height:1.55;max-width:1200px;margin:0 auto;padding:28px 22px 80px}}
h1{{font-size:1.55rem;margin:0 0 4px}}.sub{{color:#64748b;font-size:.95rem}}
.note{{background:#fffbeb;border-left:4px solid #d97706;padding:12px 16px;border-radius:0 8px 8px 0;margin:16px 0;font-size:.88rem}}.note b{{color:#92400e}}
.sec{{border:1px solid #e2e8f0;border-radius:12px;margin:20px 0;overflow:hidden}}
.sec h2{{font-size:1.05rem;margin:0;padding:12px 18px;background:#f8fafc;border-bottom:1px solid #e2e8f0}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:0}}@media(max-width:860px){{.cols{{grid-template-columns:1fr}}}}
.col{{padding:14px 18px}}.col.ours{{border-right:1px solid #e2e8f0;background:#fff}}.col.staar{{background:#f6f8fc}}
.ch{{font-size:.68rem;font-weight:800;letter-spacing:.04em;text-transform:uppercase;color:#64748b;margin-bottom:10px}}
.item{{border:1px solid #eef2f7;border-radius:8px;padding:10px 12px;margin-bottom:10px}}
.iid{{font-family:ui-monospace,Menlo,monospace;font-size:.68rem;color:#4338ca;background:#eef2ff;display:inline-block;padding:1px 6px;border-radius:4px;margin-bottom:6px}}
.stem{{font-size:.9rem;white-space:pre-wrap}}
.opts{{list-style:none;padding:0;margin:8px 0 4px}}.opts li{{font-size:.84rem;margin:4px 0;padding:5px 8px;border-radius:6px;background:#fafafa}}
.key{{color:#166534;font-size:.66rem;font-weight:700;background:#dcfce7;padding:1px 6px;border-radius:10px;margin-left:6px}}
.dis{{color:#64748b;font-size:.66rem;background:#f1f5f9;padding:1px 6px;border-radius:10px;margin-left:6px}}
.rat{{display:block;color:#64748b;font-size:.74rem;font-style:italic;margin-top:2px}}
.ak,.rub,.model{{font-size:.74rem;color:#475569;margin-top:6px;font-family:ui-monospace,Menlo,monospace}}
.model{{background:#f0fdf4;border-left:3px solid #86efac;padding:6px 10px;white-space:pre-wrap;font-family:inherit;font-size:.84rem}}
details.src{{margin-top:8px;border:1px solid #bae6fd;border-radius:8px;background:#f0f9ff;padding:4px 10px}}
details.src summary{{cursor:pointer;font-size:.76rem;font-weight:700;color:#0369a1;padding:4px 0}}
.ptitle{{font-weight:700;color:#075985;font-size:.8rem;margin:8px 0 2px}}.ptext{{white-space:pre-wrap;font-size:.82rem;background:#fff;border-left:3px solid #7dd3fc;padding:8px 12px;border-radius:0 6px 6px 0}}
.what{{font-size:.88rem}}.rlabel{{font-size:.68rem;font-weight:800;text-transform:uppercase;color:#64748b;margin:10px 0 3px}}
.rtext{{font-size:.84rem}}.skills{{margin:2px 0;padding-left:20px}}.skills li{{font-size:.82rem}}
.tea{{display:inline-block;margin-top:10px;font-size:.82rem;color:#2563eb;font-weight:600}}
.fid{{padding:11px 18px;background:#eef2ff;border-top:1px solid #e2e8f0;font-size:.85rem}}.fid b{{color:#4338ca}}
</style></head><body>
<h1>Grade 10 Model Test: Our Content vs Real STAAR English II</h1>
<p class="sub">Form {esc(form["form_id"])}, every item's full content, beside what the matching STAAR English II item and rubric actually do.</p>
<div class="note"><b>Copyright note.</b> Our item content (left) is original and shown in full. STAAR's actual
passages, prompts, and item text are NOT reproduced (own-words-only rule). The right column describes what
STAAR does in our own words, quotes only its public rubric criteria, and links to the genuine released
materials at TEA so you can read the real thing directly and judge the translation yourself.</div>
{"".join(blocks)}
<p class="sub" style="margin-top:24px">Left column read live from the item bank (cannot drift from what was built). Right column grounded in AnchorSets/G10_anchor_forms.md and the TEA rubric PDFs (fetched this session). To read a full real released STAAR English II form: <a href="{esc(STAAR_LINKS['scoring_guide'])}" target="_blank">2025 scoring guide (TEA)</a> and <a href="{esc(STAAR_LINKS['released'])}" target="_blank">released items portal</a>.</p>
</body></html>"""
    out = os.path.join(ROOT, "model_test_content_vs_staar.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(doc)
    return out, form


if __name__ == "__main__":
    out, form = render()
    n_items = sum(len(s["items"]) for s in form["sections"])
    print(f"wrote {os.path.relpath(out, HERE)}  ({n_items} items on {form['form_id']}, full content vs STAAR)")
