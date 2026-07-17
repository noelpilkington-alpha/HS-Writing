"""
mastery_prompts_g9.py  -  the AUTHORED, task-specific PP100 mastery prompt for every G9 v3.1 lesson.

Decision (Noel 2026-07-14): the PP100 mastery task must (a) assess the exact skill the lesson taught, and
(b) be a FRESH held-out task, not a re-submit of the in-lesson write. A generic "apply the skill to the new
source" instruction failed both: the readiness audit flagged it as not-doable (no vague claim to sharpen, no
stated task to answer) and as skill-mismatched. So each lesson gets a REAL task on its held-out topic: a
specific claim to take a side on, a real vague claim to sharpen, a stated explain task, a provided weak draft
to diagnose and revise, etc. All content is own-words and traces to the held-out source's own facts.

Single source of truth: g9_push_mastery_v3_1.mastery_targets() reads L.mastery if the lesson file sets it,
else falls back to MASTERY[L.id] here. The held-out `source` id must match g9_push_mastery_v3_1.HELDOUT so the
pusher inlines the same source above this prompt. `unit`/`rubric_ref` keep the graded shape. prompt_html is
rendered by gated_reading._render_body (same typography as the in-article writes). No em dashes.
"""

# ---- small inline-styled builders (match the v3.1 lesson vocabulary) -------------------------------------
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

    # L01 - take an arguable side (sentence). Held-out: SOCIALMEDIAAGE.
    "ACC-W910-L-G9-C901-0001": {"source": "ACC-W910-FRAME-SOCIALMEDIAAGE", "unit": "sentence",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("The question to take a side on:",
               "Should social media apps be required to check how old their users are?", "teal")
        + _task("Write ONE arguable claim that answers this question.",
                "Take a clear side (yes or no) and give a reason drawn from the source above.",
                "It counts as arguable only if someone could reasonably disagree with it. Write one sentence.")},

    # L03 - sharpen a vague claim + so-what (sentence). Held-out: SOCIALMEDIAAGE.
    "ACC-W910-L-G9-C901-0003": {"source": "ACC-W910-FRAME-SOCIALMEDIAAGE", "unit": "sentence",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("A vague claim to sharpen:", '"Age checks on social media are a good idea."')
        + _task("This claim takes a side but is vague, and it never says why it matters.",
                "Rewrite it into ONE sharper claim that does two things: (1) make the position specific (which "
                "apps, or what the check should actually do), and (2) reach the so-what: name what is at stake "
                "if it happens or does not.",
                "Use a reason from the source above. Write one sentence.")},

    # L04 - controlling idea for an explain task (sentence). Held-out: RECYCLING.
    "ACC-W910-L-G9-C905-0004": {"source": "ACC-W910-INFO-LESSON-RECYCLING", "unit": "sentence",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your explain task:",
               "Explain how a recycled bottle becomes new material after it leaves the blue bin.", "teal")
        + _task("This is an EXPLAIN task, not an argument. Do not take a side.",
                "Write ONE controlling idea: a single sentence that sets the focus and previews the parts your "
                "explanation would cover, using the source above. Write one sentence.")},

    # (L05 removed 2026-07-14: merged into L04/C905-0004 per the design audit; its mastery entry is retired.)

    # L06 - argue or explain? decide from the verb (sentence). Held-out: SCHOOLYEAR.
    "ACC-W910-L-G9-C901-0006": {"source": "ACC-W910-FRAME-SCHOOLYEAR", "unit": "sentence",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your task (follow THIS, not the source's own suggestion):",
               "Explain why supporters and critics disagree about lengthening the school year.", "teal")
        + _task("The source above is written as a debate and even invites you to pick a side, but your task "
                "is what counts, so read your task's verb and let it decide.",
                "First, name whether your task wants an ARGUMENT claim (take a side) or a CONTROLLING IDEA "
                "(set a focus, no side). Decide it from the verb yourself.",
                "Then write the ONE right product for that verb, using facts from the source. Write one sentence.")},

    # L07 - name your source: quote/paraphrase/summarize + attribution (sentence). Held-out: AIWORKFORCE.
    "ACC-W910-L-G9-C902-0007": {"source": "ACC-W910-ARG-LESSON-AIWORKFORCE", "unit": "sentence",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("The claim you are supporting:",
               "The government should steer workers toward the fields that are growing fastest.", "teal")
        + _task("Bring ONE piece of evidence from the source above into a sentence that supports this claim.",
                "Choose whether to quote, paraphrase, or summarize, and always name who the evidence comes from "
                "(for example, the Bureau of Labor Statistics) so a reader can trust it.",
                "No fact may stand alone without its source. Write one sentence.")},

    # L08 - pick the evidence that proves THIS claim (sentence). Held-out: GRIDSPENDING.
    "ACC-W910-L-G9-C902-0008": {"source": "ACC-W910-ARG-LESSON-GRIDSPENDING", "unit": "sentence",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("The claim you must prove:",
               "Renewable sources already supply a substantial share of U.S. electricity.", "teal")
        + _task("The source has several true facts, and only some prove THIS exact claim. Choose the ONE piece "
                "of evidence that actually proves it (a fact about the renewable share), not just any true fact "
                "about energy.",
                "Put it in one sentence and name its source. Write one sentence.")},

    # L09 - integrate a quote (sentence). Held-out: AIWORKFORCE.
    "ACC-W910-L-G9-C902-0009": {"source": "ACC-W910-ARG-LESSON-AIWORKFORCE", "unit": "sentence",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("The claim you are supporting:",
               "Fast growth in technical jobs is a real reason to help workers train for them.", "teal")
        + _task("Find a short phrase in the source above worth quoting. Do NOT drop it in on its own.",
                "Fold it into a sentence YOU build: add an introduction and an attribution (name who said it) so "
                "the quoted words connect to your claim. Write one sentence.")},

    # L10 - because / but / so reasoning hinge (sentence). Held-out: GRIDSPENDING.
    "ACC-W910-L-G9-C903-0010": {"source": "ACC-W910-ARG-LESSON-GRIDSPENDING", "unit": "sentence",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your claim and evidence:",
               "Claim: The grid should be funded first. &nbsp;Evidence: New wind and solar cannot deliver power "
               "if the wires and storage to carry it are not built.", "teal")
        + _task("Write ONE sentence that ties this evidence to this claim with a reasoning hinge.",
                "Use because (state the reason), but (state a limit or contrast), or so (state the consequence) "
                "to make the link explicit. Write one sentence.")},

    # L11 - warrant (sentence). Held-out: AIWORKFORCE.
    "ACC-W910-L-G9-C903-0011": {"source": "ACC-W910-ARG-LESSON-AIWORKFORCE", "unit": "sentence",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your claim and evidence:",
               "Claim: Government should help workers move into growing fields. &nbsp;Evidence: The Bureau of "
               "Labor Statistics projects data-science jobs will grow about 33.5 percent from 2024 to 2034, far "
               "faster than the 3.1 percent average.", "teal")
        + _task("Write the WARRANT: one sentence that states WHY this evidence supports this claim.",
                "Use a because, since, or as clause plus a short why-explanation. Do not just restate the claim. "
                "Write one sentence.")},

    # L12 - build a Point-Evidence-Warrant paragraph (paragraph). Held-out: RECYCLING.
    "ACC-W910-L-G9-C903-0012": {"source": "ACC-W910-INFO-LESSON-RECYCLING", "unit": "paragraph",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your point to develop:",
               "One wrong item in the bin can undo a whole batch of recycling.", "teal")
        + _task("Write ONE complete paragraph that develops this point using the source above.",
                "Include all three moves: state the point, fold in evidence and name its source, then add a "
                "warrant that explains why the evidence supports the point.")},

    # L13 - check the reasoning, then revise a provided draft (sentence). Held-out: ENERGYMIX.
    "ACC-W910-L-G9-C903-0013": {"source": "ACC-W910-INFO-LESSON-ENERGYMIX", "unit": "sentence",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("A draft whose warrant is weak:",
               "Claim: The U.S. is shifting toward cleaner electricity. &nbsp;Evidence: The EIA reports "
               "renewables supplied about 21 percent of U.S. electricity in 2023, while coal kept falling. "
               "&nbsp;Warrant: This shows the U.S. is shifting toward cleaner electricity.")
        + _task("The warrant just restates the claim. It never explains WHY the evidence supports it.",
                "Rewrite the warrant sentence so it truly explains why renewables rising while coal keeps "
                "falling signals a real shift toward cleaner electricity. Write one sentence.")},

    # L14 - pick the transition the logic needs (paragraph). Held-out: HIGHWAYS.
    "ACC-W910-L-G9-C906-0014": {"source": "ACC-W910-INFO-LESSON-HIGHWAYS", "unit": "paragraph",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("A paragraph with filler transitions:",
               "After World War II, more Americans owned cars than ever before. Also, the nation's roads were a "
               "patchwork of narrow, crowded routes. Also, Congress passed the Federal-Aid Highway Act in 1956. "
               "Then the country built a network that now runs about 46,876 miles.")
        + _task("The words also and then hide the real relationships between these ideas.",
                "Rewrite the paragraph, replacing each filler transition with one that names the true "
                "relationship (add, contrast, cause, or sequence). Keep the facts the same.")},

    # L15 - fix a vague back-reference (sentence). Held-out: RECYCLING.
    "ACC-W910-L-G9-C906-0015": {"source": "ACC-W910-INFO-LESSON-RECYCLING", "unit": "sentence",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("A sentence with a vague reference:",
               "At the recovery facility, machines and workers sort the material into clean streams. This is why "
               "one wrong item can ruin the batch.")
        + _task("The second sentence starts with a naked This, and it is not clear what This points to.",
                "Rewrite the second sentence so the reference is anchored: name exactly what This is, using the "
                "source above. Write one sentence.")},

    # L16 - revise a choppy paragraph for cohesion (paragraph). Held-out: GRIDSPENDING.
    "ACC-W910-L-G9-C906-0016": {"source": "ACC-W910-ARG-LESSON-GRIDSPENDING", "unit": "paragraph",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("A choppy paragraph to revise:",
               "Renewables now supply about a fifth of U.S. electricity. Also, that share keeps rising. Also, new "
               "wind and solar need wires to carry the power. This is a problem. Then the grid becomes the real "
               "bottleneck.")
        + _task("Revise this paragraph for cohesion.",
                "Replace each filler transition (also, then) with one that names the real relationship, and "
                "anchor the vague This so the reader knows what it points to. Keep the facts the same.")},

    # L17 - build a complete body paragraph: claim, evidence, warrant (paragraph). Held-out: AIWORKFORCE.
    "ACC-W910-L-G9-C906-0017": {"source": "ACC-W910-ARG-LESSON-AIWORKFORCE", "unit": "paragraph",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your claim:",
               "The government should actively help workers train for fast-growing technical fields.", "teal")
        + _task("Write ONE complete body paragraph that supports this claim using the source above.",
                "It must have all three parts, joined so they connect: the claim, attributed evidence from the "
                "source, and a warrant that explains why the evidence supports the claim.")},

    # L18 - write a fresh paragraph, then self-check (paragraph). Held-out: GRIDSPENDING.
    "ACC-W910-L-G9-C906-0018": {"source": "ACC-W910-ARG-LESSON-GRIDSPENDING", "unit": "paragraph",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your task:",
               "Take a position on which should be funded first: new clean-power generation, or the grid that "
               "moves the power.", "teal")
        + _task("Write ONE complete body paragraph from scratch that argues your position, using the source "
                "above: a claim, attributed evidence, and a warrant.",
                "Then run the yes/no self-check on your own paragraph before you submit: Does it state a clear "
                "claim? Is the evidence attributed? Does the warrant explain why? Fix any No.")},

    # L19 - single-paragraph outline (plan). Held-out: HIGHWAYS.
    "ACC-W910-L-G9-C904-0019": {"source": "ACC-W910-INFO-LESSON-HIGHWAYS", "unit": "multi_paragraph",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your essay task:",
               "Explain how the Interstate Highway System began, how big it grew, and how the country paid for "
               "it.", "teal")
        + _task("Do NOT write the essay. Write the PLAN as a multiple-paragraph outline (the MPO this lesson "
                "taught).",
                "Give a governing thesis for the whole essay, an introduction line, then ordered body rows that "
                "each pair a main idea with its details and the specific evidence from the source, and a "
                "conclusion line that restates the thesis. Do not write a single-paragraph plan.")},

    # L20 - order the body paragraphs so the essay builds (plan). Held-out: RECYCLING.
    "ACC-W910-L-G9-C904-0020": {"source": "ACC-W910-INFO-LESSON-RECYCLING", "unit": "multi_paragraph",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Three body points, out of order:",
               "(A) One wrong item can contaminate a whole batch. &nbsp;(B) Trucks carry mixed bins to a "
               "materials recovery facility. &nbsp;(C) Inside, machines and workers sort the material into clean "
               "streams.", "teal")
        + _task("These body points are out of order for an essay explaining how recycling works.",
                "Put them in an order where each paragraph builds on the one before, and write the opening "
                "transition sentence for the second and third paragraphs so each links to the point before it.")},

    # L21 - intro + conclusion (plan). Held-out: ENERGYMIX.
    "ACC-W910-L-G9-C904-0021": {"source": "ACC-W910-INFO-LESSON-ENERGYMIX", "unit": "multi_paragraph",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your thesis (already written):",
               "The mix of sources that powers the U.S. is shifting, with fossil fuels slowly giving ground to "
               "renewables and steady nuclear power.", "teal")
        + _task("Write TWO paragraphs for an essay built on this thesis, using the source above.",
                "First, an introduction that orients the reader and states the thesis.",
                "Second, a conclusion that lands the upshot (why the shift matters), not one that just repeats "
                "the thesis.")},

    # L22 - argue or explain? choose the essay mode (plan). Held-out: SCHOOLYEAR.
    "ACC-W910-L-G9-C901-0022": {"source": "ACC-W910-FRAME-SCHOOLYEAR", "unit": "multi_paragraph",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your essay task (follow THIS, not the source's own suggestion):",
               "Explain why supporters and critics disagree about lengthening the school year.", "teal")
        + _task("The source above is written as a debate and even invites you to pick a side, but your task "
                "is what counts, so read your task's verb and let it decide.",
                "First name whether this whole essay should ARGUE (a thesis that takes a side) or EXPLAIN (a "
                "controlling idea, no side). Decide it from the verb yourself.",
                "Then write the matching thesis sentence for that mode, using the source above.")},

    # L23 - full argument essay (essay). Held-out: AIWORKFORCE.
    "ACC-W910-L-G9-C904-0023": {"source": "ACC-W910-ARG-LESSON-AIWORKFORCE", "unit": "essay",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your argument task:",
               "Should the government actively steer workers toward the fields that are growing, or leave that "
               "sorting to the market? Take a side.", "teal")
        + _task("Plan and write a complete single-source argument essay using the source above.",
                "Include: an intro that frames your thesis; ordered body paragraphs, each with a claim, "
                "attributed evidence, and a warrant, linked with real transitions; and a conclusion that lands "
                "the upshot. Run your self-check before you submit.")},

    # L24 - full informational essay (essay). Held-out: HIGHWAYS.
    "ACC-W910-L-G9-C904-0024": {"source": "ACC-W910-INFO-LESSON-HIGHWAYS", "unit": "essay",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your explain task:",
               "Explain how the Interstate Highway System began, how it grew, and how the country paid for it.",
               "teal")
        + _task("Plan and write a complete single-source informational essay using the source above.",
                "Include: an intro that frames a controlling-idea thesis (no side); ordered body paragraphs that "
                "explain each part with attributed evidence, linked with real transitions; and a conclusion that "
                "lands the upshot. Run your self-check before you submit.")},

    # L25 - revise against the rubric, then self-check (paragraph). Held-out: GRIDSPENDING.
    "ACC-W910-L-G9-C904-0025": {"source": "ACC-W910-ARG-LESSON-GRIDSPENDING", "unit": "paragraph",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("An essay body paragraph with a gap:",
               "The grid should be funded before new generation. The U.S. Energy Information Administration "
               "reports that renewables already supply about 21 percent of U.S. electricity, and that share is "
               "rising. That is a lot of clean power.")
        + _task("Find the specific gap: this paragraph gives a claim and evidence but no warrant, and its last "
                "sentence never explains why the evidence supports funding the grid first.",
                "Revise the paragraph against the rubric so it includes a warrant that explains the link.",
                "Then run the self-check on your revision before you submit.")},

    # L26 - GATE: complete single-source essay, verb sets the mode (essay). Held-out: ENERGYMIX.
    "ACC-W910-L-G9-C904-0026": {"source": "ACC-W910-INFO-LESSON-ENERGYMIX", "unit": "essay",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your gate task:",
               "Explain how and why the mix of sources for U.S. electricity has been shifting.", "teal")
        + _task("This is the course gate. Read the verb to set your mode (this task asks you to EXPLAIN, so use "
                "a controlling idea, no side).",
                "Independently plan, draft, and self-check a complete single-source essay using the source "
                "above: intro that frames the focus, ordered body paragraphs with attributed evidence and real "
                "transitions, and a conclusion that lands the upshot.")},

    # L16/tone - formal, objective tone (sentence). Held-out: PAYGRADES (a topic not used in the lesson).
    "ACC-W910-L-G9-C906-0027": {"source": "ACC-W910-FRAME-PAYGRADES", "unit": "sentence",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("An informal sentence to fix:",
               '"Honestly, I think paying kids for good grades is a totally awesome idea, because it gives them a '
               'real reason to show up and try."')
        + _task("Rewrite this sentence in a formal, objective tone, keeping its position AND its reason.",
                "Cut the first person (I think), the hedge (Honestly), and the slang (totally awesome, kids), and "
                "state the point about the issue. Keep the reason (it gives students a reason to try). Do not "
                "change what it claims. Write one sentence.")},

    # L11/two-evidence - develop a point with two facts that add up (paragraph). Held-out: GRIDSPENDING.
    "ACC-W910-L-G9-C903-0028": {"source": "ACC-W910-INFO-LESSON-ENERGYMIX", "unit": "paragraph",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your point to develop:",
               "Fossil fuels still supply most U.S. electricity, but low-carbon sources now cover a real share of it.", "teal")
        + _task("Develop this point with TWO facts from the source above that ADD UP (not two that repeat the "
                "same idea), for example the fossil-fuel share and the combined renewable-plus-nuclear share.",
                "Write ONE paragraph: state the point, bring in the two attributed figures in an order where the "
                "second builds on the first, and add one warrant that ties BOTH facts to the point.")},

    # L27/argument gate - cold full argument essay (essay). Held-out: AIWORKFORCE (cold vs the lesson's sources).
    "ACC-W910-L-G9-C904-0029": {"source": "ACC-W910-ARG-LESSON-AIWORKFORCE", "unit": "essay",
        "rubric_ref": "rc.staar", "prompt_html": _INTRO
        + _box("Your argument gate task:",
               "Should the government actively steer workers toward the growing fields, or leave that sorting to "
               "the market? Take a side.", "teal")
        + _task("This is the argument gate. Independently plan, draft, and self-check a complete single-source "
                "ARGUMENT essay using the source above.",
                "Include: an intro that frames a thesis taking a clear side; ordered body paragraphs, each with a "
                "claim backed by attributed evidence and a warrant explaining why that evidence proves the claim; "
                "and a conclusion that lands the upshot. Run your self-check before you submit.")},
}
