"""
Per-lesson, per-task grading rubrics for A1 Course.

Each rubric defines:
- task_type: what kind of writing task
- criteria: list of specific, observable criteria to evaluate
- common_pitfalls: mistakes to watch for (used in grading prompt)
- min_words: minimum word count for the task
- max_score: maximum score for the task (number of criteria)
"""

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
}


def get_rubric(rubric_id: str) -> dict | None:
    """Look up a rubric by ID."""
    return RUBRICS.get(rubric_id)


def get_rubrics_for_lesson(lesson: str) -> list[dict]:
    """Get all rubrics for a given lesson (e.g., 'L01')."""
    return [
        {"id": k, **v}
        for k, v in RUBRICS.items()
        if v["lesson"] == lesson
    ]
