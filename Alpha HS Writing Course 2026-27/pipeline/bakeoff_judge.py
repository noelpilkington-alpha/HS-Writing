"""
bakeoff_judge.py  -  ONE judge path used for BOTH pipelines in the G9 bake-off (fairness).

LIVE: call an LLM judge n times and take the median (the spec's noise mitigation; Incept's own judge was
observed swinging ~17 pts run to run). OFFLINE (default): a deterministic heuristic proxy so tests and
offline bake-off runs are reproducible; it scores structural quality signals the same way for both
pipelines, so it never advantages one source.
"""
from __future__ import annotations
import os, sys, statistics, re, json
sys.path.insert(0, os.path.dirname(__file__))

RUBRIC_VERSION = "g9-item-quality-v1"

_RUBRIC = (
    "You are scoring the QUALITY of a single grade 9 argumentative-writing TEST ITEM, as a neutral "
    "assessment reviewer. Anchor: {anchor}. Score 0-100 on these axes, weighted equally: "
    "(1) distractor plausibility (for MC: are the wrong options tempting but defensibly wrong, each a real "
    "misconception, not filler); (2) discrimination (does the item separate a student who has the skill from "
    "one who does not); (3) gradeability (is the prompt specific enough and the expected response clear "
    "enough that a scorer could reliably tell a strong answer from a weak one); (4) fit to the anchor and "
    "grade 9. Judge ONLY the item shown. You may reason briefly first, but your reply MUST END with a line "
    "in exactly this form and nothing after it:\nSCORE: <integer 0-100>"
)

def _judge_prompt(item, anchor: str) -> str:
    lines = [f"STEM: {getattr(item, 'stem', '')}"]
    if getattr(item, "options", None):
        for o in item.options:
            mark = " [KEY]" if o.correct else ""
            rat = f"  (rationale: {o.rationale})" if o.rationale else ""
            lines.append(f"OPTION {o.id}{mark}: {o.text}{rat}")
    if getattr(item, "answer_key", None):
        lines.append(f"MODEL ANSWER: {item.answer_key[0] if item.answer_key else ''}")
    return _RUBRIC.format(anchor=anchor) + "\n\nITEM:\n" + "\n".join(lines)

def _parse_score(text: str) -> float:
    """Read the judge's score. The judge is told to END with a 'SCORE: <int>' line, which we prefer so a
    leading '1.' in reasoning ('1. Distractor plausibility...') is never mistaken for the score. Falls back
    to a JSON {"score": N} object, then to the LAST number in the text. Returns 0.0 only if no number at all."""
    t = text or ""
    # 1) preferred: the explicit SCORE: line (take the last one if repeated)
    labeled = re.findall(r"SCORE\s*[:=]\s*(\d+(?:\.\d+)?)", t, flags=re.IGNORECASE)
    if labeled:
        return max(0.0, min(100.0, float(labeled[-1])))
    # 2) a JSON object with a score field
    try:
        obj = json.loads(t)
        if isinstance(obj, dict) and "score" in obj:
            return max(0.0, min(100.0, float(obj["score"])))
    except Exception:
        pass
    # 3) last-ditch: the LAST number in the text (a score line, if present, comes last), not the first
    nums = re.findall(r"(\d+(?:\.\d+)?)", t)
    return max(0.0, min(100.0, float(nums[-1]))) if nums else 0.0

def _anthropic_client():
    """Self-contained Anthropic client (mirrors the grader engine's provider logic; NOT a cross-repo import).
    FAILS LOUD if no provider is usable (live judge must never silently fall back to the heuristic)."""
    import anthropic   # lazy: only imported on the live path
    provider = os.environ.get("ANTHROPIC_PROVIDER", "bedrock").strip().lower()
    if provider == "bedrock":
        region = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")).strip()
        return anthropic.AnthropicBedrock(aws_region=region), _model()
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        raise ValueError("live judge needs ANTHROPIC_API_KEY (provider=direct) or ANTHROPIC_PROVIDER=bedrock")
    return anthropic.Anthropic(api_key=key), _model()

def _model() -> str:
    explicit = os.environ.get("ANTHROPIC_MODEL", "").strip()
    if explicit:
        return explicit
    prov = os.environ.get("ANTHROPIC_PROVIDER", "bedrock").strip().lower()
    return "us.anthropic.claude-sonnet-4-6" if prov == "bedrock" else "claude-sonnet-4-6"

def _heuristic_score(item) -> float:
    """Deterministic 0-100 proxy: rewards a real stem, >=3 options for MC, rationalized distractors,
    a model answer for constructed, and no em dashes. SAME logic for both pipelines."""
    s = 60.0
    stem = getattr(item, "stem", "") or ""
    if len(stem) >= 20:
        s += 10
    body = stem + " " + " ".join(o.text + o.rationale for o in getattr(item, "options", []))
    if "\u2014" in body or "\u2013" in body:   # em or en dash present
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
        samples = [base] * max(1, n)   # deterministic: no variance offline
    else:
        cli, model = (client if client else _anthropic_client())
        prompt = _judge_prompt(item, anchor)
        samples = []
        for _ in range(max(1, n)):
            msg = cli.messages.create(model=model, max_tokens=512,
                                      messages=[{"role": "user", "content": prompt}])
            text = "".join(getattr(b, "text", "") for b in msg.content)
            samples.append(_parse_score(text))
    med = statistics.median(samples)
    var = statistics.pvariance(samples) if len(samples) > 1 else 0.0
    return {"median": med, "samples": samples, "variance": var}
