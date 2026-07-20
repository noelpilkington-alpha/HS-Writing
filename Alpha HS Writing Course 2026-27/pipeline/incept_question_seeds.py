"""
incept_question_seeds.py  -  a SEED-ONLY distractor assist over the Incept /api/v1/generate endpoint.

WHAT THIS IS (and is NOT):
  * It asks Incept for CANDIDATE multiple-choice distractors for a skill/concept we teach. The
    candidates are RAW MATERIAL for an authoring agent to select, edit, and verify. This module
    never produces a shippable item.
  * The distinction is the whole point of the module: seeds are NOT items. See SEEDS_ARE_NOT_ITEMS.

DRY-BY-DEFAULT:
  seed_distractors(..., live=False) makes NO network call: it returns the would-send body from
  InceptClient (generation_type == "question"). Only seed_distractors(..., live=True) POSTs and
  returns the raw Incept response (parse it with parse_distractors).

PARSING IS DEFENSIVE:
  parse_distractors accepts several plausible Incept `question` response shapes, excludes any option
  flagged correct, dedups exact repeats within the one response, and returns [] on an unrecognized
  shape. It NEVER raises. Deduping against the caller's existing options is the CALLER's job.

Stdlib only, plus the sibling InceptClient for transport. No em dashes.
"""
from __future__ import annotations

from incept_client import InceptClient

# The guard, stated in plain text so it is impossible to miss: an Incept distractor seed is not an
# item. It must be selected/edited by an author and then pass our contract before any push.
SEEDS_ARE_NOT_ITEMS = (
    "Incept distractor seeds are RAW MATERIAL. An author must select/edit them, "
    "then they must pass gate_structural_item + anti-slop + provenance before any push. Never bind a raw seed."
)


def _build_prompt(skill_prompt: str, existing_options, n: int) -> str:
    """Compose the generate prompt: the skill being taught, the options to avoid duplicating, and n.

    The existing options are embedded so Incept generates DIFFERENT (wrong-answer) distractors,
    not copies of what an author already wrote.
    """
    existing = list(existing_options or [])
    lines = [
        f"Skill or concept being taught: {skill_prompt}",
        "",
        f"Generate {n} plausible but WRONG multiple-choice distractors for this skill.",
        "Each distractor must be clearly incorrect to an expert yet tempting to a struggling learner.",
        "Do NOT duplicate or paraphrase any of the existing options below; produce DIFFERENT distractors.",
    ]
    if existing:
        lines.append("")
        lines.append("Existing options (do not repeat these):")
        for opt in existing:
            lines.append(f"- {opt}")
    return "\n".join(lines)


def seed_distractors(skill_prompt: str, existing_options, n: int = 3,
                     live: bool = False, client: InceptClient | None = None):
    """Ask Incept for candidate multiple-choice distractors for a skill. SEED-ONLY.

    The returned distractors are RAW MATERIAL, never a shippable item: an author must select/edit
    them and they must pass gate_structural_item + anti-slop + provenance before any push. See
    SEEDS_ARE_NOT_ITEMS.

    Builds a `question` generate body with options={"interaction_type": "multiple_choice",
    "structure": "bank"}. `skill_prompt`, the `existing_options` (so Incept avoids duplicates), and
    the count `n` are embedded in the prompt.

    DRY (live=False): returns the client would-send dict (generation_type == "question"); no network.
    LIVE (live=True): POSTs and returns the raw Incept response (parse via parse_distractors).
    """
    if client is None:
        client = InceptClient()
    prompt = _build_prompt(skill_prompt, existing_options, n)
    options = {"interaction_type": "multiple_choice", "structure": "bank"}
    return client.generate(prompt, "question", options=options,
                           subject="writing", live=live)


def _is_correct(opt: dict) -> bool:
    """True if an option dict is flagged correct under any of the plausible field names."""
    for key in ("correct", "is_correct", "answer"):
        if opt.get(key):
            return True
    return False


def _option_text(opt) -> str | None:
    """Extract the display text of an option; None if it has no usable text."""
    if isinstance(opt, str):
        text = opt
    elif isinstance(opt, dict):
        text = opt.get("text", opt.get("value", opt.get("label", "")))
    else:
        return None
    text = str(text).strip()
    return text or None


def parse_distractors(response) -> list:
    """Turn a synthetic/real Incept `question` response into a flat list of distractor strings.

    Defensive about shape: candidates may live under
      response["questions"][i]["options"]  (each option a dict; correct ones excluded), or
      response["distractors"]              (a flat list of strings), or
      response["choices"]                  (options for a single question).
    Excludes any option flagged correct (correct / is_correct / answer). Dedups EXACT repeats within
    this one response (deduping against the caller's existing options is the CALLER's job). Returns
    [] on an unrecognized shape. NEVER raises.
    """
    if not isinstance(response, dict):
        return []

    out: list = []
    seen: set = set()

    def _add(opt) -> None:
        if isinstance(opt, dict) and _is_correct(opt):
            return
        text = _option_text(opt)
        if text is None or text in seen:
            return
        seen.add(text)
        out.append(text)

    # shape 1: response["questions"][i]["options"]
    questions = response.get("questions")
    if isinstance(questions, list):
        for q in questions:
            if not isinstance(q, dict):
                continue
            for opt in (q.get("options") or q.get("choices") or []):
                _add(opt)

    # shape 2: response["distractors"] (flat list)
    for opt in (response.get("distractors") or []):
        _add(opt)

    # shape 3: response["choices"] (single-question options at top level)
    for opt in (response.get("choices") or []):
        _add(opt)

    return out
