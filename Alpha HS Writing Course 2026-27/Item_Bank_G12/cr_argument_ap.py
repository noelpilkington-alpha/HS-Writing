"""
cr_argument_ap.py  -  G12 constructed-response (CR) SOURCE-FREE ARGUMENT essay prompts (AP Lang mastery tier).

Six extended-text argument prompts, each BINDING to one of the three NEW G12 source-free (prompt-only)
argument stimuli in Stimulus_Bank_G12. Modeled on the AP English Language argument FRQ (Q3): a general
prompt presents an abstract tension, and the student develops and defends an original position using
evidence from OWN knowledge, with NO provided passage. Scored on rc.ap. mode="argument".

The G12 tier foregrounds SOPHISTICATION (Row C) + sustained timed conditions: the stems demand a NUANCED
position (not a flat yes/no), attention to the so-what and to context, and genuine engagement with the
strongest competing perspective, all under a stated time limit.

G12-DISTINCT id range: CR-ARG-08xx (zero collision with G9 05xx / G10 00xx / G11 07xx).

Stimulus coverage (each of the 3 NEW G12 SFA-PROMPT ids used twice, 6 items total):
  ACC-W910-SFA-PROMPT-0004  what is lost when a society optimizes for efficiency -> 0801, 0804
  ACC-W910-SFA-PROMPT-0005  is doubt more valuable than certainty                -> 0802, 0805
  ACC-W910-SFA-PROMPT-0006  does genuine freedom require obligation to others     -> 0803, 0806

Each pair uses two angles: the first asks for a nuanced position that engages the strongest competing
perspective; the second presses the student to define terms, draw a principled line, and make the
significance (the so-what and its wider context) explicit. Runs each item through the item_contract QC
harness and prints "N/6 PASS". No em dashes.
"""
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from item_contract import Item, qc_item, qc_report

ACC = ["ACC.W.ARG.1", "ACC.W.ARG.2", "CCSS.W.11-12.1"]
PROV = {"copyright": "own_authored", "authored": "2026-07-09"}

EFFICIENCY = "ACC-W910-SFA-PROMPT-0004"
DOUBT = "ACC-W910-SFA-PROMPT-0005"
FREEDOM = "ACC-W910-SFA-PROMPT-0006"

ITEMS = [
    # ---- 0801: EFFICIENCY (nuanced position + competing perspective) ---------------------------------
    Item(
        id="ACC-W910-CR-ARG-0801", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("You have 40 minutes. Some argue that a society organized around efficiency quietly discards "
              "goods it cannot measure; others answer that the drive to do more with less has relieved real "
              "human suffering. Write an essay that develops a nuanced position on what, if anything, is "
              "lost when a society optimizes for efficiency. Argue from your own knowledge, using specific "
              "examples from your reading, studies, observation, or experience. Engage the strongest version "
              "of the view opposed to yours rather than a weak one, and make clear why the answer matters."),
        acc_tags=ACC,
        stimulus_ref=EFFICIENCY,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
    # ---- 0802: DOUBT vs CERTAINTY (nuanced position + competing perspective) -------------------------
    Item(
        id="ACC-W910-CR-ARG-0802", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("You have 40 minutes. Some hold that doubt keeps a mind honest and open to correction; others "
              "warn that doubt carried too far becomes paralysis, and that action requires conviction. Write "
              "an essay that develops a nuanced position on whether doubt is more valuable than certainty to "
              "a thinking person. Argue from your own knowledge, using specific examples from your reading, "
              "studies, observation, or experience. Take the opposing view seriously at its strongest, and "
              "make clear what is at stake in how a person answers."),
        acc_tags=ACC,
        stimulus_ref=DOUBT,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
    # ---- 0803: FREEDOM vs OBLIGATION (nuanced position + competing perspective) ----------------------
    Item(
        id="ACC-W910-CR-ARG-0803", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("You have 40 minutes. It is common to picture freedom as the absence of constraint, yet many "
              "thinkers argue that a person is most free when bound well, by promises and duties that give a "
              "life direction. Write an essay that develops a nuanced position on whether genuine freedom "
              "requires obligation to others. Argue from your own knowledge, using specific examples from "
              "your reading, studies, observation, or experience. Confront the strongest form of the view "
              "you reject, and explain why the question matters beyond the individual case."),
        acc_tags=ACC,
        stimulus_ref=FREEDOM,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
    # ---- 0804: EFFICIENCY, second prompt (define terms, draw the line, significance) -----------------
    Item(
        id="ACC-W910-CR-ARG-0804", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("You have 40 minutes. Efficiency is neither simply a virtue nor simply a loss. Write an essay "
              "that develops a position on where the line should fall between the efficiencies a society "
              "should pursue and the ones it should refuse. Argue from your own knowledge, using specific "
              "examples from your reading, studies, observation, or experience. Define what you mean by "
              "efficiency, qualify your position so that it holds even in the cases that seem to work "
              "against it, and situate the choice in the larger values it serves or sacrifices."),
        acc_tags=ACC,
        stimulus_ref=EFFICIENCY,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
    # ---- 0805: DOUBT vs CERTAINTY, second prompt (draw the line, significance) -----------------------
    Item(
        id="ACC-W910-CR-ARG-0805", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("You have 40 minutes. Doubt and certainty each serve a thinking person in some situations and "
              "fail in others. Write an essay that develops a position on when a person should hold to doubt "
              "and when the moment demands conviction instead. Argue from your own knowledge, using specific "
              "examples from your reading, studies, observation, or experience. Draw a principled line "
              "rather than splitting the difference, qualify it so that it survives the hardest cases, and "
              "explain why getting this balance right matters."),
        acc_tags=ACC,
        stimulus_ref=DOUBT,
        rubric_ref="rc.4trait",
        provenance=PROV,
    ),
    # ---- 0806: FREEDOM vs OBLIGATION, second prompt (define terms, draw the line, significance) -------
    Item(
        id="ACC-W910-CR-ARG-0806", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("You have 40 minutes. A free person owes some things to others and is entitled to refuse "
              "others. Write an essay that develops a position on how much obligation genuine freedom "
              "requires and where its demands should stop. Argue from your own knowledge, using specific "
              "examples from your reading, studies, observation, or experience. Define what you mean by "
              "freedom, qualify your position so that it holds even in the hardest cases you can imagine, "
              "and make clear why the line you draw matters for how people live together."),
        acc_tags=ACC,
        stimulus_ref=FREEDOM,
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
