"""
compound_learning.py  -  Tier C: the defect ledger + compound-learning metric (C1 + C2).

THE LITERAL GOAL of this whole effort (Noel): "our next run can lead to me reviewing courses with no
issues," and reviews get CLEANER over time instead of re-finding the same classes. That only happens
if there is ONE honest number tracking it. This module is that number.

C2 - COMPOUND-LEARNING METRIC. Every defect a HUMAN (or the Council/Fable audit) caught this project
is recorded here as a DefectRecord with HOW it is now covered: a deterministic gate + fixture, a
stimulus/item fixture, or an LLM-judge calibration case. The metric is:

    caught_by_human_not_by_gate  =  defects with NO verified automated coverage

It must trend to ZERO. Crucially this is NOT self-reported: verify_coverage() checks each record's
claimed anchor AGAINST THE LIVE CORPUS (does that fixture/gate/calibration case actually exist?). A
record that claims "covered" but whose anchor is missing is counted as UNCOVERED - you cannot lie your
way to a clean metric. That is the difference between a receipt and a report (Tier E1).

C1 - SELF-IMPROVING RATCHET. record_defect() is the single funnel: when a human catches a new defect,
you add a DefectRecord + its fixture/calibration anchor in the SAME change. next_actions() lists any
record whose coverage does not yet verify - the concrete to-do that turns "issue I caught in review"
into "issue the build rejects." A recurrence count >= 2 marks the richest signal to codify first.

This is deterministic + offline. It is the scoreboard the rest of the suite is judged by.
"""
from __future__ import annotations
from dataclasses import dataclass, field
import os, sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)

# coverage kinds
DET_GATE = "deterministic_gate"       # a lesson/stimulus/item gate + a known-bad fixture that proves it
JUDGE_CASE = "judge_calibration"      # a semantic defect covered by a labeled calibration case (Tier B)
UNCOVERED = "uncovered"               # caught by a human, no automated coverage yet (the number to kill)


@dataclass
class DefectRecord:
    id: str                    # short slug
    summary: str               # what the defect was, in one line
    caught_by: str             # "human" | "council" | "fable_audit" | "gate"  (provenance of the CATCH)
    date: str                  # when it was caught (absolute)
    coverage_kind: str         # DET_GATE | JUDGE_CASE | UNCOVERED
    # the ANCHOR that must actually exist for the coverage claim to verify:
    fixture_gate: str = ""     # for DET_GATE: the gate name a known-bad fixture must target
    fixture_scope: str = "lesson"   # "lesson" | "stimulus" | "item"
    calibration_class: str = ""     # for JUDGE_CASE: the defect_class a calibration case must carry
    recurrences: int = 1       # how many times this class has been seen (>=2 = codify-first signal)
    note: str = ""


# ---------------------------------------------------------------------------
# THE LEDGER - every human/Council/Fable-caught defect this project, with its coverage anchor.
# ---------------------------------------------------------------------------
# Seeded from THIS session's defects + the fail-opens the corpus caught. Extend via record_defect()
# whenever a human catches a new one (C1 ratchet): add the record AND its fixture/calibration in the
# same change, or verify_coverage() will count it UNCOVERED and next_actions() will surface it.

DEFECT_LEDGER = [
    # --- semantic defects (need an LLM judge; covered by Tier B calibration cases) ---
    DefectRecord("also_correct_distractor",
                 "A discrimination distractor was also defensibly correct under the stem as worded.",
                 caught_by="council", date="2026-07-15", coverage_kind=JUDGE_CASE,
                 calibration_class="also_correct_distractor", recurrences=1,
                 note="Sentence-grain Council review, fix f3e2da4."),
    DefectRecord("planner_grain_mismatch",
                 "A single-paragraph outline was taught to plan a whole multi-paragraph essay (TWR category error).",
                 caught_by="human", date="2026-07-16", coverage_kind=JUDGE_CASE,
                 calibration_class="planner_grain_mismatch", recurrences=1,
                 note="Noel flag + TWR primary-text verify, fix 3381a49."),
    DefectRecord("phantom_draft_diagnosis",
                 "A one-write essay's diagnosis step referenced a draft the student never actually wrote.",
                 caught_by="human", date="2026-07-15", coverage_kind=JUDGE_CASE,
                 calibration_class="phantom_draft_diagnosis", recurrences=1,
                 note="One-write essay re-architecture, fix 084ff7e."),

    # --- register/credibility defect (deterministic; covered by a stimulus known-bad) ---
    DefectRecord("childish_stimulus_opener",
                 "A stimulus passage opened with a childish 'The topic here is ...' orientation line.",
                 caught_by="human", date="2026-07-16", coverage_kind=DET_GATE,
                 fixture_gate="register", fixture_scope="stimulus", recurrences=1,
                 note="Noel flag; fix f9944e0; gate_register added + hole (passage vs slot) closed 2551ed7."),

    # --- structural / deterministic defects the corpus caught (fail-opens + item form) ---
    DefectRecord("discrimination_fail_open",
                 "An unlabeled discrimination slot could ride on a labeled sibling (any() fail-open).",
                 caught_by="gate", date="2026-07-15", coverage_kind=DET_GATE,
                 fixture_gate="discrimination_before_production", fixture_scope="lesson", recurrences=1,
                 note="Checker corpus caught it after the spine re-architecture added a 2nd discrimination; any()->all()."),
    DefectRecord("distractor_length_cue_fail_open",
                 "distractor_length_cue passed silently on unparseable options (a real lone-longest key cue slipped).",
                 caught_by="gate", date="2026-07-15", coverage_kind=DET_GATE,
                 fixture_gate="distractor_length_cue", fixture_scope="lesson", recurrences=1,
                 note="Rewrote to prefer choices[], fail-closed on unparseable; caught g11_l24 key A."),
    DefectRecord("structural_banned_option_form",
                 "An 'all/none of the above' or Type-K option form in a discrimination.",
                 caught_by="council", date="2026-07-15", coverage_kind=DET_GATE,
                 fixture_gate="structural_item", fixture_scope="lesson", recurrences=1,
                 note="A8 gate_structural_item; relaxed to 2-4 options after over-flagging 5 legit binary pairs."),
    DefectRecord("mastery_genre_mismatch",
                 "A PP100 mastery source was the wrong writing genre for what the lesson taught.",
                 caught_by="human", date="2026-07-15", coverage_kind=DET_GATE,
                 fixture_gate="", fixture_scope="lesson", recurrences=4,
                 note="A5 mastery_genre_gate reproduces the 4 triage mismatches; covered by test_mastery_genre_gate "
                      "(its own corpus), not the lesson known-bad list - see verify_coverage special-case."),
]


# ---------------------------------------------------------------------------
# COVERAGE VERIFICATION - check each record's claim against the LIVE corpus (not self-report).
# ---------------------------------------------------------------------------

def _fixture_gate_names():
    """The set of (scope, gate) a known-bad fixture actually targets, loaded live from fixtures.py."""
    sys.path.insert(0, os.path.join(HERE, "tests"))
    import fixtures as fx
    out = set()
    for g, _, _ in fx.LESSON_KNOWN_BAD:
        out.add(("lesson", g))
    for g, _, _ in fx.STIMULUS_KNOWN_BAD:
        out.add(("stimulus", g))
    for g, _, _ in fx.ITEM_KNOWN_BAD:
        out.add(("item", g))
    return out


def _calibration_classes():
    import judge_calibration as jc
    return {c.defect_class for c in jc.CALIBRATION_CASES}


def _mastery_gate_covered():
    """Special case: the mastery-genre defect is covered by the mastery_genre_gate's OWN test corpus
    (test_mastery_genre_gate reproduces the 4 triage mismatches), not the shared known-bad list. Verify
    that gate + its exact-4 test still exist."""
    try:
        import mastery_genre_gate as mg  # noqa: F401
    except Exception:
        return False
    return os.path.exists(os.path.join(HERE, "tests", "test_mastery_genre_gate.py"))


def verify_coverage(rec: DefectRecord) -> bool:
    """Does this record's CLAIMED coverage actually exist in the live corpus? A missing anchor => the
    defect is effectively UNCOVERED, no matter what coverage_kind claims."""
    if rec.coverage_kind == UNCOVERED:
        return False
    if rec.coverage_kind == JUDGE_CASE:
        return rec.calibration_class in _calibration_classes()
    if rec.coverage_kind == DET_GATE:
        if rec.id == "mastery_genre_mismatch":
            return _mastery_gate_covered()
        if not rec.fixture_gate:
            return False
        return (rec.fixture_scope, rec.fixture_gate) in _fixture_gate_names()
    return False


def metric() -> dict:
    """C2: the one number. Returns total defects, how many have VERIFIED automated coverage, and
    caught_by_human_not_by_gate = the count still relying on a human (must trend to 0)."""
    verified = [r for r in DEFECT_LEDGER if verify_coverage(r)]
    uncovered = [r for r in DEFECT_LEDGER if not verify_coverage(r)]
    return {
        "total_defects": len(DEFECT_LEDGER),
        "verified_covered": len(verified),
        "caught_by_human_not_by_gate": len(uncovered),   # THE number
        "coverage_rate": len(verified) / len(DEFECT_LEDGER) if DEFECT_LEDGER else 1.0,
        "uncovered_ids": [r.id for r in uncovered],
    }


def next_actions() -> list:
    """C1 ratchet: the concrete to-do list - every record whose coverage does not verify, richest
    signal (recurrences >= 2) first. Empty list == the suite has caught up to every known defect."""
    todo = [r for r in DEFECT_LEDGER if not verify_coverage(r)]
    todo.sort(key=lambda r: (-r.recurrences, r.id))
    return [{"id": r.id, "summary": r.summary, "recurrences": r.recurrences,
             "needed": (f"add a {r.fixture_scope} known-bad targeting gate '{r.fixture_gate}'"
                        if r.coverage_kind == DET_GATE
                        else f"add a calibration case for class '{r.calibration_class}'"
                        if r.coverage_kind == JUDGE_CASE
                        else "define a gate or calibration case for this defect")}
            for r in todo]


def record_defect(rec: DefectRecord):
    """C1 funnel (programmatic): register a newly human-caught defect. In practice you edit
    DEFECT_LEDGER above in the same change that adds the fixture; this helper exists for tooling that
    appends at runtime. Appends and returns the current metric so a caller sees the new gap."""
    DEFECT_LEDGER.append(rec)
    return metric()


def main():
    m = metric()
    print("=== COMPOUND-LEARNING METRIC (Tier C2) ===")
    print(f"  total defects tracked:            {m['total_defects']}")
    print(f"  with VERIFIED automated coverage: {m['verified_covered']}")
    print(f"  caught_by_human_not_by_gate:      {m['caught_by_human_not_by_gate']}   <-- must trend to 0")
    print(f"  coverage rate:                    {m['coverage_rate']*100:.0f}%")
    acts = next_actions()
    if acts:
        print("\n  NEXT ACTIONS (C1 ratchet - close these to reach 0):")
        for a in acts:
            print(f"   - [{a['recurrences']}x] {a['id']}: {a['needed']}")
    else:
        print("\n  every tracked defect has verified automated coverage. The suite has caught up.")
    return 0 if m["caught_by_human_not_by_gate"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
