"""
incept_diagram.py  -  editable-diagram stage (Incept drawio -> local PNG) for gated-reading teach cards.

WHAT THIS IS:
  * Incept can generate an editable drawio image (generation_type="image",
    options={"image_subtype":"drawio"}). The drawio XML is the SOURCE OF TRUTH for the labels;
    the PNG is the display asset bound into a teach card via _content_card(img=...).
  * This mirrors the authored-SVG path (l01_diagrams.verify_svg): the anti-garble check here is
    verify_drawio, which asserts every expected label survives verbatim in the drawio XML.

DRY-BY-DEFAULT:
  request_diagram(spec, live=False) makes NO network call: it returns the would-send body from
  InceptClient.generate. fetch(...) in dry mode reads the local client cache / returns cached local
  paths and never touches the network. Only live=True spends quota (exercised in Task 7).

Stdlib only (xml.etree, os, json) + the sibling InceptClient for transport.
"""
from __future__ import annotations

import json
import os
import xml.etree.ElementTree as ET

from incept_client import InceptClient

_DRAWIO_OPTIONS = {"image_subtype": "drawio"}


# ---- request ---------------------------------------------------------------
def request_diagram(spec, live: bool = False, client: InceptClient | None = None,
                    grade_levels=None, subject: str = "writing") -> dict:
    """POST an "image"/"drawio" generate for a diagram described by `spec`.

    `spec` is a dict (prompt + expected labels) or a bare prompt string. In dry mode this returns
    the client would-send stub: {"status":"dry","would_send":<body>,"request_id":None}. The expected
    labels ride along in the prompt so the generator is asked for them and verify_drawio can check them.
    """
    if isinstance(spec, str):
        prompt = spec
    else:
        prompt = str(spec.get("prompt", "") or "")
        labels = spec.get("expected_labels") or []
        if labels:
            prompt = f"{prompt}\nRequired labels (verbatim): {', '.join(str(l) for l in labels)}"
    if client is None:
        client = InceptClient()
    return client.generate(prompt, "image", options=dict(_DRAWIO_OPTIONS),
                           grade_levels=grade_levels, subject=subject, live=live)


# ---- fetch (download to a local hosted dir) --------------------------------
def _write_bytes(dest_dir: str, name: str, data) -> str:
    """Write bytes/text to dest_dir/name; return the LOCAL relative path (basename)."""
    os.makedirs(dest_dir, exist_ok=True)
    safe = os.path.basename(name)
    path = os.path.join(dest_dir, safe)
    mode = "wb" if isinstance(data, (bytes, bytearray)) else "w"
    if mode == "w":
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(data)
    else:
        with open(path, "wb") as fh:
            fh.write(data)
    return safe


def fetch(artifact_id, dest_dir: str, live: bool = False,
          client: InceptClient | None = None) -> dict:
    """Pull the drawio + PNG for an artifact into dest_dir; return LOCAL relative paths.

    Returns {"drawio": <rel path or None>, "png": <rel path or None>}.

    LIVE (live=True): read the artifact JSON (client.artifact), locate the inline drawio XML and PNG
    bytes/url in the response, write them into dest_dir. This path is exercised live only in Task 7.
    DRY (live=False): read the artifact from the client cache (no network); if the local files are
    already present in dest_dir, return their relative paths without touching the network.
    """
    if client is None:
        client = InceptClient()

    base = f"artifact_{artifact_id}"
    out = {"drawio": None, "png": None}

    # Dry short-circuit: if the local assets are already on disk, just return them (no cache read).
    if not live:
        for key, ext in (("drawio", ".drawio"), ("png", ".png")):
            cand = os.path.join(dest_dir, base + ext)
            if os.path.exists(cand):
                out[key] = os.path.basename(cand)
        if out["drawio"] or out["png"]:
            return out

    # Read the artifact JSON (live: fetch + write-through cache; dry: read cache, raises on miss).
    art = client.artifact(artifact_id, live=live)

    drawio_xml = art.get("drawio") or art.get("drawio_xml") or art.get("xml")
    if drawio_xml:
        out["drawio"] = _write_bytes(dest_dir, base + ".drawio", drawio_xml)

    png = art.get("png") or art.get("png_bytes") or art.get("image")
    if png is not None:
        # png may be raw bytes already; leave URL-download (presigned S3) to the live Task 7 caller.
        if isinstance(png, (bytes, bytearray)):
            out["png"] = _write_bytes(dest_dir, base + ".png", png)
        elif isinstance(png, str) and not png.startswith("http"):
            out["png"] = _write_bytes(dest_dir, base + ".png", png.encode("latin-1", "ignore"))
    return out


# ---- anti-garble check -----------------------------------------------------
def verify_drawio(drawio_path: str, expected_labels) -> bool:
    """Parse the drawio XML and assert every string in `expected_labels` appears verbatim as a
    substring of some mxCell value="..." attribute (the node labels).

    Mirrors the anti-garble intent of l01_diagrams.verify_svg. Returns True if all present; raises
    AssertionError naming the FIRST missing label otherwise.
    """
    tree = ET.parse(drawio_path)
    root = tree.getroot()
    # collect every mxCell value= attribute (the node labels)
    labels = []
    for cell in root.iter("mxCell"):
        val = cell.get("value")
        if val:
            labels.append(val)
    for want in expected_labels:
        if not any(want in got for got in labels):
            raise AssertionError(f"drawio label missing (anti-garble): {want!r}")
    return True


if __name__ == "__main__":
    probe = "C:/tmp/incept_probe/arguable_claim.drawio"
    if os.path.exists(probe):
        print("PASS" if verify_drawio(probe, ["SIDE", "REASON", "ARGUABLE CLAIM"]) else "FAIL")
    r = request_diagram({"prompt": "arguable-claim formula", "expected_labels": ["SIDE", "REASON"]},
                        live=False)
    print(json.dumps(r, indent=2))
