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
RUBRIC_CONFIGS = {"rc.staar", "rc.mcas", "rc.ohio", "rc.4trait", "rc.ap"}

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

# Unit-of-production ladder (TWR Principle 2: begin at the sentence, then build to paragraphs, then
# compositions; "a writer who cannot compose a decent sentence will never produce a decent essay",
# TWR2.0 loc ~1343-1395). KH element-interactivity: do not compose the whole before the parts are fluent
# (HLH Ch.17 blank-page fails novices; KB 00 §1.1/§1.2). The SPO explicitly scales sentence->paragraph->
# multi-paragraph (TWR2.0 Ch.6). This is the settled developmental axis; ordered low->high.
UNIT_LADDER = ["sentence", "paragraph", "multi_paragraph", "essay"]
UNIT_RANK = {u: i for i, u in enumerate(UNIT_LADDER)}

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

# ---- bank id index (scan once) --------------------------------------------

def _bank_ids() -> set[str]:
    ids: set[str] = set()
    for d in (STIMULUS_DIR, ITEM_DIR, os.path.join(HERE)):
        for f in glob.glob(os.path.join(d, "*.py")):
            try:
                src = open(f, encoding="utf-8").read()
            except Exception:
                continue
            # ANY literal full id token: "ACC-W910-<FAMILY>-NNNN". Catches both id="..." AND ids passed
            # as positional args to helper builders (e.g. mk("ACC-W910-SR-LANG-0001", ...) in sr_language.py
            # and scr("ACC-W910-SR-SCR-0001", ...) in sr_scr_modifier.py, which an id="..."-only regex misses).
            ids.update(re.findall(r'"(ACC-W910-[A-Z0-9\-]+-\d{4})"', src))
            # bare literal id="..." without a trailing 4-digit block (defensive)
            ids.update(re.findall(r'\bid\s*=\s*"(ACC-W910-[A-Z0-9\-]+)"', src))
            # programmatic ids: id=f"ACC-W910-SR-ORG-{idnum:04d}"  ->  register the prefix as a family
            for pre in re.findall(r'\bid\s*=\s*f"(ACC-W910-SR-[A-Z]+)-\{', src):
                ids.add(pre + "-*")   # wildcard family marker
    return ids

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
    for r in SHELL_ORDER:
        if r not in roles:
            return False, f"SRSD shell incomplete: missing '{r}' stage"
    # shell stages must appear in order (first occurrence of each role is monotincreasing)
    firsts = [roles.index(r) for r in SHELL_ORDER]
    if firsts != sorted(firsts):
        return False, f"shell stages out of order: {[(r, roles.index(r)) for r in SHELL_ORDER]}"
    return True, "SRSD shell complete + in order (Teach->Model->Supported->Independent->Transfer)"

def gate_model_sequence(L: Lesson) -> tuple[bool, str]:
    """Modality-corrected Model slot: clean annotated before/after -> predict-the-fix (mechanisms 1-2 in
    MODEL), plus a student-generated diagnosis somewhere in the lesson (mechanism 4). Mechanism 3 (feedback
    on the student's OWN draft) is the production_frq's grader feedback. NO passive-read messy think-aloud."""
    model = [s for s in L.slots if s.role == "MODEL"]
    kinds = {s.kind for s in model}
    if "annotated_before_after" not in kinds:
        return False, "MODEL missing the clean annotated before/after (mechanism 1: unambiguous worked example)"
    if "predict_the_fix" not in kinds:
        return False, "MODEL missing predict-the-fix (mechanism 2: student diagnoses BEFORE the reveal)"
    if not any(s.kind == "diagnosis_frq" for s in L.slots):
        return False, "no student-generated diagnosis slot (mechanism 4) anywhere in the lesson"
    # predict-the-fix must carry a reveal (feedback-block)
    for s in model:
        if s.kind == "predict_the_fix" and not s.feedback.strip():
            return False, "predict-the-fix has no feedback reveal (feedback-block)"
    return True, "Model = 4-mechanism async sequence (annotated before/after + predict-the-fix + diagnosis)"

def gate_discrimination_before_production(L: Lesson) -> tuple[bool, str]:
    """Grade-C move, LABELED as a design bet. A discrimination slot must appear before any production FRQ."""
    disc_idx = [i for i, s in enumerate(L.slots) if s.kind == "discrimination"]
    prod_idx = [i for i, s in enumerate(L.slots) if s.kind in ("production_frq", "diagnosis_frq")]
    if not disc_idx:
        return False, "no discrimination slot (the Grade-C discriminate-before-produce move is required)"
    if prod_idx and min(disc_idx) > min(prod_idx):
        return False, "production appears before any discrimination (violates discriminate-before-produce)"
    # must be LABELED a design bet (Grade C), not sold as evidence
    if not any(s.labeled_grade_c for s in L.slots if s.kind == "discrimination"):
        return False, "discrimination slots must set labeled_grade_c=True (label the Grade-C design bet)"
    return True, "discrimination precedes production; Grade-C move labeled"

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
    taught = {s.bank for s in L.slots if s.role in ("MODEL", "SUPPORTED") and s.bank}
    transfer = [s for s in L.slots if s.role == "TRANSFER"]
    if not transfer:
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
    KILL-list: never 'hand rubric + grade yourself'; ban person-praise. (W&H: overestimate bias g=0.206.)"""
    ss_idx = [i for i, s in enumerate(L.slots) if s.kind == "self_score"]
    prod_idx = [i for i, s in enumerate(L.slots) if s.kind in ("production_frq", "diagnosis_frq")]
    for i in ss_idx:
        if not any(j > i for j in prod_idx):
            return False, "a self_score has no following graded reveal (must predict THEN reveal the gap)"
    # ban person-praise in authored bodies/feedback (praise ~0.12; kill-list)
    praise = re.compile(r"\b(great job|good job|you'?re so smart|nice work|well done|you'?re a natural)\b", re.I)
    for s in L.slots:
        blob = f"{s.body} {s.feedback}"
        if praise.search(blob):
            return False, f"person-praise in {s.role}/{s.kind} (kill-list: praise ES ~0.12; use GOAL/NOW/NEXT)"
    return True, ("calibration: self-score precedes reveal; no person-praise" if ss_idx
                  else "no self_score slot (n/a); no person-praise")

def gate_grader_routing(L: Lesson) -> tuple[bool, str]:
    """Every production_frq must carry a valid rc.* rubric config the deployed grader implements."""
    prods = [s for s in L.slots if s.kind == "production_frq"]
    if not prods:
        return False, "no production_frq slot (a lesson must reach production)"
    for s in prods:
        if s.rubric_ref not in RUBRIC_CONFIGS:
            return False, f"production_frq '{s.title[:30]}' rubric_ref '{s.rubric_ref}' not in {RUBRIC_CONFIGS}"
    return True, f"{len(prods)} production FRQ(s), all routed to a valid rc.* config"

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

# --- Direct-Instruction / completeness gates (Instructional_Design_KB rules 1,2,4 + Engelmann faultless
#     communication). These enforce that a lesson is a FINISHED, teachable artifact, not a thin blueprint. ---

# Technical terms a G10 writer does not already know: each must be DEFINED in a TEACH slot (in plain words)
# before it appears in any student-facing body/feedback. Keyed term -> a short regex of its surface forms.
_TECH_TERMS = {
    "they-say/I-say": r"\bthey[- ]say\b|\bi[- ]say\b",
    "controlling idea": r"\bcontrolling idea\b",
    "thesis": r"\bthesis\b",
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
            # scaffold present: sentence frames, a checklist, or named steps in the prompt
            if not re.search(r"(frame|checklist|step 1|first,|use this|fill in|sentence starter|template|"
                             r"name the|say what|then say|prompt:)", s.body or "", re.I):
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

GATES = [
    ("shell_completeness", gate_shell_completeness),
    ("model_sequence", gate_model_sequence),
    ("discrimination_before_production", gate_discrimination_before_production),
    ("binding_integrity", gate_binding_integrity),
    ("bank_partition", gate_bank_partition),
    ("calibration_discipline", gate_calibration_discipline),
    ("grader_routing", gate_grader_routing),
    ("timeback_native", gate_timeback_native),
    ("no_source_markup", gate_no_source_markup),
    ("no_prior_work_reference", gate_no_prior_work_reference),
    ("define_before_use", gate_define_before_use),
    ("content_depth", gate_content_depth),
    ("model_before_required", gate_model_before_required),
    ("no_ambiguous_reference", gate_no_ambiguous_reference),
    ("unit_ladder", gate_unit_ladder),
    ("type_ceiling", gate_type_ceiling),
    ("effect_size_honesty", gate_effect_size_honesty),
    ("mnemonic_status", gate_mnemonic_status),
    ("no_em_dash", gate_no_em_dash),
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
