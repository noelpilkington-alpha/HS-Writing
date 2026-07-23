import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from incept_test_adapter import parse, classify_gate_failure

FIXTURE = "C:/tmp/incept_fulltest_11324.json"

def _output_json():
    return json.load(open(FIXTURE, encoding="utf-8"))["output_json"]

def test_parse_returns_items_and_warnings():
    items, warnings = parse(_output_json())
    assert len(items) == 8               # the fixture has 8 items
    assert isinstance(warnings, list)

def test_mc_correct_id_resolved_by_text_match():
    items, _ = parse(_output_json())
    mc = [it for it in items if it.qti_type == "choice"]
    assert mc, "expected at least one MC item"
    for it in mc:
        correct = [o for o in it.options if o.correct]
        assert len(correct) == 1                       # exactly one keyed correct option
        assert it.answer_key == [correct[0].id]        # answer_key matches the correct Option id
        assert all(o.rationale.strip() for o in it.options if not o.correct), "distractors need non-empty rationales"

def test_text_entry_becomes_scr_or_cr_with_model_answer():
    items, _ = parse(_output_json())
    constructed = [it for it in items if it.qti_type in ("text-entry", "extended-text")]
    assert constructed, "expected SCR/ECR items"
    for it in constructed:
        assert it.answer_key and it.answer_key[0].strip()   # model answer carried
        assert it.family in ("SCR", "CR")

def test_no_item_silently_dropped():
    oj = _output_json()
    items, warnings = parse(oj)
    assert len(items) == len(oj["items"])   # one Item per source item, none dropped

def test_classify_gate_failure_split():
    assert classify_gate_failure("distractor_integrity") == "fatal"
    assert classify_gate_failure("scr_binding") == "fatal"
    assert classify_gate_failure("rubric_config") == "fatal"
    assert classify_gate_failure("schema") == "fatal"
    assert classify_gate_failure("no_em_dash") == "fixable"
