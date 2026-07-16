"""Load the G9 v3.1 course in sequence and render each lesson to the DEVELOPMENT-FREE
student experience. Students see student_view(L) output ONLY - never the Lesson object,
the .py source, or any internal id/label."""
import os, sys, glob, importlib.util

HERE = os.path.dirname(__file__)
PIPE = os.path.join(HERE, "..")           # Alpha HS Writing Course 2026-27/pipeline
ROOT = os.path.join(PIPE, "..")           # Alpha HS Writing Course 2026-27
sys.path.insert(0, PIPE)

import lesson_review  # noqa: E402  (import side effects wire STIM + gated_reading)


def _load_module(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def load_g9_lessons() -> list:
    lessons = []
    pattern = os.path.join(ROOT, "Lesson_Bank_G9", "lesson_g9_l*_v3_1.py")
    for f in sorted(glob.glob(pattern)):
        m = _load_module(f)
        L = getattr(m, "LESSON", None) or (getattr(m, "LESSONS", [None]) or [None])[0]
        if L is not None:
            L._src_file = os.path.basename(f)  # for short_id; not shown to students
            lessons.append(L)
    return lessons


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
