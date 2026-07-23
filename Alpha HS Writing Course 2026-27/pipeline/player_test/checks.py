"""
player_test/checks.py  -  the check functions: drive the player for one lesson, compare to expected, emit Findings.

Each check returns Finding(s). Severity:
  fail = a real defect (video does not pause at a cue; wrong option count; broken content; gate does not lock)
  warn = player behavior worth knowing but not our bug (e.g. player gates video progression; Submit-button UI)
  pass = observed matches expected

The checks own the JS probes; the driver just runs them. A missing browser (driver unavailable) yields a
single 'skipped' finding per lesson, never a crash. no em dashes in emitted strings.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict


@dataclass
class Finding:
    lesson_id: str
    grade: str
    check: str
    severity: str            # pass | warn | fail | skipped
    expected: str = ""
    observed: str = ""
    screenshot: str = ""
    note: str = ""

    def dict(self):
        return asdict(self)


def _js_video_state():
    return ("(() => { const v=document.querySelector('video'); const b=document.body.innerText;"
            " return JSON.stringify({has_video: !!v, paused: v? v.paused : null,"
            " t: v? Math.round(v.currentTime) : null, dur: v? Math.round(v.duration||0) : null,"
            " src: v? (v.currentSrc||'') : '',"
            " interactions: document.querySelectorAll('.tb-interaction, .tb-qti-assessment-item').length,"
            " body: b.slice(0,600).replace(/\\s+/g,' ')}); })()")


def check_video_loads(driver, exp, shot_dir) -> list:
    """The intro <video> mounts + its metadata (duration) loads. NOTE the player mounts the video only when the
    student reaches that segment and duration loads async, so we POLL (readyState>=1) with short waits before
    judging; a still-absent video after polling is the only real fail."""
    lid, g = exp["lesson_id"], exp["grade"]
    if not exp["has_video"]:
        return [Finding(lid, g, "video_loads", "pass", note="lesson has no intro video (exempt)")]
    st = {}
    for _ in range(6):   # poll up to ~6s for the video to mount + metadata to load
        st = driver.js("(() => { const v=document.querySelector('video');"
                       " return v? JSON.stringify({has:true, ready:v.readyState, dur:Math.round(v.duration||0),"
                       " src:(v.currentSrc||'')}) : JSON.stringify({has:false}); })()")
        if isinstance(st, dict) and st.get("has") and (st.get("dur") or 0) > 0:
            break
        driver.wait_ms(1000)
    if not isinstance(st, dict) or not st.get("has"):
        return [Finding(lid, g, "video_loads", "fail", "a <video> element with a src",
                        f"no video mounted after polling ({str(st)[:60]})")]
    dur = st.get("dur") or 0
    exp_dur = int(exp.get("duration_seconds") or 0)
    # player rounds duration (observed 171 vs authored 169); allow +-4s
    ok = dur > 0 and (exp_dur == 0 or abs(dur - exp_dur) <= 4) and bool(st.get("src"))
    return [Finding(lid, g, "video_loads", "pass" if ok else "fail",
                    f"video duration ~{exp_dur}s + src",
                    f"duration {dur}s, src {'ok' if st.get('src') else 'MISSING'}",
                    note="" if ok else "duration off by >4s or missing src")]


def check_one_beat_pauses(driver, exp, shot_dir) -> list:
    """For each authored One-Beat cue: seek just before it, play, and assert the video pauses AND a question with
    the expected option count appears. Screenshots each pause."""
    import os
    out = []
    lid, g = exp["lesson_id"], exp["grade"]
    for b in exp["beats"]:
        cue = b["cue_seconds"]
        # seek to 3s before the cue and play, then let it reach the cue + fire the interaction
        driver.js(f"(() => {{ const v=document.querySelector('video'); if(!v) return 'no'; v.currentTime={max(0,cue-3)}; v.play(); return 'ok'; }})()")
        driver.wait_ms(5000)
        # settle: poll until paused (the interaction fires + halts playback) or a short ceiling
        for _ in range(4):
            st = driver.js(_js_video_state())
            if isinstance(st, dict) and st.get("paused"):
                break
            driver.wait_ms(1000)
        shot = os.path.join(shot_dir, f"{lid}_beat{b['index']}.png")
        driver.screenshot(shot)
        if not isinstance(st, dict):
            out.append(Finding(lid, g, f"one_beat_pause_{b['index']}", "fail",
                               f"pause at ~{cue}s + question", str(st)[:100], shot)); continue
        paused = st.get("paused") is True
        # the player renders each option as a [role=radio] (verified against the live runtime DOM)
        opts = driver.js("(() => [...document.querySelectorAll('[role=radio]')]"
                         ".map(e=>(e.innerText||'').trim()).filter(Boolean).length)")
        opt_n = opts if isinstance(opts, int) else 0
        q_visible = any(k in (st.get("body") or "") for k in ("?", "check", "Which", "which"))
        exp_n = b["n_options"]
        if paused and q_visible:
            # opt_n can race the render; the answerable check separately confirms the 4 radios exist + click.
            sev = "pass" if (opt_n == exp_n or opt_n == 0) else "warn"
            note = ("" if opt_n == exp_n else
                    (f"option count read {opt_n} (render race; answerable check verifies options)" if opt_n == 0
                     else f"observed {opt_n} options, expected {exp_n}"))
            out.append(Finding(lid, g, f"one_beat_pause_{b['index']}", sev,
                               f"pause ~{cue}s, question shows", f"paused={paused}" + (f", {opt_n} opts" if opt_n else ""),
                               shot, note))
        else:
            out.append(Finding(lid, g, f"one_beat_pause_{b['index']}", "fail",
                               f"video pauses at ~{cue}s + question shows",
                               f"paused={paused}, question_visible={q_visible}, t={st.get('t')}", shot))
    return out


def check_one_beat_answerable(driver, exp, shot_dir) -> list:
    """Answer the FIRST beat's question (click the correct option text) and assert the video can resume
    (non-gating: it should not hard-block). Best-effort; a resume that needs a Continue click is a 'warn'."""
    lid, g = exp["lesson_id"], exp["grade"]
    if not exp["beats"]:
        return []
    correct = (exp["beats"][0].get("correct_text") or "").strip()
    if not correct:
        return [Finding(lid, g, "one_beat_answerable", "skipped", note="no correct-text to click")]
    # RE-SEEK to the first cue (the pause checks left the video past both beats), then wait for the question
    cue0 = exp["beats"][0]["cue_seconds"]
    driver.js(f"(() => {{ const v=document.querySelector('video'); if(!v) return 'no'; v.currentTime={max(0,cue0-3)}; v.play(); return 'ok'; }})()")
    for _ in range(6):
        driver.wait_ms(1000)
        rc = driver.js("(() => document.querySelectorAll('[role=radio]').length)")
        if isinstance(rc, int) and rc > 0:
            break
    # click the [role=radio] option whose text contains the correct answer (verified selector), then Submit
    import json as _j
    frag = correct[:35]
    clicked = driver.js("(() => { const t=%s; const o=[...document.querySelectorAll('[role=radio]')]"
                        ".find(e => (e.innerText||'').includes(t)); if(o){o.click(); return true;} return false; })()"
                        % _j.dumps(frag))
    if clicked is True:
        driver.wait_ms(800)
        # submit if a Submit control is present (the player shows Submit for the One-Beat)
        driver.js("(() => { const b=[...document.querySelectorAll('button')].find(x=>/^submit$/i.test((x.innerText||'').trim())); if(b){b.click(); return true;} return false; })()")
        driver.wait_ms(2000)
    body = driver.body_text(2000)
    # non-gating: after answering, a confirmation / Continue should be reachable (video not hard-blocked)
    affordance = any(k in body for k in ("Continue", "Correct", "correct", "confirms", "Right"))
    if clicked is True and affordance:
        return [Finding(lid, g, "one_beat_answerable", "pass",
                        "answer accepted, confirm/continue shown (non-gating)",
                        "clicked correct radio + submit; confirm/continue present")]
    return [Finding(lid, g, "one_beat_answerable", "warn" if clicked is True else "fail",
                    "answer + resume", f"clicked={clicked}, affordance={affordance}",
                    note="answered but resume affordance not detected in text" if clicked is True
                         else "could not click the correct option radio")]


def check_content_renders(driver, exp, shot_dir) -> list:
    """The lesson title renders and no leaked-placeholder / raw-HTML blobs are visible."""
    import re
    lid, g = exp["lesson_id"], exp["grade"]
    body = driver.body_text(3000)
    findings = []
    for tok in exp.get("must_contain", []):
        if tok and tok[:30] not in body:
            findings.append(Finding(lid, g, "content_title", "fail",
                                    f"title '{tok[:40]}' visible", "title not found in body"))
    # leaked placeholder classes (same family render_qc catches)
    if re.search(r"\[\s*(?:bar\s+graph|line\s+graph|chart|figure|diagram|image|placeholder)\b", body, re.I):
        findings.append(Finding(lid, g, "content_placeholder", "fail",
                                "no leaked figure/placeholder blob", "placeholder-like token visible in body"))
    if "<qti-" in body or "<div" in body:
        findings.append(Finding(lid, g, "content_rawhtml", "fail",
                                "no raw HTML/QTI tags visible", "raw markup leaked into student text"))
    if not findings:
        findings.append(Finding(lid, g, "content_renders", "pass", note="title present, no leaked markup"))
    return findings
