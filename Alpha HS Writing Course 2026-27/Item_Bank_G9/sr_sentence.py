"""
sr_sentence.py  -  G9 selected-response test-bank items for the "sentence" subskill
(sentence structure and boundaries: fragments, run-ons, comma splices, sentence combining).

Standard: ACC.W.CONV.1 (CCSS.L.9-10.1). Family = SR (auto-gradable editing items, no stimulus binding).
G9 (English I) difficulty: short, plain draft sentences with a single clearly diagnosable boundary error.

Design notes (so the QC gates stay green):
  - Boundary-error items present the full draft sentence in the stem and give SHORT junction-rewrite
    options, so a literal "NO CHANGE" option stays length-balanced with the other choices.
  - Combining items give full-sentence options (naturally similar lengths, no NO CHANGE).
  - Every distractor carries a rationale = the misconception it captures.
  - "NO CHANGE" is the key on items 9 and 16 (a sometimes-correct discipline across the bank).
  - No em dashes; content is neutral and everyday.

Run:  python sr_sentence.py   ->   prints per-item PASS/FAIL and "N/16 PASS".
"""
from __future__ import annotations
import os, sys

# item_contract.py lives in ../pipeline; put it on the path, then import the contract + QC harness.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline"))
from item_contract import Item, Option, qc_item, qc_report  # noqa: E402

ACC = ["ACC.W.CONV.1", "CCSS.L.9-10.1"]
PROV = {"copyright": "own_authored", "authored": "2026-07-09", "subskill": "sentence"}


def _item(num, qti, stem, opts, key):
    return Item(
        id=f"ACC-W910-SR-SENT-{num:04d}", family="SR", grade="9-10",
        subskill_or_mode="sentence", qti_type=qti, stem=stem,
        acc_tags=list(ACC), options=opts, answer_key=key, provenance=dict(PROV),
    )


ITEMS = [

    # 1 - comma splice fixed with a period
    _item(501, "choice",
          ('Read the sentence and focus on the words in quotation marks. "The sun came out, we went '
           'outside to play." How should the underlined portion "out, we" be written?'),
          [Option("A", "NO CHANGE", False, "leaves a comma splice: two complete sentences joined by only a comma"),
           Option("B", "out. We", True, "a period correctly ends the first complete sentence"),
           Option("C", "out we", False, "deletes the comma, producing a fused run-on"),
           Option("D", "out; We", False, "uses a semicolon but wrongly capitalizes the next word")],
          ["B"]),

    # 2 - comma splice fixed with a semicolon
    _item(502, "inline-choice",
          ('"The library was quiet, everyone was studying for finals." How should "quiet, everyone" be '
           'written to link two closely related complete sentences with a single mark?'),
          [Option("A", "NO CHANGE", False, "comma splice: a comma alone cannot join two complete sentences"),
           Option("B", "quiet; everyone", True, "a semicolon correctly links the two related sentences"),
           Option("C", "quiet everyone", False, "fused run-on: no punctuation between the clauses"),
           Option("D", "quiet: everyone", False, "a colon does not correctly join two equal sentences here")],
          ["B"]),

    # 3 - fused run-on fixed with a period
    _item(503, "choice",
          ('"The movie was long we still enjoyed it." The underlined portion "long we" joins two complete '
           'sentences with no punctuation. How should it be written?'),
          [Option("A", "NO CHANGE", False, "fused run-on: two sentences run together with no punctuation"),
           Option("B", "long. We", True, "a period correctly separates the two complete sentences"),
           Option("C", "long, we", False, "adds only a comma, creating a comma splice"),
           Option("D", "long we,", False, "places the comma after the wrong word and still fuses the clauses")],
          ["B"]),

    # 4 - fused run-on fixed with comma + coordinating conjunction
    _item(504, "inline-choice",
          ('"The bus was late the driver apologized to us." Choose the best way to write "late the" so the '
           'two complete sentences are joined with a coordinating conjunction.'),
          [Option("A", "NO CHANGE", False, "fused run-on with no punctuation or conjunction"),
           Option("B", "late, so the", True, "a comma plus 'so' correctly joins the two sentences"),
           Option("C", "late, the", False, "comma splice: a comma with no conjunction cannot join two clauses"),
           Option("D", "late so the", False, "uses the conjunction but omits the required comma before it")],
          ["B"]),

    # 5 - fragment (dependent clause) attached to the main clause
    _item(505, "choice",
          ('Read the two word groups. "We stayed inside. Because it was raining hard." How should the '
           'boundary "inside. Because" be written so the dependent clause joins the main clause?'),
          [Option("A", "NO CHANGE", False, "leaves a sentence fragment: 'Because...' cannot stand alone"),
           Option("B", "inside because", True, "joining the clauses fixes the fragment and reads smoothly"),
           Option("C", "inside, Because", False, "adds a comma but keeps the capital, still stranding the clause"),
           Option("D", "inside; because", False, "a semicolon must join two complete sentences, not a fragment")],
          ["B"]),

    # 6 - fragment (missing verb) fixed
    _item(506, "choice",
          ('"The team practiced hard. Every player on the field." How should the boundary "hard. Every" be '
           'written to fix the fragment?'),
          [Option("A", "NO CHANGE", False, "'Every player on the field' is a fragment with no verb"),
           Option("B", "hard, and every player joined in", True, "adding a verb turns the fragment into a full clause"),
           Option("C", "hard every player on the field", False, "runs the fragment onto the clause with no punctuation"),
           Option("D", "hard. Every player on the field?", False, "adding a question mark does not supply the missing verb")],
          ["B"]),

    # 7 - combine two sentences with a subordinating conjunction (contrast)
    _item(507, "choice",
          ('Which choice best combines the two sentences into one, showing that the second idea contrasts '
           'with the first? "The test was hard. Most students passed it."'),
          [Option("A", "Although the test was hard, most students passed it.", True, "'although' correctly signals the contrast between the ideas"),
           Option("B", "The test was hard, so most students passed it.", False,
                  "'so' signals cause and effect, not the contrast the ideas require"),
           Option("C", "The test was hard, most students passed it.", False,
                  "joins two complete sentences with only a comma (comma splice)"),
           Option("D", "The test was hard and most students passing it.", False,
                  "'and most students passing it' turns the second clause into a fragment")],
          ["A"]),

    # 8 - combine two sentences with a coordinating conjunction (cause and effect)
    _item(508, "choice",
          ('Which choice best combines the two sentences into one, showing that the first idea causes the '
           'second? "The alarm went off. Everyone left the building."'),
          [Option("A", "The alarm went off, so everyone left the building.", True, "'so' correctly signals the cause-and-effect link"),
           Option("B", "The alarm went off, everyone left the building.", False,
                  "joins two complete sentences with only a comma (comma splice)"),
           Option("C", "The alarm went off everyone left the building.", False,
                  "runs the two clauses together with no punctuation (fused sentence)"),
           Option("D", "The alarm went off, but everyone left the building.", False,
                  "'but' signals contrast rather than the cause-and-effect relationship")],
          ["A"]),

    # 9 - NO CHANGE correct: compound sentence already correct (comma + coordinating conjunction)
    _item(509, "choice",
          ('"The rain stopped, and the sun came out." Focus on the portion "stopped, and the." How should '
           'it be written?'),
          [Option("A", "NO CHANGE", True, "a comma before 'and' correctly joins the two complete sentences"),
           Option("B", "stopped and the", False, "removes the comma required before 'and' joining two clauses"),
           Option("C", "stopped, the", False, "deletes the conjunction, leaving a comma splice"),
           Option("D", "stopped. And, the", False, "starts a new sentence with 'And,' and adds a needless comma")],
          ["A"]),

    # 10 - comma splice fixed by adding a coordinating conjunction
    _item(510, "inline-choice",
          ('"The store was closed, we drove to the next town." Choose the best way to write "closed, we" '
           'using a coordinating conjunction.'),
          [Option("A", "NO CHANGE", False, "comma splice: a comma alone cannot join two complete sentences"),
           Option("B", "closed, so we", True, "a comma plus 'so' correctly joins the two sentences"),
           Option("C", "closed so we", False, "uses the conjunction but omits the required comma"),
           Option("D", "closed. so we", False, "ends the sentence but fails to capitalize the new one")],
          ["B"]),

    # 11 - fragment beginning with 'Although' joined to its main clause
    _item(511, "choice",
          ('"Although the room was cold. We kept the window open." How should the boundary "cold. We" be '
           'written to fix the fragment?'),
          [Option("A", "NO CHANGE", False, "leaves 'Although...' as a fragment; it needs a main clause"),
           Option("B", "cold, we", True, "a comma joins the introductory clause to its main clause"),
           Option("C", "cold we", False, "joins the clauses with no punctuation, creating a run-on"),
           Option("D", "cold; we", False, "a semicolon must join two complete sentences, not a fragment")],
          ["B"]),

    # 12 - run-on fixed by subordinating one clause
    _item(512, "choice",
          ('"We left early we wanted to beat the traffic." Choose the best way to write "early we" so one '
           'clause becomes subordinate.'),
          [Option("A", "NO CHANGE", False, "fused run-on: two clauses with no punctuation or conjunction"),
           Option("B", "early because we", True, "'because' makes the second clause subordinate and fixes the run-on"),
           Option("C", "early, we", False, "a comma alone leaves a comma splice"),
           Option("D", "early we, because", False, "places the comma in the wrong clause, scrambling the boundary")],
          ["B"]),

    # 13 - comma splice fixed with a period (three plain clauses context)
    _item(513, "choice",
          ('"The dog barked, the cat ran away." Focus on the portion "barked, the." How should it be '
           'written as two complete sentences?'),
          [Option("A", "NO CHANGE", False, "comma splice: two complete sentences joined by only a comma"),
           Option("B", "barked. The", True, "a period correctly separates the two complete sentences"),
           Option("C", "barked the", False, "removes the comma, creating a fused run-on"),
           Option("D", "barked, The", False, "keeps the comma splice and wrongly capitalizes after a comma")],
          ["B"]),

    # 14 - combine by turning one clause into a relative clause
    _item(514, "choice",
          ('Which choice best combines the two sentences by turning the second into a clause that describes '
           'the coach? "The coach gave a speech. She had won three titles."'),
          [Option("A", "The coach, who had won three titles, gave a speech.", True, "the relative clause 'who...' correctly describes the coach"),
           Option("B", "The coach gave a speech, she had won three titles.", False,
                  "joins two complete sentences with only a comma (comma splice)"),
           Option("C", "The coach gave a speech and she had won three titles.", False,
                  "omits the comma before 'and' joining two complete sentences"),
           Option("D", "The coach gave a speech which had won three titles.", False,
                  "'which' wrongly refers to the speech instead of describing the coach")],
          ["A"]),

    # 15 - fused run-on fixed with a semicolon
    _item(515, "inline-choice",
          ('"The garden was full of flowers bees buzzed around every plant." Choose the best way to write '
           '"flowers bees" to link the two complete sentences with one mark.'),
          [Option("A", "NO CHANGE", False, "fused run-on: two complete sentences with no punctuation"),
           Option("B", "flowers; bees", True, "a semicolon correctly links the two related sentences"),
           Option("C", "flowers, bees", False, "a comma alone creates a comma splice"),
           Option("D", "flowers: bees", False, "a colon does not correctly join two equal sentences here")],
          ["B"]),

    # 16 - NO CHANGE correct: compound sentence correctly joined by a semicolon
    _item(516, "choice",
          ('"The trail was steep; the view was worth it." Focus on the portion "steep; the." How should it '
           'be written?'),
          [Option("A", "NO CHANGE", True, "a semicolon correctly joins the two related complete sentences"),
           Option("B", "steep, the", False, "a comma alone cannot join two complete sentences (comma splice)"),
           Option("C", "steep the", False, "removing punctuation fuses the two clauses into a run-on"),
           Option("D", "steep: the", False, "a colon wrongly signals a list or explanation, not two equal clauses")],
          ["A"]),
]


def main() -> int:
    passed = 0
    for it in ITEMS:
        r = qc_item(it)
        if r["passed"]:
            passed += 1
            print(f"[PASS] {it.id}")
        else:
            print(qc_report(it))
    print(f"\n{passed}/{len(ITEMS)} PASS")
    return 0 if passed == len(ITEMS) else 1


if __name__ == "__main__":
    sys.exit(main())
