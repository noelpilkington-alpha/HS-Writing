"""
Course Review Agent (Option A): Content Review

Reads each lesson's HTML source, extracts instructional content,
sends it to Claude for pedagogical evaluation, and generates a
structured report.

Usage:
  python course_review_agent.py                  # Review all 20 lessons
  python course_review_agent.py L01 L05 L10      # Review specific lessons
  python course_review_agent.py --unit 1          # Review all lessons in a unit

Output: course_review_report.md in the project root
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()

# ===== Config =====
LESSONS_DIR = Path(__file__).parent.parent / "Generated_Content" / "Lessons_HTML"
OUTPUT_FILE = Path(__file__).parent.parent / "course_review_report.md"

UNIT_MAP = {
    1: ["L01", "L02", "L03", "L04", "L05"],
    2: ["L06", "L07"],
    3: ["L08", "L09", "L10"],
    4: ["L11", "L12", "L13"],
    5: ["L14", "L15", "L16"],
    6: ["L17", "L18", "L19"],
    7: ["L20"],
}

LESSON_FILES = {
    "L01": "A1_L01_From_Expository_to_Argumentative.html",
    "L02": "A1_L02_Taking_a_Position.html",
    "L03": "A1_L03_Evidence_and_Reasoning.html",
    "L04": "A1_L04_Counterarguments.html",
    "L05": "A1_L05_Argument_Essay.html",
    "L06": "A1_L06_You_Already_Make_Choices.html",
    "L07": "A1_L07_Close_Reading_Protocol.html",
    "L08": "A1_L08_Structure_Function_Effect.html",
    "L09": "A1_L09_Analysis_vs_Summary.html",
    "L10": "A1_L10_SFE_Fluency_Drill.html",
    "L11": "A1_L11_Thesis_Development.html",
    "L12": "A1_L12_Essay_Structures.html",
    "L13": "A1_L13_Architecture_and_Evidence.html",
    "L14": "A1_L14_Body_Paragraph_Sprint.html",
    "L15": "A1_L15_Analysis_vs_Summary_Calibration.html",
    "L16": "A1_L16_Three_Pass_Revision.html",
    "L17": "A1_L17_Style_and_Sentences.html",
    "L18": "A1_L18_Pre_Gate_Practice.html",
    "L19": "A1_L19_Voice_and_Revision.html",
    "L20": "A1_L20_Gate_Assessment.html",
}

# ===== Content extraction =====

def extract_content(html: str) -> str:
    """Strip JS/CSS and extract instructional content from lesson HTML."""
    # Remove style blocks
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL)
    # Remove script blocks
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
    # Keep data attributes (they contain rubric IDs, correct answers, etc.)
    # Convert HTML to readable text while preserving structure
    # Replace block elements with newlines
    html = re.sub(r"<(h[1-6])[^>]*>", r"\n### ", html)
    html = re.sub(r"</(h[1-6])>", "\n", html)
    html = re.sub(r"<p[^>]*>", "\n", html)
    html = re.sub(r"</p>", "\n", html)
    html = re.sub(r"<br\s*/?>", "\n", html)
    html = re.sub(r"<li[^>]*>", "\n- ", html)
    html = re.sub(r"<tr[^>]*>", "\n| ", html)
    html = re.sub(r"<t[dh][^>]*>", " | ", html)
    # Preserve data attributes as annotations
    html = re.sub(r'data-correct="([^"]*)"', r'[CORRECT: \1]', html)
    html = re.sub(r'data-rubric="([^"]*)"', r'[RUBRIC: \1]', html)
    html = re.sub(r'data-phase="([^"]*)"', r'[PHASE: \1]', html)
    # Remove remaining tags
    html = re.sub(r"<[^>]+>", "", html)
    # Clean up whitespace
    html = re.sub(r"\n{3,}", "\n\n", html)
    html = re.sub(r"[ \t]+", " ", html)
    # Decode HTML entities
    html = html.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    html = html.replace("&quot;", '"').replace("&#39;", "'").replace("&rsquo;", "'")
    html = html.replace("&ldquo;", '"').replace("&rdquo;", '"')
    html = html.replace("&mdash;", "—").replace("&ndash;", "–")
    html = html.replace("&nbsp;", " ")
    return html.strip()


# ===== Review prompt =====

SYSTEM_PROMPT = """You are a senior instructional designer reviewing a Grade 9 writing course lesson. You have deep expertise in:
- SRSD (Self-Regulated Strategy Development) lesson design
- Writing pedagogy (Graham, Harris, MacArthur)
- Wise feedback principles (Yeager)
- Discrimination-before-production sequencing
- Coping modeling (showing false starts and self-correction)
- 4:2:1 ratio (plans:paragraphs:essays)

You are reviewing for QUALITY, not just correctness. Be specific. Quote from the lesson when pointing to issues.

For each criterion, give a score of 1-4:
  1 = Major issue that would confuse or mislead students
  2 = Needs revision — unclear, missing, or pedagogically weak
  3 = Solid — meets expectations with minor suggestions
  4 = Excellent — exemplary instructional design

Be honest. A course full of 4s is suspicious. Find what needs fixing."""


def build_review_prompt(lesson_id: str, content: str) -> str:
    return f"""Review this lesson from the A1 Grade 9 Writing Course.

LESSON: {lesson_id}

LESSON CONTENT:
---
{content[:20000]}
---

Evaluate on these 8 criteria:

1. **INSTRUCTIONAL CLARITY** (1-4): Are instructions clear enough for a Grade 9 student working independently (no teacher)? Any ambiguous directions? Any jargon without definition?

2. **SRSD FIDELITY** (1-4): Does the lesson follow the SRSD shell? Teach → Model → Supported Practice → Independent Practice → Transfer Bridge. Is each phase clearly delineated? Does the Model phase use coping modeling (false starts, self-correction)?

3. **CONTENT ACCURACY** (1-4): Are model texts, examples, and answer keys correct? Any factual errors? Do MCQ correct answers actually match the instruction? Any contradictions?

4. **PROGRESSION & SCAFFOLDING** (1-4): Does difficulty increase appropriately within the lesson? Does supported practice scaffold before removing support in independent practice? Is the cognitive load manageable?

5. **ENGAGEMENT & RELEVANCE** (1-4): Are topics and examples engaging for Grade 9 students? Are prompts interesting enough to motivate genuine writing? Would a 14-year-old want to do this?

6. **WRITING TASK QUALITY** (1-4): Are writing prompts clear about what to produce? Do they specify genre, audience, length? Do they match the KCs being taught? Is there enough guidance without being prescriptive?

7. **ASSESSMENT ALIGNMENT** (1-4): Do practice items and writing tasks actually assess the knowledge components being taught? Could a student pass by gaming the system without learning? Are MCQ distractors plausible?

8. **TRANSFER & CONNECTION** (1-4): Does the lesson connect to prior learning and preview future lessons? Does the transfer bridge prompt genuine reflection, not just a generic "think about it" question?

For each criterion, provide:
- Score (1-4)
- 1-2 sentence justification (quote from the lesson when relevant)
- Specific fix if score < 4

Then provide:
- **OVERALL SCORE**: Average of all 8 criteria (to 1 decimal)
- **TOP ISSUE**: The single most important thing to fix in this lesson
- **BRIGHT SPOT**: The single best element of this lesson

Respond in this JSON format:
{{
  "lesson_id": "{lesson_id}",
  "criteria": [
    {{"name": "Instructional Clarity", "score": <1-4>, "justification": "...", "fix": "..." or null}},
    {{"name": "SRSD Fidelity", "score": <1-4>, "justification": "...", "fix": "..." or null}},
    {{"name": "Content Accuracy", "score": <1-4>, "justification": "...", "fix": "..." or null}},
    {{"name": "Progression & Scaffolding", "score": <1-4>, "justification": "...", "fix": "..." or null}},
    {{"name": "Engagement & Relevance", "score": <1-4>, "justification": "...", "fix": "..." or null}},
    {{"name": "Writing Task Quality", "score": <1-4>, "justification": "...", "fix": "..." or null}},
    {{"name": "Assessment Alignment", "score": <1-4>, "justification": "...", "fix": "..." or null}},
    {{"name": "Transfer & Connection", "score": <1-4>, "justification": "...", "fix": "..." or null}}
  ],
  "overall_score": <float>,
  "top_issue": "...",
  "bright_spot": "..."
}}"""


# ===== Run reviews =====

def review_lesson(client: anthropic.Anthropic, lesson_id: str) -> dict:
    """Review a single lesson and return structured results."""
    filename = LESSON_FILES.get(lesson_id)
    if not filename:
        return {"lesson_id": lesson_id, "error": f"Unknown lesson ID: {lesson_id}"}

    filepath = LESSONS_DIR / filename
    if not filepath.exists():
        return {"lesson_id": lesson_id, "error": f"File not found: {filepath}"}

    print(f"  Reading {filename}...")
    html = filepath.read_text(encoding="utf-8")
    content = extract_content(html)

    print(f"  Sending to Claude for review ({len(content)} chars)...")
    prompt = build_review_prompt(lesson_id, content)

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
    except anthropic.APIError as e:
        return {"lesson_id": lesson_id, "error": f"API error: {e}"}

    response_text = message.content[0].text.strip()

    # Extract JSON
    if "```" in response_text:
        match = re.search(r"```(?:json)?\s*\n(.*?)\n```", response_text, re.DOTALL)
        if match:
            response_text = match.group(1)

    try:
        result = json.loads(response_text)
    except json.JSONDecodeError:
        return {"lesson_id": lesson_id, "error": f"Failed to parse response", "raw": response_text[:500]}

    return result


def generate_report(results: list[dict]) -> str:
    """Generate a markdown report from review results."""
    lines = [
        "# A1 Course Review Report",
        f"*Generated: {time.strftime('%Y-%m-%d %H:%M')}*",
        f"*Lessons reviewed: {len(results)}*",
        "",
    ]

    # Summary table
    lines.append("## Summary")
    lines.append("")
    lines.append("| Lesson | Overall | Clarity | SRSD | Accuracy | Progression | Engagement | Writing | Assessment | Transfer | Top Issue |")
    lines.append("|--------|---------|---------|------|----------|-------------|------------|---------|------------|----------|-----------|")

    all_scores = []
    for r in results:
        if "error" in r:
            lines.append(f"| {r['lesson_id']} | ERROR | — | — | — | — | — | — | — | — | {r['error'][:40]} |")
            continue

        scores = [c["score"] for c in r["criteria"]]
        overall = r.get("overall_score", sum(scores) / len(scores))
        all_scores.append(overall)
        score_cells = " | ".join(str(s) for s in scores)
        top_issue = r.get("top_issue", "—")[:50]
        lines.append(f"| {r['lesson_id']} | {overall:.1f} | {score_cells} | {top_issue} |")

    if all_scores:
        avg = sum(all_scores) / len(all_scores)
        lines.append(f"| **AVG** | **{avg:.1f}** | | | | | | | | | |")

    lines.append("")

    # Detailed results per lesson
    lines.append("## Detailed Reviews")
    lines.append("")

    for r in results:
        lines.append(f"### {r['lesson_id']}")
        lines.append("")

        if "error" in r:
            lines.append(f"**Error:** {r['error']}")
            if "raw" in r:
                lines.append(f"\nRaw response:\n```\n{r['raw']}\n```")
            lines.append("")
            continue

        for c in r["criteria"]:
            score = c["score"]
            icon = {1: "!!!", 2: "!!", 3: "OK", 4: "+++"}[score]
            lines.append(f"**{c['name']}**: {score}/4 [{icon}]")
            lines.append(f"  {c['justification']}")
            if c.get("fix"):
                lines.append(f"  *Fix: {c['fix']}*")
            lines.append("")

        lines.append(f"**Overall: {r.get('overall_score', 0):.1f}/4**")
        lines.append(f"**Top Issue:** {r.get('top_issue', '—')}")
        lines.append(f"**Bright Spot:** {r.get('bright_spot', '—')}")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Aggregate issues
    lines.append("## Issues by Priority")
    lines.append("")
    issues = []
    for r in results:
        if "error" in r:
            continue
        for c in r["criteria"]:
            if c["score"] <= 2 and c.get("fix"):
                issues.append((c["score"], r["lesson_id"], c["name"], c["fix"]))

    issues.sort(key=lambda x: x[0])
    if issues:
        for score, lid, name, fix in issues:
            icon = "CRITICAL" if score == 1 else "NEEDS WORK"
            lines.append(f"- **[{icon}] {lid} — {name}**: {fix}")
    else:
        lines.append("No critical or major issues found.")

    lines.append("")
    return "\n".join(lines)


# ===== CLI =====

def main():
    parser = argparse.ArgumentParser(description="Review A1 course lessons with Claude")
    parser.add_argument("lessons", nargs="*", help="Specific lesson IDs (e.g., L01 L05)")
    parser.add_argument("--unit", type=int, help="Review all lessons in a unit (1-7)")
    parser.add_argument("--all", action="store_true", help="Review all 20 lessons")
    parser.add_argument("--output", type=str, default=str(OUTPUT_FILE), help="Output file path")
    args = parser.parse_args()

    # Determine which lessons to review
    if args.unit:
        lesson_ids = UNIT_MAP.get(args.unit, [])
        if not lesson_ids:
            print(f"Unknown unit: {args.unit}. Valid: 1-7")
            sys.exit(1)
    elif args.lessons:
        lesson_ids = [lid.upper() for lid in args.lessons]
    elif args.all:
        lesson_ids = list(LESSON_FILES.keys())
    else:
        # Default: review all
        lesson_ids = list(LESSON_FILES.keys())

    print(f"Reviewing {len(lesson_ids)} lessons: {', '.join(lesson_ids)}")
    print()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set in .env")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    results = []

    for i, lid in enumerate(lesson_ids, 1):
        print(f"[{i}/{len(lesson_ids)}] Reviewing {lid}...")
        result = review_lesson(client, lid)
        results.append(result)

        if "error" not in result:
            score = result.get("overall_score", 0)
            top = result.get("top_issue", "—")
            print(f"  Score: {score:.1f}/4 | Top issue: {top[:60]}")
        else:
            print(f"  ERROR: {result['error']}")
        print()

        # Small delay to avoid rate limits
        if i < len(lesson_ids):
            time.sleep(1)

    # Generate report
    report = generate_report(results)
    output_path = Path(args.output)
    output_path.write_text(report, encoding="utf-8")
    print(f"Report saved to: {output_path}")

    # Print summary
    scores = [r.get("overall_score", 0) for r in results if "error" not in r]
    if scores:
        print(f"\nOverall average: {sum(scores)/len(scores):.1f}/4")
        lowest = min(results, key=lambda r: r.get("overall_score", 99) if "error" not in r else 99)
        if "error" not in lowest:
            print(f"Lowest scoring: {lowest['lesson_id']} ({lowest.get('overall_score', 0):.1f}/4)")


if __name__ == "__main__":
    main()
