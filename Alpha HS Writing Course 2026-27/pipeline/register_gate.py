"""
register_gate.py  -  Tier A7 REGISTER / CREDIBILITY gate for the G9-G12 writing course.

WHY (Noel + the Fable eval, this session): student-facing lesson text sometimes drifts into two
register failures that break credibility with a real high-school reader:

  (a) META / CHILDISH OPENERS - a body that opens by narrating the lesson to the student instead
      of getting to work: "The topic here is how volcanoes form", "Today we will learn...",
      "This passage is about...", "Boys and girls,...". Elementary-worksheet voice; a G9-12 reader
      reads it as talking down.

  (b) AUDITOR / DESIGN JARGON leaked into student text - QC/instructional-design vocabulary that is
      meant for the build pipeline and its reviewers, never for a student: "Grade-C design bet",
      "distractor", "minimal pair", "coping model", "scaffold", "we label ... a bet", "the correct
      option", "confound". These are the words WE use ABOUT the lesson; a student seeing them is a
      tell that internal notes leaked into the delivered copy (exactly the Fable catch:
      "a Grade-C design bet we label as a bet" sitting in student-visible text).

  (c) (conservative readability signal) a teach_card body whose LONGEST single sentence runs past
      the run-on threshold - a wall/overload tell. Kept deliberately narrow (teach cards only, real
      sentence-segmented count, block boundaries broken so a merged <li> list is NOT mistaken for a
      run-on) so it flags GENUINE run-ons, not dense-but-fine prose. The threshold is set ABOVE the
      natural top of the healthy live corpus (dense AP colon-structured teach sentences legitimately
      reach ~46 words) precisely to avoid the documented over-flag failure mode; it exists to catch a
      future 60+-word wall, not to trim the current clean corpus.

SCOPE (the load-bearing constraint - this is what stops over-flagging): this gate reads ONLY
student-FACING slot text - the body of teach_card / stimulus_display / production_frq /
diagnosis_frq / self_score slots, and the CHOICE texts of discrimination / predict_the_fix slots.
It NEVER reads provenance dicts, version notes, authoring comments, choice rationales ("why"), or
this module's own docstring - all places where "distractor", "scaffold", "Grade-C design bet",
"confound" legitimately appear as the build team's own vocabulary. The jargon terms are banned in
what a student sees, not in how we describe the design to ourselves.

API:
  check_register(L) -> (passed: bool, flags: list[str])   # per-lesson; passed == (flags == [])
  run_grade(grade)  -> list[(lesson_id, flag)]            # for a controller: all catches in a grade
  run_all()         -> dict[grade -> list[(lesson_id, flag)]]

Run: python pipeline/register_gate.py [G9|G10|G11|G12|all]   -> per-grade counts + catches, exit-coded.
"""
from __future__ import annotations
import os, sys, re, html, glob

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)

# Slot kinds whose BODY is student-facing prose we scan for openers + jargon + (teach only) readability.
_BODY_KINDS = {"teach_card", "stimulus_display", "production_frq", "diagnosis_frq", "self_score"}
# Slot kinds whose structured CHOICE texts are student-facing (the option a student reads + picks).
_CHOICE_KINDS = {"discrimination", "predict_the_fix"}

# teach_card run-on threshold. Set at 55, ABOVE the natural top of the healthy live corpus (longest
# clean live teach sentence = 46 words, dense AP colon-lists), so this flags a genuine wall (a 55+-word
# run-on) and never trims coherent-but-dense prose. Deliberately conservative per the documented
# over-flag failure mode.
_LONGEST_SENTENCE_WORDS = 55

# Meta/childish openers are only a defect when they OPEN the body (talk-down first impression). A
# "This lesson is about ..." signpost mid-body, AFTER real teaching content, is a legitimate move and
# must not flag. So opener matching is restricted to the first _OPENER_WINDOW sentence-units of a body
# (a short lead-in region: a callout label + the first line or two).
_OPENER_WINDOW = 3

# ---- (a) META / CHILDISH OPENERS (curated; matched only at a sentence start) -----------------
# Each pattern is anchored at the (punctuation-stripped) start of a sentence. Kept tight and specific
# so ordinary teaching prose ("In this lesson you will practice...", a callout label "The one idea")
# does NOT trip it - only the narrate-the-lesson / talk-down openers do.
_META_OPENERS = [
    r"the topic here is\b",
    r"the topic\s*:",
    r"the topic of (?:this|today'?s) (?:lesson|passage|reading)\b",
    r"today,?\s+we(?:'ll| will| are going to| are gonna| shall| start| begin)\b",
    r"today,?\s+we're\s+going to\b",
    r"let'?s\s+(?:learn|explore|dive|begin|get started|find out|talk about|discover)\b",
    r"let us\s+(?:learn|explore|begin|discover)\b",
    r"in this lesson,?\s+we\b",
    r"in this passage,?\s+we\b",
    # "This passage/reading is about ..." = elementary reading-comprehension voice (childish). NOTE:
    # "This lesson is about ..." is deliberately NOT listed - the live corpus uses it as a legitimate
    # signpost, and flagging it is the documented over-flag mode.
    r"this passage is about\b",
    r"this reading is about\b",
    r"boys and girls\b",
    r"welcome,?\s+(?:class|students|everyone|kids|boys)\b",
    r"(?:okay|ok|alright|hello|hi),?\s+(?:class|kids|everyone|students|boys)\b",
    r"class,?\s+today\b",
]
_META_RE = [re.compile(p, re.I) for p in _META_OPENERS]

# ---- (b) AUDITOR / DESIGN JARGON (banned only in student-facing text) ------------------------
# (label, compiled-regex). Word-boundaried and specific to the internal-vocabulary sense.
_JARGON = [
    ("Grade-<letter> design label", re.compile(r"\bgrade-[a-f]\b", re.I)),
    ("design bet",                   re.compile(r"\bdesign[-\s]bets?\b", re.I)),
    ("distractor",                   re.compile(r"\bdistractors?\b", re.I)),
    ("minimal pair",                 re.compile(r"\bminimal[-\s]pairs?\b", re.I)),
    ("coping model",                 re.compile(r"\bcoping[-\s]model", re.I)),
    ("scaffold",                     re.compile(r"\bscaffold(?:s|ing|ed)?\b", re.I)),
    ("'the correct option'",         re.compile(r"\bthe correct option\b", re.I)),
    ("'we label'",                   re.compile(r"\bwe label\b", re.I)),
    ("confound",                     re.compile(r"\bconfound(?:s|ed|ing)?\b", re.I)),
]

_LEAD_STRIP = re.compile(r"^[\s\"'*‘’“”\-–—:;>()\[\]#|]+")


def _blockify(h: str) -> str:
    """Insert a hard break at every block boundary so a bulleted list / paragraph break becomes a
    sentence boundary (a merged <li> wall is NOT then read as one giant run-on sentence)."""
    h = re.sub(r"<\s*br\s*/?\s*>", "\n", h, flags=re.I)
    h = re.sub(r"</\s*(?:p|li|div|ol|ul|h[1-6]|tr|td|th|section|blockquote)\s*>", "\n", h, flags=re.I)
    return h


def _plain(h: str) -> str:
    """HTML -> plain text (tags dropped, entities decoded, whitespace collapsed). Tags become spaces
    so adjacent words never fuse into a false compound."""
    if not h:
        return ""
    t = re.sub(r"<[^>]+>", " ", h)
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def _sentences(h: str) -> list[str]:
    """Student-visible text split into sentence-start units: block boundaries AND [.!?] both split.
    Used for start-of-sentence opener matching and for the longest-sentence readability count."""
    t = _blockify(h)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    parts = re.split(r"(?<=[.!?])\s+|\n+", t)
    return [re.sub(r"\s+", " ", p).strip() for p in parts if p.strip()]


def _slot_units(L):
    """Yield (idx, kind, label, text) student-facing units to scan.
    label distinguishes a body from a specific choice for the flag message."""
    for i, s in enumerate(L.slots):
        kind = getattr(s, "kind", "")
        if kind in _BODY_KINDS:
            yield i, kind, "body", getattr(s, "body", "") or ""
        if kind in _CHOICE_KINDS:
            # scan ONLY the structured choice TEXT a student reads (not the "why" rationale, which is
            # authoring/feedback voice where design terms can legitimately appear).
            for c in getattr(s, "choices", None) or []:
                cid = c.get("id", "?")
                yield i, kind, f"choice {cid}", c.get("text", "") or ""


def _check_openers(sentences: list[str]) -> list[str]:
    """Match a curated meta/childish opener at the START of a sentence, but only within the body's
    opening window (a talk-down FIRST impression). A signpost that appears mid-body, after real
    teaching, is legitimate and is intentionally not flagged."""
    hits = []
    for sent in sentences[:_OPENER_WINDOW]:
        head = _LEAD_STRIP.sub("", sent)
        for rx in _META_RE:
            if rx.match(head):
                hits.append(head[:70])
                break
    return hits


def _check_jargon(plain: str) -> list[str]:
    hits = []
    for label, rx in _JARGON:
        m = rx.search(plain)
        if m:
            hits.append(f"{label} ('{m.group(0)}')")
    return hits


def check_register(L) -> tuple[bool, list[str]]:
    """Register/credibility gate on one Lesson. Returns (passed, flags). passed == (flags == [])."""
    flags: list[str] = []
    lid = getattr(L, "id", "?")
    for idx, kind, label, text in _slot_units(L):
        if not text.strip():
            continue
        where = f"slot {idx} {kind} {label}"
        # (b) jargon anywhere in the student-facing unit
        for j in _check_jargon(_plain(text)):
            flags.append(f"{lid} [{where}]: auditor/design jargon leaked - {j}")
        if label == "body":
            sents = _sentences(text)
            # (a) meta/childish opener at a sentence start
            for op in _check_openers(sents):
                flags.append(f"{lid} [{where}]: meta/childish opener - \"{op}\"")
            # (c) teach_card readability: longest single sentence > ~45 words (run-on/overload tell)
            if kind == "teach_card" and sents:
                longest = max(sents, key=lambda x: len(x.split()))
                n = len(longest.split())
                if n > _LONGEST_SENTENCE_WORDS:
                    flags.append(f"{lid} [{where}]: run-on teach sentence ({n} words > "
                                 f"{_LONGEST_SENTENCE_WORDS}) - \"{longest[:60]}...\"")
    return (not flags), flags


# ---- grade runners (for a controller) --------------------------------------------------------

def _iter_lessons(grade):
    """Iterate LIVE lessons for a grade (same source of truth as the rest of the pipeline)."""
    from g9_push_dryrun import _load
    from mastery_targets_grade import _GRADE_GLOB
    subdir, pat = _GRADE_GLOB[grade]
    for f in sorted(glob.glob(os.path.join(ROOT, subdir, pat))):
        if "_deprecated" in f:
            continue
        m = _load(f)
        L = getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0] if m else None
        if L:
            yield f, L


def run_grade(grade) -> list:
    """[(lesson_id, flag)] for every register flag in a grade's live lessons."""
    out = []
    for _f, L in _iter_lessons(grade):
        ok, flags = check_register(L)
        for fl in flags:
            out.append((getattr(L, "id", "?"), fl))
    return out


def run_all() -> dict:
    return {g: run_grade(g) for g in ("G9", "G10", "G11", "G12")}


def main():
    arg = (sys.argv[1] if len(sys.argv) > 1 else "all").upper()
    grades = ["G9", "G10", "G11", "G12"] if arg == "ALL" else [arg]
    print("=== REGISTER / CREDIBILITY GATE (Tier A7) ===")
    total = 0
    for g in grades:
        lessons = list(_iter_lessons(g))
        flags = run_grade(g)
        total += len(flags)
        print(f"\n{g}: {len(lessons)} live lessons scanned  |  {len(flags)} flag(s)")
        for lid, fl in flags:
            print("   !! " + fl)
    print(f"\nTOTAL register flags across {', '.join(grades)}: {total}")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
