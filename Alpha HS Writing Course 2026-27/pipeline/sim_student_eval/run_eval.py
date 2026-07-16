# pipeline/sim_student_eval/run_eval.py
"""Orchestrator: 2 models x 2 personas x 27 G9 lessons + test -> report.
Each (persona, model) is an independent course-walk with its own journal. The next lesson
sees ONLY persona + journal digest + rendered lesson (never prior raw transcripts)."""
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


def _client(model_name, keys, gpt_model):
    if model_name == "fable":
        return FableClient(keys["anthropic"])
    if model_name == "gpt":
        return GptClient(keys["openai"], model=gpt_model)
    raise ValueError(model_name)


def run_walk(persona_id, model_name, lessons, run_dir, keys, gpt_model, do_test):
    persona = PERSONAS[persona_id]
    client = _client(model_name, keys, gpt_model)
    tag = f"{persona_id}_{model_name}"
    jstore = JournalStore(os.path.join(run_dir, f"journal_{tag}.jsonl"))
    tpath = os.path.join(run_dir, f"transcript_{tag}.jsonl")
    for seq, L in enumerate(lessons, 1):
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
        items = load_g9_test_items()
        tres = take_test(client, persona, items, jstore.digest())
        with open(os.path.join(run_dir, f"test_{tag}.json"), "w", encoding="utf-8") as f:
            json.dump(tres, f, ensure_ascii=False, indent=2)
        print(f"  [{tag}] test: mcq {tres['mcq_scored']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="only the first N lessons (smoke)")
    ap.add_argument("--personas", default="average,achiever")
    ap.add_argument("--models", default="fable,gpt")
    ap.add_argument("--gpt-model", default="gpt-5.5")
    ap.add_argument("--no-test", action="store_true")
    ap.add_argument("--run-id", default="g9_pilot")
    a = ap.parse_args()

    persona_ids = [p.strip() for p in a.personas.split(",") if p.strip()]
    unknown = [p for p in persona_ids if p not in PERSONAS]
    if unknown:
        ap.error(f"unknown persona(s): {', '.join(unknown)}. Known: {', '.join(sorted(PERSONAS))}")

    keys = load_keys()
    lessons = load_g9_lessons()
    if a.limit:
        lessons = lessons[:a.limit]
    run_dir = os.path.join(OUT_ROOT, a.run_id)
    os.makedirs(run_dir, exist_ok=True)
    print(f"Run dir: {run_dir}  |  lessons: {len(lessons)}")

    for persona_id in persona_ids:
        for model_name in a.models.split(","):
            print(f"WALK: {persona_id} x {model_name}")
            run_walk(persona_id, model_name.strip(), lessons, run_dir, keys, a.gpt_model, not a.no_test)

    print("Synthesizing report...")
    md = synthesize(run_dir, keys["anthropic"])
    rp = os.path.join(run_dir, "SIM_STUDENT_EVAL_G9.md")
    with open(rp, "w", encoding="utf-8") as f:
        f.write(md)
    print("REPORT:", rp)


if __name__ == "__main__":
    main()
