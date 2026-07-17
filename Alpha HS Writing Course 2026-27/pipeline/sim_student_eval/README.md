# Simulated-Student Curriculum Evaluation (G9 pilot)

LLM "students" (Fable-5 + GPT), with no knowledge of course development, walk the G9 course
in sequence, attempt every task, take the test bank, and produce a report answering:
1. Do the lessons make sense?  2. Are there redundancies?
3. Do they prepare students for the full compositions?  4. Do they prepare students for the tests?

## Design boundary
Students see ONLY `render_student_experience(L)` (the dev-free view) plus a bounded on-disk
learner journal (their only memory between lessons). They never see source, ids, gates, or labels.
No writing is scored (grading is not wired); findings are lived experience + deterministic MCQ matches
(choice + inline-choice items only; hottext/text-entry/extended-text are attemptability-only and reported
as unscored so the match rate is not over-read).

## Run (from the pipeline dir)
    cd "Alpha HS Writing Course 2026-27/pipeline"

    # full pilot: 2 models x 2 personas x 27 lessons + test
    python -m sim_student_eval.run_eval

    # cheap smoke first (2 lessons, 1 model, no test)
    python -m sim_student_eval.run_eval --limit 2 --personas average --models fable --no-test --run-id smoke

Options: --limit N, --personas average,achiever, --models fable,gpt, --gpt-model <id>,
--report-model <id>, --no-test, --run-id NAME, --resume, --synthesize-only.

Safety: fails fast if a requested model's API key is missing; refuses to write into a run-id that already
has journals (use a fresh --run-id, --resume to continue, or --synthesize-only to rebuild the report);
one failed lesson or test item is logged and the walk continues; a synthesize failure leaves journals
intact and prints a --synthesize-only retry hint.

Outputs land in `out/<run_id>/`: journal_*.jsonl, transcript_*.jsonl, test_*.json, SIM_STUDENT_EVAL_G9.md.

## Live smoke results (2026-07-16)
- FABLE path: WORKS end-to-end. 2-lesson smoke (average_fable) produced high-quality, specific journals;
  memory carried (l02 felt_repeated correctly named g9_l01 + flagged the 3x same-claim repetition), and the
  synthesis report led with a real content bug (l02 Step 6 MCQ with no options) and correctly labeled its
  own single-walk evidence limits. Report model claude-fable-5 works.
- GPT path: BLOCKED by account billing, NOT a code bug. OpenAI returned 429 insufficient_quota (the key in
  .env is a well-formed sk-proj... key but the project has no available quota/billing). The harness handled
  it correctly: per-lesson error logged, walk continued, no crash. To enable the GPT-student walks, add
  billing/quota to that OpenAI project (or supply a funded key), then re-smoke:
      python -m sim_student_eval.run_eval --limit 2 --personas average --models gpt --no-test --run-id smoke_gpt2
- WORKING GPT MODEL ID: NOT YET CONFIRMED. The 429 (quota) happens before model validation, so gpt-5.5 is
  unverified. On a funded key, if gpt-5.5 errors as an unknown model, re-run with --gpt-model <valid-id>.

## Scaling to G10-G12
The harness is grade-general in shape; the loaders (`render_course.load_g9_lessons`,
`test_taker.load_g9_test_items`) are G9-hardcoded. Generalize by parameterizing the grade
glob before running other grades. Add the struggling + distractible personas in personas.py.
