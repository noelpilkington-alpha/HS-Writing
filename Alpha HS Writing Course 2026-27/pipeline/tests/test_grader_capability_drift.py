"""Drift test: the course's mirrored grader-capability set MUST match the grader's source of truth.

Regeneration contract (design: Writing_Test_Grader/Grading Standards Documentation/CCSS_G910/
Grading_Regeneration_Contract_DESIGN.md): grading routes off the declared (unit, frq_type) tuple. The GRADER
owns the SUPPORTED set (grader/engine/routing.py); the course mirrors it as GRADER_SUPPORTED_TUPLES so
gate_grader_routing can validate declared lesson tuples at authoring time. This test asserts the two copies
agree — if the grader adds/removes a supported combo, this fails until the course mirror is synced.

Follows the codebase's existing "duplicated set in both repos" pattern (RUBRIC_CONFIGS), adding the missing
equality guard so the copies can't silently drift.

The grader lives in a SEPARATE repo. If it isn't checked out alongside this course, the test SKIPS (so the
course suite still runs standalone) — but when both are present, drift is a hard failure.
"""
import importlib.util
import os
import sys
import unittest

from lesson_contract import GRADER_SUPPORTED_TUPLES  # the course's mirror

# Candidate locations of the grader repo (sibling checkouts / this machine's layout).
_CANDIDATES = [
    r"c:/Users/noelp/Writing_Test_Grader/grader/engine/routing.py",
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..",
                 "Writing_Test_Grader", "grader", "engine", "routing.py"),
]


def _load_grader_routing():
    for path in _CANDIDATES:
        if os.path.isfile(path):
            spec = importlib.util.spec_from_file_location("grader_routing", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
    return None


class TestGraderCapabilityDrift(unittest.TestCase):
    def test_course_mirror_matches_grader_source_of_truth(self):
        routing = _load_grader_routing()
        if routing is None:
            self.skipTest("grader repo not checked out alongside course; drift test skipped")
        grader_supported = set(routing.capability_manifest()["supported"])  # {"sentence:writing", ...}
        self.assertEqual(
            GRADER_SUPPORTED_TUPLES, grader_supported,
            "DRIFT: course GRADER_SUPPORTED_TUPLES != grader routing.SUPPORTED. "
            f"course-only={GRADER_SUPPORTED_TUPLES - grader_supported}  "
            f"grader-only={grader_supported - GRADER_SUPPORTED_TUPLES}. "
            "Sync lesson_contract.GRADER_SUPPORTED_TUPLES to the grader's capability_manifest().",
        )


if __name__ == "__main__":
    unittest.main()
