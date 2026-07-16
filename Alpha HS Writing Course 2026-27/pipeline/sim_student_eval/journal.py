"""The external, bounded, on-disk learner memory. One JSON line per lesson.
This is the ONLY memory carried between lessons (no raw transcripts), so context
stays constant-size and every downstream finding traces to an inspectable entry."""
import json, os

_LIST_KEYS = ("skills_i_can_now_do", "terms_learned", "where_i_struggled", "open_questions")
_MAX_LIST = 12
_MAX_STR = 400


def _clip_str(s):
    return str(s)[:_MAX_STR]


def validate_entry(entry: dict) -> dict:
    if "lesson" not in entry or "seq" not in entry:
        raise ValueError("journal entry needs 'lesson' and 'seq'")
    out = {"lesson": str(entry["lesson"]), "seq": int(entry["seq"])}
    for k in _LIST_KEYS:
        vals = entry.get(k) or []
        if not isinstance(vals, list):
            vals = [vals]
        out[k] = [_clip_str(v) for v in vals[:_MAX_LIST]]
    fr = entry.get("felt_repeated")
    if isinstance(fr, dict) and fr.get("echoes_lesson"):
        out["felt_repeated"] = {"echoes_lesson": _clip_str(fr.get("echoes_lesson", "")),
                                "what": _clip_str(fr.get("what", ""))}
    else:
        out["felt_repeated"] = None
    conf = entry.get("confidence") or {}
    out["confidence"] = {str(k)[:60]: float(v) for k, v in conf.items()
                         if isinstance(v, (int, float))} if isinstance(conf, dict) else {}
    return out


class JournalStore:
    def __init__(self, path: str):
        self.path = path

    def append(self, entry: dict) -> None:
        e = validate_entry(entry)
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    def entries(self) -> list:
        if not os.path.exists(self.path):
            return []
        rows = []
        for line in open(self.path, encoding="utf-8"):
            line = line.strip()
            if line:
                rows.append(json.loads(line))
        return rows

    def digest(self) -> str:
        """A compact running-memory string for the NEXT lesson call. Bounded: only the
        cumulative skill list, current confidence, and the last 5 lessons' struggles/questions."""
        rows = self.entries()
        if not rows:
            return "(You are starting the course. You have learned nothing yet.)"
        skills = []
        conf = {}
        for r in rows:
            for s in r.get("skills_i_can_now_do", []):
                if s not in skills:
                    skills.append(s)
            conf.update(r.get("confidence", {}))
        recent = rows[-5:]
        lines = ["LESSONS DONE: " + ", ".join(r["lesson"] for r in rows)]
        lines.append("SKILLS I CAN DO: " + ("; ".join(skills[:20]) or "none yet"))
        lines.append("MY CONFIDENCE: " + ("; ".join(f"{k}={v:.1f}" for k, v in list(conf.items())[:15]) or "n/a"))
        struggles = [s for r in recent for s in r.get("where_i_struggled", [])]
        if struggles:
            lines.append("RECENT STRUGGLES: " + "; ".join(struggles[:6]))
        opens = [q for r in recent for q in r.get("open_questions", [])]
        if opens:
            lines.append("MY OPEN QUESTIONS: " + "; ".join(opens[:6]))
        return "\n".join(lines)[:4000]
