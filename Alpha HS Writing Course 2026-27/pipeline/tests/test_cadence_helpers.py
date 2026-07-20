# pipeline/tests/test_cadence_helpers.py
import os, sys
PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path: sys.path.insert(0, PIPE)
from lesson_contract import Slot, Lesson, archetype_of, CADENCE_CEILING, MEMORIZABLE_TOOL_CEILING

def _L(lt): return Lesson(id="X", grade="9-10", lesson_type=lt, unit="U", title="T", target="t", slots=[])

def test_archetype_mapping():
    assert archetype_of(_L(1)) == "concept"
    assert archetype_of(_L(2)) == "concept"
    assert archetype_of(_L(3)) == "concept"
    assert archetype_of(_L(4)) == "concept"   # DEW text-dependent-analysis
    assert archetype_of(_L(6)) == "concept"
    assert archetype_of(_L(5)) == "checking_revision"
    assert archetype_of(_L(7)) == "full_essay_build"
    assert archetype_of(_L(8)) == "full_essay_build"

def test_ceilings():
    assert CADENCE_CEILING["concept"] == 3
    assert CADENCE_CEILING["checking_revision"] == 2
    assert CADENCE_CEILING["full_essay_build"] == 4
    assert MEMORIZABLE_TOOL_CEILING == 2

def test_slot_tag_defaults_empty_and_accepts_values():
    s = Slot("TEACH", "teach_card", "t")
    assert s.tag == ""
    s2 = Slot("TEACH", "teach_card", "t", tag="memorizable_tool")
    assert s2.tag == "memorizable_tool"
