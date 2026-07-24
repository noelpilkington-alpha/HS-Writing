"""
test_grader_xml_wiring.py  -  lock in the 2026-07-24 grader-wiring fixes.

Two defects the live G9 L01 review surfaced, both fixed host-independently:
  A. The JSON push SILENTLY STRIPS the customOperator from the executable rawXml (CRITICAL RULE 1), so no
     grader fires. Fix: wire_payload items are serialized to {format:xml} with a LITERAL <qti-custom-operator>
     inside <qti-response-processing>. These tests assert the operator + grader URL survive in the XML.
  B. _grader_url_for / normalize_grader_url doubled query params / appended '/score' after the query when
     handed an already-parameterized URL. Fix: both are now idempotent. These tests assert idempotency.

If a future change reverts to a JSON push (dropping the operator) or breaks idempotency, CI fails here.
"""
import os, sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, ".."))

from g9_wire_grader import _grader_url_for, normalize_grader_url, item_to_xml_payload, wire_payload
from lesson_contract import Slot

APPROVED = "https://hsw-grader.lambda-url.us-east-1.on.aws/score"   # an allowlist-approved pattern


# ---- B: URL idempotency -----------------------------------------------------

def test_grader_url_for_idempotent_on_parameterized_base():
    clean = _grader_url_for(APPROVED, "sentence", "writing")
    assert clean.count("grain=") == 1 and clean.count("frq_type=") == 1
    # re-baking an already-parameterized URL must NOT double the params
    again = _grader_url_for(clean, "sentence", "writing")
    assert again == clean, f"not idempotent: {again}"
    # a stale grain must be stripped when the slot is now essay-grain
    essay = _grader_url_for(clean, "essay", "writing")
    assert "grain=" not in essay, f"stale grain not stripped: {essay}"


def test_grader_url_for_mode_and_grain_orthogonal():
    assert _grader_url_for(APPROVED, "essay", "writing", "analysis").endswith("?mode=analysis")
    both = _grader_url_for(APPROVED, "sentence", "writing", "analysis")
    assert "grain=sentence" in both and "mode=analysis" in both


def test_normalize_idempotent_and_query_safe():
    assert normalize_grader_url("https://x.lambda-url.us-east-1.on.aws").endswith("/score")
    assert normalize_grader_url(APPROVED) == APPROVED
    # an already-parameterized URL must not get '/score' appended after the query
    par=  "https://x.lambda-url.us-east-1.on.aws/score?grain=sentence&frq_type=writing"
    assert normalize_grader_url(par) == "https://x.lambda-url.us-east-1.on.aws/score"


# ---- A: XML wiring carries the operator -------------------------------------

def _sentence_slot():
    return Slot("INDEPENDENT", "production_frq", "Write one arguable claim", unit="sentence",
                rubric_ref="rc.staar", scored=True, frq_type="writing", bank="a",
                body="Write one arguable claim: take a side and give one checkable reason.")


def _paragraph_slot():
    return Slot("INDEPENDENT", "production_frq", "Write a paragraph", unit="paragraph",
                rubric_ref="rc.staar", scored=True, frq_type="writing", bank="a",
                body="Write an analytical paragraph.")


def test_render_paragraph_serializes_to_valid_xml_with_operator():
    # paragraph+ routes to the RENDER grader; the operator must survive LITERALLY in the executable XML.
    item = wire_payload("ZZ-PARA-FRQ", _paragraph_slot(), APPROVED)
    body = item_to_xml_payload(item)
    assert body["format"] == "xml"
    xml = body["xml"]
    ET.fromstring(xml)                                   # valid XML (RULE 2)
    assert "com.alpha-1edtech.ExternalApiScore" in xml   # operator present
    assert "qti-custom-operator" in xml                  # written literally, not as JSON responseProcessing
    assert "lambda-url.us-east-1.on.aws/score" in xml    # Render grader URL survives in the executable XML
    assert "grain=paragraph" in xml and "frq_type=writing" in xml
    assert "alphatest.alpha.school" not in xml           # paragraph does NOT go native


def test_render_xml_escapes_the_ampersand_in_the_grader_url():
    # the definition URL has an unescaped & between query params; it MUST be &amp; inside an XML attribute
    xml = item_to_xml_payload(wire_payload("ZZ-PARA-FRQ", _paragraph_slot(), APPROVED))["xml"]
    ET.fromstring(xml)                                   # would raise if & were bare
    assert "grain=paragraph" in xml


def test_sentence_routes_to_native_grader_with_grading_prompt():
    # 2026-07-24 split: SENTENCE grain wires to the NATIVE AlphaTest grader (Timeback's hosted URL) + an
    # embedded ext:grading-prompt rubric-block; NOT to the Render host (no allowlist dependency).
    item = wire_payload("ZZ-SENT-FRQ", _sentence_slot(), APPROVED)
    xml = item_to_xml_payload(item)["xml"]
    ET.fromstring(xml)
    assert item["responseProcessing"]["customOperator"]["definition"] == "https://alphatest.alpha.school/prod/ai-grading"
    assert "alphatest.alpha.school/prod/ai-grading" in xml
    assert 'use="ext:grading-prompt"' in xml             # the authored grading prompt is embedded
    assert 'normal-maximum="3"' in xml                   # sentence-writing scale on the SCORE declaration
    assert "lambda-url" not in xml                        # sentence does NOT go to Render


def test_sentence_render_path_still_available_via_flag():
    # native=False forces the Render path for a sentence (e.g. if native is ever retired for a route)
    item = wire_payload("ZZ-SENT-FRQ", _sentence_slot(), APPROVED, native=False)
    defn = item["responseProcessing"]["customOperator"]["definition"]
    assert "lambda-url.us-east-1.on.aws/score" in defn and "grain=sentence" in defn


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn(); print(f"ok: {name}")
    print("OK: grader XML wiring + URL idempotency locked in")
