"""theme_registry.py - complementary-pair composition backbone.

A theme is one topic several passages illuminate from different facets. Complementary singles are tagged with
theme_id + facet + a connection_point (the one idea joining them). A complementary pair = two singles, same theme,
DIFFERENT facets, SAME connection_point. This is the structural proxy for combinability; a semantic combinability
judge is applied downstream in composition.py. Stdlib only."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class ThemeSingle:
    single_id: str
    theme_id: str
    facet: str
    connection_point: str
    lexile: int
    words: int

class ThemeRegistry:
    def __init__(self) -> None:
        self._by_theme: dict[str, list[ThemeSingle]] = {}

    def add(self, single: ThemeSingle) -> None:
        self._by_theme.setdefault(single.theme_id, []).append(single)

    def singles(self, theme_id: str) -> list[ThemeSingle]:
        return list(self._by_theme.get(theme_id, []))

    def complementary_candidates(self, theme_id: str,
                                 lexile_window: int = 100) -> list[tuple[ThemeSingle, ThemeSingle]]:
        rows = self.singles(theme_id)
        out: list[tuple[ThemeSingle, ThemeSingle]] = []
        for i in range(len(rows)):
            for j in range(i + 1, len(rows)):
                a, b = rows[i], rows[j]
                if a.facet == b.facet:
                    continue
                if not a.connection_point or a.connection_point != b.connection_point:
                    continue
                if abs(a.lexile - b.lexile) > lexile_window:
                    continue
                out.append((a, b))
        return out


if __name__ == "__main__":
    r = ThemeRegistry()
    T = "theme_pollinators"
    CP = "pollinator decline threatens the food supply"
    r.add(ThemeSingle("t1", T, "causes", CP, 1100, 300))
    r.add(ThemeSingle("t2", T, "consequences", CP, 1130, 310))
    r.add(ThemeSingle("t3", T, "causes", CP, 1110, 305))          # same facet as t1 -> not with t1
    r.add(ThemeSingle("t4", T, "solutions", "unrelated thread", 1120, 300))  # different connection_point
    cands = r.complementary_candidates(T, lexile_window=100)
    ids = {frozenset((a.single_id, b.single_id)) for a, b in cands}
    assert frozenset(("t1", "t2")) in ids, "different facet + shared connection_point -> candidate"
    assert frozenset(("t1", "t3")) not in ids, "same facet -> excluded"
    assert all("t4" not in {a.single_id, b.single_id} for a, b in cands), "different connection_point -> excluded"
    assert all(a.facet != b.facet for a, b in cands)
    print("theme_registry self-test PASS")
    import sys; sys.exit(0)
