# pipeline/tests/test_incept_diagram.py
# All tests run live=False / no network.
import os, sys
import pytest

PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)

from incept_diagram import request_diagram, verify_drawio
from incept_diagrams import INCEPT_DIAGRAMS
from gated_reading import _content_card

PROBE_DRAWIO = "C:/tmp/incept_probe/arguable_claim.drawio"


def test_verify_drawio_passes_on_probe_labels():
    # SIDE, REASON, ARGUABLE CLAIM all appear verbatim as value="..." substrings in the probe.
    assert verify_drawio(PROBE_DRAWIO, ["SIDE", "REASON", "ARGUABLE CLAIM"]) is True


def test_verify_drawio_fails_on_absent_label():
    with pytest.raises(AssertionError):
        verify_drawio(PROBE_DRAWIO, ["SIDE", "TOTALLY_ABSENT_LABEL"])


def test_request_diagram_dry_is_image_drawio():
    spec = {"prompt": "teach the arguable-claim formula", "expected_labels": ["SIDE", "REASON"]}
    r = request_diagram(spec, live=False)
    assert r["status"] == "dry"
    assert r["would_send"]["generation_type"] == "image"
    assert r["would_send"]["options"]["image_subtype"] == "drawio"
    assert r["request_id"] is None


def test_registry_ships_empty():
    assert isinstance(INCEPT_DIAGRAMS, dict)
    assert INCEPT_DIAGRAMS == {}


def test_content_card_img_path_renders():
    out = _content_card("Title", ["a paragraph"], "idref-1",
                        ("#e7e4ff", "#f6f2ff", "#3b3a88"),
                        img=("foo.png", "alt text"))
    assert "<img" in out
    assert "alt text" in out
