"""
sr_organization.py  -  16 selected-response items for the G9 subskill "organization"
(organization & cohesion: transitions, topic sentences, logical order / sentence placement).

Contract: mirrors ../pipeline/item_contract.py (family="SR", grade="9-10",
subskill_or_mode="organization", qti_type in {"choice","inline-choice"}). Every item carries a short
embedded draft written at an English-I (G9) reading level (shorter sentences, simpler topics than the G10
bank). The stem asks for the best transition, the best topic sentence, or the best placement / order of a
sentence. 3-4 options, exactly the key marked correct, each distractor a real-misconception rationale.

acc_tags: argument drafts carry ["ACC.W.ARG.3", "CCSS.W.9-10.1"]; informational drafts carry
["ACC.W.INFO.3", "CCSS.W.9-10.2"] (organization rides both the argument and the informational spine).
Own-authored; embedded drafts are illustrative, not fact-bearing. No em dashes.

Item 5 keeps its existing transition, so its "NO CHANGE" option is the KEY (part of the bank-level rule
that NO CHANGE is sometimes correct). Its options are short transitions, so the length-leak gate stays clear.

Run: python sr_organization.py  ->  prints per-item QC + "N/16 PASS".
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from item_contract import Item, Option, qc_item, qc_report  # noqa: E402

ARG = ["ACC.W.ARG.3", "CCSS.W.9-10.1"]
INFO = ["ACC.W.INFO.3", "CCSS.W.9-10.2"]
PROV = {"copyright": "own_authored", "authored": "2026-07-09"}


def sr(idnum, qti, stem, options, key, tags):
    return Item(
        id=f"ACC-W910-SR-ORG-{idnum:04d}", family="SR", grade="9-10",
        subskill_or_mode="organization", qti_type=qti, stem=stem,
        acc_tags=list(tags), options=options, answer_key=key, provenance=dict(PROV),
    )


ITEMS = []

# ---- Transitions (items 1-6) ------------------------------------------------

ITEMS.append(sr(501, "inline-choice",
    "Read the paragraph. Our class started a lunchtime recycling bin last month. ____ the trash we send to "
    "the dumpster has already gone down. Which transition best fills the blank?",
    [
        Option("A", "As a result,", True,
               "correct: the smaller trash pile is the outcome of the new bin, so a result signal fits"),
        Option("B", "However,", False,
               "signals a contrast, but the second sentence continues the same idea instead of opposing it"),
        Option("C", "For example,", False,
               "signals an illustration of a general claim, but this sentence reports a consequence"),
        Option("D", "Meanwhile,", False,
               "signals two things happening at once, but the drop in trash follows from the bin"),
    ], ["A"], ARG))

ITEMS.append(sr(502, "inline-choice",
    "Read the paragraph. Bike helmets are cheap and easy to find in stores. ____ many riders still skip "
    "them on short trips around the block. Which transition best fills the blank?",
    [
        Option("A", "However,", True,
               "correct: it marks the gap between how easy helmets are and the riders who skip them"),
        Option("B", "Therefore,", False,
               "signals a result, but skipping helmets is the opposite of what easy access predicts"),
        Option("C", "In addition,", False,
               "signals another point on the same side, but this sentence pushes the other way"),
        Option("D", "For instance,", False,
               "signals an example, but the second sentence raises a contrast, not an example"),
    ], ["A"], INFO))

ITEMS.append(sr(503, "inline-choice",
    "Read the paragraph. Walking to school saves money on gas. ____ it wakes students up before class even "
    "starts. Which transition best fills the blank?",
    [
        Option("A", "In addition,", True,
               "correct: the second sentence adds a second benefit alongside the first"),
        Option("B", "However,", False,
               "signals a contrast, but both sentences name benefits that point the same way"),
        Option("C", "For example,", False,
               "signals an example, but waking up is a separate benefit, not an example of saving gas"),
        Option("D", "As a result,", False,
               "signals cause and effect, but waking up does not result from saving money on gas"),
    ], ["A"], ARG))

ITEMS.append(sr(504, "choice",
    "Read the paragraph. Our public library now lends more than books. ____ it lets cardholders borrow "
    "board games, tools, and even ukuleles. Which transition best fills the blank?",
    [
        Option("A", "For example,", True,
               "correct: the games, tools, and ukuleles are specific examples of the broader claim"),
        Option("B", "However,", False,
               "signals a contrast, but the second sentence supports the first rather than opposing it"),
        Option("C", "As a result,", False,
               "signals a consequence, but lending games is an instance, not a result of the claim"),
        Option("D", "In conclusion,", False,
               "signals a closing summary, but this sentence opens the support instead of wrapping it up"),
    ], ["A"], INFO))

ITEMS.append(sr(505, "inline-choice",
    "Read the paragraph. The city planted shade trees along Main Street last year. As a result, the "
    "sidewalks now stay cooler on hot afternoons. The underlined transition is 'As a result.' "
    "Which choice is best?",
    [
        Option("A", "NO CHANGE", True,
               "correct: the cooler sidewalks are the outcome of the trees, so the result signal already fits"),
        Option("B", "However,", False,
               "signals a contrast, but the second sentence continues the idea instead of opposing it"),
        Option("C", "For example,", False,
               "signals an example, but the cooler sidewalks are a result, not an instance of the trees"),
        Option("D", "Meanwhile,", False,
               "signals two things at once, but the cooling follows from the trees being planted"),
    ], ["A"], INFO))

ITEMS.append(sr(506, "inline-choice",
    "Read the paragraph. A new skate park would give teens a safe place to hang out. ____ it would cost the "
    "city money that some neighbors want spent elsewhere. Which transition best fills the blank?",
    [
        Option("A", "However,", True,
               "correct: it marks the shift from the benefit to a drawback that cuts the other way"),
        Option("B", "Therefore,", False,
               "signals a result, but the cost is a competing concern, not an effect of the benefit"),
        Option("C", "For example,", False,
               "signals an example, but the cost is a drawback, not an instance of the safe hangout"),
        Option("D", "Also,", False,
               "signals another point on the same side, but this sentence raises the opposing side"),
    ], ["A"], ARG))

# ---- Topic sentences (items 7-11) -------------------------------------------

ITEMS.append(sr(507, "choice",
    "Read the paragraph. ____ First, a longer lunch gives students time to eat a real meal. Second, a short "
    "walk outside helps them focus in class. Finally, teachers notice fewer problems in the afternoon. "
    "Which sentence is the best topic sentence to begin this paragraph?",
    [
        Option("A", "A longer lunch break would help students in several clear ways.", True,
               "correct: it names the paragraph's claim and previews the reasons that follow"),
        Option("B", "High schools across the country all use very different daily schedules.", False,
               "too broad: it is about schedules in general and never sets up the specific benefits"),
        Option("C", "Teachers notice far fewer problems in class during the afternoon.", False,
               "this is one of the supporting details, too narrow to serve as the topic sentence"),
        Option("D", "Students should always get as much free time as they could ever want.", False,
               "an overgeneralization the paragraph does not actually argue or support"),
    ], ["A"], ARG))

ITEMS.append(sr(508, "choice",
    "Read the paragraph. ____ The morning drive across town takes longer than it did a few years ago. The "
    "main highway backs up for miles each day. City buses are more crowded than ever before. "
    "Which sentence is the best topic sentence for this paragraph?",
    [
        Option("A", "Traffic across our town has clearly gotten worse in recent years.", True,
               "correct: it umbrellas the commute, highway, and bus details that follow"),
        Option("B", "The morning drive across town takes a bit longer than it once did.", False,
               "this is one supporting detail, not an umbrella sentence for the whole paragraph"),
        Option("C", "Cars have been part of American daily life for well over a century.", False,
               "too broad and off point: the paragraph is about worsening local traffic, not history"),
        Option("D", "The city council will vote on a brand-new bus budget sometime next month.", False,
               "introduces a new topic the paragraph never develops"),
    ], ["A"], INFO))

ITEMS.append(sr(509, "choice",
    "Read the paragraph. ____ Its leaves can be dried and brewed into a mild tea. Its flowers feed the bees "
    "that visit the garden. Its roots have been used in home remedies for years. "
    "Which sentence is the best topic sentence?",
    [
        Option("A", "The common dandelion is far more useful than most people assume.", True,
               "correct: it frames the leaves, flowers, and roots as evidence of usefulness"),
        Option("B", "Dandelion leaves can be dried out and then brewed into a mild cup of tea.", False,
               "one supporting detail, too narrow to open a paragraph about the plant's many uses"),
        Option("C", "Plants have amazed gardeners and scientists alike for thousands of years.", False,
               "too broad: it is about plants in general, not the specific uses of the dandelion"),
        Option("D", "Many people spend hours each spring pulling dandelions out of their lawns.", False,
               "sets up a different point about dandelions as weeds, which the paragraph never argues"),
    ], ["A"], INFO))

ITEMS.append(sr(510, "choice",
    "Read the paragraph. ____ A student who reads for fun builds a bigger vocabulary without even trying. "
    "Regular readers also tend to write more clearly. Best of all, they are more likely to keep reading as "
    "adults. Which sentence best begins this paragraph?",
    [
        Option("A", "Reading for fun brings real benefits that reach beyond the classroom.", True,
               "correct: it states the claim and previews the vocabulary, writing, and habit benefits"),
        Option("B", "Regular readers usually tend to write far more clearly than their classmates.", False,
               "a detail drawn from the paragraph, too narrow to work as the topic sentence"),
        Option("C", "Schools ought to make every student read for a full hour every single night.", False,
               "a policy claim the paragraph does not make or defend"),
        Option("D", "Books have been printed, bound, and shared for hundreds of years by now.", False,
               "too broad and off topic: it is about the history of books, not the value of reading"),
    ], ["A"], ARG))

ITEMS.append(sr(511, "choice",
    "Read the paragraph. ____ First, volunteers cleared the trash that had piled up for years. Next, they "
    "planted grass and a few young trees. Finally, the city added benches and a swing set. "
    "Which sentence is the best topic sentence?",
    [
        Option("A", "The empty lot on Fifth Street became a small neighborhood park.", True,
               "correct: it names the overall change that the ordered steps go on to describe"),
        Option("B", "Volunteers first cleared away the trash that had long piled up on the lot.", False,
               "one step in the process, too narrow to open the paragraph"),
        Option("C", "Public parks can be found in nearly every neighborhood across the city.", False,
               "too broad: it is about parks in general, not this specific lot's change"),
        Option("D", "The city budget set aside for parks has grown a little in recent years.", False,
               "introduces an unrelated topic the paragraph does not develop"),
    ], ["A"], INFO))

# ---- Sentence placement / logical order (items 12-16) -----------------------

ITEMS.append(sr(512, "choice",
    "Read the paragraph. (1) Our garden club started with just six students and a patch of weeds. "
    "(2) By the end of the year, it had grown to more than forty members. (3) Together they grew vegetables "
    "the cafeteria used in its lunches. The writer wants to add this sentence: 'They spent the first "
    "weekends clearing the soil and building beds.' Where should it best be placed?",
    [
        Option("A", "Between sentences 1 and 2", True,
               "correct: the early clearing work follows the club's start and comes before its later growth"),
        Option("B", "Before sentence 1", False,
               "the added sentence describes work that only makes sense once the club has formed"),
        Option("C", "Between sentences 2 and 3", False,
               "this splits the club's growth from what its members went on to accomplish"),
        Option("D", "After sentence 3", False,
               "the clearing happened at the very start, so ending with it reverses the time order"),
    ], ["A"], INFO))

ITEMS.append(sr(513, "choice",
    "Read the paragraph. (1) Sea otters are more than just fun animals to watch. (2) They eat sea urchins "
    "that would otherwise chew up whole kelp forests. (3) Healthy kelp forests then shelter many kinds of "
    "fish. The writer wants to add this sentence: 'In this way, one animal helps hold a whole habitat "
    "together.' Where should it best be placed?",
    [
        Option("A", "After sentence 3", True,
               "correct: it sums up the chain of effects, so it belongs after that chain is laid out"),
        Option("B", "Before sentence 1", False,
               "a summarizing sentence cannot come before the evidence it is meant to sum up"),
        Option("C", "Between sentences 1 and 2", False,
               "this interrupts the setup before any supporting detail has been offered"),
        Option("D", "Between sentences 2 and 3", False,
               "this cuts the cause-and-effect chain in half before the paragraph finishes it"),
    ], ["A"], ARG))

ITEMS.append(sr(514, "choice",
    "Read the paragraph. (1) Making a good cup of tea takes only a few simple steps. (2) First, bring fresh "
    "water to a boil. (3) The tea should then steep for a few quiet minutes. (4) Pour the hot water over the "
    "tea leaves in the cup. Which change would best improve the order of this paragraph?",
    [
        Option("A", "Move sentence 4 so that it comes before sentence 3.", True,
               "correct: you pour the water over the leaves before the tea can steep"),
        Option("B", "Move sentence 1 to the very end of the paragraph.", False,
               "sentence 1 is the topic sentence and belongs at the start, not the end"),
        Option("C", "Move sentence 2 so that it comes after sentence 3.", False,
               "boiling the water must come first, so shifting it later breaks the sequence"),
        Option("D", "Leave the order of the paragraph exactly as it is.", False,
               "as written, the tea steeps before the leaves are added, which reverses the real steps"),
    ], ["A"], INFO))

ITEMS.append(sr(515, "choice",
    "Read the paragraph. (1) Our school's new bike-share program was popular from day one. (2) Riders pick "
    "up a bike at one rack and drop it at another. (3) Each bike comes with lights and a basket for a "
    "backpack. The writer wants to add this sentence: 'More than two hundred students signed up in the "
    "first week.' Where should it best be placed?",
    [
        Option("A", "Between sentences 1 and 2", True,
               "correct: the sign-up number backs the opening claim about popularity right where it is made"),
        Option("B", "Before sentence 1", False,
               "the number only makes sense once the program itself has been introduced"),
        Option("C", "Between sentences 2 and 3", False,
               "this separates two sentences that both describe how the bikes are used"),
        Option("D", "After sentence 3", False,
               "a sign-up number backs the popularity claim, not the closing detail about equipment"),
    ], ["A"], ARG))

ITEMS.append(sr(516, "choice",
    "Read the paragraph. (1) Learning to cook at home can save a lot of money. (2) A restaurant meal often "
    "costs several times what the same dish costs to make. (3) Cooking also lets you control what goes into "
    "your food. (4) Over a year, those savings can add up fast. Which change would best improve the "
    "organization of this paragraph?",
    [
        Option("A", "Move sentence 3 to the very end of the paragraph.", True,
               "correct: sentences 1, 2, and 4 build the savings point, so the ingredients aside fits last"),
        Option("B", "Move sentence 1 to the very end of the paragraph.", False,
               "sentence 1 is the topic sentence and must stay at the start"),
        Option("C", "Move sentence 2 so that it comes after sentence 4.", False,
               "sentences 2 and 4 both develop the cost point and already sit in a sensible order"),
        Option("D", "Leave the order of the paragraph exactly as it is.", False,
               "as written, the ingredients point interrupts the two sentences about cost savings"),
    ], ["A"], INFO))


if __name__ == "__main__":
    npass = 0
    for it in ITEMS:
        qc_item(it)
        if it.qc["passed"]:
            npass += 1
        else:
            print(qc_report(it))
            print()
    print(f"{npass}/{len(ITEMS)} PASS")
    sys.exit(0 if npass == len(ITEMS) else 1)
