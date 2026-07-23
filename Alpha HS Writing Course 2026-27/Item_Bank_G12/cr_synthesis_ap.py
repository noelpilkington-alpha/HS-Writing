"""
cr_synthesis_ap.py  -  G12 constructed-response (CR) SYNTHESIS-essay prompts (AP Lang mastery tier).

Five extended-text synthesis prompts that REUSE the three G11 SYNTHESIS SOURCE SETS in Stimulus_Bank_G11
(the G12 tier rides on G11 stimuli; the NEW dimension is SOPHISTICATION + sustained timed conditions, not
new sources). Modeled on the AP English Language synthesis FRQ (Q1) scored on rc.ap, where the top of Row B
(Evidence & Commentary, 0-4) and Row C (Sophistication, 0-1) reward a response that situates the debate in a
broader context, holds the tension across sources in view, and explains significance rather than summarizing.

MODE MAPPING NOTE: the item contract's CR_MODES = {"argument", "explanatory", "analysis"} does not include
"synthesis". Per the mapping rule, subskill_or_mode is set to "explanatory" for these synthesis items. The
synthesis task shape lives in the stem + the bound synthesis_set stimulus + rc.ap, not in the mode token.

G12-DISTINCT id range: CR-SYN-08xx (zero collision with G9 05xx / G10 00xx / G11 07xx).

Stimulus coverage (5 items across the 3 reused G11 SYNTH-SET ids):
  ACC-W910-SYNTH-SET-0001  renewable power grid    -> 0801, 0804
  ACC-W910-SYNTH-SET-0002  AI and the workforce    -> 0802, 0805
  ACC-W910-SYNTH-SET-0003  managing water scarcity -> 0803

Runs each item through the item_contract QC harness and prints "N/5 PASS". No em dashes.
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
    # ---- 0801: RENEWABLE GRID (significance / so-what) -----------------------------------------------
    Item(
        id="ACC-W910-CR-SYN-0801", family="CR", grade="9-10", subskill_or_mode="explanatory",
        qti_type="extended-text",
        stem=("You have 40 minutes to read the sources and write. The sources address one debatable "
              "question: can the United States power grid run mostly on renewable energy? Read them "
              "carefully. Then write an essay that synthesizes material from at least three of the sources "
              "and develops your own position on how far a shift toward renewable power can reasonably "
              "extend. Do not summarize the sources in turn. Instead, put them in conversation with one "
              "another, and make clear why the answer matters, what larger question about risk, cost, and "
              "public trust it turns on, and cite the sources you draw on."),
        acc_tags=ACC,
        stimulus_ref=GRID,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
    # ---- 0802: AI WORKFORCE (tension across sources) -------------------------------------------------
    Item(
        id="ACC-W910-CR-SYN-0802", family="CR", grade="9-10", subskill_or_mode="explanatory",
        qti_type="extended-text",
        stem=("You have 40 minutes to read the sources and write. The sources address one debatable "
              "question: how will artificial intelligence reshape the American workforce? Read them "
              "carefully. Then write an essay that synthesizes material from at least three of the sources "
              "and develops your own position on what the shift toward artificial intelligence will mean "
              "for American workers. Bring the sources into genuine tension rather than lining them up in "
              "agreement, weigh where they genuinely conflict, and explain what is at stake in choosing "
              "between them. Cite the sources you use."),
        acc_tags=ACC,
        stimulus_ref=AI,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
    # ---- 0803: WATER SCARCITY (situate in broader context) -------------------------------------------
    Item(
        id="ACC-W910-CR-SYN-0803", family="CR", grade="9-10", subskill_or_mode="explanatory",
        qti_type="extended-text",
        stem=("You have 40 minutes to read the sources and write. The sources address one debatable "
              "question: how should the United States manage water scarcity? Read them carefully. Then "
              "write an essay that synthesizes material from at least three of the sources and develops "
              "your own position on the approach the country should take to a shrinking water supply. "
              "Situate the debate in the broader tension between short-term relief and long-term "
              "stewardship, use the sources to advance a single line of reasoning rather than summarizing "
              "each in turn, and cite the sources you draw on."),
        acc_tags=ACC,
        stimulus_ref=WATER,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
    # ---- 0804: RENEWABLE GRID, second prompt (competing perspectives + significance) -----------------
    Item(
        id="ACC-W910-CR-SYN-0804", family="CR", grade="9-10", subskill_or_mode="explanatory",
        qti_type="extended-text",
        stem=("You have 40 minutes to read the sources and write. The sources address one debatable "
              "question: can the United States power grid run mostly on renewable energy? Read them "
              "carefully. Then write an essay that synthesizes material from at least three of the sources "
              "and develops your own position, weighing the strongest case the optimists make against the "
              "most serious obstacles the skeptics raise. Do not settle for a middle that ignores both. "
              "Explain why the disagreement itself is revealing, and let the sources develop your reasoning "
              "rather than dictate a summary. Cite the sources you use."),
        acc_tags=ACC,
        stimulus_ref=GRID,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
    # ---- 0805: AI WORKFORCE, second prompt (limits of the evidence + so-what) ------------------------
    Item(
        id="ACC-W910-CR-SYN-0805", family="CR", grade="9-10", subskill_or_mode="explanatory",
        qti_type="extended-text",
        stem=("You have 40 minutes to read the sources and write. The sources address one debatable "
              "question: how will artificial intelligence reshape the American workforce? Read them "
              "carefully. Then write an essay that synthesizes material from at least three of the sources "
              "and develops your own position on how much confidence the available evidence actually "
              "allows about the future of work. Interrogate what the sources can and cannot show, qualify "
              "your reasoning where the evidence thins, and explain why the limits of the evidence matter "
              "for anyone deciding what to do now. Cite the sources you draw on."),
        acc_tags=ACC,
        stimulus_ref=AI,
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
