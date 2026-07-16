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


# ---- (2) KNOWN-BAD: a real GENRE MISMATCH is flagged (mutation, not live data) ----------------
# The 4 triage mismatches were FIXED in the bank on 2026-07-16 (mastery sources swapped / prompts realigned),
# so the gate logic can no longer be proven against the live lessons. Instead we re-INJECT the exact defect the
# triage found onto the now-fixed lesson and assert the gate still rejects it - the mutation is data-independent,
# so it tests the LOGIC, not today's corpus. (History: before the fix these were live known-bads.)

def test_known_bad_analysis_vs_explanatory_is_flagged():
    """C1003-0025 was fixed to a literary-analysis held-out source. Re-inject the ORIGINAL defect
    (an explanatory-nonfiction mastery on an analysis lesson) and assert the gate still rejects it."""
    L = _lesson_from("Lesson_Bank_G10/lesson_g10_l25_analysis_essay_single.py")
    assert L.id == "ACC-W910-L-G10-C1003-0025"
    L.mastery = {"source": "ACC-W910-INFO-LESSON-WETLANDS",           # the original mismatched source
                 "prompt_html": "<p>Analyze how the author builds interest in protecting wetlands.</p>"}
    ok, problems = check_mastery_alignment(L, "G10")
    assert not ok, "re-injected known-bad (analysis taught / explanatory mastery) was NOT flagged"
    assert any("GENRE mismatch" in p and "ANALYSIS" in p for p in problems), problems


# ---- (3) THE FOUR TRIAGE MISMATCHES ARE NOW FIXED (live corpus clean) + logic still catches them --

# The four lessons the triage marked as genre mismatches, with the FIX applied 2026-07-16:
FIXED_TRIAGE_LESSONS = {
    "ACC-W910-L-G10-C1006-0021",   # reframed cross-text -> single-text analysis (Challenger, analysis source)
    "ACC-W910-L-G10-C1003-0025",   # explanatory wetlands -> literary analysis (Silk Stockings)
    "ACC-W1112-L-G11-C1102-0030",  # synthesis-set -> source-free ARGUMENT (SFA-PROMPT-0004) the gate rehearses
    "ACC-W910-L-G12-C1202-0012",   # prompt disambiguated + rubric-rows dropped; genre adjudicated (recognition lesson)
}


def test_the_four_triage_mismatches_are_now_clean_on_the_live_course():
    """After the 2026-07-16 fixes, NONE of the four triage lessons should flag, AND the whole course
    should be genre-clean (0 flags) - the goal state."""
    flagged = {lid for _g, catches in run_all().items() for lid, _p in catches}
    still_broken = FIXED_TRIAGE_LESSONS & flagged
    assert not still_broken, f"a triage lesson is still flagged after its fix: {sorted(still_broken)}"
    assert not flagged, f"course not genre-clean; unexpected flags: {sorted(flagged)}"


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


# ---- (6) ADJUDICATED false-positive: suppressed ONLY while the profile holds -----------------

def test_adjudicated_recognition_lesson_is_suppressed():
    """C1202-0012 is a genre-agnostic FRQ-RECOGNITION lesson (type 5) taught on BOTH a synthesis set and an
    analysis source; its synthesis-set mastery is correct. The gate's genre flag is a documented false-positive,
    adjudicated (ADJUDICATED registry), so the live lesson must pass."""
    L = _lesson_from("Lesson_Bank_G12/lesson_g12_l12_which_frq_type.py")
    assert L.id == "ACC-W910-L-G12-C1202-0012"
    ok, problems = check_mastery_alignment(L, "G12")
    assert ok, "adjudicated recognition lesson wrongly flagged:\n" + "\n".join(problems)


def test_adjudication_does_not_mask_a_defect_when_profile_breaks():
    """Belt-and-suspenders: if C1202-0012 stops matching the adjudicated profile (e.g. it becomes an
    analysis-PRODUCTION lesson, not a type-5 recognition lesson), the suppression must NOT fire - the guard
    protects against the adjudication silently masking a future genuinely-different defect on the same id."""
    from mastery_genre_gate import ADJUDICATED
    L = _lesson_from("Lesson_Bank_G12/lesson_g12_l12_which_frq_type.py")
    assert L.id in ADJUDICATED
    # break the profile: make it a text-dependent-analysis PRODUCTION lesson (type 4), no longer type-5 recognition
    L.lesson_type = 4
    assert ADJUDICATED[L.id]["guard"](L) is False, "guard should not hold once the recognition profile is broken"
    ok, problems = check_mastery_alignment(L, "G12")
    assert not ok, "adjudication wrongly suppressed a real flag after the lesson profile changed"
