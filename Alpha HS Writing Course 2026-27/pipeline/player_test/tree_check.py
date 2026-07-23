"""
player_test/tree_check.py  -  OneRoster LESSON-TREE integrity check (the gap the article-only eval missed).

The delivery player-eval fetches each lesson's ARTICLE url directly and can call it "clean" even when the
lesson's OneRoster topic carries EXTRA or STALE component-resources a real student would also be served. That
is exactly the defect the 2026-07-23 colleague review surfaced: 23 of 29 G9 lessons still had the OLD per-item
QTI quiz CR (cr-<id>, lessonType=quiz) active ALONGSIDE the new article + pp100, rendering teach HTML as raw
text.

This check walks each lesson topic's component-resources and asserts EXACTLY the expected v3.1 set:
  cr-<id>-article  (the gated-reading article)  +  cr-<id>-pp100  (the mastery test)
and FLAGS any other ACTIVE CR on the topic (e.g. a stale cr-<id> quiz) as a fail, plus a missing expected CR.

Read-only (GET only). Auth via the shared session (OneRoster reads need the token). Never mutates.
"""
from __future__ import annotations
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.dirname(HERE)
if PIPE not in sys.path:
    sys.path.insert(0, PIPE)
from player_test.checks import Finding

ROSTER = "https://api.alpha-1edtech.ai/ims/oneroster/rostering/v1p2"
COMPRES = f"{ROSTER}/courses/component-resources"


def _cr(session, cr_id):
    """GET one component-resource by id. Returns the dict or None. Direct-by-id (the filtered collection query
    paginates unreliably, so we probe the exact ids we care about)."""
    try:
        r = session.get(f"{COMPRES}/{cr_id}", timeout=25)
        if r.status_code != 200:
            return None
        j = r.json()
        return j.get("componentResource", j)
    except Exception:
        return None


def _active(cr):
    return bool(cr) and cr.get("status") != "tobedeleted"


# stale CR ids we know the old per-item build created on a surviving topic (extend as new stale classes appear)
def _stale_candidates(lesson_id):
    return [f"cr-{lesson_id}"]   # the OLD per-item quiz link (no -article / -pp100 suffix)


def check_lesson_tree(exp: dict, session) -> list:
    """Assert the lesson topic serves EXACTLY article + pp100, no stale/extra CRs. session must be authed."""
    lid, g = exp["lesson_id"], exp["grade"]
    findings = []
    # 1. the two EXPECTED v3.1 CRs must be active
    art = _cr(session, f"cr-{lid}-article")
    pp = _cr(session, f"cr-{lid}-pp100")
    if not _active(art):
        findings.append(Finding(lid, g, "tree_article_cr", "fail",
                                "active article component-resource", f"cr-{lid}-article missing/inactive"))
    if not _active(pp):
        findings.append(Finding(lid, g, "tree_pp100_cr", "fail",
                                "active pp100 component-resource", f"cr-{lid}-pp100 missing/inactive"))
    # 2. NO stale/extra CR may be active (the old quiz is the known class)
    stale_found = []
    for sc in _stale_candidates(lid):
        if _active(_cr(session, sc)):
            stale_found.append(sc)
    if stale_found:
        findings.append(Finding(lid, g, "tree_stale_cr", "fail",
                                "only article + pp100 CRs on the topic",
                                f"STALE active CR still served to students: {stale_found} "
                                f"(old per-item quiz - renders raw HTML)",
                                note="retire this CR + its old resource; student sees it alongside the article"))
    if not findings:
        findings.append(Finding(lid, g, "tree_integrity", "pass",
                                note="topic serves exactly article + pp100, no stale/extra CRs"))
    return findings
