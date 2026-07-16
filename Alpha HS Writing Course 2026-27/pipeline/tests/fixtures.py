"""Checker-corpus fixtures: verify the verifier.

The point (Fable eval + BrainLift SPOV6 "the verifier rots first"): prove each gate REJECTS
the defect it claims to catch. A corpus of only-passing content validates nothing; the
known-BAD fixtures are the load-bearing half.

Design:
  - `golden_lesson()` loads a REAL passing lesson from the bank as the baseline, so a golden is
    ground truth, not a hand-built approximation that could drift from the real records.
  - Each KNOWN_BAD is a (gate_name, mutate_fn, why) tuple. mutate_fn takes a deep copy of the
    golden lesson and introduces exactly ONE defect. The harness asserts that gate REJECTS it.
  - Stimulus/item known-bads are built as minimal records (their contracts have simple ctors).

Seeded from the defects the council + Fable already caught (the four P1 families, the ~4 false
passes, the two fail-opens just closed, and the fabrication hole). Add a fixture whenever a new
defect is found: that is how the corpus grows into real coverage.
"""
from __future__ import annotations

import copy
import glob
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.dirname(HERE)
ROOT = os.path.dirname(PIPE)


def _load_module(path):
    spec = importlib.util.spec_from_file_location("fx_" + os.path.basename(path)[:-3], path)
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
    except SystemExit:
        pass
    return m


def golden_lesson():
    """A real, passing lesson from the bank (G9 L07 integrate_quote: has teach/model/discrim/
    production, bound refs, options). Baseline for known-bad mutations."""
    import sys
    if PIPE not in sys.path:
        sys.path.insert(0, PIPE)
    cands = sorted(glob.glob(os.path.join(ROOT, "Lesson_Bank_G9", "lesson_g9_l07_*.py")))
    assert cands, "golden baseline lesson (G9 L07) not found"
    m = _load_module(cands[0])
    lessons = getattr(m, "LESSONS", [])
    assert lessons, "no LESSONS in golden baseline module"
    return copy.deepcopy(lessons[0])


# ---- KNOWN-BAD MUTATIONS (each introduces exactly one defect) ----
# (gate_name, mutate_fn, why) - the harness asserts gate_name REJECTS mutate_fn(golden).

def _mut_shell_incomplete(L):
    # Drop every TRANSFER slot -> SRSD shell incomplete.
    L.slots = [s for s in L.slots if s.role != "TRANSFER"]
    return L


def _mut_phantom_ref(L):
    # Point a bound slot at an SR id that was never generated (HOLE 2 regression guard).
    for s in L.slots:
        if s.ref.strip():
            s.ref = "ACC-W910-SR-ORG-9999"
            break
    return L


def _mut_length_cue_in_predict_fix(L):
    # Make the correct option the lone-longest in a predict_the_fix, with the marker in FEEDBACK
    # (HOLE 1 regression guard: the gate must read the marker from feedback and catch this).
    for s in L.slots:
        if s.kind == "predict_the_fix":
            s.body = ("Which move most improves it? (A) add a fact (B) be formal (C) shorten it "
                      "(D) take a clear side on the full ban and add a specific reason a reader could dispute here")
            s.feedback = "Correct: D. It takes a side and gives a reason."
            return L
    raise AssertionError("golden has no predict_the_fix slot to mutate")


def _mut_em_dash(L):
    # Inject an em dash into authored prose (house-rule violation).
    for s in L.slots:
        if s.body:
            s.body = s.body + " This is a trailing clause — with an em dash."
            return L
    raise AssertionError("golden has no body prose to mutate")


def _mut_unlabeled_grade_c(L):
    # Every discrimination slot must be labeled a Grade-C design bet. Unlabel ALL of them (the golden now has
    # >1 discrimination after the spine re-architecture; unlabeling just the first let a labeled sibling mask
    # the defect, which is exactly the any()->all() fail-open the gate was hardened to close).
    for s in L.slots:
        if s.kind == "discrimination":
            s.labeled_grade_c = False
    return L
    raise AssertionError("golden has no discrimination slot to mutate")


LESSON_KNOWN_BAD = [
    ("shell_completeness", _mut_shell_incomplete, "SRSD shell missing TRANSFER stage"),
    ("binding_integrity", _mut_phantom_ref, "bound ref to a never-generated SR id (HOLE 2)"),
    ("distractor_length_cue", _mut_length_cue_in_predict_fix,
     "predict_the_fix correct option lone-longest, marker in feedback (HOLE 1)"),
    ("no_em_dash", _mut_em_dash, "em dash in authored lesson prose (house rule)"),
    ("discrimination_before_production", _mut_unlabeled_grade_c,
     "discrimination slot not labeled_grade_c"),
]


# ============================================================================
# ITEM fixtures (item_contract). Golden = the SR item from item_contract's self-test.
# ============================================================================

def golden_sr_item():
    import item_contract as IC
    return IC.Item(
        id="ACC-W910-SR-EVIDENCE-9001", family="SR", grade="9-10", subskill_or_mode="evidence",
        qti_type="choice",
        stem="A student argues cities should expand transit. Which sentence best supports the claim?",
        acc_tags=["ACC.W.SRC.1", "CCSS.W.9-10.1"],
        options=[
            IC.Option("A", "One light-rail line moves as many riders per hour as six highway lanes.", True, ""),
            IC.Option("B", "Many people enjoy listening to music while they commute to their work.", False,
                      "off-claim: rider experience, not capacity"),
            IC.Option("C", "Traffic congestion is a serious problem in almost every large city today.", False,
                      "restates topic, no evidence"),
            IC.Option("D", "Some drivers still prefer their own cars because of privacy and control.", False,
                      "supports the opposing view"),
        ],
        answer_key=["A"],
        provenance={"copyright": "own_authored", "authored": "2026-07-14"},
    )


def _mut_item_length_leak(it):
    # Make the correct option conspicuously longest (>25% over the longest distractor): a real length leak.
    it.options[0].text = it.options[0].text + " " + ("and it is by far the most detailed and qualified choice " * 3)
    return it


def _mut_item_duplicate_options(it):
    it.options[1].text = it.options[2].text  # two identical option texts
    return it


def _mut_item_distractor_no_rationale(it):
    it.options[1].rationale = ""  # a distractor with no misconception rationale
    return it


def _mut_item_answer_key_mismatch(it):
    it.answer_key = ["B"]  # key does not match the option flagged correct=True (A)
    return it


def _mut_item_em_dash(it):
    it.stem = it.stem + " Consider the tradeoffs — carefully."
    return it


ITEM_KNOWN_BAD = [
    ("distractor_integrity", _mut_item_length_leak, "correct option conspicuously longest (length leak)"),
    ("distractor_integrity", _mut_item_duplicate_options, "two identical option texts"),
    ("distractor_integrity", _mut_item_distractor_no_rationale, "distractor missing misconception rationale"),
    ("schema", _mut_item_answer_key_mismatch, "answer_key does not match the correct option id"),
    ("no_em_dash", _mut_item_em_dash, "em dash in item stem"),
]


# ============================================================================
# STIMULUS fixtures (stimulus_contract). Golden = a minimal own-authored single-source stimulus.
# ============================================================================

def golden_stimulus():
    """A real, passing single-source own-authored stimulus from the bank (coral reefs, G10).
    Loading a real record (not a hand-built one) keeps the golden ground-truth: it meets the actual
    480-word floor, >=3-fact, and Lexile-band bars instead of a fragile approximation that could drift."""
    import glob
    cands = sorted(glob.glob(os.path.join(ROOT, "Stimulus_Bank_G10", "info_coral_reefs.py")))
    assert cands, "golden baseline stimulus (info_coral_reefs) not found"
    m = _load_module(cands[0])
    for v in vars(m).values():
        if type(v).__name__ == "StimulusRecord" and getattr(v, "id", "") == "ACC-W910-INFO-SINGLE-0001":
            return copy.deepcopy(v)
    raise AssertionError("ACC-W910-INFO-SINGLE-0001 not found in golden stimulus module")


def _mut_stim_unbacked_figure(s):
    # Add a numeric figure to the passage that has NO fact-source row (fabrication risk).
    s.passages[0].text += " A striking 87 percent of shoppers said they never plan meals ahead."
    return s


def _mut_stim_bad_url(s):
    s.fact_sources[0].url_fetched = "not-a-url"  # fact-source with no valid fetched URL
    return s


def _mut_stim_no_facts(s):
    s.fact_sources = []  # own-authored stimulus with no fact table
    return s


STIMULUS_KNOWN_BAD = [
    ("fact_sources", _mut_stim_unbacked_figure, "in-text figure with no fact-source row (fabrication risk)"),
    ("fact_sources", _mut_stim_bad_url, "fact-source with no valid fetched URL"),
    ("fact_sources", _mut_stim_no_facts, "own-authored stimulus with empty fact table"),
]
