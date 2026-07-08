"""
lesson_t1_source_reading.py  -  G10 model lesson, TYPE 1: SOURCE-READING (low-load supporting component).

Assembles a Timeback assessment-test (ordered item sequence) that instantiates the council-adjudicated
Type-1 shell (G10_Model_Lesson_Specs.md) against the REAL G10 LESSON-POOL banks (contamination-free: no
test-pool stimulus, no CR/SR item is bound; students never learn on a passage they are later tested on).
Target: read one source, build a fair attributive understanding, and extract usable material (the "they
say"). Binds:
  - stimulus  ACC-W910-INFO-LESSON-WEATHER (how a weather forecast is made) -> the source read + summarized fairly
  - stimulus  ACC-W910-INFO-LESSON-RECYCLING (materials recovery)           -> the bank-partitioned transfer source
The fair-use-of-source discrimination is authored inline (Grade-C, labeled); no item-bank binding.

SRSD shell (Teach/Model/Supported/Independent/Transfer). Model = the modality-corrected 4-mechanism async
sequence (clean annotated before/after -> predict-the-fix -> student-generated diagnosis; feedback on the
student's OWN draft is the FRQ grader). This is a supporting component, so the ladder fades FAST: annotated
model -> partial (student supplies the attribution slot) -> full independent MARK summary. Mnemonic MARK
(proposal, not sourced). Bank-partitioned transfer (weather taught -> recycling new).
All slots map to native Timeback interactions.

Runs the QC harness on execution and prints PASS/FAIL. Dependency-free (stdlib + lesson_contract).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report

LESSON = Lesson(
    id="ACC-W910-L-T1-SOURCE-0001", grade="9-10", lesson_type=1,
    unit="G10 U1 - Reading a source fairly (source-reading)",
    title="Read It Fairly First: Building the They-Say (MARK)",
    target=("Read one source and build a fair, attributed summary you could quote from: name the Main idea, "
            "Attribute the figures to who reported them, capture the Reasons/evidence, and lift one Key line. "
            "Sets up the they-say that later argument answers. Trait: reading/summary accuracy."),
    acc_tags=["ACC.W.SRC.1", "ACC.W.INFO.1", "CCSS.RI.9-10.2"],
    provenance={"copyright": "own_authored", "authored": "2026-07-07",
                "mnemonic_status": "proposal",
                "council": "SRSD shell; TSIS they-say (fair representation before response); DI faultless "
                           "minimal-pair distortion; adapts SRSD Model-It for async delivery (no ES claimed)"},
    fade_ledger_moves=["attributive-tag", "fair-summary", "hedge-preservation"],
    slots=[
        # ---------------- TEACH: background + discuss + test-demand orientation ----------------
        Slot("TEACH", "teach_card", "Why a fair, attributed summary comes first",
             body=("Before you can argue with a source, you have to represent it fairly. That fair version is "
                   "the they-say your own writing will answer, so getting it wrong quietly weakens every point "
                   "you build on top of it. Our cue for reading a source is MARK: Main idea (what is the "
                   "author's overall point?), Attribution (who is saying it, and where does the figure come "
                   "from?), Reasons/evidence (what facts back the point?), Key quotable line (one sentence "
                   "worth quoting exactly). A fair summary keeps the author's hedges (words like about, can, "
                   "and twice a day) and names the source. A distortion does the opposite: it cherry-picks the "
                   "scariest number, drops the attribution, or turns a careful claim into an absolute (for "
                   "example, turning the article's plain statement that no forecast model is perfect into a "
                   "claim that forecasters can predict any storm). Reading tasks on the test ask you to "
                   "summarize and use a source accurately, so a distorted they-say costs you. Goal for today: "
                   "build a fair, attributed summary you could actually quote from.")),
        Slot("TEACH", "stimulus_display", "Read the source on how a weather forecast is made",
             ref="ACC-W910-INFO-LESSON-WEATHER", bank="weather_science",
             body=("Read the article about how the National Weather Service builds a forecast. As you read, "
                   "keep the MARK moves in mind: find the one sentence that states the author's Main idea, "
                   "notice each place a figure is Attributed to a named source (NOAA or the National Weather "
                   "Service), and pick one Key line you could quote exactly. The next steps will ask you to "
                   "use what you found.")),

        # ---------------- MODEL: 4-mechanism async sequence (clean before/after + predict-the-fix) --------
        Slot("MODEL", "annotated_before_after", "Watch a distorted summary become a fair one",
             bank="weather_science",
             body=("BEFORE (distorts the source): Weather balloons fly 115,000 feet into the sky every hour, "
                   "and the article proves the Weather Service can predict any storm perfectly, so no forecast "
                   "should ever catch anyone off guard. "
                   "AFTER (fair, annotated with MARK): [Main idea] The article explains that a modern forecast "
                   "is built as a chain that runs from observation to prediction to a public warning, not from "
                   "a single guess. [Attribution] Its figures come from NOAA and the National Weather Service, "
                   "not from the writer's opinion. [Reasons/evidence] The agency runs 92 weather-balloon "
                   "stations that launch twice a day, 365 days a year, and each balloon can rise above 35 "
                   "kilometers, about 115,000 feet; closer to the ground it operates a network of about 160 "
                   "Doppler radars, and 122 local offices adjust the computer models with regional knowledge. "
                   "[Key line] As the article puts it, a forecast 'is built from steady measurement, tested "
                   "science, and human judgment.' "
                   "Notice what the BEFORE version broke: it said balloons fly every hour (the article says "
                   "twice a day), it treated 115,000 feet as a routine altitude (the article says a balloon "
                   "CAN rise that high, which is a ceiling), it turned 'no model is perfect' into perfect "
                   "prediction, and it dropped who reported the figures. The AFTER version keeps the hedges and "
                   "names the source, so it earns the reader's trust.")),
        Slot("MODEL", "predict_the_fix", "Predict the distortion before the reveal",
             bank="weather_science",
             body=("Diagnose this summary before we reveal the fix. A classmate writes: 'The weather article "
                   "shows the Weather Service launches balloons every hour and can predict any storm "
                   "perfectly.' Which is the clearest distortion of the source? "
                   "(A) it turns the article's 'twice a day' launches into 'every hour' and its plain statement "
                   "that no model is perfect into a claim of perfect prediction, and it drops who reported the "
                   "figures  (B) the summary is simply too short  (C) it summarizes the wrong topic  (D) it "
                   "quotes far too much of the article"),
             feedback=("The strongest answer is A. The source says crews launch the balloons twice a day, 365 "
                       "days a year, not every hour, and it states plainly that no model is perfect, which is "
                       "exactly why local forecasters adjust the computer results by hand. The summary also "
                       "never names NOAA or the National Weather Service as the source. A fair MARK summary "
                       "keeps the article's hedges (about, can, twice a day) and attributes each figure to who "
                       "reported it. That is the Main idea and Attribution moves working together. Length is "
                       "not the problem here; faithfulness is.")),

        # ---------------- SUPPORTED: discrimination (Grade-C, labeled) then partial-fade attribution --------
        Slot("SUPPORTED", "discrimination", "Fair use of a source vs. off-claim or overstated material",
             ref="", labeled_grade_c=True, bank="weather_science",
             body=("Design-bet step (discriminate before you produce, a Grade-C move we are testing, not a "
                   "proven law): choosing material that genuinely and fairly supports a claim is the flip side "
                   "of writing a fair summary. Both sentences below draw on the weather source for the claim "
                   "that a forecast rests on measurement. Pick the one that stays inside what the source "
                   "reports, not the one that quietly overstates it. "
                   "Option A (fair support): 'The forecast rests on measurement: the National Weather Service "
                   "runs 92 balloon stations that launch twice a day and about 160 Doppler radars that track "
                   "storms.' "
                   "Option B (off-claim / overstated): 'The forecast rests on measurement, which is why the "
                   "Weather Service can tell you exactly what the weather will be a month from now.' "
                   "The options differ on exactly one thing: whether the material earns its place as fair "
                   "support. Option A repeats figures the source actually reports; Option B adds a claim about "
                   "month-ahead certainty the source never makes.")),
        Slot("SUPPORTED", "production_frq", "Partial fade: write the Attribution move only",
             bank="weather_science", rubric_ref="rc.mcas", scored=True,
             body=("Guided practice (partial fade). The Main idea and Reasons are already drafted for you: "
                   "'The article explains that a forecast is built as a chain, from balloon and radar "
                   "observations to computer models that local forecasters adjust, and finally to a public "
                   "warning when dangerous weather is near.' Write the Attribution move only: in one sentence, "
                   "name who reports the forecasting figures and make clear the claims come from the source, "
                   "not from your own opinion.")),
        Slot("MODEL", "diagnosis_frq", "Diagnose your own attribution",
             bank="weather_science", scored=True,
             body=("In one or two sentences, diagnose your own work: what would a no-attribution version have "
                   "looked like, what did you add to attribute the figures, and why does naming the source make "
                   "the summary fairer to the author? Name the MARK letters you used.")),

        # ---------------- INDEPENDENT: full MARK summary, faded to no scaffold ----------------
        Slot("INDEPENDENT", "production_frq", "Write a full fair MARK summary of the source",
             bank="weather_science", rubric_ref="rc.mcas", scored=True,
             body=("Independent performance: write a short fair summary (3 to 4 sentences) of the "
                   "weather-forecast article using all four MARK moves. State the Main idea, Attribute the "
                   "figures to the agency that reported them, give the key Reasons/evidence, and end with one "
                   "Key line you could quote exactly. Keep the author's hedges (words like about, can, and "
                   "twice a day); do not overstate. Scored on summary accuracy and fair attribution.")),

        # ---------------- TRANSFER: same MARK move, partitioned content bank ----------------
        Slot("TRANSFER", "production_frq", "Apply MARK to a NEW source (bank-partitioned)",
             ref="ACC-W910-INFO-LESSON-RECYCLING", bank="recycling_recovery", rubric_ref="rc.mcas", scored=True,
             body=("Transfer: apply MARK to a source you have not practiced on. Read the recycling article, "
                   "then write a short fair summary (3 to 4 sentences) that states the Main idea, Attributes "
                   "the figures to the agency that reported them (the EPA), gives the key Reasons/evidence, and "
                   "ends with one Key line you could quote. Keep every hedge the article uses (words like about "
                   "and almost). Scored on summary accuracy and fair attribution.")),
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
