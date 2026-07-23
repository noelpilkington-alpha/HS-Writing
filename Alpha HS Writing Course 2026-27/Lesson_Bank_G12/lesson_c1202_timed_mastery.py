"""
lesson_c1202_timed_mastery.py  -  G12 KC C.12.02, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD), applied to SUSTAINED
TIMED AP WRITING. This is the G12 U2 course-completion gate; woven D.12.01 (voice) folds in here.

CURRENT SoT ANCHOR:
  - KC:    C.12.02  "Sustained AP writing under timed conditions"  (OVERLAY: exam timing on CCSS W.10)
  - unit:  G12 U2  Timed AP mastery (course_gate=True); woven D.12.01 voice
  - funnel: timed   archetype: T7 (BUILD)   production ceiling: essay
  - acc:   [ACC.W.PROD.1]   ccss: [W.11-12.10]
  - taught stimulus:   ACC-W910-ARG-LESSON-WORKFORCEINVEST   (G12 lesson bucket)
  - transfer stimulus: ACC-W910-ARG-LESSON-WATERTRADEOFF     (bank-partitioned)
  - rc.* rubric:       rc.ap

AUTHORED to the finalized T7/BUILD playbook + the 19-gate contract:
  * The G12 mastery tier: assemble a full AP-quality argument essay under sustained timed conditions, holding
    everything the course has taught (nuanced claim, evidence, reasoning, positioning, AND sophistication)
    while managing the clock. CUE the faded sub-skills, do NOT re-teach; the plan offloads structure.
  * Woven D.12.01 (voice through syntactic choice): folded into the final pass as a style move, vary sentence
    structure for emphasis, not a separate lesson.
  * PLAN written ON-PLATFORM (vet blocker fix); all prompts SELF-CONTAINED (no prior-work reference).
  * MODEL is the async annotated before/after worked example of a timed budget/plan (NO near-peer/human coping
    model; labeled author-voice annotations) + predict-the-fix; diagnosis modeled-then-scaffolded. SRSD live ES
    NOT claimed.
  * Stateless / display-only; no prior-work ref; no off-platform; no loops. Seam-routing UNBUILT/pending-eng.

Runs the QC harness on execution and prints PASS/FAIL. Dependency-free (stdlib + lesson_contract).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report

LESSON = Lesson(
    id="ACC-W910-L-G12-C1202-0001", grade="9-10", lesson_type=7,
    unit="G12 U2 - Timed AP mastery (course completion gate; voice woven)",
    title="Sustained and Timed: Assemble a Full AP Argument Under the Clock (BUILD)",
    target=("Assemble a complete, AP-quality argument essay under sustained timed conditions: budget the time, "
            "plan fast, then build with everything the course taught (nuanced claim, evidence, reasoning, "
            "positioning, sophistication), closing with a voice-and-concision pass. Climbs to the essay under "
            "time. Traits: the full AP rubric (Thesis, Evidence and Commentary, Sophistication)."),
    acc_tags=["ACC.W.PROD.1", "CCSS.W.11-12.10"],
    provenance={"copyright": "own_authored", "authored": "2026-07-10", "mnemonic_status": "proposal",
                "kc": "C.12.02", "sot": "KC_Map_and_Unit_Arch_G9-12.md (G12 U2 Timed AP mastery; course gate)",
                "taught_stimulus": "ACC-W910-ARG-LESSON-WORKFORCEINVEST",
                "transfer_stimulus": "ACC-W910-ARG-LESSON-WATERTRADEOFF",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "d1201_note": ("D.12.01 (voice through syntactic choice) is woven into this capstone's final "
                               "pass as a style move, not built as a separate file."),
                "council": ("T7/BUILD playbook, G12 mastery tier: cue faded sub-skills not re-teach; plan "
                            "ON-PLATFORM (vet blocker fix); self-contained prompts (no prior-work ref); "
                            "annotated before/after (labeled author-voice annotations, NO near-peer/human "
                            "coping model); app-owned mechanics assumed not re-taught; SRSD live ES NOT claimed. "
                            "rc.ap = AP mastery tier.")},
    fade_ledger_moves=["time-budget", "cue-faded-subskills", "voice-and-concision-pass"],
    slots=[
        # ================= TEACH: define time budgeting + what to hold; the voice pass =================
        Slot("TEACH", "teach_card", "What sustained timed mastery adds (budget the whole time, not just plan)",
             body=("By now you can plan fast and build an argument. The mastery tier adds one thing: sustaining "
                   "quality across a full timed essay without running out of clock or energy. Time budgeting "
                   "means deciding, before you write, roughly how many minutes go to reading and planning, to "
                   "drafting each body paragraph, and to a final pass, so no stage steals from the others. The "
                   "trap at this level is uneven pacing: a brilliant opening and a rushed, thin ending, or so "
                   "much time on the plan that the essay is unfinished. Your claim, also called the thesis, "
                   "means the one position your essay defends. This capstone does not teach new moves; it asks "
                   "you to HOLD all of them at once under time, the nuanced claim, evidence and reasoning, "
                   "positioning among views, and the sophistication moves, while pacing yourself. Goal today: "
                   "budget the time, plan fast, and produce a complete, sustained AP-quality argument.")),
        Slot("TEACH", "teach_card", "What to cue, and the closing voice-and-concision pass",
             body=("Assemble moves you already own; cue them, do not relearn them. Claim: a nuanced position, "
                   "not X but Y. Evidence and reasoning: each body point carries support and a warrant, which "
                   "means the reasoning sentence that says why the evidence supports the point. Positioning: "
                   "concede a rival view and turn to hold yours. Sophistication: situate the question in a "
                   "larger one, show its complexity, and hold the tension. Reserve the final minutes for a "
                   "voice-and-concision pass. Voice through syntactic choice means using sentence structure "
                   "for emphasis: a short, blunt sentence after several longer ones lands a key point; varying "
                   "how sentences open keeps the prose from droning. Concision means cutting words that do no "
                   "work so each sentence earns its place. Together they are the last-pass polish that "
                   "separates a strong essay from a merely complete one. Reward the essay that is complete, "
                   "sustained, and controlled, not the one that peaked early. (App-ownership note: the sentence "
                   "mechanics behind voice and concision, combining, subordination, and conventions, are owned "
                   "upstream by AlphaWrite, G3-8, and EGUMPP, G3-10; assumed as retrieval-gated prerequisites "
                   "and applied, not re-taught here.)")),
        Slot("TEACH", "stimulus_display", "Read the prompt source: prepare the next workers, or protect the present ones?",
             ref="ACC-W910-ARG-LESSON-WORKFORCEINVEST", bank="workforce_invest",
             body=("Read the source on whether a society should invest first in preparing more people for "
                   "growing fields or first in protecting the workers a change leaves behind. This is your "
                   "timed prompt. Read and note the points you would most want to make and where the real "
                   "complexity sits, so that when the clock starts you can budget your time and plan fast. The "
                   "source stays on screen while you work.")),

        # ================= MODEL: annotated before/after of a TIME BUDGET/PLAN -> predict-the-fix ============
        Slot("MODEL", "annotated_before_after", "Watch an unbudgeted attempt become a paced plan",
             bank="workforce_invest",
             body=("BEFORE (no budget, no plan, all-in on the opening): a writer spends the first third of the "
                   "time crafting an elaborate, beautiful introduction about 'the timeless struggle between "
                   "progress and security,' reaches the first body paragraph with the clock half gone, and "
                   "ends with a one-line conclusion and no sophistication move. Check it: the prose is fine, "
                   "but the pacing sank the essay, the argument is unfinished and the top-band moves never "
                   "arrive. Under time, an unbudgeted essay fails no matter how strong the sentences are. "
                   "AFTER (a time budget and fast plan jotted first, annotated): "
                   "'Budget: 2 min read/plan, 3 min intro + claim, 6 min each of two body paragraphs, 2 min "
                   "sophistication turn, 2 min voice/concision pass [time budget: every stage protected]. "
                   "Claim: invest first in protecting displaced workers, not in broad pipelines [nuanced claim "
                   "cued]. Body 1: the harm is present and concentrated + warrant. Body 2: concede the "
                   "prepare-the-future view, then answer it. Sophistication: situate as future-vs-present "
                   "justice; hold the tension. Order: present-harm first.' "
                   "From that budget the writer opens directly with the claim, gives each paragraph its share "
                   "of the clock, and reserves time for the sophistication turn and the polish. "
                   "Read the labels: the budget protects every stage and the plan cues owned moves, so the "
                   "essay is complete AND sustained. That paced control is what the mastery tier rewards, and "
                   "what the beautiful-but-unfinished BEFORE never reaches.")),
        Slot("MODEL", "predict_the_fix", "Predict: what most threatens this timed essay?",
             bank="workforce_invest",
             body=("Diagnose this timed approach before the reveal. A writer plans to 'just start writing and "
                   "see where it goes,' intending to make it sophisticated by using impressive sentences "
                   "throughout. What single move would most protect the essay? "
                   "(A) set a time budget and a fast plan first, reserving explicit minutes for a body-paragraph "
                   "each and for the sophistication turn, so the essay finishes complete  "
                   "(B) write longer, more impressive sentences  "
                   "(C) spend more time on the introduction  "
                   "(D) use a larger vocabulary throughout"),
             feedback=("Correct: A. 'Start writing and see where it goes' is the pacing trap: without a budget "
                       "the essay drifts and the sophistication move and conclusion get squeezed out. A time "
                       "budget plus a fast plan protects each stage and guarantees the top-band moves actually "
                       "get written. Impressive sentences (B), a longer intro (C), or big vocabulary (D) "
                       "consume the very time the essay needs to finish, and none of them is sophistication, "
                       "which is depth of thinking, not diction.")),

        # ================= SUPPORTED: discrimination (Grade-C) -> guided ON-PLATFORM budget+plan ==============
        Slot("SUPPORTED", "discrimination", "Which timed approach will finish a strong essay? (labeled Grade-C)",
             ref="", labeled_grade_c=True, bank="workforce_invest",
             body=("Discriminate before you produce (a Grade-C design bet we label as a bet, not proof). Under "
                   "sustained time, which approach best assembles a complete, high-scoring essay? "
                   "(A) 'Budget the time across reading, planning, two body paragraphs, a sophistication turn, "
                   "and a polish pass; jot a nuanced claim and an order; then draft to the budget.'  "
                   "(B) 'Write a gorgeous introduction and trust the rest to flow.'  "
                   "(C) 'Use the most advanced vocabulary possible so it sounds sophisticated.'  "
                   "(D) 'Draft with no plan and fix everything at the end.' (no time will remain to fix)  "
                   "Correct: A. A protects every stage with a budget, cues a nuanced claim, and sets an order, "
                   "so the essay finishes complete with its top-band moves intact. B over-invests in the "
                   "opening; C mistakes vocabulary for sophistication; D leaves no time to repair. Only A "
                   "sustains quality under the clock.")),
        Slot("SUPPORTED", "production_frq", "Guided: write your time budget + plan in the plan box",
             ref="", bank="workforce_invest", rubric_ref="rc.4trait", scored=True, unit="sentence",
             body=("Write your budget and plan in the plan box below (this is your on-platform plan; there is "
                   "no paper). In a few lines, set a time budget and a fast plan for the workforce prompt. Fill "
                   "in this frame, or write your own: 'Budget: ___ min read/plan, ___ min per body paragraph, "
                   "___ min sophistication turn, ___ min voice/concision pass. Claim: ___ [nuanced, not X but "
                   "Y]. Body 1: ___ + why it counts. Body 2: ___ [the view you concede and answer]. "
                   "Sophistication: ___ [how you will situate and hold the tension]. Order: ___.' Product goal: "
                   "a realistic time budget plus a nuanced claim, planned body points, a sophistication plan, "
                   "and an order. Scored on Organization (planning), AP tier.")),
        Slot("MODEL", "diagnosis_frq", "Diagnose a timed budget/plan with the mastery checklist (modeled, then you)",
             ref="", bank="workforce_invest", scored=True,
             body=("First watch the check run on a weak budget/plan, then run the same checklist on a fresh one "
                   "you write here. Weak plan: 'Spend most of the time making it sound good. Claim: this is a "
                   "hard issue. Just write until done.' Run the mastery self-check step by step. Step 1, "
                   "Budget: are minutes assigned to each stage, including the ending? No; assign them so the "
                   "essay finishes. Step 2, Claim: is it a nuanced position? No ('a hard issue' is not a "
                   "claim); sharpen to 'not X but Y.' Step 3, Sophistication: is there a plan to situate and "
                   "hold the tension? No; add one. Step 4, Order + polish: is there an order and time reserved "
                   "to tighten? No; add both. Now you: write a fresh budget-and-plan for the workforce prompt "
                   "in the box, then run the same 4-item checklist on it. For each No, use the matching repair. "
                   "Finish by naming which mastery item your plan still needs.")),

        # ================= INDEPENDENT: build the full timed essay + voice/concision pass, self-contained =====
        Slot("INDEPENDENT", "production_frq", "Build the sustained timed AP essay, then polish (self-contained)",
             ref="", bank="workforce_invest", rubric_ref="rc.4trait", scored=True, unit="essay",
             body=("Independent performance, self-contained (write a fresh budget, plan, and essay here; do not "
                   "refer to an earlier item). On the workforce prompt, under sustained timed conditions, jot a "
                   "brief time budget and plan at the top of the box, then draft the full essay. Product goal: "
                   "(1) a nuanced claim; (2) at least two body paragraphs with evidence and reasoning warrants; "
                   "(3) a handled opposing view; (4) the sophistication moves woven in (situate, complicate, "
                   "hold the tension); (5) a brief conclusion. Reserve the last minutes for a voice-and-"
                   "concision pass: vary sentence structure for emphasis and cut words that do no work. Before "
                   "you submit, check that the essay is COMPLETE (not cut off), the claim is nuanced, and the "
                   "sophistication moves are present. Scored on the full AP rubric.")),

        # ================= TRANSFER: same timed mastery move, bank-partitioned prompt =================
        Slot("TRANSFER", "stimulus_display", "Read a NEW timed prompt: when food and power compete for the same water",
             ref="ACC-W910-ARG-LESSON-WATERTRADEOFF", bank="water_tradeoff",
             body=("Read this new prompt source on a hard trade-off: when water is scarce, should a region "
                   "protect it for growing food or for generating power? This is a new timed prompt. Read and "
                   "note the points you would make and where the complexity sits, so you can budget your time "
                   "and plan fast when the clock starts. The source stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Build a sustained timed AP essay on the new prompt (bank-partitioned)",
             ref="", bank="water_tradeoff", rubric_ref="rc.4trait", scored=True, unit="essay",
             body=("Transfer to a prompt you have not practiced, under sustained timed conditions. On the water "
                   "trade-off prompt, jot a time budget and plan at the top of the box, then draft the full "
                   "essay. Product goal: a nuanced claim; body paragraphs with evidence and warrants; a handled "
                   "opposing view; the sophistication moves woven in (situate, complicate, hold the tension); a "
                   "brief conclusion; and a closing voice-and-concision pass. Same sustained timed mastery move "
                   "as the workforce prompt; new prompt. Scored on the full AP rubric.")),
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
