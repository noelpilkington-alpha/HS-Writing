"""
cr_multi_perspective.py  -  G11 constructed-response (CR) MULTI-PERSPECTIVE argument essay prompts.

Six extended-text argument prompts, each BINDING to one of the three G11 multi-perspective
(perspective-set) stimuli in Stimulus_Bank_G11. Modeled on ACT Writing: an issue is presented with
EXACTLY three given perspectives and NO source passage. The scored move is to evaluate the three
perspectives, develop and support the student's OWN perspective, and analyze the RELATIONSHIP between
the student's position and at least one of the given perspectives. Scored on rc.ap. mode="argument"
(accepted by CR_MODES). No passage is attached to these ACT-shaped items.

Stimulus coverage (each of the 3 MP-PERSP ids used twice, 6 items total):
  ACC-W910-MP-PERSP-0001  the value of human work as machines advance -> 0701, 0704
  ACC-W910-MP-PERSP-0002  privacy vs. public safety in a connected world -> 0702, 0705
  ACC-W910-MP-PERSP-0003  the role of standardized testing in education -> 0703, 0706

Each pair varies which relationship the student must foreground: the first asks the student to build a
position by weighing all three perspectives; the second asks the student to align with or push against
a single named perspective and analyze that relationship directly. Runs each item through the
item_contract QC harness and prints "N/6 PASS". No em dashes.
"""
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from item_contract import Item, qc_item, qc_report

ACC = ["ACC.W.ARG.2", "CCSS.W.11-12.1"]
PROV = {"copyright": "own_authored", "authored": "2026-07-09"}

WORK = "ACC-W910-MP-PERSP-0001"
PRIVACY = "ACC-W910-MP-PERSP-0002"
TESTING = "ACC-W910-MP-PERSP-0003"

ITEMS = [
    # ---- 0701: AUTOMATION AND WORK (weigh all three) -------------------------------------------------
    Item(
        id="ACC-W910-CR-MP-0701", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("Read and consider the three perspectives on the value of human work as machines advance. "
              "Then write a unified essay that evaluates the three perspectives, develops and supports your "
              "own perspective on the issue, and analyzes the relationship between your perspective and at "
              "least one of the perspectives given. You may agree with any of them, disagree with all of "
              "them, or take a position of your own."),
        acc_tags=ACC,
        stimulus_ref=WORK,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
    # ---- 0702: PRIVACY vs SAFETY (weigh all three) ---------------------------------------------------
    Item(
        id="ACC-W910-CR-MP-0702", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("Read and consider the three perspectives on the balance between privacy and public safety in "
              "a connected world. Then write a unified essay that evaluates the three perspectives, develops "
              "and supports your own perspective on the issue, and analyzes the relationship between your "
              "perspective and at least one of the perspectives given. You may agree with any of them, "
              "disagree with all of them, or take a position of your own."),
        acc_tags=ACC,
        stimulus_ref=PRIVACY,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
    # ---- 0703: STANDARDIZED TESTING (weigh all three) ------------------------------------------------
    Item(
        id="ACC-W910-CR-MP-0703", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("Read and consider the three perspectives on the role of standardized testing in education. "
              "Then write a unified essay that evaluates the three perspectives, develops and supports your "
              "own perspective on the issue, and analyzes the relationship between your perspective and at "
              "least one of the perspectives given. You may agree with any of them, disagree with all of "
              "them, or take a position of your own."),
        acc_tags=ACC,
        stimulus_ref=TESTING,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
    # ---- 0704: AUTOMATION AND WORK, second prompt (single-relationship focus) ------------------------
    Item(
        id="ACC-W910-CR-MP-0704", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("Read and consider the three perspectives on the value of human work as machines advance. "
              "Then write a unified essay that develops and supports your own perspective on the issue. "
              "Identify the one given perspective that stands closest to or furthest from your own, and "
              "analyze that relationship in depth, showing where the two agree, where they part, and why. "
              "Evaluate the remaining perspectives as you build your case."),
        acc_tags=ACC,
        stimulus_ref=WORK,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
    # ---- 0705: PRIVACY vs SAFETY, second prompt (single-relationship focus) --------------------------
    Item(
        id="ACC-W910-CR-MP-0705", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("Read and consider the three perspectives on the balance between privacy and public safety in "
              "a connected world. Then write a unified essay that develops and supports your own perspective "
              "on the issue. Choose the one given perspective you find strongest or most mistaken, and "
              "analyze the relationship between it and your own position in depth. Evaluate the remaining "
              "perspectives as you build your case."),
        acc_tags=ACC,
        stimulus_ref=PRIVACY,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
    # ---- 0706: STANDARDIZED TESTING, second prompt (single-relationship focus) -----------------------
    Item(
        id="ACC-W910-CR-MP-0706", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("Read and consider the three perspectives on the role of standardized testing in education. "
              "Then write a unified essay that develops and supports your own perspective on the issue. "
              "Single out the one given perspective that most sharply challenges your own, and analyze the "
              "relationship between it and your position in depth, answering its strongest point. Evaluate "
              "the remaining perspectives as you build your case."),
        acc_tags=ACC,
        stimulus_ref=TESTING,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
]

if __name__ == "__main__":
    passed = 0
    for it in ITEMS:
        qc_item(it)
        print(qc_report(it))
        print(f"  -> binds to {it.stimulus_ref} | rubric {it.rubric_ref}")
        print()
        if it.qc["passed"]:
            passed += 1
    print(f"{passed}/{len(ITEMS)} PASS")
    sys.exit(0 if passed == len(ITEMS) else 1)
