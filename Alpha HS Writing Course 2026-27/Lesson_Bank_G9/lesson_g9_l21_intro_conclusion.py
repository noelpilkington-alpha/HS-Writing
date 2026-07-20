"""
lesson_g9_l21_intro_conclusion.py  -  G9 KC C.9.04, ARCHETYPE T7: ESSAY-ASSEMBLY (BUILD, ceiling essay).

G9 course L21 (Unit 4, guided). Introductions and conclusions (B4): frame the thesis with an opening that
orients the reader, and land the upshot with a conclusion that says why it matters (not just a restatement).
Locked L01 template. ESSAY-TIER binds full sources. Taught: SCHOOLLUNCH (full) -> transfer: PHOTOSYNTHESIS
(full, partitioned). rc.staar, unit="multi_paragraph". BUILD=proposal. No coping-model persona; no source
markup; no prior-work ref; no em dashes. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report

BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> an intro that stalls and a conclusion that just repeats</span>'
    '<p style="margin:8px 0 0;font-size:15px"><i>Intro:</i> This essay is about free school meals. A lot of '
    'schools already have them. In this essay I will talk about free meals and give some reasons why they are a '
    'good idea. <i>Conclusion:</i> In conclusion, schools should offer free meals to all students. Like I said '
    'above, free meals are a good idea and they help students, so that is why schools should have them.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">The intro announces the topic and promises to "talk '
    'about it," but it frames no thesis; the conclusion repeats the claim in new words and adds no upshot. '
    'Neither paragraph does real work.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> an intro that frames the thesis, a conclusion that lands the upshot</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">INTRO frames the thesis</span> "For a student who comes to school with an empty stomach, '
      'lunch is not a small thing; it is whether the afternoon is a class or a countdown to the next meal. '
      'Because hunger and focus cannot share one desk, schools should offer free meals to every student, no '
      'matter what a family earns." '
      '<span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">CONCLUSION lands the upshot</span> "Free meals are not a handout to families who could '
      'pay; they are a way to keep any student from being too hungry to learn or from being marked as poor at '
      'the lunch line. A school that feeds every student removes one real barrier between a child and a fair '
      'chance to succeed."</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Same topic, but the intro orients the reader and '
    'states the thesis, and the conclusion says why the argument matters instead of repeating it. Framing the '
    'thesis and landing the upshot are the moves.</p>'
  '</div>'
'</div>')

LESSON = Lesson(
    id="ACC-W910-L-G9-C904-0021", grade="9-10", lesson_type=7,
    unit="G9 U4 - Build essay (introductions and conclusions)",
    title="Frame the Thesis, Land the Upshot",
    target=("Write an introduction that orients the reader and states the thesis, and a conclusion that lands "
            "the upshot (why it matters) instead of just repeating the claim. Written across an essay. Trait: "
            "Organization."),
    acc_tags=["ACC.W.INFO.5", "CCSS.W.9-10.2a"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12",
                "mnemonic_status": "proposal", "kc": "C.9.04", "sot": "icm course-G9.md L21",
                "taught_stimulus": "ACC-W910-ARG-LESSON-SCHOOLLUNCH",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-PHOTOSYNTHESIS",
                "playbook": "_phase2/playbook_T7_BUILD.md",
                "template": "locked L01 template; ESSAY-TIER binds full sources.",
                "council": ("T7/BUILD framing rung: introduces B4 introductions and conclusions (intro frames "
                            "the thesis; conclusion lands the upshot, not a restatement). frames-vs-stalls / "
                            "lands-vs-repeats discrimination labeled Grade-C. BUILD=proposal; unit=multi_paragraph.")},
    fade_ledger_moves=["intro-frames-the-thesis", "conclusion-lands-the-upshot"],
    slots=[
        Slot("TEACH", "teach_card", "Openings orient, endings land the upshot",
             body=("An essay's first and last paragraphs have real jobs, not filler. The INTRODUCTION orients "
                   "the reader and states the thesis: a sentence or two that sets up why the topic matters, "
                   "then the thesis itself. It does not announce 'this essay is about X, I will talk about it,' "
                   "which stalls and frames nothing. The CONCLUSION lands the upshot: it says why the argument "
                   "matters, what follows from it, instead of repeating the thesis in new words. 'In "
                   "conclusion, free meals are good, like I said' does no work. A conclusion that lands says "
                   "something like 'feeding every student is a condition for learning, not charity.' The trap "
                   "is a stalling intro and a repeating conclusion, the two weakest habits in student essays. "
                   "Goal today: write an intro that frames the thesis and a conclusion that lands the upshot.")),
        Slot("TEACH", "stimulus_display", "Read the source: free school meals",
             ref="ACC-W910-ARG-LESSON-SCHOOLLUNCH", bank="school_lunch",
             body=("Read this source about free school meals. Because your job is to FRAME an essay, read the "
                   "whole thing and think about why this issue matters (for the intro) and what follows from "
                   "the argument (for the conclusion). The text stays on screen while you work.")),
        Slot("TEACH", "discrimination", "Which conclusion lands the upshot?",
             ref="", labeled_grade_c=True, bank="school_lunch",
             body=("Sort these before you write (spotting the target first, a Grade-C design bet we label as a "
                   "bet, not a proven ingredient). The thesis was 'Schools should offer free meals to all "
                   "students.' Which conclusion LANDS the upshot rather than just repeating? "
                   "(A) In conclusion, as I explained above, schools should offer free meals to all students, because the reasons I already gave show that free meals help students.  "
                   "(B) Feeding every student is not charity but a condition for learning: a school that "
                   "removes hunger removes one real barrier between a child and a fair chance. "
                   "Correct: B. (A) restates the thesis and adds nothing, so the reader gains nothing from it. "
                   "(B) says why the argument matters and what follows from it (hunger as a barrier to a fair "
                   "chance). Landing the upshot is the move.")),
        Slot("MODEL", "annotated_before_after", "Watch a stalling frame become a working one",
             bank="school_lunch",
             body=("Here is a stalling intro and repeating conclusion being rebuilt to do real work. Read the "
                   "BEFORE, then the AFTER, and notice the intro now frames the thesis and the conclusion lands "
                   "the upshot." + BEFORE_AFTER_HTML +
                   " The BEFORE announces and repeats. The AFTER orients the reader to the thesis and ends on "
                   "why it matters. Framing and landing are the moves.")),
        Slot("MODEL", "predict_the_fix", "What does this conclusion most need?",
             bank="school_lunch",
             body=("Diagnose before the reveal. An essay ends: 'In conclusion, free school meals help students, "
                   "so schools should offer them. That is what I argued.' Which single change would most "
                   "improve the conclusion? "
                   "(A) replace the restatement with an upshot, why the argument matters or what follows from it  "
                   "(B) add one more fact about school meals, like how many students eat lunch at school each day  "
                   "(C) make it two sentences longer by restating the main reasons from the body paragraphs  "
                   "(D) start it with 'To sum up' instead of 'In conclusion' so it sounds more formal and polished"),
             feedback=("Correct: A. The conclusion just repeats the thesis ('help students, so offer them, that "
                       "is what I argued'), so it does no work. The fix is an upshot: say why it matters (for "
                       "example, that removing hunger removes a barrier to learning) or what follows. Another "
                       "fact (B), more length (C), or a different opener phrase (D) do not turn a restatement "
                       "into an upshot.")),
        Slot("SUPPORTED", "production_frq", "Write a framing intro",
             ref="", bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=("Write an INTRODUCTION for an essay arguing that schools should offer free meals to all "
                   "students. Goal: one or two sentences that orient the reader to why the issue matters, then "
                   "the thesis. Do not announce 'this essay is about ...'; frame the thesis instead. Write the "
                   "intro. Scored on Organization.")),
        Slot("MODEL", "diagnosis_frq", "Check an intro and conclusion for their jobs",
             ref="", bank="school_lunch", scored=True,
             body=("First watch the check run on a provided draft, then run it on a fresh conclusion of your "
                   "own. Provided intro: 'This essay will discuss free school meals and give reasons.' "
                   "Provided conclusion: 'In conclusion, free meals are a good idea.' Run the check step by "
                   "step. Intro: does it FRAME the thesis (orient + state it)? No, it announces the topic, so "
                   "rewrite it to set up and state the thesis. Conclusion: does it LAND an upshot? No, it "
                   "repeats, so add why it matters. Now you: write a fresh conclusion for the free-meals essay, "
                   "then check it, does it land an upshot rather than repeat? Fix it if not. Finish by naming "
                   "the upshot your conclusion delivers.")),
        Slot("INDEPENDENT", "production_frq", "Write an intro and a conclusion",
             ref="", bank="school_lunch", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=("On your own now. For an essay arguing that schools should offer free meals to all students, "
                   "write BOTH an INTRODUCTION that frames the thesis (orient the reader, then state it) and a "
                   "CONCLUSION that lands the upshot (why it matters or what follows), not a restatement. Before "
                   "you submit, check: does the intro frame the thesis rather than announce the topic, and does "
                   "the conclusion land an upshot rather than repeat? Fix any that fail before you submit. "
                   "Scored on Organization.")),
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: photosynthesis",
             ref="ACC-W910-INFO-LESSON-PHOTOSYNTHESIS", bank="photosynthesis",
             body=("Read this new source about photosynthesis. Because your job is to FRAME an essay, read the "
                   "whole thing and think about why the topic matters (for the intro) and what the reader "
                   "should take away (for the conclusion). This is an explain task, so the thesis sets a focus "
                   "and takes no side. The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Write an intro and conclusion on a NEW topic",
             ref="", bank="photosynthesis", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=("New topic. For an essay explaining how photosynthesis turns light into food, write an "
                   "INTRODUCTION that frames the thesis, a focusing idea that takes no side (orient the reader, "
                   "then state it), and a "
                   "CONCLUSION that lands the upshot (why understanding it matters), not a restatement. Same "
                   "framing-and-landing move as the meals essay, new topic. Scored on Organization.")),
    ],
)

LESSONS = [LESSON]

if __name__ == "__main__":
    ok = True
    for L in LESSONS:
        qc_lesson(L); print(qc_report(L)); print(); ok = ok and L.qc["passed"]
    passed = sum(1 for L in LESSONS if L.qc["passed"])
    print(f"{passed}/{len(LESSONS)} PASS")
    sys.exit(0 if ok else 1)
