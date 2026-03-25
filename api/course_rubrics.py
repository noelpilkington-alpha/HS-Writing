"""
Course-specific rubrics for A2, B1L (non-gateway), and B2 (non-gateway).
Imported and merged into RUBRICS in grading_rubrics.py.
"""

A2_RUBRICS = {

    # ===================== A2 Unit 1: Force Field & Claim Hierarchy =====================

    "A2_L01_independent_force_field": {
        "task_type": "force_field_analysis",
        "lesson": "L01",
        "course": "A2",
        "scoring_model": "criteria",
        "description": "Map the Force Field for Patrick Henry and write 2 sentences explaining how one force shaped a specific choice",
        "criteria": [
            {"id": "identifies_force", "name": "Identifies a specific rhetorical force", "description": "Names one of the four forces (Audience, Exigence, Writer's Position, Context) and explains what it constrained or enabled.", "weight": 2},
            {"id": "names_specific_choice", "name": "Names a specific authorial choice", "description": "Points to a specific choice Henry made (word choice, strategy, tone, structure) — not vague.", "weight": 2},
            {"id": "explains_causal_connection", "name": "Explains how the force shaped the choice", "description": "Shows the connection between the force and the choice — explains WHY the force led to that decision.", "weight": 1},
        ],
        "common_pitfalls": [
            "Listing forces as a checklist without explaining constraints or enablements",
            "Identifying a choice but not connecting it to a specific force",
            "Vague force description without explaining what the audience prevented or enabled",
        ],
        "min_words": 30,
    },

    "A2_L02_independent_claim_hierarchy": {
        "task_type": "claim_hierarchy_analysis",
        "lesson": "L02",
        "course": "A2",
        "scoring_model": "criteria",
        "description": "Map the Claim Hierarchy of Thomas Paine's Common Sense and evaluate strongest/weakest claim",
        "criteria": [
            {"id": "maps_hierarchy", "name": "Maps thesis and claims", "description": "Identifies Paine's thesis and at least 2 main claims — shows hierarchical structure, not flat list.", "weight": 2},
            {"id": "evaluates_evidence_strength", "name": "Evaluates evidence strength", "description": "Identifies which claim has strongest evidence and which has weakest, with specific text reference.", "weight": 2},
            {"id": "justifies_evaluation", "name": "Justifies evaluation", "description": "Explains WHY one claim's evidence is stronger or weaker — not just assertions.", "weight": 1},
        ],
        "common_pitfalls": [
            "Listing Paine's claims as a flat sequence without showing hierarchy",
            "Confusing the thesis with a sub-claim",
            "Evaluating evidence strength based on personal agreement rather than textual support",
        ],
        "min_words": 40,
    },

    "A2_L03_independent_hierarchy_to_plan": {
        "task_type": "essay_plan",
        "lesson": "L03",
        "course": "A2",
        "scoring_model": "criteria",
        "description": "Build a Claim Hierarchy outline for an analytical essay on Stanton (thesis, 2 claims, evidence, counterargument)",
        "criteria": [
            {"id": "thesis_arguable", "name": "Thesis is arguable and analytical", "description": "Contains a thesis about Stanton's rhetorical strategies — not just what she says.", "weight": 2},
            {"id": "two_claims_hierarchical", "name": "Two claims that support thesis", "description": "Includes 2 sub-claims that clearly support the thesis and connect hierarchically.", "weight": 2},
            {"id": "evidence_planned", "name": "Evidence is planned for each claim", "description": "Each claim has at least one piece of textual evidence planned.", "weight": 1},
            {"id": "counterargument_included", "name": "Includes counterargument", "description": "Plan includes at least one counterargument that will be addressed.", "weight": 1},
        ],
        "common_pitfalls": [
            "Thesis about Stanton's topic rather than her rhetorical approach",
            "Two claims that are parallel but don't build hierarchically",
            "No evidence specified — just vague claim statements",
            "Counterargument missing or treated as afterthought",
        ],
        "min_words": 50,
    },

    # ===================== A2 Unit 2: They Say/I Say =====================

    "A2_L05_independent_they_say_i_say": {
        "task_type": "argumentative_response",
        "lesson": "L05",
        "course": "A2",
        "scoring_model": "criteria",
        "description": "Write all 3 They Say/I Say moves (agree with difference, disagree diplomatically, complicate) with no templates",
        "criteria": [
            {"id": "all_three_moves_present", "name": "All three moves are present", "description": "Response includes distinct examples of all 3 moves: Agree with Difference, Disagree Diplomatically, Complicate the Debate.", "weight": 2},
            {"id": "genuine_engagement", "name": "Genuine engagement with opposing view", "description": "Each move represents the opposing view fairly — no straw man arguments.", "weight": 2},
            {"id": "no_template_dependence", "name": "Written without visible template dependence", "description": "The moves sound natural, not mechanically filled-in templates.", "weight": 1},
        ],
        "common_pitfalls": [
            "Missing one of the three moves (usually 'complicate the debate')",
            "Straw man version of opposing view that's easy to dismiss",
            "Visible template language repeated mechanically",
            "Response that dismisses rather than engages",
        ],
        "min_words": 40,
    },

    "A2_L06_independent_nuance_ladder": {
        "task_type": "thesis_revision",
        "lesson": "L06",
        "course": "A2",
        "scoring_model": "criteria",
        "description": "Revise 2 flat, binary positions through 3 levels of nuance, write final nuanced thesis",
        "criteria": [
            {"id": "progression_through_levels", "name": "Shows progression through nuance levels", "description": "Each position moves through at least 2 visible revision stages, getting more nuanced.", "weight": 2},
            {"id": "final_thesis_nuanced", "name": "Final thesis is genuinely nuanced", "description": "Final version qualifies claims, acknowledges complexity, or reframes the debate.", "weight": 2},
            {"id": "uses_m3_or_m4", "name": "Uses M3 or M4 reasoning", "description": "Revision demonstrates awareness of audience constraints (M3) or claim hierarchy (M4).", "weight": 1},
        ],
        "common_pitfalls": [
            "Final 'nuanced' version is just the original with 'sometimes' added",
            "Revision makes the position weaker rather than more sophisticated",
            "No visible progression — only shows flat and final version",
            "Nuance that hedges instead of complicates",
        ],
        "min_words": 40,
    },

    "A2_L07_gateway_essay": {
        "task_type": "argument_essay",
        "lesson": "L07",
        "course": "A2",
        "scoring_model": "criteria",
        "gateway": True,
        "gateway_threshold": {"min_score": 4},
        "description": "Full argument essay using They Say/I Say structure (25 min timed)",
        "criteria": [
            {"id": "thesis_they_say_i_say", "name": "Thesis uses They Say/I Say framing", "description": "Introduction includes a 'They Say' and an 'I Say' — not just a flat claim.", "weight": 1},
            {"id": "argument_structure", "name": "Argument structure follows Claim Hierarchy", "description": "Builds claims hierarchically with evidence and reasoning — at least 2 body paragraphs.", "weight": 2},
            {"id": "counterargument_genuine", "name": "Counterargument is genuine, not straw man", "description": "Addresses the strongest opposing view, concedes something valid, responds thoughtfully.", "weight": 1},
            {"id": "evidence_and_commentary", "name": "Evidence + reasoning present", "description": "Claims supported with specific evidence AND reasoning.", "weight": 1},
            {"id": "conventions", "name": "Conventions do not impede meaning", "description": "Grammar and mechanics errors are minor.", "weight": 1},
        ],
        "common_pitfalls": [
            "Thesis states a position without engaging the 'They Say' conversation",
            "Counterargument is a weak straw man version",
            "Missing the concede move in counterargument",
            "Evidence without reasoning or reasoning without evidence",
        ],
        "min_words": 250,
    },

    # ===================== A2 Unit 3: Synthesis =====================

    "A2_L08_independent_source_evaluation": {
        "task_type": "source_analysis",
        "lesson": "L08",
        "course": "A2",
        "scoring_model": "criteria",
        "description": "Evaluate 2 sources: identify perspective, what it reveals, what it obscures",
        "criteria": [
            {"id": "identifies_perspective", "name": "Identifies source perspective", "description": "For each source, names whose perspective or interest the source represents.", "weight": 2},
            {"id": "what_it_reveals", "name": "Explains what the source reveals", "description": "Identifies what aspects of the debate the source illuminates.", "weight": 1},
            {"id": "what_it_obscures", "name": "Explains what the source obscures", "description": "Identifies what the source downplays, omits, or ignores.", "weight": 2},
        ],
        "common_pitfalls": [
            "Treating sources as neutral rather than having a perspective",
            "Identifying perspective but not explaining what it reveals or obscures",
            "Only identifying what the source says, not what it hides",
        ],
        "min_words": 40,
    },

    "A2_L09_independent_synthesis_matrix": {
        "task_type": "synthesis_planning",
        "lesson": "L09",
        "course": "A2",
        "scoring_model": "criteria",
        "description": "Complete Synthesis Matrix for Source Set A (4 sources, 3 themes) + 1 synthesis sentence",
        "criteria": [
            {"id": "matrix_complete", "name": "Matrix maps sources by theme", "description": "Organizes what each source says about each theme — not source-by-source summary.", "weight": 2},
            {"id": "synthesis_sentence_combines", "name": "Synthesis sentence combines sources", "description": "Weaves 2 sources together around a theme — not sequential.", "weight": 2},
            {"id": "organized_by_argument", "name": "Organized by argument, not source", "description": "Prioritizes the thematic argument, using sources as support.", "weight": 1},
        ],
        "common_pitfalls": [
            "Matrix organized by source rather than themes",
            "Synthesis sentence that summarizes sources sequentially",
            "Themes that are too broad rather than specific analytical angles",
        ],
        "min_words": 20,
    },

    "A2_L10_independent_attribution": {
        "task_type": "evidence_integration",
        "lesson": "L10",
        "course": "A2",
        "scoring_model": "criteria",
        "description": "Integrate 3 pieces of evidence using the most appropriate signal phrase for each",
        "criteria": [
            {"id": "attribution_varied", "name": "Uses varied signal phrases", "description": "3 integrations use 3 different signal phrases — not all 'according to'.", "weight": 2},
            {"id": "signal_phrase_appropriate", "name": "Signal phrase matches source attitude", "description": "Each signal phrase accurately reflects the source's stance.", "weight": 2},
            {"id": "evidence_embedded", "name": "Evidence is embedded, not dropped", "description": "Evidence is woven into the student's own sentences.", "weight": 1},
        ],
        "common_pitfalls": [
            "Using 'according to' or 'says' for all integrations",
            "Signal phrase doesn't match the source's stance",
            "Floating quotes as standalone sentences",
        ],
        "min_words": 30,
    },

    "A2_L11_independent_source_weaving": {
        "task_type": "synthesis_paragraph",
        "lesson": "L11",
        "course": "A2",
        "scoring_model": "criteria",
        "description": "Write 1 paragraph integrating 3 sources around a student-generated claim (no scaffold)",
        "criteria": [
            {"id": "claim_first_structure", "name": "Claim-first, not source-first", "description": "Opens with the student's claim, then uses sources to support it.", "weight": 2},
            {"id": "three_sources_woven", "name": "Three sources are woven together", "description": "All 3 sources appear and interact (agreement, contrast, or synthesis).", "weight": 2},
            {"id": "avoids_serial_summary", "name": "Avoids serial summarizing", "description": "Sources are not presented sequentially — they talk to each other.", "weight": 2},
        ],
        "common_pitfalls": [
            "Serial summarizing — organizing by source rather than argument",
            "Claim stated but sources just listed without synthesis",
            "Only 2 sources used when 3 are required",
        ],
        "min_words": 80,
    },

    "A2_L12_gateway_synthesis_essay": {
        "task_type": "synthesis_essay",
        "lesson": "L12",
        "course": "A2",
        "scoring_model": "criteria",
        "gateway": True,
        "gateway_threshold": {"min_score": 4},
        "description": "Full synthesis essay on Source Set C (25 min timed, at least 3 of 4 sources)",
        "criteria": [
            {"id": "thesis_original", "name": "Thesis states student's own position", "description": "Student's original argument — not just summarizing sources.", "weight": 1},
            {"id": "source_integration", "name": "Sources are synthesized, not serial", "description": "Weaves sources by theme/argument — not 'Source A says... Source B says...'", "weight": 2},
            {"id": "three_sources", "name": "At least 3 sources integrated", "description": "Integrates evidence from at least 3 of 4 sources with attribution.", "weight": 2},
            {"id": "argument_sophistication", "name": "Argument shows sophistication", "description": "Engages complexity — acknowledges counterarguments or tensions between sources.", "weight": 1},
            {"id": "conventions", "name": "Conventions do not impede meaning", "description": "Grammar and attribution mechanics are mostly clear.", "weight": 1},
        ],
        "common_pitfalls": [
            "Using fewer than 3 sources",
            "Serial summarizing instead of synthesis",
            "Thesis that just says 'sources disagree' without taking a position",
            "Sources cited but not explained",
        ],
        "min_words": 250,
    },

    # ===================== A2 Unit 4: Self-Assessment =====================

    "A2_L14_independent_self_score_revision": {
        "task_type": "self_assessment_and_revision",
        "lesson": "L14",
        "course": "A2",
        "scoring_model": "criteria",
        "description": "Self-score L07 essay on 3-point rubric, identify improvement, revise one paragraph",
        "criteria": [
            {"id": "self_score_accurate", "name": "Self-score is calibrated", "description": "Score on 3-point rubric (Weak/Adequate/Strong) is within 1 level of actual quality.", "weight": 1},
            {"id": "improvement_specific", "name": "Identifies specific improvement", "description": "Names specific weakness — not vague ('needs to be better').", "weight": 2},
            {"id": "revision_demonstrates", "name": "Revision shows the improvement", "description": "Revised paragraph actually addresses the identified weakness.", "weight": 2},
        ],
        "common_pitfalls": [
            "Self-score too generous — calling Adequate work Strong",
            "Identifying vague improvement without specific diagnosis",
            "Revision doesn't actually fix the identified problem",
            "Making only surface-level changes instead of substantive revision",
        ],
        "min_words": 80,
    },

    # ===================== A2 Unit 5: Timed Writing =====================

    "A2_L15_independent_good_enough_plan": {
        "task_type": "timed_planning",
        "lesson": "L15",
        "course": "A2",
        "scoring_model": "criteria",
        "description": "'Good Enough' plan (5 min) + first paragraph (5 min)",
        "criteria": [
            {"id": "plan_complete", "name": "Plan is complete in time", "description": "Includes thesis, 2-3 claims, and key evidence — within 5 minutes.", "weight": 2},
            {"id": "paragraph_follows_plan", "name": "First paragraph follows the plan", "description": "Written paragraph reflects the planned thesis and opening claim.", "weight": 2},
            {"id": "plan_sufficient", "name": "Plan is good enough — messy but sufficient", "description": "Has enough detail to write from but isn't over-planned.", "weight": 1},
        ],
        "common_pitfalls": [
            "Over-planning — spending more than 5 minutes",
            "Plan too vague without specific thesis or claims",
            "First paragraph doesn't match the plan",
        ],
        "min_words": 50,
    },

    # ===================== A2 Unit 6: ACT Writing =====================

    "A2_L16_independent_act_perspectives": {
        "task_type": "perspective_analysis",
        "lesson": "L16",
        "course": "A2",
        "scoring_model": "criteria",
        "description": "Decompose all 3 ACT perspectives and evaluate strengths/limitations",
        "criteria": [
            {"id": "three_decomposed", "name": "All three perspectives decomposed", "description": "Identifies core claim, underlying assumption, and value for each perspective.", "weight": 2},
            {"id": "strengths_identified", "name": "Strength of each identified", "description": "For each, names a condition where it is strongest.", "weight": 2},
            {"id": "limitations_identified", "name": "Limitation of each identified", "description": "For each, names a gap or condition where the perspective fails.", "weight": 1},
        ],
        "common_pitfalls": [
            "Summarizing what perspectives say without decomposing assumptions",
            "Evaluating based on personal agreement rather than analytical strengths",
            "Only analyzing 2 perspectives instead of all 3",
        ],
        "min_words": 50,
    },

    "A2_L17_independent_constructed_support": {
        "task_type": "evidence_generation",
        "lesson": "L17",
        "course": "A2",
        "scoring_model": "criteria",
        "description": "Generate 4 types of support, rank by persuasiveness, write opposition paragraph",
        "criteria": [
            {"id": "four_types", "name": "All four support types generated", "description": "Includes real-world example, logical reasoning, hypothetical scenario, analogy.", "weight": 2},
            {"id": "ranking_justified", "name": "Ranking is justified", "description": "Ranks by persuasiveness and explains why one type is stronger.", "weight": 1},
            {"id": "opposition_they_say", "name": "Opposition paragraph uses They Say/I Say", "description": "Acknowledges strongest opposing perspective, concedes, responds.", "weight": 2},
        ],
        "common_pitfalls": [
            "Missing one or more support types",
            "Real-world example is just personal anecdote without broader significance",
            "Opposition paragraph dismisses rather than engages",
        ],
        "min_words": 80,
    },

    "A2_L18_independent_act_essay_1": {
        "task_type": "act_essay",
        "lesson": "L18",
        "course": "A2",
        "scoring_model": "criteria",
        "description": "Full ACT essay #1 — 35 min timed",
        "criteria": [
            {"id": "ideas_analysis", "name": "Ideas & Analysis", "description": "Develops a clear position that engages multiple perspectives.", "weight": 2},
            {"id": "development_support", "name": "Development & Support", "description": "Uses reasoning and specific examples — not just abstract claims.", "weight": 2},
            {"id": "organization", "name": "Organization", "description": "Clear introduction, body paragraphs, and conclusion.", "weight": 1},
            {"id": "language_use", "name": "Language Use", "description": "Mostly clear and grammatical.", "weight": 1},
        ],
        "common_pitfalls": [
            "Position just repeats one given perspective without development",
            "No engagement with other perspectives",
            "Support is all personal opinion without specific examples",
            "Essay under 200 words",
        ],
        "min_words": 250,
    },

    "A2_L19_independent_act_essay_2": {
        "task_type": "act_essay",
        "lesson": "L19",
        "course": "A2",
        "scoring_model": "criteria",
        "description": "Full ACT essay #2 — 35 min timed",
        "criteria": [
            {"id": "ideas_analysis", "name": "Ideas & Analysis", "description": "Develops a clear position that engages multiple perspectives.", "weight": 2},
            {"id": "development_support", "name": "Development & Support", "description": "Uses reasoning and specific examples.", "weight": 2},
            {"id": "organization", "name": "Organization", "description": "Clear logical structure.", "weight": 1},
            {"id": "language_use", "name": "Language Use", "description": "Mostly clear and grammatical.", "weight": 1},
        ],
        "common_pitfalls": [
            "Position just repeats one given perspective",
            "No engagement with opposing perspectives",
            "Support is all personal opinion",
            "No improvement from Essay #1",
        ],
        "min_words": 250,
    },

    "A2_L20_gate_synthesis": {
        "task_type": "synthesis_essay",
        "lesson": "L20",
        "course": "A2",
        "scoring_model": "criteria",
        "gate": True,
        "gate_threshold": {"min_score": 4},
        "description": "Gate: Synthesis essay on Source Set D (40 min)",
        "criteria": [
            {"id": "thesis_original", "name": "Thesis states own position", "description": "Student's original argument synthesizing source material.", "weight": 1},
            {"id": "source_integration", "name": "Sources synthesized, not serial", "description": "Weaves at least 3 sources by theme/argument.", "weight": 2},
            {"id": "argument_sophistication", "name": "Argument shows sophistication", "description": "Acknowledges complexity, qualifies claims, or addresses tensions.", "weight": 2},
            {"id": "conventions", "name": "Conventions do not impede meaning", "description": "Grammar and attribution are mostly clear.", "weight": 1},
        ],
        "common_pitfalls": [
            "Using fewer than 3 sources",
            "Serial summarizing instead of synthesis",
            "Thesis that doesn't take a position",
            "No engagement with counterarguments",
        ],
        "min_words": 250,
    },

    "A2_L20_gate_act_essay": {
        "task_type": "act_essay",
        "lesson": "L20",
        "course": "A2",
        "scoring_model": "criteria",
        "gate": True,
        "gate_threshold": {"min_score": 4},
        "description": "Gate: ACT essay on Prompt 7 (40 min)",
        "criteria": [
            {"id": "ideas_analysis", "name": "Ideas & Analysis", "description": "Develops a clear, thoughtful position engaging all 3 perspectives.", "weight": 2},
            {"id": "development_support", "name": "Development & Support", "description": "Specific reasoning and examples from knowledge.", "weight": 2},
            {"id": "organization", "name": "Organization", "description": "Clear and logical structure.", "weight": 1},
            {"id": "language_use", "name": "Language Use", "description": "Clear, varied, and grammatically sound.", "weight": 1},
        ],
        "common_pitfalls": [
            "Position adopts one given perspective without development",
            "No engagement with opposing perspectives",
            "Support is all abstract or personal anecdote",
            "Essay under 250 words",
        ],
        "min_words": 250,
    },
}


B1L_RUBRICS = {

    # ===================== B1L Unit 1: Rhetorical Analysis =====================

    "B1L_L01_independent_decision_reconstruction": {
        "task_type": "decision_reconstruction",
        "lesson": "L01",
        "course": "B1L",
        "scoring_model": "criteria",
        "description": "Decision Reconstruction on Ida B. Wells — 3 key moments as 'writer's problem was ___, solved by ___'",
        "criteria": [
            {"id": "identifies_writer_problem", "name": "Identifies the writer's problem at each moment", "description": "For each of the 3 moments, clearly names what rhetorical or argumentative problem the writer faced.", "weight": 2},
            {"id": "identifies_solution", "name": "Identifies how the writer solved it", "description": "For each problem, identifies the specific choice the writer made to solve it.", "weight": 2},
            {"id": "uses_m5_framework", "name": "Uses M5 'If I Were Writing This' lens", "description": "Frames the analysis as reverse engineering decisions, not summarizing content.", "weight": 1},
            {"id": "three_moments_present", "name": "Covers 3 distinct key moments", "description": "Addresses 3 different moments from the passage.", "weight": 1},
        ],
        "common_pitfalls": [
            "Summarizing what Wells says rather than reconstructing WHY she made specific choices",
            "Identifying problems about content rather than rhetoric",
            "Solutions that are vague instead of specific choices",
            "Only addressing 1-2 moments instead of 3",
        ],
        "min_words": 30,
    },

    "B1L_L02_independent_rhetorical_situation": {
        "task_type": "rhetorical_situation_map",
        "lesson": "L02",
        "course": "B1L",
        "scoring_model": "criteria",
        "description": "Timed (3 min) rhetorical situation map for Wendell Phillips",
        "criteria": [
            {"id": "exigence_identified", "name": "Identifies the exigence", "description": "Names the specific problem or occasion that prompted the writing.", "weight": 2},
            {"id": "audience_characterized", "name": "Characterizes the audience with needs/resistance", "description": "Names the specific audience and identifies what they need or resist.", "weight": 2},
            {"id": "key_constraint_identified", "name": "Identifies a key constraint", "description": "Names at least one constraint that shapes the writer's choices.", "weight": 1},
        ],
        "common_pitfalls": [
            "Exigence too vague instead of specific problem",
            "Audience identified but not characterized",
            "No constraint mentioned",
        ],
        "min_words": 20,
    },

    "B1L_L03_independent_strategy_identification": {
        "task_type": "strategy_identification",
        "lesson": "L03",
        "course": "B1L",
        "scoring_model": "criteria",
        "description": "Identify rhetorical strategies in William Apess and select the 2-3 that matter most",
        "criteria": [
            {"id": "identifies_multiple", "name": "Identifies multiple strategies from different categories", "description": "Names at least 3 specific rhetorical strategies from different categories.", "weight": 2},
            {"id": "selects_key", "name": "Selects 2-3 strategies that matter most", "description": "Narrows to the 2-3 most important strategies for the writer's purpose.", "weight": 2},
            {"id": "justifies_selection", "name": "Justifies the selection", "description": "Explains WHY these 2-3 strategies matter most.", "weight": 1},
        ],
        "common_pitfalls": [
            "Listing strategies without identifying which ones matter most",
            "Vague identifications without citing specific examples",
            "Selection criteria not based on rhetorical significance",
        ],
        "min_words": 25,
    },

    "B1L_L04_independent_analytical_sentences": {
        "task_type": "sfe_analysis",
        "lesson": "L04",
        "course": "B1L",
        "scoring_model": "criteria",
        "description": "Analytical S-F-E sentences for 3 strategies from an AP passage",
        "criteria": [
            {"id": "structure_named", "name": "Names each structure with evidence", "description": "For each sentence, identifies a specific strategy and references the text.", "weight": 1},
            {"id": "function_explained", "name": "Explains function for each strategy", "description": "Each sentence explains WHAT the strategy does in context.", "weight": 2},
            {"id": "effect_reached", "name": "Reaches Effect on at least 2 strategies", "description": "At least 2 sentences push to Effect — impact on the reader or argument.", "weight": 2},
            {"id": "avoids_feature_spotting", "name": "Avoids feature-spotting", "description": "All sentences are analytical, not just device identification.", "weight": 1},
        ],
        "common_pitfalls": [
            "Stopping at Structure or Function without reaching Effect",
            "Effect claims that are vague instead of specific to rhetorical situation",
            "Feature-spotting without explaining function or effect",
        ],
        "min_words": 30,
    },

    "B1L_L05_independent_thesis": {
        "task_type": "thesis_statement",
        "lesson": "L05",
        "course": "B1L",
        "scoring_model": "criteria",
        "description": "Write AP rhetorical analysis thesis for William Lloyd Garrison passage",
        "criteria": [
            {"id": "names_strategies", "name": "Names specific rhetorical strategies", "description": "The thesis identifies at least 2 specific strategies.", "weight": 2},
            {"id": "states_purpose", "name": "Connects strategies to purpose", "description": "The thesis states what the writer is trying to achieve.", "weight": 1},
            {"id": "line_of_reasoning", "name": "Establishes a line of reasoning", "description": "Previews HOW the strategies work together.", "weight": 2},
            {"id": "defensible", "name": "Thesis is defensible", "description": "Makes an arguable claim about the passage.", "weight": 1},
        ],
        "common_pitfalls": [
            "Thesis about what the author says rather than how they say it",
            "Listing strategies without connecting them to purpose",
            "No line of reasoning",
        ],
        "min_words": 20,
    },

    "B1L_L06_independent_body_paragraph": {
        "task_type": "rhetorical_analysis_paragraph",
        "lesson": "L06",
        "course": "B1L",
        "scoring_model": "criteria",
        "description": "7-minute body paragraph sprint on Carrie Chapman Catt",
        "criteria": [
            {"id": "analytical_claim", "name": "Opens with analytical claim", "description": "Topic sentence makes a claim about what a strategy does.", "weight": 1},
            {"id": "evidence_present", "name": "Includes specific textual evidence", "description": "Contains at least one quote or specific paraphrase.", "weight": 1},
            {"id": "sfe_present", "name": "Includes S-F-E analysis", "description": "Explains Structure, Function, and Effect.", "weight": 2},
            {"id": "reaches_effect", "name": "Reaches Effect level", "description": "Connects to rhetorical impact.", "weight": 2},
            {"id": "connects_to_purpose", "name": "Connects back to purpose", "description": "Ties back to the writer's overall rhetorical purpose.", "weight": 1},
        ],
        "common_pitfalls": [
            "Topic sentence that summarizes content instead of analytical claim",
            "Feature-spotting without explaining function or effect",
            "Evidence dropped without analysis",
            "Stopping at Function and never reaching Effect",
        ],
        "min_words": 60,
    },

    # ===================== B1L Unit 2: AP Argument Essay =====================

    "B1L_L08_independent_prompt_deconstruction": {
        "task_type": "prompt_analysis",
        "lesson": "L08",
        "course": "B1L",
        "scoring_model": "criteria",
        "description": "Deconstruct AP argument prompt — identify claim, complexity, map 3 positions, choose strongest",
        "criteria": [
            {"id": "core_claim", "name": "Identifies the core claim", "description": "Clearly states the central claim or question in the prompt.", "weight": 1},
            {"id": "complexity", "name": "Identifies what makes it debatable", "description": "Names the tension or competing values that make it complex.", "weight": 2},
            {"id": "three_positions", "name": "Maps 3 possible positions", "description": "Identifies agree, disagree, and complicate positions.", "weight": 2},
            {"id": "strongest_chosen", "name": "Chooses strongest with justification", "description": "Selects one position and explains why it's strongest.", "weight": 1},
        ],
        "common_pitfalls": [
            "Confusing the topic with the claim",
            "Three positions that are all variations of 'agree'",
            "No justification for choosing strongest position",
        ],
        "min_words": 30,
    },

    "B1L_L09_independent_evidence_and_reasoning": {
        "task_type": "argument_planning",
        "lesson": "L09",
        "course": "B1L",
        "scoring_model": "criteria",
        "description": "Evidence brainstorm (6+), rank by strength, write thesis + 3 topic sentences",
        "criteria": [
            {"id": "evidence_quantity", "name": "Generates 6+ pieces of evidence", "description": "Brainstorms at least 6 pieces from knowledge.", "weight": 1},
            {"id": "evidence_ranked", "name": "Ranks evidence by strength", "description": "Identifies strongest vs. weakest pieces.", "weight": 1},
            {"id": "thesis_clear", "name": "Thesis is clear and defensible", "description": "Takes a clear position that is arguable.", "weight": 2},
            {"id": "line_of_reasoning", "name": "Topic sentences build a line of reasoning", "description": "The 3 topic sentences advance the argument progressively.", "weight": 2},
        ],
        "common_pitfalls": [
            "Generating only 3-4 pieces instead of brainstorming broadly",
            "All evidence is the same type",
            "Topic sentences that list parallel reasons instead of building",
        ],
        "min_words": 40,
    },

    "B1L_L10_independent_body_paragraphs": {
        "task_type": "argument_paragraphs",
        "lesson": "L10",
        "course": "B1L",
        "scoring_model": "criteria",
        "description": "Write 1 body paragraph + 1 counterargument paragraph (12 min timed)",
        "criteria": [
            {"id": "body_claim", "name": "Body paragraph: Clear claim", "description": "Opens with a topic sentence that advances the line of reasoning.", "weight": 1},
            {"id": "body_evidence", "name": "Body paragraph: Specific evidence", "description": "Contains at least one specific example with enough detail.", "weight": 2},
            {"id": "body_commentary", "name": "Body paragraph: Commentary explains HOW", "description": "Explains HOW the evidence supports the claim.", "weight": 1},
            {"id": "counterarg_moves", "name": "Counterargument: Three moves", "description": "Includes acknowledge, concede, respond.", "weight": 2},
            {"id": "counterarg_genuine", "name": "Counterargument: Genuine opposition", "description": "Addresses a real, strong opposing position.", "weight": 1},
        ],
        "common_pitfalls": [
            "Vague evidence instead of specific examples",
            "Evidence dropped without commentary",
            "Counterargument that dismisses instead of engaging",
            "Missing the concede move",
        ],
        "min_words": 80,
    },

    "B1L_L12_independent_sophistication_revision": {
        "task_type": "revision",
        "lesson": "L12",
        "course": "B1L",
        "scoring_model": "criteria",
        "description": "Revise L11 weakest paragraph to include a Row C sophistication move",
        "criteria": [
            {"id": "identifies_weakest", "name": "Identifies weakest paragraph", "description": "Correctly diagnoses which paragraph lacks sophistication.", "weight": 1},
            {"id": "sophistication_added", "name": "Adds a sophistication move", "description": "Includes at least one Row C move: broader context, tension, alternative interpretation, or vivid style.", "weight": 2},
            {"id": "sophistication_integrated", "name": "Sophistication is integrated", "description": "Move fits naturally, doesn't feel like an afterthought.", "weight": 2},
            {"id": "original_preserved", "name": "Original argument preserved", "description": "Deepens without abandoning original claim.", "weight": 1},
        ],
        "common_pitfalls": [
            "Choosing a paragraph that already had sophistication",
            "Adding complexity that contradicts the thesis",
            "Sophistication that feels tacked on",
            "Revising for length instead of depth",
        ],
        "min_words": 60,
    },

    # ===================== B1L Unit 3: AP Synthesis Essay =====================

    "B1L_L13_independent_source_selection": {
        "task_type": "source_selection",
        "lesson": "L13",
        "course": "B1L",
        "scoring_model": "criteria",
        "description": "Choose 3-4 sources from SYN-04 matrix and justify each selection",
        "criteria": [
            {"id": "three_plus", "name": "Selects 3-4 sources", "description": "Chooses 3 or 4 sources.", "weight": 1},
            {"id": "strategic", "name": "Selection is strategic", "description": "Sources chosen to support thesis, provide counterargument, or add perspectives.", "weight": 2},
            {"id": "justifies_each", "name": "Justifies each selection", "description": "Explains WHY each was chosen and what role it plays.", "weight": 2},
            {"id": "considers_excluded", "name": "Explains what was excluded", "description": "Notes which sources were NOT chosen and why.", "weight": 1},
        ],
        "common_pitfalls": [
            "Choosing sources because they're easy, not strongest",
            "Selecting all sources that agree — no counterargument source",
            "Justification repeats what source says instead of strategic role",
        ],
        "min_words": 30,
    },

    "B1L_L14_independent_source_weaving": {
        "task_type": "self_assessment",
        "lesson": "L14",
        "course": "B1L",
        "scoring_model": "criteria",
        "description": "Self-assess both source weaving paragraphs on synthesis vs. serial, attribution, forced weaving",
        "criteria": [
            {"id": "synthesis_vs_serial", "name": "Identifies synthesis vs. serial", "description": "Accurately diagnoses whether each paragraph synthesizes or lists serially.", "weight": 2},
            {"id": "attribution_assessment", "name": "Assesses attribution fluency", "description": "Notes whether attribution is fluent or mechanical.", "weight": 2},
            {"id": "forced_weaving_check", "name": "Identifies forced weaving", "description": "Recognizes if sources feel forced or irrelevant.", "weight": 1},
            {"id": "specific_evidence", "name": "Cites specific sentences", "description": "Points to specific sentences as evidence.", "weight": 1},
        ],
        "common_pitfalls": [
            "Claiming both paragraphs synthesize when one is clearly serial",
            "Not recognizing forced weaving",
            "Vague self-assessment without specific evidence",
        ],
        "min_words": 30,
    },

    "B1L_L15_independent_attribution_and_planning": {
        "task_type": "synthesis_planning",
        "lesson": "L15",
        "course": "B1L",
        "scoring_model": "criteria",
        "description": "Attribution fluency drill (5 sentences, 5 patterns) + full synthesis planning for SYN-06",
        "criteria": [
            {"id": "attribution_patterns", "name": "Uses 5 different attribution patterns", "description": "5 sentences demonstrate 5 distinct attribution patterns.", "weight": 2},
            {"id": "attribution_fluent", "name": "Attribution is fluent", "description": "Sentences sound natural and varied.", "weight": 1},
            {"id": "planning_complete", "name": "Planning is complete", "description": "SYN-06 plan includes thesis, source selection, and outline of 3 body paragraphs.", "weight": 2},
            {"id": "sources_assigned", "name": "Sources assigned to paragraphs", "description": "Plan clearly indicates which sources in each paragraph.", "weight": 1},
        ],
        "common_pitfalls": [
            "Attribution drill uses only 2-3 patterns instead of 5",
            "Planning is too vague without assigning sources",
            "Sources listed but not assigned to specific paragraphs",
        ],
        "min_words": 50,
    },

    # ===================== B1L Unit 4: AP Calibration & Revision =====================

    "B1L_L17_independent_calibration": {
        "task_type": "calibration_scoring",
        "lesson": "L17",
        "course": "B1L",
        "scoring_model": "criteria",
        "description": "Re-score own essays (L07, L11, L16) with calibrated eyes",
        "criteria": [
            {"id": "scores_all_three", "name": "Scores all 3 essays on Rows A, B, C", "description": "Provides Row A (0-1), Row B (0-4), Row C (0-1) for each.", "weight": 1},
            {"id": "score_justification", "name": "Justifies each score", "description": "Explains the score with reference to specific sentences.", "weight": 2},
            {"id": "calibration_shift", "name": "Identifies calibration shift", "description": "Notes where original scoring differs from current and explains what changed.", "weight": 2},
            {"id": "pattern_identified", "name": "Identifies weakest row pattern", "description": "Recognizes consistent weakness across essays.", "weight": 1},
        ],
        "common_pitfalls": [
            "Scores haven't changed from original — no calibration learning",
            "Justifications are vague without citing specific evidence",
            "No recognition of a pattern across essays",
        ],
        "min_words": 40,
    },

    "B1L_L18_independent_revision": {
        "task_type": "targeted_revision",
        "lesson": "L18",
        "course": "B1L",
        "scoring_model": "criteria",
        "description": "Choose 2 essays and revise the weakest row in each",
        "criteria": [
            {"id": "weakest_row_identified", "name": "Correctly identifies weakest row", "description": "For both essays, accurately diagnoses which row is weakest.", "weight": 1},
            {"id": "row_a_fix", "name": "Row A fix (if needed)", "description": "If Row A weak, adds or strengthens line of reasoning.", "weight": 2},
            {"id": "row_b_fix", "name": "Row B fix (if needed)", "description": "If Row B weak, converts feature-spotting to full S-F-E chains.", "weight": 2},
            {"id": "row_c_fix", "name": "Row C fix (if needed)", "description": "If Row C weak, adds broader context, tension, or alternative interpretation.", "weight": 2},
            {"id": "no_weakening", "name": "Revision doesn't weaken other rows", "description": "Improves weakest row without creating new problems.", "weight": 1},
        ],
        "common_pitfalls": [
            "Revising the wrong row — choosing one already strong",
            "Row B fix that adds length but not analysis depth",
            "Row C fix that feels bolted on",
            "Revision that fixes one problem but creates another",
        ],
        "min_words": 80,
    },
}


B2_RUBRICS = {

    # ===================== B2 Unit 1: Who Benefits? =====================

    "B2_L01_independent_m6_analysis": {
        "task_type": "m6_analysis",
        "lesson": "L01",
        "course": "B2",
        "scoring_model": "criteria",
        "description": "M6 protocol analysis on contemporary editorial — visible/obscured/who benefits/alternative framing for 2 moves",
        "criteria": [
            {"id": "m6_visible", "name": "Identifies what framing makes visible", "description": "Names specific aspects foregrounded by the framing.", "weight": 2},
            {"id": "m6_obscured", "name": "Names what framing obscures", "description": "Identifies perspectives or complications the framing hides.", "weight": 2},
            {"id": "m6_benefits", "name": "Explains who benefits", "description": "Analyzes whose position is strengthened (framing effects, not authorial motivation).", "weight": 2},
            {"id": "m6_alternative", "name": "Describes alternative framing", "description": "Proposes at least one alternative framing and why writer didn't choose it.", "weight": 1},
        ],
        "common_pitfalls": [
            "Confusing M6 with strategy effectiveness analysis",
            "Claiming the writer personally benefits rather than analyzing framing effects",
            "Describing what the text says rather than what the framing reveals/obscures",
        ],
        "min_words": 100,
    },

    "B2_L02_independent_framing_analysis": {
        "task_type": "framing_analysis",
        "lesson": "L02",
        "course": "B2",
        "scoring_model": "criteria",
        "description": "Full framing analysis on economic policy excerpt — M6 protocol + 2 sophistication sentences",
        "criteria": [
            {"id": "m6_protocol_complete", "name": "Completes M6 4-question protocol", "description": "Addresses all 4 questions: visible, obscured, who benefits, alternative framing.", "weight": 2},
            {"id": "sophistication_sentences", "name": "Generates 2 sophistication sentences", "description": "Writes 2 sentences using M6 analysis for Row C thinking.", "weight": 2},
            {"id": "organic_integration", "name": "Sophistication feels organic", "description": "Sentences deepen analysis rather than feeling tacked on.", "weight": 2},
        ],
        "common_pitfalls": [
            "Completing M6 protocol but failing to generate sophistication sentences",
            "Writing sophistication sentences that feel like trivia",
            "Focusing on content rather than framing choices",
        ],
        "min_words": 80,
    },

    "B2_L03_independent_sophistication_identification": {
        "task_type": "sophistication_addition",
        "lesson": "L03",
        "course": "B2",
        "scoring_model": "criteria",
        "description": "Read essay scored 4 (Row C=0), identify where sophistication could go, write 2-3 sentences adding it",
        "criteria": [
            {"id": "placement_strategic", "name": "Strategic placement", "description": "Identifies logical location where sophistication deepens rather than interrupts.", "weight": 1},
            {"id": "type_appropriate", "name": "Appropriate sophistication type", "description": "Chooses type that fits the passage and argument.", "weight": 2},
            {"id": "execution_quality", "name": "Quality of sophistication move", "description": "Demonstrates genuine analytical depth, not surface-level addition.", "weight": 2},
            {"id": "integration", "name": "Organic integration", "description": "New sentences flow naturally from existing analysis.", "weight": 2},
        ],
        "common_pitfalls": [
            "Choosing placement that interrupts flow",
            "Adding historical trivia that doesn't deepen analysis",
            "Writing sophistication that contradicts the essay's thesis",
        ],
        "min_words": 50,
    },

    # ===================== B2 Unit 2: Writing Sophistication =====================

    "B2_L04_independent_broader_context": {
        "task_type": "body_paragraph",
        "lesson": "L04",
        "course": "B2",
        "scoring_model": "criteria",
        "description": "Body paragraph on Emma Goldman (SP-017) with organic broader context move",
        "criteria": [
            {"id": "sfe_analysis", "name": "S-F-E analysis", "description": "Identifies strategy, explains function, analyzes effect; reaches Effect level.", "weight": 2},
            {"id": "broader_context", "name": "Broader context move", "description": "Situates Goldman's choices within larger historical/cultural context.", "weight": 2},
            {"id": "context_organic", "name": "Context is organic", "description": "Context explains WHY Goldman made these choices; removing it would weaken analysis.", "weight": 2},
        ],
        "common_pitfalls": [
            "Adding historical facts that don't explain rhetorical choices",
            "Placing context at end as separate sentence rather than integrating",
            "Summarizing argument rather than analyzing strategies",
        ],
        "min_words": 120,
    },

    "B2_L05_independent_alternative_reading": {
        "task_type": "body_paragraph",
        "lesson": "L05",
        "course": "B2",
        "scoring_model": "criteria",
        "description": "Body paragraph on William Apess (ES-029) with alternative reading move",
        "criteria": [
            {"id": "sfe_analysis", "name": "S-F-E analysis", "description": "Clear analysis with Strategy-Function-Effect framework.", "weight": 2},
            {"id": "alternative_reading", "name": "Alternative reading move", "description": "Presents plausible alternative interpretation of the same evidence.", "weight": 2},
            {"id": "your_reading_stronger", "name": "Explains why your reading is stronger", "description": "Argues back explaining why original interpretation is more complete.", "weight": 2},
        ],
        "common_pitfalls": [
            "Confusing alternative reading with counterargument",
            "Presenting alternative but never arguing back",
            "Alternative reading feels implausible",
        ],
        "min_words": 120,
    },

    "B2_L06_independent_tension_exploration": {
        "task_type": "tension_analysis",
        "lesson": "L06",
        "course": "B2",
        "scoring_model": "criteria",
        "description": "Return to previously analyzed passage, find missed tension, write 3 sentences exploring without resolving",
        "criteria": [
            {"id": "tension_identified", "name": "Identifies genuine tension", "description": "Names contradiction or complexity that resists simple resolution.", "weight": 2},
            {"id": "exploration_not_resolution", "name": "Explores without resolving", "description": "Sits with complexity rather than explaining it away.", "weight": 2},
            {"id": "analytical_depth", "name": "Demonstrates sophisticated thinking", "description": "Explains why tension matters and complicates straightforward interpretation.", "weight": 2},
        ],
        "common_pitfalls": [
            "Identifying surface contradiction rather than productive tension",
            "Resolving the tension rather than exploring it",
            "Calling something a tension when it's just two different ideas",
        ],
        "min_words": 60,
    },

    "B2_L07_independent_sophistication_paragraph": {
        "task_type": "sophistication_paragraph",
        "lesson": "L07",
        "course": "B2",
        "scoring_model": "criteria",
        "description": "Write essay plan for argument prompt, then write ONLY the sophistication paragraph (7 min timed)",
        "criteria": [
            {"id": "plan_complete", "name": "Complete essay plan", "description": "Includes thesis, 3 body claims, sophistication type/location.", "weight": 1},
            {"id": "sophistication_present", "name": "Sophistication move executed", "description": "Paragraph contains identifiable Row C move.", "weight": 2},
            {"id": "paragraph_coherence", "name": "Paragraph functions as body paragraph", "description": "Has claim, evidence, reasoning; sophistication enhances core argument.", "weight": 2},
            {"id": "sophistication_organic", "name": "Sophistication is organic", "description": "Deepens analysis rather than feeling appended.", "weight": 2},
        ],
        "common_pitfalls": [
            "Writing sophistication as separate paragraph rather than integrating",
            "Planning sophistication but forgetting to execute it",
            "Paragraph that is ONLY sophistication with no claim/evidence",
        ],
        "min_words": 100,
    },

    # ===================== B2 Unit 3: Recovery Drill =====================

    "B2_L13_recovery_drill": {
        "task_type": "rhetorical_analysis_essay",
        "lesson": "L13",
        "course": "B2",
        "scoring_model": "criteria",
        "description": "Recovery drill: minimum viable essay in 30 min on Garrison (SP-028). Thesis + 2 body paragraphs + conclusion.",
        "criteria": [
            {"id": "completeness", "name": "Essay is complete", "description": "Finished essay with intro, 2 body paragraphs, conclusion; no abrupt endings.", "weight": 2},
            {"id": "row_a_thesis", "name": "Thesis with line of reasoning", "description": "Clear thesis previewing TWO strategies.", "weight": 2},
            {"id": "row_b_analysis", "name": "S-F-E analysis in both paragraphs", "description": "Both body paragraphs include Strategy-Function-Effect analysis.", "weight": 2},
            {"id": "triage_decisions", "name": "Sacrificed right elements", "description": "Sacrificed third body paragraph and elaborate intro, NOT analysis quality.", "weight": 1},
        ],
        "common_pitfalls": [
            "Attempting 3 body paragraphs and running out of time",
            "Spending too long on intro/conclusion instead of analysis",
            "Feature-spotting rather than reaching Effect",
        ],
        "min_words": 250,
    },

    # ===================== B2 Unit 4: Self-Diagnosis & Revision =====================

    "B2_L14_independent_recalibration": {
        "task_type": "self_assessment",
        "lesson": "L14",
        "course": "B2",
        "scoring_model": "criteria",
        "description": "Re-score Speed Run 1 essay (L08) with calibrated eyes after 4 calibration exercises",
        "criteria": [
            {"id": "row_scores_accurate", "name": "Scores within 1 point on each row", "description": "Row A, B, C scores within 1 point of expert scores.", "weight": 2},
            {"id": "identifies_drift", "name": "Identifies calibration drift", "description": "Names where original self-score differed and explains the error.", "weight": 2},
            {"id": "specific_evidence", "name": "Uses specific evidence from essay", "description": "Points to specific sentences that justify re-score.", "weight": 1},
        ],
        "common_pitfalls": [
            "Re-scoring but not explaining calibration drift",
            "Changing score without evidence from the essay",
            "Over-scoring due to recognizing own writing",
        ],
        "min_words": 40,
    },

    "B2_L15_independent_pattern_diagnosis": {
        "task_type": "self_diagnosis",
        "lesson": "L15",
        "course": "B2",
        "scoring_model": "criteria",
        "description": "Diagnose Speed Run 3 + write 3-sentence pattern diagnosis across all 3 speed runs",
        "criteria": [
            {"id": "specific_diagnosis", "name": "Specific diagnosis", "description": "Identifies SPECIFIC problem within weakest row, not vague.", "weight": 2},
            {"id": "prescription_actionable", "name": "Actionable prescription", "description": "Prescribes ONE concrete practice target for each essay.", "weight": 2},
            {"id": "pattern_identified", "name": "Identifies consistent pattern", "description": "3-sentence pattern diagnosis recognizes weakness across multiple essays.", "weight": 2},
        ],
        "common_pitfalls": [
            "Diagnosing different weaknesses in each essay (missing the pattern)",
            "Vague diagnosis like 'needs more analysis'",
            "Prescription too broad rather than concrete",
        ],
        "min_words": 100,
    },

    "B2_L16_independent_revision_comparison": {
        "task_type": "revision",
        "lesson": "L16",
        "course": "B2",
        "scoring_model": "criteria",
        "description": "Surface edit (2 min) then substantive revision (5 min) on weakest Speed Run paragraph. Compare.",
        "criteria": [
            {"id": "surface_appropriate", "name": "Surface edit targets surface issues", "description": "2-min edit fixes grammar, punctuation, word choice.", "weight": 1},
            {"id": "substantive_changes_ideas", "name": "Substantive revision changes ideas", "description": "5-min revision alters thesis, evidence, argument structure, or analytical depth.", "weight": 2},
            {"id": "comparison_accurate", "name": "Accurate comparison", "description": "Correctly identifies which version improved Row score.", "weight": 2},
        ],
        "common_pitfalls": [
            "Doing surface editing during substantive revision time",
            "Substantive revision that changes wording but not ideas",
            "Claiming surface edit improved score when it only improved clarity",
        ],
        "min_words": 50,
    },

    "B2_L17_independent_multipass_revision": {
        "task_type": "revision",
        "lesson": "L17",
        "course": "B2",
        "scoring_model": "criteria",
        "description": "Apply 4-pass revision protocol to Speed Run essay. Pass 1: Thesis/Structure, Pass 2: Evidence/Analysis, Pass 3: Sophistication, Pass 4: Style/Concision.",
        "criteria": [
            {"id": "pass1", "name": "Pass 1: Improves thesis/structure", "description": "Strengthens thesis clarity or line of reasoning.", "weight": 2},
            {"id": "pass2", "name": "Pass 2: Deepens evidence/analysis", "description": "Adds S-F-E analysis or replaces summary with Effect-level thinking.", "weight": 2},
            {"id": "pass3", "name": "Pass 3: Adds organic sophistication", "description": "Integrates M6 move that feels organic.", "weight": 2},
            {"id": "pass4", "name": "Pass 4: Refines style", "description": "Cuts wordiness, varies sentence length, strengthens voice.", "weight": 1},
            {"id": "transformation", "name": "Revised paragraph shows transformation", "description": "Final version is meaningfully different from original.", "weight": 2},
        ],
        "common_pitfalls": [
            "Trying to do all 4 passes simultaneously",
            "Pass 3 sophistication feels tacked on",
            "Final paragraph is only surface-edited",
        ],
        "min_words": 60,
    },

    # ===================== B2 Unit 5: Voice Development =====================

    "B2_L18_independent_voice_analysis": {
        "task_type": "voice_analysis",
        "lesson": "L18",
        "course": "B2",
        "scoring_model": "criteria",
        "description": "Describe own voice in 2 sentences (diction, syntax, register, rhythm). Identify 2 syntactic choices to strengthen.",
        "criteria": [
            {"id": "voice_description", "name": "Accurate voice description", "description": "Uses voice framework (diction, syntax, register, rhythm) to characterize current writing.", "weight": 2},
            {"id": "default_vs_chosen", "name": "Identifies default vs. chosen voice", "description": "Recognizes whether current voice is default academic or intentionally chosen.", "weight": 1},
            {"id": "syntactic_choices", "name": "Identifies 2 specific syntactic choices", "description": "Names concrete changes that would strengthen voice.", "weight": 2},
        ],
        "common_pitfalls": [
            "Describing content rather than voice",
            "Vague descriptions like 'my voice is good'",
            "Not recognizing template language as absence of voice",
        ],
        "min_words": 60,
    },

    "B2_L19_independent_voice_paragraph": {
        "task_type": "body_paragraph",
        "lesson": "L19",
        "course": "B2",
        "scoring_model": "criteria",
        "description": "Write body paragraph in YOUR chosen voice. Apply 'read aloud test' — no template language.",
        "criteria": [
            {"id": "voice_intentional", "name": "Voice is intentional", "description": "Diction, syntax, rhythm reflect conscious choices, not generic academic prose.", "weight": 2},
            {"id": "analysis_quality", "name": "Maintains analytical quality", "description": "Voice doesn't sacrifice S-F-E analysis.", "weight": 2},
            {"id": "passes_read_aloud", "name": "Passes 'read aloud test'", "description": "Sounds like a human voice, not template language.", "weight": 2},
        ],
        "common_pitfalls": [
            "Voice becomes conversational at expense of analytical rigor",
            "Starting with voice but reverting to templates mid-paragraph",
            "Confusing fancy vocabulary with voice",
        ],
        "min_words": 100,
    },

    "B2_L20_independent_voice_under_pressure": {
        "task_type": "timed_paragraph",
        "lesson": "L20",
        "course": "B2",
        "scoring_model": "criteria",
        "description": "Timed body paragraph (7 min) on Catt (SP-015) with S-F-E, sophistication move, and voice",
        "criteria": [
            {"id": "sfe_complete", "name": "S-F-E analysis complete", "description": "Reaches Effect level despite time pressure.", "weight": 2},
            {"id": "sophistication_present", "name": "Sophistication move included", "description": "Contains identifiable Row C move.", "weight": 2},
            {"id": "voice_maintained", "name": "Voice maintained under pressure", "description": "Does not revert to template language.", "weight": 2},
        ],
        "common_pitfalls": [
            "Time pressure causes reversion to template prose",
            "Including sophistication but forgetting S-F-E",
            "Running out of time mid-paragraph",
        ],
        "min_words": 100,
    },
}
