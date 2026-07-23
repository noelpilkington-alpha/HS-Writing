"""
lesson_contract.py  -  The enforceable contract + QC harness for the G10 LESSON generator.

Third contract in the pipeline, mirroring stimulus_contract.py and item_contract.py.

WHAT A LESSON IS (per Timeback_Feasibility.md + G10_Model_Lesson_Specs.md):
A lesson is a Timeback assessment-TEST = an ORDERED SEQUENCE OF ITEMS following the SRSD shell
(Teach -> Model -> Supported -> Independent -> Transfer). It ASSEMBLES existing bank artifacts
(stimuli by id, SR/CR items by id) and AUTHORS the connective slots that are not standalone bank items
(teach cards, the clean annotated before/after worked example, predict-the-fix pairs, calibration
self-scores, student-diagnosis prompts).

WHY MACHINE-ENFORCED: a skill-pack reproduces its model lesson at scale. If the shell is malformed the
generator scales the flaw. So the council's rulings are encoded here as gates that REJECT, not as prose
a model claims to have followed. Everything that can't be checked mechanically is labeled, never trusted.

Gates: shell_completeness, model_sequence (modality-corrected 4-mechanism), discrimination_before_production
(Grade-C, LABELED), binding_integrity (refs exist in the banks), bank_partition (DI transfer),
calibration_discipline (judge-then-reveal; no person-praise), grader_routing (rc.* config), timeback_native
(supported qti types), effect_size_honesty (standing rule), mnemonic_status, no_em_dash.

Dependency-free (stdlib only; scans the sibling bank dirs for id existence).
"""
from __future__ import annotations
import re, os, sys, glob
import importlib.util
from dataclasses import dataclass, field
from typing import Literal

HERE = os.path.dirname(__file__)
STIMULUS_DIR = os.path.join(HERE, "..", "Stimulus_Bank_G10")
ITEM_DIR = os.path.join(HERE, "..", "Item_Bank_G10")

# ---- vocab -----------------------------------------------------------------
Role = Literal["TEACH", "MODEL", "SUPPORTED", "INDEPENDENT", "TRANSFER"]
SHELL_ORDER = ["TEACH", "MODEL", "SUPPORTED", "INDEPENDENT", "TRANSFER"]

# slot kinds and the Timeback interaction each renders as
KIND_QTI = {
    "stimulus_display":       "stimulus",        # native HTML display
    "teach_card":             "stimulus",        # native HTML display (authored teaching content)
    "annotated_before_after": "stimulus",        # native HTML display (MODEL mechanism 1)
    "discrimination":         "choice",          # choice/match/order (Grade-C move)
    "predict_the_fix":        "choice",          # choice + feedback-block (MODEL mechanism 2)
    "self_score":             "choice",          # calibration: student predicts THEN reveal
    "production_frq":         "extended-text",   # + ExternalApiScore -> grader (mechanism 3: feedback on OWN draft)
    "diagnosis_frq":          "extended-text",   # + grader (MODEL mechanism 4: student-generated diagnosis)
    "sr_practice":            "choice",          # bound SR item used as Supported/Independent practice
}
NATIVE_JSON_SAFE = {"choice", "extended-text", "order", "text-entry"}       # JSON POST safe
NATIVE_XML_REQUIRED = {"inline-choice", "hottext", "match"}                 # XML POST required (still native)
RUBRIC_CONFIGS = {"rc.staar", "rc.sbac", "rc.mcas", "rc.ohio", "rc.4trait", "rc.ap"}
# ^ rc.sbac added 2026-07-21 (G9/10 CCSS scorer, bake-off winner) to reconcile drift with the grader.

# GRADING REGENERATION CONTRACT (design: grader repo CCSS_G910/Grading_Regeneration_Contract_DESIGN.md).
# A scored production_frq declares (unit, frq_type, rubric_ref); the grader routes off (unit, frq_type).
# frq_type = the CONSTRUCT: revision (transform a provided draft) | writing (produce from a task).
FRQ_TYPES = {"revision", "writing"}
# rc.4trait (G11/G12 Regents) TASK PROFILE the wirer bakes into the grader URL (?mode=). Orthogonal to the
# (unit, frq_type) grain routing above. "" = the grader's rc.4trait default (argument); analysis is explicit.
MODES = {"argument", "analysis"}
# Thin CAPABILITY MIRROR of the grader's SUPPORTED (grader/engine/routing.py is the source of truth).
# "unit:frq_type" strings the deployed grader accepts. A drift test (pipeline/tests) asserts this equals the
# grader's capability_manifest()['supported']; if the grader adds/removes a combo, the test fails until synced.
GRADER_SUPPORTED_TUPLES = {
    "sentence:revision", "sentence:writing",
    "paragraph:revision", "paragraph:writing",
    "multi_paragraph:revision", "multi_paragraph:writing",
    "essay:revision", "essay:writing",
}

# the 8 reusable types (G10_Model_Lesson_Specs.md) + their mnemonic + status
LESSON_TYPES = {
    1: ("source-reading",       "MARK",  "proposal"),
    2: ("claim-building",       "STAND", "proposal"),
    3: ("evidence-integration", "PROVE", "established-caveat"),  # unverified-shipped K-8; verify before reuse
    4: ("text-dependent-analysis", "DEW", "proposal"),
    5: ("rubric-revision",      "CHECK", "proposal"),
    6: ("editing-in-context",   "SPOT",  "proposal"),
    7: ("essay-assembly",       "BUILD", "proposal"),
    8: ("cross-source-synthesis", "WEAVE", "proposal"),
}

# ---- council cadence tiers (LS feedback 2026-07) ---------------------------
# Archetype is DERIVED from lesson_type (no new lesson field). Cadence ceiling = max run of counted
# teach segments allowed before an intervening check. Type 4 (DEW) = text-dependent-analysis, a
# concept-teaching move (device -> effect -> warrant). Unknown types default to concept (tightest ceiling).
CADENCE_CEILING = {"concept": 3, "checking_revision": 2, "full_essay_build": 4}
MEMORIZABLE_TOOL_CEILING = 2
_ARCHETYPE_BY_TYPE = {1: "concept", 2: "concept", 3: "concept", 4: "concept", 6: "concept",
                      5: "checking_revision", 7: "full_essay_build", 8: "full_essay_build"}
def archetype_of(L) -> str:
    """Council cadence tier from lesson_type. Type 4 = DEW text-dependent-analysis (concept-teaching).
    Unknown types default to concept (the tightest ceiling, safest for novices)."""
    return _ARCHETYPE_BY_TYPE.get(getattr(L, "lesson_type", 0), "concept")

# Unit-of-production ladder (TWR Principle 2: begin at the sentence, then build to paragraphs, then
# compositions; "a writer who cannot compose a decent sentence will never produce a decent essay",
# TWR2.0 loc ~1343-1395). KH element-interactivity: do not compose the whole before the parts are fluent
# (HLH Ch.17 blank-page fails novices; KB 00 §1.1/§1.2). The SPO explicitly scales sentence->paragraph->
# multi-paragraph (TWR2.0 Ch.6). This is the settled developmental axis; ordered low->high.
UNIT_LADDER = ["sentence", "paragraph", "multi_paragraph", "essay"]
UNIT_RANK = {u: i for i, u in enumerate(UNIT_LADDER)}


def grain(L) -> str:
    """The lesson's grain = the highest unit-ladder rank among its scored production_frq slots.
    Falls back to 'sentence' if no scored production exists. (Spine re-architecture: the spine density is
    keyed on grain, derived from the terminal production unit, not the lesson title.)"""
    units = [s.unit for s in L.slots if s.kind == "production_frq" and getattr(s, "unit", "")]
    if not units:
        return "sentence"
    return max(units, key=lambda u: UNIT_RANK.get(u, 0))


# Required slot shape per (class, grain), from SPINE_DELIBERATION_verdict.md. gate is class-level
# (grain-independent). "revision_or_coached_transfer": paragraph grain and above pass with EITHER an own-draft
# diagnosis_frq OR exactly one coached (feedback-bearing) TRANSFER write, never both. multi_paragraph is treated
# as paragraph-family (verdict language "paragraph grain and above"); it is a documented interpolation.
GRAIN_TEMPLATES = {
    "gate": {
        "banned_kinds": {"annotated_before_after", "discrimination", "predict_the_fix"},
        "require_kinds": {"production_frq"},   # >=1 cold write
        # the plan (a SUPPORTED production_frq) must be scored=False; every SCORED write must be a cold
        # INDEPENDENT/TRANSFER production. This allows a single-essay gate (1 cold write) AND an AP FRQ-section
        # gate (e.g. G12: synthesis + rhetorical analysis + argument = 3 cold writes) without letting a scored
        # plan re-introduce construct-irrelevant variance.
        "no_scored_plan": True,
    },
    ("practice", "sentence"): {"discrimination_min": 2, "production_writes": (2, 3)},
    ("practice", "paragraph"): {"discrimination_min": 1, "production_writes": (2, 3), "revision_or_coached_transfer": True},
    ("practice", "multi_paragraph"): {"discrimination_min": 1, "production_writes": (1, 3), "revision_or_coached_transfer": True},
    ("practice", "essay"): {"discrimination_max": 1, "production_writes": (1, 1), "revision_or_coached_transfer": True,
                            "no_transfer_write": True},
}

@dataclass
class Slot:
    role: Role
    kind: str
    title: str
    ref: str = ""            # a stimulus_id or item_id it binds to ("" for authored connective slots)
    body: str = ""           # authored HTML/text (teach cards, annotations, prompts) - own-authored
    feedback: str = ""       # predict-the-fix reveal (feedback-block, ~1000 char limit)
    rubric_ref: str = ""     # production_frq only: an rc.* config
    bank: str = ""           # content-bank/topic slug (for DI bank-partition on TRANSFER)
    scored: bool = False
    labeled_grade_c: bool = False  # discrimination slots must be LABELED a design bet
    unit: str = ""           # production slots: the UNIT of production written here.
                             # "" = not a sized production; else one of UNIT_LADDER (sentence..essay).
                             # Enforces the TWR sentence->paragraph->composition scaffold (see gates below).
    frq_type: str = ""       # scored production_frq only: the grading CONSTRUCT, one of FRQ_TYPES.
                             # "revision" = transform a PROVIDED draft; "writing" = produce from a task.
                             # With `unit`, forms the (unit, frq_type) tuple the grader routes off (regeneration
                             # contract). REQUIRED for scored sentence/paragraph; essays default to "writing".
    mode: str = ""           # scored production_frq only, rc.4trait (G11/G12 Regents): the TASK PROFILE, one of
                             # MODES. "argument" (each criterion 0-6, total 24) | "analysis" (each 0-4, total 16).
                             # Orthogonal to grain routing; baked into the grader URL by the wirer (?mode=).
                             # Empty -> the grader defaults rc.4trait to "argument", so ONLY analysis tasks
                             # (rhetorical/literary analysis essays) must declare mode="analysis".
    choices: list = field(default_factory=list)   # OPTIONAL explicit MCQ options for discrimination/predict:
                             # [{"id":"A","text":"...","correct":bool,"why":"why this option is right/wrong"}].
                             # When present, the renderer uses these directly (reliable per-choice feedback)
                             # instead of parsing options+reveal out of the body prose.
    tag: str = ""            # "" | "buy_in" | "memorizable_tool" | "worked_example"; cadence-gate hints
                             # (buy_in counts 0; memorizable_tool tightens the ceiling)

@dataclass
class Lesson:
    id: str
    grade: str               # "9-10"
    lesson_type: int         # 1..8
    unit: str                # which G10 unit this instantiates
    title: str
    target: str
    acc_tags: list[str] = field(default_factory=list)
    slots: list[Slot] = field(default_factory=list)
    fade_ledger_moves: list[str] = field(default_factory=list)
    provenance: dict = field(default_factory=dict)
    qc: dict = field(default_factory=dict)
    # PP100 MASTERY task (held-out, task-specific): {"source": "<held-out stimulus id>", "prompt_html": "<the
    # task-specific mastery instruction, authored to this lesson's skill, referencing the held-out source>",
    # "unit": "<sentence|paragraph|multi_paragraph|essay>", "rubric_ref": "rc.*"}. The mastery pusher renders
    # this (source block + prompt_html) instead of reusing the in-lesson INDEPENDENT write, so mastery is a
    # genuinely fresh, task-specific cold assessment. Empty -> pusher falls back to the held-out generic path.
    mastery: dict = field(default_factory=dict)
    # lesson CLASS: "practice" (the default teaching lesson, full grain-differentiated arc) or "gate" (a unit
    # certification: scaffold-free cold write, per the spine re-architecture verdict). Class-aware gates below
    # relax the SRSD-arc / model-sequence / discrimination-before-production checks for gate lessons.
    lesson_class: str = "practice"

# ---- bank id index (scan once) --------------------------------------------

def _bank_ids() -> set[str]:
    ids: set[str] = set()
    # scan ALL grade stimulus banks (G9-G12) + item dir + HERE - NOT just STIMULUS_DIR (=G10). G9/G11/G12
    # lessons bind refs from their own grade's Stimulus_Bank_*; a G10-only scan false-fails binding_integrity
    # on every other grade (regression seen 2026-07-13 when lesson_contract was reverted to a G10-only version).
    dirs = [ITEM_DIR, os.path.join(HERE)]
    for g in ("G9", "G10", "G11", "G12"):
        dirs.append(os.path.join(HERE, "..", f"Stimulus_Bank_{g}"))
        dirs.append(os.path.join(HERE, "..", f"Item_Bank_{g}"))  # scan every grade's item bank, not just G10
    seen = set()
    for d in dirs:
        for f in glob.glob(os.path.join(d, "*.py")):
            if f in seen:
                continue
            seen.add(f)
            try:
                src = open(f, encoding="utf-8").read()
            except Exception:
                continue
            # ANY literal full id token "ACC-W<band>-<FAMILY>-NNNN" (band 910 or 1112). Catches id="..." AND
            # ids passed positionally to helper builders (mk(...), scr(...)) that an id="..."-only regex misses.
            ids.update(re.findall(r'"(ACC-W(?:910|1112)-[A-Z0-9\-]+-\d{4})"', src))
            # bare literal id="..." with NO trailing 4-digit block - e.g. FRAME stimuli ACC-W910-FRAME-PHONEBAN.
            ids.update(re.findall(r'\bid\s*=\s*"(ACC-W(?:910|1112)-[A-Z0-9\-]+)"', src))
            # frame/stimulus records may set the id via other attrs (id=, sourced ids in rec builders):
            ids.update(re.findall(r'"(ACC-W(?:910|1112)-FRAME-[A-Z0-9\-]+)"', src))
            # programmatic ids: id=f"ACC-W910-SR-ORG-{idnum:04d}" cannot be read by a source regex, so
            # EXECUTE the module and collect the CONCRETE .id of every generated item. This closes the
            # family-wildcard fail-open (a bogus -9999 that was never generated no longer resolves). The
            # "-*" wildcard is registered only as a fallback when exec fails, so an unloadable bank never
            # silently blocks binding; that fallback path is the one place a bogus number can still pass.
            # Only actual item-bank modules generate SR ids programmatically. Exclude the pipeline's own
            # files (this module contains the pattern in comments), which would exec-fail and wrongly
            # trigger the permissive wildcard fallback.
            in_item_bank = os.sep + "Item_Bank_" in os.path.abspath(f)
            if in_item_bank and re.search(r'\bid\s*=\s*f"ACC-W(?:910|1112)-SR-[A-Z]+-\{', src):
                loaded = _concrete_ids_from_module(f)
                if loaded:
                    ids.update(loaded)
                else:
                    for pre in re.findall(r'\bid\s*=\s*f"(ACC-W(?:910|1112)-SR-[A-Z]+)-\{', src):
                        ids.add(pre + "-*")   # fallback: exec failed, keep the old permissive behavior
    return ids


def _concrete_ids_from_module(path: str) -> set[str]:
    """Execute an item-bank module and return the concrete .id of every item it generates.
    Item banks expose an ITEMS list of records with an .id attribute (see Item_Bank_*/sr_*.py)."""
    out: set[str] = set()
    try:
        name = "ib_" + os.path.basename(path)[:-3].replace(".", "_")
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except SystemExit:
        mod = None
    except Exception:
        return out
    for attr in ("ITEMS", "LESSONS", "RECORDS"):
        for obj in getattr(mod, attr, []) or []:
            rid = getattr(obj, "id", None)
            if isinstance(rid, str) and rid.startswith("ACC-W"):
                out.add(rid)
    return out

_BANK = None
def bank_ids() -> set[str]:
    global _BANK
    if _BANK is None:
        _BANK = _bank_ids()
    return _BANK

def _ref_exists(ref: str) -> bool:
    ids = bank_ids()
    if ref in ids:
        return True
    # programmatic family match: SR item like ACC-W910-SR-ORG-0007 matches family ACC-W910-SR-ORG-*
    m = re.match(r"(ACC-W910-SR-[A-Z]+)-\d{4}$", ref)
    if m and (m.group(1) + "-*") in ids:
        return True
    return False

# ---- gates -----------------------------------------------------------------

def gate_shell_completeness(L: Lesson) -> tuple[bool, str]:
    roles = [s.role for s in L.slots]
    if getattr(L, "lesson_class", "practice") == "gate":
        # a gate is the Independent-Performance endpoint: a cue + a cold TRANSFER write. No full SRSD arc.
        missing = {"TEACH", "TRANSFER"} - set(roles)
        if missing:
            return False, f"gate missing {missing} (needs a cue + a cold TRANSFER write)"
        return True, "gate shell (cue + cold write) present"
    # essay-grain practice lessons route TRANSFER out to the gate/PP100 (verdict), so the in-article shell
    # ends at INDEPENDENT. Require the first four stages; TRANSFER is not expected at essay grain.
    required = list(SHELL_ORDER)
    if getattr(L, "lesson_class", "practice") == "practice" and grain(L) == "essay":
        required = [r for r in SHELL_ORDER if r != "TRANSFER"]
    for r in required:
        if r not in roles:
            return False, f"SRSD shell incomplete: missing '{r}' stage"
    # shell stages must appear in order (first occurrence of each required role is monotonic increasing)
    firsts = [roles.index(r) for r in required]
    if firsts != sorted(firsts):
        return False, f"shell stages out of order: {[(r, roles.index(r)) for r in required]}"
    tail = "" if "TRANSFER" in required else " (essay grain: transfer routed to gate/PP100)"
    return True, "SRSD shell complete + in order" + tail

def gate_model_sequence(L: Lesson) -> tuple[bool, str]:
    """Modality-corrected Model slot: clean annotated before/after -> predict-the-fix (mechanisms 1-2 in
    MODEL), plus a student-generated diagnosis somewhere in the lesson (mechanism 4). Mechanism 3 (feedback
    on the student's OWN draft) is the production_frq's grader feedback. NO passive-read messy think-aloud.
    Gate lessons are scaffold-free by design (verdict) -> exempt. The diagnosis (mechanism 4) is required only
    at paragraph grain and above, and a coached (feedback-bearing) TRANSFER write satisfies it as an
    alternative (paragraph transfer-flagged lessons); at sentence grain it folds into predict-the-fix."""
    if getattr(L, "lesson_class", "practice") == "gate":
        return True, "gate: model sequence not required (scaffold-free by design)"
    model = [s for s in L.slots if s.role == "MODEL"]
    kinds = {s.kind for s in model}
    if "annotated_before_after" not in kinds:
        return False, "MODEL missing the clean annotated before/after (mechanism 1: unambiguous worked example)"
    if "predict_the_fix" not in kinds:
        return False, "MODEL missing predict-the-fix (mechanism 2: student diagnoses BEFORE the reveal)"
    rank = UNIT_RANK.get(grain(L), 0)
    needs_revision = rank >= UNIT_RANK["paragraph"]
    has_diag = any(s.kind == "diagnosis_frq" for s in L.slots)
    has_coached_transfer = any(s.kind == "production_frq" and s.role == "TRANSFER" and s.feedback.strip()
                               for s in L.slots)
    if needs_revision and not (has_diag or has_coached_transfer):
        return False, ("paragraph grain or above needs EITHER an own-draft diagnosis_frq OR one coached "
                       "(feedback-bearing) TRANSFER write (mechanism 4)")
    # predict-the-fix must carry a reveal (feedback-block)
    for s in model:
        if s.kind == "predict_the_fix" and not s.feedback.strip():
            return False, "predict-the-fix has no feedback reveal (feedback-block)"
    return True, "Model = mechanisms 1-2 (before/after + predict-the-fix) + grain-appropriate diagnosis"

def gate_discrimination_before_production(L: Lesson) -> tuple[bool, str]:
    """Grade-C move, LABELED as a design bet. A discrimination slot must appear before any production FRQ.
    Gate lessons are scaffold-free (verdict) -> discrimination intentionally absent -> exempt."""
    if getattr(L, "lesson_class", "practice") == "gate":
        return True, "gate: discrimination intentionally absent (scaffold-free)"
    disc_idx = [i for i, s in enumerate(L.slots) if s.kind == "discrimination"]
    prod_idx = [i for i, s in enumerate(L.slots) if s.kind in ("production_frq", "diagnosis_frq")]
    if not disc_idx:
        return False, "no discrimination slot (the Grade-C discriminate-before-produce move is required)"
    if prod_idx and min(disc_idx) > min(prod_idx):
        return False, "production appears before any discrimination (violates discriminate-before-produce)"
    # EVERY discrimination slot must be LABELED a design bet (Grade C), not sold as evidence. (Hardened from
    # any()->all() 2026-07-15: the spine re-architecture added a 2nd discrimination to sentence-grain lessons,
    # and any() let an unlabeled slot ride on a labeled sibling - a real fail-open the checker corpus caught.)
    unlabeled = [i for i, s in enumerate(L.slots) if s.kind == "discrimination" and not s.labeled_grade_c]
    if unlabeled:
        return False, (f"discrimination slot(s) {unlabeled} not labeled_grade_c=True (every Grade-C design bet "
                       f"must be labeled, not just one)")
    return True, "discrimination precedes production; every Grade-C move labeled"

def gate_diagnosis_after_write(L: Lesson) -> tuple[bool, str]:
    """PHANTOM-DRAFT ORDERING: a diagnosis_frq that tells the student to reread "the essay you just
    wrote" / run a checklist on "YOUR draft" must appear AFTER the INDEPENDENT production write, not
    before it - otherwise the student is told to check an essay that does not exist yet.

    WHY (this session): the one-write re-architecture (084ff7e) reworded the essay-grain diagnosis to
    "Reread the essay you just wrote..." but left the diagnosis slot POSITIONED BEFORE the independent
    write in 25 lessons - a defect that slipped past all 24 contract gates + the 4 new gates and only
    the readiness audit caught. This closes the hole deterministically.

    CONSERVATIVE (avoids the documented over-flag mode): fires ONLY when the diagnosis body actually
    references an already-written draft (the signature phrases). A diagnosis that checks "your PLAN
    before you draft" (a legitimate coping-model / plan-check, e.g. G11 L31) does NOT reference a
    written essay, so it is not flagged even when it precedes the write - that ordering is correct."""
    _WRITTEN_DRAFT_SIGNATURES = ("you just wrote", "reread the essay", "essay you wrote",
                                 "draft you just wrote", "reread your essay", "reread your draft")
    indep_idx = [i for i, s in enumerate(L.slots)
                 if s.kind == "production_frq" and s.role in ("INDEPENDENT", "TRANSFER")]
    if not indep_idx:
        return True, "no independent/transfer write (n/a)"
    # The diagnosis must follow SOME write it could be rereading, i.e. at least the FIRST such write.
    # (Using min, not max: a diagnosis that correctly trails the INDEPENDENT write is fine even if a
    # separate later TRANSFER write on a NEW source follows it - it reads the draft the student already
    # produced, not the not-yet-written transfer.)
    first_write = min(indep_idx)
    offenders = []
    for i, s in enumerate(L.slots):
        if s.kind != "diagnosis_frq":
            continue
        body = (getattr(s, "body", "") or "").lower()
        refers_to_written = any(sig in body for sig in _WRITTEN_DRAFT_SIGNATURES)
        if refers_to_written and i < first_write:
            offenders.append(i)
    if offenders:
        return False, (f"diagnosis_frq slot(s) {offenders} tell the student to reread 'the essay you just "
                       f"wrote' but appear BEFORE any independent write (first write at slot {first_write}): a "
                       f"phantom-draft check on an essay that does not exist yet. Move the diagnosis AFTER the write.")
    return True, "any own-draft diagnosis runs after the independent write"

def gate_binding_integrity(L: Lesson) -> tuple[bool, str]:
    """Every ref (stimulus_id / item_id) must exist in the banks. Authored slots (ref='') are exempt."""
    missing = []
    n_bound = 0
    for s in L.slots:
        if s.ref.strip():
            n_bound += 1
            if not _ref_exists(s.ref):
                missing.append(f"{s.role}/{s.kind}:{s.ref}")
    if missing:
        return False, f"refs not found in banks: {missing[:6]}"
    if n_bound == 0:
        return False, "lesson binds to NO bank artifacts (must reference >=1 real stimulus/item)"
    return True, f"{n_bound} bound refs, all present in the banks"

def gate_bank_partition(L: Lesson) -> tuple[bool, str]:
    """DI hard bank-partition: the TRANSFER slot's content bank must DIFFER from every taught
    (MODEL/SUPPORTED) content bank, so transfer is genuine, not recall of the same material."""
    # gates ARE the cold transfer on a held-out source; the plan + cold write share that held-out bank by
    # design, so bank-partition does not apply. Exempt gates outright.
    if getattr(L, "lesson_class", "practice") == "gate":
        return True, "gate: the cold write IS the transfer (partition n/a)"
    taught = {s.bank for s in L.slots if s.role in ("MODEL", "SUPPORTED") and s.bank}
    transfer = [s for s in L.slots if s.role == "TRANSFER"]
    if not transfer:
        # essay-grain practice lessons route transfer to the gate + PP100 (verdict), so no in-article
        # TRANSFER slot is expected -> exempt.
        if getattr(L, "lesson_class", "practice") == "practice" and grain(L) == "essay":
            return True, "essay grain: in-article transfer routed to gate/PP100 (no TRANSFER slot expected)"
        return False, "no TRANSFER slot"
    tbanks = {s.bank for s in transfer if s.bank}
    if not tbanks:
        return False, "TRANSFER slot has no content-bank tag (cannot verify partition)"
    overlap = tbanks & taught
    if overlap:
        return False, f"TRANSFER reuses a taught content bank {overlap} (no partition; not real transfer)"
    return True, f"transfer bank {tbanks} partitioned from taught {taught or '{}'}"

def gate_calibration_discipline(L: Lesson) -> tuple[bool, str]:
    """Judge-then-reveal: any self_score slot must PRECEDE a production/grader reveal (predict THEN reveal).
    KILL-list: never 'hand rubric + grade yourself'; ban person-praise. (W&H: overestimate bias g=0.206.)
    EXCEPTION (gate lessons): the verdict places the gate's self_score AFTER the cold write as post-hoc
    calibration (train the student to judge their own finished work against the rubric), so the predict-then-
    reveal ordering does not apply to gates."""
    ss_idx = [i for i, s in enumerate(L.slots) if s.kind == "self_score"]
    prod_idx = [i for i, s in enumerate(L.slots) if s.kind in ("production_frq", "diagnosis_frq")]
    scored_prod_idx = [i for i, s in enumerate(L.slots)
                       if s.kind in ("production_frq", "diagnosis_frq") and getattr(s, "scored", False)]
    if getattr(L, "lesson_class", "practice") != "gate":
        for i in ss_idx:
            # valid EITHER as predict-then-reveal (a production follows) OR as post-hoc calibration on a
            # scored write that PRECEDES it (the external grader reveals the truth on that write's submission).
            follows_scored_write = any(j < i for j in scored_prod_idx)
            if not any(j > i for j in prod_idx) and not follows_scored_write:
                return False, "a self_score has no graded reveal (predict THEN reveal, or score a preceding graded write)"
    # ban person-praise in authored bodies/feedback (praise ~0.12; kill-list)
    praise = re.compile(r"\b(great job|good job|you'?re so smart|nice work|well done|you'?re a natural)\b", re.I)
    for s in L.slots:
        blob = f"{s.body} {s.feedback}"
        if praise.search(blob):
            return False, f"person-praise in {s.role}/{s.kind} (kill-list: praise ES ~0.12; use GOAL/NOW/NEXT)"
    return True, ("calibration: self-score precedes reveal; no person-praise" if ss_idx
                  else "no self_score slot (n/a); no person-praise")

def gate_grader_routing(L: Lesson) -> tuple[bool, str]:
    """Every SCORED production_frq must declare a grading tuple the deployed grader can route + score.

    REGENERATION CONTRACT: grading routes off the DECLARED (unit, frq_type, rubric_ref) tuple, never off
    content. This gate is the futureproofing lever — a regenerated/authored lesson whose declared tuple the
    grader can't grade FAILS HERE (at authoring, via tier_a_regression), not silently at grade time. Checks:
      - rubric_ref in RUBRIC_CONFIGS (the standard family the grader implements)
      - unit in UNIT_LADDER
      - frq_type in FRQ_TYPES, REQUIRED for scored sentence/paragraph (load-bearing there; essays default writing)
      - (unit:frq_type) in GRADER_SUPPORTED_TUPLES (the grader's mirrored capability set)
    Unscored production_frq (e.g. a SUPPORTED plan) only needs a valid rubric_ref (it isn't graded).
    """
    prods = [s for s in L.slots if s.kind == "production_frq"]
    if not prods:
        return False, "no production_frq slot (a lesson must reach production)"
    for s in prods:
        if s.rubric_ref not in RUBRIC_CONFIGS:
            return False, f"production_frq '{s.title[:30]}' rubric_ref '{s.rubric_ref}' not in {RUBRIC_CONFIGS}"
        if not getattr(s, "scored", False):
            continue  # unscored (plan/scaffold) — not graded, tuple not required
        unit = getattr(s, "unit", "") or ""
        if unit and unit not in UNIT_RANK:
            return False, f"production_frq '{s.title[:30]}' unit '{unit}' not in {UNIT_LADDER}"
        frq_type = getattr(s, "frq_type", "") or ""
        # sentence/paragraph MUST declare the construct; essay/multi_paragraph may default to "writing".
        if unit in ("sentence", "paragraph") and frq_type not in FRQ_TYPES:
            return False, (f"scored production_frq '{s.title[:30]}' (unit={unit}) must declare frq_type "
                           f"in {sorted(FRQ_TYPES)} (regeneration contract); got '{frq_type}'")
        eff_type = frq_type or "writing"
        tuple_key = f"{unit or 'essay'}:{eff_type}"
        if tuple_key not in GRADER_SUPPORTED_TUPLES:
            return False, (f"scored production_frq '{s.title[:30]}' declares ({tuple_key}) which the grader "
                           f"does not support; accepts {sorted(GRADER_SUPPORTED_TUPLES)}")
        # mode (rc.4trait TASK PROFILE) is optional; if declared it must be valid, and it only means anything
        # for rc.4trait (the argument/analysis scale switch). A stray mode on another rubric is a design error.
        mode = getattr(s, "mode", "") or ""
        if mode:
            if mode not in MODES:
                return False, (f"scored production_frq '{s.title[:30]}' mode '{mode}' not in {sorted(MODES)}")
            if s.rubric_ref != "rc.4trait":
                return False, (f"scored production_frq '{s.title[:30]}' declares mode '{mode}' but rubric_ref "
                               f"is '{s.rubric_ref}' (mode only applies to rc.4trait)")
    scored = [s for s in prods if getattr(s, "scored", False)]
    return True, f"{len(prods)} production FRQ(s) ({len(scored)} scored); all tuples routable to the grader"

def gate_timeback_native(L: Lesson) -> tuple[bool, str]:
    """Every slot's interaction must be a supported Timeback type. Flag which need XML POST."""
    xml = set()
    for s in L.slots:
        qti = KIND_QTI.get(s.kind)
        if qti is None:
            return False, f"slot kind '{s.kind}' has no Timeback interaction mapping"
        if qti in NATIVE_XML_REQUIRED:
            xml.add(qti)
        elif qti not in NATIVE_JSON_SAFE and qti != "stimulus":
            return False, f"slot kind '{s.kind}' -> '{qti}' is not Timeback-native"
    note = f" (XML POST required for: {sorted(xml)})" if xml else " (all JSON-safe)"
    return True, "all slots map to native Timeback interactions" + note

def gate_effect_size_honesty(L: Lesson) -> tuple[bool, str]:
    """Standing rule: no slot may claim SRSD's live-enacted effect size (ES 1.14 / 1.02) for the async model,
    nor say the Model 'inherits' SRSD's evidence. Async adaptations cite modality-flexible mechanisms only."""
    bad = re.compile(r"(ES\s*1\.(14|02)|effect size of 1\.(14|02)|inherits? SRSD'?s? (evidence|effect))", re.I)
    for s in L.slots:
        if bad.search(f"{s.body} {s.feedback} {s.title}"):
            return False, f"{s.role}/{s.kind} claims SRSD's ES for the async model (violates effect-size-honesty rule)"
    return True, "no over-claimed effect sizes (async model cites modality-flexible mechanisms only)"

# Timeback QTI reality (verified against the timeback skill references, 2026-07-08):
#  - A stimulus is DISPLAY-ONLY XHTML; JavaScript is stripped. A student CANNOT mark up / highlight /
#    annotate a passage. So no display/stimulus slot may instruct the student to mark the source.
#  - QTI items are STATELESS and ISOLATED: no item can show or reference a student's response to a prior
#    item (retake starts blank). So no slot may reference the student's own earlier work.
_MARKUP_VERBS = re.compile(
    r"\b(mark it up|mark up the|underline (?:the|each|one|any)|circle (?:the|each|every|one|any)|"
    r"highlight (?:the|each|any)|star (?:the|one|each)|annotate the (?:source|passage|text|article))\b", re.I)
_PRIOR_WORK = re.compile(
    r"\b(revise your|your (?:sentence|claim|paragraph|essay|draft|response|answer|version|plan|outline) "
    r"(?:from|you wrote|above|earlier)|look back at (?:your|what you)|the (?:sentence|paragraph|essay|claim) "
    r"you (?:wrote|created|made)|earlier you wrote|from step \d|your work from|revisit your)\b", re.I)

def gate_no_source_markup(L: Lesson) -> tuple[bool, str]:
    """Timeback stimuli are display-only (JS stripped): a student cannot mark up / highlight / annotate a
    passage. Flag mark-the-source imperatives on display slots (teach_card, stimulus_display,
    annotated_before_after). Author-written labels inside worked examples are fine; this targets instructions
    TO THE STUDENT to mark the source. Use 'read and note' framing, or a discrete hottext/choice item instead."""
    display_kinds = {"teach_card", "stimulus_display", "annotated_before_after"}
    for s in L.slots:
        if s.kind in display_kinds:
            m = _MARKUP_VERBS.search(s.body or "")
            if m:
                return False, (f"{s.role}/{s.kind} tells the student to mark up the source ('{m.group(0)}'); "
                               f"Timeback stimuli are display-only. Use read-and-note framing or a hottext/choice item.")
    return True, "no mark-up-the-source instructions on display slots"

def gate_no_prior_work_reference(L: Lesson) -> tuple[bool, str]:
    """QTI items are stateless/isolated: no item can show a student's response to a prior item. Flag slots
    that reference the student's own earlier work (e.g. 'revise your paragraph', 'your sentence from Step 5').
    Each production slot must be self-contained. Revision is taught via discrimination on PROVIDED pairs, not
    by asking the student to look back at their own submission (which they cannot see)."""
    for s in L.slots:
        blob = f"{s.body} {s.feedback}"
        m = _PRIOR_WORK.search(blob)
        if m:
            return False, (f"{s.role}/{s.kind} references the student's prior work ('{m.group(0)}'); QTI items "
                           f"are stateless (retake is blank). Make the slot self-contained (write fresh), not a look-back.")
    return True, "no cross-item references to the student's prior work"

# a fill-in frame = student-facing text with fill blanks; comma before a restrictive because/so clause in
# a FRAME reads as a punctuation model the student copies. Flag ", because"/", so" ONLY inside a frame
# (a chunk containing "______"), never in ordinary prose.
_FRAME_COMMA_RE = re.compile(r",\s+(because|so)\b", re.I)
def gate_frame_comma(L) -> tuple[bool, str]:
    hits = []
    for i, s in enumerate(L.slots, 1):
        body = s.body or ""
        if "______" not in body:            # only fill-in frames
            continue
        # scan each frame-ish sentence containing a blank
        for seg in re.split(r"(?<=[.!?])\s+", re.sub(r"<[^>]+>", " ", body)):
            if "______" in seg and _FRAME_COMMA_RE.search(seg):
                hits.append(f"slot {i}: '{seg.strip()[:60]}'")
    if hits:
        return False, "comma before 'because'/'so' in a fill-in frame (drop it): " + "; ".join(hits[:4])
    return True, "no frame punctuation-model errors"

_SELF_ANSWER_RE = re.compile(r"\?\s*(yes|no)[,\.\s]", re.I)
# own-turn signal = an independent student turn AFTER a coping-model demo. Recognizes "now write",
# "now rewrite" (the sanctioned coping-model turn: rewrite the provided weak draft), "now revise", and
# "now you [do work]" UNLESS it is the giveaway phrasing "now you have/'ve [the fixed version]"
# (possessing the answer, not doing the work).
_OWN_TURN_RE = re.compile(r"\b(now (?:(?:re)?write|revise|you\b(?!\s*(?:have|'ve)\b))|your own|a fresh|write and check)\b", re.I)
# A COPING-MODEL marker: pre-answered checks are OK only when they model the check on a supplied specimen
# and THEN hand the student their own turn, OR when the student runs the check on their OWN just-written
# draft (a self-check). Both are sanctioned; a bare "...No. Now rewrite it." with neither is a giveaway.
# Two structural signals cover every real bank pattern:
#   (a) "watch/run the check ON a <specimen>" demo -> "weak/provided/example <draft|paragraph|plan|map|
#       sentence|judgment|read|pool|version|claim>", "<specimen> to (fix|check)", "example:", "here is what".
#   (b) an OWN-draft self-check -> "your own draft", "the essay you just wrote", "reread your draft" (the
#       _WRITTEN_DRAFT_SIGNATURES vocabulary): the student IS answering the check, on their own writing.
_PROVIDED_DRAFT_RE = re.compile(
    r"\b(?:(?:weak|provided|example|this)\s+"
    r"(?:draft|paragraph|plan|map|sentence|judgment|read|pool|version|claim|essay|argument)"
    r"|(?:draft|paragraph|plan|map|read|judgment)\s+to\s+(?:fix|check)"
    r"|watch\s+(?:the\s+)?(?:check|precision pass|\w+\s+pass)\s+run"
    r"|here\s+is\s+what|example:\s|for example)\b", re.I)
_OWN_DRAFT_SELFCHECK_RE = re.compile(
    r"\b(your own draft|the essay you just wrote|essay you just wrote|reread (?:your|the) (?:draft|essay)"
    r"|run this checklist on your|check your own draft)\b", re.I)
def gate_self_answered_check(L) -> tuple[bool, str]:
    """#6: a diagnosis must make the student ANSWER the check, not read pre-answered ones. Pre-answered
    checks are OK ONLY as a coping-model demo: the answers must diagnose a PROVIDED specimen (a named weak
    draft) AND be followed by an independent student turn (own-turn signal). A prompt that pre-answers with
    an own-turn tail but NO provided specimen ('...No. Now rewrite it.') still fails - that is a giveaway
    wearing a fig leaf, not a coping model."""
    for i, s in enumerate(L.slots, 1):
        if s.kind != "diagnosis_frq":
            continue
        text = re.sub(r"<[^>]+>", " ", s.body or "")
        if not _SELF_ANSWER_RE.search(text):
            continue
        # sanctioned = (a) coping-model demo on a supplied specimen + an independent own-turn, OR
        #              (b) the student runs the check on their OWN just-written draft (a self-check).
        coping_demo = bool(_OWN_TURN_RE.search(text)) and bool(_PROVIDED_DRAFT_RE.search(text))
        own_selfcheck = bool(_OWN_DRAFT_SELFCHECK_RE.search(text))
        sanctioned = coping_demo or own_selfcheck
        if not sanctioned:
            return False, (f"slot {i}: diagnosis pre-answers its own check without the sanctioned coping-model "
                           f"shape (a named PROVIDED weak draft to diagnose + an independent student turn). "
                           f"Make the student answer the check, or frame it as 'check this weak draft ... now "
                           f"write your own'.")
    return True, "diagnosis checks are student-answered (or a sanctioned coping-model: provided draft + own turn)"

# --- Direct-Instruction / completeness gates (Instructional_Design_KB rules 1,2,4 + Engelmann faultless
#     communication). These enforce that a lesson is a FINISHED, teachable artifact, not a thin blueprint. ---

# Technical terms a G10 writer does not already know: each must be DEFINED in a TEACH slot (in plain words)
# before it appears in any student-facing body/feedback. Keyed term -> a short regex of its surface forms.
_TECH_TERMS = {
    "they-say/I-say": r"\bthey[- ]say\b|\bi[- ]say\b",
    "controlling idea": r"\bcontrolling idea\b",
    # match the CONCEPT 'thesis' but NOT the STAAR rubric-trait label 'Thesis/Purpose' (a scoring category name,
    # not the pedagogical term a lesson must define). Excludes 'thesis/purpose' and 'thesis/'.
    "thesis": r"\bthesis\b(?!\s*/)",
    "claim (arguable)": r"\barguable claim\b",
    "attributive tag": r"\battributive tag\b",
    "appositive": r"\bappositive\b",
    "because/but/so hinge": r"\bbecause/but/so\b|\bbecause-hinge\b",
    "SPO": r"\bSPO\b|single-paragraph outline",
    "counterclaim": r"\bcounterclaim\b",
    "synthesis": r"\bsynthes(is|ize|ise)\b",
    "rhetorical device": r"\brhetorical device\b",
    "warrant": r"\bwarrant\b",
    "rubric trait": r"\brubric trait\b",
}
_DEF_CUE = re.compile(r"\b(means|is when|is a|are the|refers to|that is,|in other words|put simply|"
                      r"stands for|the (?:move|term|idea) here is|we call this|is called)\b", re.I)

def _teach_defines(term_regex: str, teach_bodies: list[str]) -> bool:
    """A term is 'defined' if a TEACH body contains the term AND a definitional cue near it."""
    pat = re.compile(term_regex, re.I)
    for b in teach_bodies:
        for m in pat.finditer(b):
            window = b[max(0, m.start() - 120): m.end() + 160]
            if _DEF_CUE.search(window):
                return True
    return False

def gate_define_before_use(L: Lesson) -> tuple[bool, str]:
    """Engelmann faultless communication + KB Rule 1: no technical term may appear in student-facing text
    unless a TEACH slot defines it in plain words first. Catches jargon like 'they-say' used cold."""
    slots_in_order = L.slots
    teach_bodies = [s.body for s in slots_in_order if s.role == "TEACH"]
    for term, rgx in _TECH_TERMS.items():
        pat = re.compile(rgx, re.I)
        # first student-facing appearance (body OR feedback), in slot order
        used = False
        for s in slots_in_order:
            if pat.search(f"{s.body} {s.feedback}"):
                used = True
                break
        if used and not _teach_defines(rgx, teach_bodies):
            return False, (f"technical term '{term}' is used in student-facing text but never defined in a "
                           f"TEACH slot (faultless-communication / define-before-use). Add a plain-words definition.")
    return True, "all technical terms defined before use"

# substance floors (chars) - a finished slot's student-facing text, not a one-line gesture at content
_DEPTH_FLOOR = {"teach_card": 200, "annotated_before_after": 220, "predict_the_fix": 120,
                "production_frq": 90, "diagnosis_frq": 90, "discrimination": 90}

def gate_content_depth(L: Lesson) -> tuple[bool, str]:
    """KB completeness: teach/model/production bodies must carry REAL content, not a blueprint stub.
    annotated_before_after must contain BOTH a BEFORE and an AFTER inline (the worked example, written out)."""
    for s in L.slots:
        floor = _DEPTH_FLOOR.get(s.kind)
        if floor and len((s.body or "").strip()) < floor:
            return False, (f"{s.role}/{s.kind} body is {len((s.body or '').strip())} chars (< {floor}); "
                           f"looks like a blueprint stub, not finished student-facing content")
        if s.kind == "annotated_before_after":
            b = (s.body or "")
            if not (re.search(r"\bBEFORE\b", b) and re.search(r"\bAFTER\b", b)):
                return False, f"{s.role}/annotated_before_after must contain BOTH a BEFORE and an AFTER example inline"
    return True, "all slots carry finished-depth content; worked examples show before+after"

def gate_model_before_required(L: Lesson) -> tuple[bool, str]:
    """KB Rule 2 (model before produce) + worked-example effect: any slot that asks the student to perform a
    high-load move (diagnose / integrate / synthesize / analyze / revise) must be preceded by a MODEL of that
    move, and a self-diagnosis slot must supply a scaffold (frames / a checklist / named steps) in its body."""
    roles_seen = []
    saw_model = False
    for s in L.slots:
        if s.role == "MODEL" or s.kind in ("annotated_before_after", "predict_the_fix"):
            saw_model = True
        if s.kind == "diagnosis_frq":
            if not saw_model:
                return False, f"{s.role}/diagnosis_frq asks students to diagnose before any MODEL of how to diagnose"
            # scaffold present: sentence frames, a checklist, named steps, OR an authored list/set-apart block
            # (<ol>/<li> = a real checklist rendered structurally; <div ... dashed> = a set-apart weak-draft/frame).
            body = s.body or ""
            has_structured = re.search(r"<ol\b|<li\b|border:1px dashed", body, re.I)
            has_keyword = re.search(r"(frame|checklist|step 1|first,|use this|fill in|sentence starter|template|"
                                    r"name the|say what|then say|prompt:|run the test|rewrite)", body, re.I)
            if not (has_structured or has_keyword):
                return False, (f"{s.role}/diagnosis_frq gives no scaffold (frames/checklist/named steps) for HOW "
                               f"to diagnose; novices need the move modeled + scaffolded, not a blank 'diagnose it'")
    return True, "high-load moves are modeled before required; diagnosis is scaffolded"

def gate_no_ambiguous_reference(L: Lesson) -> tuple[bool, str]:
    """Faultless communication: a slot must not point at 'the summary / this version / that draft / the example'
    unless that referent's text is present IN THE SAME slot body. Catches 'which summary?' ambiguity."""
    deictic = re.compile(r"\b(the summary|this summary|that summary|this version|that version|the draft above|"
                         r"the example above|the passage above|the sentence above)\b", re.I)
    for s in L.slots:
        b = s.body or ""
        m = deictic.search(b)
        if m:
            # OK only if the slot itself shows the referent (a quoted example, a BEFORE/AFTER, or an option list)
            shows_referent = ('"' in b or "BEFORE" in b or "AFTER" in b
                              or re.search(r"\b(Option [AB]|\([AB]\))\b", b) or s.ref)
            if not shows_referent:
                return False, (f"{s.role}/{s.kind} references '{m.group(0)}' but shows no referent in the slot; "
                               f"the student cannot tell WHICH one. Quote it inline or bind the source.")
    return True, "no dangling references; every 'this/that X' shows its referent"

# The developmental TIER each lesson type is allowed to reach (its CEILING unit of production). Derived
# from TWR (sentence-first) + KH (parts before whole) + the reconciled spine. Types that build components
# top out lower; composite-essay types (essay-assembly, synthesis) are the only ones that reach "essay".
#   sentence tier: claim (T2), editing sentences (T6)
#   paragraph tier: source-reading (T1), evidence-integration (T3), analysis (T4), rubric-revision (T5)
#   essay/composite tier: essay-assembly (T7), synthesis (T8)
TYPE_CEILING_UNIT = {
    1: "paragraph", 2: "sentence", 3: "paragraph", 4: "paragraph",
    5: "paragraph", 6: "sentence", 7: "essay", 8: "essay",
}

def gate_unit_ladder(L: Lesson) -> tuple[bool, str]:
    """Within-lesson: the UNIT of production must be NON-DECREASING across the shell (TWR sentence->
    paragraph->composition; never drop back down). A lesson may hold one unit (a claim lesson stays at
    'sentence') or climb, but a later production slot must not produce a SMALLER unit than an earlier one.
    Also: every scored production_frq must declare a unit (so the ladder is auditable)."""
    seq = []  # (slot_title, unit) for production slots that declare a unit, in order
    for s in L.slots:
        if s.kind == "production_frq" and s.scored:
            if not s.unit:
                return False, f"scored production '{s.title[:34]}' declares no unit (sentence|paragraph|multi_paragraph|essay)"
            if s.unit not in UNIT_RANK:
                return False, f"'{s.title[:30]}' has unknown unit '{s.unit}' (must be one of {UNIT_LADDER})"
            seq.append((s.title, s.unit))
    if not seq:
        return True, "no scored sized production slots (n/a)"
    max_so_far = -1
    for title, unit in seq:
        r = UNIT_RANK[unit]
        if r < max_so_far:
            prev = UNIT_LADDER[max_so_far]
            return False, (f"unit ladder DROPS: '{title[:30]}' produces '{unit}' after the lesson already "
                           f"reached '{prev}'. The scaffold must be non-decreasing (sentence->paragraph->essay).")
        max_so_far = max(max_so_far, r)
    ceiling = UNIT_LADDER[max_so_far]
    return True, f"unit ladder non-decreasing; reaches '{ceiling}' ({' -> '.join(u for _t, u in seq)})"

def gate_type_ceiling(L: Lesson) -> tuple[bool, str]:
    """Course-level: a lesson's TOP production unit must not exceed the developmental ceiling for its type.
    Composite-essay types (T7/T8) may reach 'essay'; component types top out at paragraph or sentence, so an
    editing lesson (T6) cannot suddenly demand a full essay before the essay-assembly type teaches it. This
    encodes the 4:2:1 / parts-before-whole ordering as a machine check (KH element-interactivity)."""
    ceiling = TYPE_CEILING_UNIT.get(L.lesson_type)
    if ceiling is None:
        return True, "no ceiling defined for this type (n/a)"
    top = -1
    top_title = ""
    for s in L.slots:
        if s.kind == "production_frq" and s.scored and s.unit in UNIT_RANK:
            if UNIT_RANK[s.unit] > top:
                top, top_title = UNIT_RANK[s.unit], s.title
    if top < 0:
        return True, f"no sized production (n/a); type ceiling is '{ceiling}'"
    if top > UNIT_RANK[ceiling]:
        return False, (f"type {L.lesson_type} tops out at '{UNIT_LADDER[top]}' ('{top_title[:30]}') but its "
                       f"developmental ceiling is '{ceiling}'; a composite-essay unit belongs in T7/T8, not here.")
    return True, f"top production unit '{UNIT_LADDER[top]}' within type ceiling '{ceiling}'"

def gate_mnemonic_status(L: Lesson) -> tuple[bool, str]:
    if L.lesson_type not in LESSON_TYPES:
        return False, f"unknown lesson_type {L.lesson_type}"
    name, mnem, status = LESSON_TYPES[L.lesson_type]
    declared = (L.provenance or {}).get("mnemonic_status")
    if declared != status:
        return False, f"mnemonic_status must be '{status}' for type {L.lesson_type} ({mnem}); got '{declared}'"
    return True, f"type {L.lesson_type} {name}: {mnem} [{status}]"

def gate_no_em_dash(L: Lesson) -> tuple[bool, str]:
    blob = L.title + L.target + " ".join(f"{s.title}{s.body}{s.feedback}" for s in L.slots)
    if "—" in blob or "–" in blob:
        return False, "em/en dash in authored lesson prose (house rule: use commas/colons/parens)"
    return True, "no em dashes"

_OPT_MARKER = re.compile(r"\(([A-D])\)\s")


def gate_distractor_length_cue(L: Lesson) -> tuple[bool, str]:
    """BLOCKS: a choice item (discrimination/predict_the_fix/self_score) must NOT have its correct option as the
    single longest option - that length cue lets a student guess without reasoning (Haladyna item-writing rule:
    options homogeneous in length). Correct answer is read from the 'Correct: X.' / 'Reveal: X.' tail."""
    problems = []
    inspected = 0
    for i, s in enumerate(L.slots):
        # self_score is a PREDICT-YOUR-OWN-RESULT calibration item (often a 2-option pass/gap or a 2-point
        # scale), NOT a distractor-based MCQ where length cues the key. The Haladyna length rule applies to
        # discrimination / predict_the_fix (real distractors); exempt self_score.
        if s.kind not in ("discrimination", "predict_the_fix"):
            continue
        # PREFER the structured choices=[] array (unambiguous). Fall back to prose-parsing only when a slot
        # has no choices[]. If NEITHER yields options for a slot that carries option markers, that is a
        # FAILURE TO INSPECT (fail-closed), NOT a silent skip - the old `continue` here was a fail-open that
        # let an unparseable length-cued item ship green (Fable eval HOLE 1).
        opts, correct = {}, None
        if getattr(s, "choices", None):
            for c in s.choices:
                if c.get("id") and c.get("text") is not None:
                    opts[c["id"]] = str(c["text"])
                if c.get("correct"):
                    correct = c["id"]
        else:
            body = re.sub(r"<[^>]+>", " ", s.body or "")
            fb = re.sub(r"<[^>]+>", " ", s.feedback or "")
            rev = re.search(r"\b(Correct:|Reveal:)", body, re.I)
            core = body[:rev.start()] if (rev and _OPT_MARKER.search(body[:rev.start()])) else body
            cm = re.search(r"\b(?:Correct|Reveal):\s*\(?([A-D])\)?", body + "\n" + fb, re.I)
            for pc in re.split(r"(?=\([A-D]\)\s)", core):
                m = re.match(r"\(([A-D])\)\s*(.+)", pc.strip(), re.S)
                if m:
                    opts[m.group(1)] = m.group(2).strip()
            correct = cm.group(1) if cm else None
        # self_score with 2 options is a legit predict-then-reveal binary; still length-checkable if it has a key.
        has_markers = bool(getattr(s, "choices", None)) or bool(_OPT_MARKER.search(re.sub(r"<[^>]+>", " ", s.body or "")))
        if has_markers and (len(opts) < 2 or not correct):
            problems.append(f"slot {i+1} '{(s.title or '')[:28]}': choice item could not be parsed for "
                            f"length-cue check (opts={len(opts)}, key={correct!r}) - unparseable = fail-closed")
            continue
        if not opts or not correct or correct not in opts:
            continue
        inspected += 1
        lens = {k: len(v) for k, v in opts.items()}
        mx = max(lens.values())
        if lens[correct] == mx and sum(1 for v in lens.values() if v == mx) == 1:
            problems.append(f"slot {i+1} '{(s.title or '')[:28]}': key ({correct}) is the lone longest "
                            f"({lens[correct]} vs {sorted(v for k,v in lens.items() if k!=correct)})")
    if problems:
        return False, "distractor length cue: " + "; ".join(problems)
    return True, f"no length cue: {inspected} choice item(s) inspected, correct never lone-longest"


# internal design vocabulary that must NEVER reach a student. These are authoring/QC terms; a real G9 student
# reading "a Grade-C design bet, labeled as a bet" (as they did in the Fable eval) is confused by jargon that
# was never meant for them. The design RATIONALE belongs in provenance/comments, not the student-facing body.
_LEAKED_LABELS = [
    r"\bgrade[- ]?c\b", r"\bdesign bet\b", r"\blabeled as a bet\b", r"\bdiscrimination slot\b",
    r"\bsignature[- ]?error\b", r"\bcoping model\b", r"\bnear[- ]?peer\b", r"\bSRSD\b",
    r"\bissue frame\b", r"\bissue_frame\b", r"\bstimulus_display\b", r"\bteach_card\b",
    r"\barchetype\b", r"\bT[2-8]\b(?!\w)", r"\brubric_ref\b", r"\brc\.staar\b", r"\brc\.ap\b",
    r"\bmnemonic\b", r"\bcalibration discipline\b", r"\bbank[- ]?partition\b",
]
_LEAK_RE = re.compile("|".join(_LEAKED_LABELS), re.I)

def gate_leaked_internal_label(L: Lesson) -> tuple[bool, str]:
    """No internal authoring/QC jargon in STUDENT-FACING text (slot body/feedback/title). Design rationale lives
    in provenance + comments. Fixes the live Fable finding: 'a Grade-C design bet, labeled as a bet' leaked into
    the discrimination prompt and confused every simulated student ('made zero sense', 'not written for me')."""
    hits = []
    for i, s in enumerate(L.slots):
        text = f"{s.title or ''} {s.body or ''} {s.feedback or ''}"
        text = re.sub(r"<[^>]+>", " ", text)   # ignore markup/attribute values
        for m in _LEAK_RE.finditer(text):
            hits.append(f"slot {i+1} '{(s.title or '')[:24]}': leaked '{m.group(0)}'")
    if hits:
        return False, "internal label leaked into student text: " + "; ".join(hits[:6])
    return True, "no internal design/QC jargon in student-facing text"


def gate_leaked_answer_cue(L: Lesson) -> tuple[bool, str]:
    """No answer given away inside the options. The Fable students noticed wrong MCQ options literally contained
    'Try again' text -> the correct option was the only one without it, so they never had to reason. Distractor
    text must not contain retry/feedback phrasing; that belongs in per-choice feedback, not the option label."""
    leak = re.compile(r"\btry again\b|\bincorrect\b|\bthat'?s wrong\b|\bnot quite\b|\bre-?read\b", re.I)
    hits = []
    for i, s in enumerate(L.slots):
        if s.kind not in ("discrimination", "predict_the_fix", "self_score"):
            continue
        body = re.sub(r"<[^>]+>", " ", s.body or "")
        rev = re.search(r"\b(Correct:|Reveal:)", body, re.I)
        core = body[:rev.start()] if rev else body   # only the OPTIONS region, not the reveal/feedback tail
        for pc in re.split(r"(?=\([A-D]\)\s)", core):
            m = re.match(r"\(([A-D])\)\s*(.+)", pc.strip(), re.S)
            if m and leak.search(m.group(2)):
                hits.append(f"slot {i+1} option ({m.group(1)}) contains feedback/retry text")
    if hits:
        return False, "answer-cue leaked into an option: " + "; ".join(hits[:6])
    return True, "no retry/feedback text leaked into option labels"


def gate_format_fidelity(L: Lesson) -> tuple[bool, str]:
    """Format sanity on authored bodies: (a) any HTML present must be well-formed enough to not run text
    together (balanced block tags), (b) no doubled spaces from a stripped tag, (c) a body with >45 words and NO
    block break (p/br/li/heading/div) is a wall-of-text risk the renderer cannot paragraph -> flag it. This is
    the machine half of Noel's 'formatting 100% correct' gate; visual review still catches the rest."""
    problems = []
    for i, s in enumerate(L.slots):
        b = s.body or ""
        if not b:
            continue
        # balanced common block tags (unbalanced -> run-together render)
        for tag in ("div", "p", "span"):
            if b.lower().count(f"<{tag}") != b.lower().count(f"</{tag}>"):
                problems.append(f"slot {i+1}: unbalanced <{tag}> tags")
        # wall of text: long prose slot with zero block markup
        plain = re.sub(r"<[^>]+>", " ", b)
        words = len(re.findall(r"[A-Za-z]+", plain))
        has_block = re.search(r"</(p|div|li|h[1-6])>|<br", b, re.I)
        if words > 45 and not has_block and s.kind in ("teach_card", "annotated_before_after"):
            problems.append(f"slot {i+1} '{(s.title or '')[:22]}': {words}-word body with no block breaks (wall of text)")
    if problems:
        return False, "format-fidelity: " + "; ".join(problems[:6])
    return True, "authored bodies format-clean (balanced tags, no unbroken wall of text)"


def gate_gate_shape(L: Lesson) -> tuple[bool, str]:
    """A gate lesson must be scaffold-free (verdict): no annotated_before_after / discrimination /
    predict_the_fix; exactly one SCORED cold production write (TRANSFER role, held-out bank); a brief plan is
    allowed only as an UNSCORED affordance (scored=False). Non-gate lessons pass trivially."""
    if getattr(L, "lesson_class", "practice") != "gate":
        return True, "not a gate"
    spec = GRAIN_TEMPLATES["gate"]
    banned = spec["banned_kinds"] & {s.kind for s in L.slots}
    if banned:
        return False, f"gate contains banned teaching scaffold(s): {sorted(banned)}"
    scored_writes = [s for s in L.slots if s.kind == "production_frq" and getattr(s, "scored", False)]
    if not scored_writes:
        return False, "gate has no scored (cold) production write"
    # every SCORED write must be a cold INDEPENDENT/TRANSFER production; a SUPPORTED plan must be scored=False
    # (so it is an affordance, not a certification write). This allows 1 cold essay OR a multi-FRQ section.
    scored_plan = [s for s in scored_writes if s.role == "SUPPORTED"]
    if scored_plan:
        return False, f"gate has a SCORED SUPPORTED plan ({len(scored_plan)}); the plan must be scored=False"
    if not any(s.role in ("INDEPENDENT", "TRANSFER") for s in scored_writes):
        return False, "gate has no cold INDEPENDENT/TRANSFER scored write"
    return True, f"gate is scaffold-free (cue + unscored plan + {len(scored_writes)} cold scored write(s))"


# Structural MCQ defects "no LLM natively avoids" (TestBuilder doc: length-cueing failed 2,400+ items).
# LENGTH-CUEING is handled by gate_distractor_length_cue; gate_structural_item ADDS the OTHER deterministic
# item-writing defects. Banned option FORMS (all/none/both-of-the-above, Type-K roman-numeral combinations)
# invite test-taking heuristics that let a student answer without the target reasoning; a non-standard option
# COUNT, a missing/duplicated key, and duplicate option text are item-writing defects the generator will scale.
_BANNED_OPTION_FORM = re.compile(
    r"\ball of the (?:above|following)\b|\bnone of the (?:above|following)\b|"
    r"\bboth\s+\(?[A-D]\)?\s+and\s+\(?[A-D]\)?\b|"          # both A and B / both (A) and (B)
    r"\b[A-D]\s+and\s+[A-D]\s+(?:only|both)\b",             # A and B only / C and D both
    re.I)
# Type-K roman-numeral combination options ("I and II only", "II and III", "I, II, and III"). Case-SENSITIVE
# (uppercase roman tokens only) so the English pronoun "I" and stray lowercase letters do not false-match.
_BANNED_TYPE_K = re.compile(
    r"\b(?:I{1,3}|IV|V)\b\s*(?:,\s*(?:and\s+)?|and\s+)\b(?:I{1,3}|IV|V)\b")


def _norm_opt(t: str) -> str:
    """Normalize an option's text for duplicate detection: strip tags, lowercase, drop non-alphanumerics,
    collapse whitespace. Two options that differ only in punctuation/case/markup normalize equal."""
    t = re.sub(r"<[^>]+>", " ", t or "")
    t = re.sub(r"[^a-z0-9 ]+", " ", t.lower())
    return re.sub(r"\s+", " ", t).strip()


def _slot_options(s):
    """([(id, text)], correct_ids, parseable) for a choice slot: PREFER the structured choices=[] array;
    fall back to the '(A)...(B)...' prose + 'Correct:/Reveal: X' tail in the body (same parse as
    gate_distractor_length_cue). correct_ids is de-duplicated by letter (a prose reveal names one key)."""
    if getattr(s, "choices", None):
        opts, correct = [], []
        for c in s.choices:
            oid = c.get("id")
            if oid is None:
                continue
            opts.append((oid, str(c.get("text", ""))))
            if c.get("correct"):
                correct.append(oid)
        return opts, correct, True
    body = re.sub(r"<[^>]+>", " ", s.body or "")
    fb = re.sub(r"<[^>]+>", " ", s.feedback or "")
    rev = re.search(r"\b(Correct:|Reveal:)", body, re.I)
    core = body[:rev.start()] if (rev and _OPT_MARKER.search(body[:rev.start()])) else body
    opts = []
    for pc in re.split(r"(?=\([A-D]\)\s)", core):
        m = re.match(r"\(([A-D])\)\s*(.+)", pc.strip(), re.S)
        if m:
            opts.append((m.group(1), m.group(2).strip()))
    correct = [m.group(1) for m in re.finditer(r"\b(?:Correct|Reveal):\s*\(?([A-D])\)?", body + "\n" + fb, re.I)]
    correct = list(dict.fromkeys(correct))   # unique, order-preserving
    return opts, correct, bool(opts)


def gate_structural_item(L) -> tuple[bool, str]:
    """Deterministic structural MCQ micro-checks on discrimination / predict_the_fix items, targeting the
    item-writing defect families 'no LLM natively avoids' (TestBuilder doc) that gate_distractor_length_cue
    does NOT already cover (length-cueing is handled there; this does not duplicate it):
      (a) banned option FORMS: 'all/none of the above', 'both A and B', Type-K roman-numeral combinations;
      (b) option COUNT: a discrimination needs EXACTLY 4 options (LS-feedback #8, 2026-07; each a named
          misconception); other choice items (e.g. predict_the_fix) allow 2-4 (self_score - a 2-point
          predict-your-own-result item - is not a discrimination/predict item and is not inspected here);
      (c) EXACTLY-ONE-CORRECT: exactly one option flagged correct (0 or 2+ correct = defect);
      (d) NO DUPLICATE OPTIONS: two option texts identical/near-identical after normalization.
    Reads s.choices when present, else the '(A)...(B)...'/'Correct: X' prose in s.body/feedback. An
    unparseable choice item is left to gate_distractor_length_cue's fail-closed check, not double-flagged."""
    problems = []
    for i, s in enumerate(L.slots):
        if s.kind not in ("discrimination", "predict_the_fix"):
            continue
        opts, correct, parseable = _slot_options(s)
        if not parseable or not opts:
            continue
        tag = f"slot {i+1} '{(s.title or '')[:24]}'"
        # (a) banned option forms
        for oid, txt in opts:
            if _BANNED_OPTION_FORM.search(txt) or _BANNED_TYPE_K.search(txt):
                problems.append(f"{tag}: banned option form in ({oid}) '{txt.strip()[:36]}'")
        # (b) option count. DISCRIMINATION requires EXACTLY 4 options (LS-feedback #8, 2026-07: 4 lowers the
        # guess rate vs 3, and each 4th is a named misconception). OTHER choice items (predict_the_fix) allow
        # 2-4: a 2-option predict is a legitimate binary pick-better-of-two minimal pair, so for non-
        # discrimination we flag only <2 (not a choice) or >4 (Haladyna: too many options).
        n = len(opts)
        if s.kind == "discrimination":
            if n != 4:
                problems.append(f"{tag}: discrimination has {n} options (need exactly 4; each a named misconception)")
        elif n < 2 or n > 4:
            problems.append(f"{tag}: {n} options (a choice item needs 2-4)")
        # (c) exactly one correct
        if len(correct) != 1:
            problems.append(f"{tag}: {len(correct)} option(s) flagged correct (need exactly 1)")
        # (d) duplicate / near-identical options
        seen = {}
        for oid, txt in opts:
            key = _norm_opt(txt)
            if not key:
                continue
            if key in seen:
                problems.append(f"{tag}: options ({seen[key]}) and ({oid}) are duplicate/near-identical")
            else:
                seen[key] = oid
    if problems:
        return False, "structural item: " + "; ".join(problems[:6])
    return True, "structural items well-formed (option forms, count, single key, no duplicates)"


_CHECK_KINDS = {"discrimination", "predict_the_fix", "self_score"}
_COUNTED_KINDS = {"teach_card", "stimulus_display", "annotated_before_after"}
def gate_check_cadence(L) -> tuple[bool, str]:
    """#3 (council): a run of counted teach segments may not exceed the archetype ceiling with no
    intervening check. Worked-example run = 1; buy_in = 0; memorizable_tool tightens the ceiling to 2
    until the next check. Gate-class lessons + the final write block are exempt."""
    if getattr(L, "lesson_class", "practice") == "gate":
        return True, "gate-class lesson exempt from cadence"
    ceiling = CADENCE_CEILING[archetype_of(L)]
    count = 0; eff = ceiling; prev_worked = False; run_start = None
    for i, s in enumerate(L.slots, 1):
        if s.kind in _CHECK_KINDS:
            count = 0; eff = ceiling; prev_worked = False; continue
        if s.kind not in _COUNTED_KINDS:
            prev_worked = False                   # a write/other slot breaks worked-example adjacency
            continue                              # production/diagnosis writes are not teach segments
        if s.tag == "buy_in":
            prev_worked = False                   # a buy-in card between two A/B slots breaks the run too
            continue
        # collapse a run of DIRECTLY-ADJACENT annotated_before_after into one worked example (anything
        # between them - a write, a buy-in, a plain teach card - ends the run so the next A/B counts fresh)
        if s.kind == "annotated_before_after" and prev_worked:
            continue
        prev_worked = (s.kind == "annotated_before_after")
        count += 1
        if count == 1: run_start = i
        eff = min(ceiling, MEMORIZABLE_TOOL_CEILING) if s.tag == "memorizable_tool" else eff
        if count > eff:
            return False, (f"slots {run_start}-{i}: {count} counted teach segments with no check "
                           f"(archetype {archetype_of(L)} ceiling {eff})")
    return True, f"cadence ok (ceiling {ceiling})"


GATES = [
    ("shell_completeness", gate_shell_completeness),
    ("model_sequence", gate_model_sequence),
    ("discrimination_before_production", gate_discrimination_before_production),
    ("diagnosis_after_write", gate_diagnosis_after_write),
    ("binding_integrity", gate_binding_integrity),
    ("bank_partition", gate_bank_partition),
    ("calibration_discipline", gate_calibration_discipline),
    ("grader_routing", gate_grader_routing),
    ("timeback_native", gate_timeback_native),
    ("no_source_markup", gate_no_source_markup),
    ("no_prior_work_reference", gate_no_prior_work_reference),
    ("frame_comma", gate_frame_comma),
    ("self_answered_check", gate_self_answered_check),
    ("define_before_use", gate_define_before_use),
    ("content_depth", gate_content_depth),
    ("model_before_required", gate_model_before_required),
    ("no_ambiguous_reference", gate_no_ambiguous_reference),
    ("unit_ladder", gate_unit_ladder),
    ("distractor_length_cue", gate_distractor_length_cue),
    ("leaked_internal_label", gate_leaked_internal_label),
    ("leaked_answer_cue", gate_leaked_answer_cue),
    ("format_fidelity", gate_format_fidelity),
    ("type_ceiling", gate_type_ceiling),
    ("effect_size_honesty", gate_effect_size_honesty),
    ("mnemonic_status", gate_mnemonic_status),
    ("no_em_dash", gate_no_em_dash),
    ("gate_gate_shape", gate_gate_shape),
    ("structural_item", gate_structural_item),
    ("check_cadence", gate_check_cadence),
]

def qc_lesson(L: Lesson) -> dict:
    gr, first = {}, None
    for name, fn in GATES:
        try:
            ok, detail = fn(L)
        except Exception as e:
            ok, detail = False, f"gate error: {e!r}"
        gr[name] = {"passed": ok, "detail": detail}
        if not ok and first is None:
            first = name
    overall = all(g["passed"] for g in gr.values())
    L.qc.update({"passed": overall, "gates": gr, "first_failure": first})
    return L.qc

def qc_report(L: Lesson) -> str:
    r = L.qc or qc_lesson(L)
    name = LESSON_TYPES.get(L.lesson_type, ("?",))[0]
    lines = [f"=== LESSON QC: {L.id} (type {L.lesson_type}/{name}) -> {'PASS' if r['passed'] else 'FAIL'} ===",
             f"    slots: {len(L.slots)}  ({', '.join(s.role[0] + ':' + s.kind for s in L.slots)})"]
    for nm, g in r["gates"].items():
        lines.append(f"  [{'PASS' if g['passed'] else 'FAIL'}] {nm}: {g['detail']}")
    return "\n".join(lines)

# ---- self-test: a minimal well-formed lesson ------------------------------
if __name__ == "__main__":
    demo = Lesson(
        id="ACC-W910-L-EVIDENCE-DEMO", grade="9-10", lesson_type=3,
        unit="G10 U2 source-based argument (evidence-integration)",
        title="Integrating Evidence So No Quote Stands Alone (PROVE)",
        target="Integrate a source quote with attribution + a because/but/so hinge tied to the claim.",
        acc_tags=["ACC.W.SRC.1", "ACC.W.ARG.2", "CCSS.W.9-10.1"],
        provenance={"copyright": "own_authored", "authored": "2026-07-07", "mnemonic_status": "established-caveat"},
        fade_ledger_moves=["because/but/so", "attributive-tag"],
        slots=[
            Slot("TEACH", "teach_card", "What integration means + the PROVE cue",
                 body="A dropped quote leaves the reader to guess who said it and why it matters. PROVE: Point, "
                      "Reference, Observe, Verify, Extend. On the test, bare quotes cap your Evidence score."),
            Slot("TEACH", "stimulus_display", "Read the source", ref="ACC-W910-INFO-SINGLE-0001",
                 bank="coral_reefs"),
            Slot("MODEL", "annotated_before_after", "Before/after: a dropped quote becomes integrated",
                 body="BEFORE (drops the move): The author says reefs are dying. This proves my point. "
                      "AFTER (explains HOW): Marine biologist Dr. Lee, writing for NOAA, reports that half of "
                      "reef cover has been lost since 1950, which matters because it shows the loss is already "
                      "underway, not a distant risk.", bank="coral_reefs"),
            Slot("MODEL", "predict_the_fix", "Predict: what is missing before we fix it?",
                 body="Which move would most improve: 'Reefs are important. \"They support fish.\" So we should act.'?",
                 feedback="The quote has no attribution and no tie to the claim. Adding who said it plus a "
                          "because-hinge (it matters because...) is the fix. That is the R and V in PROVE.",
                 bank="coral_reefs"),
            Slot("SUPPORTED", "discrimination", "Integrated vs dropped (minimal pair)",
                 ref="ACC-W910-SR-EVID-0001", labeled_grade_c=True, bank="street_trees"),
            Slot("SUPPORTED", "production_frq", "Write one integrated PROVE sentence on the source",
                 body="Using the source, write ONE sentence that attributes a fact and ties it to a claim with a "
                      "because/but/so hinge.", rubric_ref="rc.staar", scored=True, bank="coral_reefs",
                 unit="sentence"),
            Slot("MODEL", "diagnosis_frq", "Diagnose your own sentence",
                 body="In one sentence: what was weak in a bare quote, how did you fix it, why is it stronger?",
                 scored=True, bank="coral_reefs"),
            Slot("INDEPENDENT", "production_frq", "Integrate evidence into a full PROVE paragraph",
                 body="Write a paragraph that states a claim and develops it with an integrated source quote.",
                 rubric_ref="rc.staar", scored=True, bank="coral_reefs", unit="paragraph"),
            Slot("TRANSFER", "production_frq", "Integrate evidence on a NEW topic (bank-partitioned)",
                 body="Now do the same with a source on a different topic you have not practiced.",
                 rubric_ref="rc.ohio", scored=True, bank="nuclear_power", unit="paragraph"),
        ],
    )
    qc_lesson(demo)
    print(qc_report(demo))
    sys.exit(0 if demo.qc["passed"] else 1)
