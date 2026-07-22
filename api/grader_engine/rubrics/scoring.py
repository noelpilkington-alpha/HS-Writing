"""Deterministic scoring from structured observations.

Phase 2 of the modular prompt system. Claude extracts observations (what it
sees in the student's response), then these functions compute scores from rules.

This makes scoring testable, reproducible, and removes subjective variation
between runs — disagreements can only arise from different observations, not
inconsistent rule application.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Q1-Q5: Sentence Editing / Revision  (Ideas 0-1, Conventions 0-1)
# ---------------------------------------------------------------------------

def score_q1_q5(obs: dict, test_data: dict, qnum: int, grade: int) -> dict:
    """Deterministically score Q1-Q5 from observations.

    Returns dict with ideas_score, conventions_score, internal_notes.
    """
    notes = []

    # --- Ideas (0 or 1) ---
    ideas = 0
    if obs.get("is_passage_copy"):
        ideas = 0
        notes.append("Ideas 0: passage copy")
    elif not obs.get("task_skill_met"):
        ideas = 0
        notes.append("Ideas 0: task skill not met")
    else:
        # Check conjunction restriction (some Q1/Q4 tasks require specific conjunctions)
        conj_ok = True
        target = test_data.get("q_targets", {}).get(str(qnum), {})
        restriction = target.get("conjunction_restriction")
        if restriction and obs.get("conjunction_used"):
            if obs["conjunction_used"].lower() not in [c.lower() for c in restriction]:
                conj_ok = False
                notes.append(f"Ideas 0: used '{obs['conjunction_used']}' but only {restriction} accepted")

        if not conj_ok:
            ideas = 0
        elif obs.get("cj_level") in ("proficient", "advanced"):
            ideas = 1
            notes.append("Ideas 1: skill met, CJ proficient+")
        else:
            ideas = 0
            notes.append(f"Ideas 0: skill met but CJ {obs.get('cj_level', 'unknown')}")

    # --- Conventions (0 or 1) ---
    conventions = 1
    if obs.get("is_passage_copy"):
        conventions = 0
        notes.append("Conv 0: passage copy")
    elif obs.get("is_fragment") or obs.get("is_run_on") or obs.get("is_comma_splice"):
        conventions = 0
        notes.append("Conv 0: major structural error")
    elif not obs.get("starts_with_capital", True) or not obs.get("ends_with_terminal", True):
        conventions = 0
        notes.append("Conv 0: missing capitalization or terminal punctuation")
    else:
        minor_count = len(obs.get("minor_errors", []))
        tolerance = 2 if grade == 3 else 1  # G3: ≤2, G4-G5: ≤1

        if minor_count > tolerance + 1:
            # Hard boundary: more than tolerance+1 errors → deny
            conventions = 0
            notes.append(f"Conv 0: {minor_count} errors > hard boundary ({tolerance + 1})")
        elif minor_count > tolerance:
            # Soft boundary: CJ decides
            if obs.get("cj_level") in ("beginning", "developing"):
                conventions = 0
                notes.append(f"Conv 0: {minor_count} errors at soft boundary, CJ {obs.get('cj_level')}")
            else:
                conventions = 1
                notes.append(f"Conv 1: {minor_count} errors at soft boundary, CJ {obs.get('cj_level')} → allow")
        else:
            notes.append(f"Conv 1: {minor_count} errors within tolerance ({tolerance})")

    return {
        "ideas_score": ideas,
        "conventions_score": conventions,
        "internal_notes": "; ".join(notes),
    }


# ---------------------------------------------------------------------------
# Q6-Q10: One-Sentence Writing  (Ideas 0-2, Conventions 0-1)
# ---------------------------------------------------------------------------

def score_q6_q10(obs: dict, grade: int) -> dict:
    """Deterministically score Q6-Q10 from observations.

    Returns dict with ideas_score, conventions_score, internal_notes.
    """
    notes = []

    # --- Ideas (0-2) ---
    if not obs.get("is_on_topic"):
        ideas = 0
        notes.append("Ideas 0: off-topic")
    elif not obs.get("is_complete_sentence"):
        ideas = 0
        notes.append("Ideas 0: not a complete sentence")
    elif obs.get("is_circular_reasoning"):
        ideas = 1
        notes.append("Ideas 1: circular reasoning")
    elif not obs.get("has_support"):
        ideas = 1
        notes.append("Ideas 1: on-topic but no support")
    else:
        # On-topic, complete, with support
        if obs.get("cj_level") in ("proficient", "advanced"):
            ideas = 2
            notes.append("Ideas 2: complete, on-topic, supported, CJ proficient+")
        else:
            ideas = 1
            notes.append(f"Ideas 1: complete with support but CJ {obs.get('cj_level', 'unknown')}")

    # --- Conventions (0 or 1) ---
    conventions = 1
    if obs.get("is_fragment") or obs.get("is_run_on") or obs.get("is_comma_splice"):
        conventions = 0
        notes.append("Conv 0: major structural error")
    elif not obs.get("starts_with_capital", True) or not obs.get("ends_with_terminal", True):
        conventions = 0
        notes.append("Conv 0: missing capitalization or terminal punctuation")
    else:
        minor_count = len(obs.get("minor_errors", []))
        tolerance = 2 if grade == 3 else 1

        if minor_count > tolerance + 1:
            conventions = 0
            notes.append(f"Conv 0: {minor_count} errors > hard boundary ({tolerance + 1})")
        elif minor_count > tolerance:
            if obs.get("cj_level") in ("beginning", "developing"):
                conventions = 0
                notes.append(f"Conv 0: {minor_count} errors at soft boundary, CJ {obs.get('cj_level')}")
            else:
                conventions = 1
                notes.append(f"Conv 1: {minor_count} errors at soft boundary, CJ {obs.get('cj_level')} → allow")
        else:
            notes.append(f"Conv 1: {minor_count} errors within tolerance ({tolerance})")

    return {
        "ideas_score": ideas,
        "conventions_score": conventions,
        "internal_notes": "; ".join(notes),
    }


# ---------------------------------------------------------------------------
# Q11 Paragraph (G3-G5):  Ideas 0-15, Conventions 0-5
# ---------------------------------------------------------------------------

def score_q11_paragraph(obs: dict, grade: int) -> dict:
    """Deterministically score Q11 paragraph (G3-G5) from observations.

    Ideas: start at 15, deduct 2-3 per conceptual gap. Cap by classification.
    Conventions: start at 5, deduct per excess error beyond tolerance.
    """
    notes = []

    # --- Verbatim copying gate ---
    copy_pct = obs.get("verbatim_copy_percent", 0)
    ideas_cap = 15
    conv_cap = 5
    if copy_pct >= 80:
        ideas_cap = 2
        conv_cap = 1
        notes.append(f"COPYING GATE: {copy_pct}% verbatim → Ideas cap 2, Conv cap 1")
    elif copy_pct >= 50:
        ideas_cap = 6
        notes.append(f"COPYING GATE: {copy_pct}% verbatim → Ideas cap 6")

    # --- Ideas (0-15) ---
    ideas = 15

    # Deduct for conceptual gaps (2-3 points each)
    gaps = obs.get("conceptual_gaps", [])
    for gap in gaps:
        ideas -= 3  # major conceptual gap
        notes.append(f"Ideas -3: conceptual gap: {gap}")

    # Elaboration gaps are noted but NOT deducted
    elab_gaps = obs.get("elaboration_gaps", [])
    if elab_gaps:
        notes.append(f"Noted {len(elab_gaps)} elaboration gaps (no deduction)")

    # Detail sufficiency check
    details = obs.get("text_details_count", 0)
    if details < 2:
        ideas = min(ideas, 9)  # insufficient evidence
        notes.append(f"Ideas capped at 9: only {details} text details (need ≥2)")
    elif not obs.get("has_central_idea"):
        ideas = min(ideas, 6)
        notes.append("Ideas capped at 6: no clear central idea")

    # Classification cap (RETELLING vs THEME vs MIXED)
    classification = obs.get("classification", "theme")
    if classification == "retelling":
        ideas = min(ideas, 9)
        notes.append("Classification: RETELLING → cap 9/15")
    elif classification == "mixed":
        ideas = min(ideas, 12)
        notes.append("Classification: MIXED → cap 12/15")
    else:
        notes.append("Classification: THEME → full credit possible")

    # Apply copying cap
    ideas = min(max(ideas, 0), ideas_cap)

    # CJ override for borderline
    if obs.get("cj_level") == "beginning" and ideas > 6:
        ideas = min(ideas, 6)
        notes.append("CJ override: Beginning → cap 6")
    elif obs.get("cj_level") == "advanced" and ideas < 12 and ideas > 0:
        ideas = max(ideas, 12)
        notes.append("CJ override: Advanced → floor 12")

    ideas = max(ideas, 0)

    # --- Conventions (0-5) ---
    conventions = 5
    minor_count = len(obs.get("minor_errors", []))
    tolerance = 3 if grade == 3 else 2  # Q11 tolerance is higher

    excess = max(0, minor_count - tolerance)
    if excess > 0:
        conventions = max(0, conventions - excess)
        notes.append(f"Conv {conventions}/5: {minor_count} errors, tolerance {tolerance}, deducted {excess}")
    else:
        notes.append(f"Conv 5/5: {minor_count} errors within tolerance ({tolerance})")

    # Apply copying cap
    conventions = min(conventions, conv_cap)

    return {
        "ideas_score": ideas,
        "conventions_score": conventions,
        "internal_notes": "; ".join(notes),
    }


# ---------------------------------------------------------------------------
# Q11 Essay (G6-G8):  Ideas 0-6, Organization 0-8, Conventions 0-6
# ---------------------------------------------------------------------------

def score_q11_essay(obs: dict) -> dict:
    """Deterministically score Q11 essay (G6-G8) from observations.

    Alpha rubric: Structure(5) + Evidence(5) + Organization(4) + Sentences(3) + Editing(3) = 20
    Grouped into 3 JSON fields:
      ideas_score      = Structure(0-5) + Evidence(0-5)   = max 10
      organization_score = Organization(0-4) + Sentences(0-3) = max 7
      conventions_score  = Editing(0-3)                    = max 3
    """
    notes = []

    # --- Verbatim copying gate ---
    copy_pct = obs.get("verbatim_copy_percent", 0)
    ideas_cap = 10
    org_cap = 7
    conv_cap = 3
    if copy_pct >= 80:
        ideas_cap = 2
        org_cap = 1
        conv_cap = 1
        notes.append(f"COPYING GATE: {copy_pct}% verbatim → caps 2/10, 1/7, 1/3")
    elif copy_pct >= 50:
        ideas_cap = 5
        org_cap = 4
        notes.append(f"COPYING GATE: {copy_pct}% verbatim → Ideas cap 5/10, Org cap 4/7")

    # --- Structure (0-5) ---
    para_count = obs.get("paragraph_count", 0)
    has_purpose = obs.get("paragraphs_have_distinct_purpose", False)
    if para_count >= 5 and has_purpose:
        structure = 5
    elif para_count == 4 and has_purpose:
        structure = 4
    elif para_count >= 5:
        structure = 4  # five paragraphs but one underdeveloped
    elif para_count >= 3:
        structure = 3
    elif para_count >= 2:
        structure = 2
    elif para_count == 1:
        structure = 1
    else:
        structure = 0
    notes.append(f"Structure {structure}/5: {para_count} paragraphs")

    # --- Evidence & Explanation (0-5) ---
    # Thesis (0-1)
    thesis_q = obs.get("thesis_quality", "missing")
    thesis = 1 if thesis_q == "clear" else 0
    notes.append(f"Thesis {thesis}/1: {thesis_q}")

    # Evidence (0-2)
    ev_count = obs.get("evidence_count", 0)
    if ev_count >= 3:
        evidence = 2
    elif ev_count >= 1:
        evidence = 1
    else:
        evidence = 0
    notes.append(f"Evidence {evidence}/2: {ev_count} details")

    # Analysis (0-2)
    analysis_q = obs.get("analysis_quality", "no_connection")
    if analysis_q == "explains_how_why":
        analysis = 2
    elif analysis_q == "mostly_summary":
        analysis = 1
    else:
        analysis = 0
    notes.append(f"Analysis {analysis}/2: {analysis_q}")

    evidence_total = thesis + evidence + analysis
    notes.append(f"Evidence & Explanation {evidence_total}/5")

    ideas = min(structure + evidence_total, ideas_cap)

    # --- Organization (0-4) ---
    # Transitions (0-2)
    trans_q = obs.get("transitions_quality", "none")
    if trans_q == "smooth":
        transitions = 2
    elif trans_q == "inconsistent":
        transitions = 1
    else:
        transitions = 0
    notes.append(f"Transitions {transitions}/2: {trans_q}")

    # Intro & Conclusion (0-2)
    ic_q = obs.get("intro_conclusion_quality", "both_missing")
    if ic_q == "both_strong":
        intro_conc = 2
    elif ic_q == "one_weak":
        intro_conc = 1
    else:
        intro_conc = 0
    notes.append(f"Intro/Conc {intro_conc}/2: {ic_q}")

    org_subtotal = transitions + intro_conc

    # --- Sentence Quality (0-3) ---
    sent_variety = obs.get("sentence_variety", "mixed")
    sent_clarity = obs.get("sentence_clarity", "clear")
    sent_register = obs.get("sentence_register", "formal")

    variety_score = 1 if sent_variety == "mixed" else 0
    clarity_score = 1 if sent_clarity == "clear" else 0
    register_score = 1 if sent_register == "formal" else 0
    sentences = variety_score + clarity_score + register_score
    notes.append(f"Sentences {sentences}/3: variety={sent_variety}, clarity={sent_clarity}, register={sent_register}")

    organization = min(org_subtotal + sentences, org_cap)

    # --- Editing (0-3) ---
    # Grammar (0-1)
    grammar_errs = len(obs.get("grammar_errors", []))
    grammar = 1 if grammar_errs == 0 else 0
    notes.append(f"Grammar {grammar}/1: {grammar_errs} errors")

    # Spelling (0-1)
    spelling_errs = len(obs.get("spelling_errors", []))
    spelling = 1 if spelling_errs <= 1 else 0
    notes.append(f"Spelling {spelling}/1: {spelling_errs} errors")

    # Punctuation (0-1)
    punct_errs = len(obs.get("punctuation_errors", []))
    punctuation = 1 if punct_errs == 0 else 0
    notes.append(f"Punctuation {punctuation}/1: {punct_errs} errors")

    conventions = min(grammar + spelling + punctuation, conv_cap)

    return {
        "ideas_score": ideas,
        "organization_score": organization,
        "conventions_score": conventions,
        "internal_notes": "; ".join(notes),
    }


# ---------------------------------------------------------------------------
# Teacher notes generation
# ---------------------------------------------------------------------------

def build_teacher_notes_q1_q5(obs: dict, scores: dict, qnum: int) -> str:
    """Build teacher-facing score breakdown for Q1-Q5."""
    lines = []
    ideas = scores["ideas_score"]
    conv = scores["conventions_score"]

    # Ideas line
    if obs.get("is_passage_copy"):
        lines.append(f"Ideas {ideas}/1: Student copied the passage without performing the task.")
    elif not obs.get("task_skill_met"):
        lines.append(f"Ideas {ideas}/1: Task skill not demonstrated.")
    else:
        conj = obs.get("conjunction_used")
        conj_note = f' (used "{conj}")' if conj else ""
        lines.append(f"Ideas {ideas}/1: Task skill {'met' if ideas else 'attempted but below proficient'}{conj_note}.")

    # Conventions line
    errors = obs.get("minor_errors", [])
    if obs.get("is_fragment"):
        lines.append(f"Conv {conv}/1: Sentence fragment.")
    elif obs.get("is_run_on"):
        lines.append(f"Conv {conv}/1: Run-on sentence.")
    elif obs.get("is_comma_splice"):
        lines.append(f"Conv {conv}/1: Comma splice.")
    elif not obs.get("starts_with_capital", True):
        lines.append(f"Conv {conv}/1: Missing initial capital letter.")
    elif not obs.get("ends_with_terminal", True):
        lines.append(f"Conv {conv}/1: Missing terminal punctuation.")
    elif errors:
        lines.append(f"Conv {conv}/1: {len(errors)} minor error(s): {'; '.join(errors[:3])}.")
    else:
        lines.append(f"Conv {conv}/1: No errors.")

    return "\n".join(lines)


def build_teacher_notes_q6_q10(obs: dict, scores: dict) -> str:
    """Build teacher-facing score breakdown for Q6-Q10."""
    lines = []
    ideas = scores["ideas_score"]
    conv = scores["conventions_score"]

    # Ideas line
    if not obs.get("is_on_topic"):
        lines.append(f"Ideas {ideas}/2: Off-topic response.")
    elif not obs.get("is_complete_sentence"):
        lines.append(f"Ideas {ideas}/2: Not a complete sentence.")
    elif obs.get("is_circular_reasoning"):
        lines.append(f"Ideas {ideas}/2: On-topic but circular reasoning — restates the question without adding new information.")
    elif not obs.get("has_support"):
        lines.append(f"Ideas {ideas}/2: On-topic sentence but no supporting reason, explanation, or example.")
    elif ideas == 2:
        lines.append(f"Ideas {ideas}/2: Complete, on-topic sentence with support.")
    else:
        lines.append(f"Ideas {ideas}/2: On-topic with support but below proficient level.")

    # Conventions line
    errors = obs.get("minor_errors", [])
    if obs.get("is_fragment"):
        lines.append(f"Conv {conv}/1: Sentence fragment.")
    elif obs.get("is_run_on"):
        lines.append(f"Conv {conv}/1: Run-on sentence.")
    elif obs.get("is_comma_splice"):
        lines.append(f"Conv {conv}/1: Comma splice.")
    elif errors:
        lines.append(f"Conv {conv}/1: {len(errors)} minor error(s): {'; '.join(errors[:3])}.")
    else:
        lines.append(f"Conv {conv}/1: No errors.")

    return "\n".join(lines)


def build_teacher_notes_q11_paragraph(obs: dict, scores: dict, grade: int) -> str:
    """Build teacher-facing score breakdown for Q11 paragraph (G3-G5)."""
    lines = []
    ideas = scores["ideas_score"]
    conv = scores["conventions_score"]

    # Copying gate
    copy_pct = obs.get("verbatim_copy_percent", 0)
    if copy_pct >= 50:
        lines.append(f"⚠ Copying: ~{copy_pct}% verbatim from passage.")

    # Ideas breakdown
    classification = obs.get("classification", "theme")
    details = obs.get("text_details_count", 0)
    gaps = obs.get("conceptual_gaps", [])

    parts = [f"Ideas {ideas}/15"]
    parts.append(f"{classification.title()} response")
    parts.append(f"{details} text-based detail(s)")
    if gaps:
        parts.append(f"{len(gaps)} conceptual gap(s)")
    lines.append(": ".join([parts[0], ", ".join(parts[1:])]) + ".")

    # List specific gaps
    for gap in gaps:
        lines.append(f"  - Gap: {gap}")

    # Conventions breakdown
    errors = obs.get("minor_errors", [])
    tolerance = 3 if grade == 3 else 2
    excess = max(0, len(errors) - tolerance)
    if errors:
        lines.append(f"Conv {conv}/5: {len(errors)} error(s) (tolerance {tolerance}, {excess} excess).")
        for err in errors[:5]:
            lines.append(f"  - {err}")
    else:
        lines.append(f"Conv {conv}/5: No errors.")

    return "\n".join(lines)


def build_teacher_notes_q11_essay(obs: dict, scores: dict) -> str:
    """Build teacher-facing score breakdown for Q11 essay (G6-G8)."""
    lines = []
    ideas = scores["ideas_score"]
    org = scores["organization_score"]
    conv = scores["conventions_score"]

    # Copying gate
    copy_pct = obs.get("verbatim_copy_percent", 0)
    if copy_pct >= 50:
        lines.append(f"⚠ Copying: ~{copy_pct}% verbatim from passage.")

    # Structure + Evidence (ideas_score = max 10)
    para_count = obs.get("paragraph_count", 0)
    thesis_q = obs.get("thesis_quality", "missing")
    ev_count = obs.get("evidence_count", 0)
    analysis_q = obs.get("analysis_quality", "no_connection")
    analysis_labels = {
        "explains_how_why": "explains how/why",
        "mostly_summary": "mostly summary",
        "no_connection": "no connection to thesis",
    }
    lines.append(
        f"Content {ideas}/10: {para_count} paragraph(s), "
        f"thesis {thesis_q}, "
        f"{ev_count} evidence detail(s), "
        f"analysis {analysis_labels.get(analysis_q, analysis_q)}."
    )

    # Organization + Sentences (organization_score = max 7)
    trans_q = obs.get("transitions_quality", "none")
    ic_q = obs.get("intro_conclusion_quality", "both_missing")
    ic_labels = {
        "both_strong": "intro & conclusion strong",
        "one_weak": "one weak or missing",
        "both_missing": "both missing or ineffective",
    }
    sent_variety = obs.get("sentence_variety", "unknown")
    sent_clarity = obs.get("sentence_clarity", "unknown")
    lines.append(
        f"Org+Sentences {org}/7: transitions {trans_q}, "
        f"{ic_labels.get(ic_q, ic_q)}, "
        f"variety {sent_variety}, clarity {sent_clarity}."
    )

    # Editing (conventions_score = max 3)
    grammar = obs.get("grammar_errors", [])
    spelling = obs.get("spelling_errors", [])
    punctuation = obs.get("punctuation_errors", [])
    all_errors = grammar + spelling + punctuation
    if all_errors:
        lines.append(
            f"Editing {conv}/3: {len(grammar)} grammar, "
            f"{len(spelling)} spelling, "
            f"{len(punctuation)} punctuation error(s)."
        )
        for err in all_errors[:5]:
            lines.append(f"  - {err}")
    else:
        lines.append(f"Editing {conv}/3: No errors.")

    return "\n".join(lines)


def build_teacher_notes_from_scores(score, internal_notes: str = "") -> str:
    """Build teacher notes from an existing QuestionScore (non-observation mode).

    Uses the score breakdown + internal_notes from Claude to produce a
    teacher-readable summary.
    """
    lines = []
    qnum = score.question if hasattr(score, "question") else score.get("question", 0)
    is_essay = score.organization_max > 0 if hasattr(score, "organization_max") else score.get("organization_max", 0) > 0

    if hasattr(score, "ideas_score"):
        ideas_s, ideas_m = score.ideas_score, score.ideas_max
        conv_s, conv_m = score.conventions_score, score.conventions_max
    else:
        ideas_s = score.get("ideas_score", 0)
        ideas_m = score.get("ideas_max", 0)
        conv_s = score.get("conventions_score", 0)
        conv_m = score.get("conventions_max", 0)

    if is_essay:
        org_s = score.organization_score if hasattr(score, "organization_score") else score.get("organization_score", 0)
        org_m = score.organization_max if hasattr(score, "organization_max") else score.get("organization_max", 0)
        lines.append(f"Ideas {ideas_s}/{ideas_m}, Org {org_s}/{org_m}, Conv {conv_s}/{conv_m}")
    else:
        lines.append(f"Ideas {ideas_s}/{ideas_m}, Conv {conv_s}/{conv_m}")

    if internal_notes:
        lines.append(internal_notes)

    return "\n".join(lines)
