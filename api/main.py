"""
A1 Course Grading API

Evaluates student free-response writing against lesson-specific rubrics
using Claude, then returns structured feedback following best-practice
principles (wise feedback, specific criteria, one next step).

Run locally: uvicorn main:app --reload --port 8000
"""

import json
import os
from contextlib import asynccontextmanager

import anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from grading_prompts import SYSTEM_PROMPT, build_grading_prompt
from grading_rubrics import RUBRICS, get_rubric, get_rubrics_for_lesson

load_dotenv()

client: anthropic.Anthropic | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global client
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("WARNING: ANTHROPIC_API_KEY not set. Grading will fail.")
    else:
        client = anthropic.Anthropic(api_key=api_key)
        print("Anthropic client initialized.")
    yield


app = FastAPI(
    title="A1 Course Grading API",
    description="AI grading for free-response writing tasks in the A1 writing course",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow lesson HTML files to call this API from any origin (GitHub Pages, localhost, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


# ===== Request / Response Models =====

class GradeRequest(BaseModel):
    rubric_id: str  # e.g., "L01_independent_expository"
    student_text: str
    lesson_id: str | None = None  # optional, for logging


class CriterionResult(BaseModel):
    id: str
    met: bool
    feedback: str


class GradeResponse(BaseModel):
    rubric_id: str
    word_count: int
    word_count_met: bool
    criteria_results: list[CriterionResult]
    criteria_met: int
    criteria_total: int
    overall_feedback: str
    next_step: str


# ===== Endpoints =====

@app.get("/")
async def root():
    return {"status": "ok", "service": "A1 Course Grading API"}


@app.get("/rubrics")
async def list_rubrics():
    """List all available rubric IDs."""
    return {
        "rubrics": [
            {"id": k, "lesson": v["lesson"], "task_type": v["task_type"], "description": v["description"]}
            for k, v in RUBRICS.items()
        ]
    }


@app.get("/rubrics/{lesson_id}")
async def get_lesson_rubrics(lesson_id: str):
    """Get all rubrics for a specific lesson."""
    rubrics = get_rubrics_for_lesson(lesson_id.upper())
    if not rubrics:
        raise HTTPException(status_code=404, detail=f"No rubrics found for lesson {lesson_id}")
    return {"lesson": lesson_id.upper(), "rubrics": rubrics}


@app.post("/grade", response_model=GradeResponse)
async def grade_submission(req: GradeRequest):
    """Grade a student writing submission against a rubric."""

    if not client:
        raise HTTPException(status_code=503, detail="Anthropic API key not configured")

    rubric = get_rubric(req.rubric_id)
    if not rubric:
        raise HTTPException(
            status_code=404,
            detail=f"Rubric '{req.rubric_id}' not found. Use GET /rubrics to see available rubrics.",
        )

    # Basic validation
    text = req.student_text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Student text is empty")

    word_count = len(text.split())
    if word_count < 5:
        raise HTTPException(status_code=400, detail="Submission too short to grade (under 5 words)")

    # Build prompt and call Claude
    user_prompt = build_grading_prompt(text, rubric)

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )
    except anthropic.APIError as e:
        raise HTTPException(status_code=502, detail=f"Anthropic API error: {e}")

    # Parse response
    response_text = message.content[0].text.strip()

    # Extract JSON from response (handle markdown code blocks)
    if response_text.startswith("```"):
        lines = response_text.split("\n")
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
        response_text = "\n".join(json_lines)

    try:
        result = json.loads(response_text)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to parse grading response as JSON. Raw: {response_text[:500]}",
        )

    return GradeResponse(
        rubric_id=req.rubric_id,
        word_count=result.get("word_count", word_count),
        word_count_met=result.get("word_count_met", word_count >= rubric["min_words"]),
        criteria_results=[
            CriterionResult(
                id=cr["id"],
                met=cr["met"],
                feedback=cr["feedback"],
            )
            for cr in result.get("criteria_results", [])
        ],
        criteria_met=result.get("criteria_met", 0),
        criteria_total=result.get("criteria_total", len(rubric["criteria"])),
        overall_feedback=result.get("overall_feedback", ""),
        next_step=result.get("next_step", ""),
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
