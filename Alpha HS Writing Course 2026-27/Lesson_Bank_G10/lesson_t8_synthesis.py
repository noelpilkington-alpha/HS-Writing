"""
lesson_t8_synthesis.py  -  G10 model lesson, TYPE 8: CROSS-SOURCE SYNTHESIS.

RECRAFTED to the 17-gate DI bar (T1 precedent). Assembles a Timeback assessment-test (ordered item
sequence) that instantiates the council-adjudicated Type-8 shell against the REAL G10 banks. The move:
combine 2+ sources into ONE argument, tracking which idea comes from which source, engineering genuine
combination rather than two summaries placed side by side. This is the direct foundation for G11 AP
synthesis. Binds ONLY LESSON-pool stimuli (no test-pool item is reused as instruction):
  - stimulus  ACC-W910-ARG-OPP-LESSON-SCHOOLYEAR (longer school year = 2 passages in one) -> the source read
  - the INDEPENDENT synthesis essay is AUTHORED inline (ref="") on the school-year sources -> no CR item reuse
  - stimulus  ACC-W910-ARG-OPP-LESSON-DST (daylight saving, opposing pair)                 -> partitioned transfer

Four DI defects fixed to clear the gates (same moves T1 used):
  1. define_before_use: TEACH defines "synthesis", "attributive tag", "controlling idea/claim", and the
     "because/but/so hinge" in plain words WITH a definitional cue BEFORE any student-facing use.
  2. content_depth: every teach/model/production body carries finished student-facing content; the
     annotated before/after writes out BOTH a summary-plus-summary BEFORE and a woven AFTER inline.
  3. model_before_required: the diagnosis is MODELED on a flawed draft first (checklist run step by step),
     THEN the student runs the same four-step checklist on their own synthesis. No blank "diagnose it."
  4. no_ambiguous_reference: four named objects kept distinct (Source A, Source B, the shared thread, your
     controlling claim); every choice item embeds its options (A)-(D) and states "Correct: X." inline.

SRSD shell (Teach/Model/Supported/Independent/Transfer). Model = the 4-mechanism async sequence (clean
annotated before/after -> predict-the-fix -> feedback on the student's OWN draft [the FRQ grader] ->
student-generated diagnosis). Mnemonic WEAVE (proposal): Which source says what, Establish the shared
thread, Attribute each idea to its source, Voice your own claim across them, Explain how they combine.
Source-count staging is enforced by content: single-source integration is assumed fluent (Type 3) before
the 2nd source is introduced; staging runs single -> complementary -> opposing (opposing is hardest:
synthesize, weigh, pick). Bank-partitioned transfer (longer school year -> daylight saving). All slots
map to native Timeback interactions.

Runs the QC harness on execution and prints PASS/FAIL. Dependency-free (stdlib + lesson_contract).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report

LESSON = Lesson(
    id="ACC-W910-L-T8-SYNTHESIS-0001", grade="9-10", lesson_type=8,
    unit="G10 U3 - Cross-source synthesis (combine two sources into one argument)",
    title="Weave the Sources: One Argument, Not Two Summaries (WEAVE)",
    target=("Combine two sources into ONE argument, tracking which idea comes from which source and joining "
            "them on a shared thread instead of reporting them in sequence. Attribute each idea to its "
            "source, voice your own claim across both, and explain how they combine. Traits: "
            "Evidence/Development and Organization."),
    acc_tags=["ACC.W.SRC.1", "ACC.W.ARG.2", "ACC.W.ARG.3", "CCSS.W.9-10.1"],
    provenance={"copyright": "own_authored", "authored": "2026-07-07",
                "mnemonic_status": "proposal",
                "council": "TSIS they-say-across-sources + weigh-and-pick; KH source-count staging; "
                           "TWR sentence-combining fuses cross-source evidence; SRSD shell; W&H boundary-pair "
                           "calibration; DI summary-vs-synthesis minimal pairs"},
    fade_ledger_moves=["attribute-each-idea", "shared-thread", "because/but/so", "weigh-and-pick"],
    slots=[
        # ---------------- TEACH: define every term, then the WEAVE cue, then the read ----------------
        Slot("TEACH", "teach_card", "What synthesis is (one argument, not two summaries) + four things to track",
             body=("Synthesis means combining two or more sources into ONE argument that YOU build, instead "
                   "of reporting each source on its own. You already know how to integrate a single source so "
                   "that no quote stands alone; synthesis is the next step up. The trap is writing one "
                   "paragraph that reports Source A, then a separate paragraph that reports Source B, and "
                   "calling that synthesis. That is two summaries sitting side by side: the two ideas never "
                   "touch, and you never say what YOU conclude from holding them together. Real synthesis "
                   "puts both sources to work on one shared thread and tracks which idea came from which "
                   "source the whole way. Keep four things straight, and give each its own name: (1) Source A "
                   "is the first passage you read; (2) Source B is the second passage; (3) the shared thread "
                   "is the one topic both sources circle, even when they land on opposite conclusions; (4) "
                   "your controlling idea is a single claim that your whole argument is built around, the one "
                   "position everything else supports (some teachers call this your controlling claim). To "
                   "keep credit clear, attribute every idea. An attributive tag is a short phrase that names "
                   "who said something, such as 'According to Source A' or 'Source B argues.' Never blur "
                   "which source said what.")),
        Slot("TEACH", "teach_card", "The WEAVE strategy + the because/but/so hinge",
             body=("WEAVE is how you build one argument from two sources. Each letter has one job. W = Which "
                   "source says what: map the one usable idea in EACH source before you write, so you know "
                   "your raw material. E = Establish the shared thread: name the one point where the two "
                   "sources meet, the topic both circle even if they disagree about the answer. A = Attribute "
                   "each idea to its source: put an attributive tag on every idea ('According to Source A,' "
                   "'Source B counters') so the reader always knows who said what. V = Voice your own claim "
                   "across them: state your controlling idea, the one position that USES both sources rather "
                   "than repeating either. E = Explain how they combine: show WHY the two ideas together "
                   "support your claim, not just that they both exist. The join often runs on a because/but/so "
                   "hinge. A because/but/so hinge is a small connecting word (because, but, or so) that links "
                   "two ideas into one sentence: 'because' gives a reason, 'but' turns to a tension, 'so' "
                   "draws a conclusion. We build synthesis in stages: first a single source, then two sources "
                   "that AGREE (complementary), then two that DISAGREE (opposing). Opposing is the hardest, "
                   "because there you must synthesize, weigh the two sides, and pick. Goal for today: write "
                   "one argument that genuinely joins two sources, with every idea attributed to its source.")),
        Slot("TEACH", "stimulus_display", "Read the paired source on a longer school year",
             ref="ACC-W910-ARG-OPP-LESSON-SCHOOLYEAR", bank="longer_school_year",
             body=("This stimulus is really two sources in one: a pro passage arguing FOR a longer school "
                   "year (call it Source A) and a con passage arguing AGAINST it (Source B), both on the same "
                   "question, whether the United States should adopt a longer school year. Read both. As you "
                   "read, note one usable idea from EACH source, and keep track of which source each idea came "
                   "from. Then look for the shared thread: what topic do both passages circle, even though "
                   "they land on opposite conclusions?")),

        # ---------------- MODEL: 4-mechanism async sequence ----------------
        Slot("MODEL", "annotated_before_after", "Watch two summaries become one woven argument",
             bank="longer_school_year",
             body=("BEFORE (two summaries side by side, never joined): "
                   "Paragraph 1: The first source argues for a longer school year. It reports that a typical "
                   "American public school runs about 180 days (NCES) and that a long summer break lets "
                   "learning slide, hitting low-income students hardest. So a longer year would narrow the "
                   "gap. "
                   "Paragraph 2: The second source argues against it. It reports that more time in a seat is "
                   "not the same as more learning and that running schools longer costs real money, since "
                   "teachers are salaried and must be paid for the added weeks (BLS). So a longer year is not "
                   "worth the price. "
                   "(Notice: each paragraph reports ONE source and stops. The two ideas never touch. That is "
                   "summary plus summary, not synthesis.) "
                   "AFTER (one argument across both, annotated): "
                   "Both passages actually agree on one fact, that the summer slide is real and falls hardest "
                   "on low-income students, yet they split on whether adding days is the right cure "
                   "[Establish the shared thread: the summer-slide gap set against the cost of the cure]. "
                   "The pro source points to the summer slide to argue that more days would keep vulnerable "
                   "students from losing ground (Source A) [Attribute to Source A], but the con source "
                   "counters that seat time is not learning and that stretched districts might add days "
                   "without adding pay, burning out the teachers schools cannot lose (Source B) [Attribute to "
                   "Source B]. "
                   "Read together, the honest question is not whether the summer slide matters, which both "
                   "sources grant, but whether a longer calendar or a targeted summer program is the wiser "
                   "way to spend the same money [Voice your own claim across both + Explain how they "
                   "combine]. "
                   "(Notice the AFTER version names a shared thread, cites BOTH sources on it, keeps each "
                   "idea tagged to its source, and lands one claim that needed both. That is WEAVE.)")),
        Slot("MODEL", "predict_the_fix", "Predict the fix before you see it",
             bank="longer_school_year",
             body=("Diagnose this draft before we reveal the fix. A student wrote: 'Source A says a longer "
                   "school year would reduce the summer slide. Source B says a longer school year costs money "
                   "and does not guarantee better teaching. Both are important points about the school "
                   "calendar.' It reports both sources correctly, so what is still missing? Which single move "
                   "would most turn it into synthesis? "
                   "(A) name the shared thread the two sources meet on and state one claim that uses both  "
                   "(B) add a third source  "
                   "(C) add more statistics from Source A  "
                   "(D) put Source B before Source A"),
             feedback=("The strongest fix is A. The draft is two summaries reported in sequence: it tells us "
                       "what each source says but never JOINS them. Nothing states where the two ideas "
                       "connect or what YOU conclude from holding them together. The fix is to name the "
                       "shared thread (both sources are really arguing about how best to spend the same money "
                       "to close the summer-slide gap) and then voice one claim that needs both sources, "
                       "keeping each idea attributed. A third source or more statistics only stacks more "
                       "summary; reordering the sources changes nothing about whether they are joined.")),

        # ---------------- SUPPORTED: discrimination (Grade-C, labeled) then guided production ----------------
        Slot("SUPPORTED", "discrimination", "Synthesis vs. summary-plus-summary (minimal pair, mastery gate)",
             ref="", labeled_grade_c=True, bank="longer_school_year",
             body=("Discriminate before you produce (a labeled Grade-C step). Every option below uses the "
                   "same two school-year facts and is correct about each source. Which one SYNTHESIZES, that "
                   "is, joins the sources on a shared thread and lands one controlling claim that needs both, "
                   "rather than reporting them in sequence? "
                   "(A) 'Source A reports that a long summer break lets low-income students slide backward, "
                   "so a longer year would help. Source B reports that running schools longer costs real "
                   "money and does not guarantee better teaching. Both are facts about the school calendar.'  "
                   "(B) 'Source A shows the summer slide falls hardest on students who cannot afford "
                   "enrichment, but Source B shows that adding costly days does not make the teaching inside "
                   "them better, so the fairer fix may be a targeted summer program rather than a longer year "
                   "for everyone.'  "
                   "(C) 'Source A argues for a longer school year. First it says the summer slide is real. "
                   "Then it says a longer year would narrow the gap. It gives several reasons for this view.'  "
                   "(D) 'Source B argues against a longer school year because it costs money and teachers "
                   "are salaried. Source A disagrees. The two sources take opposite sides of the question.' "
                   "Correct: B. Only B names the shared thread (closing the summer-slide gap set against the "
                   "cost of the cure), attributes each idea, and voices one claim that needs BOTH sources on a "
                   "but/so hinge. A lists two facts and stops (summary plus summary). C summarizes only Source "
                   "A. D reports that the sources disagree but never joins their ideas or states what YOU "
                   "conclude.")),
        Slot("SUPPORTED", "production_frq", "Combine two given facts into one attributed claim (claim provided)",
             bank="longer_school_year", rubric_ref="rc.ohio", scored=True, unit="sentence",
             body=("Scaffolded synthesis. The CLAIM is given to you: 'The United States should fix the summer "
                   "slide with targeted summer programs rather than a longer year for everyone.' You are "
                   "given one fact from EACH source: "
                   "from Source A, the summer slide lets low-income students lose ground while wealthier peers "
                   "keep learning; "
                   "from Source B, running schools longer costs real money because teachers are salaried and "
                   "would have to be paid for the added weeks. "
                   "Write TWO to THREE sentences that support the given claim by JOINING both facts on a "
                   "shared thread. You must (1) attribute each fact to its source (name Source A and Source "
                   "B, do not blur them), (2) use a because/but/so hinge to connect the gap to the cost of "
                   "the cure, and (3) make the reader see why the two facts together support a targeted "
                   "program. Do not write one sentence on Source A and a separate sentence on Source B: weave "
                   "them.")),
        Slot("MODEL", "diagnosis_frq", "Diagnose a draft with the WEAVE self-check (modeled, then you)",
             bank="longer_school_year", scored=True,
             body=("First watch the self-check run on a flawed draft, then run the same check yourself. "
                   "Flawed draft: 'Source A says a longer school year would reduce the summer slide. Source B "
                   "says a longer year costs money and does not guarantee better teaching. Both make good "
                   "points about the school calendar.' Run the four-step WEAVE self-check, step by step. "
                   "Step 1 (Attribute): does each idea name its source? Yes, it names Source A and Source B, "
                   "so attribution is met. Step 2 (Establish the shared thread): does it name the one point "
                   "where the sources meet? No, it never says they are both really arguing about how to spend "
                   "the same money to close the gap; repair frame: 'Both sources are really arguing about "
                   "____.'. Step 3 (Voice your claim): does one controlling claim use BOTH sources? No, it "
                   "just lists them; repair frame: 'Holding both sources together, I conclude that ____.'. "
                   "Step 4 (Explain how they combine): does a because/but/so hinge show WHY the two ideas "
                   "together support the claim? No; repair frame: 'The gap matters, but the cost matters too, "
                   "so ____.'. That draft is a summary-plus-summary: it passed Attribute but failed E, V, and "
                   "E. Now you: in two or three sentences, run the same four-step check on your OWN synthesis. "
                   "Name which WEAVE letters you actually hit, name the one you most need to repair, and write "
                   "one repair sentence using a frame above.")),

        # ---------------- INDEPENDENT: paragraph rung, THEN the full synthesis-then-pick essay ----------
        Slot("INDEPENDENT", "production_frq", "Write ONE synthesis paragraph from both sources (the paragraph rung)",
             ref="", bank="longer_school_year", rubric_ref="rc.ohio", scored=True, unit="paragraph",
             body=("Before the whole essay, build ONE synthesis paragraph, no scaffold this time. Using BOTH "
                   "school-year sources, write a single paragraph that makes one claim and supports it by "
                   "joining a fact from Source A and a fact from Source B on a shared thread. Name which source "
                   "each fact comes from (do not blur them), connect the two facts so the reader sees why they "
                   "point to your claim together, and do not write one sentence on A and a separate sentence "
                   "on B. This is the sentences-to-paragraph step: you combined two given facts a moment ago, "
                   "now build a full synthesized paragraph before you build a whole essay of them. Product "
                   "goal: one paragraph, one claim, a fact from each source attributed, and a shared thread "
                   "that joins them. Scored on Evidence/Development and Organization.")),
        Slot("INDEPENDENT", "production_frq", "Synthesize then pick: full school-year essay (authored)",
             ref="", bank="longer_school_year", rubric_ref="rc.ohio", scored=True, unit="essay",
             body=("Independent performance (opposing sources, the hardest stage: synthesize, weigh, pick). "
                   "Weighing BOTH school-year passages you read at the start of the lesson, write an "
                   "argumentative essay stating your position on whether the United States should adopt a "
                   "longer school year. Support your claim with specific evidence from BOTH sources, keep "
                   "every idea attributed to the source it came from, address at least one objection from the "
                   "side you argue against, and make clear what is at stake for students and schools. Your "
                   "job is not to report each source in turn but to build ONE argument that uses both. Scored "
                   "on Evidence/Development and Organization.")),

        # ---------------- TRANSFER: same synthesis move, partitioned NEW paired topic ----------------------
        Slot("TRANSFER", "production_frq", "Synthesize on a NEW paired topic (bank-partitioned)",
             ref="ACC-W910-ARG-OPP-LESSON-DST", bank="daylight_saving", rubric_ref="rc.ohio", scored=True, unit="essay",
             body=("Transfer to a paired source set you have not practiced on. Read the two opposing passages "
                   "on whether the United States should abolish daylight saving time and keep one clock year "
                   "round. Do the same WEAVE move: find the shared thread both sources circle, cite specific "
                   "evidence from BOTH, attribute each idea to its source, then voice one position that "
                   "weighs the two sides and picks. Address at least one objection from the side you argue "
                   "against. Do not write a paragraph on one source and a separate paragraph on the other. "
                   "Scored on Evidence/Development and Organization.")),
    ],
)

LESSONS = [LESSON]

if __name__ == "__main__":
    ok = True
    for L in LESSONS:
        qc_lesson(L)
        print(qc_report(L)); print()
        ok = ok and L.qc["passed"]
    passed = sum(1 for L in LESSONS if L.qc["passed"])
    print(f"{passed}/{len(LESSONS)} PASS")
    sys.exit(0 if ok else 1)
