"""Load a grade's v3.1 course in sequence and render each lesson to the DEVELOPMENT-FREE
student experience. Students see student_view(L) output ONLY - never the Lesson object,
the .py source, or any internal id/label.

Grade globs differ by how each grade was built: G9's v3.1 lessons are `_v3_1.py` SIBLINGS of the
originals; G10-G12 were rebuilt IN-PLACE, so their v3.1 lessons ARE the canonical
`lesson_g{gr}_l*.py` (no version suffix, and no legacy `_v*` siblings remain in those dirs)."""
import os, sys, glob, importlib.util, re

HERE = os.path.dirname(__file__)
PIPE = os.path.join(HERE, "..")           # Alpha HS Writing Course 2026-27/pipeline
ROOT = os.path.join(PIPE, "..")           # Alpha HS Writing Course 2026-27
sys.path.insert(0, PIPE)

import lesson_review  # noqa: E402  (import side effects wire STIM + gated_reading)

GRADES = ("g9", "g10", "g11", "g12")

# per-grade (bank dir, filename glob). G9 selects the _v3_1 siblings; G10-G12 select canonical files.
_GRADE_SPEC = {
    "g9":  ("Lesson_Bank_G9",  "lesson_g9_l*_v3_1.py"),
    "g10": ("Lesson_Bank_G10", "lesson_g10_l*.py"),
    "g11": ("Lesson_Bank_G11", "lesson_g11_l*.py"),
    "g12": ("Lesson_Bank_G12", "lesson_g12_l*.py"),
}
# canonical grades must exclude any legacy versioned siblings that a future edit might add back
_LEGACY_VERSION_RE = re.compile(r"_v[0-9]")


def _load_module(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _sort_key(path):
    """Order by the lesson number in the filename (l01..l31), not lexically (so l2 < l10)."""
    m = re.search(r"_l(\d+)", os.path.basename(path))
    return int(m.group(1)) if m else 0


def load_lessons(grade: str) -> list:
    grade = grade.lower()
    if grade not in _GRADE_SPEC:
        raise ValueError(f"unknown grade {grade!r}; expected one of {GRADES}")
    bank, pat = _GRADE_SPEC[grade]
    lessons = []
    for f in sorted(glob.glob(os.path.join(ROOT, bank, pat)), key=_sort_key):
        base = os.path.basename(f)
        # G9's pattern already pins _v3_1; for canonical grades, skip any legacy _v2/_v3 sibling
        if grade != "g9" and _LEGACY_VERSION_RE.search(base[:-3]):
            continue
        m = _load_module(f)
        L = getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0]
        if L is not None:
            L._src_file = base  # for short_id; not shown to students
            lessons.append(L)
    return lessons


def load_g9_lessons() -> list:
    """Back-compat wrapper (kept so existing G9 callers/tests are unchanged)."""
    return load_lessons("g9")


def short_id(L) -> str:
    stem = getattr(L, "_src_file", "") or ""
    stem = stem[:-3] if stem.endswith(".py") else stem
    if stem.startswith("lesson_"):
        stem = stem[len("lesson_"):]
    if stem.endswith("_v3_1"):
        stem = stem[:-len("_v3_1")]
    return stem


def student_view(L) -> str:
    return lesson_review.render_student_experience(L)
