"""topic_seed_g10.py - the G10 topic partition seed.

Assigns every G10 stimulus topic to a pool so lessons and tests draw from DISJOINT topic sets (the hard
lesson-to-test contamination partition). The 15 topics behind the original bank become the TEST pool (the
6 argument propositions decomposed into stance singles + the info/analysis topics bound by CR test items);
the 9 new topics authored for the lesson bucket become the LESSON pool.

This is the ground-truth registry the loader/push layer consults to prove a lesson never binds a test topic
(and vice versa). Dependency-free (stdlib + topic_registry). Run: python pipeline/topic_seed_g10.py"""
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from topic_registry import TopicRegistry, Topic, POOL_TEST, POOL_LESSON

GRADE = "9-10"

# TEST pool: the topics behind the original 16-stimulus bank (now the test side).
TEST_TOPICS = {
    "energy": ["nuclear_power"],
    "labor": ["minimum_wage"],
    "transportation": ["ev_mandate"],
    "education_policy": ["school_start"],
    "technology_policy": ["social_media_age"],
    "science_funding": ["space_spending"],
    "ecology": ["coral_reefs", "pollinators", "wildfires"],
    "urban": ["heat_islands"],
    "civics_land": ["national_parks", "food_waste"],
    "rhetoric_pd": ["henry_speech", "chopin_prose", "reagan_challenger", "douglass_fourth"],
}

# LESSON pool: the 9 NEW topics authored for the lesson bucket (disjoint from every TEST topic).
LESSON_TOPICS = {
    "weather_science": ["nws_forecasting"],
    "materials": ["recycling_recovery"],
    "infrastructure": ["interstate_highways"],
    "ecology": ["wetlands_restoration"],            # different topic than the test-pool ecology topics
    "urban": ["congestion_pricing"],
    "education_policy": ["longer_school_year"],
    "time_policy": ["daylight_saving"],
    "rhetoric_pd": ["gettysburg_address", "fdr_infamy"],
}


def build() -> TopicRegistry:
    r = TopicRegistry()
    for domain, topics in TEST_TOPICS.items():
        for t in topics:
            r.add(Topic(topic_id=t, domain=domain, pool=POOL_TEST, grade=GRADE))
    for domain, topics in LESSON_TOPICS.items():
        for t in topics:
            r.add(Topic(topic_id=t, domain=domain, pool=POOL_LESSON, grade=GRADE))
    return r


if __name__ == "__main__":
    r = build()
    test_ids = set()
    for ts in TEST_TOPICS.values():
        test_ids |= set(ts)
    lesson_ids = set()
    for ls in LESSON_TOPICS.values():
        lesson_ids |= set(ls)

    # the whole point: the two pools must be DISJOINT (no topic is both lesson and test)
    overlap = test_ids & lesson_ids
    assert not overlap, f"CONTAMINATION: topics in both pools: {overlap}"
    assert len(test_ids) == 16, f"expected 16 test topics (the existing bank), got {len(test_ids)}"
    assert len(lesson_ids) == 9, f"expected 9 lesson topics (the new seed), got {len(lesson_ids)}"
    for t in test_ids:
        assert r.pool_of(t) == POOL_TEST
    for t in lesson_ids:
        assert r.pool_of(t) == POOL_LESSON
    print(f"topic_seed_g10: {len(test_ids)} test topics / {len(lesson_ids)} lesson topics, pools DISJOINT")
    print("topic_seed_g10 self-test PASS")
    sys.exit(0)
