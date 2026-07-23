"""
player_test/grading_check.py  -  evaluate GRADING OUTCOMES for a lesson's PP100 mastery FRQ.

Full-scope eval (Noel 2026-07-23): confirm a real response to the lesson's mastery task returns a real,
non-zero, correctly-scaled score through the SAME grader URL the live item is wired to (rubric + grain +
frq_type + mode baked in). We read the grader URL off the LIVE item (so we test exactly what a student hits),
POST a mode-appropriate exemplar response, and assert a numeric score in (0, maxScore].

This is a DIRECT grader-endpoint check (the wired URL), which is what the runtime calls server-side. It does
NOT drive a full student-runtime submission (that needs an authenticated student session); the direct call
mirrors the ExternalApiScore the runtime performs. Never raises; a grader/network error is a 'fail' finding.
"""
from __future__ import annotations
import os, sys, re, json, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.dirname(HERE)
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)
from player_test.checks import Finding

# mode-appropriate exemplar responses by grain (a genuine, rubric-passing answer)
_SENT = "Schools should ban phones during class, because constant notifications pull attention from learning."
_PARA = ("Cities should charge congestion tolls because traffic imposes real costs on everyone. When drivers "
         "pay for peak use, some shift their trips and the roads clear for those who truly need them, and the "
         "revenue can fund buses that give lower-income riders a faster option.")
_ESSAY = ("Schools should ban phones during the school day because constant notifications fracture the sustained "
          "attention learning requires. A buzz pulls a glance and the lesson thread breaks; refocusing takes "
          "minutes, so even quick checks cost the whole class. Some cite emergencies, but a front-office contact "
          "system answers that without a distraction in every pocket. A whole-day ban protects the deep focus "
          "real learning needs.")
_ANALYSIS = ("Douglass repeats the word your so his celebrating audience feels the holiday as theirs alone; the "
             "pronoun that should include becomes a wall, so the reader confronts the exclusion structurally "
             "before he names it.")


def _exemplar(grain: str, mode: str) -> str:
    if grain == "sentence":
        return _SENT
    if "paragraph" in grain:
        return _PARA
    return _ANALYSIS if mode == "analysis" else _ESSAY


def _live_grader_url(session, item_id: str) -> str:
    """Read the wired grader URL off the LIVE mastery FRQ item (the exact URL the runtime would call)."""
    QTI = "https://qti.alpha-1edtech.ai/api"
    r = session.get(f"{QTI}/assessment-items/{item_id}", timeout=30)
    if r.status_code != 200:
        return ""
    m = re.search(r"https://[^\"\\<>\s]*?/score\?[a-zA-Z0-9=&_%]*", r.text)
    return m.group(0) if m else ""


def check_grading(exp: dict, session) -> list:
    """Submit an exemplar response to the lesson's wired grader URL and assert a real score returns."""
    import requests
    lid, g = exp["lesson_id"], exp["grade"]
    frq_id = exp["mastery_frq_id"]
    url = _live_grader_url(session, frq_id)
    if not url:
        return [Finding(lid, g, "grading", "fail", "wired grader URL on the live FRQ", "no /score URL found on item")]
    # infer grain + mode from the URL params (they were baked in at wire time)
    grain = (re.search(r"grain=(\w+)", url) or [None, "essay"])[1]
    mode = (re.search(r"mode=(\w+)", url) or [None, ""])[1]
    rubric = "rc.4trait" if g in ("G11", "G12") else "rc.staar"
    body = {"response": _exemplar(grain, mode), "rubric": rubric,
            "grade": "11" if rubric == "rc.4trait" else "9",
            "prompt": exp["title"], "passage": ""}
    try:
        r = requests.post(url, json=body, timeout=90)
        d = r.json()
    except Exception as e:
        return [Finding(lid, g, "grading", "fail", "grader returns a score", f"{type(e).__name__}: {e}")]
    sc, mx = d.get("score"), d.get("maxScore")
    ok = (r.status_code == 200 and isinstance(sc, (int, float)) and isinstance(mx, (int, float))
          and mx > 0 and sc > 0)
    return [Finding(lid, g, "grading", "pass" if ok else "fail",
                    f"non-zero score /{mx if isinstance(mx,(int,float)) else '?'} ({rubric} {grain}{'/'+mode if mode else ''})",
                    f"{sc}/{mx} [{r.status_code}] {(d.get('note') or d.get('detail') or '')[:60]}")]
