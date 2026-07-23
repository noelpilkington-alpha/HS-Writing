# Content-Fix Re-render Verification (2026-07-23) - LOCAL, deploy HELD

Re-rendered all 4 grades with the Council content fixes (commit 3c4cdd8). RENDER-QC clean on all 4. Verified in
the rendered artifacts (NOT yet deployed):

- L01 diagnosis check: frq-...-s8.xml now carries 3x "your call: yes / no"; pre-answered "No, it just reports a
  fact" is GONE. (The FRQ checklist renders into the item XML, not lesson.html - initial probe looked in the
  wrong file.)
- L01 transfer write: "topic you choose" present (Rule 4 escalation rendered).
- L01 jargon: "is my reason good enough" disclaimer GONE from the article.
- L04 (C901-0006) confound: distractor now carries "because" (cp item) so the connective no longer signals.
- G11 l01 (+ G10 l01/l02/l05, etc.): "your call" present = pre-answered fix rendered.
- REVERT held: G10 l09 (analysis_check, a watch-then-do lesson) does NOT have "your call" - correctly kept its
  demonstration.

## One finding worth noting (pre-existing, not introduced by this work)
L01's teach-card DEFINITION edit ("Arguable claim: this is a sentence that takes a side...") does NOT appear in
the rendered ARTICLE, because L01 has an intro video and the earlier council rule COMPRESSES the opening
teach_card to just the one-idea callout (the video teaches the expansion). So:
- The define_before_use GATE reads the SOURCE (definition present -> passes).
- The rendered ARTICLE compresses the taxonomy away (student sees it in the video, not the text).
This gate-vs-render mismatch affects every VIDEO lesson, predates this work, and is not a defect in the content
fix. Flag for the render-layer pass: decide whether the compressed callout should retain the one-line
definition, or whether the gate should check the rendered (post-compression) article for video lessons.

## Status
Fixes are rendered LOCALLY into the vercel_deploy dir. NOT deployed (per Noel: re-render + review, hold deploy).
