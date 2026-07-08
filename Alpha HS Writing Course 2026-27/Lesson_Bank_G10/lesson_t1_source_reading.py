"""
lesson_t1_source_reading.py  -  G10 model lesson, TYPE 1: SOURCE-READING (low-load supporting component).

FULLY CRAFTED via the Council of Writing Instruction (DI/Engelmann, Kirschner & Hendrick, SRSD, TSIS) with
a judge adjudication (see docs). Solves four defects a prior draft had: (1) "they-say" used undefined;
(2) whole 635-word read with nothing to do (working-memory overload); (3) ambiguous "the summary" referent;
(4) "diagnose your own work" with no model/scaffold.

Fixes, by council ruling:
  1. TEACH defines BOTH "they-say" AND "MARK" in plain words before first use (DI define-before-use + TSIS
     verbatim def). Three named objects, never "the summary": the SOURCE ARTICLE, your MARK NOTES, your THEY-SAY.
  2. The read is CHUNKED by the source's natural sections; each chunk closes with a stateless choice item that
     builds one MARK slot at its lowest-load moment (KH cognitive-load management). No passive whole-source read.
  3. The MODEL DISPLAYS the finished they-say verbatim, labeled inline [M][A][R][K]; the weak version is labeled
     "do NOT copy" and corrected adjacent (DI faultless-communication; SRSD error->fix contrast survives in text).
  4. Diagnosis is MODELED (predict-the-fix) before it is asked; the self-diagnosis slot supplies a fixed MARK
     self-check with a binary per row + a repair frame + the closest-cliche fairness test (KH worked->completion
     ->independent; SRSD self-monitoring; TSIS closest-cliche). No blank "diagnose it."

Conflicts ruled: async clean model beats live coping false-start (SRSD concedes; ES 1.14 not claimed for async);
fairness/closest-cliche test is a first-class production criterion (TSIS wins the production layer); lesson stays
they-say-only, no "I say" turn (KH wins on element-interactivity for a Type-1 read).

Binds ONLY lesson-pool stimuli (contamination-free): weather (taught) -> recycling (bank-partitioned transfer).
Mnemonic MARK (proposal, not sourced). All slots map to native Timeback interactions. Runs the QC harness.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report

LESSON = Lesson(
    id="ACC-W910-L-T1-SOURCE-0001", grade="9-10", lesson_type=1,
    unit="G10 U1 - Reading a source fairly (source-reading)",
    title="Read It Fairly First: Building the They-Say (MARK)",
    target=("Read one source and write a fair, attributed they-say (a 4 to 6 sentence summary the author would "
            "agree with) using the MARK strategy: Main idea, Attribution, Reasons/evidence, Key quotable line. "
            "This is the they-say that later argument answers. Trait: reading/summary accuracy."),
    acc_tags=["ACC.W.SRC.1", "ACC.W.INFO.1", "CCSS.RI.9-10.2"],
    provenance={"copyright": "own_authored", "authored": "2026-07-08",
                "mnemonic_status": "proposal",
                "council": "Judge-adjudicated: SRSD shell; TSIS they-say def + closest-cliche test; DI "
                           "define-before-use + faultless minimal pairs; KH chunked read + worked->completion "
                           "->independent fade. Async clean model (SRSD ES 1.14 NOT claimed for async)."},
    fade_ledger_moves=["attributive-tag", "fair-summary", "hedge-preservation"],
    slots=[
        # ================= TEACH: define they-say + MARK before use; name the three objects =================
        Slot("TEACH", "teach_card", "What a they-say is (and the three things you will keep straight)",
             body=("A they-say is what your source actually says, put fairly and in its own words, before you "
                   "react to it. Here is the plain test: write it so well that the author would nod and say, "
                   "'Yes, that is my point,' even if you were about to disagree. A they-say is NOT your opinion, "
                   "and it is NOT whether you agree. You are reporting the source, not answering it. Why it "
                   "matters: a fair they-say is the point your own writing will later push against, so if you "
                   "get it wrong, everything you build on it is shaky. In this lesson you write only the "
                   "they-say. Keep three things straight, and give each its own name: (1) the SOURCE ARTICLE is "
                   "the weather article on your screen, the words the author wrote; (2) your MARK NOTES are the "
                   "four parts you find; (3) your THEY-SAY is the 4 to 6 sentence paragraph you write from those "
                   "notes. When a step names one of these three, it will say which one.")),
        Slot("TEACH", "teach_card", "The MARK strategy: each letter, with a right and a wrong example",
             body=("MARK is how you build a fair they-say from one source. Each letter has one job. "
                   "M = Main idea: the ONE point the whole source is built around. Right: the Weather Service "
                   "exists to observe, predict, and warn so people get more time. Wrong (too narrow): 'The "
                   "agency uses weather balloons,' which is one detail, not the whole point. "
                   "A = Attribution: WHO is saying it, named out loud, so the credit is clear. Right: 'According "
                   "to the National Weather Service...'. Wrong (bare fact, no source): 'Watches and warnings are "
                   "different,' which never says who reported it. "
                   "R = Reasons/evidence: the support the source gives for its main idea. Right: it pairs "
                   "computer models with the local knowledge of forecasters in its 122 offices. Wrong (your "
                   "reason, not the source's): 'because weather is important to everyone,' which the source "
                   "never says. "
                   "K = Key quotable line: ONE sentence in the source's EXACT words, inside quotation marks. "
                   "Right: 'A tornado watch means be prepared; a tornado warning means take action now.' Wrong "
                   "(a paraphrase you put in quotes, or a tiny detail): not the author's exact words, or not the "
                   "key point. Your goal today: a they-say that hits all four MARK parts and adds no opinion.")),
        Slot("TEACH", "stimulus_display", "Read the source one section at a time",
             ref="ACC-W910-INFO-LESSON-WEATHER", bank="weather_science",
             body=("Here is the source article on how the National Weather Service builds a forecast. Read it "
                   "one section at a time. After each section you will answer one short question that builds one "
                   "part of MARK, so you never have to hold the whole article in your head at once. The article "
                   "stays on screen while you answer.")),
        Slot("TEACH", "discrimination", "Section 1 check: who is speaking? (builds A)",
             ref="", labeled_grade_c=True, bank="weather_science",
             body=("Read the opening section. Then answer: in this article, who is making the claims you will "
                   "summarize? (A) a reporter who interviewed some scientists  (B) the National Weather Service "
                   "(NWS)  (C) local news stations  (D) the article does not say. "
                   "Correct: B. The source names itself, the NWS. That name is your A, Attribution. This is a "
                   "labeled Grade-C discriminate-before-produce step: naming who speaks before you summarize.")),
        Slot("TEACH", "discrimination", "Section 2 check: which detail is observation? (builds R)",
             ref="", labeled_grade_c=True, bank="weather_science",
             body=("Read the observation section. Which detail belongs to the OBSERVATION stage, measuring what "
                   "is happening now? (A) computer models calculate the coming days (that is prediction)  "
                   "(B) Doppler radars see the rotation inside a thunderstorm  (C) the agency issues a flood "
                   "forecast (that is the rivers stage)  (D) people take protective action (that is a warning "
                   "response). Correct: B. Radar readings are how the NWS observes conditions right now, a "
                   "Reasons/evidence detail (R).")),
        Slot("TEACH", "discrimination", "Section 3 check: watch or warning? (the point the author calls critical)",
             ref="", labeled_grade_c=True, bank="weather_science",
             body=("Read the warning section. A tornado is happening right now in a town. According to the "
                   "source, the NWS would issue a: (A) watch, because conditions are favorable (a watch is 'be "
                   "ready,' before it happens)  (B) warning, because the dangerous weather is already happening  "
                   "(C) flood forecast  (D) neither, until the storm ends. Correct: B. A warning means take "
                   "action now. The source calls this difference critical for public safety.")),

        # ================= MODEL: clean labeled before/after (weak struck + corrected adjacent) =============
        Slot("MODEL", "annotated_before_after", "A weak they-say becomes a fair one",
             bank="weather_science",
             body=("BEFORE (weak they-say, do NOT copy this): 'The weather is going to be bad this week, and you "
                   "should be careful.' Why it is weak, checked against MARK: A is missing (it never says WHO is "
                   "speaking); M is vague (this could describe ANY weather article ever written; it does not "
                   "name THIS source's point); R is missing (no reason or evidence from the source); K is "
                   "missing (no exact-words quote). This is the closest-cliche trap: it swaps the source's "
                   "specific point for a generic idea that fits any article. "
                   "AFTER (a strong they-say; the labels point to the visible parts): 'According to the National "
                   "Weather Service [A], the agency's central job is to observe, predict, and warn so that "
                   "communities get as much time as possible before dangerous weather hits [M]. It supports this "
                   "by pairing computer models with the local knowledge of forecasters in its 122 offices, and "
                   "by drawing a sharp line between a watch and a warning [R]. As the NWS puts it, \"A tornado "
                   "watch means be prepared; a tornado warning means take action now\" [K].' "
                   "Read the labels: the part naming the National Weather Service is [A]; the part naming "
                   "observe, predict, and warn is [M]; the part about models plus local knowledge and the "
                   "watch/warning line is [R]; the quoted sentence in quotation marks is [K]. Every MARK part is "
                   "visible in that one paragraph.")),
        Slot("MODEL", "predict_the_fix", "Predict the one fix this draft needs",
             bank="weather_science",
             body=("Here is a fresh they-say another student wrote. It passes some MARK checks but fails one "
                   "badly. Draft: 'The National Weather Service says weather can be dangerous and people should "
                   "be careful. It uses radar and balloons.' Which single fix does it most need? "
                   "(A) add attribution, name who is speaking  (B) replace the vague main idea with the source's "
                   "specific point, that the NWS exists to observe, predict, and warn so people get more time  "
                   "(C) delete the detail about radar and balloons  (D) add your own opinion about whether you "
                   "think the NWS is effective"),
             feedback=("The answer is B. The draft already names the NWS, so A is not the gap. It is a "
                       "closest-cliche: 'weather can be dangerous' could describe any article, so it fails M, "
                       "the Main idea. The one fix it most needs is the source's specific point. Option C is "
                       "wrong because the radar and balloon details are fine evidence (R); cutting them does not "
                       "fix the real problem. Option D is a trap: a they-say reports, it never reacts, so you "
                       "never add your own opinion.")),

        # ================= SUPPORTED: discrimination gate -> completion production (fade rung 1) ============
        Slot("SUPPORTED", "discrimination", "Which is a correct Key line? (minimal pair, mastery gate)",
             ref="", labeled_grade_c=True, bank="weather_science",
             body=("Discriminate before you produce (a labeled Grade-C step). All four options are candidate K "
                   "lines (Key quotable line) for the weather source. Which one is a correct K, an exact-words "
                   "quote that captures the source's most important point? "
                   "(A) 'A tornado watch means be prepared; a tornado warning means take action now.'  "
                   "(B) 'Weather balloons, released twice a day, carry instruments high into the sky.'  "
                   "(C) A tornado watch means be prepared and a warning means act now.  "
                   "(D) 'The weather can be dangerous.' "
                   "Correct: A. Option B is exact words but a minor detail, not the key point. Option C captures "
                   "the point but has no quotation marks and is not the exact words, a dropped quote. Option D "
                   "fails the fairness test: it could describe any weather article. Only A is a true K.")),
        Slot("SUPPORTED", "production_frq", "Completion: fill the MARK frame (fade rung 1)",
             bank="weather_science", rubric_ref="rc.mcas", scored=True,
             body=("Guided practice with the frame provided. Using the weather source, fill in each blank, then "
                   "read your sentences back as one paragraph. A (attribution): 'According to ____,'. M (main "
                   "idea): 'its main point is that ____.'. R (reasons): 'It supports this by ____.'. K (key "
                   "line): 'As the source puts it, \"____.\"'. Product goal: all four blanks filled from the "
                   "source, the quote in exact words, no opinion added. Scored on summary accuracy and fair "
                   "attribution.")),
        Slot("MODEL", "diagnosis_frq", "Diagnose a draft with the MARK self-check (modeled, then you)",
             bank="weather_science", scored=True,
             body=("First, watch the check run on a flawed draft, then run it yourself. Flawed draft: 'The "
                   "Weather Service does important work and uses a lot of technology.' Run the MARK self-check, "
                   "step by step. Step 1, M: does it state the source's ONE main point? No, it is a cliche that "
                   "fits any article, so the repair frame is 'The main idea of this article is ____.'. Step 2, "
                   "A: does it name who is speaking? It says Weather Service, so A is met. Step 3, R: does it "
                   "give the source's reasons or evidence? No, so add one: 'The NWS bases this on ____.'. Step "
                   "4, K: is there an exact-words quote in quotation marks? No, so add one. Now you: in two or "
                   "three sentences, say which MARK letters that draft was missing, write one repair using a "
                   "frame above, and name the closest-cliche problem in your own words.")),

        # ================= INDEPENDENT: full they-say + fixed self-check with repair frames =================
        Slot("INDEPENDENT", "production_frq", "Write a full fair they-say, then run the self-check",
             bank="weather_science", rubric_ref="rc.mcas", scored=True,
             body=("Independent performance: write a fair they-say of the weather article, 4 to 6 sentences, "
                   "using MARK. You may use these frames or your own: 'According to the NWS, ____.'; 'The NWS "
                   "reports that ____.'; 'The NWS bases this on ____.'; 'As the NWS puts it, \"____.\"'. Product "
                   "goal, all four required: (1) M name the source's one main idea, not just a detail; (2) A "
                   "name who is speaking; (3) R include at least one reason or piece of evidence the source "
                   "gives; (4) K include one exact-words quote in quotation marks; and add no opinion. Then run "
                   "the MARK self-check on your own they-say. For each row, if you mark No, use the repair frame "
                   "and rewrite. M: did I state the ONE main point, not just a detail? Repair: 'The source's "
                   "main point is that ____.'. A: did I name WHO is speaking? Repair: 'According to ____,'. R: "
                   "did I include a reason or evidence the source gives? Repair: 'The source supports this by "
                   "____.'. K: did I include one exact-words quote in quotation marks? Repair: 'As the source "
                   "puts it, \"____.\"'. FAIR (the closest-cliche test): could my they-say describe ANY article "
                   "on this topic, or ONLY this source? If any article, add the source's specific claim and "
                   "evidence until it could only describe this one, and cut any opinion. Scored on summary "
                   "accuracy and fair attribution.")),

        # ================= TRANSFER: same MARK + self-check, bank-partitioned recycling source ==============
        Slot("TRANSFER", "production_frq", "Apply MARK to a NEW source (bank-partitioned)",
             ref="ACC-W910-INFO-LESSON-RECYCLING", bank="recycling_recovery", rubric_ref="rc.mcas", scored=True,
             body=("Transfer: apply MARK to a source you have not practiced on. Read the recycling article, then "
                   "write a fair they-say, 4 to 6 sentences, using the same MARK moves. You may use the frames: "
                   "'According to the source, ____.'; 'The source reports that ____.'; 'It bases this on ____.'; "
                   "'As the source puts it, \"____.\"'. Product goal, all four required: name the Main idea, "
                   "Attribute the claims to the source, give at least one Reason or piece of evidence, and quote "
                   "one Key line in exact words; add no opinion. Then run the same MARK self-check, using the "
                   "FAIR closest-cliche test: could your they-say describe any recycling article, or only this "
                   "one? Keep every hedge the article uses. Scored on summary accuracy and fair attribution.")),
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
