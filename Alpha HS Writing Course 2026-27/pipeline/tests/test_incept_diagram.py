# pipeline/tests/test_incept_diagram.py
# All tests run live=False / no network.
import os, sys
import pytest

PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)

from incept_diagram import request_diagram, verify_drawio, fetch
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


class _FilesArtifactStub:
    """Mimics the REAL drawio artifact shape (confirmed live 2026-07-20): files[] presigned pairs +
    output_json caption/alt_text + top-level below_bar/judge_score. download() returns synthetic bytes
    so the test never hits the network (fetch is called live=True but curl is monkeypatched out)."""
    def artifact(self, artifact_id, live=False):
        return {
            "below_bar": False, "judge_score": 100.0,
            "output_json": {"caption": "read left to right", "alt_text": "SIDE plus REASON"},
            "files": [
                {"filename": "claim_formula.drawio", "url": "https://s3/presigned/claim.drawio?sig=x"},
                {"filename": "claim_formula.png", "url": "https://s3/presigned/claim.png?sig=y"},
            ],
        }


def test_fetch_downloads_files_from_presigned_urls(tmp_path, monkeypatch):
    import incept_diagram as idg
    # stub the presigned download so no network + no secret leaves the test
    monkeypatch.setattr(idg, "_download",
                        lambda url, client: b"<mxfile/>" if url.endswith(".drawio?sig=x") else b"PNGBYTES")
    res = fetch(4242, str(tmp_path), live=True, client=_FilesArtifactStub())
    assert res["drawio"] == "artifact_4242.drawio"
    assert res["png"] == "artifact_4242.png"
    assert res["below_bar"] is False
    assert res["judge_score"] == 100.0
    assert res["caption"] == "read left to right"
    assert (tmp_path / "artifact_4242.drawio").read_bytes() == b"<mxfile/>"
    assert (tmp_path / "artifact_4242.png").read_bytes() == b"PNGBYTES"
