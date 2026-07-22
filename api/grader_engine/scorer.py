"""Single-grader scoring: one Claude API call per question."""

import json
import logging
import os
import re
import time

import anthropic
import httpx

from .models import QuestionScore, sub_maxes

logger = logging.getLogger(__name__)

# Timeout for each API call (connect, read, write, pool)
API_TIMEOUT = httpx.Timeout(10.0, read=90.0, write=10.0, pool=10.0)
MAX_RETRIES = 3
RETRY_BACKOFF = [2, 5, 10]  # seconds between retries

# Transient errors worth retrying (httpx + Anthropic SDK's own error types)
_TRANSIENT_ERRORS = (
    httpx.TimeoutException, httpx.ConnectError, httpx.RemoteProtocolError,
    anthropic.APITimeoutError, anthropic.APIConnectionError,
)


def _api_call_with_retry(client, **kwargs):
    """Make an API call with timeout and retry on transient failures."""
    for attempt in range(MAX_RETRIES):
        try:
            return client.messages.create(timeout=API_TIMEOUT, **kwargs)
        except _TRANSIENT_ERRORS as e:
            if attempt < MAX_RETRIES - 1:
                wait = RETRY_BACKOFF[attempt]
                logger.warning(f"API call failed (attempt {attempt + 1}/{MAX_RETRIES}): {e}. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                logger.error(f"API call failed after {MAX_RETRIES} attempts: {e}")
                raise
        except anthropic.RateLimitError as e:
            if attempt < MAX_RETRIES - 1:
                wait = RETRY_BACKOFF[attempt] * 2
                logger.warning(f"Rate limited (attempt {attempt + 1}/{MAX_RETRIES}): {e}. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise
        except Exception as e:
            # Catch-all for rate limit messages not using the SDK error type
            if "rate" in str(e).lower() or "throttl" in str(e).lower() or "529" in str(e) or "overloaded" in str(e).lower():
                if attempt < MAX_RETRIES - 1:
                    wait = RETRY_BACKOFF[attempt] * 2
                    logger.warning(f"Rate limited (attempt {attempt + 1}/{MAX_RETRIES}): {e}. Retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    raise
            else:
                raise
from .rubrics.assembler import assemble_observation_prompt
from .rubrics.scoring import (
    score_q1_q5, score_q6_q10, score_q11_paragraph, score_q11_essay,
    build_teacher_notes_q1_q5, build_teacher_notes_q6_q10,
    build_teacher_notes_q11_paragraph, build_teacher_notes_q11_essay,
    build_teacher_notes_from_scores,
)


def extract_text(msg) -> str:
    """Return the assistant's TEXT output, robust to leading thinking blocks.

    Opus 4.8 (and any adaptive-thinking call) can return content[0] as a ThinkingBlock with no
    `.text` attribute — so the old `extract_text(msg)` grabbed the wrong block (or raised) and
    callers silently defaulted scores to 0. Concatenate every text block instead.
    """
    if not getattr(msg, "content", None):
        return ""
    parts = []
    for block in msg.content:
        t = getattr(block, "text", None)
        if t:
            parts.append(t)
    return "\n".join(parts)

SYSTEM_PROMPT_BASE = (
    "You are a grading assistant. Follow the rubric. "
    "Your entire response must be a single valid JSON object — no preamble, "
    "no commentary, no markdown fences, no reasoning walkthrough before the JSON. "
    "Do all reasoning internally, then output ONLY the JSON.\n"
    "Required keys:\n"
    '  "question": integer (question number),\n'
    '  "ideas_score": integer,\n'
    '  "ideas_max": integer,\n'
    '  "conventions_score": integer,\n'
    '  "conventions_max": integer,\n'
    '  "total_score": integer,\n'
    '  "total_max": integer,\n'
    '  "feedback": string (student-facing feedback following the rubric output rules),\n'
    '  "internal_notes": string (brief internal reasoning)\n'
)

SYSTEM_PROMPT_Q11_PARAGRAPH = (
    "You are a grading assistant scoring a student paragraph. "
    "Match the paragraph to the single best-fit anchor in the rubric. "
    "Each anchor is a FIXED score (15, 13, 11, 9, 7, 5, or 0) — not a range. "
    "When in doubt between two anchors, choose the HIGHER one. "
    "A paragraph with a clear main idea, 2+ supporting details, and reasonable order = 11 or above. "
    "A paragraph with clear main idea, 2-3 details that clearly support it, and logical order = 13. "
    "Your entire response must be a single valid JSON object — no preamble, "
    "no commentary, no markdown fences, no reasoning walkthrough before the JSON. "
    "Do all reasoning internally, then output ONLY the JSON.\n\n"
    "IMPORTANT: You MUST populate the enumeration fields BEFORE deciding the "
    "conventions score. List what you find first, then apply the thresholds.\n\n"
    "LOCK RULE: Your conventions score MUST match the enumeration counts + "
    "grade-level thresholds. Only count [NOTABLE] errors toward thresholds — "
    "[MINOR] errors are mentioned in feedback but do not affect the score. "
    "Do NOT second-guess or adjust downward after enumerating.\n\n"
    "Required keys:\n"
    '  "question": integer (question number),\n'
    "\n"
    "  --- ENUMERATION (populate these FIRST) ---\n"
    '  "spelling_errors": list of strings — prefix each with [NOTABLE] or [MINOR]\n'
    '  "grammar_errors": list of strings — prefix each with [NOTABLE] or [MINOR]\n'
    '  "punctuation_errors": list of strings — prefix each with [NOTABLE] or [MINOR]\n'
    "\n"
    "  --- SCORES (derived from rubric anchors + enumeration thresholds) ---\n"
    '  "ideas_score": integer,\n'
    '  "ideas_max": integer,\n'
    '  "conventions_score": integer,\n'
    '  "conventions_max": integer,\n'
    '  "total_score": integer,\n'
    '  "total_max": integer,\n'
    '  "feedback": string (student-facing feedback following the rubric output rules),\n'
    '  "internal_notes": string (brief internal reasoning)\n'
)

SYSTEM_PROMPT_ESSAY = (
    "You are a grading assistant. Follow the rubric exactly. "
    "Your entire response must be a single valid JSON object — no preamble, "
    "no commentary, no markdown fences, no reasoning walkthrough before the JSON. "
    "Do all reasoning internally, then output ONLY the JSON. "
    "Keep `internal_notes` to 2-3 sentences summarizing the key scoring decisions — "
    "do NOT re-enumerate errors or causal sentences there (those are already in their "
    "own fields). This keeps the response under the token limit.\n\n"
    "IMPORTANT: You MUST populate the enumeration fields BEFORE deciding scores. "
    "List what you find first, then apply the thresholds in the rubric.\n\n"
    "LOCK RULE: Your numeric scores MUST match your enumeration counts + thresholds. "
    "Only count [NOTABLE] errors toward thresholds — [MINOR] errors are mentioned "
    "in feedback but do not affect the score. Do NOT second-guess or adjust downward "
    "after enumerating.\n\n"
    "The rubric uses 5 Alpha categories grouped into 3 JSON score fields:\n"
    "  ideas_score   = Structure (0-5) + Evidence & Explanation (0-5) = max 10\n"
    "  organization_score = Organization (0-4) + Sentence Quality (0-3) = max 7\n"
    "  conventions_score  = Editing (0-3) = max 3\n\n"
    "Required keys:\n"
    '  "question": integer (question number),\n'
    "\n"
    "  --- ENUMERATION (populate these FIRST) ---\n"
    '  "causal_sentences": list of strings — quote each student sentence that\n'
    "    explains a CONSEQUENCE, MECHANISM, or CAUSE-AND-EFFECT chain.\n"
    "    Include any sentence where the student explains WHY something matters\n"
    "    or WHAT HAPPENS AS A RESULT. Copy the student's exact words.\n"
    '  "spelling_errors": list of strings — prefix each with [NOTABLE] or [MINOR]\n'
    '  "grammar_errors": list of strings — prefix each with [NOTABLE] or [MINOR]\n'
    '  "punctuation_errors": list of strings — prefix each with [NOTABLE] or [MINOR]\n'
    "\n"
    "  --- SCORES (derived from enumeration + rubric thresholds) ---\n"
    '  "ideas_score": integer (Structure + Evidence, max 10),\n'
    '  "ideas_max": 10,\n'
    '  "organization_score": integer (Organization + Sentences, max 7),\n'
    '  "organization_max": 7,\n'
    '  "conventions_score": integer (Editing, max 3),\n'
    '  "conventions_max": 3,\n'
    '  "total_score": integer (ideas_score + organization_score + conventions_score, max 20),\n'
    '  "total_max": 20,\n'
    '  "feedback": string (student-facing feedback following the rubric output rules),\n'
    '  "internal_notes": string (brief internal reasoning)\n'
)


def _fill_rubric(rubric: str, passage: str, question: str, response: str) -> str:
    """Replace template placeholders in the rubric."""
    filled = rubric
    filled = filled.replace("{{passage}}", passage or "(no passage)")
    filled = filled.replace("{{question}}", question or "(no question)")
    filled = filled.replace("{{response}}", response or "(no response)")
    return filled


def _parse_json(text: str) -> dict | None:
    """Try to parse JSON from the API response.

    Robustness layers:
    1. Direct parse of full text (fast path when the model complied)
    2. Strip markdown code fences (```json ... ```)
    3. Brace-balanced scanner: finds the LAST balanced {...} block with a
       top-level "total_score" key, since some models narrate first and
       then write the JSON at the end. Preamble-then-JSON is common enough
       that the first {...} regex match can miss the real payload.
    """
    if not text:
        return None

    # Layer 1: direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Layer 2: strip markdown fences
    stripped = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.IGNORECASE)
    stripped = re.sub(r"\s*```$", "", stripped)
    if stripped != text:
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            pass

    # Layer 3: brace-balanced scanner. Collect every balanced {...} block,
    # then return the last one that parses and contains "total_score".
    candidates = []
    depth = 0
    start = None
    in_str = False
    escape = False
    for i, ch in enumerate(text):
        if in_str:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
            continue
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            if depth > 0:
                depth -= 1
                if depth == 0 and start is not None:
                    candidates.append(text[start:i + 1])
                    start = None

    # Prefer the largest block containing "total_score"
    for block in sorted(candidates, key=len, reverse=True):
        if '"total_score"' in block:
            try:
                return json.loads(block)
            except json.JSONDecodeError:
                continue

    # Fall back to any parseable block
    for block in sorted(candidates, key=len, reverse=True):
        try:
            return json.loads(block)
        except json.JSONDecodeError:
            continue

    return None


def _count_notable(errors: list) -> int:
    """Count only [NOTABLE]-prefixed errors. Unprefixed errors are treated as notable."""
    count = 0
    for e in errors:
        e_str = str(e).strip().upper()
        if e_str.startswith("[MINOR]"):
            continue
        count += 1
    return count


def _count_paragraphs(response: str) -> int:
    """Count actual paragraph breaks in a student response.

    A paragraph is a non-empty block separated from others by one or more
    blank lines. HTML <p> tags are also counted. Returns at least 1 for
    any non-empty response. This is a deterministic count used to guard
    against LLM hallucination of paragraph structure that isn't there.
    """
    if not response or not response.strip():
        return 0

    # Strip common HTML wrappers first. <p>...</p> blocks count as paragraphs.
    html_p = re.findall(r"<p[^>]*>(.*?)</p>", response, flags=re.DOTALL | re.IGNORECASE)
    if html_p:
        # Count non-empty <p> blocks (ignore <p><br></p> spacers)
        non_empty = [
            p for p in html_p
            if re.sub(r"<[^>]+>", "", p).strip()
        ]
        if non_empty:
            return len(non_empty)

    # Fall back to blank-line separation. Normalize line endings first.
    text = response.replace("\r\n", "\n").replace("\r", "\n")
    # A paragraph break is one or more blank lines between non-empty blocks.
    blocks = re.split(r"\n\s*\n+", text.strip())
    non_empty_blocks = [b for b in blocks if b.strip()]
    return max(1, len(non_empty_blocks))


def _enforce_enumeration(data: dict, qnum: int, grade: int = 5, paragraph_count: int | None = None) -> dict:
    """Override conventions scores using enumeration counts when available.

    The model sometimes self-corrects downward against its own enumeration.
    This function mechanically applies the rubric thresholds to the
    enumerated error lists, ensuring scores match the evidence.
    Only counts [NOTABLE] errors toward thresholds; [MINOR] errors are
    mentioned in feedback but don't affect scores.
    Applies to Q11 for all grades: G6-G8 essays (6pt) and G3-G5 paragraphs (5pt).

    If paragraph_count is provided, a G6-G8 essay with <5 paragraphs has
    its Structure component capped: 1 paragraph = 1/5, 2 = 2/5, 3 = 3/5,
    4 = 4/5. This prevents the grader from hallucinating paragraph
    structure that isn't in the response.
    """
    if qnum != 11:
        return data

    # --- G3-G5 paragraph conventions (5-point scale, total notable budget) ---
    if grade < 6:
        spelling = data.get("spelling_errors")
        grammar = data.get("grammar_errors")
        punctuation = data.get("punctuation_errors")
        if not any(isinstance(x, list) for x in (spelling, grammar, punctuation)):
            return data

        total_notable = 0
        for errs in (spelling, grammar, punctuation):
            if isinstance(errs, list):
                total_notable += _count_notable(errs)

        # Grade-level thresholds: max total notables for each score level
        para_thresholds = {
            3: [(1, 5), (3, 4), (5, 3), (99, 2)],   # 0-1→5, 2-3→4, 4-5→3, 6+→2
            4: [(0, 5), (2, 4), (4, 3), (99, 2)],    # 0→5, 1-2→4, 3-4→3, 5+→2
            5: [(0, 5), (1, 4), (3, 3), (99, 2)],    # 0→5, 1→4, 2-3→3, 4+→2
        }
        thresholds = para_thresholds.get(grade, para_thresholds[3])

        computed = 2  # default floor (meaning mostly clear)
        for max_notables, score in thresholds:
            if total_notable <= max_notables:
                computed = score
                break

        # Allow 1/5 or 0/5 only if the model also judged meaning impairment
        model_conv = data.get("conventions_score", 0)
        if model_conv <= 1:
            computed = min(computed, model_conv)

        if computed != model_conv:
            logger.info(
                f"Paragraph enumeration override: conventions {model_conv} -> {computed} "
                f"(total_notable={total_notable}, grade={grade})"
            )
            data["conventions_score"] = computed

        return data

    spelling = data.get("spelling_errors")
    grammar = data.get("grammar_errors")
    punctuation = data.get("punctuation_errors")
    causal = data.get("causal_sentences")

    # Editing sub-scores: each is 0 or 1 (max 3 total).
    # Grade-level thresholds: max NOTABLE errors for 1/1.
    # Loosened 2026-04-21 to align with STAAR clarity-based convention scoring
    # (STAAR 2025 G6 SP5 R2 awarded 2/2 with 5 spelling errors). The prior
    # stricter thresholds produced systematic under-scoring vs STAAR anchors.
    # Guardrail: graders must still count ALL errors a typical reader would
    # see. They must NOT use advanced inference to "fix" ambiguity a human
    # reader could not resolve.
    editing_thresholds = {
        6: {"grammar": 1, "spelling": 4, "punctuation": 2},
        7: {"grammar": 1, "spelling": 3, "punctuation": 2},
        8: {"grammar": 1, "spelling": 2, "punctuation": 1},
    }
    ft = editing_thresholds.get(grade, editing_thresholds[6])

    model_conv = data.get("conventions_score", 0)

    if spelling is not None and isinstance(spelling, list):
        n = _count_notable(spelling)
        data["_spelling_sub"] = 1 if n <= ft["spelling"] else 0
    if grammar is not None and isinstance(grammar, list):
        n = _count_notable(grammar)
        data["_grammar_sub"] = 1 if n <= ft["grammar"] else 0
    if punctuation is not None and isinstance(punctuation, list):
        n = _count_notable(punctuation)
        data["_punctuation_sub"] = 1 if n <= ft["punctuation"] else 0

    # If all three sub-scores were computed, override conventions_score
    if all(k in data for k in ("_spelling_sub", "_grammar_sub", "_punctuation_sub")):
        computed_conv = data["_spelling_sub"] + data["_grammar_sub"] + data["_punctuation_sub"]
        if computed_conv != model_conv:
            logger.info(
                f"Enumeration override: conventions {model_conv} -> {computed_conv} "
                f"(spell={len(spelling)}, gram={len(grammar)}, punct={len(punctuation)})"
            )
            data["conventions_score"] = computed_conv

    # Analysis: compute from causal sentence count
    if causal is not None and isinstance(causal, list):
        n = len(causal)
        computed_analysis = 2 if n >= 2 else (1 if n == 1 else 0)
        data["_analysis_sub"] = computed_analysis

    # Paragraph-count gate: cap ideas_score based on actual paragraph breaks.
    # ideas_score = Structure (0-5) + Evidence (0-5) where Structure scales
    # directly with paragraph count. If grader reports ideas_score higher than
    # the cap allows, reduce it. A 1-paragraph response cannot earn more than
    # Structure 1/5 regardless of how strong the content is.
    if paragraph_count is not None and paragraph_count < 5:
        # Maximum Evidence + Explanation is 5/5
        structure_cap = max(0, paragraph_count)  # 1 para -> 1, 2 -> 2, etc.
        ideas_cap = structure_cap + 5
        model_ideas = data.get("ideas_score", 0)
        if model_ideas > ideas_cap:
            logger.info(
                f"Paragraph-count override: ideas_score {model_ideas} -> {ideas_cap} "
                f"(actual paragraphs={paragraph_count}, structure capped at {structure_cap}/5)"
            )
            data["ideas_score"] = ideas_cap
            # Recompute total_score if present
            if all(k in data for k in ("organization_score", "conventions_score")):
                data["total_score"] = (
                    data["ideas_score"]
                    + data.get("organization_score", 0)
                    + data.get("conventions_score", 0)
                )

    # Clean up internal keys before returning
    for k in ("_spelling_sub", "_grammar_sub", "_punctuation_sub", "_analysis_sub"):
        data.pop(k, None)

    return data


def _clamp_scores(data: dict, qnum: int, max_score: int, grade: int = 5) -> dict:
    """Ensure scores don't exceed known maximums."""
    ideas_max, org_max, conv_max = sub_maxes(qnum, grade)
    data["ideas_score"] = min(data.get("ideas_score", 0), ideas_max)
    data["ideas_max"] = ideas_max
    data["organization_score"] = min(data.get("organization_score", 0), org_max)
    data["organization_max"] = org_max
    data["conventions_score"] = min(data.get("conventions_score", 0), conv_max)
    data["conventions_max"] = conv_max
    data["total_score"] = min(
        data["ideas_score"] + data["organization_score"] + data["conventions_score"],
        max_score,
    )
    data["total_max"] = max_score
    data.setdefault("question", qnum)
    return data


def score_question(
    client,
    model: str,
    rubric: str,
    passage: str,
    question: str,
    response: str,
    qnum: int,
    max_score: int,
    temperature: float = 0.3,
    grade: int = 5,
) -> QuestionScore:
    """Run a single grading call and return a QuestionScore.

    This is the atomic unit of grading — one Claude call, one score.
    """
    filled = _fill_rubric(rubric, passage, question, response)
    # Q11 essays need room for enumeration + short reasoning; bumped to 4096
    # after token-limit-induced truncation was observed during calibration
    # validation (2026-04-21). Models sometimes narrate in internal_notes
    # past 2048 tokens and produce unterminated JSON.
    tokens = 4096 if qnum == 11 else 1024
    # Use specialized system prompts for Q11 scoring
    if grade >= 6 and qnum == 11:
        system_prompt = SYSTEM_PROMPT_ESSAY
    elif qnum == 11 and grade < 6:
        system_prompt = SYSTEM_PROMPT_Q11_PARAGRAPH
    else:
        system_prompt = SYSTEM_PROMPT_BASE
    user_msg = f"Grade question {qnum} (max {max_score} points).\n\n{filled}"

    data = None
    content = ""
    # Opus 4.7 rejects the temperature parameter. Drop it for that model.
    api_kwargs = {
        "model": model,
        "max_tokens": tokens,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_msg}],
    }
    if "opus-4-7" not in (model or ""):
        api_kwargs["temperature"] = temperature
    for attempt in range(2):
        msg = _api_call_with_retry(client, **api_kwargs)
        content = extract_text(msg)
        data = _parse_json(content)
        if data is not None:
            break

        # Retry with explicit JSON reminder
        if attempt == 0:
            user_msg = (
                "Your previous response was not valid JSON. "
                "Respond with ONLY a JSON object, starting with { and ending with }. "
                "No other text.\n\n" + user_msg
            )
            time.sleep(0.5)

    if data is None:
        logger.error(
            f"JSON parse failed for qnum={qnum} grade={grade} after 2 attempts. "
            f"Raw response length: {len(content)} chars. First 500 chars: {content[:500]!r}"
        )
        data = {
            "question": qnum,
            "ideas_score": 0, "ideas_max": 0,
            "organization_score": 0, "organization_max": 0,
            "conventions_score": 0, "conventions_max": 0,
            "total_score": 0, "total_max": max_score,
            "feedback": content[:500] if content else "Grading failed.",
            "internal_notes": f"JSON_PARSE_FAILED: raw={content[:1000]!r}",
        }

    # Compute actual paragraph count for G6-G8 essays to guard against
    # the grader hallucinating paragraph structure
    paragraph_count = None
    if qnum == 11 and grade >= 6:
        paragraph_count = _count_paragraphs(response)

    data = _enforce_enumeration(data, qnum, grade, paragraph_count=paragraph_count)
    data = _clamp_scores(data, qnum, max_score, grade)
    data.setdefault("feedback", "")
    data.setdefault("internal_notes", "")

    result = QuestionScore.from_dict(data)
    # Generate teacher notes from scores + Claude's internal reasoning
    result.teacher_notes = build_teacher_notes_from_scores(result, result.internal_notes)
    return result


# ---------------------------------------------------------------------------
# AlphaTest Plaintext Grading Mode
# ---------------------------------------------------------------------------

SYSTEM_PROMPT_ALPHATEST = (
    "You are a careful writing grader. Follow the rubric exactly. "
    "Output in the structured plaintext format specified — evidence log, "
    "scores with derivation, arithmetic check, TOTAL line, and feedback."
)


def _alphatest_model() -> str:
    """Get the model for AlphaTest grading — always Opus 4.7.

    AlphaTest prompts are calibrated for Opus. Uses same provider detection
    as per_cat (which works on Render).
    """
    explicit = os.environ.get("ALPHA_ALPHATEST_MODEL", "").strip()
    if explicit:
        return explicit
    provider = os.environ.get("ANTHROPIC_PROVIDER", "bedrock").strip().lower()
    if provider == "anthropic":
        return "claude-opus-4-7"
    return "us.anthropic.claude-opus-4-7"


def score_question_alphatest(
    client,
    model: str,
    rubric: str,
    passage: str,
    question: str,
    response: str,
    qnum: int,
    max_score: int,
    temperature: float = 0.3,
    grade: int = 5,
) -> QuestionScore:
    """Score using AlphaTest plaintext format (TOTAL: X/Y extraction)."""
    filled = _fill_rubric(rubric, passage, question, response)
    tokens = 3000 if qnum == 11 else 1024
    user_msg = f"Grade question {qnum} (max {max_score} points).\n\n{filled}"

    # Always use Opus 4.7 — AlphaTest prompts are calibrated for it
    alphatest_model = _alphatest_model()
    import hashlib
    rubric_hash = hashlib.md5(rubric.encode()).hexdigest()[:8]
    print(f"[ALPHATEST] Q{qnum} model={alphatest_model} client={type(client).__name__} rubric_len={len(rubric)} hash={rubric_hash}", flush=True)

    api_kwargs = {
        "model": alphatest_model,
        "max_tokens": tokens,
        "system": SYSTEM_PROMPT_ALPHATEST,
        "messages": [{"role": "user", "content": user_msg}],
    }
    if "opus-4-7" not in (alphatest_model or ""):
        api_kwargs["temperature"] = temperature

    msg = _api_call_with_retry(client, **api_kwargs)
    content = extract_text(msg)

    return _parse_alphatest_response(content, qnum, max_score, grade)


def _parse_alphatest_response(
    content: str, qnum: int, max_score: int, grade: int
) -> QuestionScore:
    """Parse the AlphaTest plaintext response into a QuestionScore.

    Simple: extract TOTAL: X/Y for the score, FEEDBACK: section for feedback.
    The total score is reported as-is without sub-score decomposition.
    """
    ideas_max, org_max, conv_max = sub_maxes(qnum, grade)

    # Extract TOTAL: X/Y
    total_match = re.search(r"TOTAL:\s*(\d+)\s*/\s*(\d+)", content)
    if not total_match:
        logger.error(f"AlphaTest TOTAL parse failed for Q{qnum}. Response: {content[:500]!r}")
        return QuestionScore(
            question=qnum,
            ideas_score=0, ideas_max=ideas_max,
            organization_score=0, organization_max=org_max,
            conventions_score=0, conventions_max=conv_max,
            total_score=0, total_max=max_score,
            feedback="Grading failed — could not parse score.",
            internal_notes=f"ALPHATEST_PARSE_FAILED: {content[:500]}",
        )

    total_score = min(int(total_match.group(1)), max_score)

    # Extract feedback section — handle any whitespace/newline after FEEDBACK:
    feedback_match = re.search(r"FEEDBACK:\s*(.+)", content, re.DOTALL)
    feedback = feedback_match.group(1).strip() if feedback_match else ""

    # Report total as the ideas_score (full allocation) — no sub-score decomposition
    result = QuestionScore(
        question=qnum,
        ideas_score=total_score, ideas_max=max_score,
        organization_score=0, organization_max=0,
        conventions_score=0, conventions_max=0,
        total_score=total_score, total_max=max_score,
        feedback=feedback,
        internal_notes=content[:1000],
    )
    result.teacher_notes = content.split("FEEDBACK:")[0].strip() if "FEEDBACK:" in content else ""
    return result




# ---------------------------------------------------------------------------
# Phase 2: Observation-then-Score
# ---------------------------------------------------------------------------

SYSTEM_PROMPT_OBSERVER = (
    "You are a grading observation assistant. Your job is to carefully observe "
    "a student's writing response and report structured observations — NOT scores. "
    "Scoring will be computed separately from your observations.\n\n"
    "Your entire response must be a single valid JSON object — no preamble, "
    "no commentary, no markdown fences. Do all reasoning internally, then output "
    "ONLY the JSON with the observation fields specified in the rubric.\n\n"
    "Be precise and literal. Report exactly what you see, not what you think the "
    "student intended. Do not autocorrect or infer."
)


def observe_and_score(
    client,
    model: str,
    test_code: str,
    passage: str,
    question: str,
    response: str,
    qnum: int,
    max_score: int,
    temperature: float = 0.3,
    grade: int = 5,
) -> QuestionScore:
    """Phase 2: Extract observations via Claude, then score deterministically.

    1. Assembles an observation prompt for the specific question type
    2. Sends to Claude to get structured observations (JSON)
    3. Passes observations through deterministic scoring functions
    4. Returns a QuestionScore (same interface as score_question)
    """
    # Build observation prompt
    rubric = assemble_observation_prompt(test_code, qnum)
    filled = _fill_rubric(rubric, passage, question, response)
    tokens = 2048 if qnum == 11 else 1024
    user_msg = f"Observe question {qnum} response and report your observations.\n\n{filled}"

    # Get observations from Claude
    obs = None
    content = ""
    for attempt in range(2):
        msg = _api_call_with_retry(
            client,
            model=model,
            max_tokens=tokens,
            temperature=temperature,
            system=SYSTEM_PROMPT_OBSERVER,
            messages=[{"role": "user", "content": user_msg}],
        )
        content = extract_text(msg)
        obs = _parse_json(content)
        if obs is not None:
            break
        if attempt == 0:
            user_msg = (
                "Your previous response was not valid JSON. "
                "Respond with ONLY a JSON object, starting with { and ending with }. "
                "No other text.\n\n" + user_msg
            )
            time.sleep(0.5)

    if obs is None:
        # Observation extraction failed — fall back to zero scores
        return QuestionScore(
            question=qnum,
            ideas_score=0, ideas_max=sub_maxes(qnum, grade)[0],
            organization_score=0, organization_max=sub_maxes(qnum, grade)[1],
            conventions_score=0, conventions_max=sub_maxes(qnum, grade)[2],
            total_score=0, total_max=max_score,
            feedback=content[:500] if content else "Grading failed.",
            internal_notes="Observation JSON parse failed after 2 attempts.",
        )

    # Extract feedback before scoring (scoring doesn't produce feedback)
    feedback = obs.get("feedback", "")

    # Deterministic scoring + teacher notes based on question type
    if grade >= 6 and qnum == 11:
        scores = score_q11_essay(obs)
        teacher_notes = build_teacher_notes_q11_essay(obs, scores)
    elif qnum <= 5:
        from .rubrics.assembler import _read_test_data
        test_data = _read_test_data(test_code)
        scores = score_q1_q5(obs, test_data, qnum, grade)
        teacher_notes = build_teacher_notes_q1_q5(obs, scores, qnum)
    elif qnum <= 10:
        scores = score_q6_q10(obs, grade)
        teacher_notes = build_teacher_notes_q6_q10(obs, scores)
    else:
        scores = score_q11_paragraph(obs, grade)
        teacher_notes = build_teacher_notes_q11_paragraph(obs, scores, grade)

    # Build QuestionScore
    ideas_max, org_max, conv_max = sub_maxes(qnum, grade)
    ideas = min(scores.get("ideas_score", 0), ideas_max)
    org = min(scores.get("organization_score", 0), org_max)
    conv = min(scores.get("conventions_score", 0), conv_max)
    total = min(ideas + org + conv, max_score)

    return QuestionScore(
        question=qnum,
        ideas_score=ideas,
        ideas_max=ideas_max,
        organization_score=org,
        organization_max=org_max,
        conventions_score=conv,
        conventions_max=conv_max,
        total_score=total,
        total_max=max_score,
        feedback=feedback,
        internal_notes=scores.get("internal_notes", ""),
        teacher_notes=teacher_notes,
    )
