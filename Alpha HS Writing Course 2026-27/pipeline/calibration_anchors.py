"""calibration_anchors.py - human-scored anchor set that DEFINES on-grade test-form difficulty.

Test-form equivalence is anchored to human judgment, not sibling-pool statistics. Per {grade, mode, form} a human
scores a small reference set; the band is the min-max envelope of those anchors on each axis (Lexile, passage
count, task-demand 1-5). A candidate test stimulus is an equivalent form only if it sits inside the band on every
axis. Widening the band is a deliberate human act (add/adjust anchors), never a silent constant. Stdlib only."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Anchor:
    anchor_id: str
    grade: str
    mode: str
    form: str
    lexile: int
    passage_count: int
    task_demand: int   # human-assigned 1-5 profile

@dataclass
class Band:
    lexile_min: int
    lexile_max: int
    passage_count: int
    demand_min: int
    demand_max: int

class AnchorSet:
    def __init__(self) -> None:
        self._anchors: list[Anchor] = []

    def add(self, anchor: Anchor) -> None:
        self._anchors.append(anchor)

    def _for(self, grade: str, mode: str, form: str) -> list[Anchor]:
        return [a for a in self._anchors if a.grade == grade and a.mode == mode and a.form == form]

    def band(self, grade: str, mode: str, form: str) -> Band | None:
        rows = self._for(grade, mode, form)
        if not rows:
            return None
        pcs = {a.passage_count for a in rows}
        # anchors for one form should agree on passage_count; take the common value (min if human error)
        pc = min(pcs)
        return Band(
            lexile_min=min(a.lexile for a in rows),
            lexile_max=max(a.lexile for a in rows),
            passage_count=pc,
            demand_min=min(a.task_demand for a in rows),
            demand_max=max(a.task_demand for a in rows),
        )

    def equivalent_form_ok(self, grade: str, mode: str, form: str,
                           lexile: int, passage_count: int, task_demand: int) -> tuple[bool, str]:
        band = self.band(grade, mode, form)
        if band is None:
            return False, f"no anchor set for {grade}/{mode}/{form}; cannot certify equivalence"
        if not (band.lexile_min <= lexile <= band.lexile_max):
            return False, f"lexile {lexile} outside anchor band {band.lexile_min}-{band.lexile_max}"
        if passage_count != band.passage_count:
            return False, f"passage_count {passage_count} != anchor {band.passage_count}"
        if not (band.demand_min <= task_demand <= band.demand_max):
            return False, f"task_demand {task_demand} outside anchor band {band.demand_min}-{band.demand_max}"
        return True, "inside anchor band on every axis"


if __name__ == "__main__":
    a = AnchorSet()
    # two human-scored anchors define the STAAR argument band
    a.add(Anchor("anc1", "9-10", "argument", "staar", lexile=1080, passage_count=2, task_demand=3))
    a.add(Anchor("anc2", "9-10", "argument", "staar", lexile=1160, passage_count=2, task_demand=4))
    band = a.band("9-10", "argument", "staar")
    assert band.lexile_min == 1080 and band.lexile_max == 1160
    assert band.passage_count == 2 and band.demand_min == 3 and band.demand_max == 4
    ok, _ = a.equivalent_form_ok("9-10", "argument", "staar", lexile=1120, passage_count=2, task_demand=3)
    assert ok, "inside band on every axis -> ok"
    bad_lex, why = a.equivalent_form_ok("9-10", "argument", "staar", lexile=1300, passage_count=2, task_demand=3)
    assert not bad_lex and "lexile" in why.lower()
    bad_pc, _ = a.equivalent_form_ok("9-10", "argument", "staar", lexile=1120, passage_count=1, task_demand=3)
    assert not bad_pc, "wrong passage count -> fail"
    none_band = a.band("9-10", "argument", "mcas")
    assert none_band is None, "no anchors for that form -> None"
    print("calibration_anchors self-test PASS")
    import sys; sys.exit(0)
