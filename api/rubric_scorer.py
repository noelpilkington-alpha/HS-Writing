"""Config-driven 4-trait rubric scorer (Model C) — the rc.* engine.

Scores a source-based essay on the CANONICAL 4 traits (Thesis/Purpose, Evidence/Development,
Organization/Coherence, Conventions/Language), where the trait COUNT, SCALE, WEIGHTING, and GATE rules
are a per-form CONFIG over one engine. This is the decisive design from TestDesign_Reference.md:
canonical traits fixed, everything else parameterized. It scores the G10 CR test-bank items
(cr_argument / cr_explanatory / cr_analysis) that carry an rc.* rubric_ref.

Scale/gate provenance (TestDesign_Reference.md §2, G10_Item_Spec_L4.md):
  rc.staar  STAAR Eng II  Org&Dev 0-3 + Conventions 0-2, x2 scorers = 10   GATE: 0 Org&Dev -> 0 Conventions
  rc.mcas   MCAS Gr 10    Idea Development 0-5 + Conventions 0-3 = 8
  rc.ohio   Ohio ELA II   Purpose/Focus/Org 0-4 + Evidence/Elaboration 0-4 + Conventions 0-2 = 10
  rc.4trait generic G10   4 traits 0-4 = 16   (default for own-target items)
  rc.ap     AP overlay    Thesis 0-1 + Evidence&Commentary 0-4 + Sophistication 0-1 = 6  (routes to ap_scorer)

DESIGN NOTE (Platform3): scoring is declared surface-owned on Platform3 ("fix gaps on the platform, not
in your app"). This module is the EXTERNAL scorer that lets our generated courses function NOW, and it is
built to migrate: the rc.* config table below is the portable contract. When the Platform3 scoring gap
closes, this table moves onto the surface unchanged and this module becomes a thin client. Filed as a
Platform3 gap; see Alpha HS Writing Course 2026-27/PLATFORM3_GAP_scoring.md.

Mirrors ap_scorer.py structure (system prompt + user prompt + parse + clamp + score_fn) so it plugs into
the existing consensus + /timeback/score machinery in main.py with no new patterns.
"""

import json
import re

# ===================================================================================================
# THE rc.* CONFIG TABLE  (the portable, surface-migratable contract)
# Each trait: (key, label, min, max). gate: optional {"if_trait": key, "is": 0, "force_trait": key, "to": 0}.
# scorers: multiplier applied to the summed traits (STAAR doubles: two independent scorers).
# ===================================================================================================

RUBRIC_CONFIGS: dict[str, dict] = {
    "rc.staar": {
        "models": "STAAR English II",
        "traits": [
            ("org_dev", "Organization & Development of Ideas", 0, 3),
            ("conventions", "Conventions", 0, 2),
        ],
        "scorers": 2,                 # summed traits x2 independent scorers = /10
        "gate": {"if_trait": "org_dev", "is": 0, "force_trait": "conventions", "to": 0,
                 "why": "STAAR gate: a 0 on Organization & Development forces Conventions to 0 (you cannot "
                        "score conventions on an essay that does not develop the idea)."},
        "trait_descriptors": {
            "org_dev": {
                0: "No clear thesis or organizing structure; little or no development; may be off-topic.",
                1: "Weak or unclear thesis; minimal organization; development is thin, listy, or mostly restates the source.",
                2: "Clear thesis and mostly logical organization; development uses some relevant source evidence with some explanation, but may be uneven or general.",
                3: "Clear, specific thesis; effective, purposeful organization; development is specific and well-elaborated, integrating source evidence with commentary that goes beyond restating.",
            },
            "conventions": {
                0: "Little command of conventions; errors are frequent and severe enough to interfere with meaning.",
                1: "Some command of conventions; errors are present and noticeable but meaning is generally clear.",
                2: "Consistent command of sentence boundaries, usage, and punctuation; errors are minor and do not interfere with meaning.",
            },
        },
    },
    "rc.mcas": {
        "models": "MCAS Grade 10",
        "traits": [
            ("idea_development", "Idea Development", 0, 5),
            ("conventions", "Conventions", 0, 3),
        ],
        "scorers": 1,                 # /8
        "gate": None,
        "trait_descriptors": {
            "idea_development": {
                0: "Insufficient, off-topic, or merely copies the source.",
                1: "Minimal development; little use of the source; no clear central idea.",
                2: "Limited development; a central idea is present but support is general and thinly explained.",
                3: "Adequate development; clear central idea developed with relevant source evidence and some explanation.",
                4: "Strong development; central idea developed with well-chosen source evidence and consistent explanation.",
                5: "Insightful development; a nuanced central idea developed with precise evidence and explanation that reaches significance (the so-what).",
            },
            "conventions": {
                0: "Frequent, serious errors that impede understanding.",
                1: "Errors in grammar, usage, and mechanics are noticeable and sometimes impede meaning.",
                2: "Generally controls conventions; errors are present but do not impede meaning.",
                3: "Consistent control of conventions and varied, appropriate sentence structure; errors are minor.",
            },
        },
    },
    "rc.ohio": {
        "models": "Ohio ELA II",
        "traits": [
            ("purpose_focus_org", "Purpose, Focus & Organization", 0, 4),
            ("evidence_elaboration", "Evidence & Elaboration", 0, 4),
            ("conventions", "Conventions", 0, 2),
        ],
        "scorers": 1,                 # /10
        "gate": None,
        "trait_descriptors": {
            "purpose_focus_org": {
                0: "No clear claim/controlling idea; no discernible organization.",
                1: "Weak or drifting claim; little organizational structure; frequent lapses in focus.",
                2: "Adequate claim; a recognizable structure with some transitions; mostly focused.",
                3: "Clear claim; logical progression with effective transitions; consistent focus.",
                4: "Precise claim; purposeful, cohesive structure; maintains a strong focus throughout and addresses opposing/other views where the mode calls for it.",
            },
            "evidence_elaboration": {
                0: "No evidence, or evidence unrelated to the claim.",
                1: "Minimal, mostly general evidence; little elaboration; leans on summary.",
                2: "Adequate source evidence with some elaboration; explanation is present but general.",
                3: "Relevant, integrated source evidence with clear elaboration tying it to the claim.",
                4: "Well-chosen, integrated evidence with thorough elaboration and commentary that reaches significance.",
            },
            "conventions": {
                0: "Frequent, serious errors that interfere with meaning.",
                1: "Some command; noticeable errors that do not usually interfere with meaning.",
                2: "Adequate command of sentence formation, usage, and mechanics; errors are minor.",
            },
        },
    },
    "rc.4trait": {
        "models": "Generic G10 analytic (own-target default)",
        "traits": [
            ("thesis_purpose", "Thesis / Purpose", 0, 4),
            ("evidence_development", "Evidence / Development", 0, 4),
            ("organization", "Organization / Coherence", 0, 4),
            ("conventions", "Conventions / Language", 0, 4),
        ],
        "scorers": 1,                 # /16
        "gate": None,
        "trait_descriptors": {
            "thesis_purpose": {
                0: "No defensible thesis; restates the prompt or takes no position.",
                1: "Vague or partly defensible thesis; purpose unclear.",
                2: "Clear, defensible thesis; purpose mostly clear.",
                3: "Precise, defensible thesis that sets a line of reasoning.",
                4: "Precise, nuanced thesis that answers the so-what and frames the whole response.",
            },
            "evidence_development": {
                0: "No relevant evidence.",
                1: "Evidence present but dropped in or unexplained.",
                2: "Relevant evidence with some explanation; may be uneven.",
                3: "Well-integrated evidence with consistent commentary tied to the claim.",
                4: "Well-chosen, integrated evidence with commentary that reaches significance.",
            },
            "organization": {
                0: "No discernible structure.",
                1: "Weak structure; abrupt or missing transitions.",
                2: "Recognizable structure; some effective transitions.",
                3: "Logical progression with effective transitions throughout.",
                4: "Purposeful, cohesive structure that advances the line of reasoning.",
            },
            "conventions": {
                0: "Frequent, serious errors that impede meaning.",
                1: "Noticeable errors; meaning generally clear.",
                2: "Adequate control; minor errors; some sentence variety.",
                3: "Consistent control; varied, appropriate sentences.",
                4: "Precise, varied, register-appropriate language (style beyond mere correctness).",
            },
        },
    },
}

# rc.ap is intentionally NOT in this table: AP's Row A/B/C (with FRQ-type-specific Row B and the
# Sophistication row) is already implemented in ap_scorer.py. main.py routes rc.ap -> score_ap_essay.
AP_CONFIG_ID = "rc.ap"


def get_rubric_config(rc_id: str) -> dict | None:
    return RUBRIC_CONFIGS.get(rc_id)


def config_max_score(rc_id: str) -> int:
    cfg = RUBRIC_CONFIGS[rc_id]
    base = sum(hi for (_k, _l, _lo, hi) in cfg["traits"])
    return base * cfg.get("scorers", 1)


# ===================================================================================================
# PROMPT BUILDERS  (mirror ap_scorer.py)
# ===================================================================================================

MODE_GUIDANCE = {
    "argument": ("This is an ARGUMENT essay from source(s). The thesis must take a defensible position; "
                 "evidence must support the claim and, where the sources oppose, the response should weigh "
                 "or acknowledge the other side."),
    "explanatory": ("This is an INFORMATIVE/EXPLANATORY essay from source(s). The controlling idea explains "
                    "rather than argues; evidence develops the topic with accurate, relevant source detail."),
    "analysis": ("This is a TEXT-DEPENDENT ANALYSIS essay. The response must analyze the author's moves "
                 "(how meaning/effect is built), not summarize; top-band responses reach significance "
                 "(why the move matters), not just name the device."),
}


def _build_system_prompt(rc_id: str, mode: str | None, grade_level: str = "Grade 10") -> str:
    cfg = RUBRIC_CONFIGS[rc_id]
    mode_line = MODE_GUIDANCE.get(mode or "", "")
    gate = cfg.get("gate")
    gate_line = f"\nGATE RULE: {gate['why']}" if gate else ""
    return f"""You are a calibrated {grade_level} writing scorer applying the {cfg['models']} rubric.
Score the student essay on each trait below using ONLY that trait's descriptors. Be honest and calibrated;
do not inflate. Most on-grade student essays land in the middle of each scale.

{mode_line}{gate_line}

FEEDBACK RULES:
- {grade_level} reading level.
- Name the specific trait that most limits the score and quote the student's actual words.
- Give exactly one concrete, actionable next step.
- No cheerleading. No person-praise. Use goal/now/next framing.
- Do not use em dashes; use commas, colons, or parentheses."""


def _build_user_prompt(rc_id: str, mode: str | None, student_text: str,
                       passage_text: str | None, prompt_text: str | None) -> str:
    cfg = RUBRIC_CONFIGS[rc_id]

    trait_blocks = []
    for (key, label, lo, hi) in cfg["traits"]:
        descs = cfg["trait_descriptors"][key]
        lines = "\n".join(f"    {s}: {descs[s]}" for s in range(lo, hi + 1))
        trait_blocks.append(f"  TRAIT {key} = {label} ({lo}-{hi}):\n{lines}")
    traits_spec = "\n".join(trait_blocks)

    # JSON skeleton the model must fill: one object per trait key
    trait_json = ",\n".join(
        f'    "{key}": {{ "score": {lo}, "reasoning": "..." }}' for (key, _l, lo, _hi) in cfg["traits"]
    )

    passage_block = f"\nSOURCE(S):\n---\n{passage_text}\n---\n" if passage_text else ""
    prompt_block = f"\nWRITING PROMPT:\n{prompt_text}\n" if prompt_text else ""
    scorers = cfg.get("scorers", 1)
    scorer_note = (f"\nThis form is scored by {scorers} independent scorers; report the single-scorer trait "
                   f"scores below and the engine will apply the x{scorers} multiplier for the reported total."
                   if scorers > 1 else "")

    return f"""RUBRIC: {cfg['models']} (config {rc_id}){scorer_note}
{passage_block}{prompt_block}
TRAIT DESCRIPTORS:
{traits_spec}

STUDENT ESSAY:
---
{student_text}
---

Score each trait. Respond with ONLY this JSON object:
{{
{trait_json},
    "feedback": "<2-3 sentences: name the limiting trait and one specific revision>",
    "weakest_trait": "<one trait key from above>",
    "next_step": "<one actionable revision instruction>"
}}

IMPORTANT:
- Use only the descriptors above; do not invent scores outside each trait's range.
- Quote the student's actual words when justifying a trait score.
- The weakest_trait must be one of the trait keys shown."""


def _parse_json(text: str) -> dict | None:
    text = (text or "").strip()
    if text.startswith("```"):
        lines, out, inb = text.split("\n"), [], False
        for line in lines:
            if line.startswith("```") and not inb:
                inb = True; continue
            if line.startswith("```") and inb:
                break
            if inb:
                out.append(line)
        text = "\n".join(out)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", text, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                return None
    return None


def _clamp_and_total(rc_id: str, data: dict) -> dict:
    """Clamp each trait to its range, apply the gate, apply the scorer multiplier, recompute total."""
    cfg = RUBRIC_CONFIGS[rc_id]
    ranges = {k: (lo, hi) for (k, _l, lo, hi) in cfg["traits"]}

    for key, (lo, hi) in ranges.items():
        node = data.get(key) or {}
        raw = node.get("score", lo)
        try:
            raw = int(round(float(raw)))
        except (TypeError, ValueError):
            raw = lo
        node["score"] = max(lo, min(hi, raw))
        data[key] = node

    # Gate: if the trigger trait is 0, the target trait is forced to 0. gate_applied reflects the CONDITION
    # being met (the gate is in force), not merely whether we had to change a score the model already zeroed.
    gate = cfg.get("gate")
    gate_applied = False
    if gate and data.get(gate["if_trait"], {}).get("score", None) == gate["is"]:
        gate_applied = True
        forced = data.get(gate["force_trait"]) or {}
        if forced.get("score", 0) != gate["to"]:
            forced["score"] = gate["to"]
            forced["reasoning"] = (forced.get("reasoning", "") +
                                   f" [gate applied: {gate['force_trait']} forced to {gate['to']} because "
                                   f"{gate['if_trait']} = {gate['is']}]").strip()
            data[gate["force_trait"]] = forced

    base = sum(data[k]["score"] for k in ranges)
    scorers = cfg.get("scorers", 1)
    data["raw_trait_sum"] = base
    data["scorers"] = scorers
    data["total"] = base * scorers
    data["max_score"] = config_max_score(rc_id)
    data["gate_applied"] = gate_applied
    return data


def score_rubric_essay(
    client,
    model: str,
    rc_id: str,
    student_text: str,
    mode: str | None = None,
    passage_text: str | None = None,
    prompt_text: str | None = None,
    grade_level: str = "Grade 10",
    temperature: float = 0.3,
) -> dict:
    """Score one essay on an rc.* config. Atomic (one Claude call); usable directly or as a consensus score_fn.

    Returns: {<trait_key>: {score, reasoning}, ..., total, max_score, raw_trait_sum, scorers,
              gate_applied, feedback, weakest_trait, next_step, rubric_config}.
    """
    if rc_id not in RUBRIC_CONFIGS:
        raise ValueError(f"Unknown rubric config '{rc_id}'. Known: {sorted(RUBRIC_CONFIGS)} (rc.ap -> ap_scorer).")

    system = _build_system_prompt(rc_id, mode, grade_level)
    user = _build_user_prompt(rc_id, mode, student_text, passage_text, prompt_text)

    cfg = RUBRIC_CONFIGS[rc_id]
    trait_keys = [k for (k, _l, _lo, _hi) in cfg["traits"]]
    data, content = None, ""
    for attempt in range(2):
        msg = client.messages.create(
            model=model, max_tokens=1536, temperature=temperature,
            system=system, messages=[{"role": "user", "content": user}],
        )
        content = msg.content[0].text
        data = _parse_json(content)
        if data and all(k in data for k in trait_keys):
            break
        if attempt == 0:
            user = ("Your previous response was not valid JSON or omitted required trait keys. Respond with "
                    "ONLY a JSON object containing every trait key: " + ", ".join(trait_keys) +
                    ", plus feedback, weakest_trait, next_step.\n\n" + user)

    if not data or not all(k in data for k in trait_keys):
        data = {k: {"score": 0, "reasoning": "Scoring failed."} for k in trait_keys}
        data.update({"feedback": (content[:400] if content else "Scoring failed."),
                     "weakest_trait": trait_keys[0], "next_step": "Please resubmit for grading."})

    data = _clamp_and_total(rc_id, data)
    data.setdefault("feedback", "")
    data.setdefault("weakest_trait", trait_keys[0])
    data.setdefault("next_step", "")
    data["rubric_config"] = rc_id
    if mode:
        data["mode"] = mode
    return data
