"""
HS Writing Grading API

Evaluates student free-response writing across all 4 courses (A1, A2, B1L, B2)
using Claude, then returns structured feedback.

Supports multiple scoring models:
- Criteria Checklist (Model A) -- existing, all courses
- AP Rubric (Model B) -- B1L, B2 essays
- Revision (Model F) -- B2 revision tasks

Run locally: uvicorn main:app --reload --port 8000
"""

import json
import os
import re
from contextlib import asynccontextmanager

import anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Security, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

from grading_prompts import SYSTEM_PROMPT, build_grading_prompt
from grading_rubrics import (
    RUBRICS,
    get_rubric,
    get_rubrics_for_lesson,
    get_rubrics_for_course,
    get_gateway_rubrics,
)
from ap_scorer import score_ap_essay
from consensus import grade_with_consensus
from passage_bank import get_passage, get_passage_text, list_passages
from revision_scorer import score_revision
from rubric_scorer import score_rubric_essay, RUBRIC_CONFIGS, config_max_score
from models import FRQType

load_dotenv()

CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5")  # was claude-sonnet-4-20250514 (404 dead, 2026-07-07)
GRADING_API_KEY = os.getenv("GRADING_API_KEY")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
client: anthropic.Anthropic | None = None

# API key auth — skipped when GRADING_API_KEY is not set (local dev)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(request: Request, api_key: str | None = Security(api_key_header)):
    if request.url.path.startswith("/timeback/") or request.url.path == "/score":
        return  # Timeback / ExternalApiScore call these directly WITHOUT our API key (no key support
                # in the ExternalApiScore operator) — same keyless contract as /timeback/score.
    if not GRADING_API_KEY:
        return  # No key configured = local dev, skip auth
    if api_key != GRADING_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")


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
    title="HS Writing Grading API",
    description="AI grading for free-response writing across A1, A2, B1L, B2 courses",
    version="2.0.0",
    lifespan=lifespan,
    dependencies=[Depends(verify_api_key)],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# ExternalApiScore /score endpoint for the LIVE G9-12 CCSS course (2026-27). The G9-12 analytic-trait grader
# (SBAC / Regents-4trait essay engines + grain routing + paragraph engine), ported here 2026-07-21 so the
# course + its grader deploy as one unit (this app -> hs-writing-grading service). App-wide verify_api_key
# already covers it. Engine vendored under api/grader_engine/ (Anthropic-direct; set ANTHROPIC_PROVIDER=anthropic).
from external_score import router as external_score_router  # noqa: E402
app.include_router(external_score_router)


# ===== Request / Response Models =====

class GradeRequest(BaseModel):
    rubric_id: str
    student_text: str
    passage_text: str | None = None
    passage_id: str | None = None
    lesson_id: str | None = None
    course: str | None = None


class APGradeRequest(BaseModel):
    frq_type: str | None = None  # "rhetorical_analysis" | "argument" | "synthesis" (derived from rubric if omitted)
    student_text: str
    passage_text: str | None = None
    passage_id: str | None = None
    prompt_text: str | None = None
    rubric_id: str | None = None
    course: str | None = None
    lesson_id: str | None = None
    use_consensus: bool = True


class RubricGradeRequest(BaseModel):
    """Config-driven 4-trait rubric scoring (Model C, the rc.* engine)."""
    rubric_config: str                 # rc.staar | rc.mcas | rc.ohio | rc.4trait  (rc.ap -> use /grade/ap)
    student_text: str
    mode: str | None = None            # argument | explanatory | analysis
    passage_text: str | None = None
    passage_id: str | None = None
    prompt_text: str | None = None
    grade_level: str = "Grade 10"
    use_consensus: bool = True


class RubricGradeResponse(BaseModel):
    scoring_model: str = "rubric_config"
    rubric_config: str
    mode: str | None = None
    traits: dict                       # {trait_key: {score, reasoning}}
    raw_trait_sum: int
    scorers: int
    total: int
    max_score: int
    gate_applied: bool
    feedback: str
    weakest_trait: str
    next_step: str
    consensus_method: str | None = None
    run_count: int | None = None


class RevisionGradeRequest(BaseModel):
    rubric_id: str
    original_text: str
    revised_text: str
    revision_target: str
    course: str | None = None
    lesson_id: str | None = None


class CriterionResult(BaseModel):
    id: str
    met: bool
    feedback: str


class GradeResponse(BaseModel):
    rubric_id: str
    scoring_model: str = "criteria"
    word_count: int
    word_count_met: bool
    criteria_results: list[CriterionResult]
    criteria_met: int
    criteria_total: int
    overall_feedback: str
    next_step: str


class APGradeResponse(BaseModel):
    scoring_model: str = "ap_rubric"
    rubric_id: str | None = None
    frq_type: str
    row_a: dict
    row_b: dict
    row_c: dict
    total: int
    feedback: str
    weakest_row: str
    next_step: str
    consensus_method: str | None = None
    run_count: int | None = None


class RevisionGradeResponse(BaseModel):
    scoring_model: str = "revision"
    rubric_id: str
    original_assessment: str
    revision_assessment: str
    changes_identified: list[str]
    substantive: bool
    improvement_score: int
    feedback: str
    next_step: str


class GatewayCheckResponse(BaseModel):
    passed: bool
    rubric_id: str
    score: int
    threshold: dict
    ap_result: APGradeResponse | None = None
    criteria_result: GradeResponse | None = None
    feedback: str


class TimebackScoreRequest(BaseModel):
    """Timeback QTI process-response format."""
    identifier: str
    response: str | list[str]


class TimebackScoreResponse(BaseModel):
    """Timeback QTI expected response format."""
    score: float
    feedback: dict


# ===== Helper Functions =====

def _require_client():
    if not client:
        raise HTTPException(status_code=503, detail="Anthropic API key not configured")
    return client


def _resolve_passage(passage_id: str | None, passage_text: str | None) -> str | None:
    """Resolve passage text from ID or direct text."""
    if passage_text:
        return passage_text
    if passage_id:
        text = get_passage_text(passage_id)
        if not text:
            raise HTTPException(status_code=404, detail=f"Passage '{passage_id}' not found")
        return text
    return None


def _parse_response_json(response_text: str) -> dict:
    """Parse JSON from Claude response, handling markdown fences."""
    text = response_text.strip()
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
        raise HTTPException(
            status_code=502,
            detail=f"Failed to parse grading response as JSON. Raw: {text[:500]}",
        )


def _validate_student_text(text: str) -> str:
    """Validate and clean student text."""
    text = text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Student text is empty")
    if len(text.split()) < 5:
        raise HTTPException(status_code=400, detail="Submission too short to grade (under 5 words)")
    return text


def _get_course_system_prompt(course: str | None) -> str:
    """Get the appropriate system prompt based on course."""
    if course in ("B1L", "B2"):
        grade = "Grade 11" if course == "B1L" else "Grade 12"
        return SYSTEM_PROMPT.replace("Grade 9", grade)
    if course == "A2":
        return SYSTEM_PROMPT.replace("Grade 9", "Grade 10")
    return SYSTEM_PROMPT


# ===== Endpoints =====

@app.get("/")
async def root():
    return {"status": "ok", "service": "HS Writing Grading API", "version": "2.0.0"}


# ----- Rubric Endpoints -----

@app.get("/rubrics")
async def list_rubrics(course: str | None = None):
    """List available rubrics, optionally filtered by course."""
    if course:
        rubrics = get_rubrics_for_course(course)
    else:
        rubrics = [
            {"id": k, "lesson": v["lesson"], "course": v.get("course", "A1"),
             "task_type": v["task_type"], "description": v["description"],
             "scoring_model": v.get("scoring_model", "criteria")}
            for k, v in RUBRICS.items()
        ]
    return {"rubrics": rubrics}


@app.get("/rubrics/{course}/{lesson_id}")
async def get_lesson_rubrics(course: str, lesson_id: str):
    """Get all rubrics for a specific course and lesson."""
    rubrics = get_rubrics_for_lesson(lesson_id.upper(), course.upper())
    if not rubrics:
        raise HTTPException(status_code=404, detail=f"No rubrics found for {course} {lesson_id}")
    return {"course": course.upper(), "lesson": lesson_id.upper(), "rubrics": rubrics}


@app.get("/rubrics/gateways")
async def list_gateway_rubrics(course: str | None = None):
    """List all gateway and gate rubrics."""
    rubrics = get_gateway_rubrics(course)
    return {"rubrics": rubrics}


# ----- Passage Endpoints -----

@app.get("/passages")
async def list_all_passages():
    """List available passages (metadata only)."""
    return {"passages": list_passages()}


@app.get("/passages/{passage_id}")
async def get_passage_detail(passage_id: str):
    """Get a specific passage with full text."""
    p = get_passage(passage_id.upper())
    if not p:
        raise HTTPException(status_code=404, detail=f"Passage '{passage_id}' not found")
    return p


# ----- Criteria Grading (Model A) -----

@app.post("/grade", response_model=GradeResponse)
async def grade_submission(req: GradeRequest):
    """Grade a student writing submission against a criteria rubric (Model A)."""
    c = _require_client()

    rubric = get_rubric(req.rubric_id)
    if not rubric:
        raise HTTPException(
            status_code=404,
            detail=f"Rubric '{req.rubric_id}' not found. Use GET /rubrics to see available rubrics.",
        )

    # Route AP rubric tasks to /grade/ap
    if rubric.get("scoring_model") == "ap_rubric":
        raise HTTPException(
            status_code=400,
            detail=f"Rubric '{req.rubric_id}' uses AP rubric scoring. Use POST /grade/ap instead.",
        )

    text = _validate_student_text(req.student_text)
    word_count = len(text.split())

    system_prompt = _get_course_system_prompt(req.course or rubric.get("course"))
    user_prompt = build_grading_prompt(text, rubric)

    try:
        message = c.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
    except anthropic.APIError as e:
        raise HTTPException(status_code=502, detail=f"Anthropic API error: {e}")

    result = _parse_response_json(message.content[0].text)

    return GradeResponse(
        rubric_id=req.rubric_id,
        scoring_model="criteria",
        word_count=word_count,
        word_count_met=word_count >= rubric["min_words"],
        criteria_results=[
            CriterionResult(id=cr["id"], met=cr["met"], feedback=cr["feedback"])
            for cr in result.get("criteria_results", [])
        ],
        criteria_met=result.get("criteria_met", 0),
        criteria_total=result.get("criteria_total", len(rubric["criteria"])),
        overall_feedback=result.get("overall_feedback", ""),
        next_step=result.get("next_step", ""),
    )


# ----- AP Rubric Grading (Model B) -----

@app.post("/grade/ap", response_model=APGradeResponse)
async def grade_ap_submission(req: APGradeRequest):
    """Grade an essay on the AP rubric (Row A/B/C). Uses 3-run consensus by default."""
    c = _require_client()

    text = _validate_student_text(req.student_text)

    # Resolve rubric first so we can derive frq_type if needed
    passage_text = req.passage_text
    prompt_text = req.prompt_text
    rubric = None

    if req.rubric_id:
        rubric = get_rubric(req.rubric_id)
        if rubric:
            if not passage_text and rubric.get("passage_id"):
                passage_text = _resolve_passage(rubric["passage_id"], None)
            if not prompt_text and rubric.get("prompt"):
                prompt_text = rubric["prompt"]

    # Derive frq_type from rubric task_type if not explicitly provided
    TASK_TYPE_TO_FRQ = {
        "rhetorical_analysis_essay": "rhetorical_analysis",
        "argument_essay": "argument",
        "synthesis_essay": "synthesis",
    }
    if req.frq_type:
        frq_type = FRQType(req.frq_type)
    elif rubric and rubric.get("task_type") in TASK_TYPE_TO_FRQ:
        frq_type = FRQType(TASK_TYPE_TO_FRQ[rubric["task_type"]])
    else:
        raise HTTPException(status_code=400, detail="frq_type is required when rubric_id is not provided or rubric has no task_type")

    # Resolve passage from passage_id
    if not passage_text and req.passage_id:
        passage_text = _resolve_passage(req.passage_id, None)

    course = req.course or (rubric.get("course") if rubric else None)

    score_kwargs = {
        "frq_type": frq_type,
        "student_text": text,
        "passage_text": passage_text,
        "prompt_text": prompt_text,
        "course": course,
    }

    if req.use_consensus:
        consensus = grade_with_consensus(
            client=c,
            model=CLAUDE_MODEL,
            score_fn=score_ap_essay,
            scoring_model="ap_rubric",
            num_runs=3,
            **score_kwargs,
        )
        result = consensus["final_result"]
        return APGradeResponse(
            rubric_id=req.rubric_id,
            frq_type=frq_type.value,
            row_a=result.get("row_a", {"score": 0, "reasoning": ""}),
            row_b=result.get("row_b", {"score": 0, "reasoning": ""}),
            row_c=result.get("row_c", {"score": 0, "reasoning": ""}),
            total=result.get("total", 0),
            feedback=result.get("feedback", ""),
            weakest_row=result.get("weakest_row", "B"),
            next_step=result.get("next_step", ""),
            consensus_method=consensus["consensus_method"],
            run_count=consensus["run_count"],
        )
    else:
        result = score_ap_essay(c, CLAUDE_MODEL, **score_kwargs)
        return APGradeResponse(
            rubric_id=req.rubric_id,
            frq_type=frq_type.value,
            row_a=result.get("row_a", {"score": 0, "reasoning": ""}),
            row_b=result.get("row_b", {"score": 0, "reasoning": ""}),
            row_c=result.get("row_c", {"score": 0, "reasoning": ""}),
            total=result.get("total", 0),
            feedback=result.get("feedback", ""),
            weakest_row=result.get("weakest_row", "B"),
            next_step=result.get("next_step", ""),
        )


# ----- Config-driven 4-trait Rubric Grading (Model C, the rc.* engine) -----

@app.get("/rubric-configs")
async def list_rubric_configs():
    """List the available rc.* rubric configs and their trait/scale/gate shape."""
    out = {}
    for rc_id, cfg in RUBRIC_CONFIGS.items():
        out[rc_id] = {
            "models": cfg["models"],
            "traits": [{"key": k, "label": l, "min": lo, "max": hi} for (k, l, lo, hi) in cfg["traits"]],
            "scorers": cfg.get("scorers", 1),
            "gate": cfg.get("gate"),
            "max_score": config_max_score(rc_id),
        }
    out["rc.ap"] = {"models": "AP Lang/Lit", "note": "Use POST /grade/ap (Row A/B/C + Sophistication)."}
    return {"rubric_configs": out}


@app.post("/grade/rubric", response_model=RubricGradeResponse)
async def grade_rubric_submission(req: RubricGradeRequest):
    """Grade a source-based essay on an rc.* config (STAAR/MCAS/Ohio/4-trait). 3-run consensus by default.

    This is the scorer for the G10 CR test-bank items (cr_argument / cr_explanatory / cr_analysis).
    For AP (rc.ap), use POST /grade/ap instead.
    """
    c = _require_client()

    if req.rubric_config == "rc.ap":
        raise HTTPException(status_code=400, detail="rc.ap uses AP Row A/B/C scoring. Use POST /grade/ap.")
    if req.rubric_config not in RUBRIC_CONFIGS:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown rubric_config '{req.rubric_config}'. Options: {sorted(RUBRIC_CONFIGS)} + rc.ap.",
        )

    text = _validate_student_text(req.student_text)
    passage_text = _resolve_passage(req.passage_id, req.passage_text)

    score_kwargs = {
        "rc_id": req.rubric_config,
        "student_text": text,
        "mode": req.mode,
        "passage_text": passage_text,
        "prompt_text": req.prompt_text,
        "grade_level": req.grade_level,
    }

    consensus_method = None
    run_count = None
    if req.use_consensus:
        consensus = grade_with_consensus(
            client=c, model=CLAUDE_MODEL, score_fn=score_rubric_essay,
            scoring_model="rubric_config", num_runs=3, **score_kwargs,
        )
        result = consensus["final_result"]
        consensus_method = consensus["consensus_method"]
        run_count = consensus["run_count"]
    else:
        result = score_rubric_essay(c, CLAUDE_MODEL, **score_kwargs)

    cfg = RUBRIC_CONFIGS[req.rubric_config]
    trait_keys = [k for (k, _l, _lo, _hi) in cfg["traits"]]
    traits = {k: result.get(k, {"score": 0, "reasoning": ""}) for k in trait_keys}

    return RubricGradeResponse(
        rubric_config=req.rubric_config,
        mode=req.mode,
        traits=traits,
        raw_trait_sum=result.get("raw_trait_sum", 0),
        scorers=result.get("scorers", cfg.get("scorers", 1)),
        total=result.get("total", 0),
        max_score=result.get("max_score", config_max_score(req.rubric_config)),
        gate_applied=result.get("gate_applied", False),
        feedback=result.get("feedback", ""),
        weakest_trait=result.get("weakest_trait", trait_keys[0]),
        next_step=result.get("next_step", ""),
        consensus_method=consensus_method,
        run_count=run_count,
    )


# ----- Gateway / Gate Check -----

class GatewayGradeRequest(BaseModel):
    rubric_id: str
    student_text: str
    lesson_id: str | None = None


@app.post("/grade/gateway")
async def grade_gateway(req: GatewayGradeRequest):
    """Grade a gateway or gate essay and return pass/fail determination.

    Auto-detects scoring model (criteria vs AP) from the rubric and routes accordingly.
    """
    c = _require_client()

    rubric = get_rubric(req.rubric_id)
    if not rubric:
        raise HTTPException(status_code=404, detail=f"Rubric '{req.rubric_id}' not found")

    if not rubric.get("gateway") and not rubric.get("gate"):
        raise HTTPException(status_code=400, detail=f"Rubric '{req.rubric_id}' is not a gateway or gate rubric")

    threshold = rubric.get("gateway_threshold") or rubric.get("gate_threshold", {})
    scoring_model = rubric.get("scoring_model", "criteria")

    ap_result = None
    criteria_result = None
    passed = True
    total = 0

    if scoring_model == "ap_rubric":
        # Route to AP grading
        ap_req = APGradeRequest(
            rubric_id=req.rubric_id,
            student_text=req.student_text,
            lesson_id=req.lesson_id,
            use_consensus=True,
        )
        ap_result = await grade_ap_submission(ap_req)
        total = ap_result.total

        if "min_score" in threshold:
            passed = passed and total >= threshold["min_score"]
        if "row_a" in threshold:
            passed = passed and ap_result.row_a.get("score", 0) >= threshold["row_a"]
        if "row_b" in threshold:
            passed = passed and ap_result.row_b.get("score", 0) >= threshold["row_b"]

        detail_feedback = ap_result.feedback
        score_label = f"{total}/6"
    else:
        # Route to criteria grading
        criteria_req = GradeRequest(
            rubric_id=req.rubric_id,
            student_text=req.student_text,
            lesson_id=req.lesson_id,
        )
        criteria_result = await grade_submission(criteria_req)
        total = criteria_result.criteria_met

        if "min_score" in threshold:
            passed = passed and total >= threshold["min_score"]

        detail_feedback = criteria_result.overall_feedback or ""
        score_label = f"{total}/{criteria_result.criteria_total} criteria"

    if passed:
        feedback = f"Gateway PASSED ({score_label}). {detail_feedback}"
    else:
        feedback = f"Gateway not yet passed ({score_label}, threshold: {threshold}). {detail_feedback}"

    return GatewayCheckResponse(
        passed=passed,
        rubric_id=req.rubric_id,
        score=total,
        threshold=threshold,
        ap_result=ap_result,
        criteria_result=criteria_result,
        feedback=feedback,
    )


# ----- Timeback External Grader Endpoint -----

# Mapping from QTI item identifier patterns to rubric IDs.
# When Timeback calls process-response, it sends the item identifier.
# We use this to look up which rubric to grade against.
TIMEBACK_ITEM_RUBRIC_MAP: dict[str, str] = {}

# G10 CR test-bank items (ACC-W910-CR-*) route to the config-driven rc.* engine.
# Per-item registry populated at push time: identifier -> {rubric_config, mode, passage_id}.
# Until an item is registered, we fall back to a per-family default (mode + rc.4trait) so the item
# still scores. Family is read from the ID: CR-ARG -> argument, CR-INFO -> explanatory, CR-ANLY -> analysis.
TIMEBACK_CR_REGISTRY: dict[str, dict] = {}
_CR_FAMILY_DEFAULTS = {
    "ARG": ("argument", "rc.4trait"),
    "INFO": ("explanatory", "rc.4trait"),
    "ANLY": ("analysis", "rc.4trait"),
}


def _cr_routing(identifier: str) -> dict | None:
    """Return {rubric_config, mode, passage_id} for a CR item id, or None if not a CR item."""
    if identifier in TIMEBACK_CR_REGISTRY:
        return TIMEBACK_CR_REGISTRY[identifier]
    m = re.search(r"ACC-W910-CR-([A-Z]+)-\d{4}", identifier or "")
    if m:
        mode, rc = _CR_FAMILY_DEFAULTS.get(m.group(1), ("argument", "rc.4trait"))
        return {"rubric_config": rc, "mode": mode, "passage_id": None}
    # G9-G12 course LESSON FRQs (ids like ACC-W910-L-G9-C901-0001-S07-production_frq or
    # ACC-W1112-L-G11-...). These are scored by grade band, not per-item registered: grades 9/10 use the
    # STAAR English I/II CR rubric (rc.staar, genre-agnostic Dev/Org + Conventions); grades 11/12 use the
    # AP Lang overlay (rc.ap). mode is left None (rc.staar is genre-agnostic; rc.ap defaults to argument
    # frq_type downstream). This mirrors the CR-band fallback so any pushed lesson FRQ scores without a
    # per-item registration step.
    lg = re.search(r"ACC-W\d+-L-G(\d+)", identifier or "")
    if lg:
        grade = int(lg.group(1))
        rc = "rc.ap" if grade >= 11 else "rc.staar"
        return {"rubric_config": rc, "mode": None, "passage_id": None}
    return None


@app.post("/timeback/echo")
async def timeback_echo(request: Request):
    """Debug endpoint: logs and echoes whatever Timeback sends, returns a hardcoded score."""
    body = await request.json()
    print(f"TIMEBACK ECHO received: {json.dumps(body)[:500]}")
    return {"score": 0.75, "feedback": {"identifier": "partial", "value": "Echo test successful."}}


@app.post("/timeback/score", dependencies=[])  # Override global API key auth — Timeback calls this directly
async def timeback_score(req: TimebackScoreRequest):
    """External grader endpoint for Timeback QTI integration.

    Timeback calls this when a student submits an FRQ response.
    Receives: {"identifier": "<qti-item-id>", "response": "<student text>"}
    Returns: {"score": 0.0-1.0, "feedback": {"identifier": "...", "value": "..."}}
    """
    c = _require_client()

    student_text = req.response if isinstance(req.response, str) else " ".join(req.response)
    student_text = student_text.strip()
    if not student_text:
        return {"score": 0.0, "feedback": {"identifier": "incomplete", "value": "No response provided."}}

    # G10 CR test-bank items (ACC-W910-CR-*) route to the config-driven rc.* engine.
    cr = _cr_routing(req.identifier)
    if cr:
        rc_id = cr["rubric_config"]
        if rc_id == "rc.ap":
            frq_map = {"argument": "argument", "analysis": "rhetorical_analysis", "explanatory": "argument"}
            result = score_ap_essay(c, CLAUDE_MODEL, frq_type=FRQType(frq_map.get(cr["mode"], "argument")),
                                    student_text=student_text,
                                    passage_text=_resolve_passage(cr.get("passage_id"), None))
            total, max_score = result.get("total", 0), 6
            passed = total >= 4
            feedback_text = result.get("feedback", "")
        else:
            passage_text = _resolve_passage(cr.get("passage_id"), None) if cr.get("passage_id") else None
            result = score_rubric_essay(c, CLAUDE_MODEL, rc_id=rc_id, student_text=student_text,
                                        mode=cr.get("mode"), passage_text=passage_text)
            total = result.get("total", 0)
            max_score = result.get("max_score", config_max_score(rc_id))
            passed = max_score > 0 and (total / max_score) >= 0.6
            wk = result.get("weakest_trait", "")
            feedback_text = result.get("feedback", "")
            if result.get("next_step"):
                feedback_text = f"{feedback_text}\nNext: {result['next_step']}"
            if result.get("gate_applied"):
                feedback_text += "\n(Note: the scoring gate applied because the response did not develop the idea.)"
        return {
            "score": round(total / max_score, 2) if max_score else 0.0,
            "feedback": {"identifier": "correct" if passed else "incorrect", "value": feedback_text},
        }

    # Look up rubric from the item identifier
    rubric_id = TIMEBACK_ITEM_RUBRIC_MAP.get(req.identifier)
    if not rubric_id:
        # Try to extract rubric_id from identifier pattern (e.g., "s4-L01-expository-abc123")
        # Fallback: use a default rubric for testing
        rubric_id = "L01_independent_expository"

    rubric = get_rubric(rubric_id)
    if not rubric:
        return {"score": 0.0, "feedback": {"identifier": "error", "value": f"Unknown rubric: {rubric_id}"}}

    # Check scoring model and grade accordingly
    scoring_model = rubric.get("scoring_model", "criteria")

    if scoring_model == "ap_rubric":
        # AP scoring
        from ap_scorer import score_ap_essay
        from consensus import grade_with_consensus
        try:
            result = await grade_with_consensus(c, student_text, rubric, CLAUDE_MODEL)
            total = result.get("total", 0)
            max_score = 6  # AP max
            score = min(total / max_score, 1.0)
            feedback_text = result.get("feedback", "")
            passed = total >= 4
        except Exception as e:
            return {"score": 0.0, "feedback": {"identifier": "error", "value": str(e)}}
    else:
        # Criteria scoring
        word_count = len(student_text.split())
        system_prompt = _get_course_system_prompt(rubric.get("course"))
        user_prompt = build_grading_prompt(student_text, rubric)

        try:
            message = c.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=1024,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )
        except Exception as e:
            return {"score": 0.0, "feedback": {"identifier": "error", "value": str(e)}}

        result = _parse_response_json(message.content[0].text)
        criteria_met = result.get("criteria_met", 0)
        criteria_total = result.get("criteria_total", len(rubric["criteria"]))
        score = criteria_met / criteria_total if criteria_total > 0 else 0.0
        passed = criteria_met == criteria_total

        # Build feedback string from criteria results
        feedback_parts = []
        for cr in result.get("criteria_results", []):
            icon = "PASS" if cr.get("met") else "NEEDS WORK"
            feedback_parts.append(f"[{icon}] {cr.get('id', '')}: {cr.get('feedback', '')}")
        if result.get("overall_feedback"):
            feedback_parts.append(result["overall_feedback"])
        feedback_text = "\n".join(feedback_parts)

    return {
        "score": round(score, 2),
        "feedback": {
            "identifier": "correct" if passed else "incorrect",
            "value": feedback_text,
        },
    }


# ----- Revision Grading (Model F) -----

@app.post("/grade/revision", response_model=RevisionGradeResponse)
async def grade_revision_submission(req: RevisionGradeRequest):
    """Grade a revision by comparing original and revised text."""
    c = _require_client()

    rubric = get_rubric(req.rubric_id)
    if not rubric:
        raise HTTPException(status_code=404, detail=f"Rubric '{req.rubric_id}' not found")

    original = req.original_text.strip()
    revised = req.revised_text.strip()
    if not original or not revised:
        raise HTTPException(status_code=400, detail="Both original and revised text are required")

    if original == revised:
        return RevisionGradeResponse(
            rubric_id=req.rubric_id,
            original_assessment="Original text provided.",
            revision_assessment="No changes detected.",
            changes_identified=[],
            substantive=False,
            improvement_score=0,
            feedback="The original and revised text are identical. Revision requires making changes.",
            next_step="Re-read the revision target and make at least one substantive change.",
        )

    course = req.course or rubric.get("course")
    result = score_revision(
        client=c,
        model=CLAUDE_MODEL,
        original_text=original,
        revised_text=revised,
        revision_target=req.revision_target,
        course=course,
    )

    return RevisionGradeResponse(
        rubric_id=req.rubric_id,
        original_assessment=result.get("original_assessment", ""),
        revision_assessment=result.get("revision_assessment", ""),
        changes_identified=result.get("changes_identified", []),
        substantive=result.get("substantive", False),
        improvement_score=result.get("improvement_score", 0),
        feedback=result.get("feedback", ""),
        next_step=result.get("next_step", ""),
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
