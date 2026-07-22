"""Data models for the grading engine."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class ConsensusMethod(str, Enum):
    UNANIMOUS = "unanimous"
    MAJORITY = "majority"
    JUDGE = "judge"
    SINGLE = "single"  # fallback / only one valid run


@dataclass
class QuestionScore:
    """Score for a single grading run of one question."""
    question: int
    ideas_score: int
    ideas_max: int
    conventions_score: int
    conventions_max: int
    total_score: int
    total_max: int
    feedback: str
    internal_notes: str = ""
    organization_score: int = 0
    organization_max: int = 0
    teacher_notes: str = ""
    # Grader's self-reported confidence in this score (0.0-1.0). 1.0 if
    # absent, so existing code that doesn't populate it doesn't break
    # callers that read it.
    confidence: float = 1.0

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> QuestionScore:
        return cls(
            question=d.get("question", 0),
            ideas_score=d.get("ideas_score", 0),
            ideas_max=d.get("ideas_max", 0),
            conventions_score=d.get("conventions_score", 0),
            conventions_max=d.get("conventions_max", 0),
            total_score=d.get("total_score", 0),
            total_max=d.get("total_max", 0),
            feedback=d.get("feedback", ""),
            internal_notes=d.get("internal_notes", ""),
            organization_score=d.get("organization_score", 0),
            organization_max=d.get("organization_max", 0),
            teacher_notes=d.get("teacher_notes", ""),
            confidence=float(d.get("confidence", 1.0)),
        )

    @classmethod
    def blank(cls, qnum: int, max_score: int, grade: int = 5) -> QuestionScore:
        ideas_max, org_max, conv_max = sub_maxes(qnum, grade)
        return cls(
            question=qnum,
            ideas_score=0, ideas_max=ideas_max,
            organization_score=0, organization_max=org_max,
            conventions_score=0, conventions_max=conv_max,
            total_score=0, total_max=max_score,
            feedback="It looks like this question was left blank. Give it a try next time — you can do it!",
            internal_notes="No response provided.",
        )

    @classmethod
    def gibberish(cls, qnum: int, max_score: int, grade: int = 5) -> QuestionScore:
        ideas_max, org_max, conv_max = sub_maxes(qnum, grade)
        return cls(
            question=qnum,
            ideas_score=0, ideas_max=ideas_max,
            organization_score=0, organization_max=org_max,
            conventions_score=0, conventions_max=conv_max,
            total_score=0, total_max=max_score,
            feedback=(
                "It looks like this response contains random or placeholder text "
                "rather than a written answer. Take your time and give it a real try — "
                "even a short, honest answer can earn points!"
            ),
            internal_notes="GIBBERISH_DETECTED: Response flagged as nonsense/random characters.",
        )


@dataclass
class ConsensusResult:
    """Final grading result for one question after consensus."""
    question: int
    final_score: QuestionScore
    consensus_method: ConsensusMethod
    runs: list[QuestionScore] = field(default_factory=list)
    judge_reasoning: str = ""

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            **self.final_score.to_dict(),
            "consensus_method": self.consensus_method.value,
            "run_count": len(self.runs),
            "runs": [r.to_dict() for r in self.runs],
            "judge_reasoning": self.judge_reasoning,
        }


@dataclass
class StudentResult:
    """Complete grading result for one student."""
    student: str
    test_code: str
    prompt_version: str
    questions: dict[str, ConsensusResult] = field(default_factory=dict)
    total_score: int = 0
    total_max: int = 0

    def compute_totals(self):
        self.total_score = sum(q.final_score.total_score for q in self.questions.values())
        self.total_max = sum(q.final_score.total_max for q in self.questions.values())

    def to_dict(self) -> dict:
        self.compute_totals()
        return {
            "student": self.student,
            "test": self.test_code,
            "prompt_version": self.prompt_version,
            "total_score": self.total_score,
            "total_max": self.total_max,
            "questions": {k: v.to_dict() for k, v in self.questions.items()},
        }


def grade_from_test_code(test_code: str) -> int:
    """Extract the grade level from a test code like 'G3.1' -> 3."""
    import re
    m = re.match(r"G(\d+)", test_code)
    return int(m.group(1)) if m else 5


def sub_maxes(qnum: int, grade: int = 5) -> tuple[int, int, int]:
    """Return (ideas_max, organization_max, conventions_max) for a question.

    G3-G5 Q11: Ideas 15 + Conventions 5 = 20 (no separate organization)
    G6-G8 Q11: Ideas 6 + Organization 8 + Conventions 6 = 20
    """
    if qnum <= 5:
        return (1, 0, 1)
    if qnum <= 10:
        return (2, 0, 1)
    # Q11
    if grade >= 6:
        return (10, 7, 3)  # G6-G8 essay: Structure(5)+Evidence(5), Org(4)+Sentences(3), Editing(3)
    return (15, 0, 5)  # G3-G5 paragraph rubric


def max_score_for(qnum: int) -> int:
    """Return the max total score for a question number."""
    if qnum <= 5:
        return 2
    if qnum <= 10:
        return 3
    return 20
