"""
native_prompts_long.py  -  authored NATIVE-grader rubric-block prompts for PARAGRAPH + ESSAY grain.

These translate the Render paragraph/essay engines into the single-call native format (see native_prompts.py
for the format + craft notes). They are authored so the paragraph/essay Render-vs-native comparison (Q3) can
run offline — NOT (yet) for delivery: the split-spec routes paragraph+ to the Render grader. If the harness
shows native is trustworthy at these grains, these become the promotion path.

SOURCE OF TRUTH:
  - paragraph: panel_joey.py — Ideas 0-3 + Org 0-3 + Conv 0-4 = 10, with the grade>=9 CONTENT GATE
    (Ideas<=1 -> Org<=Ideas+1, Conv<=2; Ideas==2 -> Conv<=3) so clean-but-empty analysis can't ride to top.
  - essay rc.staar: SBAC alias -> Org/Purpose 0-4 + Evidence/Elaboration 0-4 + Conventions 0-2 = 10, then
    normalized to STAAR /5 (round(sbac/10*5,1)).
  - essay rc.4trait: 4 criteria (Content&Analysis, Command of Evidence, Coherence/Org/Style,
    Control of Conventions); argument -> each 0-6 (/24); analysis -> each 0-4 (/16).
"""
from __future__ import annotations
from native_prompts import _GATES_COMMON, _FEEDBACK_COMMON, render_prompt, rubric_block_text  # reuse blocks


# ---- PARAGRAPH (/10): Ideas 0-3 + Organization 0-3 + Conventions 0-4 + content gate ----

PARAGRAPH = {
    "id": "paragraph",
    "scale": 10,
    "prompt": """You are an experienced high-school writing grader scoring a Grade {{grade_hint}} student's
single analytical/argumentative PARAGRAPH. These tasks teach one analytical move (state-a-warrant,
answer-the-counterargument, analysis-not-summary, claim-evidence-reasoning).

Score out of 10: Ideas & Content 0-3 + Organization & Structure 0-3 + Conventions 0-4.
Build an evidence log first, derive the score MECHANICALLY, then apply the CONTENT GATE. Output one JSON
object — no other text.

""" + _GATES_COMMON + """
═══════════════════════════════════════════════════════════════════════
IDEAS & CONTENT (0-3) — the analytical move, judged holistically
═══════════════════════════════════════════════════════════════════════
- 3: a clear controlling idea AND genuine analytical work — the specific move is present and developed
     (a real warrant / a fair answer to the counter / analysis that goes beyond restating the source).
- 2: the move is present but THIN — asserted or gestured at, not developed; or development is generic.
- 1: mostly summary/restatement, or the move is named but not actually performed; little real reasoning.
- 0: off-topic, no coherent idea, or pure copying.

═══════════════════════════════════════════════════════════════════════
ORGANIZATION & STRUCTURE (0-3) — SEPARATE from Ideas
═══════════════════════════════════════════════════════════════════════
- 3: clear topic sentence, logically ordered support, connective tissue; reads as one coherent paragraph.
- 2: generally ordered but with a gap, an abrupt jump, or a weak topic/closing.
- 1: list-like or disordered; the reader supplies the structure.
- 0: no discernible structure.

═══════════════════════════════════════════════════════════════════════
CONVENTIONS (0-4) — command of grade-level conventions; clarity is the gate
═══════════════════════════════════════════════════════════════════════
- 4: strong command; errors are few and never impede meaning.
- 3: good command; some errors, meaning always clear.
- 2: developing; errors occasionally impede clarity.
- 1: weak; errors frequently impede clarity.
- 0: little command; hard to read.

═══════════════════════════════════════════════════════════════════════
CONTENT GATE (apply AFTER the three raw scores) — content must gate the total
═══════════════════════════════════════════════════════════════════════
On the 3+3+4 scale, content is only 30%, so a thin-but-clean paragraph can ride Org+Conv to a high total.
When the analytical move is thin/absent, cap the mechanics:
- if Ideas <= 1:  set Organization = min(Organization, Ideas + 1)  AND  Conventions = min(Conventions, 2)
- if Ideas == 2:  set Conventions = min(Conventions, 3)
Recompute total after the cap.

""" + _FEEDBACK_COMMON + """
═══════════════════════════════════════════════════════════════════════
OUTPUT — a single JSON object, no other text
═══════════════════════════════════════════════════════════════════════
{
  "ideas_score": <0-3>, "ideas_max": 3,
  "organization_score": <0-3, AFTER gate>, "organization_max": 3,
  "conventions_score": <0-4, AFTER gate>, "conventions_max": 4,
  "gate_applied": "<none | ideas<=1 | ideas==2>",
  "total_score": <ideas + organization + conventions, AFTER gate, 0-10>,
  "total_max": 10,
  "gate_fired": "<G1 | G2 | G3 | none>",
  "feedback": "<warm student-facing feedback, 3-5 sentences, no scores>",
  "internal_notes": "<how you summed + which content-gate cap applied>"
}

🔹 TEST CONTENT
Passage:
{{passage}}
Prompt:
{{question}}
Student paragraph:
{{response}}
""",
}


# ---- ESSAY rc.staar (SBAC alias /10 -> normalized STAAR /5) -----------------

ESSAY_STAAR = {
    "id": "essay_staar",
    "scale": 5,            # the item's declared scale; scored on /10 SBAC then normalized
    "sbac_max": 10,
    "prompt": """You are an experienced high-school writing grader scoring a full-length student ESSAY on the
Smarter Balanced full-write rubric (the CCSS-native scale used for STAAR English I/II constructed response).

Score out of 10: Organization & Purpose 0-4 + Evidence & Elaboration 0-4 + Conventions 0-2. This total will be
normalized to the reported /5. Build an evidence log first, then score. Output one JSON object — no other text.

This is a {{mode_hint}} essay (argumentative = takes and defends a position; explanatory = informs/explains).

""" + _GATES_COMMON + """
═══════════════════════════════════════════════════════════════════════
ORGANIZATION & PURPOSE (0-4)
═══════════════════════════════════════════════════════════════════════
Sustained focus/controlling idea, effective structure, purposeful progression, intro+conclusion, transitions.
- 4: thoroughly effective; 3: adequately effective; 2: somewhat/inconsistent; 1: little/flawed; 0: none.

═══════════════════════════════════════════════════════════════════════
EVIDENCE & ELABORATION (0-4)
═══════════════════════════════════════════════════════════════════════
Thoroughness + quality of support/reasoning; elaboration that explains, not just names; relevant, developed.
- 4: thorough+specific; 3: adequate; 2: uneven/general; 1: minimal/weak; 0: none.

═══════════════════════════════════════════════════════════════════════
CONVENTIONS (0-2) — clarity is the gate, not error count
═══════════════════════════════════════════════════════════════════════
- 2: adequate-to-strong command; errors do not impede meaning. 1: partial command; errors sometimes impede.
- 0: little command; errors frequently impede meaning. (Reserve 0 for genuine loss of control.)

""" + _FEEDBACK_COMMON + """
═══════════════════════════════════════════════════════════════════════
OUTPUT — a single JSON object, no other text
═══════════════════════════════════════════════════════════════════════
{
  "org_purpose_score": <0-4>, "org_purpose_max": 4,
  "evidence_elab_score": <0-4>, "evidence_elab_max": 4,
  "conventions_score": <0-2>, "conventions_max": 2,
  "sbac_total": <sum, 0-10>, "sbac_max": 10,
  "staar_total": <round(sbac_total/10*5, 1)>, "staar_max": 5,
  "total_score": <same as staar_total>, "total_max": 5,
  "gate_fired": "<G1 | G2 | G3 | none>",
  "feedback": "<warm student-facing feedback, 3-6 sentences, no scores>",
  "internal_notes": "<how you summed + normalized>"
}

🔹 TEST CONTENT
Passage:
{{passage}}
Prompt:
{{question}}
Student essay:
{{response}}
""",
}


# ---- ESSAY rc.4trait (Regents 4-criterion; argument /24 or analysis /16) ----

def _essay_4trait_prompt(mode: str) -> str:
    per = 6 if mode == "argument" else 4
    total = 24 if mode == "argument" else 16
    task = ("takes a clear position on the issue and defends it with reasons and evidence"
            if mode == "argument" else
            "analyzes how the text(s) work — ideas, craft, and meaning — rather than restating content")
    return f"""You are an experienced high-school writing grader scoring a full ESSAY on the NY Regents
4-criterion analytic rubric (the CCSS-native G11/G12 scale). This is a {mode.upper()} essay: the student {task}.

Score EACH of the four criteria 0-{per} (total 0-{total}). Build an evidence log first, then score.
Output one JSON object — no other text.

""" + _GATES_COMMON + f"""
═══════════════════════════════════════════════════════════════════════
FOUR CRITERIA — each scored 0-{per}
═══════════════════════════════════════════════════════════════════════
1. CONTENT & ANALYSIS: the strength of the {"position + reasoning" if mode=="argument" else "analysis of the text"};
   depth of thinking, not just presence. Top band = insightful, sustained, {"a nuanced defensible claim" if mode=="argument" else "genuine analysis of how meaning is made"}.
2. COMMAND OF EVIDENCE: relevant, specific, well-integrated support; explains how evidence supports the point
   (not dropped quotes / named-but-unexplained facts).
3. COHERENCE, ORGANIZATION & STYLE: logical structure, purposeful progression, controlled and varied language.
4. CONTROL OF CONVENTIONS: grammar/usage/mechanics; clarity is the gate — errors cost the top band only when
   they impede meaning.

Score each criterion on a 0-{per} ladder: {per}/{per-1} = strong-to-excellent command, mid = adequate/uneven,
low = minimal/flawed, 0 = absent or off-topic. Use the FULL range; reserve the top only for genuinely strong work.

""" + _FEEDBACK_COMMON + f"""
═══════════════════════════════════════════════════════════════════════
OUTPUT — a single JSON object, no other text
═══════════════════════════════════════════════════════════════════════
{{
  "mode": "{mode}",
  "content_analysis": <0-{per}>,
  "command_of_evidence": <0-{per}>,
  "coherence_org_style": <0-{per}>,
  "control_of_conventions": <0-{per}>,
  "criterion_max": {per},
  "total_score": <sum of the four, 0-{total}>,
  "total_max": {total},
  "gate_fired": "<G1 | G2 | G3 | none>",
  "feedback": "<warm student-facing feedback, 3-6 sentences, no scores>",
  "internal_notes": "<how you summed>"
}}

🔹 TEST CONTENT
Passage:
{{{{passage}}}}
Prompt:
{{{{question}}}}
Student essay:
{{{{response}}}}
"""


ESSAY_4TRAIT_ARGUMENT = {"id": "essay_4trait_argument", "scale": 24, "mode": "argument",
                         "prompt": _essay_4trait_prompt("argument")}
ESSAY_4TRAIT_ANALYSIS = {"id": "essay_4trait_analysis", "scale": 16, "mode": "analysis",
                         "prompt": _essay_4trait_prompt("analysis")}


LONG_SPECS = {
    "paragraph": PARAGRAPH,
    "essay_staar": ESSAY_STAAR,
    "essay_4trait_argument": ESSAY_4TRAIT_ARGUMENT,
    "essay_4trait_analysis": ESSAY_4TRAIT_ANALYSIS,
}
