"""
item_contract.py  -  The enforceable contract + QC harness for the G10 test-bank ITEM generator.

Mirrors stimulus_contract.py. An item is ACCEPTED only if it passes every machine-checkable gate from
the L4 item spec (`../G10_Item_Spec_L4.md`). Two families:
  - SR (selected-response editing): auto-gradable; embedded short draft; no stimulus dependency.
  - CR (constructed-response essay): extended-text + external grader; BINDS to a Stimulus_Bank_G10 stimulus.

Gates: schema, acc_tags, cr_binding, rubric_config, distractor_integrity (SR), no_change_discipline (SR),
content (reuse content_screen.py), no_em_dash. Dependency-free (stdlib + local content_screen).
"""
from __future__ import annotations
import re, os, sys, glob
from dataclasses import dataclass, field
from typing import Literal

sys.path.insert(0, os.path.dirname(__file__))
import content_screen as cs

Family = Literal["SR", "CR", "SCR"]
QTI_SR = {"choice", "inline-choice", "hottext", "text-entry"}
QTI_CR = {"extended-text"}
QTI_SCR = {"text-entry"}
RUBRIC_CONFIGS = {"rc.staar", "rc.mcas", "rc.ohio", "rc.4trait", "rc.ap",
                  "rc.scr1", "rc.scr2", "rc.scr3"}
CR_MODES = {"argument", "explanatory", "analysis"}
SR_SUBSKILLS = {"conventions", "sentence", "organization", "evidence", "language"}  # 'scr' REMOVED -> SCR family
SCR_SUBTYPES = {"scr_writing", "scr_analysis", "scr_research"}
SCR_BINDING = {"scr_writing": False, "scr_analysis": True, "scr_research": True}
SCR_RUBRIC_FOR = {"scr_writing": "rc.scr1", "scr_research": "rc.scr2", "scr_analysis": "rc.scr3"}

STIMULUS_DIR = os.path.join(os.path.dirname(__file__), "..", "Stimulus_Bank_G10")
# All grade stimulus banks a CR item may bind to (G9/G10/G11/G12). The binding gate scans every one so
# a G9 item can bind a G9 stimulus, etc. STIMULUS_DIR is kept as the G10 default for back-compat.
_ROOT = os.path.join(os.path.dirname(__file__), "..")
STIMULUS_DIRS = [os.path.join(_ROOT, d) for d in
                 ("Stimulus_Bank_G9", "Stimulus_Bank_G10", "Stimulus_Bank_G11", "Stimulus_Bank_G12")]

@dataclass
class Option:
    id: str
    text: str
    correct: bool = False
    rationale: str = ""

@dataclass
class Item:
    id: str
    family: Family
    grade: str                 # "9-10"
    stem: str
    qti_type: str
    subskill_or_mode: str      # SR: subskill; CR: mode
    acc_tags: list[str] = field(default_factory=list)
    # SR:
    options: list[Option] = field(default_factory=list)
    answer_key: list[str] = field(default_factory=list)
    # CR:
    stimulus_ref: str = ""     # a Stimulus_Bank id
    rubric_ref: str = ""       # an rc.* config
    provenance: dict = field(default_factory=dict)
    qc: dict = field(default_factory=dict)

# ---- gates ----------------------------------------------------------------

def gate_schema(it: Item) -> tuple[bool, str]:
    if it.family not in ("SR", "CR", "SCR"):
        return False, f"bad family '{it.family}'"
    if it.family == "SCR":
        return True, "schema ok (SCR: validated by scr_schema gate)"
    if not it.stem.strip():
        return False, "empty stem"
    if it.family == "SR":
        if it.qti_type not in QTI_SR:
            return False, f"SR qti_type '{it.qti_type}' not in {QTI_SR}"
        if it.subskill_or_mode not in SR_SUBSKILLS:
            return False, f"SR subskill '{it.subskill_or_mode}' not in {SR_SUBSKILLS}"
        if it.qti_type == "text-entry":
            # SCR short production: answer_key is a model answer, options may be empty
            if not it.answer_key:
                return False, "text-entry (SCR) needs a model answer_key"
            return True, "schema ok (SR text-entry/SCR)"
        if len(it.options) < 3:
            return False, f"SR choice needs >=3 options, got {len(it.options)}"
        correct = [o for o in it.options if o.correct]
        if len(correct) < 1:
            return False, "SR item has no correct option"
        if not it.answer_key or set(it.answer_key) != {o.id for o in correct}:
            return False, "answer_key must match the correct option id(s)"
        return True, f"schema ok (SR {it.qti_type}, {len(it.options)} options)"
    else:  # CR
        if it.qti_type not in QTI_CR:
            return False, f"CR qti_type '{it.qti_type}' not in {QTI_CR}"
        if it.subskill_or_mode not in CR_MODES:
            return False, f"CR mode '{it.subskill_or_mode}' not in {CR_MODES}"
        return True, "schema ok (CR extended-text)"

def gate_acc_tags(it: Item) -> tuple[bool, str]:
    if not it.acc_tags:
        return False, "missing acc_tags"
    if not any(t.startswith("ACC.W") for t in it.acc_tags):
        return False, "needs >=1 ACC.W code (plus state tags)"
    return True, f"{len(it.acc_tags)} tags"

def gate_cr_binding(it: Item) -> tuple[bool, str]:
    if it.family != "CR":
        return True, "n/a (SR)"
    if not it.stimulus_ref.strip():
        return False, "CR item missing stimulus_ref"
    # the referenced stimulus id must exist in SOME grade's stimulus bank (scan every bank's id= lines)
    ids = set()
    for d in STIMULUS_DIRS:
        for f in glob.glob(os.path.join(d, "*.py")):
            try:
                src = open(f, encoding="utf-8").read()
                for m in re.findall(r'\bid\s*=\s*"(ACC-W910-[A-Z\-]+-\d{4})"', src):
                    ids.add(m)
            except Exception:
                pass
    if it.stimulus_ref not in ids:
        return False, f"stimulus_ref '{it.stimulus_ref}' not found in any stimulus bank ({len(ids)} stimuli known)"
    return True, f"bound to {it.stimulus_ref}"

def gate_rubric_config(it: Item) -> tuple[bool, str]:
    if it.family != "CR":
        return True, "n/a (SR)"
    if it.rubric_ref not in RUBRIC_CONFIGS:
        return False, f"rubric_ref '{it.rubric_ref}' not in {RUBRIC_CONFIGS}"
    return True, f"rubric {it.rubric_ref}"

def gate_distractor_integrity(it: Item) -> tuple[bool, str]:
    if it.family != "SR" or it.qti_type == "text-entry":
        return True, "n/a"
    texts = [o.text.strip().lower() for o in it.options]
    if len(set(texts)) != len(texts):
        return False, "duplicate option texts"
    # no "all/none of the above"
    if any(re.search(r"\b(all|none) of the above\b", t) for t in texts):
        return False, "contains 'all/none of the above'"
    # position/length leak: the correct option must not be a MEANINGFUL length outlier (test-savvy students
    # pick the conspicuously longest/shortest option). Tolerance: only flag if the correct option is >25%
    # longer than the next-longest or >25% shorter than the next-shortest distractor. A 1-2 char edge is not
    # a real, exploitable leak; a "much longer, more-qualified" correct answer is.
    correct = [o for o in it.options if o.correct]
    distractor_lens = [len(o.text) for o in it.options if not o.correct]
    if distractor_lens:
        dmax, dmin = max(distractor_lens), min(distractor_lens)
        for c in correct:
            L = len(c.text)
            if L > dmax * 1.25:
                return False, f"correct option conspicuously longest ({L} vs distractor max {dmax}) - length leak"
            if L < dmin * 0.75:
                return False, f"correct option conspicuously shortest ({L} vs distractor min {dmin}) - length leak"
    # every distractor should carry a rationale (real misconception, not filler)
    if any(not o.rationale.strip() for o in it.options if not o.correct):
        return False, "every distractor needs a rationale (real misconception)"
    return True, f"{len(it.options)} options, distractors rationalized, no leaks"

def gate_no_change_discipline(it: Item) -> tuple[bool, str]:
    """If a 'NO CHANGE' option is present, it must SOMETIMES be the key across the bank. Per-item we only
    check it's a real option; the sometimes-correct property is a bank-level check (noted, not enforced here)."""
    if it.family != "SR":
        return True, "n/a"
    has_nc = any(re.match(r"\s*no change\s*$", o.text, re.I) for o in it.options)
    return True, ("NO-CHANGE present" if has_nc else "no NO-CHANGE option")

def _as_cr_for_binding(it: Item) -> Item:
    """A shim so SCR binding reuses gate_cr_binding's stimulus-existence scan."""
    return Item(id=it.id, family="CR", grade=it.grade, stem=it.stem,
                qti_type="extended-text", subskill_or_mode="argument",
                stimulus_ref=it.stimulus_ref, rubric_ref="rc.staar")

def gate_scr_schema(it: Item) -> tuple[bool, str]:
    if it.family != "SCR":
        return True, "n/a (not SCR)"
    if it.subskill_or_mode not in SCR_SUBTYPES:
        return False, f"SCR subtype '{it.subskill_or_mode}' not in {SCR_SUBTYPES}"
    if it.qti_type not in QTI_SCR:
        return False, f"SCR qti_type '{it.qti_type}' not in {QTI_SCR}"
    if not it.stem.strip():
        return False, "empty stem"
    if not it.answer_key:
        return False, "SCR needs a model answer_key"
    if it.options:
        return False, "SCR (text-entry) takes no options"
    return True, f"schema ok (SCR {it.subskill_or_mode})"

def gate_scr_binding(it: Item) -> tuple[bool, str]:
    if it.family != "SCR":
        return True, "n/a (not SCR)"
    must_bind = SCR_BINDING.get(it.subskill_or_mode, False)
    has_ref = bool(it.stimulus_ref.strip())
    if must_bind and not has_ref:
        return False, f"{it.subskill_or_mode} must bind a stimulus (stimulus_ref empty)"
    if not must_bind and has_ref:
        return False, f"{it.subskill_or_mode} must NOT bind a stimulus (sentence-level)"
    if must_bind:
        # reuse CR's stimulus-existence scan
        ok, detail = gate_cr_binding(_as_cr_for_binding(it))
        if not ok:
            return False, detail
    return True, ("bound to " + it.stimulus_ref) if must_bind else "no stimulus (correct)"

def gate_scr_rubric(it: Item) -> tuple[bool, str]:
    if it.family != "SCR":
        return True, "n/a (not SCR)"
    want = SCR_RUBRIC_FOR.get(it.subskill_or_mode)
    if it.rubric_ref != want:
        return False, f"SCR {it.subskill_or_mode} needs rubric_ref '{want}', got '{it.rubric_ref}'"
    return True, f"rubric {it.rubric_ref}"

def gate_content(it: Item) -> tuple[bool, str]:
    # screen the stem + option texts (SR) for appropriateness bright lines
    class _P:
        def __init__(s, t): s.text = t
    body = it.stem + "\n" + "\n".join(o.text for o in it.options)
    r = cs.screen([_P(body)], prompt=it.stem, mode=it.subskill_or_mode if it.family == "CR" else "",
                  family="")
    it.qc.setdefault("content_screen", r)
    if r["verdict"] == "REJECT":
        return False, "content REJECT: " + "; ".join(x["check"] for x in r["rejects"])
    if r["verdict"] == "FLAG":
        return True, "content FLAG (review): " + "; ".join(x["check"] for x in r["flags"])
    return True, "content clean"

def gate_no_em_dash(it: Item) -> tuple[bool, str]:
    body = it.stem + " ".join(o.text + o.rationale for o in it.options)
    if "—" in body or "–" in body:
        return False, "em/en dash in authored item prose"
    return True, "no em dashes"

GATES = [
    ("schema", gate_schema),
    ("acc_tags", gate_acc_tags),
    ("cr_binding", gate_cr_binding),
    ("rubric_config", gate_rubric_config),
    ("distractor_integrity", gate_distractor_integrity),
    ("no_change_discipline", gate_no_change_discipline),
    ("scr_schema", gate_scr_schema),
    ("scr_binding", gate_scr_binding),
    ("scr_rubric", gate_scr_rubric),
    ("content", gate_content),
    ("no_em_dash", gate_no_em_dash),
]

def qc_item(it: Item) -> dict:
    gr, first = {}, None
    for name, fn in GATES:
        try:
            ok, detail = fn(it)
        except Exception as e:
            ok, detail = False, f"gate error: {e!r}"
        gr[name] = {"passed": ok, "detail": detail}
        if not ok and first is None:
            first = name
    overall = all(g["passed"] for g in gr.values())
    it.qc.update({"passed": overall, "gates": gr, "first_failure": first})
    return it.qc

def qc_report(it: Item) -> str:
    r = it.qc or qc_item(it)
    lines = [f"=== ITEM QC: {it.id} ({it.family}/{it.subskill_or_mode}) -> {'PASS' if r['passed'] else 'FAIL'} ==="]
    for name, g in r["gates"].items():
        lines.append(f"  [{'PASS' if g['passed'] else 'FAIL'}] {name}: {g['detail']}")
    return "\n".join(lines)

# ---- self-test: one SR item + one CR item --------------------------------
if __name__ == "__main__":
    sr = Item(
        id="ACC-W910-SR-EVIDENCE-0001", family="SR", grade="9-10", subskill_or_mode="evidence",
        qti_type="choice",
        stem=("A student is writing an argument that cities should expand public transit. Which sentence, "
              "added after sentence 3, best supports that claim with relevant evidence?"),
        acc_tags=["ACC.W.SRC.1", "ACC.W.ARG.2", "CCSS.W.9-10.1"],
        options=[
            Option("A", "A single light-rail line moves as many riders per hour as six full highway lanes.", True, ""),
            Option("B", "Many people enjoy listening to their favorite music while they commute to work.", False, "off-claim: rider experience, not transit capacity"),
            Option("C", "Traffic congestion is a serious problem in almost every large American city.", False, "restates the topic, adds no evidence for the claim"),
            Option("D", "Some drivers still prefer their own cars because they value privacy and control.", False, "supports the opposing view, not the claim"),
        ],
        answer_key=["A"],
        provenance={"copyright": "own_authored", "authored": "2026-07-07"},
    )
    cr = Item(
        id="ACC-W910-CR-ARGUMENT-0001", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("Weighing both sources, write an argumentative essay stating your position on whether the US "
              "should build more nuclear power. Support your claim with evidence from both sources and "
              "address at least one objection to your position."),
        acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "ACC.W.ARG.5", "CCSS.W.9-10.1"],
        stimulus_ref="ACC-W910-ARG-OPP-0003",   # the nuclear opposing-pair stimulus
        rubric_ref="rc.staar",
        provenance={"copyright": "own_authored", "authored": "2026-07-07"},
    )
    for it in (sr, cr):
        qc_item(it)
        print(qc_report(it)); print()
    sys.exit(0 if (sr.qc["passed"] and cr.qc["passed"]) else 1)
