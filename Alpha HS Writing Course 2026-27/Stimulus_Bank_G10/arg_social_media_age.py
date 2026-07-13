"""
Opposing-pair argument stimulus: should the US set a minimum age (e.g. 16) for social media accounts?
Family=opposing, mode=argument. Every figure traces to a fetched federal page (US HHS Surgeon General
advisory + CDC YRBS 2021 + FTC COPPA rule), fetched live 2026-07-07. Runs itself through the QC harness
and reports. Modeled EXACTLY on pipeline/_authored_food_waste.py.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# ---------------------------------------------------------------------------
# PASSAGE A: the case FOR a minimum age of 16 (protect youth). HHS + CDC figures.
# ---------------------------------------------------------------------------
PASSAGE_A = (
"Every day, most American teenagers reach for a phone and open a social media app. This is not a small "
"trend. The U.S. Surgeon General reports that up to 95 percent of young people aged 13 to 17 use a social "
"media platform. A recent survey found that teenagers spend an average of 3.5 hours a day on these apps. "
"About one third say they use social media almost constantly. People who back a minimum age of 16 say a "
"habit this large, formed this young, is exactly why we need a firmer age limit.\n\n"

"The strongest reason is the growing proof of harm. The Surgeon General's advisory reports that teens who "
"spend more than 3 hours a day on social media face double the risk of mental health problems. That includes "
"signs of depression and anxiety. This warning matters because heavy use is now the norm, not the exception. "
"The same advisory shares one more figure. When teens were asked how social media affects their body image, "
"46 percent of those aged 13 to 17 said it makes them feel worse.\n\n"

"These are not the only troubling numbers. The Centers for Disease Control and Prevention studies the health "
"of high school students across the country. In its 2021 survey, 42 percent of high school students said they "
"felt sad or hopeless for weeks at a time. Another 29 percent said they had poor mental health. These figures "
"have climbed over the past ten years. That is the same stretch of time when phones and social media became a "
"constant part of teen life. Supporters of an age limit do not say social media is the only cause. They say a "
"product used this heavily, by this many young people, during a time when teen mental health is clearly "
"struggling, deserves real caution.\n\n"

"To be fair, the picture is not all bad, and honest supporters admit it. The Surgeon General's advisory also "
"reports real benefits. Most teenagers say social media helps them feel more accepted. Many say it gives them "
"a place to show their creative side. For some young people, these links matter, above all those who feel "
"alone. A minimum age of 16 would not erase those benefits. It would simply delay full access until students "
"are a bit older and better able to handle a public online life.\n\n"

"Sixteen is a fair line. It is close to the age when we already trust teens to drive a car. Driving offers "
"freedom, but it also carries real risk. So we set an age and we train young people first. We do not ban "
"driving. The same logic fits social media. The evidence from federal health agencies shows a product used "
"almost everywhere, for hours each day. It is used at an age when the mind is still forming and when serious "
"mental health problems are rising. Setting sixteen as the minimum age would not solve every problem. But it "
"would give young people time to grow before we hand them a tool that federal experts say we cannot yet call "
"safe."
)

# ---------------------------------------------------------------------------
# PASSAGE B: the case AGAINST a minimum age of 16 (access, expression, enforcement). HHS benefits + FTC.
# ---------------------------------------------------------------------------
PASSAGE_B = (
"Nearly every American teenager uses social media, and for many of them it is a good thing. The U.S. Surgeon "
"General's advisory is the same report often quoted to warn about these apps. Yet it also lists their "
"benefits. Most teens say social media helps them feel more accepted (58 percent). Many say it gives them "
"people who can support them through tough times (67 percent). Many say it offers a place to show their "
"creative side (71 percent). And most say it keeps them more connected to what their friends are doing (80 "
"percent). Those are not small numbers. They show why a strict minimum age of 16 could do real harm of its "
"own.\n\n"

"For some young people, these links are a lifeline, not a luxury. The advisory notes that online support can "
"matter most for youth who are often left out. That includes racial, ethnic, and LGBTQ young people. Seven "
"out of ten teen girls of color report finding positive or identity-affirming content online. A teen who "
"feels alone in a small town, or in a hard school, may find a community online that finally gets them. A law "
"that shuts the door until age 16 would cut off that support during some of the hardest years of youth. And "
"it would fall hardest on the young people who need it most.\n\n"

"There is also the hard problem of enforcement. To keep everyone under 16 off social media, a platform would "
"have to check the age of every single user, adults included. Federal law already draws an age line here. "
"The Children's Online Privacy Protection Rule, enforced by the Federal Trade Commission, requires companies "
"to get a parent's clear consent before collecting personal information from a child under 13. Pushing the "
"real age up to 16 would grow that burden. It would press companies to demand proof of age, such as a "
"government ID card, from all of us. That trades away privacy for everyone to protect some. And determined "
"teens have always found ways around such rules.\n\n"

"None of this means the risks are fake. Honest opponents of an age limit accept the evidence. The Surgeon "
"General warns that teens who spend more than 3 hours a day on social media face double the risk of mental "
"health problems. The Centers for Disease Control and Prevention found that 42 percent of high school "
"students felt sad or hopeless for weeks at a time in 2021. Those findings are serious. They deserve a "
"serious response. The real question is whether a blunt age ban is the right one.\n\n"

"A better answer targets the harm without erasing the benefits. The same federal advisory asks companies to "
"make their platforms safer by default. It asks them to limit the features that keep teens scrolling for "
"hours. It asks them to give families better tools and clearer facts. Those steps address the true danger. "
"The danger is not that a 15 year old has an account. It is how the apps are built and how heavily they are "
"used. A minimum age of 16 treats every teen as if the product can never be made safe. But the evidence shows "
"it can be both risky and useful. Rather than lock millions of young people out, we should make the place they "
"already gather online healthier for them."
)

HHS_URL = "https://www.hhs.gov/surgeongeneral/reports-and-publications/youth-mental-health/social-media/index.html"
HHS_PDF = "https://www.hhs.gov/sites/default/files/sg-youth-mental-health-social-media-advisory.pdf"
CDC_URL = "https://www.cdc.gov/yrbs/results/2021-yrbs-results.html"
FTC_URL = "https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa"

rec = StimulusRecord(
    id="ACC-W910-ARG-OPP-0005",
    grade="9-10", mode="argument", family="opposing",
    modeling_anchor="Ohio ELA II / MD MCAP (opposing-view pick-a-side)",
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "ACC.W.ARG.4", "CCSS.W.9-10.1",
              "OH-ELA.W.10.1", "MD-MCAP.W.10.ARG"],
    prompt=("Weighing both sources, write an argumentative essay stating your position on whether the United "
            "States should set a minimum age of 16 for social media accounts. Support your claim with specific "
            "evidence from both sources and address at least one objection from the side you disagree with."),
    passages=[
        Passage(title="Set a Minimum Age of 16 for Social Media",
                angle="pro-limit; US HHS Surgeon General advisory + CDC YRBS youth mental-health data",
                text=PASSAGE_A),
        Passage(title="Do Not Lock Teenagers Out: The Case Against an Age Limit",
                angle="anti-limit; HHS-documented benefits + FTC/COPPA enforcement and access cost",
                text=PASSAGE_B),
    ],
    fact_sources=[
        FactSource("Share of teens 13-17 who use social media", "95 percent", "US HHS (Surgeon General)",
                   HHS_URL, "Up to 95% of young people aged 13-17 report using a social media platform."),
        FactSource("Average daily social media use by teens", "3.5 hours", "US HHS (Surgeon General)",
                   HHS_URL, "teenagers spend an average of 3.5 hours a day on social media"),
        FactSource("Heavy use and doubled mental-health risk", "3 hours", "US HHS (Surgeon General)",
                   HHS_URL, "who spend more than 3 hours a day on social media face double the risk of mental health problems"),
        FactSource("Teens who say social media worsens body image", "46 percent", "US HHS (Surgeon General)",
                   HHS_URL, "46% of adolescents aged 13-17 said social media makes them feel worse"),
        FactSource("HS students with persistent sadness/hopelessness (2021)", "42 percent", "US CDC (YRBS)",
                   CDC_URL, "over 40 percent (42%) of high school students struggle with persistent feelings of sadness or hopelessness"),
        FactSource("HS students reporting poor mental health (2021)", "29 percent", "US CDC (YRBS)",
                   CDC_URL, "nearly 30 percent (29%) experienced poor mental health"),
        FactSource("Teens who feel more accepted via social media", "58 percent", "US HHS (Surgeon General)",
                   HHS_PDF, "helps them feel more accepted (58%)"),
        FactSource("Teens who feel supported through tough times", "67 percent", "US HHS (Surgeon General)",
                   HHS_PDF, "people who can support them through tough times (67%)"),
        FactSource("Teens who say it shows their creative side", "71 percent", "US HHS (Surgeon General)",
                   HHS_PDF, "a place to show their creative side (71%)"),
        FactSource("Teens who feel more connected to friends", "80 percent", "US HHS (Surgeon General)",
                   HHS_PDF, "more connected to what's going on in their friends' lives (80%)"),
        FactSource("Girls of color finding identity-affirming content", "", "US HHS (Surgeon General)",
                   HHS_PDF, "Seven out of ten adolescent girls of color report encountering positive or identity-affirming content"),
        FactSource("COPPA verifiable-consent age line", "13", "US FTC (COPPA Rule)",
                   FTC_URL, "operators of websites or online services directed to children under 13 years of age ... collecting personal information online from a child"),
    ],
    provenance={"copyright": "own_authored",
                "rights": "public-domain-sourced (US HHS/Surgeon General + CDC + FTC; 17 USC 105)",
                "two_source_verified": True, "authored": "2026-07-07"},
)


# --- Two-bucket migration: decompose the opposing pair into stance-tagged TEST singles ---------
# One pro + one con member of proposition "prop_social_media_age". The pair above (rec) is retained for backward
# compatibility; the singles are what the composer assembles opposing pairs from. Each single carries the
# FULL fact_sources list (the anti-fabrication gate only requires the figures IN its passage to be covered;
# extra rows are harmless and guarantee the >=3 citable-fact minimum).
SINGLES = [
    StimulusRecord(
        id="ACC-W910-ARG-SINGLE-SOCIAL-MEDIA-AGE-PRO",
        grade="9-10", mode="argument", family="single", bucket="test",
        modeling_anchor=rec.modeling_anchor,
        acc_tags=list(rec.acc_tags),
        prompt="Read this source arguing in favor of the proposal.",
        passages=[Passage(title=rec.passages[0].title, angle=rec.passages[0].angle, text=rec.passages[0].text)],
        fact_sources=list(rec.fact_sources),
        provenance=dict(rec.provenance),
        topic_id="social_media_age", proposition_id="prop_social_media_age", stance="pro",
        form="staar", task_demand=3),
    StimulusRecord(
        id="ACC-W910-ARG-SINGLE-SOCIAL-MEDIA-AGE-CON",
        grade="9-10", mode="argument", family="single", bucket="test",
        modeling_anchor=rec.modeling_anchor,
        acc_tags=list(rec.acc_tags),
        prompt="Read this source arguing against the proposal.",
        passages=[Passage(title=rec.passages[1].title, angle=rec.passages[1].angle, text=rec.passages[1].text)],
        fact_sources=list(rec.fact_sources),
        provenance=dict(rec.provenance),
        topic_id="social_media_age", proposition_id="prop_social_media_age", stance="con",
        form="staar", task_demand=3),
]

if __name__ == "__main__":
    qc_stimulus(rec)
    import re
    for p in rec.passages:
        wc = len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", p.text))
        print(f"passage '{p.title[:40]}...' word count: {wc}")
    print(qc_report(rec))
    print("-> PASS" if rec.qc["passed"] else "-> FAIL")
    # decomposed stance singles
    assert len(SINGLES) == 2 and {x.stance for x in SINGLES} == {"pro", "con"}
    for _x in SINGLES:
        assert _x.family == "single" and _x.bucket == "test" and _x.proposition_id and _x.topic_id and _x.form
        qc_stimulus(_x)
        assert _x.qc["passed"], f"single {_x.id} must pass QC: {_x.qc.get('first_failure')}"
    print("SINGLES decomposition OK")
    sys.exit(0 if rec.qc["passed"] else 1)
