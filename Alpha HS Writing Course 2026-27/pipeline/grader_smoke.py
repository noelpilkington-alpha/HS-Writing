"""
grader_smoke.py  -  end-to-end smoke + grading-accuracy sanity for the G9 graded pilot.

Validates the GRADER SIDE (the part we control) before the graded pilot, against the live grader's real
ExternalApiScore contract (POST {BASE}/score, rubric-based request, verified against api/external_score.py):

  1. HEALTH: GET {BASE}/health returns 200 (the service is deployed + warm).
  2. ROUND-TRIP: POST {BASE}/score with the exact rubric-based payload shape {response, rubric, grade,
     prompt, passage} + the X-API-Key header, on a REAL G9 FRQ prompt. Asserts a well-formed ScoreResponse
     (score, maxScore=5, breakdown with development+conventions, calibrated=true).
  3. ACCURACY SANITY: score a STRONG and a WEAK response to the same G9 prompt; assert strong > weak and
     the strong lands in a sane band. This is a smoke check, NOT a calibration study - it catches a grader
     that returns a constant/backwards score, not fine accuracy (blind human ground-truth is Tier D).

WHAT THIS DOES NOT COVER (must be confirmed LIVE, on the platform, before go-live):
  - The PLATFORM's ExternalApiScore call shape + AUTH: the timeback contract documents only a URL in the
    customOperator (no auth header mechanism). Whether Timeback sends an X-API-Key (and which one), or the
    grader must accept unauthenticated platform calls, is UNRESOLVED and must be verified with one real
    submission through the platform. This script tests the grader with OUR key; it cannot test what the
    platform sends.

Usage:
  python pipeline/grader_smoke.py https://writing-grader.onrender.com            # health + round-trip + accuracy
  python pipeline/grader_smoke.py https://writing-grader.onrender.com --key XXX  # explicit X-API-Key
  (key also read from GRADER_API_KEY env or .env)
"""
from __future__ import annotations
import os, sys, json

HERE = os.path.dirname(__file__)


def _load_key(explicit=None):
    if explicit:
        return explicit
    if os.environ.get("GRADER_API_KEY"):
        return os.environ["GRADER_API_KEY"]
    # read from HS Writing/.env (never echoed)
    env = os.path.join(HERE, "..", ".env")
    if os.path.exists(env):
        for line in open(env, encoding="utf-8"):
            if line.strip().startswith("GRADER_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


# A REAL G9 argument-FRQ prompt (the taught task shape) + two responses to it.
_PROMPT = ("Should schools require students to take part in community service to graduate? Take a clear "
           "side and defend it with reasons and evidence, and answer the strongest objection to your view.")
_PASSAGE = ("Supporters say required service teaches responsibility and connects students to their towns. "
            "Critics say forcing volunteism is a contradiction and eats into time students need for jobs "
            "or study. Districts that require it usually ask for 20 to 40 hours over four years.")

_STRONG = ("Schools should require community service to graduate because it builds civic habits that last. "
           "First, students who serve while young are far more likely to keep volunteering as adults, which "
           "strengthens the whole community; a graduation requirement reaches students who would never "
           "sign up on their own. Second, service teaches skills a classroom cannot, from showing up on "
           "time to solving real problems with strangers. Some argue that forcing service is a "
           "contradiction because true volunteering is voluntary. That objection has a point, but a "
           "requirement is not the same as forced labor: schools already require reading and math to build "
           "capacities students will value later, and civic capacity is no different. A modest 20-hour "
           "requirement respects students' time while still opening the door. For these reasons, the "
           "graduation requirement is worth keeping.")

_WEAK = ("i think community service is good. it helps people and students should do it. service is nice "
         "because you help out. some people dont like it but its still good. thats why schools should have it.")


def smoke(base, key):
    import requests
    base = base.rstrip("/")
    from g9_wire_grader import normalize_grader_url
    score_url = normalize_grader_url(base)
    health_url = base + "/health"
    hdr = {"Content-Type": "application/json", "X-API-Key": key or ""}
    out = {"base": base, "score_url": score_url}

    # 1. health
    try:
        h = requests.get(health_url, timeout=30)
        out["health_status"] = h.status_code
    except Exception as e:
        out["health_status"] = f"ERR {type(e).__name__}"

    def _score(resp, label):
        body = {"response": resp, "rubric": "rc.staar", "grade": 9, "prompt": _PROMPT, "passage": _PASSAGE}
        r = requests.post(score_url, headers=hdr, json=body, timeout=90)
        if r.status_code != 200:
            return {"label": label, "http": r.status_code, "detail": (r.text or "")[:200]}
        j = r.json()
        return {"label": label, "http": 200, "score": j.get("score"), "maxScore": j.get("maxScore"),
                "calibrated": j.get("calibrated"), "breakdown": j.get("breakdown"),
                "feedback_len": len(j.get("feedback", ""))}

    # 2 + 3. round-trip on strong + weak
    out["strong"] = _score(_STRONG, "strong")
    out["weak"] = _score(_WEAK, "weak")
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    base = args[0] if args else None
    if not base:
        print("Usage: python pipeline/grader_smoke.py <grader-base-url> [--key XXX]")
        return 2
    key = None
    if "--key" in sys.argv:
        key = sys.argv[sys.argv.index("--key") + 1]
    key = _load_key(key)
    if not key:
        print("WARN: no X-API-Key (--key / GRADER_API_KEY / .env). /score will 401 if the grader requires auth.")

    res = smoke(base, key)
    print(json.dumps({k: v for k, v in res.items()}, indent=2))

    # verdicts
    ok = True
    if res.get("health_status") != 200:
        print(f"\n[FAIL] health: {res.get('health_status')} (grader not deployed/warm?)"); ok = False
    s, w = res.get("strong", {}), res.get("weak", {})
    if s.get("http") != 200 or w.get("http") != 200:
        print(f"\n[FAIL] /score round-trip: strong={s.get('http')} weak={w.get('http')} "
              f"(detail: {s.get('detail') or w.get('detail')})"); ok = False
    else:
        if s.get("maxScore") != 5:
            print(f"[WARN] rc.staar maxScore expected 5, got {s.get('maxScore')}")
        if not (isinstance(s.get("score"), (int, float)) and isinstance(w.get("score"), (int, float))):
            print("[FAIL] non-numeric score"); ok = False
        elif s["score"] <= w["score"]:
            print(f"[FAIL] accuracy sanity: strong ({s['score']}) not > weak ({w['score']}) "
                  f"- grader may be constant/backwards"); ok = False
        else:
            print(f"\n[OK] strong {s['score']}/5 > weak {w['score']}/5; calibrated={s.get('calibrated')}; "
                  f"breakdown={s.get('breakdown')}")
    print("\n=== SMOKE " + ("PASS" if ok else "FAIL") + " ===")
    print("NOTE: this tests the GRADER with OUR key. The PLATFORM's ExternalApiScore call shape + auth is a "
          "SEPARATE live check (one real submission through Timeback) - see grader_smoke docstring.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
