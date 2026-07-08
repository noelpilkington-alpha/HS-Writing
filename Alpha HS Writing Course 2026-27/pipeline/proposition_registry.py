"""proposition_registry.py - opposing-pair composition backbone.

A proposition is one arguable question. Argumentative SINGLE passages are tagged with proposition_id + stance.
An opposing pair is composed by picking one pro + one con UNDER THE SAME proposition, with Lexile/length parity
and distinct source orgs. Same-question-opposite-side is mechanical, not a human judgment. Stdlib only."""
from __future__ import annotations
from dataclasses import dataclass

VALID_STANCES = {"pro", "con", "nuanced"}

@dataclass
class Single:
    single_id: str
    proposition_id: str
    stance: str
    lexile: int
    words: int
    source_org: str

class PropositionRegistry:
    def __init__(self) -> None:
        self._by_prop: dict[str, list[Single]] = {}

    def add(self, single: Single) -> None:
        if single.stance not in VALID_STANCES:
            raise ValueError(f"bad stance '{single.stance}' (must be one of {VALID_STANCES})")
        self._by_prop.setdefault(single.proposition_id, []).append(single)

    def singles(self, proposition_id: str, stance: str | None = None) -> list[Single]:
        rows = self._by_prop.get(proposition_id, [])
        return [s for s in rows if stance is None or s.stance == stance]

    def opposing_candidates(self, proposition_id: str, lexile_window: int = 100,
                            len_ratio: float = 1.4) -> list[tuple[Single, Single]]:
        pros = self.singles(proposition_id, "pro")
        cons = self.singles(proposition_id, "con")
        out: list[tuple[Single, Single]] = []
        for a in pros:
            for b in cons:
                if abs(a.lexile - b.lexile) > lexile_window:
                    continue
                hi, lo = max(a.words, b.words), min(a.words, b.words)
                if lo == 0 or hi / lo > len_ratio:
                    continue
                if a.source_org == b.source_org:
                    continue
                out.append((a, b))
        return out


if __name__ == "__main__":
    r = PropositionRegistry()
    P = "prop_nuclear"
    r.add(Single("s_pro1", P, "pro", 1120, 300, "US EIA"))
    r.add(Single("s_con1", P, "con", 1150, 320, "US GAO"))
    r.add(Single("s_con2", P, "con", 1400, 900, "US GAO"))   # too hard + too long -> excluded
    r.add(Single("s_pro2", P, "pro", 1130, 305, "US EIA"))   # same org as s_pro1 (n/a, pro vs con only)
    cands = r.opposing_candidates(P, lexile_window=100, len_ratio=1.4)
    ids = {(a.single_id, b.single_id) for a, b in cands}
    assert ("s_pro1", "s_con1") in ids, "close pro/con, distinct orgs -> candidate"
    assert all("s_con2" not in pair for pair in ids), "s_con2 out of Lexile/len window -> excluded"
    assert all(a.stance == "pro" and b.stance == "con" for a, b in cands)
    assert all(a.source_org != b.source_org for a, b in cands), "distinct orgs required"
    print("proposition_registry self-test PASS")
    import sys; sys.exit(0)
