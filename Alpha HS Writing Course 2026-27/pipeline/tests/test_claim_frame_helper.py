# pipeline/tests/test_claim_frame_helper.py
import os, sys
PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)
from lesson_prompts import claim_frame


def test_frame_has_no_comma_before_because():
    out = claim_frame("your side on the four-day week", "your reason")
    assert ", because" not in out
    assert "because" in out and "______" in out


def test_frame_carries_both_labels_and_stem():
    out = claim_frame("side X", "reason Y", stem="Districts should")
    assert "side X" in out and "reason Y" in out and "Districts should" in out
