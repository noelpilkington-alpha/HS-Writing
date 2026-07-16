"""
judge_calibration.py  -  Tier B JUDGE CALIBRATION CORPUS (the answer key for the LLM reviewer).

WHY THIS EXISTS (the other half of "verify the verifier"):
  - Tier A's checker corpus (fixtures.py) proves the DETERMINISTIC gates catch what they claim.
  - But three defects this session were SEMANTIC - no deterministic gate can judge them:
        1. a multiple-choice DISTRACTOR that is also defensibly correct under the stem as written,
        2. a PLANNING TOOL that does not fit the grain of the deliverable (a single-paragraph outline
           used to plan a whole essay),
        3. a diagnosis step that references a PHANTOM draft (wrapper says "revise your draft" but the
           canned verdict describes a specific draft the student never actually wrote).
    These need an LLM JUDGE. An LLM judge is itself a verifier that can rot (SPOV6: "the verifier rots
    first") - it can go blind (miss a real defect) or over-flag (re-litigate deliberate design, the
    documented Fable failure mode). So the judge needs its OWN answer key.

WHAT THIS IS: a small set of LABELED cases, each a faithful BEFORE (defect present, drawn verbatim-in-
substance from the pre-fix lesson) and AFTER (the shipped fix). A trustworthy judge must FLAG every
`before` (recall) and PASS every `after` (precision). score_judge() runs any judge callable against the
key and returns recall + precision + per-case detail, so Tier B can measure a candidate judge/prompt
BEFORE trusting it on the live course - and re-measure whenever the judge prompt changes (a judge-prompt
edit that drops recall or precision fails, the test_rewrite_guard doctrine applied to the judge).

The judge callable contract (pluggable so Tier B wires in the real model, tests use deterministic fakes):
    judge_fn(excerpt: str, rubric: str) -> bool     # True == "this excerpt HAS the defect / flag it"

Provenance: each case cites the fix commit + lesson id so the label traces to a real human/Council call,
never a paraphrase. Extend this corpus whenever a new SEMANTIC defect is found and fixed.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class CalibrationCase:
    id: str                 # short slug
    defect_class: str       # the family of semantic defect
    lesson_id: str          # the real lesson the case is drawn from
    fix_commit: str         # the commit that fixed it (provenance)
    rubric: str             # the ONE question the judge must answer about the excerpt
    before: str             # excerpt WITH the defect - a correct judge FLAGS this
    after: str              # the shipped fix - a correct judge PASSES this
    why_before_fails: str   # the human/Council reason the before is a defect
    why_after_passes: str   # why the fix resolves it


# ---------------------------------------------------------------------------
# THE CALIBRATION CASES (labeled answer key)
# ---------------------------------------------------------------------------

CALIBRATION_CASES = [
    # 1. ALSO-CORRECT DISTRACTOR (sentence grain) - Council DI/K&H/TWR review, commit f3e2da4.
    CalibrationCase(
        id="also_correct_distractor",
        defect_class="also_correct_distractor",
        lesson_id="ACC-W910-L-G9-C901-0006",
        fix_commit="f3e2da4",
        rubric=("In this single-best-answer item, is any option OTHER than the keyed answer ALSO "
                "defensibly correct under the stem exactly as worded? Flag if the stem does not state "
                "the requirement that makes the keyed option the only right one."),
        before=("Argue task: which sentence is the right product?\n"
                "The prompt asks you to ARGUE that schools should switch to a four-day week. "
                "Which sentence fits that verb?\n"
                "(A) Some schools have four-day weeks.\n"
                "(B) Schools should switch to a four-day week.\n"
                "(C) Schools should switch to a four-day week because a shorter week cuts commuting "
                "days and lets students rest.\n"
                "Keyed answer: C"),
        after=("Argue task: which sentence is the right product?\n"
               "The prompt asks you to ARGUE that schools should switch to a four-day week. An argue "
               "task calls for a claim that takes a side AND backs it with a reason. Which sentence is "
               "that finished product?\n"
               "(A) Some schools have four-day weeks.\n"
               "(B) Schools should switch to a four-day week.\n"
               "(C) Schools should switch to a four-day week because a shorter week cuts commuting "
               "days and lets students rest.\n"
               "Keyed answer: C"),
        why_before_fails=("Option B takes a side, so it 'fits the ARGUE verb' the stem literally asks "
                          "for; the keyed answer C turns on having a REASON, which the stem never "
                          "required. B is therefore also-correct - two right answers."),
        why_after_passes=("The stem now states the reason requirement ('takes a side AND backs it with "
                          "a reason'), so B (side, no reason) is unambiguously wrong and C is the only "
                          "correct answer."),
    ),

    # 2. PLANNING TOOL DOES NOT FIT THE GRAIN (essay planning) - Noel flag + TWR primary-text verify, commit 3381a49.
    CalibrationCase(
        id="planner_grain_mismatch",
        defect_class="planner_grain_mismatch",
        lesson_id="ACC-W910-L-G9-C904-0019",
        fix_commit="3381a49",
        rubric=("Does the planning tool this lesson teaches match the GRAIN of what the student must "
                "produce? Flag if a single-paragraph planning tool is used to plan a whole multi-"
                "paragraph essay (a category error), or vice versa."),
        before=("Plan Your Essay with a Single-Paragraph Outline\n"
                "Before you draft your essay, fill in a Single-Paragraph Outline (SPO): write your "
                "topic sentence at the top, list your supporting details in note form under it, then "
                "write your concluding sentence. Your SPO is the plan for your whole essay - once the "
                "SPO is done, you are ready to write all of your paragraphs from it."),
        after=("Plan Your Essay with a Multiple-Paragraph Outline\n"
               "An essay is a series of paragraphs united by one thesis, so it needs a plan built for "
               "that grain: the Multiple-Paragraph Outline (MPO). At the top you write one thesis that "
               "governs the whole essay; then an introduction row; then one row per body paragraph, "
               "each pairing a main idea with its details in note form; then a conclusion. The Single-"
               "Paragraph Outline you already know is the prerequisite building block - it plans ONE "
               "paragraph; the MPO arranges several into an essay."),
        why_before_fails=("A Single-Paragraph Outline plans ONE paragraph (a topic sentence + details "
                          "+ a concluding sentence). Using it to plan a whole multi-paragraph essay is "
                          "a TWR category error: the tool does not carry a thesis or ordered body "
                          "paragraphs, so it cannot plan the deliverable's grain."),
        why_after_passes=("The lesson now teaches the Multiple-Paragraph Outline (thesis + introduction "
                          "+ ordered body main-idea/details rows + conclusion), which matches the essay "
                          "grain; the SPO is correctly framed as the single-paragraph prerequisite."),
    ),

    # 3. PHANTOM-DRAFT DIAGNOSIS (essay grain, one-write) - one-write re-architecture, commit 084ff7e.
    CalibrationCase(
        id="phantom_draft_diagnosis",
        defect_class="phantom_draft_diagnosis",
        lesson_id="ACC-W910-L-G10-C1006-0022",
        fix_commit="084ff7e",
        rubric=("Does a diagnosis/revision step reference a draft or step that does NOT exist in the "
                "student's actual flow? Flag if the wrapper tells the student to revise 'your draft' "
                "but the verdict text describes a specific draft the student never wrote (a phantom / "
                "canned draft), rather than reading the student's own independent write."),
        before=("Now revise the draft you just wrote.\n"
                "Here is the diagnosis of your draft: your second body paragraph opens with 'Another "
                "reason is that stadiums cost too much,' which repeats your first reason instead of "
                "advancing a new one, and your counterargument in paragraph three concedes the point "
                "without answering it. Fix those two spots.\n"
                "(The student did not write a draft in this lesson - the in-article transfer write was "
                "removed; this verdict describes a fixed example draft.)"),
        after=("Now revise the essay you just wrote.\n"
               "Reread your own draft against this checklist and mark where each is true: does every "
               "body paragraph advance a NEW reason (not a restatement of an earlier one)? Does your "
               "counterargument actually ANSWER the objection, not just concede it? Fix any spot where "
               "you cannot mark it true."),
        why_before_fails=("The wrapper says 'the draft you just wrote,' but the essay-grain lesson ends "
                          "at the independent write with no earlier in-article draft, and the verdict "
                          "quotes a specific paragraph the student never produced. The student is told "
                          "to revise against a canned diagnosis of a phantom draft."),
        why_after_passes=("The revision step now points the student at THEIR OWN independent write and "
                          "gives a self-revision checklist they apply to their real draft, with no "
                          "reference to a draft that does not exist."),
    ),
]


# ---------------------------------------------------------------------------
# SCORING HARNESS  (measure any judge against the answer key)
# ---------------------------------------------------------------------------

def score_judge(judge_fn) -> dict:
    """Run `judge_fn(excerpt, rubric) -> bool` against every calibration case.

    A trustworthy judge FLAGS every `before` (True) and PASSES every `after` (False). Returns:
      recall     - fraction of `before` defects the judge correctly FLAGGED (blindness metric)
      precision  - fraction of `after` fixes the judge correctly PASSED (over-flag metric)
      composite  - recall * precision (one number; 1.0 == perfect, penalizes either failure mode)
      cases      - per-case {flagged_before, passed_after, defect_class, lesson_id}
    Both metrics matter: a judge that flags everything has recall 1.0 but precision 0 (useless), and a
    judge that flags nothing has precision 1.0 but recall 0 (blind). The composite catches both."""
    n = len(CALIBRATION_CASES)
    hit_before = 0    # before correctly flagged
    pass_after = 0    # after correctly passed
    cases = []
    for c in CALIBRATION_CASES:
        flagged_before = bool(judge_fn(c.before, c.rubric))
        flagged_after = bool(judge_fn(c.after, c.rubric))
        if flagged_before:
            hit_before += 1
        if not flagged_after:
            pass_after += 1
        cases.append({
            "id": c.id, "defect_class": c.defect_class, "lesson_id": c.lesson_id,
            "flagged_before": flagged_before,   # want True
            "passed_after": not flagged_after,  # want True
        })
    recall = hit_before / n if n else 0.0
    precision = pass_after / n if n else 0.0
    return {
        "n": n,
        "recall": recall,          # caught real defects
        "precision": precision,    # did not over-flag fixed content
        "composite": recall * precision,
        "cases": cases,
    }


def make_live_judge():
    """A real Fable-5 judge callable for Tier B: judge_fn(excerpt, rubric) -> bool. Reads the .env key
    directly (NOT os.environ.setdefault - the documented stale-key trap). Returns None if no key, so
    callers can skip the live path offline. Forces a structured tool call for a reliable boolean."""
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from lesson_review import _load_env_key, MODEL
    key = _load_env_key()
    if not key:
        return None
    import anthropic
    client = anthropic.Anthropic(api_key=key)
    tool = {"name": "judge", "description": "Report whether the excerpt has the defect the rubric describes.",
            "input_schema": {"type": "object", "properties": {
                "has_defect": {"type": "boolean",
                               "description": "True if the excerpt exhibits the defect the rubric asks about."},
                "why": {"type": "string"}},
                "required": ["has_defect", "why"]}}

    def judge_fn(excerpt: str, rubric: str) -> bool:
        prompt = (f"You are a strict writing-lesson reviewer. Answer ONE question about the excerpt.\n\n"
                  f"QUESTION (the rubric): {rubric}\n\n"
                  f"=========== EXCERPT ===========\n{excerpt}\n===============================\n\n"
                  f"Call judge with has_defect=true only if the excerpt clearly exhibits the defect the "
                  f"rubric describes. Do not invent defects; judge only against the rubric question.")
        r = client.messages.create(model=MODEL, max_tokens=600, tools=[tool],
                                   tool_choice={"type": "tool", "name": "judge"},
                                   messages=[{"role": "user", "content": prompt}])
        for b in r.content:
            if getattr(b, "type", "") == "tool_use" and getattr(b, "name", "") == "judge":
                return bool(b.input.get("has_defect"))
        return False

    return judge_fn


def main():
    """CLI: score a live Fable judge against the calibration key (needs .env key). Offline: prints the
    corpus and a note. Never echoes the key."""
    import sys
    print("=== JUDGE CALIBRATION CORPUS (Tier B answer key) ===")
    for c in CALIBRATION_CASES:
        print(f"  [{c.defect_class}] {c.lesson_id} (fix {c.fix_commit})")
    judge = make_live_judge()
    if judge is None:
        print("\n(no ANTHROPIC_API_KEY in .env - offline; run with a key to score the live Fable judge)")
        return 0
    print("\nScoring the live Fable-5 judge against the key ...")
    res = score_judge(judge)
    for cd in res["cases"]:
        mark = "OK " if (cd["flagged_before"] and cd["passed_after"]) else "!! "
        print(f"  {mark}{cd['id']:26} flagged_before={cd['flagged_before']}  passed_after={cd['passed_after']}")
    print(f"\nrecall={res['recall']:.2f}  precision={res['precision']:.2f}  composite={res['composite']:.2f}  (n={res['n']})")
    return 0 if res["composite"] == 1.0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
