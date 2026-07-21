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


def test_registry_entries_are_wellformed():
    # After the first live bind (T7), the registry is populated. Every entry must be
    # (lesson_id, slot_1based) -> (base_url-RELATIVE path, alt text), with NO em dashes in
    # the alt text (renders into the DOM) and NO absolute URL in the stored path.
    assert isinstance(INCEPT_DIAGRAMS, dict)
    for key, val in INCEPT_DIAGRAMS.items():
        assert isinstance(key, tuple) and len(key) == 2
        lid, slot = key
        assert isinstance(lid, str) and isinstance(slot, int) and slot >= 1
        rel, alt = val
        assert rel.startswith("incept_diagrams/") and not rel.startswith("http")
        assert "—" not in alt and "–" not in alt  # no em/en dash in student-facing alt


def test_content_card_img_prepends_base_url():
    # gated_reading prepends base_url to the relative registry path so the player gets an absolute src.
    import gated_reading as gr
    L_slots = [type("S", (), {"kind": "teach_card", "title": "T", "body": "", "ref": "",
                              "choices": [], "feedback": ""})()]
    L = type("L", (), {"id": "ACC-W910-L-G9-C903-0012", "slots": L_slots,
                       "title": "t", "grade": "9-10", "lesson_type": 2, "unit": "u", "target": "x"})()
    # only assert the prepend helper shape via a direct render check on a bound lesson id
    saved = dict(gr._INCEPT_DIAGRAMS)
    try:
        gr._INCEPT_DIAGRAMS[("ACC-W910-L-G9-C903-0012", 1)] = ("incept_diagrams/x.png", "alt no dash")
        html, _ = gr.build_lesson_html(L, base_url="https://host.example/g9-l07")
        assert 'src="https://host.example/g9-l07/incept_diagrams/x.png"' in html
        assert 'alt="alt no dash"' in html
    finally:
        gr._INCEPT_DIAGRAMS.clear()
        gr._INCEPT_DIAGRAMS.update(saved)


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
