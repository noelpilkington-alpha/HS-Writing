"""
mastery_prompts_g12.py  -  the AUTHORED, task-specific PP100 mastery prompt for every G12 AP-mastery lesson.

Decision (Noel 2026-07-14): the PP100 mastery task must (a) assess the exact skill the lesson taught, and
(b) be a FRESH held-out task, not a re-submit of the in-lesson write. A generic "apply the skill to the new
source" instruction fails both. So each G12 lesson gets a REAL AP task on a held-out source the lesson did NOT
use: a specific claim to situate, a real draft to revise, a source set to synthesize, a passage to analyze
rhetorically, or a full FRQ to run end to end under a self-imposed budget.

The held-out `source` id is a stimulus the lesson's OWN taught/transfer stimuli do not use, chosen of the
matching kind (argument lessons -> an argument source, rhetorical-analysis lessons -> an RA source, synthesis
lessons -> a synthesis set). AP argument prompts are source-free by design, so where a task also needs an
argument FRQ we state a self-contained prompt in the box; the inlined held-out source carries the
synthesis/analysis FRQ. rubric_ref = "rc.4trait" for every entry. `unit` keeps the graded grain. prompt_html is
rendered by gated_reading._render_body (same typography as the in-article writes). No em dashes.
"""

# ---- small inline-styled builders (copied verbatim from mastery_prompts_g9.py) ---------------------------
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

    # L01 - situate the question in the larger one (sentence). Taught/transfer: WATERTRADEOFF, WORKFORCEINVEST
    # (arg). Held-out arg source: SCHOOLLUNCH.
    "ACC-W910-L-G12-C1201-0001": {"source": "ACC-W910-ARG-LESSON-SCHOOLLUNCH", "unit": "sentence",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("The prompt to answer:",
               "Should schools be required to provide free lunch to every student, regardless of family income?",
               "teal")
        + _task("This prompt is one instance of a larger question. Do not treat it as a standalone puzzle.",
                "Write ONE claim that answers it while naming, in your own words, the broader question it "
                "belongs to, using a reason from the source above.",
                "Take a clear position. Write one sentence.")},

    # L02 - show a real tension, not a formulaic both-sides (sentence). Taught/transfer: WORKFORCEINVEST,
    # WATERTRADEOFF (arg). Held-out arg source: GRIDSPENDING.
    "ACC-W910-L-G12-C1201-0002": {"source": "ACC-W910-ARG-LESSON-GRIDSPENDING", "unit": "sentence",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("The prompt to answer:",
               "Should the country spend first on the electric grid, or first on new clean-power generation?",
               "teal")
        + _task("Write ONE claim that shows a REAL tension the source raises: name two things that are both true "
                "and genuinely pull against each other, and let that tension shape your position.",
                "This is not a formulaic 'on the other hand' that concedes nothing. Use the source above. Write "
                "one sentence.")},

    # L03 - hold the tension in a body paragraph (paragraph). Taught/transfer: WATERTRADEOFF, WORKFORCEINVEST
    # (arg). Held-out arg source: AIWORKFORCE.
    "ACC-W910-L-G12-C1201-0003": {"source": "ACC-W910-ARG-LESSON-AIWORKFORCE", "unit": "paragraph",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Your position:",
               "The government should actively help workers move into the fastest-growing technical fields.",
               "teal")
        + _task("Write ONE body paragraph that HOLDS the tension: keep two true and competing things from the "
                "source in view (for example, the pull of fast-growing fields and the cost or risk of steering "
                "people into them) and reason from their conflict.",
                "Do not flatten it by dismissing one side as weak. Use attributed evidence from the source above.")},

    # L04 - full argument that earns sophistication (essay). Taught/transfer: WORKFORCEINVEST, WATERTRADEOFF
    # (arg). Held-out arg source: GRIDSPENDING.
    "ACC-W910-L-G12-C1201-0004": {"source": "ACC-W910-ARG-LESSON-GRIDSPENDING", "unit": "essay",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Your argument task:",
               "Should the country fund the electric grid before new clean-power generation, or the reverse? "
               "Take a side.", "teal")
        + _task("Plan and write a complete AP argument essay using the source above.",
                "Earn the sophistication point (Row C): situate the question in the broader one it belongs to, and "
                "hold the tension without flattening it, so sophistication is carried across the whole essay.",
                "Include a defensible thesis, ordered body paragraphs with attributed evidence and reasoning, and "
                "a conclusion that lands the stakes.")},

    # L05 - analyze the rhetoric with sophistication (essay). Taught/transfer: ANALYSIS-LESSON-DOUGLASS,
    # RA-SINGLE-0001 (RA). Held-out RA source: RA-SINGLE-0002.
    "ACC-W910-L-G12-C1201-0005": {"source": "ACC-W910-RA-SINGLE-0002", "unit": "essay",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("The rhetorical situation:",
               "The passage above is from William Jennings Bryan's \"Cross of Gold\" speech, delivered July 9, "
               "1896, to the Democratic National Convention in Chicago. Speaking to a divided audience of party "
               "delegates, Bryan defends the free coinage of silver against the gold standard and seeks to win "
               "the convention to the cause of the common working American.",
               "teal")
        + _box("Your task:",
               "Read the passage above and analyze the rhetorical choices the writer makes to advance a purpose.",
               "teal")
        + _task("Write a full AP rhetorical-analysis essay on the passage above.",
                "Analyze the writer's choices AND earn sophistication: situate those choices in the whole "
                "rhetorical situation (audience, purpose, and moment) and hold the tension inside the argument "
                "rather than reducing it to a list of devices.",
                "Include a defensible thesis about the writer's choices, body paragraphs that trace each choice to "
                "its effect, and a conclusion.")},

    # L06 - full synthesis that earns sophistication (essay). Taught/transfer: SYNTH-LESSON-0001,
    # SYNTH-SET-0002 (synth). Held-out synth set: SYNTH-SET-0001.
    "ACC-W1112-L-G12-C1201-0006": {"source": "ACC-W910-SYNTH-SET-0001", "unit": "essay",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Your synthesis prompt:",
               "Read the source set above, then develop and defend your own position on the issue the sources "
               "debate.", "teal")
        + _task("Write a full AP synthesis essay using the set above.",
                "Weave a single argument that draws on at least three of the sources, and WEIGHT each source "
                "(lean on the strongest, qualify the weaker) instead of treating them as equal.",
                "Earn sophistication: situate the synthesized claim in a broader question and hold the tension "
                "across the whole essay.")},

    # L07 - predict whether you earned sophistication, then name the gap (essay). Taught/transfer:
    # WORKFORCEINVEST, WATERTRADEOFF (arg). Held-out arg source: SCHOOLLUNCH.
    "ACC-W910-L-G12-C1201-0007": {"source": "ACC-W910-ARG-LESSON-SCHOOLLUNCH", "unit": "essay",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Your argument task:",
               "Should schools provide free lunch to every student regardless of family income? Take a side.",
               "teal")
        + _task("Plan and write a complete AP argument essay using the source above.",
                "Before you submit, PREDICT whether your essay earns the sophistication point (Row C) and give one "
                "reason tied to the criterion: did you situate the question and hold a real tension, or not?",
                "Submit the essay and your prediction together. After it is scored, name the gap between your "
                "prediction and the grader.")},

    # L08 - sustain the whole essay, do not front-load it (essay). Taught/transfer: WATERTRADEOFF,
    # WORKFORCEINVEST (arg). Held-out arg source: AIWORKFORCE.
    "ACC-W910-L-G12-C1202-0008": {"source": "ACC-W910-ARG-LESSON-AIWORKFORCE", "unit": "essay",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Your argument task:",
               "Should the government actively steer workers toward growing fields, or leave that sorting to the "
               "market? Take a side.", "teal")
        + _task("Write a complete AP argument essay under a self-imposed time budget, using the source above. "
                "There is no platform timer, so keep a clock or phone timer in view and watch it as you finish "
                "each paragraph.",
                "The goal is to SUSTAIN quality end to end: use a recycling time-budget and a fast plan so the "
                "conclusion is as strong as the intro.",
                "Do not front-load the opening and let the essay fade.")},

    # L09 - rehearse a complete argument, end to end (essay). Taught/transfer: WORKFORCEINVEST, WATERTRADEOFF
    # (arg). Held-out arg source: GRIDSPENDING.
    "ACC-W910-L-G12-C1202-0009": {"source": "ACC-W910-ARG-LESSON-GRIDSPENDING", "unit": "essay",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Your argument task:",
               "Should the country fund the electric grid before new clean-power generation? Take a side.",
               "teal")
        + _task("Rehearse a full AP argument essay under a self-imposed budget, using the source above.",
                "Sustain quality from a situated, defensible claim through a defended conclusion, rehearsing the "
                "WHOLE arc, not just the opening moves.")},

    # L10 - rehearse a complete rhetorical analysis, end to end (essay). Taught/transfer: RA-SINGLE-0001,
    # RA-SINGLE-0002 (RA). Held-out RA source: RA-SINGLE-0003.
    "ACC-W910-L-G12-C1202-0010": {"source": "ACC-W910-RA-SINGLE-0003", "unit": "essay",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("The rhetorical situation:",
               "The passage above is from Ralph Waldo Emerson's essay \"Self-Reliance,\" published in Essays: "
               "First Series (1841). Writing for the general reading public of his day, Emerson urges each "
               "reader to trust an inner voice and resist the pressure to conform to society. Here the audience "
               "reads the essay rather than hears it, and the occasion is its publication, not a speech.",
               "teal")
        + _box("Your task:",
               "Analyze the rhetorical choices the writer of the passage above makes to achieve a purpose.",
               "teal")
        + _task("Rehearse a full rhetorical-analysis essay under a self-imposed budget, using the passage "
                "above.",
                "Cap your annotation time and pace the writing so a situated, choice-to-effect analysis is "
                "finished end to end, not abandoned mid-essay.")},

    # L11 - rehearse a complete synthesis, end to end (essay). Taught/transfer: SYNTH-SET-0002, SYNTH-SET-0001
    # (synth). Held-out synth set: SYNTH-LESSON-0001 (the G11-12 synth set).
    "ACC-W910-L-G12-C1202-0011": {"source": "ACC-W1112-SYNTH-LESSON-0001", "unit": "essay",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Your synthesis prompt:",
               "Read the source set above, then develop and defend your own position on the issue the sources "
               "debate.", "teal")
        + _task("Rehearse a full AP synthesis essay under a self-imposed budget, using the set above.",
                "Cap your reading time and pace the writing so a woven, weighted, sophisticated synthesis is "
                "finished end to end.")},

    # L12 - name the FRQ type before you write (paragraph). Taught/transfer: SYNTH-SET-0001, RA-SINGLE-0002.
    # Held-out synth set: SYNTH-SET-0002. This is a genre-AGNOSTIC recognition lesson (type 5): the skill is
    # NAMING the FRQ type, so a synthesis source is fair game (mastery_genre_gate exempts type 5 from the analysis
    # boundary). Fixed 2026-07-16 per COURSE_MASTERY17_TRIAGE C1202-0012: the real defect was the PROMPT, not the
    # source - (a) it was type-ambiguous (read as both synthesis and argument) and never told the student to USE
    # the sources, and (b) it demanded "rubric rows" the lesson never taught. Fix: state the synthesis tell
    # unambiguously (use the source set + cite), and drop the rubric-rows deliverable (name the type + tell +
    # move-set + plan is what the lesson teaches).
    "ACC-W910-L-G12-C1202-0012": {"source": "ACC-W910-SYNTH-SET-0002", "unit": "paragraph",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("The FRQ to diagnose (you will PLAN it, not write the full essay):",
               "Read the source set above and develop your position on the issue the sources debate, using and "
               "citing at least three of the sources to support it.", "teal")
        + _task("Your deliverable is a short naming-and-planning paragraph, not the finished essay. Do not "
                "default to a memorized opening.",
                "First NAME whether this is a synthesis, rhetorical-analysis, or argument FRQ, and give the tell "
                "in the prompt that proves it.",
                "Then name the move-set it rewards and sketch the plan you would run for it.")},

    # L13 - switch move-sets between two different FRQs (essay). Taught/transfer: WATERTRADEOFF, SYNTH-SET-0003
    # (arg + synth). Held-out synth set (for the synthesis half): SYNTH-SET-0001; the argument half is
    # source-free by AP design.
    "ACC-W910-L-G12-C1202-0013": {"source": "ACC-W910-SYNTH-SET-0001", "unit": "essay",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Two FRQs, back to back:",
               "FRQ 1 (argument, no source): Some hold that progress depends on questioning ideas most people "
               "accept. Take a position on the value of challenging widely held beliefs. &nbsp; FRQ 2 (synthesis): "
               "Using the source set above, develop and defend your own position on the issue the sources debate.",
               "teal")
        + _task("Rehearse these two different FRQ types back to back under a self-imposed budget.",
                "Before each, re-name the type and SWITCH the move-set: run the argument first (a defensible "
                "thesis and reasoning from your own knowledge, no sources), then the synthesis (weave and weight "
                "the sources above).",
                "Do not carry the argument move-set into the synthesis.")},

    # L14 - predict your full-write scores, then name the pacing gap (essay). Taught/transfer: WATERTRADEOFF,
    # WORKFORCEINVEST (arg). Held-out arg source: SCHOOLLUNCH.
    "ACC-W910-L-G12-C1202-0014": {"source": "ACC-W910-ARG-LESSON-SCHOOLLUNCH", "unit": "essay",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Your argument task:",
               "Should schools provide free lunch to every student regardless of family income? Take a side.",
               "teal")
        + _task("Write a complete AP argument essay under a self-imposed budget, using the source above.",
                "Predict your own rubric scores across the rows (Evidence and Sophistication) with reasons drawn "
                "from the WHOLE essay, not just the intro. Submit the essay and the prediction together.",
                "After it is scored, name the gap between your prediction and the grader and whether pacing "
                "caused it; if your prediction matched and pacing held, say so and name the row you were most "
                "at risk of missing.")},

    # L15 - shape voice with a syntactic choice (sentence). Taught/transfer: WORKFORCEINVEST, WATERTRADEOFF
    # (arg). Held-out arg source: GRIDSPENDING. Provided flat draft to revise.
    "ACC-W910-L-G12-D1201-0015": {"source": "ACC-W910-ARG-LESSON-GRIDSPENDING", "unit": "sentence",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("A flat compound sentence to revise:",
               "The grid is aging, and new wind and solar are being built quickly, and the power often cannot "
               "reach the cities that need it.")
        + _task("This is a flat string of equal clauses joined by and. Revise it into ONE sentence that carries "
                "voice and emphasis through a deliberate syntactic move.",
                "Subordinate the minor idea and place your main point at the emphatic end. Keep the facts the "
                "same. Write one sentence.")},

    # L16 - G12 GATE: write a full FRQ section, type by type (essay). Taught/transfer: SYNTH-SET-0001,
    # RA-SINGLE-0002. Held-out synth set (inlined, carries the synthesis + rhetorical-analysis halves):
    # SYNTH-SET-0002; the argument half is source-free by AP design.
    "ACC-W910-L-G12-C1202-0016": {"source": "ACC-W910-SYNTH-SET-0002", "unit": "essay",
        "rubric_ref": "rc.4trait", "prompt_html": _INTRO
        + _box("Your gate: three cold FRQs.",
               "FRQ 1 (synthesis): Using the source set above, develop and defend your own position on the issue "
               "the sources debate. &nbsp; FRQ 2 (rhetorical analysis): Choose ONE passage from the set above and "
               "analyze the rhetorical choices its writer makes to achieve a purpose. &nbsp; FRQ 3 (argument, no "
               "source): Take a position on whether individuals have an obligation to question the conventions of "
               "their society.", "teal")
        + _task("This is the course gate. For each FRQ, independently NAME the type (synthesis, rhetorical "
                "analysis, argument), run its move-set, and sustain quality end to end under a self-imposed "
                "budget.",
                "Switch the move-set between FRQs, and earn sophistication wherever the rubric offers it.")},
}
