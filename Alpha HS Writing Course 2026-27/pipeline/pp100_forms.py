"""
pp100_forms.py  -  build a lesson's PP100 equivalent-form bank and gate it on the equivalence contract.

Spec: docs/superpowers/specs/2026-07-23-pp100-form-bank-design.md.

Two public entry points:
  - qc_form_bank(lesson_id, forms, taught_source, stim) -> (ok, problems): the deterministic equivalence gate.
    A form may enter a lesson's bank only if the bank holds the taught skill/grain/rubric/frq_type/mode constant
    and each held-out source is real, distinct within the lesson, and not the article's taught source. No em dash.
  - build_bank(lesson_id, entry, taught_source, stim) -> (forms, ok, problems): normalize the entry (via
    mastery_forms.forms_for) then gate it. This is what the pusher/assembler call to get a validated form list.

The gate is the bank's admission control: the spec's central invariant ("a form that changes the grain, rubric,
or demand is NOT equivalent and must not enter the bank"). It reuses the existing gate_bank_partition idea
(held-out source != taught source) and adds within-lesson source-distinctness + grain/rubric/mode constancy.
"""
from __future__ import annotations

import mastery_forms as MF

# characters banned from student-facing prompt text (project output-doc-formatting rule): em dash + en dash.
_EM_DASHES = ("—", "–")

# the fields the equivalence contract holds CONSTANT across a lesson's forms
_CONSTANT = ("unit", "rubric_ref", "frq_type", "mode")


def qc_form_bank(lesson_id: str, forms: list[dict], taught_source, stim: dict) -> tuple[bool, list[str]]:
    """Gate a lesson's candidate form bank against the equivalence contract. Returns (ok, problems)."""
    problems: list[str] = []
    if not forms:
        return False, [f"{lesson_id}: empty bank (no forms)"]

    # 1) grain/rubric/frq_type/mode held CONSTANT across the bank (compare each form to the first)
    ref = forms[0]
    for key in _CONSTANT:
        vals = {f.get(key) for f in forms}
        if len(vals) > 1:
            label = "grain (unit)" if key == "unit" else key
            problems.append(f"{lesson_id}: {label} varies across forms ({sorted(str(v) for v in vals)}); "
                            f"the equivalence contract requires it constant")

    # 2) per-form source checks
    seen_sources: dict = {}
    seen_prompts: dict = {}
    for i, f in enumerate(forms, 1):
        src = f.get("source")
        prompt = (f.get("prompt_html") or "")
        # em-dash ban (student-facing)
        if any(d in prompt for d in _EM_DASHES):
            problems.append(f"{lesson_id} form {i}: prompt contains an em dash (banned in student-facing text)")

        if src is None:
            # source-free form: distinctness is on prompt text
            if prompt in seen_prompts:
                problems.append(f"{lesson_id} form {i}: identical prompt to form {seen_prompts[prompt]}; "
                                f"source-free forms must have distinct prompts")
            else:
                seen_prompts[prompt] = i
            continue

        # source-bearing form: exists, distinct within lesson, not the taught source
        if src not in stim:
            problems.append(f"{lesson_id} form {i}: source {src!r} does not exist in the stimulus bank")
        if taught_source and src == taught_source:
            problems.append(f"{lesson_id} form {i}: source {src!r} is the article's taught source "
                            f"(seen-in-lesson leakage); a held-out form must use a different source")
        if src in seen_sources:
            problems.append(f"{lesson_id} form {i}: source {src!r} duplicates form {seen_sources[src]}; "
                            f"each form's held-out source must be distinct within the lesson")
        else:
            seen_sources[src] = i

    return (not problems), problems


def build_bank(lesson_id: str, entry: dict, taught_source, stim: dict) -> tuple[list[dict], bool, list[str]]:
    """Normalize a MASTERY entry into forms and gate them. Returns (forms, ok, problems)."""
    forms = MF.forms_for(entry)
    ok, problems = qc_form_bank(lesson_id, forms, taught_source, stim)
    return forms, ok, problems
