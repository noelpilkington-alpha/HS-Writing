"""Mastery genre-match + DOK-consistency gate corpus - verify the verifier (Tier A5).

Same doctrine as test_checker_corpus / test_register_gate:
  1. GOLDEN: a REAL live lesson whose held-out PP100 mastery source MATCHES the taught genre passes
     clean. G12 C1202-0010 (rehearse a rhetorical analysis) teaches ANALYSIS and its mastery source
     ACC-W910-RA-SINGLE-0003 is an analysis text - the triage's own GENRE-CHECK marks it a MATCH.
     (Precision: no false flag on a genuine match.)
  2. KNOWN-BAD: a REAL live lesson the triage marks a genuine GENRE MISMATCH is flagged. G10
     C1003-0025 (single-text analysis essay) teaches literary-fiction ANALYSIS but its PP100 source
     is ACC-W910-INFO-LESSON-WETLANDS (EXPLANATORY nonfiction) - the triage's GENRE-CHECK reads
     "MISMATCH (lit-fiction analysis taught, graded on nonfiction wetlands)". (Recall: the gate
     catches the real defect.)

Plus: the gate reproduces EXACTLY the four genuine GENRE mismatches from COURSE_MASTERY17_TRIAGE.md
(C1006-0021, C1003-0025, C1102-0030, C1202-0012) across the live course, and does NOT flag the
clear matches or the genre-agnostic / multi-FRQ lessons (the documented over-flag failure mode).

Mutation known-bads (deep-copied golden with exactly one defect) exercise the analysis boundary and
the DOK two-level jump independently of the live corpus, so the gate's logic - not just today's
data - is under test.
"""
from __future__ import annotations

import copy
import glob
import importlib.util
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.dirname(HERE)
ROOT = os.path.dirname(PIPE)
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)

from mastery_genre_gate import check_mastery_alignment, run_all  # noqa: E402


def _load_module(path):
    spec = importlib.util.spec_from_file_location("mg_" + os.path.basename(path)[:-3], path)
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
    except SystemExit:
        pass
    return m


def _lesson_from(glob_pat):
    cands = [f for f in sorted(glob.glob(os.path.join(ROOT, glob_pat))) if "__pycache__" not in f]
    assert cands, f"lesson not found for pattern {glob_pat}"
    m = _load_module(cands[0])
    L = getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0]
    assert L is not None, f"no LESSON in {cands[0]}"
    return copy.deepcopy(L)


# ---- (1) GOLDEN: a real MATCH lesson passes clean --------------------------------------------

def test_golden_analysis_match_passes_clean():
    """G12 C1202-0010: analysis taught, analysis mastery source (RA-SINGLE-0003) = triage MATCH."""
    L = _lesson_from("Lesson_Bank_G12/lesson_g12_l10_timed_analysis.py")
    assert L.id == "ACC-W910-L-G12-C1202-0010"
    ok, problems = check_mastery_alignment(L, "G12")
    assert ok, "golden (analysis/analysis MATCH) lesson wrongly flagged:\n" + "\n".join(problems)


# ---- (2) KNOWN-BAD: a real GENRE MISMATCH is flagged -----------------------------------------

def test_known_bad_analysis_vs_explanatory_is_flagged():
    """G10 C1003-0025: literary-fiction analysis taught, PP100 = explanatory wetlands = triage MISMATCH."""
    L = _lesson_from("Lesson_Bank_G10/lesson_g10_l25_analysis_essay_single.py")
    assert L.id == "ACC-W910-L-G10-C1003-0025"
    ok, problems = check_mastery_alignment(L, "G10")
    assert not ok, "known-bad (analysis taught / explanatory mastery) was NOT flagged"
    assert any("GENRE mismatch" in p and "ANALYSIS" in p for p in problems), problems


# ---- (3) THE FOUR GENUINE GENRE MISMATCHES from the triage, and only those -------------------

EXPECTED_GENRE_MISMATCHES = {
    "ACC-W910-L-G10-C1006-0021",   # analysis taught, argument op-ed mastery
    "ACC-W910-L-G10-C1003-0025",   # lit-fiction analysis taught, explanatory wetlands mastery
    "ACC-W1112-L-G11-C1102-0030",  # gate rehearses argument, synthesis-set mastery
    "ACC-W910-L-G12-C1202-0012",   # analysis-tier lesson, synthesis-set mastery
}


def test_gate_reproduces_the_four_triage_genre_mismatches_exactly():
    flagged = set()
    for _grade, catches in run_all().items():
        for lid, _p in catches:
            flagged.add(lid)
    missing = EXPECTED_GENRE_MISMATCHES - flagged
    extra = flagged - EXPECTED_GENRE_MISMATCHES
    assert not missing, f"gate MISSED genuine triage mismatch(es): {sorted(missing)}"
    assert not extra, f"gate OVER-flagged (documented failure mode) beyond the triage set: {sorted(extra)}"


def test_known_matches_are_not_flagged():
    """Clear MATCHES the triage does not treat as genre defects must stay clean (precision guard)."""
    clean = {
        "ACC-W910-L-G12-C1202-0010",   # analysis/analysis MATCH
        "ACC-W910-L-G10-C1006-0022",   # argument essay, argument source set
        "ACC-W1112-L-G12-C1201-0006",  # synthesis lesson, synthesis source set
        "ACC-W1112-L-G11-C1103-0006",  # rhetorical analysis, analysis source
        "ACC-W910-L-G10-C1006-0024",   # cross-text gate (verb sets mode), argument set - NOT a genre defect
        "ACC-W910-L-G12-C1202-0016",   # multi-FRQ gate: spans genres by design
    }
    flagged = {lid for _g, catches in run_all().items() for lid, _p in catches}
    wrongly = clean & flagged
    assert not wrongly, f"clear matches wrongly flagged: {sorted(wrongly)}"


# ---- (4) MUTATION known-bads: exercise each rule in isolation --------------------------------

def test_mutation_analysis_lesson_with_argument_mastery_is_flagged():
    """Take the golden analysis MATCH lesson and swap its mastery source to an ARGUMENT source: the
    analysis boundary must reject it (analysis taught, non-analysis graded)."""
    L = _lesson_from("Lesson_Bank_G12/lesson_g12_l10_timed_analysis.py")
    L.mastery = {"source": "ACC-W910-ARG-LESSON-SCHOOLLUNCH",
                 "prompt_html": "<p>Take a side on the issue and defend your position.</p>"}
    ok, problems = check_mastery_alignment(L, "G12")
    assert not ok and any("ANALYSIS" in p for p in problems), problems


def test_mutation_dok_two_level_jump_is_flagged():
    """An explanatory-summary lesson (DOK 2) whose mastery demands 'synthesize' (DOK 4) is a
    two-level Webb jump and must be flagged by the DOK sub-check."""
    L = _lesson_from("Lesson_Bank_G10/lesson_g10_l25_analysis_essay_single.py")
    # neutralize genre: pretend it's an explanatory-summary lesson so only DOK can fire
    L.title = "Summarize the Source in One Sentence"
    L.target = "Summarize what an informational source says. Trait: central idea."
    L.lesson_type = 1
    for s in L.slots:
        if s.kind == "stimulus_display":
            s.ref = "ACC-W910-INFO-LESSON-WETLANDS"   # explanatory taught source
            s.role = "TEACH"
    L.mastery = {"source": "ACC-W910-INFO-LESSON-WETLANDS",
                 "prompt_html": "<p>Synthesize the source set: weave one argument from all the sources.</p>"}
    ok, problems = check_mastery_alignment(L, "G10")
    assert not ok and any("DOK mismatch" in p for p in problems), problems


# ---- (5) CONSERVATISM guards: the over-flag modes must NOT fire -------------------------------

def test_no_authored_mastery_source_passes_na():
    """A lesson with no held-out mastery source (source-free / pusher-filled) has nothing to
    mismatch and must pass."""
    L = _lesson_from("Lesson_Bank_G12/lesson_g12_l10_timed_analysis.py")
    L.mastery = {}
    # force the grade lookup to also miss by using a bogus grade key path: simplest is to blank the id
    L.id = "ACC-W910-L-G12-NONEXISTENT-9999"
    ok, problems = check_mastery_alignment(L, "G12")
    assert ok and problems == [], problems


def test_one_level_transfer_is_not_a_dok_defect():
    """An argument lesson (DOK 3) graded with an 'argue' mastery (DOK 3) is normal transfer - the
    one-level guard means it must NOT be flagged as a DOK defect."""
    L = _lesson_from("Lesson_Bank_G10/lesson_g10_l25_analysis_essay_single.py")
    L.title = "Write a Counterclaim-Aware Argument"
    L.target = "Take a side and answer the strongest counterclaim. Trait: argument."
    L.lesson_type = 7
    for s in L.slots:
        if s.kind == "stimulus_display":
            s.ref = "ACC-W910-ARG-OPP-LESSON-DST"
            s.role = "TEACH"
    L.mastery = {"source": "ACC-W910-ARG-OPP-LESSON-CONGESTION",
                 "prompt_html": "<p>Take a side and defend your position, answering the counterclaim.</p>"}
    ok, problems = check_mastery_alignment(L, "G10")
    assert ok, "one-level argument->argument transfer wrongly flagged:\n" + "\n".join(problems)
