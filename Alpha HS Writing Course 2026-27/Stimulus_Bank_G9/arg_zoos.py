"""
Opposing-pair ARGUMENT stimulus for the G9 (English I band) writing TEST bank.
Topic: Do zoos do more good than harm?  family=opposing, mode=argument, bucket=test.
TWO original G9-register passages (~500-620 words each, targeted 1010-1150L), one pro and one con, each
conceding the other side. >=2 distinct source orgs for credibility contrast:
  PRO side  (conservation / species recovery):  US National Park Service (California condor recovery).
  CON side  (captivity / law sets only a floor):  US Code, Animal Welfare Act (7 U.S.C. ch. 54) via govinfo.gov.
Every numeric figure in prose traces to a federal page fetched live 2026-07-08. No em/en dashes in prose.
Runs itself through the QC harness and exits on the verdict.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# ---------------------------------------------------------------------------
# PASSAGE A  -  pro-zoos (US National Park Service: the California condor recovery)
# ---------------------------------------------------------------------------
PASSAGE_A = (
"To many people, a zoo is just a place to see animals up close. But some zoos do far more than put "
"animals on display. They help save species from vanishing forever. The story of the California condor "
"shows how. This giant bird was once nearly wiped out. Zoos played a central role in bringing it back. "
"Supporters say this power to rescue a species is the strongest reason zoos are worth having.\n\n"

"The condor's fall was steep and frightening. The National Park Service reports that the wild condor "
"population dropped to a low of just 22 individuals in 1982. The species was almost gone. Faced with "
"that crisis, scientists made a bold choice. All wild condors were then trapped and placed in captive "
"breeding programs. Zoos became the last safe home for a bird that could not survive on its own in the "
"wild.\n\n"

"That gamble worked. Inside zoos, the birds were protected, fed, and bred with great care. Slowly their "
"numbers grew. The National Park Service reports that by the end of 2019, there were a total of 518 "
"condors in the world. Of those, 337 were flying free in the wild. A bird that once numbered only 22 "
"had climbed back into the hundreds. Without zoos, supporters argue, the California condor would almost "
"surely be extinct today.\n\n"

"Conservation is only part of the case. Zoos also teach. Most people will never see a wild condor, a "
"tiger, or an elephant in nature. A zoo lets a child stand a few feet from a living animal. Supporters "
"argue that this kind of wonder builds care. A student who feels amazed by an animal may grow up "
"wanting to protect it. Signs, tours, and programs turn a fun day into a lesson about the natural "
"world.\n\n"

"Zoos support science as well. Researchers can study how animals eat, move, and raise their young. "
"Some of what they learn helps protect wild animals too. Zoos also work together across the country. "
"They share animals and plans so that breeding programs stay healthy. This teamwork, supporters say, is "
"how a species like the condor was saved. A single zoo could not do it alone, but a network of zoos "
"can.\n\n"

"Zoos can also help injured or orphaned animals that could not survive in the wild. A hurt hawk or a "
"young bear without a mother may find safe care at a zoo. Supporters argue that these animals become "
"living ambassadors. They give visitors a reason to care about the wild places their relatives still "
"call home.\n\n"

"Supporters do not claim that every zoo is perfect. They agree that a bad zoo, with cramped cages and "
"poor care, does real harm. That kind of place should be fixed or closed. But they argue that the "
"answer is better zoos, not no zoos. A well-run zoo protects species, teaches the public, and supports "
"science all at once. The California condor still flies today because zoos were there when the bird "
"had nowhere else to turn. To supporters, that single rescue is proof that good zoos do far more good "
"than harm."
)

# ---------------------------------------------------------------------------
# PASSAGE B  -  against zoos (US Code, Animal Welfare Act: the law sets only a floor)
# ---------------------------------------------------------------------------
PASSAGE_B = (
"Saving a species from extinction is a real good, and a few zoos have done exactly that. But that "
"success is rare, and it does not describe most zoos. Critics argue that when we look at the whole "
"picture, zoos do more harm than good. The heart of the problem is simple. A zoo keeps wild animals in "
"captivity, and captivity carries a cost that no display sign can hide.\n\n"

"Consider what the law itself reveals. Congress passed the Animal Welfare Act to protect animals kept "
"by zoos and other exhibitors. Under this law, found in the U.S. Code, the government must set "
"standards for the humane handling, care, treatment, and transportation of these animals. The very "
"fact that such a law is needed points to a hard truth. Wild animals in cages face real risks, and "
"without federal rules, their care cannot be trusted.\n\n"

"Here is the deeper worry. The Animal Welfare Act sets only minimum standards. It requires basic "
"handling, housing, feeding, watering, sanitation, ventilation, and veterinary care. These rules are a "
"floor, not a promise of a good life. A zoo can follow every rule and still keep a large animal in a "
"space far too small for its nature. Meeting the minimum is not the same as meeting an animal's true "
"needs. Critics argue that a legal cage is still a cage.\n\n"

"That gap matters most for large, wide-ranging animals. In the wild, an elephant may walk many miles in "
"a single day. A big cat may roam a huge territory in search of food. No zoo enclosure can truly match "
"that kind of space. Animals denied room to roam can grow bored, stressed, or sick over time. Some pace "
"back and forth for hours, and others harm themselves. Critics say these troubling signs reveal the "
"true cost of life behind glass.\n\n"

"There is also the matter of purpose. Supporters point to conservation, yet most animals in most zoos "
"are not part of any release program. They are there to be seen. A crowd walks past, snaps a photo, and "
"moves on to the next exhibit. Critics argue that this is really entertainment dressed up as education. "
"The rare success of a single condor should not excuse the daily confinement of thousands of other "
"animals who will never return to the wild.\n\n"

"Critics of zoos are not blind to the good that a few of them do. They agree that captive breeding "
"saved the California condor and a handful of other species. Their point is narrower. That rescue could "
"be done through small, focused breeding centers, without putting thousands of animals on display for "
"profit. Real conservation protects animals in the wild, where they belong. Before we praise zoos as a "
"public good, critics argue, we should ask a fair question. Do these places truly serve the animals, "
"or do the animals mainly serve the crowd?"
)

FACTS = [
    # ---- PRO side (US National Park Service) ----
    FactSource("California condor wild population low", "22 individuals in 1982", "US National Park Service",
               "https://www.nps.gov/subjects/condors/understandingcondors.htm",
               "dropped to a low of 22 individuals in 1982"),
    FactSource("All wild condors trapped for captive breeding", "captive breeding programs",
               "US National Park Service",
               "https://www.nps.gov/subjects/condors/understandingcondors.htm",
               "All wild condors were then trapped and placed in captive breeding programs"),
    FactSource("Total California condors in the world, end of 2019", "518 condors", "US National Park Service",
               "https://www.nps.gov/subjects/condors/understandingcondors.htm",
               "As of the end of 2019, there were a total of 518 condors in the world"),
    FactSource("California condors flying free in the wild, end of 2019", "337 in the wild",
               "US National Park Service",
               "https://www.nps.gov/subjects/condors/understandingcondors.htm",
               "with 337 of those flying free in the wild"),
    # ---- CON side (US Code, Animal Welfare Act via govinfo.gov) ----
    FactSource("Animal Welfare Act covers animals exhibited by zoos", "exhibitor includes zoos",
               "US Code (Animal Welfare Act, 7 U.S.C. ch. 54)",
               "https://www.govinfo.gov/content/pkg/USCODE-2020-title7/html/USCODE-2020-title7-chap54.htm",
               "includes carnivals, circuses, and zoos exhibiting such animals whether operated for profit or not"),
    FactSource("AWA requires standards for humane handling and care", "humane handling, care, treatment",
               "US Code (Animal Welfare Act, 7 U.S.C. ch. 54)",
               "https://www.govinfo.gov/content/pkg/USCODE-2020-title7/html/USCODE-2020-title7-chap54.htm",
               "the humane handling, care, treatment, and transportation of animals by dealers, research facilities, and exhibitors"),
    FactSource("AWA sets only minimum standards of care", "minimum requirements",
               "US Code (Animal Welfare Act, 7 U.S.C. ch. 54)",
               "https://www.govinfo.gov/content/pkg/USCODE-2020-title7/html/USCODE-2020-title7-chap54.htm",
               "minimum requirements ... for handling, housing, feeding, watering, sanitation, ventilation ... adequate veterinary care"),
]

REC = StimulusRecord(
    id="ACC-W910-ARG-OPP-0010",
    grade="9", mode="argument", family="opposing", bucket="test",
    form="ohio", annotated=False,
    topic_id="zoos_good_or_harm",
    modeling_anchor="Ohio ELA II / MD MCAP (opposing-view pick-a-side)",
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "CCSS.W.9-10.1"],
    prompt=("Weighing both sources, write an argumentative essay stating your position on whether zoos do "
            "more good than harm. Support your claim with specific evidence from both sources, and respond "
            "to at least one objection from the side you do not take."),
    passages=[
        Passage(title="Why Zoos Are Worth Saving",
                angle="pro-zoos; US National Park Service California condor recovery data",
                text=PASSAGE_A),
        Passage(title="The Hidden Cost of Life in a Zoo",
                angle="against zoos; US Code Animal Welfare Act showing the law sets only a minimum floor of care",
                text=PASSAGE_B),
    ],
    fact_sources=FACTS,
    provenance={"copyright": "own_authored",
                "rights": "public-domain-sourced (US federal)",
                "authored": "2026-07-08"},
)

if __name__ == "__main__":
    import re
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
    import readability_gate as rg
    for p in REC.passages:
        wc = len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", p.text))
        lex = rg.analyze_text(p.text)["lexile_estimate"]
        print(f"passage '{p.title[:44]}': {wc} words, ~{lex}L")
    qc = qc_stimulus(REC); print(qc_report(REC)); import sys; sys.exit(0 if qc["passed"] else 1)
