"""
lesson_t3_evidence_integration.py  -  G10 model lesson, TYPE 3: EVIDENCE-INTEGRATION (flagship).

FULLY CRAFTED to the 17-gate DI bar (mirrors the crafted Type-1 template). This is the highest-load
supporting type: it teaches the student to integrate a source quote so no bare quote stands alone.
Relevant council seats and how each shows up:
  - SRSD: PROVE is an explicitly named, modeled strategy with a student self-check.
  - TSIS (Graff and Birkenstein): frame-the-quotation / quotation-sandwich; the attributive tag is defined.
  - TWR (The Writing Revolution): sentence-combining substrate; the because/but/so hinge and the appositive
    are defined and used as the joining moves that integrate a quote.
  - DI (Engelmann): faultless communication via minimal pairs (integrated vs dropped) and define-before-use.
  - KH (Kirschner and Hendrick): worked example -> completion frame -> independent, to stage the sub-skill load.

Four defects the earlier draft had, now fixed (and gated):
  1. "attributive tag" and "because/but/so hinge" were used before being defined -> both are now defined in
     plain words in a TEACH card, along with "appositive" and "controlling idea/claim" (define-before-use).
  2. The BEFORE/AFTER now annotates every PROVE letter on a real EPA wetlands fact (60 days to 12 days).
  3. The diagnosis is MODELED on a provided flawed draft first, then handed to the student as a fixed
     checklist ("did I name who? did I tie it to the claim with a hinge?"), never a blank "diagnose it."
  4. No mark-the-source instruction, no reference to the student's prior work, no ambiguous referents.

Binds ONLY lesson-pool stimuli (contamination-free):
  - stimulus  ACC-W910-INFO-LESSON-WETLANDS (wetlands restoration) -> the source taught and integrated on
  - stimulus  ACC-W910-INFO-LESSON-HIGHWAYS (interstate highways)  -> the bank-partitioned transfer source
The INDEPENDENT production is an AUTHORED production_frq on wetlands (no test-pool item bound), scored on
rc.staar. Mnemonic PROVE (established-caveat: verify before K-8 reuse). Runs the QC harness on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report

LESSON = Lesson(
    id="ACC-W910-L-T3-EVIDENCE-0001", grade="9-10", lesson_type=3,
    unit="G10 U2 - Source-based argument (evidence-integration)",
    title="Integrate the Evidence: No Quote Stands Alone (PROVE)",
    target=("Integrate a source quote so it never stands alone: name who said it (an attributive tag) plus a "
            "because/but/so hinge that ties the fact to the claim. Trait: Evidence/Development."),
    acc_tags=["ACC.W.SRC.1", "ACC.W.ARG.2", "CCSS.W.9-10.1"],
    provenance={"copyright": "own_authored", "authored": "2026-07-08",
                "mnemonic_status": "established-caveat",
                "council": "Judge-adjudicated: SRSD shell + PROVE as named, modeled, self-checked strategy; "
                           "TSIS frame-the-quotation + attributive-tag definition; TWR sentence-combining "
                           "(because/but/so hinge, appositive) as the joining moves; DI define-before-use + "
                           "integrated-vs-dropped minimal pairs; KH worked->completion->independent fade. "
                           "Async clean labeled model (SRSD live effect size NOT claimed for async)."},
    fade_ledger_moves=["attributive-tag", "because/but/so", "sentence-combining"],
    slots=[
        # ================= TEACH: define the move + define every technical term before use =================
        Slot("TEACH", "teach_card", "What integrating a quote means (and what a dropped quote costs you)",
             body=("When you use a source in an argument, the quote or figure cannot speak for itself. A dropped "
                   "quote is a quotation dropped into your paragraph with no lead-in and no follow-up, as if the "
                   "words explained themselves. They do not: the reader is left guessing who said it and why it "
                   "matters. Integrating a quote is the opposite move: you frame the quote so it clearly supports "
                   "the point you are making. That point is your claim. The controlling idea is a single sentence "
                   "that states the point your whole paragraph is trying to prove; the words claim and controlling "
                   "idea mean the same thing here. Everything else, including your evidence, exists to back it up. "
                   "On state writing rubrics, evidence that is merely present but not explained sits in the middle "
                   "band, while evidence that is named and tied to the claim earns the top band for the "
                   "Evidence and Development trait. Our cue for the integration move is PROVE. Goal for today: use "
                   "a source quote so that no quote ever stands alone.")),
        Slot("TEACH", "teach_card", "The PROVE strategy, letter by letter, with the terms defined",
             body=("PROVE is how you build integrated evidence from one source. Each letter has one job. "
                   "P = Point: state the claim first, the point this evidence will support. "
                   "R = Reference: attribute and cite the source. This is where you use an attributive tag. An "
                   "attributive tag is a short phrase that names who said something, such as 'According to the "
                   "EPA' or 'The U.S. Geological Survey reports.' A fancier way to name the source is an "
                   "appositive. An appositive is a noun phrase, set off with commas, that renames the noun beside "
                   "it, as in 'the EPA, the nation's environmental agency, reports.' Right: 'According to the "
                   "EPA...'. Wrong (bare figure, no source): 'Wetlands once stored 60 days of floodwater,' which "
                   "never says who reported it. "
                   "O = Observe: explain in your own words what the quote or figure shows. "
                   "V = Verify: tie the evidence back to the claim with a because/but/so hinge. A because/but/so "
                   "hinge is a joining word (because, but, or so) that links the evidence to your point, as in "
                   "'..., which matters because towns downstream now get far less warning.' "
                   "E = Extend: say why it matters beyond this one fact, the so-what. "
                   "Your goal: evidence where the source is named (an attributive tag) and the fact is tied to the "
                   "claim (a because/but/so hinge), so no quote stands alone.")),
        Slot("TEACH", "stimulus_display", "Read the source on wetlands",
             ref="ACC-W910-INFO-LESSON-WETLANDS", bank="wetlands_restoration",
             body=("Read the source about wetlands and wetland restoration. As you read, note one fact you could "
                   "use as evidence in an argument, and note who the source says reported it (the EPA or the "
                   "U.S. Geological Survey). You will use one of these facts to practice integrating evidence. The "
                   "article stays on screen while you work.")),
        Slot("TEACH", "discrimination", "Who reported it? (builds R, the Reference move)",
             ref="", labeled_grade_c=True, bank="wetlands_restoration",
             body=("Match the figure to who reported it, the first half of the Reference move. This is a labeled "
                   "Grade-C discriminate-before-produce step. Which figure does the source attribute to the "
                   "U.S. Geological Survey (not the EPA)? "
                   "(A) more than one-third of the nation's threatened and endangered species live only in "
                   "wetlands  "
                   "(B) one Mississippi River stretch went from storing at least 60 days of floodwater to only 12  "
                   "(C) the lower 48 states fell from about 221 million acres of wetlands to about 103 million by "
                   "the mid-1980s  "
                   "(D) a healthy wetland works like a giant sponge. "
                   "Correct: C. The source credits the 221-million-to-103-million acreage figures to the "
                   "U.S. Geological Survey. Options A and B are attributed to the EPA, and D is the source's own "
                   "comparison, not a cited figure. Naming the right source is the R, Reference, in PROVE.")),

        # ================= MODEL: clean annotated before/after (all five PROVE letters) + predict-the-fix ====
        Slot("MODEL", "annotated_before_after", "Watch a dropped quote become integrated (PROVE letters labeled)",
             bank="wetlands_restoration",
             body=("BEFORE (drops the move, do NOT copy this): 'Wetlands stop floods. \"Along part of the "
                   "Mississippi River, natural wetlands once stored at least 60 days of floodwater. After most "
                   "were filled or drained, the same stretch could store only 12 days.\" This proves my point.' "
                   "Why it is weak: the quote is dropped between two sentences. No attributive tag names who "
                   "reported the figures, nothing explains what the drop from 60 to 12 shows, and 'This proves my "
                   "point' never says what the point is. "
                   "AFTER (integrated; each PROVE letter is labeled): 'Draining wetlands strips away a region's "
                   "natural flood protection [P: the claim]. According to the EPA [R: who], one stretch of the "
                   "Mississippi River once held wetlands that could store at least 60 days of floodwater, but "
                   "after most were drained the same stretch could store only 12 [R: what]. That collapse from 60 "
                   "days to 12 shows the land lost most of its power to soak up and slowly release floodwater "
                   "[O: what it shows], which matters because towns downstream that once had two months of buffer "
                   "now have less than two weeks [V: tied to the claim with a because-hinge]. Protecting the "
                   "wetlands that remain is one of the cheapest forms of flood insurance a community has "
                   "[E: the so-what].' "
                   "Read the labels: the claim sentence is [P]; 'According to the EPA' is the attributive tag "
                   "[R: who]; the 60-and-12 figures are [R: what]; the 'shows' sentence is [O]; the because-hinge "
                   "is [V]; the so-what is [E]. The AFTER version never leaves the quote alone: an attributive tag "
                   "introduces it and a because-hinge follows it.")),
        Slot("MODEL", "predict_the_fix", "Predict the one fix this draft needs",
             bank="wetlands_restoration",
             body=("Diagnose this draft before we reveal the fix. Which single move would most improve it? "
                   "Draft: 'Wetlands protect rare animals. \"More than one-third of the nation's threatened and "
                   "endangered species live only in wetlands.\" So we should restore them.' "
                   "(A) add an attributive tag (name who reported it) and a because/but/so hinge that ties the "
                   "figure to the claim  "
                   "(B) add a second quote  "
                   "(C) make the sentences longer  "
                   "(D) move the quote to the end of the paragraph"),
             feedback=("The strongest fix is A. The figure is dropped: no one is named as its source, and nothing "
                       "links it to the claim. Naming the source (for example, 'The EPA reports...') and adding a "
                       "because-hinge (it matters because losing wetlands would leave those species with nowhere "
                       "else to live) turns a bare figure into developed evidence. Those are the Reference and "
                       "Verify moves in PROVE. A second quote (B) or a longer sentence (C) does not integrate the "
                       "first one, and moving the quote (D) leaves it standing alone in a new spot.")),

        # ================= SUPPORTED: integrated-vs-dropped discrimination -> completion frame (fade rung 1) ==
        Slot("SUPPORTED", "discrimination", "Integrated vs dropped (minimal pair, mastery gate)",
             ref="", labeled_grade_c=True, bank="wetlands_restoration",
             body=("Discriminate before you produce (a labeled Grade-C design bet we are testing, not a proven "
                   "law). All four drafts use a real wetlands figure. Pick the one that INTEGRATES its evidence, "
                   "with an attributive tag AND a because/but/so hinge that ties the figure to a claim, so no "
                   "quote stands alone. "
                   "(A) 'Wetlands are disappearing fast. \"The lower 48 states once held about 221 million acres "
                   "of wetlands but had only about 103 million left by the mid-1980s.\" We should act.'  "
                   "(B) 'The U.S. Geological Survey reports that the lower 48 states once held about 221 million "
                   "acres of wetlands but had only about 103 million left by the mid-1980s, which matters because "
                   "draining more than half of a flood-absorbing landscape leaves nearby towns far more exposed "
                   "to flooding.'  "
                   "(C) 'Wetlands cover about 221 million acres. That is a lot of land, so wetlands are big.'  "
                   "(D) 'According to the U.S. Geological Survey, the lower 48 states once held about 221 million "
                   "acres of wetlands and only about 103 million by the mid-1980s.' "
                   "Correct: B. Only B does both moves: it names the source (an attributive tag) AND adds a "
                   "because-hinge that tells the reader why the number matters to a claim. Option A drops the "
                   "quote in with no lead-in and no follow-up. Option C names no source and its so-what is empty. "
                   "Option D attributes the figure but stops there, with no hinge tying it to a claim, so the "
                   "evidence still does no work.")),
        Slot("SUPPORTED", "production_frq", "Completion: fill the PROVE frame (fade rung 1)",
             ref="", bank="wetlands_restoration", rubric_ref="rc.staar", scored=True, unit="sentence",
             body=("Guided practice with the frame provided. Using ONE fact from the wetlands source, fill in each "
                   "blank, then read your sentences back as one integrated piece of evidence. "
                   "P (point): 'Wetlands are worth protecting because ____.' "
                   "R (reference, attributive tag): 'According to ____, ____' (state the fact in the source's "
                   "words or numbers). "
                   "V (verify, because/but/so hinge): '..., which matters because ____.' "
                   "Product goal: the source is named with an attributive tag, the fact is stated accurately, and "
                   "a because/but/so hinge ties the fact to the claim, so no quote stands alone. Scored on "
                   "Evidence/Development.")),
        Slot("MODEL", "diagnosis_frq", "Diagnose a flawed draft with the PROVE checklist (modeled, then you)",
             ref="", bank="wetlands_restoration", scored=True,
             body=("First, watch the PROVE check run on a flawed draft, then run the same checklist yourself. "
                   "Flawed draft: 'Wetlands help endangered animals. \"More than one-third of the nation's "
                   "threatened and endangered species live only in wetlands.\" We should save them.' "
                   "Step 1, R (Reference): does an attributive tag name who reported it? No, the figure is dropped "
                   "in with no source named, so the repair frame is 'According to ____, ...'. "
                   "Step 2, V (Verify): is there a because/but/so hinge tying the figure to the claim? No, the "
                   "draft jumps straight to 'We should save them,' so add one: '..., which matters because ____.' "
                   "Step 3, O and E (Observe and Extend): does it explain what the figure shows and why it matters "
                   "beyond itself? No. "
                   "Now you: write ONE corrected sentence that integrates that same one-third figure, then run "
                   "this checklist on the sentence you just wrote. Did I name who reported it (an attributive "
                   "tag)? Did I tie the figure to a claim with a because/but/so hinge? If you answer No to either, "
                   "use a repair frame above and rewrite before you submit. Scored on Evidence/Development.")),

        # ================= INDEPENDENT: full paragraph, AUTHORED production_frq (no test-pool item bound) ====
        Slot("INDEPENDENT", "production_frq", "Develop a full evidence paragraph on the wetlands source",
             ref="", bank="wetlands_restoration", rubric_ref="rc.staar", scored=True, unit="paragraph",
             body=("Independent performance: using the wetlands source, write a paragraph that (1) states a clear "
                   "claim (a controlling idea) about why wetlands are worth protecting or restoring, and (2) "
                   "develops it with at least one fully integrated piece of source evidence. Integrated means: "
                   "name who reported the fact (an attributive tag) and tie the fact to your claim with a "
                   "because/but/so hinge. Do not let any quote or figure stand alone. Product goal, all required: "
                   "a stated claim; one source fact quoted or paraphrased accurately; an attributive tag naming "
                   "the source; a because/but/so hinge that explains why the fact supports the claim; and a "
                   "closing so-what sentence. Before you submit, run this self-check on the paragraph in the box: "
                   "did I name who reported every fact? Does every fact connect to my claim with a because/but/so "
                   "hinge instead of just sitting there? If No, add the missing move. Scored on "
                   "Evidence/Development.")),

        # ================= TRANSFER: same move, bank-partitioned content (interstate highways) ===============
        Slot("TRANSFER", "production_frq", "Integrate evidence into a paragraph on a NEW topic (bank-partitioned)",
             ref="ACC-W910-INFO-LESSON-HIGHWAYS", bank="interstate_highways", rubric_ref="rc.ohio", scored=True,
             unit="paragraph",
             body=("Transfer: do the same integration move on a source you have not practiced on, at the full "
                   "paragraph you reached in the last step. Read the interstate highways article, then write a "
                   "paragraph that states a claim about the highway system and develops it with at least one "
                   "fully integrated source fact. Pick a real figure, for example that the network runs about "
                   "48,890 miles, or that about one quarter of all the miles driven in the country happen on it, "
                   "or that the federal government paid 90 percent of the construction cost. Integrate it: name "
                   "who reported the figure with an attributive tag (for example, 'The Federal Highway "
                   "Administration reports...'), and tie the figure to your claim with a because/but/so hinge "
                   "(for example, '..., which matters because...'). Do not let any figure stand alone. Product "
                   "goal, all required: a stated claim; one accurately reported source fact; an attributive tag; "
                   "a because/but/so hinge tying the fact to the claim; a closing so-what sentence. Scored on "
                   "Evidence/Development.")),
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
