"""
incept_pool.py  -  deepen the Incept item pool across all 6 G9 slot-types for the hybrid bake-off.

Generate one targeted Incept bank per subskill (count ~10), cache each to C:/tmp/incept_pool/<subskill>.json,
then load + STAMP each item with its bank's intended subskill/family/rubric (we generate one bank per
subskill on purpose, so intent-stamping is deterministic). Feeds bakeoff_hybrid via deepened=True.

Scope note: conventions + sentence are app-owned skills (EGUMPP/AlphaWrite); generating Incept items for them
here is a GENERATOR SHOOT-OUT (bake-off input), NOT a course-scope change. Nothing here ships into the course.
"""
from __future__ import annotations
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from item_contract import Item, Option

SUBSKILLS = ["evidence", "organization", "conventions", "sentence", "scr_writing", "argument"]

# how each stamped subskill maps to our contract family/qti/rubric (mirrors incept_test_adapter)
SUBSKILL_STAMP = {
    "evidence":     {"family": "SR",  "qti_type": "choice",        "rubric_ref": ""},
    "organization": {"family": "SR",  "qti_type": "choice",        "rubric_ref": ""},
    "conventions":  {"family": "SR",  "qti_type": "choice",        "rubric_ref": ""},
    "sentence":     {"family": "SR",  "qti_type": "choice",        "rubric_ref": ""},
    "scr_writing":  {"family": "SCR", "qti_type": "text-entry",    "rubric_ref": "rc.scr1"},
    "argument":     {"family": "CR",  "qti_type": "extended-text", "rubric_ref": "rc.staar"},
}

# one targeted generation call per subskill (prompt engineered to elicit THAT subskill at G9)
SUBSKILL_PROMPTS = {
    "evidence": {"generation_type": "question",
                 "options": {"interaction_type": "multiple_choice", "structure": "bank", "count": 10},
                 "prompt": "Grade 9 argumentative writing: multiple-choice items where the student picks the "
                           "sentence that best supports a given claim with relevant evidence. Distractors: "
                           "off-claim, restates the topic, supports the opposing view."},
    "organization": {"generation_type": "question",
                     "options": {"interaction_type": "multiple_choice", "structure": "bank", "count": 10},
                     "prompt": "Grade 9 argumentative writing: multiple-choice items on organization and "
                               "cohesion, e.g. which transition or sentence order makes a paragraph flow."},
    "conventions": {"generation_type": "question",
                    "options": {"interaction_type": "multiple_choice", "structure": "bank", "count": 10},
                    "prompt": "Grade 9 editing: multiple-choice items on grammar, usage, punctuation, "
                              "capitalization, and spelling in the context of a short draft."},
    "sentence": {"generation_type": "question",
                 "options": {"interaction_type": "multiple_choice", "structure": "bank", "count": 10},
                 "prompt": "Grade 9 editing: multiple-choice items on sentence structure and boundaries "
                           "(run-ons, fragments, comma splices, combining)."},
    "scr_writing": {"generation_type": "question",
                    "options": {"interaction_type": "text_entry", "structure": "bank", "count": 10},
                    "prompt": "Grade 9 writing short-constructed-response: rewrite a flawed sentence to fix a "
                              "modifier or combine two sentences, preserving meaning."},
    "argument": {"generation_type": "test",
                 "options": {"purpose": "mastery", "grain": "grade_level", "structure": "single"},
                 "prompt": "A grade 9 source-based argumentative essay prompt with a reading passage on whether "
                           "schools should adopt a four-day week."},
}

def _normalize_items(output_json: dict) -> list[dict]:
    """Flatten any Incept artifact shape into a flat list of raw item dicts:
    single-question (the object IS the item), items[] (flat bank), or forms[].items[] (test bank),
    or questions[] (alt bank key)."""
    oj = output_json or {}
    if "items" in oj and isinstance(oj["items"], list):
        return list(oj["items"])
    if "questions" in oj and isinstance(oj["questions"], list):
        return list(oj["questions"])
    if "forms" in oj and isinstance(oj["forms"], list):
        out = []
        for f in oj["forms"]:
            out += list(f.get("items") or [])
        return out
    if "stem" in oj:            # a single-question artifact: the object itself is the item
        return [oj]
    return []

def _build_item(idx: int, subskill: str, raw: dict) -> Item:
    stamp = SUBSKILL_STAMP[subskill]
    md = raw.get("metadata") or {}
    stem = str(raw.get("stem", "")).strip()
    acc = list(md.get("standards") or ["CCSS.W.9-10.1"])
    prov = {"copyright": "incept_generated", "bakeoff_source": "incept", "dok": md.get("dok"),
            "difficulty": md.get("difficulty"), "intended_subskill": subskill}
    if stamp["family"] == "SR":
        opts_text = raw.get("options") or []
        ans = str(raw.get("answer", "")).strip()
        expl = raw.get("explanations") or {}
        options, correct = [], []
        for k, t in enumerate(opts_text):
            oid = chr(65 + k); tt = str(t).strip()
            if tt == ans: correct.append(oid)
            options.append(Option(id=oid, text=tt, correct=(tt == ans), rationale=str(expl.get(t, "")).strip()))
        return Item(id=f"INCEPT-{subskill}-{idx:02d}", family="SR", grade="9-10", stem=stem,
                    qti_type="choice", subskill_or_mode=subskill, acc_tags=acc,
                    options=options, answer_key=list(correct), provenance=prov)
    # SCR / CR: model answer in answer_key, no options
    model = str(raw.get("answer", "")).strip()
    return Item(id=f"INCEPT-{subskill}-{idx:02d}", family=stamp["family"], grade="9-10", stem=stem,
                qti_type=stamp["qti_type"], subskill_or_mode=subskill, acc_tags=acc,
                answer_key=[model] if model else [],
                stimulus_ref=("INCEPT-STIMULUS" if stamp["family"] == "CR" else ""),
                rubric_ref=stamp["rubric_ref"], provenance=prov)

def load_deepened_incept_pool(cache_dir: str = "C:/tmp/incept_pool") -> list[Item]:
    """Read the 6 cached subskill banks, normalize each, build stamped Items. Raise if any bank is missing."""
    missing = [sk for sk in SUBSKILLS if not os.path.exists(os.path.join(cache_dir, f"{sk}.json"))]
    if missing:
        raise FileNotFoundError(f"deepened Incept pool missing banks: {missing} (generate them first)")
    pool = []
    for sk in SUBSKILLS:
        with open(os.path.join(cache_dir, f"{sk}.json"), encoding="utf-8") as fh:
            oj = json.load(fh)
        raws = _normalize_items(oj)
        for i, raw in enumerate(raws, 1):
            pool.append(_build_item(i, sk, raw))
    return pool

def generate_pool(live: bool = False, client=None) -> dict:
    """Submit the 6 targeted bank generations. Dry mode returns the would-send bodies (no network).
    Live mode returns the 201 responses (request_id/status_url); polling to terminal is the operator step."""
    from incept_client import InceptClient
    client = client or InceptClient()
    out = {}
    for sk, spec in SUBSKILL_PROMPTS.items():
        out[sk] = client.generate(spec["prompt"], spec["generation_type"], options=dict(spec["options"]),
                                  grade_levels=["g9"], subject="writing", live=live)
    return out

def fetch_pool(artifact_ids: dict, live: bool = False, client=None, cache_dir: str = "C:/tmp/incept_pool") -> dict:
    """artifact_ids: {subskill -> succeeded artifact id}. Fetch each artifact's output_json and cache it to
    <cache_dir>/<subskill>.json. Operator passes the ids after polling (mirrors incept_test's hand-off)."""
    from incept_client import InceptClient
    client = client or InceptClient()
    os.makedirs(cache_dir, exist_ok=True)
    paths = {}
    for sk, aid in artifact_ids.items():
        art = client.artifact(aid, live=live)
        oj = (art or {}).get("output_json", {})
        path = os.path.join(cache_dir, f"{sk}.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(oj, fh, indent=1)
        paths[sk] = path
    return paths
