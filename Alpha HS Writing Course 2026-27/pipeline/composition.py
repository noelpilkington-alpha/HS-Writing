"""composition.py - compose multi-source stimuli from tagged singles, on demand.

A pair is never authored as a unit; it is composed WITHIN a proposition (opposing) or a theme (complementary),
so combinability is guaranteed by construction. Opposing-pairs are purely structural (pick-a-side needs no
point-by-point rebuttal). Complementary-pairs add an optional combinability judge (an LLM at mint time) on top of
the structural connection_point check, because 'genuinely combines' is semantic. Stdlib only; the judge is injected."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class ComposedPair:
    family: str      # "opposing" | "complementary"
    left_id: str
    right_id: str
    source: str      # proposition_id or theme_id

def compose_opposing(prop_reg, proposition_id: str, lexile_window: int = 100,
                     len_ratio: float = 1.4) -> list[ComposedPair]:
    cands = prop_reg.opposing_candidates(proposition_id, lexile_window=lexile_window, len_ratio=len_ratio)
    return [ComposedPair("opposing", a.single_id, b.single_id, proposition_id) for a, b in cands]

def compose_complementary(theme_reg, theme_id: str, judge=None,
                          lexile_window: int = 100) -> list[ComposedPair]:
    cands = theme_reg.complementary_candidates(theme_id, lexile_window=lexile_window)
    out: list[ComposedPair] = []
    for a, b in cands:
        if judge is not None and not judge(a, b):
            continue
        out.append(ComposedPair("complementary", a.single_id, b.single_id, theme_id))
    return out


if __name__ == "__main__":
    import os, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from proposition_registry import PropositionRegistry, Single
    from theme_registry import ThemeRegistry, ThemeSingle

    pr = PropositionRegistry()
    pr.add(Single("p1", "prop_x", "pro", 1100, 300, "US EIA"))
    pr.add(Single("c1", "prop_x", "con", 1120, 310, "US GAO"))
    opp = compose_opposing(pr, "prop_x")
    assert len(opp) == 1 and opp[0].family == "opposing"
    assert opp[0].left_id == "p1" and opp[0].right_id == "c1" and opp[0].source == "prop_x"

    tr = ThemeRegistry()
    CP = "shared thread"
    tr.add(ThemeSingle("a", "theme_y", "causes", CP, 1100, 300))
    tr.add(ThemeSingle("b", "theme_y", "effects", CP, 1120, 310))
    # structural-only: 1 candidate
    comp = compose_complementary(tr, "theme_y")
    assert len(comp) == 1 and comp[0].family == "complementary"
    # with a judge that rejects everything: 0 admitted
    comp_rejected = compose_complementary(tr, "theme_y", judge=lambda l, r: False)
    assert comp_rejected == [], "combinability judge veto drops the pair"
    # with a judge that accepts: 1 admitted
    comp_ok = compose_complementary(tr, "theme_y", judge=lambda l, r: True)
    assert len(comp_ok) == 1
    print("composition self-test PASS")
    sys.exit(0)
