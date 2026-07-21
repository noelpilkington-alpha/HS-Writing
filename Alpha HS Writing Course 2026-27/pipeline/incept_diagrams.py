"""
incept_diagrams.py  -  the _INCEPT_DIAGRAMS registry: Incept-generated drawio PNGs bound into teach cards.

Parallel to l01_diagrams.DIAGRAMS, but for DISPLAY-ONLY PNGs (not inline SVG). Entries are bound via
gated_reading's _content_card(img=(src, alt)), which renders an <img>. A slot never gets both an
authored SVG and an Incept PNG (the authored SVG wins; see gated_reading).

INCEPT_DIAGRAMS: dict keyed (lesson_id:str, slot_idx_1based:int) -> (rel_path:str, alt_text:str).
  - rel_path is base_url-RELATIVE (e.g. "incept_diagrams/foo.png"); gated_reading prepends base_url at
    render time so the same entry works in preview + prod. The PNGs live under
    Generated_Content/incept_diagrams/ in the repo (committed) and are served from that path by the host.
  - alt_text is HAND-AUTHORED here (NOT Incept's raw alt_text): alt renders into the DOM as student-facing
    text, and Incept's alt strings carried em dashes (a hard-rule violation), so we author clean, no-em-dash
    alt that traces to the diagram's labels.

Populated by the first live bind (Task 7, 2026-07-21): 10 abstract writing-structure diagrams across
G9-G12, each verify_drawio-checked (labels present, anti-garble), below_bar False, judge_score 100, and
regenerated where needed to strip em dashes and any 'what NOT to do' anti-pattern panel.
"""

# base_url-relative path prefix; gated_reading prepends base_url. PNGs committed under Generated_Content/.
_D = "incept_diagrams"

INCEPT_DIAGRAMS: dict = {
    # G9 -- claim / evidence / reasoning structures
    ("ACC-W910-L-G9-C905-0004", 1): (
        f"{_D}/g9_controlling_idea.png",
        "Formula diagram: FOCUS plus PARTS plus NO SIDE equals a CONTROLLING IDEA."),
    ("ACC-W910-L-G9-C902-0008", 1): (
        f"{_D}/g9_relevant_evidence.png",
        "Funnel diagram: many TRUE FACTs narrow to the RELEVANT EVIDENCE that PROVES THE CLAIM; "
        "off-topic true facts are set aside."),
    ("ACC-W910-L-G9-C903-0010", 1): (
        f"{_D}/g9_reasoning_hinge.png",
        "Diagram: EVIDENCE connects through a reasoning HINGE (because, but, or so) to the CLAIM."),
    ("ACC-W910-L-G9-C903-0012", 1): (
        f"{_D}/g9_point_evidence_warrant.png",
        "Three ordered boxes for a body paragraph: POINT, then EVIDENCE, then WARRANT."),
    # G10 -- analysis + synthesis structures
    ("ACC-W910-L-G10-C1003-0009", 1): (
        f"{_D}/g10_device_effect_warrant.png",
        "Three-step analysis chain: DEVICE creates EFFECT, which the WARRANT explains why it matters."),
    ("ACC-W910-L-G10-C1006-0017", 1): (
        f"{_D}/g10_weave.png",
        "Diagram: SOURCE A and SOURCE B both flow into one WEAVE box, one claim built from both sources."),
    ("ACC-W910-L-G10-C1006-0016", 1): (
        f"{_D}/g10_synthesis_claim.png",
        "Diagram: SOURCE 1, SOURCE 2, and SOURCE 3 converge into a single SYNTHESIS CLAIM that is your own."),
    ("ACC-W910-L-G10-C1003-0025", 1): (
        f"{_D}/g10_analytical_thesis.png",
        "Flowchart: an ANALYTICAL THESIS proved by parallel DEVICE to EFFECT chains."),
    # G11 -- argument synthesis (weave the argument, weight the sources)
    ("ACC-W1112-L-G11-C1102-0014", 1): (
        f"{_D}/g11_synthesis_weave.png",
        "Diagram: a CLAIM supported by SOURCE A and SOURCE B, each connected through its own WARRANT."),
    # G12 -- complex claim
    ("ACC-W910-L-G12-C1201-0003", 1): (
        f"{_D}/g12_complex_claim.png",
        "Diagram: a COMPLEX CLAIM built from a TENSION and a NUANCE, accounting for competing considerations."),

    # ---- Batch 2 (2026-07-21): 25 additional structure diagrams across G9-G12 ----
    # G9
    ("ACC-W910-L-G9-C901-0003", 1): (
        f"{_D}/g9_specific_so_what_claim.png",
        "Diagram: SPECIFIC plus SO-WHAT combine into a STRONG CLAIM."),
    ("ACC-W910-L-G9-C901-0006", 1): (
        f"{_D}/g9_verb_to_product.png",
        "Decision diagram: the TASK VERB routes to a CLAIM (with side) for argue, or a FOCUS (no side) for explain."),
    ("ACC-W910-L-G9-C902-0007", 1): (
        f"{_D}/g9_source_three_ways.png",
        "Diagram: QUOTE, PARAPHRASE, and SUMMARIZE all require you to NAME THE SOURCE."),
    ("ACC-W910-L-G9-C902-0009", 1): (
        f"{_D}/g9_integrated_quote.png",
        "Diagram: a QUOTE passes through TAG then FOLD IN to become an INTEGRATED quote inside your sentence."),
    ("ACC-W910-L-G9-C904-0020", 1): (
        f"{_D}/g9_order_and_link_paragraphs.png",
        "Diagram: ORDER paragraphs so each builds on the last, then LINK the seams with a TRANSITION."),
    ("ACC-W910-L-G9-C904-0021", 1): (
        f"{_D}/g9_intro_conclusion_jobs.png",
        "Diagram: an INTRODUCTION does ORIENT then THESIS; a CONCLUSION lands the UPSHOT."),
    ("ACC-W910-L-G9-C904-0023", 2): (
        f"{_D}/g9_essay_assembly_sequence.png",
        "Sequence: PLAN, then INTRO, then BODY, then CONCLUSION, then CHECK."),
    # G10
    ("ACC-W910-L-G10-C1001-0003", 1): (
        f"{_D}/g10_counterargument_three_parts.png",
        "Sequence: a counterargument is POSITION, then ACKNOWLEDGE the other side, then REFUTE it."),
    ("ACC-W910-L-G10-C1005-0013", 1): (
        f"{_D}/g10_error_type_to_fix.png",
        "Diagram: each ERROR TYPE (too general, off-purpose, circular) leads to its own FIX."),
    ("ACC-W910-L-G10-C1006-0015", 2): (
        f"{_D}/g10_pool_mapping_sequence.png",
        "Five-step sequence for mapping a source pool: READ, LABEL, DECIDE, PICK, WRITE."),
    ("ACC-W910-L-G10-C1006-0018", 2): (
        f"{_D}/g10_source_relationship_sequence.png",
        "Five-step sequence: READ BOTH, find AGREEMENT, find CLASH, PINPOINT the issue, CHECK."),
    # G11
    ("ACC-W1112-L-G11-C1101-0001", 1): (
        f"{_D}/g11_scope_claim_three_axes.png",
        "Diagram: narrow a claim on WHOM, WHICH CASE, and WHEN to reach a SCOPED CLAIM."),
    ("ACC-W1112-L-G11-C1101-0002", 1): (
        f"{_D}/g11_nuanced_claim_not_x_but_y.png",
        "Diagram: NOT-X then BUT-Y forms a NUANCED CLAIM."),
    ("ACC-W1112-L-G11-C1101-0003", 1): (
        f"{_D}/g11_qualified_claim_structure.png",
        "Diagram: LIMIT plus COMMIT plus REASON make a QUALIFIED CLAIM."),
    ("ACC-W1112-L-G11-C1101-0004", 1): (
        f"{_D}/g11_line_of_reasoning_chain.png",
        "Chain: REASON 1 leads to REASON 2 leads to REASON 3, then to the CLAIM (a LINE OF REASONING, not a pile)."),
    ("ACC-W1112-L-G11-C1103-0007", 1): (
        f"{_D}/g11_choice_effect_purpose.png",
        "Chain: CHOICE creates EFFECT, which serves PURPOSE."),
    ("ACC-W1112-L-G11-C1108-0010", 1): (
        f"{_D}/g11_credibility_grounds.png",
        "Diagram: CREDIBILITY rests on WHO PRODUCED the source and whether its CLAIMS are BACKED."),
    ("ACC-W1112-L-G11-C1108-0011", 1): (
        f"{_D}/g11_source_strengths_and_limits.png",
        "Diagram: weigh a source by its STRENGTHS (what to trust it for) and its LIMITS (where it falls short)."),
    ("ACC-W1112-L-G11-C1102-0012", 2): (
        f"{_D}/g11_synthesis_sequence.png",
        "Four-step sequence: READ ALL, FIND LINK, state the CLAIM, BUILD the argument."),
    ("ACC-W1112-L-G11-C1105-0021", 1): (
        f"{_D}/g11_weigh_perspective.png",
        "Sequence: to weigh a perspective, CONCEDE, then LIMIT, then ADVANCE your position."),
    ("ACC-W1112-L-G11-C1105-0022", 2): (
        f"{_D}/g11_multi_perspective_plan.png",
        "Plan: POSITION, then ASSIGN each perspective to a paragraph, then DRAFT, then CHECK."),
    ("ACC-W1112-L-G11-C1106-0023", 2): (
        f"{_D}/g11_time_budget.png",
        "Timeline: budget the 40 minutes as READ, PLAN, DRAFT, CHECK."),
    ("ACC-W1112-L-G11-C1103-0029", 1): (
        f"{_D}/g11_three_task_types.png",
        "Diagram: three task types (SYNTHESIS, SOURCE-FREE, MULTI-PERSPECTIVE), each named by its tell."),
    # G12
    ("ACC-W910-L-G12-C1201-0001", 1): (
        f"{_D}/g12_situate_question.png",
        "Diagram: zoom from a NARROW PROMPT out to the BROADER QUESTION, then ANSWER WITHIN that frame."),
    ("ACC-W910-L-G12-C1201-0005", 2): (
        f"{_D}/g12_rhetorical_analysis_plan.png",
        "Sequence: SITUATION, then TENSION, then CHOICES, each TIED back to situation and tension."),
}
