# pipeline/tests/test_incept_client.py
import os, sys
PIPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PIPE not in sys.path: sys.path.insert(0, PIPE)
from incept_client import InceptClient

def test_generate_dry_makes_no_call_and_echoes_body():
    c = InceptClient(cache_dir="C:/tmp/incept_cache_test")
    r = c.generate("teach arguable claim", "image", options={"image_subtype": "drawio"},
                   grade_levels=["g9"], subject="writing", live=False)
    assert r["status"] == "dry"
    assert r["would_send"]["generation_type"] == "image"
    assert r["would_send"]["options"]["image_subtype"] == "drawio"
    assert r["request_id"] is None  # nothing was submitted

def test_qc_dry_echoes_payload():
    c = InceptClient(cache_dir="C:/tmp/incept_cache_test")
    r = c.qc("question", {"stem": "x", "options": ["a","b","c","d"], "answer_key": {"answer":"a"}},
             prompt="assess claim id", grade_levels=["g9"], subject="writing", live=False)
    assert r["status"] == "dry" and r["would_send"]["generation_type"] == "question"

def test_key_never_appears_in_repr():
    c = InceptClient(cache_dir="C:/tmp/incept_cache_test")
    assert "ik_" not in repr(c) and "ik_" not in str(vars(c))
