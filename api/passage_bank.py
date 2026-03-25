"""Passage bank for the HS Writing grading engine.

Stores passage text indexed by ID (SP-001, SYN-07, etc.) for use
in grading prompts that need the source passage for context.

Phase 1: Gateway and gate passages only.
Passages are stored inline here. In production, these could move to a
database or file-based store.
"""

PASSAGES: dict[str, dict] = {

    # ===== B1L Gateway Passages =====

    "SP-024": {
        "id": "SP-024",
        "author": "Frances E.W. Harper",
        "title": "We Are All Bound Up Together",
        "date": "1866",
        "course": "B1L",
        "usage": "L07 gateway (rhetorical analysis)",
        "text": """We are all bound up together in one great bundle of humanity, and society cannot trample on the weakest and feeblest of its members without receiving the curse in its own soul. You tried that in the case of the negro. You pressed him down for two centuries; and in so doing you crippled the moral strength and paralyzed the spiritual energies of the white men of the country. When the hands of the black were fettered, white men were deprived of the liberty of speech and the freedom of the press. Society cannot afford to neglect the enlightenment of any class of its members.

I do not believe that giving the woman the ballot is immediately going to cure all the ills of life. I do not believe that white women are dew-drops just exhaled from the skies. I think that like men they may be divided into three classes, the good, the bad, and the indifferent. The good would vote according to their convictions and principles; the bad, as dictated by prejudice or malice; and the indifferent will vote on the strongest side of the question, with the winning party.

You white women speak here of rights. I speak of wrongs. I, as a colored woman, have had in this country an education which has made me feel as if I were in the situation of Ishmael, my hand against every man, and every man's hand against me. Let me go tomorrow morning and take my seat in one of your street cars — I do not know that they will do it in New York, but they will in Philadelphia — and the conductor will put up his hand and stop the car rather than let me ride.

Going from Washington to Baltimore this Spring, they put me in the smoking car. Aye, in the capital of the nation, where the black man consecrated himself to the nation's defence, faithful when combatants were faithless, they put me, a woman, in the smoking car! They did it once; but the next time they tried it, they failed; for I would not go in. I felt the fight in me; but I don't want to have to fight all the time. Today I am puzzled where to make my home. I would like to make it in Philadelphia, near my own friends and relations. But if I want to ride in the streets of Philadelphia, they send me to ride on the platform with the driver.

Have women nothing to do with this? Not merely combatting against the wrongs personally suffered, but combatting against the wrongs of the world; for if there is any class of people who need to be lifted out of their airy nothings and selfishness, it is the white women of America.""",
    },

    "SP-034": {
        "id": "SP-034",
        "author": "Anna Julia Cooper",
        "title": "Womanhood: A Vital Element in the Regeneration and Progress of a Race (excerpt)",
        "date": "1892",
        "course": "B1L",
        "usage": "L20 gate (rhetorical analysis)",
        "text": """The colored woman of to-day occupies, one may say, a unique position in this country. In a period of itself transitional and unsettled, her status seems one of the least ascertainable and definitive of all the forces which make for our civilization. She is confronted by both a woman question and a race problem, and is as yet an unknown or an unacknowledged factor in both.

While the women of the white race can with calm assurance enter upon the work they feel by nature appointed to do, while their men give loyal support and all-glorious to their cause, the colored woman too often finds herself hampered and shamed by a less liberal sentiment and a more conservative attitude on the part of those for whose opinion she cares most. That this survey was faithful to conditions of that day is very evident.

Only the BLACK WOMAN can say "when and where I enter, in the quiet, undisputed dignity of my womanhood, without violence and without suing or special patronage, then and there the whole Negro race enters with me." Is it not evident then that as individual workers for this race we must address ourselves with no half-hearted zeal to this survey of the survey?

It is not the intelligent woman vs. the ignorant woman; nor the white woman vs. the black woman; nor the man vs. the woman — it is not a contest between types and classes merely. It is a movement of universal interest and of vital significance to the whole body politic. The cause of freedom is not the cause of a race or a sect, a party or a class — it is the cause of human kind, the very birthright of humanity.

The higher fruits of civilization can not be extemporized, neither can they beitated by the prototypes of a favored class. They require the slow, painful, laborious mastery of the forces of nature, the systematic training and development of the mind, the training of the hand, and the building up of character. And all this in turn must rest for its base upon the broad foundation of a developed, throbbing, active womanhood — the womanhood that is the mainspring and the source of power, not of a favored class, but of the great mass of the people.""",
    },

    # ===== B1L Gate Synthesis Source Set =====

    "SYN-08": {
        "id": "SYN-08",
        "author": "Various",
        "title": "Universal Basic Income source set",
        "date": "Various",
        "course": "B1L",
        "usage": "L19 gate (synthesis)",
        "text": """SOURCE A (Economic Policy Institute, 2019):
Universal Basic Income proposals have gained traction across the political spectrum. Proponents argue UBI would provide a floor of economic security, reduce poverty, and simplify the welfare bureaucracy. A pilot program in Stockton, California gave 125 residents $500/month for two years. Recipients showed improved mental health, increased full-time employment, and reduced income volatility. Critics counter that nationwide implementation would cost $2.8-3.2 trillion annually.

SOURCE B (Charles Murray, political scientist, 2016):
Every American citizen age 21 and older would get $13,000 a year deposited electronically into a bank account in monthly installments. Of that, $3,000 must be used for health insurance, leaving $10,000 in cash. In return, we would eliminate all other transfer programs — Social Security, Medicare, Medicaid, food stamps, housing subsidies, and the rest. The UBI would be financed by the savings from eliminating existing programs plus a flat surtax on incomes above $30,000.

SOURCE C (Political cartoon, 2020):
[Image description: A two-panel cartoon. Panel 1 shows a person drowning in paperwork labeled "welfare applications" while a bureaucrat stamps "DENIED." Panel 2 shows the same person receiving a simple envelope labeled "UBI check" while the bureaucrat's desk is empty. Caption: "Simplification."]

SOURCE D (Congressional Budget Office analysis, 2020):
A universal basic income of $12,000 per adult would cost approximately $2.8 trillion per year. Current means-tested federal transfer programs total approximately $700 billion. Even eliminating all existing programs would leave a funding gap of $2.1 trillion, requiring either significant tax increases or deficit spending. However, dynamic effects — reduced emergency room visits, lower incarceration costs, increased consumer spending — could offset 15-30% of gross costs.

SOURCE E (Interview with rural community organizer, 2021):
"People in my town don't want a handout. They want jobs. When the factory closed, what hurt wasn't just the paycheck — it was the purpose. You can't replace that with a monthly check. What you can do is use that money to start a business, go back to school, take care of your kids while you figure out the next thing. But only if people see it that way, and right now most folks around here don't."

SOURCE F (Finland UBI pilot study results, 2020):
Finland's two-year UBI experiment (2017-2018) gave 2,000 unemployed citizens €560/month with no conditions. Results: participants reported significantly higher life satisfaction and trust in institutions. Employment effects were modest — participants worked an average of 6 more days than the control group. The study found UBI's primary benefit was psychological rather than economic: reduced stress, increased sense of autonomy, and greater willingness to pursue entrepreneurial activities.""",
    },

    # ===== B1L Gateway Synthesis Source Set =====

    "SYN-06": {
        "id": "SYN-06",
        "author": "Various",
        "title": "Environmental Policy and Economic Growth source set",
        "date": "Various",
        "course": "B1L",
        "usage": "L16 gateway (synthesis)",
        "text": """SOURCE A (Matthew E. Kahn, The Conversation, 2017):
California has positioned itself as a global leader in climate policy, implementing cap-and-trade programs and aggressive renewable energy mandates. Critics predicted economic catastrophe. Instead, California's GDP has grown faster than the national average since implementing its landmark climate legislation. The state's clean energy sector now employs over 500,000 workers. However, these gains are unevenly distributed — rural communities dependent on fossil fuel extraction have experienced job losses, while urban tech hubs have thrived.

SOURCE B (Congressional Budget Office, policy analysis):
Environmental regulations impose measurable costs on the economy. The CBO estimates that aggressive carbon reduction targets could reduce GDP growth by 0.1-0.5 percentage points annually through 2035. Compliance costs fall disproportionately on energy-intensive industries: manufacturing, agriculture, and transportation. However, these projections do not account for the economic costs of inaction — damage from extreme weather events, healthcare costs from air pollution, and agricultural losses from changing climate patterns, which other analyses estimate at 1-3% of GDP annually by 2050.

SOURCE C (EPA, Inventory of U.S. Greenhouse Gas Emissions and Sinks, 2023):
[Data summary: U.S. greenhouse gas emissions declined 17% from 2005 to 2022, while real GDP grew 30% over the same period. Emissions reductions were concentrated in the electricity sector (-40%) due to the coal-to-natural-gas and coal-to-renewables transition. Transportation emissions remained essentially flat. Industrial emissions declined modestly (-8%). The data demonstrates that economic growth and emissions reduction can occur simultaneously, though the pace of reduction remains insufficient to meet stated climate targets.]

SOURCE D (Small business owner, Congressional testimony, 2023):
"I run a third-generation steel fabrication shop in Ohio. When the new emissions standards came in, we had to invest $2.3 million in equipment upgrades — that's more than our annual profit. We took on debt to comply. Meanwhile, our competitors in countries without these regulations undercut our prices by 15-20%. I'm not against clean air. I'm against policies that punish domestic manufacturers while doing nothing about the steel being shipped in from countries with zero environmental standards."

SOURCE E (The Conversation, research summary, 2017):
A tiny fraction of the world's oceans — less than 1% — could potentially meet the growing global demand for seafood through sustainable aquaculture. This represents a model for environmental innovation: rather than choosing between economic growth and environmental protection, new approaches can achieve both simultaneously. The key insight is that environmental constraints often drive innovation that creates new economic opportunities, a pattern visible across sectors from energy to agriculture to manufacturing.

SOURCE F (Environmental economist, policy brief, 2023):
"The 'environment vs. economy' framing is fundamentally misleading. Every dollar spent on environmental protection is a dollar that enters the economy — it pays workers, buys equipment, funds research. The real question is not whether to spend, but how to spend. A carbon tax of $50/ton would raise approximately $300 billion annually. Returned as dividends to citizens, it would be progressive — lower-income households would receive more than they pay in higher energy costs. The economy adapts; the climate doesn't negotiate." """,
    },

    # ===== B2 Speed Run Passages =====

    "SP-027": {
        "id": "SP-027",
        "author": "Wendell Phillips",
        "title": "The Philosophy of the Abolition Movement (excerpt)",
        "date": "1853",
        "course": "B2",
        "usage": "L08 speed run 1 (rhetorical analysis)",
        "text": """We are often asked, Could not this cause have been carried on in a more quiet way? Could you not have advocated reform without such harsh language? We are told that the great misfortune of the antislavery movement was the harsh, personal, and sometimes violent language which has characterized it.

I have to say in reply, that when I look at the facts, I am satisfied that the antislavery movement has not been carried on with too much harshness of language. If the facts and arguments used against slavery were harsh, it was because slavery itself was so monstrous. The fault lies not in our language but in the institution we seek to overthrow.

Sir, when a man stands up, with the pulpit, the press, the forum, and the political party all against him, and proclaims a truth that conflicts with the interests, the prejudices, and the daily habits of a large majority of his fellow-citizens — when he stands up under these circumstances and speaks the truth, it is not strange that his voice should sometimes be harsh and his language violent. The strange thing would be if it were not.

What is the denunciation with which we are charged? It is endeavoring, in our faltering human speech, to declare the enormity of the sin of making merchandise of men — of separating husband and wife — of selling the babe from the arms of its mother — of stifling every aspiration of the human soul. Language is lame to the task of describing slavery as it is.

The great lesson of antislavery is, that you must take the community you seek to reform as you find them. Reformers are not combatants for choice. They go to war because war is the only way to peace. A man may regret war and still be a good soldier; and a man may regret the necessity of harshness in speech and still see that the occasion demands it.""",
    },

    # ===== B2 Plan-to-Essay Passages =====

    "SP-015": {
        "id": "SP-015",
        "author": "Carrie Chapman Catt",
        "title": "The Crisis (excerpt)",
        "date": "1916",
        "course": "B2",
        "usage": "L11 plan-to-essay bridge 1 (rhetorical analysis)",
        "text": """I have taken for my subject, "The Crisis," because I believe that a crisis has come in our movement which, if recognized and the opportunity seized with vigor, means the final victory of our great cause in the very near future. I am aware that some suffragists do not share this belief; they see no signs nor symptoms today which were not present yesterday; no manifestation in the year 1916 which differ significantly from those in the year 1910.

To them I say, the signs of our times point to something more than woman suffrage. They point to a changing world. To those who see, the signs of our times are full of meaning. A world crisis has come. The great war has made it. Millions of women who never gave suffrage a thought are now saying, "Why are we not consulted?" The answer to their question is coming — and it will be democracy.

Do you know that in no country in the world has woman suffrage been established by a peaceful process of evolution? In every land it has come as a revolutionary measure. The suffrage has not been handed to us as a gift; nor will it be. Nor will it come as a natural, gradual development. It will come as a crisis — sharp, decisive, final. And the question before this convention is: Shall we wait for this crisis to overtake us, or shall we make it?

There are politicians who feel the coming change. Some welcome it; more fear it. But all see it. We hold in our hands a weapon more powerful than armies — the vote. And we need not wait for legislation to give it to us; we need only the will to demand it.""",
    },

    # ===== B2 Speed Run Synthesis Source Set =====

    "SYN-09": {
        "id": "SYN-09",
        "author": "Various",
        "title": "Artificial Intelligence and Employment source set",
        "date": "Various",
        "course": "B2",
        "usage": "L10 speed run 3 (synthesis)",
        "text": """SOURCE A (McKinsey Global Institute, 2023):
By 2030, up to 30% of current work activities could be automated using existing AI technology. However, automation does not necessarily mean job elimination — it more often means job transformation. Historically, technology has created more jobs than it has displaced, though the transition periods can be painful for affected workers. The key variable is the speed of adoption: rapid deployment could cause significant short-term displacement, while gradual adoption allows for workforce adaptation.

SOURCE B (MIT economist Daron Acemoglu, 2022):
"The notion that AI will create abundance for all is dangerously naive. Previous waves of automation — the spinning jenny, the assembly line — ultimately created prosperity, but only after decades of worker exploitation and social upheaval. There is nothing automatic about shared prosperity. It requires deliberate policy choices: investment in education, strengthening of worker bargaining power, and regulation that ensures the gains from AI are broadly distributed rather than captured by a narrow elite."

SOURCE C (Graphic, Bureau of Labor Statistics, 2023):
[Chart showing projected job growth 2023-2033: Healthcare support +15%, Technology/AI development +23%, Transportation/warehousing -8%, Manufacturing -3%, Administrative support -12%, Education +5%. Note: Administrative and clerical roles show largest projected decline due to AI automation.]

SOURCE D (Small business owner, interview, 2023):
"I run a graphic design firm with six employees. When AI image generators came out, I thought we were finished. Instead, we've pivoted. We use AI for first drafts and rough concepts, which used to take 40% of our time. Now my designers focus on the creative direction, client relationships, and the kind of nuanced work that AI can't match. We're actually more profitable than before — but I had to let go of two junior designers whose roles were primarily production work. That's the uncomfortable truth."

SOURCE E (World Economic Forum, Future of Jobs Report, 2023):
The Forum estimates that AI will displace 85 million jobs globally by 2025 but create 97 million new roles. The net positive masks significant disruption: displaced workers are often not the same people who fill new roles. New positions require different skills, often in different geographic locations. Without proactive reskilling programs, AI adoption risks creating a permanent underclass of displaced workers alongside a thriving class of AI-complementary professionals.

SOURCE F (Public comment, community meeting on AI and local employment, 2023):
"Everyone talks about 'reskilling' like it's simple. I'm 54 years old. I drove a truck for 30 years. Now they want me to learn to code? My town doesn't have a community college within 50 miles. The tech companies making billions off AI should be required to fund the transitions they're causing — not just hand out pamphlets about 'lifelong learning.'" """,
    },

    # ===== B2 Gate Passages =====

    "SYN-10": {
        "id": "SYN-10",
        "author": "Various",
        "title": "Healthcare Access and Equity source set",
        "date": "Various",
        "course": "B2",
        "usage": "L21 gate (synthesis) -- RESERVED",
        "text": """SOURCE A (Kaiser Family Foundation, 2023):
Despite the Affordable Care Act's expansion of coverage, approximately 27 million Americans remain uninsured. The uninsured rate varies dramatically by state, ranging from 2.5% in Massachusetts to 18% in Texas. Key factors in coverage gaps include: states that declined Medicaid expansion, undocumented immigrants ineligible for marketplace subsidies, and the "family glitch" where employer-sponsored coverage is deemed affordable based on employee-only costs even when family premiums are unaffordable.

SOURCE B (Dr. Atul Gawande, surgeon and public health researcher, 2022):
"The fundamental problem with American healthcare is not access alone — it's that we've built a system optimized for acute intervention rather than prevention. We spend $4.3 trillion annually, more per capita than any nation, yet rank 46th in life expectancy. Universal coverage would help, but without restructuring toward preventive and primary care, we'd simply be giving more people access to a broken system. The countries with the best health outcomes invest in community health workers, preventive screenings, and social determinants — housing, nutrition, education — not just hospitals and specialists."

SOURCE C (Infographic, Commonwealth Fund, 2023):
[Comparison of healthcare systems: U.S. spends $12,555 per capita, next highest (Germany) spends $7,383. U.S. has 2.6 physicians per 1,000 people vs. OECD average of 3.7. U.S. life expectancy 76.4 years vs. OECD average 80.3. U.S. infant mortality 5.4/1,000 vs. OECD average 4.5/1,000. U.S. is only high-income country without universal health coverage.]

SOURCE D (Rural hospital administrator, testimony to Congress, 2023):
"In the past decade, 136 rural hospitals have closed. My hospital serves three counties — 45,000 people across 2,000 square miles. We're the only emergency room within 90 minutes. Last year we operated at a $2 million loss. Medicare and Medicaid reimburse below our costs. Our uninsured rate is 22%. When people can't pay, we still treat them — that's both our legal obligation and our moral calling. But the math doesn't work. If we close, the nearest trauma center is 94 miles away. People will die on the highway."

SOURCE E (Health insurance industry analysis, 2023):
Market-based approaches to healthcare have driven significant innovations in efficiency, patient experience, and specialized care. Competition between insurers has led to the development of telehealth platforms, wellness programs, and value-based care models. However, administrative costs consume 15-30% of healthcare spending in the private insurance model, compared to 2-5% in single-payer systems. The challenge is preserving innovation incentives while reducing the administrative burden that inflates costs without improving outcomes.

SOURCE F (Community health worker, urban clinic, 2023):
"My patients don't need another specialist referral. They need someone to drive them to their appointments. They need their prescriptions to cost less than their rent. I had a patient skip her diabetes medication for three months because she had to choose between insulin and keeping the lights on for her kids. By the time she came back, she needed an amputation. That amputation cost the system $250,000. Her insulin would have cost $3,000. We know how to prevent these outcomes. We just don't fund prevention."

SOURCE G (Economist, health policy think tank, 2023):
"The debate between universal coverage and market-based reform presents a false binary. Every successful healthcare system in the world uses a hybrid model. Germany has competing private insurers operating within a universal mandate. Singapore combines government subsidies with mandatory health savings accounts. The question isn't 'government vs. market' — it's what specific combination of public and private mechanisms produces the best outcomes for a given population at a sustainable cost." """,
    },

    "SP-035": {
        "id": "SP-035",
        "author": "Chief Joseph / William Apess",
        "title": "Chief Joseph's Surrender Speech and An Indian's Appeal for Justice (excerpts)",
        "date": "1877 / 1833",
        "course": "B2",
        "usage": "L22 gate (rhetorical analysis) -- RESERVED",
        "text": """CHIEF JOSEPH, "SURRENDER SPEECH" (1877):
Tell General Howard I know his heart. What he told me before, I have it in my heart. I am tired of fighting. Our chiefs are killed. Looking Glass is dead. Toohoolhoolzote is dead. The old men are all dead. It is the young men who say, "Yes" or "No." He who led the young men is dead. It is cold, and we have no blankets. The little children are freezing to death. My people, some of them, have run away to the hills, and have no blankets, no food. No one knows where they are — perhaps freezing to death. I want to have time to look for my children, and see how many of them I can find. Maybe I shall find them among the dead. Hear me, my chiefs! I am tired. My heart is sick and sad. From where the sun now stands I will fight no more forever.

WILLIAM APESS, "AN INDIAN'S LOOKING-GLASS FOR THE WHITE MAN" (1833):
Having been born in the woods, schooled by the elements, and rocked by the winds of winter, I am pleased to address this audience on the subject of the Indian's rights. I would ask you, If you are not a people who follow the example and precepts of the Savior, how is it that you have such a disregard for the rights of the poor Indian? Is there not enough in that little book, the Bible, to convince you? If you had not a heart of stone, you would consider these things.

Now let me ask you, white man, if it is a disgrace to eat, drink, and sleep with the image of God, or sit, or walk and talk with them. Or have you the folly to think that the white man, being one in fifteen or sixteen, is the only beloved image of God? Assemble all nations together in your imagination, and then let the whites be seated among them, and then let us look for the whites, and I doubt not it would be hard finding them; for amongst the multitude of nations, they would appear to be no more than a handful.

Now suppose these skins were put together, and each skin had its national crimes written upon it — which skin do you think would have the greatest? I will ask one question more. Can you charge the Indians with robbing a nation almost of their whole continent, and murdering their women and children, and then depriving the remainder of their lawful rights, that nature and God require them to have? And to cap the climax, rob another nation to till their grounds and welter out their days under the lash with hunger and fatigue?""",
    },
}


def get_passage(passage_id: str) -> dict | None:
    """Look up a passage by ID."""
    return PASSAGES.get(passage_id)


def get_passage_text(passage_id: str) -> str | None:
    """Get just the passage text by ID."""
    p = PASSAGES.get(passage_id)
    return p["text"] if p else None


def list_passages() -> list[dict]:
    """List all available passages (metadata only, no text)."""
    return [
        {
            "id": p["id"],
            "author": p["author"],
            "title": p["title"],
            "course": p["course"],
            "usage": p["usage"],
        }
        for p in PASSAGES.values()
    ]
