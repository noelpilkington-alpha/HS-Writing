"""
tier_b_judge.py  -  Tier B: make the LLM judges trustworthy BEFORE they can block (B1/B5/B6/B7).

Tier A is the deterministic floor. Tier B adds the SEMANTIC judges (the defects no gate can catch:
also-correct distractors, planner/grain mismatch, phantom-draft diagnosis). The whole risk of an LLM
judge is that it rots - goes blind (misses real defects) or over-flags (re-litigates deliberate
design, the documented Fable failure mode). So a judge does NOT get to block until it has EARNED it.

This module implements four things from PIPELINE_RELIABILITY_PROPOSAL.md, all pluggable so the harness
is testable offline with deterministic fakes and wired to Fable-5 in production:

  B1  ADVERSARIAL PER-RULE VERIFIER (fail-closed). One verifier per defect rubric, framed to REFUTE a
      pass: it must actively argue the excerpt is CLEAN; if it cannot refute the defect, or is unsure,
      it FLAGS. Isolation (one rule at a time) is why this catches what a holistic pass misses.

  B5  THREE-WAY VERDICT: PASS / FAIL / LOW_CONFIDENCE. Low-confidence routes to a human triage queue,
      never a silent hard-fail - operationalizes the "triage before fixing" rule.

  B6  PROBE-BEFORE-BLOCK. A judge is scored on the labeled calibration corpus (judge_calibration) and
      only clears if recall AND precision meet the bar. A judge that has not been probed CANNOT block.

  B7  N-CONSECUTIVE-GREEN PROMOTION + KILL-SWITCH. A judge earns autonomous block authority only after
      N straight clean probe runs, recorded in a ledger file; a kill-switch file demotes a drifting
      judge instantly without a code change. Deterministic - no LLM needed to build or test.

The judge callable contract (same as judge_calibration): judge_fn(excerpt, rubric) -> bool  (True=flag).
"""
from __future__ import annotations
import os, json, sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)

from judge_calibration import score_judge, CALIBRATION_CASES  # noqa: E402

# ---- verdict constants (B5) ----
PASS = "pass"
FAIL = "fail"
LOW_CONFIDENCE = "low_confidence"    # -> human triage queue, NOT a silent hard-fail

# ---- promotion policy (B6/B7) ----
PROMOTE_AFTER_N_GREEN = 3            # N consecutive clean probe runs before block authority
RECALL_BAR = 1.0                     # must catch EVERY labeled defect (a blind judge is worthless)
PRECISION_BAR = 1.0                  # must pass EVERY fixed excerpt (an over-flagger is worse than none)

_LEDGER = os.path.join(HERE, ".tier_b_promotion.json")     # {judge_name: {"green_streak": n, "history": [...]}}
_KILLSWITCH = os.path.join(HERE, ".tier_b_killswitch")     # presence of judge_name in this file = demoted


# ---------------------------------------------------------------------------
# B1: adversarial per-rule verifier (fail-closed), wrapping a raw model judge
# ---------------------------------------------------------------------------

# The fail-closed framing appended to a rubric so the model must REFUTE a pass and defaults to FLAG.
_ADVERSARIAL_FRAME = (
    "\n\nYou are an ADVERSARIAL verifier. Your job is to try to REFUTE the claim that this excerpt is "
    "clean on the rule above. Actively look for the defect. Answer has_defect=true if the defect is "
    "present OR if you cannot confidently rule it out. Only answer has_defect=false if you can "
    "positively establish the excerpt does NOT have this defect. When genuinely uncertain, flag it."
)


def adversarial_rubric(rubric: str) -> str:
    """B1: turn a plain rule into a fail-closed adversarial prompt (refute-the-pass, default-to-flag)."""
    return rubric.strip() + _ADVERSARIAL_FRAME


def make_adversarial_verifier(raw_judge_fn):
    """Wrap a raw judge callable so every call uses the fail-closed adversarial framing. Returns a
    judge_fn(excerpt, rubric) -> bool with the same contract, safe to pass to score_judge/probe."""
    def verifier(excerpt: str, rubric: str) -> bool:
        return bool(raw_judge_fn(excerpt, adversarial_rubric(rubric)))
    return verifier


# ---------------------------------------------------------------------------
# B5: three-way verdict from N independent adversarial votes
# ---------------------------------------------------------------------------

def three_way_verdict(votes) -> str:
    """Aggregate N boolean adversarial votes (True=flag) into PASS / FAIL / LOW_CONFIDENCE.
      - unanimous flag        -> FAIL
      - unanimous clean       -> PASS
      - split                 -> LOW_CONFIDENCE (route to human triage; never a silent hard-fail)
    Requires >=1 vote. With a single vote there is no split signal, so a lone flag is LOW_CONFIDENCE
    (a single model asserting a defect is a triage trigger, not an automatic block) and a lone clean is
    PASS (nothing to escalate)."""
    votes = [bool(v) for v in votes]
    if not votes:
        return LOW_CONFIDENCE
    flags = sum(votes)
    if flags == 0:
        return PASS
    if flags == len(votes):
        return FAIL if len(votes) >= 2 else LOW_CONFIDENCE
    return LOW_CONFIDENCE


def verdict_for(excerpt: str, rubric: str, verifiers) -> str:
    """Run a panel of adversarial verifiers on one excerpt/rubric and return the three-way verdict."""
    return three_way_verdict([v(excerpt, rubric) for v in verifiers])


# ---------------------------------------------------------------------------
# B6: probe a judge's precision/recall on the labeled corpus BEFORE it can block
# ---------------------------------------------------------------------------

def probe(judge_fn) -> dict:
    """Score judge_fn against the calibration answer key. Returns the score dict + `clears` (bool):
    True iff recall >= RECALL_BAR and precision >= PRECISION_BAR. A judge that has not cleared a probe
    is NOT allowed to block (enforced by can_block)."""
    res = score_judge(judge_fn)
    res["clears"] = (res["recall"] >= RECALL_BAR and res["precision"] >= PRECISION_BAR)
    return res


# ---------------------------------------------------------------------------
# B7: N-consecutive-green promotion ledger + kill-switch (deterministic)
# ---------------------------------------------------------------------------

def _read_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError):
        return default


def _killed(judge_name, killswitch_path=_KILLSWITCH) -> bool:
    """A judge is demoted if its name appears (one per line) in the kill-switch file."""
    if not os.path.exists(killswitch_path):
        return False
    try:
        with open(killswitch_path, encoding="utf-8") as fh:
            return any(line.strip() == judge_name for line in fh)
    except OSError:
        return False


def record_probe(judge_name, probe_result, ledger_path=_LEDGER, stamp=None) -> dict:
    """Append a probe result to the promotion ledger and update the green streak. A clearing probe
    increments the streak; a non-clearing probe RESETS it to 0 (one bad run revokes progress). Returns
    the judge's ledger entry. `stamp` is an optional caller-supplied timestamp (scripts have no clock)."""
    ledger = _read_json(ledger_path, {})
    entry = ledger.get(judge_name, {"green_streak": 0, "history": []})
    clears = bool(probe_result.get("clears"))
    entry["green_streak"] = entry["green_streak"] + 1 if clears else 0
    entry["history"].append({"clears": clears, "recall": probe_result.get("recall"),
                             "precision": probe_result.get("precision"), "stamp": stamp})
    entry["history"] = entry["history"][-20:]   # keep the tail bounded
    ledger[judge_name] = entry
    with open(ledger_path, "w", encoding="utf-8") as fh:
        json.dump(ledger, fh, indent=1)
    return entry


def can_block(judge_name, ledger_path=_LEDGER, killswitch_path=_KILLSWITCH) -> bool:
    """B6+B7 gate: is this judge allowed to BLOCK (hard-fail) autonomously right now?
    True iff it is NOT kill-switched AND has >= PROMOTE_AFTER_N_GREEN consecutive clean probe runs.
    Until then its verdicts are advisory (route FAILs to triage, do not hard-block)."""
    if _killed(judge_name, killswitch_path):
        return False
    entry = _read_json(ledger_path, {}).get(judge_name, {})
    return entry.get("green_streak", 0) >= PROMOTE_AFTER_N_GREEN


def authority_for(judge_name, verdict, ledger_path=_LEDGER, killswitch_path=_KILLSWITCH) -> str:
    """Map a raw three-way verdict to an ENFORCED action given the judge's earned authority:
      - a promoted judge's FAIL is a real BLOCK; its LOW_CONFIDENCE still routes to triage.
      - an un-promoted (or kill-switched) judge's FAIL is DOWNGRADED to triage (advisory), never a
        silent auto-block. PASS is always PASS.
    Returns one of: 'block' | 'triage' | 'pass'."""
    if verdict == PASS:
        return "pass"
    if verdict == FAIL and can_block(judge_name, ledger_path, killswitch_path):
        return "block"
    return "triage"     # FAIL-without-authority or LOW_CONFIDENCE -> human queue


# ---------------------------------------------------------------------------
# live wiring (production): a Fable-5 adversarial verifier
# ---------------------------------------------------------------------------

def make_live_adversarial_verifier():
    """The production B1 verifier: Fable-5 wrapped in the fail-closed adversarial frame. None offline."""
    from judge_calibration import make_live_judge
    raw = make_live_judge()
    if raw is None:
        return None
    return make_adversarial_verifier(raw)


def main():
    """Probe the live Fable adversarial verifier against the calibration key and record it in the
    ledger. Needs the .env key; offline it explains the state. Never echoes the key."""
    print("=== TIER B: probe the adversarial judge before granting block authority ===")
    v = make_live_adversarial_verifier()
    if v is None:
        print("(no ANTHROPIC_API_KEY in .env - offline; cannot probe the live judge)")
        print(f"promotion policy: {PROMOTE_AFTER_N_GREEN} consecutive clean probes, "
              f"recall>={RECALL_BAR}, precision>={PRECISION_BAR}")
        return 0
    res = probe(v)
    for c in res["cases"]:
        ok = c["flagged_before"] and c["passed_after"]
        print(f"  {'OK ' if ok else '!! '}{c['id']:26} flagged_before={c['flagged_before']}  passed_after={c['passed_after']}")
    print(f"\nrecall={res['recall']:.2f}  precision={res['precision']:.2f}  clears={res['clears']}")
    entry = record_probe("fable_adversarial", res)
    print(f"green_streak={entry['green_streak']}/{PROMOTE_AFTER_N_GREEN}  "
          f"can_block={can_block('fable_adversarial')}")
    return 0 if res["clears"] else 1


if __name__ == "__main__":
    sys.exit(main())
