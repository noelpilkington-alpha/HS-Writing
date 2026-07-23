"""
cr_rhetorical_analysis.py  -  G11 constructed-response (CR) RHETORICAL-ANALYSIS essay prompts.

Six extended-text rhetorical-analysis prompts, each BINDING to one of the three G11 single-passage
rhetorical-analysis stimuli in Stimulus_Bank_G11 (public-domain speeches/essay). Modeled on the AP
English Language rhetorical analysis FRQ (Q2): the student analyzes HOW the writer builds meaning
through rhetorical CHOICES (appeals, structure, diction, tone, figurative language), never merely
restating WHAT the passage argues. Scored on rc.ap. mode="analysis" (accepted by CR_MODES).

Stimulus coverage (each of the 3 RA-SINGLE ids used twice, 6 items total):
  ACC-W910-RA-SINGLE-0001  FDR, First Inaugural Address (1933)   -> 0701, 0704
  ACC-W910-RA-SINGLE-0002  Bryan, "Cross of Gold" speech (1896)  -> 0702, 0705
  ACC-W910-RA-SINGLE-0003  Emerson, "Self-Reliance" (1841)       -> 0703, 0706

Two analytical angles keep the paired items from collapsing: the first of each pair asks for a broad
analysis of the choices that build the writer's purpose; the second narrows to a named cluster of
devices (appeals / structure / diction and figurative language). Runs each item through the
item_contract QC harness and prints "N/6 PASS". No em dashes.
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
    # ---- 0701: FDR (broad choices -> purpose) --------------------------------------------------------
    Item(
        id="ACC-W910-CR-RA-0701", family="CR", grade="9-10", subskill_or_mode="analysis",
        qti_type="extended-text",
        stem=("Read the passage from Franklin D. Roosevelt's First Inaugural Address carefully. Then write "
              "an essay that analyzes the rhetorical choices Roosevelt makes to achieve his purpose with a "
              "nation in crisis. Focus on how he builds meaning and moves his audience, not simply on what "
              "he says. Support your analysis with specific evidence from the passage and explain the effect "
              "of the choices you identify."),
        acc_tags=ACC,
        stimulus_ref=FDR,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
    # ---- 0702: BRYAN (broad choices -> purpose) ------------------------------------------------------
    Item(
        id="ACC-W910-CR-RA-0702", family="CR", grade="9-10", subskill_or_mode="analysis",
        qti_type="extended-text",
        stem=("Read the passage from William Jennings Bryan's \"Cross of Gold\" speech carefully. Then write "
              "an essay that analyzes the rhetorical choices Bryan makes to persuade his audience. Focus on "
              "how he shapes his argument and appeals to his listeners, not simply on the position he takes. "
              "Support your analysis with specific evidence from the passage and explain the effect of the "
              "choices you identify."),
        acc_tags=ACC,
        stimulus_ref=BRYAN,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
    # ---- 0703: EMERSON (broad choices -> purpose) ----------------------------------------------------
    Item(
        id="ACC-W910-CR-RA-0703", family="CR", grade="9-10", subskill_or_mode="analysis",
        qti_type="extended-text",
        stem=("Read the passage from Ralph Waldo Emerson's essay \"Self-Reliance\" carefully. Then write an "
              "essay that analyzes the rhetorical choices Emerson makes to advance his view of the "
              "individual. Focus on how he develops and presses his ideas on the reader, not simply on what "
              "those ideas are. Support your analysis with specific evidence from the passage and explain "
              "the effect of the choices you identify."),
        acc_tags=ACC,
        stimulus_ref=EMERSON,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
    # ---- 0704: FDR, second prompt (appeals + tone) ---------------------------------------------------
    Item(
        id="ACC-W910-CR-RA-0704", family="CR", grade="9-10", subskill_or_mode="analysis",
        qti_type="extended-text",
        stem=("Read the passage from Franklin D. Roosevelt's First Inaugural Address carefully. Then write "
              "an essay that analyzes how Roosevelt uses appeals to his audience and shifts in tone to steady "
              "the nation and prepare it to act. Explain how these choices work on the listener rather than "
              "restating his message. Support your analysis with specific evidence from the passage."),
        acc_tags=ACC,
        stimulus_ref=FDR,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
    # ---- 0705: BRYAN (structure + figurative language) -----------------------------------------------
    Item(
        id="ACC-W910-CR-RA-0705", family="CR", grade="9-10", subskill_or_mode="analysis",
        qti_type="extended-text",
        stem=("Read the passage from William Jennings Bryan's \"Cross of Gold\" speech carefully. Then write "
              "an essay that analyzes how Bryan uses the structure of his argument and figurative language to "
              "intensify his appeal. Explain how these choices shape the audience's response rather than "
              "restating his position. Support your analysis with specific evidence from the passage."),
        acc_tags=ACC,
        stimulus_ref=BRYAN,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
    # ---- 0706: EMERSON (diction + sentence style) ----------------------------------------------------
    Item(
        id="ACC-W910-CR-RA-0706", family="CR", grade="9-10", subskill_or_mode="analysis",
        qti_type="extended-text",
        stem=("Read the passage from Ralph Waldo Emerson's essay \"Self-Reliance\" carefully. Then write an "
              "essay that analyzes how Emerson uses diction and sentence style to make his call for "
              "self-trust feel urgent and authoritative. Explain how these choices act on the reader rather "
              "than restating his ideas. Support your analysis with specific evidence from the passage."),
        acc_tags=ACC,
        stimulus_ref=EMERSON,
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
