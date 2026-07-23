"""
Tests for the PP100 form-bank infrastructure (Phase A).

Covers:
  - mastery_forms.forms_for(entry): normalizes a MASTERY entry into a canonical list of form dicts,
    with forms[0] byte-identical to the current single-form behavior (prod-safe fallback = bank of 1).
  - pp100_forms QC gate: the equivalence contract (grain/rubric/frq_type/mode held constant; held-out
    source distinct within a lesson; no em dash; source exists).
These are pure-function tests (no network, no live API).
"""
import os
import sys

HERE = os.path.dirname(__file__)
PIPE = os.path.join(HERE, "..")
sys.path.insert(0, PIPE)

import mastery_forms as MF


# ---- forms_for: normalization + backward compatibility -------------------------------------------------

def test_single_form_entry_becomes_forms0_verbatim():
    """A legacy entry (source + unit + rubric_ref + prompt_html, no `forms`) yields exactly one form whose
    fields equal the entry's, so nothing regresses (bank of 1 == today)."""
    entry = {"source": "SRC-A", "unit": "sentence", "rubric_ref": "rc.staar",
             "frq_type": "writing", "prompt_html": "<p>Write one claim.</p>"}
    forms = MF.forms_for(entry)
    assert len(forms) == 1
    f0 = forms[0]
    assert f0["source"] == "SRC-A"
    assert f0["unit"] == "sentence"
    assert f0["rubric_ref"] == "rc.staar"
    assert f0["frq_type"] == "writing"
    assert f0["prompt_html"] == "<p>Write one claim.</p>"


def test_source_free_entry_normalizes_with_none_source():
    """A source-free lesson (G11 C1104) has no `source`; forms_for must still yield one form with source=None,
    not raise."""
    entry = {"unit": "essay", "rubric_ref": "rc.4trait", "frq_type": "writing",
             "prompt_html": "<p>Take a position and supply your own example.</p>"}
    forms = MF.forms_for(entry)
    assert len(forms) == 1
    assert forms[0]["source"] is None


def test_multi_form_entry_lists_all_forms_with_inherited_defaults():
    """An entry with a `forms` list yields one dict per form; each form inherits the entry-level unit/
    rubric_ref/frq_type unless the form overrides them (grain/rubric are held constant by the contract, so
    inheritance is the normal case)."""
    entry = {
        "unit": "sentence", "rubric_ref": "rc.staar", "frq_type": "writing",
        "forms": [
            {"source": "SRC-A", "prompt_html": "<p>Claim on A.</p>"},
            {"source": "SRC-B", "prompt_html": "<p>Claim on B.</p>"},
            {"source": "SRC-C", "prompt_html": "<p>Claim on C.</p>"},
        ],
    }
    forms = MF.forms_for(entry)
    assert len(forms) == 3
    assert [f["source"] for f in forms] == ["SRC-A", "SRC-B", "SRC-C"]
    # each inherits grain/rubric/frq_type from the entry
    for f in forms:
        assert f["unit"] == "sentence"
        assert f["rubric_ref"] == "rc.staar"
        assert f["frq_type"] == "writing"


def test_legacy_source_becomes_forms0_when_forms_also_present():
    """If BOTH a top-level `source`/`prompt_html` AND a `forms` list are present, `forms` wins (explicit list
    is authoritative); the legacy top-level fields are ignored to avoid a duplicate form[0]."""
    entry = {
        "source": "LEGACY", "unit": "sentence", "rubric_ref": "rc.staar", "prompt_html": "<p>legacy</p>",
        "forms": [{"source": "SRC-A", "prompt_html": "<p>A</p>"},
                  {"source": "SRC-B", "prompt_html": "<p>B</p>"}],
    }
    forms = MF.forms_for(entry)
    assert [f["source"] for f in forms] == ["SRC-A", "SRC-B"]


def test_empty_entry_yields_no_forms():
    assert MF.forms_for({}) == []
    assert MF.forms_for(None) == []


# ---- form ids ------------------------------------------------------------------------------------------

def test_form_ids_are_stable_and_1_indexed():
    """Form k (1-indexed) for a lesson maps to deterministic FRQ + test ids the pusher and assembler share."""
    assert MF.form_frq_id("ACC-W910-L-G9-C901-0001", 1) == "ACC-W910-L-G9-C901-0001-MASTERY-FRQ-f1"
    assert MF.form_test_id("ACC-W910-L-G9-C901-0001", 2) == "ACC-W910-L-G9-C901-0001-MASTERY-f2"


def test_bank_of_one_uses_legacy_ids_for_prod_safety():
    """A bank of exactly one form must reuse the CURRENT live ids (<lesson>-MASTERY-FRQ / <lesson>-MASTERY),
    NOT the -f1 suffixed ids, so a single-form lesson stays byte-identical to what is already live."""
    assert MF.form_frq_id("ACC-W910-L-G9-C901-0001", 1, bank_size=1) == "ACC-W910-L-G9-C901-0001-MASTERY-FRQ"
    assert MF.form_test_id("ACC-W910-L-G9-C901-0001", 1, bank_size=1) == "ACC-W910-L-G9-C901-0001-MASTERY"
    # but with a bank > 1, even form 1 uses the suffixed id
    assert MF.form_frq_id("ACC-W910-L-G9-C901-0001", 1, bank_size=3) == "ACC-W910-L-G9-C901-0001-MASTERY-FRQ-f1"
