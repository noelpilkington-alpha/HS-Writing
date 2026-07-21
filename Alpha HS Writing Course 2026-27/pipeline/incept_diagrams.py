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
}
