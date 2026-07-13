"""
cr_synthesis.py  -  G11 constructed-response (CR) SYNTHESIS-essay prompts for the writing test bank.

Six extended-text synthesis prompts, each BINDING to one of the three G11 SYNTHESIS SOURCE SETS in
Stimulus_Bank_G11. Modeled on the AP English Language synthesis FRQ (Q1) and the SBAC G11 multi-source
full-write: the student synthesizes evidence from AT LEAST THREE of the provided sources into ONE
original position on the debatable question, not a source-by-source summary. Scored on rc.ap.

MODE MAPPING NOTE: the item contract's CR_MODES = {"argument", "explanatory", "analysis"} does not
include "synthesis". Per the task's mapping rule, subskill_or_mode is set to "explanatory" for these
synthesis items (the gate would reject "synthesis"). The synthesis task shape lives in the stem +
the bound synthesis_set stimulus + rc.ap, not in the mode token.

Stimulus coverage (each of the 3 SYNTH-SET ids used twice, 6 items total):
  ACC-W910-SYNTH-SET-0001  renewable power grid   -> 0701, 0704
  ACC-W910-SYNTH-SET-0002  AI and the workforce   -> 0702, 0705
  ACC-W910-SYNTH-SET-0003  managing water scarcity-> 0703, 0706

Runs each item through the item_contract QC harness (schema, acc_tags, cr_binding, rubric_config,
content, no_em_dash) on run and prints "N/6 PASS". No em dashes.
"""
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from item_contract import Item, qc_item, qc_report

ACC = ["ACC.W.SRC.1", "ACC.W.INFO.2", "CCSS.W.11-12.7"]
PROV = {"copyright": "own_authored", "authored": "2026-07-09"}

GRID = "ACC-W910-SYNTH-SET-0001"
AI = "ACC-W910-SYNTH-SET-0002"
WATER = "ACC-W910-SYNTH-SET-0003"

ITEMS = [
    # ---- 0701: RENEWABLE GRID (feasibility framing) --------------------------------------------------
    Item(
        id="ACC-W910-CR-SYN-0701", family="CR", grade="9-10", subskill_or_mode="explanatory",
        qti_type="extended-text",
        stem=("The sources address one debatable question: can the United States power grid run mostly on "
              "renewable energy? Read the sources carefully. Then write an essay that synthesizes material "
              "from at least three of the sources and develops your own position on how far a shift toward "
              "renewable power can reasonably extend. Use the sources to support and develop your reasoning "
              "rather than summarizing each one in turn, and cite the sources you draw on."),
        acc_tags=ACC,
        stimulus_ref=GRID,
        rubric_ref="rc.ap",
        provenance=PROV,
    ),
    # ---- 0702: AI WORKFORCE (impact framing) ---------------------------------------------------------
    Item(
        id="ACC-W910-CR-SYN-0702", family="CR", grade="9-10", subskill_or_mode="explanatory",
        qti_type="extended-text",
        stem=("The sources address one debatable question: how will artificial intelligence reshape the "
              "American workforce? Read the sources carefully. Then write an essay that synthesizes material "
              "from at least three of the sources and develops your own position on what the shift toward "
              "artificial intelligence will mean for American workers. Draw on the sources to build a single "
              "line of reasoning rather than summarizing each source separately, and cite the sources you use."),
        acc_tags=ACC,
        stimulus_ref=AI,
        rubric_ref="rc.ap",
        provenance=PROV,
    ),
    # ---- 0703: WATER SCARCITY (policy framing) -------------------------------------------------------
    Item(
        id="ACC-W910-CR-SYN-0703", family="CR", grade="9-10", subskill_or_mode="explanatory",
        qti_type="extended-text",
        stem=("The sources address one debatable question: how should the United States manage water "
              "scarcity? Read the sources carefully. Then write an essay that synthesizes material from at "
              "least three of the sources and develops your own position on the approach the country should "
              "take to a shrinking water supply. Use the sources to advance your own argument rather than "
              "summarizing each in turn, and cite the sources you draw on."),
        acc_tags=ACC,
        stimulus_ref=WATER,
        rubric_ref="rc.ap",
        provenance=PROV,
    ),
    # ---- 0704: RENEWABLE GRID, second prompt (tradeoffs framing) -------------------------------------
    Item(
        id="ACC-W910-CR-SYN-0704", family="CR", grade="9-10", subskill_or_mode="explanatory",
        qti_type="extended-text",
        stem=("The sources address one debatable question: can the United States power grid run mostly on "
              "renewable energy? Read the sources carefully. Then write an essay that synthesizes material "
              "from at least three of the sources and develops your own position, weighing the benefits of a "
              "renewable grid against the practical obstacles the sources raise. Let the sources develop your "
              "reasoning rather than dictate a summary, and cite the sources you use."),
        acc_tags=ACC,
        stimulus_ref=GRID,
        rubric_ref="rc.ap",
        provenance=PROV,
    ),
    # ---- 0705: AI WORKFORCE, second prompt (evidence-limits framing) ---------------------------------
    Item(
        id="ACC-W910-CR-SYN-0705", family="CR", grade="9-10", subskill_or_mode="explanatory",
        qti_type="extended-text",
        stem=("The sources address one debatable question: how will artificial intelligence reshape the "
              "American workforce? Read the sources carefully. Then write an essay that synthesizes material "
              "from at least three of the sources and develops your own position on how much confidence the "
              "available evidence allows about the future of work. Use the sources to build and qualify your "
              "reasoning rather than summarizing each one, and cite the sources you draw on."),
        acc_tags=ACC,
        stimulus_ref=AI,
        rubric_ref="rc.ap",
        provenance=PROV,
    ),
    # ---- 0706: WATER SCARCITY, second prompt (priorities framing) ------------------------------------
    Item(
        id="ACC-W910-CR-SYN-0706", family="CR", grade="9-10", subskill_or_mode="explanatory",
        qti_type="extended-text",
        stem=("The sources address one debatable question: how should the United States manage water "
              "scarcity? Read the sources carefully. Then write an essay that synthesizes material from at "
              "least three of the sources and develops your own position on which uses of water the country "
              "should protect first when supplies run short. Use the sources to develop a single argument "
              "rather than summarizing each in turn, and cite the sources you use."),
        acc_tags=ACC,
        stimulus_ref=WATER,
        rubric_ref="rc.ap",
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
