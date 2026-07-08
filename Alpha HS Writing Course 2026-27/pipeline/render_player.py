"""
render_player.py  -  Render a lesson as a STUDENT-FACING Timeback-player mock (one screen at a time).

This is the "what the learner sees" view, distinct from render_lessons.py (the developer QC surface). It
imports a lesson module, walks its slots in order, and emits a single self-contained HTML file that mimics
the Timeback assessment-player flow:
  - teach_card / annotated_before_after  -> a display screen with a Continue button
  - stimulus_display                     -> the bound source passage shown in a scrolling reading pane
  - discrimination / predict_the_fix     -> a CHOICE item: radio options, Submit, then reveal correct/feedback
  - production_frq / diagnosis_frq        -> an EXTENDED-TEXT item: textarea + "Submit to grader" (mock)

HONEST FIDELITY NOTE (printed in the page banner): this preview uses JavaScript to simulate the player's
one-item-at-a-time flow. It is NOT the QTI payload (Timeback strips JS from stimuli). It faithfully mirrors
the INTERACTION MODEL (single interaction per item, choice select->submit->feedback, extended-text ->
external grader, display-only stimuli) and the ACTUAL authored content (parsed from the lesson object, so it
cannot drift), but it does not reproduce Timeback's production CSS.

Dependency-free (stdlib only). Run: python pipeline/render_player.py [lesson_file] -> writes <lesson>_player.html
"""
from __future__ import annotations
import os, sys, re, html, importlib.util, json

HERE = os.path.dirname(__file__)
LESSON_DIR = os.path.join(HERE, "..", "Lesson_Bank_G10")
sys.path.insert(0, HERE)
from bank_loader import load_bank

CHOICE_KINDS = {"discrimination", "predict_the_fix", "sr_practice", "self_score"}
FRQ_KINDS = {"production_frq", "diagnosis_frq"}
DISPLAY_KINDS = {"teach_card", "annotated_before_after"}

ROLE_LABEL = {"TEACH": "Learn", "MODEL": "Watch", "SUPPORTED": "Practice (guided)",
              "INDEPENDENT": "Practice (on your own)", "TRANSFER": "Try it on something new"}


def esc(s: str) -> str:
    return html.escape(s or "")


def stimulus_index() -> dict:
    idx = {}
    ir = load_bank(run_qc=False)
    for s in (ir.stimuli + ir.singles):
        idx[s.id] = {"title": (s.passages[0].title if s.passages else s.id),
                     "passages": [{"title": p.title, "text": p.text} for p in s.passages]}
    return idx


def parse_choice(body: str, feedback: str) -> dict:
    """Pull stem, options A-D, correct letter, and explanation out of a choice slot's prose."""
    # options begin at the first "(A)"
    m = re.search(r"\(A\)", body)
    stem = body[:m.start()].strip() if m else body.strip()
    opt_region = body[m.start():] if m else ""
    # cut trailing explanation that starts at "Correct:" or "The answer is" (discrimination embeds it in body)
    expl_in_body = ""
    cut = re.search(r"(Correct:|The answer is|Feedback\b)", opt_region)
    if cut:
        expl_in_body = opt_region[cut.start():].strip()
        opt_region = opt_region[:cut.start()]
    # split options on the (A)/(B)/(C)/(D) markers
    parts = re.split(r"\(([A-D])\)\s*", opt_region)
    options = []
    # parts = ['', 'A', 'text', 'B', 'text', ...]
    for i in range(1, len(parts) - 1, 2):
        letter = parts[i]
        text = parts[i + 1].strip().rstrip(".").strip()
        options.append({"letter": letter, "text": text})
    # correct letter from body-explanation or feedback
    corr = None
    for src in (expl_in_body, feedback or ""):
        cm = re.search(r"(?:Correct|answer is|answer:)\s*:?\s*([A-D])\b", src)
        if cm:
            corr = cm.group(1); break
    explanation = (feedback or expl_in_body or "").strip()
    return {"stem": stem, "options": options, "correct": corr, "explanation": explanation}


def build_screens(L, stim) -> list[dict]:
    screens = []
    for i, s in enumerate(L.slots):
        base = {"n": i + 1, "role": s.role, "role_label": ROLE_LABEL.get(s.role, s.role),
                "kind": s.kind, "title": s.title}
        if s.kind in CHOICE_KINDS:
            base["type"] = "choice"
            base.update(parse_choice(s.body, s.feedback))
        elif s.kind in FRQ_KINDS:
            base["type"] = "frq"
            base["prompt"] = s.body
            base["rubric"] = s.rubric_ref or ""
        elif s.kind == "stimulus_display":
            base["type"] = "source"
            base["body"] = s.body
            base["passages"] = stim.get(s.ref, {}).get("passages", [])
            base["source_id"] = s.ref
        else:  # teach_card, annotated_before_after
            base["type"] = "read"
            base["body"] = s.body
        screens.append(base)
    return screens


def render(lesson_file: str) -> str:
    name = os.path.splitext(os.path.basename(lesson_file))[0]
    spec = importlib.util.spec_from_file_location(name, lesson_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    L = mod.LESSON if hasattr(mod, "LESSON") else mod.LESSONS[0]
    stim = stimulus_index()
    screens = build_screens(L, stim)
    data = json.dumps(screens)
    out = os.path.join(HERE, "..", f"{name}_player.html")
    doc = _HTML.replace("__TITLE__", esc(L.title)).replace("__TARGET__", esc(L.target)) \
               .replace("__COUNT__", str(len(screens))).replace("__DATA__", data)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(doc)
    return out


# Single-file player. JS drives the one-screen-at-a-time flow (a LOCAL simulation; not the QTI payload).
_HTML = r"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__ - student view</title>
<style>
:root{--ink:#1e293b;--muted:#64748b;--line:#e2e8f0;--bg:#f1f5f9;--card:#fff;--brand:#2563eb;
--ok:#166534;--okbg:#dcfce7;--bad:#991b1b;--badbg:#fee2e2;--src:#0369a1;--srcbg:#f0f9ff;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.6}
.banner{background:#0f172a;color:#cbd5e1;font-size:.72rem;padding:6px 16px;text-align:center}
.banner b{color:#fff}
.topbar{background:var(--card);border-bottom:1px solid var(--line);padding:12px 20px;position:sticky;top:0;z-index:5}
.topbar .t{font-weight:800;font-size:1rem}
.topbar .sub{color:var(--muted);font-size:.8rem;margin-top:2px}
.progwrap{max-width:820px;margin:10px auto 0;padding:0 20px}
.progbar{height:6px;background:var(--line);border-radius:6px;overflow:hidden}
.progfill{height:100%;background:var(--brand);width:0;transition:width .25s}
.progtext{font-size:.72rem;color:var(--muted);margin-top:4px}
.stage{max-width:820px;margin:22px auto;padding:0 20px 60px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:24px 26px;box-shadow:0 1px 3px rgba(0,0,0,.05)}
.phase{display:inline-block;font-size:.68rem;font-weight:800;letter-spacing:.05em;text-transform:uppercase;color:var(--brand);background:#eff6ff;padding:3px 10px;border-radius:20px;margin-bottom:10px}
.qtitle{font-size:1.15rem;font-weight:800;margin:0 0 14px}
.body{white-space:pre-wrap;font-size:.98rem}
.stem{font-size:1rem;margin-bottom:14px;white-space:pre-wrap}
.opts{display:flex;flex-direction:column;gap:10px;margin:8px 0 4px}
.opt{border:2px solid var(--line);border-radius:10px;padding:12px 14px;cursor:pointer;display:flex;gap:10px;align-items:flex-start;font-size:.95rem;background:#fff}
.opt:hover{border-color:#93c5fd}
.opt .let{font-weight:800;color:var(--brand);flex:none}
.opt.sel{border-color:var(--brand);background:#eff6ff}
.opt.correct{border-color:var(--ok);background:var(--okbg)}
.opt.wrong{border-color:var(--bad);background:var(--badbg)}
.opt.disabled{cursor:default;opacity:.85}
.reveal{margin-top:16px;padding:13px 16px;border-radius:10px;font-size:.92rem;white-space:pre-wrap;display:none}
.reveal.show{display:block}
.reveal.rc{background:var(--okbg);border:1px solid #86efac}
.reveal.rw{background:var(--badbg);border:1px solid #fca5a5}
.reveal b{display:block;margin-bottom:4px}
.srcpane{background:var(--srcbg);border:1px solid #bae6fd;border-radius:10px;padding:6px 18px;margin-top:12px;max-height:340px;overflow:auto}
.srctitle{font-weight:800;color:var(--src);font-size:.9rem;margin:12px 0 4px}
.srctext{white-space:pre-wrap;font-size:.9rem;line-height:1.55}
textarea{width:100%;min-height:150px;border:2px solid var(--line);border-radius:10px;padding:12px;font-family:inherit;font-size:.95rem;resize:vertical}
textarea:focus{border-color:var(--brand);outline:none}
.goal{background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:10px 14px;font-size:.86rem;margin:10px 0}
.goal b{color:#92400e}
.graderbox{margin-top:14px;padding:13px 16px;border-radius:10px;background:#f5f3ff;border:1px solid #ddd6fe;font-size:.9rem;display:none}
.graderbox.show{display:block}
.nav{display:flex;justify-content:space-between;align-items:center;margin-top:22px}
.btn{background:var(--brand);color:#fff;border:none;border-radius:10px;padding:11px 22px;font-size:.95rem;font-weight:700;cursor:pointer}
.btn:disabled{background:#cbd5e1;cursor:not-allowed}
.btn.ghost{background:#fff;color:var(--brand);border:2px solid var(--brand)}
.qtimeta{font-size:.68rem;color:var(--muted);font-family:ui-monospace,Menlo,monospace;margin-top:14px;border-top:1px dashed var(--line);padding-top:8px}
.done{text-align:center;padding:40px 20px}
.done h2{color:var(--ok)}
</style></head><body>
<div class="banner">PREVIEW: a local simulation of the Timeback student player. Interaction model + content are faithful; this is <b>not</b> the QTI payload (Timeback strips JS from stimuli). One item per screen, exactly as a student would step through it.</div>
<div class="topbar"><div class="t">__TITLE__</div><div class="sub">__TARGET__</div>
  <div class="progwrap"><div class="progbar"><div class="progfill" id="pf"></div></div><div class="progtext" id="pt"></div></div>
</div>
<div class="stage"><div id="screen"></div>
  <div class="nav"><button class="btn ghost" id="back" onclick="go(-1)">Back</button><button class="btn" id="next" onclick="advance()">Continue</button></div>
</div>
<script>
const SCREENS = __DATA__;
const TOTAL = __COUNT__;
let idx = 0;
const answered = {};  // screen index -> {picked, submitted}

function esc(s){return (s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}

function render(){
  const s = SCREENS[idx];
  document.getElementById("pf").style.width = ((idx)/TOTAL*100)+"%";
  document.getElementById("pt").textContent = "Step "+(idx+1)+" of "+TOTAL+"  |  "+s.role_label;
  let h = '<div class="card"><span class="phase">'+esc(s.role_label)+'</span><h2 class="qtitle">'+esc(s.title)+'</h2>';
  const next = document.getElementById("next");
  const back = document.getElementById("back");
  back.style.visibility = idx===0 ? "hidden":"visible";

  if(s.type==="read"){
    h += '<div class="body">'+esc(s.body)+'</div>';
    next.textContent = "Continue"; next.disabled=false; next.dataset.mode="advance";
  }
  else if(s.type==="source"){
    h += '<div class="body">'+esc(s.body)+'</div>';
    h += '<div class="srcpane">';
    for(const p of s.passages){ h+='<div class="srctitle">'+esc(p.title)+'</div><div class="srctext">'+esc(p.text)+'</div>'; }
    h += '</div>';
    next.textContent = "Continue"; next.disabled=false; next.dataset.mode="advance";
  }
  else if(s.type==="choice"){
    h += '<div class="stem">'+esc(s.stem)+'</div><div class="opts" id="opts">';
    const st = answered[idx];
    s.options.forEach(o=>{
      let cls="opt";
      if(st&&st.submitted){ cls+=" disabled";
        if(o.letter===s.correct) cls+=" correct";
        else if(o.letter===st.picked) cls+=" wrong";
      } else if(st&&st.picked===o.letter){ cls+=" sel"; }
      h+='<div class="'+cls+'" onclick="pick(\''+o.letter+'\')"><span class="let">'+o.letter+'</span><span>'+esc(o.text)+'</span></div>';
    });
    h += '</div>';
    const rc = (st&&st.submitted&&st.picked===s.correct);
    h += '<div class="reveal '+(rc?"rc":"rw")+(st&&st.submitted?" show":"")+'" id="reveal"><b>'+(rc?"Correct":"Not quite")+'</b>'+esc(s.explanation)+'</div>';
    if(st&&st.submitted){ next.textContent="Continue"; next.disabled=false; next.dataset.mode="advance"; }
    else { next.textContent="Submit"; next.disabled=!(st&&st.picked); next.dataset.mode="submit"; }
  }
  else if(s.type==="frq"){
    h += '<div class="goal"><b>Your task.</b> '+esc(s.prompt)+'</div>';
    h += '<textarea id="ta" placeholder="Write your response here..." oninput="onType()">'+(answered[idx]?esc(answered[idx].text||""):"")+'</textarea>';
    h += '<div class="graderbox" id="gb"><b>Sent to the writing grader.</b> In Timeback this response goes to the external grader ('+(s.rubric?esc(s.rubric):"rubric")+'), which returns a score and feedback keyed to the goal above. (No live grader in this preview.)</div>';
    const st = answered[idx];
    if(st&&st.submitted){ next.textContent="Continue"; next.disabled=false; next.dataset.mode="advance"; }
    else { next.textContent="Submit to grader"; next.disabled=!(st&&st.text&&st.text.trim().length>10); next.dataset.mode="submitfrq"; }
  }
  h += '<div class="qtimeta">item type: '+esc(s.kind)+'  |  QTI: '+(s.type==="choice"?"choice (select + feedback)":s.type==="frq"?"extended-text + ExternalApiScore":"stimulus (display-only)")+'</div>';
  h += '</div>';
  document.getElementById("screen").innerHTML = h;
}

function pick(letter){ const st=answered[idx]||{}; if(st.submitted) return; st.picked=letter; answered[idx]=st; render(); }
function onType(){ const st=answered[idx]||{}; st.text=document.getElementById("ta").value; answered[idx]=st; const n=document.getElementById("next"); n.disabled=!(st.text.trim().length>10); }
function advance(){
  const mode=document.getElementById("next").dataset.mode;
  if(mode==="submit"){ answered[idx].submitted=true; render(); return; }
  if(mode==="submitfrq"){ answered[idx].submitted=true; document.getElementById("gb").classList.add("show"); render(); document.getElementById("gb").classList.add("show"); return; }
  go(1);
}
function go(d){ idx+=d; if(idx>=TOTAL){ finish(); return; } if(idx<0) idx=0; render(); }
function finish(){
  document.getElementById("pf").style.width="100%";
  document.getElementById("pt").textContent="Complete";
  document.getElementById("screen").innerHTML='<div class="card done"><h2>Lesson complete</h2><p>You stepped through all '+TOTAL+' items, one at a time, the way a student would in the Timeback player.</p></div>';
  document.querySelector(".nav").style.display="none";
}
render();
</script></body></html>"""


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(LESSON_DIR, "lesson_t1_source_reading.py")
    out = render(target)
    print(f"Rendered student-player preview -> {os.path.relpath(out, HERE)}")
