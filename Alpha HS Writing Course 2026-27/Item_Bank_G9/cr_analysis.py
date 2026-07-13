"""
cr_analysis.py  -  Four CR (constructed-response) text-dependent ANALYSIS essay prompts for the G9 bank.

Each item is an extended-text ANALYSIS prompt (mode="analysis") that BINDS to the single G9-test-bucket
ANALYSIS stimulus in Stimulus_Bank_G9, the public-domain setup excerpt of Guy de Maupassant's 1884 short
story "The Necklace" (ACC-W910-ANALYSIS-SINGLE-0005). Every prompt asks HOW the author builds meaning
(the move, its effect, its significance), never merely WHAT the text says (gap #22). Four distinct
analytical angles keep the four items from collapsing into one:
  0001  characterization + imagery + irony (develop Madame Loisel and the tone)
  0002  imagery + concrete detail (how her surroundings reveal her longing)
  0003  irony + narrative turn (the gap between what she wants and what she has)
  0004  word choice + sentence patterns (how the excerpt builds toward the closing discovery)

Runs each item through the item_contract QC harness (schema, acc_tags, cr_binding, rubric_config,
distractor_integrity, no_change_discipline, content, no_em_dash) and prints "N/4 PASS". No em dashes.
"""
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from item_contract import Item, qc_item, qc_report

ACC = ["ACC.W.INFO.6", "ACC.W.SRC.3", "CCSS.W.9-10.9"]
PROV = {"copyright": "own_authored", "authored": "2026-07-09"}
NECKLACE = "ACC-W910-ANALYSIS-SINGLE-0005"

ITEMS = [
    Item(
        id="ACC-W910-CR-ANLY-0501", family="CR", grade="9-10", subskill_or_mode="analysis",
        qti_type="extended-text",
        stem=("Analyze how Guy de Maupassant uses characterization, imagery, and irony to develop Madame "
              "Loisel and the tone of this excerpt from the setup of his 1884 short story \"The Necklace.\" "
              "Explain how these choices reveal her situation and inner life. Use specific evidence from the "
              "text to support your analysis."),
        acc_tags=ACC,
        stimulus_ref=NECKLACE,
        rubric_ref="rc.mcas",
        provenance=PROV,
    ),
    Item(
        id="ACC-W910-CR-ANLY-0502", family="CR", grade="9-10", subskill_or_mode="analysis",
        qti_type="extended-text",
        stem=("Analyze how Guy de Maupassant uses imagery and concrete detail to show what Madame Loisel "
              "longs for and how she feels about her own life in this excerpt from the setup of his 1884 "
              "short story \"The Necklace.\" Explain how these details shape the reader's understanding of "
              "her. Use specific evidence from the text to support your analysis."),
        acc_tags=ACC,
        stimulus_ref=NECKLACE,
        rubric_ref="rc.ohio",
        provenance=PROV,
    ),
    Item(
        id="ACC-W910-CR-ANLY-0503", family="CR", grade="9-10", subskill_or_mode="analysis",
        qti_type="extended-text",
        stem=("Analyze how Guy de Maupassant uses irony and the narrative turn near the end of this excerpt "
              "to sharpen the gap between what Madame Loisel wants and what she has, in this passage from "
              "the setup of his 1884 short story \"The Necklace.\" Explain how this choice develops the "
              "meaning of the excerpt. Use specific evidence from the text to support your analysis."),
        acc_tags=ACC,
        stimulus_ref=NECKLACE,
        rubric_ref="rc.mcas",
        provenance=PROV,
    ),
    Item(
        id="ACC-W910-CR-ANLY-0504", family="CR", grade="9-10", subskill_or_mode="analysis",
        qti_type="extended-text",
        stem=("Analyze how Guy de Maupassant uses word choice and sentence patterns to build this excerpt "
              "toward Madame Loisel's discovery of the diamond necklace in this passage from the setup of "
              "his 1884 short story \"The Necklace.\" Explain how these choices create that effect. Use "
              "specific evidence from the text to support your analysis."),
        acc_tags=ACC,
        stimulus_ref=NECKLACE,
        rubric_ref="rc.ohio",
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
