"""
expected_exceptions.py  -  the EXPECTED-EXCEPTION REGISTRY (Tier A2).

Test Builder doctrine (SPOV7): "a decision without a written rationale is a latent regression... the next reader
is an agent with every incentive to revert it." The Fable eval's own finding: the wrong-flag class was
dominated NOT by real bugs but by re-litigating deliberate decisions nobody had written down.

This registry co-locates the DELIBERATE design decisions (Council + Fable verdicts, Noel calls) that a strict
auditor (Fable readiness audit, LLM panel) would otherwise re-flag every run. It has two uses:
  1. As machine-readable SUPPRESSION: a readiness-audit blocker matching an entry here is downgraded to
     resolved/expected (not re-surfaced), the same discipline scaffold_crosscheck.ADJUDICATED already uses.
  2. As the DECLARED-INTENT scope injected into the audit prompt (Tier A3), so the model judges against intent.

Extend the same pattern scaffold_crosscheck.ADJUDICATED uses. Every entry: owner + date + the trigger that
would REVERSE it (so it is not a permanent rug to sweep real defects under).
"""

# --- design-level exceptions that apply COURSE-WIDE (matched by keyword against a blocker's text) ---
# Each: key -> {"rationale", "owner", "date", "reverse_if", "match": [substrings that identify the flag class]}
DESIGN_EXCEPTIONS = {
    "scaffold_free_gate": {
        "rationale": ("Gate lessons (lesson_class='gate') are SCAFFOLD-FREE by the spine-rearchitecture verdict: "
                      "a certification is the SRSD independent-performance stage, so no worked model / "
                      "discrimination / predict-the-fix / supported teaching frame. An audit flagging a gate as "
                      "'under-scaffolded' or 'no worked example' is re-litigating this decision."),
        "owner": "Council+Fable verdict (SPINE_DELIBERATION_verdict.md)", "date": "2026-07-15",
        "reverse_if": "gate pass-rates show mastered-upstream students failing due to missing scaffold (not the format hazard)",
        "applies_when": "lesson_class == 'gate'",
        "match": ["under-scaffold", "no worked example", "no model", "missing discrimination", "no predict",
                  "add a worked", "should model", "no scaffold before the write"],
    },
    "essay_one_write_no_transfer": {
        "rationale": ("Essay-grain practice lessons end at ONE independent write + self-revision; the in-article "
                      "TRANSFER write was deliberately DROPPED (transfer routed to the gate + PP100) per the "
                      "verdict (Bjork/Messick: warm rehearsals contaminate the mastery measure). An audit "
                      "flagging 'no transfer practice' / 'only one write' at essay grain is re-litigating this."),
        "owner": "Council+Fable verdict", "date": "2026-07-15",
        "reverse_if": "gate/PP100 failure data shows students need an in-article transfer rep before the cold write",
        "applies_when": "grain == 'essay' and lesson_class == 'practice'",
        "match": ["no transfer", "only one write", "single write", "add a transfer", "no second source", "lacks transfer practice"],
    },
    "sentence_dense_discrimination": {
        "rationale": ("Sentence-grain lessons are DISCRIMINATION-DENSE by design (>=2 minimal-pair reps; verdict: "
                      "cheap fast reps at the grain where they pay off). Minimal-pair distractors are INTENDED to "
                      "be near-identical; an audit flagging 'distractor too similar' or 'too many discriminations' "
                      "on a sentence lesson is re-litigating the design."),
        "owner": "Council verdict (DI/TWR/K&H sentence review)", "date": "2026-07-15",
        "reverse_if": "students systematically miss on surface similarity rather than the target contrast",
        "applies_when": "grain == 'sentence'",
        "match": ["distractor too similar", "options too similar", "too many discrimination", "minimal pair too close",
                  "near-identical option"],
    },
    "provided_weak_draft_diagnosis": {
        "rationale": ("At paragraph grain the diagnosis_frq uses a PROVIDED weak draft ('watch the check run on "
                      "this weak draft, then do your own') as a coping-model scaffold - the sanctioned TWR/SRSD "
                      "model-before-produce move (Council scope-review verified sound). An audit flagging 'the "
                      "diagnosis fixes an example, not the student's own draft' at paragraph grain is re-litigating."),
        "owner": "Council scope-review (paragraph grain)", "date": "2026-07-15",
        "reverse_if": "paragraph lessons are found to have the essay-grain phantom-draft mismatch (wrapper says 'your draft' but verdict describes a deleted draft)",
        "applies_when": "grain in ('paragraph','multi_paragraph') and lesson_class == 'practice'",
        "match": ["provided weak draft", "fixes an example not", "not the student's own draft", "canned weak draft",
                  "diagnosis on a provided"],
    },
    "one_line_source_reminder": {
        "rationale": ("For LATER same-source writes in a lesson, the source is shown as a ONE-LINE reminder rather "
                      "than the full re-inlined block (the full block on first use; a reminder after), to avoid "
                      "the repeated-wall-of-text skim the eval found. An audit flagging 'the source is not shown "
                      "in full for this write' on a repeat same-source write is re-litigating this."),
        "owner": "gated-reading design (frq_xml source_reminder)", "date": "2026-07-14",
        "reverse_if": "students cannot recall the source at the later write (no-scroll-back harm observed)",
        "applies_when": "a repeat write on an already-inlined source",
        "match": ["source not shown in full", "only a one-line reminder", "student cannot see the full source",
                  "reminder instead of the source"],
    },
    "no_author_named_analytical": {
        "rationale": ("An analytical-claim task uses 'the author' as the agent ('the author uses X to Y'); it does "
                      "NOT require a named proper noun. An audit flagging 'no author is named so the student can't "
                      "write a claim' is overreach - the taught frame works off 'the author'."),
        "owner": "readiness-triage (G10/11/12)", "date": "2026-07-14",
        "reverse_if": "a task genuinely requires attribution the source cannot support",
        "applies_when": "analytical-claim task on a source with no named author",
        "match": ["no author is named", "no author named", "cannot name the author", "author is not identified"],
    },
}


def scope_note_for(L):
    """Tier A3: the DECLARED-INTENT scope line to inject into the audit prompt for lesson L, so the model
    judges against the design, not a generic expectation. Deterministic from the lesson's own fields."""
    from lesson_contract import grain
    cls = getattr(L, "lesson_class", "practice")
    g = grain(L)
    lines = [f"DECLARED DESIGN INTENT (judge against THIS, do not re-litigate): lesson_class={cls}, grain={g}."]
    if cls == "gate":
        lines.append("This is a scaffold-free GATE by design: a bare cue + held-out source + optional plan + "
                     "cold write + post-hoc self-score. Do NOT flag the absence of a worked model, "
                     "discrimination, or predict-the-fix - that is the intended certification format.")
    if cls == "practice" and g == "essay":
        lines.append("Essay grain by design ends at ONE independent write + a self-revision diagnosis; the "
                     "in-article transfer write was intentionally removed (transfer -> gate/PP100). Do NOT flag "
                     "'no transfer practice' or 'only one write'.")
    if g == "sentence":
        lines.append("Sentence grain by design is discrimination-dense with intentionally near-identical "
                     "minimal-pair distractors. Do NOT flag distractor similarity or discrimination count.")
    if g in ("paragraph", "multi_paragraph"):
        lines.append("The diagnosis step uses a PROVIDED weak draft as a coping model, then has the student do "
                     "their own; this is the intended scaffold. Do NOT flag it as 'not the student's own draft'.")
    return " ".join(lines)


def is_expected(blocker_text, L=None):
    """Suppression check: does this readiness-audit blocker match a written design exception (optionally scoped
    to lesson L's class/grain)? Returns (True, rationale_key) if expected, else (False, None). Conservative:
    matches only on the curated `match` substrings, so a genuine defect worded differently still surfaces."""
    from lesson_contract import grain
    t = (blocker_text or "").lower()
    cls = getattr(L, "lesson_class", "practice") if L is not None else None
    g = grain(L) if L is not None else None
    for key, e in DESIGN_EXCEPTIONS.items():
        if not any(m.lower() in t for m in e["match"]):
            continue
        # scope: if we have the lesson, only suppress when the applies_when condition plausibly holds
        if L is not None:
            aw = e.get("applies_when", "")
            if "lesson_class == 'gate'" in aw and cls != "gate":
                continue
            if "grain == 'essay'" in aw and g != "essay":
                continue
            if "grain == 'sentence'" in aw and g != "sentence":
                continue
            if "grain in ('paragraph','multi_paragraph')" in aw and g not in ("paragraph", "multi_paragraph"):
                continue
        return True, key
    return False, None


if __name__ == "__main__":
    print(f"expected-exception registry: {len(DESIGN_EXCEPTIONS)} design exceptions")
    for k, e in DESIGN_EXCEPTIONS.items():
        print(f"  {k}: reverse_if = {e['reverse_if']}")
