"""
lesson_t3_evidence_integration.py  -  G10 model lesson, TYPE 3: EVIDENCE-INTEGRATION (flagship).

Assembles a Timeback assessment-test (ordered item sequence) that instantiates the council-adjudicated
Type-3 shell (G10_Model_Lesson_Specs.md) against the REAL G10 LESSON-POOL banks (contamination-free: no
test-pool stimulus, no CR/SR item is bound; students never learn on a passage they are later tested on).
Binds:
  - stimulus  ACC-W910-INFO-LESSON-WETLANDS (wetlands restoration) -> the source read + integrated on
  - stimulus  ACC-W910-INFO-LESSON-HIGHWAYS (interstate highways)  -> the bank-partitioned transfer source
The integrated-vs-dropped discrimination is authored inline (Grade-C, labeled). The Independent production
is an AUTHORED production_frq on the wetlands source (no CR item bound), grader-scored on rc.staar.

SRSD shell (Teach/Model/Supported/Independent/Transfer). Model = the modality-corrected 4-mechanism async
sequence (clean annotated before/after -> predict-the-fix -> feedback on the student's OWN draft [the FRQ
grader] -> student-generated diagnosis). Mnemonic PROVE (established-caveat: verify before K-8 reuse).
Bank-partitioned transfer (wetlands -> interstate highways). All slots map to native Timeback interactions.

Runs the QC harness on execution and prints PASS/FAIL. Dependency-free (stdlib + lesson_contract).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report

LESSON = Lesson(
    id="ACC-W910-L-T3-EVIDENCE-0001", grade="9-10", lesson_type=3,
    unit="G10 U2 - Source-based argument (evidence-integration)",
    title="Integrate the Evidence: No Quote Stands Alone (PROVE)",
    target=("Integrate a source quote so it never stands alone: attributive tag (who said it) plus a "
            "because/but/so hinge that ties it to the claim. Trait: Evidence/Development."),
    acc_tags=["ACC.W.SRC.1", "ACC.W.ARG.2", "CCSS.W.9-10.1"],
    provenance={"copyright": "own_authored", "authored": "2026-07-07",
                "mnemonic_status": "established-caveat",
                "council": "SRSD flagship shell; TWR sentence-combining substrate; TSIS frame-the-quotation"},
    fade_ledger_moves=["because/but/so", "attributive-tag", "sentence-combining"],
    slots=[
        # ---------------- TEACH: background + discuss + test-demand orientation ----------------
        Slot("TEACH", "teach_card", "Why a dropped quote costs you points",
             body=("A dropped quote is a quotation set into your paragraph with no lead-in and no follow-up, "
                   "as if it could speak for itself. It cannot. The reader is left guessing who said it and "
                   "why it matters to your claim. On every state rubric, evidence that is merely present but "
                   "not developed sits in the middle band. The move that lifts it is integration. Our cue for "
                   "it is PROVE: Point (state the claim), Reference (attribute and cite the source), Observe "
                   "(explain what it shows), Verify (tie it back to the claim), Extend (say why it matters). "
                   "Goal for today: write evidence where no quote stands alone.")),
        Slot("TEACH", "stimulus_display", "Read the source on wetlands",
             ref="ACC-W910-INFO-LESSON-WETLANDS", bank="wetlands_restoration",
             body="Read the source about wetlands. Mark one fact you could use as evidence, and note who reports it."),

        # ---------------- MODEL: 4-mechanism async sequence ----------------
        Slot("MODEL", "annotated_before_after", "Watch a dropped quote become integrated",
             bank="wetlands_restoration",
             body=("BEFORE (drops the move): The source says wetlands stop floods. \"Wetlands once stored 60 "
                   "days of floodwater.\" This proves my point. "
                   "AFTER (explains HOW, annotated): According to the source, which cites the EPA, one stretch "
                   "of the Mississippi River once held natural wetlands that could store at least 60 days of "
                   "floodwater, but after most were drained or filled the same stretch could store only 12 "
                   "days [Reference: who + what]. That drop from 60 days to 12 matters because it shows "
                   "draining the wetlands did not just remove scenery; it stripped away most of the land's "
                   "built-in flood protection [Verify + Extend: tied to the claim]. "
                   "Notice the AFTER version never leaves the quote alone: an attributive tag introduces it and "
                   "a because-hinge follows it. That is the R-O-V-E of PROVE doing the work.")),
        Slot("MODEL", "predict_the_fix", "Predict the fix before you see it",
             bank="wetlands_restoration",
             body=("Diagnose this draft before we reveal the fix. Which single move would most improve it? "
                   "Draft: 'Wetlands protect rare animals. \"More than one-third of endangered species live "
                   "only in wetlands.\" So we should restore them.' "
                   "(A) add an attributive tag and a because-hinge  (B) add a second quote  "
                   "(C) make the sentences longer  (D) move the quote to the end"),
             feedback=("The strongest fix is A. The quote is dropped: no one is named and nothing ties it to the "
                       "claim. Naming the source and adding a because-hinge (it matters because losing wetlands "
                       "would leave those species with nowhere else to live) turns a bare quote into developed "
                       "evidence. That is the Reference and Verify moves in PROVE. A longer sentence or a second "
                       "quote does not fix an unintegrated one.")),

        # ---------------- SUPPORTED: discrimination (Grade-C, labeled) then guided production ----------------
        Slot("SUPPORTED", "discrimination", "Integrated vs. dropped (minimal pair)",
             ref="", labeled_grade_c=True, bank="wetlands_restoration",
             body=("Design-bet step (discriminate before you produce, a Grade-C move we are testing, not a "
                   "proven law): pick the version that integrates its evidence rather than dropping it. Both "
                   "use the same wetlands figure; they differ on exactly one move, the attribution-plus-hinge. "
                   "Option A (dropped): 'Wetlands are disappearing. \"The country once held 221 million acres "
                   "and only 103 million remained by the mid-1980s.\" We should act.' "
                   "Option B (integrated): 'The U.S. Geological Survey reports that the lower 48 states once "
                   "held about 221 million acres of wetlands but had only about 103 million left by the "
                   "mid-1980s, which matters because it means the country drained more than half of a landscape "
                   "before understanding the flood control and habitat it provided.' "
                   "Option B names who reported the figures and ties the loss to why it matters; Option A drops "
                   "the numbers in with no lead-in and no follow-up.")),
        Slot("SUPPORTED", "production_frq", "Write ONE integrated PROVE sentence",
             bank="wetlands_restoration", rubric_ref="rc.staar", scored=True,
             body=("Using one fact from the wetlands source, write ONE sentence that (1) attributes the fact to "
                   "the source and (2) ties it to a claim with a because/but/so hinge. Do not let the quote "
                   "stand alone.")),
        Slot("MODEL", "diagnosis_frq", "Diagnose your own sentence",
             bank="wetlands_restoration", scored=True,
             body=("In one or two sentences, diagnose your own work: what would a dropped-quote version have "
                   "looked like, what move did you add to integrate it, and why is your version stronger for "
                   "the claim? Name the PROVE letters you used.")),

        # ---------------- INDEPENDENT: full paragraph, AUTHORED production (no CR item bound) ----------------
        Slot("INDEPENDENT", "production_frq", "Develop a full evidence paragraph on the wetlands source",
             ref="", bank="wetlands_restoration", rubric_ref="rc.staar", scored=True,
             body=("Independent performance: using the wetlands source, write a paragraph that states a claim "
                   "about why wetlands are worth protecting or restoring and develops it with at least one "
                   "fully integrated piece of source evidence (attribution plus a because/but/so hinge). Do not "
                   "let any quote or figure stand alone. Scored on Evidence/Development.")),

        # ---------------- TRANSFER: same move, partitioned content bank ----------------
        Slot("TRANSFER", "production_frq", "Integrate evidence on a NEW topic",
             ref="ACC-W910-INFO-LESSON-HIGHWAYS", bank="interstate_highways", rubric_ref="rc.ohio", scored=True,
             body=("Transfer: do the same integration move on a source you have not practiced on. Read the "
                   "interstate highways article, then write one integrated evidence sentence (for example, "
                   "about the network's roughly 48,890 miles or the share of driving it carries), attributing "
                   "the figure to who reported it and extending it with why the evidence matters to a claim. "
                   "Scored on Evidence/Development.")),
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
