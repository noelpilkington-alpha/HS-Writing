"""
sr_language.py  -  14 selected-response (SR) items for the G9 "language" subskill.

Scope: knowledge of language / STYLE, at an English-I (G9) reading level:
  - word-choice precision (say what you mean with the exact word)
  - concision (fewest words that keep the meaning)
  - register / tone (formal, academic, objective vs informal / slangy)
  - sentence variety (combine choppy sentences, vary syntax for effect)

Each item embeds a short student draft and asks for the most precise word, the most
concise revision, the option that best matches a formal/academic register, or the
best-varied sentence. 4 options; one correct; every distractor carries a real
misconception rationale (wordy / imprecise / wrong register / informal / fragment /
meaning-changing). acc_tags = ["ACC.W.CONV.3", "ACC.W.ARG.4", "CCSS.L.9-10.3"].

CONCISION LENGTH-LEAK NOTE (QC gate_distractor_integrity):
  The correct concise revision is naturally short. The gate FAILS an item whose correct
  option is >25% shorter than the SHORTEST distractor (a test-savvy student would just
  pick the shortest option). To defuse the leak WITHOUT bloating the correct answer, each
  concision item includes ONE short distractor that is concise-but-wrong (it drops needed
  meaning or reverses the logic, e.g. "Though" for "Because", "Someday" for "Currently").
  That short distractor is also pedagogically real: concision is the fewest words that KEEP
  the meaning, so a terse-but-meaning-changing option is exactly the trap to teach.

Run: python sr_language.py  ->  prints per-item pass and "N/14 PASS".
"""
from __future__ import annotations
import os
import sys

# item_contract.py lives in ../pipeline relative to this file.
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "pipeline"))

from item_contract import Item, Option, qc_item, qc_report  # noqa: E402

ACC = ["ACC.W.CONV.3", "ACC.W.ARG.4", "CCSS.L.9-10.3"]
PROV = {"copyright": "own_authored", "authored": "2026-07-09"}


def mk(idn, stem, opts, key):
    return Item(
        id=idn, family="SR", grade="9-10", subskill_or_mode="language",
        qti_type="choice", stem=stem, acc_tags=list(ACC),
        options=opts, answer_key=key, provenance=dict(PROV),
    )


ITEMS = [

    # ---- PRECISION (word choice) --------------------------------------------
    mk(
        "ACC-W910-SR-LANG-0501",
        ("A student is revising a science report. In the sentence 'The strong wind really "
         "messed up the old footbridge,' which replacement for 'really messed up' is the "
         "most precise and best suited to a formal report?"),
        [
            Option("A", "weakened the supports of", True,
                   "precise: names the specific damage and keeps a formal register"),
            Option("B", "did a number on", False,
                   "informal idiom; imprecise about what was actually damaged"),
            Option("C", "totally wrecked", False,
                   "informal intensifier; overstates and never specifies the damage"),
            Option("D", "had a bad effect on the whole structure of", False,
                   "wordy and still vague about how the bridge was damaged"),
        ],
        ["A"],
    ),

    mk(
        "ACC-W910-SR-LANG-0502",
        ("In the sentence 'The new plan will help fix the traffic problem,' which "
         "replacement for 'fix' is the most precise for a claim a writer can support?"),
        [
            Option("A", "reduce", True,
                   "precise: claims a partial improvement that evidence can actually back"),
            Option("B", "solve", False,
                   "overstates; implies the problem is completely gone"),
            Option("C", "deal with", False,
                   "informal and vague about the actual effect"),
            Option("D", "take care of", False,
                   "informal idiom; imprecise about the result"),
        ],
        ["A"],
    ),

    mk(
        "ACC-W910-SR-LANG-0503",
        ("In the sentence 'The report gives information about the causes of coral "
         "bleaching,' which replacement for 'gives information about' is the most precise?"),
        [
            Option("A", "explains", True,
                   "precise verb naming what the report does with the causes"),
            Option("B", "talks about", False,
                   "informal and vague; 'talks' suits speech, not a written report"),
            Option("C", "covers", False,
                   "vague; does not say the report actually makes the causes clear"),
            Option("D", "gives some details related to", False,
                   "wordy and still vague about what the report does"),
        ],
        ["A"],
    ),

    mk(
        "ACC-W910-SR-LANG-0504",
        ("In the sentence 'The coach said the team did good in the final game,' which "
         "replacement for 'did good' is the most precise and correct?"),
        [
            Option("A", "played well", True,
                   "precise and correct: 'well' is the adverb that describes how they played"),
            Option("B", "did real good", False,
                   "still uses 'good' as an adverb, which is not standard here"),
            Option("C", "was awesome", False,
                   "informal and vague about what the team actually did"),
            Option("D", "put on a pretty decent kind of show", False,
                   "wordy and still vague about the team's performance"),
        ],
        ["A"],
    ),

    # ---- CONCISION -----------------------------------------------------------
    mk(
        "ACC-W910-SR-LANG-0505",
        ("Which revision of the underlined phrase is the most concise while keeping the "
         "original meaning? Draft: 'Due to the fact that the trail was closed, the group "
         "changed its route.' Underlined: 'Due to the fact that'"),
        [
            Option("A", "Because", True,
                   "concise causal connector that keeps the meaning"),
            Option("B", "Due to the fact of the reason that", False,
                   "wordy and redundant; stacks two ways of naming a cause"),
            Option("C", "On account of the fact that", False,
                   "wordy filler for a simple cause"),
            Option("D", "Though", False,
                   "concise but reverses the logic to a contrast; changes the meaning"),
        ],
        ["A"],
    ),

    mk(
        "ACC-W910-SR-LANG-0506",
        ("Which revision of the underlined portion is the most concise without losing "
         "meaning? Draft: 'The team came to the conclusion that the plan should change.' "
         "Underlined: 'came to the conclusion that'"),
        [
            Option("A", "concluded that", True,
                   "one precise verb replaces the wordy phrase"),
            Option("B", "came to the final conclusion that", False,
                   "still wordy; 'final' adds nothing"),
            Option("C", "arrived at the conclusion that", False,
                   "wordy synonym for the same phrase"),
            Option("D", "guessed that", False,
                   "concise but changes the meaning; a conclusion is not a guess"),
        ],
        ["A"],
    ),

    mk(
        "ACC-W910-SR-LANG-0507",
        ("Which revision of the underlined portion is the most concise while keeping the "
         "meaning? Draft: 'At this point in time, the club has enough members to compete.' "
         "Underlined: 'At this point in time'"),
        [
            Option("A", "Currently", True,
                   "one adverb replaces the five-word filler phrase"),
            Option("B", "At the present moment in time", False,
                   "wordy; three ways of saying 'now' in a row"),
            Option("C", "As of right now at this time", False,
                   "wordy and redundant"),
            Option("D", "Someday", False,
                   "concise but changes the meaning to a future time"),
        ],
        ["A"],
    ),

    mk(
        "ACC-W910-SR-LANG-0508",
        ("Which revision of the underlined portion is the most concise without changing "
         "the meaning? Draft: 'The team won in spite of the fact that two players were "
         "hurt.' Underlined: 'in spite of the fact that'"),
        [
            Option("A", "although", True,
                   "one concise connector keeps the concession relationship"),
            Option("B", "regardless of the fact that", False,
                   "wordy filler for a simple concession"),
            Option("C", "in spite of the fact of how", False,
                   "wordy and garbled; adds 'of how' for no reason"),
            Option("D", "because", False,
                   "concise but reverses the logic to a cause; changes the meaning"),
        ],
        ["A"],
    ),

    # ---- REGISTER / TONE -----------------------------------------------------
    mk(
        "ACC-W910-SR-LANG-0509",
        ("A student is drafting the opening of a class essay. Which version of the "
         "underlined sentence best matches a formal, academic register? Draft: 'This "
         "essay is gonna talk about why the city should build more bike lanes.'"),
        [
            Option("A", "This essay argues that the city should build more bike lanes.", True,
                   "formal register; states a clear claim without slang"),
            Option("B", "This essay is gonna talk about why the city needs way more bike lanes.", False,
                   "informal: contraction 'gonna' and slang 'way more'"),
            Option("C", "I am just gonna go over some reasons the city should add bike lanes.", False,
                   "informal and tentative; casual 'just gonna go over'"),
            Option("D", "So basically the city really ought to get around to adding bike lanes.", False,
                   "conversational fillers ('so basically', 'get around to')"),
        ],
        ["A"],
    ),

    mk(
        "ACC-W910-SR-LANG-0510",
        ("A student is writing a formal email to the principal. Which version of the "
         "underlined sentence best fits a formal, respectful register? Draft: 'Hey, I "
         "wanna know if the library can stay open later.'"),
        [
            Option("A", "I am writing to ask whether the library could stay open later.", True,
                   "formal, polite, and clear request"),
            Option("B", "Hey, I wanna know if the library can stay open later.", False,
                   "informal greeting and contraction ('wanna'); too casual"),
            Option("C", "Can you guys keep the library open late? That would be awesome.", False,
                   "casual address ('you guys') and slang ('awesome')"),
            Option("D", "I was just kind of wondering if maybe the library might stay open.", False,
                   "wordy and tentative; hedging weakens the request"),
        ],
        ["A"],
    ),

    mk(
        "ACC-W910-SR-LANG-0511",
        ("In a class research paper, which version of the underlined sentence best matches "
         "a formal, objective register? Draft: 'Honestly, the results were kind of "
         "surprising to a lot of people.'"),
        [
            Option("A", "The results were unexpected for many of the students who ran the test.", True,
                   "objective and formal; drops the personal aside and vague quantifier"),
            Option("B", "Honestly, the results were kind of surprising to a lot of people.", False,
                   "informal aside ('honestly') and vague hedges ('kind of', 'a lot of')"),
            Option("C", "To be real, those results kind of shocked a whole bunch of folks.", False,
                   "slang ('to be real', 'a whole bunch of folks'); too casual"),
            Option("D", "The results, which nobody really saw coming at all, were surprising.", False,
                   "wordy and conversational; buries the point in an aside"),
        ],
        ["A"],
    ),

    mk(
        "ACC-W910-SR-LANG-0512",
        ("A student is writing a formal argument essay. Which version of the underlined "
         "sentence best fits an academic register? Draft: 'Kids these days are super glued "
         "to their phones all day long.'"),
        [
            Option("A", "Many teenagers now spend a large part of their day using smartphones.", True,
                   "formal and specific; neutral academic word choice"),
            Option("B", "Kids these days are super glued to their phones all day long.", False,
                   "slang ('kids these days', 'super glued'); too casual"),
            Option("C", "Teens are basically always on their phones, like, all the time.", False,
                   "conversational fillers ('basically', 'like'); repeats itself"),
            Option("D", "It is a well known thing that young people are on phones a whole lot now.", False,
                   "wordy and vague ('a whole lot', 'a well known thing')"),
        ],
        ["A"],
    ),

    # ---- SENTENCE VARIETY ----------------------------------------------------
    mk(
        "ACC-W910-SR-LANG-0513",
        ("A student wrote two short, choppy sentences: 'The robotics team met after "
         "school. The team practiced for the contest.' Which revision best combines them "
         "into a single, varied sentence?"),
        [
            Option("A", "After school, the robotics team met to practice for the contest.", True,
                   "combines both ideas and opens with a variety-adding introductory phrase"),
            Option("B", "The robotics team met after school and the team practiced for the contest for the contest.", False,
                   "wordy and repetitive; repeats 'for the contest'"),
            Option("C", "The robotics team met after school, they practiced for the contest.", False,
                   "joins two independent clauses with only a comma (comma splice)"),
            Option("D", "Meeting after school, practicing for the contest.", False,
                   "concise but lacks a main subject and verb; a fragment"),
        ],
        ["A"],
    ),

    mk(
        "ACC-W910-SR-LANG-0514",
        ("A paragraph reads: 'The museum opened a new exhibit. The exhibit shows local "
         "artists. The artists use recycled materials.' Which revision best combines these "
         "into one clear, varied sentence?"),
        [
            Option("A", "The museum's new exhibit shows local artists who use recycled materials.", True,
                   "combines all three ideas with a subordinate clause for variety"),
            Option("B", "The museum opened a new exhibit and it shows local artists and they use recycled stuff.", False,
                   "strings clauses together with repeated 'and'; wordy and dull"),
            Option("C", "The museum opened a new exhibit, it shows local artists, they use recycled materials.", False,
                   "comma splices join three independent clauses incorrectly"),
            Option("D", "Showing local artists who use recycled materials.", False,
                   "concise but a fragment; no main subject and verb"),
        ],
        ["A"],
    ),

]


def main() -> int:
    assert len(ITEMS) == 14, f"expected 14 items, got {len(ITEMS)}"
    ids = [it.id for it in ITEMS]
    assert len(set(ids)) == len(ids), "duplicate item ids"

    npass = 0
    for it in ITEMS:
        r = qc_item(it)
        if r["passed"]:
            npass += 1
        else:
            print(qc_report(it))
            print()

    print(f"{npass}/14 PASS")
    return 0 if npass == 14 else 1


if __name__ == "__main__":
    sys.exit(main())
