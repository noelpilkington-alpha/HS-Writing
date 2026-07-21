"""
scr_writing.py  -  G9 SCR writing-domain short-constructed-response bank.

The student is shown a single flawed or improvable sentence and must REWRITE it while keeping the
original information/meaning. No stimulus is attached (these are sentence-level production items).
Family SCR, subtype "scr_writing", qti_type "text-entry": the contract requires NO options; answer_key
carries a MODEL correct rewrite (a text-entry item is externally/AI graded against the model plus the
task criterion, so the key is illustrative, not the only right answer). rubric_ref is always "rc.scr1".

Task types covered:
  - modifier_repair: fix a misplaced/dangling modifier, preserve intended meaning (migrated, verbatim).
  - sentence_combining: fuse two sentences into one clear sentence, keep all information.
  - precise_word_choice: replace vague wording with more precise language (knowledge of language).
  - revise_for_cohesion: rewrite so the second sentence connects cleanly, without clunky repetition.
  - transition: open the second sentence with a transition that shows its logical link to the first.

No em dashes. IDs ACC-W910-SCR-WRIT-0501..0520.

Run:  python scr_writing.py   ->   prints per-item QC then "N/N PASS".
"""
from __future__ import annotations
import os, sys

# import the contract from the sibling pipeline/ directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from item_contract import Item, qc_item, qc_report  # noqa: E402

ACC_CONV = ["ACC.W.CONV.1", "CCSS.L.9-10.1"]          # sentence construction / conventions
ACC_LANG = ["ACC.W.CONV.3", "CCSS.L.9-10.3"]          # precise word choice / knowledge of language
ACC_COH  = ["ACC.W.ARG.3", "CCSS.W.9-10.1c"]          # cohesion / transitions in revision
PROV = {"copyright": "own_authored", "authored": "2026-07-21"}


def scr(idnum, instruction, flawed, model, task_type, acc, note=""):
    """Build one writing-domain SCR (0-1, text-entry, no stimulus)."""
    stem = instruction + (f" ({note})" if note else "") + f'\n\nSentence: "{flawed}"'
    return Item(id=idnum, family="SCR", grade="9-10", subskill_or_mode="scr_writing",
                qti_type="text-entry", stem=stem, acc_tags=list(acc), options=[],
                answer_key=[model], rubric_ref="rc.scr1",
                provenance=dict(PROV, task_type=task_type))


ITEMS = [
    # --- migrated: modifier-repair (from sr_scr_modifier.py), 10 items, verbatim wording ---
    scr("ACC-W910-SCR-WRIT-0501",
        "Rewrite the sentence below to correct the dangling participle (the opening phrase does not "
        "describe the subject that follows). Keep the original intended meaning; change only what you "
        "must to make the modifier clearly and logically attach to the right word.",
        "Running to catch the bus, my backpack fell open.",
        "Running to catch the bus, I felt my backpack fall open.",
        "modifier_repair", ACC_CONV),
    scr("ACC-W910-SCR-WRIT-0502",
        "Rewrite the sentence below to correct the misplaced modifying phrase (it sits next to the wrong "
        "noun). Keep the original intended meaning; change only what you must to make the modifier clearly "
        "and logically attach to the right word.",
        "She gave a sandwich to the boy on a paper plate.",
        "She gave the boy a sandwich on a paper plate.",
        "modifier_repair", ACC_CONV),
    scr("ACC-W910-SCR-WRIT-0503",
        "Rewrite the sentence below to correct the misplaced adverb \"only\" (its position changes what it "
        "limits). Keep the original intended meaning; change only what you must to make the modifier "
        "clearly and logically attach to the right word.",
        "The team only lost one game all season.",
        "The team lost only one game all season.",
        "modifier_repair", ACC_CONV,
        note="Intended meaning: the team lost just a single game, no more."),
    scr("ACC-W910-SCR-WRIT-0504",
        "Rewrite the sentence below to correct the dangling modifier (the introductory phrase has no "
        "logical doer in the main clause). Keep the original intended meaning; change only what you must "
        "to make the modifier clearly and logically attach to the right word.",
        "After cleaning the kitchen, the floor looked shiny.",
        "After cleaning the kitchen, we saw that the floor looked shiny.",
        "modifier_repair", ACC_CONV),
    scr("ACC-W910-SCR-WRIT-0505",
        "Rewrite the sentence below to correct the misplaced participial phrase (it attaches to the wrong "
        "noun). Keep the original intended meaning; change only what you must to make the modifier clearly "
        "and logically attach to the right word.",
        "We saw a deer walking through the woods.",
        "Walking through the woods, we saw a deer.",
        "modifier_repair", ACC_CONV,
        note="Intended meaning: we were the ones walking through the woods."),
    scr("ACC-W910-SCR-WRIT-0506",
        "Rewrite the sentence below to correct the dangling participle (the opening phrase does not "
        "describe the subject that follows). Keep the original intended meaning; change only what you "
        "must to make the modifier clearly and logically attach to the right word.",
        "Tired after the game, the couch felt comfortable.",
        "Tired after the game, I found the couch comfortable.",
        "modifier_repair", ACC_CONV),
    scr("ACC-W910-SCR-WRIT-0507",
        "Rewrite the sentence below to correct the misplaced prepositional phrase (it lands next to the "
        "wrong word). Keep the original intended meaning; change only what you must to make the modifier "
        "clearly and logically attach to the right word.",
        "He almost read the whole book on the long trip.",
        "On the long trip, he read almost the whole book.",
        "modifier_repair", ACC_CONV,
        note="Intended meaning: he read nearly all of the book."),
    scr("ACC-W910-SCR-WRIT-0508",
        "Rewrite the sentence below to correct the dangling gerund phrase (the introductory action has no "
        "logical subject). Keep the original intended meaning; change only what you must to make the "
        "modifier clearly and logically attach to the right word.",
        "By practicing every day, my free throws improved.",
        "By practicing every day, I improved my free throws.",
        "modifier_repair", ACC_CONV),
    scr("ACC-W910-SCR-WRIT-0509",
        "Rewrite the sentence below to correct the misplaced modifying phrase (it sits next to the wrong "
        "noun). Keep the original intended meaning; change only what you must to make the modifier clearly "
        "and logically attach to the right word.",
        "The girl fed the cat wearing a red hat.",
        "The girl wearing a red hat fed the cat.",
        "modifier_repair", ACC_CONV),
    scr("ACC-W910-SCR-WRIT-0510",
        "Rewrite the sentence below to correct the dangling participle (the opening phrase does not "
        "describe the subject that follows). Keep the original intended meaning; change only what you "
        "must to make the modifier clearly and logically attach to the right word.",
        "Waiting at the bus stop, the rain started to fall.",
        "Waiting at the bus stop, we felt the rain start to fall.",
        "modifier_repair", ACC_CONV),

    # --- NEW: sentence-combining (3 items) ---
    scr("ACC-W910-SCR-WRIT-0511",
        "Combine the two sentences into one clear sentence, keeping all the information.",
        "The library extended its hours. Students now have more time to study after practice.",
        "The library extended its hours, so students now have more time to study after practice.",
        "sentence_combining", ACC_CONV),
    scr("ACC-W910-SCR-WRIT-0512",
        "Combine the two sentences into one sentence using a subordinate clause, keeping all the "
        "information.",
        "The debate team met every Friday. The team wanted to sharpen its arguments.",
        "The debate team met every Friday because it wanted to sharpen its arguments.",
        "sentence_combining", ACC_CONV),
    scr("ACC-W910-SCR-WRIT-0513",
        "Combine the two sentences into one clear sentence, keeping all the information.",
        "The city repaved Main Street. The repaving reduced the number of accidents.",
        "The city repaved Main Street, which reduced the number of accidents.",
        "sentence_combining", ACC_CONV),

    # --- NEW: precise word choice (3 items) ---
    scr("ACC-W910-SCR-WRIT-0514",
        "Rewrite the sentence, replacing the vague words \"really big effect\" with more precise language "
        "that fits its meaning.",
        "The new policy had a really big effect on how students got to school.",
        "The new policy sharply changed how students got to school.",
        "precise_word_choice", ACC_LANG),
    scr("ACC-W910-SCR-WRIT-0515",
        "Rewrite the sentence, replacing the vague word \"good\" with a more precise word that fits its "
        "meaning.",
        "The mayor gave a good speech about the new recycling program.",
        "The mayor gave a persuasive speech about the new recycling program.",
        "precise_word_choice", ACC_LANG),
    scr("ACC-W910-SCR-WRIT-0516",
        "Rewrite the sentence, replacing the vague phrase \"a lot of stuff\" with more precise language.",
        "The report included a lot of stuff about local water quality.",
        "The report included detailed data about local water quality.",
        "precise_word_choice", ACC_LANG),

    # --- NEW: revise-for-cohesion (2 items) ---
    scr("ACC-W910-SCR-WRIT-0517",
        "Rewrite the second sentence so it connects clearly to the first, without repeating words "
        "awkwardly.",
        "The city added bike lanes downtown. The city hoped the bike lanes downtown would cut traffic.",
        "The city added bike lanes downtown, hoping they would cut traffic.",
        "revise_for_cohesion", ACC_COH),
    scr("ACC-W910-SCR-WRIT-0518",
        "Rewrite the second sentence so it connects clearly to the first, without repeating words "
        "awkwardly.",
        "The school opened a new tutoring center. The new tutoring center helped students raise their "
        "grades.",
        "The school opened a new tutoring center, which helped students raise their grades.",
        "revise_for_cohesion", ACC_COH),

    # --- NEW: add/sharpen a transition (2 items) ---
    scr("ACC-W910-SCR-WRIT-0519",
        "Rewrite the second sentence to open with a transition that shows its logical link to the first.",
        "The team practiced every morning for months. They lost in the first round.",
        "The team practiced every morning for months. Even so, they lost in the first round.",
        "transition", ACC_COH),
    scr("ACC-W910-SCR-WRIT-0520",
        "Rewrite the second sentence to open with a transition that shows its logical link to the first.",
        "The volunteers cleaned the entire park by noon. The event was a clear success.",
        "The volunteers cleaned the entire park by noon. As a result, the event was a clear success.",
        "transition", ACC_COH),
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
