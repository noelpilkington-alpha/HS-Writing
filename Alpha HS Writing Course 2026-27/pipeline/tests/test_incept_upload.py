# pipeline/tests/test_incept_upload.py
#
# incept_upload.py hosts VIDEO assets (mp4 + vtt) in the Incept video bucket via a two-step
# presigned-S3 uploader. Every test here runs live=False / NO network: the transport is never
# exercised. No presigned uploadUrl appears in this file; fixtures use synthetic local paths only.
import os
import sys

PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)

import incept_upload
from incept_upload import request_upload_urls, put_file, upload_files, _strip_query, API_URL


# ---- (a) request_upload_urls DRY derives filename + contentType from paths -----------------
def test_request_upload_urls_dry_derives_content_types():
    r = request_upload_urls(["C:/tmp/x.mp4", "C:/tmp/y.vtt"], live=False)
    assert r["status"] == "dry"
    assert r["urls"] is None  # nothing was requested
    files = r["would_send"]["files"]
    assert files[0]["contentType"] == "video/mp4"
    assert files[1]["contentType"] == "text/vtt"
    assert files[0]["filename"] == "x.mp4"
    assert files[1]["filename"] == "y.vtt"


def test_request_upload_urls_dry_accepts_explicit_dicts():
    r = request_upload_urls(
        [{"filename": "narration.vtt", "contentType": "text/vtt"}], live=False
    )
    assert r["status"] == "dry"
    assert r["would_send"]["files"][0]["filename"] == "narration.vtt"
    assert r["would_send"]["files"][0]["contentType"] == "text/vtt"


# ---- (b) upload_files DRY returns a would-send manifest, no network -------------------------
def test_upload_files_dry_returns_manifest_no_network():
    r = upload_files(["C:/tmp/a.mp4", "C:/tmp/b.vtt"], live=False)
    assert r["status"] == "dry"
    files = r["would_send"]["files"]
    assert [f["filename"] for f in files] == ["a.mp4", "b.vtt"]
    assert files[0]["contentType"] == "video/mp4"
    assert files[1]["contentType"] == "text/vtt"


# ---- (c) _strip_query drops the presigned query string -------------------------------------
def test_strip_query_drops_presigned_signature():
    url = "https://s3/bucket/key.mp4?X-Amz-Signature=SECRET&y=1"
    assert _strip_query(url) == "https://s3/bucket/key.mp4"


def test_strip_query_leaves_bare_url_untouched():
    assert _strip_query("https://s3/bucket/key.mp4") == "https://s3/bucket/key.mp4"


# ---- (d) put_file DRY returns without network (dry stub shape) -----------------------------
def test_put_file_dry_returns_stub_no_network(tmp_path):
    p = tmp_path / "clip.mp4"
    p.write_bytes(b"0123456789")  # 10 bytes
    r = put_file(str(p), "https://upload/presigned?sig=SECRET", live=False)
    assert isinstance(r, dict)
    assert r["status"] == "dry"
    assert r["local_path"] == str(p)
    assert r["bytes"] == 10


# ---- (e) API_URL constant is the decoded API Gateway upload endpoint -----------------------
def test_api_url_is_the_upload_endpoint():
    assert API_URL == "https://m0wtmamd39.execute-api.us-east-1.amazonaws.com/upload"


# ---- (f) module never imports requests -----------------------------------------------------
def test_no_requests_dependency():
    src = open(incept_upload.__file__, "r", encoding="utf-8").read()
    assert "import requests" not in src
    assert "from requests" not in src
