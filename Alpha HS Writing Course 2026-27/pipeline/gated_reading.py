"""
gated_reading.py  -  generate a Timeback "Learning Journey" gated-reading lesson.html from a lesson's slot
sequence, matching the live format decoded 2026-07-13 (see memory: gated-reading-format).

WHY: the current per-item QTI push renders our lessons as isolated "Question 1/11" quiz cards. The science
courses use a much better format: a self-contained, ZERO-JS lesson.html on CloudFront, rendered by
content.platform.learnwith.ai/player, that reveals one `tb-segment` at a time with a Continue button, gates on
embedded `tb-qti-config` checkpoints (Read - Check - Unlock), narrates via `tb-narration` audio, and defines
terms via `tb-glossary-term`. Same current platform - just a different lesson FORMAT.

This generator maps our slots -> that format:
  teach_card / stimulus_display / annotated_before_after / (non-scored) -> tb-narration content segment
  discrimination / predict_the_fix / self_score                        -> tb-qti-config CHECKPOINT segment (gate)
  production_frq / diagnosis_frq (scored writing)                      -> a writing segment (own interaction; the
      external grader is NOT a gate here - kept as a produce step; wiring to the player's interaction is TBD)

Output: a lesson.html string (+ a list of checkpoint QTI xml strings to write as items/cpN-*.xml). Narration
audio is OPTIONAL (the player URL carries ttsEnabled=true, so the player can synthesize from text; we emit the
audio-catalog entry only when a .wav url is supplied). HOSTING (S3/CloudFront) is a separate step - this only
builds the artifact so it can be viewed locally and, once a bucket is available, uploaded.

This is dependency-free + self-testing (bottom). It does NOT push anything.
"""
from __future__ import annotations
import os, sys, re, glob, html as _html

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
from g9_push_dryrun import _load, _choice_options, _stim_html, STIM
try:
    from l01_diagrams import DIAGRAMS as _DIAGRAMS   # authored SVG diagrams keyed by (lesson_id, slot)
except Exception:
    _DIAGRAMS = {}
try:
    from incept_diagrams import INCEPT_DIAGRAMS as _INCEPT_DIAGRAMS  # Incept drawio PNGs keyed by (lesson_id, slot)
except Exception:
    _INCEPT_DIAGRAMS = {}

# ---- palette (faithful to the decoded science lesson) ------------------------------------------------------
NODE_COLORS = [  # cycled per content node (bar/bg/ink), matching the science lesson's color-coded nodes
    ("#e7e4ff", "#f6f2ff", "#3b3a88"),   # purple
    ("#ffe6cf", "#fff7ef", "#6b3f1f"),   # brown
    ("#dbe7ff", "#f3f7ff", "#1d3b7a"),   # blue
    ("#bfe7da", "#eefaf6", "#0f6b54"),   # teal
]
CHECK_BAR = "#4b63c6"; CHECK_BG = "#faf9ff"; CHECK_INK = "#3b3a88"
WRITE_BAR = "#d97706"; WRITE_BG = "#fffbeb"; WRITE_INK = "#b45309"


def esc(s: str) -> str:
    return _html.escape(s or "", quote=True)


def _plain(body_html: str) -> str:
    """Strip our stylize HTML wrappers to the RAW prose. Also UNESCAPE HTML entities (source stimuli store
    apostrophes/quotes pre-escaped as &#x27; etc): raw prose must be true unicode, so a later esc() produces
    &#x27; not the double-escaped &amp;#x27; the student would see as literal garbage."""
    t = re.sub(r"<[^>]+>", " ", body_html or "")
    t = _html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def _html_blocks(body_html: str) -> list[str]:
    """Split authored body HTML into plain-text blocks, PRESERVING structural breaks. A heading (<h1-6>) or a
    <p>/<li>/<br> becomes its own block, so e.g. '<h3>The debate...</h3><p>Here is...</p>' -> two blocks (title
    on its own line) instead of one collapsed run. If there is no block markup, returns [] (caller falls back
    to sentence-splitting the plain text). Entities are UNESCAPED to true unicode (see _plain) so a downstream
    esc() does not double-escape."""
    h = body_html or ""
    if not re.search(r"</(h[1-6]|p|li|div)>|<br", h, re.I):
        return []
    # mark block boundaries, then strip remaining tags
    h = re.sub(r"</(h[1-6]|p|li|div)>", "\n\n", h, flags=re.I)
    h = re.sub(r"<br\s*/?>", "\n\n", h, flags=re.I)
    h = re.sub(r"<[^>]+>", "", h)
    return [_html.unescape(b.strip()) for b in re.split(r"\n{2,}", h) if b.strip()]


# key terms to emphasize (bold) in instructional prose - defined/used terms across G9 argument lessons.
_KEY_TERMS = ["arguable claim", "controlling idea", "thesis", "counterargument", "evidence", "reasoning",
              "warrant", "claim", "reason", "FACT", "OPINION", "SIDE", "REASON", "argue", "explain",
              "rotation", "revolution", "orbit", "axis"]
_TERM_RE = re.compile(r"\b(" + "|".join(re.escape(t) for t in sorted(_KEY_TERMS, key=len, reverse=True)) + r")\b")


# issue-frame stimuli open their passage with "Here is the question for your claim: <Q>? <rest of framing>".
# Rendered as one flat run it reads as a wall with the question buried. Split it into a styled structural
# lead-in: a bold label + the italicized question on its own line + a break, then the rest of the framing as a
# normal paragraph. Matches the fix Noel requested. Returns None if the block is not a question lead-in.
_Q_LEADIN = re.compile(r"^\s*Here is the question for your claim:\s*(.+?\?)\s*(.*)$", re.S | re.I)


def _render_source_block(b: str) -> str:
    """Render ONE source block as prompt/card HTML. If it is an issue-frame question lead-in, style the question
    as a bold label + italic question + break; otherwise a plain paragraph. esc() everything (XML-safe)."""
    m = _Q_LEADIN.match(b or "")
    if m:
        question, rest = m.group(1).strip(), m.group(2).strip()
        html_out = ('<div style="font-weight:700;margin:0 0 2px;">Here is the question for your claim:</div>'
                    f'<div style="font-style:italic;margin:0 0 8px;">{esc(question)}</div>')
        if rest:
            html_out += f'<p style="margin:0 0 8px;">{esc(rest)}</p>'
        return html_out
    return f'<p style="margin:0 0 8px;">{esc(b)}</p>'


def _emphasize(text: str) -> str:
    """Escape text, then bold the FIRST occurrence of each key term (so definitions stand out without over-
    bolding every repeat). Operates on escaped text so it never injects unsafe markup."""
    safe = esc(text)
    done = set()
    def repl(m):
        term = m.group(1)
        key = term.lower()
        if key in done:
            return term
        done.add(key)
        return f"<strong>{term}</strong>"
    return _TERM_RE.sub(repl, safe)


# named HTML entities that are NOT valid in XML (the player uses a SAX parser) -> Unicode. Timeback RULE:
# use Unicode, never named HTML entities, in QTI/player HTML. Applies to raw authored panels passed verbatim.
_ENT_FIX = {"&nbsp;": " ", "&mdash;": "—", "&ndash;": "–", "&rarr;": "→",
            "&larr;": "←", "&hellip;": "…", "&times;": "×", "&deg;": "°",
            "&rsquo;": "’", "&lsquo;": "‘", "&ldquo;": "“", "&rdquo;": "”",
            "&trade;": "™", "&copy;": "©", "&bull;": "•"}

def _xml_safe_entities(html: str) -> str:
    for ent, uni in _ENT_FIX.items():
        html = html.replace(ent, uni)
    return html


# glossary tooltip: authors write <dfn class="tb-glossary-term" data-catalog-idref="def-X" title="short def">term</dfn>
# inline in a body. The player's upgradeGlossary() turns each into a tap/hover tooltip, pulling the FULL definition
# from a hidden <div id="def-X" class="tb-glossary-definition"> in the catalog (title = fallback). This lets
# NON-operational terms (e.g. "thesis") sit behind a tooltip instead of cluttering the main reading flow.
_GLOSS_RE = re.compile(
    r'<dfn\b[^>]*class="[^"]*tb-glossary-term[^"]*"[^>]*data-catalog-idref="([^"]+)"[^>]*(?:title="([^"]*)")?[^>]*>(.*?)</dfn>',
    re.I | re.S)

def _harvest_glossary(body_html: str, defs: dict):
    """Scan an authored body for tb-glossary-term <dfn>s. For each, register its FULL definition in `defs`
    keyed by catalog id. The definition text is the dfn's title attribute (authors put the full text there;
    the term stays short inline). Returns nothing; mutates defs. The <dfn> itself stays in the body verbatim."""
    for ref, title, _term in _GLOSS_RE.findall(body_html or ""):
        if ref and ref not in defs:
            defs[ref] = (title or "").strip()


# top-level authored STRUCTURE that must survive the flattener verbatim (the player's sanitizer keeps these +
# their inline styles): callout/panel <div>s AND real lists/tables (<ol>/<ul>/<table>). A bare <ol> in a prose
# run would otherwise be flattened by _html_blocks (</li> -> paragraph break) and lose its list structure.
_RAW_BLOCK_TAGS = ("div", "ol", "ul", "table")
_RAW_OPEN_RE = re.compile(r"<(" + "|".join(_RAW_BLOCK_TAGS) + r")\b", re.I)

def _rich_segments(body_html: str):
    """Split an authored body into ordered segments so trusted STRUCTURE survives the flattener:
      ('raw', html)   -> a top-level <div>/<ol>/<ul>/<table> (authored callout, panel, list, or table), VERBATIM
      ('prose', text) -> loose text between them, flattened + key-term-emphasized like normal narration
    The player's sanitizer keeps inline styles and strips script/iframe/on*/unsafe-url, so these render in both
    tracks. Depth-matching handles nesting (a callout <div> may contain <p>/<span>/<ol>)."""
    h = body_html or ""
    segs, i, n = [], 0, len(h)
    while i < n:
        m = _RAW_OPEN_RE.search(h[i:])
        if not m:
            if h[i:].strip():
                segs.append(("prose", h[i:]))
            break
        start = i + m.start()
        tag = m.group(1).lower()
        if start > i and h[i:start].strip():
            segs.append(("prose", h[i:start]))
        # depth-match this opening tag to its matching close (same tag type, allowing nesting of that tag)
        depth, j = 0, n
        for mm in re.finditer(rf"<{tag}\b|</{tag}>", h[start:], re.I):
            depth += 1 if not mm.group(0).startswith("</") else -1
            if depth == 0:
                j = start + mm.end()
                break
        segs.append(("raw", h[start:j]))
        i = j
    return segs


def _render_body(body_html: str) -> str:
    """Render an authored body to card-inner HTML: prose runs become emphasized <p>s (as before), and trusted
    inline-styled <div> panels pass through verbatim, in authored order. This preserves the visual callouts
    (one-idea box, reminder, decompose panel, before/after) the plain flattener would strip to text."""
    out = []
    for kind, chunk in _rich_segments(body_html):
        if kind == "raw":
            out.append(_xml_safe_entities(chunk))
            continue
        # protect inline <dfn> glossary tooltips from the flatten/escape pass: stash them, flatten+emphasize the
        # prose, then restore the <dfn> verbatim (it is trusted authored markup the player upgrades to a tooltip).
        dfns = {}
        def _stash(m):
            key = f"DFN{len(dfns)}"
            dfns[key] = m.group(0)
            return key
        protected = _GLOSS_RE.sub(_stash, chunk)
        blocks = _html_blocks(protected) or _sentences_to_paras(_plain(protected))
        for b in blocks:
            rendered = _emphasize(b)
            for key, dfn in dfns.items():
                rendered = rendered.replace(esc(key), dfn).replace(key, dfn)
            out.append(f'<p style="margin:0 0 8px;">{rendered}</p>')
    return "".join(out)


def _connector(top: str, bottom: str) -> str:
    return (f'<div aria-hidden="true" style="position:absolute; left:29px; top:{top}; bottom:{bottom}; '
            f'width:3px; border-radius:3px; '
            f'background:linear-gradient(180deg,rgba(43,78,162,.32),rgba(106,91,214,.32));"></div>')


def _node(icon_bg_ink, inner: str, *, first=False, last=False) -> str:
    """A left-rail node (icon + connector) + the content card on the right."""
    bar, bg, ink = icon_bg_ink
    top = "8px" if not first else "46px"
    bottom = "8px" if last else "-24px"
    dot = (f'<div style="position:relative; width:46px; height:46px; border-radius:15px; '
           f'background:linear-gradient(180deg,#fff,{bg}); border:1px solid {bar}; '
           f'box-shadow:0 10px 18px rgba(43,42,85,.10); display:flex; align-items:center; justify-content:center;">'
           f'<div style="width:12px;height:12px;border-radius:50%;background:{ink}"></div></div>')
    return (f'<section class="tb-segment"><div style="display:grid; grid-template-columns:62px 1fr; gap:14px; '
            f'position:relative;"><div style="position:relative;">{_connector(top, bottom)}{dot}</div>'
            f'{inner}</div></section>')


def _content_card(title: str, body_paragraphs: list[str], idref: str, colors, img=None, svg=None,
                  raw_body: str = "") -> str:
    bar, bg, ink = colors
    # raw_body (authored HTML with trusted inline-styled callout/panel divs) renders through _render_body so
    # visual callouts survive; otherwise fall back to the flattened paragraph list (bound-stimulus text).
    if raw_body:
        ps = _render_body(raw_body)
    else:
        # each paragraph is emphasized (key terms bolded) + escaped inside _emphasize; do NOT re-escape here
        ps = "".join(f'<p style="margin:0 0 8px;">{_emphasize(p)}</p>' for p in body_paragraphs)
    imgblock = ""
    if img:
        imgblock = (f'<div style="text-align:center; margin:12px 0 4px;"><img src="{esc(img[0])}" '
                    f'alt="{esc(img[1])}" style="max-width:520px; width:100%; height:auto; border-radius:12px;"/>'
                    f'<div style="margin-top:6px; color:#5a5d77; font-size:13px;">{esc(img[1])}</div></div>')
    # svg=(svg_markup, caption): an authored inline-SVG diagram (Track A of the visual protocol). The SVG is
    # emitted verbatim (it is trusted, verified inline-styled markup); caption sits below in muted slate.
    svgblock = ""
    if svg:
        svg_markup, caption = svg
        svgblock = (f'<div style="text-align:center; margin:12px 0 4px;">{svg_markup}'
                    f'<div style="margin-top:6px; color:#5a5d77; font-size:13px;">{esc(caption)}</div></div>')
    return (f'<div style="border-radius:18px; border:1px solid {bar}; background:#fff; '
            f'box-shadow:0 12px 22px rgba(43,42,85,.08); padding:16px 18px;">'
            f'<div style="font-weight:900; color:{ink}; font-size:16px; margin-bottom:8px;">{esc(title)}</div>'
            f'<div class="tb-narration" data-catalog-idref="{idref}" style="color:#1f2a44; line-height:1.65;">'
            f'{ps}{svgblock}{imgblock}</div></div>')


def _checkpoint_card(idref: str) -> str:
    return (f'<div style="border-radius:18px; border:1px solid #d7d2f7; background:{CHECK_BG}; '
            f'box-shadow:0 12px 22px rgba(43,42,85,.08); padding:16px 18px;">'
            f'<div style="font-weight:900; color:{CHECK_INK}; font-size:16px; margin-bottom:10px;">'
            f'Check your understanding</div>'
            f'<div class="tb-interaction tb-qti-assessment-item" data-catalog-idref="{idref}"></div></div>')


def _writing_card(title: str, prompt_paragraphs: list[str], idref: str) -> str:
    # The extended-text QTI item carries its OWN prompt, so the card is just the title + the mount (idref MUST
    # match the tb-qti-config catalog id, else "QTI item not found in catalog"). No separate narration div, or
    # the prompt would render twice.
    return (f'<div style="border-radius:18px; border:1px solid #f5d9a8; background:{WRITE_BG}; '
            f'box-shadow:0 12px 22px rgba(180,83,9,.08); padding:16px 18px;">'
            f'<div style="font-weight:900; color:{WRITE_INK}; font-size:16px; margin-bottom:8px;">{esc(title)}</div>'
            f'<div class="tb-interaction tb-qti-assessment-item" data-catalog-idref="{idref}"></div></div>')


def _parse_reveal(slot, correct):
    """Extract feedback text from a slot's reveal ("Correct: C. (A) is a FACT... (B) is a bare OPINION...
    Only (C)..."). Returns (correct_text, {letter: wrong_text}). The reveal lives in slot.feedback or the
    'Correct:'/'Reveal:' tail of the body."""
    src = _plain(slot.feedback) if getattr(slot, "feedback", "") else ""
    if not src:
        body = _plain(slot.body)
        m = re.search(r"\b(Correct:|Reveal:)", body, re.I)
        src = body[m.start():].strip() if m else ""
    if not src:
        return "", {}
    # Per-letter explanations. A "(X)" only STARTS an explanation when it is at a clause boundary (string start,
    # or just after '. '/'; '/': '), NOT mid-sentence like "Only (C) takes a side". This stops a later inline
    # "(C)" from truncating the "(B)" explanation. Marker positions = boundary-anchored "(X)".
    MARK = re.compile(r"(?:(?<=^)|(?<=[.;:]\s)|(?<=[.;:]\s\s))\(([A-D])\)\s")
    marks = [(m.group(1), m.start(), m.end()) for m in MARK.finditer(src)]
    per = {}
    for i, (letter, _s, e) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else len(src)
        seg = src[e:end].strip().rstrip(".") + "."
        # if this letter already captured (a stray boundary match), keep the LONGER (fuller) explanation
        if letter not in per or len(seg) > len(per[letter]):
            per[letter] = seg
    # the correct-answer sentence: prefer its "(correct-letter)" explanation, else the lead before the first marker
    lead = (src[:marks[0][1]] if marks else src).replace("Correct:", "").replace("Reveal:", "").strip()
    correct_text = per.get(correct) or lead
    return correct_text, {k: v for k, v in per.items() if k != correct}


def checkpoint_xml(cp_id: str, slot) -> str:
    """A gated-reading checkpoint QTI item (matches the decoded cpN xml): choice interaction, hard-gate retry
    via INTERACTION_VISIBILITY, per-wrong-choice teaching feedback, and a PERSISTENT 'correct' feedback-block
    (item-body level) that stays visible after the interaction hides. Reuses the slot's options + reveal."""
    # PREFER explicit structured choices (reliable per-choice feedback) over parsing options+reveal from prose.
    explicit = list(getattr(slot, "choices", []) or [])
    if explicit:
        opts = [{"identifier": c["id"], "content": c["text"]} for c in explicit]
        correct = next((c["id"] for c in explicit if c.get("correct")), explicit[0]["id"])
        wrong_text = {c["id"]: c.get("why", "") for c in explicit if not c.get("correct")}
        correct_text = next((c.get("why", "") for c in explicit if c.get("correct")), "") or "Correct."
        prompt = _plain(slot.body).split("(A)")[0].strip() if slot.body else (slot.title or "")
    else:
        opts, correct = _choice_options(slot)
        opts = opts or []
        correct = correct or (opts[0]["identifier"] if opts else "A")
        prompt = _plain(slot.body).split("(A)")[0].strip() if slot.body else (slot.title or "")
        correct_text, wrong_text = _parse_reveal(slot, correct)
        if not correct_text:
            correct_text = "Correct."
    choices_xml = []
    wrong_conditions = []
    for o in opts:
        oid = f"opt_{o['identifier']}"
        fb = ""
        if o["identifier"] != correct:
            fbid = f"feedback_{oid}"
            wt = (wrong_text.get(o["identifier"]) or "").strip()
            if not wt:
                wt = "Not quite. Re-read the section above, then try again."
            elif not re.search(r"try again", wt, re.I):
                wt = wt.rstrip() + " Try again."
            fb = (f'<qti-feedback-block identifier="{fbid}" outcome-identifier="FEEDBACK" show-hide="show">'
                  f'<qti-content-body><div class="tb-feedback-incorrect"><p>{esc(wt)}</p></div>'
                  f'</qti-content-body></qti-feedback-block>')
            # a response-condition routing this wrong choice to its feedback id
            wrong_conditions.append(
                f'<qti-response-condition><qti-response-if>'
                f'<qti-match><qti-variable identifier="RESPONSE"/>'
                f'<qti-base-value base-type="identifier">{oid}</qti-base-value></qti-match>'
                f'<qti-set-outcome-value identifier="FEEDBACK">'
                f'<qti-base-value base-type="identifier">{fbid}</qti-base-value></qti-set-outcome-value>'
                f'</qti-response-if></qti-response-condition>')
        choices_xml.append(f'<qti-simple-choice identifier="{oid}"><div>{esc(o["content"])}</div>{fb}'
                           f'</qti-simple-choice>')
    # the persistent CORRECT feedback-block (item-body level, AFTER the show_interaction wrapper) - this is what
    # stays green/visible after answering; keyed to FEEDBACK=correct which response-processing sets on a right answer.
    correct_block = (f'<qti-feedback-block identifier="correct" outcome-identifier="FEEDBACK" show-hide="show">'
                     f'<qti-content-body><div class="tb-feedback-correct"><p>{esc(correct_text)}</p></div>'
                     f'</qti-content-body></qti-feedback-block>')
    # response-processing: correct -> SCORE 1 + completed + hide interaction (unlock the gate); else SCORE 0 +
    # incomplete; then per-wrong-choice feedback routing. (Matches the science cpN pattern; REQUIRED - the
    # player rejects an item with no <qti-response-processing>.)
    response_processing = (
        f'<qti-response-processing>'
        f'<qti-response-condition><qti-response-if>'
        f'<qti-match><qti-variable identifier="RESPONSE"/><qti-correct identifier="RESPONSE"/></qti-match>'
        f'<qti-set-outcome-value identifier="SCORE"><qti-base-value base-type="float">1</qti-base-value></qti-set-outcome-value>'
        f'<qti-set-outcome-value identifier="completionStatus"><qti-base-value base-type="identifier">completed</qti-base-value></qti-set-outcome-value>'
        f'<qti-set-outcome-value identifier="FEEDBACK"><qti-base-value base-type="identifier">correct</qti-base-value></qti-set-outcome-value>'
        f'<qti-set-outcome-value identifier="INTERACTION_VISIBILITY"><qti-base-value base-type="identifier">hidden</qti-base-value></qti-set-outcome-value>'
        f'</qti-response-if><qti-response-else>'
        f'<qti-set-outcome-value identifier="SCORE"><qti-base-value base-type="float">0</qti-base-value></qti-set-outcome-value>'
        f'<qti-set-outcome-value identifier="completionStatus"><qti-base-value base-type="identifier">incomplete</qti-base-value></qti-set-outcome-value>'
        f'</qti-response-else></qti-response-condition>'
        f'{"".join(wrong_conditions)}'
        f'</qti-response-processing>')
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<qti-assessment-item xmlns="http://www.imsglobal.org/xsd/imsqtiasi_v3p0" identifier="{cp_id}" '
            f'title="{esc(slot.title or "Checkpoint")}" adaptive="true" time-dependent="false">'
            f'<qti-response-declaration identifier="RESPONSE" cardinality="single" base-type="identifier">'
            f'<qti-correct-response><qti-value>opt_{correct}</qti-value></qti-correct-response>'
            f'</qti-response-declaration>'
            f'<qti-outcome-declaration identifier="SCORE" cardinality="single" base-type="float">'
            f'<qti-default-value><qti-value>0</qti-value></qti-default-value></qti-outcome-declaration>'
            f'<qti-outcome-declaration identifier="FEEDBACK" cardinality="single" base-type="identifier"/>'
            f'<qti-outcome-declaration identifier="completionStatus" cardinality="single" base-type="identifier">'
            f'<qti-default-value><qti-value>incomplete</qti-value></qti-default-value></qti-outcome-declaration>'
            f'<qti-outcome-declaration identifier="INTERACTION_VISIBILITY" cardinality="single" base-type="identifier">'
            f'<qti-default-value><qti-value>show_interaction</qti-value></qti-default-value></qti-outcome-declaration>'
            f'<qti-item-body>'
            f'<qti-feedback-block identifier="show_interaction" outcome-identifier="INTERACTION_VISIBILITY" show-hide="show">'
            f'<qti-content-body>'
            f'<qti-choice-interaction class="qti-labels-none" response-identifier="RESPONSE" shuffle="true" max-choices="1">'
            f'<qti-prompt>{esc(prompt)}</qti-prompt>{"".join(choices_xml)}</qti-choice-interaction>'
            f'</qti-content-body></qti-feedback-block>'
            f'{correct_block}'
            f'</qti-item-body>'
            f'{response_processing}</qti-assessment-item>')


def _source_reminder(source_text) -> str:
    """A ONE-LINE reminder of the topic/question, for repeat same-source writes (so we don't re-paste the whole
    source block every time). Uses the source's own question sentence if present, else its first clause.
    source_text may be a list of blocks or a string."""
    st = " ".join(source_text) if isinstance(source_text, list) else _plain(source_text)
    q = re.search(r"(should [^?.!]{5,120}\?)", st, re.I)
    if q:
        return q.group(1)[0].upper() + q.group(1)[1:]
    return (st[:110].rsplit(" ", 1)[0] + "...") if len(st) > 110 else st


def _render_task(task_html: str) -> str:
    """Render an FRQ task prompt readably. PREFERRED: the author builds the body with lesson_prompts.frq_prompt
    (explicit structured HTML) -> we detect the block markup and pass it through VERBATIM via _render_body (no
    guessing). FALLBACK (legacy plain-text bodies): best-effort parse - bold key terms per line, group a "Step N"
    run into a numbered list, set apart a quoted frame/weak-draft. Either way, strip rubric-trait chrome."""
    # structured/authored HTML body -> render verbatim (blocks preserved), just strip any trait chrome.
    if re.search(r"</(p|div|ol|ul|li)>", task_html or "", re.I):
        cleaned = re.sub(r"<p[^>]*>\s*Scored on [^<]*</p>", "", task_html, flags=re.I)
        return _render_body(cleaned)
    task = _plain(task_html)
    # strip trailing rubric-trait chrome ("Scored on Thesis/Purpose." / "Scored on Development.")
    task = re.sub(r"\s*Scored on [^.]*\.?\s*$", "", task).strip()
    # pull out a SET-APART block: a copy-this frame (quoted, has blanks) OR a quoted weak-draft/example.
    setapart = setapart_label = None
    fm = re.search(r"['\"]([^'\"]*_{3,}[^'\"]*)['\"]", task)
    if fm:
        setapart = fm.group(1).strip(); setapart_label = "Copy this frame exactly, then fill in the blanks:"
        task = (task[:fm.start()] + task[fm.end():])
    else:
        ex = re.search(r"['\"]([^'\"]{10,})['\"]", task)
        if ex and re.search(r"\b(draft|example)\b", task[:ex.start()], re.I):
            setapart = ex.group(1).strip(); setapart_label = "Weak draft to fix:"
            task = (task[:ex.start()] + task[ex.end():])
    task = re.sub(r"\s{2,}", " ", task).replace(" :", ":").strip()
    # split into sentence lines; group a run of "Step N ..." lines into a numbered list
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", task) if s.strip()]
    out, steps = [], []
    def flush_steps():
        if steps:
            lis = "".join(f'<li style="margin:3px 0;">{_emphasize(re.sub(r"^Step \\d[,:]?\\s*", "", s))}</li>'
                          for s in steps)
            out.append(f'<ol style="margin:6px 0;padding-left:22px;color:#1f2a44;">{lis}</ol>')
            steps.clear()
    for s in sents:
        if re.match(r"Step \d", s):
            steps.append(s)
        else:
            flush_steps()
            out.append(f'<p style="margin:0 0 6px;">{_emphasize(s)}</p>')
    flush_steps()
    body = "".join(out)
    if setapart:
        body += ('<div style="margin:8px 0;padding:10px 14px;background:#fffbeb;border:1px dashed #d97706;'
                 'border-radius:8px;">'
                 f'<div style="font-size:12px;font-weight:700;color:#b45309;margin-bottom:4px;">{esc(setapart_label)}</div>'
                 f'<div style="font-size:15px;color:#1f2a44;font-style:italic;">{esc(setapart)}</div></div>')
    return body


def frq_xml(fr_id: str, slot, source_text="", source_reminder="", boxed_source=False) -> str:
    """A gated-reading WRITING item: extended-text QTI. Carries the prompt; the external grader
    (ExternalApiScore) is attached at push time (like our G9 FRQs). Keeps the student a text box in the journey.

    source_text: the framing source, INLINED as a 'Source' block ONLY on its first use in the lesson (a gated
    student cannot scroll back). source_reminder: a one-line topic reminder for LATER same-source writes, so we
    do not re-paste the whole paragraph every time (the repeated wall of text drove skim/boredom in the eval)."""
    prompt_html = ""
    if source_text:
        # source_text is a LIST of blocks (title + paragraphs); render each on its own line so the source is
        # readable, not one flattened run. First block (the stimulus title) gets a small heading style.
        blocks = source_text if isinstance(source_text, list) else [source_text]
        body_html = ""
        for k, b in enumerate(blocks):
            if k == 0 and len(blocks) > 1:
                body_html += f'<div style="font-weight:700;margin:0 0 4px;">{esc(b)}</div>'
            else:
                body_html += _render_source_block(b)
        if boxed_source:
            # essay/gate writes: cap the source in a scrollable panel so the write box stays near the fold
            # (SPINE_REARCH_renderQA_result.md: a naive full re-inline pushes the box 395-587px below the fold).
            prompt_html += (
                '<div style="font-size:12px;font-weight:700;letter-spacing:.04em;color:#0f766e;'
                'text-transform:uppercase;margin-bottom:4px;">Source (scroll within this box)</div>'
                '<div class="tb-source" style="max-height:230px;overflow:auto;border:1px solid #99f6e4;'
                f'background:#f8fafc;border-radius:8px;padding:10px 14px;margin:0 0 12px;color:#1f2a44;'
                f'line-height:1.6;">{body_html}</div>')
        else:
            prompt_html += (f'<div class="tb-source" style="border-left:4px solid #0d9488;background:#f8fafc;'
                            f'border-radius:8px;padding:10px 14px;margin:0 0 12px;">'
                            f'<div style="font-size:12px;font-weight:700;letter-spacing:.04em;color:#0f766e;'
                            f'text-transform:uppercase;margin-bottom:4px;">Source</div>'
                            f'<div style="color:#1f2a44;line-height:1.6;">{body_html}</div></div>')
    elif source_reminder:
        prompt_html += (f'<div style="color:#0f766e;font-size:13px;font-style:italic;margin:0 0 8px;">'
                        f'Same topic: {esc(source_reminder)}</div>')
    # the task: split into separate lines (one instruction per line). If the author marked a copy-this FRAME
    # with the sentinel [[FRAME: ...]], pull it out into its own set-apart block with an explicit copy directive.
    prompt_html += _render_task(slot.body or (slot.title or "Write your response."))
    rubric = getattr(slot, "rubric_ref", "") or "rc.staar"
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<qti-assessment-item xmlns="http://www.imsglobal.org/xsd/imsqtiasi_v3p0" identifier="{fr_id}" '
            f'title="{esc(slot.title or "Write")}" adaptive="false" time-dependent="false">'
            f'<qti-response-declaration identifier="RESPONSE" cardinality="single" base-type="string"/>'
            f'<qti-outcome-declaration identifier="SCORE" cardinality="single" base-type="float">'
            f'<qti-default-value><qti-value>0</qti-value></qti-default-value></qti-outcome-declaration>'
            f'<qti-outcome-declaration identifier="FEEDBACK" cardinality="single" base-type="identifier"/>'
            f'<qti-outcome-declaration identifier="completionStatus" cardinality="single" base-type="identifier">'
            f'<qti-default-value><qti-value>incomplete</qti-value></qti-default-value></qti-outcome-declaration>'
            f'<qti-item-body>'
            f'<qti-extended-text-interaction response-identifier="RESPONSE">'
            f'<qti-prompt>{prompt_html}</qti-prompt></qti-extended-text-interaction>'
            f'</qti-item-body>'
            # response-processing REQUIRED (player rejects items without it). Free-text has no auto-key, so mark
            # complete on any non-empty response; the real score comes from the external grader at push time.
            f'<qti-response-processing>'
            f'<qti-response-condition><qti-response-if>'
            f'<qti-not><qti-is-null><qti-variable identifier="RESPONSE"/></qti-is-null></qti-not>'
            f'<qti-set-outcome-value identifier="completionStatus">'
            f'<qti-base-value base-type="identifier">completed</qti-base-value></qti-set-outcome-value>'
            f'</qti-response-if></qti-response-condition>'
            f'</qti-response-processing>'
            f'<!-- rubric {esc(rubric)}; external grader attached at push -->'
            f'</qti-assessment-item>')


def _sentences_to_paras(text: str, per=2) -> list[str]:
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[\"'A-Z0-9])", text.strip()) if s.strip()]
    if len(sents) <= per:
        return [text.strip()] if text.strip() else []
    out, buf = [], []
    for s in sents:
        buf.append(s)
        if len(buf) >= per:
            out.append(" ".join(buf)); buf = []
    if buf:
        out[-1] = out[-1] + " " + " ".join(buf) if out else out.append(" ".join(buf))
    return out


def build_lesson_html(L, base_url="") -> tuple[str, list[tuple[str, str]]]:
    """Return (lesson_html, [(item_id, xml)]) for a lesson. Content slots -> narration segments; discrimination/
    predict/self_score -> checkpoint gates; production/diagnosis_frq -> extended-text writing items. base_url =
    the absolute URL where items/*.xml are hosted (the player resolves tb-qti-config hrefs against ITS OWN
    origin, so relative hrefs 404; base_url must be our host, e.g. https://<vercel>.vercel.app)."""
    base_url = (base_url or "").rstrip("/")
    segments = []
    catalog_defs, catalog_audio, catalog_items = [], [], []
    gloss_defs = {}   # catalog id -> full definition text, harvested from authored <dfn> tooltips
    checkpoints = []
    node_i = 0
    cur_source = ""   # nearest-preceding framing source, inlined into FRQ prompts (student can't scroll back)
    cur_source_is_frame = False   # True when cur_source is an issue_frame (orientation, never quoted -> not re-inlined)
    inlined_sources = set()   # source texts already inlined ONCE; repeats get a short reminder, not the full block
                              # (Fable eval: pasting the full source into every same-topic write drove skim/boredom)
    for idx, s in enumerate(L.slots):
        first = (idx == 0)
        last = (idx == len(L.slots) - 1)
        if s.kind in ("teach_card", "stimulus_display", "annotated_before_after"):
            colors = NODE_COLORS[node_i % len(NODE_COLORS)]; node_i += 1
            idref = f"narr-{idx+1}"
            # source text for a stimulus_display comes from its bound stimulus; else the slot body.
            # PREFER structural blocks (heading/paragraph breaks preserved) over a flattened run; only
            # sentence-split when the source has no block markup.
            src_html = _stim_html(STIM[s.ref]) if (s.kind == "stimulus_display" and getattr(s, "ref", "") and STIM.get(s.ref)) else (s.body or "")
            blocks = _html_blocks(src_html)
            if blocks:
                paras = blocks
            else:
                paras = _sentences_to_paras(_plain(src_html))
            if s.kind == "stimulus_display" and getattr(s, "ref", "") and STIM.get(s.ref):
                # remember the framing source for downstream FRQs, PRESERVING block structure (title + each
                # paragraph on its own line) instead of one flattened run. blocks already computed above.
                cur_source = blocks if blocks else _sentences_to_paras(_plain(src_html))
                # is this an ISSUE_FRAME (topic orientation for an argue-from-knowledge claim)? Such frames are
                # shown ONCE as their own card and are NEVER quoted by the following write (the student argues
                # from own view), so re-inlining the whole debate into the write card is pure redundancy (the
                # exact duplication Noel flagged on L01). Real passages (single/synthesis) are still inlined
                # because the write quotes them. Track the family so the FRQ step below can skip re-inlining.
                cur_source_is_frame = (getattr(STIM.get(s.ref), "family", "") == "issue_frame")
            # visual-design-protocol Track A: if an authored SVG diagram exists for this (lesson, slot), embed
            # it in the card (replacing the densest paragraph's cognitive load with a labeled diagram).
            diagram = _DIAGRAMS.get((L.id, idx + 1)) if _DIAGRAMS else None
            # Incept drawio PNG (display-only, bound via img=). SVG wins: a slot never gets both.
            incept_png = _INCEPT_DIAGRAMS.get((L.id, idx + 1)) if _INCEPT_DIAGRAMS else None
            # teach/model cards carry OWN-AUTHORED HTML (callout boxes, decompose + before/after panels) that must
            # survive verbatim -> render via raw_body. stimulus_display text comes from a bound stimulus -> paras.
            raw_body = s.body if (s.kind in ("teach_card", "annotated_before_after") and s.body) else ""
            if raw_body:
                _harvest_glossary(raw_body, gloss_defs)   # register any <dfn> tooltips for the catalog
            card = _content_card(s.title or "", paras, idref, colors, svg=diagram,
                                 img=(None if diagram else incept_png), raw_body=raw_body)
            segments.append(_node(colors, card, first=first, last=last))
        elif s.kind in ("discrimination", "predict_the_fix", "self_score"):
            cp_id = f"cp-{L.id}-s{idx+1}"
            segments.append(_node((CHECK_BAR, CHECK_BG, CHECK_INK), _checkpoint_card(cp_id), first=first, last=last))
            checkpoints.append((cp_id, checkpoint_xml(cp_id, s)))
            # ABSOLUTE href (the player resolves relative hrefs against ITS OWN origin -> 404). base_url points
            # at where we host items/*.xml.
            catalog_items.append(f'<div class="tb-qti-config" id="{cp_id}"><a href="{base_url}/items/{cp_id}.xml" '
                                 f'type="application/xml"></a></div>')
        elif s.kind in ("production_frq", "diagnosis_frq"):
            # a writing task = an extended-text QTI item, mounted + wired in the catalog like a checkpoint.
            fr_id = f"frq-{L.id}-s{idx+1}"
            paras = _sentences_to_paras(_plain(s.body))
            segments.append(_node((WRITE_BAR, WRITE_BG, WRITE_INK),
                                  _writing_card(s.title or "Write", paras, fr_id), first=first, last=last))
            # inline the FULL source only the FIRST time this source appears; later same-source writes get a
            # one-line reminder instead of the whole paragraph (kills the repeated-wall-of-text skim the eval found).
            # cur_source is a LIST of blocks; track dedup by a hashable string key (lists are unhashable).
            src_key = " ".join(cur_source) if isinstance(cur_source, list) else cur_source
            # BOX the source for high-load writes: any write at multi_paragraph/essay unit, OR any gate lesson.
            # Boxed writes ALWAYS re-inline the FULL source in a capped scroller (not the one-line reminder), so
            # the student can see the whole source while composing without the write box dropping below the fold.
            boxed = (getattr(L, "lesson_class", "practice") == "gate"
                     or getattr(s, "unit", "") in ("multi_paragraph", "essay"))
            if cur_source_is_frame:
                # issue_frame orientation: the debate was already shown as its own card and the write argues
                # from the student's own view (it does not quote the frame). Do NOT re-inline the whole debate
                # into the write card (that was the L01 redundancy); a one-line topic reminder is enough.
                src_arg, reminder = "", _source_reminder(cur_source)
            elif cur_source and (boxed or src_key not in inlined_sources):
                src_arg, reminder = cur_source, ""
                inlined_sources.add(src_key)
            elif cur_source:
                src_arg, reminder = "", _source_reminder(cur_source)
            else:
                src_arg, reminder = "", ""
            checkpoints.append((fr_id, frq_xml(fr_id, s, source_text=src_arg, source_reminder=reminder,
                                               boxed_source=boxed)))
            catalog_items.append(f'<div class="tb-qti-config" id="{fr_id}"><a href="{base_url}/items/{fr_id}.xml" '
                                 f'type="application/xml"></a></div>')
    # emit harvested glossary definitions into the catalog (player resolves tb-glossary-term -> these by id)
    for ref, text in gloss_defs.items():
        catalog_defs.append(f'<div id="{ref}" class="tb-glossary-definition"><p>{esc(_xml_safe_entities(text))}</p></div>')
    catalog = (f'<div class="tb-catalog" hidden>{"".join(catalog_defs)}{"".join(catalog_audio)}'
               f'{"".join(catalog_items)}</div>')
    # title BANNER, prepended INSIDE the first content segment (NOT its own tb-segment) so the student lands
    # directly on the first teaching slide, not a near-empty title tile that forces an extra Continue click
    # (Noel review 2026-07-14). No "Learning Journey" banner - the player supplies its own progression chrome.
    header = (f'<div style="border-radius:20px; border:1px solid #dbe7ff; '
              f'background:linear-gradient(135deg,#eef6ff 0%,#f6f2ff 55%,#ffffff 100%); color:#1d3b7a; '
              f'font-weight:900; font-size:24px; text-align:center; padding:18px; margin-bottom:14px;">'
              f'{esc(L.title or L.id)}</div>')
    if segments:
        # place the banner as the first child of the first segment, so it shares that segment's reveal step
        # (the student sees title + first teaching card together, no empty title tile / extra Continue click).
        segments[0] = segments[0].replace('<section class="tb-segment">',
                                          f'<section class="tb-segment">{header}', 1)
    html = (f'<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{esc(L.id)}</title></head>\n<body>\n  <div class="tb-article-container">\n'
            f'{"".join(segments)}\n  </div>\n  {catalog}\n</body></html>')
    return html, checkpoints


# A large inlined source stacked full-height above a write box pushes the box below the fold (render-QA:
# 741-word source fails on all student viewports; the largest LEGITIMATE un-boxed source in the live course is
# 74 words). Above this many words, the source MUST be in a capped scroller (boxed_source -> overflow:auto).
SOURCE_BOX_WORD_MAX = 150


# ---- RENDER-FIDELITY parsers/patterns (Tier A6) ------------------------------------------------------------
# These back the render-fidelity checks in render_qc: parse the RENDERED artifact back and assert integrity, so
# the "mangled options / chopped reveal behind a green PASS badge" class (FABLE5_PIPELINE_EVAL section 2a) and
# the "Cat-N label" class (Test Builder BrainLift) can never ship silently.

# a rendered choice option: <qti-simple-choice identifier="opt_X"><div>TEXT</div>...  (TEXT is escaped plain text,
# no nested <div> - build_lesson_html emits <div>{esc(content)}</div>, so the FIRST </div> closes the option).
_OPT_RENDER_RE = re.compile(r'<qti-simple-choice identifier="(opt_[^"]+)"><div>(.*?)</div>', re.S)
_CORRECT_RESP_RE = re.compile(r"<qti-correct-response>\s*<qti-value>(opt_[^<]+)</qti-value>")
# a CHOICE-label marker that leaked INTO an option's text (the eval's chop tell: prose split at "(A)"/"(B)").
_EMBED_MARKER_RE = re.compile(r"\([A-D]\)")
# a DANGLING-CONTINUATION tail: a full sentence, then a break, then a lone connective the option ends on
# (the eval's slot-4 defect: "...is a bare OPINION with no reason. Only" rendered as an option item). This is
# the PRECISE residue a bad chop leaves; a raw "starts-lowercase / <3-words / no-terminal-punct" rule was
# rejected after calibration (it false-flags ~45% of the course's legitimate lowercase imperative move-options).
_OPT_DANGLE_RE = re.compile(
    r"[.;]\s+(only|then|but|and|or|so|because|also|which|that|yet|however|nor|since|as)\s*$", re.I)
# LLM alt-text descriptor blobs that leaked into student-visible content (Test Builder: figure-descriptor blobs
# an LLM emits when it cannot render an image). Anchored on a leading figure/visual keyword INSIDE the brackets,
# so authored fill-in frames like "[your side on the four-day week]" are NOT flagged (0 FP across 100 lessons).
_PLACEHOLDER_RE = re.compile(
    r"\[\s*(?:bar\s+graph|line\s+graph|pie\s+chart|column\s+chart|stacked\s+bar|scatter\s?plot|"
    r"graph|chart|image|figure|diagram|photo|picture|illustration|screenshot|infographic|plot|map|visual)"
    r"\b[^\]]{0,200}\]", re.I)
# Cat-N disease (Test Builder): generic axis/category labels where real data labels are expected. Detected as a
# SEQUENCE (>=2 siblings in the same family), because the defect is always a run ("Category 1, Category 2, ...")
# and a lone occurrence is usually legitimate ("a Category 3 hurricane"). 0 FP across 100 lessons.
_CATN_RE = re.compile(r"\b(Category|Series|Column|Region|Data\s?set|Slice|Wedge)\s+([A-H]|\d{1,3})\b")


def _flat_text(fragment: str) -> str:
    """Strip tags + unescape entities + collapse whitespace: the true student-visible text of a rendered fragment."""
    t = re.sub(r"<[^>]+>", " ", fragment or "")
    t = _html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def _catn_families(text: str) -> dict:
    """Return {family: {labels}} for any Cat-N family with >=2 sibling generic labels in `text` (the defect tell)."""
    fams: dict = {}
    for m in _CATN_RE.finditer(text):
        fams.setdefault(m.group(1).lower().replace(" ", ""), set()).add(re.sub(r"\s+", " ", m.group(0)))
    return {k: v for k, v in fams.items() if len(v) >= 2}


def render_qc(html: str, checkpoints, lessons=None) -> list:
    """Hard gate on the RENDERED output (lesson.html + item XML). Catches the recurring defect classes that used
    to require manual review, so they can never ship silently. Returns a list of problem strings (empty = clean).
    Checks the STUDENT-VISIBLE prompt text of every FRQ/checkpoint item + the lesson body.

    `lessons` (OPTIONAL, backward-compatible): the source Lesson object(s) this html/checkpoints was built from.
    When supplied, the OPTION-INTEGRITY check also asserts each rendered option count matches the source slot's
    choices[] count. The two live callers pass only (html, checkpoints); the choices[] cross-check is skipped
    there and every artifact-level check still runs."""
    import xml.etree.ElementTree as ET
    problems = []
    # map cp-<lesson>-s<i> -> declared choices[] count, so OPTION-INTEGRITY can assert the rendered option count
    # matches the authored slot's choices[] (only when the caller passes the source lesson(s); default off).
    choice_counts = {}
    if lessons is not None:
        _ls = lessons if isinstance(lessons, (list, tuple)) else [lessons]
        for L in _ls:
            for i, s in enumerate(getattr(L, "slots", []) or []):
                if getattr(s, "choices", None):
                    choice_counts[f"cp-{L.id}-s{i+1}"] = len(s.choices)
    # 1. well-formed body (the player uses a SAX parser). Treat the boolean 'hidden' attr as the known exception.
    mb = re.search(r"<body>(.*)</body>", html, re.S)
    if mb:
        try:
            ET.fromstring("<root>" + mb.group(1).replace(" hidden>", ">") + "</root>")
        except ET.ParseError as e:
            problems.append(f"lesson body not well-formed XML: {str(e)[:80]}")
    # collect all student-visible prompt HTML: item prompts + lesson narration/card bodies
    prompts = []
    for _id, xml in checkpoints:
        mp = re.search(r"<qti-prompt>(.*?)</qti-prompt>", xml, re.S)
        if mp:
            prompts.append((_id, mp.group(1)))
    for i, seg in enumerate(re.findall(r'<div class="tb-narration"[^>]*>(.*?)</div>', html, re.S)):
        prompts.append((f"narration-{i+1}", seg))
    for pid, p in prompts:
        text = re.sub(r"<[^>]+>", " ", p)
        text = re.sub(r"\s+", " ", text).strip()
        # 2. leaked rubric-trait chrome
        if re.search(r"\bthesis\s*/\s*purpose\b|\bscored on\b", text, re.I):
            problems.append(f"{pid}: leaked rubric-trait chrome ('Scored on ...'/'Thesis/Purpose') in student text")
        # 3. double-numbering: a real <ol> whose <li> text ALSO starts with 'N.' or 'Step N'
        for li in re.findall(r"<li[^>]*>(.*?)</li>", p, re.S):
            lit = re.sub(r"<[^>]+>", " ", li).strip()
            if re.match(r"(\d+[\.\):]|Step \d)", lit):
                problems.append(f"{pid}: list item begins with its own number ('{lit[:24]}...') -> double numbering")
                break
        # 4. merged 'label: Step' run (the 'Weak draft: Step 1' defect) in plain text
        if re.search(r"\b(weak draft|example|draft)\s*:\s*step \d", text, re.I):
            problems.append(f"{pid}: a set-apart label ran into a 'Step N' checklist (merged block)")
        # 5. wall of text: a single prompt with >55 words and NO block break (<p>/<li>/<ol>/<br>)
        if len(re.findall(r"[A-Za-z]+", text)) > 55 and not re.search(r"</(p|li|ol|ul)>|<br", p, re.I):
            problems.append(f"{pid}: {len(re.findall(r'[A-Za-z]+', text))}-word prompt with no block breaks (wall of text)")
        # 6. a LARGE inlined source block must be in a capped scroller (overflow:auto), not stacked full-height,
        #    or it pushes the write box below the fold (SPINE_REARCH_renderQA_result.md). Measure the SOURCE
        #    block's words only, so legitimate long paragraph-grain prompts are not false-flagged.
        for srcblock in re.findall(r'class="tb-source"[^>]*>(.*?)</div>', p, re.S):
            words = len(re.findall(r"[A-Za-z]+", re.sub(r"<[^>]+>", " ", srcblock)))
            if words > SOURCE_BOX_WORD_MAX and "overflow:auto" not in srcblock:
                problems.append(f"{pid}: {words}-word inlined source not in a capped scroller "
                                f"(use boxed_source; box pushed below fold)")

    # ==== RENDER-FIDELITY checks (Tier A6): parse the RENDERED artifact back and assert integrity. ====
    # 7. OPTION-INTEGRITY: parse the rendered option list of every choice-interaction item and assert no "fake"
    #    options created by a chopped reveal (the eval's slot-4/slot-6 defect), no empty options, no marker-desync.
    for _id, xml in checkpoints:
        if "<qti-choice-interaction" not in xml:
            continue
        opts = _OPT_RENDER_RE.findall(xml)
        if not opts:
            problems.append(f"{_id}: choice interaction rendered with NO parseable options")
            continue
        opt_ids = {oid for oid, _ in opts}
        for oid, body in opts:
            t = _flat_text(body)
            if not t:
                problems.append(f"{_id}/{oid}: rendered option is EMPTY (prose chopped to nothing)")
                continue
            # a leaked "(A)/(B)" choice-label inside an option's own text = prose was split mid-list into it
            if _EMBED_MARKER_RE.search(t):
                problems.append(f"{_id}/{oid}: rendered option contains a leaked choice marker "
                                f"('{t[:48]}...') -> reveal prose chopped into a fake option")
            # a dangling-continuation tail = a full sentence then a lone connective the option ends on (the eval's
            # '...no reason. Only' chop). Precise residue of a bad chop; calibrated to 0 false positives.
            elif _OPT_DANGLE_RE.search(t):
                problems.append(f"{_id}/{oid}: rendered option ends mid-clause on a dangling connective "
                                f"('...{t[-40:]}') -> reveal prose chopped mid-sentence")
        # the correct-response must point at an option that actually rendered (a chop can drop the keyed option)
        cr = _CORRECT_RESP_RE.search(xml)
        if cr and cr.group(1) not in opt_ids:
            problems.append(f"{_id}: correct-response '{cr.group(1)}' has no matching rendered option "
                            f"(rendered: {sorted(opt_ids)}) -> option list mangled")
        # when the source lesson was supplied, the rendered option count must equal the authored choices[] count
        want = choice_counts.get(_id)
        if want is not None and len(opts) != want:
            problems.append(f"{_id}: rendered {len(opts)} options but the slot declares {want} choices[] "
                            f"-> options added/dropped by the renderer")

    # collect ALL student-visible rendered text for the content-blob checks (item XML + lesson body, catalog
    # excluded - it holds hidden glossary/audio defs, not student-visible chrome). The catalog is always the
    # LAST child of <body>, so split at its opening tag (nested divs make a regex strip unreliable).
    body_html = (mb.group(1) if mb else "").split('<div class="tb-catalog"', 1)[0]
    visible_fragments = [(f"item {_id}", xml) for _id, xml in checkpoints]
    visible_fragments.append(("lesson body", body_html))

    for where, frag in visible_fragments:
        flat = _flat_text(frag)
        # 8. LEAKED-PLACEHOLDER: an LLM figure-descriptor / alt-text blob that leaked into student-visible content.
        for m in _PLACEHOLDER_RE.finditer(flat):
            problems.append(f"{where}: leaked figure-descriptor placeholder in student text "
                            f"('{m.group(0)[:60]}') -> LLM alt-text blob, not real content")
        # 9. CAT-N LABELS: generic axis/category placeholders (>=2 siblings in a family) where real data is expected.
        for fam, labs in _catn_families(flat).items():
            problems.append(f"{where}: generic Cat-N labels {sorted(labs)[:4]} in a stimulus/diagram "
                            f"-> labels must trace to real data, not placeholders")

    return problems


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("lesson", nargs="?", default="Lesson_Bank_G9/lesson_g9_l01_arguable_claim.py")
    ap.add_argument("--out", default=os.path.join(ROOT, "GATED_READING_PROTOTYPE"))
    ap.add_argument("--base-url", default="", help="absolute URL where items/*.xml are hosted (e.g. the Vercel prod URL)")
    args = ap.parse_args()
    m = _load(os.path.join(ROOT, args.lesson) if not os.path.isabs(args.lesson) else args.lesson)
    L = getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0]
    html, checkpoints = build_lesson_html(L, base_url=args.base_url)
    # RENDER-QC (hard gate): the rendered lesson + items must be free of the recurring defect classes, so
    # typography never needs manual review again. Fails loud (exit 2) if any defect is present.
    problems = render_qc(html, checkpoints)
    if problems:
        print(f"RENDER-QC FAILED for {L.id}:", file=sys.stderr)
        for p in problems:
            print("  - " + p, file=sys.stderr)
        sys.exit(2)
    items_dir = os.path.join(args.out, "items")
    os.makedirs(items_dir, exist_ok=True)
    # CLEAN stale item files for THIS lesson id first (slot layout can change between runs -> old cp-*/frq-*
    # files for now-removed/renumbered slots would otherwise linger as orphans). Only remove this lesson's ids.
    for old in glob.glob(os.path.join(items_dir, f"cp-{L.id}-*.xml")) + glob.glob(os.path.join(items_dir, f"frq-{L.id}-*.xml")):
        try:
            os.remove(old)
        except OSError:
            pass
    hp = os.path.join(args.out, "lesson.html")
    with open(hp, "w", encoding="utf-8") as f:
        f.write(html)
    for cp_id, xml in checkpoints:
        with open(os.path.join(items_dir, f"{cp_id}.xml"), "w", encoding="utf-8") as f:
            f.write(xml)
    print(f"gated-reading prototype for {L.id}:")
    print(f"  lesson.html  ({len(html)} bytes, {html.count('tb-segment')} segments, {len(checkpoints)} checkpoints)")
    print(f"  -> {hp}")
    print(f"  open it in a browser to preview the Learning Journey layout (static; the live player adds the")
    print(f"     Continue gating + Read Aloud + checkpoint rendering).")


if __name__ == "__main__":
    main()
