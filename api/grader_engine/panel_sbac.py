"""Smarter Balanced (SBAC) 3-trait full-write grader (rc.sbac) — a CCSS consortium rubric.

Reuses panel.py's machinery (preflight, _run_panel, _call_rubric_grader, _call_synthesis, _age_hint,
_build_audit) UNCHANGED. The ONLY new content is the rubric: SBAC's Performance Task full-write, three
traits, verbatim-grounded in the official rubric PDFs (Updated Aug 2022):
  Organization/Purpose 0-4 + Evidence/Elaboration 0-4 + Conventions 0-2 = 10.

Two purpose profiles (SBAC ships separate rubrics per purpose; narrative is 3-8 only, excluded):
  - profile "argumentative" (grades 6-11)
  - profile "explanatory"   (grades 6-11)

This is a G9/G10 bake-off candidate: SBAC is Common-Core-native and its 3-trait split (structure/purpose
vs evidence/elaboration vs standalone conventions) is a finer CCSS fit than STAAR's blended Development 0-3.
Bands 6-11, so grades 9/10 use these descriptors directly (a grade-7 gate turns on opposing-argument
handling, which is active at 9/10).

Descriptors are COMPACT paraphrases + key distinguishing phrases from the official ladders (the functional
scoring criteria); full source PDFs in Grading Standards Documentation/CCSS_G910/ (sbac_pt_rubric_*.pdf).
Conventions is scored holistically on Variety / Severity / Density per the SBAC Conventions rubric.
"""
from __future__ import annotations

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
from .panel_joey import check1_insufficient_text  # validated near-blank/stub floor


_SBAC_INTRO = """You are an experienced writing grader scoring a Grade {grade} student's {task_desc}.

This uses the Smarter Balanced (SBAC) Performance Task full-write rubric, a Common Core writing rubric for
grades 6-11. The response is scored on THREE traits (total 0-10):

- Organization/Purpose (0-4)
- Evidence/Elaboration (0-4)
- Conventions (0-2)

Score EACH trait independently against its score-point descriptors. Assign the ONE score point whose
description best fits. The student is {age_hint}. Score what the student demonstrates; the source material is
provided so you can judge whether evidence is integrated and relevant."""


# ═══════════════════════════════════════════════════════════════════════════════
# ARGUMENTATIVE (grades 6-11). Source: sbac_pt_rubric_argumentative_6-11.pdf
# ═══════════════════════════════════════════════════════════════════════════════

_ARG_ORG = """Score ORGANIZATION/PURPOSE on the SBAC 0-4 scale (Argumentative).
Judges organizational structure, sustained focus, claim, transitions, intro/conclusion, and whether
opposing arguments are acknowledged/addressed (this is expected at grades 7-11).
- 4: "clear and effective organizational structure"; claim "fully sustained"; "consistent use of a variety
  of transitional strategies"; opposing arguments "clearly acknowledged or addressed"
- 3: "evident organizational structure and a sense of completeness"; "adequately sustained"; "adequate use
  of transitional strategies with some variety"; opposing arguments "adequately acknowledged"
- 2: "inconsistent organizational structure"; "somewhat sustained"; "inconsistent use of transitional
  strategies"; intro/conclusion "may be weak"; opposing arguments "confusing or not acknowledged"
- 1: "little or no discernible organizational structure"; "few or no transitional strategies"; intro/
  conclusion "may be missing"; ideas "randomly ordered"
- 0 / NS: insufficient (incl. copied text), off-topic, off-purpose, or in a language other than English
Output evidence as short observations. Output reasoning as 1-2 sentences naming the score point."""

_ARG_EVID = """Score EVIDENCE/ELABORATION on the SBAC 0-4 scale (Argumentative).
Judges support/evidence for the claim, integration of source material, citations, elaborative techniques,
and vocabulary.
- 4: "thorough and convincing elaboration"; "reasoned, in-depth analysis"; "comprehensive evidence ...
  integrated, relevant, and specific"; "clear citations"; "effective use of a variety of elaborative
  techniques"; "precise language"
- 3: "adequate elaboration"; "reasoned analysis"; evidence "integrated and relevant, yet may be general";
  "adequate use of citations"; vocabulary "generally appropriate"
- 2: "uneven, cursory elaboration"; "some reasoned analysis"; evidence "weakly integrated, imprecise,
  repetitive"; "weak use of citations"; may "rely on emotional appeal" or source summary
- 1: "minimal elaboration"; evidence "minimal, irrelevant, absent, incorrectly used, or predominantly
  copied"; "insufficient use of citations"; vocabulary "limited or ineffective"
- 0 / NS: insufficient/copied, off-topic, off-purpose, non-English
Output evidence as short observations. Output reasoning as 1-2 sentences naming the score point."""

_EXP_ORG = """Score ORGANIZATION/PURPOSE on the SBAC 0-4 scale (Explanatory).
Same structure as the argumentative ladder but keyed to a "thesis/controlling idea" (NOT a claim), and with
NO opposing-argument requirement.
- 4: "clear and effective organizational structure"; controlling idea "fully sustained"; "consistent use of
  a variety of transitional strategies"; effective intro/conclusion
- 3: "evident organizational structure and a sense of completeness"; "adequately sustained"; "adequate use
  of transitional strategies with some variety"
- 2: "inconsistent organizational structure"; "somewhat sustained"; "inconsistent use of transitional
  strategies"; intro/conclusion "may be weak"
- 1: "little or no discernible organizational structure"; "few or no transitional strategies"; intro/
  conclusion "may be missing"; ideas "randomly ordered"
- 0 / NS: insufficient/copied, off-topic, off-purpose, non-English
Output evidence as short observations. Output reasoning as 1-2 sentences naming the score point."""

_EXP_EVID = """Score EVIDENCE/ELABORATION on the SBAC 0-4 scale (Explanatory).
Same ladder as argumentative, keyed to the controlling idea, but WITHOUT "reasoned analysis" or "emotional
appeal" language; elaborative techniques may include relevant personal experiences that support the idea.
- 4: "thorough" elaboration; "comprehensive evidence ... integrated, relevant, and specific"; "clear
  citations"; "effective use of a variety of elaborative techniques"; "precise language"
- 3: "adequate elaboration"; evidence "integrated and relevant, yet may be general"; "adequate use of
  citations"; vocabulary "generally appropriate"
- 2: "uneven, cursory elaboration"; evidence "weakly integrated, imprecise, repetitive"; "weak use of
  citations"; may rely on source summary
- 1: "minimal elaboration"; evidence "minimal, irrelevant, absent, incorrectly used, or predominantly
  copied"; "insufficient use of citations"; vocabulary "limited or ineffective"
- 0 / NS: insufficient/copied, off-topic, off-purpose, non-English
Output evidence as short observations. Output reasoning as 1-2 sentences naming the score point."""

# Conventions is identical across both purposes (SBAC ships one Conventions rubric).
_SBAC_CONVENTIONS = """Score CONVENTIONS on the SBAC 0-2 scale.
Scored HOLISTICALLY on three factors: Variety (range of error types across sentence formation, punctuation,
capitalization, grammar usage, spelling), Severity (basic errors weigh more than higher-level errors), and
Density (proportion of errors to the amount of writing done well, relative to length).
- 2: "adequate command of conventions" — errors are minor relative to the length/complexity; a range of
  correct sentence formation, punctuation, capitalization, grammar usage, and spelling
- 1: "partial command" — an accumulation of errors OR limited/simple correct use that does not vary
- 0: "little or no command" — infrequent correct use; errors are frequent/severe/dense relative to length
Enumerate the notable errors you see (by type), weigh Variety/Severity/Density, then choose the score point.
Output evidence as categorized observations; reasoning as 1 sentence stating the Variety/Severity/Density call."""


_PROFILES = {
    "argumentative": {
        "task_desc": "argument essay written from sources",
        "prompts": {"org": _ARG_ORG, "evidence": _ARG_EVID, "conventions": _SBAC_CONVENTIONS},
    },
    "explanatory": {
        "task_desc": "explanatory/informational essay written from sources",
        "prompts": {"org": _EXP_ORG, "evidence": _EXP_EVID, "conventions": _SBAC_CONVENTIONS},
    },
}

_TRAIT_NAMES = {
    "org": "Organization/Purpose",
    "evidence": "Evidence/Elaboration",
    "conventions": "Conventions",
}
_MAXES = {"org": 4, "evidence": 4, "conventions": 2}


_SBAC_SYNTHESIS = """Combine the panel's three trait recommendations into final scores and a single
student-facing feedback message. This is the SBAC 3-trait full-write rubric (Org/Purpose 0-4 +
Evidence/Elaboration 0-4 + Conventions 0-2 = 10).

★ STEP 0 — NON-SCORABLE (NS) CHECK. Do this FIRST, before any trait scoring. SBAC assigns a "condition
code" (NS) that scores the WHOLE response 0 — this is not a low score, it is a gate. Fire NS -> 0/0/0 when
ANY of these is true. Judge against the TASK/PROMPT shown to you, not just the topic:
  (a) OFF-PURPOSE: the response is about the right TOPIC but does NOT do the task's PURPOSE. On an
      ARGUMENTATIVE task it must take and defend a position/claim; a piece that only describes/explains/
      reports facts (no claim, no argument) is OFF-PURPOSE -> NS. On an EXPLANATORY task it must explain/
      analyze the specific question asked; a piece that just lists facts about the general topic WITHOUT
      addressing the task's specific explanatory question is OFF-PURPOSE -> NS. (Example: an explanatory
      task asks the student to explain a stated relationship, and the response is a fluent encyclopedia-
      style description of the subject that never addresses that relationship -> OFF-PURPOSE -> NS, even if
      it is well written and on-topic.)
  (b) OFF-TOPIC: unrelated to the source/topic.
  (c) INSUFFICIENT: too little writing to constitute a full-write attempt (e.g. a single sentence, or a
      few words), OR predominantly a verbatim copy of the sources with negligible original writing.
  (d) Not in English.
If NS fires, set all three traits to 0, feedback = a brief, kind redirect telling the student what the task
actually asked for, and reasoning = which NS condition fired + why. A high panel score does NOT override an
NS condition — the panel graders scored fluency/structure and can miss that the piece never did the task.

If NOT NS, score normally:
1. Score-vs-evidence consistency: if a trait grader's reasoning contradicts its own score, override to match
   the enumerated evidence. Conventions is enumeration-locked: accept its Variety/Severity/Density call
   unless the listed errors plainly contradict the score.
2. Do NOT let a weak Organization/Purpose drag down Evidence/Elaboration or vice versa; they are independent.

Set overridden=true + overrideReason ONLY when you adjust a trait (NS counts as an override on all three);
else overridden=false.

Student-facing feedback: open with one specific strength; name 1-2 concrete, rubric-grounded improvements
(prioritize Organization/Purpose + Evidence over Conventions); age-appropriate; 4-7 sentences; no scores,
trait names, or rubric jargon."""


def score_panel_sbac(
    client,
    *,
    grade: int,
    passage: str,
    question: str,
    response: str,
    profile: str = "argumentative",
    qnum: int = 11,
) -> tuple[QuestionScore, dict]:
    """Score a full-write on the SBAC 3-trait rubric (total 0-10).

    profile: "argumentative" or "explanatory".
    Returns (QuestionScore, traits) where traits = {org, evidence, conventions, total, total_max, profile}.
    """
    if profile not in _PROFILES:
        raise ValueError(f"unknown profile {profile!r}; expected {list(_PROFILES)}")
    cfg = _PROFILES[profile]
    total_max = 10

    gate = _preflight(response)
    if gate == "empty":
        return QuestionScore.blank(qnum, total_max, grade), {"gate": "empty"}
    if gate == "gibberish":
        return QuestionScore.gibberish(qnum, total_max, grade), {"gate": "gibberish"}

    # Deterministic INSUFFICIENT-TEXT floor (defense-in-depth for NS condition (c)): a near-blank stub
    # or a fragment with no complete sentence is non-scorable -> 0. Reuses the validated panel_joey rule
    # (<22 words or no complete sentence; >=40 words never floors, so it will NOT mis-fire on a real short
    # attempt). The semantic OFF-PURPOSE case (fluent, long, wrong task) is caught by the synthesis Step-0
    # NS gate, which needs the prompt; this floor only catches the mechanical stub case.
    if check1_insufficient_text(response):
        qs = QuestionScore(
            question=qnum, ideas_score=0, ideas_max=4,
            organization_score=0, organization_max=4,
            conventions_score=0, conventions_max=2,
            total_score=0, total_max=total_max,
            feedback=("It looks like this is too short to score as a full essay yet. Give it a real try — "
                      "state your position (or main idea) and back it up with details from the sources."),
            internal_notes=f"SBAC-3trait[{profile}] NS: insufficient_text floor (deterministic) -> 0/10",
        )
        return qs, {"org": 0, "evidence": 0, "conventions": 0, "total": 0,
                    "total_max": total_max, "profile": profile, "gate": "insufficient_text"}

    response = _normalize_response_preserving_paragraphs(response)
    model = _default_panel_model()
    intro = _SBAC_INTRO.format(grade=grade, age_hint=_age_hint(grade), task_desc=cfg["task_desc"])

    dimensions = [
        RubricDimension(id=tid, name=_TRAIT_NAMES[tid], max_points=_MAXES[tid], prompt=cfg["prompts"][tid])
        for tid in ("org", "evidence", "conventions")
    ]

    synthesis, panel_results, elapsed = _run_panel(
        client, dimensions, intro, passage, question, response, grade, model, _SBAC_SYNTHESIS)

    def pick(tid):
        pr = next((r for r in panel_results if r.id == tid), None)
        fallback = pr.score if pr else 0
        return max(0, min(_MAXES[tid], synthesis.category_scores.get(tid, fallback)))

    org, evidence, conventions = pick("org"), pick("evidence"), pick("conventions")
    total = org + evidence + conventions

    internal_notes, teacher_notes = _build_audit(panel_results, synthesis, elapsed, qnum, grade)
    internal_notes = (f"SBAC-3trait[{profile}] " + internal_notes +
                      f" | org={org} evidence={evidence} conv={conventions} total={total}/10")

    traits = {
        "org": org, "evidence": evidence, "conventions": conventions,
        "total": total, "total_max": total_max, "profile": profile,
    }

    qs = QuestionScore(
        question=qnum,
        ideas_score=org, ideas_max=4,
        organization_score=evidence, organization_max=4,
        conventions_score=conventions, conventions_max=2,
        total_score=total, total_max=total_max,
        feedback=synthesis.feedback,
        internal_notes=internal_notes, teacher_notes=teacher_notes,
    )
    return qs, traits
