"""
incept_test_adapter.py  -  map a raw Incept `test` artifact's output_json into our Item objects.

One-way, PURE (no I/O, no network) so it is testable from a cached fixture. It faithfully represents what
Incept produced: it does NOT strip em dashes or fix length leaks, so the item_contract gates measure the
real artifact. Unmappable fields go to a warnings list, never silently dropped.
"""
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from item_contract import Item, Option  # noqa: E402

# Which failing gates are structural (fatal) vs mechanical/post-fixable.
_FATAL_GATES = {"schema", "acc_tags", "cr_binding", "rubric_config",
                "distractor_integrity", "scr_schema", "scr_binding", "scr_rubric"}
_FIXABLE_GATES = {"no_em_dash", "no_change_discipline", "content"}

def classify_gate_failure(gate_name: str) -> str:
    """A failing gate is 'fatal' (structural) or 'fixable' (mechanical/post-processable)."""
    if gate_name in _FATAL_GATES:
        return "fatal"
    if gate_name in _FIXABLE_GATES:
        return "fixable"
    return "fatal"   # default unknown gates to fatal (conservative: never hide a defect)

def _mc_item(idx, raw, warnings) -> Item:
    # options are bare strings; assign synthetic A/B/C/D ids
    opts_text = raw.get("options") or []
    ans_text = str(raw.get("answer", "")).strip()
    expl = raw.get("explanations") or {}
    options, correct_ids = [], []
    for k, txt in enumerate(opts_text):
        oid = chr(65 + k)
        t = str(txt).strip()
        is_c = (t == ans_text)
        if is_c:
            correct_ids.append(oid)
        options.append(Option(id=oid, text=t, correct=is_c, rationale=str(expl.get(txt, "")).strip()))
    if len(correct_ids) != 1:
        warnings.append(f"item {idx}: MC answer text matched {len(correct_ids)} options (expected 1)")
    md = raw.get("metadata") or {}
    return Item(
        id=f"INCEPT-G9-{idx:02d}", family="SR", grade="9-10", stem=str(raw.get("stem", "")).strip(),
        qti_type="choice", subskill_or_mode="evidence",  # neutral SR subskill for gating parity
        acc_tags=list(md.get("standards") or ["CCSS.W.9-10.1"]),
        options=options, answer_key=list(correct_ids),
        provenance={"copyright": "incept_generated", "dok": md.get("dok"), "difficulty": md.get("difficulty")},
    )

def _constructed_item(idx, raw, warnings) -> Item:
    stem = str(raw.get("stem", "")).strip()
    model = str(raw.get("answer", "")).strip()
    if not model:
        warnings.append(f"item {idx}: constructed item has no model answer")
    md = raw.get("metadata") or {}
    stimulus = raw.get("stimulus")
    has_stim = isinstance(stimulus, dict) and bool(stimulus.get("article"))
    # Heuristic: a long constructed task bound to a passage = ECR essay; a short one = SCR analysis.
    is_essay = len(stem) > 300 or (md.get("difficulty") == "hard" and has_stim)
    if is_essay:
        return Item(
            id=f"INCEPT-G9-{idx:02d}", family="CR", grade="9-10", stem=stem, qti_type="extended-text",
            subskill_or_mode="argument", acc_tags=list(md.get("standards") or ["CCSS.W.9-10.1"]),
            answer_key=[model], stimulus_ref="INCEPT-STIMULUS",  # synthetic ref; gating parity, not a bank lookup
            rubric_ref="rc.staar",
            provenance={"copyright": "incept_generated", "note": "adapter: classified ECR essay"},
        )
    return Item(
        id=f"INCEPT-G9-{idx:02d}", family="SCR", grade="9-10", stem=stem, qti_type="text-entry",
        subskill_or_mode="scr_analysis" if has_stim else "scr_writing",
        acc_tags=list(md.get("standards") or ["CCSS.W.9-10.1"]),
        answer_key=[model], stimulus_ref="INCEPT-STIMULUS" if has_stim else "",
        rubric_ref="rc.scr3" if has_stim else "rc.scr1",
        provenance={"copyright": "incept_generated", "note": "adapter: classified SCR"},
    )

def parse(output_json: dict) -> tuple[list[Item], list[str]]:
    items, warnings = [], []
    raw_items = (output_json or {}).get("items") or []
    for idx, raw in enumerate(raw_items, 1):
        it = str(raw.get("interaction_type", "")).strip().lower()
        if it == "multiple_choice":
            items.append(_mc_item(idx, raw, warnings))
        elif it in ("text_entry", "text-entry", "extended_text", "extended-text"):
            items.append(_constructed_item(idx, raw, warnings))
        else:
            warnings.append(f"item {idx}: unmapped interaction_type '{it}' (kept as SR/choice best-effort)")
            items.append(_mc_item(idx, raw, warnings))
    return items, warnings
