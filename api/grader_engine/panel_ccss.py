"""CCSS 4-trait analytic grader — the NY Regents 11-12 rubric family (rc.4trait).

Reuses panel.py's machinery (preflight, _run_panel, _call_rubric_grader, _call_synthesis,
_age_hint, _build_audit) UNCHANGED. The ONLY new content is the rubric: NY Regents ELA's four
co-equal analytic criteria, verbatim-grounded in the official Educator Guide (Aug 2025 rev).

Two task profiles under ONE engine (Regents scores argument on 6, analysis on 4):
  - profile "argument"  (source-based argument / synthesis / source-free argument): 4 traits x 0-6
  - profile "analysis"  (rhetorical / text analysis):                               4 traits x 0-4

The four criteria (Regents' own names):
  Content and Analysis · Command of Evidence · Coherence, Organization, and Style · Control of Conventions

This engine does DOUBLE DUTY:
  - G11/G12: the primary CCSS rubric (replaces the AP-derived rc.ap; see CCSS_G1112 sourcing spec).
  - G9/G10: a bake-off candidate ("one CCSS family across G9-12"), scored on the SAME four criteria.

Native scoring is holistic (one level per part); the anchor annotations break each level out under all
four criteria, so we score PER-CRITERION (our engine's strength) and sum. QuestionScore carries only three
sub-slots, so the full 4-trait vector is returned separately via score_panel_ccss's `traits` dict for the
bake-off harness; the QuestionScore slots hold content/evidence/coherence-folded + conventions for
pipeline compatibility.

Rubric source: english-language-arts-educator-guide-2025rev.pdf (Part 2 rubric p.14, Part 3 rubric p.15),
stored in Grading Standards Documentation/CCSS_G1112/.
"""
from __future__ import annotations

from dataclasses import dataclass

from .models import QuestionScore
from .panel import (
    RubricDimension,
    _age_hint,
    _preflight,
    _run_panel,
    _default_panel_model,
    _build_audit,
)
from .per_cat import _normalize_response_preserving_paragraphs


# ═══════════════════════════════════════════════════════════════════════════════
# INTRO (shared across profiles; scale + task filled per call)
# ═══════════════════════════════════════════════════════════════════════════════

_CCSS_INTRO = """You are an experienced writing grader scoring a Grade {grade} student's {task_desc}.

This uses the New York State Regents ELA analytic rubric (Next Generation), a Common Core Grade 11-12
writing rubric. The response is scored on FOUR co-equal criteria, each on a 0-{scale} scale (total 0-{total}):

- Content and Analysis (0-{scale})
- Command of Evidence (0-{scale})
- Coherence, Organization, and Style (0-{scale})
- Control of Conventions (0-{scale})

Score EACH criterion independently against the score-point descriptors you are given. Assign the ONE score
point whose description best fits the response for that criterion. The student is {age_hint}. Score what the
student demonstrates against the descriptors; do not import expectations the rubric does not state, and do
not withhold the top point from a response that meets the top descriptor."""


# ═══════════════════════════════════════════════════════════════════════════════
# PART 2 — ARGUMENT (6-point). Descriptors verbatim from Educator Guide p.14.
# ═══════════════════════════════════════════════════════════════════════════════

_ARG_CONTENT = """Score CONTENT AND ANALYSIS on the Regents 0-6 scale (Argument).
Measures: introducing a claim; analyzing the sources and topic; distinguishing the claim from alternate or
opposing claims (counterclaim). Assign the ONE score point whose description best fits:
- 6: sophisticated claim; insightful source and topic analysis; insightful evaluation of a counterclaim
- 5: thorough claim; thorough source and topic analysis; thorough evaluation of a counterclaim
- 4: specific claim; appropriate source and topic analysis; appropriate evaluation of a counterclaim
- 3: surface-level claim; emerging source and topic analysis; insufficient evaluation of a counterclaim
- 2: limited claim; unclear or confused source and topic analysis; confused or no counterclaim
- 1: unrelated or no claim; no source and/or topic analysis
Output evidence as short observations (quote/point to the claim, the analysis, the counterclaim handling).
Output reasoning as 1-2 sentences naming the score point chosen."""

_ARG_EVIDENCE = """Score COMMAND OF EVIDENCE on the Regents 0-6 scale (Argument).
Measures: incorporating relevant evidence from the sources; avoiding plagiarism when citing the texts.
- 6: sophisticated support using a wide range of strategically chosen, relevant evidence; consistent avoidance of plagiarism with acceptable citation
- 5: thorough and accurate support using effective and relevant evidence; consistent avoidance of plagiarism with acceptable citation
- 4: sufficient and adequate support using relevant evidence; consistent avoidance of plagiarism with acceptable citation
- 3: basic support using relevant and/or generalized evidence; partial avoidance of plagiarism with emerging citation
- 2: insufficient support using limited, inaccurate, or irrelevant evidence; insufficient avoidance of plagiarism
- 1: provides no evidence; no use of citations
NOTE: for a SOURCE-FREE argument (no sources provided), judge evidence QUALITY and RELEVANCE from the
student's own knowledge; ignore the citation/plagiarism clause (it does not apply with no sources).
Output evidence as short observations. Output reasoning as 1-2 sentences naming the score point."""

_ARG_COHERENCE = """Score COHERENCE, ORGANIZATION, AND STYLE on the Regents 0-6 scale (Argument).
Measures: maintaining focus on task; organizing ideas; optimizing language style.
- 6: strategic focus on task; strategic organization of ideas; sophisticated language and sentence structure
- 5: clear and appropriate focus; thoughtful organization; precise language and sentence structure
- 4: acceptable focus; logical organization; appropriate language and sentence structure
- 3: emerging focus; emerging organization; basic language and sentence structure
- 2: lacks appropriate focus but suggests organization, OR suggests focus but lacks organization; imprecise language
- 1: little to no focus; little to no organization; incoherent language -OR- minimal writing making assessment unreliable
Output evidence as short observations. Output reasoning as 1-2 sentences naming the score point."""

_ARG_CONVENTIONS = """Score CONTROL OF CONVENTIONS on the Regents 0-6 scale (Argument).
Measures control of 9-12 band grammar, usage, capitalization, punctuation, and spelling.
- 6: exceptional control; virtually no errors when using sophisticated language
- 5: considerable control; errors that do not hinder comprehension, even when using sophisticated language
- 4: partial control; errors that do not hinder comprehension
- 3: emerging control; errors that hinder comprehension
- 2: lack of control; errors that make comprehension difficult
- 1: significant lack of control; errors that severely interfere with comprehension -OR- minimal writing making assessment unreliable
Enumerate the notable errors you see, then choose the score point whose description best fits. Comprehension
impact (not raw error count) sets the score. Output evidence as categorized observations; reasoning as 1 sentence."""


# ═══════════════════════════════════════════════════════════════════════════════
# PART 3 — TEXT ANALYSIS (4-point). Descriptors verbatim from Educator Guide p.15.
# ═══════════════════════════════════════════════════════════════════════════════

_ANA_CONTENT = """Score CONTENT AND ANALYSIS on the Regents 0-4 scale (Text-Analysis).
Measures: establishing a central idea or theme; analyzing the author's use of a writing strategy.
- 4: thorough central idea or theme; thorough writing-strategy analysis
- 3: appropriate central idea or theme; appropriate or sufficient writing-strategy analysis
- 2: general or emerging central idea or theme; limited, surface-level writing-strategy analysis
- 1: unclear or confused central idea or theme; confused, inaccurate, or no writing-strategy analysis
Output evidence as short observations. Output reasoning as 1-2 sentences naming the score point."""

_ANA_EVIDENCE = """Score COMMAND OF EVIDENCE on the Regents 0-4 scale (Text-Analysis).
Measures: supporting analysis; linking writing-strategy evidence to the central idea or theme.
- 4: thorough support; clear link between specific and relevant evidence and the central idea or theme
- 3: sufficient support; reasonable link between adequate evidence and the central idea or theme
- 2: attempted support; emerging link between partial/inconsistent/inaccurate evidence and the idea or theme
- 1: minimal or no support; little or no evidence
Output evidence as short observations. Output reasoning as 1-2 sentences naming the score point."""

_ANA_COHERENCE = """Score COHERENCE, ORGANIZATION, AND STYLE on the Regents 0-4 scale (Text-Analysis).
Measures: maintaining focus on task; organizing ideas; optimizing language style.
- 4: clear and appropriate focus; logical organization; precise language and sound sentence structure
- 3: acceptable focus; acceptable organization; appropriate language and sentence structure
- 2: lacks focus but suggests organization, OR suggests focus but lacks organization; basic or imprecise language
- 1: little or no focus; little or no organization; predominantly incoherent or copied language -OR- minimal original writing
Output evidence as short observations. Output reasoning as 1-2 sentences naming the score point."""

_ANA_CONVENTIONS = """Score CONTROL OF CONVENTIONS on the Regents 0-4 scale (Text-Analysis).
Measures control of 9-12 band grammar, usage, capitalization, punctuation, and spelling.
- 4: considerable control; rare errors that do not hinder comprehension
- 3: partial control; errors that do not hinder comprehension
- 2: emerging control; errors that hinder comprehension
- 1: lack of control; errors that make comprehension difficult -OR- minimal original writing
Enumerate notable errors, then choose the fitting score point (comprehension impact, not raw count). Output
evidence as categorized observations; reasoning as 1 sentence."""


_PROFILES = {
    "argument": {
        "scale": 6, "task_desc": "argument essay written from sources",
        "prompts": {
            "content": _ARG_CONTENT, "evidence": _ARG_EVIDENCE,
            "coherence": _ARG_COHERENCE, "conventions": _ARG_CONVENTIONS,
        },
    },
    "analysis": {
        "scale": 4, "task_desc": "text-analysis response",
        "prompts": {
            "content": _ANA_CONTENT, "evidence": _ANA_EVIDENCE,
            "coherence": _ANA_COHERENCE, "conventions": _ANA_CONVENTIONS,
        },
    },
}

_TRAIT_NAMES = {
    "content": "Content and Analysis",
    "evidence": "Command of Evidence",
    "coherence": "Coherence, Organization, and Style",
    "conventions": "Control of Conventions",
}


_CCSS_SYNTHESIS = """Combine the panel's four criterion recommendations into final criterion scores and a
single student-facing feedback message. This is the Regents 4-criterion analytic rubric.

Apply these gates BEFORE finalizing (Regents condition rules + consistency):
1. Verbatim-copy gate: a response that is predominantly a verbatim copy of the task/sources with negligible
   student writing must be scored 0 across all criteria.
2. Off-topic gate (argument): an essay entirely unrelated to the topic / making no reference to the sources
   or task can be scored no higher than 1 on Content and Analysis.
3. Fewer-than-3-sources (argument, source-based only): if the essay uses information from fewer than 3
   sources, no criterion may exceed 3. (Do NOT apply to source-free argument or to analysis.)
4. Score-vs-evidence consistency: if a panel grader's reasoning contradicts its own score, override to match
   its enumerated evidence. Conventions is enumeration-locked: accept the conventions grader's score unless
   its listed errors plainly contradict it.

Set overridden=true + overrideReason ONLY when you adjust a criterion; else overridden=false.

Student-facing feedback: open with one specific strength tied to the response; name 1-2 concrete, rubric-
grounded improvements (prioritize Content/Evidence over Conventions); age-appropriate; 4-7 sentences; no
scores, criterion names, or rubric jargon."""


def score_panel_ccss(
    client,
    *,
    grade: int,
    passage: str,
    question: str,
    response: str,
    profile: str = "argument",
    qnum: int = 11,
    source_free: bool = False,
) -> tuple[QuestionScore, dict]:
    """Score a response on the Regents 4-trait CCSS rubric.

    profile: "argument" (0-6 each, total 24) or "analysis" (0-4 each, total 16).
    Returns (QuestionScore, traits) where traits = full 4-criterion breakdown
    {content, evidence, coherence, conventions, scale, total, total_max} for the bake-off harness.
    """
    if profile not in _PROFILES:
        raise ValueError(f"unknown profile {profile!r}; expected {list(_PROFILES)}")
    cfg = _PROFILES[profile]
    scale = cfg["scale"]
    total_max = scale * 4

    gate = _preflight(response)
    if gate == "empty":
        return QuestionScore.blank(qnum, total_max, grade), {"gate": "empty"}
    if gate == "gibberish":
        return QuestionScore.gibberish(qnum, total_max, grade), {"gate": "gibberish"}

    response = _normalize_response_preserving_paragraphs(response)
    model = _default_panel_model()
    intro = _CCSS_INTRO.format(grade=grade, age_hint=_age_hint(grade),
                               task_desc=cfg["task_desc"], scale=scale, total=total_max)

    dimensions = [
        RubricDimension(id=tid, name=_TRAIT_NAMES[tid], max_points=scale, prompt=cfg["prompts"][tid])
        for tid in ("content", "evidence", "coherence", "conventions")
    ]

    synthesis, panel_results, elapsed = _run_panel(
        client, dimensions, intro, passage, question, response, grade, model, _CCSS_SYNTHESIS)

    def pick(tid):
        pr = next((r for r in panel_results if r.id == tid), None)
        fallback = pr.score if pr else 0
        return max(0, min(scale, synthesis.category_scores.get(tid, fallback)))

    content, evidence, coherence, conventions = (pick("content"), pick("evidence"),
                                                 pick("coherence"), pick("conventions"))
    total = content + evidence + coherence + conventions

    internal_notes, teacher_notes = _build_audit(panel_results, synthesis, elapsed, qnum, grade)
    internal_notes = (f"CCSS-4trait[{profile}] " + internal_notes +
                      f" | content={content} evidence={evidence} coherence={coherence} "
                      f"conv={conventions} total={total}/{total_max}")

    traits = {
        "content": content, "evidence": evidence, "coherence": coherence,
        "conventions": conventions, "scale": scale,
        "total": total, "total_max": total_max, "profile": profile,
    }

    # QuestionScore has 3 sub-slots; fold coherence into organization slot, keep the 4-vector in `traits`.
    qs = QuestionScore(
        question=qnum,
        ideas_score=content, ideas_max=scale,
        organization_score=coherence, organization_max=scale,
        conventions_score=conventions, conventions_max=scale,
        total_score=total, total_max=total_max,
        feedback=synthesis.feedback,
        internal_notes=internal_notes, teacher_notes=teacher_notes,
    )
    return qs, traits
