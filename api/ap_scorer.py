"""AP Rubric scorer (Model B).

Scores student essays on the official AP English Language rubric:
- Row A (Thesis): 0-1
- Row B (Evidence & Commentary): 0-4
- Row C (Sophistication): 0-1
- Total: 0-6
"""

import json
import re

from models import FRQType


# ===== Row B Descriptors by FRQ Type =====

ROW_B_DESCRIPTORS = {
    FRQType.RHETORICAL_ANALYSIS: {
        0: "No evidence, or evidence irrelevant to the prompt.",
        1: "Evidence (references or quotes) but no explanation of how it contributes to the argument.",
        2: "Evidence + feature-spotting: names rhetorical devices but does not explain their function or effect.",
        3: "Evidence + S-F-E analysis: explains how rhetorical choices function to achieve the writer's purpose. Some line of reasoning.",
        4: "Evidence + S-F-E analysis + consistent, well-developed line of reasoning throughout the essay.",
    },
    FRQType.ARGUMENT: {
        0: "No evidence, or evidence irrelevant to the claim.",
        1: "Evidence provided but no explanation of how it supports the argument.",
        2: "Evidence + explanation, but generic or superficial commentary.",
        3: "Specific evidence + commentary that explains significance. Some line of reasoning.",
        4: "Specific evidence + commentary explaining significance + consistent line of reasoning throughout.",
    },
    FRQType.SYNTHESIS: {
        0: "Fewer than 2 sources cited, or sources irrelevant.",
        1: "Evidence from sources but no commentary explaining relevance.",
        2: "Evidence from sources + explanation, but superficial or summary-level.",
        3: "Evidence from 3+ sources + analysis of how sources support the argument. Some line of reasoning.",
        4: "Evidence from 3+ sources + sustained analysis + consistent line of reasoning throughout.",
    },
}


def _build_ap_system_prompt(course: str | None = None) -> str:
    """Build the system prompt for AP rubric scoring."""
    grade_level = "Grade 11-12"
    if course == "B1L":
        grade_level = "Grade 11"
    elif course == "B2":
        grade_level = "Grade 12"

    return f"""You are an AP English Language exam reader scoring a student essay.
Score on the official AP rubric (Rows A, B, C). Be calibrated:

ROW A (Thesis, 0-1):
- 0: No thesis, thesis restates prompt, or thesis is not defensible
- 1: Defensible thesis that establishes a line of reasoning

ROW B (Evidence & Commentary, 0-4):
- Scores depend on FRQ type (provided below)
- Key distinction: Row B 2 = feature-spotting (names devices without explaining function)
- Row B 3 requires genuine analysis (S-F-E: explains function AND effect)
- Row B 4 requires sustained, consistent line of reasoning throughout

ROW C (Sophistication, 0-1):
- Must demonstrate at least ONE of:
  1. Broader context (historical, cultural, literary)
  2. Alternative interpretation acknowledged and addressed
  3. Tension/complexity explored without false resolution
  4. Consistently vivid and persuasive prose style
- The move must be organic and integrated, not tacked on

CALIBRATION NOTES:
- Most student essays earn 0-1 on Row A, 1-3 on Row B, 0 on Row C
- A Row B 3 is genuinely strong analysis; do not give it for feature-spotting
- Row C is rare; only award it for genuine sophistication, not surface attempts
- Be honest and calibrated; do not inflate scores

FEEDBACK RULES:
- {grade_level} reading level
- Name the specific Row that needs improvement
- Distinguish feature-spotting from analysis (Row B)
- Identify whether sophistication attempt is organic or tacked-on (Row C)
- Reference specific rubric language
- One concrete next step
- No cheerleading"""


def _build_ap_user_prompt(
    frq_type: FRQType,
    student_text: str,
    passage_text: str | None = None,
    prompt_text: str | None = None,
) -> str:
    """Build the user prompt for AP rubric scoring."""
    row_b_desc = ROW_B_DESCRIPTORS[frq_type]
    row_b_block = "\n".join(f"  {score}: {desc}" for score, desc in row_b_desc.items())

    passage_block = ""
    if passage_text:
        passage_block = f"\nPASSAGE:\n---\n{passage_text}\n---\n"
    elif frq_type == FRQType.ARGUMENT:
        passage_block = "\nPASSAGE: N/A (argument from knowledge)\n"

    prompt_block = ""
    if prompt_text:
        prompt_block = f"\nPROMPT:\n{prompt_text}\n"

    return f"""FRQ TYPE: {frq_type.value}
{passage_block}{prompt_block}
ROW B SCORING FOR {frq_type.value.upper().replace('_', ' ')}:
{row_b_block}

STUDENT ESSAY:
---
{student_text}
---

Score this essay on the AP rubric. Respond in this exact JSON format:
{{
  "row_a": {{ "score": 0|1, "reasoning": "..." }},
  "row_b": {{ "score": 0|1|2|3|4, "reasoning": "..." }},
  "row_c": {{ "score": 0|1, "sophistication_type": null|"broader_context"|"alternative"|"tension"|"style", "reasoning": "..." }},
  "total": <sum of row scores>,
  "feedback": "<2-3 sentences: name the weakest row and one specific revision>",
  "weakest_row": "A"|"B"|"C",
  "next_step": "<1 actionable revision instruction>"
}}

IMPORTANT:
- Quote the student's actual words when pointing to strengths or weaknesses.
- For Row B, explicitly state whether the student reaches S-F-E analysis or stops at feature-spotting.
- For Row C, if awarding 1, name the specific sophistication type and quote the passage that demonstrates it.
- The "total" must equal row_a.score + row_b.score + row_c.score."""


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


def _clamp_ap_scores(data: dict) -> dict:
    """Ensure AP scores are within valid ranges."""
    if "row_a" in data:
        data["row_a"]["score"] = max(0, min(1, data["row_a"].get("score", 0)))
    if "row_b" in data:
        data["row_b"]["score"] = max(0, min(4, data["row_b"].get("score", 0)))
    if "row_c" in data:
        data["row_c"]["score"] = max(0, min(1, data["row_c"].get("score", 0)))

    # Recalculate total
    ra = data.get("row_a", {}).get("score", 0)
    rb = data.get("row_b", {}).get("score", 0)
    rc = data.get("row_c", {}).get("score", 0)
    data["total"] = ra + rb + rc

    return data


def score_ap_essay(
    client,
    model: str,
    frq_type: FRQType,
    student_text: str,
    passage_text: str | None = None,
    prompt_text: str | None = None,
    course: str | None = None,
    temperature: float = 0.3,
) -> dict:
    """Score a single essay on the AP rubric. Returns a dict.

    This is the atomic scoring function -- one Claude call, one result.
    Used directly for single-call grading or as the score_fn for consensus.
    """
    system = _build_ap_system_prompt(course)
    user_prompt = _build_ap_user_prompt(frq_type, student_text, passage_text, prompt_text)

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
        if data and "row_a" in data and "row_b" in data:
            break

        if attempt == 0:
            user_prompt = (
                "Your previous response was not valid JSON or was missing required fields. "
                "Respond with ONLY a JSON object. Required keys: row_a, row_b, row_c, total, "
                "feedback, weakest_row, next_step.\n\n" + user_prompt
            )

    if not data or "row_a" not in data:
        data = {
            "row_a": {"score": 0, "reasoning": "Scoring failed."},
            "row_b": {"score": 0, "reasoning": "Scoring failed."},
            "row_c": {"score": 0, "sophistication_type": None, "reasoning": "Scoring failed."},
            "total": 0,
            "feedback": content[:500] if content else "Scoring failed.",
            "weakest_row": "B",
            "next_step": "Please resubmit for grading.",
        }

    data = _clamp_ap_scores(data)
    data.setdefault("feedback", "")
    data.setdefault("weakest_row", "B")
    data.setdefault("next_step", "")
    data.setdefault("frq_type", frq_type.value)

    return data
