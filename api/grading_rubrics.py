"""
Per-lesson, per-task grading rubrics for all courses (A1, A2, B1L, B2).

Each rubric defines:
- task_type: what kind of writing task
- criteria: list of specific, observable criteria to evaluate
- common_pitfalls: mistakes to watch for (used in grading prompt)
- min_words: minimum word count for the task
- max_score: maximum score for the task (number of criteria)
"""

from course_rubrics import A2_RUBRICS, B1L_RUBRICS, B2_RUBRICS

RUBRICS = {

    # ===================== L01: From Expository to Argumentative =====================
    "L01_independent_expository": {
        "task_type": "expository_paragraph",
        "lesson": "L01",
        "description": "Write an expository paragraph about a chosen topic (space exploration, privacy/security, or public libraries)",
        "criteria": [
            {
                "id": "topic_sentence_fact",
                "name": "Topic sentence states a fact",
                "description": "The topic sentence states a factual observation that no reasonable person would disagree with. It does NOT take a position or use 'should'.",
                "weight": 2,
            },
            {
                "id": "supporting_info",
                "name": "Supporting sentences provide information",
                "description": "At least 2 supporting sentences give facts, details, examples, or explanations — not opinions or arguments.",
                "weight": 1,
            },
            {
                "id": "concluding_sentence",
                "name": "Has a concluding sentence",
                "description": "The paragraph ends with a sentence that wraps up or summarizes without introducing a new idea or taking a position.",
                "weight": 1,
            },
            {
                "id": "neutral_tone",
                "name": "Maintains neutral, objective tone",
                "description": "The paragraph explains or informs without trying to persuade. No persuasive language ('should', 'must', 'need to').",
                "weight": 1,
            },
        ],
        "common_pitfalls": [
            "Accidentally writing an argumentative paragraph instead of expository (topic sentence makes a claim)",
            "Topic sentence that is technically factual but so obvious it provides no information",
            "Supporting sentences that drift into opinion without the student realizing",
            "No concluding sentence — paragraph just stops after the last supporting detail",
        ],
        "min_words": 50,
    },

    "L01_independent_argumentative": {
        "task_type": "argumentative_paragraph",
        "lesson": "L01",
        "description": "Write an argumentative paragraph about the same topic chosen for the expository paragraph",
        "criteria": [
            {
                "id": "topic_sentence_claim",
                "name": "Topic sentence makes a debatable claim",
                "description": "The topic sentence makes a claim someone could reasonably disagree with. It takes a clear position, often using 'should' or similar language.",
                "weight": 2,
            },
            {
                "id": "supporting_reasons",
                "name": "Supporting sentences provide reasons and evidence",
                "description": "At least 2 supporting sentences give reasons or evidence that support the claim — not just information or description.",
                "weight": 1,
            },
            {
                "id": "concluding_sentence",
                "name": "Has a concluding sentence",
                "description": "The paragraph ends with a sentence that reinforces the position or calls for action.",
                "weight": 1,
            },
            {
                "id": "persuasive_tone",
                "name": "Maintains committed, persuasive tone",
                "description": "The paragraph clearly tries to convince the reader. The writer is taking a side, not just presenting information.",
                "weight": 1,
            },
        ],
        "common_pitfalls": [
            "Topic sentence that states a fact rather than a claim ('Most cities have surveillance cameras' instead of 'Cities should limit surveillance cameras')",
            "Supporting sentences that describe the topic instead of arguing for the position",
            "Weak claim that no one would disagree with ('Privacy is important')",
            "No concluding sentence or a concluding sentence that contradicts the position",
        ],
        "min_words": 50,
    },

    # ===================== L02: Taking a Position =====================
    "L02_independent_position": {
        "task_type": "position_statement",
        "lesson": "L02",
        "description": "Narrow a broad topic to a specific, debatable, supportable position statement",
        "criteria": [
            {
                "id": "debatable",
                "name": "Position is debatable",
                "description": "A reasonable person could disagree with this position. It is not a fact, truism, or statement everyone would accept.",
                "weight": 2,
            },
            {
                "id": "specific",
                "name": "Position is specific",
                "description": "Names WHO should act, WHAT they should do, and HOW or WHEN. Not vague or overly broad.",
                "weight": 2,
            },
            {
                "id": "supportable",
                "name": "Position is supportable",
                "description": "The student could realistically provide at least 2 reasons with evidence from their own knowledge. Not too extreme or absolute to defend.",
                "weight": 1,
            },
        ],
        "common_pitfalls": [
            "Position is a fact disguised as a claim ('College athletes work hard')",
            "Position is too vague ('Something should be done about energy')",
            "Position is too extreme to defend ('All fossil fuels should be banned immediately')",
            "Position uses 'should' but doesn't specify who, what, or how",
        ],
        "min_words": 15,
    },

    "L02_independent_paragraph": {
        "task_type": "argumentative_paragraph",
        "lesson": "L02",
        "description": "Write a complete argumentative paragraph supporting one of the position statements",
        "criteria": [
            {
                "id": "topic_sentence_position",
                "name": "Topic sentence is the position statement",
                "description": "The paragraph opens with the student's specific, debatable position from the narrowing exercise.",
                "weight": 1,
            },
            {
                "id": "supporting_reasons",
                "name": "At least 2 supporting sentences with reasons",
                "description": "Contains at least 2 sentences that give reasons or evidence supporting the claim.",
                "weight": 2,
            },
            {
                "id": "concluding_sentence",
                "name": "Has a concluding sentence",
                "description": "Ends with a sentence that reinforces the position.",
                "weight": 1,
            },
            {
                "id": "structure_complete",
                "name": "Paragraph has 4-6 sentences",
                "description": "Complete paragraph with topic sentence, support, and conclusion — not too short or rambling.",
                "weight": 1,
            },
        ],
        "common_pitfalls": [
            "Opening with a fact instead of the position statement",
            "Only 1 supporting sentence (needs at least 2)",
            "Supporting sentences that restate the claim instead of adding new reasons",
            "No concluding sentence — paragraph just stops",
        ],
        "min_words": 50,
    },

    # ===================== L03: Evidence and Reasoning =====================
    "L03_practice_evidence": {
        "task_type": "evidence_and_reasoning",
        "lesson": "L03",
        "description": "Generate 3 pieces of evidence with reasoning for a given claim",
        "criteria": [
            {
                "id": "evidence_present",
                "name": "Contains identifiable evidence",
                "description": "Includes at least 2 specific facts, examples, data points, or observations that relate to the claim.",
                "weight": 2,
            },
            {
                "id": "reasoning_present",
                "name": "Contains reasoning explaining WHY",
                "description": "At least 1 sentence explains WHY the evidence supports the claim, using signal words like 'because', 'this matters because', 'which means'.",
                "weight": 2,
            },
            {
                "id": "evidence_not_just_listed",
                "name": "Evidence is connected to the claim",
                "description": "Evidence is not just listed — each piece is followed by reasoning that explains its relevance to the claim.",
                "weight": 1,
            },
        ],
        "common_pitfalls": [
            "Listing facts without explaining why they matter (evidence without reasoning)",
            "Stating opinions as if they were evidence ('Everyone knows that...')",
            "Reasoning that just restates the evidence in different words",
            "All evidence is the same type (e.g., all personal opinion, no data or examples)",
        ],
        "min_words": 15,
    },

    "L03_independent_paragraph": {
        "task_type": "support_paragraph",
        "lesson": "L03",
        "description": "Write ONE body paragraph supporting a claim with evidence and reasoning",
        "criteria": [
            {
                "id": "topic_sentence",
                "name": "Topic sentence states a specific reason",
                "description": "Opens with a sentence that states ONE specific reason the claim is true.",
                "weight": 1,
            },
            {
                "id": "evidence_count",
                "name": "At least 2 pieces of evidence",
                "description": "Contains at least 2 facts, examples, or observations as evidence.",
                "weight": 2,
            },
            {
                "id": "reasoning_follows_evidence",
                "name": "Reasoning follows each piece of evidence",
                "description": "Each piece of evidence is followed by reasoning (look for 'because', 'this matters because', 'which means').",
                "weight": 2,
            },
            {
                "id": "concluding_tie_back",
                "name": "Concluding sentence ties back to claim",
                "description": "Ends with a sentence that connects back to the original claim.",
                "weight": 1,
            },
        ],
        "common_pitfalls": [
            "Evidence listed without reasoning — reads like a fact sheet",
            "Reasoning that just restates the claim ('This is why we should...' without explaining the mechanism)",
            "Only 1 piece of evidence (needs at least 2)",
            "No concluding sentence or conclusion that introduces a new idea",
        ],
        "min_words": 80,
    },

    # ===================== L04: Counterarguments =====================
    "L04_practice_counterargument": {
        "task_type": "counterargument_response",
        "lesson": "L04",
        "description": "Write a counterargument response using Acknowledge, Concede, Respond",
        "criteria": [
            {
                "id": "acknowledge_present",
                "name": "Acknowledges the opposing view",
                "description": "Contains a sentence that restates or summarizes the opposing argument fairly (signal: 'Some argue that...', 'Critics say...').",
                "weight": 2,
            },
            {
                "id": "concede_present",
                "name": "Concedes what is valid",
                "description": "Contains a sentence that admits something true or fair about the opposing view (signal: 'While it is true that...', 'Granted...').",
                "weight": 2,
            },
            {
                "id": "respond_present",
                "name": "Responds with why position still stands",
                "description": "Contains a sentence that explains why the writer's position holds despite the concession (signal: 'However...', 'But this overlooks...').",
                "weight": 2,
            },
            {
                "id": "genuine_counterargument",
                "name": "Counterargument is genuine, not a straw man",
                "description": "The opposing argument is one a smart person would actually make — not a weak or absurd version that is easy to dismiss.",
                "weight": 1,
            },
        ],
        "common_pitfalls": [
            "Straw man — presenting a weak version of the opposing argument that is easy to knock down",
            "Dismissing instead of conceding ('Some people think X but they are wrong')",
            "Missing one of the three moves entirely (usually the concede)",
            "Responding without actually addressing the conceded point",
        ],
        "min_words": 15,
    },

    "L04_independent_counterargument": {
        "task_type": "counterargument_response",
        "lesson": "L04",
        "description": "Write a counterargument paragraph for the student's own position using all three moves",
        "criteria": [
            {
                "id": "acknowledge_present",
                "name": "Acknowledges the opposing view",
                "description": "Contains a sentence that restates the opposing argument fairly.",
                "weight": 1,
            },
            {
                "id": "concede_present",
                "name": "Concedes what is valid",
                "description": "Admits something true about the opposing view.",
                "weight": 1,
            },
            {
                "id": "respond_present",
                "name": "Responds with why position still stands",
                "description": "Explains why the writer's position holds despite the concession.",
                "weight": 2,
            },
            {
                "id": "genuine_counterargument",
                "name": "Counterargument is genuine",
                "description": "The opposing argument is one a thoughtful person would actually make.",
                "weight": 1,
            },
            {
                "id": "paragraph_length",
                "name": "Paragraph is 80-120 words",
                "description": "Complete paragraph, not too short (under 60 words) or too long (over 150 words).",
                "weight": 1,
            },
        ],
        "common_pitfalls": [
            "Straw man counterargument",
            "Missing the concede move — jumping from acknowledge straight to respond",
            "Response that dismisses rather than engages ('They are wrong because...')",
            "Paragraph too short — all three moves need room to develop",
        ],
        "min_words": 80,
    },

    # ===================== L05: Argument Essay =====================
    "L05_independent_essay": {
        "task_type": "argument_essay",
        "lesson": "L05",
        "description": "Write a full argument essay (300-500 words) with introduction, body paragraphs, counterargument, and conclusion",
        "criteria": [
            {
                "id": "clear_position",
                "name": "Clear, specific position statement in introduction",
                "description": "The introduction contains a clear, specific, debatable position statement that passes the 3-Test Checklist.",
                "weight": 2,
            },
            {
                "id": "body_evidence_reasoning",
                "name": "Body paragraphs have evidence AND reasoning",
                "description": "At least 2 body paragraphs, each with a sub-claim supported by evidence AND reasoning (not just one).",
                "weight": 2,
            },
            {
                "id": "counterargument_three_moves",
                "name": "Counterargument uses all three moves",
                "description": "A counterargument section that acknowledges, concedes, and responds — not a dismissal.",
                "weight": 2,
            },
            {
                "id": "conclusion_restate_so_what",
                "name": "Conclusion restates position and explains 'so what'",
                "description": "The conclusion restates the position in different words AND explains why the argument matters.",
                "weight": 1,
            },
            {
                "id": "logical_organization",
                "name": "Essay is organized logically",
                "description": "Follows a clear structure: position, support, counterargument, conclusion. Ideas flow logically.",
                "weight": 1,
            },
        ],
        "common_pitfalls": [
            "Position statement is vague or not debatable",
            "Body paragraphs have evidence but no reasoning (or vice versa)",
            "Counterargument is a straw man or missing the concede move",
            "Conclusion just repeats the introduction without the 'so what'",
            "Essay is under 200 words — too short to develop all required elements",
        ],
        "min_words": 250,
    },

    # ===================== L06: You Already Make Choices =====================
    "L06_independent_choice_audit": {
        "task_type": "choice_audit",
        "lesson": "L06",
        "description": "Identify 3 specific choices an author makes in a passage and explain what each choice does",
        "criteria": [
            {
                "id": "names_specific_choices",
                "name": "Names specific authorial choices",
                "description": "Identifies at least 2 specific choices the author makes (e.g., word choice, sentence structure, opening strategy, tone) — not vague labels like 'good writing'.",
                "weight": 2,
            },
            {
                "id": "explains_what_choice_does",
                "name": "Explains what each choice does",
                "description": "For each choice identified, the student explains what the choice accomplishes — not just that it exists, but what effect it has.",
                "weight": 2,
            },
            {
                "id": "uses_m1_framework",
                "name": "Treats writing as deliberate choices",
                "description": "The response treats the author's writing as intentional decisions (M1: Everything Is a Choice), not as accidental or automatic.",
                "weight": 1,
            },
        ],
        "common_pitfalls": [
            "Naming vague features ('good vocabulary') instead of specific choices ('uses the word tyrant instead of ruler')",
            "Identifying choices but not explaining what they accomplish",
            "Treating the text as accidental rather than as a set of deliberate decisions",
        ],
        "min_words": 40,
    },

    # ===================== L07: Close Reading Protocol =====================
    "L07_independent_annotation": {
        "task_type": "close_reading",
        "lesson": "L07",
        "description": "Apply the close reading protocol to a passage — identify patterns and explain what they reveal",
        "criteria": [
            {
                "id": "identifies_patterns",
                "name": "Identifies specific textual patterns",
                "description": "Names at least 2 specific patterns in the text (repeated words, shifts in tone, structural choices, imagery clusters).",
                "weight": 2,
            },
            {
                "id": "explains_significance",
                "name": "Explains why patterns matter",
                "description": "Moves beyond identification to explain what the patterns reveal about the author's purpose or argument.",
                "weight": 2,
            },
            {
                "id": "uses_textual_evidence",
                "name": "Cites specific words or phrases",
                "description": "References specific words, phrases, or sentences from the text — not just general impressions.",
                "weight": 1,
            },
        ],
        "common_pitfalls": [
            "Listing observations without explaining their significance",
            "Making claims about the text without pointing to specific evidence",
            "Identifying only one pattern when multiple are present",
        ],
        "min_words": 40,
    },

    # ===================== L08: Structure-Function-Effect =====================
    "L08_independent_sfe": {
        "task_type": "sfe_analysis",
        "lesson": "L08",
        "description": "Write S-F-E analysis sentences identifying a structure, explaining its function, and connecting to its effect",
        "criteria": [
            {
                "id": "structure_named",
                "name": "Names a specific structure",
                "description": "Identifies a specific rhetorical or literary choice (diction, metaphor, repetition, sentence structure, etc.) with a textual example.",
                "weight": 1,
            },
            {
                "id": "function_explained",
                "name": "Explains the function",
                "description": "Explains WHAT the structure does — its purpose or role in the argument (e.g., 'creates contrast', 'builds credibility', 'signals a shift').",
                "weight": 2,
            },
            {
                "id": "effect_reached",
                "name": "Reaches Effect",
                "description": "Connects to the EFFECT on the reader or the argument as a whole — not just what it does, but why it matters or how it shapes the reader's response.",
                "weight": 2,
            },
        ],
        "common_pitfalls": [
            "Stopping at Structure (naming the device without explaining function or effect)",
            "Reaching Function but not Effect ('The metaphor compares X to Y' without explaining why that matters)",
            "Vague effect claims ('This is effective' without specifying how or why)",
            "Confusing summary of what the author says with analysis of how the author says it",
        ],
        "min_words": 30,
    },

    # ===================== L09: Analysis vs. Summary =====================
    "L09_independent_analysis": {
        "task_type": "analysis_paragraph",
        "lesson": "L09",
        "description": "Write an analytical paragraph that reaches Function and Effect, avoiding summary",
        "criteria": [
            {
                "id": "claim_about_how",
                "name": "Makes a claim about HOW, not just WHAT",
                "description": "The paragraph's main claim is about how the author achieves something (rhetorical strategy), not just what the author says (content summary).",
                "weight": 2,
            },
            {
                "id": "reaches_function",
                "name": "Reaches Function on evidence",
                "description": "At least one piece of evidence is explained at the Function level — what the choice does in context.",
                "weight": 2,
            },
            {
                "id": "reaches_effect",
                "name": "Reaches Effect on at least one piece of evidence",
                "description": "At least one piece of evidence is pushed to Effect — why the choice matters for the reader or the argument.",
                "weight": 2,
            },
            {
                "id": "avoids_summary",
                "name": "Avoids pure summary",
                "description": "The paragraph does not simply retell what happens in the text. Every sentence serves the analytical claim.",
                "weight": 1,
            },
        ],
        "common_pitfalls": [
            "Writing summary disguised as analysis ('The author says... then the author says...')",
            "Stopping at Function and never reaching Effect",
            "Making Effect claims that are vague ('This is powerful') instead of specific",
            "No textual evidence — claims without quotes or references",
        ],
        "min_words": 60,
    },

    # ===================== L10: S-F-E Fluency Drill =====================
    "L10_independent_sfe_drill": {
        "task_type": "sfe_analysis",
        "lesson": "L10",
        "description": "Rapid S-F-E analysis on multiple passages — must reach Effect consistently",
        "criteria": [
            {
                "id": "structure_specific",
                "name": "Names specific structures with evidence",
                "description": "Each analysis identifies a specific choice and quotes or references the relevant text.",
                "weight": 1,
            },
            {
                "id": "function_clear",
                "name": "Function is clearly stated",
                "description": "Explains what the choice does in context — not just labeling the device.",
                "weight": 2,
            },
            {
                "id": "effect_consistent",
                "name": "Reaches Effect consistently",
                "description": "Pushes to Effect (reader impact / argument significance) on at least half of the analyses.",
                "weight": 2,
            },
        ],
        "common_pitfalls": [
            "Rushing and only reaching Structure (naming devices without analysis)",
            "Repetitive effect claims ('This is effective' on every item)",
            "Confusing the author's content with the author's strategy",
        ],
        "min_words": 30,
    },

    # ===================== L11: Thesis Development =====================
    "L11_independent_thesis": {
        "task_type": "thesis_statement",
        "lesson": "L11",
        "description": "Write a text-based analytical thesis that is arguable, specific, and significant",
        "criteria": [
            {
                "id": "arguable",
                "name": "Thesis is arguable",
                "description": "A reasonable reader could disagree with this thesis. It makes a claim about HOW the text works, not just WHAT it says.",
                "weight": 2,
            },
            {
                "id": "specific",
                "name": "Thesis is specific",
                "description": "Names particular rhetorical choices, strategies, or techniques — not vague claims like 'uses many techniques'.",
                "weight": 2,
            },
            {
                "id": "significant",
                "name": "Thesis is significant",
                "description": "The claim matters — it tells us something important about how the text works, not something obvious.",
                "weight": 1,
            },
            {
                "id": "about_rhetoric_not_content",
                "name": "About rhetoric, not content",
                "description": "The thesis is about the author's choices and strategies, not a summary of the author's argument or topic.",
                "weight": 1,
            },
        ],
        "common_pitfalls": [
            "Thesis is about what the author says, not how they say it",
            "Too vague: 'The author uses rhetorical strategies to persuade the reader'",
            "Not arguable: merely stating a fact about the text ('Douglass gives a speech about slavery')",
            "Too many strategies listed without focus — tries to cover everything",
        ],
        "min_words": 15,
    },

    # ===================== L12: Essay Structures =====================
    "L12_independent_outline": {
        "task_type": "essay_outline",
        "lesson": "L12",
        "description": "Choose and outline an essay structure (Classical, Rogerian, etc.) for a given passage",
        "criteria": [
            {
                "id": "structure_chosen_justified",
                "name": "Structure choice is justified",
                "description": "The student names a specific structure (Classical, Rogerian, Problem-Solution, etc.) and explains WHY it fits this passage and argument.",
                "weight": 2,
            },
            {
                "id": "outline_complete",
                "name": "Outline includes all required sections",
                "description": "The outline has an introduction with thesis, body paragraphs with planned evidence, and a conclusion. No sections are missing.",
                "weight": 2,
            },
            {
                "id": "evidence_planned",
                "name": "Evidence is planned for each body paragraph",
                "description": "Each body paragraph in the outline names the specific quote or textual evidence that will be used.",
                "weight": 1,
            },
        ],
        "common_pitfalls": [
            "Choosing a structure without explaining why it fits",
            "Outline is too vague ('Body 1: talk about metaphor') — needs specific quotes planned",
            "Missing the conclusion or counterargument section",
            "Choosing a structure that doesn't match the argument being made",
        ],
        "min_words": 40,
    },

    # ===================== L13: Architecture and Evidence =====================
    "L13_independent_plan": {
        "task_type": "essay_plan",
        "lesson": "L13",
        "description": "Build a full essay architecture: thesis + evidence map with quotes assigned to paragraphs",
        "criteria": [
            {
                "id": "thesis_present",
                "name": "Has a clear analytical thesis",
                "description": "The plan includes a thesis that is arguable, specific, and about rhetorical choices.",
                "weight": 1,
            },
            {
                "id": "evidence_mapped",
                "name": "Evidence is mapped to paragraphs",
                "description": "At least 3 pieces of textual evidence (quotes) are assigned to specific body paragraphs.",
                "weight": 2,
            },
            {
                "id": "sfe_planned",
                "name": "S-F-E analysis is sketched for each quote",
                "description": "For each piece of evidence, the plan includes at least a note about what Function or Effect will be argued.",
                "weight": 2,
            },
        ],
        "common_pitfalls": [
            "Evidence selected but not assigned to specific paragraphs",
            "Quotes chosen that don't connect to the thesis",
            "No notes about what the analysis will say — just quotes with no planned commentary",
            "Only 1-2 quotes when 3+ are needed",
        ],
        "min_words": 40,
    },

    # ===================== L14: Body Paragraph Sprint =====================
    "L14_independent_paragraph": {
        "task_type": "analytical_body_paragraph",
        "lesson": "L14",
        "description": "Write a timed body paragraph with embedded evidence and S-F-E commentary",
        "criteria": [
            {
                "id": "topic_sentence_claim",
                "name": "Topic sentence makes an analytical claim",
                "description": "Opens with a claim about a rhetorical choice — not a summary statement.",
                "weight": 1,
            },
            {
                "id": "embedded_evidence",
                "name": "Evidence is embedded, not floating",
                "description": "Quotes are woven into the student's own sentences, not dropped in as standalone sentences.",
                "weight": 2,
            },
            {
                "id": "sfe_chain_complete",
                "name": "S-F-E chain is complete",
                "description": "Commentary moves from naming the Structure through Function to Effect — does not stop at identification.",
                "weight": 2,
            },
            {
                "id": "reaches_effect",
                "name": "Reaches Effect",
                "description": "At least one piece of evidence is analyzed all the way to Effect (reader/argument impact).",
                "weight": 2,
            },
            {
                "id": "concluding_tie",
                "name": "Ties back to thesis or larger argument",
                "description": "The paragraph ends by connecting back to the essay's thesis or the 'so what' of the analysis.",
                "weight": 1,
            },
        ],
        "common_pitfalls": [
            "Floating quotes — quote appears as its own sentence without integration",
            "Stopping at Function and never reaching Effect",
            "Topic sentence that summarizes the text instead of making an analytical claim",
            "No tie-back — paragraph ends after the quote or after Function",
        ],
        "min_words": 80,
    },

    # ===================== L15: Analysis vs. Summary Calibration =====================
    "L15_independent_calibration": {
        "task_type": "calibration_scoring",
        "lesson": "L15",
        "description": "Score sample paragraphs for analysis depth and justify the scores",
        "criteria": [
            {
                "id": "score_accurate",
                "name": "Score matches the rubric level",
                "description": "The student's assigned score aligns with the actual depth of the sample (within 1 point of the model score).",
                "weight": 2,
            },
            {
                "id": "justification_specific",
                "name": "Justification references specific evidence",
                "description": "The explanation points to specific sentences or phrases in the sample that justify the score — not vague impressions.",
                "weight": 2,
            },
            {
                "id": "uses_sfe_test",
                "name": "Applies the S-F-E test",
                "description": "The justification explicitly uses S-F-E levels (Structure, Function, Effect) to explain why the sample earns that score.",
                "weight": 1,
            },
        ],
        "common_pitfalls": [
            "Scoring too generously — giving high scores to paragraphs that stop at Function",
            "Justification is vague ('This is good analysis') without pointing to specific evidence",
            "Not using S-F-E language in the justification",
            "Confusing length with depth — long paragraphs aren't automatically better analysis",
        ],
        "min_words": 30,
    },

    # ===================== L16: Three-Pass Revision =====================
    "L16_independent_revision": {
        "task_type": "revision",
        "lesson": "L16",
        "description": "Apply the Three-Pass Revision Protocol to a body paragraph and explain which pass helped most",
        "criteria": [
            {
                "id": "unity_applied",
                "name": "Unity pass evidence",
                "description": "The revised paragraph shows evidence that drifting or off-topic sentences were identified and removed or moved.",
                "weight": 1,
            },
            {
                "id": "coherence_applied",
                "name": "Coherence pass evidence",
                "description": "The revised paragraph has clear transitions between ideas and logical flow within the paragraph.",
                "weight": 1,
            },
            {
                "id": "concision_applied",
                "name": "Concision pass evidence",
                "description": "The revised paragraph is tighter than the original — deadwood phrases removed, passive voice fixed where appropriate.",
                "weight": 1,
            },
            {
                "id": "diagnosis_specific",
                "name": "Self-diagnosis is specific",
                "description": "The student identifies which pass helped most and explains what it reveals about their writing habits.",
                "weight": 2,
            },
        ],
        "common_pitfalls": [
            "Claiming all three passes helped equally (rare — one usually helps most)",
            "Making only surface-level changes (fixing commas instead of cutting drifting sentences)",
            "Self-diagnosis is vague ('I need to revise more') instead of specific",
        ],
        "min_words": 80,
    },

    # ===================== L17: Style — Rhythm, Parallelism & Sentence Combining =====================
    "L17_independent_parallelism": {
        "task_type": "sentence_revision",
        "lesson": "L17",
        "description": "Fix broken parallelism in a sentence",
        "criteria": [
            {
                "id": "parallelism_fixed",
                "name": "All items use the same grammatical form",
                "description": "All items in the series use the same grammatical structure (all gerunds, all infinitives, all noun phrases, etc.).",
                "weight": 2,
            },
            {
                "id": "meaning_preserved",
                "name": "Original meaning is preserved",
                "description": "The revision fixes the structure without changing the meaning of the sentence.",
                "weight": 1,
            },
        ],
        "common_pitfalls": [
            "Fixing the form of one item but not all of them",
            "Changing the meaning while fixing the structure",
            "Creating a grammatically correct but awkward-sounding sentence",
        ],
        "min_words": 10,
    },

    "L17_independent_combining": {
        "task_type": "sentence_combining",
        "lesson": "L17",
        "description": "Combine sentences using subordination and/or coordination",
        "criteria": [
            {
                "id": "subordination_used",
                "name": "Uses at least one subordinate clause",
                "description": "The combined sentence uses a subordinating conjunction (when, because, although, etc.) to show the relationship between ideas.",
                "weight": 2,
            },
            {
                "id": "relationship_clear",
                "name": "Relationship between ideas is clear",
                "description": "The combination clarifies which idea is more important or how the ideas relate (cause-effect, contrast, concession).",
                "weight": 2,
            },
            {
                "id": "no_run_on",
                "name": "No run-on or comma splice",
                "description": "The combined sentence is grammatically correct — no fused sentences or comma splices.",
                "weight": 1,
            },
        ],
        "common_pitfalls": [
            "Joining with 'and' only (coordination when subordination would show the relationship better)",
            "Creating a run-on by combining without proper punctuation",
            "Losing one of the original ideas in the combination",
        ],
        "min_words": 15,
    },

    "L17_independent_rhythm": {
        "task_type": "rhythm_imitation",
        "lesson": "L17",
        "description": "Write three sentences following a LONG-SHORT-LONG rhythm pattern analyzing an author's choice",
        "criteria": [
            {
                "id": "long_short_long_pattern",
                "name": "Follows LONG-SHORT-LONG pattern",
                "description": "First sentence is 20+ words, second is 5 words or fewer, third is 20+ words.",
                "weight": 2,
            },
            {
                "id": "analytical_content",
                "name": "Content is analytical",
                "description": "The three sentences analyze an author's choice — not just describe or summarize.",
                "weight": 2,
            },
            {
                "id": "short_sentence_impact",
                "name": "Short sentence creates impact",
                "description": "The short sentence serves a purpose (emphasis, contrast, surprise) — not just an arbitrary cutoff.",
                "weight": 1,
            },
        ],
        "common_pitfalls": [
            "All three sentences are roughly the same length (no actual variation)",
            "Short sentence is just a filler ('This is true') instead of purposeful",
            "Content is summary, not analysis",
        ],
        "min_words": 40,
    },

    # ===================== L18: Pre-Gate Practice Essay =====================
    "L18_practice_essay": {
        "task_type": "analytical_essay",
        "lesson": "L18",
        "description": "Write a timed analytical essay on Red Cloud's Cooper Union speech",
        "criteria": [
            {
                "id": "arguable_thesis",
                "name": "Arguable thesis about rhetorical strategy",
                "description": "Contains a thesis that makes a specific, arguable claim about Red Cloud's rhetorical choices — not just what he says.",
                "weight": 2,
            },
            {
                "id": "embedded_evidence",
                "name": "At least 3 embedded quotes",
                "description": "Uses at least 3 quotes from the passage, embedded into the student's own sentences (not floating).",
                "weight": 2,
            },
            {
                "id": "sfe_commentary",
                "name": "Commentary reaches Effect",
                "description": "At least 2 pieces of evidence are analyzed through the S-F-E chain, reaching Effect (reader/argument impact).",
                "weight": 2,
            },
            {
                "id": "organized_structure",
                "name": "Clear essay structure",
                "description": "Has a recognizable introduction (with thesis), at least 2 body paragraphs, and a conclusion.",
                "weight": 1,
            },
            {
                "id": "conventions_clear",
                "name": "Conventions do not impede meaning",
                "description": "Writing is mostly clear — grammar and spelling errors do not prevent the reader from understanding the argument.",
                "weight": 1,
            },
        ],
        "common_pitfalls": [
            "Thesis is about what Red Cloud says, not how he says it",
            "Floating quotes without integration into sentences",
            "Commentary stops at Function — never reaches Effect",
            "Essay is mostly summary of the speech rather than analysis of rhetorical choices",
            "No conclusion or conclusion that just repeats the introduction",
        ],
        "min_words": 250,
    },

    # ===================== L19: Voice + Final Revision =====================
    "L19_supported_two_voices": {
        "task_type": "voice_exercise",
        "lesson": "L19",
        "description": "Write the same analytical claim in two different voices (spare/direct vs. elaborate/layered)",
        "criteria": [
            {
                "id": "two_versions_present",
                "name": "Two distinct versions are written",
                "description": "The student writes two versions of the same claim — one spare/direct and one elaborate/layered.",
                "weight": 1,
            },
            {
                "id": "voices_distinguishable",
                "name": "Voices are clearly different",
                "description": "The two versions sound noticeably different in sentence length, diction, and tone — not just minor word swaps.",
                "weight": 2,
            },
            {
                "id": "both_analytical",
                "name": "Both versions are analytical",
                "description": "Both versions make analytical claims about the text — neither one drifts into summary.",
                "weight": 2,
            },
        ],
        "common_pitfalls": [
            "Two versions that sound nearly identical (only changed a few words)",
            "One version is analytical but the other is just summary",
            "Confusing 'elaborate' with 'wordy' — adding filler instead of nuance",
        ],
        "min_words": 80,
    },

    "L19_independent_revision": {
        "task_type": "voice_revision",
        "lesson": "L19",
        "description": "Revise a paragraph from L18 to strengthen voice",
        "criteria": [
            {
                "id": "sentence_length_varied",
                "name": "At least 3 different sentence lengths",
                "description": "The revised paragraph contains short, medium, and long sentences — not all the same length.",
                "weight": 1,
            },
            {
                "id": "strong_verbs",
                "name": "At least one weak verb replaced",
                "description": "At least one instance of 'is', 'was', or 'has' replaced with a stronger action verb.",
                "weight": 1,
            },
            {
                "id": "filler_cut",
                "name": "At least one filler phrase removed",
                "description": "At least one unnecessary phrase was cut without losing meaning.",
                "weight": 1,
            },
            {
                "id": "voice_recognizable",
                "name": "Voice is recognizable and consistent",
                "description": "The paragraph sounds like a specific person — consistent tone, not generic student writing.",
                "weight": 2,
            },
        ],
        "common_pitfalls": [
            "Making only surface changes (fixing commas) instead of voice changes",
            "Trying to sound 'smart' instead of authentic — voice should feel natural",
            "All sentences still the same length after revision",
        ],
        "min_words": 80,
    },

    # ===================== L20: Gate Assessment =====================
    "L20_gate_essay": {
        "task_type": "analytical_essay",
        "lesson": "L20",
        "description": "Gate assessment analytical essay on Abigail Adams's 'Remember the Ladies' letter",
        "criteria": [
            {
                "id": "thesis_arguable_specific",
                "name": "Thesis: arguable and about rhetorical choices",
                "description": "Contains a clear thesis that makes an arguable claim about Adams's specific rhetorical strategies — not just what she says.",
                "weight": 1,
            },
            {
                "id": "evidence_3_plus",
                "name": "Evidence: 3+ well-selected, embedded quotes",
                "description": "Uses at least 3 relevant quotes from the passage, properly embedded into the student's sentences.",
                "weight": 2,
            },
            {
                "id": "commentary_function",
                "name": "Commentary reaches Function on some evidence",
                "description": "At least some evidence is analyzed at the Function level — explains what the choice does in context.",
                "weight": 1,
            },
            {
                "id": "commentary_effect",
                "name": "Commentary reaches Effect consistently",
                "description": "At least 2 pieces of evidence are pushed to Effect — explains why the choice matters for the reader or argument.",
                "weight": 2,
            },
            {
                "id": "conventions_clear",
                "name": "Conventions: mostly clear",
                "description": "Grammar and mechanics errors are minor and do not impede meaning.",
                "weight": 1,
            },
        ],
        "common_pitfalls": [
            "Thesis is about Adams's topic (women's rights) instead of her rhetorical choices",
            "Floating quotes — evidence not embedded into sentences",
            "Commentary stops at Structure or Function — never reaches Effect",
            "Essay is mostly summary of the letter",
            "Missing conclusion or conclusion that just restates intro",
        ],
        "min_words": 250,
    },

    # ===================== B1L: AP Language Gateways & Gate =====================

    "B1L_L07_gateway_essay": {
        "task_type": "rhetorical_analysis_essay",
        "lesson": "L07",
        "course": "B1L",
        "description": "Full rhetorical analysis essay on Frances Harper's 'We Are All Bound Up Together'",
        "scoring_model": "ap_rubric",
        "frq_type": "rhetorical_analysis",
        "gateway": True,
        "gateway_threshold": {"row_a": 1, "row_b": 2},
        "passage_id": "SP-024",
        "prompt": "Write an essay that analyzes the rhetorical choices Harper makes to argue for the interconnectedness of racial and gender justice.",
        "min_words": 250,
        "common_pitfalls": [
            "Summarizing Harper's arguments instead of analyzing her rhetorical strategies",
            "Feature-spotting: naming devices ('Harper uses pathos') without explaining function or effect",
            "Thesis about what Harper says rather than how she says it",
            "Ignoring the specific audience (white suffragists) and how Harper adapts her argument to them",
            "Treating the personal anecdotes as mere examples rather than analyzing their rhetorical function",
        ],
    },

    "B1L_L11_gateway_essay": {
        "task_type": "argument_essay",
        "lesson": "L11",
        "course": "B1L",
        "description": "Full AP argument essay from an original AP-style prompt",
        "scoring_model": "ap_rubric",
        "frq_type": "argument",
        "gateway": True,
        "gateway_threshold": {"row_a": 1, "row_b": 2},
        "prompt": "In a well-written essay, develop your position on whether individuals have an obligation to challenge unjust laws or whether stability and order should take precedence.",
        "min_words": 250,
        "common_pitfalls": [
            "Thesis that merely restates the prompt without taking a defensible position",
            "Evidence from personal experience only, without specific historical or literary examples",
            "Generic reasoning that could apply to any topic ('It is important because...')",
            "No counterargument or dismissive counterargument (straw man)",
            "Line of reasoning that lists reasons without connecting them to a throughline",
        ],
    },

    "B1L_L16_gateway_essay": {
        "task_type": "synthesis_essay",
        "lesson": "L16",
        "course": "B1L",
        "description": "Full AP synthesis essay on Environment & Economic Growth (SYN-06)",
        "scoring_model": "ap_rubric",
        "frq_type": "synthesis",
        "gateway": True,
        "gateway_threshold": {"row_a": 1, "row_b": 2, "min_sources": 3},
        "passage_id": "SYN-06",
        "prompt": "Synthesize material from at least three of the provided sources and develop a position on the relationship between environmental protection and economic growth.",
        "min_words": 250,
        "common_pitfalls": [
            "Using fewer than 3 sources",
            "Summarizing sources sequentially rather than synthesizing them into an argument",
            "Attributing evidence to sources but not explaining how it supports the argument",
            "Thesis that simply says 'both sides have good points' without taking a position",
            "Ignoring sources that complicate the argument",
        ],
    },

    "B1L_L19_gate_synthesis": {
        "task_type": "synthesis_essay",
        "lesson": "L19",
        "course": "B1L",
        "description": "Gate: AP Synthesis Essay on Universal Basic Income (SYN-08, cold source set)",
        "scoring_model": "ap_rubric",
        "frq_type": "synthesis",
        "gate": True,
        "gate_threshold": {"min_score": 4},
        "passage_id": "SYN-08",
        "prompt": "Synthesize material from at least three of the provided sources and develop a position on whether universal basic income is a viable policy solution for economic insecurity.",
        "min_words": 250,
        "common_pitfalls": [
            "Using fewer than 3 sources",
            "Summarizing sources rather than synthesizing",
            "No clear position — hedging without committing to a defensible thesis",
            "Ignoring economic counterarguments or dismissing them without engagement",
            "Citing sources without explaining their relevance to the argument",
        ],
    },

    "B1L_L20_gate_rhetorical_analysis": {
        "task_type": "rhetorical_analysis_essay",
        "lesson": "L20",
        "course": "B1L",
        "description": "Gate: AP Rhetorical Analysis Essay on Anna Julia Cooper (SP-034, reserved)",
        "scoring_model": "ap_rubric",
        "frq_type": "rhetorical_analysis",
        "gate": True,
        "gate_threshold": {"min_score": 4},
        "passage_id": "SP-034",
        "prompt": "Write an essay that analyzes the rhetorical choices Cooper makes to argue for the centrality of Black womanhood to racial progress.",
        "min_words": 250,
        "common_pitfalls": [
            "Summarizing Cooper's argument instead of analyzing her strategies",
            "Feature-spotting without function/effect analysis",
            "Missing the intersectional dimension of Cooper's rhetoric",
            "Thesis about Cooper's topic rather than her rhetorical approach",
        ],
    },

    "B1L_L20_gate_argument": {
        "task_type": "argument_essay",
        "lesson": "L20",
        "course": "B1L",
        "description": "Gate: AP Argument Essay (reserved prompt)",
        "scoring_model": "ap_rubric",
        "frq_type": "argument",
        "gate": True,
        "gate_threshold": {"min_score": 4},
        "prompt": "Some people argue that progress requires individuals willing to disrupt the status quo, while others believe lasting change comes through working within existing systems. Write an essay that develops your position on which approach is more likely to achieve meaningful and lasting change.",
        "min_words": 250,
        "common_pitfalls": [
            "Thesis that merely restates the prompt",
            "Only abstract reasoning without specific evidence",
            "No engagement with the opposing position",
            "Line of reasoning that doesn't build toward a larger claim",
        ],
    },

    # ===================== B2: AP Mastery Speed Runs & Gate =====================

    "B2_L08_speed_run_ra": {
        "task_type": "rhetorical_analysis_essay",
        "lesson": "L08",
        "course": "B2",
        "description": "Speed Run 1: Rhetorical Analysis on Wendell Phillips (SP-027)",
        "scoring_model": "ap_rubric",
        "frq_type": "rhetorical_analysis",
        "passage_id": "SP-027",
        "prompt": "Write an essay that analyzes the rhetorical choices Phillips makes to defend harsh abolitionist language and justify confrontational reform tactics.",
        "min_words": 250,
        "common_pitfalls": [
            "Summarizing Phillips's argument instead of analyzing his rhetoric",
            "Missing the meta-rhetorical dimension (Phillips is defending rhetoric with rhetoric)",
            "Feature-spotting without S-F-E analysis",
            "No sophistication move despite B2-level expectation",
        ],
    },

    "B2_L09_speed_run_arg": {
        "task_type": "argument_essay",
        "lesson": "L09",
        "course": "B2",
        "description": "Speed Run 2: Argument essay on knowledge and action",
        "scoring_model": "ap_rubric",
        "frq_type": "argument",
        "prompt": "Some people believe that knowledge is most valuable when it leads to action, while others argue that the pursuit of knowledge is inherently worthwhile regardless of its practical applications. Write an essay that develops your position on the relationship between knowledge and action.",
        "min_words": 250,
        "common_pitfalls": [
            "Vague thesis without clear position",
            "Evidence that is generic rather than specific",
            "No sophistication move",
            "Counterargument that is dismissive rather than engaged",
        ],
    },

    "B2_L10_speed_run_syn": {
        "task_type": "synthesis_essay",
        "lesson": "L10",
        "course": "B2",
        "description": "Speed Run 3: Synthesis on AI and Employment (SYN-09)",
        "scoring_model": "ap_rubric",
        "frq_type": "synthesis",
        "passage_id": "SYN-09",
        "prompt": "Synthesize material from at least three of the provided sources and develop a position on whether the benefits of AI-driven automation outweigh the risks to workers and communities.",
        "min_words": 250,
        "common_pitfalls": [
            "Using fewer than 3 sources",
            "Summarizing rather than synthesizing",
            "No M6 perspective analysis (whose perspective is represented/missing)",
            "No sophistication move despite B2-level expectation",
        ],
    },

    "B2_L11_plan_to_essay_ra": {
        "task_type": "rhetorical_analysis_essay",
        "lesson": "L11",
        "course": "B2",
        "description": "Plan-to-Essay Bridge 1: Rhetorical Analysis on Carrie Chapman Catt (SP-015)",
        "scoring_model": "ap_rubric",
        "frq_type": "rhetorical_analysis",
        "passage_id": "SP-015",
        "prompt": "Write an essay that analyzes the rhetorical choices Catt makes to argue that the suffrage movement has reached a decisive crisis point requiring immediate action.",
        "min_words": 250,
        "common_pitfalls": [
            "Summarizing Catt's argument rather than analyzing her strategies",
            "Missing the urgency rhetoric and how Catt constructs a sense of crisis",
            "Feature-spotting without reaching Effect",
            "Plan not reflected in the actual essay",
        ],
    },

    "B2_L12_plan_to_essay_arg": {
        "task_type": "argument_essay",
        "lesson": "L12",
        "course": "B2",
        "description": "Plan-to-Essay Bridge 2: Argument on tradition and progress",
        "scoring_model": "ap_rubric",
        "frq_type": "argument",
        "prompt": "Many argue that traditions provide stability and continuity, while others contend that clinging to tradition impedes necessary progress. Write an essay that develops your position on the tension between tradition and progress.",
        "min_words": 250,
        "common_pitfalls": [
            "Vague thesis that doesn't commit to a position",
            "Evidence from personal experience only",
            "Plan not reflected in the essay",
            "No sophistication move",
        ],
    },

    "B2_L21_gate_synthesis": {
        "task_type": "synthesis_essay",
        "lesson": "L21",
        "course": "B2",
        "description": "Gate: AP Synthesis Essay on Healthcare Access (SYN-10, reserved cold source set)",
        "scoring_model": "ap_rubric",
        "frq_type": "synthesis",
        "gate": True,
        "gate_threshold": {"min_score": 5, "floor_score": 4},
        "passage_id": "SYN-10",
        "prompt": "Synthesize material from at least three of the provided sources and develop a position on what approach to healthcare reform would best address both access and quality in the United States.",
        "min_words": 250,
        "common_pitfalls": [
            "Using fewer than 3 sources",
            "Binary framing (government vs. market) when sources suggest hybrid approaches",
            "No sophistication move — required at B2 level for score 5+",
            "Ignoring the rural/urban disparity raised in multiple sources",
            "Summarizing rather than synthesizing",
        ],
    },

    "B2_L22_gate_rhetorical_analysis": {
        "task_type": "rhetorical_analysis_essay",
        "lesson": "L22",
        "course": "B2",
        "description": "Gate: AP Rhetorical Analysis on Chief Joseph / William Apess (SP-035, reserved)",
        "scoring_model": "ap_rubric",
        "frq_type": "rhetorical_analysis",
        "gate": True,
        "gate_threshold": {"min_score": 5, "floor_score": 4},
        "passage_id": "SP-035",
        "prompt": "The following passages present two Native American speakers addressing white audiences about injustice. Write an essay that analyzes the rhetorical strategies each speaker uses and how those strategies reflect their different circumstances and purposes.",
        "min_words": 250,
        "common_pitfalls": [
            "Analyzing only one speaker and neglecting the comparison",
            "Summarizing what each speaker says rather than how they say it",
            "Missing the contrast between Chief Joseph's restraint and Apess's confrontation",
            "Feature-spotting without S-F-E analysis",
            "No sophistication move",
        ],
    },

    "B2_L22_gate_argument": {
        "task_type": "argument_essay",
        "lesson": "L22",
        "course": "B2",
        "description": "Gate: AP Argument Essay (reserved prompt)",
        "scoring_model": "ap_rubric",
        "frq_type": "argument",
        "gate": True,
        "gate_threshold": {"min_score": 5, "floor_score": 4},
        "prompt": "Some people argue that the pursuit of certainty — in science, politics, or personal belief — leads to deeper understanding, while others contend that certainty closes the mind and hinders genuine inquiry. Write an essay that develops your position on whether the pursuit of certainty helps or hinders understanding.",
        "min_words": 250,
        "common_pitfalls": [
            "Thesis that merely restates the prompt",
            "Only abstract philosophical reasoning without concrete evidence",
            "No engagement with the opposing position",
            "No sophistication move — required at B2 level",
            "Line of reasoning that lists reasons without building a throughline",
        ],
    },
}


# Merge course-specific rubrics
RUBRICS.update(A2_RUBRICS)
RUBRICS.update(B1L_RUBRICS)
RUBRICS.update(B2_RUBRICS)


def get_rubric(rubric_id: str) -> dict | None:
    """Look up a rubric by ID."""
    return RUBRICS.get(rubric_id)


def get_rubrics_for_lesson(lesson: str, course: str | None = None) -> list[dict]:
    """Get all rubrics for a given lesson (e.g., 'L01'), optionally filtered by course."""
    results = []
    for k, v in RUBRICS.items():
        if v["lesson"] == lesson:
            if course is None or v.get("course", "A1") == course:
                results.append({"id": k, **v})
    return results


def get_rubrics_for_course(course: str) -> list[dict]:
    """Get all rubrics for a given course (e.g., 'B1L')."""
    return [
        {"id": k, **v}
        for k, v in RUBRICS.items()
        if v.get("course", "A1") == course
    ]


def get_gateway_rubrics(course: str | None = None) -> list[dict]:
    """Get all gateway rubrics, optionally filtered by course."""
    results = []
    for k, v in RUBRICS.items():
        if v.get("gateway") or v.get("gate"):
            if course is None or v.get("course", "A1") == course:
                results.append({"id": k, **v})
    return results
