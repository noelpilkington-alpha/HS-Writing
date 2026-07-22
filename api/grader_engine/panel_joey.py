"""Joey's STAAR-derived 3-trait rubric, grade-adapted G3-8, with 10-pt and 20-pt modes.

Reuses panel.py's engine UNCHANGED (preflight, _run_panel, _call_rubric_grader,
_call_synthesis). The rubric is Joey's 3-trait scale:

  Ideas and Content        (0-3)
  Organization & Structure (0-3)   <- own trait (vs Alpha folding it into Ideas)
  Conventions              (0-4)
  Total = 0-10. Gating: Ideas=0 -> Organization=0 AND Conventions=0.

Descriptors are VERBATIM from Joey's Draft Rubric (G6 baseline). GRADE ADAPTATION (Joey
Gap 8): per-band calibration blocks (G3 / G4-5 / G6 / G7-8) tune the EXPECTATIONS within
each band without rewriting the descriptors. G6-8 Q11 are essays, graded on the SAME
unified 3-trait rubric (decision A1) with an essay-level Organization note.

20-PT MODE (scale=20): grades on the native 0-3/0-3/0-4 judgment — preserving the
granularity that dissolved the 13-wall (see Experiment_STAAR_Rubric_Swap.md) — then ×2's
the trait scores + maxes to fill the legacy 20-pt Q11 slot. Totals land on even numbers
by design. NOT to be confused with re-authoring native 0-6/0-6/0-8 bands (rejected:
re-introduces the 13-wall). See Experiment_Design_Joey20_G38.md.

SCORING PROTOCOL (Joey Part B-D): Check 1 (insufficient text → 0), Check 3 (verbatim
copying, 2-tier caps) are deterministic; Check 2 (off-topic) + Check 4 (placeholder) need
no code per Joey's dispositions (rubric+gating handle them). The Scoring Firewall (mechanics
never lower Ideas/Org) is enforced in the Ideas prompt + synthesis. Gating rule (Ideas=0 →
all 0) deterministic. Part D feedback priority is in the synthesis prompt.
"""
from __future__ import annotations

from .models import QuestionScore
from .panel import (
    RubricDimension,
    _age_hint,
    _preflight,
    _run_panel,
    _default_panel_model,
    _build_audit,
)
import re

from .per_cat import _normalize_response_preserving_paragraphs, verbatim_fraction


# ═══════════════════════════════════════════════════════════════════════════════
# PART B — PRE-SCORING CHECKS (Joey Scoring Protocol, verbatim dispositions)
# Check 2 (off-topic) and Check 4 (placeholder) need NO code: Joey's dispositions say
# "score normally; the rubric + gating rule handle it." Only Check 1 (insufficient text)
# and Check 3 (verbatim copying, 2-tier) require pre-scoring logic.
# ═══════════════════════════════════════════════════════════════════════════════

def _count_sentences(text: str) -> int:
    """Count sentences by meaning, not just punctuation (Joey Check-1 guidance:
    a run-on with 3 distinct clauses counts as 3). Approximate: split on terminal
    punctuation AND on independent-clause coordinators when no terminal punct is present."""
    t = (text or "").strip()
    if not t:
        return 0
    # primary: terminal punctuation
    parts = [p for p in re.split(r"[.!?]+", t) if p.strip()]
    n = len(parts)
    # secondary: catch run-ons — count clause-joining patterns inside long unpunctuated spans
    for p in parts:
        words = p.split()
        if len(words) > 25:  # long span likely hides multiple clauses
            joins = len(re.findall(r"\b(and|but|so|because|then|also)\b", p, re.I))
            n += min(joins, 2)
    return n


def _has_complete_sentence(text: str) -> bool:
    """True if the response contains at least one COMPLETE sentence: a span of >=4 words that ends in
    terminal punctuation. Distinguishes a real (if short) attempt from a truncated fragment/stub."""
    t = re.sub(r"<[^>]+>", " ", text or "").strip()
    for span in re.split(r"(?<=[.!?])\s+", t):
        span = span.strip()
        if re.search(r"[.!?]$", span) and len(span.split()) >= 4:
            return True
    return False


def check1_insufficient_text(response: str) -> bool:
    """Check 1: catch TRUE STUBS only (Joey's intent: near-blank/fragmentary, NOT short-but-complete).

    Fire (→ floor) only when the response is a genuine stub:
      - <22 words (too short to be a real attempt), OR
      - no complete sentence at all (truncated mid-clause / pure fragment).
    A clearly-substantive word count (>=40 words) always overrides — a long response with few
    "sentences" is comma-splice/run-on writing (a CONVENTIONS problem, graded normally), not a stub.

    CALIBRATION (2026-06-04, bake-off n=12): the old rule (<30 words OR <3 sentences) MIS-FIRED on
    short-but-complete on-topic attempts. Anchor: Zenon (G4.1, Noel 40%) — 25 words, 2 complete
    sentences naming a passage detail — was floored to 10%; graded by the rubric he lands ~50% (within
    10% of Noel). The refined rule still correctly floors the true stubs from the same set: Felix
    (blank), Christian ("i love school", 3w), Dax (11w fragment), Liam (19w, truncated mid-clause).
    (Also preserves Anchor C4 — 77w of comma-spliced prose stays gradeable via the >=40-word override.)"""
    words = len((response or "").split())
    if words >= 40:
        return False  # substantive length — grade it; brokenness is Conventions' concern
    return words < 22 or not _has_complete_sentence(response)


def check3_verbatim_tier(response: str, passage: str) -> int:
    """Check 3 — verbatim copying severity:
      3 = wholesale copy: little original content (orig ratio < 15%) AND high overlap → gate to 0
      2 = Tier-1 (>=80% overlap): cap Ideas/Org at 1
      1 = Tier-2 (50-80% overlap): cap Ideas/Org at 2
      0 = legitimate (paraphrase is fine)
    The orig-ratio test catches the A5 case: 60% overlap but only ~10% original words — the student
    lifted the passage's opening and added almost nothing of their own. Noel graded that 0, not capped.
    """
    if not passage:
        return 0
    frac, orig, total = verbatim_fraction(response, passage)
    orig_ratio = (orig / total) if total else 1.0
    # Wholesale copy: overlap is substantial AND the student contributed little original prose.
    if frac >= 0.50 and orig_ratio < 0.15:
        return 3
    if frac >= 0.80:
        return 2
    if frac >= 0.50:
        return 1
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# GRADE-BAND CALIBRATION (Joey Gap 8: descriptors are G6 template; tune expectations
# per grade WITHOUT rewriting the descriptors). Appended to each trait prompt.
# Knobs only — analysis depth, sentence complexity, vocabulary, transitions, tolerance.
# ═══════════════════════════════════════════════════════════════════════════════

def _grade_band(grade: int) -> str:
    if grade <= 3:
        return "G3"
    if grade <= 5:
        return "G4-5"
    if grade == 6:
        return "G6"
    if grade <= 8:
        return "G7-8"
    return "G9-12"   # high-school analytical paragraphs (counterargument / DEW / claim-evidence-reasoning)


# Per-band, per-trait calibration text. Keep SHORT — these tune the bar, not the rubric.
_CALIBRATION = {
    "ideas": {
        "G3": "GRADE 3 calibration: top Ideas (3) needs ONE plainspoken reason developed (e.g. "
              "'...because it brings life'); do not require multi-step reasoning. Passage terms + "
              "simple on-topic claims count as specific evidence.",
        "G4-5": "GRADE 4-5 calibration: top Ideas (3) needs a reason plus brief elaboration; "
                "grade-appropriate detail from the passage. Reasoning may still be plain.",
        "G6": "GRADE 6 calibration (baseline): top Ideas (3) shows consistent explanation across the "
              "response, precise word choice, domain terms where apt.",
        "G7-8": "GRADE 7-8 calibration: top Ideas (3) expects sustained, multi-step reasoning and "
                "purposeful diction; a single reason repeated is Ideas 2, not 3.",
        "G9-12": "GRADE 9-12 calibration: this is a single ANALYTICAL/ARGUMENTATIVE paragraph "
                 "(e.g. counterargument, device->effect->warrant analysis, or claim+evidence+reasoning). These "
                 "are ANALYTICAL tasks, NOT narrative retelling — the WARRANT/analysis is what earns Ideas, not "
                 "mere thorough development. Ideas 3 = a defensible point AND explained reasoning that WARRANTS "
                 "the evidence (a stated why/how), OR a counterargument that GENUINELY ANSWERS the other side "
                 "(not just names it). Ideas 2 = point + evidence present but analysis THIN/generic. Ideas 1 = "
                 "the analytical move is essentially ABSENT (evidence dropped with no warrant; counter merely "
                 "mentioned; or SUMMARY of the source instead of analysis). Depth on the single move, not word "
                 "count; do NOT require full-essay breadth (this is one paragraph).",
    },
    "organization": {
        "G3": "GRADE 3 calibration: First/Next/Last transitions are fully acceptable at the top band; "
              "a clear opening + ordered details + a closing earns 3.",
        "G4-5": "GRADE 4-5 calibration: expect basic transitions plus some variety; clear structure "
                "earns 3 even if transitions are simple.",
        "G6": "GRADE 6 calibration (baseline): purposeful, varied transitions; logical progression.",
        "G7-8": "GRADE 7-8 calibration: expect varied, near-seamless transitions and a structure that "
                "builds; mechanical First/Second/Third alone is Organization 2, not 3.",
        "G9-12": "GRADE 9-12 calibration (SINGLE paragraph): top Organization (3) is INTERNAL paragraph "
                 "coherence — a clear point, ideas ordered so the reasoning builds (claim->evidence->warrant, "
                 "or concession->rebuttal), and logical connectives that signal the moves. Judge the "
                 "paragraph's internal logic, NOT essay-level intro/body/conclusion architecture (there is "
                 "none to expect). A paragraph that lists points with no connective logic is Organization 2.",
    },
    "conventions": {
        "G3": "GRADE 3 calibration: phonetic/spelling slips are expected and acceptable at the top "
              "bands if meaning is clear; simple sentences with one compound construction satisfy "
              "'sentence variety' for the 4 band.",
        "G4-5": "GRADE 4-5 calibration: a few isolated errors are fine at top; expect some compound/"
                "complex sentences for the 4 band.",
        "G6": "GRADE 6 calibration (baseline): few errors, no clarity impact; varied incl. complex "
              "sentences for the 4 band.",
        "G7-8": "GRADE 7-8 calibration: expect mature, sustained control and varied/complex sentences; "
                "a clean but uniformly simple response tops out at Conventions 3, not 4.",
        "G9-12": "GRADE 9-12 calibration: expect command of 9-12 band conventions with sustained control "
                 "and syntactic variety (subordination, appositives, varied openers). Occasional minor slips "
                 "are fine at the top if control holds; a clean but uniformly simple/monotonous paragraph "
                 "tops out at Conventions 3, not 4. Errors that recur or blur meaning cap lower.",
    },
}


def _calibrated(trait: str, base_prompt: str, grade: int) -> str:
    """Append the per-grade calibration block to a trait's base prompt."""
    band = _grade_band(grade)
    cal = _CALIBRATION[trait][band]
    return base_prompt + f"\n\n📐 GRADE-BAND CALIBRATION ({band}):\n{cal}"


# ═══════════════════════════════════════════════════════════════════════════════
# IDEAS AND CONTENT (0-3) — verbatim from Joey's Draft Rubric
# ═══════════════════════════════════════════════════════════════════════════════

_JOEY_IDEAS_PROMPT = """Score IDEAS AND CONTENT on a 0-3 scale. Judge holistically against the
descriptors and assign the ONE score point that best fits. This trait covers controlling idea,
evidence, analysis/reasoning, and expression — together.

🔒 PROMPT-RELEVANCE GATE (apply FIRST — NARROW; see calibration note):
Ask whether the response answers a genuinely DIFFERENT question than the one asked, versus answering the
right question thinly. These are NOT the same and must be treated differently:
  - PROMPT-MISS (cap Ideas at 1): the response addresses a different task than the prompt names. Example:
    prompt asks "HOW does the AUTHOR organize/support the argument?" (a meta-analysis of the author's
    craft) and the student instead argues the topic in their own voice, never analyzing the author's
    technique. The question asked was not attempted.
  - THIN-BUT-RESPONSIVE (do NOT cap — score on the descriptors): the response answers the prompt's
    actual question, just briefly or generically. Example: prompt asks "WHY does learning to cook help
    children?" and the student gives two real reasons ("if home alone you can feed yourself"; "after
    college you can take care of yourself"). That IS answering "why" — it is thin (likely Ideas 2), not
    a prompt-miss. Do not cap it.
The test is "did they attempt the question asked?", NOT "did they attempt it well?". Thinness is scored
by the descriptors below; only a genuine wrong-question answer is gated to 1.

🧱 SCORING FIREWALL: Ideas scores CONTENT QUALITY ONLY. Spelling, grammar, punctuation, and other
mechanical errors belong to the Conventions trait — NEVER let them lower the Ideas score. A response
with a strong controlling idea, specific evidence, and genuine reasoning earns full Ideas credit EVEN IF
it is riddled with spelling errors. The only word-level concern that touches Ideas is word CHOICE
(precision/formality), not word EXECUTION (spelling): a student who picks the right word but misspells
it loses Conventions credit, not Ideas credit.

⚠️ CALIBRATION STATUS: this gate is UNDER TEST. On the audit set it correctly caught Ellen (G5.4,
author-craft prompt answered with a topic-argument) but, in an over-aggressive earlier form, wrongly
failed Robin (G3.7, "why cook" answered thinly but correctly). The narrowed wording above is the fix;
re-validate against BOTH anchors (Ellen = miss, Robin = pass) before relying on it in production.

SCORE POINT 3:
- Controlling idea is clear and addresses the prompt. The main idea is clearly identifiable, directly
  responds to what the prompt asks, and is stated in the student's own words.
- Evidence is specific, well chosen, and relevant. Specific facts/details/references from the source
  passage develop the controlling idea; evidence consistently supports the main idea rather than
  appearing as loose detail.
- Analysis shows genuine reasoning. Explanatory sentences go beyond restating evidence — the student
  reasons about why the evidence matters or how it connects to the controlling idea, even in plain,
  workmanlike language ("This allows…", "So that…", "This means that…"). Bare restatement ("This shows
  that…" + a paraphrase) is not the sole form of explanation.
- Expression is clear and precise. Word choice is specific to the topic; passage vocabulary used where
  appropriate; tone formal and suited to expository writing.

SCORE POINT 2:
- Controlling idea is present and partially developed — identifiable but general, broadly stated, or
  only partially developed.
- Evidence is limited or may include some irrelevant information; relevant evidence is present but does
  not consistently develop the controlling idea.
- Analysis is basic or partially formulaic. Some explanation present, but reasoning may rely on
  formulaic restatement rather than causal/explanatory thinking; genuine reasoning, if present, limited
  to one or two sentences.
- Expression is general; word choice general rather than precise.

SCORE POINT 1:
- Controlling idea is evident but not developed, or only loosely connected to the prompt; may echo/copy
  the prompt wording.
- Evidence is insufficient and/or mostly irrelevant; information may be listed without being tied to
  the controlling idea.
- Analysis is ineffective — explanation absent or limited to restating evidence; where attempted, it is
  formulaic and adds no new thinking.
- Expression is unclear; word choice vague, imprecise, or repetitive.

SCORE POINT 0:
- A controlling idea responsive to the prompt is not evident; off-topic; or near-verbatim restatement
  of the prompt with no original writing.
- Evidence not provided or not relevant.
- Analysis not provided.
- Expression unclear or incoherent.

CALIBRATION: Workmanlike, plainspoken reasoning COUNTS as analysis — it need not use "because" or formal
transitions. Reward what the student demonstrates at grade level.

🔑 DEVELOPMENT DEPTH is the primary 1-vs-2-vs-3 axis (calibrated to expert grades):
Judge HOW RICHLY the ideas are developed, not only whether explicit "why" analysis is present. A
response that develops its points THOROUGHLY — each idea elaborated across multiple sentences with
specific detail — earns Ideas 3 EVEN IF the reasoning is largely implicit in a well-told account.
Do NOT cap a richly-developed response at 2 merely because it "retells/lists rather than analyzes":
sustained, detailed development of relevant content IS the substance this trait rewards.
  • Ideas 3 = several relevant ideas, EACH developed across multiple sentences with specific
    passage-grounded detail; the account is full and thorough. (Anchor: a ~230-word Wilma essay that
    elaborates polio → mother's help → walking at 12 → track career → Olympic medals → legacy, each
    across 2-3 sentences — earns 3 even though the "why it shows perseverance" is mostly implicit.)
  • Ideas 2 = relevant ideas present and partially developed — some elaboration but uneven, OR a
    competent but general treatment; the content is there but not richly built out.
  • Ideas 1 = ideas/points NAMED but THIN — each stated in a sentence or two with little development;
    a brief summary that touches the points without building any of them out. (Anchor: a ~78-word
    Wilma paragraph that names polio → walking → Olympics → "inspired people" in single sentences =
    Ideas 1, NOT 2 — the points are present but undeveloped.)
The D12-vs-B4 line: SAME content arc, but B4 develops each stage across multiple detailed sentences
(→3) while D12 names each stage once (→1). Word count is a SIGNAL of development, not the criterion —
a long but repetitive response is not developed; a tight but genuinely elaborated one can be. When
between two scores, ask: is EACH main idea built out with specific detail (→higher) or just named
(→lower)?

Output evidence as short observations tied to phrases; reasoning as 2-3 sentences naming the score point."""


# ═══════════════════════════════════════════════════════════════════════════════
# ORGANIZATION AND STRUCTURE (0-3) — verbatim from Joey's Draft Rubric
# ═══════════════════════════════════════════════════════════════════════════════

_JOEY_ORG_PROMPT = """Score ORGANIZATION AND STRUCTURE on a 0-3 scale. This trait is SEPARATE from Ideas
— it scores how the response is arranged (topic sentence, logical progression, transitions, concluding
sentence), NOT the substance of the ideas themselves.

SCORE POINT 3:
- Topic sentence is clear and introduces the paragraph in the student's own words.
- Ideas progress logically in a purposeful sequence (e.g., general→specific, cause→effect,
  evidence→explanation).
- Transitions guide the reader (addition, cause/effect, example, contrast) and feel purposeful rather
  than decorative.
- Concluding sentence follows from the body and provides a sense of completion — more than restating the
  topic sentence verbatim.

SCORE POINT 2:
- Topic sentence is present but may be underdeveloped, broad, partially on-prompt, or echo the prompt.
- Ideas show some logical progression, but sequencing may have gaps; structure apparent but not
  consistent throughout.
- Some transitions present but inconsistent or limited to a narrow set (repeated "also"/"then").
- A concluding sentence is present but may be weak — restating the topic sentence with little extension,
  or ending somewhat abruptly.

SCORE POINT 1:
- A topic sentence may be evident but does not effectively introduce the paragraph (off-prompt, copied,
  or fails to establish a clear topic).
- Organizational structure is minimal or weak; the body reads as a list of details rather than a
  developed progression.
- Transitions are minimal or missing; relies on adjacency rather than explicit transitional language.
- A concluding sentence is weak or missing.

SCORE POINT 0:
- No topic sentence evident; no discernible organizational structure; transitions absent; no concluding
  sentence.

CALIBRATION: A response can be strong in Ideas but weaker in Organization, or vice versa — score this
trait independently. At grade level, a clear opening + ordered details + a closing earns 3 even if
transitions are simple. Do not require essay-level sophistication in a single paragraph.

Output evidence as short observations; reasoning as 2-3 sentences naming the score point."""


# ═══════════════════════════════════════════════════════════════════════════════
# CONVENTIONS (0-4) — verbatim from Joey's Draft Rubric
# ═══════════════════════════════════════════════════════════════════════════════

_JOEY_CONVENTIONS_PROMPT = """Score CONVENTIONS on a 0-4 scale. Judge overall COMMAND of grade-level
conventions (spelling, capitalization, punctuation, grammar/usage, sentence construction). Impact on
clarity is the controlling question, not error count.

SCORE POINT 4:
- Consistent mastery of grade-level conventions across spelling, capitalization, punctuation, grammar,
  and sentence construction.
- The response has few, if any, errors, and any errors present do not impact clarity.
- Sentences show some variety in length or structure.

SCORE POINT 3:
- Strong command across all convention areas.
- A small number of minor errors, but they do not impact clarity.
- Sentence construction is reliable throughout.

SCORE POINT 2:
- Adequate command across the areas.
- Several errors, possibly in more than one area, but the reader can understand the writer's thoughts
  throughout.
- Sentences generally complete, though there may be a run-on, comma splice, or fragment.

SCORE POINT 1:
- Limited command, with inconsistent use of correct spelling, capitalization, punctuation, grammar,
  and sentence construction.
- Errors at times interfere with clarity, though the reader can generally recover the meaning.

SCORE POINT 0:
- Little to no command; many errors that impact clarity and the reader's understanding.

CALIBRATION — CLARITY IS THE GATE, NOT ERROR PRESENCE (expert-calibrated; do not over-dock):
The single controlling question is: do the errors IMPEDE CLARITY/MEANING? Errors that a reader glides
past without rereading do NOT cost points, no matter how many there are.
  🔑 HARD RULE: if a trained reader can read the response smoothly and the meaning is never in doubt,
     the floor is 3 — do NOT drop below 3 for errors that don't impede clarity. Score 3 even with
     several spelling slips, missing commas, or a stray run-on, AS LONG AS meaning stays clear.
  • 4 = errors are few AND clarity is pristine AND some sentence variety. (A clean response with only a
     couple of trivial slips and varied sentences is a 4, not a 3.)
  • 3 = clarity fully intact; errors are noticeable but never make the reader stop or reread. This is
     the DEFAULT for any readable, grade-appropriate response. Repeated grade-level-typical
     misspellings that don't obscure the word stay here.
  • 2 = RESERVED for when errors actually START to impede — the reader must occasionally pause or
     reread to recover meaning. Do NOT assign 2 merely because errors are present and clarity holds.
  • 1 = errors frequently interfere; reader works to recover meaning.
  • 0 = meaning is often lost.
A repeated single skill gap (e.g. the same misspelled word ×4) is ONE pattern, not N errors, and if the
word is still recognizable it does not impede clarity. When genuinely between two scores and clarity is
NOT impeded, choose the HIGHER score — under-docking clean-but-imperfect writing is the error to avoid.

Output evidence as categorized observations (spelling/punctuation/grammar/sentence construction/clarity);
reasoning as 1-2 sentences. State explicitly whether clarity was impeded."""


# ═══════════════════════════════════════════════════════════════════════════════
# JUDGE / SYNTHESIS
# ═══════════════════════════════════════════════════════════════════════════════

_JOEY_SYNTHESIS = """Combine the panel's three trait recommendations into a final score.

Total = Ideas and Content (0-3) + Organization and Structure (0-3) + Conventions (0-4) = 0-10.

Apply these rules BEFORE finalizing:

1. GATING RULE (from the rubric): If Ideas and Content = 0, then Organization = 0 AND Conventions = 0.
   A response that does not address the prompt or present a controlling idea cannot be meaningfully
   scored for organization or mechanics. Apply automatically.
2. Verbatim-copy check (Check 3, applied via condition codes — see PRE-SCORING CHECKS below if present):
   Tier 1 (≥80% verbatim): cap Ideas at 1 AND Organization at 1. Tier 2 (50-80%): cap Ideas at 2 AND
   Organization at 2, crediting only original analysis/structure. Paraphrasing is NOT copying — only
   word-for-word reproduction triggers this.
3. Score-vs-evidence consistency: If a panel grader's reasoning contradicts its score, override to match
   the evidence it listed, and explain.
4. Independence: Ideas and Organization are SEPARATE traits — do not collapse them to the same number.
   A response can have strong ideas but weak structure, or clean structure around thin ideas. Likewise
   Conventions is independent of both. Resist the pull to make all three land at the same level.
5. 🧱 SCORING FIREWALL: convention/spelling/grammar errors live ONLY in Conventions. NEVER let weak
   mechanics pull down Ideas or Organization. Strong content with many spelling errors = full Ideas
   credit + low Conventions. Do not let a messy-looking response depress the content traits.
6. Do not inflate or deflate beyond the descriptors. A solid, complete, grade-appropriate response
   earns high marks across traits and that is correct; do not withhold top points to seem rigorous.

If no override is needed, accept the panel scores as-is.

Student-facing feedback (Part D structure — follow the priority order):
- PRIORITY: if Ideas < top, the #1 improvement is explaining WHY/HOW the evidence matters (give a short
  model sentence) — NOT "add more details". If Ideas is strong but Organization is weak, target
  structure. If only Conventions is weak, name the one most impactful mechanical pattern (sentence
  boundaries before spelling).
- Open with one specific, sincere strength tied to the student's actual words.
- Name ONE concrete, actionable improvement per the priority above.
- Be 4-6 sentences, encouraging, age-appropriate. Never mention scores, points, or rubric names.

Return JSON: { "totalScore": <0-10>, "maxScore": 10,
  "categoryScores": [
    {"rubricId":"ideas","name":"Ideas and Content","score":<0-3>,"maxPoints":3,"overridden":<bool>,"overrideReason":<string|null>},
    {"rubricId":"organization","name":"Organization and Structure","score":<0-3>,"maxPoints":3,"overridden":<bool>,"overrideReason":<string|null>},
    {"rubricId":"conventions","name":"Conventions","score":<0-4>,"maxPoints":4,"overridden":<bool>,"overrideReason":<string|null>}],
  "feedback":"<student-facing>", "reasoning":"<audit trail, not shown to student>" }"""


_JOEY_INTRO = """You are an experienced writing grader scoring a Grade {grade} student's response to a
write-a-paragraph-from-prompt task, using a standards-derived rubric.

The student read a short text and wrote a paragraph responding to a specific question about it. You will
receive the source text, the exact question, and the student's paragraph. With the rest of the panel,
score it on the rubric below.

The rubric scores the response out of 10 total points across THREE independent traits:
- Ideas and Content (0-3): controlling idea, evidence, analysis/reasoning, expression.
- Organization and Structure (0-3): topic sentence, logical progression, transitions, concluding sentence.
- Conventions (0-4): spelling, capitalization, punctuation, grammar, sentence construction.

The student is {age_hint}. Score what the student demonstrates at grade level; do not penalize for the
absence of sophistication the rubric does not demand, and do not withhold full marks from a complete,
well-developed, grade-appropriate response."""


_JOEY_ESSAY_INTRO = """You are an experienced writing grader scoring a Grade {grade} student's response
to an expository essay-from-prompt task, using a standards-derived rubric.

The student read a short text and wrote a multi-paragraph essay (target: ~5 paragraphs) responding to a
specific question about it. You will receive the source text, the exact question, and the student's
essay. With the rest of the panel, score it on the SAME three-trait rubric used across grades, applied
at the essay level.

The rubric scores the response out of 10 total points across THREE independent traits:
- Ideas and Content (0-3): controlling idea/thesis, evidence, analysis/reasoning, expression.
- Organization and Structure (0-3): essay-level structure — intro paragraph, ordered body paragraphs,
  cross-paragraph transitions, and a concluding paragraph.
- Conventions (0-4): spelling, capitalization, punctuation, grammar, sentence construction.

The student is {age_hint}. Score what the student demonstrates at grade level; do not penalize for the
absence of sophistication the rubric does not demand, and do not withhold full marks from a complete,
well-developed, grade-appropriate essay."""


# ═══════════════════════════════════════════════════════════════════════════════
# PROFICIENCY DECISION (separate from the raw rubric score)
# ═══════════════════════════════════════════════════════════════════════════════
#
# Empirically derived from the 17-essay standards-audit ground truth
# (see Grading Standards Documentation/Proficiency_Cut_Analysis.md):
#   - cut = 7/10 matches a ~60-65% proficiency standard (88% -> 94% with the Ideas gate)
#   - cut = 9/10 matches a 90% proficiency standard
# "Gate A": Ideas >= 2 is REQUIRED to clear the cut — analogous to STAAR's Development
#   cascade. A clean/well-organized but thin-content paragraph (Ideas <= 1) cannot pass
#   on form alone. This removed the Reed Robertson false-pass with zero true-pass breakage.

def is_proficient(score: QuestionScore, cut: int | None = None) -> bool:
    """Proficiency decision. Total >= cut AND Ideas >= the band's "2-of-3" floor.

    Scale-aware: detects 10-pt vs 20-pt mode from ideas_max (3 vs 6).
      10-pt: default cut 7/10, Ideas floor 2/3.
      20-pt: default cut 14/20, Ideas floor 4/6 (= the doubled "Ideas >= 2").
    Gate A (Ideas floor) is the proficiency-boundary analogue of STAAR's Development cascade.
    """
    if score.ideas_max >= 6:  # 20-pt mode
        cut = 14 if cut is None else cut
        ideas_floor = 4
    else:                      # 10-pt mode
        cut = 7 if cut is None else cut
        ideas_floor = 2
    return score.total_score >= cut and score.ideas_score >= ideas_floor


# ═══════════════════════════════════════════════════════════════════════════════
# PUBLIC API
# ═══════════════════════════════════════════════════════════════════════════════

def score_panel_joey(
    client,
    *,
    grade: int,
    passage: str,
    question: str,
    response: str,
    qnum: int = 11,
    scale: int = 10,
) -> QuestionScore:
    """Score a Q11 paragraph (G3-5) or essay (G6-8) on Joey's 3-trait rubric.

    Same panel engine as panel.py; only the rubric differs. Grade-adapted via per-band
    calibration blocks (G3 / G4-5 / G6 / G7-8). G6-8 essays use the SAME unified 3-trait
    rubric (decision A1): the Organization trait rewards multi-paragraph flow.

    scale: 10 (native) or 20 (legacy Q11 slot). In 20-pt mode the engine STILL grades on
      the native 0-3/0-3/0-4 judgment (preserving the granularity that beat the 13-wall),
      then ×2 the trait scores + maxes for display (Ideas 0-6 / Org 0-6 / Conv 0-8 = 20).
      Totals land on even numbers only — by design.
    """
    assert scale in (10, 20), "scale must be 10 or 20"
    max_total = scale
    mult = scale // 10  # 1 or 2

    gate = _preflight(response)
    if gate == "empty":
        return QuestionScore.blank(qnum, max_total, grade)
    if gate == "gibberish":
        return QuestionScore.gibberish(qnum, max_total, grade)

    response = _normalize_response_preserving_paragraphs(response)

    # Part B — Check 1: Insufficient Text.
    # POLICY (Noel, provisional 2026-05-29): a genuine-but-truncated ATTEMPT should not score 0 — that
    # floor is for near-blank/gibberish only. A response with a real topic sentence + start of an idea
    # that simply stops earns a FLOOR of 1 (Ideas 1), not 0. Pure fragments (<8 words, no central idea)
    # still go to 0 via _preflight gibberish / the empty gate above.
    if check1_insufficient_text(response):
        words = len(response.split())
        has_attempt = words >= 8  # a real clause/topic-sentence attempt, not a stub
        floor = 1 if has_attempt else 0
        return QuestionScore(
            question=qnum, ideas_score=floor * mult, ideas_max=3 * mult,
            organization_score=0, organization_max=3 * mult,
            conventions_score=0, conventions_max=4 * mult,
            total_score=floor * mult, total_max=max_total,
            feedback="You made a good start! Next time, aim to write a full paragraph: state your main "
                     "idea, give a couple of details from the text, and explain why they matter.",
            internal_notes=(f"JOEY{scale} {_grade_band(grade)} INSUFFICIENT_TEXT (Check 1) → "
                            f"{floor*mult}/{max_total} [provisional floor: attempt={has_attempt}]"),
            teacher_notes="Pre-scoring Check 1 fired: <3 sentences / <30 words. "
                          f"{'Genuine truncated attempt → Ideas floor 1.' if has_attempt else 'Near-blank → 0.'}",
        )

    model = _default_panel_model()
    is_essay = grade >= 6
    intro = (_JOEY_ESSAY_INTRO if is_essay else _JOEY_INTRO).format(grade=grade, age_hint=_age_hint(grade))

    # Apply per-grade calibration to each trait prompt.
    ideas_p = _calibrated("ideas", _JOEY_IDEAS_PROMPT, grade)
    org_p = _calibrated("organization", _JOEY_ORG_PROMPT, grade)
    conv_p = _calibrated("conventions", _JOEY_CONVENTIONS_PROMPT, grade)
    if is_essay:
        org_p += (
            "\n\n📄 ESSAY STRUCTURE — score the ARCHITECTURE of the response.\n"
            "🧱 FIREWALL (applies to MULTI-PARAGRAPH essays): when an essay HAS real paragraph structure, "
            "do NOT lower Organization just because individual body paragraphs are brief or analysis is "
            "shallow — that thinness is the IDEAS trait's concern. A well-built but thin multi-paragraph "
            "essay keeps high Organization.\n"
            "⚖️ SINGLE-BLOCK EXCEPTION (the firewall does NOT apply here): when a response is ONE unbroken "
            "block with no real paragraph breaks, development depth DOES gate Organization — because "
            "whether the block is 'really an essay' depends on whether its ideas are developed enough to "
            "BE separate paragraphs. Score:\n"
            "  3 = Real multi-paragraph architecture: actual paragraph breaks (or labeled sections) forming "
            "intro / body paragraphs / conclusion. Reader sees a built essay.\n"
            "  2 = SINGLE BLOCK containing SEVERAL distinct, FULLY-DEVELOPED ideas — each elaborated enough "
            "(multiple sentences of real development each) that it could stand as its own body paragraph "
            "AS-WRITTEN. Latent paragraphs are genuinely present; only the line breaks are missing. "
            "(Anchor: a ~230-word block where polio→learning-to-walk→track-career→legacy are EACH "
            "elaborated across several sentences.)\n"
            "  1 = SINGLE BLOCK whose ideas are present but TOO THIN to be real paragraphs — narrative "
            "STAGES or points named in a sentence or two each, not developed into paragraph-worthy units; "
            "OR ideas that blur together as one flow. Most short single-paragraph 'essays' land here. "
            "(Anchors: an ~80-word block that names childhood→walking→Olympics→reflection as single "
            "sentences = 1, NOT 2 — the stages exist but are undeveloped; a ~140-word block whose ideas "
            "run together as one stretch = 1.)\n"
            "  0 = No discernible arrangement; disordered.\n"
            "🔑 THE 1-vs-2 LINE ON A SINGLE BLOCK: not 'are there distinct ideas' (a 4-sentence summary "
            "has 4 distinct ideas but is still 1). The test is: is EACH distinct idea DEVELOPED across "
            "multiple sentences with real elaboration, such that it is already a body paragraph minus the "
            "break? Several genuinely-developed ideas → 2. Stages/points stated thinly → 1. When unsure "
            "between 1 and 2 on a single block, default to 1 unless the development is clearly "
            "paragraph-level.")

    dimensions = [
        RubricDimension(id="ideas", name="Ideas and Content", max_points=3, prompt=ideas_p),
        RubricDimension(id="organization", name="Organization and Structure", max_points=3, prompt=org_p),
        RubricDimension(id="conventions", name="Conventions", max_points=4, prompt=conv_p),
    ]

    synthesis, panel_results, elapsed = _run_panel(
        client, dimensions, intro, passage, question, response, grade, model, _JOEY_SYNTHESIS)

    ideas = max(0, min(3, synthesis.category_scores.get("ideas", panel_results[0].score)))
    org = max(0, min(3, synthesis.category_scores.get("organization", panel_results[1].score)))
    conv = max(0, min(4, synthesis.category_scores.get("conventions", panel_results[2].score)))

    # Part B — Check 3: Verbatim copying caps (deterministic backstop to the judge).
    copy_note = ""
    tier = check3_verbatim_tier(response, passage)
    if tier == 3:  # wholesale copy — negligible original content → gate to 0 (Noel's A5 standard)
        ideas = org = conv = 0
        copy_note = " | VERBATIM_COPY (negligible original content): all traits → 0"
    elif tier == 2:  # >=80% overlap
        ideas, org = min(ideas, 1), min(org, 1)
        copy_note = " | VERBATIM_TIER1(>=80%): Ideas/Org capped at 1"
    elif tier == 1:  # 50-80% overlap
        ideas, org = min(ideas, 2), min(org, 2)
        copy_note = " | VERBATIM_TIER2(50-80%): Ideas/Org capped at 2"

    # Gating rule (Joey) — but NARROWED per Noel (2026-05-29): the Ideas=0 → all-0 cascade should fire
    # only on TRUE off-topic (a response that addresses a different topic, with no real structure/mechanics
    # to credit). When Ideas=0 but the Organization AND Conventions graders independently found a genuine,
    # mechanically-sound attempt (both >=2) — i.e. the writing engaged the passage but missed the prompt's
    # specific question — preserve their Org/Conv credit rather than zeroing it. (Anchor: C2 — on-passage,
    # prompt-missing, but organized and readable: Noel scored Org/Conv ~2 each, not 0.)
    if ideas == 0:
        true_off_topic = not (org >= 2 and conv >= 2)
        if true_off_topic:
            org = 0
            conv = 0
        else:
            copy_note += " | OFF-PROMPT (not off-topic): Ideas 0 but Org/Conv credited on the attempt"

    # POLICY (Noel, provisional 2026-05-29): on ESSAY tasks, a response that did not produce a real
    # multi-paragraph essay (Org <= 1, i.e. a single undivided block) cannot earn the top Conventions
    # point — the 4 is reserved for developed, essay-shaped writing. Cap Conventions at 3 for non-essays.
    if is_essay and org <= 1 and conv > 3:
        conv = 3
        copy_note += " | NON-ESSAY: Conventions capped at 3 (single-block response)"

    # G9-12 ANALYTICAL-PARAGRAPH CONTENT GATE (added 2026-07-21; grade>=9 ONLY — G3-8 production untouched).
    # These tasks TEACH an analytical move (warrant / answer-the-counter / analysis-not-summary). On the raw
    # 3+3+4 scale, content is only 30% of the total, so a thin-but-CLEAN, well-ordered paragraph rode Org+Conv
    # to ~9/10 (Ideas 2 + Org 3 + Conv 4) even with no real analysis — the inflation the validation caught
    # (STAAR G3-5 +11.8%/+23% low-band; G9-12 spot-check misses). Fix: when the analytical move is thin/absent
    # (low Ideas), the paragraph is NOT proficient no matter how clean — cap Org+Conv so content gates the total.
    # This is the same principle the essay layer settled (conventions-weight is a design choice, Building 17.4),
    # applied at the paragraph grain. Same shape as the existing Ideas==0 cascade + non-essay conv cap above.
    if grade >= 9:
        if ideas <= 1:
            # analytical move essentially absent -> a clean-but-empty paragraph caps well below proficient.
            org = min(org, ideas + 1)   # Ideas 1 -> Org<=2, Ideas 0 -> Org<=1
            conv = min(conv, 2)          # clean mechanics alone cannot exceed 2 when there is no analysis
        elif ideas == 2:
            # thin-but-present analysis -> may not ride perfect Org+Conv to a top-band total.
            conv = min(conv, 3)

    # ×2 display scaling for the 20-pt slot (judgment already made on 0-3/0-3/0-4).
    ideas *= mult
    org *= mult
    conv *= mult
    total = ideas + org + conv

    internal_notes, teacher_notes = _build_audit(panel_results, synthesis, elapsed, qnum, grade)
    internal_notes = (f"JOEY{scale} {_grade_band(grade)} {'essay' if is_essay else 'para'} "
                      + internal_notes + f" | ideas={ideas} org={org} conv={conv} total={total}/{max_total}"
                      + copy_note)

    return QuestionScore(
        question=qnum, ideas_score=ideas, ideas_max=3 * mult,
        organization_score=org, organization_max=3 * mult,
        conventions_score=conv, conventions_max=4 * mult,
        total_score=total, total_max=max_total,
        feedback=synthesis.feedback,
        internal_notes=internal_notes, teacher_notes=teacher_notes,
    )
