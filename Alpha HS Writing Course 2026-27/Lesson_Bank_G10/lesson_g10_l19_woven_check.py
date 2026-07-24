"""
lesson_g10_l19_woven_check.py  -  G10 KC C.10.06, ARCHETYPE T8: CROSS-SOURCE-SYNTHESIS (WEAVE, ceiling essay). V3.1.

G10 course L19 (Unit 4). Teaching point (KEPT): judge whether a multi-source paragraph WEAVES the sources into
one point or LISTS them source-by-source, predict its score, see the reveal, then revise a source-by-source
paragraph into woven synthesis (both sources serving X1/X2 + O1). Trait: Development (use of sources).

Rebuilt to the v3.1 build spine (hand-authored, matching the G9 L23 v3.1 pattern):
  1. TEACH = a ONE_IDEA teal callout (synthesis = weave, not cover) + the two paragraph shapes as a real <ul>,
     then the check routine as a real <ol> (no wall of text -> format_fidelity).
  2. MODEL = a coping-model think-aloud (first try -> run the check -> catch -> final) with a literal BEFORE and
     AFTER block, then the reusable 3-question check folded in as a dashed REMEMBER box.
  3. DISCRIMINATION via explicit choices=[]; the leaked "Grade-C design bet" label is GONE from student text
     (labeled_grade_c stays True in code only); the reveal is in a "Correct: A ..." tail, not in an option.
  4. Deterministic FRQ + diagnosis prompts via frq_prompt/setapart/checklist (no "Step 1/2" prose, no
     "Scored on ..." chrome).

Preserved EXACTLY: id="ACC-W910-L-G10-C1006-0019", lesson_type=8, kc="C.10.06", mnemonic_status="proposal",
unit, the bound stimuli (WEATHER taught -> RECYCLING transfer), and every production_frq unit=multi_paragraph.
Own words, faithful to the bound federal sources, no fabricated figures, no em dashes. Passes all 23 gates +
render-qc. Runs QC on execution.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from lesson_contract import Lesson, Slot, qc_lesson, qc_report
from lesson_prompts import frq_prompt, setapart, checklist

ONE_IDEA = (
'<div style="border-left:4px solid #0d9488;background:#ecfdf5;border-radius:8px;padding:10px 14px;margin:8px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">The one idea</div>'
'<div style="color:#0f2f28;font-size:15px;margin-top:2px">To <strong>synthesize</strong> means to combine two or '
'more sources into <strong>one point</strong>. The single line that decides a synthesis score is <strong>woven '
'vs source-by-source</strong>. A paragraph can quote both sources accurately and still be a list.</div></div>')

REMEMBER = (
'<div style="border:1px dashed #0d9488;border-radius:8px;padding:10px 14px;margin:8px 0;background:#f8fffd;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
'<div style="font-size:11px;font-weight:700;letter-spacing:.05em;color:#0f766e;text-transform:uppercase">Your check tool: woven or listed?</div>'
'<div style="color:#1f2a44;font-size:14px;margin:4px 0 0">Before you submit, reread the paragraph and ask:</div>'
'<ol style="color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px">'
'<li style="margin:2px 0">Is there ONE point that both sources build together?</li>'
'<li style="margin:2px 0">Are the two sources connected in the same sentences, not reported in separate blocks?</li>'
'<li style="margin:2px 0">If you deleted one source, would the point fall apart? If not, they are only listed.</li></ol>'
'<div style="color:#0f766e;font-size:13px;margin-top:6px">If any answer is no, weave them before you submit.</div></div>')

# coping-model before/after: a source-by-source weather paragraph is drafted, checked, caught, and rebuilt into
# woven synthesis. Contains BOTH a literal BEFORE and AFTER (content_depth). Faithful to the NWS source (balloons
# read the upper air; local offices correct the models). No named person (Timeback stateless rule).
BEFORE_AFTER_HTML = (
'<div style="border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;margin:6px 0;'
'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">'
  '<div style="background:#fef2f2;padding:12px 14px;border-bottom:1px solid #fecaca">'
    '<span style="display:inline-block;background:#dc2626;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">BEFORE</span>'
    '<span style="color:#991b1b;font-size:13px;font-weight:600"> source-by-source: a block per source</span>'
    '<p style="margin:8px 0 0;font-size:15px">Source A explains that forecasters launch weather balloons to '
    'read the upper air. Source B explains that local offices adjust the computer models. Both sources are '
    'about making a forecast.</p>'
    '<p style="margin:6px 0 0;color:#991b1b;font-size:13px">Two separate reports with no shared point. It reads '
    'like a list of what each source says, not one idea built from both.</p>'
  '</div>'
  '<div style="background:#f0fdf4;padding:12px 14px">'
    '<span style="display:inline-block;background:#15803d;color:#fff;font-size:11px;font-weight:700;'
    'padding:2px 8px;border-radius:4px">AFTER</span>'
    '<span style="color:#166534;font-size:13px;font-weight:600"> woven: both sources build one point</span>'
    '<p style="margin:8px 0 0;font-size:15px">'
      '<span style="background:#dbeafe;color:#1e3a8a;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">ONE POINT</span> A forecast is reliable because measurement and judgment work as one '
      'chain: '
      '<span style="background:#fef9c3;color:#854d0e;padding:1px 6px;border-radius:3px;font-size:11px;'
      'font-weight:700">A + B WOVEN</span> the upper-air readings Source A describes give the models their '
      'starting numbers, and the local forecasters Source B describes correct those models against what they '
      'see, so raw data becomes a forecast people can trust.</p>'
    '<p style="margin:6px 0 0;color:#166534;font-size:13px">Both sources now serve ONE point, connected in the '
    'same sentences. Revising the list into woven synthesis is the fix.</p>'
  '</div>'
'</div>')


LESSON = Lesson(
    id="ACC-W910-L-G10-C1006-0019", grade="9-10", lesson_type=8,
    unit="G10 U4 - Cross-text synthesis (woven vs source-by-source check)",
    title="Check It: Woven Synthesis or Source-by-Source?",
    target=("Judge whether a multi-source paragraph weaves the sources into one point or lists them "
            "source-by-source, predict its score, see the reveal, then revise a listed paragraph into woven "
            "synthesis. Written across a multi-source paragraph. Trait: Development (use of sources)."),
    acc_tags=["ACC.W.SRC.1", "CCSS.W.9-10.7", "CCSS.W.9-10.8"],
    provenance={"copyright": "own_authored", "authored": "2026-07-12", "revised": "2026-07-15",
                "mnemonic_status": "proposal", "kc": "C.10.06", "sot": "icm course-G10.md L19",
                "taught_stimulus": "ACC-W910-INFO-LESSON-WEATHER",
                "transfer_stimulus": "ACC-W910-INFO-LESSON-RECYCLING",
                "playbook": "_phase2/playbook_T8_WEAVE.md",
                "template": "v3.1 spine; SYNTHESIS-TIER binds full sources for context (provided paragraphs are the material).",
                "one_idea": "Synthesis = weaving sources into ONE point, not covering both. Woven vs source-by-source is the line.",
                "one_reminder": "Woven-or-listed check: one shared point? sources connected in the same sentences? point falls apart if one source is cut?",
                "version_note": ("V3.1 rebuild of L19. FIXED the two failing gates on the prior version: removed "
                                 "the leaked internal label ('a Grade-C design bet we label as a bet') from the "
                                 "discrimination and moved the options to explicit choices=[]; broke the two "
                                 "wall-of-text teach cards into a ONE_IDEA callout + real <ul>/<ol> lists "
                                 "(format_fidelity). Coping-model before/after kept with the 3-question check "
                                 "folded in as a REMEMBER box; deterministic frq_prompt/setapart/checklist bodies "
                                 "(no 'Step 1/2' prose, no 'Scored on' chrome). Preserved id, type 8, kc C.10.06, "
                                 "mnemonic_status=proposal, bound stimuli, and every production unit=multi_paragraph."),
                "council": ("T8/WEAVE synthesis capstone: calibrate on woven-vs-source-by-source (the synthesis "
                            "signature error) via discrimination + predict-the-fix, then revise a listed "
                            "paragraph into woven synthesis (X1/X2). WEAVE=proposal; unit=multi_paragraph."),
                "review_provenance": "built to the G9 L23 v3.1 pattern; 23 gates + render-qc clean"},
    fade_ledger_moves=["calibrate-woven-vs-source-by-source", "revise-list-into-synthesis"],
    slots=[
        # ===== TEACH: the one idea + the two shapes (as a list), then the check routine (as a list) =====
        Slot("TEACH", "teach_card", "The synthesis line: woven vs source-by-source",
             body=(ONE_IDEA +
                   "Every multi-source paragraph is one of two shapes. Learn to tell them apart at a glance:"
                   "<ul style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>Woven</strong>: two or more sources are used TOGETHER to "
                   "build one point, connected in the same sentences. Cut one source and the point falls apart.</li>"
                   "<li style=\"margin:4px 0\"><strong>Source-by-source</strong>: each source gets its own "
                   "separate block, a summary of A, then a summary of B, with no shared point, so it reads like a "
                   "list, not an argument.</li></ul>"
                   "In each practice paragraph below, the two sources are handed to you as short findings quoted "
                   "right inside the paragraph and labeled Source A and Source B, so everything you need to weave "
                   "them is on the page. There is no separate text to open; you work with the two findings in "
                   "front of you. "
                   "The trap is that a clean list looks finished. A paragraph can name both sources and quote "
                   "them accurately and still be source-by-source, because covering both sources is not the same "
                   "as weaving them.")),
        Slot("TEACH", "teach_card", "The routine: check, predict, reveal, revise",
             body=("Run this routine on every paragraph you judge or write. It trains your eye, because a "
                   "well-written list can pass for synthesis until you commit to a call:"
                   "<ol style=\"color:#1f2a44;font-size:14px;margin:6px 0 0;padding-left:22px\">"
                   "<li style=\"margin:4px 0\"><strong>CHECK</strong>: are the sources woven into one point, or "
                   "listed in turn?</li>"
                   "<li style=\"margin:4px 0\"><strong>PREDICT</strong>: call it woven or source-by-source before "
                   "you look, and predict how high it scores.</li>"
                   "<li style=\"margin:4px 0\"><strong>REVEAL</strong>: read the real judgment and why, and "
                   "notice the gap between your call and the truth.</li>"
                   "<li style=\"margin:4px 0\"><strong>REVISE</strong>: turn a source-by-source paragraph into "
                   "woven synthesis by finding the shared point and connecting the sources on it.</li></ol>"
                   "Predicting first is what exposes the gap between 'covers both sources' and 'weaves them.'")),
        Slot("TEACH", "stimulus_display", "Read the source: how a weather forecast is made (context)",
             ref="ACC-W910-INFO-LESSON-WEATHER", bank="weather",
             body=("For this check you will judge and revise multi-source paragraphs. Read this explanatory "
                   "source so the topic material is familiar; the paragraphs you work on combine points like "
                   "these (how forecasters gather data, turn it into a forecast, and warn the public). The text "
                   "stays on screen while you work.")),

        # ===== MODEL (before the quiz): coping-model think-aloud before/after + check tool, then the items =====
        Slot("MODEL", "annotated_before_after", "Watch a source-by-source paragraph become woven",
             bank="weather",
             body=("Here is a writer thinking aloud. The two sources are the findings quoted inside the "
                   "paragraph, labeled Source A and Source B; there is no separate text to open. First try, they "
                   "draft a paragraph that names both sources. Then they run the check, catch that the sources "
                   "are only listed, and revise. Read the BEFORE, then the AFTER." + BEFORE_AFTER_HTML +
                   " The BEFORE lists two separate reports about forecasting. The Final version connects them on "
                   "one point (measurement feeds judgment, so the forecast can be trusted). Revising a list into "
                   "woven synthesis is the move." + REMEMBER +
                   "Run this same check on every paragraph you judge below and on every one you write.")),
        Slot("MODEL", "discrimination", "Which paragraph weaves the sources?",
             ref="", labeled_grade_c=True, bank="weather",
             body=("You have watched a list become woven. Now spot the target: which paragraph WEAVES two sources "
                   "into one point, and which three do not? "
                   "(A) The upper-air readings Source A describes feed the models, while the forecasters Source B "
                   "describes correct those models, so measurement and judgment build one reliable forecast.  "
                   "(B) Source A explains that forecasters launch weather balloons to read the upper air, and "
                   "Source B explains that local offices adjust the computer models before release, and both "
                   "sources accurately describe separate steps in the forecasting process.  "
                   "(C) Source A reports that Doppler radar detects storms as they move. Source B reports that "
                   "river centers predict when rivers will rise. Each source covers one kind of work the agency does.  "
                   "(D) Source A shows the upper-air readings give the models their starting data, so measurement "
                   "is what makes the forecast reliable. Source B is named at the end but adds nothing to that point. "
                   "Correct: A. It connects both sources on ONE point (measurement feeding judgment); B and C "
                   "report each source in its own block with no shared point, and D builds a point from Source A "
                   "alone while Source B does no work. Weaving both sources on one point is the move."),
             choices=[
                 {"id": "A",
                  "text": "The upper-air readings Source A describes feed the models, while the forecasters Source B describes correct those models, so measurement and judgment build one reliable forecast.",
                  "correct": True,
                  "why": "Correct. Both sources are connected in the same sentences to build ONE point (measurement feeds judgment), so it is woven."},
                 {"id": "B",
                  "text": "Source A explains that forecasters launch weather balloons to read the upper air, and Source B explains that local offices adjust the computer models before release, and both sources accurately describe separate steps in the forecasting process.",
                  "correct": False,
                  "why": "Source-by-source. It reports each source in its own clause and only says both describe steps, with no shared point tying them together."},
                 {"id": "C",
                  "text": "Source A reports that Doppler radar detects storms as they move. Source B reports that river centers predict when rivers will rise. Each source covers one kind of work the agency does.",
                  "correct": False,
                  "why": "Source-by-source. Two separate reports, one per source, with no single point built from both. Naming both sources is not weaving them."},
                 {"id": "D",
                  "text": "Source A shows the upper-air readings give the models their starting data, so measurement is what makes the forecast reliable. Source B is named at the end but adds nothing to that point.",
                  "correct": False,
                  "why": "Single-source. It builds one point, but only from Source A; Source B is named yet does no work, so the sources are not woven. If you could cut Source B and lose nothing, it is not synthesis."},
             ]),
        Slot("MODEL", "predict_the_fix", "Why does this paragraph score as source-by-source?",
             bank="weather",
             body=("Predict before the reveal. A provided paragraph reads: 'Source 1 gives the cost of a warning "
                   "system. Source 2 gives its benefit. Source 1 has numbers, and Source 2 has examples.' Which "
                   "judgment is correct? "
                   "(A) source-by-source: it reports each source on its own and never ties them to one point  "
                   "(B) woven, because it brings in two different sources instead of relying on only one of them  "
                   "(C) source-by-source, but only because it is too short, and adding a few more sentences to it "
                   "would be enough to make it count as woven synthesis  "
                   "(D) woven, because it names both the cost and the benefit of the system inside a single paragraph"),
             feedback=("Correct: A. The paragraph reports each source separately (cost here, benefit there) and "
                       "never connects them on one point, so it is source-by-source even though it uses two "
                       "sources. Merely using two sources (B) or naming cost and benefit (D) is not weaving; "
                       "length (C) is not the issue. To weave, tie the sources to one point, for example that "
                       "the benefit is what justifies the cost.")),

        # ===== SUPPORTED: revise a listed paragraph into woven synthesis WITH A FRAME (highest-value scaffold) =====
        Slot("SUPPORTED", "production_frq", "Revise a source-by-source paragraph into woven synthesis",
             ref="", bank="weather", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="Revise this source-by-source paragraph so both sources build ONE point, connected in the "
                       "same sentences. The two sources are the two findings given inside the paragraph (Source A "
                       "on gathering data, Source B on adjusting the models); weave those two.",
                 setapart_block=setapart("Source-by-source paragraph to fix:",
                                         "Source A explains that forecasters gather data with balloons and radar. "
                                         "Source B explains that local forecasters adjust the models. Both are "
                                         "about making a forecast.", "red"),
                 checklist_block=setapart("Weave it with this frame:",
                                         "Both sources show that ______ (one point). The ______ Source A "
                                         "describes ______, and the ______ Source B describes ______ so ______."),
                 closer="Rewrite the paragraph using the frame. Goal: woven, not a list. Then run the "
                        "woven-or-listed check and fix any answer that is no.")),
        # COUNCIL FIX (2026-07-24): Option A (later-in-arc), watch-then-do: demo preserved, produce is the graded
        # act. The old diagnosis_frq bundled a watched woven-or-listed demo (pre-answered (q,a) tuple rows) + a
        # fresh two-source paragraph + a run-and-name-the-point tail in one box (unscoreable, wired to no grader,
        # and the (q,a) rows leaked the answers). The coping-model demo is PRESERVED as read-only narration (the
        # three checks shown running on the weak paragraph, in plain declarative prose). The student's ONLY
        # graded act is now the fresh woven paragraph; the three checks sit read-only beneath as plain-string
        # reminders; the run-and-name tail is deleted. Kept as diagnosis_frq (multi_paragraph grain needs an
        # own-draft diagnosis for model_sequence). Stays on the taught source (load balance).
        Slot("MODEL", "diagnosis_frq", "Write a woven multi-source paragraph",
             ref="", bank="weather", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="First, watch the woven-or-listed check run on the weak paragraph below. It reports a "
                       "watch from Source A and a warning from Source B with no shared point tying them; each "
                       "source gets its own sentence, then a soft 'both are about alerts'; and there is no point "
                       "that would fall apart if one source were cut, which is the tell that it is a list. A "
                       "stronger version would build ONE point both sources support, connected in the same "
                       "sentences. Now write a fresh paragraph of your own that weaves them.",
                 setapart_block=setapart("Weak paragraph the check was run on:",
                                         "Source A says the agency issues watches. Source B says the agency "
                                         "issues warnings. Both are about alerts.", "red"),
                 checklist_block=checklist(title="Check your paragraph against these (no need to type answers):", rows=[
                     "Is there ONE point both sources build?",
                     "Are the sources connected in the same sentences?",
                     "Would the point fall apart if one source were cut (the test that it is truly woven)?",
                 ]),
                 closer="Write a fresh two-source paragraph on weather that WEAVES the sources into one point, "
                        "connecting a fact from each in the same sentences so the point rests on both. Run the "
                        "three checks above before you submit.")),

        # ===== INDEPENDENT: revise a listed paragraph with no frame (say-the-standard) =====
        Slot("INDEPENDENT", "production_frq", "Revise a listed paragraph on your own",
             ref="", bank="weather", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="On your own now, no frame.",
                 setapart_block=setapart("Source-by-source paragraph to fix:",
                                         "Source A describes how river centers track rainfall. Source B describes "
                                         "how offices warn the public. Each covers a task.", "red"),
                 closer="Rewrite it so both sources build ONE point, connected in the same sentences. Weaving two "
                        "sources into one point is what every real synthesis paragraph is built on, and you are "
                        "ready to do it cold. Run the woven-or-listed check before you submit and fix any answer "
                        "that is no.")),

        # ===== TRANSFER: same list-into-synthesis move, a NEW source (recycling), partitioned from taught bank =====
        Slot("TRANSFER", "stimulus_display", "Read a NEW source: what happens to what you recycle (context)",
             ref="ACC-W910-INFO-LESSON-RECYCLING", bank="recycling",
             body=("Read this new explanatory source so the topic material is familiar; the paragraph you revise "
                   "combines points like these (how materials recovery works and why contamination threatens it). "
                   "The text stays on screen while you work.")),
        Slot("TRANSFER", "production_frq", "Revise a listed paragraph on a NEW topic",
             ref="", bank="recycling", rubric_ref="rc.staar", scored=True, unit="multi_paragraph",
             body=frq_prompt(
                 intro="New topic. Same list-into-synthesis revision as the weather paragraph. The two sources "
                       "are the two findings given inside the paragraph below (Source A on sorting, Source B on "
                       "remaking); weave those two, there is no separate text to open.",
                 setapart_block=setapart("Source-by-source paragraph to fix:",
                                         "Source A explains how a facility sorts materials. Source B explains how "
                                         "factories remake them into new goods. Both describe recycling.", "red"),
                 closer="Rewrite it so both sources build ONE point, connected in the same sentences (for "
                        "example, that careful sorting is what makes remaking possible). Run the woven-or-listed "
                        "check before you submit.")),
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
