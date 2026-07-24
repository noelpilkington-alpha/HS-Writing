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

# Patterns that signal a factual claim/figure that would need a real source (default DROP if present).
_STAT_PATTERNS = [
    re.compile(r"\b\d+\s*(?:percent|%)", re.I),          # "14 percent", "13%"
    re.compile(r"\b(?:a|an|the|this|that|according to|per the)\s+(?:study|survey|research|report|data|poll|census)\b", re.I),  # citation context
    re.compile(r"\b\d{2,}\s+(?:districts|schools|students|people|cities|states)\b", re.I),  # "62 districts"
    re.compile(r"\bin\s+(?:19|20)\d{2}\b"),               # "in 2019"
    re.compile(r"\bfrom\s+\d+\S*\s+to\s+\d+", re.I),      # "from 21% to 13%"
]

def _fact_verify(item: Item):
    """DETERMINISTIC strip-or-drop: if any option/stem carries a stat/claim pattern we cannot verify, DROP the
    item (default-safe: no fabricated facts to students). Claim-free items pass. An agent verify-pass could
    rescue some, but the deterministic path drops-when-uncertain."""
    body = item.stem + " " + " ".join(o.text for o in item.options) + " " + " ".join(item.answer_key)
    for pat in _STAT_PATTERNS:
        m = pat.search(body)
        if m:
            return None, f"dropped: unverifiable stat/claim '{m.group(0)}'"
    return item, "no stats"

# a fixed cleanup date (deterministic; the module does not call datetime.now to keep tests reproducible)
_CLEANUP_DATE = "2026-07-23"

class _P:
    def __init__(self, t): self.text = t

def _provenance_screen(item: Item):
    """Stamp provenance + run the appropriateness/copyright screen. REJECT verdict -> drop."""
    body = item.stem + "\n" + "\n".join(o.text for o in item.options)
    r = cs.screen([_P(body)], prompt=item.stem, mode="", family="")
    if r["verdict"] == "REJECT":
        reasons = "; ".join(x.get("check", "") for x in r.get("rejects", []))
        return None, f"dropped: content REJECT ({reasons})"
    out = copy.copy(item)
    out.provenance = dict(item.provenance or {})
    out.provenance.update({"copyright": "incept_generated", "model": "incept",
                           "cleaned": _CLEANUP_DATE, "content_screen": r["verdict"]})
    return out, "provenance stamped"

def _fix_scr_model_answer(item: Item):
    """An Incept scr_writing item must carry a model answer to pass the SCR schema gate. The deterministic
    path does NOT fabricate one (that authoring is an own-authored operator step), so a model-less SCR drops."""
    if item.family == "SCR" and item.subskill_or_mode == "scr_writing" and not (item.answer_key and item.answer_key[0].strip()):
        return None, "dropped: Incept SCR has no model answer (author one to include)"
    return item, "scr ok"

def clean_item(item: Item):
    """Ours-origin items pass through untouched. Incept items run the 4 drop-safe steps in order."""
    if (item.provenance or {}).get("bakeoff_source") != "incept":
        return item, ["passthrough (ours)"]
    actions = []
    cur = _strip_em_dash(item); actions.append("em-dash stripped")
    cur, note = _fact_verify(cur); actions.append(note)
    if cur is None:
        return None, actions
    cur, note = _provenance_screen(cur); actions.append(note)
    if cur is None:
        return None, actions
    cur, note = _fix_scr_model_answer(cur); actions.append(note)
    if cur is None:
        return None, actions
    return cur, actions
