import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lesson_contract import Slot
from gated_reading import frq_xml

SRC = ["A Title", "Para one is long. " * 30, "Para two is also long. " * 30]


def _prompt(xml):
    return re.search(r"<qti-prompt>(.*)</qti-prompt>", xml, re.S).group(1)


def test_boxed_source_wraps_in_capped_scroller():
    s = Slot(role="TRANSFER", kind="production_frq", title="Write", body="Write the essay.",
             unit="essay", rubric_ref="rc.ap", scored=True)
    xml = frq_xml("frq-x", s, source_text=SRC, boxed_source=True)
    p = _prompt(xml)
    assert "overflow:auto" in p and "max-height:" in p, "boxed source must be a capped scroller"


def test_default_source_unchanged():
    s = Slot(role="SUPPORTED", kind="production_frq", title="Write", body="Write.", unit="sentence",
             rubric_ref="rc.staar", scored=True)
    xml = frq_xml("frq-y", s, source_text=SRC)  # boxed_source defaults False
    p = _prompt(xml)
    assert "overflow:auto" not in p, "short-grain source must not be boxed"


def test_boxed_still_contains_the_source_text():
    s = Slot(role="TRANSFER", kind="production_frq", title="Write", body="Write.", unit="essay",
             rubric_ref="rc.ap", scored=True)
    p = _prompt(frq_xml("frq-z", s, source_text=SRC, boxed_source=True))
    assert "A Title" in p and "Para one is long." in p, "boxed source must still render the full source text"


def test_multi_paragraph_outline_slot_is_boxed_in_build():
    # the essay template's SUPPORTED outline slot has unit=multi_paragraph -> it should get a boxed source.
    import re as _re, sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from lesson_contract import Lesson
    from gated_reading import build_lesson_html
    from g9_push_dryrun import STIM
    src_id = next(iter(STIM))  # any real bound stimulus
    L = Lesson(id="X-MP", grade="9-10", lesson_type=7, unit="U", title="T", target="t",
               lesson_class="practice",
               slots=[
                   Slot(role="MODEL", kind="stimulus_display", title="Src", ref=src_id, bank="a"),
                   Slot(role="SUPPORTED", kind="production_frq", title="Outline", body="Outline the essay.",
                        unit="multi_paragraph", bank="a", rubric_ref="rc.staar", scored=True),
               ])
    _html, cps = build_lesson_html(L, base_url="https://x")
    frq = [x for _id, x in cps if "frq-" in _id][0]
    assert "overflow:auto" in frq, "multi_paragraph outline slot must box its source"
