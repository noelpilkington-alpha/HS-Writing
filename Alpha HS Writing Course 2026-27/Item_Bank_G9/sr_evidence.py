"""
sr_evidence.py  -  16 selected-response test-bank items for the G9 "evidence-in-draft" subskill.

Subskill: evidence (add / delete / select the best supporting detail; relevance to the claim, and
choosing the best evidence for a stated claim). ACC: ACC.W.SRC.1 (use relevant, sufficient evidence)
+ ACC.W.ARG.2 (support a claim with evidence), mapped to CCSS.W.9-10.1. Mirrors the working SR
example in ../pipeline/item_contract.py (__main__) and the G10 sr_evidence bank, at a simpler
English-I (G9) reading level (shorter sentences, everyday topics).

Every item embeds a short student draft (argument) with no external stimulus dependency. Four
question shapes, all inside this one subskill:
  - ADD:     which sentence best supports the claim with relevant evidence?    (qti_type "choice")
  - DELETE:  which sentence should be removed because it is irrelevant?        (qti_type "hottext")
  - SELECT:  which detail is the most relevant evidence for the claim?         (qti_type "choice")
  - BEST:    which of two on-topic details is the STRONGER evidence?           (qti_type "choice")

Each distractor carries a real-misconception rationale from one of the named families:
  off-claim  |  restates the topic  |  supports the opposing view  |  weaker-but-on-topic  |
  (delete items) relevant, should stay.

Runs every item through the QC harness on run and prints "N/16 PASS". Dependency-free (stdlib + contract).
IDs: ACC-W910-SR-EVID-0501 .. 0016.
"""
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from item_contract import Item, Option, qc_item, qc_report  # noqa: E402

ACC = ["ACC.W.SRC.1", "ACC.W.ARG.2", "CCSS.W.9-10.1"]
PROV = {"copyright": "own_authored", "authored": "2026-07-09"}

ITEMS: list[Item] = []


def add(it: Item) -> None:
    ITEMS.append(it)


# ============================================================================
# ADD shape: which sentence best supports the claim with relevant evidence?
# 3 distractors = off-claim / restates the topic / supports the opposing view.
# ============================================================================

add(Item(
    id="ACC-W910-SR-EVID-0501", family="SR", grade="9-10", subskill_or_mode="evidence",
    qti_type="choice",
    stem=("A student is arguing that the city should plant more trees along busy streets. Which sentence, "
          "added after the claim, best supports it with relevant evidence?"),
    acc_tags=ACC,
    options=[
        Option("A", "On hot days, shaded streets can measure several degrees cooler than bare streets nearby.", True, ""),
        Option("B", "Many people say they simply like how a leafy, tree-lined street looks in the fall.", False, "off-claim: an opinion on looks, not the cooling benefit the claim rests on"),
        Option("C", "Planting more street trees is an idea that many big cities have talked about lately.", False, "restates the topic and adds no evidence for the claim"),
        Option("D", "Some drivers say that tree roots can crack a sidewalk and cost the city money to fix.", False, "supports the opposing view, not the claim"),
    ],
    answer_key=["A"], provenance=PROV,
))

add(Item(
    id="ACC-W910-SR-EVID-0502", family="SR", grade="9-10", subskill_or_mode="evidence",
    qti_type="choice",
    stem=("A student argues that the school should expand its recycling program. Which sentence best "
          "supports that claim with relevant evidence?"),
    acc_tags=ACC,
    options=[
        Option("A", "In its first year, the new bins kept about six tons of paper out of the landfill.", True, ""),
        Option("B", "Recycling is a topic that comes up often in science class and school assemblies now.", False, "restates the topic and gives no evidence of what recycling achieves"),
        Option("C", "A few teachers say the extra bins slow students down and clutter the crowded halls.", False, "supports the opposing view, not the claim"),
        Option("D", "Many students feel a little proud when they drop a bottle in the right colored bin.", False, "off-claim: reports a feeling, not evidence the program works"),
    ],
    answer_key=["A"], provenance=PROV,
))

add(Item(
    id="ACC-W910-SR-EVID-0503", family="SR", grade="9-10", subskill_or_mode="evidence",
    qti_type="choice",
    stem=("In an argument that the library should stay open later on weeknights, which sentence best "
          "supports the claim with relevant evidence?"),
    acc_tags=ACC,
    options=[
        Option("A", "A survey found most teens reach the library only after their sports and jobs end.", True, ""),
        Option("B", "Libraries have been an important part of American towns for well over a century now.", False, "restates the topic and adds no support for later hours"),
        Option("C", "Some taxpayers worry that longer hours would raise costs the town cannot afford well.", False, "supports the opposing view, not the claim"),
        Option("D", "The library's reading room has tall windows and soft chairs that many patrons enjoy.", False, "off-claim: describes the room, not a reason to extend hours"),
    ],
    answer_key=["A"], provenance=PROV,
))

add(Item(
    id="ACC-W910-SR-EVID-0504", family="SR", grade="9-10", subskill_or_mode="evidence",
    qti_type="choice",
    stem=("A student argues that the school district should switch its old diesel buses to electric buses. "
          "Which sentence best supports the claim with relevant evidence?"),
    acc_tags=ACC,
    options=[
        Option("A", "Electric buses give off no tailpipe exhaust, so riders breathe cleaner air each morning.", True, ""),
        Option("B", "School buses are a familiar yellow sight on almost every neighborhood street at dawn.", False, "restates the topic and adds no support for switching to electric"),
        Option("C", "Some parents worry that new electric buses would cost far more than the district can spend.", False, "supports the opposing view, not the claim"),
        Option("D", "Plenty of students say the seats on a bus feel more comfortable than the seats in a car.", False, "off-claim: seat comfort has nothing to do with the claim"),
    ],
    answer_key=["A"], provenance=PROV,
))

add(Item(
    id="ACC-W910-SR-EVID-0505", family="SR", grade="9-10", subskill_or_mode="evidence",
    qti_type="choice",
    stem=("In an argument that the neighborhood should turn an empty lot into a community garden, which "
          "sentence best supports the claim with relevant evidence?"),
    acc_tags=ACC,
    options=[
        Option("A", "In one town, a garden on a vacant lot now grows fresh food for dozens of families.", True, ""),
        Option("B", "Empty lots can be found in nearly every older neighborhood in cities across the land.", False, "restates the topic and gives no reason to build a garden"),
        Option("C", "A number of gardeners find that pulling weeds on a quiet morning helps them relax a bit.", False, "off-claim: a personal feeling, not evidence about the neighborhood"),
        Option("D", "Some owners object that a garden ties up land they had hoped to sell to a developer.", False, "supports the opposing view, not the claim"),
    ],
    answer_key=["A"], provenance=PROV,
))

# ============================================================================
# DELETE shape: which sentence should be removed because it is irrelevant?
# The correct option IS the off-topic sentence; distractors are relevant lines
# whose rationale explains why each belongs (should stay).  qti_type "hottext".
# ============================================================================

add(Item(
    id="ACC-W910-SR-EVID-0506", family="SR", grade="9-10", subskill_or_mode="evidence",
    qti_type="hottext",
    stem=("Read this draft, which argues that the school should plant a pollinator garden. "
          "(1) A pollinator garden gives bees and butterflies the wildflowers they need to feed. "
          "(2) Because many crops depend on pollinators, losing them would put our food at risk. "
          "(3) The cafeteria recently added a salad bar that many students say they really enjoy. "
          "(4) A garden also gives science classes a living place to study insects up close. "
          "Select the sentence that should be deleted because it does not support the claim."),
    acc_tags=ACC,
    options=[
        Option("S1", "A pollinator garden gives bees and butterflies the wildflowers they need to feed.", False, "relevant: names the direct benefit to pollinators, so it should stay"),
        Option("S2", "Because many crops depend on pollinators, losing them would put our food at risk.", False, "relevant: links pollinators to the food supply, so it supports the claim"),
        Option("S3", "The cafeteria recently added a salad bar that many students say they really enjoy.", True, ""),
        Option("S4", "A garden also gives science classes a living place to study insects up close.", False, "relevant: gives an educational reason to keep the garden, so it should stay"),
    ],
    answer_key=["S3"], provenance=PROV,
))

add(Item(
    id="ACC-W910-SR-EVID-0507", family="SR", grade="9-10", subskill_or_mode="evidence",
    qti_type="hottext",
    stem=("Read this draft, which argues that the school should put solar panels on its roof. "
          "(1) Once installed, rooftop panels can cut the school's electric bill by a large share. "
          "(2) The money the school saves on power could then buy books, supplies, and repairs. "
          "(3) The gym floor was refinished last spring and now looks shiny and brand new. "
          "(4) Panels also let science classes track real energy data from above their classroom. "
          "Select the sentence that should be deleted because it does not support the claim."),
    acc_tags=ACC,
    options=[
        Option("S1", "Once installed, rooftop panels can cut the school's electric bill by a large share.", False, "relevant: names the money-saving benefit, so it should stay"),
        Option("S2", "The money the school saves on power could then buy books, supplies, and repairs.", False, "relevant: shows what the savings enable, so it supports the claim"),
        Option("S3", "The gym floor was refinished last spring and now looks shiny and brand new.", True, ""),
        Option("S4", "Panels also let science classes track real energy data from above their classroom.", False, "relevant: gives a learning benefit of the panels, so it should stay"),
    ],
    answer_key=["S3"], provenance=PROV,
))

add(Item(
    id="ACC-W910-SR-EVID-0508", family="SR", grade="9-10", subskill_or_mode="evidence",
    qti_type="hottext",
    stem=("Read this draft, which argues that the cafeteria should work harder to cut food waste. "
          "(1) Lunch trays leave the cafeteria each day still piled with uneaten fruit and bread. "
          "(2) Food that gets thrown out wastes both the money spent on it and the work to grow it. "
          "(3) The cafeteria repainted its walls a bright blue over the long winter break. "
          "(4) A simple share table lets students leave sealed snacks for classmates who are hungry. "
          "Select the sentence that should be deleted because it does not support the claim."),
    acc_tags=ACC,
    options=[
        Option("S1", "Lunch trays leave the cafeteria each day still piled with uneaten fruit and bread.", False, "relevant: shows the scale of the waste problem, so it should stay"),
        Option("S2", "Food that gets thrown out wastes both the money spent on it and the work to grow it.", False, "relevant: explains why the waste matters, so it supports the claim"),
        Option("S3", "The cafeteria repainted its walls a bright blue over the long winter break.", True, ""),
        Option("S4", "A simple share table lets students leave sealed snacks for classmates who are hungry.", False, "relevant: offers a fix that would cut waste, so it should stay"),
    ],
    answer_key=["S3"], provenance=PROV,
))

add(Item(
    id="ACC-W910-SR-EVID-0509", family="SR", grade="9-10", subskill_or_mode="evidence",
    qti_type="hottext",
    stem=("Read this draft, which argues that the town should hold a beach cleanup each spring. "
          "(1) Plastic left on the beach breaks into tiny bits that birds and fish swallow by mistake. "
          "(2) A single morning cleanup can pull hundreds of pounds of trash off one stretch of sand. "
          "(3) The snack stand near the pier just started selling a new flavor of ice cream. "
          "(4) Regular cleanups also teach people to throw away less single-use plastic at home. "
          "Select the sentence that should be deleted because it does not support the claim."),
    acc_tags=ACC,
    options=[
        Option("S1", "Plastic left on the beach breaks into tiny bits that birds and fish swallow by mistake.", False, "relevant: shows the harm a cleanup would reduce, so it should stay"),
        Option("S2", "A single morning cleanup can pull hundreds of pounds of trash off one stretch of sand.", False, "relevant: shows how effective a cleanup is, so it supports the claim"),
        Option("S3", "The snack stand near the pier just started selling a new flavor of ice cream.", True, ""),
        Option("S4", "Regular cleanups also teach people to throw away less single-use plastic at home.", False, "relevant: names a lasting benefit of cleanups, so it should stay"),
    ],
    answer_key=["S3"], provenance=PROV,
))

# ============================================================================
# SELECT shape: which detail is the most relevant evidence for the claim?
# Same misconception families as the ADD items (off-claim / restates / opposing).
# ============================================================================

add(Item(
    id="ACC-W910-SR-EVID-0510", family="SR", grade="9-10", subskill_or_mode="evidence",
    qti_type="choice",
    stem=("A student wants to add evidence to an argument that dry towns should set stricter water rules. "
          "Which detail is the most relevant evidence for that claim?"),
    acc_tags=ACC,
    options=[
        Option("A", "During the last dry spell, towns that limited lawn watering made their water last longer.", True, ""),
        Option("B", "Water is a resource that people in every part of the country use in some form each day.", False, "restates the topic and adds no support for stricter rules"),
        Option("C", "Some people feel that watering rules are a bother that spoils the look of a green lawn.", False, "supports the opposing view, not the claim"),
        Option("D", "A cold glass of water is what many people reach for first on a hot summer afternoon.", False, "off-claim: a preference for water, not evidence about rules"),
    ],
    answer_key=["A"], provenance=PROV,
))

add(Item(
    id="ACC-W910-SR-EVID-0511", family="SR", grade="9-10", subskill_or_mode="evidence",
    qti_type="choice",
    stem=("A student argues that the high school should start the day a little later. Which detail is the "
          "most relevant evidence to support that claim?"),
    acc_tags=ACC,
    options=[
        Option("A", "Schools that pushed start times later found students showed up more alert and on time.", True, ""),
        Option("B", "The first bell of the school day is a routine that nearly every teenager knows well.", False, "restates the topic and gives no support for a later start"),
        Option("C", "Some coaches worry that a later start would push practices and games into the evening.", False, "supports the opposing view, not the claim"),
        Option("D", "A number of students say the walk to school feels nicer once the sun is fully up.", False, "off-claim: how the walk feels, not evidence about learning"),
    ],
    answer_key=["A"], provenance=PROV,
))

add(Item(
    id="ACC-W910-SR-EVID-0512", family="SR", grade="9-10", subskill_or_mode="evidence",
    qti_type="choice",
    stem=("A student is writing that the town museum should offer more free-admission days. Which detail "
          "should the writer add to best support that claim?"),
    acc_tags=ACC,
    options=[
        Option("A", "On free days, the museum drew families from parts of town that had rarely visited before.", True, ""),
        Option("B", "The museum holds paintings, tools, and fossils that record the long story of the town.", False, "restates the topic and adds no support for free days"),
        Option("C", "A few donors argue that free days cut the ticket money the museum needs to pay its staff.", False, "supports the opposing view, not the claim"),
        Option("D", "Many visitors say the quiet marble halls of the old museum feel calm and pleasant to walk.", False, "off-claim: the mood of the halls, not evidence about access"),
    ],
    answer_key=["A"], provenance=PROV,
))

add(Item(
    id="ACC-W910-SR-EVID-0513", family="SR", grade="9-10", subskill_or_mode="evidence",
    qti_type="choice",
    stem=("A student argues that the town should offer curbside composting pickup. Which detail is the most "
          "relevant evidence to support that claim?"),
    acc_tags=ACC,
    options=[
        Option("A", "In one town, curbside composting cut the trash sent to the landfill by nearly a third.", True, ""),
        Option("B", "Composting is a practice that gardeners and farmers have relied on for a great many years.", False, "restates the topic and adds no evidence about curbside pickup"),
        Option("C", "Some people complain that a separate compost bin is one more container to store and clean.", False, "supports the opposing view, not the claim"),
        Option("D", "Plenty of people say a backyard compost pile has an earthy smell they do not really mind.", False, "off-claim: an opinion on smell, not evidence about pickup"),
    ],
    answer_key=["A"], provenance=PROV,
))

# ============================================================================
# BEST-EVIDENCE shape: both A and a distractor are ON topic, but A is stronger.
# Distractors: weaker-but-on-topic (vague/anecdote) / restates / opposing.
# ============================================================================

add(Item(
    id="ACC-W910-SR-EVID-0514", family="SR", grade="9-10", subskill_or_mode="evidence",
    qti_type="choice",
    stem=("A student claims that a later lunch would help students focus in afternoon classes. Which detail "
          "is the STRONGEST evidence for that claim?"),
    acc_tags=ACC,
    options=[
        Option("A", "After the later lunch began, teachers logged far fewer students dozing off after noon.", True, ""),
        Option("B", "My friend told me that he always feels a little more awake after he finally eats lunch.", False, "weaker-but-on-topic: a single friend's story is thin next to a measured result"),
        Option("C", "Lunchtime is a part of the day that almost every student looks forward to at school.", False, "restates the topic and gives no evidence about focus"),
        Option("D", "Some teachers say a later lunch would cut into the time they have to teach new lessons.", False, "supports the opposing view, not the claim"),
    ],
    answer_key=["A"], provenance=PROV,
))

add(Item(
    id="ACC-W910-SR-EVID-0515", family="SR", grade="9-10", subskill_or_mode="evidence",
    qti_type="choice",
    stem=("A student claims that adding bike racks would get more students to ride to school. Which detail "
          "is the STRONGEST evidence for that claim?"),
    acc_tags=ACC,
    options=[
        Option("A", "After a nearby school added racks, the number of students biking in doubled that year.", True, ""),
        Option("B", "One student said he might ride more often if there were a good spot to leave his bike.", False, "weaker-but-on-topic: a single guess is thin next to a measured change"),
        Option("C", "Biking to school is a healthy habit that plenty of families talk about at home now.", False, "restates the topic and offers no evidence about racks"),
        Option("D", "Some drivers worry that more student bikes would crowd the busy street near the gate.", False, "supports the opposing view, not the claim"),
    ],
    answer_key=["A"], provenance=PROV,
))

add(Item(
    id="ACC-W910-SR-EVID-0516", family="SR", grade="9-10", subskill_or_mode="evidence",
    qti_type="choice",
    stem=("A student claims that a homework help club would raise students' math grades. Which detail is the "
          "STRONGEST evidence for that claim?"),
    acc_tags=ACC,
    options=[
        Option("A", "Students who joined the help club raised their math grades by a full letter on average.", True, ""),
        Option("B", "A classmate said she thinks a help club would probably make math feel less scary to her.", False, "weaker-but-on-topic: one opinion is thin next to a measured grade change"),
        Option("C", "Math is a subject that many students find tricky at some point during high school.", False, "restates the topic and gives no evidence about the club"),
        Option("D", "Some parents worry that a club after school would leave less time for family dinners.", False, "supports the opposing view, not the claim"),
    ],
    answer_key=["A"], provenance=PROV,
))


# ---- run the QC harness over the whole file --------------------------------
if __name__ == "__main__":
    passed = 0
    for it in ITEMS:
        r = qc_item(it)
        if r["passed"]:
            passed += 1
        else:
            print(qc_report(it))
            print()
    print(f"{passed}/{len(ITEMS)} PASS")
    sys.exit(0 if passed == len(ITEMS) else 1)
