"""
cr_source_free_argument.py  -  G11 constructed-response (CR) SOURCE-FREE ARGUMENT essay prompts.

Six extended-text argument prompts, each BINDING to one of the three G11 source-free (prompt-only)
argument stimuli in Stimulus_Bank_G11. Modeled on the AP English Language argument FRQ (Q3): a general
prompt presents an idea or tension, and the student develops and defends an original position using
evidence from OWN knowledge (reading, studies, observation, or experience), with NO provided passage.
Scored on rc.ap. mode="argument" (accepted by CR_MODES).

Stimulus coverage (each of the 3 SFA-PROMPT ids used twice, 6 items total):
  ACC-W910-SFA-PROMPT-0001  tradition vs. progress          -> 0701, 0704
  ACC-W910-SFA-PROMPT-0002  individual freedom vs. community-> 0702, 0705
  ACC-W910-SFA-PROMPT-0003  ambition vs. contentment        -> 0703, 0706

Each pair uses two argumentative angles: the first asks the student to defend a position and address
the strongest opposing view; the second asks the student to draw a line or qualify their claim so it
holds under pressure. Runs each item through the item_contract QC harness and prints "N/6 PASS".
No em dashes.
"""
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from item_contract import Item, qc_item, qc_report

ACC = ["ACC.W.ARG.1", "CCSS.W.11-12.1"]
PROV = {"copyright": "own_authored", "authored": "2026-07-09"}

TRAD = "ACC-W910-SFA-PROMPT-0001"
FREEDOM = "ACC-W910-SFA-PROMPT-0002"
AMBITION = "ACC-W910-SFA-PROMPT-0003"

ITEMS = [
    # ---- 0701: TRADITION vs PROGRESS (defend + counter) ----------------------------------------------
    Item(
        id="ACC-W910-CR-SFA-0701", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("Some argue that inherited customs carry a wisdom no single generation can match; others hold "
              "that meaningful advance demands a deliberate break with tradition. Write an essay that develops "
              "a position on whether genuine progress requires breaking with tradition. Argue from your own "
              "knowledge, drawing on specific examples from your reading, studies, observation, or "
              "experience, and address the strongest objection to your view."),
        acc_tags=ACC,
        stimulus_ref=TRAD,
        rubric_ref="rc.ap",
        provenance=PROV,
    ),
    # ---- 0702: INDIVIDUAL vs COMMUNITY (defend + counter) --------------------------------------------
    Item(
        id="ACC-W910-CR-SFA-0702", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("Communities prize individual freedom, yet there are moments when a personal liberty is asked "
              "to give way to the welfare of the group. Write an essay that develops a position on when, if "
              "ever, individual freedom should yield to the community good. Argue from your own knowledge, "
              "drawing on specific examples from your reading, studies, observation, or experience, and "
              "address the strongest objection to your view."),
        acc_tags=ACC,
        stimulus_ref=FREEDOM,
        rubric_ref="rc.ap",
        provenance=PROV,
    ),
    # ---- 0703: AMBITION vs CONTENTMENT (defend + counter) --------------------------------------------
    Item(
        id="ACC-W910-CR-SFA-0703", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("Societies often celebrate ambition as the engine of invention and reform, while others argue "
              "that contentment is the rarer and more valuable achievement. Write an essay that develops a "
              "position on whether ambition is more valuable than contentment. Argue from your own knowledge, "
              "drawing on specific examples from your reading, studies, observation, or experience, and "
              "address the strongest objection to your view."),
        acc_tags=ACC,
        stimulus_ref=AMBITION,
        rubric_ref="rc.ap",
        provenance=PROV,
    ),
    # ---- 0704: TRADITION vs PROGRESS, second prompt (draw the line) ----------------------------------
    Item(
        id="ACC-W910-CR-SFA-0704", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("People disagree about when a society should hold to its traditions and when it should break "
              "with them. Write an essay that develops a position on where the line should fall between "
              "preserving tradition and pursuing progress. Argue from your own knowledge, using specific "
              "examples from your reading, studies, observation, or experience, and qualify your position so "
              "that it holds even in the cases that seem to work against it."),
        acc_tags=ACC,
        stimulus_ref=TRAD,
        rubric_ref="rc.ap",
        provenance=PROV,
    ),
    # ---- 0705: INDIVIDUAL vs COMMUNITY, second prompt (draw the line) --------------------------------
    Item(
        id="ACC-W910-CR-SFA-0705", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("A free society must decide how much it can ask of the individual for the sake of the group. "
              "Write an essay that develops a position on where the limit of that demand should lie. Argue "
              "from your own knowledge, using specific examples from your reading, studies, observation, or "
              "experience, and qualify your position so that it holds even in the hardest cases you can "
              "imagine."),
        acc_tags=ACC,
        stimulus_ref=FREEDOM,
        rubric_ref="rc.ap",
        provenance=PROV,
    ),
    # ---- 0706: AMBITION vs CONTENTMENT, second prompt (draw the line) --------------------------------
    Item(
        id="ACC-W910-CR-SFA-0706", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("Ambition can build a life or consume it, and contentment can bring peace or breed "
              "complacency. Write an essay that develops a position on how a person should balance ambition "
              "and contentment in a life well lived. Argue from your own knowledge, using specific examples "
              "from your reading, studies, observation, or experience, and qualify your position so that it "
              "holds even in the cases that seem to challenge it."),
        acc_tags=ACC,
        stimulus_ref=AMBITION,
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
