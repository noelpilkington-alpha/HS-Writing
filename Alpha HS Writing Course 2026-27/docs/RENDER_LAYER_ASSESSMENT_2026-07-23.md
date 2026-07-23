# Render-Layer Council Rules - Assessment (2026-07-23)

Before building the render-layer engine changes, investigated what gated_reading ALREADY does for the three
render-layer Council rules. Finding: they are essentially ALREADY IMPLEMENTED. No engine change is warranted.

## Rule: PRESENT-ONCE SOURCE -> ALREADY DONE
build_lesson_html tracks `inlined_sources` (gated_reading.py ~705-794): a source is inlined in FULL only the
FIRST time it appears; later same-source writes get a one-line `_source_reminder`, not the full block. Deliberate
exception: BOXED high-load writes (multi_paragraph/essay/gate) re-show the full source in a capped-height
scroller so the student can reference it WHILE composing (correct pedagogy - the source is needed at point of
use, not redundant). This IS the team's earlier anti-redundancy fix; matches the Council ruling exactly.

## Rule: FADE THE CHECK-TOOL -> ALREADY DONE
Verified in rendered L01: the FULL 3-question list appears exactly ONCE (the "Your check tool" REMEMBER block);
the two later recurrences are BY-NAME references ("run the 3 questions"), not verbatim restatements. That is
precisely the Council's fade (teach in full once, re-invoke by name). No verbatim 4-5x restatement exists in
the render (the Fable-5 reviewer's "restated 4-5x" counted by-name references + item-level reminders as if they
were full restatements).

## Rule: CHUNK DENSE BLOCKS -> render already splits; residual is source-authoring
_render_body / _html_blocks split authored body on block markup (<p>/<li>/<ol>/<br>) into separate paragraphs;
render_qc flags a >55-word prompt with NO block break as a wall. Remaining density is in SOURCE authoring (a
few run-together prompts the colleague/Council flagged), handled per-lesson in the content pass, not by an
engine change.

## The ONE real render-layer item (small, deferred by default)
The video-lesson COMPRESS-vs-GATE mismatch (see CONTENT_FIX_RENDER_VERIFY): for lessons with an intro video,
_compress_teach_body drops the teach-card expansion (incl. the term definition) from the ARTICLE, while
define_before_use reads the uncompressed SOURCE. Options: (a) keep the one-line definition in the compressed
callout, or (b) have the gate check the rendered article for video lessons. This is a targeted ~1-function
change, NOT the broad present-once/fade/chunk build. Recommend handling it as a small standalone fix if desired.

## Conclusion
No broad render-layer engine change is justified - the present-once/fade/chunk behaviors already exist and match
the Council ruling. The content-LAYER fixes (committed 3c4cdd8) were the real remediation. Remaining optional
work: the small compress-vs-gate definition fix.
