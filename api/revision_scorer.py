"""Revision scorer (Model F).

Scores student revisions by comparing original and revised text.
Evaluates whether changes are substantive (transforming ideas, deepening analysis)
or surface (fixing grammar, changing words).
"""

import json
import re


def _build_revision_system_prompt(course: str | None = None) -> str:
    """Build the system prompt for revision scoring."""
    grade_level = "Grade 9"
    if course == "A2":
        grade_level = "Grade 10"
    elif course in ("B1L", "B2"):
        grade_level = "Grade 11-12"

    return f"""You are a writing instructor evaluating a student's revision of their own writing.
Focus on whether the changes are SUBSTANTIVE or SURFACE.

SURFACE EDITING: Fixing grammar, spelling, punctuation, word choice, sentence fluency.
Surface editing makes a 4 into a cleaner 4. It does NOT change the score.

SUBSTANTIVE REVISION: Changing IDEAS -- thesis, evidence selection, argument structure,
analytical depth, sophistication moves, line of reasoning.
Substantive revision makes a 4 into a 5. It DOES change the score.

IMPROVEMENT SCORING:
- 0: No meaningful change, or revision made the writing WORSE
- 1: Surface edits only (grammar, word choice, sentence fluency) -- cleaner but same ideas
- 2: Some substantive changes (new evidence, deeper analysis in one place) but inconsistent
- 3: Genuinely transformed -- new ideas, deeper analysis, or structural improvement throughout

FEEDBACK RULES:
- {grade_level} reading level
- Name the SPECIFIC changes you see
- Distinguish surface from substantive explicitly
- Quote both original and revised text when comparing
- One concrete next step for further revision
- No cheerleading -- only praise genuine improvement"""


def _build_revision_user_prompt(
    original_text: str,
    revised_text: str,
    revision_target: str,
) -> str:
    """Build the user prompt for revision scoring."""
    return f"""REVISION TARGET: {revision_target}

ORIGINAL:
---
{original_text}
---

REVISED:
---
{revised_text}
---

Evaluate the revision. Respond in this exact JSON format:
{{
  "original_assessment": "<1-2 sentences describing the original's strengths and weaknesses>",
  "revision_assessment": "<1-2 sentences describing what changed in the revision>",
  "changes_identified": ["<specific change 1>", "<specific change 2>", ...],
  "substantive": true|false,
  "improvement_score": 0|1|2|3,
  "feedback": "<2-3 sentences: what improved, what is still surface-level, what remains to fix>",
  "next_step": "<1 specific, actionable revision instruction>"
}}

IMPORTANT:
- Quote specific text from both versions when identifying changes.
- "substantive" is true ONLY if at least one change transforms IDEAS, not just fixes errors.
- Be honest about surface-only revisions -- students need to learn the difference.
- The "changes_identified" list should name EVERY noticeable change, labeled as (surface) or (substantive)."""


def _parse_json(text: str) -> dict | None:
    """Parse JSON from API response."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        json_lines = []
        in_block = False
        for line in lines:
            if line.startswith("```") and not in_block:
                in_block = True
                continue
            elif line.startswith("```") and in_block:
                break
            elif in_block:
                json_lines.append(line)
        text = "\n".join(json_lines)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", text, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                pass
    return None


def score_revision(
    client,
    model: str,
    original_text: str,
    revised_text: str,
    revision_target: str,
    course: str | None = None,
    temperature: float = 0.2,
) -> dict:
    """Score a revision comparing original and revised text.

    Returns a dict with: original_assessment, revision_assessment,
    changes_identified, substantive, improvement_score, feedback, next_step.
    """
    system = _build_revision_system_prompt(course)
    user_prompt = _build_revision_user_prompt(original_text, revised_text, revision_target)

    data = None
    for attempt in range(2):
        msg = client.messages.create(
            model=model,
            max_tokens=1536,
            temperature=temperature,
            system=system,
            messages=[{"role": "user", "content": user_prompt}],
        )
        content = msg.content[0].text
        data = _parse_json(content)
        if data and "improvement_score" in data:
            break

        if attempt == 0:
            user_prompt = (
                "Your previous response was not valid JSON. "
                "Respond with ONLY a JSON object. Required keys: "
                "original_assessment, revision_assessment, changes_identified, "
                "substantive, improvement_score, feedback, next_step.\n\n" + user_prompt
            )

    if not data or "improvement_score" not in data:
        data = {
            "original_assessment": "Scoring failed.",
            "revision_assessment": "Scoring failed.",
            "changes_identified": [],
            "substantive": False,
            "improvement_score": 0,
            "feedback": content[:500] if content else "Scoring failed.",
            "next_step": "Please resubmit for grading.",
        }

    # Clamp improvement score
    data["improvement_score"] = max(0, min(3, data.get("improvement_score", 0)))
    data.setdefault("substantive", False)
    data.setdefault("changes_identified", [])
    data.setdefault("feedback", "")
    data.setdefault("next_step", "")

    return data
