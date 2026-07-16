"""
mastery_genre_gate.py  -  Tier A5 MASTERY GENRE-MATCH + Webb DOK-CONSISTENCY gate (G9-G12).

WHY (COURSE_MASTERY17_TRIAGE.md, human review 2026-07-15): a lesson's held-out PP100 mastery
source (mastery_prompts_g{N}.MASTERY[id]["source"]) was sometimes chosen for TOPIC variety without
checking it shares the lesson's TAUGHT writing genre, or the mastery task demanded a cognitive move
the lesson never built. Human review caught 17 mastery-misaligned lessons; of those, the triage's
deterministic GENRE-CHECK column marks FOUR as a true taught-vs-mastery genre MISMATCH:

  - ACC-W910-L-G10-C1006-0021 : lesson teaches ANALYSIS (literary + expository craft), PP100 grades
    craft analysis of ARGUMENT op-eds (a genre the lesson never modeled).
  - ACC-W910-L-G10-C1003-0025 : lesson teaches literary-fiction ANALYSIS, PP100 = EXPLANATORY
    (nonfiction wetlands) rhetorical analysis (untaught device set).
  - ACC-W1112-L-G11-C1102-0030 : gate rehearses a source-free ARGUMENT, PP100 grades SYNTHESIS on a
    labeled source SET (a type the gate never rehearsed).
  - ACC-W910-L-G12-C1202-0012 : "name the FRQ type" lesson taught on argument/analysis tells; PP100
    hands a SYNTHESIS source set to a lesson that must instead produce an analysis-tier deliverable.

WHAT THIS GATE DOES (deterministic, offline, CONSERVATIVE):
  check_mastery_alignment(L, grade) -> (ok, problems)
    1. GENRE MATCH. Compare the held-out mastery source's writing genre (family-aware: a
       synthesis_set source is a "synthesis" task, a perspective_set/prompt_only source is
       "argument", else the record .mode) to what the LESSON teaches. Analysis is the hard
       boundary: a lesson that teaches text/craft analysis must be graded on an analysis source,
       and a non-analysis lesson must not be graded on an analysis source. A labeled multi-source
       SET (synthesis) mastery on a lesson that never rehearses source-set synthesis is a mismatch.
    2. DOK CONSISTENCY (Webb). Anchor the lesson's cognitive tier on its robust genre (argument /
       analysis / synthesis are inherently DOK 3-4; explanatory-summary is DOK 2) PLUS any literal
       high-DOK verb the lesson actually asks for; flag only when the mastery prompt demands a
       verb TWO Webb levels above what the lesson builds. This two-level guard is deliberately
       strict: the documented failure mode of the readiness audit is OVER-flagging (a Fable judge
       that flagged deliberate design), so this gate fires only on clear mismatches.

WHY NOT A NAIVE .mode COMPARISON: the raw stimulus .mode tag is NOISY for this purpose. Analysis
lessons legitimately analyze EXPLANATORY-mode nonfiction; a synthesis SET carries whatever .mode
its lead source happens to have (argument OR explanatory); revision / editing / evidence-selection
skills are genre-agnostic. A blunt "any taught .mode != mastery .mode" check flags ~16-17 lessons
(most of them fine). The rules below normalize genre by FAMILY, treat analysis as the one hard
boundary, and exempt genre-agnostic process skills - reproducing exactly the triage's 4 genuine
GENRE mismatches with zero false positives on the live course.

SCOPE: this gate reads the lesson's slots + provenance + its authored PP100 mastery entry (source
id + prompt_html). It is offline and deterministic (no LLM, no network). It does NOT re-judge the
in-article steps (that is other gates' job) - only the held-out mastery SOURCE's fit.

API:
  check_mastery_alignment(L, grade) -> (passed: bool, problems: list[str])   # passed == (problems == [])
  run_grade(grade) -> list[(lesson_id, problem)]
  run_all()        -> dict[grade -> list[(lesson_id, problem)]]

Run: python pipeline/mastery_genre_gate.py [G9|G10|G11|G12|all]   -> per-grade counts + verdict, exit-coded.
"""
from __future__ import annotations
import os, sys, re, glob

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)

from g9_push_dryrun import _load, STIM                       # noqa: E402
from mastery_targets_grade import _authored, _GRADE_GLOB      # noqa: E402


# ---------------------------------------------------------------------------
# source genre (family-aware) + plain-text helpers
# ---------------------------------------------------------------------------

def _rec(sid):
    return STIM.get(sid) if sid else None


def _src_genre(sid):
    """The WRITING GENRE a source implies for a task, normalized by family so the noisy .mode tag
    does not drive the check:
      - synthesis_set  -> 'synthesis'  (a labeled SET is a synthesis task regardless of lead .mode)
      - perspective_set / prompt_only -> 'argument'  (ACT multi-perspective / AP Q3 are argue-from-)
      - else the record .mode ('argument' | 'explanatory' | 'analysis')."""
    r = _rec(sid)
    if r is None:
        return None
    fam = getattr(r, "family", "") or ""
    if fam == "synthesis_set":
        return "synthesis"
    if fam in ("perspective_set", "prompt_only"):
        return "argument"
    return getattr(r, "mode", None)


def _src_family(sid):
    r = _rec(sid)
    return (getattr(r, "family", "") or "") if r else ""


def _plain(h: str) -> str:
    if not h:
        return ""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()


# ---------------------------------------------------------------------------
# genre classifiers (from the lesson's target/title/type + its taught sources)
# ---------------------------------------------------------------------------

# analysis = producing an analysis of an author's craft / rhetoric (NOT "task analysis", a process phrase).
_ANALYSIS_RE = re.compile(
    r"(analytical (?:thesis|claim|essay)|analysis essay|rhetorical(?:-| )analysis|rhetorical choice|"
    r"author'?s craft|\bcraft\b|device.{0,10}(?:to |and )?effect|analyze (?:how|the|this|a )|"
    r"single-text analysis|cross-text analysis|does this paragraph analyze|\(analysis\))", re.I)

# source-set synthesis = weaving one argument from a labeled SET of sources.
_SYNTH_RE = re.compile(
    r"(synthes|weav|woven|source set|multi-source|multiple source|across the (?:set|sources)|"
    r"the set builds|whole set|cross-source|two sources together|evidence pool|map the source)", re.I)

# lesson types that are GENRE-AGNOSTIC by design (they operate on any genre's prose):
#   3 evidence-integration, 5 rubric-revision, 6 editing-in-context.
_GENRE_AGNOSTIC_TYPES = {3, 5, 6}


def _taught_source_genres(L, roles=("TEACH", "MODEL")):
    """Genres of the stimuli the lesson DISPLAYS in the given roles (the sources it teaches on)."""
    out = set()
    for s in L.slots:
        if s.kind == "stimulus_display" and getattr(s, "ref", "") and _rec(s.ref) and getattr(s, "role", "") in roles:
            g = _src_genre(s.ref)
            if g:
                out.add(g)
    return out


def _lesson_requires_analysis(L) -> bool:
    """The lesson trains the student to PRODUCE analysis, OR to recognize/revise/work ON analysis text
    (so an analysis-mode held-out source is a genre MATCH). This is deliberately inclusive of the
    genre-agnostic recognition/editing types (3/5/6) WHEN their content is about analysis - e.g. a
    'Does this paragraph analyze or summarize?' check (type 5) or 'Trim the quote in analysis' (type 3)
    legitimately carry an analysis-mode mastery source. The regex below matches both 'produce analysis'
    and 'analyze the author's choices' framings, which is why those recognition lessons are correctly
    NOT flagged."""
    if getattr(L, "lesson_type", 0) == 4:            # text-dependent-analysis type
        return True
    t = (L.title or "") + " " + (L.target or "")
    if _ANALYSIS_RE.search(t):
        return True
    # taught ONLY on analysis-mode sources (and at least one such source)
    tg = _taught_source_genres(L)
    return tg == {"analysis"}


def _lesson_produces_synthesis(L) -> bool:
    """The lesson rehearses writing a synthesis across a labeled SOURCE SET."""
    taught_set = any(
        _src_family(s.ref) == "synthesis_set"
        for s in L.slots
        if s.kind == "stimulus_display" and getattr(s, "ref", "") and getattr(s, "role", "") in ("TEACH", "MODEL", "TRANSFER")
    )
    if getattr(L, "lesson_type", 0) == 8 and taught_set:
        return True
    t = (L.title or "") + " " + (L.target or "")
    if getattr(L, "lesson_type", 0) in (7, 8) and _SYNTH_RE.search(t):
        return True
    return False


def _mastery_is_multi_frq(prompt_plain: str) -> bool:
    """A gate/section mastery that presents MULTIPLE FRQs (e.g. 'FRQ 1 (synthesis)... FRQ 2
    (rhetorical analysis)...') deliberately spans several genres - it is NOT a single-genre mismatch,
    so the genre check must not fire on it."""
    return bool(re.search(r"FRQ\s*1", prompt_plain, re.I) and re.search(r"FRQ\s*2", prompt_plain, re.I))


# ---------------------------------------------------------------------------
# (1) GENRE MATCH
# ---------------------------------------------------------------------------

def _genre_problem(L, msrc, prompt_html) -> str | None:
    """Return a genre-mismatch problem string, or None if the mastery source's genre fits the lesson.
    Conservative: analysis is the one hard boundary; a labeled synthesis SET is the other."""
    prompt_plain = _plain(prompt_html)
    if _mastery_is_multi_frq(prompt_plain):
        return None                                  # multi-FRQ section spans genres by design
    mg = _src_genre(msrc)
    if mg is None:
        return None                                  # unknown source: nothing to compare (fail-open by design)
    mfam = _src_family(msrc)
    fam_genre = "synthesis" if mfam == "synthesis_set" else mg

    req_analysis = _lesson_requires_analysis(L)
    mast_analysis = (mg == "analysis")

    # analysis boundary, both directions
    if req_analysis and not mast_analysis:
        return (f"GENRE mismatch: the lesson teaches text/craft ANALYSIS but the held-out mastery source "
                f"({msrc}) is a {fam_genre!r} task; an analysis mastery needs an analyzable text of the "
                f"taught kind")
    if mast_analysis and not req_analysis and not _lesson_produces_synthesis(L):
        return (f"GENRE mismatch: the held-out mastery source ({msrc}) demands rhetorical/craft ANALYSIS, "
                f"but the lesson does not teach analysis")

    # synthesis-set boundary: a labeled multi-source SET on a lesson that never rehearses synthesis
    if mfam == "synthesis_set" and not _lesson_produces_synthesis(L) and not req_analysis:
        return (f"GENRE mismatch: the held-out mastery source ({msrc}) is a labeled multi-source SET "
                f"(a synthesis task), but the lesson never rehearses writing a source-set synthesis")

    return None


# ---------------------------------------------------------------------------
# (2) WEBB DOK CONSISTENCY
# ---------------------------------------------------------------------------

# Webb DOK tier of the writing GENRE the lesson trains (its cognitive floor):
#   summarize/explain an informational source        -> DOK 2 (skill/concept)
#   argue / analyze a text                            -> DOK 3 (strategic thinking)
#   synthesize a source set / evaluate                -> DOK 4 (extended thinking)
def _lesson_dok_tier(L) -> tuple[int, str]:
    t = (L.title or "") + " " + (L.target or "")
    taught = _taught_source_genres(L)
    if _lesson_produces_synthesis(L):
        return 4, "synthesis"
    if _lesson_requires_analysis(L):
        return 3, "analysis"
    # argument (from target language OR an argument taught source)
    if re.search(r"(argu|counterclaim|counterargument|take a side|concede|concession|rebut|"
                 r"\bposition\b|hold the tension|defensible claim)", t, re.I) or "argument" in taught:
        return 3, "argument"
    return 2, "explanatory/summary"

# High-DOK cognitive demands the MASTERY PROMPT may make (literal task verbs), with Webb tier.
_MASTERY_DOK = {
    "analyze":    (3, re.compile(r"\banaly[sz](?:e|es|ing|is)\b|rhetorical analysis|analytical (?:claim|thesis)", re.I)),
    "argue":      (3, re.compile(r"\bargue\b|take a (?:side|position)|defend (?:your|a) (?:own )?position|develop and defend", re.I)),
    "evaluate":   (4, re.compile(r"\bevaluate\b|\bcritique\b|\bassess\b|weigh the (?:merit|value)", re.I)),
    "synthesize": (4, re.compile(r"\bsynthesiz(?:e|ing)\b|\bsynthesis\b|weave (?:a|one|the|two|sources)|weight (?:each|the) source", re.I)),
}


def _mastery_dok(prompt_html) -> tuple[int, str | None]:
    pp = _plain(prompt_html)
    best, verb = 0, None
    for v, (tier, rx) in _MASTERY_DOK.items():
        if rx.search(pp) and tier > best:
            best, verb = tier, v
    return best, verb


def _dok_problem(L, prompt_html) -> str | None:
    """Flag only when the mastery prompt demands a cognitive verb TWO Webb levels above the tier the
    lesson builds. Two levels (not one) is a deliberate conservatism guard against the documented
    over-flag failure mode: a one-level gap (argue on an argument lesson, analyze on an analysis
    lesson) is normal transfer, never a defect."""
    l_tier, l_label = _lesson_dok_tier(L)
    m_tier, m_verb = _mastery_dok(prompt_html)
    if m_verb and (m_tier - l_tier) >= 2:
        return (f"DOK mismatch: the mastery task demands '{m_verb}' (Webb {m_tier}) but the lesson builds "
                f"only {l_label} (Webb {l_tier}); the held-out task is two cognitive levels above what is taught")
    return None


# ---------------------------------------------------------------------------
# ADJUDICATED false-positives (per-lesson, documented). Same discipline as scaffold_crosscheck.ADJUDICATED /
# expected_exceptions: a decision without a written rationale is a latent regression. Each entry names WHY the
# genre flag is deliberate design, WHO decided, and the trigger that REVERSES it. Belt-and-suspenders: the
# suppression only fires if the lesson STILL matches the adjudicated profile (guard()), so it can never silently
# mask a future genuinely-different defect on the same id.
# ---------------------------------------------------------------------------
ADJUDICATED = {
    "ACC-W910-L-G12-C1202-0012": {
        "rationale": ("Genre-agnostic FRQ-RECOGNITION lesson (type 5): the skill is NAMING whether a cold FRQ is "
                      "synthesis / rhetorical-analysis / argument. It is taught on BOTH a synthesis set AND an "
                      "analysis text, so a synthesis-set held-out source is correct (recognizing a synthesis FRQ "
                      "is the point). The gate flags it only because 'rhetorical analysis' appears as a TYPE LABEL "
                      "in the target, not because the lesson produces analysis. COURSE_MASTERY17_TRIAGE confirmed "
                      "the real defect was the type-ambiguous PROMPT + untaught rubric-rows deliverable, both "
                      "fixed 2026-07-16; the source genre is not a defect."),
        "owner": "COURSE_MASTERY17_TRIAGE + Noel (2026-07-16)",
        "reverse_if": "the lesson stops teaching on both a synthesis set and an analysis source, or stops being a "
                      "recognition (type-5) lesson - i.e. it starts requiring the student to PRODUCE one genre.",
        "guard": lambda L: (getattr(L, "lesson_type", 0) == 5
                            and "synthesis" in _taught_source_genres(L, roles=("TEACH", "MODEL", "TRANSFER"))
                            and "analysis" in _taught_source_genres(L, roles=("TEACH", "MODEL", "TRANSFER"))),
    },
}


# ---------------------------------------------------------------------------
# the gate
# ---------------------------------------------------------------------------

def check_mastery_alignment(L, grade) -> tuple[bool, list[str]]:
    """Mastery genre-match + Webb DOK-consistency gate on one Lesson (needs `grade` to load the
    authored PP100 mastery entry). Returns (passed, problems). passed == (problems == []).

    A lesson with NO authored mastery source (source-free gate, or an entry the pusher fills later)
    is passed as n/a: there is no held-out source to mismatch."""
    problems: list[str] = []
    lid = getattr(L, "id", "?")

    # the lesson's OWN mastery dict wins (single source of truth), else the grade's MASTERY[id].
    entry = getattr(L, "mastery", None) or _authored(grade).get(lid, {}) or {}
    msrc = entry.get("source")
    prompt_html = entry.get("prompt_html", "")
    if not msrc or _rec(msrc) is None:
        return True, []                              # no held-out source bound -> nothing to check

    g = _genre_problem(L, msrc, prompt_html)
    if g:
        problems.append(f"{lid}: {g}")
    d = _dok_problem(L, prompt_html)
    if d:
        problems.append(f"{lid}: {d}")

    # documented per-lesson adjudication: suppress a KNOWN gate false-positive, but ONLY if the lesson still
    # matches the adjudicated profile (guard) - so it can never mask a future genuinely-different defect.
    adj = ADJUDICATED.get(lid)
    if problems and adj and adj["guard"](L):
        return True, []

    return (not problems), problems


# ---------------------------------------------------------------------------
# grade runners (for a controller)
# ---------------------------------------------------------------------------

def _iter_lessons(grade):
    """Iterate LIVE lessons for a grade (same source of truth as the rest of the pipeline)."""
    subdir, pat = _GRADE_GLOB[grade]
    for f in sorted(glob.glob(os.path.join(ROOT, subdir, pat))):
        if "_deprecated" in f:
            continue
        m = _load(f)
        L = (getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0]) if m else None
        if L:
            yield f, L


def run_grade(grade) -> list:
    """[(lesson_id, problem)] for every mastery-alignment problem in a grade's live lessons."""
    out = []
    for _f, L in _iter_lessons(grade):
        ok, problems = check_mastery_alignment(L, grade)
        for p in problems:
            out.append((getattr(L, "id", "?"), p))
    return out


def run_all() -> dict:
    return {g: run_grade(g) for g in ("G9", "G10", "G11", "G12")}


def main():
    arg = (sys.argv[1] if len(sys.argv) > 1 else "all").upper()
    grades = ["G9", "G10", "G11", "G12"] if arg == "ALL" else [arg]
    print("=== MASTERY GENRE-MATCH + DOK-CONSISTENCY GATE (Tier A5) ===")
    total = 0
    for g in grades:
        lessons = list(_iter_lessons(g))
        checked = sum(1 for _f, L in lessons
                      if (getattr(L, "mastery", None) or _authored(g).get(getattr(L, "id", ""), {})).get("source")
                      and _rec((getattr(L, "mastery", None) or _authored(g).get(getattr(L, "id", ""), {})).get("source")))
        flags = run_grade(g)
        total += len(flags)
        print(f"\n{g}: {len(lessons)} live lessons ({checked} with a held-out mastery source)  |  {len(flags)} flag(s)")
        for lid, p in flags:
            print("   !! " + p)
    print(f"\nTOTAL mastery-alignment flags across {', '.join(grades)}: {total}")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
