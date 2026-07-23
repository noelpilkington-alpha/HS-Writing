"""
external_score.py  -  the Timeback ExternalApiScore entry point for the HS Writing G9-12 courses.

The internal /grade endpoint is a test_code + question-number JOB model (built for the G3-8 AlphaTest flow).
Timeback's custom scorer (com.alpha-1edtech.ExternalApiScore) is different: it POSTs a single student response
+ a rubric to a grader URL and expects a score + feedback back SYNCHRONOUSLY. This module adds that endpoint.

Rubric configs (from the HS Writing build):
- rc.sbac (G9/G10, Smarter Balanced full-write: Org/Purpose 0-4 + Evidence/Elaboration 0-4 + Conventions 0-2
  = 10 pts) via panel_sbac. This is the CCSS-native G9/G10 rubric selected by the 2026-07-21 bake-off
  (evidence winner: mean |Δ| 7.9%, +0.4% inflation bias vs state anchors — vs STAAR's +13-18% low-end
  inflation). Two purpose profiles: argumentative | explanatory (caller sends `mode`; defaults argumentative).
- rc.staar (G9/G10, STAAR English I/II CR: Dev/Org 0-3 + Conv 0-2 = 5 pts). Items stay tagged rc.staar, but
  by default they are SCORED with the SBAC engine and normalized back to /5 (the ROUTE-ONLY ALIAS below): the
  bake-off found the STAAR engine inflates weak essays while SBAC tracks the standard, so we upgrade the
  scoring without touching the ~40 G9/G10 lesson files or the student-visible STAAR rubric block. Set
  RC_STAAR_SCORE_ENGINE=staar to force literal STAAR-native scoring.
- rc.4trait (G11/G12, NY Regents 4-criterion analytic: Content & Analysis + Command of Evidence +
  Coherence/Org/Style + Control of Conventions) via panel_ccss. The CCSS-native G11/G12 rubric (see the
  CCSS_G1112 sourcing spec). Two task profiles: argument (each criterion 0-6, total 24) | analysis (each
  0-4, total 16); caller sends `mode` (argument default). VALIDATED 2026-07-21 against the Regents anchor
  ladder (L1-6): discriminates correctly, tracks low/mid within ~8% |Δ|. CAVEAT: the top-band validation
  gap was traced to VISION-TRANSCRIPTION noise in the anchor conventions (the strongest anchors, which NY
  annotates as "virtually no errors," picked up injected misspellings), NOT engine harshness — a
  ground-truth-cleanup follow-up, not a scorer bug.
- rc.ap (G11/G12, AP Lang Row A/B/C = 6 pts) is stubbed and returns a 503 "uncalibrated". SUPERSEDED for
  G11/G12 by rc.4trait (the reskin moved G11/G12 from AP-track to CCSS); kept only for any legacy caller.

rc.staar/rc.sbac/rc.4trait reuse the panel engines; only the age band differs across grades (via _age_hint).

WIRE-SHAPE CAVEAT: the timeback skill documents the ExternalApiScore contract loosely ("receives student
response + rubric, returns score + feedback") but does NOT pin the exact request/response JSON. This endpoint
accepts a DEFENSIVE superset of likely field names and returns a superset response; the exact shape must be
confirmed against the live platform before go-live (see the OPEN item in the grader stage doc).
"""
from __future__ import annotations
import os
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

# PORTED into HS-Writing/api 2026-07-21: engine vendored as the grader_engine sub-package; auth reuses this
# app's X-API-Key (verify_api_key in main.py), not the grader repo's require_api_key. Provider = Anthropic-
# direct (set ANTHROPIC_PROVIDER=anthropic in the service env; same Opus 4.8 model as validation, no boto3).
from grader_engine.client import create_client
from grader_engine.panel_staar import score_panel_staar
from grader_engine.panel_sbac import score_panel_sbac
from grader_engine.panel_ccss import score_panel_ccss
from grader_engine.panel import score_panel  # G3-8 short-grain scorers (sentence revision/writing), grade-param
from grader_engine.panel_joey import score_panel_joey  # 3-trait paragraph engine (Ideas+Org+Conv=10), G9-12 band
from grader_engine import routing            # (unit, frq_type) -> scorer key; grader-owned SoT

router = APIRouter()

# ROUTE-ONLY ALIAS (decision 2026-07-21): the G9/G10 course items are tagged rc.staar (kept stable — the
# STAAR CR shape is the course's exam-prep target + the reskin froze rubric_ref). But the bake-off found the
# STAAR engine INFLATES weak G9/10 essays (+13-18% low-end) while the SBAC engine tracks the standard (+0.4%).
# So we SCORE incoming rc.staar (G9/10) requests with the SBAC engine and NORMALIZE the result back to the
# STAAR 5-point scale the item declares — better scoring, zero change to the 40 lesson files / rubric blocks /
# mastery scale. Set RC_STAAR_SCORE_ENGINE=staar to force the literal STAAR engine (e.g. a genuine STAAR
# exam-prep caller that wants STAAR-native scoring rather than the CCSS-calibrated SBAC scoring).
_RC_STAAR_SCORE_ENGINE = os.environ.get("RC_STAAR_SCORE_ENGINE", "sbac").strip().lower()

# Paragraph grader validation status. No grade+construct-matched paragraph ANCHOR ground truth exists (none
# published at the HS band), so this is BOUNDED validation, not an anchor bake-off. Set True on 2026-07-21
# after 3 independent reads agreed the G9-12 content-gate fix works: (A) STAAR G3-5 ECR official anchors
# exposed +11.8%/+23% low-band inflation in the baseline; the fix targeted it; (C) on 14 REAL MCAS G10
# anchor paragraphs the fixed engine tracks human quality (Pearson r=0.85, monotonic high>mid>low) with
# ZERO low-end inflation (0/6 weak-essay paras scored proficient); (B) self-authored construct set 7/8.
# Honest scope: validated for RANKING + inflation-direction on real HS prose, NOT absolute per-paragraph
# accuracy (no official paragraph scores exist to measure that). See G910_Paragraph_Validation_Report.md.
# Override to false to re-gate if a future model change shifts calibration.
_PARAGRAPH_CALIBRATED = os.environ.get("PARAGRAPH_CALIBRATED", "true").strip().lower() == "true"

# rubric_id -> config. Grade may be overridden per request.
RUBRIC_CONFIGS = {
    "rc.sbac":   {"grade": 10, "total_max": 10, "engine": "sbac"},   # G9/G10 CCSS default (bake-off winner)
    "rc.staar":  {"grade": 10, "total_max": 5, "engine": "staar"},   # G9/G10 STAAR-exam-prep target
    "rc.4trait": {"grade": 11, "total_max": 24, "engine": "ccss"},   # G11/G12 CCSS (Regents 4-criterion); total_max varies by mode
    "rc.ap":     {"grade": 11, "total_max": 6, "engine": "ap"},       # G11/G12 legacy AP; NOT calibrated -> 503
}

# SBAC purpose profiles the caller may request via `mode`.
_SBAC_MODES = {"argumentative", "explanatory"}
# rc.4trait (Regents) task profiles: argument (0-6 x4 = 24) | analysis (0-4 x4 = 16).
_CCSS_MODES = {"argument", "analysis"}


class ScoreRequest(BaseModel):
    """Defensive superset of the fields the platform's ExternalApiScore may send."""
    response: str = Field(default="", description="The student's written response (plain text).")
    rubric: str = Field(default="rc.sbac", description="Rubric config id: rc.sbac | rc.staar | rc.ap")
    grade: int | None = Field(default=None, description="Grade level (9-12). Defaults from rubric if omitted.")
    prompt: str = Field(default="", description="The task/question the student answered.")
    passage: str = Field(default="", description="The bound source text (for grounding/off-topic).")
    mode: str = Field(default="",
                      description="Writing purpose/task. rc.sbac: 'argumentative' | 'explanatory'. "
                                  "rc.4trait: 'argument' | 'analysis'. Defaults per engine if omitted.")
    grain: str = Field(default="",
                       description="Task GRAIN: sentence | paragraph | multi_paragraph | essay. Baked into the "
                                   "grader URL by the wirer from the slot's declared `unit`. Absent -> essay "
                                   "(back-compat: today's essay callers keep working unchanged).")
    frq_type: str = Field(default="",
                          description="Task CONSTRUCT: revision (transform a provided draft) | writing "
                                      "(produce from a task). Declared per slot; load-bearing at sentence/paragraph.")
    # aliases the platform might use instead of the above (accepted, best-effort mapped)
    studentResponse: str | None = None
    rubricId: str | None = None
    stimulus: str | None = None


class ScoreResponse(BaseModel):
    score: float
    maxScore: float
    feedback: str
    rubric: str
    grade: int
    breakdown: dict
    calibrated: bool
    note: str = ""


@router.post("/score", response_model=ScoreResponse, tags=["ExternalApiScore"])
def external_score(
    req: ScoreRequest,
    grain: str = Query(default=""),
    frq_type: str = Query(default=""),
):
    """Score ONE free-response answer against a rubric config. Synchronous (ExternalApiScore contract).

    Auth is applied at router-include time in main.py (dependencies=[Depends(verify_api_key)]), using this
    app's X-API-Key scheme — so this route carries no auth dependency of its own (avoids a circular import).

    GRAIN ROUTING FIX (2026-07-23): the wirer bakes grain/frq_type into the grader URL as QUERY params
    (.../score?grain=sentence&frq_type=writing). FastAPI populates the Pydantic body model from the JSON
    body ONLY, so `req.grain` was always empty on the live HTTP path and every task fell to the essay
    engine (sentence/paragraph scored 0 — GRADER_WIRING_FINDINGS Defect 1). We now read grain/frq_type
    from the QUERY string first, falling back to the body fields for non-URL callers.
    """
    response = (req.response or req.studentResponse or "").strip()
    rubric = req.rubric or req.rubricId or "rc.staar"
    passage = req.passage or req.stimulus or ""
    if rubric not in RUBRIC_CONFIGS:
        raise HTTPException(status_code=400, detail=f"unknown rubric '{rubric}'; expected {list(RUBRIC_CONFIGS)}")
    cfg = RUBRIC_CONFIGS[rubric]
    grade = req.grade or cfg["grade"]

    client = create_client()

    # ── GRAIN DISPATCH (regeneration contract) ───────────────────────────────────────────────────────
    # Route off the DECLARED (grain, frq_type) tuple, not the content. grain is baked into the grader URL by
    # the wirer from the slot's `unit`; frq_type is the declared construct. Absent grain -> essay (back-compat:
    # today's essay callers, which send no grain, fall straight through to the rubric-family dispatch below).
    # query param wins (the wirer's channel); body field is the fallback for JSON-only callers.
    grain = (grain or req.grain or "").strip().lower()
    if grain and grain != "essay":
        frq_type = (frq_type or req.frq_type or routing.default_frq_type(grain)).strip().lower()
        scorer = routing.resolve(grain, frq_type)
        if scorer is None:
            raise HTTPException(status_code=400,
                                detail=f"unsupported (grain={grain}, frq_type={frq_type}); "
                                       f"grader accepts {sorted(routing.SUPPORTED)}")
        if not routing.is_implemented(scorer):
            # e.g. paragraph is reserved in the routing table but not yet calibrated for G9-12. Fail LOUD,
            # never silently essay-grade a paragraph/sentence task.
            raise HTTPException(status_code=501,
                                detail=f"(grain={grain}, frq_type={frq_type}) -> '{scorer}' is routed but not "
                                       f"yet implemented for this grade band; implemented: "
                                       f"{sorted(routing.IMPLEMENTED)}")
        if scorer in ("sentence_revision", "sentence_writing"):
            # Reuse the VALIDATED, grade-parameterized G3-8 sentence scorers via the public score_panel API.
            # qnum selects the construct: 1-5 => sentence-revision (Skill+Conv=2); 6-10 => sentence-writing
            # (Answer+Conv=3). HYBRID: pass THIS lesson's regenerated passage+prompt+response.
            qnum = 1 if scorer == "sentence_revision" else 6
            qs = score_panel(client, grade=grade, passage=passage,
                             question=req.prompt or "(prompt not supplied)", response=response, qnum=qnum)
            return ScoreResponse(
                score=float(qs.total_score), maxScore=float(qs.total_max), feedback=qs.feedback,
                rubric=rubric, grade=grade, calibrated=True,
                breakdown={"skill_or_answer": qs.ideas_score, "skill_or_answer_max": qs.ideas_max,
                           "conventions": qs.conventions_score, "conventions_max": qs.conventions_max},
                note=(f"grain={grain} frq_type={frq_type} -> {scorer} (panel sentence scorer, "
                      f"{qs.total_max}-pt); rubric_ref '{rubric}' carried for standard-family record."))
        if scorer == "paragraph":
            # Single analytical/argumentative paragraph -> panel_joey 3-trait (Ideas+Org+Conv=10) with the
            # G9-12 band. HYBRID: pass THIS lesson's regenerated passage+prompt+response. frq_type
            # (revision|writing) both score on the same paragraph rubric (construct differs, trait scale doesn't).
            # calibrated=_PARAGRAPH_CALIBRATED: the G9-12 band is authored + bounded-validated (STAAR G3-5 ECR
            # inflation-direction check + G9-12 spot-check set), NOT anchor-bake-off-validated (no real
            # grade+construct-matched paragraph ground truth exists — see the design doc / validation report).
            qs = score_panel_joey(client, grade=grade, passage=passage,
                                  question=req.prompt or "(prompt not supplied)", response=response,
                                  qnum=11, scale=10)
            return ScoreResponse(
                score=float(qs.total_score), maxScore=float(qs.total_max), feedback=qs.feedback,
                rubric=rubric, grade=grade, calibrated=_PARAGRAPH_CALIBRATED,
                breakdown={"ideas": qs.ideas_score, "ideas_max": qs.ideas_max,
                           "organization": qs.organization_score, "organization_max": qs.organization_max,
                           "conventions": qs.conventions_score, "conventions_max": qs.conventions_max},
                note=(f"grain={grain} frq_type={frq_type} -> paragraph (panel_joey 3-trait /10, G9-12 band); "
                      f"validation={'bounded' if _PARAGRAPH_CALIBRATED else 'provisional'}; "
                      f"rubric_ref '{rubric}' carried for standard-family record."))
        # scorer == "essay" for multi_paragraph -> fall through to the rubric-family dispatch below.

    if cfg["engine"] == "sbac":
        mode = (req.mode or "argumentative").strip().lower()
        if mode not in _SBAC_MODES:
            raise HTTPException(status_code=400,
                                detail=f"unknown mode '{mode}' for rc.sbac; expected {sorted(_SBAC_MODES)}")
        qs, tr = score_panel_sbac(client, qnum=11, grade=grade, passage=passage,
                                  question=req.prompt or "(prompt not supplied)", response=response,
                                  profile=mode)
        return ScoreResponse(
            score=float(qs.total_score), maxScore=float(qs.total_max), feedback=qs.feedback,
            rubric=rubric, grade=grade, calibrated=True,
            breakdown={"organization_purpose": tr.get("org"), "organization_purpose_max": 4,
                       "evidence_elaboration": tr.get("evidence"), "evidence_elaboration_max": 4,
                       "conventions": tr.get("conventions"), "conventions_max": 2},
            note=f"rc.sbac via panel_sbac (SBAC full-write, {mode}).")

    if cfg["engine"] == "ccss":
        mode = (req.mode or "argument").strip().lower()
        if mode not in _CCSS_MODES:
            raise HTTPException(status_code=400,
                                detail=f"unknown mode '{mode}' for rc.4trait; expected {sorted(_CCSS_MODES)}")
        qs, tr = score_panel_ccss(client, qnum=11, grade=grade, passage=passage,
                                  question=req.prompt or "(prompt not supplied)", response=response,
                                  profile=mode)
        scale = tr["scale"]
        return ScoreResponse(
            score=float(tr["total"]), maxScore=float(tr["total_max"]), feedback=qs.feedback,
            rubric=rubric, grade=grade, calibrated=True,
            breakdown={"content_analysis": tr.get("content"), "content_analysis_max": scale,
                       "command_of_evidence": tr.get("evidence"), "command_of_evidence_max": scale,
                       "coherence_org_style": tr.get("coherence"), "coherence_org_style_max": scale,
                       "control_of_conventions": tr.get("conventions"), "control_of_conventions_max": scale},
            note=f"rc.4trait via panel_ccss (Regents 4-criterion, {mode}, 0-{scale}/criterion).")

    if cfg["engine"] == "staar":
        # ROUTE-ONLY ALIAS: score with the SBAC engine (bake-off winner), normalize back to the STAAR
        # 5-point scale the item declares. The item stays tagged rc.staar; only the scoring engine changes.
        if _RC_STAAR_SCORE_ENGINE == "sbac":
            # STAAR CR mode maps to SBAC's argumentative/explanatory purpose; default argumentative unless the
            # caller specifies (STAAR ECR is argumentative OR informational).
            mode = (req.mode or "argumentative").strip().lower()
            if mode not in _SBAC_MODES:
                mode = "argumentative"
            qs, tr = score_panel_sbac(client, qnum=11, grade=grade, passage=passage,
                                      question=req.prompt or "(prompt not supplied)", response=response,
                                      profile=mode)
            staar_score = round(tr["total"] / 10.0 * 5.0, 1)   # SBAC /10 -> STAAR /5, preserve the item's scale
            return ScoreResponse(
                score=float(staar_score), maxScore=5.0, feedback=qs.feedback,
                rubric=rubric, grade=grade, calibrated=True,
                breakdown={"sbac_org_purpose": tr.get("org"), "sbac_evidence_elab": tr.get("evidence"),
                           "sbac_conventions": tr.get("conventions"), "sbac_total_of_10": tr.get("total"),
                           "normalized_to_staar_5": staar_score},
                note=(f"rc.staar item scored via SBAC engine ({mode}) per the 2026-07-21 route-only alias "
                      f"(SBAC {tr.get('total')}/10 -> {staar_score}/5); STAAR engine avail. via "
                      f"RC_STAAR_SCORE_ENGINE=staar."))
        # literal STAAR engine (RC_STAAR_SCORE_ENGINE=staar): STAAR-native scoring
        qs = score_panel_staar(client, qnum=1, grade=grade, passage=passage,
                               question=req.prompt or "(prompt not supplied)", response=response)
        return ScoreResponse(
            score=float(qs.total_score), maxScore=float(qs.total_max), feedback=qs.feedback,
            rubric=rubric, grade=grade, calibrated=True,
            breakdown={"development": qs.ideas_score, "development_max": qs.ideas_max,
                       "conventions": qs.conventions_score, "conventions_max": qs.conventions_max},
            note="rc.staar via panel_staar (STAAR English I/II CR rubric, literal engine).")

    # rc.ap: legacy AP path, never calibrated + superseded by rc.4trait for G11/G12. Fail LOUD.
    raise HTTPException(status_code=503,
                        detail="rc.ap (AP Lang Row A/B/C) is uncalibrated and superseded: G11/G12 now use "
                               "rc.4trait (Regents 4-criterion CCSS). Live: rc.sbac (G9/10), rc.staar (G9/10), "
                               "rc.4trait (G11/12).")
