"""
Production-length opposing-pair ARGUMENT stimulus for the G10 test bank.
Topic: Should the US build more nuclear power?  (PRODUCTION version of the ~200-word demo in
stimulus_contract.py's __main__.) Family=opposing, mode=argument. Two original 500-900 word
passages, G10 register, each conceding the other's point. Every figure traces to a fetched
federal page (US EIA, US DOE, US GAO, US NRC), verified live 2026-07-07. Runs itself through
the QC harness and reports. No em dashes in prose.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, FactSource, qc_stimulus, qc_report

# --- Source A: pro-expansion, EIA/DOE operations data -----------------------------------------
PASSAGE_A = (
"When Americans turn on a light or charge a phone, the power often comes from a nuclear plant. "
"Nuclear energy has been a quiet workhorse of the American grid for decades. The U.S. Energy "
"Information Administration reports that nuclear plants made about 19 percent of the nation's "
"electricity in 2023. That is close to one-fifth of all the power the country used. And that share "
"has stayed steady for years. The same agency reports that, as of early 2026, 57 commercial nuclear "
"plants ran 96 reactors in 28 states. Supporters say this record is the very reason to build more.\n\n"

"The strongest point in favor of nuclear power is that it is reliable. Engineers measure how hard a "
"power source works with a number called the capacity factor. It shows how often a plant makes power "
"compared with how much it could make if it ran full-time. The U.S. Department of Energy reports that "
"nuclear plants ran at more than 92 percent of that limit in 2024. No other source ran as often. Coal "
"plants ran at about 42 percent. Natural gas plants ran at about 60 percent. Wind farms ran at about "
"34 percent, and solar farms ran at about 23 percent. The wind does not always blow, and the sun does "
"not always shine. But a country needs power every hour of every day. To supporters, a source that "
"runs almost all the time is worth far more than one that stops and starts.\n\n"

"That strength is even clearer when size is compared with output. The Department of Energy notes that "
"nuclear plants make up only about 8 percent of the country's power capacity. Yet those same plants "
"make close to a fifth of the electricity people actually use. In plain terms, nuclear delivers far "
"more than its size on paper. Few other sources come close to that steady record.\n\n"

"Supporters point to a second big benefit: clean air. Plants that burn coal or natural gas give off "
"carbon dioxide. That is the main gas linked to a warming climate. Nuclear reactors split atoms "
"instead of burning fuel. So they do not give off carbon dioxide while they run. A source that makes "
"about a fifth of the nation's power without that pollution, supporters argue, is a tool the country "
"should not throw away. As old coal plants close, they say, new reactors could take their place and "
"keep the lights on.\n\n"

"The country has also shown it can still build. The Energy Information Administration reports that the "
"newest American reactor is Vogtle Unit 4 in Georgia. It began running in April 2024. It joined a "
"plant that now runs four reactors, the most of any site in the nation. To supporters, Vogtle is proof "
"that large nuclear projects are still possible here, even if they are hard.\n\n"

"Supporters do not pretend that nuclear power is perfect. They agree the country still has no permanent "
"home for the dangerous waste that reactors leave behind. They accept that this problem is real and "
"must be solved. But they argue that the waste is a challenge to manage, not a reason to stop. The "
"waste already exists whether or not one new plant is built. For decades the current plants have run "
"safely while storing their used fuel on site. The demand for power never pauses. The need to cut "
"climate pollution is urgent. So supporters conclude that the wiser path is to keep building. A source "
"that runs more than 92 percent of the time, supplies close to a fifth of the grid, and adds no carbon "
"while it runs is, in their view, just what the country's future needs."
)

# --- Source B: anti-expansion, GAO/NRC waste and oversight watchdog ---------------------------
PASSAGE_B = (
"Nuclear power plants do something useful. They make large amounts of electricity without giving off "
"the carbon dioxide that pours from coal and gas plants. That is a real benefit, and few critics deny "
"it. Yet a serious problem has gone unsolved for more than forty years. A federal watchdog warns that "
"it should give the country pause before it builds more reactors. The United States still has no "
"permanent place to put the dangerous waste that nuclear plants make.\n\n"

"The waste is already large in scale, and it keeps growing. The U.S. Government Accountability Office "
"reports that about 86,000 metric tons of spent nuclear fuel sit in storage at 75 sites. This used "
"fuel is not gathered in one safe national place. Instead it stays where the power was made. It sits "
"at working and closed plants in 33 states, often near the towns that use the power. The pile grows by "
"about 2,000 metric tons each year as reactors keep running. In short, the country keeps making more "
"of a substance it does not yet know how to store for the long term.\n\n"

"What makes spent fuel so hard to handle is how long it stays dangerous. The U.S. Nuclear Regulatory "
"Commission explains that high-level nuclear waste stays harmful for a stunning length of time. Some "
"of the material in spent fuel breaks down fast, but some does not. One part of the fuel, plutonium, "
"has a half-life of about 24,000 years. That means half of its radiation fades only after 24,000 "
"years. Much of the danger in the waste remains even after 1,000 years have passed. A choice made "
"today, in other words, reaches thousands of years into the future.\n\n"

"The reason the waste has piled up is a long political failure. Under the Nuclear Waste Policy Act of "
"1982, the government promised to collect and bury the nation's spent fuel. The only site ever picked "
"for burial was Yucca Mountain in Nevada. But in 2010 the government halted work on Yucca Mountain. No "
"new plan has replaced it since. The Government Accountability Office calls the situation an impasse. "
"Policymakers have simply not been able to agree on a way forward.\n\n"

"That failure carries a steep price for taxpayers. The government promised to take the waste by a set "
"date, and it did not. So it broke a legal deal with the companies that own the reactors. To pay for "
"storing the fuel the government never collected, it has already paid those companies about 9 billion "
"dollars. That bill climbs every year the waste stays stuck at reactor sites. And none of that money "
"brings the country any closer to a real fix.\n\n"

"Critics who are cautious about nuclear power do not always want to shut down today's plants. Many "
"admit that nuclear power's clean-air record is real and worth a lot. Their objection is narrower, and "
"they argue it is harder to answer. The country already struggles to handle the waste it has. Even "
"now, the Nuclear Regulatory Commission reports that 19 reactors at 15 sites are being taken apart. "
"That work adds still more material that must be handled with care. Building many new reactors would "
"make still more waste that stays dangerous for thousands of years. And it would do so on top of a "
"backlog the government has failed to clear for four decades. Before the nation takes that step, these "
"critics ask a fair question. Why make more of a problem we have never solved? Until there is a real "
"plan and a real place for the waste, they argue, the wise choice is to fix the problem we already "
"have before we make it bigger."
)

rec = StimulusRecord(
    id="ACC-W910-ARG-OPP-0003",
    grade="9-10", mode="argument", family="opposing",
    modeling_anchor="Ohio ELA II / MD MCAP (opposing-view argument, pick-a-side)",
    acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "ACC.W.ARG.5", "CCSS.W.9-10.1", "CCSS.W.9-10.1.b", "TX-TEKS.EII.9.A"],
    prompt=("Weighing both sources, write an argumentative essay stating your position on whether the "
            "United States should build more nuclear power. Support your claim with specific evidence "
            "from both sources, and respond to at least one objection from the side you do not take."),
    passages=[
        Passage(title="The Case for Building More Nuclear Power",
                angle="pro-expansion; EIA/DOE operations and reliability data", text=PASSAGE_A),
        Passage(title="The Unsolved Problem of Nuclear Waste",
                angle="anti-expansion; GAO/NRC waste and oversight watchdog", text=PASSAGE_B),
    ],
    fact_sources=[
        FactSource("Nuclear share of US electricity in 2023", "19 percent", "US EIA",
                   "https://www.eia.gov/tools/faqs/faq.php?id=427&t=3",
                   "About 19% was from nuclear energy"),
        FactSource("Nuclear plants / reactors / states (early 2026)", "57 / 96 / 28", "US EIA",
                   "https://www.eia.gov/tools/faqs/faq.php?id=207&t=3",
                   "the United States had 57 commercially operated nuclear power plants with 96 nuclear power reactors in 28 states"),
        FactSource("Nuclear capacity factor in 2024", "92 percent", "US DOE",
                   "https://www.energy.gov/ne/articles/what-generation-capacity",
                   "producing reliable and secure power more than 92% of the time in 2024"),
        FactSource("Coal capacity factor in 2024", "42 percent", "US DOE",
                   "https://www.energy.gov/ne/articles/what-generation-capacity",
                   "a coal (42.36%)"),
        FactSource("Natural gas capacity factor in 2024", "60 percent", "US DOE",
                   "https://www.energy.gov/ne/articles/what-generation-capacity",
                   "natural gas (59.9%)"),
        FactSource("Wind capacity factor in 2024", "34 percent", "US DOE",
                   "https://www.energy.gov/ne/articles/what-generation-capacity",
                   "wind (34.3%)"),
        FactSource("Solar capacity factor in 2024", "23 percent", "US DOE",
                   "https://www.energy.gov/ne/articles/what-generation-capacity",
                   "solar (23.4%)"),
        FactSource("Nuclear share of total US generating capacity", "8 percent", "US DOE",
                   "https://www.energy.gov/ne/articles/what-generation-capacity",
                   "made up 8% of the country's total capacity"),
        FactSource("Newest US reactor online (Vogtle Unit 4)", "April 2024", "US EIA",
                   "https://www.eia.gov/tools/faqs/faq.php?id=207&t=3",
                   "Vogtle Unit 4 ... began commercial operation in April 2024"),
        FactSource("Spent nuclear fuel accumulated / sites", "86,000 metric tons / 75", "US GAO",
                   "https://www.gao.gov/products/gao-21-603",
                   "about 86,000 metric tons of spent nuclear fuel from commercial reactors stored at 75 U.S. sites"),
        FactSource("Spent fuel spread across states", "33 states", "US GAO",
                   "https://www.gao.gov/products/gao-21-603",
                   "stored on-site at 75 operating or shutdown nuclear power plants in 33 states"),
        FactSource("Annual growth of spent fuel", "2,000 metric tons", "US GAO",
                   "https://www.gao.gov/products/gao-21-603",
                   "an amount that grows by about 2,000 metric tons each year"),
        FactSource("Yucca Mountain licensing work halted", "2010", "US GAO",
                   "https://www.gao.gov/products/gao-21-603",
                   "in 2010, DOE terminated its efforts to license a repository at Yucca Mountain"),
        FactSource("Government paid reactor owners to store fuel", "9 billion", "US GAO",
                   "https://www.gao.gov/products/gao-21-603",
                   "the U.S. government has paid reactor owners about $9 billion for storage"),
        FactSource("Plutonium-239 half-life", "24,000 years", "US NRC",
                   "https://www.nrc.gov/reading-rm/doc-collections/fact-sheets/radwaste",
                   "Plutonium-239 has a half-life of 24,000 years"),
        FactSource("Reactors in decommissioning", "19 reactors / 15 sites", "US NRC",
                   "https://www.eia.gov/energyexplained/nuclear/us-nuclear-industry.php",
                   "According to the U.S. Nuclear Regulatory Commission, 19 commercial nuclear power reactors at 15 sites are in various stages of decommissioning"),
    ],
    provenance={"copyright": "own_authored",
                "rights": "public-domain-sourced (US EIA + US DOE + US GAO + US NRC)",
                "multi_source_verified": True, "authored": "2026-07-07"},
)

# --- Two-bucket migration: decompose the opposing pair into stance-tagged TEST singles ---------
# Each single is a composable member of proposition "prop_nuclear_power" (one pro, one con). The pair
# above (rec) is retained for backward compatibility; the singles are what the composer assembles from.
SINGLES = [
    StimulusRecord(
        id="ACC-W910-ARG-SINGLE-NUCLEAR-PRO",
        grade="9-10", mode="argument", family="single", bucket="test",
        modeling_anchor="Ohio ELA II / MD MCAP (opposing-view member)",
        acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "CCSS.W.9-10.1"],
        prompt="Read this source arguing in favor of building more nuclear power.",
        passages=[Passage(title=rec.passages[0].title, angle=rec.passages[0].angle, text=rec.passages[0].text)],
        fact_sources=[f for f in rec.fact_sources if f.org in ("US EIA", "US DOE")],
        provenance=dict(rec.provenance),
        topic_id="nuclear_power", proposition_id="prop_nuclear_power", stance="pro",
        form="staar", task_demand=3),
    StimulusRecord(
        id="ACC-W910-ARG-SINGLE-NUCLEAR-CON",
        grade="9-10", mode="argument", family="single", bucket="test",
        modeling_anchor="Ohio ELA II / MD MCAP (opposing-view member)",
        acc_tags=["ACC.W.ARG.1", "ACC.W.ARG.2", "CCSS.W.9-10.1"],
        prompt="Read this source arguing against building more nuclear power.",
        passages=[Passage(title=rec.passages[1].title, angle=rec.passages[1].angle, text=rec.passages[1].text)],
        fact_sources=[f for f in rec.fact_sources if f.org in ("US GAO", "US NRC")],
        provenance=dict(rec.provenance),
        topic_id="nuclear_power", proposition_id="prop_nuclear_power", stance="con",
        form="staar", task_demand=3),
]

if __name__ == "__main__":
    import re
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
    import readability_gate as rg
    qc_stimulus(rec)
    for p in rec.passages:
        wc = len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", p.text))
        lex = rg.analyze_text(p.text)["lexile_estimate"]
        print(f"passage '{p.title}': {wc} words, ~{lex}L")
    print(qc_report(rec))

    # decomposed stance singles
    assert len(SINGLES) == 2, "nuclear decomposes into 2 stance singles"
    stances = {x.stance for x in SINGLES}
    assert stances == {"pro", "con"}, "one pro, one con"
    for x in SINGLES:
        assert x.family == "single" and x.bucket == "test"
        assert x.proposition_id and x.topic_id and x.form
        qc_stimulus(x)
        assert x.qc["passed"], f"single {x.id} must pass QC: {x.qc.get('first_failure')}"
    print("nuclear SINGLES decomposition OK")

    sys.exit(0 if rec.qc["passed"] else 1)
