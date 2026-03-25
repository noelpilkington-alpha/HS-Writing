"""Data models for the HS Writing grading engine.

Supports multiple scoring models:
- Criteria Checklist (Model A)
- AP Rubric (Model B)
- Hybrid (Model C)
- Discrimination (Model D)
- Planning (Model E)
- Revision (Model F)
"""

from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field


class ScoringModel(str, Enum):
    CRITERIA = "criteria"
    AP_RUBRIC = "ap_rubric"
    HYBRID = "hybrid"
    DISCRIMINATION = "discrimination"
    PLANNING = "planning"
    REVISION = "revision"


class ConsensusMethod(str, Enum):
    UNANIMOUS = "unanimous"
    MAJORITY = "majority"
    JUDGE = "judge"
    SINGLE = "single"


class FRQType(str, Enum):
    RHETORICAL_ANALYSIS = "rhetorical_analysis"
    ARGUMENT = "argument"
    SYNTHESIS = "synthesis"


class SophisticationType(str, Enum):
    BROADER_CONTEXT = "broader_context"
    ALTERNATIVE = "alternative"
    TENSION = "tension"
    STYLE = "style"


# ===== Request Models =====

class GradeRequest(BaseModel):
    """Grade a student submission against a rubric (Model A/C/E)."""
    rubric_id: str
    student_text: str
    passage_text: str | None = None
    passage_id: str | None = None
    lesson_id: str | None = None
    course: str | None = None


class APGradeRequest(BaseModel):
    """Grade an essay on the AP rubric (Model B)."""
    frq_type: FRQType
    student_text: str
    passage_text: str | None = None
    passage_id: str | None = None
    prompt_text: str | None = None
    rubric_id: str | None = None
    course: str | None = None
    lesson_id: str | None = None
    use_consensus: bool = True


class RevisionGradeRequest(BaseModel):
    """Grade a revision (Model F)."""
    rubric_id: str
    original_text: str
    revised_text: str
    revision_target: str
    course: str | None = None
    lesson_id: str | None = None


# ===== Response Models =====

class CriterionResult(BaseModel):
    id: str
    met: bool
    feedback: str


class CriteriaGradeResult(BaseModel):
    """Result from Model A (Criteria Checklist)."""
    scoring_model: str = "criteria"
    rubric_id: str
    word_count: int
    word_count_met: bool
    criteria_results: list[CriterionResult]
    criteria_met: int
    criteria_total: int
    overall_feedback: str
    next_step: str
    internal_notes: str = ""

    @property
    def total_score(self) -> int:
        return self.criteria_met


class APRowScore(BaseModel):
    score: int
    reasoning: str


class APRowCScore(BaseModel):
    score: int
    sophistication_type: SophisticationType | None = None
    reasoning: str


class APGradeResult(BaseModel):
    """Result from Model B (AP Rubric)."""
    scoring_model: str = "ap_rubric"
    rubric_id: str | None = None
    frq_type: FRQType
    row_a: APRowScore
    row_b: APRowScore
    row_c: APRowCScore
    total: int = Field(ge=0, le=6)
    feedback: str
    weakest_row: str
    next_step: str
    internal_notes: str = ""

    @property
    def total_score(self) -> int:
        return self.total


class HybridGradeResult(BaseModel):
    """Result from Model C (Hybrid: Criteria + AP Preview)."""
    scoring_model: str = "hybrid"
    rubric_id: str
    word_count: int
    word_count_met: bool
    criteria_results: list[CriterionResult]
    criteria_met: int
    criteria_total: int
    overall_feedback: str
    next_step: str
    ap_preview: APGradeResult | None = None
    internal_notes: str = ""

    @property
    def total_score(self) -> int:
        return self.criteria_met


class RevisionGradeResult(BaseModel):
    """Result from Model F (Revision)."""
    scoring_model: str = "revision"
    rubric_id: str
    original_assessment: str
    revision_assessment: str
    changes_identified: list[str]
    substantive: bool
    improvement_score: int = Field(ge=0, le=3)
    feedback: str
    next_step: str
    internal_notes: str = ""

    @property
    def total_score(self) -> int:
        return self.improvement_score


class ConsensusResult(BaseModel):
    """Wrapper for any grading result that went through consensus."""
    consensus_method: ConsensusMethod
    final_result: APGradeResult | CriteriaGradeResult
    run_count: int
    runs: list[dict] = []
    judge_reasoning: str = ""


# ===== Gateway / Gate Models =====

class GatewayCheck(BaseModel):
    """Result of a gateway pass/fail check."""
    passed: bool
    rubric_id: str
    score: int
    threshold: dict
    feedback: str
