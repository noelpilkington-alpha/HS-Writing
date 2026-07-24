import os, sys, copy
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from incept_cleanup import _strip_em_dash, _fact_verify
from item_contract import Item, Option, qc_item

def _incept_mc(stem, opts, answer_idx=0):
    options = [Option(id=chr(65+i), text=t, correct=(i == answer_idx),
                      rationale=("correct" if i == answer_idx else "a distractor")) for i, t in enumerate(opts)]
    return Item(id="INCEPT-x-01", family="SR", grade="9-10", stem=stem, qti_type="choice",
                subskill_or_mode="evidence", acc_tags=["CCSS.W.9-10.1"], options=options,
                answer_key=[chr(65+answer_idx)], provenance={"bakeoff_source": "incept"})

def test_strip_em_dash_removes_all_dashes_and_passes_gate():
    it = _incept_mc("Which choice — the best evidence — supports the claim?",
                    ["Cities should add bike lanes – safer routes get more riders.",
                     "It was warm.", "Buses run late.", "People liked it."])
    out = _strip_em_dash(it)
    body = out.stem + " ".join(o.text + o.rationale for o in out.options) + " ".join(out.answer_key)
    assert "—" not in body and "–" not in body        # no em/en dashes remain
    # the no-em-dash gate now passes on the cleaned item
    r = qc_item(out)
    assert r["gates"]["no_em_dash"]["passed"]

def test_strip_em_dash_preserves_meaning():
    it = _incept_mc("The plan — adopted last year — helped.", ["A", "B", "C"])
    out = _strip_em_dash(it)
    # content preserved minus the dash: the words survive
    assert "adopted last year" in out.stem
    assert "The plan" in out.stem and "helped" in out.stem

def test_strip_em_dash_does_not_mutate_original():
    it = _incept_mc("X — Y", ["A", "B", "C"])
    _strip_em_dash(it)
    assert "—" in it.stem   # original untouched (copy semantics)

def test_fact_verify_keeps_claim_free_item():
    it = _incept_mc("Which sentence is an arguable claim?",
                    ["Cities should build bike lanes because safer routes get more riders.",
                     "Many cities have bike lanes.", "Bikes are nice.", "Some cities got grants."])
    out, note = _fact_verify(it)
    assert out is not None    # no hard stat -> kept

def test_fact_verify_drops_unverifiable_stat():
    it = _incept_mc("Which is the best evidence?",
                    ["A study of 62 districts found a 14 percent rise in scores.",
                     "It was warm.", "Buses run late.", "People liked it."])
    out, note = _fact_verify(it)
    assert out is None          # fabricated/unverifiable stat -> dropped
    assert "stat" in note.lower() or "percent" in note.lower() or "62" in note

def test_fact_verify_drops_on_percent_or_year_figure():
    it = _incept_mc("Pick the strongest support.",
                    ["Turnover fell from 21% to 13% after the change.", "A", "B", "C"])
    out, note = _fact_verify(it)
    assert out is None

def test_fact_verify_allows_study_as_verb():
    it = _incept_mc("Which is the best claim?", ["Students should study more before exams.", "B", "C", "D"])
    out, note = _fact_verify(it)
    assert out is not None   # 'study' as a verb is not a citation

def test_fact_verify_allows_data_as_generic_noun():
    it = _incept_mc("Which is an arguable claim?", ["Cities should update their data privacy rules.", "B", "C", "D"])
    out, note = _fact_verify(it)
    assert out is not None   # 'data privacy' is not a stat citation
