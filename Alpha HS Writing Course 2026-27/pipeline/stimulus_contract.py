"""
stimulus_contract.py  -  The enforceable contract + QC harness for the G10 stimulus generator.

WHY THIS EXISTS: "high rigor" means the pipeline MECHANICALLY ENFORCES the gates, not that an LLM
claims it followed them. An authored stimulus is only ACCEPTED if it passes every machine-checkable
gate here. Anything that can't be checked mechanically (e.g. "is this fact really on that page?") is
routed to an explicit human/verify step, never silently trusted.

This module defines:
  1. StimulusRecord  - the schema every generated stimulus must fill (the emit contract).
  2. qc_stimulus()   - the QC harness: runs all mechanical gates, returns PASS/FAIL + reasons.
  3. The gates:       structure, provenance-completeness, copyright-posture, fact-source-table
                      integrity, citable-facts, two-sidedness (paired), and Lexile (via readability_gate).

Dependency-free except the local readability_gate. Python stdlib only.
"""
from __future__ import annotations
import re, json, sys, os
from dataclasses import dataclass, field, asdict
from typing import Literal

# import the Lexile gate we already built + validated
sys.path.insert(0, os.path.dirname(__file__))
import readability_gate as rg
import calibration_anchors as ca  # noqa: F401  (available for gate_equivalent_form callers)

Mode = Literal["argument", "explanatory", "analysis"]
# Families: single/complementary/opposing = G9-10 shapes (1-2 passages). G11 adds:
#   synthesis_set  = a SOURCE SET of 3-6 passages (SBAC 4 / AP Lang 6) for cross-source synthesis
#   perspective_set= an issue + given PERSPECTIVES, NO source passage (ACT Writing 3-perspective)
#   prompt_only    = a source-free prompt, NO passage (AP Lang Q3 argue-from-own-knowledge)
Family = Literal["single", "complementary", "opposing", "synthesis_set", "perspective_set", "prompt_only"]

# ---------------------------------------------------------------------------
# 1. THE EMIT CONTRACT
# ---------------------------------------------------------------------------

@dataclass
class FactSource:
    """One row of the fact-source table. Every figure in a passage MUST have one."""
    fact: str           # the fact as stated in the passage (our words)
    figure: str         # the exact figure/quote (e.g. "1-7 degrees", "86,000 metric tons", "" if qualitative)
    org: str            # source org (e.g. "US EPA", "CDC MMWR", "US DOE")
    url_fetched: str    # the URL a human/agent ACTUALLY fetched (must be http(s))
    verbatim: str = ""  # short verbatim phrase captured from the page (traceability)

@dataclass
class Passage:
    title: str
    text: str
    angle: str = ""     # for paired sets: which side / vantage (e.g. "pro-expansion; EIA/DOE data")

@dataclass
class StimulusRecord:
    id: str
    grade: str                       # "9-10"
    mode: Mode
    family: Family
    prompt: str                      # the writing task
    passages: list[Passage]
    fact_sources: list[FactSource]
    provenance: dict                 # {copyright: "own_authored", rights: "public-domain-sourced", ...}
    modeling_anchor: str = ""        # which real form this models (STAAR / MCAS / Ohio)
    acc_tags: list[str] = field(default_factory=list)
    perspectives: list[str] = field(default_factory=list)  # perspective_set (ACT): the given perspective statements
    # two-bucket architecture fields (all defaulted -> backward compatible with the existing 16 stimuli)
    bucket: str = "lesson"           # "lesson" | "test"
    topic_id: str = ""
    proposition_id: str = ""
    stance: str = ""                 # "" | "pro" | "con" | "nuanced"
    theme_id: str = ""
    facet: str = ""
    connection_point: str = ""
    task_demand: int = 0             # 1-5 when set; 0 = unset
    annotated: bool = False          # lesson bucket may annotate; test bucket may not
    form: str = ""                   # test bucket: which rc form this mirrors ("staar"|"mcas"|"ohio"|"4trait")
    # QC results are filled by qc_stimulus():
    qc: dict = field(default_factory=dict)

# ---------------------------------------------------------------------------
# 2. THE GATES  (each returns (passed: bool, detail: str))
# ---------------------------------------------------------------------------

WORD_MIN, WORD_MAX = 480, 950                 # per-passage word band (spec ~500-900, small tolerance)
LEXILE_GRADE = 10                             # default when a record's grade does not pin a single grade

def _lexile_grade_for(s) -> int:
    """The single grade whose Lexile band a stimulus is gated against, from its `grade` field.
    '9' -> 9 (English I), '10'/'9-10' -> 10 (English II band, the seed default), '11' -> 11, '12' -> 12.
    Keeps G10 behavior identical (a '9-10' record still gates at 10)."""
    g = (getattr(s, "grade", "") or "").strip()
    if g == "9":
        return 9
    if g == "11":
        return 11
    if g == "12":
        return 12
    return LEXILE_GRADE  # "10" or "9-10" or anything else -> the seed's G10 band

def _words(t: str) -> int:
    return len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", t))

SYNTHESIS_SET_MIN, SYNTHESIS_SET_MAX = 3, 6   # source-set size (SBAC 4 / AP Lang 6)

def gate_structure(s: StimulusRecord) -> tuple[bool, str]:
    if not s.prompt.strip():
        return False, "empty prompt"
    # G11 shapes with no single-passage word-band expectation:
    if s.family == "prompt_only":
        if s.passages:
            return False, "prompt_only family must have NO passages (source-free argument)"
        return True, "source-free prompt (no passage), prompt present"
    if s.family == "perspective_set":
        if s.passages:
            return False, "perspective_set family must have NO source passage (perspectives are given in-prompt)"
        if len(s.perspectives) < 2:
            return False, f"perspective_set needs >=2 given perspectives, got {len(s.perspectives)}"
        return True, f"perspective set: {len(s.perspectives)} given perspectives, no source passage"
    if s.family == "synthesis_set":
        n = len(s.passages)
        if not (SYNTHESIS_SET_MIN <= n <= SYNTHESIS_SET_MAX):
            return False, f"synthesis_set needs {SYNTHESIS_SET_MIN}-{SYNTHESIS_SET_MAX} sources, got {n}"
        # each text source obeys the word band; a visual/quantitative source may be shorter (flagged by short text)
        for p in s.passages:
            w = _words(p.text)
            if w > WORD_MAX:
                return False, f"source '{p.title}' is {w} words, over {WORD_MAX}"
            if w < WORD_MIN and "visual" not in (p.angle or "").lower() and "quantitative" not in (p.angle or "").lower():
                return False, f"text source '{p.title}' is {w} words, under {WORD_MIN} (mark angle 'visual'/'quantitative' if a chart/figure)"
        return True, f"synthesis set of {n} sources, all within band (visual sources exempt from the word floor)"
    # G9-10 shapes (single/complementary/opposing)
    need = 2 if s.family in ("complementary", "opposing") else 1
    if len(s.passages) != need:
        return False, f"family '{s.family}' needs {need} passage(s), got {len(s.passages)}"
    for p in s.passages:
        w = _words(p.text)
        if not (WORD_MIN <= w <= WORD_MAX):
            return False, f"passage '{p.title}' is {w} words, outside {WORD_MIN}-{WORD_MAX}"
    return True, f"{len(s.passages)} passage(s), all in word band"

def gate_provenance(s: StimulusRecord) -> tuple[bool, str]:
    """Two shippable provenance paths:
    - 'own_authored': original prose over public-domain facts (argument/explanatory stimuli).
    - 'public_domain': a VERBATIM public-domain real text (analysis-mode stimuli need a real author's
      choices to analyze). Requires a documented PD source (a fact_sources row with the source URL)."""
    cp = (s.provenance or {}).get("copyright", "")
    if cp not in ("own_authored", "public_domain"):
        return False, f"copyright must be 'own_authored' or 'public_domain', got '{cp}'"
    if cp == "public_domain":
        # a PD verbatim text must document its source + PD status
        if not (s.provenance or {}).get("source", "").strip():
            return False, "public_domain stimulus missing provenance['source'] (author/work/year + repo URL)"
        if not any(re.match(r"^https?://", (f.url_fetched or "").strip()) for f in s.fact_sources):
            return False, "public_domain stimulus needs a fact_sources row with the fetched source URL"
    if not s.modeling_anchor.strip():
        return False, "missing modeling_anchor (which real form this models)"
    if not s.acc_tags:
        return False, "missing acc_tags"
    return True, f"provenance complete ({cp})"

def gate_fact_sources(s: StimulusRecord) -> tuple[bool, str]:
    """Anti-fabrication gate. For OWN-AUTHORED stimuli: every numeric figure in the passages must be
    backed by a fact-source row with a real fetched http(s) URL. For PUBLIC-DOMAIN verbatim texts
    (analysis mode): the text is a real author's words (not facts we authored), so the figure-backing
    check does not apply; instead we require the PD source to be documented (a source row with a URL).
    SOURCE-FREE families (perspective_set, prompt_only) provide no external facts (the student argues from
    OWN knowledge), so a fact table is not required; but any fact-source row present must still be valid."""
    if s.family in ("perspective_set", "prompt_only"):
        for fsrc in s.fact_sources:  # optional, but if present must be well-formed
            if not re.match(r"^https?://", (fsrc.url_fetched or "").strip()):
                return False, f"fact-source '{fsrc.fact[:40]}' has no valid fetched URL"
        return True, "source-free family: no external fact table required (argue from own knowledge)"
    if not s.fact_sources:
        return False, "no fact-source table"
    for fsrc in s.fact_sources:
        if not re.match(r"^https?://", fsrc.url_fetched.strip()):
            return False, f"fact-source '{fsrc.fact[:40]}' has no valid fetched URL"
        if not fsrc.org.strip():
            return False, f"fact-source '{fsrc.fact[:40]}' missing org"
    if (s.provenance or {}).get("copyright") == "public_domain":
        # PD verbatim text: source documented above; skip own-authored figure-backing
        return True, f"{len(s.fact_sources)} source row(s), PD text source documented (verbatim real text)"
    # OWN-AUTHORED: every load-bearing figure in the text must trace to a fact-source row
    combined = " ".join(p.text for p in s.passages)
    figures_in_text = set(re.findall(r"\b\d[\d,\.]*\s?(?:%|percent|degrees?|billion|million|metric tons?|MW|hours?)\b", combined, re.I))
    covered = " ".join(f.figure.lower() for f in s.fact_sources)
    unbacked = [fig for fig in figures_in_text if not _figure_covered(fig, covered)]
    if unbacked:
        return False, f"figures in text with no fact-source row (fabrication risk): {unbacked[:5]}"
    return True, f"{len(s.fact_sources)} fact-sources, all with fetched URLs; all in-text figures backed"

def _figure_covered(fig: str, covered: str) -> bool:
    # crude numeric-token match: does the fact-source table mention this figure's number?
    nums = re.findall(r"\d[\d,\.]*", fig)
    return all(n.rstrip(".") in covered for n in nums)

def gate_citable_facts(s: StimulusRecord) -> tuple[bool, str]:
    """Rubrics require citable evidence (FL caps Development at 2 without citation).
    OWN-AUTHORED (argument/explanatory): need >=3 discrete facts to write evidence-based from.
    PUBLIC-DOMAIN (analysis): the student cites the TEXT itself (lines/moves), not external facts, so
    only the source-documentation row(s) are required (>=1)."""
    n = len(s.fact_sources)
    if s.family in ("perspective_set", "prompt_only"):
        return True, "source-free family: student supplies own evidence (no citable-fact requirement)"
    if s.family == "synthesis_set":
        # a synthesis set's "citable facts" are the sources themselves; own-authored needs >=3 sources, PD >=1
        if (s.provenance or {}).get("copyright") == "public_domain":
            return True, f"synthesis set of {len(s.passages)} PD sources (cite across sources)"
        if len(s.passages) < 3:
            return False, f"synthesis_set needs >=3 sources to synthesize, got {len(s.passages)}"
        return True, f"synthesis set of {len(s.passages)} sources + {n} fact rows"
    if (s.provenance or {}).get("copyright") == "public_domain":
        if n < 1:
            return False, "analysis text needs >=1 documented source row"
        return True, f"{n} source row(s); student cites the text's own lines/moves (analysis mode)"
    if n < 3:
        return False, f"only {n} citable facts; need >=3 discrete facts for evidence-based writing"
    return True, f"{n} citable facts"

def gate_source_config(s: StimulusRecord) -> tuple[bool, str]:
    """Source-configuration validity. Replaces gate_two_sidedness for the compose-from-singles world.

    - A composable SINGLE (tagged proposition+stance, or theme+facet+connection_point) is always valid.
    - An untagged single is valid for lesson bucket, or for explanatory/analysis mode (single-source IS the form).
      An untagged single in test+argument fails (a pick-a-side test must be a composed opposing pair).
    - A pre-composed opposing/complementary pair keeps the legacy checks (2 passages, distinct angles, >=2 orgs)."""
    is_prop_member = bool(s.proposition_id and s.stance)
    is_theme_member = bool(s.theme_id and s.facet and s.connection_point)

    # G11 families
    if s.family == "synthesis_set":
        n = len(s.passages)
        orgs = {f.org for f in s.fact_sources if f.org.strip()}
        # a synthesis set must present multiple distinct sources; own-authored sets need >=2 distinct orgs
        if (s.provenance or {}).get("copyright") == "own_authored" and len(orgs) < 2:
            return False, f"synthesis_set (own-authored) should draw on >=2 distinct source orgs, got {len(orgs)}"
        return True, f"synthesis set of {n} sources (>=1 visual/quantitative recommended)"
    if s.family == "perspective_set":
        return True, f"perspective set ({len(s.perspectives)} given perspectives; ACT multi-perspective form)"
    if s.family == "prompt_only":
        return True, "source-free prompt (AP Lang Q3 argue-from-knowledge form)"

    if s.family == "single":
        if is_prop_member or is_theme_member:
            return True, "composable single (tagged to a proposition or theme)"
        if s.bucket == "lesson" or s.mode in ("explanatory", "analysis"):
            return True, "valid single-source (lesson teaching single, or explanatory/analysis form)"
        return False, ("untagged argument single in test bucket: a pick-a-side test needs a composed opposing "
                       "pair, so this single must carry a proposition_id + stance")

    # pre-composed pair (legacy path)
    if s.family in ("complementary", "opposing"):
        if len(s.passages) != 2 or not all(p.angle.strip() for p in s.passages):
            return False, "paired set needs 2 passages each with a recorded angle"
        if s.passages[0].angle.strip().lower() == s.passages[1].angle.strip().lower():
            return False, "the two angles are identical (not genuinely two-sided)"
        if s.family == "opposing":
            orgs = {f.org for f in s.fact_sources}
            if len(orgs) < 2:
                return False, "opposing set should draw on >=2 distinct source orgs (credibility contrast)"
        return True, "pre-composed pair with distinct angles"
    return False, f"unknown family '{s.family}'"

def gate_lexile(s: StimulusRecord) -> tuple[bool, str]:
    """Every passage must land in the grade's Lexile band (per the record's grade) via the readability gate."""
    grade = _lexile_grade_for(s)
    results = []
    for p in s.passages:
        analysis = rg.analyze_text(p.text)
        lex = analysis["lexile_estimate"]
        g = rg.apply_gate(lex, grade)
        results.append((p.title, lex, g["verdict"]))
        if g["verdict"] != "PASS":
            fails = "; ".join(f"{t}={l}L {v}" for t, l, v in results)
            return False, f"Lexile FAIL (G{grade} band {rg.GRADE_GATE[grade][0]}-{rg.GRADE_GATE[grade][1]}L): {fails}"
    return True, f"all passages in G{grade} Lexile band: " + ", ".join(f"{t}={l}L" for t, l, _ in results)

def gate_content(s: StimulusRecord) -> tuple[bool, str]:
    """Content-appropriateness screen (strictest-state envelope). AUTO-REJECT on Tier-3 bright lines;
    a FLAG is NOT a hard fail here (it means 'ship only after human review') so the gate returns True on
    FLAG but records the flags in the detail. REJECT fails the gate. First-pass filter, not legal review."""
    import content_screen as cs
    is_pd = (s.provenance or {}).get("copyright") == "public_domain"
    r = cs.screen(s.passages, prompt=s.prompt, mode=s.mode, family=s.family, is_verbatim_pd=is_pd)
    s.qc.setdefault("content_screen", r)  # stash full result for the record
    if r["verdict"] == "REJECT":
        why = "; ".join(x["check"] for x in r["rejects"])
        return False, f"content REJECT (bright-line): {why}"
    if r["verdict"] == "FLAG":
        why = "; ".join(x["check"] for x in r["flags"])
        return True, f"content PASS-with-FLAGS (human review before ship): {why}"
    return True, "content clean (no bright-line, no flags)"

def gate_bucket_profile(s: StimulusRecord) -> tuple[bool, str]:
    """Profile rules that differ by bucket. Test: no annotation, must carry a form. Lesson: annotation allowed."""
    if s.bucket not in ("lesson", "test"):
        return False, f"bucket must be 'lesson' or 'test', got '{s.bucket}'"
    if s.bucket == "test":
        if s.annotated:
            return False, "test bucket stimulus must not be annotated (annotation can cue the answer)"
        if not s.form.strip():
            return False, "test bucket stimulus must carry a form (staar|mcas|ohio|4trait) for calibration"
    return True, f"{s.bucket} profile ok"

def gate_equivalent_form(s: StimulusRecord, anchor_set=None) -> tuple[bool, str]:
    """Test bucket only: the stimulus must sit inside the human-scored anchor band for {grade, mode, form}.
    When no anchor_set is supplied, or it has no anchors for that form yet, pass as UNCERTIFIED so the seed pool
    can be built before anchors are scored. Lesson bucket is n/a."""
    if s.bucket != "test":
        return True, "n/a (lesson bucket)"
    if anchor_set is None:
        return True, "no anchor set supplied; test form UNCERTIFIED (calibrate before go-live)"
    passage_count = len(s.passages)
    lexile = rg.analyze_text(s.passages[0].text)["lexile_estimate"] if s.passages else 0
    band = anchor_set.band(s.grade, s.mode, s.form)
    if band is None:
        return True, f"no anchors for {s.grade}/{s.mode}/{s.form}; test form UNCERTIFIED (calibrate before go-live)"
    ok, why = anchor_set.equivalent_form_ok(s.grade, s.mode, s.form, lexile, passage_count, s.task_demand or band.demand_min)
    return ok, why

GATES = [
    ("structure", gate_structure),
    ("provenance", gate_provenance),
    ("fact_sources", gate_fact_sources),
    ("citable_facts", gate_citable_facts),
    ("source_config", gate_source_config),
    ("lexile", gate_lexile),
    ("content", gate_content),
    ("bucket_profile", gate_bucket_profile),
    ("equivalent_form", gate_equivalent_form),
]

# ---------------------------------------------------------------------------
# 3. THE QC HARNESS
# ---------------------------------------------------------------------------

def qc_stimulus(s: StimulusRecord) -> dict:
    """Run every gate. Returns {passed: bool, gates: {name: {passed, detail}}, first_failure: str|None}."""
    gate_results = {}
    first_failure = None
    for name, fn in GATES:
        try:
            passed, detail = fn(s)
        except Exception as e:
            passed, detail = False, f"gate error: {e!r}"
        gate_results[name] = {"passed": passed, "detail": detail}
        if not passed and first_failure is None:
            first_failure = name
    overall = all(g["passed"] for g in gate_results.values())
    s.qc = {"passed": overall, "gates": gate_results, "first_failure": first_failure}
    return s.qc

def qc_report(s: StimulusRecord) -> str:
    r = s.qc or qc_stimulus(s)
    lines = [f"=== QC: {s.id} ({s.mode}/{s.family}) -> {'PASS' if r['passed'] else 'FAIL'} ==="]
    for name, g in r["gates"].items():
        mark = "PASS" if g["passed"] else "FAIL"
        lines.append(f"  [{mark}] {name}: {g['detail']}")
    return "\n".join(lines)

# ---------------------------------------------------------------------------
# self-test with the nuclear opposing-pair exemplar (revised, Lexile-passed prose)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    demo = StimulusRecord(
        id="ACC-W910-ARG-OPP-DEMO",
        grade="9-10", mode="argument", family="opposing",
        modeling_anchor="Ohio ELA II / MD MCAP (opposing-view pick-a-side)",
        acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "CCSS.W.9-10.1"],
        prompt="Weighing both sources, write an argumentative essay stating your position on whether the US should build more nuclear power. Support your claim with evidence from both sources and address at least one objection.",
        passages=[
            Passage(title="The Case for More Nuclear Power", angle="pro-expansion; EIA/DOE operations data", text=(
                "When Americans flip a light switch, about one in five times the power comes from a nuclear plant. "
                "Nuclear energy has supplied roughly 20 percent of U.S. electricity every year since 1990. Today, 57 "
                "nuclear plants run 96 reactors across 28 states. Together they produce a large share of the nation's "
                "power. Supporters say this strength is exactly why the country should build more. One of the strongest "
                "points is that nuclear runs almost all the time. Engineers use a number called the capacity factor to "
                "measure this. It shows how often a source makes power at full strength. In 2024, nuclear plants ran at "
                "more than 92 percent. That was far ahead of every other source. A country needs electricity every hour "
                "of every day. That steady output is valuable in a way that wind and solar cannot always match. Nuclear "
                "power has another benefit that supporters feel is often missed. Plants that burn coal or gas release "
                "carbon dioxide into the air. Nuclear reactors do not produce that pollution while they run. Carbon "
                "dioxide is the main gas linked to a warming climate. So a source that makes one-fifth of our power "
                "without it is, to supporters, a tool we should use more.")),
            Passage(title="The Unsolved Problem of Nuclear Waste", angle="anti-expansion; GAO oversight watchdog", text=(
                "Nuclear power plants make electricity without releasing carbon dioxide while they run, and that is a "
                "real benefit. But a government watchdog warns of a problem that has gone unsolved for decades. The "
                "United States has no permanent place to put the dangerous waste that nuclear plants create. That waste "
                "is piling up. The Government Accountability Office reports about 86,000 metric tons of spent nuclear "
                "fuel stored at 75 sites. The amount grows by about 2,000 metric tons every year. This fuel is not in a "
                "secure national site. It sits at plants in 33 states, in the communities where the power was made. The "
                "reason is a long political failure. The only site ever chosen for permanent storage was Yucca Mountain "
                "in Nevada. But in 2010 the government stopped work there. Since then no plan has replaced it. The waste "
                "stays dangerous for thousands of years. It is also costly. Because the government promised to take the "
                "waste and did not, it has already paid companies about 9 billion dollars to store it. Those who are "
                "cautious ask a fair question. Why build more plants, and make more waste that lasts thousands of years, "
                "before we have solved what to do with the waste we already have?")),
        ],
        fact_sources=[
            FactSource("Nuclear share of US electricity since 1990", "20 percent", "US EIA", "https://www.eia.gov/energyexplained/nuclear/"),
            FactSource("Plants/reactors/states", "57 / 96 / 28", "US EIA", "https://www.eia.gov/tools/faqs/faq.php?id=207&t=3"),
            FactSource("Nuclear capacity factor 2024", "92 percent", "US DOE", "https://www.energy.gov/ne/articles/what-generation-capacity"),
            FactSource("Spent fuel accumulated / sites", "86,000 metric tons / 75", "US GAO", "https://www.gao.gov/products/gao-21-603"),
            FactSource("Annual growth of spent fuel", "2,000 metric tons", "US GAO", "https://www.gao.gov/products/gao-21-603"),
            FactSource("Govt paid to store fuel", "9 billion", "US GAO", "https://www.gao.gov/products/gao-21-603"),
        ],
        provenance={"copyright": "own_authored", "rights": "public-domain-sourced (US federal)", "authored": "2026-07-07"},
    )
    qc_stimulus(demo)
    print(qc_report(demo))
    # NOTE: the demo passages are ABBREVIATED (~200 words) for readability, so the demo intentionally fails
    # the 480-word structure gate. The demo is illustrative; the real bank (full-length passages) is verified
    # by bank_loader.py. This file's exit status reflects the SELF-TEST ASSERTIONS below, not the abbreviated demo.

    # two-bucket fields: backward-compatible defaults
    assert demo.bucket == "lesson", "default bucket is lesson"
    assert demo.topic_id == "" and demo.proposition_id == "" and demo.task_demand == 0
    assert demo.annotated is False and demo.form == ""
    _t = StimulusRecord(id="X", grade="9-10", mode="argument", family="single", prompt="p",
                        passages=[Passage("t", "w " * 500)], fact_sources=[], provenance={},
                        bucket="test", topic_id="nuclear_power", form="staar", task_demand=3)
    assert _t.bucket == "test" and _t.topic_id == "nuclear_power" and _t.form == "staar"
    print("stimulus_contract two-bucket fields OK")

    # profile gate: a TEST stimulus may not be annotated and must carry a form
    _bad = StimulusRecord(id="B", grade="9-10", mode="argument", family="single", prompt="p",
                          passages=[Passage("t", "w " * 500)], fact_sources=[], provenance={},
                          bucket="test", annotated=True, form="staar")
    ok, why = gate_bucket_profile(_bad)
    assert not ok and "annotat" in why.lower(), "test bucket cannot be annotated"
    _bad2 = StimulusRecord(id="B2", grade="9-10", mode="argument", family="single", prompt="p",
                           passages=[Passage("t", "w " * 500)], fact_sources=[], provenance={},
                           bucket="test", form="")
    ok2, why2 = gate_bucket_profile(_bad2)
    assert not ok2 and "form" in why2.lower(), "test bucket needs a form"
    _lesson_annot = StimulusRecord(id="L", grade="9-10", mode="argument", family="single", prompt="p",
                                   passages=[Passage("t", "w " * 500)], fact_sources=[], provenance={},
                                   bucket="lesson", annotated=True)
    ok3, _ = gate_bucket_profile(_lesson_annot)
    assert ok3, "lesson bucket may be annotated"

    # equivalent-form gate against an anchor set
    aset = ca.AnchorSet()
    aset.add(ca.Anchor("a1", "9-10", "argument", "staar", 1080, 1, 3))
    aset.add(ca.Anchor("a2", "9-10", "argument", "staar", 1160, 1, 4))
    _testfit = StimulusRecord(id="T", grade="9-10", mode="argument", family="single", prompt="p",
                              passages=[Passage("t", "w " * 500)], fact_sources=[], provenance={},
                              bucket="test", form="staar", task_demand=3)
    # single passage -> passage_count 1 matches anchors; lexile of "w "*500 will be low, so expect a band failure msg
    ok4, why4 = gate_equivalent_form(_testfit, anchor_set=aset)
    assert ("lexile" in why4.lower()) or ok4, "equivalent-form gate consults the anchor band"
    # no anchors for a different form -> uncertified pass (seed can be built pre-calibration)
    ok5, why5 = gate_equivalent_form(
        StimulusRecord(id="T2", grade="9-10", mode="argument", family="single", prompt="p",
                       passages=[Passage("t", "w " * 500)], fact_sources=[], provenance={},
                       bucket="test", form="ohio", task_demand=3), anchor_set=aset)
    assert ok5 and "uncertified" in why5.lower()
    # lesson bucket -> n/a pass
    ok6, _ = gate_equivalent_form(_lesson_annot, anchor_set=aset)
    assert ok6
    print("stimulus_contract profile gates OK")

    # composable single: argument single tagged as a proposition member (pro) -> valid
    _member = StimulusRecord(id="M", grade="9-10", mode="argument", family="single", prompt="p",
                             passages=[Passage("t", "w " * 500)], fact_sources=[], provenance={},
                             bucket="test", form="staar", proposition_id="prop_x", stance="pro")
    okm, _ = gate_source_config(_member)
    assert okm, "argument single tagged to a proposition is a valid composable single"
    # untagged argument single in TEST bucket -> fail (pick-a-side test needs a pair)
    _untagged = StimulusRecord(id="U", grade="9-10", mode="argument", family="single", prompt="p",
                               passages=[Passage("t", "w " * 500)], fact_sources=[], provenance={},
                               bucket="test", form="staar")
    oku, whyu = gate_source_config(_untagged)
    assert not oku and "proposition" in whyu.lower(), "untagged argument test single must be a proposition member"
    # untagged explanatory single -> valid (single-source IS the form)
    _info = StimulusRecord(id="I", grade="9-10", mode="explanatory", family="single", prompt="p",
                           passages=[Passage("t", "w " * 500)], fact_sources=[], provenance={},
                           bucket="test", form="mcas")
    oki, _ = gate_source_config(_info)
    assert oki, "explanatory single is a valid single-source form"
    print("stimulus_contract source-config gate OK")

    # reaching here means every self-test assertion above passed (the abbreviated demo's structure failure is
    # expected and does not gate this file; the real bank is verified by bank_loader.py).
    print("stimulus_contract self-test PASS")
    sys.exit(0)
