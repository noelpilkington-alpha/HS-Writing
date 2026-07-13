"""
sr_conventions.py  -  G9 selected-response (SR) test-bank items for subskill "conventions".

20 auto-gradable editing items covering standard English grammar, usage, punctuation, spelling, and
capitalization in a short embedded student draft. G9 (English I) difficulty: single, clearly diagnosable
errors in short, plain draft sentences (simpler than the G10 bank). ACC.W.CONV.1 = grammar/usage
(CCSS.L.9-10.1); ACC.W.CONV.2 = capitalization/punctuation/spelling (CCSS.L.9-10.2).

Each item is an Item record validated against ../pipeline/item_contract.py. Every distractor carries a
rationale naming the misconception it targets. Some items include a "NO CHANGE" option; "NO CHANGE" is the
key on ACC-W910-SR-CONV-0509 and ACC-W910-SR-CONV-0514 (the sometimes-correct property across the bank).
Three items are qti_type="text-entry" (short constructed correction) with a model answer_key. No em dashes.

Run:  python sr_conventions.py   ->  prints per-item failures (if any) and "N/20 PASS".
"""
from __future__ import annotations
import os, sys

# make pipeline/ importable (item_contract itself adds its own dir for content_screen)
_HERE = os.path.dirname(os.path.abspath(__file__))
_PIPELINE = os.path.normpath(os.path.join(_HERE, "..", "pipeline"))
sys.path.insert(0, _PIPELINE)

from item_contract import Item, Option, qc_item, qc_report  # noqa: E402

PROV = {"copyright": "own_authored", "authored": "2026-07-09", "generator": "sr_conventions.py"}

ITEMS: list[Item] = [

    # 0001  subject-verb agreement (simple singular subject)
    Item(
        id="ACC-W910-SR-CONV-0501", family="SR", grade="9-10", subskill_or_mode="conventions",
        qti_type="choice",
        stem=("In the draft sentence 'My little brother walk to school every morning,' which is the best "
              "choice for the underlined word 'walk'?"),
        acc_tags=["ACC.W.CONV.1", "CCSS.L.9-10.1"],
        options=[
            Option("A", "NO CHANGE", False,
                   "uses the plural verb 'walk' with the singular subject 'brother'"),
            Option("B", "walks", True, "singular verb 'walks' agrees with the singular subject 'brother'"),
            Option("C", "walked", False, "shifts to past tense; the habitual 'every morning' needs the present"),
            Option("D", "are walking", False, "plural helping verb 'are' disagrees with singular 'brother'"),
        ],
        answer_key=["B"], provenance=PROV,
    ),

    # 0002  its vs it's (contraction mistaken for possessive)
    Item(
        id="ACC-W910-SR-CONV-0502", family="SR", grade="9-10", subskill_or_mode="conventions",
        qti_type="choice",
        stem=("In the draft sentence 'The dog wagged it's tail at the door,' which is the best choice for the "
              "underlined word 'it's'?"),
        acc_tags=["ACC.W.CONV.2", "CCSS.L.9-10.2"],
        options=[
            Option("A", "NO CHANGE", False,
                   "confuses the contraction 'it's' (it is) with the possessive needed here"),
            Option("B", "its", True, "possessive pronoun 'its' correctly shows the tail belongs to the dog"),
            Option("C", "its'", False, "invents a possessive apostrophe form of 'it' that does not exist"),
            Option("D", "it is", False, "expands the contraction, giving 'wagged it is tail,' which is wrong"),
        ],
        answer_key=["B"], provenance=PROV,
    ),

    # 0003  their / there / they're
    Item(
        id="ACC-W910-SR-CONV-0503", family="SR", grade="9-10", subskill_or_mode="conventions",
        qti_type="choice",
        stem=("In the draft sentence 'The players forgot there water bottles in the locker room,' which is "
              "the best choice for the underlined word 'there'?"),
        acc_tags=["ACC.W.CONV.2", "CCSS.L.9-10.2"],
        options=[
            Option("A", "NO CHANGE", False, "uses the place word 'there' where a possessive is needed"),
            Option("B", "they're", False, "uses the contraction 'they are,' which does not fit here"),
            Option("C", "thier", False, "misspells the possessive by reversing the 'i' and 'e'"),
            Option("D", "their", True, "possessive 'their' shows the bottles belong to the players"),
        ],
        answer_key=["D"], provenance=PROV,
    ),

    # 0004  your / you're
    Item(
        id="ACC-W910-SR-CONV-0504", family="SR", grade="9-10", subskill_or_mode="conventions",
        qti_type="choice",
        stem=("In the draft sentence 'I think your going to enjoy the movie tonight,' which is the best "
              "choice for the underlined word 'your'?"),
        acc_tags=["ACC.W.CONV.2", "CCSS.L.9-10.2"],
        options=[
            Option("A", "NO CHANGE", False,
                   "uses the possessive 'your' where the contraction 'you are' is needed"),
            Option("B", "you're", True, "contraction 'you are' correctly fits 'you are going to enjoy'"),
            Option("C", "youre", False, "leaves out the apostrophe in the contraction"),
            Option("D", "your'e", False, "places the apostrophe in the wrong spot in the contraction"),
        ],
        answer_key=["B"], provenance=PROV,
    ),

    # 0005  comma splice fixed with a period
    Item(
        id="ACC-W910-SR-CONV-0505", family="SR", grade="9-10", subskill_or_mode="conventions",
        qti_type="choice",
        stem=("In the draft sentence 'The bell rang, we walked to class,' which is the best choice for the "
              "underlined text 'rang, we'?"),
        acc_tags=["ACC.W.CONV.2", "CCSS.L.9-10.2"],
        options=[
            Option("A", "NO CHANGE", False,
                   "joins two complete sentences with only a comma (a comma splice)"),
            Option("B", "rang. We", True, "a period correctly ends the first complete sentence"),
            Option("C", "rang we", False, "removes all punctuation, creating a fused run-on"),
            Option("D", "rang, and, we", False, "adds an extra comma after 'and,' which is not needed"),
        ],
        answer_key=["B"], provenance=PROV,
    ),

    # 0006  missing comma after introductory dependent clause
    Item(
        id="ACC-W910-SR-CONV-0506", family="SR", grade="9-10", subskill_or_mode="conventions",
        qti_type="choice",
        stem=("In the draft sentence 'When the movie ended the crowd clapped loudly,' which is the best "
              "choice for the underlined text 'ended the'?"),
        acc_tags=["ACC.W.CONV.2", "CCSS.L.9-10.2"],
        options=[
            Option("A", "NO CHANGE", False, "leaves out the comma needed after an introductory clause"),
            Option("B", "ended, the", True,
                   "a comma correctly separates the introductory clause from the main clause"),
            Option("C", "ended; the", False,
                   "a semicolon cannot separate a dependent clause from the main clause"),
            Option("D", "ended: the", False, "a colon does not follow an introductory adverb clause"),
        ],
        answer_key=["B"], provenance=PROV,
    ),

    # 0007  singular possessive apostrophe
    Item(
        id="ACC-W910-SR-CONV-0507", family="SR", grade="9-10", subskill_or_mode="conventions",
        qti_type="choice",
        stem=("In the draft sentence 'My friends bike had a flat tire this morning,' which is the best choice "
              "for the underlined word 'friends'?"),
        acc_tags=["ACC.W.CONV.2", "CCSS.L.9-10.2"],
        options=[
            Option("A", "NO CHANGE", False, "leaves out the apostrophe needed to show possession"),
            Option("B", "friend's", True,
                   "singular possessive: the apostrophe shows the bike belongs to one friend"),
            Option("C", "friends'", False, "plural possessive, but the sentence names only one friend"),
            Option("D", "friends's", False, "adds an extra 's' after a plural noun that already ends in 's'"),
        ],
        answer_key=["B"], provenance=PROV,
    ),

    # 0008  verb tense consistency
    Item(
        id="ACC-W910-SR-CONV-0508", family="SR", grade="9-10", subskill_or_mode="conventions",
        qti_type="choice",
        stem=("In the draft sentence 'Yesterday we finished the poster and hang it on the wall,' which is the "
              "best choice for the underlined word 'hang'?"),
        acc_tags=["ACC.W.CONV.1", "CCSS.L.9-10.1"],
        options=[
            Option("A", "NO CHANGE", False, "present tense 'hang' clashes with the past-tense 'finished'"),
            Option("B", "hung", True, "past tense 'hung' keeps the sentence consistent with 'finished'"),
            Option("C", "hangs", False, "still present tense and disagrees with the plural subject 'we'"),
            Option("D", "will hang", False, "future tense clashes with the past-tense 'finished'"),
        ],
        answer_key=["B"], provenance=PROV,
    ),

    # 0009  pronoun case in a compound subject  ->  NO CHANGE is the key
    Item(
        id="ACC-W910-SR-CONV-0509", family="SR", grade="9-10", subskill_or_mode="conventions",
        qti_type="choice",
        stem=("In the draft sentence 'She and I studied for the quiz together,' which is the best choice for "
              "the underlined text 'She and I'?"),
        acc_tags=["ACC.W.CONV.1", "CCSS.L.9-10.1"],
        options=[
            Option("A", "NO CHANGE", True,
                   "both pronouns are subject forms, correct for the compound subject of 'studied'"),
            Option("B", "Her and I", False, "'Her' is an object form used incorrectly as a subject"),
            Option("C", "Her and me", False, "both are object forms used incorrectly as the subject"),
            Option("D", "She and me", False, "mixes a subject form and an object form in one compound subject"),
        ],
        answer_key=["A"], provenance=PROV,
    ),

    # 0010  then vs than (comparison)
    Item(
        id="ACC-W910-SR-CONV-0510", family="SR", grade="9-10", subskill_or_mode="conventions",
        qti_type="choice",
        stem=("In the draft sentence 'The blue backpack is bigger then the red one,' which is the best choice "
              "for the underlined word 'then'?"),
        acc_tags=["ACC.W.CONV.1", "CCSS.L.9-10.1"],
        options=[
            Option("A", "NO CHANGE", False, "uses the time word 'then' where a comparison word is needed"),
            Option("B", "than", True, "'than' correctly signals a comparison after 'bigger'"),
            Option("C", "that", False, "'that' does not signal the comparison between the two backpacks"),
            Option("D", "thenn", False, "misspelling of the word 'then'"),
        ],
        answer_key=["B"], provenance=PROV,
    ),

    # 0011  to / too (intensifier)
    Item(
        id="ACC-W910-SR-CONV-0511", family="SR", grade="9-10", subskill_or_mode="conventions",
        qti_type="choice",
        stem=("In the draft sentence 'The soup was to hot to eat right away,' which is the best choice for "
              "the underlined word 'to'?"),
        acc_tags=["ACC.W.CONV.2", "CCSS.L.9-10.2"],
        options=[
            Option("A", "NO CHANGE", False, "uses the preposition 'to' where the intensifier 'too' is needed"),
            Option("B", "too", True, "'too' correctly means excessively (too hot to eat)"),
            Option("C", "two", False, "the number word, which does not fit the meaning here"),
            Option("D", "to be", False, "adds a verb that does not fit the sentence"),
        ],
        answer_key=["B"], provenance=PROV,
    ),

    # 0012  affect (verb) vs effect (noun)
    Item(
        id="ACC-W910-SR-CONV-0512", family="SR", grade="9-10", subskill_or_mode="conventions",
        qti_type="choice",
        stem=("In the draft sentence 'Getting enough sleep can effect your mood the next day,' which is the "
              "best choice for the underlined word 'effect'?"),
        acc_tags=["ACC.W.CONV.1", "CCSS.L.9-10.1"],
        options=[
            Option("A", "NO CHANGE", False, "uses the noun 'effect' where an action verb is required"),
            Option("B", "affect", True, "verb 'affect' correctly follows 'can' and means to influence"),
            Option("C", "effects", False, "still the noun form, now plural; the sentence needs a verb"),
            Option("D", "affects", False, "correct root, but 'can' requires the base verb without the 's'"),
        ],
        answer_key=["B"], provenance=PROV,
    ),

    # 0013  spelling: receive (i before e rule)
    Item(
        id="ACC-W910-SR-CONV-0513", family="SR", grade="9-10", subskill_or_mode="conventions",
        qti_type="choice",
        stem=("In the draft sentence 'Every student will recieve a copy of the schedule,' which is the best "
              "choice for the underlined word 'recieve'?"),
        acc_tags=["ACC.W.CONV.2", "CCSS.L.9-10.2"],
        options=[
            Option("A", "NO CHANGE", False, "reverses 'ei'; the rule is 'i' before 'e' except after 'c'"),
            Option("B", "receive", True, "correct spelling: 'e' before 'i' after the letter 'c'"),
            Option("C", "receeve", False, "doubles the 'e' and drops the 'i' entirely"),
            Option("D", "receve", False, "leaves the 'i' out of the word completely"),
        ],
        answer_key=["B"], provenance=PROV,
    ),

    # 0014  subject-verb agreement with 'each'  ->  NO CHANGE is the key
    Item(
        id="ACC-W910-SR-CONV-0514", family="SR", grade="9-10", subskill_or_mode="conventions",
        qti_type="choice",
        stem=("In the draft sentence 'Each of the runners has a water bottle,' which is the best choice for "
              "the underlined word 'has'?"),
        acc_tags=["ACC.W.CONV.1", "CCSS.L.9-10.1"],
        options=[
            Option("A", "NO CHANGE", True, "singular verb 'has' agrees with the singular subject 'Each'"),
            Option("B", "have", False, "treats 'runners' as the subject; the subject is singular 'Each'"),
            Option("C", "have had", False, "plural and shifts to present perfect; disagrees with 'Each'"),
            Option("D", "having", False, "a participle, not a finite verb, so it cannot head the sentence"),
        ],
        answer_key=["A"], provenance=PROV,
    ),

    # 0015  capitalization of proper nouns (months)
    Item(
        id="ACC-W910-SR-CONV-0515", family="SR", grade="9-10", subskill_or_mode="conventions",
        qti_type="choice",
        stem=("In the draft sentence 'Our school play opens in march this year,' which is the best way to "
              "write the underlined word 'march'?"),
        acc_tags=["ACC.W.CONV.2", "CCSS.L.9-10.2"],
        options=[
            Option("A", "NO CHANGE", False, "leaves the month name lowercase, but months are proper nouns"),
            Option("B", "March", True, "the name of a month is a proper noun and is capitalized"),
            Option("C", "Marches", False, "capitalizes correctly but wrongly changes the month to plural"),
            Option("D", "Mar.", False, "abbreviates the month instead of writing the full capitalized name"),
        ],
        answer_key=["B"], provenance=PROV,
    ),

    # 0016  double negative (usage)
    Item(
        id="ACC-W910-SR-CONV-0516", family="SR", grade="9-10", subskill_or_mode="conventions",
        qti_type="choice",
        stem=("In the draft sentence 'We did not have no homework over the long weekend,' which is the best "
              "choice for the underlined text 'not have no'?"),
        acc_tags=["ACC.W.CONV.1", "CCSS.L.9-10.1"],
        options=[
            Option("A", "NO CHANGE", False, "uses a double negative ('not' plus 'no') in one clause"),
            Option("B", "not have any", True, "'not have any' removes the double negative and reads clearly"),
            Option("C", "not have none", False, "'none' is still a negative, keeping the double negative"),
            Option("D", "have not no", False, "reorders the words but keeps both negatives in the clause"),
        ],
        answer_key=["B"], provenance=PROV,
    ),

    # 0017  fused (run-on) sentence
    Item(
        id="ACC-W910-SR-CONV-0517", family="SR", grade="9-10", subskill_or_mode="conventions",
        qti_type="choice",
        stem=("In the draft sentence 'The rain stopped the game continued,' which is the best choice for the "
              "underlined text 'stopped the'?"),
        acc_tags=["ACC.W.CONV.2", "CCSS.L.9-10.2"],
        options=[
            Option("A", "NO CHANGE", False,
                   "two complete sentences run together with no punctuation (a fused sentence)"),
            Option("B", "stopped. The", True, "a period correctly ends the first complete sentence"),
            Option("C", "stopped, the", False, "a comma alone between the clauses creates a comma splice"),
            Option("D", "stopped the,", False, "the comma is misplaced and still fuses the two clauses"),
        ],
        answer_key=["B"], provenance=PROV,
    ),

    # 0018  a lot (spelling of two words as one)
    Item(
        id="ACC-W910-SR-CONV-0518", family="SR", grade="9-10", subskill_or_mode="conventions",
        qti_type="choice",
        stem=("In the draft sentence 'There were alot of people at the game,' which is the best choice for "
              "the underlined word 'alot'?"),
        acc_tags=["ACC.W.CONV.2", "CCSS.L.9-10.2"],
        options=[
            Option("A", "NO CHANGE", False, "'alot' is not a word; 'a lot' is always written as two words"),
            Option("B", "a lot", True, "'a lot' is correctly written as two separate words"),
            Option("C", "alott", False, "still one word and adds an extra 't'"),
            Option("D", "allot", False, "'allot' means to give out shares, not a large amount"),
        ],
        answer_key=["B"], provenance=PROV,
    ),

    # 0019  text-entry (SCR): fix subject-verb agreement
    Item(
        id="ACC-W910-SR-CONV-0519", family="SR", grade="9-10", subskill_or_mode="conventions",
        qti_type="text-entry",
        stem=("Rewrite the following draft sentence, correcting the subject-verb agreement error. "
              "Draft: 'The stack of books were on the table.'"),
        acc_tags=["ACC.W.CONV.1", "CCSS.L.9-10.1"],
        answer_key=["The stack of books was on the table."],
        provenance=PROV,
    ),

    # 0020  text-entry (SCR): fix a possessive apostrophe
    Item(
        id="ACC-W910-SR-CONV-0520", family="SR", grade="9-10", subskill_or_mode="conventions",
        qti_type="text-entry",
        stem=("Type the corrected form of the underlined word. In the draft sentence 'The teachers desk was "
              "covered in papers,' the possessive 'teachers' should be written as:"),
        acc_tags=["ACC.W.CONV.2", "CCSS.L.9-10.2"],
        answer_key=["teacher's"],
        provenance=PROV,
    ),
]


def main() -> int:
    passed = 0
    for it in ITEMS:
        r = qc_item(it)
        if r["passed"]:
            passed += 1
        else:
            print(qc_report(it))
            print()
    # bank-level sanity checks (noted in the L4 spec, not enforced per-item):
    nc_keys = [it.id for it in ITEMS
               if it.qti_type == "choice"
               and any(o.correct and o.text.strip().lower() == "no change" for o in it.options)]
    key_letters: dict[str, int] = {}
    for it in ITEMS:
        if it.qti_type == "choice":
            for k in it.answer_key:
                key_letters[k] = key_letters.get(k, 0) + 1
    print(f"NO CHANGE is the key on: {', '.join(nc_keys) if nc_keys else '(none)'}")
    print(f"answer-key letter spread (choice items): {dict(sorted(key_letters.items()))}")
    print(f"{passed}/{len(ITEMS)} PASS")
    return 0 if passed == len(ITEMS) else 1


if __name__ == "__main__":
    sys.exit(main())
