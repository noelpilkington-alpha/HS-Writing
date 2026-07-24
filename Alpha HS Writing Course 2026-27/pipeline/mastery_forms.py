"""
mastery_forms.py  -  normalize a PP100 MASTERY entry into a canonical list of equivalent FORM dicts, and
derive the stable FRQ/test ids each form maps to.

This is the backward-compatibility seam for the PP100 form-bank build (spec:
docs/superpowers/specs/2026-07-23-pp100-form-bank-design.md). Today each mastery_prompts_g{N}.MASTERY[id] is a
SINGLE form: {source, unit, rubric_ref, [frq_type], prompt_html}. The form-bank build lets an entry instead
carry a `forms: [{source, prompt_html, ...}, ...]` list of equivalent forms (same skill/grain/rubric, distinct
held-out source). This module is the ONE place that reads either shape and returns a uniform list, so the
pusher, assembler, coverage report, and QC gate never branch on entry shape.

PROD-SAFETY INVARIANT (the spec's core guarantee): a bank of exactly ONE form must reuse the CURRENT live ids
(`<lesson>-MASTERY-FRQ` / `<lesson>-MASTERY`) and the entry's exact fields, so a single-form lesson is
byte-identical to what is already live on Timeback. Only a bank of >1 uses the `-f{k}` suffixed ids.
"""
from __future__ import annotations

# entry-level fields a form inherits unless it overrides them. grain/rubric/frq_type/mode are held CONSTANT
# across a lesson's forms by the equivalence contract, so they normally live at the entry level and every form
# inherits them; source + prompt_html are what VARY per form.
_INHERITED = ("unit", "rubric_ref", "frq_type", "mode")


def forms_for(entry) -> list[dict]:
    """Return the canonical list of form dicts for a MASTERY entry.

    - {} or None -> [] (no forms).
    - An entry with a `forms: [...]` list -> one dict per listed form, each inheriting the entry-level
      unit/rubric_ref/frq_type/mode unless the form overrides them. The explicit list is authoritative; any
      top-level legacy `source`/`prompt_html` on the entry is ignored (avoids a duplicate form[0]).
    - A legacy single-form entry (no `forms`) -> exactly one form built from the entry's own fields, with
      `source` defaulting to None for source-free lessons. This path is byte-identical to today.
    """
    if not entry:
        return []
    if entry.get("forms"):
        out = []
        for f in entry["forms"]:
            form = dict(f)
            for k in _INHERITED:
                if k not in form and k in entry:
                    form[k] = entry[k]
            form.setdefault("source", None)
            out.append(form)
        return out
    # legacy single-form entry
    form = {"source": entry.get("source")}
    for k in _INHERITED:
        if k in entry:
            form[k] = entry[k]
    if "prompt_html" in entry:
        form["prompt_html"] = entry["prompt_html"]
    return [form]


def form_frq_id(lesson_id: str, k: int, bank_size: int = None) -> str:
    """The FRQ item id for form k (1-indexed) of a lesson.

    bank_size == 1 (or a single-form entry) reuses the CURRENT live id so nothing regresses; a bank > 1 uses
    the `-f{k}` suffix. When bank_size is None the caller has not asserted single-form safety, so the suffixed
    id is used (the safe default for a multi-form world)."""
    if bank_size == 1:
        return f"{lesson_id}-MASTERY-FRQ"
    return f"{lesson_id}-MASTERY-FRQ-f{k}"


def form_test_id(lesson_id: str, k: int, bank_size: int = None) -> str:
    """The single-item assessment-test id for form k (1-indexed) of a lesson (see form_frq_id for the id rule)."""
    if bank_size == 1:
        return f"{lesson_id}-MASTERY"
    return f"{lesson_id}-MASTERY-f{k}"


def bank_resource_id(lesson_id: str) -> str:
    """The assessment-bank Resource id for a lesson's PP100 (the CR points at this when bank > 1)."""
    return f"res-{lesson_id}-pp100-bank"


def form_subresource_id(lesson_id: str, k: int) -> str:
    """The wrapping OneRoster Resource id for form k's single-item test.

    Verified live (2026-07-23 probe): a `type: assessment-bank` bank validates metadata.resources as Resource
    sourcedIds, NOT assessment-test ids. So each form-test must be wrapped in its own Resource, and the bank
    lists these sub-resource ids. Only used when bank > 1 (a single-form lesson has no bank)."""
    return f"res-{lesson_id}-pp100-f{k}"
