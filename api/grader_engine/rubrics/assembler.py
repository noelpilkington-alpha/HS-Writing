"""Prompt assembler — builds per-question prompts from modules + test data.

Usage:
    from grader.engine.rubrics.assembler import assemble_prompt

    prompt = assemble_prompt("G4.5", qnum=3)
    # Returns a string with {{passage}}, {{question}}, {{response}} placeholders
"""

import json
import re
from functools import lru_cache
from pathlib import Path

RUBRICS_DIR = Path(__file__).resolve().parent
MODULES_DIR = RUBRICS_DIR / "modules"
RUBRIC_DIR = RUBRICS_DIR / "rubric"
PROTOCOL_DIR = RUBRICS_DIR / "protocol"
EXAMPLES_DIR = RUBRICS_DIR / "examples"
TEST_DATA_DIR = RUBRICS_DIR / "test_data"

# Feature flag: use the new three-layer (rubric/protocol/examples) structure
# for Q11 assembly. Falls back to legacy modules/ when False or when the
# new files are missing.
#
# Evidence-based default (set 2026-04-24 from three_way_ab_fast_20260424_095112.json):
# G6-G8 essay:      NEW-FULL improves mean |Δ| by 29% vs legacy (n=35). USE IT.
# G3-G5 paragraph:  NEW-FULL and legacy are statistically tied (n=18, mean |Δ|
#                   1.79 vs 1.73 after excluding parse failures). NEW-FULL has
#                   more parse failures (4 vs 3) and 3x prompt cost. USE LEGACY.
import os
USE_NEW_Q11_STRUCTURE = os.environ.get("ALPHA_USE_NEW_Q11", "1") == "1"

# Band-specific override: the G3-G5 paragraph rubric is already well-calibrated
# in the legacy module, so defaulting off. Set ALPHA_USE_NEW_Q11_PARAGRAPH=1 to
# override and use the new structure for G3-G5 paragraphs too.
USE_NEW_Q11_PARAGRAPH = os.environ.get("ALPHA_USE_NEW_Q11_PARAGRAPH", "0") == "1"

# Secondary flag: when using the new structure, include calibration examples
# alongside the rubric + protocol. Set to False to isolate the effect of the
# examples layer for A/B testing.
INCLUDE_Q11_EXAMPLES = os.environ.get("ALPHA_INCLUDE_Q11_EXAMPLES", "1") == "1"


@lru_cache(maxsize=32)
def _read_module(name: str) -> str:
    """Read a shared module file by name."""
    path = MODULES_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Module not found: {path}")
    return path.read_text(encoding="utf-8").strip()


@lru_cache(maxsize=16)
def _read_rubric(name: str) -> str:
    """Read a clean rubric file (score-point descriptors only)."""
    path = RUBRIC_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Rubric not found: {path}")
    return path.read_text(encoding="utf-8").strip()


@lru_cache(maxsize=16)
def _read_protocol(name: str) -> str:
    """Read a scoring protocol file (gates, thresholds, enumeration rules)."""
    path = PROTOCOL_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Protocol not found: {path}")
    return path.read_text(encoding="utf-8").strip()


@lru_cache(maxsize=1)
def _read_paragraph_examples() -> str:
    """Read all paragraph example files, concatenated with section headers."""
    examples_root = EXAMPLES_DIR / "paragraph"
    if not examples_root.exists():
        return ""
    parts = [
        "════════════════════════════════════════════════════════",
        "CALIBRATION EXAMPLES — Q11 PARAGRAPH  (G3-G5)",
        "════════════════════════════════════════════════════════",
        "",
        "Real student responses at each Ideas & Organization band, graded",
        "using the protocol above. Each example cites the specific protocol",
        "sections that justify its score. Use these as anchors when placing",
        "a new response into a band.",
        "",
    ]
    # Read files in sorted order; README first (if present), then band_* files
    files = sorted(examples_root.glob("*.md"), key=lambda p: (p.stem != "README", p.stem))
    for f in files:
        parts.append("")
        parts.append(f.read_text(encoding="utf-8").strip())
    return "\n".join(parts)


@lru_cache(maxsize=1)
def _read_essay_examples() -> str:
    """Read all essay example files, concatenated with section headers."""
    examples_root = EXAMPLES_DIR / "essay"
    if not examples_root.exists():
        return ""
    parts = [
        "════════════════════════════════════════════════════════",
        "CALIBRATION EXAMPLES — Q11 ESSAY  (G6-G8)",
        "════════════════════════════════════════════════════════",
        "",
        "Real student essays at representative total-score points, graded",
        "using the protocol above. Each example cites the specific protocol",
        "sections that justify each category score. Use these as anchors",
        "when placing a new essay.",
        "",
    ]
    files = sorted(examples_root.glob("*.md"), key=lambda p: (p.stem != "README", p.stem))
    for f in files:
        parts.append("")
        parts.append(f.read_text(encoding="utf-8").strip())
    return "\n".join(parts)


def _assemble_q11_paragraph_threelayer(test_data: dict) -> str:
    """Assemble Q11 paragraph prompt from the new rubric/protocol/examples structure.

    Returns the concatenated rubric + protocol + examples + test-specific section.
    Placeholders ({q11_purpose}, {classification_guidance}) are filled in as in
    the legacy path.
    """
    rubric = _read_rubric("q11_paragraph.txt")
    protocol = _read_protocol("q11_paragraph_protocol.txt")
    examples = _read_paragraph_examples() if INCLUDE_Q11_EXAMPLES else ""

    # Fill Q11-specific placeholders from test data into the rubric if present
    q11 = test_data.get("q11", {})
    if "{q11_purpose}" in rubric:
        rubric = rubric.replace("{q11_purpose}", q11.get("topic", ""))
    if "{classification_guidance}" in rubric:
        rubric = rubric.replace(
            "{classification_guidance}",
            _render_classification_guidance(test_data),
        )
    # Same for protocol (in case it ever grows placeholders)
    if "{q11_purpose}" in protocol:
        protocol = protocol.replace("{q11_purpose}", q11.get("topic", ""))

    sections = [rubric, protocol]
    if examples:
        sections.append(examples)
    return "\n\n".join(sections)


def _assemble_q11_essay_threelayer() -> str:
    """Assemble Q11 essay prompt from the new rubric/protocol/examples structure."""
    rubric = _read_rubric("q11_essay.txt")
    protocol = _read_protocol("q11_essay_protocol.txt")
    examples = _read_essay_examples() if INCLUDE_Q11_EXAMPLES else ""

    sections = [rubric, protocol]
    if examples:
        sections.append(examples)
    return "\n\n".join(sections)


def _q11_new_structure_available(qnum: int, grade: int) -> bool:
    """Check whether the new three-layer Q11 files exist."""
    if qnum != 11:
        return False
    if grade >= 6:
        return (
            (RUBRIC_DIR / "q11_essay.txt").exists()
            and (PROTOCOL_DIR / "q11_essay_protocol.txt").exists()
        )
    return (
        (RUBRIC_DIR / "q11_paragraph.txt").exists()
        and (PROTOCOL_DIR / "q11_paragraph_protocol.txt").exists()
    )


@lru_cache(maxsize=64)
def _read_test_data(test_code: str) -> dict:
    """Read test-specific JSON data."""
    path = TEST_DATA_DIR / f"{test_code}.json"
    if not path.exists():
        raise FileNotFoundError(f"Test data not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _grade_from_code(test_code: str) -> int:
    """Extract grade level from test code like 'G4.5' -> 4."""
    m = re.match(r"G(\d+)", test_code)
    return int(m.group(1)) if m else 5


def _render_q1_q5_targets(test_data: dict, qnum: int) -> str:
    """Render the test-specific target skill section for a Q1-Q5 question."""
    q_targets = test_data.get("q_targets", {})
    target = q_targets.get(str(qnum))
    if not target:
        return ""

    lines = []
    lines.append("════════════════════════════════════════════════════════")
    lines.append("TEST-SPECIFIC TARGET SKILL")
    lines.append("════════════════════════════════════════════════════════")
    lines.append("")

    skill = target.get("skill", "")
    desc = target.get("description", "")
    lines.append(f"Q{qnum} — {desc}")

    # Conjunction restrictions
    conj = target.get("conjunction_restriction")
    if conj:
        conj_str = ", ".join(f'"{c}"' for c in conj)
        lines.append(f"  🔒 CONJUNCTION RESTRICTION: ONLY {conj_str} accepted.")
        rejected = [c for c in ["and", "but", "so", "or", "because", "since", "although", "however"]
                     if c not in conj]
        if rejected:
            lines.append(f"  X Do NOT accept: {', '.join(rejected)}.")
        lines.append(f"  X Score Ideas 0/1 if a conjunction other than {conj_str} is used.")

    # Target sentences
    targets = target.get("targets", [])
    if targets and len(targets) == 2:
        lines.append(f'  Target sentences: "{targets[0]}" + "{targets[1]}"')

    # Fragment
    fragment = target.get("fragment")
    if fragment:
        lines.append(f'  Target fragment: "{fragment}"')

    # Original sentence (for interrogative)
    orig = target.get("original_sentence")
    if orig:
        lines.append(f'  Original sentence: "{orig}"')

    # Example
    example = target.get("example")
    if example:
        lines.append(f'  Example: "{example}"')

    # Task-type-specific guidance from JSON
    task_type = target.get("task_type", "")
    if task_type == "fill_in_blank":
        accepted = target.get("accepted_answers", [])
        lines.append("")
        lines.append("  ⚠️ FILL-IN-THE-BLANK: The student only needs to supply a SINGLE WORD")
        lines.append("  (or short phrase). A one-word response is the EXPECTED format.")
        if accepted:
            accepted_str = ", ".join(f'"{a}"' for a in accepted)
            lines.append(f"  Accepted answers (all earn full Ideas credit): {accepted_str}")
        lines.append("  Any word that produces a grammatical, logical sentence earns Ideas 1/1.")
    elif task_type == "expand":
        lines.append("")
        lines.append("  ⚠️ EXPAND TASK: Ideas 1/1 if the student added at least one meaningful")
        lines.append("  detail and the sentence is complete. Do NOT penalize for adding extra detail.")
    elif task_type == "complete_sentence":
        lines.append("")
        lines.append("  ⚠️ SENTENCE COMPLETION: Ideas 1/1 if the student completes the sentence")
        lines.append("  grammatically and logically. Accept any reasonable completion.")

    return "\n".join(lines)


def _render_q11_details(test_data: dict, grade: int) -> str:
    """Render the test-specific Q11 section."""
    q11 = test_data.get("q11", {})
    if not q11:
        return ""

    lines = []
    lines.append("════════════════════════════════════════════════════════")
    lines.append("TEST-SPECIFIC DETAILS")
    lines.append("════════════════════════════════════════════════════════")
    lines.append("")

    title = test_data.get("title", "")
    test_code = test_data.get("test_code", "")
    lines.append(f"Test: {test_code} — {title}")
    lines.append("")

    topic = q11.get("topic", "")
    if topic:
        lines.append(f"Q11 Task: {topic}")

    article_title = q11.get("article_title")
    if article_title:
        lines.append(f"Article: {article_title}")

    # Passage summary (for G6-G8)
    summary = q11.get("passage_summary")
    if summary:
        lines.append(f"Passage Summary: {summary}")

    # Essay prompt (for G6-G8)
    essay_prompt = q11.get("essay_prompt")
    if essay_prompt:
        lines.append(f"Essay Prompt: {essay_prompt}")

    # Student requirements (for G6-G8)
    requirements = q11.get("student_requirements")
    if requirements:
        lines.append("")
        lines.append("Student Requirements:")
        for req in requirements:
            lines.append(f"  - {req}")

    # Key evidence
    evidence = q11.get("key_evidence", [])
    if evidence:
        lines.append("")
        lines.append("Key Text-Based Evidence Available:")
        for e in evidence:
            lines.append(f"  - {e}")

    # Paraphrasing example
    para_ex = q11.get("paraphrasing_example")
    if para_ex:
        lines.append("")
        lines.append("Paraphrasing example (for copying gate):")
        lines.append(f'  COPYING: Student reproduces passage sentences in order with near-identical wording.')
        lines.append(f'  PARAPHRASING: Passage says "{para_ex.get("passage", "")}" -> student writes "{para_ex.get("student", "")}"')

    return "\n".join(lines)


def _render_classification_guidance(test_data: dict) -> str:
    """Render RETELLING/THEME/MIXED classification guidance for Q11."""
    q11 = test_data.get("q11", {})
    classification = q11.get("classification", {})
    if not classification:
        return ""

    lines = []
    lines.append("CRITICAL DISTINCTION — Retelling vs. Theme:")

    retelling = classification.get("retelling", "")
    theme = classification.get("theme", "")
    mixed = classification.get("mixed", "")

    if retelling:
        lines.append(f"  RETELLING (Ideas 7-9/15): {retelling}")
        lines.append(f"  ⚠️ A retelling with 2+ identifiable passage details = 9 minimum (see 9 vs 11 rule).")
    if theme:
        lines.append(f"  THEME-BASED (Ideas 12-15/15): {theme}")
    if mixed:
        lines.append(f"  MIXED (Ideas 10-12/15): {mixed}")

    return "\n".join(lines)


def _render_json_output_block(qnum: int, grade: int) -> str:
    """Render the machine-readable JSON output instruction block.

    Appended to a per-question prompt so it's self-contained for a single
    Claude API call — returns both a numeric score AND student feedback
    in one response, no matter what system prompt the caller uses.

    Score maxes by question type:
      Q1-Q5  (editing):        Ideas 1 + Conv 1 = 2
      Q6-Q10 (sentence write): Ideas 2 + Conv 1 = 3
      Q11 G3-G5 (paragraph):   Ideas 15 + Conv 5 = 20
      Q11 G6-G8 (essay):       Ideas 10 + Org 7 + Conv 3 = 20
    """
    if qnum <= 5:
        ideas_max, org_max, conv_max, total_max = 1, 0, 1, 2
        org_line = ""
        org_max_line = ""
    elif qnum <= 10:
        ideas_max, org_max, conv_max, total_max = 2, 0, 1, 3
        org_line = ""
        org_max_line = ""
    elif grade >= 6:
        # G6-G8 Q11 essay
        ideas_max, org_max, conv_max, total_max = 10, 7, 3, 20
        org_line = '  "organization_score": <integer 0-7 (Organization 0-4 + Sentences 0-3)>,\n'
        org_max_line = '  "organization_max": 7,\n'
    else:
        # G3-G5 Q11 paragraph — Ideas 0-15, Conventions 0-5, no Organization bucket
        ideas_max, org_max, conv_max, total_max = 15, 0, 5, 20
        org_line = ""
        org_max_line = ""

    return (
        "════════════════════════════════════════════════════════\n"
        "FINAL OUTPUT FORMAT (REQUIRED — machine-readable JSON)\n"
        "════════════════════════════════════════════════════════\n"
        "\n"
        "Your ENTIRE response must be a single valid JSON object — no "
        "preamble, no commentary, no markdown fences. Do ALL reasoning "
        "(CHECKLIST → COMPARATIVE INTERPRETATION → SCORE → SELF-CHECK → "
        "FEEDBACK) internally, then output ONLY the JSON.\n"
        "\n"
        "Required fields (exactly as shown):\n"
        "\n"
        "{\n"
        f'  "question": {qnum},\n'
        f'  "ideas_score": <integer 0-{ideas_max}>,\n'
        f'  "ideas_max": {ideas_max},\n'
        + org_line
        + org_max_line +
        f'  "conventions_score": <integer 0-{conv_max}>,\n'
        f'  "conventions_max": {conv_max},\n'
        f'  "total_score": <integer 0-{total_max} — sum of ideas + '
        + ("organization + " if grade >= 6 and qnum == 11 else "")
        + "conventions>,\n"
        f'  "total_max": {total_max},\n'
        '  "confidence": <float 0.0-1.0 — your confidence in this score '
        'given the response clarity; see guidance below>,\n'
        '  "feedback": "<warm student-facing feedback following the '
        'VOICE RULES in the rubric above — typically 2-3 sentences for '
        'Q1-Q10, 3-5 sentences for Q11; never mention scores, rubric '
        'labels, or JSON field names in this text>",\n'
        '  "internal_notes": "<2-3 sentences summarizing the key '
        'scoring decisions; cite rubric sections when relevant>"\n'
        "}\n"
        "\n"
        "CONFIDENCE GUIDANCE:\n"
        "  - 0.95-1.0  — Response is clearly on-task, scoring is unambiguous\n"
        "                (clean refusal gate, straightforward Proficient,\n"
        "                 textbook Beginning)\n"
        "  - 0.80-0.94 — Response is clear but some rubric judgment is\n"
        "                involved (band boundary, soft convention tolerance)\n"
        "  - 0.60-0.79 — Response is ambiguous — could reasonably score\n"
        "                one band higher or lower (partial appositive,\n"
        "                edge-case copy fraction, unusual strategy)\n"
        "  - <0.60     — Response is hard to classify — escalate for\n"
        "                human review (unusual response, rubric gap)\n"
        "\n"
        "Low confidence is not a problem — it's a signal. A confidence "
        "of 0.55 with well-reasoned `internal_notes` is more useful to "
        "the grading system than a confidence of 0.95 on a borderline "
        "response. Be honest.\n"
        "\n"
        "IMPORTANT:\n"
        "  - Output ONLY the JSON object. No other text before or after.\n"
        "  - The `feedback` field is what the student sees. The other "
        "fields are for the grading system.\n"
        "  - Do NOT include score numbers, fractions, or rubric labels "
        "in the `feedback` string.\n"
        "  - If the response triggers a gate (refusal, blank, wrong "
        "topic, verbatim copy), set scores to 0, set confidence to "
        "0.95+, and use a gentle, warm invitation in `feedback` "
        "(~30 words)."
    )


def assemble_prompt(test_code: str, qnum: int, *, include_json_output: bool = False) -> str:
    """Assemble a per-question grading prompt from modules + test data.

    Returns a string with {{passage}}, {{question}}, {{response}} placeholders,
    ready to be filled by _fill_rubric() just like the old monolithic prompts.
    """
    grade = _grade_from_code(test_code)
    test_data = _read_test_data(test_code)

    parts = []

    # --- Layer 1: Grade-band base ---
    if grade == 3:
        base = _read_module("g3_base.txt")
    elif grade <= 5:
        base = _read_module("g4_g5_base.txt").replace("{grade}", str(grade))
    else:
        base = _read_module("g6_g8_base.txt").replace("{grade}", str(grade))
    parts.append(base)

    # --- Layer 2: Question-type module ---
    new_available = _q11_new_structure_available(qnum, grade)

    if grade >= 6:
        # G6-G8 essay: use new three-layer structure by default (A/B-validated win)
        use_new = USE_NEW_Q11_STRUCTURE and new_available
        if use_new:
            parts.append(_assemble_q11_essay_threelayer())
        else:
            parts.append(_read_module("q11_essay.txt"))
    elif qnum <= 5:
        q_module = _read_module("q1_q5_editing.txt")
        parts.append(q_module)
    elif qnum <= 10:
        q_module = _read_module("q6_q10_writing.txt")
        parts.append(q_module)
    else:
        # G3-G5 Q11 paragraph: use legacy module by default (A/B-validated tie
        # with new structure; legacy has fewer parse failures and lower cost).
        # Override with ALPHA_USE_NEW_Q11_PARAGRAPH=1 to use new structure.
        use_new_paragraph = (
            USE_NEW_Q11_STRUCTURE and USE_NEW_Q11_PARAGRAPH and new_available
        )
        if use_new_paragraph:
            parts.append(_assemble_q11_paragraph_threelayer(test_data))
        else:
            q_module = _read_module("q11_paragraph.txt")
            # Fill Q11-specific placeholders
            q11 = test_data.get("q11", {})
            q_module = q_module.replace("{q11_purpose}", q11.get("topic", ""))
            q_module = q_module.replace(
                "{classification_guidance}",
                _render_classification_guidance(test_data),
            )
            parts.append(q_module)

    # --- Layer 3: Test-specific section ---
    if grade >= 6:
        test_section = _render_q11_details(test_data, grade)
        if test_section:
            parts.append(test_section)
    elif qnum <= 5:
        target_section = _render_q1_q5_targets(test_data, qnum)
        if target_section:
            parts.append(target_section)
    elif qnum <= 10:
        # Q6-Q10 don't have per-question targets, just a topic reference
        title = test_data.get("title", "")
        test_code_val = test_data.get("test_code", test_code)
        parts.append(
            f"════════════════════════════════════════════════════════\n"
            f"TEST-SPECIFIC DETAILS\n"
            f"════════════════════════════════════════════════════════\n\n"
            f"Test: {test_code_val} — {title}\n"
            f"Q6-Q10: One-sentence writing about the passage (opinion/personal response with support)."
        )
    else:
        test_section = _render_q11_details(test_data, grade)
        if test_section:
            parts.append(test_section)

    # --- Machine-readable JSON output block (for self-contained per-question
    # prompts that need to return scores directly, not just student feedback)
    if include_json_output:
        parts.append(_render_json_output_block(qnum, grade))

    # --- Content placeholders ---
    parts.append(
        "🔹 TEST CONTENT\n"
        "Here is the passage:\n"
        "  {{passage}}\n"
        "Here is the question:\n"
        "  {{question}}\n"
        "Here is the student's response:\n"
        "  {{response}}"
    )

    return "\n\n".join(parts)


def assemble_observation_prompt(test_code: str, qnum: int) -> str:
    """Assemble a per-question observation prompt (Phase 2).

    Like assemble_prompt(), but uses observer modules instead of scoring modules.
    Claude returns structured observations (JSON) instead of scores.
    """
    grade = _grade_from_code(test_code)
    test_data = _read_test_data(test_code)

    parts = []

    # --- Layer 1: Grade-band base (same as scoring mode) ---
    if grade == 3:
        base = _read_module("g3_base.txt")
    elif grade <= 5:
        base = _read_module("g4_g5_base.txt").replace("{grade}", str(grade))
    else:
        base = _read_module("g6_g8_base.txt").replace("{grade}", str(grade))
    parts.append(base)

    # --- Layer 2: Observer module (different from scoring mode) ---
    if grade >= 6:
        q_module = _read_module("q11_essay_observer.txt")
        parts.append(q_module)
    elif qnum <= 5:
        q_module = _read_module("q1_q5_observer.txt")
        parts.append(q_module)
    elif qnum <= 10:
        q_module = _read_module("q6_q10_observer.txt")
        parts.append(q_module)
    else:
        q_module = _read_module("q11_paragraph_observer.txt")
        q11 = test_data.get("q11", {})
        q_module = q_module.replace("{q11_purpose}", q11.get("topic", ""))
        q_module = q_module.replace(
            "{classification_guidance}",
            _render_classification_guidance(test_data),
        )
        parts.append(q_module)

    # --- Layer 3: Test-specific section (same as scoring mode) ---
    if grade >= 6:
        test_section = _render_q11_details(test_data, grade)
        if test_section:
            parts.append(test_section)
    elif qnum <= 5:
        target_section = _render_q1_q5_targets(test_data, qnum)
        if target_section:
            parts.append(target_section)
    elif qnum <= 10:
        title = test_data.get("title", "")
        test_code_val = test_data.get("test_code", test_code)
        parts.append(
            f"════════════════════════════════════════════════════════\n"
            f"TEST-SPECIFIC DETAILS\n"
            f"════════════════════════════════════════════════════════\n\n"
            f"Test: {test_code_val} — {title}\n"
            f"Q6-Q10: One-sentence writing about the passage (opinion/personal response with support)."
        )
    else:
        test_section = _render_q11_details(test_data, grade)
        if test_section:
            parts.append(test_section)

    # --- Content placeholders ---
    parts.append(
        "🔹 TEST CONTENT\n"
        "Here is the passage:\n"
        "  {{passage}}\n"
        "Here is the question:\n"
        "  {{question}}\n"
        "Here is the student's response:\n"
        "  {{response}}"
    )

    return "\n\n".join(parts)


def assemble_qualitative_prompt(test_code: str) -> str:
    """Run 1 of the 3-run pipeline: qualitative classification.

    Returns a string with {{passage}}, {{question}}, {{response}}
    placeholders. Independent of grade — the same prompt is used for
    G3-G5 paragraphs and G6-G8 essays; grade-specific thresholds are
    referenced in the prompt body.
    """
    protocol = _read_protocol("q11_qualitative.txt")
    return protocol


def assemble_mastery_prompt(test_code: str) -> str:
    """Run 2 of the 3-run pipeline: content scoring.

    Returns a string with {{passage}}, {{question}}, {{response}},
    {{run1_observations}} placeholders. The orchestrator fills
    {{run1_observations}} with the JSON output from Run 1.
    """
    grade = _grade_from_code(test_code)
    test_data = _read_test_data(test_code)

    if grade >= 6:
        protocol = _read_protocol("q11_mastery_essay.txt")
        test_section = _render_q11_details(test_data, grade)
    else:
        protocol = _read_protocol("q11_mastery_paragraph.txt")
        test_section = _render_q11_details(test_data, grade)
        # Fill classification guidance if the test_data defines one
        guidance = _render_classification_guidance(test_data)
        if guidance:
            test_section = (test_section + "\n\n" + guidance) if test_section else guidance

    parts = [protocol]
    if test_section:
        parts.append(test_section)
    return "\n\n".join(parts)


def assemble_mechanics_prompt(test_code: str) -> str:
    """Run 3 of the 3-run pipeline: mechanics enumeration.

    Returns a string with {{response}}, {{grade}}, {{question_format}}
    placeholders. The passage is NOT included — mechanics grading is
    context-free.
    """
    return _read_protocol("q11_mechanics.txt")


def clear_cache():
    """Clear the module and test data caches (e.g., after admin sync)."""
    _read_module.cache_clear()
    _read_test_data.cache_clear()
    _read_rubric.cache_clear()
    _read_protocol.cache_clear()
    _read_paragraph_examples.cache_clear()
    _read_essay_examples.cache_clear()
    _read_test_data.cache_clear()
