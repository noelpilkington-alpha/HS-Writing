"""
mastery_targets_grade.py  -  grade-aware mastery targets + rendered PP100 prompt, for the readiness audit.

Generalizes g9_push_mastery_v3_1's G9-only mastery_targets()/_mastery_prompt() to any grade (G9-G12) WITHOUT
touching the working G9 pusher. For a grade it: globs that grade's lesson bank, finds each lesson's INDEPENDENT
production FRQ (the graded composition outcome), pulls the AUTHORED task-specific held-out prompt from
mastery_prompts_g{N}.MASTERY[id] (source + prompt_html), inlines the held-out source, and renders the prompt HTML
with the same gated-reading engine the in-article writes use. Used by course_readiness_audit.py so the audit sees
EXACTLY the PP100 task a student is graded on.
"""
from __future__ import annotations
import os, sys, glob, re, importlib

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
from g9_push_dryrun import _load, STIM, _stim_html
from gated_reading import _render_body, _render_task, _html_blocks, _plain, esc, _xml_safe_entities, _render_source_block

_GRADE_GLOB = {
    "G9":  ("Lesson_Bank_G9",  "lesson_g9_l*_v3_1.py"),
    "G10": ("Lesson_Bank_G10", "lesson_g10_l*.py"),
    "G11": ("Lesson_Bank_G11", "lesson_g11_l*.py"),
    "G12": ("Lesson_Bank_G12", "lesson_g12_l*.py"),
}
_MASTERY_MOD = {"G9": "mastery_prompts_g9", "G10": "mastery_prompts_g10",
                "G11": "mastery_prompts_g11", "G12": "mastery_prompts_g12"}


# OPT-IN quick-bank overlay: when PP100_QUICK_BANK_DEPTH is set (env, an int >= 2), _authored applies the
# conservative depth-N auto-bank generator (pp100_autobank) on top of the hand-authored MASTERY entries -
# extending safely-swappable lessons to depth N and leaving source-specific / already-multi-form lessons
# untouched. UNSET (default) => hand-authored entries only, byte-identical to today (prod path is unaffected
# unless the operator explicitly opts in). This is the single choke point both the pusher and assembler read,
# so the overlay reaches them without editing the 4 mastery_prompts_g{N} files.
import os as _os


def _raw_authored(grade):
    try:
        mod = importlib.import_module(_MASTERY_MOD[grade])
        return getattr(mod, "MASTERY", {})
    except Exception:
        return {}


def _authored(grade):
    raw = _raw_authored(grade)
    depth_env = _os.environ.get("PP100_QUICK_BANK_DEPTH", "").strip()
    if not depth_env:
        return raw
    try:
        depth = int(depth_env)
    except ValueError:
        return raw
    if depth < 2:
        return raw
    # apply the generator per lesson; needs the lesson object (for taught sources) + its indep slot
    import pp100_autobank as _AB
    from g9_push_dryrun import STIM as _STIM
    out = dict(raw)
    for _lid, _slot, _prompt, _L in mastery_targets_raw(grade):
        if _slot is None:
            continue
        entry = raw.get(_lid, {}) or {}
        taught = {getattr(s, "ref", "") for s in _L.slots
                  if s.kind == "stimulus_display" and getattr(s, "ref", "")}
        forms, _skip = _AB.build_quick_bank(grade, _lid, entry, _slot, taught, _STIM, depth=depth)
        if len(forms) > 1:
            # promote to a forms[] entry (grain/rubric/frq lifted to entry level; sources+prompts per form)
            out[_lid] = {"unit": forms[0].get("unit"), "rubric_ref": forms[0].get("rubric_ref"),
                         "frq_type": forms[0].get("frq_type", "writing"),
                         "forms": [{"source": f.get("source"), "prompt_html": f.get("prompt_html")}
                                   for f in forms]}
    return out


def _indep_slot(L):
    indep = None
    for s in L.slots:
        if s.kind == "production_frq" and getattr(s, "role", "") == "INDEPENDENT":
            indep = s
    if indep is None:
        prods = [s for s in L.slots if s.kind == "production_frq" and getattr(s, "scored", False)]
        indep = prods[-1] if prods else None
    return indep


def mastery_prompt_html(L, authored_entry):
    """The rendered PP100 prompt HTML: held-out source block + the authored task-specific prompt."""
    parts = []
    src_id = (authored_entry or {}).get("source")
    rec = STIM.get(src_id) if src_id else None
    if rec:
        blocks = _html_blocks(_stim_html(rec)) or [_plain(_stim_html(rec))]
        body = ""
        for k, b in enumerate(blocks):
            if k == 0 and len(blocks) > 1:
                body += f'<div style="font-weight:700;margin:0 0 4px;">{esc(b)}</div>'
            else:
                body += _render_source_block(b)
        parts.append('<div class="tb-source" style="border-left:4px solid #0d9488;background:#f8fafc;'
                     'border-radius:8px;padding:10px 14px;margin:0 0 12px;">'
                     '<div style="font-size:12px;font-weight:700;color:#0f766e;text-transform:uppercase;'
                     'margin-bottom:4px;">New source</div>'
                     f'<div style="color:#1f2a44;line-height:1.6;">{body}</div></div>')
    authored_html = (authored_entry or {}).get("prompt_html")
    if authored_html:
        parts.append(_render_body(authored_html))
    else:
        parts.append(_render_task("This is your mastery task. Apply the skill from this lesson to the new source above."))
    return _xml_safe_entities("".join(parts))


_ROLE_LABEL = {"SUPPORTED": "Supported (we-do)", "MODEL": "Model / diagnosis",
               "INDEPENDENT": "Independent (you-do)", "TRANSFER": "Transfer (new source)"}


def in_lesson_writes(L):
    """[(role_label, title, prompt_html)] for EVERY scored writing task in the lesson (production_frq +
    diagnosis_frq), rendered with the SAME prompt-building a student sees in the article: nearest-preceding
    stimulus inlined ONCE (block-structured), later same-source writes get a one-line reminder. Reuses
    gated_reading.frq_xml so the prompt HTML is byte-for-byte what the article shows, then lifts the
    <qti-prompt>...</qti-prompt> inner HTML back out."""
    from gated_reading import frq_xml, _sentences_to_paras, _source_reminder
    out = []
    cur_source = ""          # nearest-preceding framing source (list of blocks), same as build_lesson_html
    inlined = set()
    for s in L.slots:
        if s.kind == "stimulus_display" and getattr(s, "ref", "") and STIM.get(s.ref):
            blocks = _html_blocks(_stim_html(STIM[s.ref])) or _sentences_to_paras(_plain(_stim_html(STIM[s.ref])))
            cur_source = blocks
            continue
        if s.kind in ("production_frq", "diagnosis_frq"):
            src_key = " ".join(cur_source) if isinstance(cur_source, list) else cur_source
            if cur_source and src_key not in inlined:
                src_arg, reminder = cur_source, ""
                inlined.add(src_key)
            elif cur_source:
                src_arg, reminder = "", _source_reminder(cur_source)
            else:
                src_arg, reminder = "", ""
            xml = frq_xml(f"prev-{s.kind}", s, source_text=src_arg, source_reminder=reminder)
            m = re.search(r"<qti-prompt>(.*)</qti-prompt>", xml, re.S)
            inner = m.group(1) if m else ""
            role = getattr(s, "role", "") or ""
            label = _ROLE_LABEL.get(role, role or s.kind)
            out.append((label, s.title or "Write", inner))
    return out


def mastery_targets_raw(grade):
    """[(lesson_id, indep_slot, None, L)] for a grade - lessons + indep slots WITHOUT the _authored overlay.
    Used by the quick-bank overlay inside _authored (avoids recursion) and anywhere only the lesson objects
    are needed. prompt_html is None here (the overlay does not need it)."""
    subdir, pat = _GRADE_GLOB[grade]
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, subdir, pat))):
        if "_deprecated" in f:
            continue
        m = _load(f)
        L = getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0]
        if not L:
            continue
        out.append((L.id, _indep_slot(L), None, L))
    return out


def mastery_targets(grade):
    """[(lesson_id, indep_slot, prompt_html, L)] for a grade."""
    subdir, pat = _GRADE_GLOB[grade]
    authored = _authored(grade)
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, subdir, pat))):
        if "_deprecated" in f:
            continue
        m = _load(f)
        L = getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0]
        if not L:
            continue
        indep = _indep_slot(L)
        entry = authored.get(L.id, {})
        out.append((L.id, indep, mastery_prompt_html(L, entry), L))
    return out


if __name__ == "__main__":
    g = sys.argv[1] if len(sys.argv) > 1 else "G9"
    t = mastery_targets(g)
    have = sum(1 for _lid, _s, p, _L in t if p and "New source" in p)
    print(f"{g}: {len(t)} mastery targets, {have} with a held-out source block")
