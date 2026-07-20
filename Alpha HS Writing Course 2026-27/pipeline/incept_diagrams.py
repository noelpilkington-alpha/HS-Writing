"""
incept_diagrams.py  -  the _INCEPT_DIAGRAMS registry: Incept-generated drawio PNGs bound into teach cards.

Parallel to l01_diagrams.DIAGRAMS, but for DISPLAY-ONLY PNGs (not inline SVG). Entries are bound via
gated_reading's _content_card(img=(png_url_or_local_path, alt_caption)), which renders an <img>. A slot
never gets both an authored SVG and an Incept PNG (the authored SVG wins; see gated_reading).

INCEPT_DIAGRAMS: dict keyed (lesson_id:str, slot_idx_1based:int) -> (png_url_or_local_path:str, alt_caption:str).

Ships EMPTY. The live bind step (Task 7) populates it after each drawio is generated, verify_drawio-checked
(labels present, anti-garble), confirmed not below_bar, and its PNG downloaded to a local hosted dir. Adding
this empty registry changes NOTHING in existing output.
"""

INCEPT_DIAGRAMS: dict = {}
