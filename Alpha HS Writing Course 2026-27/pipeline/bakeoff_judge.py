"""
bakeoff_judge.py  -  ONE judge path used for BOTH pipelines in the G9 bake-off (fairness).

LIVE: call an LLM judge n times and take the median (the spec's noise mitigation; Incept's own judge was
observed swinging ~17 pts run to run). OFFLINE (default): a deterministic heuristic proxy so tests and
offline bake-off runs are reproducible; it scores structural quality signals the same way for both
pipelines, so it never advantages one source.
"""
from __future__ import annotations
import os, sys, statistics
sys.path.insert(0, os.path.dirname(__file__))

def _heuristic_score(item) -> float:
    """Deterministic 0-100 proxy: rewards a real stem, >=3 options for MC, rationalized distractors,
    a model answer for constructed, and no em dashes. SAME logic for both pipelines."""
    s = 60.0
    stem = getattr(item, "stem", "") or ""
    if len(stem) >= 20:
        s += 10
    body = stem + " ".join(o.text + o.rationale for o in getattr(item, "options", []))
    if "—" in body or "–" in body:   # em/en dash present
        s -= 15
    if item.qti_type == "choice":
        opts = item.options
        if len(opts) >= 3:
            s += 10
        distractors = [o for o in opts if not o.correct]
        if distractors and all(o.rationale.strip() for o in distractors):
            s += 10
        # length-leak signal: correct option not the conspicuous longest
        if opts:
            correct = [o for o in opts if o.correct]
            dl = [len(o.text) for o in opts if not o.correct]
            if correct and dl and len(correct[0].text) <= max(dl) * 1.25:
                s += 10
    else:
        if item.answer_key and item.answer_key[0].strip():
            s += 15
    return max(0.0, min(100.0, s))

def judge_item(item, anchor: str = "STAAR English I (G9 argument)", n: int = 3,
               live: bool = False, client=None) -> dict:
    if not live:
        base = _heuristic_score(item)
        samples = [base, base, base][:max(1, n)]   # deterministic: no variance offline
    else:
        # LIVE: call the real judge n times. Kept minimal + identical for both pipelines.
        from incept_client import InceptClient
        client = client or InceptClient()
        samples = []
        for _ in range(max(1, n)):
            verdict = client.qc("question", _item_to_qc_content(item), prompt=anchor, live=True)
            samples.append(float(_extract_score(verdict)))
    med = statistics.median(samples)
    var = statistics.pvariance(samples) if len(samples) > 1 else 0.0
    return {"median": med, "samples": samples, "variance": var}

def _item_to_qc_content(item) -> dict:
    return {"stem": item.stem,
            "options": [o.text for o in item.options],
            "answer_key": {"answer": (item.answer_key[0] if item.answer_key else "")}}

def _extract_score(verdict: dict) -> float:
    v = (verdict or {}).get("verdict") or verdict or {}
    return float(v.get("judge_score", 0.0))
