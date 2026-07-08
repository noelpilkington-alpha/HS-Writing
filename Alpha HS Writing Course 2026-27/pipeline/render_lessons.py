"""
render_lessons.py  -  Render the G10 Lesson_Bank into one browsable HTML file for evaluation.

Imports every Lesson_Bank_G10/lesson_*.py module, pulls its LESSONS list, runs the QC harness on each,
and renders the full SRSD item-sequence (every slot) as a Timeback-style lesson walkthrough with a live
QC panel per lesson. This is the human-review surface: it shows exactly what each lesson delivers, slot by
slot, and proves (green/red) that every lesson passed the machine gates.

Matches the house visual style (purple accent, load colors) used by model_lesson_specs.html.
Dependency-free (stdlib only). Run: python pipeline/render_lessons.py  ->  writes lesson_bank.html
"""
from __future__ import annotations
import os, sys, glob, importlib.util, html

HERE = os.path.dirname(__file__)
LESSON_DIR = os.path.join(HERE, "..", "Lesson_Bank_G10")
OUT = os.path.join(HERE, "..", "lesson_bank.html")
sys.path.insert(0, HERE)
from lesson_contract import qc_lesson, LESSON_TYPES, KIND_QTI, NATIVE_XML_REQUIRED
from bank_loader import load_bank

# Index every stimulus's passage text by id, so the renderer can INLINE the bound source a student reads
# (a lesson binds a stimulus by id; without the text you cannot evaluate the lesson). Built once.
def _stimulus_text_index() -> dict:
    idx = {}
    try:
        ir = load_bank(run_qc=False)
        for s in (ir.stimuli + ir.singles):
            passages = [{"title": getattr(p, "title", ""), "text": getattr(p, "text", "")}
                        for p in getattr(s, "passages", [])]
            idx[s.id] = {"prompt": getattr(s, "prompt", ""), "passages": passages,
                         "mode": getattr(s, "mode", ""), "bucket": getattr(s, "bucket", "")}
    except Exception as e:
        print(f"  !! stimulus index failed: {e!r}")
    return idx

STIM_TEXT = _stimulus_text_index()

ROLE_COLOR = {"TEACH": "#0d9488", "MODEL": "#7c3aed", "SUPPORTED": "#2563eb",
              "INDEPENDENT": "#d97706", "TRANSFER": "#be123c"}
KIND_LABEL = {
    "stimulus_display": "Stimulus (source display)", "teach_card": "Teach card",
    "annotated_before_after": "Annotated before/after", "discrimination": "Discrimination (choice)",
    "predict_the_fix": "Predict-the-fix (choice + reveal)", "self_score": "Self-score (calibration)",
    "production_frq": "Production FRQ (grader)", "diagnosis_frq": "Diagnosis FRQ (grader)",
    "sr_practice": "SR practice item (choice)",
}

def esc(s: str) -> str:
    return html.escape(s or "")

def load_lessons():
    lessons = []
    for f in sorted(glob.glob(os.path.join(LESSON_DIR, "lesson_*.py"))):
        name = os.path.splitext(os.path.basename(f))[0]
        spec = importlib.util.spec_from_file_location(name, f)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            print(f"  !! failed to import {name}: {e!r}")
            continue
        for L in getattr(mod, "LESSONS", []):
            qc_lesson(L)
            lessons.append((os.path.basename(f), L))
    return lessons

def render_slot(i, s):
    qti = KIND_QTI.get(s.kind, "?")
    xml = " · XML POST" if qti in NATIVE_XML_REQUIRED else ""
    ref = f'<span class="ref">binds {esc(s.ref)}</span>' if s.ref else '<span class="auth">authored</span>'
    bank = f'<span class="bank">bank: {esc(s.bank)}</span>' if s.bank else ""
    rub = f'<span class="rub">{esc(s.rubric_ref)}</span>' if s.rubric_ref else ""
    scored = '<span class="scored">scored</span>' if s.scored else ""
    gc = '<span class="gc">Grade-C labeled</span>' if s.labeled_grade_c else ""
    col = ROLE_COLOR.get(s.role, "#64748b")
    body = f'<div class="body">{esc(s.body)}</div>' if s.body else ""
    fb = f'<div class="fb"><b>Reveal:</b> {esc(s.feedback)}</div>' if s.feedback else ""
    # INLINE the bound stimulus's actual passage text (the source the student reads) so the lesson is
    # evaluable. Only for slots that bind a stimulus present in the index.
    stim = ""
    if s.ref and s.ref in STIM_TEXT:
        st = STIM_TEXT[s.ref]
        parts = []
        if st.get("prompt"):
            parts.append(f'<div class="stimprompt"><b>Prompt:</b> {esc(st["prompt"])}</div>')
        for p in st["passages"]:
            parts.append(f'<div class="passage"><div class="ptitle">{esc(p["title"])}</div>'
                         f'<div class="ptext">{esc(p["text"])}</div></div>')
        stim = (f'<details class="stimwrap"><summary>Bound source text ({esc(s.ref)}) '
                f'&mdash; {len(st["passages"])} passage(s), click to read</summary>{"".join(parts)}</details>')
    return f"""
    <div class="slot">
      <div class="rail" style="background:{col}"></div>
      <div class="slotmain">
        <div class="slothd">
          <span class="role" style="color:{col}">{esc(s.role)}</span>
          <span class="kind">{esc(KIND_LABEL.get(s.kind, s.kind))}</span>
          <span class="qti">{esc(qti)}{xml}</span>
        </div>
        <div class="slottitle">{i}. {esc(s.title)}</div>
        <div class="chips">{ref} {bank} {rub} {scored} {gc}</div>
        {body}{fb}{stim}
      </div>
    </div>"""

def render_lesson(fname, L):
    r = L.qc
    tname = LESSON_TYPES.get(L.lesson_type, ("?",))[0]
    ok = r["passed"]
    seq = " → ".join(s.role[0] + ":" + s.kind.replace("_", "") for s in L.slots)
    gates = "".join(
        f'<span class="g {"gp" if g["passed"] else "gf"}" title="{esc(g["detail"])}">{esc(n)}</span>'
        for n, g in r["gates"].items())
    bound = sorted({s.ref for s in L.slots if s.ref})
    boundhtml = "".join(f"<code>{esc(b)}</code> " for b in bound) or "<i>none</i>"
    slots = "".join(render_slot(i + 1, s) for i, s in enumerate(L.slots))
    return f"""
  <section class="lesson" id="{esc(L.id)}">
    <div class="lhd t{L.lesson_type}">
      <div class="lnum">TYPE {L.lesson_type}</div>
      <div class="ltitle">{esc(L.title)}
        <span class="badge {'ok' if ok else 'bad'}">{'PASS' if ok else 'FAIL'} · {sum(1 for g in r['gates'].values() if g['passed'])}/{len(r['gates'])} gates</span>
      </div>
      <div class="lmeta">{esc(tname)} · {esc(L.id)} · {esc(L.grade)} · {len(L.slots)} slots · <span class="file">{esc(fname)}</span></div>
    </div>
    <div class="ltarget"><b>Target:</b> {esc(L.target)}</div>
    <div class="lacc">ACC: {" ".join(f'<code>{esc(t)}</code>' for t in L.acc_tags)} &nbsp;|&nbsp; Fade-ledger moves: {", ".join(esc(m) for m in L.fade_ledger_moves) or "none"}</div>
    <div class="lseq"><b>Sequence:</b> {esc(seq)}</div>
    <div class="lbound"><b>Bound bank refs:</b> {boundhtml}</div>
    <div class="gates">{gates}</div>
    <div class="slots">{slots}</div>
  </section>"""

def main():
    lessons = load_lessons()
    lessons.sort(key=lambda t: t[1].lesson_type)
    npass = sum(1 for _, L in lessons if L.qc["passed"])
    total_slots = sum(len(L.slots) for _, L in lessons)
    total_frq = sum(1 for _, L in lessons for s in L.slots if s.kind in ("production_frq", "diagnosis_frq"))
    total_bound = len({s.ref for _, L in lessons for s in L.slots if s.ref})
    toc = "".join(
        f'<a href="#{esc(L.id)}" class="tocitem {"tp" if L.qc["passed"] else "tf"}">'
        f'<b>T{L.lesson_type}</b> {esc(LESSON_TYPES.get(L.lesson_type, ("?",))[0])}</a>'
        for _, L in lessons)
    body = "".join(render_lesson(f, L) for f, L in lessons)
    doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>G10 Lesson Bank — Model Lessons (QC-verified)</title>
<style>
:root{{--ink:#1e293b;--muted:#64748b;--line:#e2e8f0;--panel:#f8fafc;--accent:#7c3aed;--accentbg:#f5f3ff;
--ok:#166534;--okbg:#dcfce7;--bad:#991b1b;--badbg:#fee2e2;}}
*{{box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);
line-height:1.55;margin:0;background:#fff}}
.wrap{{max-width:1080px;margin:0 auto;padding:28px 22px 90px}}
header.top{{border-bottom:3px solid var(--accent);padding-bottom:14px;margin-bottom:10px}}
h1{{font-size:1.7rem;margin:0 0 4px}}
.sub{{color:var(--muted);font-size:.94rem;margin:0}}
.summary{{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}}
.stat{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 16px;min-width:120px}}
.stat .n{{font-size:1.5rem;font-weight:800;color:var(--accent)}}
.stat .l{{font-size:.72rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}}
.prov{{background:var(--accentbg);border-left:4px solid var(--accent);padding:11px 15px;border-radius:0 8px 8px 0;
margin:14px 0;font-size:.84rem}}
.toc{{display:flex;flex-wrap:wrap;gap:7px;margin:14px 0 26px}}
.tocitem{{text-decoration:none;color:var(--ink);border:1px solid var(--line);border-radius:20px;padding:5px 13px;font-size:.82rem}}
.tocitem b{{color:var(--accent)}}
.tocitem.tp{{border-color:#86efac;background:var(--okbg)}} .tocitem.tf{{border-color:#fca5a5;background:var(--badbg)}}
.lesson{{border:1px solid var(--line);border-radius:14px;margin:22px 0;overflow:hidden}}
.lhd{{padding:14px 18px;color:#fff;background:var(--accent)}}
.lhd.t1,.lhd.t6{{background:#0d9488}} .lhd.t2,.lhd.t3,.lhd.t8{{background:#2563eb}}
.lhd.t4{{background:#be123c}} .lhd.t5,.lhd.t7{{background:#d97706}}
.lnum{{font-size:.72rem;font-weight:700;opacity:.9;letter-spacing:.06em}}
.ltitle{{font-size:1.2rem;font-weight:800;margin:2px 0}}
.badge{{font-size:.68rem;font-weight:700;padding:3px 10px;border-radius:20px;vertical-align:middle;margin-left:8px}}
.badge.ok{{background:var(--okbg);color:var(--ok)}} .badge.bad{{background:var(--badbg);color:var(--bad)}}
.lmeta{{font-size:.74rem;opacity:.92}} .lmeta .file{{font-family:ui-monospace,Menlo,monospace}}
.ltarget,.lacc,.lseq,.lbound{{padding:9px 18px;font-size:.84rem;border-bottom:1px solid var(--line);background:var(--panel)}}
.lacc code,.lbound code{{background:#eef2ff;color:#4338ca;border-radius:5px;padding:1px 6px;font-size:.78rem}}
.lseq{{font-family:ui-monospace,Menlo,monospace;font-size:.76rem;color:var(--muted)}}
.gates{{display:flex;flex-wrap:wrap;gap:5px;padding:12px 18px}}
.g{{font-size:.68rem;padding:3px 9px;border-radius:6px;font-family:ui-monospace,Menlo,monospace;cursor:help}}
.gp{{background:var(--okbg);color:var(--ok)}} .gf{{background:var(--badbg);color:var(--bad);font-weight:700}}
.slots{{padding:6px 18px 18px}}
.slot{{display:flex;gap:0;margin:10px 0;border:1px solid var(--line);border-radius:10px;overflow:hidden}}
.rail{{width:6px;flex:none}}
.slotmain{{padding:11px 15px;flex:1}}
.slothd{{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}}
.role{{font-size:.68rem;font-weight:800;letter-spacing:.05em}}
.kind{{font-size:.8rem;font-weight:700}}
.qti{{font-size:.68rem;color:var(--muted);font-family:ui-monospace,Menlo,monospace;margin-left:auto}}
.slottitle{{font-size:.92rem;font-weight:600;margin:3px 0 5px}}
.chips{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:6px}}
.chips span{{font-size:.68rem;padding:2px 8px;border-radius:12px}}
.ref{{background:#e0e7ff;color:#3730a3;font-family:ui-monospace,Menlo,monospace}}
.auth{{background:#f1f5f9;color:var(--muted)}}
.bank{{background:#ecfeff;color:#0e7490}} .rub{{background:#fef3c7;color:#92400e;font-family:ui-monospace,Menlo,monospace}}
.scored{{background:#dcfce7;color:#166534}} .gc{{background:#fae8ff;color:#86198f}}
.body{{font-size:.85rem;white-space:pre-wrap;background:#fff;border-left:3px solid var(--line);padding:6px 12px;margin-top:4px}}
.fb{{font-size:.82rem;background:#f5f3ff;border-left:3px solid var(--accent);padding:6px 12px;margin-top:6px;border-radius:0 6px 6px 0}}
.stimwrap{{margin-top:8px;border:1px solid #bae6fd;border-radius:8px;background:#f0f9ff;padding:4px 10px}}
.stimwrap summary{{cursor:pointer;font-size:.78rem;font-weight:700;color:#0369a1;padding:4px 0}}
.stimprompt{{font-size:.82rem;color:#0c4a6e;margin:6px 0;padding:6px 10px;background:#e0f2fe;border-radius:6px}}
.passage{{margin:8px 0}}
.ptitle{{font-size:.82rem;font-weight:700;color:#075985;margin-bottom:2px}}
.ptext{{font-size:.83rem;line-height:1.5;white-space:pre-wrap;background:#fff;border-left:3px solid #7dd3fc;padding:8px 12px;border-radius:0 6px 6px 0}}
.fb b{{color:var(--accent)}}
footer{{margin-top:40px;font-size:.78rem;color:var(--muted);border-top:1px solid var(--line);padding-top:16px}}
</style></head><body><div class="wrap">
<header class="top"><h1>Grade 10 Lesson Bank &mdash; Model Lessons</h1>
<p class="sub">The 8 reusable, council-adjudicated lesson TYPES, each assembled as a Timeback assessment-test
(SRSD item sequence) and machine-verified against the 11-gate lesson contract.</p></header>
<div class="prov"><b>What this is:</b> each lesson is an ORDERED item sequence (Teach &rarr; Model &rarr;
Supported &rarr; Independent &rarr; Transfer) that binds real bank artifacts (stimuli + SR/CR items) and
authors the connective slots. The Model stage is the modality-corrected 4-mechanism sequence (annotated
before/after &rarr; predict-the-fix &rarr; feedback on the student's own draft &rarr; self-diagnosis), NOT a
passive-read think-aloud. Every gate below passed on the machine harness; hover a gate chip for its check.</div>
<div class="summary">
  <div class="stat"><div class="n">{len(lessons)}</div><div class="l">lesson types</div></div>
  <div class="stat"><div class="n">{npass}/{len(lessons)}</div><div class="l">QC pass</div></div>
  <div class="stat"><div class="n">{total_slots}</div><div class="l">total slots</div></div>
  <div class="stat"><div class="n">{total_frq}</div><div class="l">graded FRQ slots</div></div>
  <div class="stat"><div class="n">{total_bound}</div><div class="l">bound bank refs</div></div>
</div>
<div class="toc">{toc}</div>
{body}
<footer>Generated by pipeline/render_lessons.py from the Lesson_Bank_G10 modules. Green gate chips = the
machine QC contract (pipeline/lesson_contract.py) passed. FRQ slots route to the external grader via the
listed rc.* rubric config. XML POST flagged where the Timeback interaction requires it.</footer>
</div></body></html>"""
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print(f"Rendered {len(lessons)} lessons ({npass} pass) -> {os.path.relpath(OUT, HERE)}")
    for f, L in lessons:
        print(f"  [{'PASS' if L.qc['passed'] else 'FAIL'}] T{L.lesson_type} {L.id}  ({len(L.slots)} slots)  {f}")

if __name__ == "__main__":
    main()
