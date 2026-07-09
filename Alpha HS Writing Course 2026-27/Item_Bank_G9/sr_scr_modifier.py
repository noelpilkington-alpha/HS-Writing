"""
sr_scr_modifier.py  -  G9 SR/SCR proof-set: modifier-repair with meaning-preservation.

The short-constructed-response item: the student is shown a flawed sentence (misplaced modifier,
dangling modifier, or awkward construction) and must REWRITE it correctly while PRESERVING the original
intended meaning. G9 (English I) difficulty: short, everyday sentences with a single, clearly visible
modifier fault.

Family SR, subskill "scr", qti_type "text-entry". For text-entry the contract requires no options;
answer_key carries a MODEL correct rewrite (a text-entry item is externally/AI graded against the model
plus the meaning-preservation criterion, so the key is illustrative, not the only right answer).

ACC.W.CONV.1 (sentence construction/conventions) + CCSS.L.9-10.1. No em dashes. IDs 0001-0010.

Run:  python sr_scr_modifier.py   ->   prints per-item QC then "N/10 PASS".
"""
from __future__ import annotations
import os, sys

# import the contract from the sibling pipeline/ directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from item_contract import Item, Option, qc_item, qc_report  # noqa: E402

ACC = ["ACC.W.CONV.1", "CCSS.L.9-10.1"]
PROV = {"copyright": "own_authored", "authored": "2026-07-09", "item_type": "scr_modifier_repair"}


def scr(idnum: str, flaw_kind: str, flawed: str, model: str, note: str = "") -> Item:
    """Build one modifier-repair SCR text-entry item."""
    instruction = (
        f"Rewrite the sentence below to correct the {flaw_kind}. "
        f"Keep the original intended meaning; change only what you must to make the "
        f"modifier clearly and logically attach to the right word."
    )
    if note:
        instruction += f" ({note})"
    stem = f'{instruction}\n\nFlawed sentence: "{flawed}"'
    return Item(
        id=idnum,
        family="SR",
        grade="9-10",
        subskill_or_mode="scr",
        qti_type="text-entry",
        stem=stem,
        acc_tags=list(ACC),
        options=[],                 # text-entry: no selected-response options
        answer_key=[model],         # a MODEL correct rewrite
        provenance=dict(PROV),
    )


ITEMS = [
    scr(
        "ACC-W910-SR-SCR-0501",
        "dangling participle (the opening phrase does not describe the subject that follows)",
        "Running to catch the bus, my backpack fell open.",
        "Running to catch the bus, I felt my backpack fall open.",
    ),
    scr(
        "ACC-W910-SR-SCR-0502",
        "misplaced modifying phrase (it sits next to the wrong noun)",
        "She gave a sandwich to the boy on a paper plate.",
        "She gave the boy a sandwich on a paper plate.",
    ),
    scr(
        "ACC-W910-SR-SCR-0503",
        'misplaced adverb "only" (its position changes what it limits)',
        "The team only lost one game all season.",
        "The team lost only one game all season.",
        note="Intended meaning: the team lost just a single game, no more.",
    ),
    scr(
        "ACC-W910-SR-SCR-0504",
        "dangling modifier (the introductory phrase has no logical doer in the main clause)",
        "After cleaning the kitchen, the floor looked shiny.",
        "After cleaning the kitchen, we saw that the floor looked shiny.",
    ),
    scr(
        "ACC-W910-SR-SCR-0505",
        "misplaced participial phrase (it attaches to the wrong noun)",
        "We saw a deer walking through the woods.",
        "Walking through the woods, we saw a deer.",
        note="Intended meaning: we were the ones walking through the woods.",
    ),
    scr(
        "ACC-W910-SR-SCR-0506",
        "dangling participle (the opening phrase does not describe the subject that follows)",
        "Tired after the game, the couch felt comfortable.",
        "Tired after the game, I found the couch comfortable.",
    ),
    scr(
        "ACC-W910-SR-SCR-0507",
        "misplaced prepositional phrase (it lands next to the wrong word)",
        "He almost read the whole book on the long trip.",
        "On the long trip, he read almost the whole book.",
        note="Intended meaning: he read nearly all of the book.",
    ),
    scr(
        "ACC-W910-SR-SCR-0508",
        "dangling gerund phrase (the introductory action has no logical subject)",
        "By practicing every day, my free throws improved.",
        "By practicing every day, I improved my free throws.",
    ),
    scr(
        "ACC-W910-SR-SCR-0509",
        "misplaced modifying phrase (it sits next to the wrong noun)",
        "The girl fed the cat wearing a red hat.",
        "The girl wearing a red hat fed the cat.",
    ),
    scr(
        "ACC-W910-SR-SCR-0510",
        "dangling participle (the opening phrase does not describe the subject that follows)",
        "Waiting at the bus stop, the rain started to fall.",
        "Waiting at the bus stop, we felt the rain start to fall.",
    ),
]


def main() -> int:
    passed = 0
    for it in ITEMS:
        qc_item(it)
        print(qc_report(it))
        print()
        if it.qc["passed"]:
            passed += 1
    print(f"{passed}/{len(ITEMS)} PASS")
    return 0 if passed == len(ITEMS) else 1


if __name__ == "__main__":
    sys.exit(main())
