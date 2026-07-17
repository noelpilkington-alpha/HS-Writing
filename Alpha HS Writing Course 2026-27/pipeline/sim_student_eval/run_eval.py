# pipeline/sim_student_eval/run_eval.py
"""Orchestrator. Two modes:

  PER-GRADE (default): for --grade {g9,g10,g11,g12}, run each (persona x model) as an independent
  course-walk with its own journal; then synthesize a per-grade report. The next lesson sees ONLY
  persona + journal digest + rendered lesson (never prior raw transcripts).

  CROSS-GRADE (--cross-grade): ONE persistent student walks g9 -> g10 -> g11 -> g12 in sequence on a
  SINGLE journal spanning all grades (each entry keeps its grade-prefixed lesson id). The digest emits
  a durable per-earlier-grade skills rollup so the G12 student still recalls G9. A cross-grade report
  asks specifically about cross-grade redundancy + progression.

Safety for a PAID run: fails fast if a requested model's key is missing; refuses to write into a
run-id that already has journals (unless --resume, which skips already-recorded lessons, or
--synthesize-only, which just rebuilds the report). One failed lesson or test item never aborts a
walk; journals are appended per-lesson so partial progress survives a crash."""
import os, sys, json, argparse

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, ".."))

from sim_student_eval.personas import build_personas, GRADE_LABELS
from sim_student_eval.models import load_keys, FableClient, GptClient
from sim_student_eval.render_course import load_lessons, short_id, GRADES
from sim_student_eval.journal import JournalStore
from sim_student_eval.student_agent import walk_lesson, is_composition_lesson
from sim_student_eval.test_taker import load_test_items, take_test
from sim_student_eval.analyst import synthesize

OUT_ROOT = os.path.join(HERE, "out")
KNOWN_MODELS = ("fable", "gpt")
CROSS_GRADE_SEQUENCE = ("g9", "g10", "g11", "g12")


def _client(model_name, keys, gpt_model):
    if model_name == "fable":
        return FableClient(keys["anthropic"])
    if model_name == "gpt":
        return GptClient(keys["openai"], model=gpt_model)
    raise ValueError(model_name)


def _key_for(model_name, keys):
    return keys["anthropic"] if model_name == "fable" else keys["openai"] if model_name == "gpt" else ""


def _comp_ids(lessons):
    """short-ids of the composition-probe lessons (structural: type 7/8 or gate)."""
    return {short_id(L) for L in lessons if is_composition_lesson(L)}


def run_walk(persona_id, model_name, lessons, run_dir, keys, gpt_model, do_test, resume,
             personas, grade_label, grade, tag=None, jstore=None, seq_offset=0):
    """Walk `lessons` for one (persona, model). Reusable for both per-grade and cross-grade:
    pass a shared jstore + seq_offset to continue a single spanning journal across grades."""
    persona = personas[persona_id]
    client = _client(model_name, keys, gpt_model)
    tag = tag or f"{persona_id}_{model_name}"
    if jstore is None:
        jstore = JournalStore(os.path.join(run_dir, f"journal_{tag}.jsonl"))
    tpath = os.path.join(run_dir, f"transcript_{tag}.jsonl")
    comp = _comp_ids(lessons)
    done_seqs = {e.get("seq") for e in jstore.entries()} if resume else set()
    for i, L in enumerate(lessons, 1):
        seq = seq_offset + i
        sid = short_id(L)
        if seq in done_seqs:
            print(f"  [{tag}] {seq} {sid} (resume: skip)")
            continue
        try:
            res = walk_lesson(client, persona, L, jstore.digest(), grade_label)
        except Exception as e:  # keep the walk alive on a single API failure
            res = {"lesson": sid, "response": "", "journal_update": {"lesson": sid, "seq": seq}, "raw_error": repr(e)}
        res["journal_update"]["seq"] = seq
        res["journal_update"]["lesson"] = res["lesson"]
        jstore.append(res["journal_update"])
        with open(tpath, "a", encoding="utf-8") as f:
            f.write(json.dumps({"lesson": res["lesson"], "seq": seq, "grade": grade,
                                "is_composition": sid in comp,
                                "response": res["response"], "error": res.get("raw_error", "")},
                               ensure_ascii=False) + "\n")
        print(f"  [{tag}] {seq} {res['lesson']}" + (" ERROR" if res.get("raw_error") else ""))
    if do_test:
        test_path = os.path.join(run_dir, f"test_{tag}.json")
        if resume and os.path.exists(test_path):
            print(f"  [{tag}] test: (resume: skip, already done)")
            return jstore
        try:
            items = load_test_items(grade)
            tres = take_test(client, persona, items, jstore.digest())
            with open(test_path, "w", encoding="utf-8") as f:
                json.dump(tres, f, ensure_ascii=False, indent=2)
            print(f"  [{tag}] test: mcq {tres['mcq_scored']}")
        except Exception as e:  # a test-pass failure must not kill later walks
            print(f"  [{tag}] test: ERROR {e!r}")
    return jstore


def _write_report(run_dir, anthropic_key, model, grade, comp_ids, cross_grade=False):
    """Wrapped so a synthesize failure leaves all journals intact and tells you how to retry."""
    report_name = "SIM_STUDENT_EVAL_CROSSGRADE.md" if cross_grade else f"SIM_STUDENT_EVAL_{grade.upper()}.md"
    try:
        md = synthesize(run_dir, anthropic_key, model=model, grade=grade, comp_ids=comp_ids)
    except Exception as e:
        print(f"SYNTHESIZE FAILED ({e!r}). Journals + transcripts are intact in {run_dir}.")
        print(f"Re-run just the report with: python -m sim_student_eval.run_eval --synthesize-only "
              f"--run-id {os.path.basename(run_dir)} --grade {grade} [--report-model claude-fable-5]")
        return None
    rp = os.path.join(run_dir, report_name)
    with open(rp, "w", encoding="utf-8") as f:
        f.write(md)
    print("REPORT:", rp)
    return rp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grade", default="g9", help="g9|g10|g11|g12 (ignored with --cross-grade)")
    ap.add_argument("--cross-grade", action="store_true",
                    help="ONE persistent student walks g9->g10->g11->g12 on a single spanning journal")
    ap.add_argument("--limit", type=int, default=0, help="only the first N lessons per grade (smoke)")
    ap.add_argument("--personas", default="average,achiever")
    ap.add_argument("--models", default="fable,gpt")
    ap.add_argument("--gpt-model", default="gpt-5.5")
    ap.add_argument("--report-model", default="claude-fable-5",
                    help="model for the synthesis report (proven default)")
    ap.add_argument("--no-test", action="store_true")
    ap.add_argument("--resume", action="store_true",
                    help="continue an existing run-id: skip lessons/tests already recorded")
    ap.add_argument("--synthesize-only", action="store_true",
                    help="skip all walks; just (re)build the report from an existing run-id")
    ap.add_argument("--run-id", default=None)
    a = ap.parse_args()

    keys = load_keys()
    grade = a.grade.lower()
    if not a.cross_grade and grade not in GRADES:
        ap.error(f"--grade must be one of {GRADES} (got {a.grade!r})")
    run_id = a.run_id or ("crossgrade" if a.cross_grade else f"{grade}_run")
    run_dir = os.path.join(OUT_ROOT, run_id)

    # composition ids for the report evidence (union across grades for cross-grade)
    if a.cross_grade:
        comp_ids = set()
        for g in CROSS_GRADE_SEQUENCE:
            comp_ids |= _comp_ids(load_lessons(g))
        report_grade = "crossgrade"
    else:
        comp_ids = _comp_ids(load_lessons(grade))
        report_grade = grade

    # --synthesize-only: no walks, no spend on students; just rebuild the report from disk.
    if a.synthesize_only:
        if not os.path.isdir(run_dir):
            ap.error(f"--synthesize-only: run dir does not exist: {run_dir}")
        if not keys["anthropic"]:
            ap.error("--synthesize-only needs ANTHROPIC_API_KEY (for the report model).")
        print(f"Synthesizing report from {run_dir} ...")
        _write_report(run_dir, keys["anthropic"], a.report_model, report_grade, comp_ids, a.cross_grade)
        return

    personas = build_personas("g9" if a.cross_grade else grade)
    persona_ids = [p.strip() for p in a.personas.split(",") if p.strip()]
    unknown = [p for p in persona_ids if p not in personas]
    if unknown:
        ap.error(f"unknown persona(s): {', '.join(unknown)}. Known: {', '.join(sorted(personas))}")

    model_names = [m.strip() for m in a.models.split(",") if m.strip()]
    unknown_m = [m for m in model_names if m not in KNOWN_MODELS]
    if unknown_m:
        ap.error(f"unknown model(s): {', '.join(unknown_m)}. Known: {', '.join(KNOWN_MODELS)}")

    # KEY PREFLIGHT: fail before spending a cent if a requested model's key is missing.
    missing = [m for m in model_names if not _key_for(m, keys)]
    if missing:
        env_name = {"fable": "ANTHROPIC_API_KEY", "gpt": "OPEN_AI_API_KEY"}
        ap.error("missing API key(s) for requested model(s): "
                 + "; ".join(f"{m} needs {env_name[m]}" for m in missing)
                 + ". Set them in HS Writing/.env or drop the model from --models.")
    if not keys["anthropic"]:
        ap.error("ANTHROPIC_API_KEY is required for the synthesis report (--report-model).")

    # RUN-DIR GUARD: refuse to overwrite an existing run unless --resume.
    if os.path.isdir(run_dir):
        import glob as _glob
        existing = _glob.glob(os.path.join(run_dir, "journal_*.jsonl"))
        if existing and not a.resume:
            ap.error(f"run-id '{run_id}' already has {len(existing)} journal file(s) in {run_dir}. "
                     f"Use a fresh --run-id, or --resume to continue, or --synthesize-only to rebuild the report.")
    os.makedirs(run_dir, exist_ok=True)

    if a.cross_grade:
        # ONE student per (persona,model) walks all grades on a single spanning journal.
        print(f"CROSS-GRADE run: {run_dir}  |  personas={persona_ids}  models={model_names}  resume={a.resume}")
        for persona_id in persona_ids:
            for model_name in model_names:
                tag = f"{persona_id}_{model_name}"
                jstore = JournalStore(os.path.join(run_dir, f"journal_{tag}.jsonl"))
                seq_offset = 0
                for g in CROSS_GRADE_SEQUENCE:
                    lessons = load_lessons(g)
                    if a.limit:
                        lessons = lessons[:a.limit]
                    print(f"WALK: {persona_id} x {model_name} -> {g} ({len(lessons)} lessons)")
                    run_walk(persona_id, model_name, lessons, run_dir, keys, a.gpt_model,
                             not a.no_test, a.resume, personas, GRADE_LABELS[g], g,
                             tag=tag, jstore=jstore, seq_offset=seq_offset)
                    seq_offset += len(lessons)
    else:
        lessons = load_lessons(grade)
        if a.limit:
            lessons = lessons[:a.limit]
        print(f"Run dir: {run_dir}  |  grade={grade}  lessons: {len(lessons)}  resume={a.resume}")
        for persona_id in persona_ids:
            for model_name in model_names:
                print(f"WALK: {persona_id} x {model_name}")
                run_walk(persona_id, model_name, lessons, run_dir, keys, a.gpt_model,
                         not a.no_test, a.resume, personas, GRADE_LABELS[grade], grade)

    print("Synthesizing report...")
    _write_report(run_dir, keys["anthropic"], a.report_model, report_grade, comp_ids, a.cross_grade)


if __name__ == "__main__":
    main()
