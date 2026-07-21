"""
scr_writing.py  -  G10 SCR writing-domain short-constructed-response bank.

The STAAR every-year short-constructed-response item: the student is shown a single flawed sentence
(misplaced modifier, dangling modifier, or awkward construction) and must REWRITE it correctly while
PRESERVING the original intended meaning. No stimulus is attached (these are sentence-level production
items).

Family SCR, subtype "scr_writing", qti_type "text-entry": the contract requires NO options; answer_key
carries a MODEL correct rewrite (a text-entry item is externally/AI graded against the model plus the
meaning-preservation criterion, so the key is illustrative, not the only right answer). rubric_ref is
always "rc.scr1".

Task type: modifier_repair (migrated from sr_scr_modifier.py, verbatim wording).

No em dashes. IDs ACC-W910-SCR-WRIT-1001..1012.

Run:  python scr_writing.py   ->   prints per-item QC then "N/12 PASS".
"""
from __future__ import annotations
import os, sys

# import the contract from the sibling pipeline/ directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from item_contract import Item, qc_item, qc_report  # noqa: E402

ACC = ["ACC.W.CONV.1", "ACC.W.CONV.2", "CCSS.L.9-10.1"]
PROV = {"copyright": "own_authored", "authored": "2026-07-21"}


def scr(idnum, flaw_kind, flawed, model, note=""):
    """Build one modifier-repair SCR text-entry item (no stimulus, no options)."""
    instruction = (
        f"Rewrite the sentence below to correct the {flaw_kind}. "
        f"Keep the original intended meaning; change only what you must to make the "
        f"modifier clearly and logically attach to the right word."
    )
    if note:
        instruction += f" ({note})"
    stem = f'{instruction}\n\nFlawed sentence: "{flawed}"'
    return Item(id=idnum, family="SCR", grade="9-10", subskill_or_mode="scr_writing",
                qti_type="text-entry", stem=stem, acc_tags=list(ACC), options=[],
                answer_key=[model], rubric_ref="rc.scr1",
                provenance=dict(PROV, task_type="modifier_repair"))


ITEMS = [
    scr(
        "ACC-W910-SCR-WRIT-1001",
        "dangling participle (the opening phrase does not describe the subject that follows)",
        "Walking home from practice, the sunset looked beautiful.",
        "Walking home from practice, I thought the sunset looked beautiful.",
    ),
    scr(
        "ACC-W910-SCR-WRIT-1002",
        "dangling modifier (the introductory phrase has no logical doer in the main clause)",
        "After finishing the experiment, the lab was cleaned by the students.",
        "After finishing the experiment, the students cleaned the lab.",
    ),
    scr(
        "ACC-W910-SCR-WRIT-1003",
        'misplaced adverb "only" (its position changes what it limits)',
        "The store only sells shoes on weekends.",
        "The store sells shoes only on weekends.",
        note="Intended meaning: the shoes are sold on weekends and at no other time.",
    ),
    scr(
        "ACC-W910-SCR-WRIT-1004",
        'misplaced adverb "almost" (its position changes what it limits)',
        "The teacher almost graded every essay before dinner.",
        "The teacher graded almost every essay before dinner.",
        note="Intended meaning: nearly all of the essays were graded, not that grading nearly happened.",
    ),
    scr(
        "ACC-W910-SCR-WRIT-1005",
        "misplaced modifying phrase (it sits next to the wrong noun)",
        "She returned the shirt to the store with a stain.",
        "She returned the stained shirt to the store.",
    ),
    scr(
        "ACC-W910-SCR-WRIT-1006",
        "dangling infinitive phrase (no agent in the main clause can perform the action)",
        "To win the science fair, a strong hypothesis is needed.",
        "To win the science fair, a student needs a strong hypothesis.",
    ),
    scr(
        "ACC-W910-SCR-WRIT-1007",
        "dangling gerund phrase (the introductory action has no logical subject)",
        "By studying every night, my grades improved.",
        "By studying every night, I improved my grades.",
    ),
    scr(
        "ACC-W910-SCR-WRIT-1008",
        "misplaced participial phrase (it attaches to the wrong noun)",
        "We watched the eagle soar over the canyon sitting on the bench.",
        "Sitting on the bench, we watched the eagle soar over the canyon.",
    ),
    scr(
        "ACC-W910-SCR-WRIT-1009",
        "dangling participle (the opening phrase does not describe the subject that follows)",
        "Exhausted after the long hike, the tent was a welcome sight.",
        "Exhausted after the long hike, the campers found the tent a welcome sight.",
    ),
    scr(
        "ACC-W910-SCR-WRIT-1010",
        "misplaced prepositional phrase (it lands next to the wrong verb)",
        "The chef described how to bake bread on the morning news.",
        "On the morning news, the chef described how to bake bread.",
    ),
    scr(
        "ACC-W910-SCR-WRIT-1011",
        "misplaced participial phrase (it describes the wrong noun and reverses who acts)",
        "Barking loudly, the mail carrier was frightened by the dog.",
        "The mail carrier was frightened by the dog barking loudly.",
    ),
    scr(
        "ACC-W910-SCR-WRIT-1012",
        "dangling participle (the opening phrase does not describe the subject that follows)",
        "Having studied all week, the test seemed easy to Maria.",
        "Having studied all week, Maria found the test easy.",
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
