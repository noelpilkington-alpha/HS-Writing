"""
mastery_prompts_g11.py  -  the AUTHORED, task-specific PP100 mastery prompt for every G11 lesson.

Decision (Noel 2026-07-14, same rule as G9): the PP100 mastery task must (a) assess the exact skill the lesson
taught, and (b) be a FRESH held-out task, not a re-submit of the in-lesson write. A generic "apply the skill to
the new source" instruction fails both. So each lesson gets a REAL task on a held-out source: a concrete claim to
scope or qualify, a provided draft to diagnose and revise, a stated rhetorical-analysis task, a source set to
synthesize, given perspectives to weigh, etc. All content is own-words; any source facts are kept generic.

Single source of truth: the G11 pusher reads L.mastery if the lesson file sets it, else falls back to
MASTERY[L.id] here. The held-out `source` id must be a stimulus the lesson's own taught/transfer did NOT use, so
the task cannot be a re-submit. `unit`/`rubric_ref` keep the graded shape; rubric_ref = "rc.4trait" (Regents 4-criterion CCSS; G11/G12 moved off AP).
prompt_html is rendered by gated_reading._render_body (same typography as the in-article writes). No em dashes.

Held-out sources are drawn from the shared ACC pool. For source-free (C.11.06) and multi-perspective (C.11.07)
lessons, whose taught/transfer prompts are not in the pool, the concrete material (the general prompt, or the set
of perspectives) is authored inline in the _box so the task is doable regardless of the inlined stimulus.
"""

# ---- small inline-styled builders (copied verbatim from mastery_prompts_g9.py) ---------------------------------
def _p(t):
    return f'<p style="margin:0 0 8px;">{t}</p>'


def _box(label, text, tone="red"):
    """A set-apart block: red-dashed for a provided weak draft / vague claim the student must fix; teal for a
    given claim or evidence the student must use."""
    if tone == "teal":
        border, bg, lc, tc = "#0d9488", "#f0fdfa", "#0f766e", "#0f2f28"
    else:
        border, bg, lc, tc = "#dc2626", "#fef2f2", "#991b1b", "#1f2a44"
    return (f'<div style="margin:8px 0;padding:10px 14px;background:{bg};border:1px dashed {border};'
            f'border-radius:8px;">'
            f'<div style="font-size:12px;font-weight:700;color:{lc};margin-bottom:4px;">{label}</div>'
            f'<div style="font-size:15px;color:{tc};line-height:1.5;">{text}</div></div>')


def _task(*lines):
    return "".join(_p(l) for l in lines)


_INTRO = _p("This is your mastery task, on a topic you have not written on in this lesson.")

# ---- per-lesson authored mastery ----------------------------------------------------------------------------
MASTERY = {

    # C1101-0001 - scope a sweeping claim (sentence). Held-out: PHONEBAN (lesson used the AIWORKFORCE frames).
    "ACC-W1112-L-G11-C1101-0001": {"source": "ACC-W910-ARG-LESSON-PHONEBAN", "unit": "sentence",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("A sweeping claim to scope:",
               '"Phones always ruin students\' focus, so every school everywhere should ban them for everyone."')
        + _task("This claim overreaches: always, every, everyone. Nobody has to prove that much, so it is not "
                "defensible.",
                "Rewrite it into ONE scoped claim that narrows which case, whom, or when it covers, using a reason "
                "from the source above. Write one sentence.")},

    # C1101-0002 - nuanced not-X-but-Y claim (sentence). Held-out: SCHOOLLUNCH.
    "ACC-W1112-L-G11-C1101-0002": {"source": "ACC-W910-ARG-LESSON-SCHOOLLUNCH", "unit": "sentence",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("A flat, one-sided claim:",
               '"Free school lunch for every student is simply the right thing to do."')
        + _task("This asserts one side but never marks off the close position it is rejecting, so the exact "
                "stance is fuzzy.",
                "Rewrite it in the not-X-but-Y shape: name the near-miss position you reject, then state what you "
                "actually claim, using a reason from the source above. Write one sentence.")},

    # C1101-0003 - qualify without waffling (sentence). Held-out: WATERTRADEOFF.
    "ACC-W1112-L-G11-C1101-0003": {"source": "ACC-W910-ARG-LESSON-WATERTRADEOFF", "unit": "sentence",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("An absolute claim to qualify:",
               '"In a drought, a region must always protect water for growing food before protecting water for generating power."')
        + _task("The word always makes this indefensible, but a claim that hedges until it says nothing is no "
                "better.",
                "Rewrite it as a qualified claim that names its limit with a qualifier and a reason (in most "
                "cases, or when..., because...) yet still commits to a side, using the source above. Write one "
                "sentence.")},

    # C1101-0004 - build a line of reasoning (paragraph). Held-out: WORKFORCEINVEST.
    "ACC-W1112-L-G11-C1101-0004": {"source": "ACC-W910-ARG-LESSON-WORKFORCEINVEST", "unit": "paragraph",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("The claim to build toward:",
               "Public money should go first to preparing more workers for the fastest-growing fields rather "
               "than to cushioning the workers those changes leave behind.",
               "teal")
        + _task("Write ONE paragraph that builds a LINE OF REASONING toward this claim, using evidence from the "
                "source above.",
                "Each reason must build on the one before it, so the paragraph moves toward the claim step by "
                "step, rather than stacking unconnected points as a list.")},

    # C1101-0005 - earn the claim: develop a thin assertion (paragraph). Held-out: COMMUNITYSERVICE.
    "ACC-W1112-L-G11-C1101-0005": {"source": "ACC-W910-ARG-LESSON-COMMUNITYSERVICE", "unit": "paragraph",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("A thin, under-argued paragraph:",
               "Required community service is good for students. It teaches them useful things. Schools should "
               "require it before graduation.")
        + _task("This claim is asserted, not earned: it has almost no reasoning to carry it.",
                "Develop it into a paragraph with ENOUGH reasoning to carry the claim, using evidence from the "
                "source above, so the claim is earned rather than merely stated.")},

    # C1103-0006 - name a choice + its effect on the audience (sentence). Held-out: RA-SINGLE-0002.
    "ACC-W1112-L-G11-C1103-0006": {"source": "ACC-W910-RA-SINGLE-0002", "unit": "sentence",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Your rhetorical-analysis task:",
               "The source above is an excerpt from an 1896 speech delivered to the delegates of a national "
               "political convention, an audience the speaker needed to win to his side. Analyze ONE rhetorical "
               "choice the author makes for that audience.", "teal")
        + _task("Write ONE sentence that names a specific rhetorical choice the author makes and explains why it "
                "works on that AUDIENCE, the convention delegates listening to him.",
                "Analyze the choice and its effect on that audience, not the content or subject the text is "
                "about. Write one sentence.")},

    # C1103-0007 - chain choice to effect to purpose (paragraph). Held-out: RA-SINGLE-0003.
    "ACC-W1112-L-G11-C1103-0007": {"source": "ACC-W910-RA-SINGLE-0003", "unit": "paragraph",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Your rhetorical-analysis task:",
               "Analyze how one choice by the author of the source above serves a larger purpose.", "teal")
        + _task("Write ONE paragraph that chains the move all the way: name the author's choice, its effect on "
                "the audience, and the PURPOSE that effect serves.",
                "Do not stop at naming the device; carry it through to why the author wanted that effect.")},

    # C1103-0008 - trim the quote, then frame it (paragraph). Held-out: RA-SINGLE-0001.
    "ACC-W1112-L-G11-C1103-0008": {"source": "ACC-W910-RA-SINGLE-0001", "unit": "paragraph",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Your task:",
               "Analyze one moment in the source above where the author's exact wording does work.", "teal")
        + _task("From the source above, choose a phrase worth quoting and TRIM it to the smallest piece that "
                "earns its place.",
                "Then FRAME it in a paragraph you build: set it up before the quote and interpret it after, so it "
                "connects to your point. Do not drop in a long quote that floats.")},

    # C1103-0009 - check: rhetorical analysis or summary, then revise (paragraph). Held-out: RA-SINGLE-0002.
    "ACC-W1112-L-G11-C1103-0009": {"source": "ACC-W910-RA-SINGLE-0002", "unit": "paragraph",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("A paragraph that slips into summary:",
               "The author of the source above argues that ordinary working people count as business men, praises "
               "the pioneers who settled the West, and says the people will beg no longer but defy their opponents. "
               "He also defends the income tax as fair. The speech covers a lot of ground and makes its point clearly.")
        + _task("This paragraph SUMMARIZES the text; it never analyzes the author's rhetorical choices.",
                "Revise it into a real rhetorical-analysis paragraph about the source above: name a choice, frame "
                "a trimmed piece of evidence, and give its effect on the audience and the purpose it serves.")},

    # C1108-0010 - judge a source on grounds (sentence). Held-out: INFO-LESSON-HIGHWAYS (a held-out informational
    # source that names its producer in-text and reports checkable federal figures, so the taught who+backed frame
    # transfers; the lesson's own taught=ENERGYMIX and transfer=WATERUSE, so HIGHWAYS is not a re-submit).
    "ACC-W1112-L-G11-C1108-0010": {"source": "ACC-W910-INFO-LESSON-HIGHWAYS", "unit": "sentence",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Your task:",
               "Judge the credibility of the source above.", "teal")
        + _task("Write ONE sentence that assesses this source on GROUNDS: who produced it and whether its claims "
                "are backed.",
                "Do not trust it just because it sounds official. Base your judgment on evidence in the source. "
                "Write one sentence.")},

    # C1108-0011 - name strengths and limits (sentence). Held-out: INFO-LESSON-RECYCLING (a held-out informational
    # source with national EPA totals and shares, so the taught strengths-and-limits frame - strong FOR national
    # totals, limited on any single place - transfers directly; the lesson's own taught=WATERUSE and
    # transfer=ENERGYMIX, so RECYCLING is not a re-submit). Task matches the two-part move the lesson practices.
    "ACC-W1112-L-G11-C1108-0011": {"source": "ACC-W910-INFO-LESSON-RECYCLING", "unit": "sentence",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Your task:",
               "Weigh what the source above is good for and where it falls short.", "teal")
        + _task("Write ONE sentence that names BOTH a strength and a limit of this source: what to trust it for "
                "(a use its figures are strong evidence for) and where it falls short (what its national figures "
                "leave out or cannot tell you about any single place).",
                "Do not accept or reject it whole. Write one sentence.")},

    # C1102-0012 - full synthesis: one argument from the set (multi_paragraph). Held-out: SYNTH-SET-0002.
    "ACC-W1112-L-G11-C1102-0012": {"source": "ACC-W910-SYNTH-SET-0002", "unit": "multi_paragraph",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Your task:",
               "Synthesize the source set above.", "teal")
        + _task("Write a synthesis across the source set above that draws three or more of the sources into ONE "
                "argument the set builds together, one that no single source states on its own.",
                "Do not survey the sources one by one; make them serve a single argument.")},

    # C1102-0013 - weave by point, do not tour (multi_paragraph). Held-out: SYNTH-SET-0001.
    "ACC-W1112-L-G11-C1102-0013": {"source": "ACC-W910-SYNTH-SET-0001", "unit": "multi_paragraph",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Your task:",
               "Synthesize the source set above, organized by point.", "teal")
        + _task("Write a synthesis from the source set above organized BY POINT, with several sources meeting on "
                "each point (woven together).",
                "Do not organize it source by source with one paragraph per source (a tour).")},

    # C1102-0014 - weave the argument, weight the sources (essay). Held-out: SYNTH-SET-0002.
    "ACC-W1112-L-G11-C1102-0014": {"source": "ACC-W910-SYNTH-SET-0002", "unit": "essay",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Your task:",
               "Write a full synthesis essay on the source set above.", "teal")
        + _task("Write a full multi-source synthesis that weaves ONE argument from the set AND weights each "
                "source by what it is good for and where it falls short.",
                "Do not lean on every source equally; let the stronger sources carry more of the argument.")},

    # C1103-0015 (kc C.11.02) - predict own score, then name the gap (essay). Held-out: SYNTH-SET-0001.
    "ACC-W1112-L-G11-C1103-0015": {"source": "ACC-W910-SYNTH-SET-0001", "unit": "essay",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Your task:",
               "Write a full synthesis on the source set above, then grade your own work.", "teal")
        + _task("Write a full synthesis that weaves ONE argument from the source set above.",
                "Before you submit, PREDICT your own score row by row (Development and Evidence, each 1 to 4), "
                "giving a reason for each row from what your writing actually does.",
                "Then re-score your finished draft carefully against those same two rows, and name the GAP "
                "between your prediction and your honest re-score, saying what caused it.")},

    # C1102-0016 - mid-gate: independent full synthesis (essay). Held-out: SYNTH-LESSON-0001.
    "ACC-W1112-L-G11-C1102-0016": {"source": "ACC-W1112-SYNTH-LESSON-0001", "unit": "essay",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Your gate task (follow THIS, not the prompt printed inside the source set):",
               "The three sources above are labeled Source 1, Source 2, and Source 3. On your own, plan and "
               "write a full synthesis ACROSS the set.", "teal")
        + _task("This is the mid-course gate. Independently plan, draft, and self-check a full multi-source "
                "synthesis, using at least two of the three labeled sources above.",
                "Do the synthesis move the unit taught: name the ONE claim the set jointly supports, weave "
                "evidence from more than one source to build it, and lean on each source where it is strong "
                "while naming where it is limited. This is a descriptive synthesis of what the sources show, not "
                "a debate where you pick one side. Run your self-check before you submit.")},

    # C1104-0017 (kc C.11.06) - source-free: position + own example (sentence). SOURCE-FREE: no passage inlined
    # (an inlined passage would contradict the "do not use any passage" instruction); the general prompt is in-box.
    "ACC-W1112-L-G11-C1104-0017": {"source": None, "unit": "sentence",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("A general prompt (no passage to quote):",
               "Do smartphones help or hurt the way people your age pay attention?", "teal")
        + _task("This is a SOURCE-FREE task. Do not use any passage; argue from your own knowledge.",
                "Write ONE sentence that takes a defensible position on the question and anchors it to a "
                "specific example from your own reading, studies, or experience, rather than arguing in "
                "generalities. Write one sentence.")},

    # C1104-0018 - source-free: develop one specific example (paragraph). No held-out `source`: this is a
    # SOURCE-FREE task, so attaching a passage would contradict the "do not use any passage" instruction. The
    # fresh topic (community service, unused in the lesson) supplies the held-out material inline in the _box.
    "ACC-W1112-L-G11-C1104-0018": {"unit": "paragraph",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("A general prompt (no passage to quote):",
               "Should schools require students to complete community service in order to graduate?", "teal")
        + _task("This is a SOURCE-FREE task. Argue from your own knowledge; do not use any passage.",
                "Write ONE paragraph that supports your position with a single specific, developed example from "
                "your own knowledge, one that is named, detailed, and tied to the claim, rather than a vague "
                "generality.")},

    # C1104-0019 - full source-free argument essay (essay). No held-out `source`: this is a SOURCE-FREE task,
    # so inlining a passage would contradict the "do not use any passage" instruction. The fresh topic (school
    # lunch, unused in the lesson) supplies the held-out material inline in the _box.
    "ACC-W1112-L-G11-C1104-0019": {"unit": "essay",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("A general prompt (no passage to quote):",
               "Should public schools provide free lunch to every student, regardless of family income?", "teal")
        + _task("This is a SOURCE-FREE task. Argue entirely from your own knowledge; do not use any passage.",
                "Plan and write a complete argument essay: a defensible thesis carried across the body "
                "paragraphs by specific, developed examples from your own reading, studies, or experience.")},

    # C1105-0020 (kc C.11.07) - weigh perspectives, stake your own (sentence). SOURCE-FREE: this multi-perspective
    # task is argued from own knowledge, so no passage is attached. (The former WATERTRADEOFF passage framed water
    # as a two-way food-vs-power trade-off, which does not match and actively misleads against the three farms /
    # cities / rivers perspectives authored inline below.) The three perspectives are self-contained in the _box.
    "ACC-W1112-L-G11-C1105-0020": {"source": None, "unit": "sentence",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Three perspectives on how a dry region should share its limited water:",
               "(1) Farms should get first claim, since they grow the food everyone depends on. "
               "(2) Cities should get first claim, since that is where most people live. "
               "(3) Some water should stay in the rivers, since the ecosystem collapses without it.", "teal")
        + _task("Weigh these perspectives against each other and stake YOUR OWN position in relation to them.",
                "Do not summarize the perspectives one by one. Write one sentence.")},

    # C1105-0021 - weigh a perspective against your own (paragraph). Held-out: PHONEBAN.
    "ACC-W1112-L-G11-C1105-0021": {"source": "ACC-W910-ARG-LESSON-PHONEBAN", "unit": "paragraph",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("A given perspective:",
               "Schools should ban phones outright, because any phone in the room splits students' attention.",
               "teal")
        + _task("Write ONE body paragraph that weighs this perspective against your own position.",
                "Concede what holds in it, show where it falls short, and advance your own view with a specific "
                "example.")},

    # C1105-0022 - full multi-perspective essay (essay). Held-out: WORKFORCEINVEST.
    "ACC-W1112-L-G11-C1105-0022": {"source": "ACC-W910-ARG-LESSON-WORKFORCEINVEST", "unit": "essay",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Three perspectives on where a society should spend first as technical fields grow faster than "
               "the economy:",
               "(1) Prepare the next generation first: widen the pipeline into the fast-growing technical fields "
               "through schools, training, and apprenticeships, because that treats the cause rather than the "
               "symptom. "
               "(2) Protect the displaced first: fund transition support for the workers whose industries are "
               "shrinking now, because a society is judged by what happens to the people a change harms. "
               "(3) Favor neither side wholesale: set a fixed rule for splitting a limited budget between "
               "preparation and protection, because both aims are humane and a budget rarely funds both fully.",
               "teal")
        + _task("Plan and write a complete multi-perspective essay.",
                "It must have a thesis that stakes your own position, body paragraphs that weigh these "
                "perspectives to build it (concede, limit, advance with an example), and a conclusion.")},

    # C1106-0023 (kc C.11.05) - budget your minutes across an essay (essay). Held-out: SCHOOLLUNCH.
    "ACC-W1112-L-G11-C1106-0023": {"source": "ACC-W910-ARG-LESSON-SCHOOLLUNCH", "unit": "essay",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Your task and window:",
               "You have 40 minutes. Using the source above, write a full argument essay on whether free school "
               "lunch should be universal.", "teal")
        + _task("Before you draft, write a TIME BUDGET that allots minutes to reading, planning, drafting, and "
                "checking so the whole essay fits the 40-minute window.",
                "Then write the essay to that budget, rather than drafting until time runs out. Show the budget "
                "first, then the essay.")},

    # C1106-0024 - make a fast plan: position plus ordered points (essay). Held-out: WATERTRADEOFF.
    "ACC-W1112-L-G11-C1106-0024": {"source": "ACC-W910-ARG-LESSON-WATERTRADEOFF", "unit": "essay",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Your task:",
               "Using the source above, argue how a dry region should share its limited water.", "teal")
        + _task("First make a QUICK two- or three-line plan (your position plus your ordered points) that will "
                "steer the draft.",
                "Do not skip the plan, and do not write a full-page outline that eats the window. Then write the "
                "essay to that plan. Show the plan first, then the essay.")},

    # C1107-0025 (kc C.11.04) - put the strongest reason last (sentence). Held-out: WORKFORCEINVEST.
    "ACC-W1112-L-G11-C1107-0025": {"source": "ACC-W910-ARG-LESSON-WORKFORCEINVEST", "unit": "sentence",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("A reason string in its current order:",
               "Training programs are worth funding because they measurably raise the wages of the workers who "
               "finish them, because they cost relatively little to launch, and because they are popular with "
               "voters.")
        + _task("The strongest reason (higher wages) is buried up front, and the string trails off on the weakest "
                "(popular with voters).",
                "Rewrite the reason string so the strongest reason lands LAST, in the emphatic position, and cut "
                "the weak filler reason. Write one sentence.")},

    # C1107-0026 - cut the words that do no work (sentence). Held-out: COMMUNITYSERVICE.
    "ACC-W1112-L-G11-C1107-0026": {"source": "ACC-W910-ARG-LESSON-COMMUNITYSERVICE", "unit": "sentence",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("A padded sentence:",
               '"In my own personal opinion, it really does seem that required community service is basically a '
               'very important and truly necessary thing that all students everywhere should absolutely have to '
               'do."')
        + _task("Run a CONCISION pass on this sentence: cut the empty intensifiers, the redundant pairs, and the "
                "throat-clearing opener, without losing the meaning.",
                "Do not pad it further. Write one tighter sentence.")},

    # C1106-0027 (kc C.11.05) - rehearse a full synthesis under your own budget (essay). Held-out: SYNTH-LESSON-0001.
    # The held-out set is auto-inlined above as one block, so the three titled sources can read as a single essay.
    # Labeled here (Source 1/2/3 by title) so the taught move (tag each point with the source that carries it) has
    # clear referents: the three sources are the three titled sections, not the USGS/EPA/EIA citations inside them.
    "ACC-W1112-L-G11-C1106-0027": {"source": "ACC-W1112-SYNTH-LESSON-0001", "unit": "essay",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("The set above is three sources:",
               "Source 1, \"Where the Nation's Water Goes,\" frames the national water budget. "
               "Source 2, \"The Water That Keeps the Lights On,\" argues for protecting the water that cools power "
               "plants. Source 3, \"The Water That Grows the Food,\" argues for protecting the water that irrigates "
               "crops. Treat these three titled sources as your set, and tag each point in your plan with the one "
               "that carries it (the citations to the USGS, EPA, and EIA are evidence inside the sources, not "
               "separate sources).",
               "teal")
        + _box("Your task:",
               "Write a full synthesis on these three sources, end to end, under a budget you set yourself.",
               "teal")
        + _task("Budget the stages (reading, planning, drafting, checking) for the time you give yourself.",
                "Then fast-plan the ONE argument the set builds, weave the three sources by point and weight them, "
                "and check at the end. Show your budget first, then the synthesis.")},

    # C1106-0028 (kc C.11.05) - match the moves to the task type (essay). Both prompts authored inline; no
    # external passage, so the source-free vs multi-perspective spot stays clean and the student names it.
    "ACC-W1112-L-G11-C1106-0028": {"source": None, "unit": "essay",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Two prompts:",
               "Prompt A: 'Does technology make people more connected or less connected?' "
               "Prompt B: respond to these three views on phones in school. "
               "(1) Ban them outright; they split attention. (2) Allow them but teach self-control. "
               "(3) Leave the rule to each teacher.", "teal")
        + _task("First, NAME the task type of each prompt yourself (source-free, or multi-perspective), and say "
                "how you can tell.",
                "Then write a complete essay in response to Prompt B, running the moves its task type rewards: a "
                "thesis that stakes your position, body paragraphs that weigh the given perspectives against one "
                "another and position your own claim in relation to them, and a conclusion.")},

    # C1103-0029 (kc C.11.05) - name the task type before you write (paragraph). This is a pure task-type
    # CLASSIFICATION task: the held-out material IS the three fresh quoted prompts below, which the student
    # classifies by their tell. No inlined stimulus source (a "New source" block would be irrelevant noise the
    # task never uses and would collide with prompt (1)'s quoted "four sources below").
    "ACC-W1112-L-G11-C1103-0029": {"source": "", "unit": "paragraph",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Three prompts:",
               "(1) 'Read the four sources below and write an essay that uses them to develop your position.' "
               "(2) 'Some argue success comes from talent, others from effort. Take a position, drawing on your "
               "own knowledge and experience.' "
               "(3) 'Below are three given perspectives on the issue. Read them, then develop your own position "
               "in relation to them.'", "teal")
        + _task("For each prompt, name whether it is synthesis (a source set to combine), source-free (a general "
                "question answered from your own knowledge), or multi-perspective (a set of perspectives to "
                "weigh).",
                "State the TELL that gave each one away. Write one short paragraph.")},

    # C1102-0030 - COURSE GATE: name the task type, then write the right essay (essay). Held-out: SFA-PROMPT-0004
    # (source-free ARGUMENT). Fixed 2026-07-16: was SYNTH-SET-0002, an unlabeled SYNTHESIS set with no stated
    # issue - but the gate REHEARSES and certifies a source-free argument (target: "argue a position from own
    # knowledge"; taught prompt SFA-PROMPT-0002 is prompt_only argument). Grading it on a synthesis set tests a
    # type the gate never rehearses. Per COURSE_MASTERY17_TRIAGE C1102-0030 fix option 1: align the gate PP100 to
    # what the gate rehearses. The held-out prompt is a self-contained argument prompt (states its own issue), so
    # the "name the type, then write the essay its moves reward" skill is exercised on a genuinely cold argument.
    "ACC-W1112-L-G11-C1102-0030": {"source": "ACC-W910-SFA-PROMPT-0004", "unit": "essay",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("A cold prompt:",
               "Read the prompt above and write the essay it calls for.", "teal")
        + _task("This is the course gate. First, name the TASK TYPE from its tell (what kind of prompt is this, "
                "and does it give you sources or ask you to argue from your own knowledge?).",
                "Then write the essay its moves reward, planning first and running a self-check at the end. Say "
                "which type it is before you begin.")},

    # C1103-0031 - full rhetorical-analysis essay (essay). Held-out: RA-SINGLE-0003.
    "ACC-W1112-L-G11-C1103-0031": {"source": "ACC-W910-RA-SINGLE-0003", "unit": "essay",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Your task:",
               "The source above is an excerpt from Ralph Waldo Emerson's essay \"Self-Reliance,\" published in "
               "1841 for a general reading audience of his day, in which he urges readers to trust their own "
               "inner voice and resist the pressure to conform. Analyze the rhetorical choices Emerson makes to "
               "move that audience.", "teal")
        + _task("Plan and write a complete rhetorical-analysis essay.",
                "Include: an introduction that names the author (Emerson) and the occasion (his 1841 essay to a "
                "general reading audience) and states a thesis naming his overall rhetorical purpose; body "
                "paragraphs that each move from a choice to its effect on the audience to the purpose it serves, "
                "with evidence trimmed and framed; and a conclusion that ties the choices back to the one "
                "purpose.")},
}
