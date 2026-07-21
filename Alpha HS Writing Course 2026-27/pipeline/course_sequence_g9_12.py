"""
course_sequence_g9_12.py - THE single machine-readable source of truth for the G9-12 writing course.

Everything downstream (the coverage matrix, the lesson generator, the gate/QC code, the renderers) MUST
import the KC map, ACC anchoring, unit architecture, prerequisite DAG, and gate spec FROM HERE - so the
common-standard anchoring cannot drift across artifacts. Prose docs (KC_Map_and_Unit_Arch_G9-12.md,
Sentence_Skill_Roster_FINAL.md) are the human-readable render OF this data; this module is authoritative.

ANCHOR: the AlphaCommonCore (ACC) spine (05_AlphaCommonCore_Writing_Spine.md) - the empirical >=2-state
union of all 50 states' writing standards. CCSS/TEKS are SUBSETS of ACC; AP/ACT are thin overlays.

WHAT THIS ENCODES (validated by the __main__ self-test):
  - ACC_SPINE          : the 35-code common standard (core §1 + net-new §3) + owner category
  - HS_KCS             : every HS-owned KC (id, grade, ACC tags, CCSS/TEKS/AP-ACT tags, funnel, type, gateway)
  - EXTERNAL_OWNED     : skills owned by the separate HS Language/Vocabulary/Reading courses (gated, not taught)
  - DESCOPED           : explicit documented deferrals (narrative, AP Lit, full research)
  - UNITS              : per-grade unit architecture (ordered; each unit's KCs + gateway + gate)
  - PREREQ_DAG         : the internal HS prerequisite graph (acyclic, forward-only across grades)
  - Helpers            : owning_grade, kcs_for_acc, is_owned, inherited_at, unit_order, ...

OPEN SEQUENCE-BUILDER FLAG - CROSS-LESSON SPACING (council, KH, grade-A; LS-feedback 2026-07-20):
  The per-lesson `gate_check_cadence` (in lesson_contract.py) enforces retrieval-practice WITHIN a lesson
  (a check every N teach cards). That is necessary but NOT sufficient for durable recall: the same taught
  tools (the 3-question tests, warrant, synthesis, counterclaim, etc.) must be RE-RETRIEVED in LATER
  lessons (distributed practice; spacing effect g=0.74). That is a SEQUENCE-level responsibility this
  module owns, and it is NOT yet encoded here (no gate can check it per-lesson). TODO for a future
  spacing/interleaving pass: add a cross-lesson retrieval schedule (which earlier KCs each lesson should
  recruit) so a tool taught in lesson L is deliberately retrieved again in L+k. Do not mistake a green
  in-lesson cadence gate for handled retention. See INCEPT_INTEGRATION.md / the LS-feedback plan for context.

Dependency-free (stdlib). Run: python pipeline/course_sequence_g9_12.py   (prints self-test result)
Exit 0 iff ALL invariants hold.

Provenance: converges the reconciled KC map (KC_Map_and_Unit_Arch_G9-12.md), the ACC spine
(05_...), the backward-trace coverage audit (_evidence/kc_coverage_audit.md), the council-reviewed
sentence decomposition (Sentence_Skill_Roster_FINAL.md), and Noel's scope decisions 2026-07-08.
"""
from __future__ import annotations

GRADE_ORDER = {"G9": 0, "G10": 1, "G11": 2, "G12": 3}

# ===========================================================================
# 1. ACC SPINE - the common standard (source of truth). need: hs | external | descoped.
#    §3 net-new filtered by Noel's rule: WRITING owns only the TESTED slices.
# ===========================================================================
ACC_SPINE = [
    # --- §1 core (CCSS-anchored; ~37+ states each) ---
    dict(code="ACC.W.ARG.1",  name="Precise defensible claim; distinguish opposing", section="core", need="hs"),
    dict(code="ACC.W.ARG.2",  name="Develop claims AND counterclaims fairly", section="core", need="hs"),
    dict(code="ACC.W.ARG.3",  name="Transitions/cohesion linking claim-reason-evidence", section="core", need="hs"),
    dict(code="ACC.W.ARG.4",  name="Formal style / objective tone", section="core", need="hs"),
    dict(code="ACC.W.ARG.5",  name="Concluding statement following from argument", section="core", need="hs"),
    dict(code="ACC.W.INFO.1", name="Introduce & organize complex ideas", section="core", need="hs"),
    dict(code="ACC.W.INFO.2", name="Develop with facts/details/examples", section="core", need="hs"),
    dict(code="ACC.W.INFO.3", name="Transitions/cohesion across ideas", section="core", need="hs"),
    dict(code="ACC.W.INFO.4", name="Precise language + domain vocabulary", section="core", need="external"),
    dict(code="ACC.W.INFO.5", name="Formal style; concluding section", section="core", need="hs"),
    dict(code="ACC.W.INFO.6", name="Analyze complex texts (analysis)", section="core", need="hs"),
    dict(code="ACC.W.PROD.1", name="Writing appropriate to task/purpose/audience", section="core", need="hs"),
    dict(code="ACC.W.PROC.1", name="Plan/draft/revise/edit (recursive)", section="core", need="hs"),
    dict(code="ACC.W.PROC.2", name="Revise for clarity/style/audience", section="core", need="hs"),
    dict(code="ACC.W.RES.1",  name="Conduct short & sustained research", section="core", need="descoped"),
    dict(code="ACC.W.RES.2",  name="Formulate & refine inquiry questions", section="core", need="descoped"),
    dict(code="ACC.W.SRC.1",  name="Gather from multiple credible sources; assess", section="core", need="hs"),
    dict(code="ACC.W.SRC.2",  name="Integrate evidence; cite; avoid plagiarism", section="core", need="hs"),
    dict(code="ACC.W.SRC.3",  name="Draw evidence from texts (write-about-reading)", section="core", need="hs"),
    dict(code="ACC.W.CONV.1", name="Command of grammar & usage", section="core", need="external"),
    dict(code="ACC.W.CONV.2", name="Capitalization, punctuation, spelling", section="core", need="external"),
    dict(code="ACC.W.CONV.3", name="Apply knowledge of language / style", section="core", need="external"),
    dict(code="ACC.W.NARR.1", name="Narrative: context/POV/characters", section="core", need="descoped"),
    dict(code="ACC.W.NARR.2", name="Narrative techniques", section="core", need="descoped"),
    dict(code="ACC.W.NARR.3", name="Narrative sequence/coherence", section="core", need="descoped"),
    dict(code="ACC.W.NARR.4", name="Narrative precise/sensory language", section="core", need="descoped"),
    dict(code="ACC.W.NARR.5", name="Narrative reflective conclusion", section="core", need="descoped"),
    # --- §3 net-new (>=2 deviation states, beyond CCSS); WRITING owns only tested slices ---
    dict(code="ACC.W.TECH.1",  name="Multimodal/digital composition", section="net_new", need="descoped",
         note="8 states but standards-only, not summatively tested; QTI text-first"),
    dict(code="ACC.W.MEDIA.1", name="Analyze/evaluate media messages/bias", section="net_new", need="external",
         note="reading/language territory; not writing-composition, not summatively tested"),
    dict(code="ACC.W.WORK.1",  name="Workplace/technical writing", section="net_new", need="descoped",
         note="tested only in VA G12; deferred-with-note (in-scope iff VA is a target)"),
    dict(code="ACC.W.WORK.2",  name="Correspondence as a genre", section="net_new", need="descoped",
         note="verified NOT tested (retired from STAAR); descope"),
    dict(code="ACC.W.DIG.1",   name="Digital citizenship / ethical source use", section="net_new", need="external",
         note="civic-literacy/library; not summatively tested as writing"),
    dict(code="ACC.W.INQ.1",   name="Inquiry/reflection cycle", section="net_new", need="hs",
         note="TESTED slice = source-evaluation, owned by C.11.08; full cycle deferred"),
    dict(code="ACC.W.BLEND.1", name="Blend multiple modes in one piece", section="net_new", need="descoped",
         note="standards-only, not summatively tested"),
    dict(code="ACC.W.CRAFT.1", name="Discrete word-choice/voice/organization craft", section="net_new", need="external",
         note="Language course (craft) + D.12.01 voice woven"),
]
ACC_CODES = {a["code"] for a in ACC_SPINE}

# ===========================================================================
# 2. HS-OWNED KCs. type: D(iscrimination)/P(roduction)/S(tructure)/I(ntegrative)/woven.
#    acc[] = ACC codes this KC carries (primary first). ccss/teks = subset alignment. sec = AP/ACT overlay.
#    funnel = the tested capability it serves. gateway = blocks downstream if unmastered.
# ===========================================================================
HS_KCS = [
    # G9
    dict(id="C.9.01", grade="G9", type="D->P", gateway=True,  funnel="argument",
         name="Defensible argument claim", acc=["ACC.W.ARG.1"], ccss=["W.9-10.1a"], teks=["EI.10.C"], sec=["ACT.1"]),
    dict(id="C.9.05", grade="G9", type="D->P", gateway=True,  funnel="informational",
         name="Informational controlling-idea", acc=["ACC.W.INFO.1"], ccss=["W.9-10.2a"], teks=["EI.9.B"], sec=[]),
    dict(id="C.9.02", grade="G9", type="P",    gateway=False, funnel="evidence",
         name="Attributed-evidence sentence", acc=["ACC.W.SRC.2"], ccss=["W.9-10.1b", "W.9-10.8"], teks=["EI.11.H"], sec=["AP.3"]),
    dict(id="C.9.03", grade="G9", type="P",    gateway=True,  funnel="reasoning",
         name="Reason/warrant sentence", acc=["ACC.W.INFO.2"], ccss=["W.9-10.1b", "W.9-10.2b"], teks=["EI.10.C"], sec=["AP.5", "ACT.4"]),
    dict(id="C.9.06", grade="G9", type="D->P", gateway=False, funnel="production_of_writing",
         name="Transitions, cohesion & formal tone", acc=["ACC.W.ARG.3", "ACC.W.INFO.3", "ACC.W.ARG.4"],
         ccss=["W.9-10.1c", "W.9-10.2c", "W.9-10.1d"], teks=["EI.9.C"], sec=["ACT.9"]),
    dict(id="C.9.04", grade="G9", type="I",    gateway=True,  funnel="essay",
         name="Single-source essay (argument + informational)",
         acc=["ACC.W.PROD.1", "ACC.W.ARG.5", "ACC.W.INFO.2", "ACC.W.INFO.3", "ACC.W.INFO.5", "ACC.W.PROC.1"],
         ccss=["W.9-10.1", "W.9-10.1e", "W.9-10.2", "W.9-10.2e", "W.9-10.4", "W.9-10.5", "W.9-10.9"],
         teks=["EI.10.C", "EI.9.B"], sec=[]),
    dict(id="C.9.07", grade="G9", type="D->P", gateway=False, funnel="counterargument",
         name="Acknowledge and answer a counterargument (introductory)", acc=["ACC.W.ARG.2"],
         ccss=["W.9-10.1a"], teks=[], sec=["ACT.2"]),
    # G10
    dict(id="C.10.01", grade="G10", type="P", gateway=True,  funnel="counterargument",
         name="Counterclaim-aware claim", acc=["ACC.W.ARG.2"], ccss=["W.9-10.1a"], teks=["EII.10.C"], sec=["ACT.2"]),
    dict(id="C.10.02", grade="G10", type="P", gateway=True,  funnel="analysis",
         name="Device->effect->warrant (text-dependent analysis)", acc=["ACC.W.INFO.6", "ACC.W.SRC.3"],
         ccss=["W.9-10.9", "RI.9-10.6"], teks=["EII.5.B"], sec=[]),
    dict(id="C.10.05", grade="G10", type="D->P", gateway=False, funnel="production_of_writing",
         name="Rhetorical revision: add/delete/reorder + organization", acc=["ACC.W.PROC.2"],
         ccss=["W.9-10.4", "W.9-10.5"], teks=["EII.9.C"], sec=["ACT.7", "ACT.8"]),
    dict(id="C.10.06", grade="G10", type="I", gateway=True,  funnel="multisource",
         name="Cross-text (2-3 source) argument/analysis", acc=["ACC.W.SRC.1"],
         ccss=["W.9-10.7", "W.9-10.8", "W.9-10.9"], teks=["EII.5.D"], sec=[]),
    dict(id="C.10.03", grade="G10", type="I", gateway=True,  funnel="analysis",
         name="Analysis essay strategy", acc=["ACC.W.INFO.6", "ACC.W.INFO.2", "ACC.W.SRC.3"],
         ccss=["W.9-10.2", "W.9-10.9"], teks=["EII.5.B"], sec=[]),
    dict(id="C.10.04", grade="G10", type="woven", gateway=False, funnel="production_of_writing",
         name="Precision-in-argument (applied revision pass, woven)", acc=["ACC.W.PROC.2"],
         ccss=["W.9-10.4", "W.9-10.5"], teks=["EII.9.C"], sec=[]),
    # G11
    dict(id="C.11.01", grade="G11", type="P", gateway=True,  funnel="argument",
         name="Nuanced claim", acc=["ACC.W.ARG.1"], ccss=["W.11-12.1a"], teks=[], sec=["AP.1", "ACT.6"]),
    dict(id="C.11.03", grade="G11", type="I", gateway=True,  funnel="rhetorical_analysis",
         name="Rhetorical-analysis essay (author's choices)", acc=["ACC.W.INFO.6"],
         ccss=["W.11-12.9", "RI.11-12.6"], teks=[], sec=["APL.4"]),
    dict(id="C.11.02", grade="G11", type="I", gateway=True,  funnel="synthesis",
         name="Cross-source synthesis essay", acc=["ACC.W.SRC.1"],
         ccss=["W.11-12.7", "W.11-12.8", "W.11-12.9"], teks=[], sec=["APL.3"]),
    dict(id="C.11.08", grade="G11", type="D", gateway=False, funnel="source_evaluation",
         name="Evaluate source credibility/bias", acc=["ACC.W.SRC.1", "ACC.W.INQ.1"],
         ccss=["W.11-12.8"], teks=["EII.11.G"], sec=[]),
    dict(id="C.11.06", grade="G11", type="P->I", gateway=True, funnel="source_free_argument",
         name="Argue from own knowledge (source-free)", acc=["ACC.W.ARG.1"], ccss=["W.11-12.1"], teks=[], sec=["AP.4"]),
    dict(id="C.11.07", grade="G11", type="P->I", gateway=False, funnel="multi_perspective",
         name="Multi-perspective argument (3 given perspectives)", acc=["ACC.W.ARG.2"], ccss=["W.11-12.1"], teks=[], sec=["ACT.2", "ACT.3"],
         overlay="ACT/AP exam overlay on CCSS W.11-12.1 argument; the given-perspectives format is an exam construct on the core argument standard"),
    dict(id="C.11.04", grade="G11", type="woven", gateway=False, funnel="production_of_writing",
         name="Rhetorical concision/style (applied revision pass, woven)", acc=["ACC.W.PROC.2"],
         ccss=["W.11-12.4", "W.11-12.5"], teks=[], sec=["ACT.10"]),
    dict(id="C.11.05", grade="G11", type="P", gateway=False, funnel="timed",
         name="Timed-writing strategy", acc=["ACC.W.PROC.1"], ccss=["W.11-12.4", "W.11-12.10"], teks=[], sec=["AP.9"],
         overlay="AP/ACT exam overlay on CCSS W.11-12.4/10 (produce coherent writing + write routinely on demand); the clock is an exam condition, not a CCSS construct"),
    # G12
    dict(id="C.12.01", grade="G12", type="I", gateway=True, funnel="sophistication",
         name="AP sophistication (significance/context/complexity) [intro G11]", acc=["ACC.W.ARG.2"],
         ccss=["W.11-12.1", "W.11-12.2", "W.11-12.8", "W.11-12.9"], teks=[], sec=["AP.8", "ACT.5"],
         overlay="AP exam overlay (Row C sophistication) on CCSS W.11-12.1/2; sophistication is an AP rubric band, not a standalone CCSS construct"),
    dict(id="C.12.02", grade="G12", type="I", gateway=True, funnel="timed",
         name="Budget-managed sustained AP writing (self-imposed budget; external proctored timed-mock before AP.9 sign-off)",
         acc=["ACC.W.PROD.1"], ccss=["W.11-12.4", "W.11-12.5", "W.11-12.9", "W.11-12.10"], teks=[], sec=["AP.9"],
         overlay="AP exam overlay on CCSS W.11-12.4/5/10; timed on-demand production is an exam condition (Timeback has no clock -> external proctored mock)"),
    dict(id="D.12.01", grade="G12", type="woven", gateway=False, funnel="voice",
         name="Voice through syntactic choice (woven)", acc=["ACC.W.CONV.3"], ccss=["W.11-12.4"], teks=[], sec=[]),
]
KC_BY_ID = {k["id"]: k for k in HS_KCS}

# ===========================================================================
# 3. EXTERNALLY-OWNED (gated; separate HS courses/apps) + DESCOPED (documented deferrals).
# ===========================================================================
EXTERNAL_OWNED = {
    "conventions":            "HS Language course + EGUMPP (conventions G3-10)",
    "knowledge_of_language":  "HS Language course (precision/concision/style-tone as SR editing)",
    "sentence_mechanics":     "EGUMPP + AlphaWrite (combining, appositives, subordination, parallelism, phrase/clause, modifiers)",
    "vocabulary":             "HS Vocabulary course + AlphaRead",
    "reading_comprehension":  "Reading course / AlphaRead (incl. HS-Lexile + literary/nonfiction)",
}
DESCOPED = {
    "narrative":             "DESCOPED now, BACKLOGGED phase 2 (7 systems test it)",
    "ap_literature":         "NAMED-BUT-DEFERRED (B2 = AP Lang only; literary-analysis KCs queued)",
    "research_process_full": "DEFERRED (locate/present); source-evaluation slice covered (C.11.08)",
}

# ===========================================================================
# 4. UNIT ARCHITECTURE - per grade, ordered. Each unit: id, title, KC ids, gateway KC, is course gate.
#    Scaffold (all units): entry retrieval-gate (app-owned substrate) -> genre-specific sentence move
#    just-in-time -> paragraph phase -> staged essay -> calibration/revision woven.
# ===========================================================================
UNITS = {
    "G9": [
        dict(id="G9.U1", title="Claim/controlling-idea + evidence", kcs=["C.9.01", "C.9.05", "C.9.02"], gateway="C.9.01", course_gate=False),
        dict(id="G9.U2", title="Reasoning + the complete paragraph", kcs=["C.9.03"], gateway="C.9.03", course_gate=False),
        dict(id="G9.U3", title="Cohesion, tone & paragraph mastery", kcs=["C.9.06"], gateway="C.9.06", course_gate=False),
        dict(id="G9.U4", title="Counterargument", kcs=["C.9.07"], gateway="C.9.07", course_gate=False),
        dict(id="G9.U5", title="Single-source essay + gate", kcs=["C.9.04"], gateway="C.9.04", course_gate=True),
    ],
    "G10": [
        dict(id="G10.U1", title="Counterargument", kcs=["C.10.01"], gateway="C.10.01", course_gate=False),
        dict(id="G10.U2", title="Text-dependent analysis", kcs=["C.10.02"], gateway="C.10.02", course_gate=False),
        dict(id="G10.U3", title="Rhetorical revision", kcs=["C.10.05"], gateway=None, course_gate=False),
        dict(id="G10.U4", title="Cross-text analysis essay", kcs=["C.10.06", "C.10.03", "C.10.04"], gateway="C.10.06", course_gate=True),
    ],
    "G11": [
        dict(id="G11.U1", title="Nuance", kcs=["C.11.01"], gateway="C.11.01", course_gate=False),
        dict(id="G11.U2", title="Rhetorical analysis", kcs=["C.11.03"], gateway="C.11.03", course_gate=False),
        dict(id="G11.U3", title="Synthesis + source evaluation", kcs=["C.11.02", "C.11.08"], gateway="C.11.02", course_gate=False),
        dict(id="G11.U4", title="Source-free argument", kcs=["C.11.06"], gateway="C.11.06", course_gate=False),
        dict(id="G11.U5", title="Multi-perspective argument", kcs=["C.11.07"], gateway="C.11.07", course_gate=False),
        dict(id="G11.U6", title="Timing, calibration + task-type gate", kcs=["C.11.05", "C.11.04"], gateway="C.11.05", course_gate=True),
    ],
    "G12": [
        dict(id="G12.U1", title="Sophistication mastery", kcs=["C.12.01"], gateway="C.12.01", course_gate=False),
        dict(id="G12.U2", title="Budget-managed sustained AP writing", kcs=["C.12.02", "D.12.01"], gateway="C.12.02", course_gate=True),
    ],
}

# ===========================================================================
# 5. INTERNAL HS PREREQUISITE DAG (from Sentence_Skill_Roster_FINAL 2A + KC map).
#    edge A -> [B,...] means A is a prerequisite of B. Must be acyclic + forward-only across grades.
# ===========================================================================
PREREQ_DAG = {
    "C.9.01": ["C.9.03", "C.9.04", "C.10.01", "C.10.05", "C.9.07"],
    "C.9.05": ["C.9.04"],
    "C.9.02": ["C.9.04", "C.11.02", "C.9.07"],
    "C.9.03": ["C.9.04", "C.10.02", "C.9.07"],
    "C.9.06": ["C.9.04"],
    "C.9.04": ["C.10.03", "C.10.06"],
    "C.9.07": ["C.9.04", "C.10.01"],
    "C.10.01": ["C.11.01", "C.11.07"],
    "C.10.02": ["C.10.03", "C.11.03"],
    "C.10.05": ["C.10.04", "C.11.04"],
    "C.10.06": ["C.10.03"],
    "C.11.01": ["C.11.06", "C.12.01"],
    "C.11.02": ["C.12.01"],
    "C.11.03": ["C.12.01"],
    "C.11.08": ["C.11.02"],
    "C.12.01": ["C.12.02"],
}

# ===========================================================================
# Helpers (the import surface for downstream consumers)
# ===========================================================================
def owning_grade(kc_id: str) -> str:
    return KC_BY_ID[kc_id]["grade"]

def kcs_for_acc(acc_code: str) -> list[str]:
    return [k["id"] for k in HS_KCS if acc_code in k["acc"]]

def acc_owner(acc_code: str) -> tuple[str, str]:
    """Return (owner_category, detail) for an ACC code: hs / external / descoped."""
    a = next((x for x in ACC_SPINE if x["code"] == acc_code), None)
    if not a:
        return ("unknown", "not an ACC code")
    if a["need"] == "hs":
        owners = kcs_for_acc(acc_code)
        return ("hs", ", ".join(owners) if owners else "NO HS KC")
    if a["need"] == "external":
        return ("external", "external HS course / woven")
    return ("descoped", DESCOPED.get(_descope_key(acc_code), a.get("note", "documented descope")))

def _descope_key(acc_code: str) -> str:
    if acc_code.startswith("ACC.W.NARR"):
        return "narrative"
    if acc_code in ("ACC.W.RES.1", "ACC.W.RES.2"):
        return "research_process_full"
    return acc_code

def gateway_kcs(grade: str) -> list[str]:
    return [k["id"] for k in HS_KCS if k["grade"] == grade and k["gateway"]]

def unit_order(grade: str) -> list[str]:
    return [u["id"] for u in UNITS[grade]]

def course_gate_kc(grade: str) -> str | None:
    for u in UNITS[grade]:
        if u["course_gate"]:
            return u["gateway"]
    return None

def topo_order() -> list[str]:
    """Kahn topological sort of the prereq DAG over all HS KC ids. Raises on cycle."""
    from collections import defaultdict, deque
    indeg = defaultdict(int)
    nodes = set(KC_BY_ID)
    for u, vs in PREREQ_DAG.items():
        for v in vs:
            indeg[v] += 1
    q = deque(sorted(n for n in nodes if indeg[n] == 0))
    order = []
    while q:
        u = q.popleft(); order.append(u)
        for v in PREREQ_DAG.get(u, []):
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if len(order) != len(nodes):
        raise ValueError("PREREQ_DAG has a cycle")
    return order


# ===========================================================================
# SELF-TEST (the regression guard). Run: python pipeline/course_sequence_g9_12.py
# ===========================================================================
if __name__ == "__main__":
    import sys
    errs = []

    # 1. every KC has a valid grade, type, funnel, and >=1 ACC tag; every ACC tag is a real ACC code
    valid_types = {"D", "P", "S", "I", "woven", "D->P", "P->I"}
    for k in HS_KCS:
        if k["grade"] not in GRADE_ORDER:
            errs.append(f"{k['id']}: bad grade {k['grade']}")
        if k["type"] not in valid_types:
            errs.append(f"{k['id']}: bad type {k['type']}")
        if not k["acc"]:
            errs.append(f"{k['id']}: no ACC tag (ACC-anchoring required)")
        for a in k["acc"]:
            if a not in ACC_CODES:
                errs.append(f"{k['id']}: ACC tag {a} not in the ACC spine")
        if not (k["ccss"] or k["teks"]):
            errs.append(f"{k['id']}: no CCSS/TEKS subset tag")

    # 2. every ACC-core code with need='hs' is carried by >=1 KC (the common-standard coverage guarantee)
    kc_acc = {a for k in HS_KCS for a in k["acc"]}
    for a in ACC_SPINE:
        if a["need"] == "hs" and a["code"] not in kc_acc:
            errs.append(f"ACC {a['code']} needs an HS KC but none carries it")
    # ...and no NON-WOVEN HS KC carries an ACC code marked external/descoped (no scope leak).
    # 'woven' KCs APPLY an externally-owned standard inside writing (e.g. voice applies CONV.3 style);
    # they do not OWN it, so they may reference an external ACC code. Taught KCs may not.
    ext_desc = {a["code"] for a in ACC_SPINE if a["need"] != "hs"}
    for k in HS_KCS:
        if k["type"] == "woven":
            continue
        for a in k["acc"]:
            if a in ext_desc:
                errs.append(f"{k['id']} (taught) carries {a} which is externally-owned/descoped (scope leak)")

    # 3. DAG: acyclic + forward-only across grades + all nodes real
    try:
        order = topo_order()
    except ValueError as e:
        errs.append(str(e)); order = []
    for u, vs in PREREQ_DAG.items():
        if u not in KC_BY_ID:
            errs.append(f"DAG source {u} is not a KC")
        for v in vs:
            if v not in KC_BY_ID:
                errs.append(f"DAG target {v} is not a KC")
            elif GRADE_ORDER[KC_BY_ID[v]["grade"]] < GRADE_ORDER[KC_BY_ID[u]["grade"]]:
                errs.append(f"DAG edge {u}->{v} goes backward across grades")

    # 4. UNITS: every unit KC exists; every KC appears in exactly one unit; gateway KC is in its unit;
    #    each grade has exactly one course gate; unit order respects the DAG (a KC's prereqs are taught no later)
    seen_kc = {}
    for grade, units in UNITS.items():
        gates = 0
        pos = {}  # kc_id -> global sequence index within grade-ordered units
        for ui, u in enumerate(units):
            for kc in u["kcs"]:
                if kc not in KC_BY_ID:
                    errs.append(f"{u['id']}: unknown KC {kc}")
                elif KC_BY_ID[kc]["grade"] != grade:
                    errs.append(f"{u['id']}: KC {kc} is {KC_BY_ID[kc]['grade']}, not {grade}")
                seen_kc[kc] = seen_kc.get(kc, 0) + 1
                pos[kc] = ui
            if u["gateway"] and u["gateway"] not in u["kcs"]:
                errs.append(f"{u['id']}: gateway {u['gateway']} not in its unit's KCs")
            if u["course_gate"]:
                gates += 1
        if gates != 1:
            errs.append(f"{grade}: expected exactly 1 course gate, found {gates}")
    for k in HS_KCS:
        c = seen_kc.get(k["id"], 0)
        if c != 1:
            errs.append(f"{k['id']}: appears in {c} units (must be exactly 1)")

    # 5. within-grade unit ordering respects the DAG: if A->B and both same grade, A's unit <= B's unit
    unit_index = {}
    for grade, units in UNITS.items():
        for ui, u in enumerate(units):
            for kc in u["kcs"]:
                unit_index[kc] = (GRADE_ORDER[grade], ui)
    for u, vs in PREREQ_DAG.items():
        for v in vs:
            if u in unit_index and v in unit_index and unit_index[u] > unit_index[v]:
                errs.append(f"unit ordering violates DAG: {u} (prereq) is after {v}")

    # 6. every KC's funnel is either an HS-owned tested capability or... (funnels must not be external/descoped keys)
    for k in HS_KCS:
        if k["funnel"] in EXTERNAL_OWNED or k["funnel"] in DESCOPED:
            errs.append(f"{k['id']} funnel '{k['funnel']}' collides with an external/descoped key")

    # ---- report ----
    if errs:
        print("course_sequence_g9_12 self-test FAIL:")
        for e in errs:
            print("  -", e)
        sys.exit(1)
    print("course_sequence_g9_12 self-test PASS")
    print(f"  ACC spine: {len(ACC_SPINE)} codes ({sum(1 for a in ACC_SPINE if a['need']=='hs')} hs / "
          f"{sum(1 for a in ACC_SPINE if a['need']=='external')} external / "
          f"{sum(1 for a in ACC_SPINE if a['need']=='descoped')} descoped)")
    print(f"  HS KCs: {len(HS_KCS)} | units: {sum(len(v) for v in UNITS.values())} across "
          f"{len(UNITS)} grades | DAG edges: {sum(len(v) for v in PREREQ_DAG.values())}")
    print(f"  teach order (topo): {' -> '.join(order)}")
    sys.exit(0)
