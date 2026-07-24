"""
sentence_probes.py  -  a small SENTENCE probe set for the native-vs-Render comparison.

No real scored sentence corpus exists (the lowest real grain on disk is the sliced MCAS body paragraph), so
this is a construct-validity probe set: hand-authored sentence responses spanning the behaviors the sentence
scorers must discriminate, with a PREDICTED band (not an official score). Used to check that native and Render
AGREE on the discrimination (and both floor the traps), not to measure absolute accuracy.

Each probe: prompt (the task), response (the student sentence), expect (predicted /3 for writing or /2 for
revision), why. WRITING = Answer 0-2 + Conv 0-1 (/3). REVISION = Skill 0-1 + Conv 0-1 (/2).
"""

PASSAGE = ("Some schools have started the day later, at 9 a.m. instead of 8 a.m. Supporters say teens are "
           "biologically wired to sleep later and that more sleep improves focus and mood. Critics worry "
           "about bus schedules and after-school activities running late.")

WRITING_PROMPT = ("Should schools start the day later? Answer in ONE sentence: take a side and give one reason.")

WRITING_PROBES = [
    {"response": "Schools should start later because more sleep helps teens focus and stay in a better mood during class.",
     "expect": (3, 3), "why": "clear side + real reason (focus/mood) in one sentence -> Answer 2 + Conv 1"},
    {"response": "Schools should start later because it is a good idea that would be better for everyone.",
     "expect": (1, 2), "why": "side taken but reason is circular/vague ('good idea','better') -> Answer 1"},
    {"response": "Schools should start later because of teens.",
     "expect": (1, 2), "why": "'because of' + noun, relationship unexplained -> Answer 1 (underdeveloped)"},
    {"response": "Schools should start later. This is because teens need more sleep to focus.",
     "expect": (1, 2), "why": "two sentences; first has no reason -> grade sentence 1 only -> Answer 1"},
    {"response": "i think its fine i dont really care about school times",
     "expect": (0, 1), "why": "no real side/reason, off the specific question, conv weak -> low"},
    {"response": "asdf asdf asdf",
     "expect": (0, 0), "why": "gibberish gate -> 0"},
    {"response": "Pizza is my favorite food and I like to eat it on Fridays with my friends.",
     "expect": (0, 1), "why": "off-topic -> Answer 0 (conv may be 1)"},
    {"response": "Schools should keep the early start because after-school jobs and sports need the daylight hours afterward.",
     "expect": (3, 3), "why": "opposite side, still a real reason (daylight for jobs/sports) -> Answer 2 + Conv 1"},
]

REVISION_PROMPT = ("Rewrite this sentence as a question: 'The school day should start later.'")

REVISION_PROBES = [
    {"response": "Should the school day start later?",
     "expect": (2, 2), "why": "structural transform correct (is a question), clean -> Skill 1 + Conv 1"},
    {"response": "The school day should start later.",
     "expect": (0, 1), "why": "not transformed (still a statement) -> Skill 0; conv clean -> Conv 1"},
    {"response": "should the school day start later",
     "expect": (1, 2), "why": "is a question (skill met) but no capital/?, conv slips -> Skill 1, Conv 0-1"},
    {"response": "Do you think that maybe the school day should perhaps start later or not?",
     "expect": (2, 2), "why": "is a question, meaning preserved; wordy but not a skill/clarity failure -> 2"},
    {"response": "why school",
     "expect": (0, 1), "why": "fragment, not a real transformation of the sentence -> Skill 0"},
]
