"""
native_vs_render_harness.py  -  offline comparison: authored NATIVE prompt (via direct Anthropic) vs the live
Render /score, optionally vs the corpus's official human score.

WHY OFFLINE: the live native grader (alphatest.alpha.school/prod/ai-grading) is server-invoked only (direct
POST 405; a real native score needs an enrolled-student submit). So we validate the AUTHORED native prompt by
running it through the SAME model the Render grader uses (Opus 4.8, Anthropic-direct) and comparing behavior.
This is the fidelity proof we can get without the enrolled session; the enrolled run later confirms the
platform runs the prompt as expected.

WHAT IT MEASURES per grain, on a corpus of {passage, prompt, response, official_score?}:
  - native score (authored prompt -> model -> parsed JSON total, normalized to a common % of scale)
  - render score (POST /score with the route's grain/frq_type/mode -> total/maxScore)
  - |native - render| agreement (mean abs %-of-scale delta), signed bias (native - render),
    Spearman rank correlation, and (if official scores present) each grader's delta vs official.
Both graders are temperature=1, so each score is a MEDIAN of N runs (default 3) to damp variance.

USAGE:
  python native_vs_render_harness.py --grain sentence  --n 3 --limit 12
  python native_vs_render_harness.py --grain paragraph --corpus mcas  --n 3
  python native_vs_render_harness.py --grain essay --rubric rc.staar --corpus staar --n 3 --limit 15
  python native_vs_render_harness.py --grain essay --rubric rc.4trait --mode argument --corpus regents

Requires ANTHROPIC_API_KEY (funded) in ../../../.env and network to the Render grader. Read-only vs Render.
"""
from __future__ import annotations
import os, sys, json, re, argparse, statistics, warnings
warnings.filterwarnings("ignore")
try:                                        # Windows console defaults to cp1252; force UTF-8 for output
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)                                   # native_prompts*
PIPE = os.path.join(HERE, "..")
sys.path.insert(0, PIPE)
ROOT = os.path.join(PIPE, "..")

import native_prompts as NP
import native_prompts_long as NPL

RENDER_URL = os.environ.get("RENDER_GRADER_URL", "https://hs-writing-grading.onrender.com/score")
CORPUS_DIR = os.path.abspath(os.path.join(
    ROOT, "..", "..", "Writing_Test_Grader", "Grading Standards Documentation", "CCSS_G910"))
_MODEL = None
_CLIENT = None


def _load_env():
    # OVERRIDE for the funded key: a stale shell ANTHROPIC_API_KEY (unfunded) otherwise shadows the .env one
    # (setdefault gotcha -> "credit balance too low" while Render, which uses its own service key, works).
    _OVERRIDE = {"ANTHROPIC_API_KEY", "ANTHROPIC_PROVIDER", "ALPHA_PANEL_MODEL", "ANTHROPIC_MODEL"}
    envp = os.path.join(ROOT, "..", ".env")
    if os.path.exists(envp):
        for line in open(envp, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                k = k.strip(); v = v.strip().strip('"').strip("'")
                if k in _OVERRIDE:
                    os.environ[k] = v
                else:
                    os.environ.setdefault(k, v)
    os.environ.setdefault("ANTHROPIC_PROVIDER", "anthropic")


def _client():
    global _CLIENT, _MODEL
    if _CLIENT is None:
        import anthropic
        _CLIENT = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        _MODEL = os.environ.get("ALPHA_PANEL_MODEL", "claude-opus-4-8")
    return _CLIENT, _MODEL


def _parse_json(text: str) -> dict | None:
    """Same defensive parse the grader uses: direct -> strip fences -> brace-balanced scan for total_score."""
    for attempt in (text, re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M)):
        try:
            return json.loads(attempt)
        except Exception:
            pass
    # brace-balanced: prefer the object containing "total_score"
    best = None
    for m in re.finditer(r"\{", text):
        depth = 0
        for i in range(m.start(), len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    blob = text[m.start():i + 1]
                    try:
                        obj = json.loads(blob)
                        if "total_score" in obj:
                            return obj
                        best = best or obj
                    except Exception:
                        pass
                    break
    return best


# ---- native grader (authored prompt -> direct model) ------------------------

def native_score_once(spec: dict, passage: str, question: str, response: str,
                       grade_hint="9-10", mode_hint="argumentative") -> dict | None:
    client, model = _client()
    prompt = spec["prompt"]
    prompt = prompt.replace("<<<JSONOPEN>>>", "{").replace("<<<JSONCLOSE>>>", "}")
    prompt = prompt.replace("{{grade_hint}}", grade_hint).replace("{{mode_hint}}", mode_hint)
    prompt = prompt.replace("{{passage}}", passage or "(none)")
    prompt = prompt.replace("{{question}}", question or "(none)")
    prompt = prompt.replace("{{response}}", response or "")
    try:
        msg = client.messages.create(
            model=model, max_tokens=3000, temperature=1,
            thinking={"type": "enabled", "budget_tokens": 2000},
            messages=[{"role": "user", "content": prompt}])
    except Exception as e:
        # thinking may be unsupported on some model aliases; retry plain
        try:
            msg = client.messages.create(model=model, max_tokens=3000, temperature=1,
                                         messages=[{"role": "user", "content": prompt}])
        except Exception as e2:
            return {"_error": f"{type(e2).__name__}: {e2}"}
    text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
    obj = _parse_json(text)
    return obj


def native_total(spec, passage, question, response, n, **hints) -> tuple[float | None, float, list]:
    """Median native total over n runs. Returns (median_total, max, per_run_totals)."""
    runs = []
    for _ in range(n):
        obj = native_score_once(spec, passage, question, response, **hints)
        if obj and "total_score" in obj:
            runs.append(float(obj["total_score"]))
    if not runs:
        return None, float(spec["scale"]), []
    return statistics.median(runs), float(spec["scale"]), runs


# ---- render grader (live /score) --------------------------------------------

def render_score_once(grain, frq_type, mode, rubric, passage, question, response, grade) -> dict | None:
    import requests
    params = []
    if grain in ("sentence", "paragraph"):
        params.append(f"grain={grain}"); params.append(f"frq_type={frq_type or 'writing'}")
    if mode and rubric == "rc.4trait":
        params.append(f"mode={mode}")
    url = RENDER_URL + (("?" + "&".join(params)) if params else "")
    body = {"response": response, "rubric": rubric, "grade": grade,
            "prompt": question or "(prompt not supplied)", "passage": passage or ""}
    if mode and rubric == "rc.sbac":
        body["mode"] = mode
    try:
        r = requests.post(url, json=body, timeout=150, verify=False)
        if r.status_code == 200:
            return r.json()
        return {"_error": f"HTTP {r.status_code}: {(r.text or '')[:120]}"}
    except Exception as e:
        return {"_error": f"{type(e).__name__}: {e}"}


def render_total(grain, frq_type, mode, rubric, passage, question, response, grade, n) -> tuple[float | None, float, list]:
    runs = []; mx = None
    for _ in range(n):
        obj = render_score_once(grain, frq_type, mode, rubric, passage, question, response, grade)
        if obj and "score" in obj and "_error" not in obj:
            runs.append(float(obj["score"])); mx = float(obj["maxScore"])
    if not runs:
        return None, mx or 1.0, []
    return statistics.median(runs), mx, runs


# ---- corpus loaders ---------------------------------------------------------

def _corpus(name: str) -> list[dict]:
    """Return [{passage, question, response, official_pct, scale_note}] for a named corpus."""
    _FILE = {"staar": "staar_g910_groundtruth.json", "mcas": "mcas_g10_groundtruth.json",
             "regents": "regents_g1112_groundtruth.json", "sbac": "sbac_g11_groundtruth.json"}
    path = os.path.join(CORPUS_DIR, _FILE.get(name, "")) if name in _FILE else None
    if not path or not os.path.exists(path):
        raise SystemExit(f"corpus '{name}' not found at {path}")
    rows = json.load(open(path, encoding="utf-8"))
    if isinstance(rows, dict):
        rows = rows.get("cases") or rows.get("records") or next(iter(rows.values()))
    out = []
    for r in rows:
        essay = r.get("essay") or r.get("response") or ""
        if not essay:
            continue
        if name == "staar":
            off = r.get("total"); mx = r.get("total_max") or 5
        elif name == "mcas":
            off = r.get("idea_dev_score"); mx = r.get("idea_dev_max") or 5
        elif name == "regents":
            off = r.get("official_level"); mx = r.get("level_max") or 6
        elif name == "sbac":
            off = r.get("total"); mx = r.get("total_max") or 10
        official_pct = (float(off) / float(mx)) if (off is not None and mx) else None
        out.append({"passage": r.get("passage", ""), "question": r.get("prompt", ""),
                    "response": essay, "official_pct": official_pct,
                    "task": r.get("task") or r.get("part") or ""})
    return out


# ---- spearman (no scipy) ----------------------------------------------------

def _spearman(xs, ys):
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    if len(pairs) < 3:
        return None
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        rk = [0.0] * len(v)
        i = 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                rk[order[k]] = avg
            i = j + 1
        return rk
    xr, yr = ranks([p[0] for p in pairs]), ranks([p[1] for p in pairs])
    n = len(pairs)
    d2 = sum((a - b) ** 2 for a, b in zip(xr, yr))
    return 1 - (6 * d2) / (n * (n * n - 1))


# ---- main comparison --------------------------------------------------------

def _sentence_cases(frq_type):
    """Build corpus-shaped cases from the hand-authored sentence probe set (no real scored corpus exists).
    official_pct here is the PREDICTED band midpoint (construct validity, not an official score)."""
    import sentence_probes as SP
    if frq_type == "revision":
        prompt, probes, scale = SP.REVISION_PROMPT, SP.REVISION_PROBES, 2
    else:
        prompt, probes, scale = SP.WRITING_PROMPT, SP.WRITING_PROBES, 3
    out = []
    for p in probes:
        lo, hi = p["expect"]
        out.append({"passage": SP.PASSAGE, "question": prompt, "response": p["response"],
                    "official_pct": ((lo + hi) / 2.0) / scale, "task": p["why"][:22]})
    return out


def run(grain, rubric, mode, frq_type, corpus, n, limit, grade):
    _load_env()
    if grain == "sentence":
        spec = NP.SENTENCE_SPECS[("sentence", frq_type)]
    elif grain == "paragraph":
        spec = NPL.PARAGRAPH
    else:  # essay
        spec = (NPL.ESSAY_STAAR if rubric in ("rc.staar", "rc.sbac")
                else NPL.ESSAY_4TRAIT_ANALYSIS if mode == "analysis" else NPL.ESSAY_4TRAIT_ARGUMENT)
    if grain == "sentence" and not corpus:
        cases = _sentence_cases(frq_type)[:limit]
    else:
        cases = _corpus(corpus)[:limit] if corpus else []
    if not cases:
        raise SystemExit("no cases; pass --corpus for paragraph/essay (sentence uses the probe set if no --corpus)")
    mode_hint = "analysis" if mode == "analysis" else "argumentative" if rubric != "rc.4trait" else "argument"
    rows = []
    print(f"grain={grain} rubric={rubric} mode={mode or '-'} corpus={corpus} n={n} cases={len(cases)} "
          f"native_spec={spec['id']} model={os.environ.get('ALPHA_PANEL_MODEL','claude-opus-4-8')}")
    for i, c in enumerate(cases, 1):
        nat, nmax, nruns = native_total(spec, c["passage"], c["question"], c["response"], n,
                                        grade_hint=str(grade), mode_hint=mode_hint)
        ren, rmax, rruns = render_total(grain, frq_type, mode, rubric, c["passage"], c["question"],
                                        c["response"], grade, n)
        nat_pct = (nat / nmax) if nat is not None else None
        ren_pct = (ren / rmax) if ren is not None else None
        rows.append({"i": i, "native_pct": nat_pct, "render_pct": ren_pct,
                     "official_pct": c["official_pct"], "native_runs": nruns, "render_runs": rruns,
                     "task": c["task"]})
        d = (abs(nat_pct - ren_pct) * 100) if (nat_pct is not None and ren_pct is not None) else None
        print(f"  [{i:2}] native={_p(nat_pct)} render={_p(ren_pct)} official={_p(c['official_pct'])}"
              f" |d(nat-ren)|={f'{d:.0f}%' if d is not None else '  -'}  {c['task'][:22]}", flush=True)
    _summary(rows)
    return rows


def _p(x):
    return f"{x*100:4.0f}%" if x is not None else "  - "


def _summary(rows):
    both = [(r["native_pct"], r["render_pct"]) for r in rows if r["native_pct"] is not None and r["render_pct"] is not None]
    print("\n=== SUMMARY (all as % of each grader's own scale) ===")
    print(f"  scored by BOTH: {len(both)}/{len(rows)}")
    if both:
        deltas = [abs(a - b) for a, b in both]
        signed = [a - b for a, b in both]      # native - render
        print(f"  mean |native-render|:  {statistics.mean(deltas)*100:.1f}%")
        print(f"  signed bias (nat-ren): {statistics.mean(signed)*100:+.1f}%  (>0 = native scores higher)")
        print(f"  within 10%: {sum(1 for d in deltas if d<=0.10)}/{len(both)}   within 20%: {sum(1 for d in deltas if d<=0.20)}/{len(both)}")
        rho = _spearman([a for a, b in both], [b for a, b in both])
        if rho is not None:
            print(f"  Spearman rank corr (native vs render): {rho:.2f}")
    off = [(r["native_pct"], r["render_pct"], r["official_pct"]) for r in rows if r["official_pct"] is not None]
    off_n = [(n, o) for n, r, o in off if n is not None]
    off_r = [(r, o) for n, r, o in off if r is not None]
    if off_n and off_r:
        print(f"  vs OFFICIAL (n={len(off)}): native |Δ|={statistics.mean(abs(n-o) for n,o in off_n)*100:.1f}%"
              f"  render |Δ|={statistics.mean(abs(r-o) for r,o in off_r)*100:.1f}%")
        rn = _spearman([n for n, o in off_n], [o for n, o in off_n])
        rr = _spearman([r for r, o in off_r], [o for r, o in off_r])
        print(f"  rank corr vs official: native {rn if rn is None else round(rn,2)}  render {rr if rr is None else round(rr,2)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--grain", required=True, choices=["sentence", "paragraph", "essay"])
    ap.add_argument("--rubric", default="rc.staar")
    ap.add_argument("--mode", default="")            # argument|analysis (4trait) or argumentative|explanatory
    ap.add_argument("--frq_type", default="writing") # sentence: writing|revision
    ap.add_argument("--corpus", default="")          # staar|mcas|regents|sbac
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--limit", type=int, default=12)
    ap.add_argument("--grade", type=int, default=10)
    a = ap.parse_args()
    run(a.grain, a.rubric, a.mode, a.frq_type, a.corpus, a.n, a.limit, a.grade)
