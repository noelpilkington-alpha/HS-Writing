"""Generalized consensus engine for HS Writing grading.

Ported and adapted from Writing_Test_Grader's 3-run consensus logic.
Works with any scoring result that has a total_score property.

Resolution order:
1. Unanimous -- all runs agree on total_score -> pick best feedback
2. Majority  -- 2/3 agree -> use majority score, pick best feedback
3. Judge     -- all differ -> 4th Claude call reviews all runs and picks winner
"""

import json
import logging
import re
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)


def _pick_best_feedback(runs: list[dict]) -> dict:
    """From runs with the same score, pick the one with the longest feedback."""
    return max(runs, key=lambda r: len(r.get("feedback", "")))


def _parse_json(text: str) -> dict | None:
    """Try to parse JSON from API response, handling markdown fences."""
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


def _judge_call_ap(
    client,
    model: str,
    runs: list[dict],
    frq_type: str,
) -> tuple[dict, str]:
    """4th Claude call to adjudicate when all 3 AP rubric runs disagree."""
    runs_summary = []
    for i, r in enumerate(runs, 1):
        runs_summary.append(
            f"Run {i}: Row A={r.get('row_a', {}).get('score', '?')}, "
            f"Row B={r.get('row_b', {}).get('score', '?')}, "
            f"Row C={r.get('row_c', {}).get('score', '?')}, "
            f"Total={r.get('total', '?')}/6\n"
            f"  Row A reasoning: {r.get('row_a', {}).get('reasoning', '')[:200]}\n"
            f"  Row B reasoning: {r.get('row_b', {}).get('reasoning', '')[:200]}\n"
            f"  Row C reasoning: {r.get('row_c', {}).get('reasoning', '')[:200]}"
        )

    system = (
        "You are a senior AP exam reader reviewing three independent scores of the same "
        "student essay. All three gave different total scores. Review their reasoning "
        "and determine the most accurate score.\n\n"
        "Output ONLY a JSON object with these keys:\n"
        '  "chosen_run": integer (1, 2, or 3),\n'
        '  "row_a_score": 0 or 1,\n'
        '  "row_b_score": 0-4,\n'
        '  "row_c_score": 0 or 1,\n'
        '  "reasoning": string (brief explanation)\n'
    )

    user_msg = (
        f"FRQ type: {frq_type}\n\n"
        + "\n\n".join(runs_summary)
        + "\n\nWhich run is most accurate? Or provide corrected scores."
    )

    msg = client.messages.create(
        model=model,
        max_tokens=512,
        temperature=0.0,
        system=system,
        messages=[{"role": "user", "content": user_msg}],
    )

    data = _parse_json(msg.content[0].text)
    if not data:
        # Fallback: use median total score
        sorted_runs = sorted(runs, key=lambda r: r.get("total", 0))
        return sorted_runs[1], "Judge parse failed; using median."

    reasoning = data.get("reasoning", "Judge adjudication.")

    chosen = data.get("chosen_run")
    if chosen and 1 <= chosen <= 3:
        result = dict(runs[chosen - 1])
        # Override with judge scores if provided
        if "row_a_score" in data:
            result["row_a"] = {"score": min(data["row_a_score"], 1), "reasoning": result["row_a"]["reasoning"]}
            result["row_b"] = {"score": min(data["row_b_score"], 4), "reasoning": result["row_b"]["reasoning"]}
            result["row_c"] = {"score": min(data["row_c_score"], 1), "reasoning": result["row_c"]["reasoning"]}
            result["total"] = result["row_a"]["score"] + result["row_b"]["score"] + result["row_c"]["score"]
        return result, reasoning

    # Judge provided scores but no chosen_run
    if "row_a_score" in data and "row_b_score" in data and "row_c_score" in data:
        ra = min(data["row_a_score"], 1)
        rb = min(data["row_b_score"], 4)
        rc = min(data["row_c_score"], 1)
        total = ra + rb + rc
        closest = min(runs, key=lambda r: abs(r.get("total", 0) - total))
        result = dict(closest)
        result["row_a"] = {"score": ra, "reasoning": closest["row_a"]["reasoning"]}
        result["row_b"] = {"score": rb, "reasoning": closest["row_b"]["reasoning"]}
        result["row_c"] = {"score": rc, "reasoning": closest["row_c"]["reasoning"]}
        result["total"] = total
        result["feedback"] = closest.get("feedback", "")
        return result, reasoning

    # Final fallback: median
    sorted_runs = sorted(runs, key=lambda r: r.get("total", 0))
    return sorted_runs[1], f"Judge parse incomplete; using median. Raw: {msg.content[0].text[:200]}"


def _judge_call_criteria(
    client,
    model: str,
    runs: list[dict],
) -> tuple[dict, str]:
    """Judge call for criteria-based scoring disagreements."""
    runs_summary = []
    for i, r in enumerate(runs, 1):
        criteria_summary = ", ".join(
            f"{cr['id']}={'met' if cr['met'] else 'not met'}"
            for cr in r.get("criteria_results", [])
        )
        runs_summary.append(
            f"Run {i}: {r.get('criteria_met', 0)}/{r.get('criteria_total', 0)} criteria met\n"
            f"  Criteria: {criteria_summary}\n"
            f"  Feedback: {r.get('overall_feedback', '')[:200]}"
        )

    system = (
        "You are a senior grading reviewer. Three independent graders scored the same "
        "student response and all three gave different total scores. Review their reasoning "
        "and determine the most accurate result.\n\n"
        "Output ONLY a JSON object with these keys:\n"
        '  "chosen_run": integer (1, 2, or 3 — which run is most accurate),\n'
        '  "reasoning": string (brief explanation)\n'
    )

    user_msg = "\n\n".join(runs_summary) + "\n\nWhich run is most accurate?"

    msg = client.messages.create(
        model=model,
        max_tokens=512,
        temperature=0.0,
        system=system,
        messages=[{"role": "user", "content": user_msg}],
    )

    data = _parse_json(msg.content[0].text)
    if not data:
        sorted_runs = sorted(runs, key=lambda r: r.get("criteria_met", 0))
        return sorted_runs[1], "Judge parse failed; using median."

    reasoning = data.get("reasoning", "Judge adjudication.")
    chosen = data.get("chosen_run")
    if chosen and 1 <= chosen <= 3:
        return runs[chosen - 1], reasoning

    sorted_runs = sorted(runs, key=lambda r: r.get("criteria_met", 0))
    return sorted_runs[1], reasoning


def _get_total_score(result: dict, scoring_model: str) -> int:
    """Extract the total score from a grading result dict."""
    if scoring_model == "ap_rubric":
        return result.get("total", 0)
    elif scoring_model in ("criteria", "hybrid", "planning"):
        return result.get("criteria_met", 0)
    elif scoring_model == "revision":
        return result.get("improvement_score", 0)
    return 0


def grade_with_consensus(
    client,
    model: str,
    score_fn,
    scoring_model: str,
    num_runs: int = 3,
    **score_kwargs,
) -> dict:
    """Run multiple grading calls and resolve via consensus.

    Args:
        client: Anthropic client
        model: Claude model ID
        score_fn: Callable that takes (client, model, **score_kwargs) and returns a dict
        scoring_model: "ap_rubric" | "criteria" | etc.
        num_runs: Number of parallel grading runs
        **score_kwargs: Additional kwargs passed to score_fn (frq_type included for AP)

    Returns:
        dict with consensus_method, final_result, runs, judge_reasoning
    """
    frq_type = score_kwargs.get("frq_type")
    runs: list[dict] = []
    with ThreadPoolExecutor(max_workers=num_runs) as pool:
        futures = [
            pool.submit(score_fn, client, model, **score_kwargs)
            for _ in range(num_runs)
        ]
        for f in as_completed(futures):
            try:
                runs.append(f.result())
            except Exception as e:
                logger.error(f"Grading run failed: {e}")
                runs.append({"_error": str(e), "total": 0, "criteria_met": 0})

    # Filter out errors
    valid_runs = [r for r in runs if "_error" not in r]
    if not valid_runs:
        valid_runs = runs

    if len(valid_runs) == 1:
        return {
            "consensus_method": "single",
            "final_result": valid_runs[0],
            "run_count": len(runs),
            "runs": runs,
            "judge_reasoning": "",
        }

    # Check consensus on total score
    scores = [_get_total_score(r, scoring_model) for r in valid_runs]
    counts = Counter(scores)
    most_common_score, freq = counts.most_common(1)[0]

    # Unanimous
    if freq == len(valid_runs):
        best = _pick_best_feedback(valid_runs)
        return {
            "consensus_method": "unanimous",
            "final_result": best,
            "run_count": len(runs),
            "runs": runs,
            "judge_reasoning": "",
        }

    # Majority
    if freq >= 2:
        matching = [r for r in valid_runs if _get_total_score(r, scoring_model) == most_common_score]
        best = _pick_best_feedback(matching)
        return {
            "consensus_method": "majority",
            "final_result": best,
            "run_count": len(runs),
            "runs": runs,
            "judge_reasoning": "",
        }

    # All differ -- judge call
    time.sleep(0.3)
    if scoring_model == "ap_rubric":
        frq_str = frq_type.value if hasattr(frq_type, 'value') else (frq_type or "unknown")
        judge_result, reasoning = _judge_call_ap(client, model, valid_runs, frq_str)
    else:
        judge_result, reasoning = _judge_call_criteria(client, model, valid_runs)

    return {
        "consensus_method": "judge",
        "final_result": judge_result,
        "run_count": len(runs),
        "runs": runs,
        "judge_reasoning": reasoning,
    }
