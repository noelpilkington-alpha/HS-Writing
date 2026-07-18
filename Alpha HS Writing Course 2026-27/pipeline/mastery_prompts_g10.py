"""
mastery_prompts_g10.py  -  the AUTHORED, task-specific PP100 mastery prompt for every G10 lesson.

Same decision as G9 (Noel 2026-07-14): the PP100 mastery task must (a) assess the exact skill the lesson
taught, and (b) be a FRESH held-out task, not a re-submit of the in-lesson write. A generic "apply the skill to
the new source" fails both (not-doable, skill-mismatched). So each lesson gets a REAL task on a held-out
source the lesson's own taught/transfer stimuli did NOT use: a concrete claim to make counterclaim-aware, a
provided draft to diagnose and revise, a source set to map or synthesize, a passage to analyze for craft, etc.

Held-out sources are drawn from the G10 pool and are always of a compatible kind: analysis lessons get an
analysis/rhetorical-analysis source, synthesis (C.10.06) lessons get a multi-perspective source set, argument
lessons get an argument-with-opposition source, revision/organization lessons get an informational source. All
content is own-words; source facts are referenced generically (no fabricated figures). No em dashes.

Single source of truth: the G10 pusher reads L.mastery if the lesson file sets it, else falls back to
MASTERY[L.id] here. The held-out `source` id must match the pusher's HELDOUT map so the same source is inlined
above this prompt. `unit`/`rubric_ref` keep the graded shape. prompt_html is rendered by
gated_reading._render_body (same typography as the in-article writes).
"""

# ---- small inline-styled builders (copied verbatim from mastery_prompts_g9.py) -----------------------------
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


_INTRO = _p("This is your mastery task, on a source you have not written on in this lesson.")

# ---- per-lesson authored mastery ----------------------------------------------------------------------------
MASTERY = {

    # C1001-0001 - counterclaim-aware claim "Although X, Y because Z" (sentence). Taught CONGESTION/DST -> held-out SCHOOLYEAR.
    "ACC-W910-L-G10-C1001-0001": {"source": "ACC-W910-ARG-OPP-LESSON-SCHOOLYEAR", "unit": "sentence",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("The question to take a side on:",
               "Should the school year be made longer?", "teal")
        + _task("Write ONE counterclaim-aware claim in the shape Although X, Y because Z.",
                "Name the strongest point on the OTHER side (X), then hold your position (Y) with a reason (Z) "
                "that actually answers that point, drawing on the source above.",
                "The reason must answer the objection, not ignore it. Write one sentence.")},

    # C1001-0002 - concede-and-hold, not concede-and-collapse (sentence). Taught DST/SCHOOLYEAR -> held-out CONGESTION.
    "ACC-W910-L-G10-C1001-0002": {"source": "ACC-W910-ARG-OPP-LESSON-CONGESTION", "unit": "sentence",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your position:",
               "Cities should charge drivers a fee to enter the busiest downtown zones at peak hours.", "teal")
        + _task("Write ONE sentence that concedes a REAL objection to this position and still holds it.",
                "Concede something true (a genuine cost or downside drivers face, drawn from the source), but do "
                "NOT concede so far that you abandon your own position.",
                "The finished sentence must still clearly support charging the fee. Write one sentence.")},

    # C1001-0003 - counterargument paragraph (paragraph). Taught SCHOOLYEAR/CONGESTION -> held-out DST.
    "ACC-W910-L-G10-C1001-0003": {"source": "ACC-W910-ARG-OPP-LESSON-DST", "unit": "paragraph",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your position:",
               "The country should stop switching clocks twice a year and keep one time all year.", "teal")
        + _task("Write ONE counterargument paragraph on this position, using the source above.",
                "State your position, fairly concede the strongest counterclaim, then ANSWER it with evidence "
                "from the source and reasoning.",
                "Answering means more than repeating your claim: show why your position holds even given that "
                "objection.")},

    # C1002-0004 - analytical claim (about craft) vs summary, from the verb (sentence). Taught HOUR/HIGHWAYS -> held-out DOUGLASS.
    "ACC-W910-L-G10-C1002-0004": {"source": "ACC-W910-ANALYSIS-LESSON-DOUGLASS", "unit": "sentence",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your task:",
               "Analyze how the author of the passage above builds his case, rather than summarizing what he "
               "says.", "teal")
        + _task("The task verb is ANALYZE, not summarize.",
                "Write ONE analytical claim: a claim ABOUT the author's craft, naming a choice he makes and its "
                "purpose, not a retelling of the content.",
                "It counts as analytical only if it points to a technique, not just to what happened. Write one "
                "sentence.")},

    # C1002-0005 - tell a craft claim from a content claim dressed up (sentence). Taught HOUR/RECYCLING -> held-out DOUGLASS.
    "ACC-W910-L-G10-C1002-0005": {"source": "ACC-W910-ANALYSIS-LESSON-DOUGLASS", "unit": "sentence",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("A content claim wearing analytical clothing:",
               '"The author shows that the holiday means something very different to the enslaved than it does to '
               'free citizens."')
        + _task("This looks analytical because it says the author shows, but it only restates the content.",
                "Rewrite it into a TRUE craft claim about the source above: name a specific technique the author "
                "uses and the effect that technique has, not just what the passage is about. Write one sentence.")},

    # C1002-0006 - name the device, then say its effect (sentence). Taught HOUR/WEATHER -> held-out DOUGLASS.
    "ACC-W910-L-G10-C1002-0006": {"source": "ACC-W910-ANALYSIS-LESSON-DOUGLASS", "unit": "sentence",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your task:",
               "Point to one specific device in the passage above and say what it does to the reader.", "teal")
        + _task("Do the core analytical move on the source above.",
                "Name the author's specific device (a choice you can actually point to in the text) AND state its "
                "effect on the reader.",
                "Do not just label the device: naming it is only half. Write one sentence.")},

    # C1002-0007 - reach the warrant/significance after device+effect (paragraph). Taught HIGHWAYS/WETLANDS -> held-out DOUGLASS.
    "ACC-W910-L-G10-C1002-0007": {"source": "ACC-W910-ANALYSIS-LESSON-DOUGLASS", "unit": "paragraph",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("A device and its effect (already written for you):",
               "The author stacks pointed questions on top of one another, which presses the audience and leaves "
               "them no comfortable place to stand.", "teal")
        + _task("You have the device and the effect. Now reach the WARRANT.",
                "Write a short paragraph that starts from this observation and explains WHY that effect matters "
                "to the author's purpose, grounding the why in the source above.",
                "The significance step, not just the effect, is what lifts analysis into the top band.")},

    # C1002-0008 - device-chain: link several choices to build one point (paragraph). Taught RECYCLING/WEATHER
    # -> held-out CHALLENGER. Fixed 2026-07-16 (readiness triage, genre/difficulty jump): the lesson models the
    # device-chain ONLY on plain expository texts (recycling, weather) whose choices are concrete and easy to
    # spot (an opening image, traced steps). The old held-out source (DOUGLASS, an 1852 oration dense with irony,
    # biblical allusion, and archaic diction) demanded locating a kind of "choice" the lesson never modeled. The
    # genre gate requires an ANALYSIS-mode held-out source for this type-4 lesson, so the source was swapped to
    # Reagan's 1986 Challenger address: analysis-mode (gate-clean), modern plain prose, with concrete, spottable
    # choices (naming each of the seven crew, the repeated "pioneers" framing, direct address to schoolchildren)
    # of the same accessibility the lesson taught on. Unused elsewhere in G10; not a taught source in L08.
    "ACC-W910-L-G10-C1002-0008": {"source": "ACC-W910-ANALYSIS-SINGLE-0003", "unit": "paragraph",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your single analytical point:",
               "The author consoles a grieving nation while reassuring it that space exploration will go on.", "teal")
        + _task("Sustain this ONE point across a paragraph with a device-chain, using the source above.",
                "Link two or more of the author's choices that together build this point, showing how each choice "
                "adds to it.",
                "Do not make a single observation and stop; the moves must connect into one point.")},

    # C1003-0009 - judge analyze vs summarize, predict, revise (paragraph). Taught WEATHER/WETLANDS -> held-out HOUR.
    "ACC-W910-L-G10-C1003-0009": {"source": "ACC-W910-ANALYSIS-LESSON-HOUR", "unit": "paragraph",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("A paragraph to judge:",
               "In the story, a woman named Mrs. Mallard is told that her husband has died in a railroad "
               "accident. She weeps, then goes to her room alone and sits facing an open window. Slowly she "
               "begins to feel a strange sense of freedom and whispers the word 'free' to herself. The author "
               "shows that she had mixed feelings about her marriage.")
        + _task("First JUDGE: does this paragraph analyze (choice, effect, warrant) or only summarize? Predict "
                "the score it would earn on a 2-point scale (2 = analysis with a choice, effect, and warrant; "
                "1 = summary) and say why.",
                "Then REVISE it into real analysis using the source above: name a specific choice the author "
                "makes, its effect on the reader, and why that effect matters to the story's purpose.")},

    # C1005-0010 - revise for purpose: add what is needed, cut what is not. Taught WETLANDS/HIGHWAYS -> held-out
    # RECYCLING. Fixed 2026-07-16 (COURSE_MASTERY17_TRIAGE C1005-0010): the old PP100 demanded WITHIN-sentence
    # clause surgery (cut a subordinate clause inside one compound sentence) - an operation the lesson never
    # modeled. Every practice slot revises a MULTI-SENTENCE draft: delete the one off-purpose sentence, add the
    # sentence the point needs. Reworded the PP100 to that same shape (unit stays multi-sentence draft revision).
    "ACC-W910-L-G10-C1005-0010": {"source": "ACC-W910-INFO-LESSON-RECYCLING", "unit": "sentence",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("A draft to revise (its point: how sorting produces clean streams):",
               "Workers and machines sort the material into clean streams. The facility opened years ago and now "
               "employs many people. Only clean, correctly sorted material can be pressed into bales and sold.")
        + _task("Revise this draft for its purpose using the source above.",
                "Delete the one sentence that does not serve the point (how sorting produces clean streams), and "
                "add a sentence that shows HOW the sorting actually separates the material into those clean "
                "streams.",
                "Write the revised draft.")},

    # C1005-0011 - order sentences so each builds on the last (sentence). Taught HIGHWAYS/RECYCLING -> held-out WEATHER.
    "ACC-W910-L-G10-C1005-0011": {"source": "ACC-W910-INFO-LESSON-WEATHER", "unit": "sentence",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Three sentences, out of order:",
               "(A) Computers then run those readings through models to project the days ahead. &nbsp;(B) A "
               "forecast is only as reliable as the data behind it. &nbsp;(C) So forecasters first gather "
               "readings from satellites, balloons, and ground stations.")
        + _task("These sentences are scrambled.",
                "Reorder them so each one builds on the sentence before it, using the source above to check the "
                "logic.",
                "Write them out in the corrected order.")},

    # C1005-0012 - pick the better draft and say why, then apply (sentence). Taught RECYCLING/WEATHER -> held-out WETLANDS.
    "ACC-W910-L-G10-C1005-0012": {"source": "ACC-W910-INFO-LESSON-WETLANDS", "unit": "sentence",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Two drafts of the same point about wetlands:",
               'Draft 1: "Wetlands are good for the environment in many ways." &nbsp;Draft 2: "Wetlands filter '
               'pollutants out of water before it reaches rivers, keeping downstream supplies cleaner."')
        + _task("These two drafts make the same point but differ on one move: one is vague, the other gives a "
                "specific, checkable reason.",
                "Pick the stronger draft and name the SPECIFIC reason it is better.",
                "Then apply that judgment: rewrite the weaker draft so it is as strong, using the source above. "
                "Write one sentence for your rewrite.")},

    # C1005-0013 - name the error TYPE and its fix (paragraph). Taught WEATHER/WETLANDS -> held-out ENERGYMIX.
    "ACC-W910-L-G10-C1005-0013": {"source": "ACC-W910-INFO-LESSON-ENERGYMIX", "unit": "paragraph",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("A draft with more than one problem:",
               "The country's electricity is getting cleaner because the sources it uses are becoming cleaner. "
               "This is important. Energy is a big topic in the news today. The mix has changed.")
        + _task("Diagnose this draft against the source above.",
                "For each problem, name the TYPE of error (too general, off-purpose, circular reason, out of "
                "order) and the fix that type calls for, not a vague it is weak.",
                "Then say, using the source, what the paragraph should do instead.")},

    # C1005-0014 - revise a whole draft for purpose: add, delete, reorder (paragraph). Taught WETLANDS/RECYCLING -> held-out HIGHWAYS.
    "ACC-W910-L-G10-C1005-0014": {"source": "ACC-W910-INFO-LESSON-HIGHWAYS", "unit": "paragraph",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("A draft to revise (its purpose: explain how the system was built and paid for):",
               "The Interstate Highway System is enormous. Congress passed a law in the 1950s. The system now "
               "stretches across the whole country. It was also a time when many families bought their first "
               "television. The money to build it came from a federal fuel tax.")
        + _task("Revise this paragraph for its purpose by combining the moves, using the source above.",
                "ADD what the point needs to be clear, DELETE what is off-purpose (the television aside), and "
                "REORDER the sentences so the explanation builds.",
                "Then run a quick self-check that the finished paragraph serves its purpose.")},

    # C1006-0015 - map the sources / build the evidence pool (multi_paragraph). Taught CONGESTION/DST -> held-out SCHOOLYEAR.
    "ACC-W910-L-G10-C1006-0015": {"source": "ACC-W910-ARG-OPP-LESSON-SCHOOLYEAR", "unit": "multi_paragraph",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your planning task:",
               "You are planning an essay on whether the school year should be lengthened, using the source set "
               "above.", "teal")
        + _task("Do NOT write the essay. MAP the sources first.",
                "The set has two sources: one making the case FOR a longer school year and one arguing against "
                "it. Go through BOTH. For each source, decide whether it is usable and write what it lets you "
                "say (the claim it can support, or the objection it raises against your position).",
                "Then name the one objection you will answer in your essay.",
                "The point is to survey the whole set, not to grab one source and ignore the rest.")},

    # C1006-0016 - synthesis claim the set jointly builds (multi_paragraph). Taught DST/SCHOOLYEAR -> held-out CONGESTION.
    "ACC-W910-L-G10-C1006-0016": {"source": "ACC-W910-ARG-OPP-LESSON-CONGESTION", "unit": "multi_paragraph",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your task:",
               "Using the source set on congestion pricing above, take your own position on whether cities "
               "should charge drivers to enter crowded zones.", "teal")
        + _task("Write ONE synthesis claim.",
                "It must be your own position that the SET of sources jointly supports, not a summary of any "
                "single source.",
                "Someone should be able to see it draws on the set as a whole. Write one sentence.")},

    # C1006-0017 - use two sources together (woven) for one point (sentence). Taught SCHOOLYEAR/CONGESTION ->
    # held-out DST. Fixed 2026-07-16 (COURSE_MASTERY17_TRIAGE C1006-0017): the taught move (per the lesson's
    # own SCHOOLYEAR model + CONGESTION transfer) weaves a fact from EACH side of an opposing pair so the two
    # RELATE in one claim ("the slide meets the cost"; "the toll money can be aimed at the drivers the other
    # source worries about") - NOT both sources cheering one side. The old PP100 assigned a one-sided pro-abolish
    # health point on an OPPOSING pair, so the con passage could not honestly feed it. Reworded the point to a
    # connect-both-sides claim that matches how the lesson modeled the weave on its own opposing sets.
    "ACC-W910-L-G10-C1006-0017": {"source": "ACC-W910-ARG-OPP-LESSON-DST", "unit": "sentence",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("The point you are building:",
               "Any decision about the clock has to weigh a real health cost against a real everyday benefit.", "teal")
        + _task("Write ONE sentence that uses BOTH sources in the set above TOGETHER to build this point: a fact "
                "from the source that argues for ending the switch meeting a fact from the source that argues "
                "against it.",
                "Weave them so the two facts RELATE in one claim (the way the lesson wove the learning slide with "
                "the cost), rather than giving each source its own separate chunk, and attribute each source.",
                "Write one sentence.")},

    # C1006-0018 - name where sources agree and where they clash (sentence). Taught CONGESTION/DST -> held-out SCHOOLYEAR.
    "ACC-W910-L-G10-C1006-0018": {"source": "ACC-W910-ARG-OPP-LESSON-SCHOOLYEAR", "unit": "sentence",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your task:",
               "The two sources in the set above both discuss the effects of a longer school year.", "teal")
        + _task("Write ONE sentence that states the RELATIONSHIP between the two sources.",
                "Name where they AGREE and where they CONFLICT, rather than reporting each source in turn.",
                "Write one sentence.")},

    # C1006-0019 - judge woven vs source-by-source, then revise (multi_paragraph). Taught WEATHER/RECYCLING -> held-out DST.
    "ACC-W910-L-G10-C1006-0019": {"source": "ACC-W910-ARG-OPP-LESSON-DST", "unit": "multi_paragraph",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("A multi-source paragraph to judge:",
               "Source 1 says the spring clock change is followed by a short rise in car crashes, because people "
               "are running on less sleep. Source 2 says that switching to earlier sunsets would send many "
               "workers home in the dark, and darkness is a known danger on the road.")
        + _task("First JUDGE: does this paragraph weave the sources into one point, or list them source-by-"
                "source? Predict whether it would score high or low for use of sources, and say why.",
                "Then REVISE it into a woven paragraph that builds ONE point from the sources in the set above, "
                "with the sources feeding that point together.")},

    # C1006-0020 (standalone cross-text planner) RETIRED 2026-07-18 (F3 orphan-planning fix): the "plan by
    # points, not by sources" teaching was folded into the cross-text essay lessons C1006-0021/0022 (which plan
    # AND write from the plan), so the standalone plan-only lesson + its plan-only mastery are removed.
    # See docs/superpowers/plans/2026-07-17-retire-orphan-planning-lessons.md.

    # C1006-0021 - CROSS-TEXT ANALYSIS essay (essay). The lesson teaches device-to-effect craft analysis WOVEN
    # ACROSS TWO texts (taught on HOUR + HIGHWAYS). Held-out mastery = ANALYSIS-PAIR-0001, a genuine analysis-mode
    # PAIR (Henry 1775 + Douglass 1852, two verbatim PD speeches sharing a rhetorical-question/parallelism craft),
    # so the cross-text task the lesson teaches is assessed on a genre-matched, un-taught source pair. Fixed
    # 2026-07-16: the old source was an ARGUMENT op-ed pair (SCHOOLYEAR) - a genre the lesson never modeled. A
    # first fix reframed this to single-text on the Challenger address, but the Tier-B Fable judge caught that it
    # conflicts with the lesson's cross-text body AND would duplicate L25 (single-text). So a proper analysis PAIR
    # was authored instead. (COURSE_MASTERY17_TRIAGE C1006-0021; A5 gate; Tier-B judge catch; Noel call.)
    "ACC-W910-L-G10-C1006-0021": {"source": "ACC-W910-ANALYSIS-PAIR-0001", "unit": "essay",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your task:",
               "Both speakers above use a cascade of rhetorical questions and parallel clauses to move an "
               "audience. Analyze how they use that craft.", "teal")
        + _task("Plan and write a full cross-text ANALYSIS essay on the two texts above.",
                "Make one analytical claim about the authors' craft, and support it with device-effect-warrant "
                "woven across BOTH texts (not one text and then the other).",
                "Frame it with an introduction and a conclusion, and self-check before you submit.")},

    # C1006-0022 - cross-text ARGUMENT essay (essay). Taught DST/SCHOOLYEAR -> held-out CONGESTION.
    "ACC-W910-L-G10-C1006-0022": {"source": "ACC-W910-ARG-OPP-LESSON-CONGESTION", "unit": "essay",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your task:",
               "Should cities charge drivers a fee to enter the busiest zones at peak hours? Take a side, using "
               "the source set above.", "teal")
        + _task("Plan and write a full cross-text ARGUMENT essay on the source set above.",
                "Defend one synthesis claim across the set, weaving sources into your points and answering the "
                "strongest counterclaim.",
                "Frame it with an introduction and a conclusion, and self-check before you submit.")},

    # C1006-0023 - revise a cross-text draft, then self-check (paragraph). Taught CONGESTION/SCHOOLYEAR -> held-out DST.
    "ACC-W910-L-G10-C1006-0023": {"source": "ACC-W910-ARG-OPP-LESSON-DST", "unit": "paragraph",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("A cross-text draft with synthesis gaps:",
               "Source 1 shows the spring switch costs sleep and is linked to a rise in crashes. Source 2 shows "
               "that longer evening light draws people outside and helps some businesses. Therefore the country "
               "should abolish daylight saving time and stay on permanent standard time. Some people say permanent "
               "standard time would bring dark winter evenings that hurt evening businesses.")
        + _task("Find the synthesis-specific gaps: this draft handles the sources one-by-one, and it names a "
                "counterclaim (dark winter evenings and evening businesses) but never answers it. Predict the "
                "score it would earn on the 2-point synthesis scale (2 = sources woven and counterclaim answered; "
                "1 = a gap remains).",
                "REVISE it into woven synthesis that also answers the counterclaim, using the set above.",
                "Then run a self-check on your revision before you submit.")},

    # C1006-0024 - G10 GATE: complete cross-text essay, verb sets mode (essay). Taught SCHOOLYEAR/CONGESTION -> held-out DST.
    "ACC-W910-L-G10-C1006-0024": {"source": "ACC-W910-ARG-OPP-LESSON-DST", "unit": "essay",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your gate prompt:",
               "Argue whether the country should stop changing clocks twice a year, using the source set above.",
               "teal")
        + _task("This is the course gate. Read the verb to set your mode (this prompt says argue, so take a "
                "side).",
                "Independently plan, draft, and self-check a complete cross-text essay from the set: a synthesis "
                "claim, sources woven point by point, the counterclaim answered, framed by an introduction and a "
                "conclusion.")},

    # C1003-0025 - single-text ANALYSIS essay (essay). Taught literary-fiction analysis on HOUR ("The Story of
    # an Hour") -> held-out single literary text SILK STOCKINGS ("A Pair of Silk Stockings", Chopin). Genre-matched
    # (literary-fiction craft analysis, as taught) and mirrors the real single-text analysis format (NY Regents
    # Part 3 / AP Lit prose-fiction analysis). Fixed 2026-07-16: was WETLANDS (explanatory nonfiction), a genre the
    # lesson never taught (COURSE_MASTERY17_TRIAGE C1003-0025; caught by mastery_genre_gate A5).
    "ACC-W910-L-G10-C1003-0025": {"source": "ACC-W910-ANALYSIS-SINGLE-0002", "unit": "essay",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your task:",
               "Analyze how the author of the passage above uses craft to develop Mrs. Sommers and the meaning of "
               "her afternoon.", "teal")
        + _task("Plan and write a complete single-text ANALYSIS essay on the source above.",
                "Open with an analytical thesis about the author's craft (not a retelling of the story), then "
                "write body paragraphs that each run device to effect to warrant.",
                "Frame it with an introduction and a conclusion, and self-check before you submit.")},

    # C1004-0026 - precision pass on an argument, position unchanged (paragraph). Taught WETLANDS/HIGHWAYS -> held-out CONGESTION.
    "ACC-W910-L-G10-C1004-0026": {"source": "ACC-W910-ARG-OPP-LESSON-CONGESTION", "unit": "paragraph",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("An argument draft to sharpen (do not change its position):",
               "Congestion pricing would totally fix traffic everywhere, and it is honestly a really good policy "
               "that a lot of people probably support, because it clearly makes cities better in every way.")
        + _task("Run a precision pass on this draft, using the source above, WITHOUT changing its position "
                "(it still favors congestion pricing).",
                "Replace a vague or overreaching claim word (totally fix, everywhere, in every way) with an exact "
                "one you can defend from the source, cut a hedge (probably) or an empty intensifier "
                "(honestly, really, clearly), and tighten the wording.",
                "The revised paragraph must keep the same side.")},
}
