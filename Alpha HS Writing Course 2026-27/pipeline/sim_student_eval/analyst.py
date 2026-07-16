# pipeline/sim_student_eval/analyst.py
"""Synthesis pass. Reads all four course-walks' journals + transcripts + test logs, runs a
deterministic redundancy pre-pass (from felt_repeated), then asks Claude to write the report
answering the four curriculum questions. Findings are corroboration-labeled; nothing is scored."""
import os, json, glob


def gather(run_dir: str) -> dict:
    out = {"walks": {}, "tests": {}}
    for f in glob.glob(os.path.join(run_dir, "journal_*.jsonl")):
        key = os.path.basename(f)[len("journal_"):-len(".jsonl")]  # persona_model
        out["walks"].setdefault(key, {})["journal"] = [json.loads(l) for l in open(f, encoding="utf-8") if l.strip()]
    for f in glob.glob(os.path.join(run_dir, "transcript_*.jsonl")):
        key = os.path.basename(f)[len("transcript_"):-len(".jsonl")]
        out["walks"].setdefault(key, {})["transcript"] = [json.loads(l) for l in open(f, encoding="utf-8") if l.strip()]
    for f in glob.glob(os.path.join(run_dir, "test_*.json")):
        key = os.path.basename(f)[len("test_"):-len(".json")]
        out["tests"][key] = json.load(open(f, encoding="utf-8"))
    return out


def detect_redundancies(gathered: dict) -> list:
    groups = {}
    for walk_key, data in gathered["walks"].items():
        for entry in data.get("journal", []):
            fr = entry.get("felt_repeated")
            if fr and fr.get("echoes_lesson"):
                k = (entry["lesson"], fr["echoes_lesson"])
                groups.setdefault(k, {"lesson": entry["lesson"], "echoes_lesson": fr["echoes_lesson"],
                                      "what": fr.get("what", ""), "raised_by": []})
                groups[k]["raised_by"].append(walk_key)
    rows = list(groups.values())
    for r in rows:
        models = {w.split("_")[-1] for w in r["raised_by"]}
        personas = {w.rsplit("_", 1)[0] for w in r["raised_by"]}
        r["corroboration"] = ("CORROBORATED (cross-model)" if len(models) > 1 else
                              "CORROBORATED (cross-persona)" if len(personas) > 1 else "SINGLE")
    return sorted(rows, key=lambda r: -len(r["raised_by"]))


_REPORT_TOOL = {
    "name": "write_report",
    "description": "Write the curriculum-evaluation report sections.",
    "input_schema": {"type": "object", "properties": {
        "makes_sense": {"type": "string", "description": "Q1 findings: per-lesson clarity, specific confusion points with lesson+step. Markdown."},
        "redundancies": {"type": "string", "description": "Q2 findings: corroborated redundancy list, each with the two lessons + which walks flagged it. Markdown."},
        "composition_readiness": {"type": "string", "description": "Q3: for each composition probe (l18/l23/l24/l26/l27), which skills were/weren't in place, traced to lessons. Markdown."},
        "test_readiness": {"type": "string", "description": "Q4: items students couldn't attempt + missing-skill trace; MCQ match rates as context. Markdown."},
        "top_findings": {"type": "string", "description": "The 5-10 most severe findings, ranked, each traceable to a student utterance. Markdown."}},
        "required": ["makes_sense", "redundancies", "composition_readiness", "test_readiness", "top_findings"]}}


def _build_evidence(gathered: dict, redundancies: list) -> str:
    parts = ["DETERMINISTIC REDUNDANCY TABLE (from students' own felt_repeated flags):"]
    for r in redundancies:
        parts.append(f"- {r['lesson']} felt like a repeat of {r['echoes_lesson']} ({r['corroboration']}; raised by {', '.join(r['raised_by'])}): {r['what']}")
    for wk, data in gathered["walks"].items():
        parts.append(f"\n===== WALK: {wk} =====")
        for e in data.get("journal", []):
            parts.append(f"[{e['lesson']}] can_do={e.get('skills_i_can_now_do')}; struggled={e.get('where_i_struggled')}; open={e.get('open_questions')}; conf={e.get('confidence')}")
        for t in data.get("transcript", []):
            if any(t["lesson"].startswith(p) for p in ("g9_l18", "g9_l23", "g9_l24", "g9_l26", "g9_l27")):
                parts.append(f"[COMPOSITION {t['lesson']}] response: {t['response'][:1200]}")
    for tk, tr in gathered["tests"].items():
        na = [a for a in tr["attempts"] if not a["can_attempt"]]
        parts.append(f"\n===== TEST {tk} ===== mcq {tr['mcq_scored']}; cannot-attempt {len(na)}: " +
                     "; ".join(f"{a['id']}:{a['missing_skill']}" for a in na[:20]))
    return "\n".join(parts)[:120000]


def synthesize(run_dir: str, anthropic_key: str, model: str = "claude-opus-4-8") -> str:
    import anthropic
    gathered = gather(run_dir)
    redundancies = detect_redundancies(gathered)
    evidence = _build_evidence(gathered, redundancies)
    prompt = (
        "You are an instructional-design analyst. Four simulated 9th-grade students (two personas: "
        "on-grade average and high-achiever; each run once by Fable-5 and once by GPT) walked the "
        "G9 writing course in order, carrying a running memory. Below is their evidence. Write a "
        "curriculum evaluation answering four questions: (1) do the lessons make sense? (2) are there "
        "redundancies? (3) do the lessons prepare students for the full compositions? (4) do they "
        "prepare students for the tests?\n\n"
        "RULES: Every finding must be specific and cite a lesson (and step if possible) and the walk "
        "that raised it. Label redundancy/readiness findings CORROBORATED (raised across models or "
        "personas) vs PERSONA-SPECIFIC vs SINGLE-MODEL. Do NOT invent findings not in the evidence. "
        "Do NOT score writing. NO em dashes anywhere (use commas, colons, parentheses). Be blunt and "
        "concrete, never generic.\n\n" + evidence)
    c = anthropic.Anthropic(api_key=anthropic_key)
    r = c.messages.create(model=model, max_tokens=6000, tools=[_REPORT_TOOL],
                          tool_choice={"type": "tool", "name": "write_report"},
                          messages=[{"role": "user", "content": prompt}])
    rep = {}
    for b in r.content:
        if getattr(b, "type", "") == "tool_use":
            rep = b.input
    md = ["# Simulated-Student Curriculum Evaluation - G9 Pilot", "",
          "> Signal, not proof. Four simulated students are a design signal to investigate, "
          "NOT field evidence of efficacy. No writing was scored (grading is not yet wired); "
          "findings are the students' lived experience plus deterministic multiple-choice matches.", "",
          "## Most severe findings (ranked)", "", rep.get("top_findings", "(none)"), "",
          "## 1. Do the lessons make sense?", "", rep.get("makes_sense", ""), "",
          "## 2. Are there redundancies?", "", rep.get("redundancies", ""), "",
          "## 3. Do the lessons prepare them for the full compositions?", "", rep.get("composition_readiness", ""), "",
          "## 4. Do the courses prepare them for the tests?", "", rep.get("test_readiness", "")]
    return "\n".join(md)
