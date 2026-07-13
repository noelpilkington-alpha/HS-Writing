"""
cr_explanatory.py  -  6 constructed-response EXPLANATORY essay items for the G9 test bank.

Each item is a CR extended-text prompt (mode="explanatory") that BINDS to one of the four
single-source informational stimuli in the G9 test bucket of Stimulus_Bank_G9 (each stimulus used
at least once):
  ACC-W910-INFO-SINGLE-0006  ocean tides    ("The Rhythm of the Tides")
  ACC-W910-INFO-SINGLE-0007  earthquakes    ("When the Ground Slips")
  ACC-W910-INFO-SINGLE-0008  hurricanes     ("How a Hurricane Is Born")
  ACC-W910-INFO-SINGLE-0009  honeybees      ("The Work of the Honeybee")

Prompts are varied: several target the controlling idea / how the article develops it; several
target SIGNIFICANCE / "so what" (why the topic matters) to close gap #22. Every prompt requires
specific evidence FROM THE ARTICLE, per the STAAR/MCAS single-source informational model.

Runs every item through the item_contract QC harness and prints "N/6 PASS". No em dashes.
"""
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from item_contract import Item, qc_item, qc_report

ACC = ["ACC.W.INFO.1", "ACC.W.INFO.2", "CCSS.W.9-10.2"]
PROV = {"copyright": "own_authored", "authored": "2026-07-09"}

ITEMS = [
    # 0001 - tides - controlling idea (cause + pattern)
    Item(
        id="ACC-W910-CR-INFO-0501", family="CR", grade="9-10",
        subskill_or_mode="explanatory", qti_type="extended-text",
        stem=("Read the article \"The Rhythm of the Tides.\" Then write a well-organized informational "
              "composition that uses specific evidence from the article to explain what causes ocean tides, "
              "how often they occur, and why their timing shifts a little each day."),
        acc_tags=ACC,
        stimulus_ref="ACC-W910-INFO-SINGLE-0006", rubric_ref="rc.mcas",
        provenance=dict(PROV, note="controlling idea: cause + timing pattern"),
    ),
    # 0002 - earthquakes - controlling idea (cause + measurement)
    Item(
        id="ACC-W910-CR-INFO-0502", family="CR", grade="9-10",
        subskill_or_mode="explanatory", qti_type="extended-text",
        stem=("Read the article \"When the Ground Slips.\" Then write a well-organized informational "
              "composition that uses specific evidence from the article to explain what causes earthquakes "
              "and how scientists measure their size after they strike."),
        acc_tags=ACC,
        stimulus_ref="ACC-W910-INFO-SINGLE-0007", rubric_ref="rc.staar",
        provenance=dict(PROV, note="controlling idea: cause + measurement"),
    ),
    # 0003 - hurricanes - controlling idea (form + rank + track)
    Item(
        id="ACC-W910-CR-INFO-0503", family="CR", grade="9-10",
        subskill_or_mode="explanatory", qti_type="extended-text",
        stem=("Read the article \"How a Hurricane Is Born.\" Then write a well-organized informational "
              "composition that uses specific evidence from the article to explain how hurricanes form, how "
              "forecasters rank their strength, and how they are tracked."),
        acc_tags=ACC,
        stimulus_ref="ACC-W910-INFO-SINGLE-0008", rubric_ref="rc.staar",
        provenance=dict(PROV, note="controlling idea: formation + ranking + tracking"),
    ),
    # 0004 - honeybees - controlling idea (hive + pollination + food supply)
    Item(
        id="ACC-W910-CR-INFO-0504", family="CR", grade="9-10",
        subskill_or_mode="explanatory", qti_type="extended-text",
        stem=("Read the article \"The Work of the Honeybee.\" Then write a well-organized informational "
              "composition that uses specific evidence from the article to explain how a honeybee hive "
              "works, how bees pollinate crops, and why the health of honeybees matters to the food supply."),
        acc_tags=ACC,
        stimulus_ref="ACC-W910-INFO-SINGLE-0009", rubric_ref="rc.staar",
        provenance=dict(PROV, note="controlling idea: hive + pollination + food supply"),
    ),
    # 0005 - honeybees - significance / "so what" (gap #22)
    Item(
        id="ACC-W910-CR-INFO-0505", family="CR", grade="9-10",
        subskill_or_mode="explanatory", qti_type="extended-text",
        stem=("The article \"The Work of the Honeybee\" reports that about one mouthful in three of our diet "
              "benefits from honeybee pollination. Write a well-organized informational composition that "
              "uses specific evidence from the article to explain why a decline in honeybees would matter to "
              "ordinary people."),
        acc_tags=ACC,
        stimulus_ref="ACC-W910-INFO-SINGLE-0009", rubric_ref="rc.mcas",
        provenance=dict(PROV, note="significance / so-what framing"),
    ),
    # 0006 - hurricanes - significance / "so what" (gap #22)
    Item(
        id="ACC-W910-CR-INFO-0506", family="CR", grade="9-10",
        subskill_or_mode="explanatory", qti_type="extended-text",
        stem=("Using specific evidence from the article \"How a Hurricane Is Born,\" write a well-organized "
              "informational composition that explains why understanding how hurricanes form and how they "
              "are tracked matters for the people who live in their path."),
        acc_tags=ACC,
        stimulus_ref="ACC-W910-INFO-SINGLE-0008", rubric_ref="rc.mcas",
        provenance=dict(PROV, note="significance / so-what framing"),
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
