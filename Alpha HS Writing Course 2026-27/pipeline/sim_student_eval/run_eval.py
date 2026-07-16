# pipeline/sim_student_eval/run_eval.py
"""Orchestrator: 2 models x 2 personas x 27 G9 lessons + test -> report.
Each (persona, model) is an independent course-walk with its own journal. The next lesson
sees ONLY persona + journal digest + rendered lesson (never prior raw transcripts).

Safety for a PAID run: fails fast if a requested model's key is missing; refuses to write
into a run-id that already has journals (unless --resume, which skips already-recorded lessons,
or --synthesize-only, which just rebuilds the report from an existing run dir). One failed
lesson or test item never aborts a walk; journals are appended per-lesson so partial progress
survives a crash."""
import os, sys, json, argparse

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, ".."))

from sim_student_eval.personas import PERSONAS
from sim_student_eval.models import load_keys, FableClient, GptClient
from sim_student_eval.render_course import load_g9_lessons, short_id
from sim_student_eval.journal import JournalStore
from sim_student_eval.student_agent import walk_lesson
from sim_student_eval.test_taker import load_g9_test_items, take_test
from sim_student_eval.analyst import synthesize

OUT_ROOT = os.path.join(HERE, "out")
KNOWN_MODELS = ("fable", "gpt")


def _client(model_name, keys, gpt_model):
    if model_name == "fable":
        return FableClient(keys["anthropic"])
    if model_name == "gpt":
        return GptClient(keys["openai"], model=gpt_model)
    raise ValueError(model_name)


def _key_for(model_name, keys):
    return keys["anthropic"] if model_name == "fable" else keys["openai"] if model_name == "gpt" else ""


def run_walk(persona_id, model_name, lessons, run_dir, keys, gpt_model, do_test, resume):
    persona = PERSONAS[persona_id]
    client = _client(model_name, keys, gpt_model)
    tag = f"{persona_id}_{model_name}"
    jstore = JournalStore(os.path.join(run_dir, f"journal_{tag}.jsonl"))
    tpath = os.path.join(run_dir, f"transcript_{tag}.jsonl")
    # resume: skip lessons already recorded for this walk (by seq), so a re-run continues
    # rather than re-paying + double-appending. Only meaningful with --resume.
    done_seqs = {e.get("seq") for e in jstore.entries()} if resume else set()
    for seq, L in enumerate(lessons, 1):
        if seq in done_seqs:
            print(f"  [{tag}] {seq}/{len(lessons)} {short_id(L)} (resume: skip)")
            continue
        try:
            res = walk_lesson(client, persona, L, jstore.digest())
        except Exception as e:  # keep the walk alive on a single API failure
            res = {"lesson": short_id(L), "response": "", "journal_update": {"lesson": short_id(L), "seq": seq}, "raw_error": repr(e)}
        res["journal_update"]["seq"] = seq
        res["journal_update"]["lesson"] = res["lesson"]
        jstore.append(res["journal_update"])
        with open(tpath, "a", encoding="utf-8") as f:
            f.write(json.dumps({"lesson": res["lesson"], "seq": seq, "response": res["response"], "error": res.get("raw_error", "")}, ensure_ascii=False) + "\n")
        print(f"  [{tag}] {seq}/{len(lessons)} {res['lesson']}" + (" ERROR" if res.get("raw_error") else ""))
    if do_test:
        test_path = os.path.join(run_dir, f"test_{tag}.json")
        if resume and os.path.exists(test_path):
            print(f"  [{tag}] test: (resume: skip, already done)")
            return
        try:
            items = load_g9_test_items()
            tres = take_test(client, persona, items, jstore.digest())
            with open(test_path, "w", encoding="utf-8") as f:
                json.dump(tres, f, ensure_ascii=False, indent=2)
            print(f"  [{tag}] test: mcq {tres['mcq_scored']}")
        except Exception as e:  # a test-pass failure must not kill later walks
            print(f"  [{tag}] test: ERROR {e!r}")


def _write_report(run_dir, anthropic_key, model):
    """Wrapped so a synthesize failure leaves all journals intact and tells you how to retry."""
    try:
        md = synthesize(run_dir, anthropic_key, model=model)
    except Exception as e:
        print(f"SYNTHESIZE FAILED ({e!r}). Journals + transcripts are intact in {run_dir}.")
        print(f"Re-run just the report with: python -m sim_student_eval.run_eval --synthesize-only "
              f"--run-id {os.path.basename(run_dir)} [--report-model claude-fable-5]")
        return None
    rp = os.path.join(run_dir, "SIM_STUDENT_EVAL_G9.md")
    with open(rp, "w", encoding="utf-8") as f:
        f.write(md)
    print("REPORT:", rp)
    return rp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="only the first N lessons (smoke)")
    ap.add_argument("--personas", default="average,achiever")
    ap.add_argument("--models", default="fable,gpt")
    ap.add_argument("--gpt-model", default="gpt-5.5")
    ap.add_argument("--report-model", default="claude-fable-5",
                    help="model for the synthesis report (proven default; the plan's claude-opus-4-8 was unverified)")
    ap.add_argument("--no-test", action="store_true")
    ap.add_argument("--resume", action="store_true",
                    help="continue an existing run-id: skip lessons/tests already recorded (no re-pay, no double-append)")
    ap.add_argument("--synthesize-only", action="store_true",
                    help="skip all walks; just (re)build the report from an existing run-id")
    ap.add_argument("--run-id", default="g9_pilot")
    a = ap.parse_args()

    keys = load_keys()
    run_dir = os.path.join(OUT_ROOT, a.run_id)

    # --synthesize-only: no walks, no spend on students; just rebuild the report from disk.
    if a.synthesize_only:
        if not os.path.isdir(run_dir):
            ap.error(f"--synthesize-only: run dir does not exist: {run_dir}")
        if not keys["anthropic"]:
            ap.error("--synthesize-only needs ANTHROPIC_API_KEY (for the report model).")
        print(f"Synthesizing report from {run_dir} ...")
        _write_report(run_dir, keys["anthropic"], a.report_model)
        return

    persona_ids = [p.strip() for p in a.personas.split(",") if p.strip()]
    unknown = [p for p in persona_ids if p not in PERSONAS]
    if unknown:
        ap.error(f"unknown persona(s): {', '.join(unknown)}. Known: {', '.join(sorted(PERSONAS))}")

    model_names = [m.strip() for m in a.models.split(",") if m.strip()]
    unknown_m = [m for m in model_names if m not in KNOWN_MODELS]
    if unknown_m:
        ap.error(f"unknown model(s): {', '.join(unknown_m)}. Known: {', '.join(KNOWN_MODELS)}")

    # KEY PREFLIGHT (#3): fail before spending a cent if a requested model's key is missing.
    missing = [m for m in model_names if not _key_for(m, keys)]
    if missing:
        env_name = {"fable": "ANTHROPIC_API_KEY", "gpt": "OPEN_AI_API_KEY"}
        ap.error("missing API key(s) for requested model(s): "
                 + "; ".join(f"{m} needs {env_name[m]}" for m in missing)
                 + ". Set them in HS Writing/.env or drop the model from --models.")
    # the report model is Anthropic-backed; make sure that key exists too
    if not keys["anthropic"]:
        ap.error("ANTHROPIC_API_KEY is required for the synthesis report (--report-model).")

    lessons = load_g9_lessons()
    if a.limit:
        lessons = lessons[:a.limit]

    # RUN-DIR GUARD (#1): refuse to write into a run-id that already has journals unless
    # --resume (continue it) is set. Prevents silent double-append + memory contamination on re-run.
    if os.path.isdir(run_dir):
        import glob as _glob
        existing = _glob.glob(os.path.join(run_dir, "journal_*.jsonl"))
        if existing and not a.resume:
            ap.error(f"run-id '{a.run_id}' already has {len(existing)} journal file(s) in {run_dir}. "
                     f"Use a fresh --run-id, or pass --resume to continue it, or --synthesize-only to rebuild the report.")
    os.makedirs(run_dir, exist_ok=True)
    print(f"Run dir: {run_dir}  |  lessons: {len(lessons)}  |  resume={a.resume}")

    for persona_id in persona_ids:
        for model_name in model_names:
            print(f"WALK: {persona_id} x {model_name}")
            run_walk(persona_id, model_name, lessons, run_dir, keys, a.gpt_model, not a.no_test, a.resume)

    print("Synthesizing report...")
    _write_report(run_dir, keys["anthropic"], a.report_model)


if __name__ == "__main__":
    main()
