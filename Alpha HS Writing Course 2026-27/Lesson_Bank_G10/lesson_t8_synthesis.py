"""
lesson_t8_synthesis.py  -  G10 model lesson, TYPE 8: CROSS-SOURCE SYNTHESIS.

Assembles a Timeback assessment-test (ordered item sequence) that instantiates the council-adjudicated
Type-8 shell (G10_Model_Lesson_Specs.md) against the REAL G10 banks. The move: combine 2+ sources into
ONE argument, tracking which idea comes from which source, engineering genuine combination rather than
two summaries placed side by side. This is the direct foundation for G11 AP synthesis. Binds ONLY
LESSON-pool stimuli (no test-pool item is reused as instruction):
  - stimulus  ACC-W910-ARG-OPP-LESSON-SCHOOLYEAR (longer school year = 2 passages in one) -> the source read
  - the INDEPENDENT synthesis essay is AUTHORED inline (ref="") on the school-year sources -> no CR item reuse
  - stimulus  ACC-W910-ARG-OPP-LESSON-DST (daylight saving, opposing pair)                 -> partitioned transfer

SRSD shell (Teach/Model/Supported/Independent/Transfer). Model = the modality-corrected 4-mechanism async
sequence (clean annotated before/after -> predict-the-fix -> feedback on the student's OWN draft [the FRQ
grader] -> student-generated diagnosis). Mnemonic WEAVE (proposal): Which source says what, Establish the
shared thread, Attribute each idea to its source, Voice your own claim across them, Explain how they
combine. Source-count staging is enforced by content: single-source integration is assumed fluent (Type 3)
before the 2nd source is introduced; staging runs single -> complementary -> opposing (opposing is hardest:
synthesize, weigh, pick). Bank-partitioned transfer (longer school year -> daylight saving). All slots map
to native Timeback interactions.

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
        # ---------------- TEACH: background + discuss + test-demand orientation ----------------
        Slot("TEACH", "teach_card", "What synthesis is + the WEAVE cue",
             body=("You already know how to integrate ONE source so no quote stands alone. Synthesis is the "
                   "next step up: you combine TWO (later more) sources into a SINGLE argument. The trap is "
                   "writing a paragraph that reports Source A, then a separate paragraph that reports Source "
                   "B, and calling that synthesis. That is two summaries sitting side by side. They were "
                   "never joined. Real synthesis puts both sources to work on ONE shared thread and tracks "
                   "which idea came from which source the whole way. Our cue is WEAVE: Which source says "
                   "what (map both), Establish the shared thread (the point where they meet), Attribute each "
                   "idea to its source (never blur who said what), Voice your own claim across them (your "
                   "position uses both), Explain how they combine. We build this in stages: first a single "
                   "source, then two sources that agree (complementary), then two that disagree (opposing). "
                   "Opposing is the hardest, because there you synthesize, weigh the two sides, and pick. "
                   "Goal for today: write one argument that genuinely joins two sources, with every idea "
                   "attributed to the source it came from.")),
        Slot("TEACH", "stimulus_display", "Read the paired source on a longer school year",
             ref="ACC-W910-ARG-OPP-LESSON-SCHOOLYEAR", bank="longer_school_year",
             body=("This stimulus is really two sources in one: a pro passage arguing for a longer school "
                   "year and a con passage arguing against it, on the same question, whether the United "
                   "States should adopt a longer school year. Read both. As you read, note one usable idea "
                   "from EACH source and, next to each, write which source it came from. Then look for the "
                   "shared thread: what topic do both passages circle, even though they land on opposite "
                   "conclusions?")),

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
        Slot("SUPPORTED", "discrimination", "Synthesis vs. summary-plus-summary (minimal pair)",
             ref="", labeled_grade_c=True, bank="longer_school_year",
             body=("Design-bet step (discriminate before you produce): both responses below use the same two "
                   "school-year facts and are equally correct about each source. Pick the one that "
                   "SYNTHESIZES (joins the sources on a shared thread and lands one claim) rather than "
                   "summarizing them in sequence. "
                   "Option 1 (summary plus summary): 'Source A reports that a long summer break lets "
                   "low-income students slide backward, so a longer year would help. Source B reports that "
                   "running schools longer costs real money and does not guarantee better teaching. Both are "
                   "facts about the school calendar.' "
                   "Option 2 (synthesis): 'Source A shows the summer slide falls hardest on students who "
                   "cannot afford enrichment, but Source B shows that simply adding costly days does not make "
                   "the teaching inside them better, which is why the fairer fix may be a targeted summer "
                   "program rather than a longer year for everyone.' "
                   "The two responses differ on exactly one move: Option 2 names the shared thread (closing "
                   "the summer-slide gap set against the cost of the cure) and voices a claim that needs both "
                   "sources; Option 1 reports each source and stops. Correct choice: Option 2.")),
        Slot("SUPPORTED", "production_frq", "Combine two given facts into one attributed claim (claim provided)",
             bank="longer_school_year", rubric_ref="rc.ohio", scored=True,
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
        Slot("MODEL", "diagnosis_frq", "Diagnose your own synthesis",
             bank="longer_school_year", scored=True,
             body=("In one or two sentences, diagnose your own work. Answer honestly: did I JOIN the two "
                   "sources on a shared thread, or did I report them one after the other? Is every idea "
                   "still attributed to the correct source, or did I blur which source said what? Name the "
                   "WEAVE letters you actually used, and say what a summary-plus-summary version of your "
                   "response would have looked like instead.")),

        # ---------------- INDEPENDENT: full synthesis-then-pick essay, AUTHORED (no CR item reuse) ----------
        Slot("INDEPENDENT", "production_frq", "Synthesize then pick: full school-year essay (authored)",
             ref="", bank="longer_school_year", rubric_ref="rc.ohio", scored=True,
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
             ref="ACC-W910-ARG-OPP-LESSON-DST", bank="daylight_saving", rubric_ref="rc.ohio", scored=True,
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
