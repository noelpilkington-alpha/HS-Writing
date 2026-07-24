"""
pp100_autobank.py  -  conservative depth-N PP100 quick-bank generator (Phase B, "quick banks for Codex").

Goal: give as many lessons as possible a small (depth-3) equivalent-form bank NOW, so a test-out retry serves
a fresh, non-repeating task, WITHOUT hand-authoring every form. It does this only where it is SAFE:

  - forms[0] is ALWAYS the lesson's existing authored prompt, VERBATIM (prod-safe; nothing regresses).
  - forms[1..] reuse the SAME prompt text but point at a DISTINCT held-out source of the same grain/mode/family
    band. This is valid only when the prompt refers to its source generically ("the question/source above") and
    embeds NO source-specific material.
  - If the prompt references source-set-specific content ("the source set above", "the three sources", an
    embedded quoted draft/claim/point the student must react to), a blind source-swap would strand it, so the
    generator REFUSES: it returns only forms[0] plus a skip reason. Those lessons get hand-authored later.

Everything it emits is gated by pp100_forms.qc_form_bank at the call site. Selection is DETERMINISTIC (staggered
by a stable hash of the lesson id) so pushes are idempotent and different lessons in a group start at different
pool offsets. No Math.random / Date - determinism is required for resumable pushes.
"""
from __future__ import annotations
import re

# prompt markers that make a source-swap UNSAFE (the prompt leans on THIS specific source/draft/claim)
_UNSAFE = re.compile(
    r'\"[^\"]{12,}\"'                       # an embedded quoted draft/claim/sentence the student reacts to
    r'|source set above|the (three|two|four) sources|sources? (1|2|3|4)|labeled source'
    r'|claim:|evidence:|point to develop|your point:|weak draft|this draft|the draft (above|below)'
    r'|vague claim|to sharpen|rewrite this|draft to fix|given claim|the sentence:',
    re.I)


def _flat(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html or "")).strip()


def _stagger(lesson_id: str, n: int) -> int:
    """A stable, dependency-free offset in [0, n) from the lesson id (so different lessons start at different
    pool positions and the same lesson is always identical)."""
    if n <= 0:
        return 0
    h = 0
    for ch in lesson_id:
        h = (h * 131 + ord(ch)) & 0xFFFFFFFF
    return h % n


def _eligible_sources(entry, slot, taught_sources, stim):
    """Held-out sources of the same GRAIN family band + MODE as the lesson's taught source, excluding every
    taught source. Family band is inferred from the taught source's own family (same-family swap = safest)."""
    taught_id = entry.get("source")
    taught_rec = stim.get(taught_id) if taught_id else None
    want_mode = str(getattr(taught_rec, "mode", "")) if taught_rec else None
    want_family = getattr(taught_rec, "family", None) if taught_rec else None
    out = []
    for sid, rec in stim.items():
        if sid in taught_sources or sid == taught_id:
            continue
        if want_family is not None and getattr(rec, "family", None) != want_family:
            continue
        if want_mode is not None and str(getattr(rec, "mode", "")) != want_mode:
            continue
        out.append(sid)
    return sorted(out)   # sorted for determinism


def build_quick_bank(grade, lesson_id, entry, slot, taught_sources, stim, depth=3):
    """Return (forms, skip_reason). forms[0] is the existing prompt verbatim; up to depth-1 added forms reuse
    that prompt on distinct held-out sources. skip_reason is None if forms were added, else a string saying why
    the lesson was left single-form (safe refusal). Never emits a source-swapped form for an unsafe prompt."""
    base_prompt = entry.get("prompt_html") or (entry.get("forms", [{}])[0].get("prompt_html") if entry.get("forms") else "")
    base_source = entry.get("source") or (entry.get("forms", [{}])[0].get("source") if entry.get("forms") else None)
    unit = entry.get("unit") or getattr(slot, "unit", None)
    rubric = entry.get("rubric_ref") or getattr(slot, "rubric_ref", None)
    frq = entry.get("frq_type") or getattr(slot, "frq_type", "writing")

    form0 = {"source": base_source, "prompt_html": base_prompt, "unit": unit,
             "rubric_ref": rubric, "frq_type": frq}

    # already a multi-form bank (hand-authored, e.g. L01)? leave it as-is.
    if entry.get("forms") and len(entry["forms"]) > 1:
        return entry["forms"], "already a multi-form bank (left as authored)"

    # unsafe to swap? refuse, return single form.
    if _UNSAFE.search(_flat(base_prompt)):
        return [form0], "prompt references source-specific material; needs a hand-authored variant (not swapped)"

    pool = _eligible_sources(entry, slot, taught_sources, stim)
    if not pool:
        return [form0], "no eligible held-out source of the same grain/mode/family in the pool"

    # staggered round-robin pick of depth-1 distinct sources
    want = max(0, depth - 1)
    start = _stagger(lesson_id, len(pool))
    picked = []
    i = 0
    while len(picked) < want and i < len(pool):
        cand = pool[(start + i) % len(pool)]
        if cand not in picked:
            picked.append(cand)
        i += 1

    forms = [form0]
    for sid in picked:
        forms.append({"source": sid, "prompt_html": base_prompt, "unit": unit,
                      "rubric_ref": rubric, "frq_type": frq})
    return forms, None
