"""
cr_argument.py  -  G9 constructed-response (CR) ARGUMENT essay prompts for the writing test bank.

Six extended-text argument prompts, each BINDING to one of the four opposing-pair argument stimuli in
the G9 test bucket of Stimulus_Bank_G9. Authored through the proven engine: imports Item/qc_item/qc_report
from pipeline/item_contract.py and runs every item through the same QC harness (schema, acc_tags,
cr_binding, rubric_config, content, no_em_dash) on run.

Prompt variety (gap #22): some prompts emphasize significance / the "so what" of the position; others
push hard on the counterclaim (name the opposing side's strongest point, then answer it).

Stimulus coverage (each of the 4 G9 ARG-OPP stimuli used >=1; the two strongest carry 2 prompts):
  ACC-W910-ARG-OPP-0007  school uniforms       -> 2 prompts (0001, 0005)
  ACC-W910-ARG-OPP-0008  year-round school     -> 1 prompt  (0002)
  ACC-W910-ARG-OPP-0009  voting age lowered 16 -> 2 prompts (0003, 0006)
  ACC-W910-ARG-OPP-0010  zoos good or harm     -> 1 prompt  (0004)
"""
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from item_contract import Item, qc_item, qc_report

ACC = ["ACC.W.ARG.1", "ACC.W.ARG.2", "CCSS.W.9-10.1"]
PROV = {"copyright": "own_authored", "authored": "2026-07-09"}

ITEMS = [
    # ---- 0001: SCHOOL UNIFORMS (counterclaim emphasis) ----------------------------------------------
    Item(
        id="ACC-W910-CR-ARG-0501", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("Weighing both sources, write an argumentative essay stating your position on whether schools "
              "should require students to wear uniforms. Support your claim with specific evidence from both "
              "sources, and directly address at least one objection raised by the side you argue against "
              "before defending your own view."),
        acc_tags=ACC,
        stimulus_ref="ACC-W910-ARG-OPP-0007",
        rubric_ref="rc.ohio",
        provenance=PROV,
    ),
    # ---- 0002: YEAR-ROUND SCHOOL (significance / "so what" emphasis) --------------------------------
    Item(
        id="ACC-W910-CR-ARG-0502", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("Weighing both sources, write an argumentative essay stating your position on whether schools "
              "should switch to a year-round calendar. Support your claim with specific evidence from both "
              "sources, address at least one objection to your position, and explain why the choice matters "
              "for students and their families."),
        acc_tags=ACC,
        stimulus_ref="ACC-W910-ARG-OPP-0008",
        rubric_ref="rc.staar",
        provenance=PROV,
    ),
    # ---- 0003: VOTING AGE LOWERED TO 16 (significance / "so what" emphasis) -------------------------
    Item(
        id="ACC-W910-CR-ARG-0503", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("Weighing both sources, write an argumentative essay stating your position on whether the "
              "voting age should be lowered to 16. Support your claim with specific evidence from both "
              "sources, address at least one objection to your position, and explain why the outcome matters "
              "for how well government represents young people."),
        acc_tags=ACC,
        stimulus_ref="ACC-W910-ARG-OPP-0009",
        rubric_ref="rc.staar",
        provenance=PROV,
    ),
    # ---- 0004: ZOOS (counterclaim emphasis) ---------------------------------------------------------
    Item(
        id="ACC-W910-CR-ARG-0504", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("Weighing both sources, write an argumentative essay stating your position on whether zoos do "
              "more good than harm. Support your claim with evidence from both sources. Name the single "
              "strongest objection the side you disagree with could raise, then answer it and show why your "
              "position still holds."),
        acc_tags=ACC,
        stimulus_ref="ACC-W910-ARG-OPP-0010",
        rubric_ref="rc.ohio",
        provenance=PROV,
    ),
    # ---- 0005: SCHOOL UNIFORMS, second prompt (significance / "so what" emphasis) -------------------
    Item(
        id="ACC-W910-CR-ARG-0505", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("Weighing both sources, write an argumentative essay stating your position on whether schools "
              "should require students to wear uniforms. Support your claim with specific evidence from both "
              "sources, address at least one objection to your position, and explain why the decision matters "
              "for students and their families."),
        acc_tags=ACC,
        stimulus_ref="ACC-W910-ARG-OPP-0007",
        rubric_ref="rc.staar",
        provenance=PROV,
    ),
    # ---- 0006: VOTING AGE LOWERED TO 16, second prompt (counterclaim emphasis) ----------------------
    Item(
        id="ACC-W910-CR-ARG-0506", family="CR", grade="9-10", subskill_or_mode="argument",
        qti_type="extended-text",
        stem=("Weighing both sources, write an argumentative essay stating your position on whether the "
              "voting age should be lowered to 16. Support your claim with evidence from both sources. Then "
              "take on the best argument the opposing side makes, using specific evidence to answer it rather "
              "than simply restating your own view."),
        acc_tags=ACC,
        stimulus_ref="ACC-W910-ARG-OPP-0009",
        rubric_ref="rc.ohio",
        provenance=PROV,
    ),
]

if __name__ == "__main__":
    passed = 0
    for it in ITEMS:
        qc_item(it)
        print(qc_report(it))
        print(f"  -> binds to {it.stimulus_ref} | rubric {it.rubric_ref}")
        print()
        if it.qc["passed"]:
            passed += 1
    print(f"{passed}/{len(ITEMS)} PASS")
    sys.exit(0 if passed == len(ITEMS) else 1)
