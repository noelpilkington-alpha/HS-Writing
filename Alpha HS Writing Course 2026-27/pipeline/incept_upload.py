"""
incept_upload.py  -  upload local VIDEO assets (mp4 + vtt) to the Incept video bucket.

WHAT THIS IS FOR:
  The post-lock video stage produces local files (an mp4 voiceover + its .vtt captions). This module
  HOSTS those files: it uploads them to the Incept video bucket and returns each file's PERMANENT
  public URL. That public_url is what we bind as a OneRoster component-resource (a hosted asset the
  learner surface fetches), NOT embedded into lesson.html and NOT wrapped in QTI, per the Incept team's
  delivery instruction. This module does the hosting only; the binding lives elsewhere.

THE UPLOAD MECHANISM (a two-step presigned-S3 uploader over AWS API Gateway; NO auth needed):
  1. POST API_URL with body {"files":[{"filename":..,"contentType":..}, ...]} -> the gateway returns
     {"urls":[{"uploadUrl":<presigned S3 PUT url>,"publicUrl":<permanent url>,"folder":..,
     "filename":..}, ...]}.
  2. For each returned url: PUT the file BYTES to uploadUrl with Content-Type matching the file
     (video/mp4 or text/vtt). A 2xx is success.
  3. The file then lives permanently at publicUrl -- that permanent url is what we bind.

DRY-BY-DEFAULT / --live contract (mirrors incept_client.py):
  * Every function takes `live: bool` (default False).
  * DRY (live=False) makes NO network call: request_upload_urls returns the would-send body,
    put_file returns a would-do stub (getsize only; the file is NOT read/streamed), upload_files
    returns the would-send manifest.
  * LIVE (live=True) is the only path that spends network: curl via subprocess (stdlib), never
    `requests`.

SECRET HYGIENE:
  This endpoint needs NO auth key. BUT the presigned uploadUrl returned in step 1 is WRITE-CAPABLE and
  must be treated as sensitive: it is passed to curl at call time only and is NEVER logged in full. If
  a url must appear in an error message it is passed through _strip_query() first, which drops the
  query string (where the signature lives).

Stdlib only (os, json, subprocess). Import-safe.
"""
from __future__ import annotations

import json
import os
import subprocess

# The decoded API Gateway upload endpoint (from https://upload.inceptstore.com/). No auth header.
API_URL = "https://m0wtmamd39.execute-api.us-east-1.amazonaws.com/upload"

# file-extension -> Content-Type. mp4 videos and vtt captions are the only assets we host here.
_CONTENT_TYPES = {".mp4": "video/mp4", ".vtt": "text/vtt"}
_DEFAULT_CONTENT_TYPE = "video/mp4"


def _strip_query(url: str) -> str:
    """Return `url` with its query string dropped (everything from the first '?').

    Presigned uploadUrls carry the write-capable signature in the query string. Any url that might
    reach a log or error message is passed through here first so the signature never surfaces.
    """
    if not url:
        return ""
    return url.split("?", 1)[0]


def _content_type_for(filename: str) -> str:
    """Infer the Content-Type from a filename extension (.mp4 -> video/mp4, .vtt -> text/vtt).

    Falls back to video/mp4 for anything else (the bucket's primary asset)."""
    ext = os.path.splitext(filename or "")[1].lower()
    return _CONTENT_TYPES.get(ext, _DEFAULT_CONTENT_TYPE)


def _normalize_files(files) -> list:
    """Coerce `files` into a list of {"filename","contentType"} dicts.

    Accepts either explicit dicts (passed through, with contentType derived from the filename when
    absent) OR local path strings (filename = basename, contentType derived from extension)."""
    out = []
    for item in files or []:
        if isinstance(item, dict):
            filename = item.get("filename") or ""
            ctype = item.get("contentType") or _content_type_for(filename)
            out.append({"filename": filename, "contentType": ctype})
        else:
            # a local path string: derive filename + content type from it.
            filename = os.path.basename(str(item))
            out.append({"filename": filename, "contentType": _content_type_for(filename)})
    return out


def request_upload_urls(files, live: bool = False) -> dict:
    """Step 1: ask the gateway for presigned upload urls.

    `files` = a list of {"filename","contentType"} dicts OR a list of local path strings (filename +
    contentType are then derived by extension: .mp4 -> video/mp4, .vtt -> text/vtt).

    DRY (live=False): NO network. Returns {"status":"dry","would_send":<body>,"urls":None}.
    LIVE (live=True): POST the body and return the parsed {"urls":[...]} response."""
    body = {"files": _normalize_files(files)}
    if not live:
        return {"status": "dry", "would_send": body, "urls": None}

    cmd = [
        "curl", "-s", "--ssl-no-revoke", "--max-time", "60",
        "-X", "POST", API_URL,
        "-H", "Content-Type: application/json",
        "-d", json.dumps(body),
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    except Exception as e:
        raise RuntimeError(f"Incept upload request failed: {type(e).__name__}") from None
    if proc.returncode != 0:
        raise RuntimeError(f"Incept upload request curl failed rc={proc.returncode}: {proc.stderr}")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"Incept upload request returned non-JSON: {proc.stdout[:200]}")


def put_file(local_path: str, upload_url: str, content_type: str | None = None,
             live: bool = False):
    """Step 2: PUT the file bytes to a presigned uploadUrl.

    `content_type` defaults to the value inferred from `local_path`'s extension.

    DRY (live=False): NO network and the file is NOT read/streamed. Returns a would-do stub
    {"status":"dry","local_path":..,"bytes":<os.path.getsize>}.
    LIVE (live=True): curl the PUT (--upload-file). Returns True on a 2xx, False otherwise. Never
    raises; the presigned url is never logged (only _strip_query(url) if a diagnostic is needed)."""
    ctype = content_type or _content_type_for(local_path)
    if not live:
        try:
            size = os.path.getsize(local_path)
        except OSError:
            size = None
        return {"status": "dry", "local_path": local_path, "bytes": size}

    # LIVE: PUT the bytes. --upload-file streams the file (large videos ~14MB); --max-time is generous.
    # -w writes the HTTP status code to stdout; -o discards the body.
    cmd = [
        "curl", "-s", "--ssl-no-revoke", "--max-time", "300",
        "--upload-file", local_path,
        "-H", f"Content-Type: {ctype}",
        "-o", os.devnull,
        "-w", "%{http_code}",
        upload_url,
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=360)
    except Exception:
        # advisory: a failed PUT is a per-file failure, not a crash. Url is not surfaced.
        return False
    if proc.returncode != 0:
        return False
    code = (proc.stdout or "").strip()
    return code.startswith("2")


def upload_files(local_paths, live: bool = False):
    """Orchestrate the two-step upload for a list of local files.

    DRY (live=False): NO network. Returns the would-send manifest
    {"status":"dry","would_send":{"files":[...]}} listing the intended files.
    LIVE (live=True): request presigned urls, PUT each file, and return a list of
    {"local_path","filename","folder","public_url","ok"}. On any per-file failure ok=False and the
    loop continues (advisory; never raises)."""
    paths = list(local_paths or [])
    if not live:
        return {"status": "dry", "would_send": {"files": _normalize_files(paths)}}

    resp = request_upload_urls(paths, live=True)
    urls = (resp or {}).get("urls") or []
    # map each returned url entry back to a local path by filename (basename), preserving order.
    by_name = {}
    for u in urls:
        if isinstance(u, dict) and u.get("filename"):
            by_name.setdefault(u["filename"], u)

    results = []
    for path in paths:
        filename = os.path.basename(str(path))
        entry = by_name.get(filename)
        if not entry:
            results.append({
                "local_path": path, "filename": filename, "folder": None,
                "public_url": None, "ok": False,
            })
            continue
        ok = False
        try:
            ok = put_file(path, entry.get("uploadUrl", ""),
                          content_type=_content_type_for(filename), live=True) is True
        except Exception:
            ok = False
        results.append({
            "local_path": path,
            "filename": filename,
            "folder": entry.get("folder"),
            "public_url": entry.get("publicUrl"),
            "ok": ok,
        })
    return results


if __name__ == "__main__":
    print("API_URL:", API_URL)
    print(json.dumps(request_upload_urls(["C:/tmp/x.mp4", "C:/tmp/y.vtt"], live=False), indent=2))
    print(json.dumps(upload_files(["C:/tmp/x.mp4", "C:/tmp/y.vtt"], live=False), indent=2))
