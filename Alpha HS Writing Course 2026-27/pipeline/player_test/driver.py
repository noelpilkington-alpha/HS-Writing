"""
player_test/driver.py  -  thin wrapper over the gstack `browse` (Playwright) CLI.

One place that knows the CLI. Exposes the ops the checks need: goto, eval-JS (returns parsed JSON when the
expression yields JSON), click-by-text, wait, screenshot. The daemon is a persistent local Chromium the CLI
talks to; the player (content.platform.learnwith.ai) is a public SPA that renders our lesson.html with no auth.

Stdlib subprocess only. The browse binary path is discovered; if absent, Driver.available is False and the
runner degrades to expectations-only (never crashes the whole run).
"""
from __future__ import annotations
import os, subprocess, json, shutil

_CANDIDATES = [
    os.path.expanduser("~/.claude/skills/gstack/browse/dist/browse.exe"),
    os.path.expanduser("~/.claude/skills/gstack/browse/dist/browse"),
    shutil.which("browse") or "",
]


def _find_browse() -> str:
    for c in _CANDIDATES:
        if c and os.path.exists(c):
            return c
    return ""


class Driver:
    def __init__(self, timeout: int = 60):
        self.bin = _find_browse()
        self.available = bool(self.bin)
        self.timeout = timeout

    def _run(self, *args, timeout=None) -> tuple[int, str]:
        """Run one browse command. Returns (returncode, stdout+stderr)."""
        if not self.available:
            return 1, "browse binary not found"
        try:
            p = subprocess.run([self.bin, *args], capture_output=True, text=True,
                               timeout=timeout or self.timeout)
            return p.returncode, (p.stdout or "") + (p.stderr or "")
        except subprocess.TimeoutExpired:
            return 124, "timeout"
        except Exception as e:
            return 1, f"{type(e).__name__}: {e}"

    def goto(self, url: str, timeout=90) -> bool:
        rc, out = self._run("goto", url, timeout=timeout)
        return rc == 0 and "(200)" in out or (rc == 0 and "Navigated" in out)

    def wait_ms(self, ms: int) -> None:
        """Fixed pause via a JS busy-resolve (browse `wait` wants a selector; we want a time delay)."""
        # a promise that resolves after ms - browse js awaits async expressions
        self.js(f"new Promise(r => setTimeout(() => r('ok'), {int(ms)}))", timeout=max(30, ms // 1000 + 20))

    def js(self, expr: str, timeout=60):
        """Evaluate JS in the page. If the result parses as JSON, return the object; else the raw string."""
        rc, out = self._run("js", expr, timeout=timeout)
        if rc != 0:
            return {"_error": out.strip()[:200]}
        s = out.strip()
        # browse prints the value; try JSON first (our exprs return JSON.stringify(...))
        try:
            return json.loads(s)
        except Exception:
            # sometimes wrapped in quotes or prefixed; try to find the first {...} or [...]
            for a, b in (("{", "}"), ("[", "]")):
                i, j = s.find(a), s.rfind(b)
                if 0 <= i < j:
                    try:
                        return json.loads(s[i:j + 1])
                    except Exception:
                        pass
            return s

    def click_text(self, text: str, timeout=30) -> bool:
        """Click the first element whose visible text contains `text` (JS-driven; robust to the SPA's DOM)."""
        expr = ("(() => { const t=%s; const els=[...document.querySelectorAll('button,[role=button],li,label,a,div')];"
                " const el=els.find(e => (e.innerText||'').trim().includes(t) && e.offsetParent!==null);"
                " if(el){ el.click(); return 'clicked'; } return 'notfound'; })()" % json.dumps(text))
        return self.js(expr, timeout=timeout) == "clicked"

    def screenshot(self, path: str) -> bool:
        rc, out = self._run("screenshot", path)
        return rc == 0 and "saved" in out.lower()

    def body_text(self, limit=1200) -> str:
        r = self.js(f"document.body.innerText.slice(0,{limit}).replace(/\\s+/g,' ')")
        return r if isinstance(r, str) else ""
