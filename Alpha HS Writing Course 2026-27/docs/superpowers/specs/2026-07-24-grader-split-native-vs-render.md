# Grader routing: native (sentence) + Render (paragraph and up)

**Date:** 2026-07-24
**Supersedes the "allowlist blocker" framing in** `2026-07-24-grader-allowlist-and-wiring-fix.md` (that finding
stands, but the resolution is now the split below, not "allowlist our Render host for everything").
**Decision owner:** Noel. This spec is the shared source of truth for the course session AND the grader session.

## The question that started this

Before freezing the Render grader and porting it to AWS: how do we know grading works for EVERY written
response a student produces (all in-lesson guided writes + all PP100 prompts)? A live L01 review had surfaced
one grading gap by accident, which meant there was no systematic coverage proof.

## The written-response universe (measured)

Scored written responses (in-lesson `production_frq` + every PP100 form), by grain:

| grain | responses | distinct routes |
|---|---|---|
| sentence | 186 | 4 |
| paragraph | 95 | 4 |
| multi_paragraph | 50 | 5 |
| essay | 65 | 5 |

A "route" = a distinct `(grain, frq_type, mode, rubric)` combo. Certifying a grader = proving it on each route,
not on all 396 responses.

(Separately: 95 in-lesson `diagnosis_frq` items are self-check/calibration, currently ungraded. 47 of them
bundle multiple instructions in one response box - see "Content prerequisite" below.)

## Two grading paths on Timeback (both verified live 2026-07-24)

1. **Native AlphaTest AI grader.** Invoked by the SAME `com.alpha-1edtech.ExternalApiScore` customOperator, but
   with Timeback's OWN hosted definition URL `https://alphatest.alpha.school/prod/ai-grading`, plus a
   `<qti-rubric-block use="ext:grading-prompt" view="scorer">` grading prompt embedded in the item. This is what
   the shipped G3-G8 STC courses use (Q6-Q10 write-sentence 3pts; Q11 write-paragraph /20).
   - **PROVEN:** an HS sentence item wired this way POSTs 201 and the operator + host + rubric-block ALL persist
     in the stored `rawXml`. No allowlist error (Timeback's own host is inherently approved).
2. **External Render grader** (`hs-writing-grading.onrender.com/score`). Our purpose-built rubric grader with
   grain/mode/rubric routing + panel scorers.
   - **BLOCKED for direct wiring:** not on Timeback's approved-grader allowlist. JSON push silently STRIPS the
     operator; XML push 500s (`validateCustomOperatorUrls`). Reaching it needs either an allowlist add or
     re-hosting on an approved pattern (this is the grader-session's job; see the other spec).

## DECISION: route by grain

- **sentence -> NATIVE grader.** 186 responses, 4 routes. Sentence-grain claims have unbounded valid phrasings
  but a compact rubric; the native grader (proven on G3 sentences) is sufficient and removes the allowlist/AWS
  dependency for the largest slice.
- **paragraph, multi_paragraph, essay -> RENDER grader.** 210 responses. Any response beyond a single sentence
  goes to Render, where the purpose-built panel scorers (rc.staar development/conventions; rc.4trait
  4-criterion argument/analysis) live. Rationale: HS extended writing carries real rubric weight that the
  generic native grader is not trusted to score to our standard. (Note: this is a QUALITY judgment, not a native
  limit - G3 grades paragraphs natively /20 - so it can be revisited if native proves strong enough.)

### Native grader owns these 4 sentence routes (each needs an authored rubric-block prompt)

| frq_type | rubric | count | prompt needed |
|---|---|---|---|
| writing | rc.staar | 111 | sentence answer-quality 0-2 + conventions 0-1 |
| writing | rc.4trait | 54 | sentence, 4trait-aligned (G11/G12) |
| revision | rc.staar | 18 | sentence revision skill 0-1 + conventions 0-1 |
| revision | rc.4trait | 3 | sentence revision, 4trait-aligned |

So **4 native rubric-block grading prompts** to author (reuse the G3 prompt craft: pre-scoring gates ->
evidence log -> mechanical rubric -> JSON output). The rc.4trait sentence prompts are distinct from the
rc.staar ones (different criteria), so do not collapse them.

## Work items

### Course session (this repo)
1. **Native wiring path in the pusher.** `wire_payload` must emit, for SENTENCE-grain items, the native
   operator (`definition=https://alphatest.alpha.school/prod/ai-grading`) + the route's rubric-block grading
   prompt, as **XML-format** POST (JSON strips the operator - proven). For paragraph+ items, keep the Render
   operator (pending the grader session's allowlist/host resolution).
2. **Author the 4 sentence rubric-block prompts** (rc.staar/rc.4trait x writing/revision).
3. **Fix the doubled query-param bug** in the Render wiring (`_grader_url_for` appended params to an
   already-parameterized URL in the pilot).
4. **Re-push** sentence mastery items with native wiring; hold paragraph+ until the Render path is unblocked.
5. **Verify** post-push that the stored `rawXml` contains the operator (the check the earlier JSON-field
   verification missed).

### Grader session (Render -> AWS)
- Resolve the Render allowlist/host so paragraph+ items can wire to it (per the other 2026-07-24 spec). The
  Render grader now only needs to cover paragraph/multi_paragraph/essay routes (10 routes), not sentence.
- Build the route-conformance harness for THOSE routes (strong/weak/empty/off-topic probes; assert in-scale
  score, ordering sanity, non-empty feedback) against Render, then re-run post-AWS-port.

### Content prerequisite (before certifying ANY grader)
- **47 diagnosis_frq tasks bundle multiple instructions** ("mark each yes/no AND rewrite AND name the fix" in
  one box). A grader cannot score a multi-instruction response. Decide per task: split into separate steps, or
  drop the self-diagnosis (keep only the gradeable rewrite). Council-adjudicate keep-vs-drop. This gates
  grading of the diagnosis writes; it does not block sentence/PP100 grading.

## Still unproven (needs an enrolled student session)

Both graders' actual SCORING can only be observed at submit-time through an authenticated enrolled student
(the `/prod/ai-grading` endpoint is server-invoked; direct POST is 405, and the QTI test is 401 anonymously).
So the final quality proof - native scores HS sentences sanely; Render scores HS essays to rubric - requires
the enrolled-session run (see `docs/CODEX_AUTHENTICATED_SESSION.md`). The DELIVERABILITY of the native path
(accepted, persists, no allowlist) is proven; its HS scoring QUALITY is not yet.
```
