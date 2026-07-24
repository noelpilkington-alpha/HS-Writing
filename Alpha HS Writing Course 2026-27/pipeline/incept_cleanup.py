"""
incept_cleanup.py  -  make an Incept-generated Item student-shippable before it lands on a real form.

Four DROP-SAFE steps (em-dash strip, fact-verify, provenance+copyright screen, SCR model-answer). Ours-origin
items pass through untouched. clean_item runs all 4 on Incept items, short-circuiting to dropped-with-reason
on the first unrecoverable failure and accumulating an actions log. Nothing ambiguous ships.
"""
from __future__ import annotations
import os, sys, re, copy
sys.path.insert(0, os.path.dirname(__file__))
from item_contract import Item, Option  # noqa: E402
import content_screen as cs  # noqa: E402

def _dedash(text: str) -> str:
    """Replace em/en dashes with house-style punctuation, preserving content. A spaced dash becomes a comma;
    a bare dash becomes a comma too (never drops words)."""
    t = text or ""
    t = t.replace(" \u2014 ", ", ").replace(" \u2013 ", ", ")
    t = t.replace("\u2014", ", ").replace("\u2013", ", ")
    return t

def _strip_em_dash(item: Item) -> Item:
    out = copy.copy(item)
    out.provenance = dict(item.provenance or {})
    out.stem = _dedash(item.stem)
    out.options = [Option(id=o.id, text=_dedash(o.text), correct=o.correct, rationale=_dedash(o.rationale))
                   for o in item.options]
    out.answer_key = [_dedash(a) for a in item.answer_key]
    return out
