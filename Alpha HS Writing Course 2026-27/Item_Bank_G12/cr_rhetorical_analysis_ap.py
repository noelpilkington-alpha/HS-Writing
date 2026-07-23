"""
cr_rhetorical_analysis_ap.py  -  G12 constructed-response (CR) RHETORICAL-ANALYSIS essay prompts (AP tier).

Five extended-text rhetorical-analysis prompts that REUSE the three G11 single-passage rhetorical-analysis
stimuli in Stimulus_Bank_G11 (public-domain speeches/essay). The G12 tier rides on the G11 passages; the NEW
dimension is SOPHISTICATION + sustained timed conditions. Modeled on the AP English Language rhetorical
analysis FRQ (Q2), scored on rc.ap, where Row B point 4 and Row C reward analysis that treats the COMPLEXITY
of the writer's choices (tensions, shifts, how choices work together) and situates them rhetorically within
the writer's situation, audience, and purpose, never merely restating what the passage says.

mode="analysis" (accepted by CR_MODES).

G12-DISTINCT id range: CR-RA-08xx (zero collision with G9 05xx / G10 00xx / G11 07xx).

Stimulus coverage (5 items across the 3 reused G11 RA-SINGLE ids):
  ACC-W910-RA-SINGLE-0001  FDR, First Inaugural Address (1933)   -> 0801, 0804
  ACC-W910-RA-SINGLE-0002  Bryan, "Cross of Gold" speech (1896)  -> 0802, 0805
  ACC-W910-RA-SINGLE-0003  Emerson, "Self-Reliance" (1841)       -> 0803

Runs each item through the item_contract QC harness and prints "N/5 PASS". No em dashes.
"""
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from item_contract import Item, qc_item, qc_report

ACC = ["ACC.W.INFO.6", "ACC.W.SRC.3", "CCSS.W.11-12.9"]
PROV = {"copyright": "own_authored", "authored": "2026-07-09"}

FDR = "ACC-W910-RA-SINGLE-0001"
BRYAN = "ACC-W910-RA-SINGLE-0002"
EMERSON = "ACC-W910-RA-SINGLE-0003"

ITEMS = [
    # ---- 0801: FDR (complexity of the choices + rhetorical situation) --------------------------------
    Item(
        id="ACC-W910-CR-RA-0801", family="CR", grade="9-10", subskill_or_mode="analysis",
        qti_type="extended-text",
        stem=("You have 40 minutes. Read the passage from Franklin D. Roosevelt's First Inaugural Address "
              "carefully. Then write an essay that analyzes the rhetorical choices Roosevelt makes to lead "
              "a frightened nation. Do not catalog devices. Instead, analyze how his choices work together, "
              "and account for the tension he must manage between acknowledging fear and demanding "
              "confident action. Situate the choices in his rhetorical situation, and explain their effect. "
              "Support your analysis with specific evidence from the passage."),
        acc_tags=ACC,
        stimulus_ref=FDR,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
    # ---- 0802: BRYAN (complexity + audience) ---------------------------------------------------------
    Item(
        id="ACC-W910-CR-RA-0802", family="CR", grade="9-10", subskill_or_mode="analysis",
        qti_type="extended-text",
        stem=("You have 40 minutes. Read the passage from William Jennings Bryan's \"Cross of Gold\" speech "
              "carefully. Then write an essay that analyzes the rhetorical choices Bryan makes to move a "
              "divided convention. Go beyond naming appeals. Analyze how his choices interact, how he "
              "positions himself in relation to his audience, and what he risks in pressing his case so "
              "far. Explain the effect of the choices you identify, and situate them in his rhetorical "
              "situation. Support your analysis with specific evidence from the passage."),
        acc_tags=ACC,
        stimulus_ref=BRYAN,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
    # ---- 0803: EMERSON (complexity + purpose) --------------------------------------------------------
    Item(
        id="ACC-W910-CR-RA-0803", family="CR", grade="9-10", subskill_or_mode="analysis",
        qti_type="extended-text",
        stem=("You have 40 minutes. Read the passage from Ralph Waldo Emerson's essay \"Self-Reliance\" "
              "carefully. Then write an essay that analyzes the rhetorical choices Emerson makes to press "
              "his view of the individual on a reader. Do not restate his ideas. Analyze how his choices "
              "work together to make a demanding and even unsettling claim feel authoritative, and address "
              "the complexity of asking readers to trust themselves over the crowd. Explain the effect of "
              "the choices, and situate them in his purpose. Support your analysis with specific evidence "
              "from the passage."),
        acc_tags=ACC,
        stimulus_ref=EMERSON,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
    # ---- 0804: FDR, second prompt (shifts + how choices build on one another) ------------------------
    Item(
        id="ACC-W910-CR-RA-0804", family="CR", grade="9-10", subskill_or_mode="analysis",
        qti_type="extended-text",
        stem=("You have 40 minutes. Read the passage from Franklin D. Roosevelt's First Inaugural Address "
              "carefully. Then write an essay that analyzes how Roosevelt's rhetorical choices shift across "
              "the passage and build on one another to move the nation from fear toward resolve. Trace how "
              "one choice sets up the next rather than treating the choices as a list, and explain why the "
              "order and interaction matter to the effect. Support your analysis with specific evidence "
              "from the passage."),
        acc_tags=ACC,
        stimulus_ref=FDR,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
    # ---- 0805: BRYAN, second prompt (structure + figurative language in tension) ---------------------
    Item(
        id="ACC-W910-CR-RA-0805", family="CR", grade="9-10", subskill_or_mode="analysis",
        qti_type="extended-text",
        stem=("You have 40 minutes. Read the passage from William Jennings Bryan's \"Cross of Gold\" speech "
              "carefully. Then write an essay that analyzes how Bryan uses the structure of his argument "
              "and his figurative language together to intensify his appeal, and consider what that "
              "intensity costs him as well as what it wins. Explain how these choices act on the audience "
              "rather than restating his position, and account for the risk in the strategy. Support your "
              "analysis with specific evidence from the passage."),
        acc_tags=ACC,
        stimulus_ref=BRYAN,
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
