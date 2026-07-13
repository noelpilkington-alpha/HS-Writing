"""contamination_check.py - prove no lesson is contaminated by a test-pool stimulus.

The two-bucket architecture's core guarantee: a student never learns on a passage (or topic) they are later
tested on. This checker makes that STRUCTURAL, not a one-off grep. For every lesson, it resolves each bound
stimulus ref to its stimulus, reads that stimulus's topic_id, and looks up the topic's pool in the G10 topic
seed. A lesson binding any stimulus whose topic is in the TEST pool is a contamination violation.

Also flags a lesson binding a stimulus that is itself bucket="test" (belt and suspenders).

Dependency-free (stdlib + sibling modules). Run: python pipeline/contamination_check.py"""
from __future__ import annotations
import os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from bank_loader import load_bank
from topic_seed_g10 import build as build_topic_seed
from topic_registry import POOL_TEST

# The original test-bank stimulus + item IDs are test-pool BY CONSTRUCTION (they predate the topic_id field,
# so they carry no topic tag and a topic-only check is blind to them). A lesson must never bind these.
# Lesson-pool stimuli use the *-LESSON-* / ARG-SINGLE-<topic>-PRO/CON id shapes, which these patterns exclude.
TEST_ID_PATTERNS = [
    re.compile(r"^ACC-W910-INFO-SINGLE-\d{4}$"),      # original explanatory test stimuli
    re.compile(r"^ACC-W910-ARG-OPP-\d{4}$"),          # original opposing-pair test stimuli
    re.compile(r"^ACC-W910-ANALYSIS-SINGLE-\d{4}$"),  # original analysis test stimuli
    re.compile(r"^ACC-W910-CR-[A-Z]+-\d{4}$"),        # constructed-response TEST items
]

def _is_test_family(ref: str) -> bool:
    return any(p.match(ref) for p in TEST_ID_PATTERNS)


def check() -> dict:
    ir = load_bank()
    topics = build_topic_seed()

    # id -> topic_id for every stimulus (monolithic + singles)
    stim_topic = {}
    for s in (ir.stimuli + ir.singles):
        stim_topic[s.id] = getattr(s, "topic_id", "")
        # also record bucket for the belt-and-suspenders check
    stim_bucket = {s.id: getattr(s, "bucket", "lesson") for s in (ir.stimuli + ir.singles)}

    violations = []
    lesson_bound_total = 0
    for L in ir.lessons:
        for slot in L.slots:
            ref = getattr(slot, "ref", "")
            if not ref:
                continue  # authored connective slot
            lesson_bound_total += 1
            # 1) known test-family ID by construction (catches the original untagged test stimuli + CR items)
            if _is_test_family(ref):
                violations.append((L.id, slot.role, ref, stim_topic.get(ref, ""), "test-family id (by construction)"))
                continue
            # 2) resolves to a stimulus whose topic is in the TEST pool
            tid = stim_topic.get(ref, "")
            pool = topics.pool_of(tid) if tid else None
            if pool == POOL_TEST:
                violations.append((L.id, slot.role, ref, tid, "topic in TEST pool"))
            # 3) resolves to a stimulus explicitly tagged bucket=test
            elif stim_bucket.get(ref) == "test":
                violations.append((L.id, slot.role, ref, tid, "stimulus bucket=test"))
    return {"violations": violations, "lessons": len(ir.lessons),
            "lesson_bindings_checked": lesson_bound_total}


if __name__ == "__main__":
    r = check()
    print(f"lessons: {r['lessons']}  |  lesson bindings checked: {r['lesson_bindings_checked']}")
    if r["violations"]:
        print(f"CONTAMINATION FOUND ({len(r['violations'])}):")
        for lid, role, ref, tid, why in r["violations"]:
            print(f"  {lid} [{role}] binds {ref} (topic {tid or '?'}) -> {why}")
        sys.exit(1)
    print("NO CONTAMINATION: no lesson binds a test-pool stimulus. PASS")
    sys.exit(0)
