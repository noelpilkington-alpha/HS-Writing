"""topic_registry.py - topic partition + reservation for the two-bucket stimulus layer.

A topic is coarser than a passage (one topic supports many passages). Each topic is assigned to a pool:
lesson-only, test-only, or shared. Test gets first claim on a domain's topics (test needs unseen-per-student
depth and cannot borrow lesson topics). Dependency-free (stdlib only)."""
from __future__ import annotations
from dataclasses import dataclass

POOL_LESSON = "lesson_pool"
POOL_TEST = "test_pool"
POOL_SHARED = "shared_ok"

@dataclass
class Topic:
    topic_id: str
    domain: str
    pool: str
    grade: str

class TopicRegistry:
    def __init__(self) -> None:
        self._topics: dict[str, Topic] = {}

    def add(self, topic: Topic) -> None:
        self._topics[topic.topic_id] = topic

    def reserve_test_first(self, domain: str, topic_ids: list[str], grade: str, n_test: int) -> None:
        for i, tid in enumerate(topic_ids):
            pool = POOL_TEST if i < n_test else POOL_LESSON
            self.add(Topic(topic_id=tid, domain=domain, pool=pool, grade=grade))

    def pool_of(self, topic_id: str) -> str | None:
        t = self._topics.get(topic_id)
        return t.pool if t else None

    def topics_for(self, pool: str, grade: str, domain: str | None = None) -> list[str]:
        return [t.topic_id for t in self._topics.values()
                if t.pool == pool and t.grade == grade and (domain is None or t.domain == domain)]

    def starvation(self, grade: str, domain: str, bucket_pool: str, projected_use: int) -> dict:
        remaining = len(self.topics_for(bucket_pool, grade, domain))
        return {"remaining": remaining, "alarm": remaining < projected_use}


if __name__ == "__main__":
    r = TopicRegistry()
    r.reserve_test_first("energy", ["nuclear_power", "solar", "wind", "coal"], "9-10", n_test=2)
    assert r.pool_of("nuclear_power") == POOL_TEST, "first reserved -> test"
    assert r.pool_of("wind") == POOL_LESSON, "remainder -> lesson"
    assert set(r.topics_for(POOL_TEST, "9-10", "energy")) == {"nuclear_power", "solar"}
    assert r.pool_of("unknown") is None
    st = r.starvation("9-10", "energy", POOL_TEST, projected_use=5)
    assert st["remaining"] == 2 and st["alarm"] is True, "2 test topics < 5 projected -> alarm"
    st2 = r.starvation("9-10", "energy", POOL_TEST, projected_use=1)
    assert st2["alarm"] is False
    print("topic_registry self-test PASS")
    import sys; sys.exit(0)
