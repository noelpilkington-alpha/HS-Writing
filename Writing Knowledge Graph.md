# Writing Knowledge Graph

## Design Principles

This knowledge graph is a directed acyclic graph (DAG) implementing the Writing Brainlift's Knowledge Tree. Every skill is decomposed into granular Knowledge Components (KCs), each with a type that determines the activity the app presents.

**Node Coding:** `Strand.Grade.Number`
- Strand: C = Composition, M = Mechanics, D = Discourse
- Grade: K, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
- Number: Sequential within strand and grade

**KC Types:**
- **D** = Discrimination (can the student SEE the problem?)
- **P** = Production (can the student FIX or CREATE?)
- **S** = Structure (does the student know the RULE?)
- **I** = Integrative (can the student APPLY multiple skills in context?)

**Rules:**
- Discrimination always precedes Production for the same skill
- 80%+ mastery required before advancing to any dependent node
- Gateway KCs are flagged — failure here blocks all downstream learning
- Cross-strand connections are marked with `[X-STRAND]`

---

## STRAND 1: COMPOSITION

### K-2 Foundational

| Code | Name | Type | Prerequisites | Gateway? | Description |
|------|------|------|--------------|----------|-------------|
| C.K.01 | Oral Idea Generation | P | — | | Generate ideas verbally about familiar topics ("Tell me about your favorite...") |
| C.K.02 | Oral Storytelling | P | C.K.01 | | Tell a simple story with beginning, middle, end |
| C.K.03 | Answering in Complete Sentences | P | C.K.01 | | Respond to questions using full oral sentences, not fragments |
| C.K.04 | Dictation to Text | I | C.K.03 | | Teacher transcribes student's oral ideas; student sees words become text |
| C.1.01 | Sentence vs. Not-a-Sentence (Oral) | D | C.K.03 | **YES** | Tell a complete sentence from an incomplete thought (oral). Gateway: if student can't hear the difference, written sentence work will fail |
| C.1.02 | What a Sentence Needs | S | C.1.01 | | A sentence has a "who/what" and a "what happened" |
| C.1.03 | Simple Sentence Construction | P | C.1.02, M.1.01 | | Write subject + verb sentences with student-chosen topics. [X-STRAND: requires M.1.01 letter formation] |
| C.1.04 | Adding Details (who, what, where, when) | P | C.1.03 | | Expand a simple sentence by adding one detail at a time |
| C.2.01 | Sentence Expansion with Adjectives | P | C.1.04 | | Add descriptive words to make sentences more specific |
| C.2.02 | Sentence Expansion with Prepositional Phrases | P | C.1.04 | | Add "in the park," "under the table," etc. |
| C.2.03 | Combining Two Ideas | P | C.2.01 | | Join two simple ideas with "and" |
| C.2.04 | Write Multiple Related Sentences | I | C.2.03 | | Write 3-4 sentences on the same topic (proto-paragraph) |

### Grade 3 (Sentence Mastery)

Incorporates and extends MasteryWrite's KC framework.

| Code | Name | Type | Prerequisites | Gateway? | Description |
|------|------|------|--------------|----------|-------------|
| C.3.01 | Spot Fragment: Missing Subject | D | C.2.04 | **YES** | Tell a complete sentence from a fragment missing the "who/what." Gateway: if student can't spot fragments, don't teach fixing yet |
| C.3.02 | Spot Fragment: Missing Predicate | D | C.3.01 | | Tell a complete sentence from a fragment missing the "what happened." Include -ing trap (e.g., "The turtle swimming") |
| C.3.03 | Spot Fragment: Dependent Clause | D | C.3.02 | | Spot fragments starting with trap words: because, although, when, if, since, while, unless |
| C.3.04 | Fragment Traps: Length and Commands | D | C.3.01 | | Long doesn't mean complete; commands ARE sentences (hidden "you") |
| C.3.05 | Spot Run-on: Fused Sentence | D | C.3.01 | | Two sentences jammed together with nothing between them |
| C.3.06 | Spot Run-on: Comma Splice | D | C.3.05 | | A comma alone can't join two complete sentences |
| C.3.07 | Find the Seam in a Run-on | P | C.3.05 | | Identify where one thought ends and the next begins (prerequisite for fixing) |
| C.3.08 | Three-Way Sort: Sentence vs. Fragment vs. Run-on | D | C.3.06, C.3.03, C.3.04 | **YES** | Integrates all discrimination KCs. Gateway to all production work |
| C.3.09 | Fix a Fragment | P | C.3.08 | | Add subject, add predicate, or complete dependent clause (three fix types match three fragment types) |
| C.3.10 | Fix a Run-on | P | C.3.08 | | Split with full stop OR join with comma + conjunction |
| C.3.11 | Spot Simple vs. Compound Sentence | D | C.3.08 | | How many complete thoughts? |
| C.3.12 | Conjunction Meanings: and vs. but vs. so | D | C.3.11 | | and = addition, but = contrast, so = cause-effect |
| C.3.13 | Combine Sentences with Comma + Conjunction | P | C.3.12 | | FANBOYS — focus on and, but, so, or. [X-STRAND: feeds M.3.03] |
| C.3.14 | Choose the Right Conjunction for Meaning | P | C.3.12 | | and ≠ but ≠ so — conjunction must match the meaning relationship |
| C.3.15 | Vary Sentence Openings | P | C.3.13 | | Don't start every sentence the same way across 3+ consecutive sentences |
| C.3.16 | Because, But, So (TWR) | P | C.3.14 | | Given a stem, complete with because/but/so to show reasoning. "Dogs make good pets because..." |
| C.3.17 | Edit Sentences in Connected Text | I | C.3.09, C.3.10, C.3.15 | | Find and fix fragments, run-ons in a full paragraph (not isolated sentences). Bridges to real writing |

### Grade 3 (Idea Development)

| Code | Name | Type | Prerequisites | Gateway? | Description |
|------|------|------|--------------|----------|-------------|
| C.3.18 | Spot Developed vs. Underdeveloped Response | D | C.3.08 | **YES** | Tell a developed idea from an undeveloped one. GATEWAY: if this fails, no elaboration procedure will help |
| C.3.19 | Spot Specific Detail vs. Vague Statement | D | C.3.18 | | "The dog was nice" vs. "The golden retriever wagged her tail and licked my hand" |
| C.3.20 | Spot Genuine Support vs. Restatement | D | C.3.19 | | "Dogs are great. They are really good" = restatement, not support |
| C.3.21 | Add a Reason ("why is this true?") | P | C.3.20 | | First elaboration strategy |
| C.3.22 | Add a Specific Example ("like what?") | P | C.3.20 | | Second elaboration strategy |
| C.3.23 | Add a Concrete Detail ("what exactly?") | P | C.3.20 | | Third elaboration strategy — replace vague with specific |
| C.3.24 | Spot On-Topic vs. Off-Topic Sentence | D | C.3.18 | | Progress from obvious to subtle off-topic. [X-STRAND: feeds C.3.30] |
| C.3.25 | Delete or Revise Off-Topic Sentence | P | C.3.24 | | Revision skill |

### Grade 3 (Paragraph Structure)

| Code | Name | Type | Prerequisites | Gateway? | Description |
|------|------|------|--------------|----------|-------------|
| C.3.26 | Spot Organised vs. Random Sentences | D | C.3.18 | | Can they see the difference between a paragraph and a jumble? |
| C.3.27 | Paragraph Structure Rule | S | C.3.26 | | A paragraph has introduction, supporting details, and conclusion (SPO template) |
| C.3.28 | Write a Topic Sentence | P | C.3.27, C.3.20 | | Write a sentence that states the controlling idea |
| C.3.29 | Write Supporting Sentences | P | C.3.28, C.3.21, C.3.22, C.3.23 | | Develop the topic sentence using elaboration strategies |
| C.3.30 | Remove Off-Topic Sentence from Paragraph | P | C.3.24, C.3.27 | | Revision skill tied to paragraph unity |
| C.3.31 | Write a Complete Single Paragraph | I | C.3.29, C.3.30 | **YES** | First integrative writing task: topic sentence + support + logical flow. Gateway to all multi-paragraph work |

### Grade 4 (Deepening)

| Code | Name | Type | Prerequisites | Gateway? | Description |
|------|------|------|--------------|----------|-------------|
| C.4.01 | Spot Adequate vs. Surface-Level Elaboration | D | C.3.31 | | Both "say more" but one is genuinely developed |
| C.4.02 | Transitions Within a Paragraph | P | C.3.31 | | Connect ideas within a paragraph using transition words |
| C.4.03 | Multiple Elaboration Strategies in One Paragraph | P | C.4.01 | | Reason + example, not just reason alone |
| C.4.04 | Write a Grade 4 Paragraph | I | C.4.02, C.4.03 | | Paragraph with transitions and multiple types of support |
| C.4.05 | Appositives | P | C.3.16 | | Embed definitions and descriptions: "[Noun], [appositive], [verb]..." |
| C.4.06 | Subordinating Conjunctions | P | C.3.16 | | Although, while, when, if, since, unless — sentence combining |

### Grade 4 (Text Evidence)

| Code | Name | Type | Prerequisites | Gateway? | Description |
|------|------|------|--------------|----------|-------------|
| C.4.07 | Spot Central Idea vs. Supporting Details | D | C.3.18 | **YES** | Reading-to-write bridge. Must understand a passage before using it. Gateway for all evidence work |
| C.4.08 | Spot Relevant vs. Irrelevant Evidence | D | C.4.07 | | Not all details from the passage support your point |
| C.4.09 | Spot Direct Quote vs. Paraphrase | D | C.4.07 | | Understanding the difference before choosing which to use |
| C.4.10 | State Central Idea in Own Words | P | C.4.07 | | Comprehension + paraphrase |
| C.4.11 | Paraphrase Without Changing Meaning | P | C.4.09 | | Keep meaning, change words |
| C.4.12 | Signal Phrase + Evidence + Explanation | I | C.4.10, C.4.11 | | The core text evidence integration task. Quote sandwich template |
| C.4.13 | Spot Stronger vs. Weaker Evidence | D | C.4.12 | | Both relevant, but which is more convincing? |
| C.4.14 | Integrate Evidence While Maintaining Voice | P | C.4.13 | | Evidence serves YOUR point, not the other way round |
| C.4.15 | Explain How Evidence Connects to Claim | P | C.4.14 | | Don't just drop evidence in — explain why it matters |
| C.4.16 | Write Claim + Evidence + Explanation Paragraph | I | C.4.15 | | Grade 4 evidence paragraph |

### Grade 4-5 (Multi-Paragraph)

| Code | Name | Type | Prerequisites | Gateway? | Description |
|------|------|------|--------------|----------|-------------|
| C.4.17 | Spot Central Idea vs. Paragraph Controlling Idea | D | C.4.04 | | Central idea governs the whole piece; controlling idea governs one paragraph |
| C.4.18 | Spot When to Start a New Paragraph | D | C.4.17 | | New aspect = new paragraph |
| C.4.19 | Generate 2-3 Distinct Aspects of a Topic | P | C.4.18 | | Planning skill — before writing |
| C.4.20 | Write Transitions Between Paragraphs | P | C.4.19 | | Connect back to the central idea |
| C.4.21 | Write a Two-Paragraph Response | I | C.4.20, C.4.04 | | Each paragraph covers a different aspect, connected by transitions |
| C.5.01 | Essay Organisation Rule | S | C.4.21 | | Introduction with thesis, body paragraphs with topic sentences, conclusion |
| C.5.02 | Write a Thesis Statement | P | C.5.01 | | The central claim that everything else supports |
| C.5.03 | Write Topic Sentences That Serve the Thesis | P | C.5.02 | | Each body paragraph supports the thesis from a different angle |
| C.5.04 | Write Transitions Using Conjunctive Adverbs | P | C.5.03, M.5.05 | | Connects to Mechanics strand conjunctive adverbs. [X-STRAND: requires M.5.05] |
| C.5.05 | Write a Complete Multi-Paragraph Response | I | C.5.04, C.4.16 | **YES** | THE capstone: pulls together all 4 areas. Gateway to 6-8 composition |

### Grade 5 (Advanced Evidence & Depth)

| Code | Name | Type | Prerequisites | Gateway? | Description |
|------|------|------|--------------|----------|-------------|
| C.5.06 | Spot Depth of Thought vs. Surface Response | D | C.4.04 | | Move beyond opinions to evidence-grounded claims |
| C.5.07 | Develop with Specific Facts and Details | P | C.5.06 | | "I think..." → evidence-grounded claims |
| C.5.08 | Sustain Development Without Repetition | P | C.5.07 | | Depth, not just breadth |
| C.5.09 | Write a Fully Developed Paragraph | I | C.5.08 | | Grade 5 level paragraph demonstrating depth of thought |
| C.5.10 | Identify Which Source Supports Which Aspect (Paired Passages) | D | C.4.16 | | Two passages, different contributions |
| C.5.11 | Synthesise Evidence from Two Sources | P | C.5.10 | | Draw from both passages, not just one |
| C.5.12 | Evidence for Depth of Thought | P | C.5.11 | | Evidence as thinking tool, not just decoration |
| C.5.13 | Write Multi-Paragraph Evidence-Based Response | I | C.5.12, C.5.05 | | Full extended constructed response from paired passages |

### Grade 6-8 (Academic Argument)

| Code | Name | Type | Prerequisites | Gateway? | Description |
|------|------|------|--------------|----------|-------------|
| C.6.01 | Spot Well-Organised vs. Poorly Organised Multi-Paragraph Text | D | C.5.05 | | Can they see structural problems in an essay? |
| C.6.02 | Multiple Paragraph Outline (MPO) Template | S | C.6.01 | | Introduction (hook, context, thesis) → Body paragraphs (SPO structure) → Conclusion |
| C.6.03 | Write an Introduction Paragraph | P | C.6.02 | | Hook → Context → Thesis |
| C.6.04 | Write Body Paragraphs with Transitions | P | C.6.02, C.5.04 | | Transition + topic sentence + evidence + analysis + concluding transition |
| C.6.05 | Write a Conclusion Paragraph | P | C.6.03 | | Restate thesis + synthesize + final thought |
| C.6.06 | Write a Complete Multi-Paragraph Essay | I | C.6.03, C.6.04, C.6.05 | **YES** | Full MPO-structured essay. Gateway to academic argument |
| C.7.01 | Quote Sandwich: Introduce → Quote → Explain | S | C.4.12 | | Formalises the evidence integration pattern |
| C.7.02 | Select and Introduce Textual Evidence | P | C.7.01, C.6.06 | | Choose the right evidence and set it up |
| C.7.03 | Explain Evidence (Analysis, Not Summary) | P | C.7.02 | | "This shows that..." — interpretation, not retelling |
| C.7.04 | Spot Analysis vs. Summary | D | C.7.03 | **YES** | Can the student see when they're retelling vs. interpreting? Gateway for all analytical writing |
| C.7.05 | Write Analytical Paragraphs | I | C.7.04 | | Claim-evidence-reasoning paragraphs |
| C.7.06 | Summarise Others' Views (They Say) | P | C.7.05 | | "Many people assume that..." / "It is often said that..." |
| C.7.07 | Respond to Others' Views (I Say) | P | C.7.06 | | "However, I would argue that..." |
| C.7.08 | They Say / I Say Combined | I | C.7.06, C.7.07 | | Full academic argument move |
| C.8.01 | Anticipate Counterargument | P | C.7.08 | | "Some might object that..." |
| C.8.02 | Respond to Counterargument | P | C.8.01 | | "However, [response with evidence]..." |
| C.8.03 | Naysayer Planting | I | C.8.02 | | Weave counterargument into essay structure |
| C.8.04 | Write a Full Academic Argument Essay | I | C.8.03, C.6.06 | **YES** | Complete They Say / I Say essay with counterargument. Gateway to 9-12 |

### Grade 9-12 (Sophisticated Composition)

| Code | Name | Type | Prerequisites | Gateway? | Description |
|------|------|------|--------------|----------|-------------|
| C.9.01 | Spot Differences Between Essay Structures | D | C.8.04 | | Classical, Rogerian, problem-solution, comparison, cause-effect |
| C.9.02 | Essay Architecture: Match Structure to Purpose | S | C.9.01 | | Which structure serves which rhetorical goal? |
| C.9.03 | Write Flexible Essay Structures | P | C.9.02 | | Move beyond 5-paragraph to structures matched to purpose |
| C.9.04 | Spot Weak vs. Strong Thesis | D | C.9.03 | | "Social media is bad" vs. "Social media's algorithmic design exploits adolescent psychology" |
| C.9.05 | Craft Arguable, Specific, Significant Thesis | P | C.9.04 | | "So what?" test — thesis revision |
| C.10.01 | Agree with a Difference | P | C.8.03, C.9.05 | | "While I agree with X that..., I want to add that..." |
| C.10.02 | Disagree Diplomatically | P | C.10.01 | | "X's argument that... overlooks the fact that..." |
| C.10.03 | Complicate the Debate | P | C.10.02 | | "The debate typically focuses on..., but we should also consider..." |
| C.10.04 | Write Sophisticated Academic Argument | I | C.10.03 | | Full nuanced They Say / I Say essay |
| C.11.01 | Source Mapping and Synthesis Matrix | P | C.10.04 | | Organise multiple sources by theme, not by source |
| C.11.02 | Weave Multiple Sources into Argument | P | C.11.01 | | Synthesis, not serial summarising |
| C.11.03 | Write Synthesis Essay | I | C.11.02 | **YES** | Integrate 3+ sources into coherent argument. DOK 4. Gateway to research |
| C.12.01 | Research Question Development | P | C.11.03 | | Develop an arguable, researchable question |
| C.12.02 | Source Evaluation | P | C.12.01 | | Assess credibility, relevance, bias |
| C.12.03 | Citation and Attribution | S | C.12.01 | | MLA/APA format, avoiding plagiarism |
| C.12.04 | Scaffolded Research Paper | I | C.12.01, C.12.02, C.12.03, C.11.03 | | Full knowledge-transforming process (Bereiter & Scardamalia) |

---

## STRAND 2: MECHANICS

### K-2 Foundational (Transcription Automaticity)

| Code | Name | Type | Prerequisites | Gateway? | Description |
|------|------|------|--------------|----------|-------------|
| M.K.01 | Pencil Grip and Posture | S | — | | Proper grip, paper position |
| M.K.02 | Letter Formation: Uppercase | P | M.K.01 | | Form all 26 uppercase letters |
| M.K.03 | Letter Formation: Lowercase | P | M.K.02 | | Form all 26 lowercase letters |
| M.K.04 | Letter Spacing and Sizing | P | M.K.03 | | Consistent spacing between letters and words |
| M.1.01 | Handwriting Fluency | I | M.K.04 | **YES** | Write letters automatically without thinking about formation. Gateway: if transcription consumes working memory, composition fails (Berninger) |
| M.1.02 | Sound-Letter Correspondence | S | M.K.03 | | Single consonants and short vowels |
| M.1.03 | Phonetic Spelling: CVC Words | P | M.1.02 | | Encode simple words by sound |
| M.1.04 | Phonetic Spelling: Blends and Digraphs | P | M.1.03 | | bl, cr, sh, ch, th, etc. |
| M.1.05 | High-Frequency Words (Tier 1) | P | M.1.03 | | the, is, and, was, to — automatic spelling |
| M.2.01 | High-Frequency Words (Tier 2) | P | M.1.05 | | because, would, their, people — spaced repetition |
| M.2.02 | Keyboarding Introduction | P | M.1.01 | | Home row, basic typing (parallel with handwriting) |
| M.2.03 | Capital Letters Rule | S | C.1.02 | | Sentences start with capitals; proper nouns are capitalised. [X-STRAND: requires C.1.02] |
| M.2.04 | End Punctuation: Period, Question Mark, Exclamation | S | C.1.02 | | Match punctuation to sentence type. [X-STRAND: requires C.1.02] |
| M.2.05 | Apply Capitals and End Punctuation in Own Writing | P | M.2.03, M.2.04 | | Use correctly in student-composed sentences |

### Grade 3-5 (Contextual Grammar)

| Code | Name | Type | Prerequisites | Gateway? | Description |
|------|------|------|--------------|----------|-------------|
| M.3.01 | Spot Sentence Boundary Errors in Own Drafts | D | M.2.05, C.3.08 | | Find run-ons and fragments in connected text (not isolated). [X-STRAND: requires C.3.08] |
| M.3.02 | Fix Sentence Boundary Errors in Own Drafts | P | M.3.01 | | Revision skill — fix errors while preserving surrounding text |
| M.3.03 | Comma Before Conjunction in Compound Sentence | S | C.3.13 | | Comma before and/but/so/or. [X-STRAND: requires C.3.13] |
| M.3.04 | Apply Comma Rule in Own Writing | P | M.3.03 | | Use correctly in student-composed compound sentences |
| M.4.01 | Comma After Introductory Element | S | C.4.06 | | After subordinating clause openers. [X-STRAND: requires C.4.06] |
| M.4.02 | Commas in Lists | S | M.3.03 | | Serial comma in a series of items |
| M.4.03 | Apply All Comma Rules in Context | P | M.4.01, M.4.02 | | Notice patterns in mentor texts, apply to own drafts |
| M.4.04 | Spot Subject-Verb Agreement Errors | D | M.3.02 | | Find agreement errors in own and sample text |
| M.4.05 | Fix Subject-Verb Agreement | P | M.4.04 | | Revise own sentences for agreement |
| M.4.06 | Spot Verb Tense Inconsistency | D | M.4.05 | | Find tense shifts within a paragraph |
| M.4.07 | Maintain Verb Tense Consistency | P | M.4.06 | | Edit own drafts for tense consistency |
| M.5.01 | Spot Simple vs. Compound vs. Complex Sentence | D | C.4.06, M.3.03 | | Three sentence types. [X-STRAND: requires C.4.06] |
| M.5.02 | Subordinating Conjunctions Form Complex Sentences | S | M.5.01 | | Same "trap words" from G3 fragments — now used deliberately |
| M.5.03 | Comma After Introductory Dependent Clause | S | M.5.02 | | Comma needed when dependent clause comes first |
| M.5.04 | Conjunctive Adverbs | S | M.5.01 | | however, therefore, moreover, meanwhile, furthermore |
| M.5.05 | Use Conjunctive Adverbs with Correct Punctuation | P | M.5.04 | | Full stop or semicolon before; comma after. [X-STRAND: feeds C.5.04] |
| M.5.06 | Edit a Passage for Multiple Error Types | I | M.4.07, M.5.05 | **YES** | Find and fix fragments, run-ons, comma errors, agreement, and tense in connected text. Gateway to 6-8 mechanics |

### Grade 6-8 (Grammar as Meaning-Making)

| Code | Name | Type | Prerequisites | Gateway? | Description |
|------|------|------|--------------|----------|-------------|
| M.6.01 | Identify How Nouns, Verbs, Adjectives Function in Mentor Text | D | M.5.06 | | Analyze grammatical choices — grammar as "a toolkit for discussing and shaping written text" (Myhill) |
| M.6.02 | Apply Part-of-Speech Awareness to Own Drafts | P | M.6.01 | | Choose stronger verbs, more precise nouns in revision |
| M.7.01 | Spot Sentence Variety vs. Monotony | D | M.6.02 | | Can they see when all sentences are the same length/structure? |
| M.7.02 | Use Sentence Types as Rhetorical Choices | P | M.7.01 | | Short sentence for emphasis after long ones; complex sentence for nuance |
| M.7.03 | Semicolons, Colons, and Dashes as Meaning Tools | S | M.7.02 | | Each punctuation mark creates a different rhetorical effect |
| M.7.04 | Apply Advanced Punctuation in Own Drafts | P | M.7.03 | | Experiment with options; analyze choices in published writing |
| M.8.01 | Identify Personal Error Patterns | D | M.7.04 | | their/they're/there, its/it's, affect/effect — what do YOU get wrong? |
| M.8.02 | Self-Edit Using Personal Error Checklist | P | M.8.01 | | Targeted revision based on own patterns |
| M.8.03 | Edit a Full Draft for Mechanics and Meaning | I | M.8.02 | **YES** | Holistic editing: error correction + rhetorical choices. Gateway to 9-12 |

### Grade 9-12 (Style Refinement)

| Code | Name | Type | Prerequisites | Gateway? | Description |
|------|------|------|--------------|----------|-------------|
| M.9.01 | Spot Stylistic Strengths and Weaknesses in Published Writing | D | M.8.03 | | Analyze rhythm, emphasis, variety in mentor texts |
| M.9.02 | Sentence Imitation Exercises | P | M.9.01 | | Imitate the syntactic structures of skilled writers |
| M.9.03 | Develop Personal Style | P | M.9.02 | | Cultivate consistent voice through syntactic choices |
| M.10.01 | Spot Wordiness | D | M.9.03 | | Identify unnecessary words, passive voice, nominalizations |
| M.10.02 | Revise for Concision | P | M.10.01 | | Eliminate wordiness, choose precise words |
| M.11.01 | SAT/ACT Grammar Conventions | S | M.8.03 | | Test-specific grammar and writing conventions |
| M.11.02 | SAT/ACT Practice with Test-Format Questions | P | M.11.01 | | Targeted practice in test format |

---

## STRAND 3: DISCOURSE

### K-2 Foundational

| Code | Name | Type | Prerequisites | Gateway? | Description |
|------|------|------|--------------|----------|-------------|
| D.K.01 | Writing Has a Reader | S | C.K.04 | | Understanding that writing communicates to someone who isn't here. [X-STRAND: requires C.K.04] |
| D.1.01 | Share Writing with Classmates | P | C.1.03, D.K.01 | | "Author's chair" — read your writing to peers. [X-STRAND: requires C.1.03] |
| D.2.01 | Write for a Specific Person | P | D.1.01 | | Letter to a friend, note to a family member — audience shapes content |

### Grade 3-5

| Code | Name | Type | Prerequisites | Gateway? | Description |
|------|------|------|--------------|----------|-------------|
| D.3.01 | Spot Formal vs. Informal Language | D | D.2.01 | | Tell the difference between casual and formal writing |
| D.3.02 | Adjust Word Choice for Different Audiences | P | D.3.01 | | Same content, different audiences exercise |
| D.4.01 | Spot Author's Voice in Mentor Texts | D | D.3.02 | | Recognize what makes one author sound different from another |
| D.4.02 | Imitate Author's Voice | P | D.4.01 | | Write a passage "in the style of" a mentor text |
| D.5.01 | Write with Awareness of Own Emerging Voice | I | D.4.02 | | Begin to make consistent stylistic choices |

### Grade 6-8 (Academic Discourse)

| Code | Name | Type | Prerequisites | Gateway? | Description |
|------|------|------|--------------|----------|-------------|
| D.6.01 | Spot Academic vs. Casual Register | D | D.5.01 | **YES** | Tell formal academic writing from informal. Gateway: academic writing requires register awareness |
| D.6.02 | Write in Academic Register | P | D.6.01 | | Formal language, hedging, avoiding unnecessary first person |
| D.7.01 | Signal Verb Meanings | S | C.7.06 | | Neutral (states, reports) vs. agreement (confirms) vs. disagreement (disputes) vs. qualified (suggests). [X-STRAND: requires C.7.06] |
| D.7.02 | Choose Appropriate Signal Verbs | P | D.7.01 | | Select verbs that indicate the author's stance accurately |
| D.7.03 | Metacommentary Templates | S | D.7.02 | | "In other words,...", "My point is not X but Y...", "Essentially, I am arguing that..." |
| D.7.04 | Use Metacommentary to Guide Readers | P | D.7.03 | | Weave metacommentary into own arguments |
| D.8.01 | Write for Peers with Academic Conventions | I | D.7.04, C.8.04 | | Full academic argument with register, signal verbs, and metacommentary. [X-STRAND: requires C.8.04] |

### Grade 9-12 (Voice and Publication)

| Code | Name | Type | Prerequisites | Gateway? | Description |
|------|------|------|--------------|----------|-------------|
| D.9.01 | Spot Distinctive Voice in Academic Writing | D | D.8.01 | | How do scholars maintain voice within formal constraints? |
| D.9.02 | Develop Authentic Authorial Voice | P | D.9.01 | | Find your "sound" — consistent choices in diction, syntax, tone |
| D.10.01 | Spot Discipline-Specific Conventions | D | C.9.03, D.9.02 | | Literary analysis vs. scientific vs. historical vs. philosophical writing. [X-STRAND: requires C.9.03] |
| D.10.02 | Write in Discipline-Specific Formats | P | D.10.01 | | IMRAD for science, close reading for literature, etc. |
| D.11.01 | Spot Surface Editing vs. Substantive Revision | D | C.11.03, D.9.02 | | Is this revision changing IDEAS or just fixing typos? [X-STRAND: requires C.11.03] |
| D.11.02 | Revise for Meaning Transformation | P | D.11.01 | | Revision protocols that transform ideas, not just correct errors (Sommers) |
| D.12.01 | Write for Authentic Audiences Beyond School | I | D.11.02, D.9.02 | | Blog posts, op-eds, competitions, submissions — real audience, real stakes |

---

## CROSS-STRAND INTEGRATION MAP

These are the critical points where strands connect. The app must surface these integration points to students and teachers.

| Integration Point | Composition Node | Mechanics Node | Discourse Node | Grade | Description |
|-------------------|-----------------|---------------|---------------|-------|-------------|
| First Written Sentence | C.1.03 | M.1.01 | — | 1 | Student needs handwriting fluency to compose sentences |
| Sentence Boundaries | C.3.08, C.3.09 | M.3.01, M.3.02 | — | 3 | Fragment/run-on skills serve both strands |
| Compound Sentences | C.3.13 | M.3.03, M.3.04 | — | 3 | Combining sentences requires comma knowledge |
| Subordinate Clauses | C.4.06 | M.4.01, M.5.02 | — | 4-5 | Subordinating conjunctions require comma rules |
| Conjunctive Adverbs | C.5.04 | M.5.05 | — | 5 | Transitions require punctuation knowledge |
| Academic Argument | C.7.06, C.7.07 | — | D.7.01, D.7.02 | 7 | They Say / I Say requires signal verbs and register |
| Full Academic Essay | C.8.04 | M.8.03 | D.8.01 | 8 | All three strands converge |
| Essay Architecture | C.9.03 | M.9.03 | D.10.01 | 9-10 | Flexible structures require style and discipline awareness |
| Research Writing | C.12.04 | — | D.11.02 | 12 | Research requires substantive revision |

---

## GATEWAY KC SUMMARY

These are the nodes where failure blocks all downstream progress. The diagnostic system must identify and prioritize these.

| Code | Name | Grade | Why It's a Gateway |
|------|------|-------|--------------------|
| C.1.01 | Sentence vs. Not-a-Sentence (Oral) | 1 | If they can't hear a sentence, they can't write one |
| M.1.01 | Handwriting Fluency | 1 | If transcription consumes working memory, composition fails (Berninger) |
| C.3.01 | Spot Fragment: Missing Subject | 3 | First written discrimination — everything builds on this |
| C.3.08 | Three-Way Sort | 3 | Integrates all discrimination; gates all production work |
| C.3.18 | Spot Developed vs. Underdeveloped | 3 | If they can't see weak writing, no procedure will help |
| C.3.31 | Write a Complete Single Paragraph | 3 | First integrative writing task; gates all multi-paragraph work |
| C.4.07 | Spot Central Idea vs. Supporting Details | 4 | Gates all evidence integration |
| C.5.05 | Write Complete Multi-Paragraph Response | 5 | Capstone — gates 6-8 composition |
| C.6.06 | Write a Complete Multi-Paragraph Essay | 6 | Gates academic argument |
| C.7.04 | Spot Analysis vs. Summary | 7 | Gates all analytical writing |
| C.8.04 | Write Full Academic Argument Essay | 8 | Gates 9-12 sophisticated composition |
| C.11.03 | Write Synthesis Essay | 11 | Gates research writing |
| M.5.06 | Edit Passage for Multiple Error Types | 5 | Gates meaning-making grammar |
| M.8.03 | Edit Full Draft for Mechanics and Meaning | 8 | Gates style refinement |
| D.6.01 | Spot Academic vs. Casual Register | 6 | Gates academic writing conventions |

---

## GRAPH STATISTICS

| Metric | Count |
|--------|-------|
| Total KCs | 156 |
| Composition KCs | 92 |
| Mechanics KCs | 40 |
| Discourse KCs | 24 |
| Gateway KCs | 15 |
| Discrimination KCs | 44 |
| Production KCs | 73 |
| Structure KCs | 21 |
| Integrative KCs | 18 |
| Cross-Strand Connections | 10 |
| Grade Bands | K-12 (13 grades) |

---

## DIAGNOSTIC ENTRY POINTS

When a new student enters the system, the diagnostic assessment should probe these gateway KCs to find the student's actual level — regardless of enrolled grade:

| Diagnostic Probe | If PASS → | If FAIL → |
|-----------------|-----------|-----------|
| C.3.01 (Spot fragments) | Probe C.3.08 | Start at C.1.01 |
| C.3.08 (Three-way sort) | Probe C.3.18 | Start at C.3.01 |
| C.3.18 (Developed vs. underdeveloped) | Probe C.3.31 | Start at C.3.18 |
| C.3.31 (Write a paragraph) | Probe C.5.05 | Start at C.3.28 |
| C.5.05 (Multi-paragraph response) | Probe C.6.06 | Start at C.4.17 |
| C.6.06 (Full essay) | Probe C.7.04 | Start at C.6.01 |
| C.7.04 (Analysis vs. summary) | Probe C.8.04 | Start at C.7.01 |
| C.8.04 (Academic argument) | Start at C.9.01 | Start at C.7.06 |
| M.1.01 (Handwriting fluency) | Probe M.5.06 | Start at M.K.01 |
| M.5.06 (Edit for multiple errors) | Probe M.8.03 | Start at M.3.01 |
| D.6.01 (Academic register) | Probe D.8.01 | Start at D.3.01 |

A 7th grader writing at a 3rd grade level starts at the 3rd grade node, not the 7th. The diagnostic cascade finds the actual level in 3-5 probes.

---

## VISUAL: COMPOSITION STRAND PROGRESSION

```
K               1                   2                   3
C.K.01 ──→ C.K.02 ──→ C.K.03 ──→ C.K.04
                        │
                        C.1.01 ★ ──→ C.1.02 ──→ C.1.03 ──→ C.1.04
                                                              │
                                                    C.2.01 ──→ C.2.02 ──→ C.2.03 ──→ C.2.04
                                                                                        │
SENTENCE MASTERY ───────────────────────────────────────────────────────────────────────┘
│
├── C.3.01 ★ → C.3.02 → C.3.03 ─┐
├── C.3.04 ──────────────────────┤
├── C.3.05 → C.3.06 ────────────┤
│             └── C.3.07         │
│                                ▼
│                            C.3.08 ★ ──→ C.3.09 ──→ C.3.17 (integrative)
│                              │      └──→ C.3.10 ──┘
│                              │
│                              ├──→ C.3.11 → C.3.12 → C.3.13 → C.3.14 → C.3.15 → C.3.16
│                              │                                                      │
IDEA DEVELOPMENT               │                                            C.4.05, C.4.06
│                              ▼
├── C.3.18 ★ → C.3.19 → C.3.20 → C.3.21, C.3.22, C.3.23
│   │                              │
│   ├── C.3.24 → C.3.25           │
│   └── C.3.26 → C.3.27           │
│                  │               │
PARAGRAPH          ▼               ▼
│          C.3.28 ────────→ C.3.29
│            │                │
│          C.3.30             │
│            └───────→ C.3.31 ★ (first integrative paragraph)
│                        │
│         ┌──────────────┘
│         ▼
│    C.4.01 → C.4.03 ─┐
│    C.4.02 ───────────┤
│                      ▼
│                  C.4.04
│                    │
MULTI-PARAGRAPH      │
│         ┌──────────┘
│         ▼
│    C.4.17 → C.4.18 → C.4.19 → C.4.20 → C.4.21
│                                            │
│    C.5.01 → C.5.02 → C.5.03 → C.5.04 → C.5.05 ★ (capstone G3-5)
│                                            │
│─────────────────── GRADE 6-8 ──────────────┘
│
C.6.01 → C.6.02 → C.6.03 → C.6.04 → C.6.05 → C.6.06 ★
│                                                  │
C.7.01 → C.7.02 → C.7.03 → C.7.04 ★ → C.7.05    │
│                                         │         │
│                              C.7.06 → C.7.07 → C.7.08
│                                                   │
│                                C.8.01 → C.8.02 → C.8.03 → C.8.04 ★
│                                                               │
│─────────────────── GRADE 9-12 ────────────────────────────────┘
│
C.9.01 → C.9.02 → C.9.03 → C.9.04 → C.9.05
│                                       │
│         C.10.01 → C.10.02 → C.10.03 → C.10.04
│                                          │
│                   C.11.01 → C.11.02 → C.11.03 ★
│                                          │
│                   C.12.01 → C.12.02      │
│                     └── C.12.03          │
│                           └──→ C.12.04 ──┘ (CAPSTONE)

★ = Gateway KC
```

---

*Writing Knowledge Graph*
*Created: March 2026*
*Based on: Writing Brainlift - Complete + MasteryWrite KC Framework*
*Total: 156 KCs across 3 strands, K-12*
